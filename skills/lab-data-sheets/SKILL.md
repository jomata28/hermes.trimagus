---
name: lab-data-sheets
description: Read and write JT's Cieslik-lab data in the Bitácora Lab-Data Google Sheet (colony, echo, frailty, surgery, procurement) from Telegram, and build Obsidian rollups. Google Sheets is the data engine; Obsidian is the presentation layer.
version: 1.0.0
author: Hermes Agent
category: productivity
metadata:
  hermes:
    tags: [lab, research, google-sheets, data-entry, colony, echo, hmri]
---

# Lab Data Engine

JT's lab data lives in a Google Sheet, not Obsidian. This skill logs and reads it.

- **Sheet ID:** `1poTb1bVUvi5vdyrl0Fy8g309meGACo6ZpXNfG_nHhxg`
- **Tabs:** Colony, Echo, Frailty, Surgery, Procurement (+ README)
- **Schema doc:** `/root/obsidian-vault/2-Areas/Negocio/Wiki/lab-engine.md` — read it
  for the current column order of each tab before writing (JT may adjust columns).

## Tooling
```
GA=/root/.hermes/skills/productivity/productivity-suite-workflows/references/google-workspace-package/scripts/google_api.py
python "$GA" sheets get    <sheet_id> "<Tab>!A1:Z500"
python "$GA" sheets append <sheet_id> "<Tab>!A1" --values '[[...row...]]'
python "$GA" sheets update <sheet_id> "<Tab>!A5"  --values '[[...row...]]'
```
The token already has the `spreadsheets` scope. No extra auth needed.

## Operations

### Log an entry  ("log echo for m-142: EF 58, FS 31, HR 480")
1. Read the schema doc to get the **exact column order** for that tab.
2. Build the row in that order; fill `date` with today, `operator/assessor` = JT
   unless told otherwise; leave unknowns blank.
3. `sheets append` to the right tab. Confirm in one line: "Logged echo · m-142 · EF 58 ✅".

### Frailty entries from Telegram text/voice
1. Parse bilingual shorthand carefully: alopecia/alopecia, fur color/color de pelo, coat condition/condición del pelaje, loss of whiskers/pérdida de bigotes. "Resto/todo lo demás normal" means unmentioned items are normal, not missing.
2. If the user asks for a file rather than direct Sheet logging, create a standalone `.xlsx` with:
   - a detailed item-score sheet (`mouse_id`, date, assessor, individual frailty items, score sum, denominator, provisional index, notes)
   - a `sheet_import_format` tab matching the current Frailty tab columns exactly.
3. Do not silently resolve ambiguous IDs: flag likely typos in notes (e.g. `18.1062F` vs `18.2062F`) and missing sex suffixes.
4. When computing a provisional frailty index, state the denominator assumption (e.g. score_sum/31) in the workbook notes unless the user provided the exact denominator.
5. For bulk all-normal entries like “3-month males 1221–1224, all 0s” or “first five females 1225–1229 all have 0 in every cell,” act without asking if the destination is clearly Frailty/FI. Inspect the live `Frailty` header first. If the tab still has placeholder/summary columns rather than item-by-item FI columns, append normalized rows with `frailty_index = 0`, set available numeric parameter columns to `0`, and put the missing detail in `notes` (e.g. `3-month FI; male/female; all FI parameters scored 0`). Then read back the affected rows to verify.

### AR / hanging-test entries from Telegram images
Detailed batch/correction workflow: `references/ar-stopwatch-batch-workflow.md`.

