# Gmail email data fallback (when browser can't load a bot-protected SPA)

Use this technique when a website (especially an airline/hotel/booking SPA behind Akamai, Cloudflare, or similar bot protection) won't load in a headless browser. The site's **confirmation email in Gmail** often contains more structured data than the SPA would render — and it's accessible without fighting anti-bot measures.

## Triggers

Reach for this when:
- `browser_navigate` times out with `Page.navigate` or `domcontentloaded` CDP errors
- The site is behind Akamai (`X-Akamai-*` headers), Cloudflare, or similar
- curl/Python `urllib` can reach the site but headless Chrome/Playwright cannot (network fingerprinting)
- Direct API calls to the site's backend also time out (bot-filtered API gateway)

## Availability

The `google_api.py` script (at the path below) has full Gmail access with `gmail.readonly`, `gmail.send`, and `gmail.modify` scopes. Available subcommands:

| Command | Purpose |
|---|---|
| `gmail search` | Search by query (same syntax as Gmail web) |
| `gmail get` | Fetch a full message by ID (returns HTML body) |
| `gmail send` | Send a new email |
| `gmail reply` | Reply to an existing thread |
| `gmail labels` | List all labels |
| `gmail modify` | Add/remove labels on a message |

Always try Gmail before telling the user you cannot access their email. The token is already configured.

## Workflow

### 1. Search Gmail for the confirmation

```bash
# By specific PNR/code
python $GA gmail search "Viva Aerobus DGCRHQ" --max 5

# Broader search if PNR search returns nothing
python $GA gmail search "Viva Aerobus" --max 10

# Look for other senders
python $GA gmail search "reservation@|confirmacion@|info.vivaaerobus.com" --max 10
```

The `$GA` path is:

```bash
GA=/root/.hermes/skills/productivity/productivity-suite-workflows/references/google-workspace-package/scripts/google_api.py
```

### 2. Get the full email body

```bash
python $GA gmail get <message_id>
```

The `get` command returns the full email body as an HTML string (typically 200K-350K chars). Important fields returned: `id`, `from`, `to`, `subject`, `date`, `body` (HTML).

### 3. Extract structured data from JSON-LD

Viva Aerobus (and many other airlines/OTAs) embed [Schema.org JSON-LD](https://schema.org/FlightReservation) in their confirmation email HTML. Extract it with grep or a parser:

```bash
# Quick check: grep for @type and reservationNumber
echo "$BODY" | grep -oP '"@type":"FlightReservation"[^}]+}' | head -3
```

Parse into usable fields:

```python
import re, json
matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', email_body, re.DOTALL)
for m in matches:
    data = json.loads(m)
    # data[0] might be Organization, data[1] is FlightReservation
```

### 4. Key data fields typically available

From a Viva Aerobus confirmation email JSON-LD:

| Field | Path |
|---|---|
| Reservation number | `reservationNumber` |
| Passenger name | `underName.name` |
| Flight number | `reservationFor.flightNumber` |
| Airline | `reservationFor.airline.name` / `iataCode` |
| Departure airport | `reservationFor.departureAirport.iataCode` |
| Arrival airport | `reservationFor.arrivalAirport.iataCode` |
| Departure time | `reservationFor.departureTime` (ISO 8601) |
| Arrival time | `reservationFor.arrivalTime` (ISO 8601) |
| Check-in URL | `checkinUrl` |
| Modify URL | `modifyReservationUrl` |
| Status | `reservationStatus` |

For round trips, there are two `FlightReservation` blocks — one per leg.

## Common Viva Aerobus email senders

| Sender | Email address |
|---|---|
| Confirmation | `reservations@vivaaerobus.com` |
| Check-in reminders | `notificacion@info.vivaaerobus.com` |
| Promotions | `reservation@vivaaerobus.com` |

## Pitfalls

- **Subject doesn't always contain the PNR.** The confirmation email subject is typically `"Confirmación de reservación | Viva"` without the PNR visible. Search by sender + date, or search the PNR directly — it gets indexed even if the subject doesn't contain it.
- **Email body can be huge.** Viva Aerobus confirmation emails are ~350KB of inline HTML with lots of tracking pixels, spacer tables, and footer content. Use targeted grep for JSON-LD rather than trying to parse the entire HTML.
- **Gmail API is fast.** `gmail get` returns the full body almost instantly — no need to work with truncated snippets.
- **The email data is more reliable than the SPA.** The confirmation email contains schema.org data that the SPA renders via API calls that may fail. Prefer email extraction when both are available.
- **Always try Gmail before telling the user you can't access their email.** The token is already configured with `gmail.search`, `gmail.get`, `gmail.send`, and `gmail.modify` scopes. A "sorry, I can't access your email" will frustrate the user when a simple `gmail search` would have worked.

## Viva Aerobus email analysis pattern

For extracting cancellation/refund info from a confirmation email after getting the body with `gmail get`:

```bash
python "$GA" gmail get <message_id> | python3 -c "
import sys, json, re
data = json.load(sys.stdin)
body = data.get('body', '')
text = re.sub(r'<[^>]+>', '\n', body)
text = re.sub(r'&[a-z]+;', ' ', text)
text = re.sub(r'\n\s*\n', '\n\n', text)

for kw in ['cancel', 'reembol', 'refund', 'cambio', 'vivacash', 'viva cash', 'total', 'pago', 'mxn']:
    for m in re.finditer(kw, text, re.I):
        start = max(0, m.start() - 80)
        end = min(len(text), m.end() + 120)
        snippet = text[start:end].strip().replace('\n', ' | ')
        print(f'[{kw.upper()}] {snippet}')
"
```

Key fields to extract: `Pagos aprobados`, `Pago pendiente`, `Total de la reserva`, payment deadline, fare type (e.g. `Tarifa Switch Reembolsable`), and additional services (`Tarifa Reembolsable`).