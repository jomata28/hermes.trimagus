# PROGRAM-OPERATIONS.md — Operations Manual

**Purpose**: a complete, self-contained manual for administering the
Mandarin-via-Chinese-history + Yang-24-tai-chi program from *any* executor —
Claude Code, another LLM agent, an n8n workflow, plain cron + scripts, or a
human with a printed checklist. No step in this document depends on a
specific model, vendor, or tool. Where a tool is named, it is the *default
implementation of a function* — swap it freely as long as the function is
served.

This manual assumes the reader has **no prior context**. If you are a fresh
agent picking this up cold, read §7 (Handoff Protocol) first, then come back
to the top.

---

## 1. Mission & non-negotiables

**Mission**: take the operator from current baseline to (a) functional
conversational Mandarin, acquired by narrating Chinese history chronologically,
and (b) unprompted full performance of the Yang 24 tai chi form — in 6 months
(26 weeks) instead of the ~2 years natural pace would take.

**Non-negotiables** (an executor never has discretion to change these without
the escalation in §4):
- **Timeline**: 182 days, start date and end date fixed in `STATE-SHIFU.md
  → program.start_date/end_date`. The end date never moves silently. Scope
  (which grammar patterns, which posture polish) can be cut to protect it;
  the date itself only moves via the §4 escalation, which requires operator
  sign-off.
- **Daily dose**: 150 minutes/day — 30 min SRS_ENGINE (vocab drilling) / 30
  min tai chi / 60 min INPUT_SOURCE / 30 min SPEAKING_PARTNER-or-shadowing.
  Minimum viable day (MVD) floor is 30 minutes (10+10+10 across SRS/tai
  chi/input) — see `STATE-SHIFU.md` daily protocol. Below the MVD floor, the
  day logs as `zero`.
- **Exit criteria are measurable, not vibes-based**: each block ends with a
  gate check against explicit thresholds (see the block's plan file, e.g.
  `BLOCK1-PLAN.md` §"Exit criteria"). A gate result is always one of `pass`,
  `pass-with-flags`, or `hold` — never an unscored judgment call.

---

## 2. State management

### What must persist
All of the following live in `STATE-SHIFU.md`'s `STATE` YAML block, and
nowhere else. If a value is not in that block, it does not exist as far as
any executor is concerned — do not infer program position from side
channels (chat history, memory, file timestamps).

- `program`: mission, start/end date, total weeks, daily dose (fixed, rarely
  edited)
- `position`: current block, current week, current day-in-week, program day
  number
- `adherence`: streak, zero/partial day counts, last session date/status/dose%
- `reviews`: last weekly review date + its one corrective action; last
  monthly gate date + result
- `status`: a single flag (`on-track` / `at-risk` / `plateau` /
  `injury-hold` / `tutor-gap`) plus a list of open issues
- `metrics`: the small set of leading indicators listed in the STATE block
  (Anki maturity, postures learned, form-unprompted boolean, speaking
  minutes, history periods narratable)

### Format
Plain YAML inside a fenced code block inside `STATE-SHIFU.md`. Any executor
capable of reading a text file and parsing YAML can operate this program.
No database, no proprietary state store.

### The loop every executor follows, every session
1. **Read state**: open `STATE-SHIFU.md`, parse the `STATE` block. Open the
   current block's plan file (`BLOCK1-PLAN.md` for weeks 1-12) and find the
   row matching `position.current_week`.
2. **Act**: run the matching runbook from §3 below (daily, or weekly/monthly
   if today is a review day per the cron schedule in the plan file).
3. **Write state**: update every field in `STATE` that the runbook touched
   (position counters, adherence, metrics, status, reviews) and append one
   line to `STATE-SHIFU.md`'s Changelog. Never end a session without this
   step — an unwritten session did not happen, from the next executor's
   point of view.

If two executors could plausibly run the same session (e.g. a cron job and a
human both trigger the daily runbook), the second one to write state MUST
first re-read the file to check whether `last_session_date` already equals
today; if so, treat the day as already logged and skip re-logging (idempotency
guard — prevents double-counting streaks/metrics).

---

## 3. Runbooks

### 3.1 Daily runbook
Trigger: once per calendar day, per the cron schedule in the current block's
plan file.

