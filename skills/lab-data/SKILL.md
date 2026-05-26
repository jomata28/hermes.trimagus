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