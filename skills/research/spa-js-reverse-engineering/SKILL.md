---
name: spa-js-reverse-engineering
description: Reverse-engineer single-page app (SPA) JavaScript bundles to find feature flags, modal IDs, SSR codes, API endpoints, and hidden UI flows — especially for airline/manage-booking sites behind anti-bot protection.
version: 1.1.0
author: Hermes Agent
category: research
metadata:
  hermes:
    tags: [js, reverse-engineering, spa, angular, react, web, research, airline, api]
---

# SPA JS Reverse Engineering

Extract hidden UI flows, feature flags, API contracts, and modal triggers from minified SPA JavaScript bundles. Applies to any site where the browser can't render (Akamai/bot-blocking) but the JS bundles are public.

## When to use
- Airline/hotel/booking manage pages behind anti-bot protection
- Feature flags not visible in the rendered page
- Need to find modal triggers, SSR codes, hidden payment flows
- API endpoints discovered in JS but need auth/session info to call

## Output style
When applying this skill, produce **direct, actionable commands** — raw grep/cURL/JS to paste, minimal commentary between steps. The user wants commands they can run, not a lecture.

## Step-by-step

### 1. Get the page HTML
```bash
curl -s --max-time 15 'https://target.com/page?params' | head -100
```
Extract JS bundle URLs from `<script>` tags:
```bash
curl -s --max-time 15 'https://target.com/page' | grep -oP 'src="([^"]+\.js)"' | cut -d'"' -f2
```

### 2. Download JS bundles
Identify the main bundle (largest), runtime, polyfills, scripts, etc:
```bash
curl -s --max-time 15 'URL' -o /tmp/bundle_name.js
```
Main bundle is usually the largest (2-5MB).

### 3. Search for features
```bash
# Find feature flags
grep -oP '.{0,80}(?i:flagName|featureFlag|Show[A-Z]).{0,80}' bundle.js | sort -u

# Find refund/cancel/booking UI elements
grep -oP '.{0,80}(?i:reembolso|refund|cancel|voucher|modal).{0,80}' bundle.js

# Find modal/SSR codes (specific patterns)
grep -oP '(modalId|ssrCode|code:)\s*["\x27][A-Z0-9]{2,8}["\x27]' bundle.js

# Find API endpoints
grep -oP 'https?://[^"\x27\s,]+(booking|api|service)[^"\x27\s,]*' bundle.js

# Find feature flag enum definitions (Angular pattern)
grep -oP '[A-Z][a-zA-Z]+=\"[A-Z][a-zA-Z]+\",y\.' bundle.js | head -30
```

### 4. Extract context around hits
```bash
grep -oP '.{0,150}KEYWORD.{0,150}' bundle.js | sort -u
```

### 5. Try direct API access
```bash
curl -sv --max-time 20 'https://api.target.com/endpoint?param=value' \
  -H 'User-Agent: Mozilla/5.0' \
  -H 'Origin: https://www.target.com' \
  -H 'Referer: https://www.target.com/page'
```
Note: May need `x-api-key`, `Authorization: Bearer`, or `X-Channel` headers found in the JS interceptors.

### 6. Find HTTP interceptors in minified Angular bundles
The interceptor code pattern is distinctive. Search for these signals:

```bash
# Find Authorization Bearer interceptors (add JWT to requests)
grep -oP '.{0,200}Authorization.*Bearer.{0,200}' main.js | grep 'headers.set'

# Find x-api-key interceptors
grep -oP '.{0,200}x-api-key.{0,100}publicKey.{0,200}' main.js

# Find the interceptor class pattern (Angular DI + intercept method)
grep -oP '.{0,100}intercept\(a,d\).{0,400}' main.js | head -5

# Find specific API endpoint URLs
grep -oP '"https?://api\.' main.js
```

**Interceptor anatomy** — there are typically 3+ interceptors chained:

1. **Auth interceptor** — reads from DI token service, adds `Authorization: Bearer <token>`
2. **API key interceptor** — reads from `cmsConfig.environmentConfig.webApi.publicKey`, adds `x-api-key`
3. **Error handler interceptor** — catches 401/403/5xx, shows modals, logs out on 401

