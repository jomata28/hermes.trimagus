---
name: navigate-bot-protected-sites
description: Strategies for accessing bot-protected websites including CDN-blocked authenticated APIs, Angular SPA reverse-engineering, XHR header capture, and Gmail fallback when direct access fails.
category: productivity
---

# Navigate Bot-Protected Sites

## When to Use
- You need data from a site that employs bot detection (Akamai, Cloudflare, CAPTCHAs, Turnstile)
- Headless browser navigation or API calls are blocked by CDN-level protection
- The site is an Angular SPA in production mode with locked internals
- You need to reverse-engineer an undocumented REST API behind a CDN/proxy
- You need structured data that may also exist in the user's Gmail confirmation emails

## Key references
- `references/cdn-bypass-gmail-fallback.md` — Gmail-as-fallback pattern and Angular production build analysis
- `references/cdn-blocked-api-request-patterns.md` — Request patterns that work vs. those that don't when facing Akamai/Cloudflare, including x-api-key capture methods and JS bundle analysis
- `references/human-login-authenticated-extraction.md` — human login through the VPS browser, persistent-profile/CDP handoff, geographic search pitfalls, and listing-level verification

## Approach (ordered by effort)

### Tier 1 — Passive analysis (no automated requests)
1. **Check Gmail** for confirmation/transaction emails (may contain same data as API)
2. **Download JS bundles** from the target site — search for URL patterns, API keys, feature flags
3. **Analyze the page DOM** for Angular components, ng-version, data attributes

### Tier 2 — Manual browser console (user pastes JS)
1. Guide the user to open DevTools → Network tab on the target page
2. Have them identify a successful XHR/fetch to the API
3. Extract the `x-api-key` or other auth headers from the network request headers
4. Use `credentials: 'include'` in all console fetch() calls (CDNs verify session cookies)
5. Add `X-Requested-With: XMLHttpRequest` header to match Angular's interceptor output

### Tier 3 — XHR interception (smuggle inside Angular's pipeline)
Patch `XMLHttpRequest.prototype` before the page loads (or before a button click triggers an API call), let Angular's HTTP interceptor add all the "secret sauce" headers, then capture them for replay.

### Tier 4 — Full API reverse-engineering
1. Download the main.js bundle (often 2-3MB for Angular SPAs)
2. Search for API endpoint patterns: `v1/`, `v2/`, `booking/`, `cancel`, etc.
3. Search for SSR codes, feature flags, and business rules
4. Search for hardcoded API keys and token patterns
5. Try reconstructed API calls with captured headers

### Tier 5 — Persistent visual-browser extraction

Direct HTTP may return 403/429 while the same public page renders normally in a persistent, human-verified browser profile. Before asking for a login, test the rendered page body: a CAPTCHA may already be solved and no credentials may be needed.

1. Start/reuse the persistent browser profile and let the user solve CAPTCHA or log in personally if required; never request or repeat their passwords.
2. Connect automation to the live browser session and inspect the rendered DOM/text.
3. Navigate slowly and save raw page text plus source URL for auditability.
4. Parse explicit dated outcomes/records only; do not infer success from presence in an index or schedule.
5. Cross-check overlapping records against a stronger source and count contradictions before batch consolidation.
6. Respect rate limits: human verification unlocks a session, not permission for high-volume scraping.

### Tier 6 — Manual fallback
When all automated approaches fail (server-side rule gates, strict CDN policies):
- Recommend the user calls customer service for actions the API blocks
- Document what was found for future sessions (API key, endpoints, data shapes)

## API Call Patterns That Work

```javascript
fetch('https://api.target.com/web/v1/endpoint', {
  method: 'POST',  // or GET — check what Angular uses
  credentials: 'include',  // CRITICAL: sends CDN session cookies
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('viva-user-token'),
    'X-Channel': 'web',
    'x-api-key': 'CAPTURED_KEY',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ pnr: 'PNR', lastName: 'NAME' })
})
```

### Key differences from naive fetch calls:
- `credentials: 'include'` — without it, Akamai returns 403 (missing `_abck`/`bm_sz` cookies)
- `X-Requested-With: XMLHttpRequest` — Angular HTTP client adds this by default; missing it flags the request as non-Angular
- `x-api-key` — often from a CMS config, not hardcoded in JS; must be captured from Angular's interceptor output

## How to Capture the x-api-key

### Method A — Network tab (easiest)
1. User opens DevTools → Network tab
2. User refreshes the page (or triggers an action that calls the API)
3. User clicks on any successful XHR to the API host
4. User copies the `x-api-key` value from Request Headers
5. User pastes the key into your script

### Method B — XHR prototype patching
Paste this BEFORE any API call happens (before page load or before clicking a button):
```javascript
window.__capturedHeaders = {};
XMLHttpRequest.prototype.setRequestHeader = function(header, value) {
  window.__capturedHeaders[header] = value;
  if (header.toLowerCase() === 'x-api-key') window.__capturedApiKey = value;
  return XMLHttpRequest.prototype.setRequestHeader._orig.apply(this, arguments);
};
```

### Method C — Fetch intercept
Paste this before page refresh:
```javascript
const origFetch = window.fetch;
window.fetch = function(url, opts) {
  if(url.includes('api.')) {
    window.__capturedHeaders = opts?.headers;
    window.__capturedUrl = url;
  }
  return origFetch.apply(this, arguments);
};
```

## Analyzing API Responses for Rule Gates

Many APIs include business rules alongside data. Check for:
- `rules` array with `isEnabled: true/false` flags per operation
- `disabledForBookingStatus*` or similar condition gates
- `ssrCodes` — special service request codes controlling fare features
- `featureFlags` — CMS-controlled toggles for UI features

### Common rule gate pattern:
```json
{
  "type": "TotalRefundCancellation",
  "isEnabled": false,
  "details": [{
    "code": "DisabledForBookingStatusOnHold",
    "description": "Booking rule disabled for booking status OnHold"
  }]
}
```

This means the backend enforces the gate — no frontend trick can bypass it.

## JS Bundle Analysis for SPA Reverse-Engineering

### Finding API endpoints:
```bash
grep -oP 'v1/[a-z/]+' main.js | sort -u
grep -oP 'BOOKING_[A-Z_]+_URL[^,]+' main.js
grep -oP 'CANCEL[^,=\"]+' main.js | grep -oP '[a-z]+/[a-z]+(/[a-z]+)*' | sort -u
```

### Finding API keys and config:
```bash
grep -oP 'publicKey[^,]+' main.js
grep -oP 'x-api-key[^,)]+' main.js
grep -oP 'environmentConfig[^}]+' main.js
```

### Finding SSR codes and feature flags:
```bash
grep -oP 'ssrCode[^,]+' main.js | sort -u
grep -oP 'Show[A-Z][A-Za-z]+Modal[^,]+' main.js
grep -oP '"VA[A-Z0-9]{2}"' main.js | sort -u
```

### Finding Angular component tags:
```bash
grep -oP 'app-[a-z-]+' main.js | sort -u
grep -oP 'selector:"[a-z-]+"' main.js
```

## Verification Steps
1. Confirm whether the CDN/API is returning structured data or just error pages
2. If API returns JSON, check for rule gates that block the desired action
3. If rule gates are server-side, inform the user — no frontend hack can override them
4. Always capture the x-api-key and token format for reuse in later attempts