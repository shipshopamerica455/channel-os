#!/usr/bin/env python3
"""Genius Junkie — sponsor media kit.

Every number here came out of YouTube Analytics on 12 Aug 2026 and is stated
as measured. The audience is 91% South & Southeast Asia; the kit leads with
that rather than burying it, because for the right sponsor it is the pitch.

    python3 make_media_kit.py            → genius-junkie-media-kit.pdf

Refresh the numbers first with:
    node ../../remotion-shorts/gj-slate-research.mjs --days 7
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(OUT, '..', '..', 'genius-junkie-shorts', 'media', 'library',
                    'logos', 'genius-junkie-logo.jpg')

INK = (0.059, 0.090, 0.165)     # #0f172a
PINK = (0.914, 0.118, 0.549)    # #e91e8c
YELLOW = (1.0, 0.867, 0.0)      # #ffdd00
PAPER = (1, 1, 1)
GREY = (0.42, 0.45, 0.50)
MIST = (0.94, 0.95, 0.97)
W, H = A4
M = 18 * mm

# ---- measured 12 Aug 2026 -----------------------------------------------
SUBS = '8,710'
LIFETIME = '518,195'
VIDEOS = '347'
MO_VIEWS = '43,000'
MO_MINS = '52,000'
MO_SUBS = '~137'
GEO = [('India', 62), ('Philippines', 16), ('Pakistan', 13),
       ('United States', 5), ('Indonesia / other', 4)]
AGE = [('25–34', 41), ('18–24', 31), ('35–44', 18), ('45+', 10)]
GENDER = [('Male', 61), ('Female', 39)]
DEVICE = [('Mobile', 75), ('Desktop', 21), ('Tablet / TV', 4)]
TOP = [
    ('Restaurant Menu in Canva', '4,700'),
    ('Digital Art with the Draw Tool', '3,800'),
    ('Product Labels in Canva', '2,900'),
    ('Book Covers for KDP', '2,800'),
    ('Digital Magazines in Canva', '2,750'),
    ('Professional Reports in Canva', '2,600'),
]
RATES = [
    ('Sponsored link insertion',
     'Description link above the fold + pinned comment on an existing evergreen tutorial.',
     '$150 / 6 months (one video)\n$350 / 12 months (two videos)'),
    ('Integrated segment',
     '60–90 seconds inside an upcoming tutorial, scripted around a real use case.',
     '$300'),
    ('Dedicated video',
     'A full tutorial built around a search query your product answers — not a branded review.',
     '$700'),
]


def bar(c, x, y, w, h, pct, col=PINK, track=MIST):
    c.setFillColorRGB(*track)
    c.roundRect(x, y, w, h, h / 2, stroke=0, fill=1)
    c.setFillColorRGB(*col)
    if pct > 0:
        c.roundRect(x, y, max(h, w * pct / 100.0), h, h / 2, stroke=0, fill=1)


def heading(c, y, text, size=15):
    c.setFillColorRGB(*INK)
    c.setFont('Helvetica-Bold', size)
    c.drawString(M, y, text)
    c.setFillColorRGB(*PINK)
    c.rect(M, y - 9, 34, 3, stroke=0, fill=1)
    return y - 30


def body(c, y, lines, size=10, lead=15, col=(0.25, 0.28, 0.33), indent=0):
    c.setFont('Helvetica', size)
    c.setFillColorRGB(*col)
    for ln in lines:
        c.drawString(M + indent, y, ln)
        y -= lead
    return y


def footer(c, page):
    c.setFillColorRGB(0.62, 0.65, 0.70)
    c.setFont('Helvetica', 8)
    c.drawString(M, 12 * mm, 'Genius Junkie · youtube.com/@geniusjunkieyt · geniusjunkie.net')
    c.drawRightString(W - M, 12 * mm, f'{page}  ·  figures measured 12 Aug 2026')


# ------------------------------------------------------------------ page 1
def cover(c):
    c.setFillColorRGB(*INK)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColorRGB(*PINK)
    c.rect(0, H - 8, W, 8, stroke=0, fill=1)

    y = H - 52 * mm
    if os.path.exists(LOGO):
        try:
            c.drawImage(ImageReader(LOGO), M, y + 6, width=46, height=46, mask='auto')
        except Exception:
            pass
    c.setFillColorRGB(1, 1, 1)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(M + 60, y + 30, 'GENIUS JUNKIE')
    c.setFillColorRGB(0.65, 0.70, 0.78)
    c.setFont('Helvetica', 10)
    c.drawString(M + 60, y + 14, 'Canva, KDP and design tutorials  ·  @geniusjunkieyt')

    c.setFillColorRGB(1, 1, 1)
    c.setFont('Helvetica-Bold', 40)
    c.drawString(M, y - 46, 'Media kit')
    c.setFillColorRGB(*YELLOW)
    c.setFont('Helvetica-Bold', 40)
    c.drawString(M, y - 92, 'for sponsors')

    c.setFillColorRGB(0.72, 0.77, 0.84)
    c.setFont('Helvetica', 12)
    ty = y - 130
    for ln in [
        'A search-led tutorial channel: 347 videos, three quarters of the traffic',
        'arriving from YouTube search rather than the feed. Placements keep working',
        'for years because the videos keep ranking.',
    ]:
        c.drawString(M, ty, ln)
        ty -= 18

    # headline numbers
    cards = [(SUBS, 'subscribers'), (MO_VIEWS, 'views / month'),
             (MO_MINS, 'watch-minutes / month'), ('76%', 'from YouTube search')]
    cw = (W - 2 * M - 3 * 10) / 4
    cy = ty - 70
    for i, (n, lab) in enumerate(cards):
        x = M + i * (cw + 10)
        c.setFillColorRGB(0.10, 0.15, 0.24)
        c.roundRect(x, cy, cw, 62, 8, stroke=0, fill=1)
        c.setFillColorRGB(*YELLOW)
        c.setFont('Helvetica-Bold', 19)
        c.drawCentredString(x + cw / 2, cy + 34, n)
        c.setFillColorRGB(0.65, 0.70, 0.78)
        c.setFont('Helvetica', 8)
        c.drawCentredString(x + cw / 2, cy + 18, lab)

    # the pitch
    py = cy - 42
    c.setFillColorRGB(*PINK)
    c.setLineWidth(2)
    c.setStrokeColorRGB(*PINK)
    c.roundRect(M, py - 74, W - 2 * M, 78, 10, stroke=1, fill=0)
    c.setFillColorRGB(*PINK)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(M + 16, py - 20, 'Where this audience is')
    c.setFillColorRGB(0.82, 0.86, 0.91)
    c.setFont('Helvetica', 10)
    c.drawString(M + 16, py - 38, '91% of viewers are in South and Southeast Asia — India, the Philippines and')
    c.drawString(M + 16, py - 53, 'Pakistan. If that is your growth market, this channel is priced well below what')
    c.drawString(M + 16, py - 68, 'a US-weighted channel of the same size would cost you.')

    # formats at a glance
    fy = py - 132
    c.setFillColorRGB(0.65, 0.70, 0.78)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(M, fy + 26, 'THREE WAYS TO WORK TOGETHER')
    fw = (W - 2 * M - 2 * 10) / 3
    for i, (t, sub) in enumerate([
        ('Link insertion', 'above the fold + pinned'),
        ('Integrated segment', '60–90s in a new tutorial'),
        ('Dedicated video', 'built around a search query'),
    ]):
        x = M + i * (fw + 10)
        c.setStrokeColorRGB(0.20, 0.26, 0.36)
        c.setLineWidth(1.2)
        c.roundRect(x, fy - 46, fw, 48, 8, stroke=1, fill=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(x + 12, fy - 18, t)
        c.setFillColorRGB(0.55, 0.61, 0.70)
        c.setFont('Helvetica', 8.5)
        c.drawString(x + 12, fy - 33, sub)
    c.setFillColorRGB(*YELLOW)
    c.setFont('Helvetica', 9.5)
    c.drawString(M, fy - 70, 'Rates and audience breakdown inside  →')

    c.setFillColorRGB(0.45, 0.50, 0.58)
    c.setFont('Helvetica', 8.5)
    c.drawString(M, 20 * mm, 'Every figure in this kit is taken from YouTube Analytics and stated as measured.')
    c.showPage()


# ------------------------------------------------------------------ page 2
def audience(c):
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - M - 10

    y = heading(c, y, 'The audience')
    y = body(c, y, ['Last 28 days. Advertising was switched off on 4 August, so these are organic.'],
             size=9.5, col=GREY)
    y -= 8

    colw = (W - 2 * M - 14) / 2
    top = y

    # geography
    c.setFillColorRGB(*INK)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(M, y, 'Country')
    y -= 18
    for name, pct in GEO:
        c.setFillColorRGB(0.25, 0.28, 0.33)
        c.setFont('Helvetica', 9.5)
        c.drawString(M, y, name)
        c.setFillColorRGB(*INK)
        c.setFont('Helvetica-Bold', 9.5)
        c.drawRightString(M + colw, y, f'{pct}%')
        bar(c, M, y - 11, colw, 5, pct)
        y -= 26

    # age / gender / device
    x2 = M + colw + 14
    y2 = top
    for title, data in [('Age', AGE), ('Gender', GENDER), ('Device', DEVICE)]:
        c.setFillColorRGB(*INK)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(x2, y2, title)
        y2 -= 18
        for name, pct in data:
            c.setFillColorRGB(0.25, 0.28, 0.33)
            c.setFont('Helvetica', 9.5)
            c.drawString(x2, y2, name)
            c.setFillColorRGB(*INK)
            c.setFont('Helvetica-Bold', 9.5)
            c.drawRightString(x2 + colw, y2, f'{pct}%')
            bar(c, x2, y2 - 11, colw, 5, pct, col=(0.15, 0.25, 0.45))
            y2 -= 22
        y2 -= 10

    y = min(y, y2) - 14
    y = heading(c, y, 'What people watch')
    y = body(c, y, ['Evergreen tutorials, ranked by organic views per month. A placement on any of',
                    'these keeps delivering for as long as the video ranks — which so far is years.'],
             size=9.5, col=GREY)
    y -= 6

    c.setFillColorRGB(*GREY)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(M, y, 'VIDEO')
    c.drawRightString(W - M, y, 'VIEWS / MONTH')
    y -= 6
    c.setStrokeColorRGB(0.85, 0.87, 0.90)
    c.setLineWidth(0.8)
    c.line(M, y, W - M, y)
    y -= 16
    for name, v in TOP:
        c.setFillColorRGB(0.15, 0.18, 0.23)
        c.setFont('Helvetica', 10)
        c.drawString(M, y, name)
        c.setFillColorRGB(*PINK)
        c.setFont('Helvetica-Bold', 10)
        c.drawRightString(W - M, y, v)
        y -= 20

    y -= 10
    c.setFillColorRGB(*MIST)
    c.roundRect(M, y - 58, W - 2 * M, 62, 8, stroke=0, fill=1)
    c.setFillColorRGB(*INK)
    c.setFont('Helvetica-Bold', 10.5)
    c.drawString(M + 14, y - 18, 'Why search traffic is worth more to you than feed traffic')
    c.setFillColorRGB(0.25, 0.28, 0.33)
    c.setFont('Helvetica', 9.5)
    c.drawString(M + 14, y - 34, 'A feed view is a person who was scrolling. A search view is a person who typed the')
    c.drawString(M + 14, y - 48, 'problem your product solves. 76% of views here are the second kind.')
    footer(c, 'Page 2 of 3')
    c.showPage()


# ------------------------------------------------------------------ page 3
def rates(c):
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - M - 10

    y = heading(c, y, 'Working together')
    y = body(c, y, ['Three formats. All rates in USD, invoiced on delivery.'], size=9.5, col=GREY)
    y -= 10

    for title, desc, price in RATES:
        plines = price.split('\n')
        h = 62 + 16 * len(plines)
        c.setStrokeColorRGB(0.87, 0.89, 0.92)
        c.setLineWidth(1.2)
        c.roundRect(M, y - h, W - 2 * M, h, 9, stroke=1, fill=0)
        c.setFillColorRGB(*INK)
        c.setFont('Helvetica-Bold', 12.5)
        c.drawString(M + 16, y - 24, title)
        # price sits on its own lines under the title, so it can never collide
        c.setFillColorRGB(*PINK)
        c.setFont('Helvetica-Bold', 12)
        py = y - 24
        for ln in plines:
            c.drawRightString(W - M - 16, py, ln)
            py -= 16
        c.setFillColorRGB(0.35, 0.38, 0.43)
        c.setFont('Helvetica', 9.5)
        c.drawString(M + 16, y - h + 18, desc)
        y -= h + 14

    y -= 20
    y = heading(c, y, 'How I work')
    y = body(c, y, [
        'Every placement is disclosed. I only take products I would use in a tutorial anyway.',
        '',
        'For a dedicated video I will push to build it around a search query your product',
        'answers rather than around the brand — "how to remove a background for free"',
        'rather than "[product] review". Same cost to you, and it keeps earning traffic',
        'for years instead of dying in a week.',
        '',
        'Happy to add an affiliate arrangement alongside the flat fee.',
    ], size=10, lead=15)

    y -= 18
    c.setFillColorRGB(*INK)
    c.roundRect(M, y - 66, W - 2 * M, 70, 9, stroke=0, fill=1)
    c.setFillColorRGB(*YELLOW)
    c.setFont('Helvetica-Bold', 13)
    c.drawString(M + 16, y - 24, 'Get in touch')
    c.setFillColorRGB(1, 1, 1)
    c.setFont('Helvetica', 10)
    c.drawString(M + 16, y - 44, 'youtube.com/@geniusjunkieyt        geniusjunkie.net')
    c.setFillColorRGB(0.65, 0.70, 0.78)
    c.setFont('Helvetica', 9)
    c.drawString(M + 16, y - 58, 'Full analytics screenshots available on request.')
    footer(c, 'Page 3 of 3')
    c.showPage()


if __name__ == '__main__':
    path = os.path.join(OUT, 'genius-junkie-media-kit.pdf')
    c = pdfcanvas.Canvas(path, pagesize=A4)
    c.setTitle('Genius Junkie — Media Kit')
    cover(c)
    audience(c)
    rates(c)
    c.save()
    print(f'wrote {os.path.basename(path)}')
