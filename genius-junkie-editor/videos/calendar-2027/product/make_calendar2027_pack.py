#!/usr/bin/env python3
"""2027 Calendar Kit — the reference set that ships with the editable Canva
calendar.

Every grid in here is COMPUTED from Python's calendar module, not typed. That is
the entire point of the product: the thing people get wrong is the arithmetic.

Outputs (all US Letter):
  calendar-2027-grid-reference.pdf   all twelve months, printed correctly
  calendar-2027-why-it-shifts.pdf    the 52-weeks-and-a-day explainer
  calendar-2027-print-checklist.pdf  PDF Print vs Standard, bleed on/off
  calendar-2027-listing-guide.pdf    selling the set, and the timing
  calendar-2027-READ-ME.pdf          how to use the template, and the licence
"""
import calendar
import datetime as dt
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))
YEAR = 2027

PAPER = (0.984, 0.980, 0.973)
INK = (0.078, 0.094, 0.114)
TEAL = (0.184, 0.490, 0.471)
AMBER = (0.851, 0.604, 0.169)
GREY = (0.659, 0.690, 0.682)
PINK = (0.914, 0.118, 0.549)
W, H = letter
M = 0.7 * inch

calendar.setfirstweekday(calendar.MONDAY)   # the kit is Monday-start


def page(c, title, kicker=None):
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - M
    if kicker:
        c.setFillColorRGB(*TEAL)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(M, y + 4, kicker.upper())
        y -= 6
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, y - 20, title)
    c.setFillColorRGB(*TEAL)
    c.rect(M, y - 34, 62, 3, stroke=0, fill=1)
    return y - 58


def footer(c):
    c.setFillColorRGB(0.62, 0.64, 0.63)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(W / 2, M - 16, "Genius Junkie · geniusjunkie.net")


def body(c, y, lines, size=10.5, lead=15, indent=0, col=(0.28, 0.30, 0.31)):
    c.setFont("Helvetica", size)
    c.setFillColorRGB(*col)
    for ln in lines:
        c.drawString(M + indent, y, ln)
        y -= lead
    return y


def heading(c, y, text, size=12.5):
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", size)
    c.drawString(M, y, text)
    return y - 18


def callout(c, y, title, lines, col=PINK):
    h = 34 + 13 * len(lines)
    c.setStrokeColorRGB(*col)
    c.setLineWidth(2)
    c.roundRect(M, y - h, W - 2 * M, h + 6, 9, stroke=1, fill=0)
    c.setFillColorRGB(*col)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M + 14, y - 16, title)
    c.setFillColorRGB(0.28, 0.30, 0.31)
    c.setFont("Helvetica", 9.5)
    yy = y - 33
    for ln in lines:
        c.drawString(M + 14, yy, ln)
        yy -= 13
    return y - h - 18


def checkbox_list(c, y, items, gap=20):
    for q in items:
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(1)
        c.rect(M, y - 3, 11, 11, stroke=1, fill=0)
        c.setFillColorRGB(0.28, 0.30, 0.31)
        c.setFont("Helvetica", 10)
        c.drawString(M + 20, y, q)
        y -= gap
    return y


def mini_month(c, x, y, month, cw=21, ch=12.5, highlight=False):
    """One month grid, computed. Returns the height used."""
    name = calendar.month_name[month]
    c.setFillColorRGB(*(PINK if highlight else INK))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y, f"{name} {YEAR}")
    yy = y - 15
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColorRGB(*TEAL)
    for i, d in enumerate(['M', 'T', 'W', 'T', 'F', 'S', 'S']):
        c.drawCentredString(x + i * cw + cw / 2, yy, d)
    yy -= 12
    c.setFont("Helvetica", 8.5)
    for week in calendar.monthcalendar(YEAR, month):
        for i, day in enumerate(week):
            if day:
                # weekends a touch lighter, like the template
                c.setFillColorRGB(*(GREY if i >= 5 else (0.28, 0.30, 0.31)))
                c.drawCentredString(x + i * cw + cw / 2, yy, str(day))
        yy -= ch
    if highlight:
        rows = len(calendar.monthcalendar(YEAR, month))
        c.setStrokeColorRGB(*PINK)
        c.setLineWidth(1.4)
        c.roundRect(x - 5, yy + ch - 4, cw * 7 + 10, rows * ch + 20, 4, stroke=1, fill=0)
    return y - yy


# --------------------------------------------------- grid reference --------
def grid_reference(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, f"Every {YEAR} month, correct", "2027 calendar kit")
    y = body(c, y, [
        "Monday-start. Check your grid against this one before you export anything —",
        "and check February first (see the box at the bottom of the page).",
    ], size=10, lead=14)
    y -= 10

    # 3 columns x 4 rows of mini months
    col_w = (W - 2 * M) / 3
    top = y
    for m in range(1, 13):
        col, row = (m - 1) % 3, (m - 1) // 3
        mini_month(c, M + col * col_w, top - row * 106, m, highlight=(m == 2))
    y = top - 4 * 106 - 6

    y = callout(c, y, "The one-second check — February only works this year", [
        "February 2027 starts on a MONDAY and has 28 days — exactly four weeks. On a",
        "Monday-start grid it is a perfect 4 x 7 block, no blank squares at either end.",
        "It is the only month that does. A gap anywhere means the whole grid is wrong.",
    ], col=TEAL)

    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------ why it shifts ------
