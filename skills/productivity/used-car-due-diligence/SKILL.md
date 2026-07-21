---
name: used-car-due-diligence
description: "Evaluate used/semi-new vehicle purchases: listing analysis, market comps, legal/document checks, recalls, title/registration/tenencia, mechanical checklist, and buy/negotiate/avoid recommendation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vehicles, used-cars, due-diligence, market-comps, mexico, kavak, registration]
    related_skills: [research-workflows, navigate-bot-protected-sites]
---

# Used-Car Due Diligence

## When to use

Use when JT asks whether to buy a used/semi-new car, sends a car listing/photo, asks to check plates/VIN/title/tenencia/market price, or wants a buy/negotiate/avoid decision.

## Workflow

1. **Extract hard facts first**
   - From photos/listing: make, model, year, trim, mileage, price, plate, state, VIN/NIV, seller/dealer, visible condition.
   - If VIN/NIV is partial/uncertain, state uncertainty clearly. A VIN/NIV must have 17 characters.

1a. **For post-purchase trámites, choose the registration route first**
   - If the buyer keeps the current state registration: use that state's cambio de propietario + reemplacamiento rules and domicile requirement.
   - If the buyer lives in another state: use alta de placas in the buyer's state plus whatever baja/return/resolution of prior plates is required.
   - For CDMX buyer + Edomex plates, do not phrase it as “changing Edomex plates in CDMX”; it is usually CDMX alta de placas for a used vehicle from another entity. See `references/mexico-registration-transfer-notes.md`.

2. **Validate identity/legal fit**
   - Plate must match vehicle make/model/year in the relevant official registry.
   - VIN/NIV must match listing, windshield/door labels, factura, tarjeta de circulación, and any registry output.
   - For Mexico: check/ask for REPUVE, tenencia/refrendo, multas/infracciones, verificación, factura/endosos, and no lien/gravamen if available.

3. **Market-price comparison**
   - Compare same year/trim/mileage if possible; otherwise bracket by nearby years/trim.
   - Separate dealer/platform premium (Kavak, agency) from private-sale price.
   - Produce a price ladder: good deal / reasonable / high / avoid.

4. **Mechanical/risk checks**
   - Search recalls/campaigns by model year and, if possible, VIN.
   - Ask for service history, inspection report, OBD scan, test drive, tire/brake condition, accident/flood signs, warranty and return policy.

5. **Decision output**
   - End with one of: **buy**, **buy if**, **negotiate**, **avoid**, or **need more info**.
   - Include exact missing info and a message JT can send to seller/dealer.

## Mexico/Edomex plate-tenencia pattern

For Edomex tenencia/refrendo, use the official portal and submit the plate **without hyphens and uppercase**. If a photo-read plate returns a different car, consider OCR/letter confusion before declaring a red flag; ask/try visually similar letters (e.g., H vs W). See `references/mexico-edomex-vehicle-checks.md`.

## Kavak/platform-specific notes

Kavak reduces private-party fraud risk but does **not** eliminate overpricing, registration/adeudo issues, recalls, warranty exclusions, or imperfect reconditioning. If Kavak blocks scraping, ask JT for screenshots of price/km/VIN/warranty and continue with external comps.

## Pitfalls

- Do not declare a plate mismatch from a blurry photo without testing plausible OCR alternatives.
- Do not treat a dealer/platform inspection as a substitute for checking recalls, adeudos, REPUVE, and warranty terms.
- Do not infer a final recommendation without price, mileage, year/trim, and legal checks.
- Avoid generic checklist dumps; tie the checklist to the specific vehicle and the user's current decision.
- For handouts/PDFs, keep only the requested procedural content; omit seller negotiation context unless asked.
- If the user says not to change the artifact yet, report the researched facts only and wait before editing/regenerating.
- When quoting government trámite costs, prefer official agency pages, direct links, and screenshots of the visible price section; if a portal is accordion-based, open/capture the relevant `Costo` panel.
- Do not include ISAVAU in a simple transfer/plates handout unless directly requested; mention it separately only when it affects cost.

## Verification checklist

- [ ] Vehicle identity extracted and uncertainty labeled.
- [ ] Plate/VIN consistency checked or explicitly requested.
- [ ] Market comps/range provided.
- [ ] Recalls/campaigns checked for model year.
- [ ] Legal/document checklist provided.
- [ ] Clear buy/negotiate/avoid recommendation given.
