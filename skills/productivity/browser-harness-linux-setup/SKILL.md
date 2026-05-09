---
name: browser-harness-linux-setup
description: Setting up browser-harness for browser automation in Linux environments
category: productivity
---

# Browser Harness Linux Setup

## When to Use
Setting up browser-harness for browser automation in Linux environments, especially when dealing with:
- Headless containers without GUI/X server
- Snap package restrictions (AppArmor)
- Missing standard Chrome binaries
- Need to connect to existing Chrome instance via remote debugging

## Setup Steps

### 1. Launch Chrome/Chromium with Remote Debugging
```bash
# Find available browser (try in order):
# - google-chrome
# - chromium-browser  
# - brave-browser
# - /snap/bin/chromium (for Snap packages)

# Example for Snap chromium with necessary flags:
chromium-browser --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-profile \
  --no-sandbox \
  --headless \
  --disable-gpu &
```

### 2. Get the DevTools WebSocket URL
After launching, find the WebSocket URL from:
- Console output: "DevTools listening on ws://..."
- Or visit: `http://127.0.0.1:9222/json/version` and look for "webSocketDebuggerUrl"

### 3. Configure and Run Browser Harness
```bash
# Clone if not already done
git clone https://github.com/browser-use/browser-harness.git
cd browser-harness

# Set the CDP WebSocket URL
export BU_CDP_WS="ws://127.0.0.1:9222/devtools/browser/<your-id-here>"

# Run with Python code via stdin (note the single quotes to prevent shell expansion)
python run.py <<'PY'
ensure_real_tab()
goto("https://example.com")
wait_for_load()
print("Title:", js("document.title"))
PY
```

## Common Issues and Fixes

### Issue: "Missing X server or $DISPLAY"
**Fix**: Add `--headless` flag to Chrome launch command

### Issue: "Running as root without --no-sandbox is not supported"
**Fix**: Add `--no-sandbox` flag (necessary in containers)

### Issue: Snap/AppArmor restrictions
**Fix**: 
- Use `--no-sandbox` 
- Consider installing Chrome via apt instead of Snap if possible:
  ```bash
  # For Debian/Ubuntu
  wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
  echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
  sudo apt update
  sudo apt install google-chrome-stable
  ```

### Issue: "DevToolsActivePort not found"
**Fix**: 
- Verify browser is running with remote debugging flag
- Check correct port (default 9222)
- Set BU_CDP_WS to the exact webSocketDebuggerUrl from Chrome

### Issue: JS evaluation returning unexpected types
**Fix**:
- Use `js("document.body.innerText")` for text content
- For HTML: `js("document.body.innerHTML")` (returns string)
- For DOM elements: returns JS handle, not directly usable
- To get element text: `js("document.querySelector('selector').innerText")`

## Usage Patterns

### Basic Navigation
```python
ensure_real_tab()
goto("https://example.com")
wait_for_load()
```

### Extracting Information
```python
# Get page title
title = js("document.title")

# Get element text by CSS selector
element_text = js("document.querySelector('h1').innerText")

# Get multiple elements
items = js("""() => {
  return Array.from(document.querySelectorAll('.item'))
    .map(el => el.innerText);
}""")
```

### Interacting with Pages
```python
# Click element by ref (from helpers.py)
act("e1")  # clicks element with ref e1

# Type into element
act("e2", "hello world")  # types into element with ref e2

# Press keys
press_key("Enter")
press_key("Control", modifiers=2)  # Ctrl key
```

## Verification
After setup, verify with:
```python
python run.py <<'PY'
ensure_real_tab()
print("Current tab:", js("location.href"))
print("Page title:", js("document.title"))
PY
```

## Notes
- The `js()` function returns raw values from browser (strings, numbers, booleans)
- For complex objects, use `returnByValue=True` in cdp() calls or stringify in JS
- Helper functions like `act()`, `goto()`, `wait_for_load()` are in helpers.py
- Domain-specific skills can be saved/loaded from domain-skills/ directory
- For file uploads: use `upload_file(selector, absolute_file_path)`