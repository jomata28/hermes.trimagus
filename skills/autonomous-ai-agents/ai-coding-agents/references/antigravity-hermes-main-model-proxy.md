# Antigravity as Hermes main model (agy-proxy)

Session-proven pattern for making Google Antigravity (`agy`) models selectable as Hermes' primary provider when Hermes has no first-party `google-antigravity` auth/provider entry.

## Why this exists

- `hermes auth add google-antigravity --type oauth` fails with `Unknown provider`.
- `hermes model` only lists Hermes providers; Antigravity does not appear there natively.
- `agy` owns its own Google OAuth state and model catalog (`agy models`).
- JT's ask: use agy models as Hermes main backend, not only as a spawned worker CLI.

## Architecture

```
Hermes session
  → OpenAI Chat Completions client
    → http://127.0.0.1:9777/v1
      → agy-proxy (stdlib HTTP)
        → /root/.local/bin/agy --print <prompt> --model <id> --dangerously-skip-permissions
```

Hermes sees a normal custom OpenAI-compatible provider. Credentials are dummy local (`agy-local`); real auth lives inside `agy`.

## Durable locations on JT's VPS

| Piece | Location / value |
|---|---|
| Proxy code | `/root/agy-proxy/proxy.py` |
| Process manager | PM2 app `agy-proxy` |
| Listen | `127.0.0.1:9777` |
| Config backup before switch | `/root/.hermes/config.yaml.bak-pre-agy` |
| Hermes provider name | `antigravity` |
| Verified default model | `gemini-3.5-flash-medium` |

## Hermes config shape

```yaml
providers:
  antigravity:
    name: Google Antigravity (agy)
    base_url: http://127.0.0.1:9777/v1
    api: http://127.0.0.1:9777/v1
    api_key: agy-local
    default_model: gemini-3.5-flash-medium
    api_mode: chat_completions
    transport: chat_completions

model:
  provider: antigravity
  default: gemini-3.5-flash-medium
  base_url: http://127.0.0.1:9777/v1
  api_mode: chat_completions
  api_key: agy-local
```

## Implementation rules that mattered

1. **Prefer stdlib HTTP** over nested FastAPI/Pydantic route models. Nested `BaseModel` bodies inside `make_app()` crashed OpenAPI/schema generation with:
   `PydanticUserError ... ForwardRef('Request') is not fully defined`.
2. **Bind before `agy models`**. Synchronous model enumeration can hang/timeout and leave the port unbound while PM2 reports the process "online". Seed fallback model IDs, bind immediately, refresh catalog in a background thread.
3. **Require `allow_reuse_address = True`** (or equivalent) for fast restarts after crash/kill.
4. **Reject `stream: true`** with an explicit 400 or force Hermes to non-streaming. `agy --print` is not a token stream.
5. Headless worker calls need:
   ```bash
   agy --print '...' --model <id> --print-timeout 5m --dangerously-skip-permissions
   ```
6. Tools are **prompt-serialized**, not native Hermes tool calls. Expect imperfect tool use; treat this as a model backend bridge, not a full transport family.

## Verification sequence

```bash
# proxy live
curl -sS http://127.0.0.1:9777/health
curl -sS http://127.0.0.1:9777/v1/models | python3 -m json.tool | head

# direct completion
curl -sS http://127.0.0.1:9777/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"gemini-3.5-flash-medium","messages":[{"role":"user","content":"Reply with exactly: AGY_OK"}],"stream":false}'

# Hermes one-shot
hermes chat -q 'Reply with exactly: HERMES_AGY_OK' -Q \
  --provider antigravity -m gemini-3.5-flash-medium
```

Success signals observed:
- proxy health `{"status":"ok"}`
- completion content `AGY_OK`
- Hermes reply `HERMES_AGY_OK`
- Hermes warning that streaming is unsupported then falling back to non-streaming is OK

## Known models (agy catalog at time of install)

- `gemini-3.6-flash-high|medium|low`
- `gemini-3.5-flash-high|medium|low`
- `gemini-3.1-pro-high|low`
- `claude-sonnet-4-6`
- `claude-opus-4-6-thinking`
- `gpt-oss-120b-medium`

## Ops notes

- New Hermes **CLI** sessions re-read model config without gateway restart.
- Long-lived **PM2 gateway** (`hermes`) should be restarted after provider switch if Telegram/gateway must adopt stats:
  `pm2 restart hermes --update-env` (or ask JT for `/restart`).
- Keep prior provider in `fallback_providers` so a dead local proxy does not leave JT without a model.
- Do not store Google OAuth codes in skills/memory.

## Pitfalls

- Pasting an auth code generated from a **previous** OAuth URL fails with `invalid_grant: Invalid code verifier`.
- dual proxy listeners: an old manual `python proxy.py` can hold `:9777` while PM2 marks a second instance online then fail bind (`Address already in use`). Confirm with `ss -tlnp | grep 9777` and that health responds.
- FastAPI proxy was a dead end for this bridge on the observed pydantic/fastapi pair; stick to stdlib unless a carefully freeze-schema design is added afterward.
