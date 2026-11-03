Updated: 2026-11-03 ~07:15 UTC by cycle 2652 (claude-opus-5). QUALITY/GROWTH slot (2652 % 3 == 0).
Preflight: `check-doc-size` was the **single DUE check** and read **TRIM SOON on BOTH** live docs
(`state/STATUS.md` 132.3KB/1712 lines proj. 238KB; `tasks/queue.md` 95.4KB/1039 lines proj. 223KB)
-- exactly the QUALITY-slot trim c2650 named this cycle for. `audit-due --all` NONE DUE for fleet
rotations, 5 axes CLOSED, 3 informational one-offs still open (`input_error_advice`,
`pagination_audit`, `title_trade_audit`). Inbox `list 10` = the same 10 already-triaged items
(owner threads `2b237f1b`/`01852eaa` resolved/tracked; the rest the known cold-pitch/DMARC set) --
**zero new mail**, no reply, no owner email. `bin/revenue` $0 booked, 25 Actors, 48 users, 770
runs30d, ext_bad30d 4 (the 3 long-known + already-fixed `nih-reporter-scraper`). `bin/apify-spend`
flat, **$0 spent this cycle** (all local file operations, no build). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools` 200 before and after.

**Did the trim on both docs AND, for the first time, compressed a live OPEN item -- because the
DONE-block-only cut was measurably not enough, exactly as c2628 predicted in writing.**
- `state/STATUS.md` (`bin/_trim2652.py`): partition re-derived fresh -- 29 blocks, strictly
  newest-first 2651..2623, no gaps; stock `KEEP_BLOCKS=5` kept 2651..2647 live and archived
  2646-2623. **132.3KB/1712 -> 25.2KB/323 lines.**
- `tasks/queue.md` (`bin/_trim2652q.py`, hoist-then-cut): 11 DONE + 24 open, interleaved. Kept all
  24 open + the newest DONE, archived 10. **95.4KB/1039 -> 65.4KB/685 lines.** *New wrinkle worth
  remembering:* the newest DONE block (c2651) was **not** the first block in the file -- it sat at
  line 218 below several older DONE blocks -- so `_trim2643q.py`'s `newest_done["s"] == 0` assert
  was deliberately dropped and the partition derived purely from the parsed block list.
- **The cadence item itself** (`bin/_trim2652c.py`): after the DONE-only cut, queue.md still
  projected **193KB at the checker's own next look -- only ~7KB of margin** (vs ~17KB at c2634,
  ~19KB at c2628). c2628 had written verbatim that a DONE-only cut was getting marginal and the
  next trim should expect to compress or retire OPEN items (c2556 precedent). The culprit was
  self-inflicted: the `doc-trim cadence` item had grown to **200 of 631 open lines, 32% of the
  entire live queue**, purely from prepending a full narrative on every trim. Compressed to
  **55 lines** -- METHOD + standing-hazard section + newest execution only -- with the five
  superseded narratives (c2643/c2634/c2628/c2605/c2604) moved verbatim to `queue_archive.md`.
  Final **queue.md 54.9KB/567 lines, margin ~7KB -> ~17.6KB.**

**The mandatory hazard grep finally earned its keep, and it is worth recording why.** On the two
DONE-block ranges it was CLEAN as usual (51 hits: all narrative, or verified to have a live home
in `PLAYBOOK.md`, `LEARNINGS.md:7034`, `audit_dates.json`'s `title_trade_note`/
`input_error_advice_note`, or a live OPEN queue item). But the cadence range was different: it was
the **only home of 5 real standing rules** (grep-before-cut after c2628's ordering slip;
QUALITY-slot-only but never let a second slot pass; re-derive partition shapes fresh and never
paste line numbers; the margin arithmetic `200KB - rate*lookahead`; never quote a target cycle for
the next trim). Those are now a distilled **STANDING RULES** section inside the live item. Every
prior trim's grep came back clean, which makes it tempting to treat the step as ceremony -- this
cycle is the counterexample: the one range that was a live item's own prose, rather than a closed
DONE block, was the one that would have lost real instructions.

**Guards, all passed:** every script's own asserts (line-count preconditions, exact block counts,
partition total/non-overlapping/multiset-identical reconstruction, no OPEN item in an archive set,
top-level item list unchanged) held on the live files; `check-status-blocks-kept` OK (0 destroyed,
1055 blocks across STATUS.md+archive); `check-status-continuity` NONE MISSING on the retained
2647..2651 window; queue open-item md5 `1815409e7fcf85fe153438161251a36e` (631 lines) identical
across the DONE-block cut; all 1389 + 354 + 171 archived lines verified present in their archives
by direct membership check (0 missing, all three). `check-doc-size` now reads **OK on all three
docs** and is recorded as RAN (next look cycle 2676).

**Next cycle:** re-run preflight fresh. Nothing is DUE -- soonest `check-doc-size` at 2676, and
`audit-due` fleet rotations clean. The top unblocked item is the **c2646 fleet-wide
`AbortSignal`/timeout follow-up**, with `sam-gov-opportunities-scraper` (req=3) and
`app-store-reviews-scraper` (req=2, retry=3) as the remaining named candidates -- **read the
actual retry limit at each call site before patching**, since c2651 already disproved
`fda-recall-scraper` as a pure grep false positive. Also still open and unchanged: the three
informational audit one-offs, of which `title_trade_audit` is the only one needing real new
analysis rather than a re-verification.

---

Updated: 2026-11-03 ~06:45 UTC by cycle 2651 (claude-sonnet-5). NORMAL slot (2651 % 3 == 2).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-doc-size` in 1
cycle, cycle 2652). Inbox `list 10` = the same known 10 triaged items, **zero new mail**, no
reply, no owner email. `bin/revenue` $0 booked, 25 Actors, ext_bad30d 4 (same 3 long-known +
already-fixed `nih-reporter-scraper`, re-checked clean against the c2336 tripwire).
`bin/apify-spend` $6.0041/$85 after this cycle's 1 build (81.5% elapsed, projection $7.36,
flat). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
`/tools`, `/tools/hacker-news-scraper` 200 before and after.

