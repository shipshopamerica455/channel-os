#!/bin/bash
# Build Digital Grace Records' 24/7 loop ON THE SERVER, from the uploaded album files.
#
#   scp this to the box, then:  bash build-dgr-loop.sh
#
# WHY NORMALISE FIRST. The seven albums are 25fps, 30fps and even 1fps, with differing
# encoder settings. ffmpeg's concat demuxer requires identical stream parameters, and
# the whole point of the server setup is that streaming runs `-c copy` at ~3% CPU. So
# each album is re-encoded once to the house spec (see SERVER_HANDOFF.md), with the
# overlay burned in — then concatenation and streaming are both free.
#
# The Mac was doing this live, every frame, forever, at ~45% CPU. This does it once.
set -euo pipefail

SRC=/opt/streams/dgr/src
WORK=/opt/streams/dgr/norm
OUT=/opt/streams/dgr/loop.mp4
FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf

BOTTOM_LEFT="Digital Grace Records"
BOTTOM_RIGHT="Musica Cristiana en Espanol"

[ -f "$FONT" ] || FONT=$(fc-match -f '%{file}' "DejaVu Sans:bold" 2>/dev/null || echo "")
[ -n "$FONT" ] && [ -f "$FONT" ] || { echo "no usable font found; apt install fonts-dejavu-core"; exit 1; }

mkdir -p "$WORK"

# Burned-in overlay, matching what stream.sh drew live on the Mac.
VF="scale=1920:1080:force_original_aspect_ratio=decrease,\
pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=25,setsar=1,\
drawtext=fontfile='${FONT}':text='${BOTTOM_LEFT}':fontcolor=white@0.85:fontsize=30:x=40:y=h-70:shadowcolor=black@0.6:shadowx=2:shadowy=2,\
drawtext=fontfile='${FONT}':text='${BOTTOM_RIGHT}':fontcolor=white@0.75:fontsize=26:x=w-tw-40:y=h-68:shadowcolor=black@0.6:shadowx=2:shadowy=2"

echo "normalising $(ls -1 "$SRC" | wc -l) albums to 25fps + overlay …"
i=0
for f in "$SRC"/*.mp4; do
  i=$((i+1))
  out="$WORK/$(printf '%02d' "$i").mp4"
  if [ -f "$out" ]; then echo "  [$i] cached $(basename "$f")"; continue; fi
  echo "  [$i] $(basename "$f")"
  # nice: BBTV is streaming from this box and must not be starved.
  nice -n 19 ffmpeg -y -hide_banner -loglevel error -stats -i "$f" \
    -vf "$VF" \
    -c:v libx264 -preset veryfast -b:v 2500k -maxrate 2500k -bufsize 5000k \
    -g 50 -keyint_min 50 -sc_threshold 0 -pix_fmt yuv420p \
    -c:a aac -b:a 128k -ar 44100 -ac 2 \
    "$out" 2>&1 | tr '\r' '\n' | tail -1
done

echo
echo "concatenating …"
: > "$WORK/list.txt"
for f in "$WORK"/[0-9][0-9].mp4; do echo "file '$f'" >> "$WORK/list.txt"; done

# Write to a temp name and move only on success — a half-written loop.mp4 that the
# service picks up would stream truncated content and look like a content bug.
nice -n 19 ffmpeg -y -hide_banner -loglevel error -stats \
  -f concat -safe 0 -i "$WORK/list.txt" -c copy -movflags +faststart \
  "$OUT.tmp" 2>&1 | tr '\r' '\n' | tail -1
mv "$OUT.tmp" "$OUT"

echo
echo "── result ──"
ls -lh "$OUT"
ffprobe -v error -show_entries format=duration -show_entries stream=codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1 "$OUT"
df -h / | tail -1
echo
echo "Sources kept in $SRC — rebuilding the loop later needs no upload."
