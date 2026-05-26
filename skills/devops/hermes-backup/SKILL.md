---
name: hermes-backup
category: devops
description: Back up ~/.hermes to a git repository — handle auth, secret scanning, and selective file backup for disaster recovery.
tags: [backup, git, github, hermes, cron, secrets]
trigger: "Back up ~/.hermes to a git remote, push Hermes state to GitHub, or any scheduled backup of the Hermes agent directory."
---

# Hermes Backup to Git

Backup the ~/.hermes directory to a git repository, typically for disaster recovery or state preservation across environment changes.

## Steps

1. **Check repo existence locally** — If the backup repo exists, `cd` into it and `git pull` to sync. If not, clone first.

2. **Copy key files** from `~/.hermes/`:
   - `config.yaml` — Hermes configuration
   - `.env` — environment variables and API keys (see Secrets section)
   - `memory_store.db` — persistent memory
   - `skills/` — all custom skills
   - `cron/jobs.json` and `cron/output/` — cron job definitions and output history

3. **Create `.gitignore`** to exclude caches, sessions, and ephemeral files:
   - `cache/`, `sessions/`, `sandboxes/`, `images/`, `image_cache/`, `audio_cache/`
   - `*.db-shm`, `*.db-wal`, `*.pid`, `*.lock`, `*.log`
   - `hermes-agent/`, `bin/`, `plugins/`, `hooks/`, `pastes/`, `whatsapp/`
   - Checkpoints, pairing, logs, and memory directories
   - JSON caches: `models_dev_cache.json`, `ollama_cloud_models_cache.json`, `.skills_prompt_snapshot.json`
   - State databases: `state.db*`, `kanban.db`

4. **Scan for secrets before push** — See Secrets section below.

5. **Commit with timestamp**: `git commit -m "hermes backup: <items> — $(date -u '+%Y-%m-%d %H:%M UTC')"`

6. **Push** — See Auth section below.

7. **Verify**: `git log --oneline -1` to confirm the commit exists.

## Auth — GITHUB_TOKEN is Often Empty

The `GITHUB_TOKEN` environment variable is frequently empty or commented out in `~/.hermes/.env`. **Always verify before relying on HTTPS token auth:**

```bash
if [ -z "$GITHUB_TOKEN" ]; then
    # Fall back to SSH
    git remote set-url origin git@github.com:<user>/<repo>.git
    git push origin main
else
    git remote set-url origin "https://<user>:${GITHUB_TOKEN}@github.com/<user>/<repo>.git"
    git push origin main
fi
```

Git credential helpers (especially `gh auth git-credential`) can interfere with token-embedded HTTPS URLs. If HTTPS auth fails with "Invalid username or token", switch to SSH.

## Secrets — GitHub Push Protection Will Block You

GitHub's secret scanning blocks pushes containing detected secrets. This applies to:

- **`.env` files** — Contains API keys (OpenRouter, Groq, Notion, etc.). **Exclude from the commit entirely** by adding to `.gitignore` and running: `git rm --cached .env`

- **`config.yaml`** — May contain `github.token`, provider API keys. Redact before committing:
  ```bash
  sed -i 's/token: .*/token: REDACTED/' config.yaml
  ```

- **`skills/` directory** — SKILL.md files sometimes contain live example tokens scanned by GitHub (e.g., Notion `ntn_*` keys in code blocks). Scan and redact any `ntn_`, `sk-`, `ghp_`, `github_pat_`, `groq-` patterns found in text.

- **After amending the commit** (without secrets), push with `git push` — do NOT use `--force-with-lease` in cron mode. The original push was rejected by GitHub (commit never landed), so the remote hasn't moved. `--force-with-lease` triggers an interactive approval guard that cron jobs can't pass. A plain `git push origin main` works after the amend.

- **Fix the source too**: When GitHub blocks a backup due to secrets in `~/.hermes/skills/`, the same tokens will block the next backup. After redacting in the backup copy, also redact in the live `~/.hermes/skills/` files. Use a real-token regex like `ntn_[A-Za-z0-9]{20,}` to match actual tokens, not placeholders like `ntn_your_key_here`.

## Pitfalls

- **Empty GITHUB_TOKEN**: The env var is commonly commented out in `.env`. Check before building URLs with it.
- **Credential helper interference**: `gh auth git-credential` overrides token-embedded HTTPS URLs. Use SSH as fallback when HTTPS fails.
- **Secret scanning catches SKILL.md examples**: GitHub scans commit content, not just config files. Live tokens inside SKILL.md code examples get caught and block the entire push.
- **Large state DBs**: `state.db` can be 40MB+. Exclude it — the backup targets config, skills, memory, and cron, not runtime state.
- **`--force-with-lease` blocks in cron mode**: Hermes terminal agents guard force pushes with an interactive approval prompt. Since secret-blocked commits never reach the remote, the local HEAD diverges from a commit that doesn't exist remotely. Pushing with `--force-with-lease` tries to force-push and gets intercepted. Use a plain `git push` instead.
