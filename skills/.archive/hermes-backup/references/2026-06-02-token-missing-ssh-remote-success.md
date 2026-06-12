# 2026-06-02 cron backup: missing GITHUB_TOKEN, existing SSH remote succeeded

## Context

Scheduled backup request targeted `https://github.com/jomata28/hermes.trimagus.git` and explicitly asked to use `GITHUB_TOKEN` for authentication.

## Observed environment

- Local repo existed at `/root/backups/hermes.trimagus`.
- `GITHUB_TOKEN` was missing from the runtime environment.
- `~/.hermes/.env` did not contain an active `GITHUB_TOKEN` assignment.
- Existing remote was SSH:
  - fetch: `git@github.com:jomata28/hermes.trimagus.git`
  - push: `git@github.com:jomata28/hermes.trimagus.git`

## Working approach

1. Use existing local repo instead of recloning.
2. `git pull --ff-only origin main` first.
3. Copy requested Hermes artifacts with redaction:
   - `config.yaml`
   - `.env`
   - `skills/`
   - `memory_store.db` plus compatibility `memory.db`
   - `cron/jobs.json`
4. Exclude runtime/noisy files: cron output, caches, sessions, logs, `state.db`, `kanban.db`, lock/WAL/SHM files.
5. Scan backup tree for common token patterns before commit.
6. Commit with UTC timestamp.
7. Push using the already-authenticated SSH remote, since token auth was unavailable.
8. Verify with all three:
   - `git log --oneline -1 HEAD`
   - `git log --oneline -1 origin/main`
   - `git ls-remote origin refs/heads/main`

## Lesson

When a user requests `GITHUB_TOKEN` but the token is absent, a cron backup should still complete if an existing SSH remote can push. Do not fail solely because the preferred auth mechanism is unavailable. Report the fallback clearly in the final backup report.
