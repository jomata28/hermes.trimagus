# MercadoLibre Inmuebles Extraction (CDMX rental searches)

## Why this portal
Inmuebles24 + Vivanuncios = Cloudflare Turnstile challenge (no auto-resolve even in persistent Chrome).
Propiedades.com = ERR_HTTP2_PROTOCOL_ERROR / TCP never completes. Lamudi = CloudFront 401.
MercadoLibre Inmuebles renders fully through the VPS Chrome (user `jt`, residential proxy `127.0.0.1:8888`, CDP port e.g. 9333). It is the reliable fallback for CDMX rental search.

## CDP navigation FIX (critical)
`Page.navigate` over raw CDP websocket **silently fails** on MercadoLibre — the URL never changes.
Use `Runtime.evaluate` with `window.location.href = '<url>'` instead, then wait ~8-10s and re-query
`window.location.href` + `document.title` to confirm the navigation actually landed.

```python
cdp_eval(ws_url, "window.location.href = 'https://inmuebles.mercadolibre.com.mx/departamentos/renta/3-recamaras/distrito-federal/coyoacan/'", timeout=10)
time.sleep(10)
cur = cdp_eval(ws_url, 'JSON.stringify({url: window.location.href, title: document.title})')
```
Expected title: `Departamentos en Renta en Coyoacán, 3 recámaras | MercadoLibre.com.mx`.
If you see "No encontramos resultados para tu búsqueda" that is a REAL empty result (e.g. San Ángel 3BR).

## Working URL shapes
- `https://inmuebles.mercadolibre.com.mx/departamentos/renta/3-recamaras/distrito-federal/coyoacan/`
- `https://inmuebles.mercadolibre.com.mx/departamentos/renta/distrito-federal/alvaro-obregon/santa-fe/`
- MercadoLibre may reorder path segments (e.g. `/renta/3-recamaras/distrito-federal/coyoacan/`). If a URL 404s/redirects, let it redirect and read the final `window.location.href`.
- `_PriceRange-24000-30000` suffix: unreliable — gets dropped. Filter in Python instead.
- `/amueblado/` segment: unreliable — gets dropped. Search all 3BR then filter descriptions for amueblado.

## Card extraction JS (run via CDP Runtime.evaluate)
```javascript
(function() {
    var results = [];
    var links = document.querySelectorAll('a[href*="MLM"]');
    links.forEach(function(a) {
        var href = a.href;
        var card = a.closest('li, [class*="ui-search-result"], [class*="poly-card"]');
        var text = card ? card.innerText : '';
        text = text.replace(/\n+/g, ' | ').replace(/\s+/g, ' ').trim();
        results.push({href: href, text: text.substring(0, 800)});
    });
    return JSON.stringify(results);
})()
```
- Dedupe by href — every card appears ~2x.
- Price regex: `MXN\s*\|?\s*([\d,]+)` — the card text looks like `MXN | 24,500 | 3 recámaras | 2 baños | 100 m²`.
- Bedrooms: `3 recámara` or `3 habitaciones` in card text.

## Verifying "amueblado" — avoid the false-positive trap
Checking `document.body.innerText.toLowerCase().includes('amueblado')` on the LISTING page returns True
almost always because page chrome/breadcrumbs mention it. Extract the REAL description instead:
```javascript
(function() {
    var descText = '';
    var selectors = ['[class*="ui-pdp-description"]', '[class*="item-description"]', '[class*="description__content"]', '[class*="ui-box-component"]', '#description'];
    for (var i = 0; i < selectors.length; i++) {
        var el = document.querySelector(selectors[i]);
        if (el && el.innerText && el.innerText.length > 200) { descText = el.innerText; break; }
    }
    if (!descText) {
        var all = document.querySelectorAll('*');
        for (var j = 0; j < all.length; j++) {
            var el = all[j];
            if (el.innerText && el.innerText.startsWith('Descripción')) { descText = el.innerText; break; }
        }
    }
    return JSON.stringify({title: document.querySelector('h1') ? document.querySelector('h1').textContent.trim() : '', desc: descText.substring(0, 1500)});
})()
```
Interpretation rules:
- "amueblad*" or "muebl*" in DESCRIPTION = furnished.
- "cocina equipada" / "equipad*" alone = appliances only, NOT furnished.
- "armarios empotrados" (built-in closets) = NOT furnished.
- Title says "amueblado" but description doesn't = still verify with the advertiser; treat as candidate, not confirmed.
- Sometimes a listing describes "2 recámaras + estudio" — check description, it is NOT 3 true bedrooms.

## Verified CDMX market floors (2026-08, MercadoLibre)
- Santa Fe 3BR: cheapest $48,000; typical $50k-130k. No 3BR under $48k. Furnished 3BR starts ~$45k (High Park Sur).
- Coyoacán 3BR: $13k-52k spread; furnished 3BR explicitly starts ~$45k (High Park Sur $45k, Amueblado 145m² $52k, Lomas del Pedregal $80k).
- San Ángel 3BR: ZERO listings on MercadoLibre.
- Budget reality for JT's brief ($24k-30k furnished 3BR near ABC Santa Fe or Coyoacán/San Ángel): does not exist on public portals; present the gap honestly and offer alternatives (unfurnished + furnish themselves, raise budget to ~$45k, or different zone).
