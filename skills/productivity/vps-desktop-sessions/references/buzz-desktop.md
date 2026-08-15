# Block Buzz Desktop on the VPS

Operational notes for the official `block/buzz` desktop app in the persistent noVNC desktop.

## Install the packaged Linux build

Prefer the official release `.deb` over building the Rust/Tauri monorepo from source.

1. Read the latest release metadata from `https://api.github.com/repos/block/buzz/releases/latest`.
2. Select `Buzz_<version>_amd64.deb` after verifying the VPS is `x86_64` / `amd64`.
3. Download from the release asset URL, inspect with `file`, record `sha256sum`, then install with:
   ```bash
   apt-get install -y /tmp/Buzz_<version>_amd64.deb
   ```
4. Verify with:
   ```bash
   dpkg-query -W -f='${Status} ${Version} ${Architecture}\n' buzz
   command -v buzz buzz-desktop buzz-agent buzz-acp
   ```

The package supplies the desktop app plus agent/ACP/CLI binaries.

## Launch and verify

Launch inside the persistent desktop:

```bash
env DISPLAY=:99 buzz-desktop
```

This is a genuine long-lived GUI process. Start it with `terminal(background=true)` and **no watch patterns**. Buzz emits recurring strings such as `failed` when a relay is absent; generic `error|failed|panic` watchers create noisy false alarms.

Verification:

```bash
pgrep -af '^buzz-desktop$'
DISPLAY=:99 xwininfo -root -tree | grep -i buzz
```

On first launch, the Tauri top-level window may briefly appear as `10x10` or unmapped while Buzz downloads/extracts local STT/TTS models. Do not declare the launch broken immediately. Poll logs/process state, wait for model setup, and check again for the large WebKit child window. `libEGL` / DRI3 warnings on Xvfb normally mean software rendering, not a crash.

## Onboarding and relay choices

- Buzz creates a private identity key during onboarding. The user must handle and back it up personally. Never transcribe it from a screenshot or persist it in logs, memory, skills, or summaries. Delete temporary screenshots that display it.
- The default self-host path expects `ws://localhost:3000`; heartbeat messages saying `relay unreachable` are expected when only the desktop app is installed.
- Buzz may instead open Chromium at `login.builderlab.xyz` for the hosted BuilderLab flow. This is an intentional external-browser login. The user enters their own email, completes verification, and approves returning/opening Buzz if prompted. Hosted BuilderLab does not require deploying a local relay first.
- Keep the two paths explicit: hosted BuilderLab for quickest onboarding; self-hosted relay for full control.

## noVNC disconnects and recovery

If the user says the screen disappeared, inspect the original live surface before touching Buzz:

```bash
systemctl is-active vps-screen.service
systemctl status vps-screen.service --no-pager -n 20
ss -tlnp | grep -E '(:5901|:6080)'
curl -sS -u "jt:$(tr -d '\n' </root/.vps-screen/basic-auth-password.txt)" \
  -o /dev/null -w '%{http_code}\n' \
  'https://vnc.srv1056157.hstgr.cloud/vnc.html'
```

A service restart invalidates the user's existing noVNC connection even when the desktop is healthy again. Tell the user to reopen/reload the noVNC URL, then verify Buzz and Chromium windows with `xwininfo`. Raise the active login window with `xdotool windowraise/windowactivate` when needed. Explain exactly what the foreground browser is asking the user to do rather than merely saying “Buzz is running.”

## Post-onboarding: separate UI, relay, and agent health

Do not collapse these into one status:

1. **Desktop UI:** `buzz-desktop` process, X window, and rendered community screen.
2. **Community relay:** relay `/health`, authenticated `buzz channels list`, event acceptance/readback, and active connections.
3. **Agent listeners:** `buzz-acp` wrappers, explicit-mention delivery, and a new reply authored by the target agent.
4. **Auxiliary mesh status:** `buzz-mesh: status report ... relay unreachable` can belong to MeshLLM discovery/heartbeat even when normal hosted-community chat works.

A green agent card and online presence are insufficient proof that the agent consumes new mentions. If the relay accepts correctly tagged events but agents stay silent, use Buzz's Agents page to stop and restart the running set, verify fresh `buzz-acp` PIDs, then require one bounded round-trip reply. Avoid repeated long waits and do not assume killing one wrapper will make the desktop respawn it.

The packaged app also installs the JSON-oriented `buzz` CLI. Detailed messaging, auth-tag handling, listener recovery, and latency checks live in the `ai-coding-agents` skill at `references/buzz-collaborative-workspace.md`.
