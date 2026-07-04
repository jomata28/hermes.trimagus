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

### Updating Claude Code on VPS machines

When the user asks to update Claude Code, verify both the installed package version and the binary that `PATH` actually resolves. Claude Code can have multiple shims at once: an npm/global install may be current while `/root/.local/bin/claude` or `/usr/local/bin/claude` still points at an older self-managed local version.

Recommended check:

```bash
which claude
claude --version
npm list -g --depth=0 2>/dev/null | grep -i claude || true
npm view @anthropic-ai/claude-code version
ls -l /root/.local/bin/claude /usr/local/bin/claude /usr/bin/claude 2>/dev/null || true
/usr/bin/claude --version 2>/dev/null || true
```

If npm/global is newer but `claude` resolves to a stale local shim, repoint only the stale shim to the updated npm binary and verify again:

```bash
ln -sfn /usr/bin/claude /root/.local/bin/claude
hash -r
which claude
claude --version
```

Tell the user to exit/reopen any existing tmux Claude session so the running shell picks up the updated CLI.

### Mobile/VPS access pattern

When the user wants to access Claude Code on a VPS from a phone, do **not** imply the Claude mobile app can attach to the terminal session directly. Use a persistent `tmux` session on the VPS and have the phone connect via SSH/Mosh, then attach to tmux. See `references/mobile-claude-code-tmux.md` for setup commands, Mosh firewall ports, Android client recommendations, and the root-password-login pitfall.

### VPS / phone access pattern

When the user wants Claude Code to stay open on a VPS and access it from a phone, use **SSH + tmux + Claude Code**. The Claude mobile app cannot attach directly to a Claude Code terminal session. Prefer creating a named tmux session such as `claude-phone`, start `claude` inside it, handle the workspace trust prompt, then tell the user to connect from a phone SSH client and run `tmux attach -t claude-phone`. See `references/claude-code-vps-tmux.md`.

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
