# Hermes dashboard behind Traefik with persistent cookie auth

Current verified deployment for JT's Hostinger VPS. This supersedes the original September 3 Basic-Auth/Host-rewrite recipe.

## Topology

- Hermes dashboard: systemd `hermes-dashboard.service`, bound only to `127.0.0.1:9119`.
- Host bridge: `hermes-dashboard-bridge.service`, `172.18.0.1:9119` → `127.0.0.1:9119`.
- Edge: `hermes-dashboard-proxy`, `alpine/socat`, fixed IP `172.18.0.6` on `root_default`.
- Traefik: `root-traefik-1`, TLS and routing for `hermes.srv1056157.hstgr.cloud`.
- Recovery: `hermes-dashboard-healthcheck.timer` runs every two minutes and restarts the dashboard after two consecutive failed status probes.

## Authentication boundary

Authentication belongs to Hermes's bundled `dashboard_auth/basic` provider, not Traefik's browser Basic Auth.

Canonical configuration:

- `dashboard.public_url`: exact public HTTPS URL. This both allows the exact public Host and engages the dashboard auth gate despite a loopback bind.
- `dashboard.trusted_proxies`: exact edge container IP (`172.18.0.6`).
- `HERMES_DASHBOARD_BASIC_AUTH_USERNAME`: operator username.
- `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH`: scrypt hash; never store plaintext.
- `HERMES_DASHBOARD_BASIC_AUTH_SECRET`: stable random signing key so cookies survive restarts.
- `HERMES_DASHBOARD_BASIC_AUTH_TTL_SECONDS`: 30-day access-token lifetime for this single-user deployment.

The edge router has no `basicauth` middleware and no Host-rewrite middleware. It preserves `Host: hermes.srv1056157.hstgr.cloud`; Hermes accepts that exact host from `public_url` and rejects other non-loopback hosts.

## Safe migration order

Never remove Traefik Basic Auth first.

1. Back up `~/.hermes/config.yaml` and `~/.hermes/.env` with mode 600.
2. Generate the scrypt password hash and stable signing secret without printing either.
3. Set `dashboard.public_url` and the exact trusted proxy IP.
4. Restart `hermes-dashboard.service` and wait for the real `127.0.0.1:9119` listener; startup recompiles the web UI and may take tens of seconds.
5. While old edge Basic Auth still exists, verify:
   - `/api/status` reports `auth_required=true`, `auth_providers=["basic"]`.
   - `/` redirects to `/login` after edge auth.
   - `POST /auth/password-login` sets `Secure`, `HttpOnly`, `SameSite=Lax` cookies.
   - `/api/auth/me` and `/` return 200 with that cookie jar.
6. Recreate only `hermes-dashboard-proxy`, pinning it to `172.18.0.6`, without the former Basic Auth and Host-rewrite labels.
7. Verify the final boundary:
   - anonymous `/` → 302 `/login`;
   - anonymous `/kanban` → 302 `/login?next=%2Fkanban`;
   - anonymous sensitive API such as `/api/config` → 401;
   - valid cookie login → dashboard 200;
   - no `WWW-Authenticate` browser popup;
   - invalid Host on `/login` → 400;
   - unmatched public Traefik Host → 404.
8. Restart the dashboard while retaining the cookie jar and prove `/api/auth/me` remains 200 afterward.

## Reliability

The dashboard process can remain alive after losing its listener, so `systemctl is-active` alone is insufficient. The health script probes the public-host shape locally and requires JSON containing `"auth_required":true`. It tolerates one miss, restarts after two, and waits up to 180 seconds for the Vite build plus listener recovery.

Verify:

```bash
systemctl is-active hermes-dashboard.service \
  hermes-dashboard-bridge.service \
  hermes-dashboard-healthcheck.timer
ss -ltnp | grep 9119
systemctl list-timers hermes-dashboard-healthcheck.timer --no-pager
```

Healthy listeners are `127.0.0.1:9119` (Hermes) and `172.18.0.1:9119` (socat bridge). A healthy watchdog leaves no `/run/hermes-dashboard-watchdog.failures` file.

## Security invariants

- Never bind the primary dashboard publicly to avoid the reverse proxy.
- Never put username, password, cookie, hash, or signing secret in ARX or a repository.
- Do not weaken the Host validator.
- Preserve the fixed proxy IP or update `dashboard.trusted_proxies` before recreating it at another address.
- Keep TLS at Traefik and cookie flags `Secure`, `HttpOnly`, `SameSite=Lax`.
