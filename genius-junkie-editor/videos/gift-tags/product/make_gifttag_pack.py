#!/usr/bin/env python3
"""Printable Gift Tag Kit — the £4.99 pack.

Print-ready sheets, no Canva needed: the build from the video, finished.

  * 24 Christmas designs (12 motifs × classic + kraft) and 12 all-year designs
  * every design = one sheet of 10 identical tags, 2 columns × 5 rows, edge to
    edge, no page margin — exactly the layout taught in the video
  * Letter (tags 4.25 × 2.2 in) AND A4 (tags 105 × 59.4 mm)
  * pale grey cut lines on the INSIDE guides only (5 cuts per sheet)
  * everything inside a 9 mm safe border per tag: clears the 3–6 mm a home
    printer cannot reach, and hides a wobbly cut
  * write-on To / From lines and a punch-here circle at the clear end

Output (this folder):
  gift-tags-christmas-letter.pdf   gift-tags-christmas-a4.pdf
  gift-tags-all-year-letter.pdf    gift-tags-all-year-a4.pdf
  gift-tags-READ-ME.pdf
"""
import math
import os

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

INK = (0.133, 0.125, 0.122)
GREY = (0.56, 0.54, 0.52)
CUT = (0.74, 0.72, 0.70)
WHITE = (1, 1, 1)
RED = (0.70, 0.15, 0.23)
GREEN = (0.12, 0.42, 0.31)
GOLD = (0.79, 0.64, 0.36)
KRAFT = (0.85, 0.73, 0.55)
SNOW = (0.62, 0.76, 0.86)
BLUSH, SKY, SAGE, BUTTER, LILAC = (0.95, 0.72, 0.78), (0.61, 0.76, 0.90), (0.66, 0.78, 0.71), (0.97, 0.86, 0.55), (0.78, 0.71, 0.89)
PINK = (0.914, 0.118, 0.549)

SAFE = 9 * mm      # content inset per tag
FRAME = 7 * mm     # decorative frame / kraft panel inset


# ───────────────────────────────────────────────────────────── motifs ──
# Each draws inside the square (x, y, s) — bottom-left origin.

def m_tree(c, x, y, s, p):
    c.setFillColorRGB(*p['a'])
    for k, (w, top, bot) in enumerate([(0.80, 0.70, 0.35), (0.64, 0.86, 0.52), (0.46, 0.98, 0.68)]):
        path = c.beginPath()
        path.moveTo(x + s * 0.5, y + s * top)
        path.lineTo(x + s * (0.5 + w / 2), y + s * bot)
        path.lineTo(x + s * (0.5 - w / 2), y + s * bot)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
    c.setFillColorRGB(0.48, 0.29, 0.16)
    c.rect(x + s * 0.44, y + s * 0.18, s * 0.12, s * 0.17, fill=1, stroke=0)
    c.setFillColorRGB(*p['b'])
    for bx, by in [(0.38, 0.45), (0.62, 0.58), (0.47, 0.72), (0.6, 0.42)]:
        c.circle(x + s * bx, y + s * by, s * 0.035, fill=1, stroke=0)


def star_path(c, cx, cy, r, points=5, inner=0.45, rot=90):
    path = c.beginPath()
    for i in range(points * 2):
        ang = math.radians(rot + i * 180 / points)
        rr = r if i % 2 == 0 else r * inner
        px, py = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
        (path.moveTo if i == 0 else path.lineTo)(px, py)
    path.close()
    return path


def m_star(c, x, y, s, p):
    c.setFillColorRGB(*GOLD)
    c.drawPath(star_path(c, x + s / 2, y + s / 2, s * 0.44), fill=1, stroke=0)


def leaf(c, cx, cy, l, w, ang, col):
    c.saveState()
    c.translate(cx, cy)
    c.rotate(ang)
    c.setFillColorRGB(*col)
    path = c.beginPath()
    path.moveTo(-l / 2, 0)
    path.curveTo(-l / 4, w, l / 4, w, l / 2, 0)
    path.curveTo(l / 4, -w, -l / 4, -w, -l / 2, 0)
    c.drawPath(path, fill=1, stroke=0)
    c.restoreState()


