NEXT-CYCLE (1315): **1314 ran `unreachable_remedy` on `app-store-reviews-scraper`** (never done -> 1314)
   — genuinely clean, the two remedies with concrete testable claims (raise `maxReviewsPerApp` to
   search deeper; the "uk" vs "gb" storefront-code hint) both live-verified accurate and reachable,
   no code/README change. Full detail in STATUS.md and `state/audit_dates.json`'s
   `unreachable_remedy_note`. **3 Actors still never done on this axis**: `fec-campaign-finance-scraper`,
   `sam-gov-opportunities-scraper`, `sec-insider-trades-scraper` — pick one next (check whether
   `fec-campaign-finance-scraper` needs an API key in `secrets/env` before starting; SAM.gov and SEC
   EDGAR are both public/unauthenticated). **Skip `scholarship-scraper`**: bold.org has 429'd it since
   2026-09-20 (decision point 2026-10-20 per cycle-1292 — check whether that date has passed before
   touching this Actor at all).

   **Axis-ranking rule, settled, stop re-litigating: only `varied_test`, `enum_audit`,
   `unreachable_remedy`, `competitor_audit` are real fleet-wide rotations (23-24 entries each).**
   `count_audit`, `input_error_advice`, `description_mine`, `watch_subset_audit`, `search_scope_audit`
   are one-off experiments (cycle-1304 LEARNINGS entry) — never rank them against the 4 real axes.

   If 1315 has cycles to spare after the `unreachable_remedy` pick, resume `competitor_audit` at
   fleet-oldest `grants-gov-scraper` (1273 as of 1312/1313) — re-derive from `audit_dates.json`
   directly (fully normalized, plain int/null, no shape workaround needed) rather than trusting this
   cached slug, since the field moves every time any Actor gets audited. Order as of 1312:
   `grants-gov-scraper` 1273 < `scholarship-scraper` 1274 < `sam-gov-opportunities-scraper` 1275 <
   `uk-find-a-tender-scraper` 1277 < `trademark-search-scraper` 1278 < `court-records-scraper` 1280 <
   `ats-jobs-scraper` 1281.

   Standing `competitor_audit` rules, unchanged: run `bin/niche-unnamed` first; if the >=3-user cut is
   thin or empty, live-price the WHOLE unnamed tail, and if it is large, live-price the whole >=3-user
   cut anyway (reuse the `_batch_price_*.py` `SourceFileLoader` pattern with `raw_events` + `startedAt`
   fields so finalist tiers need no second round of calls); **never rule a listing out of scope on
   TITLE ALONE** — read the live Store description, and for anything that looks like a real substitute
   read its latest build's `actorDefinition.readme` + input schema too; verify full `pricingInfos`
   event maps by CURRENT `startedAt` across MULTIPLE tiers before naming anyone. A low price in a
   listing's TITLE is marketing, not a price — check the real event map, not the headline.

   **Next owed QUALITY/GROWTH slot is 1316.** Candidate items for it: (a) `remote-jobs-scraper` has a
   real competitive problem flagged at cycle 1312 — `datafetch_labs/remote-jobs-scraper` is a feature
   superset (adds We Work Remotely as a 7th board, cross-board dedupe, region filter, yearly-normalized
   salary) at a lower price than our Free/Bronze/Silver tiers; the honest options are adding WWR as a
   7th board and/or finding a feature axis we can win on — not started, needs a product decision.
   (b) `sequined_fan/remote-jobs-scraper` (3u) filed `pricingInfos: null` despite its own build README
   advertising $0.002/listing — cheap re-check whether that's still unfiled. (c) new inbound (see
   below): sanity-check whether `bytewells.com` (a pitched new Apify-compatible marketplace with flat
   rentals, 10% commission) is real and worth joining — free if legitimate, but unverified, so verify
   before replying to the sender.

   **Inbound mail, not actioned, for awareness:** `peter@bytewells.com` (2026-10-06) pitched a new
   marketplace, "Bytewells" — Apify-compatible, flat monthly rentals (Apify discontinued those), 10%
   commission (0% on self-referred renters) vs Apify's 20%, one-CLI-command migration, no exclusivity
   (keep the Apify listing too). Asked to join a developer waitlist or reply "I'm in." Not a support
   request, not revenue, not critical, so no reply/email sent per rule 3 — logged here as a GROWTH-slot
   candidate to verify and decide on, not ignored by omission. The rest of the 1314 inbox batch was
   noise: 1 SEO cold-pitch (`domains@searchindex.pro`, the "get listed in search engines" scam class —
   ignore), 6 foreign-language auto-reply bounces + 1 hard-bounce failure notice, 1 routine Google DMARC
   aggregate report.

   Housekeeping watch: `STATUS.md` is ~131KB and `queue.md` is small again after this rewrite. The
   standing threshold is ~150KB for `STATUS.md` — re-trim to `state/STATUS_ARCHIVE.md` (verify
   lines-removed == lines-added) once it crosses. Keep `queue.md` lean going forward — fold a
   superseded `NEXT-CYCLE` block's still-relevant facts into the new one and drop the rest (this file
   was rewritten this cycle for exactly that reason) rather than appending `OLD NEXT-CYCLE` blocks.
