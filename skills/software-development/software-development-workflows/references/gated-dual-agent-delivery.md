# Gated dual-agent delivery

Use this pattern for production changes where the user requires an implementer, an independent reviewer, explicit approval gates, and no mutation before an initial audit.

## Roles

- **Hermes:** requirements custodian, orchestrator, independent verifier, and gatekeeper.
- **Primary implementer:** edits only its assigned branch/worktree and produces tests, evidence, operations docs, and rollback artifacts.
- **Independent reviewer:** starts from a separate clean worktree based on the completed implementation branch; initially reports findings only and does not edit.

Never allow implementer and reviewer to edit the same checkout.

## Phase 0: authoritative-input gate

1. Read all governing documents completely and in the user-specified order.
2. Treat earlier documents as constitutional/product constraints and later documents as scoped implementation authorization unless the documents say otherwise.
3. Do not infer missing attachments. Confirm each source is actually present before beginning.
4. Extract explicit prohibitions: canonical-data edits, deployment, merge, service restart, timer activation, secret handling, and scope exclusions.

## Phase A: genuinely read-only audit

The initial audit should cover:

- branch, actual remotes, HEADs, dirty/untracked/ignored files;
- language, dependencies, serving process, supervisor, and service account;
- current writers and commit path;
- ownership and permissions of canonical files plus Git metadata;
- backup mechanism and whether it survives host loss;
- canonical data structures and hashes;
- current tests and their executable baseline;
- secret references by name/location only;
- locking, validation, atomicity, idempotency, ledgers, and failure semantics;
- contradictions and concrete risks.

Run the primary agent with a read-only sandbox. If creating the requested audit file would violate the gate, have it emit proposed Markdown to stdout and create the file only after approval.

Hermes must independently check host-level facts that the sandbox cannot access, such as Docker, systemd, listeners, permissions from the service UID, and live health.

### Strong evidence patterns

- A green health check proves liveness, not write capability. Test read/write permissions as the actual service UID without mutating canonical data.
- `git status ... [ahead N]` can reflect a stale tracking ref. Compare `HEAD` to the actual remote with `git ls-remote` or the bare repository ref before claiming divergence.
- Two Git repositories on the same host are not an off-host backup.
- To establish that an unauthenticated mutation route is reachable without changing state, send a deliberately invalid request that is rejected before write, and verify HEAD plus canonical hashes remain unchanged.
- Do not install missing dependencies in production during a read-only audit. Record the baseline blocker and establish the executable baseline later in the isolated worktree.

At the end, re-run `git status --porcelain`, compare HEAD and canonical hashes, and list every artifact that was deliberately not created.

## Approval gate 1

Present the reconciled audit before creating branches, worktrees, backups, documentation files, or dependencies when the user required a strict no-mutation audit.

Do not convert “show me the audit first” into implied approval. Stop and request authorization for the next phase.

## Implementation phase

After approval:

1. Create a dated, recoverable backup outside all worktrees.
2. Record hashes of canonical files.
3. Create the implementation branch and dedicated worktree.
4. Put repository instructions in `AGENTS.md` as a concise index to canonical documents; do not duplicate doctrine.
5. Establish characterization tests before behavior changes.
6. Implement only authorized scope.
7. Keep timers/services installed but disabled if activation requires later approval.
8. Do not modify production checkout or canonical production data.

## Independent review phase

Create a separate clean review worktree from the completed implementation branch. The reviewer should inspect:

- corruption or data loss;
- races and lock coverage;
- atomic write sequence and crash windows;
- authorization boundaries;
- null/unknown preservation;
- idempotency and deduplication;
- false-success states;
- secret exposure and excessive permissions;
- missing tests;
- deployment or product changes outside scope;
- rollback realism.

Require severity, file/location, impact, and recommended correction. Reviewer edits happen only after Hermes assigns specific fixes, preferably in a distinct correction commit.

## Approval gate 2

Before merge, deployment, restart, or timer activation, show the user:

1. complete diff;
2. test commands and real outputs;
3. independent review and disposition of findings;
4. remaining risks;
5. rollback procedure tested against a copy;
6. exact production actions awaiting approval.

A documented rollback is not enough. Exercise it on a copy and verify restored hashes, data validity, and service behavior where possible.

## Common pitfalls

- Writing the audit document during a gate that forbids all repository mutations.
- Letting the reviewer “help” in the implementer checkout.
- Treating agent self-reports as evidence without rerunning checks.
- Using production as the dependency-install or characterization-test workspace.
- Reporting sandbox limitations as host facts instead of independently verifying them.
- Conflating app health with permissions, Git commit ability, or end-to-end write safety.
- Proceeding from audit to implementation without the explicit approval the user requested.
