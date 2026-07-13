---
name: productivity-suite-workflows
description: "Umbrella for productivity operations: Google Workspace, terminal email, documents/PDFs, slide decks, second-brain vaults, and Teams meeting pipelines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [productivity, google-workspace, gmail, calendar, drive, email, pdf, ocr, powerpoint, obsidian, second-brain, teams, microsoft-graph]
---

# Productivity suite workflows

Use this umbrella for user-facing productivity work: email and calendar, Google Drive/Docs/Sheets/Tasks, PDFs and scanned documents, slide decks, Obsidian/second-brain vaults, and Microsoft Teams meeting summaries.

This skill consolidates the former standalone packages `google-workspace`, `himalaya`, `ocr-and-documents`, `powerpoint`, `second-brain`, and `teams-meeting-pipeline`. Their complete packages, including support files and scripts, are preserved under `references/<package>-package/`.

## Route by task

| User asks for | Use subsection | Full package reference |
|---|---|---|
| Gmail, Calendar, Drive, Docs, Sheets, Google Tasks, rclone Drive mount | Google Workspace operations | `references/google-workspace-package/SKILL.md` |
| Drive folder image OCR/extraction into Google Sheets, especially timer/clock numbers from screenshots or follow-up passes for colored handwritten/digital annotations | Image-to-Sheets extraction | `references/timer-image-extraction-to-sheets.md` |
| Handwritten hanging-test sheet photos into Excel, with box/day IDs, duplicate removal, and trial time transcription | Hanging-test image extraction | `references/hanging-test-image-extraction.md` |
| IMAP/SMTP mailbox via Himalaya CLI | Terminal email operations | `references/himalaya-package/SKILL.md` |
| PDF text extraction, OCR, scanned docs, forms, marker-pdf, pymupdf | PDF and document extraction | `references/ocr-and-documents-package/SKILL.md` |
| Create/read/edit `.pptx`, slide decks, Google Slides conversion | Presentation and deck production | `references/powerpoint-package/SKILL.md` |
| Obsidian vault, Bitácora, PARA/ONEPISSA, rclone-backed knowledge base, lab vault separation | Second-brain knowledge base | `references/second-brain-package/SKILL.md` |
| Forum/community scraping into Obsidian + future NotebookLM querying | Forum scrape to knowledge base | `references/forum-scrape-to-knowledge-base.md` |
| Paid/private Substack/newsletter archive from Gmail into Markdown, Drive, and NotebookLM | Substack email archive to NotebookLM | `references/substack-email-archive-to-notebooklm.md` |
| Teams meeting summaries, Microsoft Graph transcripts, pipeline jobs/subscriptions | Teams meeting pipeline | `references/teams-meeting-pipeline-package/SKILL.md` |

## Shared safety rules

- Never send email, delete mail, create/delete calendar events, or submit externally visible messages without explicit user confirmation.
- For document deliverables, verify the real artifact: extract text, render slides/PDF pages, or download the converted Google file and inspect it.
- Preserve legal/signature fields unless the user explicitly provides authorization and required data.
- For credentialed services, check auth status before assuming access. Do not print secrets.
- Prefer task-specific scripts from preserved packages over ad-hoc one-liners when they exist.

## Google Workspace operations

Use the Google Workspace package for Gmail, Calendar, Drive, Docs, Sheets, Contacts, Tasks, OAuth setup, Drive upload/convert flows, Google Slides conversion, rclone Drive mounts, Google Cloud CLI PKCE quirks, and Antigravity CLI notes.

For Drive folders containing screenshots/photos that need values extracted into a Sheet, especially white digital timer/clock numbers, use `references/timer-image-extraction-to-sheets.md`: copy the folder locally with rclone, OCR only the target number, manually review flagged cases, then create and verify a formatted Google Sheet in the source folder. For JT's hanging-test images, preserve the requested `box_day_id` style (`F9-1`, `F9-2`, `F9-3`, etc.) next to the image/source column; de-duplicate repeated photos before producing the final workbook.

For handwritten hanging-test sheets sent as Telegram images, use `references/hanging-test-image-extraction.md`: count all attachments, transcribe box/day/mouse/trial times, add `box_day_id` next to image name (`F9-3`, `H8-2`), remove duplicate sheet photos before final Excel, and verify the workbook by reading it back.

