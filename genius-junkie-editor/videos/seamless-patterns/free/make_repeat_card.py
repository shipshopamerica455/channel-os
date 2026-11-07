#!/usr/bin/env python3
"""Canva Seamless Repeat Card — the FREE one-pager.

Built NEW, never carved out of the seamless-pattern-kit.

Verified 2026-10-05:
  * Canva Help Centre, "Move elements in your design" — X and Y are pixels
    from the TOP-LEFT corner, set under Position > Advanced
  * Spoonflower support — 150 DPI, under 40 MB, sRGB, and background to the
    edge of the file

NOT on this card: what any marketplace pays, listing costs or royalty rates.

Output: canva-seamless-repeat-card.pdf  (one page, US Letter)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))
INK, BODY, GREY = (0.133, 0.125, 0.122), (0.28, 0.30, 0.31), (0.557, 0.541, 0.525)
RULE, PINK, GREEN = (0.894, 0.878, 0.855), (0.914, 0.118, 0.549), (0.133, 0.773, 0.369)
BLUE, AMBER = (0.145, 0.388, 0.922), (0.961, 0.620, 0.043)
W, H = letter
M = 0.5 * inch


def wrap(t, f, s, w):
    words, lines, cur = t.split(), [], ""
    for x in words:
        c = (cur + " " + x).strip()
        if stringWidth(c, f, s) <= w: cur = c
        else: lines.append(cur); cur = x
    if cur: lines.append(cur)
    return lines


def rule(c, y):
    c.setStrokeColorRGB(*RULE); c.setLineWidth(0.8); c.line(M, y, W - M, y)


def para(c, y, t, size=10.5, font="Helvetica", col=BODY, lead=12.0):
    c.setFillColorRGB(*col); c.setFont(font, size)
    for ln in wrap(t, font, size, W - 2 * M):
        c.drawString(M, y, ln); y -= lead
    return y


def section(c, y, t):
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11); c.drawString(M, y, t)
    return y - 17


def tile(c, x, y, s, twins):
    """A tile with an edge motif and, when `twins`, its exact-offset partner."""
    c.setFillColorRGB(0.949, 0.902, 0.847); c.rect(x, y, s, s, stroke=0, fill=1)
    c.setStrokeColorRGB(*GREY); c.setLineWidth(0.9); c.rect(x, y, s, s, stroke=1, fill=0)
    r = s * 0.1
    c.setFillColorRGB(0.76, 0.33, 0.25)
    c.circle(x + s, y + s * 0.6, r, stroke=0, fill=1)
    if twins:
        c.setFillColorRGB(0.76, 0.33, 0.25); c.circle(x, y + s * 0.6, r, stroke=0, fill=1)
    c.setFillColorRGB(0.243, 0.42, 0.353)
    c.circle(x + s * 0.4, y, r * 0.85, stroke=0, fill=1)
    if twins:
        c.circle(x + s * 0.4, y + s, r * 0.85, stroke=0, fill=1)
    c.setFillColorRGB(*(GREEN if twins else PINK))
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(x + s / 2, y - 13, "twins placed" if twins else "no twins - seam")


def build():
    path = os.path.join(OUT, "canva-seamless-repeat-card.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("Canva Seamless Repeat Card - Genius Junkie")
    y = H - M
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 25)
    c.drawString(M, y - 20, "Canva Seamless Repeat Card")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "The offset arithmetic, the spec, and the seam test. Verified 5 October 2026.")
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 42; rule(c, y); y -= 15

    y = section(c, y, "THE ONE RULE")
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 14)
    c.drawString(M, y, "The canvas edge is a CROP, not a wrap.")
    y -= 16
    y = para(c, y, "Anything pushed past the edge is cut there and nothing continues on the other "
                   "side. So every element touching an edge needs a twin, placed by TYPED "
                   "coordinates. Canva Help Centre: X and Y are the distance in pixels from the "
                   "TOP-LEFT corner, set under Position > Advanced.")
    y -= 4
    c.setFillColorRGB(*INK); c.setFont("Courier-Bold", 12)
    for ln in ["crosses the RIGHT edge   ->   twin at  X - canvas width",
               "crosses the BOTTOM edge  ->   twin at  Y - canvas height"]:
        c.drawString(M + 10, y, ln); y -= 15
    y -= 2
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "(Mirror it for the left and top edges: X + width, Y + height.) The OTHER coordinate stays IDENTICAL.")
    y -= 16
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "A motif in a CORNER needs FOUR copies: the original, X-width, Y-height, and BOTH.")
    y -= 14
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    c.drawString(M, y, "Miss the fourth and you get a seam at every corner point - the most noticeable kind there is.")
    y -= 16
    tile(c, M + 20, y - 86, 78, False)
    tile(c, M + 170, y - 86, 78, True)
    y -= 100
    rule(c, y); y -= 15

    y = section(c, y, "THE SEAM TEST - THE ONLY HONEST CHECK")
    y = para(c, y, "You cannot judge a seam inside Canva: no tile preview, no offset preview, no "
                   "wrap mode. Export the tile as a PNG, make a second design at exactly TWICE the "
                   "tile size, and drop the PNG in four times - typed, not dragged:")
    c.setFillColorRGB(*INK); c.setFont("Courier-Bold", 12)
    c.drawString(M + 10, y, "X=0  Y=0     X=tile  Y=0     X=0  Y=tile     X=tile  Y=tile"); y -= 18
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    c.drawString(M, y, "Look at the two joins. Fix it in the ORIGINAL, export again, re-test - never patch the proof."); y -= 16
    y = para(c, y, "A hairline of white means the background does not overhang. A sliced motif means no "
                   "twin, or its other coordinate was changed. A light-to-dark band means a gradient "
                   "background - its dark end meets the next tile's light end.", 10)
    y -= 2; rule(c, y); y -= 15

    y = section(c, y, "THE SPEC - SPOONFLOWER, AS AN EXAMPLE")
    y = para(c, y, '"Your files should be a JPG or PNG, saved at your preferred print dimensions and '
                   '150 DPI, and under 40 MB." They convert everything to 150 DPI on upload, so the '
                   'PHYSICAL repeat size is your decision and the resolution is not. They print in '
                   'sRGB, not CMYK - and Canva works in RGB anyway.', 10, "Helvetica")
    y -= 2
    c.setFillColorRGB(*AMBER); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M, y, '"Be sure any background colors in your file extend to the edge of the file, otherwise the')
    y -= 13
    c.drawString(M, y, 'design will look broken up into separate squares as opposed to a seamless repeating layout."')
    y -= 18
    c.setFillColorRGB(*INK); c.setFont("Courier-Bold", 13)
    c.drawString(M, y, "inches x 150 = pixels"); y -= 18
    for a, b in [("2 in repeat", "300 x 300 px"), ("8 in repeat", "1200 x 1200 px"), ("12 in repeat", "1800 x 1800 px")]:
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5); c.drawString(M + 13, y, a)
        c.setFillColorRGB(*BLUE); c.setFont("Courier-Bold", 11.5); c.drawString(M + 170, y, b); y -= 14
    y -= 4
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M, y, "Other marketplaces differ - check your own spec page.")
    y -= 13; rule(c, y); y -= 14

    y = section(c, y, "SEVEN CHECKS BEFORE YOU LIST IT")
    checks = [("The background covers the whole canvas and overhangs every side", False),
              ("Every edge-crossing motif has an exact twin - typed, not dragged", False),
              ("Every corner motif has all four copies", False),
              ("You have tiled it two by two and looked at BOTH joins", True),
              ("The pixels match the physical repeat at your marketplace's DPI", False),
              ("It is under their file size ceiling", False),
              ("Every motif came from a Canva search filtered to Free", False)]
    for t, proves in checks:
        c.setFillColorRGB(*(PINK if proves else GREEN)); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "*")
        c.setFillColorRGB(*BODY); c.setFont("Helvetica-Bold" if proves else "Helvetica", 10.5)
        c.drawString(M + 13, y, t); y -= 11.8
    y -= 2
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Oblique", 9.4)
    c.drawString(M + 13, y, "The fourth is the only one that actually proves the first three. Arithmetic is a claim; tiling is the evidence.")

    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 8.4)
    c.drawString(M, M - 14, "Sources: Canva Help Centre (Move elements in your design); Spoonflower support.")
    c.drawRightString(W - M, M - 14, "Genius Junkie - geniusjunkie.net")
    c.showPage(); c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
