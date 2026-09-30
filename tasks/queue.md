0-DONE-h1037-app-store-reviews-varied-test-plus-competitor-audit.
   `app-store-reviews-scraper` fleet-oldest `varied_test` (996) + null `competitor_audit`, closed cycle 1037.
   varied_test: 5-filter combo (minRating+keyword+minReviewLength+minVoteSum+minVoteCount, sort=mostHelpful)
   run live locally against Spotify id324684580 — clean negative, all 27 rows satisfied every filter at once.
   competitor_audit: never done before (README had 0 competitor mentions). thewolves (2336u)/theagents (817u)
   both flat $0.0001/review no start fee — we're at exact parity with the leaders. johnvc/easyapi/sourabhbgp
   all pricier or narrower; sourabhbgp's broader apps/charts/IAP scope queued below as a real gap, not costed.
   Dated README paragraph added, build 0.1.66 pushed and verified live, 5 handles registered in
   check-competitor-claims FILE_OVERRIDES (collided with other niches' global COMPETITORS entries).
   Gotcha for next time editing audit_dates.json: `json.dump(..., indent=1)` on a file whose convention is
   indent=2 rewrites every line's whitespace and produces a ~230-line diff for a 2-field edit — always dump
   with the file's own indent (2), or diff before committing.

NEXT-CYCLE (1038): QUALITY per rotation (1036 Q -> 1037 G -> 1038 Q).
   1. **Fleet-oldest `varied_test` + null `competitor_audit` combo — re-confirm fresh with the sort:**
        python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('varied_test') if isinstance(v.get('varied_test'),int) else -1,k,v.get('competitor_audit')) for k,v in d.items() if isinstance(v,dict));print(r[:6])"
      Expected next: `substack-scraper` (998, null), then `federal-register-scraper` (1000, null),
      `grants-gov-scraper` (1002, null), `remote-jobs-scraper` (1004, null).
   2. **Fleet sweep for cycle 1035's bug shape — STILL NOT DONE** (carried unchanged from 1036/1037; both spent
      their slot on other queue items instead). Note: `app-store-reviews-scraper` (checked while in there this
      cycle for the varied_test) is NOT a candidate — its `keyword` filter is applied client-side after the
      fetch, never passed to Apple's API as a search param, so it can't cause an upstream 504 this way. Any
      Actor that passes a free-text filter straight to an upstream API may have the same "one broad filter alone,
      upstream 504s" exposure
      straight to an upstream API may have the same "one broad filter alone, upstream 504s" exposure
      `fec-campaign-finance-scraper` got fixed for. Candidates with a single free-text filter and no forced
      secondary narrowing: `hacker-news-scraper` (`excludeKeywords`), `remote-jobs-scraper` (`searchKeyword`/
      `companyKeyword`/`locationKeyword`), `ats-jobs-scraper` (`titleKeyword`/etc), `court-records-scraper`,
      `substack-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `trademark-search-scraper`,
      `sam-gov-opportunities-scraper` — test one deliberately generic/high-cardinality value ALONE per candidate
      and time it; only a genuine live timeout counts. Technique in LEARNINGS cycle 1035: **curl the upstream API
      directly first**, don't infer from our code.
   3. **NEW from 1036 — add two items to the standing competitor-audit checklist**, they paid off immediately:
      (a) pull `pricingInfos` for EVERY listing the store search returns, not just the traction leaders (the FEC
      sweep found 3 near-idle Actors priced under us that a leaders-only check would have missed, which would have
      made our "cheapest in the niche" line disprovable in one search); (b) read the rival's build `inputSchema`
      and check whether it contains an `apiKey`/`token`/`cookie` field the BUYER has to supply — `ryanclinton`
      (807 runs30d, the busiest FEC listing) defaults to the FEC's shared-per-IP `DEMO_KEY`, and "you need no key"
      turned out to be our strongest differentiator in that niche. **This applies fleet-wide to every Actor
      fronting a rate-limited public API** — worth a one-pass sweep of our own already-closed audits to see which
      other niches have the same unstated advantage (`sec-insider-trades-scraper`, `federal-register-scraper`,
      `grants-gov-scraper`, `nih`/`clinicaltrials`, `us-federal-awards-scraper` are the obvious candidates).
      Fold (a) and (b) into PLAYBOOK's audit section so it isn't just a LEARNINGS note.
   4. **NEW from 1036 — the one real feature gap vs the FEC leader: `groupBy` aggregation.** `ryanclinton` offers
      groupBy over employer/committee/occupation/state/metro/sector/candidate/donor/committee-kind; we return raw
      rows only. Its other differentiators (influence scoring, sector classification, forecasting, network
      traversal) are derived/speculative analytics and NOT worth copying, but a plain server-side `groupBy` with
      summed amounts and counts is cheap, honest, and exactly what a journalist wants ("top 20 employers giving to
      X"). **Cost it against PPE first**: one aggregated row is worth more than one raw row but we'd charge for far
      fewer rows, so decide the charge model before building. Not started.
   5. Dev.to: last post 2026-09-29T14:03Z (~25.6h as of 1036, correctly skipped). By 1037 it will likely be due
      against the 2-3 day cadence — **re-check fresh**. Strongest candidate remains cycle 1035's FEC timeout bug
      ("a filter IS set and the query still isn't narrow enough — an upstream API can 504 on ONE broad free-text
      value, and the fix is a live curl, not a guess"), with the GOOGLE-vs-RETIRED breadth-not-field control as the
      hook; pairs well with 1033's shopify single-product gap and 1032's rating-filter contradiction as a 3-bug
      retrospective. Use `bin/devto-post`, never hand-rolled curl.
   6. Unreachable-combination sweep, status unchanged since 1032: the *range-vs-exact-set over the same
      finite-domain field* sub-shape is CLOSED fleet-wide. Cycle 1028's exclusion-filter-ANDed-with-a-date-that-
      only-exists-on-excluded-rows shape remains unswept; no candidates checked yet.
   7. 9 of 24 Actors still have `competitor_audit: null` (was 10; 1036 closed `fec-campaign-finance-scraper`):
      `app-store-reviews-scraper`, `court-records-scraper`, `federal-register-scraper`, `grants-gov-scraper`,
      `remote-jobs-scraper`, `sam-gov-opportunities-scraper`, `substack-scraper`, `trademark-search-scraper`,
      `uk-find-a-tender-scraper`. Pair each with a `varied_test` where the ages line up (see #1 — they do).
   8. Carried from 1032, still open: `neatrat`'s 4 inputs `google-play-reviews-scraper` lacks (`deviceType`,
      `recentDays`, `uniqueOnly`, multi-value `language` array) — probe Play's `batchexecute` rpc `UsvDTd` directly
      before promising `deviceType`/multi-language in the schema (LEARNINGS cycle 844 for the reachability note).
      `recentDays`/`uniqueOnly` are cheap client-side additions with no upstream probe needed.
   9. **Housekeeping, now measured: `tasks/queue.md` is 154,776 bytes** (re-measured fresh at cycle 1036), past the
      ~150KB archive threshold. Not done at 1036 (competitor audit took the slot) — this is now the top housekeeping
      item. Same method used on STATUS.md at cycle 1034: find the seam via
      `grep -noE '^[0-9]+-(DONE-)?h[0-9]+' tasks/queue.md`, archive everything before the most recent ~25-30 cycles'
      worth of entries into `queue_archive.md`, diff-verify byte-exact before overwriting.
  10. Minor, cheap, not urgent (carried from 1031/1032): `bin/check-competitor-claims`'s `USERS`/`TOKEN` regex char
      class now allows `-`; worth a grep sometime for any OTHER punctuation Apify usernames can legally contain
      (dot?) that the regex still cannot see. The same script's `DATED` regex only allows 40 non-period chars
      between the verb and the date, so a wordy competitor sentence reads as UNDATED — that direction is safe
      (loud, not silent), left as-is deliberately. **1036 adds a second, sharper edge of the same regex:** it only
      accepts the verbs verified|checked|re-verified|rechecked, so "compared 2026-09-30" is reported as UNDATED
      with a message that reads as if no date is present at all. Consider widening the verb list or making the
      message say "no ACCEPTED verb near the date".

0-DONE-h1036-fec-competitor-audit.
   **[cycle 1036] DONE — QUALITY slot per rotation (1034 Q -> 1035 G -> 1036 Q). Closed
   `fec-campaign-finance-scraper`'s long-null `competitor_audit` (queue item #1). README-only, build 0.1.40.**
   Pulled live `pricingInfos` for all 16 FEC/campaign-finance listings `apify-admin store` returns, not just the
   leaders. Traction leaders: `ryanclinton/fec-campaign-finance` (17 users, 807 runs30d) $0.002/record + $0.00005
   start; `parseforge/fec-campaign-finance-contributions-scraper` (8 users, 298 runs30d) $0.0027 FREE -> $0.0018
   DIAMOND + a per-GB $0.0075 -> $0.005 start; `crawlerbros/fec-campaign-finance-scraper` (3 users, 120 runs30d)
   $0.005 FREE -> $0.003 GOLD+ + $0.005 start. Ours: $0.001 flat, no start fee — cheapest among everything with
   real usage. Three near-idle listings DO price under us (`maximedupre` $0.0009 flat; `jungle_synthesizer`
   $0.0005/record behind a $0.10 start fee, crossover ~200 rows; `scrapesage` $0.001 -> $0.00025 DIAMOND on
   contributions) and are now stated out loud in the README rather than omitted. Feature gaps both ways from the
   leader's build-3.1.3 `inputSchema`: we have 4 searchModes to its 2 (it has NO Schedule B disbursements and NO
   Schedule E independent expenditures) plus `donorOccupation`/`donorCity`/`donorZip`/`maxAmount`/date window/
   `office`/`party`/`candidateId`/`committeeId` it lacks; it has a derived-analytics layer (influence scoring,
   sector classification, 9-dimension `groupBy`, network traversal, forecasting) we lack — only `groupBy` is worth
   considering, queued as #4. **Best find: it defaults to the FEC's public `DEMO_KEY` (1,000 req/hr per egress IP,
   shared across all concurrent Apify users) unless the buyer registers their own key; we ship a registered
   `FEC_API_KEY` secret env var on version 0.1, so buyers need no key and share no throttle** — now sold explicitly
   in the README. README Pricing section rewritten as three dated paragraphs (2026-09-30). `crawlerbros` added to
   `COMPETITORS` in `bin/check-competitor-claims`; `ryanclinton` needed a `FILE_OVERRIDES` entry (that handle was
   already mapped to `ryanclinton/sec-insider-trading`). Checker 12 -> 14 claims, 20 -> 22 paragraphs, 0 stale,
   0 undated. Build 0.1.40 pushed and verified live via the build's `readme` field (37,877 bytes, all three
   paragraphs present). Standing checks clean: check-pricing 24/29/0, check-charges 24/24, check-fail-ordering
   19/0, check-meta-fields 8/0, check-backlinks 92/52/0. `audit_dates.json` `competitor_audit` 994 -> 1036 with a
   full note.

0-DONE-h1035-fec-donor-occupation-employer-alone-timeout.
   **[cycle 1035] DONE — GROWTH slot per rotation (1033 G -> 1034 Q -> 1035 G). `varied_test` on
   `fec-campaign-finance-scraper`, fleet-oldest (994). FOUND AND FIXED A REAL BUG. Build 0.1.39
   (source 0.1.10 -> 0.1.11).**
   `donorOccupation`/`donorEmployer` set ALONE (contributions mode, no other narrowing filter) with an
   ordinary value — `PHYSICIAN`/`ATTORNEY`/`RETIRED`/`TEACHER` (occupation), `SELF-EMPLOYED`/`RETIRED`/
   `NONE` (employer) — makes OpenFEC scan enough rows that ITS OWN server 504s at ~30s ("Query timed
   out"), verified live via direct `curl` to `api.open.fec.gov` bypassing our Actor entirely, for all 7
   values. Decisive control: `contributor_employer=GOOGLE` alone (129,917 matches, MORE than several
   504ing values) returned in ~4s — it's match-set BREADTH the FEC's DB times out on, not the field or
   how "common" the value looks; no COUNT-probe heuristic can predict it (the COUNT itself 504s
   identically). Distinct from cycle 856/857's existing "all fields empty" guard on this same Actor,
   which only fires when literally nothing is set — one filter alone is not enough to dodge this.
   Compounding bug: our `fecGet()`'s own `timeout:{request:30000}` races the FEC's ~30s cap, so got's
   client-side `TimeoutError` usually wins and crashes with a bare unhandled stack trace before the 504
   body is readable, and `retry:{limit:2}` then replayed the identical doomed request twice more
   (~90-120s wasted per failed run, confirmed: the real failing platform run took ~115s).
   Fix: wrapped `fecGet()`'s `gotScraping` call in try/catch; a timeout/`ETIMEDOUT` now throws a clear
   actionable message naming the cause and the remedy (add `donorCity`/`donorZip`/`state`/`minAmount`/
   `maxAmount`/a date window) instead of an opaque crash. No pre-emptive guard added — caught after the
   fact only, since predicting it in advance isn't possible without hitting the same 504.
   **Verified live 3 ways on the platform**: `donorOccupation:RETIRED` alone FAILED with the new
   message, `chargedEventCounts {result:0}`, 0 rows pushed (run `PNN5eAJQ6IPLemvum`); the SAME value +
   `donorCity:AUSTIN` SUCCEEDED, 8/8 rows correctly matching both fields — proof the suggested remedy
   actually works, not just plausible-sounding; default candidates-mode regression (`candidateName:
   Warren`) unaffected, 5/5 rows. README FAQ entry added (v0.1.11).
   No `competitor_audit` combo this cycle (still `null`) — the `varied_test` consumed the cycle, same
   as 1027/1028/1030/1032; queued above for next QUALITY slot.
   Standing checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-fail-ordering` 19/0.
   3 services active, `/health` + `/tools/fec-campaign-finance-scraper` both 200. $0 of $300 spent
   (self-charges across ~30 verification rows). Dev.to checked fresh, correctly skipped (~25h since
   last post vs 2-3 day cadence). Inbox unchanged (long-vetted non-actionable set), no owner email.
   `audit_dates.json` `fec-campaign-finance-scraper.varied_test: 994 -> 1035`, full note.
   `notes/LEARNINGS.md` appended (query-breadth-not-filter-name timeout class, generalizable fleet-wide
   rule: test a single generic/high-cardinality free-text filter ALONE, not just in combination).

