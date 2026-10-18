# Task queue

- [ ] FIX FAILED ACTORS (nightly health 2026-10-18): nih-reporter-scraper — ROOT-CAUSED by cycle
      1876, see the DONE block below. NOT our bug (NIH upstream outage) but a real silent-failure
      gap to fix: make `apiPost` detect the outage redirect and fail loudly. [medium]

DONE (cycle 1876, opus-5, BUILD slot — 1876 not divisible by 3; next QUALITY/GROWTH is 1878).
   `checks-due`: **`check-git-push` was due and ran** — OK, HEAD == origin/main, recorded (next
   due 1896). `audit-due`: NONE DUE (soonest `shopify-products-scraper` 238c/2114). Dev.to
   syndication precisely confirmed NOT due: floor `2026-10-18T06:01:36Z`, this cycle ran
   `2026-10-18T03:30:18Z` — ~2.5h early, do NOT syndicate before that timestamp; cycle 1877
   (~04:00Z) is still too early, **1878+ (06:00Z+) is the first eligible cycle**. Inbox 10 items,
   nothing owed (same JP form-autoreply/DMARC/`searchindex.pro` spam pattern). Services active,
   site 200s (`/`, `/pricing`, `/tools`). Revenue unchanged **$0 booked**. No owner email.

   **(1) SHIPPED: first attr-4/5 SEO measurement + edit on `steam-reviews-scraper` (live-verified,
   simulation matched measurement exactly).** Picked it as the thinnest-coverage slug (48/60
   seoTitle, the fleet's least-used title real estate among public Actors). Measured the OLD
   seoTitle first per the protect step — it was **already earning**, not wasted: `steam player
   stats` (573 nbHits) p2, `steam tags` (1044) p3, `steam charts api` (88) p1, all carried at
   attr=4. The real gap was two high-volume terms ranking badly: `steam game reviews api` (289
   nbHits) **p55** at attr=2, and `steam game reviews` (576) **p123** at attr=2 with a
   *non-contiguous* prox=6 match — exactly cycle 1817's "weak existing match worth re-optimizing"
   shape. Shipped seoTitle `Steam Game Reviews API, Steam Player Stats, Steam Tags` (54/60),
   measured live after reindex:
     - `steam game reviews api` (289 hits) p55 -> **p2** (attr 4, contiguous) — predicted p2 ✓
     - `steam game reviews` (576 hits) p123 -> **p71** — predicted p71 exactly ✓
     - `steam player stats` p2 HELD, `steam tags` p3 HELD ✓
     - **one accepted loss, priced before shipping**: `steam charts api` (87 nbHits) p1 -> unranked
       ("charts" no longer tokenised anywhere). Deliberate: 87 hits traded for 289+576.
   Method notes that held up: `--attr 4` re-pricing was mandatory (cycle 1820 trap 1) — the a0
   `pred` column said p1/p2 for terms that price far worse at a4. Surgical `Edit` on meta.json,
   not `json.dump` (trap 3): final diff 1 insertion / 1 deletion.
   **`apify-admin publish` alone does NOT reindex Algolia** — after publish the live listing showed
   the new seoTitle immediately but ranks were unchanged at +110s (`steam charts api` still p1 at
   attr=4 off the OLD title). `apify push --force` (build 0.1.74) then reindexed within ~120s and
   all five terms moved to the predicted values. **Both steps are required; budget ~$0.005 for the
   forced build.** `check-store-meta` clean on this slug afterwards (25 Actors, 4 drifts, all 4
   still the owner-blocked `website-screenshot-scraper` per item (j) — unchanged).

   **(2) ROOT-CAUSED the nightly health failure on `nih-reporter-scraper` — NIH upstream outage,
   not our bug, but it exposes a real silent-failure gap.** Health recorded `status 201, items 0`.
   Reproduced live (0 rows), then isolated per LEARNINGS rule 2: `{keyword}` alone, `{keyword,
   fiscalYears}` and `{keyword, agencyIcCodes}` **all** return 0 — so it is not a filter bug.
   Hit the upstream directly: `POST https://api.reporter.nih.gov/v2/projects/search` returns
   **`302 -> https://fallback.era.nih.gov/systemUnavailable`** (NIH eRA system unavailable).
   Mechanism for the silent 0: `apiPost` (`src/main.js:83`) calls `gotScraping` with
   `throwHttpErrors: false` and **default redirect-following**, so the 302 is followed to an HTML
   outage page that parses to no `results` — the run then SUCCEEDS with an empty dataset instead
   of failing. **Next cycle's fix (precise, scoped):** in `apiPost`, either set
   `followRedirect: false` and treat a 3xx (or any `fallback.era.nih.gov` / non-JSON
   `content-type`) as a retryable upstream outage, then `throw` a clear
   "NIH RePORTER is temporarily unavailable" after the retries, so the run FAILS loudly rather
   than returning 0 rows. Re-test the upstream first — **if the 302 has cleared, the Actor needs no
   code change to work, but ship the loud-failure guard anyway** (this will recur; a paying user
   getting a silent empty dataset is worse than a failed run). Do NOT chase the filters again:
   confirmed clean this cycle.

---

DONE (cycle 1875, sonnet-5, QUALITY/GROWTH slot — 1875 = 3x625).
   `checks-due`/`audit-due` both NONE DUE (soonest `check-git-push` 1c/1876; audit soonest 2114).
   Dev.to syndication precisely confirmed NOT due (`devto_syndicated.json` newest
   `devto_published_at` `2026-10-16T06:01:36Z`, floor `2026-10-18T06:01:36Z`, this cycle ran
   `2026-10-18T03:00:15Z`, ~3h early). Inbox nothing owed. Services/site healthy. Spend unchanged
   ~$2.22/$300 (only small `run-sync-get-dataset-items` test calls, no push). Revenue unchanged $0
   booked. No owner email. Git tree clean, no commit this cycle.

   **(1) Tried extending 1874's "audit filter/dedup ordering vs live data" technique to other
   Actors — came back negative.** Grepped all 24 Actors for `ocid`/`OCDS`: only
   `uk-find-a-tender-scraper` has it, so the bug shape (dedup-before-filter on a multi-release-per-
   id upstream) doesn't transfer. Read dedup/filter code in `sam-gov-opportunities-scraper`,
   `grants-gov-scraper`, `federal-register-scraper` (densest `.has(`/`.add(` patterns): all three
   dedup by canonical ID *after* filtering, no multi-version-per-id upstream shape that could
   reproduce the bug. **Do not re-check these three for this specific bug class again** — confirmed
   clean, same conclusion would recur.

   **(2) Ran the standing "platform tests with different inputs" checklist item via
   `bin/varied-test`, 0 regressions:** `court-records-scraper` (`recordType:"both"` +
   `courts:["scotus"]`) returned 10/10 opinions, 0 dockets — correct, since SCOTUS isn't a
   RECAP/PACER court, so the "both" budget-split legitimately reallocates 100% to opinions per the
   README's own documented behavior. `clinicaltrials-scraper` (`ageGroups:["CHILD"]` +
   `sex:"FEMALE"` + `conditions:"diabetes"`) returned some adult-inclusive age ranges
   (e.g. 12-50yr) — verified this is CT.gov's own overlap-based `standardAges` bucketing, already
   accurately documented in the README (line 66), zero drift. (Note: `conditions` is a string
   `textfield` input, not an array — a first test call with an array 400'd correctly against
   `.actor/input_schema.json`.)

   No code/content shipped — both lines of investigation closed clean rather than forcing a weak
   finding, per standing LEARNINGS rule. Full detail in STATUS.md cycle 1875.

NEXT (cycle 1877 — BUILD slot; 1877 not divisible by 3, next QUALITY/GROWTH is 1878).
   Run `bin/checks-due`/`bin/audit-due` fresh first (1876 ran `check-git-push`, next due 1896 —
   nothing should be due at 1877). Dev.to syndication floor is `2026-10-18T06:01:36Z`; cycle 1877
   runs ~04:00Z and is **still too early — do not syndicate**. First eligible cycle is 1878+
   (06:00Z+): syndicate the Apple Podcasts post
   (`/blog/apple-podcasts-episode-archive-is-not-there`) per PLAYBOOK via `bin/devto-post`.
   **TOP TASK, sourced and precisely scoped: the `nih-reporter-scraper` loud-failure guard** —
   full root cause, mechanism, `src/main.js:83` anchor and the exact fix are in the cycle-1876
   DONE block above. Re-test the NIH upstream 302 first, then ship the guard regardless.
   **Second, if time remains: continue the attr-4/5 SEO axis** — cycle 1876 proved the method
   transfers and is cheap (~15 min, ~$0.005/Actor). Next thinnest-coverage public slugs by unused
   seoTitle real estate: `shopify-products-scraper` (49/60, and its separator is an en-dash
   `–` rather than commas — worth checking whether it tokenises), then `substack-scraper` (50/60),
   `google-play-reviews-scraper` (51/60 — already optimised at cycle 1820, skip). Follow cycle
   1876's sequence exactly: measure the OLD field's live buckets FIRST (it may already be
   earning), shortlist at a0, **re-price survivors at `--attr 4`**, price the accepted losses
   before shipping, surgical `Edit` on meta.json, then `publish` AND `apify push --force`.
   Note `scholarship-scraper`'s seoTitle is a deliberate paused-status message — do not "optimise". Fall back to the standing BUILD-slot pick-list: (1) a competitor-feature
   spot-check on an Actor with an old/thin README competitor section not recently audited — check
   `grep -n "Update, re-verified" actors/<slug>/README.md | tail -3` for staleness before picking,
   candidates: `steam-reviews-scraper`, `ats-jobs-scraper`, `app-store-reviews-scraper`; (2) a new
   Actor on a genuinely unserved niche (max 6/day, 3 keyword-sweep axes already exhausted per
   1861/1862 — pick a 4th axis, not checkers/validators/general-primitives/public-registry); (3)
   the guide-writing GROWTH lever also works in a BUILD slot if nothing else is sourced, but the
   single-guide pick-list and the obvious saturated Actors (`us-federal-awards-scraper`,
   `substack-scraper`, `remote-jobs-scraper`, `hacker-news-scraper`, `eu-ted-tenders-scraper`) are
   all exhausted per 1869-1875 — do not re-read those five cold again without a genuinely new angle.
   Standing reminders: bucket-level regression testing; verify output field names against
   src/main.js and input names against `.actor/input_schema.json` (not variable names) —
   `conditions` on `clinicaltrials-scraper` is a string, not an array, confirmed again this cycle;
   `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` — use `bin/apify-admin get <slug>`;
   `apify push` does NOT sync the Store listing (use `bin/apify-admin publish <slug> meta.json`);
   after adding any output field, run `bin/check-real-fields` before calling the task done.

---

DONE (cycle 1872, opus-5, QUALITY/GROWTH slot — 1872 = 3x624).
   `checks-due`: **`apify-spend` was due and ran** — USED $2.2096 of the $300 total budget; Apify
   billing cycle 2026-10-09..11-08, 29.2% elapsed, projection **$7.56 vs the $85 hard cap**
   (builds $1.17 / runs $0.42, ACTOR_COMPUTE_UNITS $1.64 dominant). No action needed; recorded,
   next due cycle 1968. `audit-due`: NONE DUE (soonest `shopify-products-scraper` in 242c/2114).
   Inbox 10 items, nothing owed (same JP form-autoreply/DMARC/`searchindex.pro` spam pattern, 0
   real support mail). Services active, site 200s. Revenue not re-pulled (daily cron; no notify
   trigger fired) — unchanged **$0 booked** / 24 Actors / 45 users / 683 runs30d. No owner email.
   Spend this cycle: 2 `apify push` + 1 platform run (~$0.02) → **~$2.23/$300**.

   **Shipped item (o) from the 1871 handoff IN FULL: Form 4/A amendment support on
   `sec-insider-trades-scraper` (builds 0.1.52 code + 0.1.53 dataset schema).**
   - `formTypes` enum now `3,4,5,3/A,4/A,5/A` with matching `enumTitles`. **Default stays
     `["4"]`**, so every existing run and bill is unchanged — amendments are opt-in.
   - Five new output fields, declared in `.actor/dataset_schema.json` (42 fields now):
     `isAmendment`, `amendsOriginalFilingDate`, `supersedesAccessionNumber`,
     `supersedesCandidateAccessions`, `amendedByAccessionNumber`.
   - Part 2 (the superseding logic the handoff insisted on) is DONE, and the handoff's assumed
     match key turned out to be wrong in an important way — see LEARNINGS 1872. `<dateOfOriginal
     Submission>` is the original's **filing date** (later than `periodOfReport`, not equal to
     it), and EDGAR names the superseded accession **nowhere**. So linkage is inferred from the
     issuer's submissions index via a `(exact form|filingDate -> accessions)` map built over the
     same already-downloaded JSON (**zero extra requests**), kept separate from the capped
     `selectFilings` walk because the original is older than its amendment and usually a form the
     caller did not select.
   - Honest resolution instead of a guess: `supersedesAccessionNumber` is filled **only when the
     candidate set has exactly one member**, else null with the full set in
     `supersedesCandidateAccessions`. Both branches occur live: AAPL `0000320193-22-000078` -> 1
     candidate (resolves to `0000320193-22-000076`, independently confirmed same insider Maestri
     + same period 2022-08-17); TSLA `0000899243-22-021041` -> **3** candidates (Tesla filed 3
     Form 4s on 2022-05-04). Originals are NOT dropped — they come back tagged
     `amendedByAccessionNumber`, because an audit trail needs the wrong number and the fix.
   - **Found by testing, documented rather than papered over: issuer+insider+period is not a
     unique Form 4 key.** Denholm filed BOTH `0000899243-22-016670` and `-016671` for period
     2022-05-02, so `amendedByAccessionNumber` can mark two originals. README + code comment +
     blog update all state it means "a correction touching this issuer/insider/period exists",
     not "this exact row was restated". Do NOT "fix" this by narrowing on filingDate — already equal.
   - **Verified end-to-end on the platform**, not just locally: 45-row run, dataset
     `3xbLxdBOA9edE8mqA`, build 0.1.52 — bidirectional link correct on the Maestri pair, plain
     rows keep `isAmendment:false`/nulls/`[]` (no regression). Trick worth reusing: passing the
     **insider's** CIK (1513362) as the issuer input shrinks the index enough to reach a 2022
     filing cheaply. Published schema re-read over the API: enum + enumTitles live, readme 48,676 b.
   - README: new "Amendments (`4/A`) and which filing they replace" section with a field table,
     both worked examples and the ambiguity limit; stale "Not yet / until amendment support ships"
     FAQ answer and related-guides blurb replaced.
   - Site: `/blog/sec-form-4-amendments-are-unselectable` had become a FALSE claim about our own
     Actor — added an "Update, 2026-10-18: amendment support shipped" section + reworded the meta
     description (title/URL deliberately unchanged for SEO). `fetchsmith-web` restarted, post 200s.
   - Fleet checks: `check-real-fields` caught the undeclared fields (fixed, now **0 drift/24
     actors**), `check-code-fields` 0 drift after adding the two new `ctx` lookup keys
     (`ownershipIndex`, `amendmentsByEvent`) to FIELD_SUPPRESS with live-run evidence in the
     comment, `check-blog-claims` 0 stale, `check-links` CLEAN (122 pages). Committed + pushed
     (`444408af`), tree clean.

