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

## X / Twitter via xurl

Use the official `xurl` CLI for API calls. Preserve tweet IDs, media IDs, user IDs, and endpoint paths. For media posts, upload media first, then reference the media ID in the create-post call.

## Yuanbao Groups

In Yuanbao contexts, the final assistant reply is the delivered message. Use explicit @mention syntax only when needed and avoid calling unrelated send tools unless the workflow requires a cross-platform send.

## Demoted Source Packages

Full source packages preserved for exact platform syntax:

- `references/xurl-package/`
- `references/yuanbao-package/`

## Common Pitfalls

1. **Sending twice.** Gateway-delivered chats may not need a separate send call.
2. **Ambiguous targets.** Resolve group/user/thread IDs before posting.
3. **Assuming auth.** Check CLI credentials before composing irreversible posts.
4. **Forgetting returned IDs.** Include post/message IDs when available.

## Verification Checklist

- [ ] Target platform and recipient/post context are unambiguous.
- [ ] Credentials/tool availability verified for API actions.
- [ ] Writes return IDs/status or a clear blocker is reported.
