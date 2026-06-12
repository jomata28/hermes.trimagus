# Foundation Atlas + Apify session note (2026-05)

Context:
- User is validating a money project around `foundationatlas.cloud`.
- Domain is in Hostinger and resolved to a parked Hostinger page at time of inspection.
- Strategy discussed: national foundation-repair contractor directory + lead-routing system, starting with Texas/Houston validation, then upselling bilingual AI receptionist / missed-lead recovery.
- User said they had already scraped foundation contractors from across the US.

Apify connection outcome:
- User provided an Apify API token in chat; do not store or repeat raw token.
- Token verified successfully with `/v2/users/me`.
- Visible account at the time: username `multicoloured_toy`, email `jomata97@gmail.com`.
- Visible actor inventory included `crawler-google-places` / Google Maps Scraper.
- API checks returned empty for:
  - `/datasets?limit=100&desc=1`
  - `/datasets?limit=100&unnamed=true&desc=1`
  - `/actor-runs?limit=100&desc=1`
  - `/actor-tasks?limit=50&desc=1`
  - key-value stores, request queues, schedules, webhooks

Conclusion:
- The token worked, but the foundation scrape was not visible under that account/token.
- Most likely causes: different Apify account/workspace, dataset deleted/expired, or data exported elsewhere.

Recommended next ask:
- Ask for any of: Apify dataset URL, dataset ID, run URL, or exported CSV/Excel/Google Sheet.
- If user is in Console, have them check Storage → Datasets, Actors → Runs, Google Maps Scraper → Runs, and any workspace/account switcher.

Dataset handling plan once found:
1. Pull sample rows (`limit=5`) to infer schema.
2. Export full clean CSV/JSON.
3. Normalize fields: name, category, city, state, website, phone, email/contact, maps URL, rating, reviews, service keywords.
4. Filter first validation segment to Houston/Texas foundation/concrete companies.
5. Score: strong reputation + weak digital intake + clear contact info + local/operator vibe.
6. Produce first 50 outreach targets and personalized messages for Foundation Atlas contractor lead-routing + missed-call recovery offer.
