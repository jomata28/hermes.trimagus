---
name: google-workspace
description: "Gmail, Calendar, Drive, Docs, Sheets, Tasks via gws CLI or Python. Covers rclone Drive mount and agy CLI auth."
version: 1.2.0
author: Nous Research
license: MIT
required_credential_files:
  - path: google_token.json
    description: Google OAuth2 token (created by setup script)
  - path: google_client_secret.json
    description: Google OAuth2 client credentials (downloaded from Google Cloud Console)
metadata:
  hermes:
    tags: [Google, Gmail, Calendar, Drive, Sheets, Docs, Contacts, Email, OAuth, Tasks, Antigravity, agy, rclone]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [himalaya]
---

# Google Workspace

Gmail, Calendar, Drive, Contacts, Sheets, and Docs — through Hermes-managed OAuth and a thin CLI wrapper. When `gws` is installed, the skill uses it as the execution backend for broader Google Workspace coverage; otherwise it falls back to the bundled Python client implementation.

## References

- `references/gmail-search-syntax.md` — Gmail search operators
- `references/rclone-drive-mount.md` — Mount Google Drive as local filesystem via rclone
- `references/gcloud-cli-pkce-auth.md` — Google Cloud CLI auth pitfalls
- `references/antigravity-cli.md` — Google Antigravity CLI (`agy`) install, auth, and pricing

## Scripts

- `scripts/setup.py` — OAuth2 setup (run once to authorize)
- `scripts/google_api.py` — compatibility wrapper CLI. It prefers `gws` for operations when available, while preserving Hermes' existing JSON output contract.

## First-Time Setup

Define a shorthand first:

```bash
GSETUP="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py"
```

### Step 0: Check if already set up

```bash
$GSETUP --check
```

If it prints `AUTHENTICATED`, skip to Usage.

### Step 1: Determine scope needs

**Critical:** Before auth, check if the user needs **Drive write access** (upload, create, modify files). The default scope is `drive.readonly`. If they need write:

1. Edit the `SCOPES` list in `scripts/setup.py` (around line 45)
2. Change `"https://www.googleapis.com/auth/drive.readonly"` to `"https://www.googleapis.com/auth/drive"`
3. Do this BEFORE running auth

### Step 2: Create OAuth credentials

If the user pastes raw `client_id` + `client_secret` values (no file), create the client secret file yourself. The file MUST include the full OAuth structure with redirect URIs:

```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID",
    "project_id": "YOUR_PROJECT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": ["http://localhost"]
  }
}
```

Save as `~/.hermes/google_client_secret.json`.

If they download the JSON from Google Cloud Console, use:
```bash
$GSETUP --client-secret /path/to/client_secret_....json
```

> **Hermes CLI note:** if the file path starts with `/`, do NOT send only the bare path as its own message — it can be mistaken for a slash command. Send it in a sentence: "The JSON file path is: /home/user/Downloads/client_secret_....json"

### Step 3: Get authorization URL

```bash
$GSETUP --auth-url
```

**NOTE:** `--services` and `--format json` flags are NOT supported by setup.py. Just use `--auth-url` directly.

This prints a raw URL. Send the entire URL to the user.

After the user approves, the browser will try to redirect to `http://localhost:1` and fail. **This is expected.** Tell them to copy the ENTIRE URL from the browser address bar (including `?code=...&scope=...`) and paste it back.

### Step 4: Exchange the code

```bash
$GSETUP --auth-code "THE_FULL_REDIRECT_URL_THE_USER_PASTED"
```

If the code expired, it returns a fresh auth URL. Send that and retry.

### Step 5: Verify

```bash
$GSETUP --check
```

Should print `AUTHENTICATED`. Token auto-refreshes from `~/.hermes/google_token.json`.

## Usage

```bash
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
```

### Calendar

```bash
$GAPI calendar list                                          # next 7 days
$GAPI calendar list --start 2026-03-01T00:00:00Z --end 2026-03-07T23:59:59Z
$GAPI calendar create --summary "Meeting" --start 2026-03-01T10:00:00-06:00 --end 2026-03-01T10:30:00-06:00
$GAPI calendar delete EVENT_ID
```

### Drive

```bash
$GAPI drive search "quarterly report" --max 10
$GAPI drive search "'FOLDER_ID' in parents" --raw-query --max 20
```

### Tasks

Tasks API is NOT exposed via `$GAPI` (the python wrapper only covers Gmail, Calendar, Drive, Contacts, Sheets, Docs). Use `curl` directly with the token from `~/.hermes/google_token.json`.

**Important:** the stored `token` may be expired even when a `refresh_token` is present. For reliable task writes, refresh with `google.oauth2.credentials.Credentials` first, then call the REST API:

```bash
python3 - <<'PY'
import json, os, requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

path = os.path.expanduser('~/.hermes/google_token.json')
info = json.load(open(path))
creds = Credentials.from_authorized_user_info(info)
if not creds.valid and creds.refresh_token:
    creds.refresh(Request())
    info.update({'token': creds.token})
    if creds.expiry:
        info['expiry'] = creds.expiry.isoformat().replace('+00:00', 'Z')
    json.dump(info, open(path, 'w'))

headers = {'Authorization': 'Bearer ' + creds.token, 'Content-Type': 'application/json'}
TASKS_API = 'https://www.googleapis.com/tasks/v1'
print(requests.get(f'{TASKS_API}/users/@me/lists', headers=headers).text)
PY
```

