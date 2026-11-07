"""Shared helpers for the Genius Junkie editing pipeline."""
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def brand():
    return json.loads((ROOT / "brand.json").read_text())


def project(slug):
    """Resolve a project dir — accepts a slug or a path."""
    p = Path(slug)
    if p.is_dir():
        return p.resolve()
    p = ROOT / "videos" / slug
    p.mkdir(parents=True, exist_ok=True)
    return p


def load(path, default=None):
    path = Path(path)
    if not path.exists():
        if default is not None:
            return default
        die(f"missing required file: {path}")
    return json.loads(path.read_text())


def save(path, data):
    Path(path).write_text(json.dumps(data, indent=2))
    return path


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def run(cmd, quiet=True, check=True):
    """Run a command list. ffmpeg is noisy, so swallow stderr unless it fails."""
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="replace",
    )
    if check and proc.returncode != 0:
        tail = "\n".join(proc.stderr.strip().splitlines()[-25:])
        die(f"command failed ({proc.returncode}): {shlex.join(cmd)}\n{tail}")
    if not quiet:
        print(proc.stderr)
    return proc


def ffprobe(path):
    proc = run([
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", str(path),
    ])
    info = json.loads(proc.stdout)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    if not v:
        die(f"no video stream in {path}")
    num, den = (v.get("r_frame_rate") or "30/1").split("/")
    return {
        "duration": float(info["format"]["duration"]),
        "width": int(v["width"]),
        "height": int(v["height"]),
        "fps": float(num) / float(den or 1),
        "has_audio": a is not None,
        "audio_channels": int(a["channels"]) if a else 0,
    }


def encode_args(b):
    v = b["video"]
    return [
        "-c:v", "libx264", "-preset", v["preset"], "-crf", str(v["crf"]),
        "-pix_fmt", v["pix_fmt"], "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
    ]


def timecode(seconds):
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def source_video(proj):
    """Find the raw recording in a project dir."""
    explicit = proj / "source.mp4"
    if explicit.exists():
        return explicit
    raw = proj / "raw"
    pool = sorted(raw.glob("*")) if raw.is_dir() else []
    pool += sorted(proj.glob("*.mp4")) + sorted(proj.glob("*.mov")) + sorted(proj.glob("*.MOV"))
    stages = {"master.mp4", "zoomed.mp4", "captioned.mp4", "final.mp4"}
    pool = [p for p in pool if p.suffix.lower() in (".mp4", ".mov", ".mkv") and p.name not in stages]
    if not pool:
        die(f"no source recording found in {proj} (drop it in as source.mp4 or raw/)")
    return pool[0]


def stage_input(proj, prefer):
    """Pick the newest available stage output, walking back from `prefer`."""
    chain = ["final.mp4", "captioned.mp4", "zoomed.mp4", "master.mp4"]
    for name in chain[chain.index(prefer):]:
        p = proj / name
        if p.exists():
            return p
    return source_video(proj)


def piecewise(keys, index, default, tvar="t"):
    """Build an ffmpeg expression: smoothstep-interpolated keyframes.

    keys: [(t, (x, y, w, h)), ...] sorted by t. `index` selects the tuple slot.
    Emits nested if() so the whole timeline is one filter, one encode pass.
    `tvar` is the time variable — "t" in most filters, "(in/30)" in zoompan.
    """
    if not keys:
        return str(default)
    pts = [(t, vals[index]) for t, vals in keys]
    expr = f"{pts[-1][1]:.3f}"
    for i in range(len(pts) - 2, -1, -1):
        t0, v0 = pts[i]
        t1, v1 = pts[i + 1]
        span = max(t1 - t0, 1e-3)
        # smoothstep p*p*(3-2p) over the segment
        p = f"clip(({tvar}-{t0:.3f})/{span:.3f},0,1)"
        seg = f"({v0:.3f}+({v1 - v0:.3f})*({p})*({p})*(3-2*({p})))"
        expr = f"if(lt({tvar},{t1:.3f}),{seg},{expr})"
    return f"if(lt({tvar},{pts[0][0]:.3f}),{pts[0][1]:.3f},{expr})"


def zoom_chain(keys_px, W, H, OW, OH, fps=30):
    """Animated zoom/pan via zoompan (constant frame size end to end).

    keys_px: [(t, (x, y, w, h))] crop boxes in SOURCE pixels. Do NOT feed crop
    an animated scale — mid-stream frame-size changes silently reset crop's
    position expressions to 0. zoompan crops iw/zoom at (x, y) per frame and
    scales to a fixed output, which is exactly the effect and never reinits.
    Input must already be constant-fps `fps` (zoompan's clock is frame count).
    """
    tv = f"(in/{fps})"
    keys = [(t, (W / w, x, y)) for t, (x, y, w, h) in keys_px]
    z = f"max({piecewise(keys, 0, 1, tv)},1.001)"
    x = f"clip({piecewise(keys, 1, 0, tv)},0,iw-iw/zoom)"
    y = f"clip({piecewise(keys, 2, 0, tv)},0,ih-ih/zoom)"
    return (f"fps={fps},zoompan=z='{z}':x='{x}':y='{y}'"
            f":d=1:s={OW}x{OH}:fps={fps},setsar=1")


def concat_filter(keeps, has_audio):
    """trim/concat filtergraph for a list of [start, end] keep ranges."""
    parts, labels = [], []
    for i, (a, b) in enumerate(keeps):
        parts.append(f"[0:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS[v{i}]")
        if has_audio:
            parts.append(f"[0:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS[a{i}]")
        labels.append(f"[v{i}][a{i}]" if has_audio else f"[v{i}]")
    n = len(keeps)
    parts.append(f"{''.join(labels)}concat=n={n}:v=1:a={1 if has_audio else 0}[vout]"
                 + ("[aout]" if has_audio else ""))
    return ";".join(parts)


def remap_transcript(transcript, keeps):
    """Shift word/segment timestamps onto the post-cut timeline; drop cut words."""
    offsets, cum = [], 0.0
    for a, b in keeps:
        offsets.append((a, b, cum))
        cum += b - a

    def shift(t):
        for a, b, base in offsets:
            if a <= t <= b:
                return base + (t - a)
        return None

    out = {"duration": cum, "segments": []}
    for seg in transcript.get("segments", []):
        words = []
        for w in seg.get("words", []):
            s, e = shift(w["start"]), shift(w["end"])
            if s is None or e is None or e <= s:
                continue
            words.append({**w, "start": round(s, 3), "end": round(e, 3)})
        if not words:
            continue
        out["segments"].append({
            "start": words[0]["start"],
            "end": words[-1]["end"],
            "text": " ".join(w["word"].strip() for w in words),
            "words": words,
        })
    return out


def all_words(transcript):
    return [w for seg in transcript.get("segments", []) for w in seg.get("words", [])]