1. Read state (§2 step 1).
2. If `position.current_week == 0`: this is day 1. Set `start_date` = today
   if not already set, `current_week = 1`, `current_day_in_week = 1`,
   `program_day_number = 1`. Otherwise increment `current_day_in_week`
   (roll to 1 and increment `current_week` if it exceeds 7) and
   `program_day_number`.
3. Look up today's row in the current block's plan file weekly table.
4. Run the 150-minute session in order: positive slide (2 min, not counted)
   → SRS_ENGINE due-queue (30 min) → tai chi, current week's posture(s) then
   full sequence-so-far (30 min) → INPUT_SOURCE on this week's unit, shadow
   at least 10 min of it aloud (60 min) → SPEAKING_PARTNER on scheduled
   tutor days, solo shadowing + self-recorded narration on non-tutor days
   (30 min).
5. Compute `dose_pct` = minutes actually completed / 150. Classify:
   `dose_pct >= 100%` → `full`; MVD floor met (≥30 min across the 3
   MVD-eligible components) but <100% → `partial`; below MVD floor → `zero`.
6. Update `adherence`: if status is `full` or `partial`, `streak_days += 1`
   (update `longest_streak` if exceeded); if `zero`, `streak_days = 0`.
   Recompute `zero_days_last_14` / `partial_days_last_14` by counting the
   last 14 Changelog entries.
7. Update any `metrics` that moved (new mature Anki cards, a posture newly
   drilled to completion, speaking minutes logged, etc.) — pull these from
   whatever the SRS_ENGINE/FORM tools report; if a tool doesn't report a
   number automatically, the executor (human or agent) enters it from
   direct observation of the session just run.
8. Write state (§2 step 3).
9. Check escalation triggers (§4). If any fire, run that escalation's
   procedure now, in the same session.

### 3.2 Weekly runbook
Trigger: once per program week, per the plan file's cron schedule (default:
end of program week, i.e. after 7 program days have been logged).

1. Read state.
2. Pull the last 7 daily Changelog entries.
3. Write the weekly review — **hard cap 300 words** — covering exactly:
   dose adherence (X/7 full, Y/7 partial, Z/7 zero), the single metric that
   moved most (or least), and **exactly one** corrective action for next
   week. Do not list multiple corrective actions — if more than one issue is
   visible, pick the one blocking the most progress and defer the rest.
   Decision rule for picking it: prioritize whichever of {adherence, tai
   chi, Mandarin} is furthest behind its week-N-of-26 expected pace; ties
   broken toward tai chi (physical skill decays faster than SRS-anchored
   vocabulary if neglected).
4. Append the review to `STATE-SHIFU.md` Changelog (or a `REVIEWS.md` log
   file if the Changelog is getting unwieldy — either is acceptable, pick
   one and stay consistent for the rest of the program).
5. Update `reviews.last_weekly_review_date` and
   `last_weekly_review_corrective_action`.
6. Write state.

