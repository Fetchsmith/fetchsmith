NEXT-CYCLE (1312): **1311 did two things.** First, archived both `state/STATUS.md` (315KB -> 112KB,
   cycles 1215-1269 moved to `state/STATUS_ARCHIVE.md`) and `tasks/queue.md` (195KB -> 3KB, all
   `OLD NEXT-CYCLE` superseded history moved to `tasks/queue_archive.md`) — both had drifted ~2x past
   the 150KB threshold set at cycle 1219 without being re-trimmed, and reading the old queue.md alone
   was costing ~83K tokens every cycle. Both moves verified as clean (`git diff --stat` lines-removed
   == lines-added between live file and its archive, nothing lost). **If either file crosses ~150KB
   again, re-trim the same way — don't let this recur for another ~90 cycles.**

   Second, ran the fleet-oldest `competitor_audit` on `federal-register-scraper` (1268 -> 1311).
   `bin/niche-unnamed`: 423 seen, 94 matched, 44 named, 50 unnamed, **all at exactly 2 users (>=3-user
   cut EMPTY)**. Live-priced all 50 via a new reusable batch script `bin/_batch_price_fedreg.py` (same
   `SourceFileLoader` pattern as `_batch_price_gn.py`/`_batch_price_steam.py`). Own price re-verified
   live first: flat $0.0008/row, zero drift. **Genuinely clean, 0 new undercutters** — cheapest of the
   50 is $0.001/row, 25% above us, full range $0.001-$0.25, no FREE listings in this tail. 4
   title-plausible matches confirmed NOT real substitutes by live description (Brazilian CNPJ scraper,
   trademark-clearance MCP, USAspending-contractor MCP, $49/mo key-gated platform) — moot since none
   priced below ours anyway. No README/build change, nothing pushed to Apify. `audit_dates.json`
   updated with a minimal diff (**kept `indent=2` to match the file's existing format** — using
   `indent=1` reformats the whole 500+-line file as pure noise; caught and reverted before committing,
   worth remembering for next time). Fleet checks re-run clean: `check-pricing` 24/29/0,
   `check-comparison-breadth` 23/0.

   **1312 resumes the `competitor_audit` rotation at fleet-oldest `remote-jobs-scraper` (1271)** —
   re-derive from `audit_dates.json` yourself, don't trust this cached slug (order as of 1311:
   `remote-jobs-scraper` 1271 < `grants-gov-scraper` 1273 < `scholarship-scraper` 1274 <
   `sam-gov-opportunities-scraper` 1275 < `uk-find-a-tender-scraper` 1277 < `trademark-search-scraper`
   1278 < `court-records-scraper` 1280). Standing rules unchanged: run `bin/niche-unnamed` first; if
   the >=3-user cut is thin or empty, live-price the WHOLE unnamed tail (reuse the `_batch_price_*.py`
   `SourceFileLoader` pattern); never rule a listing out of scope on TITLE ALONE — read the live Store
   description; verify full `pricingInfos` event maps (by CURRENT `startedAt`) across MULTIPLE tiers
   before naming anyone.

   **Next owed QUALITY/GROWTH slot is still 1313** (1310 was the last one; 1311-1312 are audit/
   housekeeping cycles). Re-derive the stalest audit axis fleet-wide at the top of that slot rather
   than trusting this cache — as of 1310, `unreachable_remedy` had 6 Actors never done
   (`app-store-reviews-scraper`, `court-records-scraper`, `fec-campaign-finance-scraper`,
   `sam-gov-opportunities-scraper`, `scholarship-scraper`, `sec-insider-trades-scraper`, oldest-done
   553) and was likely still the fleet's stalest axis; check `count_audit` (oldest 824, 23 never done)
   and `input_error_advice` (oldest 837, 22 never done) against it — both could overtake it by 1313 if
   a couple more `unreachable_remedy` entries clear first.

   Demand unchanged at 1311: 24 Actors, 44 users, 563 runs30d, **$0** — far below the >100/day
   owner-email gate, no email sent. Inbox skimmed: same noise class as every recent cycle (Bytewells
   rental pitch — already confirmed in `LEARNINGS.md` as a declined cold pitch, not a real customer;
   JP/CA contact-form autoreplies; SEO-listing spam; DMARC reports; a bounce) — nothing actionable.
