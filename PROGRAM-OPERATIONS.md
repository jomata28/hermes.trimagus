# PROGRAM-OPERATIONS.md — Operations Manual

**Purpose**: a complete, self-contained manual for administering the SHIFU
curriculum (Mandarin via Chinese history + Yang 24 tai chi) from *any*
executor — Claude Code, another LLM agent, an n8n workflow, plain cron +
scripts, or a human with a printed checklist. No step here depends on a
specific model, vendor, or tool. Where a tool is named, it is the *default
implementation of a function*; swap it freely as long as the function is
served. "Hermes" below refers to the parent agent/orchestration system SHIFU
runs under — if there is no Hermes in your executor (e.g. a lone human), read
every "escalate to Hermes" instruction as "flag this prominently and keep
going per the stated fallback," since none of the escalation rules in §4 ever
require pausing the whole program while waiting on a response.

This manual assumes the reader has **no prior context**. If you are a fresh
agent picking this up cold, read §7 (Handoff Protocol) first, then come back
to the top.

---

## 1. Mission & non-negotiables

**Mission**: compress ~2 years of natural-pace progress into 6 months —
Mandarin from absolute zero to solid HSK 3 (touching HSK 4), and Yang 24 tai
chi from a few classes' worth of exposure to the full form performed fluently
from memory with correct structure — using Chinese history as the shared
content spine and tai chi as the embodied-practice track. Full mission
statement: `STATE-SHIFU.md` → MISSION.

**Non-negotiables** (Rules for Shifu, `STATE-SHIFU.md` → RULES FOR SHIFU):
- **Daily dose**: 2.5 hours, protected on the calendar ahead of any other
  work (Rule 2) — 30 min Anki / 2 min slide ritual / 30 min tai chi / 60 min
  input / 30 min output, per `STATE-SHIFU.md` → DAILY PROTOCOL.
- **Timeline never moves silently** (Rule 5) — the only path that can touch
  the 6-month timeline or Block exit bar is the operator-sign-off escalation
  in §4.
- **Weekly review is ≤300 words, ends in exactly one corrective action**
  (Rule 4).
- **Every tai chi movement is logged with its Chinese name** — characters +
  pinyin + tone (Rule 3), not an English label alone.
- **Missed days escalate, never silently reschedule** (Rule 1) — see §4.

---

## 2. State management

### What must persist, and where
`STATE-SHIFU.md` is the single source of truth for program position. Its
sections map to specific kinds of state:

| Section | Holds |
|---|---|
| CURRENT STATUS | Phase/week, per-track pre-launch or in-progress status, history spine position, open blockers (e.g. tutor not booked) |
| METRICS | The weekly-updated numbers: Anki mature/retention, speaking sessions /4, tai chi movements /24 + streak, history spine position, hours actual vs. planned |
| LOG | Append-only session/decision history — never edit or delete a prior entry, only append |

`BLOCK1-PLAN.md` (and its successor `BLOCK2-PLAN.md` once Block 1 exits) is
the content plan: sources, week-by-week curriculum, cron schedule, exit
criteria. It changes far less often than `STATE-SHIFU.md` — only when a
block transition, a plateau-driven encoding swap (Rule 7), or an accepted
Ikenna-Method-style reconciliation touches it.

### Format
Plain markdown tables and bullet lists. No YAML, no database, no proprietary
state store — any executor that can read and edit a text file can run this
program.

### The loop every executor follows, every session
1. **Read state**: open `STATE-SHIFU.md`, read CURRENT STATUS, METRICS, and
   the tail of LOG. Open `BLOCK1-PLAN.md` and find the row under
   WEEK-BY-WEEK matching the current week.
2. **Act**: run the matching runbook from §3 (daily always; Friday/Sunday
   additions per the WEEKLY PROTOCOL; monthly per MONTHLY PROTOCOL).
3. **Write state**: update CURRENT STATUS fields that changed (week number,
   track status, blockers resolved/opened), update METRICS if it's a Sunday
   review, and append one dated LOG line describing what happened. Never end
   a session without this step — an unwritten session did not happen, from
   the next executor's point of view.

If two executors could plausibly run the same day's session, the second one
to write state MUST first check whether today's date already has a LOG entry
and, if so, treat the day as already handled rather than double-logging.

---

## 3. Runbooks

### 3.1 Daily runbook
Trigger: once per calendar day (cron: `0 6 * * * shifu daily-brief` to open
the session, `0 21 * * * shifu daily-log` to close it — `BLOCK1-PLAN.md` §CRON
SCHEDULE).

1. Read state (§2 step 1). If CURRENT STATUS still says "Phase: BLOCK 1 —
   not started," this is Day 1: set Week to 1 and proceed; otherwise use the
   current week number.
