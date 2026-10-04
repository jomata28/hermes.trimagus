# Bee → personal system digestion

Process complete recent days first, then move backward in bounded conversation batches. Use `bee conversations list --limit N --cursor CURSOR --json`, `conversations get ID --json` for full transcriptions, and `activity --limit N --json` for notes/todos. Save source JSON and checkpoint locally before reasoning; do not treat a summary as full-transcript review.

Read all existing Google Tasks lists with pagination before writing. Deduplicate using Bee IDs AND meaning; preserve original notes and enrich the existing task rather than create parallel tasks. Date-only Tasks due fields do not schedule timed Calendar blocks.

Separate JT speech/commitments from requests, other people's obligations, media/tutorial audio, assistant output heard by the wearable, and ambiguous Unknown speakers. A CAPTURING conversation needs later re-read even after a provisional digest. Tutorial examples (clients, email drafts, times) are not JT's commitments. Medical discussion is context to verify, not a recommendation or medication instruction.

Route confirmed actions to Tasks, agreed timed commitments to Calendar, context/decisions/ideas to a Drive-native Bitácora synthesis. Default to a digest under the actual existing Admin/Reviews tree, preserving source IDs, dates, original uncertain tokens, and project/area links. Do not dump full sensitive transcripts into Drive by default; retain local read-only source snapshot.

Discover the real Drive root/folder using API metadata/listing if an injected root ID returns 404; never silently normalize the identifier. The verified bitacora root in this environment ends in Gq, not Gg. Use direct Drive writes and read back each exact file and Tasks write before claiming success. Do not use a local vault mirror as canonical state.

Each checkpoint records fetched IDs, fully reviewed IDs, open conversations, exact backward cursor, destinations/remote IDs, verification state, open questions, and incomplete day boundary. Save one checkpoint per batch. No daemon/cron/recurring execution claim unless explicitly configured. Present 3–5 high-value questions at a time, and distinguish first batch complete from whole history complete.
