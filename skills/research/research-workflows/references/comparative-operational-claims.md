# Comparative Operational Claims: Audit Note

Use this note when investigating claims that an airline, company, platform, hospital, carrier, or other operator has the “most,” “fewest,” “worst,” or “best” operational outcomes.

## Evidence table

Capture each candidate source in a compact table:

| Source / URL | Publisher and date | Underlying source | Geography | Exact period | Comparison set | Numerator | Denominator | Raw count or rate | Caveats |
|---|---|---|---|---|---|---:|---:|---|---|

A source is not a valid general ranking merely because it uses superlative language. Determine whether it describes:

- one airport or multiple airports;
- domestic, international, or whole-network operations;
- a single disruption event, live snapshot, rolling window, month, or year;
- all competitors or only entities appearing in a table;
- scheduled operations, operated events, arrivals, or tracker-observed records.

## Direct table audit

When an article publishes a table:

1. Count the actual rows.
2. Group rows by entity.
3. Count distinct dates or weekday labels.
4. Check for duplicate identifiers.
5. Compare table total with headline and prose totals.
6. Record whether the table names its upstream data provider and retrieval timestamp.

If the headline says “over 40” but the table contains 33 entries, report both; never silently choose one.

## Calculation patterns

### Rate from counts

If canceled events and operated events are reported separately, scheduled events may be:

`scheduled ≈ operated + canceled`

Then:

`cancellation rate ≈ canceled / (operated + canceled)`

Label this as inferred unless the source explicitly defines the denominator. Do not divide by arrivals and call the result an official cancellation rate.

### Expected events over a window

With a known exposure:

`expected events = unique eligible events × event rate`

With only a period count:

`expected events over D days = period count / period days × D`

For seasonal, weather-sensitive, or clustered events, this is a baseline expectation—not a forecast guarantee.

### Comparing an event table with normal operations

Keep these separate:

- **Event-table pace:** listed events divided by the event’s actual span.
- **Typical operating rate:** longer-period cancellations divided by scheduled operations.
- **Monitor expectation:** unique eligible records observed by that monitor multiplied by a comparable rate.

Do not apply a whole-network monthly count directly to a subset of airports or routes.

## Monitoring reconciliation checklist

Before calling a zero-result monitor contradictory, ask:

- Does it observe final operational status or only future schedules?
- Can it detect a flight removed before the first baseline?
- Are snapshots deduplicated into unique departures?
- Is the observation window based on completed departures?
- Does its geography match the benchmark source?
- Does disappearance mean cancellation, schedule revision, or missing data?
- Is the sample large enough that zero would be surprising?

## Reporting language

Preferred conclusion structure:

1. **Verdict:** supported, unsupported, or supported only narrowly.
2. **Origin:** earliest credible/discoverable wording and its underlying source, if any.
3. **Scope:** geography, exact date range, and comparison set.
4. **Metric:** raw count versus rate and denominator.
5. **Typical magnitude:** clearly labeled longer-period benchmarks.
6. **Requested-window expectation:** calculation with assumptions.
7. **Narrow restatement:** the strongest wording the evidence actually supports.

Example narrow restatement:

> “Operator X had the largest raw count among entities listed in this multi-site disruption table; the source does not establish the highest long-run normalized rate.”
