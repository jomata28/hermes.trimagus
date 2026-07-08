# Handwritten hanging-test image extraction to Excel

Use when JT sends phone photos/screenshots of handwritten hanging-test sheets and wants the times transcribed into Excel.

## Core workflow

1. **Count attachments explicitly**
   - List every received image filename in working notes before extracting.
   - If the user asks “how many did you get?”, answer the count and filenames.

2. **Extract sheet structure**
   - Capture: `source_image`, box/group label (e.g. `F9`, `H8`, `E2`, `E4`), day label (`D1`, `D2`, `D3`), date if visible, mouse ID, trial 1, trial 2, trial 3, confidence, notes.
   - Times should stay as handwritten text (`00:56:97` etc.); do not numerically convert unless asked.
   - Mark overwritten/folded/ambiguous cells with `confidence=medium/low` and concise notes rather than guessing silently.

3. **Box-day ID column**
   - JT wants a column immediately next to `source_image` named like `box_day_id`.
   - Format: `<BOX>-<DAY_NUMBER>` from the sheet label and day label, e.g. `F9-3`, `H8-2`, `E4-3`.
   - If day is not visible but the row belongs to an inferred day, mark that inference in notes.

4. **Duplicate handling**
   - Before final Excel, check for accidental duplicates.
   - Use exact file hashes for byte duplicates plus content-level comparison from extracted metadata/values.
   - Perceptual hashes are useful, but handwritten sheet photos at different angles may not flag as close; still compare box/day/date/mouse IDs/trial values.
   - If duplicate sheets exist, keep the clearer copy and do not double-count rows. Note the excluded filename.

5. **Excel deliverable**
   - Output `.xlsx`, not just a text table.
   - Recommended columns: `source_image`, `box_day_id`, `box_label`, `date`, `day`, `mouse_id`, `trial_1`, `trial_2`, `trial_3`, `confidence`, `notes`.
   - Freeze header, add filters/table formatting, auto-size columns.
   - Verify by reading the workbook back: row count, headers, first row, last row.

## Common pitfalls

- Do not count a clearer duplicate photo as a new experimental day.
- Do not bury the requested `F9-1/F9-2/F9-3` style identifier in notes; it must be a real column next to image name.
- The user may send follow-up images after an initial workbook. Regenerate a new workbook containing all unique sheets rather than appending blindly.
