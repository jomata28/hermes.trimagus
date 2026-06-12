---
name: productivity-api-integrations
description: "Use when automating external productivity/data APIs such as Airtable, Apify, and maps/geocoding services. Class-level umbrella for token setup, curl/Python calls, pagination, exports, and data validation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [productivity, api, integrations, airtable, apify, maps, data]
    related_skills: []
---

# Productivity API Integrations

## Overview

Use this umbrella for API-backed productivity and data services. The common class is: discover credentials, call a REST/CLI endpoint, handle pagination/export formats, validate returned records, and produce a user-ready dataset or update.

## When to Use

- Airtable bases/tables/records, CRUD, filters, upserts, or formulas.
- Apify actors, runs, datasets, tasks, exports, scraping diagnostics, or lead-gen datasets.
- Maps/geocoding/POI/routing/timezone queries using OpenStreetMap/Nominatim/Overpass/OSRM-style services.
- Any similar external productivity API where curl/Python is more reliable than browser clicking.

## Shared Workflow

1. Identify the target service, resource ID, and required credential environment variables.
2. Prefer official API/CLI docs and machine-readable JSON responses.
3. Use environment variables for tokens; never paste secrets into files or summaries.
4. Fetch a small sample first, inspect schema, then page/export the full result.
5. Validate counts, IDs, timestamps, and user-visible fields before reporting success.
6. For write operations, perform dry-run/sample where possible and report exact affected records.

## Airtable Notes

- Use `AIRTABLE_API_KEY` or the configured personal access token.
- Common resources are base ID, table name/table ID, record IDs, fields, `filterByFormula`, `sort`, and `pageSize`/offset pagination.
- For upserts, choose a stable key and verify the returned record IDs.

## Apify Notes

- Use Apify API tokens via environment variables.
- Inspect actors/runs/tasks first, then datasets; missing rows are often run-status, dataset-ID, pagination, or export-format issues.
- Preserve run IDs and dataset IDs in summaries so results can be audited.

## Maps / Geospatial Notes

- Use open-data services with polite rate limits and user-agent strings where required.
- Geocode before route/POI queries; verify coordinates and bounding boxes to avoid wrong-city results.
- Report assumptions such as travel mode, radius, and timezone.

## Demoted Source Packages

Full source packages preserved for detailed service-specific commands and examples:

- `references/airtable-package/`
- `references/apify-package/`
- `references/maps-package/`

Use these for exact endpoint/CLI examples while keeping this umbrella as the discoverable entry point.

## Common Pitfalls

1. **Using browser scraping for an API task.** Prefer API/CLI calls unless auth requires browser setup.
2. **Ignoring pagination.** Always check continuation tokens/offsets.
3. **Trusting names without IDs.** Persist service IDs in the answer.
4. **Leaking credentials.** Redact tokens and avoid writing them to skill references.

## Verification Checklist

- [ ] Credential and resource prerequisites are known.
- [ ] A sample response/schema was inspected before bulk operations.
- [ ] Pagination/export completeness was checked.
- [ ] Final answer includes stable IDs/counts and any assumptions.
