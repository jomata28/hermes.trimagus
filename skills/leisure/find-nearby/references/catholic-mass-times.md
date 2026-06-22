# Catholic Mass times near a location

Use this when the user asks for nearby misa / Mass times, especially while traveling.

## Fast workflow

1. Geocode the user's hotel/landmark with the `find_nearby.py --near ... --json` script to get precise origin coordinates.
2. Query MassTimes directly for Catholic parishes and schedules near that coordinate:

```python
import requests
lat, lon = 22.8973469, -109.890727
s = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": f"https://masstimes.org/map?lat={lat:.3f}&lng={lon:.3f}",
    "X-Requested-With": "XMLHttpRequest",
}
r = s.get(f"https://masstimes.org/Churchs/?lat={lat}&long={lon}&pg=1", headers=headers, timeout=20)
r.raise_for_status()
parishes = r.json()
```

3. Filter `church_worship_times` for the requested day (`day_of_week.strip()`) and service type (`Weekend`, weekday, confession, etc.).
4. Run `date` for the destination timezone before recommending a soonest option.
5. Present a tiny actionable answer: best option first, backup second, direct Google Maps links, and "go now"/"you have time" guidance.

## Pitfalls

- A bare API request to `https://masstimes.org/Churchs/?lat=...&long=...&pg=1` may return `403 Forbidden`. First load or spoof the map referer and include browser-like headers plus `X-Requested-With: XMLHttpRequest`.
- Generic OSM `place_of_worship` results include non-Catholic churches and may omit actual Mass schedules. Use OSM for coordinates/distance, but MassTimes for Catholic schedule data.
- Search engines often bot-block VPS sessions. Prefer direct MassTimes API + OSM/Nominatim rather than wasting time on search pages.
- MassTimes distances are usually miles. The user's hotel-to-church route may differ from straight-line distance; include Maps links for verification.
