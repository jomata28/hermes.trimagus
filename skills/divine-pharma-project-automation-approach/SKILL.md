---
name: divine-pharma-project-automation-approach
description: Approach for automating Divine Intervention Pharmacology podcast processing into Obsidian notes using Notion, Whisper, and Hermes cron jobs
category: productivity
---

# Divine Intervention Pharmacology Project Automation Approach

This skill documents the approach and lessons learned for automating the Divine Intervention Pharmacology podcast processing pipeline. It captures the non-trivial workflow discovered through session history exploration and iterative implementation.

## Project Context

The user had an existing sophisticated Divine Pharmacology study system comprising:
- Obsidian vault: `Divine-Pharmacology/` with structured folders (Daily-Sessions, Drugs, Mechanisms, etc.)
- Notion database: `D.I. PHARM PODCASTS` (ID: `2f88c883-85ba-81ed-8d31-000b07f32c0e`)
- Existing skills in `/root/Gracvity-Claw/skills/`:
  - `devine-pharma-obsidian-bolt.md`: Vault structure and daily processing template
  - `pharma-cron-obsidian-link.md`: Cron schedule (9AM/2PM/7PM Houston CST) and delivery format

## Key Discoveries & Approach

### 1. Notion API Version Specifics
**Challenge**: Initial API queries failed due to using outdated endpoint assumptions.
**Discovery**: Notion API version 2025-09-03 uses:
- `/data_sources/{id}` endpoint (not `/databases/{id}`)
- `data_source_id` for querying, `database_id` for creating pages
**Solution**: Updated API calls to use `data_sources` endpoint with proper version header.

### 2. Integration with Existing Infrastructure
**Challenge**: User already had elaborate Obsidian bolt structure and processing expectations.
**Discovery**: The system expects:
- Daily notes in `Daily-Sessions/` folder with specific naming (`YYYY-MM-DD-Topic.md`)
- Frontmatter with date, podcast, time, duration, topic, usmle_weight
- Structured sections: Key Lessons, Mechanisms Explained, Drug Connections, Comprehension Questions, USMLE High-Yield Points, Evening Review
**Solution**: Built pipeline to conform to existing `devine-pharma-obsidian-bolt` template rather than creating new format.

### 3. Processing Pipeline Components
**Challenge**: Need to connect multiple systems reliably.
**Solution**: Created modular approach:
- **Fetch**: Notion API query for latest episode
- **Download**: Audio acquisition (with fallback for redirect handling)
- **Transcribe**: Whisper speech-to-text (configurable model size)
- **Extract**: Pharmacology insight extraction (pattern-based or LLM-enhanced)
- **Format**: Obsidian note generation using bolt template
- **Notify**: Telegram delivery with obsidian:// deep link
- **Track**: Processed episode ID logging to prevent duplicates

### 4. Cron Job Integration
**Challenge**: Aligning with user's preferred 7:00 AM CST schedule.
**Solution**: Created Hermes cron job with:
- Schedule: `0 7 * * *` (7:00 AM CST)
- Delivery: Telegram (user's primary communication platform)
- Skills: `divine-pharma-podcast-processing-pipeline`
- Model/Provider: Inherits from Hermes defaults for consistency

## Step-by-Step Implementation Approach

### Phase 1: Reconnaissance
1. Search session history for existing Divine Pharmacology references
2. Locate Notion database ID from past conversations
3. Examine existing skill files for vault structure and templates
4. Verify Notion API key availability in environment

### Phase 2: API Integration
1. Test Notion API connection with correct version header
2. Experiment with querying `data_sources` endpoint
3. Handle pagination and sorting (sort by Created time descending)
4. Extract episode metadata: title, link URL, topics, ID

### Phase 3: Audio Processing
1. Determine actual audio source (may require webpage scraping)
2. Implement robust download with retry and redirect handling
3. Configure Whisper transcription (base model for balance speed/accuracy)
4. Extract transcript to text file for processing

### Phase 4: Content Extraction
1. Initial approach: Pattern matching for key sections (lessons, mechanisms, etc.)
2. Enhancement option: LLM-based extraction for better accuracy
3. Focus on pharmaco-specific content: drug names, mechanisms, clinical vignettes
4. Generate USMLE-style high-yield points and comprehension questions

### Phase 5: Obsidian Integration
1. Format note according to `devine-pharma-obsidian-bolt` template
2. Include proper frontmatter with all required fields
3. Populate sections with extracted content
4. Save to `Daily-Sessions/` with date-based filename
5. Verify note creation and structure

### Phase 6: Automation & Notification
1. Implement duplicate processing prevention (ID tracking)
2. Create Telegram notification with obsidian:// deep link
3. Add error handling and logging
4. Package as executable script for cron execution
5. Schedule with Hermes cronjob tool

## Verification & Validation

**Success Criteria**:
1. New note appears daily in Obsidian vault under `Daily-Sessions/`
2. Note contains all required sections from bolt template
3. Episode metadata (title, date, time) is accurate
4. Telegram notification includes working obsidian:// link
5. Same episode not processed twice (ID tracking functional)
6. Audio downloaded and transcribed successfully

**Troubleshooting Points**:
- Notion API 400 errors: Check API version header and endpoint
- Audio download failures: Inspect actual podcast page for media URL
- Transcription issues: Adjust Whisper model size or audio quality
- Note format mismatches: Compare against bolt template specifications
- Duplicate processing: Verify ID tracking file is updated

## Customization Options

**For Different Workflows**:
- Adjust transcription model (tiny/base/small/medium/large) based on resources
- Modify extraction patterns to match host's speaking style
- Change delivery time in cron schedule (currently 7:00 AM CST)
- Add additional sections to note template if needed
- Integrate with other study systems (Anki, Notion, etc.)

**Enhancement Paths**:
1. Add LLM-based insight extraction for better accuracy
2. Implement audio duration calculation for frontmatter
3. Add cross-reference linking to existing drug/mechanism notes
4. Create weekly review notes summarizing multiple episodes
5. Add spaced repetition system integration for key facts

## Related Skills Created

1. `divine-pharma-notion-episodes-fetch`: Foundation for Notion database querying
2. `divine-pharma-podcast-processing-pipeline`: Complete end-to-end automation
3. Cron job: "Divine Pharma Daily Processing" (ID: 69aae56e9148)

## Lessons Learned

1. **Always verify API versions**: Notion's shift to data_sources broke initial assumptions
2. **Leverage existing infrastructure**: User's elaborate bolt system provided excellent template to follow
3. **Modular design wins**: Separating fetch, transcribe, extract, format phases made debugging easier
4. **Prevent duplicates**: Simple ID tracking is crucial for daily automation
5. **Meet users where they are**: Using Telegram for notifications aligned with their communication preference
6. **Respect existing conventions**: Conforming to bolt template ensured seamless integration

This approach successfully automates the user's request for daily Divine Intervention pharmacology notes while integrating seamlessly with their established study system.

---
*Skill created to document the non-trivial approach developed through session exploration, API experimentation, and iterative implementation of the Divine Intervention pharmacology podcast automation project.*