---

DONE (cycle 1873, sonnet-5, BUILD slot — 1873 not divisible by 3; next QUALITY/GROWTH is 1875).
   `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` in 3c/1876;
   audit soonest `shopify-products-scraper` in 241c/2114). Inbox 10 items, nothing owed (same
   spam pattern). Services active, site 200s. Spend unchanged **~$2.21/$300** (no push/call this
   cycle). Revenue unchanged **$0 booked** / 24 Actors / 45 users / 683 runs30d. No owner email.

   **(a) Dev.to confirmed still NOT due**, with the precise timestamp this time (1867/1869 both
   mis-predicted it off a rounded date): `state/devto_syndicated.json` has the last publish at
   exactly `2026-10-16T06:01:36Z`; the 2-day floor clears `2026-10-18T06:01:36Z`; this cycle ran
   at ~02:00Z, ~4h early. **Next cycle that runs after 06:01:36Z UTC today should syndicate it**
   (the Apple Podcasts post) if no fresher candidate has shipped by then.

   **(b)/(c) Checked the single-guide pick-list and declined to force a post — thin, not empty.**
   `us-federal-awards-scraper` (dedicated=1, lowest live count) and the dedicated=2/related=4 pair
   `substack-scraper`/`remote-jobs-scraper` were all read in full (README + relevant `src/main.js`
   sections) looking for one untested angle worth a new dedicated post. All three came back
   saturated — every input, edge case and competitor angle checked so far has already been
   measured and written down (see STATUS 1873 for the specific list per Actor). **Do not re-read
   these three for this purpose again without a genuinely new angle** (a product change on the
   upstream API, a new competitor feature, a support question) — re-reading them cold costs a
   cycle and reliably finds nothing new, as it did this time.

   **(d) Resolved the check-status-continuity hygiene item — fixed the tool, not a one-off
   backfill.** 9 of the 10 "MISSING" blocks were a false positive from wording drift
   (`Previous:`/`Previously:` headers the old regex couldn't match); generalized
   `HEADER_RE` to `^\w+:.*?by cycle (\d+)` so the next drift doesn't repeat this. The 10th
   (cycle 1855) was real — its block existed in commit `f846b3e7` and was later overwritten in
   place — backfilled a condensed `PRIOR (cycle 1855, ...)` block from that commit. Verified:
   `bin/check-status-continuity` now reports **0 missing**. Full writeup in LEARNINGS 1873.

   No code/content shipped this cycle (two closed candidates, no forced weak post). Committed
   and pushed.

DONE (cycle 1874, sonnet-5, BUILD slot — 1874 not divisible by 3; next QUALITY/GROWTH is 1875).
   `checks-due`/`audit-due` both re-ran fresh: NONE DUE. Dev.to confirmed still not due (~3h
   early, floor `2026-10-18T06:01:36Z`). Inbox nothing owed. Services/site healthy. Spend
   **$2.2197/$300**. Revenue unchanged. No owner email.

   **Picked `uk-find-a-tender-scraper` from the 1873 handoff's list (b) and found a real bug, not
   just a documentation gap — fixed it end to end.** `trademark-search-scraper` was skipped (got
   a fresh dedicated post the day before, 2026-10-17); `hacker-news-scraper` and
   `eu-ted-tenders-scraper` were read in full and are exhaustively saturated (same pattern as
   1869-1873's other finds — their competitor-pricing sweeps alone run 100+ paragraphs). UK's
   README led somewhere real.

   **The bug: OCDS tags an amended Contracts Finder release `tenderAmendment`, not `tender`**
   (live-measured: 61/368 = 16.6% of a 6-week CF `stages=tender` sample, spanning 39/316 = 12.3%
   of distinct procurements) — CF's own server already includes these under `stages=tender`, but
   this Actor's client-side re-filter did exact string equality and threw every one back out.
   **Compounded by a second bug**: the `ocid` "keep newest copy" dedup ran *before* that filter
   check and registered the ocid as seen regardless of match, so once the (newer, newest-first-
   paged) amendment failed the filter, the still-valid older `tender` original for the same ocid
   was then also dropped as a false duplicate. Net effect on the default `stages:["tender"]`
   input: **every amended procurement vanished entirely**, not just the amendment.

   **Fix (two parts, both needed)**: stage matching by tag-prefix (OCDS's own
   amendment/update/cancellation naming convention: `tenderAmendment`/`tenderUpdate`/
   `tenderCancellation` count as `tender`, `awardUpdate`/`awardCancellation` as `award`) instead
   of exact equality; and moved the `ocid` dedup bookkeeping to run only after the filter check,
   so a non-matching release of any kind can no longer block a later matching release of the same
   procurement (more general than just the amendment case).

   **Verified both locally and on the live platform**: unfixed code returned 0/4 sampled amended
   procurements, fixed code returned 4/4 (locally and via a real `run-sync-get-dataset-items`
   call against build **0.1.81**) — 269 rows before the fix, 311 after on the same test window.
   `bin/check-real-fields`: 0 drift (no new fields, correctness-only). Confirmed via
   `bin/apify-spend` that running your own PPE Actor under your own token only costs compute, not
   the per-event rate (~$0.01 total this cycle for one push + one live run).

   **Shipped the full package**: README FAQ entry with the measurement + fix-version note,
   `/blog/uk-tender-amendments-were-vanishing` (61 posts now, this Actor dedicated=2→3,
   related=5→6), root `README.md` Guides-list entry, `bin/indexnow` ping. Fleet checks all clean
   post-publish: `check-links` (123 CLEAN), `check-backlinks` (103 pairs, 0 missing), `check-
   blog-cta` (60 posts, 0 missing — first draft only had a two-hop `/tools/` link, fixed to a
   direct `/go/` one before this counted as done), `check-disclosure` (0 missing),
   `check-blog-claims` (0 stale), `check-actor-guides` (24 live, 0 flagged). Committed
   (`273e782b`) and pushed.

   **Standing lesson worth generalizing**: any Actor with client-side re-filtering on top of an
   OCDS/tag-based upstream (anything using the OCDS release-tag convention — `award`-stage
   content on other gov-procurement feeds included) should double check whether its own filter
   does exact-tag-equality instead of a stage-prefix match. Not re-auditing other Actors for this
   shape this cycle — flagging as a possible follow-up only if one surfaces again.

DONE-SUPERSEDED (was NEXT for cycle 1875; see the DONE 1875 block at the top of this file for
   what actually ran — the cross-Actor bug-class check + 2 platform regression tests, not a new
   dedicated post or dev.to syndication, since dev.to confirmed not due and (c)'s saturated-Actor
   list left no new angle).
   Run `bin/checks-due`/`bin/audit-due` fresh first; both NONE DUE as of 1874 (soonest
   `check-git-push` in ~2c/1876, audit soonest 2114).
   **(a) Dev.to syndication** — check the clock against `2026-10-18T06:01:36Z` precisely (see
   `state/devto_syndicated.json`), don't round; by cycle 1875 (~30min/cycle later) it may be due.
   If past, syndicate the 1864 Apple Podcasts post per PLAYBOOK (re-read it first for staleness).
   **(b) Standard QUALITY/GROWTH checklist** per CLAUDE.md: re-run platform tests on 2-3 existing
   Actors with different inputs, improve a README or two, answer support mail (none owed as of
   1874), check `bin/devto-comments` if due.
   **(c) Do NOT re-read `us-federal-awards-scraper`, `substack-scraper`, `remote-jobs-scraper`,
   `hacker-news-scraper`, or `eu-ted-tenders-scraper` cold again looking for a new dedicated-post
   angle** — all five were read in full across 1869-1874 and found saturated. If another
   dedicated post is wanted, either wait for a genuinely new angle (upstream API change,
   competitor feature) or consider a live-behavior AUDIT of an existing Actor's filter/dedup
   logic instead of a README read — that is what turned up this cycle's real bug on
   `uk-find-a-tender-scraper`, and the same technique (read `matches()`/dedup code, then verify
   against a live multi-page API pull) could be worth trying on another Actor with a similar
   OCDS/tag-based or multi-release upstream shape.
   `website-screenshot-scraper` stays skipped (still Store-unpublished, `isPublic: false`).
   Standing reminders: bucket-level regression testing; verify output field names against
   src/main.js and input names against `.actor/input_schema.json`, not variable names;
   `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` — use `bin/apify-admin get <slug>`;
   `apify push` ships only the Docker build and does NOT sync the Store listing (use
   `bin/apify-admin publish <slug> meta.json`); after adding any output field, run
   `bin/check-real-fields` before calling the task done.

---
DONE (cycle 1868, opus-5, BUILD slot — 1868 not divisible by 3; next QUALITY/GROWTH is 1869).
   `checks-due`/`audit-due` both NONE DUE on a fresh run (soonest `apify-spend` 4c/1872; audit
   soonest 2114). Inbox 10 items, nothing owed (same spam pattern). Services active, site 200s.
   Spend one `apify push` (~$0.005) → **~$2.21/$300**. Revenue **$0 booked** / 24 Actors / 45
   users / 683 runs30d / 0 bookmarks / 0 reviews, unchanged. No owner email.

   **Dev.to syndication was NOT due after all** — floor clears 2026-10-18 ~06:01Z and this cycle
   started 2026-10-17 ~23:30Z. 1867's handoff mis-predicted it. Fell through to the pick-list.

   **Published `/blog/openfda-count-shows-you-the-top-1000-and-never-says-so`** for
   `fda-recall-scraper` (58 posts now). Live-probed openFDA enforcement `count=`: default **100**
   buckets / max **1,000** (clean 400 at 1001), **exactly 1000 on all three endpoints** over
   corpora of 29,485 / 18,010 / 40,249 rows (ceiling, not a count); `meta.results` is **absent
   from count responses**, so truncation is undetectable except via `len(results)==limit`; `skip`
   is rejected (`400`, "Should not use skip param when using count"); **date-partitioning is the
   fix and is exactly additive** — 15 single-year `report_date` windows give **5,526** distinct
   food firms (5.5x), 0 global terms lost, window counts sum to 29,485 = corpus total, top firm
   633 == 633; `count=`/`sort=` on a non-`.exact` string field returns **HTTP 500** leaking the
   Elasticsearch `illegal_argument_exception` (reproduced on `classification`, `state`,
   `voluntary_mandated`, `product_description`, and on drug + device), while `sort=` is a 400;
   `limit` is **inert on date counts** (745 buckets at limit=5/1000/none). README backlink pushed
   (build **0.1.72**) and verified on the build's `readme` over the API (68,202 bytes); IndexNow
   200. `fda-recall-scraper` now `dedicated=2 related=6` — pick-list down to 2. All six fleet
   checks clean, 0 regressions (disclosure 58+19, blog-cta 58, backlinks 101, links 121 CLEAN,
   blog-claims 0 stale, actor-guides 24/0).

DONE (cycle 1869, sonnet-5, QUALITY/GROWTH slot — 1869 = 3x623).
   `checks-due`/`audit-due` both NONE DUE at cycle start (soonest `apify-spend` 3c/1872; audit
   soonest 2114) — confirmed, not re-run. Inbox 10 items, nothing owed (same spam/DMARC pattern,
   0 real support mail). Services active (`fetchsmith-web`/`fetchsmith-mail`/`caddy`), site 200s
   (`/`, `/pricing`, `/tools`). No `apify push`/`apify call` this cycle → spend unchanged at
   **~$2.21/$300**. Revenue **$0 booked** / 24 Actors / 45 users / 683 runs30d / 0 bookmarks / 0
   reviews, unchanged. `bin/traffic 7` shows the BUYER-INTENT funnel still nowhere near the >100
   verified-visits/day notify bar (tools 46/7d, pricing 3/7d) — no owner email.

   **Dev.to syndication confirmed NOT YET due**: floor from the last publish (2026-10-16 ~06:01Z)
   clears 2026-10-18 ~06:01Z; this cycle started 2026-10-18 ~00:00Z, ~6h early. At ~30min/cycle
   that's roughly cycle **1881**, not 1870 — don't hand this to 1870 as "due".

   **Ran `bin/devto-comments` (the standing every-QUALITY/GROWTH-cycle check): 3 unanswered, 0
   actionable.** The 2 already on record (`shieldxbot`/4809157, `nikhil_patel_10`/4689167) are the
   deliberate WON'T-REPLY pair from cycle 1416 (content-free praise, no claim/question) — left
   alone per standing rule. One NEW one, `suppdevbot` on article 4826969: a spam/phishing comment
   ("You need to verify your account", `tr.ee/dev-to` link-shortener) — not a real reader, not
   replied to, not worth a backlog item.

   **Checked the two-item single-guide pick-list and decided NOT to force either this cycle,
   rather than ship a weak 8th/9th post:**
   - `website-screenshot-scraper`: re-confirmed (without re-investigating the root cause, per item
     (j)) that it is still genuinely Store-unpublished — `bin/apify-admin get` shows `isPublic:
     false`, and `https://apify.com/fetchsmith/website-screenshot-scraper` still 404s live. A new
     blog post would funnel readers to a tool page whose own Store link is dead, so it stays
     skipped until the owner's Polar decision unblocks it.
   - `us-federal-awards-scraper`: spent the remaining budget auditing its two most complex README
     sections (Opportunity Score, Watch-mode fingerprinting) against current `src/main.js` instead
     of fabricating a new blog claim under time pressure. **Both are accurate, zero drift found**:
     the `opportunityScore()` weights/log-scale/keyword-list/category table match the README
     table exactly, and `watchKeyFor`'s `criteria` object includes every filter input that can
     change which awards match (categories/keywords/agencies/fundingAgencies/recipients/
     states/recipientStates/recipientTypes/naicsCodes/pscCodes/defCodes/min+maxAwardAmount/
     expiring*Days/startDate+endDateRaw) while correctly excluding non-filtering inputs
     (sortBy/order/maxResults/maxPagesPerCategory/includeOpportunityScore/webhookUrl/
     watchChanges) — no fingerprint-collision bug. This Actor is mature; a fresh USAspending
     `time_period` probe this cycle (large 2025-dated query) returned awards with start dates as
     old as 1993, confirming `time_period` filters on transaction/action date, not award start
     date — true, but not a strong enough standalone angle for a dedicated post this cycle, so
     parked rather than rushed (LEARNINGS rule: don't publish a one-shot-channel claim you haven't
     given a second look).
   No code/content changes this cycle — everything checked came back clean. Nothing committed/
   pushed (git tree unchanged).

DONE (cycle 1870, sonnet-5, BUILD slot — 1870 not divisible by 3; next QUALITY/GROWTH is 1872).
   `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `apify-spend` 2c/1872; audit
   soonest 2114). Git clean, 0 ahead/behind. Inbox nothing owed (same spam pattern). Services/site
   healthy. Spend unchanged **$2.2072/$300**. Revenue unchanged **$0 booked** / 24 Actors / 45
   users / 683 runs30d / 0 bookmarks / 0 reviews. Dev.to still not due (floor 2026-10-18 ~06:01Z).
   No owner email.

   **Closed 1869's parked USAspending `time_period` finding as NOT new info**: re-read
   `us-federal-awards-scraper/README.md`'s existing FAQ (lines ~190-196, "Why does `startDate` on
   a row show a date decades before my search window?") and confirmed it already documents this
   exact behavior in more depth (a live two-day window returning a 2018-2023 period-of-performance
   award, the 1-of-10 `lastModifiedDate` stat) than 1869's fresh 1993-dated-award probe. Same
   phenomenon, more extreme example, not a new angle — do NOT re-surface this without a genuinely
   different endpoint/filter-field angle.

   **Spot-checked `google-news-scraper` vs. its #1-by-users rival `lhotanova` (3,213 users)** —
   a single live pricing re-verification, not a full sweep. Pulled `lhotanova`'s public
   `pricingInfos` directly from the Apify API: the README's claimed 2026-10-14 PAY_PER_EVENT
   switch (start fee $0.005/0.004/0.00325, $0.002/0.0016/0.0013/article, $0.001/0.0008/0.00065
   per add-on) matches exactly, **zero drift**. This README is already on its 11th+ competitor
   sweep (latest dated 2026-10-16) — extremely well-maintained, no gap found, nothing to ship.

   No code/content shipped this cycle by deliberate choice — both candidates on the 1869 handoff
   closed as "nothing to do" rather than forcing a weak post or a redundant audit. Nothing
   committed/pushed (git tree unchanged).

DONE-SUPERSEDED (was NEXT for cycle 1871; see the DONE 1871 block at the top of this file for what
   actually ran — the sec-insider-trades-scraper Form 4/A finding, not a build-slot new-Actor pick).
NEXT (cycle 1871 — BUILD slot; 1871 is not divisible by 3, next QUALITY/GROWTH is 1872 = 3x624).
   Run `bin/checks-due`/`bin/audit-due` fresh first; 1870 left NONE due (soonest `apify-spend`
   ~1-2c/1872 — likely DUE this cycle, check before assuming).
   **The single-guide pick-list and the parked USAspending angle are now BOTH closed — no sourced
   BUILD candidate remains.** Do not re-check `website-screenshot-scraper` (item (j), standing) or
   `us-federal-awards-scraper` (related=7, audited clean 1869) without a genuinely new angle, and
   do not re-open the USAspending `time_period` item (closed for good at 1870 — the README already
   documents it more thoroughly than our finding).
   Options, in order: (1) a genuinely new Actor on an unserved niche — three keyword-sweep axes
   are exhausted (~75 keywords, 1 hit) per 1861/1862, so a 4th blind sweep is low-EV; if attempted,
   pick a different axis than checkers/validators, general primitives, or public-registry/
   compliance. (2) a competitor-feature spot-check on an Actor with an old/thin README competitor
   section — candidates not recently deep-audited: `steam-reviews-scraper`, `hacker-news-scraper`,
   `remote-jobs-scraper`, `ats-jobs-scraper`, `app-store-reviews-scraper`, `court-records-scraper`
   (check `grep -n "Update, re-verified" actors/<slug>/README.md | tail -3` for each to see how
   stale its last sweep actually is before picking — `google-news-scraper` looked stale by gap-
   count alone but turned out current at 1870, so check content, not just the audit-due table).
   (3) GROWTH-side volume work per 1862/1863's standing conclusion (top-of-funnel traffic, not
   features/niches, is the real $0-revenue bottleneck) — `bin/traffic 7`, `channel-mix`, or a
   backlink/outreach lever from PLAYBOOK, due 142c away per `checks-due` but doable ad hoc.
   Carried single-guide pick-list note: exhausted, both items closed, do not re-open without a new
   reason (standing, see above).
   Standing reminders: bucket-level regression testing; verify output field names against
   src/main.js before trusting a None/bug read, and input field names against
   `.actor/input_schema.json`, not variable names in main.js; `seoTitle`/`seoDescription` are NOT
   in `.actor/actor.json` — use `bin/apify-admin get <slug>`; `apify push` ships only the Docker
   build and does NOT sync the Store listing (use `bin/apify-admin publish <slug> meta.json`).
   **Rule from 1868: on an Elasticsearch-backed public API, a `count=`/aggregation endpoint that
   returns a plain 200 array is not evidence you got every distinct value — check whether the
   response still carries the `total`/`meta` block an ordinary search gives you. When it doesn't,
   `len(results) == limit` is the ONLY truncation signal, and the remedy is to partition the
   corpus on an indexed date field and union the per-window aggregations (verify additivity by
   summing bucket counts against the corpus total before trusting the union).**
   **Rule from 1867: when a new input joins a watch-mode baseline's fingerprint key, only include
   it in the hashed criteria object when it's set to something other than its backward-compatible
   default** — including it unconditionally reseeds every existing watch label.
   **Rule from 1865: a "declared vs delivered" check must compare against what was actually
   REQUESTED, not the raw declared total,** or it false-positives on every intentionally capped
   record.

---

DONE (cycle 1866, sonnet-5, QUALITY/GROWTH slot — 1866 = 3x622).
   `checks-due`/`audit-due` both NONE DUE (soonest `apify-spend` 6c/1872; audit sweep forbidden).
   Git clean at start. Inbox 10 items, nothing owed (same spam pattern). Services/site all
   healthy. Spend **$2.1655/$300** ($7.51 projection, one build this cycle, well under $25 alarm).
   Revenue **$0 booked** / 24 Actors / 45 users / 675 runs30d / 0 bookmarks / 0 reviews,
   unchanged. No owner email. Dev.to syndication checked but not yet due at this cycle's start
   time (~22:30 UTC Oct 17); floor clears 2026-10-18 ~06:01Z — fell through to the pick-list.

   **Wrote and published a second dedicated guide for `trademark-search-scraper`**
   (`/blog/tmview-search-criteria-undocumented-modes`), picked from the single-guide pick-list.
   New finding, live-verified, distinct from the existing post: TMview's search endpoint's
   `criteria` parameter accepts exactly three values — `C` (contains, pure substring, no word
   boundary), `W` (starts with a *complete word*), `E` (ends with a *complete word*) — everything
   else (including lowercase `c`/`e`/`s`, digits, empty string) returns `400
   PARAMETER_INCORRECT_FORMAT`. Proved `W`/`E` require a whole token (not just a substring) by
   searching the half-word fragment `"solarw"`: 829 hits under `C`, **0** under `W`/`E`. Our
   Actor and the official UI both hardcode `criteria: "C"` always. Added the backlink to the
   Actor's `## Related guides`, pushed (`apify push --force`, build **0.1.66**), verified live on
   the build's `readme` field over the API (54,827 bytes). `check-actor-guides` now reads
   `trademark-search-scraper dedicated=2 related=5`. Post-publish fleet checks clean, 0
   regressions: `check-disclosure` (57 site + 19 dev.to), `check-links` (120 pages CLEAN),
   `check-backlinks` (100 pairs), `check-blog-cta` (57 posts, 0 missing-CTA/bad-slug/dead-link).

   **New BUILD-slot candidate surfaced, not yet sized or implemented:** add a `matchMode` input
   to `trademark-search-scraper` (`contains` default / `startsWith` / `endsWith`, mapping straight
   to the `criteria: C/W/E` values above — no other request shape changes needed, already proven
   live). This is a real differentiation lever (narrows clearance-search noise, e.g. "does
   anything **start with** my proposed name" vs wading through every mark that merely contains
   it) — worth doing as a proper BUILD-slot task: update `.actor/input_schema.json`, thread the
   new input into the request builder (`src/main.js` ~line 379-381, currently hardcodes
   `criteria: 'C'`), and update the README input table + FAQ to describe the three modes. Do NOT
   just hardcode `'W'` or add it as a silent behavior change — it must be an explicit opt-in input
   so existing scheduled/watch-mode runs (which key their baseline on the `criteria`-less
   `searchTerm`/`offices`/`niceClasses`/`statuses` combo per `watchKeyFor`) are unaffected by
   default.

DONE (cycle 1865, sonnet-5, BUILD slot — 1865 not divisible by 3; next QUALITY/GROWTH is 1866).
   `checks-due`/`audit-due` both NONE DUE (soonest `apify-spend` 7c/1872). Git clean at start.
   Inbox 10 items, nothing owed (same spam pattern). Services/site all healthy. Spend
   **~$2.1623/$300** ($7.51 cycle projection, well under the $25 alarm line). Revenue **$0
   booked** / 24 Actors / 45 users / 675 runs30d (+2 my own test runs) / 0 bookmarks / 0 reviews.
   No owner email.

   **Shipped queue item (n): `apple-podcasts-scraper`'s declared-vs-delivered truncation
   warning**, closing the promise the 1864 blog post made. Added `warnIfTruncated()` to
   `src/main.js` — fires after each podcast's episode fetch (both the Apple-lookup path and the
   `useRssForFullArchive` RSS path), comparing the show's own `trackCount` against rows actually
   delivered, before any user filter. Did NOT hardcode 200 (1864 measured The Daily delivering
   only 44 via lookup, not 200). Found and fixed a false-positive risk while designing it: the
   lookup URL's own `limit=` is capped at the caller's `maxEpisodesPerPodcast` (default 100), so a
   naive declared-vs-delivered compare would warn on every >100-episode show even when the caller
   asked for fewer on purpose — fixed with `requestedLimit < 200 && delivered === requestedLimit
   && requestedLimit < declaredCount` as the suppression condition (landing exactly on Apple's
   200 hard cap still warns, since that's Apple's limit, not the caller's choice). Extended
   `getFeedUrlOnly()` to also return `trackCount` (same cached response, no extra request) so the
   RSS path has a declared count even when `includePodcastInfo` is off.

   **Verified live via real Apify runs, not just local simulation** — pushed build **0.1.90**,
   ran both paths against all 3 of 1864's known-good test IDs: The Daily (`1200361736`, 2751
   declared) warned on both lookup (44 delivered) and RSS (66 delivered); Lex Fridman
   (`1434243584`, 502 declared) warned on lookup only (200 delivered, hit Apple's hard cap), NOT
   on RSS (502/502 complete); Hardcore History (`173001861`, 13 declared) — the no-false-positive
   control — produced zero warnings either way (13/13). Separately confirmed the caller-explicit-
   low-cap case (`maxEpisodesPerPodcast=10` on The Daily) does not warn. Also fixed the stale
   over-claim comment at `src/main.js` ~line 136 ("RSS has no such cap", now qualified with the
   66/2,752 measurement); checked the other flagged line (~551) and found it already correct —
   1864's note was imprecise there, nothing to fix. Post-change fleet checks clean, 0 regressions:
   `check-disclosure`, `check-actor-guides` (`apple-podcasts-scraper dedicated=2 related=6`, 24
   live, 0 flagged).

DONE (cycle 1867, sonnet-5, BUILD slot — 1867 not divisible by 3; next QUALITY/GROWTH is 1869).
   `checks-due`/`audit-due` both NONE DUE (soonest `apify-spend` 5c/1872; audit soonest 2114).
   Git clean at start. Inbox 10 items, nothing owed (same spam pattern). Services/site all
   healthy. Spend **$2.2051/$300** ($7.62 projection, ~$0.04 this cycle: one build + ~8 live
   `apify call` test runs, well under the $25 alarm). Revenue **$0 booked** / 24 Actors / 45
   users / 683 runs30d / 0 bookmarks / 0 reviews, unchanged. No owner email. Dev.to syndication
   of the 1864 Apple Podcasts post checked — still not due at this cycle's ~23:15 UTC start
   (floor clears 2026-10-18 ~06:01Z).

   **Shipped the `matchMode` input for `trademark-search-scraper`** (1866's well-scoped BUILD
   candidate): added `matchMode` (`contains`/`startsWith`/`endsWith`, default `contains`) to
   `.actor/input_schema.json`, mapped it to TMview's `criteria: C/W/E` in `fetchPage`
   (`src/main.js`, replacing the old hardcoded `criteria: 'C'`), added it to `RUN_SUMMARY`,
   updated the README input table + added a dedicated FAQ entry + a Use-cases mention. **Kept
   `matchMode` OUT of the watch-mode fingerprint except when non-default** — `watchKeyFor`'s
   `criteria` object only gets a `matchMode` key when it's not `"contains"`, so every watch label
   that never touches this input (i.e. all of them, pre-this-change) hashes identically to
   before and keeps its existing baseline; only a label that actively opts into `startsWith`/
   `endsWith` gets a fresh baseline, same as changing any other filter.

   **Verified live, not just locally**: pushed build **0.1.67**, ran real `apify call` tests
   against the Store build. `searchTerm: "solarw"` (US+EM): `matchMode` omitted and
   `matchMode: "contains"` both → **193** matches; `startsWith`/`endsWith` both → **0** (matches
   1866's live-verified semantics — "solarw" is a substring but not a complete word).
   `searchTerm: "solar", matchMode: "startsWith"` → **9,410** declared matches, confirming the
   mode finds real positive hits, not just correctly rejecting fragments. A bogus `matchMode`
   value is rejected up-front by Apify's own input-schema `enum` (before the Actor even starts);
   the in-code fallback-to-`contains` is defense-in-depth for direct API callers who bypass
   schema validation, matching the existing `offices`/`niceClasses`/`statuses` guard style.
   **Fingerprint continuity directly verified**: a baseline run with `matchMode` omitted and one
   with `matchMode: "contains"` explicit landed on the byte-identical baseline key and the second
   correctly read the existing baseline (193 marks) instead of re-seeding; `matchMode:
   "startsWith"` on the same label produced a distinct key and started a fresh baseline, as
   intended. (Two early test calls TIMED-OUT at 120s after logging the match count, with no
   further progress; an immediate retry of the identical call succeeded in ~5s — transient
   TMview/proxy flakiness, not reproducible, not a code issue — not investigated further.)

   Committed (`59fb8049`) and pushed to `origin/main`. Did not run QUALITY-cycle fleet checks
   (none due, BUILD slot) and did not touch `meta.json` (no title/description/category change).

---

DONE-SUPERSEDED (was NEXT for cycle 1868; see the DONE 1868 block above for what actually ran).
   Run `bin/checks-due`/`bin/audit-due` fresh first; 1867 left NONE due (soonest `apify-spend`
   5c/1872; audit soonest 2114). **Dev.to syndication of the 1864 Apple Podcasts post is very
   likely due now** (floor cleared 2026-10-18 ~06:01Z) — strongest candidate on hand (three
   negative results with a measured table); use `bin/devto-post`, don't hand-roll the curl
   (PLAYBOOK Marketing section).
   Carried single-guide pick-list (oldest-posted first), **3** Actors (trademark-search-scraper
   done at 1866): `us-federal-awards-scraper` (2026-09-10, already related=7 — most-covered,
   lowest payoff), `fda-recall-scraper` (2026-09-11), `website-screenshot-scraper` (newest post
   2026-10-16 + Store-unpublished — lowest payoff).
   (`scholarship-scraper` shows 1 post by grep but is NOT in `check-actor-guides`' 24-live list —
   check `registry.json` status before picking it.)
   **Do NOT re-run:** niche-keyword sweeps (3 axes exhausted per 1861/1862); competitor checks on
   `trademark-search-scraper`/`fec-campaign-finance-scraper` (clean at 1862); the Apple Podcasts
   endpoint map, the declared-vs-delivered warning, the TMview `criteria` enum, or the new
   `matchMode` input (all shipped/live-verified at 1864/1865/1866/1867 — reuse those numbers,
   don't re-measure or re-ship).
   Standing reminders: bucket-level regression testing; verify output field names against
   src/main.js before trusting a None/bug read, and input field names against
   `.actor/input_schema.json`, not variable names in main.js; `seoTitle`/`seoDescription` are NOT
   in `.actor/actor.json` — use `bin/apify-admin get <slug>`; `apify push` ships only the Docker
   build and does NOT sync the Store listing (use `bin/apify-admin publish <slug> meta.json`).
   **Rule from 1865: when a per-request `limit=`/cap parameter is itself bounded by the
   caller's own input (not just the API's hard ceiling), a "declared vs delivered" check must
   compare against what was actually REQUESTED, not the raw declared total, or it produces a
   false positive on every record the caller intentionally capped below the maximum.**
   **Rule from 1867: when a new input joins a watch-mode baseline's fingerprint key, only include
   it in the hashed criteria object when it's set to something other than its backward-compatible
   default — including it unconditionally reseeds every existing watch label the moment the
   change ships, silently discarding their accumulated baselines.**

---

DONE (cycle 1864, opus-5, BUILD slot — 1864 not divisible by 3; next QUALITY/GROWTH is 1866).
   `checks-due`/`audit-due` both NONE DUE on a fresh run (soonest `apify-spend` 8c/1872; audit
   soonest `shopify-products-scraper` 2114). Inbox 10 items, nothing owed (same JP form-autoreply
   / DMARC / `searchindex.pro` domain-pitch spam, 0 real support mail). Services active, site
   200s. Git clean at start. Spend **~$0.005 this cycle** (one `apify push --force`), total
   **~$2.158/$300**. Revenue **$0 booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks /
   0 reviews — unchanged. No owner email (nothing met the notify bar).

   **Took the guide-writing GROWTH lever in the BUILD slot** (explicitly sanctioned by 1863's
   note as option 3), since both due-checks were empty and `audit-due` forbade a competitor sweep.
   Picked `apple-podcasts-scraper` from the single-guide pick-list — tied-oldest dedicated guide
   (2026-09-10) and the fewer related posts of the two tied. Skipped
   `website-screenshot-scraper` despite being listed first: its newest post is 2026-10-16 (1 day
   old) and item (j) leaves it unpublished on the Store, so a new guide there has the weakest
   payoff on the list.

   **Published `/blog/apple-podcasts-episode-archive-is-not-there`** (56 posts now, was 55), all
   numbers from live probes. Findings: (1) `itunes.apple.com/lookup?entity=podcastEpisode` caps
   at **200** episodes and clamps **silently** — `limit=201/300/1000` all return a byte-identical
   843,886-byte body, HTTP 200, no flag; (2) **`offset` is inert across the whole host** —
   `/lookup` and `/search`, podcast AND music (full ID lists identical), so there is no working
   control regime to switch to and the 200 is absolute, not a page size; (3) the big one —
   delivered counts are **sampled, not truncated**: The Daily (`trackCount: 2752`) returns **44**
   episodes spanning **307 days**, weekly-spaced at the old end, daily at the new, largest gap 21
   days. Disproved both a recency-window and a byte-cap explanation (Up First: 200 eps/671KB vs
   Daily: 44 eps/181KB — fewer rows came with fewer bytes); (4) `trackCount` vs delivered
   `podcastEpisode` rows is a **free, calibration-free truncation detector**, and strictly better
   than an "is it 200?" test precisely because delivered counts vary per show.

   **Corrected two of our own over-claims rather than restating them.** The earlier post said
   "for a complete back catalogue, parse the publisher's own RSS"; measured, RSS is **deeper, not
   complete** — Lex 502/502 (100%), Up First 500/1,425 (35%), The Daily 66/2,752 (**2.4%**, feed
   only reaches 2021 so it is sampled too). Added an inline **Updated 2026-10-17** annotation to
   `/blog/apple-podcasts-public-json-api` covering both the vague-`limit` and the complete-RSS
   claims. A `src/main.js` comment (~line 136) makes the same over-generalisation from one feed
   ("a real feed returned 2,977 items") — left alone this cycle, see (n) below.

   Added the backlink to the Actor's `## Related guides`, pushed (`apify push --force`, build
   0.1.89), and verified the backlink **live on the build's `readme` field over the API** (49,111
   bytes, string present) rather than trusting the cached Store page. `check-actor-guides` now
   reads `apple-podcasts-scraper dedicated=2 related=6` — off the pick-list, which is down to 4.
   Post-publish fleet checks all clean, **0 regressions**: `check-disclosure` (56 posts + 19
   dev.to, 0 missing), `check-links` (119 pages, CLEAN), `check-blog-claims` (0 stale),
   `check-blog-cta` (56 posts, 0 missing-CTA/bad-slug/dead-link), `check-backlinks` (99 pairs, 0
   missing), `check-actor-guides` (24 live, 0 flagged). Ran `check-doc-size` after noticing
   LEARNINGS.md is 746KB: it is **deliberately not size-gated** (appended and tailed, never Read
   whole, has its own archive) — STATUS 60.7KB / queue 69.7KB both OK, next look 24c. Do not
   "fix" the LEARNINGS size.

   Caught two factual errors in my own draft by checking source before publishing: the
   user-facing input is **`useRssForFullArchive`** (`rssFullArchive` is only an internal variable;
   a stale comment at main.js:551 uses the other name) and `source` values are
   `itunes`/`rss`/`chart`. Dev.to syndication deliberately NOT done — last publish 2026-10-16
   ~06:01Z, ~39h, under PLAYBOOK's 2–3 day floor (same gate as 1863). This post is a strong
   dev.to candidate the moment the floor clears.

NEXT (cycle 1865 — BUILD slot, 1865 not divisible by 3; next QUALITY/GROWTH is 1866 = 3x622).
   Run `bin/checks-due`/`bin/audit-due` fresh first; 1864 left NONE due (soonest `apify-spend`
   7c/1872).
   **(n) NEW, highest-value and well-specified — ship the truncation warning in
   `apple-podcasts-scraper`.** The post publicly states this gap ("what it does *not* yet do is
   warn you when `episodeCount` exceeds the rows it actually delivered … that warning is queued"),
   so it is now a promise. Shape: after the episode walk for a podcast, compare the show row's
   `trackCount` (already mapped to output `episodeCount`, main.js:489/652) against the count of
   `podcastEpisode` rows actually emitted for that `collectionId`; if short, `log.warning` naming
   the two numbers and pointing at `useRssForFullArchive` (exact input name — verified; do NOT
   use the internal `rssFullArchive`). **Do not hardcode 200 as the expected ceiling — 1864
   measured 44 for The Daily, so the only correct test is declared-vs-delivered.** Must also fire
   on the RSS path, where the shortfall is usually larger in absolute terms (66 of 2,752) but the
   user has explicitly opted into the deeper source, so word it as "this is the edge of what is
   public", not as a misconfiguration. Known-good test inputs: `id=1200361736` (The Daily, 2752
   declared / 44 lookup / 66 RSS — should warn on both paths), `id=1434243584` (Lex, 502/200/502 —
   should warn on lookup, NOT on RSS), `id=173001861` (Hardcore History, 13/13 — must NOT warn,
   the no-false-positive control). While in the file, fix the stale over-claim in the comment at
   ~line 136 ("RSS has no such cap … a real feed returned 2,977 items") and the stale
   `useRssForFullArchive`-vs-`rssFullArchive` naming in the comment at ~line 551.
   If (n) is somehow blocked, the guide-writing lever remains cheap and proven (one post, ~$0.005,
   ~25 min, 0 regressions) and the pick-list is now **4** single-guide Actors, oldest-posted
   first: `us-federal-awards-scraper` (2026-09-10, but already related=7 — most-covered),
   `fda-recall-scraper` (2026-09-11), `trademark-search-scraper` (2026-09-24),
   `website-screenshot-scraper` (newest post 2026-10-16 + Store-unpublished — lowest payoff, skip
   unless the others are exhausted). (`scholarship-scraper` shows 1 post by grep but is NOT in
   `check-actor-guides`' 24-live list — check `registry.json` status before picking it.)
   **Also now due-ish:** dev.to syndication of the 1864 Apple Podcasts post once the 2–3 day floor
   clears (last publish 2026-10-16 ~06:01Z, so from 2026-10-18 ~06:01Z). It is the strongest
   dev.to candidate on hand — three negative results with a measured table.
   **Do NOT re-run:** niche-keyword sweeps (3 axes exhausted per 1861/1862); competitor checks on
   `trademark-search-scraper`/`fec-campaign-finance-scraper` (clean at 1862); the Apple Podcasts
   endpoint map (1864 probed `lookup`/`search` `limit`+`offset` and the RSS depth of 3 feeds —
   reuse those numbers, don't re-measure).
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   Standing reminders: bucket-level regression testing; verify output field names against
   src/main.js before trusting a None/bug read — **and input field names against
   `.actor/input_schema.json`, not variable names in main.js (1864 nearly shipped the wrong one)**;
   LEARNINGS rule 2 (isolate multi-value filters when only one value survives before declaring a
   pass) and rule 6 (check whether two zero-row causes can co-occur and both get named).
   **New rule from 1864: when a source returns fewer rows than requested, check the SPAN of what
   came back before naming a mechanism — fewer rows over the same period is sampling, not a
   shorter window.** `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` — use
   `bin/apify-admin get <slug>`, never the local file. The real source of truth for
   `title`/`description`/`seoTitle`/`seoDescription`/`categories` is each Actor's `meta.json` +
   `bin/apify-admin publish`; `apify push` ships only the Docker build and silently does NOT sync
   the Store listing.

---

DONE (cycle 1863, sonnet-5, QUALITY/GROWTH slot — 1863 = 3x621).
   `checks-due`/`audit-due` both NONE DUE (soonest `apify-spend` 9c/1872 — checks-due itself said
   "spend it on growth work"). Git tree clean before starting. Inbox nothing owed. Services
   active, site 200s. Spend **$2.1534/$300** (~$0.005 this cycle, one README-backlink push).
   Revenue unchanged ($0 booked / 24 Actors / 45 users / 668 runs30d).

   **Acted directly on 1862's conclusion (top-of-funnel volume is the bottleneck) instead of
   deferring again: wrote and published a new site blog post, the most concrete GROWTH lever on
   the pick-list.** Checked Dev.to cadence first and correctly skipped it — last dev.to publish
   was 2026-10-16T06:01Z, ~39h before this cycle, under the 2-3 day floor in PLAYBOOK's Marketing
   section. Picked `fec-campaign-finance-scraper` (1 of 7 Actors at exactly 1 dedicated guide) and
   found a genuinely new, live-verified gotcha: OpenFEC's `/schedules/schedule_a/` (+`schedule_b`/
   `schedule_e`) `page=` parameter is silently ignored — `page=1/2/30/500` all return the
   byte-identical first row, `HTTP 200`, no error — while `/candidates/` pages normally (control).
   The real cursor is `pagination.last_indexes`, verified it actually advances. Also found a
   smaller secondary trap: `contributor_employer` free-text match (`GOOGL` outscores `GOOGLE`,
   129,954 vs 129,917 rows). Published `/blog/fec-schedule-a-page-parameter-ignored`, added the
   backlink to the Actor's `## Related guides`, pushed (`apify push --force`), verified live via
   the `latest` build's `readme` field over the API (not the cached page). Ran
   `check-disclosure`/`check-links`/`check-backlinks`/`check-actor-guides` fleet-wide post-publish
   — all clean, 0 regressions. Did not touch `store-rank`'s TERMS map (`donor search`/`donor
   search api` already tracked for this Actor since cycle 1828).

NEXT (cycle 1864 — BUILD slot, 1864 not divisible by 3; next QUALITY/GROWTH is 1866).
   Run `bin/checks-due`/`bin/audit-due` fresh first; 1863 left NONE due (soonest `apify-spend`
   8c/1872). **The GROWTH-volume lever is proven cheap and repeatable (one post, ~$0.005, ~20
   min, 0 regressions) — the remaining 6 single-guide Actors are a ready-made pick-list for
   future QUALITY/GROWTH slots, oldest-posted first unless a better angle turns up:**
   `website-screenshot-scraper`, `trademark-search-scraper`, `apple-podcasts-scraper`,
   `fda-recall-scraper`, `us-federal-awards-scraper`. (`scholarship-scraper` also shows 1 post by
   grep but is NOT in `check-actor-guides`' 24-live list — check `registry.json` status before
   picking it; may be retired/unpublished.) For a BUILD slot with no sourced candidate, same
   pick-list as 1861/1862 applies: (1) competitor-feature check on an Actor not recently covered,
   (2) a new Actor only on a genuinely unserved niche (max 6/day), (3) this guide-writing lever
   also works fine in a BUILD slot if nothing else is sourced. **Do NOT re-run:** niche-keyword
   sweeps (3 axes exhausted per 1861/1862), competitor checks on `trademark-search-scraper`/
   `fec-campaign-finance-scraper` (both just confirmed clean at 1862).
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   Standing reminders: bucket-level regression testing; verify output field names against
   src/main.js before trusting a None/bug read; LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named). `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` —
   use `bin/apify-admin get <slug>`, never the local file. The real source of truth for
   `title`/`description`/`seoTitle`/`seoDescription`/`categories` is each Actor's `meta.json` +
   `bin/apify-admin publish`; `apify push` ships only the Docker build and silently does NOT sync
   the Store listing.

---

DONE (cycle 1862, sonnet-5, BUILD slot — 1862 not divisible by 3; next QUALITY/GROWTH is 1863).
   `checks-due`/`audit-due` both NONE DUE (soonest `apify-spend` 10c/1872). Git tree clean and
   pushed before starting. Inbox nothing owed. Services active, site 200s. Spend **$2.153/$300**,
   **$0 this cycle**. Revenue unchanged ($0 booked / 24 Actors / 45 users / 668 runs30d).

   **Resolved 1861's flagged strategic question by testing it, not deferring again: spot-checked
   `trademark-search-scraper` and `fec-campaign-finance-scraper` (deepest-documented Actors)
   against their top-by-users live competitors — both still clear feature leaders, no closeable
   gap on either.** Also verified the top-traffic blog post's tool CTA is intact and that all 24
   live Actors already have >=1 dedicated blog post (0 orphans). Full writeup in `notes/
   NICHES.md` cycle-1862 entry. **Verdict: "deepen existing Actors" is also low-EV right now —
   the real gap per `bin/traffic`'s verified BUYER-INTENT funnel is top-of-funnel volume (8
   visitors/week to /tools, 2 to /pricing), not missing features/niches/content.**

NEXT (cycle 1863 — QUALITY/GROWTH slot, 1863 = 3x621).
   Run `bin/checks-due`/`bin/audit-due` fresh first; 1862 left NONE due (soonest `apify-spend`
   10c/1872). **Act on 1862's conclusion directly this cycle instead of flagging it a fourth
   time:** pick a GROWTH-volume lever from PLAYBOOK — most concretely, write/publish a new blog
   post targeting a fresh long-tail query for an Actor that currently has only 1 post (several
   listed in `notes/NICHES.md`/this file's blog-coverage check), or push `channel-mix`/backlink
   work, or the Dev.to article if due (`devto-comments` last=1836, not re-due until 1980 per
   `checks-due`, but publishing a NEW article is separate from the comment-check cadence — check
   `notes/PLAYBOOK.md` for the Dev.to cadence rule specifically, not just `checks-due`). Do NOT
   spend this slot re-auditing `trademark-search-scraper` or `fec-campaign-finance-scraper` for
   feature gaps (both just confirmed clean at 1862) or re-running niche-keyword sweeps (exhausted
   per 1861/1862, 2 independent axes now empty).
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   Standing reminders: bucket-level regression testing; verify output field names against
   src/main.js before trusting a None/bug read; LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named). `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` —
   use `bin/apify-admin get <slug>`, never the local file. The real source of truth for
   `title`/`description`/`seoTitle`/`seoDescription`/`categories` is each Actor's `meta.json` +
   `bin/apify-admin publish`; `apify push` ships only the Docker build and silently does NOT sync
   the Store listing.

---

DONE (cycle 1861, sonnet-5, BUILD slot — 1861 not divisible by 3; next QUALITY/GROWTH is 1863).
   `checks-due`/`audit-due` both NONE DUE (soonest `apify-spend` 11c/1872, soonest audit
   `shopify-products-scraper` 253c/2114) — clean preflight as 1860 predicted. Git tree clean and
   fully pushed before starting. Inbox 10 items nothing owed (same pattern, 0 real support mail).
   Services active, site 200s, spend **$2.1525/$300** ($7.55 projection), **$0 this cycle**.
   Revenue **$0 booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews unchanged.
   No owner email.

   **No sourced build item was queued, so worked the BUILD-slot pick-list in order.** (1)
   `sam-gov-opportunities-scraper` vs. its 10 live competitors: already the clear feature leader
   (6 data types vs. their single-purpose opportunity scrapers), no closeable gap, no time
   wasted forcing one. (2) Fresh 10-keyword `store-scan` on the public-registry/compliance axis
   (company registries, business licenses, building permits, court cases, patents, clinical
   trials, nonprofit 990s, OSHA/EPA violations, FDA 510(k)) — best was `company registry data`
   at d/c=3.7 (23 Actors already), nowhere near the ~50 bar. Recorded in `notes/NICHES.md`
   (cycle 1861 entry) — do not re-check these 10 keywords without a new reason.

   **New standing observation (NICHES.md, cycle 1861):** three independent keyword-sweep axes
   now done (checkers/validators 1778/1811, general primitives 1814, public-registry/compliance
   1861) — ~75 keywords, 1 hit (`website screenshot`, 1772). The low hit rate is itself the
   signal: further blind sweeps are low-expected-value. A future QUALITY/GROWTH cycle should
   pick this up and decide whether to pivot BUILD-slot effort toward deepening existing Actors
   (new fields/data types on current niches) or GROWTH-side work (traffic/conversion) instead of
   more niche-hunting — $0 revenue after 1861 cycles is being decided there, not in the Store
   search index. Not actioned this cycle (out of scope/budget), just flagged.

NEXT (cycle 1862 — BUILD-default slot, 1862 not divisible by 3; next QUALITY/GROWTH is
   1863 = 3x621).
   Run `bin/checks-due`/`bin/audit-due` fresh first; 1861 left NONE due (soonest `apify-spend`
   11c/1872). **Pick up 1861's flagged strategic question first if there's room:** read
   `notes/NICHES.md`'s cycle-1861 entry and decide — continue niche-hunting, or pivot a cycle to
   deepening an existing Actor (e.g. add a data type/field competitors lack) or to GROWTH work
   (`bin/traffic`, pageviews on `/pricing`/`/tools`). If no decision is made, default to the
   existing pick-list: (1) standing QUALITY backlog not needing a QUALITY slot (clinicaltrials's
   2 remaining low-value FRAGILE terms — still skip unless a field frees up room); (2) a new
   Actor only if a genuinely unserved niche turns up (max 6 new Actors/day — 0 built today as of
   1861); (3) competitor-feature comparison on an Actor not yet checked this way (sam-gov and
   clinicaltrials/nih/eu-ted already covered recently).
   **Do NOT re-run:** the 10 keywords from 1861's scan, or the ~65 from 1778/1811/1814, without a
   new reason. **Do NOT resurrect:** sam-gov's `excluded parties list` (priced negative twice),
   item (r)/(r2) audits (fleet-exhausted), item (p) cycle-1772 niche axis (now 4 batches,
   exhausted per 1814's own note), item (t) varied-test re-test (not due until ~1969).
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   Standing reminders: bucket-level regression testing; verify output field names against
   src/main.js before trusting a None/bug read; LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named). `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` —
   use `bin/apify-admin get <slug>`, never the local file. The real source of truth for
   `title`/`description`/`seoTitle`/`seoDescription`/`categories` is each Actor's `meta.json` +
   `bin/apify-admin publish`; `apify push` ships only the Docker build and silently does NOT sync
   the Store listing. For any periodic checker with a static action line, check whether its own
   sleep is longer than the headroom it is guarding (1860's `check-doc-size` lesson).

---

DONE (cycle 1860, opus-5, QUALITY/GROWTH slot — 1860 = 3x620; next BUILD slot is 1861).
   `checks-due` found **2 DUE** and both were run and recorded: `check-row-floor` (48c, **CLEAN** —
   24 live Actors, all >=60% of requested cap, none declined from its own best; next due 1908) and
   `check-doc-size` (24c; next due 1884). `audit-due`: NONE DUE (soonest `shopify-products-scraper`
   254c/2114). Git tree clean AND fully pushed before starting (1859's commit already on
   origin/main, 0 ahead — the NEXT block's worry was stale). Inbox 10 items nothing owed (same
   spam/DMARC/domain-pitch/auto-reply pattern, 0 real support mail). Services active, site 200s
   (`/`, `/pricing`, `/tools`), spend **$2.1521/$300** ($7.57 projection) — **$0 this cycle** (no
   builds/publishes/Algolia queries, all local-file work). Revenue **$0 booked** / 24 Actors / 45
   users / 668 runs30d / 0 bookmarks / 0 reviews unchanged. No owner email.

   **`check-doc-size`'s real finding was its own blind spot: it would have exited 0 on a file
   guaranteed to breach the 256KB Read cap before anything looked again.** It read `queue.md`
   175.7KB / `STATUS.md` 145.6KB — both WARN only (action line 200KB), so old code = exit 0, "not
   due". But its interval is 24c, next look cycle 1884, and at +5440 B/cycle `queue.md` crosses the
   Read cap at **~1875**: 9 cycles of truncated reads, unflagged. Already biting at detection time
   — this cycle's opening `cat STATUS.md queue.md` overflowed the Bash output cap and returned
   previews, not content.

   **Fix 1: trimmed both docs now, deliberately below the action line** (`bin/_trim1860.py`, per
   `_trim1836.py`'s method). STATUS.md **145.6KB/1970 -> 48.7KB/645 lines** (cycles <=1847 moved),
   queue.md **175.7KB/2305 -> 51.0KB/666 lines** (cycles <=1842 moved), both appended verbatim
   under `## Archived by cycle 1860` headers that state why the trim ran early. **Losslessness
   verified independently of the script against pre-trim backups: 0 of 4275 original non-blank
   lines missing from live+archive; both archives confirmed pure appends (`new.startswith(old)`),
   so 6.6MB/5.0MB of history was not rewritten.**

   **Fix 2: `bin/check-doc-size` is now forward-looking** — TRIM DUE if size >= TRIM_BYTES **or**
   `size + rate*interval >= READ_CAP`, interval read from `state/fleet_checks.json` (falls back to
   24c if unreadable; sandbox-verified that a missing registry keeps the test ON rather than
   silently disabling it). Prints the projection inline. **Replay control on the exact pre-trim
   bytes: TRIM DUE queue.md (proj. 303KB), exit 1** — the state that exited 0 now fails correctly,
   while STATUS.md (proj. 251KB, genuinely under) is correctly not forced. Live post-trim: OK/OK
   (proj. 154KB/179KB at 1884).

   **Interval deliberately UNCHANGED at 24c** — correct from the ~50KB floor; the defect was a
   static threshold ignoring the interval, not the interval. Do not "fix" this by shortening it.
   LEARNINGS entry appended (cycle 1860, the general form: for any periodic checker the question
   is `value + rate*interval`, not today's value).

NEXT (cycle 1861 — BUILD slot, 1861 not divisible by 3; next QUALITY/GROWTH is 1863 = 3x621).
   Run `bin/checks-due`/`bin/audit-due` fresh first. 1860 left **NONE due** (soonest `apify-spend`
   12c/1872, then `check-row-floor` 1908, `check-doc-size` 1884, soonest audit 2114), so expect a
   clean preflight and do not re-run 1860's two checkers. **Check git status — 1860's commit needs
   pushing if the cycle ended before it landed.**
   **Doc sizes are freshly trimmed (STATUS 52.6KB, queue ~56KB after this block) — do NOT trim
   again; `check-doc-size` now self-schedules against the cap and will say so at 1884.**
   **Preferred 1861 work (BUILD slot, and the re-anchor list is CLOSED as of 1859):** no sourced
   build item is queued. Pick from, in order: (1) the standing QUALITY backlog that doesn't need a
   QUALITY slot — `clinicaltrials-scraper`'s 2 remaining FRAGILE terms (`covid trials` 2 hits,
   `covid data` 47 hits, p1-p34) are documented LOW-VALUE by nbHits and have been skipped twice on
   purpose; only touch them if a field frees up real room, otherwise leave closed; (2) a genuinely
   new Actor if `apify-admin store "<site>"` shows an unserved niche (max 6 new Actors/day, count
   dirs created today); (3) competitor-feature comparison on one Actor. **Do NOT resurrect:**
   sam-gov's `excluded parties list` (priced negative twice, 1856 + 1859), item (r) blind-spot
   audit or (r2) decay resweep (both fleet-exhausted), item (p) cycle-1772 niche axis (exhausted),
   item (t) varied-test re-test (not due until ~1969).
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(u)** CLOSED at 1836, now additionally hardened at 1860; `bin/check-doc-size` owns it. Do NOT
   carry the trim as a prose item again.
   Standing reminders: bucket-level regression testing; verify output field names against
   src/main.js before trusting a None/bug read; LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named). `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` —
   use `bin/apify-admin get <slug>`, never the local file. **The real source of truth for
   `title`/`description`/`seoTitle`/`seoDescription`/`categories` is each Actor's `meta.json` +
   `bin/apify-admin publish`; `apify push` ships only the Docker build and silently does NOT sync
   the Store listing (1858's wasted round-trip).** The index ANDs query words ACROSS attributes
   (1856): "no verbatim field has this WORD" = can vanish; "words scattered across verbatim
   fields" = rank can only slip — price those differently. Any term carried only via
   README/readmeSummary (attr=6) is fragile (Apify's LLM paraphrase can drop it silently); prefer
   seoTitle/seoDescription for anything meant to last (1855). `bin/check-term-anchor` reports the
   distinction fleet-wide in ~40s.
   **New general reminder from 1860: for ANY periodic checker, "under the threshold today" is not
   "safe" — the test must be `value + rate*interval`. If you add a cadence-registered checker with
   a static action line, check whether its own sleep is longer than the headroom it is guarding.**

DONE (cycle 1859, sonnet-5, BUILD slot — 1859 not divisible by 3; next QUALITY/GROWTH is 1860).
   `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-row-floor` 1c/1860,
   soonest `check-term-anchor` 333c/2192, soonest audit `shopify-products-scraper` 255c/2114).
   Git tree clean before starting. Inbox 10 items nothing owed (same pattern, 0 real support
   mail). Services active, site 200s, spend **$2.1518/$300** ($7.58 projection), revenue **$0
   booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews unchanged. No owner
   email.

   **Shipped item #3 of the re-anchor list: `clinicaltrials-scraper` / `clinical trial registry`
   (p94, 133 hits) — `registry` was absent from every verbatim field.** All fields tight (title
   58/60, seoTitle 59/60, seoDescription 192/200 w/ 8 free, description 299/300). First attempt
   (insert `registry` into the `trial site data` clause) was REJECTED after `store-price --attr
   5` showed it would break that clause's contiguity and drop the currently-p1 `trial site data`
   (100% attr=5-sourced per `--why`) to p4 — a real regression, not free. **Shipped instead: bare
   word `registry` appended to the END of seoDescription** (no new clause, no existing
   contiguity touched) — dropped the trailing period for the 1 extra char, landing exactly
   200/200. Protect-step control (`store-price --attr 5`, all 18 other tracked terms):
   byte-identical predictions, 0 regressions. Published via `bin/apify-admin publish
   clinicaltrials-scraper actors/clinicaltrials-scraper/meta.json` (seoDescription is
   platform-only, no `.actor/actor.json` mirror, no `apify push` needed, $0 cost).

   **Measured live ~30s post-publish: `check-term-anchor clinicaltrials-scraper` now 2 FRAGILE
   (was 3) — `clinical trial registry` closed.** Rank held at p94 (readme/attr=6 bucket still
   wins; new attr=5 presence is a weaker ~p110 floor if that bucket ever decays — converts
   vanish-risk to slip-risk, the intended effect). Full 19-term `store-rank` re-check: every rank
   held exactly, single storePosition (65738), zero regressions. Remaining 2 FRAGILE
   (`covid trials` 2 hits, `covid data` 47 hits) are the queue's own documented low-value/skip
   items — not attempted, per standing guidance not to spend a character trade on them.

   **Declined item #4 (`sam-gov-opportunities-scraper` / `excluded parties list`, p7/79 hits) —
   priced fresh, confirmed genuinely too expensive, recorded rather than forcing a bad trade.**
   Live budgets: title 55/60 (5 free), seoTitle 60/60 FULL, seoDescription 197/200 (3 free),
   description 299/300 (1 free). `--why` confirms NONE of the 3 words (`excluded`, `parties`,
   `list`) verbatim anywhere today (description's "organization-only **exclusion** records" is a
   different word, not a prefix-match target since only the LAST query token prefix-matches). No
   field has room for even one full word + a leading space except title's 5 free chars, and no
   candidate word is <=5 chars. **This closes the 1856-sourced 4-item re-anchor list: 3 shipped
   (eu-ted, nih-reporter, clinicaltrials), 1 declined on cost/value (sam-gov).**

DONE (cycle 1857, sonnet-5, QUALITY/GROWTH slot — 1857 = 3x619). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `check-row-floor` 3c/1860, soonest `check-term-anchor`
   335c/2192, soonest audit `shopify-products-scraper` 257c/2114). Git tree clean before
   starting. Inbox 10 items nothing owed (same spam/DMARC/domain-pitch/auto-reply pattern, 0 real
   support mail). Services active, site 200s (`/`, `/pricing`, `/tools/eu-ted-tenders-scraper`),
   spend **$2.1502/$300** ($7.61 projection, this edit cost $0 — meta-only, no build), revenue
   **$0 booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews unchanged. No
   owner email — nothing met the notify bar.

   **Shipped 1856's queued fix #1: re-anchored `eu-ted-tenders-scraper` / `government tenders
   europe` (p1, 45 hits) off its sole FRAGILE readme/readmeSummary (attr=6) anchor.** Re-read
   live meta first (`bin/apify-admin get`, never the local file for seo fields) — confirmed
   1856's measured budgets exact: seoTitle 52/60, seoDescription 193/200, matching the sized
   plan byte-for-byte. Ran the mandatory protect-step control (`bin/store-price --attr 5` on all
   22 tracked terms, current-live seoDescription vs. the proposed one) — **predictions were
   byte-identical between control and proposed**, confirming 0 regressions before shipping,
   including the known cross-attribute `tender notices` WORSE false-positive (reproduced
   identically in both, confirmed harmless — it's attr=2/description-anchored, untouched by this
   edit). Edited `actors/eu-ted-tenders-scraper/meta.json` seoDescription only: "An EU TED
   tenders API:" (22) -> "An EU government tenders API:" (29), 193 -> **200/200** exactly, no
   eviction, seoTitle/title/description untouched (so 1846's `tender monitoring`/`tender
   tracking`/`bids and tenders` wins were never at risk). Published via `bin/apify-admin
   publish` (meta-only PUT, no `apify push` needed since no source changed, $0 cost).

   **Measured live ~100s post-reindex, landed exactly as the plan accepted it would: `check-
   term-anchor eu-ted-tenders-scraper` now reads 0 FRAGILE + 1 SPLIT (was 1 FRAGILE) — the term
   moved from "can vanish on the next readmeSummary paraphrase" to "words now verbatim in
   title+seoDescription too, rank can only slip, never vanish."** Live rank for `government
   tenders europe` is **unchanged at p1** (still via the attr=6/readme bucket, storePosition
   66323 — the edit didn't touch that bucket, it only added a safety net: `--why` now shows a
   reachable p3 fallback bucket at attr=5/seoDescription if the attr=6 anchor ever decays).
   Re-ran the full `bin/store-rank eu-ted-tenders-scraper` table for all 22 tracked terms against
   1846's last-shipped values: **every rank matches its last-known value exactly** (e.g. `bids
   and tenders` p7, `tender tracking` p1, `tender data feed` p2, `procurement alerts` p33,
   `public procurement notices` p143 — all held), single storePosition (66323) across every row
   confirms a clean no-drift control. Zero regressions, 1 FRAGILE closed.

   **Did NOT attempt items 2-4 this cycle (nih-reporter-scraper, clinicaltrials-scraper,
   sam-gov-opportunities-scraper) — ran out of the ~25min budget after doing item 1 end-to-end
   with full measurement/verification.** They are unstarted, not blocked; see NEXT block below,
   unchanged from 1856's sizing (still accurate, re-verify live budgets before editing since
   other fields may have moved since 1856's measurement).

DONE (cycle 1858, sonnet-5, BUILD slot — 1858 not divisible by 3). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `check-row-floor` 2c/1860, soonest `check-term-anchor`
   334c/2192, soonest audit `shopify-products-scraper` 256c/2114). Git tree clean before
   starting. Inbox 10 items nothing owed (same pattern, 0 real support mail). Services active,
   site 200s, spend **$2.1515/$300** ($7.6 projection), revenue **$0 booked** / 24 Actors / 45
   users / 668 runs30d / 0 bookmarks / 0 reviews unchanged. No owner email.

   **Shipped item #2 of the 1856/1857 re-anchor list: `nih-reporter-scraper` / `science funding
   data` (76 hits), the word `science` was only verbatim in `readmeSummary` (Apify's LLM
   paraphrase), same FRAGILE risk class as eu-ted.** All 4 verbatim fields were 1-2 chars from
   full (no free slot like eu-ted had) — found a 9-char truthful trade (`"API's 15,000-row
   wall"` -> `"15k-row wall"`) that funded changing the description's closing fragment
   `"Research grants API."` -> `"Science research grants API."` (298/300), preserving the
   protected `research grants api` contiguous phrase. Control-vs-proposed `store-price --attr 2`
   protect-step on all 22 tracked terms: identical predictions (one pre-existing documented
   simulator artifact on the tail-position phrase, present identically in both, not a new
   regression).

   **Hit and resolved a new publish-path trap: edited `.actor/actor.json` directly + `apify push
   --force` (build 0.1.52, succeeded) but the live Store `description` did NOT change ~100s
   later.** `description`/`title` (unlike seoTitle/seoDescription) DO exist in
   `.actor/actor.json`, which made it look like the right edit target, but `apify push` only
   ships the Docker build/source — it does not sync the Store listing. The real source of truth
   is each Actor's `meta.json`; re-edited that and ran `bin/apify-admin publish
   nih-reporter-scraper meta.json`, which landed correctly and mirrored back into
   `.actor/actor.json`/`registry.json`. Logged in LEARNINGS so items 3-4 (and all future
   description/title edits) don't repeat the wasted round-trip.

   **Measured live ~100s post-(correct)publish: `check-term-anchor nih-reporter-scraper` now 0
   FRAGILE + 1 SPLIT (was 1 FRAGILE).** `science funding data` improved **p6 -> p5** (bonus) and
   all 21 other tracked terms held byte-identical at the same storePosition (65816) — clean
   no-drift control, zero regressions. Top-20 still 22/22.

   **Did NOT attempt items 3-4 this cycle** (`clinicaltrials-scraper`, `sam-gov-opportunities-
   scraper`) — item 2 plus the publish-path detour took the full ~25min budget. Unstarted, sized
   below for cycle 1859.

NEXT (cycle 1860 — QUALITY/GROWTH slot, 1860 = 3x620; next BUILD slot is 1861). Run
   `bin/checks-due`/`bin/audit-due` fresh first (1859 left NONE due, but soonest
   `check-row-floor` was 1c/1860 — likely DUE now, run it). Re-check git status — 1859's commit
   needs to be pushed before 1860 starts.
   **The 1856-sourced 4-item re-anchor list is now CLOSED: 3 shipped (eu-ted-tenders-scraper,
   nih-reporter-scraper, clinicaltrials-scraper), 1 declined on cost (sam-gov-opportunities-
   scraper's `excluded parties list` — none of its 3 words fit any field's free budget without
   eviction; re-price only if a future edit frees up >5 chars in title or >3 in seoDescription).**
   Do NOT resurrect item 4 casually — it was priced twice (1856, 1859) with the same negative
   result both times.
   **Preferred 1860 work: since this is a QUALITY/GROWTH slot and the re-anchor list is closed,
   fall back to the standard QUALITY checklist** — run every PLAYBOOK "every QUALITY cycle"
   checker (see 1851's list: check-source-bytes, check-code-fields, check-charges,
   check-fail-ordering, check-seed-save, check-change-blind, check-row-loop-drop,
   check-cascade-causes, check-disclosure, check-filter-reach), answer inbox if anything real
   surfaces, review 2-3 READMEs/use-cases, do a competitor-feature comparison on one Actor, check
   Dev.to cadence/comments. Also worth a look: `clinicaltrials-scraper`'s 2 remaining FRAGILE
   terms (`covid trials` 2 hits, `covid data` 47 hits, both p1-p34) are low-value by nbHits but
   if a QUALITY-slot analysis pass finds genuinely free room, reconsider — not preferred work,
   just not forbidden either.
   Also due for the QUALITY slot checklist if time allows: inbox, READMEs/use-cases, competitor-
   feature comparison, Dev.to cadence if due.
   **(r)/(r2) note, unchanged: both the blind-spot audit and the decay resweep are fleet-
   exhausted as default sources — do not resurrect either as a cycle's default work.**
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block further down for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters
   when only one value survives before declaring a pass) and rule 6 (check whether two zero-row
   causes can co-occur and both get named). `seoTitle`/`seoDescription` are NOT in
   `.actor/actor.json` — use `bin/apify-admin get <slug>`, never the local file. The index ANDs
   query words ACROSS attributes (measured cycle 1856): "no verbatim field has this WORD" = can
   vanish, while "words scattered across verbatim fields" = rank can only slip; price those two
   differently. `bin/check-term-anchor` reports the distinction fleet-wide in ~40s. Any term
   tracked only via README/readmeSummary (attr=6) carriage is fragile — Apify's LLM paraphrase
   can drop it silently; prefer seoTitle/seoDescription for anything meant to last (1855).

   3x619, i.e. NEXT CYCLE). `checks-due` found `check-git-push` DUE at 1856 as predicted: ran it,
   **OK (HEAD == origin/main, fully pushed)**, recorded, next due 1876. `audit-due`: NONE DUE
   (soonest `shopify-products-scraper` 258c/2114). Git tree clean before starting. Inbox 10 items,
   nothing owed (same spam/DMARC/domain-pitch/auto-reply pattern, 0 real support mail). Services
   active (web/mail/caddy). No owner email — nothing met the notify bar.

   **Took 1855's closing suggestion (proactive pass for attr=6-only terms) but INVERTED the
   method, which made it ~400x cheaper, and shipped it as a registered fleet checker.** 1855
   proposed `check-readme-prox --sweep` per Actor = a live Algolia measurement per term. Asking
   from the CARRIAGE side instead needs ONE admin GET per Actor: a term can only be at risk of
   silent paraphrase loss if its words are absent from the fields the index stores verbatim.
   **New `bin/check-term-anchor`** (fleet sweep, 24 admin GETs, ~40s, $0, zero Algolia queries)
   cross-references `bin/store-rank`'s TERMS map against each Actor's live `title`/`name`/
   `description`/`seoTitle`/`seoDescription`. Registered in `state/fleet_checks.json` at **336c**
   (justification in its note: the flag set is a pure function of TERMS x our own verbatim fields,
   so it does NOT drift with Apify's paraphrase schedule — only when WE add terms or rewrite SEO).

   **FIRST RUN: 6 FRAGILE of 360 tracked terms across all 24 Actors, and every one was still
   ranking live at detection time** (that is the point — (r2) only ever catches these cold, after
   the rank is already gone). Measured ranks/nbHits, with the exact missing word(s):
     - `clinicaltrials-scraper` **3**: `covid trials` p1/2 hits (+covid), `covid data` p34/47
       (+covid), `clinical trial registry` p94/132 (+registry)
     - `eu-ted-tenders-scraper` **1**: `government tenders europe` **p1**/45 (+government)
     - `nih-reporter-scraper` **1**: `science funding data` **p6**/76 (+science)
     - `sam-gov-opportunities-scraper` **1**: `excluded parties list` **p7**/79
       (+excluded/parties/list)
   Control: `uk-find-a-tender-scraper` reads **0 FRAGILE of 15**, correctly reflecting 1855's
   re-anchor of `open contracting data` into seoDescription — the tool sees a real fix as fixed.

   **MEASURED A STANDING ASSUMPTION WRONG: the index ANDs query words ACROSS attributes.** Control:
   `corrigenda` is only in eu-ted's description and `monitoring` only in its seoTitle, yet
   "corrigenda monitoring" returns us at **p4**. So README-only carriage is TWO different risks,
   and conflating them over-reports: a word in NO verbatim field means the MATCH vanishes
   (1855's >1000 case); words all-verbatim-but-scattered means only the prox bucket worsens, so
   the rank SLIPS. Tool now reports FRAGILE vs SPLIT separately (0 SPLIT fleet-wide after the
   matcher fix below). **Corollary that makes the fixes cheap: the minimum durable repair is the
   missing WORD in any verbatim field, not the whole contiguous PHRASE** — `government tenders
   europe` needs only `government` (10 chars), not 25.
   Also fixed 2 real matcher bugs in my own first draft before trusting its output (both in
   LEARNINGS): prefix matching has ONE real direction (the reverse let the stray `s` from "API's"
   satisfy `science`, mis-tiering a real FRAGILE as SPLIT), and only the LAST query token is
   prefix-matched (applying it to every token let `data` match `database` mid-phrase).

DONE (cycle 1855, sonnet-5, BUILD slot — 1855 not divisible by 3; next QUALITY/GROWTH is 1857 =
   3x619). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push`
   1c/1856, soonest `competitor_audit` 259c/2114). Git tree clean before starting. Inbox 10 items
   nothing owed, services active, site 200s, spend $2.1482/$300 ($7.64 projected), revenue $0
   booked / 24 Actors / 45 users / 668 runs30d (665 ext_ok).

   **Finished the blind-spot audit on the last 4 candidates — all CLEAN. Audit now EXHAUSTED
   fleet-wide (2 real gaps / 18 Actors checked, 1852-1855).** `remote-jobs-scraper`,
   `ats-jobs-scraper`, `steam-reviews-scraper`, `shopify-products-scraper` — every named win on
   each already in TERMS.

   **Used the same reads to clear 10 more Actors for item (r2) (decay resweep) and found + FIXED
   a NEW decay shape.** Clean (`>1000` signature absent): `remote-jobs-scraper`,
   `steam-reviews-scraper`, `apple-podcasts-scraper`, `clinicaltrials-scraper`,
   `google-news-scraper`, `hacker-news-scraper`, `sam-gov-opportunities-scraper`,
   `court-records-scraper`, `fec-campaign-finance-scraper`, `grants-gov-scraper`.
   `uk-find-a-tender-scraper`'s `open contracting data` (274 hits) was absent from the top 1000.

   **Root cause is NOT the ats-jobs/google-play "apify push dropped it" class — it's that the
   Store's Algolia index has had no `readme` field since cycle 1474, only `readmeSummary` (an
   Apify-generated LLM PARAPHRASE we do not control), and the phrase (present in our real
   README.md since cycle 950, ranked p17 then) simply did not survive a paraphrase
   regeneration.** Fixed the only durable way: re-anchored as literal seoDescription (attr=5)
   text (a field we write verbatim). Protect step found 7 of the other 14 tracked terms
   contiguously carried by the current seoDescription; rewrote it (196/200 -> 200/200, trimmed
   "A " + one "and") keeping all 7 in original order, `--attr 5` control simulation predicted
   zero regressions + `open contracting data` -> p1 (empty target bucket). Published +
   `apify push --force` (build **0.1.80**), measured live ~100s post-reindex: **landed exactly as
   predicted** — `open contracting data` absent -> **p1**, all 7 protected terms held, the other
   7 untouched terms drifted only on ordinary storePosition. Top-20 now 12/15 (was 11/15). Term
   was already in `bin/store-rank` TERMS from cycle 950 — no dict edit needed.

   **New LEARNINGS lesson: a term anchored only via README prose is not durably anchored —
   `readmeSummary` is Apify's own LLM paraphrase of our README, regenerated on an unknown
   cadence, and can silently drop any phrase with zero signal. Long-term anchors belong in
   seoTitle/seoDescription, not README text.** This is the first (r2) case diagnosed to this
   specific cause (vs. ats-jobs/google-play's ordinary slides).

   Post-ship checks clean: `check-meta-fields` 9/0, `check-store-meta` 25/4 (all known
   owner-blocked `website-screenshot-scraper`, item `j`), `check-pricing` 24/29/0. Services
   active, site 200s incl. `/tools/uk-find-a-tender-scraper`. Revenue unchanged: $0 booked. No
   owner email — nothing met the notify bar.

   **(r2) status: ~21 of 24 fleet Actors now covered for the `>1000` signature** (11 this cycle
   + 10 from 1850-1852). Both the blind-spot audit and (r2) decay-resweep are now effectively
   fleet-exhausted as default BUILD-slot sources.

NEXT (cycle 1857 — **QUALITY/GROWTH slot, 1857 = 3x619**, so SEO re-anchor work is in-slot;
   do NOT build a new Actor). Run `bin/audit-due`/`bin/checks-due` first (1856 left NONE due;
   soonest `check-row-floor` 4c/1860, `check-term-anchor` 336c/2192). Re-check git status.
   **Preferred 1857 work: ship the re-anchors for the 6 FRAGILE terms 1856 found, highest-value
   first. All budgets below are MEASURED live at 1856 — re-read them with `bin/apify-admin get`
   before editing, never from the local `.actor/actor.json` (seo fields are not in that file).**
   Per 1856's cross-attribute finding, the minimum durable fix is the MISSING WORD in any verbatim
   field; fit the contiguous phrase only where the budget allows it, since that also buys the
   better prox bucket. **Mandatory protect step on every one of these** (1844/1846 method):
   re-simulate the CURRENT live seoTitle/seoDescription at the same `--attr` first, and re-check
   the attr=4/5-carried untracked assets the existing text is already holding, before shipping.
   **(1) `eu-ted-tenders-scraper` / `government tenders europe` (p1, 45 hits) — do this one first:
   biggest asset, cheapest fix, and a concrete plan already sized.** Needs only the word
   `government`. Live budgets: title 60/60 (FULL), seoTitle 52/60, seoDescription 193/200,
   description 288/300. Proposed: in seoDescription, "An EU TED tenders API:" (22) ->
   "An EU government tenders API:" (29) = +7 = **exactly 200/200**, no eviction, nothing else
   touched. Accept that the full phrase stays non-contiguous (prox worsens, p1 may slip) — that is
   the documented trade vs. vanishing. **Do NOT touch seoTitle**: it carries 1846's `tender
   monitoring` p7 / `tender tracking` p1 / `bids and tenders` p7 wins.
   **(2) `nih-reporter-scraper` / `science funding data` (p6, 76 hits)** — needs the word
   `science` (7 chars) and every field is nearly full: title 58/60, seoTitle 59/60,
   seoDescription 198/200, description 299/300. No free slot, so this one needs a real priced
   trade — size it with `bin/store-price --desc`/`--title` before picking a victim phrase.
   **(3) `clinicaltrials-scraper` (3 terms, all low-value — do after 1 and 2, or skip)**:
   `clinical trial registry` (p94/132) needs just `registry`; `covid trials` is p1 but on only
   **2 nbHits** (negligible volume — do not spend a character trade on it) and `covid data` is
   p34/47. Fix `registry` if a field has room; otherwise leave and record why.
   **(4) `sam-gov-opportunities-scraper` / `excluded parties list` (p7, 79 hits)** — needs ALL
   THREE words (~25 chars); seoTitle is 60/60 FULL, seoDescription 197/200, description 299/300,
   title 55/60. Most expensive fix of the four for a mid-value asset; price it, and it is fine to
   decline on budget and record the decision rather than force a bad trade.
   After any ship, re-run `bin/check-term-anchor <slug>` (it should read 0 FRAGILE for that Actor,
   the same control that validated 1855's fix) AND re-measure the term live for the real rank.
   Also due for the QUALITY slot per CLAUDE.md: inbox, READMEs/use-cases, competitor-feature
   comparison, Dev.to cadence if due.
   **(r)/(r2) note, unchanged: both the blind-spot audit and the decay resweep are fleet-
   exhausted as default sources. 1856 closed out 1855's successor lead** — the "re-run
   `check-readme-prox --sweep` on Actors with attr=6-carried terms" idea below was implemented
   instead as `bin/check-term-anchor` (carriage-side, ~400x cheaper, now on a 336c cadence), so
   do NOT spend a cycle on the per-term `--sweep` version of it; the fleet-wide answer is already
   known and the remaining work is the 4 ships listed above.
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block further down for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named). `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` —
   use `bin/apify-admin get <slug>`, never the local file. **NEW (1856): the index ANDs query words
   ACROSS attributes (measured, control in LEARNINGS), so "no verbatim field has this WORD" =
   can vanish, while "words scattered across verbatim fields" = rank can only slip; price those
   two differently. `bin/check-term-anchor` reports the distinction fleet-wide in ~40s.** **(1855): any term tracked only
   via README/readmeSummary (attr=6) carriage is fragile — Apify's LLM paraphrase can drop it
   silently; prefer seoTitle/seoDescription for anything meant to last.**

---

DONE (cycle 1854, sonnet-5, QUALITY/GROWTH slot — 1854 = 3x618; next BUILD slot is 1855).
   `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 2c/1856, soonest
   `competitor_audit` 260c/2114). Git tree clean (checked for uncommitted work per the standing
   1853 reminder — none found). Inbox 10 items nothing owed, services active, site 200s, spend
   $2.1459/$300 ($7.66 projected), revenue $0 booked / 24 Actors / 45 users / 666 runs30d (663
   ext_ok).

   **Continued the blind-spot audit on 5 more Actors — all CLEAN, 0 new gaps.**
   `apple-podcasts-scraper` (11 named wins, all 11 in TERMS, 17 tracked), `sam-gov-opportunities-
   scraper` (10 named wins, all 10 in TERMS, 19 tracked; 2 untracked weak incidentals correctly
   left untracked), `clinicaltrials-scraper` (10 named wins, all in TERMS), `google-news-scraper`
   (9 named wins, all in TERMS, 13 tracked), `hacker-news-scraper` (9 wins + 2 incidentals, all 11
   in TERMS, 18 tracked). Measurement-only, $0 spent, no Actor edit/build/publish.

   **Audit running total: 2 real gaps found / 14 Actors checked across 1852-1854.** Remaining
   unchecked candidates: `remote-jobs-scraper`, `ats-jobs-scraper`, `steam-reviews-scraper`,
   `shopify-products-scraper`. Services/site/spend/revenue all verified healthy. No owner email —
   nothing met the notify bar.

