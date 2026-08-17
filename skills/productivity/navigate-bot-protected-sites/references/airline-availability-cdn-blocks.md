# Airline Availability CDN Block Triage

Session pattern: a carrier homepage renders normally, but the flight availability/search API returns a generic CDN/edge error such as `Lo sentimos / servicio no disponible` with an Akamai-style detail code. Treat this as an API-access problem, not proof that no flights exist.

## Fast diagnostic sequence

1. Capture the visible page first. Read the exact modal/error text and route/date shown.
2. Use CDP/performance entries or DevTools Network to identify the failing resource. For Viva Aerobus the sensitive call observed was:
   - `https://api.vivaaerobus.com/web/v1/availability/search` → HTTP `403`
3. Check whether the page itself is healthy. If static assets, login panels, analytics, etc. load while only availability fails, do not keep changing dates/routes as if it were inventory.
4. Compare browser/network reputation before blaming Chromium version:
   - launch as a normal desktop user with sandbox when possible;
   - use a persistent human profile and navigate from the homepage rather than deep-linking;
   - compare `curl -4` vs `curl -6` to the target and to a high-signal control such as Google search;
   - if only IPv6 is challenged, test IPv4-only for the browser UID.
5. If Google or another major site shows a network-abuse CAPTCHA for the VPS IP, report IP reputation as the likely blocker and stop burning time on browser flags.

## Practical fallback

For purchase/booking/hold flows, do not try to bypass the CDN gate or force hidden business actions. Use the VPS browser for observation only if it works; otherwise have JT use his phone/normal browser/app for the transaction while Hermes supplies monitoring, candidate selection, and concise decision reports.

### User-owned mobile egress when VPS IP is blocked

If the homepage renders but the airline availability endpoint returns WAF 403 from a VPS/datacenter IP, route only the visible browser through a user-owned mobile/residential connection before giving up on shared-screen operation. Use the `references/user-owned-mobile-egress.md` reverse-tunnel pattern and verify with both an IP check and the formerly blocked endpoint.

Observed Viva Aerobus success pattern:

1. VPS network produced generic “servicio no disponible” and explicit `WAF_BLOCKED_ERROR` on `availability/search`.
2. Browser hygiene alone did not fix it: non-root user, sandbox, official Chrome, persistent profile, locale, and IPv4-only were insufficient.
3. Android Every Proxy + Termius remote port forward exposed a localhost-only proxy on the VPS (`127.0.0.1:8888`).
4. Launching Chrome with `--proxy-server=http://127.0.0.1:8888` changed egress to the user’s mobile IP.
5. The same Viva availability resources then returned HTTP 200 and real fare inventory rendered.

Keep the tunnel scoped to the browser. Do not route the whole VPS through the phone, and do not expose the reverse proxy publicly.

## Safety boundary

Do not generate coupons, credits, cash-equivalent codes, or code intended to manipulate carrier business rules. You may analyze legitimate eligibility, public schedules, operational risk, and cancellation/refund rules, and you may explain that a server-side state gate cannot be bypassed from the browser console.