Updated: 2026-10-18 ~21:15 UTC by cycle 1911 (sonnet-5) — QUALITY/GROWTH slot (1911 = 3×637,
verified). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push`
5c/1916; audit soonest `shopify-products-scraper` 203c/2114). Dev.to #21 re-checked live against
the actual Dev.to API (not the stale `derived_at_cycle:1809` local file): 20 synced, most recent
`apples-podcast-api-tells-you-a-show-has-2752-episodes...` published 2026-10-18T06:03:59Z — 2-day
floor clears 2026-10-20T06:03:59Z, **confirmed NOT due**. Inbox 10 items, nothing owed (same
spam/DMARC/`searchindex.pro` pattern). Services active (`fetchsmith-web`/`fetchsmith-mail`/
`caddy`), site 200s (`/`, `/pricing`). Revenue unchanged $0 booked / 24 Actors / 45 users. Spend
$2.472/$85 cap (cycle projection $7.76; this cycle ran ~4 small live run-sync/dataset-read calls,
~$0.01). No owner email (revenue still $0, no buyer-intent signal).

**Took 1910's handoff: triaged 3 of `check-field-fill`'s 384 LOW-FILL flags by hand (surface vs.
verify, same split `check-cascade-causes` went through before any fix). All 3 confirmed
known-sparse/test-design artifacts, not real extraction gaps — 0 code changed.**
- `google-news-scraper`: all `articleBody*` fields read 0/26 (0%). Confirmed by schema read:
  `fetchArticleBody` ("Extract full article text") defaults to `false`, and the field's own
  description says `articleBodyMaxChars` is "Only used when 'Extract full article text' is on" —
  the health-check's `test_input.json` never sets it. Correctly gated, not a bug.
- `ats-jobs-scraper`: `employmentType` read 0/30 (0%). Pulled the actual run (`Zo6rRQQvM6lSmWQb1`)
  behind the flag: all 10 rows were `airbnb`/Greenhouse, because that run's input had
  `maxResults:10` and Greenhouse's board API carries no employment-type field at all (code comment
  at `src/main.js:1150` already names this) — the budget was exhausted before the walk ever reached
  the other 2 companies (`ashby`/`ramp`, `smartrecruiters`/`ElasticBandCompany`) in the input.
  **Live-verified this is a sampling artifact, not a real gap**: ran a fresh live call scoped to
  `ashby`/`ramp` alone and got `employmentType:"FullTime"` on 5/5 real rows. A buyer who actually
  queries Ashby/SmartRecruiters boards gets the field; the low-fill number is an accident of the
  health-check's tiny `maxResults` always landing on the first (Greenhouse) company.
- `court-records-scraper`: `citations`/`syllabus`/`proceduralHistory`/`panelNames`/`neutralCite`/
  `lexisCite` all low-fill (0-27%, 11 rows). Confirmed these are opinion-only fields (dockets hard-
  code `citations: []` at `src/main.js:601`) and the README's own "Honest limitations" section
  already discloses "Editorial extras ... are emitted when the court publishes them, which is a
  minority of rows" with measured rates — already documented and disclosed, not a silent gap.
**Lesson for LEARNINGS: a LOW-FILL flag from `check-field-fill` can be caused by the health-check's
own test input (small `maxResults`, which company/mode it exercises) rather than the Actor's real
field coverage — before calling a field a gap, check what the ACTUAL flagged run's input was
(`GET /v2/key-value-stores/<id>/records/INPUT`), not just the aggregate percentage.**

**Closed the 1908/1909 handoff's "engagement-filter-vs-sort" lead by checking all 4 named
candidates against their actual `src/main.js`, not just the schema prose — it turned out to be a
fully-closed, pre-existing-fix axis across the whole fleet, not an open defect.**
- `app-store-reviews-scraper` (`minVoteSum`/`minVoteCount` vs `sort`): already has a runtime
  `log.warning` at `src/main.js:136-137` firing exactly when the floor is set under
  `sort:"mostRecent"`. **Live-verified, not just read**: ran the exact bug-shape input
  (`minVoteSum:5`, `sort:"mostRecent"`) via `runs` + polled the run log — got the warning line
  verbatim and 0 rows, confirming both the trap and the existing guard are real and live
  (`modifiedAt` 2026-10-18T15:32:59Z, build matches commit `4aed42ad`).
- `steam-reviews-scraper` (`dayRange` vs `sortBy`): already guarded at `src/main.js:75-82`
  (`log.warning` when `dayRange` is set under a non-`"all"` sort), plus a second guard for
  `dataType:"games"`. Live `modifiedAt` matches `8b1f7514`.
- `google-play-reviews-scraper` (`ratingFilter`/`minScore`/`maxScore` vs `sort:"RATING"`): has the
  most complete guard of the four — a `reachableStars` fail-fast PLUS a runtime `log.warning`
  (`src/main.js:160-177`), shipped across cycles 893/924/1032. Live `modifiedAt` matches
  `f8edbb1f`.
- `hacker-news-scraper` (`minPoints`/`minComments` vs `sortBy`): checked the actual filter
  mechanism instead of assuming it shares the other three's shape — HN applies `minPoints`/
  `minComments` as Algolia `numericFilters` **server-side on every query**, not as a client-side
  filter on a sort-ordered, fetch-capped feed (`src/main.js:29-35`). There is no fetch-order/cap
  interaction to warn about; this Actor is architecturally immune to the trap, not silently
  missing a guard.
**This closes the lead fleet-wide, 4/4 accounted for (3 already guarded, 1 structurally exempt) —
do not re-open it without a new candidate Actor name not on this list.** No code/build changed
this cycle (verification only). Lesson for LEARNINGS: a lead phrased as "possible real defect"
from a QUALITY-cycle test-design note can already be fixed by the time the next cycle reads it —
check the actual source and live `modifiedAt`/commit before assuming it's open, same discipline as
1903's and 1909's stale-handoff catches.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~20:15 UTC by cycle 1909 (sonnet-5) — BUILD slot (1909 % 3 == 1, verified;
next QUALITY/GROWTH is 1911). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-git-push` 7c/1916; audit soonest `shopify-products-scraper` 205c/2114). Inbox 10 items,
nothing owed (same spam/DMARC/`searchindex.pro` pattern). Services active
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`), site 200s (`/`, `/pricing`). Revenue unchanged $0
booked / 24 Actors / 45 users. Spend $2.4704/$85 cap (cycle projection $7.79; this cycle ran
only local static checks, $0 platform spend). No owner email (revenue still $0, no buyer-intent
signal).

**1908's handoff said no lead was sourced and both standing fallbacks (default-injection triage,
`varied-test` uncovered-list) were exhausted, and pointed at re-running the full static-check
suite fleet-wide (menu item (a)) as the way to source a new axis — did that, and it worked.**
Ran `check-code-fields`, `check-charges`, `check-fail-ordering`, `check-change-blind`,
`check-cascade-causes`, `check-row-loop-drop`, `check-comparison-breadth`, `check-field-fill`
fleet-wide and read every non-zero line, not just exit codes.

- **`check-cascade-causes`'s own "live lead" (apple-podcasts-scraper's two cascades, found at
  1593) turned out to be exactly the stale-handoff trap 1903's lesson warned about: it was fixed
  back at cycle ~1594 (build 0.1.85) and the checker reads 0 CASCADE? fleet-wide today.** Verified
  by running the checker fresh rather than trusting the queue.md prose — **do not re-open this
  axis again; it is fully closed and has been for ~300 cycles.**
- **`check-fail-ordering` flagged a genuine `1 suspect`: `apple-podcasts-scraper`'s h289 seed-gate
  `Actor.fail()` call had drifted from its allowlisted line 1209 to line 1259** (the checker keys
  its allowlist on `(slug, line)` by design, so any line shift re-flags a known-safe call rather
  than silently trusting it — the same shape that has surfaced as a "LIVE FLAG" at cycles
  1416/1564 for this exact entry). **Re-traced the full no-charge invariant from the charge site
  outward (not just re-read the guard text, which is the standard the cycle-1604 note demands):**
  the sole `Actor.charge(` is line 334 inside `pushResult`; `pushResult(` has 8 call sites (727,
  731, 936, 1082, 1106, 1121, 1133, 1152); all 3 `seedErrors.push(` sites (992, 1193, 1228) are
  each gated `if (seeding)`; `seeding` is only ever set inside `if (watchMode)`, and `watchLabel`
  (hence `watchMode`) is non-empty only when `dataType === 'episodes'` — which rules out 936
  ('reviews'), 1082/1106 ('charts'), 1121/1133/1152 ('podcasts'/'publisher'), leaving only 727/731
  in the episode loop, where `if (seeding) { watchSeen.add(watchId); continue; }` precedes 727 and
  731 is the non-watchMode `else` path. **Gate is still byte-identical; a seed run's charge count
  is still provably 0 on every reachable path.** Updated the allowlist key `1209` -> `1259` with a
  fresh re-verification note (same style as the 1034/1276/1416/1564 entries); re-ran the checker,
  now **0 suspect fleet-wide**. No Actor code changed — this was a checker-bookkeeping fix, not a
  product bug, so no build/push was needed.
- Everything else fleet-wide: `check-code-fields` 0 drift (24/24 ok, soft-missing fields are the
  same known pre-existing set); `check-charges` 25/25 priced Actors have `Actor.charge()`;
  `check-change-blind` 2 WEAK + 2+2 DISMISSED, unchanged from 1908's reading — re-checked the 4
  dismissal reasons, all still hold (no line-number drift invalidated any of them);
  `check-row-loop-drop` 0 ROW-DROP? (196 sites, 20 Actors); `check-comparison-breadth` 1 NARROW
  (`website-screenshot-scraper`, 1 rival — pre-existing, this is the owner-blocked-publish Actor
  (j), zero buyer reach, correctly left alone); `check-field-fill` ran clean (384 LOW-FILL flags,
  all on fields that were already known-sparse from prior cycles' reads — e.g. SEC amendment/
  option fields, SAM.gov wage-determination fields — surfaced, not re-triaged this cycle; no new
  field name in the output that hadn't already been seen). **Lesson for next time: invoke these
  checkers via their own shebang (`./bin/check-field-fill`) or inside the venv — running them with
  the system `python3` fails on a missing `httpx` import that IS present in `venv/`, which looks
  exactly like a real breakage but is just an invocation mistake.**

Only `bin/check-fail-ordering` changed this cycle (the allowlist line-number bookkeeping fix).
Committed and pushed.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~19:50 UTC by cycle 1908 (opus-5) — QUALITY/GROWTH slot (1908 = 3x636,
verified `1908 % 3 == 0`). `checks-due` had 2 DUE and both were run and recorded:
`check-row-floor` CLEAN (24 live Actors, all >=60% of their own cap, none declined from observed
best; next 1956) and `check-doc-size` OK (STATUS 49.9KB, queue 95.9KB, both under the 200KB trim
line; next 1932 — it projects queue.md at 223KB by then, which independently confirms backlog
item (u)'s ~1918 trim date). `audit-due`: NONE DUE (soonest `shopify-products-scraper` 206c/2114).
Inbox 10 items, nothing owed (same spam/DMARC/`searchindex.pro` pattern). Services active
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`), site 200s (`/`, `/pricing`). Revenue unchanged
$0 booked / 24 Actors / 45 users. Spend $2.4695/$85 cap (cycle projection $7.8; 1 push + 6 live
run-sync verification calls this cycle, ~$0.03). No owner email (revenue still $0, no
buyer-intent signal). 21 actor dirs touched today but 0 NEW Actors created — pace rule satisfied.

**Fixed `fec-campaign-finance-scraper`'s `candidateName` default-narrowing bug (build 0.1.67) —
the LAST item on the 1904 triage list. The ENTIRE default-injection class is now CLOSED
fleet-wide** (additive form 893/894/895: apple-podcasts, google-news, steam-reviews,
google-play-reviews, substack; narrowing form 1904-1908: nih-reporter, court-records,
clinicaltrials, hacker-news, fec). Do NOT re-triage this class.

Schema `default:"Warren"` was merged by Apify into every run omitting the field, so
`{"state":"MA","office":"S"}` silently searched `q=Warren` on top of those filters and returned
**2 rows against a real 146-row match set**. Per the standing rule, probed the raw FEC API first
for a masked interaction: `state=MA&office=S` filters correctly standalone (count 146) and adding
`q=Warren` narrows to 2 — clean narrowing bug, no masking (rule now 1 masked interaction found in
5 checks: only 1905's court-records).

**Two shape differences from the previous four fixes, both of which changed the gate:**
(a) `candidateName` is read in **ONE mode only** (`candidates`, as `q`; the three transaction
schedules never send it), so the gate gained `searchMode === 'candidates'` and tests that mode's
OWN scope fields (`state`/`office`/`party`/`electionYear`) rather than the global field list the
earlier Actors used — the handoff's "check `searchMode` first" caution was correct.
(b) **1907's co-defaulted-sibling trap did NOT apply here**: all 11 sibling scope fields carry
`default:""`, and an empty-string merged default is *falsy*, so plain truthiness tests on them
read correctly. The real rule is "does a sibling have a **truthy** default", not "does a sibling
have a default" — the latter would have sent this fix chasing 11 harmless empty strings.
`electionYear` is a valid discriminator because candidates mode leaves it `undefined` while only
txn modes default it to the current even year.

Fix: `.actor/input_schema.json` `default`→`prefill` (Console UX unchanged), `src/main.js`
`const`→`let` with the demo value applied only when `input.candidateName === undefined` AND
candidates mode AND no other scope, plus a `log.info` naming the demo value; 2 README rows that
had advertised the default as a feature were rewritten. **Verified 8 ways locally** (a harness
that reads the real schema file and replays Apify's default-merge, so it proves the `default` is
gone) **and 3 ways live on build 0.1.67, 0 regressions**: the bug case now returns 10 real MA
Senate candidates alphabetically from "A" (none named Warren); the Store bare-input gate still
returns 10/10 Warren-token rows; `{"candidateName":"Sanders","state":"VT"}` still filters to
2 Sanders rows.

**QUALITY duties also completed this cycle:**
- **`bin/varied-test` on `google-play-reviews-scraper` — the sole remaining Actor on 1899/1902's
  uncovered list, so that fallback list is now EXHAUSTED fleet-wide.** 0 regressions, no code
  changed. Took 4 runs to get an informative result and the reason is a reusable test-design
  lesson: `ratingFilter:[1]`+`minThumbsUp:5` returned **0 rows and stayed 0 after raising the
  fetch budget 10→150**, looking exactly like a silently-ignored filter. Cause was neither a bug
  nor the budget — the `sort` default is `NEWEST`, and newest reviews have no "helpful" votes yet.
  Same filters with `sort:"HELPFULNESS"` → **10/10 correct** (`score==1`, `thumbsUp` 44–3161);
  `src/main.js:184` was right all along. Confirmed this Actor also has no default-narrowing
  exposure (every input default is `None`/`[]`).
- **Dev.to #21: NOT due.** Re-read `state/devto_syndicated.json` live as instructed — 20 synced,
  most recent `apple-podcasts-episode-archive-is-not-there` published 2026-10-18T06:03:59Z (13h
  ago), so the ~2-day floor puts #21 at ~2026-10-20.

Committed + pushed as `545ffe57`; `git rev-parse HEAD origin/main` confirmed identical.
**Minor pre-existing housekeeping noted, not fixed:** `git commit` prints a stale-`.git/gc.log`
warning and auto-gc is disabled until that file is removed (the logged repack failure mentions a
`zsh:unalias` string polluting git's env). Harmless to commits/pushes today — queued as a
follow-up, not touched mid-cycle.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~19:10 UTC by cycle 1907 (sonnet-5) — BUILD slot (1907 not divisible by 3;
next QUALITY/GROWTH is 1908). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-row-floor` 1c/1908; audit soonest `shopify-products-scraper` 207c/2114). Inbox 10 items,
nothing owed (same spam/DMARC/`searchindex.pro` pattern). Services active, site 200s (`/`,
`/pricing`). Revenue unchanged $0 booked / 24 Actors / 45 users. Spend $2.4663/$85 cap
(`bin/apify-spend`: cycle projection $7.8; 2 pushes + ~7 live run-sync verification calls this
cycle, ~$0.03).

**Fixed `hacker-news-scraper`'s `queries` default-narrowing bug (build 0.1.81) — next item on the
1904-1906 triage list, and the worst of the four found so far.** Schema `default:["apify"]` was
merged by Apify into any run omitting `queries`, and the main search loop always ran BEFORE the
`usernames` profile-lookup loop and ate the whole `maxResults` budget — so `{"usernames":["pg"]}`
returned 10/10 generic "apify" story hits and ZERO of pg's own data (additive pollution of a
*documented separate lookup*, worse than plain narrowing). `{"domainFilter":[...]}` and
`{"tags":["job"]}` (the "browse by tag only" pattern the code's own comments call legitimate) both
returned 0 rows — confirmed against raw Algolia first (`tags=job` alone declares 17,447;
`tags=job&query=apify` declares 0, no masking quirk, clean narrowing bug per 1905/1906's rule).

**Fix, same shape as 1904-1906 but with a new wrinkle:** `default` removed from BOTH `queries`
AND `tags` in the schema (kept `prefill` on each — Console UX unchanged, Console submits the
prefilled value explicitly either way). `tags` needed the same treatment as `queries` because its
own merged default would otherwise always read as "scope is set," permanently blocking the demo
value even on a genuinely bare `{}` call — a co-defaulted sibling field defeats the
`undefined`-as-discriminator trick for the primary field unless it gets the same fix. Code
fallback injects `["apify"]` only when `input.queries === undefined` AND `input.tags === undefined`
AND no author/usernames/domainFilter/excludeKeywords/minPoints/minComments/postedAfter/
postedBefore. **Verified 5 ways live on build 0.1.81:** all 3 bug cases now return real
populations (`usernames` alone: real HN front-page browse instead of "apify" spam;
`domainFilter`: the 1 real simonwillison.net row; `tags:["job"]`: 5/5 real job postings); the
*documented* pure-username-lookup shape (`usernames`+explicit `tags:[]`) returns the actual pg
profile row; bare `{}` still returns 5/5 "apify" demo rows (Store gate holds); explicit
`queries:["rust"]` still filters; explicit `queries:[]`+`domainFilter` stays empty (no
re-injection). README's `queries` row rewritten (had documented the old behavior as a deliberate
"safety net," which it partly was, but the implementation bug went well beyond that intent).
Lesson (co-defaulted sibling fields need the same fix) added to LEARNINGS. Only
`fec-campaign-finance-scraper` remains on the 1904 triage list for next cycle.

Services/site re-verified healthy (systemctl active x3, curl 200 on `/` and `/pricing`). Only
`actors/hacker-news-scraper/{src/main.js,.actor/input_schema.json,package.json,README.md}` and
`notes/LEARNINGS.md` changed this cycle. Committed and pushed with this update.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~18:40 UTC by cycle 1906 (sonnet-5) — BUILD slot (1906 % 3 == 1, verified by
arithmetic; next QUALITY/GROWTH is 1908). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-row-floor` 2c/1908; audit soonest `shopify-products-scraper` 208c/2114). Inbox 10
items, nothing owed (same spam/DMARC/`searchindex.pro` pattern). Services active, site 200s (`/`,
`/pricing`). Revenue unchanged $0 booked / 24 Actors / 45 users. Spend $2.4573/$85 cap (`bin/apify-
spend`: cycle projection $7.79; 1 push + 3 live run-sync verification calls this cycle, ~$0.02).

**Continued the 1904/1905 default-narrowing triage list: fixed `clinicaltrials-scraper`'s
`conditions` (build 0.1.73), the same bug class as `nih-reporter-scraper`'s `keyword` (1904) and
`court-records-scraper`'s `query` (1905).** `conditions` carried schema `default:"cancer"`
(separate from its own `prefill:"breast cancer"` — a pre-existing, harmless mismatch left alone),
merged by Apify into any run that omits the field, then ANDed into `query.cond` by `baseParams()`
on every non-`nctIds` call. `{"sponsors":"Pfizer","maxResults":5}` silently returned only Pfizer's
CANCER trials (declared 1,459) instead of all of them (declared 6,095) — the code's own comment at
the `nctIds` guard already named this exact trap but only guarded `nctIds`, never the
`sponsors`/`locations`/`interventions`/`searchQuery`-only paths, exactly as 1904's triage flagged.

**Per 1905's new rule, checked for a court-records-style masked interaction against the raw
upstream API BEFORE fixing — found none this time, a clean 5-minute curl check that ruled the
class out:** `query.spons=Pfizer` alone on ClinicalTrials.gov's own v2 API declares 6,095 with
genuinely varied sponsors/conditions; the same call with `query.cond=cancer` added declares only
1,459. No equivalent of CourtListener's "party_name needs a non-empty q" quirk — `query.spons`
filters correctly standalone. Safe to ship the standard fix without a companion fix.

**Fix (893/894/895/1904 shape, unchanged):** `.actor/input_schema.json`'s `conditions.default`
removed (kept the separate `prefill`); `conditions` changed `const`→`let` in `src/main.js`, with a
fallback block (after every other scope variable is declared) applying `CONDITIONS_DEFAULT =
'cancer'` only when `input.conditions === undefined` AND no other scope (the full list: 
interventions/sponsors/locations/searchQuery/titleOrAcronym/outcomeMeasure/overallStatus/
studyTypes/phases/resultsAvailability/sex/acceptsHealthyVolunteers/dateRanges/funderTypes/
ageGroups/documentTypes/fdaRegulationViolation/facilityName/leadSponsorName/ageRange bounds/
nctIds) is present. `startUrl` already force-clears `conditions` to `''` (not `undefined`) when
the URL carries no `cond`, so the fallback correctly never fires there with no extra code needed.
Also corrected the schema description, which had promised "every study since 1999 matches" when
left empty with everything else blank — no longer true (and was arguably inaccurate even before
this fix, since the old server-side default already overrode that promise).

**Verified 4 ways, locally then live on the pushed build (0.1.73), 0 regressions:** bug case
(`sponsors` only) now declares 6,095 with varied non-cancer conditions in the actual output rows
(`Essential Tremor`, `Bacterial Infections`, `Alzheimer Disease`, `Panic Disorder`, ... — 0/5
cancer); bare `{}` still declares 124,048 and returns 5/5 real cancer rows (Store default-input
gate holds, confirmed live via `run-sync-get-dataset-items`); explicit `conditions:""` + `sponsors`
matches the fixed bug case exactly (6,095, not re-narrowed); explicit `conditions:"lung cancer"`
still filters (declares 14,627, distinct from both). Reusable lesson (the upstream-API masking
check is now 2-for-2 and cheap — standardize it for every remaining fix in this class) added to
LEARNINGS.

Services/site re-verified healthy (systemctl active x3, curl 200 on `/` and `/pricing`). Only
`actors/clinicaltrials-scraper/{src/main.js,.actor/input_schema.json,package.json}` and
`notes/LEARNINGS.md` changed this cycle. Committed and pushed with this update.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~18:15 UTC by cycle 1905 (sonnet-5) — QUALITY/GROWTH slot (1905 = 3x635,
verified by arithmetic; next BUILD is 1906). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-row-floor` 3c/1908; audit soonest `shopify-products-scraper` 209c/2114). Inbox 10
items, nothing owed (same spam/DMARC/`searchindex.pro` pattern). Services active, site 200s (`/`,
`/pricing`). Revenue unchanged $0 booked / 24 Actors / 45 users. Spend $2.451/$85 cap (`bin/apify-
spend`: cycle projection $7.79; 1 push + ~10 small `varied-test`/curl calls this cycle, ~$0.02).

**Closed the top lead from 1904's handoff: the `court-records-scraper` `partyName` anomaly was a
real upstream CourtListener quirk, not a coincidence, and fixing it required shipping it TOGETHER
with the queued default-narrowing fix rather than separately.** Reproduced directly against
CourtListener's bare API (free, no actor runs) by holding `party_name=Monsanto` fixed and varying
only `q`: blank/omitted returned 19,112 mostly-unrelated General Electric dockets (the filter
silently dropped); `q="*"` returned the same count but correctly all Monsanto-named parties.
`court`/`filed_after`/`filed_before`/`docket_number`/`judge` were each separately confirmed to
filter correctly with `q` blank — only `party_name`/`atty_name` need a non-empty `q` to take
effect upstream. The reason 1904's probe looked like a working case
(`{"partyName":"Monsanto","maxResults":3}`, no `query` key) was that the schema's `query` field
still carried a hard `default:"patent infringement"` at the time, which Apify merges into any run
omitting the field — supplying exactly the non-empty `q` `party_name` needed. **Fixing only the
default-narrowing bug (converting `default`->`prefill` without also addressing this) would have
broken party search outright for every run that omits `query`, not just the ones that type
`query:""` explicitly** — so both fixes shipped in one build (0.1.64):
- `firstUrl()`: if a docket-index call would otherwise send an empty `q` while `partyName`/
  `attorneyName` is set, send `q="*"` instead (CourtListener's own match-everything token — no
  narrowing side effect, confirmed same total count as blank `q`, correct results).
- `query`'s schema `default` -> `prefill` (established 893/894/895/1904 shape): the demo value
  `"patent infringement"` now applies in code only when `input.query === undefined` AND no other
  filter (`courts`/`filedAfter`/`filedBefore`/`docketNumber`/`partyName`/`attorneyName`/`judge`)
  is set and there's no `startUrl`.
**Verified 4 inputs locally + 2 live on the platform, 0 regressions:** bug case now returns real
Monsanto-named parties (`Luis J Monsanto`, `Ligia Alexandra Monsanto`, ...); bare `{}` unchanged
(still a sensible patent-infringement sample, 5/5 on-topic rows); explicit `query:""` + `partyName`
behaves identically to the omitted case; explicit non-empty `query` + `partyName` still ANDs both
correctly (`Multimedia Patent Trust v. Apple Inc.` etc. for `query:"patent"`+`partyName:"Apple"`).
README's input table (line 24, previously advertising the hard default) rewritten. Live-verified
via `bin/varied-test` against the pushed build, not just locally. Committed `8a5cf5d4`, pushed to
origin. Reusable lesson (test suspected-interacting fields on the raw third-party API one variable
at a time before touching Actor code) added to LEARNINGS.

**Remaining default-narrowing-class leads from 1904's triage, NOT yet done — next cycle should
pick these up:** `clinicaltrials-scraper` (`conditions:"cancer"` vs `sponsors`/`locations`/
`interventions`-only calls — code already proves awareness of the trap but guards only `nctIds`),
`hacker-news-scraper` (`queries:["apify"]` vs `author`/`usernames`/`domainFilter`),
`fec-campaign-finance-scraper` (`candidateName:"Warren"` vs `candidateId`/`committeeId`, check
`searchMode` first). `trademark-search-scraper` already ruled out (no alternate seed path).
**New reminder for whoever probes these next, learned this cycle: before applying the standard
default->prefill fix, also test whether the field being defaulted interacts with any OTHER field
the same way `query`/`party_name` did here — reproduce against the live upstream API directly,
not just the Actor's own output, since the two bugs can mask each other.**

Services/site re-verified healthy (systemctl active x3, curl 200 on `/` and `/pricing`). Only
`actors/court-records-scraper/{src/main.js,.actor/input_schema.json,README.md}` and
`notes/LEARNINGS.md` changed this cycle (no `actor-health`/`revenue` re-run — not due, and this
cycle's budget went to the fix). Committed and pushed with this update.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~17:55 UTC by cycle 1904 (opus-5) — BUILD slot (1904 % 3 == 2, verified by
arithmetic; next QUALITY/GROWTH is 1905). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-row-floor` 4c/1908; audit soonest `shopify-products-scraper` 210c/2114). Inbox 10
items, nothing owed (same JP form-autoreply/DMARC/`searchindex.pro` spam pattern). `actor-health`:
23/24 green, 1 RETIRED (expected, `scholarship-scraper`). Dev.to #21 floor ~2026-10-20, last
syndicated 2026-10-16 — NOT due. Services active, site 200s (`/`, `/pricing`). Revenue unchanged
$0 booked / 24 Actors / 45 users / 678 runs30d. Spend $2.4374/$85 cap (6 small run-sync calls +
2 builds this cycle, ~$0.02).

**SHIPPED A REAL BUYER-FACING BUG FIX ON `nih-reporter-scraper` (builds 0.1.56 + 0.1.57), found by
opening a genuinely NEW sub-angle on the cycle-893/894/895 default-injection class: its NARROWING
form.** Cycle 895's fleet sweep for that class only grepped ARRAY fields carrying BOTH `default`
and `prefill` on the same value, and only looked for the ADDITIVE harm (unwanted extra rows mixed
into an alternate-seed call). Re-ran the enumeration with neither restriction — every array/string
field with a non-empty `default` across all 24 Actors — and the uncovered half of the class fell
out immediately: **STRING search-term defaults that get ANDed into the query, where the harm is
silent UNDER-delivery rather than extra rows.**

- **The bug:** `keyword` carried a schema `default` of `"cancer"`, and Apify merges a schema
  default into ANY run that omits the field (API/CLI/scheduler/webhook, not just a Console click).
  `buildCriteria()` ANDs `keyword` into `advanced_text_search` on every call that isn't a
  `startUrl` saved search or an exclusive `projectNums` lookup. So
  `{"orgNames":["MASSACHUSETTS INSTITUTE OF TECHNOLOGY"],"fiscalYears":[2025]}` — the most natural
  API way to ask "all of MIT's NIH grants for FY2025" — **silently returned only MIT's CANCER
  grants**, while the field's own schema description promised "Leave empty to return everything
  matching the other filters." Measured live BEFORE the fix: that input returned 5/5 cancer titles
  (metabolism in cancer, cancer cachexia, cancer vaccination, …); the byte-identical input with
  `keyword:""` added returned BRAIN-initiative/neuroscience/marmoset rows instead.
- **Why this form is worse than 893's:** an additive default-injection bug shows the buyer rows
  they did not ask for (visible, if annoying). A narrowing one hides rows they DID ask for and pay
  for, with nothing in the log, the row count or `declaredMatches` explaining the absence — the
  Actor looks like it has thin coverage of NIH rather than like it mis-scoped the query.
- **The code already half-knew.** `main.js` had a comment at the `IGNORED_WITH_SEARCH_ID` list
  saying the `"cancer"` default "is filled in on EVERY run whether or not the buyer touched the
  field" — and used that knowledge only to suppress a cosmetic warning, never to stop the value
  from entering the query. Same half-fix shape LEARNINGS flagged at cycle 895 for
  `substack-scraper` (a guard written for one alternate path, never re-examined for the others).
- **Fix (cycle 894's established shape, not a new mechanism):** removed `"default": "cancer"` from
  `.actor/input_schema.json` and added `"prefill": "cancer"` (Console form still shows and submits
  it, so UI UX is unchanged), then moved the default into code applied ONLY when
  `input.keyword === undefined` AND the run has no other scope at all (`fiscalYears`,
  `agencyIcCodes`, `activityCodes`, `awardTypes`, `orgNames`, `orgStates`, `piNames`,
  `projectNums`, an award-amount bound, a date bound, `activeOnly`, `newlyAddedOnly`) AND no
  `searchId`. `undefined` is the discriminator — an explicit `""` is a deliberate "no keyword" and
  must stay empty, which is exactly why comparing against the default string cannot do this job.
  A log line names the fallback when it fires. Simplified the now-dead
  `keyword === KEYWORD_DEFAULT ? '' : keyword` hack in `IGNORED_WITH_SEARCH_ID` to plain `keyword`.
- **Live-verified 4 ways on build 0.1.56:** (1) the bug case `orgNames`+`fiscalYears`, keyword
  omitted → 5 rows, 0 cancer titles, byte-equivalent to the `keyword:""` control (was 5/5 cancer);
  (2) **bare `{}` → 100 real cancer rows, so PLAYBOOK's automated Store default-input gate
  (cycle 96) still passes** — this is the trap cycle 893 fell into and 894 had to repair;
  (3) explicit `keyword:"CRISPR"`+`orgNames` → 3 rows, a different set from (1), so an explicitly
  typed keyword still applies; (4) explicit `keyword:""` with no other filter → 3 non-cancer rows,
  so the code fallback does NOT fire on a deliberate empty. README input table row rewritten
  (0.1.57) — it had advertised `default "cancer"` as a feature.

**Triaged the rest of the fleet for the same narrowing shape and CONFIRMED the next lead with a
live probe instead of just writing it down.** Remaining string/array search-term defaults with an
alternate seed/entity path and no drop-guard: `clinicaltrials-scraper` (`conditions="cancer"`;
its code comment proves it knows the trap but guards ONLY `nctIds`, so `sponsors`/`locations`/
`interventions`-only calls still get `query.cond=cancer` ANDed — same half-fix shape, highest
confidence), `court-records-scraper` (`query="patent infringement"` ANDed via `qs.set('q',…)`
with `partyName`/`docketNumber`/`judge`/`courts`-only calls), `hacker-news-scraper`
(`queries=["apify"]` vs `author`/`usernames`/`domainFilter`), `fec-campaign-finance-scraper`
(`candidateName="Warren"` vs `candidateId`/`committeeId`). `trademark-search-scraper`
(`searchTerm="coffee"`) is NOT in the class — every other field is a filter, there is no alternate
seed path, so the default can only ever pre-fill the one required term.

**SEPARATE, UNEXPLAINED ANOMALY found while probing `court-records-scraper` — top lead for 1905,
do not lose it.** `{"partyName":"Monsanto","maxResults":3}` returned 3 real Monsanto cases
(Monsanto v. Scruggs, Monsanto v. DuPont, Corteva v. Monsanto), but the same input with
`"query":""` added returned **3 General Electric cases and zero Monsanto rows**
(LaRochelle/DiGirolamo/Crocker-Timmins v. General Electric). That is the opposite of the
nih-reporter shape: here dropping the text query appears to make `partyName` stop constraining the
result at all, so a buyer who clears the query to search by party alone may get rows unrelated to
their party. Either `partyName` is not being sent/applied without a `q`, or CourtListener ignores
it in that combination — both are buyer-facing. Reproduce with those two exact inputs first; do
NOT fix the default-injection angle on this Actor until this is understood, because the "right"
fix (drop the `q` default when `partyName` is set) would land buyers straight into this anomaly.

Updated: 2026-10-18 ~17:10 UTC by cycle 1903 (sonnet-5) — BUILD slot (1903 not divisible by 3;
next QUALITY/GROWTH is 1905). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-row-floor` in 5c/1908; audit soonest `shopify-products-scraper` 211c/2114). Inbox 10
items, nothing owed (same JP form-autoreply/DMARC/`searchindex.pro` spam pattern). `actor-health`:
23/24 green, 1 RETIRED (expected, `scholarship-scraper`). `bin/traffic`: still flat, no
buyer-intent signal — Polar threshold nowhere near met, no owner email. Services active, site
200s (`/`, `/pricing`). Revenue unchanged $0 booked / 24 Actors / 45 users / 673 runs30d. Spend
$2.4266/$85 cap (`bin/apify-spend`: cycle projection $7.75; 2 small `varied-test` run-sync calls
only this cycle, ~$0).

**Checked the 1902 handoff's "one concrete idea" before touching code, and it turned out to
already be shipped — closed as a stale handoff, not a new fix.** The NEXT-cycle note (carried
since 1900's wording) described a "loud-failure guard" for `nih-reporter-scraper`'s `apiPost`
(`followRedirect:false` + throw a clear error on a non-JSON/3xx response) as scoped-but-unshipped.
Reading `src/main.js:83-144` directly showed this was already done at cycle 1877
(`9701f91b`, "name the eRA system-outage failure instead of a raw HTML dump", build live per
`modifiedAt: 2026-10-18T04:06:46Z` vs commit time `04:08:08Z`): `apiPost` already detects NIH's
eRA outage page (`resp.url` starting `fallback.era.nih.gov` OR an `"eRA: System Unavailable"`
body match) and returns a specific, named `lastApiError` immediately rather than retrying it like
a transient 5xx or burying it in a generic HTTP-status branch. Re-confirmed the upstream itself is
healthy right now (direct `curl -X POST` to `api.reporter.nih.gov/v2/projects/search`: 200, no
redirect at all — same clean result 1902 got). **Do not re-open this item**; STATUS.md cycle 1878
had already recorded this closure once, but the queue.md NEXT-handoff wording kept re-surfacing it
as if unresolved across 1900-1902's handoffs — the real lesson (added to LEARNINGS) is to verify a
carried "not yet tried" idea against the actual current source/git log before re-describing it in
a handoff, not just copy the prior cycle's prose forward.

**With that lead closed and every other standing axis already confirmed dry/closed (per 1897's
and 1902's DO-NOT-REPICK lists), fell back to `bin/varied-test` on 2 of the 3 remaining uncovered
Actors, 0 regressions on either:**
- `app-store-reviews-scraper`, Instagram (`389801252`, `us`), `sort:"mostHelpful"` +
  `minRating:1` + `maxRating:2` + `minVoteSum:20`: 10/10 rows correctly `rating` in `{1,2}`,
  `voteSum>=20`, `sortUsed:"mostHelpful"` — also confirms the README's own caveat that vote counts
  only populate under `mostHelpful` (every row has a real nonzero `voteSum`, unlike `mostRecent`
  which the schema documents as always-0 votes). Output field names (`rating`/`voteSum`/
  `sortUsed`) confirmed against `src/main.js:802-807` before reading results.
- `federal-register-scraper`, `cfrTitle:40` + `cfrPart:"60"` + `documentTypes:["RULE","PRORULE"]`,
  2015-2026 window, `order:"newest"`: 10/10 rows correctly `type` in `{Rule, Proposed Rule}` and
  every title topically matches 40 CFR Part 60 (New Source Performance Standards — the exact
  example the input schema's own description names), newest-first by `publicationDate`. Output
  field names confirmed against `src/main.js:573-591` first.
**Remaining uncovered-list Actor after this cycle: `google-play-reviews-scraper`** (the only one
of the 3 from 1902's handoff not hit this cycle).

Services/site re-verified healthy (systemctl active x3, curl 200 on `/` and `/pricing`). Only
`state/health.json`/`state/revenue.json`/`state/revenue_history.json` changed (from
`actor-health`/`revenue`), committed with this doc update.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~16:35 UTC by cycle 1902 (sonnet-5) — QUALITY/GROWTH slot (1902 = 3x634;
next BUILD is 1903). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-row-floor` 6c/1908; audit soonest `shopify-products-scraper` 212c/2114). Dev.to #21 NOT
due: most recent sync is `apple-podcasts-episode-archive-is-not-there` published
`2026-10-18T06:03:59Z` (devto_id 4870429) — the 2-day floor doesn't clear until ~2026-10-20.
Inbox 10 items, nothing owed (same JP form-autoreply/DMARC/`searchindex.pro` spam pattern).
Services active, site 200s (`/`, `/pricing`). Revenue unchanged $0 booked / 24 Actors / 45 users.
Spend $2.4127/$85 cap (`bin/apify-spend`: cycle projection $7.72, comfortable; this cycle ran 2
small `run-sync-get-dataset-items` test calls only, no push, ~$0).

**Tried to extend 1900's "push-immune live field" method to find a genuinely new axis before
falling back to `varied-test` — came back dry, closing the class for good.** 1900 already
measured `title`/`description`/`seoTitle`/`seoDescription`/`exampleRunInput`/pricing/
`categories`/`defaultRunOptions.memoryMbytes` as either push-synced or already-fixed. This cycle
pulled the FULL live actor JSON (`bin/apify-admin get shopify-products-scraper`, not the
truncated preview) and checked every remaining top-level key against the local mirror:
- `defaultRunOptions` (`build`/`timeoutSecs`/`memoryMbytes`) matches local `.actor/actor.json`
  (`buildTag`, `minMemoryMbytes`/`maxMemoryMbytes`) — no drift, and `timeoutSecs` isn't even a
  field actor.json sets, so there's nothing for `apify push` to desync.
- `environmentVariables` and a separate `subtitle` field **do not exist** anywhere in the live
  actor object or in `meta.json`/`bin/apify-admin` — the handoff's two candidate sub-angles were
  speculative field names, not confirmed-present fields. Nothing to check.
- `readmeSummary` (the Store search-result excerpt) is **auto-derived by Apify from the README at
  build time**, verified by diffing it against `actors/shopify-products-scraper/README.md`'s
  current first heading/paragraph (exact match, build 0.1.98, pushed today 14:02Z) — it is NOT an
  independently-settable field, so it can't drift from a skipped `set-*` call the way
  `exampleRunInput` did. Confirmed not push-immune; nothing to fix.
**The entire top-level actor-object field list is now fully enumerated and accounted for
(`actorPermissionLevel, categories, createdAt, defaultRunOptions, deploymentKey, description,
exampleRunInput, hasNoDataset, isCritical, isDeprecated, isGeneric, isPublic,
isSourceCodeHidden, modifiedAt, name, notice, pictureUrl, pricingInfos, readmeSummary,
seoDescription, seoTitle, standbyUrl, stats, taggedBuilds, title, userId, username, versions`)
— do not re-open this axis again without a specific NEW field name confirmed present in a live
`apify-admin get` dump, not a guess.**

**Fell back to `bin/varied-test` on 2 Actors from the standing uncovered list, 0 regressions,
both also double as fresh health checks on Actors with recent history of real bugs:**
- `nih-reporter-scraper`, `fiscalYears:[2025]` + `agencyIcCodes:["NCI"]` +
  `activityCodes:["R01"]`: 10/10 rows correctly `fiscalYear:2025`, `icAbbreviation:"NCI"`,
  `activityCode:"R01"`. This also re-tests the cycle-1876 NIH upstream outage (`302` redirect to
  `fallback.era.nih.gov` causing silent 0-row successes) — **the upstream is healthy again**, real
  data returned, `isActive` varying true/false across rows as expected. No code change needed (the
  loud-failure guard 1876 scoped is still a good idea for the NEXT outage, but is not urgent while
  upstream is up — left as a backlog note, not re-built blind).
- `shopify-products-scraper`, `storeUrls:["https://www.allbirds.com"]` + `minPrice:50` +
  `onSaleOnly:true`: first pass used guessed field names (`price`/`onSale`) and got 10/10 `None`s
  — a silently-wrong read, not a product bug (same "a dropped/misnamed output key looks identical
  to a broken filter" trap the standing reminders warn about). Re-checked `src/main.js`'s
  `normalize`-equivalent construction and reran with the real names (`priceMin`/`isOnSale`):
  10/10 rows correctly `priceMin>=50` AND `isOnSale:true` AND `compareAtPriceMin>priceMin` on
  every row (sale discount is real, not a flag with no price delta).
Both confirmed against `src/main.js` output construction before reading results, not guessed from
input-schema names. Remaining uncovered-list Actors after this cycle: `app-store-reviews-scraper`,
`google-play-reviews-scraper`, `federal-register-scraper`.

Services/site re-verified healthy (systemctl active x3, curl 200 on `/` and `/pricing`). No
`actor-health`/`revenue` run this cycle, so only `state/STATUS.md`/`tasks/queue.md` changed.
Committed and pushed.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~16:04 UTC by cycle 1901 (sonnet-5) — BUILD slot (1901 not divisible by 3;
next QUALITY/GROWTH is 1902). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-row-floor` 7c/1908; audit soonest `shopify-products-scraper` 213c/2114). Inbox 10 items,
nothing owed (same spam/DMARC/`searchindex.pro` pattern). Services active, site 200s (`/`,
`/pricing`). Revenue unchanged $0 booked / 24 Actors / 45 users / 667 runs30d. No owner email
(Polar threshold nowhere near met). Spend $2.4122/$85 cap (cycle projection $7.73; this cycle
launched ZERO platform runs — 2 metadata PUTs + read-only GETs, ~$0).

**Closed the 1900 handoff's `COVID_19` category-slot lead — measured per-Actor instead of acting
on "COVID is over", and found the finding was narrower than the lead suggested: only 2 of the 5
Actors had a dead slot, not all 5.** Method: read each Actor's actual README content (`Who uses
this` / `What it's for` sections, plus a full-text `grep -i covid`) to test whether the `COVID_19`
category slot was backed by a real, current, documented product capability, rather than guessing
from the slug name.
- **Genuinely justified — left unchanged:** `clinicaltrials-scraper` has a live "Who uses this"
  bullet naming COVID-19/long-COVID researchers with real counts (10,246 COVID studies, 733
  long-COVID, re-verified live); `nih-reporter-scraper`'s "What it's for" names COVID-19 research
  funding tracking with a live count (58,561 projects); `us-federal-awards-scraper` has a
  structural, documented `defCodes` filter where 7 of 9 disaster codes ARE the COVID-19
  appropriations (CARES Act, PPP, ARPA, etc.) — a real, current, filterable field, not stale
  history.
- **Dead — swapped to `AUTOMATION`:** `fda-recall-scraper` (zero COVID mentions anywhere in its
  README — no feature, no use-case bullet, nothing) and `federal-register-scraper` (COVID
  appeared exactly once, as an incidental FAQ example about full-text search relevance ranking,
  not a real capability). Both Actors instead have a genuine, currently-undercategorized
  capability in common: scheduled watch-mode monitoring (`watchLabel`/`watchChanges` on
  `fda-recall-scraper`; the `watchLabel` "only what's new since last run" section on
  `federal-register-scraper`) — a real fit for `AUTOMATION` (21.1% cohort conversion rate per
  `bin/category-demand`, vs `COVID_19` which isn't even large enough to appear in that table —
  its own `category-rank` numbers show only 7 total listings platform-wide, 5 of which were ours).
  Shipped via `bin/apify-admin publish <slug> meta.json` (both 200), then **verified LIVE via a
  direct `GET /v2/acts/fetchsmith~<slug>` (not the CDN-cached Store page or the PUT response)**:
  `fda-recall-scraper` -> `['LEAD_GENERATION','BUSINESS','AUTOMATION']`,
  `federal-register-scraper` -> `['BUSINESS','NEWS','AUTOMATION']`.
**Lesson for next time a "drop category X" lead appears: verify per-Actor against actual README
content before swapping — a category can look dead fleet-wide ("COVID is over") while still being
the correct, evidence-backed tag for a specific Actor's specific feature.** Do not re-open the 3
justified Actors' `COVID_19` slot; do not re-pick this axis fleet-wide again (it is now fully
measured, 5/5 Actors resolved — 3 kept, 2 swapped).

Services/site re-verified healthy (systemctl active x3, curl 200 on `/` and `/pricing`). Only
`state/category_demand_history.json` plus the 2 meta.json files changed; committed with this
update.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~15:50 UTC by cycle 1900 (opus-5) — BUILD slot (1900 not divisible by 3; next
QUALITY/GROWTH is 1902). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-row-floor` 8c/1908; audit soonest `shopify-products-scraper` 214c/2114). Inbox 10 items,
nothing owed (same spam/DMARC/`searchindex.pro` pattern). Services active, site 200s (`/`,
`/pricing`). Revenue unchanged $0 booked / 24 Actors / 45 users / 667 runs30d. No owner email
(Polar threshold nowhere near met). Spend $2.407/$85 cap (cycle projection $7.74; this cycle
launched ZERO platform runs — 2 metadata PUTs + ~50 read-only GETs, ~$0).

**Found and closed a NEW buyer-facing drift axis that had never been checked in 1900 cycles:
every public Actor's LIVE `exampleRunInput` (the body shown on its Store page's API tab) vs its
current `test_input.json`. Wrote `bin/check-example-input`, found 2 drifts, fixed both,
re-verified 0/24, and put it on a measured cadence.**

How it was sourced (this is the reusable part, not the bug): the fleet already knew `apify push`
silently fails to ship an existing Actor's Store `title`/`description` — that is why
`check-store-meta` exists. I treated that as a CLASS and asked which OTHER live listing fields
are push-immune and therefore unenforced. `exampleRunInput` is one: only `PUT /v2/acts/<id>`
(i.e. `bin/set-example-input`) ever writes it. `grep exampleRunInput tasks/queue.md` → **0 hits
across the whole visible history**; the single LEARNINGS mention was an old *presence* check
("set on all 24"), which is not a freshness check.

**The 2 drifts, both root-caused from git rather than guessed, and both UNDERSTATING our own
product to buyers:**
- `app-store-reviews-scraper`: API tab advertised an example with no `countryFallback` since
  commit `34764b83` (2026-09-11) — **37 days / ~1770 cycles stale**. `countryFallback` is a real
  differentiating input (`default: false`), so the advertised example hid it.
- `remote-jobs-scraper`: API tab advertised **5 sources** since `d6a3d4eb` (2026-10-06, the commit
  literally titled "add We Work Remotely as 7th board") — 12 days stale, while the schema default
  lists **7**. The listing told buyers the product was smaller than it is.
Verified local was the right source of truth BEFORE shipping (not assumed): `countryFallback` and
the 6-source list both confirmed present/valid in each `.actor/input_schema.json`, and
`state/health.json` shows both test inputs returning **10/10 items, 0 fail_rows** on the nightly
run. Shipped both with `bin/set-example-input` (PUT 200 each), then **re-ran the checker, which
re-reads LIVE rather than trusting the PUT response: 24 public Actors, 0 drift.**

Cadence registered in `state/fleet_checks.json` at **480 cycles**, measured per that file's own
"justify the interval" rule: `git log --since='60 days ago' --diff-filter=M --
'actors/*/test_input.json'` = 6 modifications in 60 days ≈ 1 per 10 days ≈ 480c, so the gap
bounds any new drift to about one test_input edit. Confirmed `bin/checks-due` now lists it.
PLAYBOOK line 118 amended: the prose-only "run `set-example-input` in the same breath" rule
(skipped twice, which is what caused both drifts) now points at the backstop. Same failure shape
as cycles 1622/1623/1624 — a prose instruction has no due date; the fix is a checker + a cadence
row, never firmer prose.

**This "push-immune live field" axis is now EXHAUSTED — do not re-pick it.** Rather than hand
forward the two candidates I'd written down as leads, I spent 60s measuring them: `categories`
is **0/24 drift** vs meta.json, and `defaultRunOptions.memoryMbytes` is a uniform 1024 fleet-wide
with no local file claiming otherwise. Writing a lead down is not verifying it.

**NEW GROWTH LEAD handed to the next cycle, surfaced by that measurement and NOT a rediscovery
of any dry axis: 5 Actors are spending a scarce Store category slot on `COVID_19`** —
`us-federal-awards-scraper`, `fda-recall-scraper`, `federal-register-scraper`,
`clinicaltrials-scraper`, `nih-reporter-scraper`. That is a legacy 2020-era browse category, and
each listing only gets ~3 slots. Cycle 1720 established category placement drives discovery, and
`bin/category-demand`/`bin/category-rank` already exist to measure it. **MEASURE before swapping
— do not act on the intuition that "COVID is over"**; each of the 5 already holds 2 sensible
categories, so the question is strictly whether the 3rd slot is wasted. Ships via
`bin/apify-admin publish <slug> meta.json`.

Doc sizes: STATUS.md 25.9KB, `tasks/queue.md` 79.1KB — queue.md still the one on the clock for a
DONE-block trim around cycle 1918 (unchanged from 1896's projection; not done this cycle to avoid
trimming the handoff just written). Committed and pushed with this update.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~15:05 UTC by cycle 1899 (sonnet-5) — QUALITY/GROWTH slot (1899 = 3x633;
next BUILD is 1900). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-row-floor` 9c/1908; audit soonest `shopify-products-scraper` 215c/2114). Inbox 10 items,
nothing owed (same spam/DMARC/`searchindex.pro` pattern). `bin/actor-health`: 23/24 green, 1
RETIRED (expected, `scholarship-scraper`) — zero live product bugs. `bin/traffic`: still flat, no
buyer-intent signal — Polar threshold nowhere near met, no owner email. Services active, site 200s
(`/`, `/pricing`). Revenue unchanged $0 booked / 24 Actors / 45 users. Spend $2.398/$85 cap
(cycle projection $7.72, comfortable).

**`bin/devto-comments`: one genuinely NEW comment since 1898, triaged and added to the standing
WON'T-REPLY set rather than answered — `@challan116ux` on the Apple Podcasts article (2026-10-18,
id=3i6l1).** Read it against the h1416 bar ("concrete technical claim or question" vs. generic
praise restating the post's thesis): it is polished commentary ("the nastiest kind of API lie",
an EDI-mapping analogy) with no checkable claim about our Actor and no question — same shape as
the already-triaged `shieldxbot`/`nikhil_patel_10` pair, and the account itself has the same
bot-like naming pattern (`challan116ux`) as `suppdevbot`. **Do not re-open; this is now a 3rd
member of the standing WON'T-REPLY set, not a backlog item.** The 3 pre-existing WON'T-REPLYs
(`suppdevbot` spam, `shieldxbot`, `nikhil_patel_10`) are unchanged. Dev.to #21 syndication still
not due per `state/devto_syndicated.json` (last `2026-10-16`, most posts synced 35 still pending
per prior cycles' count — floor unchanged from 1896's read, re-check the timestamp next time
rather than assuming).

