#!/usr/bin/env python3
"""Canva Website Mobile Check Card — the FREE rung.

Built NEW, never carved out of the Canva Website Launch Kit: the kit's audit
sheets are per-page worksheets; this card is the rules on one sheet.

Verified 2026-11-06 (Canva Help Centre, read that day):
  * "My website looks different on mobile" — "Reflow adapts Canva websites to
    different screen sizes by stacking elements vertically." Overlapping
    elements shrink in mobile view; ungrouped elements can separate ("Otherwise,
    they might separate in mobile view."). The five fixes, verbatim:
    "Select elements in your design and resize or crop them so their borders
    don't touch." / "Replace large elements that span the full width with
    smaller ones that stack neatly." / "Keep important elements inside the safe
    margin boundaries." / "Use the mobile preview panel while editing." ("Treat
    it as an approximation, since the published site can vary by device and
    browser.") / "Group related elements, then lock the group so they stay
    together." Paths: select (drag or Shift-click) → floating toolbar → Group;
    Preview → Mobile button.
  * "Publish websites to a free domain" — "Turn on Resize on mobile to optimize
    your site for mobile devices."
  * "Designing websites" — "Resize on mobile: Automatically adjust your design
    for mobile screens"; up to 45 pages; Free publishes up to 10 sections a
    page (design up to 20); paid plans publish up to 20.

NOT claimed: a phone canvas size (Canva gives none).

Output: canva-website-mobile-check-card.pdf (one page, Letter)
"""
import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))
INK, BODY, GREY = (0.133, 0.125, 0.122), (0.28, 0.30, 0.31), (0.557, 0.541, 0.525)
PINK, GREEN, BLUE, AMBER = (0.914, 0.118, 0.549), (0.133, 0.773, 0.369), (0.145, 0.388, 0.922), (0.96, 0.62, 0.04)
BAND = (0.957, 0.949, 0.933)
W, H = letter


def card():
    path = os.path.join(OUT, 'canva-website-mobile-check-card.pdf')
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle('Canva Website Mobile Check Card · Genius Junkie')
    c.setAuthor('Genius Junkie')
    L = 0.65 * inch
    R = W - 0.65 * inch
    y = H - 0.7 * inch

    def wrap(text, x, width, font='Helvetica', size=9.6, color=BODY, lead=1.36, bullet=''):
        nonlocal y
        c.setFont(font, size)
        c.setFillColorRGB(*color)
        words, line, first = text.split(), '', True
        for w_ in words:
            trial = (line + ' ' + w_).strip()
            if c.stringWidth(trial, font, size) > width - (12 if bullet else 0):
                c.drawString(x + (0 if first or not bullet else 12), y, ((bullet + '  ') if first and bullet else '') + line)
                y -= size * lead
                line, first = w_, False
            else:
                line = trial
        c.drawString(x + (0 if first or not bullet else 12), y, ((bullet + '  ') if first and bullet else '') + line)
        y -= size * (lead + 0.18)

    def head(t, tone):
        nonlocal y
        y -= 4
        c.setFillColorRGB(*tone)
        c.rect(L, y - 2, 4, 13, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 12.5)
        c.setFillColorRGB(*INK)
        c.drawString(L + 10, y, t)
        y -= 17

    c.setFont('Helvetica-Bold', 9)
    c.setFillColorRGB(*PINK)
    c.drawString(L, y, 'GENIUS JUNKIE · FREE · VERIFIED AGAINST CANVA HELP, 6 NOV 2026')
    y -= 28
    c.setFont('Helvetica-Bold', 23)
    c.setFillColorRGB(*INK)
    c.drawString(L, y, 'Canva website: the mobile check card')
    y -= 18
    c.setFont('Helvetica', 11)
    c.setFillColorRGB(*BODY)
    c.drawString(L, y, 'There is one design. The phone version is stacked from it — so every fix goes on the desktop page.')
    y -= 22

    head('How a phone gets your site', BLUE)
    wrap('"Reflow adapts Canva websites to different screen sizes by stacking elements vertically." Two rules cause almost every broken phone page:', L, R - L)
    wrap('OVERLAPPING elements shrink in mobile view — words placed over a photo come out tiny.', L, R - L, bullet='1')
    wrap('UNGROUPED elements can separate — a price that only looks attached to its picture drifts away from it.', L, R - L, bullet='2')

    head("Canva's five fixes — in Canva's words", GREEN)
    for t in [
        '"Select elements in your design and resize or crop them so their borders don\'t touch."',
        '"Replace large elements that span the full width with smaller ones that stack neatly."',
        '"Keep important elements inside the safe margin boundaries."',
        '"Use the mobile preview panel while editing." (Preview → Mobile.) "Treat it as an approximation, since the published site can vary by device and browser."',
        '"Group related elements, then lock the group so they stay together." (Select → floating toolbar → Group, then the lock.)',
    ]:
        wrap(t, L, R - L, bullet='•')

    head('Three passes on every page (mobile preview open)', AMBER)
    wrap('ORDER — read it top to bottom like a stranger: heading, photo, details, button. Wrong order = where things sit on the desktop page.', L, R - L, bullet='1')
    wrap('SIZE — text that suddenly went tiny is almost always overlapping something.', L, R - L, bullet='2')
    wrap('GAPS — things drifted apart (a price under the wrong product) were never grouped.', L, R - L, bullet='3')
    wrap('Write down what you find on each page BEFORE you fix anything.', L, R - L, font='Helvetica-Oblique')

    head('Publish, then test the real thing', PINK)
    wrap('Publish website → Site address → Settings → turn on Resize on mobile ("Automatically adjust your design for mobile screens") → Continue → Publish.', L, R - L)
    wrap('Open the LIVE address on a real phone, in its own browser — every page, the same three passes. Then a second phone, a different make, if you can.', L, R - L)
    wrap('Canva Free publishes up to 10 sections per page (you can design with 20). A website can have up to 45 pages.', L, R - L)

    # the eight checks, as tick boxes in a band
    y -= 4
    top = y + 6
    rows = [
        'Nothing overlaps — every element has its own space', 'Words are never on top of a photo',
        'Every pair that belongs together is grouped + locked', 'No single element spans the full width',
        'Text and buttons sit inside the safe margin', 'The button is big enough for a thumb',
        'Resize on mobile is on', 'Checked on a real phone — every page, top to bottom',
    ]
    bh = 18 + 4 * 17 + 10
    c.setFillColorRGB(*BAND)
    c.roundRect(L, top - bh, R - L, bh, 8, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 11.5)
    c.setFillColorRGB(*INK)
    c.drawString(L + 12, top - 16, 'The eight checks before you send the address to anyone')
    colw = (R - L - 24) / 2
    for i, t in enumerate(rows):
        cx = L + 12 + (i // 4) * colw
        cy = top - 36 - (i % 4) * 17
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(0.9)
        c.rect(cx, cy - 2, 9, 9, fill=0, stroke=1)
        c.setFont('Helvetica', 9.2)
        c.setFillColorRGB(*BODY)
        c.drawString(cx + 15, cy, t)

    c.setFont('Helvetica', 8)
    c.setFillColorRGB(*GREY)
    c.drawString(L, 0.6 * inch, "Sources: Canva Help Centre — My website looks different on mobile; Publish websites to a free domain; Designing websites (read 6 Nov 2026).")
    c.drawString(L, 0.46 * inch, 'Planning the whole build? The Canva Website Launch Kit — geniusjunkie.net/canva-website-launch-kit/')
    c.showPage()
    c.save()
    return path


if __name__ == '__main__':
    print('wrote', os.path.basename(card()))
