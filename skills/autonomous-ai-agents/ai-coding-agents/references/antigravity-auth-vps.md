# Google Antigravity (`agy`) Auth on Headless VPS

Session-derived operational notes for authenticating Antigravity CLI from a Hermes/VPS context.

## Key distinction

`hermes auth add google-antigravity --type oauth` is not a supported Hermes auth provider flow. Antigravity manages its own Google OAuth state through the `agy` CLI.

If the user asks for `google-antigravity` auth, run/guide the `agy` auth flow instead of trying to register a Hermes provider.

## Verified behavior

- Binary observed as `/root/.local/bin/agy`.
- `agy --version` works as a non-interactive install check.
- `agy --print ...` with no saved session prints a Google OAuth URL and waits for an authorization code on stdin.
- The CLI advertises the user-facing auth wait as `timeout 60s`, even if the outer `--print-timeout` is longer.
- The Google OAuth redirect is `https://antigravity.google/oauth-callback`.
- The flow expects the final authorization code pasted back into the waiting process.

## Headless flow

1. Verify the CLI:
   ```bash
   command -v agy && agy --version
   ```
2. Start a waiting auth run in PTY mode, ideally backgrounded so Hermes can capture the URL and later submit the code:
   ```bash
   agy --print 'auth smoke test' --print-timeout 5m
   ```
3. Give the user the printed Google OAuth URL immediately.
4. Tell the user to paste the authorization code back quickly; the inner auth prompt only waits about 60 seconds.
5. Submit the code to the process stdin, then verify with another short `agy -p` run.

## Pitfalls

- Do not describe `google-antigravity` as a Hermes credential pool provider unless Hermes actually registers it in the current install.
- Increasing `--print-timeout` does not necessarily extend the OAuth code-entry window; the inner prompt still timed out after about 60 seconds in this session.
- Starting the auth run and then waiting for the user in a final message is race-prone. Prefer a short instruction that emphasizes the 60-second window, or have the user ready before starting the process.
- If the process times out, restart the flow and use the fresh URL; OAuth state/code_challenge values are per-attempt.
