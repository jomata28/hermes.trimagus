---
name: notebooklm-vault
description: "NotebookLM: query, add to, generate from, and download NotebookLM artifacts. Sourced from the user's Bitácora vault."
version: 1.0.0
author: REDACTED
license: MIT
---

# Skill: NotebookLM

You are connected to the user's NotebookLM via the `notebooklm` CLI.

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

1. If no notebook is active, run `notebooklm status` or `notebooklm list` first.
2. Use `notebooklm use <id>` to set context before anything else.
3. Add sources or query as needed.
4. For generation, kick off with `notebooklm generate <type>`, then `notebooklm artifact wait <id>` before downloading.
5. Cite source IDs in your answer when relevant.

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

If a command fails with an auth error: tell the user the session expired and they need to re-authenticate locally. Do NOT try to recover programmatically.
