# CDN-Blocked API Access: Gmail Fallback Pattern

When a website behind CDN protection (Akamai, Cloudflare, etc.) blocks both
headless browser navigation and direct API calls, confirmation/transaction
emails in Gmail may contain the same data as Schema.org JSON-LD structured
data embedded in the HTML email body.

## When to use

- Browser times out on Page.navigate (CDP timeout) from headless Chrome
- Direct API calls return 403 Forbidden or time out
- The user has a Gmail account and the target service sends HTML confirmation emails
- The `google_api.py` tool is available with Gmail scopes

## Detection: CDN-blocked vs. API error

```bash
# CDN block — Akamai returns HTML error page, not JSON
curl -s "https://api.example.com/v1/endpoint" | head -5
# Returns: <HTML><HEAD><TITLE>Access Denied</TITLE>...
# CDN reference edge key in the body

# API auth error — returns JSON with error message
curl -s "https://api.example.com/v1/endpoint"
# Returns: {"message":"Forbidden"}
```

## Step-by-step

### 1. Search for the relevant email

```bash
# Search by service name
python google_api.py gmail search "Viva Aerobus DGCRHQ" --max 5

# Broader search if exact code fails
python google_api.py gmail search "Viva Aerobus" --max 10
```

### 2. Get the full email body

```bash
python google_api.py gmail get MESSAGE_ID
```

### 3. Extract structured data

The body field contains full HTML. Extract Schema.org JSON-LD:

```python
import json, re
data = json.loads(output)
body = data.get('body', '')
# Find JSON-LD blocks
jsonld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', body)
for block in jsonld:
    parsed = json.loads(block)
    # Look for FlightReservation, Reservation, Order, etc.
```

The JSON-LD typically contains: reservationNumber, underName,
reservationFor (flight/order details), departure/arrival times,
modifyReservationUrl, checkinUrl.

### 4. Extract plain text for policy/terms content

```python
import re
text = re.sub(r'<[^>]+>', '\n', body)
text = re.sub(r'\n\s*\n', '\n\n', text)
```

## Limitations

- Only works for email-sending services (not sites without email confirmations)
- Email may show pending/unpaid state if sent before payment confirmation
- JSON-LD data covers top-level reservation info only (not full API response)
- Booking status flags (paid/pending/cancelled) come from the API, not the email

## Angular production build: what NOT to waste time on

When the target site is built with Angular (detect via `ng-version` attribute
on `<app-root>`), production builds are locked:

| Approach | Typically fails? | Why |
|---|---|---|
| `__ngContext__` on component elements | ❌ Returns 0 (TNode index), not LView | Prod build strips LView refs |
| `window.ng` | ❌ `undefined` | Dev mode only |
| `getAllAngularTestabilities()` | ⚠️ Object exists, can't reach injector | Zone object available but no component access |
| `ng.probe()` | ❌ `undefined` | Dev mode only |
| DOM `.click()` on Angular components | ⚠️ May not trigger | Angular uses zone.js patched events; use `dispatchEvent(new MouseEvent(...))` instead |

**Better approaches for Angular prod builds:**
- Find the REST API that Angular calls (check JS bundles for URL patterns)
- Use Gmail fallback for data the API would return
- XHR intercept: override `XMLHttpRequest.prototype.open/setRequestHeader/send`
  to capture auth headers from real API calls, then replay them
- Fetch intercept: override `window.fetch` to capture headers from live calls.
  Note: Angular HTTP client usually uses XHR, not fetch — override both.
- **credentials: 'include'**: Always include in console fetch() calls —
  CDNs like Akamai set `_abck`/`bm_sz` cookies validated per-request.
  Missing cookies = 403 even with correct headers.
- **API method**: Many SPAs use POST for data retrieval (not GET). Check
  the JS bundle — Angular's `http.post()` is common even for reads.
- **x-api-key is NOT hardcoded**: It comes from a remote CMS (Contentful)
  config at runtime, stored in Angular's `cmsConfig.environmentConfig.webApi.publicKey`.
  You must capture it from the Network tab or XHR intercept.
  See `references/cdn-blocked-api-request-patterns.md` for capture methods.
- **X-Requested-With header**: Angular's HttpClient adds this automatically.
  Without it, CDNs may flag the request as non-Angular and reject it.
- **Rule gates in API responses**: Check the `rules` array for `isEnabled: false`
  gates like `DisabledForBookingStatusOnHold`. These are server-side and cannot
  be bypassed from the frontend.
- **SSR codes**: Search for codes like `VAJR` (refundable fare), `VBJL` (total
  refund charge), `VBDB` (carry-on baggage) in the API response or JS bundles
  to understand what features/services the booking has.