#!/usr/bin/env python3
"""Canva Infographic Size Card — the FREE one-pager.

Built NEW, never carved out of the presentation-kit.

Verified 2026-10-06:
  * Canva Help Centre, "Resize designs and size limits" — minimum 40 x 40 px,
    maximum 8000 x 3125 px (PER AXIS), and PNG download "from 0.5 up to 3.125
    times its size"
  * canva.com/create/infographics — their own three recommended sizes:
    blog 663 x 2000, Facebook 1200 x 628, LinkedIn 1104 x 736

NOT on this card: how any platform crops a feed image, what any algorithm
rewards, engagement figures, or the price of any Canva plan.

Output: canva-infographic-size-card.pdf  (one page, US Letter)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))
INK, BODY, GREY = (0.133, 0.125, 0.122), (0.28, 0.30, 0.31), (0.557, 0.541, 0.525)
RULE, PINK, GREEN = (0.894, 0.878, 0.855), (0.914, 0.118, 0.549), (0.133, 0.773, 0.369)
BLUE, AMBER, RED = (0.145, 0.388, 0.922), (0.961, 0.620, 0.043), (0.863, 0.149, 0.149)
TEAL = (0.055, 0.482, 0.463)
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


def para(c, y, t, size=10.5, font="Helvetica", col=BODY, lead=12.0, w=None):
    c.setFillColorRGB(*col); c.setFont(font, size)
    for ln in wrap(t, font, size, w or (W - 2 * M)):
        c.drawString(M, y, ln); y -= lead
    return y


def section(c, y, t):
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11); c.drawString(M, y, t)
    return y - 17


def shape(c, x, y, w, h, label, dims, col, scale):
    """One of Canva's recommended sizes, drawn to a shared scale."""
    sw, sh = w * scale, h * scale
    c.setFillColorRGB(0.957, 0.949, 0.933); c.rect(x, y, sw, sh, stroke=0, fill=1)
    c.setStrokeColorRGB(*col); c.setLineWidth(1.4); c.rect(x, y, sw, sh, stroke=1, fill=0)
    c.setFillColorRGB(*col); c.setFont("Helvetica-Bold", 8.4)
    c.drawCentredString(x + sw / 2, y - 11, label)
    c.setFillColorRGB(*GREY); c.setFont("Courier", 8)
    c.drawCentredString(x + sw / 2, y - 20, dims)
    return sw


