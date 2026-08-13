# Live Rental Listing Research

Use this workflow when compiling current, deduplicated housing listings from multiple portals, especially when major marketplaces are bot-protected.

## Evidence standard

A listing may enter the final table only when the individual listing URL or a current source page exposes enough fields to identify it. Do not turn search-category counts, snippets, or inaccessible result cards into fully specified listings.

For every row, retain:

- Source and canonical listing URL
- Stable listing/property ID when available
- Title/address or development name
- Monthly rent and currency
- Exact bedroom count
- Furnished status only when explicit
- Maintenance amount/inclusion only when explicit
- Publication/update date, or an honest retrieval-status label
- Location precision used for distance/commute estimate

Use `Not stated` rather than inferring furnishing, maintenance, or amenities from photos or market norms.

## Multi-source collection under access controls

1. Search each requested portal directly first.
2. If a portal blocks direct retrieval, try its public category/index page and current search-engine result pages.
3. A text-rendering proxy such as `https://r.jina.ai/https://...` can expose server-rendered public content and structured listing cards. Treat it as an alternate renderer, not a separate source.
4. Search source-specific queries for listing-level URLs, stable IDs, prices, bedroom terms, development names, and streets.
5. Consult aggregators only to discover candidates. Prefer the originating portal or agency page for the final row.
6. Report blocked/inaccessible sources transparently, but do not imply that searching a source produced verified individual rows when it did not.

Do not persist claims that a portal is generally inaccessible: access controls vary by session. Retry direct, index, search-engine, and alternate-renderer paths each time.

### Confirm that portal filters actually applied

Rental and travel portals may return fallback, sponsored, or worldwide recommendations even when the request URL contains a neighborhood, whole-unit filter, bedroom count, or dates. Before evaluating a candidate:

1. Verify the candidate's displayed city/neighborhood and, when exposed, coordinates. Reject off-geography results even if they came from the intended search URL.
2. Require the same listing object/card/ID to contain the required bedroom count, whole-unit or furnished status, and price. Do not join nearby strings from different cards in flattened HTML or serialized state.
3. For Airbnb/Vrbo, bind `total mensual` to the same listing ID, exact check-in/check-out dates, and bedroom field; include mandatory taxes/fees shown in that total and exclude it when the all-in amount exceeds the cap.
4. Treat `no results` followed by “more properties,” recommendations, or sponsored inventory as fallback content—not matches to the active filters.
5. If a promising category card's canonical detail URL is 404, redirects to search, or no longer exposes the qualifying fields, reject it rather than citing the card as a verified individual listing.
6. A link labeled `3 or more bedrooms` is not proof that the active page enforced exactly three; verify the detail page.

## Cross-checking listing fields

Portal search cards and detail pages can disagree or render labels incorrectly. Before asserting an **exact** bedroom count:

1. Compare the category/card bedroom count with the detail-page title, description, and structured fields.
2. A current collection card and a live individual detail page may be used jointly only when they share the same stable listing ID/canonical URL: retain the card evidence for fields omitted by the detail renderer and the detail evidence for current page status. Record this as a joined verification, not as if every field appeared on the detail page.
3. If the detail page displays a conflicting count, omit the candidate or mark it `conflicting—verify`; do not silently choose the favorable value.
4. Watch for parser/layout shifts where a numeric value appears without its label, bedrooms are mislabeled as bathrooms, or a title says one bedroom count while the card badge says another.
5. Treat near-identical units in the same development as separate only if they have distinct IDs and materially distinct unit facts; otherwise deduplicate conservatively.

## Deduplication

Normalize and compare:

- Canonical URL and stable ID
- Street/building/development
- Rent
- Bedroom count
- Area in square meters
- Photo fingerprints when available
- Agency description text

Listings mirrored across portals should become one row with primary and alternate URLs. Different units in the same building may remain separate if their IDs, rent, area, floor, or furnishing differ.

## Freshness labels

Use the strongest defensible label:

- `Published <date>` or `Updated <date>` when shown by the source
- `Live page retrieved <date>` when the individual page loaded but no publication date was exposed
- `Present in current results <date>` when only a current result card was accessible
- `Unverified/stale` candidates should not be mixed into the live table