def why_it_shifts(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Why last year's calendar is wrong", "2027 calendar kit")
    y = body(c, y, [
        "One idea, and you will never make this mistake again.",
    ])
    y -= 16

    y = heading(c, y, "A year does not divide into weeks")
    y = body(c, y, [
        "365 days.  52 weeks is 364.  So a common year is 52 weeks and ONE day left over.",
        "That leftover day pushes every date one weekday later the following year.",
        "",
        "A leap year is 366 days — 52 weeks and TWO days — so it pushes you two.",
    ], size=10.5, lead=15)
    y -= 12

    rows = [
        ("1 January 2026", dt.date(2026, 1, 1), "2026 is not a leap year"),
        ("1 January 2027", dt.date(2027, 1, 1), "→ one day later than 2026"),
        ("1 January 2028", dt.date(2028, 1, 1), "2028 IS a leap year"),
        ("1 January 2029", dt.date(2029, 1, 1), "→ TWO days later than 2028"),
    ]
    for lab, d, note in rows:
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M + 8, y, lab)
        c.setFillColorRGB(*PINK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M + 150, y, d.strftime('%A'))
        c.setFillColorRGB(0.45, 0.47, 0.48)
        c.setFont("Helvetica-Oblique", 9.5)
        c.drawString(M + 250, y, note)
        y -= 19
    y -= 12

    y = callout(c, y, "What that does to a reused file", [
        "Take a 2026 calendar, change the year in the title, and you have not made a 2027",
        "calendar. You have made a 2026 calendar with the wrong year printed on it.",
        "",
        "Nothing turns red. It just quietly tells you Christmas Day is a Friday —",
        f"and in 2027 Christmas Day is a {dt.date(2027,12,25).strftime('%A')}.",
    ])

    y = heading(c, y, "Months that share a starting day in 2027")
    from collections import defaultdict
    g = defaultdict(list)
    for m in range(1, 13):
        d = dt.date(YEAR, m, 1)
        g[d.strftime('%A')].append((calendar.month_name[m], calendar.monthrange(YEAR, m)[1]))
    for day, ms in g.items():
        if len(ms) > 1:
            c.setFillColorRGB(*INK)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(M + 8, y, f"{day}:")
            c.setFillColorRGB(0.28, 0.30, 0.31)
            c.setFont("Helvetica", 10)
            c.drawString(M + 80, y, " · ".join(f"{n} ({d})" for n, d in ms))
            y -= 16
    y -= 6
    y = body(c, y, [
        "Sharing a start only gets you most of the way — the lengths differ, so the last",
        "row is wrong. Exactly ONE pair is identical: January and October, both Friday,",
        "both 31 days. Build January; October is a copy-paste.",
    ], size=9.5, lead=13)
    y -= 14

    y = heading(c, y, "So")
    body(c, y, [
        "Reuse the layout, the fonts, the photographs, the colours — all of it.",
        "Never reuse the numbers. Rebuild the grid, or start from one built for 2027",
        "and check February against the four-week rule before you trust it.",
    ], size=10.5, lead=15)
    footer(c)
    c.showPage()
    c.save()


