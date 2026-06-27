# Placeholder Completion Pattern for Divine Pharmacology Cron

Use this when the scheduled Divine Pharmacology pipeline finds no truly new episode but existing notes include incomplete placeholders.

## Trigger

A candidate from Notion or the live site is already in `.divine_pharma_processed`, or already has a matching Obsidian note, but the note contains placeholder language such as:

- `Transcription failed`
- `Content pending transcription`
- `structured fallback`
- `To be extracted from transcript`
- missing or non-completed `transcription_status`

## Procedure

1. Prefer completing the matching note over creating a new note.
   - Preserve the original note path/date where possible.
   - Update frontmatter with `updated`, `processing_status: completed`, and `transcription_status: completed`.
2. Reuse existing audio in `/root/Divine-Pharmacology/Audio` if present and large enough; otherwise scrape/download the MP3 from the episode page.
3. Transcribe with `faster_whisper` CPU/int8 base model; use a foreground timeout of at least 600 seconds for 20-35 minute episodes.
4. Save both:
   - raw transcript `.txt` for searchable processing
   - Obsidian transcript note under `Transcripts/` with `transcription_status: completed`
5. Replace placeholder bullets with curated transcript-derived sections:
   - Key Lessons
   - Mechanisms Explained
   - Drug Connections
   - Comprehension Questions
   - USMLE High-Yield Points
   - Evening Review
6. Verify note, transcript, audio sizes, required sections, and processed marker before reporting.

## Notes

Automated grep/name extraction may miss drug names because Whisper can mangle terms (`ondansetron`, `metoclopramide`, `cimetidine`, etc.). For high-value notes, inspect transcript excerpts around pharmacology keywords and curate the final bullets rather than relying entirely on raw regex output.

## Example from prior run

A previous placeholder for `Ep. 10 - GI Drugs` was completed by reusing/downloading the MP3, transcribing a ~35-minute / 34 MB episode with faster-whisper base CPU/int8 inside a 600-second timeout, writing a transcript note, and replacing the placeholder note in-place instead of creating a duplicate dated note.