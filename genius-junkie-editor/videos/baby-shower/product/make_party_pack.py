#!/usr/bin/env python3
"""Party Printables Kit — the reference sheets that ship with the editable Canva
party kit (A6 invitation, favour tag, table number, thank-you card, plus the
four-up A4 sheets).

The card and envelope arithmetic is COMPUTED from the ISO A-series definition,
so the chart and the diagrams cannot drift from each other.

Verified 2026-09-01.

Outputs (all US Letter):
  01-size-and-envelope-chart.pdf  what fits what, and why A6 wins
  02-print-dialog-guide.pdf       the setting that shrinks your card, per app
  03-paper-guide.pdf              weights, trays and finishes
  04-trimming-guide.pdf           steel rule, three passes, long cuts first
  05-pre-print-checklist.pdf      the one-page check before you print twenty
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

PAPER = (0.984, 0.980, 0.973)
INK = (0.227, 0.200, 0.188)
BLUSH = (0.906, 0.812, 0.780)
SAGE = (0.725, 0.780, 0.706)
GREY = (0.659, 0.690, 0.682)
PINK = (0.914, 0.118, 0.549)
GREEN = (0.133, 0.773, 0.369)
AMBER = (0.961, 0.620, 0.043)
BODY = (0.28, 0.30, 0.31)
W, H = letter
M = 0.7 * inch

# The A series, from the definition: A(n+1) is A(n) halved across the long side.
A4_W, A4_H = 210.0, 297.0
A6_W, A6_H = A4_W / 2, A4_H / 2          # 105 x 148.5 → A6 is 105 x 148
A6_H = 148.0
DEAD_MM = 4.5        # typical home-printer non-printable margin
GUIDE_MM = 10.0      # keep-in margin for type


def page(c, title, kicker=None):
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - M
    if kicker:
        c.setFillColorRGB(*PINK)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(M, y + 4, kicker.upper())
        y -= 6
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 23)
    c.drawString(M, y - 20, title)
    c.setFillColorRGB(*PINK)
    c.rect(M, y - 34, 62, 3, stroke=0, fill=1)
    return y - 58


def footer(c):
    c.setFillColorRGB(0.62, 0.64, 0.63)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(W / 2, M - 16, "Genius Junkie · geniusjunkie.net")


def body(c, y, lines, size=10.5, lead=15, indent=0, col=BODY):
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


def wrap(text, width_pt, size, font="Helvetica"):
    out, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if stringWidth(trial, font, size) <= width_pt:
            line = trial
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def para(c, y, text, size=10.5, lead=15, col=BODY, width=None):
    return body(c, y, wrap(text, width or (W - 2 * M), size), size=size, lead=lead, col=col)


def callout(c, y, title, lines, col=PINK, width=None):
    w = width or (W - 2 * M)
    wrapped = []
    for ln in lines:
        wrapped.extend(wrap(ln, w - 28, 9.5) if ln else [""])
    h = 34 + 13 * len(wrapped)
    c.setStrokeColorRGB(*col)
    c.setLineWidth(2)
    c.roundRect(M, y - h, w, h + 6, 9, stroke=1, fill=0)
    c.setFillColorRGB(*col)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M + 14, y - 16, title)
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 9.5)
    yy = y - 33
    for ln in wrapped:
        c.drawString(M + 14, yy, ln)
        yy -= 13
    return y - h - 18


def table(c, y, cols, rows, widths, head_col=PINK):
    x = M
    c.setFillColorRGB(*head_col)
    c.setFont("Helvetica-Bold", 9)
    for col, wdt in zip(cols, widths):
        c.drawString(x, y, col.upper())
        x += wdt
    y -= 6
    c.setStrokeColorRGB(*GREY)
    c.setLineWidth(0.7)
    c.line(M, y, M + sum(widths), y)
    y -= 14
    for row in rows:
        x = M
        for cell, wdt, i in zip(row, widths, range(len(row))):
            c.setFillColorRGB(*(INK if i == 0 else BODY))
            c.setFont("Helvetica-Bold" if i == 0 else "Helvetica", 10)
            c.drawString(x, y, str(cell))
            x += wdt
        y -= 16
    return y - 6


def checkbox_list(c, y, items, size=10.5, lead=19):
    for t in items:
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(0.9)
        c.rect(M, y - 2, 10, 10, stroke=1, fill=0)
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica", size)
        c.drawString(M + 20, y, t)
        y -= lead
    return y


# ---------------------------------------------------- 1 · sizes & envelopes ---
def pdf_sizes():
    c = pdfcanvas.Canvas(os.path.join(OUT, "01-size-and-envelope-chart.pdf"), pagesize=letter)
    y = page(c, "Card sizes and the envelopes that fit them", "party kit · sheet 1")
    y = para(c, y, "The size decides the envelope, and the envelope is the thing you cannot change "
                   "later. Decide this first.")
    y -= 8
    y = table(c, y, ["card", "size", "envelope", "per A4 sheet"], [
        ("A6 ✓", f"{A6_W:.0f} × {A6_H:.0f} mm", "C6", "4"),
        ("5 × 7 in", "127 × 178 mm", "A7", "2"),
        ("A5", "148 × 210 mm", "C5", "2"),
        ("Favour tag", "50 × 90 mm", "—", "8–10"),
        ("Place card", "90 × 55 mm folded", "—", "8"),
    ], [1.6 * inch, 1.9 * inch, 1.5 * inch, 1.5 * inch])

    # the tiling diagram, computed
    y -= 6
    scale = (3.0 * inch) / (A4_H * mm)
    aw, ah = A4_W * mm * scale, A4_H * mm * scale
    x0, y0 = M, y - ah
    c.setFillColorRGB(1, 1, 1)
    c.rect(x0, y0, aw, ah, stroke=0, fill=1)
    c.setStrokeColorRGB(*INK); c.setLineWidth(1); c.rect(x0, y0, aw, ah, stroke=1, fill=0)
    for i in range(4):
        cx = x0 + (i % 2) * aw / 2
        cy = y0 + (1 - i // 2) * ah / 2
        c.setFillColorRGB(*(BLUSH if i % 2 == 0 else SAGE))
        c.rect(cx + 1, cy + 1, aw / 2 - 2, ah / 2 - 2, stroke=0, fill=1)
    c.setStrokeColorRGB(*PINK); c.setLineWidth(1.4); c.setDash(4, 3)
    c.line(x0 + aw / 2, y0, x0 + aw / 2, y0 + ah)
    c.line(x0, y0 + ah / 2, x0 + aw, y0 + ah / 2)
    c.setDash()
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10)
    c.drawString(x0 + aw + 20, y - 16, "Four A6 cards tile an A4 sheet exactly.")
    c.setFillColorRGB(*BODY); c.setFont("Helvetica", 9.5)
    for i, ln in enumerate(wrap("That is not a coincidence — A6 is defined as a quarter of A4. It is "
                                "why A6 is the recommendation: no waste, no arithmetic, and C6 "
                                "envelopes are sold everywhere.", W - (x0 + aw + 20) - M, 9.5)):
        c.drawString(x0 + aw + 20, y - 34 - i * 13, ln)
    y = y0 - 24

    y = callout(c, y, "Measure an envelope you already own", [
        "Envelope sizing is quoted loosely. A C6 that is really 114 × 162 mm wants a card a",
        "couple of millimetres UNDER A6, not exactly A6, or it fights you going in.",
        "Two millimetres of clearance is the difference between posting twenty invitations",
        "and wrestling twenty invitations.",
    ])
    footer(c)
    c.save()


# --------------------------------------------------- 2 · the print dialog ---
def pdf_dialog():
    c = pdfcanvas.Canvas(os.path.join(OUT, "02-print-dialog-guide.pdf"), pagesize=letter)
    y = page(c, "The setting that shrinks your card", "party kit · sheet 2")
    y = para(c, y, "Every print dialog has a page-sizing option, and the default is some version of "
                   "\"Fit\". Fit shrinks the document so it sits inside the area your printer can "
                   "physically reach — by a few percent. That is enough that the card no longer fits "
                   "the envelope.")
    y -= 8
    y = table(c, y, ["where you print from", "what it is called", "set it to"], [
        ("Adobe Acrobat", "Page Sizing and Handling", "Actual size"),
        ("Chrome / Edge", "More settings → Scale", "100 (Custom)"),
        ("macOS Preview", "Scale to fit", "untick it"),
        ("Windows Photos", "Fit picture to frame", "untick it"),
    ], [2.1 * inch, 2.6 * inch, 1.9 * inch])

    y = callout(c, y, "Never choose", [
        "Fit · Fit to page · Fit to printable area · Shrink oversized pages · Scale to fit",
    ])
    y = callout(c, y, "Then prove it before you cut twenty", [
        f"Print one sheet. Take a ruler. An A6 card is {A6_W:.0f} millimetres wide.",
        "If it measures 101, the dialog is still scaling and no amount of redesigning fixes it.",
        "This takes fifteen seconds and it is the only check that matters.",
    ], col=GREEN)

    y = heading(c, y, "The other half of the problem")
    y = para(c, y, f"Your printer cannot print to the edge of the sheet. Consumer machines have a "
                   f"non-printable margin of roughly {DEAD_MM:.0f} millimetres, often deeper on the "
                   f"trailing edge. That is why the kit lays four cards up on one A4 sheet with white "
                   f"all round the outside of the block: the dead zone lands on empty paper, and "
                   f"because the cards touch each other, cutting down the shared line gives you "
                   f"colour running right to the edge — full bleed on a printer that cannot do it.")
    footer(c)
    c.save()


# ------------------------------------------------------------ 3 · paper ---
def pdf_paper():
    c = pdfcanvas.Canvas(os.path.join(OUT, "03-paper-guide.pdf"), pagesize=letter)
    y = page(c, "Paper", "party kit · sheet 3")
    y = para(c, y, "The single biggest jump in perceived quality available to you, and it costs "
                   "almost nothing.")
    y -= 8
    y = table(c, y, ["weight", "what it is", "use it for"], [
        ("80 gsm", "copier paper", "test prints only"),
        ("120–160 gsm", "heavy paper", "order-of-service, inserts"),
        ("200–250 gsm", "light card", "invitations, tags"),
        ("300 gsm", "card", "invitations you want to feel"),
    ], [1.7 * inch, 2.4 * inch, 2.5 * inch])

    y = callout(c, y, "Check the tray before you buy a ream", [
        "Most home printers take about 200 gsm through the main tray and heavier through the",
        "rear or manual feed, one sheet at a time. It is in the manual under media weight.",
        "Feeding 300 gsm through the main tray is how you jam a printer.",
    ], col=AMBER)

    y = heading(c, y, "Finish")
    y = para(c, y, "Matt or silk for anything with text on it. Gloss fingerprints, and an invitation "
                   "gets handled — passed round, stuck on a fridge, put in a bag.")
    y -= 4
    y = heading(c, y, "One more thing that costs nothing")
    y = para(c, y, "Print the whole run in one sitting, from the same pack, on the same day. Card "
                   "from two different packs can differ slightly in whiteness, and once you have "
                   "seen it side by side in a stack you cannot unsee it.")
    footer(c)
    c.save()


# --------------------------------------------------------- 4 · trimming ---
def pdf_trimming():
    c = pdfcanvas.Canvas(os.path.join(OUT, "04-trimming-guide.pdf"), pagesize=letter)
    y = page(c, "Cutting them neatly", "party kit · sheet 4")
    y = para(c, y, "Cutting is where home-made cards are usually given away, and it is entirely "
                   "fixable. Do not use scissors.")
    y -= 8
    y = heading(c, y, "What you need")
    y = body(c, y, [
        "· A steel rule — not plastic, the blade will shave plastic",
        "· A craft knife with a fresh blade",
        "· A self-healing cutting mat",
        "· Optional: a corner rounder",
    ])
    y -= 6
    y = callout(c, y, "Three light passes, not one heavy one", [
        "One heavy pass drags the card and tears the last centimetre. Three light passes cut",
        "clean through. Hold the rule down harder than feels necessary and keep your fingers",
        "behind the blade line, not beside it.",
    ], col=GREEN)

    y = heading(c, y, "The order")
    y = body(c, y, [
        "1.  Cut the long lines first, all the way across the sheet.",
        "2.  Then the short ones.",
        "3.  Fewer setups, and the pieces stay square.",
    ], size=11, lead=17)
    y -= 8
    y = callout(c, y, "If you use a guillotine", [
        "Check it against a set square before you trust it. One that is half a degree out will",
        "taper twenty cards IDENTICALLY — and you will not notice until they are stacked.",
    ], col=AMBER)
    y = para(c, y, "Punch holes in favour tags AFTER cutting, never before, or you will cut through "
                   "the hole. A corner rounder, if you own one, is the last five percent.")
    footer(c)
    c.save()


# -------------------------------------------------------- 5 · checklist ---
def pdf_checklist():
    c = pdfcanvas.Canvas(os.path.join(OUT, "05-pre-print-checklist.pdf"), pagesize=letter)
    y = page(c, "Before you print twenty", "party kit · sheet 5")
    y = para(c, y, "Print this and tick it. Everything on it is recoverable before you press print "
                   "and expensive afterwards.")
    y -= 10
    y = heading(c, y, "Design")
    y = checkbox_list(c, y, [
        f"Card is A6 ({A6_W:.0f} × {A6_H:.0f} mm) — or the size that matches my envelopes",
        f"I measured an actual envelope, not the label on the pack",
        f"All type sits inside a {GUIDE_MM:.0f} mm guide from every edge",
        "Name largest, date and time second, address and RSVP smallest",
        "The RSVP has a real date on it, not \"let me know\"",
        "Decoration sits behind the type, not through it",
    ])
    y -= 6
    y = heading(c, y, "Sheet")
    y = checkbox_list(c, y, [
        "Four cards laid up on one A4 sheet",
        "White margin all round the OUTSIDE of the block",
        "Artwork touching BETWEEN the cards",
        "Downloaded as PDF Print with crop marks",
    ])
    y -= 6
    y = heading(c, y, "Print")
    y = checkbox_list(c, y, [
        "Page sizing set to Actual size / 100% — not Fit",
        "Paper size in the dialog matches the sheet (A4)",
        "Card is in the right tray for its weight",
        "Printed ONE sheet",
        f"Measured a card with a ruler — it is {A6_W:.0f} mm wide",
    ])
    y -= 6
    y = heading(c, y, "Then, and only then")
    y = checkbox_list(c, y, [
        "Print the rest of the run in one sitting",
        "Cut long lines first, three light passes",
        "Punch tag holes after cutting",
    ])
    footer(c)
    c.save()


if __name__ == "__main__":
    pdf_sizes()
    pdf_dialog()
    pdf_paper()
    pdf_trimming()
    pdf_checklist()
    print("5 sheets written to", OUT)
