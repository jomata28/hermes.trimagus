---
name: divine-pharma-podcast-processing-pipeline
description: Complete pipeline to fetch Divine Intervention podcast, transcribe, extract pharmacology insights, and create Obsidian notes
category: productivity
---

# Divine Intervention Podcast Processing Pipeline

This skill provides a complete reusable approach to automatically process Divine Intervention Pharmacology podcast episodes into structured Obsidian notes for USMLE-style study.

## Overview

Daily workflow:
1. Fetch latest episode from Notion database
2. Download podcast audio
3. Transcribe audio to text using Whisper
4. Extract pharmacology insights (key lessons, mechanisms, drug connections, comprehension questions, USMLE points)
5. Format note using Divine Pharmacology Obsidian Bolt template
6. Write note to Obsidian vault
7. Send notification with Obsidian deep link

## Prerequisites

- NOTION_API_KEY set in ~/.hermes/.env
- WHISPER_MODEL_PATH or access to Whisper for transcription
- Obsidian vault configured at ~/Documents/Obsidian/Divine-Pharmacology/ (or similar)
- Required tools: curl, wget, jq (for JSON processing)
- Python packages: faster-whisper (pip install faster-whisper)

## Step-by-Step Pipeline

### Step 1: Fetch Latest Unprocessed Episode from Notion

Fetch multiple episodes and find the first one that hasn't been processed yet:

```bash
# Fetch multiple episodes to check for unprocessed ones
EPISODE_DATA=$(curl -s -X POST "https://api.notion.com/v1/data_sources/2f88c883-85ba-81ed-8d31-000b07f32c0e/query" \\
  -H "Authorization: Bearer $NOTION_API_KEY" \\
  -H "Notion-Version: 2025-09-03" \\
  -H "Content-Type: application/json" \\
  -d '{"page_size": 20}')

# Get processed IDs from log
PROCESSED_LOG="$HOME/.divine_pharma_processed"
if [ -f "$PROCESSED_LOG" ]; then
    PROCESSED_IDS=$(cat "$PROCESSED_LOG" | sort -u | tr '\\n' '|' | sed 's/|$//')
else
    PROCESSED_IDS=""
fi

# Find first unprocessed episode
EPISODE_COUNT=$(echo "$EPISODE_DATA" | jq '.results | length')
FOUND_UNPROCESSED=false

for i in $(seq 0 $((EPISODE_COUNT - 1))); do
    EPISODE_ID=$(echo "$EPISODE_DATA" | jq -r ".results[$i].id")
    EPISODE_TITLE=$(echo "$EPISODE_DATA" | jq -r ".results[$i].properties.Title.title[0].text.content")
    EPISODE_URL=$(echo "$EPISODE_DATA" | jq -r ".results[$i].properties.Link.url")
    
    # Trim whitespace
    EPISODE_URL=$(echo "$EPISODE_URL" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    EPISODE_TITLE=$(echo "$EPISODE_TITLE" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    
    # Skip if already processed
    if echo "$PROCESSED_IDS" | grep -q "$EPISODE_ID"; then
        continue
    fi
    
    # Found unprocessed episode
    FOUND_UNPROCESSED=true
    break
done

if [ "$FOUND_UNPROCESSED" = false ]; then
    echo "No new episodes to process"
    exit 0
fi

# Trim whitespace one more time for safety
EPISODE_URL=$(echo "$EPISODE_URL" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
EPISODE_TITLE=$(echo "$EPISODE_TITLE" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
```

### Step 2: Download Audio

For Divine Intervention podcast, scrape the webpage to find the MP3 URL with multiple fallback patterns:

