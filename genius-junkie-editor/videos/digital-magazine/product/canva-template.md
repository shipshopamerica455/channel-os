# Digital Magazine Kit — Canva assets

Built 10 Aug 2026 in the user's Canva account via the Canva MCP.

## Template (live)

- **Digital Magazine Kit — A4, wired contents page (Genius Junkie)**
  - design_id `DAHR479afAA` · **5 pages, 1240 × 1754 px** (A4 portrait proportions)
  - edit: https://www.canva.com/design/DAHR479afAA/edit
  - **Template link (buyers): NOT YET CREATED** — see "one manual step" below
  - Palette: paper `#fdfbf7`, ink `#171512`, editorial red `#c8402f`,
    slate `#4a5a6a`, warm grey `#b9b2a7`. Column guides use the Genius Junkie
    pink `#e91e8c` at 45% so they read as guides, not design.

### The pages

| # | Page title | What's on it |
|---|---|---|
| 1 | 1 COVER | full-bleed photographic cover art, `PAPER` masthead at 190 pt, issue line, three cover lines (the first in Genius Junkie yellow) |
| 2 | 2 CONTENTS (links wired) | four entries at 46 pt, underlined in editorial red, plus the note explaining **Link → Pages in this document** and the effect-text warning |
| 3 | 3 FEATURE | the two column guides drawn in, 96 pt headline, 34 pt standfirst, 21 pt two-column body, image well in the third column, red-ruled pull quote |
| 4 | 4 SPONSOR | full-bleed image block, 82 pt heading, one-line pitch, a rounded **Find out more** button for the sponsor URL, and the click-test reminder |
| 5 | 5 PARTS BIN (keep this page) | one styled example of all four sizes + a pull quote — the page the buyer copies from instead of restyling |

The type scale is the one the video teaches: **96 / 34 / 21 / 15 pt** plus a
62 pt pull quote. Margins are 15 mm (88 px at this scale); the two column
guides sit at x = 443 and x = 797.

## ⚠ One manual step (Canva UI, cannot be done over the API)

Open the design → **Share → Template link → Create template link → Copy**.
Then:

1. put it in `videos/digital-magazine/video.json` → `product.canvaTemplate`
2. run `node pipeline/gj.mjs commerce digital-magazine`

The thank-you page will NOT publish until that link exists — `commerce()`
refuses to ship a paid delivery page with a dead link in it.

## Reference PDFs (generated, not Canva)

`python3 product/make_magazine_kit.py` → 6 A4 PDFs: the grid drawn to scale,
the type scale set at real sizes, a 16-page flatplan, a link map to click-test
against, the export checklist, and the read-me.

## Sold as

- Page: https://geniusjunkie.net/digital-magazine-kit/
- Delivery: https://geniusjunkie.net/digital-magazine-kit-thank-you/
- Stripe: created by `gj commerce` (£4.99) — written back into `video.json`
- Files on server: /var/www/ghost/content/files/<kit-base>/magazine/
