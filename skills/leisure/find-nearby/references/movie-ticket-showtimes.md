# Movie-ticket / showtime lookup pattern

Use this when JT asks for movie tickets near a landmark, city zone, or travel plan.

## Date grounding

- Always resolve today's date/time in the relevant timezone first.
- If the user says "Thursday" / "Friday", map that to concrete dates and state the assumption.
- Check the official movie site/release date before assuming a Thursday showing exists; early previews may be available even if release is Friday.

## US / Fandango pattern

Fandango movie pages lazy-load showtimes via a JSON endpoint that can be queried directly when browser automation is slow:

```text
https://www.fandango.com/napi/theaterShowtimeGroupings/<movie_id>/<YYYY-MM-DD>?zip=<ZIP>&isdesktop=true&isDesktopMOP=true
```

Useful extraction fields:

- `hasShowtimes`
- `theaterShowtimes.formats.availableFormats`
- `theaterShowtimes.theaters[].name`
- `distance`
- `address`
- `variants[].amenityGroups[].showtimes[]`
- showtime fields: `date`, `dateLocal`, `filmFormat[].filterName`, `ticketingJumpPageURL`, `type`, `expired`

Use ZIP codes near the user's landmark when available (e.g. 77030 for Hermann Park/TMC). Filter by `IMAX`, `70MM`, `Dolby`, etc. Present direct ticket links only when the source returned a `ticketingJumpPageURL`.

## Mexico / CDMX pattern

Cinépolis/IMAX often bot-block VPS requests. Do not fabricate live inventory. When blocked:

1. Identify confirmed theatres from official/credible sources.
2. Geocode named theatres and rank by distance from the user's landmark/zone.
3. Provide direct Cinépolis/movie/theatre links and say that the final seat/time check should be done in the Cinépolis app/site.
4. For Coapa, confirmed/nearby IMAX candidates for *La Odisea / The Odyssey* were:
   - Cinépolis Perisur & IMAX (~7 km from Coapa)
   - Cinépolis Universidad & IMAX (~8 km from Coapa)
   - Cinemex Parque Delta (~11 km)
   - Cinépolis Fórum Buenavista (~16 km)
   - Cinemex Santa Fe (~17 km)

## Output standard

Keep it practical:

- Best pick first
- Date + theatre + address/area + distance
- Showtimes table with buy links when verified
- Clearly label any venue-only recommendation where live inventory was blocked
- Do not claim seats are available unless the ticketing source returned active showtime links/status