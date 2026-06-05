---
name: divine-pharma-daily-cron
description: Daily Divine Intervention Pharmacology podcast processing - fetches latest episode, transcribes, extracts insights, creates Obsidian notes
version: 1.1.0
author: Hermes Agent
category: productivity
---

# Divine Intervention Pharmacology Daily Processor

This skill automates the daily processing of Divine Intervention Pharmacology podcast episodes for USMLE-style study notes in Obsidian.

## Workflow

1. **Notion Query**: Fetch latest episode from D.I. PHARM PODCASTS database
2. **Audio Processing**: Download MP3 and transcribe with Whisper
3. **Content Extraction**: Use LLM to identify key pharmacological concepts
4. **Obsidian Integration**: Create formatted daily note with template structure
5. **Notification**: Send Telegram alert with Obsidian URI

## Required Tools

- `notion`: For querying the podcast database
- `terminal`: For downloading podcast audio (curl) and file operations
- `mlops/whisper`: For audio transcription (may fail in resource-constrained environments)
- `obsidian`: For creating/updating vault notes
- `file_tools`: For HTML parsing when needed (via execute_code)

## Environment Variables

- `NOTION_API_KEY`: Notion integration token
- `OBSIDIAN_VAULT_PATH`: Path to Divine Pharmacology vault (default: `/root/Divine-Pharmacology`)

Note: Environment variables are loaded from `~/.hermes/.env` if present, otherwise from system environment.

## Processing Steps

### 1. Database Query
Queries the Notion database for the most recent episode by checking:
- Uses database ID: `2f88c883-85ba-81d3-a9d2-eca5f4e30d0b` (the database, not the data_source)
- Requires Notion API version `2022-06-28` for querying (version `2025-09-03` fails with invalid_request_url)
- Uses sort format: `{"timestamp": "created_time", "direction": "descending"}` (property sort fails with validation_error)
- Alternative approach: Fetch all records (page_size=100) and sort by created_time descending in code
- Checks properties: `Link` (URL), `Title` (episode title), `Related Topic` (categorization)
- Working query: POST to `/v1/databases/{database_id}/query` with Notion-Version: 2022-06-28
- If Notion returns only stale/already-processed pharmacology entries, use the live-site fallback rather than re-processing Notion rows.

### 2. Audio Processing
- Falls back to basic note structure if transcription fails due to resource constraints
- Saves transcription temporarily for processing when successful
- Uses HTML parsing to extract MP3 URL from episode page when direct browser tools unavailable
- For long episodes on CPU, do **not** rely on a full-episode Whisper pass: `base` and even `tiny` can exceed cron runtime. Split MP3s into ~8-minute chunks with `ffmpeg -f segment -segment_time 480 -c copy`, transcribe each chunk with `whisper --model tiny --language English --output_format txt --verbose False`, then concatenate chunk text files.
- Store noisy raw transcripts separately under `Transcripts/YYYY-MM-DD-...-Transcript.md`; keep the Daily-Sessions note cleaned/corrected for USMLE study instead of pasting noisy transcript text into the main sections.
- See `references/transcription-runtime-notes.md` for the exact chunked-transcription fallback commands and quoting pitfalls.
- See `references/live-site-scrape-fallback.md` for safe homepage scraping rules when Notion is stale; especially avoid navigation/category anchors like `Podcast Topics` and iterate past already-processed live-site episodes.
- See `references/processed-episode-matching.md` for strict processed-vs-preview matching rules; avoid treating `Evening Review Preview`/`Processing Log` mentions as evidence that an episode has already been processed.
- See `references/cron-fallback-implementation-notes.md` for stdlib-only HTML parsing when `bs4` is unavailable, plus the long-episode/no-GPU fallback checklist and verification steps.

### 3. Pharmacological Extraction
Uses LLM analysis to identify key pharmacological concepts from transcription:
- Key lessons and explained concepts
- Drug mechanisms and classifications
- New drugs mentioned with mechanisms
- System-level connections (RAAS, autonomic, etc.)
- Clinical vignettes and patient cases
- USMLE high-yield facts and mnemonics
- Comprehension questions (clinical + mechanism-based)
- Falls back to basic structure if transcription unavailable, extracting minimal info from episode title/link

### 4. Obsidian Note Creation
Formats content using the Daily-Session template:
- Frontmatter with date, podcast info, duration, and processing status
- Key Lessons section (verbatim-arranged for readability when transcription successful, placeholder when failed)
- Mechanisms Explained (detailed pathways)
- Drug Connections (new, system, previous links)
- Comprehension Questions (3-5 mixed clinical/mechanism)
- USMLE High-Yield Points (prioritized automatically)
- Evening Review Preview (teaser for next day)
- Handles transcription failures gracefully by creating structured note with placeholders

### 5. Delivery
- Creates/updates note in `Daily-Sessions/YYYY-MM-DD-Topic.md`
- For Hermes scheduled jobs where the user/system says delivery is automatic, **do not call `send_message` or any Telegram tool yourself**. Put the notification/report directly in the final response; the cron runner delivers it.
- Only send Telegram directly when the invocation explicitly requires direct delivery and no automatic delivery instruction is present.
- Notification/report should include:
  - Episode title and topic
  - Key takeaway summary or fallback/transcription status
  - Obsidian URI: `obsidian://open?vault=Divine-Pharmacology&file=Daily-Sessions/{{date}}.md`