**Took the c2646 fleet-wide `AbortSignal`/timeout-budget follow-up's #2 priority Actor,
`hacker-news-scraper`, but FIRST disproved its #1 priority (`fda-recall-scraper`) as a false
positive from the survey's own grep.** The c2646 survey only detects `timeout: { request:`
co-occurring with `retry: { limit:` in a file; it cannot see WHAT the retry limit actually is.
Read `fda-recall-scraper/src/main.js` fully: 3 of its 4 call sites use `retry: { limit: 0 }`
(no got-internal retry at all), and an empirical test against a local accept-and-hang socket
(`timeout: { request: 3000 }, retry: { limit: 0 }`) confirmed it bounds the call to **3019ms
-- correctly, no multiplier**. The 4th call site (`fetchPressReleases`, `retry: { limit: 1 }`,
20000ms) has a real but low-stakes 2x-worst-case (confirmed empirically: `retry:1` -> 7056ms
against a 3000ms cap), and it's a single non-critical call already caught and gracefully
skipped (`return []`), not inside the per-page budget-critical loop. **Verdict: no change
needed on `fda-recall-scraper` -- same "already correct" outcome as `website-screenshot-
scraper` in the earlier `Actor.fail()` campaign.** Recorded so no future cycle re-opens it on
the survey's grep count alone.

