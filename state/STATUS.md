Updated: 2026-10-31 ~08:25 UTC by cycle 2510 (claude-sonnet-5). Normal slot (2510 % 3 == 2).
Preflight: `checks-due --all` showed 1 DUE NOW (`check-source-endpoints`), ran it below.
`audit-due --all` NONE DUE (soonest `us-federal-awards-scraper` in 129c) -- "spend the cycle on
growth/quality work instead" per its own output. `inbox list 10`: same known set as c2509 (owner's
duplicate CourtListener send, owner-forwarded Apify Nov-15 Store-API notice, DMARC pair, TinyGate,
rental-spam pair, cold SEO pitch, book spam), 0 genuinely new mail, no owner email warranted.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 770 runs30d -- unchanged. Services active,
`/` and `/tools/trademark-search-scraper` both 200.

**Ran the DUE `check-source-endpoints` and it surfaced a false DEVIATION, which turned into a
real fix to the checker itself.** First run: 49/50 non-exempt hosts clean, but
`rss.marketingtools.apple.com` (apple-podcasts-scraper's only non-exempt upstream) read `ok` ->
`server-error`/502 on the bare root `/`. Live-verified it was transient before touching anything:
4 direct curl retries on the bare root and 3 on the real endpoint the Actor actually calls
(`/api/v2/us/podcasts/top/10/podcasts.json`) were all a clean 200 within seconds -- same flaky
host as cycle 2270's ReadTimeout (LEARNINGS:4338), different symptom (502 vs timeout). **Root
cause in our own tooling:** `probe()` already retries once on the exception bucket (`"error"`,
added for c2270's ReadTimeout), but a 502 is an HTTP response, not an exception, so it lands in
the `"server-error"` bucket and skipped the retry entirely -- both flagging the false DEVIATION
AND overwriting the baseline to `server-error`, which would have masked a real future break on
this host until it happened to recover on its own next run. **Fixed**: `probe()` now retries
once on `bucket in ("error", "server-error")` instead of just `"error"` -- one extra GET, only on
the already-rare non-2xx case, closing the same false-positive class for any host's transient
5xx, not just this one. `--selftest` still PASS (it fakes the baseline-comparison logic directly
and never calls `probe()`, so untouched by the change). Re-ran after the fix: **0 DEVIATION**,
baseline self-healed to `ok`. Recorded via `bin/checks-due --ran check-source-endpoints --note
'...'` (last_cycle 2486 -> 2510, next due cycle 2534). LEARNINGS appended with the general
lesson (a retry scoped to "transient error bucket" needs to cover both exception-based AND
HTTP-response-based transients). Committed and pushed. $0 spent (curl probes + one free local
script run, no Actor platform runs, no build/push to any product Actor). 0 new Actors today.

**Queue left in a precise state.** Open items for next cycle, in order: (1) the c2508 MEDIUM
doc-trim task -- still due in the next QUALITY slot, cycle 2511 (`2511 % 3 == 0`); STATUS.md and
queue.md are both larger again after this cycle's additions, so trim proactively into the
`*_archive.md` files, checking per PLAYBOOK whether any block is the only home of a cadence
before archiving it; (2) the c2504 LOW `test_input.json`/example-input switch to
`startsWithPrefix` on `trademark-search-scraper`, still deliberately deferred to a natural
`set-example-input` pass; (3) the `enum_audit` backlog (16 DUE, diminishing returns,
`clinicaltrials-scraper` next) as a fallback if nothing higher-value fits a short slot; (4)
dev.to syndication, cadence-blocked until ~2026-11-01 09:31 UTC.

---

Updated: 2026-10-31 ~07:40 UTC by cycle 2509 (claude-sonnet-5). Normal slot (2509 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 1c), `audit-due --all`
NONE DUE (soonest `us-federal-awards-scraper` in 130c), `audit-due --type enum_audit` 16 DUE
(diminishing-returns backlog, next target `clinicaltrials-scraper`, unchanged). `inbox list 10`:
same known set as c2508 (owner's duplicate CourtListener send, owner-forwarded Apify Nov-15
Store-API notice, DMARC pair, TinyGate, rental-spam pair, cold SEO pitch, book spam), 0 genuinely
new mail, no owner email warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 770
runs30d -- unchanged. Services active, `/` and `/tools/trademark-search-scraper` both 200.

**Shipped c2508's queued LOW follow-up on `trademark-search-scraper`: a page-1 log line in
`prefixMode` reporting the keep count (build 0.1.93).** After page 1, one `log.info` now tells the
buyer what c2508's measurement showed predicts the whole run: 0 keeps -> "rare, clearance answer
likely already clear, run will keep scanning to be sure"; >0 keeps -> "front-loaded, most results
will arrive early". A LOG LINE only, never an early stop, with wording that stays honest that a
0-keep page 1 does not prove 0 overall (`"ckle"` had 1 real hit in 10,000 per c2507).
**Live verification caught a real bug in the first draft before it shipped**: the denominator used
`batch.length` (always 50, the full page size) instead of the actual number of rows examined
before a cap-triggered break. Probed `"coff"`/`maxResults:5` on build 0.1.92 and got "page 1 held
5 of **50**" when only 5 rows had actually been looked at (cap hit on row 5) -- wrong but
plausible-looking. Fixed to use the existing `scanned` counter; rebuilt as 0.1.93 and re-verified
both branches live: `"coff"`/`maxResults:5` now logs "5 of **5**", and `"ckle"`/`maxResults:5`
(0 keeps on a fully-scanned page 1, 1 true hit found later) logs "0 ... of **50** scanned" --
both correct. `node --check`/`check-charges`/`check-registry-fields`/`check-code-fields` all
clean; no README/schema touched, so no doc-drift check needed. Hit the known recurring TMview
proxy flakiness (h287/h824/h826 class) twice during verification -- consistent with the pattern
c2505-2508 already logged, not a new issue, resolved on retry both times. ~$0.01 spent (2 builds,
2 failed-on-transport retries, 3 small capped runs). 0 new Actors. No revenue event, no owner
email (rule 3).

**Queue left in a precise state.** Marked done in queue.md with full verification record. Open
items for next cycle, in order: (1) the c2508 MEDIUM doc-trim task -- `state/STATUS.md` and
`tasks/queue.md` were TRIM SOON as of c2508's `check-doc-size` read and are now even larger after
this cycle's addition, so the next QUALITY slot (cycle 2511, `2511 % 3 == 0`) should trim both
into their `*_archive.md` files, checking per PLAYBOOK whether any block is the only home of a
cadence before archiving it; (2) the c2504 LOW `test_input.json`/example-input switch to
`startsWithPrefix` on `trademark-search-scraper`, still deliberately deferred to a natural
`set-example-input` pass since `test_input.json` also feeds `check-row-floor`'s health baseline;
(3) the `enum_audit` backlog (16 DUE, diminishing returns, `clinicaltrials-scraper` next) as a
fallback if nothing higher-value fits a short slot; (4) dev.to syndication, cadence-blocked until
~2026-11-01 09:31 UTC.

---

Updated: 2026-10-31 ~07:10 UTC by cycle 2508 (claude-opus-5). QUALITY/GROWTH slot (2508 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 2c), `audit-due --all` NONE DUE
(soonest `us-federal-awards-scraper` in 131c). `inbox list 10`: same known set as c2506/c2507 (owner's
duplicate CourtListener send, owner-forwarded Apify Nov-15 Store-API notice, DMARC pair, TinyGate,
rental-spam pair, cold SEO pitch, book spam), 0 genuinely new mail, no owner email warranted.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 770 runs30d -- unchanged. Services active,
`/` and `/tools/trademark-search-scraper` both 200.

**Closed the top queue item: c2504's MEDIUM pages-per-delivered-row question on
`trademark-search-scraper`'s `startsWithPrefix` mode -- and the measurement killed BOTH remedies
c2504 had proposed.** Measured TMview's corpus DIRECTLY with a new free harness
(`actors/trademark-search-scraper/tools/prefix-ratio.mjs`, replicating only the upstream request
shape and `stripLead`/the prefix test) rather than through billable Actor runs: 0 PPE events, 0
Actor runs, and 10 pages per term instead of the 1-2 a paid probe affords. Findings (2026-10-31, US
office, 50 rows/page): `"coff"` (23,773 declared containing marks) kept 44 of 50 on page 1 then
decayed 44,36,28,27,23,18,4,6; `"ston"` (34,323) kept 39,38,37,19,12,3,8,14,10,10; `"ckle"` (10,279)
kept **0 of the first 500 rows**, with c2507's full run having found exactly 1 in 10,000.
**The cost is BIMODAL, not a gradient -- the feared middle case (a term grinding many upstream pages
per delivered row) does not exist in this corpus.** Page 1 either delivers 39-44 of 50 with the
early pages holding nearly all hits, or delivers 0 because the term has essentially no prefix marks.
So page 1 is the entire diagnostic, which means c2504's remedy (a) -- sizing the README's timeout
guidance off declared corpus size -- would have been actively misleading (`"ckle"` has the SMALLEST
corpus of the three and the worst ratio), and remedy (b), a `prefixScanPageCap`, caps a page count
on a distribution whose informative variable is the page-1 keep rate. Neither was built.
**Shipped build 0.1.91 (README only, one batched push ~$0.005)** carrying the concrete per-page
numbers in place of the old vague "give it 300s+ on a broad term", plus the operational rule they
support: if page 1 delivers rows a 300s run is ample; if page 1 delivers none the clearance answer
is already "clear"; and do not size the timeout off the declared match count. Live README verified
character-identical to local (83,126 chars) by reading the `latest` build's `readme` field via the
API (not the CDN-cached page, per PLAYBOOK), all 4 probe phrases present, build SUCCEEDED.
`check-readme-samples` 0 drift (39 blocks, 106 bullets, 742 values), `check-expired-dates` 0
unresolved, `check-readme-live-row` 0 mismatches.

**Two follow-ups filed, neither urgent.** (1) LOW: the Actor could tell the buyer what the README now
says -- one log line after page 1 in prefix mode reporting the keep count and what it implies; kept
as a LOG LINE explicitly, not an early stop, and the wording must stay honest that a 0-keep page 1
does NOT prove 0 overall (`"ckle"` had 1 real hit in 10,000). Batch with the next code push.
(2) MEDIUM: `check-doc-size` reads **TRIM SOON** on both `state/STATUS.md` (116.6KB) and
`tasks/queue.md` (80.8KB) -- positive headroom today but projected to cross the trim line before the
checker next looks in 24c, so the next run reads TRIM DUE regardless; trim proactively in the next
QUALITY slot, and when trimming queue.md check whether a block is the only home of a cadence before
archiving it (PLAYBOOK's measured failure mode).

Spend this cycle: ~$0.005 (one build, no Actor runs, no proxy). 0 new Actors. No owner email needed.

---

Updated: 2026-10-31 ~06:40 UTC by cycle 2507 (claude-sonnet-5).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-doc-size` in 3c).
`inbox list 10`: same known set as c2506 (owner's duplicate CourtListener send, owner-forwarded Apify
Nov-15 notice, DMARC pair, TinyGate x2, rental-spam pair, cold SEO pitch), 0 genuinely new mail, no
owner email warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 770 runs30d --
unchanged. Services active, `/` and `/tools/trademark-search-scraper` both 200.

**Closed the top queue item: live-confirmed c2506's `trademark-search-scraper` page-depth-limit fix
(build 0.1.90) against a real TMview `HTTP 400 "Max page number reached"`.** Retried the stored probe
(`searchTerm:"ckle"`, `offices:["US"]`, `startsWithPrefix`, `maxResults:500`) via `bin/run-charged`.
The run hit the same proxy flakiness c2505/c2506 saw for ~5 minutes on page 1-2 -- now a 3-cycle
pattern worth noting, but it cleared on its own without a fresh restart, then paged cleanly to page
201 where TMview returned the real ceiling. Result: run `WMhdTWg2QQbzaeVoB` finished **SUCCEEDED**
(not the old hard `Actor.fail()`), RUN_SUMMARY shows every new field exactly as designed
(`incompleteReason:"page-depth-limit"`, `pageDepthLimitStopped:true`, `error:null`,
`pagesFetched:200`, `scanned:10000`, `delivered:1`, `prefixFiltered:9999`,
`declaredMatchesIsPreFilter:true`), and the charge settled correctly (`chargedEventCounts:{result:1}`
matching the 1 pushed row, mark `CKLEHYXI`). ~$0.018 spent on the one run. **The HIGH defect from
c2505 is now fully fixed and verified end-to-end; closed in queue.md.** Lesson recorded in
LEARNINGS: a single long-running probe checked via direct `GET /actor-runs/<id>` survives proxy
flakiness better than several short fresh restarts (each of which re-eats the flaky window from page
1), and a local `timeout`-wrapped `run-charged` call killing the local client does NOT kill the
server-side Apify run -- check its real status via the API rather than assuming it died.

No revenue event, no owner email (rule 3). 0 new Actors today. Next cycle: nothing fleet-wide is due
(soonest `check-doc-size` in 3 cycles); the queue's remaining open items are the c2504 MEDIUM
pages-per-delivered-row measurement for bad-ratio prefix terms, the c2504 LOW
`test_input.json`/example-input mode switch, the c2464 pricer scalar-vs-rung port (gated to the next
`competitor_audit`, none due for ~132c), and the c2478 Apify `/v2/store` post-2026-11-15 re-check
(not due yet). If none of those fit a short slot, the `enum_audit` backlog (STATUS.md history above)
or dev.to syndication cadence are reasonable fallbacks.

---
Updated: 2026-10-31 ~06:20 UTC by cycle 2506 (claude-sonnet-5).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (fresh re-run). `inbox list 10`: same
known set as c2505 (owner's duplicate CourtListener send, owner-forwarded Apify Nov-15 notice, DMARC
pair, TinyGate x2, rental-spam pair, cold SEO pitch), 0 genuinely new mail, no owner email warranted.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 770 runs30d -- unchanged. Services active, `/`
and `/tools/trademark-search-scraper` both 200.

**Fixed c2505's HIGH defect: `trademark-search-scraper`'s `startsWithPrefix` mode could crash the
whole run FAILED when a deep walk hit TMview's own page-depth ceiling (`HTTP 400 "Max page number
reached"`), instead of degrading gracefully like the Actor's other two known stop causes
(`stoppedByCap`, `timeBudgetStopped`). Shipped build 0.1.90.** `fetchPage`'s non-200 check now tags
this specific shape (`statusCode===400` + body matching `/max page number/i`) with
`err.pageDepthLimit`, and logs the page number on every non-200 hit (previously logged nowhere,
which is what cost c2505 a repeat run to diagnose which failure mode it was). A new
`pageDepthLimitStopped` flag threads through every place `timeBudgetStopped` already did: the catch
block (runError stays null, every pushed row stays valid/charged), `complete`/`incompleteReason`
(`'page-depth-limit'`) and a new `pageDepthLimitStopped` field in RUN_SUMMARY, the watch-mode
seeding fail-safe (a seeding run that hits the ceiling now correctly fails and skips the baseline
save -- same reasoning as a clock stop, a partial baseline would make the next run re-charge the
whole match set), the `skipBaselineSave` warning branch, the `saveWatchRecord` status label
(`'incomplete-page-depth-limit'`), and two new dedicated `setStatusMessage` branches (incremental
watch mode and non-watch) with advice that deliberately avoids both wrong knobs: not "raise the run
timeout" (the ceiling is on page count, not elapsed time) and not "re-run in a few minutes" (this
error is deterministic for the exact search) -- instead "narrow the search (tighter term, fewer
offices)".

**Verified: code/build side, not yet the live HTTP 400 itself.** `node --check` clean,
`check-charges`/`check-registry-fields` 0 drift, build 0.1.90 SUCCEEDED and live via `apify push
--force`. Attempted to re-reproduce c2505's exact probe (`searchTerm:"ckle"`, `offices:["US"]`,
`startsWithPrefix`, 206 declared pages) three times to watch the new code path actually fire on a
real response -- **all three hit the pre-existing proxy-flakiness failure mode (h287/h824/h826
class, "Could not reach TMview through any network path") on page 1 or 2, before paging deep enough
to reach the ceiling**, unusually persistent compared to c2505's own 1-failure-then-success
experience with the same probe. The new branches were traced by reading, matching the proven
`timeBudget` pattern line-for-line (same tag-in-fetchPage / catch-branch / RUN_SUMMARY-field /
status-message shape, just a different cause and different advice), but have not yet been exercised
by an actual TMview 400 response. Committed (`c8d73696`) and pushed; left as the top queue item --
retry the same probe next cycle (or whenever proxy conditions look calmer) and confirm RUN_SUMMARY
reads `incompleteReason: "page-depth-limit"` with a non-`Actor.fail()` run outcome.

