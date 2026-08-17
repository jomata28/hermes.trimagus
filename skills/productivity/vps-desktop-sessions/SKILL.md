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
- For sites with payment, airline inventory, anti-bot, or reputation-sensitive APIs, prefer launching Chromium as a normal desktop user instead of root. Snap Chromium run as root requires `--no-sandbox`, which is a noisy browser fingerprint. If `runuser` fails with Snap cgroup/session errors, start a real user session and launch via `systemd-run`, e.g. `loginctl enable-linger jt; systemctl start user@1001.service; systemd-run --unit=<name> --collect --uid=jt --gid=jt --property=PAMName=login --setenv=HOME=/home/jt --setenv=DISPLAY=:99 --setenv=XDG_RUNTIME_DIR=/run/user/1001 chromium --disable-dev-shm-usage --lang=es-MX --start-maximized <url>`. Verify with process list and a fresh X11 screenshot before claiming the page is visible.
- When a site works generally but a sensitive API returns CDN/edge blocks, isolate network reputation before changing browsers: compare IPv4 vs IPv6 with `curl -4/-6`, and if needed temporarily block IPv6 only for the browser UID (`ip6tables -I OUTPUT 1 -m owner --uid-owner jt -j REJECT`) to test whether IPv6 reputation is the culprit. Remove/review such test rules after the session.
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
7. For multi-page extraction after human verification, prefer a dedicated profile plus local CDP endpoint, e.g. `--user-data-dir=/root/snap/chromium/common/<task-profile> --remote-debugging-address=127.0.0.1 --remote-debugging-port=<port>`. Verify the page through `http://127.0.0.1:<port>/json/list` before claiming control. A dedicated profile may require its own one-time Turnstile even if the default profile is already verified. See `references/human-verified-cdp-browser.md` for the reusable launch, handoff, verification, and stop conditions.

### Interaction and latency discipline

JT prefers fast, concise operation. Do not narrate every screenshot, click, or hypothesis.

- Batch independent readiness checks, launch, and capture where safe.
- After each state-changing click, verify once; after **two failed coordinate attempts**, change strategy rather than repeating pixels.
- If the visible browser is not present in X11 window discovery, focus is ambiguous, or events land in another window, launch a dedicated CDP-controlled Chromium profile instead of continuing `xdotool` trial-and-error.
- Give the user only meaningful checkpoints: human action required, verified result, or real blocker. Keep low-level diagnostics internal unless requested.
- For agent/chat round-trip tests, use a short fixed timeout and one controlled restart before deeper diagnosis; report measured latency separately from relay/network latency.

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

**If `import` (ImageMagick) is not installed**, `ffmpeg -f x11grab` is the most reliable fallback. `scrot` may fail silently. The `vision_analyze` tool may also be unavailable (503 from the vision model provider) — always have a text-based fallback (check window titles via `xdotool search --name "" getwindowname`, or inject JS via the DevTools console with `ctrl+shift+j`).

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

## noVNC Basic Auth password management

The noVNC URL is fronted by a Traefik reverse proxy (`vps-screen-proxy` Docker container running `alpine/socat`) that enforces HTTP Basic Auth via Traefik labels. The auth credentials are NOT in a file — they're baked into the container's Traefik labels.

**The socat container forwards Traefik → host's websockify on `172.18.0.1:6080`.** The container must use `TCP:172.18.0.1:6080` as the socat target (NOT `host.docker.internal` — that doesn't resolve without `--add-host`).

### Reading current credentials
```bash
docker inspect vps-screen-proxy --format '{{json .Config.Labels}}' | python3 -c "
import sys, json
labels = json.load(sys.stdin)
print(labels.get('traefik.http.middlewares.vps-screen-auth.basicauth.users', 'not found'))
"
```

