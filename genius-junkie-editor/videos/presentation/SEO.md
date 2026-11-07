# SEO — Business Presentation (video 20)


## Release

Long-form **j6Hxcjm1i6E**, private draft, public **27 Sep 2026 17:00 UTC**.

- **8V24xqYG6hY** — promo-deck-handover, 28 Sep 12:00 UTC
- **RinQ0n-WtZg** — promo-deck-headline, 29 Sep 12:00 UTC

Canva template: **DAHTtF0GzAc** — canva.link/<presentation.canvaTemplate>. Eight pages at
1920 x 1080: title, section divider, three content layouts, the chart slide,
the closing slide and an empty shell. Thank-you page and shop card live.

Built **by hand in the Canva editor** after the API commits failed. Every label
headline was rewritten as a statement so the template teaches what the video
teaches: "Revenue grew every quarter except the one we repriced" (not
"Performance Overview"), "Q1 grew 15% on engagement" (not "Q1 Performance"),
"One hire unblocks three workstreams", and a closing slide that says "What
happens next" rather than "Contact Info".

⚠️ **The `resize-design` theory was wrong.** This deck came straight from
`create-design-from-candidate` with no resize and its commit failed identically.
Commits worked up to 21 Aug and have failed on every attempt from 25 Aug — an
API-side regression, not a property of resized designs. See
`feedback-canva-commit-verify`. The Chrome editor path still works.

Also learned: nested text needs the **full locator path** including the group
segment (`page-group-child`). A `page-child` id returns "does not contain
element". And the op is `replace_text`, not `update_text`.

## Pin comment

```
Before you export to PowerPoint, read what Canva itself says about it:

"Designs downloaded as PPTX or DOCX files may look different when opened in Microsoft Powerpoint or Microsoft Word."
"You may need to make edits, or download and install the fonts you used in Canva to your device."
"Animations and embedded videos are not yet supported… they may not play as expected."

That is the vendor telling you the file will change. If the deck matters, present from Canva or send a PDF.
```
