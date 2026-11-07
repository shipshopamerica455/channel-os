"""Turn the activity map into a shot list of zooms → zooms.json

    python3 tools/plan_zooms.py <project> [--max-zoom 1.75] [--hold 3.5]

Rules that keep it watchable rather than seasick:
  * one crop per hold window (default 3.5s) — never chase the cursor frame to frame
  * adjacent windows within `merge_tolerance` collapse into one continuous hold
  * when the action is spread across the whole screen (a full-page redraw, a
    transition, a preview playing) it pulls back to wide instead of guessing
  * the opening seconds are always wide, so the viewer gets their bearings first
  * crop never exceeds `max_zoom`, so a 1080p source never turns to mush
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import brand, load, project, save, timecode

SPREAD_WIDE = 0.62  # activity box wider than this fraction of frame → stay wide


def fit_box(cx, cy, w, h, aspect, max_zoom, margin):
    """Grow a normalised activity box to the output aspect, honour the zoom cap."""
    w = w * (1 + margin) + 0.06
    h = h * (1 + margin) + 0.06
    # force the output aspect: in normalised source units the frame is 1x1, so
    # the target box ratio is already folded into `aspect`
    if w / max(h, 1e-6) < aspect:
        w = h * aspect
    else:
        h = w / aspect
    # never crop tighter than the zoom cap allows
    floor = 1.0 / max_zoom
    if w < floor:
        k = floor / w
        w, h = w * k, h * k
    # never crop looser than the frame
    if w > 1.0 or h > 1.0:
        k = min(1.0 / w, 1.0 / h)
        w, h = w * k, h * k
    x = min(max(cx - w / 2, 0.0), 1.0 - w)
    y = min(max(cy - h / 2, 0.0), 1.0 - h)
    return [round(x, 4), round(y, 4), round(w, 4), round(h, 4)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--hold", type=float)
    ap.add_argument("--max-zoom", type=float)
    ap.add_argument("--margin", type=float)
    args = ap.parse_args()

    proj = project(args.project)
    b = brand()
    cfg = b["zoom"]
    hold = args.hold or cfg["hold_seconds"]
    max_zoom = args.max_zoom or cfg["max_zoom"]
    margin = args.margin if args.margin is not None else cfg["margin"]

    act = load(proj / "activity.json")
    duration = act["duration"]
    pts = act["points"]
    src_aspect = act["width"] / act["height"]
    out_aspect = b["video"]["width"] / b["video"]["height"]
    # crop is expressed in normalised source units, so the target box ratio is
    # the output ratio divided by the source ratio
    aspect = out_aspect / src_aspect

    wide = [0.0, 0.0, 1.0, 1.0]
    segments = []
    n_windows = max(1, int(np.ceil(duration / hold)))
    for i in range(n_windows):
        s, e = i * hold, min((i + 1) * hold, duration)
        win = [p for p in pts if s <= p["t"] < e]
        if s < cfg["open_wide_seconds"] or len(win) < 3:
            segments.append({"start": s, "end": e, "crop": wide, "reason": "wide"})
            continue
        energy = np.array([p["energy"] for p in win])
        wts = energy / energy.sum()
        cx = float(np.dot([p["cx"] for p in win], wts))
        cy = float(np.dot([p["cy"] for p in win], wts))
        x0 = float(np.percentile([p["x0"] for p in win], 15))
        x1 = float(np.percentile([p["x1"] for p in win], 85))
        y0 = float(np.percentile([p["y0"] for p in win], 15))
        y1 = float(np.percentile([p["y1"] for p in win], 85))
        bw, bh = max(x1 - x0, 0.02), max(y1 - y0, 0.02)
        if bw > SPREAD_WIDE and bh > SPREAD_WIDE:
            segments.append({"start": s, "end": e, "crop": wide, "reason": "spread"})
            continue
        crop = fit_box(cx, cy, bw, bh, aspect, max_zoom, margin)
        segments.append({"start": s, "end": e, "crop": crop, "reason": "focus"})

    tol = cfg["merge_tolerance"]
    merged = []
    for seg in segments:
        if merged and max(abs(a - c) for a, c in zip(merged[-1]["crop"], seg["crop"])) < tol:
            merged[-1]["end"] = seg["end"]
            continue
        merged.append(dict(seg))

    # a single-window blip between two identical holds reads as a twitch — drop it
    cleaned = []
    for i, seg in enumerate(merged):
        short = seg["end"] - seg["start"] < hold * 1.2
        neighbours_match = (
            0 < i < len(merged) - 1
            and max(abs(a - c) for a, c in zip(merged[i - 1]["crop"], merged[i + 1]["crop"])) < tol
        )
        if short and neighbours_match and cleaned:
            cleaned[-1]["end"] = seg["end"]
            continue
        cleaned.append(seg)

    for seg in cleaned:
        seg["zoom"] = round(1.0 / max(seg["crop"][2], 1e-6), 3)
        seg["start"], seg["end"] = round(seg["start"], 3), round(seg["end"], 3)

    save(proj / "zooms.json", {
        "input": act["input"], "duration": duration,
        "width": act["width"], "height": act["height"],
        "settings": {"hold": hold, "max_zoom": max_zoom, "margin": margin,
                     "transition": cfg["transition_seconds"]},
        "segments": cleaned,
    })

    zoomed = [s for s in cleaned if s["zoom"] > 1.02]
    hold_avg = np.mean([s["end"] - s["start"] for s in cleaned]) if cleaned else 0
    print(f"zoom plan: {len(cleaned)} shots, {len(zoomed)} pushed in, "
          f"avg hold {hold_avg:.1f}s, peak {max((s['zoom'] for s in cleaned), default=1):.2f}x")
    for s in cleaned[:12]:
        print(f"  {timecode(s['start'])}–{timecode(s['end'])}  {s['zoom']:.2f}x  {s['reason']}")
    if len(cleaned) > 12:
        print(f"  … {len(cleaned) - 12} more")
    print(proj / "zooms.json")


if __name__ == "__main__":
    main()
