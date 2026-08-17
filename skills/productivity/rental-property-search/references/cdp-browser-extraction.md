# CDP Browser Extraction for Cloudflare-Blocked Portals

When all major MX real estate portals are Cloudflare-blocked, use the VPS persistent Chrome with CDP (Chrome DevTools Protocol) to extract page content. This works both for MercadoLibre (no Cloudflare) and for Inmuebles24/Vivanuncios (after JT solves the Turnstile challenge via noVNC).

## Launch Chrome with CDP

```bash
# Kill any existing jt Chrome
pkill -u jt -f "google-chrome" 2>&1 || true
sleep 3

# Launch Chrome as jt with CDP on port 9333
# Use background=true in terminal tool — this is a long-lived process
su - jt -c 'export DISPLAY=:99 && google-chrome-stable \
  --display=:99 \
  --disable-gpu \
  --no-first-run \
  --start-maximized \
  --remote-debugging-port=9333 \
  --remote-debugging-address=127.0.0.1 \
  --user-data-dir="/home/jt/.config/google-chrome-rental" \
  "<target-url>"'
```

Key points:
- Use `google-chrome-stable` (not snap Chromium) for proper SUID sandbox.
- Use a **separate profile dir** per task (`google-chrome-rental`) so sessions don't collide.
- Grant X11 access first: `xhost +SI:localuser:jt`
- Launch via `terminal(background=true)` — Chrome is a long-lived process.

## CDP page-reader script (Python stdlib only)

The following script reads page DOM via CDP using raw TCP WebSocket — no `websocket-client` library needed. Save as `/tmp/cdp_read.py` and run with `python3 /tmp/cdp_read.py`.

```python
#!/usr/bin/env python3
"""CDP query script to read page content via Chrome DevTools Protocol.
Uses only Python stdlib — no websocket-client dependency."""
import json, socket, sys, http.client

CDP_PORT = 9333

# Get the target tab
conn = http.client.HTTPConnection("127.0.0.1", CDP_PORT)
conn.request("GET", "/json/list")
resp = conn.getresponse()
tabs = json.loads(resp.read().decode())
conn.close()

# Find first non-chrome tab
target = None
for t in tabs:
    url = t.get("url", "")
    if url and not url.startswith("chrome://"):
        target = t
        break

if not target:
    print("No suitable tab found")
    for t in tabs:
        print(f"  - {t.get('title','')} | {t.get('url','')}")
    sys.exit(1)

ws_url = target["webSocketDebuggerUrl"]
parts = ws_url.replace("ws://", "").split("/")
host_port = parts[0]
path = "/" + "/".join(parts[1:])
host, port = host_port.split(":")

# Raw socket WebSocket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, int(port)))

handshake = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {host}:{port}\r\n"
    f"Upgrade: websocket\r\n"
    f"Connection: Upgrade\r\n"
    f"Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
    f"Sec-WebSocket-Version: 13\r\n\r\n"
)
sock.sendall(handshake.encode())

response = b""
while b"\r\n\r\n" not in response:
    response += sock.recv(4096)

# WebSocket frame helpers
def send_ws_frame(sock, data):
    payload = data.encode("utf-8")
    frame = bytearray([0x81])
    mask_key = b"\x00\x01\x02\x03"
    length = len(payload)
    if length < 126:
        frame.append(0x80 | length)
    elif length < 65536:
        frame.append(0x80 | 126)
        frame.extend(length.to_bytes(2, "big"))
    else:
        frame.append(0x80 | 127)
        frame.extend(length.to_bytes(8, "big"))
    frame.extend(mask_key)
    masked = bytearray()
    for i, b in enumerate(payload):
        masked.append(b ^ mask_key[i % 4])
    frame.extend(masked)
    sock.sendall(frame)

def recv_ws_frame(sock, timeout=15):
    sock.settimeout(timeout)
    data = bytearray()
    while len(data) < 2:
        chunk = sock.recv(2 - len(data))
        if not chunk: return None
        data.extend(chunk)
    masked = data[1] & 0x80
    length = data[1] & 0x7F
    header_len = 2
    if length == 126:
        while len(data) < 4:
            chunk = sock.recv(4 - len(data))
            if not chunk: return None
            data.extend(chunk)
        length = int.from_bytes(data[2:4], "big")
        header_len = 4
    elif length == 127:
        while len(data) < 10:
            chunk = sock.recv(10 - len(data))
            if not chunk: return None
            data.extend(chunk)
        length = int.from_bytes(data[2:10], "big")
        header_len = 10
    if masked:
        while len(data) < header_len + 4:
            chunk = sock.recv(header_len + 4 - len(data))
            if not chunk: return None
            data.extend(chunk)
        mask_key = data[header_len:header_len+4]
        payload_start = header_len + 4
    else:
        payload_start = header_len
    while len(data) < payload_start + length:
        remaining = payload_start + length - len(data)
        chunk = sock.recv(min(remaining, 65536))
        if not chunk: break
        data.extend(chunk)
    payload = data[payload_start:payload_start+length]
    if masked:
        unmasked = bytearray()
        for i, b in enumerate(payload):
            unmasked.append(b ^ mask_key[i % 4])
        return unmasked.decode("utf-8", errors="replace")
    return payload.decode("utf-8", errors="replace")

# Evaluate JS to extract page content
js_code = """
JSON.stringify({
    url: window.location.href,
    title: document.title,
    bodyText: document.body ? document.body.innerText.substring(0, 8000) : 'no body',
    links: Array.from(document.querySelectorAll('a[href]')).slice(0, 30).map(a => ({href: a.href, text: a.innerText.substring(0, 100)}))
})
"""

send_ws_frame(sock, json.dumps({
    "id": 1,
    "method": "Runtime.evaluate",
    "params": {"expression": js_code, "returnByValue": True}
}))

result = recv_ws_frame(sock, timeout=15)
if result:
    resp_data = json.loads(result)
    if "result" in resp_data and "result" in resp_data["result"]:
        value = resp_data["result"]["result"].get("value", "")
        parsed = json.loads(value)
        print(f"URL: {parsed.get('url', '')}")
        print(f"Title: {parsed.get('title', '')}")
        print(f"\nBody text:\n{parsed.get('bodyText', '')[:5000]}")
        if parsed.get("links"):
            print(f"\nLinks ({len(parsed['links'])}):")
            for link in parsed["links"][:20]:
                print(f"  {link['text'][:60]}: {link['href']}")

sock.close()
```

