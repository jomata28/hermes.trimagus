---
name: travel-disruption-monitoring
description: Build and operate prospective travel-disruption risk monitors by separating schedules, live operations, predictions, and verified outcomes; includes weather-vintage joins, source validation, calibration, and concise decision reports.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [travel, aviation, monitoring, forecasting, weather, calibration]
---

# Travel Disruption Monitoring

## When to Use

Use this skill when the user wants recurring monitoring or early-warning estimates for flight cancellation, delay, diversion, airport disruption, or similar travel failures.

## Core Data Model

Keep four layers separate:

1. **Published schedule** — what the carrier currently sells or displays.
2. **Operational state** — scheduled, delayed, departed, arrived, diverted, cancelled.
3. **Prospective prediction** — risk score recorded *before* the outcome.
4. **Verified outcome** — operated/cancelled/diverted/unknown, with source and evidence.

Never use a schedule listing alone as proof that a flight operated. Likewise, a single disappearance is not proof of cancellation.

Use a stable event key such as `(carrier, flight_number, origin, destination, service_date, scheduled_departure)`; flight number alone can collide across dates or routes.

## Workflow

1. **Define the decision and horizon.** Distinguish a 48–72 h watchlist from a 2–8 h operational alert.
2. **Collect schedules prospectively.** Timestamp every snapshot and preserve changes rather than overwriting history.
3. **Collect live operational features.** Save status, scheduled/estimated/actual times, tail number, equipment, irregularity messages, and source URL.
4. **Preserve forecast vintages.** For weather-based prediction, store the forecast that was actually available at prediction time. Do not join final observed weather or hindsight forecasts into a 48–72 h model.
5. **Label outcomes independently.** Cross-check at least two sources where possible. Keep blocked, mismatched-date, future, and ambiguous records as `Unknown`; never count them as operated.
6. **Build an interpretable shadow score first.** Store score, level, reasons, horizon, and timestamp without sending recommendations.
7. **Follow flights beyond scheduled departure.** Maintain a short lookback window so normal operations become negative labels; collecting only cancellations destroys calibration.
8. **Evaluate.** Report sample size, class balance, precision, recall, false positives, false negatives, calibration/Brier score, and median lead time.
9. **Activate alerts conservatively.** Require multiple independent signals for the highest action category.
10. **Keep automation informational.** Do not automatically purchase, reserve, pay, or manipulate inventory. A prediction does not create compensation, rebooking, or IROP eligibility.

## Signal Families by Horizon

### 48–72 hours

- Forecast-vintage severe weather at origin/destination or prior station
- Hurricane, airport closure, planned runway/ATC restriction, or broad disruption notice
- Route/flight historical baseline with shrinkage or Bayesian smoothing
- Repeated schedule thinning, renumbering, or withdrawal from sale

Treat this as a watchlist. Weather models often miss rapidly developing convection at this horizon.

### 12–24 hours

- TAF and updated convective forecast
- Tail assignment and inbound aircraft rotation
- Accumulating delays or cancellations at the airport
- Recent irregularity messages or meaningful estimate changes

### 2–8 hours

- Inbound aircraft cancelled, diverted, or stranded
- Explicit operational irregularity
- Persistent schedule disappearance
- No aircraft assignment unusually close to departure
- Severe delay escalation or explicit cancellation

## Statistical Guardrails

- Avoid raw percentages from tiny samples; include denominators and uncertainty intervals.
- Use balanced or stratified sampling before comparing airports. A dataset concentrated at one hub cannot establish that the hub cancels more.
- Compare hubs using cancellations divided by resolved departures over the same dates and coverage window. Absolute cancellation counts mostly measure hub traffic volume.
- Before computing any cancellation rate from a live observation stream, audit outcome capture. If cancelled flights resolve reliably but operated flights remain `Scheduled`/`Unknown` because follow-up stops too early, the apparent rate is unusable. Use that stream for event-pattern discovery only, and use an independently followed clean cohort for rates.
- Report traffic share versus cancellation share only as an exploratory signal when their denominators differ; never present that mismatch as proof that a hub has an elevated rate.
- A recent cancellation of the same flight number is a weak signal unless validated against many operated controls.
- Validate event date and route when a tracker returns “the latest” instance despite date parameters.
- Distinguish `0 cancelled among resolved` from `0 cancelled overall`.
- Do not call a heuristic score a probability until calibrated prospectively.

