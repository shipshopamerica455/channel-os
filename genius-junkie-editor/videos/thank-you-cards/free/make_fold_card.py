#!/usr/bin/env python3
"""Fold & Print Card — the FREE one-pager.

Built NEW rather than carved out of the party-printables-kit: the kit is the
revenue that converts the same week, so the free rung creates appetite for it
instead of replacing part of it.

The panel diagram is DRAWN, not described, because the whole point of the video
is that the rotation is obvious once you see it and impossible to hold in your
head otherwise. The A-series figures are computed from ISO 216 so the card
cannot drift from the video.

Verified 2026-10-02. No printer-specific flip setting is named, and no postage
or card-stock weight is quoted — none was checked against a manufacturer's own
page.

Output: fold-and-print-card.pdf  (one page, US Letter)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

INK   = (0.149, 0.137, 0.125)
BODY  = (0.28, 0.30, 0.31)
GREY  = (0.553, 0.533, 0.502)
RULE  = (0.898, 0.878, 0.839)
PINK  = (0.914, 0.118, 0.549)
GREEN = (0.133, 0.773, 0.369)
BLUE  = (0.145, 0.388, 0.922)

W, H = letter
M = 0.62 * inch

# ISO 216 from the definition — A4 halved across the long side, twice.
def iso(n):
    s = {4: (210.0, 297.0)}
    for k in range(5, n + 1):
        w, h = s[k - 1]
        s[k] = (round(h / 2), w)
    return s[n]

A5_W, A5_H = iso(5)      # 148 x 210 → the SHEET is this rotated: 210 x 148
A6_W, A6_H = iso(6)      # 105 x 148 → the finished card


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


def sheet(c, x, y, w, h, rotated, caption):
    """One A5 sheet drawn to scale, with the fold line and both panels."""
    c.setFillColorRGB(1, 1, 1); c.setStrokeColorRGB(*RULE); c.setLineWidth(1)
    c.rect(x, y, w, h, fill=1, stroke=1)
    # fold line
    c.setStrokeColorRGB(*PINK); c.setDash(3, 3); c.setLineWidth(1)
    c.line(x + w / 2, y, x + w / 2, y + h); c.setDash()
    # right panel = FRONT
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(x + w * 0.75, y + h / 2 - 4, "thank you")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 6.5)
    c.drawCentredString(x + w * 0.75, y + 7, "RIGHT = FRONT")
    # left panel = BACK, drawn rotated when it should be
    c.saveState()
    c.setFillColorRGB(*(GREEN if rotated else PINK)); c.setFont("Helvetica", 8)
    if rotated:
        c.translate(x + w * 0.25, y + h / 2)
        c.rotate(180)
        c.drawCentredString(0, -3, "made by hand")
        c.restoreState()
    else:
        c.drawCentredString(x + w * 0.25, y + h / 2 - 3, "made by hand")
        c.restoreState()
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 6.5)
    c.drawCentredString(x + w * 0.25, y + 7, "LEFT = BACK")
    c.setFillColorRGB(*(GREEN if rotated else PINK)); c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(x + w / 2, y - 13, caption)


def build():
    path = os.path.join(OUT, "fold-and-print-card.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("Fold & Print Card — Genius Junkie")
    y = H - M

    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 25)
    c.drawString(M, y - 20, "Fold & Print Card")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "The panel layout, both page sizes, and the settings. Verified 2 October 2026.")
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 56; rule(c, y); y -= 24

    # ── THE DIAGRAM — the whole reason this page exists
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "THE ONE THAT GETS EVERYONE")
    y -= 18
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 16)
    c.drawString(M, y, "Rotate the LEFT panel 180° on the sheet")
    y -= 14
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10)
    c.drawString(M, y, "Fold a sheet and the top half flips over — so the left panel becomes the back of the card, upside down.")
    y -= 108

    sw, sh = 200, 88
    sheet(c, M + 10, y, sw, sh, False, "WRONG — back prints upside down")
    sheet(c, M + 10 + sw + 60, y, sw, sh, True, "RIGHT — rotated on the sheet")
    y -= 30
    c.setFillColorRGB(*BLUE); c.setFont("Helvetica-Bold", 10)
    c.drawString(M, y, "The INSIDE (page 2) is never rotated — it reads as one spread, left to right.")
    y -= 20; rule(c, y); y -= 24

    # ── SIZES
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "SIZES")
    y -= 8
    rows = [
        ("Card (finished)", f"{A6_W:.0f} x {A6_H:.0f} mm  (A6)", "5.5 x 4.25 in"),
        ("Sheet you print", f"{A5_H:.0f} x {A5_W:.0f} mm  (A5 landscape)", "8.5 x 5.5 in"),
        ("Margin, all round", "10 mm", "0.4 in"),
        ("Fold guide", f"{A5_H / 2:.0f} mm — the exact centre", "4.25 in"),
    ]
    c.setFillColorRGB(*GREY); c.setFont("Helvetica-Bold", 8.4)
    for x, t in [(M, "WHAT"), (M + 160, "METRIC"), (M + 370, "US EQUIVALENT")]:
        c.drawString(x, y - 12, t)
    y -= 24
    for a, b, d in rows:
        c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, a)
        c.setFont("Courier", 10.5); c.setFillColorRGB(*BODY)
        c.drawString(M + 160, y, b)
        c.drawString(M + 370, y, d)
        y -= 16
    y -= 8; rule(c, y); y -= 24

    # ── PRINTING
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "PRINTING")
    y -= 19
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    for t in [
        "Export PDF Print (300 DPI). PDF Standard is 96 DPI and this has type on it.",
        "Double-sided: your printer says \"flip on long edge\" or \"flip on short edge\". The names differ by make.",
        "DO NOT guess it. Print ONE, fold it, look at it. Wrong way up? Change the flip edge, print one more.",
        "Write the printer and the setting that worked on the back of that test card, in pencil. Keep it.",
        "Four up: four A6 fronts on an A4 sheet, artwork touching on the shared line, then cut down it.",
        "Steel rule and a sharp blade, three light passes. Scissors wander.",
    ]:
        c.setFillColorRGB(*PINK); c.drawString(M, y, "-")
        c.setFillColorRGB(*BODY); c.drawString(M + 12, y, t)
        y -= 14.5
    y -= 8; rule(c, y); y -= 24

    # ── THE FOLD
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "THE FOLD")
    y -= 19
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    for ln in wrap(
        "Score before you fold. Run the back of a butter knife, or a bone folder, down the centre "
        "line against a ruler — you are crushing the fibres in a straight line, not cutting them. "
        "Unscored card stock cracks along the spine and you get a white line through the fold. "
        "Once it cracks, that card is finished.", "Helvetica", 10.5, W - 2 * M):
        c.drawString(M, y, ln); y -= 13.6

    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 8.6)
    c.drawString(M, M - 10, "A-series figures computed from ISO 216 (A4 = 210 x 297 mm, halved across the long side).")
    c.drawString(M, M - 22, "Genius Junkie  ·  geniusjunkie.net/party-printables-kit")
    c.showPage(); c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
