---
name: bee-remote-connector
description: "Use when managing Bee wearable CLI or Claude connectors."
---

# Bee wearable and Claude

Use canonical npm package @beeai/cli, not unrelated Bee projects.
On this headless VPS, use BEE_FORCE_FILE_STORE=1: the installed secret-service keyring has no login collection. Credentials are under /root/.bee, mode 0600. Never print tokens. Login --no-wait creates a pairing link but does not finish token redemption; after owner approval run bee login, then verify authenticated retrieval.

Claude Code uses a user-scope stdio server named bee with command /usr/lib/node_modules/@beeai/cli/dist/platforms/linux-x64/bee, args mcp serve, env BEE_FORCE_FILE_STORE=1. Local configuration does not sync to other computers.

Claude browser/Desktop/mobile remote connector:
- HTTPS URL: https://bee.srv1056157.hstgr.cloud/mcp
- App /root/bee-remote/server.py, service bee-remote.service.
- Root-only bearer credential /root/bee-remote/connector-token. Add as required authorization request header in Claude custom connector, with value Bearer followed by token. Never embed credentials in URLs. No-sign-in selection means bearer header authentication, not anonymous access.
- Five allowlisted read-only tools. Auth middleware rejects all anonymous HTTP with 401, including tool routes.
- App binds only Docker gateway 172.18.0.1:9781. Edge bee-remote-proxy, root_default, IP 172.18.0.8; UFW only permits this edge to host port. Existing Traefik uses TLS resolver mytlschallenge.
- Test /root/bee-remote/.venv/bin/python /root/bee-remote/verify.py verifies public TLS, 401, initialize, exact tool list and a live read without printing personal data.
- Pin mcp<2 (currently 1.30.0) for FastMCP import; mcp 2 renamed that API.

For reading and organizing Bee history into Tasks/Calendar/Bitácora, follow `references/bee-digestion.md`.

Keep all credentials and personal Bee data out of public GitHub. Full encrypted Restic script /root/.local/sbin/hostinger-full-backup.sh includes Bee filesystem and restore comparisons of server.py, bearer token, Bee token and service unit. Inspect final status plus integrity and restore output before claiming backup complete.

The private Drive handoff package for the renamed agent **Stuart B 🐝** is under Bitácora `3-Resources/Stuart B 🐝`, folder ID `1wb7VNBIeZ3WZiLkDV0KMIkw9CxPjD_Yg`. It contains the identity, master prompt, architecture, operating manual, policy, schemas, current state, activation plan, security rules, sanitized cron definitions, code/tests, skills, compiled exports, latest conversation, and a private raw-source archive. Treat it as a consultation/transfer snapshot; the live source remains `/root/.hermes/bee-steward/`. Never include credentials, and verify every Drive upload by remote size + MD5 plus absence of public permissions.
