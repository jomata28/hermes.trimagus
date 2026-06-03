# Processed Episode Matching — Divine Pharma Cron

Use this when selecting the next live-site candidate after the Notion database is stale.

## Problem observed

A daily note can mention an episode that has **not** yet been processed, for example:

- `Evening Review Preview`: "Tomorrow’s first unprocessed live-site candidate appears to be DIP Ep 654..."
- `Processing Log`: lists candidates checked, skipped, or expected next.

A naive full-text search for title or URL can falsely mark that episode as already processed. This happened with `DIP Ep 654`: it appeared only as a tomorrow-preview inside the `DIP Ep 655` note, so broad content matching initially selected the older `DIP Ep 653` instead.

## Strong evidence that an episode is processed

Count a note as processing a candidate only if the candidate title or URL appears in one of these locations:

- YAML frontmatter keys such as `podcast_title`, `podcast`, `episode_url`, or `link`
- The main H1 title (`# DIP Ep ...`)
- Top metadata lines such as `Source: [Episode page](exact URL)` or `**Episode link:** exact URL`
- The note filename/stem clearly names the candidate episode

## Weak evidence to ignore

Do **not** count these alone:

- `Evening Review Preview`
- `Processing Log`
- "Tomorrow's candidate" / "next candidate" wording
- A list of checked live-site candidates
- Body text that mentions a neighboring episode without matching the frontmatter/H1/source metadata

## Minimal matching pattern

```python
import re, yaml
from pathlib import Path

STRONG_KEYS = {"podcast_title", "podcast", "episode_url", "link"}
WEAK_SECTION_RE = re.compile(r"\n## (Evening Review Preview|Processing Log)\n.*", re.I | re.S)

def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()

def processed_by_note(note_path: Path, title: str, url: str) -> bool:
    text = note_path.read_text(errors="ignore")
    title_n = norm(title)
    url = url.rstrip("/")

    # filename is strong evidence
    if title_n and title_n in norm(note_path.stem):
        return True

    # frontmatter is strong evidence
    if text.startswith("---"):
        try:
            _, fm, rest = text.split("---", 2)
            data = yaml.safe_load(fm) or {}
            values = "\n".join(str(data.get(k, "")) for k in STRONG_KEYS)
            if url in values or title_n in norm(values):
                return True
        except Exception:
            rest = text
    else:
        rest = text

    # Strip weak sections before body matching
    strong_body = WEAK_SECTION_RE.sub("", rest)

    # H1/top metadata exactness is strong enough
    top = "\n".join(strong_body.splitlines()[:30])
    return (url and url in top) or (title_n and title_n in norm(top))
```