```bash
TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/.hermes/google_token.json'))['token'])")
TASKS_API="https://www.googleapis.com/tasks/v1"

# List all task lists
curl -s -H "Authorization: Bearer $TOKEN" "$TASKS_API/users/@me/lists"

# Create a new task list
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "$TASKS_API/users/@me/lists" -d '{"title": "My List"}'

# List tasks in a list
curl -s -H "Authorization: Bearer $TOKEN" "$TASKS_API/lists/LIST_ID/tasks"

# Create a task
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "$TASKS_API/lists/LIST_ID/tasks" -d '{"title": "Do the thing", "notes": "Details", "due": "2026-06-01T12:00:00Z"}'

# Update a task
curl -s -X PUT -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "$TASKS_API/lists/LIST_ID/tasks/TASK_ID" -d '{"title": "Updated title", "status": "completed"}'

# Delete a task
curl -s -X DELETE -H "Authorization: Bearer $TOKEN" "$TASKS_API/lists/LIST_ID/tasks/TASK_ID"
```

### Gmail attachments and full-message extraction

`$GAPI gmail get MESSAGE_ID` is enough for simple messages, but it can miss attachment contents and may emit raw HTML/CSS-heavy bodies. For operational tasks (lease packets, maintenance docs, forms), use the Gmail API directly to recursively walk MIME parts, decode text parts, and download attachments:

```python
import base64, json, os, re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_info(json.load(open(os.path.expanduser('~/.hermes/google_token.json'))))
svc = build('gmail', 'v1', credentials=creds, cache_discovery=False)

def walk(part, texts, atts):
    filename = part.get('filename')
    body = part.get('body') or {}
    if filename and body.get('attachmentId'):
        atts.append((filename, part.get('mimeType'), body['attachmentId']))
    data = body.get('data')
    mime = part.get('mimeType', '')
    if data and (mime.startswith('text/') or mime in ('text/html', 'text/plain')):
        texts.append(base64.urlsafe_b64decode(data + '=' * ((4 - len(data) % 4) % 4)).decode('utf-8', 'ignore'))
    for child in part.get('parts', []) or []:
        walk(child, texts, atts)

msg = svc.users().messages().get(userId='me', id='MESSAGE_ID', format='full').execute()
texts, atts = [], []
walk(msg['payload'], texts, atts)
for filename, mime, attachment_id in atts:
    data = svc.users().messages().attachments().get(userId='me', messageId=msg['id'], id=attachment_id).execute()['data']
    raw = base64.urlsafe_b64decode(data + '=' * ((4 - len(data) % 4) % 4))
    safe = re.sub(r'[^A-Za-z0-9._ -]', '_', filename)
    open('/tmp/' + safe, 'wb').write(raw)
    print('/tmp/' + safe, len(raw), mime)
```

Use this when the user asks for “all data from emails” or needs attached PDFs/DOCX files from Gmail.

### Gmail

```bash
$GAPI gmail search "is:unread newer_than:1d" --max 10
$GAPI gmail send --to user@example.com --subject "Hello" --body "Message text"
```

## Rules

1. **Never send email or create/delete calendar events without confirming.** Show content, ask for approval.
2. **Check auth before first use** — `setup.py --check`.
3. **Calendar times must include timezone** — ISO 8601 with offset or `Z`.
4. **rclone for persistent Drive access:** Install rclone (`which rclone` to check), then mount with:
   ```bash
   # Configure rclone to use the same token as google-workspace
   mkdir -p ~/.config/rclone
   # Create rclone.conf manually using token from google_token.json:
   python3 -c "
   import json
   token = json.load(open('$HOME/.hermes/google_token.json'))
   conf = f\"\"\"[drive-hermes]
   type = drive
   token = {{\\\"access_token\\\": \\\"{token['token']}\\\", \\\"token_type\\\": \\\"Bearer\\\", \\\"refresh_token\\\": \\\"{token['refresh_token']}\\\", \\\"expiry\\\": \\\"{token['expiry']}\\\"}}
   client_id = {token['client_id']}
   client_secret = {token['client_secret']}
   \"\"\"
   print(conf)
   " > ~/.config/rclone/rclone.conf
   # Mount Obsidian vault or any Drive folder:
   rclone mount drive-hermes:bitacora ~/obsidian-vault --vfs-cache-mode writes --daemon
   ```
   This gives direct filesystem access to Drive folders — much better than Drive API for editing markdown files.
5. **Respect rate limits** — batch reads, avoid rapid-fire sequential calls.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `NOT_AUTHENTICATED` | Run setup Steps 2-5 |
| `REFRESH_FAILED` | Token revoked/expired — redo Steps 3-5 |
| `HttpError 403: Insufficient Permission` | Missing scope — `$GSETUP --revoke`, fix SCOPES in setup.py, redo Steps 3-5 |
| `HttpError 403: Access Not Configured` | API not enabled in Google Cloud Console |
| `ModuleNotFoundError` | Run `$GSETUP --install-deps` |
| `--auth-url --services/--format flags fail` | Not supported — just run `$GSETUP --auth-url` |
| Client secret format error | Must include `auth_uri`, `token_uri`, `redirect_uris` — not just client_id/secret |
| `Error 403: access_denied` | User needs to add themselves as test user at `console.cloud.google.com/auth/audience` |

## Revoking Access

```bash
$GSETUP --revoke
```
