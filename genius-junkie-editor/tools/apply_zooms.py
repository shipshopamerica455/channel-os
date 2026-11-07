"""Render the zoom shot list → zoomed.mp4

    python3 tools/apply_zooms.py <project> [--input master.mp4]

One crop filter with per-frame expressions and smoothstep easing between shots,
so the whole timeline is a single encode pass — no per-segment renders, no
concat seams, and the audio is copied through untouched.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (brand, ffprobe, load, project, run, stage_input, timecode,
                    zoom_chain)


def keyframes(segments, trans, W, H):
    """(t, (x, y, w, h)) in source pixels, with a lead-in at each shot change."""
    keys = []
    for i, seg in enumerate(segments):
        x, y, w, h = seg["crop"]
        px = (x * W, y * H, w * W, h * H)
        if i == 0:
            keys.append((0.0, px))
        else:
            lead = min(trans, max(0.05, (seg["end"] - seg["start"]) * 0.5))
            keys.append((seg["start"], keys[-1][1]))
            keys.append((seg["start"] + lead, px))
        keys.append((seg["end"], px))
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--input")
    ap.add_argument("--out", default="zoomed.mp4")
    args = ap.parse_args()

    proj = project(args.project)
    b = brand()
    plan = load(proj / "zooms.json")
    src = Path(args.input) if args.input else stage_input(proj, "master.mp4")
    info = ffprobe(src)
    W, H = info["width"], info["height"]
    segments = plan["segments"]
    if not segments:
        raise SystemExit("zooms.json has no segments")

    trans = plan["settings"]["transition"]
    keys = keyframes(segments, trans, W, H)

    # zoompan, not scale+crop: mid-stream frame-size changes silently reset
    # crop's position expressions to 0 (verified empirically — a tracked square
    # disappears). zoompan keeps every link a constant size.
    vf = zoom_chain(keys, W, H, b["video"]["width"], b["video"]["height"],
                    fps=b["video"]["fps"])

    out = proj / args.out
    print(f"rendering {len(segments)} shots over {timecode(info['duration'])} → {out.name}")
    v = b["video"]
    cmd = ["ffmpeg", "-y", "-i", str(src), "-vf", vf,
           "-c:v", "libx264", "-preset", v["preset"], "-crf", str(v["crf"]),
           "-pix_fmt", v["pix_fmt"], "-movflags", "+faststart"]
    cmd += ["-c:a", "copy"] if info["has_audio"] else ["-an"]
    cmd.append(str(out))
    run(cmd)

    got = ffprobe(out)
    print(f"zoomed : {timecode(got['duration'])} at {got['width']}x{got['height']}")
    print(out)


if __name__ == "__main__":
    main()
