---
name: creative-web-artifacts
description: "Use when creating visual or interactive browser artifacts: landing-page mockups, diagrams, Excalidraw, p5.js sketches, design tokens, pretext layouts, and visual design-system variants."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative, html, css, svg, p5js, diagrams, design, prototype]
    related_skills: []
---

# Creative Web Artifacts

## Overview

This umbrella covers visual and interactive artifacts that are usually delivered as HTML/CSS/SVG/JS or browser-viewable files. Choose the subsection based on the desired output, but keep the shared workflow: clarify the artifact type, build a real file, open/render it when possible, and verify visually.

## When to Use

- The user wants a landing page, deck-like page, prototype, or mockup.
- The user wants an architecture/cloud/infra diagram.
- The user wants Excalidraw or hand-drawn-style diagrams.
- The user wants generative or interactive p5.js sketches.
- The user wants DESIGN.md design tokens/specs.
- The user wants browser demos using text layout or real design-system references.

## Shared Workflow

1. Identify output format: HTML, SVG, Excalidraw JSON, p5.js, DESIGN.md, or template-derived page.
2. Create an actual artifact file, not just a description.
3. Prefer self-contained assets unless the user requests external dependencies.
4. Render or validate the artifact with browser/screenshot/export tooling when available.
5. Return the file path and any screenshot/media handle.

## HTML Mockups and Design Variants

For one-off designs, produce 2-3 strong variants when comparison is useful. Use concrete layout, typography, color, and interaction details rather than generic boxes.

## Architecture Diagrams

For infrastructure or system diagrams, dark-themed SVG-in-HTML artifacts are a durable default. Label services, data flow, boundaries, and failure domains.

## Excalidraw

For hand-drawn diagrams, generate valid Excalidraw JSON and verify structure. Use it for architecture, flow, sequence, and rough workshop-style visuals.

## p5.js and Interactive Sketches

Use p5.js for generative art, shaders, interactions, or 3D browser sketches. Include controls/instructions if interaction matters.

## DESIGN.md and Design Systems

Use DESIGN.md for token/spec authoring and validation. Use real design-system templates when the user asks for a style like Stripe, Linear, or Vercel.

## Pretext Layouts

Use pretext when text layout itself is the medium: ASCII art, typographic flow around obstacles, text-as-geometry games, or DOM-free text demos.

## Common Pitfalls

1. Stopping at a prompt or concept instead of writing a file.
2. Returning an artifact without rendering or syntax validation.
3. Mixing incompatible formats (e.g., Excalidraw JSON inside plain SVG expectations).
4. Using external assets that break offline delivery.

## Verification Checklist

- [ ] Output format selected.
- [ ] Artifact file written.
- [ ] Syntax/structure validated.
- [ ] Render/screenshot/export attempted when possible.
- [ ] Final response includes path or media handle.
