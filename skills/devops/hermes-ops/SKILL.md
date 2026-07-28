---
name: hermes-ops
description: "Operate JT's Hermes VPS deployment: gateway lifecycle (PM2), model/provider switching, API keys, private-login browser sessions."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, ops, gateway, models, providers, vps]
    related_skills: [hermes-agent, agent-teams]
---

# Hermes Ops — JT's Deployment

Operating procedures for THIS Hermes instance (Hostinger VPS). For generic Hermes usage/config, load the bundled `hermes-agent` skill — it stays authoritative; this skill holds deployment-specific ops lessons.

## When to use

- JT asks to add/rotate an API key or switch the Hermes model/provider
- Gateway restart/status is needed
- JT needs a private-login browser session (he logs into his own accounts; agent reads after)

## Model / provider switching

1. Add the key to `/root/.hermes/.env`. When a provider has two common env names, set both (e.g. `KIMI_API_KEY` + `MOONSHOT_API_KEY`).
2. Verify the key BEFORE switching (e.g. Moonshot: `GET https://api.moonshot.ai/v1/models` with Bearer — expect 200).
3. Switch config:
   ```bash
   hermes config set model.provider <slug>      # Kimi/Moonshot slug: kimi-coding
   hermes config set model.default <model-id>   # e.g. kimi-k3
   hermes config set model.base_url <url>       # e.g. https://api.moonshot.ai/v1
   hermes config set model.api_mode chat_completions
   ```
4. **No gateway restart needed**: model/provider config is re-read per session — a new session comes up on the new model even with the same gateway PID. Only restart if behavior demands it.
5. Only change model/provider when JT explicitly asks.

## Gateway lifecycle

- Gateway runs under **PM2** (process name `hermes`, script `/root/.hermes/start-gateway.sh`): `pm2 list`, `pm2 logs hermes`.
- Dashboard is separate: systemd `hermes-dashboard.service` (127.0.0.1:9119).
- **Restart from inside the gateway is blocked** ("cannot restart or stop the gateway from inside the gateway process" — SIGTERM would kill the command itself). Options:
  - JT sends `/restart` in chat (preferred), or
  - External shell: `pm2 restart hermes` with `HOME=/root`.
- Pitfall: `systemd-run ... pm2 restart hermes` spawns with `PM2_HOME=/etc/.pm2` → fresh daemon → "Process or Namespace hermes not found". Set `PM2_HOME=/root/.pm2` explicitly if scripting restarts.

## Private-login browser sessions (JT logs in himself)

1. `systemctl start vps-screen.service` (Xvfb :99 + x11vnc 5901 + noVNC proxy 6080).
2. Launch the login page: `terminal(background=true)` → `DISPLAY=:99 chromium --no-sandbox --disable-dev-shm-usage --start-maximized <url>`.
3. Send JT: `https://vnc.srv1056157.hstgr.cloud/vnc.html?autoconnect=true&resize=scale&path=websockify` + password from `/root/.vps-screen/basic-auth-password.txt` (his own server credential — DM delivery is the established pattern; never store it in memory/skills).
4. JT logs in (Claude.ai, ORA, etc.) and tells you when done; then read the screen (`DISPLAY=:99 xwd -root -out /tmp/screen.xwd`) or drive the page.
5. Setup details live in bundled `hermes-agent` skill → `references/persistent-vps-screen.md`.

## Security rules

- Never echo API keys/secrets back in chat, files, or memory — redact as `[REDACTED]`.
- Verify new keys work before pointing config at them; keep prior provider config intact as fallback.

## References

- `references/gateway-model-ops.md` — session-derived detail: Kimi K3 switch (2026-07-25), restart-block behavior, PM2_HOME pitfall, observed env/config values.
