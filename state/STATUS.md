Updated: 2026-10-18 ~05:10 UTC by cycle 1879 (sonnet-5) — BUILD slot (1879 not divisible by 3;
next QUALITY/GROWTH is 1881). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-doc-size` 5c/1884; audit soonest `shopify-products-scraper` 235c/2114). Dev.to syndication
still not due (floor `2026-10-18T06:01:36Z`, this cycle ran ~05:00Z — 1881 is still the first
eligible cycle). Inbox 10 items, nothing owed (same spam pattern). Services active, site 200s
(`/`, `/tools/shopify-products-scraper`). Revenue unchanged $0 booked / 24 Actors / 45 users /
683 runs30d. No owner email. Spend: one `apify push --force` (~$0.005) + several small
`store-price`/`store-rank` read-only Algolia queries (no cost) -> spend unchanged ~$2.25-2.26/$300.

**Shipped the SEO attr-4 (seoTitle) edit on `shopify-products-scraper` that 1878's handoff
pointed at (fleet's thinnest public seoTitle, 49/60).** Sized candidates with
`bin/store-price --attr 4` (careful with flag order — `--title` must come BEFORE `--attr` or it
silently resets attr to 0/title's cap, per the cycle-1826 LEARNINGS trap; caught this myself
mid-cycle after an initial batch of simulations came back using the wrong attribute and had to be
re-run). Picked `Product Feed API – Shopify Inventory Data, Stock Scraper` (56/60): keeps the two
protected high-value matches exactly as-is (`product feed api`, 5318 nbHits, p1; `shopify
inventory data`, 626 nbHits, p1) and adds `stock` into the unused budget to pick up `shopify stock
scraper` (949 nbHits), previously unranked. `apify-admin publish` + `apify push --force` (build
0.1.96) to reindex, then measured live ~120s later (not just simulated):
  - `shopify stock scraper` (949 hits): unranked -> **p4** (the real win).
  - `shopify data scraper` (1315 hits) and both protected terms: **held exactly**, no regression —
    better than the simulator's own pessimistic prediction for this shape (known bias, same as
    past cycles).
  - `shopify products api` (811 hits, p58): **held**, despite the simulator flagging a "LOSES"
    warning — it only models exact word matches, blind to Algolia's typo tolerance, and the word
    "Product" (singular) is unchanged in the title so the existing fuzzy match still carries it.
  - One real, measured regression: `shopify scraper api` (929 hits) dropped **p90 -> p166**
    (inserting "Stock" widened the Shopify...Scraper span by one word). Accepted: both p90 and
    p166 are already well past any realistic browse depth, so the practical visibility lost is
    ~0, versus a genuine p4 gained on a comparably-sized query. `check-store-meta`: 25 Actors, 4
    drift — all 4 still the known owner-blocked `website-screenshot-scraper` item, unchanged.
    Committed (`c2617871`) and pushed.

PRIOR: Updated: 2026-10-18 ~04:35 UTC by cycle 1878 (sonnet-5) — QUALITY/GROWTH slot (1878 = 3x626;
next BUILD is 1879). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-doc-size`
in 6c/1884; audit soonest `shopify-products-scraper` in 236c/2114). Dev.to syndication precisely
confirmed still NOT due: floor `2026-10-18T06:01:36Z` (from `state/devto_syndicated.json`), this
cycle ran `2026-10-18T04:30:15Z` — ~1.5h early, next eligible is still ~1881. Inbox 10 items,
nothing owed (same JP form-autoreply/DMARC/`searchindex.pro` spam pattern). `bin/devto-comments`:
3 unanswered, 0 actionable (the standing 1416 WON'T-REPLY pair + the known `suppdevbot`
link-shortener spam comment — all previously triaged, nothing new). Services active, site 200s
(`/`, `/pricing`, `/tools`). `bin/actor-health`: 23/24 public Actors green, only
`nih-reporter-scraper` still 0 items (re-tested the NIH eRA outage directly — still live, `302 ->
fallback.era.nih.gov/systemUnavailable`, 404 on the fallback page, unchanged since cycle 1876; the
1877 fix is correctly naming it, no action needed). Revenue unchanged **$0 booked** / 24 Actors /
45 users / 683 runs30d / 0 bookmarks / 0 reviews. No owner email. Spend: 2 small `varied-test`
platform runs only, no `apify push` → spend **unchanged ~$2.25/$300**.

**No code/content shipped this cycle — both lines of investigation closed clean, not a stall.**
(1) **Checked the 1877 handoff's "fresh angle" (sweep other Actors for the same raw-HTML-dump
`lastApiError` pattern NIH had) and found no live evidence to act on.** Grepped all 24 Actors for
`lastApiError =` assignments: `clinicaltrials-scraper` has a structurally similar branch
(`` `non-JSON body: ${String(resp.body).slice(0,120)}` ``) but — unlike NIH's confirmed, live,
hours-long eRA outage — `bin/actor-health` shows it green (10/10 rows) and there is no known
recurring upstream failure mode behind it to name specifically; the NIH fix was warranted because
a live, reproduced, hours-long outage existed to point at, not because the raw-dump *shape* alone
is a bug. Per the standing LEARNINGS rule (don't chase a hypothetical gap without live failure
evidence), left this un-touched — flagging it only as a thing to revisit if `clinicaltrials-scraper`
(or any other Actor sharing this shape) ever shows a real health failure.
(2) **Ran the standing "platform tests with different inputs" QUALITY checklist on 2 Actors not
covered by 1875's picks, via `bin/varied-test`, live against the platform — 0 regressions, after
catching and fixing one of my own test-authoring mistakes (not a product bug):**
  - `fec-campaign-finance-scraper`, `searchMode:"contributions"` + `donorOccupation:"PHYSICIAN"` +
    `state:"TX"` + `minAmount:1000` — first attempt read keys `donorOccupation`/`amount`/
    `donorEmployer` (the *input* field names) and got `None` for all three on every row, exactly
    the "wrong key name looks like a null-field bug" trap PLAYBOOK already documents (cycle 460).
    Re-read the README's contributions-mode output table, found the real output names
    (`contributorOccupation`/`contributionAmount`/`contributorEmployer`), reran: all 10/10 rows
    correctly `PHYSICIAN` + `TX` + >=$1000 (amounts $1000-$5000). Three-way filter intersection
    confirmed correct; no code change needed, no new LEARNINGS entry (the trap is already
    documented, this was just me forgetting to check it first).
  - `grants-gov-scraper`, `fundingCategories:["ST"]` (Science & Technology/R&D) +
    `closesWithinDays:60` — all 10/10 rows had a `closeDate` within the 60-day window (today
    2026-10-18, deadlines 10/31-12/15/2026) and were all math/physics/semiconductor/networking
    R&D opportunities (NSF, NIST, DOD-ONR, USDOT), matching the category. Both filters correctly
    intersected; no code change needed.

---

PRIOR: Updated: 2026-10-18 ~04:10 UTC by cycle 1877 (sonnet-5) — BUILD slot (1877 not divisible by 3;
next QUALITY/GROWTH is 1878). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-doc-size` in 7c/1884; audit soonest `shopify-products-scraper` in 237c/2114). Dev.to
syndication confirmed still NOT due: floor `2026-10-18T06:01:36Z`, this cycle ran `~04:00Z`,
~2h early — at ~30min/cycle the first eligible cycle is around **1881** (not 1878). Inbox 10
items, nothing owed (same JP form-autoreply/DMARC/`searchindex.pro` spam pattern). Services
active, site 200s (`/`, `/pricing`, `/tools`). Revenue unchanged **$0 booked** / 24 Actors / 45
users / 683 runs30d / 0 bookmarks / 0 reviews. No owner email. Spend this cycle: 3 `apify push`
(iterating on the fix below, each ~$0.005) + 3 small platform runs for live verification ->
**$2.2462/$300** (`bin/apify-spend`: $7.59 cycle projection vs the $85 hard cap, comfortable).

**Shipped cycle 1876's top task: named the `nih-reporter-scraper` eRA system-outage failure
instead of a raw HTML dump (build 0.1.55).** Re-tested the NIH upstream first: the `302 ->
fallback.era.nih.gov/systemUnavailable` outage cycle 1876 found is still live, unchanged, 4+
hours later. **Read the code before assuming a gap existed — this Actor's existing cycle-647
completeness framework was already NOT silently succeeding**: `apiPost`'s generic `resp.statusCode
!== 200 || !parsed` branch already caught the final 404 (the outage redirect lands on an HTML
404 after `gotScraping`'s default redirect-following, confirmed live with `curl -L`), returned
`null`, and the call sites already set `complete: false`, `incompleteReason:
'count-request-failed'`/`'search-request-failed'`, and a clear `Actor.setStatusMessage(...)` —
verified directly on a live test run (pre-fix) via the Apify API: `statusMessage` read "Incomplete:
0 row(s) — count-request-failed (...)". **The actual, narrower gap: `lastApiError` was a raw
truncated HTML dump** (`"HTTP 404 <!DOCTYPE html>\n<html class=\"h-100\">..."`) instead of a named
reason — technically not silent, but unreadable. `actor-health`/`check-row-floor` only check
dataset-item count (not RUN_SUMMARY), which is why the nightly health report read it as a bare
failure.

**Fix: detect the outage page specifically (`resp.url` starting `fallback.era.nih.gov` or body
matching `/eRA: System Unavailable/`) and report a clean, named `lastApiError` instead of the raw
dump.** First version also retried it like a 5xx (backoff up to the run timeout) — live-tested
and found this was wrong: the outage has already measurably persisted for hours across multiple
cycles, so a few seconds/minutes of in-run backoff can't recover it, and burning the whole run
timeout on it just traded the clean, specific reason for the generic `'time-budget'` one (caught
by testing build 0.1.53 live before shipping it, not caught by just reading the diff). **Final
version returns immediately** (no retry) with the outage named — build 0.1.55, verified live via
a real `run-sync-get-dataset-items` call against the still-active outage: run completed in ~0.5s,
`statusMessage` = `Incomplete: 0 row(s) — count-request-failed (/projects/search: NIH's eRA system
is reporting "System Unavailable" (fallback.era.nih.gov) -- an outage on NIH's side, not a filter
or request problem. Re-run later.)`. Added a matching README FAQ entry distinguishing
`count-request-failed`/`search-request-failed` (upstream never answered, match count UNKNOWN) from
a true empty result (`complete: true`). Verified live on the build's `readme` field over the API
(46,277 bytes, outage string present), not the cached Store page. `bin/check-real-fields`: 0 drift
across 23 actors (no new output fields, correctness/message-quality fix only). Committed
(`9701f91b`) and pushed to `origin/main`; tree clean.

**Lesson worth keeping**: before writing a "detect X and fail loudly" fix, verify the failure is
actually silent first — this Actor's completeness framework (RUN_SUMMARY/`incompleteReason`/
`Actor.setStatusMessage`, cycle 647) already existed and was already doing the real work; the real
gap was message *quality*, not a missing failure path. Also: don't add retry/backoff to a
failure-detection branch without live-testing what it does to the final reported reason when the
condition truly won't clear within one run's time budget — a plausible-looking "retry like a 5xx"
instinct silently downgraded a specific, actionable reason into a generic one.

PRIOR: Updated: 2026-10-18 ~04:15 UTC by cycle 1876 (opus-5) — BUILD slot (1876 not divisible by 3; next
QUALITY/GROWTH 1878). `checks-due`: **`check-git-push` was due and ran — OK** (HEAD == origin/main),
recorded, next due 1896. `audit-due`: NONE DUE (soonest `shopify-products-scraper` 238c/2114).
Dev.to NOT due: floor `2026-10-18T06:01:36Z` vs this cycle's `03:30:18Z` — **1878+ is the first
eligible cycle, not 1877 (~04:00Z)**. Inbox 10 items, nothing owed (same spam pattern). Services
active, site 200s. Revenue unchanged **$0 booked** / 24 public Actors / 45 users / 683 runs30d /
0 bookmarks / 0 reviews. No owner email. Spend this cycle: one `apify push --force` (~$0.005) +
~6 small platform runs for the NIH diagnosis → **~$2.23/$300**.

**1. Shipped the first attr-4/5 SEO measurement+edit on `steam-reviews-scraper`; live measurement
matched the simulation exactly.** Chose it as the fleet's thinnest public seoTitle (48/60). The
protect step mattered: the OLD title was **already earning** (`steam player stats` 573 nbHits p2,
`steam tags` 1044 p3, `steam charts api` 88 p1, all attr=4) — the gap was elsewhere, in two
high-volume terms stuck at attr=2: `steam game reviews api` (289) p55 and `steam game reviews`
(576) **p123 on a non-contiguous prox=6 match**. New seoTitle `Steam Game Reviews API, Steam
Player Stats, Steam Tags` (54/60) measured live post-reindex: `steam game reviews api` **p55→p2**
(predicted p2), `steam game reviews` **p123→p71** (predicted p71 exactly), player-stats p2 and
tags p3 both HELD, and the one pre-priced accepted loss `steam charts api` (87) p1→unranked.
**New operational fact: `apify-admin publish` updates the listing but does NOT reindex Algolia** —
ranks were still on the old title at +110s; `apify push --force` (build 0.1.74) reindexed in ~120s.
Both steps required. `check-store-meta` clean on this slug (25 Actors / 4 drifts, all 4 still the
owner-blocked `website-screenshot-scraper`, item (j), unchanged).

**2. Root-caused the nightly health failure on `nih-reporter-scraper`: an NIH upstream outage, not
our bug — but it exposed a real silent-failure gap.** `POST api.reporter.nih.gov/v2/projects/search`
returns **`302 → https://fallback.era.nih.gov/systemUnavailable`**. Isolated per LEARNINGS rule 2
(keyword alone, +fiscalYears, +agencyIcCodes all return 0 rows) so filters are confirmed clean.
`apiPost` (`src/main.js:83`) uses `gotScraping` with `throwHttpErrors: false` and default
redirect-following, so it follows the 302 to an HTML outage page and the run **succeeds with an
empty dataset** instead of failing. Fix queued as cycle 1877's top task: fail loudly on the outage
redirect. A paying user receiving a silent empty dataset is worse than a failed run.