To reconstruct what headers an endpoint needs, look at the URL-matching conditions in each interceptor (e.g., `a.url.includes(je.UB) || a.url.includes(je.cO)`).

### 7. Find the real x-api-key (two approaches)

**Approach A — Network tab (RELIABLE, preferred):**
When the user is logged into the target site:
1. Open DevTools → Network tab
2. Refresh the page or trigger any action that makes an API call
3. Find any successful XHR to the target API
4. Click on it → Request Headers → find `x-api-key` value

This works even when Angular is in production mode and `__ngContext__` is inaccessible.

**Approach B — Angular DI walk (FRAGILE, often fails in prod):**

```javascript
const all = document.querySelectorAll('*');
let apiKey = null;
for (const el of all) {
  const ctx = el.__ngContext__;
  if (!ctx || !Array.isArray(ctx)) continue;
  JSON.stringify(ctx, function(k, v) {
    if (v && typeof v === 'object' && v.publicKey && typeof v.publicKey === 'string' && v.publicKey.length > 10) {
      apiKey = v.publicKey;
    }
    if (v && typeof v === 'object' && v.webApi && v.webApi.publicKey) {
      apiKey = v.webApi.publicKey;
    }
    return v;
  });
  if (apiKey) break;
}
```

**⚠️ NOTE:** In Angular 19 production mode, ALL `__ngContext__` values are TNode indices (numbers), NOT LView arrays. The JSON.stringify walk will ALWAYS fail. Use Approach A (Network tab) instead.

The key values to look for typically live in:
- `this.cmsConfig.environmentConfig.webApi.publicKey` → `x-api-key`
- `this.token.authToken` → read from localStorage key `viva-user-token` (find the key name in bundle: `grep 'LOGIN_TOKEN'`)

### 8. Craft the browser console API call

Try GET first for data retrieval, POST for mutations. API call troubleshooting progression:

```javascript
const jwt = localStorage.getItem('viva-user-token');  // or the found key name
const headers = {
  'X-Channel': 'web',
  'Authorization': 'Bearer ' + jwt
};
if (apiKey) headers['x-api-key'] = apiKey;

// Try GET first
const res = await fetch('https://api.target.com/web/v1/endpoint?param=value', {
  method: 'GET',
  headers,
  credentials: 'include',  // CRITICAL: sends Akamai/bot cookies
});
```

**Troubleshooting progression:**
- `403 Forbidden` → Missing headers or Akamai cookies. Add `credentials: 'include'` + all 3 headers + `X-Requested-With: XMLHttpRequest`
- `405 Method Not Allowed` → Wrong HTTP method. Try GET ↔ POST
- `400 Bad Request` → Auth/headers correct! Fix params/body

### 9. For Angular apps specifically
- `ng-version` attribute indicates Angular
- `__ngContext__` on elements gives LView (array) or index number
- **In Angular 19 prod: `__ngContext__` returns ONLY numbers** (TNode indices) — NEVER LView arrays. Can't walk DI tree this way.
- `_nghost-*` attributes = component host elements. Angular 19 uses `_nghost-ng-cXXXXXXXX` format — CSS `[_nghost]` selector does NOT match these.
- Interceptor classes: `class h{constructor(a){this.X=a}intercept(a,d){...}}` with `static \\u0275fac` / `static \\u0275prov`
- `getAllAngularTestabilities()` works in production — returns an object with `_ngZone`, but you CANNOT access the injector or services from it
- `window.ng` is undefined in production — no devtools support

### 10. Check server-side rule gates

After getting a successful API response, check the `rules[]` array to understand which operations are blocked server-side (by booking status). This is more reliable than assuming a hidden frontend toggle exists.

```javascript
// After getting booking data from the API:
const booking = await response.json();
const disabledRules = booking.data?.rules?.filter(r => !r.isEnabled) || [];
disabledRules.forEach(r => {
  console.log(r.type + ': disabled — ' + r.details.map(d => d.description).join(', '));
});
```