## Usage

This skill is designed to be run via Hermes cron job:
- Schedule: `0 7 * * *` (7:00 AM CST daily)
- Delivery: `telegram` (to user's home channel)
- Model: Current main provider (for consistency)

## Error Handling

- Skips if episode already processed today
- **Also skips if the latest Notion entry matches an episode already processed on a prior day** — check `Daily-Sessions/` for notes containing the same episode title. If found, respond with `[SILENT]` instead of re-processing.
- For live-site fallback episodes, mark both a stable synthetic processed ID (for example `live:<sha256(page_url)[:16]>`) and the page URL in `~/.divine_pharma_processed`; this helps avoid duplicate processing even when titles/slugs vary.
- **Notion database staleness**: The podcast Notion database may fall behind the actual podcast feed. If the latest Notion entry is older than the last processed episode, check the podcast site directly for newer episodes (scrape `https://divineinterventionpodcasts.com/` for recent URLs). If nothing new, `[SILENT]`.
- Retries failed downloads up to 3 times
- Falls back to summary-only if transcription fails
- Preserves existing notes if processing fails mid-pipeline

## ⚠️ Critical Pitfalls

### Whisper on CPU is effectively unusable for full episodes
- Even with `tiny` model and 8-minute chunks, each chunk takes ~40-50 minutes on CPU. A 52-minute episode split into 7 chunks would take 5+ hours.
- If the cron environment has no GPU, **do not attempt Whisper** unless the episode is very short (<5 min). Fall back to structure-from-title extraction immediately.
- Even when skipping transcription, still download the MP3, verify duration with `ffprobe`, create a transcript placeholder in `Transcripts/`, and include the fallback status in frontmatter so later GPU/manual transcription has a clean handoff.
- If a prior successful transcript already exists for the episode (check `Transcripts/` or referenced in an existing note's frontmatter), reuse it instead of re-transcribing.

### Minimal dependencies in cron
- Do not assume `bs4`/BeautifulSoup is installed in the cron environment. If it is missing, use Python stdlib `html.parser` for homepage and episode-page link extraction rather than stopping or installing dependencies mid-cron.

### Notion DB vs. actual podcast feed drift
- The D.I. PHARM PODCASTS Notion database (`2f88c883-85ba-81d3-a9d2-eca5f4e30d0b`) is manually updated and can lag months behind the actual podcast feed at `divineinterventionpodcasts.com`.
- Episodes found in Notion may have been processed many times already; always cross-reference with existing notes in `Daily-Sessions/` before starting transcription.
- The `divine-pharma-notion-episodes-fetch` skill is responsible for keeping the Notion DB in sync. If the DB is stale, run that skill first or fetch directly from the podcast site.
- When scraping the live site fallback, do **not** treat navigation/category anchors or course/class announcements as episodes. Filter homepage anchors to real episode titles/URLs (prefer labels matching `DIP Ep \d+`, `Divine Intervention Episode \d+`, `Episode \d+`, or URL slugs like `dip-ep-\d+`; do **not** accept a generic dated WordPress permalink by itself). Exclude `/podcast-categories/`, `/wp-content/` audio-only links, author pages, `#respond`, and generic/announcement labels like `Podcast Topics`, `Tutoring`, `Episode Notes`, `June 2026 ... ZOOM Classes`, `Step 1 Basic Science Review`, or dates. A prior cron run almost selected a `June 2026 Step 1-3 USMLE/COMLEX ZOOM Classes` announcement because it had an MP3; skip those and continue to the newest unprocessed real episode.
- The latest live-site post may also already be processed (example: `DIP Ep 657: OMBRS 3-The OSHA Silica Standard` existed from the previous day). Iterate through real episode posts newest-to-oldest and choose the first whose title/link is not already present in `Daily-Sessions/`.

### Existing note multiplicity
- The same episode may have multiple notes across different dates (e.g., `2026-05-26-Episode-8-Heme-Drugs.md` and `2026-05-08-Heme-Drugs.md`). When a new Notion entry matches a previously-processed episode, check the most recent note for that title and only create a new note if the prior one was incomplete or needs a fresh pass.
- **Do not treat preview/log mentions as processed evidence.** Prior daily notes often include lines like `Tomorrow’s first unprocessed candidate appears to be DIP Ep 654...` or processing logs listing skipped candidates. When checking whether a live-site candidate is already processed, only count strong evidence: frontmatter `podcast_title`/`podcast`/`episode_url`/`link`, the main `#` title, `Source: [Episode page](exact URL)`, or exact episode URL in the primary episode metadata. Ignore `Evening Review Preview`, `Processing Log`, and generic body mentions unless corroborated by metadata. A prior run almost skipped `DIP Ep 654` because it appeared only as a tomorrow-preview in the `DIP Ep 655` note.
