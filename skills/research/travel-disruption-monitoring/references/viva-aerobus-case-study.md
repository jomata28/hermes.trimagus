# Viva Aerobus Case Study

This reference captures implementation-specific lessons that generalize to future airline monitors. Treat paths and sample counts as historical context, not permanent guarantees.

## Proven Source Behaviors

### Viva `plannedFlights`

- Useful for published schedules, snapshots, disappearance candidates, retimes, and renumbering.
- Not operational ground truth: a flight can remain listed after an independent tracker marks it cancelled.
- Absence must persist across snapshots before becoming a candidate; even persistent absence needs operational confirmation.

### FlightStats/Cirium public tracker

Date-specific pattern:

```text
https://www.flightstats.com/v2/flight-tracker/VB/{number}?year={YYYY}&month={M}&date={D}
```

The HTML contains a JavaScript assignment resembling:

```html
<script>__NEXT_DATA__ = {...}</script>
```

Parse the balanced JSON object after the assignment rather than assuming a modern `<script id="__NEXT_DATA__">` element. Validate returned service date, route, and scheduled departure because old requests may return a newer instance.

Useful evidence fields include flight ID, status/statusCode, cancellation flag/note, scheduled/estimated/actual times, tail number, and equipment.

### Airportia/Aviation Edge

A persistent browser session exposed 7–10 days of flight history when direct HTTP sources rate-limited. Preserve the exact page URL and raw table status. In the tested overlap, 21 resolved flight-days agreed with FlightStats, but Airportia remains a secondary source.

Never interpret `Unknown`, HTTP 403/429, date mismatch, or future service date as operated.

## Retrospective Labeling Lesson

An initial backfill found 133 flight-days but direct FlightAware access produced mostly HTTP 429 and a few Unknown responses. The initial script risked presenting this as “0% cancelled.” Correct behavior:

```text
resolved denominator = Cancelled + Diverted + Arrived/Landed + other explicit final states
unresolved = Unknown + blocked + parse failure + date mismatch + future
```

Cross-source browser work later resolved a subset as operated/cancelled while leaving the remainder Unknown. The durable lesson is denominator discipline, not the session-specific counts.

## Schedule-Trail Finding

For reconstructible cancellations, the published schedule stayed unchanged until roughly 2–3 hours before departure. One example remained normally listed from about 39 hours out through seven hours out, then disappeared near two hours before departure. Therefore:

- Published schedule changes were useful close to departure.
- They did not provide a reliable 48–72 h signal.
- A daily 48–72 h product should be labeled a watchlist, not a cancellation prediction.

## Weather Cross-Section

Historical METAR/ASOS sources:

```text
https://aviationweather.gov/api/data/metar?ids=MMMY,KIAH&format=json&hours=240
https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?...
```

Observed severe weather coincided with one cancellation to GDL: thunder/rain, low visibility, low ceiling, and strong gusts. Other cancellations had benign observed conditions. This showed weather is one feature family, not a complete explanation.

### Avoid forecast leakage

Observed weather near departure cannot be used as if it were known 48–72 hours earlier. Reconstruct model vintages with Open-Meteo Single Runs:

```text
https://single-runs-api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&run={ISO_RUN}&hourly=precipitation,weather_code,visibility,wind_speed_10m,wind_gusts_10m&models=gfs_seamless&forecast_days=7&timezone=UTC
```

Choose a model run initialized before the prediction timestamp, preserve the run value and URL, and extract only the forecast valid at the flight time. In the tested cancellation controls, 48–72 h runs did not flag severe weather even where severe weather later occurred; shorter horizons were therefore expected to be more informative.

TAF is valuable for shorter horizons but usually covers about 24–30 hours and public endpoints may not return historical issuance vintages. Capture TAF prospectively.

## Implementation Artifacts on JT's VPS

Historical implementation used:

- `/root/.hermes/scripts/viva_operational_status.py`
- `/root/.hermes/scripts/viva_weather_snapshot.py`
- `/root/.hermes/scripts/viva_operational_with_weather.py`
- `/root/.hermes/viva_operational_status/observations.jsonl`
- `/root/.hermes/viva_operational_status/risk_predictions.jsonl`
- `/root/.hermes/viva_operational_status/weather_snapshots.jsonl`

Before relying on these paths, verify they still exist and inspect current schemas.

## Reporting Correction

JT's actual need is a daily decision list, not a long methodology report. Use:

1. `APARTAR` only with multiple strong independent signals and verified availability.
2. `VIGILAR` for weak/moderate evidence.
3. `NINGUNO` when no candidate clears the threshold.

Do not pad the report with technical detail. Put methodology behind the decision and explain only the concrete reasons for each candidate.
