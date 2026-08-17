# User-Owned Mobile Egress for a Shared VPS Browser

Use this when a real visible browser on a VPS loads a site's shell/homepage but a sensitive API call returns a WAF 403 because the VPS/datacenter network is distrusted. This is a legitimate network handoff through the user's own mobile connection, not a rotating-proxy or bot-evasion scheme.

## Diagnose before changing browsers

A generic frontend modal such as “service unavailable” is not enough. Determine whether the failure is inventory/business logic or WAF/network rejection.

1. Inspect rendered text and resource timing from the visible browser/CDP session.
2. Look specifically for the business endpoint and its `responseStatus`:

```javascript
performance.getEntriesByType('resource')
  .filter(e => e.name.includes('/availability/') || e.name.includes('/api/'))
  .map(e => ({ url: e.name, status: e.responseStatus || 0, duration: e.duration }))
```

3. Check analytics/error metadata for explicit signals such as `WAF_BLOCKED_ERROR`.
4. Compare host IPv4 and IPv6 reputation separately. A search engine block notice on the VPS network is corroborating evidence, not proof by itself.
5. Do not interpret a 403 as “no inventory.” A genuine no-results response normally comes from the application API with a successful HTTP response.

### Browser hygiene before changing egress

Try the legitimate browser fixes once, with verification after each:

- Run the visible browser as a non-root Linux user in a real PAM/systemd session so its sandbox remains enabled.
- **Never use `--no-sandbox`** — Akamai detects the "unsupported command line flag: no sandbox" console warning and uses it as a bot fingerprint. The user identified this directly as the cause of persistent blocking.
- **Use `google-chrome-stable` (.deb) not snap chromium** on the VPS. Snap chromium cannot run as non-root due to snap confinement, which forces `--no-sandbox`. The .deb Chrome has a proper SUID sandbox (`/opt/google/chrome/chrome-sandbox`) and runs fine as user `jt`. Launch pattern:
  ```bash
  xhost +SI:localuser:jt  # grant X11 access (once per session)
  su - jt -c 'export DISPLAY=:99 && google-chrome-stable \
    --display=:99 --disable-gpu --no-first-run --start-maximized \
    --proxy-server="http://127.0.0.1:8888" \
    --user-data-dir="/home/jt/.config/google-chrome-viva" "URL"'
  ```
- Use a persistent profile, normal locale, cookies, and navigation from the homepage.
- If IPv6 reputation is independently bad, test IPv4-only egress without changing unrelated host traffic.

If the same sensitive endpoint still returns an explicit WAF 403 across those variants, stop cycling browser flags. The remaining variable is usually network reputation.

## Android mobile-proxy pattern

### Phone side

1. Disable Wi-Fi if the goal is to use mobile carrier egress.
2. Start a user-controlled HTTP proxy app such as Every Proxy on `127.0.0.1:8080` (or its documented local bind).
3. Keep the proxy app and SSH client active.
4. Create a reverse SSH tunnel from Android to the VPS:

```bash
ssh -N -R 127.0.0.1:8888:127.0.0.1:8080 USER@VPS
```

Termius can create the same **Remote Port Forward**:

- remote/bind address: `127.0.0.1`
- remote port: `8888`
- destination host: `127.0.0.1`
- destination port: `8080`

### VPS SSH policy

Use the narrowest forwarding policy:

```text
AllowTcpForwarding remote
GatewayPorts no
```

Validate before reload:

```bash
sshd -t
systemctl reload ssh
sshd -T | grep -E '^allowtcpforwarding|^gatewayports'
```

`GatewayPorts no` is important: the reverse-forwarded proxy must bind only to VPS localhost, never a public interface.

### Verify the tunnel before launching the browser

```bash
ss -ltnp | grep ':8888 '
curl --max-time 15 -x http://127.0.0.1:8888 https://api.ipify.org
```

The returned address should differ from the VPS address and correspond to the user's mobile/residential egress. If the first request works and later requests stall, check that Android did not suspend the proxy or Termius session.

### Launch the shared browser

Run the browser as the normal desktop user and point only that browser at the tunnel:

```bash
# On the Hermes VPS: use google-chrome-stable (.deb), NOT snap chromium.
# Snap chromium can't run as non-root → forces --no-sandbox → Akamai detects it.
xhost +SI:localuser:jt  # grant X11 access (once per session)

su - jt -c 'export DISPLAY=:99 && google-chrome-stable \
  --display=:99 \
  --disable-gpu \
  --no-first-run \
  --start-maximized \
  --proxy-server="http://127.0.0.1:8888" \
  --user-data-dir="/home/jt/.config/google-chrome-viva" \
  "https://www.vivaaerobus.com/es-mx"'
```

On a normal desktop with `google-chrome-stable` in PATH:

```bash
google-chrome-stable \
  --proxy-server=http://127.0.0.1:8888 \
  --user-data-dir="$HOME/.config/chrome-mobile-egress" \
  --start-maximized 'https://target.example/'
```

Use a **separate profile directory** (e.g., `viva-proxy-profile`) so the proxied browser session doesn't collide with the non-proxied profile. Persistent profiles retain Akamai cookies across sessions, reducing re-challenge frequency.

Do not route the whole VPS through the phone. Browser-scoped proxying preserves SSH/gateway stability.

### Confirmed working: Viva Aerobus (2026-08-16)

Mobile proxy tunnel deployed and verified:
- Every Proxy on Android → reverse SSH tunnel via Termius → VPS `127.0.0.1:8888`
- Egress IP: `76.143.90.155` (residential, US-based carrier)
- Chromium launched with `--proxy-server=http://127.0.0.1:8888`
- Viva homepage loaded successfully (window title: "Sitio Oficial Viva | Boletos avión | Vuelos baratos")
- Previously blocked from VPS datacenter IP (Akamai 403 Access Denied)
- The `plannedFlights` and `stations` API endpoints work from VPS without proxy (tier 1 public), but `booking/full`, `availability/search`, and authenticated endpoints need the proxied browser session

## Latency and verification discipline

Mobile reverse tunnels can take 30–60 seconds to render asset-heavy SPAs. A blank page or persistent loader is not yet failure.

- Keep the tunnel alive and wait deliberately.
- Verify the page title and rendered DOM.
- Re-check the exact business endpoint status.
- Declare success only when the formerly blocked endpoint returns 2xx and real application data renders.
- Declare tunnel failure when the localhost proxy test itself times out or the listening socket disappears.

## Safety boundaries

- Use only a connection/proxy controlled by the user.
- Do not use this workflow to automate purchases, exploit refunds, generate credits, bypass account authorization, or evade enforcement after access has been explicitly revoked.
- Keep irreversible transactions manual and user-approved.
- Never expose the reverse proxy publicly or persist website credentials in scripts/logs.
