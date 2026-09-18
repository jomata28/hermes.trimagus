---
name: viva-renovar-reserva
description: Use when renewing JT's Viva cash-payment hold.
version: 1.0.0
author: Hermes Agent + JT
category: productivity
metadata:
  hermes:
    tags: [viva-aerobus, reservation, renewal, cash-payment, oxxo, banamex, browser]
---

# Viva: renovar reservación apartada

Renew an existing JT-owned Viva Aerobus reservation by replacing its pending cash-payment reference and obtaining a new approximately 24-hour payment deadline.

## Standing authorization

JT explicitly authorizes this workflow to press the final **Renovar / Aceptar / Confirmar** control whenever every invariant below passes. Do not stop merely because the final button changes the reservation deadline. The authorization is limited to renewing the payment hold and does not authorize purchases, immediate charges, itinerary changes, cancellations, insurance, add-ons, or disclosure of booking/account data.

## Required invariants

Before final confirmation, verify:

- The target is an existing held/on-hold reservation owned by JT.
- Flight dates, routes, passengers, fare, seats, baggage, and total price have not changed.
- No insurance or optional product is selected.
- The chosen method creates a cash-payment reference and does not charge immediately.
- Prefer **OXXO**; use **Banamex** only if OXXO is unavailable or clearly invalid.

If any invariant fails, stop before confirmation and report the exact blocker without exposing PNR, passenger name, email, itinerary, or payment reference.

## Browser workflow

1. Use an authenticated persistent browser session. Prefer Codex Work `@Browser` when the VPS/datacenter browser receives Akamai errors.
2. Open **Mis vuelos / My Trips** and identify the currently held reservation.
3. Record the visible current deadline and invariant summary privately.
4. Open the reservation/payment details.
5. Choose **Cambiar método de pago**.
6. When offered travel insurance, explicitly choose **No**, remove it, or leave it unselected.
7. Open **Otros métodos de pago**.
8. Choose **Pago en efectivo**.
9. Select **OXXO**. If unavailable, select **Banamex**.
10. Re-check the total and trip invariants.
11. Press the final **Renovar**, **Aceptar**, or equivalent confirmation control. This final press is part of the authorized workflow, not a stopping point.
12. Wait for Viva's confirmation page and read back the reservation state.
13. Verify all of the following before reporting success:
    - a new deadline/reference was issued;
    - the deadline moved forward by approximately 24 hours;
    - the booking remains held/on hold rather than cancelled or charged;
    - PNR, flight, passengers, and total price remain unchanged;
    - insurance remains absent.

## Timing and retries

- Attempt renewal about one hour before the existing deadline when the deadline is known.
- If Viva temporarily refuses or the booking service is unavailable, retry every 30 minutes while the existing hold is still valid.
- Never report success from a button click alone. Success requires reading the new deadline or equivalent confirmed server/UI state.
- If login, CAPTCHA, 2FA, or browser approval is required, ask JT to complete only that step and resume afterward.

## Reporting

Return a compact sanitized result:

- success or failure;
- OXXO or Banamex selected;
- old deadline and new deadline;
- whether the booking remained OnHold;
- whether PNR/flight/price remained unchanged;
- next planned renewal attempt, if applicable.

Never output the PNR, passenger identity, email, itinerary, payment reference, token, cookies, or API keys in chat or logs intended for the user.

## Known environment distinction

Codex CLI and Hermes' VPS Chrome use VPS egress and may reach the Viva shell while sensitive booking endpoints return `403` or “booking service unavailable.” Codex **Work** inside the ChatGPT/Codex desktop app has its own `@Browser` and may succeed where the VPS browser fails. Do not confuse model/provider identity with browser egress.
