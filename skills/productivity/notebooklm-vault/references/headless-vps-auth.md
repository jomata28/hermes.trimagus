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
printf 'VNC_PASSWORD=%s\n' "$PASS"
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

If the trycloudflare URL returns a Cloudflare `502` and the log says `dial tcp 127.0.0.1:6080: connect: connection refused`, noVNC/websockify is not listening where cloudflared expects. Kill just the noVNC/cloudflared layer and restart with direct websockify, then re-check before sharing the URL:

```bash
pkill -f 'websockify.*6080|novnc_proxy|cloudflared.*6080' || true
websockify --web=/usr/share/novnc 127.0.0.1:6080 127.0.0.1:5901 >/tmp/websockify-notebooklm.log 2>&1 &
cloudflared tunnel --url http://127.0.0.1:6080 --no-autoupdate >/tmp/cloudflared-novnc.log 2>&1 &
```

From Hermes, do not run those `&` commands directly in a foreground terminal call; wrap them in a small script and launch it with `terminal(background=true)`, then verify with `ss` and the cloudflared log.

Give the user the **auto-connect URL** if possible:

```text
https://<random>.trycloudflare.com/vnc.html?autoconnect=true&resize=scale&path=websockify&password=<VNC_PASSWORD>
```

This avoids the common failure mode where the user opens noVNC but only sees the connection/password screen. If you send the plain URL instead, include:

- `https://<random>.trycloudflare.com/vnc.html`
- the generated VNC password
- steps: Connect → enter password → complete Google login → wait until NotebookLM home loads → tell Hermes "done".

If the user says they cannot see it, cannot enter the noVNC password, or the password is rejected:

1. Check processes/ports/logs before rotating links/passwords:
   ```bash
   pgrep -fa 'Xvfb :99|x11vnc|websockify|novnc|cloudflared|notebooklm login|chrome-linux' | head -120 || true
   ss -tlnp | grep -E ':(5901|6080)\\b' || true
   tail -40 /tmp/notebooklm-login.log || true
   tail -40 /tmp/novnc-notebooklm.log || true
   tail -40 /tmp/websockify-notebooklm.log || true
   ```
   A stale `x11vnc` may still own port `5901` and may be using a different `-rfbauth` file than the password you just generated. Kill stale VNC/websockify/cloudflared/login/browser processes, verify `5901` and `6080` are free, then restart. If an existing VPS-screen service intentionally owns VNC, use its actual VNC password rather than inventing a new one.
2. If Cloudflare returns 502, compare `cloudflared --url` with the actual `websockify` listener from `ss -tlnp`. In containerized setups, `websockify` may listen on an interface address (for example `172.x.x.x:6080`) while `cloudflared` points to `127.0.0.1:6080`; make them match and verify the final `vnc.html` URL returns HTTP 200 with `curl` before sending it.
3. If `notebooklm login` timed out (`Login not detected within 5 minutes`), restart just the login command in background:
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
pkill -f 'Xvfb :99|x11vnc.*:99|websockify.*6080|novnc_proxy|cloudflared.*6080|notebooklm login|chrome.*notebooklm' || true
```

## Refresh / repair an expired remote-view link

When the user asks for a new remote-view link, treat the quick tunnel as disposable. Do not reuse an old `trycloudflare.com` URL. Kill only the exposure/login pieces, keep or restart `Xvfb :99` and `fluxbox`, then create a fresh VNC password, start `x11vnc`, `websockify`, `notebooklm login`, and a new `cloudflared` tunnel.

A reliable repair sequence is:

```bash
PASS=$(openssl rand -base64 18 | tr -d '=+/ ' | cut -c1-14)
mkdir -p /root/.notebooklm
printf '%s' "$PASS" > /root/.notebooklm/current_vnc_password.txt
x11vnc -storepasswd "$PASS" /root/.notebooklm/x11vnc.pass >/dev/null

pkill -f 'x11vnc.*5901|websockify.*6080|novnc_proxy|cloudflared.*6080|notebooklm login|chrome.*notebooklm' || true