def m_holly(c, x, y, s, p):
    leaf(c, x + s * 0.33, y + s * 0.56, s * 0.56, s * 0.17, 25, p['a'])
    leaf(c, x + s * 0.67, y + s * 0.56, s * 0.56, s * 0.17, -25, p['a'])
    c.setFillColorRGB(*RED)
    for bx, by in [(0.44, 0.40), (0.56, 0.40), (0.50, 0.30)]:
        c.circle(x + s * bx, y + s * by, s * 0.075, fill=1, stroke=0)


def m_bauble(c, x, y, s, p):
    c.setFillColorRGB(*p['b'])
    c.circle(x + s / 2, y + s * 0.42, s * 0.34, fill=1, stroke=0)
    c.setFillColorRGB(*GOLD)
    c.rect(x + s * 0.42, y + s * 0.74, s * 0.16, s * 0.1, fill=1, stroke=0)
    c.setStrokeColorRGB(*GOLD)
    c.setLineWidth(max(0.6, s * 0.02))
    c.circle(x + s / 2, y + s * 0.89, s * 0.05, fill=0, stroke=1)
    c.setStrokeColorRGB(*WHITE)
    c.setLineWidth(max(0.8, s * 0.03))
    c.line(x + s * 0.2, y + s * 0.42, x + s * 0.8, y + s * 0.42)


def m_snowflake(c, x, y, s, p):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.42
    c.setStrokeColorRGB(*SNOW if p['name'] == 'classic' else WHITE)
    c.setLineWidth(max(1, s * 0.05))
    c.setLineCap(1)
    for k in range(6):
        a = math.radians(k * 60 + 90)
        ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
        c.line(cx, cy, ex, ey)
        for side in (-1, 1):
            b = a + side * math.radians(35)
            mx, my = cx + r * 0.62 * math.cos(a), cy + r * 0.62 * math.sin(a)
            c.line(mx, my, mx + r * 0.25 * math.cos(b), my + r * 0.25 * math.sin(b))


def m_candy(c, x, y, s, p):
    c.setLineCap(1)
    c.setLineWidth(s * 0.13)
    c.setStrokeColorRGB(*RED)
    path = c.beginPath()
    path.moveTo(x + s * 0.55, y + s * 0.1)
    path.lineTo(x + s * 0.55, y + s * 0.62)
    path.curveTo(x + s * 0.55, y + s * 0.92, x + s * 0.2, y + s * 0.92, x + s * 0.2, y + s * 0.66)
    c.drawPath(path, fill=0, stroke=1)
    c.setStrokeColorRGB(*WHITE)
    c.setLineWidth(s * 0.07)
    c.setLineCap(0)
    c.setDash(s * 0.05, s * 0.09)
    c.drawPath(path, fill=0, stroke=1)
    c.setDash()


def m_present(c, x, y, s, p):
    c.setFillColorRGB(*p['b'])
    c.rect(x + s * 0.16, y + s * 0.1, s * 0.68, s * 0.56, fill=1, stroke=0)
    c.setFillColorRGB(*p['a'])
    c.rect(x + s * 0.1, y + s * 0.56, s * 0.8, s * 0.16, fill=1, stroke=0)
    c.setFillColorRGB(*GOLD)
    c.rect(x + s * 0.45, y + s * 0.1, s * 0.1, s * 0.62, fill=1, stroke=0)
    leaf(c, x + s * 0.38, y + s * 0.8, s * 0.26, s * 0.09, 20, GOLD)
    leaf(c, x + s * 0.62, y + s * 0.8, s * 0.26, s * 0.09, -20, GOLD)


def m_wreath(c, x, y, s, p):
    cx, cy = x + s / 2, y + s / 2
    for k in range(14):
        a = k * 360 / 14
        rx, ry = cx + s * 0.32 * math.cos(math.radians(a)), cy + s * 0.32 * math.sin(math.radians(a))
        leaf(c, rx, ry, s * 0.2, s * 0.07, a + 70, p['a'])
    c.setFillColorRGB(*RED)
    leaf(c, cx - s * 0.08, cy - s * 0.36, s * 0.16, s * 0.07, 25, RED)
    leaf(c, cx + s * 0.08, cy - s * 0.36, s * 0.16, s * 0.07, -25, RED)


