# Frailty workbook update workflow

Use this when Jose sends a mouse frailty-index voice note and asks to add/update a mouse in the Cieslik LabVault workbook.

## Workbook location

Drive remote/path:

```text
drive-lab:Raw/frailty/Friality Index and Hanging Time Excel /FI_WHT_4.14.26__updated.xlsx
```

Main sheet: `Fraility Index` (typo preserved). Preserve existing sheet names and workbook formulas.

## Safe update sequence

1. Refresh Google OAuth token if needed, then update rclone token fields for `drive-lab:` before reading/writing.
2. Copy the workbook locally to a temp path.
3. Create a remote backup before editing, named like:
   `FI_WHT_4.14.26__updated.backup_before_<mouse_id>.xlsx`
4. Open with `openpyxl` using `data_only=False` so formulas are preserved.
5. Search for the mouse ID first. If present, update that row instead of adding a duplicate.
6. If adding a new mouse, append after the **last non-empty Mouse ID row**, not the first blank row. The sheet has group separator blanks in the middle, so first-blank insertion can put new mice into an old cohort block.
7. Copy row style/number formats from the previous non-empty row.
8. Fill the dictated clinical sign columns; leave strain/cage/weight blank when not provided.
9. Set the Total FI formula in column AJ / 36:
   `=IF(COUNT(F<row>:AH<row>)=0,"",SUM(F<row>:AH<row>)/29)`
10. Upload the workbook back to the same remote path.
11. Re-download the uploaded workbook and verify:
    - exactly one row has the mouse ID
    - row values match the voice note
    - row formula is present
    - backup file exists remotely

## Column mapping reminders

- Mouse ID: B / 2
- Date: E / 5
- Clinical signs: F:AH / 6:34
- Total Weight: AI / 35
- TOTAL FI formula: AJ / 36

Important voice-transcription pitfall: the column is **Kyphosis**. Voice transcription may render it as “psychosis”; if Jose says it in the frailty-index clinical-sign sequence, map it to Kyphosis unless context clearly says otherwise.

## Formula sanity check

For an entry with Alopecia `0.5`, Coat Condition `0.5`, Kyphosis `1`, and all other signs `0`, the expected FI is:

```text
(0.5 + 0.5 + 1) / 29 = 0.0689655172
```
