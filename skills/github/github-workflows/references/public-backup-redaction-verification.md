# Public backup redaction verification

Use this after copying `.env`/`config.yaml` into a **public** backup repository and running the redaction scripts.

## Why this check exists

A literal-token scanner may replace a token on a continuation line while leaving the YAML key on the preceding line, producing a shape such as:

```yaml
github:
  token:
    __REDACTED_FOR_GITHUB_BACKUP__
```

That can still parse, but it changes the value from a scalar into a nested mapping and may also introduce trailing whitespace. Normalize it to a scalar placeholder:

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
6. If the platform requests fresh verification evidence, create the probe with `mktemp /tmp/hermes-verify-XXXXXXXX.py`, run it, and remove it. Report this as **targeted ad-hoc verification**, not as a project test-suite pass.
7. Confirm cleanup and synchronization with `git status --short --branch` and matching local/remote SHAs.

Do not weaken the live source configuration to make verification pass; normalize or redact only the repository copy.