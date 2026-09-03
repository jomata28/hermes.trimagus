# OpenCode with an OpenAI-Compatible Router

Use this when updating OpenCode, testing a newly exposed router model, or making the same model available as a Hermes backend.

## 1. Identify the active OpenCode install

OpenCode can exist in multiple install lineages. Verify the binary that the current shell actually resolves before and after updating:

```bash
command -v opencode
opencode --version
type -a opencode
```

Prefer OpenCode's own updater for a self-managed/curl installation:

```bash
opencode upgrade
hash -r
command -v opencode
opencode --version
```

Do not automatically delete, overwrite, or symlink every other `opencode` binary. A second copy may belong to another Unix user or an older, incompatible project. The success criterion is that the intended user's `PATH` resolves to the updated CLI.

## 2. Discover and smoke-test the router model

Never assume the model ID. Query OpenCode's live catalog and filter it:

```bash
opencode models 2>&1 | grep -i -E 'glm|z-ai|zhipu'
```

Run the model in an empty temporary directory so the smoke test cannot modify a real repository:

```bash
mkdir -p /tmp/opencode-model-smoke
opencode run -m <provider/model-id> \
  'Reply with exactly: MODEL_SMOKE_OK'
```

Verify both the process exit code and the literal response. The display banner may normalize the model name; use the requested catalog ID for subsequent commands unless the provider documentation says otherwise.

## 3. Reuse the router directly from Hermes

OpenCode and Hermes do not proxy through each other. If both support the same OpenAI-compatible router, configure Hermes directly against that router.

Define a named provider in `~/.hermes/config.yaml` (prefer `key_env` so the secret remains in `.env`):

```yaml
providers:
  my-router:
    name: My Router
    api: https://router.example/v1
    key_env: MY_ROUTER_API_KEY
    transport: chat_completions
    default_model: vendor/model-name
```

Use `hermes config set` rather than hand-editing when practical:

```bash
hermes config set providers.my-router.name 'My Router'
hermes config set providers.my-router.api 'https://router.example/v1'
hermes config set providers.my-router.key_env 'MY_ROUTER_API_KEY'
hermes config set providers.my-router.transport 'chat_completions'
hermes config set providers.my-router.default_model 'vendor/model-name'
```

First test without changing the default:

```bash
hermes chat --provider my-router -m vendor/model-name \
  -q 'Reply with exactly: HERMES_MODEL_OK' --max-turns 2 -Q --source tool
```

Then test actual agent/tool behavior, not only text completion:

```bash
hermes chat --provider my-router -m vendor/model-name -t terminal --yolo \
  -q 'You must call terminal once to execute: printf TOOL_OK. After observing its output, reply exactly: TOOL_OK' \
  --max-turns 4 -Q --source tool
```

Inspect the saved session transcript and confirm it contains an assistant `tool_call`, a real tool result, and the final response. A model echoing `TOOL_OK` without a tool call is not a valid agent smoke test.

Only after both checks pass, switch defaults:

```bash
hermes config set model.provider my-router
hermes config set model.default 'vendor/model-name'
```

Keep a known-good fallback provider configured. Model/provider changes apply to new Hermes sessions; they do not replace the model already running the current conversation. Restart the gateway separately only when messaging-platform traffic must reload the new default.