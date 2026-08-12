# Video-only episode fallback

Use this when a real Divine Intervention episode page contains an embedded YouTube mini-lecture but no MP3. This is a supported episode type, not a failed podcast scrape.

## Detection

1. Confirm the page is a real episode using the normal title/URL filters and strong processed matching.
2. Search the page HTML for a YouTube embed/watch URL, including forms such as:
   - `https://www.youtube.com/embed/VIDEO_ID?...`
   - `https://youtu.be/VIDEO_ID`
   - `https://www.youtube.com/watch?v=VIDEO_ID`
3. Normalize it to `https://www.youtube.com/watch?v=VIDEO_ID`.
4. Capture any worksheet/download link from the episode page and include it in the study note.

## Transcript retrieval

Prefer existing YouTube captions over a new Whisper pass:

```bash
uvx yt-dlp \
  --write-auto-subs --write-subs \
  --sub-langs 'en.*' --sub-format vtt \
  --skip-download \
  -o '/tmp/divine-video.%(ext)s' \
  'https://www.youtube.com/watch?v=VIDEO_ID'
```

Get verified metadata separately:

```bash
uvx yt-dlp --skip-download \
  --print '%(title)s' --print '%(duration)s' --print '%(webpage_url)s' \
  'https://www.youtube.com/watch?v=VIDEO_ID'
```

Do not require the media download if captions are complete. YouTube may permit caption retrieval while requiring authentication for audio/video download.

## Cleaning rolling VTT captions

YouTube auto-caption VTT commonly repeats rolling windows. The useful incremental text is generally on payload lines containing inline timestamp tags such as `<00:00:03.440>`. To clean it:

1. Ignore `WEBVTT`, cue timing lines, blank lines, and payload lines without inline timestamp tags.
2. Keep payload lines containing inline timestamp tags.
3. Strip all `<...>` tags and HTML-unescape the text.
4. Join whitespace and split into readable sentences/paragraphs.
5. Store this machine transcript under `Transcripts/`; explicitly label it as auto-generated and potentially noisy.

Verify the beginning and end of the saved transcript so a partial caption download is not reported as complete.

## Study-note handling

- Treat a complete caption transcript as successful transcription: for example, `transcription_status: completed_from_youtube_auto_captions`.
- Use `processing_status: completed_youtube_auto_transcript` after the Daily-Session synthesis is written.
- Include episode page, normalized YouTube URL, worksheet URL when present, duration, transcript link, and stable processed ID in frontmatter.
- Correct obvious caption errors in the Daily-Session note while preserving the raw cleaned machine transcript separately.
- Build the normal class-level outputs: key lessons, mechanisms, drug/system connections, USMLE corrections, 3–5 comprehension questions, and evening review preview.
- For physiology/toxicology episodes, distinguish source teaching from clinically important nuance (for example, measured PaO2 versus pulse oximetry/co-oximetry).

## Processed markers and verification

After both notes are successfully written:

1. Append the stable `live:<sha256(page_url)[:16]>` marker and exact episode URL to `~/.divine_pharma_processed`.
2. Read back the Daily-Session note and transcript note.
3. Confirm both processed markers are present.
4. Return the exact Obsidian URI for the actual note filename.

Do not mark the episode processed before the note and transcript exist.