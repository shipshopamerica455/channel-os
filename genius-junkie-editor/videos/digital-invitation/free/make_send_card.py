#!/usr/bin/env python3
"""Digital Invitation Send Card — the FREE one-pager.

Built NEW, never carved out of the party-printables-kit.

Verified 2026-10-28:
  * Canva Help Centre, "Add hyperlinks" — "Hyperlinks will not work on PNGs,
    JPGs, MP4s, etc., or when you post your design on social media."
    "Links remain clickable by downloading your design as a PDF or by presenting
    it." "...except flattened PDFs". "For videos, hyperlinks are only clickable in
    the Presenter window while on Presenter view." Page links: "Pages in this
    document".
  * Canva Help Centre, "Design websites" — "each page will appear as a separate
    scrollable page on the same website"; Free publishes 10 sections per page;
    Resize on mobile.
  * Canva Help Centre, "Publish websites to a free domain" — Website template
    only; "Canva Free users can have up to five live websites on the free
    domain"; link-in-bio and mobile sites publish to canva.link only.

NOT on this card: the free-domain suffix, whether a view-only link keeps links
clickable, how any messaging app previews a link, plan or domain prices.

Output: digital-invitation-send-card.pdf  (one page, US Letter)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))
INK, BODY, GREY = (0.133, 0.125, 0.122), (0.28, 0.30, 0.31), (0.557, 0.541, 0.525)
RULE, PINK, GREEN = (0.894, 0.878, 0.855), (0.914, 0.118, 0.549), (0.133, 0.773, 0.369)
BLUE, RED = (0.145, 0.388, 0.922), (0.863, 0.149, 0.149)
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


def para(c, y, t, size=10.5, font="Helvetica", col=BODY, lead=12.6):
    c.setFillColorRGB(*col); c.setFont(font, size)
    for ln in wrap(t, font, size, W - 2 * M):
        c.drawString(M, y, ln); y -= lead
    return y


def section(c, y, t):
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 11); c.drawString(M, y, t)
    return y - 17


def build():
    path = os.path.join(OUT, "digital-invitation-send-card.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    # Metadata a buyer's PDF viewer shows — reportlab's default is "anonymous"
    # (caught by PdfCraft `info`, 24 Oct 2026).
    c.setTitle("Digital Invitation Send Card - Genius Junkie")
    c.setAuthor("Genius Junkie")
    c.setCreator("geniusjunkie.net")
    c.setSubject("Which ways of sending a Canva invitation keep the tap working")
    y = H - M
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 25)
    c.drawString(M, y - 20, "Digital Invitation Send Card")
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "Which ways of sending keep the tap working - in Canva's own words. Verified 28 October 2026.")
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 42; rule(c, y); y -= 15

    # ── WHERE THE TAP SURVIVES ──────────────────────────────────────────────
    y = section(c, y, "WHERE THE TAP SURVIVES - FROM CANVA'S OWN HELP PAGE")
    ROWS = [
        ("Published website", "WORKS", "send the link - the way this card recommends", GREEN),
        ("PDF (standard)", "WORKS", '"Links remain clickable by downloading your design as a PDF"', GREEN),
        ("Presenting", "WORKS", "only while you are presenting it yourself", GREEN),
        ("PDF (flattened)", "DEAD", '"...except flattened PDFs"', RED),
        ("PNG / JPG", "DEAD", '"Hyperlinks will not work on PNGs, JPGs, MP4s..."', RED),
        ("MP4 video", "DEAD", '"only clickable in the Presenter window"', RED),
        ("Posted to social", "DEAD", '"...or when you post your design on social media"', RED),
    ]
    for i, (k, v, note, tone) in enumerate(ROWS):
        if i % 2 == 0:
            c.setFillColorRGB(*BAND); c.rect(M, y - 4.5, W - 2 * M, 17, stroke=0, fill=1)
        c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10.5); c.drawString(M + 6, y, k)
        c.setFillColorRGB(*tone); c.setFont("Helvetica-Bold", 11); c.drawString(M + 135, y, v)
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 9.8); c.drawString(M + 195, y, note)
        y -= 17
    y -= 3
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 11.5)
    c.drawString(M, y, "A picture of an invitation is a picture. Send the LINK - and the picture only as a teaser.")
    y -= 16; rule(c, y); y -= 15

    # ── THE BUILD ───────────────────────────────────────────────────────────
    y = section(c, y, "THE BUILD - THREE PAGES, ONE WEBSITE")
    y = para(c, y, "Start from a WEBSITE template (search \"website\"). Not a poster, not a post - and not a "
                   "mobile site or link in bio: Canva says those publish to a canva.link address only. "
                   "Each page publishes as \"a separate scrollable page on the same website\".", 10.3)
    y -= 4
    for k, v, tone in [("Page 1", "The envelope. Big, a seal with the initial, and the words: You're invited - tap to open.", BLUE),
                       ("Page 2", "The opened card: what, when, where - one line each, readable without zooming.", PINK),
                       ("Page 3", "The details: address + map button, reply button, dress code, parking, gift list.", BLUE)]:
        c.setFillColorRGB(*tone); c.setFont("Helvetica-Bold", 10.5); c.drawString(M + 13, y, k)
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.2); c.drawString(M + 65, y, v)
        y -= 13.5
    y -= 3
    c.setFillColorRGB(*GREEN); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M, y, "Link: select the envelope > More > Link > Pages in this document > page 2. Same for the words.")
    y -= 13
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.2)
    c.drawString(M, y, "Keep the envelope and the words as separate pieces, both linked - a tap anywhere near it opens it.")
    y -= 15; rule(c, y); y -= 15

    # ── PUBLISH ─────────────────────────────────────────────────────────────
    y = section(c, y, "PUBLISH IT FREE - TWO LIMITS TO KNOW")
    y = para(c, y, "Publish website > site address (keep it short) > Settings > turn on Resize on mobile > "
                   "Continue > Publish.", 10.3, "Helvetica-Bold", INK)
    y = para(c, y, "1. \"Canva Free users can have up to five live websites on the free domain.\" Unpublish "
                   "an invitation after the event and the slot is yours again.", 10.3)
    y = para(c, y, "2. Canva Free publishes up to 10 sections per page. If something is missing on the "
                   "published site, check that first.", 10.3)
    y -= 2; rule(c, y); y -= 15

    # ── CHECKS ──────────────────────────────────────────────────────────────
    y = section(c, y, "SEVEN CHECKS BEFORE A SINGLE GUEST SEES IT")
    checks = [("It was made from a website template", False),
              ("The envelope AND the words both link to page 2", False),
              ("Page 2 links to the details page", False),
              ("Every button on the details page goes where it says", False),
              ("You opened the PUBLISHED link on a phone, from a message, and tapped through every page", True),
              ("Every line is readable with the phone at arm's length", False),
              ("You are sending the link - not the PNG, not the MP4", False)]
    for t, hard in checks:
        c.setFillColorRGB(*(RED if hard else GREEN)); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "*")
        c.setFillColorRGB(*BODY); c.setFont("Helvetica-Bold" if hard else "Helvetica", 10.5)
        c.drawString(M + 13, y, t); y -= 12.2
    y -= 2
    c.setFillColorRGB(*PINK); c.setFont("Helvetica-Oblique", 9.4)
    c.drawString(M + 13, y, "The fifth is the one nobody does - everything works in the editor. Your guests are not in the editor.")

    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 8.2)
    c.drawString(M, M - 14, "Sources: Canva Help Centre - Add hyperlinks; Design websites; Publish websites to a free domain.")
    c.drawRightString(W - M, M - 14, "geniusjunkie.net")
    c.showPage(); c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
