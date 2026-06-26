---
name: creative-production-workflows
description: "Umbrella for creative production workflows: humanized prose, infographics, Manim explainers, and ComfyUI generative media."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative, writing, infographic, manim, animation, comfyui, image-generation, video-generation, humanize]
---

# Creative production workflows

Use this umbrella when the user asks Hermes to create or polish a creative artifact: prose that should sound human, an infographic or visual summary, a programmatic explainer animation, or advanced image/video generation through ComfyUI.

This skill consolidates the former standalone packages `humanizer`, `baoyu-infographic`, `manim-video`, and `comfyui`. Their complete packages, including support files, are preserved under `references/<package>-package/`.

## Route by artifact type

| User asks for | Use subsection | Full package reference |
|---|---|---|
| Humanize / de-AI / rewrite in a natural voice | Humanized prose editing | `references/humanizer-package/SKILL.md` |
| Infographic, visual summary, 信息图, 可视化 | Infographic generation | `references/baoyu-infographic-package/SKILL.md` |
| 3Blue1Brown-style explainer, math animation, algorithm visualization | Manim video production | `references/manim-video-package/SKILL.md` |
| ComfyUI, Stable Diffusion, Flux, SDXL, workflow JSON, custom nodes/models | ComfyUI generative media | `references/comfyui-package/SKILL.md` |

## Humanized prose editing

Load the preserved humanizer package when text should sound less like an LLM. Scan for AI tells: significance inflation, vague authorities, promotional phrasing, rule-of-three padding, em-dash overuse, bold inline headers, sycophantic chat artifacts, generic conclusions, and signposting. Preserve meaning, match the requested voice, and do a final read-aloud pass for rhythm.

For file edits, read the target file, apply targeted patches when possible, and show the changed section or diff. If the user provides a voice sample, analyze sentence length, punctuation habits, paragraph starts, and preferred word choice before rewriting.

## Infographic generation

Use the infographic workflow for high-density visual summaries. Preserve source facts exactly, strip secrets, choose a layout and style, then assemble a generation prompt from the package references. The preserved package contains the full 21-layout × 21-style gallery under `references/baoyu-infographic-package/references/layouts/` and `references/baoyu-infographic-package/references/styles/`.

Default path:
1. Analyze source content and audience.
2. Build structured content with title, objectives, sections, data points, and labels.
3. Recommend layout/style/aspect options, using keyword shortcuts when present.
4. Generate the image prompt and call the image generation tool.
5. Report layout, style, aspect, language, and output files.

## Manim video production

Use Manim for educational animations, math/algorithm explainers, architecture diagrams, and paper explainers. Plan before coding: narrative arc, misconception, aha moment, scene list, color palette, and voiceover/subtitle script. Every scene should be independently renderable and visually QA'd.

Core loop:
1. Write `plan.md` with scene breakdown and visual language.
2. Write one Python script with one class per scene.
3. Render drafts with `manim -ql`, stitch with ffmpeg, then render final quality only after QA.
4. Inspect preview stills/video for clutter, timing, readability, and style consistency.

The preserved package includes references for animations, mobjects, equations, graphs, 3D cameras, rendering, troubleshooting, and production checklists.

## ComfyUI generative media

Use ComfyUI for advanced image/video/audio generation, custom workflow execution, model/node management, and parameter sweeps. First decide local vs cloud. For local setup, run a hardware check before installing; for cloud, require a Comfy Cloud API key and paid tier for workflow execution.

Execution pattern:
1. Ensure workflow JSON is API format, not editor format.
2. Extract controllable parameters and dependencies.
3. Check/fix missing nodes and models.
4. Run workflow or batch script, monitoring via REST/WebSocket.
5. Download and present output files; fetch logs on failure.

The complete scripts and example workflows are preserved under `references/comfyui-package/scripts/` and `references/comfyui-package/workflows/`.

## Package integrity rule

Do not flatten these preserved packages further unless you re-home every needed support file and rewrite internal paths. The original package directories were copied intact so relative links such as `references/...`, `scripts/...`, and `workflows/...` still make sense when read from each preserved package root.
