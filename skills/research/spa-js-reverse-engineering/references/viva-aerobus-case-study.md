# Viva Aerobus — JS Reverse Engineering Reference

PNR DGCRHQ case study (2026-08-04) + bundle re-analysis (2026-08-16)

## Bundle versions
| Date | Bundle hash | Size | Angular |
|---|---|---|---|
| 2026-08-04 | `main.fb03daf92fe221a8.js` | ~2.5MB | 19.2.25 prod |
| 2026-08-16 | `main.8fbb310697f5850a.js` | ~2.68MB | 19.2.25 prod |

Re-download and diff bundles periodically — Viva ships updates. Extract URLs from HTML:
```bash
curl -s 'https://www.vivaaerobus.com/es-mx' | grep -oP 'src="([^"]+\.js)"' | cut -d'"' -f2
```

## Complete endpoint catalog (from 2026-08-16 bundle)

All URLs use base `l` = `https://api.vivaaerobus.com/web/` and base `w` = global API base.
All API calls need: `x-api-key`, `X-Channel: web`, `Authorization: Bearer <token>`, `credentials: 'include'`

### Booking & Basket
| Constant | URL | Method | Notes |
|---|---|---|---|
| `FULL_BOOKING_URL` | `v1/booking/full` | GET | `?pnr=...&lastName=...` |
| `BASKET_BOOKING_URL` | `v1/booking` | - | Base booking |
| `BASKET_URL` | `v1/basket` | - | Base basket |
| `CREATE_BASKET_URL` | `v1/basket/create` | POST | Does NOT check booking status |
| `LOAD_BASKET_BOOKING_URL` | `v1/basket/loadbooking` | POST | Binds PNR to basket |
| `UPDATE_BASKET_URL` | `v1/basket/update` | - | |
| `KEEP_ALIVE_BASKET_URL` | `v1/basket/keepalive` | - | |
| `BOOKING_CANCEL_URL` | `v1/booking/cancel` | POST | Needs BasketId + JourneyKeys |
| `CANCEL_OPTIONS_URL` | `v1/booking/canceloptions` | GET | Needs BasketId |
| `BOOKING_VERIFY_URL` | `v1/booking/verify` | - | |
| `PNR_RECOVERY_URL` | `vb/v1/booking/recover` | - | Recover lost PNR |
| `ADD_PASSENGERS_URL` | `v1/booking/passengers` | - | |
| `UPDATE_PASSENGERS_URL` | `v1/booking/updatepassengers` | - | |
| `UPDATE_EMAIL_PASSENGERS_URL` | `vb/v1/booking/updatepassengeremail` | - | |
| `PASSENGER_RULES_URL` | `v1/booking/passengerrules` | - | |
| `JOURNEYS_BOOKING_BASKET_URL` | `v1/booking/journeys` | POST | Change journeys |
| `CHANGE_JOURNEYS_AVAILABILITY_URL` | `v1/booking/changejourneys` | - | |
| `CHANGE_SEATS_URL` | `v1/booking/changeseats` | - | |
| `CHANGE_SERVICES_URL` | `v1/booking/changeservices` | - | |
| `CHANGE_INSURANCES_URL` | `v1/booking/changeinsurances` | - | |
| `ACCEPT_SEATS_URL` | `v1/booking/acceptseats` | - | |
| `PROPOSED_SEATS_URL` | `v1/booking/proposedseats` | - | |
| `SEATMAPS_URL` | `v1/booking/seatmaps` | - | |
| `BUNDLES_URL` | `v1/booking/bundles` | - | |
| `BUNDLES_AVAILABILITY_URL` | `v1/booking/availablebundles` | - | |
| `AVAILABLE_SERVICES_URL` | `v1/booking/availableservices` | - | |
| `AVAILABLE_INSURANCES_URL` | `v1/booking/availableinsurances` | - | |
| `INSURANCES_STATUS_URL` | `v1/booking/insurancesStatus` | - | |
| `UPSELL_SERVICES_URL` | `v1/booking/upsellservices` | - | |
| `CHECK_AVAILABILITY_URL` | `v1/booking/searchavailability` | - | |
| `SEARCH_JOURNEY_AVAILABILITY_URL` | `v1/booking/searchjourneys` | - | |
| `ADD_HOTEL_URL` | `v1/booking/hotel` | - | |
| `DELETE_HOTEL_URL` | `v1/booking/deletehotel` | - | |
| `TUALIADO_URL` | `v1/booking/tua` | - | TUA (airport tax) |
| `MEXICAN_TOURISM_TAX_URL` | `v1/booking/mexicantourismtaxverification` | - | |
| `ACCRUAL_DETAILS_URL` | `vb/v1/booking/accrualdetails` | - | Doters accrual |
| `POST_ACCRUAL_URL` | `vb/v1/booking/postaccrual` | - | |
| `DOCUMENT_VALIDATION` | `vb/v1/booking/documentValidation` | - | |
| `BAG_ENQUIRY` | `vb/v1/booking/bagEnquiry` | - | |

