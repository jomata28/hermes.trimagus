# Secure dashboard embedding in an existing web application

Use this reference when integrating a sensitive operational dashboard into another authenticated or single-user web app while preserving the dashboard's own security boundary.

## Discovery before implementation

1. Read the host application's architecture, data model, repository rules, deployment path, and service-worker strategy.
2. Inspect the dashboard's bind address, reverse proxy, authentication, anti-DNS-rebinding behavior, and public route.
3. Test framing policy with an authenticated **GET**, not only `HEAD`. Some dashboards return `405` to `HEAD`. Inspect `X-Frame-Options` and CSP `frame-ancestors` from the real GET response.
4. Confirm the dashboard route itself works through TLS and authentication before changing the host app.

## Safe integration pattern

- Keep the sensitive dashboard loopback-bound when possible.
- Preserve edge authentication. Never disable Host validation or anti-DNS-rebinding just to make embedding easy.
- If a dedicated reverse-proxy route needs a downstream Host rewrite, scope it to that router only and rewrite to the loopback host Hermes expects. Do not weaken global validation.
- Store only an HTTPS dashboard URL and descriptive metadata in the host app's data layer. Never commit Basic Auth credentials, API keys, cookies, or a URL containing userinfo.
- Add a dedicated host-app view rather than a visually unrelated raw link.
- Make iframe loading explicit. Start with `src="about:blank"` plus a data attribute, then assign the real URL only after the user clicks. This avoids an authentication prompt during normal app boot and avoids loading a privileged surface unintentionally.
- Provide a `target="_blank" rel="noopener noreferrer"` full-screen fallback. Basic Auth may need to be completed in a top-level tab before the browser will show the authenticated dashboard inside a cross-origin iframe.
- Give the iframe an accessible title. Keep the host UI honest about authentication and do not claim the embedded content loaded merely because the iframe element exists.

## PWA considerations

- Bump the service-worker cache version whenever navigation or shell HTML changes, otherwise installed PWAs may retain the old navigation indefinitely.
- Do not cache cross-origin privileged dashboard responses in the host app's service worker.
- Preserve any special small-screen surface. A dashboard-management view should not displace a glanceable phone-cover or kiosk view.

## Tests

Write a DOM-level regression test before implementation that verifies:

- The new navigation destination exists and renders.
- The HTTPS URL comes from the declared data source.
- URL username and password are empty.
- The iframe begins blank and does not auto-load.
- The explicit control assigns the declared URL.
- The iframe has an accessible title.
- A full-screen link uses the same declared URL.

Treat `IFRAME` like `IMG` in generic empty-leaf scanners when it has an accessible title. Do not weaken unrelated accessibility checks.

## Verification

1. Run the existing full test suite and diff checks.
2. Confirm the live host app serves the new navigation and data.
3. Use browser automation to click the host-app control and inspect the actual iframe `src`, visibility, dimensions, button state, and console errors.
4. Verify the dashboard public route separately with valid authentication.
5. Capture desktop and phone-sized screenshots. Check overflow, bottom-navigation collisions, touch target size, and whether the embedded view still feels native to the host application.
6. Commit only after the live path and responsive layouts are verified.

## Reporting language

Distinguish these claims:

- **Verified host integration:** the view renders, the button assigns the correct URL, the frame is visible, and no host-app JavaScript error occurs.
- **Verified authenticated dashboard:** the dashboard HTML, assets, and API return success through the secured route.
- **User login still required:** the user's browser may need a first top-level authentication before cross-origin embedding displays content.
