# Mexico vehicle registration / ownership-transfer notes

Use when JT asks about post-purchase trámites, cambio de propietario, reemplacamiento, baja/alta de placas, or PDF handouts for a buyer in Mexico.

## Workflow lessons

1. **Separate the registration route before listing steps.** For a car with plates from one state and buyer domicile in another, do not assume the buyer should renew the current plates. First identify:
   - keep registration in current state → cambio de propietario + reemplacamiento in that state, usually with proof of domicile there;
   - register in buyer's state → alta de placas in buyer's state, plus baja/return/resolution of prior plates as required.

2. **For CDMX vs Edomex:** if the buyer lives in Tlalpan/Coapa and has CDMX proof of domicile, the likely route is CDMX alta de placas for a used vehicle, not “cambiar placas Edomex en CDMX.” Edomex reemplacamiento usually requires Edomex domicile.

3. **Do not include dealer/Kavak negotiation context in a procedural PDF unless the user asks.** If the user asks for a handout for another person, keep it to official steps, documents, portals, costs, and decision points.

4. **Do not include ISAVAU unless it is directly relevant or requested.** The user found it distracting for a simple steps handout. If needed, explain separately as a possible acquisition tax, not as a required core step.

5. **When asked for prices, do not modify the artifact yet.** Research and report costs first; wait for explicit approval before updating a PDF/guide.

## Cost anchors verified in-session

CDMX Finanzas Autos particulares (Clave 36):
- Baja (36_2): **$590**.
- Cambio de propietario / carrocería / motor / domicilio / corrección de datos (36_7): **$433**.
- Reposición o renovación de tarjeta de circulación (36_15): **$433**.
- Source path: `https://data.finanzas.cdmx.gob.mx/formato_lc/vehicular/36`.

CDMX SEMOVI alta foránea (used vehicle from another state):
- Official page: `https://www.semovi.cdmx.gob.mx/tramites-y-servicios/vehiculos-particulares/placas/alta-de-placas-vehiculos-usados/alta-de-placas-vehiculos-usados-de-otra-entidad-federativa-foraneos`.
- **$972.00** por derechos de alta.
- **$590.00** por baja de placas de otra entidad only if doing the digital Ventanilla de Control Vehicular route, lacking prior baja, and needing a baja FUM.
- Practical total: **$972** if baja is already resolved, or **$1,562** if alta + baja FUM applies. Capture a screenshot of the SEMOVI `Costo` accordion when the user asks for proof.

For CDMX cars already in the CDMX padrón, the line-capture forms for 36_2/36_7 can calculate from marca/modelo/placa. For an Edomex plate, the CDMX form may return “datos no se encuentran actualizados en el padrón,” which is expected and indicates this is an **alta from another entity**, not a simple CDMX cambio-propietario calculation.

Edomex reemplacamiento 2026 public page confirms:
- Vehicles with plates issued in 2021 must reemplacar in 2026.
- Program: **1 Apr–31 Aug 2026**.
- Plate endings 9/0: **August**.
- Reemplacamiento steps: requisitos → capture info → pay → appointment/collect plates.
- Source path: `https://pagosytramites.edomex.gob.mx/recaudacion/CtrlVeh/MicRemplaca/index.jsp`.

## PDF/artifact QA lesson

When generating a PDF via headless Chromium from a local HTML file, avoid `file://` with Snap Chromium because it can render an “ERR_FILE_NOT_FOUND” page. Serve the HTML via localhost and print from `http://127.0.0.1:<port>/file.html`, then verify with `pdfinfo` and `pdftotext` before sending. Kill the temporary HTTP server afterward.
