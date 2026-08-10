# Validating disappearance-based monitors

Use this for airline schedules, inventory feeds, event listings, and any monitor where an item disappearing from an API is treated as a possible cancellation/removal.

## Epistemic rule

**Disappearance is a signal, not ground truth.** Until a known real cancellation/removal is observed end-to-end, label results `candidate`, not `cancelled`. A stable schedule on normal days does not prove what the source does on cancellation days.

Keep separate claims:

1. **Published-schedule detection:** item vanished from source A.
2. **Public-status publication:** source B/webpage explicitly shows cancelled/removed.
3. **Transaction availability:** booking/search endpoint stopped offering it.
4. **User notification:** passenger/customer was notified.
5. **Prediction:** an upstream signal estimated risk before any authoritative decision.

Do not collapse these into one timestamp or claim one source leads another without paired observations.

## Required observation record

For every candidate, persist:

- full observation timestamp and timezone;
- item identity using route/date/number or the domain’s full natural key;
- previous and current payload hashes or normalized fields;
- scope-fetch completeness and errors;
- first missing time, consecutive-miss count, and confirmation time;
- event/departure time and computed lead time;
- public webpage/status result with timestamp;
- transaction/search availability result with timestamp, when authorized;
- later ground-truth outcome and evidence source.

## Ground-truth strategy

Rank evidence:

1. Authoritative operator/airport cancellation record.
2. Credible operational-history API with explicit cancellation status.
3. Passenger notice or verified public status page.
4. Third-party tracker.
5. Inference from missing schedule/ADS-B records (weak; never sufficient alone).

A historical schedule endpoint may accept past dates yet still return the planned timetable rather than actual operations. Validate historical semantics against a known cancelled and a known operated item before using it as labels.

## Measuring source lead

To answer “did API A update before webpage B?” poll both independently and store first-observed timestamps. Report an interval bounded by polling cadence, e.g. “between 10:00 and 17:00 CT,” not a fabricated exact cancellation time. Multiple daily snapshots narrow the interval but do not prove notification timing.

## Classification pitfalls

- Match flights/items using the full natural key, not number/name alone.
- For retime/renumber detection, match a missing item only against **newly appearing** survivors; matching against an item that existed in both snapshots creates false retimes on high-frequency routes.
- Compare only overlapping observation windows. Items entering/leaving lookahead boundaries are not cancellations.
- Deduplicate origin/partition enumeration before diffing.
- Abort partial snapshots; a failed partition can mimic mass disappearance.
- Confirmation must persist across runs and count distinct full snapshot timestamps, not just calendar dates.

## Success metrics

After enough verified events, calculate precision, recall, false-positive causes, median lead time, percent first detected ≥48h before event time, and source-A-to-source-B publication delta. Before labels exist, say the metrics are unknown.
