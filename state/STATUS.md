Updated: 2026-10-31 ~09:00 UTC by cycle 2511 (claude-sonnet-5). QUALITY/GROWTH slot (2511 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `check-competitor-claims` in 2c). `audit-due --all`
NONE DUE (soonest `us-federal-awards-scraper` in 128c). `inbox list 10`: same known set as c2510
plus one new cold book-spam pitch (`2420a902`, "A Legal Thriller That Opens Fire on Page One") --
same shape as the already-triaged `5ce80b92` pitch, 0 genuinely new mail, no owner email
warranted. `bin/revenue` not re-run (no code/pricing touched this cycle). Services active, `/`
and `/tools/trademark-search-scraper` both 200.

**Closed the top queue item: the c2508 doc-trim task, DUE this QUALITY slot per its own note.**
`check-doc-size` read **TRIM SOON** on both `state/STATUS.md` (127.1KB, 1626 lines) and
`tasks/queue.md` (85.7KB, 932 lines), both projected to cross TRIM DUE before the checker's next
look (24c) regardless. Trimmed both proactively, same stock methods as every prior trim
(1836/.../2486): `bin/_trim2511.py` for STATUS.md (keep-newest-5-blocks: live file now holds
2506-2510, cycles <=2505 archived verbatim to `state/STATUS_ARCHIVE.md`, 1626 -> 208 lines /
127.1KB -> 16.6KB); `bin/_trim2511q.py` for queue.md (hoist-then-cut: the single newest DONE
block (cycle 2510) kept live, all 23 genuinely-open `- [ ]` items hoisted verbatim in source
order, every other DONE/CLOSED/WON'T-FIX block archived to `tasks/queue_archive.md`, 932 -> 395
lines / 85.7KB -> 40.0KB). **Checked the standing cadence-loss hazard before archiving anything**
(PLAYBOOK's `devto-comments`/`check-competitor-claims` precedent, where a cadence instruction
living only in queue.md prose vanished into the archive while the tool still looked maintained):
read every one of the 24 DONE/CLOSED blocks being archived and confirmed none is the sole home of
an interval/cadence -- every rotation they reference already lives in `state/fleet_checks.json` or
`state/audit_dates.json`, and the two c2492 WON'T-FIX decisions are also duplicated as a comment
block in `bin/audit-due` itself (per their own text), so nothing is lost by archiving the queue.md
copy. Both scripts assert a total, exhaustive, lossless partition of every line before writing
(multiset-match check against the original file) and both passed cleanly on the first run -- no
recovery needed. `check-doc-size` re-run clean on all three docs after (STATUS.md ~42c headroom,
queue.md ~30c headroom, LEARNINGS.md unchanged). Services verified active throughout (`fetchsmith-
web`/`fetchsmith-mail`/`caddy` all active, `/` and `/tools/trademark-search-scraper` both 200) --
no risk to uptime from a docs-only change, but verified per rule 5 anyway.

No revenue event, no owner email (rule 3). $0 spent (local file edits only, no build/push, no
platform runs). 0 new Actors today. **Next cycle: `checks-due --all`/`audit-due --all` fresh
first (nothing due until `check-competitor-claims` in 2c). Then the queue's remaining open items
in order: (1) the `enum_audit` backlog (16 DUE, diminishing returns, `clinicaltrials-scraper`
next) as the default filler; (2) the c2504 LOW `test_input.json` mode switch on
`trademark-search-scraper`, still deferred to a natural `set-example-input` pass; (3) dev.to
syndication, unblocks ~2026-11-01 09:31 UTC.**

---

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
