#!/usr/bin/env python3
"""Canva Wedding Website Checklist — the FREE one-pager.

Built NEW, never carved out of the party-printables-kit.

Verified 2026-10-19:
  * Canva Help Centre, "Publish websites to a free domain" — Website template
    required for .canva.site; "Canva Free users can have up to five live
    websites on the free domain"; Mobile website / Link in Bio publish to
    canva.link only; "Resize on mobile"; the footer stays on Free
  * Google Docs Editors Help, "View & manage form responses" — "form owners can
    download and delete existing responses"
  * Google Docs Editors COMMUNITY guide — the /copy link (labelled as such)
  * Google Workspace Learning Center — Accepting responses / Set close date
  * Canva Newsroom — countdown timer "using Canva Code"

NOT on this card: any price, Canva Code availability on Free, how an embedded
form renders.

Output: canva-wedding-website-checklist.pdf  (one page, US Letter)
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


def line(c, y, t, col=BODY, font="Helvetica", size=10.5, x=None):
    c.setFillColorRGB(*col); c.setFont(font, size); c.drawString(x if x is not None else M + 13, y, t)
    return y - 13


def build():
    path = os.path.join(OUT, "canva-wedding-website-checklist.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("Canva Wedding Website Checklist - Genius Junkie")
    y = H - M
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 25)
    c.drawString(M, y - 20, "Canva Wedding Website Checklist")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "Publishing rules, the RSVP trap, and the phone checks. Verified 19 October 2026.")
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 42; rule(c, y); y -= 15

    # ── THE TRAP ────────────────────────────────────────────────────────────
    y = section(c, y, "THE TRAP - THE RSVP FORM BELONGS TO WHOEVER MADE IT")
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 13)
    c.drawString(M, y, "Every reply lands in the form owner's Responses tab - not the couple's.")
    y -= 15
    y = para(c, y, 'Google: "form owners can download and delete existing responses." Build the site for '
                   'someone else, or sell it as a template, with YOUR form behind the RSVP button and '
                   'every guest list ends up in your account. Sharing the form does not fix it - that '
                   'gives them access to yours. They need their own COPY.')
    y -= 3
    ROWS = [
        ("Your own wedding", "nothing to do - you own the form", GREEN),
        ("Built for someone", "they make the form, or More > Make a copy (Google help)", AMBER),
        ("Selling the template", "form URL ending in /copy - prompts each buyer to copy it *", BLUE),
    ]
    for i, (who, what, tone) in enumerate(ROWS):
        if i % 2 == 0:
            c.setFillColorRGB(*BAND); c.rect(M, y - 4.5, W - 2 * M, 17, stroke=0, fill=1)
        c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10.5); c.drawString(M + 6, y, who)
        c.setFillColorRGB(*tone); c.setFont("Helvetica-Bold", 10.2); c.drawString(M + 140, y, what)
        y -= 17
    y -= 2
    c.setFillColorRGB(*GREY); c.setFont("Helvetica-Oblique", 8.8)
    c.drawString(M, y, "* From a Google Docs Editors COMMUNITY guide, not an official policy page - test it before you rely on it.")
    y -= 13
    y = para(c, y, "Then let Google close it: Accepting responses > Set close date. Late RSVPs after "
                   "the caterer has the numbers are worse than none.", 10.5, "Helvetica-Bold", INK)
    y -= 3; rule(c, y); y -= 15

    # ── PUBLISHING RULES ────────────────────────────────────────────────────
    y = section(c, y, "CANVA'S PUBLISHING RULES - THE TEMPLATE DECIDES THE ADDRESS")
    for t, tone in [
        ("Free .canva.site address: the design must come from a WEBSITE template.", INK),
        ("Mobile website / Link in Bio templates: canva.link only, and NO custom domain.", RED),
        ('Canva: "Canva Free users can have up to five live websites on the free domain."', AMBER),
        ("The Designed with Canva footer stays on Free - removing it needs Pro.", BODY),
        ("Publish website > Site address > Settings > Continue > Publish.", BLUE),
    ]:
        y = line(c, y, t, tone, "Helvetica-Bold" if tone in (INK, RED) else "Helvetica")
    y -= 2
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10.4)
    c.drawString(M, y, "The address is a promise: once it is printed on an invitation it cannot change. Name it, then print it.")
    y -= 15; rule(c, y); y -= 15

    # ── THE PHONE ───────────────────────────────────────────────────────────
    y = section(c, y, "THE PHONE - MOST GUESTS NEVER SEE THE DESKTOP VERSION")
    y = line(c, y, 'Turn on "Resize on mobile" in the publishing settings - then do not trust it.', INK, "Helvetica-Bold")
    y = line(c, y, "Preview in mobile view and go through EVERY page, top to bottom.")
    y = line(c, y, "Look for: text that moved, text shrunk to nothing, buttons too small for a thumb.", RED, "Helvetica-Bold")
    y = line(c, y, "Anything side by side on desktop has to stack on a phone - the stacking is where it breaks.")
    y = line(c, y, "The countdown is made with Canva Code (Canva's own wedding page) - check the time zone.", BLUE)
    y -= 2; rule(c, y); y -= 15

    # ── GETTING IT TO GUESTS ────────────────────────────────────────────────
    y = section(c, y, "GETTING IT TO THE GUESTS")
    y = line(c, y, "Test the link from a phone that is NOT yours - logged in, you may not see what a guest sees.")
    y = line(c, y, "QR code on the printed invitation: large, plain background, scanned from the PRINTED PROOF.", INK, "Helvetica-Bold")
    y = line(c, y, "A QR code that works on a laptop and fails on paper is the most common way this goes wrong.", RED)
    y -= 2; rule(c, y); y -= 14

    # ── THE CHECKS ──────────────────────────────────────────────────────────
    y = section(c, y, "SEVEN CHECKS BEFORE YOU SEND THE ADDRESS TO ANYONE")
    checks = [("The design was made from a Website template", False),
              ("The RSVP button points at a form the COUPLE owns - not you", True),
              ("You filled in the RSVP yourself on the published site, and it arrived in the right account", False),
              ("Resize on mobile is on, and every page was checked in mobile view", False),
              ("The RSVP button is big enough to tap with a thumb", False),
              ("The form has a close date", False),
              ("The QR code scans from the printed proof, not just the screen", False)]
    for t, hard in checks:
        c.setFillColorRGB(*(RED if hard else GREEN)); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "*")
        c.setFillColorRGB(*BODY); c.setFont("Helvetica-Bold" if hard else "Helvetica", 10.5)
        c.drawString(M + 13, y, t); y -= 11.8
    y -= 2
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Oblique", 9.4)
    c.drawString(M + 13, y, "The second is the one that goes wrong silently - and nobody finds out until the guest list is missing.")

    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 8.2)
    c.drawString(M, M - 14, "Sources: Canva Help Centre; Canva Newsroom; Google Docs Editors Help + Community guide; Google Workspace.")
    c.drawRightString(W - M, M - 14, "geniusjunkie.net")
    c.showPage(); c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
