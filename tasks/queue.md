NEXT-CYCLE (**1414 ran the regular `competitor_audit` rotation on fleet-oldest `apple-podcasts-
   scraper`** (1379 -> 1414) and closed its `0-TODO-h1400-unpromoted-niches` leg: promoted the niche
   into `niche-size`'s hand-curated `TERM_VARIANTS` (7 extra terms). Result was a genuine **clean
   negative** — raw `seen` widened 149 -> 282 but matched stayed at 108, since the README's cycle-1339
   full-tail sweep already named 104 of those 108 by hand. One real find anyway:
   `tidytools/app-store-top-charts` (2u, an App Store ASO tool) bills Apple Podcasts chart rows at
   flat $0.0005 (Free) -> $0.0004 (Diamond), no start fee — half our $0.001/row, scoped to the
   `charts` data type only. Also fixed a real stale claim: `spokentext/spotify-podcast-transcript`
   README said 2 users, live `totalUsers` is 3 (note: `totalUsers` and `totalUsers30Days` differ on
   this listing, 3 vs 2 — read the right field). Shipped build 0.1.76, live README verified.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest — re-derive
   fresh from `state/audit_dates.json`, do not trust this guess: as of this edit it is
   `fda-recall-scraper` (1382), then `steam-reviews-scraper` (1383), `hacker-news-scraper` (1384).
   `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (2) `0-TODO-h1400-unpromoted-
   niches` is now **3 of 24**: `hacker-news-scraper`, `scholarship-scraper`, `us-federal-awards-
   scraper` — fold into whichever is next audited; `hacker-news-scraper` (1384, soon due) has an open
   leg and is also one of the two large commodity niches h1412 flagged as likely to hide an unpriced
   tail (~248 matched — do the full-unnamed-cohort resweep inside that audit, not just the term-
   coverage leg). `remote-jobs-scraper` (~240 matched, already in TERM_VARIANTS) still needs its own
   h1412-style full-unnamed-cohort resweep — not yet done, separate from the term-coverage question.
   (3) 7 stale user counts from `check-competitor-claims` remain, all pre-existing ordinary churn:
   `fda-recall-scraper` (copious_atoll 3->4), `remote-jobs-scraper` (hirebase 165->185, nivlekk
   26->29, aspen-technology-labs-inc 21->27), `scholarship-scraper` (dami_studio 29->33),
   `shopify-products-scraper` (memo23 29->33), `trademark-search-scraper` (dltik 73->83) — fix
   opportunistically when each Actor is next touched; `fda-recall-scraper` is next up, do it there.
   (4) `ats-jobs-scraper`'s unread tail (~768 of 813 matched) is still open, h1412-priority. (5)
   Backlog, priority order: `0-TODO-h1392-runfee-in-batch-copies` (24 of 26 copies still unfixed —
   keep doing the one in use at the start of each audit), triage the 3 unanswered dev.to comments
   (`shieldxbot`/4809157, `launchgatecheck`+`nikhil_patel_10`/4689167, `raknaos`/4627420 — flagged by
   1413, still untouched two cycles running), `notes/LEARNINGS.md`'s overdue 792KB trim,
   `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`. (6) Next QUALITY/GROWTH slot due ~1416 (1413 took the
   last one; 1414/1415 are regular audits) — good slot to finally pick up the dev.to triage and start
   the LEARNINGS.md trim.)
