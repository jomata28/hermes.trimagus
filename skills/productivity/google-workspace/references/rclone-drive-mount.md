# rclone — Mount Google Drive as local filesystem

## When to use

When you need read/write access to Google Drive files via standard filesystem operations (not just the Drive API). Perfect for syncing vaults, editing markdown files, or any workflow that benefits from `cp`, `mv`, `sed`, etc. on Drive content.

## Prerequisites

- rclone installed: `which rclone` (pre-installed on this VPS, v1.72+)
- Google OAuth token already obtained via `google-workspace` skill setup (token at `~/.hermes/google_token.json`)

## Setup — Reuse existing Google OAuth token

**Key technique:** You don't need a separate OAuth flow for rclone. Reuse the token from the Google Workspace setup.

```bash
# Read the existing token
python3 -c "
import json
with open('/root/.hermes/google_token.json') as f:
    t = json.load(f)
token_data = {
    'access_token': t['token'],
    'token_type': 'Bearer',
    'refresh_token': t['refresh_token'],
    'expiry': t['expiry']
}
print(json.dumps(token_data))
"

# Write rclone config (replace values from above)
mkdir -p ~/.config/rclone
cat > ~/.config/rclone/rclone.conf << 'EOF'
[drive-hermes]
type = drive
token = REDACTED
client_id = <from google_token.json>
client_secret = REDACTED
EOF
```

Or in one shot with Python:

```python
import json, os

with open("/root/.hermes/google_token.json") as f:
    t = json.load(f)

token_data = {
    "access_token": t["token"],
    "token_type": "Bearer",
    "refresh_token": t["refresh_token"],
    "expiry": t["expiry"]
}

rclone_conf = f"""[drive-hermes]
type = drive
token = REDACTED
client_id = {t["client_id"]}
client_secret = REDACTED
"""

os.makedirs(os.path.expanduser("~/.config/rclone"), exist_ok=True)
with open(os.path.expanduser("~/.config/rclone/rclone.conf"), "w") as f:
    f.write(rclone_conf)
```

## Verify

```bash
rclone lsd drive-hermes: --max-depth 1
```

## Mount a folder locally

```bash
mkdir -p ~/obsidian-vault
rclone mount drive-hermes:bitacora ~/obsidian-vault \
  --vfs-cache-mode writes \
  --daemon
```

`--vfs-cache-mode writes` ensures local edits are synced back to Drive. `--daemon` runs in background.

## Common operations

```bash
# List files
rclone ls drive-hermes:some-folder

# Search (uses Drive API)
rclone lsf drive-hermes: --max-depth 2

# Copy local → Drive
rclone copy /local/path drive-hermes:remote/path

# Sync Drive → local (one-way, deletes local extras)
rclone sync drive-hermes:remote /local/path

# Mount (background, read/write)
rclone mount drive-hermes:folder ~/mount-point --vfs-cache-mode writes --daemon

# Unmount
fusermount -u ~/mount-point
```

## Pitfalls

- **Token expiry:** The access_token expires after ~1 hour, but the refresh_token is permanent. rclone will auto-refresh if the credentials are set up correctly.
- **Drive scope matters:** If the token was created with `drive.readonly`, rclone mounts will be read-only. You must use `https://www.googleapis.com/auth/drive` (full access) scope. The `google-workspace` setup script defaults to `drive` after patching.
- **Unmount before re-mounting:** If the daemon crashes or the mount becomes stale, `fusermount -u ~/mount-point` before retrying.
- **Large file trees:** rclone `lsd` is slow on folders with 1000+ items. Use `--max-depth` to limit traversal.
