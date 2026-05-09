---
name: platform-tool-verification
description: Process for verifying tool platform compatibility and setting up Linux alternatives when user is on Linux but initial suggestions are macOS-specific
category: productivity
---

# Platform Tool Verification and Linux Alternative Setup

## When to Use This Skill
When a user inquires about a tool that appears to be platform-specific (particularly macOS-focused) and you need to:
1. Verify the tool's actual platform support
2. Confirm the user's operating system
3. Identify and set up appropriate Linux-compatible alternatives
4. Document the process for future similar situations

## Verification Process

### Step 1: Initial Tool Assessment
When presented with a tool suggestion:
- Examine documentation/platform markers:
  - Look for DMG/pkg installers (macOS-specific)
  - Check for Homebrew mentions
  - Note OS-level feature descriptions (e.g., "macOS bridge", "native messaging for macOS")
  - Review installation scripts for platform conditionals
- Example red flags in Interceptor README:
  - "Option 1: DMG Installer (Recommended)"
  - "Register native messaging (for macOS bridge)"
  - macOS-specific build instructions

### Step 2: Platform Confirmation
When user indicates Linux usage:
- Explicitly acknowledge platform mismatch: "I see you're running Linux, and this tool appears macOS-focused..."
- Ask for distribution if relevant for specific setup steps (Ubuntu, Fedora, etc.)
- Accept user-suggested alternatives or be prepared to research options

### Step 3: Alternative Evaluation
For browser automation tools specifically:
- Look for CDP/WebSocket-based solutions (work cross-platform)
- Prioritize tools with:
  - No platform-specific installers
  - Cross-platform dependencies (Python/Node.js)
  - Active Linux user base/documentation
- Example: browser-harness meets these criteria

### Step 4: Linux Alternative Setup (browser-harness example)
When browser-harness or similar is suggested:

#### Prerequisites Verification
- Chrome/Brave browser installed
- Python 3.9+ available
- git installed

#### Setup Procedure
1. Clone repository:
   ```bash
   git clone https://github.com/browser-use/browser-harness.git
   cd browser-harness
   ```

2. Launch browser with remote debugging (close all instances first):
   ```bash
   # Chrome
   google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-dev-profile
   
   # Brave
   brave-browser --remote-debugging-port=9222 --user-data-dir=/tmp/brave-dev-profile
   ```

3. Start harness in separate terminal:
   ```bash
   python run.py
   ```

#### Key Helper Functions (from helpers.py)
- `open(url, wait_time=3000, timeout=10000)` - Navigation
- `act(ref, text=None, **kwargs)` - Click/type
- `read(ref=None, tree_only=False, text_only=False)` - DOM inspection
- `inspect()` - Tree + text + network + headers
- `find(text, **kwargs)` - Element location
- Plus network interception, form handling, navigation controls

#### Usage Workflow
```python
# Example: Star a GitHub repo if logged in
open("https://github.com/browser-use/browser-harness")
# [Page loads]
star_btn = find("Star" --role button)  # Conceptual - actual use via helper
act(star_btn)  # Click if user consents
```

### Step 5: Comparison Documentation
Document key differences for user understanding:

| Feature | browser-harness (Linux) | Interceptor (macOS) |
|---------|-------------------------|---------------------|
| **Core Browser Control** | ✅ CDP-based (Linux compatible) | ✅ Extension-based (core works on Linux) |
| **OS-level Features** | ❌ (Requires separate tools) | ✅ Speech, vision, file system access |
| **Install Method** | Clone + remote debugging flag | DMG or manual script + native messaging |
| **Extensibility** | ✅ Agent edits `helpers.py` | ❌ Fixed helper set |
| **Skill Sharing** | ✅ `domain-skills/` folder | ❌ |
| **Resource Footprint** | Pure Python (~600 lines) | Rust/Bun + native deps |
| **Network Intercept** | ✅ Auto fetch/XHR capture | ✅ Similar capability |
| **Teach-and-Replay** | ✅ Via helper updates | ❌ |

### Step 6: Alternative Linux Approaches
If browser-harness isn't suitable:
- **Selenium/WebDriver** - Established but heavier
- **Puppeteer** (Node.js) - Good CDP alternative
- **Playwright** - Cross-browser automation
- **Hybrid approach**: Browser extension for DOM/network + Linux tools for OS control:
  - `xdotool`/`wmctl` for window/input control
  - `pynput` or `uinput` for low-level input
  - `dbus-send` for desktop service interaction

### Troubleshooting Guide
- **Connection refused**: Verify browser launched with `--remote-debugging-port`
- **Target window closed**: Re-launch browser with debugging flag
- **Profile conflicts**: Use `--user-data-dir` to isolate debugging profile
- **Missing functionality**: Agent can add helpers mid-task (self-healing property)

## Reusability Notes
This process applies whenever:
- User requests platform-specific tool
- Initial suggestions don't match user's actual OS
- Need to validate tool claims vs documentation
- Must provide equivalent functionality on user's platform

Key indicators for reusability:
- User explicitly states their OS differs from tool's assumed platform
- Tool documentation shows clear platform-specific markers
- User suggests or accepts alternatives
- Setup process involves verifiable, documented steps
- Outcome provides equivalent core functionality

## Quality Indicators for Saved Approach
Worth saving because:
1. Required trial/error: Verified Interceptor's macOS focus through doc examination
2. Changed course: Abandoned Interceptor setup when confirmed macOS-only
3. Evaluated alternative: Assessed browser-harness for Linux suitability
4. Provided actionable steps: Detailed, working setup instructions
5. Added value: Comparison matrix and troubleshooting guidance
6. Generalizable: Framework applies to future platform-mismatch scenarios

This skill prevents repetitive clarification about platform compatibility and provides a structured approach to delivering equivalent functionality on the user's actual operating system.