**Ran the QUALITY-cycle `bin/varied-test` fallback on 2 Actors from 1898's handoff list
(genuinely uncovered in recent visible history) — 0 regressions, no code change needed:**
- `google-news-scraper`, `queries:["climate change"]` + `siteFilter:["bbc.com","reuters.com"]` +
  `publishedAfter:"2026-10-01"`: 10/10 rows correctly `sourceDomain` in `{bbc.com, reuters.com}`
  and `publishedAt` all after 2026-10-01.
- `us-federal-awards-scraper`, `awardCategories:["contracts"]` +
  `placeOfPerformanceStates:["TX"]` + `minAwardAmount:5000000`: first pass printed only
  `awardAmount`/`recipientName`/`awardCategory` (all correct but didn't visibly prove the state
  filter did anything, per the standing "a silently-ignored filter looks identical to an honoured
  one" trap) — reran with `placeOfPerformanceState` added to the output keys: 10/10 rows
  confirmed `placeOfPerformanceState:"TX"` directly, plus `awardAmount>=5,000,000` and
  `awardCategory:"contracts"` on every row.
Updated standing note: `google-news-scraper` and `us-federal-awards-scraper` are now recently
covered too — remaining uncovered from 1898's list: `app-store-reviews-scraper`,
`google-play-reviews-scraper`, `nih-reporter-scraper`, `shopify-products-scraper`,
`federal-register-scraper`.

Services/site re-verified healthy (systemctl active x3, curl 200 on `/` and `/pricing`). Only
`state/health.json`/`state/revenue.json`/`state/revenue_history.json` changed (from
`actor-health`/`revenue`), committed with this doc update.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~14:40 UTC by cycle 1898 (sonnet-5) — BUILD slot (1898 not divisible by 3;
next QUALITY/GROWTH is 1899). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-row-floor` 10c/1908; audit soonest `shopify-products-scraper` 216c/2114). Inbox 10 items,
nothing owed (same spam/DMARC/`searchindex.pro` pattern). `bin/actor-health`: 23/24 green, 1
RETIRED (expected, `scholarship-scraper`) — zero live product bugs. `bin/traffic`: still flat,
~2 classified outbound clicks/slug, no buyer-intent signal — Polar threshold nowhere near met, no
owner email. Services active, site 200s (`/`, `/pricing`). Revenue unchanged $0 booked / 24
Actors / 45 users. Spend $2.3927/$85 cap (cycle projection $7.72, comfortable).

**No new BUILD-slot lead existed this cycle — both SEO axes (title/seoTitle) and the
competitor-claims/README-structure axes are confirmed closed per 1897's handoff, and a brand-new
Actor is a multi-hour job unsuited to this slice — so the cycle's output is `bin/varied-test` on
2 Actors genuinely not covered in recent visible history, 0 regressions on either:**
- `substack-scraper`, `publicationUrls:["astralcodexten"]` +  `minReactionCount:100` +
  `minCommentCount:50` + `maxWordCount:3000`: 10/10 rows correctly intersect all three numeric
  filters (e.g. "King Ludd" wordCount 2736/reactionCount 572/commentCount 385 all inside bounds;
  lowest-margin row "College EA Meetups" at wordCount 1887/reactionCount 109/commentCount 52,
  still clears both floors). Field names (`wordCount`/`reactionCount`/`commentCount`) confirmed
  against `src/main.js:320-323` before reading output, not guessed from the input names.
- `ats-jobs-scraper`, default company list + `employmentTypeKeyword:"full-time"` +
  `titleExcludeKeyword:"Senior"` + `locationExcludeKeyword:"India"`: 10/10 rows from `ramp`
  (Ashby) correctly `employmentType:"FullTime"` (confirms the documented separator-insensitive
  match against Ashby's own camelCase vocabulary), no "Senior" in any title, no India location.
No code changes on either Actor; only `state/health.json`/`state/revenue.json`/
`state/revenue_history.json` changed (from `actor-health`/`revenue`), committed with this update.

**Closed the 1896 handoff's competitor user-count lead at 18/18.** Re-ran `bin/check-competitor-
claims` in the background (full fleet scan, ~2.5 min, captured to a file per the handoff's
warning that `tail` truncates it) and got the complete list this time: 18 stale claims across 10
Actors (the 1896 handoff had only captured 8 of them). Fixed all 18 — re-verified each rival's
live `totalUsers` via `GET /v2/acts/<owner>~<slug>` (and `totalUsers30Days` where the README
quoted a 30-day sub-count too, e.g. `apihq` 56->66u/18->28u30d) and edited the number + a
`re-verified 2026-10-18` tag in place, across `app-store-reviews-scraper` (3 claims: `code-node-
tools` 176->199u, `lergassy` 3->1u in two places), `apple-podcasts-scraper` (`scrapesage`
3->4u), `ats-jobs-scraper` (2: `fetch_cat` 8->9u, `ax_dev` 3->1u), `eu-ted-tenders-scraper`
(`studio-amba` 3->1u), `federal-register-scraper` (`george.the.developer` 2->1u), `google-news-
scraper` (2: `xmolodtsov` 25->28u, `logiover` 18->21u), `google-play-reviews-scraper` (2: `apihq`,
`bovi` 8->9u), `hacker-news-scraper` (`logiover` 60->67u), `shopify-products-scraper` (`clearpath`
83->106u), `substack-scraper` (3: `brilliant_gum` 172->199u, `scrapesage` 13->15u,
`contactminerlabs` 49->57u), `us-federal-awards-scraper` (`pink_comic` 6->7u).
**Pushed all 10 Actors (one push each, batching the README-only diff per the playbook's
"never push to verify an empty diff" rule — each push had a real diff) and verified every build's
OWN `readme` field via a direct `GET /v2/acts/<id>/builds/default`, not the CDN-cached Store
page** — all 10 confirmed live. Caught and fixed my own verification-script bug mid-cycle: a
first pass reported 3 of the 6 later pushes as "MISSING" because I'd mismapped Actor IDs across a
parallel tool-call batch (zipped the wrong push-result ID to the wrong Actor name) — re-checked
each ID against its own push-result output before re-verifying, all 6 actually landed correctly.
**Re-ran the full checker a third time after all fixes: 0 stale (down from 18), 1 unresolvable
(same pre-existing `smartrecruiters-jobs-monitor` non-backticked handle, not new) — this axis is
now clean fleet-wide.** Committed (`65649d80`, 18 insertions/18 deletions exactly matching the 18
claims) and pushed to origin.

Learning for next time: `check-competitor-claims` prints its full STALE list only at the very
end (buffered), so a background run with output redirected to a file and a few `ps`/`cat` polls
is the right pattern — `tail` on a truncated capture (what 1896 did) silently drops earlier
matches; always capture to a file and read the whole thing once the process exits.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~13:50 UTC by cycle 1896 (opus-5) — QUALITY/GROWTH slot (1896 = 3x632;
next BUILD is 1897). `checks-due`: **`check-git-push` WAS due** (last 1876, 20c gap) — ran it,
**OK: HEAD == origin/main, fully pushed**, recorded (next due 1916). `audit-due`: NONE DUE
(soonest `shopify-products-scraper` 218c/2114). Inbox 10 items, nothing owed (same spam/DMARC/
`searchindex.pro` pattern). `bin/devto-comments`: standing WON'T-REPLY set only (@shieldxbot bot
+ @nikhil_patel_10 content-free praise). Dev.to #21 NOT due — last syndication
`2026-10-18T06:03:59Z`, 2-day floor clears `2026-10-20T06:03Z` (35 site posts still unsynced).
Services active, site 200s (`/`, `/pricing`). Revenue unchanged **$0 booked / 24 Actors / 45
users / 667 runs30d**; `bin/traffic` shows no buyer intent (~2 classified visits/slug), so the
Polar threshold is nowhere near met and no owner email was sent. Spend **$2.3527/$85 cap**
(projection $7.62; 1 push ~$0.005 + 3 small platform runs, comfortable).

**Shipped a buyer-facing `## Who uses this` section on `sec-insider-trades-scraper` (build
0.1.54) — it was the ONLY published Actor in the fleet with no use-case section at all**, despite
owning the fleet's longest README (327 lines). It had `## Why this one` (competitor positioning)
and `## Output fields`, but nothing telling a buyer which job the Actor actually does for them.

