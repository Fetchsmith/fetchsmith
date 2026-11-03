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

Updated: 2026-11-03 ~16:05 UTC by cycle 2670 (claude-sonnet-5). QUALITY/GROWTH slot (2670 % 3 ==
0, 2670 = 3x890 exactly). Preflight clean and independently re-run: `checks-due --all` NONE DUE
(soonest `check-row-floor` in 6c, cycle 2676); `audit-due --all` showed exactly 1 real backlog
item, `varied_test` DUE on `grants-gov-scraper`; `inbox list 10` the same known 8 triaged items,
zero new mail, zero replies owed; `bin/revenue` $0 booked, 25 Actors, 48 users, 778 runs30d,
`ext_bad30d` same 4 known events; `bin/apify-spend` $6.1485/$85 (82.8% elapsed, projection
$7.43); `bin/actor-health` (full fleet) 24/24 public Actors green, `scholarship-scraper` still
PAUSED/429 as expected; services active and `/`, `/pricing`, `/tools`, `/tools/grants-gov-scraper`
all 200.

**Closed the one real backlog item: `grants-gov-scraper`'s fleet-oldest `varied_test` (2334 ->
2670, 336c gap).** Targeted the two documented date-filter precedence rules that had never been
exercised TOGETHER: `postedWithinDays` is dropped when `postedFrom`/`postedTo` is set
(`main.js:196-198`), and `closesWithinDays` is dropped when `closeDateFrom`/`closeDateTo` is set
(`main.js:231-234`) -- both existed in code/prose and each had been *read*, but no prior
`varied_test` entry (1041/1292/1628/1833/2185/2213/2334) had ever set a relative AND an absolute
filter from the same family at once. Predicted free first via a direct
`api.grants.gov/v1/api/search2` call (caught my own probe bug: `oppStatuses` must be the
pipe-joined string `"forecasted|posted"`, not an array -- an array-shaped probe silently returned
`hitCount:0` until re-read against `main.js:502`): `keyword:"wildfire"` -> 25 hits; hand-filtered
all 25 by `openDate`/`closeDate` to the intended windows -> exactly 9 matches, sized so a wrongly
-honored relative filter would collapse the count sharply rather than shift it by one row (the
earliest close in the matched set is 11/14, well outside a wrongly-applied `closesWithinDays:7`
window). Ran the real Actor **locally for $0** (`CRAWLEE_STORAGE_DIR=./storage node src/main.js`
under `ACTOR_TEST_PAY_PER_EVENT=true`) rather than a platform run, since both rules are pure
client-side branching and local still exercises the real `apiPost()` call against the real
grants.gov API plus the real `Actor.charge()`/`ignoredInputs` logic -- no platform charge needed
to validate pure branching logic. **Result: CLEAN, exact match.** Both precedence warnings fired
by name, `RUN_SUMMARY.ignoredInputs` listed both fields, the status message named both, and the
c2334 forecasted+closeDate interaction warning also correctly fired (oppStatuses included
`forecasted`). Pushed exactly 9 rows, and the opportunity numbers were byte-identical to the free
hand-filtered prediction (not just the count) -- proving both absolute windows were genuinely
applied, not silently intersected with the relative ones. Charged 0 enriched / 9
`opportunity-thin`, matching `enrich:false`. No defect, no code change. Recorded in
`state/audit_dates.json` (`varied_test: 2670`); `audit-due --all` now reads **FLEET ROTATIONS:
NONE DUE** across the whole fleet again. Local test storage cleaned up after.

$0 spent (local run only, no Apify platform call), $0 revenue change, no owner email (a clean
verification is neither a revenue event nor owner-fixable). **Next cycle:** nothing fleet-wide due
until `check-row-floor`/`check-upstream-warnings` at ~cycle 2676, and no `audit-due` backlog
remains anywhere. The standing `eu-ted-tenders-scraper` runs30d-is-not-demand watch (queue.md) is
still open but not urgent. Recompute `cycle % 3` fresh rather than trusting this header.

---

Updated: 2026-11-03 ~15:40 UTC by cycle 2669 (claude-sonnet-5). NORMAL slot (2669 % 3 == 2,
recomputed fresh off 2667=3x889). Preflight clean and independently re-run: `checks-due --all`
NONE DUE (soonest `check-row-floor` in 7c, cycle 2676); `audit-due --all` FLEET ROTATIONS NONE
DUE, every type CLOSED or not due; `inbox list 10` the same known 10 triaged items (owner threads
`2b237f1b`/`01852eaa` stay resolved/tracked, `01852eaa`'s 2026-11-15 `/v2/store` deadline still
12 days out and already hardened per c2478/c2496), zero new mail, zero replies owed; `bin/revenue`
$0 booked, 25 Actors, 48 users, 778 runs30d, `ext_bad30d` same 4 known events; `bin/apify-spend`
$6.1293/$85 (82.7% elapsed, projection $7.41); services active and `/`, `/pricing`, `/tools`,
`/tools/ats-jobs-scraper` all 200.

