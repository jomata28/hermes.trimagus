# Human-verified browser with stable CDP control

Use when direct HTTP/headless access gets Cloudflare/Turnstile but a human can verify once through noVNC.

## Launch

Choose a task-specific profile and unused localhost port:

```bash
DISPLAY=:99 chromium \
  --no-sandbox \
  --disable-dev-shm-usage \
  --user-data-dir=/root/snap/chromium/common/<task-profile> \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=<port> \
  --start-maximized '<target-url>'
```

Run as a tracked long-lived background process.

## Verify attachment

```bash
ss -ltnp | grep <port>
curl -sS http://127.0.0.1:<port>/json/list
```

Confirm the page title and URL. `Just a moment...` plus a `challenges.cloudflare.com` iframe means human verification is still pending.

## Human handoff

1. Verify noVNC HTTP access without printing passwords.
2. Send JT the noVNC URL.
3. Ask him only to complete the visible checkbox/CAPTCHA or login himself.
4. Keep the same profile and browser process alive.
5. After confirmation, re-check `/json/list` and the rendered page before extracting.

Never automate the human-verification control or request website credentials in chat.

## Why dedicated profiles

A visible pre-existing browser may be unattached, owned by another workflow, or absent from X11 window discovery. Repeated coordinate clicks can silently hit another window. A dedicated profile provides stable cookies, process ownership, URL verification, and CDP DOM access.

A fresh profile has a separate cookie jar, so it may trigger Turnstile even when the default browser already loads the site. That is expected; solve once and reuse the profile.

## Stop conditions

Switch to this pattern after two failed coordinate attempts, ambiguous focus, or inability to discover the visible browser window. Keep user updates to meaningful checkpoints rather than each diagnostic action.