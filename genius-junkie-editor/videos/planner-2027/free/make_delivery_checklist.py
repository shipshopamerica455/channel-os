#!/usr/bin/env python3
"""Printable Planner Delivery Checklist — the FREE one-pager.

Built NEW rather than carved out of the 2027 Calendar Kit: the kit is the
revenue that converts the same week, so the free rung creates appetite for it
instead of replacing part of it.

Every Canva claim here is quoted from Canva's own Help Centre, verified
2026-10-02 ("Share your design as a template link", "Sharing designs via email
or links", "Download designs as flattened PDF").

Deliberately contains NO Etsy fee and NO Canva subscription price — neither was
checked against the platform's own page in that session, and a tutorial channel
loses credibility on exactly that kind of number.

Output: printable-planner-delivery-checklist.pdf  (one page, US Letter)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

INK   = (0.122, 0.114, 0.106)
BODY  = (0.28, 0.30, 0.31)
GREY  = (0.545, 0.529, 0.510)
RULE  = (0.902, 0.886, 0.859)
PINK  = (0.914, 0.118, 0.549)
GREEN = (0.133, 0.773, 0.369)
BLUE  = (0.145, 0.388, 0.922)

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
    path = os.path.join(OUT, "printable-planner-delivery-checklist.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("Printable Planner Delivery Checklist — Genius Junkie")
    y = H - M

    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 24)
    c.drawString(M, y - 20, "Printable Planner Delivery Checklist")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "Six checks before you list. Canva facts verified 2 October 2026.")
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 56; rule(c, y); y -= 26

    # ── THE ONE THAT COSTS YOU THE SHOP
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "THE ONE THAT COSTS YOU THE SHOP")
    y -= 21
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 17)
    c.drawString(M, y, "Template link, not edit link")
    y -= 21
    for label, url, note, col in [
        ("TEMPLATE LINK", ".../template", "each buyer gets their own copy", GREEN),
        ("EDIT LINK", ".../view?...", "they are guests IN your design", PINK),
    ]:
        c.setFillColorRGB(*col); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M + 8, y, label)
        c.setFillColorRGB(*INK); c.setFont("Courier-Bold", 12)
        c.drawString(M + 128, y, url)
        c.setFillColorRGB(*GREY); c.setFont("Helvetica-Oblique", 10)
        c.drawString(M + 248, y, note)
        y -= 18
    y -= 4
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    for ln in wrap(
        "Canva: the edit link \"lets people make changes without signing up or logging in to "
        "Canva\". There is only one master file — twelve buyers are all in it. To get the right "
        "one: Share, then See all (it is hidden behind that), then Create template link.",
        "Helvetica", 10.5, W - 2 * M):
        c.drawString(M, y, ln); y -= 13.4
    y -= 4
    # wrap it — as one line this ran off the right edge and lost its last word
    c.setFillColorRGB(*BLUE); c.setFont("Helvetica-Bold", 10.5)
    for ln in wrap(
        "Template links are Pro, Teams, Enterprise, Education or Nonprofits only. "
        "Deleting one makes the URL inactive for every buyer who has it.",
        "Helvetica-Bold", 10.5, W - 2 * M):
        c.drawString(M, y, ln); y -= 13.4
    y -= 10; rule(c, y); y -= 26

    # ── THE SIX CHECKS
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "THE SIX CHECKS")
    y -= 22
    checks = [
        ("The link says /template", "not /view, not /edit. Read the URL before you paste it."),
        ("Both page sizes exist", "US Letter 8.5 x 11 in AND A4 210 x 297 mm. Open both."),
        ("The dates are 2027 dates", "1 Jan 2027 is a Friday. Weekdays move every year."),
        ("February has 28 days", "2027 is not a leap year."),
        ("Print file is PDF Print, flattened", "PDF Standard is 96 DPI. PDF Print is 300."),
        ("You bought your own listing", "Different browser, as a stranger. The only real test."),
    ]
    for i, (t, note) in enumerate(checks, 1):
        c.setFillColorRGB(*GREEN); c.setFont("Helvetica-Bold", 13)
        c.drawString(M, y, "[  ]")
        c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 12)
        c.drawString(M + 34, y, f"{i}.  {t}")
        c.setFillColorRGB(*GREY); c.setFont("Helvetica", 10)
        c.drawString(M + 300, y, note)
        y -= 19
    y -= 6; rule(c, y); y -= 26

    # ── BUILD SETTINGS
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "BUILD SETTINGS")
    y -= 19
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    for t in [
        "Margin 0.5 in all round. A hole punch bites about a centimetre in — half an inch clears it.",
        "Month grids need SIX rows. A 31-day month starting on a Saturday needs six, not five.",
        "Weekday names on EVERY month, not just January. People print one month on its own.",
        "Day numbers lighter than the buyer's handwriting. The numbers are furniture.",
        "Resize to A4 as a COPY, then check the right edge, the bottom edge, and any heading that may now wrap.",
    ]:
        c.setFillColorRGB(*PINK); c.drawString(M, y, "-")
        c.setFillColorRGB(*BODY); c.drawString(M + 12, y, t)
        y -= 14.5
    y -= 10; rule(c, y); y -= 24

    # ── THE DELIVERY
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "WHAT GOES IN THE ORDER")
    y -= 19
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
    for t in [
        "1.  Printable PDF, US Letter — 300 DPI, flattened",
        "2.  Printable PDF, A4 — the same, checked separately",
        "3.  The template link",
        "4.  One page of instructions — most support messages are buyers who did not know to click it",
        "5.  If you sell a digital version: a SECOND export, NOT flattened (flattening kills clickable links)",
    ]:
        c.drawString(M + 4, y, t); y -= 14.5

    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 8.6)
    c.drawString(M, M - 10, "Sources: Canva Help Centre — Share your design as a template link; Sharing designs via link; Download as flattened PDF.")
    c.drawString(M, M - 22, "Genius Junkie  ·  geniusjunkie.net/2027-calendar-kit")
    c.showPage(); c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
