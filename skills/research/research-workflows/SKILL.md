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
5. For comparative superlatives ("most," "worst," "highest"), identify the exact comparison set, geography, observation period, denominator, and metric before repeating the claim.

## Investigating Comparative Performance Claims

Use this workflow for claims such as “company X cancels the most,” “service Y is least reliable,” or similar rankings:

1. **Trace the wording to its origin.** Search exact and near-exact phrases in the relevant languages. Distinguish the first discoverable article from the underlying data source it cites.
2. **Define scope explicitly.** Record geography, entities included, start/end dates, event window versus ordinary operations, and whether the source is a snapshot, rolling period, month, or year.
3. **Audit the metric.** Separate raw event counts from rates. For rates, identify the denominator (scheduled, operated, arriving, or observed records); do not silently infer that “most” means highest rate.
4. **Inspect the underlying table.** Count rows and categories directly when possible. Flag discrepancies between headline totals, prose, and the published table.
5. **Assess credibility in layers.** Prefer regulator or first-party operational data, then established specialist data providers, then transparent secondary analysis. Treat SEO/news aggregation without named methodology as evidence of the claim’s origin, not proof of the generalization.
6. **Triangulate typical magnitude.** Use at least one longer-period rate or count and one operational-volume source. Label estimates when sources use different periods or denominators.
7. **Normalize to the requested window.** Compute expected events as `exposure × rate`; if only a period count exists, use `count ÷ period_days × observation_days`. State assumptions and do not compare whole-network counts with a route or airport subset without adjustment.
8. **Reconcile monitoring results carefully.** Distinguish unique completed events from repeated forward-looking snapshots. A schedule feed may omit pre-baseline removals or lack final operational status, so zero detected candidates is not automatically evidence of zero real events.
9. **State the narrowest defensible conclusion.** Replace unsupported global claims with wording preserving verified scope, such as “largest raw count in this six-airport event table.”

See `references/comparative-operational-claims.md` for a compact audit checklist and calculation patterns.

## arXiv and Literature Search

Use arXiv search by keyword, author, category, or ID. Record paper IDs, titles, authors, dates, and links. For literature reviews, cluster papers by theme rather than dumping a flat list.

## Primary-Paper Journal Club Analysis

Use this workflow when the user requests a figure-level, section-by-section analysis of a scientific paper:

1. Retrieve the final paper, Methods, supplementary files, reporting summary, source-data files, and peer-review history when available. Treat the paper and source data as primary evidence. Use peer review only to identify design criticisms, revisions, and unresolved caveats.
2. Build an experiment map before writing: cohort, species or population, intervention, comparator, timing, sample size, endpoint family, masking, randomization, and statistical model. Keep independent cohorts distinct.
3. Verify exact quantitative claims against source-data tables rather than estimating values from plotted bars. Record units, mean and uncertainty convention, n, test direction, adjustment method, and exact P value. If a paper reports only a pathway-level result, do not invent an effect size.
4. For longitudinal figures, distinguish within-group slope tests from adjusted between-group slope comparisons. Do not use a significant within-group change as proof that groups differ.
5. Separate three levels of inference: direct outcome, mechanistic association, and causal mediation. Biomarker movement or transcription-factor enrichment does not establish pathway necessity.
6. Audit causal comparators carefully. A calorie-matched, pair-fed, weight-matched, vehicle, or sham arm may clarify some confounding while leaving survival, exposure, timing, or tissue-specific causality unresolved.
7. Recommend figure panels by argumentative role: primary endpoint, representative functional evidence, mechanism, decisive comparator, and limitations. Prefer a small coherent panel set over a dense figure dump.
8. Surface statistical caveats explicitly, especially one-sided tests, permissive false-discovery thresholds, many endpoint families, small mechanistic n, non-independent measurements, and absence of global multiplicity control.
9. Match the user's requested headings exactly and run a final formatting audit for prohibited punctuation, terminology, and schema constraints.

For a detailed retrieval and evidence-extraction checklist, see `references/primary-paper-journal-club.md`.

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

## Live Marketplace and Rental-Listing Research

Use this workflow for housing, vehicles, jobs, tickets, and other time-sensitive marketplace searches:

