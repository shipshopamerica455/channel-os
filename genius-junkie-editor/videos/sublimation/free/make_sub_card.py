#!/usr/bin/env python3
"""Canva Sublimation Card — the FREE one-pager.

Built NEW, never carved out of the sticker-illustration-kit: the pack is the
only revenue that converts the same week, so the free rung has to create
appetite for it rather than replace part of it.

Every claim is quoted from the source named beside it, verified 2026-10-05:
  * Epson    — dye-sublimation requires polyester or polymer-coated surfaces
  * Printify — there is no white ink; white areas are the product itself
  * Sawgrass — their VersiFlex system does not print white ink
  * Canva    — RGB is converted automatically; transparent PNG is Pro-only;
               the Content Licence Agreement names mugs

Deliberately NOT on this card: the price of any printer, ink, paper or blank,
which brand is best, or a universal blank size. Suppliers differ and the card
says so -- it teaches inches x 300 and sends you to your own template.

Output: canva-sublimation-card.pdf  (one page, US Letter)
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
AMBER = (0.961, 0.620, 0.043)

W, H = letter
M = 0.5 * inch


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


def rule(c, y):
    c.setStrokeColorRGB(*RULE)
    c.setLineWidth(0.8)
    c.line(M, y, W - M, y)


def para(c, y, text, size=10.5, font="Helvetica", col=BODY, lead=12.6):
    c.setFillColorRGB(*col)
    c.setFont(font, size)
    for ln in wrap(text, font, size, W - 2 * M):
        c.drawString(M, y, ln)
        y -= lead
    return y


def section(c, y, title):
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, title)
    return y - 19


def build():
    path = os.path.join(OUT, "canva-sublimation-card.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("Canva Sublimation Card - Genius Junkie")

    y = H - M
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 25)
    c.drawString(M, y - 20, "Canva Sublimation Card")
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "The white-ink rule, the blank, the sizes. Verified 5 October 2026.")
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 46
    rule(c, y)
    y -= 18

    # -- THE ONE THAT RUINS DESIGNS
    y = section(c, y, "THE ONE THAT RUINS DESIGNS")
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(M, y, "There is no white ink. White is a WINDOW onto the blank.")
    y -= 17
    y = para(c, y, '"Dye sublimation requires light-colored materials because there\'s no white ink '
                   'in the standard process. White areas are inherent to the product itself."',
             10, "Helvetica-Oblique")
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 8.6)
    c.drawString(M, y, "Printify. Sawgrass say the same of their VersiFlex ink: it does not print with white.")
    y -= 20
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y, "In Canva white is a colour you pick. At the press it is the absence of ink, so:")
    y -= 16
    for t, ok in [("White text on a DARK SHAPE works - the shape is ink, the letters are the blank", True),
                  ("White text on nothing is invisible. Blank on blank", False),
                  ("A white drop shadow, outline or glow does nothing at all", False),
                  ("Off-white, cream and the palest grey ARE ink - they do print", False)]:
        c.setFillColorRGB(*(GREEN if ok else PINK))
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "+" if ok else "-")
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica", 10.5)
        c.drawString(M + 13, y, t)
        y -= 12.8
    y -= 4
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(M, y, "The ten-second test: drop a mid-tone rectangle behind your design and see what survives.")
    y -= 14
    rule(c, y)
    y -= 18

    # -- THE BLANK
    y = section(c, y, "THE BLANK")
    y = para(c, y, '"Dye-sublimation printing requires polyester fabrics or polymer-coated surfaces." '
                   "(Epson.) Not a preference - the dye bonds with polyester. On cotton it sits on "
                   "the surface, looks acceptable for about one wash, and then it is gone.", 10.5)
    y -= 4
    for t, ok in [("Polyester fabric, or a polymer-coated hard good (mug, tumbler, slate, metal)", True),
                  ("LIGHT blanks only - on a dark blank the ink is translucent and disappears", True),
                  ("Cotton, or an uncoated mug from a supermarket: takes nothing at all", False)]:
        c.setFillColorRGB(*(GREEN if ok else PINK))
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "+" if ok else "-")
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica", 10.5)
        c.drawString(M + 13, y, t)
        y -= 12.8
    y -= 2
    rule(c, y)
    y -= 18

    # -- THE SIZE
    y = section(c, y, "THE SIZE")
    c.setFillColorRGB(*INK)
    c.setFont("Courier-Bold", 14)
    c.drawString(M, y, "inches x 300 = pixels")
    y -= 20
    for a, b in [("9 x 3.5 in mug wrap", "2700 x 1050 px"), ("10 x 12 in shirt area", "3000 x 3600 px")]:
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica", 10.5)
        c.drawString(M + 13, y, a)
        c.setFillColorRGB(*BLUE)
        c.setFont("Courier-Bold", 11.5)
        c.drawString(M + 200, y, b)
        y -= 14
    y -= 2
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M, y, "Your blank supplier publishes a template. THAT is the number that counts - suppliers differ.")
    y -= 15
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y, "Canva: Custom size, switch units to pixels, type it in. Never design small and scale up.")
    y -= 14
    rule(c, y)
    y -= 18

    # -- THE EXPORT
    y = section(c, y, "THE EXPORT - AND THE MYTH")
    y = para(c, y, '"Export transparent or you get a white box" is a PRINT ON DEMAND rule, where a '
                   "provider lays white ink onto a dark shirt. Your sublimation printer has no white "
                   "ink, so a white background and a transparent one do the same thing. Export "
                   "transparent anyway - it is the only way YOU can see the windows.", 10.5)
    y -= 4
    c.setFillColorRGB(*AMBER)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M, y, "Share > Download > PNG > Transparent background ON. Tick 2x size if offered.")
    y -= 15
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 9)
    c.drawString(M, y, "Transparent background is Canva Pro, Teams, Business, Education and Nonprofits only.")
    y -= 15
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y, "Mirror ONCE. Most printer software mirrors for you - do both and it is not mirrored.")
    y -= 15
    c.drawString(M, y, "Canva is RGB and converts automatically. Press a colour swatch sheet once and keep it.")
    y -= 14
    rule(c, y)
    y -= 16

    # -- THE CHECKS
    y = section(c, y, "SEVEN CHECKS BEFORE YOU PRESS")
    checks = [
        ("The background is deleted, not white", True),
        ("Everything that must be visible is INK, not white", True),
        ("You looked at it on a mid-tone background and it still reads", True),
        ("The PNG is transparent, and in the thousands of pixels", False),
        ("The blank is polyester or polymer coated - and light", False),
        ("You mirrored exactly once. Printer software OR Canva, not both", False),
        ("Every element came from a Canva search filtered to Free", False),
    ]
    for t, first in checks:
        c.setFillColorRGB(*(PINK if first else GREEN))
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "*")
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica-Bold" if first else "Helvetica", 10.5)
        c.drawString(M + 13, y, t)
        y -= 12.4
    y -= 2
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Oblique", 9.4)
    c.drawString(M + 13, y, "The first three are all the same thing, which tells you how often it is the thing that goes wrong.")

    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 8.4)
    c.drawString(M, M - 14, "Sources: Epson; Printify; Sawgrass; Canva Help Centre; Canva Content Licence Agreement.")
    c.drawRightString(W - M, M - 14, "Genius Junkie - geniusjunkie.net")

    c.showPage()
    c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