```bash
# Create safe filename
SAFE_TITLE=$(echo "$EPISODE_TITLE" | tr '[:space:]' '_' | tr -cd '[:alnum:]_.-')
AUDIO_FILE="/tmp/${SAFE_TITLE}.mp3"

# Scrape the webpage for audio URL with robust extraction
echo "Scraping webpage for audio URL..."
PAGE=$(curl -s "$EPISODE_URL")
# Try multiple patterns to find the MP3 URL
AUDIO_URL=$(echo "$PAGE" | sed -n 's/.*<a[^>]*href="\(https:\/\/divineinterventionpodcasts.com\/wp-content\/uploads\/[^"]*\.mp3\)".*/\1/p' | head -1)
if [ -z "$AUDIO_URL" ]; then
    # Try the source tag
    AUDIO_URL=$(echo "$PAGE" | sed -n 's/.*<source[^>]*src="\(https:\/\/divineinterventionpodcasts.com\/wp-content\/uploads\/[^"]*\.mp3\)".*/\1/p' | head -1)
fi
if [ -z "$AUDIO_URL" ]; then
    # Try direct grep patterns as fallback
    AUDIO_URL=$(echo "$PAGE" | grep -o 'https://divineinterventionpodcasts.com/wp-content/uploads/[^"]*\\.mp3' | head -1)
fi
if [ -z "$AUDIO_URL" ]; then
    # Try any mp3 URL in quotes
    AUDIO_URL=$(echo "$PAGE" | grep -o 'https?://[^"'\'']*\\.mp3' | head -1)
fi

# Remove any query parameters for cleaner URL (e.g., ?_=1)
AUDIO_URL=$(echo "$AUDIO_URL" | cut -d'?' -f1)

if [ -z "$AUDIO_URL" ]; then
    echo "ERROR: Could not find audio URL on page"
    # Save page for debugging (optional)
    # curl -s "$EPISODE_URL" > "/tmp/${SAFE_TITLE}_debug.html"
    exit 1
fi

echo "Found audio URL: $AUDIO_URL"

# Download the audio
if wget -O "$AUDIO_FILE" "$AUDIO_URL" --quiet --show-progress; then
    echo "Download successful"
else
    echo "ERROR: Failed to download audio"
    exit 1
fi
```

### Step 3: Transcribe with Faster Whisper

Use faster_whisper directly to avoid ffmpeg compatibility issues:

```bash
TRANSCRIPT_FILE="/tmp/${SAFE_TITLE}.txt"
# Use faster_whisper via Python
python3 - << EOF
import sys
sys.path.insert(0, '/root/.hermes/hermes-agent/venv/lib/python3.11/site-packages')
from faster_whisper import WhisperModel
# Use base model for balance of speed/accuracy, or tiny for faster processing
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe("$AUDIO_FILE", beam_size=5)
transcript = ""
for segment in segments:
    transcript += segment.text + " "
with open("$TRANSCRIPT_FILE", "w") as f:
    f.write(transcript.strip())
EOF

# Verify transcript
if [ ! -f "$TRANSCRIPT_FILE" ] || [ ! -s "$TRANSCRIPT_FILE" ]; then
    echo "WARNING: Transcription failed or empty, creating placeholder"
    echo "[Transcription failed - please manually process this episode]" > "$TRANSCRIPT_FILE"
fi
```

### Step 4: Extract Pharmacology Insights

Process transcript to extract structured information. The extraction is simplified for automation:

```bash
# Extract insights using grep patterns (can be enhanced based on actual transcript format)
KEY_LESSONS=$(grep -i "key point\|lesson\|important" "$TRANSCRIPT_FILE" | head -5 || echo "Key lessons to be extracted")
MECHANISMS=$(grep -i "mechanism\|pathway\|how it works" "$TRANSCRIPT_FILE" | head -5 || echo "Mechanisms to be extracted")
QUESTIONS=$(grep -i "question\|what is\|which\|why" "$TRANSCRIPT_FILE" | head -3 || echo "Comprehension questions to be extracted")
USMLE_POINTS=$(grep -i "high yield\|usmle\|important\|remember" "$TRANSCRIPT_FILE" | head -5 || echo "USMLE high-yield points to be extracted")
```

### Step 5: Format Obsidian Note

Create note using the Divine Pharmacology Bolt template:

```bash
NOTE_DATE=$(date +%Y-%m-%d)
NOTE_TIME=$(date +%H:%M)
NOTE_PATH="$HOME/Documents/Obsidian/Divine-Pharmacology/Daily-Sessions/${NOTE_DATE}-${SAFE_TITLE}.md"

cat > "$NOTE_PATH" << EOF
---
date: $NOTE_DATE
podcast: $EPISODE_TITLE
time: $NOTE_TIME
duration: $(get_audio_duration "$AUDIO_FILE")  # Implement duration extraction
topic: $(echo "$EPISODE_TOPICS" | jq -r '. | join(", ")')
usmle_weight: High
---

# $EPISODE_TITLE

## Key Lessons
$KEY_LESSONS

## Mechanisms Explained
$MECHANISMS

## Drug Connections
### New Drugs
$NEW_DRUGS

### System Connections
$SYSTEM_RELATIONSHIPS

### Previous Drug Links
$PREVIOUS_DRUG_LINKS

## Comprehension Questions
$QUESTIONS

## USMLE High-Yield Points
$USMLE_POINTS

## Evening Review
$EVENING_SUMMARY
EOF
```

