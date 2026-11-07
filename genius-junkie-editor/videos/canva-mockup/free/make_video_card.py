#!/usr/bin/env python3
"""Etsy Listing Video Card — the FREE one-pager.

Built NEW, never carved out of the etsy-listing-image-kit.

Verified 2026-10-21:
  * Etsy Help, "How to Add Listing Videos" (read in a browser) — 3-15 seconds,
    "will not contain any audio once uploaded", aspect ratio "should be 2:1 or
    1:2", min 500px / ideal >=1080px, 100 MB, up to 2 videos per listing
  * Canva Help Centre, "Apply, change, or remove animations" — Create an
    Animation; "Each animation can only be 10 seconds long at the maximum";
    animated designs download as videos or GIFs
  * Canva, "Free Online Phone Mockup Generator" — mockups download as PDF, SVG,
    JPG or PNG (stills)

NOT on this card: what Etsy does to a video of another ratio, Etsy fees, sales
uplift, which mockups are free.

Output: etsy-listing-video-card.pdf  (one page, US Letter)
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


def para(c, y, t, size=10.5, font="Helvetica", col=BODY, lead=12.0):
    c.setFillColorRGB(*col); c.setFont(font, size)
    for ln in wrap(t, font, size, W - 2 * M):
        c.drawString(M, y, ln); y -= lead
    return y


def section(c, y, t):
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11); c.drawString(M, y, t)
    return y - 17


def line(c, y, t, col=BODY, font="Helvetica", size=10.5):
    c.setFillColorRGB(*col); c.setFont(font, size); c.drawString(M + 13, y, t)
    return y - 13


def build():
    path = os.path.join(OUT, "etsy-listing-video-card.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("Etsy Listing Video Card - Genius Junkie")
    y = H - M
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 25)
    c.drawString(M, y - 20, "Etsy Listing Video Card")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "Etsy's rules, Canva's limit, and the size to build at. Verified 21 October 2026.")
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 42; rule(c, y); y -= 15

    # ── ETSY'S RULES ────────────────────────────────────────────────────────
    y = section(c, y, "ETSY'S RULES - FROM ETSY'S OWN HELP PAGE")
    ROWS = [
        ("Length", "3 - 15 seconds", "anything longer is not a listing video", RED),
        ("Sound", "NONE", '"will not contain any audio once uploaded"', RED),
        ("Shape", "2:1 or 1:2", "a 9:16 phone video is neither", RED),
        ("Resolution", "1080 px ideal", "500 px minimum", BLUE),
        ("File size", "100 MB max", "MP4, MOV and others", BLUE),
        ("How many", "2 per listing", "almost everyone uses one, or none", GREEN),
    ]
    for i, (k, v, note, tone) in enumerate(ROWS):
        if i % 2 == 0:
            c.setFillColorRGB(*BAND); c.rect(M, y - 4.5, W - 2 * M, 17, stroke=0, fill=1)
        c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10.5); c.drawString(M + 6, y, k)
        c.setFillColorRGB(*tone); c.setFont("Helvetica-Bold", 11); c.drawString(M + 100, y, v)
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10); c.drawString(M + 220, y, note)
        y -= 17
    y -= 3
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 11.5)
    c.drawString(M, y, "The usual scrolling mockup - 9:16, 30 seconds, set to music - breaks all three red rows.")
    y -= 16; rule(c, y); y -= 15

    # ── CANVA ───────────────────────────────────────────────────────────────
    y = section(c, y, "CANVA'S SIDE - TWO THINGS NOBODY TELLS YOU")
    y = para(c, y, "1. Canva's mockups are STILLS. Elements > Mockups > Smartphones makes a great listing "
                   "PHOTO - and it downloads as PDF, SVG, JPG or PNG. There is no video option. The "
                   "scrolling version is built separately.", 10.5, "Helvetica", BODY)
    y -= 3
    y = para(c, y, '2. "Each animation can only be 10 seconds long at the maximum." (Canva Help) - so '
                   "your scroll is 10 seconds or less, which fits inside Etsy's 15 nicely.", 10.5,
             "Helvetica-Bold", INK)
    y -= 4; rule(c, y); y -= 15

    # ── THE BUILD ───────────────────────────────────────────────────────────
    y = section(c, y, "THE BUILD - EXACT NUMBERS")
    c.setFillColorRGB(*INK); c.setFont("Courier-Bold", 13)
    c.drawString(M + 10, y, "video page  1080 x 2160   = exactly 1:2"); y -= 17
    c.drawString(M + 10, y, "screenshot  1080 wide, up to 3125 tall (Canva's limit)"); y -= 19
    for k, v, tone in [("Page 1", "the top of the screenshot, still - 2 s", BLUE),
                       ("Page 2", "Animate > Create an Animation, drag UP, hold Shift - 10 s", PINK),
                       ("Page 3", "the bottom of the screenshot, still - 2 s", BLUE)]:
        c.setFillColorRGB(*tone); c.setFont("Helvetica-Bold", 10.5); c.drawString(M + 13, y, k)
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5); c.drawString(M + 70, y, v)
        y -= 13
    y -= 2
    c.setFillColorRGB(*GREEN); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M, y, "= 14 seconds. Transitions off, so it reads as one shot. Download as MP4 video.")
    y -= 13
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.2)
    c.drawString(M, y, "Pages flying past too fast to read? The screenshot is too tall for 10 s - take a page OUT, don't speed it up.")
    y -= 15; rule(c, y); y -= 15

    # ── SILENT FIRST ────────────────────────────────────────────────────────
    y = section(c, y, "DESIGN FOR SILENCE - ETSY REMOVES THE SOUND")
    y = line(c, y, "Watch it with the sound OFF. What does a shopper actually learn?", INK, "Helvetica-Bold")
    y = line(c, y, "Facts go on screen as text: how many pages, what size, editable in Canva.")
    y = line(c, y, "Put the first line on the FIRST FRAME - that second is all most shoppers see.")
    y = line(c, y, 'Nothing that needs a voice: no "watch this", no "here\'s the best bit".', RED)
    y -= 2; rule(c, y); y -= 14

    # ── CHECKS ──────────────────────────────────────────────────────────────
    y = section(c, y, "SEVEN CHECKS BEFORE IT GOES ON ETSY")
    checks = [("The page is 1080 x 2160 - one to two", False),
              ("The video is under 15 seconds", False),
              ("The scroll is 10 seconds or less", False),
              ("Every page is readable as it passes", False),
              ("The facts are on screen, and it makes sense with the sound OFF", True),
              ("The first frame says what the product is", False),
              ("You made the SECOND video too - e.g. the template opening and being edited in Canva", False)]
    for t, hard in checks:
        c.setFillColorRGB(*(RED if hard else GREEN)); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "*")
        c.setFillColorRGB(*BODY); c.setFont("Helvetica-Bold" if hard else "Helvetica", 10.5)
        c.drawString(M + 13, y, t); y -= 11.8
    y -= 2
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Oblique", 9.4)
    c.drawString(M + 13, y, "The fifth is the one nobody checks - because they never watch their own video silent.")

    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 8.2)
    c.drawString(M, M - 14, "Sources: Etsy Help - How to Add Listing Videos; Canva Help Centre; Canva phone mockup page.")
    c.drawRightString(W - M, M - 14, "geniusjunkie.net")
    c.showPage(); c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
