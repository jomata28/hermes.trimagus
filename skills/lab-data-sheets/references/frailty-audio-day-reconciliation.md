# Frailty audio-day reconciliation

Use when JT asks whether every frailty voice note from a particular chat/day was transcribed and imported.

## Source inventory

Classify each item separately:

1. **Original audio available** — retain the exact media path/handle and transcribe it directly.
2. **Platform-generated transcript only** — preserve and parse it, but label it as such; do not claim the underlying audio was independently transcribed.
3. **Mentioned but unavailable media** — search the chat/session evidence and audio cache by date, then report the gap honestly.

Answer “all audios were transcribed” only after reconciling the expected voice-note count against the original-media inventory. A visible text transcription is evidence of content, not proof that Hermes independently processed the audio.

## Normalize into a staging manifest

Before any Sheet/workbook write, build one record per observation with:

- mouse ID exactly as spoken
- source type and handle/path
- item-level scores
- `all_other_items = 0` only when JT said everything else was normal/fine
- ambiguous ASR phrases and provisional mappings
- conflicts or duplicate IDs
- intended measurement date, kept distinct from submission/transcription date

Keep the manifest pending until every authoritative destination verifies.

## Duplicate-ID reconciliation

If sequential observations contain the same mouse ID but materially different scores:

- preserve both observations rather than merging them
- do not silently assign the first to the missing sequential ID
- ask one tight identity question before import
- if JT explicitly says to import all but does not resolve the identity, import only unambiguous mice and leave the conflicting observations pending; report exactly what remains blocked

## Two-destination import

Once identities are resolved:

1. Write item-level values to the detailed legacy workbook sheet `Fraility Index`.
2. Use the workbook’s actual live header mapping; do not rely on remembered column positions.
3. Fill all explicitly normal/unmentioned FI items with zero, preserve unknown metadata (strain/cage/weight) as blank, and use the workbook’s existing FI denominator/formula.
4. Write the normalized summary to the Google `Frailty` tab. If it still has placeholder columns, store the calculated FI and put the full score/provenance summary in `notes`; do not mislabel FI parameters as weight, grip, or gait.
5. Read back both destinations and compare mouse IDs, item scores, date, formula/result, and provenance.
6. Mark the staging manifest merged only after both writes verify.

## Reporting

State separately:

- original audios directly transcribed
- transcript-only observations parsed
- rows imported and verified
- unresolved observations still pending

Do not let one blocked Drive/workbook operation obscure successful writes to an independent destination, but never call the overall two-destination import complete until both verify.
