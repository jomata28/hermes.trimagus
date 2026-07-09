# Private/paywalled platform auth via remote browser

Use this when a user needs Hermes to inspect private or paid content on a web/social/content platform (e.g. Substack) and direct unauthenticated fetch will not work.

## Recommended flow

1. Try the public URL first only if low-cost; expect paywalls/private posts to require login.
2. Start a temporary remote browser/noVNC flow and have the user type credentials themselves. Never ask for or repeat account passwords.
3. If reusing an existing VNC stack, verify which `x11vnc` process and password file are actually serving the public noVNC link before giving the user a password.
4. Prefer a separate, fresh VNC/websockify/cloudflared stack on unused ports for temporary auth when an old VPS-screen stack is already present. This avoids password-file mismatches.
5. After login, verify access by opening the specific private post/newsletter URL and extracting/reading only what the user asked for.
6. When finished, close public tunnel processes unless the user explicitly says to keep the remote view open.

## Durable pitfalls from Substack auth session

- **Password mismatch:** a new temp password is useless if the active `x11vnc` process is still using an old password file such as a VPS-screen password. Check process args and listening ports before sending credentials.
- **`pkill -f` self-match:** broad patterns can match the command runner itself and terminate the shell. Prefer explicit PIDs from `/proc`, narrower patterns, or separate fresh ports instead of killing by broad command text.
- **Invisible browser window:** Chromium may be running with a profile but have no visible/focused window on the X display, or the window may be partially off-screen. Check X windows (`xwininfo`/`wmctrl` if available) and move/resize with `xdotool` if needed.
- **Autoconnect links prove HTTP only:** an HTTP 200 from noVNC proves the web UI loads, not that the VNC password, window visibility, or target page is correct. Verify the actual desktop state when the user says they see a blank/static screen.

## Quick diagnostic checklist

- `pgrep -fa 'cloudflared|websockify|x11vnc|Xvfb|fluxbox|chrom(e|ium)'`
- `ss -tlnp | grep -E ':(5901|6080|5903|6082)\\b'`
- Inspect `x11vnc` args for `-rfbauth` path and port.
- Confirm noVNC HTTP 200 for the exact trycloudflare URL.
- Check windows on the X display (`xwininfo -root -children`, `wmctrl -l` when installed).
- If a large browser window is off-screen, move/resize it with `xdotool windowmove/windowresize`.
