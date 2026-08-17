# Airline Hold / Pay-Later Flow Observation

Use this reference when the user wants to understand an airline “hold fare”, “pay later”, cash-in-store, or reservation-payment flow. The goal is to map the legitimate UI and business rules, not to create a booking, exploit credits, or force unavailable options.

## Safe observation boundary

Before progressing past flight selection, state the operating boundary:

- It is OK to select flights, fare family/combos, and proceed to passenger/contact/payment pages to observe available methods.
- It is OK to document copy, prices, fees, eligibility, expiration wording, and accepted payment channels.
- Stop before any irreversible button such as confirm, reserve, generate booking/PNR, finish, pay, issue, finalize, or equivalent.
- If the user account is logged in and personal data is visible, do not repeat PII back in chat. Summarize only the workflow state.
- Explicit user authorization is required before using real passenger/contact data to advance.

## Observation checklist

Capture these fields as they appear in the UI:

1. Route, dates, passengers, and fare family selected.
2. Whether the hold/pay-later option appears for one-way vs round-trip.
3. Minimum lead time and any route/currency restrictions.
4. Hold fee, if any, and whether it is refundable/credited.
5. Reservation total, TUA/taxes, and any excluded fees.
6. Payment channels: cards, PayPal, Viva Cash, OXXO/convenience store, bank transfer, app-only options, financing/MSI.
7. Expiration timestamp and whether it is 24 h, end-of-day, or a shorter rolling window.
8. Whether a PNR/booking code is generated before payment.
9. Whether login/Doters account is required.
10. Exact wording for cancellation, no-payment expiry, and fare/rule changes.

## Viva Aerobus notes from observed flow

- A VPS/datacenter browser may render the Viva homepage while `availability/search` is WAF-blocked. Diagnose in this order before changing many browser flags:
  1. Test official Chrome or Chromium as a non-root desktop user with sandbox enabled and a clean persistent profile.
  2. Compare IPv4/IPv6 reputation; a blocked datacenter address can coexist with a usable address on the other family.
  3. Inspect the actual availability response. `403` plus `WAF_BLOCKED_ERROR` while the homepage loads indicates network/WAF rejection, not “no flights.”
  4. If a shared browser is required and the user explicitly authorizes their own network as egress, use the private mobile-egress pattern below. Do not use it to evade anti-fraud controls or automate abusive transactions.
- On a working session, selecting IAH↔MTY flights and choosing Tarifa Zero reached `/book/passenger` normally.
- Viva may already be logged into the user’s Doters/Viva account and preload passenger/contact data. Treat this as sensitive; do not quote names, email, membership number, balance, birth date, phone, or document fields in the chat.
- Fare selection can require accepting Zero restrictions before progressing.
- Payments/hold details are not visible until after passenger/contact requirements and intermediate add-ons/asientos/hotel steps, so decide beforehand how far the user authorizes the agent to proceed.

### Private Android mobile-egress pattern

Use this only with the user’s own Android device/network and explicit permission. It solves datacenter false positives while keeping the shared browser on the VPS.

```text
VPS Chrome -> VPS 127.0.0.1:8888 -> reverse SSH tunnel
           -> Android 127.0.0.1:8080 -> HTTP proxy app -> mobile data
```

1. On the VPS, verify SSH forwarding policy and local-port availability:
   ```bash
   sshd -T | grep -E 'allowtcpforwarding|gatewayports'
   ss -ltnp | grep ':8888 ' || true
   ```
2. Permit reverse forwarding while keeping exposure local-only:
   ```text
   AllowTcpForwarding remote
   GatewayPorts no
   ```
   Back up SSH configuration, run `sshd -t`, then reload SSH without terminating the current connection.
3. On Android, run an HTTP proxy bound locally (for example port `8080`) over mobile data.
4. In Termius, create **Remote Port Forwarding** through the existing VPS host:
   - remote bind: `127.0.0.1:8888`
   - destination on Android: `127.0.0.1:8080`
5. Verify the tunnel and egress before launching the browser:
   ```bash
   ss -ltnp | grep ':8888 '
   curl --max-time 15 -x http://127.0.0.1:8888 https://api.ipify.org
   ```
   The returned address must be the user’s mobile egress, not the VPS address.
6. Launch official Chrome as a normal desktop user with sandbox enabled:
   ```bash
   google-chrome-stable \
     --proxy-server=http://127.0.0.1:8888 \
     --user-data-dir="$HOME/.config/google-chrome-airline-mobile" \
     --no-first-run --no-default-browser-check
   ```
7. Keep the Android proxy and Termius forwarding session alive. If pages partially render or stall, re-test the proxy with `curl` before changing browser settings.
8. Verify success from the real browser request, not merely the homepage: the availability endpoint should return `200` and actual fares.

### Payment-page findings

- Doters and Viva Cash are presented as partial-or-total payment methods. Each opens a reversible modal; custom redemption amounts are supported. Do not enter or apply real account value without the user choosing the amount.
- The custom Doters input did not expose HTML `min`/`max` attributes. This is not evidence of a vulnerability; server-side validation remains authoritative. Do not probe out-of-balance values on a live account.
- Cash/deposit displayed a 24-hour payment window after concluding the reservation. Observed channels included OXXO, 7-Eleven, Farmacias del Ahorro, Bodega Aurrera, additional stores, Banamex, Santander, and Scotiabank.
- Selecting cash/deposit automatically added optional “Protección por imprevistos” in the observed flow. Record this separately from fare/TUA and do not remove it without authorization.
- The final cash/deposit page required accepting privacy/terms and exposed an irreversible-looking **Concluir reservación** button. Treat it as the PNR/reference-generation boundary even if hidden DOM components use labels such as `Generar referencia`.
- After observation, use **Cambiar forma de pago** and verify that the cash method and final button are no longer active/visible. This prevents accidental completion.
- A specific Doters/Viva Cash + OXXO split was not verified because doing so would require applying real loyalty value. Report it as unverified rather than inferring from “partial payment” copy.

### PII-safe browser inspection

- Avoid dumping `document.body.innerText` on authenticated payment pages: account balances, membership IDs, names, and contact data can be mixed into otherwise relevant lines.
- A regex such as `Doters|Viva Cash` can still capture identifiers and balances. Prefer targeted DOM extraction whose output is redacted in the page context, or inspect a screenshot with an explicit instruction not to repeat PII.
- Verify each modal visually before acting. Overlay state can cause a click intended for Viva Cash to remain inside the Doters dialog.

## Recommended report shape

```markdown
## Hold-flow findings

| Field | Observed value |
|---|---|
| Route/date | ... |
| Fare family | ... |
| Total before payment | ... |
| Hold/pay-later available? | Yes/No/Not reached |
| Hold cost | ... |
| Expires | ... |
| Payment channels | ... |
| PNR generated before payment? | ... |
| Stop point | ... |

## Risk / caveats
- ...
```

## Do not do

- Do not generate or manipulate Viva Cash, coupons, payment codes, credits, or refunds.
- Do not click any final confirmation/booking/payment button without an explicit same-turn instruction.
- Do not assume “prediction of cancellation” creates IROP/refund eligibility.
- Do not paste or persist user credentials/payment details in scripts, logs, or summaries.