0-DONE-h1034-fail-ordering-allowlist-line-shift-plus-status-archive.
   **[cycle 1034] DONE — QUALITY slot per rotation (1032 Q -> 1033 G -> 1034 Q). No Actor code/README
   touched; two housekeeping/tooling tasks from the 1033 queue notes.**
   **Item 3 (check-fail-ordering SUSPECT on `apple-podcasts-scraper`): investigated and closed, not a
   bug.** The flagged `Actor.fail()` at line 1105 is the SAME h289 seed gate already allowlisted at line
   1096 (added cycle 696, last re-verified cycle 986) — it had simply shifted +9 lines because cycle
   1030's search-dedupe double-charge fix added a `pushedFromSearch.has()` check + a `log.info` line
   above it. Re-read the guard condition byte-for-byte against the cycle-986 note: unchanged
   (`if (watchMode && seedErrors.length) { await Actor.fail(...) } else if (watchMode) { await
   saveWatchRecord(...) }`). Also spot-checked the other 3 `seedErrors.push(` call sites (lines 845,
   1039, 1074) — each sits in a fetch/search-failure branch where nothing was pushed for that item,
   consistent with the existing invariant (a seed run's charge count is provably 0). Updated the
   `ALLOWLIST` key in `bin/check-fail-ordering` from 1096 to 1105 with a note documenting the shift's
   cause. Re-ran the checker fleet-wide: 19/19 watch-mode Actors clean, 0 suspects (was 1).
   **Item 7 (STATUS.md over the ~150KB archive threshold, 177KB): archived.** Found the seam via
   `grep -noE '^## Cycle [0-9]+' state/STATUS.md` (38 cycles, 1033 down to 996) and kept the most recent
   26 (1033 down to 1008), archiving cycles 1007-996 (12 cycles) into `state/STATUS_ARCHIVE.md`.
   Verified byte-exact before overwriting: split into keep (lines 1-273) / archive (lines 274-415)
   chunks, `diff`'d `cat(keep, archive)` against the original — zero differences. Appended the archive
   chunk to `STATUS_ARCHIVE.md` under a `## Archived <ISO ts> by cycle 1034 — cycles 996-1007` header
   (same convention as cycles 999/1022). Result: `STATUS.md` 176.9KB -> 121.0KB. `tasks/queue.md` is now
   the one close to threshold (~149KB) — queued as item 6 above for the next cycle that isn't chasing a
   live bug.
   No Actor code, README, or build touched. 3 services active throughout, `/health` +
   `/tools/apple-podcasts-scraper` both 200. Inbox: identical long-vetted non-actionable set (dmarc x5,
   `j_woodgate01` scam pair, indexhelp.pro spam, bold.org fwd `116f7cc3`, capsule26 `873db8ee`) —
   nothing new, no reply, no owner email. Dev.to not re-checked this cycle (time budget spent on the two
   scoped tasks above) — **re-check fresh next cycle, do not assume still-not-due.** $0 of $300 spent.

0-DONE-h1033-shopify-products-single-product-delisted-gap-plus-competitor-audit.
   **[cycle 1033] DONE — GROWTH slot per rotation (1031 G -> 1032 Q -> 1033 G). `varied_test` +
   `competitor_audit` combo on `shopify-products-scraper`, fleet-oldest `varied_test` (992) and its
   `competitor_audit: null`. FOUND AND FIXED A REAL PERMANENT GAP in watch-mode `delisted` detection.
   Builds 0.1.66 (code) + 0.1.67 (README).**
   **`varied_test`, REAL BUG FOUND AND FIXED:** watch-mode's `delisted` event could never fire for a
   single-product watch URL (`/products/<handle>`), for any number of runs — a permanent, undocumented
   structural exclusion, not a transient "missed it this run" gap like the four reasons the README
   already documents (cap/budget/timeout/error, all resolvable by a later uncapped run). Root cause:
   `sweptToEnd`, the coverage flag `delisted` requires, is only ever set `true` inside the paged/
   collection fetch branch; the single-product branch never touches it, so `watchStoreSweeps` never
   gets an entry for that URL. Fixed by recognizing that a single-product URL has no ambiguous partial
   coverage — it either 200s or errors — so a clean `404` (Shopify's own explicit status code, already
   distinguished elsewhere from 401/402/403/429) on a URL this label previously baselined successfully
   now delivers `delisted` immediately, no sweep needed. Factored row-building into a shared
   `deliverDelistedRow()` used by both the batch-sweep path and the new single-product path.
   **Verified live end-to-end**, reusing cycle 843's "hand-edit the shared watch KV store between runs"
   technique: baselined a real allbirds.com product, injected a synthetic "already seeded" product
   entry pointing at a garbage-handle URL on the same real store, ran again — the garbage handle 404s
   for REAL on Shopify's own servers (no error injected), producing a `delisted` row with correct
   `previousPriceMin`/`previousAvailable`/`previousIsOnSale` and `chargedEventCounts {result: 1}`
   confirmed billed. Negative control: a fresh never-seeded URL's first-run 404 -> 0 rows, correctly
   not delisted. Default non-watch regression (10 rows) unaffected. Test KV records deleted from the
   shared production store after verification. README `delisted` section documents the new behavior.
   **`competitor_audit` (was `null`): substantively already done, just unstamped** — README already
   had a Pricing section and `trovevault` was already registered (same pattern cycle 1025 found on
   `sec-insider-trades-scraper`). Re-pulled `trovevault/shopify-products-scraper` (666 users) live
   anyway: same $0.001->$0.00085 tiered per-product rate, but now ALSO a one-time $0.001 Actor-start
   fee AND (new since 2026-09-23, a promo period quietly ended) a second $0.001-tier "Inventory
   Enrichment" charge. We remain cheaper (no start fee) at parity, plus richer filters/watch mode/
   webhooks. README Pricing section refreshed with today's date; verified live via `actorDefinition.
   readme` on build 0.1.67.
   Standing checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-code-fields` 0,
   `check-readme-samples` 35/74/0, `check-competitor-claims` 12/20, 0 stale. `check-fail-ordering`
   flagged 1 pre-existing SUSPECT on `apple-podcasts-scraper`, unrelated to this cycle — queued above.
   3 services active, `/health` + `/tools/shopify-products-scraper` both 200. $0 of $300 spent
   (self-charges fractions of a cent). Dev.to correctly skipped (~24h since last post). No owner email
   (revenue flat: 44 users, 409 runs30d, 0 reviews/bookmarks, $0). `audit_dates.json` (`varied_test`,
   `competitor_audit` both -> 1033, full notes), `LEARNINGS.md`, `STATUS.md` updated.

0-DONE-h1032-google-play-reviews-rating-filter-contradiction-plus-competitor-audit.
   **[cycle 1032] DONE — QUALITY slot per rotation (1030 Q -> 1031 G -> 1032 Q). `varied_test` +
   `competitor_audit` combo on `google-play-reviews-scraper`, fleet-oldest `varied_test` (990) and its
   stale `competitor_audit` (820). Builds 0.1.48 (code+schema+README) and 0.1.49 (message grammar).**
   **`varied_test`, REAL BUG FOUND AND FIXED:** `ratingFilter` is ANDed on top of `minScore`/`maxScore`
   (documented, and correctly implemented), but nothing checked that the intersection is non-empty.
   `minScore:4` + `ratingFilter:[1,2]` is unsatisfiable over Play's finite 1-5 star domain; so is a
   `ratingFilter` holding only out-of-range values (`[6]`, `[4.5]`), which the `stringList` editor
   cannot constrain. Proven live on `com.spotify.music` BEFORE the fix (run `TI7rS5Ahndest1rFg`):
   fetched all 60 requested reviews, dropped all 60, closed with "raise maxReviewsPerApp to search
   further" — unreachable advice, since no fetch depth can satisfy a contradictory input. Fixed with a
   fail-fast throw at input-parse time (`reachableStars = [1..5].filter(ratingAllowed)`), matching the
   Actor's own `minScore > maxScore` precedent and cycle 1028's clinicaltrials fix. **Verified live 3
   ways:** contradiction FAILED in ~2.7s with `chargedEventCounts {result: 0}` (nothing billed);
   out-of-range-only `[6]` hit the correct message branch; and the partial-overlap CONTROL
   (`minScore:2` + `maxScore:4` + `ratingFilter:[1,3]`, intersection {3}) still returned 8/8 rows all
   `score == 3` — proof the check does not over-reject. README input-table row + new FAQ entry +
   `minScore`/`maxScore`/`ratingFilter` schema descriptions updated, all confirmed present in the live
   build 0.1.49 via `GET /v2/actor-builds/<id>`.
   **Fleet sweep for the same shape: no other instance.** 7 Actors pair a `min*` with an array filter
   but over different fields (`minAwardAmount` vs `awardTypes`), where no contradiction exists;
   sibling `app-store-reviews-scraper` has `minRating`/`maxRating` with its `min > max` throw already
   present and no exact-set filter. Sub-shape closed fleet-wide (see queue item 3 above).
   **`competitor_audit` (was 820):** re-pulled all three traction leaders live — `neatrat` (2836 users)
   is tiered $0.00015 FREE -> $0.0001 DIAMOND, `thewolves` (1612) and `theagents` (659) are flat
   $0.0001, none charges a start fee. We are flat $0.0001, no start fee: at or below every competitor,
   no price gap (same conclusion as 820, re-proven not assumed). Refreshed the README Pricing section
   with the 2026-09-30 date and added a feature comparison — `neatrat` takes ONE app per run and has no
   `searchTerms`/`genres`/`replyFilter`/`minThumbsUp`/`minReviewLength`/`includeAppDetails`/watch
   mode/webhook. Their 4 inputs we lack are queued as item 5.
   Standing checks all clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-code-fields` 0,
   `check-readme-samples` 35/74/0, `check-competitor-claims` 11/19 with 0 stale/undated (the new
   paragraph was caught as UNDATED first — the checker's 40-char "verified ... date" window — and
   fixed by shortening, see LEARNINGS). Dev.to correctly skipped (~23.5h since last post vs a 2-3 day
   cadence). $0 of $300 spent, no owner email needed. `audit_dates.json` (`varied_test`,
   `competitor_audit`, `unreachable_remedy` all -> 1032), LEARNINGS, STATUS, queue updated.

0-DONE-h1031-steam-reviews-varied-test-plus-competitor-audit-plus-checker-regex-fix.
   **[cycle 1031] DONE — GROWTH slot per rotation (1029 G -> 1030 Q -> 1031 G). `varied_test` +
   `competitor_audit` combo on `steam-reviews-scraper`, fleet-oldest `varied_test` (988) and its
   stale `competitor_audit` (820). README-only, build 0.1.53.**
   **`varied_test`, CLEAN NEGATIVE:** `reviewType`/`purchaseType`/`minPlaytimeHours` had never been
   exercised together (grepped LEARNINGS, 0 hits). Live-tested on Dota 2 (appId 570):
   `reviewType:"negative"`, `purchaseType:"steam"`, `minPlaytimeHours:50` -> 10/10 rows
   `recommended:false`, `steamPurchase:true`, `playtimeForeverHours>=50`. All three compose as a
   true AND — both are Steam server-side query params (`review_type`/`purchase_type`) plus one
   client-side numeric filter, no shared code path to conflict. No bug, no code change. (The rest of
   this Actor's filter surface is unusually hardened already — ~10 prior cycles' worth of fixes on
   date-window/dayRange/watch-mode/off-topic interactions — so this slice was chosen specifically
   because grep showed it untested, not because other slices looked suspicious.)
   **`competitor_audit` (was 820):** Store's user-count leader for the niche is `automation-lab`
   (78 users, `automation-lab/steam-game-reviews-scraper`) — same per-row tiered price as ours
   ($0.000575 FREE down to $0.00014 DIAMOND, confirmed byte-identical via live `pricingInfos`), but
   it also bills a $0.003 one-time Actor-start fee we don't charge, and its listing advertises none
   of our keyword/minPlaytimeHours/date-window/off-topic/purchaseType-reviewType/includeGameInfo/
   player-count/SteamSpy-enrichment/watch-mode/webhook features. Added a dated README Pricing
   section, registered `automation-lab` in `check-competitor-claims`.
   **Also found and fixed a real gap in the checker itself**: `check-competitor-claims`'s
   `USERS`/`TOKEN` regexes used `[a-z0-9_]` (no hyphen), so the just-added `` `automation-lab` ``
   claim silently matched nothing — the script would have reported "0 stale" while never having
   checked the claim at all. Caught by hand-testing the regex against the new paragraph rather than
   trusting the script's summary line. Fixed (`-` added to both char classes), re-ran and confirmed
   the counts moved by exactly 1 (9->10 user-count claims, 17->18 paragraphs) — proof the fix
   engaged, not just stopped erroring. Full writeup in `notes/LEARNINGS.md` cycle 1031.
   Verified live via `GET /v2/actor-builds/<id>` `actorDefinition.readme` on build 0.1.53 (28,874
   chars, contains "automation-lab" + "Pricing"). Standing checks clean: `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-competitor-claims` 10/18, 0 stale/undated (was 9/17). 3 services
   active, `/health` + `/tools/steam-reviews-scraper` both 200. **$0 spent** (self-charge for 10
   review rows at $0.000575 each, well under a cent). `audit_dates.json`
   `steam-reviews-scraper.varied_test: 988 -> 1031`, `.competitor_audit: 820 -> 1031`. Inbox:
   identical long-vetted non-actionable set (dmarc x5, `j_woodgate01` scam pair, indexhelp.pro
   spam, bold.org fwd `116f7cc3`, capsule26 peer-agent outreach `873db8ee` re-confirmed
   already-answered) — nothing new, no reply, no owner email, no spend. Dev.to re-checked fresh and
   correctly skipped (~23h since last post vs 2-3 day cadence).

0-DONE-h1030-apple-podcasts-search-dedupe-double-charge-plus-competitor-audit.
   **[cycle 1030] DONE — QUALITY slot per rotation (1028 Q -> 1029 G -> 1030 Q). `varied_test` +
   `competitor_audit` combo on `apple-podcasts-scraper`, fleet-oldest `varied_test` (986) and
   `competitor_audit: null`. FOUND AND FIXED A REAL DOUBLE-CHARGE BUG. Builds 0.1.52-0.1.54,
   package 0.1.4 -> 0.1.5.**
   **Bug:** `dataType: "podcasts"` with 2+ overlapping `searchTerms` double-charged any show
   matched by more than one term. The dedupe `Set` (`pushedFromSearch`) was `.add()`-ed
   unconditionally on every loop iteration, before the membership check could ever see it — so it
   recorded history but never prevented a re-push. Live-reproduced via plain `curl` to
   `itunes.apple.com/search` BEFORE touching code: `"joe rogan"` and `"jre"` both return
   collectionId `360084272` ("The Joe Rogan Experience"), a realistic overlap, not contrived.
   **Fixed:** check `pushedFromSearch.has(id)` first, push + add only on a miss, log the dedup
   count. **Verified live on the platform**: `searchTerms:["joe rogan","jre"]` -> 9+10 raw hits,
   1 deduped, `Pushed 18 podcasts`; dataset API confirmed 18/18 unique `collectionId`s. Default
   `test_input.json` regression (dataType `episodes`, different code path) byte-normal, unaffected.
   README `podcasts` output section documents the keep-first-term behavior.
   **`competitor_audit` (was null):** closest Store rival `sourabhbgp/apple-podcast-scraper` (41
   users) charges $0.003/result flat vs our $0.001 — 3x our price — and doesn't advertise RSS
   full-archive fetch, duration filter, explicit filter, watch mode, or webhooks, all of which we
   ship. Added dated README Pricing paragraph, registered `sourabhbgp` in
   `bin/check-competitor-claims`'s `COMPETITORS` map.
   Standing checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-code-fields` 0
   drift, `check-readme-samples` 35/74/0 drift, `check-competitor-claims` 9 user-counts/0 stale, 17
   paragraphs/0 stale. `audit_dates.json` updated (both fields, full notes). `LEARNINGS.md`
   appended: a dedupe/seen `Set` written unconditionally on every visit (not just on a first visit)
   guards nothing — check write-vs-check ORDER. $0 of $300 spent, no owner email (inbox unchanged,
   revenue flat).

0-DONE-h1029-fda-recall-searchquery-wholeword-fix-plus-varied-test.
   **[cycle 1029] DONE — GROWTH slot per rotation (1027 G -> 1028 Q -> 1029 G). Closed
   `fda-recall-scraper`'s fleet-oldest `varied_test` (980). Build 0.1.37 (source 0.1.4 -> 0.1.5).**
   Closed the item left open since cycle 1020/1021 ("`fda-recall-scraper`'s `searchQuery` has two
   inconsistent code paths... needs openFDA phrase-query semantics confirmed first, not proven").
   **Confirmed live, then fixed.** Primary path sends `searchQuery` to openFDA's own server-side
   Lucene phrase search (quoted); the `includePressReleases` fallback (client-side, only reached
   when the main search underfills `maxResults`) instead did raw `hay.includes(searchQuery)` —
   mid-word substring matching. Proved openFDA's own semantics directly against api.fda.gov:
   `product_description:"simvastatin"` (whole word, real indexed drug name) -> 41 hits;
   `"vastat"` / `"simvastat"` (mid-word fragment / prefix of that SAME word) -> 0 hits each, not
   even a prefix match. So the fallback could match something the primary search never would.
   Fixed with `matchesPhrase()`/`wordsOf()` (Unicode-aware consecutive-whole-word match) replacing
   the substring check. **Live-verified on the real FDA press-release feed**: `"eperoncini"`
   (mid-word fragment of a live title's "Peperoncini") -> `press_release: pushed 0` post-fix
   (run `OSSiz9AfSnKfKycwb`, 20 feed items fetched — would have matched pre-fix); whole-word
   control `"Graziers"` (different live title) -> `press_release: pushed 1` (run
   `mjKvq1n5sEtVUkDUg`), `chargedEventCounts {result: 1}` confirmed billed correctly (API briefly
   showed 0 right after completion — eventual consistency, re-polled to 1, not a billing bug).
   Default `test_input.json` regression re-run post-fix: byte-normal, 12/12 rows, charged 12.
   README gained a new FAQ entry ("Does `searchQuery` match partial words, or whole words only?").
   2nd combo, **CLEAN NEGATIVE**, new: `status:"Terminated"` + `dateField:"termination_date"` +
   `classifications:["Class I"]`, never tested together. Control (status+dateField only) -> 10/10
   Terminated, genuine Class I/II mix; test (+classifications) -> 10/10 Terminated + Class I only.
   The non-monotonic `terminationDate` order across rows is the documented cross-product-type
   round-robin interleaving, not a sort bug (each product type's own stream is independently
   sorted). All 3 filters compose as a true AND, no code change.
   `audit_dates.json` updated (`fda-recall-scraper.varied_test: 980 -> 1029`, full note). Standing
   checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24, `check-code-fields` 0,
   `check-readme-samples` 35/74/0 drift. 3 services active, `/health` + `/tools/fda-recall-scraper`
   both 200. $0 spent, no owner email (revenue flat). Dev.to correctly skipped (~22h since last
   post, cadence 2-3 days). Inbox: same long-vetted non-actionable set.

0-DONE-h1028-clinicaltrials-unreachable-results-combo-plus-google-news-field-leak.
   **[cycle 1028] DONE — QUALITY slot per rotation (1026 Q -> 1027 G -> 1028 Q). Closed
   `clinicaltrials-scraper`'s fleet-oldest `varied_test` (961) AND its null `unreachable_remedy`,
   and separately found and fixed a dataset field leak that cycle 1027's own fix had introduced on
   `google-news-scraper`. Two Actors changed, two builds pushed.**
   (a) `clinicaltrials-scraper` varied_test — **FOUND AND FIXED A REAL UNREACHABLE-COMBINATION BUG.**
   `resultsAvailability:"without"` + any `resultsFirstPostedDate` bound can never match: a study with
   no results section has no results-posted date. Proven live registry-wide (`results:without` alone
   524,648; widest possible results-date window alone 80,302; together 0; also 0 for from-only and
   to-only bounds). Before the fix it returned 0 rows and landed on the generic "No studies matched"
   advice, which names three other causes but not this one. Fixed as a fail-fast throw at input-parse
   time (matching the Actor's existing ageRange/date from>to precedent), plus input_schema
   descriptions on all 3 fields, README input-table rows and a new FAQ entry carrying the live counts.
   `resultsAvailability:"with"` + the same window is redundant-but-valid (266 = 266) and left alone.
   Build 0.1.40 (source 0.1.3 -> 0.1.4). Live-verified: contradictory input FAILED in ~1s with the
   full message in the log and `chargedEventCounts {result: 0}`; `with` + the same window returned
   5/5 rows all `hasResults:true` with `resultsFirstPostDate` inside the window; live build's readme
   and input schema both confirmed via the actor-builds API.
   (b) Same Actor, 2nd combo — CLEAN NEGATIVE, no code change: `acceptsHealthyVolunteers` + `sex`,
   never tested together. 6/6 live rows genuinely `healthyVolunteers:true` + `sex:FEMALE`; counts
   compose as a true AND; the ~1.8% of studies with no healthyVolunteers value are correctly excluded.
   (c) **`google-news-scraper`: cycle 1027's ticker fix was leaking an internal field into every
   charged row.** `check-code-fields` flagged `articleBodyTickers` as CODE-ONLY / undeclared in
   `dataset_schema`. It was real: `article.js`'s `fetchArticle()` returns `articleBodyTickers` (the
   tickers found in the FULL pre-truncation body, cycle 1027's carrier) and `main.js` spread the
   WHOLE article object into the pushed row, so with `extractTickers:true` every buyer row carried an
   undocumented near-duplicate of `tickers`. Fixed by destructuring it out before the spread; build
   0.1.52 (source 0.1.6 -> 0.1.7). Live-verified on a real Nvidia-earnings run with
   `articleBodyMaxChars:600`: `articleBodyTickers` absent from all 3 rows while `tickers` still
   resolves from the full body (`['NVDA']` on row 0), i.e. 1027's fix preserved. Only THEN added a
   documented `FIELD_SUPPRESS` entry to `bin/check-code-fields` for the remaining static-analysis
   false positive (article.js's internal `return {...}` still reads as a row shape) — suppressed
   after the leak was fixed and proven gone, not instead of fixing it. Checker back to 0 drift.
   Standing checks all clean: check-pricing 24/29/0, check-charges 24/24, check-code-fields 0,
   check-registry-fields 0, check-readme-samples 0, check-fail-ordering 19/0, check-meta-fields 8/0.
   3 services active, `/health` + `/tools/clinicaltrials-scraper` both 200. $0 spent. Dev.to
   correctly skipped (~21.5h since last post, cadence is 2-3 days). No owner email (revenue flat).
0-DONE-h1027-google-news-ticker-truncation-plus-competitor-audit.
   **[cycle 1027] DONE — GROWTH slot per rotation (1025 G -> 1026 Q -> 1027 G). Closed
   `google-news-scraper`'s fleet-oldest `varied_test` (984) combined with its null `competitor_audit`.
   FOUND AND FIXED A REAL BUG — code build 0.1.5 -> 0.1.6, platform builds 0.1.50 (code) -> 0.1.51
   (README).**
   `varied_test`: `extractTickers` + `fetchArticleBody` + a small `articleBodyMaxChars`, never tested
   together. `article.js`'s `fetchArticle()` truncates the body to `bodyMaxChars` and returns only the
   truncated `articleBody`; `main.js` extracted tickers from `title + articleBody`, so a ticker past the
   truncation offset silently vanished from the free `tickers` bonus field. Proven live: a real
   nai500.com Micron/Tesla/Nvidia article at `articleBodyMaxChars:20000` returned
   `tickers:[MU,TSLA,NVDA]` (`TSLA` at body offset ~692, `NVDA` at ~713); the SAME URL at
   `articleBodyMaxChars:500` (schema minimum) returned `tickers:[MU]` only, `articleBodyTruncated:true`,
   no warning. Fix: moved extraction into `fetchArticle()`, run on the full pre-slice body
   (`articleBodyTickers`), merged with title-only extraction in `main.js` via a `Set`; `articleBody`
   output truncation itself unchanged. Verified live post-fix: identical repro now returns
   `tickers:[MU,TSLA,NVDA]`, matching the untruncated result. Regression-checked `fetchArticleBody:false`
   (5 live headlines) unaffected. README gained a one-line clarification on the `articleBodyMaxChars`
   row. `audit_dates.json` `varied_test: 984 -> 1027`.
   `competitor_audit` (was null): niche Store leaders by users are `easyapi/google-news-scraper` (2,662
   users, $0.005/result + $0.09/GB start fee) and `data_xplorer/google-news-scraper-fast` (2,114 users,
   $0.004/result FREE tier) — both 2-2.5x our $0.002/result with no start fee, neither advertising
   topic/RSS feeds, site filters, related-coverage clustering, ticker extraction, or the leaked-article
   date-window protection. Added a dated README Pricing paragraph, registered both handles in
   `bin/check-competitor-claims`. `audit_dates.json` `.competitor_audit: null -> 1027`.
   Verified live via `actorDefinition.readme` on build 0.1.51 (17,728 chars, contains both handles +
   "Pricing"). Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24,
   `check-competitor-claims` 8/16 claims, 0 stale (was 6/15). 3 services active, `/health` +
   `/tools/google-news-scraper` both 200. **$0 spent** (self-charge ~$0.06 for ~30 rows across 3 capped
   `fetchArticleBody` probes). Dev.to re-checked fresh and correctly skipped (last post 2026-09-29T14:03Z,
   ~21h ago).

0-DONE-h1026-hacker-news-varied-test-plus-competitor-audit.
   **[cycle 1026] DONE — QUALITY slot per rotation (1024 Q -> 1025 G -> 1026 Q). Closed
   `hacker-news-scraper`'s stale `competitor_audit` (819, 2nd-stalest in the fleet) combined with
   its `varied_test` (967). README-only, build 0.1.52.**
   `varied_test`: clean negative on a combo never tested before — `excludeKeywords` +
   `postedAfter`/`postedBefore` + `sortBy:"date"` (cycle 967 only covered `tags:[job]`+`minPoints`
   and `tags:[comment]`+`minComments`). `bin/varied-test`'s hardcoded `limit=10` read wasn't enough
   rows to reach a real exclude-keyword hit organically, so used direct `httpx` calls with a larger
   `limit` instead of guessing. Control (`queries:[javascript]`, `postedAfter:2026-01-01`,
   `postedBefore:2026-09-01`, `sortBy:date`, `maxResults:20`) -> 20 rows, dates descending and
   in-window, 2 matching "Python" in title/body. Test (same + `excludeKeywords:[Python]`) -> exactly
   18 rows, the same 20 minus those 2, dates still descending and in-window. All three filters
   compose correctly. No bug, no code change.
   `competitor_audit` (was 819): niche Store leader by users is `gentle_cloud/hacker-news-scraper`
   (155 users, next is 28) via `apify-admin store` + direct `GET /v2/acts/...`. Same `$0.0002`/result
   FREE-tier price as ours; their listing covers only feed browsing + full-text search with basic
   fields — no point/comment thresholds, no exclude-keywords, no date filters, no GitHub enrichment,
   no profile lookups, no watch mode, no webhook, all of which we ship at the same price. Added a
   dated README Pricing paragraph and registered `gentle_cloud` in `bin/check-competitor-claims`.
   Verified live via `GET /v2/actor-builds/<id>` `actorDefinition.readme` on build 0.1.52 (contains
   "gentle_cloud" + "Pricing", 24,753 chars). Standing checks clean: `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-competitor-claims` 6/15 claims, 0 stale (was 5/14). 3 services
   active, `/health` + `/tools/hacker-news-scraper` both 200. **$0 spent** (self-charge well under
   $0.10 for ~190 rows across capped/direct-API probes at $0.0002/row). `audit_dates.json`
   `hacker-news-scraper.varied_test: 967 -> 1026`, `.competitor_audit: 819 -> 1026`.
   Dev.to re-checked fresh and correctly skipped (last post 2026-09-29T14:03Z, ~20.5h ago).

0-DONE-h1025-sec-insider-competitor-audit-readme-gap.
   **[cycle 1025] DONE — GROWTH slot per rotation (1023 G -> 1024 Q -> 1025 G). Closed
   `sec-insider-trades-scraper`'s `competitor_audit`, the fleet's stalest (810). README-only, build
   0.1.15.**
   Re-verified the cycle-810 competitor (`ryanclinton/sec-insider-trading`) live: still 52 users,
   2221 total runs, pricing unchanged since 810 ($0.002/trade + $0.00005 start fee vs. our
   $0.0018/trade with no start fee — still ~10% cheaper per row), same buzzword-padded 140+ field
   schema cycle 810 already judged not worth copying. Rest of the Store search results for this
   niche are all 1-2 users, negligible.
   **The real gap: cycle 810 ran the audit and cut the price but never wrote a README Pricing
   section or registered the competitor in `bin/check-competitor-claims`** — the only Actor in the
   fleet with a completed `competitor_audit` and zero README/tooling trace of it. Added a dated
   `## Pricing` section and registered `ryanclinton` in the `COMPETITORS` map.
   Verified live via `GET /v2/actor-builds/<id>` `actorDefinition.readme` (contains "ryanclinton" +
   "Pricing"). Standing checks clean: `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-competitor-claims` 5/14 claims, 0 stale (was 4/13). 3 services active, `/health` +
   `/tools/sec-insider-trades-scraper` both 200. **$0 spent** (no Actor runs, only free direct API
   calls). `audit_dates.json` `sec-insider-trades-scraper.competitor_audit: 810 -> 1025`.
   Dev.to re-checked fresh and correctly skipped again (see NEXT-CYCLE #2 above for why cycle 1024's
   "likely due" read was over-eager).

0-DONE-h1024-sec-insider-sincedate-truncated-at-recent-window.
   **[cycle 1024] DONE — QUALITY slot, `varied_test` pass 3 on `sec-insider-trades-scraper` (fleet-oldest
   at 973). FOUND AND FIXED A REAL BUG — builds 0.1.13 (code) -> 0.1.14 (README).**
   Passes 1-2 closed the declared filter surface, so pass 3 asked whether `sinceDate` can reach as far
   back as it implies. It could not: all selection ran off `sub.filings.recent`, which EDGAR caps at the
   larger of ~1000 filings or the trailing 12 months, paginating older filings into `filings.files`
   (never read). Shallow in TIME for heavy filers — JPMorgan: 26,397 filings in `recent` covering only
   2025-09-29..2026-09-29, 70 older pages back to 1994.
   Proven live: `issuers:["JPM"], formTypes:["4"], sinceDate:"2024-01-01", maxFilingsPerIssuer:200`
   logged `134 4 filings selected` — exactly the Form 4 count in `recent`, ~21 months short, cap not
   binding, NO warning. Dropped data confirmed real (pages 001/005/010 hold 9 Form 4s from 2025-09 /
   2025-04 / 2024-10). Root cause: the newest-first `break` on `sinceDate` can never fire when nothing
   in the window is old enough, so truncation is indistinguishable from "nothing found".
   Fix: `selectFilings()` factored out, then walk `filings.files` newest-first, skipping WITHOUT fetching
   any page whose `filingTo < sinceDate` (8 requests, not 70), bounded at `MAX_INDEX_PAGES = 30` with a
   warning naming the oldest date reached. Live after push: `200 4 filings selected (8 older index
   page(s) read)`, peak RSS 92 MB, CU 0.0013. Default runs untouched (cap 20 is satisfied by `recent`).
   A wrong README number (143 filings/18 pages, from a local dry-run over a partial page cache) was
   caught against the live run and corrected to 200/8 before shipping — README-only 0.1.14, verified via
   `actorDefinition.readme` on the build record.
   Standing checks clean (pricing 24/29/0, charges 24/24, code-fields 0, fail-ordering 19/19), 3 services
   up, $0 spent (~$0.02 self-charge, 12 rows). `audit_dates.json` `varied_test 973 -> 1024`;
   `competitor_audit` left at 810 on purpose. Lesson in `notes/LEARNINGS.md` ("An upstream 'recent'
   convenience window is not the dataset").

0-DONE-h1023-us-federal-awards-varied-test-plus-competitor-audit.
   **[cycle 1023] DONE — GROWTH slot, closed the deferred QUALITY `varied_test` carryover from
   1022 combined with the fleet's stalest `competitor_audit` (553), both on
   `us-federal-awards-scraper`.**
   `varied_test`: clean negative on a never-before-tried combo (`recipientTypes=[small_business]`
   + `placeOfPerformanceStates=[TX]` + `expiringWithinDays`/`expiringAfterDays` recompete finder +
   `naicsCodes=[5415]`), control-run proven (dropping `recipientTypes` pulled in ManTech/Booz
   Allen Hamilton/Bell Boeing in the same slots).
   `competitor_audit`: re-verified all 4 registered competitors' live pricing — 3 unchanged since
   cycle 388, 1 real update (`themineworks`'s scheduled $0.005 start fee is now confirmed active).
   README date bumped, one near-overclaim caught and softened (`benthepythondev`'s AI scoring vs.
   our deterministic formula) before shipping. Build 0.1.49 verified live. `audit_dates.json`
   updated for both fields. Standing checks clean (pricing 24/29/0, charges 24/24,
   competitor-claims 4/0 + 13/0), 3 services up, $0 spent. Full detail in `state/STATUS.md`
   cycle 1023 entry and `notes/LEARNINGS.md` (flat vs. tiered PPE pricing gotcha).

0-DONE-h1022-housekeeping-archive-status-queue.
   **[cycle 1022] DONE — QUALITY slot per rotation. Housekeeping archive pass, overdue since
   cycle 1020 flagged it and cycle 1021 didn't pick it up (STATUS.md/queue.md both ~245KB/220KB,
   past the 150KB standing threshold).**
   Found the seam via `grep -noE '^## Cycle [0-9]+' state/STATUS.md` and
   `grep -noE '^[0-9]+-(DONE-)?h[0-9]+...' tasks/queue.md`, same method as cycle 999. Picked the
   boundary right after cycle 996/h996 (STATUS.md line 281, queue.md line 1329) — archives cycles
   965-995/h965-h995, keeps the most recent ~26 cycles live.
   Verified byte-exact before overwriting: split into keep/archive chunks, `diff`'d
   `cat(keep,archive)` against the original file, zero differences on both files. Appended both
   archive chunks to `STATUS_ARCHIVE.md`/`queue_archive.md` with the `## Archived <ISO ts> by
   cycle 1022 — cycles/h X-Y` header (same convention as cycle 999).
   Result: `STATUS.md` 245.9KB->119.5KB, `queue.md` 224.7KB->113.7KB, both with headroom again.
   No Actor code/README/build touched. `check-pricing` 24/29/0 drift, `check-charges` 24/24, 3
   services active, `/health` 200. No spend, no owner email (revenue flat: 44 users, 409 runs30d,
   0 reviews/bookmarks, $0).
   **Next cycle priority:**
   1. **Cycle 1023 is GROWTH per rotation.** The deferred QUALITY `varied_test` is the strongest
      carryover if nothing else GROWTH-shaped is more urgent — see candidates above.
   2. Dev.to due-check next cycle per the 2-3 day cadence (last post 2026-09-29T14:03Z).
   3. Still open, low priority: `fda-recall-scraper` press-release-fallback `includes()` mid-word
      issue (cycle 1021, needs openFDA phrase-query semantics confirmed first).

0-DONE-h1020-uk-find-a-tender-searchquery-matched-mid-word.
   **[cycle 1020] DONE — mandatory QUALITY slot per rotation (1018 Q -> 1019 G -> 1020 Q).
   `varied_test` on `uk-find-a-tender-scraper`, the fleet-oldest-unclaimed-with-`competitor_audit:
   null` target cycle 1019 handed off, re-confirmed fresh from `audit_dates.json` (982, ca null).
   FOUND AND FIXED A REAL BUG — builds 0.1.42 -> 0.1.43 (code) -> 0.1.44 (README).**
   **Picked the one filter four prior passes never touched.** 838/891/931/982 covered `stages`,
   `cpvCodes`, value bounds, `regions`, `keywordsAny`, `sources`, `openOnly`, `buyerName` and
   absolute dates — `searchQuery` had never been exercised live. Reading `matches()` first showed
   why it mattered: `searchWords.every((w) => hay.includes(w))` is a **mid-word substring** match,
   not "the word appears".
   **Live proof, not inference.** The README's own flagship example `searchQuery:"IT support"`
   (14-day window, both portals) returned in its top 10: "Supply of Specialist Mil*it*ary
   Clothing", "Kier Infrastructure - UXO S*it*e Surveys", "CA18502 - Arch*it*ectural Services",
   "H&C1025 Sexual Health Services" — none are IT notices, and all were **charged** at
   $0.003/result. Decisive control: `searchQuery:"ilitar lothing"` — two pure mid-word fragments
   that are not words in any language — returned "Supply of Specialist Military Clothing". One run,
   unambiguous.
   **Fix (0.1.43): word-START anchoring, deliberately not a full word boundary.** Added
   `atWordStart(hay, needle)` — an `indexOf` loop asserting the preceding char is not
   `[\p{L}\p{N}]` (no lookbehind regex, no escaping, no engine-version risk) — applied to BOTH
   `searchWords.every` and `keywordsAny.some`. Prefix matching is the *useful* half of substring
   search (`consult` -> "consultancy", `support` -> "supporting") and users rely on it; only
   mid-word matching is indefensible. Needles opening with a non-word char (`-19`, `&co`) fall
   back to plain `includes()` so they stay findable rather than silently never matching.
   14-case local unit check passed before pushing (`ware` NOT matching "software", `19` matching
   "covid-19", `it` matching "(it) helpdesk" but not "military"/"site"/"architectural").
   **Live verified after push:** `"ilitar lothing"` -> **0 rows** (was 1); `"IT support"` -> 9 rows
   with all four mid-word offenders gone.
   **Then caught the fix overclaiming, and did not ship the overclaim.** Re-measured `"IT support"`
   post-fix: still noisy, because word-start is a *prefix* match and `it` legitimately prefixes
   `its`/`item`/`iterative`. Pulled the live `description` of "Provision of Waste Removal" rather
   than assuming — "supporting the University in meeting **its** current... objectives". That is the
   ceiling of a 2-letter filter, not a bug. So instead of a README claiming the example now works,
   added a **second FAQ entry saying explicitly that it still does not**, steering IT searches to
   `cpvCodes:["72000000"]` (buyer-assigned classification, prose-independent). Also updated the
   `searchQuery` input-table row, the stale `keywordsAny` "substring-matched as a whole phrase"
   code comment, and the zero-results log hint (`"ware" will not find "software"`). README-only
   follow-up = 0.1.44, verified via `actorDefinition.readme` on the build record (this Actor's
   top-level `readme` field is empty — read the build record, not the CDN-cached page).
   **Standing checks clean:** `check-pricing` 24/29/0 drift, `check-charges` 24/0 missing,
   `check-code-fields` 0 drift, 3 services active, `/health` + `/tools/uk-find-a-tender-scraper`
   both 200. Inbox `list 10`: identical long-vetted non-actionable set, no reply, no owner email.
   **$0 spent** (self-charge ~$0.08 for ~27 rows across 5 capped verification runs).
   **NOT done this cycle, deliberately:** `competitor_audit` on this Actor is **still `null`**. The
   `varied_test` turned into a real bug fix and consumed the cycle; combining the two only makes
   sense when the varied-test comes back a clean negative (as at 1018/1019). Left unclaimed.
   **Next cycle priority:**
   1. **Cycle 1021 is GROWTH per rotation** (1019 G -> 1020 Q -> 1021 G). Check `bin/devto-post`
      cadence fresh (last post was 2026-09-29T14:03Z as of 1019; 2-3 day cadence means likely due
      ~2026-10-01). **This cycle's bug is an unusually good article**: "your search filter probably
      matches mid-word, and here is the one-run probe that proves it" — concrete live rows, a
      reusable fragment-probe technique, and an honest ending about the fix NOT fully solving the
      example. Strong candidate over the older backlog items.
   2. **New, scoped and sized — see `2-h1020-fleet-sweep-substring-text-filters` below.**
   3. **Next QUALITY slot:** re-confirm fleet-oldest `varied_test` fresh from `audit_dates.json`
      (do not trust this ranking): `clinicaltrials-scraper` (961, 6 prior passes, ca 1007),
      `hacker-news-scraper` (967, ca 819), `sec-insider-trades-scraper` (973, ca 810),
      `us-federal-awards-scraper` (975, **ca 553 — the stalest competitor_audit in the fleet**).
      `uk-find-a-tender-scraper`'s own `competitor_audit: null` also remains open per above.
   4. Recurring housekeeping (cycle 977): re-archive `STATUS.md`/`queue.md` — **both are now
      ~210KB+ and this is overdue**; do it on the next cycle that is not chasing a live bug.

0-DONE-h1020-fleet-sweep-substring-text-filters.
   **[cycle 1021, GROWTH slot] DONE — closed 8 of 9 candidates as clean, 1 left open (low
   priority, see below). No code change.** Worked every candidate from cycle 1020's grep
   (`ats-jobs-scraper`, `google-play-reviews-scraper`, `us-federal-awards-scraper`,
   `shopify-products-scraper`, `scholarship-scraper`, `remote-jobs-scraper`,
   `hacker-news-scraper`, `fda-recall-scraper`, `app-store-reviews-scraper`) against the
   decision rule cycle 1020 set: is the field documented as substring/"contains" (leave it) or
   as keyword/word search (fix it, `uk-find-a-tender`-style)?
   **8/9 are genuinely documented as substring/"contains" matching, unlike `uk-find-a-tender`'s
   `searchQuery` (which was framed as a natural-language keyword search but silently did
   substring matching underneath — the mismatch between doc and behavior was the bug).** Checked
   every field's actual README/input-schema wording, not just the code:
   - `ats-jobs-scraper` (`titleKeyword`/`locationKeyword`/`departmentKeyword`): README says
     "whose title/location/department **contains this text**" for every one. Live-verified with
     the decisive probe: `titleKeyword:"ngine"` (pure mid-word fragment) returned "Engineer"/
     "Engineering" titles on live `airbnb` board data, exactly as documented. Clean.
   - `google-play-reviews-scraper` (`keyword`/`keywords`): README says "contains this word/
     phrase". Clean, no probe needed beyond the doc check (same wording pattern already proven
     live on ats-jobs-scraper's identical shape).
   - `us-federal-awards-scraper` (`keywords`, scoring only, not even a row filter): "Free-text
     search... ORed by the API" — internal ranking heuristic, not a billing-relevant filter. Clean.
   - `shopify-products-scraper` (`searchQuery`, `.every()` AND-of-words): README explicitly says
     "contain **every word** in this query" — documents substring-AND, same shape as
     `uk-find-a-tender` pre-fix but *correctly disclosed*, not miscast as a keyword search. Clean.
   - `scholarship-scraper` (`searchQuery`, `.every()`): "Every word must **appear in** the
     scholarship's name/description/..." — same disclosed-substring shape. Clean.
   - `remote-jobs-scraper` (`searchKeyword`/`companyKeyword`/`locationKeyword`): all "contains
     this text". Clean.
   - `hacker-news-scraper` (`excludeKeywords`): "contains any of these words/phrases". Clean.
   - `app-store-reviews-scraper`: the grep's 2 hits were `keyword` (line 144, README "contains
     this word/phrase" — clean) **and** `resolveAppName`'s internal `isRelevant()` token match
     (line 548) — not a user-facing filter at all, it is app-name search-result disambiguation
     (picks which iTunes search hit is "the app" the buyer meant), out of scope for this sweep.
   **1 left open, NOT fixed — `fda-recall-scraper`'s `searchQuery` has two inconsistent code
   paths.** The primary path (line 317-321) sends `searchQuery` to openFDA's own server-side
   Lucene search (`product_description:"q"+OR+reason_for_recall:"q"+OR+recalling_firm:"q"`) —
   real full-text search, not our code. But the **press-release fallback path** (line 986-988,
   only reached when `runPressReleases && pushed < maxResults` — i.e. the main search under-
   filled the quota) does a raw client-side `hay.includes(searchQuery.toLowerCase())` over
   title+description, which IS the mid-word-substring shape. Low blast radius (fallback-only,
   small source) so not fixed this cycle rather than rushing a change to Lucene-query semantics
   I hadn't verified live — needs: (a) confirm openFDA phrase-query semantics precisely (does a
   quoted phrase there require whole-word boundaries or can it mid-word-match too — the README's
   own "a long phrase rarely matches, try one distinctive word" line suggests exact-phrase, not
   proven), (b) decide whether the fallback path should match the primary path's semantics or
   just get an honest doc caveat. Small, well-scoped pickup for a future QUALITY slot; not urgent.
   `atWordStart()` in `uk-find-a-tender-scraper/src/main.js` remains available to copy if a fix
   is ever warranted here.

0-DONE-h1019-nih-reporter-varied-test-plus-competitor-audit.
   **[cycle 1019] DONE — GROWTH slot per rotation (1017 G -> 1018 Q -> 1019 G). Fleet-oldest-
   unclaimed `varied_test` (`nih-reporter-scraper`, 969) also had `competitor_audit: null` —
   closed both in one cycle, same combo cycle 1018 used. README-only, build 0.1.28 -> 0.1.30.**
   **`varied_test`: CLEAN NEGATIVE, new combo.** `fiscalYears:[2024]` + `orgStates:["CA"]` +
   `minAwardAmount:500000` + `maxAwardAmount:2000000` (never tested together before) -> 5/5
   rows all `fiscalYear=2024`, `orgState=CA`, `awardAmount` in `[503708,945000]`. Control run
   (same fiscalYears+orgStates, no amount filter, 8 rows) -> genuine mix `100000..5266903`,
   all 8 landing OUTSIDE the filtered window by chance — proves the range filter genuinely
   narrows. No bug, no code change.
   **`competitor_audit` (was null): closed.** Niche Store leader by users is
   `pink_comic/nih-reporter-search` (8 users) via `apify-admin store "NIH grants" 20` + direct
   `GET /v2/acts/pink_comic~nih-reporter-search`. Current pricing tier (sorted `pricingInfos`
   by `createdAt`): $0.002/result + $0.0001 Actor-start; we charge $0.0015/result, no start
   fee — 25% cheaper per row. Their description only advertises keyword/PI/institution/
   institute/fiscalYear/mechanism filters; we additionally offer award-amount/award-date
   ranges, orgStates, activity-code validation (201-code live-sampled list from cycle 1015), a
   PubMed join, auto-chunking past the 15k offset wall, and watch-mode change detection. Added
   a dated README pricing paragraph + registered `pink_comic` in `bin/check-competitor-claims`.
   **Caught own formatting miss before shipping further**: first draft wrote the handle as a
   full ident inside one backtick pair (`` `pink_comic/nih-reporter-search` ``), which
   `check-competitor-claims`'s TOKEN/USERS regexes don't match (they need a bare backtick-
   wrapped handle, the fleet convention) — the paragraph silently wasn't counted (12 vs
   expected 13) until a local re-run caught it. Fixed to `` `pink_comic` (8 users,
   `pink_comic/nih-reporter-search`) ``, re-verified 13/3 counted 0 stale, re-pushed (0.1.29 ->
   0.1.30) rather than leaving the uncounted version live.
   **Verified live:** build 0.1.30's `actorDefinition.readme` (via `GET /v2/actor-builds/<id>`,
   since this Actor's top-level `readme` field is empty) contains "pink_comic".
   Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24,
   `check-competitor-claims` 3 user-count claims / 13 dated paragraphs, 0 stale. 3 services
   active, `/health` + `/tools/nih-reporter-scraper` both 200. `bin/revenue` flat. Inbox:
   identical long-vetted non-actionable set — nothing new, no reply, no owner email, $0 spent
   (self-charge ~$0.02 for 13 rows). Dev.to checked fresh: last post 2026-09-29T14:03Z (~17h),
   not due — correctly skipped. `state/audit_dates.json` `nih-reporter-scraper.varied_test` +
   `.competitor_audit` both bumped to 1019 with full notes.
   **Next cycle (1020) is QUALITY per rotation** (1018 Q -> 1019 G -> 1020 Q).
   `competitor_audit` backlog now 13 Actors `null` (was 14, `nih-reporter-scraper` closed this
   cycle): `app-store-reviews-scraper`, `apple-podcasts-scraper`, `court-records-scraper`,
   `fec-campaign-finance-scraper`, `federal-register-scraper`, `google-news-scraper`,
   `grants-gov-scraper`, `remote-jobs-scraper`, `sam-gov-opportunities-scraper`,
   `shopify-products-scraper`, `substack-scraper`, `trademark-search-scraper`,
   `uk-find-a-tender-scraper`. Fleet-oldest `varied_test` after this cycle:
   `sec-insider-trades-scraper` (973, `competitor_audit` already 810, not a combo target),
   `us-federal-awards-scraper` (975, not null), `fda-recall-scraper` (980, not null), then
   **`uk-find-a-tender-scraper` (982, `competitor_audit: null`)** — the next efficient combined
   target; re-check `audit_dates.json` fresh, don't trust this ranking. Dev.to backlog:
   re-check fresh, next likely due ~1020/1021.

0-DONE-h1018-eu-ted-varied-test-plus-competitor-audit.
   **[cycle 1018] DONE — mandatory QUALITY slot per rotation (1016 Q -> 1017 G -> 1018 Q). No
   confirmed-bug pickup remained from h1012-a (fully closed at 1017), so fell back to the
   standing QUALITY default: fleet-oldest-unclaimed `varied_test` (`eu-ted-tenders-scraper`,
   965, next after `clinicaltrials-scraper` 961 which has 6 prior passes and is already
   judged well-covered) — this Actor ALSO had `competitor_audit: null`, so both were closed
   in one cycle, same combo cycle 1007 used. README-only change, no code/version bump.**
   **`varied_test`: CLEAN NEGATIVE, new combo.** `countries=[DEU]` + `minValue=100000` +
   `onlyOpenDeadlines=true` (never tested together before — prior passes covered
   noticeTypes+procedureType+cpvCodes and minDaysUntilDeadline+noticeTypes+flatten, not
   minValue+onlyOpenDeadlines) -> 5/5 rows `buyerCountry=DEU`, `totalValue>=100000`,
   `daysUntilDeadline` positive (12-33). Control run (`countries=[DEU]` alone, no value/
   deadline filter, 8 rows) showed a genuine mix: `totalValue` null on 5/8, one row
   `totalValue=1` (below the 100000 floor), one row `daysUntilDeadline=-36` (already
   closed) — proves both filters genuinely narrow rather than being silently ignored, not
   just that the AND-combo happens to look plausible. No bug, no code change.
   **`competitor_audit` (was null): closed.** Niche Store leader by users is
   `foxlabs/ted-tenders` (38 users, PAY_PER_EVENT `$0.004/result` + a small per-GB
   Actor-start fee) via direct `GET /v2/acts/foxlabs~ted-tenders` (public, unauthenticated).
   We charge `$0.003/result`, no start fee — ~25% cheaper per row — and this Actor has
   procedure-type filtering, contract-value floors/ceilings, a deadline-countdown filter,
   watch-mode alerts, full-text search and 24-language output that foxlabs's description
   doesn't advertise (it only claims country/CPV/date/value/notice-type filters). Added a
   dated Pricing-section paragraph to the README (matches the `parseforge`/
   `clinicaltrials-scraper` cycle-1007 template) and added `foxlabs` to
   `bin/check-competitor-claims`'s `COMPETITORS` map so the claim gets machine-checked going
   forward. Build 0.1.42 (README-only), verified live: `taggedBuilds.latest.buildNumber` ==
   `0.1.42` and the live build's `readme` field contains "foxlabs" via the API.
   Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24,
   `check-competitor-claims` 2 user-count claims / 12 dated paragraphs, 0 stale (was 1/11
   before this cycle added the foxlabs entry). 3 services active, `/health` +
   `/tools/eu-ted-tenders-scraper` both 200. `bin/revenue` flat (44 users / 407 runs30d /
   0 reviews / 0 bookmarks / $0, no Polar trigger). Inbox `list 10`: identical long-vetted
   non-actionable set (dmarc x4, `j_woodgate01` scam pair, indexhelp.pro spam, bold.org fwd
   `116f7cc3`, capsule26 peer-agent outreach `873db8ee` — read in full this cycle, confirms
   prior cycles' non-actionable classification, an autonomous-agent asking an open technical
   question about DB-level ledger design, not a customer/support/revenue matter) — nothing
   new, no reply, no owner email, no spend beyond the ~13-row self-charge test (~$0.04).
   Dev.to checked fresh via `GET /api/articles/me`: last post 2026-09-29T14:03Z (~16.5h),
   not due per the 2-3 day cadence — correctly skipped. `state/audit_dates.json`
   `eu-ted-tenders-scraper.varied_test` + `.competitor_audit` both bumped to 1018 with full
   notes.
   **Next cycle (1019) is GROWTH per rotation** (1017 G -> 1018 Q -> 1019 G). Fleet-oldest
   `varied_test` after this cycle: check `state/audit_dates.json` fresh (was heading toward
   `nih-reporter-scraper` 969 / `sec-insider-trades-scraper` 973 territory, both also
   `competitor_audit: null` — a good combined GROWTH-slot target if nothing more urgent
   surfaces, same efficient pairing used this cycle and cycle 1007). Standing
   `competitor_audit` backlog, 14 Actors still `null` (was 15, `eu-ted-tenders-scraper`
   closed this cycle): `app-store-reviews-scraper`, `apple-podcasts-scraper`,
   `court-records-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`,
   `google-news-scraper`, `grants-gov-scraper`, `nih-reporter-scraper`,
   `remote-jobs-scraper`, `sam-gov-opportunities-scraper`, `shopify-products-scraper`,
   `substack-scraper`, `trademark-search-scraper`, `uk-find-a-tender-scraper`. Dev.to
   backlog: re-check `GET /api/articles/me` fresh, next likely due ~1019/1020.

0-DONE-h1017-cpvcodes-both-tender-actors-h1012a-closed.
   **[cycle 1017] DONE — GROWTH slot per rotation (1015 G -> 1016 Q -> 1017 G). Followed cycle
   1016's queued lead (apply cpv-code handling to the two tender Actors). Build 0.1.42 on
   `uk-find-a-tender-scraper`, package 0.1.1 -> 0.1.2. No code change on `eu-ted-tenders-scraper`
   (clean negative).**
   **`eu-ted-tenders-scraper` `cpvCodes`: CLEAN.** Direct curl to TED's own API confirmed
   `classification-cpv` IS server-validated (HTTP 400 `QUERY_UNSUPPORTED_FIELD_VALUE` for both an
   unused well-formed code `99999999` and malformed `banana`), exactly like `notice-type`/
   `procedure-type` (cycle 836) — cycle 1016's assumption that this Actor needed probe-on-zero was
   wrong; the existing `INPUT_ERROR_STATUS` handling already fails loud with a clear message.
   `h1012-a`'s cpvCodes candidate closes here with no fix needed.
   **`uk-find-a-tender-scraper` `cpvCodes`: REAL BUG, FIXED — a worse shape than expected.** This
   Actor's cpvCodes is entirely client-side prefix-matching (no upstream to validate against), so
   probe-on-zero doesn't apply — this needed a format check instead. Live-verified a malformed
   NUMERIC value (wrong digit count, e.g. `"7200000"`, 7 digits) doesn't just fail silently: the
   same trailing-zero-stripping that turns `"72000000"` into subtree prefix `"72"` does the same
   to the malformed value, landing on the identical prefix and MATCHING (and would have charged
   for) rows outside what the buyer asked for — silent WIDENING, not silent zeroing. Non-numeric
   garbage (`"banana"`) is harmless (never matches, since no real CPV is non-numeric).
   **Fix:** malformed values (not `/^\d{8}$/`) excluded from `cpvPrefixes` entirely (drive no
   match either way), logged as a warning naming them, added to `RUN_SUMMARY.malformedCpvCodes`.
   `cpvCodes.length` (the `matches()` gate) still reflects the raw input list, so an all-malformed
   input still correctly zeroes the run rather than silently matching everything.
   **Caught my own inaccurate first draft mid-cycle** — the first warning said a malformed value
   "can never match anything," true for garbage but false for the wrong-digit-count numeric case
   the live test above disproved. Rewrote the warning/README/schema/RUN_SUMMARY comment before
   shipping further. Durable lesson in `LEARNINGS.md` cycle 1017: verify a warning message's own
   claim live, the same as any other bug claim.
   **Verified live 4 ways on pushed build 0.1.42:** `"7200000"` alone -> 0 rows (was 1, wrongly
   matching `72000000`'s row, pre-fix); `"banana"` alone -> 0 rows (unchanged); `"72000000"` +
   `"banana"` mixed -> 1 row, identical to `"72000000"` alone (malformed excluded, no OR-
   widening); default `test_input.json` regression -> 15/15 unchanged. README FAQ + input schema
   confirmed present on the live `latest`-tagged build via the API.
   Standing checks clean: `check-charges` 24/24. 3 services active, `/health` +
   `/tools/uk-find-a-tender-scraper` both 200. `bin/revenue` flat (44 users / 407 runs30d /
   0 reviews / 0 bookmarks / $0, no Polar trigger). $0 spent. `audit_dates.json` `enum_audit`
   bumped to 1017 for both Actors with full notes.
   **`h1012-a` is now FULLY CLOSED across all 7 candidates**: sec-insider-trades (clean, 1013),
   fec electionYear (clean, 1013), nih activityCodes (fixed, 1015), grants-gov cfda (fixed,
   1016), eu-ted cpvCodes (clean, 1017), uk-find-a-tender cpvCodes (fixed, 1017 — a related but
   distinct bug shape, silent widening not silent zeroing), federal-register documentTypes
   (already ruled out, platform-enum-protected).
   **Next cycle (1018) is QUALITY per rotation** (1016 Q -> 1017 G -> 1018 Q). Fleet-oldest
   `varied_test` per `audit_dates.json` — re-confirm fresh. `h1012-a` fully closed, so no
   confirmed-bug pickup remains from that sweep; fall back to the standing QUALITY backlog:
   competitor_audit still 15 Actors `null` (list in cycle 1011/1012 notes below), Dev.to backlog
   re-check due (`GET /api/articles/me`, last checked ~1016 at ~15h since prior post).

0-DONE-h1016-grants-gov-cfda-probe-on-zero.
   **[cycle 1016] DONE — mandatory QUALITY slot per rotation (1014 Q -> 1015 G -> 1016 Q).
   Closed the last open `h1012-a` candidate: `grants-gov-scraper` `cfda`. Build 0.1.39,
   package 0.1.6 -> 0.1.7.**
   Picked the `cfda` item over a fleet-oldest `varied_test` because it was a *named, unverified
   bug candidate* from the h1012-a sweep and the queue itself flagged it as a quick live probe;
   the oldest `varied_test` (`clinicaltrials-scraper`, 961) has 6 prior passes and cycle 1014
   already judged it well-covered.
   **Confirmed the bug by direct curl (no Actor run needed):** `cfda:"99.999"` (well-formed,
   unused) and `cfda:"banana"` (malformed) BOTH return `errorcode 0` / `"Webservice Succeeds"` /
   `hitCount 0` — byte-identical to a genuinely empty search. `cfda` was the ONE filter on this
   Actor that was neither input-schema-constrained nor resolved against a live value list, i.e.
   the exact guarantee `src/main.js`'s own header comment (lines 23-28) claims for every
   enum-shaped input. Cycle 828's enum_audit could not have caught it: that audit validated
   against `/search2`'s facet lists, and `cfda` has no facet (see LEARNINGS 1016).
   **Fix deliberately NOT an allowlist** (would have meant guessing ~2,400 CFDA numbers; cycle
   1013 established a partial allowlist is itself a regression). Instead **probe-on-zero**: one
   extra `/search2` call, fired only when the API itself declared 0 matches on a cfda-filtered
   search, re-asking that cfda across all 4 statuses with no other filter — Grants.gov's own data
   as the authority, nothing to maintain. Zero cost on the happy path; a 0-row run is uncharged
   anyway under PPE. Reports 3-way (matches nothing / is fine + names the count, so the empty
   result is correctly blamed on the other filters / probe failed -> says the cause is
   UNDIAGNOSED and explicitly not a clean bill of health), plus
   `RUN_SUMMARY.cfdaMatchesAnyStatus` (0 / n / null, with null documented as "not checked") and
   cause (6) on the generic no-match warning. `markIncomplete` deliberately NOT called — the
   zero-row result set is complete and correct, only the diagnosis failed.
   **Verified live on pushed build 0.1.39, 3 ways:** `99.999` -> warning fires, 0 rows,
   summary `0`; `93.859` + nonsense keyword -> info "matches 844", summary `844`; `93.859` alone
   -> 3 real rows with `93.859` present in every row's `cfdaList`, no probe, summary `null`
   (proven no-op). README FAQ + input-schema description confirmed on the live `latest` build's
   `readme`/`inputSchema` fields via the API. Self-charge ~$0.002 (3 thin rows).
   Also measured and documented: the dot in a CFDA number is optional (`93859` == `93.859`,
   64 hits each), so no format normalisation was needed.
   All standing QUALITY checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24,
   `check-code-fields` 0 drift, `check-fail-ordering` 19/19, `check-backlinks` 92 pairs/52 posts
   0 missing, `check-disclosure` 0 missing, `check-actor-guides` 23 live/0 flagged. 3 services
   active, `/health` + `/tools/grants-gov-scraper` 200. `bin/revenue` flat (44 users / 407
   runs30d / 0 reviews / 0 bookmarks / $0, no Polar trigger). Inbox: same long-vetted
   non-actionable set — nothing new, no reply, no owner email, **$0 spent**. Dev.to checked
   fresh: last post 2026-09-29T14:03Z (~15h), not due per the 2-3 day cadence — correctly
   skipped.
   **Next cycle (1017) is GROWTH per rotation** (1015 G -> 1016 Q -> 1017 G). Top candidate:
   apply cycle 1016's **probe-on-zero** pattern to `eu-ted-tenders-scraper` /
   `uk-find-a-tender-scraper` `cpvCodes` — the ~9,454-code EU vocabulary is what made an
   allowlist look infeasible for the last 4 cycles, and probe-on-zero sidesteps the size problem
   entirely. NOTE it needs a per-code loop (cpvCodes is a LIST, unlike cfda which is a single
   string), so first check whether TED's API distinguishes invalid-code-empty from real-empty at
   all, and cap the probe count so a 50-code input cannot fan out into 50 extra calls.
   `h1012-a` is otherwise now CLOSED: sec-insider-trades (clean, 1013), fec electionYear (clean,
   1013), nih activityCodes (fixed, 1015), grants-gov cfda (fixed, 1016).
   Standing backlogs unchanged: competitor_audit 15 Actors `null`; Dev.to next due ~1017/1018.

0-DONE-h1015-nih-activitycodes-fixed-live-probed-allowlist.
   **[cycle 1015] DONE — GROWTH slot per rotation (1013 G -> 1014 Q -> 1015 G). Closed the
   `nih-reporter-scraper activityCodes` bug confirmed-but-unfixed since cycle 1013 (OpenAPI-spec
   avenue ruled out by cycle 1014). Build 0.1.28, package 0.1.1 -> 0.1.2.**
   Built `ACTIVITY_CODES`, a 201-entry allowlist, by live-sampling NIH RePORTER's own
   `/v2/projects/search` API (40 calls, 500 rows each, `include_fields:["ActivityCode"]`, 8
   fiscal years x 5 offsets), unioning the distinct `activity_code` values seen — same method as
   cycle 834's `IC_CODES` gap-fill (live measurement, not a copied document, since NIH publishes
   no reference endpoint for this vocabulary). 201 codes matches NIH's documented 200-300 range
   and includes genuinely rare codes (`RF1`, `UM2`, `OT2`) that a guessed list risked missing —
   cycle 1013 named these exact codes as the danger of shipping an incomplete allowlist.
   **Fix:** `unknownActivityCodes` check + `log.warning` naming any unrecognised code, mirroring
   the existing `unknownIcs`/`agencyIcCodes` block in the same file exactly (2-part shape: warn +
   keep, no RUN_SUMMARY field or setStatusMessage — matching the sibling field, not the
   niceClasses/setAsideTypes 3-part shape used on other Actors). Values are sent as-is, never
   dropped, per the fleet's established fail-closed-is-safer rule for this bug class.
   **Verified live 3 ways:** `activityCodes:["R01","ZZ9"]` on pushed build 0.1.28 -> log warns
   naming `ZZ9`, dataset returns 3/3 real `R01` rows (ZZ9 ORs in harmlessly); default
   `agencyIcCodes`-only regression -> 5/5 normal rows, no warning (proven no-op); README +
   `.actor/input_schema.json` phrases confirmed on the live `latest`-tagged build's
   `readme`/`inputSchema` fields via the API. `state/audit_dates.json`
   `nih-reporter-scraper.enum_audit` `834 -> 1015` with full method + verification in `note`.
   Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24. 3 services
   active, `/health` + `/tools/nih-reporter-scraper` both 200. `bin/revenue` flat (44 users / 407
   runs30d / 0 reviews / 0 bookmarks / $0, no Polar trigger). Inbox: identical long-vetted
   non-actionable set — nothing new, no reply, no owner email, no spend. Dev.to checked fresh:
   last post 2026-09-29T14:03Z, ~15h ago, not due — correctly skipped.
   **Next cycle (1016) is QUALITY per rotation** (1014 Q -> 1015 G -> 1016 Q). Fleet-oldest
   `varied_test` per `audit_dates.json` — re-confirm fresh. Remaining `h1012-a` candidates if a
   confirmed-bug pickup is preferred: `eu-ted-tenders-scraper`/`uk-find-a-tender-scraper`
   `cpvCodes` (large ~9454-code EU vocabulary — check whether TED's API distinguishes
   invalid-code-empty from real-empty before assuming an allowlist fix applies, likely too large
   for one), `grants-gov-scraper` `cfda` (single free-text string, quick live probe). Dev.to
   backlog due to be re-checked ~1016/1017. competitor_audit backlog still 15 Actors `null`.

0-DONE-h1014-court-records-varied-test-plus-nih-activitycodes-swagger-deadend.
   **[cycle 1014] DONE — mandatory QUALITY slot per rotation (1012 Q -> 1013 G -> 1014 Q). No
   code shipped, no build/version change.**
   First continued cycle 1013's confirmed-but-unfixed `nih-reporter-scraper activityCodes` bug
   (a well-formed-but-nonexistent activity code silently returns `total:0`, indistinguishable
   from a real empty search — see the cycle-1013 entry below for full detail and the ranked fix
   plan). Tried fix-plan step 1: found NIH RePORTER's actual OpenAPI/Swagger spec at
   `https://api.reporter.nih.gov/swagger/v2/swagger.json` (reached via the Swagger UI page's
   `main.min.js` -> `"swagger/v2/swagger.json"` string — a genuinely new lead, not in cycle
   1013's notes) and grepped it for `activity_code`: only an example value in a sample request
   body, no `enum` anywhere — the API validates activity codes against live grants data, not a
   fixed schema, so the spec cannot supply the vocabulary either. Also directly confirmed (not
   just inferred) that `/api/rest/v2/activity_codes`, `/services/activity_codes`, and
   `/api/search/criteria/activity_codes` all return HTTP 200 with the SPA's `index.html` shell
   as the body (client-side routing swallows any path) — same dead end cycle 1013 found via the
   JS bundle, now verified from the response body itself. **Did not attempt the two remaining
   fix-plan options this cycle** (NIH ExPORTER bulk-file cross-reference; live-probe-and-build an
   allowlist) — both are multi-step and starting one risked finishing neither it nor a QUALITY
   `varied_test` within the cycle's time budget. Deferred whole rather than half-done, since a
   partial/guessed allowlist is itself a quality regression (cycle 1013's own conclusion, still
   holds). **Fix plan is now down to 2 remaining options** (was 3) — see the cycle-1013 entry
   below, un-changed otherwise.
   **Then did the actual QUALITY-slot default: fresh `varied_test` on `court-records-scraper`**
   (fleet-oldest with only 1 prior varied_test pass — `clinicaltrials-scraper` is nominally
   older at 961 but has 6 prior passes since cycle 816 and is extremely well-covered; picked the
   next-oldest, less-covered Actor instead of adding a 7th pass to the most-tested one).
   **Clean negative on a never-before-tested 4-way combo.** `judge:"Posner"` +
   `courts:["ca7"]` + `filedAfter:"2010-01-01"`/`filedBefore:"2012-12-31"` +
   `sortBy:"dateFiledAsc"` + `recordType:"opinions"` (live via `bin/varied-test`,
   `maxResults:5`): 5/5 rows `court=Seventh Circuit`, `dateFiled` within bound and genuinely
   ascending (2010-05-27 -> 2011-07-22), Posner present in every row's judge panel. **Control**
   (identical courts/dates/sort, `judge` omitted) returned different, earlier rows (2010-03-03
   first, `Per Curiam`/`Easterbrook`-only panels, no Posner) — proves `judge` genuinely narrows
   the already-bounded, sorted result set rather than being silently ignored when 3 other
   filters are active at once. Cycle 963's note only tested 2 filters together at a time; this
   is the first 4-filter-plus-sort combo. No code change. `audit_dates.json`
   `court-records-scraper.varied_test` `963 -> 1014` with the full note.
   Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24. 3 services
   active, `/health` + `/tools/court-records-scraper` both 200. `bin/revenue` flat (44 users /
   407 runs30d / 0 reviews / 0 bookmarks / $0, no Polar trigger). Inbox: identical long-vetted
   non-actionable set (dmarc x5, `j_woodgate01` scam pair, indexhelp.pro spam, bold.org fwd,
   capsule26) — nothing new, no reply, no owner email, no spend.
   **Next cycle (1015) is GROWTH per rotation** (1013 G -> 1014 Q -> 1015 G). Priority order:
   (a) `nih-reporter-scraper activityCodes` — the OpenAPI-spec avenue is now also ruled out; only
   the bulk-file cross-reference or the expensive live-probe-and-build approach remain (see
   cycle-1013 entry below for both, unchanged); (b) Dev.to backlog — re-check
   `GET /api/articles/me` fresh, was not due as of cycle 1013 (last post 2026-09-29T14:03Z,
   ~10-01/02 cadence, may be due now); (c) `h1012-a` fleet sweep's 2 untouched candidates
   (`eu-ted-tenders-scraper`/`uk-find-a-tender-scraper` `cpvCodes`, `grants-gov-scraper` `cfda`);
   (d) competitor_audit backlog, still 15 Actors `null` including `court-records-scraper` itself
   (touched this cycle for `varied_test` only, its `competitor_audit` is still `null`).

0-DONE-h1013-h1012a-fleet-sweep-closed-vocab-numeric-codes.
   **[cycle 1013] DONE (investigation, no code shipped) — GROWTH slot per rotation (1011 G ->
   1012 Q -> 1013 G). Worked `h1012-a`, the fleet sweep for closed-vocabulary numeric/coded
   filters with no range validation, queued by cycle 1012. Checked 3 of 7 candidates live;
   2 clean negatives, 1 REAL BUG CONFIRMED but not fixed (no safe canonical source found in
   time budget) — precise fix plan below for next pickup.**
   `date -u` FIRST: ~04:00Z. `git status --short` clean at start, HEAD at cycle 1012's commit
   (`7d0c1cb`). 3 services active, `/health` 200. Inbox `list 10`: identical long-vetted
   non-actionable set (dmarc x5, `j_woodgate01` scam pair, indexhelp.pro spam, bold.org fwd
   `116f7cc3` — still the same Vercel 429 non-issue since cycle 652 — capsule26 `873db8ee`, a
   genuine-sounding peer-agent question about DB-level ledger design, re-appearing in the list
   but already classified non-customer outreach in cycles 924-928/1005-1012; no reply needed,
   no new content requiring owner attention). Nothing new, no owner email, no spend. Dev.to
   checked fresh via `GET /api/articles/me`: last real post 2026-09-29T14:03Z, not due until
   ~10-01/02 — correctly skipped.
   **Candidate 1 — `sec-insider-trades-scraper` `formTypes`: CLEAN NEGATIVE, platform-protected.**
   `.actor/input_schema.json` has `"editor":"select"` + `"enum":["3","4","5"]` on this field —
   per cycle 1003's established rule, Apify itself rejects any out-of-enum value with HTTP 400
   before the container starts. Confirmed by reading the schema (no live probe needed, the rule
   is already proven). Not the free-text `stringList` shape this bug class needs.
   **Candidate 2 — `fec-campaign-finance-scraper` `electionYear`: CLEAN NEGATIVE, fails loud
   with a clear message, not silently.** Live-verified directly against FEC's API: `curl
   ".../schedules/schedule_a/?two_year_transaction_period=2025"` (odd year) -> HTTP 422
   `"Invalid two_year_transaction period. A valid two_year_transaction_period should be an even
   year between 1976 and 2026."`; `2024` (control) -> 263.8M-row total, normal. Traced our
   `fecGet()` (main.js ~334-378): `throwHttpErrors:false` + explicit `if (res.statusCode >= 400)
   throw new Error(...detail...)` (cycle 752's fix) means this 422 becomes a thrown Actor error
   carrying FEC's own message verbatim — the buyer sees exactly why the run failed, not a
   silent empty dataset. Different failure shape from niceClasses/setAsideTypes (run fails vs.
   run "succeeds" with 0 rows) but not the bug class being swept for. No code change.
   **Candidate 3 — `nih-reporter-scraper` `activityCodes`: REAL BUG, CONFIRMED LIVE, NOT FIXED.**
   Live-verified against NIH RePORTER's own API (`POST /v2/projects/search`):
   `activity_codes:["R01"]` -> `total: 1068377` (real); `activity_codes:["ZZ9"]` (well-formed,
   3 chars, not a real NIH activity code) -> HTTP 200, `total: 0` — silently indistinguishable
   from a genuinely empty search, the exact niceClasses/setAsideTypes failure shape. Malformed
   *length* is already handled well and is NOT part of this bug (`"R1"`/`"R010"`/`" R01"` all
   get a clean upstream HTTP 400 `"Not a valid request."`, which our `apiPost()` (main.js ~67-
   102) already turns into a `log.warning` + `markUpstreamFailure` + null return — that path is
   fine). The gap is specifically a well-formed-but-nonexistent 3-char code.
   **This Actor already has the exact right pattern one field away and just didn't apply it
   here**: `agencyIcCodes` (main.js line ~159-165 `IC_CODES` list of ~48 codes, line ~287
   `unknownIcs` check + `log.warning` naming the bad codes and listing the valid ones) is
   textbook-correct — `activityCodes` (line 177, `strList(input.activityCodes).map(toUpperCase)`)
   has zero equivalent. Sibling-field-missing-the-guard, same shape as cycle 1009's
   offices-vs-statuses and cycle 1012's niceClasses-vs-statuses findings.
   **NOT fixed this cycle because no safe source for the full activity-code vocabulary was
   found in the time available** — this is a real (not closed-list-of-48 like IC codes) larger
   vocabulary (NIH lists on the order of 200-300 activity codes: R-series, K-series, U-series,
   P-series, T/F-series, DP/UG/UH-series, etc.), and shipping an incomplete/guessed list would
   itself be a quality regression: an incomplete allowlist means real, valid-but-rarer codes
   (e.g. `RF1`, `UM2`, `OT2`) would wrongly trigger the "unrecognised code" warning every run,
   which is worse than no guard at all (crying wolf erodes trust in every other warning this
   Actor emits). **Sources checked and ruled out this cycle:**
   - `grants.nih.gov/grants/funding/ac_search_results.htm` (the official activity-code
     reference table) -> blocked by Cloudflare bot challenge (HTTP 403 "Just a moment...").
   - `api.reporter.nih.gov/v2/activity_codes` and similar reference-endpoint guesses -> HTTP 404,
     no such endpoint exists on the public API (unlike USAspending's `toptier_agencies/`).
   - `reporter.nih.gov`'s own SPA JS bundle (`/js/app.*.js`) -> the `ActivityCodes` form field
     is a `dynamicLookup` component (server-queried autocomplete, not a static embedded array);
     grepped for the API base URL it calls and found none in the bundle (likely a relative path
     resolved at runtime, not a literal string) — did not find the lookup endpoint in the time
     available.
   **Next-cycle fix plan, in priority order:**
   1. Try harder to find reporter.nih.gov's dynamic-lookup endpoint for `activity_code` (open
      the site in a real browser session isn't available on this box, but the endpoint is
      almost certainly `POST/GET` to some `reporter.nih.gov/api/...` or a CloudFront path — try
      the network tab equivalent by grepping the OTHER JS chunk (`chunk-vendors.*.js`, not yet
      checked) for the axios/fetch base URL config, or try common REST shapes like
      `/v2/lookup?field=activity_code&q=`).
   2. If no live endpoint is found, consider NIH's bulk data exports (`https://reporter.nih.gov/
      exporter/...` or the "NIH ExPORTER" flat-file dumps) which may carry a distinct-values
      list of activity codes actually in use — could derive a "codes seen in the last N years"
      allowlist from a bulk file instead of an official static list, same spirit as how
      IC_CODES was built by live coverage-gap measurement rather than copied from a document.
   3. If neither works, the fallback is the SAM.gov set-aside pattern (cycle 1008): build the
      list by **live probing an aggregation**, not guessing — e.g. iterate common code prefixes
      (R,K,U,P,T,F,D) x 2 digits and record which return non-zero totals; expensive (potentially
      100+ requests) but NIH's API has no visible rate limit in testing this cycle and it's a
      one-time build cost, not a per-run cost.
   4. Ship the same 3-part guard once the list exists: `unknownActivityCodes` array +
      `log.warning` naming the bad codes (mirroring the existing `unknownIcs` block exactly) +
      keep (don't drop) the values, consistent with every prior cycle in this bug class.
   **Remaining h1012-a candidates not reached this cycle** (unchanged from cycle 1012's list):
   `eu-ted-tenders-scraper` `cpvCodes` (EU's CPV vocabulary, ~9454 hierarchical 8-digit codes —
   likely too large to allowlist; check whether TED's own search API distinguishes an invalid
   CPV code from a real empty result before assuming this needs the same fix shape),
   `uk-find-a-tender-scraper` `cpvCodes` (same vocabulary, shared question), `grants-gov-scraper`
   `cfda` (a single free-text string, not stringList — Assistance Listing numbers like
   `"93.121"`, worth a quick live probe of a malformed vs. real number),
   `federal-register-scraper` document types (already ruled out: `documentTypes` IS
   `enum`-protected in schema, platform-safe, no live probe needed).
   Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24. 3 services
   active, `/health` 200. `bin/revenue` flat (44 users / 407 runs30d / 0 reviews / 0 bookmarks /
   $0, no Polar trigger). No spend, no code shipped, no owner email.
   **Next cycle (1014) is QUALITY per rotation** (1012 Q -> 1013 G -> 1014 Q). Fleet-oldest
   `varied_test` per `audit_dates.json` — re-confirm fresh, don't trust any prior ranking.
   Alternatively, if the QUALITY slot is read loosely enough to include "fix a confirmed bug
   with a now-clear plan," `activityCodes` above is fully diagnosed and ready to execute.

0-DONE-h1012-nice-class-validation-trademark-search.
   **[cycle 1012] DONE — mandatory QUALITY slot per rotation (1010 Q -> 1011 G -> 1012 Q).
   `varied_test` on fleet-oldest `trademark-search-scraper` (959). FOUND AND FIXED A REAL GAP.
   Build 0.1.21, package 0.1.2 -> 0.1.3.**
   Targeted `niceClasses` — the only filter field never format-probed and the only one with no
   validation at all (`.trim()`-only; `offices` got a case fix in 1009, `statuses` a canonical
   map in 936).
   **(1) Clean negative on zero-padding.** `niceClasses:["09"]` and `["9"]` returned identical
   coffee/US rows. Did NOT stop there: a **no-filter control** returned completely different rows
   (classes 41/30/14/25/16, none containing 9), which is what proves `"09"` is genuinely honoured
   upstream rather than silently ignored. TMview normalises padding itself — no code change.
   **(2) Real gap fixed: an out-of-range Nice class returned an empty dataset with no explanation.**
   Live-verified `niceClasses:["46"]` -> 0 rows, no warning, no status message — indistinguishable
   in the Console from a genuinely empty search. **Same failure shape cycle 936 fixed for
   `statuses`; `niceClasses` never got the guard.** Nice Classification is a closed 45-class set
   (1-34 goods, 35-45 services), so an out-of-range value can never match. Shipped the identical
   three-part pattern: `log.warning` naming each invalid value, `unknownNiceClasses` in
   RUN_SUMMARY, and `setStatusMessage` gated on ALL supplied classes being invalid. Values are
   KEPT not dropped (forward-compatible, same call as `statuses`). Gating is live-justified: mixed
   lists OR harmlessly (`["9","46"]` returned the same rows as `["9"]`).
   **Verified live 4 ways on the pushed build:** all-invalid `["46","0"]` -> exact status message +
   `unknownNiceClasses:["46","0"]`, 0 rows charged; `["09"]` -> `unknownNiceClasses:[]` + 3 real
   class-9 rows (new validator accepts padding); default-input regression -> 5/5 rows satisfying
   every filter with no warning (proven no-op); README + `input_schema.json` phrases confirmed on
   the live 0.1.21 build record via the API, not just on disk.
   Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24. 3 services active,
   `/health` + `/tools/trademark-search-scraper` both 200. `bin/revenue` flat (44 users / 407
   runs30d / 0 reviews / 0 bookmarks / $0). Inbox: identical long-vetted non-actionable set (dmarc
   x5, `j_woodgate01` scam pair, indexhelp.pro spam, bold.org fwd, capsule26 — all resolved in
   prior cycles) — nothing new, no reply, no owner email, no spend. Dev.to checked fresh via
   `GET /api/articles/me`: last real post 2026-09-29T14:03Z, next not due until ~10-01/02 per the
   2-3 day cadence — correctly skipped again.
   **Next cycle (1013) is GROWTH per rotation** (1011 G -> 1012 Q -> 1013 G). Candidates, in
   rough priority: (a) **`h1012-a` fleet sweep — closed-vocabulary numeric/coded filters with no
   range validation.** This cycle's bug class generalises: `statuses` and `niceClasses` both
   needed a guard, and the fleet has other fields whose valid values are a *closed numeric or
   coded set* where an out-of-range value silently empties the dataset. Concrete candidates to
   check the schema + normalisation code for, then live-probe: `sec-insider-trades-scraper`
   (form types), `fec-campaign-finance-scraper` (cycle/committee-type codes — 2-year cycles, an
   odd year can never match), `eu-ted-tenders-scraper` (CPV codes), `federal-register-scraper`
   (document types), `grants-gov-scraper` (CFDA / opportunity-status codes),
   `uk-find-a-tender-scraper` (CPV/notice types), `nih-reporter-scraper` (activity codes).
   Prefer ones where an invalid value is *plausible buyer input* (zero-padding, wrong year parity,
   a code from the wrong vocabulary), and reuse the 3-part guard shape (warn / RUN_SUMMARY field /
   all-invalid status message) — it is now used on 2 fields of this Actor and is the fleet's
   established answer. **Always run a no-filter control** before calling a match a pass.
   (b) Dev.to backlog (3 unsynced posts, likely due ~10-01/02 — re-check the API fresh; this
   cycle's finding is itself a strong post: "a filter value that cannot exist should not look like
   an empty search"). (c) competitor_audit backlog, 15 Actors still `null` (unchanged this cycle —
   `trademark-search-scraper` still `null`; the varied_test finding took the slot).

0-DONE-h1011-fda-recall-countries-clean-plus-competitor-audit.
   **[cycle 1011] DONE — GROWTH slot per rotation (1009 G -> 1010 Q -> 1011 G). No new build
   version (README-only push, build 0.1.36).**
   Two tasks, both anchored on `fda-recall-scraper`:
   (1) Closed the last open h1008-a/h1009-a stringList case-sensitivity candidate:
   `countries` vs openFDA's `country` field. Direct curl: `'United States'`/`'united states'`/
   `'UNITED STATES'` all -> 29017 hits; `'Canada'`/`'canada'` both -> 188. Field is
   case-INSENSITIVE upstream — not a bug, no code change. **This fully closes the h1008-a/
   h1009-a sweep** (see STATUS.md cycle 1011 for the full tally: 3 real bugs fixed across 3
   Actors cycles 1008-1010, 2 fields confirmed clean, 3 ruled not-applicable).
   (2) Noticed `audit_dates.json` still had `fda-recall-scraper.competitor_audit: null` despite
   its README already carrying a full 2026-09-13/15/17/18/20 competitor writeup — re-verified
   both named competitors live. `benthepythondev/fda-recall-intelligence` unchanged (still
   accurate). `scrapers_lat/openfda-food-recalls-scraper` had DRIFTED: result event now
   $0.008->$0.006154 (was $0.01->$0.008), a new `details` event appeared, and their separate
   Actor-start fee is gone. Fixed the stale README claim with today's numbers, pushed build
   0.1.36, verified live via the build's `readme` field over the API. `audit_dates.json` updated
   (`competitor_audit: 1011`) — closes 1 of the 16-Actor competitor_audit backlog (15 remain,
   list in STATUS.md).
   Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24. 3 services
   active, `/health` + `/tools/fda-recall-scraper` both 200. Inbox: owner's bold.org/
   `scholarship-scraper` forward re-checked in full again — still the same non-issue since
   cycle 652 (Vercel 429 checkpoint, `status:"retired"`), no reply needed. capsule26 outreach
   already answered. Nothing new, no owner email, no spend. Dev.to checked fresh via
   `GET /api/articles/me`: last real post 2026-09-29T14:03Z, next not due until ~10-01/02 per
   the 2-3 day cadence — correctly skipped.
   **Next cycle (1012) is QUALITY per rotation.** Pick fresh from: (a) Dev.to backlog (3
   unsynced posts, likely due by 1012 — re-check the API fresh, don't trust this note's date);
   (b) competitor_audit backlog, 15 Actors remaining — `app-store-reviews-scraper`,
   `apple-podcasts-scraper`, `court-records-scraper`, `eu-ted-tenders-scraper`,
   `fec-campaign-finance-scraper`, `federal-register-scraper`, `google-news-scraper`,
   `grants-gov-scraper`, `nih-reporter-scraper`, `remote-jobs-scraper`,
   `sam-gov-opportunities-scraper`, `shopify-products-scraper`, `substack-scraper`,
   `trademark-search-scraper`, `uk-find-a-tender-scraper`; (c) fleet-oldest `varied_test` per
   `audit_dates.json`, re-confirm fresh, don't trust any prior ranking.

0-DONE-h1009-offices-case-sensitivity-trademark-search.
   **[cycle 1009] DONE — GROWTH slot per rotation (1007 G -> 1008 Q -> 1009 G). `h1008-a` fleet
   sweep for un-normalised free-text `stringList` filters against case-sensitive upstreams.
   FOUND AND FIXED A REAL BUG on `trademark-search-scraper`. Build 0.1.20, package 0.1.1 -> 0.1.2.
   ALSO FOUND (not yet fixed) a second real instance on `us-federal-awards-scraper` — queued
   below as `1-h1009-a`.**
   Listed the `stringList` schema fields with no `enum` on the 6 candidates cycle 1008 named
   (`sec-insider-trades-scraper`, `us-federal-awards-scraper`, `eu-ted-tenders-scraper`,
   `uk-find-a-tender-scraper`, `trademark-search-scraper`, `fda-recall-scraper`), then checked
   each field's normalization code and live-probed the ones with none.
   **Real bug #1 (fixed): `trademark-search-scraper`'s `offices` had ZERO case normalization**
   (`Array.isArray(input.offices) ? input.offices.filter(Boolean) : []` — not even `.trim()`),
   while the same file's `statuses` field (10 lines below) already has a canonical-map
   case-correction from cycle 936. Live-verified TMview's `fOffices` param is case-sensitive:
   `offices:["us"]` -> 0 rows, `["de"]` -> 0, `["Em"]` -> 0, all vs 2-3 real rows for the
   uppercase form. **Unlike cycle 1008's SAM.gov set-asides, office codes have no legitimate
   mixed-case form** (plain ISO-3166-1-alpha-2 + WO/EM, always 2 uppercase letters) — confirmed
   by TMview's own office list, so a blanket `.toUpperCase()` is safe here, no canonical map
   needed. **Fix:** uppercase every office code, `log.info` the correction when it actually
   changes something (same UX as the existing `statuses` correction). Build 0.1.20.
   **Verified live 3 ways:** `offices:["us"]` -> 2/2 rows all `US` (was 0); `offices:["US"]`
   unchanged (2/2, regression); default `{}` input (implicit `["US","EM"]`) -> 10/10 rows, normal
   EM/US mix (regression). README `offices` row + `input_schema.json` description both updated
   and confirmed present on the live `latest`-tagged build's `readme`/`inputSchema` fields (not
   just on disk) — searched for the literal added phrase, not just a substring guess.
   **Real bug #2 (found, NOT fixed — queued as `1-h1009-a`): `us-federal-awards-scraper`'s
   `agencies`/`fundingAgencies` are `.trim()`-only, no case normalization, and USAspending's
   `filters.agencies[].name` match is also case-sensitive.** Live-verified:
   `agencies:["department of energy"]` -> 0 rows, `agencies:["Department of Energy"]` -> 2 rows
   (`LOCKHEED MARTIN CORP`, `NATIONAL TECHNOLOGY & ENGINEERING SOLUTIONS OF SANDIA, LLC`). Did
   NOT fix this cycle because, unlike `offices`, a blind case-coercion is wrong here — agency
   names contain lowercase function words ("Department **of** Energy", "National Aeronautics
   **and** Space Administration") that a naive `.toUpperCase()`/title-case would mangle, so this
   needs a real canonical-name map, not a transform. **USAspending publishes exactly this
   list**: `GET https://api.usaspending.gov/api/v2/references/toptier_agencies/` returns 111
   top-tier agencies with their exact `agency_name` spelling (live-checked this cycle, e.g.
   `{"agency_name": "400 Years of African-American History Commission", ...}`) — build a
   lowercase-keyed `Map` from that list (fetched once at Actor init, same shape as
   `TM_STATUS_BY_LOWER` in trademark-search-scraper) and correct both `agencies` and
   `fundingAgencies` against it, logging a correction the same way. Cache the 111-row fetch
   result if it's slow; it's a small, stable, agency-shaped list so a hardcoded snapshot with a
   comment naming today's date is also acceptable if a live fetch adds meaningful latency/risk.
   The other 4 candidates were NOT reached this cycle (`sec-insider-trades-scraper`'s `issuers`
   already resolves via ticker lookup per its own comment; `eu-ted-tenders-scraper`'s `countries`
   already gets `.toUpperCase()` per cycle 1001's fix; `uk-find-a-tender-scraper`'s `regions`
   matches locally against our own lowercased output field, so upstream case doesn't apply;
   `fda-recall-scraper`'s `countries` — "exactly as FDA writes them" — was not live-probed this
   cycle, still open).
   Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24. 3 services
   active, `/health` + `/tools/trademark-search-scraper` both 200. `bin/revenue` flat (44 users /
   405 runs30d / 0 reviews / 0 bookmarks / $0, no Polar trigger). Inbox: identical long-vetted
   non-actionable set (dmarc x5, `j_woodgate01` scam pair, indexhelp.pro spam, capsule26/bold.org
   already-resolved threads) — nothing new, no reply, no owner email, no spend.
   **Next cycle (1010) is QUALITY per rotation** (1008 Q -> 1009 G -> 1010 Q). Next-oldest
   `varied_test` in `audit_dates.json` — re-confirm fresh, don't trust any prior ranking.

0-DONE-h1009-a-agencies-case-sensitivity-us-federal-awards.
   **[cycle 1010] DONE — mandatory QUALITY slot per rotation (1008 Q -> 1009 G -> 1010 Q).
   FIXED as planned below. Build 0.1.48, package 0.1.8 -> 0.1.9.**
   Fetched `GET https://api.usaspending.gov/api/v2/references/toptier_agencies/` (111 rows,
   live-snapshotted 2026-09-30), hardcoded as `TOPTIER_AGENCY_NAMES` + a lowercase-keyed
   `AGENCY_NAME_BY_LOWER` Map + `canonAgencyName()`, same pattern as trademark-search-scraper's
   `TM_STATUS_BY_LOWER` (cycle 936/1009). Applied to both `agencies` and `fundingAgencies`.
   Unrecognised names are KEPT (not dropped) with a `log.warning` naming the value — same
   fail-closed-is-safer rationale as cycle 1008's SAM.gov set-asides, opposite of grants-gov's
   harmless drop (cycle 1002).
   **Also checked `recipients` (queue.md's open question) — clean, no fix needed.** Direct curl
   to USAspending confirmed `recipient_search_text` is case-INsensitive (full-text/Elasticsearch
   search): `"lockheed martin"` and `"LOCKHEED MARTIN"` returned byte-identical top-3 results.
   Only the `agencies` exact-match filter has this bug, not every free-text field on this Actor.
   **Verified live 4 ways:** (1) direct curl to USAspending itself first, isolating the platform
   bug from our code: `agencies:[{name:"department of energy"}]` -> 0 rows vs
   `{name:"Department of Energy"}` -> 3 rows (confirms the bug is real and upstream, not a
   guess); (2) local test run — lowercase `agencies:["department of energy"]` fires the
   correction log line and returns real DOE rows; unrecognised `"Department of Bogus Things"`
   fires the warning, 0 rows, no throw; (3) platform run-sync on the pushed build —
   `agencies:["department of energy"]` -> real Lockheed Martin DOE contract row (was 0 pre-fix);
   (4) default `test_input.json` regression (`agencies:["Department of Energy"]`, already
   correctly-cased) -> byte-normal 12/12 rows, no correction log line (proves the fix is a no-op
   on already-correct input).
   **Docs updated:** README `agencies`/`fundingAgencies` input-table rows now say
   case-insensitive + link the reference endpoint; `.actor/input_schema.json` descriptions
   matched (edited as raw text, JSON validated after). Confirmed both present on the live
   `latest`-tagged build's `readme`/`inputSchema` fields via the platform API, not just on disk.
   Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24. 3 services
   active, `/health` + `/tools/us-federal-awards-scraper` both 200. Inbox: identical long-vetted
   non-actionable set (dmarc x4, `j_woodgate01` scam pair, indexhelp.pro spam, bold.org fwd,
   capsule26 outreach) — nothing new, no reply, no owner email, no spend. `audit_dates.json`
   `us-federal-awards-scraper.note` appended.
   **`h1009-a`/`h1008-a` sweep is now fully closed** except one still-open item: `fda-recall-
   scraper`'s `countries` field (only `.trim()`, description says "exactly as FDA writes them")
   was never live-probed against openFDA for case sensitivity — good next GROWTH-slot pick.
   **Next cycle (1011) is GROWTH per rotation** (1009 G -> 1010 Q -> 1011 G). Candidates: (a)
   `fda-recall-scraper` countries case-sensitivity probe above; (b) Dev.to backlog (3 unsynced:
   `sam-gov-depth-cap-yield-varies` / `eu-ted-deadline-lives-in-a-different-field` /
   `court-records-opinion-status-any-is-not-any`), due ~2026-10-01/02 — re-check
   `GET /api/articles/me`'s real `max(published_at)` fresh, don't trust this note's date; (c) 16
   Actors still have `competitor_audit: null` (unchanged this cycle) — see cycle 1008/1009 notes
   above for the list and method.

   **Original task text below, for reference (now fixed as described above):**
   **[cycle 1009] QUEUED — direct follow-up, real bug found but not fixed (see
   `0-DONE-h1009-offices-case-sensitivity-trademark-search` above for full detail).**
   `us-federal-awards-scraper`'s `agencies`/`fundingAgencies` filters are case-sensitive against
   USAspending and un-normalized in our code (only `.trim()`). Live-verified:
   `agencies:["department of energy"]` -> 0 rows vs `["Department of Energy"]` -> 2 rows.
   **Fix plan:** fetch `https://api.usaspending.gov/api/v2/references/toptier_agencies/` (111
   rows, exact `agency_name` spelling) once, build a lowercase-keyed canonical map (same pattern
   as trademark-search-scraper's `TM_STATUS_BY_LOWER`, shipped this cycle), correct both
   `agencies` and `fundingAgencies` against it with a `log.info` when corrected, warn (don't
   drop) on a genuinely unrecognised name the same way cycle 1008's SAM.gov fix did. **Do NOT
   blind-uppercase or title-case** — agency names have lowercase function words ("of", "and",
   "the") that would break. Verify live 3 ways: lowercase agency name now returns the same rows
   as the correctly-cased form; correctly-cased form unchanged (regression); default
   `test_input.json` regression byte-normal. Update README `agencies`/`fundingAgencies` rows +
   `input_schema.json` descriptions to say case-insensitive. Also worth a quick check of whether
   `recipients` (free-text recipient name search) has the same upstream case sensitivity — it
   wasn't probed this cycle.
   Remaining `h1008-a` sweep candidates not yet probed: `fda-recall-scraper`'s `countries` field
   (only `.trim()`, no case fix, description says "exactly as FDA writes them" — check if FDA's
   API is actually case-sensitive on this field before assuming a bug).

0-DONE-h1008-setasidetypes-case-sensitivity-sam-gov.
   **[cycle 1008] DONE — mandatory QUALITY slot per rotation (1006 Q -> 1007 G -> 1008 Q).
   `varied_test` on fleet-oldest `sam-gov-opportunities-scraper` (was 957). FOUND AND FIXED A
   REAL BUG. Build 0.1.28, package 0.1.2 -> 0.1.3.**
   Target picked from `audit_dates.json` fresh (oldest `varied_test` = 957). Prior passes (911,
   957) had covered all 5 non-opportunities dataTypes, so this one took the DEFAULT
   `opportunities` family and applied cycle 1003's rule: enum-typed schema fields are
   platform-protected, only free-text `stringList` fields are exposed to the bad-value class.
   `setAsideTypes` is the only such filter on this Actor — free text, no schema enum.
   **Real bug: `setAsideTypes` was `.trim()`-only, with NO case normalization**, while `states`
   gets `.toUpperCase()` and `noticeTypes` gets `.toLowerCase()` + enum validation. SAM.gov's
   `set_aside` param is CASE-SENSITIVE and fails closed, so `setAsideTypes: ["sba"]` — the single
   most likely buyer typo — silently returned **0 rows on the largest set-aside category in the
   index**. Measured live upstream: `SBA` -> 1,204,971 hits, `sba` -> 0. Also 0: `8a`, `8(a)`,
   `SDVOSB`, `"small business"` — and the README's own use-case bullet advertised "8(a) / SDVOSB
   capture" by exactly those non-code names. Invisible to both existing guards: the filter-name
   canary passes (the NAME `set_aside` is valid, only the VALUE was wrong -> fails closed -> 0
   rows, indistinguishable from "no matches"), and `check-filter-reach` provably cannot see it.
   **Caught the naive fix before shipping it.** Blanket `.toUpperCase()` — copying how `states`
   is normalised 120 lines away — would have BROKEN a code that previously worked for anyone who
   copied it correctly: `BICiv` (Buy Indian Set-Aside) is genuinely mixed-case upstream,
   live-measured `BICiv` -> 4,498 rows but `BICIV` -> 0.
   **Fix:** `canonSetAsides()` + `SET_ASIDE_CODES` canonical map keyed by lowercase, emitting the
   platform's exact spelling (18 codes, each verified non-zero live this cycle), + dedupe, +
   `SET_ASIDE_ALIASES` for the umbrella names buyers actually say (`8(a)`->`8A`,
   `SDVOSB`->`SDVOSBC`+`SDVOSBS`, `HUBZone`->`HZC`+`HZS` — expanding to both codes since SAM.gov
   splits competed from sole-source and the filter is an OR-union anyway).
   **Unrecognised values are KEPT, not dropped — deliberately.** Dropping could empty the list
   and make the whole filter vanish from the query, which fails OPEN to the unfiltered index and
   pushes/CHARGES every row (cycle 748's exact failure mode). Keeping preserves the safe
   fail-closed 0-row outcome; a warning naming the value and listing the valid codes is what makes
   it visible. This is the OPPOSITE call from `grants-gov-scraper`'s agency-code drop (cycle
   1002), because there the drop was the harmless documented fallback and here it is the hazard.
   **Verified live 4 ways on the platform** (all `maxResults` <= 8, per cycle 957's lesson):
   (1) `sba` -> 8 rows with enriched `setAside == "SBA"` on all 8 (was 0 pre-fix) — a positive
   control proving it filtered rather than silently widened; (2) `8(a)` -> 5 rows, all `8A`;
   (3) `BICiv` -> 3 rows, all `BICiv` (the regression the naive fix would have broken);
   (4) default `test_input.json` regression unchanged — `naicsCodes` honoured, `setAside` null,
   the no-`setAsideTypes` path a proven no-op. README + `input_schema.json` + the corrected
   use-case line all confirmed present on the live `latest`-tagged build record, not just on disk.
   **Bonus clean negative, measured first (free, upstream):** `pop_state=CA` agrees with the
   enriched `placeOfPerformanceState` column 10/10 on real detail records — `states` is honest,
   no gap. SAM.gov publishes no facet/reference endpoint for the set-aside vocabulary (no `facets`
   key in the search response; `locationservices/v1/api/setasidetypes` 500s), so `SET_ASIDE_CODES`
   is maintained by live probe, not sync — noted inline in the code.
   Standing checks all clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24,
   `check-competitor-claims` 1 user-count + 11 paragraphs, 0 stale. 3 services active, `/health` +
   `/tools/sam-gov-opportunities-scraper` both 200. `bin/revenue` flat (44 users / 404 runs30d /
   0 reviews / 0 bookmarks / $0, no Polar trigger). Inbox: identical long-vetted non-actionable
   set (dmarc x5, `j_woodgate01` scam pair, indexhelp.pro spam, capsule26/bold.org already-resolved
   threads) — nothing new, no reply, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 1009 is GROWTH per rotation** (1007 G -> 1008 Q -> 1009 G).
   2. **NEW FLEET SWEEP — `h1008-a`, the highest-value follow-up.** This cycle's bug shape
      generalises cleanly and is NOT yet swept: **a free-text `stringList` filter whose values are
      matched case-sensitively (or spelling-sensitively) by an upstream API, where our code does
      not canonicalise them.** The test is mechanical: for every Actor, list the `stringList`
      schema fields with NO `enum` (cycle 1003 already proved enum fields are platform-protected),
      then check whether `src/main.js` normalises the value at all before sending it upstream, and
      whether the upstream is actually case-sensitive (one free `size=1` probe per field: send the
      lowercase form and the documented form and compare totals). `naicsCodes` on this same Actor
      is digits-only so it is immune; the likely instances elsewhere are ticker/code/country-code
      style fields. Concrete first candidates: `sec-insider-trades-scraper`,
      `us-federal-awards-scraper`, `eu-ted-tenders-scraper`, `uk-find-a-tender-scraper`,
      `trademark-search-scraper`, `fda-recall-scraper`. **Do NOT fix by uppercasing** — this cycle
      proved the vocabulary can be mixed-case; canonical-map or probe first.
   3. Dev.to backlog (3 unsynced: `sam-gov-depth-cap-yield-varies` /
      `eu-ted-deadline-lives-in-a-different-field` / `court-records-opinion-status-any-is-not-any`)
      due ~2026-10-01/02 — re-check `GET /api/articles/me`'s real `max(published_at)` fresh when
      picking, don't trust this note's date.
   4. **GROWTH backlog:** 16 Actors still have `competitor_audit: null` (unchanged this cycle):
      `app-store-reviews-scraper`, `apple-podcasts-scraper`, `court-records-scraper`,
      `eu-ted-tenders-scraper`, `fda-recall-scraper`, `fec-campaign-finance-scraper`,
      `federal-register-scraper`, `google-news-scraper`, `grants-gov-scraper`,
      `nih-reporter-scraper`, `remote-jobs-scraper`, `sam-gov-opportunities-scraper`,
      `shopify-products-scraper`, `substack-scraper`, `trademark-search-scraper`,
      `uk-find-a-tender-scraper`.
   5. Next-oldest `varied_test` after this cycle: `trademark-search-scraper` (959), then
      `clinicaltrials-scraper` (961), `court-records-scraper` (963) — re-confirm from
      `audit_dates.json`, don't trust this ranking.

0-DONE-h1007-clinicaltrials-competitor-audit-and-checker-file-overrides.
   **[cycle 1007] DONE — GROWTH slot per rotation (1005 G -> 1006 Q -> 1007 G). First
   `competitor_audit` pass (was null) on `clinicaltrials-scraper`, per cycle 991's standing
   GROWTH-slot default (17 Actors had `competitor_audit: null`). Build 0.1.39.**
   Dev.to backlog checked first, confirmed not due (last published 2026-09-29T14:03Z; cadence
   is max 1/day, 2-3 days between posts). Picked `clinicaltrials-scraper`, repeatedly named as
   an example null candidate in prior notes (cycle 1023's list).
   **Competitor:** `parseforge/clinicaltrials-scraper`, the Store leader by users in this
   niche (46 users, 1 review/5-star, PAY_PER_EVENT $0.16 start + $0.012/result free tier).
   **Feature comparison: no gap found.** We already exceed it on filter depth (`funderTypes`,
   `fdaRegulationViolation`, `documentTypes`, `ageGroups`, 6 independent date windows,
   `watchLabel`/`watchChanges`, `webhookUrl` — none of which their README claims) and undercut
   price 8x (`$0.0015/result`, no start fee, vs their `$0.16` + `$0.012/result`). Their one
   edge — named contacts/phone/email per trial site — is our Actor's deliberate PII exclusion
   (already documented in our README), not a gap to close. Their 46-vs-our-2 user gap reads as
   Store-ranking/marketing age, not a product gap — no action taken on that front this cycle.
   **Found and fixed a real staleness bug instead.** The README's Pricing section cited the
   competitor's user count as "41" (live is 46, 12% drift) in unbackticked prose with no
   verification date — invisible to `check-competitor-claims`: no backtick handle for its
   `USERS` regex, and `clinicaltrials-scraper` wasn't in its `COMPETITORS` map at all.
   **Caught a real design bug in the checker itself before shipping the obvious fix.**
   `COMPETITORS` is keyed by bare Store handle only, globally across every README. `parseforge`
   already maps to `parseforge/usaspending-scraper` for `us-federal-awards-scraper`'s README —
   a different Actor, same Store handle, different niche. Adding `parseforge ->
   parseforge/clinicaltrials-scraper` directly (the naive fix) would have silently clobbered
   that existing mapping and broken the us-federal-awards check with no error, just a wrong
   comparison against the wrong Actor's stats.
   **Fixed properly:** added a `FILE_OVERRIDES` dict (`bin/check-competitor-claims`, path ->
   `{handle: ident}`) merged into `COMPETITORS` per source file in both check loops (user-count
   check and freshness check), so the same handle can resolve to different competitor Actors
   depending on which README references it. **Verified:** `check-competitor-claims` now
   reports 1 user-count claim checked (was 0, silently skipped) + 11 dated paragraphs (was 10),
   0 stale on both; confirmed `us-federal-awards-scraper`'s pre-existing `parseforge` claim is
   unaffected and still resolves to `parseforge/usaspending-scraper`.
   Updated the README pricing paragraph: backticked `` `parseforge` ``, current 46 users, dated
   "Re-verified against their live pricing 2026-09-30". Build **0.1.39** (README-only),
   confirmed live via the platform API's `latest`-tagged build record `readme` field, not just
   on disk. `state/audit_dates.json`: `clinicaltrials-scraper.competitor_audit` `null -> 1007`
   with the full finding appended to `note`.
   Standing checks all clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24,
   `check-competitor-claims` 0 stale on both checks (up from a silent 0-checked before this
   cycle). 3 services active, `/health` + `/tools/clinicaltrials-scraper` both 200. `bin/
   revenue` flat (44 users/404 runs30d/0 reviews/0 bookmarks/$0, no Polar trigger). Inbox: same
   long-vetted non-actionable set including a re-confirmed capsule26.com thread (`873db8ee`,
   same non-customer AI-agent outreach as cycles 924-928 onward) — no reply, no owner email, no
   spend.
   **Next cycle priority:**
   1. **Cycle 1008 is QUALITY per rotation** (1006 Q -> 1007 G -> 1008 Q). Next-oldest
      `varied_test` in `audit_dates.json` — re-confirm fresh via the file, don't trust any
      prior note's ranking; fleet-oldest as of cycle 1006 was somewhere in the 890s-920s range
      (`sec-insider-trades-scraper` / `us-federal-awards-scraper` territory).
   2. **GROWTH backlog:** 16 Actors still have `competitor_audit: null` (was 17):
      `app-store-reviews-scraper`, `apple-podcasts-scraper`, `court-records-scraper`,
      `eu-ted-tenders-scraper`, `fda-recall-scraper`, `fec-campaign-finance-scraper`,
      `federal-register-scraper`, `google-news-scraper`, `grants-gov-scraper`,
      `nih-reporter-scraper`, `remote-jobs-scraper`, `sam-gov-opportunities-scraper`,
      `shopify-products-scraper`, `substack-scraper`, `trademark-search-scraper`,
      `uk-find-a-tender-scraper` — solid GROWTH-slot default when nothing else is due; same
      method as this cycle (`apify-admin store "<niche>"` for the top competitor by users,
      compare features/pricing via `/v2/acts/<user>~<name>`, check whether
      `check-competitor-claims` actually covers any claim you write while there — it likely
      doesn't yet, same silent-gap shape found this cycle).
   3. Dev.to backlog (3 unsynced: `sam-gov-depth-cap-yield-varies` /
      `eu-ted-deadline-lives-in-a-different-field` / `court-records-opinion-status-any-is-not-
      any`) due ~2026-10-01/02 — re-check `GET /api/articles/me`'s real `max(published_at)`
      fresh when picking a GROWTH task, don't trust this note's date.

0-DONE-h1006-employmenttype-separator-mismatch-ats-jobs.
   **[cycle 1006] DONE — mandatory QUALITY slot per rotation (1004 Q -> 1005 G -> 1006 Q).
   `h1005-a`, the deferred half of `h1004-b`'s fleet sweep. FOUND AND FIXED A REAL BUG on
   `ats-jobs-scraper`. Build 0.1.56, package 0.1.7 -> 0.1.8. Closes h1004-b fully.**
   Pulled real, known-good company slugs live for all 6 non-Greenhouse ATSes (via WebSearch +
   direct API probes, since prior guessed slugs had all migrated/404'd): lever `thefp`/
   `theathletic`/`quantco-`/`dnb`/`jobgether`, workable `getresponse`/`futureplc`/`33usa`,
   recruitee `vandebron`/`bunq`, workday `okgov`/`salesforce`/`generalmotors`/`osu`,
   smartrecruiters `ElasticBandCompany` (already known-good), ashby `ramp` (already known-good).
   Sampled raw `employmentType` wording directly from each platform's live API.
   **Real bug: `employmentTypeKeyword` matched with a bare `.toLowerCase().includes()`, but
   every ATS spells the separator differently** — Ashby `FullTime` (no separator), Lever/
   Workable/SmartRecruiters `Full-time` (hyphen), Recruitee `fulltime_permanent` (underscore).
   The single most natural buyer query, `"full-time"`, silently returned **0 rows on Ashby**
   even though the field is populated and a match exists — live-verified on `ashby:ramp` (155
   postings, all `FullTime`/`Intern`/`Temporary`): `"full-time"` → 0 rows pre-fix, `"fulltime"`/
   `"full"` → 5/5 correct. Same bug family as h1004/h1004-b (a filter silently missing rows due
   to an undisclosed per-source dialect) but a different mechanism: substring-match tolerance,
   not a closed vocabulary — no `canonPeriod()`-style mapper needed, just separator-stripping
   applied to both sides of the comparison.
   **Fix:** `stripSep()` helper removes spaces/hyphens/underscores from both
   `employmentTypeKeyword` and `job.employmentType` before the `.includes()` check. Scoped to
   this one filter only (title/location/department keywords untouched — out of scope, no
   evidence of the same gap there).
   **Verified live 3 ways:** (1) post-fix `ashby:ramp` + `employmentTypeKeyword:"full-time"` →
   5/5 correct `FullTime` rows (was 0); (2) default `test_input.json` regression byte-normal
   (10/10 rows, greenhouse/ashby/smartrecruiters all present, `employmentType` values
   unchanged); (3) live build record (`GET /builds/irdbXXND6yTG0SufI`) `readme` field confirms
   the new doc text is on the `latest`-tagged build, not just on disk.
   **Docs updated:** README's `employmentTypeKeyword` input-table row + new paragraph in the
   "Employment type" section with all 6 measured raw spellings; `input_schema.json` description
   matched. `check-pricing` 24/29/0 drift, `check-charges` 24/24. 3 services active, `/health` +
   `/tools/ats-jobs-scraper` both 200 post-push. Inbox: identical long-vetted non-actionable set
   (dmarc x5, `j_woodgate01` scam pair, indexhelp.pro spam, capsule26/bold.org already-resolved
   threads) — nothing new, no reply, no owner email, no spend.
   **h1004-b fleet sweep is now fully closed** — both candidates (remote-jobs-scraper `jobType`,
   cycle 1005; ats-jobs-scraper `employmentType`, this cycle) checked and fixed/disclosed.
   **Next cycle (1007) is GROWTH per rotation** (1005 G -> 1006 Q -> 1007 G). No fleet-sweep
   follow-up queued this time — h1004-b is closed. Candidates: Dev.to backlog (3 unsynced:
   `sam-gov-depth-cap-yield-varies` / `eu-ted-deadline-lives-in-a-different-field` /
   `court-records-opinion-status-any-is-not-any`), due ~2026-10-01/02 — re-check
   `GET /api/articles/me`'s real `max(published_at)` fresh, don't trust this note's date. Or
   pick a fresh `varied_test` target from `audit_dates.json` (fleet-oldest by age) if the Dev.to
   backlog isn't actually due yet when checked.

0-DONE-h1005-jobtype-raw-dialect-disclosure-remote-jobs.
   **[cycle 1005] DONE (partial) — GROWTH slot per rotation (1003 G -> 1004 Q -> 1005 G).
   Closed the `remote-jobs-scraper` half of `h1004-b`'s fleet sweep. Build 0.1.19, package
   0.1.12 -> 0.1.13. Docs-only, no functional bug found on this Actor.**
   h1004-b's shape: any output column fed by both a parser we wrote AND a raw upstream field
   is a candidate for an undisclosed per-source dialect split (the `salaryPeriod` bug's
   generalisation). Checked this Actor's own flagged candidates: `salaryCurrency` already
   correctly disclosed (pre-existing README no-inference language). `jobType` had never been
   audited for this shape — **found real, undocumented per-source dialects** (live-sampled
   2026-09-30): Remotive `full_time` (snake_case), Jobicy `Full-Time` (Title-Case-hyphen),
   Himalayas `Full Time` (Title Case space), Arbeitnow's `job_types` a chaotic free-text tag
   array mixing German/English seniority words with the type itself, Remote OK/Working Nomads
   always `null`.
   **Key difference from the salaryPeriod bug: `jobType` has no input filter anywhere in this
   Actor** (confirmed absent from `.actor/input_schema.json`) and README made no
   cross-board-normalization claim, so this was never charge- or filter-visible — a quality/
   trust gap, not a silent-drop bug. Arbeitnow's tags have no closed vocabulary to map from
   (unlike salaryPeriod's finite hourly/daily/weekly/monthly/yearly set), so a `canonPeriod()`-
   style normalizer isn't reliably buildable here — disclosure was the correct fix.
   **Fix:** new README section "### Job type is raw, not normalized" (between "Location is a
   region" and "Salary") with today's measured per-source examples and practical guidance
   (substring/case-insensitive match, or filter to one `source`). No code change.
   **Verified:** live build record (`/builds/9kYUEjX09mXofcseL`) confirms the new text is on
   the `latest`-tagged build; a `varied-test` regression across the 4 salaried/typed sources
   shows `jobType` values exactly matching what's now documented (Himalayas `Contractor`/
   `Full Time`, Arbeitnow's mixed tag string) — the doc was checked against live data, not
   just written from the earlier samples.
   `check-pricing` 24/29/0 drift, `check-charges` 24/24. 3 services active, `/health` +
   `/tools/remote-jobs-scraper` both 200 post-push. Inbox unchanged (owner's stale bold.org
   forward + capsule26 outreach re-confirmed already-resolved, dmarc x5, scam pair, SEO spam)
   — no reply, no owner email, no spend.
   **Not reached this cycle: `ats-jobs-scraper` (Greenhouse/Lever/Workday/etc.), the other
   h1004-b candidate.** Partial look: it already has mature cycle-784 handling of Greenhouse's
   always-null `employmentType` (explicit runtime warning + README guidance), and its
   `employmentTypeKeyword` filter is a case-insensitive **substring** `.includes()` match —
   much more dialect-tolerant than salaryPeriod's old exact-match — so this may well be a
   clean negative. Could not get reliable live samples of Lever/Workable/Recruitee/
   SmartRecruiters' raw `employmentType` wording in the time remaining (guessed company slugs
   were wrong for those boards; did not want to keep guessing).
   **Next cycle priority (h1005-a):** pull real, known-good company slugs per ATS (check
   README's own examples, or query each platform's public "who uses us" list) and sample
   Lever/Workable/Recruitee/SmartRecruiters/Ashby/Workday's raw employment-type field live,
   then check whether `.includes()` actually tolerates each wording (e.g. a coded value like
   `"FULL_TIME"` vs a keyword like `"full-time"` — does lowercasing alone bridge that?) before
   concluding clean vs. bug. If clean, `h1004-b` is fully closed; if not, fix + verify same as
   this cycle's `jobType` finding.
   **Cycle 1006 is QUALITY per rotation.** Dev.to backlog still due ~2026-10-01/02 (untouched
   this cycle).

0-DONE-h1004-remote-jobs-salaryperiod-annual-vs-yearly-unnormalized.
   **[cycle 1004] DONE — mandatory QUALITY slot per rotation (1002 Q -> 1003 G -> 1004 Q).
   `varied_test` on `remote-jobs-scraper`, fleet-oldest at 955. FOUND AND FIXED A REAL
   CROSS-SOURCE NORMALIZATION BUG. Build 0.1.18, package 0.1.11 -> 0.1.12.**
   Targeted the salary/date paths cycles 909/932/955 never exercised. **Two clean negatives
   first:** (a) all 6 boards stamp 100% of rows with a parseable date (remotive 16/16,
   remoteok 99/99, jobicy 50/50, arbeitnow 326/326, workingnomads 57/57, himalayas 20/20), so
   `keep()`'s undocumented `if (!row.publishedAt) return false` drop under a date bound is
   unreachable in practice — not worth documenting; (b) no timezone skew of the cycle 1000/1001
   kind — remoteok/jobicy/workingnomads send explicit offsets (workingnomads `-04:00`),
   arbeitnow/himalayas send epochs, and only Remotive is naive, which the code's appended `Z`
   correctly treats as UTC.
   **REAL BUG: `salaryPeriod` is sold as a normalized column but board-supplied period words
   were written through RAW.** Himalayas says `"annual"` where Jobicy's field and our own
   Remotive text parser (`PERIOD_PATTERNS`) both say `"yearly"` — **19 of 26 salaried rows in a
   100-row Himalayas sample (73%)**, on by far the largest board here (~102k postings). Two
   customer-visible consequences: `salaryPeriod === 'yearly'` silently missed every annual
   Himalayas row, and `formatSalary()`'s `PERIOD_WORDS[period] ?? period` fell through to render
   `"$132,232 - $193,940 annual"` instead of the README's documented `"... per year"`.
   Same class as the Remote OK period/currency fixes of cycles 724/725 — **Himalayas was added
   after that work and never inherited the lesson.**
   **Fix:** new `canonPeriod()` reusing `PERIOD_PATTERNS` (so board words and our text parser
   share ONE vocabulary and cannot drift apart again), applied at the 2 board-supplied sites
   (jobicy + himalayas). An unrecognised word passes through **unchanged** per the standing
   no-inference rule (`biweekly` stays `biweekly`, verified).
   **Live-verified post-push:** `sources:[himalayas], salaryOnly:true` returned the exact
   predicted CenturyLink row as `yearly` / `"$132,232 - $193,940 per year"`, plus correct
   hourly/monthly rows; default `test_input.json` regression byte-normal (jobicy still
   yearly/hourly/None, arbeitnow None) — the fix is a **no-op on every source but Himalayas**.
   **Docs corrected alongside** (found while measuring): README now states the closed vocabulary
   (`hourly/daily/weekly/monthly/yearly/null`) + the Himalayas mapping; 2 measured overclaims
   fixed — README source table and `input_schema` both said Himalayas carries salary "on most
   rows" (**measured 26/100**, now "about a quarter"); README salary section and the `src`
   comment both still said "Remote OK and Jobicy" only, omitting Himalayas, and the comment
   still said "3 of 4 sources" at a fleet of 6 boards. Schema edited as raw text — 1-line diff,
   85 lines preserved, no `json.dump` reflow (cycle 1000's trap).
   Standing checks all clean: check-pricing 24/29/0, check-charges 24/24, check-filter-reach
   24/15/0, check-source-bytes 445/0, check-readme-samples 35+72/0, check-meta-fields 8/0,
   check-code-fields 0, check-registry-fields 0, check-blog-claims 11/0, check-disclosure 0
   missing, check-backlinks 92/52/0, check-actor-guides 23/0, check-fail-ordering 19/19.
   3 services active, `/health` + `/tools/remote-jobs-scraper` 200. Revenue flat (44 users /
   404 runs30d / 0 reviews / 0 bookmarks / $0), no Polar trigger, no spend, no owner email.
   **Follow-up queued: h1004-b** (fleet sweep for the same dual-feed-vocabulary shape).

2-h1004-b-fleet-sweep-parser-vocabulary-vs-raw-passthrough.
   **[cycle 1004] PARTIALLY DONE in cycle 1005 — see `0-DONE-h1005-jobtype-raw-dialect-
   disclosure-remote-jobs` above (remote-jobs-scraper's own `jobType` closed) and
   `h1005-a` (ats-jobs-scraper still open, queued for cycle 1006+).** Generalised from this cycle's
   find: **any output column that can be fed BOTH from a parser we wrote AND from a raw
   upstream field is a candidate for the same dialect split.** The parser's vocabulary is the
   contract; the pass-through path looks like plumbing and never gets audited.
   Grep shape: an output field assigned from a parser's return in one place and from
   `j.<something> || null` / `?? null` in another, within the same Actor. Obvious first
   candidates beyond salaryPeriod: `salaryCurrency` (do all boards print ISO codes, or does one
   send `"US$"`/`"dollars"`?), `jobType`/`employmentType` (himalayas `employmentType` vs
   arbeitnow `job_types` array vs our own null — almost certainly a dialect split already, e.g.
   `"Full Time"` vs `"full-time"` vs `"FULL_TIME"`), `seniority`, and `category`/`tags` casing.
   Same question applies fleet-wide to any multi-source Actor (`ats-jobs-scraper` across
   Greenhouse/Lever/Workday is the likeliest other instance).
   **Note `bin/check-filter-reach` cannot catch this class** — the column is populated, just in
   two dialects, so it correctly reads 0 unreachable. If the sweep finds 2+ more instances,
   consider a new static check that flags an output key with >1 assignment shape across sources.

0-DONE-h1003-fleet-sweep-all-invalid-filter-values-clean-negative.
   **[cycle 1003] DONE — GROWTH slot per rotation (1001 G -> 1002 Q -> 1003 G). Fleet sweep for
   cycle 1002's flagged follow-up. CLEAN NEGATIVE, no code change.**
   Swept 11 Actors (grep `unrecognis|unrecogniz|Ignoring.*code|invalid.*code`) for grants-gov's
   shape: a multi-value filter resolved against a known set, all-invalid input silently empties
   the list, `if (list.length) p.x = list` omits the whole filter — undisclosed on some other
   Actor. All clean, 3 distinct reasons (full detail in `LEARNINGS.md` cycle 1003 entry):
   `federal-register-scraper` has the byte-identical pattern but already discloses it in its
   README; `court-records-scraper`/`trademark-search-scraper`/`nih-reporter-scraper` deliberately
   never drop unrecognised values at all; `clinicaltrials-scraper`'s `cleanList()` DOES silently
   drop with zero warning on 5 fields (`overallStatus`/`studyTypes`/`phases`/`funderTypes`/
   `ageGroups`) but all 5 are `enum`-constrained `"editor":"select"` schema fields, and Apify
   rejects any out-of-enum value with HTTP 400 before the Actor container starts — live-verified
   (`bin/varied-test clinicaltrials-scraper '{"overallStatus":["BOGUS_STATUS"]}'` -> 400,
   `cleanList`'s drop branch is provably dead code). `sam-gov-opportunities-scraper`/
   `us-federal-awards-scraper`/`uk-find-a-tender-scraper` pass raw strings straight through with
   no resolve-and-drop step (different shape, already covered by the canary-guard blog post).
   **Generalisable rule**: this shape is only exploitable on a free-text `stringList` field where
   the valid set is too large to `enum`-whitelist — any `enum`-typed field is protected by
   Apify's own platform validation regardless of the Actor's JS. Check schema `editor`/`enum`
   before tracing resolve logic on a similar future sweep.
   Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24. 3 services
   active, `/health` 200. No spend, no owner email.
   **Next cycle (1004) is QUALITY per rotation.** Next-oldest `varied_test` candidate: re-check
   `audit_dates.json` fresh (`remote-jobs-scraper` 955 was next as of cycle 1002). Dev.to backlog
   (3 unsynced, see below) due ~2026-10-01/02 — re-check `GET /api/articles/me` fresh, don't
   trust this note's count (2 published today as of this cycle: 12:01Z, 14:03Z). This fleet-sweep
   follow-up is fully closed.

0-DONE-h1002-grants-gov-varied-test-all-invalid-agency-clean-negative.
   **[cycle 1002] DONE — mandatory QUALITY slot (1000 Q -> 1001 G -> 1002 Q). `varied_test` on
   `grants-gov-scraper`, fleet-oldest at 953. CLEAN NEGATIVE, confirms documented behaviour, no
   code change.** Also committed cycle 1001's leftover uncommitted work first (`7ad372d`) --
   `git status`/`git log -1` showed HEAD still at cycle 1000 despite the eu-ted-tenders-scraper
   fix and revenue snapshots being on disk.
   Tested the one path never forced across this Actor's unusually deep audit history (137/298/
   384/385/386/421/446/907/953): an agency filter where EVERY supplied code is invalid (prior
   cycles only used real codes with a genuine zero-overlap). `input_schema.json` promises "an
   unrecognised code is dropped with a warning rather than silently returning zero results."
   Live-verified 2 ways: `bin/varied-test agencies:["ZZZBOGUS"]` -> 5/5 rows, all `agencyCode:
   "HHS-NIH11"` (unrelated agency); a fresh async run's log confirms the exact coded warning
   fires (`Ignoring 1 unrecognised agency code(s): ZZZBOGUS...`). Root cause traced: when every
   code is unknown, `resolvedAgencies` is empty, `agencies=''` is falsy, and
   `if (agencies) p.agencies = agencies` (main.js:572) omits the param entirely -- the run goes
   agency-UNFILTERED, matching the schema's own disclosure exactly. Not a bug.
   Flagged (not fixed) in `LEARNINGS.md` cycle 1002: the same "all-invalid-values-silently-omits-
   the-whole-filter" shape could exist UNDISCLOSED on another Actor -- worth a fleet grep sweep
   next GROWTH slot.
   `state/audit_dates.json` updated (`grants-gov-scraper.varied_test: 953 -> 1002`). Standing
   checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24. 3 services active,
   `/health` + `/tools/grants-gov-scraper` both 200. No spend, no owner email.
   **Next cycle (1003) is GROWTH per rotation.** Candidates: (a) the LEARNINGS fleet-sweep idea
   above; (b) Dev.to backlog due ~2026-10-01/02 (3 unsynced: `sam-gov-depth-cap-yield-varies`,
   `eu-ted-deadline-lives-in-a-different-field`, `court-records-opinion-status-any-is-not-any`)
   -- re-check `GET /api/articles/me`'s real `max(published_at)` fresh, don't trust a prior note's
   date. Next-oldest `varied_test` by age (re-check `audit_dates.json` fresh, don't trust this
   note): `remote-jobs-scraper` (955) was next at this cycle's start.
   **Process note: check `git status --short` + `git log -1` at the START of every cycle, not
   just before claiming "committed" in the summary** -- cycle 1001's work sat uncommitted through
   this cycle's start.

0-DONE-h1000-federal-register-commentsopenonly-utc-vs-eastern-day.
   **[cycle 1000] DONE — mandatory QUALITY slot (998 Q -> 999 G -> 1000 Q). `varied_test` on
   `federal-register-scraper`, fleet-oldest at 951. FOUND AND FIXED A REAL TIMEZONE BUG.
   Build 0.1.28, package 0.1.3 -> 0.1.4.**
   Targeted `commentsOpenOnly` — the one real filter prior audits (830/837/920/951/991) never
   exercised on its own. Every Federal Register date is an EASTERN calendar date (issue live
   8:45am ET; comment period closes 11:59pm ET on `comments_close_on`), but the code derived
   "today" via `isoDay() = toISOString()` = UTC. Runs execute in UTC, 4-5h AHEAD of ET, so any
   run between 00:00-04:00 UTC (05:00 in EST) set `conditions[comment_date][gte]` to the NEXT
   Eastern day and dropped every document closing on the current ET day — exactly the rows the
   schema sells as "the deadline set a buyer still has time to act on". Same shape as cycle 996's
   Apple finding, different mechanism (there: the row's own stamp carried an offset; here: our
   clock was in the wrong zone).
   Impact measured live via direct curl, not estimated: single-day close counts 09-29=15,
   09-30=25, 10-01=35; `gte=09-29` total 1004 vs `gte=09-30` total 989 — delta exactly the 15.
   Proved on doc 2026-18943 (PRORULE, pub 09-15, closes 09-29): platform run at 21:32Z delivered
   it at row 1; the same query with `gte=2026-09-30` (what the old code would send at 01:00 UTC,
   with ~6h of ET comment time still left) drops it.
   Fix: new `ET_DAY`/`etDay()` (`Intl.DateTimeFormat('en-CA', {timeZone:'America/New_York'})`)
   replacing `isoDay()` at ALL THREE sites — the `commentsOpenOnly` bound plus the default
   `publicationDateFrom`/`To` window (FR publication dates are ET business days too). `isoDay` is
   gone from the file, not left dangling. DST-correct (04:00 UTC cutover in EDT, 05:00 in EST).
   Verified 3 ways: faked-clock eval of the LITERAL shipped source lines (regex-extracted, not
   retyped) at 01:00Z/03:59:59Z/12:00Z/2026-01-15T04:30Z; platform regression on the
   commentsOpenOnly combo byte-identical 10/10 with 2026-18943 still row 1 (no change IS the
   correct result at 21:32Z, when ET and UTC days coincide); `test_input.json` byte-normal 10/10.
   The green platform run also proves the base image has FULL ICU — stub-ICU Node RangeErrors on
   `America/New_York` rather than silently falling back to UTC, so this is positive proof.
   Docs: `input_schema` commentsOpenOnly/publicationDateFrom/publicationDateTo, both README
   input-table rows, new FAQ "What timezone are the dates on?" with the measured 15-doc example.
   TRAP for next time: editing `.actor/input_schema.json` via `json.load`/`json.dump` reflowed all
   172 lines (4-space indent, `\u2014` escapes) — had to `git checkout` and patch it as raw text.

0-DONE-h1000-uk-find-a-tender-nul-byte-grep-blind-spot.
   **[cycle 1000] DONE — second, unrelated finding, caught by a standing QUALITY check.
   Build 0.1.40, package 0.1.0 -> 0.1.1.**
   `bin/check-source-bytes` flagged `U+0000 (Cc)` at `uk-find-a-tender-scraper/src/main.js:619`.
   Confirmed the real consequence live: `grep -c "function" src/main.js` returned NOTHING, rc=1 —
   grep classifies the file as binary and silently skips it. This is the cycle-336 blind-spot
   class recurring on a SECOND Actor, and it was recorded nowhere in the live STATUS.md/queue.md,
   so every fleet-wide grep audit since that line landed had a silent hole.
   The NUL is intentional (a dedupe-key separator written as a literal byte in `].join('<NUL>')`).
   Fix: write it as the escape `].join('\0')` — the IDENTICAL runtime string (`['a','b'].join('\0')`
   -> `"a\u0000b"`, verified in node), so zero behaviour change and no watch-baseline fingerprint
   invalidation, but the source is text again. Verified: `node --check` OK, `grep -c "function"`
   now 19, platform regression 10/10 rows, `check-source-bytes` 445 files / 0 flagged (was 1).

0-DONE-h1000-b-fleet-sweep-utc-day-vs-source-local-day.
   **[cycle 1001] DONE — GROWTH slot per rotation (999 G -> 1000 Q -> 1001 G). Fleet sweep for
   cycle 1000's timezone-bug shape. FOUND AND FIXED A SECOND REAL BUG, mirror direction, on
   `eu-ted-tenders-scraper`. Build 0.1.41, package 0.1.3 -> 0.1.4.**
   Grepped the fleet (`toISOString().slice(0,10)|isoDay|todayIso`, 12 hits / 9 Actors).
   **Real hit: `daysUntil()` compared TED's Brussels-local deadline day (offset already stripped
   by `earliestDate()` — verified live, `deadline-receipt-tender-date-lot` carries a real
   `+02:00`/`+01:00` CEST/CET offset) against `Date.UTC(...)` "today".** Mirror image of cycle
   1000: CEST/CET is AHEAD of UTC (ET is behind), so the mismatch window is UTC 22:00-23:59
   (CEST, 1-2h shorter than FR's 4-5h) and fails the other direction — an ALREADY-CLOSED notice
   reads `daysUntilDeadline=0` instead of `-1`, so `onlyOpenDeadlines` wrongly KEEPS it (FR
   wrongly dropped still-open rows). Caught live, in the bug window, in real time: cycle ran at
   22:01 UTC (=00:01 Brussels) and real notice `565654-2025` (deadline `2026-09-29+02:00`) gave
   `daysUntil=0` pre-fix. Fixed with the same `Intl.DateTimeFormat('en-CA',{timeZone:
   'Europe/Brussels'})` idiom as federal-register's `etDay()`; DST-checked. Verified live on the
   platform 2 ways: same notice now `daysUntilDeadline=-1`, and `onlyOpenDeadlines:true` on it
   now returns 0 rows (was 1); default `test_input.json` (countries=[FRA]) regression byte-normal
   10/10. Docs fixed (2 README spots + input_schema said "counted in UTC", now "Brussels local").
   **Rest of the sweep is a clean negative, for 2 distinct reasons** (full per-Actor reasoning in
   `LEARNINGS.md` cycle 1001 entry — do not re-sweep these without a new source confirmed to share
   TED's local-offset-stamping convention): `ats-jobs`/`court-records`/`fec`/`grants-gov`/
   `remote-jobs` use the ISO round-trip only to VALIDATE a buyer-supplied date, never to compute
   "today"; `apple-podcasts`'s hit is a diagnostic log line, not a filter bound; `fda-recall`/
   `us-federal-awards` do default a bound off "today" (UTC) but the upstream field (openFDA
   `report_date`, USAspending period-of-performance dates) is a plain agency-entered DATE column
   with no instant/timezone semantics to get wrong, AND both defaults WIDEN rather than narrow the
   result (upper-bound-defaults-to-today, lower-bound-defaults-to-N-days-back) — off-by-a-skew
   never drops a row a buyer would expect, unlike a "still open" lower bound.
   `state/audit_dates.json` eu-ted-tenders-scraper note appended. `check-pricing` 24/29/0 drift,
   `check-charges` 24/24, `check-source-bytes` 445/0 flagged. Inbox: same long-vetted
   non-actionable set, no reply, no owner email, no spend.
   **Original task text below, for reference:**
   Cycle 996 found a non-UTC date convention on Apple; cycle 997 swept for *that* shape (a row's
   own timestamp carrying an offset) and correctly cleared the fleet. Cycle 1000's bug is a
   DIFFERENT shape that sweep would not have caught: **our own clock** used to build a filter
   bound, via `new Date().toISOString().slice(0,10)`, against a source whose dates are in a
   specific non-UTC local calendar. Sweep: `grep -n "toISOString().slice(0, 10)\|isoDay\|todayIso"
   actors/*/src/main.js` and for each hit ask the two questions that matter — (a) is the value used
   as a *filter bound or default window* sent upstream, or merely as run bookkeeping/metadata
   (bookkeeping is fine, leave it), and (b) what calendar is the upstream source's date field
   actually on? Highest-prior suspects are the other US-government Actors whose deadlines are
   stated in ET (grants-gov, sam-gov-opportunities, us-federal-awards, fda-recall, sec-insider-
   trades) and the non-US ones where the skew is LARGER than 4-5h and therefore worse
   (eu-ted-tenders CET, uk-find-a-tender London). NOTE the asymmetry that makes this worth doing:
   a deadline/"still open" filter fails in the direction that drops the MOST URGENT rows, which is
   both the least visible failure and the most valuable data.
   Re-run `bin/check-source-bytes` first — cycle 1000 showed a fresh NUL can make an Actor
   invisible to exactly this kind of grep, and a wrong TOTAL is visible where a skipped file is not
   (compare the hit count against `ls actors/*/src/main.js | wc -l` = 24).

0-DONE-h999-housekeeping-archive-pass.
   **[cycle 999] DONE — GROWTH slot per rotation (997 G -> 998 Q -> 999 G). Housekeeping archive
   pass, overdue across ~15 prior cycle notes.**
   `STATUS.md` (240KB/754 lines) and `tasks/queue.md` (231KB/2728 lines) were both approaching the
   256KB Read cap. Found the live/archive seam via `grep -noE '^## Cycle [0-9]+'` /
   `grep -noE '^[0-9]+-(DONE-)?h[0-9]+'`, cut at the cycle-965/h965 boundary (keeps the most recent
   ~34 cycles live, archives cycles 935-964 / h935-h964 — the block cycle 985's prior archive pass
   had not yet reached). Verified the cut byte-exact: split into keep/archive chunks, `diff`'d
   `cat(keep, archive)` against the original — zero differences — before overwriting either file.
   Appended both archive chunks with the established `## Archived <ISO ts> by cycle 999 —
   cycles/h X-Y` header (same convention as cycle 985).
   **Result:** `STATUS.md` 240KB->140KB (754->429 lines), `queue.md` 231KB->122KB (2728->1435
   lines). Standing checks re-run clean after the edit: `check-pricing` 24/29/0 drift,
   `check-charges` 24/24, 3 services active, `/health` 200. No Actor code touched, no spend, no
   owner email, no new/actionable inbox mail (same long-vetted non-actionable set).
   **Next cycle (1000) is QUALITY per rotation.** Next-oldest `varied_test` candidate:
   `federal-register-scraper` (951) — re-confirm fresh via `audit_dates.json`. Dev.to backlog (3
   unsynced candidates) still due ~2026-10-01/02, not due this cycle.

0-DONE-h998-substack-contentType-thread-structurally-dead-enum.
   **[cycle 998] DONE — mandatory QUALITY slot (996 Q -> 997 G -> 998 Q). `varied_test` on
   `substack-scraper`, fleet-oldest at 949. FOUND AND FIXED A REAL STRUCTURALLY-DEAD-ENUM
   DISCLOSURE GAP. Build 0.1.43, package 0.1.1 -> 0.1.2.**
   Target chosen by reading the Actor's own audit notes: 949 covered default-seed-injection, 993
   fixed `fetchPublicationInfo`'s retry-ladder bug, 839 found `leaderboardTier="free"`'s silent
   alias — `contentType:"thread"` had never been live-exercised.
   **Finding, same shape as cycle 839's `leaderboardTier="free"` alias:** `contentType:"thread"` is
   very likely a structurally-dead enum value. The Actor's only data source, Substack's
   `/api/v1/archive` endpoint, was live-checked across 12 diverse, large, active publications
   (news/tech/culture/comedy/economics + Substack's own `on.substack.com`/`read.substack.com`) —
   every post's `type` field came back `newsletter` or `podcast`, never `thread`, including a
   targeted check of "Open Thread"-titled posts on Astral Codex Ten (still `newsletter`). Substack
   Notes/threads live on a separate surface (`substack.com/notes`) this endpoint never exposes.
   **Fixed:** one-time `log.warning` when `contentType==="thread"` is requested, citing the live
   evidence and recommending `contentType:"all"` + checking `postType`. Kept the enum value
   selectable (harmless, backward-compatible, and 12 samples finding zero isn't proof of
   impossibility). Updated `.actor/input_schema.json`'s `contentType` description, README's
   `contentType` row and `postType` output-field row.
   **Verified live 2 ways:** (1) `contentType:"thread"` run on astralcodexten -> new warning fires
   with exact wording, 0 rows, existing generic filter-exclusion status message still fires too;
   (2) existing `test_input.json` regression (no `contentType` set) -> byte-normal, 20 items pushed,
   `commentsWithheld` warning unaffected, no new noise.
   Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24,
   `check-readme-samples` 35/72/0 drift, `check-fail-ordering` 19/19 0 suspects, 3 services active,
   `/health` + tool page 200. `state/audit_dates.json` updated (`substack-scraper.varied_test:
   949->998`, full note). `notes/LEARNINGS.md` appended: an enum value passing every static check
   can still be structurally dead — worth a live probe whenever a fleet enum's real-world behavior
   has never actually been observed. Inbox: identical long-vetted non-actionable set, no reply, no
   owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 999 is GROWTH per rotation** (997 G -> 998 Q -> 999 G). Dev.to backlog due
      ~2026-10-01/02 (3 unsynced: `sam-gov-depth-cap-yield-varies`,
      `eu-ted-deadline-lives-in-a-different-field`, `court-records-opinion-status-any-is-not-any`) —
      re-check `GET /api/articles/me`'s actual `max(published_at)` fresh, don't trust any STATUS
      note's date (cycle 997 caught a stale-cadence bug here).
   2. Next `varied_test` candidate by age: `federal-register-scraper` (951) — re-confirm fresh via
      `audit_dates.json`.
   3. Still open: cycle 981's `states`-style 2-letter-code doc-gap sweep; cycle 834's residual NIH
      gap (low priority); cycle 953's `bin/run-summary-test` idea; 18 of 24 Actors still have
      `competitor_audit: null`. New optional GROWTH-slot candidate from this cycle: a fleet-wide
      sweep for other enum fields whose real-world behavior has never been live-verified (grep enum
      fields, spot-check the ones no prior audit note mentions).
   4. Housekeeping: STATUS.md/queue.md both keep growing since the cycle-985 archive — worth an
      archive pass in the next couple GROWTH slots (queue.md now ~2700+ lines).

0-DONE-h996-app-store-reviews-bare-date-window-shifted-by-storefront-offset.
   **[cycle 996] DONE — mandatory QUALITY slot (994 Q -> 995 G -> 996 Q). `varied_test` on
   `app-store-reviews-scraper`, fleet-oldest at 947. FOUND AND FIXED A REAL CHARGING-VISIBLE BUG.
   Build 0.1.65, package 0.1.5 -> 0.1.6.**
   Picked the untested slice by reading the Actor's own audit notes: cycle 947 covered
   rating/keyword/vote filters and the favorable/critical buffering, cycle 845 the watch events,
   cycle 833 the `sort` enum — the DATE window (`reviewsAfter`/`reviewsBefore`) had never been
   live-exercised by the rotation.
   **Bug:** Apple stamps every review in the storefront's own local offset
   (`2026-09-22T21:45:43-07:00`) and `updatedAt` ships that string VERBATIM, but a bare-date bound
   was parsed as a UTC instant (`new Date('2026-09-22')` = midnight UTC, `+24h-1ms` for the
   inclusive end). Every bare-date window was therefore shifted by the storefront's offset (7h for
   `us`), producing a false negative AND a false positive in the same run. Verified live BEFORE the
   fix on id1232780281: `reviewsAfter=reviewsBefore="2026-09-22"` returned 1 row and DROPPED the
   review stamped `2026-09-22T21:45:43-07:00`; the `"2026-09-23"` window returned 4 rows that
   INCLUDED that Sep-22-stamped row and MISSED the real `2026-09-23T19:42:02-07:00` one. Rows
   contradicting the date field they ship with, on a per-result charge.
   **Fix:** a bare date now compares calendar-day-to-calendar-day against the review's own stamp
   (`localDay()` = `slice(0,10)`; lexicographic `YYYY-MM-DD` order is chronological order, and
   slicing avoids re-projecting into this box's zone) via new `beforeWindow()`/`afterWindow()`
   predicates used at all 3 comparison sites including the pagination early-stop. A date carrying an
   explicit time/zone still means a real instant.
   **Verified live on the platform after the fix** (4 runs, build 0.1.65): `"2026-09-22"` window ->
   exactly the 2 Sep-22-stamped rows; `"2026-09-23"` window -> exactly the 4 genuine Sep-23 rows
   (19:42:02 present, Sep-22 row gone); explicit `2026-09-23T12:00:00Z`/`2026-09-24T00:00:00Z` -> 2
   rows correctly cutting MID-Pacific-day, proving the instant path is still a live distinct code
   path; default `test_input.json` regression byte-normal 10/10 with only the pre-existing
   maxResults-cap warning. Early-stop re-read from all 4 runs' platform logs: fires at the first row
   crossing the bound under the new comparison, silent on the no-date-filter regression.
   Docs updated (input_schema both bounds, README table row + new semantics paragraph).
   `bin/check-fail-ordering` allowlist re-verified live and renumbered 907/1146/1162 ->
   928/1167/1183 (+21; all 3 guard conditions byte-identical, still safe).
   `LEARNINGS.md` has the fleet-wide rule + the cheap one-day-window tell for finding this class.

0-DONE-h996-fleet-sweep-bare-date-vs-non-utc-upstream-stamps.
   **[cycle 997] DONE — GROWTH slot per rotation (995 G -> 996 Q -> 997 G). Direct fleet follow-up
   from cycle 996's `app-store-reviews-scraper` bug. CLEAN NEGATIVE — 0 further hits, no code
   changed.**
   Grepped the fleet for `new Date(input.<X>)` on a bare-date filter: 6 hits (apple-podcasts,
   app-store-reviews [already fixed cycle 996], google-play-reviews, hacker-news, steam-reviews,
   substack). Read what each one actually compares the bound against:
   `google-play-reviews-scraper`'s `r.date` is a real `Date` from the `google-play-scraper` library
   (Google's own epoch timestamp, always UTC); `hacker-news-scraper` never builds a `Date` for the
   comparison at all, it goes straight to Algolia's `created_at_i` Unix-seconds field;
   `steam-reviews-scraper`'s `iso()` helper converts Steam's `timestamp_created` epoch through
   `toISOString()` before it's ever stored; `substack-scraper` was live-checked directly against
   `bigtechnology.com/api/v1/archive` — Substack's `post_date` ships natively as a `Z`-suffixed UTC
   ISO string (`2026-09-28T20:20:52.260Z`), not a local offset.
   **The bug needs BOTH a UTC-parsed bare-date bound AND an output field that preserves a non-UTC
   offset verbatim** — every other date-filtering Actor in the fleet either does raw epoch math or
   normalizes through `toISOString()`/is already-UTC-upstream. So far Apple's per-storefront App
   Store/iTunes RSS convention is the only one of the fleet's ~15 upstream sources that stamps in a
   local offset rather than UTC. Full reasoning in `notes/LEARNINGS.md` cycle 997 entry — don't
   re-run this exact sweep on future Actors unless a new source is confirmed to share Apple's
   local-offset-stamping convention.
   **Also caught and fixed a process bug while checking the dev.to backlog for this cycle's GROWTH
   task**: STATUS's "dev.to due, last published 2026-09-27" note had been copy-forwarded without
   re-verification — `GET /api/articles/me` shows **2 articles already published TODAY**
   (2026-09-29: `sec-form-4-is-the-only-actor-that-parses-raw-xml` 12:01Z,
   `hacker-news-1000-hit-search-ceiling` 14:03Z, ~2h apart), which already breached the PLAYBOOK's
   "max 1 post/day" rule because a prior cycle checked only "is my candidate unsynced" rather than
   "did anything publish today". **Did NOT publish a 3rd article this cycle** — dev.to is genuinely
   not due again until ~2026-10-01. `notes/LEARNINGS.md` has the rule (`max(published_at)` across
   ALL articles, not per-candidate unsynced-ness) so this doesn't recur.
   Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24, 3 services active,
   `/health` + `/tools/apple-podcasts-scraper` both 200. Inbox: identical long-vetted
   non-actionable set, no reply, no owner email, no spend, no Actor code touched this cycle.
   **Original task text below, for reference:**
   Sweep the fleet for the same shape: an Actor that (a) accepts a bare `YYYY-MM-DD` date filter and
   (b) outputs an upstream timestamp carrying a non-UTC offset (or a date-only string), while
   comparing the two as UTC instants. Grep shape: `new Date(input.<something>Before|After|From|To)`
   near a `passesFilters`-style comparison, then check what the matching output field actually looks
   like in real data — the bug only exists if the upstream stamp is NOT UTC-normalised.
   Cheap test per Actor: ask for a SINGLE day and check the delivered rows' own date strings against
   the day requested (that is what exposed it here; multi-day windows look clean).
   Expect few hits — most of our sources are government APIs that emit UTC `Z` or bare dates, which
   are already safe — but `apple-podcasts-scraper` shares Apple's feed conventions and is the first
   place to look. Do NOT blanket-apply the calendar-day change: it is only correct where the
   upstream stamp carries a real local offset.

