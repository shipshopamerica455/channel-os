"""Plan the cut: dead air + filler words + any manual kills → cuts.json.

    python3 tools/plan_cuts.py <project> [--min-silence 0.55] [--no-fillers]

Screen recordings are mostly dead air — waiting on menus, hunting for a button,
thinking mid-click. This collapses every silence longer than `min_silence` down
to `keep_pad` on each side, so the tutorial stays breathable but never drags.

Manual kills (bad takes) go in <project>/kills.json as [[start, end], ...] in
SOURCE time; they are merged in here. Nothing is rendered — review cuts.json first.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (all_words, brand, ffprobe, load, project, run, save,
                    source_video, timecode)


def detect_silence(src, db, min_silence):
    proc = run(["ffmpeg", "-i", str(src), "-af",
                f"silencedetect=noise={db}dB:d={min_silence}", "-f", "null", "-"],
               check=False)
    spans, start = [], None
    for line in proc.stderr.splitlines():
        m = re.search(r"silence_start:\s*(-?[\d.]+)", line)
        if m:
            start = max(0.0, float(m.group(1)))
        m = re.search(r"silence_end:\s*([\d.]+)", line)
        if m and start is not None:
            spans.append((start, float(m.group(1))))
            start = None
    return spans


def filler_spans(transcript, cfg):
    """Kill filler words, but only where they are not load-bearing."""
    words = all_words(transcript)
    norm = [re.sub(r"[^a-z']", "", w["word"].lower()) for w in words]
    singles = {f for f in cfg["fillers"] if " " not in f}
    phrases = [f.split() for f in cfg["fillers"] if " " in f]
    protected = {tuple(p.split()) for p in cfg.get("protected_fillers", [])}
    spans, hits = [], []

    i = 0
    while i < len(words):
        matched = None
        for ph in phrases:
            n = len(ph)
            if tuple(norm[i:i + n]) == tuple(ph) and tuple(ph) not in protected:
                matched = (i, i + n - 1, " ".join(ph))
                break
        if not matched and norm[i] in singles:
            matched = (i, i, norm[i])
        if matched:
            a, b, text = matched
            spans.append((words[a]["start"] - 0.04, words[b]["end"] + 0.04))
            hits.append({"t": words[a]["start"], "text": text})
            i = b + 1
        else:
            i += 1
    return spans, hits


def merge(spans):
    spans = sorted((max(0.0, a), b) for a, b in spans if b > a)
    out = []
    for a, b in spans:
        if out and a <= out[-1][1] + 0.01:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def invert(removals, duration, min_keep):
    keeps, cursor = [], 0.0
    for a, b in removals:
        if a - cursor >= min_keep:
            keeps.append([round(cursor, 3), round(a, 3)])
        cursor = max(cursor, b)
    if duration - cursor >= min_keep:
        keeps.append([round(cursor, 3), round(duration, 3)])
    return keeps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--min-silence", type=float)
    ap.add_argument("--silence-db", type=float)
    ap.add_argument("--pad", type=float)
    ap.add_argument("--no-fillers", action="store_true")
    args = ap.parse_args()

    proj = project(args.project)
    b = brand()
    cfg = b["cut"]
    min_silence = args.min_silence or cfg["min_silence"]
    db = args.silence_db or cfg["silence_db"]
    pad = args.pad if args.pad is not None else cfg["keep_pad"]

    src = source_video(proj)
    info = ffprobe(src)
    duration = info["duration"]
    transcript = load(proj / "transcript.json")

    removals, notes = [], []

    for a, b_ in detect_silence(src, db, min_silence):
        inner_a, inner_b = a + pad, b_ - pad
        if inner_b - inner_a > 0.05:
            removals.append((inner_a, inner_b))
    notes.append(f"{len(removals)} silences over {min_silence}s")

    hits = []
    if cfg["strip_fillers"] and not args.no_fillers:
        fspans, hits = filler_spans(transcript, cfg)
        removals += fspans
        notes.append(f"{len(hits)} filler words")

    kills = load(proj / "kills.json", default=[])
    if kills:
        removals += [(float(a), float(b_)) for a, b_ in kills]
        notes.append(f"{len(kills)} manual kills")

    removals = merge(removals)
    keeps = invert(removals, duration, cfg["min_keep"])
    kept = sum(b_ - a for a, b_ in keeps)

    save(proj / "cuts.json", {
        "source": src.name,
        "source_duration": round(duration, 3),
        "output_duration": round(kept, 3),
        "removed_seconds": round(duration - kept, 3),
        "settings": {"min_silence": min_silence, "silence_db": db, "pad": pad},
        "filler_hits": hits,
        "keeps": keeps,
    })

    print(f"cut plan: {', '.join(notes)}")
    print(f"  {timecode(duration)} → {timecode(kept)} "
          f"({(duration - kept) / duration * 100:.0f}% removed, {len(keeps)} segments)")
    if hits:
        preview = ", ".join(f"{h['text']}@{timecode(h['t'])}" for h in hits[:8])
        print(f"  fillers: {preview}{' …' if len(hits) > 8 else ''}")
    print(proj / "cuts.json")


if __name__ == "__main__":
    main()
