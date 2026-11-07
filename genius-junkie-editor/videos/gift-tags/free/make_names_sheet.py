#!/usr/bin/env python3
"""Gift Tag Names Sheet + Cutting Guide — the FREE rung.

Built NEW, never carved out of the Printable Gift Tag Kit.

Verified 2026-11-02 (Canva Help Centre, read that day):
  * "Create designs in bulk": "Each row creates one version of your design";
    Output "1 design with multiple pages" = a separate page per row; "For text,
    add a separate text box for each field"; "You can connect up to 150 data
    fields"; Canva Sheets up to 300 rows / 150 columns; data from a Canva Sheet,
    CSV or XLSX, a connected app, or a typed table; buttons "Match and fill
    fields", (•••) More options next to Create designs, "Create [n] designs".
    Plans: Pro, Teams, Business, Enterprise, Education, Nonprofit — not Free.
  * "Adding and removing guides": File → Rulers and guides → Add guides → Custom.
  * "Margins, bleed and crop marks": crop marks only in PDF Print exports,
    off by default.

Our layout (labelled as ours): 2 × 5 grid filling the page; Letter tags
4.25 × 2.2 in, A4 tags 105 × 59.4 mm; ~8 mm safe border; 5 cuts.

Output: gift-tag-names-sheet.csv  ·  gift-tag-cutting-guide.pdf (one page, Letter)
"""
import csv
import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))
INK, BODY, GREY = (0.133, 0.125, 0.122), (0.28, 0.30, 0.31), (0.557, 0.541, 0.525)
RULE, PINK, GREEN = (0.894, 0.878, 0.855), (0.914, 0.118, 0.549), (0.133, 0.773, 0.369)
CUT = (0.74, 0.72, 0.70)
W, H = letter


def write_csv():
    path = os.path.join(OUT, 'gift-tag-names-sheet.csv')
    rows = [
        ['Grandma', 'Grandpa', 'Mum', 'Dad', 'Leo', 'Ava', 'Aunt Rose', 'Uncle Joe', 'Mia', 'Noah'],
        ['Ella', 'Sam', 'Ruby', 'Max', 'Isla', 'Finn', 'Zoe', 'Jack', 'Lily', 'Oscar'],
        ['Grace', 'Theo', 'Maya', 'Ben', '', '', '', '', '', ''],
    ]
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow([f'Name {i}' for i in range(1, 11)])
        w.writerows(rows)
    return path