def m_bell(c, x, y, s, p):
    c.setFillColorRGB(*GOLD)
    path = c.beginPath()
    path.moveTo(x + s * 0.18, y + s * 0.24)
    path.curveTo(x + s * 0.3, y + s * 0.34, x + s * 0.26, y + s * 0.82, x + s * 0.5, y + s * 0.84)
    path.curveTo(x + s * 0.74, y + s * 0.82, x + s * 0.7, y + s * 0.34, x + s * 0.82, y + s * 0.24)
    path.close()
    c.drawPath(path, fill=1, stroke=0)
    c.circle(x + s * 0.5, y + s * 0.18, s * 0.07, fill=1, stroke=0)
    leaf(c, x + s * 0.4, y + s * 0.9, s * 0.2, s * 0.07, 20, p['a'])
    leaf(c, x + s * 0.6, y + s * 0.9, s * 0.2, s * 0.07, -20, p['a'])


def m_mitten(c, x, y, s, p):
    c.setFillColorRGB(*p['b'])
    c.roundRect(x + s * 0.28, y + s * 0.3, s * 0.42, s * 0.56, s * 0.2, fill=1, stroke=0)
    c.roundRect(x + s * 0.16, y + s * 0.42, s * 0.2, s * 0.26, s * 0.1, fill=1, stroke=0)
    c.setFillColorRGB(*WHITE)
    c.roundRect(x + s * 0.24, y + s * 0.12, s * 0.5, s * 0.2, s * 0.05, fill=1, stroke=0)


def m_baubles3(c, x, y, s, p):
    for bx, by, r, col in [(0.28, 0.42, 0.17, RED), (0.52, 0.32, 0.2, p['a']), (0.74, 0.48, 0.15, GOLD)]:
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(max(0.5, s * 0.012))
        c.line(x + s * bx, y + s * (by + r), x + s * bx, y + s * 0.96)
        c.setFillColorRGB(*col)
        c.circle(x + s * bx, y + s * by, s * r, fill=1, stroke=0)


def m_sprig(c, x, y, s, p):
    c.setStrokeColorRGB(0.48, 0.29, 0.16)
    c.setLineWidth(max(0.8, s * 0.025))
    c.line(x + s * 0.2, y + s * 0.15, x + s * 0.8, y + s * 0.85)
    for k in range(7):
        t = 0.2 + k * 0.1
        px, py = x + s * (0.2 + 0.6 * t / 0.9), y + s * (0.15 + 0.7 * t / 0.9)
        for side in (-1, 1):
            leaf(c, px + side * s * 0.06, py - side * s * 0.06, s * 0.16, s * 0.035, 45 + side * 45, p['a'])
    c.setFillColorRGB(*RED)
    c.circle(x + s * 0.74, y + s * 0.6, s * 0.05, fill=1, stroke=0)
    c.circle(x + s * 0.68, y + s * 0.52, s * 0.05, fill=1, stroke=0)


# all-year
def m_balloons(c, x, y, s, p):
    for bx, by, col in [(0.34, 0.6, BLUSH), (0.6, 0.66, SKY), (0.5, 0.48, BUTTER)]:
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(max(0.5, s * 0.012))
        c.line(x + s * bx, y + s * (by - 0.16), x + s * 0.48, y + s * 0.06)
        c.setFillColorRGB(*col)
        c.ellipse(x + s * (bx - 0.14), y + s * (by - 0.17), x + s * (bx + 0.14), y + s * (by + 0.17), fill=1, stroke=0)


def m_cake(c, x, y, s, p):
    c.setFillColorRGB(*BLUSH)
    c.rect(x + s * 0.18, y + s * 0.14, s * 0.64, s * 0.3, fill=1, stroke=0)
    c.setFillColorRGB(*BUTTER)
    c.rect(x + s * 0.26, y + s * 0.44, s * 0.48, s * 0.18, fill=1, stroke=0)
    c.setFillColorRGB(*SKY)
    for k in range(3):
        c.rect(x + s * (0.36 + k * 0.12), y + s * 0.62, s * 0.04, s * 0.16, fill=1, stroke=0)
    c.setFillColorRGB(*GOLD)
    for k in range(3):
        c.circle(x + s * (0.38 + k * 0.12), y + s * 0.82, s * 0.03, fill=1, stroke=0)