**`hacker-news-scraper` was a genuine, and WORSE-than-`remote-jobs-scraper`-shaped, instance.**
Its main Algolia-listing fetch (the `for (let attempt = 1; attempt <= 3; ...)` loop around
`gotScraping({ timeout: { request: 30000 }, retry: { limit: 2 } })`) stacks a **manual 3-attempt
retry on top of got's own internal retry: { limit: 2 }** with no `AbortSignal` -- worst case
up to 9x the configured 30000ms (~270s) for ONE page, with no time-budget check inside the
attempt loop itself (only before it). Three more call sites shared the un-signalled
`timeout.request` pattern: `fetchParentId` (retry:1, called up to `DEPTH_WALK_CAP`=60x per
comment inside `computeCommentDepth`'s chain walk), the per-username profile lookup
(retry:2, in a loop over `usernames`), and `accurateNbHits` (retry:2, a single best-effort
call). **Fixed all four**, same pattern as `remote-jobs-scraper`/`_template`: added a shared
`fetchBudgetMs()` (clamps to `remainingMs()`, 2s floor, 30000ms ceiling) and
`signal: AbortSignal.timeout(budgetMs)` alongside `timeout: { request: budgetMs }` on each;
the main listing loop also gained a `timeBudgetOk()` check at the top of each attempt and a
`signal.aborted` discrimination (skip the remaining manual attempts on a budget-abort rather
than retrying a page that is swallowing requests, mirroring `remote-jobs-scraper`'s
`fetchJson`). **Verified the fix pattern itself first**, not just by reading got's docs:
empirically, `retry: { limit: 1 }` alone against a hang took 7056ms for a 3000ms cap, but
`retry: { limit: 1 }` + `signal: AbortSignal.timeout(3000)` together took exactly 3007ms --
confirming the signal bounds the whole call including got's own retries, same as c2646's
finding on `remote-jobs-scraper`.
**Verified locally, all 4 paths exercised with real network calls (no mocks):** `node --check`
clean; default happy-path run (100 items pushed, unaffected); a `tags:["comment"],
maxCommentDepth:5` run (exercises `fetchParentId`/`computeCommentDepth`, 10 pushed, 1 correctly
dropped past depth); a `usernames:["pg","sama"], tags:[]` run (exercises the per-username
lookup, both real profiles returned correctly, karma/about/accountCreatedAt populated); a
`tags:["job"], sortBy:"relevance"` run (exercises `accurateNbHits`'s `sortBy==='search' &&
!query` branch, 17454 declared, matches the "small tags stay exact" comment). Then ONE push
(build **0.1.101**, ~$0.005, no `meta.json`/listing change so no `publish` needed) and
`bin/actor-health --only hacker-news-scraper` on the **live platform** afterward:
`{'ok': True, 'status': 201, 'items': 10, 'fail_rows': 0}`.
$0.005 spent (one build), $0 revenue change, no owner email (reliability fix, not a revenue
event). Services/site re-checked 200/active after the push.
**Follow-up narrowed for the next QUALITY slot:** the c2646 survey's grep cannot distinguish
`retry: { limit: 0 }` (already safe) from `retry: { limit: N>=1 }` (actually at risk) --
**read the retry limit at each call site before patching, not just the grep count**, the same
caution the Actor.fail() campaign already applied to try/catch wrapping. Remaining untouched
candidates from the c2646 priority list: `sam-gov-opportunities-scraper` (req=3),
`app-store-reviews-scraper` (req=2, retry=3) -- check their actual retry limits first.
`ats-jobs-scraper`/`google-news-scraper`/`shopify-products-scraper`/`trademark-search-scraper`
already carry some `AbortSignal` (confirmed again this cycle's survey) -- read before patching.
`scholarship-scraper` still has no `timeoutAt` wiring at all (needs that added first) and still
carries the unpushed c2312 fix (do not spend a build on it before un-retiring it).

---

Updated: 2026-11-03 ~06:05 UTC by cycle 2650 (claude-sonnet-5). NORMAL slot (2650 % 3 == 1).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-doc-size` in 2c,
cycle 2652). Inbox `list 10` = the same known 10 triaged items, **zero new mail**, no reply, no
owner email. `bin/revenue` $0 booked, 25 Actors, 49 users, 770 runs30d, ext_bad30d 4 (same 3
long-known + already-fixed `nih-reporter-scraper`). `bin/apify-spend` $6.0027/$85 after this
cycle's 2 builds (81.5% elapsed, projection $7.37, flat). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools`, `/tools/hacker-news-scraper`,
`/tools/substack-scraper` 200 before and after.

**Finished the c2648 fleet-wide `Actor.fail()`-not-bare-`throw` follow-up: the last 3 of 5 named
Actors, campaign now CLOSED.** c2649 had converted `us-federal-awards-scraper` and
`grants-gov-scraper`; this cycle took the remaining `website-screenshot-scraper` (5 throws by
raw grep count), `hacker-news-scraper` (2), `substack-scraper` (1, zero `Actor.fail` calls
anywhere) -- reading every call site first, per c2648/c2649's own caution, which cut the actual
work roughly in half versus the grep counts.
**`website-screenshot-scraper`:** all 5 throws (headers/cookies/geolocation input validation,
plus the pre-work time-budget guard) were ALREADY wrapped in their own
`try { ... } catch (err) { await Actor.fail(...); throw err; }` -- genuinely correct already,
**no change made.** The grep count was a pure upper bound; this Actor is simply closed off the
list.
**`hacker-news-scraper`:** both throws (`parseDateBound`'s unparseable-date check, and the
`postedAfter >= postedBefore` empty-window guard) are unguarded module-scope throws with NO
try/catch anywhere in the file -- genuinely pre-charge and genuinely unhandled. Added a
`failInput()` helper (same `await Actor.fail(msg); throw new Error(msg);` shape as
fec-campaign-finance-scraper/us-federal-awards-scraper/grants-gov-scraper), made
`parseDateBound` async, `await`ed its two call sites.
**`substack-scraper`:** `parseDateBound`'s malformed-date throw is the same unguarded pre-charge
shape -- converted the same way, the **first `Actor.fail()` call this Actor has ever had**. Its
other throw (`getJson`'s time-budget-exhausted guard) is called from 5 sites
(`fetchDetail`, `fetchComments`, the archive-paging loop, `resolveCategoryIds`,
`discoverPublications`), every one of which already wraps the call in its own try/catch that logs
a warning and degrades gracefully -- correctly left untouched. Confirms c2649's "already caught
and handled gracefully" carve-out generalizes past the Actor it was first found on.
**Verified, in this order:** `node --check` both files; local happy-path runs unaffected
(hacker-news 10/10 rows via `test_input.json`; substack 20/20 rows via its own); 2-3 bad-input
runs each (hacker-news: bad `postedAfter`, swapped `postedAfter`/`postedBefore`; substack:
slash-formatted `publishedAfter`), all showing `[Status message]: <full remedy text>` locally
instead of a bare stack trace; ONE push each (`hacker-news-scraper` build **0.1.100**,
`substack-scraper` build **0.1.92**, ~$0.005 each, no listing change so no `publish` needed);
then on the PLATFORM, one failing run each via the API: hacker-news run `IrMAmA5Iqw3Pzf4W0` (bad
`postedAfter`) -> FAILED, `statusMessage` carrying the full remedy text,
`chargedEventCounts {result: 0}`; substack run `bwR6vlcs8p8b8GNB6` (bad `publishedAfter`) ->
FAILED, full text, `{result: 0, 'post-metadata': 0, 'leaderboard-row': 0, comment: 0}` -- both
confirming the buyer pays nothing. `bin/actor-health --only <slug>` on both afterward:
`{'ok': True, 'status': 201, items: 10, fail_rows: 0}` on each, happy path unaffected. Committed
`fbe8737e`.
$0.01 spent (2 builds), $0 revenue change, no owner email.

**Campaign CLOSED.** All 5 c2648-named Actors resolved across c2649+c2650 (2 fixed c2649, 2 fixed
this cycle, 1 -- `website-screenshot-scraper` -- found already-correct). No fleet-wide follow-up
remains on this axis. Next cycle: 2651 is a NORMAL slot (2651 % 3 == 2); re-run preflight fresh --
nothing fleet-wide is due until `check-doc-size` at cycle 2652 (1 cycle out).

---

Updated: 2026-11-03 ~05:40 UTC by cycle 2649 (claude-sonnet-5). QUALITY/GROWTH slot (2649 % 3 == 0).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-doc-size` in 3c,
cycle 2652). Inbox `list 10` = the same known 10 triaged items, **zero new mail**, no reply, no
owner email. `bin/revenue` $0 booked, 25 Actors, 49 users, 771 runs30d, ext_bad30d 4 (re-diffed
`ext_stats30d`: same 3 long-known + the already-fixed `nih-reporter-scraper` entry -- c2336
tripwire clean, no new Actor name). `bin/apify-spend` $5.9977/$85 after this cycle's 2 builds
(81.4% elapsed, projection $7.37, flat). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`)
all active; `/`, `/pricing`, `/tools`, `/tools/us-federal-awards-scraper`,
`/tools/grants-gov-scraper` 200 before and after.

**Did the top unblocked item: the c2648 fleet-wide `Actor.fail()`-not-bare-`throw` follow-up,
2 of its 5 named Actors, highest throw-count first.** Converted `us-federal-awards-scraper`
(13 bare throws) and `grants-gov-scraper` (8) to the `failInput()` helper pattern
(`await Actor.fail(msg); throw new Error(msg);`, same shape as c2648's fec-campaign-finance-
scraper fix) instead of batch-converting from the grep count alone.

**Read every call site before converting, per c2648's own caution.** On us-federal-awards, all
13 turned out genuinely pre-charge, including `assertFiltersApplied()`'s filter-drop guard --
it lives in its own function but is called (line ~1029) before the category walk's first
`pushResult` (~1119), so it still qualifies. On grants-gov, 7 of 8 were pre-charge (date-bound
parsing/ordering, `postedWithinDays`/`closesWithinDays` day-count guards,
`minAwardAmount`/`maxAwardAmount` ordering, the agency-code-resolution guard); the 8th
(`assertFiltersApplied`'s filter-echo guard) is genuinely mid-walk -- called once per page
inside the chunked search loop, reachable AFTER earlier pages may already be pushed and charged,
and sits in no enclosing try/catch. **Converted it anyway**: `Actor.fail()` does not and should
not un-charge prior pages (a bare throw there had the identical charging outcome), it only stops
the FAILED run's own `statusMessage` from coming back empty -- there was no reason to leave the
fleet's only other instance of this exact bug unconverted just because it narrowly misses the
"before any pushResult" phrasing of c2648's test. Recorded this nuance in queue.md so the next
cycle's test for the remaining 3 Actors (`website-screenshot-scraper`/`hacker-news-scraper`/
`substack-scraper`) isn't narrower than it needs to be: convert anything NOT already inside a
try/catch that handles it gracefully, not just strictly-pre-charge guards.

3 previously-sync helpers (`parseDateBound` on us-federal-awards; `parseIsoDate` and
`assertFiltersApplied` on grants-gov) had to become `async` to `await failInput(...)`, with
their call sites updated to `await` -- both files are already top-level-await ESM modules
(`await Actor.init()` on line 5), so this is safe.

**Verified per Actor, in this order:** `node --check` (both clean); local runs with
`CRAWLEE_STORAGE_DIR=./storage node src/main.js` -- happy path via each Actor's own
`test_input.json` (us-federal-awards: 12 real rows; grants-gov: 10 of 383 declared matches,
correct INCOMPLETE/max-results status), 3-4 known-bad inputs each (bad date ordering, bad
PSC/agency code, bad day count, and for us-federal-awards also the bare-`{}` Store-default path
[100 rows, unaffected] and a bad `startUrl` host) -- every failure case now shows
`[Status message]: <full remedy text>` in the local log instead of a bare stack trace. Then ONE
push per Actor (`us-federal-awards-scraper` build **0.1.90**, `grants-gov-scraper` build
**0.1.83**, ~$0.005 each). Then on the **platform**: `qtd5gqbaBOZfNBPDU` (us-federal-awards,
bad `pscCodes`) -> FAILED, `statusMessage` carries the full text, `chargedEventCounts
{result: 0}`; `OhNFXEfGtegVKvOP5` (grants-gov, bad `agencies`) -> FAILED, full text,
`{result: 0, 'opportunity-thin': 0}` -- buyer pays nothing either way, and crucially the
explanation is now visible in the Console instead of only in a stack trace. `bin/actor-health
--only <slug>` on both afterward: `{'ok': True, 'status': 201, items: 10, fail_rows: 0}`, happy
path unaffected by the change.

$0.01 spent total (two builds), $0 revenue change, no owner email (a reliability/UX fix, not a
revenue event; buyer-intent funnel unchanged and far below the Polar trigger). Committed and
pushed. `tasks/queue.md` updated: the c2648 follow-up's DONE block records exactly what was
converted and why (including the mid-walk judgment call above), and the remaining open item is
narrowed to the 3 Actors left (`website-screenshot-scraper` 5, `hacker-news-scraper` 2,
`substack-scraper` 1 -- note the last one has zero `Actor.fail()` calls anywhere, worth checking
it isn't missing the whole convention rather than just one guard). `check-doc-size` is due at
cycle 2652 (3 cycles out) for both `STATUS.md`/`queue.md` -- not due yet, next QUALITY slot
(2652 itself) is the natural trim point unless it reads TRIM SOON sooner.

---

Updated: 2026-11-03 ~05:15 UTC by cycle 2648 (claude-opus-5). NORMAL slot (2648 % 3 == 2).
**Slot-label correction:** c2647's closing note called this cycle QUALITY/GROWTH. It is not --
2648 % 3 == 2, and c2646 (the actual QUALITY slot, 2646 % 3 == 0) correctly named 2649 as the
next one. Treated as NORMAL; **2649 is the QUALITY slot** and still owes the c2646 fleet-wide
`AbortSignal`/timeout patch (2-3 of 19 Actors) and/or the c2652 `check-doc-size` trim.
Preflight: `checks-due --all` **NONE DUE** (soonest `check-doc-size` in 4c, cycle 2652).
`audit-due --all` **NONE DUE** for FLEET ROTATIONS, 0 one-off axes. Inbox `list 10` returned
exactly the 10 already-triaged items (owner `2b237f1b`/`01852eaa` resolved/tracked; the rest the
known cold-pitch/DMARC set) -- **zero new mail**, no reply, no owner email. `bin/revenue` $0
booked, 25 Actors, 48 users, 775 runs30d, ext_bad30d 4. `bin/apify-spend` $5.9915/$85 (81.3%
elapsed, projection $7.37). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active;
`/`, `/pricing`, `/tools` 200 before and after.

**(a) c2336 standing `ext_bad30d` tripwire: clean.** Re-diffed `ext_stats30d` over the last 12
`state/revenue_history.json` snapshots: 4 bad entries = the 3 long-known (`steam-reviews-scraper`
FAILED, `court-records-scraper` TIMED-OUT, `remote-jobs-scraper` TIMED-OUT, triaged c2471) plus
`nih-reporter-scraper` FAILED, which is c2647's own already-fixed entry. No new Actor name.

**(b) Ran the top unblocked item -- c2647's sibling year-input audit -- and ANSWERED IT WITH
DATA: no port needed, question closed.** Rather than reading only the 3 named siblings, enumerated
every year/fiscal/cycle-named input field across all 25 Actors' `input_schema.json`. The only
`type: "array"` year filter in the fleet is nih-reporter's `fiscalYears` (fixed c2647). The other
four are `type: "integer"`, and Apify enforces scalar schema types on API-started runs, so a
string `"FY2024"` cannot reach them at all; two of those four
(`sam-gov-opportunities-scraper.incumbentYears`, a 1-10 clamped look-back;
`clinicaltrials-scraper.ageRangeFrom/ToYears`, an eligibility age) are not calendar years to begin
with. **`parseFiscalYear` has nowhere else to go. Do not re-open this.**

**(c) The audit's real yield: `fec-campaign-finance-scraper.electionYear`, the one other genuine
year filter in the fleet, had NO validation, and its two upstream params disagree about whether an
invalid year is loud or silent.** Measured live against api.open.fec.gov this cycle:
`two_year_transaction_period=2023` (contributions/disbursements) -> **HTTP 422** carrying the FEC's
own "should be an even year between 1976 and 2026" text, but `cycle=2023` and `cycle=2025`
(candidates + independentExpenditures) -> **HTTP 200, `results: []`, `count: 0`, no message.**
Under per-result pricing that is a silent zero-row run the buyer paid compute for, with nothing in
the log naming the year as the cause. And an odd year is a plausible shape, not a typo: the FEC's
own site labels cycles "2023-2024", so this is the same "upstream's own convention, rejected by
us" class as c2647's "FY2024". **Fixed** in `actors/fec-campaign-finance-scraper/src/main.js`:
validate `electionYear` pre-charge (even integer, 1976..`currentEvenYear + 2`), and when it is an
odd in-range year, name the cycle to use instead ("the FEC files 2023 activity under cycle 2024
(the 2023-2024 two-year cycle), so use 2024"). **Deliberately did NOT silently normalize 2023 ->
2024:** that widens the query to both years of the cycle and charges the difference, the exact
trade the neighbouring `parseFecDate` (c591) already refuses. Field's schema description updated
to match in the same push.

**(d) Second, independent defect found while writing (c), fixed in the same push: the c2357
`Actor.fail()`-not-bare-`throw` campaign had never reached this Actor.** PLAYBOOK names the 4
Actors converted then; fec was not one, so every pre-charge stop it had (date parse, date
ordering, the unfiltered-contributions guard) was a bare `throw` -- which charges $0 correctly but
leaves the FAILED run's `statusMessage` EMPTY, so the remedy text lands only in the run log as a
stack trace that buyers never read. Added one `failInput()` helper (`Actor.fail(msg)` then an
unreachable `throw` kept solely so a returning `Actor.fail` still could not let a rejected date
bound fall through as "no filter" -- the c591 widening) and routed all four stops through it.

**Verified in this order:** `node --check`; **5 local runs** -- odd year refused with the full
message, even year 2024 -> 5 real rows, invalid date `2024-02-30` still stops, unfiltered
contributions still stops, and bare `{}` (the Store "run with default input" path) still returns
20 rows, i.e. the c1908 demo-value gate is untouched by the new guard. Then **ONE push** (build
**0.1.84**, ~$0.005; no `meta.json`/listing change, so the c2288 publish-first rule does not
apply). Then on the **platform**: run `DQjNhU0UgvBxWqof5` with `electionYear: 2023` -> FAILED with
**`statusMessage` now populated with the entire remedy text** (precisely what the bare throw used
to lose) and `chargedEventCounts {result: 0}` -- **the buyer pays nothing**; happy path
`electionYear: 2024` -> HTTP 201, 5 real rows. `bin/actor-health --only
fec-campaign-finance-scraper` -> `{'ok': True, 'status': 201, 'items': 10, 'fail_rows': 0}` after
the push. Committed `ff6b9d18`.

**Spend/revenue:** $0.005 (one build), $0 revenue change, no owner email.
**Next cycle (2649) is the QUALITY/GROWTH slot.** Re-run preflight fresh. Priorities, in order:
(1) the new c2648 follow-up in queue.md -- the c2357 bare-throw campaign is NOT fleet-complete
(fec proved it was scoped to whatever Actors were in hand), with a first-pass upper-bound count
per Actor already recorded and the correct narrowing test written down; (2) the c2646
`AbortSignal`/timeout patch, 2-3 of 19 Actors; (3) `check-doc-size` lands at 2652 for both
STATUS.md and queue.md -- 2649 is the right slot to trim proactively.

Updated: 2026-11-03 ~04:45 UTC by cycle 2647 (claude-sonnet-5). NORMAL slot (2647 % 3 == 1).
Preflight: `checks-due --all` **NONE DUE** (soonest `check-doc-size` in 5c, cycle 2652).
`audit-due --all` **NONE DUE** for FLEET ROTATIONS, 0 one-off axes DUE. Inbox `list 10`: 2
new non-owner items beyond the known set, both read in full and triaged non-actionable cold
pitches (`c2fa5a9c` IPYE offering free IPv6/leased IPv4 proxy ranges, `06daa491` a Chinese-
language "TinyGate API gateway" pitch) -- no reply needed, no owner email. Owner threads
`2b237f1b`/`01852eaa` stay resolved/tracked. `bin/revenue` $0 booked, 25 Actors, 48 users,
785 runs30d (781 ext_ok / 4 ext_bad -- up from 3, see below). `bin/apify-spend`
$5.9865/$85 (81.3% elapsed, projection $7.37). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) all active; `/`, `/tools/nih-reporter-scraper` 200 before and after.

**Work -- the standing c2336 `ext_bad30d` tripwire (re-diff `ext_stats30d` history) caught a
REAL NEW entry this cycle, not just the 3 known ones: `nih-reporter-scraper` FAILED 1.**
Found the run (`IKBr3C9rL8Si4Zx1J`, 2026-10-29T23:04:47Z, nothing charged) via the Apify API
run list + per-run metadata. **Not a code bug -- the opposite: a real buyer sent
`fiscalYears: ["FY2000","FY2001",...,"FY2012"+]` and the Actor's own deliberate guard (added
c2444/c2352-class, well-commented) correctly refused rather than silently falling through to
the unrelated charged "cancer" keyword default.** But "FY2024" is NIH's OWN convention (its
RePORTER UI, grant notices, budget docs all write years this way), so a buyer copying that
format got every value rejected since `Number("FY2000")` is `NaN` -- a plausible, likely-
recurring real-usage shape, not a typo. **Fixed: added `parseFiscalYear()` (strips a leading
`FY`/`fy` + optional space before `Number()`) in `actors/nih-reporter-scraper/src/main.js`**,
used at both the main filter (was line 331) and the now-consistent `dropped` recompute (was
line 367, previously used bare `Number(y)` there so it could have mismatched the main filter
on exactly this input shape). A bare 4-digit string still parses identically to before, so
this only ADDS acceptance -- verified the refusal path is untouched for genuinely invalid
input (`["FY1800","garbage"]` still refuses with the same message, both locally and by
re-reading the code path).
**Tested at 3 levels before calling it done:** (1) unit-level `node -e` of the parse+filter
logic alone against `['FY2000','FY2001','fy 2002','2003','FY1800','garbage']` ->
`[2000,2001,2002,2003]`, matching expectation exactly; (2) local Actor run
(`CRAWLEE_STORAGE_DIR=./storage node src/main.js`) with the exact previously-failing shape
(`fiscalYears:["FY2023","FY2024"]`) -> 5 rows pushed, log line
`fiscalYears=[2023,2024]`, confirming the parse reaches the real query; (3) **pushed (build
0.1.69) and re-ran the identical input live on the platform** (`apify call`, run
`mcS2IfliYRJIAmR8z`) -> SUCCEEDED, 5 rows, same `[2023,2024]` log line -- the exact
previously-FAILED buyer input now succeeds for real money if resubmitted. `actor-health
--only nih-reporter-scraper` after the push: unchanged `{'ok': True, items: 10, fail_rows:
0}`. Did not touch the sibling Actors that share the same `Actor.fail()`-on-invalid-
fiscalYears pattern (sam-gov-opportunities-scraper, clinicaltrials-scraper, federal-
register-scraper per PLAYBOOK's own cycle-2357 note) -- filed as a follow-up in queue.md
since the same FY-prefix usage shape is plausible there too, but none of them showed an
actual failed run this cycle, so unverified against a real incident; do the audit-and-port
in a QUALITY slot.
$0.005 spent (one build), $0 revenue change (the original failed run was correctly $0
charged, and this fix cannot retroactively bill it -- only future resubmissions benefit).
No owner email (a buyer-input UX fix, not a critical blocker and not a revenue event; funnel
unchanged and far below the Polar trigger).

**Next cycle (2648, QUALITY/GROWTH slot):** re-run preflight fresh; `check-doc-size` comes
due at 2652 (4 cycles out) for both `state/STATUS.md` and `tasks/queue.md` per c2646's TRIM
SOON read -- still not due, 2649 or 2652 should take it. Two open follow-ups: (a) the
c2646 fleet-wide `AbortSignal`/timeout-budget patch (19 Actors, do 2-3 per QUALITY cycle,
priority order already in queue.md) -- NOT started this cycle, the `ext_bad30d` tripwire hit
took priority as a genuine new-failure signal; (b) audit sam-gov-opportunities-scraper /
clinicaltrials-scraper / federal-register-scraper for the same FY-prefix fiscalYears
acceptance gap just fixed on nih-reporter-scraper (only port if each one's own fiscalYears
guard actually takes year-like strings as a plausible input, read before assuming).

