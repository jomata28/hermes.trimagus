# 2026-06-10 — GitHub placeholder token scan quirk

During the scheduled Hermes backup to `jomata28/hermes.trimagus`, the first redaction/scan pass still flagged `.env` because it contained a GitHub-token-shaped placeholder like `__REDACTED_FOR_GITHUB_BACKUP__...`.

## Durable lesson

Do not scan/redact only `ghp_[A-Za-z0-9]{20,}`. GitHub token placeholders and some copied examples may contain underscores after `ghp_`, so use a broader pattern in backup copies:

```python
re.compile(r'ghp_[A-Za-z0-9_]{10,}')
```

Likewise, for Notion-style examples/tokens, prefer allowing underscores:

```python
re.compile(r'ntn_[A-Za-z0-9_]{10,}')
```

Keep this as a backup-copy redaction rule, not a global source mutation rule. The aim is to prevent GitHub push protection failures and local secret-scan false negatives in the backup repo.

## Verification pattern

After redaction, run a second independent scan over every committed text file excluding `.git/`, then require no literal-token hits before `git add`/`git commit`.
