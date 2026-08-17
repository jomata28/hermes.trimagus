# Raw CDP Websocket via Python Stdlib

Use this when you need to read page content or execute JavaScript inside a Chrome
tab that has `--remote-debugging-port` enabled, but:

- The `websocket-client` Python package is NOT installed and `pip install` is
  blocked by PEP 668 / missing venv / environment constraints.
- `vision_analyze` is returning 503 (vision model provider down).
- `xdotool` typing into the DevTools console is unreliable (events landing in
  wrong window, focus ambiguity, typing too slow for complex JS).

## Prerequisites

Chrome must be running with remote debugging:

```bash
google-chrome-stable --remote-debugging-port=9333 --remote-debugging-address=127.0.0.1 ...
```

Verify the endpoint is up:

```bash
curl -s http://127.0.0.1:9333/json/list | python3 -c "
import sys, json
tabs = json.load(sys.stdin)
for t in tabs:
    print(f\"{t.get('title','?')}: {t.get('url','?')[:80]}\")
"
```

## The technique

Use Python's built-in `socket`, `base64`, `os`, `json`, and `re` modules to
implement a minimal WebSocket client. No third-party packages needed.

### Core functions

```python
import json, socket, base64, os, re, urllib.request, time

def cdp_eval(ws_url, js_expression, timeout=15):
    """Evaluate JS in a Chrome tab via CDP using raw stdlib websocket."""
    m = re.match(r'ws://([^:]+):(\d+)(.*)', ws_url)
    host, port, path = m.group(1), int(m.group(2)), m.group(3)
    
    sock = socket.create_connection((host, port), timeout=timeout)
    
    # WebSocket handshake
    key = base64.b64encode(os.urandom(16)).decode()
    handshake = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n"
        f"\r\n"
    )
    sock.sendall(handshake.encode())
    
    # Read handshake response (discard)
    response = b""
    while b"\r\n\r\n" not in response:
        response += sock.recv(4096)
    
    # Send CDP Runtime.evaluate command
    msg = json.dumps({
        'id': 1,
        'method': 'Runtime.evaluate',
        'params': {'expression': js_expression, 'returnByValue': True}
    })
    _ws_send(sock, msg)
    
    # Read response
    time.sleep(3)
    resp = _ws_recv(sock)
    
    result = json.loads(resp.decode('utf-8', errors='replace'))
    return result.get('result', {}).get('result', {}).get('value', '')


def cdp_navigate(ws_url, url):
    """Navigate a Chrome tab to a new URL via CDP."""
    m = re.match(r'ws://([^:]+):(\d+)(.*)', ws_url)
    host, port, path = m.group(1), int(m.group(2)), m.group(3)
    
    sock = socket.create_connection((host, port), timeout=20)
    key = base64.b64encode(os.urandom(16)).decode()
    sock.sendall(f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode())
    resp = b""
    while b"\r\n\r\n" not in resp:
        resp += sock.recv(4096)
    
    msg = json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': url}})
    _ws_send(sock, msg)
    time.sleep(2)
    sock.close()


def _ws_send(sock, message):
    """Send a masked text websocket frame."""
    data = message.encode('utf-8')
    mask = os.urandom(4)
    header = bytearray([0x81])  # FIN + text frame
    if len(data) < 126:
        header.append(0x80 | len(data))
    elif len(data) < 65536:
        header.append(0x80 | 126)
        header.extend(len(data).to_bytes(2, 'big'))
    else:
        header.append(0x80 | 127)
        header.extend(len(data).to_bytes(8, 'big'))
    header.extend(mask)
    masked = bytearray(b ^ mask[i % 4] for i, b in enumerate(data))
    sock.sendall(bytes(header) + bytes(masked))


def _ws_recv(sock, timeout=10):
    """Receive a websocket frame (handles fragmentation up to 64-bit length)."""
    sock.settimeout(timeout)
    resp = b""
    while len(resp) < 2:
        resp += sock.recv(65536)
    
    payload_len = resp[1] & 0x7F
    offset = 2
    if payload_len == 126:
        payload_len = int.from_bytes(resp[2:4], 'big')
        offset = 4
    elif payload_len == 127:
        payload_len = int.from_bytes(resp[2:10], 'big')
        offset = 10
    
    masked_bit = (resp[1] & 0x80) != 0
    if masked_bit:
        mask = resp[offset:offset+4]
        offset += 4
    
    payload = resp[offset:]
    while len(payload) < payload_len:
        payload += sock.recv(65536)
    
    if masked_bit:
        payload = bytearray(b ^ mask[i % 4] for i, b in enumerate(payload[:payload_len]))
    
    return bytes(payload[:payload_len])
```

### Usage pattern

```python
# 1. Get the websocket URL for the target tab
tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9333/json/list').read())
page_tab = [t for t in tabs if 'target-site' in t.get('url', '')][0]
ws_url = page_tab['webSocketDebuggerUrl']

# 2. Check login state
result = cdp_eval(ws_url, '''
    JSON.stringify({
        hasToken: !!localStorage.getItem("viva-user-token"),
        url: window.location.href,
        bodyText: document.body.innerText.substring(0, 1500)
    })
''')
print(json.loads(result))

# 3. Navigate to a new page
cdp_navigate(ws_url, 'https://example.com/search?filter=value')
time.sleep(8)  # Wait for page to render

# 4. Extract data from the rendered page
listings = cdp_eval(ws_url, '''
    (function() {
        var results = [];
        document.querySelectorAll('.listing-card').forEach(function(card) {
            results.push({
                title: card.querySelector('h2')?.textContent?.trim() || '',
                price: card.querySelector('.price')?.textContent?.trim() || '',
                link: card.querySelector('a')?.href || ''
            });
        });
        return JSON.stringify(results);
    })()
''')
```

## When to prefer this over alternatives

| Situation | Best approach |
|---|---|
| vision_analyze working, simple page check | Screenshot + vision_analyze |
| Need to extract structured data from SPA | CDP raw websocket (this technique) |
| Need to click/type in a form | xdotool (if window focus is clear) or CDP `Input.dispatchMouseEvent` |
| vision_analyze down (503) | CDP raw websocket is the primary fallback |
| Package installation blocked (PEP 668) | CDP raw websocket (stdlib only) |

## Pitfalls

- **Large responses**: If the JS return value is very large (>65KB), the websocket
  frame may be split across multiple TCP segments. The `_ws_recv` function handles
  this by continuing to read until `payload_len` bytes are collected.
- **Timing**: After `cdp_navigate`, wait at least 5-8 seconds for SPAs to render
  before querying content. Angular/React apps may need longer.
- **Multiple tabs**: Always filter by URL substring when selecting the tab. Chrome
  opens internal tabs (Omnibox Popup, Service Workers) that should be skipped.
- **Connection lifecycle**: Each `cdp_eval`/`cdp_navigate` call opens a fresh
  websocket connection. This is simpler than maintaining a persistent connection
  and avoids stale-socket issues, at the cost of a small per-call overhead.
