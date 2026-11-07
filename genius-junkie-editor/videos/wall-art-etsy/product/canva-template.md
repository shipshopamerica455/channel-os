# Wall Art Starter Pack — Canva assets

Built 6 Aug 2026 in the user's Canva account via the Canva MCP.

## Template (live)

- **Printable Wall Art — Neutral Arch Set of 3**
  - design_id `DAHRigihX3E` · 3 pages, 16 × 20 in (1536 × 1920 px @ 96dpi)
  - edit: https://www.canva.com/design/DAHRigihX3E/fUvtkonVf35SXvZWJ3TVbQ/edit
  - **Template link (buyers):** canva.link/<wall-art-etsy.canvaTemplate>
  - Palette: paper `#f5f1ea`, ink `#2c2622`, terracotta `#c26e4f`,
    sand `#dcc9b0`, sage `#8d9b83`.
  - Pages: *bloom* (arch + circle), *drift* (pill + dome), *still*
    (small arch + tall pill). 10% margin built in; word set at 112pt.

## Print files (generated, not Canva)

`python3 product/make_wallart_pack.py` → 15 art PDFs (3 designs × 5 ratios:
2x3, 3x4, 4x5, 11x14, ISO-A) + sizes chart + read-me. All vector, so they
are genuinely 300 DPI at any size — this sidesteps Canva's 96-DPI PNG trap
that the video is built around.

## Sold as

- Page: https://geniusjunkie.net/wall-art-starter-pack/
- Delivery: https://geniusjunkie.net/wall-art-starter-pack-thank-you/
- Stripe: https://buy.stripe.com/6oU9AU6Zd5XlcEAdanaR208 (£4.99)
  - product `prod_V1ZCB2Q1f5ZwUo` · price `price_1U1W41Lqu5srzOz9v79Maz0a`
- Files on server: /var/www/ghost/content/files/<kit-base>/wallart/ (17 PDFs)
