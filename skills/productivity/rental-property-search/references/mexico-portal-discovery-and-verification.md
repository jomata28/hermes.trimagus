# Mexico portal discovery and verification

Use these patterns for Propiedades.com, EasyBroker/Pincali, and local-agency inventory when normal browser access or portal search is incomplete.

## Discovery versus verification

- Search-engine results are useful only for discovering stable individual URLs. Query by exact phrases such as `amueblado`, bedroom count, neighborhood, and portal path (`/inmueble/`, `/mx/inmueble/`).
- EasyBroker and Pincali often expose the same underlying inventory and ID (`EB-...`). Treat matching title, ID, photos, dimensions, and description as one listing, not two sources.
- Portal recommendation cards can surface current-looking inventory from an old individual page. Never infer that the page itself is active from its recommendations.

## Text-mirror fallback

When the normal page is blocked, retrieve the exact individual URL through a reputable text-rendering mirror such as `https://r.jina.ai/http://<host/path>` and inspect the rendered page. Use this only as a reading fallback; report the canonical individual URL to the user.

### When the text mirror also fails

Reader proxies like r.jina.ai use datacenter egress IPs themselves, so they cannot bypass IP-reputation WAF blocks:

- **Propiedades.com:** Serves a JavaScript anti-bot challenge. jina.ai returns the challenge HTML (confirming the site is up) but not the rendered content. The VPS headless browser also fails (`ERR_HTTP2_PROTOCOL_ERROR`) because it runs with `--no-sandbox`/`--headless` flags that are themselves bot fingerprints.
- **Lamudi.com.mx:** Behind CloudFront. Returns `401 Unauthorized` even through jina.ai. Even `robots.txt` and `sitemap.xml` return 403. No datacenter-egress path works.

When both direct access and reader proxies fail, the only remaining automated path is the **mobile-proxy tunnel** (see `navigate-bot-protected-sites` skill, `references/user-owned-mobile-egress.md`). If no tunnel is active, inform the user that the portals are blocked from this server and offer the manual-browser fallback.

### Search-engine URL discovery during portal blocking

Google and DuckDuckGo return CAPTCHA challenges from datacenter IPs. Bing loads but **silently ignores the `site:` operator** in many queries, returning irrelevant results. Do not rely on `site:` alone — use the domain as a quoted search term and decode Bing's base64 redirect URLs to find actual listing pages. See `navigate-bot-protected-sites` skill, `references/reader-proxy-and-search-engine-diagnosis.md` for the full accessibility matrix and Bing workaround.

**⚠️ Reader-proxy limitations (validated 2026-08-17):**

r.jina.ai uses datacenter egress IPs itself, so it cannot bypass IP-reputation WAF blocks. However, it is NOT uniformly blocked — the behavior differs by portal:

- **Propiedades.com:** jina.ai returns the JS challenge HTML page (site is up, challenge is JS-based). The VPS headless browser fails with `ERR_HTTP2_PROTOCOL_ERROR` because it runs with `--no-sandbox`/`--headless` flags that are themselves bot fingerprints. jina.ai confirms the site structure but cannot render content.
- **Lamudi.com.mx:** Behind CloudFront. Returns `401 Unauthorized` even through jina.ai. Even `robots.txt` and `sitemap.xml` return 403. No datacenter-egress path works.
- **Inmuebles24 / Vivanuncios / EasyBroker:** May be Cloudflare-protected. Test with jina.ai first — if it returns a Cloudflare challenge page rather than content, the block is IP-reputation-based.
- **Google Cache** (`webcache.googleusercontent.com`) is CAPTCHA-blocked from the VPS network.
- **Wayback Machine** returned 503 during testing — do not rely on it as a guaranteed fallback.

**Working alternatives when portals are WAF-blocked:**

1. **MercadoLibre Inmuebles** (`inmuebles.mercadolibre.com.mx`) — not Cloudflare-protected, loads in headless Chrome. Use as primary alternative when all other portals are blocked.
2. **Mobile-proxy tunnel** — the only confirmed path to Lamudi/CloudFront-protected portals from this VPS. See `navigate-bot-protected-sites` skill, `references/user-owned-mobile-egress.md`. Requires an active reverse SSH tunnel on port 8888.
3. **Human-in-the-loop noVNC** — launch Chrome as `jt` with CDP, have JT solve the Turnstile/JS challenge manually, then extract via CDP `Runtime.evaluate`.
4. **Search-engine cached snippets** — Bing loads from the VPS but silently ignores `site:` operator. Google/DuckDuckGo return CAPTCHAs. Snippets may contain partial listing data (price, bedrooms) but do NOT prove the individual page is accessible or current. Treat as unverified leads only.

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