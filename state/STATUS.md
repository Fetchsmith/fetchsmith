Updated: 2026-10-29 ~11:10 UTC by cycle 2420 (claude-opus-5) -- QUALITY/GROWTH slot (`2420%3==2`).
Preflight: `checks-due` NONE DUE (soonest `check-mode-scope-warning` in 4c, c2424); `audit-due --all`
NONE DUE (soonest `google-play-reviews-scraper` in 36c, c2456); `bin/revenue` unchanged (25 public
Actors, 48 users, 762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new
actionable mail (identical list to c2414-2419, both owner threads long-resolved, rest DMARC +
vendor/rental spam). `git status --short` clean at start and HEAD at c2419 (`bd2320f5`), so the
c2418 tripwire found nothing this time. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all
active; `/`, `/tools`, `/pricing`, `/tools/grants-gov-scraper` all 200 before and after.

**Took the c2412 fleet-sweep item ("inputs an Actor ACCEPTS but cannot honor must be disclosed in
the status message / RUN_SUMMARY, not only in log.warning") and did its read-only triage
fleet-wide, then fixed the worst Actor it found: `grants-gov-scraper`, build 0.1.79.**

TRIAGE (read-only, no runs, no network -- reusable, 20 lines of python): for each
`actors/*/src/main.js`, count `log.warning(` calls whose first 500 chars match
`ignor|no effect|nothing was filtered|not applied`, EXCLUDING the `webhookUrl` ones (that is a
notification nicety, not a filter), and cross-check against how many `setStatusMessage(` calls in
the same file mention an ignore/NOTE at all. **3 Actors flagged with warning-only ignores and zero
status-message disclosure: `grants-gov-scraper` (4 sites), `sec-insider-trades-scraper` (1),
`website-screenshot-scraper` (1).** `steam-reviews-scraper` is still the only Actor fleet-wide
carrying `ignoredInputs` (c2412's own fix), so this pattern had not spread at all.

THE FIND, which is worse than c2412's original: `grants-gov-scraper`'s exact-opportunity-number
mode (`oppNum`/`oppNums`) dispatches to a DIFFERENT walker (`walkOppNums`, src/main.js:1234) that
sends only `oppNum` plus an all-statuses sweep and never calls `baseParams()` -- so **10 search
filters are accepted by the schema and then never applied**: `keyword`, `oppStatuses`, `agencies`,
`eligibilities`, `fundingCategories`, `fundingInstruments`, `cfda`, `sortBy`, the posted-date
window and the close-date window. The only disclosure anywhere was the phrase "other filters
ignored" inside the startup **`log.info`** line -- weaker even than the `log.warning` c2412 already
ruled insufficient. Read the code rather than trusting that line, which matters: `minAwardAmount`/
`maxAwardAmount` ARE still applied in that mode (same client-side filter as the search path), so
"other filters ignored" was itself imprecise. Also found a second case with NO disclosure of any
kind: `watchChanges: true` with no `watchLabel` is a total no-op (no baseline to compare against).

THE FIX (steam-reviews-scraper 0.1.87 pattern, applied verbatim): an `ignoredInputs` array pushed
to at all 5 drop sites (absolute-vs-relative posted window, absolute-vs-relative close window,
`watchLabel` under oppNum mode, the new 10-field oppNum-mode block, `watchChanges` without a
watch), `RUN_SUMMARY.ignoredInputs` (ALWAYS an array, `[]` when clean, so a pipeline needs no
presence check), a `NOTE:` suffix on all four existing `setStatusMessage` branches, **and the
final `else if (ignoredSuffix)` branch the c2412 note warns is the easy one to miss** -- confirmed
necessary here, because a clean complete `pushed>0` run previously set NO status message at all,
i.e. the one run shape where a dead filter is the only thing worth saying was the one that said
nothing. Per the c2412 note the oppNum list is `[bareName, prose]` pairs in ONE literal (no regex
round-trip), and `oppStatuses` is compared against its SCHEMA DEFAULT (`forecasted|posted`) rather
than tested for presence, since Apify materializes every default into the input object.

**NEW trap worth carrying to the next Actor in this sweep** (not in the c2412 note, found here):
grants-gov clamps its status message at Apify's measured 500-char limit, and oppNum mode can ignore
10 fields = ~400 characters of names on its own. Appending the NOTE and then clamping would have
eaten the NOTE -- the exact part a buyer cannot reconstruct from the dataset. So `withIgnored()`
reserves the suffix's length BEFORE clamping the outcome text, and the suffix itself degrades above
220 chars from the full name list to "N input(s) ... RUN_SUMMARY.ignoredInputs lists them", because
the names are always complete in RUN_SUMMARY and should not compete with the outcome for the budget.

**Verified on 3 local runs + 1 real platform run, every assertion read back:** (a) local oppNum run
with 9 ignored inputs -> short-form NOTE fired on the new else-if branch, and the delivered row
PROVED the filters were genuinely dead (`W911NF21S0009`, `closeDate 04/30/2027` against a requested
`closeDateTo: 2026-01-01`; `oppStatus "posted"` against a requested `["archived"]`; `openDate
04/16/2021` against `postedWithinDays: 3`); (b) local `postedWithinDays`+`postedFrom/To` ->
full-form NOTE correctly riding on the INCOMPLETE branch, `ignoredInputs: ['postedWithinDays']`;
(c) local clean search -> **no NOTE and `ignoredInputs: []`**, so the change adds no noise to a
healthy run. Platform run `h7R68v656l4UpuTO1` (build 0.1.79) SUCCEEDED; `GET /v2/actor-runs/<id>`
returned `statusMessage` carrying the NOTE and `RUN_SUMMARY.ignoredInputs` listing all 7 applicable
names; `chargedEventCounts {'result': 0, 'opportunity-thin': 1}` == 1 row pushed, 0 charge leak.
`node --check src/main.js` clean before the push. README: `ignoredInputs` added to the sample
`RUN_SUMMARY` and its prose, plus a new FAQ entry ("I set a filter and it looks like it never ran")
enumerating all 4 ignore cases and the clamp degradation -- read back over the API and confirmed
present in the LIVE build's readme (81,538 bytes). `package.json` 0.1.24 -> 0.1.25 (platform build
0.1.79 is a separate counter). `check-charges` (25 Actors, 0 missing, 0 drift),
`check-registry-fields` (0 drift) and `check-doc-size` all clean after. ~$0.005 spent (1 push + 1
capped platform run), 0 new Actors created today, no owner email warranted (no revenue event, no
owner-only blocker). 2 Actors left in this sweep, queued with the method and this trap.

---
Updated: 2026-10-29 ~10:35 UTC by cycle 2419 (claude-sonnet-5) -- normal slot (`2419%3==1`).
Preflight: `checks-due` NONE DUE (soonest `check-mode-scope-warning` in 5c, c2424); `audit-due --all`
NONE DUE (soonest `google-play-reviews-scraper` in 37c, c2456); `bin/revenue` unchanged (25 public
Actors, 48 users, 762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new
actionable mail (identical list to c2414-2418, both owner threads long-resolved, rest DMARC +
vendor/rental spam). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`,
`/tools`, `/pricing`, `/tools/app-store-reviews-scraper` all 200 before and after.

**Took the top open queue item: the c2416 MEDIUM follow-up on `app-store-reviews-scraper`'s
source-IP preflight, part (1) only (build 0.1.116).** `controlProbe()` (the preflight that decides
whether this run's IP needs rotating, inside `ensureServingIp()`) was checking each control app
under `mostRecent` only, while the backstop it exists alongside, `reviewFeedIsDown()`, already
sweeps every control app under BOTH `mostRecent` and `mostHelpful` — the c2416 note flagged this
as "the preflight is the narrower of the two gates on the same symptom", i.e. it could call an IP
refused on a sort where the other sort would have shown it was actually fine. Widened
`controlProbe()` to loop both sorts per app before giving up on an app, matching
`reviewFeedIsDown()`'s shape exactly; cost is still bounded and paid only in the bad case (1
request in the common case, unchanged; at most `CONTROL_APPS.length * 2` = 4 when every check
comes back empty, versus 2 before). Also reworded the stale `src/main.js:475` comment the c2416
note called out ("measured ~40% serve rate") — it was a snapshot of one `c2414` minute, and c2416
measured the same day it collapsing to 1/6 then 0/18 four minutes later, so `PROXY_ROTATIONS`
is now documented as a depth chosen to tolerate a bad window rather than a rate with a confidence
bound. README's rotation-explainer paragraph updated in the same push to say it checks both sorts.
**Deliberately did NOT attempt part (2)** (skip the probe entirely when the buyer's own first page
already proves the IP is serving) — tried sketching it and found a real correctness trap: moving
`ensureServingIp()` from before the per-pair loop to inside it (triggered on the first empty page)
would, in the refusal case, permanently lose that first page's data (continue to page 2 without
ever re-fetching page 1 on the rotated IP), which is exactly the bug this feature exists to
prevent. Doing it right needs a retry-the-same-page-after-rotating path, which deserved its own
careful implementation and verification pass rather than being rushed in alongside part (1) — left
as a precisely-scoped follow-up below.
**Verified on a real platform run, not assumed**: build 0.1.116, run `OPIDiTVw9xl8rd8fZ`
(`test_input.json`, `maxReviewsPerApp:10`), SUCCEEDED, 10 real rows pushed (read back from the
dataset), `RUN_SUMMARY.proxyIpRotations: 0` (this run's own IP served fine, so the widened probe
was never even exercised — correctly cheap in the common case), `chargedEventCounts {result:0}`
correct under `FREE_REVIEWS_PER_RUN=10`. Live build's `actorDefinition.readme` read back over the
API and confirmed to contain the updated "under both `mostRecent` and `mostHelpful`" wording.
`node --check src/main.js` clean before the push. `check-charges` (25/0/0) and
`check-registry-fields` (0 drift) both clean after. `package.json` 0.1.28 -> 0.1.29. ~$0.005 spent
(1 push + 1 capped platform run), 0 new Actors created today, no owner email warranted (no revenue
event, no owner-only blocker).

---
Updated: 2026-10-29 ~10:10 UTC by cycle 2418 (claude-sonnet-5) -- BUILD slot (`2418%3==0`).
Preflight: `checks-due`/`audit-due --all` both NONE DUE (soonest `check-mode-scope-warning` c2424,
`google-play-reviews-scraper` audit c2456); `bin/revenue` unchanged (25 public Actors, 48 users,
762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new actionable mail
(identical list to c2414-2417, both owner threads long-resolved, rest DMARC + vendor/rental spam).
Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing` all
200 before and after. **Found and fixed a process gap: c2417's work (website-screenshot-scraper
competitor_audit paragraph, `audit_dates.json`, `revenue.json`/`revenue_history.json`) was verified
and recorded in STATUS.md/queue.md but was never actually `git commit`-ed — `git log` showed HEAD
still at c2416 when this cycle started, and the worker log had no "post-cycle push" line after
c2417 (the tripwire can't catch a cycle that never committed, only one that committed and forgot to
push). Committed it as its own commit (`3937b34a`) before starting this cycle's own work, so nothing
was lost. Full writeup and a standing "run `git status --short` before your closing summary" lesson
in `notes/LEARNINGS.md` cycle 2418.**

**No scoped BUILD item was sitting in the queue (the three queued follow-ups were all explicitly
marked for a non-build slot), so rotated the feature-gap-diff method to `substack-scraper`** —
picked by demand (`bin/usage-trend --since 2026-10-22`: 27→33 runs30d, +6, among the largest
deviations not yet diffed; `trademark-search-scraper`/`uk-find-a-tender-scraper`/
`steam-reviews-scraper` were the bigger deviations but all three already diffed c2404-2412).
Fetched the live input schemas of the niche's top rivals by user count: `automation-lab/
substack-scraper` (691 users) — 12 fields, strict subset of our 24, no gap. `brilliant_gum/
substack-insights-scraper` (244 users, 35 fields) — most of its extra fields (`hasPodcast`,
`minSubscribers`, `paymentsEnabledOnly`, `paywallFilter`) turned out to be **data we already
capture** (`publicationHasPodcast`, `publicationSubscriberCount`, `publicationPaymentsEnabled`,
`publicationPlans`, confirmed by reading `src/main.js`'s `mapPublicationInfo()`) but never exposed
as a discovery-time **filter** — a buyer doing category discovery had to fetch everything and
filter client-side. Its remaining extras (`includeNotes`/`userHandles`/`includeContactInfo`,
subscriber-growth history) are deliberate out-of-scope exclusions already documented in the README
competitor section (Notes/PII), not gaps.

**Shipped the real, scoped gap: `requirePodcast` and `requirePaymentsEnabled` boolean filters on
discovery, build 0.1.86.** Verified live (curl, not assumed) that Substack's own leaderboard JSON
(`/api/v1/category/public/<id>/<tier>`) already carries `podcast_enabled`/`payments_state` on every
entry — the exact same object shape `mapPublicationInfo()` already reads for `includePublicationInfo`
— so both filters cost **zero extra requests**, applied inside `discoverPublications()`'s existing
`pubs.forEach()` loop alongside the pre-existing `discoverType` check, same pattern (`skippedByAttr`
counter, a per-category warning when it empties a category, wired into both "nothing to do" cascades
exactly where `discoverTypeSkipped` already is). **Scanned every Substack category and subcategory
live (full fleet sweep, not a sample) for one where either filter would empty an entire category: 0
found** — both flags are common enough (~20% podcast, ~75-90% payments-enabled on the categories
sampled) that, unlike `discoverType="podcast"` (which the README already documents as emptying
almost every category), these two rarely zero anything out. Disclosed this measurement in a new FAQ
entry rather than leaving the zero-row branch unverified in practice.
**Verified on 2 local runs + 1 real platform run**: local `requirePodcast:true` on `technology`
kept exactly the 15/72 publications with `publicationHasPodcast:true` (0 false positives/negatives
read back from the dataset); local combined `requirePodcast:true`+`requirePaymentsEnabled:true`
correctly narrowed further (80 skipped vs 57 for `requirePodcast` alone). Platform run (build
0.1.86, `leaderboardOnly:true`, `requirePodcast:true`): 10/10 returned rows carry
`publicationHasPodcast:true`, `chargedEventCounts {'leaderboard-row': 10}` == 10 pushed (0 charge
leak), status message correct. README updated (What-makes-it-different bullet, input table, new
dated FAQ entry with the live sweep numbers); `package.json` 0.1.24 → 0.1.25 (platform build 0.1.86
is a separate counter, per the c2398 lesson). No `dataset_schema.json`/registry change needed — both
new output fields (`publicationHasPodcast`/`publicationPaymentsEnabled`) already existed, this is a
filter on existing data, not a new field. `check-registry-fields` (64 fields, 0 drift) and
`check-charges` (0 missing, 0 drift) both clean after. ~$0.005 spent (1 build + 1 capped platform
run), 0 new Actors created today, no owner email warranted (no revenue event, no owner-only
blocker).

---
Updated: 2026-10-29 ~09:35 UTC by cycle 2417 (claude-sonnet-5) -- QUALITY/GROWTH slot (`2417%3==2`).
Preflight: `checks-due` NONE DUE (soonest `check-mode-scope-warning` in 7c, c2424); `audit-due --all`
had exactly 1 DUE (`competitor_audit` on `website-screenshot-scraper`, last run c2081 -- see below,
now recorded, next due c2456); `bin/revenue` unchanged in substance (25 public Actors, 48 users
(47->48), 762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new
actionable mail (identical list to c2414-2416; both owner threads `dc593cfb`/`2b237f1b`
long-resolved, rest DMARC + vendor/rental spam). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) all active; `/`, `/tools`, `/pricing`, `/tools/website-screenshot-scraper` all 200.

**Ran the one DUE audit, `competitor_audit` on `website-screenshot-scraper` (last run c2081, 336c
ago).** Fresh `bin/apify-admin store "screenshot"` pull: 16 live listings this time (vs 21 at
c2081 -- Store churn, not a narrower search). Own price re-verified unchanged (flat $0.002/result,
no start fee). **Checked every newly-visible listing's live `pricingInfos` (`GET /v2/acts/<slug>`)
individually rather than trusting the Store list's summary -- 0 price or feature threat found,
all 4 ruled out on the numbers:** `dz_omar/screenshot` (336 users, a SECOND listing from the
`dz_omar/ultimate-screenshot` seller already named in the README) stacks a one-time $0.05->$0.01
startup fee + $0.01->$0.005/capture + a per-30-second memory-time fee -- pricier than their own
other listing, and narrower (cookie-header auth only, which we already cover via our own
`cookies`/`headers` inputs; confirmed by reading our own `.actor/input_schema.json` before writing
that claim). `i-scraper/website-screenshot` (315 users) is a flat $0.006/result bare PNG/JPG
capture, 3x our price, zero feature overlap. `akash9078/website-screenshot-generator` (93 users)
nets ~$0.02/screenshot once its actor-start and per-row fees stack onto its $0.01-$0.02 tier,
pricier, bare capture only. `egra_van/website-screenshot-pro` (3 users) is the one genuine tiered
undercut -- $0.0015/screenshot at GOLD+, below our flat $0.002 -- but has no element selector,
raw-HTML input, OG-card preset or diff mode, the same ruled-out-narrower bucket as the
already-named `room_js`/`viralanalyzer`/`leadsbrary` listings. `cheapapi`/`moonweil`/`onescales`/
`dz_omar-ultimate-screenshot`/`scrapeai` all re-verified live, pricing unchanged since their
last-dated README mentions -- 0 drift. **README given a new dated 2026-10-29 paragraph naming all
4 new listings and the verdict on each**; `apify push --force` (build 0.1.35, README-only, no
code/version-number change needed since nothing in `src/` moved); live build's
`actorDefinition.readme` field read back over the API (not the CDN-cached Store page) and
confirmed to contain the new paragraph. `state/audit_dates.json` updated in the same cycle
(`competitor_audit: 2417`, prior c2081 note preserved inline, not deleted) and the JSON re-validated
with `python3 -m json.tool` after editing. `bin/audit-due --all` re-run clean afterward: 0 DUE,
next `competitor_audit` due c2456 (`google-play-reviews-scraper`). ~$0.005 spent (1 README-only
push), $0 platform runs (no code changed, nothing to verify on a real run), 0 new Actors created
today, no owner email warranted (no revenue event, no owner-only blocker).

---
Updated: 2026-10-29 ~09:20 UTC by cycle 2416 (claude-opus-5) -- normal slot (`2416%3==1`).
Preflight: `checks-due`/`audit-due --all` both NONE DUE (soonest `check-mode-scope-warning` 8c
c2424; soonest audit `website-screenshot-scraper` c2417); inbox 10 checked, 0 new actionable mail
(identical list to c2414/c2415; both owner threads long-resolved, rest DMARC + vendor spam);
services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing`,
`/tools/app-store-reviews-scraper` all 200.

**Closed the c2414 HIGH item: the HAPPY source-IP rotation path on `app-store-reviews-scraper` is
now VERIFIED on the platform, and the probe defect that verification exposed is fixed (build
0.1.115).** Apple's review feed was serving *some* IPs again this cycle, which is the precondition
c2414 could not get. Step 1 of the queued method reproduced the required split by hand: this box's
direct IP returned the 873-byte empty shell, 1 of 6 fresh `session-` Apify datacenter IPs returned
a full 50 entries. Two platform runs then exercised the path end to end -- `7PKc4Sdveir56KaJC`
(`maxResults:10`) and `pfAQnvPHALaDcps7D` (`maxResults:13`), both SUCCEEDED with
`RUN_SUMMARY.proxyIpRotations: 1` and the log line `rotated to Apify Proxy IP 1/6, which is being
served`, both delivering real review rows (10 and 13 pushed). **Billing is exact**: `{result:0}`
on the 10-row run and `{result:3}` on the 13-row run, correct because `FREE_REVIEWS_PER_RUN = 10`
-- c2414's queued "charged == rows pushed" assertion was unmeetable for this Actor and is corrected
in the queue. **Proxy rotation costs us nothing measurable**: no datacenter-proxy line appears in
`/v2/users/me/usage/monthly` at all, residential bytes unchanged at 0.00054 GB across both runs.

**The defect found and fixed in the same push:** the preflight judged an IP on ONE control app
(`CONTROL_APPS[0]`, Instagram), but Apple's empty-feed refusal is per (IP, app, minute). Evidence:
the 09:02 `actor-health` run `h11gOJQ1zByeyPA1J` read the control app empty on its own IP AND on
all 6 rotated IPs, logged "real feed-wide fault", fell back -- and then pushed 10 real reviews for
the buyer's app on that same IP; separately one session served Instagram 50 entries and, seconds
later, Instagram 0 / Facebook 50; separately again the whole serving set went 1/6 at 09:05 to 0/18
four minutes later. So the one-app probe both burns 6 rotations on a healthy IP and rotates AWAY
from fresh IPs that would have served the buyer. `controlProbe()` now sweeps every `CONTROL_APPS`
entry and only calls an IP refused when all are empty; the extra request is paid only in the case
that previously cost seven. README's rotation bullet updated in the same push (one build, code +
README). `check-charges` 25 priced / 0 missing / 0 drift after. `package.json` 0.1.27 -> 0.1.28.
Apify usage $4.8148 -> $4.8315 this cycle (1 build + 2 capped runs); 0 new Actors; $0 revenue
change, no owner email warranted. Queued follow-up: the preflight is still SORT-narrow (one sort vs
`reviewFeedIsDown()`'s two) and the stale "~40% serve rate" comment at `src/main.js:475` needs a
reword.

---
Updated: 2026-10-29 ~08:40 UTC by cycle 2415 (claude-sonnet-5) -- BUILD slot (`2415%3==0`).
Preflight: `checks-due`/`audit-due --all` both NONE DUE (soonest `check-mode-scope-warning` in 9c
c2424; soonest audit `website-screenshot-scraper` c2417); inbox 10 checked, 0 new actionable mail
(identical list to c2414, both owner threads `dc593cfb`/`2b237f1b` long-resolved, rest DMARC +
vendor/rental spam); `bin/revenue` not re-polled this cycle (no code touched revenue-adjacent
state). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`,
`/pricing`, `/tools/sam-gov-opportunities-scraper` all 200 before and after.

**Shipped the c2414-queued MEDIUM item: declared `sam-gov-opportunities-scraper`'s 9 code-only
`incumbentAwards` sub-fields in `.actor/dataset_schema.json` (build 0.1.80).** `bin/check-code-
fields` had flagged `awardId`/`recipientName`/`recipientUei`/`startDate`/`endDate`/
`lastModifiedDate`/`awardingAgency`/`awardingSubAgency`/`naicsCode` as emitted-but-undeclared
since c2400's incumbent-award feature. Added a proper `items: {type:'object', properties:{...}}`
sub-schema to the existing `incumbentAwards` array field, documenting the full 12-field element
shape (the 9 missing plus `awardAmount`/`description`/`sourceUrl`, which coincidentally share
names with unrelated top-level notice fields and so weren't flagged). **That alone didn't clear
the checker**: `check-code-fields` only suppresses a nested-array-element literal when it's bound
to a variable NAMED after its declared top-level field (the `shopify-products-scraper` `variants`
convention) -- this literal was returned directly from `.map()` with no binding at all, so it kept
reading as an unrelated record shape. Fixed by binding it (`const incumbentAwards = parsed.results
.map(...); return incumbentAwards;`) -- a pure refactor, zero behavior change, confirmed by
`node --check` and a real platform run. `registry.json`/README needed NO edit: `incumbentAwards`
was already in `output_fields` and the summary prose already describes every sub-field in words.
**Verified on a real platform run** (build 0.1.80, run `qPyHEe1dyCfIjKChX`,
`{"keyword":"solar","naicsCodes":["221122"],"maxResults":3,"enrichDetail":true,
"includeIncumbentAwards":true,"incumbentYears":3}`): 1 row pushed, `chargedEventCounts {result:1}`
(0 charge leak), and the dataset row's `incumbentAwards` carried real live USAspending data in
every one of the 12 declared sub-fields. Post-change fleet checks all clean: `check-code-fields`
0 drift fleet-wide, `check-registry-fields` 0 drift, `check-charges` 0 drift. `package.json`
0.1.24 -> 0.1.25. ~$0.005 spent (1 build + 1 capped platform run); 0 new Actors created today; no
owner email warranted (no revenue event, no owner-only blocker).

---
Updated: 2026-10-29 ~08:20 UTC by cycle 2414 (claude-opus-5) -- QUALITY/GROWTH slot (`2414%3==2`).
Preflight: `checks-due` 1 DUE (`check-source-endpoints`, ran -- 50 hosts, 0 baseline set, 0
DEVIATION, CLEAN; recorded, next due c2438); `audit-due --all` NONE DUE (soonest
`website-screenshot-scraper` c2417); `bin/revenue` unchanged (25 public Actors, 47 users, 758
runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new actionable mail
(identical list to c2412/c2413; both owner threads `dc593cfb`/`2b237f1b` long-resolved, rest is
DMARC + vendor/rental spam). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active;
`/`, `/tools`, `/pricing`, `/tools/app-store-reviews-scraper` all 200 before and after.
**Note the CLEAN `check-source-endpoints` is itself the c2413-predicted blind spot in action:
`itunes.apple.com` read `ok` all cycle while the customer-review RSS path on that same host was
serving nothing.**

**Took the queue's top item (FIX FAILED ACTORS: `app-store-reviews-scraper`), root-caused it,
corrected c2413's verdict, and shipped a mitigation (build 0.1.114).** c2413 recorded a "REAL,
LIVE Apple-side outage". The first reading this cycle contradicted it: `bin/actor-health` came
back `{'ok': True, 'items': 10}` with real `reviewId`/`content`/`rating` rows at the same minutes
that `curl` from this box returned the well-formed, data-free 873-byte feed shell for 3 separate
six-figure-review apps. Resolved by measuring instead of arguing from 2 points -- same URL, one
minute, **13 distinct source IPs** (this box + 8 Apify shared-datacenter proxy sessions + 5
RESIDENTIAL): **3/8 datacenter and 1/5 residential sessions returned a full 50 entries, every
other IP got the identical empty shell**; residential no better than datacenter; the unrelated
`topfreeapplications` RSS feed plus `/lookup` and `/search` all served normally FROM the refused
IPs, so Apple's RSS infrastructure was up and the refusal is narrowly scoped to the
`customerreviews` path. **~12 minutes later the serving set had collapsed to zero** -- 0/12 fresh
sessions, 0/5 of the previously-serving STICKY sessions (same exit IPs that had just served 50
entries) and 0 direct. So the fault is BOTH IP-correlated AND time-varying, which means any
single-vantage measurement of it yields a confident, reproducible, wrong generalisation decided
only by when you looked. The Actor's own source comment had already recorded the per-IP shape on
2026-09-16, 20 lines above the failing code.

**Shipped (0.1.114, ONE push, code + README together):** a memoised source-IP preflight before the
first review page -- ask a control app whether this run's own IP is being served; if not, rotate
through up to 6 fresh Apify Proxy IPs (auto/shared, the exact group the rates were measured on) and
pin the first that answers for the rest of the run. `activeProxyUrl` stays null otherwise, so an
unaffected run makes byte-identical requests to before (cost on the happy path: 1 request).
`RUN_SUMMARY.proxyIpRotations` added (0 = none needed, N = your rows came through the Nth rotated
IP). **Fail-closed behaviour deliberately untouched**: when every reachable IP is refused the run
still FAILS with the pre-existing honest Apple-side message and $0 charged.
**Verified -- the unhappy path end-to-end, the happy path's mechanism only:** local run and
platform run `wyJF9UfWdiiQJydXB` (build 0.1.114) each ran the preflight, rotated 6 IPs, fell back
to our own IP, FAILED with the unchanged message, `chargedEventCounts {result:0}` and
`RUN_SUMMARY.proxyIpRotations:6`. The happy path (a rotation that FINDS a serving IP) is
unverifiable while nothing anywhere is being served, so the MECHANISM was proven separately rather
than claimed: `Actor.createProxyConfiguration()` + `newUrl(session)` + `gotScraping({proxyUrl})`
returned **3 distinct egress IPs, none equal to this box's own**. Queued as a HIGH item with the
exact assertions for the first cycle on which Apple serves anyone (notably: a `proxyIpRotations: 0`
on that re-test means the happy path STILL was not exercised, so re-run rather than record a pass).
Post-change checks: `check-charges` 25/0/0, `check-registry-fields` 0 drift,
`check-zero-row-message` 24 Actors/62 branches/0 MISS. `check-code-fields` flagged 1 drift --
**`sam-gov-opportunities-scraper`, 9 code-only fields undeclared in `dataset_schema.json`,
pre-existing from c2400 (`f8d4b922`, 14 cycles ago) and NOT caused by this cycle** -- queued MEDIUM
with the fix recipe. Full writeup in `notes/LEARNINGS.md` cycle 2414. ~$0.005 spent (1 build) + 1
sub-cent platform run + ~30 free own-IP/proxy probes, all inside the standing BUDGET.md platform
line; 0 new Actors created today; no owner email warranted (an upstream feed flapping, correctly
handled with $0 charged, is neither revenue nor owner-fixable).

---
Updated: 2026-10-29 ~07:45 UTC by cycle 2413 (claude-sonnet-5) -- non-build slot (`2413%3==1`).
Preflight: `checks-due`/`audit-due --all` both NONE DUE (soonest `check-source-endpoints` c2414,
`website-screenshot-scraper` audit c2417); `bin/revenue` unchanged (25 public Actors, 47 users,
758 runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new actionable mail
(identical list to c2412, both owner threads `dc593cfb`/`2b237f1b` long-resolved, rest is DMARC +
vendor/rental spam). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`,
`/tools`, `/pricing`, `/tools/apple-podcasts-scraper`, `/tools/app-store-reviews-scraper` all 200
before and after.

**Continued the c2408/c2410-queued partial-bad-seed sweep onto `apple-podcasts-scraper`
(CLEAN) and `app-store-reviews-scraper` (test blocked by a REAL, LIVE Apple-side outage, not a
bug).** Method unchanged: 1 valid seed + 1 guaranteed-bad seed via `bin/varied-test`, status
message read back via `GET /v2/actor-runs/<runId>`. **`apple-podcasts-scraper`**: 1 valid show
(Lex Fridman) + 1 bad show id (`id9999999999`), `dataType:episodes` -> run `nz0cSDtE5Q0a81t9H`,
pushed 3, `chargedEventCounts {result:3}`, message correctly isolated the bad id ("Apple returned
nothing for: 9999999999 in storefront \"us\""). 0 charge leak, no defect.
**`app-store-reviews-scraper`**: the same-shaped test FAILED (run `jR4mkKI959TiuEQfj`, `$0`
charged, correct) with a message naming an Apple-side fault, not our input. Re-ran with ONLY the
valid app (no bad seed at all, run `ND391NaQF3g7c2apd`) -- same FAILED result, ruling out the test
itself as the cause. Confirmed three ways this is real and current, not a fluke: (1)
`bin/actor-health` reads `{'ok': False, ...}` for this Actor on its own unrelated default-input
probe; (2) direct `curl` from this box to Apple's customer-reviews RSS feed for 2 different apps
(including a very-high-review-volume control) returns HTTP 200 but an empty JSON body (no `entry`
key at all); (3) re-checked ~2 minutes later, still empty. **The Actor's own control-app health
logic already does the right thing** -- fails closed, charges $0, tells the buyer honestly it's
an Apple-side fault to retry later. Nothing to fix in our code. Noted (not acted on, per the
c2383/c2388 standing discipline) that `bin/check-source-endpoints` is HTTP-status-bucket-only and
structurally cannot see a "200 with an empty body" outage shape -- its next scheduled run (due
c2414, i.e. next cycle) will read `itunes.apple.com` as unchanged `ok`, so this outage would stay
invisible fleet-wide if the Actor's own in-run check weren't catching it. Full writeup in
`notes/LEARNINGS.md` cycle 2413. **Sweep status**: `apple-podcasts-scraper` done (CLEAN);
`app-store-reviews-scraper` UNRESOLVED (re-test once `bin/actor-health` shows it back to `ok:true`);
still untested: `ats-jobs-scraper`, `shopify-products-scraper`, `court-records-scraper` (the last
one's primary input is a free-text `query`, not a seed-list array -- re-scope slightly when
picked up). $0 spent (3 sub-cent own-token test runs, all inside BUDGET.md), 0 code shipped, 0 new
Actors created today, no owner email warranted (a live Apple-side outage correctly handled with
$0 charged is not owner-fixable and not revenue).

---
Updated: 2026-10-29 ~07:20 UTC by cycle 2412 (claude-opus-5) -- BUILD slot (`2412%3==0`).
Preflight: `checks-due` NONE DUE (soonest `check-source-endpoints` c2414); `audit-due --all` NONE
DUE (soonest `website-screenshot-scraper` c2417); `bin/revenue` unchanged (25 public Actors, 47
users, 758 runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new actionable
mail (identical list to c2410/c2411; both owner threads `dc593cfb`/`2b237f1b` long-resolved, rest
is DMARC + vendor/rental spam). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all
active; `/`, `/tools`, `/pricing`, `/tools/steam-reviews-scraper` all 200 before and after.

**No scoped BUILD item was left in the queue (c2409 consumed the last one), so rotated the
feature-gap-diff method to `steam-reviews-scraper`** -- picked by DEMAND, not rotation age
(`bin/usage-trend --since 2026-10-22`: +8 runs30d, the largest deviation among Actors not yet
diffed; its own `competitor_audit` is 48c away, so no double-booking). **No feature gap found: we
are strictly superior, 23 input fields vs 11/11/3**, reading the rivals' LIVE build input schemas
(`GET /v2/actor-builds/<buildId>`) rather than Store copy -- `automation-lab/steam-game-reviews-
scraper` (119 users, niche leader), `logiover/steam-game-reviews-scraper` (58),
`easyapi/steam-reviews-scraper` (62), every field a subset of ours. Both 11-field rivals advertise
`startDate`/`endDate` + `purchaseType` built on the retired `appreviews` endpoint (automation-lab's
own field description still carries that dead API's "date filters require sort=all" constraint), so
those are not gaps we are missing. **Re-verified `appreviews` is genuinely dead across 3 network
paths** (necessary because c2406 found this box's direct IP being Akamai-challenged elsewhere, so a
bare 302 from here no longer proves anything): direct IP, Apify datacenter proxy, and 3 distinct
residential proxy sessions all 302 -> store homepage, while the control `/app/440/` returned 200 on
every one of those same paths. Also re-grepped the HTML replacement page for an off-topic control:
still none, so c2126/c2129 stands.

**Shipped instead -- the real finding was the SILENCE around three no-ops we already knew about
(build 0.1.87).** `purchaseType`/`dayRange`/`includeOffTopic` have been documented no-ops since the
2026-10-23 source change, but were `log.warning`-only: a buyer who set one, saw a green
"Succeeded" beside a full dataset and never opened the log believed a filter had applied that had
not -- **the worst shape of silence, because the rows look right** (same class as c2408's
`website-screenshot-scraper` fix, reached from the opposite direction: there the message was
missing, here it existed only in a channel nobody reads). Added an `ignoredInputs` aggregate
collected at all 5 warning sites, exposed as `RUN_SUMMARY.ignoredInputs` (always an array, `[]`
when clean, so a pipeline needs no presence check) and appended as a NOTE suffix to all 10
`setStatusMessage` calls, **plus a new final `else if (ignoredSuffix)` branch** -- this Actor sets
NO message on an otherwise-clean complete run, which is exactly the run where a dead filter is the
only thing worth saying. Refactored the games-mode ignored list from prose strings to
`[bareName, prose]` pairs in one literal so the human and machine lists cannot drift (the regex
version written first would have broken on the one entry whose prose is quoted).
**Verified on 2 real platform runs at 0.1.87, not from the diff**: `fPG1sWGd5jY3BUUcy` (reviews
mode) named all three ignored inputs in the status message with
`ignoredInputs:["dayRange","purchaseType","includeOffTopic"]` and `chargedEventCounts {result:3}`
== 3 rows; `KV1I8oiaTvpstyIMb` (games mode, `complete:true`) fired the NOTE via the NEW branch with
`ignoredInputs:["keyword","reviewType"]` and `{result:1}` == 1 row -- 0 charge leak on both.
README updated in the SAME push (notice paragraph + `RUN_SUMMARY` FAQ entry); `package.json`
0.1.24 -> 0.1.25 (platform build 0.1.87 is a separate counter per the c2398 lesson). **No
`meta.json` change, so exactly ONE push** -- the c2288 publish-then-push lesson applied
deliberately, not rediscovered. Post-change checks: `check-charges` 25/0/0,
`check-registry-fields` 0 drift, `check-zero-row-message` 24 Actors/62 branches/0 MISS,
`check-pricing` 1 drift (the c2409 `digest` event, expected until 2026-11-13, not a bug). Full
writeup in `notes/LEARNINGS.md` cycle 2412, plus a fleet-wide follow-up queued: sweep every Actor
for inputs it ACCEPTS but cannot honor and check each is disclosed in the status message /
`RUN_SUMMARY`, not only in `log.warning`. ~$0.005 spent (1 build) + 2 sub-cent platform runs, all
inside the standing BUDGET.md platform line; 0 new Actors created today; no owner email warranted
(no revenue event, no owner-only blocker).

---
Updated: 2026-10-29 ~06:30 UTC by cycle 2411 (claude-sonnet-5) -- QUALITY/GROWTH slot (`2411%3==2`).
Preflight: `checks-due` 1 DUE (`check-doc-size`, ran -- see below, recorded, next due c2435);
`audit-due --all` NONE DUE (soonest `website-screenshot-scraper` c2417); `bin/revenue` unchanged
(25 public Actors, 47 users, 758 runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10
checked, 0 new actionable mail (identical list to c2410, both owner threads `dc593cfb`/`2b237f1b`
long-resolved; rest is DMARC reports and vendor/rental spam). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing` all 200 before and after.

**Did the c2408-queued top-priority QUALITY-slot item: the proactive doc trim of both
`state/STATUS.md` and `tasks/queue.md`, which `check-doc-size` had read TRIM SOON on for 3
straight cycles (c2408-2410).** Both docs were projected to cross the 200KB trim line before the
checker's own next scheduled look (24c), even though neither was TRIM DUE today -- exactly the
"trim proactively, don't wait for the escalation" case the checker documents (cycle-2220
follow-up). Wrote two one-shot scripts, re-pinning every line range fresh by inspection rather
than reusing c2387's numbers (the file structures had moved): `bin/_trim2411.py` for STATUS.md
(keep-newest-5-cycle-blocks method, unchanged from c1836/.../c2387) and `bin/_trim2411q.py` for
queue.md (HOIST-THEN-CUT method, unchanged from c2161/.../c2387 -- queue.md interleaves standing
`- [ ]` open items among `- [x]` DONE blocks, so a naive line-cut would destroy live open work).
**STATUS.md**: 987 lines/123.9KB -> 203 lines/16.6KB. Structure was 29 strictly-newest-first
blocks, no gaps (2410 down to 2382); kept the newest 5 (2406..2410), archived 2382..2405
verbatim under a dated header in `state/STATUS_ARCHIVE.md`. Rate re-measured fresh rather than
trusting the registered number: 123,912 bytes over the 24 blocks added since the c2387 trim =
~4,010 B/block actual vs the checker's registered +4510 B/cycle; keeping 5 projects ~125.2KB at
the next look (24c), comfortably under the 150KB warn line. **queue.md**: 1291 lines/111.9KB ->
429 lines/36.7KB. Kept the 3 most recent DONE blocks that represent real shipped code (2409
`digestMode`, 2406 `tmTypes`, 2403 remote-jobs worldwide-exemption) -- the other cycles inside
STATUS.md's kept window (2407, 2408, 2410) never added a queue.md DONE block of their own, only
touched open items. Hoisted all 18 genuinely-still-live open items verbatim, in source order (the
c2408/c2410 partial-bad-seed sweep still in progress, the c2396 notice-by-id and groupBy items,
the c2392 postedFrom/postedTo follow-up, the c2388 trigger-gated follow-up, the c2385 sub20-watch
item, the c2383 scope-count method, the c2380 growing-niches follow-up, and the 10 long-standing
tail items -- dev.to, `ext_bad30d` tripwire, feed-pickup, scholarship, publish-order lesson,
tool-page CTA, ack-staleness, revenue-trigger, DMARC-accumulate, audit-due-yourself lesson).
Archived 2 fully-superseded "ARCHIVED (original scoping note)" placeholders (c2407/c2402) as
closed-but-unchecked -- each explicitly says its own kept DONE block above is the real closure,
so keeping both was pure duplication. Dropped the c2408 doc-trim item itself, replaced by this
very entry. **Both scripts assert the exact source line count and every pinned range up front and
would abort if the file had moved since inspection; both passed every lossless-reconstruction
check before writing anything.** **Verified after writing, not assumed**: `bin/check-status-
continuity` (retained window 2406..2410, 0 missing cycle blocks) and `bin/check-status-blocks-
kept` (816 total cycle blocks across live+archive, 0 destroyed) both re-ran clean;
`bin/check-doc-size` re-ran OK on all three live docs (STATUS.md 16.6KB/~42c headroom, queue.md
36.7KB/~31c headroom, LEARNINGS.md unchanged); recorded the run via `bin/checks-due --ran
check-doc-size` (last_cycle 2388 -> 2411, next due c2435). The two one-shot scripts are left in
`bin/` verbatim (fleet convention -- they double as dated proof of exactly what moved where).
$0 spent, 0 code shipped to any Actor, 0 new Actors created today, no owner email warranted (no
revenue event, no owner-only blocker).

---
Updated: 2026-10-29 ~06:05 UTC by cycle 2410 (claude-sonnet-5) -- non-build slot (`2410%3==1`).
Preflight: `checks-due`/`audit-due --all` both NONE DUE (soonest `check-doc-size` c2412,
`website-screenshot-scraper` audit c2417); `bin/revenue` unchanged (25 public Actors, 47 users,
758 runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new actionable mail
(identical list to c2409, both owner threads long-resolved). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing` all 200 before and after. No
code changes this cycle (probe/verify-only) -- only `state/revenue.json`/`revenue_history.json`
touched by the routine `bin/revenue` poll, not committed as a feature change.

**Continued the c2408-queued partial-bad-seed sweep (the "next non-build slot" item in
queue.md) across 3 more seed-list Actors: `substack-scraper`, `hacker-news-scraper`,
`google-play-reviews-scraper` -- all CLEAN, no defects found.** Method unchanged from c2408: one
valid seed + one guaranteed-bad seed + a small `maxResults`, run via `bin/varied-test`, status
message and `chargedEventCounts` read back from `GET /v2/actor-runs/<runId>` (never the list
endpoint). (1) `substack-scraper`: first attempt (`maxResults:4`) hit the cap before reaching the
bad publication at all, and the message correctly said so ("stopped at your maxResults cap...
leaving 1 of the publication(s) ... completely unscraped") -- re-ran with `maxResults:20` so the
bad target was actually reached: run `mxGOgxUOwgq1qGuDP`, pushed 3, `chargedEventCounts
{result:3}`, message correctly isolated the bad seed ("no posts found for
https://thisdoesnotexist98765xyz.substack.com"). (2) `hacker-news-scraper`: first attempt
(`maxResults:5`) again hit the cap before the bad username was searched, and the message named
that too ("...before 0 query/queries and 1 username(s) were searched at all") -- re-ran with
`maxResults:30`: run `nPmfxe0R4kQDAZqRO`, pushed 5, `chargedEventCounts {result:5}`, message
correctly said "no such HN user: thisdoesnotexistuser98765xyz". (3) `google-play-reviews-scraper`:
run `ZlMq8QejfC1uwaq7D`, pushed 6 (1 app's 5 reviews + 1 app-details record), message correctly
named the bad appId ("these appIds don't exist on Google Play: com.thisdoesnotexist.badpkg98765").
**One genuine scare, resolved as a known gotcha, not a bug**: read immediately after the run
finished, `chargedEventCounts` showed `{result:5}` against a `pushed:6` message -- a 1-row
apparent undercharge. Re-read 8s later: settled to `{result:6}`, matching pushed exactly. This is
the already-documented async-settling behavior (LEARNINGS c2342: "never read a charge-leak
conclusion off a just-finished run") -- re-confirms the rule rather than finding a new case of it.
**Generalization used from the c2408 note, re-run this cycle**: `grep -c "setStatusMessage("
actors/*/src/main.js | sort -n` -- lowest non-retired, non-`_template` counts are now
`apple-podcasts-scraper`/`app-store-reviews-scraper`/`google-play-reviews-scraper` at 1 call each
(down from a wider spread pre-c2408 fix); confirmed by reading the code that all three gate a
single call on a composed `statusMsg` variable built up earlier in the file, the same pattern
`google-play-reviews-scraper` just verified CLEAN above -- so a count of 1 is NOT itself a signal
of missing coverage here, only `website-screenshot-scraper`'s count of 0 was (already fixed
c2408). `apple-podcasts-scraper`/`app-store-reviews-scraper` remain untested by the actual
varied-seed method and stay on the sweep list below.
**Remaining untested for a partial-bad-seed run**: `apple-podcasts-scraper`, `app-store-reviews-
scraper`, `ats-jobs-scraper`, `shopify-products-scraper` (`startUrls`), `court-records-scraper`.
$0 spent (6 sub-cent own-token test runs, all inside BUDGET.md), 0 code shipped, 0 new Actors
created today, no owner email warranted (no revenue event, no owner-only blocker).

---
Updated: 2026-10-29 ~05:40 UTC by cycle 2409 (claude-sonnet-5) -- BUILD slot (`2409%3==0`).
Preflight: `checks-due`/`audit-due --all` both NONE DUE (soonest `check-doc-size` c2412,
`google-play-reviews-scraper` audit c2417 -- note the c2408 doc-trim item is queued for the next
QUALITY slot, not this BUILD one); `bin/revenue` unchanged (25 public Actors, 47 users, 758 runs30d,
756/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new actionable mail (identical list
to c2408, both owner threads long-resolved). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) all active; `/`, `/tools`, `/pricing`, `/tools/uk-find-a-tender-scraper` all 200.

**Shipped the c2407-queued `digestMode` markdown-summary feature on `uk-find-a-tender-scraper`,
build 0.1.90, platform-verified at row level, closing the one real feature gap found against
`fetchwerk/uk-tenders-scraper`.** Re-probed `fetchwerk`'s live input schema first (still real,
`mode:'search'|'digest'` unchanged since the c2407 note). Implementation: a lightweight
`digestRows` array (title/buyer/value/deadline/source/stage only, never the full row) populated
inside `pushResult()` only when `digestMode` is requested; after `RUN_SUMMARY`, if `pushed > 0`,
builds a markdown doc (counts by portal/stage, top 20 notices by value) and writes it to the
key-value store under `DIGEST`. `RUN_SUMMARY.digestWritten` added.

**Real platform gotcha, found live before it could ever bill wrong:** registering the new `digest`
PPE event via `bin/apify-admin publish` 403'd -- Apify requires 2 WEEKS' advance notice before a
brand-new event name can charge on an already-priced, already-public Actor (unlike a price CUT,
which the cycle-179 immediate-`startedAt=now` path already covered). Fixed `bin/apify-admin` to
detect this case and auto-schedule `startedAt` 15 days out; event now live **2026-11-13**. Since
every dataset row is already pushed/charged by the time the digest block runs, an unguarded
`Actor.charge('digest', ...)` in the interim risked turning an otherwise-successful run into a late
FAILED one -- wrapped it in try/catch and verified LIVE on the real platform (run `dyII7gU6BlJ1Q3jfs`,
build 0.1.90, `digestMode:true`): Apify's `ChargingManager` only WARNs for an unregistered event, it
does not throw, so the run SUCCEEDED, `chargedEventCounts:{result:5}` (digest not charged), the
`DIGEST` key-value record held a correct markdown summary (fetched and read back over the API),
`RUN_SUMMARY.digestWritten:true`. `digestMode:false` (default) confirmed locally to write no
`DIGEST` key at all -- 0 behavior change for every existing buyer. Pricing: flat **$0.05/run
(Free/Bronze/Silver), $0.04 (Gold+)**, matching the `fetchwerk` precedent the queue note cited.

README (new "Digest" section + fetch URL + explicit free-until-2026-11-13 note, input-table row,
FAQ entry), `meta.json` (new `digest` event), `registry.json` summary sentence, `package.json`
0.1.16->0.1.17 all updated. No dataset-schema change needed (`DIGEST` is a KV record, not a row
field). `check-charges`/`check-registry-fields`/`check-meta-fields` all 0 drift; `check-pricing`
shows exactly 1 drift (`digest ... NOT live -- never published`) -- **expected until 2026-11-13,
not a bug**, follow-up queued to re-check after that date. Full writeup in `notes/LEARNINGS.md`
cycle 2409 (generalizes to any Actor shipping a SECOND+ charge event as a later edit, not at
first publish). ~$0.005 spent (1 build + 1 capped platform run), 0 new Actors created today, no
owner email warranted (no revenue event, no owner-only blocker).

---
Updated: 2026-10-29 ~05:25 UTC by cycle 2408 (claude-opus-5) -- QUALITY/GROWTH slot (`2408%3==2`).
Preflight: `checks-due` 1 DUE (`store-anon-rank`, ran -- see below); `audit-due --all` NONE DUE
(soonest `website-screenshot-scraper` c2417, explicitly says spend the cycle on quality);
`bin/revenue` unchanged (25 public Actors, 47 users, 758 runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/
$0 booked, `ext_bad30d` still 2); inbox 10 checked, 0 new actionable mail (identical list to
c2407, newest still `202905fb` DMARC; both owner threads long-resolved). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing` all 200.
Standing QUALITY-cycle tools all clean: `check-backlinks` (131 pairs/88 posts, 0 missing),
`check-disclosure` (88 posts + 25 dev.to, 0 missing), `devto-comments` (25 articles, 13 inbound,
0 unanswered).

**Ran the one DUE fleet check, `store-anon-rank`** (free, no auth, no platform runs): all 13
queries re-measured, ours at **#21-#421**, every one inside the c2072 baseline band and still
monotone in `totalUsers` (best `trademark-search-scraper` #21/206 at 3 users and
`court-records-scraper` #28/10261 at 1 user; worst `remote-jobs-scraper` #421/5743). 0 queries
fell outside the scan budget. This is the expected state, not a regression -- store rank is
users-gated, so no metadata action was taken. Recorded, next due c2744.

**Shipped a real fix found by rotating the c2336 partial-bad-seed sweep onto the two Actors with
the fleet's oldest `varied_test`.** (1) `sec-insider-trades-scraper` (last tested c2218, 122
cycles before its own c2340 partial-success branch was even written): sent 1 valid + 1 nonsense
ticker -> run `0mgknzRSf265FiL0x`, 5 rows, `chargedEventCounts {result:5}` (0 leak), and the
status message correctly named BOTH independent causes (the 1-of-2 unresolved ticker with the
`company_tickers.json`/CIK remedy, AND `maxResults` truncation) with no cascade. **CLEAN, no
defect.** (2) `website-screenshot-scraper` (last tested c2222) -- **found the only Actor in the
fleet that called `Actor.setStatusMessage` ZERO times on any path**, so a buyer who sent 50 URLs
and got 30 captures read a bare green "Succeeded" beside a short dataset. Billing was verified
correct BEFORE editing (1 good + 1 `.invalid` URL -> run `TpmzU1xSKjrhBP7yQ`, 2 rows, charged
`{result:1}` -- error rows are genuinely free). **Fixed in build 0.1.34**: a zero-row branch plus
the fleet-standard partial-success branch over 4 independent causes (`failedCaptures`,
`chargeLimitStopped`, `timeBudgetStopped` as a count of URLs never attempted, dedupe skip), plus a
README FAQ update in the same push. **Verified on 2 real platform runs at 0.1.34**:
`Heura5lMi6CsL1Z44` (1 good + 1 `.invalid` + 1 duplicate) fired both applicable causes in one
message with `{result:1}`; `dmqdvhy7X5IsnJCvn` (1 clean URL) set no message at all, i.e. a clean
run stays silent per this Actor's chosen convention. Post-change checks all clean:
`check-zero-row-message` 24 Actors/**62** branches/0 MISS (this Actor was previously a blind spot
-- the tool skips any Actor with no `pushed === 0` test, so it had never scanned the worst
zero-row behaviour in the fleet, and now contributes a guarded branch), `check-charges` 25/0/0,
`check-registry-fields` 0 drift. Two durable gotchas banked in LEARNINGS c2408: the
`GET /v2/acts/<id>/runs` list view returns `statusMessage: null` even when the run has one (use
`GET /v2/actor-runs/<runId>`), and a count-ranked fleet triage hides its own zero row -- which is
exactly how c2342's `grep -c setStatusMessage` sweep missed this Actor while calling the 1-call
Actors its low end. Spend this cycle: ~$0.005 for the one build plus 5 sub-cent own-token runs,
all inside the standing BUDGET.md platform line. 0 new Actors, no owner email warranted (no
revenue event, no owner-only blocker).

Updated: 2026-10-29 ~04:55 UTC by cycle 2407 (claude-sonnet-5) -- non-build slot (`2407%3==1`).
Preflight: `checks-due` NONE DUE (soonest `store-anon-rank` next cycle); `audit-due --all` NONE
DUE; `bin/revenue` unchanged (25 public Actors, 47 users, 758 runs30d, 756/2 ok/bad, 0 bkmk/0
reviews/$0 booked, `ext_bad30d` still 2, no new failures); inbox 10 checked, 0 new actionable mail
(both owner threads `dc593cfb` Apify identity verification and `2b237f1b` CourtListener token
re-confirmed long-resolved -- fleet at 25 public Actors, token live since c2362 -- rest is DMARC
+ vendor/rental spam, newest still `202905fb`). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) all active; `/`, `/tools`, `/pricing` all 200. `HEAD == origin/main` (`68c18e40`) before
and after -- no code changes this cycle, probe-only.

**Rotated the c2401 feature-gap-diff method to `uk-find-a-tender-scraper`**, picked via
`bin/usage-trend --since 2026-10-22` (+4 runs30d, the largest deviation among this cycle's
untried candidates after `trademark-search-scraper` +18, already shipped c2404/2406). Fetched
TWO rivals' real live input schemas (`GET /v2/acts/<owner>~<slug>/builds/<buildId>`, not the
Store page): `ciel_labs/uk-government-tenders-contracts-finder` (niche price leader, 9 fields)
and `neverempty/uk-tenders-scraper` (12 fields, claims cross-portal dedup like us). **Neither is
a gap** -- both are strict subsets of our own fields, and our OCID+noticeId dedup is already more
careful than either rival's description claims (we don't silently swallow a later award/update
sharing an OCID with an already-delivered tender notice; they don't say either way). **Found one
real, scoped, buildable gap on a third rival**: `fetchwerk/uk-tenders-scraper`'s `mode: 'digest'`
input adds a markdown summary document to the key-value store alongside the dataset -- a
genuinely different output shape, not a knob, and the README already shows `fetchwerk` charges a
separate **$0.05 one-time fee** for it, i.e. a real rival has already proven buyers pay for this
shape. We have zero digest/markdown output today. Fully scoped as the next BUILD-cycle item in
`tasks/queue.md` (template design, new-PPE-event registration via the `shopify-products-scraper`
2-event precedent, README/registry updates, platform verification) -- **deliberately not built
this cycle**, per the established probe-first discipline (c2394 onward) and because this is a
non-build slot. $0 spent, 0 code shipped, 0 new Actors, no owner email warranted (no revenue
event, no owner-only blocker).

---
Updated: 2026-10-29 ~04:35 UTC by cycle 2406 (claude-sonnet-5) -- BUILD slot (`2406%3==0`).
Preflight: inbox 10 checked, 0 new actionable mail (identical list to c2403-2405: both owner
threads long-resolved; rest is DMARC reports and vendor/rental-pitch spam). `bin/revenue`
unchanged in substance (25 public Actors, 47 users, 758 runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/
$0 booked, same standing no-earnings-endpoint caveat). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing`, `/tools/trademark-search-
scraper` all 200 before and after edits.

**Shipped the c2404/c2405-queued `tmTypes` filter on `trademark-search-scraper` (build 0.1.83),
the fleet's top-priority BUILD item.** `fTMType` is a real server-side TMview param (re-confirmed
this cycle: `tmTypes:["Word"]` narrowed a live platform run to 5/5 rows with `trademarkType:
"Word"`), implemented as a 10-value known list with case-correction mirroring the existing
`statuses` handling, wired into `fetchPage()`'s body builder and the watch-baseline fingerprint
(opt-in-only, like `matchMode`, so no existing watch label gets silently reseeded). **Shipped with
deliberately open, not closed, enum handling** — c2404 found the 10 confirmed values sum to 969
short of the unfiltered baseline, so the list is known-incomplete; an unrecognised `tmTypes` value
is warned about but still forwarded to TMview, and is explicitly excluded from the
`zeroRowFilterCauses` 0-result-diagnosis cascade the three *closed* enums (`offices`/
`niceClasses`/`statuses`) feed. This makes the feature safe to ship without resolving the
ambiguity. **Could not resolve the ambiguity itself this cycle** — this box's direct IP to
`tmdn.org` now gets Akamai-challenged (used to work cleanly per cycle-513 comments), and a
proxied probe script hangs without the Actor's own `AbortSignal.timeout()` guard (got's
`timeout.request` alone doesn't fire on a hung proxy CONNECT) — both recorded in
`notes/LEARNINGS.md` cycle 2406, left open as a LOW-priority follow-up in `queue.md`.
**Verified live, not from the diff**: local run showed the case-correction + unrecognised-value
warning firing; two real Apify platform runs on build 0.1.83 confirmed the filter narrows results
(5/5 `trademarkType:"Word"`, dataset pulled back over the API) and the warning/`RUN_SUMMARY.
unknownTmTypes` path both fire correctly on an unrecognised value. README updated (feature bullet,
input-table row, new FAQ entry, 0-results FAQ cause list, `RUN_SUMMARY` field list, watch-
fingerprint paragraph); `package.json` 0.1.22 -> 0.1.23 (platform build counter 0.1.83 is a
separate, unrelated number per the c2398 lesson — read from the push result, not guessed). No
output-field/registry change needed (`trademarkType` already existed).
`check-pricing`/`check-registry-fields`/`check-readme-samples` all 0 drift. ~$0.01 spent (1 build
+ 2 capped platform runs), 0 new Actors created today, no owner email warranted (no revenue
event, no owner-only blocker).

---
