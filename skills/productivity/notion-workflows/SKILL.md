---
name: notion-workflows
description: "Use when working with Notion from Hermes: API debugging, database queries, relation linking, project databases, and audio/podcast processing records."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [notion, databases, api, relations, projects, podcast]
    related_skills: []
---

# Notion Workflows

## Overview

This umbrella covers Notion API work as a class. Most failures come from database access, property schema mismatches, relation fields without data, or brittle assumptions about page structure. Start with API/database diagnostics, then use the relevant workflow subsection.

## When to Use

- The user asks to query, create, update, or debug Notion pages/databases.
- A Notion database appears disconnected despite relation fields.
- A project database query needs active-project filters or property extraction.
- A podcast/audio workflow stores episode metadata in Notion.
- Notion API access, sharing, token, property, or pagination behavior is unclear.

## Diagnostic Gate

1. Verify `NOTION_API_KEY`/token availability and database/page IDs.
2. Confirm the integration is shared with the page or database.
3. Fetch database schema before writing filters or property names.
4. Log raw API errors and response fragments; do not guess property types.
5. Paginate until complete when the user expects full coverage.

## General Notion API

Use curl or Python against the Notion API for page, database, block, and search operations. Keep payloads explicit and preserve Notion property type names.

## Database Troubleshooting

For access issues, distinguish authentication failure, missing sharing, wrong database ID, archived pages, filter syntax errors, and property name/type mismatches. Build the smallest working query before adding filters.

## Debug and Query

When a user asks for project data, first inspect schemas and sample records, then build filters. Store durable project knowledge outside this skill only if it is stable and not a one-off result.

## Active Projects

For active-project queries, systematically identify status/select fields, date fields, relation fields, and rollups. Report skipped or ambiguous records rather than hiding schema gaps.

## Database Linking

When databases have relation fields but no actual links, map candidate records, propose matching criteria, then update relations in controlled batches. Verify links by re-querying both sides.

## Audio and Podcast Processing Records

For podcast/audio pipelines, expect Notion records to be incomplete. Use fallback mechanisms for missing audio URLs, transcripts, or episode metadata; verify each stage before writing notes or summaries.

## Common Pitfalls

1. Querying a database that has not been shared with the integration.
2. Assuming display names match API property names/types.
3. Forgetting pagination.
4. Updating relations without re-query verification.
5. Treating missing podcast metadata as a hard stop when documented fallbacks exist.

## Verification Checklist

- [ ] Token and sharing verified.
- [ ] Database schema fetched.
- [ ] Filters match actual property types.
- [ ] Pagination handled.
- [ ] Writes verified by readback.
