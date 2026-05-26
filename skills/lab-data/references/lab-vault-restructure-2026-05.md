# Cieslik LabVault restructure — 2026-05 session notes

## Final architecture
Drive folder: `Cieslik LabVault` (`root_folder_id=1wpi2sSDvg_gqm_7wa4QAjLkNXtK32nkl`) mounted via rclone remote `drive-lab:` to `/root/obsidian-lab/`.

Root should contain only:

```text
Cieslik LabVault/
├── Raw/
├── Wiki/
└── Outputs/
```

The old numbered folders were flattened into `Raw/` subfolders:

```text
Raw/
├── colony/       # Mice, Racks, Strains
├── experiments/  # Active, Completed, Templates
├── echo/         # Pending, Analyzed, Templates
├── surgery/      # Logs, Equipment
├── frailty/      # RawData, Cohorts, Analysis, frailty Excel upload
├── stats/        # R-Scripts, Prism, Results
├── protocols/    # SOP files / old Protocols subfolder
├── scripts/      # lab_vault.py
└── .obsidian-config/ # old Obsidian JSON files, not active vault config
```

`Wiki/` contains synthesized markdown such as CCL2KO echo study notes and template-derived pages. `Outputs/` contains finished deliverables / weekly PI reports.

## Important details
- The lab vault is private to Jose; he exports selected material elsewhere for lab sharing. Do not treat it as shared or publishable.
- Keep it as a sibling to personal `bitacora`, not nested inside `bitacora`.
- Personal bridge file belongs at `/root/obsidian-vault/2-Areas/Negocio/Wiki/cieslik-lab.md`; do not duplicate raw lab data there.
- If rclone cannot resolve folder by path, create/use a remote with `root_folder_id=1wpi2sSDvg_gqm_7wa4QAjLkNXtK32nkl`.
- During restructure, Google Drive API `addParents/removeParents` was needed because `rclone mount drive-hermes:<folder_id>` showed an empty mount.

## Frailty workbook
Current uploaded workbook:

`/root/obsidian-lab/Raw/frailty/Friality Index and Hanging Time Excel /FI_WHT_4.14.26__updated.xlsx`

Known sheets:
- `Fraility Index` — Mouse ID, Strain, Cage ID, Date, clinical frailty signs
- `Anesthesia Recovery` — Mouse ID, recovery time
- `Wire Test` — Mouse ID, Strain, Cage ID, Date, trial 1/2/3, means
- `weight`
- `C57BL6`, `NRF2-KO`, `CCL2-KO` summary tabs

Use `openpyxl` to inspect/edit. Preserve sheet names unless Jose explicitly approves renaming; typos may be referenced by formulas/workflows.
