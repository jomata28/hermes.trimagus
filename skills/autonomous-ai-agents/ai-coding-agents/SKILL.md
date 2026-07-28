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

### Herdr as a Claude Code cockpit

When Herdr is installed/running, prefer treating it as the persistent terminal cockpit for Claude Code/Codex/Hermes agent panes instead of guessing from process names alone. Useful inspection commands:

```bash
herdr status
herdr api snapshot
herdr workspace list
herdr tab list
herdr pane list
herdr pane current
herdr pane read <pane-id>
```

Summarize the live Herdr state as workspace → tabs → panes → agent/status/cwd. If the user asks to modify Claude Code provider/auth, do **not** mutate the currently working pane by default; create a separate Herdr tab/pane for experimentation so the existing Anthropic/OpenAI setup remains intact.

### Routing Claude Code to Kimi/Moonshot (verified working)

Claude Code works directly against Moonshot's Anthropic-compatible endpoint — no proxy needed. Verified with model `kimi-k3` in a parallel Herdr pane while the original Anthropic pane stayed untouched:

```bash
export ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"
export ANTHROPIC_AUTH_TOKEN="$KIMI_API_KEY"
export ANTHROPIC_MODEL="kimi-k3"
export ANTHROPIC_SMALL_FAST_MODEL="kimi-k3"
claude
```

Verify inside the session with `/status` — must show `Auth token: ANTHROPIC_AUTH_TOKEN`, base URL `api.moonshot.ai/anthropic`, `Model: kimi-k3`. Subscription marketing banners (Max plan, model promos) still render but are NOT evidence of which backend is active; `/status` is the only source of truth. Full verified Herdr launch sequence (tab create with `--env`, trust-prompt/fullscreen-prompt handling, pane-read checks) is in `references/herdr-agent-multiplexer.md`. Keep experiments in a separate Herdr tab/pane until the user explicitly asks to switch defaults.

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

Two separate use modes. Keep them distinct:

1. **Worker CLI** — Hermes launches `agy -p ...` for coding/review tasks.
2. **Hermes main model backend** — local OpenAI-compatible proxy fronts `agy` so Hermes can use Antigravity subscription models as `model.provider`.

Confirm install/auth before either mode; capture CLI output and changed files for worker runs.

### Worker CLI usage

```bash
command -v agy && agy --version
agy models
agy -p 'task prompt' --model gemini-3.5-flash-medium --print-timeout 10m --dangerously-skip-permissions
```

Headless VPS needs `--dangerously-skip-permissions` for tool/command permission prompts that would otherwise auto-deny.

### Auth on headless VPS

Antigravity auth belongs to the `agy` CLI itself, not Hermes credential pools. If the user asks for a command like `hermes auth add google-antigravity --type oauth`, first test it, but expect current Hermes installs to reject `google-antigravity` as an unknown provider. In that case, run the `agy` auth flow instead.

Pattern:

```bash
command -v agy && agy --version
agy --print 'auth smoke test' --print-timeout 5m
```

When unauthenticated, `agy --print` prints a Google OAuth URL and waits for an authorization code on stdin. The inner auth prompt may time out after ~60 seconds even when `--print-timeout` is longer, so make the user ready before starting the flow or restart with a fresh URL if it expires. Full operational notes: `references/antigravity-auth-vps.md`.

### Using Antigravity models as Hermes main model

Hermes has no first-party `antigravity` / `google-antigravity` provider. When JT wants Hermes itself to run on agy models, do **not** invent a core Hermes provider plugin unless asked for a repo contribution. The proven local path is:

1. Auth `agy`.
2. Run a local OpenAI-compatible server at `http://127.0.0.1:9777/v1` with `/health`, `/v1/models`, `/v1/chat/completions` backed by `agy --print`.
3. Register it as Hermes custom provider `antigravity` and set `model.*` to that proxy.
4. Smoke-test: `hermes chat -q '...' --provider antigravity -m <model>`.

On JT's VPS the durable artifacts are:

- proxy: `/root/agy-proxy/proxy.py` (stdlib HTTP; avoid nested FastAPI/Pydantic route models that crash schema generation)
- PM2 app: `agy-proxy`
- Hermes provider: `antigravity`
- verified default: `gemini-3.5-flash-medium`

Full recipe + caveats: `references/antigravity-hermes-main-model-proxy.md`.

## Common Pitfalls

1. Delegating with vague acceptance criteria.
2. Letting an external agent overwrite uncommitted user work.
3. Believing a self-reported test pass without rerunning tests.
4. Forgetting that external CLIs may need auth or interactive setup.
5. Treating every external agent auth as a Hermes `auth add` provider; some CLIs, including Antigravity, manage OAuth in their own CLI state.
6. Expecting Antigravity to appear in `hermes model` without a local proxy/custom-provider bridge.
7. Reusing a Google OAuth code from a previous `agy` URL attempt → `invalid_grant` / `Invalid code verifier`.
8. Blocking proxy startup on synchronous `agy models` — bind the HTTP port first; refresh models in background.
9. Assuming agy-proxy supports streaming or native Hermes tool calling; the current bridge is non-stream text in/out with tools serialized into the prompt.

## Verification Checklist

- [ ] Repository and dirty state inspected.
- [ ] CLI installation/auth verified.
- [ ] Prompt includes tests and acceptance criteria.
- [ ] Diff reviewed by Hermes.
- [ ] Tests/linters run by Hermes after agent completion.