## Three-Day Forecast Product

A T-72 forecast is a ranked watchlist, not a definitive cancellation call. Use staged predictions that gain stronger operational evidence as departure approaches:

1. **T-72:** route/flight baseline with shrinkage, preserved weather forecast vintage, planned airport restrictions, schedule thinning/retimes, and route redundancy. Do not assume tail assignment or crew state is known.
2. **T-24:** add TAF, airport-wide disruption, recent carrier cancellations, and meaningful estimate changes.
3. **T-8:** add inbound aircraft/rotation, tail assignment, diversions, stranded aircraft, and accumulating delays.
4. **T-3:** add explicit IROP messages, persistent schedule disappearance, broken outbound-return pairs, and operational confirmation.

Store every revision as a new timestamped prediction rather than overwriting the T-72 estimate. Evaluate each horizon separately because a strong T-3 detector can hide a useless T-72 model if results are pooled.

## Source and Access Discipline

- Prefer official carrier/airport/aviation sources, then independent trackers.
- Browser sessions may expose history that direct HTTP requests rate-limit; use conservative pacing and preserve evidence URLs/IDs.
- Never bypass access controls. A user may manually complete authentication or human verification, but credentials should not be shared in chat.
- Store source, query timestamp, event identifier, raw status, and minimal evidence for every label.

## JT Daily Report Format

For JT, lead with the decision—not the research narrative:

- **APARTAR** — only when at least two independent strong signals exist and availability is verified.
- **VIGILAR** — partial or moderate evidence.
- **NINGUNO** — explicitly say `Hoy no recomiendo apartar ninguno` when evidence is weak.

For each candidate include flight, route, service date/time, category, concrete reasons, operational-status link, and booking/search link. Keep the report concise. Clearly state that if the flight operates, normal fare rules apply and the estimate does not guarantee cancellation, IROP, compensation, or refund.

## Verification Checklist

- [ ] Schedule, operational state, prediction, and outcome are separate fields.
- [ ] Predictions were timestamped before outcomes.
- [ ] Unknown/future/rate-limited records were excluded from outcome denominators.
- [ ] Weather features came from the forecast vintage available at the stated lead time.
- [ ] Operated flights are captured as controls.
- [ ] Airport comparisons use balanced samples and uncertainty intervals.
- [ ] High-action alerts require independent corroboration.
- [ ] No transaction is performed automatically.

## Booking / Hold-Flow Observation

When monitoring is meant to support a legitimate “hold fare”, “pay later”, or cash-in-store strategy, separate the prediction work from the transaction flow. Use monitoring to recommend candidates, then map the airline UI carefully and stop before irreversible booking/payment actions unless the user explicitly authorizes that step in the current session. If a logged-in account or prefilled passenger profile appears, do not repeat PII in chat; summarize only workflow state and ask before advancing with real data.

If a shared VPS browser loads the airline homepage but a protected availability endpoint is WAF-blocked, do not stop after one fingerprint tweak or immediately fall back to “use your phone manually.” Systematically test an unprivileged sandboxed browser, IP-family reputation, and an official browser build; if the WAF still rejects datacenter egress, offer a localhost-only reverse-SSH route through the user’s own mobile connection. Verify the protected endpoint itself, not just the homepage.

See `references/airline-hold-pay-later-flow.md` for the observation checklist, Viva-specific notes, and safe stop points.

## References

- `references/viva-aerobus-case-study.md` — concrete source behaviors, retrospective labeling lessons, and weather-vintage findings from the Viva Aerobus implementation.
- `references/airline-hold-pay-later-flow.md` — safe observation checklist for airline hold/pay-later/cash-in-store flows, including Viva-specific lessons and PII boundaries.
- `references/mobile-egress-browser-pattern.md` — WAF diagnosis and a localhost-only reverse-SSH Android/mobile egress pattern for keeping a shared VPS browser visible without exposing a public proxy.
