# Portal Verification Playbook

## Evidence hierarchy

1. Live individual listing detail page.
2. Authenticated portal detail page.
3. Independent duplicate/corroborating detail page.
4. Portal search card.
5. Search-engine snippet.

Only levels 1–3 should establish hard facts. Cards and snippets are discovery aids.

## Authenticated browser pattern

1. Start or reuse the persistent VPS desktop browser.
2. Open protected portals in separate tabs.
3. Ask the user to complete login/CAPTCHA themselves.
4. Verify the tab title changed from the challenge page to a real result count.
5. Connect automation to the existing browser session when available.
6. Extract unique individual listing URLs from the result page.
7. Visit each URL and capture the complete visible text plus image URLs.
8. Parse and normalize fields; do not rely on card titles alone.

A productive unlocked-portal audit should report both the result count and the number of individual pages actually reviewed.

## Required fields per strict candidate

- Source and direct URL
- Checked date and listing freshness
- Rent
- Maintenance and whether included
- Other mandatory recurring charges
- Total known monthly cost
- Exact bedroom count
- Evidence that the unit is furnished
- Bathrooms and size
- Neighborhood/address precision
- Parking and security
- Lease/guarantor requirements
- Approximate commute to exact destination
- Visual-quality assessment and evidence limits

## Text interpretation

| Listing language | Interpretation |
|---|---|
| “Amueblado”, “totalmente amueblado”, “se entrega con muebles” | Furnished, subject to inventory confirmation |
| “Cocina equipada”, “línea blanca” | Appliances/kitchen only; not furnished |
| “Las fotos muestran muebles” | Unknown unless description confirms inclusion |
| “Sin muebles”, “no incluye muebles” | Exclude from furnished shortlist |
| “Opción de amueblar” | Pending; require final furnished price |
| “2 recámaras + estudio/family room” | Not 3 true bedrooms without physical verification |
| “3 recámaras” in card but 2 in description | Exclude or correct to 2 |

## Contradiction handling

If structured metadata and prose conflict:

1. Quote both values.
2. Calculate both possible totals.
3. Do not silently choose the favorable one.
4. Ask the advertiser to confirm in writing.
5. Keep it pending unless both interpretations satisfy all hard constraints.

## Visual review checklist

- Are all three bedrooms photographed?
- Does each show a bed, door, window, and usable storage?
- Are common areas genuinely furnished?
- Are photos consistent in flooring, windows, and layout?
- Are any images renders or AI staging?
- Is the building entrance shown?
- Does the exterior suggest controlled access, but avoid inferring safety from appearance alone?

## Final contact message template

> Hola, somos tres estudiantes y nos interesa el inmueble. ¿Sigue disponible? ¿La renta incluye mantenimiento? ¿Se entrega amueblado exactamente como aparece en las fotos? ¿Cada una de las tres recámaras tiene puerta, ventana, cama y clóset? ¿Aceptan tres estudiantes en un contrato y qué requisitos piden: aval, obligado solidario o póliza jurídica? ¿Podrían compartir video completo y ubicación aproximada antes de agendar visita?

## Fraud precautions

- Never transfer a holding deposit before viewing/video verification, advertiser identity/authority checks, and contract review.
- Confirm ownership or valid brokerage authority.
- Verify the unit number and inventory annex.
- Confirm deposits, advance rent, policy fees, maintenance, utilities, and refund terms in writing.
