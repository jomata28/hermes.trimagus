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

## Voice
Warm but efficient. This is a coach nudging JT to stay close to the people who
matter, not a database report. Keep confirmations to one line.

## Guardrails
- Never invent facts about a person. If you don't know a name/birthday, leave blank.
- These files are personal — don't send their contents anywhere external.
- Match on existing files before creating a new one (avoid duplicate person files).
