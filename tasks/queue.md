- [x] **DONE cycle 2287 (NOT a QUALITY slot -- `2287%3==1`) -- ran a fresh `bin/check-store-rank`
      sweep and confirmed it is fully exhausted again: the near-miss list (rank 25-60) came
      back with exactly the same 8 Actors as c2279/c2280's original list (minus the 3 already
      closed: website-screenshot/`url to pdf`, google-play/`android app reviews`, `jobicy`),
      and every one of the 8 (`court-records-scraper` #29, `apple-podcasts-scraper` #31,
      `sec-insider-trades-scraper` #33, `shopify-products-scraper` #34,
      `uk-find-a-tender-scraper` #46, `remote-jobs-scraper` #53, `fda-recall-scraper` #55,
      `eu-ted-tenders-scraper` #56) was already triaged and closed as NOT copy-closable
      (storePosition-gated / already-optimal bucket, c2280/c2283/c2285) or already rejected
      on trade-off grounds (`podcast charts`, c2282). No edit made, no new growth lever found.
      **Flagged one easy misread for later cycles:** this REST/CLI sweep now shows
      `website-screenshot-scraper`/`url to pdf` at #23 ("PAGE 1") -- this is NOT the buyer-
      facing number (that's `store-price`/Algolia, confirmed **p25** and storePosition-gated
      at c2285) and should not be treated as a fresh opportunity. **Do not re-run
      `check-store-rank` on a bare time interval -- it will just reproduce this same exhausted
      8-item list until a new title/description edit ships elsewhere in the fleet to create
      fresh REST-surface near-misses worth checking.**
      $0 spent (read-only Algolia/REST queries only), 0 new Actors, revenue still $0 booked
      (`bkmk`/`rev` 0/0, `users` 47, unchanged), no owner email warranted. Re-verified fresh
      first: `bin/checks-due`/`bin/audit-due --all`/`--type varied_test --all` all NONE DUE
      (soonest `check-row-floor` in 5c, cycle 2292); inbox unchanged (same 10 known items,
      newest still `c2fa5a9c`; owner thread `dc593cfb` re-confirmed resolved); services active;
      site 200 on `/` `/tools` `/pricing`; `HEAD == origin/main` (`42089e27`) and tree clean
      before edits. 0 Actors created today. All 5 open follow-ups (c2276/c2272/c2196/c2168-
      c2268/c2103) re-confirmed still correctly blocked, not re-litigated.**

- [x] **DONE cycle 2286 (QUALITY/GROWTH slot -- `2286%3==0`) -- ad-hoc competitor
      README/feature diff on `court-records-scraper` (our highest-demand niche, never
      checked this way before), found NO gap -- a useful negative result, not a dead cycle.**
      Pulled the top Store rival by users (`automation-lab/court-records-scraper`, 78
      users) via `bin/apify-admin store "court records" 15` and its live description via
      the public Apify API: a one-line pitch, 400+ courts, no field/pricing detail. Our own
      `actors/court-records-scraper/README.md` already names and prices this exact rival
      (line 172) among 100+ CourtListener-niche competitors swept live across a dozen+ dated
      passes (2026-09-17..2026-10-25), and already covers 3,359 courts vs. their 400+, both
      dockets+opinions (41 fields) in one schema, watch-mode with termination detection,
      `startUrl` paste-in, and a candid pricing-undercutters section. **No edit made -- this
      README's competitive depth is already far beyond what an ad-hoc cycle could add.**
      Confirms the fleet's best-demand Actor has no low-hanging README work left; next
      QUALITY cycle doing this method should pick a different, less-visited Actor (e.g.
      `fda-recall-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper` --
      none of which have had a README-level, not just Store-title, competitor diff yet).
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/`--type varied_test
      --all` all NONE DUE (soonest `check-row-floor` in 6c, cycle 2292); inbox unchanged
      (same 10 known items, newest still `c2fa5a9c`); services active; site 200 on `/`
      `/tools` `/pricing`; `HEAD == origin/main` (`75a02570`) and tree clean before edits.
      0 Actors created today; `state/health.json` all 24 Actors `ok:true`. All 5 open
      follow-ups below (c2276/c2272/c2196/c2168/c2103) re-confirmed still correctly blocked.
      $0 spent (read-only API calls only), 0 new Actors, revenue still $0 booked
      (`bkmk`/`rev` 0/0, `users` 47, unchanged), no owner email warranted.

- [x] **DONE cycle 2284 (NOT a QUALITY slot -- `2284%3==1`) -- closed the c2280
      `website-screenshot-scraper` VERIFY item below, and found its core diagnosis was
      wrong.** It was never blocked on "Apify's Algolia batch schedule": the Store search
      index is **BUILD-GATED**. `bin/check-store-index` shows `idx` == latest build
      `finishedAt` **exactly for all 25 Actors**, and we were the only stale listing in the
      fleet because c2280's metadata-only publish was never followed by a build (PLAYBOOK
      line 85 requires `apify push --force` right after one; rule dates to cycle 515).
      Force-pushed (build **0.1.30**, 15:31:44) -> index refreshed **~3 min later**, fleet
      to **0 stale fields**. Measured the prize post-reindex and **the edit did not deliver
      it**: `url to pdf` (1184 hits) p34 -> **p25** (predicted p23 -- real 9-slot gain but
      **one slot short of page 1**, which is top 24); `jpeg screenshot` p25 -> **p26** (wrong
      way by 1, predicted p24); `screenshot png` p112 -> **p192** (regression was accepted
      but cost 80 slots, not the ~0 implied); `screenshot scraper` **p6** held exactly.
      c2280's "bare `screenshot` holds at p6" was a transcription slip (that is the
      `screenshot scraper` number) -- bare `screenshot` is live **p307** and our edit cannot
      have moved it, the token is in both titles twice. **Probable cause of the 2-slot
      misses: `storePosition` drifted 93256 -> 94979 (+1723) since the simulation.**
      Deliberately NOT reverting: both titles leave every query off page 1, the new one wins
      the biggest query, and a revert costs a build + reindex wait for no page-1 slot.
      **Shipped the guard** (rule now violated twice => missing guard, not missing reminder):
      `apify-admin publish` records `state/pending_reindex.json` + prints a `!! REINDEX
      REQUIRED` block (silent on categories/pricing-only publishes); `bin/audit-due` prints
      a `PENDING REINDEX` footer **every cycle** (offline -- `check-store-index`'s own
      672-cycle cadence is far too slow for copy published this cycle); `bin/check-store-index`
      is the only clearer, and only on an observed in-sync comparison for slugs it checked
      (a finished build is NOT accepted as proof -- the 15:31 build read `idx=10-25 18:33`
      for minutes after). Both branches verified live. `fleet_checks.json` 1621 -> 2284.
      $0 beyond one ~$0.005 build, 0 new Actors, $0 revenue, no owner email warranted.

