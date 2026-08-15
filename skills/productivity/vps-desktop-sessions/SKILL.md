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

## Packaged GUI applications

For installing and launching `.deb`/AppImage/Tauri/GTK/WebKit apps on this desktop, follow `references/packaged-gui-apps.md`. It covers architecture/release selection, tracked `DISPLAY=:99` launches, delayed or initially unmapped Tauri windows, three-layer verification (process → X window → rendered UI), and safe handling of first-run screens containing private keys or recovery secrets. For Block Buzz specifically, use `references/buzz-desktop.md` for the official packaged install, first-run model downloads, relay choices, BuilderLab handoff, and noVNC recovery.

For long-lived GUI apps, do not attach broad watch patterns such as `error|failed|panic` unless the matched events are truly exceptional. Apps that retry unavailable backends can otherwise spam the user with harmless heartbeat failures. Prefer a silent tracked background process, then inspect its process state and logs deliberately when diagnosing it.

Always distinguish **installed**, **launched**, and **operational**. A GUI client may be correctly installed and visible while its required relay/backend is still offline.

For packaged-app OAuth flows that say they will open a browser, use `references/gui-oauth-browser-handoff.md`. It separates desktop/app health, external-browser launch, and relay/callback connectivity; includes a known-good Snap Chromium desktop launcher for a root-run VPS; and preserves the boundary that JT enters passwords and 2FA directly in noVNC.

## Screenshots of the desktop

Capture the current X11 desktop before claiming what is open. Do not infer the visible window from browser/CDP tabs alone.

Preferred raw capture when `xwd` is available:

```bash
DISPLAY=:99 xwd -root -silent -out /tmp/screen.xwd
```

A reliable PNG fallback is `ffmpeg` with X11 grab. Discover the actual display geometry first instead of assuming 1920x1080; this desktop is commonly 1440x950, and an oversized capture area fails.

```bash
GEOM=$(DISPLAY=:99 xdpyinfo | awk '/dimensions:/{print $2; exit}')
ffmpeg -y -f x11grab -video_size "$GEOM" -i :99 -frames:v 1 -update 1 /tmp/current-screen.png
```

Load the resulting image with vision and report only what is visibly present: active app/window, page or setup step, notable warnings, and whether the requested application is actually on screen.

### Screenshot credential safety

GUI setup screens can expose API keys, recovery phrases, passwords, cookies, or tokens. If a screenshot contains a secret:

1. Never transcribe, quote, or partially reproduce the value.
2. Describe it only as a visible credential and warn the user before screen sharing or recording.
3. Delete temporary screenshots and logs immediately after inspection unless the user explicitly asked to retain them.
4. Do not attach or deliver the screenshot back to the user unless it has been safely redacted.

### Entering secrets into GUI setup screens

When JT explicitly authorizes entering an API key or token into a GUI, treat successful keystrokes and successful configuration as separate claims:

1. Capture and inspect the live screen immediately before clicking. Do not reuse coordinates from an older screenshot because responsive layouts, dropdowns, and scroll position can move the target field.
2. Locate the field by its visible label and current geometry, then type. A command that returns no error proves only that input events were sent, not that they reached the correct control.
3. Verify the target field indirectly: its placeholder should disappear, dependent controls should unlock or populate, and the wizard should advance after validation. Never claim success from `xdotool` exit status alone.
4. If input may have landed in the wrong field, clear that candidate field before entering the secret in the corrected location. Do not leave the credential duplicated in a provider URL, model, search, or other text box.
5. After a secret is present, never send the raw screenshot to vision. Capture locally, redact every plausible credential-bearing field into a separate image, delete the raw image first, and inspect only the redacted copy.
6. Delete all temporary redacted screenshots after verification unless JT explicitly asks to retain one.
7. Complete deterministic setup choices such as provider, model, and effort when the requested configuration makes them obvious. Stop and ask when the next screen asks a meaningful user-specific question, such as account role or community ownership.

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