- The schema doc may lag the live spreadsheet. Before writing assay rows, inspect the actual spreadsheet tabs and headers, especially for tabs not listed in the doc.
- AR entries are stored in the `Hanging_Test` tab with `assay = AR` using columns: `mouse_id, assay, day, trial, time, source_image, marking, ocr_status, confidence, notes, updated`.
- For a stopwatch screenshot plus shorthand like “Add ar to mice 1222,” parse the visible stopwatch time, check for an existing row for that mouse, then append a row like `["1222","AR","","","02:18.03","<image>","AR; 1222","ok","high","<visual note>",today]` and verify by reading the row back.
- For a batch of stopwatch screenshots, build a table first: image filename → visible stopwatch time → visible blue label/ID → interpreted mouse ID. Preserve user corrections in `notes` (e.g. “blue handwriting appears 1223; user corrected first 1223 to 1221” or “no blue mouse number visible; user identified as 1228”).
- Before appending batch AR rows, read the live `Hanging_Test` tab and skip exact duplicates already present for the same `mouse_id` + `assay=AR` + `time`; report skipped rows separately as “already existed, not duplicated.”
- If the same screenshot is sent twice or appears under two cached filenames, log one AR row and mention the duplicate image filename in `notes` rather than creating a second AR row.
- After appending, read back the affected rows/range and report a concise verified table plus any still-missing IDs from the intended block.
- When JT corrects a previously logged AR mapping (e.g. “you got 1221 and 1223 backwards”), update the existing rows in place rather than only appending corrected rows. If append/update creates duplicate correction rows, clear the stale duplicates before reporting success.
- If JT asks for “the file” after Sheet logging, update a copy of the latest legacy FI workbook (`FI_WHT...xlsx`) by appending to `Anesthesia Recovery`: column B = mouse ID, C = date, D = numeric time in seconds, optionally E = `mm:ss.xx`, F/G = update/source notes. If the same batch also includes whole-FI/Frailty rows (e.g. 1221–1229 all-zero FI), also append those rows to the workbook's `Fraility Index` sheet before delivering. Verify both `Fraility Index` and `Anesthesia Recovery` target rows with `openpyxl`; do not deliver an AR-only workbook when FI rows were part of the requested file.

### Whole FI lookup vs hanging/AR data
- If JT asks whether mice were "logged" in **whole FI**, **FI**, **Frailty Index**, or similar, search the actual whole-FI workbook/tab first (e.g. files/tabs named `FI_*`, `Fraility Index`, `Frailty Index`, `frailty_index_*`, and the Google Sheet `Frailty` tab). Do **not** answer from hanging test, wire test, or AR extraction files unless he explicitly asks about those assays.
- Treat hanging/wire/AR rows as supporting assay data, not proof that a mouse exists in whole FI.
- If you accidentally find data in a different assay while answering an FI question, label it clearly as non-FI and continue checking FI before answering.
- When current FI has no rows for requested mouse IDs, proactively search older/backed-up Excel sources before giving a negative: Drive folders such as `Cieslik LabVault/Raw/frailty/Friality Index and Hanging Time Excel/`, backup files named `FI_WHT_*.backup_before_*`, local `/tmp/frailty*`/`/tmp/lab*` copies, and broader Drive spreadsheets that may contain older lab history (e.g. `DAILY1.xlsx`).
- Report findings by source class: **whole-FI hits**, **non-FI assay hits** (HT/Wire/AR), and **older unrelated lab-history hits** (echo/dopp/weight). This prevents conflating “mouse ID exists somewhere” with “mouse has a whole-FI row.”
- Avoid creating new non-FI tabs in the lab data engine when the user's target is whole FI; ask one tight clarification if the destination tab/schema is unclear.

### Query  ("how many live mice?", "last echo for m-142")
1. `sheets get` the relevant tab, filter in-agent, answer concisely.
2. For counts/summaries, compute — don't dump the whole sheet.

### Obsidian rollup  (on request or weekly)
1. Read the tab(s), compute the summary JT wants (e.g. colony census by strain,
   week's echo averages).
2. Write a **read-only summary** note under `2-Areas/Negocio/Wiki/lab/` — clearly
   marked "generated from the Sheet, do not edit here." Never treat Obsidian as source.

## Guardrails
- **Sheet is source of truth.** Obsidian only ever presents; never edit data there.
- Confirm the column order from the schema doc each session — don't hardcode it here
  in case JT changed columns.
- Lab data is sensitive/unpublished — never send it to any external service.
- On ambiguous entries (which mouse? which tab?), ask one tight clarifying question
  rather than guessing.
