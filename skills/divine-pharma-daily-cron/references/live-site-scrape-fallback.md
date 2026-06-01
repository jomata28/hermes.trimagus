# Live Site Scrape Fallback — Divine Pharma Cron

Use this when the Notion pharmacology database is stale or the latest Notion entry is already represented in `Daily-Sessions/`.

## What went wrong once

A homepage scrape treated the navigation link `Podcast Topics` (`/podcast-categories/`) as an episode and created a bogus daily note. The homepage contains navigation anchors, post title anchors, date anchors, author links, comments links, and raw MP3 download links interleaved together.

## Safer selection rule

1. Scrape `https://divineinterventionpodcasts.com/`.
2. Collect anchors only if they look like real episode posts:
   - label matches `^DIP\s+Ep\s+\d+`
   - label matches `Divine Intervention Episode`
   - label matches `Episode\s+\d+`
   - label contains a specific USMLE episode title, e.g. `USMLE Step 2/3 Rapid Review`
3. Exclude:
   - `/podcast-categories/`, `/tutoring/`, `/notes/`, `/contact/`, `/exam-topic-lists/`
   - `/wp-content/` audio URLs as candidate pages (keep them only as `audio_url`)
   - author pages, `#respond`, comments, dates, generic labels (`Podcast Topics`, `Tutoring`, `Episode Notes`, `Audio Download`)
4. For each real candidate newest-to-oldest, search `Daily-Sessions/` for both exact link and normalized title.
5. Select the first unprocessed real episode. If all are processed, return exactly `[SILENT]`.

## Minimal Python anchor filter

```python
import re, html, urllib.parse

REAL_EPISODE = re.compile(
    r"^(DIP\s+Ep\s+\d+|Divine Intervention Episode|Episode\s+\d+)|USMLE Step",
    re.I,
)

def episode_candidates(homepage_html):
    out = []
    for m in re.finditer(r"<a[^>]+href=['\"]([^'\"]+)['\"][^>]*>(.*?)</a>", homepage_html, re.I|re.S):
        href = html.unescape(m.group(1))
        label = html.unescape(re.sub(r"\s+", " ", re.sub(r"<.*?>", " ", m.group(2)))).strip()
        if not href.startswith("http"):
            href = urllib.parse.urljoin("https://divineinterventionpodcasts.com/", href)
        if "divineinterventionpodcasts.com" not in href:
            continue
        if not REAL_EPISODE.search(label):
            continue
        if "/wp-content/" in href or "#respond" in href or "/author/" in href:
            continue
        if href not in [x["link"] for x in out]:
            out.append({"title": label, "link": href})
    return out
```

## Example from 2026-05-31

- Notion latest: `Ep. 8 - Heme Drugs`, already processed in multiple notes.
- Live-site latest: `DIP Ep 657: OMBRS 3-The OSHA Silica Standard`, already processed on `2026-05-30`.
- Correct next selection: `DIP Ep 656: The Clutch Health Insurance Podcast (Part 2)`.

No GPU was available, so the correct behavior was to create a structured fallback note rather than run CPU Whisper.
