# Reader-Proxy and Search-Engine Diagnosis from Datacenter IPs

Session-validated techniques for when the VPS datacenter IP is blocked by target-site WAF (CloudFront, Cloudflare, Akamai) and you need to either (a) read the target page through a proxy or (b) discover indexed listing URLs via search engines.

## r.jina.ai Reader Proxy

### What it is
`https://r.jina.ai/<target-url>` fetches and renders a web page from jina.ai's own egress IPs, returning the page content as markdown or HTML. It is a reading/diagnostic tool, not a scraping tool.

### Usage
```bash
# Default: returns markdown
curl -s --max-time 30 -A "Mozilla/5.0" \
  "https://r.jina.ai/https://target-site.com/path" -o /tmp/jina_result.txt

# Force HTML output (useful to see challenge pages)
curl -s --max-time 30 -H "X-Return-Format: html" -A "Mozilla/5.0" \
  "https://r.jina.ai/https://target-site.com/path" -o /tmp/jina_result.html
```

### What works
- **Sites with JS challenges (not WAF IP blocks):** Propiedades.com serves a JavaScript challenge page. Through jina.ai, the challenge page HTML is returned (confirming the site is up and identifying the challenge type), even though the VPS browser gets `ERR_HTTP2_PROTOCOL_ERROR` directly.
- **Search engine result pages:** jina.ai can fetch Bing search results when the VPS's direct Google/DuckDuckGo access is CAPTCHA-blocked. This is useful for discovering indexed URLs.
  ```bash
  curl -s --max-time 30 -A "Mozilla/5.0" \
    "https://r.jina.ai/https://www.bing.com/search?q=site:target.com+keywords" \
    -o /tmp/jina_bing.txt
  ```

### What does NOT work
- **CloudFront WAF IP-reputation blocks:** Lamudi.com.mx (behind CloudFront) returns `401 Unauthorized` even through jina.ai. jina.ai's egress IPs are also datacenter IPs that CloudFront distrusts. The block is IP-reputation-based, not content-based, so no reader proxy that uses datacenter egress will help.
- **JS challenge execution:** jina.ai returns the challenge HTML page, not the post-challenge rendered content. It cannot solve JS challenges.

### Decision tree
```
Direct browser/curl fails (403/401/connection error)
  → Try r.jina.ai
    → Returns real page content → use as reading fallback (secondary evidence)
    → Returns challenge page HTML → site is up but JS-challenged; need real browser
    → Returns 401/403/error → IP-reputation WAF block; need residential egress (Tier 5)
```

## Search-Engine Accessibility from Datacenter IPs

Tested 2026-08-17 from VPS IP 82.197.95.9:

| Engine | Direct (browser/curl) | Via jina.ai | Notes |
|--------|----------------------|-------------|-------|
| Google | ❌ CAPTCHA block | ❌ CAPTCHA block | "unusual traffic from your computer network" |
| DuckDuckGo | ❌ CAPTCHA challenge | untested | "Select all squares containing a duck" image challenge |
| Bing | ✅ Loads | ✅ Loads | But `site:` operator is unreliable (see below) |
| Brave | ✅ Loads (JS-dependent) | untested | Results require JS rendering; raw HTML empty |
| Yandex | ❌ Empty response | untested | Connection returns nothing |

### Bing `site:` operator pitfall (IMPORTANT)

Bing silently ignores the `site:` operator in many cases, returning irrelevant results instead of an error or "no results":

- Query `site:lamudi.com.mx "santa fe" "3 recamaras" renta departamento` returned **Santa Claus Wikipedia pages** and Google Santa Tracker — Bing completely ignored the `site:` restriction.
- Query `site:propiedades.com departamento renta santa fe 3 recamaras amueblado` returned **apartments.com and apartmenthomeliving.com results** — again ignoring the `site:` filter.

**Workaround:** Do not rely on `site:` alone. Use the domain name as a quoted search term and scan results manually, or use Bing's `url:` or `link:` operators if available. When using jina.ai to fetch Bing results, decode the base64-encoded redirect URLs (`u=a1<base64>`) to extract actual destination URLs:

```bash
grep -oE 'u=a1[a-zA-Z0-9_-]+' /tmp/jina_bing.txt | \
  sed 's/u=a1//' | while read b64; do \
    echo "$b64" | base64 -d 2>/dev/null; echo ""; \
  done | grep -i target-domain
```

## Lamudi (CloudFront) specifics

- Lamudi.com.mx is behind CloudFront and returns `403 ERROR` (browser) or `401 Unauthorized` (curl) for all datacenter IPs.
- Even `robots.txt` and `sitemap.xml` return 403 — there is no way to discover listing URLs from Lamudi's own infrastructure without a residential IP.
- The mobile-proxy tunnel (see `references/user-owned-mobile-egress.md`) is the only confirmed path to Lamudi access from this VPS.

## Propiedades.com specifics

- DNS resolves (23.34.62.169) but direct TCP connections fail from the VPS (`ERR_HTTP2_PROTOCOL_ERROR`, curl returns HTTP 000).
- The site serves a JavaScript anti-bot challenge (detected via jina.ai HTML output) — it is not a simple IP block but a JS challenge that the headless agent browser (running with `--no-sandbox` and `--headless`) cannot pass.
- Per the `user-owned-mobile-egress.md` reference: `--no-sandbox` is itself a bot fingerprint that Akamai-style protection detects. The agent browser's flags make it inherently detectable.

## Wayback Machine as fallback

- The Wayback Machine CDX API (`web.archive.org/cdx/search/cdx`) and direct archive access (`web.archive.org/web/2026/<url>`) both returned `503 Service Unavailable` during this session.
- Do not rely on Wayback Machine as a guaranteed fallback — it has its own availability issues.
