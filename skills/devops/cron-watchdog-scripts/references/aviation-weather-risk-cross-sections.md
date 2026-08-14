# Aviation Weather Cross-Sections for Operational-Risk Monitors

Use this reference when testing whether weather known before an event improves an airline cancellation-risk monitor.

## Separate explanation from prediction

Two datasets answer different questions:

1. **Observed weather (METAR):** explains conditions around the event. It is valid for association analysis, but using future observed weather as a 48–72 h feature is leakage.
2. **Forecast vintage (TAF or archived model forecast):** records what was actually knowable at prediction time. This is required for honest 48–72 h backtesting.

Capture forecasts prospectively with `collected_at`, issue time, valid interval, raw payload, source URL, airport, and forecast fields. Never replace the vintage forecast with a later corrected forecast.

## Recommended event table

One row per `(flight, origin, destination, scheduled_departure_utc)`:

- outcome: `operated | cancelled | unknown`
- prediction timestamp and lead time
- origin/destination METAR aggregates over prior 3/6/12 h
- origin/destination TAF features known at 24/48/72 h lead
- visibility, ceiling, precipitation, thunder, wind, gusts, flight category
- airport disruption intensity (other delays/cancellations in the same window)
- route/flight-number history, tail assignment, inbound rotation, schedule changes
- source and evidence identity for every outcome

Keep `unknown` outcomes out of the denominator rather than treating them as operated.

## Sources and retrieval

- AviationWeather API: `https://aviationweather.gov/api/data/metar?ids=MMMY&format=json&hours=3`
- AviationWeather TAF: `https://aviationweather.gov/api/data/taf?ids=MMMY&format=json&hours=3`
- Iowa Mesonet ASOS/METAR archive can supply historical observations for station/date ranges.
- Historical TAF retention varies by station/source. If the old forecast vintage is unavailable, label the predictive feature missing; observed weather cannot substitute for it.

Fetch once per airport per poll and cache; do not query per flight. A combined wrapper may collect weather and then run the operational validator while preserving silent-unless-news stdout.

## Statistical discipline

- Report counts and uncertainty intervals, not only raw rates.
- A dataset concentrated at one origin cannot establish that origin “cancels more.” Compare airports only after representative sampling or suitable weighting.
- Use route/flight-number rates with smoothing; tiny cells such as 2/10 have wide uncertainty and are watchlist signals, not probabilities.
- Compare cancelled flights to operated controls matched on airport, local time, route class, and date where possible.
- Test incremental value: weather-only, operations-only, and combined models.
- Predeclare score thresholds, sample-size requirements, and evaluation metrics before enabling alerts.

## Practical interpretation

Weather can flag some events strongly while operational cancellations occur in benign weather. Therefore weather should be one feature family, not a causal assumption. For 48–72 h alerts, use forecast-vintage severity. For 6–24 h alerts, add METAR trends, airport-wide disruption, tail/inbound rotation, and recent irregular operations.
