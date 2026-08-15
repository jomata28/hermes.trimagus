# Packaged Linux GUI Apps on the noVNC Desktop

Use this pattern for `.deb`/AppImage/Tauri/GTK/WebKit applications that JT needs to see through the persistent VPS desktop.

## Install and verify

1. Confirm the VPS architecture before choosing a release asset (`uname -m`, `dpkg --print-architecture`).
2. Prefer the project's official release artifact over building from source when the user only asked to install/try the app.
3. For a Debian package, download the exact release asset, inspect it with `file`, record `sha256sum`, then install with `apt-get install -y /path/to/package.deb` so dependencies are resolved.
4. Verify package state and installed entry points (`dpkg-query -W`, `command -v`, and the package's `.desktop` file).

## Launch on the persistent desktop

Launch with `DISPLAY=:99` as a tracked long-lived background process, then verify all three layers:

- process exists (`pgrep` or tracked-process status),
- an X window appears (`DISPLAY=:99 xwininfo -root -tree`),
- the rendered UI is actually usable (desktop screenshot + vision inspection).

Tauri/WebKit apps may initially expose only a tiny or unmapped helper window while first-run assets/models download. Do not conclude the launch failed from the first `xwininfo` result. Read the live process log, wait for initialization/download completion, then inspect the X tree and screenshot again. A later child window may be the real full-size UI.

## First-run secrets and privacy

Onboarding screens may display recovery phrases, Nostr private keys, API keys, QR codes, or device codes.

- Never transcribe such a secret into chat or a task summary.
- Do not save or persist it to memory/skills.
- If a verification screenshot contains it, delete the PNG and source XWD immediately after inspection.
- Stop at the backup/identity screen and let JT record the secret and click through himself unless he explicitly asks otherwise.

## Product-state distinction

Separate these claims clearly:

- **Installed:** package and binaries are present.
- **Launched:** GUI process/window is running.
- **Operational:** required backend, relay, account, or service is connected.

A desktop client can be correctly installed and launched while its default backend is still unreachable. Report that as the next setup requirement rather than claiming the whole product is ready.