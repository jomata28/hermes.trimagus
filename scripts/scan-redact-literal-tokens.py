#!/usr/bin/env python3
"""Redact literal token-shaped strings across a backup repo copy, then verify none remain.

Use after copying dotfiles/config/skills into a GitHub backup repo and after targeted
.env/config redaction. This script intentionally scans text files only and skips .git/.
It is designed for the backup repository copy, not the live ~/.hermes source.

Usage:
  python scripts/scan-redact-literal-tokens.py /path/to/backup/repo
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

PLACEHOLDER = "__REDACTED_FOR_GITHUB_BACKUP__"
PATTERNS = [
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{10,}"),
    re.compile(r"sk-or-v1-[A-Za-z0-9_-]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"gsk_[A-Za-z0-9_-]{20,}"),
    re.compile(r"ntn_[A-Za-z0-9_]{10,}"),
    re.compile(r"secret_[A-Za-z0-9]{10,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
]


def iter_text_files(repo: Path):
    for path in repo.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if b"\0" in data[:4096]:
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = data.decode("utf-8", "surrogateescape")
            except Exception:
                continue
        yield path, text


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    repo = Path(sys.argv[1]).expanduser().resolve()
    if not repo.is_dir():
        print(f"not a directory: {repo}", file=sys.stderr)
        return 2

    changed: list[str] = []
    for path, text in iter_text_files(repo):
        original = text
        for pattern in PATTERNS:
            text = pattern.sub(PLACEHOLDER, text)
        if text != original:
            path.write_text(text, encoding="utf-8", errors="surrogateescape")
            changed.append(str(path.relative_to(repo)))

    remaining: list[str] = []
    for path, text in iter_text_files(repo):
        if any(pattern.search(text) for pattern in PATTERNS):
            remaining.append(str(path.relative_to(repo)))

    print("literal_redacted_files=" + ",".join(changed))
    print("literal_remaining_count=" + str(len(remaining)))
    if remaining:
        print("\n".join(remaining[:50]))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
