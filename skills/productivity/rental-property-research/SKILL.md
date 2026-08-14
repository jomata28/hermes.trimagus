---
name: rental-property-research
description: Research and verify residential rental listings across public, bot-protected, and authenticated property portals; deduplicate, validate hard constraints, assess commute and listing quality, and maintain a decision-ready shortlist.
---

# Rental Property Research

Use this skill for apartment or house searches where availability, furnishing, room count, budget, safety, commute, and portal access all matter.

## Core rule: hard constraints are evidence gates

A listing enters the strict shortlist only when its individual live page supports every hard requirement. Distinguish clearly among:

- **Confirmed:** explicitly stated on the individual listing.
- **Candidate:** plausible but one or more facts need confirmation.
- **Excluded:** violates a hard requirement.

Never treat any of the following as equivalent:

- “Cocina equipada” ≠ furnished.
- Furniture visible in photos ≠ rented furnished.
- “2 bedrooms + study” ≠ 3 true bedrooms.
- A search-card filter hit ≠ verified listing detail.
- Base rent within budget ≠ total monthly cost within budget.
- “Near the area” ≠ practical commute to the exact destination.

When the user requires furnished housing, do not present attractive unfurnished properties as finalists. If useful, put them in a separate **negotiation candidates** section labeled explicitly as unfurnished.

## Workflow

1. **Normalize requirements**
   - Exact destination/campus.
   - Total monthly ceiling, not per-person unless requested.
   - Exact bedroom count and definition of a real bedroom.
   - Furnished required/preferred/optional.
   - Move-in date, lease length, occupants, pets, parking.
   - Guarantor, obligado solidario, or póliza constraints.
   - Safety and transport mode, especially late-night trips.

2. **Search broadly, verify narrowly**
   - Search portal indices, search engines, authenticated portals, agencies, and medium-term rental sites.
   - Open individual detail pages for every finalist.
   - Extract price, maintenance, furnishing language, bedrooms, bathrooms, size, address/area, listing age, availability, security, parking, contact, and URL.
   - Exclude stale/404 pages and cards whose details conflict with the listing page.

3. **Handle protected portals with human-in-the-loop login**
   - Use the persistent VPS browser session when public/headless access hits login or CAPTCHA.
   - The user enters credentials and solves CAPTCHA; never ask them to paste account passwords.
   - Preserve the authenticated browser profile and connect automation to the live session when possible.
   - After access is unlocked, extract index links, then visit each individual page and read the complete details.
   - Do not claim a portal has no inventory merely because its unauthenticated surface was blocked.

4. **Deduplicate**
   - Match address/development, area, price, room count, photos, description, and broker contact.
   - Treat reposts by different agents as one property.
   - Prefer the freshest and most complete source; retain alternate links only as corroboration.

5. **Compute total cost**
   - Total = rent + maintenance + mandatory recurring fees.
   - Flag contradictory portal fields versus description (for example, a maintenance field showing a charge while prose says included).
   - Keep the candidate if both interpretations fit budget, but require written confirmation.

6. **Assess commute and neighborhood fit**
   - Route to the exact workplace/campus, not just the neighborhood name.
   - Give free-flow estimate and a labeled peak-hour range; never present free-flow as typical.
   - Consider whether the route depends on a car/Uber, has bottleneck roads, or is unsuitable after night shifts.
   - A farther but connected neighborhood may be better for students without cars than a geographically closer hillside area.

7. **Assess visual quality honestly**
   - Review multiple interior photos: living room, kitchen, each bedroom, bathrooms, building entrance, and surroundings.
   - One exterior photo is insufficient to call a property attractive inside.
   - Explicitly flag AI-staged furniture, renders, stock photos, or photos that do not prove furnishings are included.
   - Use neutral labels such as modern, traditional but maintained, dated, bright, cramped, or insufficient visual evidence.

8. **Deliver a decision-ready shortlist**
   - Lead with the best strict matches.
   - Include direct links and a compact comparison table unless the user asks for message-by-message delivery.
   - Separate strict matches, pending-confirmation candidates, and excluded/negotiation-only listings.
   - State the checked date and “confirm availability.”
   - Provide a copyable message asking about availability, total cost, furniture in each bedroom, lease requirements, and video tour.

### WhatsApp/Telegram message-by-message mode

When the user asks for **“un mensaje por inmueble,” “uno por uno,” or “mensajes separados”**, do not place multiple properties in one assistant response separated by headings or horizontal rules. Send exactly **one property per assistant message**, then wait for the user’s acknowledgement before sending the next.

Each message must be self-contained and include:

- Property/zone and total monthly cost.
- Furnishing status and whether all required bedrooms are real/usable.
- Maintenance included or explicitly pending confirmation.
- Approximate commute with free-flow clearly labeled.
- Full plain-text URL (`https://...`) so WhatsApp makes it clickable; do not hide it behind Markdown.
- One concise caveat or question for the advertiser.

Do not repeat already rejected listings merely to fill a requested count. If no new strict match exists, say so directly and continue searching rather than recycling the shortlist.

## Persistence and monitoring

For time-sensitive searches, create a finite alert-only recurring search only with user authorization. The recurring prompt must be self-contained, list known listings for deduplication, and remain silent when there are no genuinely new matches. Update its geography and hard constraints when the user changes the brief.

## Common pitfalls

- Do not repeatedly ask for constraints after the user has already answered them.
- Do not pad the shortlist with noncompliant properties just to reach a target count.
- Do not silently relax furnishing, bedroom count, budget, or destination.
- Do not call an option “beautiful” based only on listing copy or one exterior image.
- Do not confuse portal metadata with description truth; report contradictions.
- Do not overfocus on premium districts when adjacent safe corridors offer better budget/commute tradeoffs.
- Do not claim Airbnb monthly affordability without a real full-stay total; unavailable dates or nightly snippets are not evidence.

## Supporting reference

See `references/portal-verification-playbook.md` for authenticated portal extraction, evidence standards, and a reusable verification checklist.
