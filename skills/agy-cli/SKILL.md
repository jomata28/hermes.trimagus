---
name: agy-cli
description: "Google Antigravity CLI (agy) — install, authenticate, and use for agentic coding."
version: 1.0.0
author: REDACTED
license: MIT
---

# Google Antigravity CLI (agy)

Google's Antigravity CLI — lightweight terminal interface to Gemini models and Claude models via Google's OAuth.

## Install

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

Binary: `/root/.local/bin/agy`

## Auth

**Preferred (non-interactive):** If authed on another machine (e.g., work laptop), copy token files from `~/.cache/antigravity/` to the VPS.

**Interactive (requires real-time):**
1. Run `export PATH="/root/.local/bin:$PATH" && timeout 120 agy --print "hello"`
2. Copy the auth URL from the output
3. User approves in browser
4. User copies the `code=` from the redirect URL
5. Agent pastes the code into the running process via PTY

### ⚠️ Auth Pitfall
The `agy` CLI uses PKCE with per-process verifiers. **Each `agy --print` call generates a different URL**. A code from one URL won't work with a different session. The auth round-trip must happen within a single running process, and the 30-second timeout is tight over Telegram.

**Proven workaround for headless VPS:** Try running `agy` with `GOOGLE_APPLICATION_CREDENTIALS` pointing to an existing Google token file. The CLI may accept the same token as Google Workspace (since both use Gemini models). If that doesn't work, the alternative is to auth `agy` on the work laptop (where you have a real terminal + Gemini AI Pro) and copy the token from `~/.cache/antigravity/` to the VPS.

## Usage

```bash
export PATH="/root/.local/bin:$PATH"

# Single prompt (non-interactive, prints result)
agy --print "your prompt here"

# Continue last conversation
agy --continue

# Run interactively
agy --prompt-interactive

# Auto-approve permissions
agy --dangerously-skip-permissions
```

## Plans / Quota

Your Google AI Pro subscription ($20/mo) gives:
- Gemini 3.1 Pro, 3.5 Flash, Claude Sonnet & Opus 4.6
- Higher weekly rate limits vs free tier
- Flexible AI credit pool for overages

## Notes
- Auth token stored in `~/.cache/antigravity/`
- Uses same Google account as Google Workspace (shared credentials)
- Better for interactive use on work laptop; on VPS, prefer token file transfer