### Changing the Basic Auth password (full recreation)
```bash
# 1. Generate new apr1 hash (Traefik requires this format)
NEW_HASH=$(printf "NEW_PASSWORD\n" | openssl passwd -apr1 -salt vnc12345 -stdin)
echo "jt:$NEW_HASH"

# 2. Stop and remove the old container
docker stop vps-screen-proxy && docker rm vps-screen-proxy

# 3. Recreate with new password hash in the Traefik label
#    NOTE: dollar signs in the hash MUST be escaped with backslash in --label
docker run -d \
  --name vps-screen-proxy \
  --network root_default \
  --restart always \
  --label "traefik.enable=true" \
  --label "traefik.http.middlewares.vps-screen-auth.basicauth.realm=JT VPS Screen" \
  --label "traefik.http.middlewares.vps-screen-auth.basicauth.users=jt:\$apr1\$vnc12345\$NEW_HASH_HERE" \
  --label "traefik.http.routers.vps-screen.entrypoints=web,websecure" \
  --label "traefik.http.routers.vps-screen.middlewares=vps-screen-auth" \
  --label "traefik.http.routers.vps-screen.rule=Host(\`vnc.srv1056157.hstgr.cloud\`)" \
  --label "traefik.http.routers.vps-screen.tls=true" \
  --label "traefik.http.routers.vps-screen.tls.certresolver=mytlschallenge" \
  --label "traefik.http.services.vps-screen.loadbalancer.server.port=6080" \
  alpine/socat -d -d TCP-LISTEN:6080,fork,reuseaddr TCP:172.18.0.1:6080
```

### Pitfall: 502 Bad Gateway after container recreation
If the user reports "Bad Gateway" after recreating the container, the socat target is wrong. The original container used `TCP:host.docker.internal:6080` which fails because `host.docker.internal` doesn't resolve in the `root_default` Docker network without `--add-host host.docker.internal:host-gateway`. The fix is to use `TCP:172.18.0.1:6080` directly (the Docker bridge gateway IP where websockify listens).

The VNC password (second prompt, inside noVNC) is separate and stored at `/root/.vps-screen/password.txt`.

### User preference: simple passwords
When JT says "haz el usuario más sencillo" or asks for simpler credentials, change the Basic Auth password via the container recreation above. Use a short, memorable password (e.g., `viva`). Do NOT change the VNC password (second prompt) unless asked — that requires regenerating `x11vnc.pass`.

## Launching Google Chrome as non-root (for bot-protected sites)

Snap Chromium cannot run as non-root due to snap confinement, forcing `--no-sandbox` which is a bot detection signal. Use `google-chrome-stable` (.deb at `/usr/bin/google-chrome-stable`) instead — it has a proper SUID sandbox and runs fine as user `jt`.

```bash
# Grant X11 access to jt (once per session or after Xvfb restart)
xhost +SI:localuser:jt

# Launch as jt with sandbox enabled, GPU disabled (Xvfb has no GPU)
su - jt -c 'export DISPLAY=:99 && google-chrome-stable \
  --display=:99 \
  --disable-gpu \
  --no-first-run \
  --start-maximized \
  --proxy-server="http://127.0.0.1:8888" \
  --user-data-dir="/home/jt/.config/google-chrome-viva" \
  "https://target-site.com"'
```

Use a **separate profile directory** per task (e.g., `google-chrome-viva`) so sessions don't collide. Persistent profiles retain cookies across launches.

For sites with Akamai/bot protection, combine this with the mobile proxy pattern (see `navigate-bot-protected-sites` skill, `references/user-owned-mobile-egress.md`).

### Reading page content when vision and packages are unavailable

When `vision_analyze` returns 503 (provider down), `xdotool` console typing is unreliable, and `pip install websocket-client` is blocked by PEP 668, use **raw CDP via Python stdlib sockets** to execute JavaScript and read page content directly. This is the most reliable fallback for extracting structured data from a Chrome tab with `--remote-debugging-port` enabled. See `references/cdp-raw-websocket.md` for the full reusable technique, including navigate, evaluate, and data extraction patterns.

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
