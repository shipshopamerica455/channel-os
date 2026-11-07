"""Whole pipeline, one command — raw recording in, final.mp4 out.

    python3 tools/run_all.py <project> [--model small.en] [--from cut] [--no-zoom]
                             [--music assets/bed.mp3] [--denoise] [--force]

Stages: transcribe → cut → zoom → captions → polish → verify
Each stage skips if its output already exists, so re-running is cheap and you can
restart mid-pipeline with --from. Nothing here touches YouTube.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import project, timecode

TOOLS = Path(__file__).parent
STAGES = ["transcribe", "cut", "zoom", "captions", "polish", "verify"]


def call(script, *a):
    cmd = [sys.executable, str(TOOLS / script), *[str(x) for x in a]]
    print(f"\n$ {' '.join(cmd[1:])}")
    r = subprocess.run(cmd)
    if r.returncode != 0:
        raise SystemExit(f"\nstage failed: {script}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--model", default="small.en")
    ap.add_argument("--from", dest="start_at", choices=STAGES, default="transcribe")
    ap.add_argument("--no-zoom", action="store_true")
    ap.add_argument("--no-captions", action="store_true")
    ap.add_argument("--music")
    ap.add_argument("--intro")
    ap.add_argument("--outro")
    ap.add_argument("--denoise", action="store_true")
    ap.add_argument("--force", action="store_true", help="redo stages even if output exists")
    args = ap.parse_args()

    proj = project(args.project)
    begin = STAGES.index(args.start_at)
    t0 = time.time()
    print(f"=== {proj.name} — from '{args.start_at}'")

    def wanted(stage, artefact):
        if STAGES.index(stage) < begin:
            return False
        return args.force or not (proj / artefact).exists()

    if wanted("transcribe", "transcript.json"):
        call("transcribe.py", proj, "--model", args.model, *(["--force"] if args.force else []))

    if wanted("cut", "master.mp4"):
        call("plan_cuts.py", proj)
        call("apply_cuts.py", proj)

    if not args.no_zoom and wanted("zoom", "zoomed.mp4"):
        call("motion_map.py", proj)
        call("plan_zooms.py", proj)
        call("apply_zooms.py", proj)

    if not args.no_captions and wanted("captions", "captioned.mp4"):
        call("captions.py", proj)

    if wanted("polish", "final.mp4"):
        extra = []
        for flag in ("music", "intro", "outro"):
            if getattr(args, flag):
                extra += [f"--{flag}", getattr(args, flag)]
        if args.denoise:
            extra.append("--denoise")
        call("polish.py", proj, *extra)

    print()
    subprocess.run([sys.executable, str(TOOLS / "verify.py"), str(proj)])
    print(f"\n=== done in {timecode(time.time() - t0)} → {proj / 'final.mp4'}")
    print("next: /gj-package for title + thumbnails, then /gj-publish")


if __name__ == "__main__":
    main()
