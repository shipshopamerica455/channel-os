#!/usr/bin/env python3
"""Canva Website Launch Kit — the £4.99 pack.

Print-ready (or fill-on-screen) planning sheets for building a Canva website
that survives a phone and goes live on your own domain. No Canva plan needed to
use the sheets. Serves S8 #2 (mobile view) and S8 #3 (custom domain).

Every Canva fact on these sheets was read on Canva's Help Centre on 6 Nov 2026:
  * Designing websites — up to 45 pages; design up to 20 sections a page; Canva
    Free publishes up to 10 sections a page, paid plans up to 20; "Resize on
    mobile: Automatically adjust your design for mobile screens".
  * My website looks different on mobile — reflow stacks elements vertically;
    the five fixes (borders don't touch / nothing full width / safe margin /
    mobile preview, an approximation / group then lock).
  * Publishing websites with your own domain — Pro, Teams, Business, Education;
    Pro/Teams/Business connect up to five existing domains at a time; enter the
    domain without "www"; "Log in and auto connect" or connect manually; DNS
    changes can take up to 72 hours.
  * Setting up Website DNS records — copy only the records Canva gives you
    (Settings → Domain settings → Manage); back up your DNS first; delete
    conflicting A / AAAA / CNAME records (parked A records are common); turn off
    any host redirect; Cloudflare: proxy OFF (grey cloud); use your host's
    recommended nameservers; unsupported CAA records can block the SSL
    certificate; still Pending after 72 h → remove the domain, republish, add it
    again.

No record VALUES are printed: Canva shows them in Domain settings, and the
sheet says to copy them from there.

Output: canva-website-launch-kit-letter.pdf · canva-website-launch-kit-a4.pdf
"""
import os

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))
INK, BODY, GREY, RULE = (0.133, 0.125, 0.122), (0.28, 0.30, 0.31), (0.557, 0.541, 0.525), (0.86, 0.84, 0.81)
PINK, GREEN, BLUE, AMBER = (0.914, 0.118, 0.549), (0.133, 0.773, 0.369), (0.145, 0.388, 0.922), (0.96, 0.62, 0.04)
BAND = (0.957, 0.949, 0.933)


