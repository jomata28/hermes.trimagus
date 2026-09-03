# OpenCode Go subscription setup

Use this when the user expects Kimi or GLM access through OpenCode's low-cost subscription rather than a separate pay-as-you-go router.

## Distinguish the three cost surfaces

- **OpenCode CLI** is free/open source; that does not make every provider free.
- Provider/model IDs under `opencode/...-free` are the anonymous free catalog.
- `opencode-go/<model>` uses the $10/month OpenCode Go subscription and its rolling/weekly/monthly allowance.
- `orcarouter/<model>` or another provider prefix uses that provider's key and billing, even when invoked from OpenCode.
- OpenCode Zen is a separate metered credit balance. Do not describe Go, Zen, and the anonymous catalog as interchangeable.

Always inspect the full model ID/provider prefix before making a cost claim:

```bash
opencode models opencode
opencode models opencode-go
opencode models 2>&1 | grep -i -E 'glm|kimi'
```

A successful command such as `opencode run -m orcarouter/z-ai/glm-5.3 ...` proves model compatibility, but it does **not** test the Go allowance.

## Authenticate OpenCode CLI

```bash
opencode providers login --provider opencode-go
opencode providers list
opencode models opencode-go
```

The login prompt needs a real PTY. In Hermes background-process automation, wait until `Enter your API key` appears, then send the key and carriage return in one raw write (`<key>\r`). Sending the key with a line-feed and later sending carriage return can create an empty final line and trigger `Required`.

Never print the key in verification output. If the user pasted it in chat, recommend rotation after setup.

## Verify the subscribed route

Use a harmless empty directory and an exact-response smoke test:

```bash
opencode run -m opencode-go/glm-5.3 'Reply with exactly: OPENCODE_GO_CLI_OK'
```

Verify that output identifies the Go model, not an identically named model behind another provider.

## Use OpenCode Go directly from Hermes

Hermes has a first-class `opencode-go` provider. Store credentials through the auth CLI rather than adding the secret inline to `config.yaml`:

```bash
hermes auth add opencode-go --type api-key --label 'OpenCode Go'
hermes chat --provider opencode-go -m glm-5.3 -q 'Reply with exactly: OPENCODE_GO_GLM_OK' -Q --source tool
```

After inference succeeds, test native tool calling before making it the default. Inspect the resulting session with tool-role messages to prove the model actually issued a tool call rather than merely repeating the requested sentinel.

Then persist:

```bash
hermes config set model.provider opencode-go
hermes config set model.default glm-5.3
```

Existing Hermes conversations retain the model selected at session start. Start `/new` or relaunch Hermes to use the new default. Preserve a known-good fallback provider when possible.

## Verification checklist

- [ ] `opencode providers list` shows OpenCode Go credential.
- [ ] `opencode models opencode-go` contains the requested Kimi/GLM ID.
- [ ] OpenCode smoke test uses the `opencode-go/` prefix.
- [ ] Hermes explicit-provider smoke test succeeds.
- [ ] Hermes model performs a real tool call through Go.
- [ ] Default provider/model changed only after those tests pass.
- [ ] User is told that Go is subscription-limited, not unlimited/free.