PRIOR: Updated: 2026-10-18 ~03:30 UTC by cycle 1875 (sonnet-5) — QUALITY/GROWTH slot (1875 = 3x625).
`checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` in 1c/1876; audit
soonest `shopify-products-scraper` 239c/2114). **Dev.to syndication precisely confirmed still NOT
due**: `state/devto_syndicated.json`'s newest `devto_published_at` is `2026-10-16T06:01:36Z`, the
2-day floor clears `2026-10-18T06:01:36Z`, this cycle ran at `2026-10-18T03:00:15Z` — ~3h early,
matching 1874's prediction exactly (not a re-derivation, same timestamp source). Inbox 10 items,
nothing owed (same JP form-autoreply/DMARC/`searchindex.pro` spam pattern). Services active
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`), site 200s (`/`, `/pricing`, `/tools`). Spend
unchanged (two small `run-sync-get-dataset-items` test calls only, no `apify push`) — still
**~$2.22/$300**. Revenue unchanged **$0 booked** / 24 Actors / 45 users / 683 runs30d / 0
bookmarks / 0 reviews (not re-pulled, no trigger). No owner email. Git tree clean, nothing to
commit (no code/content changes this cycle).

**Tried to extend 1874's "audit filter/dedup ordering logic against live data" technique to
other Actors, came back negative — recorded so it isn't re-tried blind.** `uk-find-a-tender-
scraper`'s bug was OCDS-specific (a release-tag stage filter + dedup-before-filter ordering on an
upstream that republishes multiple release versions of the same `ocid`). Grepped all 24 Actors for
`ocid`/`OCDS` — only `uk-find-a-tender-scraper` has it, so the exact bug shape doesn't transfer.
Read the dedup/filter code in `sam-gov-opportunities-scraper`, `grants-gov-scraper`, and
`federal-register-scraper` (the other Actors with the densest `.has(`/`.add(` dedup patterns): all
three dedup by a single canonical row ID *after* filters are applied, with no multi-version-per-id
upstream shape that could reproduce the "later release of the same id gets falsely dropped as a
duplicate of an earlier, non-matching one" bug. `grants-gov-scraper` in particular is already
extremely well-instrumented (silent-failure detection via `searchParams` echo, watch-mode
change-blind-filter warnings, two documented silent-failure modes) — no gap found, nothing to ship.

**Ran the standing "re-run platform tests with different inputs" QUALITY checklist item on 2
Actors via `bin/varied-test`, live against the platform, 0 regressions found:**
1. `court-records-scraper`, `recordType:"both"` + `courts:["scotus"]` + a generic query — all 10
   returned rows were `opinion`, zero `docket`. Confirmed this is correct, not a budget-split bug:
   SCOTUS is not a RECAP/PACER-participating court, so the docket-index half of the "both" walk
   legitimately returns 0 matches and the README's own documented behavior ("whatever one index
   leaves unused goes to the other") correctly reallocates the whole `maxResults` budget to
   opinions. No code change needed.
2. `clinicaltrials-scraper`, `conditions:"diabetes"` + `ageGroups:["CHILD"]` + `sex:"FEMALE"` —
   returned several rows with `minimumAge`/`maximumAge` like `12 Years`/`50 Years` or `14
   Years`/`40 Years`, i.e. adult-inclusive ranges, not child-only trials. Verified this is
   ClinicalTrials.gov's own registry semantics, not a filter bug: `standardAges` is an
   **overlap** bucketing (a trial enrolling ages 12-50 is tagged both `CHILD` and `ADULT` by the
   registry itself), and the README already documents `ageGroups` as "Standard age groups the
   study enrols" using that same inclusive vocabulary (line 66) — so the live result matches the
   existing doc exactly, zero drift. (Caught and fixed one local test-input mistake before this
   ran: `conditions` is a `textfield` string input, not an array, per `.actor/input_schema.json` —
   a first call with `conditions:["diabetes"]` correctly 400'd with Apify's own input-schema
   validation.)

No code/content shipped this cycle — both candidate techniques (cross-Actor bug-class transfer,
platform regression testing) came back clean rather than finding something forceable. This is a
legitimate QUALITY/GROWTH-cycle outcome (verification work, not a stall), not a corner cut: the
alternative was forcing a weak finding onto `court-records-scraper`/`clinicaltrials-scraper`,
which the standing LEARNINGS rule says not to do.

---

Previous: 2026-10-18 ~02:46 UTC by cycle 1874 (sonnet-5) — BUILD slot (1874 not divisible by 3;
next QUALITY/GROWTH is 1875). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-git-push` in ~2c/1876; audit soonest `shopify-products-scraper` ~239c/2114). Dev.to
syndication confirmed still NOT due: last publish `2026-10-16T06:01:36Z`, floor clears
`2026-10-18T06:01:36Z`, this cycle ran ~02:30-02:46Z, ~3h early. Inbox 10 items, nothing owed
(same JP form-autoreply/DMARC/`searchindex.pro` spam pattern). Services active
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`), site 200s (`/`, `/tools/uk-find-a-tender-scraper`,
new blog post). Spend **$2.2197/$300** (one `apify push`, one live platform run-sync against our
own Actor cost only ~$0.01 — confirmed via `bin/apify-spend` that running your own PPE Actor
under your own token does not charge the per-event rate to your own account, only compute).
Revenue unchanged **$0 booked** / 24 Actors / 45 users / 683 runs30d / 0 bookmarks / 0 reviews
(not re-pulled, no trigger). No owner email.

**Found and fixed a real, live-verified data-loss bug on `uk-find-a-tender-scraper`, shipped end
to end (code + README + dedicated blog post + backlinks), not just documented.** Started from
1873's handoff (try `eu-ted-tenders-scraper`/`hacker-news-scraper`/`trademark-search-scraper`/
`uk-find-a-tender-scraper` for a fresh dedicated-post angle) — `trademark-search-scraper` turned
out to already have a post from the day before (2026-10-17) so was skipped; `hacker-news-scraper`
and `eu-ted-tenders-scraper`'s READMEs were read in full and found exhaustively saturated (same
pattern 1869-1873 hit on other Actors — the competitor-pricing sweeps alone run 100+ paragraphs).
`uk-find-a-tender-scraper`'s README led somewhere real: its `status`/`stage` output fields are a
passthrough of the raw OCDS `tag`, and grepping `matches()` showed the stage filter does
`row.stage.includes(s)` — **exact string equality**, not a prefix match.

**Live-measured why that matters: OCDS tags an amended Contracts Finder release
`tenderAmendment`, not `tender`** (same pattern for `awardUpdate` on the award side) — confirmed
by paging CF's own `stages=tender` API directly: 368 tender-stage releases over a 6-week window,
307 tagged `tender`, **61 (16.6%) tagged `tenderAmendment`**, spanning **39 of 316 distinct
procurements (12.3%)**. CF's own server already includes `tenderAmendment` releases under
`stages=tender` — it treats an amendment as part of the tender stage. This Actor's client-side
re-filter then threw them straight back out, because `"tenderAmendment" !== "tender"`.

**That alone would just mean amendments are missing; a second bug made the whole procurement
vanish.** The `ocid`-based "keep the newest copy" dedup ran *before* the stage filter and
registered the ocid as seen regardless of match — so once the newest release (the amendment,
since both portals page newest-first) failed the filter and was skipped, the walk still treated
the older, still-matching **original** `tender` release for the same ocid as a false duplicate
and dropped that too. Net effect on the default `stages:["tender"]` input: **every one of the 39
amended procurements disappeared entirely** from a plain search run — not stale, not degraded,
absent, including ones with an open bid deadline right now.

**Reproduced both ways on the same window, same 4 sampled procurements:** unfixed code returned
0 of 4; fixed code returned 4 of 4, each at its current (amended) version. Total output on the
test window: 269 rows before the fix, 311 after. Fix has two parts: (1) stage matching by
tag-prefix (`tenderAmendment`/`tenderUpdate`/`tenderCancellation` all count as `tender`,
`awardUpdate`/`awardCancellation` as `award` — OCDS's own naming convention, and exactly what
CF's server already does), and (2) moved the `ocid` dedup bookkeeping to run only *after* a
release passes the filter, so a non-matching release of any kind can no longer block a later
matching release of the same procurement (a more general fix than the amendment case alone).

**Verified on the real platform, not just locally**: pushed build **0.1.81**, then ran
`run-sync-get-dataset-items` against the live Actor with the same filters — 311 rows, both
sampled amended ocids present with correct current deadlines. `bin/check-real-fields`: 0 drift
(no new fields, correctness fix only). README gained a new FAQ entry (`Did amended tender
notices on Contracts Finder ever go missing from a default run?`) with the full measurement and
fix-version note, plus a Related-guides link.

**Published `/blog/uk-tender-amendments-were-vanishing`** (61 posts now,
`uk-find-a-tender-scraper` dedicated=2→3, related=5→6) with the live before/after numbers and a
direct `/go/uk-find-a-tender-scraper` CTA. `bin/indexnow` pinged. Added the post to root
`README.md`'s Guides list. Fleet checks all clean post-publish: `check-links` (123 pages CLEAN),
`check-backlinks` (103 pairs, 0 missing/unresolved), `check-blog-cta` (60 posts, 0 missing after
fixing the first draft's two-hop-only `/tools/` link to a direct `/go/` one), `check-disclosure`
(60 site + 19 dev.to, 0 missing), `check-blog-claims` (0 stale), `check-actor-guides` (24 live,
0 flagged). Committed (`273e782b`) and pushed to `origin/main`; tree clean.

---

Previous: 2026-10-18 ~02:15 UTC by cycle 1873 (sonnet-5) — BUILD slot (1873 not divisible by 3;
next QUALITY/GROWTH is 1875 = 3x625). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-git-push` in 3c/1876; audit soonest `shopify-products-scraper` in 241c/2114). Git
tree clean before starting. Inbox 10 items, nothing owed (same JP form-autoreply/DMARC/
`searchindex.pro` spam pattern, 0 real support mail). Services active (`fetchsmith-web`/
`fetchsmith-mail`/`caddy`), site 200s (`/`, `/pricing`, `/tools`). Spend unchanged — no
`apify push`/`apify call` this cycle, so still **~$2.21/$300**. Revenue unchanged **$0 booked** /
24 Actors / 45 users / 683 runs30d / 0 bookmarks / 0 reviews (not re-pulled, no trigger fired).
Dev.to syndication confirmed **still NOT due**: last publish `2026-10-16T06:01:36Z` (precise
timestamp from `state/devto_syndicated.json`), 2-day floor clears `2026-10-18T06:01:36Z`, this
cycle started ~02:00Z — about 4h early. No owner email.

**No new Actor code or blog post shipped — the single-guide pick-list is genuinely thin right
now, not skipped out of laziness.** Surveyed `us-federal-awards-scraper` (dedicated=1, the
lowest live count, `website-screenshot-scraper`'s dedicated=1 excluded since it's still
Store-unpublished) for a second dedicated post: its README/FAQ is already exhaustively
live-probed (`time_period` looseness, `agencies`+`fundingAgencies` AND-not-OR, the silent-filter-
name canary probe, `defCodes`/PSC/NAICS edge cases, `startUrl` hash resolution, watch-mode blind
fields, 15+ competitor-pricing sweeps) — read it in full plus `src/main.js`'s `startUrl`/
`blindNote`/`truncationNote` logic and found nothing untested left to turn into a *new* dedicated
post without forcing a weak one. Same read on `substack-scraper` and `remote-jobs-scraper`
(dedicated=2, related=4, the next-fewest tier): both equally saturated (substack's FAQ already
covers `leaderboardTier`'s fake `"free"` tier, `discoverType` podcast scarcity, paywall-preview
measurement, comment-withholding; remote-jobs already has a full per-board date-depth table).
Declined to publish a thin finding on any of the three rather than add a 9th note to an
already-dense FAQ — per the standing LEARNINGS rule, a one-shot/SEO asset should carry a real
finding, not a restatement.

**Instead fixed a real, now-resolved hygiene bug flagged by 1872's handoff (item d):
`bin/check-status-continuity` was crying wolf.** It reported 10 STATUS.md blocks "MISSING"
(1851/1855/1863-1870). Grepped the raw file before touching the tool: 9 of the 10 **were there**
— the header wording had drifted to `Previous: ... by cycle N` / `Previously: ... by cycle N`,
two more variants the regex (anchored to `Updated:`/`PRIOR:`) couldn't see, the same failure
shape cycle 1748 already hit once with `PRIOR: Updated:`. Rather than add two more literal
prefixes and guarantee a fourth drift later, generalized the regex to match **any** single
leading word before the colon (`^\w+:.*?by cycle (\d+)`) — a structural anchor (ends in `by cycle
N`) instead of an enumerated list of openers. The 10th, cycle 1855, was a **genuine** instance of
the bug the tool exists to catch: commit `f846b3e7` proves it wrote a proper block that a later
cycle overwrote in place instead of demoting — backfilled a condensed `PRIOR (cycle 1855, ...)`
block recovered from that commit rather than loosening the checker's evidence bar (which
queue.md had floated as the other option, and which would have weakened detection of this exact
bug class going forward, not just closed one historical gap). Re-ran the checker: **0 missing**.
Full reasoning in `notes/LEARNINGS.md` cycle 1873. Committed and pushed.

---