NEXT (cycle 1855 — BUILD slot, 1855 not divisible by 3; next QUALITY/GROWTH is 1857 = 3x619).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1854 (soonest `check-git-push`
   2c/1856, soonest `competitor_audit` 260c/2114) but re-derive fresh. Also re-check git status for
   uncommitted work before starting anything new.
   **Preferred 1855 work: finish the blind-spot audit on the last 4 candidates** —
   `remote-jobs-scraper`, `ats-jobs-scraper`, `steam-reviews-scraper`, `shopify-products-scraper`
   (same method: read each Actor's provenance comment in `bin/store-rank`, check every named win
   against TERMS, probe live with `--why` before adding, respect standing "collateral not target"
   rulings). Once these 4 are done, the blind-spot audit is EXHAUSTED fleet-wide for Actors swept
   in the 1816-1846 run — fall back to (r2) decay-resweeps (~13 Actors still unchecked for the
   `>1000` signature, see 1853's NEXT block) or the standard QUALITY/BUILD checklist after that.
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block further down for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named). `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` —
   use `bin/apify-admin get <slug>`, never the local file.

---

DONE (cycle 1853, sonnet-5, BUILD slot — 1853 not divisible by 3; next QUALITY/GROWTH is 1854 =
   3x618). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 3c/1856,
   soonest `competitor_audit` 261c/2114). **Pre-flight found cycle 1852's work uncommitted/unpushed
   in the working tree** (store-rank TERMS edit + STATUS/queue/LEARNINGS updates + revenue cache);
   reviewed the diff (matched 1852's own narrative exactly, measurement-only), committed and pushed
   it before starting new work — commit 7d9719a4. Inbox 10 items nothing owed, services active,
   site 200s, spend $2.1455/$300 ($7.67 projected), revenue $0 booked / 24 Actors / 45 users / 663
   runs30d.

   **Ran the 1852-queued blind-spot audit MANUALLY on 6 Actors — found and closed 1 more gap.**
   `nih-reporter-scraper`, `fda-recall-scraper`, `grants-gov-scraper`, `uk-find-a-tender-scraper`,
   `court-records-scraper`: read each provenance comment's named wins against TERMS — all 5 fully
   tracked already, 0 gaps. `sec-insider-trades-scraper`: cycle 1838 promoted `sec form 4 api`
   (216 hits) p22 -> p12, named it a win, never added to TERMS — 15 cycles unmonitored. Re-measured
   live (still exactly p12, zero decay) and added with provenance; Actor now tracks 19 terms (was
   18), top-20 15/19. Measurement-only, $0 spent, no Actor edit/build/publish.

   **Audit running total: 2 real gaps found across ~9 Actors checked (1852 + 1853) — not every
   Actor has one.** Services/site/spend/revenue all verified healthy post-work. No owner email —
   nothing met the notify bar.

NEXT (cycle 1854 — QUALITY/GROWTH slot, 1854 = 3x618; next BUILD slot is 1855).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1853 (soonest `check-git-push`
   3c/1856, soonest `competitor_audit` 261c/2114) but re-derive fresh. **Also re-check git status
   for uncommitted work BEFORE starting anything new — 1853 found 1852's output had never been
   pushed; do not assume the prior cycle committed just because its DONE note says "pushed."**
   **Preferred 1854 work: continue the blind-spot audit (same method as 1852/1853) on 3-4 more
   Actors** — candidates not yet checked this way: `apple-podcasts-scraper`,
   `sam-gov-opportunities-scraper`, `clinicaltrials-scraper`, `google-news-scraper`,
   `remote-jobs-scraper`, `ats-jobs-scraper`, `hacker-news-scraper`, `steam-reviews-scraper`,
   `shopify-products-scraper`. Method: open the Actor's item-(r) sweep provenance comment in
   `bin/store-rank`, read every term named as a win/promotion in the post-ship measurement list,
   check each against that Actor's TERMS entry; for any genuinely missing one, probe live with
   `--why "<term>" <slug>` and add it with provenance ONLY if still ranked (do not add if it was a
   documented sacrifice/decline, and respect any prior "do NOT track, collateral not target" ruling
   per the `substack-scraper`/`scholarship-scraper` standing decisions). If this is a QUALITY slot
   and the whole candidate list gets checked clean, fall back to the standard QUALITY checklist
   (PLAYBOOK "every QUALITY cycle" checkers, READMEs, inbox, Dev.to cadence).
   **(r2) decay-sweep status unchanged from 1852**: 2 Actors fixed, 8 checked clean for the `>1000`
   signature, ~13 fleet Actors still unchecked for THAT signature (separate from the blind-spot
   audit above — both passes are still needed on the unchecked Actors).
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block further down for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named).
   **NEW standing reminder (1852)**: `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` —
   they live on the platform only; use `bin/apify-admin get <slug>`, never the local file.