def heart_path(c, cx, cy, r):
    path = c.beginPath()
    path.moveTo(cx, cy - r * 0.9)
    path.curveTo(cx - r * 1.3, cy - r * 0.1, cx - r * 0.7, cy + r * 1.0, cx, cy + r * 0.4)
    path.curveTo(cx + r * 0.7, cy + r * 1.0, cx + r * 1.3, cy - r * 0.1, cx, cy - r * 0.9)
    return path


def m_heart(c, x, y, s, p):
    c.setFillColorRGB(*BLUSH)
    c.drawPath(heart_path(c, x + s / 2, y + s * 0.5, s * 0.4), fill=1, stroke=0)


def m_hearts(c, x, y, s, p):
    for hx, hy, r, col in [(0.35, 0.58, 0.2, BLUSH), (0.64, 0.42, 0.16, PINK), (0.38, 0.28, 0.1, LILAC)]:
        c.setFillColorRGB(*col)
        c.drawPath(heart_path(c, x + s * hx, y + s * hy, s * r), fill=1, stroke=0)


def m_daisy(c, x, y, s, p):
    cx, cy = x + s / 2, y + s / 2
    for k in range(10):
        a = k * 36
        leaf(c, cx + s * 0.2 * math.cos(math.radians(a)), cy + s * 0.2 * math.sin(math.radians(a)), s * 0.32, s * 0.08, a, BLUSH if k % 2 else LILAC)
    c.setFillColorRGB(*BUTTER)
    c.circle(cx, cy, s * 0.11, fill=1, stroke=0)


RULE_LIGHT = (0.86, 0.84, 0.80)


def m_leaf(c, x, y, s, p):
    leaf(c, x + s / 2, y + s / 2, s * 0.8, s * 0.26, 40, SAGE)
    c.setStrokeColorRGB(0.44, 0.56, 0.47)
    c.setLineWidth(max(0.6, s * 0.02))
    c.line(x + s * 0.2, y + s * 0.24, x + s * 0.8, y + s * 0.76)


def m_confetti(c, x, y, s, p):
    import random
    rnd = random.Random(7)
    for k in range(22):
        col = [BLUSH, SKY, BUTTER, SAGE, LILAC][k % 5]
        c.setFillColorRGB(*col)
        px, py = x + s * rnd.uniform(0.08, 0.92), y + s * rnd.uniform(0.08, 0.92)
        if k % 2:
            c.circle(px, py, s * 0.045, fill=1, stroke=0)
        else:
            c.rect(px, py, s * 0.07, s * 0.035, fill=1, stroke=0)


def m_bow(c, x, y, s, p):
    leaf(c, x + s * 0.3, y + s * 0.58, s * 0.42, s * 0.16, 15, LILAC)
    leaf(c, x + s * 0.7, y + s * 0.58, s * 0.42, s * 0.16, -15, LILAC)
    leaf(c, x + s * 0.38, y + s * 0.32, s * 0.36, s * 0.07, 70, LILAC)
    leaf(c, x + s * 0.62, y + s * 0.32, s * 0.36, s * 0.07, -70, LILAC)
    c.setFillColorRGB(*PINK)
    c.circle(x + s * 0.5, y + s * 0.56, s * 0.08, fill=1, stroke=0)


def m_moon(c, x, y, s, p):
    c.setFillColorRGB(*BUTTER)
    c.circle(x + s * 0.44, y + s * 0.5, s * 0.32, fill=1, stroke=0)
    c.setFillColorRGB(*WHITE)
    c.circle(x + s * 0.58, y + s * 0.6, s * 0.28, fill=1, stroke=0)
    c.setFillColorRGB(*GOLD)
    for sx, sy, r in [(0.78, 0.3, 0.07), (0.84, 0.72, 0.05), (0.62, 0.16, 0.04)]:
        c.drawPath(star_path(c, x + s * sx, y + s * sy, s * r), fill=1, stroke=0)


def m_sun(c, x, y, s, p):
    cx, cy = x + s / 2, y + s / 2
    c.setStrokeColorRGB(*BUTTER)
    c.setLineWidth(max(1, s * 0.05))
    c.setLineCap(1)
    for k in range(12):
        a = math.radians(k * 30)
        c.line(cx + s * 0.3 * math.cos(a), cy + s * 0.3 * math.sin(a), cx + s * 0.44 * math.cos(a), cy + s * 0.44 * math.sin(a))
    c.setFillColorRGB(*BUTTER)
    c.circle(cx, cy, s * 0.22, fill=1, stroke=0)


