# Historical Operational Outcome Backfill

Use this pattern when a monitor has schedule snapshots but lacks reliable operated/cancelled labels.

## Evidence hierarchy

1. Date-specific operational tracker returning explicit status and matching event identity.
2. Independent historical status table with explicit `Cancelled` / `Landed` outcomes.
3. Search snippets or airport boards only when they show an explicit outcome for the exact date/flight/route.
4. Schedule presence or absence is never an outcome label.

## Date-specific FlightStats/Cirium pages

Pattern:

```text
https://www.flightstats.com/v2/flight-tracker/<carrier>/<number>?year=YYYY&month=M&date=D
```

The HTML may assign JSON as `__NEXT_DATA__ = {...}` rather than use a pure JSON script tag. Locate the assignment and use `json.JSONDecoder().raw_decode()`.

Before labeling, validate all available identity fields:

- requested date equals `schedule.scheduledDepartureUTC` date;
- returned flight number matches;
- origin and destination match;
- preserve `flightId`, raw status, URL, and query timestamp as evidence.

Label only explicit final states:

- `statusCode C/CX` or `Cancelled` → cancelled;
- `A/L`, `Departed`, `Arrived`, or `Landed` → operated;
- `Scheduled`, mismatched identity, unreadable page, 403/429, or missing status → unknown.

Public retention may be short. An old-date request can silently return a newer instance, so date validation is mandatory.

## Browser-session fallback

Direct HTTP may receive 403/429 while a persistent, human-verified browser profile renders the page. In that case:

1. Ask the user to solve CAPTCHA/login in the persistent browser without sharing credentials.
2. Connect automation to the live browser session.
3. Read rendered historical tables slowly and save the raw page text/URL.
4. Rate-limit navigation; a successful browser session does not authorize high-volume scraping.

Airportia historical tables can provide multiple dated `Landed`, `Landed Late`, `CANCELLED`, or `Unknown` rows. Treat it as a secondary source (it may cite Aviation Edge), retain provenance, and cross-check overlap against the primary source before trusting a batch.

## Consolidation and metrics

- Prefer the stronger source when both resolve the same event.
- Audit overlap for contradictions before merging.
- Keep `Unknown` explicit; never count it as operated.
- Cancellation rate denominator must include only resolved outcomes.
- Future dates and same-day pending flights remain unknown until final.
- Report attempted, resolved, unresolved, operated, cancelled, contradictions, and source counts.
- Before claiming that an airport, route, or carrier segment “cancels more,” audit the sampling frame. A backfill intentionally centered on one hub cannot compare that hub against the network. Report cell counts and uncertainty intervals; small rates such as 2/10 are watchlist signals, not stable estimates.

## Predictive limitation

Historical outcome labels alone support base rates by route/flight/time. They do not reconstruct pre-event features. A predictive model still needs prospective snapshots of delays, estimate changes, assigned aircraft, irregular-operation timestamps, and time-to-departure. Keep heuristic scoring in shadow mode until calibrated against enough final outcomes.