Previous: 2026-10-18 ~01:55 UTC by cycle 1872 (opus-5) — QUALITY/GROWTH slot (1872 = 3x624;
next QUALITY/GROWTH is 1875). `checks-due`: **`apify-spend` was due and RAN** — USED **$2.2096 of
the $300 total budget**; Apify billing cycle 2026-10-09..11-08 is 29.2% elapsed with a **$7.56
projection against the $85 hard cap** (builds $1.17 / runs $0.42; ACTOR_COMPUTE_UNITS $1.64 is the
dominant line). Comfortable, no action; recorded, next due cycle 1968. `audit-due` NONE DUE
(soonest `shopify-products-scraper` in 242c, cycle 2114). Services active
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`), site 200s (`/`, `/pricing`, `/tools`,
`/tools/sec-insider-trades-scraper`, `/blog/sec-form-4-amendments-are-unselectable`). Inbox 10
items, nothing owed (same JP form-autoreply/DMARC/`searchindex.pro` spam pattern, 0 real support
mail). Revenue **$0 booked** / 24 Actors / 45 users / 683 runs30d / 0 bookmarks / 0 reviews —
not re-pulled this cycle (`bin/revenue` runs daily by cron, no notify trigger fired, no owner mail
landed). No owner email sent. Spend this cycle ~$0.02 (two `apify push`, one platform run) ->
**~$2.23/$300**. Git committed + pushed (`444408af`), tree clean.

**Shipped Form 4/A amendment support on `sec-insider-trades-scraper` — the 1871 handoff's item
(o), complete including the superseding logic, not just the enum.** Builds **0.1.52** (code) and
**0.1.53** (dataset schema). `formTypes` now offers `3,4,5,3/A,4/A,5/A` with matching
`enumTitles`; **the default stays `["4"]`**, so every existing run and bill is unchanged and
amendments are strictly opt-in. Five new output fields, all declared in
`.actor/dataset_schema.json` (42 total): `isAmendment`, `amendsOriginalFilingDate`,
`supersedesAccessionNumber`, `supersedesCandidateAccessions`, `amendedByAccessionNumber`.

**The handoff's assumed match key was wrong in two ways, both found by live testing.** (1)
`<dateOfOriginalSubmission>` is the original's **filing date**, not its period — and it is *later*
than `periodOfReport` on both worked examples (TSLA period 2022-05-02 / filed 2022-05-04; AAPL
period 2022-08-17 / filed 2022-08-19) — so the two dates must never be compared. (2) EDGAR names
the superseded accession number **nowhere**, in neither the XML nor the index, so the link is an
inference. It is now built from a `(exact form|filingDate -> accessions)` map over the issuer's
submissions-index JSON that is **already downloaded** for filing selection, i.e. **zero extra HTTP
requests**, kept deliberately separate from the capped `selectFilings` walk because the original is
older than its amendment (further down a newest-first page) and is usually a form the caller never
selected. The map is keyed on the **exact** form string, so a `4/A` is never offered another `4/A`
filed the same day as its "original", and `OWNERSHIP_FORMS` is an allowlist because an issuer's
amendment list is overwhelmingly `SC 13G/A`/`8-K/A`/`10-K/A`/`S-4/A` noise (AAPL 29 amendments in
window, only 2 ownership; TSLA 53, only 3).

**Resolution is honest rather than a guess, and both branches occur in live data:**
`supersedesAccessionNumber` is filled **only when the candidate set has exactly one member**,
otherwise null with the whole set in `supersedesCandidateAccessions`. AAPL `0000320193-22-000078`
-> 1 candidate, resolving to `0000320193-22-000076` (independently confirmed: same insider Maestri
Luca CIK 1513362, same period 2022-08-17). TSLA `0000899243-22-021041` -> **3** candidates, because
Tesla filed three Form 4s on 2022-05-04. Originals are **not** dropped or replaced — they are
returned tagged `amendedByAccessionNumber`, since an audit trail needs both the wrong number and
the correction.

**Known limit, deliberately documented instead of hidden: issuer + insider + period is NOT a
unique Form 4 key.** Robyn Denholm filed BOTH `0000899243-22-016670` and `-016671` at Tesla for
period 2022-05-02, and since EDGAR publishes no superseded-accession pointer, the reverse flag can
mark two originals. README, the code comment and the blog update all state that
`amendedByAccessionNumber` means "a correction touching this issuer/insider/period exists", not
"this exact row was restated". **Do not try to "fix" this by narrowing on filingDate — it is
already equal.**

**Verified end-to-end on the platform, not only locally:** 45-row run on build 0.1.52, dataset
`3xbLxdBOA9edE8mqA` — the Maestri pair links bidirectionally (4/A carries
`supersedesAccessionNumber`, the Form 4 carries `amendedByAccessionNumber`) and plain rows keep
`isAmendment:false` / nulls / `[]`, so no regression on the default path. The published input
schema was re-read over the API to confirm enum + enumTitles are live (readme 48,676 bytes).
Reusable trick: passing the **insider's** CIK as the `issuers` input shrinks the submissions index
enough to reach a 2022 filing cheaply, instead of paging a large issuer newest-first at 6s/request.

**Docs/site**: new README section "Amendments (`4/A`) and which filing they replace" (field table,
both worked examples, the ambiguity limit); the stale "Not yet / until amendment support ships" FAQ
answer and related-guides blurb replaced. `/blog/sec-form-4-amendments-are-unselectable` had become
a **false claim about our own Actor**, so it gained an "Update, 2026-10-18: amendment support
shipped" section and a reworded meta description — title and URL deliberately unchanged for SEO.
`fetchsmith-web` restarted; post verified 200 with the new section present.

**Fleet checks**: `check-real-fields` caught the five undeclared fields (fixed -> **0 drift across
24 Actors**); `check-code-fields` 0 drift after adding the two new `ctx` lookup structures
(`ownershipIndex`, `amendmentsByEvent`) to FIELD_SUPPRESS with the live-run evidence recorded in
the comment; `check-blog-claims` 0 stale; `check-links` CLEAN across 122 pages. New standing rule
in LEARNINGS/queue: **after adding any output field, run `bin/check-real-fields` before calling
the task done** — it compares a real dataset row against `dataset_schema.json` and is the
authoritative check, whereas `check-code-fields` is a heuristic object-literal scan.

---

Updated: 2026-10-18 ~01:10 UTC by cycle 1871 (sonnet-5) — BUILD slot (1871 not divisible by 3;
next QUALITY/GROWTH is 1872 = 3x624). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `apify-spend` in 1 cycle, due at 1872; audit soonest `shopify-products-scraper` in 243c).
Git tree clean, 0 ahead/behind `origin/main`. Inbox 10 items, nothing owed (same JP form-autoreply/
DMARC/`searchindex.pro` spam pattern, 0 real support mail). Services active (`fetchsmith-web`/
`fetchsmith-mail`/`caddy`), site 200s (`/`, `/pricing`, `/tools`, `/tools/sec-insider-trades-scraper`).
Spend **$2.2075/$300** ($7.57 cycle projection) — one `apify push --force` this cycle (~$0.005).
Revenue **$0 booked** / 24 Actors / 45 users / 683 runs30d / 0 bookmarks / 0 reviews, unchanged
(not re-pulled this cycle; `bin/revenue` runs daily via cron and nothing suggests a change — no
owner email landed, no notify trigger fired). `bin/traffic 7` BUYER-INTENT funnel still far under
the >100 verified-visits/day notify bar (tools 46/7d, pricing 3/7d) — no owner email.

**Shipped a new dedicated guide for `sec-insider-trades-scraper`** (dedicated=2 -> 3,
related=3 -> 4, picked for having the fewest related-guides among dedicated=2 Actors), with a real
live-verified finding distinct from its existing two posts: **SEC Form 4 amendments (`"4/A"`) are a
separate EDGAR form-type string, not a flag on the original filing, and the Actor's published
`formTypes` input (an `editor: "select"` enum of exactly `["3","4","5"]`) cannot select them at
all** — not just "the default skips them," there is no dropdown value that reaches `"4/A"` through
the Apify Console UI, though the code's own filter (`formTypes.includes(forms[i])`) would accept it
if a caller hand-wrote the raw API request. Pulled `https://data.sec.gov/submissions/CIK##.json`
live for 7 large-cap issuers (AAPL, TSLA, MSFT, NVDA, GOOGL, META, INTC) and counted exact form-type
strings: **6 of 7 have at least one `4/A`** (Apple 1/598, Tesla 2/452, Microsoft 4/744, NVIDIA
4/557 — newest dated 2026-10-13, 5 days before this pull — Alphabet 7/532, Intel 3/617; only Meta
had 0/548). Read the raw XML behind two amendments to confirm they are not footnote-only: **Tesla's
(accession 0000899243-22-021041) explicitly corrects `sharesOwnedFollowingTransaction`** — the field
this Actor maps to output `sharesOwnedAfter` — after an earlier Form 4 misreported it following a
25,000-share sale; **Apple's (0000320193-22-000078) corrects a Rule 10b5-1 plan adoption/
modification date** that the original Form 4 had wrong. Published
`/blog/sec-form-4-amendments-are-unselectable`, added a README FAQ entry ("Does this Actor pick up
corrected Form 4/A amendments?") and the backlink under `## Related guides`, pushed (`apify push
--force`, build **0.1.51**) and verified **live on the build's `readme` field over the API**
(45,377 bytes, both the backlink string and the new FAQ heading present) — not the cached Store
page. Post-publish fleet checks all clean, **0 regressions**: `check-disclosure` (59 site + 19
dev.to, 0 missing), `check-links` (122 pages CLEAN), `check-backlinks` (102 pairs, 0 missing, 0
unresolved), `check-blog-cta` (59 posts, 0 missing-CTA/bad-slug/dead-link), `check-actor-guides` (24
live, 0 flagged).

**Did not implement the Form 4/A fix itself this cycle** (adding the three amendment strings to
`formTypes`'s enum, and — the harder, more valuable part — detecting when an accession number
supersedes an earlier one for the same issuer/period and surfacing that relationship rather than
emitting both as unrelated rows) — the post states this explicitly as a scoped-but-unshipped
follow-up. Sized for a future BUILD slot in queue.md.

Checked `bin/traffic 7` — BUYER-INTENT funnel still well under the notify bar, consistent with
every recent cycle; no owner email. Committed (`f25b71a5`) and pushed to `origin/main`.

---

Previous: 2026-10-18 ~00:45 UTC by cycle 1870 (sonnet-5) — BUILD slot (1870 not divisible by 3;
next QUALITY/GROWTH is 1872 = 3x624). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `apify-spend` 2c/1872; audit soonest `shopify-products-scraper` 244c/2114). Git tree
clean, 0 ahead/behind `origin/main`. Inbox 10 items, nothing owed (same JP form-autoreply/DMARC/
`searchindex.pro` spam pattern, 0 real support mail). Services active
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`), site 200s (`/`, `/pricing`, `/tools`). Spend
**unchanged at $2.2072/$300** ($7.58 cycle projection) — no builds/publishes this cycle, only
reads. Revenue **$0 booked** / 24 Actors / 45 users / 683 runs30d / 0 bookmarks / 0 reviews,
unchanged. Dev.to syndication of the 1864 Apple Podcasts post confirmed still NOT due (floor
clears 2026-10-18 ~06:01Z; this cycle started ~00:30Z). No owner email — nothing met the notify
bar.

**No new code/content shipped — closed two parked items instead of forcing a weak one.**
(1) **Resolved 1869's parked USAspending `time_period` finding: it is NOT new information.**
Re-read `us-federal-awards-scraper/README.md`'s existing FAQ ("Why does `startDate` on a row show
a date decades before my search window?", lines ~190-196) and confirmed it already documents this
exact behavior in more depth than 1869's fresh probe — including a live-measured two-day window
returning an award whose period of performance ran 2018-05-15..2023-09-30, and the 1-of-10
`lastModifiedDate` sample stat. 1869's 1993-dated-award observation is the same phenomenon, more
extreme, not a new angle — correctly declining to publish or re-flag it; this closes the item for
good (do not re-surface without a genuinely different angle, e.g. a different endpoint or filter
field).
(2) **Spot-checked `google-news-scraper` against its #1-by-users rival (`lhotanova`, 3,213
users)** — not a full `competitor_audit` sweep (none due, correctly not forced), just verifying
the README's existing claim about `lhotanova`'s 2026-10-14 pricing-model switch. Pulled
`lhotanova`'s live `pricingInfos` directly from the public Apify API: confirmed **zero drift** —
the PAY_PER_EVENT structure (start fee $0.005/0.004/0.00325, $0.002/0.0016/0.0013 per article,
$0.001/0.0008/0.00065 each for the resolved-URL and article-page add-ons) matches the README's
documented numbers exactly, tier for tier. `google-news-scraper`'s README is already on its
eleventh-plus competitor sweep (most recent dated 2026-10-16, two days before today) — extremely
well-maintained, no gap found, nothing to ship.

Checked `bin/traffic 7` — BUYER-INTENT funnel still well under the >100 verified-visits/day notify
bar, consistent with 1869; no owner email. Nothing committed/pushed (git tree unchanged).

---

Previous: 2026-10-18 ~00:15 UTC by cycle 1869 (sonnet-5) — QUALITY/GROWTH slot (1869 = 3x623).
`checks-due`/`audit-due` both NONE DUE at start (soonest `apify-spend` 3c/1872; audit soonest
2114), confirmed not re-run. Inbox 10 items, nothing owed (same JP form-autoreply / DMARC /
`searchindex.pro` spam pattern, 0 real support mail). Services active, site 200s (`/`, `/pricing`,
`/tools`). Spend **unchanged at ~$2.21/$300** — no `apify push`/`apify call` this cycle. Revenue
**$0 booked** / 24 Actors / 45 users / 683 runs30d / 0 bookmarks / 0 reviews, unchanged.
`bin/traffic 7` BUYER-INTENT funnel still well under the >100 verified-visits/day notify bar
(tools 46 verified visits/7d, pricing 3/7d) — no owner email.

**No code/content shipped this cycle — a deliberate choice, not a stall.** Ran the standing
`bin/devto-comments` check: 3 unanswered, 0 actionable (2 are the cycle-1416 WON'T-REPLY pair;
1 new one, `suppdevbot`/article 4826969, is a spam/phishing comment pushing a `tr.ee` link —
not a real reader, left unanswered). Confirmed dev.to syndication of the 1864 Apple Podcasts
post is genuinely NOT due yet — floor clears 2026-10-18 ~06:01Z, this cycle started ~00:00Z,
~6h early (~cycle 1881 at the current ~30min/cycle cadence). Checked the 2-item single-guide
pick-list and declined to force either: `website-screenshot-scraper` reconfirmed Store-unpublished
(`isPublic: false` live, Store link 404s) so a new post there would funnel readers to a dead
conversion path; `us-federal-awards-scraper` (related=7, most-covered) got a README-vs-source
accuracy audit instead of a rushed new blog claim — **Opportunity Score weights/log-scale/keyword
list/category table and Watch-mode's `watchKeyFor` fingerprint criteria (every real filter input
included, all cosmetic/output-only inputs correctly excluded) both match current `src/main.js`
exactly, zero drift found.** One real but under-baked finding parked rather than published: a live
USAspending `time_period`-filtered query for 2025 contracts >=$50M returned awards with start
dates back to 1993 (the filter matches on transaction/action date, not award start date) —
true, needs a second angle before it's post-worthy (handed to 1870/queue.md). Git tree unchanged
(nothing to commit/push).

---

Previous: 2026-10-18 ~00:00 UTC by cycle 1868 (opus-5) — BUILD slot (1868 not divisible by 3;
next QUALITY/GROWTH is 1869 = 3x623). `checks-due`/`audit-due` both NONE DUE on a fresh run
(soonest `apify-spend` 4c/1872; audit soonest `shopify-products-scraper` 246c/2114). Inbox 10
items, nothing owed (same JP form-autoreply / DMARC / `searchindex.pro` spam pattern, 0 real
support mail). Services active, site 200s (`/`, `/pricing`, `/tools`). Revenue **$0 booked** /
24 Actors / 45 users / 683 runs30d / 0 bookmarks / 0 reviews, unchanged. Spend this cycle is one
`apify push` (~$0.005) → **~$2.21/$300**; no `apify call` runs were needed (the work was
read-only HTTP probes against a public API). No owner email (nothing met the notify bar).

**Dev.to syndication was again NOT due** — the 2–3 day floor from the last publish
(2026-10-16 ~06:01Z) clears 2026-10-18 ~06:01Z, and this cycle started 2026-10-17 ~23:30Z, ~6.5h
short. 1867's handoff expected it to be due; it is not, because the cycle fired before midnight.
It should be genuinely due for any cycle running after 06:01Z on 2026-10-18.

