---
name: kanban-workflows
description: "Use when coordinating Hermes Kanban work: orchestrator decomposition, worker execution rules, lifecycle checks, and anti-patterns for not doing the wrong role's work."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kanban, orchestration, workers, task-routing, hermes]
    related_skills: []
---

# Kanban Workflows

## Overview

This umbrella consolidates Kanban orchestration and worker guidance into one role-aware workflow. The key distinction is role discipline: orchestrators decompose and route; workers execute assigned tasks and report evidence.

## When to Use

- The user asks to run work through a Kanban board or queue.
- You are acting as an orchestrator assigning tasks to workers.
- You are a worker receiving a Kanban task and need lifecycle/pitfall guidance.
- Work requires multiple independent task cards, status transitions, or handoff summaries.

## Orchestrator Responsibilities

1. Decompose work into small cards with clear acceptance criteria.
2. Avoid doing worker tasks yourself unless the workflow explicitly switches roles.
3. Track dependencies and unblock workers with concrete context.
4. Require verifiable outputs: file paths, command output, URLs, IDs, or screenshots.

## Worker Responsibilities

1. Read the assigned card and acceptance criteria.
2. Execute only the scoped task unless escalation is needed.
3. Keep status current and report blockers early.
4. Return evidence, not just a claim of success.

## Lifecycle

Use the injected KANBAN_GUIDANCE as the authoritative live lifecycle when present. This skill adds durable pitfalls and examples; it does not replace system guidance.

## Common Pitfalls

1. Orchestrator temptation: doing the implementation instead of routing it.
2. Worker drift: expanding scope beyond the assigned card.
3. Weak handoffs: reporting success without artifacts.
4. Lost dependencies: assigning downstream work before upstream evidence exists.
5. **`--initial-status blocked` is not a durable human gate by itself.** A gateway dispatcher may promote a newly created card before a typed block record exists. For a batch of human-gated cards, pause dispatch first, create the cards, apply `hermes kanban --board <board> block <id> '<reason>' --kind needs_input`, verify every card is `blocked`, then resume dispatch. Do not assign runnable profiles before the typed block is present.
6. **A DB block does not prove the worker process stopped.** Blocking a `running` card from the CLI can close its run and clear `worker_pid` while the already spawned OS process continues. After any external block/reclaim, inspect the prior run PID or process environment (`HERMES_KANBAN_TASK`, `HERMES_KANBAN_BOARD`), terminate lingering workers, and verify there are zero matching processes before claiming the work is paused.

## Verification Checklist

- [ ] Role identified: orchestrator or worker.
- [ ] Card scope and acceptance criteria are explicit.
- [ ] Status transitions are made in the correct system.
- [ ] Final report includes verifiable evidence.
