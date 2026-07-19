# Mexico used/semi-new vehicle purchase due diligence

Use when JT asks whether to buy a used/semi-new car in Mexico, including listings from Kavak/agencies or private sellers.

## Goal

Move from listing/photos to a clear `buy / negotiate / avoid / need more info` recommendation grounded in visible evidence, public checks, market comparables, and required documents.

## Intake checklist

Ask for or extract from screenshots/photos:

- Make/model/body style/color and visible plates/state.
- Listing link or seller platform (Kavak, agency, Marketplace, private).
- Year, trim/version, transmission, mileage, price, location.
- Full 17-character VIN/NIV; if OCR yields 16 characters or invalid check digit, say it is incomplete and request a clearer source.
- Photos: all sides, interior, odometer, dashboard on, engine bay, trunk floor, tires, VIN tags, invoice/card with sensitive fields redacted.

## Public checks to run

1. **REPUVE / theft status** — query plate and VIN/NIV. CAPTCHA may require the user to do it on phone; give exact fields and acceptable result: `Sin reporte de robo`.
2. **State fiscal status** — for Edomex use the official Portal de Servicios al Contribuyente:
   - Tenencia/refrendo: `https://sfpya.edomexico.gob.mx/controlv/tenencia/`
   - Portal root: `https://sfpya.edomexico.gob.mx/recaudacion/`
   - Enter plate uppercase and without hyphens first, e.g. `NCW769C`. Hyphenated/lowercase variants may return empty records.
   - The first result may only show a vehicle record/ficha (model year, make/model/trim, factura date/amount, clave vehicular, cylinders), not the final adeudo amount. Tell user to continue in browser through Guardar/Validar/Generar formato or require seller/Kavak official no-adeudo proof.
   - If a plate lookup returns the wrong vehicle, first suspect OCR/transcription (`H/W`, `O/0`, hyphens) before declaring a documentary red flag.
3. **Multas/infracciones** — start from `https://sfpya.edomexico.gob.mx/recaudacion/`. Internal Edomex route observed: `/ingresos/ControlObl/RedirVG?fw=../faces/ControlObl/Multas/Inicio.xhtml&bn=MultaBean&P=2`. Seller/Kavak should clear and prove zero balance before delivery.
4. **Verificación** — confirm hologram, semester/year, and whether it will need immediate renewal. If Kavak says they cover it, get that in writing.
5. **Reemplacamiento / plate renewal** — for Edomex, use `https://pagosytramites.edomex.gob.mx/recaudacion/CtrlVeh/MicRemplaca/index.jsp` when available. 2026 rules observed:
   - Plates generally have 5-year validity from expedition.
   - 2026 program applies to service-particular vehicles with plates issued in 2021, plus 2020-or-earlier plates that did not renew in 2025.
   - Calendar by final plate digit: 1/2 April, 3/4 May, 5/6 June, 7/8 July, 9/0 August.
   - September–December 2021 plates keep the validity shown on the circulation card and renew within 15 business days after expiry, or can renew early during the program.
   - Non-renewal consequences include traffic/administrative sanctions, possible plate removal/impoundment, 20 UMA sanction, and inability to verify.
6. **Recalls/campaigns** — decode VIN (or candidate VIN) and check recalls. NHTSA APIs can be useful for Mazda2-like vehicles:
   - Decode: `https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/<VIN>?format=json`
   - Recalls: `https://api.nhtsa.gov/recalls/recallsByVehicle?make=<MAKE>&model=<MODEL>&modelYear=<YEAR>`
   - For Mazda2 2019–2020, check fuel pump recall; Mazda2 2020–2021, check headlight adjustment cap recall. Mexico units still need confirmation with Mazda/Kavak by VIN.
7. **Market comps** — check Kavak, Autocosmos, Seminuevos, MercadoLibre if accessible. If a site blocks scraping, report that and use accessible alternatives/APIs/manual-user screenshot.