### IROP (Irregular Operations)
| Constant | URL | Method | Notes |
|---|---|---|---|
| `IROP_CANCEL_URL` | `v1/irop/cancel` | POST | Needs ReimbursementMethod, NOT OnHold-gated |
| `IROP_DETAILS_URL` | `v1/irop/details` | GET | Returns NoIropQueue if not disrupted |
| `IROP_ACCEPT_URL` | `v1/irop/accept` | POST | Accept IROP solution |
| `IROP_REDEEM_COMPENSATION_URL` | `v1/irop/redeemcompensation` | POST | Redeem IROP compensation |
| `IROP_KEEP_URL` | `vb/v1/booking/irop/keepflight` | POST | Keep flight during IROP |
| `IROP_CANCEL_RESEND_EMAIL_URL` | `vb/v1/booking/mail/cancel` | POST | Resend cancel email |
| `IROP_REASON_MODAL_URL` | `service/v1/fsnc/plannedFlights` | GET | Schedule + IROP status |

### Marketplace / BuyBack (NEW — NFT ticket resale)
| Constant | URL | Notes |
|---|---|---|
| `BUYBACK_URL` | `vb/v1/booking/buyback` | Sell reservation back to Viva. Needs JWT auth. |
| `MARKETPLACE` | `vb/v1/booking/marketplace` | Publish reservation for resale |
| `BUYBACK_WHITE_LABEL_URL` | `https://marketplace.vivaaerobus.com/nftickets` | NFT ticket marketplace platform |

Rule types: `BuyBack`, `SellBack`, `MarketplacePublished`, `Peer2Peer`

### Payment Plan / Apartado (NEW)
| Constant | URL | Notes |
|---|---|---|
| `PLAN_OPTIONS` | `v1/payment/planoptions` | View apartado options. Needs BasketId + DownPaymentAmount |
| `SELECT_PLAN` | `v1/payment/selectplan` | Select payment plan |
| `DELETE_PLAN` | `v1/payment/deleteplan` | Cancel plan |
| `PAYMENT_PLAN` | `vb/v1/booking/paymentPlan` | Plan details |
| `PAYMENT_PLAN_METHODS` | `vb/v1/payment/methods-available` | Available payment methods for plan |
| `PAYMENT_PLAN_PAYMENT_PROCESS` | `vb/v1/payment/process` | Process plan payment |
| `PAYMENT_PLAN_PAYMENT_STATEMENT` | (vb/v1/payment/...) | Payment statement |
| `PAYMENT_METHODS` | `v1/payment/methodsavailable` | All payment methods |

Apartado detection: `getReserveType()` returns `"apartados"` when `paymentPlan.pendingQuantity > 0`
Plan structure: `downPaymentAmount`, `paymentDetails[]` (with `partialAmount`), `frequency`, `pendingQuantity`
Charge groups: `InitialPaymentHoldTrip`, `PendingPaymentsHoldTrip`

### Compensations
| Constant | URL | Notes |
|---|---|---|
| `GET_COMPENSATIONS_URL` | `vb/v1/booking/compensations` | Available compensations |
| `PROCESS_COMPENSATION_URL` | `vb/v1/booking/compensations/process` | Process compensation |

Compensation types: `SeatDowngrade`, `CancelFlight`, `FoodVoucherCompensation`, `DelayCompensation`, `PostFlightMove`, `MoveFlight`, `VBCashCompensation`
Compensation formats: `Vivacash`, `Voucher`

### VivaCash Wallet (NEW — full endpoint set)
| Constant | URL | Notes |
|---|---|---|
| `ACCOUNT_VIVACASH` | `v1/account/vivacash` | Base VivaCash account |
| `ACCOUNT_VIVACASH_V2` | `v2/account/vivacash` | V2 endpoint |
| `ACCOUNT_VIVACASH_WALLET` | `vb/v1/vivacash/checkout/balance` | Wallet balance |
| `ACCOUNT_VIVACASH_GENERATE_REFERENCE` | `v1/account/vivacash/generatereference` | Generate payment reference |
| `ACCOUNT_VIVACASH_TRANSACTIONS` | `v1/account/vivacash/transactions` | Transaction history |
| `ACCOUNT_VIVACASH_ACTIVE_REFERENCES` | `v1/account/vivacash/activereferences` | Active references |
| `ACCOUNT_FUNDS_URL` | `v1/account/funds` | Account funds (Doters + VivaCash) |

