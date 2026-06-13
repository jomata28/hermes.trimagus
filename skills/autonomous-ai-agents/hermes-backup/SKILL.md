---
name: hermes-backup
description: "Back up ~/.hermes to a git/GitHub repository while handling selective file sync, redacted credential copies, push protection, auth fallback, and verification."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [hermes, backup, github, git, cron, secrets, disaster-recovery]
---

# Hermes Backup

Use this skill when backing up `~/.hermes` or a Hermes profile directory to a git/GitHub repository, especially from a scheduled cron job.

## Goals

Back up the durable Hermes state needed for recovery without dumping noisy caches or leaking live secrets:

- `config.yaml`
- `.env` as a **redacted backup copy** unless the user explicitly requests raw secrets and accepts push-protection risk
- `skills/`
- memory database (`memory_store.db`; optionally also legacy `memory.db`)
- `cron/jobs.json` or legacy `cron/jobs/`

## Workflow

1. **Locate or clone the repository.** Prefer `/root/backups/<repo>` if present, otherwise `/tmp/<repo>`. If cloning, use the user-provided URL.
2. **Sync first.** In an existing clone, run `git pull --ff-only` before copying files.
3. **Copy selected live files into the repo working tree.** Do not copy sessions, logs, caches, image/audio artifacts, sandboxes, WhatsApp state, or Hermes source checkouts unless explicitly requested.
4. **Use SQLite online backup for memory DBs.** Current Hermes commonly uses `~/.hermes/memory_store.db`; legacy prompts may say `memory.db`. Back up `memory_store.db` and, when useful for compatibility, refresh `memory.db` from it.
5. **Redact credential values in repository copies only.** Replace values in `.env` and `config.yaml` for secret-like keys (`api_key`, `token`, `secret`, `password`, `credential`, `client_secret`, etc.) with `REDACTED_IN_BACKUP`. Never edit the live `~/.hermes` credential files just to satisfy backup push protection.
6. **Commit with a timestamp message.** Example: `Backup Hermes 2026-06-12 03:02:14 UTC`.
7. **Push and verify.** Run `git push`, then verify `git ls-remote origin refs/heads/main` matches `git rev-parse HEAD`; also show `git log -1 --oneline --decorate`.

## Auth and push protection pitfalls

- Scheduled cron environments may not include `GITHUB_TOKEN` even when the prompt says to use it. Check first. If it is absent but the repo remote is SSH and `ssh -T git@github.com` succeeds, use the existing SSH auth and report that fallback.
- GitHub push protection rejects commits containing recognized tokens, even in backup repositories. If a push is rejected for secrets, amend the local commit with redacted backup copies and push again. Do not force push unless the rejected commit already reached the remote, which push protection usually prevents.
- Keep command output secret-safe: show paths, status, commit messages, and SHAs, but do not print `.env` or credential values.

## Exclusions

Recommended `.gitignore` patterns for Hermes backups:

```gitignore
cache/
sessions/
sandboxes/
images/
image_cache/
audio_cache/
logs/
cron/output/
*.db-shm
*.db-wal
*.pid
*.lock
*.log
hermes-agent/
bin/
plugins/
hooks/
pastes/
whatsapp/
state.db*
kanban.db
__pycache__/
*.pyc
skills/.curator_backups/
```

`skills/.curator_backups/` is a recursive/generated backup artifact; exclude it unless the user explicitly asks for curator snapshots.

## References

- `references/2026-06-12-cron-redacted-backup-push.md` — cron backup run with missing `GITHUB_TOKEN`, SSH fallback, GitHub push protection rejection, redaction/amend, and remote SHA verification.