### Step 6: Verify and Notify

```bash
# Verify note was created
if [ -f "$NOTE_PATH" ]; then
    # Send Telegram notification with Obsidian deep link
    OBSIDIAN_URL="obsidian://open?vault=Divine-Pharmacology&file=Daily-Sessions/${NOTE_DATE}-${SAFE_TITLE}.md"
    send_message telegram "📚 Daily Pharmacology Note Ready\n\n$EPISODE_TITLE\n[Open in Obsidian Bolt]($OBSIDIAN_URL)"
else
    send_message telegram "❌ Failed to create pharmacology note for $EPISODE_TITLE"
fi
```

## Complete Cron Job Example (7:00 AM CST)

Create `/usr/local/bin/divine-pharma-daily.sh`:

```bash
#!/bin/bash
set -euo pipefail

# Load environment
source "$HOME/.hermes/.env"

# Temporary directory for processing
WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT

# Step 1: Fetch episode
EPISODE_DATA=$(curl -s -X POST "https://api.notion.com/v1/data_sources/2f88c883-85ba-81ed-8d31-000b07f32c0e/query" \\
  -H "Authorization: Bearer $NOTION_API_KEY" \\
  -H "Notion-Version: 2025-09-03" \\
  -H "Content-Type: application/json" \\
  -d '{"page_size": 1}')

# If sorting fails, remove the sorts parameter
# EPISODE_DATA=$(curl -s -X POST "https://api.notion.com/v1/data_sources/2f88c883-85ba-81ed-8d31-000b07f32c0e/query" \\
#   -H "Authorization: Bearer $NOTION_API_KEY" \\
#   -H "Notion-Version: 2025-09-03" \\
#   -H "Content-Type: application/json" \\
#   -d '{"page_size": 1, "sorts": [{"property": "Created time", "direction": "descending"}]}')

EPISODE_URL=$(echo "$EPISODE_DATA" | jq -r '.results[0].properties.Link.url')
EPISODE_TITLE=$(echo "$EPISODE_DATA" | jq -r '.results[0].properties.Title.title[0].text.content')
EPISODE_ID=$(echo "$EPISODE_DATA" | jq -r '.results[0].id')

# Skip if already processed (simple ID tracking)
PROCESSED_LOG="$HOME/.divine_pharma_processed"
if grep -q "$EPISODE_ID" "$PROCESSED_LOG"; then
    echo "Episode $EPISODE_TITLE already processed"
    exit 0
fi

# Step 2: Download audio
SAFE_TITLE=$(echo "$EPISODE_TITLE" | tr '[:space:]' '_' | tr -cd '[:alnum:]_-.')
AUDIO_FILE="$WORK_DIR/${SAFE_TITLE}.mp3"
echo "Downloading: $EPISODE_TITLE"
wget -O "$AUDIO_FILE" "$EPISODE_URL" --quiet --show-progress

# Step 3: Transcribe
echo "Transcribing..."
# Try whisper command first with timeout, fall back to faster_whisper via Python
if command -v whisper >/dev/null 2>&1; then
    # Try whisper with timeout (adjust based on episode length)
    timeout 120 whisper "$AUDIO_FILE" --model base --output_format txt --output_dir "$WORK_DIR" || \
    echo "Whisper transcription timed out or failed, falling back to faster_whisper"
fi

# Check if transcription succeeded, otherwise use faster_whisper fallback
if [ ! -f "$WORK_DIR/${SAFE_TITLE}.txt" ] || [ ! -s "$WORK_DIR/${SAFE_TITLE}.txt" ]; then
    # Fallback to faster_whisper via Python
    python3 - << EOF
import sys
sys.path.insert(0, '/root/.hermes/hermes-agent/venv/lib/python3.11/site-packages')
from faster_whisper import WhisperModel
# Use base model for balance of speed/accuracy, or tiny for faster processing
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe("$AUDIO_FILE", beam_size=5)
transcript = ""
for segment in segments:
    transcript += segment.text + " "
with open("$WORK_DIR/${SAFE_TITLE}.txt", "w") as f:
    f.write(transcript.strip())
EOF
fi
TRANSCRIPT_FILE="$WORK_DIR/${SAFE_TITLE}.txt"
# For longer episodes (>15 min), consider using --model tiny or processing in chunks

# Step 4: Extract insights (simplified - enhance as needed)
KEY_LESSONS=$(grep -i "key point\|lesson" "$TRANSCRIPT_FILE" | head -10 || echo "Extract key lessons from transcript")
MECHANISMS=$(grep -i "mechanism\|pathway" "$TRANSCRIPT_FILE" | head -10 || echo "Extract mechanisms from transcript")
QUESTIONS=$(grep -i "question\|what is\|which" "$TRANSCRIPT_FILE" | head -5 || echo "Generate comprehension questions")
USMLE_POINTS=$(grep -i "high yield\|usmle\|important" "$TRANSCRIPT_FILE" | head -10 || echo "Identify USMLE high-yield points")

# Step 5: Create Obsidian note
NOTE_DATE=$(date +%Y-%m-%d)
NOTE_TIME=$(date +%H:%M)
OBSIDIAN_VAULT="$HOME/Documents/Obsidian/Divine-Pharmacology"
NOTE_PATH="$OBSIDIAN_VAULT/Daily-Sessions/${NOTE_DATE}-${SAFE_TITLE}.md"

mkdir -p "$OBSIDIAN_VAULT/Daily-Sessions"

cat > "$NOTE_PATH" << EOF
---
date: $NOTE_DATE
podcast: $EPISODE_TITLE
time: $NOTE_TIME
duration: 0  # TODO: Implement actual duration extraction
topic: Pharmacology
usmle_weight: High
---

# $EPISODE_TITLE

## Key Lessons
$KEY_LESSONS

## Mechanisms Explained
$MECHANISMS

## Drug Connections
### New Drugs
To be extracted from transcript

### System Connections
To be extracted from transcript

### Previous Drug Links
To be extracted from transcript

## Comprehension Questions
$QUESTIONS

## USMLE High-Yield Points
$USMLE_POINTS

## Evening Review
Review connections and preview tomorrow's topic
EOF

# Step 6: Mark as processed and notify
echo "$EPISODE_ID" >> "$PROCESSED_LOG"
OBSIDIAN_URL="obsidian://open?vault=Divine-Pharmacology&file=Daily-Sessions/${NOTE_DATE}-${SAFE_TITLE}.md"

# Send Telegram notification if credentials are available
if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
    send_message telegram "📚 Daily Pharmacology Note Ready\n\n$EPISODE_TITLE\n[Open in Obsidian Bolt]($OBSIDIAN_URL)"
fi
```