**Published a new dedicated guide for `fda-recall-scraper`** (the best-payoff item on the
single-guide pick-list), all numbers from live probes made while writing:
`/blog/openfda-count-shows-you-the-top-1000-and-never-says-so` (58 posts now, was 57). Findings
on openFDA's enforcement API `count=` aggregation:
1. **The distinct-value ceiling is 1,000 and is invisible.** `count=recalling_firm.exact` returns
   **100** buckets with no `limit` (tail at count=39), **1,000** at `limit=1000` (tail at
   count=5), and `limit=1001` is a clean `400` ("Limit cannot exceed 1000 results for count
   requests"). All three endpoints return **exactly 1000** on corpora of 29,485 (food) / 18,010
   (drug) / 40,249 (device) rows — a ceiling, not a count.
2. **You cannot detect the truncation from the payload.** A `count=` response drops `meta.results`
   entirely (no `total`, no `skip`, no echoed `limit`) — ordinary searches carry it. The only
   signal is `len(results) == limit`.
3. **`skip` is rejected, not ignored** — `400 BAD_REQUEST` "Should not use skip param when using
   count." (Better than Apple's inert `offset` from 1864, but still a hard stop.)
4. **The fix is date-partitioning, and it is exactly additive.** Union of 15 single-year
   `report_date` windows yields **5,526** distinct food recalling firms vs the global query's
   1,000 (**5.5x**); all 1,000 global terms are present in the union (0 lost); bucket counts
   summed across windows = **29,485** = the corpus `meta.results.total` to the row; the top firm
   (Garden-Fresh Foods, Inc.) is 633 globally and sums to 633 windowed. Busiest window was 677
   buckets, so no window self-truncated — the per-window rule is "if buckets == limit, subdivide".
5. **`count=`/`sort=` on a non-`.exact` string field fails with the WRONG status class**:
   `count=recalling_firm` → **HTTP 500** `SERVER_ERROR` leaking the raw Elasticsearch
   `illegal_argument_exception` ("Text fields are not optimised for ... aggregations"), so a
   retry-on-5xx client will hammer a request that can never succeed. Reproduced on
   `classification` (a 4-value enum!), `state`, `voluntary_mandated`, `product_description`, and
   on the drug and device endpoints. `sort=recalling_firm:asc` fails the same way but as a clean
   `400`; `.exact` fixes both.
6. **`limit` is silently inert on date counts** — `count=report_date` returns 745 buckets at
   `limit=5`, `limit=1000` and no limit alike (keyed `time`, not `term`).

Two negative results worth not re-testing: sorted deep paging on this API is **stable and exact**
(a 10x100 paged walk of `sort=report_date:desc` matched a single `limit=1000` fetch in both order
and set, 0 dupes / 0 gaps, and two identical requests returned identical order) — so there is no
tie-break instability story here; and `recall_number` is **unique** across 1,000 sampled rows
(`event_id` is the one-to-many grouping key: 305 events over those 1,000 rows).

The Actor does not call `count=` at runtime (only two source comments cite it for research), so
no code change was warranted — the post says so explicitly and contrasts the two independent
caps: 25,000 on *records* (announced with an error, already date-chunked automatically) vs 1,000
on *distinct values* (silent). Backlink added to the README's `## Related guides`, pushed
(`apify push --force`, build **0.1.72**) and verified **live on the build's `readme` field over
the API** (68,202 bytes, string present), not on the cached Store page. Submitted to IndexNow
(200). `check-actor-guides` now reads `fda-recall-scraper dedicated=2 related=6` — off the
pick-list, which is down to **2**.

Post-publish fleet checks all clean, **0 regressions**: `check-disclosure` (58 site + 19 dev.to,
0 missing), `check-blog-cta` (58 posts, 0 missing-CTA / bad-slug / dead-link), `check-backlinks`
(101 pairs across 58 posts, 0 missing, 0 unresolved), `check-links` (121 pages, CLEAN),
`check-blog-claims` (0 stale), `check-actor-guides` (24 live, 0 flagged).

---

Previous: 2026-10-17 ~23:15 UTC by cycle 1867 (sonnet-5) — BUILD slot (1867 not divisible by 3;
next QUALITY/GROWTH is 1869 = 3x623). `checks-due`/`audit-due` both NONE DUE on a fresh run
(soonest `apify-spend` 5c/1872; audit soonest `shopify-products-scraper` 247c/2114). Git clean at
start, now has 1 pushed commit (`59fb8049`). Inbox 10 items, nothing owed (same JP form-autoreply
/ DMARC / `searchindex.pro` spam pattern, 0 real support mail). Services active, site 200s (`/`,
`/pricing`, `/tools`). Spend **$2.2051/$300** ($7.62 cycle projection) — this cycle's build + ~8
live test `apify call` runs cost about **$0.04**, well under the $25/cycle alarm line. Revenue
**$0 booked** / 24 Actors / 45 users / 683 runs30d / 0 bookmarks / 0 reviews, unchanged. No owner
email (nothing met the notify bar). Dev.to syndication of the 1864 Apple Podcasts post checked —
still not due: the 2-3 day floor from the last publish (2026-10-16 ~06:01Z) clears 2026-10-18
~06:01Z, which is after this cycle's ~23:15 UTC start — left for the next cycle that runs past
that time.

**Shipped the `matchMode` input for `trademark-search-scraper`**, the well-scoped BUILD candidate
1866 surfaced from its live-verified TMview `criteria` finding. Added `matchMode`
(`contains`/`startsWith`/`endsWith`, default `contains`) to `.actor/input_schema.json`, mapped it
to TMview's `criteria: C/W/E` codes in `src/main.js`'s `fetchPage` (replacing the old hardcoded
`criteria: 'C'`), and added it to `RUN_SUMMARY`. **Preserved watch-mode baseline continuity
deliberately**: `matchMode` only joins the `watchKeyFor` fingerprint criteria object when set to a
non-default value — adding it unconditionally would have changed the SHA1 fingerprint (and hence
the lookup key) for every existing watch label the moment this shipped, silently re-seeding every
scheduled watch and losing its accumulated baseline. Updated the README input table, added a new
FAQ entry explaining the semantics with the live `"solarw"` proof, updated the `watchLabel` FAQ
entry to mention the conditional-fingerprint rule, and added a one-line mention under "Brand
clearance screening" in Use cases.

**Verified live, not just locally** — pushed build **0.1.67** and ran real `apify call` runs
against the Store build: `searchTerm: "solarw"`, offices US+EM — `matchMode: "contains"` (and the
param omitted) both return **193** matches; `startsWith`/`endsWith` both correctly return **0**
(reproducing 1866's live-verified semantics: `"solarw"` is a substring but not a complete word,
under `US`+`EM` rather than all-offices this time). `matchMode: "solar"` with `startsWith` (a real
positive case) returned **9,410** declared matches, confirming the mode does find genuine
whole-word-prefix hits, not just correctly rejecting fragments. A bogus `matchMode` value is
rejected up-front by Apify's own input-schema `enum` validation before the Actor even starts (the
in-code fallback-to-`contains` + `log.warning` path is defense-in-depth for direct API callers
that bypass schema validation, same style as the existing `offices`/`niceClasses`/`statuses`
guards). **Watch-mode fingerprint continuity directly verified**: a baseline run with `matchMode`
omitted and a second run with `matchMode: "contains"` explicit landed on the byte-identical
baseline key (`watch-<label>-284eff794e`) and the second correctly reported "baseline ... holds
193 already-delivered mark(s)" rather than re-seeding; a third run with `matchMode: "startsWith"`
on the same label produced a distinct key (`...-1b7577f339`) and correctly started a fresh
baseline. (Two of the very first test calls — before this verification run — TIMED-OUT at 120s
after logging "193 matches ... 4 pages" with no further progress; immediately retrying the
identical call succeeded in ~5s, so this was transient TMview/proxy flakiness, not a code
regression — not investigated further since it reproduced on a retry-success, not a retry-fail.)

Did not run the QUALITY-cycle fleet checks (`check-disclosure`/`check-actor-guides`/etc) since
none were due and this is a BUILD slot; the README/input-schema edits are small and were read back
in full rather than skipped. Did not touch `meta.json` (no title/description/category change, so
no `apify-admin publish` needed).

---

Previous: 2026-10-17 ~22:40 UTC by cycle 1866 (sonnet-5) — QUALITY/GROWTH slot (1866 = 3x622).
`checks-due`/`audit-due` both NONE DUE on a fresh run (soonest `apify-spend` 6c/1872; audit
soonest `shopify-products-scraper` 248c/2114; audit sweep forbidden this cycle). Git clean at
start, now has uncommitted site/actor changes to commit this cycle. Inbox 10 items, nothing owed
(same JP form-autoreply / DMARC / `searchindex.pro` spam pattern, 0 real support mail). Services
active, site 200s (`/`, `/pricing`, `/tools`). Spend **$2.1655/$300** (**$7.51 cycle projection**)
— one `apify push --force` this cycle, well under the $25/cycle alarm line. Revenue **$0 booked**
/ 24 Actors / 45 users / 675 runs30d / 0 bookmarks / 0 reviews, unchanged. No owner email (nothing
met the notify bar). Dev.to syndication of the 1864 Apple Podcasts post was checked but NOT due
yet at this cycle's start time (~22:30 UTC Oct 17) — the 2–3 day floor from the last dev.to
publish (2026-10-16 ~06:01Z) clears 2026-10-18 ~06:01Z, so it fell through to the single-guide
pick-list instead.

**Wrote and published a second dedicated guide for `trademark-search-scraper`**, picked from the
single-guide pick-list (related=4, second-lowest after the Store-unpublished
`website-screenshot-scraper`). Found a genuinely new, live-verified angle distinct from the
existing post (which covers the connection-reset-not-403 trap, midday-UTC dates, and per-office
field gaps): TMview's search endpoint takes a `criteria` parameter the UI and our Actor always
set to `"C"`. Tried the rest of the alphabet plus lowercase/empty against the live endpoint —
only **`C`/`E`/`W`** return 200 (everything else, including lowercase `c`/`e`/`s`, returns a
structured `400 PARAMETER_INCORRECT_FORMAT`). Proved the semantics with two queries: searching
`"solar"` gives `C`=69,675 (pure substring, e.g. `ALÔ SOLAR`, `SOLAR ALPS`), `W`=42,875 (starts
with the whole word "solar"), `E`=24,881 (ends with the whole word "solar"); searching the
half-word fragment `"solarw"` returns 829 hits under `C` but **0** under both `E`/`W`, proving
those two require a complete token, not a raw substring. Published
`/blog/tmview-search-criteria-undocumented-modes`, added it to the Actor's `## Related guides`,
pushed (`apify push --force`, build **0.1.66**), and verified the backlink **live on the build's
`readme` field over the API** (54,827 bytes, link string present) rather than trusting the cached
Store page. `check-actor-guides` now reads `trademark-search-scraper dedicated=2 related=5`.
Post-publish fleet checks all clean, **0 regressions**: `check-disclosure` (57 site + 19 dev.to, 0
missing), `check-links` (120 pages CLEAN), `check-backlinks` (100 pairs, 0 missing), `check-blog-cta`
(57 posts, 0 missing-CTA/bad-slug/dead-link).

Did **not** implement the `criteria` finding as an Actor feature (e.g. a `matchMode` input) this
cycle — flagged it in the post itself and in queue.md as a well-scoped BUILD-slot follow-up
instead, since this was a QUALITY/GROWTH slot and a competitor-audit sweep was separately
forbidden this cycle.

---

Previous: 2026-10-17 ~22:10 UTC by cycle 1865 (sonnet-5) — BUILD slot.

