#!/usr/bin/env python3
"""Canva Photo Calendar Print Card — the FREE one-pager.

Built NEW, never carved out of the 2027-calendar-kit.

Verified 2026-10-16:
  * Canva Help Centre, "Use margins, bleed, rulers, and crop marks" — "Canva
    adds 0.125 inches (3.175 mm) on all sides for products that trim or get
    cut"; "Changing margin, bleed, and crop mark sizes are also not available.
    These are fixed and are measured based on our print specifications.";
    "resize or stretch your background to cover them"
  * Canva Help Centre, "Check file upload formats and requirements" — under
    50MB, not more than 250 million total pixels; JPEG, PNG, HEIC/HEIF, WebP
  * Canva Help Centre, "Choose the right download file type" — PDF Print is
    300 dpi "with bleed, crop marks, and color profile (RGB or CMYK)"

NOT on this card: what Canva Print or any print shop charges, turnaround
times, paper weights or binding prices.

Output: canva-photo-calendar-print-card.pdf  (one page, US Letter)
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
BAND = (0.957, 0.949, 0.933)
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


def bleed_diagram(c, x, y, w, h, stretched):
    """A page with its bleed line, photo short of it or past it."""
    over = 9
    if stretched:
        c.setFillColorRGB(0.55, 0.62, 0.58)
        c.rect(x - over, y - over, w + over * 2, h + over * 2, stroke=0, fill=1)
    else:
        c.setFillColorRGB(0.55, 0.62, 0.58); c.rect(x, y, w, h, stroke=0, fill=1)
    # the trim edge (solid) and the bleed line (dashed, outside it)
    c.setStrokeColorRGB(*INK); c.setLineWidth(1.0); c.rect(x, y, w, h, stroke=1, fill=0)
    c.setStrokeColorRGB(*(GREEN if stretched else RED)); c.setLineWidth(1.0)
    c.setDash(3, 2); c.rect(x - over, y - over, w + over * 2, h + over * 2, stroke=1, fill=0); c.setDash()
    c.setFillColorRGB(*(GREEN if stretched else RED)); c.setFont("Helvetica-Bold", 8.6)
    c.drawCentredString(x + w / 2, y - over - 12, "STRETCHED PAST IT" if stretched else "SIZED TO THE PAGE")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 8)
    c.drawCentredString(x + w / 2, y - over - 22, "every cut lands on photo" if stretched else "white sliver, all 12 months")


def build():
    path = os.path.join(OUT, "canva-photo-calendar-print-card.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("Canva Photo Calendar Print Card - Genius Junkie")
    y = H - M
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 24)
    c.drawString(M, y - 20, "Canva Photo Calendar Print Card")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "The bleed, the pixels, and the seven checks. Verified 16 October 2026.")
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 42; rule(c, y); y -= 15

    # ── THE BLEED ───────────────────────────────────────────────────────────
    y = section(c, y, "THE BLEED - WHY EVERY MONTH PRINTS WITH A WHITE LINE")
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 13.5)
    c.drawString(M, y, "Canva adds 0.125 in (3.175 mm) on all sides - OUTSIDE your page.")
    y -= 16
    y = para(c, y, 'Canva: it is added "for products that trim or get cut", and "changing margin, bleed, and crop '
                   'mark sizes are also not available. These are fixed." Turn it on: File > Settings > Show print bleed.')
    y -= 4
    c.setFillColorRGB(*RED); c.setFont("Helvetica-Bold", 10.6)
    c.drawString(M, y, "A photo sized to fit the page is 3 mm short on all four sides. The cut lands past where it ends.")
    y -= 13
    c.setFillColorRGB(*GREEN); c.setFont("Helvetica-Bold", 10.6)
    c.drawString(M, y, 'Canva\'s own fix: "resize or stretch your background to cover them." Drag past the dashed line.')
    y -= 16
    bleed_diagram(c, M + 60, y - 74, 68, 66, False)
    bleed_diagram(c, M + 260, y - 74, 68, 66, True)
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10)
    c.drawString(M + 380, y - 10, "No two copies are trimmed in")
    c.drawString(M + 380, y - 23, "exactly the same place - so the")
    c.drawString(M + 380, y - 36, "sliver moves from edge to edge")
    c.drawString(M + 380, y - 49, "across the twelve months.")
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10)
    c.drawString(M + 380, y - 68, "It costs 3 mm of picture.")
    y -= 112
    rule(c, y); y -= 15

    # ── THE PIXELS ──────────────────────────────────────────────────────────
    y = section(c, y, "THE PIXELS - CHECK THE LONG EDGE BEFORE YOU CROP")
    c.setFillColorRGB(*INK); c.setFont("Courier-Bold", 11.5)
    c.drawString(M + 8, y, "page           300 dpi page      + Canva bleed")
    y -= 15
    for name, pg, bl in [("A4  210x297 mm", "2480 x 3508", "2565 x 3583"),
                         ("A3  297x420 mm", "3508 x 4961", "3583 x 5036"),
                         ("Letter 8.5x11 in", "2550 x 3300", "2625 x 3375")]:
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5); c.drawString(M + 8, y, name)
        c.setFillColorRGB(*BLUE); c.setFont("Courier-Bold", 10.5); c.drawString(M + 140, y, pg)
        c.setFillColorRGB(*AMBER); c.setFont("Courier-Bold", 10.5); c.drawString(M + 250, y, bl)
        y -= 14
    y -= 3
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 11.5)
    c.drawString(M, y, "RULE OF THUMB: about 2,500 px on the long edge for an A4 page - BEFORE you crop.")
    y -= 15
    y = para(c, y, "Check the pixel dimensions in your file browser, not the megapixels and not how it looks on a "
                   "phone. A photo straight off a modern phone clears it easily. The ones that fail are the COPIES - "
                   "anything that came through a messaging app, off social media, or by email. Those are compressed "
                   "on the way, often to around 1,600 px, and it is invisible on screen.", 10)
    y -= 2
    c.setFillColorRGB(*RED); c.setFont("Helvetica-Bold", 10.4)
    c.drawString(M, y, "Too small? Use it inset with a border, or do not use it. Stretching it to fill is what looks cheap in print.")
    y -= 14
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 9.8)
    c.drawString(M, y, "Canva's upload ceiling, at the other end: under 50 MB and no more than 250 million total pixels (JPEG, PNG, HEIC/HEIF, WebP).")
    y -= 15; rule(c, y); y -= 15

    # ── THE EXPORT ──────────────────────────────────────────────────────────
    y = section(c, y, "THE EXPORT - ONE CORRECT ANSWER")
    c.setFillColorRGB(*GREEN); c.setFont("Helvetica-Bold", 11.5)
    c.drawString(M + 8, y, "PDF Print")
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    c.drawString(M + 90, y, 'Canva: 300 dpi, "with bleed, crop marks, and color profile (RGB or CMYK)". Tick crop marks AND bleed.')
    y -= 14
    c.setFillColorRGB(*RED); c.setFont("Helvetica-Bold", 11.5)
    c.drawString(M + 8, y, "NOT Standard")
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    c.drawString(M + 105, y, "96 dpi - prints soft. And NOT JPG/PNG: 13 separate files, no crop marks on any of them.")
    y -= 15
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M, y, "Then OPEN the PDF and look at the corners: crop marks outside the page, photo running all the way out to them.")
    y -= 13
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.3)
    c.drawString(M, y, "If the photo stops at the page edge, you did not stretch it - go back before you send it.")
    y -= 15; rule(c, y); y -= 14

    # ── THE CHECKS ──────────────────────────────────────────────────────────
    y = section(c, y, "SEVEN CHECKS BEFORE YOU EXPORT")
    checks = [("Show print bleed is ON, and every photo is stretched past the dashed line on all four sides", True),
              ("Every date sits inside the margin guide", False),
              ("The first weekday of all twelve months checked against a real calendar", False),
              ("Every photo was 2,500+ px on its long edge BEFORE you cropped it", False),
              ("Thirteen pages, including a cover", False),
              ("The week starts on the same day throughout", False),
              ("Exported PDF Print with crop marks - not PDF Standard", False)]
    for t, hard in checks:
        c.setFillColorRGB(*(RED if hard else GREEN)); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "*")
        c.setFillColorRGB(*BODY); c.setFont("Helvetica-Bold" if hard else "Helvetica", 10.5)
        c.drawString(M + 13, y, t); y -= 11.8
    y -= 2
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Oblique", 9.4)
    c.drawString(M + 13, y, "The first is the one that ruins all twelve months at once - and you cannot see it until they are in the box.")

    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 8.4)
    c.drawString(M, M - 14, "Sources: Canva Help Centre - margins/bleed/crop marks; upload requirements; download file types.")
    c.drawRightString(W - M, M - 14, "Genius Junkie - geniusjunkie.net")
    c.showPage(); c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
