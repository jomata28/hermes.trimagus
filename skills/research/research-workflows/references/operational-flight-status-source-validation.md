# Operational Flight-Status Source Validation

Use this note when identifying a source that must distinguish real operational outcomes such as **CANCELLED**, rather than merely returning scheduled/planned flights.

## Validation standard

A source is not validated merely because its schema, UI copy, or JavaScript bundle contains the word `Cancelled`. Make a real request and capture:

- Request timestamp and exact URL/parameters (redact credentials).
- HTTP status and content type.
- Carrier identity and flight number.
- Route/date and source freshness field, when available.
- The actual per-flight status field/value.
- A concrete cancelled flight if cancellation exposure is the requirement.

When possible, independently corroborate the same flight with a second operational source. Report disagreements rather than silently choosing one.

## Discovery workflow for undocumented airline/airport feeds

1. Load the airline's flight-status page and inspect its current JavaScript bundle.
2. Locate the service method and base URL constants; reconstruct the exact query shape from the call site, not by guessing parameter names.
3. Check request interceptors for required browser-facing headers such as `x-api-key`, channel, origin, or locale.
4. If configuration is loaded from a public CMS/bootstrap document, retrieve it dynamically. Never persist the current key in this skill, source control, logs, or examples; public browser visibility does not make a key stable or unrestricted.
5. Reproduce the browser request directly and verify the returned status on a known flight.
6. Sample several flights/statuses when practical. A single on-time response proves data access, but does not prove cancellation representation.
7. Compare airport boards and aggregators against the airline result. Airport autocomplete/search endpoints may expose structured JSON yet still be stale or timetable-derived.

## Viva Aerobus case study (validated 2026-08-12; re-discover before reuse)

The public Viva web application used:

```text
GET https://api.vivaaerobus.com/web/vb/v1/flightstatus
```

Observed query shape:

```text
date=YYYY-MM-DD&flight=<numeric flight number>&lang=eng|esp
```

The browser client supplied a public web `x-api-key` obtained from its live CMS configuration. Retrieve that value from the current application/config at runtime; do not copy the historical value from a report.

A real request for Viva flight 4042 on 2026-08-12 returned HTTP 200 and identified `VB`, MTY→TLC, with:

```json
{
  "operatingCarrier": "VB",
  "operatingCode": "4042",
  "lastStatusUpdate": "2026-08-12T07:54:53",
  "operatingStatus": "CANCELLED"
}
```

The same response included an operational notification saying the flight had been canceled for operational reasons. FlightAware's public flight page for `VIV4042` independently embedded `"cancelled":true` for that flight. By contrast, an OMA Monterrey search endpoint reported the same flight as `A TIEMPO`, demonstrating that a convenient airport-board JSON endpoint is not automatically authoritative or fresh.

Treat these endpoint details as a reproducible lead, not a permanent contract: the endpoint, schema, key distribution, and access policy may change.

## FlightStats/Cirium SSR historical lookup

For public historical lookup by airline + flight number + date, first try the server-rendered tracker page:

```text
https://www.flightstats.com/v2/flight-tracker/{IATA}/{NUMBER}?year=YYYY&month=M&date=D
```

FlightStats has exposed structured tracker state through a JavaScript assignment shaped like:

```html
<script>__NEXT_DATA__ = {"props": ... }</script>
```

Do not assume the modern Next.js form `<script id="__NEXT_DATA__" type="application/json">`. A robust extractor finds the assignment, finds the following `{`, and uses `json.JSONDecoder().raw_decode()` so trailing `</script>` or JavaScript does not break parsing:

```python
import json, requests

url = "https://www.flightstats.com/v2/flight-tracker/VB/4042?year=2026&month=8&date=12"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
r.raise_for_status()
p = r.text.index("__NEXT_DATA__")
p = r.text.index("{", p)
next_data, _ = json.JSONDecoder().raw_decode(r.text[p:])
flight = next_data["props"]["initialState"]["flightTracker"]["flight"]
```

Useful evidence fields:

- `flightId`
- `flightNote.canceled`, `flightNote.landed`, `flightNote.hasDepartedGate`
- `status.statusCode`, `status.status`, `status.finalStatus`
- `schedule.scheduledDepartureUTC`, `schedule.tookOff`, `schedule.landing`
- `departureAirport.iata`, `arrivalAirport.iata`
- `positional.flexTrack.positions`, `tailNumber`, and `irregularOperations`

