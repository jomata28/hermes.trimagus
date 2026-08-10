# Mobile Claude Code on a VPS via SSH + tmux

Use this when the user wants to run Claude Code on a remote VPS and access it from a phone/tablet.

## Pattern

Claude Code itself runs as a terminal TUI on the VPS. Mobile apps do not attach directly to the Claude app; the reliable route is:

`phone SSH/Mosh client -> VPS -> tmux session -> claude`

## Server setup checklist

1. Verify Claude Code and tmux:
   ```bash
   command -v claude && claude --version
   command -v tmux && tmux -V
   ```
2. Start a durable session:
   ```bash
   tmux new-session -d -s claude-phone -c /root 'claude'
   tmux attach -t claude-phone
   ```
3. If prompted by Claude Code's workspace trust prompt, select the trusted workspace only after confirming the directory is safe.
4. Create a convenience wrapper if useful:
   ```bash
   cat >/usr/local/bin/claude-phone <<'EOF'
   #!/usr/bin/env bash
   set -euo pipefail
   SESSION="claude-phone"
   WORKDIR="/root"
   if tmux has-session -t "$SESSION" 2>/dev/null; then
     exec tmux attach -t "$SESSION"
   else
     cd "$WORKDIR"
     tmux new-session -s "$SESSION" "claude"
   fi
   EOF
   chmod +x /usr/local/bin/claude-phone
   ```
5. From phone, SSH in and run:
   ```bash
   claude-phone
   # or, if attaching to a root-owned tmux session from another user:
   sudo claude-phone
   ```

## Mobile network resilience

For Android/iOS over flaky networks, Mosh can be better than SSH if the client supports it:

```bash
apt-get update && apt-get install -y mosh
ufw allow 60000:61000/udp comment 'Mosh mobile SSH'
mosh user@HOST
```

Still use tmux inside Mosh so Claude survives app closure/reconnect.

## Root login pitfall

Many VPS images have `PermitRootLogin without-password`, so password SSH as root fails even when SSH is up. Check:

```bash
sshd -T | grep -E '^(permitrootlogin|passwordauthentication|pubkeyauthentication) '
tail -n 80 /var/log/auth.log 2>/dev/null || journalctl -u ssh -n 80 --no-pager
```

If root password login is disabled, prefer a dedicated mobile user over enabling root passwords:

```bash
useradd -m -s /bin/bash jt
passwd jt
usermod -aG sudo jt
```

If the Claude tmux session is root-owned, either run the session under the phone user from the start or add a narrow sudoers rule for the wrapper/tmux only.

## Android client recommendations

- Termius: easiest UI for saved SSH hosts and phone use.
- JuiceSSH: good Android-native alternative.
- Termux: best for a real shell; install `openssh` and optionally `mosh`.

## Safety

Do not paste credentials into durable skills or memory. If a password is generated during a session, deliver it to the user in the current chat only and encourage changing it or replacing it with SSH keys later.

## OAuth login fallback (when Herdr pane auth fails)

Claude Code OAuth through a Herdr pane repeatedly fails with "Invalid code" — the authorization code expires in ~2 min, and Herdr pane text input + keypress submission introduces enough delay (and possible encoding issues) to miss the window.

**Working fix:** Have the user SSH into the VPS directly and run:

```bash
claude auth login --claudeai
```

This prints an OAuth URL. The user opens it in their browser, authorizes, copies the code, and pastes it back into the SSH terminal within the 2-min window. Direct SSH is faster and more reliable than Herdr pane input routing.

Once authenticated, `~/.claude/.credentials.json` is written with the access token. Any Herdr pane Claude Code processes may need a restart to pick up the new token.

**Verification:**
```bash
claude --version
# Should print version number without prompting for login
```
