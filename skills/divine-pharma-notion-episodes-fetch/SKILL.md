---
name: divine-pharma-notion-episodes-fetch
description: Fetches Divine Intervention Pharmacology podcast episodes from the Notion database for processing into Obsidian notes
category: productivity
---

# Fetching Divine Intervention Podcast Episodes from Notion

This skill provides a reusable approach to query the Divine Pharmacology Notion database for podcast episodes, extract audio links, and prepare them for processing (download, transcribe, extract pharm insights).

## Prerequisites

- NOTION_API_KEY set in ~/.hermes/.env
- Access to the "D.I. PHARM PODCASTS" database

## Database Information

- Database Name: `D.I. PHARM PODCASTS`
- Database ID: `2f88c883-85ba-81ed-8d31-000b07f32c0e` (from session history)
- Properties:
  - `Title`: Title of the podcast entry (e.g., "Ep. 6 - Pharm Cases")
  - `Link`: URL to the podcast episode
  - `Related Topic`: Multi-select (e.g., Pharmacology, Cases, GI, Heme, Immuno)

## Step-by-Step Approach

### 1. Query the Notion Database for Episodes

Use the notion skill to learn the curl pattern, then execute:

```bash
curl -s -X POST "https://api.notion.com/v1/data_sources/2f88c883-85ba-81ed-8d31-000b07f32c0e/query" \\
  -H "Authorization: Bearer $NOTION_API_KEY" \\
  -H "Notion-Version: 2025-09-03" \\
  -H "Content-Type: application/json" \\
  -d '{
    "page_size": 50,
    "sorts": [
      {
        "property": "Created time",
        "direction": "descending"
      }
    ]
  }'
```

**Note**: If sorting by "Created time" fails, try sorting by "Created time" without specifying the property name, or remove sorts to get latest entries first.

### 2. Extract Episode Information

From the response, for each result in `results` array:

- `id`: Page ID (can be used to get full content)
- `properties.Title.title[0].text.content`: Episode title (e.g., "Ep. 6 - Pharm Cases")
- `properties.Link.url`: Direct link to podcast episode
- `properties.Related Topic.multi_select`: Array of topic objects with `name` field

### 3. Get Most Recent Unprocessed Episode

Sort by `Created time` descending and take the first result that hasn't been processed yet. You may need to:

- Track processed episodes in a local file or Obsidian property
- Compare episode IDs or titles against your processing log

### 4. Prepare for Processing Pipeline

Once you have the episode link:

1. Download the audio (using wget, curl, or youtube-dl if YouTube)
2. Transcribe with Whisper: `whisper audio_file.mp3`
3. Extract pharmacology insights from transcript
4. Format according to Divine Pharmacology Obsidian Bolt template
5. Write to Obsidian vault under `Daily-Sessions/`

## Example Usage in Cron Job

For a 9:00 AM CST job that processes the latest episode:

```bash
0 9 * * * /path/to/pharma-9am.sh
```

Where `pharma-9am.sh` contains:

```bash
#!/bin/bash
# Fetch latest episode from Notion
EPISODE_JSON=$(curl -s -X POST "https://api.notion.com/v1/data_sources/2f88c883-85ba-81ed-8d31-000b07f32c0e/query" \\
  -H "Authorization: Bearer $NOTION_API_KEY" \\
  -H "Notion-Version: 2025-09-03" \\
  -H "Content-Type: application/json" \\
  -d '{"page_size": 1, "sorts": [{"property": "Created time", "direction": "descending"}]}')

EPISODE_URL=$(echo "$EPISODE_JSON" | jq -r '.results[0].properties.Link.url')
EPISODE_TITLE=$(echo "$EPISODE_JSON" | jq -r '.results[0].properties.Title.title[0].text.content')

# Download audio (example - adapt to actual source)
# wget -O "$EPISODE_TITLE.mp3" "$EPISODE_URL"

# Transcribe
# whisper "$EPISODE_TITLE.mp3" --output_format txt

# Process transcript to extract pharm insights
# (Implementation depends on desired output format)

# Write to Obsidian using template
# ...
```

## Notes & Pitfalls

- The Notion API uses `data_sources` endpoint (not `databases`) in version 2025-09-03
- Rate limit: ~3 requests/second - add delay if processing multiple episodes
- Some podcast links may redirect - you may need to follow redirects to get actual audio URL
- Consider checking if episode was already processed by tracking IDs in a local file
- The Divine Pharmacology Obsidian Bolt expects specific frontmatter and sections in the notes

## Verification

After running, verify:

1. New note appears in Obsidian vault under `Daily-Sessions/`
2. Note contains:
   - Key lessons from episode
   - Mechanisms explained
   - Drug connections
   - Comprehension questions
   - USMLE high-yield points
   - Evening review preview
3. Note has proper frontmatter with date, podcast title, time, etc.

## Related Skills

- `devine-pharma-obsidian-bolt`: Defines the Obsidian vault structure and note template
- `pharma-cron-obsidian-link`: Defines the cron schedule and delivery format
- `whisper`: For audio transcription
- `obsidian`: For creating/updating Obsidian notes

## Example Output

After processing Ep. 6 - Pharm Cases, you would have a note like:

```markdown
---
date: 2026-04-16
podcast: Ep. 6 - Pharm Cases
time: 07:00
duration: 20:00
topic: Pharmacology Cases
usmle_weight: High
---

# Ep. 6 - Pharm Cases

## Key Lessons
- Cimetidine causes gynecomastia via anti-androgen effects
- Lindane poisoning presents with seizures due to GABA antagonism
- ...

## Mechanisms Explained
- ...

## Drug Connections
### New Drugs
- Cimetidine (H2 blocker)
- Lindane (scabicide)
- ...

## Comprehension Questions
- A patient presents with ... What is the likely cause?
- ...

## USMLE High-Yield Points
- ...

## Evening Review
- Preview of tomorrow's topic: Renal Pharmacology
- ...
```