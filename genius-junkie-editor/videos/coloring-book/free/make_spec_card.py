#!/usr/bin/env python3
"""KDP Coloring Book Spec Card — the FREE one-pager.

This is the lead magnet, and it is built NEW rather than carved out of the
kdp-interior-pack: the pack is the only revenue that converts the same week,
so the free rung has to create appetite for it, not replace part of it.

Every number here is quoted from Amazon KDP's own help pages, verified
2026-09-24:
  · Paperback Submission Guidelines  — line weight, DPI, fonts, flattening,
                                       page-count rounding
  · Set Trim Size, Bleed, and Margins — bleed edges and the margin table

Output: kdp-coloring-book-spec-card.pdf  (one page, US Letter)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

INK   = (0.133, 0.125, 0.122)
BODY  = (0.28, 0.30, 0.31)
GREY  = (0.557, 0.541, 0.525)
RULE  = (0.894, 0.878, 0.855)
PINK  = (0.914, 0.118, 0.549)
GREEN = (0.133, 0.773, 0.369)
BLUE  = (0.145, 0.388, 0.922)
PAPER = (1, 1, 1)

W, H = letter
M = 0.62 * inch


def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if stringWidth(t, font, size) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rule(c, y, x0=M, x1=W - M, col=RULE, w=0.8):
    c.setStrokeColorRGB(*col)
    c.setLineWidth(w)
    c.line(x0, y, x1, y)


def build():
    path = os.path.join(OUT, "kdp-coloring-book-spec-card.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("KDP Coloring Book Spec Card — Genius Junkie")

    y = H - M

    # ── masthead
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 25)
    c.drawString(M, y - 20, "KDP Coloring Book Spec Card")
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "Every number Amazon actually requires. Verified 24 September 2026.")
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 56
    rule(c, y)
    y -= 26

    # ── THE ONE THAT BREAKS BOOKS
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "THE ONE THAT BREAKS BOOKS")
    y -= 20
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 19)
    c.drawString(M, y, "Minimum line weight:  0.75 pt  ·  0.01 in  ·  0.3 mm")
    y -= 18
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10.5)
    for ln in wrap(
        "A coloring book is nothing but lines, so this applies to every stroke in it. "
        "Canva's element line art is often 0.5 pt — under the floor. It looks perfect on "
        "screen and prints as a broken dotted line, or not at all. Work at 1 pt to give "
        "yourself the margin.", "Helvetica", 10.5, W - 2 * M):
        c.drawString(M, y, ln)
        y -= 13.4
    y -= 6
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(M, y, "Scaling an image down scales its stroke down with it.")
    y -= 15
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y, "A 1 pt line at half size is a 0.5 pt line. Resize FIRST, then read the stroke, then fix it.")
    y -= 24
    rule(c, y)
    y -= 26

    # ── BLEED
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "BLEED — NOT SYMMETRICAL")
    y -= 19
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica", 11.5)
    c.drawString(M, y, "0.125 in on the TOP, BOTTOM and OUTER edge. Nothing on the inner edge — that is the spine.")
    y -= 20
    c.setFont("Courier-Bold", 12)
    c.drawString(M + 8, y, "page height  =  trim height + 0.125 + 0.125   =  + 0.25 in")
    y -= 16
    c.drawString(M + 8, y, "page width   =  trim width  + 0.125           =  + 0.125 in")
    y -= 20
    c.setFillColorRGB(*GREEN)
    c.setFont("Helvetica-Bold", 12.5)
    c.drawString(M + 8, y, "8.5 x 11 in  ->  8.625 x 11.25 in")
    y -= 18
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica-Oblique", 10.5)
    c.drawString(M, y, "Canva's bleed sits on all four sides. Do not use it — type the bled size in as your custom size.")
    y -= 24
    rule(c, y)
    y -= 26

    # ── MARGINS
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "INSIDE MARGIN — BY PAGE COUNT")
    y -= 8
    rows = [("24 – 150 pages", "0.375 in"), ("151 – 300", "0.5 in"),
            ("301 – 500", "0.625 in"), ("501 – 700", "0.75 in"), ("701 – 828", "0.875 in")]
    colw = (W - 2 * M) / len(rows)
    for i, (a, b) in enumerate(rows):
        x = M + i * colw
        c.setFillColorRGB(*GREY)
        c.setFont("Helvetica", 8.6)
        c.drawString(x, y - 14, a)
        c.setFillColorRGB(*BLUE if i == 0 else INK)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x, y - 30, b)
    y -= 46
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y, "Outside margin: 0.25 in minimum without bleed, 0.375 in with it.")
    y -= 14
    c.drawString(M, y, "Change the page count and the inside margin may change — go back and check it.")
    y -= 24
    rule(c, y)
    y -= 26

    # ── EXPORT
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "EXPORTING FROM CANVA")
    y -= 20
    for label, val, col in [
        ("PDF Standard", "96 DPI  —  do not use", PINK),
        ("PDF Print", "300 DPI  —  use this", GREEN),
    ]:
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(M + 8, y, label)
        c.setFillColorRGB(*col)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(M + 140, y, val)
        y -= 18
    y -= 2
    for label, val, col in [
        ("Crop marks and bleed", "LEAVE UNTICKED", PINK),
        ("Flatten PDF", "TICK IT", GREEN),
    ]:
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica", 11.5)
        c.drawString(M + 8, y, label)
        c.setFillColorRGB(*col)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString(M + 200, y, val)
        y -= 17
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10)
    c.drawString(M + 8, y, "You already built the bleed into the page size. Flatten also embeds fonts, which Amazon requires.")
    y -= 24
    rule(c, y)
    y -= 24

    # ── ALSO TRUE
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "ALSO TRUE")
    y -= 17
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10.5)
    for t in [
        "Minimum 24 pages. Amazon rounds the page count UP to an even number.",
        "Images at least 300 DPI. Fonts embedded. Transparency flattened.",
        "Custom trim: width 4–8.5 in, height 6–11.69 in.",
        "Interior and cover are two separate uploads — lock the page count before making the cover.",
        "Blank backs are a convention buyers expect (markers soak through), NOT an Amazon rule.",
    ]:
        c.setFillColorRGB(*PINK)
        c.drawString(M, y, "•")
        c.setFillColorRGB(*BODY)
        c.drawString(M + 12, y, t)
        y -= 14

    # ── footer
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 8.6)
    c.drawString(M, M - 14, "Sources: KDP Paperback Submission Guidelines; Set Trim Size, Bleed and Margins.")
    c.drawRightString(W - M, M - 14, "Genius Junkie · geniusjunkie.net/kdp-interior-pack")

    c.showPage()
    c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