A page loading successfully does not prove vacancy. Always advise confirming availability before documents or payment.

## Budget semantics

Clarify whether the cap applies to advertised base rent or to the effective monthly housing cost. When the request simply says `precio/renta ≤ cap`, include base-rent matches but add an explicit `known monthly total` field:

- If maintenance is included, total equals advertised rent.
- If maintenance is stated separately, compute rent + maintenance and flag any cap breach.
- If maintenance is not stated, write `total unknown` rather than implying the property fits an all-in cap.
- A base rent exactly at the cap has no room for an additional fee; highlight it for confirmation.

## Distance and commute

1. Geocode the hospital entrance and the listing's best available location.
2. Prefer route distance/time from a live maps service and state travel mode plus retrieval time.
3. If the listing hides its location, label the estimate as neighborhood/street-level and use a range.
4. If geocoding fails, retry with successively broader queries (exact address → street → development/landmark → neighborhood centroid) and with a second geocoder. Never substitute a similarly named result outside the target city.
5. Use a routing engine only for successfully geocoded origins. Identify its time as free-flow/modelled rather than live traffic unless the service explicitly supplies current traffic.
6. Never present mentally estimated kilometer or drive-time ranges as measured values. If no origin can be geocoded, label any qualitative proximity separately and omit numeric distance/time.
7. Note that peak traffic can materially change Santa Fe travel times.

## Safety framing

Do not declare a neighborhood or building safe solely because it is affluent or gated. Rank practical suitability using observable features:

- Short route to hospital/school, especially for late shifts
- 24/7 staffed access, controlled entry, CCTV, and interior pickup/drop-off
- Well-lit pedestrian route and nearby active frontage
- Reliable transport and ride-hail access
- Three legal bedrooms with doors/windows

Frame area recommendations as relative suitability, not guarantees. Recommend an in-person daytime and nighttime route check.

## Empty-result and strict-filter audits

When no listing survives all hard filters, the zero-result answer still needs an auditable evidence trail:

1. Build a source-coverage matrix with `source requested`, `retrieval route`, `individual pages inspected`, and `reason no row survived`. Do not say a source was searched merely because a generic web query mentioned it; distinguish direct inspection, indexed discovery, and no retrievable candidate.
2. Name a small set of representative near-misses only when their individual pages were verified. For each, state the exact failing constraint (price, bedroom count, furnishing, geography, or market status) and include its individual URL when useful.
3. Check explicit lifecycle markers such as `fuera del mercado`, `rentada`, `suspendida`, and `despublicada`. A detailed page with photos and contact text is not current if one of these markers is present.
4. Do not generalize a market floor from a handful of near-misses. Say `the verified near-misses I found were priced at…`, not `the market starts at…`.
5. Preserve budget semantics in a zero-result conclusion: distinguish base rent under the cap with unknown maintenance from a confirmed all-in total under the cap.
6. If exact proximity was not measured, use only a qualitative location statement; do not imply that every neighborhood-level candidate is near the destination.

## EasyBroker/Pincali and card-boundary quirks

- EasyBroker marketplace pages may render with Pincali branding and expose a `Ver original` Pincali URL. Treat these as two surfaces for the same underlying listing and deduplicate by EasyBroker ID (`EB-…`), not as independent sources.
- Search/category pages can misassociate a price, title, or bedroom badge with the next card when parsed as flattened text. Parse card boundaries conservatively, then verify every promising ID on its individual page.
- An individual page may remain publicly retrievable after it has been rented, suspended, or unpublished. Prefer the lifecycle marker over the presence of the page.

## Final-answer checklist

- At least the requested number of verified rows, or an explicit reason fewer were possible
- Requested columns exactly, including exact bedrooms and freshness
- Deduplicated across sources and mirrored EasyBroker/Pincali surfaces
- No inferred furnishing or maintenance
- Measured or clearly labeled approximate distance/commute
- Source coverage summary distinguishes direct searches, indexed discovery, blocked/no-candidate sources, and sources contributing rows
- For zero results, representative verified near-misses and their exact failing filters; no unsupported market-wide claim
- Short prioritized shortlist based on commute, building controls, and value when qualifying rows exist
- Scam warning: verify advertiser/ownership, never pay before validating the property and contract