## CDP navigate script

To navigate the existing tab to a new URL without relaunching Chrome:

```python
# Same socket setup as above, then:
nav_msg = json.dumps({
    "id": 1,
    "method": "Page.navigate",
    "params": {"url": "https://target-url.com"}
})
send_ws_frame(sock, nav_msg)
result = recv_ws_frame(sock, timeout=15)  # Returns frameId on success
```

## Workflow for Cloudflare-locked portals

1. Launch Chrome with CDP (above).
2. Wait ~15s for page load.
3. Run `cdp_read.py` — if title is "Just a moment..." the Cloudflare challenge is active.
4. Send JT the noVNC URL (`https://vnc.srv1056157.hstgr.cloud/vnc.html?autoconnect=true&resize=scale&path=websockify`) with both auth stages.
5. JT solves the Turnstile checkbox in the noVNC browser.
6. Wait 10s, then run `cdp_read.py` again to confirm the real page loaded.
7. Extract listing links from the search results.
8. Use the navigate script to open each individual listing URL.
9. Run `cdp_read.py` after each navigation to capture listing details.

## When vision_analyze is unavailable (503)

CDP `Runtime.evaluate` on `document.body.innerText` is the primary text-based fallback. It returns the full rendered text content including prices, bedroom counts, and descriptions — sufficient for rental verification without screenshots.

## Pitfalls

- The agent-browser's headless Chrome (port 34001 etc.) has `--no-sandbox` and fails Cloudflare. Use `jt`'s Chrome with SUID sandbox instead.
- CDP port 9222 may conflict with other services; use 9333 or another free port.
- Cloudflare Turnstile does NOT auto-resolve even in a real Chrome — a human must click the checkbox.
- MercadoLibre Inmuebles does not need this workflow — it loads fine in headless Chrome or via `browser_navigate`.
