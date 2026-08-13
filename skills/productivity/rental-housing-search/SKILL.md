---
name: rental-housing-search
description: Find, verify, deduplicate, and rank residential rental listings across portals, authenticated marketplaces, and short-term platforms; use when users need a current apartment or house shortlist.
version: 1.0.0
metadata:
  hermes:
    tags: [housing, rentals, apartments, marketplace, due-diligence]
---

# Rental Housing Search

Build a decision-ready shortlist of **individual, currently retrievable listings**—not a list of portal search pages.

## Intake and defaults

Capture: destination/anchor, total monthly budget, true bedroom count, furnished status, move-in date, lease length, parking/pets, guarantor or policy constraints, and who will occupy it. If some details are missing, search broadly first and ask without blocking the initial shortlist.

Translate preferences into hard and soft filters:

- **Hard:** total budget, genuine bedroom count, furnished/unfurnished, acceptable geographic radius.
- **Soft:** appearance/modernity, amenities, walkability, security, commute, bathrooms.
- When the user changes a qualitative preference such as “nicer,” immediately redefine ranking and rerun the search; do not keep returning technically compliant but visibly poor options.

## Search sequence

1. Search public listing-level pages across multiple portals and agencies.
2. Use portal indexes only to discover candidate URLs; verify each candidate on its individual page.
3. If portals block automation, try indexed/rendered pages, XML sitemaps, structured metadata (`__NEXT_DATA__`, JSON-LD), and public agency mirrors without claiming blocked inventory was reviewed. A portal landing page, CAPTCHA, 403, HTTP 202 challenge/empty body, account-verification redirect, malformed guessed URL, irrelevant search-engine response, or sitemap slug counts only as an **attempted/discovered source**—not as reviewed inventory.
   - Keep a per-source coverage ledger with three distinct states: **attempted**, **candidate URLs discovered**, and **individual listings verified**. In the final report, never collapse these into “reviewed” or imply zero inventory on a source when listing-level access was unavailable.
   - For EasyBroker/Pincali, use `references/easybroker-pincali-sitemap-discovery.md`: parse all sitemap shards dynamically, filter candidate slugs before detail requests, and treat slugs only as discovery metadata.
   - Beware repurposed URLs: a slug may say `renta` or `amueblada` while the current page is a sale or has different facts. Current listing-level fields override the slug.
   - Do not regex the entire HTML for price, bedrooms, or maintenance when recommendation cards are present; isolate the primary listing object/section first.
4. For Next.js listing sites, inspect `__NEXT_DATA__` on every pagination page and filter the embedded publication objects by structured bedroom count, total price, maintenance, furnished attribute, status, and canonical slug. Use prose to detect contradictions and furniture negation; use photos only for visual corroboration. See `references/structured-listing-extraction.md`.
5. When the user offers help, use the persistent noVNC desktop so they can complete login/CAPTCHA privately; then operate the authenticated browser. Follow `vps-desktop-sessions` for its two-stage access and credential handling.
5. For authenticated Marketplace searches, set the **map center/radius around the real destination** before trusting keyword results. A city-center radius can silently exclude the target neighborhood while returning irrelevant citywide matches.
6. Run separate neighborhood queries rather than one long phrase; collect item URLs, deduplicate, then inspect descriptions individually.

## Verification rules

For every candidate, verify:

- individual URL still loads;
- rent and whether maintenance is included;
- exactly the required number of real bedrooms;
- furnished status stated positively in the description;
- neighborhood/location and approximate commute;
- bathrooms, parking, security, amenities, lease requirements;
- publication freshness or at least date checked.

Never equate:

- “cocina equipada” with **furnished**;
- “2 bedrooms + study/family room” with **3 real bedrooms**;
- furniture visible in photos with included furniture;
- a search-card filter match with listing-level confirmation;
- “live page” with landlord-confirmed availability.

Explicitly search descriptions for negation: `sin muebles`, `no amueblado`, `muebles no incluidos`, `fotos referenciales`. Some ads show staged or AI-generated furniture while renting empty.

## Visual-quality ranking

When “nice/modern” matters, inspect photos rather than relying on adjectives. Assess:

- daylight, window area, finishes, kitchen/bath condition;
- furniture coherence and bedroom readiness;
- signs of manipulated/staged images;
- building common areas, controlled access, and pickup/drop-off practicality.

Rank by hard-filter compliance first, then commute/security, total known cost, visual quality, and entry friction.

## Pricing and alternatives

- Divide total rent per occupant only after calculating the known total, including maintenance where available.
- Do not convert short stays into monthly prices unless the platform provides a real total for exact dates.
- If furnished inventory is scarce but attractive unfurnished units have budget headroom, present **negotiating furniture inclusion** as a separate strategy—not as current compliance. Quantify monthly headroom and ask for beds, refrigerator, dining table, and basic living-room furniture in a yearly lease.

## Commute and zone screening

1. Geocode the exact destination entrance and each listing's best defensible location. If screening neighborhoods before collecting listings, route from a disclosed neighborhood centroid and keep those results separate from listing-level commutes.
2. Use a routing engine only for successfully geocoded origins. Label its output `free-flow/modelled` unless the source explicitly incorporates traffic.
3. Do not call a generic multiplier a calculated **peak commute**. Only use `peak` when a traffic-aware map supplies it for a stated departure or arrival window. Otherwise provide a clearly labeled planning scenario, disclose the multiplier or assumption, and avoid false precision.
4. If a listing hides its exact location, use a street/neighborhood range and state the location precision. A centroid result does not represent every property in the neighborhood.
5. Rank transport resilience alongside nominal drive time: alternate road routes, bottlenecks, last-mile public transport, late-shift service, pickup/drop-off practicality, walkability, and whether the area effectively requires a car. A shorter theoretical drive may be worse for car-free occupants than a slightly farther but better-connected area.
6. For hospital, school, or shift-work searches, distinguish daytime mobility from late-night return risk and recommend testing the route in both peak and nighttime conditions.

## Output

Use a compact table with: rent, known total, neighborhood, bedrooms, furnished evidence, commute, freshness, and direct link. Separate:

1. fully verified matches;
2. promising candidates needing one explicit confirmation;
3. rejected/compromise options, with the failed criterion.

If there are no strict matches, say so plainly, then give the nearest verified rejects and their failed criteria. Report source coverage in a separate compact ledger using precise labels such as `listing pages verified`, `candidates discovered only`, `login/CAPTCHA required`, or `blocked at listing level`. Do not use broad wording such as “reviewed inventory” for sources reached only through search pages, sitemaps, snippets, or blocked URLs. Counts of sitemap shards, slugs, or HTML artifacts are methodology notes—not evidence that those listings were individually reviewed.

Do not expose internal filesystem paths or audit artifacts in the user-facing answer unless the user asks for them or they are an actual requested deliverable.

Provide a short contact script that asks availability, total including maintenance, real-bedroom layout, included furniture, occupant acceptance, guarantor/policy requirements, and viewing.

## Safety

Warn against deposits before viewing/video verification, confirming the advertiser’s authority, and reviewing the contract. Flag suspiciously low prices and duplicated ads. Never expose login credentials, cookies, contact tokens, or hidden personal information.

## Reference

- See `references/marketplace-authenticated-search.md` for the reusable authenticated-Marketplace extraction and verification pattern learned during a Santa Fe housing search.
