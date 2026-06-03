---
name: notion-audio-processing-with-fallbacks
description: Robust approach to querying Notion databases for podcast episodes and processing audio with fallback mechanisms for transcription
version: 1.0.0
author: REDACTED
category: productivity
---

# Notion Audio Processing with Fallbacks

This skill provides a robust approach to querying Notion databases for podcast episodes and processing audio with fallback mechanisms for transcription.

## When to Use

Use this skill when you need to:
- Query a Notion database for the latest entry (e.g., podcast episodes)
- Download and transcribe audio content
- Handle situations where primary methods fail or are too slow
- Process content with automatic fallback to faster alternatives

## Limitations

- Assumes Notion database has Title (title type) and Link (url type) properties
- Requires OPENAI_API_KEY for Whisper transcription to work
- The tiny Whisper model is faster but less accurate than larger models
- Date extraction relies on URLs containing YYYY/MM/DD patterns

## Prerequisites

- NOTION_API_KEY environment variable set
- OPENAI_API_KEY environment variable set (for Whisper)
- Whisper installed and available in PATH
- wget or curl available for downloading

## Step-by-Step

### 1. Query Notion Database for Latest Entry

```bash
# Query Notion database and sort by creation time (newest first)
NOTION_API_KEY=REDACTED
DATABASE_ID=your_database_id_here

curl -s -X POST "https://api.notion.com/v1/databases/$DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  --data '{"page_size": 100, "sorts": [{"property": "created_time", "direction": "descending"}]}'
```

**Note**: If sorting by `created_time` fails validation, fall back to:
1. Query without sorting
2. Extract dates from URLs using regex pattern `/(\d{4})/(\d{2})/(\d{2})/`
3. Sort by extracted date

### 2. Extract Episode Information

From the Notion response, extract:
- Title: From `properties.Title.title[0].plain_text`
- URL: From `properties.Link.url`
- ID: From `id` field
- Date: Extract from URL using regex `/(\d{4})/(\d{2})/(\d{2})/` or use `created_time`

### 3. Download Audio File

```bash
# Create temporary directory
mkdir -p /tmp/podcast_processing
cd /tmp/podcast_processing

# Download MP3 (adjust URL pattern as needed)
wget -q "$AUDIO_URL" -O episode.mp3
# Or if wget not available:
# curl -s "$AUDIO_URL" -o episode.mp3
```

### 4. Transcribe with Fallback Strategy

```bash
# Try high-quality model first (may be slow)
whisper episode.mp3 --model large-v2 --output_format txt --output_dir . &
WHISPER_PID=$!

# Wait for a reasonable time (e.g., 60 seconds)
if ! timeout 60 bash -c "while kill -0 $WHISPER_PID 2>/dev/null; do sleep 1; done"; then
  # Timeout reached, kill the process and fall back
  kill $WHISPER_PID 2>/dev/null || true
  wait $WHISPER_PID 2>/dev/null || true
  
  # Fall back to faster, smaller model
  whisper episode.mp3 --model tiny --output_format txt --output_dir .
fi
```

### 5. Process Transcription

After transcription completes, you'll have `episode.txt` which can be:
- Sent to an LLM for pharmacological insight extraction
- Used to generate study notes
- Processed for key concepts and mechanisms

### 6. Clean Up

Remove temporary files when done:
```bash
rm -rf /tmp/podcast_processing
```

## Error Handling

- If Notion query fails, check API key and database ID
- If audio download fails, verify URL accessibility
- If transcription fails completely, consider using just the episode metadata
- Always check file existence before proceeding to next step

## Verification

After processing, verify:
1. Audio file downloaded successfully (`episode.mp3` exists)
2. Transcription file created (`episode.txt` exists and has content)
3. File sizes are reasonable (transcription should be much smaller than audio)
4. Content looks like proper transcription (not just error messages)

## Customization

- Adjust `page_size` in Notion query based on expected database size
- Change Whisper model (`tiny`, `base`, `small`, `medium`, `large`, `large-v2`, `large-v3`) based on speed/accuracy needs
- Modify output formats as needed (`txt`, `json`, `srt`, `vtt`)
- Adjust timeout values based on expected processing time and model size

## Example Workflow

This approach was successfully used to:
1. Query the D.I. PHARM PODCASTS Notion database
2. Identify "Ep. 10 - GI Drugs" from March 24, 2018
3. Download the corresponding MP3 file
4. Initiate transcription with fallback from large-v2 to tiny model
5. (Would continue to LLM processing and Obsidian note creation)

The key innovation is the proactive fallback mechanism that prevents getting stuck on slow processes while still attempting to get the best possible result within time constraints.