Common patterns:
- `OnHold`/`UnderPaid` status disables ALL cancel/refund/change rules server-side
- `TotalRefundCancellation`, `DisplayCustomerCancellation`, `FlexibilidadTotal` — all gated by status
- These are NOT frontend toggles — cannot be overridden from the browser console

## Pitfalls
- **Akamai/bot protection**: Headless browsers often timeout entirely. curl usually works for JS downloads.
- **403 on API calls**: Missing auth headers OR missing browser cookies. Always add `credentials: 'include'` — Akamai WAF sets `_abck`/`bm_sz` cookies and rejects requests that don't send them.
- **`x-api-key` is NOT optional**: The API gateway rejects calls without it even with valid auth. Find it via Network tab on a successful XHR.
- **CMS-controlled features**: Feature flags like `Show[Name]` are defined in code but toggled remotely (Contentful/etc). You can't trigger them from the frontend — they're server-side.
- **Angular 19 prod `__ngContext__`**: ALL `__ngContext__` values are TNode indices (numbers), NOT LView arrays. The JSON.stringify DI walk approach ALWAYS fails. Use Network tab instead.
- **`_nghost` CSS selector**: Angular 19 uses `_nghost-ng-cXXXXXXXX` suffix. `[_nghost]` selector does NOT match. Use `[ng-version]` for root or `[class*="ng-star"]` for inserted elements.
- **Endpoint method varies**: `booking/full` is GET with `?pnr=...&lastName=...`. `booking/cancel` is POST with JSON body. `booking/canceloptions` returns 405 on POST, 400 with real error on GET. Try GET first for data retrieval, POST for mutations.
- **`bookingId ≠ BasketId`**: Cancel endpoints need `BasketId` (server-side basket session ID), NOT the `bookingId` from the booking response. BasketId may be in a separate localStorage key or only in Angular in-memory state. Without it, cancel returns `{"key":"BasketId","message":"The value is not valid for BasketId."}`

- **Cancel endpoint requires both BasketId AND JourneyKeys**: `POST /web/v1/booking/cancel` needs `{"pnr":"...","lastName":"...","basketId":"...","journeyKeys":["..."]}`. JourneyKeys are base64-like strings from the booking response (e.g., `VkJ_IDYxN34gfn5JQUh_MDkvMDQvMjAyNiAyMzoxMH5NVFl_MDkvMDQvMjAyNiAyMzo0NX5_`). Without JourneyKeys you get `{"key":"JourneyKeys","message":"The JourneyKeys field is required."}`
- **Server-side rule gates**: Cancel/refund rules are gated by booking status (e.g., `OnHold` disables ALL rules server-side). The `rules[]` array in the booking response explicitly shows which rules are enabled/disabled per status — these are not frontend toggles.
- **Zone.js wrapping**: `fetch` in console returns zone-wrapped promises. Both `.then()` and `await` work.
- **Minified variable names**: Search for English strings, not variable names — strings survive minification.
- **Different endpoint path prefixes**: Not all endpoints use the same base path. The mail/cancel endpoint uses `/web/vb/v1/booking/mail/cancel` (with `vb/v1/` segment) while most other booking endpoints use `web/v1/booking/`. Always grep the JS bundle for the exact URL constant — search for patterns like `_URL:\`$\{m\}\`` or `L_RESEND_EMAIL_URL` to find the actual path. Some endpoints may live on different subdomains (`api.vs.`, `api-global.`).
- **`dataFullBasket` in sessionStorage**: When the Angular app loads a booking for management, it stores `dataFullBasket` in `sessionStorage` with just `{pnr, lastName}`. The actual basketId is in Angular's in-memory service state only.
- **Claude Code OAuth via Herdr**: When the user needs to authenticate Claude Code through a Herdr pane, use `herdr pane send-text <pane-id> <code>` followed by `herdr pane send-keys <pane-id> Enter` to submit. OAuth codes expire fast (~2 min) — have the user paste back immediately after generating the URL.