Make executable and schedule:
```bash
chmod +x /usr/local/bin/divine-pharma-daily.sh
# Cron job for 7:00 AM CST
(crontab -l 2>/dev/null; echo "0 7 * * * /usr/local/bin/divine-pharma-daily.sh") | crontab -
```

## Notes & Pitfalls

Reference: see `references/live-site-placeholder-completion.md` for the live-site fallback and the rule to complete existing placeholder notes/audio before returning `[SILENT]`.

- **Audio Source**: Divine Intervention podcast may require scraping the webpage for actual MP3 URL - inspect network tab when playing episode
- **URL Handling**: Notion API may return URLs with trailing whitespace that breaks wget/curl. Always trim whitespace: `EPISODE_URL=$(echo "$EPISODE_URL" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')`
- **Audio Download Strategy**: 
  1. Try direct download first
  2. If returns HTML, scrape webpage for MP3 URL using patterns like:
     - `https://divineinterventionpodcasts.com/wp-content/uploads/.*\\.mp3`
     - `https?://[^\"']*\\.mp3` (within quotes)
     - Check `<audio>` and `<source>` tags
  3. Use wget with `--show-progress` for large files
- **Transcription Quality & Timing**: Whisper base model can timeout on longer episodes (>20 min), but do not skip transcription solely because no GPU is present. In this environment, `faster_whisper` base on CPU/int8 successfully transcribed a 23-minute, 21MB episode in ~390 seconds. Consider:
  - Using `faster_whisper` with `WhisperModel("base", device="cpu", compute_type="int8")` as the default CPU path
  - Setting foreground command timeouts to at least 600 seconds for ~20-25 minute episodes
  - Using `--model tiny` or chunks only when base CPU exceeds the cron window
  - If a previous cron run created a placeholder note/transcript and downloaded audio, treat the next run as an opportunity to complete the transcript and replace the placeholder rather than reporting nothing
  - If transcription truly fails, create a clearly marked placeholder note and leave the audio path for follow-up
- **Insight Extraction**: The grep-based extraction is simplistic - for production use consider:
  - Fine-tuning a model on pharmacology text
  - Using few-shot prompting with examples
  - Implementing rule-based extraction for known patterns (drug names, mechanisms)
