# Claude Code on a VPS with tmux for phone access

Use this when the user wants Claude Code to stay open on a remote VPS and be accessible from a phone.

## Key distinction

The Claude mobile app does **not** attach to a Claude Code terminal session or SSH into a VPS. The reliable pattern is:

Phone SSH app → VPS → tmux session → Claude Code

Recommended phone clients: Termius, Blink Shell, Shelly, JuiceSSH.

## Setup / verification

```bash
command -v claude && claude --version
command -v tmux && tmux -V
systemctl is-active ssh 2>/dev/null || systemctl is-active sshd 2>/dev/null || true
ss -tlnp | grep ':22 ' || true
```

## Start a persistent Claude Code session

```bash
tmux new-session -d -s claude-phone -c /root 'claude'
tmux capture-pane -t claude-phone -p -S -80
```

If Claude asks to trust the workspace, send Enter or `1` + Enter, then capture again:

```bash
tmux send-keys -t claude-phone Enter
sleep 2
tmux capture-pane -t claude-phone -p -S -80
```

## User instructions

From the phone:

```bash
ssh root@<server-ip>
tmux attach -t claude-phone
```

Detach without killing Claude Code:

```text
Ctrl-b, then d
```

Reconnect later with:

```bash
tmux attach -t claude-phone
```

## Claude Code `--tmux` caveat

Claude Code has `--tmux`, but it is primarily tied to the worktree flow (`claude --worktree --tmux`). For the user's goal of persistent phone access, plain tmux wrapping `claude` is simpler and more predictable.

## Pitfalls

- Do not claim the Claude mobile app can connect directly to the VPS session.
- Do not leave Claude Code in an untracked foreground terminal if the user wants phone access; use tmux.
- Avoid exposing shell access through a web terminal unless authentication/firewall/reverse proxy are explicitly handled.