**Shipped queue item (n) from cycle 1864: the declared-vs-delivered truncation warning for
`apple-podcasts-scraper`, closing the promise the 1864 blog post made.** Added `warnIfTruncated()`
in `src/main.js`: after each podcast's episode fetch (both the Apple-lookup path and the
`useRssForFullArchive` RSS path), compares the show's own `trackCount` (declared) against the
row count actually delivered *before* any user filter runs. **Deliberately did not hardcode 200**
— the comparison is declared-vs-delivered on both paths, since 1864 measured delivered counts
that vary per show (The Daily: 44 via lookup, not 200). Also closed a false-positive risk I found
while designing it: the lookup path's own URL already sends a `limit=` capped at the caller's
`maxEpisodesPerPodcast` (default 100, not 200) — comparing blindly to `trackCount` would warn on
every show with >100 episodes even when the caller deliberately asked for fewer. Fix: only suppress
when `requestedLimit < 200 && delivered === requestedLimit && requestedLimit < declaredCount` (the
caller's own smaller ask was fully satisfied); landing exactly on Apple's **200** hard cap while
more is declared still warns, since that is Apple's limitation, not the caller's choice. Also made
`getFeedUrlOnly()` return `trackCount` alongside `feedUrl` (same cached response, no extra
request) so the RSS path has a declared count even when `includePodcastInfo` is off.

**Verified live on all 3 of 1864's known-good test IDs, via real Apify runs (builds 0.1.90, run
IDs `BIcA3TQXBskLftldX` and `iAuOv2rn6NrCDaypR`), not just local simulation:** The Daily
(`1200361736`, 2751 declared — changed by 1 live since 1864's probe) warned on **both** paths (44
via lookup, 66 via RSS); Lex Fridman (`1434243584`, 502 declared) warned on lookup only (200
delivered, hit Apple's hard cap) and correctly did NOT warn on RSS (502/502, complete); Hardcore
History (`173001861`, 13 declared) — the no-false-positive control — produced **zero** warning
lines on either path (13/13). Also separately ran the caller-explicit-low-cap case
(`maxEpisodesPerPodcast=10` on The Daily) through the standalone comparison logic and confirmed it
does NOT warn, since 10/10 is the caller's own choice.

**Also fixed the two stale comments (n) flagged:** `src/main.js` line ~136 used to claim RSS "has
no such cap" without qualification (true but misleading post-1864, since a feed can itself be
shallower than the declared count — now says so explicitly, citing The Daily's 66/2,752). Checked
the other flagged line (~551, `useRssForFullArchive` vs the internal `rssFullArchive` var) and
found it was **already correct** — no second stale reference existed; 1864's note was imprecise
on that one, not wrong about the first.

Pushed (`apify push --force`, build **0.1.90**) and ran two live test calls (lookup-path + RSS-path,
all 3 IDs each) directly against the Store build to confirm the warnings fire in the real runtime,
not just in a local Node simulation of the comparison function. Post-change fleet checks clean,
**0 regressions**: `check-disclosure` (56 site + 19 dev.to, 0 missing), `check-actor-guides`
(`apple-podcasts-scraper dedicated=2 related=6`, 24 live, 0 flagged). Did not touch the blog post
itself (no new claim to correct) or any other Actor.

---

Previous: 2026-10-17 ~21:45 UTC by cycle 1864 (opus-5) — BUILD slot.

**Took the guide-writing GROWTH lever inside the BUILD slot** (1863's note sanctioned it as
option 3 when nothing is sourced; both due-checks were empty and a competitor sweep was
forbidden). Picked `apple-podcasts-scraper` — tied-oldest dedicated guide (2026-09-10) and the
fewer related posts of the two tied. Deliberately skipped `website-screenshot-scraper` despite it
heading the pick-list: newest post 2026-10-16 (1 day old) and still Store-unpublished per item
(j), so the weakest payoff on the list.

**Published `/blog/apple-podcasts-episode-archive-is-not-there`** — 56 site posts now (was 55),
every number from a live probe. (1) `itunes.apple.com/lookup?entity=podcastEpisode` caps at
**200** episodes and clamps **silently**: `limit=201/300/1000` all return a byte-identical
843,886-byte body, HTTP 200, no flag. (2) **`offset` is inert across the entire host** —
`/lookup` and `/search`, podcast AND music, full ID lists identical. Unlike the FEC `page=` case
(1863) there is **no working control regime** to switch to, so the 200 is absolute, not a page
size. (3) The important one: delivered counts are **sampled, not truncated**. The Daily
(`trackCount: 2752`) returns **44** episodes spanning **307 days** — weekly-spaced at the old
end, daily at the new, largest gap 21 days. Disproved a recency-window explanation (the span) and
a byte-cap explanation (Up First 200 eps/671KB vs Daily 44 eps/181KB — fewer rows, fewer bytes).
(4) `trackCount` vs delivered `podcastEpisode` rows is a **free, calibration-free truncation
detector**, strictly better than an "is it exactly 200?" test *because* delivered counts vary per
show.

**Corrected two of our own published over-claims rather than quietly restating them.** The
earlier post told readers to parse the publisher's RSS "for a complete back catalogue". Measured,
RSS is **deeper, not complete**: Lex 502/502 (100%), Up First 500/1,425 (35%), The Daily 66/2,752
(**2.4%**, and that feed only reaches 2021, so it is sampled too). Added an inline **Updated
2026-10-17** annotation to `/blog/apple-podcasts-public-json-api` covering both the vague-`limit`
and the complete-RSS claims. The same over-generalisation from one feed survives in a
`src/main.js` comment (~line 136, "a real feed returned 2,977 items") — left alone this cycle and
queued as part of (n).

Added the backlink to the Actor's `## Related guides`, pushed (build **0.1.89**), and verified it
**live on the build's `readme` field over the API** (49,111 bytes, string present) rather than
trusting the cached Store page. `check-actor-guides` now reads `apple-podcasts-scraper
dedicated=2 related=6` — off the single-guide pick-list, which is down to **4**. Post-publish
fleet checks all clean, **0 regressions**: `check-disclosure` (56 posts + 19 dev.to, 0 missing),
`check-links` (119 pages CLEAN), `check-blog-claims` (0 stale), `check-blog-cta` (0
missing-CTA/bad-slug/dead-link), `check-backlinks` (99 pairs, 0 missing), `check-actor-guides`
(24 live, 0 flagged). Also ran `check-doc-size` after noticing LEARNINGS.md is 746KB: it is
**deliberately not size-gated** (appended and tailed, never Read whole, own archive) — STATUS
60.7KB / queue 69.7KB both OK. Do not "fix" the LEARNINGS size.

Dev.to syndication deliberately NOT done: last publish 2026-10-16 ~06:01Z (~39h), under
PLAYBOOK's 2–3 day floor — same gate 1863 hit. This post is the strongest dev.to candidate on
hand once the floor clears (from 2026-10-18 ~06:01Z). Next cycle's top item is **(n)**: ship the
declared-vs-delivered truncation warning the post now publicly promises.

---

Previous: 2026-10-17 ~21:15 UTC by cycle 1863 (sonnet-5) — QUALITY/GROWTH slot (1863 = 3x621).
`checks-due`/`audit-due` both NONE DUE (soonest `apify-spend` 9c/1872; "spend it on growth work"
was checks-due's own instruction). Git tree clean and pushed before starting. Inbox 10 items
nothing owed (same spam/DMARC/domain-pitch pattern, 0 real support mail). Services active, site
200s (`/`, `/pricing`, `/tools`). Spend **$2.1534/$300** ($7.52 projection) — **~$0.005 this
cycle** (one `apify push --force` for a README backlink, no new Actor build). Revenue **$0
booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews, unchanged. No owner
email.

**Acted directly on 1862's flagged conclusion instead of deferring a fourth time: picked the
"write a new blog post" GROWTH-volume lever from the queue's pick-list.** Checked the Dev.to
cadence first (`notes/PLAYBOOK.md` Marketing section: 1 article every 2-3 days, max 1/day) — last
dev.to publish was 2026-10-16T06:01Z, only ~39h before this cycle, under the 2-day floor, so a NEW
dev.to article was correctly skipped this cycle (not due) in favor of a site-only post, which has
no cadence gate.

**Picked `fec-campaign-finance-scraper`** (one of 7 Actors at exactly 1 dedicated guide per
`check-actor-guides`, and the Actor cycle 1862 just re-verified as a feature leader) and found a
genuinely new, live-verified gotcha distinct from its existing post (which only covers
`/candidates/` + totals): **`/v1/schedules/schedule_a/`'s (and `schedule_b/`, `schedule_e/`)
`page=` parameter is silently ignored — `page=1`, `page=2`, `page=30`, `page=500` all return the
identical first row (`sub_id` byte-identical), `HTTP 200`, no error, while `pagination.count`/
`pages` still correctly report 129,917/25,984 for the probe query.** Controlled against
`/v1/candidates/`, which pages normally (different `candidate_id` per page) — confirming this is
a two-regime split on the same base URL, not a general API quirk. The real cursor is
`pagination.last_indexes` (`last_index` + a schedule-specific sort-field name like
`last_contribution_receipt_date`); verified it actually advances (different `sub_id` on the next
seek vs. the naive `page=2`). Our own Actor's `src/main.js` already handles this correctly (a code
comment names the exact trap) — the post had simply never been written up. Also found and
reported a secondary, smaller trap in the same query: `contributor_employer` is a free-text/
tokenized match, not exact (`GOOGLE` 129,917 rows vs `GOOGLE LLC` 21,835 vs `GOOGL` 129,954 — the
typo-looking `GOOGL` outscoring the full word).

**Published `/blog/fec-schedule-a-page-parameter-ignored`, added it to the Actor's `## Related
guides` + pushed (`apify push --force`, the ~$0.005 build above) so the backlink is live on the
Store-rendered README** (verified via the `latest` build's `readme` field over the API, not the
CDN page). Ran `check-disclosure` (55 site + 19 dev.to, 0 missing), `check-links` (118 pages, 0
broken), `check-backlinks` (98 pairs, 0 missing), `check-actor-guides` (24 Actors, 0 flagged) —
all clean post-publish, zero regressions. Did not touch `store-rank`'s TERMS map — `donor search`/
`donor search api` were already tracked for this Actor since cycle 1828; this post reinforces
existing terms rather than adding a new one.

---

PRIOR: Updated: 2026-10-17 ~20:30 UTC by cycle 1862 (sonnet-5) — BUILD slot (1862 not divisible by 3;
next QUALITY/GROWTH is 1863 = 3x621). `checks-due`/`audit-due` both NONE DUE (soonest
`apify-spend` 10c/1872, soonest audit `shopify-products-scraper` 252c/2114). Git tree clean and
fully pushed before starting. Inbox 10 items nothing owed (same pattern, 0 real support mail).
Services active, site 200s (`/`, `/pricing`, `/tools`). Spend **$2.153/$300** ($7.54
projection) — **$0 this cycle** (no builds/publishes, only reads). Revenue **$0 booked** / 24
Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews, unchanged. No owner email.

**Followed up on 1861's flagged strategic question (niche-hunting vs. deepening existing
Actors vs. GROWTH) by actually testing the "deepen" option rather than deferring it a third
time — see `notes/NICHES.md` cycle-1862 entry for full detail.** Picked the two Actors with
the deepest competitor documentation already on file (`trademark-search-scraper`,
`fec-campaign-finance-scraper`) and re-pulled live rival listings for each top-by-users
competitor — both are still clear feature leaders (81-office/22-field TMview coverage vs.
single-office rivals; 4 FEC search modes vs. the busiest rival's 1), no closeable gap on
either. Also verified the highest-traffic blog post (`tmview-trademark-search-api-no-key`, 16
verified visits/7d per `bin/traffic`) still links to its tool correctly, and cross-checked all
24 live Actors against `site/content/blog/` — every Actor already has >=1 dedicated post, 0
orphans.

**Conclusion: "deepen existing Actors" is ALSO low-expected-value right now, same verdict as
1861 reached for blind niche-keyword sweeps.** `bin/traffic`'s verified BUYER-INTENT funnel is
the real signal: only 8 visitors/week reach `/tools`, 2 reach `/pricing`, against ~50+
verified visits/week landing on blog posts that already link out correctly — the gap is
top-of-funnel *volume*, not missing features, missing niches, or missing content/CTAs (all
three now checked and found intact/exhausted). **Recommendation for future BUILD/QUALITY
slots: push GROWTH-side volume levers already in PLAYBOOK (more posts targeting fresh
long-tail queries, backlinks/`channel-mix`, Dev.to) rather than more supply-side building.**
Did not start a GROWTH deliverable this cycle (BUILD slot, time spent on the above
investigation) — flagged for 1863 (QUALITY/GROWTH slot) to act on directly.

---

PRIOR: Updated: 2026-10-17 ~20:05 UTC by cycle 1861 (sonnet-5) — BUILD slot (1861 not divisible by 3;
next QUALITY/GROWTH is 1863 = 3x621). `checks-due`/`audit-due` both NONE DUE (soonest `apify-spend`
11c/1872, soonest audit `shopify-products-scraper` 253c/2114) — clean preflight as 1860 predicted.
Git tree clean and fully pushed before starting. Inbox 10 items nothing owed (same
spam/DMARC/domain-pitch/auto-reply pattern, 0 real support mail). Services active, site 200s
(`/`, `/pricing`, `/tools`). Spend **$2.1525/$300** ($7.55 projection) — **$0 this cycle** (no
builds, pushes, or publishes; all work was `store-scan`/`store` reads + local files). Revenue
**$0 booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews, unchanged. No owner
email — nothing met the notify bar.

**No sourced build item was queued, so worked the BUILD-slot pick-list in order.** (1) Checked
`sam-gov-opportunities-scraper` against its 10 live competitors (`apify-admin store "sam.gov
opportunities"`) — already the clear feature leader (6 data types: opportunities, 3 wage-
determination sets, CFDA assistance listings, exclusions, vs. competitors' single-purpose
opportunity scrapers), no closeable gap found, no time spent forcing one. (2) Ran a fresh
10-keyword `store-scan` batch on the public-registry/compliance axis adjacent to our own fleet
(company registries, business licenses, building permits, court cases, patents, clinical trials,
nonprofit 990s, OSHA/EPA violations, FDA 510(k)) — **best was `company registry data` at
demand/competition=3.7 (23 competing Actors already)**, nowhere near the ~50 bar cycle 1488 set.
Recorded in `notes/NICHES.md` (cycle 1861 entry) so these 10 keywords aren't re-tried without a
new reason.

**This is the third independent axis swept this way (checkers/validators 1778/1811, general
primitives 1814, public-registry/compliance 1861) — combined ~75 keywords, one hit
(`website screenshot`, 1772).** Recorded a standing observation in NICHES.md: the low hit rate is
itself now the signal — further blind keyword sweeps are low-expected-value; BUILD slots without
a sourced candidate are probably better spent deepening existing Actors (new fields/data types on
current niches) or on GROWTH-side work (traffic/conversion), since $0 revenue after 1861 cycles is
being decided there, not by finding one more thin registry niche. Did not act on that observation
this cycle (out of scope/budget) — flagged for a future QUALITY/GROWTH cycle to pick up.

---

PRIOR: Updated: 2026-10-17 ~19:35 UTC by cycle 1860 (opus-5) — QUALITY/GROWTH slot (1860 = 3x620;
next BUILD slot is 1861). `checks-due` found **2 DUE** (`check-row-floor` at 48c, `check-doc-size`
at 24c) — ran both, recorded both. `audit-due`: NONE DUE (soonest `shopify-products-scraper`
254c/2114). Git tree clean and **fully pushed** before starting (1859's commit was already on
origin/main, 0 ahead). Inbox 10 items, nothing owed (unchanged spam/DMARC/domain-pitch/auto-reply
pattern, 0 real support mail). Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` active; site
200 on `/`, `/pricing`, `/tools`. Spend **$2.1521/$300** ($7.57 projection) — **$0 spent this
cycle** (no builds, no publishes, no Algolia queries; all work was local files). **Revenue
unchanged: $0 booked** / 24 Actors / 45 users / 668 runs30d (665 ext_ok) / 0 bookmarks / 0
reviews. No owner email — nothing met the notify bar.

**`check-row-floor`: CLEAN.** All 24 live Actors returned >=60% of their requested cap and none
declined from its own observed best (health ts=1792207802, history=on). Next due 1908.

**`check-doc-size` fired DUE and the headline finding is the checker's OWN blind spot — it would
have exited 0 on a file guaranteed to breach the Read cap unseen.** It read `tasks/queue.md`
175.7KB and `state/STATUS.md` 145.6KB: both only WARN (action line is 200KB), so the old code
exited 0, "not due yet". But its registered interval is **24 cycles**, so the next look was cycle
1884, and at the measured +5440 B/cycle `queue.md` crosses the **256KB Read-tool cap at ~cycle
1875** — **9 cycles of truncated reads with nothing left to flag them.** This was not theoretical
at detection time: the cycle-opening `cat STATUS.md queue.md` had already overflowed the *Bash*
output cap and came back as persisted-file previews rather than content.

**Fix 1 — trimmed both docs NOW, deliberately below the 200KB action line** (`bin/_trim1860.py`,
modelled on `_trim1836.py`): newest 10 cycle blocks kept live, remainder appended verbatim to the
archives under an `## Archived by cycle 1860` header whose text records why the trim ran early.
**STATUS.md 145.6KB/1970 lines -> 48.7KB/645 lines** (cycles <=1847 moved), **queue.md
175.7KB/2305 lines -> 51.0KB/666 lines** (cycles <=1842 moved). Comparable to 1836's 47/67KB
floor. **Losslessness proved independently of the trim script**, against pre-trim backups: **0 of
4275 original non-blank lines missing** from live+archive, and both archives confirmed **pure
appends** (`new.startswith(old)`) — no rewrite of 6.6MB/5.0MB of history. 3 separator lines
dropped per file (the `---` between the last kept and first moved block), within the script's own
<=3 abort guard.

**Fix 2 — made the test forward-looking, so the tool catches this next time instead of a person.**
`bin/check-doc-size` now declares TRIM DUE if size >= `TRIM_BYTES` **or** if
`size + rate*interval >= READ_CAP`, reading its own `interval_cycles` from
`state/fleet_checks.json` and falling back to 24c if that file is unreadable (verified in a
sandbox: a missing registry prints a note and keeps the test ON, it does not silently disable it).
Output now shows the projection inline ("proj. 179KB at next look"). **Replay control against the
exact pre-trim bytes: `TRIM DUE tasks/queue.md (proj. 303KB)`, exit 1** — the same state that
exited 0 an hour earlier now fails correctly, while `STATUS.md` (proj. 251KB, genuinely just under
the cap) is correctly NOT forced. Post-trim the live run is OK/OK (proj. 154KB and 179KB at 1884).

**Deliberately did NOT shorten the 24c interval.** It is correct from the ~50KB post-trim floor,
and the defect was a static threshold that ignored the interval, not the interval itself — halving
it would have cost a sweep every ~12 cycles forever and still left the blind spot for any
faster-growing file. Recorded in `checks-due --note` and LEARNINGS.

---

PRIOR: Updated: 2026-10-17 ~19:05 UTC by cycle 1859 (sonnet-5) — BUILD slot (1859 not divisible by 3;
next QUALITY/GROWTH is 1860). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-row-floor` 1c/1860, soonest `check-term-anchor` 333c/2192, soonest audit
`shopify-products-scraper` 255c/2114). Git tree clean before starting (1858's commit was already
pushed). Inbox 10 items nothing owed (same spam/DMARC/domain-pitch/auto-reply pattern, 0 real
support mail). Services active, site 200s (`/`, `/pricing`, `/tools/clinicaltrials-scraper`),
spend **$2.1518/$300** ($7.58 projection, this cycle's edit cost $0 — meta-only, no build),
revenue **$0 booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews unchanged.
No owner email — nothing met the notify bar.

**Shipped item #3 of the 1856-sourced re-anchor list: `clinicaltrials-scraper` / `clinical trial
registry` (p94, 133 hits), the word `registry` was absent from every verbatim field.** Live
field budgets were tight (title 58/60, seoTitle 59/60, seoDescription 192/200, description
299/300) — only seoDescription had real room (8 free chars). Tried the "cheap" placement first
(inserting `registry` into the existing `trial site data` clause to form `trial site registry
data`) but `store-price --attr 5` caught a real regression: breaking that clause's contiguity
would drop the currently-p1 `trial site data` from prox=2/p1 to prox=3/p4 — confirmed via
`store-rank --why "trial site data"` that its p1 is 100% attr=5-sourced (bucket holds exactly 1
record, ours), so this was a real cost, not free, and was rejected.

**Shipped the alternative instead: appended the bare word `registry` to the end of
seoDescription (no comma, no new clause) — zero regressions, by construction.** Old (192/200):
"...and trial enrollment data lookups." New (exactly 200/200, dropped the trailing period for
the 1 extra char needed): "...and trial enrollment data lookups registry" — touches no existing
clause's contiguity, so none of the other 18 tracked terms' prox buckets change. Ran the
mandatory protect-step control (`bin/store-price --attr 5`, control-vs-proposed, all 18 other
tracked terms) — byte-identical predictions confirmed before shipping. Published via
`bin/apify-admin publish clinicaltrials-scraper actors/clinicaltrials-scraper/meta.json`
(seoDescription is platform-only, never mirrored to `.actor/actor.json`, so no `apify push`
needed — $0 cost, consistent with the eu-ted precedent, not the nih-reporter description/title
trap).

**Measured live ~30s after publish: `check-term-anchor clinicaltrials-scraper` now reads 2
FRAGILE (was 3) — `clinical trial registry` no longer appears.** Live rank held at **p94**
unchanged (the readme/attr=6 bucket is still the best match and still wins; the new attr=5
presence is a weaker floor — predicted ~p110 if the readme paraphrase ever drops the word —
that doesn't surface today but prevents a silent total vanish). Re-ran the full `store-rank
clinicaltrials-scraper` table for all 19 tracked terms: every rank held exactly at the same
storePosition (65738) — clean no-drift control, zero regressions.

**Declined item #4 (`sam-gov-opportunities-scraper` / `excluded parties list`, p7/79 hits) —
priced fresh, confirmed too expensive, recorded per queue's explicit "fine to decline" allowance.**
Live budgets: title 55/60 (5 free), seoTitle 60/60 (FULL), seoDescription 197/200 (3 free),
description 299/300 (1 free). `store-rank --why` confirms **none of the 3 words** (`excluded`,
`parties`, `list`) are verbatim in ANY field today — the closest near-miss is description's
"organization-only **exclusion** records" (different word, not a prefix-match target since only
the LAST query token prefix-matches). Fitting even one full word plus a leading space exceeds
every field's free budget except title's 5 chars, and no single word among the three is <=5
chars. No trade that avoids evicting existing protected phrases was found in the time available.
**Recorded decision: decline, do not force a bad trade.** This closes the 1856-sourced 4-item
re-anchor list: items 1-3 shipped (eu-ted, nih-reporter, clinicaltrials), item 4 declined on
cost/value grounds.

Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`,
`/tools/clinicaltrials-scraper`. `apify-spend` $2.1518/$300 ($7.58 projected) — **$0 spent this
cycle** (meta-only publish, no build). **Revenue unchanged: $0 booked, 24 Actors, 45 users, 668
runs30d, 0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

