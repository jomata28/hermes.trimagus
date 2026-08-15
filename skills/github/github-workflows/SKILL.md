---
name: github-workflows
description: "Use when managing GitHub work end-to-end: authentication, repository setup, issues, PR lifecycle, code review, releases, and codebase inspection."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, git, issues, pull-requests, code-review, repos]
    related_skills: []
---

# GitHub Workflows

## Overview

This umbrella skill covers GitHub as a full work class rather than separate micro-skills for auth, repos, issues, PRs, and reviews. Start by verifying authentication and repository context, then choose the subsection that matches the user's goal.

## When to Use

- The user asks to clone, fork, create, inspect, or publish a repository.
- The user asks to open, update, review, merge, or monitor a pull request.
- The user asks to create, triage, label, assign, or close issues.
- The user asks to set up GitHub authentication for Hermes.
- The user asks for repository language/LOC inspection before GitHub work.

## Context and Auth Gate

1. Run git/gh discovery in the actual working directory.
2. Verify remotes, current branch, dirty tree, and `gh auth status` or available git credentials.
3. Prefer `gh` for GitHub API operations when authenticated; use git plus REST only when needed.
4. Never fabricate PR/issue/CI state; fetch it with `gh` or API calls.

## Authentication

Use GitHub auth setup when `gh auth status` fails, git push needs credentials, or the user asks to connect Hermes to GitHub. Cover HTTPS tokens, SSH keys, credential helpers, and gh auth. Verify by a harmless authenticated command such as `gh repo view` or `gh api user`.

## Repository Management

For clone/create/fork/remotes/releases, inspect the local git state first. Confirm ownership and visibility before creating public/private repos or changing remotes.

### Backup Repositories with Config or Dotfiles

When backing up local config/dotfiles to GitHub:

1. Check repo visibility first: `gh repo view owner/repo --json visibility`. If it is PUBLIC, redaction (step 3) is mandatory — never push raw `.env`/`config.yaml`/token-bearing files — and explicitly flag the public visibility in your report so the owner can flip it to private if full-fidelity backups were intended.
2. Locate or clone the repo in the requested backup location; if it exists locally, `git pull --ff-only` before copying. If several local clones exist, inspect each clone's remote, branch, dirty state, upstream divergence, and latest commit; use the clean clone in the requested location that is synchronized with the remote. Do not merge or push stale unpublished commits from abandoned duplicate clones as part of a backup run.
3. Copy only the requested artifacts, preserving directory layout. For live SQLite databases, prefer `sqlite3 source.db ".backup 'dest.db'"` instead of raw copying so the backup is consistent. Hermes memory may be `memory_store.db` even when the user says `memory.db`; if compatibility matters, back up both names from the current source DB. Hermes cron jobs may be stored as `~/.hermes/cron/jobs.json` rather than a `cron/jobs/` directory; back up the actual jobs file found.
4. Redact secret-like values in the repository copy before committing. Use the bundled helpers when appropriate: `python scripts/redact-backup-secrets.py /path/to/backup/repo` for `.env`/`config.yaml`, then `python scripts/scan-redact-literal-tokens.py /path/to/backup/repo` for a whole-repo literal token sweep. Do not mutate the live source config. The whole-repo scan must exclude `.git/` because copied skills/docs may contain example PATs or provider tokens outside `.env`/`config.yaml`; redact those in the repo copy too before staging. If a raw backup commit was already made and GitHub Push Protection rejects it, run the redactors against the repo copy, scan the full repo, `git add` the redacted files, `git commit --amend`, then retry the push.
5. Validate redacted copies structurally, not only by token-pattern count. Run `python scripts/verify-public-backup.py /path/to/repo/config.yaml --expect-placeholder github.token` (add repeatable `--expect-placeholder` paths as appropriate), stage, and run `git diff --cached --check`. A continuation-line replacement can leave an ambiguous multiline scalar (and trailing whitespace), while malformed variants can become mappings, even when the literal scan reports zero remaining tokens. Normalize secret placeholders to explicit single-line scalars. See `references/public-backup-redaction-verification.md` for the focused probe and normalization example. Report this as **ad-hoc structural verification**, not a canonical suite pass. Create a fresh OS-safe `/tmp/hermes-verify-*` script with Python `tempfile`, execute it after the final edit, remove it, assert cleanup, and include both probe and cleanup evidence.
6. Commit with the requested timestamp/message, run `git show --check HEAD`, push, then verify with `git fetch`, `git rev-parse HEAD`, `git rev-parse origin/<branch>`, `git ls-remote origin refs/heads/<branch>`, and `git log -1 origin/<branch>`. Finish by checking `git status --short --branch` so the backup working tree is clean and synced.
7. If the requested `GITHUB_TOKEN` environment variable is absent, report that fact and fall back to existing configured credentials only if they work; do not claim token auth was used. Do NOT reconstruct it with `export GITHUB_TOKEN=$(gh auth token)` inside a terminal command — in cron/non-interactive runs the Hermes security scan holds the command for approval that never arrives, stalling the job. Rely on `gh`'s own auth or SSH instead. In cron/non-interactive backups, explicitly verify the fallback path with a real operation: try `gh auth token` for HTTPS, but if HTTPS push returns 403 while `gh repo view` shows admin/push permission, run `ssh -o BatchMode=yes -T git@github.com` and inspect stderr/stdout for `Hi <owner>! You've successfully authenticated` even if the command exits nonzero (GitHub often returns 1 because it does not provide shell access). If SSH authenticates as the repo owner, temporarily switch the remote to `git@github.com:owner/repo.git` for the push. Use a trap or explicit restore to set the remote back to the canonical requested HTTPS URL after the push, then verify with `git fetch`, `git rev-parse`, `git ls-remote`, and `git log -1 origin/<branch>`.

## Issues

For issue creation and triage, gather title, body, labels, assignees, milestone, and linked context. If the user supplies a vague bug, inspect the code/repro first and produce a concrete issue body.

## Pull Request Lifecycle

For PR work, branch from the intended base, keep commits scoped, open a PR with an evidence-backed body, monitor CI, and avoid merging unless explicitly requested or policy allows it.

## Code Review

Review PRs by reading diffs and relevant surrounding code, not only the patch. Prefer actionable findings with file/line references and severity. Verify any claimed bug when possible.

## Codebase Inspection

Use codebase inspection/LOC tooling when repository scale, languages, generated-code ratios, or architecture overview matters before GitHub actions.

## Common Pitfalls

1. Acting before confirming the repo/branch/remotes.
2. Opening or merging PRs with unverified tests.
3. Treating `gh` output from another directory as the target repository.
4. Losing issue/PR thread context by using platform names without IDs.
5. Assuming GitHub API repo permissions imply git push will work over HTTPS. Fine-grained PATs or credential-helper state can show `viewerPermission: ADMIN` / `permissions.push: true` via API while `git push` still returns 403. Verify with an actual `git push --dry-run`; if HTTPS auth fails and SSH is already configured (`ssh -T git@github.com` succeeds), switch the remote to `git@github.com:owner/repo.git` for the push, then restore the canonical remote if needed.
6. Pushing raw backup/config files that contain secrets. GitHub Push Protection can reject commits for tokens in `.env`, `config.yaml`, or copied notes. For backup repos, redact secret-like values in the repository copy only, amend/recreate the local commit, run a token-pattern scan, then push and verify the remote SHA.

## Verification Checklist

- [ ] Repository and auth context verified.
- [ ] Git state checked before writes.
- [ ] GitHub API/gh output captured for external state.
- [ ] Any created/updated artifact has a URL or ID.
