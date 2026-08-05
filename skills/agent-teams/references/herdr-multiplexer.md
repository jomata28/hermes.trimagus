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
| Run command in pane | `herdr pane run <PANE_ID> <COMMAND>...` |

Snapshot tells you: workspace name, tab labels, pane id (`w1:p1`), running agent
(e.g. `claude`), pane title, status (idle/running), cwd, focus. This is how Hermes
"sees" the cockpit from Telegram.

## Pane interaction (sending queries to agent panes like Claude Code)
Use `send-text` + `send-keys` + `read` to talk to agent panes interactively:

```
# 1. Send text (types it into the pane's terminal)
herdr pane send-text <PANE_ID> "your question here"

# 2. Press Enter to submit
herdr pane send-keys <PANE_ID> Enter

# 3. Wait for processing, then read output
herdr pane read <PANE_ID>

# Or wait for expected output pattern before reading
herdr pane wait-output <PANE_ID> "expected pattern"
```

Special keys for `send-keys`: `Enter`, `Escape`, Tab, etc. (capitalized).

## Login/auth for Claude Code in Herdr
Claude Code in a Herdr pane is a CLI session needing auth. Run `/login`:
1. Select method (1=Claude account, 2=Console API, 3=3rd-party)
2. An OAuth URL is shown — give to JT to open in browser
3. JT authenticates, gets a code — paste it back via `send-text` + `send-keys Enter`
4. If OAuth fails with "Invalid code", send `Escape` key then `/login` again

## Command map (pane-specific)
| Task | Command |
|---|---|
| Send typed text to pane | `herdr pane send-text <ID> "text"` |
| Send key press | `herdr pane send-keys <ID> Enter` |
| Read pane output | `herdr pane read <ID>` |
| Wait for output match | `herdr pane wait-output <ID> "pattern"` |
| Run and get output (non-interactive) | `herdr pane run <ID> <cmd>` |

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