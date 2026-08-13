# Viva operational-status validation

## Durable finding

`plannedFlights` is a published timetable, not reliable cancellation ground truth. A flight can remain present there after operational cancellation. Treat disappearance as a candidate signal only.

## Native operational endpoint

```text
GET https://api.vivaaerobus.com/web/vb/v1/flightstatus
```

Parameters:
- `date=YYYY-MM-DD`
- `flight=<numeric flight number>` (no `VB` prefix)
- `lang=eng|esp`

Browser-facing headers include the public web `x-api-key`, `Origin`, and `Referer`. Retrieve the key dynamically when possible; do not embed credentials in this reference.

Primary decision field:

```python
cancelled = segment.get("operatingStatus", "").upper() == "CANCELLED"
```

Useful corroboration:
- `segments[].lastStatusUpdate`
- `notifications[].type == "OPERATIONAL"`
- cancellation message/title

## Validated case

On 2026-08-12, VB4042 MTY→TLC appeared in `plannedFlights` while the native operational response reported:

- `operatingStatus: CANCELLED`
- `lastStatusUpdate: 2026-08-12T07:54:53`
- notification: cancelled for operational reasons

FlightAware independently exposed `cancelled: true` for VIV4042. This proves timetable presence cannot be interpreted as normal operation.

## Source hierarchy

1. Viva native operational-status JSON — primary when stable.
2. Licensed aviation-status API (e.g. FlightAware AeroAPI/Cirium) — independent confirmation.
3. Public FlightStats page embedded state — workable low-rate fallback; parse `__NEXT_DATA__` with `JSONDecoder.raw_decode()` and fail closed.
4. Airport autocomplete/summary boards — not ground truth unless independently validated; a tested OMA result remained “A TIEMPO” for VB4042 after Viva/FlightAware marked it cancelled.
5. `plannedFlights` disappearance — candidate only.

## Rollout checklist

1. Replay one known flight from the actual cron host.
2. Verify HTTP status, schema, status value, and latency.
3. Repeat enough times to establish unattended stability.
4. Run a small near-departure batch; measure parser/fetch failures.
5. Keep the existing working validator active until the replacement passes.
6. Poll conservatively, cache/dedupe by `(date, flight)`, honor backoff, and stay silent unless actionable.
