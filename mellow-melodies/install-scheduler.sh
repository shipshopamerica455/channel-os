#!/bin/bash
# Install the Mellow Melodies auto-publisher as a launchd job.
#
#   ./install-scheduler.sh          install / reinstall
#   ./install-scheduler.sh --status show state and recent log
#   ./install-scheduler.sh --remove uninstall
#
# Runs `publish.mjs --next --go` every day at 03:17. It only acts when calendar.json has
# an unpublished slot due within 2 days, so a daily tick is cheap — most days it prints
# "nothing due" and exits. Daily rather than weekly because a missed weekly run means a
# missed upload; a missed daily one is caught the next night.
#
# launchd, not cron: launchd runs the job on wake if the Mac was asleep at the scheduled
# time, which cron does not. The build is local — this needs the machine on and awake.

set -euo pipefail

LABEL="com.mellowmelodies.autopublish"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
DIR="/Users/admin/Documents/Kimi Extension v1/mellow-melodies"
LOG="$DIR/autopublish.log"
NODE="$(command -v node)"

case "${1:-install}" in
  --status)
    launchctl list | grep -q "$LABEL" && echo "loaded: yes" || echo "loaded: no"
    [ -f "$LOG" ] && { echo "--- last 25 log lines ---"; tail -25 "$LOG"; } || echo "no log yet"
    exit 0 ;;
  --remove)
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
    rm -f "$PLIST"
    echo "removed"
    exit 0 ;;
esac

[ -n "$NODE" ] || { echo "node not found on PATH"; exit 1; }

cat > "$PLIST" <<PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>$NODE</string>
    <string>$DIR/publish.mjs</string>
    <string>--next</string>
    <string>--go</string>
  </array>
  <key>WorkingDirectory</key><string>$DIR</string>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>3</integer><key>Minute</key><integer>17</integer></dict>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
  <key>RunAtLoad</key><false/>
</dict>
</plist>
PLISTEOF

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"

echo "installed → $PLIST"
echo "runs daily 03:17, publishes any slot in calendar.json due within 2 days"
echo "log → $LOG"
echo
echo "check with:  ./install-scheduler.sh --status"
echo "run now with: launchctl kickstart gui/$(id -u)/$LABEL"
