# Bypassing Angular SPA API Authentication

When a browser-based Angular app (e.g. Viva Aerobus) makes API calls that succeed but direct `fetch()` from the console returns 403, the issue is usually **missing headers that Angular's HTTP interceptors add**.

## Diagnostic Flow

1. **Check the Network tab** (F12 → Network → refresh the page)
2. Find a successful XHR/fetch to the API domain
3. Inspect **Request Headers** — look for:
   - `Authorization: Bearer <token>` — usually from localStorage (`viva-user-token`, `auth-token`, etc.)
   - `x-api-key` — a static API key from the app's CMS/environment config
   - `X-Channel: web` — channel identifier
   - `X-Requested-With: XMLHttpRequest` — Angular's XSRF header
4. Extract these values and replicate in your own `fetch()` call

## Key Headers to Look For

| Header | Source | How to Get |
|---|---|---|
| `Authorization: Bearer <JWT>` | localStorage token | `localStorage.getItem('viva-user-token')` |
| `x-api-key` | CMS config → Angular interceptor | Network tab on successful request |
| `X-Channel` | Hardcoded in Angular interceptor | Usually `"web"` |
| `X-Requested-With` | Angular's XSRF protection | Usually `"XMLHttpRequest"` |

## Critical: `credentials: 'include'`

CDN bot managers (Akamai, Cloudflare) check for session cookies (`_abck`, `bm_sz`, `ak_bmsc`). Raw `fetch()` calls from the console **do not send cookies** unless you explicitly set:

```js
fetch(url, { credentials: 'include', ... })
```

Without this, even with all the right headers, you'll get 403. This is the most commonly missed piece.

## HTTP Method Matters

If the Angular app uses `this.http.get(...)`, the endpoint expects GET (not POST). If it uses `this.http.post(...)`, it expects POST. Mismatch gives 405 Method Not Allowed. Check the Network tab to see which method the Angular app uses.

## Strategy: Capture from Network Tab, Then Replay

1. Open Network tab, refresh page
2. Find a successful API call
3. Copy: URL, Method, Request Headers (especially `x-api-key` and `Authorization`)
4. Replicate with fetch:

```js
fetch(url, {
  method: 'GET',  // or POST
  credentials: 'include',
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('viva-user-token'),
    'X-Channel': 'web',
    'x-api-key': 'copied-value',
    'X-Requested-With': 'XMLHttpRequest'
  }
})
```

## If You Can't Find the x-api-key

The API key lives in Angular's dependency injection (`this.cmsConfig.environmentConfig.webApi.publicKey`). To extract it:
1. Patch `XMLHttpRequest.prototype.setRequestHeader` before the page's API calls happen
2. Refresh the page so Angular makes its bootstrap API calls through your patched XHR
3. The patched `setRequestHeader` captures the `x-api-key` value

```js
window.__capturedHeaders = {};
const origSet = XMLHttpRequest.prototype.setRequestHeader;
XMLHttpRequest.prototype.setRequestHeader = function(h, v) {
  window.__capturedHeaders[h] = v;
  if (h === 'x-api-key') window.__capturedApiKey = v;
  return origSet.apply(this, arguments);
};
```