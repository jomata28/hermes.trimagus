# STATE-SHIFU.md — Agent State File

This file is the single source of truth for *where the program is right now*.
Any agent (model or human) administering a session MUST read this file first,
act, then write updates back to it before ending the session. See
`PROGRAM-OPERATIONS.md` §2 for the full read-state → act → write-state loop.

Do not delete history from the Changelog. Do not hand-edit the STATE block
except through the runbook procedures in `PROGRAM-OPERATIONS.md`.

---

## STATE (machine-readable — parse this block; update every session)

```yaml
program:
  mission: "Conversational Mandarin (via Chinese history) + Yang 24 tai chi proficiency in 6 months"
  start_date: 2026-07-27
  end_date: 2027-01-27          # start_date + 26 weeks, hard boundary — see non-negotiables
  total_weeks: 26
  daily_dose_minutes: 150        # 30 Anki / 30 tai chi / 60 input / 30 speaking

position:
  current_block: 1               # 1 = weeks 1-12 (BLOCK1-PLAN.md), 2 = weeks 13-26 (not yet written)
  current_week: 0                # 0 = not yet started
  current_day_in_week: 0         # 1-7
  total_days_elapsed: 0
  program_day_number: 0          # 1-182

adherence:
  streak_days: 0
  longest_streak: 0
  zero_days_last_14: 0
  partial_days_last_14: 0
  last_session_date: null
  last_session_status: null      # full | partial | zero
  last_session_dose_pct: null    # 0-100, minutes completed / 150

reviews:
  last_weekly_review_date: null
  last_weekly_review_corrective_action: null
  last_monthly_gate_date: null
  last_monthly_gate_result: null # pass | pass-with-flags | hold

status:
  flag: on-track                 # on-track | at-risk | plateau | injury-hold | tutor-gap
  flag_since: null
  open_issues:
    - "Ikanema notebook not yet ingested into this program — no NotebookLM access at program init. See PROGRAM-OPERATIONS.md §6 for the closing procedure. Does not block execution: program runs on DiSSS/CaFE + Ultralearning + Deep Work + Reality Transurfing as specified below."

metrics:
  anki_mature_cards: 0
  anki_cards_due_avg_7d: 0
  taichi_postures_learned: 0     # out of 24
  taichi_full_form_unprompted: false
  speaking_minutes_logged_total: 0
  history_periods_narratable: 0  # out of 10 (see BLOCK1-PLAN.md dynasty units)
```

---

## Mission (human-readable)

Compress ~2 years of natural-pace progress into 6 months (26 weeks) on two
parallel tracks that share a content spine — Chinese history — so vocabulary
acquisition and cultural/narrative context reinforce each other:

1. **Mandarin**: functional conversational proficiency, built by narrating
   Chinese history chronologically (legendary era → Qing) as the input/output
   content spine.
2. **Tai chi (Yang 24)**: full unprompted performance of the standard 24-posture
   form with correct structure, learned through the standard posture sequence.

Method stack (see `PROGRAM-OPERATIONS.md` §6 appendix for full mapping):
- **Ferriss DiSSS/CaFE** — Deconstruction, Selection, Sequencing, Stakes /
  Compression, Frequency, Encoding. Governs *what* gets taught and in what order.
- **Scott Young Ultralearning** — metalearning, directness, drill, retrieval,
  feedback. Governs *how* each session is structured.
- **Cal Newport Deep Work** — the daily 150-minute block is protected,
  distraction-free, scheduled, and non-negotiable.
- **Reality Transurfing (positive slides)** — a 2-minute pre-session mental
  rehearsal of the session going well, and post-session non-judgmental logging
  of shortfalls (reduce "importance"/anxiety around missed days rather than
  amplify it, since anxiety-driven quitting is the dominant failure mode in
  ultralearning projects).

## Daily protocol (150 min, one contiguous block, default 06:30–09:00 local —
adjust the clock time freely, never the sequence or total)

1. **Positive slide (2 min, not counted in the 150)** — visualize the session
   going well; state the day's single focus out loud or in writing.
2. **Anki (30 min)** — clear the due queue for Mandarin vocab/hanzi deck first;
   if time remains, add new cards from the current week's unit (see
   BLOCK1-PLAN.md) up to the week's new-card cap.
3. **Tai chi (30 min)** — drill the current week's posture(s) per
   BLOCK1-PLAN.md, then run every posture learned so far in sequence at least
   once. Self-record on a phone weekly (see weekly protocol).
4. **Input (60 min)** — consume the current week's history unit in Mandarin
   (graded/subtitled), shadow-read aloud for at least 10 of the 60 minutes.
5. **Speaking (30 min)** — live output practice (tutor session on the days one
   is scheduled; solo shadowing + recorded self-narration on the days it
   isn't — see BLOCK1-PLAN.md cron schedule for which days).
6. **Log** — update `adherence` and `metrics` in the STATE block above:
   session status (full/partial/zero), dose %, any metric deltas.

### Minimum viable day (MVD)
If the full 150 minutes is not available, protect this floor, in this order,
before anything else is dropped: 10 min Anki (due cards only) + 10 min tai chi
(current posture only) + 10 min input. A day meeting the MVD is logged
`partial`, dose_pct = actual/150, and does **not** break `streak_days`. A day
with zero minutes is logged `zero` and does break the streak. This rule exists
so an agent never has to ask "does this count" — it always resolves
mechanically from minutes logged.

## Weekly protocol (see PROGRAM-OPERATIONS.md §3 for the exact runbook)
Every 7th program day: run the weekly review (≤300 words, exactly one
corrective action), update `reviews.last_weekly_review_*`, advance
`position.current_week`.

## Monthly protocol
Every 4th completed week (weeks 4, 8, 12, ...): run the monthly gate check
against the current block's exit criteria (BLOCK1-PLAN.md for weeks 1-12).
Result is `pass`, `pass-with-flags`, or `hold` — see escalation rules in
PROGRAM-OPERATIONS.md §4 for what each triggers.

## Operating rules (non-negotiables)
- The 6-month end date (`program.end_date`) does not move. If a monthly gate
  returns `hold` twice consecutively, that is escalated per
  PROGRAM-OPERATIONS.md §4 as a decision for the human operator to approve —
  it is the **only** thing in this program that requires their sign-off before
  an agent acts; content scope may be cut to protect the date, but the date
  itself is never silently extended.
- Never skip the positive slide or the log step — both are part of the
  session's definition of "done," not optional add-ons.
- Any agent taking over administration reads this file, then
  `BLOCK1-PLAN.md` (or the current block's plan file), then
  `PROGRAM-OPERATIONS.md`, in that order. Full handoff procedure:
  PROGRAM-OPERATIONS.md §7.

---

## Changelog
- **2026-07-24** — Program initialized. `STATE-SHIFU.md`, `BLOCK1-PLAN.md`,
  and `PROGRAM-OPERATIONS.md` authored from the mission brief (Mandarin via
  Chinese history + Yang 24 tai chi, 6-month compression, 150 min/day dose,
  DiSSS/CaFE + Ultralearning + Deep Work + Reality Transurfing method stack).
  Ikanema (NotebookLM) reconciliation could not be run — no NotebookLM
  connector was available in the authoring environment. Logged as an open
  issue, not a blocker; see §6 of PROGRAM-OPERATIONS.md for the closing
  procedure once notebook content is supplied.