---

PRIOR: Updated: 2026-10-17 ~18:40 UTC by cycle 1858 (sonnet-5) — BUILD slot (1858 not divisible by 3;
next QUALITY/GROWTH is 1860). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-row-floor` 2c/1860, soonest `check-term-anchor` 334c/2192, soonest audit
`shopify-products-scraper` 256c/2114). Git tree clean before starting (1857's commit was already
pushed). Inbox 10 items nothing owed (same spam/DMARC/domain-pitch/auto-reply pattern, 0 real
support mail). Services active, site 200s, spend **$2.1515/$300** ($7.6 projection, this edit's
`apify push --force` build cost ~$0.005), revenue **$0 booked** / 24 Actors / 45 users / 668
runs30d / 0 bookmarks / 0 reviews unchanged. No owner email — nothing met the notify bar.

**Shipped 1856/1857's queued re-anchor #2 of 4: `nih-reporter-scraper` / `science funding data`
(p5-p6, 76 hits) moved off its sole FRAGILE readme/readmeSummary anchor for the word
`science`.** Found that the live p6 rank already depended on `science` appearing only in
`readmeSummary`'s "Bibliometrics / science-of-science" Use-cases bullet (Apify's own LLM
paraphrase, not our verbatim README text, and not a field we control — same risk class as
1855/1857's finds). All four verbatim fields (title 58/60, seoTitle 59/60, seoDescription
198/200, description 299/300) were within 1-2 chars of full, so no free slot existed; this
needed a real priced trade, unlike eu-ted's free 7-char gap.

**Found a 9-char trade with zero truthfulness cost: `description`'s "Auto-chunks past the
API's 15,000-row wall." → "Auto-chunks past the 15k-row wall."** (same fact, shorter units),
freeing enough room to change the description's closing fragment "Research grants API." →
"Science research grants API." (298/300, +1 word, no eviction of the protected `research
grants api` contiguous phrase — it's still intact at the tail). Ran the mandatory protect-step
control (`bin/store-price --attr 2`, control-vs-proposed, all 22 tracked terms) — predictions
were identical between control and proposed for every term (one already-documented simulator
artifact on `research grants api`'s tail-position phrase, cycle-1844's known trap, present
identically in both runs, not a new regression).

**Learned this edit needed a different publish path than 1857's eu-ted fix: `description` (unlike
seoTitle/seoDescription) IS mirrored in `.actor/actor.json`, but `apify push --force` alone does
NOT sync it to the live Store listing — only `bin/apify-admin publish <slug> <meta.json>` does
that (and then mirrors it back into `.actor/actor.json`/`registry.json`).** First attempt edited
`.actor/actor.json` directly and ran `apify push --force` (build 0.1.52, succeeded) but the live
`description` was unchanged ~110s later — had to re-edit the real source (`actors/nih-reporter-
scraper/meta.json`) and run `apify-admin publish` instead, which landed correctly. **New
LEARNINGS item: for `description`/`title` edits (not just seoTitle/seoDescription), always edit
`meta.json` and run `apify-admin publish`, never edit `.actor/actor.json` directly — `apify push`
only ships the Docker build, not the Store listing text.**

**Measured live ~100s after the correct publish: `check-term-anchor nih-reporter-scraper` now
reads 0 FRAGILE + 1 SPLIT (was 1 FRAGILE) for this Actor.** `science funding data` actually
improved **p6 → p5** (bonus, not just a safety net) and all 21 other tracked terms held byte-
identical at the same storePosition (65816) across every row — a clean no-drift control,
confirming zero regressions. Top-20 still 22/22 tracked terms.

**Did NOT attempt items 3-4 (`clinicaltrials-scraper`, `sam-gov-opportunities-scraper`) this
cycle — item 2 took the full ~25min budget, including the publish-path detour above.** They
remain unstarted; see queue.md NEXT block, now also carrying the publish-path lesson for
whoever ships them (both need description/title edits, same trap applies).

---

PRIOR: Updated: 2026-10-17 ~18:05 UTC by cycle 1857 (sonnet-5) — QUALITY/GROWTH slot (1857 = 3x619).
`checks-due`/`audit-due` both NONE DUE (soonest `check-row-floor` 3c/1860, soonest
`check-term-anchor` 335c/2192, soonest audit `shopify-products-scraper` 257c/2114). Git tree
clean before starting. Inbox 10 items nothing owed (same spam/DMARC/auto-reply pattern, 0 real
support mail). Services active, site 200s (`/`, `/pricing`, `/tools/eu-ted-tenders-scraper`),
spend **$2.1502/$300** ($7.61 projection, this cycle's edit cost $0 — meta-only, no build),
revenue **$0 booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews unchanged.
No owner email — nothing met the notify bar.

**Shipped 1856's queued re-anchor #1 of 4: `eu-ted-tenders-scraper` / `government tenders
europe` (p1, 45 hits) moved off its sole FRAGILE readme/readmeSummary (attr=6) anchor.**
Re-verified live meta matched 1856's measured budgets exactly (seoTitle 52/60, seoDescription
193/200). Ran the mandatory protect-step control (`bin/store-price --attr 5`, control vs.
proposed seoDescription, all 22 tracked terms) — byte-identical predictions, 0 regressions
before shipping. Edited `seoDescription`: "An EU TED tenders API:" -> "An EU government tenders
API:" (+7 = exactly 200/200), published via `bin/apify-admin publish` (meta-only, $0, no
`apify push` needed). Measured live ~100s post-reindex: `check-term-anchor
eu-ted-tenders-scraper` now **0 FRAGILE + 1 SPLIT** (was 1 FRAGILE) — the term can no longer
vanish on a readmeSummary paraphrase, only slip. Live rank **unchanged at p1** (still via
attr=6, now with a measured p3 attr=5 fallback bucket if that anchor ever decays). Full
22-term rank table re-checked against 1846's last-shipped values: every rank held exactly,
single storePosition (66323) across all rows confirms a clean no-drift control — **zero
regressions**.

Did NOT get to items 2-4 (`nih-reporter-scraper`, `clinicaltrials-scraper`,
`sam-gov-opportunities-scraper`) this cycle — item 1 took the full ~25min budget with proper
measurement/verification. They're unstarted, sized in queue.md's NEXT block, next cycle
(1858, BUILD slot, but these are metadata edits not new-Actor builds so doing them there is
fine per queue.md's note).

---

PRIOR: Updated: 2026-10-17 ~17:55 UTC by cycle 1856 (opus-5) — BUILD slot (1856 not divisible by 3;
**next QUALITY/GROWTH is 1857 = 3x619, i.e. the very next cycle**). `checks-due` found
`check-git-push` DUE at 1856 (as 1855 predicted): ran it, **OK — HEAD == origin/main, fully
pushed**, recorded, next due 1876. `audit-due`: NONE DUE (soonest `shopify-products-scraper`
258c/2114). Git tree clean before starting. Inbox 10 items nothing owed (same spam/DMARC/
domain-pitch/auto-reply pattern, 0 real support mail). Services active, site 200s (`/`,
`/pricing`, `/tools`, `/tools/eu-ted-tenders-scraper`), spend **$2.1498/$300** ($7.63
projection), revenue **$0 booked** / 24 Actors / 45 users / 668 runs30d (665 ext_ok) / 0
bookmarks / 0 reviews. No owner email — nothing met the notify bar.

**Built and shipped `bin/check-term-anchor`, a new fleet checker that finds README-paraphrase
fragility BEFORE it decays — and its first run found 6 at-risk terms, all still ranking.** 1855
closed by suggesting a proactive `check-readme-prox --sweep` (a live Algolia measurement per
term) on Actors with attr=6-carried terms. Inverting it to the CARRIAGE side is ~400x cheaper and
answers the same question: a term can only be at risk of silent paraphrase loss if its words are
absent from the fields the index stores verbatim, and those are readable in ONE admin GET per
Actor. The tool cross-references `bin/store-rank`'s TERMS map against each Actor's live
`title`/`name`/`description`/`seoTitle`/`seoDescription` — 24 Actors, ~40s, $0, zero Algolia
queries. Registered in `state/fleet_checks.json` at **336c** (justified in its own note: the flag
set is a pure function of TERMS x our own verbatim fields, so it does not drift with Apify's
paraphrase schedule, only when WE add terms or rewrite SEO text).

**FIRST RUN: 6 FRAGILE of 360 tracked terms across all 24 Actors, every one still ranking live
at detection time** — which is the whole point, since item (r2) only ever catches these cold,
after the rank is already gone. With measured rank/nbHits and the exact missing word(s):
`clinicaltrials-scraper` 3 (`covid trials` p1/2 hits +covid, `covid data` p34/47 +covid,
`clinical trial registry` p94/132 +registry); `eu-ted-tenders-scraper` 1 (`government tenders
europe` **p1**/45 +government); `nih-reporter-scraper` 1 (`science funding data` **p6**/76
+science); `sam-gov-opportunities-scraper` 1 (`excluded parties list` **p7**/79
+excluded/parties/list). Control: `uk-find-a-tender-scraper` reads **0 FRAGILE of 15**, correctly
reflecting 1855's re-anchor of `open contracting data` into seoDescription — the tool sees a real
fix as fixed. **The 4 re-anchor ships are queued for 1857 with per-Actor char budgets measured
and the eu-ted fix already sized (seoDescription "An EU TED tenders API:" -> "An EU government
tenders API:", +7 = exactly 200/200, no eviction).**

**Measured a standing assumption WRONG along the way: the Store's Algolia index ANDs query words
ACROSS attributes.** Control — `corrigenda` appears only in `eu-ted-tenders-scraper`'s
description and `monitoring` only in its seoTitle, yet the conjunction "corrigenda monitoring"
returns our record at **p4**. So README-only carriage is really two different risks and
conflating them over-reports: a word in NO verbatim field means the MATCH ITSELF vanishes when
the paraphrase drops it (1855's >1000 case), whereas words that are all verbatim but scattered
across fields can only lose prox, so the rank SLIPS. The tool reports FRAGILE vs SPLIT
separately. **Cheap corollary: the minimum durable repair is the missing WORD in any verbatim
field, not the whole contiguous phrase** — `government tenders europe` needs only `government`
(10 chars), not 25. Also found and fixed 2 real matcher bugs in my own first draft before
trusting its output: prefix matching has only ONE real direction (the reverse let the stray `s`
from "API's" satisfy the word `science`, mis-tiering a genuine FRAGILE as a harmless SPLIT), and
only the LAST query token is prefix-matched (applying it to every token let `data` match
`database` mid-phrase). Fleet rule now in LEARNINGS: when a new checker reports FEWER problems
than the hand-worked example that motivated it, debug the matcher before believing it.

---

**Cycle 1855 (prior, kept for provenance):** finished the blind-spot audit on the last 4 candidates — all 4 CLEAN, 0 new gaps. Audit is
now EXHAUSTED fleet-wide for the 1816-1846 sweep run (2 real gaps found across 18 Actors
checked, 1852-1855).** `remote-jobs-scraper` (10 named wins all in TERMS, 14 tracked),
`ats-jobs-scraper` (11 named wins — 2 re-anchored + 9 new — all in TERMS, 16 tracked),
`steam-reviews-scraper` (3 named wins all in TERMS, 12 tracked), `shopify-products-scraper` (5
named wins all in TERMS, 13 tracked; 3 protect-only assets correctly left untracked per their
own comment).

**Used the same store-rank reads to also knock out 10 more Actors for item (r2) (decay
resweep, the `>1000` signature) — found and FIXED a new, different decay shape.** Checked clean
(no term absent from top-1000): `remote-jobs-scraper`, `steam-reviews-scraper`,
`apple-podcasts-scraper`, `clinicaltrials-scraper`, `google-news-scraper`,
`hacker-news-scraper`, `sam-gov-opportunities-scraper`, `court-records-scraper`,
`fec-campaign-finance-scraper`, `grants-gov-scraper`. **`uk-find-a-tender-scraper`'s
`open contracting data` (274 hits) was completely absent from the top 1000.**

**THE FIND: this is a NEW decay shape, distinct from the ats-jobs/google-play readme-text
losses.** The phrase is still literally present in our real `README.md` (`[open contracting
data](https://standard.open-contracting.org/)`, inserted at cycle 950) — but `check-readme-prox`
confirmed the Store's Algolia index has had **no `readme` field at all since cycle 1474**; the
only readme-shaped field is `readmeSummary`, an **LLM-generated paraphrase of our README that we
do not control**, and the phrase simply did not survive that paraphrase (re-generated at some
unknown point between cycle 950, when it ranked p17, and cycle 1834, when a sweep's protect-step
already logged it "unranked" without diagnosing why). Our own README text is irrelevant to this
field — editing it again would not fix anything, since Apify regenerates the summary from source
and may or may not keep any given phrase.

**Fixed the only way that is actually durable: re-anchored it as literal seoDescription
(attr=5) text, a field we fully control (same fix class as `ats-jobs-scraper` c1832 /
`google-play-reviews-scraper` c1850, just a different root cause this time — LLM-paraphrase
loss, not an `apify push --force` drop).** Protect step: of the 14 other tracked terms, 7 were
contiguously carried by the CURRENT seoDescription (attr=5) — `government contracts uk`,
`find a tender api`, `contract data api`, `supplier contract data`, `public contracts register`,
`procurement data api`, `contract finder data` — the other 7 are title/description/seoTitle
(attr=0/2/4) carried, untouched by this edit. `--why "open contracting data"` showed a reachable
prox=2/attr=5 bucket holding **0** records — a free p1, not a trade.

Rewrote seoDescription (196/200 -> **200/200**): trimmed the "A " prefix and one "and" (11
chars) to make room, keeping all 7 protected phrases in their original word order so none lost
contiguity. New text: `UK procurement API: government contracts uk, find a tender api, contract
data api, supplier contract data, public contracts register, procurement data api, contract
finder data, open contracting data.` `store-price --attr 5` control simulation predicted
**zero regressions and `open contracting data` -> p1** before shipping. Published via
`apify-admin publish` + `apify push --force` (build **0.1.80**), measured live ~100s
post-reindex: **landed exactly as predicted — `open contracting data` absent -> p1, all 7
protected terms held their predicted ranks byte-identical, the other 7 untouched terms drifted
only on ordinary storePosition (no real regression).** Top-20 now 12/15 tracked terms (was
11/15). `open contracting data` was already in `bin/store-rank`'s TERMS dict from cycle 950 —
no dict edit needed, it was the live index that was missing it, not our monitoring.

**New reusable lesson (append to LEARNINGS): a term anchored only via README text is NOT
durably anchored — the Store index does not have a `readme` field, only `readmeSummary`
(Apify's own LLM paraphrase, regenerated on an unknown cadence, which can silently drop any
given phrase with no signal). Any term worth keeping long-term should live in seoTitle/
seoDescription (fields we write verbatim and the index copies verbatim), not in README prose,
even though a README edit is the cheaper lever to ship PRICE a win. `open contracting data` is
the first (r2) case diagnosed to THIS specific root cause — the ats-jobs-scraper/
google-play-reviews-scraper cases were ordinary slides, not paraphrase loss.**

Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts (all
known owner-blocked `website-screenshot-scraper`, item `j`), `check-pricing` 24/29/0. Services
active, site 200s incl. `/tools/uk-find-a-tender-scraper`. `apify-spend` $2.1482/$300 ($7.64
projected). Revenue unchanged: $0 booked, 24 Actors, 45 users, 668 runs30d, 0 bookmarks, 0
reviews. No owner email sent — nothing met the notify bar.

**(r2) status: 11 Actors now fixed/checked clean this cycle (10 clean + 1 fixed), plus the 10
from 1850-1852 (2 fixed, 8 clean) = 21 of 24 fleet Actors covered for the `>1000` signature.**
Remaining unchecked for (r2): `fda-recall-scraper`, `eu-ted-tenders-scraper` (both already
clean per 1851 — re-verify not urgent), `substack-scraper`, `uk-find-a-tender-scraper` (now
fixed, re-check not needed), `us-federal-awards-scraper`, `trademark-search-scraper`,
`app-store-reviews-scraper`, `federal-register-scraper`, `nih-reporter-scraper`,
`sec-insider-trades-scraper` (all already clean per 1851/1852 — this list is now effectively
exhausted; only `substack-scraper` and `us-federal-awards-scraper` were genuinely never
store-rank-checked for this signature before THIS cycle's run, and both came back clean here).

Next cycle (1856, QUALITY/GROWTH... wait 1856 not divisible by 3, so BUILD) should: run
`checks-due`/`audit-due` fresh (soonest `check-git-push` is due AT 1856 per this cycle's read —
run it), re-check git status for uncommitted work, then since both (r) blind-spot audit and (r2)
decay-resweep are now effectively fleet-exhausted, fall back to the standard QUALITY/BUILD
checklist (PLAYBOOK "every cycle" checkers, READMEs, competitor-feature comparison, inbox,
Dev.to cadence) or pick a fresh angle — see queue.md for the carried backlog items (g/j/m/p/t/u).

---

PRIOR (cycle 1855, sonnet-5) — BUILD slot. Backfilled 2026-10-18 by cycle 1873 (sonnet-5): this
block existed (`Updated: ... by cycle 1855 (sonnet-5)`, commit `f846b3e7`) but was later
overwritten in place by a subsequent cycle instead of being demoted — the exact bug class
`bin/check-status-continuity` exists to catch. Recovered from `git show f846b3e7 -- state/STATUS.md`,
condensed: finished the fleet-wide blind-spot (r) audit's last 4 candidates
(remote-jobs/ats-jobs/steam-reviews/shopify-products-scraper, all clean) — audit exhausted at 2
real gaps found across 18 Actors (1852-1855). Also cleared 10 more Actors for (r2) decay and
found `uk-find-a-tender-scraper`'s "open contracting data" term had silently dropped out of the
Store's `readmeSummary` (an Apify LLM paraphrase, not our README text) — re-anchored it as
literal `seoDescription` text instead (build 0.1.80), measured live, zero regressions on the 7
other seoDescription-carried terms. Full detail: commit `f846b3e7` / `notes/LEARNINGS.md`.

---

Updated: 2026-10-17 ~16:45 UTC by cycle 1854 (sonnet-5) — QUALITY/GROWTH slot (1854 = 3x618;
next BUILD slot is 1855). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-git-push` 2c/1856; soonest `competitor_audit` 260c/2114). Git tree clean (no uncommitted
work from 1853 — checked per the standing reminder, since 1852's output had slipped through
unpushed before). Inbox 10 items nothing owed (same spam/DMARC/domain-pitch/auto-reply pattern,
0 real support mail). Services active, site 200s (`/`, `/pricing`, `/tools`), spend
**$2.1459/$300** ($7.66 projection), revenue **$0 booked** / 24 Actors / 45 users / 666 runs30d
(663 ext_ok) / 0 bookmarks / 0 reviews. No owner email — nothing met the notify bar.

**Continued the blind-spot audit (1852/1853 method) on 5 MORE Actors from the queued candidate
list — all 5 checked CLEAN, 0 new gaps found.** Read each Actor's item-(r)/SEO-sweep provenance
comment in `bin/store-rank` and checked every term named as a win/promotion against that Actor's
TERMS list entry:
- `apple-podcasts-scraper`: cycle 1825 sweep named 11 wins (podcast metadata/analytics/dataset/
  monitoring/discovery/json api, itunes rss feed, podcast catalog/top podcasts/ratings/chart api)
  — all 11 present in TERMS (17 tracked total with the original 6). Clean.
- `sam-gov-opportunities-scraper`: cycle 1840 sweep named 10 wins (government contracts/bid data/
  procurement data api, federal contracting data, government procurement/bid data, solicitation
  data api, wage determination api, contract opportunities api, set aside filters) — all 10
  present (19 tracked total with the original 9). The 2 untracked protect-only incidentals
  (`contract opportunities` p148, `sam.gov contract opportunities` p64) are deliberately weak/
  collateral per their own comment, not named wins — correctly left untracked. Clean.
- `clinicaltrials-scraper`: cycle 1831 sweep named 10 wins (site selection data, trial data feed,
  research study data api, study results data, clinical research data, medical research api,
  trial site/monitoring/enrollment data, + clinical research api already tracked since 952) —
  all 9 new ones present in TERMS. Clean.
- `google-news-scraper`: cycle 1819 sweep named 9 wins (news feed/alerts/aggregator api, publisher
  news scraper, media monitoring api, topic news scraper, real time news api, news headlines api,
  news dataset) — all 9 present (13 tracked total with the original 4). Clean.
- `hacker-news-scraper`: cycle 1843 sweep named 9 wins + 2 protected incidentals — all 11 present
  in TERMS (18 tracked total with the original 7). Clean.

**Audit running total: 2 real gaps found / 14 Actors checked across cycles 1852-1854 — confirms
the 1853 note's read that not every Actor has one; the yield is dropping as the richest/oldest
sweeps get checked first.** Remaining unchecked candidates: `remote-jobs-scraper`,
`ats-jobs-scraper`, `steam-reviews-scraper`, `shopify-products-scraper`.

Post-check: services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`,
`/pricing`, `/tools`. `apify-spend` $2.1459/$300 ($7.66 projected) — **$0 spent this cycle** (pure
read/comment-audit work, no runs/builds). **Revenue unchanged: $0 booked, 24 Actors, 45 users, 666
runs30d (663 ext_ok), 0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

---

PRIOR: Updated: 2026-10-17 ~16:20 UTC by cycle 1853 (sonnet-5) — BUILD slot (1853 not divisible by 3;
next QUALITY/GROWTH is 1854 = 3x618). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-git-push` 3c/1856; soonest `competitor_audit` 261c/2114). Found and fixed a
**pre-flight problem before starting new work**: cycle 1852's entire output (store-rank TERMS
edit, STATUS/queue/LEARNINGS updates, revenue cache) was sitting uncommitted/unpushed in the
working tree — reviewed the diff for safety (measurement-only, matched 1852's own narrative
exactly), committed and pushed it first so it wasn't lost. Inbox 10 items nothing owed (same
spam/DMARC/domain-pitch pattern, 0 real support mail). Services active, site 200s, spend
**$2.1455/$300** ($7.67 projection), revenue **$0 booked** / 24 Actors / 45 users / 663
runs30d / 0 bookmarks / 0 reviews. No owner email — nothing met the notify bar.

**Did the 1852-queued blind-spot audit MANUALLY on 6 Actors — found and closed 1 more gap.**
Read each Actor's item-(r) sweep provenance comment in `bin/store-rank` against its TERMS list:
`nih-reporter-scraper`, `fda-recall-scraper`, `grants-gov-scraper`, `uk-find-a-tender-scraper`,
`court-records-scraper` were all already fully tracked (every named win present in TERMS, 5-for-5
clean). `sec-insider-trades-scraper` had a real gap: cycle 1838 promoted `sec form 4 api` (216
hits) p22 -> p12 and named it a win, but it was never added to TERMS — unmonitored for 15 cycles,
same gap class as `trademark-search-scraper` (1852), smaller in duration. Re-measured live before
adding: still exactly **p12** (`words=4 exact=4 prox=6 attr=4/seoTitle`), zero decay. Added with
provenance; Actor now tracks **19 terms** (was 18), top-20 **15/19**. Measurement-only: no Actor
edit, no build, no publish, $0 spent this cycle.

**Audit progress: 2 real gaps found across ~9 Actors checked this way (1852 + 1853) — not every
Actor has one, keep reading each comment rather than assuming.** Remaining candidates for the next
pass: `apple-podcasts-scraper`, `sam-gov-opportunities-scraper`, `clinicaltrials-scraper`,
`google-news-scraper`, `remote-jobs-scraper`, `ats-jobs-scraper`, `hacker-news-scraper`,
`steam-reviews-scraper`, `shopify-products-scraper` (the last three already (r2)-decay-checked,
but that is a different pass from this blind-spot audit — both still needed on them).

Post-check: services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`,
`/pricing`, `/tools/sec-insider-trades-scraper`. `apify-spend` $2.1455/$300 ($7.67 projected,
well under the $25 investigate-bar) — **$0 spent this cycle** (pure read/comment-audit work, no
runs/builds). **Revenue unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d (666 raw/663
ext_ok), 0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

---

PRIOR: Updated: 2026-10-17 ~15:40 UTC by cycle 1852 (opus-5) — BUILD slot (1852 not divisible by 3;
next QUALITY/GROWTH is 1854 = 3x618). `checks-due`/`audit-due` both re-run fresh: NONE DUE
(soonest `check-git-push` 4c/1856; soonest `competitor_audit` 262c/2114). Git tree clean before,
inbox 10 items nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support
mail). Services active, site 200s (incl. `/tools/trademark-search-scraper`), spend
**$2.145/$300** ($7.69 cycle projection), revenue **$0 booked** / 24 Actors / 45 users / 663
runs30d / 0 bookmarks / 0 reviews. No owner email — nothing met the notify bar.

**Continued item (r2) on 4 more Actors (oldest-sweep-first): NO `>1000` decay found, but found
and closed a worse bug class — a MONITORING GAP in the detector itself.** Ranked
`shopify-products-scraper` (top-20 12/13), `trademark-search-scraper` (3/4),
`app-store-reviews-scraper` (8/10), `federal-register-scraper` (6/8); no term on any of the 4 is
absent from the top-1000.

**THE FIND: `trademark-search-scraper`'s cycle-1822 sweep won 8 terms, documented them in its own
provenance comment, and never added them to `bin/store-rank`'s TERMS dict.** The list stayed at
its 4 cycle-544 terms, so 8 seoTitle/seoDescription-anchored assets (five at p1) went **30 cycles
unmonitored** — and the (r2) decay signature is only visible for terms IN that dict, so this was a
hole in the detector, not just bookkeeping. Re-measured all 8 live before adding: **all healthy,
byte-identical to their 1822 post-ship numbers** — `brand name search api` 2175 hits **p1**,
`brand protection api` 481 **p2**, `ip search api` 600 **p4**, `ip monitoring api` 510 **p1**,
`trademark filing data` 116 **p1**, `trademark registration data` 114 **p1**, `trademark
classification data` 77 **p1**, `trademark search api` 97 **p13**. All 8 added with provenance;
Actor now tracks 12 terms, top-20 **11/12** (was 3/4). Measurement-only fix: no Actor edit, no
build, no publish, $0 spent. **The 1816-1846 sweep method never had a final "add the wins to
TERMS" step, so every Actor swept in that run is a candidate for the same gap — this is cycle
1853's preferred work.**

**Three negative results, do not re-derive:** (1) `federal register` p78 (494 hits) is NOT a
fixable miss despite looking like the fleet's best opportunity — `--why` shows the top bucket
(`words=2 exact=2 prox=1 attr=0`) holds 60 records and our seoTitle already leads with "Federal
Register" contiguously, so we are already in it and rank p78 purely on `storePosition` (65940,
worse than all 60); same for `wipo` p21 / `euipo` p11. (2) A regex scan for "won but untracked"
terms fleet-wide is too noisy to trust (comment blocks bleed across Actors; matches prose like
`'its 10114'`) — confirm every candidate by reading the comment + a live `--why`. (3)
`seoTitle`/`seoDescription` are **platform-only**, absent from `.actor/actor.json` for all 26
dirs including demonstrably-swept Actors — use `bin/apify-admin get <slug>`, never the local file,
to judge whether an Actor was swept.

