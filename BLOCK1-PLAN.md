# BLOCK 1 — Weeks 1–12: Foundation
Chinese (zero → HSK 2 exit) · Tai chi (zero → Yang 24 complete, rough) · History spine (origins → Han)

## TAI CHI SOURCES (video-first path)
**Primary course (pick ONE, follow linearly):**
1. **YMAA — Master Yang, Jwing-Ming / Helen Liang (Yang 24)** — the most rigorous free+paid option. Structured step-by-step, front + rear views, martial applications explained. YouTube: youtube.com/ymaa; apps/DVDs for the full course. Best if you want depth and lineage (traces to Yang Chengfu).
2. **Chris Pei (BodyWisdom) — "24 Yang Style Tai Chi Form, Full Beginner Instruction"** — free on YouTube, single structured progression of the Yang 24, well-paced for self-learners. Best free complete course.
3. **David-Dorian Ross / Tai Chi Made Easy** — most beginner-friendly pacing, strong on principles; less martial depth.

**Supplementary:**
- **Master Yijiao Hong — Yang 24 segmented series** (YouTube) — each of the 24 movements as its own lesson; use as your per-movement reference when drilling.
- **Dr. Paul Lam — Tai Chi for Health** — slow, safety-focused; use his warm-up sequence as your daily opener.
- **Deyin Taijiquan Institute** (Master Faye Yip lineage) — competition-standard Yang style reference footage for Friday video comparisons.
- **Adam Mizner — Heaven Man Earth** — internal principles (song/relaxation, peng). Watch conceptually from Month 2; do not imitate before basics.

**Recommended stack:** YMAA or Chris Pei as spine · Yijiao Hong for per-movement drilling · Deyin footage as your Friday comparison standard · Paul Lam warm-up daily.
**Chinese-language bonus:** once at ~Week 8, watch native-Chinese tai chi instruction (search 二十四式太极拳教学) — instruction becomes comprehensible input, and from this point mine one new word every 10 minutes into Anki (Ikenna Method upgrade trigger — see STATE-SHIFU.md LOG, 2026-07-24).

## MANDARIN SOURCES
- **Anki:** start with a curated HSK 1–2 deck + custom deck of tai chi movement names (I generate this). HSK 1–2 already functions as the Ikenna Method's high-frequency word list; a well-designed gamified SRS app is an acceptable 1:1 swap for Anki if it serves the same due-queue function without padding simple content into long low-density sessions (avoid Duolingo-pattern tools).
- **Pronunciation (Weeks 1–2 only):** Yoyo Chinese pinyin course or Grace Mandarin tone videos; Ferriss-style minimal-pair tone drills
- **Comprehensible input:** Little Fox Chinese → Chinese史 graded readers (Mandarin Companion Level 1) → "Story Learning Chinese with Annie"; history podcasts in English initially (The History of China podcast) migrating to TeaTime Chinese by Week 10 — from that migration onward, mine one new word every 10 minutes into Anki (Ikenna Method upgrade trigger)
- **Speaking:** iTalki community tutor 4x/wk, 30 min ($8–12/session). Instruction to tutor: history + tai chi topics only after Week 6; pure survival Mandarin before.
- **Ferriss deconstruction:** Day 1–2 = his 12 sentences translated to Mandarin to expose grammar skeleton (no conjugation, SVO, aspect particles 了/过, measure words)

## WEEK-BY-WEEK
**W1–2 · Sound system + skeleton**
- Mandarin: pinyin complete, 4 tones + tone pairs drilled daily, Ferriss 12 sentences, first 50 Anki cards (pinyin-only)
- Tai chi: course selected; Paul Lam warm-up + movements 1–2 (起势 qǐshì, 野马分鬃 yěmǎ fēnzōng)
- History: Shang/Zhou overview (podcast, English)
- Milestone: pass a self-recorded tone-pair test; book iTalki tutor

**W3–4 · Characters begin**
- Mandarin: switch Anki to characters (radicals first), HSK1 vocab ~150, first tutor sessions (introductions, numbers, survival)
- Tai chi: movements 3–6 (白鹤亮翅, 搂膝拗步...)
- History: Spring & Autumn, Confucius vs. Laozi — 道 dào enters your vocab from philosophy, not a textbook
- Milestone: 3-sentence self-intro from memory

**W5–6 · Momentum**
- Mandarin: HSK1 complete (~300 words), graded reader #1 started
- Tai chi: movements 7–12; Friday video comparisons begin
- History: Warring States, Daoism deepens (无为 wúwéi, 气 qì — now your tai chi vocabulary IS your history vocabulary)
- Milestone: first 10-min tutor conversation with no English

**W7–8 · First integration**
- Mandarin: HSK2 vocab begins; describe tai chi movements to tutor in Mandarin
- Tai chi: movements 13–18; sectional run-throughs (1–18 continuous)
- History: Qin unification, Legalism
- Milestone: perform movements 1–12 from memory, no video

**W9–10 · Compression**
- Mandarin: HSK2 ~450 cumulative words; TeaTime Chinese podcast entry
- Tai chi: movements 19–24 — full form learned
- History: Han dynasty, Daoism institutionalizes
- Milestone: full Yang 24 run-through (rough is fine)

**W11–12 · Consolidation + exam**
- Mandarin: HSK2 mock test; 15-min free conversation
- Tai chi: daily full-form runs; record final Block 1 video vs. Week 5 video
- IRL: attend one in-person class/trial in Houston (Month 2 checkpoint — mandatory correction session)
- Exit criteria: HSK2 mock ≥80% · Yang 24 from memory · 40+ tutor sessions... if met → Block 2 (HSK3 + form refinement + push hands intro)

## CRON SCHEDULE (VPS / Hermes)
```cron
# SHIFU curriculum agent
0 6 * * *   shifu daily-brief      # today's Anki target, form segment, input resource, slide reminder
0 21 * * *  shifu daily-log        # prompt: log hours, streak, blockers → append STATE.md
0 18 * * 5  shifu video-compare    # Friday: record form, compare vs Deyin reference, log 3 corrections
0 17 * * 0  shifu weekly-review    # compile metrics, ≤300 words, 1 corrective action
0 9 1 * *   shifu monthly-irl      # generate IRL task: school trial / meetup / cultural event
0 9 * * 1   shifu tutor-check      # verify 4 iTalki sessions booked this week
```

## TRANSURFING SLIDE (pre-tai-chi, 2 min)
Construct once, run daily: you at month 6 — flowing through the full 24 form in a Houston park, exchanging comments in Mandarin with a Chinese practitioner afterward. Sensory detail, first person, no doubt-checking. The slide precedes practice; practice makes the slide true.
