---
name: lab-data
category: productivity
description: Manage Cieslik Lab vault — log mice, echo data, surgery logs, frailty scores, and sync with Google Sheets API. Separate from personal vault.
trigger: User asks to log lab data, update mouse records, record echo measurements, manage Cieslik Lab vault, or work with obsidian-lab
---

# Lab Data Management — Cieslik Lab

## References
- `references/lab-vault-restructure-2026-05.md` — session-specific notes on the Raw/Wiki/Outputs migration, rclone/Drive API quirks, and the frailty workbook location/schema.

## Architecture
The vault uses **Raw → Wiki → Outputs** (flattened from the old 01-09 numbered folder system).

```
Drive root/
├── bitacora/                  ← Personal vault (NEVER shared)
└── cieslik-lab/               ← Lab vault (NEVER shared from here)
    ├── Raw/
    │   ├── colony/            ← Mouse inventory (Google Sheets/Excel)
    │   ├── experiments/       ← Active, Completed, Templates
    │   ├── echo/              ← Pending, Analyzed, Templates
    │   ├── surgery/           ← Logs, Equipment
    │   ├── frailty/           ← RawData, Cohorts, Analysis
    │   ├── stats/             ← R-Scripts, Prism, Results
    │   ├── protocols/         ← SOP files
    │   ├── scripts/           ← lab_vault.py
    │   └── .obsidian-config/  ← Obsidian workspace JSON files
    ├── Wiki/                  ← Synthesized knowledge, protocols, study docs
    └── Outputs/
        └── weekly-reports/    ← PI update reports (Thursday 1 PM meetings)
```

**Key rule:** Both vaults are PRIVATE. User controls any export. Never share anything from either vault unless explicitly told to.

## VPS Mount
- Personal: `drive-hermes:bitacora` → `/root/obsidian-vault/`
- Lab: rclone remote `drive-lab` (root_folder_id=`1wpi2sSDvg_gqm_7wa4QAjLkNXtK32nkl`) → `/root/obsidian-lab/`
- Two separate rclone mounts, never nested
- **Use `--vfs-cache-mode writes`** for real-time sync

## Bridge
- `/root/obsidian-vault/2-Areas/Negocio/Wiki/cieslik-lab.md` tracks career-facing summary only
- No lab data duplicated inside personal vault
- Bridge content: active experiments, certifications, PI meetings, weekly rhythm, skills, succession timeline

## Data Logging Workflow

### When user sends data via Telegram (voice or text):
1. **Identify the domain:** Colony / Echo / Surgery / Frailty / Stats
2. **Find the correct file** in `/root/obsidian-lab/Raw/<domain>/`
3. **Update the markdown or spreadsheet** with proper formatting
4. **Confirm** to user what was logged and where

### Colony (`Raw/colony/`)
- **Strains:** CCL2KO, C57BL/6J, NRF2KO, Wild-Type
- **~151 mice** across 2 racks
- Fields: mouse-id, strain, sex, age-mo, cage-id, status, group
- Status values: Active, Euthanized, Pending, Scheduled

### Echo (`Raw/echo/`)
- Machines: Vevo 770 + Vevo Lab 5.11.1
- Pipeline: Pending → Analyzed
- Fields: mouse-id, group, status, date-acquired

### Surgery (`Raw/surgery/`)
- LAD occlusion training (certification assessed June 8, 2026)
- Log: mouse-id, surgery-type, scheduled-date, status, outcome

### Frailty (`Raw/frailty/`)
- Tests: frailty index, wire hang, grip strength, anesthesia recovery, weight.
- Existing Excel source file: `/root/obsidian-lab/Raw/frailty/Friality Index and Hanging Time Excel /FI_WHT_4.14.26__updated.xlsx`
  - Note the current Drive folder has a typo and trailing space: `Friality Index and Hanging Time Excel `. Do not silently rename sheet names or folder names if formulas/references may depend on them; ask first.
  - Workbook sheets observed: `Fraility Index`, `Anesthesia Recovery`, `Wire Test`, `weight`, `C57BL6`, `NRF2-KO`, `CCL2-KO`.
  - Use `openpyxl` for direct edits/inspection. If the rclone mount path is missing, remount `drive-lab:` before assuming the file is gone.
- Log: mouse-id, test-type, score/time, date, observer. For wire test, capture trial 1/2/3 and mean when available.

#### Frailty Index voice-entry workflow
When Jose dictates mouse frailty scores by voice:
1. Interpret short IDs as full IDs using the session pattern, e.g. mouse `2154`, male, cohort `18` → `18.2154M`; female → `18.2154F`. If transcript drops a digit (`18.254` while he says mouse 2154), use the spoken mouse number.
2. Before editing, create a workbook backup with a specific suffix, e.g. `.backup_before_2154.xlsx` or `.backup_before_2148_2149.xlsx`.
3. In `Fraility Index`, add/update the mouse row. Leave strain/cage/weight blank unless explicitly provided.
4. **Explicitly write `0` to every clinical frailty field `F:AG` first**, then overwrite only abnormal fields with `0.5` or `1`. This is important: normal/not-mentioned fields should not be left blank.
5. Leave `AH` Standardized Weight and `AI` Total Weight blank unless given. Write `AJ` formula as `=IF(COUNT(F{row}:AH{row})=0,"",SUM(F{row}:AH{row})/29)`.
6. Reload the workbook and verify: row number, mouse ID, nonzero fields, all other clinical fields are zero, manual FI (`sum(F:AG)/29`), and AJ formula.
7. Keep Telegram confirmation concise: row, key nonzero scores, “everything else explicitly 0,” manual FI, formula verified, backup filename.

Pitfalls:
- Avoid nested Python f-strings when building shell heredocs; outer formatting can turn `{row}`/`{0}` placeholders into `0`, producing formulas like `F0:AH0`. Prefer `.format(row, row, row, row)` inside the executed Python script and verify the formula after saving.
- Voice transcript may confuse column names: “eye discharge/swelling,” “ID discharge/scherger swelling,” etc. map to column `L`; “code/coat condition” maps to column `I`; “distended abdomen” maps to `O`; “piloerection/direction” maps to `T`.

### Stats (`Raw/stats/`)
- R scripts (3-way ANOVA for age × sex × genotype studies)
- GraphPad Prism exports

### Weekly Rhythm
- Wednesday 9-10am: Lab meeting
- Thursday 1pm: 1-on-1 with PI (Dr. Cieslik)
- Friday 9-10am: Journal club

### Key People
- Dr. Cieslik (PhD, ECM, Primary PI)
- Dr. Taffet (MD, Geriatrics, Co-PI)
- Thuy (mouse team colleague, shares colony/frailty data)
- Aude + Katia (wet lab team)

## Succession Plan
- Jose leaves December 2026
- All workflows must be documented for handoff
- Training targets: colony mgmt, echo protocol, frailty tests, R analysis pipeline