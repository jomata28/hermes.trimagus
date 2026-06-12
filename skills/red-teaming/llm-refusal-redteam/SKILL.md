---
name: llm-refusal-redteam
description: "Use when evaluating or modifying LLM refusal behavior: prompt-level jailbreak/red-team probes, refusal detection, and weight-level refusal-direction abliteration/model surgery."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [red-teaming, refusals, jailbreaks, model-surgery, uncensoring, evaluation]
    related_skills: []
---

# LLM Refusal Red-Team Workflows

## Overview

This umbrella covers the class of work around LLM refusal behavior. It includes prompt/API red-team probes, refusal detection, jailbreak-template experiments, and model-weight refusal-direction analysis or abliteration. Use it to reason about the whole refusal-behavior workflow instead of loading separate session- or technique-named skills.

## When to Use

- Testing whether a model refuses, over-refuses, or follows a policy boundary.
- Building or running jailbreak/prompt-red-team probes in an authorized evaluation context.
- Detecting refusals in outputs and comparing bypass approaches.
- Performing model surgery such as diff-in-means refusal-direction removal/abliteration.

## Workflow Selector

| Need | Subworkflow |
|---|---|
| Black-box model behavior probe | Prompt/API red-team evaluation |
| Compare refusal wording or detect refusals at scale | Refusal detection and scoring |
| Study or modify open model internal refusal directions | Model-surgery / abliteration workflow |
| Preserve exact historical templates/scripts | Consult demoted source packages |

## Prompt/API Red-Team Evaluation

Define the authorized target, model, policy boundary, and success/failure criteria. Run minimal probes first, log prompts/responses, and avoid claiming bypass success without captured model output.

## Refusal Detection

Use explicit heuristics or classifiers for refusal phrases, hedging, policy redirects, and partial compliance. Measure false positives against benign tasks before using the detector as a benchmark.

## Model-Surgery / Abliteration

For open weights, use small reproducible runs before full checkpoints: load model/tokenizer, collect contrasting activation sets, estimate refusal directions, apply projection/removal, and evaluate both refusal reduction and capability degradation.

## Demoted Source Packages

Full source packages are preserved for detailed templates, scripts, and reference material:

- `references/godmode-package/`
- `references/obliteratus-package/`

## Common Pitfalls

1. **No authorization boundary.** Do not run red-team probes against systems the user is not allowed to test.
2. **Confusing one anecdote with an eval.** Preserve prompts, outputs, model IDs, and pass/fail criteria.
3. **Breaking general capability.** Model surgery must include utility regression checks, not only refusal-rate changes.
4. **Losing provenance.** Keep original templates/scripts as references.

## Verification Checklist

- [ ] Target model/system and authorization are clear.
- [ ] Prompt or weight-level workflow is selected deliberately.
- [ ] Outputs, scores, or checkpoint paths are recorded.
- [ ] Safety/capability regression checks are included for modifications.
