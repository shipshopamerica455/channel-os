#!/usr/bin/env python3
"""Wedding Stationery Size Card — the FREE one-pager.

Built NEW rather than carved out of the party-printables-kit: the pack is the
revenue that converts the same week, so the free rung creates appetite for it
instead of replacing part of it.

The ISO column is COMPUTED from the standard's own definition (each size is the
one above halved across the long side, starting at A4 = 210 x 297 mm), so the
A7 figure in the table cannot drift from the A7 figure in the video.

Verified 2026-09-28. Deliberately contains NO postage prices — rates change and
none was verified against a carrier's own rate page.

Output: wedding-stationery-size-card.pdf  (one page, US Letter)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

INK   = (0.169, 0.153, 0.141)
BODY  = (0.28, 0.30, 0.31)
GREY  = (0.553, 0.525, 0.494)
RULE  = (0.902, 0.878, 0.839)
PINK  = (0.914, 0.118, 0.549)
GREEN = (0.133, 0.773, 0.369)
BLUE  = (0.145, 0.388, 0.922)

W, H = letter
M = 0.62 * inch

# ISO 216, from the definition — never a lookup table.
def iso_series(n=7):
    sizes = {4: (210.0, 297.0)}
    for k in range(5, n + 1):
        w, h = sizes[k - 1]
        sizes[k] = (round(h / 2), w)      # halve across the long side
    return sizes

ISO = iso_series()
A7_W, A7_H = ISO[7]                        # 74 x 105 mm


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


def rule(c, y, col=RULE):
    c.setStrokeColorRGB(*col); c.setLineWidth(0.8); c.line(M, y, W - M, y)


def build():
    path = os.path.join(OUT, "wedding-stationery-size-card.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("Wedding Stationery Size Card — Genius Junkie")
    y = H - M

    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 25)
    c.drawString(M, y - 20, "Wedding Stationery Size Card")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "Every card and envelope, in inches and millimetres. Verified 28 September 2026.")
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 56; rule(c, y); y -= 26

    # ── THE ONE THAT COSTS MONEY
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "THE ONE THAT COSTS MONEY")
    y -= 21
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 18)
    c.drawString(M, y, '"A7" is two completely different sizes')
    y -= 22
    for label, val, note, col in [
        ("A7 envelope  ·  United States", "5.25 x 7.25 in", "holds a 5 x 7 card", BLUE),
        ("A7 paper  ·  ISO 216", f"{A7_W:.0f} x {A7_H:.0f} mm", "holds nothing in this suite", PINK),
    ]:
        c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 11.5)
        c.drawString(M + 8, y, label)
        c.setFillColorRGB(*col); c.setFont("Courier-Bold", 12.5)
        c.drawString(M + 236, y, val)
        # the note column starts clear of the widest value string above
        c.setFillColorRGB(*GREY); c.setFont("Helvetica-Oblique", 10)
        c.drawString(M + 366, y, note)
        y -= 19
    y -= 4
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    for ln in wrap(
        "Order the envelope by its MEASUREMENT, never by its name. The envelope must be bigger "
        "than the card in both directions, by about an eighth to a quarter of an inch. If the two "
        "numbers look the same, stop.", "Helvetica", 10.5, W - 2 * M):
        c.drawString(M, y, ln); y -= 13.4
    y -= 12; rule(c, y); y -= 26

    # ── THE SUITE
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "THE SUITE")
    y -= 8
    rows = [
        ("Invitation", "5 x 7 in", "127 x 178 mm", "A7 envelope (US)"),
        ("Details card", "5 x 7 in", "127 x 178 mm", "stacks with the invitation"),
        ("Reply card", "3.5 x 5 in", "89 x 127 mm", "A1 envelope, or 4 x 6 postcard"),
        ("Order of service", "5.83 x 8.27 in", "148 x 210 mm (A5)", "folded from A4"),
        ("Table number", "5.83 x 8.27 in", "148 x 210 mm (A5)", "standing in a frame"),
        ("Seating plan", "—", "A2 or A1", "by guest count"),
    ]
    c.setFillColorRGB(*GREY); c.setFont("Helvetica-Bold", 8.6)
    for x, t in [(M, "PIECE"), (M + 150, "INCHES"), (M + 268, "MILLIMETRES"), (M + 400, "ENVELOPE / NOTE")]:
        c.drawString(x, y - 13, t)
    y -= 26
    for name, inch_s, mm_s, note in rows:
        c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 11)
        c.drawString(M, y, name)
        c.setFont("Courier", 11); c.setFillColorRGB(*BODY)
        c.drawString(M + 150, y, inch_s)
        c.drawString(M + 268, y, mm_s)
        c.setFont("Helvetica", 10); c.setFillColorRGB(*GREY)
        c.drawString(M + 400, y, note)
        y -= 17
    y -= 8; rule(c, y); y -= 26

    # ── ISO, FROM THE DEFINITION
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "WHY ISO A7 IS SO SMALL — IT IS ARITHMETIC")
    y -= 20
    c.setFillColorRGB(*BODY); c.setFont("Courier", 11.5)
    chain = "  ->  ".join(f"A{k} {int(ISO[k][0])}x{int(ISO[k][1])}" for k in sorted(ISO))
    c.drawString(M + 8, y, chain)
    y -= 16
    c.setFont("Helvetica", 10.5)
    c.drawString(M + 8, y, "Each size is the one above halved across the long side. A7 is not a choice.")
    y -= 24; rule(c, y); y -= 26

    # ── PRINT + POST
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "PRINTING AND POSTING")
    y -= 19
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    for t in [
        "Bleed 0.125 in every side (5 x 7 becomes 5.25 x 7.25). Keep all type 0.25 in inside the trim.",
        "Print at ACTUAL SIZE / 100%. Every print dialog defaults to Fit, which shrinks the card.",
        "Print ONE and put it in the envelope before ordering any quantity.",
        "Square envelopes, wax seals, ribbon and anything rigid are non-machinable and cost more to post.",
        "No postage price is printed here on purpose — weigh one sealed invitation at the counter.",
        "Write the month as a word. 10/09/2027 is two different days depending on who reads it.",
    ]:
        c.setFillColorRGB(*PINK); c.drawString(M, y, "•")
        c.setFillColorRGB(*BODY); c.drawString(M + 12, y, t)
        y -= 14.5

    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 8.6)
    # two footer lines, stacked — side by side they collided on Letter width
    c.drawString(M, M - 10, "ISO 216 computed from A4 = 210 x 297 mm. US envelope sizing per standard announcement-envelope charts.")
    c.drawString(M, M - 22, "Genius Junkie  ·  geniusjunkie.net/party-printables-kit")
    c.showPage(); c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
