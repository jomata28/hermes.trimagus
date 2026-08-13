---
name: vps-desktop-sessions
description: "Operate the persistent noVNC virtual desktop on JT's Hostinger VPS: start the service, launch GUI apps, take screenshots, and run the user-login pattern for authenticated accounts (claude.ai, Substack, ORA, Skool)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vps, novnc, remote-desktop, vnc, authenticated-sessions, screenshots]
---

# VPS Desktop Sessions

JT's VPS has a persistent virtual desktop (Xvfb + fluxbox + x11vnc + noVNC) used when a task needs a real browser/GUI — especially for sites where **JT logs in himself** (claude.ai, Substack, ORA, Skool, NotebookLM, government portals with CAPTCHA).

## When to use

- JT asks you to read/operate one of his authenticated web accounts.
- A site blocks automation with CAPTCHA/login walls and a human-in-the-loop browser is the answer.
- JT asks to "see his screen" from Hostinger terminal or Termius.

## Service management

```bash
systemctl start vps-screen.service        # start (it is stopped by default after reboots)
systemctl is-active vps-screen.service
ss -tlnp | grep -E '5901|6080'            # x11vnc on 5901, websockify on 172.18.0.1:6080
```

- Display is `:99` (1440x950). Launch GUI apps with `DISPLAY=:99 <app>` via `terminal(background=true)`.
- Access URL for JT: `https://vnc.srv1056157.hstgr.cloud/vnc.html?autoconnect=true&resize=scale&path=websockify`
- The first prompt is HTTP Basic Auth and requires **username `jt`** plus the password from `/root/.vps-screen/basic-auth-password.txt`.
- noVNC may then show a second, VNC-specific password prompt. The user-enterable plaintext is stored at `/root/.vps-screen/password.txt`; `/root/.vps-screen/x11vnc.pass` is the hashed/auth file used by the service, not the value to send.
- Before sending access details, verify the HTTP pair without exposing the password in output: `curl -sS -u "jt:$(tr -d '\n' </root/.vps-screen/basic-auth-password.txt)" -o /dev/null -w '%{http_code}\n' 'https://vnc.srv1056157.hstgr.cloud/vnc.html'` should return `200`.
- Send these server credentials only in JT's DM when he needs access; never persist their values to memory, skills, logs, or task summaries.

## Authenticated-account pattern (JT logs in, you read)

1. Start service, then `DISPLAY=:99 chromium --no-sandbox --disable-dev-shm-usage --start-maximized <login-url>` in background.
2. Verify HTTP Basic Auth returns `200` using username `jt` and the password file.
3. Send JT the noVNC URL plus both access stages, clearly labeled:
   - first prompt: HTTP username `jt` + Basic Auth password;
   - second prompt, if shown: VNC password from `password.txt`.
4. JT logs into the target website himself (never ask for or type his website password/2FA).
5. When he confirms, capture the desktop and verify that the target site is authenticated before operating it.
6. Chromium on this box is a **snap** — it keeps a persistent profile at `/root/snap/chromium/common/chromium/Default/`; sessions can survive across launches, so check existing cookies before asking JT to log in again.

## Screenshots of the desktop

Only `xwd` is installed (no scrot/ImageMagick):

```bash
DISPLAY=:99 xwd -root -silent -out /tmp/screen.xwd
```

Convert with PIL/ffmpeg if needed; or ask JT what he sees for quick checks.

## Chromium headless file rendering pitfall

Snap chromium (AppArmor-confined) **cannot read/write arbitrary /tmp paths** — `--screenshot=/tmp/...` fails with "No such file or directory". For HTML→PNG/PDF rendering, work under the snap-writable dir and copy out:

```bash
mkdir -p /root/snap/chromium/common/render
cp input.html /root/snap/chromium/common/render/
chromium --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --screenshot=/root/snap/chromium/common/render/out.png \
  --window-size=1600,900 file:///root/snap/chromium/common/render/input.html
cp /root/snap/chromium/common/render/out.png /tmp/
```

This is the rendering path for target-slide/vision-slide HTML→PNG pipelines.

## User-facing mental model (explain when JT confuses surfaces)

- Hostinger browser terminal = plain shell.
- Termius (Android) = SSH shell from phone.
- noVNC URL = the actual visual desktop.
- Herdr = terminal multiplexer that runs inside any of those shells.