1. **Define hard filters first:** item/property type, exact quantity requirements (for example, exactly three bedrooms rather than “3+”), target geography, budget if given, and freshness threshold.
2. **Search multiple independent sources.** Prefer live detail pages over category pages and search-result snippets. Record which requested sources were inspected, including sources that yielded no independently verifiable candidates.
3. **Verify every row against its detail page.** Never promote a search snippet into the final table unless a current primary listing surface confirms the title, price, required attributes, and canonical URL. Reconcile card/detail-page conflicts before asserting an exact count: compare title, prose, labels, structured fields, and category filters; omit or flag the candidate when the source remains internally inconsistent.
4. **Use layered retrieval rather than stopping at bot protection:** try the normal page, an indexed result exposing the canonical URL, a text-rendering/cache service, structured metadata, and the advertiser or agency's canonical page. These are retrieval routes, not proof of availability.
5. **Deduplicate by underlying asset, not URL.** Compare address/development, price, area, bedroom/bath counts, distinctive description text, photos, and agency identity. When uncertain, retain one row and flag possible cross-posting rather than inflating the count.
6. **Distinguish freshness levels:**
   - `posted/updated DATE` only when the source states it;
   - `live detail page retrieved DATE` when the page loads but supplies no publication date;
   - `indexed DATE` only for an index/cache observation, clearly labeled as weaker evidence;
   - `availability confirmed DATE` only after direct advertiser confirmation.
7. **Do not call a listing “available” merely because its page resolves.** Say “live listing page” or “publicly retrievable,” and advise confirmation before paying or traveling.
8. **Mark absent fields as “not stated.”** Do not infer furnished/unfurnished, maintenance, utilities, exact address, or security from photos, price, neighborhood reputation, or portal filters.
9. **Estimate proximity transparently.** Label road distance and travel time as approximate, state the destination used, distinguish normal from peak traffic when relevant, and avoid false precision when only the neighborhood is known.
10. **Keep suitability judgments evidence-based.** For safety or student suitability, prioritize controlled access, staffed security, lighting, safe pedestrian access, nearby transport/services, and late-night arrival logistics. Neighborhood reputation is context, never a guarantee.
11. **Return the requested schema and rank actionable candidates.** Include source, title, location, price, exact required attribute count, condition/furnishing, recurring fees, distance/commute, canonical URL, and freshness. Add a short best-first shortlist and verification checklist.

When fewer than the requested number survive verification, return the smaller honest set and explain the coverage gap; never pad the table with stale, duplicate, mismatched, or unverifiable entries.

Detailed rental-specific evidence standards, deduplication fields, alternate-renderer workflow, commute precision, and safety framing are in `references/live-rental-listing-research.md`.

## Safety / Medical-Adjacent Research

When the user asks about body-use safety of DIY experiments, supplements, devices, or electrically/chemically modified liquids:

1. Separate **anecdote**, **established mechanism**, and **clinical evidence** explicitly.
2. Do not dismiss subjective benefits, but do not let “felt good” substitute for safety evidence.
3. Triage by route and dose: ingestion, inhalation/spray, topical intact skin, wounds/eyes/mucosa, duration, amount, and current symptoms.
4. Prefer adjacent primary literatures when direct clinical evidence is absent: toxicology, electrochemistry, food-safety, water-treatment, materials/corrosion, and physiology.
5. Quantify plausible exposure when possible instead of relying on vague risk language.
6. If there are acute/severe symptoms or meaningful poisoning concern, recommend Poison Control / urgent care rather than continuing speculative analysis.

Reference note: `references/electrochemistry-body-use-risk.md` covers DIY charged/electrolyzed water or milk, electrode leaching, Faraday-law estimates, and literature-search anchors.

## Operational Status and Live-Endpoint Research

When evaluating airline, airport, logistics, or similar operational feeds, require a successful real request containing the target entity and status; a schema, UI label, documentation claim, or JavaScript string is not validation. Capture the exact endpoint and request shape, redact credentials, preserve freshness fields, and seek a second source for disputed or high-impact states. See `references/operational-flight-status-source-validation.md` for the undocumented-web-API discovery workflow, cancellation evidence standard, Viva Aerobus case study, and automation-policy checklist.

When the user wants **early cancellation risk rather than reactive status**, follow `references/predictive-flight-cancellation-monitoring.md`. It covers prospective flight-instance observations, historical outcome recovery, missing-data denominators, sampling bias, weather forecast vintage without leakage, shadow-score calibration, and JT's APARTAR/VIGILAR/NINGUNO daily brief format.

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
