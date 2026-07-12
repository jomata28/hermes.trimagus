#!/usr/bin/env python3
from pathlib import Path
import re, sys
PLACEHOLDER="__REDACTED_FOR_GITHUB_BACKUP__"
PATTERNS=[re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),re.compile(r"gh[pousr]_[A-Za-z0-9_]{10,}"),re.compile(r"sk-or-v1-[A-Za-z0-9_-]{20,}"),re.compile(r"sk-[A-Za-z0-9_-]{20,}"),re.compile(r"gsk_[A-Za-z0-9_-]{20,}"),re.compile(r"ntn_[A-Za-z0-9_]{10,}"),re.compile(r"secret_[A-Za-z0-9]{10,}"),re.compile(r"AKIA[0-9A-Z]{16}"),re.compile(r"AIza[0-9A-Za-z_-]{20,}")]
def iter_text_files(repo):
    for p in repo.rglob("*"):
        if not p.is_file() or ".git" in p.parts: continue
        try: data=p.read_bytes()
        except OSError: continue
        if b"\0" in data[:4096]: continue
        try: text=data.decode("utf-8")
        except UnicodeDecodeError:
            try: text=data.decode("utf-8","surrogateescape")
            except Exception: continue
        yield p,text
def main():
    repo=Path(sys.argv[1]).resolve(); changed=[]
    for p,text in iter_text_files(repo):
        orig=text
        for pat in PATTERNS: text=pat.sub(PLACEHOLDER,text)
        if text!=orig: p.write_text(text,encoding="utf-8",errors="surrogateescape"); changed.append(str(p.relative_to(repo)))
    remaining=[]
    for p,text in iter_text_files(repo):
        if any(pat.search(text) for pat in PATTERNS): remaining.append(str(p.relative_to(repo)))
    print("literal_redacted_files="+",".join(changed)); print("literal_remaining_count="+str(len(remaining)))
    if remaining: print("\n".join(remaining[:50])); sys.exit(1)
if __name__ == "__main__": main()
