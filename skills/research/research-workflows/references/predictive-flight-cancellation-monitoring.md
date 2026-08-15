# Predictive flight-cancellation monitoring

Use this reference when the user wants an early risk watchlist, not merely confirmation that a flight is already cancelled.

## Separate three layers

1. **Published schedule:** route, flight number, planned times, sale inventory. A schedule feed can retain cancelled flights and is not operational ground truth.
2. **Current operational state:** scheduled, delayed, departed, arrived, diverted, cancelled, plus tail number, estimates, and irregularity messages.
3. **Prospective prediction:** a timestamped risk estimate made before the outcome. Never relabel a reactive cancellation alert as a prediction.

## Build data prospectively

- Use a stable flight-instance key: carrier, flight number, origin, destination, scheduled departure date/time.
- Append each observation to JSONL before the outcome is known.
- Keep raw features, score, reasons, source URL/ID, and observation timestamp.
- Continue tracking shortly after scheduled departure so operated flights receive outcomes. Otherwise the dataset contains cancellations but lacks negative labels.
- Keep `Unknown`, parser failures, HTTP blocks, and future dates outside the denominator. Never convert missing data into “operated.”

## Historical outcome recovery

Use layered sources and preserve evidence:

1. Date-specific operational tracker, with exact flight number and date parameters.
2. Browser-rendered history tables from a secondary source.
3. Cross-check overlapping results and quantify contradictions.
4. Accept secondary evidence only when date, number, route, and explicit outcome match.

Direct requests may be rate-limited while a persistent headed browser still renders valid history. Use the browser slowly and retain canonical source URLs. If two sources overlap, report agreement count before using the secondary source for unmatched cases.

## Avoid biased comparisons

A backfill dominated by one origin cannot establish that origin “cancels most.” Before comparative claims, report:

- resolved outcomes by origin, route, and flight number;
- cancellation numerator and scheduled/observed denominator;
- sampling design and missingness;
- confidence intervals, preferably Wilson intervals for small counts.

Stratify future collection across origins and times rather than sampling only the next globally sorted flights.

## Weather cross-section without leakage

Distinguish:

- **METAR/observed weather:** useful for explaining what occurred;
- **TAF/current forecast:** useful over its actual validity horizon, commonly shorter than 48 to 72 hours;
- **archived model run:** needed to reconstruct what was knowable at a specific lead time.

For exact 24, 48, or 72 hour forecast vintages, use an archived run or previous-run API and store model, run initialization, valid time, lead time, coordinates, and full URL/parameters. Do not use final observed weather or a stitched historical forecast as if it were the forecast available three days earlier.

Candidate weather features:
- precipitation and convective weather code;
- visibility;
- ceiling from METAR/TAF;
- sustained wind and gusts;
- airport-wide disruption reports.

A weather association does not establish cancellation causality. Check whether disruption timing overlaps the flight and whether reports indicate airport-wide impact.

## Transparent shadow score

Start with an auditable heuristic, not opaque ML, when positive labels are scarce. Candidate signals:

- recent irregularity message;
- severe delay or repeated estimate shifts;
- inbound/tail rotation disruption;
- severe forecast weather plus airport-wide disruption;
- disappearance from schedule close to departure;
- recent route/flight cancellation rate, conservatively smoothed.

Make missing tail/estimate time-aware. Their absence far from departure is often normal and should not trigger a high score. Old irregularity messages should decay to zero.

Store scores silently until calibrated. Evaluate precision, recall, false positives, false negatives, Brier/calibration by band, and median lead time.

## JT daily report format

Keep the user-facing brief concise:

- **APARTAR:** only when at least two independent strong signals exist and the flight still appears purchasable.
- **VIGILAR:** partial signal, uncalibrated route history, moderate delay, or adverse weather without operational confirmation.
- **NINGUNO:** clearly say when no flight meets the threshold.

For each reported flight include number, route, departure date/time, category, concrete reasons, status link, and booking/search link. Do not call an uncalibrated score a probability. State briefly that operation remains possible, ordinary fare rules still apply, and prediction does not create IROP or refund eligibility.

Do not automate bookings, payments, speculative multi-holds, or attempts to manufacture disruption eligibility. A recommendation must remain useful even if the flight operates.
