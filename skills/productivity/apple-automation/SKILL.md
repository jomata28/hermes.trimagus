---
name: apple-automation
description: "Use when working with Apple ecosystem automation from Hermes: Notes, Reminders, iMessage/SMS, Find My devices, and macOS desktop computer-use tooling."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [apple, macos, notes, reminders, imessage, findmy, computer-use]
    related_skills: []
---

# Apple Automation

## Overview

This umbrella covers Apple-specific workflows that require macOS-only tools or Apple account state. Treat Apple automation as a platform class: first verify the session is running on macOS or has access to a macOS host, then choose the narrow tool subsection below.

## When to Use

- The user asks to create/search/edit Apple Notes.
- The user asks to add/list/complete Apple Reminders.
- The user asks to send/read iMessage or SMS.
- The user asks to locate Apple devices or AirTags via Find My.
- The user asks for GUI-level macOS computer use through screenshots, mouse, keyboard, scrolling, or drag actions.

Do not use this on Linux-only hosts unless a remote macOS bridge/tool is already configured.

## Platform Gate

1. Check the live OS before assuming Apple tooling exists.
2. If the current host is not macOS, look for configured CLI bridges or remote access instead of inventing commands.
3. Prefer the purpose-built CLI for the domain before falling back to GUI automation.

## Notes

Use the memo CLI class for Apple Notes. Typical actions are create, search, and edit. Preserve note titles exactly and verify writes by reading/searching after changes.

## Reminders

Use remindctl class tooling for Apple Reminders. Typical actions are add, list, complete, and inspect reminder lists. Confirm list names before writing into a non-default list.

## Messages

Use imsg class tooling for iMessage/SMS. When the user names a recipient, resolve the target carefully before sending. For any ambiguous person/channel, list or verify available contacts first.

## Find My

Use FindMy.app/macOS access for Apple devices and AirTags. Report location uncertainty, freshness, and device identity; do not imply real-time precision if the data is stale.

## macOS Computer Use

Use background-safe desktop automation when CLI APIs are not enough. Avoid stealing the user's active cursor/focus when a background computer-use bridge is available. Capture screenshots before and after high-impact actions.

## Common Pitfalls

1. Assuming Apple tools work on Linux. Always check the host/bridge first.
2. Sending messages without resolving the recipient.
3. Treating stale Find My data as current.
4. Using GUI automation when a safer domain CLI exists.

## Verification Checklist

- [ ] Live platform or macOS bridge verified.
- [ ] Target account/list/contact/device identified.
- [ ] Action performed with the least invasive tool.
- [ ] Result verified by readback, screenshot, or tool output.