### Flight Status & Notifications (NEW)
| Constant | URL | Notes |
|---|---|---|
| `FLIGHT_STATUS_URL` | `vb/v1/flightstatus` | Flight status by number+date |
| `FLIGHT_STATUS_ADD_NOTIFICATION_URL` | `vb/v1/notifications/add` | Subscribe to flight notifications |
| `FLIGHT_STATUS_CANCEL_SUBSCRIPTION_URL` | `vb/v1/notifications/delete` | Cancel subscription |
| `FLIGHT_STATUS_SUBSCRIPTIONS_URL` | `vb/v1/notifications/subscriptions` | List subscriptions |

### Availability & Search
| Constant | URL | Notes |
|---|---|---|
| `SEARCH_AVAILABILITY_URL` | `v1/availability/search` | POST — blocked by Akamai via curl |
| `SEARCH_AVAILABILITY_OFFERS_URL` | `v1/availability/searchOffers` | Global offers |
| `LOW_FARES_URL` | `v1/availability/lowfares` | Low fare search |
| `LOW_FARES_CACHE_URL` | `vb/v1/availability/lowfares` | Cached low fares |
| `LOW_FARE_GQL_URL` | `vb/v1/lf/graph` | GraphQL low fares |
| `LOW_FARE_GROUP_BASE_URL` | `vb/v2/lf/group` | Group low fares |
| `CALENDAR_AVAILABILITY_URL` | `v1/availability/schedule` | Calendar view |
| `GLOBAL_SEARCH_AVAILABILITY_URL` | `v1/availability/search` | Global (uses `w` base) |

### Account
| Constant | URL | Notes |
|---|---|---|
| `LOGIN_URL` | `v1/account/login` | |
| `SOCIAL_LOGIN_URL` | `v1/account/sociallogin` | |
| `ACCOUNT_LOGIN_EXTERNAL_URL` | `v1/account/loginexternal` | SSO |
| `ACCOUNT_URL` | `v1/account` | |
| `ACCOUNT_CONFIRM_URL` | `v1/account/confirmregistration` | |
| `ACCOUNT_UPDATE_URL` | `v1/account/update` | |
| `ACCOUNT_RESTORE_URL` | `v1/account/restore` | |
| `ACCOUNT_PWD_RESET_REQ_URL` | `v1/account/requestpasswordreset` | |
| `VALIDATE_TOKEN_URL` | `v1/account/validatetoken` | |
| `ACCOUNT_STAFF_STANDBY` | `vb/v1/myidtravel/link` | Staff standby (Viva Amigos) |
| `ACCOUNT_UPLOAD_PHOTO` | `vb/v1/account/uploadPhoto` | |
| `SMILE_FLY_URL` | `vb/v1/faceid/url` | FaceID check-in |

### OTP (One-Time Password)
| Constant | URL | Notes |
|---|---|---|
| `OTP_GENERATE_URL` | `vb/v1/booking/otp/generate` | Generate OTP |
| `OTP_OPTIONS_URL` | `vb/v1/booking/otp/options` | OTP options |

### Resources (public, no auth needed)
| Constant | URL | Notes |
|---|---|---|
| `STATIONS_URL` | `vb/v1/resources/stations` | ✅ 164 stations with destinations. Works with only x-api-key |
| `COUNTRIES_URL` | `v1/resources/countries` | |
| `CURRENCIES_URL` | `v1/resources/currencies` | |
| `PROVINCES_URL` | `v1/resources/provinces` | |

### Transfer & Gift
| Constant | URL | Notes |
|---|---|---|
| `TRANSFER_URL` | `v1/transfer/initiate` | Transfer booking to another person |
| `GIFT_RESEND_CODE` | `vb/v1/giftcardResend` | Resend gift card code |
| `SHARE_ITINERARY_URL` | `vb/v1/share/trip` | Share trip details |
| `SHARE_CONFIRMATION_ITINERARY_URL` | `vb/v1/share/confirmation` | Share confirmation |

### Other
| Constant | URL | Notes |
|---|---|---|
| `CC_BIN_SERVICE_URL` | `vb/v1/bin` | Credit card BIN lookup |
| `IDENTITY_DOCUMENT_URL` | `vb/v1/identity/addDocument` | Add identity document |
| `BOXEVER_API` | `https://api.boxever.com` | Personalization engine |

## Endpoints accessible WITHOUT login (only x-api-key)

