# Human-login browser handoff and authenticated extraction

Use this when public/headless access is blocked but the user can authenticate in the VPS noVNC browser.

## Pattern

1. Start the persistent VPS desktop and launch Chromium with a dedicated persistent profile.
2. Let the user complete login/CAPTCHA themselves; never request or type their account password.
3. Verify the logged-in page visually before automation.
4. Relaunch the same profile with a loopback-only CDP port when structured extraction is needed:
   ```bash
   DISPLAY=:99 chromium --no-sandbox --disable-dev-shm-usage --start-maximized \
     --remote-debugging-port=9223 \
     --user-data-dir=/root/.vps-screen/<task-profile> '<url>'
   ```
5. Verify CDP readiness at `http://127.0.0.1:9223/json/version` and attach an automation client with `connectOverCDP` rather than opening a fresh unauthenticated browser.
6. Keep the CDP port loopback-only. Reuse cookies only for the requested task and do not extract session secrets.

## Marketplace/search-site lessons

- Search terms do not override a geographic radius. Confirm and explicitly move the map/search center to the target locality before judging inventory.
- If a location widget accepts only localities/postal codes, use the nearest recognized locality rather than a landmark name.
- Apply hard structured filters (price, bedrooms, whole unit) first, then run separate short queries for neighborhood and furnishing terms.
- Extract unique individual listing URLs, open each detail page, and verify the description. Search cards often omit or misrepresent furnishing.
- Treat `cocina equipada` as appliances/cabinetry, **not** proof that the dwelling is furnished.
- Reject `no amueblado`, `sin muebles`, staged/reference photos, `2 recámaras + estudio`, rooms, placeholder prices, and cross-posted duplicates unless the user's requirements allow them.
- A query returning the same results across multiple neighborhood terms often indicates the map center/radius is wrong, not that inventory is absent.

## Verification

For each promoted listing record direct URL, current price, true bedroom count, explicit furnishing evidence, maintenance/total cost, locality, and checked date. Label details that still require advertiser confirmation.