"""Word-level transcription with local Whisper — no API key, no per-minute cost.

    python3 tools/transcribe.py <project> [--model small.en] [--force]

Writes <project>/transcript.json: {duration, segments:[{start,end,text,words:[...]}]}
Every later stage rides on these timestamps.
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import die, ffprobe, project, run, save, source_video


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--model", default="small.en",
                    help="tiny.en | base.en | small.en (default) | medium.en")
    ap.add_argument("--source", help="override the input file")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    proj = project(args.project)
    out = proj / "transcript.json"
    if out.exists() and not args.force:
        print(f"transcript.json exists — use --force to redo\n{out}")
        return

    src = Path(args.source) if args.source else source_video(proj)
    info = ffprobe(src)
    print(f"source : {src.name}  {info['width']}x{info['height']} "
          f"{info['fps']:.2f}fps  {info['duration'] / 60:.1f}min")
    if not info["has_audio"]:
        die("source has no audio track — nothing to transcribe")

    wav = proj / "audio.wav"
    run(["ffmpeg", "-y", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000",
         "-c:a", "pcm_s16le", str(wav)])

    try:
        import whisper
    except ImportError:
        die("openai-whisper not installed — pip3 install openai-whisper")

    print(f"whisper: loading {args.model} (CPU; roughly real-time/4 on M-series)")
    t0 = time.time()
    model = whisper.load_model(args.model)
    result = model.transcribe(str(wav), word_timestamps=True, language="en",
                              condition_on_previous_text=False, verbose=False)

    segments = []
    for seg in result.get("segments", []):
        words = [
            {"word": w["word"].strip(), "start": round(w["start"], 3), "end": round(w["end"], 3)}
            for w in seg.get("words", []) if w.get("word", "").strip()
        ]
        if not words:
            continue
        segments.append({
            "start": round(seg["start"], 3),
            "end": round(seg["end"], 3),
            "text": seg["text"].strip(),
            "words": words,
        })

    save(out, {"source": src.name, "model": args.model,
               "duration": info["duration"], "segments": segments})
    n_words = sum(len(s["words"]) for s in segments)
    print(f"done   : {len(segments)} segments, {n_words} words in {time.time() - t0:.0f}s")
    print(out)


if __name__ == "__main__":
    main()
