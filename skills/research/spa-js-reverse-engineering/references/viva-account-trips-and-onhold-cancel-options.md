# Viva account trips + OnHold cancel-options workflow

Session finding: when Viva's visible `my-trips` route is broken or returns a 404, the logged-in account API can still expose the user's reservation summaries. Use this reference for user-owned Viva booking diagnosis where the goal is to understand whether cancellation/reimbursement/payment options exist **without** sending messages, cancelling, paying, or publishing anything.

## Safety / action boundary

- Read-only diagnostics are okay: `account/trips`, `basket/create`, `basket/loadbooking`, `basket`, `canceloptions`, `irop/details`, payment status probes.
- Do **not** call mutating final actions (`booking/cancel`, `irop/cancel`, `irop/accept`, `compensations/process`, `payment/process`, `payment/selectmethod`, `payment/selectplan`, `booking/marketplace`, `account/trips/delete`) without explicit final confirmation from JT.
- `account/trips/delete` only removes a PNR from the profile trip list; do not describe it as cancelling the actual booking.
- If JT says “no envíes ningún mensaje,” do not draft or suggest contacting support until after exhausting on-site/API diagnosis.

## Read current trips

From the authenticated browser context, use the user's own session token and Akamai cookies:

```javascript
const tok = localStorage.getItem('viva-user-token');
const H = {
  'X-Channel': 'web',
  'x-api-key': '<captured-web-api-key>',
  'Authorization': 'Bearer ' + tok,
  'X-Requested-With': 'XMLHttpRequest'
};
const res = await fetch('https://api.vivaaerobus.com/web/v1/account/trips', {
  credentials: 'include',
  headers: H
});
console.log(await res.text());
```

Response shape:

```json
{
  "data": {
    "trips": [
      {
        "pnr": "VI2PWQ",
        "lastName": "Torres Alvarez",
        "status": "OnHold",
        "journeys": [
          {"origin":{"code":"IAH"},"destination":{"code":"GDL"},"flightNumber":"153,1392"}
        ],
        "tripType": "Roundtrip",
        "passengerCount": 1
      }
    ]
  }
}
```

This endpoint can reveal more reliable trip summaries than the SPA route when `/my-trips` is broken. It may also list older `Paid`, `Closed`, and `OnHold` trips.

## Inspect cancellation/reimbursement opportunity without mutating

For a user-owned booking, create a fresh Manage basket and load the booking. This is a legitimate read/management setup, not a cancellation.

```javascript
const pnr = 'PNR';
const lastName = 'Last Name';

const create = await fetch('https://api.vivaaerobus.com/web/v1/basket/create', {
  method: 'POST', credentials: 'include', headers: H,
  body: JSON.stringify({
    pnr, lastName, language: 'es-MX', currencyCode: 'MXN',
    customFields: { flowType: 'Manage' }
  })
}).then(r => r.json());

const basketId = create.data.basketId;

await fetch('https://api.vivaaerobus.com/web/v1/basket/loadbooking', {
  method: 'POST', credentials: 'include', headers: H,
  body: JSON.stringify({ basketId, pnr, lastName })
});

const basket = await fetch('https://api.vivaaerobus.com/web/v1/basket?BasketId=' + basketId, {
  credentials: 'include', headers: H
}).then(r => r.json());
console.log(basket);

const opts = await fetch('https://api.vivaaerobus.com/web/v1/booking/canceloptions?' +
  new URLSearchParams({ basketId, pnr, lastName }), {
    credentials: 'include', headers: H
  }).then(r => r.json());
console.log(opts);

const irop = await fetch('https://api.vivaaerobus.com/web/v1/irop/details?' +
  new URLSearchParams({ basketId, pnr, lastName }), {
    credentials: 'include', headers: H
  }).then(r => r.json());
console.log(irop);
```

Observed OnHold cancel-options result:

```json
{
  "data": {
    "status": "NotAvailable",
    "details": [{
      "status": "NoReimbursementReasons",
      "description": "There are no available reimbursement reasons for this booking."
    }],
    "fullReimbursementOptions": [],
    "partialReimbursementOptions": []
  }
}
```

