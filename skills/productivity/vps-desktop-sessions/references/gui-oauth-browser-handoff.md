# GUI OAuth browser handoff on the VPS desktop

Use this when a packaged desktop app says it will open a browser for sign-in, but the browser never appears, the app stays on “waiting for your browser,” or the browser reports that it cannot connect back to the application.

## Diagnose three separate layers

1. **Desktop/app layer**
   - Verify `vps-screen.service`, `DISPLAY=:99`, and actual geometry with `xdpyinfo`.
   - Confirm the GUI app process is alive.
   - Enumerate X windows by class, not title alone. Tauri/WebKit windows can have an empty title:
     ```bash
     DISPLAY=:99 xprop -root _NET_CLIENT_LIST
     DISPLAY=:99 xdotool search --onlyvisible --name '.*' | while read w; do
       DISPLAY=:99 xprop -id "$w" WM_CLASS WM_NAME _NET_WM_NAME
     done
     ```
   - Bring the app forward with `xdotool windowactivate` before clicking.

2. **External browser layer**
   - Inspect handlers:
     ```bash
     xdg-mime query default x-scheme-handler/https
     DISPLAY=:99 xdg-settings get default-web-browser
     ```
   - Test the handler with a harmless URL before retrying OAuth.
   - On this root-run VPS, Snap Chromium needs both `--no-sandbox` and a profile inside Snap’s allowed tree. A launcher using `/root/.hidden/profile` can fail even when Chromium itself is installed.

3. **Relay/callback layer**
   - Treat `relay unreachable` as a separate claim from “browser did not open.”
   - Extract the exact auth/relay hostnames from app logs or binary strings, then test DNS, HTTPS, and TLS directly.
   - If login endpoints and relays are reachable but the app died, restart the app first. A browser callback cannot complete when the desktop app’s local listener is gone.

## Known-good Snap Chromium launcher

Create `~/.local/share/applications/<app>-chromium.desktop`:

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Chromium for GUI OAuth
Exec=/usr/bin/chromium-browser --no-sandbox --disable-dev-shm-usage --user-data-dir=/root/snap/chromium/common/gui-oauth-browser %U
Icon=chromium-browser
Terminal=false
Categories=Network;WebBrowser;
MimeType=text/html;x-scheme-handler/http;x-scheme-handler/https;
StartupNotify=true
```

Then register it:

```bash
update-desktop-database ~/.local/share/applications || true
xdg-mime default <app>-chromium.desktop x-scheme-handler/http
xdg-mime default <app>-chromium.desktop x-scheme-handler/https
xdg-mime default <app>-chromium.desktop text/html
DISPLAY=:99 xdg-settings set default-web-browser <app>-chromium.desktop || true
```

Launch a harmless test URL with the same desktop launcher and confirm a visible Chromium window before asking the app to start OAuth again.

## Recovering a dead virtual display

If `xdpyinfo` cannot open `:99` and `vps-screen.service` is stuck in `deactivating`, inspect `systemctl status` and `journalctl -u vps-screen.service`, then restart the service and wait until these exist:

- `Xvfb :99`
- `fluxbox -display :99`
- `x11vnc` on 5901
- websockify/noVNC on 6080

Do not relaunch the GUI app until `DISPLAY=:99 xdpyinfo` succeeds.

## Credential boundary

- It is fine to enter a user-supplied email when explicitly authorized.
- Never ask the user to paste a password, recovery code, or 2FA secret into chat. Stop at the password/verification screen and have the user enter it directly in noVNC.
- Delete screenshots containing email addresses, OAuth state parameters, or credentials after inspection.

## Verification

OAuth is not complete merely because the browser opened. Verify all of the following:

1. Browser reaches the expected HTTPS login domain.
2. User completes password/2FA privately.
3. Provider redirects successfully.
4. Desktop app leaves “waiting for your browser.”
5. App remains running and records an authenticated/community state.
