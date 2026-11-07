# Etsy Listing Image Kit — Canva assets

Built 6 Aug 2026 in the user's Canva account via the Canva MCP.

## Template (live)

- **Etsy Listing Image Kit — 10 slots, 5:4 safe band (Genius Junkie)**
  - design_id `DAHRjazsnqo` · **10 pages, 2000 × 2000 px**
  - edit: https://www.canva.com/design/DAHRjazsnqo/edit
  - **Template link (buyers): NOT YET CREATED** — see "one manual step" below
  - Palette: paper `#faf7f2`, ink `#2b2622`, clay `#c2683f`, sand `#e2d4c0`,
    sage `#8d9b83`; frame `#c9a274`, table `#a8845c`. Band marker uses the
    Genius Junkie pink `#e91e8c`.

### The pages

| # | Page title | What's on it |
|---|---|---|
| 1 | 1 HERO | the abstract product art + the **5:4 safe band** drawn in: 10% pink strips top and bottom, solid guide lines at 200 px and 1800 px, and one pink note the buyer deletes before export |
| 2 | 2 MOCKUP | wall + table scene, a `#c9a274` frame with a white inner panel the buyer drops their design onto |
| 3 | 3 SCALE | the product with horizontal and vertical dimension rules and editable "20 cm" / "30 cm" labels |
| 4 | 4 CARD - INCLUDED | WHAT'S INCLUDED — 130 pt clay heading, rule, 84 pt bulleted body |
| 5 | 5 CARD - SIZES | SIZES — same card layout |
| 6 | 6 CARD - DELIVERY | HOW IT ARRIVES — same card layout |
| 7 | 7 CARD - HOW TO USE | HOW TO PRINT — same card layout |
| 8 | 8 DETAIL | close crop, shapes bled off the page edge |
| 9 | 9 DETAIL | second close crop, different part of the product |
| 10 | 10 LIFESTYLE | product on a table with two props |

All guidance lives in the page titles and the read-me PDF — the only thing on
the canvas the buyer has to delete is the safe-band layer on page 1.

## ⚠ One manual step (Canva UI, cannot be done over the API)

Open the design → **Share → Template link → Create template link → Copy**.
Then:

1. put it in `videos/etsy-mockups/video.json` → `product.canvaTemplate`
2. run `node pipeline/gj.mjs commerce etsy-mockups`

The thank-you page will NOT publish until that link exists — `commerce()`
refuses to ship a paid delivery page with a dead link in it.

## Reference PDFs (generated, not Canva)

`python3 product/make_listing_kit.py` → 6 A4 PDFs: the safe-band spec drawn to
scale, the ten-slot plan, fill-in copy for photos 4–7, the pre-publish
checklist, the Etsy specs, and the read-me.

## Sold as

- Page: https://geniusjunkie.net/etsy-listing-image-kit/
- Delivery: https://geniusjunkie.net/etsy-listing-image-kit-thank-you/
- Stripe: created by `gj commerce` (£4.99) — written back into `video.json`
- Files on server: /var/www/ghost/content/files/<kit-base>/etsylisting/
