# PDF generation and verification notes

Use when creating short user-facing PDF handouts/checklists from Markdown/HTML.

## Preferred workflow

1. Draft the source as a clean Markdown file first. Keep the scope tight: if the user asks for "solo lo necesario", remove negotiation/vendor/background sections and leave only required steps, documents, links, and cost ranges.
2. Convert to HTML/PDF with a renderer available in the environment.
3. Verify the produced PDF before delivery:
   - `file <pdf>` confirms it is a PDF.
   - `pdfinfo <pdf>` confirms page count and metadata.
   - `pdftotext <pdf> - | sed -n '1,200p'` confirms the PDF contains the intended content, not a browser error page.
4. Only deliver after the text check passes.

## Chromium/Snap pitfall

When using headless Chromium installed as a Snap, printing a local `file:///tmp/...html` can silently create a PDF containing a browser error such as `Your file couldn't be accessed` / `ERR_FILE_NOT_FOUND`, especially due to sandbox/private tmp behavior.

Robust workaround:

1. Serve the HTML over localhost from the same directory, e.g. `python3 -m http.server <port> --directory /tmp` as a tracked background process.
2. Print from `http://127.0.0.1:<port>/<file>.html` rather than `file:///...`.
3. Use `--no-pdf-header-footer` when the user wants a clean handout without date/URL headers/footers.
4. Kill the temporary HTTP server after verification.

## Delivery quality rules

- Do not stop at “PDF written”; inspect it.
- If the first render has headers/footers, literal Markdown markup, or bad pagination, regenerate and re-check.
- Keep the final PDF path stable and send only the verified file.
