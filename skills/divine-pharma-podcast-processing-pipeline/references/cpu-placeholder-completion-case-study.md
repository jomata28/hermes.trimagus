# CPU Whisper Placeholder Completion Case Study

Use this reference when the daily Divine Pharma cron finds an existing fallback/placeholder note that was previously skipped because no GPU was available.

## Durable lesson

Do not treat `skipped_no_gpu` or `structured_fallback_no_transcript` as completed work. In this environment, CPU `faster_whisper` with the `base` model and `compute_type="int8"` can complete ~30-minute Divine Intervention episodes within a 600-second cron/tool window.

## Proven case

- Episode: `DIP Ep 654: The Clutch Health Insurance Podcast (Part 1)`
- Existing placeholder note: `Daily-Sessions/2026-06-02-DIP-Ep-654-The-Clutch-Health-Insurance-Podcast-Part-1.md`
- Placeholder frontmatter/status before completion included:
  - `processing_status: "structured_fallback_no_transcript"`
  - `transcription_status: "skipped_no_gpu_episode_32m10s"`
- Audio URL: `https://divineinterventionpodcasts.com/wp-content/uploads/2026/05/DIP-Ep-654-Clutch-Health-Insurance-Part-1.mp3?_=1`
- Local audio path used: `Audio/DIP-Ep-654-The-Clutch-Health-Insurance-Podcast-Part-1.mp3`
- Audio size: `25,982,300 bytes`
- Duration by ffprobe: `1929.6 seconds` (~32:10)
- Transcription command path: `/root/.hermes/hermes-agent/venv/bin/python3`
- Model: `faster_whisper.WhisperModel("base", device="cpu", compute_type="int8")`
- Elapsed transcription time: ~405.7 seconds
- Raw transcript length: 37,069 characters

## Recommended workflow

1. When the Notion database/live-site latest is already processed, scan recent notes for placeholder markers before returning `[SILENT]`.
2. If a matching placeholder exists and audio is missing, download/reuse audio in `/root/Divine-Pharmacology/Audio`.
3. Run CPU `faster_whisper` with a 600-second timeout before declaring transcription impossible.
4. Write both:
   - raw transcript `.txt` under `Transcripts/`
   - linked transcript note `*-Transcript.md` with `transcription_status: completed_faster_whisper_base_cpu`
5. Replace the original placeholder note in place rather than creating a duplicate dated note. Preserve original note date/path when possible.
6. Verify the final note contains all required sections and no placeholder markers remain:
   - `Transcription failed`
   - `Content pending transcription`
   - `structured_fallback_no_transcript`
   - `To be extracted from transcript`
   - `skipped_no_gpu`
   - `please manually process`
7. Confirm or append the normalized processed marker (for Ep 654, `live:44678a1e71120832`).

## Curation warning

Whisper may mangle medical/system terms (`USMLE`, `NBME`, `ESRD`, disease names). For study notes, use the transcript as evidence but curate obvious homophone/terminology errors before writing final bullets.
