---
name: ai-coding-agents
description: "Use when delegating coding work to external AI coding CLIs such as Claude Code, Codex, OpenCode, or Google Antigravity; covers setup, task framing, execution, and verification."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ai-agents, coding, claude-code, codex, opencode, antigravity]
    related_skills: [subagent-driven-development]
---

# AI Coding Agents

## Overview

This umbrella covers external agentic coding CLIs as a class. The specific CLI may differ, but the durable workflow is the same: verify installation/auth, prepare a scoped task with repository context, run the agent in an isolated worktree or clean branch, then verify outputs yourself.

## When to Use

- The user asks to delegate implementation, PR review, refactoring, or debugging to Claude Code, Codex, OpenCode, or Google Antigravity (`agy`).
- A coding task benefits from independent agent exploration.
- You need a second implementation/review pass while preserving Hermes as the orchestrator.

Do not use for a single command or trivial edit where direct tools are faster.

## Shared Workflow

1. Inspect repository state, instructions, tests, and dirty files.
2. Verify the chosen CLI is installed and authenticated.
3. Create a precise prompt with goal, constraints, files, test command, and output expectations.
4. Run in a safe context: separate branch/worktree/session when possible.
5. Read the agent's changes and logs.
6. Run tests/linters yourself; never trust the agent's self-report alone.

## Claude Code

Good for feature implementation and PR-sized coding tasks. Provide exact repo context and ask for evidence. Avoid interactive hangs by using the appropriate CLI mode for the environment.

## Codex

Good for focused coding, debugging, and patch generation. Keep prompts compact and verify every changed file with git diff and tests.

## OpenCode

Good for implementation and PR review workflows. Use it when configured for the user's environment and return verifiable handles or diffs.

## Google Antigravity (`agy`)

Use for agentic coding when `agy` is installed/authenticated. Confirm setup before relying on it; capture CLI output and changed files.

## Common Pitfalls

1. Delegating with vague acceptance criteria.
2. Letting an external agent overwrite uncommitted user work.
3. Believing a self-reported test pass without rerunning tests.
4. Forgetting that external CLIs may need auth or interactive setup.

## Verification Checklist

- [ ] Repository and dirty state inspected.
- [ ] CLI installation/auth verified.
- [ ] Prompt includes tests and acceptance criteria.
- [ ] Diff reviewed by Hermes.
- [ ] Tests/linters run by Hermes after agent completion.
