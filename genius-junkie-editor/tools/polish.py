"""Final audio + assembly pass → final.mp4

    python3 tools/polish.py <project> [--input captioned.mp4]
                            [--music assets/bed.mp3] [--intro assets/intro.mp4]
                            [--outro assets/outro.mp4] [--denoise]

Two-pass loudnorm to a real -14 LUFS (single-pass loudnorm guesses and lands
2-3 LU off), optional RNNoise denoise for room hum, optional music bed ducked
well under the voice, optional intro/outro bumpers.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (brand, encode_args, ffprobe, project, run, stage_input, timecode)


def measure(src, cfg):
    """Pass 1: measure so pass 2 can hit the target exactly."""
    proc = run(["ffmpeg", "-i", str(src), "-af",
                f"loudnorm=I={cfg['loudnorm_i']}:TP={cfg['loudnorm_tp']}:"
                f"LRA={cfg['loudnorm_lra']}:print_format=json",
                "-f", "null", "-"], check=False)
    blob = re.findall(r"\{[^{}]*\"input_i\"[\s\S]*?\}", proc.stderr)
    if not blob:
        return None
    return json.loads(blob[-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--input")
    ap.add_argument("--out", default="final.mp4")
    ap.add_argument("--music")
    ap.add_argument("--intro")
    ap.add_argument("--outro")
    ap.add_argument("--denoise", action="store_true")
    args = ap.parse_args()

    proj = project(args.project)
    b = brand()
    cfg = b["audio"]
    src = Path(args.input) if args.input else stage_input(proj, "captioned.mp4")
    info = ffprobe(src)
    if not info["has_audio"]:
        raise SystemExit("no audio track to polish")

    chain = []
    if args.denoise:
        model = Path("/opt/homebrew/share/rnnoise/cb.rnnn")
        if model.exists():
            chain.append(f"arnndn=m={model}")
        else:
            # highpass + gentle gate is the no-dependency fallback for room hum
            chain.append("highpass=f=90,afftdn=nf=-24")
            print("note   : rnnoise model not found, using highpass+afftdn")

    stats = measure(src, cfg)
    if stats:
        chain.append(
            f"loudnorm=I={cfg['loudnorm_i']}:TP={cfg['loudnorm_tp']}:LRA={cfg['loudnorm_lra']}"
            f":measured_I={stats['input_i']}:measured_TP={stats['input_tp']}"
            f":measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}"
            f":offset={stats['target_offset']}:linear=true:print_format=summary"
        )
        print(f"loudness: {stats['input_i']} LUFS → {cfg['loudnorm_i']} LUFS")
    else:
        chain.append(f"loudnorm=I={cfg['loudnorm_i']}:TP={cfg['loudnorm_tp']}")

    body = proj / ".polished.mp4"
    inputs = ["-i", str(src)]
    if args.music:
        music = Path(args.music)
        if not music.is_absolute():
            music = (proj / args.music) if (proj / args.music).exists() else Path(args.music)
        inputs += ["-stream_loop", "-1", "-i", str(music)]
        fg = (f"[0:a]{','.join(chain)}[voice];"
              f"[1:a]volume={cfg['music_bed_db']}dB[bed];"
              f"[bed][voice]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck];"
              f"[voice][duck]amix=inputs=2:duration=first:dropout_transition=0[aout]")
        cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", fg,
               "-map", "0:v", "-map", "[aout]", "-c:v", "copy",
               "-c:a", "aac", "-b:a", "192k", "-shortest", str(body)]
    else:
        cmd = ["ffmpeg", "-y"] + inputs + ["-af", ",".join(chain),
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(body)]
    run(cmd)

    bumpers = ([Path(args.intro)] if args.intro else []) + [body] + \
              ([Path(args.outro)] if args.outro else [])
    out = proj / args.out
    if len(bumpers) == 1:
        body.replace(out)
    else:
        v = b["video"]
        parts, labels = [], []
        for i, _ in enumerate(bumpers):
            parts.append(f"[{i}:v]scale={v['width']}:{v['height']}:force_original_aspect_ratio=decrease,"
                         f"pad={v['width']}:{v['height']}:-1:-1,setsar=1,fps={v['fps']}[v{i}]")
            parts.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo[a{i}]")
            labels.append(f"[v{i}][a{i}]")
        parts.append(f"{''.join(labels)}concat=n={len(bumpers)}:v=1:a=1[vout][aout]")
        cmd = ["ffmpeg", "-y"]
        for p in bumpers:
            cmd += ["-i", str(p)]
        cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", "[aout]"]
        cmd += encode_args(b) + [str(out)]
        run(cmd)
        body.unlink(missing_ok=True)

    got = ffprobe(out)
    print(f"final  : {timecode(got['duration'])} {got['width']}x{got['height']}")
    print(out)


if __name__ == "__main__":
    main()
