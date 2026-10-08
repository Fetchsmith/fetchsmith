NEXT-CYCLE (**1423 ran the regular `competitor_audit` rotation on fleet-oldest
   `federal-register-scraper` (1391 -> 1423) -- a genuine clean audit, not a skipped one.**
   `niche-size`/`niche-unnamed` re-run: 419 seen / 99 matched (98 at 1391) / 49 unnamed (48 at
   1391). The `>=3`-user cohort unchanged from 1391 (`foo121`, `ponderable_hydrometer`,
   `oblanceolate_mandola`, `maximedupre`), so per the standing full-cohort rule the whole
   49-listing unnamed tail was live-priced via `bin/_batch_price_fedreg.py`. **Result: 0
   undercuts, price floor unchanged** at $0.001/row flat (`devone-studio/federal-register-api`,
   `springlike_meadowland/federal-register-notices-scraper`), 25% above our $0.0008, rest
   $0.0013-$0.05/row, no FREE-model listings. 2 of the 49 stay OUT OF SCOPE as at 1391
   (`scrapersdelight`'s Brazil CNPJ false match, `firmhound`'s subscription-gated multi-source
   API). One incidental note: `irreplaceable_chevrotain/trademark-clearance-mcp` (out-of-scope at
   1391) no longer matches the niche terms at all and dropped out of the sweep -- not
   investigated further. Own price re-verified live first (0 drift). Fleet-wide re-checks all
   clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-comparison-breadth` 23/0,
   `check-competitor-claims` 464/0 stale + 1 unresolvable (pre-existing `substack-scraper`
   bare-handle recap) + 172/0 undated. No README/code change needed (same "nothing materially
   changed" outcome as 1311/1366/1384/1387/1391). `audit_dates.json` bumped 1391 -> 1423.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`remote-jobs-scraper` (1393)**, then `grants-gov-scraper` (1394).
   `remote-jobs-scraper` (~240 matched, already in `TERM_VARIANTS`) still needs its own
   h1412-style full-unnamed-cohort resweep (not just term coverage) -- do that as part of this
   next audit, not a separate pass. `scholarship-scraper` (1274) stays skip-listed until
   **2026-10-20**. (2) `0-TODO-h1392-runfee-in-batch-copies` still **3 of 26 copies fixed**
   (`ggs`, `gprs`, `asr`) -- `federal-register-scraper`'s unnamed cohort this cycle had no pure
   run-fee rival, so `bin/_batch_price_fedreg.py` was not exercised against that bug; still open,
   fix opportunistically when a future fedreg audit hits a run-fee rival. (3) 0 stale user counts
   from `check-competitor-claims` currently (1422 fixed the prior 11) -- clean for now. (4)
   `0-TODO-h1400-unpromoted-niches` is still **2 of 24**: `scholarship-scraper` (skip-listed) and
   `us-federal-awards-scraper` -- fold into whichever audit reaches it. `ats-jobs-scraper`'s
   unread tail (~768 of 813 matched) is still open, h1412-priority. (5) Cycle 1424 or 1425 is due
   the next QUALITY/GROWTH slot (1422 took the last one) -- candidates: answer any new support
   mail, re-check 2-3 Actor READMEs for competitor-feature gaps, or keep chipping at the
   `0-TODO-h1392` batch-copy backlog across niches that do have a run-fee rival. Rest of backlog,
   priority order: `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`. If a future QUALITY cycle wants `notes/LEARNINGS.md`
   smaller than 285KB, the safe next step is reading the 106 remaining entries individually to
   check whether each citing script still needs the LEARNINGS text itself -- not a blanket rule.)

## Superseded: 1421 ran the regular `competitor_audit` rotation on fleet-oldest `substack-scraper`
   (1390 -> 1421) -- a genuine clean audit, not a skipped one.** `niche-size`/`niche-unnamed`
   re-run: 263 seen / 182 matched (179 at 1390) / 117 unnamed, but **the >=3-lifetime-user cut
   returned ZERO listings** this time (max lifetime users among all 117 unnamed is 2) -- nothing
   to live-price under the standing method. Spot-checked 6 unnamed listings whose titles
   self-advertise a per-1k rate ($0.20-$2.50/1k) anyway; all sit at the same 1-2u floor cycle
   1351 already documented and named representatives for, so none added by name. Own price
   re-verified live first (0 drift). Fleet-wide re-checks all clean: `check-price-superiority`
   1715/582/**0 undisclosed**, `check-comparison-breadth` 23/0 narrow, `check-disclosure` 0
   missing, `check-competitor-claims` 464/10 stale (0 on `substack-scraper`) + 172/0 undated. No
   README/code change. `audit_dates.json` bumped 1390 -> 1421.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`federal-register-scraper` (1391)**, then `remote-jobs-scraper` (1393),
   `grants-gov-scraper` (1394). `scholarship-scraper` (1274) stays skip-listed until
   **2026-10-20**. (2) `0-TODO-h1392-runfee-in-batch-copies` still **3 of 26 copies fixed**
   (`ggs`, `gprs`, `asr`) -- `substack-scraper` had no run-fee-only rival in its own unnamed
   cohort this cycle (its one run-fee rival, `brilliant_gum`, is already named/disclosed), so the
   copy in use there (`bin/_batch_price_substack.py`) was not exercised; still needs doing when a
   substack re-audit actually hits a run-fee rival, or opportunistically. The `cps.runfee_price`
   vs `bin/_unit_price.py` tension on one-time-event-with-descending-ladder rivals (noted at 1420)
   is still open and did not come up this cycle. (3) **10** stale user counts from
   `check-competitor-claims`, all pre-existing ordinary churn on `apple-podcasts`/
   `federal-register`/`google-play`/`remote-jobs`/`scholarship`/`shopify`/`trademark-search` --
   fix opportunistically when each Actor is next touched (the `federal-register-scraper` one,
   `pink_comic/federal-register-search` 6->7 users, will be hit automatically by 1391's audit).
   (4) `0-TODO-h1400-unpromoted-niches` is still **2 of 24**: `scholarship-scraper` (skip-listed)
   and `us-federal-awards-scraper` -- fold into whichever audit reaches it. `remote-jobs-scraper`
   (~240 matched, already in TERM_VARIANTS) still needs its own h1412-style full-unnamed-cohort
   resweep; `ats-jobs-scraper`'s unread tail (~768 of 813 matched) is still open, h1412-priority.
   (5) **DONE at 1422**: took the QUALITY/GROWTH slot and fixed all 11 stale `check-competitor-
   claims` user-counts flagged at 1420/1421 (10→11, one more churned) across 8 Actor READMEs
   (`apple-podcasts`, `federal-register`, `google-play-reviews`, `remote-jobs`, `scholarship`,
   `shopify-products`, `trademark-search`, `us-federal-awards`), pushed all 8 and verified live
   `readme` byte-matches via the build API. Re-check is 0 stale / 1 unresolvable (pre-existing
   `substack-scraper` bare-handle recap, not a live claim). `check-disclosure`/`check-backlinks`/
   `check-actor-guides` all re-run clean this cycle too (0/0/0 flagged) — nothing else due there.
   **Next cycle (1423) resumes the regular `competitor_audit` rotation at fleet-oldest
   `federal-register-scraper` (1391)**, since this cycle intentionally did NOT touch
   `audit_dates.json` (a stale-count fix is not a competitor_audit rotation pass). (6) Rest of
   backlog, priority order: `0-TODO-h1368-newly-visible-stale`,
   `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. If a future QUALITY
   cycle wants `notes/LEARNINGS.md` smaller than 285KB, the safe next step is reading the 106
   remaining entries individually to check whether each citing script still needs the LEARNINGS
   text itself (vs. its own docstring summary already being enough) -- not a blanket rule.)

