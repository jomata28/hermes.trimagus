# Bitácora Vault Reference

Session-derived operational notes for the user's Bitácora personal life-operating system. This reference was consolidated from the former `bitacora-vault` skill into the broader `second-brain` umbrella.

## Identity and context

The user is Jose Torres (JT) — Houston Methodist research fellow, ITESM med grad, USMLE Step 1/2 candidate, applying for IR or Vascular Surgery residency in 2027. Lives in Houston; girlfriend in CDMX.

Gold window: May 2026 → summer 2028 before residency = survival mode.

NotebookLM = research brain; Bitácora = action brain. They complement each other.

## Vault structure

Mounted at `/root/obsidian-vault/` via rclone, syncing to Google Drive.

```text
bitacora/
├── agent.md                    ← system prompt; read first for vault work
├── README.md                   ← user manual
├── 1-Projects/                 ← active projects with deadlines
├── 2-Areas/                    ← 8 ONEPISSA pillars
│   ├── Ocio/                   ← adventures, skills, trips
│   ├── Negocio/                ← work, money, residency
│   ├── Energy/                 ← mindset, stress, routines
│   ├── Physical/               ← Zenith, BJJ, body
│   ├── Intellectual/           ← USMLE, IFOM, Anki, research
│   ├── Social/                 ← girlfriend, family, relationships
│   ├── Spiritual/              ← TBD
│   └── Artistics/              ← language, culture
├── 3-Resources/                ← general reference
├── 4-Archives/                 ← completed projects and outputs
├── 5-Admin and Reviews/        ← daily log, weekly/monthly/quarterly
├── hermes/                     ← agent config, skills, prompts
└── raw/                        ← junk drawer; never edit
```

Each pillar in `2-Areas/<Pillar>/` contains:
- `Pillar-<Name>.md` — mission statement + active projects
- `Raw/` — unprocessed inputs
- `Wiki/` — synthesized knowledge
- `Outputs/` — finished deliverables

## ONEPISSA pillars

| Pillar | Covers | Active items |
|---|---|---|
| Ocio | Adventure, skills, transport | Pilot license, Buceo, Big Bend, Mongolia |
| Negocio | Wealth, work, investments | HMRI job, online income, residency strategy |
| Energy | Emotion, mindset | Daily routines, Step 1 stress management |
| Physical | Body mastery | Zenith program, BJJ trials |
| Intellectual | Studies, mental capacity | USMLE Step 1, IFOM, Anki |
| Social | Relationships, community | GF in CDMX, family weddings |
| Spiritual | Spiritual path | TBD |
| Artistics | Culture, language | Language decision: French/Chinese/Russian |

## RISING Brief workflow

For 7 AM CT RISING Brief cron or manual daily standup:

1. Read `5-Admin and Reviews/00_log.md` for recent context.
2. Read `1-Projects/` for deadlines this week.
3. Read `3-Resources/_decisions.md` for open bottlenecks.
4. Check Google Calendar for today and this week.
5. Check Google Tasks priority items.
6. Format:

```text
☀️ RISING Brief — [Day] [Date]
📋 TODAY'S GRID
🔥 THIS WEEK's KEY DEADLINES
✅ GOOGLE TASKS — Priority items
⚡ ACTIVE BOTTLENECKS
What are we executing today?
```

## Weekly review workflow

For Sunday 8 PM CT weekly review or manual review:

1. Read `00_log.md` for the week's entries.
2. Check Google Tasks for completed and overdue items.
3. Check Calendar for next week.
4. Format:

```text
📋 Weekly Review — [Date]
📊 THIS WEEK DONE
🔥 NEXT WEEK's KEY DATES
⏰ OVERDUE TASKS
🎯 FOCUS AREAS NEXT WEEK
```

## Google Tasks integration

Tasks are organized into 9 lists:
- `01 Ocio` through `08 Artistics`
- `09 Quick Capture` inbox

For task operations, load/use the `google-workspace` skill and its Tasks API instructions.

## Rclone Drive sync

Mount command:

```bash
rclone mount drive-hermes:bitacora /root/obsidian-vault --vfs-cache-mode writes --daemon
```

All file changes under `/root/obsidian-vault/` should auto-sync to Drive.

## Weekly scanning methodology

When the user asks “what's needed this week” or “what should we set up”:

1. List projects: `rclone lsf drive-hermes:bitacora/1-Projects/`; read each `.md` for deadlines in range.
2. Read decisions: `/root/obsidian-vault/3-Resources/_decisions.md`.
3. Scan pillars: `rclone lsf drive-hermes:bitacora/2-Areas/`; read `Pillar-*.md` for active projects and scheduled items.
4. Check Google Calendar events from today through 7 days.
5. Check incomplete Google Tasks across all 8 ONEPISSA lists.
6. Synthesize by urgency with suggested execution days.

## Pitfalls

- rclone mount must be running. Check with `ps aux | grep "rclone mount"`; remount if down.
- `search_files` does not work reliably on the rclone FUSE mount at `/root/obsidian-vault`; it can return 0 results. Use `rclone lsf drive-hermes:bitacora/<path>` to list, or direct file reads for known paths.
- Google API tokens expire hourly. If a Google API call returns 401, refresh from the stored token file using `refresh_token`, `client_id`, and `client_secret`.
- Token format varies: flat (`access_token`/`refresh_token` at root), `installed`, or `web` format. Inspect before refreshing.
- User prefers casual/direct tone; bilingual Spanish/English is natural.
- Never edit files in `raw/`.
- The old 5-domain system was replaced by ONEPISSA. Do not reference the old domains as active; they are archived concepts.
