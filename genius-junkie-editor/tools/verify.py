"""Pre-flight before anything reaches YouTube.

    python3 tools/verify.py <project>

Catches the three failures that are invisible until someone comments on them:
audio/video length mismatch, captions running past the end of the video, and a
cut that silently dropped or duplicated time.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (all_words, brand, ffprobe, load, project, run, stage_input,
                    timecode)


def stream_durations(path):
    proc = run(["ffprobe", "-v", "error", "-show_entries",
                "stream=codec_type,duration", "-of", "compact=p=0:nk=0", str(path)])
    out = {}
    for line in proc.stdout.strip().splitlines():
        kind = re.search(r"codec_type=(\w+)", line)
        dur = re.search(r"duration=([\d.]+)", line)
        if kind and dur:
            out[kind.group(1)] = float(dur.group(1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--input")
    args = ap.parse_args()

    proj = project(args.project)
    b = brand()
    src = Path(args.input) if args.input else stage_input(proj, "final.mp4")
    info = ffprobe(src)
    problems, notes = [], []

    print(f"checking {src.name} — {timecode(info['duration'])} "
          f"{info['width']}x{info['height']} @{info['fps']:.2f}fps")

    d = stream_durations(src)
    if "audio" in d and "video" in d:
        drift = abs(d["audio"] - d["video"])
        (problems if drift > 0.5 else notes).append(
            f"A/V length drift {drift:.2f}s (audio {d['audio']:.2f}s, video {d['video']:.2f}s)")
    elif "audio" not in d:
        problems.append("no audio stream")

    if info["width"] != b["video"]["width"] or info["height"] != b["video"]["height"]:
        notes.append(f"not {b['video']['width']}x{b['video']['height']} — "
                     f"got {info['width']}x{info['height']}")

    cuts_path = proj / "cuts.json"
    if cuts_path.exists():
        cuts = load(cuts_path)
        gaps = [(cuts["keeps"][i + 1][0] - cuts["keeps"][i][1])
                for i in range(len(cuts["keeps"]) - 1)]
        overlaps = [g for g in gaps if g < 0]
        if overlaps:
            problems.append(f"{len(overlaps)} overlapping keep ranges in cuts.json")
        removed_pct = cuts["removed_seconds"] / max(cuts["source_duration"], 1e-6) * 100
        if removed_pct > 45:
            notes.append(f"cut removed {removed_pct:.0f}% of the recording — "
                         f"listen back before publishing")

    tx_path = proj / "transcript.cut.json"
    if tx_path.exists():
        words = all_words(load(tx_path))
        if words:
            overrun = words[-1]["end"] - info["duration"]
            if overrun > 1.0:
                problems.append(f"captions run {overrun:.1f}s past the end of the video "
                                f"— transcript.cut.json is stale, re-run apply_cuts")

    # silence at the head reads as a dead start on a tutorial
    proc = run(["ffmpeg", "-i", str(src), "-t", "3", "-af",
                "silencedetect=noise=-40dB:d=1.2", "-f", "null", "-"], check=False)
    if "silence_start: 0" in proc.stderr:
        notes.append("over a second of silence at the top — trim the cold start")

    for path, label in [("description.txt", "description"), ("thumbnail.png", "thumbnail")]:
        if not (proj / path).exists():
            notes.append(f"no {label} yet ({path})")

    print()
    for n in notes:
        print(f"  note  {n}")
    for p in problems:
        print(f"  FAIL  {p}")
    if not problems:
        print("  pass  ready to upload" if not notes else "  pass  ready (see notes)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