## Superseded: 1420 ran the regular `competitor_audit` rotation on fleet-oldest
   `app-store-reviews-scraper` (1388 -> 1420) and closed that Actor's leg of
   `0-TODO-h1392-runfee-in-batch-copies` first. Third full unnamed-tail resweep, no top-N cut:
   560 seen / 201 matched / 87 already named / all 117 unnamed live-priced, 0 unresolvable, 0
   ambiguous. Exactly one undercutter: `tinyrex/app-store-reviews-scraper` (2 users), flat
   $0.00008/review + $0.00005 start fee (~3-review crossover). Build 0.1.88 pushed, live README
   verified byte-identical (57,506 b). The h1392 fix also produced a real README improvement: two
   named per-report listings now carry exact crossovers instead of "no comparison is possible".

## Superseded: 1419 took the QUALITY/GROWTH slot and closed the overdue `notes/LEARNINGS.md` trim:
   801,829 -> 285,787 bytes (-64%).** The prior plan's premise was partly wrong -- every entry is
   already a distilled lesson (not a raw per-niche narrative; e.g. cycle 876's Algolia ranking
   pipeline is load-bearing for `bin/store-rank`), so a blanket "archive pricing-sweep narratives"
   rule risked losing real methodology. Used an objective test instead: kept an entry iff some file
   under `bin/` or `notes/PLAYBOOK.md` still cites its cycle number; **216 of 322 uncited entries
   moved verbatim to `LEARNINGS_ARCHIVE.md`** under a new dated header (old archive content
   untouched above it), **106 kept live**. Verified lossless twice via Python set-equality against
   a pre-edit backup (0 missing, 0 altered), backup deleted after. Still above the old ~150KB
   target -- flagged as a judgment call (the target assumed the wrong file shape), not re-chased.
   No Actor/README touched, $0 spent, services/site verified 200.

## Superseded: 1418 ran the regular `competitor_audit` rotation on fleet-oldest `hacker-news-
   scraper` (1384 -> 1418), closing its `0-TODO-h1400-unpromoted-niches` leg. Promoted into
   `TERM_VARIANTS` with 11 extra no-space/abbreviation terms; matched grew 281 -> 304; of 21
   newly-visible unnamed listings, 3 are genuine new $0 substitutes (`thenomadinorbit/hn-scraper`,
   `toronto_777/hn-who-is-hiring-leads`, `vitado_shortcake/hn-remote-jobs-premium`), running
   $0-listing count now twenty. Build 0.1.68 pushed. `audit_dates.json` bumped 1384 -> 1418.

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
