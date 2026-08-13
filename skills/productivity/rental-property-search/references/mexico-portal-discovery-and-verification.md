# Mexico portal discovery and verification

Use these patterns for Propiedades.com, EasyBroker/Pincali, and local-agency inventory when normal browser access or portal search is incomplete.

## Discovery versus verification

- Search-engine results are useful only for discovering stable individual URLs. Query by exact phrases such as `amueblado`, bedroom count, neighborhood, and portal path (`/inmueble/`, `/mx/inmueble/`).
- EasyBroker and Pincali often expose the same underlying inventory and ID (`EB-...`). Treat matching title, ID, photos, dimensions, and description as one listing, not two sources.
- Portal recommendation cards can surface current-looking inventory from an old individual page. Never infer that the page itself is active from its recommendations.

## Text-mirror fallback

When the normal page is blocked, retrieve the exact individual URL through a reputable text-rendering mirror such as `https://r.jina.ai/http://<host/path>` and inspect the rendered page. Use this only as a reading fallback; report the canonical individual URL to the user.

A mirror response is still secondary evidence. Verify these page-level signals:

- explicit `Fuera del mercado` or equivalent;
- current contact controls and absence of an inactive banner;
- advertised rent and maintenance;
- explicit furnishing statement in the description;
- exact listing ID and property facts;
- requirements stated in the full description.

If the mirror returns only nearby recommendations, a challenge page, or truncated body, the candidate is not individually verified.

## Propiedades.com pitfalls

- Result cards may label a listing `3 recámaras` and `Amueblado` while the individual page omits the bedroom count or only says `equipado`/`listo para habitar`. This is a lead, not a verified match.
- Search URL filters can be ignored or can include recommendations outside the requested ceiling/geography. Reapply hard filters from each card and then from each individual page.
- Very low prices can be malformed, stale, partial-room offers, or missing maintenance. Flag them for advertiser confirmation rather than promoting them as bargains.
- A page with `Consultar` or `Ver teléfono` but no inactive banner is only portal-active, not advertiser-confirmed. Label it `vigencia de portal`; true current availability requires direct advertiser confirmation.

## EasyBroker/Pincali requirements extraction

The individual body often gives unusually useful exact terms. Capture them verbatim when present:

- rent plus separate maintenance and total monthly cost;
- deposit and first month;
- póliza jurídica and who pays it;
- aval, obligado solidario, or company guarantee;
- contract term and pagarés;
- pet restrictions;
- whether photographed furniture may vary.

An otherwise perfect listing marked `Fuera del mercado` belongs only in a clearly separated discarded/stale section, never in the shortlist.

## Reporting status precisely

Use one of these labels:

1. **Verified active with advertiser** — direct recent confirmation.
2. **Portal-active, confirmation pending** — individual page is live and contactable, but no direct confirmation.
3. **Unverified lead** — one or more hard facts exist only on a result card/snippet.
4. **Inactive/stale** — explicit out-of-market banner or dead individual page.

Do not call status 2 or 3 simply `vigente`.