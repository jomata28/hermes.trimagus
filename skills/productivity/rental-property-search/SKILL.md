---
name: rental-property-search
description: Search, verify, deduplicate, and rank residential rental listings across portals, authenticated marketplaces, and agencies using strict housing requirements.
version: 1.0.0
metadata:
  hermes:
    tags: [rentals, apartments, real-estate, housing, due-diligence, commute]
    category: productivity
---

# Rental Property Search

Use this for apartment/house searches where the user needs current individual listings rather than neighborhood-level advice.

## Core rule

A shortlist entry is valid only when its **individual listing page** confirms every hard requirement. Search cards, snippets, photos, portal filters, and generated summaries are leads—not proof.

## Workflow

1. **Normalize requirements**
   - Total monthly ceiling, not merely advertised rent.
   - Exact bedroom count and whether studies/service rooms count.
   - Furnished, partially furnished, or unfurnished.
   - Target destination and acceptable commute.
   - Move-in timing, lease duration, occupants, pets, parking, guarantor/póliza constraints.
   - If some details are missing, provide an initial shortlist rather than blocking, but label assumptions.

2. **Build the geographic search set**
   - Search the target neighborhood and nearby safe areas with practical routes.
   - Run separate portal queries for each neighborhood and common spelling/slug variant.
   - Do not conclude that a neighborhood has no inventory from a general city-wide first page; ranking often overrepresents premium districts.

3. **Search multiple surfaces**
   - Public portal pages and individual agency pages.
   - Authenticated Marketplace/session when the user volunteers to log in.
   - Text-rendered/indexed pages only for lead discovery; verify the individual page afterward.
   - If Cloudflare/CAPTCHA blocks access, use the human-in-the-loop noVNC workflow rather than asking for credentials.
   - When the request specifies result-page ranges or sort orders, keep an explicit coverage ledger by portal, property type, sort mode, and page number. Never report pages as searched when a challenge page, redirect, or block prevented the actual result inventory from loading.
   - Search-engine indexes may recover stable listing URLs and IDs during portal blocking, but they do not prove page placement, current availability, maintenance, furnishing, or exact bedroom count. Treat these strictly as unverified leads.

4. **Verify every finalist**
   Capture:
   - Stable individual URL and listing ID.
   - Advertised rent, maintenance, mandatory monthly services, and known move-in fees.
   - Exact bedrooms/bathrooms/area.
   - Furnishing evidence from explicit listing text.
   - Address or best available location.
   - Publication freshness and current page availability.
   - Security/access, parking, roomie/student acceptance, and guarantor requirements.
   - Distinguish `portal-active` from `advertiser-confirmed active`: a live contact button proves only that the portal page accepts inquiries. Do not call a listing simply `vigente` without recent advertiser confirmation.
   - If a result card supplies a hard fact omitted by the individual page (for example, bedroom count or `amueblado`), label it an unverified lead rather than a finalist.

5. **Deduplicate**
   Match by building/address, photos, area, floor plan, price, broker text, and phone/contact. Marketplace often contains many copies from different agents.

6. **Calculate commute consistently**
   - Geocode the disclosed address or neighborhood centroid.
   - Use one routing method for all candidates.
   - Label free-flow estimates as such and provide a cautious peak-hour range.
   - Penalize routes dependent on a single congested corridor or unsafe late-night transfers.

7. **Rank with hard filters first**
   - Tier A: satisfies all hard requirements.
   - Tier B: one explicitly identified compromise.
   - Do not pad a requested list with poor matches. Say when only one or two valid options exist.

## Furnishing verification

- `Cocina equipada`, appliances, closets, blinds, or furniture visible in photos do **not** prove the property is furnished.
- Require affirmative text such as `amueblado`, `totalmente amueblado`, or an inventory of included furniture.
- Search the whole description for negations: `sin muebles`, `no amueblado`, `fotos ilustrativas`, `muebles generados con IA`, or `posibilidad de amueblar`.
- `Parcialmente amueblado` is a compromise and must be labeled.
- For shared occupants, verify a bed and privacy for each real bedroom; reject `2 recámaras + estudio` unless the user explicitly accepts it.

## Pricing discipline

- Distinguish rent from total monthly cost.
- If maintenance fields conflict with description text, show both possible totals and require written confirmation.
- Never mistake sale price, maintenance, deposit, nightly rate, or a malformed Marketplace price for monthly rent.
- Airbnb/short-term rentals need a real date-specific total; do not extrapolate from partial stays.

## Visual-quality discipline

- Assess aesthetics only from accessible photos.
- Separate objective observations (light, apparent condition, finishes, furniture) from taste judgments.
- One exterior photo cannot establish interior quality.
- Watch for AI-staged furniture and listings that explicitly exclude photographed furnishings.

## Communication and delivery format

- Correct prior mistakes directly. If shown candidates lacked a hard requirement, say so rather than quietly reframing them.
- Keep links prominent and write the full raw URL when the user wants to open or forward it in WhatsApp; do not hide it behind Markdown link text.
- **Honor message granularity literally.** If the user asks for “one message per property” or “mensajes separados,” send exactly **one property in the current assistant message**, then wait for the user’s acknowledgment before sending the next. Dividers, headings, or multiple blocks inside one assistant response are not separate messages.
- Each single-property message should be self-contained: property/area, known monthly total, furnishing evidence, real-bedroom status, commute caveat, direct raw URL, and one short confirmation question for the advertiser. Do not refer to “the previous option.”
- If the user asks only for the next link, provide that property and raw URL without reprinting the entire shortlist.
- Explicitly state the compromise on every Tier B option. Never mix unfurnished or partially furnished negotiation candidates into a furnished shortlist without a conspicuous label.
- When the user changes budget or geography, rerun neighborhood-specific searches rather than merely re-ranking stale candidates.
- When the user rejects the current shortlist, deduplicate against everything already shown and return only genuinely new candidates; do not recycle rejected listings to fill a requested count.

## Safety

- Never send a deposit before viewing/video verification, identity/authority checks, and contract review.
- Confirm maintenance, utilities, inventory, lease term, deposit, póliza/aval, and total move-in cost in writing.
- Treat unusually low prices and hidden-address listings as higher-risk leads.

## References

- See `references/portal-verification-patterns.md` for portal-specific extraction, authenticated-browser, and anti-bot lessons.
- See `references/mexico-portal-discovery-and-verification.md` for Propiedades.com, EasyBroker/Pincali deduplication, text-mirror fallback, exact requirements extraction, and precise availability labels.
