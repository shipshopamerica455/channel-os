#!/usr/bin/env python3
"""Canva Export Decision Card — the FREE one-pager.

Built NEW rather than carved out of the lead-magnet-kit.

This one exists because the channel's own advice was incomplete: four print
videos said "always PDF Print", which is right for a printable and wrong for
anything read on a screen. The card is the decision table that should have
existed from the start.

Every claim is quoted from Canva's own Help Centre, verified 2026-10-02:
  · "Choose the right download file type for your Canva design"
  · "Download designs as flattened PDF"

NOT INCLUDED, deliberately: any platform file-size limit, any marketplace fee,
and any Canva subscription price. None was checked against the platform's own
page, and all of them change.

Output: canva-export-decision-card.pdf  (one page, US Letter)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

INK   = (0.118, 0.110, 0.102)
BODY  = (0.28, 0.30, 0.31)
GREY  = (0.541, 0.522, 0.498)
RULE  = (0.902, 0.882, 0.851)
PINK  = (0.914, 0.118, 0.549)
GREEN = (0.133, 0.773, 0.369)
BLUE  = (0.145, 0.388, 0.922)
AMBER = (0.961, 0.620, 0.043)

W, H = letter
M = 0.62 * inch


def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if stringWidth(t, font, size) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def rule(c, y):
    c.setStrokeColorRGB(*RULE); c.setLineWidth(0.8); c.line(M, y, W - M, y)


def build():
    path = os.path.join(OUT, "canva-export-decision-card.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("Canva Export Decision Card — Genius Junkie")
    y = H - M

    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 25)
    c.drawString(M, y - 20, "Canva Export Decision Card")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "Which export for which job. Verified against Canva's Help Centre, 2 October 2026.")
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 56; rule(c, y); y -= 26

    # ── THE DECISION
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "START HERE — WILL IT EVER BE PRINTED?")
    y -= 24

    col = (W - 2 * M) / 2 - 10
    for i, (title, tone, lines) in enumerate([
        ("NO — read on a screen", GREEN, [
            "PDF Standard  (96 DPI)",
            "Flatten: OFF",
            "Links stay clickable",
            "ebooks, lead magnets, guides",
        ]),
        ("YES — it goes on paper", BLUE, [
            "PDF Print  (300 DPI)",
            "Flatten: ON",
            "Bleed + crop marks if trimming",
            "planners, cards, KDP interiors",
        ]),
    ]):
        x = M + i * (col + 20)
        c.setStrokeColorRGB(*tone); c.setLineWidth(2)
        c.rect(x, y - 96, col, 94, fill=0, stroke=1)
        c.setFillColorRGB(*tone); c.setFont("Helvetica-Bold", 12.5)
        c.drawString(x + 12, y - 20, title)
        c.setFont("Courier-Bold", 11); c.setFillColorRGB(*INK)
        c.drawString(x + 12, y - 40, lines[0])
        c.setFont("Helvetica", 10); c.setFillColorRGB(*BODY)
        for j, ln in enumerate(lines[1:]):
            c.drawString(x + 12, y - 56 - j * 13, ln)
    y -= 118; rule(c, y); y -= 26

    # ── WHAT CANVA ACTUALLY SAYS
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "WHAT CANVA ACTUALLY SAYS")
    y -= 20
    for quote in [
        "PDF Standard is \"for multi-page and text-heavy documents\" — use it \"if you intend to share your file through email\".",
        "PDF Print is \"for printing\", and \"the only file type that saves professional print quality at 300 DPI\".",
        "Flattening \"may increase file size, especially with high-resolution images or complex designs\".",
        "Compress PDF reduces file size and is \"available only to paid Canva accounts\".",
    ]:
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
        for k, ln in enumerate(wrap(quote, "Helvetica", 10.5, W - 2 * M - 14)):
            if k == 0:
                c.setFillColorRGB(*PINK); c.drawString(M, y, "-"); c.setFillColorRGB(*BODY)
            c.drawString(M + 12, y, ln); y -= 13.4
        y -= 3
    y -= 8; rule(c, y); y -= 26

    # ── THE FLATTEN TRADE
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "FLATTEN — WHAT IT COSTS YOU EITHER WAY")
    y -= 20
    for tone, head, text in [
        (GREEN, "Flatten ON", "Nobody can edit your file. Fonts are locked. Right for a pitch deck or anything printed."),
        (PINK, "Flatten OFF", "Links keep working. Right for anything with a contents page — flattening turns pages into images and every link dies."),
    ]:
        c.setFillColorRGB(*tone); c.setFont("Helvetica-Bold", 11.5)
        c.drawString(M + 8, y, head)
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
        lines = wrap(text, "Helvetica", 10.5, W - 2 * M - 110)
        for k, ln in enumerate(lines):
            c.drawString(M + 108, y - k * 13, ln)
        y -= max(16, len(lines) * 13 + 5)
    y -= 10; rule(c, y); y -= 26

    # ── BEFORE YOU SHIP
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "BEFORE YOU SHIP IT")
    y -= 19
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    for t in [
        "Open the EXPORTED file — not the Canva design — and click a contents link. This is the one people skip.",
        "Read a paragraph at 100% zoom. If you lean in, the type is too small.",
        "Shrink the cover to postage-stamp size. If the title is unreadable, it is not finished.",
        "Check the page count is what you think, and the filename is not \"final version 2\".",
        "Put a version and date on the last page, so you can tell buyers when you update it.",
    ]:
        c.setFillColorRGB(*PINK); c.drawString(M, y, "-")
        c.setFillColorRGB(*BODY)
        for k, ln in enumerate(wrap(t, "Helvetica", 10.5, W - 2 * M - 14)):
            c.drawString(M + 12, y - k * 13, ln)
        y -= 13.4 * len(wrap(t, "Helvetica", 10.5, W - 2 * M - 14)) + 2

    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 8.6)
    c.drawString(M, M - 10, "Sources: Canva Help Centre — \"Choose the right download file type\"; \"Download designs as flattened PDF\".")
    c.drawString(M, M - 22, "Genius Junkie  ·  geniusjunkie.net/lead-magnet-kit")
    c.showPage(); c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
