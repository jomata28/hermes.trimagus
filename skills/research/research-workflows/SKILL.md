---
name: research-workflows
description: "Use when doing research workflows: paper discovery, blog/feed monitoring, market/event data lookup, knowledge-base construction, and academic paper drafting."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, arxiv, papers, blogs, prediction-markets, knowledge-base]
    related_skills: []
---

# Research Workflows

## Overview

This umbrella covers research as a class: discover sources, collect evidence, synthesize, and produce a durable artifact. Choose the subsection based on source type and final deliverable.

## When to Use

- The user asks to find papers or monitor new literature.
- The user asks to monitor blogs or RSS/Atom feeds.
- The user asks to query Polymarket or market/event probabilities.
- The user asks to build/query a linked LLM knowledge wiki.
- The user asks to draft or structure an ML research paper.

## Source Discipline

1. Prefer primary sources and tool output over memory.
2. Capture citations, URLs, dates, and IDs.
3. Separate quoted evidence from synthesis.
4. For current facts, fetch live data.

## arXiv and Literature Search

Use arXiv search by keyword, author, category, or ID. Record paper IDs, titles, authors, dates, and links. For literature reviews, cluster papers by theme rather than dumping a flat list.

## Blog and Feed Monitoring

Use blog/RSS monitoring when the task is recurring or change-oriented. Report new items, source feed, timestamp, and why each item matters.

## Polymarket and Market Data

Query live markets, prices, orderbooks, and history. Make freshness explicit and avoid treating market-implied probabilities as facts.

## LLM Wiki / Knowledge Base

Use linked markdown knowledge-base tooling for interlinked concept maps and retrieval over research notes. Keep source references attached to claims.

## Research Paper Writing

For ML papers, support the workflow from design to submission: positioning, related work, method, experiments, limitations, and template compliance. Use templates when the target venue requires them.

## Common Pitfalls

1. Mixing uncited synthesis with source facts.
2. Using stale market or feed data.
3. Overcollecting papers without clustering or ranking relevance.
4. Drafting paper claims before evidence/experiments are available.

## Verification Checklist

- [ ] Source retrieval succeeded.
- [ ] Citations/URLs/IDs captured.
- [ ] Current data freshness stated.
- [ ] Synthesis is separated from raw evidence.
- [ ] Deliverable format matches the user's request.