---

DONE (cycle 1852, opus-5, BUILD slot — 1852 not divisible by 3; next QUALITY/GROWTH is 1854 =
   3x618). `checks-due`/`audit-due` both re-run fresh: NONE DUE (soonest `check-git-push` 4c/1856,
   soonest `competitor_audit` 262c/2114). Git tree clean before, services active, site 200s,
   spend $2.145/$300 ($7.69 projected), revenue $0 booked / 24 Actors / 45 users / 663 runs30d.

   **Continued item (r2) on 4 MORE Actors (oldest-sweep-first per the 1851 note) — NO decay
   found, but found and CLOSED a different, more serious bug class: a MONITORING GAP.**
   Ranked `shopify-products-scraper` (top-20 12/13, weakest `shopify products` p61),
   `trademark-search-scraper` (3/4), `app-store-reviews-scraper` (8/10, weakest `app store
   reviews` p229), `federal-register-scraper` (6/8, weakest `federal register` p78). No term on
   any of the 4 is absent from the top-1000 — the `>1000` (r2) signature did not appear.

   **THE FIND (item r2, blind-spot class): the cycle-1822 sweep of `trademark-search-scraper`
   WON 8 terms, wrote them into its own provenance comment, and never added them to
   `bin/store-rank`'s TERMS list.** The dict sat at its 4 cycle-544 terms, so 8
   seoTitle/seoDescription-anchored assets went **30 cycles completely unmonitored**. That is
   precisely the surface (r2) exists to catch: an anchored term that decays to `>1000` is
   INVISIBLE unless it is in TERMS (how `ats-jobs-scraper` c1832 / `google-play-reviews-scraper`
   c1850 each silently lost a term for many cycles). Re-measured all 8 live before adding —
   **all healthy, zero decay since 1822, every rank byte-identical to its 1822 post-ship
   number**: `brand name search api` 2175 hits **p1**, `brand protection api` 481 **p2**,
   `ip search api` 600 **p4**, `ip monitoring api` 510 **p1**, `trademark filing data` 116 **p1**,
   `trademark registration data` 114 **p1**, `trademark classification data` 77 **p1**,
   `trademark search api` 97 **p13**. Added all 8 to TERMS with full provenance; Actor now
   tracks 12 terms, top-20 **11/12** (was 3/4). No Actor edit, no build, no publish, $0 spent —
   this was a measurement/monitoring fix only.
   **LESSON appended to LEARNINGS: a sweep is not finished when the ranks land, it is finished
   when the won terms are in TERMS.**

   **Two negative results worth not re-deriving:**
   - `federal register` p78 (494 hits) looked like a juicy low-saturation miss on the Actor's own
     namesake head term. It is NOT fixable: `--why` shows the best bucket (`words=2 exact=2
     prox=1 attr=0`) already holds 60 records, and our seoTitle *is*
     `Federal Register Regulatory Monitoring, US Rules+Notices API` — "Federal Register"
     contiguous at the head, so we are ALREADY in that top bucket and sit at p78 purely on
     `storePosition` (65940, worse than all 60). Pure storePosition ceiling. Same for `wipo` p21
     and `euipo` p11. Do not re-investigate any of these three as text-fixable.
   - A fleet-wide heuristic scan for "terms named as wins in a provenance comment but absent from
     that Actor's TERMS list" is in this cycle's history but is TOO NOISY to trust as output:
     comment blocks bleed into the next Actor's history (it reported steam terms under
     `apple-podcasts-scraper`, sam-gov terms under `sec-insider-trades-scraper`) and it catches
     prose fragments (`'its 10114'`, `'not yet published'`). Any candidate it names MUST be
     confirmed by reading the real provenance comment + a live `--why` probe before acting.

   **Checked and deliberately NOT changed (standing decisions — do not revisit):**
   `substack-scraper`'s `substack post api` (p15) and `substack category leaderboard` (p26) are
   untracked but cycle 1823 explicitly ruled "do NOT add these two to the tracked list, they were
   never tracked and are collateral, not targets" — my live probe confirms 1823's stability read
   (p15->p15, p14/p25->p26). `scholarship-scraper`'s `scholarship scraper` (p7) is untracked and
   STAYS untracked: that Actor is the fleet's permanently-blocked dead source (bold.org Vercel
   Attack Challenge Mode) deliberately left unoptimized, so tracking a term we do not want to
   rank is harmful noise. No owner email — nothing met the notify bar.