2. Positive slide (2 min) — Transurfing visualization, immediately before
   tai chi, not counted in the 2.5h.
3. Anki (30 min) — clear due queue first; new cards at the pace given in
   `STATE-SHIFU.md` DAILY PROTOCOL (~4/day wks 1–2, ~7/day wks 3–4, ~10/day
   wks 5–6+), sourced from the current week's HSK/character-set milestone in
   `BLOCK1-PLAN.md`. Never skipped, including on travel days.
4. Tai chi (30 min) — drill the current week's movement(s) per the
   WEEK-BY-WEEK table, then run every movement learned so far in sequence.
5. Input (60 min) — this week's history/tai-chi source per `BLOCK1-PLAN.md`
   Sources. Once past that source's stated English→Mandarin migration point
   (Week 8 for tai chi instruction, Week 10 for the history podcast), mine
   one new word every 10 minutes into Anki.
6. Output (30 min) — iTalki tutor on a scheduled day (survival Mandarin only
   before Week 6; history/tai-chi topics after), solo shadowing +
   self-recording otherwise.
7. If today is Friday: additionally record the tai chi form on video,
   compare against the Deyin reference, log exactly 3 corrections.
8. Write state: update CURRENT STATUS if a milestone was hit or a blocker
   changed, append a LOG line (date, dose completed y/n, anything notable).
9. Check §4 escalation triggers. If any fire, run that procedure now.

### 3.2 Weekly runbook (Sunday)
Trigger: `0 17 * * 0 shifu weekly-review`.

1. Read state, pull the week's LOG entries.
2. Update METRICS: Anki mature-card count/retention %, speaking sessions
   completed this week (/4), tai chi movements learned (/24) + current
   streak, history spine position, hours actual vs. planned.
3. Write the weekly review — **hard cap 300 words**: adherence summary, the
   metric that moved most/least, and **exactly one** corrective action
   (Rule 4). Decision rule for picking the one action when several issues are
   visible: prioritize whichever of {adherence, tai chi, Mandarin} is
   furthest behind its week-N-of-12 expected pace in `BLOCK1-PLAN.md`; ties
   broken toward tai chi (a physical skill decays faster than SRS-anchored
   vocabulary if neglected for a week).
4. Append the review to LOG (or a separate `REVIEWS.md` if LOG is getting
   long — pick one and stay consistent for the program's duration).
5. Write state.

### 3.3 Monthly runbook
Trigger: `0 9 1 * * shifu monthly-irl`, plus the Month 2 mandatory
in-person checkpoint specifically.

1. Read state.
2. Generate/confirm the month's IRL node task (tai chi school trial class,
   Chinese meetup, or cultural event) and log it.
3. Re-baseline: compare METRICS trend against the week-by-week expected pace
   and promote/demote difficulty for the coming month (e.g., add Anki new-card
   volume if retention is high and ahead of pace; hold volume steady and add
   review-only days if retention is dropping).
4. **Month 2 specifically**: the in-person tai chi correction session is
   mandatory and non-negotiable (video-only practice grooves in structural
   errors that only a live corrector catches). If it cannot be scheduled
   within the month, escalate to Hermes and reschedule within the next 2
   weeks; a slip beyond that window requires operator sign-off per Rule 5,
   since it risks the fixed timeline.
5. At week 12 (end of Block 1): run the gate check against `BLOCK1-PLAN.md`'s
   exit criteria — HSK2 mock ≥80%, Yang 24 performed from memory, 40+ tutor
   sessions logged. All three met → author `BLOCK2-PLAN.md` (HSK3, form
   refinement, push hands intro) and advance. Any one missed → do not
   advance; run one remediation week targeting only the missed criterion,
   then re-check.
6. Write state.

---

## 4. Escalation rules

Every rule below is a decision an executor makes unilaterally and logs —
none require asking the operator, **except** the one item flagged "operator
sign-off required," which is the same one Rule 5 already reserves for
timeline changes.

