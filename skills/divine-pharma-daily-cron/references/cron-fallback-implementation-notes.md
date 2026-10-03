# Cron fallback implementation notes

Session learning from the 2026-06-03 run while processing DIP Ep 653.

## HTML parsing without BeautifulSoup

The cron environment may not have `bs4` installed. Do not depend on BeautifulSoup for live-site fallback scraping. Use Python stdlib `html.parser` instead, then filter anchors by title/URL.

Minimal pattern:

```python
from html.parser import HTMLParser
import html as htmlmod, re

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'a' and 'href' in d:
            self.stack.append([d['href'], ''])
    def handle_data(self, data):
        if self.stack:
            self.stack[-1][1] += data
    def handle_endtag(self, tag):
        if tag == 'a' and self.stack:
            self.links.append(tuple(self.stack.pop()))

p = LinkParser(); p.feed(homepage_html)
candidates = []
for href, text in p.links:
    text = ' '.join(htmlmod.unescape(text).split())
    if href.startswith('/'):
        href = 'https://divineinterventionpodcasts.com' + href
    href = href.split('#')[0]
    if 'divineinterventionpodcasts.com' not in href:
        continue
    if any(x in href for x in ['/podcast-categories/', '/wp-content/', '/author/']) or href.rstrip('/') == 'https://divineinterventionpodcasts.com':
        continue
    if re.search(r'\b(DIP\s*Ep\s*\d+|Divine Intervention Episode|Episode\s*\d+)\b', text, re.I):
        candidates.append((href, text))
```

## Long episode/no-GPU fallback checklist

When `nvidia-smi` shows no CUDA GPU:

1. Still download the MP3 with `curl -L --retry 3 --fail` and verify duration with `ffprobe`.
2. For episodes up to about 35 minutes, attempt CPU transcription with `faster_whisper` base/int8 and a 600-second timeout before creating a placeholder. This path completed a 23:26 episode in 358 seconds in the cron environment.
3. If the package is absent, run the transcription script with `uv run --with faster-whisper python SCRIPT.py`; preserve raw `.txt` and timestamped `.tsv` outputs.
4. After success, write a complete transcript note, replace any placeholder Daily-Session in place, and set `processing_status: completed` plus `transcription_status: completed_faster_whisper_base_cpu`.
5. Only if transcription genuinely fails or the episode is too long for the execution window, create a transcript placeholder with `processing_status: structured_fallback_no_transcript` and `transcription_status: skipped_no_gpu_episode_...`.
6. Append both `live:<sha256(page_url)[:16]>` and the page URL to `~/.divine_pharma_processed`, but do not treat those markers as proof that a placeholder is complete.

## Verification

Before final response, read back the new Daily-Sessions note, read the transcript placeholder, and confirm the processed marker and page URL were written.