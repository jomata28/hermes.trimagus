#!/usr/bin/env python3
"""Robust Divine Pharmacology daily processor.

Stdlib-first cron helper for the Divine Intervention pharmacology pipeline:
- Query Notion database using the known-good legacy endpoint/version.
- If Notion entries are stale/processed, scrape the live podcast homepage.
- Use strong processed matching only (frontmatter/H1/source/filename), not preview/log mentions.
- Download MP3, measure duration, and skip CPU Whisper for long no-GPU episodes.
- Create Daily-Sessions note + Transcripts handoff note + processed markers.
- Print JSON status. Caller should map {"status":"silent"} to exactly [SILENT].

Environment:
  NOTION_API_KEY optional but recommended
  DIVINE_PHARMA_VAULT or OBSIDIAN_VAULT_PATH optional; defaults to /root/Divine-Pharmacology
"""
from __future__ import annotations

import hashlib
import html as htmlmod
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

HOME = Path.home()
ENV = HOME / ".hermes/.env"
if ENV.exists():
    for line in ENV.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

DB_ID = "2f88c883-85ba-81d3-a9d2-eca5f4e30d0b"
NOTION = os.environ.get("NOTION_API_KEY", "")
VAULT = Path(os.environ.get("DIVINE_PHARMA_VAULT") or os.environ.get("OBSIDIAN_VAULT_PATH") or "/root/Divine-Pharmacology")
if not (VAULT / "Daily-Sessions").exists() and Path("/root/Divine-Pharmacology").exists():
    VAULT = Path("/root/Divine-Pharmacology")
DAILY = VAULT / "Daily-Sessions"
TRANS = VAULT / "Transcripts"
AUDIO_DIR = VAULT / "Audio"
for directory in (DAILY, TRANS, AUDIO_DIR):
    directory.mkdir(parents=True, exist_ok=True)

PROCESSED = HOME / ".divine_pharma_processed"
processed_text = PROCESSED.read_text(errors="ignore") if PROCESSED.exists() else ""
REAL_EPISODE_RE = re.compile(r"^(DIP\s+Ep\s+\d+|Divine Intervention Episode\s+\d+|Episode\s+\d+)", re.I)
ANNOUNCEMENT_RE = re.compile(r"(class|course|zoom|review\s*\(|\bmcq\b|\d+\s*hour)", re.I)
WEAK_SECTION_RE = re.compile(r"\n## (Evening Review Preview|Processing Log)\n.*", re.I | re.S)
STRONG_KEYS = {"podcast_title", "podcast", "episode_url", "link", "source"}
EXCLUDE_HREFS = ["/podcast-categories/", "/tutoring/", "/notes/", "/contact/", "/exam-topic-lists/", "/wp-content/", "/author/"]
EXCLUDE_TITLE_RE = re.compile(r"(zoom\s+classes?|classes|course|review\s*\(|\b\d+\s*hour\b|\b\d+\s*mcq\b|starts?\s+\d|nutrition\s+updates)", re.I)


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def slugify(s: str, maxlen: int = 110) -> str:
    s = htmlmod.unescape(s)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")
    return s[:maxlen].strip("-") or "episode"


def fetch_url(url: str, timeout: int = 45) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 HermesCron/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, **kwargs)


EP_NUM_RE = re.compile(r"(?:dip\s*ep|episode|ep)\s*\.?\s*(\d+)", re.I)


def processed_by_note(title: str, url: str) -> tuple[bool, str]:
    title_n = norm(title)
    url = (url or "").rstrip("/")
    ep_match = EP_NUM_RE.search(title or "")
    ep_num = ep_match.group(1) if ep_match else ""
    for note_path in DAILY.glob("*.md"):
        text = note_path.read_text(errors="ignore")
        if title_n and title_n in norm(note_path.stem):
            return True, str(note_path)
        # Episode-number match catches title word-variant traps (e.g. "Localize
        # The Oxygen" vs "Localize That Oxygen") when both refer to the same DIP Ep N.
        if ep_num:
            stem_n = norm(note_path.stem)
            if re.search(rf"\bep[\s.\-]*{re.escape(ep_num)}\b", stem_n):
                return True, str(note_path)
        rest = text
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                fm, rest = parts[1], parts[2]
                values = []
                for line in fm.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        if k.strip() in STRONG_KEYS:
                            values.append(v.strip().strip('"'))
                joined = "\n".join(values)
                if (url and url in joined) or (title_n and title_n in norm(joined)):
                    return True, str(note_path)
        strong_body = WEAK_SECTION_RE.sub("", rest)
        top = "\n".join(strong_body.splitlines()[:35])
        if (url and url in top) or (title_n and title_n in norm(top)):
            return True, str(note_path)
    return False, ""


