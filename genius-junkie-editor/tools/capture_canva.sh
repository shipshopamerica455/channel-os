#!/bin/bash
# Capture ONE Chrome tab's page content (no browser chrome, no personal tabs).
#   tools/capture_canva.sh <project-dir> <shot-name> <url-substring>
# Activates the tab whose URL contains the substring, captures the window,
# crops to the page viewport (bottom innerHeight points of the window).
set -euo pipefail
PROJ="$1"; NAME="$2"; SUBSTR="$3"
VIEW_PT="${4:-809}"   # window.innerHeight in points
mkdir -p "$PROJ/shots"
OUT="$PROJ/shots/$NAME.png"
TMP="$(mktemp /tmp/gjcap-XXXX).png"

osascript >/dev/null <<EOF
tell application "Google Chrome"
  activate
  set win to front window
  set n to count of tabs of win
  repeat with i from 1 to n
    if URL of tab i of win contains "$SUBSTR" then
      set active tab index of win to i
      exit repeat
    end if
  end repeat
end tell
EOF
sleep 0.8
BOUNDS=$(osascript -e 'tell application "Google Chrome" to get bounds of front window')
screencapture -x "$TMP"

python3 - "$TMP" "$OUT" "$BOUNDS" "$VIEW_PT" <<'PY'
import sys
from PIL import Image
tmp, out, bounds, view_pt = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
l, t, r, b = [int(x.strip()) for x in bounds.split(",")]
img = Image.open(tmp)
scale = 2 if img.width > 2000 else 1
win = img.crop((l*scale, t*scale, r*scale, b*scale))
crop_top = win.height - view_pt*scale
win.crop((0, max(0, crop_top), win.width, win.height)).save(out)
print(f"{out} ({win.width}x{view_pt*scale})")
PY
rm -f "$TMP"
