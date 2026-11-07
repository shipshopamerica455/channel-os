#!/usr/bin/env python3
"""Canva -> Cricut Export Card — the FREE one-pager.

Built NEW, never carved out of the sticker-illustration-kit.

Every rule is quoted from the source named beside it, verified 2026-10-05:
  * Cricut Design Space help, "Image uploads: unsupported items" — the four
    forbidden items, the error text, the 5,000-path ceiling
  * Cricut Design Space help, "How to upload images" — the six file types and
    which upload as a single layer
  * Cricut, "How to weld" — what Weld does, and that it is one-way
  * Canva Help Centre, "Choose the right download file type" — SVG is paid

Deliberately NOT on this card: the price of Canva Pro, a machine, Cricut Access
or any material; which machine is best; or a list of which Canva elements are
vectors -- Canva does not label them, so the card teaches the test.

Output: canva-cricut-export-card.pdf  (one page, US Letter)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

INK   = (0.133, 0.125, 0.122)
BODY  = (0.28, 0.30, 0.31)
GREY  = (0.557, 0.541, 0.525)
RULE  = (0.894, 0.878, 0.855)
PINK  = (0.914, 0.118, 0.549)
GREEN = (0.133, 0.773, 0.369)
BLUE  = (0.145, 0.388, 0.922)
AMBER = (0.961, 0.620, 0.043)

W, H = letter
M = 0.5 * inch


def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if stringWidth(t, font, size) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rule(c, y):
    c.setStrokeColorRGB(*RULE)
    c.setLineWidth(0.8)
    c.line(M, y, W - M, y)


def para(c, y, text, size=10.5, font="Helvetica", col=BODY, lead=12.6):
    c.setFillColorRGB(*col)
    c.setFont(font, size)
    for ln in wrap(text, font, size, W - 2 * M):
        c.drawString(M, y, ln)
        y -= lead
    return y


def section(c, y, title):
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, title)
    return y - 19


def bullets(c, y, items, lead=12.8):
    for t, ok in items:
        c.setFillColorRGB(*(GREEN if ok else PINK))
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "+" if ok else "-")
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica", 10.5)
        c.drawString(M + 13, y, t)
        y -= lead
    return y


def build():
    path = os.path.join(OUT, "canva-cricut-export-card.pdf")
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setTitle("Canva to Cricut Export Card - Genius Junkie")

    y = H - M
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 25)
    c.drawString(M, y - 20, "Canva → Cricut Export Card")
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 37, "What Design Space will refuse, and why. Verified 5 October 2026.")
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M, y - 20, "geniusjunkie.net")
    y -= 46
    rule(c, y)
    y -= 18

    y = section(c, y, "AN .SVG MAY NOT CONTAIN")
    y = bullets(c, y, [
        ("Pattern fills", False),
        ("Clipping paths - \"multiple shapes layered together so that one shape masks or clips the others\"", False),
        ("Editable text - it has to be shapes", False),
        ("Linked images - images not embedded in the file", False),
    ])
    y -= 4
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M, y, "Every Canva FRAME is a clipping path. So is every photo dropped into a shape.")
    y -= 15
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y, "The error is \"Your file includes unsupported items.\" It does not say which one. Look for a frame first.")
    y -= 14
    rule(c, y)
    y -= 18

    y = section(c, y, "THE SIX FILE TYPES - AND WHICH ONES CUT")
    y = bullets(c, y, [
        (".svg and .dxf - \"cut-ready images that upload as designed\"; layers separate automatically", True),
        (".jpg .png .bmp .gif - upload as a SINGLE LAYER. You are tracing a picture, not cutting your shapes", False),
    ])
    y -= 2
    c.setFillColorRGB(*AMBER)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M, y, "SVG from Canva is PAID: \"transparent PNGs and SVGs are available to accounts with the Canva Pro,")
    y -= 13
    c.drawString(M, y, "Canva for Teams, Canva Education, and Canva for Nonprofits plans.\" There is no vector workaround.")
    y -= 14
    rule(c, y)
    y -= 18

    y = section(c, y, "THE TEST CANVA WILL NOT GIVE YOU")
    y = para(c, y, "Canva mixes vector and raster elements in the same results and does not label them. "
                   "Drop the element on the canvas and scale it to four or five times the page: a vector "
                   "stays crisp, a raster goes soft and then blocky. Two seconds per element.")
    y -= 2
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y, "Flat single-colour shapes and line icons are usually vectors. Photographic, shadowed or textured ones are not.")
    y -= 14
    rule(c, y)
    y -= 18

    y = section(c, y, "THE CEILING, THE WELD, AND THE COLOURS")
    y = bullets(c, y, [
        ("\"SVGs are restricted to 5000 paths; more than 5000 will cause an upload error to occur.\"", False),
        ("A simple icon ~3 paths. A script word: one per letter. A mandala or halftone: thousands.", False),
        ("Canva outlines text on SVG export - so Cricut's no-editable-text rule is handled for you", True),
        ("...but every letter is then its own shape. Script fonts need WELD in Design Space.", False),
        ("Weld \"joins shapes... by removing any overlapping cut lines\". It is ONE-WAY - duplicate first.", False),
        ("Each distinct FILL COLOUR becomes its own layer, and its own mat. Colour is instructions.", True),
    ])
    y -= 6
    rule(c, y)
    y -= 16

    y = section(c, y, "SEVEN CHECKS BEFORE YOU EXPORT")
    checks = [
        ("No frames, no photos dropped into shapes - those are clipping paths", True),
        ("Every element passed the scale-up test and is actually a vector", True),
        ("Flat solid colours, one per intended piece of material", False),
        ("No shadows, gradients or textures", False),
        ("The background is deleted, not white", False),
        ("Not so detailed that it will tear even if it uploads", False),
        ("Every element came from a Canva search filtered to Free", False),
    ]
    for t, hard in checks:
        c.setFillColorRGB(*(PINK if hard else GREEN))
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, "*")
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica-Bold" if hard else "Helvetica", 10.5)
        c.drawString(M + 13, y, t)
        y -= 12.4
    y -= 2
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Oblique", 9.4)
    c.drawString(M + 13, y, "The first is the one Design Space stops you for. The second wastes vinyl without stopping you at all.")

    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 8.4)
    c.drawString(M, M - 14, "Sources: Cricut Design Space help (image uploads, how to weld); Canva Help Centre.")
    c.drawRightString(W - M, M - 14, "Genius Junkie - geniusjunkie.net")

    c.showPage()
    c.save()
    print("wrote", path)


if __name__ == "__main__":
    build()
