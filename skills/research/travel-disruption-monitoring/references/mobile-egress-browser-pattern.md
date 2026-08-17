# Mobile-Egress Pattern for Shared Airline Browsers

Use this when a shared browser on a VPS can load an airline homepage but a protected availability/checkout API returns an edge/WAF block.

## Diagnose before changing networks

1. Record the exact failing endpoint, HTTP status, and structured error body. Distinguish WAF rejection from “no inventory” or application downtime.
2. Retest with a normal unprivileged browser user, active sandbox, persistent profile, coherent locale, and navigation from the homepage.
3. Compare IPv4 and IPv6 reputation. A blocked IPv6 may be avoidable by routing only that browser user over IPv4.
4. Try an official stable browser build if the distro Chromium fingerprint is unusual.
5. If the protected endpoint still returns an explicit WAF error, stop cycling cosmetic browser flags. Treat datacenter egress as the remaining variable.

A user frustration signal such as “there has to be a way” should trigger a broader network-path search rather than an early fallback to manual-only operation.

## Private Android egress via reverse SSH

This keeps the visible browser on the VPS while outbound web traffic uses the user’s own Android/mobile connection.

```text
Chrome on VPS
  -> HTTP proxy 127.0.0.1:8888 on VPS
  -> SSH remote forward
  -> Android local proxy 127.0.0.1:8080
  -> mobile data
  -> airline site
```

### VPS SSH hardening

Allow reverse forwarding but keep the listener localhost-only:

```sshconfig
AllowTcpForwarding remote
GatewayPorts no
```

Validate before reload:

```bash
sshd -t
systemctl reload ssh
sshd -T | grep -E '^allowtcpforwarding|^gatewayports'
```

Expected:

```text
allowtcpforwarding remote
gatewayports no
```

Do not expose the proxy port publicly. The remote forward should bind `127.0.0.1`, not `0.0.0.0`.

### Android side

1. Disable Wi-Fi if mobile egress is desired.
2. Start an HTTP proxy app such as Every Proxy on Android port `8080`.
3. In an SSH client that supports remote forwarding, create:
   - remote bind address: `127.0.0.1`
   - remote port: `8888`
   - destination host: `127.0.0.1`
   - destination port: `8080`
4. Keep both the proxy app and SSH forwarding session alive.

Equivalent OpenSSH command from Android/Termux:

```bash
ssh -N -R 127.0.0.1:8888:127.0.0.1:8080 user@vps
```

### Verify before launching the browser

```bash
ss -ltnp | grep ':8888 '
curl --max-time 15 -x http://127.0.0.1:8888 https://api.ipify.org
```

The reported IP must differ from the VPS datacenter IP. A listener alone is insufficient; verify end-to-end egress.

Launch the visible browser as an unprivileged user:

```bash
google-chrome-stable \
  --proxy-server=http://127.0.0.1:8888 \
  --no-first-run \
  --no-default-browser-check \
  --user-data-dir=/home/USER/.config/browser-mobile-egress \
  https://www.example-airline.com/
```

Verify the protected request itself returns success; a rendered homepage is not proof. Keep the phone proxy/tunnel open throughout the shared-browser session.

## Safety boundary

Use this pattern to restore ordinary access through the user’s own network, not to rotate identities, evade fraud controls, scrape aggressively, or exploit checkout systems. Do not automate purchasing, reservation creation, payment-reference generation, credit manipulation, or loyalty-balance tampering.
