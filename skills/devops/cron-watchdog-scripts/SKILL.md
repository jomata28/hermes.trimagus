---
name: cron-watchdog-scripts
description: Build and operate no_agent cron watchdog/monitor scripts — polling scripts that deliver alerts to Telegram only when something changes. Covers the stdlib-only rule, silent-unless-news output, orchestrator wrappers, false-positive hardening (grace periods, dedupe, thresholds), timezone-aware scheduling, and testing under cron's actual Python.
version: 1.0.0
author: Hermes Agent
category: devops
metadata:
  hermes:
    tags: [cron, monitoring, watchdog, telegram, alerts, no-agent]
---

# Cron Watchdog Scripts

Class-level playbook for recurring monitoring jobs created with
`cronjob(no_agent=True, script='...')`: the script IS the job, stdout is
delivered verbatim to the target, and **empty stdout = silent** (no message).

## When to use
- Polling monitors (API status, flight schedules, disk/memory, price changes)
- Any recurring job where the output is a fixed-shape alert, not reasoning
- User says "just alert me when X happens" / "don't waste tokens"

## Golden rules

### 1. STDLIB ONLY — no third-party imports in the script itself
Cron runs the script with the **system python**, not any venv you used
during development. A script that imports pandas/requests will crash on
every cron run while your interactive tests (inside the venv) pass.
This is the #1 silent-killer bug: the job reports `last_status: ok`
(cron considers "the script ran" a success even when it crashed) while
producing nothing useful.

- Use `urllib.request` instead of `requests`, `csv`/`json` instead of pandas.
- Verify exactly as cron will run it: `cd /root/.hermes/scripts && python3 script.py`
  (bare `python3`, NOT `source .venv/bin/activate`).
- If a multi-part pipeline exists, wrap it in an orchestrator that checks
  each subprocess's exit code and prints `⚠️ ... crashed: <stderr tail>` —
  a crash must surface as a message, never silence.

### 2. Silent unless news
With `no_agent=True`, EVERY non-empty stdout becomes a Telegram message.
A monitor that prints "✅ all good" every poll spams the user
(5-min poll = ~288 messages/day). Design output so the happy path prints
NOTHING. Only print on: detection, state change, or hard errors
(token expired, repeated fetch failure).

### 3. Dedupe alerts across runs
Persist a set of already-alerted event keys (JSON file) so the same event
never alerts twice. Prune the set periodically (e.g., keep last ~1000).

### 4. Grace periods and thresholds
- **Removal/disappearance detection**: require N consecutive misses
  (2+ polls) before alerting — a single transient fetch failure must not
  flag dozens of false "vanished" events. Carry a `missing_polls` counter
  in the cache for items absent this run.
- Increment missing counters only for scopes whose fetch succeeded. A failed
  hub/date/API partition must preserve counters unchanged; otherwise the next
  successful poll can falsely satisfy the consecutive-miss guard.
- Snapshot pipelines must be atomic and complete: retry transient requests,
  then abort without saving if any required partition remains missing. A
  partial snapshot is indistinguishable from a mass cancellation to a diff.
- Identify observations by full snapshot timestamp, not calendar date. If a
  monitor runs multiple times daily, counting distinct dates turns “2
  snapshots” into an accidental 24-hour confirmation delay.
- **Change detection**: set a minimum-change threshold (e.g., schedule
  shifts ≥ 30 min) so routine micro-corrections don't alert.
- **Transient HTTP errors**: skip silently; only auth errors (401/expired
  token) deserve an alert — and dedupe those too (one per day).

## Orchestrator wrapper pattern
When the job = snapshot + analysis, keep the parts as separate scripts and
add a small orchestrator that gates delivery:

```python
#!/usr/bin/env python3
import subprocess, sys
SCRIPTS = "/root/.hermes/scripts"

# 1. Run each part, capture output
r = subprocess.run([sys.executable, f"{SCRIPTS}/part_one.py"],
                   capture_output=True, text=True, timeout=600)
failed = r.returncode != 0  # or check for a success marker in r.stdout

# 2. Gate: print ONLY if there is news or a hard failure
if failed:
    print(f"⚠️ part_one FAILED: {r.stdout[-300:]} {r.stderr[-300:]}")
elif has_actionable_news(r.stdout):
    print(r.stdout)
# else: print nothing → no Telegram message
```
Progress/verbosity from the parts stays suppressed; only alerts escape.

## Scheduling & timezones
- **Cron expressions are UTC.** Convert to the user's local time before
  choosing hours (JT = America/Chicago; UTC−6/−5). A "daily 09:00" cron
  fires at 4am CT.
