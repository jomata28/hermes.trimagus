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
- The user asks for high-stakes consumer due diligence that needs public-record checks, market comparables, and a buy/avoid recommendation (for Mexico used/semi-new vehicles, use `references/vehicle-purchase-due-diligence-mexico.md`).

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

## Consumer Due Diligence

Use this subsection for practical purchase/risk research where the user needs a decision, not just a source dump. Separate visible/listing facts from assumptions, run official/public checks first, use market comparables, and end with a concrete recommendation plus missing data.

For Mexico used/semi-new car purchases, follow `references/vehicle-purchase-due-diligence-mexico.md`: extract plate/VIN/listing data from photos, check REPUVE/state tenencia-verification/recalls, benchmark price, account for Kavak-vs-private risk, and never green-light from photos alone.

## Safety / Medical-Adjacent Research

When the user asks about body-use safety of DIY experiments, supplements, devices, or electrically/chemically modified liquids:

1. Separate **anecdote**, **established mechanism**, and **clinical evidence** explicitly.
2. Do not dismiss subjective benefits, but do not let “felt good” substitute for safety evidence.
3. Triage by route and dose: ingestion, inhalation/spray, topical intact skin, wounds/eyes/mucosa, duration, amount, and current symptoms.
4. Prefer adjacent primary literatures when direct clinical evidence is absent: toxicology, electrochemistry, food-safety, water-treatment, materials/corrosion, and physiology.
5. Quantify plausible exposure when possible instead of relying on vague risk language.
6. If there are acute/severe symptoms or meaningful poisoning concern, recommend Poison Control / urgent care rather than continuing speculative analysis.

Reference note: `references/electrochemistry-body-use-risk.md` covers DIY charged/electrolyzed water or milk, electrode leaching, Faraday-law estimates, and literature-search anchors.

## Common Pitfalls

1. Mixing uncited synthesis with source facts.
2. Using stale market or feed data.
3. Overcollecting papers without clustering or ranking relevance.
4. Drafting paper claims before evidence/experiments are available.
5. Treating a lack of direct medical literature as proof of safety; absence of evidence is not evidence of absence.
6. Hardening a session-specific hazard into a blanket refusal. Capture the mechanism and safer experimental controls instead.

## Verification Checklist

- [ ] Source retrieval succeeded.
- [ ] Citations/URLs/IDs captured.
- [ ] Current data freshness stated.
- [ ] Synthesis is separated from raw evidence.
- [ ] Deliverable format matches the user's request.