def notion_candidates() -> list[dict]:
    if not NOTION:
        return []
    body = json.dumps({"page_size": 50, "sorts": [{"timestamp": "created_time", "direction": "descending"}]}).encode()
    req = urllib.request.Request(
        f"https://api.notion.com/v1/databases/{DB_ID}/query",
        data=body,
        method="POST",
        headers={"Authorization": f"Bearer {NOTION}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"},
    )
    try:
        obj = json.loads(urllib.request.urlopen(req, timeout=30).read())
    except Exception as exc:
        print(f"WARN notion query failed: {exc}", file=sys.stderr)
        return []
    out = []
    for res in obj.get("results", []):
        props = res.get("properties", {})
        try:
            title = props["Title"]["title"][0]["text"]["content"].strip()
            link = props["Link"]["url"].strip()
        except Exception:
            continue
        topics = [x.get("name", "") for x in (props.get("Related Topic", {}) or {}).get("multi_select", [])]
        out.append({"id": res.get("id", ""), "title": title, "link": link, "topics": topics, "source": "notion"})
    return out


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[list[str]] = []
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and "href" in d:
            self.stack.append([d["href"], ""])

    def handle_data(self, data):
        if self.stack:
            self.stack[-1][1] += data

    def handle_endtag(self, tag):
        if tag == "a" and self.stack:
            href, text = self.stack.pop()
            self.links.append((href, text))


def live_candidates() -> list[dict]:
    try:
        homepage = fetch_url("https://divineinterventionpodcasts.com/").decode("utf-8", "ignore")
    except Exception as exc:
        print(f"WARN homepage fetch failed: {exc}", file=sys.stderr)
        return []
    parser = LinkParser(); parser.feed(homepage)
    out, seen = [], set()
    for href, text in parser.links:
        text = " ".join(htmlmod.unescape(text).split())
        href = urllib.parse.urljoin("https://divineinterventionpodcasts.com/", htmlmod.unescape(href).split("#")[0])
        if "divineinterventionpodcasts.com" not in href or any(x in href for x in EXCLUDE_HREFS):
            continue
        if href.rstrip("/") == "https://divineinterventionpodcasts.com" or not REAL_EPISODE_RE.search(text):
            continue
        if ANNOUNCEMENT_RE.search(text):
            continue
        key = href.rstrip("/")
        if key in seen:
            continue
        seen.add(key)
        out.append({"id": "live:" + hashlib.sha256(key.encode()).hexdigest()[:16], "title": text, "link": key, "topics": ["Pharmacology"], "source": "live-site"})
    return out


def choose_candidate() -> tuple[dict | None, list]:
    checked = []
    for candidate in notion_candidates() + live_candidates():
        marker_hit = bool(candidate["id"] and candidate["id"] in processed_text) or candidate["link"] in processed_text
        note_hit, note_path = processed_by_note(candidate["title"], candidate["link"])
        checked.append((candidate["source"], candidate["title"], marker_hit, note_hit, note_path))
        if not marker_hit and not note_hit:
            return candidate, checked
    return None, checked


def extract_audio_url(page_url: str) -> str:
    page = fetch_url(page_url).decode("utf-8", "ignore")
    for pattern in [r"https://divineinterventionpodcasts\.com/wp-content/uploads/[^\"'<>\s]+\.mp3(?:\?[^\"'<>\s]*)?", r"https?://[^\"'<>\s]+\.mp3(?:\?[^\"'<>\s]*)?"]:
        match = re.search(pattern, page, re.I)
        if match:
            return htmlmod.unescape(match.group(0)).split("?")[0]
    return ""


def extract_youtube_url(page_url: str) -> str:
    """Return a normalized YouTube watch URL for video-only episode pages."""
    page = htmlmod.unescape(fetch_url(page_url).decode("utf-8", "ignore"))
    patterns = [
        r"youtube(?:-nocookie)?\.com/embed/([A-Za-z0-9_-]{6,})",
        r"youtube\.com/watch\?[^\"'<>\s]*v=([A-Za-z0-9_-]{6,})",
        r"youtu\.be/([A-Za-z0-9_-]{6,})",
    ]
    for pattern in patterns:
        match = re.search(pattern, page, re.I)
        if match:
            return "https://www.youtube.com/watch?v=" + match.group(1)
    return ""


def download(url: str, path: Path) -> None:
    result = run(["curl", "-L", "--retry", "3", "--fail", "--connect-timeout", "20", "--max-time", "600", "-o", str(path), url], timeout=650)
    if result.returncode != 0 or not path.exists() or path.stat().st_size < 10000:
        raise RuntimeError("audio download failed: " + result.stderr[-500:])


def duration_seconds(path: Path) -> float:
    result = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)], timeout=30)
    try:
        return float(result.stdout.strip()) if result.returncode == 0 else 0.0
    except ValueError:
        return 0.0


def has_gpu() -> bool:
    result = run(["bash", "-lc", "command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi -L"], timeout=15)
    return result.returncode == 0 and "GPU" in result.stdout


