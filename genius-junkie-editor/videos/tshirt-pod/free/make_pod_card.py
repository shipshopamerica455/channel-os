#!/usr/bin/env python3
"""Canva POD Licence & Size Card — the FREE one-pager.

Built NEW, never carved out of the sticker-illustration-kit: the pack is the
only revenue that converts the same week, so the free rung has to create
appetite for it rather than replace part of it.

Every clause here is quoted from the source named beside it, verified
2026-10-05:
  · Canva Content Licence Agreement — the prohibited and permitted uses
  · Canva Help Centre, "Download design with transparent background"
  · Printful, "How to prepare the perfect print file" — named as an EXAMPLE,
    because providers differ and this card says so.

Deliberately NOT on this card: what any POD company charges, what a shirt
costs, or what margin to expect. None of that was checked against a provider's
own pricing page, so none of it is stated.

Output: canva-pod-licence-size-card.pdf  (one page, US Letter)
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
M = 0.55 * inch


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


def para(c, y, text, size=10.5, font="Helvetica", col=BODY, lead=13.4, indent=0):
    c.setFillColorRGB(*col)
    c.setFont(font, size)
    for ln in wrap(text, font, size, W - 2 * M - indent):
        c.drawString(M + indent, y, ln)
        y -= lead
    return y


def build():
    path = os.path.join(OUT, "canva-pod-licence-size-card.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("Canva POD Licence & Size Card — Genius Junkie")

    y = H - M

    # ── masthead
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 25)
    c.drawString(M, y - 20, "Canva POD Licence & Size Card")
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "What you may sell, at what size. Verified 5 October 2026 against Canva's own pages.")
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 50
    rule(c, y)
    y -= 22

    # ── THE ONE THAT CLOSES SHOPS
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "THE ONE THAT CLOSES SHOPS")
    y -= 19
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M, y, "PRO content may NOT go on a t-shirt you sell.")
    y -= 17
    y = para(c, y, '"Use or display the Content on a standalone basis on websites or other venues '
                   'designed to induce or involving the sale, license or other distribution of '
                   "'on demand' products, including postcards, mugs, t-shirts, posters and other "
                   'items."', 10, "Helvetica-Oblique", BODY, 12.6)
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 8.6)
    c.drawString(M, y, "Canva Content Licence Agreement — what you may not do with Pro Content")
    y -= 18

    c.setFillColorRGB(*GREEN)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M, y, "FREE content explicitly MAY.")
    y -= 17
    y = para(c, y, '"prints, posters (i.e. hardcopies) and other reproductions for personal or '
                   'promotional purposes, resale, license or other distribution."',
             10, "Helvetica-Oblique", BODY, 12.6)
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 8.6)
    c.drawString(M, y, "Same agreement — permitted uses of Free Content")
    y -= 22

    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(M, y, "The only visible difference is a small crown on the thumbnail.")
    y -= 15
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y, "And once the element is on your canvas you cannot see it at all. There is no "
                       '"is this safe to sell" button.')
    y -= 20
    rule(c, y)
    y -= 22

    # ── HOW TO CHECK
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "SO THE CHECK HAPPENS AT THE POINT OF PLACING")
    y -= 19
    for t in [
        "Elements -> the filter icon -> Price: Free. EVERY search, not once per session — it does not always persist.",
        "Unsure about an element already in a design? Delete it and place it again from a filtered search.",
        "On a FREE plan the download dialog lists Pro content before it will export. On PRO it says nothing,",
        "because for every OTHER purpose you are entitled to use it. Your subscription is not the issue.",
    ]:
        c.setFillColorRGB(*BLUE)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "•")
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica", 10.5)
        c.drawString(M + 12, y, t)
        y -= 13.2
    y -= 4
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(M, y, "Rebuilding is cheaper than a takedown.")
    y -= 18
    rule(c, y)
    y -= 22

    # ── THE PRINT FILE
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "THE PRINT FILE")
    y -= 8
    rows = [("Print area (max)", "12 x 16 in"), ("Resolution", "150-300 DPI"),
            ("Pixels across", "3,600-4,800"), ("Format", "PNG, transparent")]
    colw = (W - 2 * M) / len(rows)
    for i, (a, b) in enumerate(rows):
        x = M + i * colw
        c.setFillColorRGB(*GREY)
        c.setFont("Helvetica", 8.6)
        c.drawString(x, y - 14, a)
        c.setFillColorRGB(*BLUE)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x, y - 30, b)
    y -= 44
    c.setFillColorRGB(*INK)
    c.setFont("Courier-Bold", 14)
    c.drawString(M, y, "4500 x 5400 px")
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M + 128, y, "— a comfortable middle that fits a 12 x 16 area at 300 DPI.")
    y -= 17
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M, y, "Printful's figures, named as an example. Providers differ — check your own provider's spec page.")
    y -= 18
    rule(c, y)
    y -= 22

    # ── THE EXPORT
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "THE EXPORT, AND THE IRONY IN IT")
    y -= 19
    y = para(c, y, 'Downloading with a transparent background is "only available to Canva Pro, '
                   'Canva Teams, Canva Business, Canva Education, and Canva for Nonprofits plans." '
                   "(Canva Help Centre.) So you need Pro for the export and you must not use Pro "
                   "in the design. Both are true at once.", 10.5)
    y -= 4
    c.setFillColorRGB(*AMBER)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M, y, "Share -> Download -> PNG -> Transparent background ON. Tick 2x size if offered — more pixels is the cheap win.")
    y -= 20
    rule(c, y)
    y -= 20

    # ── THE SIX CHECKS
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "SIX CHECKS BEFORE YOU UPLOAD")
    y -= 17
    checks = [
        ("Every element came from a search filtered to Free, or you made it.", True),
        ("PNG with transparency actually on — checked against a dark background.", False),
        ("Dimensions in the thousands, matching your provider's print area.", False),
        ("Your thinnest line survives at 100% zoom. Fabric cannot hold a hairline.", False),
        ("Print file and listing images in different folders.", False),
        ("A note of where every element came from. Two lines per design.", False),
    ]
    for t, legal in checks:
        c.setFillColorRGB(*(PINK if legal else GREEN))
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "✓")
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica-Bold" if legal else "Helvetica", 10.5)
        c.drawString(M + 13, y, t)
        y -= 13.2
    y -= 2
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Oblique", 9.6)
    c.drawString(M + 13, y, "The first one is the one that matters legally, and the one that cannot be fixed after the fact.")

    # ── footer
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 8.6)
    c.drawString(M, M - 14, "Sources: Canva Content Licence Agreement; Canva Help Centre; Printful.")
    c.drawRightString(W - M, M - 14, "Genius Junkie · geniusjunkie.net")

    c.showPage()
    c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
