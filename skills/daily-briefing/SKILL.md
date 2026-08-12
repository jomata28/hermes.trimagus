---
name: daily-briefing
category: productivity
description: RISING Brief and weekly review workflow — scans Google Calendar, Google Tasks, and Obsidian vault to deliver actionable summaries and auto-fix gaps
trigger: User asks for the RISING Brief, daily/weekly briefing, morning check-in, or "what's up today"
---

# RISING Brief & Weekly Review Workflow

## Purpose
Deliver actionable RISING Briefs and weekly reviews by scanning THREE sources, identifying conflicts/gaps, and updating Google Calendar + Tasks + Obsidian vault to stay in sync.

## Naming Rule
- **RISING Brief** is the official name for JT's 7 AM morning/daily briefing. Use this name in cron prompts, cron job names, headings, saved summaries, vault docs, memories, and user-facing replies.
- Treat "morning brief", "daily briefing", "daily standup", and "what's up today" as aliases that trigger the same workflow, but do not use them as the displayed title unless quoting the user.
- Standard heading: `☀️ RISING Brief — [Day] [Date]`.
- If JT asks to make a name change "official" or "across all time," propagate it beyond the immediate reply: update this skill, durable memory/user profile if relevant, cron job names/prompts, and any Bitácora/vault docs that display the old name.

## Data Sources (check ALL three every time)

### 1. Google Calendar
- **Scan ALL selected calendars, not just primary** (Personal + Houston Methodist Work + any other visible calendars)
- Scan events for next 7 days
- Identify time blocks for study, workouts, research, personal, and lab/work meetings
- **Look for gaps** where work/study blocks are missing
- **Flag conflicts** (overlapping events, travel days, no-research days)
- On travel days, specifically check for recurring routine events (commute, workout, sleep/study blocks) that overlap auto-created flight/hotel/airport events. Do not silently assume they are okay; surface them as cleanup candidates and ask before deleting/changing calendar events.
- Check for upcoming deadlines/events that need prep time
- When doing monthly reviews, list calendars first and query each calendar separately

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

### RISING Brief (7 AM CT)
1. Scan calendar for today + tomorrow
2. Scan tasks for due/overdue items
3. Check project files with deadlines within 2 weeks
4. **Identify gaps**: "no study time blocked today" / "no workout scheduled"
5. **Add calendar blocks** where needed (study, workout, admin time)
6. **Create/adjust tasks** for any missing next actions
7. Deliver the RISING Brief via Telegram with:
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
7. **Clean up**: mark completed tasks and surface project-archive candidates using evidence, not deadline age alone. Classify each as safe-to-archive, archive-container/preserve-open-decisions, parked, active, or needs confirmation. Do not move project files merely because a review says “archive done projects”; archive only after JT explicitly approves the candidates.
8. Deliver comprehensive weekly plan via Telegram

## Action Rules
- **Never just report — act**: If a study block is missing, add it. If a task should be due, set the date.
- **User corrections are source-of-truth updates**: If the user says a bottleneck/decision is wrong (e.g. a trip is now no-go, a vague "conference" goal should be replaced, or a prerequisite order changed), immediately edit the relevant vault decision/project files and verify the patch. Do not leave stale active bottlenecks in briefings.
- **Parking means remove from active surfaces, not destroy history**: When JT says “delete this for now,” “move it to later,” or “park it,” remove that topic from active projects, current working orders, open-decision headlines, briefings, and due tasks; preserve one clearly labeled later/post-milestone backlog note. Do not delete unrelated semantic mentions (e.g. a food preference merely sharing the word “Chinese”).
- **Run a cross-system stale-reference sweep after priority changes**: Check project notes, area/pillar summaries, `_decisions.md`, Google Tasks, recurring Calendar items, README/agent examples, and durable preference memory. A parked priority must not keep reappearing in the RISING Brief because one stale file still calls it active.
- **Calendar is truth**: If vault says "study today" but nothing on calendar, add the block.
- **Tasks are commitments**: Don't let tasks sit without due dates — assign them to the next realistic window.
- **Sync both ways**: When vault changes, update calendar/tasks. When calendar/tasks change, update vault project files.
- **Time awareness**: VPS runs UTC. User is CT (UTC-5/UTC-6). Always convert times.

## Travel Logistics / Flight Schedule Lookup

When the user asks for flight times tied to an active itinerary, first cross-check the user's Google Calendar for existing flight events. For airline route schedule questions, use third-party flight-status pages only as freshness/context and label them accordingly; distinguish scheduled/published times from recent actual departure/arrival times. In the final answer, keep it short and practical: airline, flight number, origin/destination airports, departure/arrival times, frequency if known, and a reminder to confirm on the airline site before buying/changing tickets.

## Common Pitfalls

1. Reporting a search-result time as if it were the airline's guaranteed current schedule.
2. Mixing actual recent departure times with published schedule times without labeling them.
3. Ignoring the user's own calendar when the itinerary is already present there.
4. Forgetting that recurring routine events can overlap travel events and pollute weekly reviews.

## Output Format
Keep it tight. Use sections:
- **📅 Today/Tomorrow** — calendar events
- **✅ Due/Overdue** — tasks from Google Tasks
- **🎯 Project Next Actions** — from vault
- **❓ Decisions Due** — from _decisions.md
- **🔧 Added/Adjusted** — what I changed (calendar blocks added, tasks created)