# ---------------------------------------------------- print checklist ------
def print_checklist(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Printing it properly", "2027 calendar kit")
    y = body(c, y, [
        "A calendar is a print object, so the export settings matter more than usual.",
    ])
    y -= 16

    y = heading(c, y, "The file type")
    for t, dpi, use, good in [
        ("PDF Print", "300 dpi", "bleed, crop marks, colour profile — for a print shop", True),
        ("PDF Standard", "96 dpi", "screens only. Numbers print soft and look cheap", False),
    ]:
        c.setFillColorRGB(*(TEAL if good else PINK))
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M + 8, y, t)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(M + 110, y, dpi)
        c.setFillColorRGB(0.28, 0.30, 0.31)
        c.setFont("Helvetica", 9.5)
        c.drawString(M + 175, y, use)
        y -= 19
    y -= 10

    y = callout(c, y, "Bleed: two different files for two different buyers", [
        "PRINT SHOP  →  bleed ON, crop marks ON. Anything running to the edge needs it.",
        "HOME PRINTABLE  →  bleed OFF. A home printer cannot print to the edge, so a bled",
        "file gives your buyer a white border and a cropped picture — and a bad review.",
    ])

    y = heading(c, y, "Before you export")
    y = checkbox_list(c, y, [
        "January starts on a Friday.",
        "February is a perfect 4 x 7 block with no gaps.",
        "Six rows in the table, not five.",
        "Same layout on all twelve pages.",
        "Nothing in the bottom-right cell — that is where people write.",
        "Holidays either absent, or named in the title (\"UK bank holidays\").",
        "PDF Print at 300 dpi.",
        "Bleed on for a print shop, off for a home printable.",
        "The year is in the filename.",
        "If you started from last year's file: the numbers were REBUILT, not edited.",
    ])
    y -= 6

    y = heading(c, y, "Paper and binding")
    body(c, y, [
        "160–200 gsm for a wall calendar — thin paper curls and shows the next month.",
        "Leave 12–15 mm of clear space at the top if it is going to be hole-punched or",
        "wire-bound, and check nothing important sits in that band on any of the twelve.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


# ----------------------------------------------------- listing guide -------
def listing_guide(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Selling the set", "2027 calendar kit")
    y = body(c, y, [
        "Calendars are one of the few products with a hard season. Everything below is",
        "about not missing it.",
    ])
    y -= 16

    y = callout(c, y, "The timing, which matters more than the design", [
        "Calendars sell from August to December. The heaviest weeks are late November and",
        "early December, when people buy them as gifts.",
        "",
        "If it is not listed by the end of October you have missed most of the season.",
        "Listing in January is listing a year late.",
    ], col=AMBER)

    y = heading(c, y, "Three things that move the needle")
    for n, t, s in [
        ("1", "Sell the set, not the month",
         "Twelve pages, one download, one price. Nobody wants to buy March separately."),
        ("2", "Put the year in the title AND the first line",
         "It is what people search in August, and it stops somebody buying it in March"),
        ("3", "Include A4 and US Letter, and say so",
         "Most printable-calendar complaints are an A4 file printed on Letter paper."),
    ]:
        c.setFillColorRGB(*PINK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(M + 8, y, n)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M + 28, y, t)
        y -= 14
        y = body(c, y, [s], size=9.5, lead=13, indent=28)
        y -= 8

    y = heading(c, y, "A title that works")
    c.setFillColorRGB(0.20, 0.22, 0.23)
    c.setFont("Courier", 10)
    for ln in [
        "2027 Printable Wall Calendar | 12 Months | A4 + US Letter | Instant Download",
        "2027 Calendar Printable | Minimalist Monthly Wall Calendar | Digital Download",
    ]:
        c.drawString(M + 8, y, ln)
        y -= 16
    y -= 8

    y = heading(c, y, "And the one line to put in the description")
    body(c, y, [
        "\"Monday-start, dated for 2027.\" It answers the two questions every buyer of a",
        "printable calendar actually has, and it is the reason they will not message you.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


# ---------------------------------------------------------- read me --------
def readme(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Read me first", "2027 calendar kit")

    blocks = [
        ("What's in this kit", [
            "The editable Canva calendar — twelve month pages with the 2027 grids",
            "   ALREADY CORRECT, Monday-start, in A4 and US Letter wall plus an A5",
            "   desk version, with a cover and a notes page",
            "The four reference PDFs (grid reference, why it shifts, print checklist,",
            "   listing guide)",
        ]),
        ("The one thing this kit exists to prevent", [
            "You cannot make a 2027 calendar by editing the year on a 2026 one.",
            "A common year is 52 weeks and one day, so every date lands one weekday",
            "   later. 1 January 2026 was a Thursday; 1 January 2027 is a Friday.",
            "Nothing warns you. The grid just quietly says the wrong thing, and a",
            "   printed calendar is something people trust and write on.",
        ]),
        ("The check that takes one second", [
            "February 2027 starts on a Monday and has 28 days — exactly four weeks.",
            "On a Monday-start grid it is a perfect 4 x 7 block with no blank squares",
            "   at either end. It is the only month of the year that does that.",
            "If your February has a gap, the grid is wrong. Check it before anything.",
        ]),
        ("How to use the template", [
            "Open the template link — it copies into your own Canva account.",
            "Leave the numbers alone. They are the part that is already right.",
            "Change the photographs, the colours, the fonts and the month styling.",
            "Keep the layout identical across all twelve pages, and keep the",
            "   bottom-right cell clear — that is where people write.",
            "Export as PDF Print at 300 dpi. Bleed ON for a print shop, OFF for a",
            "   home printable.",
        ]),
        ("Next year", [
            "2028 is a leap year: the shift is TWO days, not one, and February gets a",
            "   29th. Do not reuse this one either.",
        ]),
        ("Licence", [
            "Use this kit to make and sell your own calendars, including printables",
            "   you list on Etsy or elsewhere.",
            "You may not resell, share or redistribute the template or these PDFs",
            "   themselves, and you may not sell the kit as your own.",
        ]),
    ]
    for title, lines in blocks:
        y = heading(c, y, title)
        y = body(c, y, ["• " + ln if not ln.startswith("   ") else ln for ln in lines], size=9.5, lead=13)
        y -= 8

    footer(c)
    c.showPage()
    c.save()


if __name__ == "__main__":
    made = [
        ("calendar-2027-grid-reference.pdf", grid_reference),
        ("calendar-2027-why-it-shifts.pdf", why_it_shifts),
        ("calendar-2027-print-checklist.pdf", print_checklist),
        ("calendar-2027-listing-guide.pdf", listing_guide),
        ("calendar-2027-READ-ME.pdf", readme),
    ]
    for name, fn in made:
        fn(os.path.join(OUT, name))
    print(f"wrote {len(made)} PDFs")