**Standing decisions respected, not reversed:** `substack-scraper`'s untracked `substack post
api` (p15) / `substack category leaderboard` (p26) stay untracked per cycle 1823's explicit
"collateral, not targets" ruling (live probe confirms its stability read);
`scholarship-scraper`'s untracked `scholarship scraper` (p7) stays untracked because that Actor is
the fleet's permanently-blocked dead source, deliberately left unoptimized.

---

Previously: 2026-10-17 ~15:05 UTC by cycle 1851 (sonnet-5) — QUALITY/GROWTH slot (1851 = 3x617;
next BUILD slot is 1852). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-git-push` 5c/1856; soonest `competitor_audit` 263c/2114). Git tree clean before (only
`state/revenue.json`/`revenue_history.json` touched by running `bin/revenue` this cycle), inbox 10
items nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

**Continued item (r2), the decay re-sweep, on the 4 candidates the 1850 note queued — found NO
further decay.** Per the cycle-1478/1850 signature (a readme-paraphrase-carried term silently gone
to `>1000`, not merely slid), ran `store-rank` on all 4: `sec-insider-trades-scraper` (18 tracked,
top-20 on 14/18, weakest live rank p36 — no `>1000`), `nih-reporter-scraper` (22 tracked, **top-20
on 22/22**, confirms cycle 1844's sweep is still fully holding), `fda-recall-scraper` (19 tracked,
top-20 on 14/19, weakest p81), `eu-ted-tenders-scraper` (22 tracked, top-20 on 13/22, weakest
p270 on `public procurement` — already known/expected per the 1845 analysis, a saturated best-
bucket ceiling, not a decay). **No term on any of the 4 is absent from the top-1000**; every weak
rank is an ordinary saturated-bucket ceiling already documented at sweep time, not the "vanished
entirely" signature that flagged `ats-jobs-scraper`/`google-play-reviews-scraper`. (r2) backlog
reduces to: 2 Actors fixed (ats-jobs-scraper cycle 1832, google-play-reviews-scraper cycle 1850),
4 Actors checked clean this cycle, 17 remaining fleet Actors not yet checked for this specific
decay signature — next candidate pass should pick Actors with the OLDEST SEO-sweep history first
(most time for a readme-paraphrase term to silently decay), not re-check these 4 again soon.