def m_rainbow(c, x, y, s, p):
    c.setLineCap(0)
    for k, col in enumerate([BLUSH, BUTTER, SAGE, SKY]):
        c.setStrokeColorRGB(*col)
        c.setLineWidth(s * 0.08)
        r = s * (0.4 - k * 0.08)
        c.arc(x + s / 2 - r, y + s * 0.25 - r, x + s / 2 + r, y + s * 0.25 + r, 0, 180)


MOTIFS_XMAS = [
    ('Tree', m_tree), ('Star', m_star), ('Holly', m_holly), ('Bauble', m_bauble), ('Snowflake', m_snowflake),
    ('Candy cane', m_candy), ('Present', m_present), ('Wreath', m_wreath), ('Bell', m_bell), ('Mitten', m_mitten),
    ('Three baubles', m_baubles3), ('Pine sprig', m_sprig),
]
MOTIFS_YEAR = [
    ('Balloons', m_balloons), ('Cake', m_cake), ('Heart', m_heart), ('Hearts', m_hearts), ('Daisy', m_daisy),
    ('Leaf', m_leaf), ('Confetti', m_confetti), ('Bow', m_bow), ('Moon and stars', m_moon), ('Sun', m_sun),
    ('Rainbow', m_rainbow), ('Plain', None),
]
CLASSIC = {'name': 'classic', 'a': GREEN, 'b': RED, 'panel': None, 'frame': RED}
KRAFT_P = {'name': 'kraft', 'a': GREEN, 'b': RED, 'panel': KRAFT, 'frame': None}
YEAR_P = {'name': 'year', 'a': SAGE, 'b': BLUSH, 'panel': None, 'frame': LILAC}


# ──────────────────────────────────────────────────────────────── tag ──
def tag(c, x, y, cw, ch, motif, pal):
    """One tag in the cell whose bottom-left is (x, y)."""
    if pal['panel']:
        c.setFillColorRGB(*pal['panel'])
        c.roundRect(x + FRAME, y + FRAME, cw - 2 * FRAME, ch - 2 * FRAME, 3 * mm, fill=1, stroke=0)
    if pal['frame']:
        c.setStrokeColorRGB(*pal['frame'])
        c.setLineWidth(0.9)
        c.roundRect(x + FRAME, y + FRAME, cw - 2 * FRAME, ch - 2 * FRAME, 3 * mm, fill=0, stroke=1)
    inner_h = ch - 2 * SAFE
    ms = inner_h
    tx = x + SAFE
    if motif:
        motif(c, x + SAFE, y + SAFE, ms, pal)
        tx = x + SAFE + ms + 3 * mm
    # punch-here circle at the clear end
    hr = 2.6 * mm
    hx, hy = x + cw - SAFE - hr, y + ch / 2
    c.setStrokeColorRGB(*GREY)
    c.setLineWidth(0.6)
    c.setDash(1.2, 1.4)
    c.circle(hx, hy, hr, fill=0, stroke=1)
    c.setDash()
    # To / From write-on lines
    tw = (hx - hr - 4 * mm) - tx
    c.setFillColorRGB(*INK)
    lab = max(7, min(10, ch * 0.075))
    for k, word in enumerate(['To', 'From']):
        ly = y + ch * (0.6 if k == 0 else 0.3)
        c.setFont('Times-Italic', lab)
        c.drawString(tx, ly, word)
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(0.5)
        c.line(tx + lab * (1.4 if k == 0 else 2.6), ly - 1, tx + tw, ly - 1)


def sheet(c, W, H, motif, pal):
    cw, ch = W / 2, H / 5
    for i in range(10):
        col, row = i % 2, i // 2
        tag(c, col * cw, H - (row + 1) * ch, cw, ch, motif, pal)
    # cut lines — inside guides only, pale and thin
    c.setStrokeColorRGB(*CUT)
    c.setLineWidth(0.4)
    c.line(cw, 0, cw, H)
    for r in range(1, 5):
        c.line(0, r * ch, W, r * ch)


def build(name, size, designs):
    path = os.path.join(OUT, name)
    W, H = size
    c = pdfcanvas.Canvas(path, pagesize=size)
    c.setTitle(name.replace('.pdf', '').replace('-', ' ').title() + ' · Genius Junkie')
    c.setAuthor('Genius Junkie')
    for _, motif, pal in designs:
        sheet(c, W, H, motif, pal)
        c.showPage()
    c.save()
    return path


