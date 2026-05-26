---
name: bitacora-vault
description: "Bitácora vault management — PARA + ONEPISSA life OS. Folder structure, daily standups, project tracking, Google Calendar/Drive/Task integration."
version: 1.0.0
author: C.T. Gravy / Hermes
license: MIT
metadata:
  hermes:
    tags: [Bitácora, ONEPISSA, PARA, life-OS, vault, Obsidian, Google, Calendar, Tasks, Drive, rclone]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [google-workspace, second-brain, obsidian]
---

# Skill: Bitácora Vault

You are managing the user's Bitácora — a personal life-operating system built on PARA + ONEPISSA.

## When to use

- User asks about their projects, deadlines, or weekly status
- Daily standup/morning briefing (7 AM CT cron job)
- Weekly review summary (Sunday 8 PM CT cron job)
- Creating/updating project files, pillar wiki pages, or decisions
- Syncing vault changes to Google Drive via rclone mount

## Context

The user is **Jose Torres** (JT) — Houston Methodist research fellow, ITESM med grad, USMLE Step 1/2 candidate, applying for IR or Vascular Surgery residency in 2027. Lives in Houston, GF in CDMX.

**Gold window:** May 2026 → summer 2028 (before residency = survival mode).
**NotebookLM** = research brain, **Bitácora** = action brain. They complement each other.

## Vault Structure (PARA + ONEPISSA)

The vault is mounted at `/root/obsidian-vault/` via rclone, syncing to Google Drive.

```
bitacora/
├── agent.md                    ← system prompt (read FIRST)
├── README.md                   ← user manual
├── 1-Projects/                 ← active projects with deadlines
├── 2-Areas/                    ← 8 ONEPISSA pillars
│   ├── Ocio/                   ← adventures, skills, trips
│   ├── Negocio/                ← work, money, residency
│   ├── Energy/                 ← mindset, stress, routines
│   ├── Physical/               ← Zenith, BJJ, body
│   ├── Intellectual/           ← USMLE, IFOM, research, Anki
│   ├── Social/                 ← GF, family, relationships
│   ├── Spiritual/              ← TBD
│   └── Artistics/              ← language, culture
├── 3-Resources/                ← general reference
├── 4-Archives/                 ← completed projects + outputs
├── 5-Admin and Reviews/        ← daily log, weekly/monthly/quarterly
├── hermes/                     ← agent config, skills, prompts
└── raw/                        ← junk drawer (never edit)
```

Each pillar in `2-Areas/<Pillar>/` contains:
- `Pillar-<Name>.md` — mission statement + active projects
- `Raw/` — unprocessed inputs
- `Wiki/` — synthesized knowledge
- `Outputs/` — finished deliverables

## The 8 ONEPISSA Pillars

| Pillar | Covers | Active Items |
|---|---|---|
| **Ocio** | Adventure, skills, transport | Pilot license, Buceo, Big Bend, Mongolia |
| **Negocio** | Wealth, work, investments | HMRI job, online income, residency strategy |
| **Energy** | Emotion, mindset | Daily routines, Step 1 stress mgmt |
| **Physical** | Body mastery | Zenith program, BJJ trials |
| **Intellectual** | Studies, mental capacity | USMLE Step 1 (Aug 2026), IFOM (Jul 2026), Anki |
| **Social** | Relationships, community | GF in CDMX, family weddings |
| **Spiritual** | Spiritual path | TBD |
| **Artistics** | Culture, language | Language decision (FR/ZH/RU) |

## Daily Briefing Workflow (7 AM CT cron)

1. Read `5-Admin and Reviews/00_log.md` for recent context
2. Read `1-Projects/` for deadlines this week
3. Read `3-Resources/_decisions.md` for open bottlenecks
4. Check Google Calendar for today + this week
5. Check Google Tasks for priority items
6. Format briefing:
   ```
   ☀️ Morning Briefing — [Day] [Date]
   📋 TODAY'S GRID
   🔥 THIS WEEK's KEY DEADLINES
   ✅ GOOGLE TASKS — Priority items
   ⚡ ACTIVE BOTTLENECKS
   What are we executing today?
   ```

## Weekly Review Workflow (Sunday 8 PM CT cron)

1. Read `00_log.md` for the week's entries
2. Check Google Tasks for completed/overdue items
3. Check Calendar for next week
4. Format:
   ```
   📋 Weekly Review — [Date]
   📊 THIS WEEK DONE
   🔥 NEXT WEEK's KEY DATES
   ⏰ OVERDUE TASKS
   🎯 FOCUS AREAS NEXT WEEK
   ```

## Google Tasks Integration

Tasks are organized into 9 lists (numbered for sort order):
- `01 Ocio` through `08 Artistics`
- `09 Quick Capture` (inbox)

To interact with Tasks, load the `google-workspace` skill and use the Tasks API section.

## Rclone Drive Sync

The vault syncs to Google Drive via:
```bash
rclone mount drive-hermes:bitacora /root/obsidian-vault --vfs-cache-mode writes --daemon
```

All file changes at `/root/obsidian-vault/` auto-sync to Drive.

## Pitfalls

- **rclone mount must be running** — check with `ps aux | grep "rclone mount"`. If down, remount.
- **`search_files` does NOT work on the rclone FUSE mount at `/root/obsidian-vault`** — it always returns 0 results. Use `rclone lsf drive-hermes:bitacora/<path>` to list files, or direct `cat /root/obsidian-vault/<path>` to read them. This is the most common trap when working with the vault.
- **Google API tokens expire hourly** — if you get 401, refresh the token (stored in `google_token.json` or flat token format). Use `refresh_token` + `client_id` + `client_secret` to POST to `https://oauth2.googleapis.com/token` with `grant_type=refresh_token`.
- **Token format varies** — check if flat (`access_token`/`refresh_token` at root), `installed` format, or `web` format. Extract credentials accordingly before refreshing.
- **User prefers casual/direct tone** — no corporate fluff, bilingual (Spanish/English) is natural.
- **Never edit files in `raw/`** — that's the junk drawer.
- **5 domains → 8 pillars** — the original 5-domain system was replaced by ONEPISSA. Don't reference the old domains (adventures, finance, mental, spiritual, study) as active — they are archived concepts.

## Weekly Scanning Methodology

When the user asks "what's needed this week" or "what should we set up":

1. **List projects** — `rclone lsf drive-hermes:bitacora/1-Projects/` and read each `.md` for deadlines in range
2. **Read decisions** — `cat /root/obsidian-vault/3-Resources/_decisions.md` for open decisions with approaching deadlines
3. **Scan pillars** — `rclone lsf drive-hermes:bitacora/2-Areas/` then read `Pillar-*.md` for active projects and scheduled items
4. **Check Calendar** — Google Calendar API: events from today through 7 days
5. **Check Tasks** — Google Tasks API: incomplete items across all 8 ONEPISSA lists
6. **Synthesize** — group by urgency, present as prioritized list with suggested execution days
