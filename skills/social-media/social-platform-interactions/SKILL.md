---
name: social-platform-interactions
description: "Use when interacting with social or chat platforms from Hermes: X/Twitter API posting/search/DM/media via xurl, and Yuanbao group/direct messaging conventions."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [social-media, messaging, x, twitter, yuanbao, chat]
    related_skills: []
---

# Social Platform Interactions

## Overview

Use this umbrella for platform-specific social/chat actions where the agent must respect delivery mechanics, authentication, platform IDs, and API limitations.

## When to Use

- X/Twitter posting, search, DMs, media upload, or v2 API work through `xurl`.
- Yuanbao (元宝) group/direct interactions, @mentions, querying group/member info, or understanding gateway delivery behavior.
- Similar social platform tasks where the final response may itself be delivered to a group/user.

## Shared Workflow

1. Identify the platform and exact target (home channel, group, DM, post, thread, or API endpoint).
2. Verify configured CLI/tool credentials before write actions.
3. For channels/people, list available targets when the user names a specific destination.
4. For API writes, dry-run or inspect payloads where possible, then verify returned IDs/status.
5. Remember that some gateways deliver the assistant's final text directly; do not double-send unless the platform requires a send tool.
6. For private/paywalled platform content (e.g. Substack), use a user-driven remote browser login rather than requesting credentials. See `references/private-platform-novnc-auth.md` for noVNC auth setup, password-file pitfalls, and display debugging.

## Substack Private/Paid Content

Use when JT wants help reading, summarizing, or extracting private/paid Substack content. First try the public URL if available; if it is paywalled/private, use a temporary remote browser/noVNC auth flow so JT enters credentials directly. Do not ask him to paste passwords or magic-link contents in chat. After access, close any public tunnel unless he explicitly asks to keep the remote view open.

Detailed workflow: `references/substack-private-content-auth.md`.

## X / Twitter via xurl

Use the official `xurl` CLI for API calls. Preserve tweet IDs, media IDs, user IDs, and endpoint paths. For media posts, upload media first, then reference the media ID in the create-post call.

## Yuanbao Groups

In Yuanbao contexts, the final assistant reply is the delivered message. Use explicit @mention syntax only when needed and avoid calling unrelated send tools unless the workflow requires a cross-platform send.

## Demoted Source Details

Former platform-specific skills were absorbed as support material for exact syntax:

- `references/xurl-details/overview.md` — X/Twitter `xurl` posting, search, DM, media, and v2 API examples.
- `references/yuanbao-details/overview.md` — Yuanbao group/direct target conventions and @mention syntax.

## Private / Paid Content via Remote Browser

Use this pattern for platforms such as Substack where content may be paid/private and API access is unavailable:

1. Try the public URL first only if it is safe and useful; expect paid content to require login.
2. Prefer a remote browser/noVNC flow where the user types credentials directly. Never ask them to paste passwords into chat.
3. Keep the remote view temporary and explicit: give the URL, state which password prompt it is (noVNC vs platform login), and ask the user to say when logged in.
4. If reusing an existing VNC/noVNC stack, verify which `x11vnc` process and password file are actually bound to the exposed port before giving a password. Existing VPS-screen services may ignore a newly generated password file.
5. For clean temporary access, use a separate VNC/websockify/cloudflared port pair rather than fighting the persistent VPS screen stack; verify with process/port checks and an HTTP 200 probe before sending the link.
6. After the private-content task is finished, close the public tunnel and any temporary browser/VNC processes unless the user says to keep them running.

See `references/remote-browser-auth.md` for the detailed noVNC/cloudflared checklist and pitfalls.

## Common Pitfalls

1. **Sending twice.** Gateway-delivered chats may not need a separate send call.
2. **Ambiguous targets.** Resolve group/user/thread IDs before posting.
3. **Assuming auth.** Check CLI credentials before composing irreversible posts.
4. **Forgetting returned IDs.** Include post/message IDs when available.
5. **Password mismatch in noVNC auth.** A generated password is useless if the active `x11vnc` process is still using another password file; inspect the live process and bound port before telling the user what to enter.
6. **Self-killing with `pkill -f`.** Broad `pkill -f` patterns can match the current shell command. Prefer tracked process IDs, narrower patterns, or fresh unused ports.

## Verification Checklist

- [ ] Target platform and recipient/post context are unambiguous.
- [ ] Credentials/tool availability verified for API actions.
- [ ] For private content, the user authenticated directly in the browser; no platform password was pasted into chat.
- [ ] Remote auth links were verified reachable before sending.
- [ ] The exposed tunnel/processes were cleaned up or intentionally left running at the user's request.
- [ ] Writes return IDs/status or a clear blocker is reported.