| Endpoint | Confirmed working |
|---|---|
| `plannedFlights` | ✅ 110 flights from MTY on 2026-08-16 |
| `stations` | ✅ 164 stations, full destination graph |
| `flightstatus` | ⚠️ Returns error without correct params |

## Endpoints requiring JWT (`Authorization: Bearer <token>`)

`buyback`, `marketplace`, `payment/planoptions`, `compensations`, `booking/full`, `irop/*`, `transfer/initiate`, `account/*`, `basket/*`

## Working API Call Pattern (browser console)
```javascript
const token = localStorage.getItem('viva-user-token');
const apiKey = 'zasqyJdSc92MhWMxYu6vW3hqhxLuDwKog3mqoYkf';
const res = await fetch('https://api.vivaaerobus.com/web/v1/booking/full?pnr=DGCRHQ&lastName=Torres%20Alvarez', {
  method: 'GET',
  credentials: 'include',  // CRITICAL: sends Akamai cookies
  headers: {
    'Authorization': 'Bearer ' + token,
    'X-Channel': 'web',
    'x-api-key': apiKey,
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*'
  }
});
```

## Troubleshooting progression
403 (blocked) → 405 (wrong method) → 400 (validation) → 200 (success).
- 403: Missing `credentials: 'include'` or wrong/missing headers, or Akamai blocking curl
- 405: Wrong HTTP method — swap GET ↔ POST
- 400: Auth correct! Fix params/body
- `Missing Authentication Token`: JWT token not provided (buyback, marketplace, etc.)

## Basket Session Flow
```javascript
// 1. Create basket (does not check status)
POST /web/v1/basket/create
Body: {pnr, lastName, language: 'es-MX', currencyCode: 'MXN'}
→ {data: {basketId: '019fce8c-...'}, type: 'SUCCESS'}

// 2. Load booking into basket
POST /web/v1/basket/loadbooking
Body: {basketId, pnr, lastName}
→ {data: {}, type: 'SUCCESS'}
```

## Cancel endpoint shape
```javascript
POST /web/v1/booking/cancel
Body: {pnr, lastName, basketId, journeyKeys: ['...', '...']}
```

## IROP Cancel endpoint shape
```javascript
POST /web/v1/irop/cancel — different gate than regular cancel
Body: {basketId, pnr, lastName, journeyKeys, reimbursementMethod: 'VivaCash'}
// Error when no IROP: {"code":"IROP_UNAVAILABLE","message":"Booking is not in IROP queue"}
```

## Payment methods enum (complete, 2026-08-16)
```
CardPayment, StoredPayment, ExternalPayment, PayPal,
OnlinePostBookingPayment, Voucher, VivaCash, AccountCredit,
Uplift, NoPayment, ScotiaPoints, Kueski, Rappi, PayLater,
PointsRewards, PayLaterStaff, Doters, PresentCardKiosk,
YunoCard, YunoAsync_MercadoPagoCheckoutPro, YunoAsync,
YunoWallet, YunoWallet_ClickToPay, IberiaCardPayment,
PartialPayment, EP_Oxxo, EP_SafetyPay
```
New since 2026-08-04: Rappi, Yuno (MercadoPago, ClickToPay), IberiaCardPayment, EP_SafetyPay

## Booking statuses enum
`Pending → Paid → OnHold → PendingPayment → Cancelled → Closed → Archived → PaidInFull → OverPaid`

## Rule types (server-side gates, complete)
`BuyBack`, `SellBack`, `MarketplacePublished`, `Peer2Peer`, `FlexibilidadTotal`, `FlexibilitySell`, `FlexibilityTransfer`, `TransferBooking`, `TotalRefundCancellation`, `TotalRefundCancellationOffer24h`, `DisplayCustomerCancellation`, `ChangeJourneys`, `ChangeJourneysAndRoute`, `ChangeJourneysFlyAhead`, `IropCancellation`, `IropReimbursementPending`, `ProcessIropCompensation`, `IropCompensation`, `KeepFlightSelected`, `ChangeSeatsIrop`, `CallCenterCompensation`, `FixedCompensationCard`, `Binding`, `SoftBinding`, `SeatDowngrade`, `CancelFlight`, `FoodVoucherCompensation`, `DelayCompensation`, `PostFlightMove`, `MoveFlight`, `VBCashCompensation`, `PassengerCheckedIn`, `InsurancesStatus`, `AccrualPostBookingViva`

