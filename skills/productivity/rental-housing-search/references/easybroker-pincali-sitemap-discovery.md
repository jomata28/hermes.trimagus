# EasyBroker/Pincali sitemap discovery and verification

Use this when ordinary search engines are rate-limited or when Pincali/EasyBroker search pages are difficult to enumerate. This is a **candidate-discovery** method, not listing-level verification.

## Sitemap route

1. Fetch `https://www.pincali.com/sitemap.xml` (or the site's current canonical sitemap index).
2. Read the child property sitemap URLs. Pincali has exposed compressed shards under `assets.easybroker.com/marketplace_sitemaps/`, commonly named `properties.xml.gz`, `properties1.xml.gz`, etc.
3. Download and decompress every advertised shard; do not assume a fixed shard count.
4. Extract `<loc>` values and filter URL slugs separately by:
   - target neighborhood aliases;
   - residential property terms;
   - rental terms;
   - furnished/semi-furnished terms.
5. Deduplicate candidate URLs before fetching detail pages.

## Important evidence limitations

A URL slug is historical discovery metadata, not proof of the current offer. Individual pages can be repurposed or updated so that:

- a slug containing `renta` now opens a sale listing;
- a slug containing `amueblada` no longer states that furniture is included;
- the current title, price, operation, or room count differs from the slug;
- unrelated nearby recommendations inject extra prices and room counts into raw page text.

Therefore, never extract fields by broad regex over the entire HTML document. Prefer, in order:

1. current listing detail fields in the rendered page;
2. listing-specific JSON-LD or application state;
3. current title and meta description, only as partial corroboration.

Ignore prices, bedrooms, and maintenance values from recommendation cards. If the page currently says sale while the slug says rent, classify it as stale/repurposed and exclude it.

## Rate-limit discipline

- Parse the sitemap index dynamically and cache downloaded shards locally during the run.
- Filter URLs before requesting detail pages.
- Fetch candidates slowly and retry only with bounded backoff.
- Treat HTTP 202 with an empty or challenge body, 403, CAPTCHA, or account verification as **unverified**, not as a live reviewed listing and not as evidence of zero inventory.
- If only a few detail pages remain accessible, report portal coverage and verification limitations separately from the strict-match count.

## Verification gate

A finalist must have current listing-level evidence for:

- direct URL and live operation (`En renta`);
- target neighborhood/location;
- current rent;
- exact true bedroom count;
- positive furnishing language (`amueblado`, furniture included), with no negation;
- maintenance amount or explicit inclusion.

If any required field is absent, place the listing under “pending confirmation,” not under verified matches. Preserve rejected examples only when they explain a common mismatch such as wrong bedroom count or a repurposed URL.