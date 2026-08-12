# Whole-FI recovery ladder

Use this when a requested mouse/cohort is absent from the current Frailty tab or workbook—especially when JT says he already provided it.

## 1. Normalize identity variants

Search each ID as:
- bare number: `1062`
- age/timepoint prefix variants: `18.1062F`, `21-1062F`, `21.1062F`
- sex suffixes: `F`, `M`
- punctuation variants: `.`, `-`, spaces
- plausible transcription/OCR variants, but label them as hypotheses

Do not silently merge two identities.

## 2. Search authoritative FI stores

1. Live Google Sheet `Frailty` tab.
2. Latest `FI_WHT...xlsx`, sheet `Fraility Index`.
3. Every `backup_before_*` workbook.
4. Pending voice-note queues (`frailty_index_pending*.jsonl/csv`).
5. Local import/export artifacts (`frailty_index_all_workbook_rows.csv`, selected-mice workbooks).

## 3. Search beyond the modern FI folder

- Drive root and lab remote, not only `Raw/frailty/`.
- Cohort/age workbooks such as `21 and 24 months 2024.xlsx`.
- Broad lab-history workbooks such as `DAILY1.xlsx`.
- Weekly reports and experiment notes.

A mouse appearing in grip strength, echo, weight, DAILY1, or a cohort list proves context/identity only—not whole FI.

## 4. Recover conversation evidence

- Search exact IDs in user, assistant, and tool messages.
- Search parent/child session lineages around compaction boundaries.
- Search clinical terms (`alopecia`, `dermatitis`, `coat condition`, `distended abdomen`) when IDs may have been mistranscribed.
- Inspect nearby image attachments and voice-note transcriptions.
- A correction embedded in a skill or note can establish that a cohort/ID was discussed, but cannot supply missing scores by itself.

## 5. Classify the result

### A. Scores recovered
Report the authoritative source, exact ID, date, individual scores, formula/denominator, and verification.

### B. Provision evidenced, scores not recoverable
Say plainly that JT likely supplied/discussed the data, identify the evidence, and explain that values were not persisted or cannot be reconstructed. Do not phrase this as “you never gave it.”

### C. No evidence after escalation
Only use this after steps 1–4. State what source classes were checked.

## 6. Persistence repair

When scores are recovered or re-supplied:
1. Write them to the detailed legacy `Fraility Index` workbook.
2. Write the normalized summary row to the live Google `Frailty` tab.
3. Preserve source provenance (voice/image/session/date).
4. Read both back and verify IDs and values.
5. Keep a pending JSONL record until both writes verify; then mark it merged.

## Pitfalls

- Do not substitute AR/HT/Wire/grip data for FI.
- Do not infer clinical scores from cohort membership, sex, age, or weight.
- Do not become more confident merely because many backups all descend from the same already-incomplete workbook.
- Do not argue with the user's recollection; escalate the search and distinguish evidence from recoverable values.
