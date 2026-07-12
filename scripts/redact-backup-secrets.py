#!/usr/bin/env python3
from pathlib import Path
import re, sys
PLACEHOLDER = "__REDACTED_FOR_GITHUB_BACKUP__"
SECRET_KEY_RE = re.compile(r"(api[_-]?key|token|secret|password|passwd|pwd|credential|auth|bearer|private[_-]?key|access[_-]?key|client[_-]?secret|webhook|cookie)", re.I)
INLINE_PATTERNS = [re.compile(r"sk-or-v1-[A-Za-z0-9_-]+"), re.compile(r"gsk_[A-Za-z0-9_-]+"), re.compile(r"ntn_[A-Za-z0-9_-]+|secret_[A-Za-z0-9]+"), re.compile(r"gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+")]
def redact_env(path):
    changed=0; out=[]
    for line in path.read_text(errors="surrogateescape").splitlines(True):
        m=re.match(r"^([A-Za-z_][A-Za-z0-9_]*)(\s*=\s*)(.*?)(\r?\n)?$", line)
        if m and SECRET_KEY_RE.search(m.group(1)):
            val=m.group(3).strip()
            if val and val not in ('""', "''", PLACEHOLDER):
                quote = val[0] if len(val)>=2 and val[0]==val[-1] and val[0] in "'\"" else ""
                out.append(f"{m.group(1)}{m.group(2)}{quote}{PLACEHOLDER}{quote}{m.group(4) or ''}"); changed+=1; continue
        out.append(line)
    text="".join(out)
    for pat in INLINE_PATTERNS:
        text,n=pat.subn(PLACEHOLDER,text); changed+=n
    path.write_text(text, errors="surrogateescape"); return changed
def redact_yamlish(path):
    changed=0; out=[]
    pat=re.compile(r"^(\s*)([A-Za-z0-9_.-]*?(?:api[_-]?key|token|secret|password|passwd|pwd|credential|auth|bearer|private[_-]?key|access[_-]?key|client[_-]?secret|webhook|cookie)[A-Za-z0-9_.-]*)(\s*:\s*)(.*?)(\s*(?:#.*)?)?(\r?\n)?$", re.I)
    for line in path.read_text(errors="surrogateescape").splitlines(True):
        m=pat.match(line)
        if m:
            val=(m.group(4) or "").strip(); already={"{}","[]","null","Null","NULL","~",PLACEHOLDER,f'"{PLACEHOLDER}"',f"'{PLACEHOLDER}'"}
            if val and val not in already:
                out.append(f'{m.group(1)}{m.group(2)}{m.group(3)}"{PLACEHOLDER}"{m.group(5) or ""}{m.group(6) or ""}'); changed+=1; continue
        out.append(line)
    text="".join(out)
    for pat2 in INLINE_PATTERNS:
        text,n=pat2.subn(PLACEHOLDER,text); changed+=n
    path.write_text(text, errors="surrogateescape"); return changed
def main():
    repo=Path(sys.argv[1]).resolve(); rels=sys.argv[2:] or [".env","config.yaml"]; total=0
    for rel in rels:
        p=repo/rel
        if p.exists() and p.is_file(): total += redact_env(p) if p.name==".env" else redact_yamlish(p)
    print(f"redacted_fields={total}")
if __name__ == "__main__": main()
