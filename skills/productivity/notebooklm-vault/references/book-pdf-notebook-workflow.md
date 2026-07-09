# Book/PDF → NotebookLM notebook workflow

Use this when JT asks to find a book/PDF online, upload it to NotebookLM, and make it chat-ready.

## Steps

1. **Find and validate the source**
   - Prefer official publisher/author/organization pages when available; otherwise use a stable direct PDF URL.
   - Download the PDF to `/tmp/<short-topic>/`.
   - Verify it is the requested book before upload: check page count and extract/search text for title, author, or a distinctive passage.

2. **Check NotebookLM auth**
   ```bash
   command -v notebooklm
   notebooklm auth check --test || notebooklm auth check
   notebooklm list
   ```
   If auth fails on a headless VPS, use `references/headless-vps-auth.md`.

3. **Create and activate the notebook**
   ```bash
   notebooklm create "<Book title — Author>" --use --json
   ```
   Save the notebook ID from JSON output.

4. **Upload the PDF**
   ```bash
   notebooklm source add /tmp/<short-topic>/<file>.pdf --title "<Book title> (PDF, <language>)" --json
   notebooklm source list --json
   ```
   Confirm the source is present, type is `pdf`, and status is `ready`.

5. **Verify indexing with a content question**
   - Ask a source-specific question whose answer should only come from the uploaded book.
   - Example:
     ```bash
     notebooklm ask "¿Cuál es la primera máxima del libro? Responde breve y cita si puedes."
     ```
   - Do not claim the notebook is ready until NotebookLM returns a grounded answer/citation or the source is otherwise clearly queryable.

6. **Report concisely**
   - Give: notebook title, notebook ID/link, source status, and the fact that a test question worked.
   - Mention sharing status if checked. If the notebook is restricted/private, say no public share link exists unless JT wants one enabled.

## Security cleanup

After browser-based auth succeeds, shut down temporary noVNC/Cloudflare/login browser processes used only for auth. Never expose Google tokens, NotebookLM cookies, or VNC/noVNC passwords in the final message; redact them as `[REDACTED]` if referenced.
