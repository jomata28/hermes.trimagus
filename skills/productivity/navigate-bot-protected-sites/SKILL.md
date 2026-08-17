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
- `references/user-owned-mobile-egress.md` — Android reverse SSH tunnel for residential IP egress when datacenter IPs are WAF-blocked
- `references/reader-proxy-and-search-engine-diagnosis.md` — r.jina.ai reader proxy as diagnostic tier, search-engine accessibility from datacenter IPs, Bing `site:` operator pitfall

## Approach (ordered by effort)

### Tier 1 — Passive analysis (no automated requests)
1. **Check Gmail** for confirmation/transaction emails (may contain same data as API)
2. **Download JS bundles** from the target site — search for URL patterns, API keys, feature flags
3. **Analyze the page DOM** for Angular components, ng-version, data attributes

### Tier 1b — Reader-proxy diagnosis (no automated requests to target)

When direct browser and curl both fail (403/401/ERR_HTTP2_PROTOCOL_ERROR), use a third-party reader proxy to fetch the target page from a different egress IP. The most reliable is `r.jina.ai`:

```bash
curl -s --max-time 30 -A "Mozilla/5.0" \
  "https://r.jina.ai/https://target-site.com/path" \
  -o /tmp/jina_result.txt
```

**What jina.ai can do:**
- Return 200 and rendered text for sites that return connection errors or JS challenges to the VPS directly (e.g., Propiedades.com returns a JS challenge page that at least confirms the site structure).
- Fetch search-engine result pages (Bing works) when you need to discover indexed URLs from a datacenter IP that Google/DuckDuckGo would CAPTCHA.

**What jina.ai cannot do:**
- Bypass CloudFront/Cloudflare WAF blocks that are IP-reputation-based. Lamudi (CloudFront) returns `401 Unauthorized` even through jina.ai because jina's egress is also a datacenter IP.
- Execute JavaScript challenges. A site that serves a JS challenge page will return that challenge HTML, not the rendered content.

**Decision rule:** If jina.ai returns the actual page content → use it as a reading fallback (still secondary evidence). If it returns a challenge page or 401/403 → the block is IP-reputation-based and only a residential/mobile egress (Tier 5 mobile proxy) will work. See `references/reader-proxy-and-search-engine-diagnosis.md` for full details.

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

## CDP (Chrome DevTools Protocol) for reading page state

When `vision_analyze` is unavailable (503) or you need to read DOM/localStorage programmatically, launch Chrome with `--remote-debugging-port=9222` and query it via CDP. This is more reliable than `xdotool` console injection.

### Launch with CDP enabled
```bash
su - jt -c 'export DISPLAY=:99 && google-chrome-stable \
  --display=:99 --disable-gpu --no-first-run --start-maximized \
  --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 \
  --proxy-server="http://127.0.0.1:8888" \
  --user-data-dir="/home/jt/.config/google-chrome-viva" \
  "https://www.target.com/profile"'
```

### Query page content via CDP (Python stdlib only — no websocket lib needed)
Write a script to `/tmp/cdp_query.py` that:
1. Fetches `http://127.0.0.1:9222/json/list` to find the tab's `webSocketDebuggerUrl`
2. Opens a raw TCP websocket connection (stdlib `socket` + manual handshake)
3. Sends `Runtime.evaluate` with a JS expression like:
   ```javascript
   JSON.stringify({
     hasToken: !!localStorage.getItem("viva-user-token"),
     url: window.location.href,
     bodyText: document.body.innerText.substring(0, 2000)
   })
   ```
4. Reads and parses the masked websocket frame response

This avoids installing `websocket-client` (which may fail due to PEP 668 / venv isolation). The raw socket approach works with Python stdlib only.

### CDP navigation pitfall: use `window.location.href`, not `Page.navigate`
On some sites (MercadoLibre Inmuebles confirmed), sending `Page.navigate` over a raw CDP websocket
**silently fails** — the command returns success but the URL never changes and the old page stays.
Instead, navigate via `Runtime.evaluate`:
```python
cdp_eval(ws_url, "window.location.href = 'https://target.com/path'", timeout=10)
time.sleep(8)
cur = cdp_eval(ws_url, 'JSON.stringify({url: window.location.href, title: document.title})')
```
Always re-read `window.location.href` after navigating and confirm the title changed before extracting;
do not assume the navigation landed.

### CDP vs other approaches
| Method | Reliability | Limitations |
|--------|-------------|-------------|
| `vision_analyze` screenshot | Medium | Fails when vision model is 503 |
| `xdotool` console injection | Low | Unreliable keystroke timing, devtools may not open |
| CDP `Runtime.evaluate` | **High** | Requires `--remote-debugging-port` at launch |

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