"""Brand captions burned in from the word-level transcript.

    python3 tools/captions.py <project> [--input zoomed.mp4] [--vertical] [--ass-only]

Word-timed chunks with the live word lit in the brand highlight — the thing that
keeps a tutorial legible when someone is watching muted on a phone. Reads
transcript.cut.json so the words stay locked to the cut timeline.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (all_words, brand, ffprobe, load, project, run, stage_input)


def ass_colour(hexstr):
    """#rrggbb → &HAABBGGRR& (ASS is BGR and back to front)."""
    h = hexstr.lstrip("#")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def chunk_words(words, max_words, max_seconds):
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words
                    or w["end"] - cur[0]["start"] > max_seconds
                    or w["start"] - cur[-1]["end"] > 0.7):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    return chunks


def ass_time(t):
    t = max(0.0, t)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def build_ass(words, b, width, height, vertical):
    c = b["captions"]
    size = c["size_short"] if vertical else c["size_long"]
    margin = c["margin_v_short"] if vertical else c["margin_v_long"]
    primary = ass_colour(b["colors"]["paper"])
    accent = ass_colour(b["colors"]["highlight"])
    outline = ass_colour(b["colors"]["ink"])

    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: GJ,{c['font']},{size},{primary},{primary},{outline},&H80000000,-1,0,0,0,100,100,0,0,1,{c['outline']},{c['shadow']},2,60,60,{margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    lines = []
    for chunk in chunk_words(words, c["words_per_chunk"], c["max_chunk_seconds"]):
        texts = [w["word"].upper() if c["uppercase"] else w["word"] for w in chunk]
        if not c["highlight_active_word"]:
            body = " ".join(texts).replace("{", "(").replace("}", ")")
            lines.append(f"Dialogue: 0,{ass_time(chunk[0]['start'])},"
                         f"{ass_time(chunk[-1]['end'])},GJ,,0,0,0,,{body}")
            continue
        # one event per word so exactly one word is lit at a time
        for i, w in enumerate(chunk):
            parts = []
            for j, t in enumerate(texts):
                t = t.replace("{", "(").replace("}", ")")
                parts.append(f"{{\\c{accent}}}{t}{{\\c{primary}}}" if j == i else t)
            end = chunk[i + 1]["start"] if i + 1 < len(chunk) else chunk[-1]["end"] + 0.12
            lines.append(f"Dialogue: 0,{ass_time(w['start'])},{ass_time(end)},"
                         f"GJ,,0,0,0,,{' '.join(parts)}")
    return head + "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--input")
    ap.add_argument("--out", default="captioned.mp4")
    ap.add_argument("--transcript", default="transcript.cut.json")
    ap.add_argument("--vertical", action="store_true")
    ap.add_argument("--ass-only", action="store_true")
    ap.add_argument("--offset", type=float, default=0.0, help="shift all words by N seconds")
    args = ap.parse_args()

    proj = project(args.project)
    b = brand()
    src = Path(args.input) if args.input else stage_input(proj, "zoomed.mp4")
    info = ffprobe(src)

    tx_path = proj / args.transcript
    if not tx_path.exists():
        tx_path = proj / "transcript.json"
    words = all_words(load(tx_path))
    if args.offset:
        words = [{**w, "start": w["start"] + args.offset, "end": w["end"] + args.offset}
                 for w in words]
    words = [w for w in words if w["end"] > 0]
    if not words:
        raise SystemExit("no words to caption")

    ass_path = proj / ("captions.vertical.ass" if args.vertical else "captions.ass")
    ass_path.write_text(build_ass(words, b, info["width"], info["height"], args.vertical))
    print(f"captions: {len(words)} words → {ass_path.name}")
    if args.ass_only:
        print(ass_path)
        return

    out = proj / args.out
    v = b["video"]
    # subtitles= needs the path escaped for the filtergraph parser
    esc = str(ass_path).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
    cmd = ["ffmpeg", "-y", "-i", str(src), "-vf", f"subtitles='{esc}'",
           "-c:v", "libx264", "-preset", v["preset"], "-crf", str(v["crf"]),
           "-pix_fmt", v["pix_fmt"], "-movflags", "+faststart"]
    cmd += ["-c:a", "copy"] if info["has_audio"] else ["-an"]
    cmd.append(str(out))
    run(cmd)
    print(out)


if __name__ == "__main__":
    main()
