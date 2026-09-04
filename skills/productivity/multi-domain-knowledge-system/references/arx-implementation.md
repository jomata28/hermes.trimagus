# ARX implementation notes

Use this reference when operating Jose's ARX implementation of a multi-domain personal system.

## Architecture

- Repo: `/srv/arx/app`
- Web app: `https://srv1056157.hstgr.cloud`
- The app is a read-only presentation layer over `/srv/arx/app/data/*.json`.
- Hermes writes data. ARX itself has no reasoning or autonomous data production.
- Do not modify `index.html` or anything outside `data/` unless Jose explicitly changes the ownership rule.

Primary files:

- `data/proyectos.json`: projects and project-owned tasks
- `data/agentes.json`: agent jobs, last runs, outputs, and watch list
- `data/taxonomia.json`: frozen CAPA layers/domains
- `data/tempus.json`: dates and closing windows
- `data/pietas.json`: relationship recency

## Deployment topology (VPS)

- ARX container `arx` (image `arx:local`, `node servidor.mjs` :4173) sits on Docker network `root_default` behind Traefik (`root-traefik-1`, owns 80/443, Let's Encrypt resolver `mytlschallenge`, label-based discovery). No published ports; only Traefik reaches it.
- `/srv/arx/app` is bind-mounted at `/app`, so commits made from the phone land on host disk and survive container recreation.
- Wildcard DNS: any `*.srv1056157.hstgr.cloud` subdomain resolves to the VPS. Adding a sibling service (e.g. `hermes.` for the Hermes dashboard — recipe in the `hermes-ops` skill, `references/dashboard-traefik-exposure.md`) needs zero DNS work: run a labeled container on `root_default`.
- Deploy flow: `git push vps master` (SSH → bare repo `/srv/arx/repo.git`), then on the VPS `cd /srv/arx/app && git pull /srv/arx/repo.git master && docker restart arx`. GitHub is backup only.
- History carries two commit identities: app/deploy commits as `ARX <arx@srv1056157.hstgr.cloud>`, Hermes data commits as the Hermes identity per the write-and-commit protocol below.

## Non-negotiable data rule

Never fabricate a run, date, measurement, status, or output. Unknown means `null`. Preserve `null` until a real observation or executed run supplies a value. Empty honest state is better than plausible invented state.

## Write and commit protocol

1. Read the current JSON and inspect Git status before editing.
2. If upstream changed, use `git pull --rebase`. Never force.
3. Edit only the required file under `data/`.
4. Validate JSON and product invariants.
5. Commit every change:

```bash
cd /srv/arx/app
git add data/<file>.json
git -c user.name=Hermes -c user.email=hermes@srv1056157.hstgr.cloud \
  commit -m "mensaje en español, presente y concreto"
```

## Product invariants

- At most four priorities globally, numbered 1 through 4 with no duplicates.
- PIETAS uses recency only, never scores, levels, bars, or percentages.
- ARENA reports position, inputs, and external clock, not promised outcomes.
- `null` is rendered as a named unknown state, never coerced to zero or blank.
- CAPA contains domains and character statistics, not projects.
- Project tasks live under their project, not directly on a calendar.

Areas:

- `otium`: chosen for enjoyment
- `negotium`: duties and obligations
- `bellum`: expansion of internal or external territory
- `sin_decidir`: not yet classified

Do not classify Bellum merely because something has a deadline.

## Agent rollout

Roles are `tesserarius` daily, `speculator` weekly, `scriba` continuous, and `augurium` monthly. Current rollout rule: activate `speculator` first and alone for one month before building the others. Hermes is the only Telegram voice; roles do not receive separate channels.

Before saying an agent runs, verify all of the following:

- process or cron exists;
- `data/agentes.json` shows `estado: activo`;
- `ultimaCorrida` is a real ISO date from an executed run;
- `ultimaSalida` describes real produced output.

A healthy ARX Docker container and HTTP 200 prove only that the dashboard runs. They do not prove the agent layer is installed or scheduled.

## Current-state interpretation pattern

Report the two layers separately:

1. **Dashboard/application:** container health, HTTP status, JSON readability.
2. **Agent automation:** process/cron, agent state, last real run/output.

This distinction prevents telling Jose that ARX is operational when only the read-only interface is live.