| Condition | Rule | Source |
|---|---|---|
| 1 day missed | No action — a single miss is normal, log it and continue. | — |
| 2 consecutive days missed | Escalate to Hermes, propose a recovery plan, do not silently reschedule. | Rule 1 |
| iTalki tutor not booked by Day 3 | Escalate to Hermes; Output slot runs on shadowing + self-recording only until booked — does not halt the rest of the program. | Rule 6 |
| A METRICS figure flat across 2 consecutive Sunday reviews (plateau) | Swap the *encoding* for that track only: Anki card direction (recognition↔production), or the Friday-comparison reference source for the stuck tai chi segment. Do not change dose or schedule. | Rule 7 |
| Tai chi injury / physical inability | Suspend the 30-min tai chi slot, redistribute those minutes to Input, until a session logs tai chi minutes > 0 again — that next log entry is itself the "cleared to resume" signal, no separate approval step. | Rule 8 |
| iTalki tutor becomes unavailable/churns | Fall back to shadowing + self-recording for up to 2 weeks. Still unresolved at week 3 → escalate to Hermes, mark that week's speaking metric provisional; does not block the Block 1 gate. | Rule 9 |
| Month 2 in-person correction session can't be scheduled within the month | Escalate to Hermes, reschedule within +2 weeks. Slipping beyond that window is timeline risk. | MONTHLY PROTOCOL |
| Block 1 gate check fails 1 or more of the 3 exit criteria at week 12 | Do not advance to Block 2. Run one remediation week on the missed criterion/criteria only, then re-check. | §3.3 |
| Block 1 gate check still fails the **same** criterion after a remediation week | **Operator sign-off required.** This is the one case the program can't self-correct — log the specific failing criterion in CURRENT STATUS with two remediation options (extend Block 1 by N weeks and compress Block 2, or lower that criterion's bar), and hold there until the operator's next response picks one. Only path that can touch the 6-month end date or an exit criterion (Rule 5). | Rule 5 |

---

## 5. Metrics & review format

**Tracked weekly** (`STATE-SHIFU.md` → METRICS): Anki mature cards /
retention %, speaking sessions completed this week (/4), tai chi movements
learned (/24) + daily streak, history spine era + resource position, hours
actual vs. planned.

**Weekly review template** (Rule 4, ≤300 words):
```
Week N review (YYYY-MM-DD)
Adherence: <days hit full dose>/7. Streak: N days.
Moved most: <one metric, one line, with the number>
Moved least / stalled: <one metric, one line, with the number>
Corrective action (pick exactly one): <the single change for next week>
```

**Friday video-compare ritual** (WEEKLY PROTOCOL): record the form, compare
against the Deyin reference footage, log exactly 3 corrections — no more, no
fewer; forces prioritization instead of an unbounded error list.

**Monthly gate format** (§3.3 step 5, Block 1 only): each of the 3 exit
criteria marked pass/fail with the number or observation that decided it,
then the overall pass/hold.

---

## 6. Ikenna Method principles appendix

**Status: CLOSED on 2026-07-24.** Content was supplied directly by the
operator (pasted notebook summary — no NotebookLM connector was available in
this environment). Reconciled against the real `STATE-SHIFU.md` and
`BLOCK1-PLAN.md` above (note: the source is the "Ikenna Method"; the original
program brief referred to it as "Ikanema" — same source, name corrected here).

