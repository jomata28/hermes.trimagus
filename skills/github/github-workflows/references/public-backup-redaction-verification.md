# Public backup redaction verification

Use this after copying `.env`/`config.yaml` into a **public** backup repository and running the redaction scripts.

## Why this check exists

A literal-token scanner may replace a token on a continuation line while leaving the YAML key on the preceding line, producing a shape such as:

```yaml
github:
  token:
    __REDACTED_FOR_GITHUB_BACKUP__
```

YAML may still parse this as a multiline scalar, but the formatting is ambiguous and can introduce trailing whitespace; malformed variants can instead become nested mappings. Normalize every secret placeholder to an explicit single-line scalar:

```yaml
github:
  token: "__REDACTED_FOR_GITHUB_BACKUP__"
```

## Focused verification

1. Parse the repository copy of `config.yaml` with `yaml.safe_load`.
2. Assert sensitive scalar fields expected to be redacted equal `__REDACTED_FOR_GITHUB_BACKUP__`.
3. Re-run `scripts/scan-redact-literal-tokens.py` and require `literal_remaining_count=0`.
4. Stage the backup, then run `git diff --cached --check` before committing.
5. After committing, run `git show --check --oneline HEAD`.
6. Before committing, create a focused verifier with Python's OS-safe `tempfile.NamedTemporaryFile(prefix="hermes-verify-", suffix=".py", dir="/tmp", delete=False)`. Run it against the repository copy, require a zero exit status, remove it, and assert the temporary path no longer exists. This avoids verification systems rejecting a hand-written or ambiguously named probe.
7. The verifier should minimally parse `config.yaml`, assert the redacted secret field remains a string scalar equal to `__REDACTED_FOR_GITHUB_BACKUP__`, and fail on malformed nested mappings such as `token: {__REDACTED_FOR_GITHUB_BACKUP__: null}`.
8. Report this as **targeted ad-hoc verification**, not as a project test-suite pass. Include both the probe result and cleanup result in the evidence.
9. Confirm cleanup and synchronization with `git status --short --branch` and matching local/remote SHAs.

Do not weaken the live source configuration to make verification pass; normalize or redact only the repository copy.