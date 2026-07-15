# NotebookLM YouTube batch ingestion

Use this when JT wants many YouTube videos added to NotebookLM, especially for study systems, polyglot-method research, or content packs.

## Proven CLI path

1. Verify auth/session:
   ```bash
   notebooklm auth check
   notebooklm list --json
   ```
2. Create or select a notebook:
   ```bash
   notebooklm create "Notebook Title" --json
   notebooklm use <notebook-id>
   ```
3. Add a short local Markdown source with JT's hypotheses/questions before the videos. This gives NotebookLM an explicit synthesis frame.
4. Add YouTube sources one at a time with a small delay:
   ```bash
   notebooklm source add --notebook <notebook-id> --type youtube "https://www.youtube.com/watch?v=..." --json
   sleep 2
   ```
5. Verify all sources are `ready`:
   ```bash
   notebooklm source list --notebook <notebook-id> --no-truncate
   ```
6. Ask a synthesis question through the notebook to verify chat-readiness:
   ```bash
   notebooklm ask --notebook <notebook-id> "Based only on these sources, synthesize the method and adapt it for JT."
   ```
7. Save the extracted synthesis back into Bitácora when the content becomes an operating system/project, so it is not trapped only in NotebookLM.

## Source selection lessons

- Prefer official channel RSS/feeds and YouTube oEmbed metadata over noisy web-search results when curating videos.
- Web search can return unrelated YouTube false positives. Confirm each candidate by title/author before adding.
- For method extraction, include both core method videos and app/tool comparison videos, plus a JT recall note capturing what the user remembers.

## Good final report

Tell JT: notebook title, notebook ID, number of sources added, readiness status, and the extracted practical method. Keep it concise and operational.