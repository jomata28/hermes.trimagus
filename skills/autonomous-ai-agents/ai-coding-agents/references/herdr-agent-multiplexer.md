# Herdr agent multiplexer notes

Herdr is a terminal workspace manager / multiplexer for AI coding agents. Use it when JT wants persistent agent panes/tabs on the VPS, especially from Hostinger terminal or Termius on Android.

## Install / verify

Official repo/site observed in session:
- GitHub: `ogulcancelik/herdr`
- Docs: `https://herdr.dev`

Linux x86_64 manual install pattern:

```bash
mkdir -p ~/.local/bin /tmp/herdr-install
cd /tmp/herdr-install
curl -fL --retry 3 -o herdr-linux-x86_64 \
  https://github.com/ogulcancelik/herdr/releases/download/v0.7.5/herdr-linux-x86_64
chmod +x herdr-linux-x86_64
install -m 0755 herdr-linux-x86_64 ~/.local/bin/herdr
herdr --version
herdr status
```

Expected status shape after install but before launch:

```text
client: version 0.7.5
server: status: not running
```

After launch/attach, server status should become `running` with socket:

```text
~/.config/herdr/herdr.sock
```

## Useful inspection commands

```bash
herdr status
herdr api snapshot
herdr workspace list
herdr tab list
herdr pane list
herdr pane current
herdr pane read <pane-id>
```

`herdr api snapshot` returns JSON with `workspaces`, `tabs`, `panes`, `agents`, focused IDs, cwd, terminal title, and agent status. Summarize this into a small table for JT instead of dumping JSON.

## Operating pattern

- Herdr can keep a Claude Code / Codex / Hermes pane alive independently of the current chat.
- Prefer creating a separate Herdr tab for experiments (for example Kimi-backed Claude Code) instead of mutating an existing Anthropic/Claude pane.
- Leave current provider sessions untouched unless JT explicitly says to switch.

## Claude Code via Kimi/Moonshot

Claude Code can often be pointed at Kimi/Moonshot by launching it in a separate pane with environment variables such as:

```bash
export ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"
export ANTHROPIC_AUTH_TOKEN="$KIMI_API_KEY"
export ANTHROPIC_MODEL="kimi-k2.6"   # or the target Kimi model supported by endpoint
export ANTHROPIC_SMALL_FAST_MODEL="$ANTHROPIC_MODEL"
claude
```

If the direct Anthropic-compatible endpoint is rejected, run a local Anthropic-compatible proxy and point `ANTHROPIC_BASE_URL` at `http://127.0.0.1:<port>`.

## Project cockpit layout pattern

When JT asks for "multiple threads running my projects", propose one Herdr workspace per project with a long-lived agent pane in each, e.g. `bitacora` (Hermes CLI with workdir on the vault), `step1` (study/Anki generation), `foundationatlas` (Claude Code builder), `lab` (data processing). Hermes-on-Telegram stays the orchestrator: JT asks "check on the X agent" and you read that pane via `herdr api snapshot` / `herdr pane read` and report — he never context-switches unless he wants to. Create panes/tabs for experiments; never mutate a working provider pane without an explicit switch request.

## User-facing distinction

- Hostinger browser terminal = shell only.
- Termius on phone = SSH shell from Android.
- noVNC = visual virtual VPS desktop.
- Herdr = terminal multiplexer/cockpit that can run inside either shell or noVNC.