## Kavak-specific framing

Kavak reduces private-party fraud risk but does **not** eliminate overpricing, mediocre reconditioning, financing add-ons, paid warranty/coverage pressure, pending recalls, or warranty exclusions.

For Kavak, require:

- Exact listing URL and price contado vs financed total.
- VIN/NIV exactly as shown in listing/docs.
- Inspection report and warranty/devolution terms in writing.
- Confirmation of no adeudos, REPUVE clean, verification status, and pending recalls/campaigns.
- A test-drive/return-window plan: inspect hard during the return period and document issues immediately.

If Kavak's included guarantee is only a short return/coverage window (e.g. 7 days) and mechanical coverages cost extra, treat coverage as part of the **real price**, not as a cosmetic add-on.

## Cost stacking / negotiation estimates

Always compute total real cost: sticker price + coverage + owner change + plates + verification + immediate service/tires/brakes.

Working Edomex/Kavak planning ranges (verify live when possible):

- Verification: roughly MXN $700–$1,200.
- Reemplacamiento/cambio de placas: roughly MXN $1,100–$1,800+.
- Cambio de propietario/gestoría: roughly MXN $800–$2,500; agency/Kavak gestoría can be higher.
- Owner change + reemplacamiento if verification is covered: budget roughly MXN $1,900–$4,300; often about $3k–$4k.

When sticker price is fixed, negotiate risk transfer or value:

- Mechanical coverage/extended warranty included or discounted.
- Verification included.
- No adeudos: tenencia/refrendo/multas/infracciones by official proof.
- Cambio de propietario / gestoría included or bonified.
- Reemplacamiento included/bonified if due soon.
- Recall/campaign confirmation and remedy.
- Service pre-delivery documented: oil, filters, brakes, battery health, scanner.

Useful Chris Voss / *Never Split the Difference* phrasing:

- Label: “Parece que el precio está bloqueado por sistema.”
- No-oriented question: “¿Sería una locura pedir que incluyan la cobertura/cambio de propietario si el precio no se mueve?”
- Calibrated question: “¿Cómo se supone que justifique pagar precio alto si además absorbo trámites y riesgo mecánico?”
- Walk-away: “Me gusta el coche, pero sin ajuste ni beneficios prefiero esperar otra unidad.”

## Mechanical/body checks

- Transmission: no delayed reverse, slip, hard shifts, or warning lights.
- Cold start: no rattles, smoke, rough idle, fuel smell.
- OBD scan: no active/pending codes; readiness monitors reasonable.
- AC, electronics, sensors/camera, locks/windows.
- Suspension/brakes: no clunks, pulls, pulsation.
- Body: panel gaps, moved bolts, paint mismatch, trunk floor/longitudinals, water stains, mismatched glass, overspray.
- Tires: brand/date/tread evenness; uneven wear suggests alignment/suspension/impact.

## Output format

Give a concise Spanish/Spanglish decision memo:

1. **Veredicto rápido** — buy/negotiate/avoid/need info.
2. **Facts visible/extracted** — separate from assumptions.
3. **Online checks completed + blocked checks** — include source/tool limitations honestly.
4. **Price benchmark** — compare to comps by year/km/trim.
5. **Red flags / green flags**.
6. **Exact next asks to seller/Kavak** — VIN, price, km, trim, docs.
7. **Final rule** — conditions under which to buy.

## Pitfalls

- Do not give a green light from photos alone; VIN, price, mileage, docs, and public checks are required.
- Do not treat a 16-character OCR VIN as valid. A VIN/NIV should be 17 characters. VIN check-digit calculation can suggest a missing character, but final confirmation must come from seller/docs.
- Do not assume Kavak means fair price or no defects. It changes the risk profile, not the due-diligence burden.
- Do not rely on one marketplace if bot-blocked; state the block and use accessible sources.
- Redact personal/sensitive document data in summaries.
