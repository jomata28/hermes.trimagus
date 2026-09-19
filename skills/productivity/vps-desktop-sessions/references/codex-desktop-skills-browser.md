# ChatGPT/Codex desktop: local skills and `@Browser`

Use this recipe when operating the Linux ChatGPT/Codex desktop app in the VPS noVNC session, especially when a task needs Work `@Browser` rather than Codex CLI browser access.

## Launch the app in the real user session

Electron can start and immediately exit when launched from a root shell with the wrong DBus session. Use the persistent user manager and a tracked systemd unit:

```bash
loginctl enable-linger jt
systemctl start user@1001.service
systemd-run --unit=chatgpt-vps --collect \
  --uid=jt --gid=jt --property=PAMName=login \
  --setenv=HOME=/home/jt \
  --setenv=DISPLAY=:99 \
  --setenv=XDG_RUNTIME_DIR=/run/user/1001 \
  --setenv=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1001/bus \
  /usr/bin/chatgpt --disable-gpu
```

Verify all three layers before claiming readiness:

1. `systemctl is-active chatgpt-vps.service`
2. a visible X window named `ChatGPT`
3. a fresh screenshot showing the usable app UI rather than its loading splash

## Install a local skill package

A skill ZIP should contain one top-level directory with `SKILL.md`, for example:

```text
viva-renovar-reserva/
└── SKILL.md
```

Inspect the archive before extraction, then install it under the app user's Codex home:

```bash
unzip -l /path/to/skill.zip
rm -rf /tmp/codex-skill-check
mkdir -p /tmp/codex-skill-check
unzip -q /path/to/skill.zip -d /tmp/codex-skill-check

test -f /tmp/codex-skill-check/<skill-name>/SKILL.md
rm -rf /home/jt/.codex/skills/<skill-name>
cp -a /tmp/codex-skill-check/<skill-name> /home/jt/.codex/skills/
chown -R jt:jt /home/jt/.codex/skills/<skill-name>
systemctl restart chatgpt-vps.service
```

After restart, wait for the splash to finish and verify the exact card under **Plugins → Skills → Installed**. Do not report success from filesystem presence alone; the visible installed card proves that Codex indexed the skill.

Invoke an installed skill explicitly in the prompt as `$skill-name`. If the task needs the app-owned browser, mention `@Browser` in the same prompt and state the invariants and stop conditions there.

## Start and monitor an `@Browser` run

1. Open **New chat** and focus the composer.
2. Enter the full task prompt, including `$skill-name`, `@Browser`, allowed state changes, invariants, and when to stop for the user.
3. Verify the prompt is visibly present before pressing Send; successful `xdotool` exit does not prove text reached the Electron composer.
4. Monitor at meaningful intervals. Report only: browser permission needed, login/CAPTCHA/2FA needed, verified completion, or a real blocker.
5. Treat the app-owned browser panel as a distinct profile and network path. Existing cookies from VPS Chrome do not imply that `@Browser` is authenticated.

### Safe prompt entry

- Do not feed a multiline prompt to `xdotool type --file`: newline characters can submit the first line before the rest is entered. Prefer a real clipboard paste; if clipboard tooling is unavailable, convert the prompt to one line, type it, capture the screen, and click the visible Send control explicitly.
- Re-capture the screen after `@Browser` opens. The split panel changes coordinates and can move focus from the Cowork composer into a website login or verification field.
- Before typing a long prompt, click the visible composer and verify that its caret or placeholder changed. After typing, capture again and confirm the text is in the composer before sending.
- If text lands in a website field, clear that field immediately with Select All + Backspace, verify it is empty, then refocus the composer. Never leave agent instructions in a username, OTP, payment, or other site field.

### Frozen desktop recovery

Before restarting the whole VPS, diagnose resource pressure with `uptime`, `free -h`, and a process list sorted by CPU and memory. Low available RAM with a large browser renderer can make noVNC and Electron appear frozen even when their services are healthy.

1. Capture the actual X11 screen so the visible failure is known.
2. Stop only the memory-heavy browser/app process, preserving its on-disk profile and cookies; avoid restarting unrelated gateway or dashboard services.
3. Relaunch Codex through the tracked `chatgpt-vps` user-session unit.
4. Verify recovered memory, active unit state, and a fresh screenshot showing the usable UI rather than the loading splash.

## Permission dialogs

Browser access can require two confirmations: the domain-access choice and a second elevated confirmation. Obtain the user's choice before clicking either; after approval, complete both matching confirmations and verify the browser actually navigates.

Site permission prompts are separate from ChatGPT browser permission. Ask before acting on them. Prefer the least privilege that preserves the task: for example, deny geolocation when a reservation/payment workflow does not require location.

Never treat a loading logo or a button click as success. Wait for the site UI or the agent's explicit result, and for external state changes verify the exact post-action state inside the target site.

## Window targeting pitfall

The app can have stale hidden windows with the same `ChatGPT` title, and Chrome can cover part of the Codex window. Before coordinate automation:

```bash
DISPLAY=:99 xdotool search --onlyvisible --name '^ChatGPT$'
```

Minimize or raise overlapping windows, activate the visible ChatGPT window, then capture again. Otherwise clicks can land in the covering browser or an old hidden window while hover state makes the intended app appear responsive.
