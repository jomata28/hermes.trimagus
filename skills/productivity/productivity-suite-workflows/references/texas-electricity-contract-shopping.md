# Texas electricity contract shopping from Gmail

Use when JT asks about Gexa/Gexa-like annual electricity renewals, expiring contracts, or websites that find cheaper electricity deals.

## Goal

Find the best practical electricity plan for JT's Houston apartment without falling for usage-credit traps. Source facts from Gmail notices + live marketplace/API data, then give a phone-executable switch checklist.

## Workflow

1. **Read Gmail first** — search for provider emails and contract notices:
   - `from:gexaemail.com ("Contract Expiration Notice" OR "plan expires" OR "current plan is ending" OR "energy plan requires attention") newer_than:90d`
   - Broaden if the user mishears provider names: `Gexa` may be heard as “Hexa”.
2. **Extract PDFs/attachments** and run `pdftotext` to confirm:
   - provider/account suffix only if needed, service address/ZIP, ESIID if relevant
   - exact expiration date
   - no-ETF switch window (usually 14 days before expiration)
   - early termination fee
   - rollover/variable plan EFL and price at 500/1000/2000 kWh
3. **Estimate actual usage from Gmail snapshots** before comparing plans. Gexa snapshots expose lines like:
   - `Est. Total (543 kWh): $124.08`
   - `Cost so far $116.84 520 kWh`
   For JT, recent apartment usage has been around 425–543 kWh; treat low-usage sensitivity as important.
4. **Compare plans using live sources.** The ComparePower SPA exposes useful APIs:
   - TDU lookup: `https://pricing.api.comparepower.com/api/tdsps?zip_code=77004`
   - Current plans: `https://pricing.api.comparepower.com/api/plans/current?tdsp_duns=957877905`
   - Plan detail sensitivity: `https://pricing.api.comparepower.com/api/plans/<plan_id>?display_usage=<kWh>`
   Use headers with `Origin: https://orders.comparepower.com` and `Referer: https://orders.comparepower.com/`.
5. **Do sensitivity analysis**, not only advertised 500/1000/2000 rates. Test likely usage values around the user's history: 425, 480, 499, 500, 520, 543, 600, 1000 kWh.
6. **Flag bill-credit traps.** Plans with credits at exactly/above 500 kWh can look cheapest at 500 but become expensive at 425–499. If the user often falls below the threshold, prefer no-minimum/no-gimmick plans even if the exact 500-kWh rate is slightly higher.
7. **Evaluate autopilot services** separately:
   - Energy Ogre: paid membership (~$12/mo or annual) and aligned incentives because they charge the user rather than provider commissions; useful for autopilot.
   - Arbor/Rocket Money: can help, but may receive supplier compensation and may not access every plan; don't assume lowest.

## Recommendation pattern

Present:

- Current contract facts: provider, expiration, no-ETF window, ETF, rollover risk.
- Actual usage pattern from Gmail.
- Top plans table with dollar cost at realistic kWh values, not just cents/kWh.
- Recommendation and avoid list.
- Action date: do not switch before no-ETF window unless savings exceed ETF.

## Pitfalls

- Do not trust the provider renewal email's “as low as” rate without checking the EFL and usage threshold.
- Do not recommend a usage-credit plan if the user's historical usage often dips below the credit threshold.
- Do not conclude a site is unusable just because Google/search blocks the VPS. Try direct official/marketplace APIs and page bundles first.
- Do not print full account numbers, tracking links, tokens, or personal data unnecessarily; account suffix and service ZIP are usually enough.