- [x] **DONE cycle 2285 (NOT a QUALITY slot -- `2285%3==2`) -- closed both c2284 follow-ups
      with read-only re-measurement, no builds, no code changes.**
      **(1) `url to pdf`: CLOSED as not-text-fixable, joining the 7-case list.**
      `bin/store-price website-screenshot-scraper "url to pdf"` now returns **`pred == live
      == p25`** (previously `pred p23` vs `live p25` at c2284) -- the simulator and reality
      now agree because our title already sits in the best-achievable bucket. `--why` confirms:
      we are **#25 of 26** records tied in bucket `(words=3,exact=3,prox=2,attr=0/title)`,
      ranked purely by `storePosition` (ours **94979**, unchanged from c2284 -- no drift in
      ~1h); rank 24 (`weio/website-to-pdf-bulk`) sits at `storePosition=94390`, 589 lower.
      Closing the page-1 gap needs beating that one competitor's `storePosition` (distinct
      users, cycle 1608 lever) -- no title edit reaches inside a 26-way tie. `jpeg screenshot`
      held **p26** (unchanged); its `pred=p1`/`tgtN=0` is the same tool artifact as the
      c2283 `jobicy` case (nonsense prediction when `tgtN=0`), not a real lever -- do not chase.
      `screenshot png` held **p192** (unchanged, the accepted regression); `screenshot scraper`
      held **p6** exactly (`pred==live`). **Folding `url to pdf` into the "NOT copy-closable,
      storePosition-gated" list started at c2280/c2283 -- do not re-shop this title again.**
      **(2) Audited the other `store-price`-predicted wins: all held, no regressions.**
      `google-play-reviews-scraper` `android app reviews` -- live **p17**, unchanged, confirms
      the c2282 win is holding. Its companion queries also fine: `play store scraper` p69,
      `google play store scraper` p64 (improved further from c2281's p131), `play store` p111
      -- all normal pool-drift noise, no action needed. `eu-ted-tenders-scraper` (cycle-1846
      SEO wins): `tender tracking` live **p1** (holds exactly); `tender monitoring` live **p9**
      (was p7, still page 1); `bids and tenders` live **p9** (was p7, still page 1) -- both a
      2-slot drift but nowhere near falling off page 1, not a regression worth acting on;
      `ted tenders` live p86, matches `pred` exactly (already-known not-closable case, holds).
      **No new follow-up left from this thread -- both items are now fully resolved.**
      $0 spent (read-only Algolia queries only), 0 new Actors, revenue still $0 booked
      (`bkmk`/`rev` 0/0 across 25 Actors, `runs30d` 749), no owner email warranted.
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/`--type varied_test
      --all` all NONE DUE (soonest `check-row-floor` in 7c, cycle 2292); inbox unchanged
      (same 10 known spam/DMARC/resolved items, newest still `c2fa5a9c`); services active;
      site 200 on `/` `/tools` `/pricing`; `HEAD == origin/main` (`26da9f17`) and tree clean
      before edits. 0 Actors created today.

- [x] **DONE cycle 2283 (QUALITY/GROWTH slot -- `2283%3==0`) -- closed the long-open
      `remote-jobs-scraper`/`jobicy` UNRESOLVED item from c2279/c2280.** Ran
      `bin/store-rank --why "jobicy" remote-jobs-scraper` with `depth=162` (full hit set;
      the CLI caps at 60, called the Python `why()` function directly for the rest).
      Mystery resolved: we DO sit in the best bucket (`attr=0`/title, `exact=0`, `prox=0`)
      -- same bucket as all 61 records ahead of us, including the ones literally named
      `jobicy-*` -- so `exact=0` is just how Algolia reports every hit on this query, not
      a sign our title under-matches. We're last in that 62-record bucket at live **p61**,
      `storePosition=90706` (2nd-worst in the bucket). `store-price`'s `pred=p1` was
      flat-out wrong: its simulator finds the best reachable bucket but never counts how
      many competitors already tie inside it by `storePosition`, so it silently assumes
      "best bucket" == "rank 1 in it" -- false whenever the bucket is large (here, 62-way).
      **No title edit can move this ranking; the only lever is `storePosition` (distinct
      users), identical to the 6 already-closed c2280 cases.** No code changed, no commit
      for this thread. Added the general rule to LEARNINGS.md: never trust a `store-price`
      `pred` without a `--why` cross-check when the predicted bucket looks large/crowded.
      Also re-checked `website-screenshot-scraper`'s Algolia record (`--meta`): still
      stale, `modifiedAt` unchanged (`1792953186`, ~21h old) -- stays open below, no new
      info this cycle.
      $0 spent, 0 new Actors, revenue still $0 booked, no owner email warranted.

- [x] **DONE cycle 2282 (NOT a QUALITY slot -- `2282%3==2`) -- re-measured both open Algolia
      verify items via `bin/store-rank --meta <slug>`. `google-play-reviews-scraper`:
      CONFIRMED, `android app reviews` now live p17 (404 hits), exactly matching c2281's
      prediction -- real page-1 win, closed. `website-screenshot-scraper`: STILL STALE,
      `modifiedAt` unchanged (`1792953186`, ~20h old) even though google-play's record
      reindexed in the same window -- confirms the batch lag is per-record, not a global
      outage. Stays open below, re-check `--meta` only (not full rank) until the title
      string itself changes.
      Also investigated the queued `apple-podcasts-scraper`/`podcast charts` pickup and
      found it NOT closable: every title candidate that wins `podcast charts` (105 hits,
      p34->p23) costs the cycle-548 deliberate `podcast publishers` p1 (328 hits) -- shopped
      3 candidates with `store-price --title`, all regress that p1 to either no-match or
      p18. Rejected all; no file touched, no commit. See STATUS.md c2282 for the full
      3-candidate trade-off writeup -- do not re-shop the same candidates again.
      $0 spent, 0 new Actors, revenue still $0 booked, no owner email warranted.

- [x] **CLOSED cycle 2284 -- see the c2284 entry at the top of this file for the measured
      outcome (`url to pdf` p34 -> p25, one slot short of page 1; `jpeg screenshot` moved the
      wrong way; the guard that now prevents a repeat). READ THE CORRECTION BELOW BEFORE
      TRUSTING ANY PART OF THIS ITEM: the "blocked on Apify's batch schedule" premise was
      FALSE. The Store index is build-gated (`idx` == latest build `finishedAt`, exactly, for
      all 25 Actors); the record was stale only because this publish was never followed by a
      build. One `apify push --force` fixed it in ~3 min. The `screenshot` p6 figure below is
      also a transcription slip for `screenshot scraper`; bare `screenshot` is p307.**
      Original (now-corrected) text follows.
      ~~NEW follow-up (c2280) -- VERIFY the shipped `website-screenshot-scraper` title win.
      Blocked on Apify's Algolia record refresh, NOT on anything we do (re-confirmed stale
      again at cycle 2282, ~20h with no reindex).~~ c2280 published
      title `Website Screenshot Scraper – Screenshot API, JPEG, URL to PDF` (61/63; was
      `... Screenshot API, JPEG, PNG & PDF`). Live on the REST record within seconds
      (verified `GET /v2/acts/fetchsmith~website-screenshot-scraper` -> new title, 61 chars)
      but the **Store Algolia record was still serving the OLD title ~7 min later** --
      retrieved the record directly and its `modifiedAt` was `1792953186` =
      **2026-10-25T18:33Z, ~19h stale**, while the REST `modifiedAt` was the publish itself
      (2026-10-26T13:33:20Z). So the buyer-facing index refreshes our record on a BATCH
      schedule (~daily here), not on publish. Do not conclude the edit failed.
      **How to verify:** re-retrieve the Algolia record's `title`+`modifiedAt` first (the
      inline 12-line snippet is in c2280's STATUS entry; `APP=OW0O5I3QO7`,
      `KEY=0ecccd09f50396a4dbbe5dbfb17f4525`, `IDX=prod_PUBLIC_STORE`, query the slug).
      Only once `title` shows the NEW string, re-measure and record:
        * `url to pdf` (1181 hits) -- live **p34** (attr=2/description), predicted **p23**
          (joins the 25-record attr=0/prox=2 title block, inserting by storePosition 93256
          between p22=81105 and p23=93757). p23 is PAGE 1 (top 24). This is the prize.
        * `jpeg screenshot` (320 hits) -- live **p25**, predicted **p24** (prox 3->2). Also
          crosses onto page 1.
        * Accepted regression, do NOT treat as a surprise: `screenshot png` (366 hits) live
          p112 loses its weak prox=3 title match and falls to the description bucket. p112
          is page 5; traded deliberately for the two gains above.
        * Held byte-identical in simulation and must still hold: `screenshot scraper` p6,
          `screenshot` p6, `screenshot api` p89, `website screenshot` (deep, 200-record
          bucket, tool prints `-`).
      `check-store-meta` (0 drift) and `check-meta-fields` (0 stale) both clean after;
      `registry.json`/`.actor/actor.json` auto-mirrored by `apify-admin publish`; site
      `/tools/website-screenshot-scraper` renders the new title, all 4 pages 200.

- [x] **DONE cycle 2281 (NOT a QUALITY slot -- `2281%3==1`) -- shipped the
      `google-play-reviews-scraper` reword, half of this item.** New title
      `Google Play & Play Store Scraper – Android App Reviews, Dates` (61/63). Shopped 3
      candidates with `bin/store-price --title` (2 rejected for regressing
      `play store scraper`/`google play store scraper`); the shipped one gains
      `android app reviews` (405 hits) p31 -> predicted **p17** (page 1), holds `play store`
      p101 and `play store scraper` p63, and actually IMPROVES `google play store scraper`
      p136 -> p131 -- no regressions on ~15 queries tested. Published via `apify-admin
      publish` + `apify push --force` (forces the Algolia reindex a metadata-only publish
      skips -- the exact gap c2280 hit). `check-store-meta`/`check-meta-fields` clean, live
      `<title>` on `/tools/google-play-reviews-scraper` confirmed. Commit `dce7e00c`.
      **Still open: re-measure `android app reviews` once the Algolia record's own title
      shows the new string (same batch-lag caveat as the website-screenshot-scraper item
      above -- check `modifiedAt` first, don't trust a same-day re-measure).**
      `apple-podcasts-scraper` / `podcast charts` (105 hits) still NOT done: live **p34**
      (attr=2), contiguous title predicts **p23**. Lower value (105 hits, thin demand) --
      pick this up next, same `--title` shopping method (title is
      `Apple Podcasts Scraper – Charts, Episodes, Transcripts` or similar, check current
      length/room before proposing a candidate).

- [x] **DONE cycle 2280 (QUALITY/GROWTH slot -- `2280%3==0`, verified `python3 -c
      "print(2280%3)"`) -- triaged ALL 10 of c2279's near-miss Store ranks on the
      BUYER-FACING surface and shipped the one clear win. Headline: 6 of the 10 are NOT
      copy-closable at all, so the tool's own "a listing-copy change could reach page 1"
      line was wrong about most of them.**
      c2279's list came from `bin/check-store-rank`, whose own docstring (cycle-518
      correction) says it measures the **REST/CLI** surface, not what a visitor on
      apify.com/store sees. Re-measured every pair on the Algolia index via
      `bin/store-price <slug> "<query>"` (live rank + `liveBucket` + the rank a contiguous
      title match would get). **Reading rule: when `liveBucket` is already
      `(n, n, n-1, 0)` -- ideal proximity, attr=0/title -- the Actor is ALREADY at its best
      achievable text position and `pred == live`; the only remaining lever is
      `storePosition`, i.e. distinct first-time users (cycle 1608), which no copy edit
      moves.** Full triage, buyer-facing:
        * `website-screenshot-scraper` `url to pdf` 1181 hits: p34 attr=2 -> pred p23.
          **CLOSABLE -- SHIPPED this cycle** (see verify item above).
        * `google-play-reviews-scraper` `android app reviews` 405: p31 attr=2 -> pred p17.
          **CLOSABLE, best remaining** (see item above).
        * `apple-podcasts-scraper` `podcast charts` 105: p34 attr=2 -> pred p23. CLOSABLE,
          thin demand.
        * `remote-jobs-scraper` `jobicy` 162: p60, bucket `(1, 0, 0, 0)` -- attr=0 but
          **`nbExactWords=0`** though the title literally reads "Jobicy". `tgtN=0` so the
          tool predicts p1, which cannot be right when 59 records outrank us on a 162-hit
          query. Treat the p1 as a tool artifact, NOT a lever; needs a `--why "jobicy"`
          read to explain the exact=0 before anyone touches that title. UNRESOLVED.
        * NOT copy-closable, all six already `(n, n, n-1, 0)` with `pred == live`, gated
          purely on `storePosition`: `court-records-scraper` `court records` (9919 hits,
          p30, sp=90924 vs 29 better-positioned title-matchers), `sec-insider-trades-scraper`
          `form 4 insider` (328, p42), `shopify-products-scraper` `shopify products`
          (1888, p47), `fda-recall-scraper` `fda recalls` (307, p66),
          `uk-find-a-tender-scraper` `find a tender` (1789, p69),
          `eu-ted-tenders-scraper` `ted tenders` (492, p85). **Do not re-litigate these
          six from the REST near-miss list again** -- re-measure only if `storePosition`
          moves materially.
      Also: a local "is the query contiguous in the title?" string heuristic was tried
      first and MISREAD 3 of 10 (`find a tender` and `fda recalls` scored as misses when
      the title does carry them; `jobicy` scored as a clean contig match when the index
      says exact=0). Don't substitute string matching for `bin/store-price` -- prefix
      rules, stopwords and tokenization all differ from intuition.
      Re-verified fresh before any edit: `bin/checks-due`/`bin/audit-due --all`/`--type
      varied_test --all` all NONE DUE (soonest `check-status-continuity` in 1c, cycle
      2281); inbox unchanged (same 10 known items, newest DMARC still `e2f3a358`, c2103's
      trigger still unfired); `fetchsmith-web`/`fetchsmith-mail`/`caddy` active; `/`
      `/tools` `/pricing` all 200; `HEAD == origin/main` (`14dcc477`) and tree clean apart
      from routine `state/revenue.json`/`revenue_history.json`. Cost $0 -- metadata
      publish only, no `apify push`, no build.

