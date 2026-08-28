#!/usr/bin/env bash
# Render, upload and schedule the twelve September slots, one at a time.
#
# The batch that filled the disk this morning did so because nothing was watching
# free space and nothing reclaimed finished renders. 91 hours of runtime is roughly
# 75 GB of mp4, so this loop does both:
#
#   · before each slot, require MIN_GB free, and try pruning to get there
#   · after each upload, prune renders YouTube has confirmed (prune.mjs verifies
#     processing succeeded and the duration matches before deleting anything)
#
# A slot that fails does not stop the run — publish.mjs is resumable and re-running
# the script picks up whatever is still unpublished. Failures are listed at the end.

set -uo pipefail

MM="/Users/admin/Documents/Kimi Extension v1/mellow-melodies"
RS="/Users/admin/Documents/Kimi Extension v1/remotion-shorts"
NODE="$(command -v node)"
MIN_GB=12
SLOTS=(w7tue w7thu w7sun w8tue w8thu w8sun w9tue w9thu w9sun w10tue w10thu w10sun)

free_gb() { df -g /System/Volumes/Data | tail -1 | awk '{print $4}'; }

done_ok=(); failed=()

for slot in "${SLOTS[@]}"; do
  # Already published? publish.mjs would skip anyway; this keeps the log honest.
  if "$NODE" -e "
      const c=require('$MM/calendar.json'); const s=c['$slot'];
      process.exit(s && s.published && s.published!=='pending' ? 0 : 1);"; then
    echo "── $slot ── already published, skipping"
    continue
  fi

  if [ "$(free_gb)" -lt "$MIN_GB" ]; then
    echo "── $slot ── only $(free_gb)GB free, pruning first"
    ( cd "$RS" && "$NODE" prune.mjs --go 2>&1 | tail -3 )
  fi
  if [ "$(free_gb)" -lt "$MIN_GB" ]; then
    echo "!! stopping before $slot — $(free_gb)GB free, need ${MIN_GB}GB and pruning did not help"
    failed+=("$slot (no disk)")
    break
  fi

  echo ""
  echo "════════════════ $slot  ($(free_gb)GB free) ════════════════"
  if ( cd "$MM" && "$NODE" publish.mjs --slot "$slot" --go 2>&1 | tail -25 ); then
    done_ok+=("$slot")
  else
    echo "!! $slot FAILED — continuing"
    failed+=("$slot")
  fi

  # Reclaim whatever YouTube has finished with by now.
  ( cd "$RS" && "$NODE" prune.mjs --go 2>&1 | tail -2 )
done

echo ""
echo "════════════════ SEPTEMBER RUN COMPLETE ════════════════"
echo "published : ${#done_ok[@]}  ${done_ok[*]:-—}"
echo "failed    : ${#failed[@]}  ${failed[*]:-—}"
echo "disk      : $(free_gb)GB free"
( cd "$MM" && "$NODE" publish.mjs --status 2>&1 | grep -E "^w(7|8|9|10)" )
