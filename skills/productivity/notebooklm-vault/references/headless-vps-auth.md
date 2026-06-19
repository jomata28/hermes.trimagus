# NotebookLM auth on a headless VPS

Use this when Hermes runs on a VPS and the user cannot run local CLI/SSH tunnels. Goal: install NotebookLM CLI, expose a temporary noVNC browser through a Cloudflare quick tunnel, let the user complete Google login, then verify and shut it down.

## What worked

Two CLIs exist:

- `npm install -g notebooklm` installs an unofficial JS CLI. In this session it installed as `/usr/bin/notebooklm` and reported `0.1.0`, but its `login --headless` was not enough for Google auth.
- `pip install notebooklm-py` installs a richer Python CLI into the Hermes venv (`/root/.hermes/hermes-agent/venv/bin/notebooklm`) with commands matching this skill: `auth check`, `doctor`, `source`, `artifact`, `share`, `generate`, `download`, etc. Prefer this one.

Install/setup:

```bash
python3 -m pip install notebooklm-py
python3 -m pip install 'notebooklm-py[browser]'
python3 -m playwright install chromium
notebooklm doctor --fix
notebooklm auth check
```

If `command -v notebooklm` points to `/usr/bin/notebooklm` after npm install but the Hermes venv has the Python CLI, the active shell may still prefer the venv command. Verify with:

```bash
command -v notebooklm
notebooklm --help | head -40
```

Python CLI help begins with `NotebookLM CLI` and includes `auth check`, `doctor`, `share`, `artifact`, `download`.

## Temporary remote browser via noVNC + Cloudflare quick tunnel

Prereqs used:

```bash
apt-get update
apt-get install -y x11vnc novnc websockify fluxbox
# Xvfb was already installed in this environment

# cloudflared if missing
curl -L --fail --output /tmp/cloudflared.deb \
  https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
dpkg -i /tmp/cloudflared.deb
```

Create a one-time VNC password:

```bash
PASS=$(openssl rand -base64 18 | tr -d '=+/ ' | cut -c1-14)
mkdir -p /root/.notebooklm
printf '%s' "$PASS" > /root/.notebooklm/vnc_password.txt
x11vnc -storepasswd "$PASS" /root/.notebooklm/x11vnc.pass >/dev/null
printf 'VNC_PASSWORD=REDACTED_IN_BACKUP
```

Start the stack using a script (the terminal tool rejects direct foreground commands with `&` backgrounding):

```bash
cat >/tmp/start_notebooklm_vnc.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
pkill -f 'Xvfb :99|x11vnc.*:99|novnc_proxy|cloudflared.*6080|notebooklm login' || true
rm -f /tmp/notebooklm-login.log /tmp/cloudflared-novnc.log /tmp/xvfb-notebooklm.log /tmp/fluxbox-notebooklm.log /tmp/x11vnc-notebooklm.log /tmp/novnc-notebooklm.log
Xvfb :99 -screen 0 1280x900x24 -ac >/tmp/xvfb-notebooklm.log 2>&1 &
sleep 1
fluxbox -display :99 >/tmp/fluxbox-notebooklm.log 2>&1 &
x11vnc -display :99 -rfbauth /root/.notebooklm/x11vnc.pass -forever -shared -rfbport 5901 >/tmp/x11vnc-notebooklm.log 2>&1 &
/usr/share/novnc/utils/novnc_proxy --listen 127.0.0.1:6080 --vnc 127.0.0.1:5901 >/tmp/novnc-notebooklm.log 2>&1 &
DISPLAY=:99 notebooklm login --browser chromium >/tmp/notebooklm-login.log 2>&1 &
cloudflared tunnel --url http://127.0.0.1:6080 --no-autoupdate >/tmp/cloudflared-novnc.log 2>&1 &
echo "NotebookLM VNC/auth stack started. Waiting for auth; keep this process alive."
while true; do sleep 60; done
EOF
bash /tmp/start_notebooklm_vnc.sh
```

When launched from Hermes tools, use `terminal(background=true)` for the script, then verify:

```bash
sleep 10
ss -tlnp | grep -E ':(5901|6080)\b' || true
sed -n '1,80p' /tmp/notebooklm-login.log || true
grep -o 'https://[-a-zA-Z0-9.]*\.trycloudflare.com' /tmp/cloudflared-novnc.log | head -1
```

Give the user the **auto-connect URL** if possible:

```text
https://<random>.trycloudflare.com/vnc.html?autoconnect=true&resize=scale&path=websockify&password=<VNC_PASSWORD>
```

This avoids the common failure mode where the user opens noVNC but only sees the connection/password screen. If you send the plain URL instead, include:

- `https://<random>.trycloudflare.com/vnc.html`
- the generated VNC password
- steps: Connect → enter password → complete Google login → wait until NotebookLM home loads → tell Hermes "done".

If the user says they cannot see it:

1. Check processes/ports/logs:
   ```bash
   pgrep -fa 'Xvfb :99|x11vnc|novnc|cloudflared|notebooklm login|chrome-linux' | head -80 || true
   ss -tlnp | grep -E ':(5901|6080)\\b' || true
   tail -40 /tmp/notebooklm-login.log || true
   tail -40 /tmp/novnc-notebooklm.log || true
   ```
2. If `notebooklm login` timed out (`Login not detected within 5 minutes`), restart just the login command in background:
   ```bash
   pkill -f 'notebooklm login|chrome-linux|chromium-1223' || true
   rm -f /tmp/notebooklm-login.log
   DISPLAY=:99 notebooklm login --browser chromium 2>&1 | tee /tmp/notebooklm-login.log
   ```
   Launch that via `terminal(background=true)`; direct `&` backgrounding is rejected by the terminal tool.
3. Verify the auto-connect URL yourself with browser vision before sending it again. You should see the remote Chrome window on Google sign-in, not just the noVNC credential prompt.

## Verification after user logs in

```bash
notebooklm auth check --test || notebooklm auth check
notebooklm list
notebooklm status
```

If authenticated, shut down the temporary exposure:

```bash
pkill -f 'Xvfb :99|x11vnc.*:99|novnc_proxy|cloudflared.*6080|notebooklm login' || true
```

## Pitfalls

- If the user cannot see the remote browser, send the auto-connect URL form with `autoconnect=true&resize=scale&path=websockify&password=...`; verify it with browser vision before handing it off.
- Do not claim NotebookLM access until `notebooklm auth check` and `notebooklm list` pass.
- The original npm CLI may be installed but not sufficient for this workflow; prefer `notebooklm-py` and verify the command help.
- `notebooklm login --headless` can dump core / hang with Google login. Use visible Chromium over noVNC instead.
- `notebooklm login` initially failed with `Playwright not installed`; fix with `pip install 'notebooklm-py[browser]'` and `python3 -m playwright install chromium`.
- A Cloudflare quick tunnel is temporary and not access-controlled. Use it only long enough for auth, then kill it. For persistent access, use a named Cloudflare Tunnel + Access instead.
- `apt-get install` may show debconf/kernel prompts in noninteractive tools; it still completed in this session despite whiptail errors.