IROP details may return:

```json
{
  "data": {
    "rebookStatus": "NotAvailable",
    "statusDetails": [{
      "status": "NoIropQueue",
      "description": "Booking is not in IROP queue"
    }]
  }
}
```

Interpretation: if cancel options are `NotAvailable` and IROP is `NoIropQueue`, there is no current server-recognized cancellation/reimbursement path.

## Do not skip payment-state inspection

JT corrected this explicitly: do not infer “unpaid” from `OnHold` without checking payment objects.

Inspect the basket fields:

```javascript
const d = basket.data;
console.log({
  basketStatus: d.status,
  flowType: d.flowType,
  totalAmount: d.totalAmount,
  totalBalance: d.totalBalance,
  paymentPlan: d.paymentPlan,
  installmentsAvailability: d.installmentsAvailability,
  dynamicFlow: d.dynamicFlow,
  payments: d.payments,
  travelPayments: d.travel?.payments
});
```

Durable Viva observations:

- `ExternalPayment` with `status: Pending` and `isExternalPaymentReferenceNeeded: true` means an external payment attempt/order exists but is not approved/reconciled; it is not the same as `Paid`.
- `paymentPlan: null` plus `api-apartados.../vb/v1/booking/paymentPlan` returning `BOOKING_NOT_FOUND` means the booking is **not** in an Apartados/payment-plan contract, even if it is `OnHold`.
- `totalBalance` can differ from `totalAmount`; preserve both when reporting payment state.
- A `travel.payments[0].status: Pending` after `payment/checkstatus` still leaving `account/trips.status: OnHold` means reconciliation did not convert the booking to `Paid`.

## Payment / OnHold probes that do not pay

Useful read-only or reconciliation-status probes:

```javascript
// GET is 405 for checkstatus; POST requires BasketId.
await fetch('https://api.vivaaerobus.com/web/v1/payment/checkstatus', {
  method: 'POST', credentials: 'include', headers: H,
  body: JSON.stringify({ basketId })
}).then(r => r.text()).then(console.log);
```

Observed failures:

- If the basket is passive: `BASKET_PASSIVE`.
- If `BasketId` omitted: validation error `BasketId is invalid`.

`booking/verify` is not a general payment/cancel unlock. It may return:

```json
{
  "parameters": [{
    "key": "Pnr",
    "message": "Verification is not available for provided booking. Organization code is invalid; Missing verification ssr. Expected verification ssrs are: VBJZ"
  }]
}
```

Treat that as a verification-product gate, not a cancellation path.

## Passive basket behavior

- `basket/create` + `basket/loadbooking` can return 200 but the resulting basket may still be `status: Passive`.
- `v1/booking`, `payment/methodsavailable`, and `payment/checkstatus` may then return `BASKET_PASSIVE`.
- `basket/keepalive` does not revive a passive basket; rebuild it, but if a fresh basket remains passive, treat it as a server-side flow block rather than a hidden UI toggle.

## Apartados host

Payment-plan endpoints live on a separate host:

```text
https://api-apartados.vivaaerobus.com/vb/v1/booking/paymentPlan
https://api-apartados.vivaaerobus.com/vb/v1/payment/methods-available
https://api-apartados.vivaaerobus.com/vb/v1/payment/process
https://api-apartados.vivaaerobus.com/vb/v1/booking/statement
```

If `paymentPlan` returns `BOOKING_NOT_FOUND` for the PNR, the booking is not registered as an Apartados plan. Do not label the hold as “apartado” solely because it is `OnHold`.

## `vb/v1` endpoint auth pitfall

Some Viva `vb/v1` endpoints are in the interceptor blacklist (`BUYBACK_URL`, `MARKETPLACE`, `GET_COMPENSATIONS_URL`, etc.). Angular may deliberately avoid adding the standard `Authorization: Bearer <token>` header to these URLs. Manually adding Bearer to those endpoints can produce gateway errors like `Invalid key=value pair ... in Authorization header` rather than a useful business response. Removing Bearer can instead return `Missing Authentication Token`; this means the endpoint likely needs a different gateway auth/signature or exact Angular-produced headers. Capture a successful Angular XHR before probing further.

