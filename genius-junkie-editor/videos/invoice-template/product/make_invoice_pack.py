#!/usr/bin/env python3
"""Invoice Template Pack — sample invoice PDF, tracker sheet, quick-start guide.

Outputs (A4):
  invoice-sample.pdf        the finished invoice from the video
  invoice-tracker.pdf       printable tracker sheet (number/client/amount/sent/paid)
  invoice-pack-guide.pdf    1-page quick start: Canva link, the 8 must-haves, checklist
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdfcanvas

# The Canva template link is the paid product, so it is not in this file. It
# comes from gitignored pipeline/canva-links.json; without it the PDF would ship
# a dead link, so this fails loudly instead of guessing.
import json as _json, pathlib as _pathlib
TEMPLATE_LINK = _json.loads(
    (_pathlib.Path(__file__).resolve().parents[3] / "pipeline" / "canva-links.json").read_text()
)["links"]["invoice-template"]["canvaTemplate"]

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = A4  # 595 x 842 pt

INK = (0.122, 0.176, 0.239)     # #1f2d3d
ACCENT = (0.016, 0.471, 0.341)  # #047857
BODY = (0.2, 0.255, 0.333)      # #334155
DIM = (0.392, 0.455, 0.545)     # #64748b
LINE = (0.886, 0.91, 0.941)     # #e2e8f0

M = 40  # page margin (pt)

ROWS = [
    ("Homepage redesign — desktop & mobile", "1", "1,200.00", "1,200.00"),
    ("Brand style guide — 12 pages", "1", "450.00", "450.00"),
    ("Product photography — half day", "4 hrs", "85.00", "340.00"),
]


def invoice_sample(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = H - M

    # header — left
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(M, y - 14, "YOUR BUSINESS")
    c.setFillColorRGB(*DIM)
    c.setFont("Helvetica", 8.5)
    c.drawString(M, y - 32, "123 Studio Lane, London · hello@yourbusiness.com")
    c.drawString(M, y - 44, "Tax / VAT no. 000 0000 00 (if registered)")

    # header — right
    c.setFillColorRGB(*ACCENT)
    c.setFont("Helvetica-Bold", 30)
    c.drawRightString(W - M, y - 20, "INVOICE")
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 9.5)
    c.drawRightString(W - M, y - 40, "Invoice no. INV-2026-041")
    c.drawRightString(W - M, y - 53, "Issue date: 4 August 2026")
    c.drawRightString(W - M, y - 66, "Due date: 18 August 2026")

    # rule
    y -= 88
    c.setStrokeColorRGB(*LINE)
    c.setLineWidth(1.5)
    c.line(M, y, W - M, y)

    # bill to
    y -= 22
    c.setFillColorRGB(*ACCENT)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M, y, "BILL TO")
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10)
    c.drawString(M, y - 16, "Client Company Ltd · Attn: Accounts Payable")
    c.drawString(M, y - 30, "45 Client Street, City · accounts@client.com")

    # table header
    y -= 66
    c.setFillColorRGB(*ACCENT)
    c.roundRect(M, y - 26, W - 2 * M, 26, 4, stroke=0, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(M + 12, y - 18, "Description")
    c.drawString(M + 268, y - 18, "Qty")
    c.drawRightString(M + 400, y - 18, "Rate")
    c.drawRightString(W - M - 12, y - 18, "Amount")

    # rows (+ one deliberately empty row — the template tip)
    y -= 26
    c.setFont("Helvetica", 9.5)
    for desc, qty, rate, amt in ROWS + [("", "", "", "")]:
        y -= 30
        if desc:
            c.setFillColorRGB(*BODY)
            c.drawString(M + 12, y + 9, desc)
            c.drawString(M + 268, y + 9, qty)
            c.drawRightString(M + 400, y + 9, rate)
            c.drawRightString(W - M - 12, y + 9, amt)
        c.setStrokeColorRGB(*LINE)
        c.setLineWidth(0.6)
        c.line(M, y, W - M, y)

    # totals
    y -= 34
    c.setFont("Helvetica", 9.5)
    c.setFillColorRGB(*DIM)
    c.drawRightString(W - M - 90, y, "Subtotal")
    c.setFillColorRGB(*BODY)
    c.drawRightString(W - M, y, "1,990.00")
    y -= 16
    c.setFillColorRGB(*DIM)
    c.drawRightString(W - M - 90, y, "Tax (20%)")
    c.setFillColorRGB(*BODY)
    c.drawRightString(W - M, y, "398.00")

    # TOTAL DUE box — the one loud number
    y -= 46
    bw = 210
    c.setFillColorRGB(*ACCENT)
    c.roundRect(W - M - bw, y - 10, bw, 38, 6, stroke=0, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(W - M - bw + 14, y + 4, "TOTAL DUE")
    c.setFont("Helvetica-Bold", 15)
    c.drawRightString(W - M - 14, y + 2, "£2,388.00")

    # payment details
    c.setFillColorRGB(*ACCENT)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M, y + 18, "PAYMENT DETAILS")
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 9)
    for i, ln in enumerate([
        "Bank: Your Bank · Account name: Your Business",
        "Account no. 00000000 · Sort code 00-00-00",
        "Or pay online: pay.yourbusiness.com/inv-041",
        "All amounts in GBP · payment fees are the payer's responsibility",
    ]):
        c.drawString(M, y + 2 - i * 12, ln)

    # footer
    c.setFillColorRGB(*DIM)
    c.setFont("Helvetica", 8.5)
    c.drawString(M, M + 62, "Payment due within 14 days of issue. Overdue invoices may incur a late fee.")
    c.drawString(M, M + 46, "Notes: PO #4471 · Final invoice for the July project")
    c.setFont("Helvetica-Oblique", 9.5)
    c.drawCentredString(W / 2, M + 16, "Thank you for your business.")

    c.showPage()
    c.save()


def tracker(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(M, H - M - 16, "INVOICE TRACKER")
    c.setFillColorRGB(*DIM)
    c.setFont("Helvetica", 9.5)
    c.drawString(M, H - M - 34, "One row per invoice. Friday afternoons, scan the PAID column.")

    cols = [("No.", 0), ("Client", 120), ("Amount", 280), ("Sent", 360), ("Due", 430), ("Paid", 500)]
    y = H - M - 60
    c.setFillColorRGB(*ACCENT)
    c.roundRect(M, y - 24, W - 2 * M, 24, 4, stroke=0, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 9.5)
    for label, dx in cols:
        c.drawString(M + 10 + dx, y - 16, label)

    y -= 24
    c.setFont("Helvetica", 9)
    for i in range(26):
        y -= 26
        if i % 2 == 0:
            c.setFillColorRGB(0.976, 0.98, 0.988)
            c.rect(M, y, W - 2 * M, 26, stroke=0, fill=1)
        c.setStrokeColorRGB(*LINE)
        c.setLineWidth(0.6)
        c.line(M, y, W - M, y)
    c.setStrokeColorRGB(*LINE)
    for _, dx in cols[1:]:
        c.line(M + dx, y, M + dx, H - M - 84)

    c.setFillColorRGB(*DIM)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(W / 2, M - 6, "Genius Junkie · geniusjunkie.net")
    c.showPage()
    c.save()


def guide(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = H - M

    c.setFillColorRGB(*ACCENT)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(M, y - 20, "Invoice Template Pack")
    c.setFillColorRGB(*DIM)
    c.setFont("Helvetica", 10)
    c.drawString(M, y - 38, "Quick start · Genius Junkie · geniusjunkie.net")

    y -= 74
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M, y, "1 · Open the editable Canva template")
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10)
    c.drawString(M, y - 18, TEMPLATE_LINK)
    c.setFillColorRGB(*DIM)
    c.setFont("Helvetica", 9)
    c.drawString(M, y - 33, "Opens a private copy in your free Canva account. Nothing is shared back.")

    y -= 64
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M, y, "2 · The eight non-negotiables")
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 9.5)
    for i, t in enumerate([
        'The word "Invoice", visible at a glance',
        "A unique invoice number (INV-2026-041 → 042 → 043…)",
        "Your business details + tax/VAT number if registered",
        "The client's LEGAL company name and the right contact",
        "Issue date AND a real calendar due date",
        "Line items: what you did, qty, rate, amount",
        "Subtotal · tax · total due",
        "Exactly how to pay — account details or a payment link",
    ]):
        c.drawString(M + 14, y - 20 - i * 14, f"{i + 1}.  {t}")

    y -= 150
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M, y, "3 · The habits that get you paid")
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 9.5)
    for i, t in enumerate([
        "Write outcomes, not activity — 'Homepage redesign', not 'design work, 12 hrs'",
        "One loud number: box the total in your accent colour",
        "A real due date beats 'Net 30' every time",
        "Name the file: Invoice-INV-2026-041-YourBusiness.pdf",
        "Export PDF Standard (small + crisp), attach it — never a link",
        "Log every invoice in the tracker sheet the day you send it",
    ]):
        c.drawString(M + 14, y - 20 - i * 14, f"•  {t}")

    y -= 128
    c.setFillColorRGB(*ACCENT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M, y, "4 · Every future invoice = 90 seconds")
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 9.5)
    c.drawString(M + 14, y - 20, "Make a copy → number +1 → dates → line items. The total follows.")
    c.drawString(M + 14, y - 34, "Keep one design per monthly client and it becomes a two-field edit.")

    c.setFillColorRGB(*DIM)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(W / 2, M + 26, "Invoice requirements and tax rules vary by country — check what applies where you're registered.")
    c.drawCentredString(W / 2, M + 14, "© Genius Junkie · personal and single-business use · not for resale")
    c.showPage()
    c.save()


if __name__ == "__main__":
    invoice_sample(os.path.join(OUT, "invoice-sample.pdf"))
    tracker(os.path.join(OUT, "invoice-tracker.pdf"))
    guide(os.path.join(OUT, "invoice-pack-guide.pdf"))
    print("wrote invoice-sample.pdf, invoice-tracker.pdf, invoice-pack-guide.pdf")
