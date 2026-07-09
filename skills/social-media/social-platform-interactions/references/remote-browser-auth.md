# Remote Browser Auth for Private/Paid Social Content

Use when a platform (e.g. Substack) has private/paid content and the user must log in interactively.

## Safe flow

1. Open or reuse a remote browser on the VPS display.
2. Expose it with noVNC only as a temporary bridge.
3. Tell the user which password prompt they are seeing:
   - noVNC/VPS screen password = remote desktop access.
   - Platform password = typed by the user inside the browser only.
4. Never ask the user to paste platform credentials into chat.
5. Once authenticated, navigate to the provided private URL and perform the requested read/summarize/extract task.
6. After the task, close the public tunnel and temporary processes unless the user explicitly says to keep them running.

## Debug checklist when “password doesn’t work”

- Inspect the live process, not the intended command:
  - `pgrep -fa 'x11vnc|websockify|cloudflared|chrom(e|ium)'`
  - `ss -tlnp | grep -E ':(5901|6080|5902|6081|5903|6082)\\b'`
- Check whether `x11vnc` is using an existing password file such as a VPS-screen password rather than the newly generated temp file.
- If the active server is owned by a persistent VPS-screen service, avoid replacing it mid-session. Start a separate temporary stack on fresh ports instead.
- Verify the browser bridge before sending it:
  - HTTP 200 on `/vnc.html?autoconnect=true&resize=remote`
  - VNC listening on the expected localhost port.
  - websockify listening on the exposed bridge port.

## Practical pitfall

Do not use broad `pkill -f` cleanup patterns embedded in a shell command; the pattern can match and kill the current shell before setup finishes. Prefer Hermes tracked background process IDs, exact PIDs, or a new unused port pair.

## Recommended pattern

- Persistent display may already exist (`Xvfb :99`, `fluxbox`, browser).
- For a fresh temporary session, choose a new port pair such as:
  - VNC: `5903`
  - websockify: `6082`
- Start `x11vnc` with the temp password file on that VNC port.
- Start `websockify` from the bridge port to the VNC port.
- Start `cloudflared tunnel --url http://<bridge-host>:<bridge-port>`.
- Send the resulting noVNC URL plus the temp noVNC password.
