#!/usr/bin/env python3
"""Canva Newsletter Export Card — the FREE one-pager.

Built NEW, never carved out of the digital-magazine-kit.

Verified 2026-10-10:
  * Canva Help Centre, "Add hyperlinks" — "Hyperlinks will only work if you
    download your design as a PDF (except flattened PDFs)"; "Image formats like
    JPG and PNG do not support hyperlinks regardless of the image source"
  * Canva Help Centre, "Download designs as flattened PDF" — flattening
    "converts your design with multiple layers into one" and "ensures fonts
    display accurately and secures your design"
  * Canva Help Centre, "Choose the right download file type" — PDF Standard
    96 dpi; PDF Print 300 dpi "with bleed, crop marks, and color profile"

NOT on this card: how any email client renders or clips a message, what any
email platform charges, open rates, click rates or deliverability.

Output: canva-newsletter-export-card.pdf  (one page, US Letter)
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


def build():
    path = os.path.join(OUT, "canva-newsletter-export-card.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("Canva Newsletter Export Card - Genius Junkie")
    y = H - M
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 25)
    c.drawString(M, y - 20, "Canva Newsletter Export Card")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "Which export keeps your links, and which one quietly kills them. Verified 10 October 2026.")
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 42; rule(c, y); y -= 15

    # ── THE LINK TABLE — the whole point of the card ────────────────────────
    y = section(c, y, "DO YOUR LINKS SURVIVE?")
    ROWS = [
        ("In the Canva editor", "YES", GREEN, "which is why nobody catches this"),
        ("PDF Standard  (96 dpi)", "YES", GREEN, "the normal choice for an emailed newsletter"),
        ("PDF Print  (300 dpi)", "YES", GREEN, "the one to send to whoever prints it"),
        ("PDF with FLATTEN ticked", "NO", RED, "every layer merged into one image - links included"),
        ("JPG", "NO", RED, "image formats do not support hyperlinks at all"),
        ("PNG", "NO", RED, "same - 'regardless of the image source'"),
        ("Posted to social media", "NO", RED, "Canva says so explicitly"),
    ]
    rh = 17.5
    for i, (fmt, verdict, tone, note) in enumerate(ROWS):
        if i % 2 == 0:
            c.setFillColorRGB(*BAND); c.rect(M, y - 4.5, W - 2 * M, rh, stroke=0, fill=1)
        c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M + 6, y, fmt)
        c.setFillColorRGB(*tone); c.setFont("Helvetica-Bold", 11)
        c.drawString(M + 170, y, verdict)
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 9.8)
        c.drawString(M + 205, y, note)
        y -= rh
    y -= 4
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 12)
    c.drawString(M, y, 'Canva: "Hyperlinks will only work if you download your design as a PDF (except flattened PDFs)."')
    y -= 16; rule(c, y); y -= 15

    # ── THE FLATTEN TRAP ────────────────────────────────────────────────────
    y = section(c, y, "THE FLATTEN TRAP - WHY CAREFUL PEOPLE GET CAUGHT")
    y = para(c, y, "Flatten is not an obscure setting. It is what Canva offers when your fonts render "
                   "wrong on somebody else's machine - the single most common newsletter complaint there is.")
    y -= 3
    c.setFillColorRGB(*AMBER); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M + 13, y, 'Canva: flattening "ensures fonts display accurately and secures your design".')
    y -= 13
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    c.drawString(M + 13, y, 'It does that by converting "your design with multiple layers into one". Your links were layers.')
    y -= 15
    c.setFillColorRGB(*RED); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "So the fix for the fonts is the thing that kills the links - and nothing warns you either time.")
    y -= 14
    c.setFillColorRGB(*GREEN); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M, y, "INSTEAD: export twice and open it on the machine the fonts were wrong on. Leave flatten off.")
    y -= 16; rule(c, y); y -= 15

    # ── 96 vs 300 ───────────────────────────────────────────────────────────
    y = section(c, y, "NINETY-SIX OR THREE HUNDRED - THEY ARE NOT THE SAME FILE")
    for title, dpi, tone, note in [
        ("PDF Standard", "96 dpi", BLUE, 'Canva: "for illustrations, text, and graphics". Smaller file - right for the email.'),
        ("PDF Print", "300 dpi", AMBER, 'Canva: "with bleed, crop marks, and color profile (RGB or CMYK) selection option".'),
    ]:
        c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 11.5); c.drawString(M + 6, y, title)
        c.setFillColorRGB(*tone); c.setFont("Courier-Bold", 11.5); c.drawString(M + 110, y, dpi)
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10); c.drawString(M + 175, y, note)
        y -= 15
    y -= 2
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10.6)
    c.drawString(M, y, "If anybody is printing it, you need BOTH. Same design, two downloads, thirty seconds.")
    y -= 13
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.3)
    c.drawString(M, y, "96 dpi is a screen resolution - a Standard PDF run off on a school printer comes out soft, and there is no fixing it after.")
    y -= 16; rule(c, y); y -= 15

    # ── THE PHONE TEST ──────────────────────────────────────────────────────
    y = section(c, y, "THE PHONE TEST, AND THE SEND TEST")
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    c.drawString(M + 13, y, "A PDF on a phone opens as the WHOLE page, so an A4 page arrives about the size of a playing card.")
    y -= 13
    c.setFillColorRGB(*GREEN); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M + 13, y, "Should survive at that size: the masthead, the lead headline, the shape of the blocks.")
    y -= 13
    c.setFillColorRGB(*RED); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M + 13, y, "Headlines gone grey too? They are too small. Nobody zooms in to find out what they say.")
    y -= 13
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M + 13, y, "Then send it to yourself, open it ON YOUR PHONE, and click two links - one near the top, one near the bottom.")
    y -= 16; rule(c, y); y -= 14

    # ── THE CHECKS ──────────────────────────────────────────────────────────
    y = section(c, y, "SEVEN CHECKS BEFORE YOU SEND IT")
    checks = [("Every link clicked in the EXPORTED file, not in the editor", True),
              ("Flatten is off", False),
              ("You know whether this copy is the 96 or the 300, and who is getting which", False),
              ("The masthead is identical to last issue", False),
              ("Every block has the date, the time and the place IN it - not only in the link", False),
              ("It still reads at phone size, and the headlines are not grey stripes", False),
              ("It came out of the template, not out of last month's issue", False)]
    for t, hard in checks:
        c.setFillColorRGB(*(RED if hard else GREEN)); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "*")
        c.setFillColorRGB(*BODY); c.setFont("Helvetica-Bold" if hard else "Helvetica", 10.5)
        c.drawString(M + 13, y, t); y -= 11.8
    y -= 2
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Oblique", 9.4)
    c.drawString(M + 13, y, "The first is the one that actually goes wrong - and it goes wrong silently, in the one file your readers get.")

    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 8.4)
    c.drawString(M, M - 14, "Sources: Canva Help Centre - Add hyperlinks; flattened PDF; download file types.")
    c.drawRightString(W - M, M - 14, "Genius Junkie - geniusjunkie.net")
    c.showPage(); c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