- Match snapshot times to when the source system makes decisions (e.g.,
  airline ops decide during business hours → snapshot mid-morning, late
  afternoon, and evening).
- Multiple snapshots/day narrow the *time window* of a detected change:
  3×/day pins a disappearance to a 5–8h window. Schedule example:
  `0 3,15,22 * * *` UTC = 10pm, 10am, 5pm CT.
- Long polling scripts (hundreds of API calls): run as background terminal
  jobs with `notify_on_complete=true` during development; cron needs the
  script to finish within its timeout.

## State & tokens
- Keep state in a dedicated dir (`~/.hermes/<job_name>_state/`): cache JSON,
  history JSON, alerted-keys JSON.
- Expiring auth: read token from a file (`~/.hermes/<name>_token`); on auth
  failure print ONE deduped "token expired — refresh" message.
- Persist accumulating history across runs (confirmation logic that needs
  "absent in 2+ consecutive snapshots" can never fire from in-run state alone).

## Filenames
Timestamped state files that can be written more than once per day MUST
include the time (`schedule_2026-08-06_1437.csv`), or same-day runs
overwrite each other and destroy the diff baseline. Sort by full filename.

## Pitfalls
- **Scope creep on review**: when asked to review/fix one pipeline, change
  only that pipeline. Do not prune config (hub lists, endpoints, targets)
  based on unverified claims about the user's domain — ask or leave as-is.
- **"last_status: ok" lies**: cron reports ok if the script exited; a crash
  inside a subprocess wrapper can still print exit 0. Always have the
  orchestrator inspect child stderr and report failures explicitly.
- **Testing in the wrong environment**: interactive success under a venv
  proves nothing about cron. Always re-run with the bare system interpreter.
- **Alert fatigue kills the monitor**: the moment a watchdog spams, the user
  mutes it and the one real alert dies too. Silence is the default; earn
  every message.

## Validation of disappearance signals
For airline schedules, inventory feeds, event listings, and similar sources, a disappearance is only a candidate until independently verified. Use `references/disappearance-monitor-validation.md` for paired API/web observations, ground-truth labeling, lead-time metrics, boundary controls, and retime/renumber pitfalls.

- Do not interpret repeated zero disappearances as zero real-world events. First test whether the upstream endpoint is a live operational feed or an append-only/published timetable whose cancelled items remain listed.
- Add a second source that exposes explicit operational state (`status`, `statusCode`, `canceled`) and validate it on a real item before scheduling. Restrict expensive public-page checks to near-event candidates from the primary cache rather than scraping the entire inventory.
- For pages embedding JavaScript state such as `__NEXT_DATA__ = {...}`, parse with `json.JSONDecoder().raw_decode()` starting after the assignment. A non-greedy regex ending at `</script>` can stop at an inner brace or include trailing JavaScript and fail with `Extra data`.
- A validator must fail closed: record parser failure counts, alert on systemic failure, and never convert an unreadable page into a normal/non-cancelled status.
- For airline monitoring, distinguish **published schedule** from **operational status**. A cancelled flight may remain in a timetable endpoint indefinitely; zero disappearances therefore do not establish zero cancellations. Prefer an explicit field such as `operatingStatus == CANCELLED`, with disappearance only as a secondary candidate signal.
- Before replacing a working confirmation layer with a “better” native endpoint, replay the native request independently from the cron host, verify schema and latency, and test repeated unattended calls. If it times out or becomes unstable, retain the working layer until the replacement passes—do not disable first and debug later.
- For undocumented public-web APIs, poll only relevant flights at a conservative interval, cache by `(date, flight)`, back off on `429`/`5xx`, and avoid passenger/booking data.
- Viva-specific evidence, endpoint contract, and source hierarchy live in `references/viva-operational-status-validation.md`.

## Verification checklist before declaring done
1. `cd ~/.hermes/scripts && python3 <script>.py` → exit 0, output as expected
2. Happy path prints nothing (or the orchestrator gates it to nothing)
3. Synthetic change injected → exactly one alert, correct shape
4. Re-run → no duplicate alert (dedupe works)
5. `cronjob action=list` → schedule, script name, deliver target all correct

## Reference implementation
The Viva Aerobus flight-disruption monitor is the canonical instance:
`viva_snapshot.py` + `viva_diff.py` + `viva_daily.py` (orchestrator) +
`irop_monitor.py` in `/root/.hermes/scripts/`, cron jobs "Viva IROP Monitor"
(every 5m) and "Viva Schedule Diff (3x/day)". See skill
`spa-js-reverse-engineering` for the flight-classification logic itself.
Copy `templates/watchdog_template.py` as a starting skeleton.
