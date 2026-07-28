---
name: personal-crm
description: Manage JT's personal CRM — log interactions with people, track birthdays and follow-up cadence, and surface who he's overdue to contact. Backed by markdown files in the Bitácora vault.
version: 1.0.0
author: Hermes Agent
category: productivity
metadata:
  hermes:
    tags: [crm, relationships, people, contacts, follow-up, social]
---

# Personal CRM

JT's relationship tracker. One markdown file per person under
`/root/obsidian-vault/2-Areas/Social/Wiki/crm/people/`. This skill is how Hermes
reads and updates it.

## Data model
Each person is `people/firstname-lastname.md`. Frontmatter fields:
- `name`, `tier` (inner|close|network), `relationship`, `location`
- `birthday` (MM-DD, optional), `cadence_days` (int, blank = no nudge)
- `last_contact` (YYYY-MM-DD), `tags` (list)

Body has `## About`, `## Log` (newest-first dated bullets), `## Follow-ups` (checkboxes).
Template: `crm/_template.md`. Index/roster: `crm/README.md`.

## Operations

### Log a touch  ("log that I called Ana today", "note: saw Carlos at the gym")
1. Find the person file by name under `people/` (fuzzy match on name/filename).
   If none exists, create one from `_template.md`, ask only for tier if unclear.
2. Prepend a dated bullet to `## Log`: `- YYYY-MM-DD — <what happened>`.
3. Set `last_contact` in frontmatter to today.
4. Confirm briefly: "Logged 👍 last talked to Ana today."

### Add a person  ("add my new colleague Dr. Smith, close tier")
1. Copy `_template.md` → `people/<slug>.md`, fill known fields.
2. Ask (one message) only for missing high-value fields: tier, cadence, birthday.

### Who am I overdue with?  (daily CRM check, or on request)
1. For each person with a `cadence_days`, compute days since `last_contact`.
2. Overdue = days_since > cadence_days. Rank inner > close > network, most overdue first.
3. Report as a short list: "You're overdue with: Ana (inner, 4d) · Mom (inner, 9d)".
   If nobody's overdue, say so in one line — don't pad.

### Birthdays
- ~7 days before any `birthday` (MM-DD), flag it: "🎂 Ana's birthday is Sun (Mar 14)."

### Update the roster table
- After any change, refresh the `| Person | Tier | Last contact | Cadence | Next due |`
  table in `crm/README.md` from the people/ files.

## Visualization (without Telegram)
JT will ask "how do I see the CRM without talking to you?" — answer with options,
lightest first:
1. **Drive roster** — `crm/README.md` table is the at-a-glance view; readable as
   plain text in the Google Drive app/web, no setup.
2. **Obsidian** — full graph/search; work PC vault or Android + sync plugin.
3. **HTML dashboard** — on request, generate a color-coded (current vs overdue,
   sorted by urgency) dashboard into the vault; same pattern as the Dreamlining asset.
4. **Google Sheet roster mirror** — if JT wants sortable/filterable: Sheet = visual
   roster (update it whenever the roster README is refreshed), `people/*.md` stays
   the source of truth for detail/logs.

## Onboarding flow (architecture first)
JT wants the architecture agreed with him BEFORE data entry. When he starts
dictating people (usually by voice — expect transcription noise, e.g. "RME" = CRM):
- Per person, ask only: name, relationship, tier, cadence_days, birthday (if known).
- Confirm spelling of voice-dictated names before creating files (never invent).
- Batch-create the `people/` files, then show the roster table as confirmation.
- Categories he has mentioned: family, GF, friends, work colleagues, mentors/network.

## Voice
Warm but efficient. This is a coach nudging JT to stay close to the people who
matter, not a database report. Keep confirmations to one line.

## Guardrails
- Never invent facts about a person. If you don't know a name/birthday, leave blank.
- These files are personal — don't send their contents anywhere external.
- Match on existing files before creating a new one (avoid duplicate person files).
