# Structured listing extraction from server-rendered JavaScript pages

Use this when a rental portal exposes search inventory in page source even though browser search, indexing, or detail-page navigation is incomplete.

## Next.js workflow

1. Fetch every result-page URL, including all pagination pages.
2. Extract the JSON inside `<script id="__NEXT_DATA__" type="application/json">`.
3. Locate the publication/listing array under `props.pageProps`; key names vary, so inspect rather than assuming one fixed path.
4. Filter on structured fields before reading prose:
   - listing status (`PUBLISHED`, active badge, or equivalent);
   - transaction type;
   - structured bedroom count;
   - base rent, maintenance fee, and known total;
   - explicit furnished boolean/attribute;
   - location and coordinates;
   - canonical slug/reference ID.
5. Read the title and full description for contradictions, negations, extra fees, and whether bedrooms are genuine rather than studies or flex rooms.
6. Open the canonical individual slug and verify that it still resolves before reporting it.
7. Inspect photos only to assess condition and corroborate furniture. Furniture in photos is never proof that it is included.

## Useful evidence hierarchy

Strongest to weakest:

1. Individual live page plus explicit prose and structured attributes.
2. Individual live page plus structured embedded data.
3. Current search-page embedded publication object with canonical slug, followed by a successful detail-page check.
4. Search card or index snippet only — discovery evidence, not a reportable match.

## Pricing caution

Portals may expose `basePrice`, `maintenanceFee`, and `totalAmount`, but prose can mention a fee that conflicts with the structured object. Recalculate the known total from the clearest explicit evidence and flag unresolved conflicts. Do not treat a value of zero as proof that maintenance is included when prose says it is extra.

## Coverage language

Keep an attempted-source ledger. Distinguish:

- **inventory reviewed:** listing/search data were actually retrieved and candidates evaluated;
- **source attempted but blocked:** only a CAPTCHA, 403, error page, or unusable response was reached;
- **candidate verified:** canonical individual page loaded and all hard filters were confirmed.

Do not write “reviewed all requested portals” when some yielded only blocks. Report the narrower truthful coverage and return fewer matches rather than padding.