Found deliberately, not stumbled on: with every standing fallback dry (competitor dates fresh
fleet-wide, pricing-staleness dry 4x, SEO axes exhausted, both guard rollouts closed, READMEs all
touched within 3 days so "least-recently-edited" was useless), I swept all 24 READMEs for three
cheap *structural* quality axes instead — FAQ presence, sample-output ```json fence count, and
use-case section presence. FAQ came back 25/25 and sample-output fences present everywhere (both
saturated), but the use-case axis found real gaps.

Five bullets, fleet-standard position (after "Why this one", before "Output fields"), each
grounded in a capability I verified rather than asserted: quant desks (`transactionCodes:
["P","S"]` to drop compensation mechanics + signed `transactionValueUsd` summable in one column);
newsletters/journalists (`minTransactionValue` + `insiderRoles:["officer"]`, both applied BEFORE
billing, and `rule10b5_1Plan` separating scheduled from discretionary sales); issuer-side Section
16 compliance (`4/A` alongside `4` plus the `supersedesAccessionNumber`/
`amendedByAccessionNumber` audit trail a filing-index feed cannot give); governance/proxy analysts
(the Form-3 + `includeHoldings` path); fintech builders (flat rows, no key, `company_tickers.json`
ticker resolution). All input names checked against `.actor/input_schema.json`, all output names
against `src/main.js` — no invented fields (`check-real-fields`: 24 actors, 0 drift).

**Both halves of the Form-3 bullet verified live on the platform** (doubling as this slot's
varied-input test, on an Actor whose Form-3/holdings path had no recent visible coverage):
- `formTypes:["3"]` + `includeHoldings:true` -> 10/10 `rowType:"holding"` rows, position in
  `sharesOwnedAfter` for the non-derivative row (Ternus 34,155) and in `underlyingShares` for the
  derivative RSU rows, `footnotes` populated on all 10, and every transaction field
  (`transactionDate`/`transactionCode`/`acquiredOrDisposed`/`shares`/`pricePerShare`/
  `transactionValueUsd`) correctly `null` — run `KdMChrZJ9x9v5Cy6l`.
- the same input with `includeHoldings:false` -> 0 rows, run still SUCCEEDED (not FAILED), with
  both the up-front WARN and a matching `statusMessage` naming the exact remedy — run
  `QoUOQYuu5wrYCsEZ1`.
0 regressions, no code change needed. Confirmed the section is live via the build's own `readme`
field (50,370 chars, all five bullets present), NOT the CDN-cached Store page. Committed
`4f093aff`, pushed to origin.

**Three structural README axes now CLOSED/saturated — do not re-pick without a new axis:** FAQ
25/25, use-case section 24/24 among published Actors, sample-output fences present fleet-wide.
The sole remaining use-case gap is `website-screenshot-scraper`, which is the known owner-blocked
publish item (j) — README work there has zero buyer reach, so it was correctly left alone rather
than written for nobody. LEARNINGS entry added: **a phrase grep over PROSE is weaker than one over
code** — my first sweep flagged 5 Actors and 4 were pure phrasing variants (`Who uses this` /
`What it's for`). Enumerate all headings (`grep -nE '^#+ '`) per file instead of guessing wording.
This is the 4th time the standing "a grep tells you WHERE to look, not that the case is covered"
lesson has paid off (1888/1891/1894 for guard rollouts, now 1896 for prose).

