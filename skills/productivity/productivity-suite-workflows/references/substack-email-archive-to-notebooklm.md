# Substack email archive → Markdown → NotebookLM / Drive

Use this when JT wants to preserve or study paid/private Substack content that is delivered by email. Gmail is often easier and more stable than scraping the logged-in Substack web UI.

## Trigger

- User wants an archive/wiki/NotebookLM for a paid Substack/newsletter.
- User says the web page is paid/private but emails arrive in Gmail.
- Need the latest N posts with source dates/titles preserved.

## Workflow

1. **Verify Gmail auth/scopes**
   - Run the Google Workspace setup check from this umbrella package.
   - Confirm token has `gmail.readonly` or `gmail.modify` before reading mail.

2. **Identify sender/query**
   - Search Gmail by exact sender first, then broader terms:
     - `from:<newsletter>@substack.com -subject:(receipt OR "payment receipt" OR subscriptions)`
     - publication handle/title terms if sender is uncertain.
   - Exclude receipts/subscription admin emails.
   - Capture message id, sender, subject, date, and any source/post links.

3. **Extract bodies**
   - Use Gmail API `format=full`.
   - Prefer `text/html` parts if present; otherwise `text/plain`.
   - Decode base64url body data.
   - Convert HTML to readable text/Markdown-ish output with a lightweight parser.
   - Preserve frontmatter with:
     - `source: gmail`
     - `sender`
     - `gmail_id`
     - `date`
     - `subject`
     - `links`

4. **Stage durable local archive**
   - Create `manifest.json` with ordered metadata.
   - Save posts as `posts/NN_YYYY-MM-DD_slug.md`.
   - Create a ZIP containing manifest + posts + strategy/synthesis note.

5. **NotebookLM pack**
   - Verify `notebooklm auth check --test`.
   - Create a dedicated notebook.
   - Upload each Markdown post as a source.
   - Verify `notebooklm source list --json` shows every source as `ready`.
   - Ask one synthesis/verification question before telling JT it is usable.

6. **Drive / Bitácora placement**
   - Upload the strategy note, manifest, ZIP, and individual Markdown posts to Bitácora under an appropriate `3-Resources/...` folder.
   - Do not rely blindly on memorized Drive folder IDs; if a folder ID 404s, search Drive by folder name and then use the discovered live ID.

7. **Close temporary web auth exposure**
   - If noVNC/cloudflared was used for login, close public quick tunnels after extraction/upload.
   - Leave normal local-only VPS screen processes alone unless explicitly asked.

## Pitfalls

- **Web UI is not the first choice.** Paid Substack pages may be easier through Gmail because the full paid email body can already be in the mailbox.
- **Receipts pollute searches.** Always exclude receipt/payment/subscription subjects when building the article corpus.
- **Substack tracking links are noisy.** Preserve a few useful source links, but do not let tracking URLs dominate the note.
- **Folder IDs can drift or be typo-prone.** A Drive `File not found` from a remembered ID should trigger Drive search by name, not user clarification.
- **Do not share or persist credentials.** Users type Substack/Google credentials themselves in the remote browser when auth is needed.

## Deliverables checklist

- [ ] Gmail query and count reported.
- [ ] Latest N article subjects/dates captured.
- [ ] Markdown posts written.
- [ ] Manifest + ZIP created.
- [ ] NotebookLM notebook created and all sources `ready`.
- [ ] At least one NotebookLM synthesis/verification ask succeeds.
- [ ] Drive folder/files uploaded and links returned.
- [ ] Temporary public remote-view tunnel closed.
