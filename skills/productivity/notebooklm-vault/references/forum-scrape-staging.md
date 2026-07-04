# Forum scrape staging for NotebookLM

Use when a user wants to "talk to" a web forum or discussion corpus in NotebookLM, especially when the forum is Flarum-based.

## Workflow

1. Scrape into the user's vault first; do **not** upload to NotebookLM until the user confirms the batch.
2. Batch discussions in small reviewable chunks, usually 10 discussions at a time.
3. Preserve both:
   - readable Markdown files for NotebookLM/source review
   - raw JSON files for audit/reprocessing
4. Create a `README.md` and `manifest.json` per batch with source URLs, discussion IDs, titles, post counts, and output paths.
5. After scrape, verify file count, byte size, and line count before reporting success.
6. Only then check NotebookLM auth and upload status.

## Flarum extraction pattern

Flarum forums expose JSON API endpoints even when browser rendering is slow:

- List discussions: `GET /api/discussions?page[limit]=10&page[offset]=N`
- Discussion metadata: `GET /api/discussions/{discussion_id}`
- Posts for a discussion: `GET /api/posts?filter[discussion]={id}&page[limit]=50&page[offset]=N`

Use headers like:

```text
User-Agent: Hermes archival scraper for personal NotebookLM ingestion
Accept: application/vnd.api+json, application/json
```

`contentHtml` appears in post attributes. Convert it to Markdown, preserving:

- post number
- author/display name
- created/edited timestamps
- permalink
- embedded image URLs
- links
- blockquotes/code where possible

## Suggested vault layout

```text
3-Resources/<CorpusName>/Raw/batch-001/
  README.md
  manifest.json
  01-<discussion-id>-<slug>.md
  01-<discussion-id>-<slug>.json
  ...
```

For the user's Wizard Talk corpus, use:

```text
/root/obsidian-vault/3-Resources/WizardTalk/Raw/batch-XXX/
```

## Pitfalls

- Do not rely on browser automation for Flarum if direct API calls work; browser navigation can time out while API calls succeed.
- Do not claim NotebookLM upload readiness until `notebooklm auth check` and `notebooklm list` both work. Cookie presence alone may pass while `list` still redirects to Google login.
- Avoid treating transient auth/setup failures as durable limitations. Report the current auth state and offer the re-auth flow.
