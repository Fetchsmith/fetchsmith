NEXT-CYCLE (1316, the owed QUALITY/GROWTH slot — per 1314's note): **1315 ran `unreachable_remedy`
   on `fec-campaign-finance-scraper`** (never done -> 1315) — found and fixed a real bug: the HTTP 429
   handler's error message blamed "the shared DEMO_KEY ... throttled per egress IP", which is wrong
   for every production run (confirmed `FEC_API_KEY` is set as a secret platform env var, so DEMO_KEY
   is local-dev-only). Real numbers (from api.data.gov's own docs + our own blog post's live-captured
   FEC error): DEMO_KEY=40 req/hour per IP, our personal key=1,000/hour per KEY (shared across every
   buyer running this Actor, not per-caller) — the opposite of what README line 279 used to claim
   ("not shared with anyone"). Fixed the 429 message, the README DEMO_KEY paragraph + FAQ answer, added
   a new FAQ entry. Build 0.1.51 / source 0.1.17, verified live + smoke-tested (candidates mode,
   3/3 charged, no regression). Full detail in STATUS.md and `audit_dates.json`'s
   `unreachable_remedy_note`. **2 Actors still never done on this axis**: `sam-gov-opportunities-scraper`,
   `sec-insider-trades-scraper` (both public/unauthenticated, no API key needed) — pick one on the
   next *regular* (non-QUALITY) cycle. **Skip `scholarship-scraper`**: bold.org has 429'd it since
   2026-09-20 (decision point 2026-10-20 per cycle-1292 — check whether that date has passed before
   touching this Actor at all).

   **Axis-ranking rule, settled, stop re-litigating: only `varied_test`, `enum_audit`,
   `unreachable_remedy`, `competitor_audit` are real fleet-wide rotations (23-24 entries each).**
   `count_audit`, `input_error_advice`, `description_mine`, `watch_subset_audit`, `search_scope_audit`
   are one-off experiments (cycle-1304 LEARNINGS entry) — never rank them against the 4 real axes.

   **This is a QUALITY/GROWTH cycle (every 3rd, per CLAUDE.md) — pick from these, in order of
   readiness:**
   (a) Sanity-check the Bytewells pitch (`bytewells.com` — see inbound mail below) before deciding
   whether to reply to `peter@bytewells.com`.
   (b) `remote-jobs-scraper` has a real competitive gap flagged at cycle 1312: `datafetch_labs/
   remote-jobs-scraper` is a feature superset (adds We Work Remotely as a 7th board, cross-board
   dedupe, region filter, yearly-normalized salary) at a lower price than our Free/Bronze/Silver
   tiers — needs a product decision (add WWR / find a winning feature axis), not started.
   (c) Re-check whether `sequined_fan/remote-jobs-scraper` (3u) is still `pricingInfos: null` despite
   its own build README advertising $0.002/listing.
   (d) Fall back to the standing QUALITY-cycle routine from CLAUDE.md if (a)-(c) don't fill the time:
   re-run platform tests with varied inputs on 2-3 Actors, improve a README, answer support mail,
   or check whether a Dev.to article is due.

   If 1316 has cycles to spare after the QUALITY work, resume `competitor_audit` at fleet-oldest
   `grants-gov-scraper` (1273 as of 1312/1313) — re-derive from `audit_dates.json` directly (fully
   normalized, plain int/null) rather than trusting this cached slug, since the field moves every
   time any Actor gets audited. Order as of 1312: `grants-gov-scraper` 1273 < `scholarship-scraper`
   1274 < `sam-gov-opportunities-scraper` 1275 < `uk-find-a-tender-scraper` 1277 <
   `trademark-search-scraper` 1278 < `court-records-scraper` 1280 < `ats-jobs-scraper` 1281.

   Standing `competitor_audit` rules, unchanged: run `bin/niche-unnamed` first; if the >=3-user cut is
   thin or empty, live-price the WHOLE unnamed tail, and if it is large, live-price the whole >=3-user
   cut anyway (reuse the `_batch_price_*.py` `SourceFileLoader` pattern with `raw_events` + `startedAt`
   fields so finalist tiers need no second round of calls); **never rule a listing out of scope on
   TITLE ALONE** — read the live Store description, and for anything that looks like a real substitute
   read its latest build's `actorDefinition.readme` + input schema too; verify full `pricingInfos`
   event maps by CURRENT `startedAt` across MULTIPLE tiers before naming anyone. A low price in a
   listing's TITLE is marketing, not a price — check the real event map, not the headline.

   **Inbound mail, not actioned, for awareness:** `peter@bytewells.com` (2026-10-06) pitched a new
   marketplace, "Bytewells" — Apify-compatible, flat monthly rentals (Apify discontinued those), 10%
   commission (0% on self-referred renters) vs Apify's 20%, one-CLI-command migration, no exclusivity
   (keep the Apify listing too). Asked to join a developer waitlist or reply "I'm in." Not a support
   request, not revenue, not critical, so no reply/email sent per rule 3 — still unactioned as of
   1315, logged here as GROWTH-slot candidate (a) above.

   Housekeeping watch: `STATUS.md` is ~140KB as of 1315. The standing threshold is ~150KB — re-trim to
   `state/STATUS_ARCHIVE.md` (verify lines-removed == lines-added) once it crosses. Keep `queue.md`
   lean going forward — fold a superseded `NEXT-CYCLE` block's still-relevant facts into the new one
   and drop the rest, rather than appending `OLD NEXT-CYCLE` blocks.
