# Buzz collaborative agent workspace

Use this reference when operating Block Buzz as a human-and-agent workspace, especially when Hermes must chat with managed ACP agents or diagnose apparently online agents that do not reply.

## Fast answer first

For JT, lead with the current result in one or two lines before extended diagnosis. Time-box live-agent waits to about 30 seconds for a trivial test. If the relay accepted the event but no agent replied, do not stack repeated 60–90 second waits. Check one listener and restart through Buzz's supported controls. Explain deeper architecture after restoring service.

## Installed surfaces

The packaged Linux build provides:

- `buzz-desktop`: Tauri/WebKit GUI.
- `buzz`: agent-first CLI with JSON output.
- `buzz-acp`: channel/DM listener and ACP bridge.
- `buzz-agent`, `buzz-dev-mcp`, and provider-specific ACP subprocesses.

Verify the live installation rather than trusting a release page:

```bash
command -v buzz buzz-desktop buzz-acp buzz-agent
buzz --help
dpkg-query -W -f='${Package} ${Version}\n' buzz
```

The CLI needs a relay URL plus a Nostr identity. Never print, log, or persist private keys or `BUZZ_AUTH_TAG` values. Read them directly from their protected source only for the command that needs them.

## Useful CLI commands

```bash
buzz channels list
buzz channels list --member
buzz messages get --channel <UUID> --limit 50
buzz messages search --query '<text>'
buzz users get --name <agent-name>
buzz users presence --pubkeys <comma-separated-pubkeys>
buzz messages send \
  --channel <UUID> \
  --mention <agent-pubkey> \
  --content '@Agent concise request'
```

Use an explicit `--mention <pubkey>` when testing an agent. Visible `@Name` text alone is presentation text; the `p` tag is the reliable trigger identity.

## Correct round-trip verification

A successful `messages send` proves only that the relay accepted the signed event. It does not prove the agent consumed it.

1. Record the returned `event_id` and the current timestamp.
2. Poll `messages get --since <timestamp>` for a short bounded period.
3. Exclude the sent event ID. Do not grep for a marker that also appears in your request.
4. Require a new event authored by the target agent pubkey.
5. Report success only after seeing that reply event.

## Diagnosing green-but-silent agents

A green UI card or online presence is not sufficient. Check in this order:

1. Relay health and CLI read/write.
2. `buzz-acp` processes and established relay TCP/WebSocket connections.
3. The sent event's tags: channel `h` tag and target `p` tag.
4. Agent presence and channel membership.
5. Agent authorization. Managed agents may use `respond_to=owner-only`; owner resolution prefers the signed `BUZZ_AUTH_TAG`, then `BUZZ_ACP_AGENT_OWNER`.
6. Agent-side visibility. If testing with an agent identity through `buzz`, include both its private key and its signed auth tag without printing either. Omitting the auth tag can correctly produce `relay_membership_required` and is not evidence that the running harness lacks membership.
7. If all of the above pass but no mention is consumed, treat the listener/subscription as stale.

## Supported recovery for stale listeners

Prefer Buzz's own Agents UI:

1. Stop running agents.
2. Start the intended agents again, or restore all agents that were running before the test.
3. Verify fresh `buzz-acp` PIDs.
4. Send one explicit-mention round-trip test and require a real reply.

Do not repeatedly kill individual wrappers and assume the desktop will respawn them; verify actual process replacement. Preserve the user's prior running set when using a global stop/start.

## Distinguish relay layers

`relay unreachable` can refer to different paths:

- Main hosted community relay used by channels, CLI, and ACP WebSockets.
- Desktop-native MeshLLM discovery/status heartbeat.
- Local self-host default relay when no hosted relay is configured.

Check the main relay independently with health/HTTP, CLI channel listing, event acceptance, and live ACP connections. If those pass while logs say `buzz-mesh: status report ... relay unreachable`, the message is from the auxiliary mesh status path, not proof that normal chat is down.

## Latency diagnosis

Measure instead of guessing:

- Relay latency: repeated `/health` requests.
- End-to-end latency: target reply `created_at` minus sent event `created_at`.
- Separate cold first-turn latency from warm turns.

If the relay is sub-second but replies take tens of seconds, likely contributors are ACP session creation, full agent context/tool loading, provider latency, and high reasoning effort. For routine Buzz chat, prefer medium effort or a lighter model; reserve high effort for difficult coding/research.

## Pitfalls

- Claiming agents can chat because their cards are green.
- Matching the test marker in your own request and calling it a reply.
- Forgetting `BUZZ_AUTH_TAG` when testing with a managed-agent identity.
- Letting an agent auth tag remain exported while switching back to the owner's identity. Explicitly `unset BUZZ_AUTH_TAG` before owner CLI calls.
- Waiting through several long timeouts before trying one supported listener restart.
- Treating an auxiliary mesh heartbeat error as a total hosted-relay outage.
