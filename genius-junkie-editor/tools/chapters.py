"""Chapters + description assembly.

    python3 tools/chapters.py <project> --outline    # transcript digest for Claude to read
    python3 tools/chapters.py <project> --build      # chapters.json + packaging.json → description.txt

Tutorials live or die on chapters — viewers skip to the step they are stuck on,
and YouTube surfaces them as key moments. Claude authors chapters.json from the
outline; this file only handles the digest and the formatting.

chapters.json format: [{"t": 0, "title": "Intro"}, {"t": 41.2, "title": "Set the canvas size"}]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import brand, load, project, timecode


def hhmmss(t):
    t = max(0, int(t))
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--outline", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--window", type=float, default=20.0)
    args = ap.parse_args()

    proj = project(args.project)
    b = brand()

    if args.outline or not args.build:
        tx = load(proj / "transcript.cut.json") if (proj / "transcript.cut.json").exists() \
            else load(proj / "transcript.json")
        print(f"# {proj.name} — {timecode(tx.get('duration', 0))}\n")
        bucket, start = [], 0.0
        for seg in tx["segments"]:
            if seg["start"] - start >= args.window and bucket:
                print(f"[{hhmmss(start)}] {' '.join(bucket)}")
                bucket, start = [], seg["start"]
            bucket.append(seg["text"])
        if bucket:
            print(f"[{hhmmss(start)}] {' '.join(bucket)}")
        return

    chapters = load(proj / "chapters.json")
    pack = load(proj / "packaging.json", default={})
    if chapters and chapters[0]["t"] > 0:
        chapters = [{"t": 0, "title": "Intro"}] + chapters

    lines = []
    hook = pack.get("description_hook") or pack.get("summary")
    if hook:
        lines += [hook.strip(), ""]
    lines.append("⏱️ Chapters")
    lines += [f"{hhmmss(c['t'])} {c['title']}" for c in chapters]
    if pack.get("tools_used"):
        lines += ["", "🧰 Used in this tutorial", *[f"• {t}" for t in pack["tools_used"]]]
    if pack.get("links"):
        lines += ["", "🔗 Links"] + [f"• {k}: {v}" for k, v in pack["links"].items()]
    lines.append(b["packaging"]["description_footer"].rstrip())
    if pack.get("tags"):
        lines += ["", " ".join(f"#{t.replace(' ', '')}" for t in pack["tags"][:12])]

    text = "\n".join(lines).strip() + "\n"
    (proj / "description.txt").write_text(text)
    print(text)
    print(f"--- {len(text)} chars, {len(chapters)} chapters")
    print(proj / "description.txt")


if __name__ == "__main__":
    main()