**One live signal surfaced and resolved within the cycle, nothing else was due.**
`bin/actor-health` (full fleet) returned FAILED on `trademark-search-scraper` (run
`OBZEMyP5RTKYclFo9`, exit 1, `statusMessage`: "Could not reach TMview (tmdn.org) through any
network path this run: 3 Apify Proxy session(s) and a direct connection all failed transport-level
— last error: The operation was aborted due to timeout. TMview itself is frequently reachable when
this happens, so it is usually a flaky exit node rather than an outage — re-run in a few minutes.")
— this is the Actor's own self-diagnosed transient-network message, not a new code path. Confirmed
transient rather than assumed: immediately re-ran `bin/actor-health --only trademark-search-scraper`
and it came back clean (201, 10 items, 0 fail_rows). This run was our own health probe, not an
external user's, so it does not touch `ext_bad30d` (that counter is external-run-only); no fleet
regression, no code change. Also ran `bin/check-charges` as a different verification angle than
recent clean cycles (per c2663's "vary the check mix" note) — 25/25 priced Actors, 0 missing
`Actor.charge()`, 0 event-name drift.

**Per the standing c2524 rule, no code change was manufactured to fill the slot** — nothing
fleet-wide was due and the one anomaly resolved itself as transient on re-check. Best-queued real
work for the next NORMAL/QUALITY slot that finds something due: the c2464 `_batch_price_*.py`
rung-for-rung port (gated to the next `competitor_audit` due) and the c2646 `AbortSignal`/
timeout-budget patch (19 Actors, 2-3 per QUALITY cycle). $0 spent this cycle, $0 revenue change,
no owner email (transient network blip on our own probe, not a revenue event or owner-fixable).
**Next cycle:** nothing fleet-wide due until `check-row-floor`/`check-upstream-warnings` at
~cycle 2676; recompute `cycle % 3` fresh rather than continuing this header's sequence.

---

Updated: 2026-11-03 ~15:20 UTC by cycle 2668 (claude-opus-5). QUALITY/GROWTH slot by compensation:
2668 % 3 == 1 is arithmetically NORMAL, but c2667's header mis-stated `2667 % 3 == 1` (2667 = 3x889,
so == 0) and spent the real QUALITY slot on a NORMAL audit, so the fleet-hygiene slot was overdue
and this cycle took it. Preflight clean and independently re-run: `checks-due --all` NONE DUE
(soonest `check-row-floor` in 8c, cycle 2676); `audit-due --all` FLEET ROTATIONS NONE DUE, every
type CLOSED or not due (c2667's varied_test backlog really is gone); `inbox list 10` the same known
triaged items, zero new mail, zero replies owed; `bin/revenue` $0 booked, 25 Actors, 48 users, 778
runs30d, `ext_bad30d` the same 4 known events; `bin/apify-spend` $6.1267/$85 (82.7% elapsed,
projection $7.41); services active and `/`, `/pricing`, `/tools`, `/tools/app-store-reviews-scraper`
all 200 before and after.

**Nothing was due, so the cycle closed the one real queued backlog item: c2666's fleet-wide sweep
for the "fixed order decides between POPULATED candidates" bug class. It found exactly one more
instance and it was a billed wrong answer.** The keyword grep that looked like the whole job
(`auto.?detect|fetchAuto|firstNonEmpty` across all 25 `src/main.js`) hits ONLY `ats-jobs-scraper`
and would have closed the item as "nothing found"; the class is structural, so the sweep actually
performed was "wherever several populated candidates are reduced to one by `.find()`/`break`/`[0]`,
ask what decides the winner". Fleet verdict: `google-play-reviews-scraper:539` SAFE (picks by Google
Play's own relevance order -- order *within* one ranked upstream is signal, not noise);
`sam-gov-opportunities-scraper:1504-1509` and `sec-insider-trades-scraper:356` SAFE and are the
pattern to copy (both refuse to guess on ambiguity); all other hits are transient retry or enum
normalisation. **BROKEN: `app-store-reviews-scraper.resolveAppName`**, which built
`[...iosHits, ...macHits]` and then took `find(exactTitle) || find(anyTokenSubstringAnywhere)`.
Two wrong answers proved live with free `itunes.apple.com/search` probes: `"sketch app"` with
`includeMacApps:true` resolved to the iOS **"Sketchbook"** (substring hit, concatenated first)
instead of the real Mac **"Sketch"**; and `"affinity photo"` resolved **silently** to **"Canva AI
Photo & Video Editor"** on the generic token `photo` alone -- the caller then paid for Canva's
reviews, while the function's own warning string had promised for years that "an unrelated top hit
is treated as no match rather than guessed".

**Fixed and shipped as build 0.1.121** (~$0.005): scored scan (5 exact title / 4 all query tokens as
whole words in title / 3 all tokens anywhere in title+bundleId+artistName / 2 partial-but-whole-word
/ 1 partial substring), best tier wins and **list order survives only as the tie-break WITHIN a
tier**; plus a coverage gate (multi-token query, candidate matching < half the query's token chars
-> no match) and a warning that names what actually matched. Verified the way a selection change
should be -- OLD vs NEW on the same live payloads, by slicing the edited block straight out of
`src/main.js` into a throwaway harness (17 app names x {iOS-only, +Mac} = 34 outcomes): **2 fixed,
31 byte-identical, 1 incidental wash** (`"sketch app"` iOS-only, where no correct answer exists;
logged as a LOW no-action queue note so it is not re-discovered as a bug). Then live on platform
(`bin/run-charged`, run `GvHuRPNAEZH9N0Qa9`): `"sketch app"` -> `Sketch (id 1667260533) in the Mac
App Store`, `"affinity photo"` -> the new honest NO-match warning. 5 rows pushed with
`chargedEventCounts {result:0}` -- **correct, not a leak**: `FREE_REVIEWS_PER_RUN = 10`
(`src/main.js:387`) makes every run's first 10 reviews free. Post-push `check-charges` 25/25 clean,
`actor-health --only app-store-reviews-scraper` ok (201, 10 items, 0 fail_rows); no output-field
change (so `check-registry-fields`/`check-meta-fields` untriggered) and `test_input.json` untouched
(so `exampleRunInput` cannot have drifted).

~$0.005 spent (one build; the verification run was free under the Actor's own free tier, and all
name-resolution probing was free direct `itunes.apple.com` calls), $0 revenue change, no owner email
(a reliability fix is not a revenue event and nothing here is owner-fixable). Durable writeup in
`notes/LEARNINGS.md` (cycle 2668) with the three generalisable rules: fixed order is safe only as a
tie-break among candidates of EQUAL MEASURED QUALITY; substring containment is not match quality
(`includes()` makes "sketch" match "sketchbook" and "cut" match "capcut"); and on a PPE Actor a
silent wrong resolution is a BILLED wrong answer, so a single shared generic token must not count as
a match. **Next cycle:** nothing fleet-wide due until `check-row-floor`/`check-upstream-warnings` at
~cycle 2676; `audit-due` has no backlog anywhere; the c2464 `_batch_price_*.py` port remains the
best-queued real work but stays gated to the next `competitor_audit` due. Recompute `cycle % 3`
fresh -- and note c2667's header got it wrong, so check the arithmetic rather than continuing the
previous header's sequence.

---

Updated: 2026-11-03 ~14:41 UTC by cycle 2667 (claude-sonnet-5). NORMAL slot (2667 % 3 == 1,
recomputed fresh). Preflight clean: `checks-due --all` NONE DUE (soonest `check-row-floor` in 9c,
cycle 2676); `audit-due --all` showed exactly 1 real backlog item, `varied_test` DUE on
`google-news-scraper` (the item c2666 left OPEN after `ats-jobs-scraper` ate that cycle); `inbox
list 10` same known 8 triaged items, zero new mail; `bin/revenue` $0 booked, 25 Actors, 48 users,
778 runs30d, `ext_bad30d` same 4 known events; `bin/apify-spend` $6.0968/$85 (82.6% elapsed,
projection $7.38); services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active, `/`, `/pricing`,
`/tools`, `/tools/google-news-scraper` all 200 before and after.

**Finished the one real backlog item: `google-news-scraper`'s `varied_test`.** Of the two
candidates c2666 named (`topics`/`topicsHashed`, never varied_test'd; or the documented
`publishedAfter`+`publishedBefore`+`excludeSites` Google leak-protection path, c788 bug class),
picked the leak-protection path because, on inspection, it had only ever been verified by direct
`curl` against Google (c788, c933) — never driven through the real Actor with charge verification,
despite naming a real historical bug. Ran live via `bin/run-charged`:
`{queries:["artificial intelligence"], publishedAfter:"2026-09-01", publishedBefore:"2026-09-10",
excludeSites:["pinterest.com"], maxItemsPerQuery:50, maxResults:50}` (run `W3jSYB5d7MsWvJ1WK`).
**Result: still correct.** 46 rows pushed, every `publishedAt` within 2026-09-01..09-10 (inside the
documented ±1-day timezone tolerance); statusMessage read "Pushed 46 items. Dropped 4 article(s)
that Google returned well outside your publishedAfter/publishedBefore window ... you were not
charged for them."; `chargedEventCounts` settled `{result:46}` — exactly the pushed count, proving
the 4 leaked-but-dropped rows were genuinely excluded from billing (no under- or over-charge).
Post-run `check-charges` 25/25 clean, `actor-health --only google-news-scraper` ok (201, 8 items,
0 fail_rows on the default test input). Recorded `varied_test: 2667` in `state/audit_dates.json`
with the full method/result in the note. **`audit-due --type varied_test --all` now reads 0 DUE
across all 25 Actors** — the backlog c2666 found is fully closed. The other named candidate
(`topics`/`topicsHashed`) stays available for whenever this Actor's `varied_test` next comes due
(~336c out); not re-queued separately since either candidate remains valid then. Durable lesson
in `notes/LEARNINGS.md` (cycle 2667 entry): a `varied_test` candidate that cites a historical bug
number is not automatically "already covered" — check whether that bug's fix was verified through
the Actor's real run path (charged, dataset, statusMessage), not just a free external probe.

~$0.083 spent (one Actor run, 46 charged rows at $0.0018 BRONZE), $0 revenue change, no owner
email (a clean re-verification is neither a revenue event nor owner-fixable). **Next cycle:**
nothing fleet-wide due until `check-row-floor`/`check-upstream-warnings` at ~cycle 2676, and no
`audit-due` backlog remains anywhere (varied_test now fully clean fleet-wide). The standing
`eu-ted-tenders-scraper` runs30d-is-not-demand watch (queue.md) and the LOW fleet-wide grep for
other "first non-empty wins" collision bugs (c2666) are still open but not urgent. Recompute
`cycle % 3` fresh.

---

Updated: 2026-11-03 ~14:10 UTC by cycle 2666 (claude-sonnet-5). NORMAL slot (2666 % 3 == 2,
recomputed fresh -- c2665 guessed forward that 2666 would be QUALITY, which was arithmetically
wrong). Preflight clean: `checks-due --all` NONE DUE (soonest `check-row-floor` in 10c, cycle
2676); `audit-due --all` showed the one real backlog, `varied_test` DUE on `ats-jobs-scraper` and
`google-news-scraper`; `inbox list 10` same known 10 triaged items, zero new mail; `bin/revenue`
$0 booked, 25 Actors, 48 users, 778 runs30d, `ext_bad30d` same 4 known events; `bin/apify-spend`
$6.084/$85 (82.5% elapsed, projection $7.37); services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) active, `/`, `/pricing`, `/tools`, `/tools/ats-jobs-scraper` all 200 before and after.

**Ran `varied_test` on `ats-jobs-scraper` (the first of 2 DUE Actors) and it surfaced a real,
previously-unknown auto-detect bug instead of a clean no-op -- fixed and shipped.** Edge case:
`{"ats":"auto","slug":"ramp"}` (the Actor's own `input_schema.json` default example, documented
there as the canonical Ashby case) -- auto-detect resolved to **Greenhouse** instead, a 1-posting
junk/test board ("Copy of Chief Legal Officer"), silently returning the wrong company instead of
the real Ramp (fintech) Ashby board, both confirmed live with free direct calls to
`boards-api.greenhouse.io` and `api.ashbyhq.com`. Root cause: `fetchAuto()` in `main.js` picked
the first non-empty board in a fixed platform priority order rather than the largest non-empty
one, so a small decoy beats a large real match when the decoy sits earlier in the list. **Fixed**
(priority-order `.find()` -> `boardSize()`-max `reduce`, fixed order kept only as the all-empty
tie-break), pushed build **0.1.117** (~$0.005), re-verified live: `auto:ramp` now returns real
Ashby rows (`atsSource:ashby`). Paired edge case same cycle: `employmentTypeKeyword:"contract"` on
`auto:airbnb`+`workday:okgov` -- SUCCEEDED, `chargedEventCounts {job:0}` correctly uncharged,
per-board WARN logs named the exact reason on each platform, status message's "373 open
posting(s)" matched the two boards' real counts exactly. Post-push `check-charges` 0 drift,
`actor-health` 10/10 clean. Full writeup in `notes/LEARNINGS.md` (cycle 2666) including the
generalizable lesson (fixed priority order is only safe as a tie-break among EMPTY candidates,
never populated ones) and a new LOW queue item to grep the fleet for the same pattern elsewhere.

**`google-news-scraper`'s varied_test stayed DUE** -- the ats-jobs-scraper investigation/fix/push/
re-verify filled the cycle's time budget. `tasks/queue.md` names 2 specific untested-edge-case
candidates for next cycle (topics/topicsHashed, or the publishedAfter+publishedBefore+excludeSites
Google-leak protection path) so it doesn't need to re-derive them.

~$0.005 spent (one build), $0 revenue change, no owner email (a reliability fix is not a revenue
event, nothing here is owner-fixable). **Next cycle:** finish `google-news-scraper`'s varied_test
first (still DUE). Nothing fleet-wide due until ~cycle 2676. Recompute `cycle % 3` fresh.

---

Updated: 2026-11-03 ~13:33 UTC by cycle 2665 (claude-sonnet-5). NORMAL slot (2665 % 3 == 1).
Preflight fully clean, all independently re-run (not trusted from c2664's prose): `checks-due
--all` showed exactly 1 DUE -- **`check-status-continuity`, ran it: retained block window
2647..2664, 17 successfully-completed cycles in that window per `worker.log`, NONE MISSING** --
recorded via `checks-due --ran` (next due cycle 2713). `audit-due --all` FLEET ROTATIONS NONE DUE.
`inbox list 10` the same 10 known triaged items (owner threads `2b237f1b`/`01852eaa` stay
resolved/tracked; rest is the known cold-pitch/DMARC/spam set) -- zero new mail, zero replies
owed. `bin/revenue` $0 booked, 25 Actors, 48 users, 778 runs30d, `ext_bad30d` still the same 4
known events. `bin/apify-spend` $6.0667/$85 (82.5% elapsed, projection $7.36, far under the $25
trip-wire). `bin/actor-health` 24/24 public Actors green, `scholarship-scraper` still PAUSED/429
(cleared=False, c2372 bold.org gate still shut, unpushed c2312 fix stays unpushed). `bin/traffic`
still 0 buyer-intent signal on /pricing or /tools -- Polar trigger not fired, not raised. Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active; `/`, `/pricing`, `/tools` 200 before and
after. `git status`: only the 3 volatile check-cache files touched (`state/health.json`,
`state/revenue.json`, `state/revenue_history.json`) -- no substantive diff from preflight alone.

**Spent the rest of the cycle chasing the one lead that looked promising and closed it cleanly
with no code change.** The full (untruncated) inbox has 22 `dmarc@fetchsmith.com` messages, not
the 2 the STATUS/queue notes have been citing as "DMARC sample" -- worth checking whether 20 were
silently going unparsed. Read each with `dmarc-report`'s own selection logic directly against the
files: **only 2 of the 22 carry an `attachments` array at all** (`af5d9f7d`, `202905fb`, both
after the cycle-1626 receiver.py fix that first made attachment capture possible); the other 20
are older messages with no `attachments` key, `text`, or `html` at all -- the pre-fix "every DMARC
report unreadable" state the `dmarc-report` docstring already documents, and the raw body was
never stored, so there is nothing left to recover. **Confirmed, not new: the DMARC sample really
is 2 reports**, both 1-source/1-message/0-fail (`54.240.11.115`, SPF+DKIM pass), matching
`notes/LEARNINGS.md`'s standing wait-for-more-weekly-drops guidance on `p=reject` exactly. No code
change, no owner email (closing a doubt about existing data is neither a revenue event nor
owner-fixable). Also re-confirmed the Apify `/v2/store` 2026-11-15 item (`queue.md` line ~345) has
no action due today -- its own note already says the next real step is strictly AFTER the
deadline (re-run `store-anon-rank` + the self-test); re-reading it today would just restate c2478.

$0 spent, $0 revenue change. **Next cycle:** nothing fleet-wide due until `check-row-floor`/
`check-upstream-warnings` at ~cycle 2676 (11c out per `checks-due`); 2666 is a true QUALITY/GROWTH
slot (2666 % 3 == 0, recompute fresh). If it also reads clean, the c2464 `_batch_price_*.py`
rung-for-rung port (queue.md, HIGH-for-correctness but explicitly gated to "next `competitor_audit`
due", not standalone) is the best-queued real work once that audit type comes due.

Updated: 2026-11-03 ~13:10 UTC by cycle 2664 (claude-opus-5). QUALITY/GROWTH slot (2664 % 3 == 0,
recomputed fresh from the integer per the c2659 rule). Preflight all clean and all independently
run: `checks-due --all`/`audit-due --all` NONE DUE (soonest `check-status-continuity` in 1c, cycle
2665 -- RUN IT NEXT CYCLE); `inbox list 10` the same 10 known triaged items, zero new mail, zero
replies owed; `bin/revenue` $0 booked, 25 Actors, 48 users, 778 runs30d, `ext_bad30d` the same 4
known events; `bin/apify-spend` $6.0513/$85 at 82.4% elapsed (projection $7.34, well under the $25
trip-wire); `bin/actor-health` 24/24 public Actors green, `scholarship-scraper` still PAUSED/429
(`cleared=False` -- the c2372 bold.org gate has NOT opened, so the committed-but-unpushed c2312 fix
stays unpushed); `bin/traffic` still shows no /pricing or /tools buyer-intent and no purchase mail,
so the Polar-checkout trigger has not fired and was not raised; services active, `/`/`/pricing`/
`/tools` 200 before and after.

**Took c2663's advice to vary the mix, and the varied read found something worth recording.**
`bin/usage-trend` shows exactly one Actor off the ~+1/day platform-example baseline:
**`eu-ted-tenders-scraper`**, +5/24h and +9/48h while 18 of 25 Actors sit flat at +0. Its
per-snapshot series says the deviation is sustained rather than a blip -- it oscillated 26<->27
daily from 10-23 to 10-29 (the documented arrivals-equal-departures steady state), then stepped
27 -> 28 (10-29 15:30Z) -> 33 (10-30 09:00Z) -> 37 (11-02) -> **42 (11-03)**: net +15 over 5 days
against a trailing window that is simultaneously shedding old runs, all 42 SUCCEEDED, 0 failed.
**It is NOT traction, and the field that settles it is in the same API object: `stats.totalUsers7Days`,
`totalUsers30Days` and `totalUsers90Days` are all exactly `1`.** One caller increased its rate; no
new user arrived. Nothing about Store ranking, SEO or discovery is measured by this number, so it
does not license listing-copy edits (the c1468/c2280 trap). Bookmarks 0, reviews 0. New standing
rule in LEARNINGS: read the windowed distinct-user counts in the same `GET /v2/acts/<id>` call
before writing "demand" about any runs30d move -- `bin/usage-trend` does not print them.

**Ran the c2168 demand-burst protocol on it end-to-end anyway (a deviation is the right trigger
even when the cause is mundane); both halves came back healthy.** (a) Charge path **live-re-verified**
via `bin/run-charged` with `{countries:[FRA],publishedWithinDays:14,maxResults:5}`: 5 rows pushed,
`chargedEventCounts` settled `{result: 5}`, verdict clean; `accountedChargedEventCounts {result:0}`
expected on a self-run (c165). The charging shape is the safe one -- `main.js:441-445` charges
BEFORE `Actor.pushData` and returns false when `chargedCount === 0`, so a buyer's charge limit
cannot produce unpaid rows. Recorded as `charge_event_verified: 2664` in `state/audit_dates.json`,
labelled explicitly as a re-verification on current code (c2305 already closed the full
30-charge-event/24-Actor matrix; the build has moved since, hence worth redoing, and
`bin/check-charges` can only prove the call exists statically, never that it is reached).
(b) **Unit economics measured live for the first time on this Actor:** `usageTotalUsd` $0.00025405
for 5 rows = **$0.0000508/row** cost (almost entirely `ACTOR_COMPUTE_UNITS`, zero external data
transfer) against a live-read **$0.0015/result** (`pricingInfos[-1]`, `apifyMarginPercentage 0.2`)
-> **$0.0012/row net to us, ~23.6x net / ~29.5x gross margin**, versus `trademark-search-scraper`'s
~4x at c2168. This Actor's traffic is no cost risk at any plausible scale. (c) Confirmed a
non-finding so it is not chased again: `run-charged`'s `RUN_SUMMARY: none (HTTP 404)` here is
**deliberate** -- the Actor's own header (`main.js:6-8`) documents that it has no
RUN_SUMMARY/incompleteReason framework (20 of 25 Actors have one; this one intentionally does not).

Spend this cycle: one Actor run, ~$0.00025, against the BUDGET.md "Apify platform usage above
included credits" line ($120 allocated, ~$6 used). No owner email (no revenue event, nothing only
the owner can fix). **Next cycle:** `check-status-continuity` is DUE at 2665 -- run it; the
`/v2/store` 2026-11-15 item wants its pre-deadline look within the next ~12 days; DMARC sample
still only 2 reports so `p=reject` stays parked; growing-niches retry and niche-hunting both still
gated (~2026-12-26). The real trigger to watch on eu-ted is the windowed distinct-user count
rising above 1, or a first bookmark/review -- not the run count.

---

Updated: 2026-11-03 ~12:35 UTC by cycle 2663 (claude-sonnet-5). NORMAL slot (2663 % 3 == 2,
recomputed fresh from the integer). Independently re-ran the full preflight battery rather
than trusting c2662's prose: `checks-due --all`/`audit-due --all` both NONE DUE (soonest
`check-status-continuity` in 2c, cycle 2665); `inbox list 15` = same known items, zero new
mail, zero replies owed (`5ce80b92`/`ba1bf931`/`06daa491`/`9d15ac17` all previously-logged
spam); `bin/revenue` $0 booked, 25 Actors, 48 users, 778 runs30d, `ext_bad30d` still the same
4 known events; `bin/apify-spend` $6.0367/$85 flat, $0 spent; `bin/actor-health` 24/24 public
Actors green, `scholarship-scraper` still PAUSED/429 as expected; `bin/traffic` still shows
no /pricing or /tools pageview signal and no buyer mail, so the Polar-checkout trigger has
not fired (owner deferral still holds, did not raise it); services active, `/`/`/pricing`/
`/tools` all 200 before and after; `git status` showed only volatile cache files touched by
these checks -- no substantive diff, no code change manufactured. See `tasks/queue.md`
cycle-2663 DONE block for full detail. **Next cycle:** nothing fleet-wide due until 2665; if
2665 is also clean, vary the verification mix (e.g. `check-source-endpoints` cadence, or a
fresh competitor-feature scan) rather than repeating the identical battery again.

---

Updated: 2026-11-03 ~12:15 UTC by cycle 2662 (claude-sonnet-5). NORMAL slot (2662 % 3 == 1,
recomputed fresh from the integer). Preflight: `checks-due --all`/`audit-due --all` both
NONE DUE (soonest `check-status-continuity` in 3c, cycle 2665). Inbox `list 10` = the same
known 9 triaged items, zero new mail -- confirmed the two owner threads stay resolved
(`2b237f1b` CourtListener token wired c2362, `01852eaa` Apify `/v2/store` change hardened
c2496, remainder deliberately post-deadline). `bin/revenue` $0 booked, 25 Actors, 48 users,
778 runs30d, ext_bad30d 4 (same 3 long-known + already-fixed `nih-reporter-scraper`).
`bin/apify-spend` $6.0363/$85, flat, **$0 spent this cycle** -- no build, no push. Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools` 200
before and after.

**No ready task this cycle -- every live queue item is either already clean/closed or
explicitly gated on a trigger that has not fired, and both standing fallbacks (niche-hunting,
growing-niches re-grep) are also blocked. Ran the cheap verification work instead rather than
manufacture a code change (c2524 rule).**
1. **c2336 `ext_bad30d` tripwire, re-diffed fresh from `state/revenue_history.json`:** 4
   lifetime events, identical to the known baseline -- `court-records-scraper` TIMED-OUT
   (2026-10-08), `steam-reviews-scraper` FAILED (2026-10-26), `remote-jobs-scraper` TIMED-OUT
   (2026-10-29), `nih-reporter-scraper` FAILED (2026-11-03, already diagnosed-and-fixed at
   c2647, re-confirmed clean by c2742/c2787's own notes at STATUS.md lines ~692/762/787/806).
   No NEW entry beyond those four -- nothing to triage.
2. **c2380 growing-niches README-arrow grep re-run fresh:** `grep -rnlE
   "[0-9]+\s*(→|->)\s*[0-9]+" actors/*/README.md` -- same 9 files as c2635/c2654 (8 cycles
   ago), no new file. Per c2654's own guidance ("wait longer than ~19 cycles before the next
   retry"), 8 cycles is too soon -- did not spend the ~15min/Actor six-step pass on an
   unchanged candidate set.
3. **`bin/dmarc-report list`:** still only 2 reports on file (both covering the same
   2026-10-26 range, both 1 source / 0 fails), unchanged since c2372 -- not enough sample to
   revisit the c2371 `p=reject` decision.
4. **Niche-hunting / new-Actor build:** confirmed via `notes/NICHES.md`'s own c2306 closing
   note that every axis (10 keyword-category sweeps, WebSearch-for-sources, EU legal-mandate,
   paid/B2B anti-bot, category-level) is fully exhausted, with the one remaining lever
   (WebSearch-for-new-sources) explicitly gated to no sooner than ~2026-12-26. Did not
   re-attempt a search this cycle.

$0 spent, $0 revenue change, no owner email (a clean verification cycle is neither a revenue
event nor owner-fixable). **Next cycle:** nothing fleet-wide due until `check-status-
continuity` at 2665. If still nothing is due then either, the next calendar date worth
re-checking for real new work is the DMARC sample (whenever 2-3 more weekly reports land) or
2026-12-26 (WebSearch-for-sources lever). Recompute `cycle % 3` fresh rather than trusting
this label forward.

---

Updated: 2026-11-03 ~11:55 UTC by cycle 2661 (claude-sonnet-5). QUALITY/GROWTH slot
(2661 % 3 == 0, recomputed fresh from the integer). Preflight: `checks-due --all`/
`audit-due --all` both NONE DUE (soonest `check-status-continuity` in 4c, cycle 2665).
Inbox `list 10` = the same known 10 triaged items, zero new mail -- confirmed the two owner
threads on the list stay resolved: `2b237f1b` (CourtListener token) was wired at c2362, and
`01852eaa` (Apify `/v2/store` ranking change, deadline 2026-11-15) was already hardened at
c2496 with the remainder deliberately deferred post-deadline, `store-anon-rank` next due
~c2744. No reply needed, no owner email. `bin/revenue` $0 booked, 25 Actors, 48 users,
778 runs30d, ext_bad30d 4 (same 3 long-known + already-fixed `nih-reporter-scraper`).
`bin/apify-spend` $6.0357/$85, flat, **$0 spent this cycle** -- no build, no push. Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools` 200
before and after.

**Ran `check-doc-size` per c2660's flag: `tasks/queue.md` read TRIM SOON (83.7KB/917 lines,
projected 211KB by the checker's next scheduled look, past the 200KB trim line) while
`state/STATUS.md` was still OK (58.2KB). This QUALITY slot is exactly the proactive trim
point c2660 named, so trimmed queue.md only.** Ran the standing-hazard grep first over the
10 archive-bound DONE blocks (cycles 2646, 2651-2659) -- all hits were narrative already
homed elsewhere (closed-campaign details, a naming rule already in LEARNINGS.md, and
cross-references to the doc-trim item's own STANDING RULES section, which is OPEN and
untouched by this cut) or independently reconfirmed closed with no open follow-up (the
c2646 AbortSignal/timeout-budget campaign and the c2357 bare-throw/`Actor.fail()` campaign
both grepped clean fleet-wide -- a stale STATUS.md passage from several cycles back once
named 3 "remaining" Actors for the latter, but the live queue.md carries no such open item
and the archived DONE blocks confirm "all 4 named candidates" and "no fleet-wide follow-up
remains from this axis"). Wrote `bin/_trim2661q.py` following the established
hoist-then-cut method (keep every OPEN block + only the newest DONE block by cycle number,
archive the rest to `tasks/queue_archive.md` under a dated header, with asserts on block
counts/cycle numbers/line-count conservation so a structural surprise aborts instead of
silently corrupting the file). Archived 10 DONE blocks (cycles 2659 down to 2646; c2660
itself, already the first block, stays live for its "next cycle" pointer), 379 lines moved.
**Verified**: `check-doc-size` now reads `OK tasks/queue.md 52.3KB 538 lines ~28 cycles of
headroom` (was TRIM SOON); line-count-conservation and open-items-unchanged asserts inside
the script itself passed (did not just trust the printed counts); `queue_archive.md` grew
by exactly the archived byte count with nothing else touched.

No Actor code touched, nothing buyer-facing -> no build, no push beyond the doc commit, $0
spent, $0 revenue change, no owner email (doc hygiene is neither a revenue event nor
owner-fixable). **Next cycle:** nothing fleet-wide due until `check-status-continuity` at
2665. `state/STATUS.md` itself is still OK (58.2KB, ~32c headroom) -- no need to trim it
this slot; re-run `check-doc-size` fresh next QUALITY cycle rather than assuming today's
headroom holds.

Updated: 2026-11-03 ~11:20 UTC by cycle 2660 (claude-opus-5). NORMAL slot (2660 % 3 == 2,
recomputed fresh from the integer per c2659's process finding, not counted forward from the
previous cycle's printed label). Preflight: `audit-due --all` FLEET ROTATIONS NONE DUE;
`checks-due --all` **3 DUE** (`check-blog-cta`, `check-backlinks`, `check-actor-guides`).
Inbox `list 10` = the same known 10 triaged items, zero new mail, no owner email. `bin/revenue`
$0 booked, 25 Actors, 48 users, 775 runs30d (770 -> 775), ext_bad30d 4 (same 3 long-known +
already-fixed `nih-reporter-scraper`). `bin/apify-spend` $6.0352/$85, flat, **$0 spent this
cycle** -- no build, no push. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all
active; `/`, `/pricing`, `/tools` 200 before and after.

**(a) Ran all 3 due fleet checks; all clean, all recorded.**
- `check-blog-cta`: 88 posts -- 0 missing-CTA, 0 roundup-with-no-one-hop-path, 0 Apify slug
  naming no local Actor dir, 0 dead internal link.
- `check-backlinks`: 131 post(guide)-Actor pairs across those 88 posts -- 0 missing, 0
  unresolved.
- `check-actor-guides`: 24 live Actors -- 0 flagged; every Actor clears the floor with room
  (min `dedicated=2`, min `related=3`; `ats-jobs-scraper` richest at 12/15).
Recorded via `checks-due --ran` with notes: `check-blog-cta` 2324 -> 2660 (next 2996),
`check-backlinks` 1988 -> 2660 (next 3332), `check-actor-guides` 1988 -> 2660 (next 3332).

**(b) Then leaned QUALITY-flavored per c2659's note about the silently-skipped c2658 QUALITY
slot, and ran the two checkers that have NO `checks-due` cadence (PLAYBOOK's "every QUALITY
cycle" instruction): `check-code-fields` and `check-source-bytes`.**
- `check-code-fields`: **0 Actors with code-only field drift** across the fleet. All
  remaining annotations are the known-benign classes (`[soft: not in any literal: ...]`,
  `[non-row literals skipped: ...]`, `[FIELD_SUPPRESS applied: ...]`).
- `check-source-bytes`: `692 files checked, **1 flagged**` -- and the single fleet-wide hit
  was **`notes/LEARNINGS.md:7318` itself**, i.e. the c2655 note that *documents* the
  `gen-output-schema` soft-hyphen fix. **Root cause: that write-up quoted the offending
  artifact (`"U.S.<U+00AD>-based"`) with the raw U+00AD still embedded in the quote.** So
  c2655 fixed the real bug correctly and then reintroduced the exact byte class it had just
  purged, into the record of the fix.

**Why that was worth fixing rather than annotating, and what was done.** Checked the tool
first: `check-source-bytes` is a plain byte scan over `TEXT_SUFFIXES` with **no allowlist and
no suppress mechanism** (grepped for suppress/allowlist/exclude -- only `SKIP_PARTS` for
`node_modules`/`.git`/`storage`), and **no `checks-due` cadence**, so there is literally
nowhere to record "this hit is intentional". Leaving it would mean every future QUALITY cycle
re-investigates the same self-referential flag, while a genuinely new hit would hide inside a
non-zero count that already looks normal. Rewrote the quote as the spelled-out escape
`<U+00AD>` plus a short inline note on why the escape is deliberate -- meaning preserved
exactly (an invisible character inside a quotation communicated nothing to a reader anyway)
and strictly more legible. `check-source-bytes` now reads **0 flagged across 692 files**, so
the next non-zero count is unambiguous signal. No Actor code touched, nothing buyer-facing,
so no build and no push were needed (unlike c2655, which did have to push `sam-gov-
opportunities-scraper` 0.1.86 because that instance was in a live `dataset_schema.json`).

Appended the durable lesson to `notes/LEARNINGS.md` (verified the new note is itself clean --
it names codepoints, never pastes them): **when documenting a byte/codepoint finding anywhere
under `/root/agent`, name the codepoint (`U+00AD`, `U+200B`, `\x00`) -- never paste the
character**; and the general form, **a checker with no suppress list must be kept at a zero
baseline, because its only signal is the count, so any "known-benign" hit left in place
silently spends that signal** (same reasoning as c2478's `RANK UNKNOWN`-vs-`NOT FOUND` work).

**Also confirmed, so it does not get re-opened early:** the c2478 Apify `/v2/store` change
(deadline 2026-11-15, 12 days out) needs **nothing today**. Its code half was finished early
at c2496, and its remaining open half is explicitly post-deadline work; `store-anon-rank` is
next due ~c2744 (~2026-11-05), still pre-change, so the expected reading until the date is
`paging_ok: True` on every row.

$0 spent, $0 revenue change, no owner email (a doc hygiene fix and three clean checks are
neither a revenue event nor owner-fixable).

**Next cycle:** nothing fleet-wide due for 5 cycles (`check-status-continuity` soonest, c2617
+ 48 = ~2665; then `check-row-floor`/`check-doc-size`/`check-readme-live-row`/
`check-upstream-warnings` ~2676). `check-source-bytes` and `check-code-fields` are now both
at a clean zero baseline as of 2660 -- on the next QUALITY slot, **any** non-zero
`check-source-bytes` count is a real new hit, so do not re-derive the LEARNINGS self-flag.
2661 % 3 == 0, so **2661 is a true QUALITY/GROWTH slot** (recompute it yourself anyway).
Worth noting for it: `check-doc-size` is not due until ~2676, but STATUS.md has grown 25.2KB
(post-c2652-trim) -> ~53KB and queue.md 65.4KB -> ~79KB, so the doc-trim cadence may read
TRIM SOON before its checker is scheduled.

---

Updated: 2026-11-03 ~10:50 UTC by cycle 2659 (claude-sonnet-5). NORMAL slot (2659 % 3 == 1).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-blog-cta` in 1
cycle). Inbox `list 10` = the same known 10 triaged items, zero new mail, no owner email.
`bin/revenue` $0 booked, 25 Actors, 48 users, 770 runs30d, ext_bad30d 4 (same 3 long-known +
already-fixed `nih-reporter-scraper`). `bin/apify-spend` $6.0347/$85, flat, **$0 spent this
cycle** -- no build. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`,
`/pricing`, `/tools` 200 before and after.

**Closed the `input_error_advice` audit's remaining open question (named by c2658): are
`nih-reporter-scraper`'s and `grants-gov-scraper`'s own zero-row/error messages actionable,
given their POST/JSON-body shape exempts them from the url-encoding half of the audit?**
Read both Actors' `apiPost`/retry/zero-row code in full. `nih-reporter-scraper`'s retry loop
already distinguishes transient 429/5xx, a known eRA "System Unavailable" outage page, and
generic non-200/malformed bodies, each with its own `lastApiError` message; its zero-row
branch enumerates specific causes (ANDed filters, a bad IC/activity/state code, pre-1985
fiscal years) and special-cases `searchId`/`exclusiveProjectNums`. `grants-gov-scraper`'s
`apiPost` carries a comment (verified live cycle 124/125, re-confirmed in effect now) stating
Grants.gov's API never returns an HTTP error for a bad parameter -- always 200/`hitCount: 0`
-- so there is no 404-vs-retry-exhausted ambiguity to collapse in the first place; its
zero-row branch enumerates 6 specific causes including the `oppStatuses` default and the
`cfda` live-probe. **Verified empirically, not just by reading the code:** ran both Actors
locally with a keyword guaranteed to match nothing
(`zzzqqqnonexistentkeywordxyzabc123`) -- both produced exactly the coded, actionable
`statusMessage` (NIH: "No projects matched (...). NIH RePORTER confirms 0 results for these
filters -- not an error. Drop a filter to broaden the search..."; Grants.gov: "No
opportunities matched (Grants.gov declared 0) -- a complete result, you were charged nothing.
Causes in order: ..."), not a generic or empty one. **Verdict: no defect on either Actor --
same "already correct" shape as `google-news-scraper` (c2658) and the AbortSignal campaign's
`retry:0` false positives.** No code change, no build, no push (nothing to ship). Recorded
in `state/audit_dates.json` (`input_error_advice` = 2659 on both Actors, with the full
reasoning in each note). **This closes the `input_error_advice` audit across all 3 Actors
c2658 named: `sec-insider-trades-scraper` fixed at c2625, `google-news-scraper` closed c2658,
`nih-reporter-scraper`/`grants-gov-scraper` closed here.**

**Second, a small but durable process finding: the last two cycles' self-printed `cycle % 3`
slot labels were arithmetically wrong.** c2657 wrote "QUALITY/GROWTH slot (2657 % 3 == 0)"
and c2658 wrote "NORMAL slot (2658 % 3 == 2)" -- true arithmetic is 2657 mod 3 = 2 (NORMAL)
and 2658 mod 3 = 0 (QUALITY), so a QUALITY slot was silently skipped. Recomputed this cycle's
own label fresh (2659 mod 3 = 1, NORMAL) rather than counting forward from the prior labels.
Noted in `notes/LEARNINGS.md` so the next cycle re-derives `cycle % 3` from the integer
itself rather than trusting the previous cycle's printed slot name. **The next cycle that
owes a QUALITY slot should recompute from its own cycle number**, and may want to treat the
skipped c2658 QUALITY slot as reason to prioritize QUALITY-type work (re-run checkers,
README/competitor work) a bit sooner rather than strictly waiting for the next `%3==0` cycle.

$0 spent, $0 revenue change, no owner email (both findings are verification/process notes,
not revenue events or owner-fixable issues).

**Next cycle:** nothing fleet-wide due until 2660 (`check-blog-cta`/`check-backlinks`/
`check-actor-guides`). The `input_error_advice` audit is now fully closed across its 3 named
Actors -- no open thread remains on this axis. Recompute slot type fresh from `cycle % 3`;
consider leaning QUALITY-flavored given the skipped c2658 slot.

---

Updated: 2026-11-03 ~10:25 UTC by cycle 2658 (claude-sonnet-5). NORMAL slot (2658 % 3 == 2).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-blog-cta` in 2
cycles). Inbox `list 10` = the same known 10 triaged items (owner threads `2b237f1b`/`01852eaa`
long resolved; the rest confirmed-again cold-pitch/DMARC/SEO spam -- `a661a19a`, `5ce80b92`,
`2420a902`, `ba1bf931` individually re-read, all byte-matching prior triage), **zero new mail**,
no owner email. `bin/revenue` $0 booked, 25 Actors, 48 users, 770 runs30d, ext_bad30d 4 (same 3
long-known + already-fixed `nih-reporter-scraper`). `bin/apify-spend` $6.0343/$85, flat, **$0
spent this cycle** -- no build. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all
active; `/`, `/pricing`, `/tools` 200 before and after.

**First, backfilled cycle 2657's record: it did real, fully-committed work but hit the harness
timeout (`rc=124`, `aborted_streaming` after 1699s) before it could write STATUS.md/queue.md.**
Confirmed via `git log`/`git show` that nothing was lost: `9e27b2dc` is a complete, correctly-
committed `check-competitor-claims --fix` run (10 stale user counts fixed across 8 READMEs,
plus a real false claim corrected on `google-play-reviews-scraper` -- see the DONE block below
for the full record), and the harness's own safety-net auto-commit (`51fac52f`) caught only the
2 volatile `state/revenue*.json` snapshots, confirming no in-progress edit was dropped. The only
actual gap was the missing STATUS.md/queue.md narrative, now written retroactively below.

**Second, this cycle's own task: closed the `input_error_advice` audit's open "url-encoding
half of the sweep" question on `google-news-scraper`, its named top candidate.** Read all 3
URL-construction sites in `actors/google-news-scraper/src/main.js`: the search-query template
already `encodeURIComponent`s its value (line 413); the `topics` template interpolates raw but
is pre-filtered through the `VALID_TOPICS` uppercase-allowlist so it can never carry an unsafe
character; `topicsHashed` interpolates a regex-extracted-or-raw string with NO encoding at all.
**Verified empirically, not just by reading the code:** ran the Actor locally with
`topicsHashed:['bad hash&code']` and with embedded `\n`/`\t` control characters -- neither
crashed; WHATWG URL construction auto-percent-encodes the unsafe bytes, the request completes,
Google returns an empty feed, and the Actor's existing per-feed try/catch already produces the
correct, actionable status message ("...Google News returned zero results for: bad hash&code
(try a broader query, different \"country\"/\"language\", or check the RSS URL)"). **Verdict: no
defect, no code change -- same "already correct" shape as the AbortSignal campaign's `retry:0`
false positives.** Recorded in `state/audit_dates.json` (`google-news-scraper.input_error_advice`
= 2658, new field -- this Actor had never carried one). No build, no push (nothing to ship).
$0 spent, $0 revenue change, no owner email (a verification finding, not a revenue event or
anything owner-fixable). **Next cycle:** nothing fleet-wide due until `check-blog-cta`/
`check-backlinks`/`check-actor-guides` at 2660. The `input_error_advice` note's remaining open
half (whether nih-reporter/grants-gov/sec-insider-trades-scraper's own zero-row/error messages
are equally actionable, since their POST/JSON-body shape exempts them from the encoding half) is
still open for a future QUALITY slot with idle time.

---

Updated: 2026-11-03 ~09:57 UTC by cycle 2657 (claude-sonnet-5). QUALITY/GROWTH slot
(2657 % 3 == 0). **Backfilled by cycle 2658 after a harness timeout cut this cycle off before
it could write STATUS.md/queue.md -- see the 2658 block above for how this was confirmed safe.**
Preflight (from the committed work): `check-competitor-claims` was DUE (144c cadence) and was
the cycle's task.

**Ran `check-competitor-claims --fix`: auto-corrected 10 unguarded stale user-count claims
across 8 Actor READMEs** (eu-ted-tenders, google-news, google-play-reviews, hacker-news,
remote-jobs, sec-insider-trades, website-screenshot, apple-podcasts, ats-jobs, substack-scraper
-- 8 Actors, 10 fixes); 125 more stale counts remain but are guarded (superlative/trend/
sub-figure claims that need hand review, not a bare number swap) and were correctly left alone.

**Re-verified the 2 UNDATED paragraphs and found a real false claim.**
`google-play-reviews-scraper`'s `aspectRatings`-uniqueness paragraph (last checked 2026-09-17)
claimed "none of the leading competitors expose this" / "top 3 by users don't include it" --
re-read `thewolves/google-play-reviews-scraper`'s own live `actorDefinition` and README (2253
users, one of the niche's named top-3-by-users rivals) and found it exposes the same underlying
Google Play aspect-rating data under the field name `criterias`. **Both claims were false.**
Reworded the paragraph to name the real exception (thewolves) while noting the other two top-3
rivals (neatrat, curious_coder) still lack the field.

All 11 affected Actors rebuilt and pushed (`apify push --force`) so the live Store listings
carry the corrected numbers and claim; verified `google-play-reviews-scraper`'s live readme
field directly via the Builds API. `state/fleet_checks.json` updated (`check-competitor-claims`
recorded as RAN). ~$0.022 total build spend, $0 revenue change, no owner email (a listing-
accuracy fix, not a revenue event). Committed `9e27b2dc`.

---

Updated: 2026-11-03 ~09:20 UTC by cycle 2656 (claude-opus-5). NORMAL slot (2656 % 3 == 1).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-competitor-claims`
in 1 cycle, 2657; 0 fleet rotations due). Inbox `list 10` = the same known 10 triaged items,
zero new mail, no owner email. `bin/revenue` $0 booked, 25 Actors, 48 users, 770 runs30d,
ext_bad30d 4 (same 3 long-known + already-fixed `nih-reporter-scraper`). `bin/apify-spend`
$6.0095 -> $6.0099/$85 (81.9% elapsed, projection $7.34, flat, **$0 spent this cycle** -- no
build; dev.to publishing is free). Services + `/`, `/pricing`, `/tools` and the syndicated
post's own canonical all 200/active before and after. `check-doc-size` OK on all three live
docs (STATUS 39.2KB, queue 64.4KB, LEARNINGS 7318 lines) -- no trim needed.

**Nothing was due, so spent the slot on the one growth cadence that was: dev.to article #19
published, with every claim in it re-measured live first.** `state/devto_syndicated.json`
showed a dead-regular 2-day syndication beat (2026-10-22/-24/-26/-28/-30/-11-01), so today was
due, and 61 of 88 site posts were unsynced. Picked
`openfda-count-shows-you-the-top-1000-and-never-says-so` (broadest-appeal upstream, one hard
gotcha as the hook). **Re-measured every claim before publishing, because the footer we ship
asserts every number came from a live request made while writing** -- republishing October
figures under a November dateline would have made it false. All structural claims held exactly
(100-bucket default, 1000 ceiling, `400` on `limit=1001` and on `skip`-with-`count`, `500` not
`400` without `.exact` across five field/endpoint combos, no `meta.results` on count responses,
`count=report_date` still ignoring `limit` at 748/748/748); re-ran the full 15-window
year-partition rather than spot-checking it -- union **5,548 distinct firms** vs the 1,000 the
global query returns, buckets summing to **29,586** = today's `meta.results.total` to the row.
Corpus drift since October (29,485->29,586 rows, 5,526->5,548 firms, index `last_updated`
2026-10-07->2026-10-28) is now **stated in the article** rather than silently swapped.
Published via `bin/devto-post` after a dry run: **201, id 4967941**, public page 200, canonical
and both outbound site links verified resolvable first. `state/devto_syndicated.json`
re-derived whole-file (its own documented method) -- **27 -> 28 synced, 60 unsynced, 0
unmatched canonicals, diffed against a backup: 1 slug added, 0 lost.** Verified this cycle's
own output twice: `check-disclosure` 88 site posts + 28 dev.to articles / **0 missing**, and
`devto-comments` 28 articles / 15 inbound / **0 unanswered** (both recorded via `checks-due
--ran`).

**Second, durable finding: the syndication cadence itself had no clock -- registered it.**
`bin/devto-post` was filed in `fleet_checks.json`'s `not_cadence.operational` bucket at c1624,
whose `_why` ("run every cycle by the protocol, by cron, or on a specific event") is true for
its bucket-mates (`inbox`, `revenue`, `actor-health`) but **false for `devto-post`** -- nothing
invokes it every cycle and no event triggers it; the 2-3-day rhythm lived ONLY in one PLAYBOOK
sentence plus implicit timestamps in `devto_syndicated.json`. This cycle only noticed the
syndication was due by hand-reading those timestamps. That is the exact prose-only-cadence rot
this file exists to close, and it has already cost us twice on this same channel
(`devto-comments` 43 cycles unrun, `check-competitor-claims` 121). Moved it into `checks` at
**96c = exactly 2 days** (justified from the measured beat: c2586->c2656 = 70 cycles over ~35h;
96 > the hard 48c "max 1 post/day" cap, and the floor of PLAYBOOK's 2-3-day window), by
surgical JSON edits rather than a `json.dump` round-trip per the standing rule. `checks-due`
now lists `devto-post ... in 96` (next ~cycle 2752, ~2026-11-05). Mirrored into the PLAYBOOK
sentence so prose and registry agree. Two lessons appended to LEARNINGS.md: the
`not_cadence.operational` bucket is the one whose `_why` can be false per-member (it was
assigned by *what kind of tool* something is, not by *whether it has a clock*), and the standing
"re-measure before syndicating; state the drift" rule.

$0 spent, $0 revenue change, no owner email (a published article is not a revenue event and
nothing here is owner-fixable).

---

Updated: 2026-11-03 ~08:35 UTC by cycle 2655 (claude-sonnet-5). QUALITY/GROWTH slot (2655 % 3 == 0).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-competitor-claims`
in 2 cycles, cycle 2657). Inbox `list 10` = the same known 10 triaged items, zero new mail, no
owner email. `bin/revenue` $0 booked, 25 Actors, 48 users, 770 runs30d, ext_bad30d 4 (same 3
long-known + already-fixed `nih-reporter-scraper`). `bin/apify-spend` $6.0078 -> $6.0088/$85
after this cycle's 1 build (81.8% elapsed, projection $7.35, flat). Services + `/`, `/pricing`,
`/tools`, `/tools/sam-gov-opportunities-scraper` all 200 before and after.

**Ran the two QUALITY-cycle checkers with no automatic `checks-due` cadence
(`check-source-bytes`, `check-code-fields`, per PLAYBOOK's "every QUALITY cycle" instruction)
and traced a real fleet-wide generator bug from the one hit.** `check-code-fields`: 0 drift
across all 25 Actors. `check-source-bytes`: 1 file flagged, a U+00AD soft hyphen inside
`sam-gov-opportunities-scraper/.actor/dataset_schema.json`'s `eligibleApplicantsNote.example`
("U.S.­-based") -- a copy-paste artifact from the real SAM.gov text the example was sampled
from. Confirmed NOT the cycle-336 binary-detection bug (valid UTF-8, grep/`file` both see it
fine) -- cosmetic, buyer-visible on the Store API tab only. **Root cause traced to the
generator, not just this one file:** `bin/gen-output-schema` copies `v[:120]` from a real
sample row into `example` with zero sanitization, so any future regeneration on any Actor
could reintroduce the same class of artifact from real-world scraped text. Fixed at the
source (`_clean_example()`, strips the same `{Cc,Cf,Co,Cs}` categories `check-source-bytes`
flags), hand-fixed the one existing instance in the JSON, pushed (`sam-gov-opportunities-
scraper` build **0.1.86**, ~$0.005), verified via the Builds API that the live
`actorDefinition` no longer carries the soft hyphen, and `actor-health --only
sam-gov-opportunities-scraper` still 10/10 clean. Full write-up in `notes/LEARNINGS.md`.
$0.005 spent, $0 revenue change, no owner email. Details and next-cycle pointer in the
queue.md DONE block for this cycle.

---

Updated: 2026-11-03 ~08:05 UTC by cycle 2654 (claude-sonnet-5). NORMAL slot (2654 % 3 == 2).
Preflight: `checks-due --all` had exactly 1 DUE (`check-source-endpoints`) -- ran it: 50 hosts
probed, **0 deviations**, 3 exempt as before, `bold.org` (scholarship-scraper's watch_recovery
host) still `429` (confirmed separately, still blocked, no un-pause/push trigger). `audit-due
--all` NONE DUE (0 fleet rotations due). Inbox `list 10` = the same known 10 triaged items,
**zero new mail**; re-read both owner threads in that list on general principle
(`2b237f1b` CourtListener token, `01852eaa` Apify `/v2/store` ranking-change forward) and
confirmed both are already fully resolved/tracked from prior cycles (token wired since c2362,
re-confirmed c2629; store-change code hardened at c2496, deadline 2026-11-15 tracked in the
open item below) -- no new owner action needed. `bin/revenue` $0 booked, 25 Actors, 48 users,
770 runs30d, ext_bad30d 4 (same 3 long-known + already-fixed `nih-reporter-scraper`).
`bin/apify-spend` $6.0073/$85 (81.7% elapsed, projection $7.35, flat, **$0 spent this cycle** --
no build). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
`/tools`, `/tools/court-records-scraper` 200 before and after.

**Re-tried the c2380/c2583/c2635 "growing niches" one-term-diff follow-up; still 0 new
candidates, file set unchanged.** Fresh fleet-wide `grep -rlE "[0-9]+\s*(→|->)\s*[0-9]+"
actors/*/README.md` returned the identical 9 files c2635 already found (ats-jobs,
federal-register, clinicaltrials, fec-campaign-finance, sam-gov-opportunities,
uk-find-a-tender, remote-jobs, trademark-search, us-federal-awards scrapers) -- no Actor's
README has grown a new N->M arrow near listing/match text since c2635. Since the candidate set
itself hasn't moved in 19 cycles, re-running the full per-Actor six-step pass today would just
re-confirm the same "already resweeped within October/early November" verdicts c2583/c2635
already recorded. **Did not spend a build or a deep pass on this; left the open item as-is.**
Next time this is picked up, re-grep fresh again (per its own standing rule) rather than
trusting this note, and consider waiting a bit longer than 19 cycles before retrying given two
consecutive 0-candidate reads.

No code change, no build, $0 spent, $0 revenue change, no owner email (nothing only the owner
can fix, no revenue event). This cycle was intentionally light: everything due was clean,
nothing new in the inbox, and the one speculative follow-up yielded no actionable work --
recorded that explicitly rather than manufacturing a change to fill the slot.

---

Updated: 2026-11-03 ~07:45 UTC by cycle 2653 (claude-sonnet-5). NORMAL slot (2653 % 3 == 1).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-source-endpoints` in
1 cycle, cycle 2654). Inbox `list 10` = the same known 10 triaged items, **zero new mail**, no
reply, no owner email. `bin/revenue` $0 booked, 25 Actors, 48 users, 770 runs30d, ext_bad30d 4
(same 3 long-known + already-fixed `nih-reporter-scraper`). `bin/apify-spend` $6.0059/$85 after
this cycle's 1 build (81.7% elapsed, projection $7.35, flat). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools`, `/tools/app-store-reviews-
scraper` 200 before and after.

**Took the c2646 fleet-wide `AbortSignal`/timeout-budget follow-up's last 2 named candidates:
disproved `sam-gov-opportunities-scraper`, fixed `app-store-reviews-scraper`.**
`sam-gov-opportunities-scraper`'s 3 call sites (`apiGet`, `usaSpendingTopAwards`, the webhook
POST) ALL use `retry: { limit: 0 }` -- read the full manual-retry loops around each (4 and 3
attempts respectively, both already checking `timeBudgetOk()` per attempt and capping backoff
sleeps to `remainingMs()`) and confirmed `retry:0` means no got-internal multiplier, same
"already correct" verdict as `fda-recall-scraper` (c2651) and `website-screenshot-scraper`
(c2650). **No change made.**
`app-store-reviews-scraper` was a genuine instance, same shape as `hacker-news-scraper`'s
worst call site: its shared `requestWithRetry()` helper stacked a manual 3-attempt outer loop
on top of got's own `retry: { limit: 2 }` with no `AbortSignal` and no time-budget check
inside the loop (the file's `timeBudgetOk()` is only checked between apps/countries/storefront
probes, never inside a single url's retry loop) -- worst case ~9x the configured 30000ms
(~270s) for ONE url, inside a per-app x per-country x per-sort x per-page nested walk. Fixed
with `fetchBudgetMs()` (clamped to `remainingMs()`, 2s floor, 30000ms ceiling) +
`signal: AbortSignal.timeout(budgetMs)` alongside the existing `timeout: { request: budgetMs }`,
a `timeBudgetOk()` check at the top of the attempt loop, and `signal.aborted` discrimination
(no retry of a cap-exhausting abort) -- identical pattern to `hacker-news-scraper`/
`remote-jobs-scraper`. Preserved the existing per-call `opts.retry` override (line 673 passes
`retry: { limit: 1 }` for the app-info HTML fetch) since `...opts` still spreads last.
**Verified the signal/retry interaction itself empirically first, on an accept-and-hang local
socket** (not the blackhole-IP shape, which fails at the TCP-connect stage before got's retry
list ever applies and so proved nothing): no signal, `retry:{limit:2}` took **12101ms** against
a 3000ms cap (~4x, matching c2646's measurement); with `signal: AbortSignal.timeout(3000)`
added, exactly **3006ms** -- confirms the signal bounds the whole call including got's own
retries on this got-scraping version, same result hacker-news-scraper's fix measured. Then a
local happy-path run (`test_input.json`, 10 reviews fetched/pushed, unaffected) and ONE push
(build **0.1.120**, ~$0.005, no listing change so no `publish` needed); `bin/actor-health
--only app-store-reviews-scraper` on the platform afterward: `{'ok': True, 'status': 201,
'items': 10, 'fail_rows': 0}`.
$0.005 spent (one build), $0 revenue change, no owner email (reliability fix, not a revenue
event). Services/site re-checked 200/active after the push.

**c2646 fleet-wide follow-up is now CLOSED.** All 4 named priority candidates resolved:
`fda-recall-scraper` and `sam-gov-opportunities-scraper` already correct (retry:0 sites),
`hacker-news-scraper` (c2651) and `app-store-reviews-scraper` (this cycle) fixed. The broader
~19-Actor survey from c2646 still stands as a LOW-priority latent list (most already carry some
`AbortSignal` per re-confirmed greps) -- no immediate action, re-survey only if a future cycle
has idle QUALITY-slot time and nothing else queued.

**Next cycle:** re-run preflight fresh. Nothing is DUE -- soonest `check-source-endpoints` at
2654. No fleet-wide follow-up remains from the c2646 campaign. Top unblocked items are the
remaining LOW-priority tripwires/one-offs in queue.md (`title_trade_audit` needs real new
analysis; the others are re-verification only).

---

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

