# 2026-06-12 cron backup: redacted credential copies + push verification

Context: scheduled cron job backing up `/root/.hermes` to `github.com:jomata28/hermes.trimagus` from `/root/backups/hermes.trimagus`.

## What happened

- The local repo already existed at `/root/backups/hermes.trimagus` and pulled cleanly with `git pull --ff-only`.
- `GITHUB_TOKEN` was not present in the cron process environment or `~/.hermes/.env`; the existing repo remote used SSH and `ssh -T git@github.com` authenticated successfully, so the push used SSH fallback.
- The first commit copied live `.env` and `config.yaml` too literally. GitHub push protection rejected it for detected OpenRouter, Groq, Notion, and GitHub PAT values.
- The fix was to amend the local-only commit after redacting secret values in the repository copies of `.env` and `config.yaml`, then push again.
- Push verification compared `git ls-remote origin refs/heads/main` to `git rev-parse HEAD`; they matched.

## Reusable lessons

- Cron may not inherit `GITHUB_TOKEN`; check it, but do not fail if SSH auth is already configured and works.
- Use `sqlite3.Connection.backup()` for memory DBs. Current Hermes may have `memory_store.db` instead of the legacy `memory.db`; backing up both names from `memory_store.db` improves restore compatibility.
- Exclude generated/recursive skill backup artifacts like `skills/.curator_backups/` unless explicitly requested.
- Keep tool output secret-safe: status and SHAs are fine; never print `.env` contents.

## Redaction pattern

1. Copy/sync live files into the repository working tree.
2. Rewrite only the repository copies of `.env` and `config.yaml`, replacing values for keys matching `api_key`, `token`, `secret`, `password`, `credential`, `client_secret`, etc. with `REDACTED_IN_BACKUP`.
3. Also regex-replace common token shapes (`sk-or-v1-*`, `gsk_*`, `github_pat_*`, `ghp_*`, Notion tokens, Slack tokens, bearer tokens) in non-obvious locations.
4. `git add -A`, commit or amend, `git push`, then verify remote SHA equals local SHA.

## Verification commands

```bash
git log -1 --oneline --decorate
remote_sha=$(git ls-remote origin refs/heads/main | awk '{print $1}')
local_sha=$(git rev-parse HEAD)
test "$remote_sha" = "$local_sha"
```
