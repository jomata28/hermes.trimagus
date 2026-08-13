# Portal verification patterns

## Inmuebles24 and Vivanuncios

- A general CDMX query can be dominated by premium districts and does not establish that a requested neighborhood has no inventory.
- Query each target neighborhood separately using likely slugs and variants, then extract individual `/propiedades/clasificado/` or `/a-renta-.../` links.
- Result pages may contain cross-neighborhood recommendations; opening and checking every individual page is mandatory.
- Useful individual-page fields commonly include `Renta MN`, `Mantenimiento MN`, area, bedrooms, address, furnishing labels, publication age, and full description.
- Search descriptions for contradictory terms. Portal filters can return listings saying `sin muebles`, `no incluye mobiliario`, or `fotos ilustrativas`.
- Human-completed Cloudflare challenges in a persistent noVNC Chromium profile can unlock browsing. The user must handle CAPTCHA/login; afterward automation may inspect the already-authenticated session.

## Facebook Marketplace

- Marketplace location/radius matters more than query wording. A CDMX-center radius can silently exclude Santa Fe/Cuajimalpa and repeat irrelevant inventory.
- Set the location to the target municipality/neighborhood and choose a suitable radius before extracting cards.
- Search cards are noisy: wrong zones, private rooms, sale listings, malformed `$1/$10` prices, and duplicate broker copies are common.
- Open each finalist and inspect the complete description. Searches for `amueblado` often surface listings that explicitly say `no amueblado`.
- Deduplicate by listing ID plus photos/text/property characteristics.

## Homie

- Individual pages expose rent and maintenance separately and may identify whether the unit is furnished.
- Location pages can produce unrelated recommended inventory; do not treat recommendation cards as local matches.

## Airbnb/Vrbo

- Use explicit check-in/check-out dates and guest count.
- If the page says dates unavailable or asks to add dates, there is no valid monthly quote.
- Search-result bedroom counts can disagree with the full description; trust the individual listing body.
- Do not convert a nightly or partial-stay figure into monthly rent.

## Pricing conflicts

When a page's structured maintenance field conflicts with prose saying maintenance is included, report both:

- Best case: rent + mandatory services.
- Conservative case: rent + displayed maintenance + mandatory services.

Require advertiser confirmation before ranking by final cost.

## Commute comparisons

- Use address-level geocoding when disclosed; otherwise label neighborhood-centroid estimates.
- Report distance and free-flow time separately from a cautious peak-hour range.
- For hospital workers/students, account for late-night safety and transport availability, not just kilometers.