def main() -> int:
    candidate, checked = choose_candidate()
    if not candidate:
        print(json.dumps({"status": "silent", "reason": "no_unprocessed_episode", "checked": checked[:10]}, indent=2))
        return 0

    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")
    title, page_url, processed_id = candidate["title"], candidate["link"], candidate["id"]
    safe = slugify(title)
    audio_url = extract_audio_url(page_url)
    if not audio_url:
        video_url = extract_youtube_url(page_url)
        if video_url:
            print(json.dumps({
                "status": "video_fallback_required",
                "reason": "real_episode_has_youtube_embed_but_no_mp3",
                "episode_title": title,
                "episode_url": page_url,
                "youtube_url": video_url,
                "processed_id": processed_id,
                "candidate_source": candidate["source"],
                "next_step": "Follow references/video-only-episode-fallback.md; do not mark processed until Daily-Session and transcript notes exist.",
            }, indent=2))
            return 0
        raise RuntimeError(f"Could not find MP3 or YouTube embed for {title}: {page_url}")

    audio_path = AUDIO_DIR / f"{today}-{safe}.mp3"
    if not audio_path.exists() or audio_path.stat().st_size < 10000:
        download(audio_url, audio_path)
    dur = duration_seconds(audio_path)
    no_gpu_long = (not has_gpu()) and dur > 300
    tx_status = f"skipped_no_gpu_episode_{int(dur)}s" if no_gpu_long else "pending_manual_or_short_episode_transcription"
    status = "structured_fallback_no_transcript" if no_gpu_long else "structured_fallback_transcription_not_run"

    transcript_note = TRANS / f"{today}-{safe}-Transcript.md"
    transcript_note.write_text(
        f"---\ndate: {today}\npodcast_title: {title!r}\nepisode_url: {page_url}\naudio_url: {audio_url}\naudio_file: {audio_path}\nduration_seconds: {int(dur)}\ntranscription_status: {tx_status}\n---\n\n"
        f"# Transcript Placeholder: {title}\n\nWhisper transcription was not completed during the scheduled run. Status: `{tx_status}`.\n\nDownloaded audio: `{audio_path}`\n",
        encoding="utf-8",
    )

    duration_label = time.strftime("%H:%M:%S", time.gmtime(int(dur))) if dur else "unknown"
    topics = ", ".join(candidate.get("topics") or ["Pharmacology"])
    obs_file = f"Daily-Sessions/{today}-{safe}.md"
    note_path = DAILY / f"{today}-{safe}.md"
    note_path.write_text(
        f"---\ndate: {today}\ntime: {now}\npodcast_title: {json.dumps(title)}\npodcast: {json.dumps(title)}\nepisode_url: {page_url}\naudio_url: {audio_url}\naudio_file: {audio_path}\nduration: {duration_label}\nduration_seconds: {int(dur)}\ntopic: {json.dumps(topics)}\nusmle_weight: High\nprocessing_status: {status}\ntranscription_status: {tx_status}\ntranscript_note: \"Transcripts/{transcript_note.name}\"\nsource: {candidate['source']}\nprocessed_id: {processed_id}\n---\n\n"
        f"# {title}\n\nSource: [Episode page]({page_url})  \nAudio: [MP3]({audio_url})  \nTranscript handoff: [[{transcript_note.stem}]]\n\n"
        "## Key Lessons\n- Structured fallback created from episode metadata because transcription was not available in this cron environment.\n\n"
        "## Mechanisms Explained\n- To be filled after transcript review; focus on mechanisms, receptor/enzyme targets, adverse effects, and clinical indications.\n\n"
        f"## Drug Connections\n### New Drugs\n- To be extracted from transcript/manual review.\n\n### System Connections\n- Topic/source: {topics}.\n\n### Previous Drug Links\n- Add links to prior Divine Pharmacology notes after transcript/manual review.\n\n"
        "## Comprehension Questions\n- After transcript completion: write 3-5 USMLE-style questions covering mechanism, adverse effects, contraindications, and clinical use.\n\n"
        "## USMLE High-Yield Points\n- Episode queued for high-yield extraction; audio was downloaded and a transcript placeholder was created for follow-up.\n\n"
        f"## Processing Log\n- Candidate source: {candidate['source']}\n- Processed ID: `{processed_id}`\n- Audio downloaded: `{audio_path}`\n- Duration: `{duration_label}` ({int(dur)} seconds)\n- Transcription status: `{tx_status}`\n",
        encoding="utf-8",
    )

    additions = []
    for marker in (processed_id, page_url):
        if marker and marker not in processed_text:
            additions.append(marker)
    if additions:
        with PROCESSED.open("a", encoding="utf-8") as f:
            for marker in additions:
                f.write(marker + "\n")

    obsidian_url = "obsidian://open?vault=Divine-Pharmacology&file=" + urllib.parse.quote(obs_file)
    print(json.dumps({
        "status": "processed",
        "episode_title": title,
        "episode_url": page_url,
        "note_path": str(note_path),
        "transcript_note": str(transcript_note),
        "audio_path": str(audio_path),
        "duration_seconds": int(dur),
        "processing_status": status,
        "transcription_status": tx_status,
        "obsidian_url": obsidian_url,
        "processed_markers_added": additions,
        "verified": {"note": note_path.exists(), "transcript_note": transcript_note.exists()},
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
