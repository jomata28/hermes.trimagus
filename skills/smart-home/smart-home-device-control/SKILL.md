---
name: smart-home-device-control
description: "Class-level workflow for controlling smart-home devices from Hermes: discovery, safe command execution, scenes, schedules, and Philips Hue/OpenHue operations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [smart-home, home-automation, hue, lights, scenes, iot, scheduling]
---

# Smart-home device control

Use this umbrella when the user asks Hermes to control, inspect, schedule, or troubleshoot smart-home devices. It currently absorbs the former `openhue` skill as the Philips Hue / OpenHue subsection and should be expanded with future Home Assistant, Matter, Zigbee, or vendor-specific workflows as labeled subsections rather than separate micro-skills.

## Safety and confirmation rules

- Low-risk reversible actions like turning lights on/off, changing brightness, or activating a scene can be executed directly when the user asks clearly.
- Ask before disruptive or persistent changes: changing automations, deleting scenes, pairing/unpairing bridges, altering schedules, or exposing devices to a network.
- Discover exact device/room names before acting when the user uses a vague label.
- Report real command output or confirmed state; do not claim a device changed if the CLI/API failed.

## Philips Hue via OpenHue

Use OpenHue for Hue Bridge light, room, and scene control from the terminal.

Prerequisites:

```bash
# Linux pre-built binary
curl -sL https://github.com/openhue/openhue-cli/releases/latest/download/openhue-linux-amd64 \
  -o ~/.local/bin/openhue && chmod +x ~/.local/bin/openhue

# macOS
brew install openhue/cli/openhue-cli
```

First run requires pressing the physical Hue Bridge button. The bridge must be on the same local network as the machine running Hermes.

### Discovery commands

```bash
openhue get light
openhue get room
openhue get scene
```

Use these before controlling a device if names are unknown. Light and room names can be case-sensitive.

### Common controls

```bash
# individual light
openhue set light "Bedroom Lamp" --on
openhue set light "Bedroom Lamp" --off
openhue set light "Bedroom Lamp" --on --brightness 50
openhue set light "Bedroom Lamp" --on --temperature 300
openhue set light "Bedroom Lamp" --on --color red
openhue set light "Bedroom Lamp" --on --rgb "#FF5500"

# room
openhue set room "Bedroom" --off
openhue set room "Bedroom" --on --brightness 30

# scenes
openhue set scene "Relax" --room "Bedroom"
openhue set scene "Concentrate" --room "Office"
```

### Useful presets

```bash
# Bedtime: dim warm
openhue set room "Bedroom" --on --brightness 20 --temperature 450

# Work mode: bright cool
openhue set room "Office" --on --brightness 100 --temperature 250

# Movie mode: dim
openhue set room "Living Room" --on --brightness 10
```

## Troubleshooting

- If commands fail before pairing, instruct the user to press the Hue Bridge button and rerun the OpenHue auth/discovery command.
- If a color command fails, verify the target bulb is color-capable; white-only bulbs support brightness and temperature only.
- If a device is not found, run discovery and use the exact name returned by the bridge.
- For scheduled lighting, use Hermes cron jobs only after verifying the command works interactively.