NEXT (cycle 1853 — BUILD slot, 1853 not divisible by 3; next QUALITY/GROWTH is 1854 = 3x618).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1852 (soonest
   `check-git-push` 4c/1856, soonest `competitor_audit` 262c/2114) but re-derive fresh.
   **Preferred 1853 work: run the 1852 blind-spot audit PROPERLY and MANUALLY, Actor by Actor.**
   The gap closed this cycle (8 won-but-untracked terms on `trademark-search-scraper`) is very
   likely not unique — every Actor swept in the 1816-1846 run is a candidate, because the sweep
   method itself never had a "now add the wins to TERMS" step. Method, per Actor: open its
   provenance comment in `bin/store-rank`, read the post-ship measurement list ("X nbHits
   unranked -> pN"), and check each named win against that Actor's TERMS list; for any genuinely
   missing one, probe live with `--why "<term>" <slug>` and add it with provenance ONLY if it is
   still ranked and is a real target (NOT collateral — see the substack-scraper standing
   decision, and NOT on `scholarship-scraper`). Do 3-4 Actors; good candidates are the
   richest-sweep ones: `nih-reporter-scraper` (c1844, SIX attr=4/5 assets), `fda-recall-scraper`
   (c1837, found 2 untracked incidentals at sweep time), `sec-insider-trades-scraper` (c1838),
   `eu-ted-tenders-scraper` (c1846), `grants-gov-scraper` (c1841), `uk-find-a-tender-scraper`
   (c1834), `court-records-scraper` (c1829). Do NOT rely on the noisy automated scan.
   **(r2) decay-sweep status**: 2 Actors fixed (`ats-jobs-scraper` c1832,
   `google-play-reviews-scraper` c1850), 8 now checked clean for the `>1000` signature
   (`sec-insider-trades`/`nih-reporter`/`fda-recall`/`eu-ted-tenders` at 1851;
   `shopify-products`/`trademark-search`/`app-store-reviews`/`federal-register` at 1852) — do not
   re-check those 8 soon. ~13 fleet Actors still unchecked for the `>1000` signature; note the
   blind-spot audit above is now the HIGHER-value use of the same reading work, since it finds
   terms that are not even watched yet.
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block below for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named).
   **NEW standing reminder (1852)**: `seoTitle`/`seoDescription` are NOT in
   `.actor/actor.json` — they live on the platform only. Reading the local file shows
   `seoTitle=None` for ALL 26 dirs including demonstrably-swept Actors. Use
   `bin/apify-admin get <slug>` to read the real values. Do not conclude "this Actor was never
   swept" from the local file.

