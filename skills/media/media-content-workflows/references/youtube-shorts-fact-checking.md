# YouTube Shorts Fact-Checking Fallback Workflow

Use when the user asks whether a claim in a YouTube Short/video is true, especially when transcript extraction is unavailable.

## Workflow

1. **Verify the video identity**
   - Use YouTube oEmbed when possible:
     - `https://www.youtube.com/oembed?url=<video_url>&format=json`
   - Capture title, channel/author, thumbnail, and URL.

2. **Extract public page context if needed**
   - Fetch the public page with a browser-like user agent.
   - Look for `ytInitialData` and extract visible title/description/structured description fields.
   - Do not treat recommendations, comments, or unrelated page text as the video's claim unless clearly tied to the video.

3. **Try transcript, but do not stall on it**
   - Try transcript tooling if available.
   - If unavailable/blocked, say so directly and continue with a limited verdict based on verified metadata/visible claim and external sources.

4. **Check the underlying claim against authoritative sources**
   - For platform/API/product claims, check official docs.
   - For medical/legal/financial claims, prefer primary regulators, official docs, peer-reviewed sources, or audited evidence.
   - For income/trading claims, distinguish between "the tooling is possible" and "the profit claim is proven."

5. **Return a short verdict**
   - Suggested shape:
     - `Short answer: partly true / true / false / unproven.`
     - `What is true:` bullets.
     - `What is overstated/unproven:` bullets.
     - `Verdict:` one sentence.

## Pitfalls

- Do not hallucinate transcript content when transcript retrieval fails.
- Do not equate "can build a bot/tool" with "can reliably make money."
- Do not over-index on viral hooks; require hard evidence for strong earnings/performance claims.
- Avoid long generic explanations when the user asks "is this true?" — give the verdict first, then concise support.