- **Duplicate Processing**: Tracking processed episodes by ID prevents re-processing same episode
- **Error Handling**: Production script should include more robust error checking and logging, including timeout handling for transcription
- **Vault Location**: Adjust Obsidian vault path to match actual setup (in this environment: `/root/Divine-Pharmacology`)
- **Timing**: 7:00 AM CST = 13:00 UTC (adjust cron if server is in different timezone)
- **Dependencies**: Ensure whisper, wget, curl, jq are installed
- **Notion API Sorting**: The sort property "Created time" may not be valid in version 2025-09-03; if you get a validation error, try removing the sorts parameter or using the correct property ID from the database schema
- **Database staleness / live-site fallback**: The Notion database can lag behind the live Divine Intervention site or contain only already processed entries. If no unprocessed Notion rows are found, scrape `https://divineinterventionpodcasts.com/` or `/category/podcast/` for the latest `DIP Ep ...` post, extract its MP3, and process it with a `live:<hash>` processed ID. Before returning `[SILENT]`, check whether the latest live-site episode already has downloaded audio or a placeholder note in `/root/Divine-Pharmacology`; if so, complete the transcript and replace the placeholder note instead of doing nothing.
- **Whisper Availability**: The whisper command may not be installed; faster_whisper via Python (pip install faster-whisper) is a reliable alternative
- **Audio URL Extraction**: MP3 URLs are often embedded in <audio> tags or <source> elements on the podcast webpage; use regex patterns like 'https?://[^\\s\"\\'>]*\\.mp3' to extract them. For Divine Intervention specifically, look in wp-content/uploads directory.
- **Temporary Directory Cleanup**: Due to recursive delete protection in some environments, avoid using `rm -rf` on paths that could be ambiguous. Instead:
  - Use explicit file deletion: `rm -f \"$AUDIO_FILE\" \"$TRANSCRIPT_FILE\"`
  - Remove directories only when confirmed empty: `if [ -d \"$WORK_DIR\" ] && [ -z \"$(ls -A \"$WORK_DIR\")\" ]; then rmdir \"$WORK_DIR\"; fi`
  - Or use unique per-episode directories: `WORK_DIR=\"/tmp/divine_pharma_${EPISODE_ID}\"` and clean only that specific directory
- **Telegram Notifications**: Requires both TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to be set in ~/.hermes/.env
- **Processed ID Tracking**: The processed log may contain duplicate entries - consider using `sort -u` when reading or ensuring deduplication when writing
- **Existing Audio Files**: Check for pre-downloaded audio files in the vault before attempting to download (saves time and bandwidth)
- **Debugging Notion Responses**: Use `jq` to inspect the full response structure when fields appear missing: `echo "$EPISODE_DATA" | jq '.results[0].properties'`

## Verification Checklist

After running the pipeline, verify:
1. New note appears in Obsidian vault under correct date naming
2. Note contains all required sections from the bolt template
3. Episode title, date, time are correct in frontmatter
4. Telegram notification arrives with working obsidian:// link
5. Processed episode ID is logged to prevent duplicates
6. Audio file was downloaded and transcribed successfully

## Related Skills

- `divine-pharma-notion-episodes-fetch`: Foundation for fetching episodes from Notion
- `whisper`: Audio transcription
- `obsidian`: Creating/updating Obsidian notes
- `cronjob`: Scheduling the daily pipeline
- `send_message`: Telegram notifications

## Example Output

After processing Ep. 6 - Pharm Cases with transcription timeout, note contains:

```markdown
---\ndate: 2026-04-26\npodcast: Ep. 6 - Pharm Cases\ntime: 07:00\nduration: 0\ntopic: Pharmacology\nusmle_weight: High\n---\n\n# Ep. 6 - Pharm Cases\n\n## Key Lessons\n[Transcription timed out - please manually process this episode]\n\n## Mechanisms Explained\n[To be filled]\n\n## Drug Connections\n### New Drugs\nTo be extracted from transcript\n\n### System Connections\nTo be extracted from transcript\n\n### Previous Drug Links\nTo be extracted from transcript\n\n## Comprehension Questions\n[To be filled]\n\n## USMLE High-Yield Points\n[To be filled]\n\n## Evening Review Preview\nReview connections and preview tomorrow's topic
```

When transcription succeeds, the note would contain detailed pharmacological insights as shown in the original example.

---
*Skill created based on session history exploration and implementation of Divine Pharmacology project infrastructure. Combines lessons learned from Notion API querying, audio processing, and Obsidian integration patterns observed in user's existing setup.*