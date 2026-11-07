"""Render the cut → master.mp4, and rebase the transcript onto the new timeline.

    python3 tools/apply_cuts.py <project>

Uses trim/concat inside one filtergraph (not the concat demuxer) so audio never
drifts against video across a hundred splices. Also writes transcript.cut.json —
every later stage reads that, so captions stay locked to the words.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (brand, concat_filter, encode_args, ffprobe, load, project,
                    remap_transcript, run, save, timecode)

CHUNK = 120  # segments per pass — keeps the filtergraph parseable on long videos


def render_chunk(src, keeps, has_audio, out, b):
    fg = concat_filter(keeps, has_audio)
    cmd = ["ffmpeg", "-y", "-i", str(src), "-filter_complex", fg, "-map", "[vout]"]
    if has_audio:
        cmd += ["-map", "[aout]"]
    cmd += encode_args(b) + [str(out)]
    run(cmd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--out", default="master.mp4")
    args = ap.parse_args()

    proj = project(args.project)
    b = brand()
    cuts = load(proj / "cuts.json")
    src = proj / cuts["source"]
    if not src.exists():
        src = next(proj.rglob(cuts["source"]))
    info = ffprobe(src)
    keeps = cuts["keeps"]
    if not keeps:
        raise SystemExit("cuts.json has no keep ranges")

    out = proj / args.out
    print(f"rendering {len(keeps)} segments → {out.name}")

    if len(keeps) <= CHUNK:
        render_chunk(src, keeps, info["has_audio"], out, b)
    else:
        tmp = proj / ".chunks"
        tmp.mkdir(exist_ok=True)
        parts = []
        for i in range(0, len(keeps), CHUNK):
            part = tmp / f"part{i // CHUNK:03d}.mp4"
            print(f"  chunk {i // CHUNK + 1}/{-(-len(keeps) // CHUNK)}")
            render_chunk(src, keeps[i:i + CHUNK], info["has_audio"], part, b)
            parts.append(part)
        listing = tmp / "list.txt"
        listing.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
             "-c", "copy", str(out)])

    transcript = load(proj / "transcript.json")
    cut_tx = remap_transcript(transcript, keeps)
    save(proj / "transcript.cut.json", cut_tx)

    got = ffprobe(out)
    drift = got["duration"] - cuts["output_duration"]
    print(f"master : {timecode(got['duration'])} "
          f"(planned {timecode(cuts['output_duration'])}, drift {drift:+.2f}s)")
    print(f"words  : {sum(len(s['words']) for s in cut_tx['segments'])} rebased")
    print(out)


if __name__ == "__main__":
    main()
