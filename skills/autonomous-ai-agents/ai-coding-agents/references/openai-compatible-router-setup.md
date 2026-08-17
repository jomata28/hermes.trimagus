# OpenAI-Compatible Router Setup and Verification

Use this for third-party OpenAI-compatible routers used by Hermes or external coding agents.

## Safe setup sequence

1. Confirm the official API base URL and supported wire format from the provider’s own documentation.
2. Do not switch the active/main model during discovery. Add the router as a named secondary provider first.
3. Store the secret in the harness credential store or `.env`; reference it by environment-variable name from configuration. Do not embed the secret in YAML, prompts, shell history, or test output.
4. Probe `GET <base_url>/models` with bearer auth. Record only HTTP status, model count, and IDs; never print the key.
5. Configure a named custom provider with:
   - stable name;
   - base URL ending in `/v1` when documented;
   - `key_env` pointing to the secret;
   - explicit `chat_completions` transport when the endpoint is OpenAI-compatible.
6. Parse the resulting YAML and verify the provider collection is a real list/map rather than a quoted JSON string. Some generic `config set` commands accept the text but serialize structured input as a scalar. Prefer the interactive model/provider wizard when available.
7. Confirm the primary provider/model is unchanged.
8. Run a real harness smoke test through the named provider and require a deterministic response marker.
9. Only after success offer to add the router as a fallback or make it primary.

## Hermes named-provider shape

```yaml
custom_providers:
  - name: example-router
    base_url: https://api.example.com/v1
    key_env: EXAMPLE_ROUTER_API_KEY
    api_mode: chat_completions
```

CLI smoke-test pattern:

```bash
hermes chat -q 'Reply with exactly: ROUTER_OK' \
  --provider custom:example-router \
  -m router/auto -Q
```

A successful direct `curl` is not sufficient; test the Hermes/runtime resolution path too.

## OrcaRouter verified details

- Official base URL: `https://api.orcarouter.ai/v1`
- Keys use the `sk-orca-` prefix.
- `/v1/models` exposes router IDs such as `orcarouter/auto`, `orcarouter/fusion`, `orcarouter/fusion-flash`, and upstream model IDs.
- A named Hermes provider can use `name: orcarouter`, `key_env: ORCAROUTER_API_KEY`, and `api_mode: chat_completions`.
- Successful verification requires both authenticated `/models` retrieval and a real `hermes chat --provider custom:orcarouter ...` response.

## Secret exposure response

If a key was pasted into Telegram, Slack, email, a ticket, or any persisted chat:

1. Do not repeat it in responses or logs.
2. Finish only the minimum validation the user requested.
3. Tell the user the channel retained the secret and recommend rotating it.
4. Update the replacement through a hidden terminal prompt or provider credential command rather than asking them to paste it again.
