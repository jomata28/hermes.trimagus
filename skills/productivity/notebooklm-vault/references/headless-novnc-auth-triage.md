# Headless noVNC auth: password/port mismatch triage

Use this when exposing a remote browser through Xvfb + x11vnc + websockify + cloudflared for user login, and the user reports that the password does not work or the browser is not visible.

## Fast diagnosis

1. Inspect live processes and listening ports before rotating passwords:
   - `pgrep -fa 'cloudflared|websockify|x11vnc|Xvfb|fluxbox|chrom(e|ium)'`
   - `ss -tlnp | grep -E ':(5901|6080|5903|6082)\b'`
2. Identify which `x11vnc` process is actually bound to the port behind the public URL.
3. Check the active `-rfbauth` file in that process command. The password users need is for the *live x11vnc process*, not the password file you just generated.
4. Verify the noVNC HTTP page returns 200 before sending a link.

## If password rotation does not take

A common failure mode is starting a new `x11vnc` while an older one is still bound to the intended port. The public websockify/cloudflared link may continue targeting the old server and old password.

Safer fix:

1. Leave the existing local-only VPS screen alone if it is needed.
2. Start a separate temporary auth stack on fresh ports, for example:
   - VNC: `5903`
   - websockify: `6082`
   - cloudflared: `http://172.18.0.1:6082`
3. Generate/store a new temporary password file for that new x11vnc instance.
4. Verify:
   - `ss -tlnp` shows `5903` for the expected x11vnc PID.
   - `ss -tlnp` shows `6082` for websockify targeting `5903`.
   - The trycloudflare `vnc.html` URL returns HTTP 200.

## If the user sees a blank desktop / nothing moving

Chromium may be running but not mapped as a visible X window.

1. Inspect windows:
   - `DISPLAY=:99 xwininfo -root -children`
   - `DISPLAY=:99 wmctrl -l` if available.
2. Capture a screenshot when needed:
   - `ffmpeg -y -f x11grab -video_size 1440x950 -i :99 -frames:v 1 /tmp/screen.png`
3. If the browser window is off-screen, install/use `xdotool` if available:
   - `DISPLAY=:99 xdotool windowmove <window_id> 0 0`
   - `DISPLAY=:99 xdotool windowsize <window_id> 1440 930`
   - `DISPLAY=:99 xdotool windowactivate <window_id>`
4. If Chromium has processes but no visible window, restart it with a clean profile lock removal and explicit X11 flags:
   - `--no-sandbox --disable-dev-shm-usage --disable-gpu --ozone-platform=x11 --no-first-run --new-window <url>`

## Cleanup

After auth/work is complete:

- Kill public `cloudflared` quick tunnels.
- Kill the temporary VNC/websockify stack on the temporary ports.
- Leave normal local-only VPS screen processes running unless the user explicitly asks to stop them.
- Do not send or preserve credential values in summaries; redact passwords/tokens/cookies.