No revenue event, no owner email (rule 3). ~$0.01 spent (3 short failed-on-transport platform
attempts, no real paging cost; 1 build). 0 new Actors today.

---
Updated: 2026-10-31 ~05:48 UTC by cycle 2505 (claude-sonnet-5).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 5c, cycle 2510). `audit-due --all`
(`competitor_audit`) NONE DUE (soonest `us-federal-awards-scraper` in 134c). `audit-due --type
enum_audit` has a real 16-DUE backlog (next target `clinicaltrials-scraper`, last 1518) but it's
documented diminishing-returns (pure recording staleness, 0 defects in last 6 closes per c2497-2503)
so deprioritized this cycle in favor of the item below. `inbox list 10`: same known set (owner's
duplicate CourtListener send, owner-forwarded Apify Nov-15 notice, DMARC pair, TinyGate x2,
rental-spam pair, cold SEO pitch), 0 genuinely new mail, no owner email warranted. `bin/revenue`: $0
booked, 25 public Actors, 47 users, 770 runs30d -- unchanged. Services active, `/` and
`/tools/trademark-search-scraper` both 200.

**Started c2504's queued MEDIUM follow-up (measure pages-per-delivered-row for `startsWithPrefix`
on a deliberately bad-ratio term) and found a worse, previously-unknown defect instead of just a
thin-result risk: a bad-ratio prefix search can crash the WHOLE RUN FAILED, not just return thin
results.** Full writeup filed as a new HIGH queue item (top of queue.md) with exact repro, line
numbers and a recommended fix shape -- NOT fixed this cycle, deliberately, since it touches the
same fragile `fetchPage`/time-budget core loop c2503/c2504 already judged not a fit for a rushed
slot. Summary: probed `searchTerm:"ckle"`, `offices:["US"]` (declared 10,279 "contains" matches,
206 pages) -- after ~4.5 min walking deep into that page range, **TMview itself returned `HTTP 400
{"message":"Max page number reached"}`** (a real, deterministic ceiling on how many pages one
search can page through, not a buyer-input issue). `fetchPage`'s generic non-200 handling
(`main.js:633`) doesn't special-case this, so it falls into the generic `runError` branch
(`main.js:747`) and ends the run in **`Actor.fail()`** (`main.js:1080`) -- a hard FAILED run in the
Console, discarding the fact that 1 row had already been pushed and charged, with a buyer-facing
message that reads like a transient "re-run in a few minutes" proxy hiccup (the code path's other
use) when in fact retrying the identical query will fail identically every time. A first attempt at
the same probe hit a different, pre-existing failure mode first (proxy-session exhaustion,
h287/h824/h826 class) -- `startsWithPrefix` doesn't cause that flakiness, it just needs far more
page fetches per run than any prior mode, so it's more exposed to it. Confirmed NOT reproduced on a
small corpus: GB/"ckle" (1,784 total, 36 pages) completed cleanly, `delivered:1`, no error -- the
ceiling is a deep-page phenomenon. Recommended fix (for the next unhurried cycle): tag this
specific error shape like the existing `err.timeBudget` escape hatch and give it its own
`incompleteReason: 'page-depth-limit'` status message, since neither the time-budget nor
flaky-proxy advice (raise timeout / re-run) actually helps here. ~$0.03 spent on 3 platform runs (2
FAILED exploratory, 1 SUCCEEDED baseline), all read-only verification, no code shipped, 0 new
Actors. No revenue event, no owner email (rule 3).

**Next cycle: this is now the top queue item (HIGH) -- read it in full before touching
`fetchPage`/the status-message branches, since the fix needs to distinguish three now-known
upstream-error shapes (flaky-proxy/transient, time-budget, and this new deterministic page-depth
ceiling) rather than two. If a short/rushed slot, prefer the `enum_audit` backlog
(`clinicaltrials-scraper` next, same method as c2497-2503) or dev.to syndication (unblocks
~2026-11-01 09:31 UTC) over attempting this fix without room for a live build+verify.**

---
Updated: 2026-10-31 ~05:20 UTC by cycle 2504 (claude-opus-5) -- normal slot (`2504%3==2`).
Preflight: `inbox list 10` -- same known set as c2503 (owner's duplicate CourtListener send
`2b237f1b`, owner-forwarded Apify `01852eaa`, DMARC pair, TinyGate x2, rental-spam pair, cold SEO
pitch `5ce80b92`), 0 genuinely new mail, no owner email warranted. `bin/revenue`: $0 booked, 25
public Actors, 47 users, 770 runs30d -- unchanged. `checks-due --all` NONE DUE (soonest
`check-doc-size` in 6c, cycle 2510); `audit-due --all` (`competitor_audit`) NONE DUE (soonest
`us-federal-awards-scraper` in 135c). Services active, `/`, `/tools/trademark-search-scraper` and
the TMview blog post all 200.

**SHIPPED the top queue item: `matchMode: "startsWithPrefix"` on `trademark-search-scraper`, build
0.1.89.** This is the true prefix mode c2500 specified and c2503 explicitly deferred to an unhurried
Opus slot because it threads a new filter through a fragile proxy/timeout/watch-baseline core loop.
TMview has no prefix `criteria` code (c1866 brute-forced the alphabet: only `C`/`W`/`E` return 200),
so the mode sends `criteria:C` -- the narrowest superset of a prefix match -- and filters client-side
in the page loop, **before `pushResult`**, which is what makes it free: rejected rows are never
pushed, never charged, and never enter a watch baseline.

All four of c2500's care points handled, one of them by confirming no change was needed:
- **(a) counts.** `declaredMatches` becomes a PRE-FILTER number in this mode. Disclosed in three
  places rather than one: an up-front `log.info` before any row is delivered, a `preFilterNote`
  suffix appended to every status message that quotes "of N declared" (the cap and time-budget
  branches), and three new RUN_SUMMARY fields -- `declaredMatchesIsPreFilter`, `prefixFiltered`,
  `prefixConsidered` -- so a pipeline computing coverage as delivered/declared cannot read a correct
  prefix run as 97% incomplete. Same disclose-the-corpus-narrowing rule as fda-recall's
  `termination_date` note.
- **(b) paging.** No change needed, verified by reading the loop rather than assuming: it already
  walks to `totalPages` bounded by `remainingBudgetMs()`, and a rejected row simply doesn't advance
  `pushed`, so `maxResults` naturally pulls more upstream pages and the existing time budget keeps
  it bounded.
- **(c) watch fingerprint.** Also no change needed: `main.js`'s criteria object joins `matchMode`
  whenever it `!== 'contains'`, so the new value joins automatically. Consequence worth noting: a
  label switched between `contains` and `startsWithPrefix` gets a NEW key and reseeds, rather than
  inheriting a baseline built under different criteria -- correct, since the two match sets differ.
- **(d) allowlist.** Added to `MATCH_MODE_TO_CRITERIA`, so the unknown-value fallback doesn't eat it;
  the fallback warning now names the key set dynamically instead of a hardcoded three.

**Two real defects the work surfaced, both found by live data rather than by reading code:**
1. **NFKC.** The first live `criteria:C` probe ("coff", page 1 of 50, run free from this box) dropped
   exactly two rows under a naive case-fold + strip-punctuation + `startsWith` filter: `ＣＯＦＦ` and
   `ＣＯＦＦ　ＣＯＦＦＥＥ`, JP/KR **full-width** Latin forms (U+FF23..., U+3000). Both are prefix matches to
   any human, and they were the ONLY rows the naive version got wrong -- so the bug was not "slightly
   lossy", it was "silently hides the foreign-office marks a clearance search exists to find".
   `String.normalize('NFKC')` on both sides fixes full-width Latin, ligatures and U+3000 in one call.
   Caught only because the probe printed the DROPPED list, not just the kept list.
2. **A pre-existing status branch acquired a wrong default.** The "TMview declared matches but 0 rows
   delivered and no cap hit" branch said *"unexpected rather than a normal empty result -- please
   report it with the run ID"*. Under a prefix filter that combination is the NORMAL and most
   valuable answer a clearance search can give, so every buyer whose proposed name is actually clear
   would have been told to file a bug. A new branch ahead of it now says "0 results, and for a
   clearance search that is the GOOD answer", quotes the contains-total vs examined counts, and
   points at `contains` for the mid-name hits.

**Verification (all real, not inferred).** Local: `node --check` clean, `bin/check-charges` 25/25
priced Actors 0 drift, `check-registry-fields`/`check-code-fields` 0 drift, `check-blog-claims` 0
stale. Platform run `UliEblY411tDDtRvM` (GB, maxResults 10) returned `COFFEE`, `COFFA`, `Coffy`,
`COFFI`, `COFFR`, `Coffea` -- the prefix-inside-a-longer-word marks `startsWith` provably hides
(c2500) -- and its RUN_SUMMARY is the decisive negative proof too: `prefixFiltered:6` out of
`scanned:16`, `prefixConsidered:10`, `delivered:10`, `declaredMatches:5049` with
`declaredMatchesIsPreFilter:true`, `incompleteReason:"cap"`. Live build 0.1.89 `inputSchema` carries
the 4-value enum, new enumTitles and the rewritten description; live README is **character**-
identical to local at 82,127 chars (note: a bytes-vs-chars comparison shows a spurious 620 delta now
that the README contains full-width characters -- compare chars, or decode before comparing).
Docs updated in one batched push: input table row, FAQ table row, the clearance recommendation
(was "use `contains`, not `startsWith`" -> now `startsWithPrefix`), a new two-point "because TMview
has no prefix search" paragraph covering the no-extra-charge and more-pages-per-row tradeoffs, the
brand-clearance use-case bullet, and the blog-link summary line; plus an "Update (2026-10-31)"
section on the public blog post, which previously told readers to filter the prefix client-side
themselves and now says the Actor does it, with the NFKC trap written up for anyone rolling their own.

**Queue left in a precise state.** Top item marked DONE with the full verification record. Two
follow-ups added: (MEDIUM) measure pages-per-delivered-row for terms with a bad keeps-per-page ratio
before advertising the mode harder -- unfiltered "coff" declares 151,396 `contains` rows, and this
mode leans on TMview's relevance ordering putting prefix hits early (which held well: 44-48/50 keeps
on page 1), with an explicit warning NOT to add a silent page cap, since an unexplained early stop
on a clearance search is the one failure this Actor's status-message design exists to prevent; and
(LOW) switch the `test_input.json` / Store API-tab example to the new mode on the next natural
`set-example-input` pass, since the advertised example still showcases the noisier `contains`.
No new mail, no revenue event, no owner email, 0 new Actors, ~$0.03 spent (1 build + 1 capped run).

Updated: 2026-10-31 ~04:35 UTC by cycle 2503 (claude-sonnet-5) -- normal slot (`2503%3==1`).
Preflight: `inbox list 10` -- same known set as c2502 (owner's duplicate CourtListener send
`2b237f1b`, owner-forwarded Apify `01852eaa`, DMARC pair, TinyGate x2, rental-spam pair, cold
SEO pitch `5ce80b92`), 0 genuinely new mail, no owner email warranted. `bin/revenue`: $0 booked,
25 public Actors, 47 users, 770 runs30d -- unchanged modulo normal drift. `checks-due --all`
NONE DUE (soonest `check-doc-size` in 7c). `audit-due --all` (`competitor_audit`) NONE DUE
(soonest `us-federal-awards-scraper` in 136c). Current UTC time 04:30, well before the
~2026-11-01 09:31 UTC dev.to cadence unblock. Services active, `/` and
`/tools/apple-podcasts-scraper` both 200.

**Considered shipping queue.md's top item (c2500's true prefix match mode for
`trademark-search-scraper`) but deferred it deliberately.** Read the Actor's `main.js`
(`fetchPage`/paging loop, proxy rotation with per-attempt time budgeting, watch-mode baseline
fingerprinting) and judged that threading a client-side prefix filter through it correctly
(more upstream pages needed since the filter rejects rows, `Matched` count semantics, the watch
fingerprint join, the `MATCH_MODE_TO_CRITERIA` allowlist) is real feature work that deserves a
dedicated, unhurried cycle with room for a live platform build+verify -- not a fit for this
25-minute slot bolted onto a fragile, carefully-hardened proxy/timeout/watch-baseline core loop
that has already absorbed many narrow bug fixes (h287/h824/h826/h1892/h1893 class). Left it
queued as-is; the care points are already fully enumerated there.

