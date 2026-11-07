#!/usr/bin/env python3
"""Generate the music bed for one Genius Junkie long-form.

    python3 pipeline/audio/make_bed.py videos/<slug>            # writes bed.wav
    python3 pipeline/audio/make_bed.py videos/<slug> --audition  # 25 s sample only

Reads `video.json` → `timeline` and builds a mood plan from the section
structure, then renders it with the procedural score in music.py.

WHY THE BED IS SHAPED THIS WAY
------------------------------
This is a tutorial channel, not a documentary. The bed exists to stop the
voice sitting on silence; it must never compete with an instruction. So:

* It is quiet. `TARGET_LUFS` puts it ~22 dB under the −16 LUFS voice, which is
  the house spec (VO −16, music 20–25 dB under).
* It is calm almost everywhere. The only lift is S06, the trap — the one
  section that is a demonstration rather than an instruction.
* **IT STOPS DEAD AT BOTH AD WINDOWS.** `gj master` mutes those 1.4 s windows
  and then verifies with `silencedetect` that they are genuinely silent; a bed
  playing underneath would be muted by that filter anyway, but gapping it here
  with real fades avoids a hard cut in and out of the card. YouTube refuses
  manual mid-rolls where the audio is not silent, so this is not cosmetic.
* It fades out under the close so the CTA is the last thing heard.

The section→mood map is keyed off POSITION, not off the topic, because every
video in this series has the same 14-section shape.
"""
import argparse
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dsp import SR, secs, write_wav, rms_db, db          # noqa: E402
from music import render_score                            # noqa: E402

TARGET_LUFS = -38.0     # ~22 dB under a -16 LUFS voice
AD_FADE = 0.45          # seconds of fade either side of a silent ad window
TAIL_FADE = 4.0         # the close should land on the CTA, not on a chord


def plan_for(sections, total):
    """One contiguous mood plan across the whole runtime.

    Sections are the 14 VO stems in order. S06 is always the trap — it is the
    only place the bed is allowed to lean in, and even then only to 0.45.
    """
    if not sections:
        return [{"start": 0.0, "end": total, "mood": "calm", "intensity": 0.25}]

    starts = [s["at"] for s in sections]
    n = len(starts)
    bounds = starts + [total]

    def band(i):
        return {"start": bounds[i], "end": bounds[i + 1]}

    plan = []
    for i in range(n):
        b = band(i)
        if i == 0:                      # S01 hook — the claim
            mood, inten = "hopeful", 0.30
        elif i == 1:                    # S02 free card + principles
            mood, inten = "calm", 0.26
        elif i == 5:                    # S06 the trap, demonstrated
            mood, inten = "tension", 0.45
        elif i == n - 1:                # S14 close
            mood, inten = "hopeful", 0.30
        else:                           # the instructional body
            mood, inten = "calm", 0.22
        if plan and plan[-1]["mood"] == mood and plan[-1]["intensity"] == inten:
            plan[-1]["end"] = b["end"]  # merge, so the score does not re-seed
        else:
            plan.append({"start": b["start"], "end": b["end"], "mood": mood, "intensity": inten})
    return plan


def gap_ad_windows(x, windows):
    """Fade the bed out and back in across each designed ad break."""
    f = secs(AD_FADE)
    for a, b in windows:
        i0, i1 = secs(a), secs(b)
        i0 = max(0, min(i0, len(x)))
        i1 = max(0, min(i1, len(x)))
        if i1 <= i0:
            continue
        pre0 = max(0, i0 - f)
        if i0 > pre0:
            x[pre0:i0] *= np.linspace(1, 0, i0 - pre0)[:, None]
        x[i0:i1] = 0.0
        post1 = min(len(x), i1 + f)
        if post1 > i1:
            x[i1:post1] *= np.linspace(0, 1, post1 - i1)[:, None]
    return x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_dir")
    ap.add_argument("--out")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--audition", action="store_true", help="render only the first 25 s")
    a = ap.parse_args()

    manifest = json.load(open(os.path.join(a.video_dir, "video.json"), encoding="utf-8"))
    tl = manifest.get("timeline") or {}
    total = tl.get("total")
    if not total:
        sys.exit("no timeline.total in video.json — run `gj build <slug>` first")
    sections = tl.get("sections") or []
    windows = tl.get("adWindows") or []

    plan = plan_for(sections, total)
    if a.audition:
        total = 25.0
        plan = [p for p in plan if p["start"] < total]
        plan[-1]["end"] = total
        windows = []

    x = render_score(plan, total, a.seed)
    if windows:
        x = gap_ad_windows(x, windows)

    k = secs(TAIL_FADE)
    if len(x) > k:
        x[-k:] *= np.linspace(1, 0, k)[:, None]

    # render_score normalises to about -20 dB RMS; drop it to the house level.
    x = (x * db(TARGET_LUFS - rms_db(x))).astype(np.float32)

    out = a.out or os.path.join(a.video_dir, "bed.wav")
    write_wav(out, x)
    print(f"wrote {out}  ({len(x) / SR:.1f}s, {len(plan)} section(s), "
          f"{len(windows)} ad gap(s), ~{TARGET_LUFS:.0f} dB)")
    for p in plan:
        print(f"   {p['start']:7.1f}–{p['end']:7.1f}  {p['mood']:8s} {p['intensity']:.2f}")


if __name__ == "__main__":
    main()
