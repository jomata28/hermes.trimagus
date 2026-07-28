# Herdr — agent multiplexer on JT's VPS

Herdr = terminal workspace manager / agent multiplexer (ogulcancelik/herdr, herdr.dev).
JT's stated goal: Herdr is the **multi-project agent cockpit**; Hermes on Telegram is
the **orchestrator** that reads and directs panes via the socket API.

## Install (done 2026-07-25)
- Binary: `/root/.local/bin/herdr` (v0.7.5, from GitHub release `herdr-linux-x86_64`)
- Config/logs: `/root/.config/herdr/` (`config.toml`, `herdr.log`)
- Server runs in background; client+server talk over unix socket
  `/root/.config/herdr/herdr.sock`.

## Command map (verified working)
| Task | Command |
|---|---|
| Server status | `herdr status` |
| Full JSON snapshot (workspaces/tabs/panes/agents) | `herdr api snapshot` |
| Workspaces | `herdr workspace list` |
| Tabs | `herdr tab list` / `herdr tab create --label <name>` |
| Panes | `herdr pane list` / `herdr pane current` |
| Run in a pane | `herdr pane run -- <cmd>` |

Snapshot tells you: workspace name, tab labels, pane id (`w1:p1`), running agent
(e.g. `claude`), pane title, status (idle/running), cwd, focus. This is how Hermes
"sees" the cockpit from Telegram.

## Operating pattern
- One **workspace per project** (bitacora · step1 · ai-agency/foundationatlas · lab),
  agent panes inside each (Hermes CLI, Claude Code, data scripts).
- Hermes reads `herdr api snapshot` to report "what's running where" and can start
  new tabs/panes on request. JT can also attach interactively from Termius/Hostinger
  with plain `herdr`.
- Observed initial state: workspace `~`, 1 tab, 1 pane = Claude Code
  (title "Claude Code CLI session", cwd `/root`, status idle).

## Claude Code on Kimi/Moonshot (PLANNED — not applied, JT said don't switch yet)
Claude Code supports Anthropic-compatible gateway env vars:
```bash
export ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"
export ANTHROPIC_AUTH_TOKEN="$KIMI_API_KEY"   # stored in /root/.hermes/.env (verified working)
export ANTHROPIC_MODEL="kimi-k2.6"            # or kimi-k3
export ANTHROPIC_SMALL_FAST_MODEL="kimi-k2.6"
claude
```
Rules: do this in a **new Herdr tab** (e.g. label `kimi`) so the existing Claude pane
stays on its current provider; only when JT explicitly asks. If the direct endpoint is
rejected, fall back to an Anthropic-compatible proxy on 127.0.0.1 and point
ANTHROPIC_BASE_URL there.
