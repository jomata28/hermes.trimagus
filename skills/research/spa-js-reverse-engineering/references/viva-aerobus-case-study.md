# Viva Aerobus — JS Reverse Engineering Reference

Reservation PNR DGCRHQ — Case study from 2026-08-04

## URLs
- Manage page: `https://www.vivaaerobus.com/es-mx/manage/trip-details?pnr=DGCRHQ&lastName=Torres%20Alvarez`
- Main JS bundle: `https://www.vivaaerobus.com/main.fb03daf92fe221a8.js` (~2.5MB)
- Angular version: 19.2.25 (prod mode)

## API Endpoints Found
| Endpoint | Method | Response | Notes |
|---|---|---|---|
| `api.vivaaerobus.com/web/v1/booking/full` | GET | Full booking details | Works with `?pnr=...&lastName=...` |
| `api.vivaaerobus.com/web/v1/booking/canceloptions` | GET (POST=405) | Cancel options/validation | Needs BasketId param |
| `api.vivaaerobus.com/web/v1/booking/cancel` | POST | Execute cancel | Needs BasketId + JourneyKeys |
| `api.vivaaerobus.com/web/v1/account/trips` | GET | Trips list | Works with `?pnr=...`, returns all user trips |
| `api.vivaaerobus.com/web/vb/v1/booking/mail/cancel` | POST (404) | Resend cancel email | Note `vb/v1/` prefix not `web/v1/` |
| `api.vivaaerobus.com/web/v1/basket/create` | POST | Create basket session | Does NOT check booking status |
| `api.vivaaerobus.com/web/v1/basket/loadbooking` | POST | Load booking into basket | Binds PNR to basket session |
| `api.vivaaerobus.com/web/v1/irop/cancel` | POST | IROP cancel path | Needs ReimbursementMethod, not OnHold-gated |
| `api.vivaaerobus.com/web/v1/irop/details` | GET | IROP status for booking | Returns NoIropQueue if flight not disrupted |
| `api.vivaaerobus.com/web/service/v1/fsnc/plannedFlights` | GET | Flight schedule + IROP status | Polls by origin/date for all flights |
| `api.vivaaerobus.com/web/vb/v1/booking/compensations` | POST | Available compensations | |
| `api.vivaaerobus.com/web/v1/booking/payment` | ? | Payment processing | Found in JS, untested |

All API calls need: `x-api-key`, `X-Channel: web`, `Authorization: Bearer <token>`, `credentials: 'include'`

## Working API Call Pattern (browser console)
```javascript
const token = localStorage.getItem('viva-user-token');
const apiKey = 'zasqyJdSc92MhWMxYu6vW3hqhxLuDwKog3mqoYkf';
const res = await fetch('https://api.vivaaerobus.com/web/v1/booking/full?pnr=DGCRHQ&lastName=Torres%20Alvarez', {
  method: 'GET',
  credentials: 'include',  // CRITICAL: sends Akamai cookies
  headers: {
    'Authorization': 'Bearer ' + token,
    'X-Channel': 'web',
    'x-api-key': apiKey,   // Get from Network tab → any successful XHR
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*'
  }
});
```

## Troubleshooting progression
403 (blocked) → 405 (wrong method) → 400 (validation) → 200 (success).
- 403: Missing `credentials: 'include'` or wrong/missing headers
- 405: Wrong HTTP method — swap GET ↔ POST
- 400: Auth correct! Fix params/body

## Basket Session Flow (to get a valid BasketId)
```javascript
// 1. Create basket (does not check status)
POST /web/v1/basket/create
Body: {pnr, lastName, language: 'es-MX', currencyCode: 'MXN'}
→ {data: {basketId: '019fce8c-...'}, type: 'SUCCESS'}

// 2. Load booking into basket
POST /web/v1/basket/loadbooking
Body: {basketId, pnr, lastName}
→ {data: {}, type: 'SUCCESS'}

// 3. Now BasketId works with cancel/change endpoints
```

## Cancel endpoint shape
```javascript
// POST /web/v1/booking/cancel
Body: {
  pnr: 'DGCRHQ',
  lastName: 'Torres Alvarez',
  basketId: 'uuid-from-basket-create',
  journeyKeys: ['VkJ_IDYxN34gfn5...', 'VkJ_IDYxMH4gfn5...']
}
```

## IROP Cancel endpoint shape
```javascript
// POST /web/v1/irop/cancel — different gate than regular cancel
Body: {
  basketId: '...',
  pnr: 'DGCRHQ',
  lastName: 'Torres Alvarez',
  journeyKeys: ['...', '...'],
  reimbursementMethod: 'VivaCash'  // or 'Credit', 'OriginalPayment'
}
// Error when no IROP: {"code":"IROP_UNAVAILABLE","message":"Booking is not in IROP queue"}
// Does NOT return "DisabledForBookingStatusOnHold" — different rules
```

