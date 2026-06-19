---
name: apify
category: productivity
description: Use Apify API/Console to inspect actors, runs, datasets, tasks, and exported scrape data; diagnose missing scraper results and prepare lead-gen datasets.
version: 1.0.0
---

# Apify

Use this skill when the user wants to connect Apify, inspect scraper runs/datasets, retrieve exported data, or use Apify as a lead-generation data source.

## Core workflow

1. **Authenticate with an API token**
   - Prefer an environment variable for commands:
     ```bash
     export APIFY_TOKEN=REDACTED_IN_BACKUP
     ```
   - Do not persist or echo the raw token in notes, skills, or final summaries.
   - Verify token:
     ```bash
     curl -s -H "Authorization: Bearer $APIFY_TOKEN" \
       https://api.apify.com/v2/users/me | jq '.data | {id, username, email}'
     ```

2. **Inventory available Apify assets**
   ```bash
   BASE=https://api.apify.com/v2
   curl -s -H "Authorization: Bearer $APIFY_TOKEN" "$BASE/actors?limit=REDACTED_IN_BACKUP
   curl -s -H "Authorization: Bearer $APIFY_TOKEN" "$BASE/actor-tasks?limit=REDACTED_IN_BACKUP
   curl -s -H "Authorization: Bearer $APIFY_TOKEN" "$BASE/actor-runs?limit=REDACTED_IN_BACKUP
   curl -s -H "Authorization: Bearer $APIFY_TOKEN" "$BASE/datasets?limit=REDACTED_IN_BACKUP
   ```

3. **Inspect a dataset**
   ```bash
   DATASET_ID=...
   curl -s -H "Authorization: Bearer $APIFY_TOKEN" \
     "https://api.apify.com/v2/datasets/$DATASET_ID/items?format=json&clean=true&limit=5" | jq
   curl -L -H "Authorization: Bearer $APIFY_TOKEN" \
     "https://api.apify.com/v2/datasets/$DATASET_ID/items?format=csv&clean=true" \
     -o apify-dataset.csv
   ```

4. **If the user gives a Console URL**
   - Dataset URL usually contains `/storage/datasets/<DATASET_ID>`.
   - Run URL usually contains `/actors/runs/<RUN_ID>` or an actor-specific run page. Fetch run details, then inspect `defaultDatasetId`.

## Missing-data diagnostic checklist

If a token works but `datasets`, `actor-runs`, and `actor-tasks` are empty:

- The scrape may have been run under a different Apify account.
- The user may be in a different Apify workspace/team than the token.
- The dataset may have expired, been deleted, or been exported elsewhere.
- The data may live outside Apify now, e.g. CSV, Excel, Google Sheet, or Drive.
- Ask the user for the dataset ID, dataset URL, run URL, or exported file.

## Lead-generation scrape analysis

For contractor/local-services datasets, normalize and score rows before outreach.

Useful fields:
- business name
- category/services
- city/state/ZIP/service area
- website
- phone
- email/contact URL
- Google Maps URL/place ID
- rating and review count
- address
- opening hours
- source query

Prioritize prospects with:
- good rating/reviews but weak website/intake
- clear phone number and website/contact path
- local owner-operated businesses
- enough job value to justify monthly lead/intake service

Avoid first-pass outreach to:
- national chains/franchises with corporate marketing
- dead/no-contact records
- businesses with highly polished funnels unless a clear missed-call/Spanish intake gap exists

## References

- `references/foundation-atlas-apify-2026-05.md` — session note: Foundation Atlas domain, Apify token validation pattern, and missing-dataset diagnostic observed for Jose's contractor scrape.
