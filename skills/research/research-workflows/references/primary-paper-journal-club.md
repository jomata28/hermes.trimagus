# Primary-paper journal club extraction checklist

Use this note for papers whose conclusions depend on many figure panels, supplementary data, or revised analyses.

## Retrieval hierarchy

1. Final HTML article and DOI metadata.
2. Final PDF, including Methods and extended-data captions.
3. Supplementary figures and tables.
4. Per-figure source-data workbooks or archives.
5. Reporting summary for allocation, masking, exclusions, sample-size rationale, and replication.
6. Peer-review file for criticisms, author responses, and experiments added during revision.
7. Public repository accession for raw omics data.

Publisher HTML may expose downloads as in-page anchors rather than obvious direct links. Inspect all link text and href values for terms such as `Source data`, `Supplementary`, `Reporting Summary`, and `Peer Review File`, then download the underlying media URLs. Prefer direct requests for static PDF and XLSX resources once their URLs are known.

## Evidence ledger

Create one row per claim or panel with:

- section and figure panel
- cohort identity
- intervention and comparator
- timepoint
- biological unit and n
- outcome and units
- group summary values
- uncertainty type
- statistical test
- one-sided or two-sided status
- raw or adjusted P value
- multiplicity method
- direct result, association, or causal claim
- limitation or alternative explanation

Do not merge n values across physiology, histology, molecular, RNA-seq, and survival cohorts.

## Source-data extraction

- Use source workbooks to recover exact means, s.e.m., effect estimates, and P values that are hard to read from plots.
- Preserve the test named in the workbook. Counts, proportions, repeated measures, survival, and continuous outcomes may use different models.
- Recompute simple derived quantities only when useful, such as absolute and percentage change. Label them as calculations rather than author-reported endpoints.
- Do not calculate or imply a formal maximum-lifespan effect unless the paper prespecified and tested it.
- For omics tables, count significant rows only after confirming the exact adjusted-P threshold and direction convention.

## Longitudinal interpretation

Keep these questions separate:

1. Did the untreated group change with time?
2. Did the treated group change with time?
3. Were the trajectories statistically different?
4. Did treatment preserve baseline, improve above baseline, or merely finish higher at one timepoint?

The between-group slope contrast is the key test for differential ageing trajectory. A significant slope in one group and a nonsignificant slope in another does not itself prove that slopes differ.

## Comparator audit

For calorie-matched or pair-fed studies, record:

- fixed versus dynamically matched restriction
- group-level versus individual intake matching
- meal timing and fasting duration
- housing and food competition
- body-weight and composition matching
- whether the comparator appears in the survival cohort, functional cohort, molecular cohort, or only one of them

A comparator can support calorie-independent effects for selected outcomes without proving calorie-independent longevity.

## Mechanistic claim ladder

Use the narrowest justified wording:

1. Marker changed.
2. Pathway appears engaged.
3. Intervention and pathway are associated.
4. Perturbation shows pathway necessity.
5. Rescue or gain-of-function supports sufficiency.
6. Mediation links the pathway to the organismal endpoint.

Transcript abundance, enrichment predictions, colocalization, and biomarker panels usually support levels 1 to 3 only.

## Peer-review use

Peer review can reveal why analyses or cohorts were added and which concerns remain important. It is not a substitute for the final paper. Verify every accepted quantitative claim against the final manuscript or source data, and do not repeat outdated values or terminology from earlier versions.

## Journal-club output structure

For every requested section provide:

1. Central question
2. Methods
3. Exact key quantitative findings, including n and P values where important
4. Interpretation
5. Best figure panels
6. Limitations

Then add overall design, translational caveats, likely audience questions, and answers that distinguish what the study shows from what it does not show.

## Final audit

- Exact user-specified headings preserved
- No unsupported extrapolation
- Units and n values checked
- One-sided tests identified
- Adjusted and unadjusted P values not conflated
- Cross-sectional and longitudinal evidence distinguished
- Functional improvement not automatically called healthspan extension
- Biomarker change not automatically called rejuvenation
- Comparator scope stated precisely
- Conflicts of interest and patents noted when relevant
- Prohibited punctuation or formatting checked programmatically when possible