Operational pattern:
1. Run the setup check before first use. In the umbrella package layout, the Google Workspace scripts live under `productivity-suite-workflows/references/google-workspace-package/scripts/`; if older notes mention `${HERMES_HOME}/skills/productivity/google-workspace/scripts/setup.py`, resolve to this preserved package path instead.
2. Confirm required scopes before auth, especially Drive write access.
3. Use the package's `google_api.py` wrapper when possible; use direct Google APIs for Tasks and attachment-heavy Gmail workflows.
4. For Google Slides/Docs/Sheets deliverables, create locally when appropriate, upload/convert to native Google format, export back for QA, then share the final link.

## Terminal email operations

Use Himalaya when the user wants mailbox operations through IMAP/SMTP from the terminal and the external `himalaya` CLI is configured. Prefer non-interactive template piping for sends/replies. Be careful with folder alias syntax: v1.2.0 expects `folder.aliases.X`; older singular alias sections can cause sent-mail save failures after SMTP delivery, which can lead to duplicate emails if retried blindly.

## PDF and document extraction

Use this subsection for PDFs, scanned documents, OCR, forms, and extraction. Try remote extraction first when a URL is available. For local files, use lightweight `pymupdf`/`pymupdf4llm` unless OCR, equations, forms, or complex layout require marker-pdf. Before installing marker-pdf, check disk space because it can require several GB. For simple scanned forms, try Poppler + Tesseract before heavy OCR stacks.

The former package also covers lightweight PDF editing with `nano-pdf`; verify edits visually or by extracting affected page text.

## Presentation and deck production

Use this subsection for any `.pptx`, slide deck, presentation, Google Slides deliverable, or journal-club deck. Read/analyze with markitdown and thumbnails; edit with the preserved office scripts or create from scratch with pptxgenjs. Every deck must be visually QA'd by rendering to images. Assume the first render has problems and do at least one fix-and-verify cycle before declaring success.

For journal-club/scientific decks, do not only make slides look good: be ready to explain why each figure was selected and how to present it. Prefer a story-driven figure sequence (discovery → functional proof → mechanism → therapeutic/clinical implication). When the user asks how to present figures, identify the lettered subpanels worth pointing at and give short speaker language for what each proves and what limitation remains. If the user asks for more explanation or a white-background version, add explanatory text by expanding slide count rather than cramming content into crowded slides.

For research-heavy marketplace/listing decks (cars, real estate, products, vendor comparisons), use `references/marketplace-research-decks.md`: save raw source evidence and a manifest, download images, clearly label unpublished fields instead of estimating, and separate source facts from recommendation synthesis. Be especially defensive with bot-blocked or client-rendered pages because extracted tables can be shifted/misaligned.

For Google Slides deliverables, create a local `.pptx`, upload/convert to native Slides, export the converted version to PDF, render pages, and QA the converted artifact because Google conversion can change spacing and wrapping.

## Second-brain knowledge base

Use this subsection for the user's Obsidian/Bitácora knowledge system, rclone-backed vault operations, daily standups, weekly reviews, project tracking, PARA/ONEPISSA pillar structure, and separate Cieslik Lab vault workflows. The personal vault and lab vault are separate sibling mounts; never mix or share vault data unless explicitly directed.

Key rules: keep `.obsidian/` at vault root, never edit `raw/` or per-pillar `Raw/` folders, preserve frontmatter/wikilinks, and use rclone listing when file search has trouble on FUSE mounts.

For scraped forums/community archives that the user wants to query later or upload to NotebookLM, use `references/forum-scrape-to-knowledge-base.md`: archive raw JSON + Markdown in batches, create a source registry/topic index/hub, build a local SQLite FTS index, and stage a NotebookLM upload pack before attempting upload.

For paid/private Substack or newsletter content that arrives by email, prefer Gmail extraction over scraping the logged-in web UI. Use `references/substack-email-archive-to-notebooklm.md`: search by sender, exclude receipts, extract the latest posts into Markdown with manifest metadata, upload the corpus to NotebookLM, write a strategy/synthesis note, upload the archive to Bitácora/Drive, then close any temporary public remote-view tunnel.

## Teams meeting pipeline

Use this subsection for Microsoft Teams meeting summaries, transcripts, action items, Graph webhook subscriptions, job replay, and pipeline operations. The interface is the `hermes teams-pipeline` CLI. Validate config and token health before troubleshooting. Graph subscriptions expire after 72 hours; if meetings stop ingesting, inspect subscriptions and set up automated renewal.

## Package integrity rule

The original package directories were copied intact into this umbrella so their internal `references/`, `scripts/`, and other paths remain coherent. Do not flatten them unless you also re-home every referenced file and rewrite instructions to the new paths.
