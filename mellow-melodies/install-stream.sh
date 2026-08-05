#!/bin/bash
# Install the Mellow Melodies 24/7 stream as a launchd service.
#
#   ./install-stream.sh "Monk Mode.mp4"   install and start
#   ./install-stream.sh --stop            stop and uninstall
#   ./install-stream.sh --status          is it running?
#
# Why launchd rather than just running ffmpeg: a stream started from a terminal dies
# with the terminal, and one started from an agent session dies with the session. This
# has to survive logout, sleep/wake and crashes for months. KeepAlive restarts it if it
# ever exits — a dropped stream zeroes the concurrent-viewer count, so fast recovery is
# the difference between accruing watch hours and not.
set -euo pipefail

LABEL="com.mellowmelodies.stream"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
DIR="/Users/admin/Documents/Kimi Extension v1/mellow-melodies"
LOG="$DIR/stream.log"
NODE="$(command -v node || echo /opt/homebrew/bin/node)"

case "${1:-}" in
  --status)
    launchctl list | grep -q "$LABEL" && echo "loaded: yes" || echo "loaded: no"
    pgrep -f "stream.mjs --source" >/dev/null && echo "streaming: yes" || echo "streaming: no"
    [ -f "$LOG" ] && { echo "--- last 10 log lines ---"; tail -10 "$LOG"; }
    exit 0 ;;
  --stop)
    launchctl unload "$PLIST" 2>/dev/null || true
    rm -f "$PLIST"
    pkill -f "stream.mjs --source" 2>/dev/null || true
    echo "stopped and uninstalled."
    exit 0 ;;
  "")
    echo "usage: ./install-stream.sh \"Monk Mode.mp4\" | --stop | --status"; exit 1 ;;
esac

SOURCE="$1"

cat > "$PLIST" <<PLIST_END
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>$NODE</string>
    <string>$DIR/stream.mjs</string>
    <string>--source</string>
    <string>$SOURCE</string>
  </array>
  <key>WorkingDirectory</key><string>$DIR</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>ThrottleInterval</key><integer>30</integer>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
</dict>
</plist>
PLIST_END

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

echo "installed: $LABEL"
echo "  source : $SOURCE"
echo "  log    : $LOG"
echo "  starts at boot, restarts if it ever drops"
echo
echo "check with:  ./install-stream.sh --status"
echo "stop with :  ./install-stream.sh --stop"
