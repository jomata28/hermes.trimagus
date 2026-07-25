# Journal-club paper decks for JT

Use this when turning a paper/PDF into a short editable journal-club presentation.

## User preference
- Default to **editable PPTX/Slides**, not static PDF.
- If JT says **“Google Drive slides editable”** or similar, the deliverable is a **native Google Slides file** (`application/vnd.google-apps.presentation`) with a share/edit link — not merely a local PPTX attachment.
- Visual style: **white background**, minimal color/decoration, simple text, no corporate/busy templates.
- Use real **screenshots/crops from figures/graphs** when available.
- For journal-club papers, include a title/identity slide when useful; if JT specifically asks, **screenshot/crop the paper title from the PDF** and put it on a new first slide.
- Put images directly on the slide with **no added borders**.
- Keep slide text short; put the explanation in speaker notes/script.
- Provide **exact wording to say** for each slide, either in the final response and/or a separate speaker-script doc.

## Workflow
1. Extract text and metadata from the PDF (`pdftotext`, `pdfinfo`) to understand the paper.
2. Render PDF pages to images (`pdftoppm -png -r 150/200`) and inspect figure locations visually.
3. Crop only the panels needed for the deck using PIL; avoid including article captions unless the user wants them.
4. Build PPTX with `python-pptx`:
   - 16:9 widescreen
   - blank/white slides
   - editable text boxes for titles, bullets, captions, and simple diagrams
   - inserted figure crops with no custom borders
5. Render the PPTX back to PDF/images with LibreOffice + `pdftoppm` and visually QA every slide.
6. Fix common crop/layout problems before delivery:
   - wrong panels included from the source figure
   - panel labels/axes cut off
   - article caption accidentally included
   - title/subtitle overlap
   - bottom-line text overlapping figure captions
7. If the requested final artifact is Google Slides, upload/convert the PPTX to Drive as native Slides:
   - MIME target: `application/vnd.google-apps.presentation`
   - if the local Google wrapper only supports search, use the authenticated Drive API multipart upload directly with metadata `{"mimeType":"application/vnd.google-apps.presentation"}` and the PPTX media body
   - verify Drive metadata shows `mimeType = application/vnd.google-apps.presentation`
   - return the `docs.google.com/presentation/.../edit` link
8. For Google Slides deliverables, QA after conversion when feasible: export/render the converted presentation or at minimum verify the native file exists in Drive.
9. Deliver the native Slides link; also attach the local `.pptx` and a separate `.docx`/`.md` speaker script when useful.

## JT correction to remember
If JT says the deck is “supposed to be in Google Drive slides editable,” do not treat a PPTX attachment as the final deliverable. Convert/upload it to native Google Slides and give the link. If he asks to “SC the title of the paper and put into a new first slide,” add a screenshot/crop title slide before the content slides; a requested 3-slide content deck may become 4 slides total after this title slide.

## 3-slide structure that worked well
1. **Problem / limitation / novel approach** — mostly simple editable text or a clean conceptual flow.
2. **Discovery / diagnostic accuracy** — bullets left, ROC/primary performance figure screenshots right.
3. **Progression / clinical implications** — bullets left, longitudinal/Kaplan–Meier figure screenshots right.

## Quality bar
Do not stop at creating the file. Verify the generated deck by rendering it and checking real slide images. Report only after the artifact exists and the visual QA has passed.