- [x] **DONE cycle 2279 (NOT a QUALITY slot -- `2279%3==2`) -- ran 10 ad-hoc check-* tools
      never run by c2277's sweep, found and fixed a real `check-fail-ordering` stale-key
      re-flag, confirmed 2 `check-change-blind` WEAK hits as already-understood junk, and
      surfaced the `check-store-rank` near-miss lead above.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/`--type varied_test
      --all` all NONE DUE, inbox unchanged (same 10 known items, newest DMARC still
      `e2f3a358`), services active, site 200, `HEAD == origin/main` (`2889bf66`), tree
      clean before edits. 0 Actors created today. All 3 open follow-ups below
      (c2276/c2272/c2196) re-confirmed still correctly blocked.
      **The fix:** `check-fail-ordering` re-flagged `apple-podcasts-scraper`'s known h289
      seed-gate false positive (line 1319 stale -> 1347, +28 lines from cycles 2172-2278's
      work above it) -- this is the SAME allowlisted invariant re-verified at cycles
      1034/1276/1416/1564/1909/1982/2172, each time re-surfacing because the allowlist key
      is deliberately line-keyed (a moved call must be re-read, not auto-trusted). Re-traced
      the full charge-reachability chain fresh at the new line numbers (not just re-read the
      guard text): sole `Actor.charge(` at line 387 inside `pushResult` (8 call sites);
      all 3 `seedErrors.push(` gated `if (seeding)`; `seeding` only set true inside
      `if (watchMode)` (line 293); `watchLabel` (line 221) still implies
      `dataType === 'episodes'` under `watchMode`, ruling out every `pushResult` site except
      the episode loop's 780/784, where line 773's `if (seeding) {...continue;}` precedes
      780. Invariant holds -- a seed run's charge count is still provably 0. Updated
      `bin/check-fail-ordering`'s allowlist key `1319 -> 1347` with the re-verification
      appended. Verified: `0 suspect`, `ast.parse` syntax-clean.
      **Two WEAK `check-change-blind` hits, both confirmed junk:** `nih-reporter-scraper`
      `projectEndDate`~`projectNums` is literally the tool's own documented WEAK-tier junk
      example. `hacker-news-scraper` `numComments`~`maxCommentDepth` checked fresh:
      `maxCommentDepth` filters per-comment nesting depth (`src/main.js:605`), unrelated to
      the story-level `numComments` the watch snapshots (`snapshotOf()` line 256) -- shared
      substring only, no real change-blind filter. No fix needed either place.
      **Growth lead found, not acted on (time-bounded):** `check-store-rank` (stale 181c)
      found 10 near-page-1 ranks -- written up as the new follow-up directly above.
      $0 spent, 0 new Actors, revenue still $0 booked, no owner email warranted.

- [x] **DONE cycle 2278 (NOT a QUALITY slot -- `2278%3==1`) -- found and fixed a real
      measurement-integrity bug in `bin/traffic`'s VERIFIED filter (both `pageviews` and
      `out_click`), found by a method never applied before (grouping by `vid` instead of
      auditing UA strings).** Re-verified fresh first: `bin/checks-due`/`bin/audit-due
      --all`/`--type varied_test --all` all NONE DUE, inbox unchanged (same 10 known items,
      newest DMARC still `e2f3a358`), services active, site 200, `HEAD == origin/main`
      (`1e812006`), tree clean. 0 Actors created today. `health.json` all 24 Actors `ok:true`.
      **The bug:** a single-visit bot session with a plausible (non-bot-tagged) UA that
      loads every known URL in under 90 seconds passed both existing VERIFIED conditions
      (UA not bot-like; vid registered in `asset_hits`) because the filter only ever checked
      UA *strings*, never visit *speed/pattern*. 10 such sweep vids found, spanning
      2026-09-12 to 2026-10-17 (0-85s for 20-56 distinct pages, or all 24 `/go/<slug>` links
      in 0-1s) vs. a clean gap from real multi-page sessions (8-20 pages taking 436-686s).
      **Why now:** this funnel is the direct input to the CLAUDE.md Polar-escalation trigger
      (`>100 verified visits/day`) and the pending c2276 CTA-fix measurement (~cycle 2420) --
      a repeat sweep in either window could have forged the owner-email threshold or faked a
      conversion lift. None of the 10 known sweeps fall in the current 7-day window, so no
      past report was wrong -- this is preventive, timed before the 2420 window opens.
      **Fix:** added a `*_SWEEPER` exclusion to each VERIFIED definition (`bin/traffic`) --
      pageviews: `count(*)>=15 AND (max(ts)-min(ts))<=90` per vid; out_click: lifetime
      `count(*)>8` per vid. Caught and fixed a self-inflicted NULL-poisoning bug while
      building it (subquery needs `vid IS NOT NULL` or three-valued SQL logic silently
      zeroes the whole `verified` count) -- documented as a reusable rule in LEARNINGS.
      Verified post-fix: default 7-day report unchanged (28 tools / 2 verified out_clicks --
      confirms no-op today, real guard going forward); full-history run clean, out_click
      `verified=4` lifetime with `sweeper=48` broken out; `bash -n` syntax-clean; services
      and site verified healthy before/after.
      **Side finding:** c2276's "3 lifetime" out-click figure was actually a 7-day-window
      figure mislabeled lifetime (`bin/traffic` defaults to `D=7`); true lifetime is 4. Does
      not change the c2276 decision rule (still reads the 7-day default report).
      $0 spent, 0 new Actors, revenue still $0 booked, no owner email warranted (a
      false-positive-prevention fix is not itself a trigger event). **Next `varied_test`
      target when due: `grants-gov-scraper` (last 2213, due 2549).** The c2276 CTA-fix
      follow-up stays the next real growth checkpoint -- still too early (due ~2420).

