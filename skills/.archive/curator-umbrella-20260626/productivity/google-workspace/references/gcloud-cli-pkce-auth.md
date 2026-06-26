# Google Cloud CLI Auth — PKCE and agy CLI

## PKCE code verifier pitfall

Many Google CLIs (like `agy` / Antigravity CLI) use PKCE (Proof Key for Code Exchange). The CLI generates a random code verifier, derives a code challenge, and embeds it in the auth URL. When you paste the authorization code back, it must be from the **same session** that generated the verifier.

**Critical:** If you start an auth flow, get a URL, then restart or re-run the command, a _new verifier_ is generated. Any previous code will fail with:
```
Error: authentication failed: token exchange failed: oauth2: "invalid_grant" "Invalid code verifier."
```

## Working pattern for headless servers

1. Run the auth command in a **single background process**:
```bash
agy --print "hello" &  # or use background terminal process
```
2. Extract the auth URL from output
3. User approves in browser, copies the redirect URL or authorization code
4. **Immediately** paste the code into the **original process** — do NOT restart

If the process is a `process` background session, use `process(action='submit')` to paste the code.

## Why `agy` doesn't work headless without care

`agy` (Antigravity CLI) is built with bubbletea — it requires a real TTY. On headless VPS:
- Standard `terminal` calls fail with `bubbletea: error opening TTY: open /dev/tty: no such device or address`
- Using `pty: true` may work but the auth timeout is only 30s by default
- The `--print --dangerously-skip-permissions` flags help but don't bypass auth

## Alternative: Google AI Ultra / Pro API key

Instead of OAuth CLI auth, some Google Cloud CLI tools accept an API key or service account. Check the specific tool:
- `agy` uses OAuth only (no API key support as of 2026-05-25)
- For VPS use, consider delegating agy tasks to the user's laptop where they're already authed

## Relevant CLIs that use PKCE

- `agy` (Antigravity CLI)
- `gcloud auth login`
- Various Google Cloud SDK tools

All follow the same pattern: one invocation = one verifier = one chance to complete auth.