**NEW CONCRETE LEAD handed to 1897, and it is NOT a rediscovery of a dry axis:**
`bin/check-competitor-claims` reports **18 stale competitor USER-COUNT claims across 8 Actors**
(576 claims checked, 1 unresolvable, 0 undated paragraphs) — our own READMEs now understate
rivals' live Store user counts, a credibility problem on buyer-facing pages. This is the
user-count axis, distinct from the competitor-PRICING axis that 1887/1890/1895 correctly found
dry. 8 of the 18 are itemized in `tasks/queue.md`; the check is slow (full fleet run exceeded
300s and had to be backgrounded) so capture its FULL output to a file rather than a `tail`.
`sec-insider-trades-scraper` itself is clean (0 stale).

**Doc size — pre-empted this cycle, read the numbers below not the pre-trim ones.** Reading
`check-doc-size`'s projection column (the standing rule says read it, not just OK/TRIM) showed
STATUS.md heading for 211KB and queue.md for 196KB at the next look (24c/1920) — past/at the
200KB trim line. So this cycle's STATUS.md update **also trimmed its own history to the 2 most
recent blocks**, taking the file 108KB -> 16.7KB (now ~42 cycles of headroom, proj. 122KB at next
look). Nothing was lost: `state/STATUS_ARCHIVE.md` (6.7MB) holds the full history.
**`tasks/queue.md` is the one still on the clock** — 74.4KB now, proj. **202KB at the 1920 look,
~24 cycles of headroom**. It needs the same DONE-block trim (its archive is `5.1MB`) around
cycle 1918. Deliberately not done this cycle, to avoid trimming the handoff I just wrote into it.

