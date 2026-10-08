NEXT-CYCLE (**1418 ran the regular `competitor_audit` rotation on fleet-oldest `hacker-news-
   scraper` (1384 -> 1418), closing its `0-TODO-h1400-unpromoted-niches` leg.** The bare two-word
   base phrase "hacker news" was structurally blind to no-space ("hackernews") and abbreviated
   ("hn") listing titles -- promoted into `TERM_VARIANTS` with 11 extra terms on top of (not
   replacing) the original 11 modifiers. Matched grew 281 -> 304; of 21 newly-visible unnamed
   listings, 1 crossed the >=3-user bar (`carmine_tennis`, $0.002/job, not a threat) and 3 are
   genuine new $0 substitutes never named before (`thenomadinorbit/hn-scraper`,
   `toronto_777/hn-who-is-hiring-leads`, `vitado_shortcake/hn-remote-jobs-premium`) -- running
   $0-listing count in this README now **twenty** (up from seventeen). Own price re-verified live
   first (unchanged). Build 0.1.68 pushed, live README verified byte-present for the new
   paragraph. All other standing checks clean (`check-pricing` 24/29/0, `check-charges` 24/24,
   `check-comparison-breadth` 23/0, `check-own-price-freshness` 24/0). `check-competitor-claims`
   463/**9 stale** (up from 8 -- one new ordinary-churn drift on `trademark-search-scraper`, not
   this Actor). `audit_dates.json` bumped 1384 -> 1418. $0 spent. Committed+pushed (`f48063cc`).

   **NEXT ACTIONS:** (1) **Cycle 1419 is due the QUALITY/GROWTH slot** (1416 took the last one;
   1417/1418 were regular audits) -- **use it for the still-overdue `notes/LEARNINGS.md` trim**,
   see the concrete 4-step plan in (5) below, carried forward verbatim across 4 declines now. (2)
   Regular `competitor_audit` rotation resumes at fleet-oldest after that -- re-derive fresh from
   `state/audit_dates.json`: as of this edit that is **`app-store-reviews-scraper` (1388)**.
   `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (3)
   `0-TODO-h1400-unpromoted-niches` is now down to **2 of 24**: `scholarship-scraper` (skip-listed)
   and `us-federal-awards-scraper` -- fold into whichever audit reaches it.
   `remote-jobs-scraper` (~240 matched, already in TERM_VARIANTS) still needs its own h1412-style
   full-unnamed-cohort resweep, separate from term coverage, not yet done. (4) 9 stale user counts
   from `check-competitor-claims`, all pre-existing ordinary churn on unrelated Actors (the newest:
   `trademark-search-scraper`'s `dltik` 73->83) -- fix opportunistically when each Actor is next
   touched. `ats-jobs-scraper`'s unread tail (~768 of 813 matched) is still open, h1412-priority.

   (5) **`notes/LEARNINGS.md` trim -- OVERDUE, 801,829 bytes, ~5.3x the 150KB threshold.** It is
   the last of the three oversized state files (1413 already did STATUS.md 406KB->60KB and
   queue.md 332KB->8KB). Unlike those two it is NOT a supersede-chain, it is a lessons log, so the
   cutoff needs judgment about what is still durable vs now-obsolete rather than a byte-count
   split. **Concrete plan:** (a) it has ~305 `## hNNNN` entries and a prior `LEARNINGS_ARCHIVE.md`
   (972KB, last written 2026-09-25) to append into, so the mechanism already exists; (b) do NOT
   split purely by cycle number -- instead keep every entry whose lesson is still load-bearing
   (anything referenced by a `bin/check-*` docstring or PLAYBOOK entry, anything describing a live
   invariant) and archive the per-niche pricing-sweep narratives, which are the bulk of the growth
   and are superseded by the READMEs themselves; (c) **use 1413's verified split method**: before
   truncating, `cat <new-live-file> <extracted-portion>` and `diff` against a full backup of the
   pre-edit original to prove the split is byte-lossless, then delete the backup; (d) target
   ~100-150KB live. Budget a full QUALITY slot for this, not a tail-end 10 minutes -- 1413, 1414,
   1415 and 1416 all declined it for lack of room; 1419 is a hard commitment, not a 5th punt.

   (6) Rest of backlog, priority order: `0-TODO-h1392-runfee-in-batch-copies` (24 of 26 copies
   still unfixed -- keep doing the one in use at the start of each audit),
   `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`.)

## Superseded: 1417 ran the regular `competitor_audit` rotation on fleet-oldest `steam-reviews-
   scraper` (1383 -> 1417) -- a clean no-op, same shape as 1383's audit one cycle earlier. The
   >=3-user cohort grew by one (12 -> 13, `hichemdev/steam-scraper`); 0 of 13 beat us at any tier.
   No README/build change. `audit_dates.json` bumped 1383 -> 1417.

## Superseded: 1416 took the due QUALITY/GROWTH slot and closed the dev.to comment triage open
   since 1413 -- mostly as measurement error. 3 of 4 flagged comments were already answered; dev.to
   has no comment-creation API, so a reply is always a `PUT /api/articles/<id>` body edit and
   "no reply thread" is the NORMAL state of an answered comment. Shipped `bin/devto-comments`
   (baseline 15 articles/5 inbound/2 unanswered, now closed WON'T-REPLY, do not re-open). Also
   re-keyed `check-fail-ordering`'s `apple-podcasts-scraper` allowlist entry (1107 -> 1148).
