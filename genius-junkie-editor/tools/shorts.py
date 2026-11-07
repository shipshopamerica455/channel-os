"""Cut a vertical Short out of the finished tutorial.

    python3 tools/shorts.py <project> --start 154 --end 205 --slug transitions
    python3 tools/shorts.py <project> --from-clips        # batch from shorts.json

Reframes 16:9 → 9:16 by following the same activity map the zooms use, so the
crop lands on the Canva panel or the CapCut timeline rather than the middle of
the screen. Captions are re-timed to the clip and sized for a phone.

shorts.json format:
  [{"slug": "transitions", "start": 154, "end": 205, "headline": "Free CapCut transitions"}]
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from captions import build_ass
from common import (all_words, brand, ffprobe, load, project, run, stage_input,
                    timecode)


def focus_x(activity, start, end, src_w, crop_w):
    """Weighted centre of on-screen activity during the clip, in source pixels."""
    pts = [p for p in (activity or {}).get("points", []) if start <= p["t"] <= end]
    if not pts:
        return (src_w - crop_w) / 2
    energy = np.array([p["energy"] for p in pts])
    cx = float(np.dot([p["cx"] for p in pts], energy / energy.sum())) * src_w
    return min(max(cx - crop_w / 2, 0), src_w - crop_w)


def build(proj, b, src, activity, slug, start, end, headline):
    info = ffprobe(src)
    sw, sh = info["width"], info["height"]
    ow, oh = b["shorts"]["width"], b["shorts"]["height"]
    dur = end - start
    if dur > b["shorts"]["max_seconds"]:
        print(f"  ! {slug}: {dur:.0f}s is over the {b['shorts']['max_seconds']}s "
              f"Shorts limit — trimming")
        end = start + b["shorts"]["max_seconds"]
        dur = end - start

    # tallest 9:16 window the source can give, then pan it onto the action
    crop_w = min(sw, int(sh * ow / oh))
    crop_w -= crop_w % 2
    x = int(focus_x(activity, start, end, sw, crop_w)) // 2 * 2

    out_dir = proj / "shorts"
    out_dir.mkdir(exist_ok=True)
    clip = out_dir / f"{slug}.mp4"

    vf = [f"crop={crop_w}:{sh}:{x}:0", f"scale={ow}:{oh}:flags=lanczos", "setsar=1"]
    if headline:
        safe = headline.replace(":", r"\:").replace("'", "")
        vf.append(
            f"drawtext=text='{safe}':fontcolor=white:fontsize=64:borderw=5:"
            f"bordercolor={b['colors']['ink']}:x=(w-text_w)/2:y=180:"
            f"box=1:boxcolor={b['colors']['accent']}@0.85:boxborderw=24"
        )

    # captions re-timed to the clip, sized for a phone
    tx_path = proj / "transcript.cut.json"
    if tx_path.exists():
        words = [{**w, "start": round(w["start"] - start, 3), "end": round(w["end"] - start, 3)}
                 for w in all_words(load(tx_path)) if start <= w["start"] < end]
        if words:
            ass = out_dir / f"{slug}.ass"
            ass.write_text(build_ass(words, b, ow, oh, vertical=True))
            esc = str(ass).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
            vf.append(f"subtitles='{esc}'")

    v = b["video"]
    cmd = ["ffmpeg", "-y", "-ss", f"{start:.3f}", "-i", str(src), "-t", f"{dur:.3f}",
           "-vf", ",".join(vf), "-c:v", "libx264", "-preset", v["preset"],
           "-crf", str(v["crf"]), "-pix_fmt", v["pix_fmt"],
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(clip)]
    run(cmd)
    print(f"  {slug}: {timecode(start)}–{timecode(end)} ({dur:.0f}s) → {clip.name}")
    return clip


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--input")
    ap.add_argument("--start", type=float)
    ap.add_argument("--end", type=float)
    ap.add_argument("--slug", default="short")
    ap.add_argument("--headline")
    ap.add_argument("--from-clips", action="store_true")
    args = ap.parse_args()

    proj = project(args.project)
    b = brand()
    src = Path(args.input) if args.input else stage_input(proj, "final.mp4")
    activity = load(proj / "activity.json", default={})

    if args.from_clips:
        clips = load(proj / "shorts.json")
        print(f"building {len(clips)} Shorts from {src.name}")
        for c in clips:
            build(proj, b, src, activity, c["slug"], float(c["start"]), float(c["end"]),
                  c.get("headline"))
        return

    if args.start is None or args.end is None:
        raise SystemExit("give --start and --end, or --from-clips with shorts.json")
    build(proj, b, src, activity, args.slug, args.start, args.end, args.headline)


if __name__ == "__main__":
    main()