def guide():
    path = os.path.join(OUT, 'gift-tag-cutting-guide.pdf')
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle('Gift Tag Cutting Guide · Genius Junkie')
    c.setAuthor('Genius Junkie')
    L = 0.7 * inch
    y = H - 0.75 * inch
    c.setFont('Helvetica-Bold', 9); c.setFillColorRGB(*PINK)
    c.drawString(L, y, 'GENIUS JUNKIE · FREE · VERIFIED 2 NOV 2026')
    y -= 30
    c.setFont('Helvetica-Bold', 24); c.setFillColorRGB(*INK)
    c.drawString(L, y, 'Gift tags: 10 per sheet, 5 cuts')
    y -= 20
    c.setFont('Helvetica', 11); c.setFillColorRGB(*BODY)
    c.drawString(L, y, 'The build from the video on one page — so 30 names make three sheets, not thirty.')

    # ── the diagram: a sheet with the five numbered cuts ──
    sw = 2.75 * inch
    sh = sw * 11 / 8.5
    sx, sy = W - L - sw, H - 1.95 * inch - sh
    c.setFillColorRGB(1, 1, 1); c.setStrokeColorRGB(*GREY); c.setLineWidth(0.8)
    c.rect(sx, sy, sw, sh, fill=1, stroke=1)
    cw, ch = sw / 2, sh / 5
    c.setStrokeColorRGB(*PINK); c.setDash(3, 2); c.setLineWidth(0.5)
    for i in range(10):
        col, row = i % 2, i // 2
        x0, y0 = sx + col * cw, sy + sh - (row + 1) * ch
        c.rect(x0 + 0.11 * inch, y0 + 0.11 * inch, cw - 0.22 * inch, ch - 0.22 * inch, fill=0, stroke=1)
    c.setDash()
    c.setStrokeColorRGB(*INK); c.setLineWidth(1.6)
    c.line(sx + cw, sy - 8, sx + cw, sy + sh + 8)
    for r in range(1, 5):
        c.line(sx - 8, sy + r * ch, sx + sw + 8, sy + r * ch)
    c.setFont('Helvetica-Bold', 10)
    for k, (bx, by) in enumerate([(sx + cw, sy + sh + 16)] + [(sx - 18, sy + (5 - r) * ch) for r in range(1, 5)]):
        c.setFillColorRGB(*PINK); c.circle(bx, by, 8, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1); c.drawCentredString(bx, by - 3.5, str(k + 1))
    c.setFont('Helvetica', 8); c.setFillColorRGB(*GREY)
    c.drawCentredString(sx + sw / 2, sy - 22, 'pink dashes = keep everything inside (~8 mm)')
    c.drawCentredString(sx + sw / 2, sy - 33, 'outside edges = the paper\'s own edges: never cut')

    # ── left column: the steps ──
    x = L
    y = H - 1.6 * inch
    tw = sx - L - 0.35 * inch

    def head(t):
        nonlocal y
        y -= 6
        c.setFont('Helvetica-Bold', 12.5); c.setFillColorRGB(*INK); c.drawString(x, y, t); y -= 16

    def item(t, size=9.6):
        nonlocal y
        words, line = t.split(), ''
        c.setFont('Helvetica', size); c.setFillColorRGB(*BODY)
        first = True
        for w_ in words:
            trial = (line + ' ' + w_).strip()
            if c.stringWidth(trial, 'Helvetica', size) > tw - 12:
                c.drawString(x + (0 if first else 10), y, ('•  ' if first else '') + line); y -= size * 1.35; line = w_; first = False
            else:
                line = trial
        c.drawString(x + (0 if first else 10), y, ('•  ' if first else '') + line); y -= size * 1.5

    head('1  The sheet')
    item('Create a design the size of your paper: Letter (custom size 8.5 × 11 in) or search "A4".')
    item('File → Rulers and guides → Add guides → Custom: 2 columns, 5 rows. Ten tags, filling the page.')
    item('Each tag: 4.25 × 2.2 in on Letter, 105 × 59.4 mm on A4 (our layout).')
    head('2  One tag, then ten')
    item('Rectangle to the guides. Everything ~8 mm (1/3 in) inside — home printers lose 3–6 mm per side.')
    item('Art at one end, the hole at the other, then To and From. Group, duplicate, fill all ten cells.')
    item('Draw pale grey, very thin cut lines on the INSIDE guides only. Guides do not print.')
    head('3  Names — ten columns, not one')
    item('Bulk Create makes one page per row of your list. One "Name" column = one page per name = one sheet of card per tag.')
    item('Use the CSV: Name 1 … Name 10 across. Connect each to its own tag. Each row = one sheet. 30 names = 3 rows = 3 sheets.')
    item('Bulk Create: Pro, Teams, Business, Enterprise, Education, Nonprofit — not Canva Free. On Free, type the ten names and duplicate the page.')
    head('4  Print')
    item('Download → PDF Standard. Crop marks (PDF Print) only mark the page edge — your grey lines do the job.')
    item('Scale 100% / Actual size — never "Fit to page". Test on plain paper first, then card.')

    # ── bottom band: the five cuts in words ──
    by = 1.55 * inch
    c.setFillColorRGB(0.957, 0.949, 0.933)
    c.roundRect(L, by - 0.25 * inch, W - 2 * L, 0.95 * inch, 8, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 12); c.setFillColorRGB(*INK)
    c.drawString(L + 14, by + 0.42 * inch, 'The five cuts')
    c.setFont('Helvetica', 10); c.setFillColorRGB(*BODY)
    c.drawString(L + 14, by + 0.2 * inch, 'Cut 1: straight down the middle — two strips of five.   Cuts 2–5: across each strip on the four lines.')
    c.drawString(L + 14, by + 0.0 * inch, 'Punch the hole well clear of the edge, so the ribbon will not tear it out.')

    c.setFont('Helvetica', 8.5); c.setFillColorRGB(*GREY)
    c.drawString(L, 0.62 * inch, 'Sources: Canva Help Centre — Create designs in bulk; Adding and removing guides; Margins, bleed and crop marks (read 2 Nov 2026).')
    c.drawString(L, 0.48 * inch, 'Want the finished sheets? The Printable Gift Tag Kit: 36 designs, Letter + A4 — geniusjunkie.net/printable-gift-tag-kit/')
    c.showPage()
    c.save()
    return path


if __name__ == '__main__':
    for p in (write_csv(), guide()):
        print('wrote', os.path.basename(p))
