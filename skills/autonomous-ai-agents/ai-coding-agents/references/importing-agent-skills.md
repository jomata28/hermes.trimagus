# Importing Skills from Claude Code or Other Agent Harnesses

Use this when a user asks to install a named skill they already use elsewhere.

## Core distinction: install versus recreate

Treat “install this skill” as a request for the **actual upstream artifact**, not permission to write an approximation with the same name. A same-name recreation can silently change behavior, dependencies, statefulness, question cadence, or approval gates.

If the exact artifact is unavailable, say so and request one of:

- the source repository/URL;
- the original `SKILL.md` and linked files;
- an export copied to an accessible shared location.

Do not label a reconstruction as installed upstream behavior.

## Workflow

1. Search the current machine for the exact skill name in the relevant harness directories.
2. If the user says it exists only on another/local machine, search public upstream sources by exact name plus `SKILL.md` and the harness name.
3. Identify the canonical author/repository rather than choosing a random fork. Compare candidate files and attribution.
4. Inspect the full package tree for wrappers and dependencies. A tiny entry skill may delegate all behavior to another skill.
5. Preserve upstream frontmatter, invocation policy, behavior, and license. Do not “improve” it during installation unless the user explicitly asks for a fork.
6. Install dependencies before or alongside the wrapper.
7. Remove artifacts from any superseded reconstruction when the canonical package is stateless or has a different layout.
8. Load every installed component with `skill_view` and verify linked files are present.
9. State clearly what was installed, its source, dependencies, and any intentional divergence.

## Wrapper/dependency example

Matt Pocock’s canonical `grill-me` is only a manually invoked wrapper whose body runs `/grilling`. The behavior lives in the separate `grilling` skill: design tree, dependency-aware frontier, rounds, recommendations, fact lookup by the agent, user-owned decisions, and a final shared-understanding gate. Installing only `grill-me` produces an incomplete package.

## Behavioral fidelity checks

Before declaring success, compare:

- one-question cadence versus frontier rounds;
- stateless versus files/decision logs;
- manual-only versus implicit invocation;
- whether recommendations accompany questions;
- whether facts are researched by the agent;
- dependency calls to other skills;
- whether execution is blocked until explicit approval.

## Pitfalls

- Recreating a familiar workflow from memory because the name seems self-explanatory.
- Installing a fork without identifying it as a fork.
- Copying only the wrapper while missing its primitive/dependency.
- Leaving templates or state files from a discarded approximation.
- Adapting Claude-specific tool instructions literally when the destination harness exposes different tools; preserve intent, and document only the minimal compatibility adaptation.
