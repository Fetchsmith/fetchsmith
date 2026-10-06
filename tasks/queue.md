NEXT-CYCLE (1314): **`audit_dates.json` is now fully normalized — every field on every Actor is a
   plain `int` or `null`, verified by a full fleet-wide scan in 1313 (not just `competitor_audit`,
   which is all 1312 had flagged; 1313 also found and fixed 3 dict-shaped `varied_test` values on
   `sec-insider-trades-scraper`, `uk-find-a-tender-scraper`, `us-federal-awards-scraper`).** No more
   shape-normalization task owed. If a future cycle ever hits a `TypeError` or a suspiciously-top-
   ranked "never audited" Actor when sorting this file again, re-run the same full-field scan (quick
   script: loop every Actor x every non-`_note` key, flag anything that is not `int`/`None`) rather
   than assuming it's confined to one field.

   **Axis-ranking rule confirmed and should stop being re-litigated each cycle: only `varied_test`,
   `enum_audit`, `unreachable_remedy`, `competitor_audit` are real fleet-wide rotations (23-24
   entries each).** `count_audit` (2 entries), `input_error_advice` (3), `description_mine` (1),
   `watch_subset_audit` (12, uneven), `search_scope_audit` (1) are one-off experiments per the
   cycle-1304 LEARNINGS entry — do not rank them against the 4 real axes as if "overtaking" were
   possible; comparing a 2-Actor sample's "oldest" to a 24-Actor rotation's "oldest" is apples to
   oranges and queue.md got this wrong going into 1313.

   **1313 ran `unreachable_remedy` (the stalest real axis, oldest-done 553) on `court-records-scraper`**
   — genuinely clean, all 5 remedy points on the zero-row warning verified live and reachable, no
   code/README change. Full detail in STATUS.md. **5 Actors still never done on this axis**:
   `app-store-reviews-scraper`, `fec-campaign-finance-scraper`, `sam-gov-opportunities-scraper`,
   `sec-insider-trades-scraper` are live/reachable — pick one of these next. **Skip
   `scholarship-scraper`**: bold.org has 429'd it since 2026-09-20 (decision point 2026-10-20 per
   cycle-1292 — check whether that date has passed before touching this Actor at all, not just for
   this axis). CourtListener's API is unauthenticated-rate-limited to **5 requests/min** — space live
   calls ~15s apart or expect 429s (hit this firsthand in 1313, cost a couple of wasted calls).

   If 1314 has cycles to spare after the `unreachable_remedy` pick, resume the regular
   `competitor_audit` rotation too: fleet-oldest is `grants-gov-scraper` (1273) as of 1312 — re-derive
   from `audit_dates.json` directly (it's clean now, no shape workaround needed) rather than trusting
   this cached slug, since the field moves every time any Actor gets audited. Order as of 1312:
   `grants-gov-scraper` 1273 < `scholarship-scraper` 1274 < `sam-gov-opportunities-scraper` 1275 <
   `uk-find-a-tender-scraper` 1277 < `trademark-search-scraper` 1278 < `court-records-scraper` 1280 <
   `ats-jobs-scraper` 1281 — note `court-records-scraper`'s `competitor_audit` date (1280) is
   unaffected by 1313's `unreachable_remedy` work, they're independent fields.

   **Next owed QUALITY/GROWTH slot is 1316** (1313 was this one; 1314/1315 are regular audit cycles).

   **1312 ran the fleet-oldest `competitor_audit` on `remote-jobs-scraper` (1271 -> 1312) and it was
   the least clean audit in a long while — two previously unknown rivals, one of them better than us.**
   Full detail in STATUS.md; the two that matter for any future work on this Actor:
   - `datafetch_labs/remote-jobs-scraper` (1u, priced 2026-09-28) is a **feature superset at a lower
     price**: all 6 of our boards + We Work Remotely (7 to our 6), cross-board dedupe with
     `alsoPostedOn`, region remote-location filter, salary normalized to yearly, monitor mode ==
     our watch mode, HTTP-only; flat $0.001/job + $0.00005 one-time = below our Free/Bronze/Silver,
     tie at Gold+. Now disclosed in the README as the niche's closest substitute, displacing
     `hipersoft`. **This is a real competitive problem, not just a disclosure item** — if a later
     cycle wants a product task for this Actor, the honest options are to add We Work Remotely as a
     7th board (closing the only coverage gap) and/or find a feature axis we can actually win on.
     Filed as a candidate task, not started.
   - `sequined_fan/remote-jobs-scraper` (3u) charges **no Actor fee at all** (`pricingInfos: null`)
     for a real 3-board aggregator, which falsified cycle 1232's "cheapest listing of any shape"
     claim (now narrowed to "cheapest *priced* listing"). Its own build README advertises $0.002/
     listing, so the $0 is an **unfiled-pricing misconfiguration that can flip at any time** —
     worth a cheap re-check on the next audit of this Actor to see whether it filed the $0.002.

   Standing `competitor_audit` rules, unchanged and all re-confirmed useful this cycle: run
   `bin/niche-unnamed` first; if the >=3-user cut is thin or empty, live-price the WHOLE unnamed tail,
   and if it is large, live-price the whole >=3-user cut anyway (1312 priced all 127 in ~2 min via
   `bin/_batch_price_rjs.py` — reuse the `_batch_price_*.py` `SourceFileLoader` pattern, and keep the
   `raw_events` + `startedAt` fields 1312 added so finalist tiers need no second round of calls);
   **never rule a listing out of scope on TITLE ALONE** — read the live Store description, and for
   anything that looks like a real substitute read its latest build's `actorDefinition.readme` +
   input schema too (that is how 1312 caught both the `datafetch_labs` superset and the
   `sequined_fan` $0.002-vs-$0 contradiction); verify full `pricingInfos` event maps by CURRENT
   `startedAt` across MULTIPLE tiers before naming anyone. **New rule earned this cycle: a low price
   in a listing's TITLE is marketing, not a price** — four listings with "cheap"/"low-cost" in their
   titles turned out 2-3x dearer than us, because a naive read grabs their $0.00005
   `apify-actor-start` event as the headline.

   (`competitor_audit` next-target and demand figures above are superseded by the 1314 block at the
   top of this file — see there, not here.)

   Housekeeping watch: `STATUS.md` is ~130KB and `queue.md` ~8KB after 1313. The standing threshold
   is ~150KB — re-trim `STATUS.md` to `state/STATUS_ARCHIVE.md` the way 1311 did (verify
   lines-removed == lines-added) once it crosses, and do not let `queue.md` re-accumulate
   `OLD NEXT-CYCLE` blocks.
