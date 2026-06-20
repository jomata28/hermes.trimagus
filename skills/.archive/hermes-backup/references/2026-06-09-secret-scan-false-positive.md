# 2026-06-09 Cron Backup: Secret Scan False Positives

During a scheduled backup to `jomata28/hermes.trimagus`, the copy/redaction script initially failed its pre-commit scan because a broad regex matched any line containing `api_key`, `token`, or `secret`, even when the value was already `REDACTED`.

## What happened

- The backup copied/redacted `config.yaml`, `.env`, `skills/`, `cron/jobs.json`, and SQLite memory backups.
- A line regex like this produced false positives:
  - `(?im)^\s*[A-Za-z0-9_.-]*(?:TOKEN|SECRET|PASSWORD|API[_-]?KEY|...).*\s*[:=]\s*(?!REDACTED\s*$|$).+`
- It matched lines such as:
  - `api_key: REDACTED`
  - `token: REDACTED`
  - prose lines containing `secrets`
  - skill examples with placeholder `api_key = ...`

## Durable fix

Use two different checks:

1. **Literal-token scan across all copied text files** — actual high-risk token shapes only:
   - `github_pat_[A-Za-z0-9_]{20,}`
   - `ghp_[A-Za-z0-9]{20,}` / `gho_...` / `ghs_...`
   - `ntn_[A-Za-z0-9]{20,}`
   - `sk-[A-Za-z0-9_-]{20,}`
   - `AKIA[0-9A-Z]{16}`
   - `AIza[0-9A-Za-z_-]{20,}`

2. **Secret-shaped key assignment scan only for `config.yaml` and `.env`** — parse each non-comment line as `key: value` or `key=value`; only flag when the key itself matches a secret-shaped name and the value is non-empty and not exactly `REDACTED`.

Do **not** run broad secret-key assignment scans over `skills/`; skill docs and code examples commonly include placeholder names like `api_key`, and those false positives block clean cron runs.

## Verification from the run

After switching to parsed key/value scanning for `config.yaml`/`.env` and literal-token scanning everywhere else, the backup completed, committed, pushed, and verified remote `main` at commit `308bc8471c6947aff1ad5e47096a91e916f3659a`.
