---
name: data-science-workflows
description: "Class-level workflows for exploratory data science: live notebooks, iterative Python state, dataframe/API exploration, reproducible analysis, and clean verification."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [data-science, jupyter, notebook, python, dataframe, exploration, analysis, reproducibility]
---

# Data science workflows

Use this umbrella when the user asks for exploratory analysis, notebook-style iteration, dataframe/API inspection, plots, model/data experiments, or any workflow where preserving Python state across steps is useful.

This umbrella absorbs the former `jupyter-live-kernel` skill as the live-kernel subsection. Keep future narrow data-analysis incident notes as `references/<topic>.md`, reusable notebooks/templates as `templates/`, and statically re-runnable probes as `scripts/`.

## Route by analysis mode

| User asks for | Use |
|---|---|
| Quick one-shot computation or script with Hermes tool access | `execute_code` or `terminal` |
| Iterative exploration where variables should persist | Live Jupyter kernel subsection below |
| Deliverable notebook/report | Create or update a notebook, then restart/run-all for clean verification |
| Package/API/dataframe investigation | Use a live kernel when repeated inspection beats one-off scripts |

## Live Jupyter kernel workflow

Use a stateful Jupyter kernel when you would otherwise want a notebook or REPL: incremental analysis, object inspection, dataframe transformations, exploratory plotting, or debugging code over multiple executions.

Prerequisites and setup from the absorbed package:

```bash
# uv should be installed
which uv

# install JupyterLab if needed
uv tool install jupyterlab

# hamelnb script location used by the former skill
SCRIPT="$HOME/.agent-skills/hamelnb/skills/jupyter-live-kernel/scripts/jupyter_live_kernel.py"

# clone if absent
git clone https://github.com/hamelsmu/hamelnb.git ~/.agent-skills/hamelnb
```

Start or discover a server:

```bash
uv run "$SCRIPT" servers --compact
jupyter-lab --no-browser --port=8888 --notebook-dir=$HOME/notebooks \
  --IdentityProvider.token='' --ServerApp.password='' > /tmp/jupyter.log 2>&1 &
```

Create a scratch notebook/session if needed:

```bash
mkdir -p ~/notebooks
curl -s -X POST http://127.0.0.1:8888/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"path":"scratch.ipynb","type":"notebook","name":"scratch.ipynb","kernel":{"name":"python3"}}'
```

Core commands:

```bash
uv run "$SCRIPT" notebooks --compact
uv run "$SCRIPT" execute --path scratch.ipynb --code 'import pandas as pd' --compact
uv run "$SCRIPT" variables --path scratch.ipynb list --compact
uv run "$SCRIPT" variables --path scratch.ipynb preview --name df --compact
uv run "$SCRIPT" contents --path scratch.ipynb --compact
uv run "$SCRIPT" restart-run-all --path scratch.ipynb --save-outputs --compact
```

## Operational rules

1. Use `--compact` on hamelnb commands to keep output small.
2. Retry once on first-execution or websocket timeouts; kernels often need a moment after server start or restart.
3. Remember that package installs must target the JupyterLab tool environment, not necessarily the shell Python used by Hermes tools.
4. Keep subcommand flags before sub-subcommands: `variables --path nb.ipynb list`, not `variables list --path nb.ipynb`.
5. For clean deliverables, verify by restarting the kernel and running all cells top-to-bottom.
6. Label assumptions and data provenance in the final notebook/report; do not silently fabricate missing rows or API responses.
