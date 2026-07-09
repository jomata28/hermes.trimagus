# Substack private/paid content auth via remote browser

Use when JT wants Hermes to read a private/paid Substack post or newsletter and the public URL is inaccessible.

## Safe access pattern

1. Ask for or use the Substack post/newsletter URL when available.
2. Try public access first if practical; paid/private content usually requires auth.
3. For auth, use a temporary remote browser/noVNC session so JT enters credentials directly. Do **not** ask him to send passwords or magic-link contents in chat.
4. Prefer the existing VPS screen stack if already running:
   - `Xvfb :99`
   - `fluxbox -display :99`
   - `x11vnc` bound to localhost on `5901`
   - `websockify` exposing noVNC on the Docker bridge / local interface, commonly `172.18.0.1:6080`
5. Open Chromium on the display with an isolated profile for Substack, e.g.:
   - `DISPLAY=:99 chromium --no-sandbox --disable-dev-shm-usage --user-data-dir=/tmp/substack-chromium-profile https://substack.com/sign-in`
6. Expose noVNC only temporarily with Cloudflare quick tunnel:
   - `cloudflared tunnel --url http://172.18.0.1:6080 --no-autoupdate`
7. Give JT the noVNC URL and tell him to use the VPS screen/noVNC password if prompted. Do not reveal or persist password values in summaries.
8. After JT says he is logged in, verify access to the requested post/newsletter, extract/summarize only what is needed, then close the tunnel unless he explicitly wants the view kept open.

## Security / privacy notes

- Never ask JT to paste Substack credentials into chat.
- Redact any VNC/noVNC passwords, cookie values, Google/Substack account tokens, and URL query parameters that contain credentials.
- A public Cloudflare quick tunnel is temporary but still exposes the noVNC endpoint. Shut it down after auth/content access.
- Distinguish between stopping the tunnel/login browser and invalidating the authenticated session: closing the remote-view tunnel does not necessarily remove the browser profile/cookies.

## Common pitfalls

- Do not assume private Substack can be fetched through normal unauthenticated web tools.
- If a previous noVNC stack is already running, inspect/reuse it instead of spawning conflicting `x11vnc`/`websockify` instances on the same ports.
- If password entry fails on mobile, offer the non-autoconnect noVNC URL and remind JT to click into the password field; the actual password may be the VPS screen password rather than a newly generated one.
