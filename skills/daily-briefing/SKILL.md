---
name: daily-briefing
category: productivity
description: Daily and weekly briefing workflow — scans Google Calendar, Google Tasks, and Obsidian vault to deliver actionable summaries and auto-fix gaps
trigger: User asks for daily/weekly briefing, morning check-in, or "what's up today"
---

# Daily Briefing & Weekly Review Workflow

## Purpose
Deliver actionable daily and weekly briefings by scanning THREE sources, identifying conflicts/gaps, and updating Google Calendar + Tasks + Obsidian vault to stay in sync.

## Data Sources (check ALL three every time)

### 1. Google Calendar
- Scan events for next 7 days
- Identify time blocks for study, workouts, research, personal
- **Look for gaps** where work/study blocks are missing
- **Flag conflicts** (overlapping events, travel days, no-research days)
- Check for upcoming deadlines/events that need prep time

### 2. Google Tasks (ONEPISSA 8 lists)
- Scan ALL lists for due-today, overdue, and upcoming tasks
- Lists: 01 Ocio, 02 Negocio, 03 Energy, 04 Physical, 05 Intellectual, 06 Social, 07 Spiritual, 08 Artistics, 09 Quick Capture
- **Identify stale tasks** (due dates passed with no progress)
- **Surface hidden priorities** (tasks with no due date that should have one)

### 3. Obsidian Personal Vault (`/root/obsidian-vault` via rclone mount)
- `1-Projects/` — check deadlines, next actions, status
- `2-Areas/*/` — review active commitments per pillar
- `3-Resources/_decisions.md` — check open decisions with approaching deadlines
- `00_log.md` — see what happened recently

### 4. Lab Vault (`/root/obsidian-lab/` via rclone mount `drive-lab`)
- Scan only when the user asks about work/lab tasks, weekly planning includes Negocio/lab, or the `cieslik-lab.md` bridge has active items.
- `Outputs/weekly-reports/` — check whether the weekly PI update is prepared for Thursday 1 PM.
- `Wiki/` — review active experiments, milestones, protocols, and lab operating notes.
- `Raw/frailty/` and other Raw subfolders — check only when the user asks to log/update data or when a weekly PI report needs source data.
- Calendar match: Wed 9am lab meeting, Thu 1pm PI meeting, Fri 9am journal club.
- Personal bridge: `/root/obsidian-vault/2-Areas/Negocio/Wiki/cieslik-lab.md` tracks career-facing lab commitments.
- This vault is PRIVATE — never expose, share, or reference lab data in briefings unless the user asks.

## Review Process

### Daily Briefing (7 AM CT)
1. Scan calendar for today + tomorrow
2. Scan tasks for due/overdue items
3. Check project files with deadlines within 2 weeks
4. **Identify gaps**: "no study time blocked today" / "no workout scheduled"
5. **Add calendar blocks** where needed (study, workout, admin time)
6. **Create/adjust tasks** for any missing next actions
7. Deliver briefing via Telegram with:
   - Today's schedule
   - Tasks due / overdue
   - Next actions for active projects
   - Any decisions needing attention

### Weekly Review (Sunday 8 PM CT)
1. Scan calendar for next 7 days
2. Scan tasks for next week + overdue backlog
3. Check all active projects for upcoming deadlines
4. **Proactively add calendar blocks** for study, workout, project work
5. **Create tasks** for any project step that lacks one
6. **Review _decisions.md** — flag any deadlines within 14 days
7. **Clean up**: mark completed tasks, archive done subtasks
8. Deliver comprehensive weekly plan via Telegram

## Action Rules
- **Never just report — act**: If a study block is missing, add it. If a task should be due, set the date.
- **Calendar is truth**: If vault says "study today" but nothing on calendar, add the block.
- **Tasks are commitments**: Don't let tasks sit without due dates — assign them to the next realistic window.
- **Sync both ways**: When vault changes, update calendar/tasks. When calendar/tasks change, update vault project files.
- **Time awareness**: VPS runs UTC. User is CT (UTC-5/UTC-6). Always convert times.

## Output Format
Keep it tight. Use sections:
- **📅 Today/Tomorrow** — calendar events
- **✅ Due/Overdue** — tasks from Google Tasks
- **🎯 Project Next Actions** — from vault
- **❓ Decisions Due** — from _decisions.md
- **🔧 Added/Adjusted** — what I changed (calendar blocks added, tasks created)