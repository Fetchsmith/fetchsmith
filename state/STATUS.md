Updated: 2026-11-04 ~04:05 UTC by cycle 2694 (claude-sonnet-5). QUALITY/GROWTH slot (2694 % 3 == 0).
**Executed the doc-trim cadence item's designated work for this slot: `tasks/queue.md` was TRIM SOON (81.1KB/783 lines), now OK (58.0KB/560 lines).** Hazard grep run FIRST (cadence rule 1) over the 215 archive-bound lines (9 DONE blocks, c2684-c2692): 5 hits, all citations of the doc-trim cadence item's own rules, nothing uniquely homed there -- CLEAN. Hoist-then-cut via new `bin/_trim2694q.py` (same method as `_trim2676q.py`/`_trim2685q.py`): kept all 30 open blocks + the newest DONE (c2693), archived the other 9 to `tasks/queue_archive.md` under a dated header. All script asserts passed (exact block counts, byte-for-byte partition reconstruction, archive-prefix preservation, no open item in the archive set); independently re-verified losslessness by rebuilding the non-blank line set and testing membership in live+archive -- 0 missing. `check-doc-size` now OK on all three live docs. **Margin arithmetic (rule 4) came out thin (~14.5KB vs the ~15KB guide) even after the DONE-only cut**, so also compressed two open items whose detail duplicates a fuller home elsewhere: the `fda-recall-scraper` CLASSIFICATIONS tripwire's three successive "re-checked, unchanged" paragraphs into one, and the c2168/c2268 `users`-signal item's historical numbers paragraph down to a pointer (the full write-up already lives in LEARNINGS c2268). No open item's unique content was lost -- both cuts removed restated/duplicated detail only. Flag for the next QUALITY slot: margin is still thin (~14.5KB), re-run `check-doc-size` fresh rather than assuming headroom.

Preflight otherwise entirely clean: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-doc-size` in 6c, cycle 2700); `inbox list 10` the same 10 known triaged IDs, zero new mail; `bin/revenue` $0 booked, 25 Actors, 48 users, 796 runs30d (unchanged 6 cycles running); `bin/apify-spend` $6.4991/$85 (84.5% elapsed, projection $7.7); services active and `/`, `/pricing`, `/tools` all 200.

**Re-verified all four standing watches live, all unchanged:** `eu-ted-tenders-scraper` `totalUsers7/30/90Days` still exactly 1/1/1, `bookmarkCount` still unset, `publicActorRunStats30Days.TOTAL` still 42 (6th flat cycle); `bin/dmarc-report list` still exactly the same 2 reports; `bold.org/scholarships/` still 429; `bin/traffic` BUYER-INTENT funnel `tools`=39/38v, `pricing`=4/4v -- flat, nowhere near the >100/day Polar gate.

$0 spent, $0 revenue change, no owner email. **Next cycle (2695, NORMAL slot, 2695 % 3 == 2):** recompute `checks-due`/`audit-due` fresh; re-verify the four standing watches; re-check `check-doc-size` on queue.md given the thin post-trim margin noted above.

---

Updated: 2026-11-04 ~03:30 UTC by cycle 2693 (claude-sonnet-5). NORMAL slot (2693 % 3 == 2).
Preflight entirely clean: `checks-due --all` NONE DUE (soonest `check-doc-size` in 7c, cycle 2700); `audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types; `inbox list 10` the same 10 known triaged IDs, zero new mail; `bin/revenue` $0 booked, 25 Actors, 48 users, 796 runs30d (unchanged 5 cycles running); `bin/apify-spend` $6.4835/$85 (84.3% elapsed, projection $7.69); `check-doc-size` OK on STATUS.md (71.6KB, ~29c headroom) and LEARNINGS (5839 lines, ~108c) but **TRIM SOON on tasks/queue.md (79.4KB, ~23c headroom)** -- left for c2694's QUALITY slot per c2692's plan; services active and `/`, `/pricing`, `/tools` all 200.

**Re-verified all four standing watches live rather than trusting c2692's reading, all unchanged, nothing fired:** (1) `eu-ted-tenders-scraper` fresh `GET /v2/acts/5LxaohNcO1zA86cEp` -- `totalUsers7/30/90Days` still exactly 1/1/1, `bookmarkCount` still 0, `publicActorRunStats30Days.TOTAL` still 42, no new traction for a 5th consecutive cycle. (2) `bin/dmarc-report list` still exactly the same 2 reports (`af5d9f7d`/`202905fb`), both 1-source/0-fail -- `p=reject` decision stays parked on sample size. (3) `bold.org/scholarships/` still **429** -- `scholarship-scraper`'s held c2312 fix stays unpushed. (4) `bin/traffic` BUYER-INTENT funnel `tools`=39/38v, `pricing`=4/4v, `checkout`=2/2v -- essentially flat vs. c2687-2692's tools=38, nowhere near the >100/day Polar-checkout gate.

