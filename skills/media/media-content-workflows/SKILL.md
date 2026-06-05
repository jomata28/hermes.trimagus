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
