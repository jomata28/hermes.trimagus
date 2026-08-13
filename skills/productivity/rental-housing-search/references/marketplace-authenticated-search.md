# Authenticated Marketplace Search Pattern

Use when public Marketplace results are login-walled or geographically wrong.

## Workflow

1. Start the persistent noVNC desktop and let the user perform website login/2FA themselves.
2. Confirm authentication with a screenshot before proceeding.
3. Launch Chromium with a dedicated persistent profile and a remote-debugging port if programmatic extraction is needed.
4. Connect through CDP/Playwright to the already-authenticated browser; never copy cookies or ask for account credentials.
5. In Marketplace, open the location dialog and select the target municipality/neighborhood. Verify the displayed radius. Keywords alone do not override an incorrectly centered map.
6. Apply min/max price and bedroom filters, then run multiple short queries by neighborhood/synonym.
7. Extract and normalize `/marketplace/item/<id>/` URLs; strip tracking parameters and deduplicate by item ID.
8. Open candidate pages one at a time and inspect full description for bedroom structure, furniture inclusion/negation, maintenance, and exact area.
9. Reject implausible placeholder prices (`$1`, `$9`, etc.), rooms instead of entire units, duplicate broker copies, and ads whose text contradicts filters/photos.

## High-value pitfalls

- Marketplace can repeat the same citywide results for every query when the location remains centered elsewhere.
- Search terms like “amueblado” often return unfurnished listings; inspect descriptions for `no amueblado` and `sin muebles`.
- “Cocina equipada” generally means cabinetry/appliances, not furnished bedrooms or living areas.
- Photos can be referential or AI-staged. Treat explicit text as authoritative unless the advertiser confirms otherwise.
- A listing with “2 recámaras, 1 estudio o 3 recámaras” is not a verified three-bedroom unit until the study’s door, window, privacy, and bed setup are confirmed.
- Do not message sellers automatically without explicit authorization; produce links and a copy-ready inquiry first.
