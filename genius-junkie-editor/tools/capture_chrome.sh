#!/bin/bash
# Capture the frontmost Chrome window to a named shot file.
#   tools/capture_chrome.sh <project-dir> <shot-name>
# Full-screen retina grab cropped to Chrome's window bounds (points × 2).
set -euo pipefail
PROJ="$1"; NAME="$2"
mkdir -p "$PROJ/shots"
OUT="$PROJ/shots/$NAME.png"
TMP="$(mktemp /tmp/gjcap-XXXX).png"

osascript -e 'tell application "Google Chrome" to activate' >/dev/null
sleep 0.6
BOUNDS=$(osascript -e 'tell application "Google Chrome" to get bounds of front window')
screencapture -x "$TMP"

python3 - "$TMP" "$OUT" "$BOUNDS" <<'PY'
import sys
from PIL import Image
tmp, out, bounds = sys.argv[1], sys.argv[2], sys.argv[3]
l, t, r, b = [int(x.strip()) for x in bounds.split(",")]
img = Image.open(tmp)
# retina: AppleScript bounds are points, capture is pixels
scale = 2 if img.width > 2000 else 1
img.crop((l*scale, t*scale, r*scale, b*scale)).save(out)
print(f"{out} ({(r-l)*scale}x{(b-t)*scale})")
PY
rm -f "$TMP"
