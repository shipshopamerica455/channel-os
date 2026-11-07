"""Three thumbnail variants, straight off the recording.

    python3 tools/make_thumbs.py <project> --text "SIZE LABELS RIGHT" \\
        --sub "Canva · 2 min" [--at 61 --at 128 --at 190]

Tutorial thumbnails work differently from face-driven ones: the viewer is
choosing on "is that the screen I am stuck on?", so the frame itself is the hook.
This grabs high-activity frames (where the real UI is on screen, not a blank
canvas), pushes in on the action, and lays the brand bar over it. Three variants
so YouTube can A/B them.
"""
import argparse
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import brand, die, ffprobe, load, project, run, stage_input

FONT_DIRS = [
    "/System/Library/Fonts/Supplemental/",
    "/Library/Fonts/",
    "/usr/share/fonts/truetype/dejavu/",
]
FONT_FILES = ["Arial Black.ttf", "Impact.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"]


def font(size):
    from PIL import ImageFont
    for d in FONT_DIRS:
        for f in FONT_FILES:
            p = Path(d) / f
            if p.exists():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def busy_moments(proj, duration, n):
    """Pick timestamps where the screen is actually doing something."""
    act = load(proj / "activity.json", default=None)
    if not act or not act.get("points"):
        return [duration * f for f in (0.25, 0.5, 0.75)][:n]
    pts = [p for p in act["points"] if p["t"] > min(8.0, duration * 0.05)]
    pts.sort(key=lambda p: p["energy"], reverse=True)
    picked = []
    for p in pts:
        if all(abs(p["t"] - q) > duration / (n + 2) for q in picked):
            picked.append(p["t"])
        if len(picked) == n:
            break
    return picked or [duration / 2]


def compose(frame, out, text, sub, b, badge):
    from PIL import Image, ImageDraw, ImageFilter

    img = Image.open(frame).convert("RGB").resize((1280, 720), Image.LANCZOS)
    draw = ImageDraw.Draw(img, "RGBA")

    # darken the lower third so type always reads, whatever the UI is doing
    band = Image.new("RGBA", (1280, 300), (0, 0, 0, 0))
    ImageDraw.Draw(band).rectangle([0, 0, 1280, 300], fill=(15, 23, 42, 205))
    img.paste(Image.alpha_composite(
        img.crop((0, 420, 1280, 720)).convert("RGBA").filter(ImageFilter.GaussianBlur(6)),
        band).convert("RGB"), (0, 420))

    accent = b["colors"]["accent"]
    highlight = b["colors"]["highlight"]

    lines = textwrap.wrap(text.upper(), width=18)[:2]
    size = 104 if len(lines) == 1 else 84
    f = font(size)
    y = 448 if len(lines) == 2 else 478
    for line in lines:
        w = draw.textbbox((0, 0), line, font=f)[2]
        x = (1280 - w) // 2
        for dx, dy in ((-4, 0), (4, 0), (0, -4), (0, 4), (-3, -3), (3, 3)):
            draw.text((x + dx, y + dy), line, font=f, fill=b["colors"]["ink"])
        draw.text((x, y), line, font=f, fill=highlight)
        y += size + 8

    if sub:
        fs = font(38)
        bb = draw.textbbox((0, 0), sub, font=fs)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        x = (1280 - w) // 2
        top = 636
        draw.rounded_rectangle([x - 26, top, x + w + 26, top + h + 26], radius=12, fill=accent)
        draw.text((x, top + 13 - bb[1]), sub, font=fs, fill="#ffffff")

    if badge:
        fb = font(34)
        w = draw.textbbox((0, 0), badge, font=fb)[2]
        draw.rounded_rectangle([40, 40, 40 + w + 44, 104], radius=12, fill=accent)
        draw.text((62, 52), badge, font=fb, fill="#ffffff")

    img.save(out, quality=92)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--text", required=True, help="the big line, 2-4 words")
    ap.add_argument("--sub", default="", help="small pill, e.g. 'Canva · beginner'")
    ap.add_argument("--badge", default="", help="corner badge, e.g. 'FREE'")
    ap.add_argument("--at", type=float, action="append", help="force a frame time (repeatable)")
    ap.add_argument("--input")
    args = ap.parse_args()

    proj = project(args.project)
    b = brand()
    src = Path(args.input) if args.input else stage_input(proj, "final.mp4")
    info = ffprobe(src)

    try:
        import PIL  # noqa: F401
    except ImportError:
        die("Pillow not installed — pip3 install pillow")

    times = args.at or busy_moments(proj, info["duration"], b["packaging"]["thumbnail_variants"])
    outs = []
    for i, t in enumerate(times):
        letter = "ABC"[i] if i < 3 else str(i)
        frame = proj / f".frame-{letter}.png"
        run(["ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1",
             "-q:v", "2", str(frame)])
        out = proj / f"thumbnail-{letter}.png"
        compose(frame, out, args.text, args.sub, b, args.badge)
        frame.unlink(missing_ok=True)
        outs.append((letter, t, out))

    for letter, t, out in outs:
        print(f"  {letter}  frame @{t:.0f}s  →  {out.name}")
    if outs:
        # A is the default the uploader picks up
        print(f"\ndefault upload thumbnail: {outs[0][2].name} "
              f"(rename another to thumbnail-A.png to swap)")


if __name__ == "__main__":
    main()
