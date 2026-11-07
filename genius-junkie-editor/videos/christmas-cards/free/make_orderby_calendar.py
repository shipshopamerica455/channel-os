#!/usr/bin/env python3
"""2026 Christmas Card Order-By Calendar — the FREE one-pager.

Built NEW, never carved out of the 2027-calendar-kit.

Verified 2026-10-29:
  * Canva Help Centre, "Estimate delivery time for print orders" — production 1-2
    business days (+1 after 5 PM); US Express 2-3 / Standard 5-8 / Economy 7-14
    business days; other supported regions Express 2-3, Standard 5-8; business
    days exclude public holidays; "The most accurate delivery timeframe for your
    order is always the one shown at checkout."
  * Canva US Folded Cards page — Economy "FREE" "11-20 days", Standard "7-12 days",
    Express "5-5 days"; sizes 5 x 7 portrait/landscape, 4.25 x 5.5.
  * USPS, 2026 holiday mailing dates (22 Sep 2026) — First-Class Mail Dec. 17.
  * Royal Mail, last posting dates Christmas 2026 — 2nd Class Fri 18 Dec,
    1st Class Mon 21 Dec.
  * Canva Help, margins/bleed/crop marks; print in the correct orientation.
  * Canva UK cards page — Letter rate "up to 24 x 16.5cm and 5mm thick".

The ORDER-BY dates are OUR arithmetic (labelled so on the card): cards in hand
by Fri 11 Dec (US) / Tue 15 Dec (UK); 2 production days + the top of each
shipping range, read as business days; US Thanksgiving (Thu 26 Nov) skipped.

NOT on this card: prices, whether envelopes are included, the UK free-delivery
time.

Output: christmas-card-order-by-calendar.pdf  (one page, US Letter)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))
INK, BODY, GREY = (0.133, 0.125, 0.122), (0.28, 0.30, 0.31), (0.557, 0.541, 0.525)
RULE, PINK, GREEN = (0.894, 0.878, 0.855), (0.914, 0.118, 0.549), (0.133, 0.773, 0.369)
BLUE, RED, XMAS = (0.145, 0.388, 0.922), (0.863, 0.149, 0.149), (0.70, 0.11, 0.18)
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


def para(c, y, t, size=10.2, font="Helvetica", col=BODY, lead=12.4):
    c.setFillColorRGB(*col); c.setFont(font, size)
    for ln in wrap(t, font, size, W - 2 * M):
        c.drawString(M, y, ln); y -= lead
    return y


def section(c, y, t):
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11); c.drawString(M, y, t)
    return y - 16


def table(c, y, head, rows):
    cols = [M + 6, M + 175, M + 330]
    c.setFillColorRGB(*GREY); c.setFont("Helvetica-Bold", 9)
    for x, h in zip(cols, head): c.drawString(x, y, h)
    y -= 14
    for i, (a, b, d, tone) in enumerate(rows):
        if i % 2 == 0:
            c.setFillColorRGB(*BAND); c.rect(M, y - 4.5, W - 2 * M, 16.5, stroke=0, fill=1)
        c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10.5); c.drawString(cols[0], y, a)
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.2); c.drawString(cols[1], y, b)
        c.setFillColorRGB(*tone); c.setFont("Helvetica-Bold", 11); c.drawString(cols[2], y, d)
        y -= 16.5
    return y


def build():
    path = os.path.join(OUT, "christmas-card-order-by-calendar.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("2026 Christmas Card Order-By Calendar - Genius Junkie")
    c.setAuthor("Genius Junkie")
    c.setCreator("geniusjunkie.net")
    c.setSubject("When to order Canva Print Christmas cards so they arrive in time")
    y = H - M
    c.setFillColorRGB(*XMAS); c.setFont("Helvetica-Bold", 22)
    c.drawString(M, y - 20, "2026 Christmas Card Order-By Calendar")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 10.2)
    c.drawString(M, y - 36, "Canva Print shipping against the post office's last dates. Verified 29 October 2026.")
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 36, "geniusjunkie.net")
    y -= 42; rule(c, y); y -= 15

    y = section(c, y, "THE RULE - FROM CANVA'S OWN HELP PAGE")
    y = para(c, y, '"The most accurate delivery timeframe for your order is always the one shown at checkout." '
                   "Read it before you pay. Production is 1-2 business days on top of shipping, plus one more if "
                   "you order after 5 PM.", 10.3, "Helvetica-Bold", INK)
    y -= 3; rule(c, y); y -= 15

    y = section(c, y, "US - USPS LAST DATE FOR FIRST-CLASS MAIL: THURSDAY 17 DECEMBER")
    y = table(c, y, ["CANVA SHIPPING", "CANVA'S FOLDED-CARDS PAGE", "ORDER BY (OUR SUMS)"], [
        ("Economy (free)", "11-20 days", "Tue 10 Nov", RED),
        ("Standard", "7-12 days", "Fri 20 Nov", BLUE),
        ("Express", "5 days", "Wed 2 Dec", GREEN),
    ])
    y -= 2
    y = para(c, y, "Our sums: cards in your hands by Fri 11 Dec, so you have a week to write and post them. "
                   "2 production days + the top of each range, read as business days, Thanksgiving (26 Nov) skipped.",
             9.4, "Helvetica-Oblique", GREY, 11.4)
    y -= 4; rule(c, y); y -= 15

    y = section(c, y, "UK - ROYAL MAIL: 2ND CLASS FRI 18 DEC  |  1ST CLASS MON 21 DEC")
    y = table(c, y, ["CANVA SHIPPING", "CANVA'S HELP PAGE", "ORDER BY (OUR SUMS)"], [
        ("Free UK delivery", "no time published", "check checkout", RED),
        ("Standard", "5-8 business days", "Mon 30 Nov", BLUE),
        ("Express", "2-3 business days", "Mon 7 Dec", GREEN),
    ])
    y -= 2
    y = para(c, y, "Our sums: cards in your hands by Tue 15 Dec, to post 2nd Class by Fri 18 Dec. "
                   "Canva's UK page: a standard card fits the Letter rate - up to 24 x 16.5 cm and 5 mm thick.",
             9.4, "Helvetica-Oblique", GREY, 11.4)
    y -= 4; rule(c, y); y -= 15

    y = section(c, y, "THE BUILD - 5 x 7 IN, PORTRAIT")
    for t in ["File > Rulers and guides > Show margins.   File > Settings > Show print bleed.",
              "Bleed is 0.125 in (3.175 mm) on every side - Canva says it \"cannot be adjusted\".",
              "Photo out to the bleed. Text and logos INSIDE the margins. Nothing across the fold.",
              "Landscape card? Canva: \"the panel for the back cover needs to be inverted\"."]:
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.2); c.drawString(M + 13, y, t); y -= 13
    y -= 2
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10.2)
    c.drawString(M, y, "Envelopes: neither Canva's US nor UK cards page says they're included - check, and order them too.")
    y -= 15; rule(c, y); y -= 15

    y = section(c, y, "SEVEN CHECKS BEFORE YOU PAY")
    checks = [("5 x 7, portrait", False),
              ("The photo fills the front, out to the bleed", False),
              ("All the words are inside the margins", False),
              ("The inside message leaves space to sign", False),
              ("You READ the delivery date at checkout - and it is before 11 Dec (US) / 15 Dec (UK)", True),
              ("You went through the mock-up, inside and outside", False),
              ("You know whether envelopes are included", False)]
    for t, hard in checks:
        c.setFillColorRGB(*(RED if hard else GREEN)); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "*")
        c.setFillColorRGB(*BODY); c.setFont("Helvetica-Bold" if hard else "Helvetica", 10.3)
        c.drawString(M + 13, y, t); y -= 12
    y -= 2
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Oblique", 9.4)
    c.drawString(M + 13, y, "The fifth is the one nobody does - the free option is already selected. Free and late is not free.")

    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 7.8)
    c.drawString(M, M - 14, "Sources: Canva Help Centre (delivery time; margins & bleed; orientation); Canva cards pages (US, UK); USPS; Royal Mail.")
    c.drawRightString(W - M, M - 14, "geniusjunkie.net")
    c.showPage(); c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