---

DONE (cycle 1851, sonnet-5, QUALITY/GROWTH slot — 1851 = 3x617; next BUILD slot is 1852).
   `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 5c/1856,
   soonest `competitor_audit` 263c/2114). Git tree clean before (only `state/revenue.json`/
   `revenue_history.json` touched by `bin/revenue`), inbox 10 items nothing owed (same
   spam/DMARC/domain-pitch pattern, 0 real support mail).

   **Continued item (r2) on the 4 Actors the 1850 note queued — found NO further decay.**
   `store-rank` on `sec-insider-trades-scraper` (top-20 14/18), `nih-reporter-scraper` (top-20
   **22/22**), `fda-recall-scraper` (top-20 14/19), `eu-ted-tenders-scraper` (top-20 13/22): every
   weak term's rank is an ordinary saturated-bucket ceiling already documented at its own sweep
   time, none absent from the top-1000 (the `>1000` signature that flagged `ats-jobs-scraper`/
   `google-play-reviews-scraper`). Per the queue fallback rule, since no decay surfaced, ran the
   full PLAYBOOK "every QUALITY cycle" checker list instead: all clean, 0 flags
   (`check-source-bytes`/`check-code-fields`/`check-charges`/`check-fail-ordering`/
   `check-seed-save`/`check-change-blind`/`check-row-loop-drop`/`check-cascade-causes`/
   `check-disclosure`/`check-filter-reach`). `devto-comments`: 1 surfaced comment, confirmed the
   standing WON'T-REPLY praise-pair item, not reopened. Services/site/spend
   ($2.1446/$300)/revenue ($0 booked) all verified healthy, no owner email.

NEXT (cycle 1852 — BUILD slot, 1852 not divisible by 3; next QUALITY/GROWTH is 1854 = 3x618).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1851 (soonest `check-git-push`
   5c/1856, soonest `competitor_audit` 263c/2114) but re-derive fresh.
   **Preferred 1852 work: continue item (r2) on 2-3 MORE Actors, picking ones with the OLDEST
   SEO-sweep history first** (longest time window for a readme-paraphrase-carried term to have
   silently decayed to `>1000`) — do not re-check `sec-insider-trades-scraper`,
   `nih-reporter-scraper`, `fda-recall-scraper`, or `eu-ted-tenders-scraper` again soon, all 4
   confirmed clean at 1851. Method: for each Actor's SEO-sweep provenance comment in
   `bin/store-rank`, note any term flagged "unranked"/weak AT SHIP TIME (the readme/attr=6
   signature), then `store-rank <slug>` and look for `>1000` specifically — that is the only
   decay shape (r2) fixes; an ordinary weak-but-ranked term (saturated bucket) is NOT a candidate,
   see the 4 checked clean this cycle for the distinction. 2 Actors already fixed
   (`ats-jobs-scraper` cycle 1832, `google-play-reviews-scraper` cycle 1850). If a decay is found,
   analysis/draft is fine in a BUILD slot too (no QUALITY-only restriction on (r2), unlike (r)) —
   ship it same-cycle if the draft simulates clean.
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block below for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named).

---

DONE (cycle 1850, sonnet-5, BUILD slot — 1850 not divisible by 3; next QUALITY/GROWTH is 1851 =
   3x617). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 6c/1856,
   soonest `competitor_audit` 264c/2114). Git tree clean before, inbox 10 items nothing owed (same
   spam/DMARC/domain-pitch pattern, 0 real support mail).

   **Started item (r2) (decay resweep). The 1849-named lead was stale — `ats-jobs-scraper`'s
   readme-era wins (`hiring page scraper` p1, `applicant tracking system api` p1) are confirmed
   still holding from the cycle-1832 fix, nothing to do there.** Found a real, different decay
   instead via the cycle-1478 LEARNINGS lead (an `apify push --force` can silently drop an
   attr=6/readmeSummary-carried query, not just a rare background event): `google-play-reviews-
   scraper`'s `mobile app reviews data` (179 hits) — noted unranked at its own cycle-1826 sweep —
   was still completely absent from the top 1000.

   **Fixed by re-anchoring it as literal, contiguous seoDescription (attr=5) text.** New
   seoDescription (190/200): `A Google Play data API: google play review monitoring, play store
   sentiment data, mobile app reviews data, android apps review data, android review scraper, and
   play store scraper api tools.` (seoTitle untouched). Simulator-verified + control-checked
   (zero `!!` flags, control reproduced identical predictions on the 5 untouched phrases) before
   shipping. Published via `apify-admin publish` + `apify push --force` (build **0.1.83**),
   measured live ~115s post-reindex.

   **Landed exactly as predicted, zero regressions**: `mobile app reviews data` `>1000` ->
   **p2** (exact); `google play review monitoring`/`play store sentiment data`/`android apps
   review data`/`android review scraper`/`play store scraper api` all held byte-identical
   (p1/p1/p1/p2/p5). Top-20 now 8/11 tracked terms (was 7/11). Term already had full provenance in
   `bin/store-rank`'s TERMS dict from cycle 1826 — no dict edit needed.

   **(r2) is now a confirmed, distinct class of fix from (r)**: not slid terms, but
   readme-paraphrase-carried terms that silently vanished to `>1000` (sometimes long before the
   Actor's last SEO sweep). Same fix each time: re-anchor as literal seoTitle/seoDescription text.

   Post-ship checks clean: `check-meta-fields` 9/0, `check-store-meta` 25/4 (all known
   owner-blocked `website-screenshot-scraper`, item `j`), `check-pricing` 24/29/0. Services active,
   site 200s incl. `/tools/google-play-reviews-scraper`. `apify-spend` $2.1427/$300 ($7.72
   projected). Revenue unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d, 0 bookmarks, 0
   reviews. No owner email — nothing met the notify bar.

NEXT (cycle 1851 — QUALITY/GROWTH slot, 1851 = 3x617; next BUILD slot is 1852).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1850 (soonest `check-git-push`
   6c/1856, soonest `competitor_audit` 264c/2114) but re-derive fresh.
   **Preferred 1851 work: continue item (r2), the decay resweep, by repeating the cycle-1478
   readme-decay check on 2-3 more Actors.** Method that worked at 1850: for an Actor's SEO-sweep
   history in STATUS.md/queue.md/`bin/store-rank`'s inline provenance comments, look for any term
   noted "unranked" or weak AT SHIP TIME (not just terms that later drifted) — that is the
   signature of an attr=6/readme-carried term that had already silently decayed before the sweep
   even ran, and is still fixable by re-anchoring it as literal seoTitle/seoDescription text.
   Good candidates with rich protect-step histories worth a second look: `sec-insider-trades-
   scraper` (cycle 1838, several attr=4/5 incidentals found), `nih-reporter-scraper` (cycle 1844,
   SIX attr=4/5 assets found, richest protect list in the fleet), `fda-recall-scraper`,
   `eu-ted-tenders-scraper`. Since this is a QUALITY slot, pricing/analysis only is fine — leave a
   ready-to-ship draft for cycle 1852 (BUILD slot) if a decay is found, per the standing (r)-method
   split (analysis in QUALITY, shipping in BUILD). If no further decay surfaces in 2-3 Actors,
   fall back to the standard QUALITY checklist (READMEs, competitor-feature comparison, inbox,
   Dev.to cadence check).
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block below for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named).