def build():
    path = os.path.join(OUT, "canva-infographic-size-card.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("Canva Infographic Size Card - Genius Junkie")
    y = H - M
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 25)
    c.drawString(M, y - 20, "Canva Infographic Size Card")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "The ceiling, the export arithmetic, and the three shapes. Verified 6 October 2026.")
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 42; rule(c, y); y -= 15

    # ── THE CEILING ──────────────────────────────────────────────────────────
    y = section(c, y, "THE CEILING")
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 14)
    c.drawString(M, y, "Canva's maximum design size is 8000 x 3125 px - PER AXIS.")
    y -= 16
    y = para(c, y, "Minimum 40 x 40. Canva Help Centre: if the custom size fields turn red \"it means "
                   "the values are less than or exceed the size limits\". So your width can be 8,000. "
                   "Your HEIGHT stops at 3,125, and an infographic is the one format that is "
                   "inherently tall - it is the only design type where this bites.")
    y -= 3
    c.setFillColorRGB(*RED); c.setFont("Helvetica-Bold", 10.6)
    c.drawString(M, y, "There is no warning text, no suggestion, no offer to scale it. The field simply refuses the number.")
    y -= 15; rule(c, y); y -= 15

    # ── THE ARITHMETIC ───────────────────────────────────────────────────────
    y = section(c, y, "THE FIX - DESIGN SMALL, EXPORT BIG")
    y = para(c, y, "A Canva design downloads as a PNG at between 0.5x and 3.125x its size. That "
                   "multiplier is the escape hatch: the ceiling is on the CANVAS, never on the export. "
                   "So work backwards from the pixels you actually want.")
    y -= 4
    c.setFillColorRGB(*INK); c.setFont("Courier-Bold", 13)
    c.drawString(M + 10, y, "design size   x   multiplier   =   output"); y -= 17
    c.setFont("Courier-Bold", 12)
    for a, b, d in [("450 x 3000", "2x", "900 x 6000"),
                    ("600 x 2400", "2.5x", "1500 x 6000"),
                    ("640 x 3125", "3.125x", "2000 x 9765")]:
        c.setFillColorRGB(*BODY); c.drawString(M + 10, y, a)
        c.setFillColorRGB(*AMBER); c.drawString(M + 118, y, b)
        c.setFillColorRGB(*BLUE); c.drawString(M + 180, y, d)
        y -= 14
    y -= 4
    c.setFillColorRGB(*RED); c.setFont("Helvetica-Bold", 10.6)
    c.drawString(M, y, "THE CONSEQUENCE NOBODY CHECKS: every photo you place needs at least the multiplier")
    y -= 13
    c.drawString(M, y, "times the resolution it looks like it needs. Sharp at 450 wide is SOFT at 900.")
    y -= 15; rule(c, y); y -= 15

    # ── THE THREE SHAPES ─────────────────────────────────────────────────────
    y = section(c, y, "THE THREE SHAPES - FROM CANVA'S OWN INFOGRAPHIC PAGE")
    y = para(c, y, "Canva recommends a tall column for a blog and two landscapes for social. They are "
                   "not variations of each other - there is no single artwork that is both. The tall "
                   "one is your MASTER; the landscape ones are EXTRACTS: one section, one number, one "
                   "claim, re-laid out to fill a wide frame.", 10)
    y -= 6
    scale = 0.030
    base = y - 2000 * scale          # all three sit on ONE baseline
    x = M + 24
    gap = 30
    for label, w, h, col in [("BLOG", 663, 2000, TEAL), ("FACEBOOK", 1200, 628, AMBER),
                             ("LINKEDIN", 1104, 736, BLUE)]:
        sw = shape(c, x, base, w, h, label, f"{w} x {h}", col, scale)
        x += sw + gap
    # the note sits to the right of the shapes, inside their own height
    nx = x + 10
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10.6)
    c.drawString(nx, y - 10, "Resize changes the canvas.")
    c.drawString(nx, y - 24, "It does not re-think the layout.")
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10)
    c.drawString(nx, y - 40, "A tall column squashed into a landscape box is")
    c.drawString(nx, y - 52, "unreadable every time. Three extracts from a")
    c.drawString(nx, y - 64, "ten-section infographic is plenty - and only the")
    c.drawString(nx, y - 76, "sections that work ALONE.")
    y = base - 28
    rule(c, y); y -= 15

    # ── THE THUMBNAIL TEST ───────────────────────────────────────────────────
    y = section(c, y, "THE TEN-SECOND TEST ALMOST NOBODY DOES")
    y = para(c, y, "Zoom out until the whole thing fits on screen at about the size of a postage stamp - "
                   "roughly what a feed, a preview thumbnail or a search result shows.")
    y -= 2
    c.setFillColorRGB(*GREEN); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M + 13, y, "SHOULD SURVIVE: the shape of it, the colour blocks, and the biggest numbers.")
    y -= 13
    c.setFillColorRGB(*RED); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M + 13, y, "ALL GREY TEXTURE: the type is too uniform. Make THE NUMBERS bigger - not the headings.")
    y -= 13
    c.setFillColorRGB(*AMBER); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M + 13, y, "Then check the top two inches on their own - often the only part that gets seen at all.")
    y -= 15; rule(c, y); y -= 14

    # ── THE SEVEN CHECKS ─────────────────────────────────────────────────────
    y = section(c, y, "SEVEN CHECKS BEFORE YOU EXPORT")
    checks = [("The design fits inside 8,000 x 3,125", False),
              ("You know the multiplier that gets you the pixels you want", False),
              ("Every photo is at least that multiplier x the resolution it looks like it needs", True),
              ("It still reads at thumbnail size, and the numbers are what survive", False),
              ("The title and your best number are both in the top two inches", False),
              ("The sources are ON the image, with a date", False),
              ("The landscape extracts are re-laid out, not squashed", False)]
    for t, hard in checks:
        c.setFillColorRGB(*(RED if hard else GREEN)); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "*")
        c.setFillColorRGB(*BODY); c.setFont("Helvetica-Bold" if hard else "Helvetica", 10.5)
        c.drawString(M + 13, y, t); y -= 11.8
    y -= 2
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Oblique", 9.4)
    c.drawString(M + 13, y, "The third is the one nobody checks until the export comes back soft - and by then the design is finished.")
    y -= 15
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10.4)
    c.drawString(M, y, "And put the source on the image itself, with a date. A caption does not travel with a screenshot.")

    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 8.4)
    c.drawString(M, M - 14, "Sources: Canva Help Centre (Resize designs and size limits); canva.com/create/infographics.")
    c.drawRightString(W - M, M - 14, "Genius Junkie - geniusjunkie.net")
    c.showPage(); c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