pgrep -f 'Xvfb :99' >/dev/null || Xvfb :99 -screen 0 1440x950x24 -ac >/tmp/xvfb-notebooklm.log 2>&1 &
sleep 1
pgrep -f 'fluxbox -display :99' >/dev/null || fluxbox -display :99 >/tmp/fluxbox-notebooklm.log 2>&1 &
sleep 1
```

Then start long-lived pieces with Hermes `terminal(background=true)` or separate tracked processes:

```bash
x11vnc -display :99 -rfbauth /root/.notebooklm/x11vnc.pass -forever -shared -rfbport 5901 -localhost
websockify --web=/usr/share/novnc 172.18.0.1:6080 127.0.0.1:5901
DISPLAY=:99 notebooklm login --browser chromium
cloudflared tunnel --url http://172.18.0.1:6080 --no-autoupdate
```

If the tunnel serves a 502, inspect where `websockify` is actually listening (`ss -tlnp | grep -E ':(5901|6080)\\b'`) and make the `cloudflared --url` host match that listener. In this VPS/container pattern, `websockify` may show `172.18.0.1:6080`; using `http://127.0.0.1:6080` then returns Cloudflare 502 even though the tunnel exists.

Before sending the link, verify it is live:

```bash
curl -sS -o /tmp/novnc_check.html -w '%{http_code}' --max-time 15 \
  "https://<subdomain>.trycloudflare.com/vnc.html?autoconnect=true&resize=scale&path=websockify&password=$PASS"
```

Only hand off links that return `HTTP 200`. If DNS for a brand-new quick tunnel has not propagated (`Could not resolve host`), create a new quick tunnel rather than making the user retry a stale URL.

## Pitfalls

- If the user cannot see the remote browser, send the auto-connect URL form with `autoconnect=true&resize=scale&path=websockify&password=...`; verify HTTP 200 before handing it off. Browser vision is useful when available, but an HTTP 200 check is the minimum.
- Do not claim NotebookLM access until `notebooklm auth check --test` and `notebooklm list` pass.
- The original npm CLI may be installed but not sufficient for this workflow; prefer `notebooklm-py` and verify the command help.
- `notebooklm login --headless` can dump core / hang with Google login. Use visible Chromium over noVNC instead.
- `notebooklm login` can fail with “Missing X server or $DISPLAY” if Chromium starts before `Xvfb :99` is actually running. Confirm `pgrep -fa 'Xvfb :99'`, then restart only `DISPLAY=:99 notebooklm login --browser chromium` after the X server is live.
- `notebooklm login` initially failed with `Playwright not installed`; fix with `pip install 'notebooklm-py[browser]'` and `python3 -m playwright install chromium`.
- A Cloudflare quick tunnel is temporary and not access-controlled. Use it only long enough for auth, then kill it. For persistent access, use a named Cloudflare Tunnel + Access instead.
- `apt-get install` may show debconf/kernel prompts in noninteractive tools; it still completed in this session despite whiptail errors.

  Validate with `curl -sS -o /tmp/novnc.html -w '%{http_code}' "$URL/vnc.html?..."` and only share the URL if it returns 200.
- If `novnc_proxy` exits immediately or binds oddly, use direct `websockify --web=/usr/share/novnc <listen>:6080 127.0.0.1:5901` instead of the wrapper.
- If `Xvfb :99` is already running (for another remote-screen session), do not kill/restart it blindly. Reuse it, or start a different display; restarting can break the auth browser and other active VNC sessions.
- When launching NotebookLM auth, make sure `DISPLAY=:99` is exported for the `notebooklm login --browser chromium` command itself; otherwise Playwright reports “headed browser without an XServer” even if Xvfb exists.
- Do not claim NotebookLM access until `notebooklm auth check --test` and `notebooklm list` pass.
- The original npm CLI may be installed but not sufficient for this workflow; prefer `notebooklm-py` and verify the command help.
- `notebooklm login --headless` can dump core / hang with Google login. Use visible Chromium over noVNC instead.
- `notebooklm login` initially failed with `Playwright not installed`; fix with `pip install 'notebooklm-py[browser]'` and `python3 -m playwright install chromium`.
- A Cloudflare quick tunnel is temporary and not access-controlled. Use it only long enough for auth, then kill it. For persistent access, use a named Cloudflare Tunnel + Access instead.
- `apt-get install` may show debconf/kernel prompts in noninteractive tools; it still completed in this session despite whiptail errors.
