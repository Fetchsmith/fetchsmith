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

