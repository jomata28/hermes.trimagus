# YouTube-to-Business Planning Pattern

Use when the user gives a YouTube/video link and asks to turn it into a business, offer, or execution plan.

## Retrieval order

1. Try transcript retrieval first.
2. If YouTube blocks automated access, do **not** invent transcript details.
3. Verify video metadata via accessible sources such as YouTube oEmbed:
   - title
   - author/channel
   - thumbnail
   - canonical video ID
4. Try lightweight market/category search if current competitive context matters.
5. State the retrieval limitation in the final output and separate verified facts from synthesis.

## Planning output shape

Prefer a practical business plan over a generic video summary:

- Source interpretation and what was verified
- Best-fit business wedge for the user
- One-sentence offer
- ICP and buyer
- Pain points
- Positioning language
- MVP feature set
- Pricing
- Demo/script flow
- Landing page structure
- Sales motion/outbound scripts
- Delivery SOP
- Risks and mitigations
- 30-day execution plan
- Success metrics
- Next decisions

## User-context leverage

If the user already has relevant assets (domain, scraped leads, existing project, audience, vault/project folder), explicitly use them in the business design. The highest-value plan connects the video's idea to the user's unfair advantages instead of proposing a generic clone.

## Persistence

If the plan is likely durable, save it to the user's project workspace/vault as a dated Markdown plan and return the exact path. Keep raw video details and assumptions in frontmatter or a short source section.

## Pitfalls

- Do not claim you watched/read the full video when transcript retrieval failed.
- Do not stop at “this could be a business”; produce an offer and launch sequence.
- Do not overbuild the first version; define the narrowest revenue test.
- Do not sell “AI automation” abstractly; translate it into recovered revenue, time saved, or booked appointments for a specific niche.
