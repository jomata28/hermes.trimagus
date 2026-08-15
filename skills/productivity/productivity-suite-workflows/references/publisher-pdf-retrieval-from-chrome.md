# Retrieving an open-access publisher PDF through persistent Chrome

Use this when a journal article is legally open access but direct `curl`, headless browser, Elsevier API, or `showPdf` requests receive 401/403/Cloudflare responses.

## Source validation first

1. Identify whether the user supplied the original research article, a commentary/editorial, protocol, correction, or supplement.
2. Capture DOI, PII, PMID, trial registration, and linked-article DOI before building a scientific deck.
3. For a commentary, retrieve the linked original trial and supplements. Do not imply that commentary details are the complete trial methods.
4. Cross-check ClinicalTrials.gov and the published protocol for prespecified measurements that the abstract/commentary may omit.

## Persistent headed-browser method

1. Open the article full-text page in the existing persistent Chromium profile. A normal headed session may pass publisher checks that direct requests do not.
2. Extract the real PDF and supplement links from page anchors. Lancet/Elsevier commonly exposes:
   - main article: `/action/showPdf?pii=...`
   - supplements: `/cms/<doi>/attachment/<uuid>/mmcN.pdf`
3. Navigate the same tab from the validated full-text page to each PDF URL so the correct browser session/referrer state is retained.
4. Chrome replaces a PDF navigation with its internal viewer at `chrome-extension://mhjfbmdgcfjbbpaeojofohoefgiehjai/index.html`. The downloadable PDF remains behind the viewer.
5. Find the viewer's nested shadow-DOM control `cr-icon-button#save[aria-label="Download"]` and click it.
6. In an attached CDP browser context, Playwright `download.saveAs()` can lose its temporary artifact. Set a durable download directory first through a browser CDP session:

```js
const bs = await browser.newBrowserCDPSession();
await bs.send('Browser.setDownloadBehavior', {
  behavior: 'allow',
  downloadPath: '/absolute/download/dir',
  eventsEnabled: true,
});
```

7. Wait until a non-`.crdownload` file appears, then copy/rename it to the final path.

## Shadow-DOM download button

```js
function all(root) {
  let out = [];
  for (const el of root.querySelectorAll('*')) {
    out.push(el);
    if (el.shadowRoot) out = out.concat(all(el.shadowRoot));
  }
  return out;
}
const button = all(document).find(
  el => el.id === 'save' && el.getAttribute?.('aria-label') === 'Download'
);
button.click();
```

Run this inside the Chrome PDF Viewer frame, not the publisher page.

## JAMA and PubMed Central variation

JAMA may expose the article HTML after a normal headed Chrome session passes Cloudflare while direct PDF requests still redirect or return 403.

1. Query Crossref by DOI and inspect `message.link`; the `content-version: vor` entry can reveal the exact JAMA `articlepdf/...pdf` URL even when the visible PDF control is JavaScript-only.
2. After Chrome opens the JAMA full-article page, enumerate anchors again. The page can expose:
   - the version-of-record `articlepdf` URL;
   - signed `cdn.jamanetwork.com` supplementary PDFs;
   - original figure/table image download URLs.
3. Signed supplement URLs often download successfully through Chrome even if the main PDF redirects back to the article. Use the durable CDP download directory pattern above and identify each supplement from its first page.
4. If the formatted main PDF remains unavailable but the complete article is present in PubMed Central, save the official PMC full text with `Page.printToPDF`, download the original PMC/JAMA figure assets, and label the result accurately as an official PMC full-text rendering rather than the publisher-formatted PDF.
5. Keep the DOI and JAMA article URL with the deliverable so the user can open the publisher version directly.

## Verification

Never trust MIME type alone. Chrome's viewer shell can be only a few hundred bytes of HTML while claiming `application/pdf`.

Verify each artifact with:

```bash
file article.pdf
pdfinfo article.pdf
pdftotext -layout article.pdf article.txt
```

Confirm title, authors, page count, and expected section text. Separately identify each supplement before reporting success.

## Scientific-deck consequence

Once the original article is available, re-check:
- exact randomisation and sample sizes;
- primary and secondary endpoints;
- laboratory/biological measurements and visit schedule;
- actual longitudinal results in main and supplementary tables;
- limitations and estimands.

If these differ materially from the commentary-based deck, tell the user the deck is incomplete and update the relevant slide rather than silently retaining the simplified interpretation.
