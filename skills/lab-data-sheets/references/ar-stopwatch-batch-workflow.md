# AR stopwatch batch workflow notes

Use when JT sends multiple stopwatch screenshots for mouse Anesthesia Recovery (AR), especially when image labels are handwritten or corrected after upload.

## Reliable batch pattern

1. Build a temporary table before writing:
   - cached image filename
   - visible stopwatch time (`mm:ss.xx`)
   - visible handwritten/blue mouse label, if any
   - interpreted `mouse_id`
   - confidence / correction note
2. Apply JT's corrections exactly. Examples from prior session:
   - “first 1223 is really 1221” means do not trust the visible handwritten 1223 for that first image.
   - “one without blue numbers is 1228” means log 1228 with medium confidence and note that the user identified it.
3. Read the live `Hanging_Test` sheet before append; skip exact duplicates for the same `mouse_id` + `assay=AR` + `time`.
4. Append rows using schema:
   `mouse_id, assay, day, trial, time, source_image, marking, ocr_status, confidence, notes, updated`.
5. Read back the affected rows and report a compact verified table. Include “already existed, not duplicated” and “still missing” rows if relevant.
6. If JT corrects a mapping after logging, update rows in place and clear any duplicate correction rows before final confirmation.

## Legacy FI workbook export

When JT asks for the updated Excel file after AR logging, copy the latest `FI_WHT...xlsx` legacy workbook and append rows to `Anesthesia Recovery`:

- Column B: mouse ID
- Column C: date
- Column D: time in seconds as a number
- Column E: original `mm:ss.xx` string for readability
- Column F/G: update/source/correction notes

Verify with `openpyxl` readback before sending the workbook.
