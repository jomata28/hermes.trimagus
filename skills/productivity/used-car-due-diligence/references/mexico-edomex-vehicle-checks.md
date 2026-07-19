# Mexico/Edomex vehicle checks — session notes

Use these notes when evaluating a Mexico/Estado de México used-car purchase.

## Edomex tenencia/refrendo official portal

Official entry used successfully:

- `https://sfpya.edomexico.gob.mx/controlv/tenencia/`

Flow:

1. Enter plate with **no hyphens** and **uppercase**.
   - Example correct format: `NCW769C`
   - Hyphenated input may return blank/model 0.
   - Lowercase input may also fail.
2. Submit `placa` to the form action under `/controlv/tenencia/calcula;jsessionid=...`.
3. The first result may only show the vehicle identity, not the final payment/adeudo screen.
4. If the portal only shows identity, ask the dealer/seller for official proof of no adeudo / paid tenencia-refrendo for the current year.

Successful identity output example from session:

- Plate: `NCW769C`
- Modelo: `2021`
- Vehículo: `MAZDA MAZDA2 4PTAS (NAC) T/A i TOURING SKYACTIV 6AT TELA ELECTRICO 1.5L 4C`
- Fecha factura: `22/05/2021`
- Importe factura: `$333,900 MXN`

Pitfall encountered:

- Blurry photo OCR read `NCH769C`, which returned a **Dodge Stratus 2002**. User corrected plate to `NCW769C`; official portal then matched Mazda2 2021. Always test plausible visual confusions before calling it a fatal mismatch.

## VIN/NIV handling

- Mexico vehicle labels may be hard to OCR. VIN/NIV must be 17 characters.
- If one character is missing but the rest is legible, calculate/check digit to propose a candidate, but label it as **probable**, not confirmed.
- In session, partial `3MDDJBT0MM408098` was 16 chars; VIN check digit suggested probable `3MDDJBT05MM408098`, which decoded as Mazda2 2021 via NHTSA/vPIC.
- Still require seller/dealer to confirm the exact VIN/NIV in writing and match it against documents.

## Recalls/campaigns pattern

NHTSA endpoints used:

- Decode VIN: `https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/<VIN>?format=json`
- Recalls by vehicle: `https://api.nhtsa.gov/recalls/recallsByVehicle?make=MAZDA&model=MAZDA2&modelYear=2021`

For Mazda2 2021, NHTSA showed:

- Campaign `22V885000` / Mazda `5622K`
- Component: exterior lighting/headlights
- Issue: missing headlight adjustment prevention caps / possible improper adjustment
- Remedy: dealer installs caps/checks free of charge

Ask dealer: “Does this VIN have pending Mazda campaigns/recalls, especially 5622K, and can you provide proof it was completed or will be handled?”

## Kavak notes

- Kavak may block server-side scraping with CloudFront 403; if so, ask JT for listing screenshots (price, km, VIN/NIV, warranty, return terms).
- Kavak lowers private-party fraud risk, but still verify: REPUVE, tenencia/refrendo, multas/infracciones, verificación, VIN match, warranty/return policy, and recalls.
- Treat platform premium as convenience/guarantee cost; price still needs market comparison.

## Price reasoning example from session

Vehicle: Mazda 2 1.5 i Touring Sedan Auto 2021, 40,000 km, Kavak, price `$248,000 MXN`.

- Original invoice shown by Edomex: `$333,900 MXN`.
- Depreciation at `$248,000`: about `25.7%` from invoice.
- 40,000 km over ~5.16 years ≈ `7,759 km/year`, low/moderate.
- Recommendation given: viable but negotiate; target about `$238k–$242k`; `$248k` is reasonable but not a bargain.

## Message template to dealer/platform

```text
Me interesa el vehículo, pero antes de avanzar necesito:

1. VIN/NIV completo de 17 caracteres.
2. REPUVE limpio.
3. Constancia oficial de no adeudo de tenencia/refrendo/multas.
4. Verificación vigente o estado actual.
5. Confirmación de campañas/recalls de marca pendientes y si ya fueron atendidas.
6. Garantía y política de devolución por escrito.

También quisiera saber si pueden mejorar el precio o incluir algún beneficio, porque mi objetivo de cierre está más cerca de $___ MXN.
```
