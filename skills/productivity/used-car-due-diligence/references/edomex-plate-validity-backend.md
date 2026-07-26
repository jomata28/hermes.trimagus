# Edomex plate validity / tenencia backend check

Use for JT's Edomex-plated vehicle checks when he asks whether plates are current, when they expire, or whether there are adeudos.

## Known pattern

The public Tenencia Individual UI is Vue-based and asks for plate + reCAPTCHA in the browser, but the backend endpoint observed in-session accepted a POST with plate only and returned vehicle/payment/plate-validity JSON.

Base page:

```text
https://tenencia.edomex.gob.mx/
```

Current app URL shape observed:

```text
https://tenencia.edomex.gob.mx/TenenciaIndividual/tenencia/A06E1A88B8A6ED4B/
```

Backend endpoint:

```text
POST https://tenencia.edomex.gob.mx/TenenciaIndividual/tenencia/calculaTenencia
form field: placa=<PLATE_WITHOUT_HYPHENS_UPPERCASE>
```

## Minimal probe

```python
import requests, json

plate = "NCW769C"  # uppercase, no hyphens
base = "https://tenencia.edomex.gob.mx"
url = base + "/TenenciaIndividual/tenencia/A06E1A88B8A6ED4B/"
headers = {"User-Agent": "Mozilla/5.0", "Referer": url}

s = requests.Session()
s.get(url, headers=headers, timeout=30)
r = s.post(base + "/TenenciaIndividual/tenencia/calculaTenencia",
           headers=headers, data={"placa": plate}, timeout=60)
data = r.json()
tenencia = json.loads(data["tenencia"]) if isinstance(data.get("tenencia"), str) else data.get("tenencia")

print(data.get("numError"))
print(tenencia.get("descAdeudos"))
print(tenencia.get("fechaInicioVigenciaFormat"))
print(tenencia.get("fechaFinVigenciaFormat"))
```

## Fields to report

Prefer reporting a small table:

- `placa`
- `modeloVehi`
- `vehiculo`
- `descAdeudos`
- `ultPago`
- `total`
- `fechaInicioVigenciaFormat`
- `fechaFinVigenciaFormat`
- `placaBloqueada`
- `adeudosAnteriores`

Avoid exposing personal fields returned by the portal unless the user explicitly needs them: RFC, CURP, full VIN/series. If vehicle identity matters, only report enough to verify match (make/model/year and maybe masked VIN).

## Session-observed example

For JT's known Edomex plate `NCW769C`, the portal returned:

- vehicle: Mazda 2, model 2021
- adeudos: `SIN ADEUDOS`
- último pago: `26` / 2026
- total: `0`
- plate validity start: `19/01/2026`
- plate validity end: `19/01/2031`

Do not treat this example as current proof in future sessions; re-query the official portal when the user asks for current status.
