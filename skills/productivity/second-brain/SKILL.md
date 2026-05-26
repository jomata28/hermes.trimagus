---
name: second-brain
description: "Manage a second-brain knowledge base (Obsidian) backed by Google Drive, with multi-agent access (Hermes, Claude, Gemini)."
version: 1.0.0
author: Nous Research
license: MIT
metadata:
  hermes:
    tags: [Obsidian, Second-Brain, Google-Drive, rclone, Bitácora, Multi-Agent, Knowledge-Base]
---

# Second Brain / Personal Knowledge Base

Manage a second-brain knowledge system built on Obsidian, backed by Google Drive, accessible by multiple AI agents (Hermes on VPS, Claude on work laptop, Gemini).

## Architecture

```
Hermes (VPS) ──rclone mount──→ Google Drive ──Google Drive app──→ Work laptop
  │                                                        │
  ├─ Writes: daily logs, calendar summaries,              ├─ Edits via Claude
  │  project updates, proactive pings                     │  (reads/writes the same Drive files)
  └─ Manages Google Calendar + Tasks via API              │
                                                          └─ Obsidian opens Drive folder
```

**Key principle:** The vault lives on Drive. No local mirror, no sync conflicts. All agents read/write the same single source of truth.

## Rclone Setup (VPS → Drive)

### 1. Configure rclone with Google credentials

Reuse the token from `google-workspace` skill at `~/.hermes/google_token.json`:

```python
import json
from pathlib import Path

gtoken = json.loads(Path.home().joinpath(".hermes/google_token.json").read_text())

token_data = {
    "access_token": gtoken["token"],
    "token_type": "Bearer",
    "refresh_token": gtoken["refresh_token"],
    "expiry": gtoken["expiry"]
}

import json as _json
rclone_conf = f"""[drive-hermes]
type = drive
token = {_json.dumps(token_data)}
client_id = {gtoken["client_id"]}
client_secret = {gtoken["client_secret"]}
"""

import os
os.makedirs(Path.home() / ".config/rclone", exist_ok=True)
Path.home().joinpath(".config/rclone/rclone.conf").write_text(rclone_conf)
```

### 2. Mount the vault

```bash
mkdir -p ~/obsidian-vault
rclone mount drive-hermes:bitacora ~/obsidian-vault --vfs-cache-mode writes --daemon
```

### 3. Verify

```bash
ls ~/obsidian-vault/
find ~/obsidian-vault -name "*.md" | head -20
```

## Vault Structure (Bitácora — PARA + ONEPISSA Framework)

The vault moved from the original 5-domain flat structure to a PARA + ONEPISSA system:

```
vault-root/
├── agent.md                      ← system prompt for any agent (was claude.md)
├── README.md                     ← user manual
├── .obsidian/                    ← vault config (MUST stay at root)
├── raw/                          ← incoming dumps (read-only, never edited by agents)
├── 1-Projects/                   ← active projects with hard deadlines
├── 2-Areas/                      ← the 8 ONEPISSA pillars (ongoing responsibilities)
│   ├── Ocio/                     ← adventure, skills, transportation
│   ├── Negocio/                  ← wealth, work, investments, residency
│   ├── Energy/                   ← emotion, mindset, energetic health
│   ├── Physical/                 ← physical dominance, body mastery
│   ├── Intellectual/             ← studies, mental capacity
│   ├── Social/                   ← relationships, leadership, community
│   ├── Spiritual/                ← relationship with God, spiritual path
│   └── Artistics/                ← culture, artistic, linguistic
│
│   Each pillar contains:
│   ├── Pillar-<Name>.md           ← mission statement + active projects
│   ├── Raw/                      ← unprocessed inputs
│   ├── Wiki/                     ← synthesized knowledge, SOPs, rules
│   └── Outputs/                  ← finished deliverables (this pillar's)
│
├── 3-Resources/                  ← general reference that doesn't fit a pillar
│   ├── _decisions.md             ← open decisions
│   ├── _ingested.md              ← raw files already processed
│   ├── index.md                  ← cross-pillar ToC
│   └── skills-plan.md            ← full skill inventory + build plan
├── 4-Archives/                   ← completed projects + completed outputs
├── 5-Admin and Reviews/          ← daily log, weekly/monthly/quarterly reviews
│   ├── 00_log.md                 ← append-only daily log
│   ├── README.md                 ← review rituals guide
│   └── reviews/
│       ├── weekly/
│       ├── monthly/
│       └── quarterly/
├── hermes/                       ← Hermes agent config, skills, and prompts
│   ├── README.md
│   ├── skills/                   ← skill files (e.g. notebooklm.skill.md)
│   └── handoff-to-new-chat.md    ← copy-paste for new sessions
└── outputs/                      ← (deprecated - now inside pillar Outputs/ or 4-Archives)
```

