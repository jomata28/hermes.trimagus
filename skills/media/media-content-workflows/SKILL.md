---
name: media-content-workflows
description: "Use when creating, searching, or transforming media content: GIF search, YouTube transcripts, audio feature visualizations, song generation prompts, and AI music workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [media, gif, youtube, audio, music, transcripts]
    related_skills: []
---

# Media Content Workflows

## Overview

This umbrella covers lightweight media retrieval, transformation, and generation workflows. The shared pattern is to produce or fetch a real artifact or transcript, verify it exists, and return a usable media path, URL, or structured summary.

## When to Use

- The user asks to find/download GIFs.
- The user asks to summarize, transform, or repurpose YouTube transcripts.
- The user asks for audio spectrograms or audio feature analysis.
- The user asks for lyrics, Suno-style prompts, or AI music generation workflows.

## GIF Search

Use Tenor/API-backed search and download tooling. Verify selected GIF URLs and downloaded files before returning them.

## YouTube Content

Fetch transcripts when possible, then produce summaries, threads, blog posts, or study notes. If transcripts are unavailable, report the blocker and try alternate transcript sources before giving up.

### YouTube fact-checking and claim verification

When the user asks "is this true?" about a YouTube Short/video, do not require a full transcript before giving a useful answer. First verify public metadata with YouTube oEmbed (title, author, thumbnail) and, if needed, inspect the public page's `ytInitialData` for title/description/view/like/context text. Try transcript tools when available, but if transcript retrieval is blocked or unavailable, state that limitation plainly and evaluate the visible/verified claim using authoritative external docs or sources for the underlying topic.

If the user supplies a purported transcript/summary after transcript retrieval failed, treat it as user-provided evidence rather than verified transcript: use it to identify claims, then verify the underlying claims independently. For financial/trading/AI-income videos, separate: (1) technically feasible architecture, (2) verified source facts, (3) unproven performance claims. Use quick math when relevant (e.g. ROI implied by profit vs starting capital; prediction-market win rate vs entry price) and make the verdict explicit: what is true, what is overstated, and what evidence would be needed to prove stronger claims (e.g. audited P&L, broker statements, sample size, live-vs-backtest distinction, fees/slippage).

### YouTube-to-business planning

When the user asks to turn a YouTube video into a business, do not wait for a perfect transcript if YouTube blocks transcript/download tooling. Verify what you can (for example, YouTube oEmbed metadata/title/author, thumbnail, public page data), state the transcript limitation plainly, then synthesize an actionable business plan from: verified metadata, any accessible video context, market/category scan, and the user's existing assets. Prefer a concrete offer, ICP, pricing, MVP stack, sales motion, risks, and 30-day execution plan over a generic summary. If the plan is durable for the user's operating system, save it as a project note in the vault/project workspace and return the path.

Reference: `references/youtube-to-business-plan.md` contains a reusable structure and fallback pattern.
Reference: `references/youtube-shorts-fact-checking.md` contains a concise fallback workflow for claim verification when transcripts are unavailable.

## Audio Features and Spectrograms

Use audio feature tooling for mel, chroma, MFCC, spectrograms, or visual assets. Verify the output image/audio file exists and has nonzero size.

## Songwriting and AI Music

Separate songwriting craft from model prompt formatting. For Suno-like tools, produce lyrics plus tags/style metadata and preserve section labels such as verse, chorus, bridge, and outro.

## HeartMuLa / Music Generation

Use HeartMuLa when the user wants Suno-like generation from lyrics and tags. Track job IDs/URLs and verify generated audio before claiming completion.

## Common Pitfalls

1. Returning a search result without downloading or verifying when the user requested a file.
2. Hallucinating YouTube transcript content when retrieval failed.
3. Mixing lyrics with generation tags in a way the target tool cannot parse.
4. Forgetting to include media paths or URLs in the final response.

## Verification Checklist

- [ ] Source URL/query or generation prompt captured.
- [ ] Artifact/transcript fetched or generated.
- [ ] File/URL/job status verified.
- [ ] Final response includes media handle or concise transformed content.