| # | Principle | Classification | Disposition |
|---|---|---|---|
| 1 | Two-phase Consume→Output structure, 6–12 month fluency target | ALIGNED | Program already runs Anki/tai-chi/input/output concurrently within a fixed 6-month timeline (aggressive end of Ikenna's own range) |
| 2 | "Soft landing": structured audio pronunciation course first, for correct tones/sounds | ALIGNED | `BLOCK1-PLAN.md` MANDARIN SOURCES already specifies Yoyo Chinese pinyin course / Grace Mandarin tone videos, Weeks 1–2 only, before any other Mandarin input |
| 3 | High-frequency vocab list, 5–10 new words/day, reviewed via SRS | ALIGNED, pace made explicit | The curated HSK 1–2 Anki deck already *is* the high-frequency word list; added an explicit daily new-card pace (~4→7→10/day across wks 1–6) derived from the plan's existing biweekly word-count milestones — `STATE-SHIFU.md` DAILY PROTOCOL |
| 4 | SRS review of all new vocab | ALIGNED | Anki, "never skipped, travel included" (Rule-level in DAILY PROTOCOL) |
| 5 | Native content: L1 support early, upgrade to target-language-only + mine 1 word/10 min once past the beginner threshold | MISSING → added | Program already migrates English→Mandarin sources (history podcast by Week 10, tai chi instruction by Week 8) but had no word-mining mechanic at the migration point; added "mine 1 new word/10 min from migration onward" to both `BLOCK1-PLAN.md` source bullets and `STATE-SHIFU.md` DAILY PROTOCOL |
| 6 | Reading/grammar unlocked only after ~1,000 words + audio program finished | CONFLICT | Ferriss deconstruction (Day 1–2, 12 sentences) exposes the grammar skeleton immediately, before any vocab threshold — intentional, and Ferriss DiSSS/CaFE is a founding, load-bearing method here. **Kept as-is**: exposing the grammar skeleton on Day 1 is specifically how deconstruction is meant to work, and reading proper (graded reader #1) already doesn't start until Weeks 5–6 once ~300 words are banked, which is directionally consistent with Ikenna's gate even if the number differs |
| 7 | Explicit grammar instruction required (anti-Duolingo) | ALIGNED | Ferriss 12-sentence grammar-skeleton deconstruction is explicit from Day 1; no implicit-only tool is in use |
| 8 | Delay full conversational output until ~1,500 words / ~50% comprehension | ALIGNED | Program already stages this: tutor booked Week 1–2, first sessions (survival-only) Week 3–4, first no-English 10-min conversation Week 5–6, topic-specific (history/tai chi) conversation gated to *after Week 6* — the same staging principle, on the program's own timeline |
| 9 | Distribute passive/audio practice into dead time (commute, chores), not only dedicated study time | PARTIAL → added | Anki was already "travel included" flexible; there was no equivalent allowance for passive audio. Added an explicit optional/unlogged dead-time bonus-audio allowance that never substitutes for the protected 2.5h block (Rule 2 stays non-negotiable) — `STATE-SHIFU.md` DAILY PROTOCOL |
| 10 | Avoid low-density, artificially-padded gamified apps (Duolingo pattern); prefer well-designed gamified SRS (Fluyo pattern) when available | ALIGNED, note added | No Duolingo-pattern tool is in use; added an explicit note that a well-designed gamified SRS app is an acceptable swap for Anki since Anki was already a named default, not a hard requirement — `BLOCK1-PLAN.md` MANDARIN SOURCES |
| 11 | For a language already known (maintenance), skip straight to output/native-subtitle stage | N/A | This program is new acquisition of Mandarin, not maintenance of a known language — no current track to apply this to |

### Method-stack mapping (pre-existing, not Ikenna-sourced)

| Principle | Implementation |
|---|---|
| DiSSS — Deconstruction | Day 1–2 Ferriss 12-sentence grammar-skeleton exposure; tai chi broken into 24 canonical movements taught 2–6/fortnight |
| DiSSS — Selection | HSK 1–2 deck (curated high-frequency vocab), not exhaustive vocabulary |
| DiSSS — Sequencing | History spine chronological (Shang/Zhou → Han); tai chi in canonical performance order |
| DiSSS — Stakes | iTalki tutor sessions (public, scheduled output) + Friday self-recorded video vs. reference footage |
| CaFE — Compression | Biweekly milestones give the minimum viable unit per fortnight, not a syllabus dump |
| CaFE — Frequency | Daily 2.5h dose, 7 days/week |
| CaFE — Encoding | Rule 7 (plateau) explicitly changes encoding — card direction or reference video — as the lever when a metric stalls |
| Ultralearning — Directness | Practice is narrating real history / performing the real form / speaking to a real tutor, not isolated drills-for-drills'-sake |
| Ultralearning — Retrieval | Anki by construction; Week 5–6 "10-min conversation, no English" checkpoint |
| Ultralearning — Feedback | Tutor corrections + Friday video-vs-reference comparison, both weekly |
| Deep Work | The 2.5h block is one protected session, calendar-defended ahead of other work (Rule 2) |
| Reality Transurfing — positive slides | Daily 2-min pre-tai-chi visualization (month-6 vision, sensory, first person, no doubt-checking) |

---

## 7. Handoff protocol

A fresh executor (new agent, new harness, new human) taking over cold reads,
**in this exact order**:

1. **`STATE-SHIFU.md`** — CURRENT STATUS answers what week/phase it is and
   what's blocking; METRICS gives the latest numbers; the LOG tail gives
   recent history and any escalations in flight.
2. **`BLOCK1-PLAN.md`** (or the current block's plan file) — find the
   WEEK-BY-WEEK row matching CURRENT STATUS's week number for today's
   specific content, sources, and milestone.
3. **This file, `PROGRAM-OPERATIONS.md`** — §3 for the runbook matching
   today (daily always, plus Friday/Sunday/monthly additions per the cron
   schedule), §4 for what to do if a blocker or escalation condition is live.

That's the complete context set — three files, read in that order, no other
memory required. After acting, the executor writes back to `STATE-SHIFU.md`
per §2 step 3 before ending its session, which is what keeps the *next*
handoff equally clean.

**Handoff self-test**: could a fresh agent administer week 5 using only
these three files? Trace: `STATE-SHIFU.md` CURRENT STATUS would read Week 5.
`BLOCK1-PLAN.md`'s W5–6 row says: Mandarin — HSK1 complete (~300 words),
graded reader #1 started; Tai chi — movements 7–12, Friday video comparisons
begin; History — Warring States, Daoism deepens (无为, 气); Milestone — first
10-min tutor conversation with no English. `PROGRAM-OPERATIONS.md` §3.1 gives
the exact daily session structure (including the Friday-only video-compare
step, which this specific week activates) and the state-update procedure.
No step requires information absent from these three files. Test passes.