**Each pillar follows the Karpathy Pipeline:** Raw/ → Wiki/ → Outputs/

### Key rules
- `.obsidian/` MUST stay at vault root — Obsidian won't detect the vault otherwise
- `Raw/` folders (both root-level `raw/` and per-pillar `Raw/`) are NEVER edited by agents
- Wiki pages use frontmatter: `pillar: ocio | negocio | energy | physical | intellectual | social | spiritual | artistics`
- Pillar mission files are `Pillar-<Name>.md` inside each pillar folder
- Completed deliverables move from `Outputs/` → `4-Archives/`

## Important: Vault Separation

Two separate rclone mounts exist on VPS:
- `/root/obsidian-vault/` → `drive-hermes:bitacora` (personal, NEVER shared)
- `/root/obsidian-lab/` → `drive-hermes:cieslik-lab` (Cieslik Lab, NEVER shared)
- Never nest one inside the other — they are sibling Drive folders
- User controls ALL exports/sharing. Never share vault data unless explicitly directed.
- Bridge file: `2-Areas/Negocio/Wiki/cieslik-lab.md` (career-facing summary only)

## Agent Roles

| Agent | Role | Access |
|-------|------|--------|
| **Hermes (VPS)** | Calendar management, Google Tasks, daily standups, proactive Telegram pings, calendar→vault logging, project tracking | Full Drive via rclone + Calendar/Tasks API |
| **Claude (work laptop)** | Raw ingestion, wiki restructuring, knowledge synthesis, handoff summaries | Drive folder + Obsidian local |
| **Gemini** | Ad-hoc access, supplemental research | Drive folder |

## Hermes Daily Routine

When asked to do daily standup:

1. Read `5-Admin and Reviews/00_log.md` for recent context
2. Check Google Calendar for today's events
3. Check Google Tasks for @today items
4. Check `2-Areas/` pillars for active projects
5. Write morning summary to `hermes/daily/YYYY-MM-DD.md`
6. Ping user on Telegram with today's priorities
7. Update active project tracking

## Active Priorities (2026-05-25 snapshot)
- **USMLE Step 1 / IFOM** — August 2026 (Intellectual, HIGHEST PRIORITY)
- **HMRI MI ligation certification** — June 8 (Negocio)
- **Zenith BJJ program** — ends ~June 28 (Physical)
- **Monterrey wedding trip** — May 30 (Social)
- **5 gating decisions (D1-D6)** — must close before Sept 1, 2026

## Pitfalls

- **rclone mount can silently fail** if the token expires. Check with `ls ~/obsidian-vault` before operations. Remount if empty.
- **Drive rate limits** — batch reads, don't hammer the API with rapid sequential calls
- **Markdown conflict** — if multiple agents edit the same file simultaneously, Drive version conflicts can occur. Use separate files per agent per day
- **VFS cache mode matters** — use `--vfs-cache-mode writes` not `full` — it's lighter and sufficient for markdown files
- **Token refresh** — the rclone config reuses Google OAuth token. If `google-workspace` token expires, update the rclone config with fresh credentials
- **.obsidian at root required** — if you restructure the vault, NEVER move `.obsidian/` — it's what makes Obsidian recognize the folder as a vault
