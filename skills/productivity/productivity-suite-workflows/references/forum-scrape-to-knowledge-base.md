# Forum scrape → Obsidian/NotebookLM knowledge base pattern

Use when the user wants to scrape a forum/community archive, organize it for future querying, and later upload to NotebookLM or use through Obsidian/Bitácora.

## Durable workflow

1. **Archive before synthesizing**
   - Save raw API/JSON per thread/post when available.
   - Save human-readable Markdown per thread.
   - Create a manifest with source URL, discussion/thread ID, title, author/post counts, timestamps, and local paths.
   - Redact credentials/secrets if encountered.

2. **Batch large forums deliberately**
   - Scrape in numbered batches (e.g. 10 or 50 at a time) so failures are recoverable.
   - Preserve the user's requested ordering (forum list order, IDs, or explicit selected links).
   - Build README/links files per batch so the user can inspect what was captured before NotebookLM upload.

3. **Build an access layer, not just files**
   - Add a `Wiki/00-Hub.md` entry point.
   - Add a source registry with canonical source URLs and local raw paths.
   - Add a topic index grouped by the user's actual questions.
   - Add focused synthesis notes for high-interest questions; keep claims grounded in links/post IDs and label speculation.

4. **Create a local full-text index**
   - SQLite FTS works well for future retrieval: discussions table + posts table + FTS virtual table over title/author/content/url.
   - Verify with counts and sample searches before reporting success.
   - Keep example query commands in the hub note so future agents can search without rediscovering schema.

5. **NotebookLM staging**
   - Create an upload-pack note listing the exact Markdown files to upload first.
   - Prioritize hub, source registry, topic index, synthesis notes, then core raw threads.
   - Check NotebookLM auth before attempting upload; if auth is expired, leave the local pack ready and report the blocker without treating it as a durable tool failure.

## Practical conventions for Bitácora

Suggested structure:

```text
3-Resources/<SourceName>/
  Raw/
    batch-001/
    batch-002/
    selected-YYYY-MM-DD/
  Index/
    <source>_posts.sqlite
  Wiki/
    00-Hub.md
    01-Source-Registry.md
    02-Topic-Index.md
    10-<question>.md
    20-NotebookLM-Upload-Pack.md
```

## Synthesis style

- Start with the direct answer.
- Separate: direct evidence, anecdote, theory/speculation, and safety cautions.
- Link to source posts/threads inline.
- For health/medical claims from forums, explicitly state that they are anecdotal/forum-based and not medical evidence.
- For user experiments, recommend low-risk tracking protocols rather than endorsing claims.

## Pitfalls

- Do not stop after scraping raw data; the user asked to “start talking to this data,” so build retrieval and synthesis notes.
- Do not upload to NotebookLM blindly; check auth and stage an upload pack first.
- Do not convert transient auth/setup failures into persistent negative claims about NotebookLM or tools.
- Do not create a one-off skill for a single scraped forum; keep this as a reusable forum/community knowledge-base pattern.
