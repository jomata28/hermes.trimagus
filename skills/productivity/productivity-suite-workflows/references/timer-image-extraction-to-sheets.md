# Timer image extraction to Google Sheets

Use when the user has a Drive folder of screenshots/photos and wants only the visible digital timer/clock number extracted into a Google Sheet.

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

## Quality rules

- Do not present OCR output as perfect without review. Include a status/notes column for alternates and manual fixes.
- Preserve source image filenames exactly, especially converted HEIC files.
- Verify the created Sheet by reading back row count and a sample range before reporting the link.
