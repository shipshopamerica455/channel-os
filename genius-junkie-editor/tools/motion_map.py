"""Where is the action on screen? → activity.json

    python3 tools/motion_map.py <project> [--input master.mp4] [--fps 4]

Screen-recording tutorials have one thing going for them: the only pixels that
change are the ones the viewer needs to look at. Cursor moves, a menu opening, a
slider dragging. This samples the video at low res, diffs consecutive frames, and
records where the change is — no cursor tracking, no CV models, works on Canva,
CapCut, a browser, anything.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import ffprobe, project, save, stage_input

SAMPLE_W = 320  # analysis resolution; results are normalised 0..1 so this is free


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--input")
    ap.add_argument("--fps", type=float, default=4.0)
    ap.add_argument("--threshold", type=int, default=12, help="8-bit change floor")
    args = ap.parse_args()

    proj = project(args.project)
    src = Path(args.input) if args.input else stage_input(proj, "master.mp4")
    info = ffprobe(src)
    sw = SAMPLE_W
    sh = max(2, int(round(sw * info["height"] / info["width"] / 2)) * 2)

    import subprocess
    cmd = ["ffmpeg", "-v", "error", "-i", str(src),
           "-vf", f"fps={args.fps},scale={sw}:{sh},format=gray",
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    frame_bytes = sw * sh
    prev, points, idx = None, [], 0
    while True:
        buf = proc.stdout.read(frame_bytes)
        if len(buf) < frame_bytes:
            break
        frame = np.frombuffer(buf, dtype=np.uint8).reshape(sh, sw).astype(np.int16)
        t = idx / args.fps
        idx += 1
        if prev is not None:
            diff = np.abs(frame - prev)
            mask = diff > args.threshold
            n = int(mask.sum())
            if n >= 6:
                ys, xs = np.nonzero(mask)
                # percentiles, not min/max — one stray compression artefact in a
                # corner must not drag the crop box across the screen
                x0, x1 = np.percentile(xs, [4, 96])
                y0, y1 = np.percentile(ys, [4, 96])
                points.append({
                    "t": round(t, 3),
                    "cx": round(float(xs.mean()) / sw, 4),
                    "cy": round(float(ys.mean()) / sh, 4),
                    "x0": round(float(x0) / sw, 4), "x1": round(float(x1) / sw, 4),
                    "y0": round(float(y0) / sh, 4), "y1": round(float(y1) / sh, 4),
                    "energy": round(n / (sw * sh), 5),
                })
        prev = frame
    proc.stdout.close()
    proc.wait()

    save(proj / "activity.json", {
        "input": src.name, "fps": args.fps,
        "duration": info["duration"],
        "width": info["width"], "height": info["height"],
        "points": points,
    })
    live = len(points) / max(1, idx) * 100
    print(f"activity: {len(points)} moving frames of {idx} sampled ({live:.0f}% live)")
    print(proj / "activity.json")


if __name__ == "__main__":
    main()