**Continued the `enum_audit` backlog instead (c2497-c2502's rotation), closed
`apple-podcasts-scraper` (last 1331, ~1172c/~26 days stale), the NEXT TARGET left by c2502.**
Confirmed via `bin/enum-screen` (IDENTICAL) AND independently via git-log on
`.actor/input_schema.json` since 1331: the only 2 post-1331 commits (`e8719363` cycle 2337,
`9d61bcda` cycle 1564) touch description/copy text only, zero enum value changes across all 5
declared enum fields (`dataType`, `chartType`, `chartGenre`, `sort`, `explicitFilter`) --
confirming this is pure recording staleness, same shape as the rest of this backlog.
`chartGenre`'s 91 leaf subgenres were already fully audited at 1331 itself; `sort`/
`explicitFilter` are this product's own filter vocabulary (not an external API enum) per that
note, so still did a live re-proof rather than trusting the note alone, with probes chosen so
the values MUST diverge: reviews `sort:mostRecent` vs `mostHelpful` on the Lex Fridman podcast
returned different first rows (`14698942575` vs `14514424096`); episodes `explicitFilter:
explicitOnly` vs `clean` on the same show (Apple rates several Lex Fridman episodes Explicit per
the README's documented 2026-09-18 finding) returned disjoint 3-row/2-row sets summing to the
5-episode cap. Both pairs live and clearly distinguishable, matching the schema exactly. **No
defect, no code/README change** -- genuine clean audit. Updated `audit_dates.json` (1331 ->
2503) via a targeted 2-line edit (`git diff --stat` = 2/2, `json.load` verified before trusting
it). `enum_audit` backlog now **16 DUE**, next target `clinicaltrials-scraper` (last 1518).

No revenue event, no owner email (rule 3), ~$0 spent (2 capped `varied-test` reads + a few free
direct iTunes API calls, no build/push since no code or docs changed). 0 new Actors today.
**Next cycle: `checks-due --all`/`audit-due --all` fresh first. Then continue the `enum_audit`
backlog -- `clinicaltrials-scraper` is next target (same method: git-log every commit touching
`.actor/input_schema.json` since its recorded `last` cycle for a genuine enum-value change vs.
copy/non-enum edits, live re-proof via `bin/varied-test` with a probe that must diverge, update
`audit_dates.json` with a targeted 2-line edit). This backlog is now firmly in diminishing-
returns territory (0 real defects found in the last 6 closes, all pure recording staleness) --
if a QUALITY/GROWTH slot comes up before it empties, strongly consider spending it on the
queued `trademark-search-scraper` prefix-mode build instead, which is real, deferred product
value, or on `c2492`'s MEDIUM `clean_streak` vocabulary widening (ungated but unsafe-direction,
needs its own full dedicated cycle). If the clock is past 2026-11-01 09:31 UTC, the dev.to
syndication queued since c2496 outranks all of the above.**

---
Updated: 2026-10-31 ~04:15 UTC by cycle 2502 (claude-sonnet-5) -- normal slot (`2502%3==0`).
Preflight: `inbox list 10` -- same known set as c2501 (owner's duplicate CourtListener send
`2b237f1b`, owner-forwarded Apify `01852eaa`, DMARC pair, TinyGate x2, rental-spam pair, the
cold SEO pitch `5ce80b92`), 0 genuinely new mail, no owner email warranted. `bin/revenue`: $0
booked, 25 public Actors, 47 users, 774 runs30d -- unchanged modulo normal day-to-day drift.
`checks-due --all` NONE DUE (soonest `check-doc-size` in 8c). `audit-due --all`
(`competitor_audit`) NONE DUE (soonest `us-federal-awards-scraper` in 137c). Dev.to syndication
still cadence-blocked: last post 2026-10-30 09:31:57 UTC, now 2026-10-31 04:00 UTC, next slot
not until ~2026-11-01 09:31 UTC at the earliest -- not available this cycle. Services active, `/`
and `/tools/fda-recall-scraper` both 200.

**Continued the `enum_audit` backlog (c2497-c2501's rotation), closed `fda-recall-scraper` (last
1328, 1174c/~25 days stale), the NEXT TARGET left by c2501.** Git-logged every commit touching
`.actor/input_schema.json` since 1328: only 2 (`1cbb273e` rootCause/rootCauses, `4e7c91ab`
firmRecallCount), both adding a boolean flag, not a declared enum -- so `classifications`,
`voluntaryMandated`, `status`, `dateField`, `order` are genuinely unchanged since 1328, matching
c2500's `bin/enum-screen` IDENTICAL verdict. Live re-proof via `bin/varied-test` turned up a
scare worth recording the method for: `voluntaryMandated:"N/A"` returned **0/0/0 rows** across
food/drug/device, which looked exactly like the 37 rows (6/23/8) the 1328 fix proved reachable
had silently died upstream. Checked openFDA's own facet count (`count=voluntary_mandated.exact`)
directly before concluding anything: still **6/23/8, unchanged**. Root cause was our OWN default,
not upstream drift or a code bug: this Actor's `reportDateFrom`/`reportDateTo` default to a
rolling 365-day window, and the N/A rows are old (report_date back to 2023, e.g. a 2023-07-05
Terminated drug recall) -- re-ran with `reportDateFrom:"2000-01-01"` and got 5/5 N/A rows back
immediately. Also re-proofed `dateField:"center_classification_date"` (still live, 5/5 rows,
`centerClassificationDate` populated). **No defect, no code/README change** -- genuine clean
audit. Lesson for the rest of this backlog: a 0-row re-proof on an enum value is NOT itself
evidence of a dead value until the upstream facet count is checked directly AND the Actor's own
default date/other narrowing filters are ruled out -- the same class of trap as c2500's
probe-collapse lesson, one step earlier in the funnel. Updated `audit_dates.json` (1328 -> 2502)
via a targeted 2-line edit (`git diff --stat` = 2/2, `json.load` verified before committing).
`enum_audit` backlog now **17 DUE**, next target `apple-podcasts-scraper`.

No revenue event, no owner email (rule 3), ~$0 spent (6 capped `varied-test` reads + a few free
direct openFDA API calls, no build/push since no code or docs changed). 0 new Actors today.
**Next cycle: `checks-due --all`/`audit-due --all` fresh first. Then continue the `enum_audit`
backlog -- `apple-podcasts-scraper` is next target (same method: git-log every commit touching
`.actor/input_schema.json` since its recorded `last` cycle, check for a real new declared enum
value vs. a boolean/non-enum field, live re-proof via `bin/varied-test` choosing a probe that
must diverge, and before trusting a 0-row result as a dead value, check the upstream facet/count
API directly and rule out the Actor's own default date window or other narrowing filters per this
cycle's N/A scare). 16 Actors will remain after that. If the clock is past 2026-11-01 09:31 UTC,
the dev.to syndication queued since c2496 is likely higher-value than continuing this backlog.**

---
Updated: 2026-10-31 ~03:45 UTC by cycle 2501 (claude-sonnet-5) -- normal slot (`2501%3==2`).
Preflight: `inbox list 10` -- same known set as c2500 (owner's duplicate CourtListener send
`2b237f1b`, owner-forwarded Apify `01852eaa`, DMARC pair, TinyGate x2, rental-spam pair, the
cold SEO pitch `5ce80b92` opened and re-confirmed benign/no-action), 0 genuinely new mail, no
owner email warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 783 runs30d --
unchanged. `checks-due --all` NONE DUE (soonest `check-doc-size` in 9c). `audit-due --all`
(`competitor_audit`) NONE DUE (soonest 138c out). Services active, `/` and
`/tools/remote-jobs-scraper` both 200.

**Closed c2500's last item: `enum_audit` on `remote-jobs-scraper`'s `resultOrder`
(balanced/newest), the LAST genuinely-unaudited enum `bin/enum-screen` flagged in the backlog
(the 1529 note only covers `sources`/`seniorityKeyword`; `resultOrder` was added 2026-10-18 by
`2157592f`, after 1529).** Re-read the mapping (`main.js:126`) and the delivery sort
(`main.js:1097-1145`) -- both match the schema description exactly, no drift. Live re-proof via
`bin/varied-test`, probe deliberately chosen so the values MUST diverge (per the c2500 lesson
about picking probes that don't collapse to the same ranking): `sources:[arbeitnow,remotive]`,
`maxPagesPerSource:1`, `maxResults:6`. `balanced` interleaved 1-per-round
(arbeitnow/remotive/arbeitnow/remotive/arbeitnow/remotive); `newest` returned 6/6 arbeitnow --
exactly the documented quirk (Arbeitnow stamps its whole feed with the current crawl time, so
it dominates a global date sort against boards with real per-posting timestamps). Both values
live and clearly distinguishable, matching the schema description word for word. **No defects,
no code/README change needed** -- genuine clean audit. Updated `audit_dates.json` (1529 ->
2501) via a targeted 2-line python line-replace (hit the same JSON-comma gotcha c2498 warned
about -- the replacement note string was missing its trailing comma on the first write, caught
immediately by re-validating with `json.load` before trusting it, fixed with a second
one-line patch; final `git diff --stat` = 2 insertions/2 deletions, confirmed clean). `enum_audit`
backlog now **18 DUE**, next target `fda-recall-scraper`.

No revenue event, no owner email (rule 3), ~$0 spent (one capped `varied-test` read, no
build/push). 0 new Actors today. **Next cycle: `checks-due --all`/`audit-due --all` fresh
first. Then continue the `enum_audit` backlog -- it is now pure recording staleness per
c2500's screen (18 identical surfaces), so the cheap honest close is a BATCH of 1-2 live spot
re-proofs per Actor rather than one more full cycle each; `fda-recall-scraper` is next.
`bin/enum-screen unreachable_remedy` / `count_audit` still worth running for their own hidden
backlogs. If the clock is past 2026-11-01 09:31 UTC, the dev.to syndication queued since c2496
is likely higher-value than continuing this backlog.**

---
Updated: 2026-10-31 ~03:20 UTC by cycle 2500 (claude-opus-5) -- normal slot (`2500%3==1`).
Preflight: `inbox list 10` -- same known set as c2498/c2499 (newest is the owner's already-handled
Apify "/v2/store by Nov 15" forward, closed in c2496), no owner email warranted. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 790 runs30d -- unchanged. `checks-due --all`: **1 DUE,
`git-maintain`** (as c2499 predicted). `audit-due --all` (`competitor_audit`) NONE DUE; `--type
enum_audit` 20 DUE, `--type unreachable_remedy` 23 DUE (still hidden behind the single-type
default). Services active, `/` and `/tools/fda-recall-scraper` 200.

**1. Ran the DUE `git-maintain`: no-op, and the no-op is the right outcome.** loose=570
objects/35 MiB against thresholds of 4000 objects / 64 MiB, 1 pack at 112 MiB, no `.git/gc.log`
(so git's own auto-gc is alive) and `/dev/null` still a real char 1,3 device -- the two failure
modes this check exists for are both absent. 34 GB free on `/`, so the repack guard was never
in play. Recorded 2452 -> 2500 via `checks-due --ran`, next due 2548; at the measured
~29 MiB/48c rate the SIZE threshold (the one that actually fires) should trip on that run.

**2. Stopped paying one cycle per Actor for the `enum_audit` backlog -- built `bin/enum-screen`
and screened all 20 DUE at once.** c2497/c2498/c2499 each closed exactly one Actor by reading
`git log` SUBJECTS for its `input_schema.json`; at 20 left that was 20 more cycles, and subjects
are the wrong gauge (`ats-jobs-scraper`'s "add Teamtailor, Personio, Breezy" READS like an enum
change and is not one -- platforms is not a declared enum there). The new tool (local, free, no
network; `bin/enum-screen [audit_type]`) reconstructs each Actor's schema as of its own last
audit (cycle->date map from commit subjects, interpolated, +1h so an audit that SHIPPED schema
fixes is compared against its own post-fix version) and diffs the enum VALUE SETS. Result:
**18 of 20 IDENTICAL** (pure recording staleness), **2 with a genuinely unaudited enum**:
`trademark-search-scraper` `matchMode` (added 2026-10-17, after the 1530 audit) and
`remote-jobs-scraper` `resultOrder` (added 2026-10-18, after 1529). Known limits, both written
into queue.md: it only sees DECLARED enums, so free-text `stringList` fields with a closed
real-world vocabulary are invisible -- and those are exactly where this backlog's last two real
defects came from (`offices` c1530, `orgStates` c1531); and IDENTICAL means the surface is
unchanged, never that the values still work upstream.

**3. Audited `matchMode` live and found a REAL defect -- both non-default values were documented
backwards. Fixed and live in build 0.1.88.** The mapping (`MATCH_MODE_TO_CRITERIA
{contains:C, startsWith:W, endsWith:E}`, `src/main.js:166`) and the unknown-value
fallback+warning are correct; the SEMANTICS we sold were not. Live probes (GB office, 5-10 rows,
`bin/varied-test`):
- `startsWith` (`criteria:W`) is a WHOLE-WORD match at **any** position, not a prefix:
  `"syrup"` -> `SYRUP`, `SYRUP DROPS`, `HAIR SYRUP`, `Soul Syrup`, `Coff Syrup`; `"zzle"` ->
  only `POO-ZZLE` (2nd token). Decisive: `"coff"` -> `Coff Chi`/`COFF STOP`/`Coff Syrup` and
  **not** `COFFEE` -- a prefix of a longer word is not a word.
- `endsWith` (`criteria:E`) is a PLAIN SUFFIX substring with no word boundary at all:
  `"offee"` -> `toffee`, `woffee`, `Qoffee`, `COFFEE`; `"zzle"` -> `Dizzle`, `RAZZLE`, `DAZZLE`.
The schema, README input table, README FAQ, the clearance use-case bullet AND the blog post all
claimed "a complete word at the start/end" for both, and all recommended `startsWith` for brand
clearance -- the harmful half: a clearance user searching `"coff"` with `startsWith` sees 4
marks and would conclude nothing starts with their name while `COFFEE` exists. Also corrected
the inference: the old "`solarw` returns 0 under both" evidence is NOT whole-word proof, it is
two separate facts (no WORD `solarw` for W, no name ENDING in `solarw` for E). Docs-only fix:
enumTitles -> "Whole word anywhere (startsWith)" / "Ends with these letters (endsWith)", schema
+ README state the real semantics with the probes, clearance use-case now points at `contains`,
and `site/content/blog/tmview-search-criteria-undocumented-modes.md` carries a dated Correction
section (title/description corrected too, plus the Actor README's Related-guides bullet).
VERIFIED: build 0.1.88 SUCCEEDED; live README byte-identical via the build API (80,123 both
sides); live `inputSchema` shows the new enumTitles; blog page 200 with the correction rendered;
`check-blog-claims` 0 stale; services active. `audit_dates.json` 1530 -> 2500 via the targeted
2-line edit (`git diff --stat` = 2 insertions / 2 deletions). Backlog now 19 DUE.

Method note for the next cycle: choose enum probes so the values MUST diverge. Three runs here
read "all three modes identical" because `"lux"` and `"TASTIC"` are themselves exact marks that
satisfy contains/whole-word/suffix at once, and TMview ranks exact matches first -- only a
prefix-but-not-a-word term separated them. "Identical output" is a probe-design smell before it
is a finding.

Spend this cycle: ~$0.01 (1 platform build ~$0.005 + 9 capped `varied-test` reads). 0 new
Actors. No revenue event, no owner email (rule 3 -- nothing booked, nothing only the owner can
fix). Next: `remote-jobs-scraper` `resultOrder` is the last real enum gap (~10 min); the queued
true-prefix match mode on `trademark-search-scraper` is the higher-value build; dev.to
syndication unblocks ~2026-11-01 09:31 UTC.

Updated: 2026-10-31 ~02:30 UTC by cycle 2499 (claude-sonnet-5) -- normal slot (`2499%3==1`).
Preflight: inbox 10 -- same known set as c2498 (no genuinely new mail), no owner email
warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, unchanged. `checks-due
--all` **NONE DUE** (soonest `git-maintain` in 1 cycle, cycle 2500 -- due NEXT cycle).
`audit-due --all` (`competitor_audit`) **NONE DUE** (soonest `us-federal-awards-scraper` in
140c). Services all active, `/` and `/tools/hacker-news-scraper` both 200.

**Continued the `enum_audit` backlog (c2497/c2498), closed `hacker-news-scraper` (last 1307,
~1192c/~25 days stale) -- fourth close in this backlog, same method.** Git-logged every
commit touching `.actor/input_schema.json` since 1307 by date: none change the `sortBy`
enum values -- `f63aaa39` (2026-10-11) and `83f4ba55` (2026-10-18) only touch
`minPoints`/`minComments`/`queries`/`tags` descriptions and defaults, `45f138dc`
(2026-10-21) only reformats the JSON (pretty-print, `schemaVersion` bump), and the two
enum-adjacent commits (`domainFilter` `38f73444`, `maxCommentDepth` `dd23554c`) both predate
1307. So `sortBy` (relevance/date) is unchanged since the last audit -- pure recording
staleness, not an unaudited product change (same shape as c2498's court-records-scraper
close). Re-read the mapping (`main.js:25`, `input.sortBy==='date' ? 'search_by_date' :
'search'`) to confirm no silent drift from the 1307 note -- none. Still did a live re-proof:
`bin/varied-test` on `queries:[apify] tags:[story]` with `sortBy:date` returned 5/5 strictly
descending by `createdAt` (2026-10-30 -> 2026-10-15); same query with `sortBy:relevance`
returned a points-ranked set topped by the 2012 "HackerNews API...on Apify" story (132
points) -- both values live and clearly distinguishable, matching the 1307 note. No
defects, no code/README change. Updated `audit_dates.json` (1307 -> 2499) via the same
targeted python line-replace method c2498 used (read target lines, asserted they matched
before overwriting, verified `git diff --stat` = 2 insertions/2 deletions). `enum_audit`
backlog now **20 DUE**, next target `fda-recall-scraper`.

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0 spent (two capped `varied-test` reads, no build/push). 0 new Actors today.
**Next cycle: `checks-due --all` is THE thing to run first -- `git-maintain` is due cycle
2500, which is next cycle, not a future one. Run it, then continue the `enum_audit` backlog
-- `fda-recall-scraper` is NEXT TARGET (same method: git-log every commit touching its
`.actor/input_schema.json` since its recorded `last` cycle, check if any post-dates the last
audit and adds/changes an enum value, verify reachability live via `bin/varied-test`, update
`audit_dates.json` with a targeted 2-line python line-replace). If the clock is past
2026-11-01 09:31 UTC, the dev.to syndication c2496 queued is likely higher-value than
continuing this backlog.**

---
Updated: 2026-10-31 ~02:15 UTC by cycle 2498 (claude-sonnet-5) -- normal slot (`2498%3==0`).
Preflight: inbox 10 -- same known set as c2497 (owner's duplicate CourtListener send
`2b237f1b`, owner-forwarded Apify notice `01852eaa`, DMARC pair, TinyGate x2, rental-spam
pair, cold pitch `5ce80b92`), 0 genuinely new mail, no owner email warranted. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, unchanged. `checks-due --all` **NONE DUE** (soonest
`git-maintain` in 2c, cycle 2500). `competitor_audit` (audit-due's default type) **NONE DUE**
(soonest `us-federal-awards-scraper` in 141c). Services all active, `/` and
`/tools/court-records-scraper` both 200.

**Continued the `enum_audit` backlog c2497 opened (hidden behind `audit-due`'s single-type
default).** Closed `court-records-scraper` (last 1307, 1191c/~25 days stale) using the same
method as c2497's `sec-insider-trades-scraper` close: git-logged every commit touching
`.actor/input_schema.json` since 1307 by date, found the two enum-affecting commits
(`08028218` opinionStatus "any" fix, `86f6a7fe` sortBy add) both PREDATE 1307 and were
already covered by that audit's own note; the one schema commit after 1307 (`8a5cf5d4`,
2026-10-18) only converts `query`'s `default` to `prefill`, touches no enum. So all three
enums (`recordType`, `opinionStatus`, `sortBy`) are unchanged since the last audit -- this
is pure recording staleness, not an unaudited product change. Re-read the code
(`TYPE_FOR`/`OPINION_STAT_PARAM`/`SORT_PARAM`, main.js:128/174/191) to confirm no silent
drift from the 1307 note's description -- none. Still did a live re-proof rather than just
trusting the old note: `opinionStatus:any` + `recordType:opinions` on `ca9` returned a
genuine Published/Unpublished mix (10 rows: 8 Unpublished, 1 Published); `sortBy:dateFiledAsc`
on `ca9` opinions returned 5/5 strictly ascending (`1854` -> `1892`), confirming the sort
direction works outside the `scotus` case 1307 originally tested. No defects, no code/README
change. Updated `audit_dates.json` (1307 -> 2498) via a targeted 2-line edit (Edit tool
string-match failed on this file twice due to a literal mismatch in my own retyped text, not
a file issue -- fell back to a precise python line-replace that only touched the 2 target
lines, verified via `git diff --stat` = 2 insertions/2 deletions before committing).
`enum_audit` backlog now **21 DUE**, next target `hacker-news-scraper` (last 1307, same gap).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0 spent (one capped `varied-test` read, no build/push). 0 new Actors today.
**Next cycle: `checks-due --all` fresh first (`git-maintain` due cycle 2500, imminent). Then
continue the `enum_audit` backlog -- `hacker-news-scraper` is NEXT TARGET (last 1307, same
method: git-log every commit touching its `.actor/input_schema.json` since 1307 by date, check
if any post-dates the last audit and adds/changes an enum value, verify reachability live via
`bin/varied-test`, update `audit_dates.json` with a targeted 2-line Edit). Note
`hacker-news-scraper` only has one schema enum (`sortBy`: relevance/date) so this should be a
quick close. Also still worth checking `--type unreachable_remedy` and `--type count_audit`
the same way for a hidden backlog, and if the clock is past 2026-11-01 09:31 UTC, the dev.to
syndication c2496 queued is likely higher-value than continuing this backlog.**

---
Updated: 2026-10-31 ~01:55 UTC by cycle 2497 (claude-sonnet-5) -- normal slot (`2497%3==1`).
Preflight: inbox 10 -- same known set as c2496 (owner's duplicate CourtListener send
`2b237f1b`, owner-forwarded Apify notice `01852eaa`, DMARC pair, TinyGate x2, rental-spam
pair, cold pitch `5ce80b92`), 0 genuinely new mail, no owner email warranted. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 790 runs30d (787 ok/3 bad), 0 bookmarks, 0 reviews --
unchanged. `checks-due --all` **NONE DUE** (soonest `git-maintain` in 3c, cycle 2500).
`competitor_audit` (the default `audit-due --all` type) **NONE DUE** (soonest
`us-federal-awards-scraper` in 142c). Services all active, `/` and
`/tools/sec-insider-trades-scraper` both 200.

**Found a real, previously-unworked backlog that the standard `checks-due --all`/
`audit-due --all` preflight does not surface, because `audit-due` defaults to
`--type competitor_audit` unless told otherwise.** Explicitly ran `--type enum_audit`
(per the standing rotation, `state/audit_dates.json`'s `enum_audit` key) and found **23 of
23 tracked Actors DUE**, oldest last touched cycle 1304 (~1193c / ~25 days ago, far past the
336c/7-day floor) -- a genuinely stale rotation, not the known `clean_streak`-inert false-DUE
artifact c2492 already filed (that bug means this type can never back off BEYOND the 7-day
floor once clean, but these gaps are 20-25 DAYS, i.e. this rotation has simply not been
worked in a long time regardless of the streak bug).

**Closed the NEXT TARGET, `sec-insider-trades-scraper` (enum_audit last 1304).** Read the
Actor's enum surface first (`CODE_MEANING` 20 transaction codes, `formTypes` 6 values incl.
3 amendment forms, `insiderRoles` 4 values) and found the field was stale across a real
product change: `formTypes` grew from 3 values to 6 (added `3/A`/`4/A`/`5/A` via commit
`444408af`, 2026-10-18) with no `enum_audit` record of it. **Not a from-scratch gap, though
-- checked git/varied_test history before assuming one:** the `4/A` amendment-linkage
mechanism was already thoroughly proven live under the **`varied_test`** type at cycle 2218
(single-candidate CytomX case run on-platform; the known 3-candidate TSLA ambiguity
free-verified against SEC's own XML), just never logged under `enum_audit`. **This cycle
closed the two arms 2218 did NOT platform-test: `3/A` and `5/A`.** Live `bin/varied-test`
runs across AAPL/MSFT/GOOGL/AMZN/META/NVDA/JPM/WMT/TSLA/XOM (`maxFilingsPerIssuer:200` each)
confirmed both reachable with correct `amendsOriginalFilingDate`/`supersedesAccessionNumber`
linkage -- a 2026-05-18 Form 3/A resolved cleanly, plus older 4/A/5/A hits back to
1995-1996. Also re-verified: `transactionCodes`' 20-code `CODE_MEANING` table still matches
`input_schema.json`'s enum exactly (0 drift since 1304), live rows kept decoding with 0
nulls; `insiderRoles` officer/director/tenPercentOwner reachable, `'other'` still NOT
observed live -- now across ~2000 filings scanned (10 issuers x 200) vs 1304's 120, same
"rare, not dead" conclusion on a much larger sample. **No defects found, no code/README
change needed** -- this was a genuine clean audit, just never recorded. Updated
`audit_dates.json`'s `enum_audit` field (1304 -> 2497) with the full note (minimal 2-line
diff via a targeted Edit, not a full-file JSON re-dump -- that trap bit this cycle first and
was reverted before committing). `enum_audit` backlog now **22 DUE**, next target
`court-records-scraper` (last 1307).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0 spent (capped `varied-test` runs read small samples, no build/push). 0 new Actors today.
**Next cycle: `checks-due --all` fresh first (`git-maintain` due cycle 2500, ~0.1 day out).
Then, since `competitor_audit` (audit-due's default type) is NONE DUE but `enum_audit` has a
real 22-Actor backlog just opened up by this cycle, either (a) continue it --
`court-records-scraper` is NEXT TARGET, same method: read the Actor's enum surface, diff
against git history for any enum added since its last `enum_audit`, verify reachability live
via `bin/varied-test`, update `audit_dates.json` with a targeted Edit (NOT a full json.dump
rewrite -- see the diff-noise trap this cycle hit and reverted) -- or (b) if the clock is
past 2026-11-01 09:31 UTC, the dev.to syndication c2496 queued is likely higher-value (it is
the only channel feeding distinct users, which c1608 proved moves Store rank). Also worth
checking `--type unreachable_remedy` and `--type count_audit` the same way next time the
`--all` preflight says NONE DUE -- they may hide the same kind of real backlog behind
`audit-due`'s single-type default.**

---
Updated: 2026-10-31 ~01:20 UTC by cycle 2496 (claude-opus-5) -- QUALITY/GROWTH slot (`2496%3==0`).
Preflight (all re-run fresh, not trusted from c2495 per the standing c2120 rule): `checks-due
--all` **NONE DUE** (soonest `git-maintain` in 4c, cycle 2500). `audit-due --all` **NONE DUE
across every tracked type** (soonest `us-federal-awards-scraper` `competitor_audit` in 143c,
cycle 2639). `inbox list 10`: 0 genuinely new mail -- same known set as c2495 (owner's duplicate
CourtListener send `2b237f1b`, owner-forwarded Apify notice `01852eaa`, DMARC pair, TinyGate x2,
rental-spam pair, cold pitch `5ce80b92`), so no owner email warranted (CLAUDE.md rule 3).
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 790 runs30d (787 ok / 3 bad), 0 bookmarks,
0 reviews. Services all active; `/` and `/tools/court-records-scraper` both 200.

**Checked two candidate angles before picking, and rejected both on measurement rather than
assumption:** (a) the "are the Actors even wired for PPE billing, given 534 succeeded external
runs booked $0" hypothesis is **already closed** -- `bin/check-charges` covers it and LEARNINGS
records all 25 priced Actors calling `Actor.charge()`, with the reached-ness caveat and the
`chargedEventCounts` reporting lag both already documented; do not re-open it. (b) a dev.to post
(the one channel that measurably drives off-platform traffic -> distinct users -> the ONLY input
that moves `storePosition` per c1608) is **cadence-blocked**: last syndication 2026-10-30 09:31
UTC, ~15.5h ago, against a 1-post/2-3-day cadence, so the next slot is ~2026-11-01. There are
unsynced blog slugs queued in `state/devto_syndicated.json` and ready to go -- **a dev.to
syndication is the best available growth action for the next cycle that runs after
2026-11-01 09:31 UTC.**

**Spent the cycle on the only queue item with a hard external deadline: c2478's Apify
`/v2/store` change (2026-11-15, 15 days out). Shipped the code half EARLY and found a caller
c2478's own sweep had missed.** c2478 had deferred the patch to "whenever the rank checks next
come due after the deadline", which had a hole: `store-anon-rank` is due cycle 2744
(~2026-11-05, BEFORE the change) and then not again until ~3080, so no scheduled run would have
patched it inside the window, and any ad hoc run in between would have been trusted. It also
mis-triaged the failure mode -- post-change the `offset` loops would have re-scanned page 1 up
to 4x and printed a confident `NOT FOUND`/`ABSENT` for every Actor ranked deeper than ~96, i.e.
most of the fleet (c2072 baseline #29-#354), which reads as a fleet-wide ranking collapse and
invites exactly the pointless listing-copy rewrites c1468/c2280 warn against.

What shipped (3 files + 1 new self-test):
- **`bin/store-anon-rank` + `bin/check-store-rank`** -- both now detect a dead `offset`
  **structurally** (remember each page's first `(username, name)`, stop the moment one repeats;
  needs no date check and no trust in Apify's timing) and report a third state, **UNKNOWN**
  ("deeper than page 1, unmeasurable"), never ABSENT. `data["total"]` -> `.get("total")`.
  `check-store-rank` also persists **`paging_ok` into each `state/store_rank.json` row**, since
  that history is diffed across runs and the boolean is the only thing that will let a future
  cycle tell "unmeasurable" from "really disappeared".
- **`bin/store-visibility` -- a caller c2478 MISSED, and the worst of the three.** Single-page,
  so paging was never its problem, but it indexed `d["total"]` directly: a hard KeyError
  post-change, not a degraded reading. Also fixed its `a_total == t_total` "filtered" heuristic,
  vacuously true once both totals are `None`. Re-swept the rest and c2478's SAFE verdicts hold
  (`niche-size`'s only `offset` hit is a comment FORBIDDING an offset loop; `store-rank` /
  `category-rank` are Algolia and their `offset` hits are word-offsets; `store-scan`,
  `apify-admin`, `check-rental-converts`, `check-upstream-warnings` single-page, no `total`).
- **`bin/_store_paging_selftest.py` (NEW, 3/3 pass, no network/auth, free)** -- the post-change
  behaviour cannot be tested against the live API before the date, so it fakes an
  offset-ignoring/`total`-less API and asserts each tool degrades correctly **and** still reports
  a real rank when we ARE on page 1 (that control is what catches an over-eager detector).

**Verified both directions:** live pre-change API still pages (offsets 0/90/180 on `court
records` each returned a different first item, so the repeat-detector cannot false-positive
today); `store-anon-rank "court records"` reads **#29**, exactly the c2072 baseline, and
`check-store-rank --scan 200 court-records-scraper` independently also reads **#29** plus
`pacer court` #16. The partial 2-query `check-store-rank` snapshot used for that check was
**reverted out of `state/store_rank.json`** (back to 27 snapshots, last the full 50-row
2026-10-26 one) -- a 2-row snapshot in a 50-row series would read as "48 queries vanished".

No revenue event and nothing only the owner can fix, so no owner email. $0 spent (read-only
public REST + Algolia; no builds, no pushes, no platform runs). 0 new Actors today.
**Next cycle: `checks-due --all`/`audit-due --all` fresh first (`git-maintain` due cycle 2500).
Then, if the clock is past 2026-11-01 09:31 UTC, SYNDICATE A DEV.TO POST from
`state/devto_syndicated.json`'s unsynced list -- that is the highest-value growth action
currently unblocked and it is the only channel that feeds the one metric (distinct users) that
c1608 proved moves Store rank. The remaining tooling items stay as they were: `c2464` pricer
scalar-vs-rung port (gated to the next `competitor_audit`, 143c out) and `c2492`'s MEDIUM
`clean_streak` vocabulary widening (ungated, wants a full dedicated cycle, and note it lengthens
audit intervals -- the unsafe direction). c2478's remaining open half is the AFTER-2026-11-15
upside re-measure, which is the genuinely interesting part: if a `store-anon-rank` rank jumps
into the top ~20 without `totalUsers` rising, that falsifies c2072's users-gating finding.**

---
Updated: 2026-10-31 ~00:45 UTC by cycle 2495 (claude-sonnet-5) -- normal slot (`2495%3==2`).
Preflight: inbox 10 -- 1 new item since c2494, `2b237f1b` from the owner, read in full: it is a
**duplicate/delayed send of the already-resolved CourtListener API-token ask** -- the owner
replied to the c2358 request with a token, but that exact fix (Authorization header + shared
rate-limit budget) already shipped at c2362 (`d6a0126b`) and has been live since; verified by
reading that commit and confirming `src/main.js` already sends the token, so no action needed
and no reply warranted (asking again would be the thing that costs score, not staying silent on
an already-closed thread). Other 9 mail items unchanged from c2494 (2 long-resolved threads, DMARC
pair, TinyGate x2, rental-spam pair, cold pitch `5ce80b92`, owner-forwarded Apify `01852eaa`).
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 790 runs30d; Polar gate still unmet
(`bin/traffic`: verified `/go/` out-clicks spread evenly across Actors, no new buyer-intent
signal). `checks-due --all` showed **1 DUE: `check-disclosure`** -- ran it fresh (not trusting
c2494's snapshot, per the standing c2120 rule), CLEAN (88 site blog posts + 26 dev.to articles
checked, 0 missing disclosures), recorded via `bin/checks-due --ran`. `audit-due --all`
re-confirmed NONE DUE (soonest `us-federal-awards-scraper` `competitor_audit` in 144c). Services
all active, `/` and `/tools/hacker-news-scraper` both 200.

**Spent the rest of the cycle on the two options c2494 queued, both untried-this-week and aimed
at listing quality rather than more checker work:**

**(a) CLOSED as stale -- LEARNINGS c898's `us-federal-awards-scraper` description-headroom lever
(20 free chars) no longer exists.** Read the live description via `GET /v2/acts/<id>`: it is
**299 of 300 chars**, 1 char of headroom, not 20 -- the description has clearly been edited/grown
since cycle 898 (~1600 cycles ago, as c2494's note itself suspected). No `--why`/`--desc` pass is
worth running against 1 free char. Nothing to act on; do not reopen this lever again without a
specific reason to think the description shrank.

**(b) Ran a genuine field-by-field feature diff (not another price-only sweep) on
`clinicaltrials-scraper` vs its niche's Store leader by users, `parseforge/clinicaltrials-scraper`
(48 users) -- CLOSES CLEAN, no gap found.** This axis was previously tried 3/3 times
(`trademark-search-scraper` c2107, `court-records-scraper` + `sec-insider-trades-scraper` c2110),
all closing clean; this is the 4th and still 4/4. Pulled parseforge's real README via
`GET /v2/acts/<id>/builds/<latestBuildId>` (the only place a competitor's advertised output lives
-- the Actor record and `/v2/store` search surface don't carry it). Its README does not publish
an actual field list (no sample-output JSON with field names, just prose categories: status,
phase, enrollment, eligibility, contacts, locations, posted-results dates) and is **priced 8x
higher** ($0.16 start + $0.012/result on its free tier vs our $0.0015/result flat, already
disclosed in our own README since 2026-10-03). Every category it claims is already covered by our
44-field schema: `overallStatus`/`phases` (flat, filterable), `enrollmentCount` +
`eligibilityCriteria` (eligibility), `locations`/site-mode (we deliberately omit contact people/
emails as a privacy stance, already disclosed), `resultsFirstPostDate`/`hasResults` (posted
results). CSV/JSON/Excel/XML export is an Apify platform-level dataset feature available to every
Actor regardless of code, not a competitor-specific capability, so not a real gap either.
**Takeaway, now 4/4: this fleet's established Actors were built to spec with a feature superset of
their closest rival before this axis existed (PLAYBOOK's "undercut by 20-40%, superset the
fields" build step) -- it remains a real, cheap, worth-repeating-once-per-established-Actor check,
but keep expecting it to close clean rather than treating it as a reliable source of new work.**

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3). $0
spent (all read-only: 1 fleet check, 2 API reads for the feature diff). 0 new Actors today.
**Next cycle: re-run `checks-due --all`/`audit-due --all` fresh first (c2120 rule). If still
nothing due, the standing queue items are `c2464` (pricer scalar-vs-rung port, gated to the next
`competitor_audit`, none due for ~144c) and `c2492`'s MEDIUM `clean_streak`/`CLEAN`-vocabulary
widening (ungated but wants a full dedicated cycle to hand-verify newly-nonzero streaks). With
both the description-headroom lever and now a 4th feature-diff axis closed clean, growth/quality
cycles may need a genuinely new angle rather than repeating these two -- worth a steer if the
owner has one.**

---
Updated: 2026-10-31 ~00:20 UTC by cycle 2494 (claude-sonnet-5) -- normal slot (`2494%3==1`).
Preflight: inbox 10 -- same known set as c2493 (2 long-resolved owner threads incl. the
`court-records-scraper` CourtListener-token ask closed back at c2362, DMARC pair, TinyGate x2,
rental-spam pair, cold pitch `5ce80b92`, owner-forwarded Apify `01852eaa`), 0 genuinely new
mail, no owner email warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, Polar gate
still unmet (`bin/traffic`: 3 verified visits/day to `/pricing`, 28/day to `/tools/*`, both far
under the 100/day gate; the `checkout` bucket's 2 verified hits this week are the already-known
`/checkout-soon` placeholder + a browser walking `/checkout/{starter,pro}` referrers in
sequence, the same bot-shaped artifact `bin/traffic`'s own header comment already names, NOT a
new buyer signal). `checks-due --all` **NONE DUE** (soonest `check-disclosure` in 1c).
`audit-due --all` **NONE DUE across every tracked type** (`competitor_audit` soonest in 145c,
`varied_test` soonest in 61c). `bin/devto-comments`: 26 published, 0 unanswered. Free
directories/PH/HN/Reddit/dev.to-cadence all still closed or gated exactly as c2493 found one
cycle ago -- independently re-confirmed rather than trusted from the prior cycle's note (the
standing c2120 lesson). Services all active, `/`, `/tools/hacker-news-scraper` and
`/tools/substack-scraper` all 200.

**Genuinely idle cycle by every automated measure, same as c2493 -- spent it on two more ad hoc
`varied-test` spot checks (PLAYBOOK's QUALITY-cycle method) on the next-oldest-untested input
combos, picked by grepping LEARNINGS for what this fleet has NOT yet exercised on each Actor:**
(1) `hacker-news-scraper`: `domainFilter:["github.com"]` + `excludeKeywords:["gpt"]` +
`enrichGithubLinks:true` together (each tested individually before per LEARNINGS, never
combined) -- all 3 returned rows were genuinely `github.com` URLs, none contained "gpt" in the
title, and `githubRepo`/`githubStars`/`githubLanguage` enrichment populated correctly on every
row (e.g. `kavishdevar/librepods`, 30536 stars, Kotlin). 0 defects. (2) `substack-scraper`:
`discoverCategories:["technology"]` + `leaderboardTier:"paid"` + `audienceFilter:"paid"` +
`maxPostsPerPublication:3` together (date-window and `isRestack` combos tested before per
LEARNINGS c1969/c1525, this triple-filter-plus-cap combo was not) -- all 10 rows came back
`isPaid: true`, every publication (`semianalysis`, `natesnewsletter`, `pragmaticengineer`,
`bytebytego`, `exponentialview`) stayed at or under the 3-post cap. 0 defects.
**Deliberately did NOT bump `audit_dates.json`'s `varied_test` field for either Actor** -- same
rule c2493 applied: a 2-input spot check is not the full-field sweep the rotation's own notes
require, and ticking the date without doing that work is the exact "satisfies the checker, not
the job" trap c2488 found on a different field.

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3). $0
spent (read-only platform runs, well under the $300 budget envelope). 0 new Actors today (pace
cap is 6/day). `state/revenue.json`/`revenue_history.json` auto-updated by `bin/revenue`, no
other files touched. **Next cycle: re-run `audit-due --all`/`checks-due --all` fresh first (do
not trust this snapshot -- c2120). If still nothing due, growth/quality options worth
considering instead of a third straight idle-cycle spot-check: (a) the `bin/store-price --desc`
description-headroom lever flagged in LEARNINGS c898 for `us-federal-awards-scraper` (20 free
chars) -- re-verify it's still open before spending a cycle on it, since that note is ~1600
cycles old and may be stale; (b) a from-scratch feature-gap comparison (not pricing -- PLAYBOOK's
"compare features against the top competitor Actor" instruction has mostly been satisfied via
price-only `competitor_audit` sweeps, not a real field-by-field feature diff) on one Actor.
Both are untried-this-week, bounded, and aimed at listing quality/demand rather than more
checker/tooling work, which is the steer c2492 left two cycles ago.**

---
Updated: 2026-10-30 ~23:55 UTC by cycle 2493 (claude-sonnet-5) -- normal slot (`2493%3==0`).
Preflight: inbox 20 (widened from the usual 10) -- confirmed the same known set as c2492, 0
genuinely new mail (newest is still the owner-forwarded `01852eaa`), no owner email warranted.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 790 runs30d (787 ok / 3 bad), 0 bookmarks,
0 reviews; Polar gate still unmet (`bin/traffic`: 3 verified visits/day to `/pricing`, 28/day to
`/tools/*`, both far under the 100/day gate). `checks-due --all` **NONE DUE** (soonest
`check-disclosure` in 2c). `audit-due --all` **NONE DUE across every tracked type**, not just
`competitor_audit` -- explicitly re-checked `--type varied_test` too (soonest due in 62c). This
is a genuinely idle cycle by every automated measure: no checks, no audits, no new mail, no
niche candidate (niche-hunting fleet-wide exhausted per c2306, next calendar re-try not before
2026-12-26), no dev.to slot (last syndication was THIS CALENDAR DAY, 09:31 UTC, so the
1-post/2-3-days cadence blocks another today). Services all active, `/` and
`/tools/trademark-search-scraper` both 200.

**Spent the cycle on an ad hoc "re-run platform tests with different inputs" spot check
(CLAUDE.md's QUALITY/GROWTH-cycle instruction) on the two Actors with the OLDEST formal
`varied_test` audit date (`us-federal-awards-scraper` last 2219, `trademark-search-scraper` last
2221) -- but did NOT touch `audit_dates.json`'s `varied_test` field for either, since this was a
quick 2-input check, not the full-field sweep that rotation's own notes show it actually
requires (see the enum_audit/unreachable_remedy samples in LEARNINGS) -- ticking the formal date
off this would be the exact "satisfies a checker without doing the work" trap c2488 found.**
(1) `trademark-search-scraper`: `searchTerm:"apple" matchMode:"startsWith" offices:["GB"]
niceClasses:["25"]` (none of these three filter values appear in the Actor's own
`test_input.json`). All 10 returned rows: `office:"GB"` exactly, `niceClasses` contains `"25"`
on every row, and every `trademarkName` genuinely starts with the whole word "apple"
(APPLE/APPLE PIE/Apple Milk/apple park/...) -- confirms `startsWith` mode is not silently
degrading to `contains`. (2) `us-federal-awards-scraper`: `awardLevel:"subaward"` (the
non-default branch, untested by `test_input.json` which only exercises `"prime"`via its default).
10 rows, all genuinely distinct sub-awards (`subRecipientName`/`subAwardAmount`/`subAwardDate`
all vary row to row) under one matched prime grant (`primeAwardId:"2620B109"`), with the
sub-award-shaped field set (`primeAwardId`, `subRecipientName`, `subAwardAmount`, no generic
`recipientName`) -- confirms the subaward branch reshapes output correctly rather than reusing
the prime shape. Both PASS, 0 defects found. ~$0.001 spent (2 capped 10-row runs).

**Looked for a real growth lever before defaulting to tooling and found none open right now**:
niche-hunting is fleet-exhausted (c2306, re-check gated to ~2026-12-26), Hashnode is cost-gated
($5/mo, no card approved), the 7 free launch directories are all closed, Show
HN/PH/Reddit are off-limits by standing rule, dev.to already posted today, and the
`/checkout-soon` page already funnels buyer intent to the real Apify Store checkout (so there is
no missing capture step there). This matches the observation c2492 left for a steer: the fleet's
audit/guard machinery is comprehensively caught up (confirmed again this cycle, zero DUE
anywhere) while revenue is still $0 after ~2490 cycles -- the binding constraint right now reads
as genuine lack of a new growth lever, not under-maintenance. No owner email sent (nothing only
they can fix, no revenue event, and CLAUDE.md rule 3 says asking costs score).

No revenue event, no owner email, $0 Apify spend beyond the two $0.0005 varied-test runs, 0 new
Actors today. Services/site reconfirmed healthy throughout. **Next cycle: `audit-due --all` and
`checks-due --all` first (next due: `check-disclosure` in ~1-2c, `us-federal-awards-scraper`
`competitor_audit` in ~145c).** If still nothing due, the queue's two open tooling items are
`c2464` (pricer scalar-vs-rung port, gated to the next `competitor_audit`) and `c2492`'s MEDIUM
`clean_streak`/`CLEAN`-vocabulary widening (ungated but needs its own careful hand-verified
cycle, not a rushed 25-minute one -- see the full spec already in queue.md, do not shortcut the
"hand-check newly-nonzero streaks" step).

---
Updated: 2026-10-30 ~23:30 UTC by cycle 2492 (claude-opus-5) -- QUALITY/GROWTH slot
(`2492%3==2`). Preflight: inbox 10 -- same known set as c2491 (2 long-resolved owner threads,
2x DMARC, 2x TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`,
owner-forwarded Apify `/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email
warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 790 runs30d (787 ok / 3 bad),
0 bookmarks, 0 reviews; Polar gate still unmet. `checks-due --all` **NONE DUE** (soonest
`check-disclosure` in 3c, cycle 2495). `audit-due --all` **NONE DUE** -- c2491 emptied the
backlog; soonest is `us-federal-awards-scraper` in 147c (cycle 2639). Services all active,
`/` 200. **No Actor code, price, registry or README was touched this cycle, so the price/charge
guards were deliberately NOT re-run** -- `checks-due` explicitly says "do not re-run these this
cycle; spend it on growth work", and with no build and no price edit there is nothing for them
to catch. Note the c2491 header mislabels itself `2491%3==2`; 2491%3 is actually 1. Quality
slots are `%3==2` (2483, 2486, 2489-timed-out, 2492).

**Took the two open tooling-correctness follow-ups, since `audit-due` is empty and the HIGH
c2464 pricer item is explicitly gated to "the next cycle that is about to run a
`competitor_audit`" (147c away). Both closed, and BOTH turned out to rest on a wrong premise --
measuring first is what this cycle actually bought.**

**(1) c2475 CLOSED -- benign, allowlisted.** `us-federal-awards-scraper`'s
`competitor_audit_note` UNKNOWN multi-header segment was hand-read and added to
`KNOWN_CITATIONS` in `bin/_audit_note_scan.py`, which now reads **`7 found, 0 unexplained`**
(was 1 unexplained). **c2475's root-cause guess was wrong:** the "cycle 2473: BACKFILL, not a
new sweep --" opener matches `REPORT_HEAD` fine and seg0 DOES split as its own segment (13
segments total). The extra header is a genuine mid-sentence citation of the cycle that did the
real work ("...still 1441, but cycle 2303 (commit 3c98af03, ...) already ran a full fresh
niche-unnamed resweep here..."), exactly the shape `REPORT_HEAD` is built NOT to split on.
**`REPORT_HEAD` deliberately left untouched**; the wrong guess is recorded in the code comment
so it is not retried.

**(2) c2472 CLOSED as WON'T FIX -- do NOT add `"enum_audit": "note"` to
`NOTE_KEY_OVERRIDES`.** Reasoning recorded as a comment block above `NOTE_KEY_OVERRIDES` in
`bin/audit-due`. Measured: **14 of 23 enum_audit Actors DO have `enum_audit_note`** (c2472's
Actor list was itself wrong -- ats-jobs, clinicaltrials, nih-reporter, remote-jobs,
sec-insider-trades, trademark-search carry BOTH keys), and **all 14 still score streak 0**,
which proves a missing key is not what zeroes this type. The override would change **exactly
ONE streak fleet-wide** (`shopify-products` 0 -> 1) and that one is a **cross-type
misattribution**: its bare `note` head segment scores CLEAN only on "CLEAN NEGATIVE, no code
change. This closes the fleet-oldest varied_test date (786)" -- a **varied_test** verdict
credited to `enum_audit`. Hand-read 5 bare `note` fields: the key is a **mixed multi-type
catch-all** (ats-jobs opens with a provider-reachability pass, federal-register with a
facet-diff) and app-store-reviews' is **OLDEST-first**, inverting clean_streak's newest-first
contract.

**The real root cause, filed as a new MEDIUM queue item rather than fixed today: `clean_streak`
is structurally INERT for every non-price audit type, because `CLEAN`'s vocabulary is
competitor/price-specific.** It matches only undercutter/unnamed/`clean no-op|resweep|negative`
idiom plus `zero|0 (real )?price drift` -- and those last two REQUIRE the word "price", so an
enum/reachability report's "0 drift" / "no drift" / "0 residual, still exactly 22" matches
nothing. Measured streak>0: `competitor_audit` 6/25, `watch_subset_audit` 3/13, `varied_test`
**1/25**, `enum_audit` **0/23**, `unreachable_remedy` **0/23**, `count_audit` **0/2**,
pagination/title_trade/feature_diff/description_mine 0/1 each. That is why `enum_audit` reads
23/23 DUE perpetually -- its interval never leaves BASE. **Not shipped today on purpose:
widening `CLEAN` LENGTHENS intervals (fewer audits), the UNSAFE direction, unlike the c1542 and
c2464 fixes whose bias was safe.** It needs its own cycle with a hand-check of every
newly-nonzero streak, and must handle the OLDEST-first notes.

Verified after the edits: `bin/_audit_note_scan.py` rc=0 / 0 unexplained, `audit-due --all`
still NONE DUE, `audit-due --type enum_audit` still 23 DUE / NEXT TARGET
`sec-insider-trades-scraper` -- i.e. both changes are comment/allowlist-only and moved no
rotation. Committed.

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
$0 spent this cycle (no builds, no platform runs). 0 new Actors today. **Next cycle: nothing is
due until cycle 2495 (`check-disclosure`), so pick from queue.md's standing items -- the new
c2492 `CLEAN`-vocabulary item is the highest-value one but wants a full cycle and the
hand-check described above; otherwise a genuine README/FAQ quality pass on 2-3 Actors per the
QUALITY/GROWTH rotation (use-cases, sample output, FAQ, competitor feature gaps), which the
last several quality slots have spent on tooling rather than listing copy.**

---
Updated: 2026-10-30 ~22:55 UTC by cycle 2491 (claude-sonnet-5) -- normal slot (`2491%3==2`,
competitor_audit backlog item). Preflight: inbox 10 -- same known set as c2490 (2 long-resolved
owner threads, 2x DMARC, 2x TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`,
owner-forwarded Apify `/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email
warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 790 runs30d (787 ok / 3 bad),
0 bookmarks, 0 reviews; Polar gate still unmet. `checks-due --all` NONE DUE (soonest
`check-disclosure` in 4c). `audit-due --all` showed 1 DUE, NEXT TARGET `google-news-scraper`
(last 2147) -- ran it this cycle. Services all active, `/` and `/tools/google-news-scraper`
both 200.

**Ran `google-news-scraper`'s `competitor_audit` (last 2147, 344c gap). NOT CLEAN: 9 genuine
new undercutters, 2 ruled out as decoy/start-fee-negated, 5 more tie-but-dearer.** Git-log
hidden-resweep check first (c2477 rule): only commits since 2147 are a maxResults-cap
status-message feature (0.1.87) and a 2026-10-25 stale-user-count spot-check refresh, neither
a full-cohort resweep -- gap genuinely real. Own price re-read live before comparing: flat
$0.002 FREE / $0.0018 BRONZE / $0.0015 SILVER / $0.001 GOLD+/PLATINUM/DIAMOND, single `result`
event, no start fee -- unchanged. `niche-size`: 2182 seen, 398 matched (up from 357). `niche-
unnamed`: 306 unnamed of 398 (296 NONE, 10 OWNER) against 97 already named; live-priced the
full 3+-user cohort (56 listings: 47 NONE plus 9 OWNER-bucket re-verify, the 10th OWNER match
being our own listing) via `bin/_batch_price_gn.py`, 0 unresolvable. Also ran a full rung-by-
rung check (`all_tiers` vs our own ladder at every tier) across all 56 to catch any tiered rival
whose FREE price looks dearer but undercuts lower down -- confirmed exactly the same 11
candidates the headline-price filter had already found, 0 missed.

**9 genuine new undercutters** (all start-fee crossovers computed, not just headline price):
`eiv/news-monitoring-scraper` flat $0.0002/article + $0.005 start, crosses our FREE ~3
articles/run and GOLD+ ~7; `alexmorain/google-news-scraper` $0.001->$0.0004 tiered + $0.002
start, crosses FREE ~2 articles; `andok/google-news-scraper-pr-sentiment-monitoring`
$0.001->$0.00014 tiered + $0.01 start, crosses FREE ~10 articles; `groupoject/google-news-
scraper` $0.001->$0.0008 tiered, negligible start, undercuts outright; `tidydata/google-news-
scraper` $0.001->$0.0008 tiered, no start, undercuts outright; `mina_safwat/google-news-
scraper` flat $0.001 no start, undercuts FREE/BRONZE/SILVER ties GOLD+; `getanyapi/google-news-
scraper` $0.0015->flat $0.00075 tiered, negligible start, undercuts outright; `stratumics/
google-news-scraper` $0.0015->$0.001 tiered, negligible start, undercuts FREE/BRONZE/SILVER
ties GOLD+; `pipiagent/google-news-scraper` flat $0.0015 no start, undercuts FREE/BRONZE ties
SILVER. **2 checked and ruled out:** `xtracto/google-news-scraper` ties our FREE exactly but
its $0.005 start fee makes it strictly dearer there at any volume, and its BRONZE/SILVER
crossover only clears past ~36/~29 articles with GOLD+ needing ~500 -- not a realistic win;
`punctual_understanding/my-actor-4` flags `apify-actor-start` ($0.01) as primary over a
near-$0 dataset-item charge, the same decoy shape already ruled out for `my-actor-2` at the
fifteenth sweep, and is a Reddit+Google-News Korea/global trend scraper, a different-shape
product. **5 more tie at FREE only, dearer everywhere else, not counted:** `eesti` (+$0.02
start, dearer at every volume), `fguiraud` (tiers only to $0.0016 GOLD+), `piotrv1001` and
`plumblinedata` (flat $0.002, no tiers), `mahogany_songbird/news-sitemap-parser` (different
shape -- sitemap-XML parser, not keyword search).

Shipped README paragraph (sixteenth sweep), build **0.1.88** (package.json 0.1.22 -> 0.1.23);
live README confirmed **byte-identical** (57,924 bytes both sides) via the build's `readme`
field. Guards after: `check-charges` 25/0/0; `check-registry-fields` 0 drift; `check-own-price-
prose` 0 flags; `check-price-superiority` **2475 named-rival prices compared** (2459 at c2490),
**0 undisclosed anywhere**, same 12 pre-existing UNIT-MISMATCH advisories (none on this Actor).
Recorded in `audit_dates.json` (2147 -> 2491). **`audit-due --all` now shows ZERO DUE across
the whole fleet** -- the competitor_audit backlog that has run one-per-cycle since roughly
c2473 is now fully current; next due is `us-federal-awards-scraper` at cycle 2639 (~3.1 days
out). This closes out the standing "work the backlog down" queue item.

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today. **Next cycle: with
the audit backlog empty, pick up the standing LOW/MEDIUM follow-ups still open in queue.md**
(the c2464 scalar-vs-rung `_batch_price_*.py` port, the c2475 `_audit_note_scan.py` UNKNOWN
segment, the c2472 bare-`note`-key `enum_audit` fix, or -- since this is now also effectively a
QUALITY-shaped moment -- a README/FAQ pass on 2-3 Actors per the standing QUALITY/GROWTH
rotation) rather than starting a new sweep that isn't due yet.

---
Updated: 2026-10-30 ~22:20 UTC by cycle 2490 (claude-sonnet-5) -- recovery cycle (cycle 2489
timed out at rc=124 after 28 minutes, uncommitted). Preflight: inbox 10 -- same known set as
c2488 (2 long-resolved owner threads, 2x DMARC, 2x TinyGate pitch, Actor-rental + IP-lease spam,
cold pitch `5ce80b92`, owner-forwarded Apify `/v2/store` notice `01852eaa`), 0 genuinely new
mail, no owner email warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 789
runs30d (786 ok / 3 bad), 0 bookmarks, 0 reviews; Polar gate still unmet. `checks-due --all`
NONE DUE (soonest `check-disclosure` in 5c). `audit-due --all` showed 1 DUE, NEXT TARGET
`google-news-scraper` (last 2146) -- left for the next cycle, see below. Services all active,
`/`, `/tools/grants-gov-scraper` and `/tools/uk-find-a-tender-scraper` all 200.

**Recovered cycle 2489's unfinished work rather than starting fresh.** c2489 had run the c2484/
c2488 queue item to completion data-wise (a `niche-size` sweep across ALL 25 Actors, scratch
output left at `/tmp/niche_claims.txt`) and had already edited 2 READMEs to fix genuinely stale
LEAD niche-size claims, but hit rc=124 (timeout) before committing or pushing -- left
`actors/grants-gov-scraper/README.md`, `actors/uk-find-a-tender-scraper/README.md`,
`state/revenue.json` and `state/revenue_history.json` modified and uncommitted. Verified both
README edits were correct (re-ran `niche-size`, both print `MATCHES`, so neither tripped the
c2488-documented bolding trap), pushed README-only builds (`grants-gov-scraper` 0.1.82,
`uk-find-a-tender-scraper` 0.1.94), confirmed both byte-identical live via the builds API, and
ran the standard guards clean: `check-charges` 25/0/0, `check-registry-fields` 0 drift,
`check-own-price-prose` 0 flags, `check-price-superiority` 2459 named-rival prices compared
(2460 at c2488 -- expected minor churn), 0 undisclosed anywhere (same 12 pre-existing
UNIT-MISMATCH advisories, none on these 2 Actors).

**The full fleet-wide `niche-size` sweep this closes out found the c2484/c2488 item's premise
was narrower than it looked: only 3 of 25 Actors carry ANY parseable total-niche-size lead
claim at all** (the other 22 print "no parseable total-count claim found" -- most Actors simply
don't have this lead-paragraph shape in their Pricing section). `nih-reporter-scraper` was
already fixed at c2488. This cycle finished the other 2 genuine instances: `grants-gov-scraper`
lead corrected **84 -> 142** Store listings mention grants.gov (superseded figure named in
place, per the standing "correct rather than quietly re-date" rule) and `uk-find-a-tender-
scraper` lead corrected **110 -> 206** Store listings mention UK tenders (same). **A 4th hit,
`court-records-scraper` (`DIFFERS by +95`, claims 65 vs live 160), turned out to be a FALSE
POSITIVE and was deliberately left unfixed:** its only match is `niche-size`'s `CLAIM_PATTERNS`
regex `all (\d+) listings` firing on README.md:222's "all 65 listings this run's `niche-unnamed`
returned were already covered by owner above" -- a factually-correct historical sentence about
how many UNNAMED listings one specific 2026-10-09 sweep returned, not a claim about total niche
size. Editing that "65" to anything else would make a true sentence false. **This downgrades
the c2484/c2488 plan to "promote the DIFFERS line into a real fleet check in
`state/fleet_checks.json`"**: with only 3 real total-niche claims fleet-wide (now all current)
the signal is too sparse to justify a dedicated cadence entry today, and building one without
first excluding this `all N listings ... niche-unnamed returned` shape would nag forever on
`court-records-scraper`. Full detail and the queue closure are in `queue.md`.

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.01 spent this cycle (two README-only builds). 0 new Actors today. **Next cycle:
`google-news-scraper`'s `competitor_audit`** (last 2146) -- same standing method as every prior
sweep in this backlog (git-log hidden-resweep check first, own price read live before comparing,
`niche-size` + `niche-unnamed` resweep, live-price the full unnamed cohort, re-price OWNER
handles under their own IDs, guards, record).

---
Updated: 2026-10-30 ~21:15 UTC by cycle 2488 (claude-opus-5) -- normal slot (`2488%3==1`).
Preflight: inbox 10 -- same known set as c2487 (2 long-resolved owner threads, 2x DMARC, 2x
TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`, owner-forwarded Apify
`/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email warranted. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 774 runs30d (771 ok / 3 bad), 0 bookmarks, 0 reviews;
Polar gate still unmet. `checks-due --all` NONE DUE (soonest `check-disclosure` in 7c).
`audit-due --all` showed 2 DUE, NEXT TARGET `nih-reporter-scraper` (last 2145, 343c gap) -- ran
it this cycle. Services all active, `/` and `/tools/nih-reporter-scraper` both 200.

**Ran `nih-reporter-scraper`'s `competitor_audit` (last 2145, 343c gap). NOT CLEAN: 1 genuine new
undercutter, and it is now the cheapest in-scope listing in the niche.** Git-log hidden-resweep
check first (c2477 rule): the only commits touching this Actor since 2145 are varied_test and
disclosure/clamp work (projectNums exclusive-mode warning, all-invalid `fiscalYears` refusal,
`Actor.fail()` statusMessage, two clamp-reserve commits) -- none a full-cohort resweep, so the
gap is genuinely real. Own price re-read live via `GET /v2/acts/<id>` BEFORE comparing anything:
flat **$0.0015/result** on every tier, single primary `result` event, no start fee, unchanged --
no tiered block at all, so the c2464 scalar-vs-rung bug class does not apply.

`niche-size`: 1504 seen, **64 matched** (61 at 2145 -- modest real growth). `niche-unnamed`: 7
unnamed of 64 (5 NONE, 2 OWNER -- both OWNER rows are our own `fetchsmith` listings), so **5
genuinely unnamed**. No `>=3`-user head among them, but per the cycle-1260 rule the whole cohort
was live-priced anyway via new `bin/_batch_price_nih2.py` (modeled on `cts4.py`), 0 unresolvable,
0 pure run-fee, nothing ruled out on its title.

**1 new undercutter, unit-matched per project row: `pushbuild/nih-research-grants`** (2 users,
Actor filed 2026-10-14, its pricing record filed **2026-10-29** -- the day before this audit, a
new arrival not a miss) charges a flat **$0.0005 per funded project with NO start fee**: one
third of our rate at every tier and, with no per-run fee to amortise, cheaper than us from row 1.
A direct substitute, not a false match -- its own description is "Search every NIH-funded
research project (RePORTER)" with the same topic/fiscal-year/org/PI/state/institute/award-size
filter set. It is now cheaper than `themineworks`, `publicmoney` AND c2145's `one_dollar_store`,
i.e. the cheapest in-scope RePORTER listing in the sweep. 2 more are in-scope but dearer at every
tier: `pj_pai/nih-grants-search` (filed 2026-10-28) flat $0.003/grant no start fee, and
`pandadad0214/grants-finder` (filed 2026-10-29, Grants.gov-first but also returns funded NIH/NSF
awards) $0.003 FREE -> $0.0021 GOLD+ plus $0.00005 start -- **note it filed a SECOND pricing
record effective 2026-10-30 converting its original flat $0.003 into that ladder, and the ladder
is what was compared.** 2 are out-of-scope false matches: `agents001/sbir-sttr-awards-feed`
(SBIR/STTR leads; $0.003 FREE -> $0.0015 GOLD+ + $0.00005 start, so it only TIES us at its best
tier and the start fee leaves it dearer) and `litezero/clinical-trials-gov-scraper`
(ClinicalTrials.gov -- checked and it is already named and disclosed as cheaper-from-BRONZE-up in
our own `clinicaltrials-scraper` README, so not a cross-niche miss).

**Also closed the c2484 stale-LEAD-claim item for this Actor, and it turned up a real trap.** The
Pricing lead still said "51 Store listings mention" from 2026-10-06 while `niche-size` had been
printing `DIFFERS by +13` on every run since c2145. Corrected IN PLACE to 64 with the superseded
51/48/61 figures named and the rest of that dated paragraph explicitly scoped to its original
51-listing cohort; the "Seven rival listings genuinely beat us" count was corrected to nine the
same way, naming `one_dollar_store` (c2145) and `pushbuild` (c2488). **Trap: writing the
corrected figure as `**64** Store listings mention` BREAKS `niche-size`'s `CLAIM_PATTERNS`** (the
regex needs whitespace immediately after the digits), and the check fails OPEN -- it reverts to
"no parseable total-count claim found", a quiet pass. Caught by reading the post-edit re-run,
which now prints `README claims: 64 (MATCHES)`. Logged in LEARNINGS as the general rule: when an
edit exists to satisfy a prose-parsing checker, require the checker to say the affirmative thing,
not merely to stay silent. That is 2 of 2 audited Actors found with a stale lead, so queue.md now
asks for the DIFFERS line to be promoted to a real `fleet_checks.json` cadence.

Shipped README-only build **0.1.66** (package 0.1.19 -> 0.1.20); live README confirmed
**byte-identical** (55,550 bytes both sides) via the build's `readme` field. Guards after the
edit: `check-price-superiority` **2460 named-rival prices compared** (2180 at 2145), **0
undisclosed anywhere** (12 UNIT-MISMATCH advisories all pre-existing on trademark-search /
us-federal-awards / website-screenshot, none on this Actor); `check-charges` 25/0/0;
`check-registry-fields` 0 drift; `check-own-price-prose` 0 flags; `check-comparison-breadth` 0
narrow; `check-readme-samples` 0 drift; `check-meta-fields` 0 stale; `check-expired-dates` 11
past-date claims, 0 unresolved. Recorded in `audit_dates.json` (2145 -> 2488). `audit-due` now
shows **1 DUE**, next target **`google-news-scraper`** (last 2146).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today.
**Next cycle: `google-news-scraper`'s `competitor_audit`** (last 2146) -- same method (git-log
hidden-resweep check first, own price read live before comparing, `niche-size` + `niche-unnamed`
resweep, live-price the full unnamed cohort, re-price OWNER handles under their own IDs, guards,
record). Note c1475 burned a cycle re-running this exact niche 18h after c1438, so read the
existing `competitor_audit_note` before sweeping. `bin/_batch_price_nih2.py` kept in `bin/` as a
dated record per every prior per-niche pricer copy's own convention.

---
Updated: 2026-10-30 ~21:00 UTC by cycle 2487 (claude-sonnet-5) -- normal slot (`2487%3==0`).
Preflight: inbox 10 -- same known set as c2486 (2 long-resolved owner threads, 2x DMARC, 2x
TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`, owner-forwarded Apify
`/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email warranted. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 773 runs30d, 0 bookmarks, 0 reviews; Polar gate still
unmet. `checks-due --all` NONE DUE. `audit-due --all` showed 3 DUE, NEXT TARGET
`clinicaltrials-scraper` (last 2144, 342c gap) -- ran it this cycle. Services all active, `/`
and `/tools/clinicaltrials-scraper` both 200.

**Ran `clinicaltrials-scraper`'s `competitor_audit` (last 2144, 343c gap). NOT CLEAN: 5 genuine
new undercutters.** Git-log hidden-resweep check first (c2477 rule): only commits since 2144
are disclosure/feature work (billing clamp, `Actor.fail()` reserve, dedupe fix, `whyStopped`
shipped, facility-scope disclosure), none a full-cohort resweep -- gap genuinely real. Own price
re-read live via `GET /v2/acts/<id>`: flat $0.0015/result, single primary `result` event, no
start fee, unchanged -- c2464 scalar-vs-rung bug does not apply (flat, not scalar-vs-rung).

`niche-size`: 379 seen, **206 matched** (up from 182 at 2144). `niche-unnamed`: 125 unnamed (116
NONE, 9 OWNER), README named 87 handles. A `>=3`-user head exists (6 listings; `atomus/
leads-finder`, 209 users, excluded as a generic B2B lead-finder out of scope on product), so
per the cycle-1260 rule the full 124-listing unnamed cohort (125 minus our own listing) was
live-priced via new `bin/_batch_price_cts4.py` (modeled on `cts3.py`), 0 unresolvable, 0 pure
run-fee.

**5 new undercutters, all unit-matched per study/result row:** `lucacelli/
clinical-trials-fda-drug-safety-intel` flat **$0.0008**, no start fee -- but resells biotech
sponsor/contact data, closer to the PII-reselling shape we deliberately don't ship;
`manageable_gully/clinical-trials-scraper` flat **$0.001** ("$1/1k studies") plus a $0.0003
start fee, explicitly "No contact persons" same stance as us; `exuberantal/
clinicaltrials-fda-pharma-biotech-leads-scraper` and `trusted_tech_spot/
clinicaltrials-gov-research-studies-scraper` both carry **no pricing record at all** ($0 today,
can be priced any time without notice); `jpopendata/us-clinical-trials` ties us exactly at FREE
($0.0015) then crosses under at **$0.00135 (BRONZE) down to $0.00105 (GOLD+/PLATINUM/DIAMOND)**
-- explicitly "No investigator names or contacts," same no-PII stance as us. All 5 read from
each rival's own live pricing record and disclosed in a new 2026-10-30 cycle-update paragraph
in the README Pricing section.

Shipped README-only build **0.1.94** (package 0.1.33 -> 0.1.34); live README confirmed
**byte-identical** (67,819 bytes both sides) via the `/v2/acts/<id>/builds/<buildId>` `readme`
field (note: this build's response had `readme` as a direct string field, not nested under
`sourceFiles` the way c2464 found on a different Actor -- the shape apparently varies by
request/build state, so check both before concluding a byte mismatch is real). Guards:
`check-price-superiority` 0 undisclosed anywhere, `check-charges` 25/0/0, `check-registry-fields`
0 drift, `check-own-price-prose` 0 flags. Recorded in `audit_dates.json` (2144 -> 2487).
`audit-due` now shows **2 DUE**, next target **`nih-reporter-scraper`** (last 2145, 342c gap).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today. Services/site
reconfirmed healthy (all 3 active, `/` and `/tools/clinicaltrials-scraper` both 200).
**Next cycle: continue the backlog with `nih-reporter-scraper`'s `competitor_audit`** -- same
method (git-log hidden-resweep check first, own-price read live before comparing, `niche-size`
+ `niche-unnamed` resweep, live-price the full unnamed cohort, re-price OWNER handles under
their own IDs, guards, record). `bin/_batch_price_cts4.py` kept in `bin/` as a dated record per
every prior per-niche pricer copy's own convention.

---
Updated: 2026-10-30 ~20:10 UTC by cycle 2486 (claude-sonnet-5) -- QUALITY/GROWTH slot
(`2486%3==2`). Preflight: inbox 10 -- same known set as c2485 (2 long-resolved owner threads,
2x DMARC, 2x TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`,
owner-forwarded Apify `/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email
warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 773 runs30d, 0 bookmarks, 0
reviews; Polar gate still unmet. `checks-due --all` showed ONE DUE (`check-source-endpoints`) --
ran it first (CLEAN: 50 unique hosts probed, 0 deviation, same 3 standing exemptions). Services
all active, `/` and `/tools/court-records-scraper` both 200.

**Honored the c2485 handoff explicitly: this QUALITY/GROWTH slot proactively trimmed
`state/STATUS.md` and `tasks/queue.md`, both flagged TRIM SOON by `check-doc-size` three
cycles running (c2483/c2484/c2485) without yet escalating to DUE.** `audit-due --all` showed 3
DUE (`clinicaltrials-scraper` NEXT TARGET), but per this cycle's own judgment the trim was
chosen over another sweep: the backlog is a standing rotation that will still be there next
cycle regardless, while the doc-size flag had now been deferred three cycles running and both
files had grown past their last-measured sizes again (STATUS.md 140KB/1826L at c2485's own
measurement -> 147.7KB/1843L by the time this cycle ran; queue.md 105KB/1174L -> 111.8KB/1247L).

**STATUS.md**: wrote `bin/_trim2486.py`, the same keep-newest-N-blocks method as
c1836/.../c2459. 30 cycle blocks, strictly newest-first (2485 down to 2454, same two gaps at
2472/2468 already present since the c2459 trim -- their content was folded into adjacent
cycles' blocks at the time, not lost). Kept the newest 5 (2481..2485) live, archived the other
25 (2454..2480) verbatim to `state/STATUS_ARCHIVE.md` under a dated header. **147.7KB/1843L ->
24.6KB/325L.** Independently verified lossless: every non-blank line of the pre-trim file
traces to either the new live file or the archive (0 missing of 1843 lines checked).

**queue.md**: wrote `bin/_trim2486q.py`, the hoist-then-cut method (c2161/.../c2459) since this
file interleaves standing `- [ ]` open items among `- [x]` DONE cycle blocks -- a naive
line-number cut would have deleted live open work. Kept the single newest DONE block (cycle
2485) live, hoisted all **23** genuinely-still-open items verbatim in source order (the c2478
Apify deadline item, the c2484 README-lead-claim generalisation, the c2464 HIGH
scalar-vs-rung-port note, the c2464 TRIVIAL build-endpoint note, the standing
`competitor_audit` backlog pointer, the c2475/c2472 LOW audit-note-scan items, five LOW gated
follow-ups [c2456/c2436/c2396/c2392/c2388/c2385], the c2383 standing method, the c2380 ACTIVE
growing-niches rotation, the c2336 standing tripwire, c2332, the c2312 UNPUSHED-code-fix item,
two standing process lessons, c2196, c2168/c2268, and c2371 DMARC), archived every other DONE
block (31 ranges) plus 2 items that explicitly mark themselves STALE/CLOSED in their own text
(the c2467-superseded diagnosis and the c2396 CLOSED groupBy note), and **dropped** (did not
carry forward) the one item this trim itself fulfills -- the c2483 doc-trim follow-up that
asked for exactly this work. **111.8KB/1247L -> 33.4KB/361L.** Independently verified lossless:
every non-blank line of the pre-trim file traces to either the new live file or the archive,
except the 9 lines of the intentionally-dropped c2483 request (checked by name, confirmed
absent from both live and archive as intended, not lost by accident).

`check-doc-size` re-run after both trims: **OK on all three docs** (STATUS.md 24.6KB/325L,
~40c headroom; queue.md 33.4KB/361L, ~31c headroom; LEARNINGS.md unchanged, 6782/8000 lines).
Recorded both `check-source-endpoints` and `check-doc-size` in `fleet_checks.json`. Both
one-shot trim scripts kept in `bin/` as a dated record, per every prior trim's own convention
(`_trim2459.py`, `_trim2411.py`, etc. are all still present).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3). $0
spent this cycle (read-only trim + one fleet check, no builds/platform runs). 0 new Actors
today. Services/site reconfirmed healthy (all 3 active, `/` and `/tools/court-records-scraper`
both 200). **Next cycle: continue the backlog with `clinicaltrials-scraper`'s
`competitor_audit`** (last 2144, 342c gap per `audit-due`) -- same method (git-log
hidden-resweep check first, own-price read live before comparing, `niche-size` +
`niche-unnamed` resweep, live-price the full unnamed cohort via its existing
`_batch_price_*.py`, re-price OWNER handles under their own IDs, guards, record).

---
Updated: 2026-10-30 ~19:55 UTC by cycle 2485 (claude-sonnet-5) -- normal slot (`2485%3==1`).
Preflight: inbox 10 -- same known set as c2484 (2 long-resolved owner threads `dc593cfb`/
`2b237f1b`, 2x DMARC, 2x TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`,
owner-forwarded Apify `/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email
warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 773 runs30d, 0 bookmarks, 0
reviews; Polar gate still unmet. `checks-due --all` NONE DUE. `audit-due --all` showed 4 DUE,
NEXT TARGET `court-records-scraper` (last 2141, 343c gap) -- ran it this cycle. Services all
active, `/` and `/tools/court-records-scraper` both 200.

**Ran `court-records-scraper`'s `competitor_audit` (last 2141, 343c gap). NOT CLEAN: 2 genuine
new in-scope undercutters + 4 jurisdiction-excluded undercutters.** Git-log hidden-resweep
check first (c2477 rule): only commits since 2141 are disclosure-only/feature work (billing
clamp, unknown-court-id disclosure, mode-scope warning, closing 3 `check-competitor-claims`
flags), none a full-cohort resweep -- gap genuinely real. Own price re-read live via
`GET /v2/acts/<id>`: flat $0.002/result, single primary `result` event,
`eventTieredPricingUsd` absent, no start fee, unchanged since 2026-09-17 -- c2464
scalar-vs-rung bug does not apply, `bin/_batch_price_crs.py`'s flat `OURS` already matches.

`niche-size`: 6,817 seen, **160 matched** (up from 156 at the 2026-10-23 prose sweep).
`niche-unnamed`: 67 unnamed (8 NONE, 59 OWNER incl. self); **all 66 non-self handles
live-priced, 0 unresolvable.**

**2 genuine new in-scope undercutters:** `rbbscrap/fast-courtlistener-docket-scraper` has
**no pricing record at all** -- a real $0 competitor on CourtListener's own data, but federal
PACER dockets only, no state courts, no opinions (narrower than our dockets+opinions,
3,359-court scope). `parseforge/courtlistener-civil-cases-scraper` (part of this vendor's
already-named single-purpose family) is dearer on Free/Bronze/Silver but crosses under us on
Platinum ($0.00189) and Diamond ($0.00168), civil-dockets-only scope.

**4 undercut on price but out of scope on jurisdiction** (same disclosure convention since the
2026-10-08 sweep): `orange_briefcase_hrj/austria-case-law-search` + `.../german-case-law-search`
(new vendor, Austria + Germany, every tier $0.001->$0.0008), `jungle_synthesizer/
canlii-canadian-case-law-scraper` (Canada, undercuts Silver up), `steadfetch/
cendoj-jurisprudence-monitor` (5th Spanish CENDOJ rival, every tier $0.0015->$0.0012).

4 more NONE handles are dearer or a different product (`nabeelbaghoor/court-records-case-law-
api`, `groundplanes/courtlistener-bankruptcy-dockets`, `enterprising_hamster/
polish-court-judgments-saos` [Poland, a new country for this niche, dearer], `tudorlane/
adverse-media-watch` [KYC screening, not a court-records product]). Remaining 57 of 66 dearer,
already covered by an owner named above.

Shipped README-only build **0.1.74** (package 0.1.24 -> 0.1.25); live README confirmed
**byte-identical** (71,440 bytes both sides) via the `/v2/acts/<id>/versions/0.1` `sourceFiles`
endpoint. Guards: `check-price-superiority` **2,454 named-rival comparisons / 933 cheaper / 0
undisclosed anywhere** (up from 2,444/929), `check-charges` 25/0/0, `check-registry-fields` 0
drift, `check-own-price-prose` 0 flags. Recorded in `audit_dates.json` (2141 -> 2485).
`audit-due` now shows **3 DUE**, next target **`clinicaltrials-scraper`** (last 2144, 341c gap).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today. Services/site
reconfirmed healthy (all 3 active, `/` and `/tools/court-records-scraper` both 200).
**Next cycle: continue the backlog with `clinicaltrials-scraper`'s `competitor_audit`** -- same
method (git-log hidden-resweep check first, own-price read live before comparing, `niche-size`
+ `niche-unnamed` resweep, live-price the full unnamed cohort via its existing
`_batch_price_*.py`, re-price OWNER handles under their own IDs, guards, record). **Still
outstanding: the next QUALITY/GROWTH slot (cycle 2486) should proactively trim
`state/STATUS.md` (now ~140KB/1,826L) and `tasks/queue.md` (~105KB/1,174L)** -- `check-doc-size`
called both TRIM SOON at c2483 and they have grown further since.

---
Updated: 2026-10-30 ~19:12 UTC by cycle 2484 (claude-opus-5) -- normal slot (`2484%3==0`).
Preflight: `inbox list 10` -- same known set as c2482/c2483 (2 long-resolved owner threads
`dc593cfb`/`2b237f1b`, 2x DMARC, 2x TinyGate pitch, Actor-rental + IP-lease spam, cold pitch
`5ce80b92`, owner-forwarded Apify `/v2/store` notice `01852eaa`), **0 genuinely new mail**, no
owner email warranted. `bin/revenue`: **$0 booked**, 25 public Actors, 47 users, 773 runs30d, 0
bookmarks, 0 reviews; Polar gate still unmet. `checks-due --all` showed **2 DUE** and
`audit-due --all` **5 DUE** -- ran both checks first, then the backlog's NEXT TARGET.

**Both DUE fleet checks CLEAN.** `check-row-floor`: 24 live Actors against a 6.5h-old health
timestamp, every one returned >=60% of its requested cap and none declined from its own
observed best. `check-upstream-warnings`: 23 niches swept base-term, 10,917 listings seen /
5,968 in-niche, no rival advertises a NEW upstream shutdown/deprecation/migration; the same 7
acknowledged hits re-appeared with unchanged fingerprints (3x steam `appreviews`, 3x
`practical_ai_lab_jp` catalog-"migration" false positives, 1x `groupoject` deprecating its own
listing). Both recorded, next due cycle 2532.

**Ran `trademark-search-scraper`'s `competitor_audit` (last 2139, 345c gap). NOT CLEAN: 1
genuine new undercutter.** Git-log hidden-resweep check first (c2477 rule): the only commits
touching this Actor since 2139 are c2384's one-term recheck and c2405's user-count fix, neither
a full-cohort sweep, so the formal gap stood and the sweep was genuinely due. Own price re-read
live BEFORE comparing: flat **$0.002/result on every tier**, single primary `result` event,
`eventTieredPricingUsd` **absent**, no start fee -- so the standing c2464 scalar-vs-rung bug
does not apply here (`_batch_price_tms3.py` sets OURS flat across all 6 tiers). `niche-size`:
2,401 distinct listings seen, **154 matched** (up from 145 at c2139). The README's lead
paragraph still claimed **114-of-543 from 2026-10-06** -- corrected in place to 154/2,401 with
the superseded reading named, not quietly re-dated. `niche-unnamed`: 9 never-named handles (7
NONE, 2 OWNER); **all 9 live-priced, 0 unresolvable, 0 AMBIGUOUS**, and both OWNER handles were
re-priced under their own Actor IDs rather than inheriting a sibling's verdict.

The one undercutter: **`alexmorain/inpi-trademark-scraper`** tiers **$0.001 (FREE) / $0.00085
(BRONZE) / $0.0007 (SILVER) / $0.0005 (GOLD+)** plus a $0.002 start -- half our rate on FREE, a
quarter on the top three tiers, crossover ~2 rows. It searches **France's INPI register** (FR
plus EU and international marks with French effect) and **runs on the buyer's own free INPI
account** where we are keyless; one office against our 70+ in one call. 5 more are in scope and
dearer at every tier: `olliolli/eu-trademark-watch` ($0.03 + $0.05 start, 15x, EUIPO+Benelux via
TMview -- the closest to us by source), `atesen-software/trademark-phrase-risk-check`
($0.05/phrase, 25x), `chaptersoft/trademark-watch` ($0.01->$0.008, 4-5x),
`maliksaid/uspto-trademark-watch` ($0.006, 3x), `barefoot_grade/uspto-trademarks-scraper`
($0.004 + $0.005 start, 2x). 3 left the niche on scope read from their own descriptions, and
notably **only one of those three was even cheaper per unit**:
`ahmed_jasarevic/importyeti-scraper` ($0.0012->$0.0011, but ImportYeti customs bill-of-lading
profiles in which "trademarks" is one field -- same exclusion already applied to
`crawlerbros/importyeti-scraper`), `vncntlabs/amazon-book-tshirt-niche-analyzer` ($0.15/analysis)
and `parseforge/colorado-business-registry-scraper` ($0.0045->$0.0024).

**PRICE HELD flat $0.002/result, and the 2026-10-16 revisit trigger did NOT fire** -- that
trigger needs a MULTI-OFFICE undercutter, a `foxlabs/euipo-trademark-data` cut below $0.002, or
a disclosed undercutter crossing 20 users. `alexmorain` is single-register (INPI's own
France-centric database even where it returns EU/WIPO marks), sits at the 2-user floor like
every other undercutter in this niche, and carries a buyer-credential requirement we do not --
so it is the niche's fourth single-scope undercutter, and shaving our rate fleet-wide would give
up margin without closing its only real gap on us, which is scope.

Shipped README-only build **0.1.87** (package 0.1.24 -> 0.1.25); live README confirmed
**byte-identical** (79,458 bytes, md5 match both sides) via the `/v2/acts/<id>/versions/0.1`
`sourceFiles` endpoint, per the c2482 gotcha about the build record's `readme` field truncating
large files. Guards all clean: `check-price-superiority` **2,444 named-rival comparisons / 929
cheaper / 0 undisclosed anywhere** (up from 2,435/927), `check-charges` 25/0/0,
`check-registry-fields` 0 drift, `check-own-price-freshness` 25/0, `check-own-price-prose` 0
flags. Recorded in `audit_dates.json` (2139 -> 2484). `audit-due` now shows **4 DUE**, next
target **`court-records-scraper`** (last 2141, 343c gap).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today. Services/site
reconfirmed healthy (all 3 active, `/` and `/tools/trademark-search-scraper` both 200, the tool
page still quoting $0.002/result). **Next cycle: continue the backlog with
`court-records-scraper`'s `competitor_audit`** -- same method (git-log hidden-resweep check
first, own-price read live before comparing, `niche-size` + `niche-unnamed` resweep, live-price
the FULL unnamed cohort via its existing `_batch_price_*.py`, re-price OWNER handles under their
own IDs, guards, record). **Still outstanding: the next QUALITY/GROWTH slot (cycle 2486) should
proactively trim `state/STATUS.md` (now ~137KB/1,710L) and `tasks/queue.md` (~104KB/1,163L)** --
`check-doc-size` called both TRIM SOON at c2483 and they have grown since.

Updated: 2026-10-30 ~18:50 UTC by cycle 2483 (claude-sonnet-5) -- QUALITY/GROWTH slot
(`2483%3==2`), but `audit-due --all` showed 6 DUE so per the c2474/c2477/c2480 precedent
(sweeps are maintenance rotation, not slot-gated growth work) ran the backlog's NEXT TARGET
instead. Preflight: inbox 10 -- same known set as c2482 (2 long-resolved owner threads
`dc593cfb`/`2b237f1b`, 2x DMARC, 2x TinyGate pitch, Actor-rental + IP-lease spam, cold pitch
`5ce80b92`, owner-forwarded Apify `/v2/store` notice `01852eaa`), 0 genuinely new mail, no
owner email warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 773 runs30d, 0
bookmarks, 0 reviews; Polar gate still unmet. `checks-due --all` showed ONE DUE
(`check-doc-size`) -- ran it first: TRIM SOON on both `state/STATUS.md` (128.5KB/1635L) and
`tasks/queue.md` (98.5KB/1121L), not DUE yet but projected to cross the trim line before the
next scheduled look -- recorded only, next due cycle 2507, flagged for a QUALITY slot to trim
proactively per the c2220 rule. `audit-due --all` showed 6 DUE, NEXT TARGET
`uk-find-a-tender-scraper` (last 2137, 346c gap) -- ran it this cycle. Services all active,
`/` and `/tools/uk-find-a-tender-scraper` both 200.

**Ran `uk-find-a-tender-scraper`'s `competitor_audit` (last 2137, 346c gap). NOT CLEAN: 10
genuine new undercutters.** Git-log hidden-resweep check first (c2477 rule): the only commit
touching this Actor since 2137 is cycle 2380's `db321045`, a one-term store spot-check (76
listings, 7 rivals named) that does not cover the full unnamed cohort, so per the c2477 rule
it does not retire the formal gap -- the sweep was genuinely due. Own price re-read live
first: tiered **$0.003 (FREE) -> $0.0025 (GOLD+)**, Bronze $0.0028, Silver $0.0026, no start
fee, matches `meta.json` (`check-own-price-freshness` 25/0). `bin/_batch_price_uktft2.py`
already compares rung-for-rung via `_unit_price.tiers_of`, so the standing c2464
scalar-vs-rung bug does not apply here -- confirmed, not assumed.

Fresh 15-term niche-size: **207 matched** (up from 178), 1742 seen. `niche-unnamed`: **66
unnamed of 207** (62 NONE, 4 OWNER incl. our own listing). All **65** non-self handles
live-priced via `bin/_batch_price_uktft2.py`, 0 unresolvable.

**10 genuine new undercutters, with crossover worked out the same way as every prior entry
on this README (our 25-free-row allowance, then any start fee, against their per-row rate at
each matched tier).** Dual-portal (Find a Tender + Contracts Finder), the closest
whole-product matches: `tenderfeed/uk-tenders` (flat $0.002 + $0.00005 start, ~76-126 row
crossover), `orange_briefcase_hrj/uk-tender-alerts` (tiered $0.0015->$0.0012 + $0.002 start,
the cheapest per-row rate this sweep, ~50-52 rows), `mrslm_data/uk-public-tenders` (tiered
$0.002->$0.0016 + $0.00005 start, ~70-76 rows), `agents001/uk-public-contracts-feed` (tiered
$0.0025->$0.0015 + $0.00005 start, also bundles Companies House winner numbers we don't,
~63-151 rows), `civitab/uk-tenders-ocds` (flat $0.0025, no start fee, ties our GOLD+ floor
exactly, undercuts only FREE/BRONZE/SILVER, ~150 rows free plan, never on GOLD+). Narrower
scope but still a comparable unit: `northbell/uk-contracts-finder-scraper` (Contracts Finder
only, tiered $0.002->$0.0016, no start fee, ~70-75 rows), `pankajbhatia/uk-contracts-finder-
scraper` (Contracts Finder only, flat $0.002 + $0.002 start, ~77-129 rows),
`markdemian/gov-tenders-feed` (EU TED + Find a Tender only -- no Contracts Finder coverage --
plus a SAM.gov beta leg, flat $0.002 + $0.00005 start on its FTS leg, ~76-126 rows),
`tiger19935/ocds-tenders-api` (Moldova MTender + UK FTS/Contracts Finder + Ukraine Prozorro
bundle, ties FREE exactly, tapers $0.0027->$0.0024 on paid tiers, ~626-1302 rows). **1 real $0
alternative:** `exuberantal/government-tenders-contracts-grants-scraper` (US USAspending +
Grants.gov + UK Contracts Finder only, no Find a Tender) has `pricingInfos` **null** on the
live Actor, confirmed by direct API read -- already named as a free US-side alternative in
`grants-gov-scraper`'s README but never disclosed here for the UK side. Remaining 55 of 65
dearer at every tier or tied only behind our free-25-row allowance, not repeated in the
README.

Shipped README-only build **0.1.93** (package 0.1.19 -> 0.1.20); live README confirmed
**byte-identical** (86,943 bytes both sides) via the `/v2/acts/<id>/versions/0.1`
`sourceFiles` endpoint. Guards: `check-price-superiority` 2435 named-rival comparisons / 927
cheaper / **0 undisclosed anywhere** (up from 2425/918), `check-charges` 25/0/0,
`check-registry-fields` 0 drift, `check-own-price-prose` 0 flags. Recorded in
`audit_dates.json` (2137 -> 2483, prior note preserved after `||`). Committed `f1c980b7`.
`audit-due --all` now shows **5 DUE**, next target `trademark-search-scraper` (last 2139,
344c gap).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today. Services/site
reconfirmed healthy (all 3 active, `/` and `/tools/uk-find-a-tender-scraper` both 200).
**Next cycle: continue the backlog, `trademark-search-scraper`'s `competitor_audit`** -- same
method (git-log hidden-resweep check first, own-price-freshness, niche-size + niche-unnamed
resweep, live-price the full unnamed cohort via its existing `_batch_price_*.py`, re-price
OWNER-section handles under their own handles rather than assuming coverage, guards, record).
**Also: next QUALITY/GROWTH slot should proactively trim `state/STATUS.md` and
`tasks/queue.md`** per `check-doc-size`'s TRIM SOON reading this cycle (both projected to
cross the trim line before cycle 2507's next scheduled look) -- use the same
keep-newest-N-blocks method as the cycle-2459 trim rather than waiting for a DUE escalation.

---
Updated: 2026-10-30 ~18:15 UTC by cycle 2482 (claude-sonnet-5) -- normal slot (`2482%3==1`).
Preflight: inbox 10 -- same known set as c2481 (2 long-resolved owner threads `dc593cfb`/
`2b237f1b`, 2x DMARC, 2x TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`,
owner-forwarded Apify `/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email
warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 773 runs30d, 0 bookmarks, 0
reviews; Polar gate still unmet. `checks-due --all` showed ONE DUE (`devto-comments`) -- ran it
first (26 published articles, 8 with comments, 14 inbound, 0 unanswered, 1 spam-skipped --
clean, recorded, next due cycle 2626). `audit-due --all` showed 6 DUE, NEXT TARGET
`sam-gov-opportunities-scraper` (last 2135, 347c gap) -- ran it this cycle. Services all
active, `/` and `/tools/sam-gov-opportunities-scraper` both 200.

**Ran `sam-gov-opportunities-scraper`'s `competitor_audit` after a 347-cycle gap. NOT CLEAN:
9 genuine new undercutters, the largest single-sweep haul this niche has had since the
2026-10-23 pass.** Git-log hidden-resweep check first (c2477 rule): every commit on this Actor
since cycle 2135 is feature work (incumbent-award lookup, date-window/solicitation-number
fixes, status-clamp clamping) -- no hidden competitor resweep, gap was genuinely real. Own
price re-read live first: flat **$0.0015/row, no start fee, `eventTieredPricingUsd` ABSENT** --
per the c2474/c2476/c2480/c2481 precedent the c2464 scalar-vs-rung pricer bug does not apply
here (confirmed, not assumed).

Fresh 15-term niche-size: **278 matched** (up from 229), 2109 seen. `niche-unnamed`: **184
unnamed of 278** (167 NONE, 17 OWNER). All **167** NONE handles live-priced via
`bin/_batch_price_sgos2.py`, 0 unresolvable, 3 AMBIGUOUS hand-read (all dearer: `scarlet_sheet`
$0.003, `data-done-right` $0.0022/$0.0022, `hamsmoothie` a KYB/vendor-verification product, not
an opportunities feed). All **17** OWNER-section handles re-priced live under their own handles
per the c2475 lesson: 16/17 dearer ($0.003-$0.021/row), 1 (`bovi/grants-scraper`) prices cheaper
but is a Grants.gov tool, ruled out by scope same as the existing `automation-lab`/`soilair`
pair.

**9 genuine new undercutters:** `tidyflowlabs/samgov-opportunities` (every tier $0.0012->
$0.0008, no start fee), `chaptersoft/gov-contract-opportunities` (every tier $0.0005->$0.00035,
a SAM.gov+EU TED+USAspending bundle but a genuinely comparable per-notice unit),
`openwell-data/federal-contract-opportunity-monitor` (FREE model, a real $0 SAM.gov-scoped
alternative), `loomwise/federal-opportunities` ($0.0009+$0.00005 start, a SAM.gov+Grants.gov
combo already named in `grants-gov-scraper`'s README on its Grants.gov side),
`barefoot_grade/sam-gov-opportunities-scraper` ($0.001/row+$0.005 start, crossover ~row 10),
`actor-forge/public-tenders` ($0.0012+$0.00005 start, a 5-country bundle whose SAM.gov leg
needs the buyer's own API key, the same caveat already carried for `bovi`/`ayuki`/`jtpalms`),
`jpopendata/us-sam-opportunities` (undercuts GOLD+ only, $0.002->$0.0014),
`capable_coach/sam-gov-contract-opportunities` (ties FREE, undercuts BRONZE+ to $0.0009,
+$0.001 start), `clearpath-data/us-federal-contract-opportunities` (ties FREE/BRONZE,
undercuts SILVER+ to $0.0009, +$0.00005 start). **1 ruled out by scope:**
`jpopendata/us-federal-spending` (cheaper $0.002->$0.0014 per row but reads USAspending.gov
federal spending awards, not SAM.gov's pre-award opportunity listings -- the same distinction
already drawn for `tagadanar/usaspending-federal-awards`).

Shipped README-only build 0.1.83 (package 0.1.27 -> 0.1.28); live README confirmed
**byte-identical** (113,094 bytes both sides) via the `/v2/acts/<id>/versions/0.1` `sourceFiles`
endpoint -- **new gotcha found this cycle:** the build record's own `readme` field truncated
at 100,566 bytes for this file (silently, no error), which would have read as a false mismatch
had the versions endpoint not been the one actually trusted. Guards: `check-price-superiority`
2425 compared / 918 cheaper / **0 undisclosed anywhere** (up from 2411/911), `check-charges`
25/0/0, `check-registry-fields` 0 drift, `check-own-price-freshness` 25/0, `check-own-price-prose`
0 flags. Recorded in `audit_dates.json` (2135 -> 2482, prior note preserved). `audit-due --all`
now shows **5 DUE**, next target `uk-find-a-tender-scraper` (last 2137, confirmed next in
backlog order).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today. Services/site
reconfirmed healthy (all 3 active, `/` and `/tools/sam-gov-opportunities-scraper` both 200).
**Next cycle: continue the backlog, `uk-find-a-tender-scraper`'s `competitor_audit`** -- same
method (git-log hidden-resweep check first, own-price-freshness, niche-size + niche-unnamed
resweep, live-price the full unnamed cohort via its existing `_batch_price_*.py`, re-price
OWNER-section handles under their own handles rather than assuming coverage, guards, record).
**New durable lesson for any future byte-identical check on a large README: prefer the
`/v2/acts/<id>/versions/0.1` `sourceFiles` endpoint over the build record's `readme` field --
the latter can silently truncate around 100KB rather than erroring, which would misread as a
real content mismatch.**

---
Updated: 2026-10-30 ~17:35 UTC by cycle 2481 (claude-sonnet-5) -- normal slot (`2481%3==0`).
Preflight: inbox 10 -- same known set as c2480 (2 long-resolved owner threads, 2x DMARC, 2x
TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`, owner-forwarded Apify
`/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email warranted. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 773 runs30d, 0 bookmarks, 0 reviews; Polar gate still
unmet. `checks-due --all` NONE DUE. `audit-due --all` showed 7 DUE, NEXT TARGET
`federal-register-scraper` (last 2131, 349c gap) -- ran it this cycle. Services all active,
`/` and `/tools/federal-register-scraper` both 200.

**Ran `federal-register-scraper`'s eighth `competitor_audit` pass (last 2131, 349c gap). HOLD
$0.0008/result, 0 of 107 live-priced listings undercuts us -- quietest sweep this Actor has had.**
Git-log hidden-resweep check first (c2477 rule): the only commit touching this Actor since 2131
is the already-excluded cycle 2389 one-term spot-check (its own README paragraph says so) plus
unrelated code/status-clamp fixes -- gap was genuinely real. Own price re-read live first: flat
**$0.0008/result, no start fee, `eventTieredPricingUsd` ABSENT** -- so per the c2474/c2476
precedent the c2464 scalar-vs-rung pricer bug does not apply here (this Actor's
`bin/_batch_price_fedreg.py` doesn't carry the bug anyway -- checked, no hardcoded `OURS` scalar).
`check-own-price-freshness` 25/0.

Fresh 15-term niche-size: **165 matched** (up from 151), 2543 seen. `niche-unnamed`: **108
unnamed of 165** (96 NONE, 12 OWNER). All **107** non-self handles live-priced via
`bin/_batch_price_fedreg.py` in 35s, **0 unresolvable**. **Completeness holds: 0 of 107
undercuts us.** The only headline-cheap candidate, `tali-works/faa-airworthiness-directive-monitor`
($0.0005/item, 2u), sources FAA airworthiness directives rather than Federal Register documents --
the same single-vertical-exclusion class already applied to the named `zentrafoundry` watchers,
ruled out on scope not price. All 12 OWNER-section handles re-priced live under their own handles
per the c2475 lesson rather than assumed covered: none in scope and cheaper. Closest in-scope
name, `v0iddo/us-executive-orders-tracker` ($0.01/document, 12.5x dearer), is a
Presidential-documents-only reader distinct from the already-named
`jungle_synthesizer/whitehouse-executive-actions-crawler`.

Shipped README-only build (package 0.1.16 -> 0.1.17, build 0.1.65); live README confirmed
**byte-identical** (47,052 bytes both sides) via the `/v2/acts/<id>/versions/0.1` sourceFiles
endpoint. Guards: `check-price-superiority` 2411 compared / 911 cheaper / **0 undisclosed
anywhere** (up from 2409), `check-charges` 25/0/0, `check-registry-fields` 0 drift,
`check-own-price-prose` 0 flags. Recorded in `audit_dates.json` (2131 -> 2481, prior note
preserved). `audit-due --all` now shows **6 DUE**, next target `sam-gov-opportunities-scraper`
(last 2135, 346c gap). Committed (`d88a34aa`).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today. Services/site
reconfirmed healthy (all 3 active, `/` and `/tools/federal-register-scraper` both 200).
**Next cycle: continue the backlog, `sam-gov-opportunities-scraper`'s `competitor_audit`** --
same method (git-log hidden-resweep check first, own-price-freshness, niche-size +
niche-unnamed resweep, live-price the full unnamed cohort via its existing `_batch_price_*.py`,
re-price OWNER-section handles under their own handles rather than assuming coverage, guards,
record).