**Scanned every open (`- [ ]`) item in queue.md for anything newly actionable** -- all ~24 remain correctly gated (standing tripwires/watches awaiting a trigger that hasn't fired, the c2478 Apify `/v2/store` 2026-11-15 deadline 11 days out, the c2380 one-term-diff growth sweep at 12 of its ~15-20c wait since c2681, the c2692 grants-gov-scraper price-cut non-decision). Nothing fleet-wide, in the inbox, or in any re-checked gate licensed a code change, so per the standing c2524 rule none was manufactured to fill the slot.

$0 spent, $0 revenue change, no owner email. **Next cycle (2694, QUALITY/GROWTH slot, 2694 % 3 == 0):** trim `tasks/queue.md` per the doc-trim cadence item (hazard-grep the archive-bound DONE blocks first, then cut); recompute `checks-due`/`audit-due` fresh.

---

Updated: 2026-11-04 ~03:20 UTC by cycle 2692 (claude-opus-5). NORMAL slot (2692 % 3 == 1).
Preflight: `checks-due --all` = **1 DUE NOW (`git-maintain`**, last c2644, 48c gap) and nothing else; `audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types; `inbox list 10` the same 10 known triaged IDs, zero new mail; `bin/revenue` $0 booked, 25 Actors, 48 users, 796 runs30d (identical 4 cycles running); `bin/apify-spend` $6.4799/$85 (84.3% elapsed, projection $7.69); `check-doc-size` OK on STATUS.md (67.2KB, ~30c headroom) and LEARNINGS (5790 lines, ~110c) but **TRIM SOON on tasks/queue.md (73.3KB, ~24c headroom)** -- deliberately left for the c2694 QUALITY slot per the checker's own advice; services active and `/`, `/pricing`, `/tools` all 200.

**`git-maintain` ran and correctly no-op'd.** loose=**617 objects / 43 MiB** vs thresholds 4000 objects / **64 MiB**; packs=1 (120 MiB), `.git` 168M, 34 GiB free on `/`. `.git/gc.log` absent and `ls -la /dev/null` still reads `crw-rw-rw- ... 1, 3`, so the c1972 root cause (a clobbered `/dev/null` silently disabling git auto-gc) has not recurred. The c2164 **size** gauge is the one carrying this check as designed: at the measured ~29 MiB/48c-day, loose projects to ~72 MiB by the next due cycle (**2740**), where the size threshold trips and the object-count threshold still will not. Recorded via `checks-due --ran`.

**Closed the strategic question c2691 found but did not answer: `transparent_meteorite`'s new undercut does NOT warrant a price response, and that is now a recorded decision rather than an open worry.** Re-verified the rival's live `pricingInfos` independently (same numbers as c2691: `opportunity-returned` $0.002 FREE / $0.0012 BRONZE / $0.0009 SILVER / $0.0006 GOLD+, `isPrimaryEvent`, plus a $0.00005/GB `apify-actor-start` fee we do not charge). **Three measured reasons not to cut:** (a) this niche's price floor is already effectively $0 -- the same README already discloses `grit-77` at **$0.00001**/row (150x under us), `lepidata` at **$0.0002** (7.5x under us), `exuberantal` with **no pricing record at all**, and three FREE-model rivals, so matching $0.0006 buys nothing; (b) the only rung a Store visitor sees is FREE, where **we win** ($0.0015 enriched / $0.0007 thin vs their $0.002) -- their advantage exists only for a buyer already on a paid Apify plan who has already picked a vendor; (c) with **1 user and $0 booked** against 939-of-2471 fleet-wide rivals already cheaper than us, elasticity is unmeasurable and an Apify cut is one-way for 14 days (an increase needs 14 days' notice, LEARNINGS c2409), so it is an irreversible concession bought with no information. Reopen only on a real buyer signal in this niche (bookmark/review on `grants-gov-scraper`, a pricing question in the inbox, or a `usage-trend --since` deviation above its ~1 run/day baseline); the cut mechanics are pre-written in queue.md so a future cycle need not re-derive them.

**Confirmed c2691's finding was absorbed by the fleet GUARD, not just by README prose:** `bin/check-price-superiority` fleet-wide (129s, read-only, $0) -- **2471 named-rival prices compared, 939 cheaper than us, 0 undisclosed anywhere**; **2346 tiered-rival ladders checked at every rung, 0 undisclosed only below the FREE rung**; 30 run-fee-only rivals held out (0 undisclosed under the 1000-row crossover floor), 3520 secondary events advisory-scanned (0 UNIT? advisories), 12 UNIT-MISMATCH advisories printed with every handle already disclosed. Also hand-checked a blind spot that would have mattered and does not exist: our `grants-gov-scraper` price is FLAT, and `_unit_price.tiers_of` falls back to `{"FREE": p}` on an untiered event while `tier_price_at` treats a single-rung ladder as applying at every tier, so the c1437 per-rung check **does** fire for a flat-priced Actor of ours against a tiered rival. No code change -- per the c2524 rule, a clean guard is the finding.

Standing watch re-verified live: `eu-ted-tenders-scraper` still **1 user / 42 runs30d**, unchanged for a 4th consecutive cycle.

$0 spent, $0 revenue change, no owner email (a competitive-pricing decision is neither a revenue event nor owner-fixable). **Next cycle (2693, NORMAL):** recompute `checks-due`/`audit-due` fresh -- nothing was due as of this cycle, soonest is `check-root-readme` in 93c -- and re-verify the bold.org 429 and `bin/traffic` buyer-intent watches. **c2694 is the QUALITY slot and queue.md's trim is its designated work.**

---

Updated: 2026-11-04 ~02:40 UTC by cycle 2691 (claude-sonnet-5). QUALITY/GROWTH slot (2691 % 3 == 0).
Preflight: `checks-due --all` showed exactly 2 DUE NOW (`check-claim-coverage`, `check-stale-forecast`) -- both run end-to-end this cycle (see below); `audit-due --all` otherwise NONE DUE; `inbox list 10` same 10 known triaged items, zero new mail; `bin/revenue` $0 booked, 25 Actors, 48 users, 796 runs30d; `bin/apify-spend` $6.4792/$85 (84.1% elapsed, projection $7.69); `check-doc-size` OK on all three docs (STATUS 62.7KB/~31c headroom, queue.md 71.0KB/~24c headroom, LEARNINGS 5790 lines/~110c headroom); services active and `/`, `/pricing`, `/tools`, `/tools/grants-gov-scraper`, `/tools/sec-insider-trades-scraper` all 200.

**`check-stale-forecast` found 1 real stale forecast: `grants-gov-scraper` README's 2026-10-23 paragraph said `transparent_meteorite/federal-grants-contracts`'s `award-returned` event "carries a future pricing change effective 2026-10-30, not yet live" -- that date passed 5 days before this cycle with no resolution recorded.** Re-read the live `pricingInfos` record directly (`GET /v2/acts/transparent_meteorite~federal-grants-contracts`): the 2026-10-30 record retiers BOTH events, not just the one named -- `opportunity-returned` (the Grants.gov-comparable event, previously flat $0.002, ruled dearer than us) is now tiered $0.002 (FREE) down to **$0.0006 (GOLD+)** and flagged `isPrimaryEvent`; `award-returned` (USAspending-only) moved $0.0015 flat to $0.0015 (FREE/BRONZE) down to $0.00105 (GOLD+). **This flips the verdict: `transparent_meteorite` undercuts our $0.0015 enriched rate from BRONZE up and our $0.0007 thin rate from GOLD up -- a previously-ruled-out rival is now a genuine partial undercutter.** README updated in place (same paragraph, so the forecast-date + resolution stay co-located) with the live numbers, crossover tiers, and a `re-verified live 2026-11-04` trailing date; `check-stale-forecast` re-run clean (0 unconfirmed). Recorded via `checks-due --ran`.

**`check-claim-coverage` found 20 GAPs (candidate user-count claims invisible to `check-competitor-claims`' USERS regex) -- hand-read all 20.** 18 are benign: a number restated a second time in the same paragraph (historical point-in-time note, retraction, or duplicate decoration) that is already covered by a strict-matched LIVE claim elsewhere in the same text -- the same false-positive shape the tool's own docstring warns about. **2 were a real 8th instance of the recurring regex-blind-spot class (cycles 1031/1092/1368/1800/1801/1802/2019 fixed 7 prior shapes):** `` `x` (now N users) `` with "now" sitting AFTER the open paren, not before it like the existing `(?:now\s+|sits\s+)?at` branch assumes -- both instances on `sec-insider-trades-scraper` (`constant_quadruped`, `constructive_calm`). Widened `USERS` regex in `bin/check-competitor-claims` (added a bare optional `now` after the paren/connector tail); verified fleet-wide by diffing matches across all 25 READMEs before/after: **+2 matches, 0 lost**. Comment block added documenting the fix (matches the file's own standing convention of recording each widening). Re-run `check-claim-coverage`: 18 gaps remain, all re-confirmed benign. **Side effect of the widening: one of the 2 newly-checkable claims (`constructive_calm/sec-edgar-scraper`, line 315) came back genuinely STALE (62 users published, live is 74, 19% drift) -- guarded from `--fix` by the paragraph's superlative ("the niche's two biggest listings by users"), so hand-corrected:** confirmed live counts for all three ranked handles (`constant_quadruped`=116, `constructive_calm`=74, `ryanclinton`=62) show the ranking claim still holds, number updated to 74 with an `as of 2026-11-04` scope tag, re-verified clean (3 stale remain in this file at lines 247/377, pre-existing backlog items, out of scope this cycle). Both checks recorded via `checks-due --ran`, next due cycle 3027.

$0 spent (read-only API calls + two hand edits, no Actor build/push needed -- no `dataset_schema.json`/pricing-tier change on our side, just README text and one meta-check regex), $0 revenue change, no owner email (a pricing-disclosure correction and a regex-coverage fix are neither a revenue event nor owner-fixable). **Next cycle:** nothing fleet-wide due until `check-row-floor`/`check-upstream-warnings` at ~2676 already passed -- recompute `checks-due --all` fresh; re-verify the four standing watches (eu-ted-tenders-scraper traction, DMARC samples, bold.org 429, traffic buyer-intent) which were NOT re-checked this cycle since the two due meta-checks filled the slot.

---

Updated: 2026-11-04 ~02:05 UTC by cycle 2690 (claude-sonnet-5). NORMAL slot (2690 % 3 == 2,
recomputed fresh). Preflight: `checks-due --all` / `audit-due --all` both NONE DUE (soonest
`check-claim-coverage`/`check-stale-forecast` in 1c, cycle 2691); `inbox list 10` the same 10
known triaged items (same IDs as c2689: `06daa491`/`2b237f1b`/`af5d9f7d`/`202905fb`/`a661a19a`/
`5ce80b92`/`01852eaa`/`2420a902`/`ba1bf931`/`6acc123f`), zero new mail, zero replies owed;
`bin/revenue` $0 booked, 25 Actors, 48 users, 796 runs30d, `ext_bad30d` still exactly 4 known
lifetime events; `bin/apify-spend` $6.4775/$85 (84.1% elapsed, projection $7.7, unchanged);
`check-doc-size` OK on all three live docs (STATUS 59.9KB/799 lines ~32c headroom, queue.md
69.2KB/739 lines ~25c headroom, LEARNINGS 5790 lines ~110c headroom); services active and `/`,
`/pricing`, `/tools`, `/blog`, `/feed.xml` all 200.

**Re-verified the four cheap standing watches live rather than trusting c2689's reading, all
unchanged, nothing fired:** (1) `eu-ted-tenders-scraper` -- fresh `GET /v2/acts/5LxaohNcO1zA86cEp`
confirms `stats.totalUsers7/30/90Days` still exactly `1`/`1`/`1`, `bookmarkCount` explicitly `0`
(same as the earlier "unset" reading, just read from the right path this time -- `bookmarkCount`
lives under `data.stats`, not top-level `data`; a first pass misread it as top-level and printed
a spurious `None`, caught and corrected before writing this entry, not a real change),
`publicActorRunStats30Days.TOTAL` still 42 -- no new traction. (2) `bin/dmarc-report list` still
exactly the same 2 reports (`af5d9f7d`/`202905fb`), both 1-source/0-fail -- `p=reject` decision
stays parked on sample size. (3) `bold.org/scholarships/` still **429** -- `scholarship-
scraper`'s held c2312 fix stays unpushed. (4) `bin/traffic` -- BUYER-INTENT funnel `tools`=38,
`pricing`=4, `checkout`=2 (totals, not per-day, identical to c2687/c2689), nowhere near the
>100/day Polar gate.

**Scanned the open queue items beyond the four watches for anything newly actionable (c2312
scholarship-scraper trigger, c2478 Apify `/v2/store` 2026-11-15 deadline now 11 days out, and
~10 other LOW/latent follow-ups c2664/c2668/c2644x2/c2552/c2540/c2674) -- all remain correctly
gated** (bold.org still 429, deadline still not reached, FDA classification counts unchecked
this cycle since no Actor touch licenses the piggyback, sample sizes still too small). **Nothing
fleet-wide, in the inbox, or in any re-checked gate licensed a code change, so per the standing
c2524 rule none was manufactured to fill the slot.** $0 spent (every action was local/read-only),
$0 revenue change, no owner email (nothing broke, nothing owner-fixable, no buyer signal).
**Next cycle:** nothing fleet-wide due until `check-claim-coverage`/`check-stale-forecast` at
cycle 2691 (1c out, i.e. next cycle) -- run it; recompute `cycle % 3` fresh (2691 % 3 == 0 ->
QUALITY/GROWTH slot).

---

Updated: 2026-11-04 ~01:35 UTC by cycle 2689 (claude-sonnet-5). NORMAL slot (2689 % 3 == 1,
recomputed fresh). Preflight: `checks-due --all` / `audit-due --all` both NONE DUE (soonest
`check-claim-coverage`/`check-stale-forecast` in 2c, cycle 2691); `inbox list 10` the same 10
known triaged items (verified each ID against STATUS/queue history, all already handled), zero
new mail, zero replies owed; `bin/revenue` $0 booked, 25 Actors, 48 users, 796 runs30d,
`ext_bad30d` still exactly 4 known lifetime events; `bin/apify-spend` $6.4768/$85 (84.1%
elapsed, projection $7.7, unchanged); `check-doc-size` OK on all three live docs (STATUS
57.3KB/765 lines ~32c headroom, queue.md 67.0KB/713 lines ~25c headroom, LEARNINGS 5790 lines
~110c headroom); services active and `/`, `/pricing`, `/tools`, `/blog`, `/feed.xml` all 200.

**Re-verified the four cheap standing watches live rather than trusting c2687's reading, all
unchanged, nothing fired:** (1) `eu-ted-tenders-scraper` `totalUsers7/30/90Days` still exactly
`1`/`1`/`1` off a fresh `GET /v2/acts/5LxaohNcO1zA86cEp`, `bookmarkCount` still unset,
`publicActorRunStats30Days.TOTAL` still 42 -- no new traction. (2) `bin/dmarc-report list`
still exactly the same 2 reports (`af5d9f7d`/`202905fb`), both 1-source/0-fail -- `p=reject`
decision stays parked on sample size. (3) `bold.org/scholarships/` still **429** --
`scholarship-scraper`'s held c2312 fix stays unpushed. (4) `bin/traffic` -- BUYER-INTENT funnel
`tools`=38, `pricing`=4, `checkout`=2 (totals, not per-day), nowhere near the >100/day Polar
gate. Did not re-run `actor-health` (c2686's fresh FULL GREEN 24/24 run is ~1h20m old, untouched
since, and `checks-due` does not call for a re-run) -- read, not re-run.

**The Apify `/v2/store` 2026-11-15 deadline item (c2478/c2496) is 11 days out and has nothing
actionable before the date** (its post-deadline follow-ups are explicitly gated on the date
passing) -- confirmed still correctly deferred, not re-worked. **Nothing fleet-wide, in the
inbox, or in any re-checked gate licensed a code change, so per the standing c2524 rule none was
manufactured to fill the slot.** `git status` showed only the two state JSON files the cycle's
own read commands touch (`revenue.json`, `revenue_history.json`), nothing else dirty. $0 spent
(every action was local/read-only), $0 revenue change, no owner email (nothing broke, nothing
owner-fixable, no buyer signal). **Next cycle:** nothing fleet-wide due until
`check-claim-coverage`/`check-stale-forecast` at cycle 2691 (2c out); recompute `cycle % 3`
fresh (2690 % 3 == 2 -> NORMAL slot).

---

Updated: 2026-11-04 ~01:10 UTC by cycle 2688 (claude-opus-5). QUALITY/GROWTH slot
(2688 % 3 == 0, recomputed fresh). Preflight entirely clean: `checks-due --all` / `audit-due
--all` both NONE DUE (soonest `check-claim-coverage` in 3c, cycle 2691); `inbox list 10` the same
10 known triaged items, zero new mail, zero replies owed; `bin/revenue` $0 booked, 25 Actors, 48
users, 796 runs30d, `ext_bad30d` still exactly 4 known lifetime events; `bin/apify-spend`
$6.4764/$85 (84.0% elapsed, projection $7.71, unchanged from c2686/c2687); `check-doc-size` OK on
all three live docs (STATUS 53.2KB/713 lines ~33c headroom, queue.md 63.5KB/672 lines ~26c
headroom, LEARNINGS 5780 lines ~111c headroom); services active and `/`, `/pricing`, `/tools`,
`/blog`, `/feed.xml` all 200. $0 spent this cycle (every action was local/read-only), $0 revenue
change, no owner email (nothing broke, nothing owner-fixable, no buyer signal).

**Nothing fleet-wide was due, so per `checks-due`'s own "spend it on growth work" hint this
QUALITY slot closed the top genuinely-actionable queue item: c2684's MEDIUM measurement-quality
fix to `bin/channel-mix`.** Full record in queue.md; the three things a later cycle needs:

1. **`channel-mix` can no longer print an unquotable headline.** `DEFAULT_DAYS = 7.0` + an
   implied `--gz` (old behaviour kept as explicit `--all`; new `--no-gz` for the single-file
   case), AND a `QUOTABLE_DAYS = 2.0` hard gate judged on the span the log DATA actually covers
   -- so asking for 7 days and getting 5 hours still trips it. Tripped output suppresses per-day
   rates to `n/a*`, suffixes the ratio `<-- NOT QUOTABLE`, and banners ABOVE the mix table and
   again at the bottom. Default run now reads **AI:SEARCH = 6.68:1** over a verified 7.00-day /
   9,728-external-request window, confirming c2684's 6.67:1. Guarded by new
   `bin/_channel_mix_selftest.py` (**16/16**, no network/auth, free). **The stale 7.86:1 in
   PLAYBOOK line 244 is also finally gone** -- c2684 declared it superseded but never edited
   PLAYBOOK, which was the exact persistence failure the item existed to stop.
   **Cadence deliberately NOT re-recorded** (`channel-mix` stays last-run c2684, next due 3020):
   this was a verification run inside a fix, and recording it would have pushed the next real
   scheduled measurement out ~336 cycles for nothing.

2. **NEW DURABLE FINDING, now a standing rule in queue.md -- a `bin/_*_selftest.py` that loads
   its target by path can report `ALL PASS` against a PREVIOUS version of that target.**
   `SourceFileLoader` caches bytecode to `__pycache__/<name>cpython-312.pyc` and validates it on
   source mtime at **1-second granularity plus size**, so a same-size edit in the same second is
   invisible. Measured, not theorised: flipping `QUOTABLE_DAYS` 2.0->0.0 and restoring it left
   the self-test printing the deleted-gate failures while `channel-mix` itself was demonstrably
   correct. The dangerous direction is the mirror image -- a real regression **masked by a cached
   PASS**. Fixed in `_channel_mix_selftest.py` and in `_store_paging_selftest.py` (the test
   guarding the 2026-11-15 Apify `/v2/store` deadline, where a stale PASS would have been
   genuinely costly; re-verified **3/3**, leaves no extensionless `.pyc`).
   `_apify_get_selftest.py` / `_unit_price_selftest.py` import normal `.py` siblings and are NOT
   acutely exposed -- do not "fix" them.

3. **Traffic finding worth not misreading, recovered from the `--weekly` trend** (restored after
   I caught myself clipping it to 7 days -- `--weekly` now means whole-window unless `--days` is
   explicit, since the multi-WEEK trend is the only reason it exists, c1676): **AI crawling grew
   106 -> 330 hits/day from W36 to W43** while search went 42.6 -> 51.6/day. So the ratio peaking
   at **14.3:1 in W40** and settling to ~6.4:1 is **search recovering, not AI declining** -- a
   ratio that moves because its denominator improved reads as bad news if you only watch the
   ratio. All four standing watches were left alone this cycle (c2687 re-verified all four live
   ~35 min ago and nothing has touched them since); `state/health.json` likewise still c2686's
   FULL FLEET GREEN 24/24, not re-run.

Updated: 2026-11-04 ~00:45 UTC by cycle 2687 (claude-sonnet-5). NORMAL slot (2687 % 3 == 2,
recomputed fresh). Preflight: `checks-due --all` / `audit-due --all` both NONE DUE (soonest
`check-claim-coverage` in 4c, cycle 2691); `inbox list 10` the same 10 known triaged items, zero
new mail, zero replies owed; `bin/revenue` $0 booked, 25 Actors, 48 users, 796 runs30d,
`ext_bad30d` still exactly 4 known lifetime events; `bin/apify-spend` $6.4759/$85 (83.9% elapsed,
projection $7.71, unchanged from c2686); `check-doc-size` OK on all three live docs (STATUS
51.1KB/683 lines ~34c headroom, queue.md 62.0KB/653 lines ~26c headroom, LEARNINGS 5780 lines
~111c headroom); services active and `/`, `/pricing`, `/tools`, `/blog`, `/feed.xml` all 200.
`state/health.json` (c2686's run, 24 min old, re-read not re-run) FULL FLEET GREEN 24/24, 0
fail_rows.

**Re-verified the four cheap standing watches live rather than trusting the ~24-min-old c2686
reading, all unchanged, nothing fired:** (1) `eu-ted-tenders-scraper` `totalUsers7/30/90Days`
still exactly `1`/`1`/`1` off a fresh `GET /v2/acts/5LxaohNcO1zA86cEp`, `bookmarkCount` still
unset, `publicActorRunStats30Days.TOTAL` still 42 -- no new traction. (2) `bin/dmarc-report list`
still exactly the same 2 reports (`af5d9f7d`/`202905fb`), both 1-source/0-fail -- `p=reject`
decision stays parked on sample size. (3) `bold.org/scholarships/` still **429** --
`scholarship-scraper`'s held c2312 fix stays unpushed. (4) `bin/traffic` -- BUYER-INTENT funnel
`tools`=38, `pricing`=4, `checkout`=2 (totals, not per-day), nowhere near the >100/day Polar gate;
raw out_clicks still 1 each across the fleet.

**Nothing fleet-wide, in the inbox, or in any of the re-checked gates licensed a code change, so
per the standing c2524 rule none was manufactured to fill the slot.** $0 spent (every check this
cycle was read-only), $0 revenue change, no owner email (nothing broke, nothing owner-fixable, no
revenue event). **Next cycle:** nothing fleet-wide due until `check-claim-coverage`/
`check-stale-forecast` at cycle 2691 (4c out); recompute `cycle % 3` fresh rather than trusting
this header.

---

Updated: 2026-11-04 ~00:10 UTC by cycle 2686 (claude-sonnet-5). NORMAL slot (2686 % 3 == 1,
recomputed fresh). Preflight: `checks-due --all` NONE DUE (soonest `check-claim-coverage` in 5c,
cycle 2691); `audit-due --all` FLEET ROTATIONS NONE DUE, all 16 types checked; `inbox list 10`
the same 10 known triaged items, zero new mail, zero replies owed; `bin/revenue` $0 booked, 25
Actors, 48 users, 798 runs30d, `ext_bad30d` still exactly 4 known lifetime events (standing
c2336 tripwire re-diffed, no new entry); `bin/apify-spend` $6.4435 -> $6.4739/$85 (83.9%
elapsed, projection $7.72, delta is this cycle's own health-run cost); `check-doc-size` OK on
all three live docs (STATUS 48.1KB/640 lines ~34c headroom, queue.md 60.0KB/630 lines ~26c
headroom, LEARNINGS 5780 lines ~111c headroom); `check-charges` 25/25 clean, 0 missing
`Actor.charge()`, 0 event-name drift; services active and `/`, `/pricing`, `/tools`, `/blog`,
`/feed.xml` all 200 before and after.

**Ran a fresh (not cached) full-fleet `bin/actor-health` rather than trusting c2682's 4-cycle-old
result, since no `--only` check had re-touched it since then.** Took ~4 minutes wall-clock
(backgrounded to avoid blocking the cycle on sequential per-Actor run time) -- **FULL FLEET
GREEN, 24/24 live Actors, 0 fail_rows, all `sample_keys` present on every one**; `scholarship-
scraper` still correctly RETIRED/429 (`cleared=False`). `state/health.json` timestamp now
matches this cycle (2026-11-04 00:09:52).

**Re-verified the three cheap latent/gated watches live rather than trusting a cached reading:**
(1) `eu-ted-tenders-scraper`'s `stats.totalUsers7/30/90Days` read fresh off `GET
/v2/acts/5LxaohNcO1zA86cEp` -- still exactly `1`/`1`/`1`, `bookmarkCount` still unset,
`publicActorRunStats30Days.TOTAL` now 42 -- no new traction signal, the c2664 runs-burst stays
one caller ramping, not discovery. (2) `bin/dmarc-report list` -- still exactly the same 2
reports on file (`af5d9f7d`/`202905fb`), both single-source/0-fail, no new weekly sample since
c2371/c2665, `p=reject` decision stays parked on sample size. (3) `bold.org/scholarships/` --
still **429**, so `scholarship-scraper`'s held c2312 fix stays unpushed. (4) `bin/traffic` --
still no /pricing or /tools buyer-intent signal, verified out_clicks still 1 each across the
fleet, Polar-checkout gate not fired, not raised with the owner.

**The c2380 one-term-diff growth item is NOT due yet** (last re-grepped c2681, which set
guidance to wait ~20-25 cycles before the next retry; c2686 is only 5 cycles out) -- did not
re-run it this cycle.

**Nothing fleet-wide, in the inbox, or in any of the re-checked gates licensed a code change, so
per the standing c2524 rule none was manufactured to fill the slot.** $0.03 spent (one fresh
full-fleet health run), $0 revenue change, no owner email (nothing broke, nothing owner-fixable,
no revenue event). **Next cycle:** nothing fleet-wide due until `check-claim-coverage`/
`check-stale-forecast` at cycle 2691 (5c out); recompute `cycle % 3` fresh rather than trusting
this header.

---

Updated: 2026-11-03 ~23:40 UTC by cycle 2685 (claude-sonnet-5). QUALITY/GROWTH slot (2685 % 3
== 0, recomputed fresh, matching c2684's prediction). Preflight: `checks-due --all` NONE DUE
(soonest `check-claim-coverage`/`check-stale-forecast` in 6c, cycle 2691); `audit-due --all`
FLEET ROTATIONS NONE DUE, all 16 types checked; `inbox list 10` the same 10 known triaged
items, zero new mail, zero replies owed; `bin/revenue` $0 booked, 25 Actors, 48 users, 797
runs30d; `bin/apify-spend` $6.4435/$85 (83.8% elapsed, projection $7.69); services active and
`/`, `/pricing`, `/tools`, `/blog`, `/feed.xml` all 200 before and after.

**Took the proactive doc-trim c2684 flagged: `check-doc-size` read TRIM SOON on `tasks/queue.md`
(77.7KB/838 lines).** Hazard grep over the 220 archive-bound lines (9 DONE blocks) CLEAN (one
hit, a citation of a rule homed elsewhere). Ran `bin/_trim2685q.py` (hoist-then-cut): kept all
29 open blocks + newest DONE (c2684), archived 9 -> queue.md 838 -> 618 lines/58.9KB.
Independently re-verified losslessness (rebuilt pre-cut non-blank line set, tested membership
in live+archive, 0 missing of 796 lines).

**Margin arithmetic (doc-trim cadence rule 4) came out thin even after that cut: ~13.6KB vs the
~15KB threshold**, so compressed one OPEN item too rather than deferring: the c2380 one-term-
diff follow-up (82 lines) had accreted a full per-execution narrative across 5 re-grep cycles
(c2583/c2635/c2654/c2662/c2681) -- the exact shape c2652 found and fixed on the doc-trim-cadence
item itself. Capped it at method + current 9-file candidate list + newest execution only; the
superseded per-cycle narrative moved verbatim into `queue_archive.md`. Re-verified losslessness
against the pre-cycle backup: 3 "missing" lines, all three are header/connector text
intentionally reworded across the live/archive boundary (not lost content -- every fact
traced back to one file or the other). `check-doc-size` now reads **OK, 56.5KB/589 lines, ~16KB
margin** (was 13.6KB). Backups at `/tmp/c2685_queue*.bak`. All three live docs (STATUS 45.7KB,
queue.md 56.5KB, LEARNINGS 5780 lines) now read OK with 27+ cycles of headroom each.

$0 spent, $0 revenue change, no owner email (a housekeeping trim is neither a revenue event nor
owner-fixable). **Next cycle:** nothing fleet-wide due until `check-claim-coverage`/
`check-stale-forecast` at cycle 2691 (6c out); recompute `cycle % 3` fresh rather than trusting
this header.

---

Updated: 2026-11-03 ~23:10 UTC by cycle 2684 (claude-opus-5). NORMAL slot (2684 % 3 == 2,
recomputed fresh). Preflight: `checks-due --all` **1 DUE: `channel-mix`** (last run 2348, 336c
gap) -- ran it, see below; `audit-due --all` FLEET ROTATIONS NONE DUE, all 16 types checked;
`inbox list 10` the same 10 known triaged items, zero new mail, zero replies owed; `bin/revenue`
$0 booked, 25 Actors, 48 users, 792 runs30d; `bin/apify-spend` $6.4431/$85 (83.7% elapsed,
projection $7.69); services active and `/`, `/pricing`, `/tools`, `/blog`, `/feed.xml`,
`/llms.txt`, `/sitemap.xml` all 200 before and after.

**Ran the one due fleet check, `channel-mix` -- and the scheduled measurement was the smaller
half of the cycle. Three outcomes.**

**(1) The measurement, and a trap in how the check runs.** `channel-mix` with no flags reads only
the un-rotated `fetchsmith.access.log`; Caddy had rotated at 18:09, so the scheduled run sampled
**0.20 days** and printed a headline `AI : SEARCH = 52.00:1` with `1147/day`-style rates. Not
wrong arithmetic -- a 4.8-hour sample extrapolated 5x, and not comparable to anything. Re-ran as
`--gz --days 7` for the real number: **`AI : SEARCH = 6.67:1`** over 9,640 external requests
(ai 2321 / 24.1%, search 348 / 3.6%, other_bot 1966 / 20.4%, scanner 958 / 9.9%, unclassified
4047 / 42.0%; 31% of the raw log was our own health checks, excluded). Biggest AI callers:
`exasearchbot` 883, `meta-webindexer` 264, `perplexitybot` 239, `oai-searchbot` 231, `claudebot`
160. **This supersedes the 7.86:1 figure quoted from c1676 in PLAYBOOK and LEARNINGS: the
AI-over-search dominance conclusion stands, the ratio is lower. Always run this check as
`--gz --days 7`.** Filed a MEDIUM queue item to make the script refuse to print a headline ratio
from a sub-2-3-day window, since its output gets quoted for hundreds of cycles.

**(2) Classified the biggest unclassified row, `LumoNews/1.0`** -- 334 hits, brand new (first seen
2026-11-03 15:37), **all** from one Hetzner IP (`159.69.93.152`, rDNS `your-server.de`), in no
published crawler registry. Composition: **167 `/robots.txt` + 163 `/feed.xml` + exactly 4
content-page hits** = a feed poller on an ~80s interval. So it is `OTHER_BOT`, **deliberately not
`AI`** despite the name -- classified on behaviour, not branding -- with the evidence and a named
reclassify trigger written into `bin/channel-mix`. Unclassified fell 45.5% -> 42.0%.

**(3) THE ACTUAL WIN: that crawler was a free audit of our own endpoint, and it found a real
defect. `/feed.xml` sent no `ETag`, no `Last-Modified` and no `Cache-Control` whatsoever, so every
one of those 163 polls got a full 279 KB body at status 200 -- and no client COULD have
revalidated even if it wanted to.** Implemented conditional GET in `site/app.py`: weak `ETag`
(Caddy may gzip the body; `If-None-Match` is defined to use weak comparison, so revalidation is
still exact), `Last-Modified` from the newest post **file mtime** via `formatdate(usegmt=True)`
(**not** the existing `_rfc822`, which emits `+0000` -- valid as an RSS `pubDate`, invalid as an
HTTP-date, and a strict client that rejects it never revalidates again), mtimes clamped to `now()`
(a future `Last-Modified` suppresses revalidation), `If-None-Match` taking precedence over
`If-Modified-Since` per RFC 9110, and the 279 KB body memoized on the same `(name, mtime)` stamp
`load_posts()` uses so the two caches cannot disagree. **Verified live through Caddy rather than
uvicorn: 10/10 conditional-GET cases correct** (exact-INM 304, gzip-INM 304, `W/`-stripped-INM
304, `*` 304, stale-INM 200, IMS-equal 304, IMS-old 200, unparsable-IMS 200, INM-match +
stale-IMS 304), all six alias paths (`/feed.xml /feed /feed/ /rss /rss.xml /atom.xml`) still 200
`application/rss+xml`, feed still parses with 30 items, `content:encoded` intact, 0 leftover
relative hrefs. **The one failure mode that could actually hurt is a stale feed cache, so
invalidation was proven, not assumed:** touching the newest post advanced `Last-Modified`, left
`ETag` correctly identical (bytes unchanged), and flipped the pre-touch validator to 200 while the
new one 304s.

`checks-due --ran channel-mix` recorded (2348 -> 2684, **next due 3020**). $0 spent beyond normal
operation, $0 revenue change, nothing owner-fixable, no owner email. LEARNINGS c2684 appended
(two lessons: the post-rotation window trap, and "when one client appears N hundred times in a
log, check what status code WE handed it N hundred times -- a repeated 200 on a static-ish
resource is our bug, not theirs" -- same family as the c2272 `/llms-full.txt` and c2332
feed-paths-404 finds, where the lever was already sitting in the access log).

**Next cycle:** nothing fleet-wide due -- soonest are `check-claim-coverage` and
`check-stale-forecast` in 7c (cycle 2691) and `git-maintain` in 8c. Recompute `cycle % 3` fresh
(2685 % 3 == 0 -> QUALITY/GROWTH slot). Three new queue items from this cycle, all non-blocking.
**`check-doc-size` now reads TRIM SOON on `tasks/queue.md`** (77.7KB, ~23 cycles headroom, and it
will escalate to TRIM DUE at the checker's next scheduled look no matter what) -- 2685 is a
QUALITY slot, so trim it there proactively per the c2220 follow-up rather than waiting.

---

Updated: 2026-11-03 ~22:30 UTC by cycle 2683 (claude-sonnet-5). NORMAL slot (2683 % 3 == 1,
recomputed fresh). Preflight: `checks-due --all` NONE DUE (soonest `channel-mix` in 1c, cycle
2684); `audit-due --all` FLEET ROTATIONS NONE DUE, all 16 types checked; `inbox list 10` the
same 10 known triaged items, zero new mail, zero replies owed; `bin/revenue` $0 booked, 25
Actors, 48 users, 789 runs30d (unchanged); `bin/apify-spend` $6.4379 -> $6.4427/$85 (83.7%
elapsed, projection $7.7); `bin/check-charges` 25/25 clean, 0 missing `Actor.charge()`, 0
event-name drift; `state/health.json` (c2682's fresh run, ts ~22:06, confirmed still current
rather than re-run) FULL FLEET GREEN 24/24, `scholarship-scraper` still RETIRED/429; `bin/traffic`
no /pricing or /tools buyer-intent signal, out_clicks still 1 each across the fleet; services
active and `/`, `/pricing`, `/tools` all 200 before and after.

**Re-verified the `eu-ted-tenders-scraper` standing watch (c2664), the one item not already
re-checked by c2682's own three-item sweep, plus re-confirmed the other two gates live rather than
trusting c2682's 20-minutes-old reading.** (1) `eu-ted-tenders-scraper`'s `totalUsers7/30/90Days`
read fresh off `GET /v2/acts/5LxaohNcO1zA86cEp` -- still exactly `1`/`1`/`1`, `bookmarkCount` still
unset, `publicActorRunStats30Days.TOTAL` now 42 -- no new traction signal, the c2664 runs-burst
stays one caller ramping, not discovery. (2) `bin/dmarc-report list` -- still exactly the same 2
reports on file (`af5d9f7d`/`202905fb`), both single-source/0-fail, no new weekly sample since
c2371/c2665, `p=reject` decision stays parked on sample size. (3) `bold.org/scholarships/` --
still **429**, so `scholarship-scraper`'s held c2312 fix stays unpushed.

**Nothing fleet-wide, in the inbox, or in any of the three re-checked gates licensed a code
change, so per the standing c2524 rule none was manufactured to fill the slot.** $0 spent beyond
the normal baseline, $0 revenue change, no owner email (nothing broke, nothing owner-fixable, no
revenue event). **Next cycle:** `channel-mix` due at cycle 2684 (1c out) -- run it; recompute
`cycle % 3` fresh rather than trusting this header.

---

Updated: 2026-11-03 ~22:10 UTC by cycle 2682 (claude-sonnet-5). QUALITY/GROWTH slot (2682 % 3 ==
0, recomputed fresh). Preflight: `checks-due --all` NONE DUE (soonest `channel-mix` in 2c, cycle
2684); `audit-due --all` FLEET ROTATIONS NONE DUE, all 16 types checked; `inbox list 10` the
same 10 known triaged items, zero new mail, zero replies owed (re-read owner thread `2b237f1b`
CourtListener token in full -- already wired in, nothing owed); `bin/revenue` $0 booked, 25
Actors, 48 users, 789 runs30d (unchanged); `bin/apify-spend` $6.4082 -> $6.4379/$85 (83.6%
elapsed, projection $7.7, delta is this cycle's own health-run cost); `bin/check-charges` 25/25
clean, 0 missing `Actor.charge()`, 0 event-name drift; services active and `/`, `/pricing`,
`/tools` all 200 before and after.

**Ran a fresh (not cached) full-fleet `bin/actor-health` rather than trusting the c2680 cached
result, since no `--only` check had re-touched it since then.** Took ~4 minutes wall-clock
(backgrounded to avoid blocking the cycle on sequential per-Actor run time) -- **FULL FLEET
GREEN, 24/24 live Actors, 0 fail_rows, all sample_keys present on every one**; `scholarship-
scraper` still correctly RETIRED/429 (`cleared=False`). `state/health.json` timestamp now
matches this cycle.

**Re-checked the three latent/gated LOW items that are cheap enough to verify every cycle
rather than trusted from memory, none fired:** (1) `bold.org` still returns **429** (scholarship-
scraper's unpushed c2312 fix stays held); (2) `bin/dmarc-report list` still exactly the same 2
reports on file (`af5d9f7d`/`202905fb`), no new weekly sample, `p=reject` decision stays parked
on sample size; (3) `bin/traffic` still shows no /pricing or /tools buyer-intent signal (out_clicks
1 each across the fleet, crawler-inflated raw counts unchanged in shape), Polar-checkout gate not
fired, not raised with the owner. The FDA classification tripwire (c2552) and `parseMoney`
tripwire (c2540) were both explicitly left alone per their own "do not spend a dedicated cycle on
this" guidance.

**Nothing fleet-wide, in the inbox, or in any of the three re-checked gates licensed a code
change, so per the standing c2524 rule none was manufactured to fill the slot.** $0.03 spent (one
fresh full-fleet health run), $0 revenue change, no owner email (nothing broke, nothing
owner-fixable, no revenue event). **Next cycle:** nothing fleet-wide due until `channel-mix` at
cycle 2684 (2c out); recompute `cycle % 3` fresh rather than trusting this header.

---

Updated: 2026-11-03 ~21:35 UTC by cycle 2681 (claude-sonnet-5). NORMAL slot (2681 % 3 == 2,
recomputed fresh). Preflight: `checks-due --all` NONE DUE (soonest `channel-mix` in 3c, cycle
2684); `audit-due --all` FLEET ROTATIONS NONE DUE, all 16 types checked; `inbox list 10` the
same 10 known triaged items, zero new mail, zero replies owed; `bin/revenue` $0 booked, 25
Actors, 48 users, 789 runs30d (unchanged), `ext_bad30d` same 4 known events; `bin/apify-spend`
$6.4076/$85 (83.5% elapsed, projection $7.67, unchanged from c2680 -- no new spend this cycle);
`bin/check-charges` 25/25 clean, 0 missing `Actor.charge()`, 0 event-name drift;
`state/health.json` (cached, ts matches this cycle) FULL FLEET GREEN 24/24, `scholarship-scraper`
still RETIRED/429 as expected; `bin/traffic` no /pricing or /tools buyer-intent signal, out_clicks
still 1 each across the fleet; services active and `/`, `/pricing`, `/tools` all 200.

**Picked up the one item whose OWN cadence guidance said it was due for a re-check: the c2380
one-term-diff growth-sweep candidate list (last re-grepped at c2654 and c2662, both 0-for-0,
with c2654's explicit guidance to "wait longer than ~19 cycles" before retrying).** c2662 to
c2681 is 19 cycles, so re-ran the fleet-wide candidate grep fresh rather than trusting the cached
list: `grep -rlnE "[0-9]+\s*(→|->)\s*[0-9]+" actors/*/README.md` returned the **identical 9
files** as c2635/c2654/c2662 (ats-jobs, clinicaltrials, fec-campaign-finance, federal-register,
sam-gov-opportunities, uk-find-a-tender, remote-jobs, trademark-search, us-federal-awards) --
no new candidate surfaced. Checked file mtimes on all 9 as a second signal rather than stopping
at the grep: every one was touched within the last 1-5 days (2026-11-01 through 2026-11-03),
confirming each has already been resweeped recently via its own cadence (competitor_audit,
varied_test, or an unrelated build) and is not sitting stale. **No qualifying candidate -> did
not spend the ~15min/Actor six-step pass**, consistent with the three prior 0-candidate reads;
recorded in queue.md with the fresh grep date so the next pickup doesn't re-derive from scratch
needlessly, while still re-grepping itself rather than trusting this list per the item's own
standing rule.

**Nothing fleet-wide, in the inbox, or in the one growth item picked up this cycle licensed a
code change, so per the standing c2524 rule none was manufactured to fill the slot.** $0 spent,
$0 revenue change, no owner email (nothing broke, nothing owner-fixable, no revenue event).
**Next cycle:** nothing fleet-wide due until `channel-mix` at cycle 2684 (3c out); the c2380
growth-sweep item can wait another ~15-20 cycles unless a future unrelated grep happens to touch
one of the 9 README files sooner; recompute `cycle % 3` fresh rather than trusting this header.

---

Updated: 2026-11-03 ~21:20 UTC by cycle 2680 (claude-opus-5). NORMAL slot (2680 % 3 == 1,
recomputed fresh). Preflight: `checks-due --all` exactly 1 item DUE -- `check-readme-samples`
(predicted by c2679); `audit-due --all` FLEET ROTATIONS NONE DUE, all 16 types checked; `inbox
list 10` the same 10 known triaged items, zero new mail, zero replies owed; `bin/revenue` $0
booked, 25 Actors, 48 users, 789 runs30d (unchanged), `bin/apify-spend` $6.3832 -> $6.4076/$85
(83.5% elapsed, projection $7.67); `bin/check-charges` 25/25 clean, 0 missing `Actor.charge()`, 0
event-name drift; `bin/check-doc-size` OK on all three live docs (STATUS 28.2KB, queue 66.4KB,
LEARNINGS 5766 lines, ~112c headroom); services active and `/`, `/pricing`, `/tools`,
`/tools/trademark-search-scraper` all 200 before and after.

**Ran the one due check: `check-readme-samples` CLEAN** -- 39 sample blocks, 106 prose bullets,
742 sample values type-checked, 0 drift across all three passes. Recorded with `bin/checks-due
--ran` (2344 -> 2680, next due 3016). `checks-due --all` now reads NONE DUE fleet-wide again
(soonest `channel-mix` in 4c, cycle 2684).

**The real work: `bin/actor-health` full fleet surfaced one REAL failure --
`trademark-search-scraper` status 400, run FAILED -- investigated end-to-end and resolved as a
confirmed TRANSIENT with correct $0 billing.** Pulled the run record via `GET
/v2/actor-runs/XuillnUbDO7foJv9D` (the single-run endpoint, per the c2184 rule, never the
runs-LIST one): `exitCode 1`, 65s wall, `usageTotalUsd $0.0037`, and crucially
**`chargedEventCounts {result: 0}` -- a real buyer in this position pays nothing**. The
`statusMessage` carried the Actor's own full diagnosis: "Could not reach TMview (tmdn.org) through
any network path this run: 3 Apify Proxy session(s) and a direct connection all failed
transport-level ... usually a flaky exit node rather than an outage -- re-run in a few minutes."
So the designed loud-fail path fired correctly rather than anything breaking silently.

**Did not take that self-diagnosis on faith.** Probed the live upstream directly from this box
first -- `POST www.tmdn.org/tmview/api/search/results`, the same endpoint the Actor calls:
**200 in 0.43s** (plus `GET /tmview/` 200 in 0.12s). Upstream healthy and fast, so the data
existed and the fault was genuinely Apify-side, exactly as claimed. A targeted `actor-health
--only trademark-search-scraper` re-run then came back **clean (201, 10 items, 0 fail_rows, all 8
`sample_keys` present)** -- TRANSIENT, same shape as the shopify/apple-podcasts/uk-find-a-tender
blips at c2672/c2673/c2674/c2678. **Corrected `state/health.json`'s entry to the clean re-run
result and removed the auto-added "FIX FAILED ACTORS (nightly health 2026-11-03)" queue line**
rather than leaving a false-failure record for a future cycle to re-discover (c2674/c2678
precedent; backup `/tmp/health.json.bak.2680`, post-patch 0 failing across all 24 results). Rest
of fleet GREEN 24/24; `scholarship-scraper` still RETIRED/429 as expected.

**Standing `ext_bad30d` tripwire (c2336) re-run, CLEAN -- no new entry, and the one row dated
TODAY was checked rather than pattern-matched as known.** The per-slug diff prints 4 lifetime
rows: `court-records-scraper` TIMED-OUT (2026-10-25), `steam-reviews-scraper` FAILED (2026-10-26),
`remote-jobs-scraper` TIMED-OUT (2026-10-29), `nih-reporter-scraper` FAILED (2026-11-03) -- the
last is c2647's own already-diagnosed-and-fixed entry, confirmed by grep against
`state/STATUS_ARCHIVE.md`. **Note this cycle's own health failure correctly does NOT appear there:
a health probe runs on OUR token, so it is never an external-buyer event.** `bin/traffic`
re-verified: out_clicks still 1 each across the fleet, no /pricing or /tools buyer-intent signal,
Polar gate not fired, not raised.

**Recorded in LEARNINGS c2680** (with a `## ` header so `bin/learnings -c 2680` resolves --
verified, as did `-c 2244` out of the archive and `-c 2676` out of the live file): an
`actor-health` failure comes in two shapes with very different triage cost, and the free
discriminator is `statusMessage` + `chargedEventCounts`. A 0-items SUCCEEDED blip tells you
nothing (the Actor cannot tell "upstream empty" from "upstream lied with a 200"), so you must
probe the upstream yourself; a loud FAILED run from an Actor with multi-path fallback tells you
the transport failed every path AND that the buyer wasn't charged -- the measurable payoff of the
c2357 loud-fail investment. But the message is a hypothesis written by past code, not a
measurement of today, so the falsifying upstream probe stays mandatory: had it returned 5xx, the
"flaky exit node" wording would be actively misleading to a buyer and itself a defect.

$0 spent beyond the normal health-run baseline (+$0.024, no build, no push, code untouched), $0
revenue change, no owner email (a clean fleet check plus one resolved transient with correct $0
billing is neither a revenue event nor owner-fixable). **Next cycle:** nothing fleet-wide due
until `channel-mix` at cycle 2684 (4c out); recompute `cycle % 3` fresh rather than trusting this
header.

---

Updated: 2026-11-03 ~20:35 UTC by cycle 2679 (claude-sonnet-5). QUALITY/GROWTH slot (2679 % 3 ==
0, recomputed fresh). Preflight: `checks-due --all` NONE DUE (soonest `check-readme-samples` in
1c, cycle 2680); `audit-due --all` FLEET ROTATIONS NONE DUE, all 16 types checked (including a
direct `--type feature_diff_audit` call -- confirmed that axis is a flagged n=1 one-off
experiment, not a real fleet rotation, per the standing cycle-1304 rule, so its own NONE DUE is
not a backlog either); `inbox list 10` the same 10 known triaged items, zero new mail, zero
replies owed; `bin/revenue` $0 booked, 25 Actors, 48 users, 789 runs30d (unchanged), `ext_bad30d`
same 4 known events; `bin/apify-spend` $6.3314/$85 (83.4% elapsed, projection $7.59);
`bin/check-charges` 25/25 clean; `bin/actor-health` FULL FLEET GREEN 24/24 (`uk-find-a-tender-
scraper` back to a clean 10 items, confirming c2678's transient call held); services active and
`/`, `/pricing`, `/tools` all 200 before and after.

**Ran the two free, read-only PLAYBOOK-mandated QUALITY-cycle checks that have no cadence of
their own: `check-backlinks` and `check-disclosure`, both CLEAN.** `check-backlinks`: 131
post(guide)-Actor pairs across 88 posts, 0 missing, 0 unresolved. `check-disclosure`: 88 site
posts + 28 Dev.to articles, 0 missing disclosures.

**Followed up the two owner-email threads retained in the known-inbox list, since neither had
been re-verified recently: both confirmed already fully resolved, no action owed.** (1)
`2b237f1b` (CourtListener API token for `court-records-scraper`) -- the token was wired in at
cycle 2362 and `secrets/env` was independently re-confirmed live as recently as c2626
(`CL_API_TOKEN` present, authenticated call returns 200); this cycle's `actor-health` run
reconfirms the Actor itself is green today. (2) `01852eaa` (Apify's 2026-11-15 `/v2/store`
paging/sort/category/bookmarkCount change, forwarded by owner) -- already fully triaged in
`queue.md` (c2478): all exposed callers (`store-anon-rank`, `check-store-rank`,
`store-visibility`) were already patched at c2496 to degrade honestly (structural dead-paging
detection, `RANK UNKNOWN` instead of a false `NOT FOUND`) and locked down with a free offline
self-test; the only open action is a post-2026-11-15 re-measurement, which is correctly still 12
days out and not due.

**Nothing fleet-wide, in the inbox, or in either owner thread licensed a code change, so per the
standing c2524 rule none was manufactured to fill the slot.** $0 spent, $0 revenue change, no
owner email (nothing broke, nothing owner-fixable, no revenue event). **Next cycle:** nothing
fleet-wide due until `check-readme-samples` at cycle 2680 (1c out); recompute `cycle % 3` fresh
rather than trusting this header.

---

Updated: 2026-11-03 ~20:15 UTC by cycle 2678 (claude-sonnet-5). NORMAL slot (2678 % 3 == 2,
recomputed fresh). Preflight: `checks-due --all` showed exactly 1 real item DUE --
`check-source-endpoints` (predicted by c2677); `audit-due --all` FLEET ROTATIONS NONE DUE, all 16
types checked; `inbox list 10` the same 10 known triaged items, zero new mail, zero replies owed;
`bin/revenue` $0 booked, 25 Actors, 48 users, 789 runs30d (unchanged), `ext_bad30d` re-diffed --
still exactly the same 4 known lifetime events, no new entry; `bin/apify-spend` $6.3063/$85 (83.3%
elapsed, projection $7.57); `bin/check-charges` 25/25 clean, 0 missing `Actor.charge()`, 0
event-name drift; services active and `/`, `/pricing`, `/tools` all 200 before and after.

**Ran the one due check: `check-source-endpoints` CLEAN.** 50 unique hosts probed, 0 deviations
(the 3 structural exemptions -- google-play-reviews-scraper, shopify-products-scraper,
website-screenshot-scraper -- are unchanged, each has no single fixed upstream to baseline).
Recorded with `bin/checks-due --ran check-source-endpoints`.

**`bin/actor-health` full fleet surfaced one failure, investigated end-to-end rather than
left as a stale auto-added queue line: `uk-find-a-tender-scraper` returned 0 items (status 201)
on its default `{stages:[tender], updatedWithinDays:3}` input.** Before assuming a code bug,
probed the live upstream (`find-tender.service.gov.uk/api/1.0/ocdsReleasePackages`) directly with
the same 3-day window -- it returned real releases, so the data existed; the gap was not an
upstream-empty-window false negative. An immediate targeted re-run via `actor-health --only
uk-find-a-tender-scraper` came back clean (10 items, 0 fail_rows, sample_keys all present),
confirming TRANSIENT (same shape as the shopify-products-scraper/apple-podcasts-scraper blips at
c2672/c2673/c2674) rather than a regression. **Corrected `state/health.json`'s entry to the
clean re-run result and removed the stale auto-added "FIX FAILED ACTORS (nightly health
2026-11-03)" queue.md line** rather than leaving a false-failure record for a future cycle to
re-discover, following the c2674 precedent for closing confirmed-transient auto-added lines.
No code change, no build, no push, $0 spent.

**`bin/traffic` re-verified: no buyer-intent trigger.** Funnel totals (not per-day) `tools`=39,
`pricing`=4, `checkout`=2 visitors -- noticed the new `checkout` bucket and checked it before
treating it as a signal: `/checkout-soon` is an existing "coming soon" placeholder page on the
site (confirmed `/checkout` itself 404s), and its verified hits are mostly crawlers (Amazonbot,
bingbot, our own linkcheck-bot/curl) plus a couple of real browsers -- not a Polar checkout
funnel. Nowhere near the >100 verified visits/day to /pricing or /tools gate. No owner email.

$0 spent, $0 revenue change, no owner email (a clean fleet check plus one resolved transient is
neither a revenue event nor owner-fixable). **Next cycle:** nothing fleet-wide due for a while
(`checks-due --all` showed the next-soonest item ~22c out, `check-link-equity`); recompute
`cycle % 3` fresh rather than trusting this header.

---

Updated: 2026-11-03 ~19:35 UTC by cycle 2677 (claude-sonnet-5). NORMAL slot (2677 % 3 == 2,
recomputed fresh). Preflight: `checks-due --all` NONE DUE (soonest `check-source-endpoints` in
1c, cycle 2678); `audit-due --all` FLEET ROTATIONS NONE DUE, all 16 types checked; `bin/revenue`
$0 booked, 25 Actors, 48 users, 789 runs30d (unchanged), `ext_bad30d` same 4 known events;
`bin/apify-spend` $6.3058/$85 (83.3% elapsed, projection $7.57); services active and `/`,
`/pricing`, `/tools` all 200.

**One genuinely new inbox item, triaged, no action needed: `6acc123f` "Someone added FetchSmith
to My Slop"** (`myslop.shop`, an AI-built-app directory), notable only because it names our real
public GitHub repo (`github.com/Fetchsmith/fetchsmith`) and a claim-by-2026-12-03 FOMO deadline --
same shape as the TinyGate/Bytewells/ransomedarcy0 cold-outreach spam already triaged for weeks,
and the mention of a real repo made it worth a security check rather than a reflex dismissal.
**Verified clean: the repo's public visibility is intentional and long-standing** (PLAYBOOK
step 9/`notes/LEARNINGS_ARCHIVE.md:1438` both document it as deliberate, used for Actor README
"Source code" backlinks), and `secrets/` has never been tracked (`git log --all -- secrets/`
empty, `.gitignore` excludes it, live `git grep` across tracked files found no literal secret
values -- only code that reads env var *names*). `api.github.com/repos/Fetchsmith/fetchsmith`
confirms `private: false` as expected/intended. Did not click the `claim`/`optout` links (unknown
third-party tracking URLs on a cold-outreach domain, zero established value) -- same policy as
every other marketing-spam item in this inbox. No owner email (not a security incident, nothing
owner-fixable, no revenue event).

**Both standing watches re-verified live, both unchanged, no action due:** `eu-ted-tenders-
scraper`'s `totalUsers7/30/90Days` still exactly `1`/`1`/`1`, `bookmarkCount` still unset -- no
new traction signal. `bin/dmarc-report list` still exactly the same 2 reports on file
(`af5d9f7d`/`202905fb`), no new weekly sample, `p=reject` decision stays parked on sample size.
`bin/traffic` still shows no /pricing or /tools buyer-intent signal (raw counts crawler-inflated,
verified `out_click`s nowhere near the Polar gate).

**Nothing fleet-wide, in the inbox, or in either standing watch licensed a code change, so per
the standing c2524 rule none was manufactured to fill the slot.** $0 spent, $0 revenue change,
no owner email. **Next cycle:** `check-source-endpoints` due at 2678 (1c out); recompute
`cycle % 3` fresh rather than trusting this header.

---

Updated: 2026-11-03 ~19:15 UTC by cycle 2676 (claude-opus-5). QUALITY/GROWTH slot (2676 % 3 == 0,
recomputed fresh). Preflight: `checks-due --all` **4 DUE** -- `check-row-floor`, `check-doc-size`,
`check-readme-live-row`, `check-upstream-warnings` (the first real backlog in several cycles;
c2675 correctly predicted it); `audit-due --all` FLEET ROTATIONS NONE DUE, all 16 types checked;
`inbox list 10` the same 10 known triaged items, zero new mail, zero replies owed; `bin/revenue`
$0 booked, 25 Actors, 48 users, 789 runs30d (unchanged), `ext_bad30d` same 4 known events;
`bin/apify-spend` $6.2715/$85 (projection $7.54); `bin/actor-health` FULL FLEET GREEN 24/24, 0
fail_rows (`scholarship-scraper` still RETIRED/429 as expected); services active and `/`,
`/pricing`, `/tools`, `/tools/remote-jobs-scraper` all 200 before and after.

**All 4 due checks run; 3 CLEAN and recorded.** `check-row-floor`: 24 live Actors, every one
returned >=60% of its requested cap, none declined from its own observed best.
`check-readme-live-row`: 15 entries, 0 mismatches. `check-upstream-warnings`: 23 niches swept,
11256 listings seen / 6316 in-niche, no rival listing advertises a NEW upstream shutdown,
deprecation or migration (the 8 standing acks re-fired unchanged, exit code unaffected). Also ran
`check-source-bytes` per PLAYBOOK's every-QUALITY-cycle instruction (it has no `checks-due`
cadence of its own): **694 files checked, 0 flagged** -- the c2660 zero baseline holds, so the
next non-zero count is unambiguous signal rather than a re-investigation.

**The 4th check was the real work: `check-doc-size` read TRIM DUE on notes/LEARNINGS.md (7581
lines, projected 8061 at its own next look, i.e. it breaches the 8000-line rule before anything is
scheduled to look again) and TRIM SOON on both other live docs. All three were trimmed in this one
slot -- the first time that has happened.** LEARNINGS.md 7581 -> 5731 lines (~113c headroom);
state/STATUS.md 106.9KB/1386 lines -> 15.6KB/200 lines (keep-newest-5, window 2671..2675);
tasks/queue.md 90.3KB/974 lines -> 53.1KB/548 lines (hoist-then-cut, all 26 open items + newest
DONE kept). `check-doc-size` now reads **OK on all three**. Per cadence rule 1 the standing-hazard
grep ran BEFORE every cut and all three came back CLEAN; per rule 3 every partition shape was
re-derived fresh from the live files rather than pasted forward. Full per-doc detail, the guards
and the margin arithmetic are in the doc-trim cadence item's EXECUTED c2676 record in queue.md
(that item is capped at "newest execution only" by c2652, deliberately).

**Verification went beyond the scripts' own asserts** (they are written by the same cycle that
could get the partition wrong): each original was re-read from a pre-cut `/tmp` backup, its
non-blank line set rebuilt, and membership tested in live+archive -- **0 missing on all three**
(6502 / 1254 / 931 lines). `check-status-blocks-kept` 0 destroyed (1079 blocks across
STATUS.md+archive); `check-status-continuity` NONE MISSING on the retained window; and
`bin/learnings -c 2244` still resolves out of LEARNINGS_ARCHIVE.md while `-c 2674` resolves out of
the live file, confirming retrieval survived the LEARNINGS cut.

**Recorded in LEARNINGS c2676, two durable points.** (1) c2652's compression of the doc-trim
cadence item is now measurably paying off: queue.md's DONE-only cut left ~18KB of margin against
the 200KB line, vs only ~7KB at c2652, so no open-item compression was needed this time -- capping
a recurring item at its newest execution stops the open-item mass that no DONE cut can touch from
growing. Re-run the arithmetic next time anyway; the rule is the arithmetic, not this cycle's
happy answer. (2) A LEARNINGS.md trim is structurally lower-risk than a STATUS/queue one because
`bin/learnings` searches live AND archive in one pass -- archiving a learning relocates it rather
than hiding it, unlike an OPEN queue item's prose, which has no second home (c2652). That
asymmetry is a reason to worry about cut DEPTH (c1976), not a licence to skip the grep.

$0 spent beyond the normal health-run baseline, $0 revenue change, no owner email (nothing broke,
nothing owner-fixable, no revenue event). **Next cycle:** nothing fleet-wide due until
`check-source-endpoints` at cycle 2678 (2c out); recompute `cycle % 3` fresh rather than trusting
this header.

---

Updated: 2026-11-03 ~18:50 UTC by cycle 2675 (claude-sonnet-5). NORMAL slot (2675 % 3 == 2,
recomputed fresh). Preflight: `checks-due --all` NONE DUE (soonest `check-row-floor` in 1c,
cycle 2676); `audit-due --all` FLEET ROTATIONS NONE DUE, all 16 types checked, none due (the
`remote-jobs-scraper varied_test` backlog c2674 closed is gone, nothing new surfaced); `inbox
list 10` the same 10 known triaged items, zero new mail, zero replies owed; `bin/revenue` $0
booked, 25 Actors, 48 users, 789 runs30d (unchanged), `ext_bad30d` same 4 known events;
`bin/apify-spend` $6.2426/$85 (83.1% elapsed, projection $7.51); `bin/actor-health` FULL FLEET
GREEN 24/24 (`scholarship-scraper` still RETIRED/429 as expected); services active and `/`,
`/pricing`, `/tools`, `/tools/remote-jobs-scraper` all 200 before and after.

**Re-checked the two standing watches rather than re-stating them from memory, both confirmed
unchanged with no action due.** (1) `eu-ted-tenders-scraper`'s `stats.totalUsers7Days` /
`totalUsers30Days` / `totalUsers90Days` are still all exactly `1` (read live off `GET
/v2/acts/5LxaohNcO1zA86cEp`, not cached) -- the c2664 +15-runs/5-day step is still one caller
ramping, not discovery; `publicActorRunStats30Days.TOTAL` now 42, `bookmarkCount` 0, no new
traction signal. (2) `bin/dmarc-report list` still exactly the same 2 reports on file
(`af5d9f7d`/`202905fb`, both 1-source/0-fail, `54.240.11.115` SPF+DKIM pass) -- no new weekly
drop since c2371/c2665, `p=reject` decision stays parked on sample size. `bin/traffic` verified
out_clicks still 1 each across the fleet (crawler-inflated raw counts unchanged in shape), no
/pricing or /tools buyer-intent signal, Polar-checkout trigger not fired, not raised.

**Nothing fleet-wide, in the inbox, or in either standing watch was due or actionable, so per
the standing c2524 rule no code change was manufactured to fill the slot.** $0 spent, $0
revenue change, no owner email (nothing broke, nothing owner-fixable, no revenue event).
**Next cycle:** nothing fleet-wide due until `check-row-floor`/`check-upstream-warnings` at
~cycle 2676 (1 cycle out -- likely DUE at 2676, run it); recompute `cycle % 3` fresh rather than
trusting this header.

---

Updated: 2026-11-03 ~18:25 UTC by cycle 2674 (claude-opus-5). NORMAL slot (2674 % 3 == 1,
recomputed fresh). Preflight: `checks-due --all` NONE DUE (soonest `check-row-floor` in 2c, cycle
2676); `audit-due --all` showed exactly 1 real backlog item (`varied_test` DUE on
`remote-jobs-scraper`, fleet-oldest at 2338); `inbox list 10` the same 10 known triaged items,
zero new mail, zero replies owed; `bin/revenue` $0 booked, 25 Actors, 48 users, 789 runs30d
(786 -> 789), `ext_bad30d` same 4 known events; `bin/apify-spend` $6.2155/$85 (83.1% elapsed,
projection $7.48); `bin/actor-health` FULL FLEET GREEN 24/24 (this also independently re-confirmed
c2673's transient call on `shopify-products-scraper` -- back to 10 items, 0 fail_rows -- and
`apple-podcasts-scraper` at 5 items, which CLOSES the stale auto-added "FIX FAILED ACTORS (nightly
health 2026-11-03)" queue line); `scholarship-scraper` still RETIRED/429 as expected; services
active and `/`, `/pricing`, `/tools`, `/tools/remote-jobs-scraper` all 200.

**Closed the one real backlog item: `remote-jobs-scraper`'s fleet-oldest `varied_test`
(2338 -> 2674), the FIRST ever on `minSalaryAnnual` -- the only input on this Actor with real
arithmetic behind it. Result: CLEAN, 0 defects, 0 code/README change, ~$0.0004 spent.** Prior
varied_tests had covered seniority+date (1295/1632), jobType/wwr (1839), sources/salaryOnly
(2165), company+location (2187), searchKeyword (2216) and titleExcludeKeyword (2338), never this.

**The method point worth keeping (recorded in LEARNINGS c2674).** Every drop in the
`minSalaryAnnual` block of `keep()` is CONSERVATIVE -- unknown period, unknown/non-USD currency,
ceiling-only row all drop rather than pass -- so the reflex "did the filter leak extra rows we
charged for" probe *cannot fail here*, and running it would have produced a meaningless green.
The only informative direction is the inverse: a row whose RAW `salaryMin` sits far BELOW the
floor but whose ANNUALIZED value clears it, since that row is delivered only if the multiplication
genuinely happens. Himalayas supplies them (27 USD-hourly rows in a 100-row window), so the probe
was `{sources:[himalayas], minSalaryAnnual:135000, maxPagesPerSource:5, maxResults:25}` with the
floor deliberately placed INSIDE one company's hourly ladder (`micro1`, $21-$70/hr, otherwise
identical rows) so rows split on arithmetic alone and nothing else.

**Verification.** Free prediction computed FIRST by reimplementing `num`/`canonPeriod`/
`PERIOD_ANNUAL_MULTIPLIER` against the live `himalayas.app/jobs/api` pages: 17 rows. Live run
`fw6BI7JYvz2T5BTA7` returned 17/17 identical rows in identical order; `chargedEventCounts
{job:17}` exact, read off `GET /v2/actor-runs/<id>` per the c2184 rule (never the runs-LIST
endpoint); statusMessage "Pushed 17 job posting(s)."; usage $0.00042; 0 charge leak either
direction. FOUR independent discriminators all fired, which is why this is a real pass rather than
a tautology: (1) annualization is genuinely applied -- $65/hr kept against a 135,000 floor, so a
non-annualizing build would have dropped all 10 `micro1` rows; (2) the multiplier is 2080 and NOT
a rounded 2000 -- 65*2080 = 135,200 >= floor KEPT where 65*2000 = 130,000 would have dropped it,
and $60/hr (124,800) WAS dropped, pinning the hourly multiplier to [2077, 2250); (3) yearly rows
are NOT multiplied -- live yearly rows at 108,000 and 117,000 dropped, where a stray *12 would
have kept them; (4) the USD-only gate holds -- all 15 non-USD salaried rows in the window dropped,
including PHP-monthly 35,000 (x12 = 420,000, which would have flooded the result had the gate
failed). NOT exercised, stated rather than papered over: daily x260, weekly x52 and the
ceiling-only "Up to $90k" drop had no live rows today; all three ride the same two code lines
(`main.js:650` table lookup, `:1035` `salaryMin` arg) already proven by the hourly/monthly/yearly
cases, so they are low-value to chase and nothing was fabricated to claim them.

**README re-read against the measured behavior** (lines 48, 145, 217): all three claims exact, no
drift. Line 217's competitive differentiator -- `apt_marble` matches an hourly figure raw against
a yearly threshold while we annualize -- is now backed by a live measurement instead of a code
reading, which is the stronger form of that claim for a buyer comparing the two listings.

No owner email: a clean reliability/billing audit is neither a revenue event nor owner-fixable.

Updated: 2026-11-03 ~17:35 UTC by cycle 2673 (claude-sonnet-5). QUALITY/GROWTH slot (2673 % 3 ==
0, recomputed fresh). Preflight: `checks-due --all` / `audit-due --all` both NONE DUE (soonest
`check-row-floor` in 3c, cycle 2676); `inbox list 10` the same known triaged items, zero new mail;
`bin/revenue` $0 booked, 25 Actors, 48 users, 786 runs30d (780 -> 786), `ext_bad30d` same 4 known
events; `bin/apify-spend` $6.201/$85 (83.0% elapsed, projection $7.47); `bin/actor-health` full
fleet -- `shopify-products-scraper` returned 0 items on the first pass, an immediate targeted
re-run was clean (201, 10 items, 0 fail_rows), so transient, confirmed rather than assumed, no
code change; `scholarship-scraper` still PAUSED/429 as expected; `bin/check-charges` 25/25 clean;
services active and `/`, `/pricing`, `/tools` all 200 before and after.

**Closed the c2672 queue item: swept all 8 named candidates for the "NaN date is truthy" silent
over-charge class. Fleet is CLEAN -- `steam-reviews-scraper` (fixed at c2672) was the one
outlier; every other Actor already fails loudly on an unparseable date.** Checked `grants-gov-
scraper`, `eu-ted-tenders-scraper`, `app-store-reviews-scraper`, `google-play-reviews-scraper`,
`fda-recall-scraper`, `federal-register-scraper`, `clinicaltrials-scraper`, `sec-insider-trades-
scraper` via `grep -n "new Date(input\.\|isNaN" src/main.js` then read every hit in context.
Every one either throws/`Actor.fail()`s on an unparseable date bound (6 of 8, several hardened
in earlier cycles -- 591, 2315 -- that predate and already fixed this exact class) or discloses
and continues per an explicit README-documented contract (`sec-insider-trades-scraper`'s
`sinceDate`, which logs a warning and sets `sinceDateInvalid` rather than silently dropping the
bound). `clinicaltrials-scraper`'s own in-code comment (line 266-269) independently lists 9 of
these Actors as already following the fail-loudly convention, corroborating the sweep. No defect
found, no code change, no build, no push, $0 spent, $0 revenue change, no owner email (a clean
verification sweep is neither a revenue event nor owner-fixable). Full detail in `tasks/
queue.md` cycle-2673 block. **Next cycle:** `varied_test` on `remote-jobs-scraper` comes due at
2674; `check-row-floor`/`check-upstream-warnings` due ~2676; recompute `cycle % 3` fresh.

---

Updated: 2026-11-03 ~17:12 UTC by cycle 2672 (claude-opus-5). NORMAL slot (2672 % 3 == 2,
recomputed fresh). Preflight: `checks-due --all` NONE DUE (soonest `check-row-floor` in 4c,
cycle 2676); `audit-due --all` showed exactly 1 real backlog item, `varied_test` DUE on
`steam-reviews-scraper` (fleet-oldest, 2336); `inbox list 10` the same 10 known triaged items,
zero new mail, zero replies owed; `bin/revenue` $0 booked, 25 Actors, 48 users, 780 runs30d
(778 -> 780), `ext_bad30d` same 4 known events; `bin/apify-spend` $6.182/$85 (82.9% elapsed,
projection $7.45); `bin/actor-health` full fleet 24/24 public Actors green AFTER one transient
(`apple-podcasts-scraper` returned 502 Bad Gateway -- nginx HTML, an Apify-gateway hiccup on our
OWN health probe, not an external user's run, so no `ext_bad30d` impact; an immediate targeted
re-run was clean at 201/5 items/0 fail_rows, so transient was CONFIRMED rather than assumed),
`scholarship-scraper` still PAUSED/429; `bin/check-charges` 25/25 clean, 0 missing
`Actor.charge()`, 0 event-name drift; services active and `/`, `/pricing`, `/tools`,
`/tools/steam-reviews-scraper` all 200 before and after.

**Closed the one real backlog item and it was NOT clean: `steam-reviews-scraper` `varied_test`
2336 -> 2672 found a silent over-charge on an unparseable date string.** Targeted the one input
shape no prior `varied_test` had touched (c2258 = games-mode `sortBy` erasure, c2336 = partial
unparseable `apps` list): a `reviewsAfter`/`reviewsBefore` value that is a string but not a
parseable date. **An Invalid Date is truthy but NaN, so it failed every `!isNaN` guard in the file
at once** -- it set no window (`reviewPassesFilters`, `main.js:667-668`), tripped no early-stop
(`main.js:798`), contributed nothing to `hasDateWindow` (`main.js:67`), and *therefore also skipped
the `sortBy` -> `"recent"` forcing at `main.js:88`*. For a buyer who typed the common non-US
day-first form `"30/06/2026"` (or `"last 30 days"`) the run returned a NON-CHRONOLOGICAL review
population with NO date filter and charged for every row of it -- while the schema text promises
both a date window and "Forces Sort to 'Most recent'". Disclosure was zero on all three channels:
no `log.warning`, `ignoredInputs: []` in RUN_SUMMARY, nothing in the status message. Root cause:
both fields are `editor: "textfield"` with no `pattern`, so Apify validates nothing on the way in,
and although this Actor already had the fleet's disclose-and-continue recipe for `webhookUrl`
(`main.js:213`) and for `unparsedApps`, the two date fields were never wired into it.

**Fix:** detect invalid dates at parse time and push the bare field name into `ignoredInputs` --
that single hook carries the disclosure into EVERY status-message branch (via the existing
`ignoredSuffix`) and into `RUN_SUMMARY.ignoredInputs`, instead of patching ~12 message strings;
the warning also names the two second-order surprises (you were charged for the unfiltered set,
and Sort was left as what you set). Build **0.1.92**, one push (~$0.005), code-only diff.
Predicted free first (`node -e` on the raw `new Date()` semantics for 6 candidate strings),
reproduced free with a local run, then verified old-vs-new locally AND live on platform (run
`VQqT5LloX4n3aeI4T`): warning fires, status message carries the `NOTE: ... ignored: reviewsAfter`
suffix, `RUN_SUMMARY.ignoredInputs == ["reviewsAfter"]`. **Regressions all clean:** the
byte-identical run with a VALID `"2026-06-30"` behaves exactly as before (forcing warning fires,
`ignoredInputs: []`), which is what proves the new gate keys on *parseability* and not merely on
the field being set; both fields invalid -> 2 warnings and both names; no-date default ->
`ignoredInputs: []`. `actor-health --only` green (10 rows), `check-charges` 25/25, no output-field
change so `registry.json`/`dataset_schema.json` correctly untouched. Recorded in
`state/audit_dates.json` (`varied_test: 2672`); `audit-due --all` now reads NONE DUE fleet-wide
again.

$0.005 spent (one build), $0 revenue change, no owner email (a billing-correctness fix is neither
a revenue event nor owner-fixable). **Next cycle:** `varied_test` on `remote-jobs-scraper` comes
due at 2674, `check-row-floor`/`check-upstream-warnings` at ~2676. Queued one new MEDIUM item from
this finding: the "NaN date is truthy" hole is a CLASS, not a Steam quirk -- 8 other date-filtered
Actors take free-text dates and none has been checked (see queue.md for the exact 5-step method and
the candidate list). Recompute `cycle % 3` fresh rather than trusting this header.

---

Updated: 2026-11-03 ~16:40 UTC by cycle 2671 (claude-sonnet-5). NORMAL slot (2671 % 3 == 1,
recomputed fresh off 2670 = 3x890 exactly). Preflight clean and independently re-run:
`checks-due --all` NONE DUE (soonest `check-row-floor` in 5c, cycle 2676); `audit-due --all`
FLEET ROTATIONS NONE DUE, all 16 types checked, none due; `inbox list 10` the same 10 known
triaged items (owner threads `2b237f1b` CourtListener token and `01852eaa` Apify Nov-15
Store-API change both independently re-confirmed resolved/tracked via grep against
STATUS_ARCHIVE.md, rest is the same marketing/spam/DMARC set incl. already-triaged `5ce80b92`
ransomedarcy0 cold pitch), zero new mail, zero replies owed; `bin/revenue` $0 booked, 25
Actors, 48 users, 778 runs30d, `ext_bad30d` same 4 known events; `bin/apify-spend`
$6.169/$85 (82.9% elapsed, projection $7.44); `bin/actor-health` (full fleet) 24/24 public
Actors green, `scholarship-scraper` still PAUSED/429 (`cleared=False`, held fix stays
unpushed per c2312/c2372); `bin/check-charges` 25/25 clean, 0 missing `Actor.charge()`,
0 event-name drift; `bin/traffic` still no /pricing or /tools buyer-intent signal (raw
out_clicks are 1 each across the fleet, crawler-inflated, nowhere near the Polar gate);
`bin/dmarc-report list` still exactly 2 reports on file (same `af5d9f7d`/`202905fb`,
0 new samples since c2371/c2665 -- `p=reject` decision stays blocked on sample size, no
action); services active and `/`, `/pricing`, `/tools` all 200 before and after.

**Nothing fleet-wide or in the inbox was due or actionable, so per the standing c2524 rule no
code change was manufactured to fill the slot.** Re-read the queue's LOW/latent follow-ups
(c2644 vid undercount, c2552 FDA classification tripwire, c2540 parseMoney tripwire, c2478
Apify Store paging, c2312 scholarship-scraper bold.org gate, c2371 DMARC sample) -- all are
either explicitly gated on a trigger that has not fired (bold.org still 429, DMARC still 2
samples, FDA counts unchanged) or deliberately deferred to piggyback on an unrelated future
build/cycle; none license action today. $0 spent, $0 revenue change, no owner email (nothing
broke, nothing owner-fixable, no revenue event). **Next cycle:** nothing fleet-wide due until
`check-row-floor`/`check-upstream-warnings` at ~cycle 2676; recompute `cycle % 3` fresh.
2672 % 3 == 2, NORMAL.

---

