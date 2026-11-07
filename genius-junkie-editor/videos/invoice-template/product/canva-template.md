# Invoice Template Pack — Canva assets

Built 5 Aug 2026 in the user's Canva account via the Canva MCP.

## Template (live)

- **Invoice — A4 (794 × 1123 px)**
  - "Invoice Template — A4 (Genius Junkie)"
  - design_id `DAHRXOLPUH8`
  - edit: https://www.canva.com/design/DAHRXOLPUH8/fcNOK_eptI0M8bavU1Q6vA/edit
  - **Template link (buyers):** canva.link/<invoice-template.canvaTemplate>
  - Palette: ink `#1f2d3d`, accent `#047857` (green), body `#334155`,
    dim `#64748b`, rules `#e2e8f0`.
  - Layout: 4 zones — header (business left / INVOICE + number + dates right),
    parties (BILL TO), the work (accent table header + 3 rows + one empty row),
    money & method (subtotal/tax right, accent TOTAL DUE box, payment details
    left). Footer: terms, notes, thank-you.

## Sold as

- Page: https://geniusjunkie.net/invoice-template-pack/
- Delivery: https://geniusjunkie.net/invoice-template-pack-thank-you/
- Stripe: https://buy.stripe.com/aFa4gAbftetR0VS9YbaR207 (£4.99)
  - product `prod_V13fJLA4kGFaHH` · price `price_1U11YXLqu5srzOz9KJswBPQo`
- PDFs on server: /var/www/ghost/content/files/<kit-base>/invoice/
  (invoice-sample.pdf, invoice-tracker.pdf, invoice-pack-guide.pdf)
- Regenerate PDFs: `python3 product/make_invoice_pack.py`
