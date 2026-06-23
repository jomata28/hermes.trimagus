---
name: find-nearby
description: Find nearby places (restaurants, cafes, bars, pharmacies, etc.) using OpenStreetMap. Works with coordinates, addresses, cities, zip codes, or Telegram location pins. No API keys needed.
version: 1.0.0
metadata:
  hermes:
    tags: [location, maps, nearby, places, restaurants, local]
    related_skills: []
---

# Find Nearby — Local Place Discovery

Find restaurants, cafes, bars, pharmacies, and other places near any location. Uses OpenStreetMap (free, no API keys). Works with:

- **Coordinates** from Telegram location pins (latitude/longitude in conversation)
- **Addresses** ("near 123 Main St, Springfield")
- **Cities** ("restaurants in downtown Austin")
- **Zip codes** ("pharmacies near 90210")
- **Landmarks** ("cafes near Times Square")

## Quick Reference

```bash
# By coordinates (from Telegram location pin or user-provided)
python3 SKILL_DIR/scripts/find_nearby.py --lat <LAT> --lon <LON> --type restaurant --radius 1500

# By address, city, or landmark (auto-geocoded)
python3 SKILL_DIR/scripts/find_nearby.py --near "Times Square, New York" --type cafe

# Multiple place types
python3 SKILL_DIR/scripts/find_nearby.py --near "downtown austin" --type restaurant --type bar --limit 10

# JSON output
python3 SKILL_DIR/scripts/find_nearby.py --near "90210" --type pharmacy --json
```

### Parameters

| Flag | Description | Default |
|------|-------------|---------|
| `--lat`, `--lon` | Exact coordinates | — |
| `--near` | Address, city, zip, or landmark (geocoded) | — |
| `--type` | Place type (repeatable for multiple) | restaurant |
| `--radius` | Search radius in meters | 1500 |
| `--limit` | Max results | 15 |
| `--json` | Machine-readable JSON output | off |

### Common Place Types

`restaurant`, `cafe`, `bar`, `pub`, `fast_food`, `pharmacy`, `hospital`, `bank`, `atm`, `fuel`, `parking`, `supermarket`, `convenience`, `hotel`

## Workflow

1. **Get the location.** Look for coordinates (`latitude: ... / longitude: ...`) from a Telegram pin, or ask the user for an address/city/zip.

2. **Ask for preferences** (only if not already stated): place type, how far they're willing to go, any specifics (cuisine, "open now", etc.).

3. **Run the script** with appropriate flags. Use `--json` if you need to process results programmatically.

4. **Present results** with names, distances, and Google Maps links. If the user asked about hours or "open now," check the `hours` field in results — if missing or unclear, verify with `web_search`.

5. **For directions**, use the `directions_url` from results, or construct: `https://www.google.com/maps/dir/?api=1&origin=<LAT>,<LON>&destination=<LAT>,<LON>`

## Tips

- If results are sparse, widen the radius (1500 → 3000m)
- For event-day plans (festivals, sports fan zones, religious services, concerts), combine **official event pages** + nearby search: verify date-specific hours/location/security rules from the organizer or a reputable local guide, then use this skill for nearby food/bars/cafes/parking. Give the user a practical itinerary with arrival-time recommendation, not just a list of places.
- For travel-tour comparison requests (hotel concierge vs outside operators), research direct operator pages first, compute **total final cost** (tour + dock/entry/transport fees), and present a ranked shortlist by use case rather than a raw dump. For Los Cabos/Cabo San Lucas tours, see `references/los-cabos-tour-research.md` for landmarks, operator pages, price anchors, and negotiation questions.
- When a user wants to combine two destinations, geocode both, estimate rough distance/time, and include direct Google Maps directions links when helpful. If one item has fixed times (e.g. Mass, kickoff, gate open), anchor the plan around that schedule and call out conflicts clearly.
- For specialized categories (e.g. firearm ranges, niche classes, gyms, training providers), OSM amenity/type coverage may be poor. Fallback to Nominatim text searches for known phrases (`gun range Houston Texas`, `beginner handgun class Houston TX`) and then provide Google Maps search links for verification.
- For government-service searches (DMV/licensing offices, permit counters, visa offices, etc.), treat it as **place + procedure**: identify the official agency page/payment source, required documents, appointment flow, and then the nearest active office. Do not just return a nearby address.
- For CDMX driver's license questions near Coapa/Tlalpan, see `references/cdmx-driving-license.md` for the verified checklist, payment link, and Coyoacán module lead.
- Google Search and DuckDuckGo may bot-block VPS browser sessions. When blocked, use direct known business pages, Nominatim/OSM, or constructed Google Maps search URLs instead of pretending search succeeded. DuckDuckGo HTML search plus direct page fetches can work well for current event pages when browser search times out.
- For "open now" requests: check the `hours` field in results, cross-reference with web/direct business pages for accuracy since OSM hours aren't always complete
- For nearby Catholic Mass / misa requests, do **not** rely only on generic OSM `place_of_worship` results. Use OSM/geocoding for the origin, then query MassTimes for parish schedules. See `references/catholic-mass-times.md` for the direct API pattern and 403-header workaround.
- Zip codes alone can be ambiguous globally — prompt the user for country/state if results look wrong
- The script uses OpenStreetMap data which is community-maintained; coverage varies by region
