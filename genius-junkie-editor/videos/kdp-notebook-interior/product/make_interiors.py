"""KDP notebook interior pack — print-ready PDFs at the exact spec the tutorial
teaches (6"x9" trim + bleed = 6.125" x 9.25", mirrored margins, 120 pages).

    python3 make_interiors.py            # builds all four variants

Spec (matches the video narration exactly):
  page          6.125 x 9.25 in  (bleed size — KDP: trim +0.125" W, +0.25" H)
  outside/top/bottom margin  0.75 in   (generous, well above KDP minimum)
  gutter (spine)             0.875 in  (mirrored: right page = left spine)
  lines   #CCCCCC, 0.75pt, 26 lines at 23.76pt pitch
  dots    5 mm pitch, 1.1pt radius, #C6C6C6
  grid    5 mm pitch, 0.5pt, #D4D4D4
  pages   120, no page numbers (interior stays niche-neutral)
"""
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas

W, H = 6.125 * inch, 9.25 * inch
TOP, BOTTOM, OUTSIDE, GUTTER = 0.75 * inch, 0.75 * inch, 0.75 * inch, 0.875 * inch
PAGES = 120
LINE_PITCH = 23.76  # points
N_LINES = 26


def content_box(page_index):
    """Mirrored margins: odd sheets (recto) have the gutter on the left."""
    recto = page_index % 2 == 0  # first page is a recto
    left = GUTTER if recto else OUTSIDE
    right = OUTSIDE if recto else GUTTER
    return left, BOTTOM, W - right, H - TOP


def lined(c, i):
    x0, y0, x1, y1 = content_box(i)
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.setLineWidth(0.75)
    total = (N_LINES - 1) * LINE_PITCH
    start = y0 + ((y1 - y0) - total) / 2
    for n in range(N_LINES):
        y = start + n * LINE_PITCH
        c.line(x0, y, x1, y)


def dotted(c, i):
    x0, y0, x1, y1 = content_box(i)
    c.setFillColorRGB(0.776, 0.776, 0.776)
    pitch = 5 * mm
    nx = int((x1 - x0) // pitch)
    ny = int((y1 - y0) // pitch)
    ox = x0 + ((x1 - x0) - nx * pitch) / 2
    oy = y0 + ((y1 - y0) - ny * pitch) / 2
    for r in range(ny + 1):
        for q in range(nx + 1):
            c.circle(ox + q * pitch, oy + r * pitch, 1.1, stroke=0, fill=1)


def grid(c, i):
    x0, y0, x1, y1 = content_box(i)
    c.setStrokeColorRGB(0.83, 0.83, 0.83)
    c.setLineWidth(0.5)
    pitch = 5 * mm
    x = x0
    while x <= x1 + 0.1:
        c.line(x, y0, x, y1)
        x += pitch
    y = y0
    while y <= y1 + 0.1:
        c.line(x0, y, x1, y)
        y += pitch


def blank(c, i):
    pass


def build(name, draw):
    path = f"kdp-interior-{name}-6x9-120p.pdf"
    c = canvas.Canvas(path, pagesize=(W, H))
    c.setTitle(f"KDP Notebook Interior — {name.title()} — 6x9, 120 pages")
    c.setAuthor("Genius Junkie")
    for i in range(PAGES):
        draw(c, i)
        c.showPage()
    c.save()
    print(f"  {path}")


if __name__ == "__main__":
    print(f"page {W/inch:.3f} x {H/inch:.2f} in · {PAGES}pp · mirrored gutter {GUTTER/inch:.3f}\"")
    build("lined", lined)
    build("dotted", dotted)
    build("grid", grid)
    build("blank", blank)