## IROP Flight Monitoring
```javascript
// GET /web/service/v1/fsnc/plannedFlights
// Params: flightDate=YYYYMMDD&origin=XXX (also supports flightNumber, destination)
// Returns all flights from that hub/date with IROP status
// Field: noControlableMessages = null (normal) or populated (disrupted)
// Poll hubs: MTY, MEX, GDL, CUN, TIJ, IAH, BJX, HMO, PVR, SJD, MID, CJS, QRO, TLC, AGU, ZCL, TAM, MZT, TRC, VSA, LAP, SLP, OAX, VER
```

## Schedule-Diff Strategy (cancel-before-public detection)

Instead of predicting cancellations, **detect them after the airline has decided but before they've told passengers**.

### How it works
1. **Daily snapshot**: Poll `plannedFlights?origin=HUB&flightDate=YYYYMMDD` for all 24 hubs, 14 days forward
2. **Diff**: Compare today's snapshot against yesterday's for the same flight dates
3. **Classify**: 4-level classification for disappeared flights
4. **Confirm**: A flight absent for 2+ consecutive snapshots = confirmed cancellation

### The diff engine (classification logic)
```
Level 1 — Route capacity check:
  If route has same or more flights → RENUMBERED_OR_RETIMED (not cancelled)

Level 2 — New survivor check (only match against flights that DIDN'T exist in previous snapshot):
  If a new flight is close in time (<90min for high-freq, <240min for low-freq) → RETIMED

Level 3 — Route lost capacity, nothing nearby → CANCELLED_CANDIDATE

Level 4 — Flicker guard:
  If absent for 2+ consecutive snapshots → CONFIRMED CANCELLATION
```

### Bugs fixed during build
1. **History persistence**: candidates must be saved to a JSON file across runs. Continued absence must be explicitly checked against the current snapshot (flights absent in BOTH snapshots never enter classify())
2. **Flight number matching**: key on `(flight_number, route)` not just `flight_number`
3. **Retime false positives**: only match against NEW survivors, not all survivors
4. **Silent row loss**: log dropped rows from unparseable timestamps

### Monitors running
| Monitor | Frequency | Detection | Lead time |
|---|---|---|---|
| IROP Monitor | Every 5 min | `noControlableMessages` changes | Hours |
| Schedule Diff | Daily 9am CT | Flight disappears from schedule | 1-4 days |

### Key insight: 2-day advance requirement
The booking must be OnHold for 2+ days before the flight and the cancellation must happen 2+ days before departure. This means the schedule-diff strategy (which detects cancellations 1-4 days ahead) is the viable path — the IROP monitor is too late (same-day detection).

### Weather data (for prediction model)
The vb-cancel project uses NOAA Aviation Weather Center (free, no key):
- METAR observed data: `https://aviationweather.gov/api/data/metar`
- Airport-specific hazard thresholds: fog (TIJ), tropical (CUN/PVR), convective (MTY/GDL), wind (CJS/TRC)
- Per-airport CAT I landing minimums defined in config.py

## Key findings
- `bookingId != BasketId`: Cancel endpoint rejects bookingId as invalid BasketId
- `OnHold`/`UnderPaid` status disables ALL cancel/refund/change rules server-side
- `rules[]` array in booking response shows exactly what's blocked and why
- Basket creation does NOT check booking status (OnHold bypass via basket/create)
- IROP cancel checks IROP queue, NOT booking status (different gate)
- Refundable amounts per journey stored in `comments` field as `RefundableAmountsPerJourney`
- VAJR SSR codes on both legs = refundable fare purchased ($496.34 IAH→MTY, $687.38 MTY→IAH)
- Total refundable amount: IAH→MTY $2,494.94 + MTY→IAH $4,119.33 = **$6,614.27**
- x-api-key: `zasqyJdSc92MhWMxYu6vW3hqhxLuDwKog3mqoYkf`

## localStorage Keys
- `viva-user-token` — JWT auth token (long base64 string)
- `viva-user-etoken` — External (SSO) auth token (shorter string)
- `dataFullBasket` in **sessionStorage** — `{pnr, lastName}` only, no basketId

## Feature flags found in JS
- `ShowVivaCashCancellationModalInMMB` — Viva Cash refund modal toggle

## Service request (SSR) codes
- `VAJR` — Refundable Fare (per segment)
- `VBJL` — Total Refund Service charge
- `VBDB` — 10kg Carry-on Bag
- `VTUI` — Mexico Departure Tax
- `VLIG` — Bundle Light

## Journey Keys for DGCRHQ
- IAH→MTY VB617: `VkJ_IDYxN34gfn5JQUh_MDkvMDQvMjAyNiAyMzoxMH5NVFl_MDkvMDQvMjAyNiAyMzo0NX5_`
- MTY→IAH VB610: `VkJ_IDYxMH4gfn5NVFl_MDkvMDcvMjAyNiAwNjowMH5JQUh_MDkvMDcvMjAyNiAwODozNX5_`