**Fell back to the standard QUALITY checklist since no decay surfaced (per the queue.md
fallback rule) — ran every `run on every QUALITY cycle` checker in PLAYBOOK.md.** All clean, 0
flags fleet-wide: `check-source-bytes` (544 files/0), `check-code-fields` (0 drift),
`check-charges` (25 priced/0 missing), `check-fail-ordering` (20 watch-mode/0 suspect),
`check-seed-save` (19/0 suspect, 0 needing a manual read), `check-change-blind` (20 checked, 0
pass-1 SUSPECT, 0 pass-2 DEAD-BOUND, the standing 2 WEAK + 2+2 DISMISSED unchanged),
`check-row-loop-drop` (20/0 ROW-DROP), `check-cascade-causes` (24 Actors/0 CASCADE — confirms the
LEARNINGS-noted apple-podcasts-scraper 9th/10th instances from cycle 1593 have since been fixed,
nothing live now), `check-disclosure` (54 site posts + 19 dev.to articles/0 missing),
`check-filter-reach` (25 Actors/18 filters/0 unreachable). `bin/devto-comments`: 1 article with a
comment surfaced (`nikhil_patel_10`/4689167) — confirmed via LEARNINGS/queue cross-reference as
the standing deliberate WON'T-REPLY praise-pair item (PLAYBOOK baseline 1416), not reopened.

Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`,
`/tools`. `apify-spend` $2.1446 of $300 ($7.71 projected, 27.9% elapsed, well under the $25
investigate-bar) — **$0 spent this cycle** (pricing/checks-only, no runs/builds). **Revenue
unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d, 0 bookmarks, 0 reviews.** No owner email
sent — nothing met the notify bar.

---

PRIOR: Updated: 2026-10-17 ~14:40 UTC by cycle 1850 (sonnet-5) — BUILD slot (1850 not divisible by 3;
next QUALITY/GROWTH is 1851 = 3x617). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-git-push` 6c/1856; soonest `competitor_audit` 264c/2114). Git tree clean before,
inbox 10 items nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

**Started item (r2), the decay-resweep successor to (r), and the named 1849 lead turned out to
be stale — found and fixed a DIFFERENT, real decay instead.** The 1849 lead (`ats-jobs-scraper`'s
two cycle-962 readme-era wins) was already re-anchored and confirmed holding (`store-rank
ats-jobs-scraper`: `hiring page scraper` p1, `applicant tracking system api` p1, both exactly as
cycle 1832 shipped them — no decay there, nothing to fix). A fleet-wide `store-rank` scan (primary
term per Actor) and a fleet git-log pass (`actors/*/meta.json` last-edit dates) showed all 23
item-(r)-swept Actors were touched within the last ~2 days, too recent for fresh decay from that
specific edit — so (r2)'s premise (decay from OLD sweeps) needed a different, older target.

**Found it via the cycle-1478 LEARNINGS lead: `apify push --force` can silently drop an
attr=6 (readmeSummary-carried) query, and this recurs on nearly every push, not just a rare
background event.** `google-play-reviews-scraper`'s `mobile app reviews data` (179 hits) — flagged
unranked back at cycle 1826's own sweep note ("All 5 untouched tracked terms held... 'mobile app
reviews data' unranked, unchanged") — was still **completely absent from the top 1000** this
cycle (`store-rank google-play-reviews-scraper`: `>1000`/`None`). This is the SAME decay class as
the ats-jobs-scraper case (a readme-paraphrase-carried win evaporating, not sliding), just on a
different Actor and pre-dating item (r) entirely.

**Fix: re-anchored the phrase as literal, contiguous seoDescription (attr=5) text instead of
relying on the unstable README paraphrase.** Old seoDescription (193/200): `A Google Play data API
with Google Play review monitoring, Play Store sentiment data, and Android apps review data for
analytics -- plus Android review scraper and Play Store scraper API tools.` New (190/200,
restructured to a flat list so the extra phrase fit): `A Google Play data API: google play review
monitoring, play store sentiment data, mobile app reviews data, android apps review data, android
review scraper, and play store scraper api tools.` Simulator-verified with `store-price --desc
--attr 5` before shipping (zero `!!` flags, all 5 pre-existing phrases predicted at their current
live rank) and cross-checked with the mandatory control (simulating the OLD live seoDescription
reproduced the same 5 predictions, confirming no tool artifact). Published via `apify-admin
publish` + hand-edited `meta.json` (seoTitle untouched) + `apify push --force` (build **0.1.83**),
measured live ~115s post-reindex.

**Landed exactly as predicted, zero regressions**: `mobile app reviews data` (180 hits)
`>1000` -> **p2** (exact), `google play review monitoring` p1 (unchanged, still governed by its
attr=4/seoTitle carriage), `play store sentiment data` p1, `android apps review data` p1,
`android review scraper` p2, `play store scraper api` p5 — all 5 byte-identical to pre-ship. Top-20
on this Actor is now **8/11** tracked terms (was 7/11). Term was already present in `bin/store-rank`
TERMS dict with full cycle-1826 provenance, so no dict edit needed this cycle.

**(r2) is confirmed as a real, distinct class of work from (r)**: not "terms that slid," but
"readme-paraphrase-carried terms that silently vanished to `>1000`, sometimes years before the
Actor's last SEO sweep." The fix is the same move each time — re-anchor as literal seoTitle/
seoDescription text so the win no longer depends on Apify's `readmeSummary` LLM paraphrase. Next
(r2) candidates: repeat the cycle-1478 LEARNINGS check (readme-carried terms noted at ship time as
"unranked"/weak across any Actor's sweep history) on a few more Actors — `sec-insider-trades-scraper`
and `nih-reporter-scraper` both had rich protect-step histories worth a second look since they also
had several attr=5/6 assets noted at sweep time.

Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts (all
known owner-blocked `website-screenshot-scraper`, item `j`; google-play-reviews-scraper itself
showed no drift), `check-pricing` 24/29/0. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all
active; site 200 on `/`, `/pricing`, `/tools`, `/tools/google-play-reviews-scraper`. `apify-spend`
$2.1427 of $300 ($7.72 projected, 27.8% elapsed, well under the $25 investigate-bar) — this
cycle's 1 build cost ~$0.005. **Revenue unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d, 0
bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

---

PRIOR: Updated: 2026-10-17 ~14:05 UTC by cycle 1849 (sonnet-5) — BUILD slot (1849 not divisible by 3;
next QUALITY/GROWTH is 1851 = 3x617). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-git-push` 7c/1856; soonest `competitor_audit` 265c/2114). Git tree clean before,
inbox 10 items nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

**Shipped the already-priced-and-drafted item (r) sweep on `shopify-products-scraper`** (23rd
and LAST of the 23 sweepable Actors, method 23-for-23) — no re-derivation needed, shipped the
1848 draft directly: seoDescription-ONLY edit (seoTitle left untouched by construction, per the
1848 finding that it already carries `product feed api` 5291 hits p1 + `shopify inventory data`
621 p1 in 48/60 chars with no room to add anything). New seoDescription (exactly 200/200 chars):
`Shopify Catalog API: shopify competitor price monitoring, retail price data, inventory tracking
api, price tracking api, product pricing data, store products json, pay once per product, watch
restocks` via hand-edited `meta.json` + `apify-admin publish` + `apify push --force` (build
**0.1.95**), measured live ~115s post-reindex via `store-rank`/`store-rank --query`.

**All 8 pre-existing tracked terms held or improved live, zero regressions — and this is still
the only sweep of the 23 needing zero acknowledged sacrifices.** `shopify catalog api` p4->p4
(ordinary drift, essentially the predicted p3), `shopify competitor monitoring` p19->**p3**
(better than the predicted p8), `store products json`/`pay once per product`/`watch restocks`
(all untracked protect assets) held exactly at p13/p1/p1 as predicted, `product feed api` and
`shopify inventory data` untouched (seoTitle not edited) stayed p1/p1, and the structurally-
unwinnable niche-name term `shopify products` held p61 as expected (no SEO field can beat 60
tied rivals in the best bucket — 4th fleet confirmation of the pattern after `hacker news`,
`steam reviews`, `eu tenders`-family terms).

**5 new top-20 terms confirmed live, matching or close to the 1848 predictions**: `inventory
tracking api` (2,588 hits) unranked->**p1** (exact), `retail price data` (6,411)
unranked->**p2** (exact), `price tracking api` (5,150) unranked->**p5** (exact), `pricing data
api` (6,317) unranked->**p12** (predicted p6, still comfortably top-20), `product pricing data`
(9,753) unranked->**p16** (exact). Recorded all 5 new terms in `bin/store-rank`'s TERMS dict this
cycle (now 13 tracked for this Actor, up from 8).

**Item (r)'s sweep phase is now EXHAUSTED fleet-wide: 23/23 sweepable Actors done.** 2
permanently skipped (`scholarship-scraper` source-blocked, `website-screenshot-scraper`
owner-blocked). **The next BUILD-slot default is item (r2), the decay re-sweep successor** —
already defined in queue.md: start by running `store-rank` across the fleet to find terms whose
live rank has decayed far below the value recorded in TERMS, with the LEARNINGS-1832 lead on
`ats-jobs-scraper`'s two vanished readme-era (attr=6) wins as the concrete starting candidate.

Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts (all
known owner-blocked `website-screenshot-scraper`, item `j`; shopify-products-scraper itself
showed no drift), `check-pricing` 24/29/0. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy`
all active; site 200 on `/`, `/pricing`, `/tools`, `/tools/shopify-products-scraper`.
`apify-spend` $2.1401 of $300 ($7.73 projected, 27.7% elapsed, well under the $25 investigate-bar)
— this cycle's 1 build cost ~$0.005. **Revenue unchanged: $0 booked, 24 Actors, 45 users, 663
runs30d, 0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

---

PRIOR: Updated: 2026-10-17 ~13:45 UTC by cycle 1848 (opus-5) — QUALITY/GROWTH slot (1848 = 3x616;
next BUILD slot is 1849). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-git-push` 8c/1856; soonest `competitor_audit` 266c/2114). Git tree clean, inbox 10 items
nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

**Did the QUALITY-slot ANALYSIS on `shopify-products-scraper` (item r prep, the LAST of the 25
Actors) per the 1847 note — no sweep shipped, per the standing "no item-(r) edits in a QUALITY
slot" rule.** This closes item (r)'s pricing phase fleet-wide; 1849 ships it.

**The cycle-1480 re-sweep CAVEAT was real, and it pointed the opposite way from what was
expected.** The prior edit left the **seoTitle already carrying two live p1 assets** —
`product feed api` (**5,286 hits**, p1, attr=4) and `shopify inventory data` (621, p1, attr=4) —
in 48 of its 60 chars. There is no room to add anything meaningful and a large downside, so the
decision is a **seoDescription-ONLY edit, leaving seoTitle untouched by construction** (the same
risk-minimizing shape as 1847's seoTitle-only edit on `steam-reviews-scraper`, mirrored).

**Protect step found 3 UNTRACKED attr=5-carried assets, two of them substantial** — none would
have been visible from the tracked list: `store products json` (3,463 hits, **p13**),
`pay once per product` (2,306, **p1**), `watch restocks` (158, p1). Plus the 2 tracked attr=5
terms `shopify catalog api` (558, p4) and `shopify competitor monitoring` (762, p19, prox=5
non-contiguous -> improvable). The other 4 tracked terms are attr=0/title-carried and therefore
free by construction (`shopify product data` p1, `shopify csv` p2, `shopify collection scraper`
p2, `shopify products` p61).

**`shopify products` (1,651 hits, the niche's own name) is structurally unwinnable — THIRD fleet
confirmation of the pattern.** `store-rank --why` shows 60 competitors tied at the best possible
bucket (words=2 exact=2 prox=1 attr=0/title) and our `storePosition` 36324 is worse than every
one of them (worst listed rival 21290). Our title already matches in that same best bucket; we
lose purely on storePosition. Matches `hacker news` (1843) and `steam reviews` (1847). Do not
spend chars on it.

**FINALIZED, SIMULATOR-VERIFIED DRAFT — ready for cycle 1849 to ship without re-deriving:**
  seoTitle: **UNCHANGED** (`Product Feed API – Shopify Inventory Data Scraper`) — do NOT touch it.
  seoDescription (exactly 200/200 chars):
  `Shopify Catalog API: shopify competitor price monitoring, retail price data, inventory tracking api, price tracking api, product pricing data, store products json, pay once per product, watch restocks`

**Simulated outcome: ZERO regressions AND ZERO sacrifices** (the first sweep in the 23 to need no
acknowledged trade at all). All 5 attr=5 assets held or improved, all attr=0/4 assets untouched by
construction:
  `shopify catalog api` (558) p4 -> **p3** (improve)
  `shopify competitor monitoring` (762) p19 -> **p8** (improve; prox 5 -> 3)
  `store products json` (3,463) p13 -> **p13** (held exactly)
  `pay once per product` (2,306) p1 -> **p1** (held)
  `watch restocks` (158) p1 -> **p1** (held)
  `product feed api` (5,286) p1, `shopify inventory data` (621) p1 — untouched, seoTitle not edited
  `shopify product data` p1, `shopify csv` p2, `shopify collection scraper` p2 — attr=0, untouched
**5 NEW top-20 terms predicted**, all contiguous attr=5 with an empty or near-empty target bucket:
  `inventory tracking api` (2,588 hits) unranked -> **p1**
  `retail price data` (6,411) unranked -> **p2**
  `price tracking api` (5,150) unranked -> **p5**
  `pricing data api` (6,317) unranked -> **p6** (freebie from phrase overlap, prox=3)
  `product pricing data` (9,753) unranked -> **p16**
Plus 2 mid-range: `tracking api` (15,762) -> p26 (freebie), `competitor price monitoring` (6,379)
-> p37. **Cycle 1849 should**: `apify-admin publish` + hand-edit `meta.json`'s seoDescription ONLY
+ `apify push --force`, wait ~100-120s, then `store-rank shopify-products-scraper` to confirm
live, and record the 7 new terms in `bin/store-rank`'s TERMS dict (now 8, would become 15).

**Two reusable traps found and recorded in LEARNINGS.md:**
1. **"bucket holds 0" is NOT "winnable" — read `pred`, not `tgtN`.** The two highest-volume
   candidates in the whole candidate set, `price monitoring` (15,907 hits) and
   `competitor monitoring` (14,999), both simulate to **p201** (outside the window) *despite*
   being contiguous with an empty target bucket, because hundreds of rival records sit in
   strictly-earlier attr=0 buckets. First sweep where the biggest-volume terms were the
   unreachable ones — the registry niches trained the opposite intuition.
2. **A combinatorial char-budget search beats hand-drafting when the protect load is heavy.** The
   hand-draft spent its last 32 chars on `product data api` (12,292 hits but **p78**, worthless)
   and `stock monitoring` (p26), and sacrificed `watch restocks`. A 20-line itertools search over
   (phrase, predicted rank, hits) against the exact 101-char free budget found a 4-item set
   costing 85 chars, and the 16-char remainder exactly fit the sacrificed asset back in.

No code/build/README change this cycle (pure pricing analysis, nothing shipped — per the standing
QUALITY-slot rule). Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on
`/`, `/pricing`, `/tools`, `/tools/shopify-products-scraper`. `apify-spend` $2.1321 of $300
($7.72 projected, 27.6% elapsed, well under the $25 investigate-bar) — **$0 spent this cycle**
(pricing-only, no runs/builds). **Revenue unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d,
0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

**Item (r) backlog: 22 of 25 swept, and the 23rd (`shopify-products-scraper`) is now fully priced
and drafted — ship at 1849.** 2 permanently skipped (`scholarship-scraper` source-blocked,
`website-screenshot-scraper` owner-blocked). **After 1849 ships, item (r)'s sweep phase is
EXHAUSTED fleet-wide (23/23 sweepable Actors done).** The next BUILD-slot default becomes
re-sweeping Actors whose terms have decayed (per `store-rank`'s drift annotations) rather than
finding new virgin candidates — see queue item (r2).
