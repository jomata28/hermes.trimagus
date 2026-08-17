# CDN-Blocked API Request Patterns

Techniques for making authenticated API calls from the browser console
against sites behind Akamai/Cloudflare CDN protection, specifically
Angular SPAs with HTTP interceptors.

## The Core Problem

Browser console `fetch()` calls against an API behind Akamai typically
return 403 even with a valid Bearer token. The CDN validates:
1. Session cookies (`_abck`, `bm_sz`, `ak_bmsc`) — must be sent via `credentials: 'include'`
2. Header completeness — Angular's HTTP interceptor adds specific headers
3. Request timing/ordering fingerprints — non-Angular requests look different to the CDN

## Header Triad Required by Angular SPAs

Angular HTTP interceptors typically add three headers that naive fetch calls miss:

| Header | Source | Why needed |
|--------|--------|------------|
| `x-api-key` | CMS config → `environmentConfig.webApi.publicKey` | API gateway validation |
| `X-Channel: web` | Hardcoded in interceptor | Channel identification |
| `X-Requested-With: XMLHttpRequest` | Angular's HttpClient adds this automatically | CDN fingerprint |

Plus `Authorization: Bearer <token>` from the auth service.

## Step-by-Step: Getting the x-api-key

The x-api-key is NOT hardcoded in the JS bundle — it's loaded from a
remote CMS (e.g., Contentful) at runtime and stored in an Angular service.

### Method 1: Network Tab (reliable, user-driven)

1. User opens DevTools → Network tab
2. User refreshes the page (or clicks something that triggers an API call)
3. User looks for a successful request to the API host
4. User clicks on it → Headers tab → scroll to Request Headers
5. User copies the `x-api-key` value and pastes it to you

### Method 2: XHR Prototype Patch (if API calls happen after patch is applied)

Paste this BEFORE any API call fires:

```javascript
window.__capturedApiKey = null;
window.__capturedHeaders = {};
const _origOpen = XMLHttpRequest.prototype.open;
const _origSend = XMLHttpRequest.prototype.send;
const _origSetHeader = XMLHttpRequest.prototype.setRequestHeader;

XMLHttpRequest.prototype.open = function(method, url) {
  this.__vaUrl = url;
  this.__vaMethod = method;
  return _origOpen.apply(this, arguments);
};

XMLHttpRequest.prototype.setRequestHeader = function(header, value) {
  if (window.__capturedHeaders) window.__capturedHeaders[header] = value;
  if (header.toLowerCase() === 'x-api-key') window.__capturedApiKey = value;
  return _origSetHeader.apply(this, arguments);
};

XMLHttpRequest.prototype.send = function(body) {
  this.__vaBody = body;
  return _origSend.apply(this, arguments);
};
```

After patching, have the user refresh the page or click a UI button.
The patch captures all headers when Angular makes its API call.

### Method 3: Fetch Intercept

Paste before any fetch call happens:

```javascript
const _origFetch = window.fetch;
window.fetch = function(url, opts) {
  if (typeof url === 'string' && url.includes('api.')) {
    window.__capturedApiUrl = url;
    window.__capturedApiHeaders = opts?.headers;
  }
  return _origFetch.apply(this, arguments);
};
```

## API Call Template (for console pasting)

Once you have the x-api-key:

```javascript
const token = localStorage.getItem('viva-user-token');
const apiKey = 'CAPTURED_KEY';

fetch('https://api.target.com/web/v1/endpoint', {
  method: 'POST',  // or GET
  credentials: 'include',  // CRITICAL
  headers: {
    'Authorization': 'Bearer ' + token,
    'X-Channel': 'web',
    'x-api-key': apiKey,
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ /* params */ })
}).then(r => r.text()).then(d => console.log(d));
```

## Reading the Response Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 403 | CDN block / bad auth | Check cookies (credentials: 'include'), headers, or x-api-key |
| 405 | Wrong HTTP method | Switch between GET/POST — Angular often uses POST for everything |
| 400 | Bad request | Check request body/params format; may need BasketId or session ID |
| 200 | Success | Data returned |

## SSR Codes and Feature Flags

