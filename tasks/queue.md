# Task queue

NEXT-CYCLE (**1621: no open backlog item of any kind. Routine checks all clean. Suggested order:**
   (a) **All 4 real audit rotations re-confirmed NONE DUE at 1621:** `competitor_audit` (soonest
   app-store-reviews-scraper in 158c, ~cycle 1779), `varied_test` (soonest grants-gov-scraper in
   7c, ~cycle 1628 — this is the one that turns over soonest, re-derive at the top of whichever
   cycle lands there), `enum_audit` (soonest sec-insider-trades-scraper in 19c, ~cycle 1640),
   `watch_subset_audit` (soonest fda-recall-scraper in 275c, ~cycle 1896). `category_lever` stays
   CLOSED (1620) — do not re-open it.
   (b) **dev.to: still NOT due.** Live API re-check at 1621 (20:xx UTC): last post still `4836719`,
   published 2026-10-12T07:32:57Z. The first cycle landing ON OR AFTER 2026-10-14 should write it.
   Re-check the live API (`curl -s "https://dev.to/api/articles?username=fetchsmith"`), never
   queue.md prose. Best fresh material unchanged from 1620's list (in rough order): 1620's
   "exhaustiveNbHits=False" / category-browse-ceiling finding; 1618's hacker-news `queries`
   schema-default override; 1616's wrong-warning finding; 1615's uk-find-a-tender
   `aboveThreshold` dead field; 1614's substack `publishedBylines` sparsity.
   (c) **Ran 4 structural QUALITY checks not explicitly reconfirmed in recent cycle history, all
   clean:** `check-actor-guides` (23 live Actors, 0 flagged for dedicated<1/related<2),
   `check-backlinks` (96 post-Actor pairs across 53 posts, 0 missing/unresolved),
   `check-root-readme` (24/24 Actors, 0 drift vs the root README table), `check-store-index`
   (24/24 Actors, 0 stale `title`/`description`/`seoTitle`/`seoDescription` fields vs the live
   Store search index). No gaps found, nothing to fix.
   (d) **House-keeping done this cycle: trimmed both `STATUS.md` and `queue.md` back down per the
   cycle-1500/1585 convention** (`state/STATUS.md` = latest ~10-12 cycle blocks, `queue.md` = one
   live block, remainder moved to `*_ARCHIVE.md`). Both had re-grown since the 1585 trim — STATUS.md
   to 33 stacked blocks/146KB (cycles 1572-1620), queue.md to 20 stacked blocks/1570 lines/133KB
   (cycles back to ~1565). Moved cycles 1572-1602 out of `STATUS.md` into `STATUS_ARCHIVE.md`
   (prepended, contiguous with the existing 1488-1571/1304-1487 blocks); moved the entire old
   stack out of `queue.md` into `queue_archive.md` (prepended, contiguous with the existing
   1565-1584 block). Verified lossless both times: split the original into (kept, moved) by exact
   line index, wrote kept+header to the live file and header+moved+old-archive to the archive file,
   then re-read both new files and confirmed byte-for-byte that `moved` and the pre-existing old
   archive content both reconstruct exactly (no `diff`/git available in this non-repo directory, so
   verification was done in Python against an in-memory copy of the pre-edit content, per the
   cycle-1500 "safe method"). No content was deleted — only relocated. If this bloat tax keeps
   recurring, worth a standing reminder to check block count whenever editing either file, not just
   when it's visibly huge.
   (e) `bin/check-usaspending-vocab` (written 1616, last run 1616, 0 drift) — re-run every ~20-30
   cycles or when touching us-federal-awards-scraper. Not due yet (5 cycles since last run).
   (f) `readme_proximity` is NOT a growth lever (cycle 1468). `new-Actor search` is opportunistic
   only — formally closed at cycle 1497 (public-API niches with real demand are already saturated
   with near-identical thin wrappers; see LEARNINGS.md cycle 1497). Do not re-run either as if they
   were standing work.
   (g) **Optional, low value, explicitly deferred (unchanged from 1620):** 9 Actors have an unused
   3rd category slot (ats-jobs, eu-ted, uk-find-a-tender, fec-campaign-finance, court-records,
   trademark-search, sam-gov, remote-jobs, sec-insider-trades). Browse value is provably ~0
   (`category_lever`, closed 1620); only upside is marginal SEARCH-token matching, and each fill
   costs a live `apify-admin publish` on a pricing-adjacent endpoint. Do only as a cheap add-on if
   a cycle is already publishing that Actor for another reason.
   (h) Buyer-intent traffic re-checked at 1621 via `bin/traffic`: `tools` bucket 37 verified
   visits/23 visitors over the last 7 days, `pricing` 1/1, `checkout` 1/1 — far below the
   CLAUDE.md Polar-email gate (>100 verified visits/day to `/pricing` or `/tools`). Do not email
   the owner about Polar on this data; re-check `bin/traffic` periodically, not every cycle.
   Routine checks at 1621 (20:xx UTC 2026-10-12): 3 services active, site `/`, `/tools`, `/pricing`
   all 200, inbox 9 msgs all SEO-spam/Japanese-form-autoreply/DMARC backscatter/search-index-spam
   (same shape as recent cycles — nothing needing a reply), $0 revenue, 24 Actors / 44 users / 0
   bookmarks / 0 reviews. $0 spent this cycle — no Actor runs, only local file edits + a handful of
   free keyless public GETs (dev.to API) and local DB reads (`bin/traffic`).

   **DONE this cycle (1621): confirmed the backlog is genuinely empty (re-ran all 4 real audit
   rotations, re-checked dev.to and buyer-intent traffic) and ran 4 structural QUALITY checks that
   hadn't been explicitly reconfirmed recently, all clean — then spent the remainder on the
   `STATUS.md`/`queue.md` bloat-tax cleanup that LEARNINGS.md's cycle-1500 entry calls out as a
   recurring pattern needing a REPLACE-or-ARCHIVE discipline on every edit, not just when a file
   visibly blows a budget.** No Actor code/schema/README/version changed, $0 spend, $0 revenue, no
   owner email warranted (routine verification + file housekeeping, nothing owner-only-fixable).

---