XMAS = [(n, f, CLASSIC) for n, f in MOTIFS_XMAS] + [(n + ' · kraft', f, KRAFT_P) for n, f in MOTIFS_XMAS]
YEAR = [(n, f, YEAR_P) for n, f in MOTIFS_YEAR]


def readme():
    path = os.path.join(OUT, 'gift-tags-READ-ME.pdf')
    W, H = letter
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle('Printable Gift Tag Kit · Read me · Genius Junkie')
    x, y = 0.8 * 72, H - 0.9 * 72

    def line(t, size=11, font='Helvetica', col=INK, gap=1.45):
        nonlocal y
        c.setFont(font, size)
        c.setFillColorRGB(*col)
        c.drawString(x, y, t)
        y -= size * gap

    line('GENIUS JUNKIE · PRINTABLE GIFT TAG KIT', 9, 'Helvetica-Bold', PINK)
    y -= 20
    line('Read me first', 26, 'Helvetica-Bold')
    y -= 6
    line('What is in the kit', 14, 'Helvetica-Bold')
    for t in [
        'gift-tags-christmas-letter.pdf / -a4.pdf — 24 Christmas designs, one design per sheet.',
        'gift-tags-all-year-letter.pdf / -a4.pdf — 12 designs for birthdays, thank-yous and anything.',
        'Every sheet: 10 identical tags, 2 across × 5 down, filling the page edge to edge.',
        'Letter tags are 4.25 × 2.2 in. A4 tags are 105 × 59.4 mm.',
    ]:
        line('•  ' + t, 10.5)
    y -= 8
    line('Print', 14, 'Helvetica-Bold')
    for t in [
        'Open the PDF for YOUR paper: Letter in the US, A4 almost everywhere else.',
        'Print the page you want only (e.g. "Pages: 3").',
        'Scale: 100% / Actual size. NOT "Fit to page" — that shrinks every tag.',
        'Print one test on plain paper first. Hold it against your card and check.',
        'Card: check the thickest paper your printer takes in its manual.',
    ]:
        line('•  ' + t, 10.5)
    y -= 8
    line('Cut — five cuts, ten tags', 14, 'Helvetica-Bold')
    for t in [
        '1. The long cut straight down the middle of the page, on the pale line.',
        '2–5. Take each strip of five and cut across on the four lines.',
        'The outside edges are the paper\'s own edges — you never cut them.',
        'Every tag keeps 9 mm of plain border, so a wobbly cut does not show.',
        'Punch the hole on the dotted circle — it sits clear of the edge so ribbon will not tear it out.',
    ]:
        line('•  ' + t, 10.5)
    y -= 8
    line('The designs', 14, 'Helvetica-Bold')
    for k in range(0, 24, 4):
        line('   ' + '   ·   '.join(f'{k + j + 1}. {XMAS[k + j][0]}' for j in range(4)), 9.5, col=GREY)
    line('   All-year: ' + ', '.join(f'{i + 1}. {n}' for i, (n, _, _) in enumerate(YEAR[:6])), 9.5, col=GREY)
    line('   ' + ', '.join(f'{i + 7}. {n}' for i, (n, _, _) in enumerate(YEAR[6:])), 9.5, col=GREY)
    y -= 8
    line('Want names printed on? Use the free Gift Tag Names Sheet with Canva Bulk Create', 10.5)
    line('(Pro / Teams / Business / Enterprise / Education / Nonprofit) — or just write them. People notice handwriting.', 10.5)
    y -= 10
    line('Use for your own gifts and gifts you make for others. The PDFs themselves are not for resale.', 9, col=GREY)
    line('geniusjunkie.net', 9, 'Helvetica-Bold', PINK)
    c.showPage()
    c.save()
    return path


if __name__ == '__main__':
    out = [
        build('gift-tags-christmas-letter.pdf', letter, XMAS),
        build('gift-tags-christmas-a4.pdf', A4, XMAS),
        build('gift-tags-all-year-letter.pdf', letter, YEAR),
        build('gift-tags-all-year-a4.pdf', A4, YEAR),
        readme(),
    ]
    for p in out:
        print('wrote', os.path.basename(p))
