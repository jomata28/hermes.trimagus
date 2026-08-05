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

## Cancel endpoint shape
```javascript
// POST /web/v1/booking/cancel
const res = await fetch('https://api.vivaaerobus.com/web/v1/booking/cancel', {
  method: 'POST',
  credentials: 'include',
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('viva-user-token'),
    'X-Channel': 'web',
    'x-api-key': 'zasqyJdSc92MhWMxYu6vW3hqhxLuDwKog3mqoYkf',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    pnr: 'DGCRHQ',
    lastName: 'Torres Alvarez',
    basketId: '???',  // NOT the bookingId — server-side basket session ID
    journeyKeys: ['VkJ_IDYxN34gfn5...']  // from booking.data.journeys[].key
  })
});
```

## Key findings
- `bookingId ≠ BasketId`: Cancel endpoint rejects bookingId as invalid BasketId
- `OnHold`/`UnderPaid` status disables ALL cancel/refund/change rules server-side
- `rules[]` array in booking response shows exactly what's blocked and why
- Refundable amounts per journey stored in `comments` field as `RefundableAmountsPerJourney`
- VAJR SSR codes on both legs = refundable fare purchased ($496.34 IAH→MTY, $687.38 MTY→IAH)
- Total refundable amount from comments: IAH→MTY $2,494.94 + MTY→IAH $4,119.33 = **$6,614.27**
- x-api-key: `zasqyJdSc92MhWMxYu6vW3hqhxLuDwKog3mqoYkf`

## localStorage Keys
- `viva-user-token` — JWT auth token (long base64 string)
- `viva-user-etoken` — External (SSO) auth token (shorter string)
- `dataFullBasket` in **sessionStorage** — `{pnr, lastName}` only, no basketId

## Mail/cancel endpoint note
Found in JS as: `L_RESEND_EMAIL_URL:\`${m}vb/v1/booking/mail/cancel\``
The path segment is `vb/v1/booking/mail/cancel` not `web/v1/booking/mail/cancel`.
Full URL: `https://api.vivaaerobus.com/web/vb/v1/booking/mail/cancel`
Returns 404 in practice — endpoint may not exist or requires different params.

## Feature flags found in JS
- `ShowVivaCashCancellationModalInMMB` — Viva Cash refund modal toggle

## Service request (SSR) codes
- `VAJR` — Refundable Fare (per segment)
- `VBJL` — Total Refund Service charge
- `VBDB` — 10kg Carry-on Bag
- `VTUI` — Mexico Departure Tax
- `VLIG` — Bundle Light