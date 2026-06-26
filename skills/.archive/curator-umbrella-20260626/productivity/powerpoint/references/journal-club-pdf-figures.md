# Journal club decks from paper PDFs

Use this workflow when the user wants a Google Slides / PowerPoint journal-club deck and provides a PDF. Goal: slides that are presentation-readable and grounded in the paper's actual figures.

## Preferred output shape

- Plain/clean background unless the user requests otherwise.
- Large presenter-readable bullets on the slide itself (roughly 15–18 pt body text).
- Authentic paper figure crops from the PDF, not just recreated schematic graphics.
- Short captions below images: `Fig. 2d: echocardiography — EF/FS improve by day 28`.
- If 3 slides cannot fit readable text + figures, make 4 slides and tell the user why. Legibility beats strict compression unless the user insists.

## Practical workflow

1. Download or access the PDF.
2. Inspect page count and figure locations:
   - `pdfinfo paper.pdf`
   - `pdftotext paper.pdf paper.txt` then search for `Fig. 1`, `Fig. 2`, etc.
3. Render likely figure pages at high resolution:
   - `pdftoppm -png -r 170 -f 3 -l 4 paper.pdf /tmp/pages/page`
4. Create a quick montage of pages for visual triage.
5. Use visual inspection to identify pixel crop boxes for panels.
6. Crop with Pillow:
   - `Image.open(page).crop((x1,y1,x2,y2))`
   - add a small white border so crops sit cleanly on slides.
7. Build the deck with a two-column layout: bullets left, figure crops right.
8. Upload PPTX to Google Drive with MIME conversion to `application/vnd.google-apps.presentation`.
9. Export the Google Slides deck to PDF and render it for QA.
10. Fix crops/spacing and re-upload until there are no serious visual issues.

## Cropping guidance

- Keep figure panel letters and axes/legends when they help the audience understand the result.
- Crop out long Nature/Cell/Science body captions, DOI footers, and surrounding article text.
- Avoid panel crops that include partial paragraph text at the bottom; those look accidental.
- For mechanism diagrams, crop tightly enough that the model is readable, but not so tight that labels/arrows are cut off.
- If figure labels are still tiny after cropping, split across another slide rather than shrinking everything.

## Slide writing guidance

Write bullets as talk-track anchors, not dense manuscript text:

- `Problem: post-injury inflammation drives fibroblast activation, fibrosis, and remodeling.`
- `Function: EF and FS recover better with iCDC than MI/vector controls.`
- `Interpretation: benefit depends on FAP targeting + immunomodulatory payload.`

Avoid making the slide depend on tiny figure text. The user should be able to present from the slide even if the audience cannot read every axis label.

## QA checklist

- Main slide text readable in exported PDF preview.
- No overlapping elements or cut-off text.
- Figure crops do not include accidental body-caption fragments.
- Captions do not collide with images.
- Google Slides conversion did not shift layout.
- If old drafts were uploaded during iterations, trash or clearly distinguish them so the user gets one final link.
