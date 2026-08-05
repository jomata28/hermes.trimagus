---
name: software-development-workflows
description: "Use when planning, spiking, debugging, TDD, pre-commit review, or exploratory QA are part of a software delivery workflow. Class-level umbrella for execution discipline from idea to verification."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [software-development, planning, tdd, debugging, code-review, qa, workflow]
    related_skills: []
---

# Software Development Workflows

## Overview

Use this umbrella for class-level software delivery practices: plan before broad changes, run throwaway spikes to reduce uncertainty, debug from evidence, use TDD for behavioral changes, run pre-commit review before handing off, and dogfood web applications with evidence.

## When to Use

- The user asks to build, refactor, fix, investigate, verify, QA, or review software.
- The task involves more than a trivial one-file edit or has uncertainty that should be reduced before implementation.
- You need to decide which development workflow applies rather than loading several narrow process skills.

## Workflow Selector

| Situation | Use this mode | Key rule |
|---|---|---|
| Ambiguous implementation request | Planning | Write an actionable plan with exact files and bite-sized tasks before executing. |
| Unknown feasibility or risky integration | Spike | Build a disposable proof-of-concept; keep it separate from production code. |
| Bug or regression | Systematic debugging | Reproduce, collect evidence, form hypotheses, then fix root cause. |
| Behavioral change | TDD | Write/adjust a failing test first, then implement the smallest passing change. |
| Before final handoff or commit | Code review | Run security/quality checks and fix findings, not just summarize them. |
| Web/app UX validation | Dogfood QA | Explore like a user, capture evidence, and file reproducible issues. |

## Planning Mode

When the user explicitly asks for a plan or the change is broad, write a markdown plan in `.hermes/plans/` (or the project’s documented planning location). The plan should include paths, exact changes, tests, rollback notes, and acceptance criteria. Do not execute code changes in pure plan mode.

## Spike Mode

Use a spike when the right approach is unclear. Create throwaway experiments under a clearly disposable location, verify the key assumption, record the result, then delete or isolate spike artifacts before production work.

## Systematic Debugging

1. Reproduce the failure with a command, test, log, or browser action.
2. Inspect the relevant code and recent changes.
3. State competing hypotheses and choose the cheapest discriminating test.
4. Fix the root cause only after evidence points to it.
5. Re-run the failing case plus nearby regression tests.

Avoid random edits, broad rewrites before reproduction, or declaring success without executing the failing path.

## Test-Driven Development

For new behavior and bug fixes where tests are practical:

1. RED: add a failing test that captures the desired behavior or regression.
2. GREEN: implement the minimal code to pass.
3. REFACTOR: clean up while tests stay green.

If tests are impossible or too expensive, explain why and create the smallest executable verification available.

## Pre-Commit / Code Review

Before handoff, inspect diffs, run formatting/lint/tests/security checks appropriate to the repo, and fix actionable findings. Summaries must be grounded in real tool output.

## Dogfood QA

For web apps, use browser tooling to exercise primary flows, edge cases, and error states. Capture screenshots/logs/steps for bugs. See `references/dogfood/` if present for issue taxonomy and report templates.

## Demoted Source Details

Full source packages were absorbed into non-root support directories so they remain discoverable without registering as separate micro-skills:

- `references/plan-details/overview.md` — plan-mode rules and plan writing conventions.
- `references/spike-details/overview.md` — disposable experiment workflow and promotion criteria.
- `references/systematic-debugging-details/overview.md` — evidence-first root-cause workflow.
- `references/test-driven-development-details/overview.md` — RED/GREEN/REFACTOR details.
- `references/requesting-code-review-details/overview.md` — pre-commit review and security scan workflow.
- `references/dogfood-details/overview.md` plus `references/dogfood-details/references/` and `templates/` — exploratory QA issue taxonomy and report template.

Use these as supporting references; the class-level selector above should remain the primary trigger surface.

## Common Pitfalls

1. **Planning forever.** Plan enough to execute, then run the work unless the user requested plan-only mode.
2. **Skipping reproduction.** A fix that never reproduced the bug is untrusted.
3. **Inventing verification.** Report real command/browser output only.
4. **Letting spike code leak.** Promote only the understood design, not the scratch implementation.
5. **Treating QA as clicking around.** Record evidence and reproduction steps.
6. **Missing API auth headers from Angular SPAs.** When investigating web-app API calls from the console, use `credentials: 'include'` and extract `x-api-key` from the Network tab. See `references/angular-api-auth-bypass.md`.

## Verification Checklist

- [ ] Chosen workflow matches the task class.
- [ ] Any code change is backed by a failing/relevant test or an explicit verification alternative.
- [ ] Debugging changes cite the reproduced symptom and root-cause evidence.
- [ ] Final response reports actual commands, browser checks, or artifacts produced.