Classification should be asymmetric:

- `statusCode == "C"`, `flightNote.canceled == true`, or explicit `CANCELLATION` irregular operation supports **Cancelled**.
- Actual departure/arrival, `landed == true`, or credible positional evidence supports **Operated**.
- A missing record, HTTP denial, schedule-only record, or absence of ADS-B evidence is **Unknown**, never cancellation by inference.

Validated examples from 2026-08-12:

- VB4042 MTY→TLC: `statusCode: "C"`, `flightNote.canceled: true`, and `irregularOperations[].type: "CANCELLATION"` (event timestamp `2026-08-11T15:50:54.578Z`).
- VB101 JFK→MEX: `statusCode: "L"`, `landed: true`, actual departure/arrival, positions, and tail XA-VAK.

The browser bundle has also constructed an internal route like:

```text
/v2/api-next/flight-tracker/{carrier}/{flight}/{year}/{month}/{day}/{flightId}?rqid=...
```

Treat that as an implementation detail, not the primary integration: it may require browser state or reject direct requests. Prefer the SSR state when the public page returns it. Cache each flight-day, throttle requests, and preserve the raw evidence excerpt because this is undocumented and may change.

## FlightRadar24, Airportia, and airport-board triage

### FlightRadar24

Separate the Cloudflare-protected consumer website and legacy web JSON routes from the documented API. For supported automation, use the official authenticated endpoint:

```text
GET https://fr24api.flightradar24.com/api/flight-summary/full
Authorization: Bearer <API_KEY>
```

Typical filters are `flight_datetime_from`, `flight_datetime_to`, and `flights=VB101,VB4042`. The documented range is bounded (observed maximum 14 days per request), and access requires a key/subscription. FR24 is strong corroboration for **Operated** through `first_seen`, `last_seen`, route, and track data. A cancelled flight may never transmit ADS-B, so no FR24 result is not cancellation evidence.

### Airportia

Treat public flight pages as manual corroboration unless a documented/licensed automation surface is available. Check `robots.txt` before probing: Airportia has disallowed `/api/`, `/widgets/`, and date-query flight paths. Do not turn bot-control evasion into an integration strategy.

### Airport pages

Airport pages often expose convenient same-day JSON but not historical date lookup. Two observed shapes:

```text
GET https://www.oma.aero/api/flighttime.php?status=both&airport={AIRPORT_ID}
GET https://aeropuertodetoluca.com.mx/wp-json/tlc-airlabs/v1/schedules?type=arrivals&q=VB4042&limit=80&lang=es
```

Before calling either historical, prove that an explicit date parameter changes the returned service day. Search parameters may only filter an already-loaded current board, and unknown parameters may be silently ignored. Airport labels such as `A TIEMPO`, `CERRADO`, or `Activo` are not necessarily final operational outcomes. In the Viva VB4042 case, an airport board conflicted with airline/Cirium cancellation evidence, so airport feeds should be secondary and freshness-qualified.

## Candidate assessment

For each candidate, separate these judgments:

- **Technically usable:** structured response, stable identifiers, adequate freshness, manageable auth/rate limits.
- **Actually validated:** a successful live request returned carrier-specific operational evidence.
- **Automation support:** documented API/SLA versus undocumented website backend or scraped HTML.
- **Legal/policy posture:** published terms, robots directives, API licensing, and permission. `robots.txt` is relevant operational-policy evidence but is not by itself a complete legal opinion.

Prefer, in order:

1. Official documented airline or airport operational API.
2. Official browser API, conservatively polled and clearly labeled undocumented.
3. Licensed aviation-data API.
4. HTML scraping only when terms permit it and no structured source exists.

Do not recommend anti-bot circumvention as an automation strategy. If public pages return access controls, investigate the provider's documented/licensed API instead.

## Reporting format

Return a compact comparison containing:

- Exact endpoint/page URL.
- Reproducible request example with secrets represented as placeholders.
- Minimal response excerpt proving carrier, flight, freshness, and status.
- Validation date/time.
- Coverage and latency limitations.
- Technical automation feasibility.
- Terms/robots/licensing caveat, without presenting it as legal advice.
- Clear primary recommendation and fallback.
