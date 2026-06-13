# Live-site fallback and placeholder completion

Use this when the Notion database has no unprocessed rows but the live Divine Intervention podcast site has newer or already-queued episodes.

## Durable pattern

1. Query Notion first using the database workflow.
2. If Notion has no unprocessed episode, scrape `https://divineinterventionpodcasts.com/` or `https://divineinterventionpodcasts.com/category/podcast/` for recent `h1/h2.entry-title a` posts.
3. Skip promotional posts/classes; choose the latest podcast episode (`DIP Ep ...`, `OMBRS ...`, etc.).
4. Use a deterministic processed ID such as `live:<short-hash>` or the episode URL itself.
5. If the processed ID is already logged, do **not** immediately return `[SILENT]`:
   - Check `/root/Divine-Pharmacology/Audio/`, `Transcripts/`, and `Daily-Sessions/` for that episode.
   - If audio exists but transcript/note is a placeholder, continue the pipeline and replace the placeholder with a completed transcript/note.
6. Only return `[SILENT]` when there is no new episode **and** no incomplete placeholder/artifact to finish.

## CPU transcription finding

`faster_whisper` base on CPU/int8 can be viable for medium episodes. In one run, a 23-minute, ~21MB episode transcribed in ~390 seconds with:

```python
from faster_whisper import WhisperModel
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    audio_file,
    beam_size=5,
    language="en",
    initial_prompt="Divine Intervention Podcasts USMLE Step 2 Step 3 rapid review medicine pharmacology high yield.",
)
```

Set command timeouts to at least 600 seconds for this path before falling back to placeholders.