# GitHub Push Protection — Secret Scanning Blocks

## What It Does

GitHub's push protection scans **all commit content** for known secret patterns and **blocks the push entirely** if any are found. This is separate from GitHub Actions secrets management.

## What Gets Caught

- Live API keys in any file (.env, .yaml, .md, .py, etc.)
- GitHub PATs (`ghp_*`, `github_pat_*`)
- OpenAI keys (`sk-*`)
- OpenRouter keys (`sk-or-v1-*`)
- Notion tokens (`ntn_*`)
- Groq keys, AWS keys, Stripe keys, etc.

## Critical Pitfall

Secret scanning catches tokens inside **SKILL.md code examples**, not just in configuration files. Users frequently paste working API keys as examples in their skill files, and these get caught and block the entire push.

## How to Handle It

### Option 1: Remove secrets from the commit
```bash
# Redact tokens in files
sed -i 's/api_key: .*/api_key: REDACTED/' config.yaml

# Remove .env from tracking
echo ".env" >> .gitignore
git rm --cached .env
git commit --amend --no-edit
```

### Option 2: Allow the secret (requires repo admin)
After a blocked push, GitHub provides a URL to allow the specific secret:
```
https://github.com/<owner>/<repo>/security/secret-scanning/unblock-secret/<id>
```

### Option 3: Enable Secret Scanning on the repo
If the repo doesn't have Secret Scanning enabled, GitHub blocks pushes but doesn't show which secrets were found. Enable it at:
```
https://github.com/<owner>/<repo>/settings/security_analysis
```

## Detection Order

1. Push happens
2. GitHub scans all blobs in the push
3. If secrets found → push rejected with details
4. Each secret shows file path and line number

## Common Scenarios in This Environment

When backing up `~/.hermes/` to GitHub:
- `~/.hermes/.env` always has live keys — **exclude from commits entirely**
- `~/.hermes/config.yaml` may contain `github.token` — **redact before committing**
- Skills in `~/.hermes/skills/` may have live tokens in examples — **scan before pushing**
