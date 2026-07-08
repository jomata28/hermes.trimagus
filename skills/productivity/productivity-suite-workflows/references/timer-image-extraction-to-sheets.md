# Timer image extraction to Google Sheets

Use when the user has a Drive folder of screenshots/photos and wants only the visible digital timer/clock number extracted into a Google Sheet. Also use for follow-up passes on the same image set where JT asks to add adjacent columns for other visible annotations, especially hand/digitally painted red/yellow IDs or numbers.

## Workflow

1. **Locate the Drive folder with rclone first**
   - Prefer `rclone lsf --recursive --dirs-only drive-hermes:` when the folder may live outside the mounted Obsidian vault.
   - Confirm the exact folder path and count files with `rclone lsjson` or `rclone lsf`.

2. **Copy images locally for batch OCR**
   - Use `rclone copy "drive-hermes:<folder>" /tmp/<workdir> --include '*.{jpg,JPG,jpeg,JPEG,png,PNG,heic,HEIC}'`.
   - Watch for unsupported formats like HEIC. Convert them to JPG with `pillow-heif` in a temp venv if needed, but keep the original filename in final output.

3. **Extract only the timer number**
   - The target value is the large white digital clock/timer number.
   - Ignore phone status bar time, battery %, handwriting, lap row duplicates, sports/player stats, captions, and unrelated numbers.
   - For Apple Stopwatch screenshots, a crop around the main stopwatch number plus Tesseract works well:
     - crop roughly x=2%..98%, y=22%..36% for 1170×2532 screenshots
     - grayscale, threshold white digits, upscale 2–3×
     - run Tesseract with `--psm 8`, `--psm 13`, and `--psm 7`, whitelist `0123456789:.`
   - Normalize common OCR forms:
     - `021560` → `02:15.60`
     - `02.15.60` → `02:15.60`
     - `0:06.55` remains `00:06.55` if consistency is desired.

4. **Manual review queue**
   - Flag rows when OCR does not match `MM:SS.xx` / `H:MM:SS.xx` / countdown-like forms.
   - Create a contact sheet of flagged images and inspect visually.
   - Mark images with no visible timer as `NO_TIMER` rather than guessing.
   - Examples from Timer ht session:
     - fantasy draft screenshot countdown at top → `09:50`
     - iPhone stopwatch → `00:06.55`
     - stove/appliance green display → `10:02`
     - social-media screenshot with no timer → `NO_TIMER`

5. **Create the Google Sheet**
   - Use Google Sheets API with scopes `spreadsheets` and Drive write access.
   - Columns: `image`, `timer`, `status`, `notes`.
   - Freeze the header, bold it, add a basic filter, auto-resize columns.
   - Move the sheet into the source Drive folder via Drive API if the folder is found.

## Follow-up pass: colored handwritten / digitally painted IDs

When JT asks to write out hand/digitally written markings in a new column:

1. **Keep the existing image order**
   - Read the current extraction CSV/Sheet first and process images in that exact order.
   - Add new columns next to the existing extraction instead of creating a separate unsorted artifact unless asked.
   - Recommended columns: `handwritten_marking`, `marking_confidence`, `marking_notes`.

2. **Target only the annotation layer**
   - Transcribe the red/yellow/dim hand-drawn or digitally painted IDs/numbers/letters.
   - Ignore the large white timer, phone UI labels, lap row, status bar time/battery, call thumbnails, and app chrome.
   - Common patterns in the Timer ht set included `HT1/HT2/HT3`, `D1/D2`, `AR`, and mouse/ID-like numbers such as `2097`, `3008`, etc.

3. **Review twice and expose uncertainty**
   - Use contact sheets for throughput, but crop/inspect individual images for messy cases.
   - Mark uncertain reads with `?` and set confidence `low` or `medium`; do not make low-visibility scribbles look definitive.
   - Use `NO_MARKING` when no colored marking is visible.
   - Prefer concise notes like `messy overlapping yellow scribbles`, `red handwriting`, or `last digit uncertain`.

4. **Chunk large sets safely**
   - For ~1k images, split by row ranges, then combine back against the original filename order.
   - Before writing to Sheets, verify: expected row count, no missing images, no duplicate images, no blank markings.
   - After writing to Sheets, read back header + sample rows + final rows to confirm the added columns landed in the right tab/range.

## Hanging-test handwritten time sheets from chat images

Use this pattern when JT sends Telegram/chat-attached photos of yellow notepad hanging-test records and asks for Excel output.

1. **Count and preserve inputs first**
   - Confirm the number of image attachments received and preserve each cache filename in the output.
   - Process every image; do not silently skip repeated-looking sheets because D2/D3/date/group combinations can repeat across cages.

2. **Transcribe the sheet structure**
   - Extract `sheet_label` / cage-group (examples: `F9`, `E2`, `E4`, `H8`, `H9`), `date`, `day` (`D2`, `D3`), `mouse_id`, and circled trial columns `1`, `2`, `3`.
   - Keep the handwritten time text exactly as written (commonly `00:56:97`, `01:12:67`, etc.); do **not** convert to numeric Excel time unless the user explicitly asks.
   - Split multi-section sheets into separate rows while preserving the same source image filename.

3. **Expose uncertainty for correction**
   - Add `confidence` and `notes` columns. Use `medium` for overwritten/darkened cells, unclear dates, or ambiguous digits; use notes like `trial_1 overwritten/darkened`.
   - Do not guess hidden or cut-off headers. Leave missing date/day blank and explain in notes.

4. **Excel deliverable pattern**
   - Create an `.xlsx` with columns: `source_image`, `sheet_label`, `date`, `day`, `mouse_id`, `trial_1`, `trial_2`, `trial_3`, `confidence`, `notes`.
   - Add a formatted table, freeze the header, auto-size columns, and include a `readme` sheet with image count, row count, and uncertainty guidance.
   - Verify by reading the workbook back: row count, headers, first row, and last row before sending `MEDIA:/path/to/file`.

## Quality rules

- Do not present OCR/visual transcription output as perfect without review. Include status/confidence/notes columns for alternates, manual fixes, and uncertain handwriting.
- Preserve source image filenames exactly, especially converted HEIC files or Telegram image-cache filenames.
- Verify the created or updated Sheet/Excel workbook by reading back row count and sample ranges before reporting the link/file.
