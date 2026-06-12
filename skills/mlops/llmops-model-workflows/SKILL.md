---
name: llmops-model-workflows
description: "Use when working across the LLM/model operations lifecycle: Hugging Face Hub discovery/download/upload, local GGUF/llama.cpp inference, quantization, and experiment tracking with W&B."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mlops, llmops, huggingface, llama-cpp, gguf, wandb, experiment-tracking]
    related_skills: []
---

# LLMOps Model Workflows

## Overview

This umbrella covers the model lifecycle around open models: find artifacts on Hugging Face, download or publish repos, run local inference/serving with GGUF and llama.cpp, choose quantizations, and track experiments/sweeps/artifacts with Weights & Biases.

## When to Use

- Searching, downloading, uploading, or managing Hugging Face models/datasets/spaces.
- Running local inference with llama.cpp, `llama-cpp-python`, GGUF files, or model servers.
- Choosing quantization formats or troubleshooting CPU/GPU/Apple Silicon inference.
- Logging ML experiments, sweeps, model registry entries, dashboards, or artifacts in W&B.

## Shared Workflow

1. Clarify the lifecycle stage: discovery, download, conversion, quantization, inference, evaluation, tracking, or publication.
2. Verify installed tools (`hf`, Python packages, llama.cpp binaries, `wandb`) and credentials before assuming availability.
3. Prefer stable model repo IDs, revisions, filenames, run IDs, and artifact versions in outputs.
4. Start with a small smoke test before long downloads, conversions, or sweeps.
5. Report hardware constraints, memory estimates, and exact commands used.

## Hugging Face Hub

Use `hf` for repo discovery, login, downloads, uploads, and dataset/model management. Capture repo IDs, revisions, and local paths. Avoid the deprecated `huggingface-cli` unless the environment only has the older command.

## llama.cpp / GGUF

For local inference, choose a model file and quantization that fits memory. Verify with a one-prompt smoke test before serving or benchmarking. Track server host/port and model path in the response.

## Weights & Biases

For experiments, initialize the project/entity, log config/metrics/artifacts, and preserve run URLs/IDs. For sweeps, start with a minimal config and verify the agent reports metrics before scaling.

## Demoted Source Packages

Full source packages preserved for detailed commands, reference pages, and templates:

- `references/huggingface-hub-package/`
- `references/llama-cpp-package/`
- `references/weights-and-biases-package/`

Use these for exact syntax and deeper troubleshooting while this umbrella remains the class-level trigger.

## Common Pitfalls

1. **Downloading before checking disk/VRAM.** Estimate model and quantization size first.
2. **Confusing repo IDs with filenames.** Report both when relevant.
3. **Skipping auth checks.** Private HF/W&B resources fail late without tokens.
4. **Running large sweeps unverified.** Smoke-test one run.

## Verification Checklist

- [ ] Tooling and credentials are available or blocker is explicit.
- [ ] Model/dataset/run/artifact IDs are recorded.
- [ ] A small inference/download/logging smoke test succeeded before scale-up.
- [ ] Final answer includes exact paths, URLs, or run IDs.