### 3.3 Monthly runbook (gate check)
Trigger: at the end of weeks 4, 8, 12, 16, 20, 24, and the final week of the
program (per the current block's plan file).

1. Read state.
2. Evaluate the current block's plan file "Exit criteria" section — for
   Block 1, `BLOCK1-PLAN.md`'s three numbered criteria — as boolean pass/fail
   using the thresholds given there (self-assessment against the recorded
   video / tutor rating / Anki metrics, no subjective override).
3. Score: 3/3 → `pass`; 2/3 → `pass-with-flags`; ≤1/3 → `hold`.
4. `pass`: advance to the next block. If no plan file exists yet for the
   next block, author one now, following the same structure as
   `BLOCK1-PLAN.md` (weekly table, sources, cron schedule, exit criteria),
   scoped to the next 4-12 weeks and continuing the chronological/canonical
   sequencing this block established.
5. `pass-with-flags`: advance to the next block, but that block's week 1
   plan is amended to prioritize the missed criterion before new material.
6. `hold`: do NOT advance. Run the §4 plateau/at-risk escalation instead.
7. Update `reviews.last_monthly_gate_date/result`, `status.flag` if changed.
8. Write state.

---

## 4. Escalation rules

Every rule below is a decision an executor makes unilaterally and logs — none
of them require asking the operator, **except** the one item flagged
"operator sign-off required."

| Condition | Rule | Resulting status flag |
|---|---|---|
| 1 zero day | No action. Single misses are normal; the MVD floor exists precisely so a bad day doesn't cascade. | unchanged |
| 2 consecutive zero days | Next session opens with an extra positive slide (5 min instead of 2) reframing the miss non-judgmentally, then proceeds normally. Log it. | `at-risk` |
| 3+ zero days in a rolling 7-day window | Cut that week's *new* content to zero — the week's session becomes 100% review/consolidation of prior weeks until 3 consecutive `full`/`partial` days are logged, then resume the plan file's schedule from wherever it left off (do not skip missed units — shift them right). | `at-risk` |
| A monthly gate returns `hold` | Run one additional "remediation week" (same structure as the block's review week, e.g. Block 1's week 6) focused only on the failed criteria, then re-run the gate check. Do not advance the block in the meantime. | `plateau` |
| A monthly gate returns `hold` **twice in a row** on the same criteria | **Operator sign-off required.** This is the one case where the program cannot self-correct — flag `open_issues` in `STATE-SHIFU.md` with the specific failing criteria and two remediation options (extend this block by N weeks and compress a later one, or reduce this block's exit bar), and stop advancing until the operator's next session response picks one. This is the only path that can touch `program.end_date` or the exit criteria themselves. | `hold` (frozen) |
| Plateau: a metric hasn't moved for 2 consecutive weekly reviews | Change the *encoding* (CaFE) for that track only: e.g. switch Anki card format (recognition→production) or switch the tai chi FORM_REFERENCE video/instructor for that posture group. Do not change dose or schedule. Log the swap. | `plateau` until the metric moves again |
| Injury / physical inability to perform tai chi | Suspend the tai chi 30-min slot; redistribute those 30 min to INPUT_SOURCE (extra Mandarin listening/reading) until the operator logs a session with tai chi minutes > 0 again, which is read as "cleared to resume." No approval step needed to pause; resuming is self-evidenced by the operator's own next log entry. | `injury-hold` |
| SPEAKING_PARTNER (tutor) unavailable/churned | Substitute solo shadowing + self-recorded narration, scored by comparing today's recording to the prior week's on: fluency of unprompted recall (not pronunciation). Continue substituting for up to 2 weeks; if still unresolved at week 3, this is a `tutor-gap` flag but does NOT block gate checks — the Block 1 exit criterion #2 tutor rating is instead self-scored against the same rubric and marked provisional in the gate check log. | `tutor-gap` |

---

## 5. Metrics & review format

**Leading indicators tracked every day** (in `STATE-SHIFU.md → metrics`):
Anki mature-card count, 7-day average due-queue size, postures learned
(of 24), full-form-unprompted boolean, cumulative speaking minutes, history
periods narratable (of 8 in Block 1).

**Weekly review format** (§3.2) — reproduced here as the canonical template:

```
Week N review (YYYY-MM-DD)
Adherence: X/7 full, Y/7 partial, Z/7 zero. Streak: N days.
Moved most: <one metric, one line, with the number>
Moved least / stalled: <one metric, one line, with the number>
Corrective action (pick exactly one): <the single change for next week>
```
Hard cap 300 words total. If it's running long, cut narrative and keep numbers
— the point is a fast, honest pulse-check, not a report.

**Monthly gate format** — the three (or however many the current block
defines) criteria, each marked pass/fail with the one number or observation
that decided it, then the overall `pass` / `pass-with-flags` / `hold`.

---

## 6. Ikanema principles appendix

**Status: OPEN.** At program authoring time (2026-07-24), the "Ikanema"
NotebookLM notebook referenced in the original program brief could not be
read — no NotebookLM connector or MCP tool was available in the authoring
environment, and no notebook export was supplied as text. Rather than invent
placeholder "principles" and misattribute them to the operator's actual
notebook, this section is left as a structured template. This does **not**
block program execution: `STATE-SHIFU.md` and `BLOCK1-PLAN.md` are already
fully specified against the four named methodologies (§1/§6 mapping below),
which are independently sufficient to run the program.

**To close this out**, any executor — including a future session with
NotebookLM access, or the operator pasting the notebook's content directly —
follows this exact procedure:

1. Extract every principle/technique/heuristic from the Ikanema notebook as a
   flat list, one line each.
2. For each, classify against the current `STATE-SHIFU.md` +
   `BLOCK1-PLAN.md`:
   - **ALIGNED** — already implemented; cite the section/line implementing it.
   - **MISSING** — not implemented; write the concrete addition (a specific
     edit to a specific file/section, not a vague intention).
   - **CONFLICT** — contradicts something already decided; state both sides
     in one sentence each, pick one, justify the pick in ≤2 sentences. Default
     tiebreak when genuinely unresolvable: the method already load-bearing in
     `STATE-SHIFU.md` wins, since ripping out working infrastructure this late
     costs more than the marginal gain of a new technique — log the
     alternative as a Block 2 candidate instead of blocking Block 1.
3. Apply all ALIGNED confirmations (no file changes needed, just note them
   here), all MISSING additions (edit `STATE-SHIFU.md`/`BLOCK1-PLAN.md`
   directly), and the winning side of each CONFLICT.
4. Any change that would extend `program.end_date` beyond 182 days is
   **operator sign-off required** per §4 — flag it, do not apply it
   unilaterally.
5. Replace this section's status line with `Status: CLOSED on <date>` and
   list the final principle table (principle → ALIGNED/MISSING/CONFLICT →
   disposition) in place of this procedure.

### Method-stack mapping (already implemented, not Ikanema-sourced)

| Principle | Implementation |
|---|---|
| DiSSS — Deconstruction | History spine broken into 8 eras; tai chi broken into 24 canonical postures + stance fundamentals (`BLOCK1-PLAN.md`) |
| DiSSS — Selection | ~15-25 highest-frequency content words per era, not exhaustive vocab; grammar patterns chosen for reuse across every later week |
| DiSSS — Sequencing | Chronological (history) / canonical (tai chi) order, so every unit re-activates everything prior |
| DiSSS — Stakes | Weekly tutor session (Mandarin) + weekly self-recorded video (tai chi) — public/recorded output on a fixed schedule |
| CaFE — Compression | Weekly table gives the minimum viable unit per week, not a syllabus dump |
| CaFE — Frequency | Daily 150-min dose, 7 days/week, no dose holidays built in |
| CaFE — Encoding | Plateau rule (§4) explicitly changes encoding (card format, reference video) as the lever when a metric stalls |
| Ultralearning — Metalearning | This document + the plan files, read before any session, is the meta-map |
| Ultralearning — Directness | Practice is narrating real history / performing the real form, not isolated drills-for-drills'-sake |
| Ultralearning — Drill | Weak-point drilling is exactly what the MVD floor and plateau-encoding-swap protect |
| Ultralearning — Retrieval | SRS_ENGINE by construction; weekly "narrate everything so far unprompted" checkpoints |
| Ultralearning — Feedback | Tutor corrections + self-recorded video comparison, both weekly |
| Deep Work | 150-min block is a single protected session, not scattered micro-sessions; cron schedule fixes its position in the day |
| Reality Transurfing — positive slides | Daily 2-min pre-session visualization; non-judgmental logging language in the 2-zero-day escalation rule |

---

## 7. Handoff protocol

A fresh executor (new agent, new harness, new human) taking over cold reads,
**in this exact order**:

1. **`STATE-SHIFU.md`** — parse the `STATE` YAML block. This alone answers:
   what day/week/block is it, what's the adherence streak, what's the status
   flag, what (if anything) is open in `open_issues`.
2. **The current block's plan file** (`BLOCK1-PLAN.md` for
   `position.current_block == 1`; a `BLOCK2-PLAN.md` etc. will exist once
   Block 1's gate passes) — find the row matching `position.current_week` to
   know today's specific content.
3. **This file, `PROGRAM-OPERATIONS.md`** — §3 for the runbook matching
   today (daily always; weekly/monthly if the plan file's cron schedule says
   so), §4 for what to do if `status.flag` is anything other than
   `on-track`.

That's the complete context set — three files, read in that order, no other
document or memory required. After acting, the executor writes back to
`STATE-SHIFU.md` per §2 step 3 before ending its session, which is what makes
the *next* handoff (to whatever executor picks it up next) equally clean.

**Handoff self-test**: could a fresh agent, given only these three files,
correctly administer week 5 *if the program had progressed that far*? Trace
(hypothetical — as of authoring, actual `STATE-SHIFU.md` state is
`current_week: 0`, program not yet started): if `STATE-SHIFU.md` instead
read `current_block: 1, current_week: 5`, `BLOCK1-PLAN.md`'s week 5 row says
Single Whip / Wave Hands Like Clouds, Han dynasty unit, 了/过 aspect markers,
tutor Tue/Sat. `PROGRAM-OPERATIONS.md` §3.1 gives the exact 150-minute
session structure and the state-update procedure. No step requires
information not present in these three files. Test passes.