## Feature flags (complete, 2026-08-16)
- `ShowVivaCashCancellationModalInMMB`
- `EnableRefundableFare`
- `EnableUnifiedFlowDoters`
- `EnableVivaCandyFlow`
- `EnableVivaCandyProcessingHashWorkaround`
- `AutoDotersPayment`
- `DisplayKueskiDetailsModal`
- `DotersAutoToogleSelection`
- `PrioritizeExternalPaymentForPaymentPlan`
- `AccrualPostBookingViva` / `AccrualPostBookingVivaAndAltCarriers`
- `ShowCarbonModal`
- `ShowPetSwornStatement`
- `ShowCalendarFares`
- `MaintenanceSettingsPolling`
- `EnableVivaFan`
- `UsePayPalButton`
- `UseCache`
- `SendMaleAsDefault`
- `LogoutGuestFee`
- `DisplayAccumulationPerPassenger`

## localStorage Keys
- `viva-user-token` — JWT auth token
- `viva-user-etoken` — External (SSO) auth token
- `dataFullBasket` in **sessionStorage** — `{pnr, lastName}` only
- `dotersTermsSeen` — Doters terms acceptance flag

## SSR (Service Request) codes
- `VAJR` — Refundable Fare (per segment)
- `VBJL` — Total Refund Service charge
- `VBDB` — 10kg Carry-on Bag
- `VTUI` — Mexico Departure Tax
- `VLIG` — Bundle Light
- `VTUA` — TUA (airport tax)
- `MCI` — Monthly Installment Charge

## Stations data
- 164 total stations across MX, US, CO, CU, ES, DE, FR, GB, IT, PT, etc.
- MTY has 160 destinations (62 direct, 98 connecting)
- CUN has 156 destinations (largest leisure hub)
- GDL has 154 destinations
- Stations endpoint returns full route graph: each station lists all destinations with `travelType` (Direct/Connecting), `countryCode`, `transportationType`

## Schedule-Diff Strategy (cancel-before-public detection)

Detect cancellations after the airline has decided but before they've told passengers.

### How it works
1. Daily snapshot: Poll `plannedFlights?origin=HUB&flightDate=YYYYMMDD` for all hubs, 14 days forward
2. Diff: Compare today's snapshot against yesterday's
3. Classify: 4-level classification for disappeared flights
4. Confirm: Flight absent for 2+ consecutive snapshots = confirmed cancellation

### Classification logic
```
Level 1 — Route capacity check: same or more flights → RENUMBERED_OR_RETIMED
Level 2 — New survivor check (only NEW flights): close in time → RETIMED
Level 3 — Route lost capacity, nothing nearby → CANCELLED_CANDIDATE
Level 4 — Flicker guard: absent 2+ snapshots → CONFIRMED
```

### Bugs fixed during build
1. History persistence: candidates must be saved to JSON across runs
2. Flight number matching: key on `(flight_number, route)` not just `flight_number`
3. Retime false positives: only match against NEW survivors
4. Silent row loss: log dropped rows from unparseable timestamps

### Monitors
| Monitor | Frequency | Detection | Lead time |
|---|---|---|---|
| IROP Monitor | Every 5 min | `noControlableMessages` changes | Hours |
| Schedule Diff | 3×/day (3am, 3pm, 10pm UTC) | Flight disappears from schedule | 1-4 days |

### Weather data
NOAA Aviation Weather Center (free, no key):
- METAR: `https://aviationweather.gov/api/data/metar`
- Airport-specific hazard thresholds: fog (TIJ), tropical (CUN/PVR), convective (MTY/GDL), wind (CJS/TRC)

## Key findings
- `bookingId != BasketId`: Cancel endpoint rejects bookingId as invalid BasketId
- `OnHold`/`UnderPaid` status disables ALL cancel/refund/change rules server-side
- `rules[]` array in booking response shows exactly what's blocked and why
- Basket creation does NOT check booking status (OnHold bypass via basket/create)
- IROP cancel checks IROP queue, NOT booking status (different gate)
- Marketplace/buyback endpoints require JWT auth (return "Missing Authentication Token" without it)
- `availability/search` is blocked by Akamai when called via curl — only works from browser with Akamai cookies
- `stations` endpoint works with only x-api-key (no JWT needed)
- `payment/planoptions` needs BasketId + DownPaymentAmount (not just BasketId)
- x-api-key: `zasqyJdSc92MhWMxYu6vW3hqhxLuDwKog3mqoYkf`

## Journey Keys for DGCRHQ
- IAH→MTY VB617: `VkJ_IDYxN34gfn5JQUh_MDkvMDQvMjAyNiAyMzoxMH5NVFl_MDkvMDQvMjAyNiAyMzo0NX5_`
- MTY→IAH VB610: `VkJ_IDYxMH4gfn5NVFl_MDkvMDcvMjAyNiAwNjowMH5JQUh_MDkvMDcvMjAyNiAwODozNX5_`
