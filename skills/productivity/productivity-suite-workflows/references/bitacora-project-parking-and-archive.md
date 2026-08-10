# Bitácora priority parking and project-archive audits

Use this when JT says to delete/deprioritize a learning track, move something to “later,” clean active projects, or asks which completed projects can be archived.

## Park/deactivate vs delete

When the request combines “delete it now” with “move it to later,” treat it as **remove from active commitments while preserving a minimal parked backlog**, not destructive erasure.

1. Search the active sources of truth: `1-Projects/`, pillar `Wiki/` and `Pillar-*.md`, `_decisions.md`, Google Tasks, and system-facing summaries such as `agent.md`/README examples.
2. Edit only references that represent the active commitment. Do not delete unrelated semantic mentions (e.g., “Chinese food,” historical quotations, raw research) merely because they match a keyword.
3. Replace active sequencing language (“second priority,” “current quest”) with an explicit parked rule and reactivation condition, such as “post-Step review.”
4. Remove or postpone corresponding active Tasks. If none exist, say so rather than inventing a deletion.
5. Update durable preference memory/facts when the priority correction is stable.
6. Verify with a narrowed search over active project/area files.

## Project-archive audit

A passed deadline or stale `status: active` is **not proof of completion**. Classify each project:

- **Safe to archive:** dated one-off event clearly occurred/ended, or completion is corroborated by calendar/log/session history.
- **Archive the container, preserve open decisions:** a quarterly/deadline project has expired, but unresolved items must first live in `_decisions.md` or another active project.
- **Park, not complete:** cold-start/someday work with no current commitment.
- **Keep active:** has future deadlines, unresolved deliverables, or active tasks.
- **Needs confirmation:** outcome cannot be established from original sources.

For a question like “Which done projects can I archive?”, return the classified candidates but **do not move files yet** unless JT explicitly asks to archive them. State the evidence and distinguish “completed” from merely “stale.”

## Moving an archived project

After approval:

1. Ensure unresolved decisions/tasks were migrated.
2. Set frontmatter to `status: archived` and add `archived: YYYY-MM-DD`.
3. Move to the appropriate `4-Archives/` location while preserving filename and wikilinks where possible.
4. Remove stale active-project references from pillar pages and recurring briefings.
5. Verify the destination and re-scan `1-Projects/`.

## Starting the replacement priority

When one priority is parked and another becomes active, create a lightweight project note rather than over-planning. Include objective, first three decisions, immediate ≤20-minute next action, open questions, and a Google Task in the closest ONEPISSA list. Label assumptions explicitly when the user has not yet supplied the creative or operational details.
