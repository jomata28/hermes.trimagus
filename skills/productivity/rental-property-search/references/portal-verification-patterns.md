# Portal verification patterns

## Inmuebles24 and Vivanuncios

- A general CDMX query can be dominated by premium districts and does not establish that a requested neighborhood has no inventory.
- Query each target neighborhood separately using likely slugs and variants, then extract individual `/propiedades/clasificado/` or `/a-renta-.../` links.
- Result pages may contain cross-neighborhood recommendations; opening and checking every individual page is mandatory.
- Useful individual-page fields commonly include `Renta MN`, `Mantenimiento MN`, area, bedrooms, address, furnishing labels, publication age, and full description.
- Search descriptions for contradictory terms. Portal filters can return listings saying `sin muebles`, `no incluye mobiliario`, or `fotos ilustrativas`.

### Cloudflare blocking (as of 2026)

- **All major MX real estate portals are simultaneously behind Cloudflare**: Inmuebles24, Vivanuncios, Lamudi, EasyBroker, and Propiedades.com all present managed Cloudflare Turnstile challenges. Switching portals does not help when all are blocked at once.
- The `r.jina.ai` text-mirror fallback is **also Cloudflare-blocked** for these portals — jina.ai receives the same challenge page, not the listing content. Do not rely on jina.ai for Cloudflare-protected MX portals.
- Google Cache (`webcache.googleusercontent.com`) also returns a CAPTCHA from this network.
- A real Chrome (`google-chrome-stable` as user `jt` with SUID sandbox, not headless) does **not** auto-pass Cloudflare Turnstile. The challenge requires actual human interaction (clicking the checkbox) via the noVNC desktop.
- **Human-in-the-loop via noVNC is the only reliable path** for Inmuebles24/Vivanuncios: start the VPS desktop, launch Chrome as `jt` with `--remote-debugging-port`, send JT the noVNC URL, have him solve the Turnstile challenge, then extract listings via CDP. See `references/cdp-browser-extraction.md` for the reusable CDP page-reader script.

### MercadoLibre Inmuebles (not Cloudflare-protected)

- `inmuebles.mercadolibre.com.mx` is **not behind Cloudflare** and loads normally in both headless and VPS Chrome. It is a viable alternative when all other MX portals are blocked.
- URL pattern: `https://inmuebles.mercadolibre.com.mx/departamentos/renta/distrito-federal/<delegacion>/<colonia>/`
- The search results page exposes sidebar filters for: recámaras (including `3 recámaras`), price ranges (`Hasta MXN 30,000`), `Es amueblado`, surface area, baños, estacionamientos, and antigüedad.
- Listing cards show price, recámaras, baños, m² construidos, and address. Navigate to individual `/MLM-<id>` pages to verify furnishing and full details.
- Same furnishing verification rules apply: `amueblado` on the card is a lead; confirm on the individual page.

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