class Sheet:
    """One page with the house header, and a cursor `y` that flows down it."""

    def __init__(self, c, size, kicker, title, sub, tone):
        self.c, (self.W, self.H) = c, size
        self.L, self.R = 0.6 * inch, self.W - 0.6 * inch
        self.y = self.H - 0.62 * inch
        c.setFillColorRGB(*tone)
        c.rect(self.L, self.y + 4, 46, 5, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 8.5)
        c.setFillColorRGB(*PINK)
        c.drawString(self.L + 54, self.y + 3, kicker)
        self.y -= 24
        c.setFont('Helvetica-Bold', 21)
        c.setFillColorRGB(*INK)
        c.drawString(self.L, self.y, title)
        self.y -= 16
        if sub:
            self.text(sub, size=10, color=BODY)
        self.y -= 4

    def text(self, t, x=None, width=None, font='Helvetica', size=9.4, color=BODY, lead=1.36, bullet=''):
        c = self.c
        x = self.L if x is None else x
        width = (self.R - x) if width is None else width
        c.setFont(font, size)
        c.setFillColorRGB(*color)
        words, line, first = t.split(), '', True
        ind = 12 if bullet else 0
        for w_ in words:
            trial = (line + ' ' + w_).strip()
            if c.stringWidth(trial, font, size) > width - ind:
                c.drawString(x + (0 if first else ind), self.y, ((bullet + '  ') if first and bullet else '') + line)
                self.y -= size * lead
                line, first = w_, False
            else:
                line = trial
        c.drawString(x + (0 if first else ind), self.y, ((bullet + '  ') if first and bullet else '') + line)
        self.y -= size * (lead + 0.2)

    def head(self, t, tone=INK):
        c = self.c
        self.y -= 4
        c.setFillColorRGB(*tone)
        c.rect(self.L, self.y - 2, 4, 12, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 11.5)
        c.setFillColorRGB(*INK)
        c.drawString(self.L + 10, self.y, t)
        self.y -= 16

    def box(self, x, y, s=9):
        self.c.setStrokeColorRGB(*GREY)
        self.c.setLineWidth(0.9)
        self.c.rect(x, y - 2, s, s, fill=0, stroke=1)

    def ticks(self, items, cols=1, size=9.2, gap=15):
        colw = (self.R - self.L) / cols
        rows = (len(items) + cols - 1) // cols
        for i, t in enumerate(items):
            x = self.L + (i // rows) * colw
            y = self.y - (i % rows) * gap
            self.box(x, y)
            self.c.setFont('Helvetica', size)
            self.c.setFillColorRGB(*BODY)
            self.c.drawString(x + 15, y, t)
        self.y -= rows * gap + 4

    def field(self, label, x, w, y=None):
        y = self.y if y is None else y
        self.c.setFont('Helvetica', 8.5)
        self.c.setFillColorRGB(*GREY)
        self.c.drawString(x, y, label)
        self.c.setStrokeColorRGB(*RULE)
        self.c.setLineWidth(0.8)
        lw = self.c.stringWidth(label, 'Helvetica', 8.5) + 6
        self.c.line(x + lw, y - 2, x + w - 8, y - 2)

    def fields(self, labels, cols=2, gap=22):
        colw = (self.R - self.L) / cols
        for i, lab in enumerate(labels):
            self.field(lab, self.L + (i % cols) * colw, colw, self.y - (i // cols) * gap)
        self.y -= ((len(labels) + cols - 1) // cols) * gap + 2

    def table(self, cols, rows, rh=17, mark_after=None, mark_text=''):
        """cols = [(header, width_fraction)]; rows = number of blank rows (or list of first-cell labels)."""
        c = self.c
        tw = self.R - self.L
        xs = [self.L]
        for _, fr in cols:
            xs.append(xs[-1] + tw * fr)
        c.setFillColorRGB(*BAND)
        c.rect(self.L, self.y - 5, tw, 17, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 8.6)
        c.setFillColorRGB(*INK)
        for (h, _), x in zip(cols, xs):
            c.drawString(x + 4, self.y, h)
        self.y -= rh
        labels = rows if isinstance(rows, list) else [str(i + 1) for i in range(rows)]
        for i, lab in enumerate(labels):
            c.setStrokeColorRGB(*RULE)
            c.setLineWidth(0.6)
            c.line(self.L, self.y - 5, self.R, self.y - 5)
            for x in xs[1:-1]:
                c.line(x, self.y - 5, x, self.y + rh - 5)
            c.setFont('Helvetica', 8.6)
            c.setFillColorRGB(*GREY)
            c.drawString(self.L + 4, self.y, lab)
            self.y -= rh
            if mark_after is not None and i + 1 == mark_after:
                c.setStrokeColorRGB(*PINK)
                c.setLineWidth(1.6)
                c.line(self.L, self.y + rh - 5, self.R, self.y + rh - 5)
                c.setFont('Helvetica-Bold', 8)
                c.setFillColorRGB(*PINK)
                c.drawRightString(self.R, self.y + rh - 2, mark_text)
        self.y -= 4

    def foot(self, n):
        c = self.c
        c.setFont('Helvetica', 7.6)
        c.setFillColorRGB(*GREY)
        c.drawString(self.L, 0.42 * inch, 'Canva Website Launch Kit · Genius Junkie · Canva facts read on Canva Help Centre, 6 Nov 2026')
        c.drawRightString(self.R, 0.42 * inch, str(n))
        c.showPage()


def build(size, tag):
    path = os.path.join(OUT, f'canva-website-launch-kit-{tag}.pdf')
    c = pdfcanvas.Canvas(path, pagesize=size)
    c.setTitle('Canva Website Launch Kit · Genius Junkie')
    c.setAuthor('Genius Junkie')
    n = 0

    # 1 — read me
    s = Sheet(c, size, 'CANVA WEBSITE LAUNCH KIT · READ ME', 'Plan it once. Publish it once.',
              'Eight sheets that take a Canva website from an empty design to a live address on your own domain — and keep it readable on a phone.', BLUE)
    s.head('How to use the kit', BLUE)
    for t in [
        'Print the sheets you need, or fill them in on screen in any PDF reader.',
        'Plan the pages and sections BEFORE you design — sheet 2 and 3 keep you inside the free plan\'s publishing limit.',
        'Design with the mobile preview open. Before publishing, run the mobile audit (sheet 4) on every page.',
        'Publish to the free address first. Connect your own domain with sheet 6 once the site is right.',
        'Building for someone else? Finish with the handover sheet (8).',
    ]:
        s.text(t, bullet='•')
    s.head('The sheets', GREEN)
    s.ticks(['2  Site planner — every page', '3  Section planner — one per page', '4  Mobile audit — one per page',
             '5  Element map — find overlaps, pairs, full-width', '6  Custom-domain worksheet', '7  Launch checklist — 24 steps',
             '8  Handover sheet'], cols=1, gap=15)
    s.head('The two reflow rules (Canva Help: My website looks different on mobile)', PINK)
    s.text('"Reflow adapts Canva websites to different screen sizes by stacking elements vertically." Overlapping elements shrink in mobile view; ungrouped elements can separate. There is one design — fix the phone version on the desktop page.')
    s.head('The limits worth knowing (Canva Help: Designing websites)', AMBER)
    s.text('Up to 45 pages per website. You can design with up to 20 sections a page; Canva Free publishes up to 10 sections a page, paid plans up to 20.', bullet='•')
    s.text('A Mobile website or Link in Bio design publishes to a canva.link address only — no custom domain. Start from a Website template if you want one later.', bullet='•')
    s.text('Connecting your own domain: Canva Pro, Teams, Business or Education. Canva Free shows a "Designed with Canva" footer.', bullet='•')
    s.y -= 6
    s.text('These sheets are for your own sites and sites you build for clients. Please do not resell or share the PDFs themselves.', font='Helvetica-Oblique', size=8.8, color=GREY)
    n += 1; s.foot(n)

    # 2 — site planner
    s = Sheet(c, size, 'SHEET 2 · SITE PLANNER', 'Every page, before you design',
              'Page order here = the order in your menu. Up to 45 pages per website (Canva Help: Designing websites).', GREEN)
    s.fields(['Site name', 'Free address (…canva.site/…)', 'Own domain (later)', 'Template used (must be a WEBSITE template)'], cols=2)
    s.table([('#', 0.06), ('Page name', 0.28), ('What it is for (one line)', 0.38), ('Sections', 0.12), ('In menu ✓', 0.16)],
            22 if size == letter else 25)
    s.text('Sections column: on Canva Free, any page over 10 sections will not publish — split it into two pages.', size=8.8, color=PINK)
    n += 1; s.foot(n)

    # 3 — section planner
    s = Sheet(c, size, 'SHEET 3 · SECTION PLANNER', 'One page, section by section',
              'Plan the blocks top to bottom — the phone will stack them in this order.', GREEN)
    s.fields(['Page', 'Date'], cols=2)
    s.table([('#', 0.05), ('Section', 0.23), ('What is in it', 0.33), ('Words on photo?', 0.19), ('Pairs to group', 0.2)],
            20, rh=26 if size == letter else 28, mark_after=10, mark_text='CANVA FREE PUBLISHES UP TO HERE (10)')
    s.text('Design limit: 20 sections a page. Paid plans publish all 20; Canva Free publishes 10 (Canva Help: Designing websites).', size=8.8, color=GREY)
    n += 1; s.foot(n)

    # 4 — mobile audit
    s = Sheet(c, size, 'SHEET 4 · MOBILE AUDIT', 'Three passes, one page at a time',
              'Preview → Mobile. Canva calls the preview "an approximation" — the real test is the published site on a phone.', PINK)
    s.fields(['Page', 'Date', 'Resize on mobile: ON?', 'Checked by'], cols=2)
    s.head('Pass 1 · ORDER — read it top to bottom like a stranger', BLUE)
    s.table([('Should come…', 0.5), ('…but on the phone it comes', 0.5)], ['1', '2', '3', '4', '5', '6'], rh=21)
    s.head('Pass 2 · SIZE — text that suddenly went tiny (overlapping?)', PINK)
    s.table([('Element', 0.4), ('Overlaps what?', 0.35), ('Fixed ✓', 0.25)], 3, rh=21)
    s.head('Pass 3 · GAPS — things that drifted apart (never grouped?)', AMBER)
    s.table([('Element', 0.4), ('Belongs with', 0.35), ('Grouped + locked ✓', 0.25)], 3, rh=21)
    s.head("Canva's five fixes — tick what you used", GREEN)
    s.ticks(["Borders don't touch (resize / crop)", 'Nothing full width (smaller pieces)', 'Inside the safe margin',
             'Checked in the mobile preview', 'Grouped, then locked'], cols=2, gap=14)
    s.head('Live-site test — the published address, in the phone\'s own browser', INK)
    s.table([('Phone (make)', 0.3), ('Browser', 0.22), ('Date', 0.18), ('Every page OK? / notes', 0.3)], 3, rh=21)
    n += 1; s.foot(n)

    # 5 — element map
    s = Sheet(c, size, 'SHEET 5 · ELEMENT MAP', 'Sketch the page, then find the three problems',
              'Draw each element as a box — its REAL box (click it in Canva), not just the picture. A photo with a soft fade still has a full rectangle; a text box can run far past its last word.', BLUE)
    c.setStrokeColorRGB(*GREY)
    c.setLineWidth(1)
    dw = (s.R - s.L) * 0.66
    dh = dw * 0.9
    top = s.y - 6
    c.rect(s.L, top - dh, dw, dh, fill=0, stroke=1)
    pw = (s.R - s.L) * 0.22
    ph = dh * 1.12
    px = s.R - pw
    c.roundRect(px, top - ph, pw, ph, 10, fill=0, stroke=1)
    c.setFillColorRGB(*RULE)
    for gx in range(int(s.L) + 12, int(s.L + dw), 14):
        for gy in range(int(top - dh) + 12, int(top), 14):
            c.circle(gx, gy, 0.6, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 8.5)
    c.setFillColorRGB(*GREY)
    c.drawString(s.L, top + 4, 'DESKTOP PAGE')
    c.drawString(px, top + 4, 'PHONE — THE STACK')
    s.y = top - ph - 18
    s.head('Mark on the sketch', INK)
    s.ticks(['RED: every pair of boxes that touch or overlap → separate them',
             'BLUE: every pair that belongs together → group, then lock',
             'AMBER: anything the full width of the page → rebuild as smaller pieces',
             'GREEN: number the boxes 1, 2, 3… in the order the phone should show them'], cols=1, gap=15)
    n += 1; s.foot(n)

    # 6 — custom domain
    s = Sheet(c, size, 'SHEET 6 · CUSTOM DOMAIN', 'Connect your own domain — and keep a record',
              'Canva Help: Publishing websites with your own domain · Setting up Website DNS records (read 6 Nov 2026).', AMBER)
    s.fields(['Domain (no "www")', 'Bought from (registrar / DNS host)', 'Canva plan (Pro / Teams / Business / Education)', 'Root domain or subdomain?', 'Connect method (auto / manual)', 'Date connected'], cols=2)
    s.head('Before you change anything', PINK)
    s.ticks(['Backed up the current DNS settings (a screenshot is fine)',
             'Removed conflicting A / AAAA / CNAME records — parked A records are the usual culprit',
             "Turned OFF the host's redirect / forwarding feature (it can add hidden records)",
             'Nameservers are the ones the host recommends (custom nameservers block record changes)',
             'Using Cloudflare? Proxy OFF for Canva\'s records — the cloud turns grey',
             'No CAA records that block the SSL certificate (see Canva\'s DNS help)'], cols=1, gap=14)
    s.head("The records Canva gives you — copy them from Settings → Domain settings → Manage", BLUE)
    s.table([('Type', 0.12), ('Name / host', 0.2), ('Value (copy from Canva — never retype)', 0.48), ('Added ✓', 0.2)], 5, rh=21)
    s.head('Waiting for it to connect', GREEN)
    s.text('DNS changes can take up to 72 hours. In Canva, "Current value" should match "Expected value". Still Pending after 72 hours? Remove the domain connection, republish the website, and add the domain again.', size=8.9)
    s.table([('Checked on', 0.3), ('Status (Pending / Connected)', 0.4), ('What I changed', 0.3)], 4, rh=21)
    n += 1; s.foot(n)

    # 7 — launch checklist
    s = Sheet(c, size, 'SHEET 7 · LAUNCH CHECKLIST', 'Start to published — 24 steps', '', GREEN)
    steps = [
        'Started from a WEBSITE template (not Mobile website / Link in Bio)', 'Pages planned on sheet 2, in menu order',
        'No page over 10 sections if on Canva Free', 'Navigation: each menu item linked to its page',
        'Every photo is one I own or am allowed to use', 'Photos cut down — one hero per page, a few elsewhere',
        'Any music behind a play button, never autoplay', 'Mobile preview open while designing',
        'Words never placed on top of a photo', "No two elements' borders touch",
        'Every pair grouped, then locked', 'No element spans the full width',
        'Text and buttons inside the safe margin', 'Buttons big enough for a thumb',
        'Mobile audit (sheet 4) done for every page', 'Every link and button clicked in Preview',
        'Site address chosen — it will be printed and shared', 'Settings: Resize on mobile ON',
        'Published', 'Live address opened on a real phone — every page',
        'Second phone / browser checked', 'Own domain connected (sheet 6) — or free address kept',
        'Address tested from a phone that is NOT logged in to Canva', 'Address shared — and noted on the handover sheet',
    ]
    s.ticks(steps, cols=1, gap=19.5 if size == letter else 22, size=9.6)
    n += 1; s.foot(n)

    # 8 — handover
    s = Sheet(c, size, 'SHEET 8 · HANDOVER', 'Building it for someone else',
              'Hand over three things with every site: the Canva design, the live address, and who owns what.', PINK)
    s.fields(['Client / owner', 'Date handed over', 'Canva design shared to (their account)', 'Live address', 'Own domain + registrar', 'Domain login held by'], cols=2)
    s.head('Who owns what', BLUE)
    s.table([('Thing', 0.34), ('Which account owns it', 0.36), ('Notes', 0.3)],
            ['Canva design', 'Published site', 'Domain + DNS', 'Forms (e.g. Google Form)', 'Photos / licences', 'Email address on the site', 'Other'], rh=28)
    s.head('Before you hand it over', GREEN)
    s.ticks(['The design lives in THEIR Canva account, not just mine', 'Any form on the site is their copy, collecting to their account',
             'They know how to edit, then publish again (same address, new version)', 'They know a free site keeps the "Designed with Canva" footer',
             'They have this sheet'], cols=1, gap=20)
    s.head('Notes', INK)
    for _ in range(5):
        s.c.setStrokeColorRGB(*RULE); s.c.line(s.L, s.y, s.R, s.y); s.y -= 22
    n += 1; s.foot(n)

    c.save()
    return path


if __name__ == '__main__':
    for size, tag in ((letter, 'letter'), (A4, 'a4')):
        print('wrote', os.path.basename(build(size, tag)))
