"""Fake screencast — animate static UI screenshots into a screen recording.

    python3 tools/screencast.py <project> [--shots shots.json] [--out screencast.mp4]

Nobody records a screen. Each shot is one screenshot of the real UI; the engine
adds a cursor gliding along eased paths, click ripples, and camera pushes, then
cuts shot to shot exactly like a screen recording would. If a shot names an
audio file (a VO chunk), the shot stretches to fit it.

shots.json:
{
  "shots": [
    {
      "image": "shots/01-home.png",
      "duration": 5.0,                       // ignored if audio is longer
      "audio": "vo/01-cold-open.mp3",        // optional
      "cursor": [[0.50, 0.85, 0.0],          // [x, y, t] waypoints, normalised
                 [0.72, 0.18, 1.8],
                 [0.72, 0.18, 2.6]],
      "clicks": [2.0],                       // ripple at the cursor's position then
      "zoom": [
        {"t": 0.0, "cx": 0.5,  "cy": 0.5, "z": 1.0},
        {"t": 2.0, "cx": 0.72, "cy": 0.2, "z": 1.6}
      ]
    }
  ]
}
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (brand, die, encode_args, ffprobe, load, piecewise, project,
                    run, zoom_chain)

ASSETS = Path(__file__).resolve().parent.parent / "assets"
CURSOR_HOT = (10, 6)  # arrow tip inside the sprite


def make_sprites():
    """Cursor arrow + click ripple, drawn once, cached in assets/."""
    from PIL import Image, ImageDraw
    ASSETS.mkdir(exist_ok=True)
    cur = ASSETS / "cursor.png"
    if not cur.exists():
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        # macOS-style arrow: white fill, dark outline
        pts = [(10, 6), (10, 46), (20, 37), (27, 52), (34, 49), (27, 34), (40, 34)]
        d.polygon(pts, fill=(255, 255, 255, 255), outline=(15, 23, 42, 255), width=3)
        img.save(cur)
    rip = ASSETS / "ripple.png"
    if not rip.exists():
        img = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.ellipse([8, 8, 112, 112], outline=(233, 30, 140, 230), width=9)
        d.ellipse([30, 30, 90, 90], outline=(233, 30, 140, 140), width=5)
        img.save(rip)
    return cur, rip


def smoothstep(a, b, p):
    p = max(0.0, min(1.0, p))
    return a + (b - a) * p * p * (3 - 2 * p)


def cursor_at(waypoints, t):
    """Python-side evaluation of the same easing the filter uses."""
    if not waypoints:
        return 0.5, 0.5
    if t <= waypoints[0][2]:
        return waypoints[0][0], waypoints[0][1]
    for i in range(len(waypoints) - 1):
        x0, y0, t0 = waypoints[i]
        x1, y1, t1 = waypoints[i + 1]
        if t0 <= t <= t1:
            p = (t - t0) / max(t1 - t0, 1e-6)
            return smoothstep(x0, x1, p), smoothstep(y0, y1, p)
    return waypoints[-1][0], waypoints[-1][1]


def render_shot(proj, shot, idx, b, cur_png, rip_png, out):
    W, H = b["video"]["width"], b["video"]["height"]
    fps = b["video"]["fps"]

    img = proj / shot["image"]
    if not img.exists():
        die(f"shot {idx}: missing image {img}")

    audio = proj / shot["audio"] if shot.get("audio") else None
    dur = float(shot.get("duration", 4.0))
    a0 = float(shot.get("audio_start", 0.0))
    a1 = shot.get("audio_end")  # None = to the end of the file
    if audio and audio.exists():
        alen = ffprobe_audio(audio)
        a1 = min(float(a1), alen) if a1 is not None else alen
        dur = max(dur, (a1 - a0) + 0.35)
    elif shot.get("audio"):
        die(f"shot {idx}: audio not found: {audio}")

    inputs = ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(img),
              "-i", str(cur_png), "-i", str(rip_png)]
    if audio:
        inputs += ["-i", str(audio)]

    fc = [f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease,"
          f"pad={W}:{H}:-1:-1:color=0x0f172a,setsar=1,fps={fps}[base]"]
    last = "base"

    # cursor gliding between waypoints
    wp = shot.get("cursor") or []
    if wp:
        keys = [(t, (x * W - CURSOR_HOT[0], y * H - CURSOR_HOT[1])) for x, y, t in wp]
        ex, ey = piecewise(keys, 0, 0), piecewise(keys, 1, 0)
        fc.append(f"[{last}][1:v]overlay=x='{ex}':y='{ey}':eval=frame[cur]")
        last = "cur"

    # click ripples at the cursor's position at that moment
    for ci, tc in enumerate(shot.get("clicks") or []):
        cx, cy = cursor_at(wp, tc)
        px, py = cx * W - 60, cy * H - 60
        fc.append(f"[{last}][2:v]overlay=x={px:.0f}:y={py:.0f}"
                  f":enable='between(t,{tc:.3f},{tc + 0.35:.3f})'[r{ci}]")
        last = f"r{ci}"

    # camera push — crop keyframes from the zoom list, same math as gj-zoom
    zooms = shot.get("zoom") or []
    if zooms:
        keys = []
        for z in zooms:
            zz = max(1.0, float(z["z"]))
            w, h = W / zz, H / zz
            x = min(max(z["cx"] * W - w / 2, 0), W - w)
            y = min(max(z["cy"] * H - h / 2, 0), H - h)
            keys.append((float(z["t"]), (x, y, w, h)))
        fc.append(f"[{last}]{zoom_chain(keys, W, H, W, H)}[z]")
        last = "z"

    fc.append(f"[{last}]format=yuv420p[vout]")
    if audio:
        fc.append(f"[3:a]atrim={a0:.3f}:{a1:.3f},asetpts=PTS-STARTPTS,"
                  f"aresample=48000,apad,atrim=0:{dur:.3f}[aout]")
    else:
        fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{dur:.3f}[aout]")

    cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", ";".join(fc),
           "-map", "[vout]", "-map", "[aout]"] + encode_args(b) + [str(out)]
    run(cmd)
    return dur


def ffprobe_audio(path):
    return ffprobe_duration(path)


def ffprobe_duration(path):
    proc = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "csv=p=0", str(path)])
    return float(proc.stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--shots", default="shots.json")
    ap.add_argument("--out", default="screencast.mp4")
    args = ap.parse_args()

    proj = project(args.project)
    b = brand()
    spec = load(proj / args.shots)
    shots = spec["shots"]
    if not shots:
        die("no shots in shots.json")

    cur_png, rip_png = make_sprites()
    tmp = proj / ".shots"
    tmp.mkdir(exist_ok=True)

    total, parts = 0.0, []
    for i, shot in enumerate(shots):
        part = tmp / f"shot-{i:03d}.mp4"
        dur = render_shot(proj, shot, i, b, cur_png, rip_png, part)
        total += dur
        parts.append(part)
        print(f"  shot {i + 1}/{len(shots)}  {Path(shot['image']).name}  {dur:.1f}s")

    out = proj / args.out
    listing = tmp / "list.txt"
    listing.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
         "-c", "copy", str(out)])
    print(f"screencast: {len(shots)} shots, {total:.1f}s → {out}")


if __name__ == "__main__":
    main()
