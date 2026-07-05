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
