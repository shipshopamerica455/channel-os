#!/usr/bin/env python3
"""Wall Art Starter Pack — the 3-piece set at all five buyer ratios, 300 DPI.

Outputs (all 300 DPI, vector shapes so they're razor-sharp at any size):
  wallart-<word>-2x3.pdf      16 x 24 in
  wallart-<word>-3x4.pdf      18 x 24 in
  wallart-<word>-4x5.pdf      16 x 20 in   (most popular)
  wallart-<word>-11x14.pdf    11 x 14 in   (fits no ratio — its own file)
  wallart-<word>-ISO-A.pdf    A2 (420 x 594 mm)
  wallart-sizes-chart.pdf     the listing image content as a printable
  wallart-READ-ME.pdf         paper, printing, licence
"""
import os
from reportlab.lib.pagesizes import A2
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

PAPER = (0.961, 0.945, 0.918)   # #f5f1ea
INK = (0.173, 0.149, 0.133)     # #2c2622
TERRA = (0.761, 0.431, 0.310)   # #c26e4f
SAND = (0.863, 0.788, 0.690)    # #dcc9b0
SAGE = (0.553, 0.608, 0.514)    # #8d9b83

# (label, w_in, h_in) — the five files buyers expect
RATIOS = [
    ("2x3", 16, 24), ("3x4", 18, 24), ("4x5", 16, 20), ("11x14", 11, 14),
    ("ISO-A", A2[0] / inch, A2[1] / inch),
]


def arch(c, x, y, w, h, col):
    """Rounded-top arch: semicircle cap on a rectangle."""
    c.setFillColorRGB(*col)
    r = w / 2.0
    c.rect(x, y, w, h - r + 0.75, stroke=0, fill=1)   # +0.75pt overlap kills the seam
    p = c.beginPath()
    p.moveTo(x, y + h - r)
    p.arcTo(x, y + h - 2 * r, x + w, y + h, 0, 180)
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def dome(c, x, y, w, h, col):
    """Rounded-BOTTOM shape (arch flipped)."""
    c.setFillColorRGB(*col)
    r = w / 2.0
    c.rect(x, y + r - 0.75, w, h - r + 0.75, stroke=0, fill=1)
    p = c.beginPath()
    p.moveTo(x, y + r)
    p.arcTo(x, y, x + w, y + 2 * r, 180, 180)
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def pill(c, x, y, w, h, col):
    c.setFillColorRGB(*col)
    c.roundRect(x, y, w, h, w / 2.0, stroke=0, fill=1)


def circle(c, cx, cy, r, col):
    c.setFillColorRGB(*col)
    c.circle(cx, cy, r, stroke=0, fill=1)


def piece(path, variant, word, w_in, h_in):
    """One printable at an arbitrary size. Geometry is proportional, so every
    ratio keeps the same composition and the 10% margin."""
    W, H = w_in * inch, h_in * inch
    c = pdfcanvas.Canvas(path, pagesize=(W, H))
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    # art zone: inside a 10% margin, above the word
    ax, ay = W * 0.10, H * 0.22
    aw, ah = W * 0.80, H * 0.62

    if variant == 0:      # arch + circle
        arch(c, ax + aw * 0.10, ay + ah * 0.10, aw * 0.375, ah * 0.80, TERRA)
        circle(c, ax + aw * 0.71, ay + ah * 0.46, aw * 0.16, SAND)
    elif variant == 1:    # pill + dome
        pill(c, ax + aw * 0.04, ay + ah * 0.08, aw * 0.30, ah * 0.84, SAND)
        dome(c, ax + aw * 0.62, ay + ah * 0.22, aw * 0.375, ah * 0.60, TERRA)
    else:                 # small arch + tall pill
        arch(c, ax + aw * 0.06, ay + ah * 0.10, aw * 0.35, ah * 0.52, SAGE)
        pill(c, ax + aw * 0.66, ay + ah * 0.08, aw * 0.275, ah * 0.84, TERRA)

    c.setFillColorRGB(*INK)
    fs = H * 0.058
    c.setFont("Helvetica", fs)
    c.drawCentredString(W / 2.0, H * 0.105, word)
    c.showPage()
    c.save()


