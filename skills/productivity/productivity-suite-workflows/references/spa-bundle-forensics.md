# SPA Bundle Forensics — Data Extraction from Bot-Protected Sites

## When to Use

When a bot-protected Single Page Application (Angular/React/Vue) **won't load in the headless browser** (Akamai, Cloudflare, reCAPTCHA, etc.) AND Gmail didn't have the full data you needed:

1. **Gmail is the first fallback** — search for confirmation/notification emails (see `gmail-email-data-fallback.md`)
2. **SPA bundle analysis is the second tier** — download the JS bundles (unauthenticated static assets) and reverse-engineer feature flags, API endpoints, UI components, and workflows offline

## Step-by-Step

### 1. Download the JS bundles

```bash
# Find the main bundle from the page HTML (use inspect with curl first)
curl -sS "$URL" | grep -oP 'src="[^"]*\.js"' | head -10

# Download the main bundle (usually several MB)
curl -sS "$BASE_URL/main.XXXXXXXX.js" -o /tmp/main.js

# Also download runtime, polyfills, scripts bundles
```

### 2. Search for feature flags, endpoints, and UI strings

```bash
# Feature flags and CMS toggles
grep -oP '(Show[A-Z][a-zA-Z]+|Enable[A-Z][a-zA-Z]+|Feature[A-Z][a-zA-Z]+)' /tmp/main.js | sort -u

# API endpoints
grep -oP 'https?://[a-z.-]+/[a-z0-9/_-]*' /tmp/main.js | sort -u

# UI buttons, labels, modals
grep -oP '(modalId|modal-id|modal:[^,}]+|app-[a-z-]+-modal)' /tmp/main.js | sort -u

# Translation keys (i18n pattern common in Angular apps)
grep -oP '(GLOBAL_ACTION_|GLOBAL_LABEL_|BOOKER_LABEL_|BOOKER_ALERT_|PROFILE_)[A-Z_-]+' /tmp/main.js | sort -u

# SSR codes and charge codes (airline-specific)
grep -oP '"[A-Z0-9]{4}"' /tmp/main.js | sort -u

# Spanish keywords if the site is Spanish-language
grep -oP '.{0,80}(?i:reembolso|cancelar|cambiar|devolucion|vivacash).{0,80}' /tmp/main.js | sort -u
```

### 3. Map UI component names to modals/buttons

```bash
# Find component selectors (Angular pattern)
grep -oP 'selectors:\[\["[a-z][a-z-]+"' /tmp/main.js | sort -u

# Find modal references
grep -oP '"remove-[a-z-]+-modal"|"[a-z-]+-selection-modal"' /tmp/main.js | sort -u

# Look for specific button texts and their click handlers
grep -oP '(onRemove|onCancel|onClose|onConfirm|onDelete|onOpen)[A-Za-z]*' /tmp/main.js | sort -u
```

### 4. Map the full user flow

- Identify the sequence: what modal comes first, what buttons lead where
- Note the **conditions** that show/hide each component (feature flags, user segment, payment method)
- Document the **API endpoints** the SPA calls and what auth they need

### 5. Try API calls directly (if auth token isn't needed)

```bash
# Some endpoints may work without auth
curl -sS "$API_URL/v1/endpoint" \
  -H 'Origin: https://example.com' \
  -H 'Referer: https://example.com/page'
```

If they return 403/timeout, the app needs a Bearer token or API key from the user's session.

### 6. Give the user console commands to run

When the API can't be called from the VPS, provide the user with JavaScript to paste in their **browser console** (F12 → Console) on the live page:

```js
// Search for auth tokens stored in localStorage
console.log('Token:', localStorage.getItem('viva-user-token')?.substring(0, 20));
console.log('EToken:', localStorage.getItem('viva-user-etoken'));
console.log('ESID:', localStorage.getItem('viva-user-esid'));

// Try to access Angular services
const root = document.querySelector('app-root');
Object.keys(root).filter(k => k.startsWith('__ng') || k.includes('injector'));

// Try to force-open a modal
// (exact command depends on the app; inspect Angular's context first)
```

#### Production Angular 19 — when __ngContext__ returns numbers

On production Angular 19+ builds (dev mode `__ngDevMode` is false), `__ngContext__` on component host elements returns **TNode indices** (0, 1, 2...) instead of LView arrays. This means you **cannot** access the component instance, injector, or services through the standard `element.__ngContext__[1]` trick.

When `document.querySelector('app-root').__ngContext__` returns `0`, the Angular internals are locked. Try:
- `getAllAngularTestabilities()` — may return a testability object with `_ngZone` access, but even then the root injector is typically unreachable on production builds
- `localStorage` tokens (`viva-user-token`, `viva-user-etoken`) — these are JWT Bearer tokens stored in plain sight
- Direct `fetch()` calls to the API from the user's browser **will still be blocked** by Akamai/Cloudflare CDN even with valid tokens because the Angular HTTP interceptor adds headers (`X-Channel`, `x-api-key`, platform-specific `Sec-CH-UA`) that raw `fetch()` doesn't include

If the user's booking shows as pending/unpaid, cancellation/refund options will not render regardless — those flows only activate once the booking is confirmed as paid.

## Example: Viva Aerobus Manage Booking (this session)

| Technique | Result |
|---|---|
| Load page in headless Chrome | ❌ Blocked by Akamai CDN |
| Gmail search + get | ✅ Found confirmation email with Schema.org JSON-LD flight data |
| JS bundle analysis | ✅ Found 70+ feature flags including `ShowVivaCashCancellationModalInMMB`, modal IDs (`remove-total-refund-modal`, `refundable-fare-selection-modal`), SSR codes (`VAJR`, `VBJL`), i18n labels (`BOOKER_LABEL_REIMBURSABLE-FARE-CART`), Angular component selectors (`app-remove-total-refund-modal`, `app-viva-cash-terms-modal`), service method names, API base URLs, HTTP error code lists |
| API direct call (curl, VPS) | ❌ All endpoints returned 403/timeout |
| API direct call (fetch, user browser with JWT) | ❌ Blocked by Akamai even with valid `viva-user-token` Bearer token — Angular HTTP interceptor adds platform headers (`X-Channel`, `x-api-key`, device UA-CH) that raw fetch lacks |
| Angular component inspection (prod Angular 19) | ❌ `__ngContext__` returns number indices (not LView arrays) — production build locked down |
| `getAllAngularTestabilities()` | ✅ Returns testability object, but root injector inaccessible on prod build |

## Pitfalls

1. **Minified JS is hard to read** — use `grep -oP` with context windows (`.{0,100}`) instead of trying to read raw output
2. **Bundles can be 2-5 MB** — download time matters, but grep is instant once downloaded
3. **Feature flags might not be active** — finding a flag in the code doesn't mean it's enabled in the CMS
4. **Component names ≠ visible UI** — a modal component exists in the code but may only render under specific conditions (payment method, user segment, booking status)
5. **Don't confuse "found in code" with "works for this user"** — always tell the user what conditions are required
6. **Spanish-language SPAs use English internally.** The UI shows "Cancelar" and "Reembolso" but the code uses `"Cancel"`, `"refund"`, `"RefundableFare"`, `"cancelLabel"`. Search for English keywords first, Spanish second.
7. **Feature flags in the code ≠ active in production.** `ShowVivaCashCancellationModalInMMB` exists in the JS bundle but is toggled via CMS (Contentful). Finding it in code only proves the feature *can* exist, not that it's live. Viva Aerobus controls this server-side per user/segment.