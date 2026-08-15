# Journal-club paper decks for JT

Use this when turning a paper/PDF into a short editable journal-club presentation.

## User preference
- Default to **editable PPTX/Slides**, not static PDF.
- If JT says **“Google Drive slides editable”** or similar, the deliverable is a **native Google Slides file** (`application/vnd.google-apps.presentation`) with a share/edit link — not merely a local PPTX attachment.
- Visual style: **white background**, minimal color/decoration, simple text, no corporate/busy templates.
- For JT, default all editable slide typography to black or neutral gray. Keep source screenshots and scientific figures in their original colors unless he explicitly requests grayscale.
- Never use em dashes in slide text, speaker scripts, filenames, or Google Drive titles. Replace them with commas, colons, parentheses, or hyphens.
- When the user requests a single language, treat it as an artifact-wide constraint: editable text, speaker script, filenames, Drive title, and any newly written labels must comply.
- Use real **screenshots/crops from figures/graphs** when available.
- For journal-club papers, include a title/identity slide when useful; if JT specifically asks, **screenshot/crop the paper title from the PDF** and put it on a new first slide.
- Put images directly on the slide with **no added borders**.
- Keep slide text short; put the explanation in speaker notes/script.
- Provide **exact wording to say** for each slide, either in the final response and/or a separate speaker-script doc.

## Workflow
1. **Classify the supplied PDF before summarising it:** original research article, commentary/editorial, protocol, correction, or supplement. Capture DOI, PII, PMID, trial registration, and linked-article DOI. If it is a commentary, retrieve and read the original trial plus supplements before finalising methods, measurements, or results. See `references/publisher-pdf-retrieval-from-chrome.md` for the persistent-browser workflow when an open-access publisher blocks direct downloads.
2. Cross-check the trial registry and published protocol for prespecified assessments that the commentary or abstract can omit, especially laboratory measurements, visit schedules, estimands, and secondary outcomes. Do not infer that an unmentioned measurement was not taken.
3. Extract text and metadata from every relevant PDF (`pdftotext`, `pdfinfo`) and reconcile the original article with its supplements. If the original materially changes a commentary-based deck, say so and update the deck.
4. Render PDF pages to images (`pdftoppm -png -r 150/200`) and inspect figure locations visually.
5. Run `pdfimages -list` and compare extracted assets with the rendered page. **Do not assume an embedded raster contains the complete figure**: journal figures often store illustration art as a raster while labels, headings, bullets, and panel borders remain vector text. If `pdfimages` drops those elements, crop the rendered page so the slide preserves all labels.
6. Crop only the panels needed for the deck using PIL; avoid including article captions unless the user wants them. For a requested title screenshot, crop the title/header directly from the rendered first page rather than retyping it; retain journal identity/open-access marks when they fit cleanly.
7. Build PPTX with `python-pptx`:
   - 16:9 widescreen
   - blank/white slides
   - editable text boxes for titles, bullets, captions, and simple diagrams
   - inserted figure crops with no custom borders
8. Render the PPTX back to PDF/images with LibreOffice + `pdftoppm` and visually QA every slide.
9. Fix common crop/layout problems before delivery:
   - wrong panels included from the source figure
   - panel labels/axes cut off
   - article caption accidentally included
   - title/subtitle overlap
   - bottom-line text overlapping figure captions
10. If the requested final artifact is Google Slides, upload/convert the PPTX to Drive as native Slides:
   - MIME target: `application/vnd.google-apps.presentation`
   - if the local Google wrapper only supports search, use the authenticated Drive API multipart upload directly with metadata `{"mimeType":"application/vnd.google-apps.presentation"}` and the PPTX media body
   - verify Drive metadata shows `mimeType = application/vnd.google-apps.presentation`
   - return the `docs.google.com/presentation/.../edit` link
11. For Google Slides deliverables, QA after conversion: export the native presentation to PDF, extract its text, render every page, and visually inspect the converted artifact. If the user prohibited a language, character, or punctuation mark, scan both the local PPTX text and exported PDF text for it before delivery.
12. When replacing a draft in Drive, create and verify the corrected native Slides file first. Only after it passes QA, trash the outdated draft so the user sees one authoritative version.
13. Deliver the native Slides link; also attach the local `.pptx` and a separate `.docx`/`.md` speaker script when useful.

## Appending another paper to an existing deck

When the user asks for a second 3 to 4 slide study section immediately after an existing paper:

1. Treat the verified local PPTX as the base and assert its starting slide count before appending. Preserve the existing slides unchanged unless the new original paper exposes a factual error that requires correction.
2. Build a self-contained section in this order when possible: title and clinical question, design and population, primary long-term outcomes with the main figure, interpretation and limitations.
3. Reuse the deck's background, typography, footer style, and language rules. Continue slide numbering and extend the same speaker-script artifact rather than creating an unrelated mini-deck.
4. Keep original scientific figures in color. If a flow diagram is tall and unreadable at normal projection size, crop to screening, randomisation, and treatment assignment, then place follow-up counts in editable text. Do not shrink a complete flowchart until its labels become ornamental.
5. Distinguish measured outcomes from derived percentages. A derived value such as `100% minus cumulative appendectomy` can be shown for clarity, but the speaker script should identify the published endpoint that supports it.
6. Render and inspect the entire combined deck, not only the appended slides. Scan the complete PPTX and converted Google export for prohibited punctuation/language, confirm page order, and verify that figure colors and slide numbering survived conversion.
7. Upload the verified combined PPTX as the new native Google Slides artifact. Verify it first, then trash the superseded shorter deck.

## JT correction to remember
If JT says the deck is “supposed to be in Google Drive slides editable,” do not treat a PPTX attachment as the final deliverable. Convert/upload it to native Google Slides and give the link. If he asks to “SC the title of the paper and put into a new first slide,” add a screenshot/crop title slide before the content slides; a requested 3-slide content deck may become 4 slides total after this title slide.

## 3-slide structure that worked well
1. **Problem / limitation / novel approach** — mostly simple editable text or a clean conceptual flow.
2. **Discovery / diagnostic accuracy** — bullets left, ROC/primary performance figure screenshots right.
3. **Progression / clinical implications** — bullets left, longitudinal/Kaplan–Meier figure screenshots right.

## Quality bar
Do not stop at creating the file. Verify the generated deck by rendering it and checking real slide images. Report only after the artifact exists and the visual QA has passed.