## Visual-route pitfalls

- `/es-mx/my-trips` can return a Viva 404 while `account/trips` still has valid trip data.
- Legacy routes like `/mx/mi-vuelo/detalles-de-mi-reservacion?locator=...&email=...` or `/mx/mi-vuelo/pagar-mi-reservacion?...` may redirect to `/es-mx/` home without firing useful API calls. Prefer API diagnosis from the authenticated browser context.
- After creating/loading a fresh Manage basket, persist the basket into storage and open the SPA's internal Manage review route directly. This can expose the real payment UI even when legacy pay/detail routes redirect home:

```javascript
sessionStorage.setItem('BasketId', basketId);
localStorage.setItem('BasketId', basketId);
sessionStorage.setItem('BasketSrc', 'regular');
localStorage.setItem('BasketSrc', 'regular');
location.href = `https://www.vivaaerobus.com/es-mx/manage/review?basketId=${encodeURIComponent(basketId)}`;
```

If the page shows a generic `Lo sentimos... servicio no disponible` modal, close it and inspect the underlying page text before assuming the route failed; payment options may still be loaded behind the modal.

## Active Manage basket / payment-screen interpretation

A fresh Manage basket can remain `Active` even if older baskets have gone `Passive`. In this state, `GET /web/v1/booking?BasketId=...` may return full booking rules and `payment/methodsavailable` may return usable options.

Key fields to report:

```json
{
  "basket.status": "Active",
  "basket.flowType": "Manage",
  "booking.status": "OnHold",
  "booking.paidStatus": "UnderPaid",
  "booking.expirationDate": "...",
  "booking.minutesToExpire": 2076,
  "booking.irop": null,
  "booking.event": null,
  "basket.totalAmount": {"amount": 3047.69},
  "basket.totalBalance": {"amount": 10674.44}
}
```

Do not collapse `totalAmount` and `totalBalance` into one number: in Manage flow, the visible cart/modification total can differ from the booking balance.

Observed rule pattern for `OnHold` + `UnderPaid`:

| Rule | Meaning |
|---|---|
| `DisplayPayments: true` + `ProcessPayment: true` | Payment/reconciliation path exists; do not execute `payment/process` without explicit confirmation. |
| `ChangeJourneys: true` | A journey-change path may exist even while cancellation is blocked; verify with read-only rules before attempting changes. |
| `ChangeServices`, `ChangeSeats`, `ChangeBaggage`, `ChangePassengerNames: true` | Manage modifications may be available. |
| `DisplayCustomerCancellation: false` | Customer-cancel UI is intentionally disabled for `OnHold`. |
| `TotalRefundCancellation: false` | Total refund is disabled for `OnHold`. |
| `PartialPaymentCancellation: false` | Usually `NoPendingPaymentPlan` when there is no Apartados contract. |
| `IropCancellation: false` | Disabled by `OnHold` and/or no IROP type. |
| `FlexibilidadTotal`, `BuyBack`, `TransferBooking: false` | These can be explicitly disabled for `OnHold` even if other Manage actions work. |

Observed payment-method pattern from an active Manage basket:

- Commonly available: `CardPayment`, `StoredPayment`, `VivaCash`, `Voucher`, `PayPal`, MercadoPago/Yuno async wallets, ClickToPay wallets, sometimes Doters.
- Commonly unavailable in Manage: `ExternalPayment`, `Kueski`, `Uplift` (`DisallowFlowTypeConfigurableRule`), `PartialPayment` if too close to departure, and `PointsRewards` if no active method combination supports it.

## Public flight-monitoring pitfall

For `plannedFlights`, the VPS/curl default User-Agent worked, while forcing a generic `User-Agent: Mozilla/5.0` caused Akamai to complete TLS but return no body until timeout. If public Viva schedule calls start hanging only in scripts, remove the browser-like UA and retry with curl defaults before concluding the endpoint is down.