When analyzing an airline/travel API response, these are common SSR codes:

| Code | Meaning |
|------|---------|
| VAJR | Refundable Fare (refundable fare component) |
| VBJL | Total Refund Service charge |
| VBDB | 10kg Carry-on Baggage |
| VLIG | Bundle Light |
| VTUA/VTUI | Mexico Departure Tax |
| VLY/VLA | Loyalty/Viva Fan membership |
| VUI | User identification |
| VVC | Viva Cash wallet |

Common feature flags to search for in JS bundles:
```
ShowVivaCashCancellationModalInMMB
```

## Rule Gates in API Responses

Many booking/transaction APIs return business rules alongside data.
Always check the `rules` array:

```json
"rules": [{
  "type": "TotalRefundCancellation",
  "isEnabled": false,
  "details": [{
    "code": "DisabledForBookingStatusOnHold",
    "description": "Booking rule disabled for booking status OnHold"
  }]
}]
```

Common gate types:
- `DisabledForBookingStatusOnHold` — booking is pending payment
- `DisabledForBookingStatusCheckedIn` — passenger already checked in
- `DisabledForCreationTime` — outside the allowed time window
- `DisabledForCarrierVB` — rule doesn't apply to this airline code
- `DisabledForRoute` — rule doesn't apply to this origin/destination pair

## JWT Token Alone Is Not Enough from VPS

A valid JWT extracted from `localStorage` (e.g., `viva-user-token`) will return **401 from curl** even with correct headers, because Akamai validates the request's CDN session cookies (`_abck`, `bm_sz`) which only exist in the browser. Similarly, `booking/full`, `buyback`, and `marketplace` endpoints return **403 Access Denied** from curl regardless of token validity.

The token works **only when sent from the browser itself** (via console `fetch()` with `credentials: 'include'`) because the browser automatically attaches the Akamai session cookies that the CDN requires.

### Pattern: Token + mobile proxy + browser console fetch

When you have a JWT but the VPS IP is blocked:

1. User logs in on their phone/normal browser → extracts `localStorage.getItem('viva-user-token')`
2. VPS Chrome launched through mobile proxy tunnel (see `user-owned-mobile-egress.md`)
3. User navigates to the target site in the proxied VPS Chrome (gets Akamai cookies)
4. Execute authenticated API calls via **browser console fetch** (not curl), which automatically includes CDN cookies:

```javascript
fetch('https://api.vivaaerobus.com/web/v1/account/funds', {
  headers: {
    'X-Channel': 'web',
    'x-api-key': 'CAPTURED_KEY',
    'Authorization': 'Bearer ' + localStorage.getItem('viva-user-token')
  }
}).then(r => r.text()).then(t => console.log(t.substring(0, 800)))
```

5. For automated extraction without xdotool typing, use the **raw CDP websocket** technique (see `vps-desktop-sessions/references/cdp-raw-websocket.md`) to execute the same fetch from Python.

### What works from VPS curl (no proxy, no cookies)

Some endpoints are tier-1 public and work from VPS curl with just `x-api-key`:

| Endpoint | Auth needed | Works from VPS curl? |
|---|---|---|
| `plannedFlights` | `x-api-key` only | ✅ Yes |
| `resources/stations` | `x-api-key` only | ✅ Yes |
| `flightstatus` | `x-api-key` only | ✅ Yes (needs correct params) |
| `availability/search` | CDN cookies | ❌ No (Akamai 403) |
| `booking/full` | JWT + CDN cookies | ❌ No (Akamai 403) |
| `account/funds` | JWT + CDN cookies | ❌ No (401 without cookies) |
| `buyback` | JWT + CDN cookies | ❌ No (Akamai 403) |
| `marketplace` | JWT + CDN cookies | ❌ No (Akamai 403) |

## Server-Side Gates Cannot Be Bypassed

If the API response shows `isEnabled: false` with a rule gate like
`DisabledForBookingStatusOnHold`, no frontend hack can override it.
The gate is enforced on the backend. The user must either:
1. Change the booking status (e.g., pay → status changes from OnHold to Confirmed)
2. Call customer service who can process the action with elevated privileges