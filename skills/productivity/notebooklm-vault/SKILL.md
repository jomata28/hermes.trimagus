---
name: notebooklm-vault
description: "NotebookLM: query, add to, generate from, and download NotebookLM artifacts. Sourced from the user's Bitácora vault."
version: 1.0.0
author: Bitácora / C.T. Gravy
license: MIT
---

# Skill: NotebookLM

NotebookLM access is expected to be via a `notebooklm` CLI when installed, but this environment may not currently have the command available. Always verify with `command -v notebooklm` and `notebooklm auth check` before claiming access.

## When to use

Reach for this skill when the user wants to:
- Query their own sources with cited answers
- Add a URL / PDF / YouTube / file to a notebook
- Generate a podcast, video, slide deck, infographic, report, mind map, quiz, flashcards, or data table
- Download any of the above
- Run a web-research session into a notebook

For NotebookLM, always use CLI first, not browser:
- `notebooklm auth check`
- `notebooklm list`

## Workflow shape

For web/forum corpora that need to become NotebookLM sources, stage the scrape into the vault first and batch it for confirmation before upload. See `references/forum-scrape-staging.md` for the Flarum/forum pattern, including the 10-discussion batching workflow and Markdown+JSON output shape.

For a requested book/PDF found online, use `references/book-pdf-notebook-workflow.md`: download and validate the PDF, create a new notebook, upload the PDF, verify source status is `ready`, then ask a content-specific question before telling JT it is chat-ready.

For bulk YouTube ingestion, do not default to browser-extension automation if the CLI is authenticated. Accept a playlist/channel/course page/pasted URL list/text file, extract and de-duplicate YouTube URLs, then add them with `notebooklm source add --type youtube <url>` to the selected notebook. After adding, run `notebooklm source list` / wait or refresh as needed, and ask a content-specific test question before saying the notebook is chat-ready. Browser-plugin investigation is secondary: use it only to understand JT's existing workflow or when CLI ingestion fails.

0. Verify the CLI before claiming access:
   ```bash
   command -v notebooklm
   notebooklm auth check
   notebooklm list
   ```
   If `notebooklm` is missing or auth fails on a headless VPS, use `references/headless-vps-auth.md`.
1. If no notebook is active, run `notebooklm status` or `notebooklm list` first.
2. Use `notebooklm use <id>` to set context before anything else.
3. Add sources or query as needed.
4. For generation, kick off with `notebooklm generate <type>`, then `notebooklm artifact wait <id>` before downloading.
5. Cite source IDs in your answer when relevant.

## Installation / auth notes

Prefer the Python CLI from `notebooklm-py` for Hermes workflows:

```bash
python3 -m pip install notebooklm-py
python3 -m pip install 'notebooklm-py[browser]'
python3 -m playwright install chromium
notebooklm doctor --fix
```

The npm package `notebooklm` also exists, but in a headless VPS session the Python CLI had the richer command surface (`auth check`, `doctor`, `share`, `artifact`) and was the better fit. See `references/headless-vps-auth.md` for the full noVNC + Cloudflare quick-tunnel auth procedure.

## Autonomy levels

**Run without asking (read-only):**
- `list`, `status`, `auth check`
- `ask` (without `--save-as-note`)
- `source add`
- `history`
- `*-wait`, `*-status`
- `language *`

**Always confirm before:**
- `delete`
- Any `generate *`
- Any `download *`
- `ask --save-as-note`
- `history --save`

## Failure handling

If a command fails with an auth error: first report that NotebookLM is installed but not authenticated, then offer the headless auth flow in `references/headless-vps-auth.md`. Do not try to recover by silently logging into the user's Google account. When exposing a temporary noVNC/Cloudflare tunnel for auth, give the user the tunnel URL + one-time VNC password, wait for them to say login is done, verify with `notebooklm auth check` + `notebooklm list`, then shut down the tunnel/processes. If the noVNC password/link fails, use the troubleshooting sequence in `references/headless-vps-auth.md`: inspect the live `x11vnc` auth file and ports before rotating passwords, and verify the final `vnc.html` URL returns HTTP 200 before sending it.

If the Cloudflare tunnel returns `502` even though ports look open, inspect the noVNC/websockify bind address before giving the URL to the user. `novnc_proxy --listen 127.0.0.1:6080` has been observed to exit or bind unexpectedly on container interfaces; prefer a direct `websockify --web=/usr/share/novnc 127.0.0.1:6080 127.0.0.1:5901` process and verify the origin is reachable before sharing the trycloudflare link.

For remote-browser login sessions where the VNC password fails, the browser is invisible, or multiple x11vnc/websockify/cloudflared processes exist, use `references/headless-novnc-auth-triage.md`. Key rule: verify the live `x11vnc` process, bound port, and `-rfbauth` file before telling JT which password to use. If rotation is messy, start a separate temporary stack on fresh ports and close only the public/temp stack afterward.

If the user asks whether they can share notebooks: yes, but Hermes still needs an authenticated NotebookLM session or access to the source files/URLs. A shared notebook link alone is not useful until auth is configured.
