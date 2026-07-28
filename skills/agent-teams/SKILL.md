---
name: agent-teams
description: JT's playbook for spinning up multi-agent teams via delegate_task — a Research Team (fan out to gather + synthesize) and an Execution Team (fan out to build/do in parallel). Invoke from Telegram (research team / execution team); Hermes orchestrates the children and returns one synthesized result.
version: 1.0.1
author: Hermes Agent
category: productivity
metadata:
  hermes:
    tags: [agents, delegation, orchestration, research-team, execution-team, parallel]
---

# Agent Teams

Turn a big ask into a coordinated team of sub-agents using the built-in
`delegate_task` tool. Hermes is the orchestrator: it decomposes the goal, fans
work out to children (up to `delegation.max_concurrent_children`, currently 3),
then synthesizes one clean answer for JT. He should never see raw child dumps —
only the merged result.

## The `delegate_task` tool
- **Single:** `delegate_task(goal, context?, toolsets?, role?)`
- **Batch (parallel):** `delegate_task(tasks=[{goal, context, toolsets, role}, ...])`
- `role: 'leaf'` (default) = worker that can't sub-delegate; `role: 'orchestrator'`
  = can spawn its own workers (bounded by `delegation.max_spawn_depth`).
- Returns JSON with a `results` array, one entry per task.

## Team 1 — 🔎 Research Team
**Invoke:** "research team: <question>"  (e.g. "research team: IR vs vascular surgery
match trends + lifestyle, last 3 cycles")
**Pattern (fan-out → synthesize):**
1. Decompose the question into 2–3 independent angles (don't overlap them).
2. `delegate_task(tasks=[...])` — one leaf per angle, each with `toolsets: ["web"]`
   (add `research` tools for papers). Give each a tight, self-contained `goal`.
3. When results return, Hermes dedupes, resolves contradictions, and writes ONE
   synthesis. Cite sources. Flag disagreements between children instead of hiding them.
4. Offer to save the synthesis to the right vault pillar (e.g. Negocio/Wiki for
   career research, Intellectual/Wiki for study topics).

## Team 2 — 🛠️ Execution Team
**Invoke:** "execution team: <multi-part job>"  (e.g. "execution team: draft the
FoundationAtlas landing copy, outline the cold-email sequence, and list 20 target
contractors")
**Pattern (parallel independent builds):**
1. Split into parts that don't depend on each other's output.
2. `delegate_task(tasks=[...])` — one leaf per part, with the `toolsets` each needs
   (`file` to write vault notes, `web` to look things up, `terminal` for scripts).
3. Collect the parts, assemble into one deliverable, and propose where it lands
   (vault path, doc, or draft). Surface anything a child couldn't finish.

## When NOT to use a team
- A single-step question → just answer it. Teams add latency + token cost.
- Steps that depend on each other in sequence → do them inline, not as parallel children.
Rule of thumb: fan out only when the parts are genuinely independent.

## Orchestrator etiquette
- Tell JT briefly what the team is doing ("spinning up 3 researchers on match data…"),
  then go quiet until you have the synthesized result.
- Keep the final answer Telegram-sized with an option to expand.
- Respect the concurrency cap; queue extra parts rather than exceeding it.
- Children inherit the warm-but-efficient voice for anything user-facing.

## Herdr cockpit (terminal multiplexer)
For pane-based agents (Claude Code / Hermes CLI side-by-side in workspaces per
project, Hermes reading and directing them via the Herdr socket API), see
`references/herdr-multiplexer.md`.

## Config knobs (in config.yaml → delegation)
- `max_concurrent_children` (3), `max_spawn_depth`, `child_timeout_seconds` (600),
  `model`/`provider` (route children to a cheaper model to save cost),
  `reasoning_effort` (child thinking depth). Orchestrator is already enabled.
