#!/usr/bin/env bash
# Convert WAV masters to FLAC, verifying each one before the WAV is removed.
#
#   ./flac-masters.sh "<dir>"          # dry run
#   ./flac-masters.sh "<dir>" --go     # convert and replace
#
# FLAC is lossless, so this is not a quality decision — on this estate it measured
# 52-68% smaller across hymn compilations, podcast audio and generated music.
#
# It is still a decision about trust, because the WAV gets deleted. So every file is
# verified before its source goes: the FLAC is decoded back to raw PCM and MD5-summed
# against the original's PCM. Identical sums mean the audio round-trips bit for bit.
# A mismatch, a failed encode, or a missing output leaves the WAV untouched.
#
# Deliberately NOT run over the whole volume. Twelve scripts in this repo read or write
# .wav, and some use a file's existence as state — flowmusic.mjs did exactly that, and
# reclaiming space under it would have silently respent Flow Music credits regenerating
# takes that were already on disk. Point this at finished-master folders, not at working
# directories inside an active pipeline.

#
# Every ffmpeg call passes -nostdin. Without it ffmpeg inherits the loop's stdin, which
# is the find stream feeding the loop, swallows part of it, and the next iteration gets
# a truncated path. The first run failed 72 of 161 files that way, with errors like
# "stat: Users/admin/..." — a path missing its leading slash.

set -uo pipefail
DIR="${1:-}"
GO="${2:-}"
[ -z "$DIR" ] && { echo "usage: $0 \"<dir>\" [--go]"; exit 1; }
[ -d "$DIR" ] || { echo "no such directory: $DIR"; exit 1; }

command -v flac >/dev/null 2>&1 || HAVE_FLAC=0
before=0; after=0; done_n=0; skip_n=0; fail_n=0

while IFS= read -r -d '' w; do
  f="${w%.*}.flac"
  [ -f "$f" ] && { echo "  skip (flac exists): $(basename "$w")"; skip_n=$((skip_n+1)); continue; }
  ws=$(stat -f%z "$w")

  if [ "$GO" != "--go" ]; then
    before=$((before+ws)); done_n=$((done_n+1)); continue
  fi

  if ! ffmpeg -nostdin -y -v error -i "$w" -c:a flac -compression_level 8 "$f" 2>/dev/null; then
    echo "  FAILED encode, wav kept: $(basename "$w")"; rm -f "$f"; fail_n=$((fail_n+1)); continue
  fi

  # Bit-exactness: decode both to raw PCM and compare. Anything but a match keeps the wav.
  a=$(ffmpeg -nostdin -v error -i "$w" -f s32le -c:a pcm_s32le - 2>/dev/null | md5)
  b=$(ffmpeg -nostdin -v error -i "$f" -f s32le -c:a pcm_s32le - 2>/dev/null | md5)
  if [ -z "$a" ] || [ "$a" != "$b" ]; then
    echo "  CHECKSUM MISMATCH, wav kept: $(basename "$w")"; rm -f "$f"; fail_n=$((fail_n+1)); continue
  fi

  fs_=$(stat -f%z "$f")
  rm -f "$w"
  before=$((before+ws)); after=$((after+fs_)); done_n=$((done_n+1))
done < <(find "$DIR" -name "*.wav" -type f ! -path "*/Gloria Eterna Album/Vol 3/*" -print0)
# Vol 3 is excluded because video-forge/gen-gloria-vol3.mjs names those wavs literally
# ("GLORIA_ETERNA_VOL3-Eterno_Rey.wav" and so on). Renaming the extension under a script
# that hardcodes filenames breaks it silently, and 639 MB is not worth that.

if [ "$GO" != "--go" ]; then
  echo "  DRY RUN: $done_n wavs, $(echo "scale=2;$before/1000000000"|bc) GB"
  echo "  at the measured ~60% ratio that is about $(echo "scale=2;$before*0.6/1000000000"|bc) GB freed"
  echo "  add --go to convert (each file is checksum-verified before its wav is removed)"
else
  echo "  converted $done_n · skipped $skip_n · failed $fail_n"
  echo "  $(echo "scale=2;$before/1000000000"|bc) GB -> $(echo "scale=2;$after/1000000000"|bc) GB" \
       "(freed $(echo "scale=2;($before-$after)/1000000000"|bc) GB)"
fi
