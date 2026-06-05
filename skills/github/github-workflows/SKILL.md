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

## Verification Checklist

- [ ] Repository and auth context verified.
- [ ] Git state checked before writes.
- [ ] GitHub API/gh output captured for external state.
- [ ] Any created/updated artifact has a URL or ID.