- [x] **DONE cycle 2277 (MANDATED QUALITY/GROWTH slot -- `2277%3==0`) -- pure fleet-health
      verification cycle, $0 spent, no code change needed; closed the one open thread c2275
      left behind.** Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/`--type
      varied_test --all` all NONE DUE (both explicitly say do not run a sweep this cycle),
      inbox unchanged (same 10 known items, newest DMARC still `e2f3a358`), services active,
      site 200 on `/` `/tools` `/pricing` `/docs` `/llms-full.txt`, `HEAD == origin/main`
      (`aca08869`), tree clean. 0 Actors created today (confirmed via git log, not the noisier
      `find -newermt` read).
      **Ran every ad-hoc static QUALITY tool NOT on the `fleet_checks.json` cadence clock**
      (so `checks-due` never flags them): `check-filter-reach` 25/18/0, `check-source-bytes`
      630 files/0 flagged, `check-code-fields` 0 drift, `check-registry-fields` 0 drift (2
      expected multi-record-type soft-flags), `check-charges` 25/0/0, `check-meta-fields` 9/0
      stale, `check-pricing` 25/30/0 drift -- plus the standard 4 PLAYBOOK tools
      (`check-disclosure` 88+24/0 missing, `devto-comments` 24/0 unanswered, `check-backlinks`
      131/0 missing, `check-actor-guides` 24/0 flagged). All clean, nothing recorded via
      `--ran` since none were due.
      **Closed c2275's loose end:** pulled live descriptions (not just Store titles) for
      `trademark-search-scraper`'s 3 closest rivals (`scrapers_lat/tmview-global-trademarks-
      scraper`, `automation-lab/euipo-tmview-trademarks-scraper`, `jdepablos/trademark-watch-
      tmview`). All three are already named, priced, and feature-countered in our own README
      (opposition deadlines, Vienna codes, territories, watch-mode status alerts all shipped
      and compared as recently as cycle 1324) -- **no closeable gap exists at the README
      level**; a real diff now needs actually running a rival Actor, which is the scheduled
      `competitor_audit` rotation's job (due cycle 2417).
      $0 spent, 0 new Actors, revenue still $0 booked, no owner email warranted. **Next
      `varied_test` target when due: `grants-gov-scraper` (last 2213, due 2549).** The c2276
      CTA-fix follow-up below stays the next real growth checkpoint -- still too early.

- [x] **DONE cycle 2276 (NOT a QUALITY slot -- `2276%3==2`) -- FIXED a real conversion defect
      on all 24 public tool pages: the most prominent action on each one pointed at a product
      no visitor can buy.** Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/
      `--type varied_test --all` all NONE DUE, inbox unchanged (same 10 known items, newest
      DMARC still `e2f3a358`), services active, site 200, `HEAD == origin/main` (`f87423f2`),
      tree clean. 0 Actors created today.
      **The defect:** `site/templates/tool.html`'s `<h2>Run it</h2>` block -- above the fold,
      before Output fields and Sample output -- rendered ONLY `curl -X POST
      https://fetchsmith.com/api/v1/run/<slug> -H "Authorization: Bearer YOUR_KEY"`. That key
      is unobtainable while Polar is deferred: the endpoint answers **401 "Missing API key"**
      (curled live), `/pricing` reads "Hosted checkout is opening shortly", and `bin/traffic`'s
      api-usage table is **0 calls / 0 results ever**. The working path (Apify) was a sidebar
      button. **Same defect class cycle 1744 fixed for the headline PRICE in the same
      template's `aside`; the runnable example beside it was missed and stayed wrong ~530c.**
      **Why this surface:** verified (non-crawler) `bin/traffic` shows **28 verified visits to
      `/tools/*` in 7 days** -- the biggest buyer-intent bucket, `/pricing` 0 -- against **3
      verified `/go/` out-clicks lifetime**. Humans reach the product page at max intent and
      click nothing. `bin/store-anon-rank`'s standing conclusion (rank gated on `totalUsers`,
      so metadata cannot win a cold start; only off-platform direct links can) makes the tool
      page the highest-leverage thing we control.
      **The fix (`3bc3754a`):** while `checkout_live` is false AND `t.apify_listed != false`,
      lead with the pasteable real call -- `curl -X POST "https://api.apify.com/v2/acts/
      fetchsmith~<slug>/run-sync-get-dataset-items?clean=true" -H "Authorization: Bearer
      YOUR_APIFY_TOKEN"` + the Actor's own `example_input` -- framed "Pay-per-result on Apify,
      no FetchSmith account needed", with a no-token alternative (**Run** on `/go/<slug>`) and
      a `console.apify.com/settings/integrations` token link; hosted API demoted to one muted
      line pointing at `/docs`. The old curl is kept on the `checkout_live` branch so nothing
      needs undoing when Polar opens. **Verified end-to-end, not just rendered:** the exact
      published command shape ran live on `hacker-news-scraper` (`maxItemsPerQuery`/
      `maxResults` 3) -> **HTTP 201, 3 clean rows** with real titles.
      **Second defect the first one exposed:** 9 of 25 `registry.json` `example_input` blocks
      held a key the Actor's own `input_schema.json` does not declare -- harmless while the
      example targeted our API, but about to be published as valid *Apify* input, and **Apify
      silently ignores unknown input keys** (the PLAYBOOK's ~$1.10 apple-podcasts hazard). 8x
      `max_results` (hosted-API-only alias, no `src/main.js` reads it) -> declared `maxResults`
      at the same value; `remote-jobs-scraper` `keyword` -> `searchKeyword` (`src/main.js:112`).
      All 25 now validate 0-unknown-key. Also cleans the fallback input `bin/actor-health` and
      `bin/check-row-floor` use for real platform runs.
      **Post-edit verification:** `check-example-input` 25/0 drift, `check-cta-presence` CLEAN,
      `check-blog-cta` 88 posts / 0 dead-link; site 200 on `/` `/tools` `/pricing` `/docs`
      `/llms-full.txt`; `/go/<slug>` still 302s correctly. `load_registry()` is uncached and
      Jinja autoreloads, so **no service restart needed or done**. All 24 live tool URLs
      resubmitted to IndexNow. ~$0.01 spent (platform compute on one capped own-Actor run),
      0 new Actors, $0 revenue, no owner email warranted.

- [ ] **NEW follow-up (c2276) -- MEASURE the tool-page CTA fix. This is the first on-site
      conversion number this fleet has ever been able to move; do not let it go unread.**
      Baseline recorded 2026-10-26 ~11:40 UTC, immediately BEFORE the fix went live:
      `bin/traffic` verified `/go/` out-clicks = **3 lifetime** (app-store-reviews 1,
      ats-jobs 1, google-news 1), verified `/tools/*` visits = **28 per 7 days**, verified
      views 11-24/day, hosted-API calls 0 lifetime.
      **When:** in ~2-3 days (roughly **cycle 2420+**), not sooner -- at 28 verified /tools
      visits per week, a 1-day window cannot distinguish a real lift from noise.
      **How:** `bin/traffic`, read the `verified` column of the out_click table ONLY (the raw
      column is ~98% crawler per c1652) and the `tools` row of the BUYER-INTENT funnel.
      **Decision rule, so a future cycle does not have to re-derive it:**
      (a) verified out_clicks still <= 3 after ~2-3 days of comparable /tools traffic -> the
      CTA was NOT the binding constraint; stop iterating on tool-page copy and say so here,
      because the remaining candidates are traffic volume (11-24 verified views/day is simply
      small) and the Apify signup wall, neither of which a template edit can move.
      (b) verified out_clicks up but still single digits -> real but tiny; next lever is
      VOLUME (the AI-citability / dev.to channel, AI:search 7.86:1 per `bin/channel-mix`),
      not more CTA tuning.
      (c) a jump to double digits -> the tool page WAS the constraint. Then audit the same
      "does this page lead with something the visitor can actually do?" question on `/`,
      `/tools`, `/pricing` and the top blog posts, which were never checked for it.
      **Do NOT email the owner on any of these** -- an out-click is not revenue and we still
      cannot read earnings (c2168). The owner trigger stays the CLAUDE.md Polar gate (>100
      verified /pricing or /tools visits/day) or a bookmark/review.

- [x] **DONE cycle 2275 (NOT a QUALITY slot -- `2275%3==1`) -- no new growth lever found;
      checked fresh signals (`bin/revenue`, `bin/traffic`, `state/health.json`) rather than
      repeating the Caddy-log-grep method a 4th cycle running; did a bounded competitor
      spot-check on `trademark-search-scraper` (Store listing titles only) and found no
      closeable gap in the time available.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/`--type varied_test
      --all` all NONE DUE, inbox unchanged (same 10 known items, newest DMARC still
      `e2f3a358` -- c2103's trigger hasn't fired), services active, site 200, `HEAD ==
      origin/main` (`115b1fcf`), tree clean -- **STATUS.md/queue.md edits are the only
      change, pushed together.**
      `bin/revenue`: `bkmk`/`rev` still 0/0 across 25 Actors, `runs30d` 747, same
      non-billable pattern. `bin/traffic`: 3 verified out-clicks total, flat. `health.json`
      still the original 04:00:30 nightly report, untouched. All 3 open follow-ups
      (c2272/c2196/c2103) re-confirmed correctly blocked, not re-litigated.
      `bin/apify-admin store "trademark" 15`: top rival `dltik/euipo-trademarks-scraper`
      144 users; closest USPTO rivals `dev00/uspto-trademark-api` (107), `memo23/uspto-
      trademark-scraper` (45). Our Actor already covers 70+ TMview offices in one run (vs
      competitors' single-office titles), 22 fields, watch-mode + webhook, documented
      0-result diagnostics -- no concrete gap found from Store titles alone. A real
      feature diff needs reading a competitor's actual README, which is what the scheduled
      `competitor_audit` (due cycle 2417) is for -- did not duplicate that work ad hoc.
      $0 spent, 0 new Actors, revenue still $0 booked, `bkmk`/`rev` unchanged, no owner
      email warranted. **Next `varied_test` target when due: `grants-gov-scraper` (last
      2213, due 2549).** The c2272 `/llms-full.txt` fetch-check follow-up is still too
      early (~3 cycles old) -- don't check before ~cycle 2321.

- [x] **DONE cycle 2274 (QUALITY/GROWTH slot -- `2274%3==0`, verified via
      `python3 -c "print(2274%3)"`) -- no new growth lever found; sharpened the Caddy-log
      method to also read HTTP method (not just path+status), chased three candidate
      leads, ruled out all three as already-fine rather than bugs.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/`--type varied_test
      --all` all NONE DUE, inbox unchanged (nothing to answer), `bin/devto-comments` ad hoc
      re-check 0 unanswered of 12 inbound, services active, site 200, `HEAD ==
      origin/main` (`603cbb18`), tree clean -- **no commit this cycle, STATUS.md/queue.md
      edits are the only change, pushed together.**
      (1) `HEAD /` and `HEAD /blog` showed 405 in log data up to ~54 days old (real
      monitoring-tool UAs: `python-httpx`, `Go-http-client`, `node`) -- live `curl -I`
      against both today returns 200, already fixed, nothing to do. (2) `OPTIONS /` 405
      with `Allow: GET` is correct REST behavior, not a bug. (3) ~90 `GET
      /api/v1/run/<slug>` 405s (that route is `POST`-only, `site/app.py:774`) looked like
      buyers misreading the `curl -X POST` snippet in `home.html`/`tool.html` at first, but
      it's one UA (`iPhone OS 13_2_3`) mechanically cycling every slug incl. nonexistent
      ones plus explicit scanner UAs (`ZOLTRAAK`, `meta-webindexer`) -- automated probing,
      not confused humans; the 405 returned is already correct.
      Also checked the two previously-flagged "unblogged content gaps" (c2263 FEC
      charge-limit fix, c2264 Shopify `available`-field fix) for a README gap instead of
      waiting on a blog slot -- **both already fully documented** in their Actor's FAQ
      (`fec-campaign-finance-scraper/README.md:358`, `shopify-products-scraper/README.md:162`),
      so no README edit needed; the gap is blog-narrative only, and today's blog cadence
      was already satisfied by c2271's post.
      $0 spent, 0 new Actors, revenue still $0 booked, `bkmk`/`rev` unchanged, no owner
      email warranted. **Next `varied_test` target when due: `grants-gov-scraper` (last
      2213, due 2549).** The c2272 `/llms-full.txt` fetch-check follow-up is still too
      early (~2 cycles old) -- don't check it again before ~cycle 2321.

- [x] **DONE cycle 2273 (NOT a QUALITY slot -- `2273%3==2`) -- no new growth lever found;
      chased the `/blog/null` lead from the c2272 log-grep method and ruled it out as stale
      (no live occurrence since 2026-10-04); caught and stopped a self-inflicted duplicate
      `bin/actor-health` run (~$0.03, no lasting effect) before it could overwrite today's
      real 04:00 report or open a spurious FIX task.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/`--type varied_test
      --all` all NONE DUE, inbox unchanged (nothing to answer), services active, site 200,
      `HEAD == origin/main` (`a7026eb8`), tree clean -- **no commit this cycle, STATUS.md/
      queue.md edits are the only change, pushed together.**
      Grepped Caddy 404s for non-scanner paths (c2272's method): the one repeat worth
      chasing was `/blog/null` (27 hits, always referred from a real `/blog/<slug>` post,
      always Facebook's `meta-externalagent`) but every timestamp predates 2026-10-04 --
      curled a live affected post today, grepped every `href=` in the raw HTML and every
      template + `content/blog/*.md` for the literal string, found nothing. Whatever
      produced it is already gone from the live site (fixed by an intervening cycle, never
      written up) -- nothing left to fix, so no code change and no LEARNINGS entry.
      **Full detail on the near-miss is in STATUS.md this cycle** -- short version: guessed
      `bin/actor-health --help` to check its usage instead of reading the script first; it
      has no `--help` handling so the flag was ignored and it re-ran the real nightly
      all-Actors health check a second time today. Stopped via `TaskStop` within ~45s;
      confirmed via the Apify runs API only ~25 small runs executed (~$0.03) and
      `state/health.json` still shows the original 04:00:30 report, untouched.
      $0.03 spent (the near-miss only), 0 new Actors, revenue still $0 booked, `bkmk`/`rev`
      unchanged, no owner email warranted. **Next `varied_test` target when due:
      `grants-gov-scraper` (last 2213, due 2549).** The c2272 `/llms-full.txt` fetch-check
      follow-up (below) is still too early to act on.

- [x] **DONE cycle 2272 (NOT a quality slot -- `2272%3==1`; nothing due anywhere, so growth
      work per `checks-due`'s own instruction) -- shipped `/llms-full.txt`, the llms.txt
      convention's full-content companion, which was a 404 that real external AI crawlers were
      requesting BY NAME.**
      Re-verified fresh first (c2120 process lesson): `bin/checks-due` NONE DUE (soonest
      `check-status-continuity` in 9c), `bin/audit-due --all`/`--type varied_test --all` both
      NONE DUE, inbox unchanged (same 10 known items, newest `c2fa5a9c`, newest DMARC still
      `e2f3a358`/ts 1792145357 -- nothing to answer), services active, site 200, `HEAD ==
      origin/main` (`82bd9b23`), tree clean, 0 Actors created today.
      **Why this and not a blog post or a niche hunt:** found in the Caddy access logs, not
      guessed -- `/llms-full.txt` had 4 lifetime requests, all 404, and one is a genuine
      third-party agent crawler (`agentcensus-crawler/1.0`, ts 1792882360) that fetched
      `/llms.txt` and 0.36s later asked for `/llms-full.txt`. `bin/channel-mix` measures
      assistant/AI traffic at ~7.9x search, so the file answer engines ask for by name is the
      highest-leverage page the site can add, and niche-hunting is documented exhausted across
      9 axes (NICHES.md c2093).
      **What shipped (`ebf4c014`):** 244KB / 1,153 lines, HTTP 200. Each of the 24 public tools
      expanded in place -- docs URL, Apify URL + payable-today price, summary, **every input
      parameter with type/default/allowed values/full description (504 params, exactly the
      fleet's schema count once `_template` and retired `scholarship-scraper` are excluded)**,
      example input JSON, full output-field list. Read live from
      `actors/<slug>/.actor/input_schema.json` (mtime-stamped cache like `_blog_cache`), so
      there is no second copy to drift. This is NEW information on the site, not a reshuffle:
      `tool.html` renders only `example_input` + `output_fields`, so until now an answer engine
      could say what a tool returns but not how to ask for it.
      `_apify_price_phrase` lifted to module scope so both files share one price wording --
      verified output-neutral by before/after diff of `/llms.txt` (only the added pointer line).
      `prefill` printed as `no default, Apify Console prefills X`, never as a default (20 fleet
      fields have prefill without default; an API call does not get them; spot-checked
      `court-records-scraper` `src/main.js` has no code-level fallback either). Pointers added
      from the `/llms.txt` Docs section and the `robots.txt` comments. `bin/check-citable` run
      as verification (not recorded, not due): CLEAN.

- [ ] **NEW follow-up (c2272) -- in ~1-2 days, check whether anything actually FETCHED
      `/llms-full.txt`, and only then expand it further.** This is the honest test of the c2272
      change and it is cheap (no network, read-only). Run:
      `python3 - <<'EOF'` over `/var/log/caddy/fetchsmith.access*` (gzip + plain, `json.loads`
      each line, filter `'llms-full' in line`, print ts/status/User-Agent) -- the same one-liner
      shape c2272 used; **ignore `curl/8.5.0` rows, those are our own probes.** Baseline to
      compare against: as of c2272 there were exactly 4 lifetime requests, ALL 404, of which 1
      was external (`agentcensus-crawler/1.0`, ts 1792882360).
      **If real non-curl agents are fetching it 200:** the next expansion is guide BODIES (the
      88 posts, 860KB of markdown) -- `_parse_post` currently keeps only rendered `html`, so
      that needs the raw `body` retained in the cache (~860KB more RSS, acceptable on 2GB but
      measure `systemctl status fetchsmith-web` RSS before/after). **If nothing fetched it:**
      do NOT expand it further and do not keep re-checking -- record that result and treat the
      llms.txt family as done at this size, since the cost of a bigger file is real and the
      measured benefit would be zero.

- [x] **DONE cycle 2271 (MANDATED QUALITY/GROWTH slot -- `2271%3==0`, verified via
      `python3 -c "print(2271%3)"`) -- ran all 4 PLAYBOOK quality tools (all clean) and wrote +
      published the dev.to-due blog post on the c2262 google-play-reviews-scraper watch-mode
      "new review count" bug, closing a real content gap.**
      Re-verified fresh first: `bin/checks-due` NONE DUE, `bin/audit-due --all`/`--type
      varied_test --all` both NONE DUE (`competitor_audit` explicitly says do not run a sweep
      this cycle), inbox unchanged (same 10 known items, owner thread `dc593cfb` re-confirmed
      resolved -- nothing to answer), services active, site 200 everywhere, `HEAD ==
      origin/main` (`5e74d3bf`) and tree clean before edits.
      **Quality tools:** `check-disclosure` 88 site posts + 24 dev.to articles / 0 missing;
      `devto-comments` 23 articles / 0 unanswered; `check-backlinks` 131 pairs / 0 missing;
      `check-actor-guides` 24 Actors / 0 flagged. Both backstop-cadence tools recorded via
      `bin/checks-due --ran` (next due 2319 / 2415).
      **The post:** last site post was ~2 days old (edge of the 2-3 day cadence), and a grep
      across all 87 existing posts confirmed the c2262 fix (phantom "new review" count from a
      per-app snapshot row riding along in the `pushed - watchChanged` formula) had never been
      written up, despite being a concrete, numeric, buyer-relevant bug in the house voice.
      Wrote `watch-mode-new-review-count-included-a-snapshot-row.md` using the already-live-
      verified c2262 numbers (2 pushed/0 new reported as 2, should be 1; scoreChanged control
      2 pushed/1 changed reported as 1, should be 0) and the real code diff; used the NEUTRAL
      disclosure footer since no fresh live call was made specifically while writing this post
      (the strong footer's "fetched while writing" claim would have been false here).
      `check-blog-cta` caught a real omission before commit (linked `/tools/` instead of a
      direct `/go/` CTA) -- fixed. Built the dev.to draft the documented way (cycle 2173
      lesson: scratch `/tmp` file, H1 + stripped frontmatter) and additionally confirmed from a
      previously-published article's live `body_markdown` that dev.to needs ABSOLUTE
      `https://fetchsmith.com/...` links, not the site's relative ones -- rewrote them before
      publishing (new finding, not previously documented; worth a LEARNINGS entry if this trips
      again). Published dev.to id `4920453`, verified 200 live. `check-blog-claims`/
      `check-blog-cta`/`check-backlinks`/`check-links`/`check-disclosure` all clean after.
      3 commits pushed to `origin/main` (`7c656148` post, `ad530aab` fleet_checks.json state).
      $0 spent (pure content work, no Actor runs, no builds), 0 new Actors, revenue still $0
      booked, `bkmk`/`rev` 0 across all 25 Actors (unchanged), no owner email warranted.
      **Still-unblogged content gaps for a future QUALITY slot (checked, confirmed not covered
      by any existing post): the c2263 fec-campaign-finance-scraper watch-disclosure
      "incomplete scan" fix, and the c2264 shopify-products-scraper `available`-field ordering
      fix.** Next `varied_test` target when due: `grants-gov-scraper` (last 2213, due 2549).
      Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`,
      `/pricing`, and the new post URL), verified again after all edits.

- [x] **DONE cycle 2270 (NOT a QUALITY slot -- `2270%3==2`, verified via
      `python3 -c "print(2270%3)"`) -- cleared the one DUE fleet check (`check-source-endpoints`,
      last 2246) and fixed a real recurring false-positive in it rather than just dismissing the
      flag again.**
      Re-verified fresh first: `bin/checks-due` **1 DUE (`check-source-endpoints`, last 2246)**,
      `bin/audit-due --all` NONE DUE (soonest `competitor_audit`: website-screenshot-scraper in
      147c, cycle 2417), `bin/audit-due --type varied_test --all` NONE DUE (soonest
      `grants-gov-scraper` in 279c, cycle 2549), inbox unchanged (same 10 known spam/DMARC/
      resolved items, newest still `c2fa5a9c` -- nothing to answer), services active, site 200
      on `/` `/tools` `/pricing`, `HEAD == origin/main` (`cb8bd384`) and tree clean before edits.
      **The check:** `bin/check-source-endpoints` flagged 1 DEVIATION: `rss.marketingtools.
      apple.com` (apple-podcasts-scraper's only non-exempt upstream) went `ok` -> `error`/
      `ReadTimeout` on the bare root `/` under the script's 10s timeout. Direct `curl` and a
      standalone `httpx` loop both got 200 in <3s immediately after; the real endpoint the
      Actor actually depends on (`/api/v2/<country>/podcasts/top/<n>/podcasts.json`) also
      answered correctly. **This exact false positive on this exact host already happened at
      cycle 2222** (per `fleet_checks.json`'s own prior note) and was dismissed both times as "a
      transient blip" with no code change -- so instead of writing a third identical dismissal,
      reproduced the flake standalone (ran the unmodified checker 3x back-to-back: 1 DEVIATION,
      then 0, 0, 0 -- genuinely intermittent, not a one-off) and fixed the root cause.
      **The underlying bug this surfaced:** `run_real()` writes `baseline[host]=...`
      unconditionally every run, including on an `error` bucket -- so a single flaky timeout
      silently overwrites a healthy baseline to `error`, and a REAL future break on that same
      host would then go undetected (error->error isn't `broke`) until the host happened to
      self-heal on some later run. **Fix:** split `probe()` into `probe_once()` (original logic)
      + a `probe()` wrapper that retries once, only on an `error` bucket, before accepting it
      (`bin/check-source-endpoints`). `--selftest` still passes unchanged (exercises the
      baseline-comparison logic directly, not the network path); 3 consecutive live runs
      post-fix were all CLEAN. Documented as a LEARNINGS entry (does not fully eliminate the
      false-positive window -- two flaky hits in a row is still possible, just far less likely --
      so a repeat flag on this host even after the retry should be treated as real signal, not
      dismissed a third time).
      Recorded via `bin/checks-due --ran check-source-endpoints` -> next due 2294. 3 commits
      pushed to `origin/main` (`6fcce322` code+LEARNINGS, `453e1b6e` fleet_checks.json state).
      $0 spent (no Actor runs, no builds), 0 new Actors, revenue still $0 booked, `bkmk`/`rev`
      0 across all 25 Actors (checked via `bin/audit-due --all`'s table, no change), no owner
      email warranted.
      Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`,
      `/pricing`), verified again after all edits.

- [x] **DONE cycle 2268 (MANDATED QUALITY/GROWTH slot -- `2268%3==0`, verified via
      `python3 -c "print(2268%3)"`) -- cleared the one DUE fleet check by TRIMMING both live
      docs proactively (STATUS.md 134.9KB->20.6KB, queue.md 101.6KB->21.4KB, losslessly), ran
      all 4 PLAYBOOK QUALITY tools (all clean), and CORRECTED a stale standing queue item after
      measuring that the metric it watched is reversible.**
      Re-verified fresh first: `bin/checks-due` **1 DUE (`check-doc-size`, last 2244)**,
      `bin/audit-due --all` NONE DUE (soonest `competitor_audit`: website-screenshot-scraper in
      149c, cycle 2417), `bin/audit-due --type varied_test --all` NONE DUE (soonest
      `grants-gov-scraper` in 281c, cycle 2549 -- so NO varied_test this cycle, per the tool's
      own "spend the cycle on growth/quality work instead"), inbox unchanged (same 10 known
      spam/DMARC/resolved items, newest still `c2fa5a9c` -- nothing to answer), services active,
      site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main` (`e2c7600a`) and tree clean
      before edits.
      **(1) The trim -- the one c2244's own script predicted would fall due at exactly this
      cycle.** `check-doc-size` read TRIM SOON (not DUE) on both docs: positive headroom today
      but ~241KB / ~229KB projected at its own next look (24c, cycle 2292), i.e. past both the
      150KB warn and 200KB trim lines BETWEEN looks -- the escalation its own advice says to
      pre-empt in a QUALITY slot (c2220 follow-up). `bin/_trim2268.py`: STATUS.md 346 -> 70
      lines / 20.6KB, keeping the newest 6 blocks (2262..2267). Unlike at 2244 the 29 blocks
      were STRICTLY newest-first (2267..2239, asserted), so every prefix was hole-free for
      check-status-continuity and the keep-count was pure arithmetic. `bin/_trim2268q.py`:
      queue.md 1249 -> 259 lines / 21.4KB, keeping the same 6 DONE blocks (here a single
      contiguous prefix, lines 1-219) + ALL 5 live open items HOISTED; 0 archived as closed
      (no `- [ ] NEXT` handoff item and no duplicate this time -- c2244's 7 hoisted items are
      down to 5 because c2243 competitor-claims, c2238 x-appliesTo, both c2232 items, c2228
      eu-ted flatten and c2224 maxCommentDepth were all closed by cycles since).
      6 lossless verifications passed in each script before writing (full-file reconstruction,
      byte-identical archive prefix, no destroyed block header, live window contiguous).
      After: `check-doc-size` OK/OK/OK (41c and 34c headroom), `check-status-continuity` NONE
      MISSING (674 blocks retained, window 2262..2267, 6 rc=0 cycles all present),
      `check-status-blocks-kept` OK (HEAD's 29 blocks all still present across live+archive).
      Recorded via `bin/checks-due --ran check-doc-size` -> next due 2292.
      **Rates re-measured, as c2244's script explicitly asked the next trim to do rather than
      re-derive:** STATUS.md ~4.7KB/cycle actual (c2244 left 21.5KB; file hit 134.9KB in 24c) --
      the checker's +4510 B/c is accurate for this file, used as-is. queue.md ~3.3KB/cycle
      actual (c2244 left 24.0KB; file hit 101.6KB in 24c) vs the checker's +5440 B/c, i.e. it
      runs ~60% hot here -- third consecutive measurement agreeing on 3.3-3.9KB/c (c2220 ~3.75,
      c2244 ~3.9, c2268 ~3.3). Projections at cycle 2292: STATUS.md 126KB, queue.md ~104KB at
      the measured rate (149KB at the checker's pessimistic one). Kept 6 blocks not 8 in
      STATUS.md because 8 would have left 32.4KB projecting 142.5KB -- only 7KB under the warn
      line, the cycle-1976 mistake c2220 and c2244 both named.
      **(2) All 4 PLAYBOOK QUALITY tools, all clean:** `check-disclosure` 87 site posts + 23
      dev.to articles / 0 missing; `devto-comments` 23 published / 7 with comments / 12 inbound
      / 0 unanswered / 1 spam-skipped; `check-backlinks` 131 post-Actor pairs across 87 posts /
      0 missing / 0 unresolved; `check-actor-guides` 24 live Actors / 0 flagged. No support mail
      to answer.
      **(3) The real finding -- the `users` column is reversible, so the c2168 standing item was
      watching a metric that retracts.** Glanced at `bin/usage-trend` per that item and noticed
      its premise ("trademark-search-scraper is the only Actor off the baseline and the only one
      at 3 users") no longer held: shopify-products-scraper is at 4. Dug the transitions out of
      `state/revenue_history.json` (400 snapshots, ~every 30 min, printing only the snapshots
      where the tuple CHANGES -- collapses 400 records to 7 lines) and found the field is **not
      cumulative and not monotone**: `website-screenshot-scraper` went 1->2->3->1 inside ~36h
      (10-19 23:00 -> 10-21 11:30) and `steam-reviews-scraper` 2->3->1 in 17h (10-22 16:00 ->
      10-23 09:18), i.e. a -2 step. So shopify's 3->4 (10-24 16:03) and trademark's 2->3 (10-23
      09:18) are equally likely to evaporate and neither is evidence of a buyer. Rewrote the
      c2168 open item: it now carries the DECISION RULE only (escalate on a bookmark, a review,
      or `bin/traffic` buyer intent -- never on a run/user climb) plus today's numbers explicitly
      marked re-derive-don't-trust, instead of a named-leader claim with a ~1-day shelf life.
      Wrote the method + the three consequences up in LEARNINGS c2268.
      `bin/traffic` checked in the same pass: 11-24 VERIFIED views/day fleet-wide (raw
      207-440/day is crawler-inflated), 3 verified out_clicks total, top verified paths are blog
      posts and `/tools/<slug>` pages at 5-7 views each -- nowhere near the CLAUDE.md Polar gate
      (>100 verified visits/day to /pricing or /tools), so no owner email, correctly.
      $0 spent (no Actor runs, no builds -- all local/read-only work), 0 new Actors, revenue
      still $0 booked, `bkmk`/`rev` 0 across all 25 Actors, no owner email warranted.
      **Next `varied_test` target when one next comes due: `grants-gov-scraper` (last 2213) --
      but note NOTHING is strictly due until cycle 2549, so the next two cycles should pick up
      queue work rather than force a rotation.**

- [x] **DONE cycle 2267 (NOT a QUALITY slot -- `2267%3==2`, verified via
      `python3 -c "print(2267%3)"`) -- ran the fleet-oldest `varied_test`
      (`app-store-reviews-scraper`, 2212, 55c stale): FIRST-EVER live test of watch-mode
      `scoreChanged` detection on this Actor. 0 defects, clean confirmation, no code change.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/`bin/audit-due --type
      varied_test --all` all NONE DUE, inbox unchanged (same 10 known spam/DMARC/resolved
      items, newest still `c2fa5a9c` -- nothing to answer; also re-checked the old owner
      "Done" identity-verification thread (`dc593cfb`) via `apify-admin list` and confirmed
      `website-screenshot-scraper` is public, fleet at 25 live Actors -- stays resolved),
      services active, site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main` (`43d7b246`)
      and tree clean before edits.
      Grepped all 6 prior `varied_test` notes on this Actor (833/1089/1517/1827/2182/2212) for
      `watchLabel`/`webhookUrl`/"watch mode" -- all scored 0 (c2228 method), so the entire
      watch mechanism (shipped alongside the Actor, never exercised live) was the gap.
      (1) Seed run `{apps:["324684580"], countries:["us"], sort:"mostRecent",
      maxReviewsPerApp:50, maxResults:5, watchLabel:"ast-watch-test1"}` (Spotify) -> HTTP 201,
      `pushed:0`, baseline of 50 reviews recorded in KV store `fetchsmith-app-store-reviews-watch`.
      (2) Reimplemented `watchKeyFor()` in python (sha1 of `JSON.stringify(criteria,
      sortedKeys)`, compact separators) to compute the exact KV key -- matched the live key
      first try (`watch-ast-watch-test1-d31527f929`). Doctored one real review's stored
      `seenMeta` (id `324684580:us:6052627987`, live rating 5) from 5 down to 1 via the
      key-value-store API, simulating a stale baseline predating a rating change. (3) Re-ran
      the identical input -> exactly 1 row: `reviewId:6052627987`, `rating:5` (today's live
      value), `watchEvent:"scoreChanged"`, `previousScore:1` (the doctored value) -- precisely
      correct. Run log status message matched `main.js:1344` verbatim. `chargedEventCounts`
      settled to `{result:1}` == 1 delivered row (polled 6x/60s), 0 leak. Test KV record
      deleted after (204, confirmed 404 on re-GET).
      `check-charges` 25/0, `check-pricing` 25/30/0 both clean (no build, no code touched).
      `audit_dates.json` recorded at 2267 with full note.
      ~$0.0005 spent (1 free seed run, 1 charged test result), 0 new Actors, revenue still $0
      booked, no owner email warranted. **Next `varied_test` target: `grants-gov-scraper`
      (2213, now fleet-oldest by `last`).** Still untested on `app-store-reviews-scraper`
      itself: `webhookUrl` (generic mechanism fleet-verified on `federal-register-scraper` at
      c2265, never on this Actor specifically).

- [x] **DONE cycle 2266 (NOT a QUALITY slot -- `2266%3==1`, verified via
      `python3 -c "print(2266%3)"`) -- ran the fleet-oldest `varied_test`
      (`sam-gov-opportunities-scraper`, 2211, 55c stale): closed TWO gaps at once --
      first-ever test of `wage-determinations-cba` (last of the 3 wd siblings, per c2211's
      own note) AND first-ever test of `watchLabel`/`watchChanges` on this Actor at ANY
      dataType. 0 defects, clean confirmation, no code change.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/`bin/audit-due --type
      varied_test --all` all NONE DUE, inbox unchanged (same 10 known spam/DMARC/resolved
      items, newest still `c2fa5a9c` -- nothing to answer), services active, site 200 on `/`
      `/tools` `/pricing`, `HEAD == origin/main` (`c144868c`) and tree clean before edits.
      Predicted free first via 3 direct `sam.gov/api/prod/sgs/v1/search/?index=wd` calls:
      scanned 200 live CBA rows and found `revisionNumber` can be nonzero even when
      `isActive:true` (`_id` 56262, `cbaNumber` CBA-2013-6079, `revisionNumber` 1) --
      confirming a CBA revision updates the SAME `_id` in place, so `watchChanges`'
      `revisionNumber` detection is genuinely live-exercisable. `keyword:"CBA-2013-6079"`
      isolates exactly that 1 record live.
      (1) Seed run (watchLabel + watchChanges:true) -> `watchSeeding:true`, `baselineSize:1`,
      `pushed:0`, `watchChangeBlindFilters:["isActive"]` (correct, documented default-on
      `activeOnly` blind spot). (2) Reimplemented `watchKeyFor()` in node to compute the exact
      KV key, doctored the live named record (`fetchsmith-samgov-watch`) via the
      key-value-store API -- set the stored revisionNumber from the real 1 down to 0.
      (3) Re-ran identical input -> `watch-incremental`, `pushed:1`, `changedRedelivered:1`,
      `chargedEventCounts` settled `{result:1}`, 1:1 no leak. Dataset row confirmed:
      `revisionNumber:1` (today's live value), `_watchChangeType:["revisionNumber"]`,
      `_watchPrevious:{revisionNumber:0}` -- exactly correct. Test KV record deleted after
      (204, confirmed 404 on re-GET).
      `check-charges` 25/0, `check-pricing` 25/30/0 both clean (no build, no code touched).
      `audit_dates.json` recorded at 2266 with full note.
      ~$0.0003 spent (2 tiny capped live runs, 1 charged result), 0 new Actors, revenue still
      $0 booked, no owner email warranted. **Next `varied_test` target:
      `app-store-reviews-scraper` (2212, now fleet-oldest by `last`).** Still untested on this
      Actor specifically: `webhookUrl` (generic mechanism fleet-verified on
      `federal-register-scraper` at c2265, never on `sam-gov-opportunities-scraper` itself),
      and `organizationId` combined with `assistance-listings`/`exclusions`.

- [x] **DONE cycle 2265 (MANDATED QUALITY/GROWTH slot -- `2265%3==0`, verified via
      `python3 -c "print(2265%3)"`) -- ran both PLAYBOOK QUALITY tools (check-disclosure,
      devto-comments, check-backlinks, check-actor-guides -- all clean, recorded), then the
      fleet-oldest `varied_test` (`federal-register-scraper`, last=2210, 55c stale): FIRST-EVER
      live test of `webhookUrl` across the ENTIRE FLEET (0-count per c2228's LEARNINGS method),
      also the first test combining it with `watchLabel`. 0 defects -- clean confirmation, not a
      bug cycle.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/`bin/audit-due --type
      varied_test --all` all NONE DUE, inbox unchanged (same 10 known spam/DMARC/resolved items,
      newest still `c2fa5a9c` -- nothing to answer), services active, site 200 on `/` `/tools`
      `/pricing`, `HEAD == origin/main` (`f54f0cbd`) and tree clean before edits (aside from the
      routine daily `state/revenue.json`/`revenue_history.json` snapshot).
      **Quality tools:** `check-disclosure` 87 posts + 23 dev.to articles / 0 missing;
      `devto-comments` 23 articles / 12 inbound / 0 unanswered; `check-backlinks` 131 pairs / 0
      missing; `check-actor-guides` 24 live Actors / 0 flagged. No support mail.
      **The varied_test:** created a real public capture endpoint (webhook.site, no account
      needed) and pointed 3 live platform runs at it as `webhookUrl`. (1) Plain search
      (documentTypes:[NOTICE], agencies:[nuclear-regulatory-commission], maxResults:3) -- webhook
      received one POST, 200, payload matched the run exactly (`pushed:3`, `scanned:3`,
      `summary.complete:false`, `incompleteReason:'max-results'`, correct). (2) Watch SEED (same
      filters, `watchLabel`) -- payload `watchSeeding:true`, `watchNewCount:null`,
      `baselineSize:102`, `pushed:0`, correct. (3) Watch INCREMENTAL after doctoring one id
      (`2026-21781`) out of the live KV baseline via the API (c2210's technique) -- payload
      `watchSeeding:false`, `watchNewCount:1`, `skippedSeen:101`, and the delivered dataset row's
      `documentNumber` matched the doctored-out id exactly. All 3 confirmed independently via the
      run log's own `Posted completion summary to webhookUrl (200)` line. **0 defects** -- the
      mechanism works exactly as coded on both plain search and watch seed/incremental. Test KV
      record deleted after (204, confirmed 404 on re-GET). No code/README change (nothing to fix).
      `check-charges` 25/0, `check-pricing` 25/30/0 drift, both clean.
      **Side-finding, not a bug:** `chargedEventCounts` via `GET /v2/actor-runs/<id>` lagged the
      real charge by far longer than previously seen -- still `{result:0}` ~47s after `SUCCEEDED`
      on the 1-row incremental run, well past c2210's ~15s. Verified the charge had actually
      happened via the run log instead (`pushResult()` only calls `Actor.pushData` after
      `Actor.charge(...).chargedCount > 0`, so a logged "Pushed N documents" **is** proof of
      charge) -- recorded as a LEARNINGS method note so a future cycle doesn't misread a slow
      summary field as a leak.
      `audit_dates.json` recorded (`federal-register-scraper.varied_test` -> 2265, full note).
      ~$0.001 spent (3 small live runs), 0 new Actors, revenue still $0 booked, no owner email
      warranted. **Next `varied_test` target: `sam-gov-opportunities-scraper` (2211, now
      fleet-oldest by `last`).**

- [x] **DONE cycle 2264 (NOT a QUALITY slot -- `2264%3==2`, verified via
      `python3 -c "print(2264%3)"`) -- ran the fleet-oldest `varied_test` (`shopify-products-scraper`,
      2209, 55c stale): FIRST-EVER live test of `detailLevel:"full"` and of the `productDetail`
      charge event, and it found and fixed a real ordering defect. Build 0.1.102 live and
      byte-verified.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all` both NONE DUE, inbox unchanged
      (same 10 known spam/DMARC/resolved items, newest `c2fa5a9c` -- nothing to answer), services
      active, site 200 everywhere, `HEAD == origin/main` (`40947236`) and tree clean before edits.
      **The live test:** every prior `varied_test` here ran basic detail (c2209/c2180/c2162 all
      recorded `productDetail:0`), so the second charge event had never run on the platform.
      Predicted free first (c1514 technique) from `allbirds.com/products.json?limit=5` + each
      handle's `.js` route -> tracked-variant roll-up 8/169/210/160/61. Live run
      (`detailLevel:full`, `maxProductsPerStore:5`, `maxResults:5`) -> 5/5 rows, `totalInventory`
      matched all five predictions exactly, every variant carried barcode/inventoryQuantity/
      inventoryManagement/inventoryTracked/inventoryPolicy, `quantityRule` correctly `null` on
      Shopify's universal default (README claim verified live for the first time), and
      `chargedEventCounts` (via `GET /v2/actor-runs/<runId>`, not the runs-LIST endpoint) was
      `{result:5, productDetail:5}` -- one detail charge per enriched product, 0 leak.
      **The bug:** `enrichWithDetail`'s `available`-resolution block (fills a null `available`/
      `availableVariantCount`/per-variant `available` from the `.js` route's own flags) sat AFTER
      the `nothing found, nothing charged` early return, so the case the README FAQ promises it for
      skipped it: a store publishing no stock data at all (verified free on brooklinen.com -- its
      `.js` route returns inventory_management/policy/quantity ALL null, so `hasInventoryData` is
      false for every variant) whose product page also yielded nothing (bot-blocked -> no `<title>`,
      no meta description, no rating) shipped `available: null` while the `.js` response in hand had
      the answer. Not a charge bug either direction -- a data gap against a stated promise.
      Proved $0 with a pure extraction of the function tail (`/tmp/prove_avail_order.js`): pre-fix
      `charged=0 available=null`, post-fix `charged=0 available=true availableVariantCount=1`;
      both other paths (seo-found, base-route-already-shipped-available) identical pre/post.
      **Fix:** hoisted the fill above both gates (it is a BASE field and costs no request of its
      own), charge rule untouched. Live post-fix regression on the deployed build: 2/2 rows, detail
      fields intact, `{result:2, productDetail:2}`. Build 0.1.102 (package 0.1.17 -> 0.1.18), live
      source byte-identical (76801==76801, sha `257dd1b8`). README needed no change (the FAQ claim
      is now unconditionally true). `check-charges` 25/0, `check-pricing` 25/30/0, `node --check`
      clean. `audit_dates.json` recorded at 2264 with full note.
      ~$0.006 spent (1 push + 3 small live runs), 0 new Actors, revenue still $0 booked, no owner
      email warranted. **Next `varied_test` target: `federal-register-scraper` (2210, now
      fleet-oldest by `last`).**

- [x] **DONE cycle 2263 (NOT a QUALITY slot -- `2263%3==1`, verified via
      `python3 -c "print(2263%3)"`) -- ran the fleet-oldest `varied_test` (`fec-campaign-finance-scraper`,
      2208, 55c stale) and it found and fixed a real disclosure bug. Build 0.1.79 live and byte-verified.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all` both NONE DUE, inbox unchanged
      (10 known spam/DMARC/resolved items, incl. the old owner "Done" verification thread -- already
      acted on, nothing to answer), services active, site 200 everywhere, `HEAD == origin/main`
      (`f59aedff`) and tree clean before edits.
      **The bug:** the incremental watch-mode status message's `pushed === 0` branch fired
      unconditionally, so a run that stopped early (`chargeLimitReached`/`timeBudgetHit`/
      `watchPageCapHit`) before delivering anything told the buyer "every matching contribution had
      already been delivered ... that is the expected result most of the time" -- false confidence
      when the scan genuinely hadn't finished and a real new row could exist past the stopping point.
      Proved via an extracted branch-selection snippet (pure control-flow, $0, no network needed):
      pre-fix code picks the misleading message for `{pushed:0, complete:false,
      incompleteReason:"charge-limit"}`. **Fix:** split on `complete` -- `pushed===0 && complete`
      keeps the old message; `pushed===0` alone (incomplete) gets a new one naming
      incompleteReason/incompleteDetail and stating "this is NOT a confirmed 'nothing new'". Re-ran
      the extraction post-fix on all 3 cases (charge-limit-incomplete, genuine-quiet,
      normal-delivery) -- correct, no regression.
      **Live check:** seeded a real 3-row watch baseline (contributions, donorEmployer=GOOGLE,
      state=AK, electionYear=2026), doctored one id out of the named KV record via the API, reran
      with a tiny `maxTotalChargeUsd` -- confirmed the general chargeLimitReached -> "Scan
      INCOMPLETE" path fires correctly. Could NOT isolate the exact `pushed===0` edge live:
      `maxTotalChargeUsd` on the runs API (query param and JSON body, both tried) was silently
      ignored (`isMaxTotalChargeUsdSetByUser` stayed `false`), so the existing row got charged
      before a limit could block it. Logged in LEARNINGS -- do not re-try the same two shapes; check
      whether an Actor Task or the Console UI's limit field is needed instead, if a future cycle
      wants to force `chargedCount:0` on the very first charge of a run. Test KV record deleted
      after. Build 0.1.79 (package 0.1.24 -> 0.1.25), live source byte-identical. README needed no
      change. `check-charges` 25/0, `check-pricing` 25/30/0, `node --check` clean. `audit_dates.json`
      recorded at 2263 with full note.
      ~$0.0015 spent (one build + two tiny live runs, 1 charged test result), 0 new Actors, revenue
      still $0 booked, no owner email warranted. One commit (`8b4f19e9`) pushed to `origin/main`.
      **Next `varied_test` target: `shopify-products-scraper` (2209, now fleet-oldest).**

- [x] **DONE cycle 2262 (MANDATED QUALITY/GROWTH slot -- `2262%3==0`, verified via
      `python3 -c "print(2262%3)"`) -- ran both PLAYBOOK QUALITY tools (both clean, recorded),
      then the fleet-oldest `varied_test` (`google-play-reviews-scraper`, 55c stale), which
      FOUND AND FIXED a real disclosure bug. Build 0.1.91 live and byte-verified.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all` both NONE DUE, inbox
      unchanged (10 known spam/DMARC/resolved items), services active, site 200 everywhere,
      `HEAD == origin/main` (`52500008`) and tree clean before edits.
      `check-disclosure` 87 posts + 23 dev.to articles / 0 missing (recorded, next due 2310);
      `devto-comments` 23 articles / 12 inbound / 0 unanswered (recorded, next due 2406). No
      support mail. dev.to cadence checked live: most recent post 2.2 days old, within cadence.
      **The bug:** in watch mode, the per-app app-details snapshot is pushed and counted in
      `pushed` like a review row, but the status message and `webhookUrl` payload both derived
      "new reviews" as `pushed - watchChanged` -- silently counting that app-detail row as a
      phantom "new review" whenever `includeAppDetails` (default **true**) was combined with
      `watchLabel` and any app had a delivery. First-ever test of this exact combination.
      Reproduced for $0 locally (real Spotify reviews via `CRAWLEE_STORAGE_DIR`): doctored the
      stored watch record (remove-a-reviewId for a "new" case, edit-a-score for a "changed"
      case, same KV method as c2207) to deterministically prove pre-fix overcounts: 2 reported
      as "new" when only 1 (or 0) really were. **Fix:** added `watchNewDelivered`, incremented
      only when a genuinely new review row is pushed (never for the app record or a changed
      row), and swapped both reporting paths to read it directly. Proved 3 paths for $0: new+
      app-record (now correct), changed+app-record (now correct), no-app-record (unaffected,
      regression-safe). README needed no change (names the field, makes no formula claim).
      Build 0.1.91 (0.1.28 -> 0.1.29), live source byte-identical (51493==51493). **Then
      reproduced the exact scenario on the REAL PLATFORM**, not just locally: seeded a live
      watch baseline, doctored the live named KV record via the API, reran -- log correctly
      said "1 new review(s)" for `pushed=2`, `chargedEventCounts {result:2}` matched exactly
      (checked twice, no charge leak -- disclosure bug only). Test KV record deleted after.
      `check-charges` 25/0, `check-pricing` 25/30/0, `node --check` clean. `audit_dates.json`
      recorded at 2262 with full note.
      ~$0.0004 spent (one build + two tiny capped live runs), 0 new Actors, revenue still $0
      booked, no owner email warranted. One commit (`8166d520`) pushed to `origin/main`.
      **Next `varied_test` target: `fec-campaign-finance-scraper` (2208, now fleet-oldest).**

- [x] **MEASURED cycle 2269 (c2260's own ask: measure the false-positive rate before
      registering) -- naive unit-word matching is far too noisy, do NOT register as-is.**
      Built `bin/_proto_numclaim.py` (prototype only, not in `state/fleet_checks.json`):
      number + nearest lowercase word within 2 tokens, grouped per-Actor across
      `.actor/input_schema.json` descriptions + `README.md`, flagged when a group's numbers
      disagree. Result: **343 flagged unit-groups out of 3,054 candidate claims across 26
      Actors** -- confirmed noisy. Three noise sources, not one: (1) pronouns/stopwords/spelled
      numbers misread as "units" (`them`/`this`/`now`/`one`/`two`/`three`/`four`); (2) worked
      FAQ examples and sample-output JSON legitimately cite different numbers next to the same
      noun (different hypothetical review/user counts, different sample timestamps); (3) nothing
      distinguishes a prose CLAIM from a number inside a ```json fixture or changelog entry.
      `check-meta-fields` avoids all three by anchoring to one fixed phrase template applied
      only to known claim fields -- it does not do open-ended "any number near any word"
      matching, which is the actual reason it stays clean. **If revisited:** enumerate the
      small set of real repeated-claim phrase templates fleet-wide first (`"max N <noun>"`,
      `"up to N <noun>"`, `"N <noun> seen"` appearing in BOTH a schema description and the
      README) and match only those, excluding fenced code blocks and FAQ worked-example
      sections of the README -- don't widen the matching window instead. Full write-up in
      LEARNINGS cycle 2269. `bin/_proto_numclaim.py` left in the repo as a harness for that
      narrower pass (same `_`-prefix one-off convention as the `_trimNNNN.py` scripts).

- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS warning in `check-upstream-warnings`.**
      Acks currently never expire. An ack written against a correct verification stays silent
      even if, 500 cycles later, we refactor the Actor back onto the dead upstream (unlikely) or
      the rival's warning becomes relevant to a DIFFERENT Actor of ours sharing that upstream.
      Cheap, bounded fix: print `ACK STALE (acked cNNNN, >672c ago -- re-verify)` next to any
      acked hit older than the longest audit interval, without changing the exit code. Only
      worth doing once there are >2 acks or the oldest crosses ~672 cycles (i.e. ~cycle 2868);
      noted now so the decision is deliberate rather than forgotten.

- [ ] **NEW follow-up (c2168, REWRITTEN c2268 -- the old wording named a leader on a metric
      that retracts) -- watch for the first real buyer. Do NOT watch the `users` column.**
      Decision rule, so a future cycle doesn't have to re-derive it: external runs are
      observable but earnings are NOT, so the escalation trigger is a **bookmark, a review, or
      `bin/traffic` buyer intent** (the CLAUDE.md Polar gate: >100 verified visits/day to
      /pricing or /tools), NOT a run-count or user-count climb. A climb alone must never
      trigger an owner email -- c2168 confirmed we cannot see earnings, so we could not
      substantiate a revenue claim even if we wanted to.
      **What c2268 changed and why:** the item used to say `trademark-search-scraper` "is the
      only Actor off the baseline and the only one at 3 users". Both halves were false by the
      time anyone read them. `state/revenue_history.json` shows `website-screenshot-scraper`
      went users 1->2->3->1 inside ~36h (10-19 23:00 .. 10-21 11:30) and
      `steam-reviews-scraper` 2->3->1 in 17h (10-22 16:00 .. 10-23 09:18) -- the field is not
      cumulative and not even monotone, so a +1 is no evidence a real user arrived. Today's
      numbers (re-derive, don't trust these): shopify-products-scraper 4 (since 10-24 16:03,
      fleet high), trademark-search-scraper 3 (since 10-23 09:18); `bkmk`/`rev` still 0 across
      all 25 Actors, and those two columns do not oscillate, which is why they are the usable
      ones. Full write-up in LEARNINGS c2268. `bin/traffic` this cycle: 11-24 verified
      views/DAY fleet-wide, 3 verified out_clicks total -- nowhere near the Polar gate.

- [ ] **STILL OPEN (carried from c2103, blocked on an external event): verify the DMARC
      receiver fix end-to-end on a genuinely NEW report.** Re-checked at c2133 after the doc
      trim moved its old entry to `queue_archive.md` -- re-stating here so it isn't lost.
      Newest DMARC mail is still `e2f3a358` / ts 1792145357, unchanged. Next cycle that sees a
      DMARC message with a timestamp newer than that: run `bin/dmarc-report` on it and confirm
      a real per-source pass/fail count comes back, not `0 source(s)`.

- [ ] **Process lesson to apply every cycle (found c2120).** Do NOT trust the previous cycle's
      "nothing audit-due" prediction -- c2119 wrote "NONE DUE fleet-wide" and one cycle later the
      7-day floor had made `google-play-reviews-scraper` due. Always re-run `bin/audit-due --all`
      and `bin/checks-due` yourself at the top of the cycle. (Cheap, read-only, local.)

