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

If a command fails with an auth error: first report that NotebookLM is installed but not authenticated, then offer the headless auth flow in `references/headless-vps-auth.md`. Do not try to recover by silently logging into the user's Google account. When exposing a temporary noVNC/Cloudflare tunnel for auth, give the user the tunnel URL + one-time VNC password, wait for them to say login is done, verify with `notebooklm auth check` + `notebooklm list`, then shut down the tunnel/processes.

If the user asks whether they can share notebooks: yes, but Hermes still needs an authenticated NotebookLM session or access to the source files/URLs. A shared notebook link alone is not useful until auth is configured.
