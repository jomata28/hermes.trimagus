# BLOCK1-PLAN.md — Weeks 1–12 ("Foundations")

Companion to `STATE-SHIFU.md` (current position, metrics, operating rules) and
`PROGRAM-OPERATIONS.md` (runbooks any executor follows). This file is the
detailed content plan for program weeks 1–12 only. Weeks 13–26 (Block 2) get
their own plan file, authored no later than the Block 1 exit review (week 12).

Daily dose is fixed at 150 min/day per `STATE-SHIFU.md`: 30 Anki / 30 tai chi
/ 60 input / 30 speaking. This file specifies *what content* fills each of
those slots, week by week, and does not change the daily structure.

## Design rationale (DiSSS/CaFE applied)

- **Deconstruction**: Mandarin is split into tones+pinyin, a core hanzi/radical
  set, and grammar patterns, taught against a **chronological Chinese history
  spine** so vocabulary is always acquired inside a narrative, not a list.
  Tai chi is split into the 24 canonical postures, taught in their standard
  performance order in groups of 2, plus stance/weight-shift fundamentals in
  week 1.
- **Selection**: history units use the highest-frequency ~15-25 content words
  per era (rulers, era-defining nouns, one or two verbs), not exhaustive
  vocabulary. Grammar patterns are selected for reuse across every later unit
  (是/有/在 in week 2 get used in every week after).
- **Sequencing**: both tracks move chronologically/canonically so each new
  unit builds on and re-activates everything before it (retrieval practice is
  built into the sequencing itself, not bolted on).
- **Stakes**: weekly tutor session is the stakes mechanism for Mandarin
  (must produce spoken output in front of another person on a schedule);
  weekly self-recorded video is the stakes mechanism for tai chi (must show
  visible progress against last week's recording).

## Weekly table

| Wk | Tai chi (new postures) | Mandarin/history unit | Grammar/pattern focus | Tutor day(s) |
|----|------------------------|------------------------|------------------------|---------------|
| 1  | Stance & weight-shift fundamentals; Commencing Form; Part Wild Horse's Mane (L/R/L) | Tones + pinyin system; numbers, dates, time words (年/世纪/朝代); legendary era (三皇五帝) | Tone pairs drilling only, no sentence grammar yet | Sat |
| 2  | White Crane Spreads Wings; Brush Knee Twist Step (L/R/L) | Xia & Shang dynasty (王/朝/青铜/甲骨文) | 是, 有, 在 | Tue, Sat |
| 3  | Hand Strums the Lute; Step Back Repulse Monkey | Zhou dynasty + Warring States (诸侯/战国/思想家) | Question words (谁/什么/哪儿/为什么); basic verbs | Tue, Sat |
| 4  | Left Grasp Sparrow's Tail; Right Grasp Sparrow's Tail | Qin dynasty (统一/长城/秦始皇) | Measure words (个/条/座) | Tue, Sat + **monthly gate** |
| 5  | Single Whip; Wave Hands Like Clouds | Han dynasty (丝绸之路/汉字/汉朝) | Aspect markers 了 / 过 | Tue, Sat |
| 6  | Review + consolidate postures 1–10; first slow full run-through with prompts allowed | Consolidation: narrate legendary era → Han aloud, unprompted | Free recombination of weeks 1–5 patterns | Tue, Sat |
| 7  | High Pat on Horse; Kick with Right Heel | Three Kingdoms/Jin/Sui (三国/分裂/统一) | 比 comparatives | Tue, Sat |
| 8  | Strike Ears with Both Fists; Turn and Kick with Left Heel | Tang dynasty (盛世/诗/长安) | 因为...所以 / 虽然...但是 | Tue, Sat + **monthly gate** |
| 9  | Snake Creeps Down + Golden Rooster Stands on One Leg (L then R) | Song dynasty (科技/印刷术/火药) | 的 relative clauses | Tue, Sat |
| 10 | Fair Lady Works the Shuttles (L/R); Needle at Sea Bottom; Fan Through the Back | Yuan & Ming dynasty (蒙古/郑和/明朝) | Narrative connectors (然后/后来/于是) | Tue, Sat |
| 11 | Turn/Deflect/Parry/Punch; Apparent Close Up; Cross Hands; Closing Form | Qing dynasty + early modern transition (清朝/鸦片战争) | Review all patterns, no new grammar | Tue, Sat |
| 12 | Full unprompted run-through of all 24 postures, self-recorded | Capstone: narrate legendary era → Qing chronologically, unprompted, to tutor | — | Tue, Sat + **Block 1 exit review** |

All 24 Yang-form postures are covered by end of week 11; week 12 is
integration and assessment only, no new material on either track.

## Sources (function → default implementation; swap the implementation freely)

| Function | What it must do | Default implementation |
|---|---|---|
| SRS_ENGINE | Spaced repetition of vocab/hanzi with due-queue tracking | Anki, deck per week's unit, tags = dynasty name |
| FORM_REFERENCE | Canonical, correct demonstration of each posture, replayable | A single consistent Yang 24 instructional video series (same instructor throughout, for consistency of cueing) |
| FORM_FEEDBACK | Catches structural errors invisible to the self | Weekly self-recorded video, compared side-by-side against FORM_REFERENCE |
| INPUT_SOURCE | Comprehensible Mandarin content on this week's history unit, at a level ~10% above current ability | A graded-Mandarin history course/channel with subtitle toggle; fall back to written graded readers if no video exists for a given era |
| SPEAKING_PARTNER | Live, corrective, scheduled spoken output practice | iTalki (or equivalent live-tutor marketplace) tutor, 2x/week per the table above |

## Cron schedule (adjust clock times to local timezone; do not change cadence)

```
# Daily deep-work block (Mon-Sun) — see STATE-SHIFU.md daily protocol for the internal 4-part split
30 6 * * *   run-daily-session       # positive slide + Anki + tai chi + input + speaking-or-shadow
0 21 * * *   log-daily-session       # write session status/dose_pct/metrics to STATE-SHIFU.md if not already logged

# Weekly review — see PROGRAM-OPERATIONS.md §3
0 20 * * 0   run-weekly-review       # Sunday, end of program week

# Monthly gate — only fires on weeks 4, 8, 12 (checked inside the job, not the cron expression)
0 19 * * 0   run-monthly-gate-check  # Sunday evening, same day as weekly review on gate weeks
```

## Exit criteria — Block 1 (end of week 12)

All of the following must be true for the monthly gate to return `pass`.
Partial success (2 of 3 true) returns `pass-with-flags` and Block 2 starts
with the missed item as its first-week priority. Fewer than 2 true returns
`hold` — see `PROGRAM-OPERATIONS.md` §4 for what `hold` triggers.

1. **Tai chi**: full 24-posture form performed unprompted (no verbal/video
   cueing) from a single self-recording, in the correct order, without
   stopping. Individual posture precision is not graded at this checkpoint —
   sequence completeness and continuity are.
2. **Mandarin**: chronological narration of legendary-era-through-Qing (the
   10 history units above — weeks 1,2,3,4,5,7,8,9,10,11; weeks 6 and 12 are
   consolidation, not new eras) delivered unprompted to the tutor in Mandarin,
   using at least 6 of the 8 grammar patterns from the weekly table, tutor
   rates it comprehensible without English fallback.
3. **Anki**: ≥80% of cards introduced in weeks 1-11 are at "mature" SRS
   interval (≥21 days) by end of week 12, and 7-day rolling due-queue
   completion rate ≥90% (from `STATE-SHIFU.md` metrics).
