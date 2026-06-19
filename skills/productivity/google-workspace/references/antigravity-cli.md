# Rclone Drive Mount — Quick Auth

When you need rclone to mount Google Drive and you already have
`~/.hermes/google_token.json` from the `google-workspace` skill:

## Setup

Save credentials to the rclone config:

```python
import json, os
from pathlib import Path

gtoken =REDACTED_IN_BACKUP

os.makedirs(Path.home() / ".config/rclone", exist_ok=True)
with open(Path.home() / ".config/rclone/rclone.conf", "w") as f:
    f.write(f"""[drive-hermes]
type = drive
token =REDACTED_IN_BACKUP
client_id = {gtoken["client_id"]}
client_secret =REDACTED_IN_BACKUP
""")
```

Or via shell:

```python
python3 -c "
import json, os
gtoken =REDACTED_IN_BACKUP
os.makedirs(os.path.expanduser('~/.config/rclone'), exist_ok=True)
with open(os.path.expanduser('~/.config/rclone/rclone.conf'), 'w') as f:
    token_str =REDACTED_IN_BACKUP
    f.write(f'[drive-hermes]\ntype = drive\ntoken = {token_str}\nclient_id = {gtoken[\"client_id\"]}\nclient_secret = {gtoken[\"client_secret\"]}\n')
print('rclone configured')
"
```

## Mount

```bash
mkdir -p ~/obsidian-vault
rclone mount drive-hermes:bitacora ~/obsidian-vault --vfs-cache-mode writes --daemon
```

## Verify

```bash
ls ~/obsidian-vault/
```

## Key flags
- `--vfs-cache-mode writes` — light and sufficient for markdown files
- `--daemon` — detached mode

## Refresh

If the mount shows no files, the token expired. Re-auth via `google-workspace`,
then rebuild the rclone config with the steps above. Kill the old mount with:
```bash
fusermount -u ~/obsidian-vault 2>/dev/null || umount ~/obsidian-vault
```