def sizes_chart(path):
    W, H = 16 * inch, 20 * inch
    c = pdfcanvas.Canvas(path, pagesize=(W, H))
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica", H * 0.036)
    c.drawCentredString(W / 2, H * 0.88, "SIZES INCLUDED")
    c.setFillColorRGB(*TERRA)
    c.rect(W * 0.42, H * 0.855, W * 0.16, H * 0.004, stroke=0, fill=1)

    rows = [
        ("2:3", "4×6  ·  8×12  ·  16×24 in"),
        ("3:4", "6×8  ·  9×12  ·  18×24 in"),
        ("4:5", "8×10  ·  16×20 in"),
        ("11×14", "11×14 in (its own file)"),
        ("ISO A", "A5 · A4 · A3 · A2 · A1"),
    ]
    y = H * 0.74
    for lab, ex in rows:
        c.setFillColorRGB(*TERRA)
        c.setFont("Helvetica-Bold", H * 0.028)
        c.drawString(W * 0.14, y, lab)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica", H * 0.022)
        c.drawString(W * 0.34, y, ex)
        y -= H * 0.075

    c.setFillColorRGB(*INK)
    c.setFont("Helvetica", H * 0.019)
    c.drawCentredString(W / 2, H * 0.24, "All files 300 DPI · print at 100% — do not scale up")
    c.setFont("Helvetica", H * 0.016)
    c.drawCentredString(W / 2, H * 0.19, "Instant digital download · nothing is shipped")
    c.showPage()
    c.save()


def readme(path):
    W, H = 8.27 * inch, 11.69 * inch  # A4
    c = pdfcanvas.Canvas(path, pagesize=(W, H))
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    M = 0.9 * inch
    y = H - M

    c.setFillColorRGB(*TERRA)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(M, y, "Read me first")
    c.setFillColorRGB(*TERRA)
    c.rect(M, y - 14, 70, 3, stroke=0, fill=1)

    y -= 56
    c.setFillColorRGB(*INK)
    blocks = [
        ("What's included",
         ["3 designs — bloom, drift, still", "Each at 5 ratios: 2:3, 3:4, 4:5, 11×14, ISO A",
          "All 300 DPI, print-ready PDF"]),
        ("Paper",
         ["Matte or lightly textured art paper", "200 GSM or heavier gives the best result",
          "Avoid gloss — it fights the muted palette"]),
        ("Where to print",
         ["Home printer, a photo lab, or any print shop", "Ask for 'borderless' if your frame has no mat"]),
        ("⚠ Do not scale up",
         ["Print at 100%. Your printer may offer to enlarge —", "decline it, or the file will soften."]),
        ("Framing",
         ["The design has a 10% margin built in, so a mat", "board will not crop anything important."]),
        ("Licence",
         ["Personal use only. You may print as many copies", "as you like for your own home or as a gift.",
          "No resale, no commercial reproduction, no reselling", "the files themselves."]),
    ]
    for title, lines in blocks:
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 12.5)
        c.drawString(M, y, title)
        y -= 18
        c.setFont("Helvetica", 10.5)
        c.setFillColorRGB(0.35, 0.32, 0.30)
        for ln in lines:
            c.drawString(M + 12, y, ln)
            y -= 14
        y -= 12

    c.setFillColorRGB(0.55, 0.52, 0.50)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(W / 2, M - 18, "Genius Junkie · geniusjunkie.net")
    c.showPage()
    c.save()


if __name__ == "__main__":
    made = []
    for variant, word in [(0, "bloom"), (1, "drift"), (2, "still")]:
        for lab, w_in, h_in in RATIOS:
            f = f"wallart-{word}-{lab}.pdf"
            piece(os.path.join(OUT, f), variant, word, w_in, h_in)
            made.append(f)
    sizes_chart(os.path.join(OUT, "wallart-sizes-chart.pdf"))
    readme(os.path.join(OUT, "wallart-READ-ME.pdf"))
    print(f"wrote {len(made)} art files + sizes chart + read-me")
