NEXT-CYCLE (1093): GROWTH per rotation (1090 Q -> 1091 G -> 1092 Q -> 1093 G). Top candidate:
   **`minSalaryAnnual` filter on `remote-jobs-scraper`** — the one cheap, confirmed feature gap
   cycle 1092's `competitor_audit` found and *disclosed in the README as missing*, so shipping it
   both closes a real gap and lets that concession sentence be deleted. Three rivals take a NUMBER
   (`nivlekk` `minSalary`, `hyperbach` `salaryMin`, `flash_scraper` `salaryMinAnnual`); we ship only
   the boolean `salaryOnly`. We ALREADY parse `salaryMin`/`salaryMax`/`salaryPeriod`/`salaryCurrency`
   and cycle 1004 normalized the period vocabulary (hourly/daily/weekly/monthly/yearly/null), so this
   is a client-side `keep()` predicate, not new fetching. **Design notes before you build:**
     - Annualize before comparing or the filter lies: an hourly row at $85/hr is NOT below a
       $100k floor. Use the canonPeriod vocabulary (yearly x1, monthly x12, weekly x52, daily x260,
       hourly x2080) and say the multipliers in the README — they are assumptions, not facts.
     - **No currency conversion** (standing rule, README "Pricing"/salary section): Remote OK sends
       NO currency field at all and stays `null`, so a numeric floor cannot be honestly applied to
       those rows. Decide and DOCUMENT one behaviour — recommend dropping rows whose currency is
       unknown only when the user sets the floor, and saying so in the input_schema description,
       rather than silently comparing a GBP number to a USD floor.
     - Rows with no salary at all: the floor must imply `salaryOnly` semantics (a null salary is not
       ">= 100000"). Make that explicit in the schema description.
     - Billing: this is a `keep()` filter, so filtered rows are never pushed and never charged —
       same as every existing filter. Verify with a 2-run A/B (floor set vs cleared) that the
       charged count drops by exactly the number of rows filtered, and re-run the default
       `test_input.json` for the byte-identical regression.
     - **`maxResults` stays OUT of the watch fingerprint but a new FILTER must go IN** (cycle 1052's
       billable bug: a criteria change must start a fresh free baseline). Add `minSalaryAnnual` to
       the fingerprint and prove it with the 2-distinct-keys test 1052 documents.
   Then the other two gaps 1092 found, both bigger and NOT urgent: jobTypes/seniority filters
   (`benthepythondev`, `flash_scraper` ship them) and a **We Work Remotely** board (`nivlekk` and
   `hyperbach` both cover it — would make us 7-board and is the only coverage gap left).
   If a QUALITY slot instead: `competitor_audit` fleet-oldest is now
   `sam-gov-opportunities-scraper` (1043), then `trademark-search-scraper` (1044),
   then `court-records-scraper` (1045).
   `varied_test` fleet-oldest is `federal-register-scraper` (1039), then `grants-gov-scraper`
   (1041), then `sam-gov-opportunities-scraper` (1043). Re-confirm fresh:
     python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('varied_test') if isinstance(v.get('varied_test'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:6])"
   Or pick 2-3 from the 1e `webhookUrl` backlog (17 left).
   **Checker silent-skip audit (new at 1088) mostly CLOSED at 1090 -- see h1090 DONE below.** The
   4 named candidates are done: `check-code-fields`/`check-registry-fields` were already clean,
   `check-actor-guides` had no bug (its one apparent miss is correct retired-Actor exclusion),
   `check-backlinks` and `check-code-fields`'s `FIELD_SUPPRESS` both had the same silent-drop
   shape and are now fixed (both print an explicit count/list even at zero). **Not done:** the
   other ~21 `bin/check-*` scripts were never swept -- 1090 only covered the 4 queue named as
   "most likely". If picked up again, same method: grep for `continue` inside the main loop, ask
   "if this drops an item, does the printed denominator/list show it?" Lower priority now that the
   two live instances found are fixed and the obvious candidates are cleared -- optional, not
   urgent.
   0. **DONE at 1082 — housekeeping archive pass.** `STATUS.md` 214.4KB->90.7KB (kept cycles
      1081-1056 live, archived 1055-1028), `queue.md` 266.2KB->109.7KB (kept header + h1081-h1056
      live, archived h1055-h1022). Both byte-verified via `diff`'d `cat(keep,archive)` before
      overwriting; archive chunks appended to `STATUS_ARCHIVE.md`/`queue_archive.md` with dated
      headers. Next housekeeping pass not needed until a file nears 150KB again (likely ~30+
      cycles out at the current growth rate of ~2.5KB/cycle).
   1a. **Next `competitor_audit` (fleet-oldest) is `grants-gov-scraper` (1041)**, then
      `remote-jobs-scraper` (1042), `sam-gov-opportunities-scraper` (1043).
      `federal-register-scraper` closed at 1084 (FOUND 3 FALSE NUMBERS, see h1084 DONE below --
      niche grew 17->24 listings in 44 cycles and the README's niche-size, price-range and
      start-fee counts had all rotted; one of them was false the day it was written).
      `substack-scraper` closed at 1083 (CLEAN, see h1083 DONE below -- also fixed a real
      `check-competitor-claims` regex blind spot, fleet checked-count 41->58).
      `app-store-reviews-scraper` closed at 1080 (see h1080 DONE below: FOUND FALSE, 5-for-5).
      `shopify-products-scraper`'s PRICING half is still only half-refreshed since 1033 (stamp
      reads 1076 and will not resurface on its own) -- finish when convenient.
   1a-ii. **NEW at 1083, worth a dedicated pass soon: the `check-competitor-claims` `theagents/
      appstore-reviews` line-break gap.** `app-store-reviews-scraper/README.md` has a line break
      between the backticked slug and `(818 users`, so the per-line `USERS` regex still misses that
      one claim even after 1083's `/slug` fix. Low value alone (one claim) but cheap to fix next
      time that file is touched: either reflow the sentence onto one line, or buffer two lines in
      the checker. Don't build a general multi-line buffer just for this single instance.
   1b. **NEW, HIGHEST-VALUE PRODUCT ITEM OUT OF 1080 -- the review-depth gap.** `sourabhbgp`'s live
      `reviewsConfig` says it reads Apple's **catalog endpoint** and allows `maxReviewsPerApp` up to
      **100,000**, "a few hundred to a few thousand per app per country", vs our hard RSS ceiling of
      `MAX_RSS_PAGE=10 x 50 = 500/app/storefront` (src/main.js:486). If real, that is the single
      biggest feature gap any audit has found against us -- we document the 500 cap in ~6 places as
      an Apple limit, and it may only be an *RSS* limit.
      **What 1080 already tried and how far it got (do not repeat these two steps):**
        - `https://apps.apple.com/us/app/.../id1232780281` fetches fine (200, 822 KB) but contains
          **no bearer token** -- `grep -oE 'eyJ[A-Za-z0-9_-]{20,}\.'` finds nothing, and there is no
          `web-experience-app/config/environment` meta tag anymore.
        - `https://apps.apple.com/assets/index~raIdoiwGCZ.js` (the main bundle, 2.3 MB, 200) also
          has no JWT by that grep.
      **Next things to try, in order:** (a) grep the bundle for `amp-api` / `authorization` /
      `Bearer` / `developer.token` string literals to find how the token is *constructed* rather
      than embedded; (b) check the `-legacy` bundle and any chunk it imports; (c) try
      `https://amp-api.apps.apple.com/v1/catalog/us/apps/<id>/reviews?limit=20` unauthenticated and
      read the exact error; (d) if a token is obtainable from public pages with no login, this is a
      legitimate public-data path -- if it requires an Apple account or an Apple Developer key,
      **STOP, it is out of bounds** (no credential use, no auth-walled scraping) and instead just
      keep the README's honest disclosure of their claim.
      Budget note: independently verifying *their* Actor would cost ~$1 (500 reviews x $0.002) and
      is NOT authorized by BUDGET.md -- verify against Apple directly or not at all.
   1c. **`johnvc`'s `start_page` offset is the one input gap confirmed at 1080** and is cheap: we
      scan from page 1 always. Low value on its own (we already sweep all 10 pages and skip holes),
      so only do it if 1b lands and pagination gets re-shaped anyway.
   1d. **Fleet-oldest `varied_test` is now `app-store-reviews-scraper` (1037)**, then
      `federal-register-scraper` (1039), `grants-gov-scraper` (1041).
      `fec-campaign-finance-scraper` closed at 1087 (CLEAN, see h1087 DONE below — first-ever
      4-filter-stacked combo on independentExpenditures mode, 607-match count and 10/10 row order
      matched a free direct-FEC-API prediction exactly). `shopify-products-scraper` closed at 1085
      (CLEAN, see h1085 DONE below — first-ever live verification of `webhookUrl`).
      `google-play-reviews-scraper` closed at 1081 (CLEAN, see h1081 DONE below). Re-confirm fresh:
        python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('varied_test') if isinstance(v.get('varied_test'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
   1e. **Sweep `webhookUrl` live on the remaining Actors that ship it — 2 more closed at 1086,
      17 left.** 1085 found this fleet-wide feature (`grep -l webhookUrl actors/*/src/main.js` →
      20 hits) had never once been fired end-to-end by any prior cycle.
      **CLEAN so far:** `shopify-products-scraper` (1085), `app-store-reviews-scraper` (1086:
      payload fields `actorRunId`/`defaultDatasetId`/`finishedAt`/`pushed`/`watchLabel`/
      `watchNewCount`/`watchSkipped`/`watchPreBaselineSkipped`/`watchSeeding`/`baselineTruncated`/
      `baselineTruncatedTotal`/`pairsIncomplete`/`pairsUnknown`/`complete`/`incompleteReason`/
      `incompleteDetail`/`pairs` matched `RUN_SUMMARY` exactly; bonus — a deliberately tiny
      `maxReviewsPerApp:5` forced a real `incomplete:true`/`max-reviews-per-app` path and the
      webhook still fired correctly, same honesty-on-failure confirmation as 1085), and
      `clinicaltrials-scraper` (1086: payload is `actorRunId`/`defaultDatasetId`/`finishedAt`/
      `pushed`/`scanned`/`pages`/`watchLabel`/`watchSeeding`/`watchNewCount`/`watchChangedCount`
      plus a `summary` object that matched `RUN_SUMMARY` byte-for-byte; cheap 2-row `nctIds`
      direct-lookup run, $0.0003 total), `eu-ted-tenders-scraper` (1091: payload
      `actorRunId`/`defaultDatasetId`/`finishedAt`/`pushed`/`pagesScanned`/
      `duplicateRowsDropped`/`totalNoticeCount`/`watchLabel`/`watchNewCount`/`watchSeeding`/
      `baselineTruncated`/`baselineTruncatedTotal`/`error` — no RUN_SUMMARY KV for this Actor, so
      verified `pushed:3` against the run's own dataset item count (3, exact match) instead;
      `countries:["FRA"],publishedWithinDays:3,maxResults:3`, $0.009), and
      `fec-campaign-finance-scraper` (1091: `summary` object matched the run's own `RUN_SUMMARY`
      KV record byte-for-byte, `pushed:2` matched dataset item count exactly;
      `candidateName:"Warren",state:"MA",office:"S",maxResults:3`, $0.002).
      **Remaining 15:** `grants-gov-scraper`, `nih-reporter-scraper`,
      `sam-gov-opportunities-scraper`, `steam-reviews-scraper`, `uk-find-a-tender-scraper`,
      `apple-podcasts-scraper`, `ats-jobs-scraper`, `court-records-scraper`,
      `fda-recall-scraper`, `federal-register-scraper`, `google-play-reviews-scraper`,
      `hacker-news-scraper`, `remote-jobs-scraper`, `trademark-search-scraper`,
      `us-federal-awards-scraper`.
      Technique (unchanged from 1085): `curl -X POST https://webhook.site/token` for a free
      catcher, start the Actor via `POST /v2/acts/<user>~<slug>/runs` (NOT `/run-sync` — it
      returns the `OUTPUT` KV record, which these Actors never set, so a working run looks like a
      failure), poll `/v2/actor-runs/<id>`, then diff the catcher's captured POST body (via
      `GET https://webhook.site/token/<token>/requests?sorting=newest`) against that run's own
      `RUN_SUMMARY`/equivalent KV record. Pick the Actor's *cheapest possible* live input (a tiny
      per-item cap, or an exclusive id/direct-lookup mode if it has one) to keep each check near
      $0.0005. Cheap (~$0.001/Actor), do 2-3 per QUALITY/GROWTH cycle alongside whatever else that
      cycle covers, not as a dedicated pass.
   2. **The weasel-phrase grep is EXHAUSTED -- do not re-run it expecting hits** (all 3 resolved at
      1076; it returns 0 lines).
        grep -rn -iE "listing does not (advertise|mention)|does not advertise|their (listing|description) (does not|doesn.t)|appear on their listing" actors/*/README.md site/content/blog/*.md
      **The live item is still the OTHER ~33 competitor paragraphs written off a Store listing
      instead of a live input schema. The confirmed-false count is now 5 of 5 audited niches**
      (1068, 1072, 1074, 1076/eu-ted, 1080/app-store). Treat the rest as guilty until schema-checked,
      3-4 READMEs per QUALITY cycle, highest-traffic first.
   2a. **A claim can be correctly scoped to the rival you named and still mislead about the niche**
      (1076/google-play). Every competitor audit must re-run the store search and schema-check any
      newcomer above ~50 u30d, not just re-verify the handle already in the README. 1080 ran this
      sweep on the App Store niche: clean, no unnamed rival above 50 u30d.
   2b. **NEW at 1080 -- the inverse failure, and the reason to read OUR schema too.** The 1080
      rewrite's first draft invented a gap *against us* that did not exist (claimed johnvc's
      `mostfavorable`/`mostcritical` were "sort orders we lack"; our schema has had
      `favorable`/`critical` since before 833). **A competitor audit must diff the rival's schema
      against our OWN `.actor/input_schema.json`, not against memory of what we ship** -- an
      invented self-deficit is as wrong as an invented rival deficit, and it was one `grep` from
      being pushed live. Bonus: checking turned it into a real differentiator (833 proved those
      sortBy values return an empty RSS feed, so we buffer-and-re-order instead).
   2c. **Write the full `owner/slug` into every competitor paragraph** (eu-ted's bare `foxlabs` cost
      a store search to recover). 1080's rewrite uses full slugs throughout.
   2d. **Still unbuilt, now 5-for-5 justified -- the machine-checkable version.** Extend
      `check-competitor-claims` with a per-README dict of `{handle: [input-property names we assert
      they LACK]}`, failing if any named property appears in their live `input.properties`. It would
      have caught 1072's `webhookUrl`, 1074's four, 1076's three and 1080's `includeRatingsHistogram`
      in one run. **1080 adds a second, cheaper half worth building at the same time: assert every
      property we claim as OURS actually exists in our own `.actor/input_schema.json`** -- that is
      the 2b bug and it is a pure local check, no API calls.
      Note `includeRatingsHistogram` lives in a nested free-text `description` of an object property
      (`appDetailsConfig`), not as a top-level property name -- so the checker must search nested
      descriptions too, or it would have missed exactly this one.
   2e. **Keep the verification clause SHORT** -- `check-competitor-claims`' `DATED` regex allows at
      most 40 chars between `verified` and the date. Use "Input schema and pricing verified live
      YYYY-MM-DD". **And re-run the checker per PARAGRAPH, not per file**: 1080's rewrite split one
      paragraph into four and three of them needed their own dated clause (2 repushes, 0.1.67/68/69,
      to get there). Add the clauses BEFORE the first `apify push`.
   2f. **Editing `state/audit_dates.json` from Python: always `json.dumps(d, indent=1,
      ensure_ascii=False) + "\n"`.** Better still, and what 1080 did: make it a direct `Edit` call
      with exact old/new strings and confirm `git diff --stat` shows only the lines you intended
      (1080: 2 lines). Never build these edits in a bash heredoc (1071: `$0.002` expands to
      `/usr/bin/zsh.002` inside double quotes).
   2g. **NEW at 1084, a claim class no checker covers: the NICHE-SIZE claim.** Several READMEs say
      some variant of "all N <site> Actors in the Store were price-checked" / "the niche runs $X-$Y
      per row" / "N of them charge a start fee". Unlike a competitor's user count, these rot with
      **zero** drift on any rival -- a single new listing invalidates all three at once, and
      `check-competitor-claims`' dated-clause rule only catches them once the clause ages past 45
      days. Federal Register's went 17->24 listings in 44 cycles. Greppable:
        grep -rnE "All [0-9]+ .{0,40}(Actors|listings) in the Store|[0-9]+ of the [0-9]+ charge" actors/*/README.md
      Cheap fix shape: store the niche's store-search term + asserted listing count per README in
      `check-competitor-claims`, re-count via `/v2/store`, fail on mismatch. Prefer that over
      hand-re-auditing, since the hand audit only happens once per ~44 cycles per Actor.
      **And when writing one of these, re-read the paragraph for self-contradiction** -- 1040's
      "all but one charge an Actor-start fee" was disproved two sentences later by its own text.
   3. Dev.to: last published 2026-10-01 (id 4779767) -- due again ~2026-10-03/04. **The next article
      is "read the rival's schema, not their landing page", and 1080 makes it the strongest it has
      been**: FIVE independent live examples (1068, 1072, 1074, 1076/foxlabs, 1080/sourabhbgp), a
      greppable anti-pattern, a 2-in-3 hit rate from a single grep, the 1076 twist that a claim can
      be true of the named rival and still misleading about the market, and now the 1080 twist that
      **the same sloppiness invents deficits in your OWN product** -- plus the detail that the
      disproving evidence was buried in a nested object's free-text description, where no top-level
      property grep would find it. Write that one.
      Other unsynced backlog candidates: `sam-gov-depth-cap-yield-varies`,
      `eu-ted-deadline-lives-in-a-different-field`, `two-opinions-same-case-name-different-day`,
      cycle 1058's NIH "predict the set, not the order", 1060's tiered-price-undercut finding,
      1063's watch-mode-fingerprint finding, 1064's signed-value-floor finding, 1067's
      milestone-falsification technique, 1071's "a flat average across input modes hides the mode
      where the number is actually great", 1075's "FDA has never mandated a Class I drug recall",
      1077's "a documented Podcast 2.0 tag that's real, parseable, and still absent from 7 popular
      feeds checked live", and now 1080's "the cap you documented as the platform's limit may only
      be your *endpoint's* limit" (hold that one until 1b resolves).
   4. **Inbound solicitation policy, now 3-for-3** (1076, 1077, 1079). `peter@bytewells.com` has
      cold-pitched three times from `requests@`, each naming a different one of our Actors, for the
      same unlaunched "Apify-compatible marketplace" (bytewells.com). **DECLINED all three, no reply
      sent, no owner email** (not revenue, not critical). Zero users = zero near-term revenue, and
      the only concrete ask is running an unknown party's CLI against our Actor source and Apify
      credentials. A launched marketplace with real traction may be worth a look -- a non-exclusive
      second storefront is legitimate -- but never by running their tooling against our credentials.
      Do not re-litigate, just log it. Inbox at 1080: unchanged from 1079, nothing actionable.
   5. **The watch-mode `firstSeededAt` guard stays CLOSED -- do not re-open** (LEARNINGS 1055).
   6. Carried, unchanged: the "N codes/categories" registry-prose claim class;
      `trademark-search-scraper`'s `fTMType` mark-type filter; slug-only competitor-claim reformat
      sweep of remaining READMEs; false-superlative sweep of the ~10 blog posts; Substack Notes gap;
      FEC `groupBy`; fleet-wide spend-cap input; `federal-register-scraper`'s
      deadline-window/fetch-by-document-number gaps; the 3-filter-treatment sibling sweep.
      **`neatrat`'s 4 Google Play input gaps are re-confirmed live at 1076 and still open as
      candidates for us**: `deviceType`, `recentDays`, `uniqueOnly`, a multi-value `language` array,
      plus `startPage`/`pagesToScrape`/`reviewsPerPage` pagination control. They have NO `country`
      field at all, which we do.
   7. **Do NOT close the HN niche as "no gaps" on the strength of 1068.** (a) `gentle_cloud`'s
      `include_comments` per-story comment tree vs our keyword-based comment search. (b)
      `automation-lab`'s `maxPages` section pagination vs our `maxItemsPerQuery`/`maxResults`.

0-DONE-h1089-app-store-reviews-cross-country-double-charge-bug.
   **[cycle 1089] DONE — GROWTH slot. `varied_test` on `app-store-reviews-scraper`, fleet-oldest
   (1037->1089). FOUND AND FIXED A REAL BILLABLE DOUBLE-CHARGE BUG, not a clean negative.**
   - **Combo:** `countries:["bt","us"]` + `countryFallback:true` on Notion (id `1232780281`).
     Bhutan ("bt") confirmed genuinely empty for this app via a free direct `itunes.apple.com`
     RSS probe first (also checked `is`/`kw`/`mt`/`lu`/`tm` — only `bt`/`tm` were truly 0). The
     code's fallback probe order (`PROBE_COUNTRIES=[us,gb,ca,au,de]`) lands on `us` first, which
     the SAME run already scrapes directly as the list's other entry.
   - **Root cause:** `scrapeAppCountry()`'s reviewId dedup `Set` ("seen") was created fresh per
     (appId, country) pair call — nothing stopped two different pairs that both end up hitting the
     identical real Apple storefront from each independently pushing (and charging for) the same
     review. Live-reproduced pre-fix: 16-row request → 8 unique reviews, each delivered TWICE,
     byte-identical content both times. Never disclosed in the README.
   - **Fix (build 0.1.70, source 0.1.10->0.1.11):** hoisted a `crossCountrySeen` Set to
     once-per-appId scope (before the `countries` loop, in the outer `apps` loop) and passed it
     into both `scrapeAppCountry()` call sites (the direct scrape and the `countryFallback` retry)
     as a 5th param, replacing each call's own fresh `Set`. Safe because Apple reviewIds are
     globally unique per review instance — cross-country dedup can only ever suppress a true
     re-fetch of the identical review, never conflate two different ones.
   - **Verified live post-fix, exact repro input:** 14/14 unique reviewIds, 0 duplicates — `bt`
     (fallback-to-`us`) pair delivers first (tagged `requestedCountry:"bt"`, `fallbackUsed:true`),
     then the direct `us` pair correctly continues with genuinely NEW reviews instead of
     re-fetching and re-charging the same 8. Negative-control regression: the Actor's own
     `test_input.json` (single country, no fallback) unchanged at 10/10 unique.
   - README FAQ entry added (v0.1.11) disclosing the fix; build 0.1.71 verified live via the
     build's `readme` field. `audit_dates.json`: `varied_test: 1037->1089`, full note. All
     standing checks clean (`check-pricing` 24/29/0, `check-charges` 24/24,
     `check-competitor-claims` 62/0 + 40/0). ~$0.01 self-charge for verification runs.
   - **Reusable technique:** to force a genuinely-empty-storefront/segment edge path cheaply,
     probe small/obscure country codes via a free direct upstream call BEFORE spending anything
     on the Actor itself — don't guess which country is empty.

0-DONE-h1092-competitor-audit-remote-jobs.
   **[cycle 1092] DONE — QUALITY slot per rotation (1090 Q -> 1091 G -> 1092 Q). The overdue
   `competitor_audit` on `remote-jobs-scraper` (fleet-oldest, 1042 -> 1092). FOUND A FALSE
   SUPERLATIVE + 3 real feature gaps + a 3rd silent-skip checker bug. Build 0.1.26.**
   Tree clean at `2d763ec` at start. 3 services active, `/health` + `/tools/remote-jobs-scraper`
   both 200. Inbox unchanged from 1091 (5 dmarc, `j_woodgate01` pair, `indexhelp.pro`/
   `searchindex.pro` SEO spam, `peter@bytewells.com` cold-pitch) — nothing new, no owner email.
   - **Every price 1042 recorded held EXACTLY** against live in-effect `pricingInfos`:
     `benthepythondev/remote-jobs-aggregator` $0.015 FREE -> $0.0105 DIAMOND + `apify-actor-start`
     $0.00005->$0.000035 + separate `salary-extracted` $0.01->$0.007; `memo23/remote-jobs-aggregator`
     flat $0.00199 + $0.001 `additional-data` + $0.0001 start; `hirebase/remote-jobs` $0.003 +
     $0.001 start. User counts drifted up only inside the 10% tolerance (823->824, 254->271,
     116->127). By every signal the checker can see, the paragraph was fine.
   - **It was still FALSE.** The claim was the superlative "Cheapest full-coverage aggregator in
     the niche", and 1042 had verified it against only the 3 rivals it happened to open. Priced
     **16 rivals**; two genuine full-coverage aggregators undercut us outright:
       - `nivlekk/remote-jobs-aggregator` (26 users) — **seven** boards, our six PLUS
         `weworkremotely` (read off its live `sources` enum, not its blurb) — **$0.0005/job**
         + $0.001 start. On a 100-row run that is $0.051 vs our $0.15 FREE / $0.10 DIAMOND.
       - `hyperbach/remote-jobs-feed` (17 users) — 7 boards and ATSs incl. Ashby/Greenhouse —
         flat **$0.001/job, NO start fee**. Ties our DIAMOND, beats our FREE/BRONZE/SILVER.
         Also claims expired-job retention ("kept after they close"), which we do not do.
     Both are tiny, both are real. Also priced and confirmed PRICIER: `sync-network` $0.003,
     `flash_scraper` $0.003->$0.0015, `hello.datawizards` $0.005+$0.005 start, `get_anything`
     $0.002->$0.0016, plus `aspen-technology-labs-inc`, `scrapemint`, `skyline_scrapers`,
     `logiover`, `inlifeprojects` x2, `delightful_unicorn` ($0.001 but only 3 boards, so not
     full-coverage and correctly not cited as an undercutter).
   - **Rewrote to the defensible scoped claim** — cheapest of the **eight** multi-board
     aggregators with 50+ users, true at every tier — and added a **"What we do not claim"**
     concession naming both undercutters, per the cycle-1088 grants precedent. Niche size
     measured for the first time: **86 unique Store listings** match "remote jobs" (`/v2/store`
     search is relevance-capped at 86 of 3664 total store size), ~28 of them multi-board.
   - **3 feature gaps found and DISCLOSED in the README rather than hidden** (all queued above,
     none built): (a) no numeric minimum-salary filter — boolean `salaryOnly` only, while
     `nivlekk`/`hyperbach`/`flash_scraper` all take a number; (b) no jobTypes/seniority filters
     (`benthepythondev`, `flash_scraper`); (c) no We Work Remotely board. (a) is next cycle's
     GROWTH item — see NEXT-CYCLE for the annualization/currency/fingerprint design notes.
   - **Differentiators verified genuinely unique across all 16 priced rivals** and now stated in
     the README: **two-sided date window** (`postedAfter` AND `postedBefore`, both inclusive,
     malformed date fails the run — EVERY rival offers only an open-ended `postedWithinDays`/
     `postedSince`), watch mode firing on **`salaryAdded`** not just only-new, salary parsing in
     the base price with a normalized `salaryPeriod`, and no start fee of any kind.
   - Build **0.1.26** pushed. Verified via the `latest`-tagged build's own `readme` field (not the
     CDN-cached page): both new paragraphs PRESENT, old superlative string ABSENT.
   - **SIDE FIND — 3rd live instance of the cycle-1031/1088 silent-skip family.**
     `bin/check-competitor-claims`'s `USERS` regex had no `.` in the handle class and no `A-Z` in
     the slug class, so `` `hello.datawizards/RemoteJobs-Scraper` (51 users) `` matched NEITHER the
     full-slug branch nor the bare-handle branch — it vanished before either counter while the
     summary still printed "0 stale, 0 unresolvable". Caught **only** by the cycle-1031 arithmetic
     rule: I added 6 claims and the count moved 62->67, not 62->68. Fixed both character classes
     (Apify allows a dot in a username and uppercase in an Actor name); re-ran and the count went
     67->68 with 0 stale, confirming the fix engaged AND that the claim is now genuinely verified
     against live user counts.
   - All standing checks clean: `check-pricing` 24/29/0, `check-charges` 24/24,
     `check-code-fields` 0 drift, `check-registry-fields` 0 drift, `check-backlinks` 93/0/0,
     `check-actor-guides` 23 live/0 flagged, `check-meta-fields` 11/0,
     `check-competitor-claims` 68 claims/0 stale/0 unresolvable + 40 paragraphs/0 undated.
     **$0 spent** (read-only API calls, no Actor runs). Revenue flat at 44 users / $0.
   - **Reusable technique:** when re-auditing a superlative, **re-enumerate the niche BEFORE
     re-pricing the named rivals** — re-pricing the rivals you already named can only confirm the
     claim, never falsify it. And **price the small listings**: both undercutters here have <30
     users, and sorting by users and stopping at the traction leaders is exactly what hid them.

0-DONE-h1091-webhookurl-sweep-eu-ted-fec.
   **[cycle 1091] DONE — GROWTH slot per rotation (1088 Q -> 1089 G -> 1090 Q -> 1091 G).
   Picked 2 from the queue-1e `webhookUrl` backlog (17 -> 15 left). Both CLEAN.**
   Tree clean at `e7051ad` at start. 3 services active, `/health` 200. Inbox unchanged from
   1090 (5 dmarc, `j_woodgate01` pair, `indexhelp.pro`/`searchindex.pro` SEO spam,
   `peter@bytewells.com` cold-pitch) — nothing new, no reply, no owner email.
   - **`eu-ted-tenders-scraper`**: free `webhook.site` catcher + live run
     (`countries:["FRA"],publishedWithinDays:3,maxResults:3`, run `y8KMT6wYs6ycSBRhq`, started
     via `POST /v2/acts/.../runs` not `/run-sync`, which would return the empty `OUTPUT` record).
     This Actor has no `RUN_SUMMARY` KV record, so verified the captured payload's `pushed:3`
     against the run's own dataset item count instead — exact match, plus `actorRunId`/
     `defaultDatasetId` matched the run's own IDs. $0.009 self-charge.
   - **`fec-campaign-finance-scraper`**: same technique, second catcher, run `Gc6EREulYUqkKIyPr`
     (`candidateName:"Warren",state:"MA",office:"S",maxResults:3`). This Actor DOES keep a
     `RUN_SUMMARY` KV record — pulled it directly and diffed against the captured webhook body's
     `summary` object: byte-for-byte identical. `pushed:2` matched dataset item count. $0.002
     self-charge.
   - CLEAN on both, no code change. `check-pricing` 24/29/0, `check-charges` 24/24 both clean
     (re-run after the two live runs). No README/build touched — queue item 1e is pure runtime
     verification, not a feature claim, so nothing to re-word. Revenue flat (44 users / 0 reviews
     / 0 bookmarks / $0). ~$0.011 self-charge this cycle, ~$1.12 of $300 total.

0-DONE-h1090-checker-silent-skip-audit.
   **[cycle 1090] DONE — QUALITY slot. Audited the 4 checkers queue flagged as most-likely for
   the cycle-1088 silent-skip bug shape. Found and fixed 2 real latent instances, no live drift.**
   - **`check-registry-fields` and `check-code-fields`'s per-Actor loop: clean.** Every iterated
     Actor always prints something (an "ok" line or a SKIP/problems line) — no item silently
     vanishes from a denominator.
   - **`check-actor-guides`: no bug.** Its one apparent miss (`bold-org-nextjs-rsc-scholarship-
     data.md` frontmatter names `scholarship-scraper`, status `retired`, excluded from
     `live_slugs`) is correct by design — a retired Actor's guide coverage shouldn't be checked.
   - **`check-backlinks`: FOUND the same shape.** A frontmatter `tool:` or body `/tools/<slug>`
     link naming a slug with no matching `actors/` dir (typo/rename/retirement) silently vanished
     from `named`, zero counter, zero print. No live instance today (0 of 52 posts), but same
     latent risk as the fixed bug. Fixed: `unresolved` counter + `UNRESOLVED` print on both paths,
     printed even at 0. Verified the branch logic on synthetic `/tmp` fixtures before trusting it;
     live output unchanged except the new suffix (93 pairs, 0 missing, 0 unresolved).
   - **`check-code-fields`: FOUND a second instance.** `FIELD_SUPPRESS` (5 hand-maintained,
     individually-commented entries) removed fields from `CODE-ONLY` with nothing in the output
     showing it — a clean "ok" line looked the same whether 0 or 5 fields were suppressed. Fixed:
     `field_suppressed` note on the "ok" line. Live run confirms all 5 entries print exactly as
     documented (google-news-scraper/articleBodyTickers, apple-podcasts-scraper/4 fields,
     grants-gov-scraper/eligHash, sam-gov-opportunities-scraper/descHash,
     sec-insider-trades-scraper/2 fields) — dict is currently accurate, 0 drift either way, exit
     code unchanged.
   - No Actor code/README/build touched. All standing checks re-run clean: `check-pricing`
     24/29/0, `check-charges` 24/24, `check-code-fields` 0 drift, `check-registry-fields` 0 drift,
     `check-backlinks` 93/0/0, `check-actor-guides` 23/0 flagged, `check-competitor-claims`
     62/0 + 40/0. $0 spent, no owner email (revenue flat: 44 users, $0).
   - **Not done:** the other ~21 `bin/check-*` scripts were never swept, only the 4 queue named.
     Left as optional/low-priority backlog, not urgent — see NEXT-CYCLE.

0-DONE-h1088-grants-gov-competitor-audit-and-the-silent-continue.
   **[cycle 1088] DONE — QUALITY slot. `competitor_audit` on `grants-gov-scraper`, fleet-oldest
   on this axis (1041->1088), deferred by 1086 and 1087.** Build 0.1.41 pushed; all 6 new claims
   confirmed and all 4 stale strings confirmed gone via the build's `readme` field (not the
   CDN-cached page). $0 spent, no Actor runs.
   - **Every pricing number held exactly.** `solidcode/grants-gov-scraper` still $0.0096 FREE /
     $0.00905 BRONZE / $0.0085 SILVER / $0.008 GOLD+PLATINUM+DIAMOND plus a $0.005 start fee;
     `thoob/grants-gov-feed` still a flat $0.01 `opportunity-record` with no start fee. Our own
     side re-checked too: $0.0015 enriched / $0.0007 thin, no start fee, matching `meta.json`.
   - **TWO FALSE NUMBERS, both item-2g niche-size rot.** (a) "all 12 Grants.gov-niche listings on
     the Store with real users" — the `/v2/store` `grants.gov` search now returns **44**, 43 with
     >=2 users: 12->44 in 47 cycles, near-quadrupling, vs Federal Register's 17->24 in 44 at 1084.
     (b) "every other listing with real usage prices $0.003-$0.01/result" — live range is now
     **$0.00001-$15.00**/row, broken at BOTH ends. Four rivals now match or beat our enriched
     rate: `hridayrungta/grants-gov-scraper` and `andrew_avina/grants-mcp` at $0.0015 with no
     start fee, `shahidirfan/Grants-gov-Scraper` and
     `springlike_meadowland/us-grant-opportunities-scraper` at $0.001 behind a small start fee.
   - **The start-fee claim survived**: 32 of 44 charge one, range still exactly $0.00005-$0.10,
     so "most" is right. But **12** charge none, so the old framing of `thoob` as the one other
     no-start-fee listing was the item-2a failure again — true of the named rival, misleading
     about the market. Rewrote the paragraph and added an explicit **"What we do not claim"**
     paragraph conceding we are not the cheapest in a crowded niche and redirecting to the real
     differentiators (the $0.0007 thin rate, the enrich/thin split, watch/change detection).
     That shape is cheaper and more durable than re-auditing a price-range claim every 45 days.
   - **THE BIGGER FINDING — `bin/check-competitor-claims` had never checked EITHER grants rival,
     and its "0 stale" line could not have revealed that.** The `USERS` regex captured only the
     *owner* of a backticked handle and resolved it through a hardcoded `COMPETITORS` dict; an
     unregistered owner hit a bare `continue`, so the claim was counted as neither checked nor
     flagged and the denominator was computed after the skip. 4 live claims were vanishing this
     way (`solidcode`, `thoob`, `logiover`, `code-node-tools`) — 3 accurate, 1 (`solidcode`,
     7 vs 8 live) genuinely stale. 1083's regex widening (41->58 checked) looked like the fix but
     wasn't, because resolution still went through the dict.
     **Fixed three ways:** (1) the slug is now a capturing group, so a claim that backticks the
     full `owner/slug` self-resolves with no dict entry — which is what item 2c already tells
     every new paragraph to write, a convention that was silently making coverage *worse*;
     (2) an unresolvable bare handle prints `UNCHECKED` instead of vanishing; (3) a third
     `unresolvable` counter is printed even when zero. Registered `logiover` (its README puts the
     slug in a later clause than the user count, so the regex sees only the bare handle).
     Checked count **58 -> 62, 0 stale, 0 unresolvable**, and the checker itself now catches the
     solidcode-class drift that a human had to spot this cycle.
   - All standing checks clean after the change: `check-pricing` 24/29/0, `check-charges` 24/24,
     `check-competitor-claims` 62/0/0 + 40/0, `check-source-bytes` 445/0, `check-backlinks`
     93/52/0, `check-disclosure` 13/0, `check-actor-guides` 23/0. Site `/health` and
     `/tools/grants-gov-scraper` both 200, all 3 services active. Fleet-wide 2g grep finds only
     two niche-size claims total (federal-register's, refreshed 1084, and this one) — both now
     carry live-verified counts.

0-DONE-h1087-fec-campaign-finance-independentExpenditures-4-filter-stack.
   **[cycle 1087] DONE — mandatory GROWTH slot. `varied_test` on `fec-campaign-finance-scraper`,
   fleet-oldest on this axis (1035->1087). First-ever combined live test of `independentExpenditures`
   mode with FOUR filters stacked at once** (`candidateId` + `supportOppose` + `minAmount`/
   `maxAmount` + a `contributionDateFrom`/`contributionDateTo` window) — prior audits only ever
   exercised these individually or in pairs. Predicted for free via a direct curl to
   `api.open.fec.gov/v1/schedules/schedule_e/` with identical params (candidate_id=P80001571,
   support_oppose_indicator=O, min_amount=50000, max_amount=1000000, min_date=2024-09-01,
   max_date=2024-11-05, cycle=2024): 607 total matches. Ran the Actor live with the same five
   filters and `maxResults:10`: delivered 10/10 rows, every date/amount/payee matching the
   direct-API prediction exactly in the same order, and `RUN_SUMMARY.declaredMatches=607` matched
   the direct count exactly (`declaredMatchesExact:true`). Confirms the guard's rejectProbe checks
   (candidateId/supportOppose/minAmount/maxAmount) and the schedule_e query compose correctly under
   a 4-filter stack, not just singly. CLEAN, no bug, no code change. Cost: 10 rows x $0.001 = $0.01.
   Inbox: a 4th recurring `peter@bytewells.com` cold-pitch (same unlaunched marketplace, now
   targeting `ats-jobs-scraper` monthly-rental billing) — declined per standing policy (queue item
   4), no reply, no owner email. Nothing else new/actionable.

0-DONE-h1085-shopify-products-webhookUrl-first-ever-live-verification.
   **[cycle 1085] DONE — GROWTH slot per rotation (1083 G -> 1084 Q -> 1085 G). `varied_test` on
   `shopify-products-scraper`, fleet-oldest (1033->1085). FIRST-EVER LIVE VERIFICATION of
   `webhookUrl`, a feature shared by 20 Actors that no prior cycle had ever actually fired.**
   Created a free webhook.site catcher, ran the Actor live via `POST /v2/acts/<user>~<slug>/runs`
   (not `/run-sync`, which returns the empty `OUTPUT` KV record and looks like a no-op even though
   the run and webhook both fire). The captured POST body matched the run's own `RUN_SUMMARY` KV
   record field-for-field, exactly as the README documents. A second run — triggered by accident
   when an earlier `/run-sync` attempt turned out to have run the Actor for real — hit a genuine
   Shopify 429 on allbirds.com and still correctly POSTed `pushed:0` with the error attributed to
   the right store, confirming the webhook fires honestly on a failure path too, not just the
   happy path. CLEAN, no bug, no code change. Cost: one `result` self-charge ($0.0008) + ~$0.0007
   compute across both runs. Full writeup in `state/audit_dates.json` (`varied_test_note`) and
   `notes/LEARNINGS.md` (Cycle 1085 entry). Opened queue item **1e**: sweep the same check across
   the other 19 webhookUrl Actors, 2-3 per QUALITY/GROWTH cycle. Inbox unchanged (dmarc reports,
   two recurring SEO-listing spam pitches, one stale cold-pitch) — no reply, no owner email
   warranted. `check-pricing` 24/29/0, `check-charges` 24/24, both clean; all 3 services active,
   `/health` and `/tools/shopify-products-scraper` both 200.

0-DONE-h1084-competitor-audit-federal-register-scraper-three-false-numbers.
   **[cycle 1084] DONE -- `competitor_audit` on `federal-register-scraper`, fleet-oldest
   (1040->1084). FOUND AND FIXED THREE FALSE NUMBERS IN OUR OWN README, 6-for-6 on the
   listing-sourced-claim pattern.** The niche grew **17 -> 24 Store listings in 44 cycles** (every
   newcomer at 2 users / 1 u30d, all far below the ~50-u30d mandatory-schema-check bar, so
   pricing-only: pink_comic, benthepythondev, logiover, nexgenwatch, thirdwatch, adobeflex,
   maximedupre, straightforward_hydra, nexgendata, crawlerbros, skootle, andrew_avina,
   quarterly_jingo). Leader is still `ryanclinton/federal-register-search` at 14 users; nobody else
   above 6. All 24 price-checked live via in-effect `pricingInfos` (`startedAt <= now`; the 2
   zentrafoundry listings with a future-dated entry were correctly filtered).
   **The three fixes:** (1) "All 17" -> 24. (2) per-row range "$0.0007-$0.029" -> **$0.0007-$0.05**,
   because `nexgendata/federal-register-rules-scraper` bills $0.05/row and is now the niche's most
   expensive per row. (3) "all but one charge an Actor-start fee" -> **16 of 24 do, 8 do not**
   (`agentictools`, 3x `zentrafoundry`, `chrisp1211`, `maximedupre`, `scrapemint`, `andrew_avina`)
   -- **and that one was already false the day it was written at 1040, self-contradicted two
   sentences later by the same paragraph naming two no-start-fee rivals.** See queue item 2g.
   Also tightened "cheapest on Free, Bronze and Silver" to "cheapest per row on Free and Bronze,
   cheapest in total on Silver" -- `koalastuff` ties our $0.0008/row on SILVER and only loses on its
   $0.00005 start fee (the 1040 audit *note* had this right; the README prose had rounded it off).
   **Nothing drifted on any previously-named rival** -- `koalastuff` $0.0007/row GOLD+ with
   `maxResults` maximum=100 and `agentictools` $0.001/row flat with `maxItems` maximum=1000 both
   re-pulled from their live latest-build `inputSchema` and both still exactly as claimed. Our own
   side re-verified per queue 2b: `meta.json` `result` = $0.0008 FLAT, no start event; our
   `.actor/input_schema.json` `maxResults` maximum=50000, so the "50,000 rows via cursor paging"
   ceiling claim holds. Cheapest-anywhere scan: $0.0007 (koalastuff GOLD+) is the niche floor and
   $0.001 is the FREE-tier floor, both above/at our $0.0008 as claimed.
   One new pricing SHAPE logged for the fleet: `nexgenwatch/us-federal-register-rule-event-watch`
   bills **$0.067-$0.10 per "source-check" event plus a $0.02 Actor start, before any row is
   delivered** -- first per-check (rather than per-row or per-start) pricing seen in this niche.
   Build **0.1.31** pushed; all 5 edited claims confirmed live by reading the `latest` build's
   `readme` field via the API (and "All 17" confirmed ABSENT). `audit_dates.json` stamped
   competitor_audit 1040->1084 with a full note, clean 2-line `git diff --stat`.
   Standing checks all clean: `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-competitor-claims` 58/0 + 40/0, `check-backlinks` 93/52/0, `check-disclosure` 52+13/0,
   `check-actor-guides` 23/0, `check-meta-fields` 11/0. Site `/health` and
   `/tools/federal-register-scraper` both 200. No Actor runs, **$0 spent.**

0-DONE-h1083-competitor-audit-substack-scraper-plus-checker-regex-fix.
   **[cycle 1083] DONE — `competitor_audit` on `substack-scraper`, fleet-oldest (1038->1083).
   CLEAN: zero pricing/schema drift on both named rivals, zero false claims.** Re-pulled live
   `pricingInfos` + input schemas for `automation-lab/substack-scraper` (519u/138u30d, pricing
   byte-identical to 1038) and `sourabhbgp/substack-scraper` (93u/20u30d, pricing identical,
   schema re-confirmed still missing `discoverCategories`/`leaderboardOnly`/engagement filters).
   Store re-swept: two newcomers above sourabhbgp's user count but below the ~50-u30d mandatory-
   schema-check bar -- `easyapi/substack-posts-scraper` (273u/29u30d, $0.00499/result + $0.09
   start fee) and `fatihtahta/substack-scraper` (243u/32u30d, $0.00199/result flat), both pricier
   than us at every tier -- added as a one-sentence addendum, dated 2026-10-01. Build 0.1.46
   pushed, verified live via the build `readme` field.
   **Found a real checker bug, worth more than the audit: `bin/check-competitor-claims`' `USERS`
   regex required the closing backtick immediately after the handle, so it silently matched
   nothing on any paragraph that backticks the full `owner/slug` instead of the bare handle** --
   caught by testing the regex directly against this README's own paragraph. Fleet grep found 10
   README files / ~19 claims affected (sam-gov-opportunities, remote-jobs, google-play-reviews,
   eu-ted-tenders, grants-gov, app-store-reviews, substack, steam-reviews) that had never actually
   had their user counts checked despite "0 stale" every cycle since whenever each was written.
   Fixed with a one-line regex change (optional `(?:/[a-z0-9_-]+)?` before the closing backtick)
   plus registering `easyapi`/`fatihtahta` in substack's `FILE_OVERRIDES`. Re-run fleet-wide:
   checked count 41->58, still 0 stale -- every number the blind spot had been hiding was still
   accurate, but the blind spot itself was real for 45+ cycles. One residual gap intentionally
   left open: see queue item 1a-ii (`theagents/appstore-reviews` line-break case).
   Standing checks clean after the fix: `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-competitor-claims` 58/0 + 40/0. $0 spent (schema/pricing reads only, no Actor runs).
   `audit_dates.json`, `STATUS.md`, `LEARNINGS.md` updated; committed and pushed.

0-DONE-h1082-housekeeping-archive-status-queue.
   **[cycle 1082] DONE — QUALITY slot per rotation (1080 Q -> 1081 G -> 1082 Q). Housekeeping
   archive pass, overdue since 1046 (flagged at 1081), same method as 999/1022/1034/1038/1046.**
   Found the cycle boundary via `grep -noE '^## Cycle [0-9]+' state/STATUS.md` (1081 at top, 1028
   at bottom, 507 lines) and `grep -noE '^[0-9]+-(DONE-)?h[0-9]+...' tasks/queue.md` (h1081 at line
   125, h1022 at line 2963, header lines 1-124). Cut STATUS.md before `## Cycle 1055` (line 224),
   keeping cycles 1081-1056 live; cut queue.md after the h1056 entry (line 1237), keeping the
   header plus h1081-h1056 live.
   Verified byte-exact before overwriting: split into keep/archive chunks, `diff`'d
   `cat(keep,archive)` against the original on both files — zero differences. Appended both archive
   chunks to `STATUS_ARCHIVE.md`/`queue_archive.md` with a `## Archived 2026-10-01T14:31:01Z by
   cycle 1082 — cycles/h X-Y` header, same convention as prior passes. Confirmed both live files'
   tails end on a clean entry boundary.
   Result: `STATUS.md` 214.4KB->90.7KB, `queue.md` 266.2KB->109.7KB, both with headroom again. No
   Actor code/README/build touched, so `check-pricing`/`check-charges` were not re-run; confirmed
   nothing broke via `systemctl is-active` (3/3) and `/health` + `/tools/substack-scraper` curl
   checks (both 200). **$0 spent.** Inbox unchanged from 1080/1081, nothing actionable, no owner
   email.
   Ran out of cycle time budget on the archive pass itself; did not reach the also-flagged
   `competitor_audit` on `substack-scraper` — left as top priority for cycle 1083 (GROWTH slot;
   this audit task is being pulled forward out of rotation since it's overdue, same precedent as
   prior cycles carrying work across slots).

0-DONE-h1081-google-play-reviews-varied-test-appversions-sincedate-minthumbsup.
   **[cycle 1081] DONE — GROWTH slot per rotation (1079 G -> 1080 Q -> 1081 G). `varied_test` on
   `google-play-reviews-scraper`, fleet-oldest on that axis (1032 -> 1081). CLEAN, no code change.**
   First-ever combined test of `appVersions` + `sinceDate` + `minThumbsUp` on this Actor (prior
   passes at 800/820/844/1032 never combined a version filter with a date window and a thumbs-up
   floor). Predicted free and local first: fetched Discord's (`com.discord`) 150 newest reviews via
   the same `google-play-scraper` npm library the Actor itself calls (`node -e`, no platform cost).
   Version `"347.12 - Stable"` had 50 of 150 reviews; narrowing to `thumbsUp>=1` +
   `date>=2026-09-30T00:00:00Z` predicted exactly 14 reviews with known reviewIds. Live run
   (`appVersions:["347.12 - Stable"]`, `sinceDate:"2026-09-30T00:00:00Z"`, `minThumbsUp:1`,
   `maxReviewsPerApp:200`, `maxResults:20`) delivered exactly those same 14 reviewIds — exact match,
   proving the three filters compose correctly (genuine AND, no silent drop/over-match). Self-charge
   $0.0014 (14 result events). `audit_dates.json` `varied_test: 1032 -> 1081`, clean 2-line `Edit`,
   prior note preserved inline. `check-pricing` 24/29/0, `check-charges` 24/24 both clean. 3 services
   active, `/health` + `/tools/google-play-reviews-scraper` both 200. Revenue flat (44 users / 0
   reviews / 0 bookmarks / $0), no owner email. Inbox unchanged from 1080, nothing actionable.
   **Flagged but not done: `state/STATUS.md` (211KB) and `tasks/queue.md` (263KB) are both past the
   150KB housekeeping threshold again** (last archived cycle 1046) — see NEXT-CYCLE item 0 above.

0-DONE-h1080-app-store-reviews-competitor-audit-FOUND-FALSE-ratings-histogram.
   **[cycle 1080] DONE -- QUALITY slot per rotation (1079 G -> 1080 Q). `competitor_audit` on
   `app-store-reviews-scraper`, fleet-oldest on that axis (1037 -> 1080). FOUND FALSE: the
   listing-sourced-claim pattern is now 5-for-5.**
   Tree clean at cycle 1079's `b240d9f` at start. 3 services active, `/health` and
   `/tools/app-store-reviews-scraper` both 200. Inbox `list 10` unchanged from 1079, nothing
   actionable (bytewells x1, dmarc x5, j_woodgate01 pair, indexhelp.pro, capsule26).
   **The false claim:** README said "None of the five list the per-star ratings breakdown, watch-mode
   rating-edit detection, or storefront-fallback/hole-skipping behaviour." Pulled all five rivals'
   **live build input schemas** (not Store descriptions) and
   `sourabhbgp/apple-app-store-scraper` ships **`includeRatingsHistogram`, default ON**, in its
   `app-details` mode. Note where it was hiding: in the free-text `description` of the nested
   `appDetailsConfig` object, not as a top-level property -- a property-name grep would have missed it.
   **Rescoped to what is actually true and checkable:** its modes are mutually exclusive, so reviews
   + distribution there costs two runs and a join; ours rides along in the same run, per storefront,
   free, and is dropped if it fails to reconstruct Apple's published average. The watch-mode and
   storefront-fallback thirds of the claim **survived schema-checking on all five** (`theagents`'
   `until` and `sourabhbgp`'s `sinceDate` are one-shot date cutoffs, not baselines;
   `availability-matrix` probes app existence 200/404, not review presence, and does not re-route).
   **Second finding, now queue 1b:** `sourabhbgp`'s `reviewsConfig` claims depth past Apple's RSS
   500-cap via Apple's catalog endpoint, `maxReviewsPerApp` to 100,000. Disclosed in the README as
   *their* claim (with their own schema's admission that that endpoint ignores `sortBy` and returns
   relevance order) rather than asserted or dismissed. Tried to verify against Apple directly and
   free: the App Store page and the main JS bundle both fetch 200 but neither contains a bearer
   token -- parked with exact next steps and an explicit out-of-bounds line in 1b.
   **Pricing re-pulled live for all five: ZERO drift since 1037.** thewolves $0.0001 flat, theagents
   $0.0001 flat (both = our price and shape), johnvc $0.00125-0.00144 tiered + $0.0175 setup +
   $0.00005 start + $0.00001/row (that last one was missing from our prose, now added), easyapi
   $0.00299 + $0.09 start, sourabhbgp $0.002 flat. Newcomer sweep per 2a: no unnamed rival above
   50 u30d; `code-node-tools/app-reviews-scraper` (155 users, 38 u30d) schema- and price-checked
   anyway -- 3-5x our price, no threat.
   **Near-miss, now queue 2b:** the first draft of the rewrite asserted johnvc had sort orders "we
   lack" -- false, we have had `favorable`/`critical` all along. Caught by reading our own
   `input_schema.json` before commit and inverted into a real differentiator (833 proved those
   `sortBy` values return an empty RSS feed live, so we buffer-and-re-order instead).
   Full `owner/slug` used throughout per 2c. Builds 0.1.67 -> 0.1.69 (two repushes to get a dated
   verification clause into each of the new paragraphs -- see 2e), final README confirmed live via
   the build's `readme` field, `package.json` 0.1.7 -> 0.1.10. `check-competitor-claims` 41/0 stale,
   40/0 undated; `check-pricing` 24/29/0; `check-charges` 24/24. No Actor runs, $0 spent this cycle.
   Revenue flat (44 users / 0 reviews / 0 bookmarks / $0), no owner email needed.


0-DONE-h1079-steam-reviews-searchterms-dedupe-filter-varied-test-clean.
   **[cycle 1079] DONE — GROWTH slot per rotation (1077 G -> 1078 Q -> 1079 G). `varied_test` on
   `steam-reviews-scraper`, fleet-oldest on that axis (1031 -> 1079). First-ever combined test of
   the `searchTerms` resolution path with a review filter, exercising `addId`'s cross-term dedupe
   live for the first time. CLEAN, no code change.**
   Tree clean at cycle 1078's `c7d944f` at start. 3 services active, `/health` and
   `/tools/steam-reviews-scraper` both 200.
   **Inbox: a THIRD `peter@bytewells.com` cold pitch** (`14fb0a04`, same unlaunched Bytewells
   marketplace, now targeting `ats-jobs-scraper`) — declined, no reply, no owner email, same policy
   as cycles 1076/1077. Now 3-for-3. Rest of `list 10` unchanged.
   **Every prior varied_test/enum_audit on this Actor (801/820/840/846/937/988/1031) drove
   `apps:[...]` directly** — `searchTerms` (resolve a query via Steam's `storesearch` API, then scrape
   each resolved app through the identical filter pipeline) had never been combined with a review
   filter, and `addId`'s dedupe across two search terms resolving to an overlapping game had never
   been exercised live at all.
   **Picked `searchTerms:["Half-Life","Half-Life 2"]`, `searchLimit:2`** after a free `storesearch`
   probe confirmed overlap: term 1 resolves to [220,70], term 2 to [220,290930] — app 220 (Half-Life
   2) appears in both, which is exactly what tests the dedupe (disjoint terms wouldn't). Added
   `reviewType:"negative"` + `purchaseType:"steam"` to test filter composition across the resolved
   set simultaneously.
   **Predicted per-app counts via 3 free direct Steam `appreviews` calls first** (review_type=negative,
   purchase_type=steam, num_per_page=15): 220->15, 70->15, 290930->2 (that app genuinely has only 2
   such reviews, ever).
   **Live run** (`maxReviewsPerApp:15`, `maxResults:50`): `RUN_SUMMARY.appsRequested=3` (not 4 —
   confirms app 220 was scraped once despite matching both search terms), delivered 32 rows with
   per-app counts 220:15/70:15/290930:2 — an EXACT match to the prediction — and all 32 rows had
   `recommended:false` + `steamPurchase:true` (0 filter violations across any resolved app).
   `chargedEventCounts {result:32}` matched delivered rows exactly, no double-charge from the dedupe.
   **CLEAN, no code change.** `audit_dates.json`: `steam-reviews-scraper.varied_test` `1031 -> 1079`,
   full note, prior 1031/988 notes preserved inline (1031's note had never actually been written at
   the time it bumped the number — backfilled now from its commit message), clean 2-line `Edit` (JSON
   re-validated, `git diff --stat` confirmed exactly 2 lines). `check-pricing` 24/29/0,
   `check-charges` 24/24 both clean. Self-charge ~$0.0008 (32 result events), still ~$1.1 of $300.
   Revenue flat (44 users / 0 reviews / 0 bookmarks / $0), no owner email needed.

0-DONE-h1078-fec-competitor-audit-clean-reverification-no-drift.
   **[cycle 1078] DONE — QUALITY slot per rotation (1077 G -> 1078 Q). `competitor_audit` on
   `fec-campaign-finance-scraper`, fleet-oldest on that axis (1036 -> 1078). CLEAN
   RE-VERIFICATION — no drift, no code change, confirms the cycle-1036 audit held up over time.**
   Tree clean at cycle 1077's commit at start. 3 services active, `/health` and
   `/tools/fec-campaign-finance-scraper` both 200.
   **Inbox: nothing actionable.** `list 10` unchanged except a new message from
   `contact@capsule26.com` (another autonomous agent, `873db8ee`, re-sent/still sitting) asking a
   genuine technical question about DB-layer vs app-layer dedup enforcement, prompted by our own
   watch-mode-baseline-eviction postmortem. Not revenue, not critical, no concrete ask — logged,
   no reply, no owner email, consistent with standing policy on this inbox.
   **Re-ran the store search for the niche (15 listings)**: no new entrant above 3 total users;
   `ryanclinton` still the clear leader (17 users, 40 actual runs30d via the Actor API — the
   store-search `runs30d` field itself reads 0 for every listing, a known display quirk, not real
   zero traffic). **Pulled `ryanclinton`'s live input schema fresh** (not the Store description):
   `searchMode` enum is still exactly `[contributions, candidates]` — no `disbursements`/
   `independentExpenditures` — and `donorOccupation`/`donorCity`/`donorZip`/`maxAmount`/a date
   window/`office`/`party`/`candidateId`/`committeeId` are all still absent from its schema. Every
   property in our README's feature-gap claim re-verified true, property by property, no drift.
   **Pricing re-pulled live for both named rivals**: `ryanclinton` $0.002/record + $0.00005 start,
   `crawlerbros` $0.005 FREE tapering to $0.003 GOLD+ + $0.005 start — both byte-for-byte unchanged
   since 1036. No feature or price drift anywhere, so no substantive README rewrite was needed —
   bumped the two "re-verified live" dates from 2026-09-30 to 2026-10-01, `package.json`
   0.1.11 -> 0.1.12, build 0.1.41 pushed and verified live via the build's `readme` field.
   **Lesson applied, not re-learned the hard way**: built the `audit_dates.json` edit as a direct
   `Edit` call with exact old/new strings, not a bash/python heredoc — a first attempt via a
   double-quoted `python3 -c "..."` heredoc let the shell expand every `$0.002`-style price into
   `/usr/bin/zsh.002` (since `$0` inside double quotes is the shell's own script-name variable);
   caught immediately via `git diff` before committing, reverted with `git checkout --`, and redone
   clean as a 2-line `Edit` diff (JSON re-validated, trailing newline confirmed byte-for-byte).
   All standing checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-competitor-claims`
   46/0 + 38/0, `check-readme-samples` 35/79/0. $0 self-charge (no platform runs needed — every
   finding came from free API schema/pricing reads), still ~$1.1 of $300. Revenue flat (44 users,
   0 reviews, 0 bookmarks, $0), no owner email needed.

0-DONE-h1077-apple-podcasts-chapters-shipped-and-live-verified.
   **[cycle 1077] DONE — GROWTH slot per rotation (1076 Q -> 1077 G). `varied_test` on
   `apple-podcasts-scraper`, fleet-oldest on that axis (1030), paired per 1b/1c with shipping the
   1072-queued `chapters` product gap. Build 0.1.56 (code+README) pushed and verified live on both
   the itunes and RSS code paths. No pricing drift, no code bugs found — a pure product-gap close.**
   Tree clean at `121af00` at start. 3 services active, `/health` + `/tools/apple-podcasts-scraper`
   both 200. **Inbox: a SECOND `peter@bytewells.com` pitch** (see item 4 above) — declined, no reply,
   no owner email, same policy as 1076. Rest of `list 10` unchanged.
   **Added `chaptersUrl`**, reading Podcast 2.0 `<podcast:chapters url="...">` the same way
   `transcriptUrl` already reads `<podcast:transcript>` — one new line in `rssEpisodeRow()` plus the
   itunes-path base object (`src/main.js`). Unit-verified the cheerio selector first against a
   synthetic Podcast 2.0 XML snippet in isolation (`node -e`, both `transcriptUrl` and `chaptersUrl`
   extracted correctly) before trusting any live feed.
   **Then searched 7 real feeds for one that actually publishes `podcast:chapters` — found none**
   (Lex Fridman, Darknet Diaries via 2 hosts, No Such Thing As A Fish, ATP, podcastindex.org's own
   Podcasting-2.0 feed, WNYC). The tag is real, documented, and now correctly parsed when present —
   but genuinely rare in the wild today. Worth remembering before assuming any Podcasting-2.0 field
   shows up often in practice; queued as a quick Dev.to angle (item 3).
   **Build 0.1.56 verified live 2 ways.** (1) Default regression input (itunes path): 5/5 charged,
   `chaptersUrl` present and `null` as expected. (2) Live `useRssForFullArchive:true` run (first-ever
   live exercise of this exact combo): 3/3 rows, `source:"rss"`, `chaptersUrl` present (null on this
   feed, consistent with the survey above) — own-account run, `chargedEventCounts {result:0}` as
   expected. README's `logiover` paragraph rewritten to drop the "beats it on one" concession;
   `registry.json output_fields` and `.actor/dataset_schema.json` both updated to list `chaptersUrl`.
   Standing checks clean post-push: `check-pricing` 24/29/0, `check-charges` 24/24, `check-meta-fields`
   11/0, `check-registry-fields` 0 drift, `check-readme-samples` 35/79/0, `check-competitor-claims`
   46/0 + 38/0 (a first run flagged `uk-find-a-tender-scraper`'s `publicdata` claim as "gone from the
   Store" — immediate re-run was clean and a direct `GET /v2/acts/publicdata~...` confirmed 200 live;
   a transient API hiccup, not real drift).
   `audit_dates.json`: `apple-podcasts-scraper.varied_test` `1030 -> 1077`, full note, prior note
   preserved inline, clean 2-line `Edit`. $0 self-charge (both platform runs were own-account) — still
   ~$1.1 of $300. Revenue flat (44 users / 0 reviews / 0 bookmarks / $0), no owner email needed.

0-DONE-h1076-weasel-phrase-grep-swept-fleetwide-eu-ted-false-on-3-of-6-claims.
   **[cycle 1076] DONE — QUALITY slot per rotation (1075 G -> 1076 Q). Ran the queue's own
   weasel-phrase grep fleet-wide for the first time: 3 hits, graded clean / scoped-but-misleading /
   false-on-half by pulling each rival's LIVE INPUT SCHEMA. 3 builds pushed and verified live.**
   Tree clean at cycle 1075's `057d135` at start. 3 services active, `/health`,
   `/tools/google-play-reviews-scraper` and `/tools/eu-ted-tenders-scraper` all 200.
   **INBOX: one NEW message** (first change since cycle 1054) — `peter@bytewells.com`, see item 4
   above. Declined, no reply, no owner email. Rest of `list 10` unchanged (dmarc x5,
   `j_woodgate01` pair, indexhelp.pro, capsule26 `873db8ee`).
   **Assigned task (`competitor_audit` on `google-play-reviews-scraper`, fleet-oldest at 1032) —
   DONE and CLEAN on the named rival.** Pulled `neatrat`'s live input schema off its 2026-09-30
   build and checked all 9 of cycle 1032's differentiator claims property by property: every one
   survives (`appIdOrUrl` still a single string; no `searchTerms`/`genres`/`replyFilter`/
   `minThumbsUp`/`minReviewLength`/`includeAppDetails`/watch/webhook). First clean rival paragraph
   in four audits. Rephrased it from "none of which appear on their listing" to schema-sourced
   wording anyway.
   **But found the real defect by re-running the store search: `code-node-tools/google-play-reviews-scraper`**
   (252 users, **53 u30d — 4th by 30-day growth**, never named by any prior audit of this niche)
   ships `minThumbsUp` and `minReviewLength` under IDENTICAL property names, plus `hasReply`
   (== our `replyFilter`), `dateFrom`/`dateTo` (== our `sinceDate`/`untilDate`), `minScore`/
   `maxScore` and `keywords`, and takes `appIds` as an array (many apps per run) like we do. Our
   differentiator list was true of `neatrat` and would read to a buyer as a claim about the niche.
   Added a dated paragraph naming them, saying explicitly "treat the filter list above as what
   `neatrat` lacks, not as unique to us", and listing what they really have no equivalent for
   (`searchTerms`, `genres`, `includeAppDetails`, watch mode, `webhookUrl`, `aspectRatings`).
   **We crush them on price** and verified it live: $0.002 `apify-actor-start` EVERY run + tiered
   $0.0005/review FREE -> $0.0003 GOLD+, vs our flat $0.0001 no start fee = ~$0.50 vs $0.10 per
   1,000 reviews. The README's "no Actor in this niche advertises a lower per-review price" survives.
   Build **0.1.51** (0.1.50 then a repush for 2e's regex limit), verified live via the build `readme`.
   **`eu-ted-tenders-scraper` vs `foxlabs/ted-tenders` — FOURTH confirmed false-claim hit, 3 of 6
   named differentiators FALSE.** They DO ship `keywords` (phrase match over notice text) = our
   "full-text search" claim; a `language` enum holding exactly the same 24 EU official languages we
   advertise; and a `query` field whose own description documents `total-value>=1000000` as an
   example = our contract-value-floor claim. Only `procedureType` (their `noticeTypes` is the
   *notice* kind, not the procurement procedure), deadline filtering and watch mode survive.
   Rewrote the paragraph to admit in-text that the earlier version overstated it, and reframed the
   value claim on its real structural win: their DSL **overrides all other filters**, so there you
   pick either a value floor or your country/CPV/date filters, while our `minValue`/`maxValue`
   compose with everything in one run. Pricing re-verified live and unchanged ($0.004/result +
   $0.00005 start, record still from 2026-05-15; 39 users / 12 u30d) — only the feature half had
   rotted. Build **0.1.44** verified live.
   **`shopify-products-scraper` vs `trovevault` — CLEAN, claim CONFIRMED.** Their entire live input
   schema is six properties (`domains`, `maxProducts`, `includeInventoryDetails`,
   `proxyConfiguration` + `datasetId`/`runId` plumbing), so the filters/watch/webhooks we claim they
   lack, they genuinely lack. Rephrased to cite the six-property schema as the evidence. Build
   **0.1.68** verified live. **Pricing half still outstanding — see 1a.**
   **All standing checks clean**: `check-competitor-claims` 46 user-count/0 stale + 38 paragraphs/0
   undated (after the 2e repush), `check-pricing` 24/29/0 drift, `check-charges` 24/24,
   `check-readme-samples` 35/79/0, `check-backlinks` 93 pairs/52 posts/0 missing, `check-disclosure`
   0, `check-meta-fields` 11/0, `check-source-bytes` 445/0, `check-actor-guides` 23/0 flagged.
   **$0 self-charge** (no platform runs needed — every finding came from free API schema reads),
   still ~$1.1 of $300. Revenue flat: 44 users, 0 reviews, 0 bookmarks, $0.

0-DONE-h1075-fda-recall-voluntaryMandated-classifications-varied-test-class-i-never-mandated.
   **[cycle 1075] DONE — GROWTH slot per rotation (1074 Q -> 1075 G). `varied_test` on
   `fda-recall-scraper`, fleet-oldest on that axis (1029). CLEAN NEGATIVE (no code change) + a
   genuine, surprising data finding written into the README.**
   Tree clean at `6e791ed` at start. 3 services active, `/health` 200, `/tools/fda-recall-scraper`
   200. Inbox `list 10` unchanged from cycles 1054-1074 (dmarc x5, `j_woodgate01` pair,
   indexhelp.pro, bold.org `116f7cc3`, capsule26 `873db8ee`) — nothing new, no owner email.
   **Grepped LEARNINGS.md for `voluntaryMandated` and got zero hits — it had never been combined
   with another filter in a `varied_test` before**, despite being a real, documented, rare (<2%)
   filter since the Actor shipped. Picked `voluntaryMandated` + `classifications` as the combo.
   **Predicted via 3 free direct openFDA API calls first** (no Actor cost): `voluntary_mandated:
   "FDA Mandated"` alone = 715 across all 3 endpoints (396 food + 29 drug + 290 device); adding
   `classification:"Class I"` = 28 (27 food + 0 drug + 1 device). **Of openFDA's entire 1,750-row
   Class I drug recall history, not one is FDA Mandated** — every single one is voluntary/firm-
   initiated — while Class I food (27) and device (1) recalls do include FDA-Mandated ones.
   **Live-verified with 2 real capped Actor runs** (`maxResults:5`, `reportDateFrom:"2000-01-01"`
   to cover full history): control run (`voluntaryMandated` alone) `RUN_SUMMARY.declaredMatches=715`
   (396/29/290 per product type); test run (+`classifications:["Class I"]`) `declaredMatches=28`
   (27/0/1 per product type) — both totals and both per-type breakdowns matched the direct-API
   predictions exactly, proving genuine AND composition rather than either filter being silently
   ignored.
   This is a real, buyer-relevant fact, not a defect — wrote it up as a new dated README FAQ entry
   ("Are FDA-mandated recalls more or less severe than voluntary ones?") rather than just logging it
   here. Build 0.1.40 pushed (`package.json` 0.1.6->0.1.7, README only), verified live via the
   build's `readme` field (new FAQ text present). `check-pricing` 24/29/0, `check-charges` 24/24
   both clean. Self-charge: 10 result events (5+5) at $0.0035 = $0.035, negligible — still ~$1.1 of
   $300. `audit_dates.json`: `fda-recall-scraper.varied_test` `1029 -> 1075`, full note, prior note
   preserved inline, clean 2-line `Edit` (JSON re-validated, `git diff --stat` confirmed exactly 2
   lines changed). Revenue flat (44 users / 0 reviews / 0 bookmarks / $0), no owner email needed.

0-DONE-h1074-steam-reviews-competitor-audit-automation-lab-false-claims-memo23-added.
   **[cycle 1074] DONE — QUALITY slot per rotation (1072 Q -> 1073 G -> 1074 Q). `competitor_audit`
   on `steam-reviews-scraper`, fleet-oldest on that axis (1031). 3rd confirmed false competitor-
   feature claim of this class (after 1068 gentle_cloud, 1072 sourabhbgp), plus a 254-cycle-old
   known-but-unshipped finding finally added. 1 build pushed (0.1.54, README only), verified live.
   No code change.**
   Tree clean at `b4ac3d6` at start. Inbox `list 10` unchanged from cycles 1054-1073 — nothing new,
   no owner email. 3 services active, `/health` + `/tools/steam-reviews-scraper` both 200.
   **Pulled `automation-lab/steam-game-reviews-scraper`'s live input schema off its latest build**
   (modified 2026-09-02) instead of its Store description. Our README's only competitor paragraph
   claimed it "does not advertise" `purchaseType`/`reviewType` filters, an exact date window, or
   game-metadata attachment — **all 4 were false**: the schema carries `purchaseType`, `reviewType`,
   `startDate`/`endDate`, and `includeGameInfo` (identical property name to ours). Genuine surviving
   gaps re-confirmed: no keyword/`minPlaytimeHours` filter, no off-topic toggle, no `games` mode (so
   no player-count/owner-estimate data), no watch mode, no webhook. Pricing claim re-verified correct
   (their current in-effect pricingInfo: $0.003 flat start + review tiered FREE $0.000575 -> DIAMOND
   $0.00014 — identical per-review numbers to ours, minus their start fee we don't charge).
   **Second finding: `memo23/steam-reviews-scraper` (17 users, created 2026-09-07, 17/17 users30d)
   was already named "fastest-growing" in this Actor's own cycle-820 audit note but never added to
   the README** — a known-but-unshipped gap, not a fresh discovery. Added now: thin 8-property
   schema, no search-by-name/keyword/playtime/games-mode/watch/webhook, pricier ($0.005 start +
   flat $0.001/review vs our tiered $0.000575->$0.00014, no start fee).
   Build 0.1.54 pushed, README verified live via the build's `readme` field (new text present, old
   "does not advertise" phrase absent). `check-competitor-claims` needed a `FILE_OVERRIDES` entry for
   `memo23` on this README (handle-level map points at `memo23/remote-jobs-aggregator`) — **6th hit**
   of the LEARNINGS-1064 handle-collision trap.
   `audit_dates.json`: `steam-reviews-scraper.competitor_audit` `1031 -> 1074`, full note, prior
   note preserved inline, clean 2-line `Edit` (JSON re-validated, `git diff --stat` confirmed exactly
   2 lines changed). Final: `check-competitor-claims` 47/0 stale, 37 dated paragraphs/0 stale (was
   36), `check-pricing` 24/29/0, `check-charges` 24/24, `check-readme-samples` 35/79/0,
   `check-backlinks` 93/0, `check-disclosure` 52+13/0, `check-meta-fields` 11/0. $0 self-charge
   (read-only API reads + 1 free build) — still ~$1.1 of $300. Revenue flat (44 users / 0 reviews /
   0 bookmarks / $0), no owner email needed.

0-DONE-h1073-clinicaltrials-documenttypes-leadsponsor-varied-test.
   **[cycle 1073] DONE — GROWTH slot per rotation (1071 G -> 1072 Q -> 1073 G). `varied_test` on
   `clinicaltrials-scraper`, fleet-oldest on that axis (1028). CLEAN NEGATIVE, no code change —
   first-ever combined test of `documentTypes` (OR) with `leadSponsorName` (AND).**
   Tree clean at `9ffcae0` at start. Inbox `list 10` unchanged from cycles 1054-1072 (dmarc x5,
   `j_woodgate01` pair, indexhelp.pro, bold.org `116f7cc3`, capsule26 `873db8ee`) — nothing new, no
   owner email. 3 services active, `/health` + `/tools/clinicaltrials-scraper` both 200.
   **Picked `documentTypes` (aggFilters=docs:prot/sap/icf, OR-ed, ~9% of studies) combined with
   `leadSponsorName` (AREA[LeadSponsorName], AND)** — `documentTypes` had only ever been
   enum-validated (cycle 822), never combined with another filter in a `varied_test`. This Actor
   exposes no `documents` field in its dataset output, so the only live-checkable proof of the
   filter working is the registry's own `declaredMatches` count in RUN_SUMMARY, not dataset rows.
   **Predicted via 2 free direct CT.gov v2 API calls first** (no Actor cost): `icf`+leadSponsor
   alone = 433, `prot`+leadSponsor alone = 631, `icf OR prot`+leadSponsor = 681 — a genuine
   partial-overlap union (not equal to either alone, not the naive sum). Adding `sap` to the OR left
   it unchanged at 681 — `sap`'s 586 NCI studies are a full subset of `icf|prot`'s 681 for this
   sponsor, a real structural fact about the registry's document coverage, not a bug.
   **Live Actor run** (`documentTypes:["icf","prot"]` + `leadSponsorName:"National Cancer Institute"`
   + `conditions:"cancer"` + `maxResults:10`) returned `RUN_SUMMARY.declaredMatches=681`, an exact
   match. **Falsification control**: same query with `documentTypes` dropped entirely returned
   `declaredMatches=3544`, also an exact match to a separate direct-API prediction — proves the OR
   filter is genuinely load-bearing, not silently ignored (a single matching call can't rule that
   out; the control's different, also-correct number can).
   `audit_dates.json`: `clinicaltrials-scraper.varied_test: 1028 -> 1073`, full note, prior note
   preserved inline, clean 2-line `Edit` (JSON re-validated, `git diff --stat` confirmed exactly 2
   lines changed). `check-pricing` 24/29/0 drift, `check-charges` 24/24. Self-charge $0.0225 (15
   result events x $0.0015) — still ~$1.1 of $300. Revenue flat (44 users / 0 reviews / 0
   bookmarks / $0), no owner email needed.

0-DONE-h1072-apple-podcasts-scraper-competitor-audit-two-false-claims-and-logiover-found.
   **[cycle 1072] DONE — QUALITY slot per rotation (1070 Q -> 1071 G -> 1072 Q). `competitor_audit`
   on `apple-podcasts-scraper`, fleet-oldest on that axis (1030). Found and fixed 2 FALSE competitor
   feature claims live on our Store page since cycle 1030, plus the niche's fastest-growing rival
   never named. 1 build pushed (0.1.55, README only), verified live. No code change.**
   Tree clean at `df8d3fe` at start. 3 services active, `/health` 200. Inbox `list 10` unchanged
   from cycles 1054-1071 (dmarc x5, `j_woodgate01` pair, indexhelp.pro, bold.org `116f7cc3`,
   capsule26 `873db8ee`) — nothing new, no owner email.
   **Pulled live `input.properties` off the latest build for 3 rivals** (`sourabhbgp`, `logiover`,
   `coder_zoro`) rather than reading their Store descriptions — the method from 1068.
   **Finding 1, 2 of 5 claimed gaps against `sourabhbgp` are false.** Their schema carries
   `webhookUrl` ("POST each emitted record as it is collected") and `rssFeedUrl`/`rssFeedUrls` + an
   `episodes` mode that reads the feed directly, with their README discussing full feed archives
   outright. The word "webhook" appears nowhere in their README prose, which is how 1030 missed it.
   Surviving and schema-confirmed: no duration filter, no explicit filter, no new-episode-only watch
   mode (`trackDeltas` is chart-RANK snapshots only). Our hedge "its listing does not advertise ..."
   was literally true and read as "they lack these" — rewrote it to say what they actually lack.
   **Finding 2, `logiover/apple-podcasts-episode-scraper` (53 users, 15 u30d, modified 2026-09-23)**
   — highest 30-day growth in the niche by 3x, never named by any prior audit, and ships
   `useRssForFullArchive`, `minDurationSeconds`, `explicit` and a release-date window, some under
   property names identical to ours. Episodes-only (no reviews/charts/publisher), no watch mode, no
   webhook, and start fee + $0.0025/result FREE vs our flat $0.001 no-start-fee (2.5x) — but it
   parses Podcast 2.0 `chapters` and we do not (queued as 1c above). Added as a second dated
   paragraph naming the price and breadth advantages honestly.
   Build 0.1.55 pushed, verified live via the build's `readme` field (5 string assertions, incl. the
   old "Its listing does not advertise" phrase now absent). `check-competitor-claims` flagged one
   unrelated stale count on the way through (`scrapers_lat` 8 -> 9 in `trademark-search-scraper`) —
   fixed. Final: `check-competitor-claims` 47/36/0, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-readme-samples` 35/79/0, `check-backlinks` 93/0, `check-meta-fields` 11/0,
   `check-disclosure` 13/0. `audit_dates.json` `apple-podcasts-scraper.competitor_audit`
   `1030 -> 1072`, prior note preserved inline, 2-line `Edit` (no shell, per 1071's lesson).
   $0 self-charge — no platform runs needed, still ~$1.1 of $300. Revenue flat (44 users / 0 reviews
   / 0 bookmarks / $0), no owner email needed.

0-DONE-h1071-google-news-scraper-relatedArticles-varied-test-readme-split.
   **[cycle 1071] DONE — GROWTH slot per rotation (1069 G -> 1070 Q -> 1071 G). `varied_test` on
   `google-news-scraper`, fleet-oldest on that axis (1027). 1 build pushed (0.1.54, README only),
   verified live. No code change — the README's number was wrong for part of its own claim, not a
   bug.**
   Tree clean at `3a4a23e` at start. Inbox `list 10` unchanged from cycles 1054-1070 (dmarc x5,
   `j_woodgate01` pair, indexhelp.pro, bold.org `116f7cc3`, capsule26 `873db8ee`) — nothing new, no
   owner email. 3 services active, `/health` + `/tools/google-news-scraper` both 200.
   **Picked `relatedArticles` because it was never live-tested**: shipped cycle 264, and a grep of
   LEARNINGS.md for the field name returned nothing. The README has claimed a flat "roughly 1% of
   results for a typical search" the whole time.
   **Ran 6 real capped platform runs (240 articles, decodeUrls/fetchArticleBody/extractTickers off
   to hold down cost) split by feed type.** 3 keyword searches: "stock market" 0/50, "Tesla" 0/30,
   "artificial intelligence" 1/30 — averaged ~1.1%, matching the old claim. 3 topic/section feeds:
   WORLD 50/50, NATION 50/50, TECHNOLOGY 29/30 — **97-100%**, a large gap the flat number was hiding.
   Spot-checked several topic-feed `relatedArticles` arrays against the actual titles/sources
   returned: real Reuters/BBC/NYT/CNN/Fox multi-outlet coverage of the same story, not a parsing
   artifact.
   **This is an undersold differentiator, not a defect** — rewrote the README bullet to give both
   measured ranges and recommend topic browsing for buyers who want related-coverage data. Build
   0.1.54 pushed, verified live via the build's `readme` field (new phrase + "97-100%" present, old
   flat "roughly 1%" claim string absent).
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-competitor-claims` 47/35/0,
   `check-readme-samples` 35/79/0.
   `audit_dates.json`: `google-news-scraper.varied_test` `1027 -> 1071`, full note, prior preserved
   inline, targeted 2-line `Edit` (first attempt via a python/bash heredoc corrupted every `$` in the
   note via shell interpolation — `\$0.002` became `/usr/bin/zsh.002` — and duplicated the "cycle
   1027:" prefix; caught before committing, reverted with `git checkout`, redone as a direct `Edit`
   tool call with no shell involved, confirmed `git diff --stat` shows exactly 2 lines). Self-charge
   240 result events x $0.002 = $0.48 — still ~$1.1 of $300. Revenue flat (44 users / 0 reviews / 0
   bookmarks / $0), no owner email needed.

0-DONE-h1070-google-news-scraper-competitor-audit-memo23-found.
   1. **Fleet-oldest `competitor_audit` is now `apple-podcasts-scraper` (1030)**, then
      `steam-reviews-scraper` (1031), `google-play-reviews-scraper` (1032). Not due this cycle
      (it's a GROWTH slot) — pick up on the next QUALITY cycle. Re-confirm fresh with:
        python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('competitor_audit') if isinstance(v.get('competitor_audit'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
   1b. **Fleet-oldest `varied_test`** — check with the equivalent `varied_test` sort; `google-news-
      scraper` itself is a candidate (last run cycle 1027) if nothing older turns up, now that its
      `competitor_audit` is freshly closed (1070). Good GROWTH-slot target.
   2. **HIGH VALUE, carried from 1069/1070 — fleet-wide re-audit of competitor FEATURE claims against
      rival input schemas.** Cycle 1068 proved the whole class is unverified: `check-competitor-
      claims` only checks user counts and paragraph dates, so every "no X, no Y, no Z" feature
      assertion in the fleet's ~34 competitor paragraphs rests on whoever wrote it having read the
      rival's *description* rather than its schema — the exact error that put a false claim on our
      Store page for 42 cycles. Do it in batches of 3-4 READMEs per QUALITY cycle, highest-traffic
      Actors first, using the snippet that worked at 1068:
        GET /v2/acts/<user>~<name> -> taggedBuilds.latest.buildId
        GET /v2/actor-builds/<buildId> -> data.actorDefinition.input.properties  (+ .readme for sample output)
      Start with the two other paragraphs that make the most sweeping "no watch mode / no user
      lookups" claims. **Consider instead/also extending `check-competitor-claims` with a
      machine-checkable form**: a per-README dict of `{handle: [input-property names we assert they
      LACK]}`, failed if any named property shows up in their live schema. That converts the whole
      class from prose-trust to a check, and is the better long-term fix — scope it before batching
      the manual sweep.
   3. Dev.to: last published 2026-10-01 (id 4779767) — due again ~2026-10-03/04. Backlog candidates
      unsynced: `sam-gov-depth-cap-yield-varies`, `eu-ted-deadline-lives-in-a-different-field`,
      `two-opinions-same-case-name-different-day`, cycle 1058's NIH "predict the set, not the
      order", cycle 1060's tiered-price-undercut finding, cycle 1063's watch-mode-fingerprint
      finding, cycle 1064's signed-value-floor finding, cycle 1067's milestone-falsification
      technique, and now **cycle 1068's "the competitor claim on your own listing is the one nobody
      checks — audit the schema, not the description"** (buyer-facing trust angle, pairs naturally
      with 1060's tiered-price finding since both are "read the rival's actual data" stories).
   5. **The watch-mode `firstSeededAt` guard stays CLOSED — do not re-open** (LEARNINGS 1055).
   6. Carried, unchanged from 1068: the "N codes/categories" registry-prose claim class (per-slug
      mapping table design written out in the 1067 note below); `trademark-search-scraper`'s
      `fTMType` mark-type filter; slug-only competitor-claim reformat sweep of remaining READMEs;
      false-superlative sweep of the ~10 blog posts; Substack Notes gap; FEC `groupBy`; `neatrat`'s
      4 Google Play input gaps; fleet-wide spend-cap input; `federal-register-scraper`'s
      deadline-window/fetch-by-document-number gaps; the 3-filter-treatment sibling sweep.
   7. **Do NOT close the HN niche as "no gaps" on the strength of 1068.** The input-surface diff is
      done and we win it, but two things were explicitly NOT checked: (a) whether `gentle_cloud`'s
      `include_comments` (top-level comments *per story*, a tree walk) returns something our
      keyword-based `tags:["comment"]` search cannot — our comment search finds comments MATCHING A
      QUERY, theirs returns a given story's comment thread, which is a genuinely different shape and
      the one plausible real gap in the niche; (b) `automation-lab`'s `maxPages` section pagination
      vs our `maxItemsPerQuery`/`maxResults`. (a) is worth a scoped look on a GROWTH cycle — "give
      me every comment on story X" is a normal buyer ask and we may not answer it today.

0-DONE-h1070-google-news-scraper-competitor-audit-memo23-found.
   **[cycle 1070] DONE — QUALITY slot per rotation (1068 Q -> 1069 G -> 1070 Q). `competitor_audit`
   on `google-news-scraper`, fleet-oldest on that axis (1027). 1 build pushed (0.1.53, README only),
   verified live. No code change. Found a real, fast-growing 3rd competitor the README never named.**
   Tree clean at `e110d2a` at start. Inbox `list 10` unchanged from cycles 1054-1069 (dmarc x5,
   `j_woodgate01` pair, indexhelp.pro, bold.org `116f7cc3`, capsule26 `873db8ee`) — nothing new, no
   owner email. 3 services active, `/health` + `/tools/google-news-scraper` both 200.
   **Refreshed the two known rivals' live input schemas and counts** (easyapi 2662->2668 users,
   data_xplorer 2114->2130; pricing unchanged for both, still 2-2.5x our $0.002/result FREE tier) —
   then ran a fresh `apify-admin store "Google News scraper"` sweep per the 1068 playbook and found
   2 candidates not in the README: `automation-lab/google-news-scraper` (558 users, thin 7-property
   schema, no real threat) and **`memo23/google-news-scraper` (120 users but 53 of them joined in
   the last 30 days, Actor created June 2026)** — a genuinely fast-growing new entrant.
   **memo23 out-features this Actor in two verified places**: named-entity extraction
   (`extractEntities`: people/orgs/locations, vs. our tickers-only `extractTickers`) and an
   `enableCfBypass` flag for Cloudflare-protected publisher pages, which this Actor has no
   equivalent for. **But it unbundles what this Actor gives away free**: $0.0025/result base plus
   $0.0005 for URL-resolve and $0.0005 for body-enrichment ($0.0035/article fully enriched vs. our
   flat $0.002 with both included) and a $0.05/GB start fee we don't charge. Its `siteFilter` is
   include-only (no `excludeSites` equivalent) and it has no built-in list of Google News' 20 named
   sections — you need a section's URL already in hand to paste it, where this Actor takes
   `topics: ["BUSINESS"]` directly. Added a new dated README paragraph naming memo23 honestly
   (credits the 2 real wins, doesn't overclaim on the rest).
   **Handle-collision trap, 5th hit (LEARNINGS 1064/1068 pattern):** `memo23` already maps to
   `memo23/remote-jobs-aggregator` in `check-competitor-claims`'s handle-level `COMPETITORS` dict
   (a different niche). Added a `FILE_OVERRIDES` entry for `actors/google-news-scraper/README.md` ->
   `memo23/google-news-scraper` rather than clobbering the existing mapping.
   Build 0.1.53 pushed; README verified live by reading the build's `readme` field (memo23 +
   "Cloudflare-bypass" + "2026-10-01" all present, 18,697 chars — was 17,728 at cycle 1027).
   `check-competitor-claims` 47 user-count claims / 35 dated paragraphs, 0 stale (was 8/16 at 1027 —
   growth is from other Actors' cycles in between, not this edit alone). `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-backlinks` 93/0, `check-disclosure` 52+13/0, `check-actor-guides`
   23/0, `check-meta-fields` 11/0.
   `audit_dates.json`: `google-news-scraper.competitor_audit` `1027 -> 1070`, full note, prior
   preserved inline (" | cycle 1027: ..."), targeted 2-line `Edit` (not a full `json.dump` re-indent
   — first attempt used `indent=2` against a file that uses 1-space indent and produced a 474-line
   noise diff; reverted with `git checkout` and redone as a surgical string replace, confirmed
   `git diff --stat` shows exactly 2 lines changed). $0 self-charge (read-only API calls + 1 free
   build) — still ~$0.6 of $300. Revenue flat (44 users / 0 reviews / 0 bookmarks / $0), no owner
   email needed.

0-DONE-h1069-sec-insider-trades-combined-filter-varied-test.
   **[cycle 1069] DONE — GROWTH slot per rotation (1067 G -> 1068 Q -> 1069 G). `varied_test` on
   `sec-insider-trades-scraper`, fleet-oldest on that axis (1024). CLEAN, no code change — first-
   ever COMBINED run of the 3 cycle-1064 filters, against a new issuer.**
   Tree clean at `c164429` (cycle 1068's commit) at start. Inbox `list 10` unchanged from cycles
   1054-1068 (dmarc x5, `j_woodgate01` pair, indexhelp.pro, bold.org `116f7cc3`, capsule26
   `873db8ee`) — nothing new, no owner email. 3 services active, `/health` +
   `/tools/sec-insider-trades-scraper` both 200.
   **Combined `transactionCodes`+`minTransactionValue`+`insiderRoles` for the first time, against
   TSLA (not AAPL, which 1064's individual-filter checks used).** Pulled a full unfiltered baseline
   (93 rows across 15 filings, `maxResults` cap not hit) and hand-computed the predicted surviving
   set for `transactionCodes:["S"], minTransactionValue:1000000, insiderRoles:["officer"]`: exactly
   3 rows (Vaibhav Taneja's sales). The live filtered call matched by accession-number+value exactly.
   **Then ran a control that actually distinguishes AND from a dead filter**: swapped only
   `insiderRoles` to `["director"]` (same code/value thresholds) and predicted a disjoint 23-row set
   (Kathleen Wilson-Thompson's sales) — the live call matched that set exactly too. A single
   matching filtered call can't rule out a filter being silently ignored; getting the FLIP when one
   filter changes is what proves genuine combination. Also re-confirmed the cycle-1064 `Math.abs()`
   signed-value fix on new data: TSLA's baseline has a same-day Elon Musk M/F pair at
   +$7,094,441,104.20 / -$7,094,441,253.62 — both handled correctly regardless of issuer or
   magnitude.
   `audit_dates.json`: `sec-insider-trades-scraper.varied_test` `1024 -> 1069`, full note, clean
   4-line diff (re-dumped with `ensure_ascii=False` to avoid re-escaping unrelated unicode in other
   entries — first attempt produced a 474-line noise diff, reverted and redone). `check-pricing`
   24/29/0, `check-charges` 24/24. Self-charge: 297 events across 6 live calls = **$0.53** — two
   calls (93+93) were an avoidable duplicate baseline pull (computed the officer and director
   predictions from two separate live fetches instead of one cached pull), noted in LEARNINGS so
   the next `varied_test` fetches the baseline once. Cumulative still ~$0.6 of $300. Revenue flat
   (44 users / 0 reviews / 0 bookmarks / $0), no owner email needed.

0-DONE-h1068-hacker-news-competitor-feature-audit-false-claim-fixed.
   **[cycle 1068] DONE — QUALITY slot per rotation (1066 Q -> 1067 G -> 1068 Q). `competitor_audit`
   on `hacker-news-scraper`, fleet-oldest on that axis (1026). 1 build pushed (0.1.53, README only),
   verified live. No code change. TWO real findings — one of them a false claim of OUR OWN.**
   Tree clean at `d4ebd4e` at start. Inbox `list 10` unchanged from cycles 1054-1067 — nothing new,
   no owner email. 3 services active, `/health` + `/tools/hacker-news-scraper` 200.
   **Ran it as a FEATURE audit per the 1060/1062/1064 precedent, and crucially pulled each rival's
   live INPUT SCHEMA off `GET /v2/actor-builds/<latest>` -> `actorDefinition.input` rather than
   reading their Store description.** Niche: `gentle_cloud` 156 users (was 155 at 1026),
   `shahidirfan/hacker-news-data-scraper` 56, `automation-lab/hackernews-scraper` 28. Their input
   surfaces are 7 / 3 / 8 properties against our 19 — we remain a strict superset of all three.
   **FINDING 1: our README's claim that `gentle_cloud` has "no user-profile lookups" was FALSE and
   had been live on the Apify Store page since cycle 1026 (42 cycles).** Their schema has carried
   `mode:"user"` + `username` ("fetches a specific user's submitted stories") since their only
   build (March 2026) — cycle 1026 read the prose description, which omits it. `check-competitor-
   claims` passed every cycle in between because it verifies user counts and paragraph DATES, not
   feature assertions. Narrowed to the true claim: their `user` mode returns that user's STORIES,
   not profile fields (karma / about text / account age), which our `usernames` lookup does return.
   **FINDING 2: `minPoints`/`minComments`/date-windows are no longer unique in this niche** —
   `automation-lab` (listing rebuilt 2026-09-13, i.e. after 1026) ships all four. Our paragraph
   named only `gentle_cloud` so it was not yet false, one rewrite from being so. Added a second
   dated paragraph naming them and competing on PRICE: $0.001 per RUN START + $0.00115/story at
   Free there, so a 100-story run bills $0.116 vs $0.02 here, and they have no comment search, no
   user lookups, no `excludeKeywords`, no multi-query, no watch mode, no webhook.
   **Also: `gentle_cloud`'s tier ladder is non-monotonic** — $0.0002 at Free/Bronze (matching ours)
   but **$0.0015 at Silver**, 11x our $0.00013, before $0.0001 at Gold+. Prior audits read only the
   FREE tier and concluded "same price as us". Now quoted. `shahidirfan` $0.0009/result + $0.00005
   start (4.5x ours), 3 inputs, no threat.
   `hacker-news-scraper` 0.1.53 pushed; README confirmed live by reading the build's `readme` field
   (all 5 new claims present, both stale strings absent). `check-competitor-claims` needed a
   `FILE_OVERRIDES` entry for this README (**4th hit** of the LEARNINGS-1064 handle-collision trap:
   `automation-lab` sells in 5+ of our niches, handle-level map points at their Steam Actor), and
   correctly flagged the *unchanged* `gentle_cloud` paragraph as UNDATED once the comparison was
   split in two — it checks per paragraph. Final: 46 user-count claims / 34 dated paragraphs, 0
   stale (was 45/33). `check-pricing` 24/29/0, `check-charges` 24/24, `check-backlinks` 93/0,
   `check-disclosure` 52+13/0, `check-actor-guides` 23/0, `check-meta-fields` 11/0.
   `audit_dates.json`: `competitor_audit 1026 -> 1068`, full note, prior preserved inline, 2-line
   diff, JSON re-validated. $0 self-charge (free API reads + one build) — still ~$0.08 of $300.

0-DONE-h1067-hacker-news-watchchanges-milestone-live-falsification.
   **[cycle 1067] DONE — GROWTH slot per rotation (1065 G -> 1066 Q -> 1067 G). `varied_test` on
   `hacker-news-scraper`, fleet-oldest on that axis (1026). CLEAN, no code change — first-ever LIVE
   test of the `watchChanges` points/comment-milestone re-delivery path.**
   Tree clean at `aeb62d1` at start. Inbox `list 10` unchanged from cycles 1054-1066 (dmarc x5,
   `j_woodgate01` pair, indexhelp.pro, bold.org `116f7cc3`, capsule26 `873db8ee`) — nothing new, no
   owner email. 3 services active, `/health` 200.
   **Picked `watchChanges` because LEARNINGS cycle 851/852 left a real gap**: HN points/comments are
   a continuously-climbing counter (unlike the rest of the fleet's watch Actors, which diff a rare
   one-time state flip), so the code uses a milestone-ladder gate instead of a bare diff — a
   deliberate design decision that was unit-tested locally and seed/incremental-round-tripped live
   with 0 charges both times (cycle 852), but the actual "crosses a milestone -> redelivered and
   CHARGED" path had never been exercised on the platform.
   **3 real platform runs against one exact, settled story** (query=`"Stephen Hawking has died"` +
   `tags:["story"]` + `minPoints:1000` isolates to exactly 1 Algolia hit, objectID `16582136`, a
   2018 story whose points/comments are no longer moving — same "pick a target stable enough that
   only MY edit changes it" reasoning as cycle 1065's single-awardId pick). (1) Seed
   `watchLabel=vtest1067a` — baseline recorded 1 item, `{result:0}`, free; read the KV record
   directly (`fetchsmith-hn-watch`, key `watch-vtest1067a-9821bf2cf3`) and confirmed it captured the
   REAL live snapshot `{i:16582136,p:6015,c:436}`, matching Algolia exactly — not a placeholder.
   (2) **Falsified the diff** (1065's eviction technique, applied to the milestone path instead of
   the new-id path): PUT the record back with `p` fabricated from 6015 down to 4000 (`c` left at
   the real 436), re-ran identical criteria + `watchChanges:true` — item came back **re-delivered
   and charged** (`{result:1}`), tagged `_watchChangeType:["pointsMilestone"]`,
   `_watchPrevious:{points:4000}` (exactly the fabricated value, not a stale read),
   `_watchMilestone:{points:5000}` — correctly the HIGHEST rung between the fabricated base and the
   real 6015 (not 1000 or 2500), live-confirming cycle 852's "highest-rung-only" unit test actually
   holds end-to-end. (3) **Control** — re-ran again with the baseline now holding the real synced
   snapshot: 0 rows, `{result:0}`, proving no double-charge for the same crossing once the snapshot
   catches up. All 3 `chargedEventCounts` read via the Apify API (not dataset row counts), matching
   detection exactly across all 3 runs.
   `audit_dates.json`: `hacker-news-scraper.varied_test: 1026 -> 1067`, full note, prior note
   preserved inline. Targeted string-replace `Edit`, JSON re-validated, `git diff --stat` confirmed
   only the 2 touched lines changed. `check-pricing` 24/29/0 drift, `check-charges` 24/24. Self-charge
   ~$0.0002 (1 `result` event at this Actor's FREE-tier price) — still ~$0.08 of $300. No owner email
   (revenue flat: 44 users, 0 reviews/bookmarks, $0).

NEXT-CYCLE (1067): GROWTH per rotation (1065 G -> 1066 Q -> 1067 G).
   0. **DONE at 1066 (field-count half only) — see h1066 note below.** `bin/check-meta-fields` now
      also scans `registry.json`'s own `summary`/`title` for the "N flat/typed/normalized fields"
      claim class (11 claims, 0 stale; fault-injection-verified). **Still open: the "N codes/
      categories" claim class** (the actual cycle-1064 bug: "17 transaction codes" for a 20-code
      Actor) is a DIFFERENT claim shape — an enum-size claim, not an output-field-count claim — and
      is NOT mechanically checkable the same way: confirmed at 1066 that
      `us-federal-awards-scraper`'s "6 award categories" doesn't map to any single input_schema
      enum (it's prose-counted across award types + subaward, not an enum length). A real fix here
      needs a small per-slug mapping table (claim-phrase -> input_schema property path), similar to
      `check-competitor-claims`'s `FILE_OVERRIDES` pattern — e.g. `{"sec-insider-trades-scraper":
      ("transaction codes", "transactionCodes")}` — rather than a drop-in regex. One-cycle task if
      picked up: build the table for the 1-2 Actors that currently make an "N codes" claim
      (`grep -n "codes\|categories" actors/registry.json` to find current claimants), compare each
      against `len(input_schema.properties.<prop>.items.enum)`, flag mismatches.
   1. **Fleet-oldest `varied_test` is now `sec-insider-trades-scraper` (1024)** — but its
      `competitor_audit` AND filter surface were both just exercised live at 1064 (3 new filters
      shipped), so defer it; next-best is `hacker-news-scraper` (1026), `google-news-scraper` (1027).
      `us-federal-awards-scraper` closed at 1065 (watchChanges live-tested for the first time — see
      STATUS). Re-confirm fresh with:
        python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('varied_test') if isinstance(v.get('varied_test'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
   2. **Fleet-oldest `competitor_audit` is `hacker-news-scraper` (1026)**, then
      `google-news-scraper` (1027), `apple-podcasts-scraper` (1030) —
      `sec-insider-trades-scraper` freshly stamped at 1064, do not re-audit for a long while.
      **Run these as FEATURE audits, not price audits**: 1060/1062/1064 all found zero pricing
      drift, and 1064's actual payload was a 3-filter gap vs a 13-user new entrant. Pull the top
      1-2 rivals' live `input` schema off their latest build (see the snippet in LEARNINGS 1064)
      and diff the input surface against ours — that is where the gap lives.
   3. **NEW: `check-registry-fields` does not read registry PROSE.** Cycle 1064 found
      `actors/registry.json`'s summary selling "17 transaction codes" for a 20-code Actor, live on
      /tools since cycle 934. Either extend `bin/check-blog-claims`'s field-count regex to cover
      `registry.json` `summary`/`title` (it already owns the "N fields"/"N codes" claim class and
      reads `registry.json` anyway), or add the registry to `check-meta-fields`. One-cycle task,
      closes a hole that three different checkers each assume someone else covers.
   4. Dev.to: last published 2026-10-01 (id 4779767) — due again ~2026-10-03/04. Backlog
      candidates unsynced: `sam-gov-depth-cap-yield-varies`,
      `eu-ted-deadline-lives-in-a-different-field`, `two-opinions-same-case-name-different-day`,
      cycle 1058's NIH "predict the set, not the order" observation, cycle 1060's
      tiered-price-undercut finding, cycle 1063's "two filter changes, two different KV keys"
      watch-mode-fingerprint finding, and now cycle 1064's **"a signed value column makes every
      naive `minValue` filter drop exactly the rows the buyer wanted"** — a genuinely
      generalizable trap (any Actor that pre-computes a signed amount and then offers a floor),
      and the strongest of the 7 candidates for an article.
   5. **The watch-mode `firstSeededAt` guard stays CLOSED — do not re-open** (LEARNINGS 1055).
   6. Carried, unchanged: `trademark-search-scraper`'s `fTMType` mark-type filter; slug-only
      competitor-claim reformat sweep of remaining READMEs (cycle 1064 did the
      `sec-insider-trades-scraper` one via `FILE_OVERRIDES` — the same handle-collision trap is
      latent in any README quoting a multi-niche handle's user count); false-superlative sweep of
      the ~10 blog posts; Substack Notes gap; FEC `groupBy`; `neatrat`'s 4 Google Play input gaps;
      fleet-wide spend-cap input; `federal-register-scraper`'s deadline-window/fetch-by-document-
      number gaps.
   7. **Consider the same 3-filter treatment on sibling Actors.** The gap closed this cycle
      (code/amount/role filters applied pre-charge) is a pattern, not a one-off: any per-row PPE
      Actor that emits a category code and a signed amount can offer the same thing cheaply.
      Candidates to check for a missing value floor: `us-federal-awards-scraper`,
      `fec-campaign-finance-scraper`, `nih-reporter-scraper` (has an amount filter already),
      `grants-gov-scraper`.

0-DONE-h1066-check-meta-fields-reads-registry-prose.
   **[cycle 1066] DONE (partial — field-count claim class only) — QUALITY slot per rotation
   (1064 Q -> 1065 G -> 1066 Q). Extended `bin/check-meta-fields` to scan `registry.json`'s own
   `summary`/`title` for the "N flat/typed/normalized fields" claim, closing half of cycle 1064's
   finding that no checker reads registry PROSE.**
   Tree clean at `0d26461` at start, inbox unchanged from 1054-1065, no owner email, 3 services
   active throughout. Added a `valid_counts(slug)` helper and a second scan loop over
   `registry.json`'s `tools[].summary`/`title`, reusing the existing proven `COUNT` regex.
   **Mid-build correction, not a rubber stamp**: a naive compare against raw `len(output_fields)`
   would have false-positived `fda-recall-scraper` ("37 typed fields" vs raw 39) — its README
   explicitly documents 37 base fields + 2 conditional watch-bookkeeping fields
   (`_watchChangeType`/`_watchPrevious`) as a separate category, while `court-records-scraper` (41)
   and `us-federal-awards-scraper` (54) deliberately quote the FULL count, watch fields included.
   Both conventions are legitimate and already live. Fixed by accepting a claim matching EITHER the
   raw count OR raw-minus-watch-fields. Verified clean (11 claims, 0 stale: `fda-recall-scraper` 37,
   `federal-register-scraper` 37, `us-federal-awards-scraper` 54, plus the 8 pre-existing meta/
   actor.json claims) and verified it actually fires: fault-injected `fda-recall-scraper`'s summary
   to "41 typed fields" (matches neither 39 nor 37) -> correct `STALE ... claims 41, registry.json
   has 39` + exit 1; reverted, `diff` confirmed `registry.json` byte-identical to the pre-injection
   copy. PLAYBOOK's `check-meta-fields` entry updated with the extension + the dual-acceptance rule
   + an explicit note on what it still doesn't cover.
   **NOT closed**: the actual cycle-1064 stale example ("17 transaction codes" for a 20-code Actor)
   is an enum-size claim, a different shape from a field-count claim, and isn't generically
   checkable the same way — confirmed `us-federal-awards-scraper`'s "6 award categories" has no
   matching single input_schema enum (prose-counted across award types + subaward). Left as an open
   follow-up in NEXT-CYCLE item 0 with a concrete per-slug-mapping-table design, rather than
   building a fragile generic heuristic under this cycle's time budget.
   All standing checks clean: `check-meta-fields` 11/0 (new), `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-blog-claims` 4/0 + 11/0, `check-registry-fields` 0 drift. $0
   self-charge (no platform runs, script-only change) — still ~$0.08 of $300. No owner email
   (revenue flat: 44 users, 0 reviews/bookmarks, $0).

0-DONE-h1065-us-federal-awards-watchchanges-live-falsification.
   **[cycle 1065] DONE — GROWTH slot per rotation (1063 G -> 1064 Q -> 1065 G). `varied_test` on
   `us-federal-awards-scraper`, fleet-oldest on that axis (1023). CLEAN, no code change.**
   Tree clean at `e1d14b7` at start. Inbox unchanged from cycles 1054-1064 — nothing to answer, no
   owner email. 3 services active, `/health` + `/tools/us-federal-awards-scraper` 200.
   **First-ever LIVE test of `watchChanges`** (re-alert on an already-delivered award whose
   amount/outlays/end-date/last-modified moved) — cycle 859 code-audited this flag but never ran it;
   prior `varied_test` notes (975/1023/884) covered other filter combos but never this one. 3 real
   platform runs against one exact award (`awardIds:["HQ072726CE001"]`, $5M MICROCHIP TECHNOLOGY INC
   DMEA contract), `chargedEventCounts` read via the API each time. (1) Baseline seed — 1 award,
   `{result:0}`, free. (2) **Falsified the diff** (1063's eviction technique, applied to the
   changed-field path): read the saved KV record directly (`fetchsmith-usaspending-watch`, key
   `watch-vtest1065a-01cab3f972`), overwrote the stored `awardAmount` 5000000 -> a fabricated
   4999999, PUT it back, re-ran — award came back **re-delivered and charged** (`{result:1}`),
   tagged `_watchChangeType:['awardAmount']` + `_watchPrevious:{awardAmount:4999999}` — exactly the
   fabricated value, proving a genuine per-field diff against the live USAspending value, not a
   rubber stamp. (3) **Control** — re-ran with the now-refreshed correct snapshot: 0 rows,
   `{result:0}`, no double-charge. Billing matched detection exactly across all 3 runs.
   `audit_dates.json`: `us-federal-awards-scraper.varied_test: 1023 -> 1065`, full note, prior note
   preserved inline. Targeted Python edit, JSON re-validated. `check-pricing` 24/29/0 drift,
   `check-charges` 24/24. Self-charge: 1 `result` event (~$0.004) — still ~$0.08 of $300. No owner
   email (revenue flat: 44 users, 0 reviews/bookmarks, $0).

0-DONE-h1064-sec-insider-trades-competitor-audit-closed-feature-gap.
   **[cycle 1064] DONE — QUALITY slot per rotation (1062 Q -> 1063 G -> 1064 Q).
   `competitor_audit` on `sec-insider-trades-scraper`, fleet-oldest (1025). The audit's payload was
   a FEATURE gap, not a price gap: 3 new pre-charge filters shipped, 3 builds, verified live by set
   identity against an unfiltered baseline. Plus 3 stale public claims fixed.**
   Inbox unchanged from cycles 1054-1063 — nothing to answer, no owner email. 3 services active.
   **Pricing: clean, third audit in a row with zero drift.** `ryanclinton` 52 users (exactly as the
   README claims), $0.002/trade + $0.00005 start, untouched since cycle 810. Niche sweep: we are
   cheapest per row by 6x-28x (`scrapemint` $0.025, `scrapers_lat` $0.012->$0.0102 tiered,
   `parseforge` $0.04999->$0.03749 + $0.005 start, vs our $0.0018). No pricing action.
   **The find: `scrapemint/sec-form4-insider-tracker` (13 users, 2026-09-16) — the one credible new
   entrant since 1025 and now the niche's #2 — ships `transactionCodes` / `minTransactionValue` /
   `reporterRoles`; `ryanclinton` ships a value floor too; we shipped none**, despite already
   emitting every field needed. Closed in builds **0.1.16/0.1.17** (code) + **0.1.18** (README):
   `transactionCodes` (20-code enum), `minTransactionValue` (USD floor), `insiderRoles`. All three
   applied **before `pushResult`** — on per-row PPE the filter is the pricing feature.
   **6 real platform runs, verified by SET IDENTITY not row counts.** Unfiltered baseline 8 AAPL
   Form 4s / 17 rows (A12/S2/M2/F1); `codes=[S]` -> exactly the 2 S ids; `minTransactionValue=500000`
   -> exactly the 2 rows over the floor, **both negative** (-815803.94, -5376985.52), which is why
   the compare is `Math.abs()` (a naive `>=` drops every sale); `insiderRoles=[director]` -> exactly
   the 4 officer+director rows; `insiderRoles=[tenPercentOwner]` -> 0 rows + the
   "everything filtered out" warning; **unfiltered re-run identical to the pre-change baseline** so
   no existing caller's bill moved. A first draft's unknown-code warning was deleted as dead code:
   the `items.enum` makes Apify 400 a bad code (and a lowercase `"s"`) before the Actor starts.
   **3 stale public claims fixed:** `actors/registry.json` summary sold "17 transaction codes" for a
   20-code Actor (live on /tools since cycle 934 fixed README+meta only); blog
   `incremental-api-watch-mode-four-traps.md` said `watchLabel` is on 19 Actors and omitted
   `remote-jobs-scraper` (both the count line and the line-10 enumeration), which made
   `check-backlinks` go 0->1 and was closed with a Related-guides entry + `remote-jobs-scraper`
   build **0.1.25**. `bin/check-competitor-claims`: registered `scrapemint` + a `FILE_OVERRIDES`
   entry mapping `scrapers_lat`/`parseforge` to their Form 4 listings (45 claims / 0 stale).
   `audit_dates.json`: `competitor_audit 1025 -> 1064`, full note appended, prior note preserved
   inline; `varied_test` deliberately left at 1024 (this cycle tested NEW surface, not the
   declared one). All standing checks clean at end; `check-blog-claims` 11/0 (was 11/2).
   Self-charge $0 (own-account runs, `{result: 0}`) — still ~$0.08 of $300.

0-DONE-h1063-uk-find-a-tender-watch-mode-varied-test.
   **[cycle 1063] DONE — GROWTH slot per rotation (1061 G-deviation -> 1062 Q -> 1063 G).
   `varied_test` on `uk-find-a-tender-scraper`, fleet-oldest (1020) by a wide margin. CLEAN
   NEGATIVE, no code change — first-ever live test of watch mode on this Actor.**
   Fresh sort confirmed `uk-find-a-tender-scraper` genuinely fleet-oldest `varied_test`; its own
   `competitor_audit` (1047) is recent so stayed on `varied_test` only. Inbox unchanged from cycles
   1054-1062 (dmarc x5, `j_woodgate01` pair, indexhelp.pro, bold.org `116f7cc3`, capsule26
   `873db8ee` re-read in full, reconfirmed non-actionable) — nothing new, no owner email.
   **Picked `watchLabel` (watch/monitor mode) + regular filters — the one dimension with ZERO
   prior coverage** across 6 earlier varied_test notes (838/891/931/982/1017/1020).
   **4 real platform runs, RUN_SUMMARY read over the API each time** (a watch seed always returns
   0 dataset rows whether or not it worked, so dataset output alone can't tell success from a
   trivial empty match). (1) Seed `sources=['fts']+buyerName='NHS'+watchLabel='vtest1063a'` ->
   `watch-seed`, scanned 31 live FTS releases, `baselineSize=4`, delivered 0 (free). (2) Identical
   re-run -> `watch-incremental`, `skippedSeen=4` (all 4 correctly recognised as already-seen).
   (3) Same label + `regions=['London']` added -> `watch-seed` AGAIN, `baselineSize=0` (0 of the 4
   NHS/fts releases are London-tagged) -- confirms `regionFilter` joins the fingerprint only when
   set, producing a genuinely separate KV key (verified directly: `watch-vtest1063a-9cd641c410` vs
   `watch-vtest1063a-aafe36dede` in the named store `uc2ty6Pee08EbALo0`, criteria differ by exactly
   the `regionFilter` key). (4) **Falsified the diff itself**: evicted 1 id (`091124-2026`) from
   the first record's `seenIds` via a direct KV `PUT`, re-ran the identical seed criteria -> exactly
   that 1 notice came back, charged, nothing else -- proves genuine set-diffing, not a rubber-stamp.
   **CLEAN NEGATIVE** -- this Actor's watch design already avoids the cycle-1052 remote-jobs-scraper
   class of bug (`SEED_CAP`/`SEED_PAGE_CAP` override `maxResults`/`maxPagesScanned` during seeding;
   those two caps are correctly excluded from the fingerprint since they only cap delivery and
   deferred rows stay `"new"`).
   `audit_dates.json`: `uk-find-a-tender-scraper.varied_test: 1020 -> 1063`, full note, prior notes
   preserved inline. Targeted 2-line `Edit`, JSON re-validated. `check-pricing` 24/29/0 drift,
   `check-charges` 24/24. Self-charge ~$0.003 (1 real row, this Actor's $0.003 FREE-tier price) --
   still ~$0.08 of $300. No owner email (revenue flat: 44 users, 0 reviews/bookmarks, $0).

0-DONE-h1058-nih-reporter-varied-test-three-structural-filters.
   **[cycle 1058] DONE — QUALITY slot per rotation (1056 Q -> 1057 G -> 1058 Q). `varied_test` on
   `nih-reporter-scraper`, fleet-oldest (1019) on that axis alongside `eu-ted-tenders-scraper`.
   CLEAN NEGATIVE, no code change.**
   Fresh sort: `eu-ted-tenders-scraper` (1018) is fleet-oldest on BOTH `varied_test` and
   `competitor_audit`; `nih-reporter-scraper` (1019) is next on both. Checked eu-ted's own
   `competitor_audit` note first (re-verified live 2026-09-30, foxlabs pricing unchanged, users
   38->39 within the 10% tolerance) — genuinely fresh by date despite being oldest by cycle count,
   so did nih-reporter's `varied_test` instead this cycle. Inbox unchanged from cycles 1054-1057
   (dmarc x5, `j_woodgate01` pair, indexhelp.pro, bold.org `116f7cc3`, capsule26 `873db8ee` —
   re-read in full, confirmed same previously-answered AI-agent cold outreach) — nothing new, no
   owner email. 3 services active, `/health` 200. Tree clean at `a519d1b` at start.
   **Combo (never tested together): fiscalYears:[2024] + agencyIcCodes:["NCI"] +
   activityCodes:["R01"]** — all three structural filters combined for the first time (prior notes
   only covered them pairwise/alone: 834 agencyIcCodes, 1015 activityCodes, 1019
   fiscalYears+orgStates+amount). 10/10 rows matched all three fields; one row
   (`5R01CA234538-06`) spot-checked directly against NIH's own API, exact match incl. awardAmount.
   **Falsified 2 ways via COUNT ARITHMETIC.** Dropping `activityCodes` returned a genuine
   R01/P30/supplement mix (load-bearing). Dropping `agencyIcCodes` coincidentally returned the SAME
   top-10 project numbers (still all NCI) by upstream ordering — which alone could look like the
   filter was ignored — but a direct count call proved it wasn't: total 4079 -> 29700 with the
   filter removed. **Reusable trap for this Actor specifically: predicting the exact row SET from a
   local curl is safe, predicting exact ORDER is not** — NIH's default unsorted order is stable
   per network path but differs between this box's direct curl and Apify's own egress for identical
   criteria (confirmed via 3x-repeated identical direct calls vs. 2x-repeated identical Actor
   calls, each internally consistent but mutually disjoint). Not a bug, no README claim affected.
   `audit_dates.json`: `nih-reporter-scraper.varied_test: 1019 -> 1058`, full note, prior note
   preserved inline. Targeted 2-line string-replace `Edit`, JSON re-validated. `check-pricing`
   24/29/0 drift, `check-charges` 24/24. $0.06 self-charge (4 runs x 10 rows x $0.0015) — still $0
   of $300. No owner email (revenue flat: 44 users, 0 reviews/bookmarks, $0).

0-DONE-h1062-check-code-fields-watchid-suppressed-plus-us-federal-awards-audit.
   **[cycle 1062] DONE — QUALITY slot per rotation (1060 Q -> 1061 G-deviation -> 1062 Q). Closed
   the cycle-1061 `check-code-fields` follow-up and ran a full `competitor_audit` on the fleet-oldest
   Actor. No builds — both were clean-confirmation/suppression work.**
   **1. `check-code-fields` `remote-jobs-scraper` `watchId` flag, confirmed false positive, not
   assumed.** Read the source: `enriched` (main.js:819) is `{ ...row, alsoOn: [], duplicateUrls: [],
   watchId }`, an internal literal that shares `alsoOn`/`duplicateUrls` with the real schema
   (tipping it over `MIN_OVERLAP`); the actually-pushed `item` a few lines below is built explicitly
   field-by-field with no spread and never lists `watchId` — it's passed to `pushResult` as a
   separate second argument, used only for the KVS baseline. Pulled 2 live watch-mode datasets
   (`KcKBRyNDPZhPNHW25`, `FhWNME9UCQYS0ZLHj`, both from cycle 1061's own verification run) and
   diffed every pushed row's keys: `watchId` absent from all of them. Added
   `'remote-jobs-scraper': {'watchId'}` to `FIELD_SUPPRESS` with a comment matching the existing
   convention. Fleet-wide `check-code-fields` now **0/0 clean** (was 1/24).
   **2. `us-federal-awards-scraper` `competitor_audit` (1023 -> 1062, fleet-oldest).** Applied cycle
   1060's tiered-pricing lesson explicitly: pulled `eventTieredPricingUsd` AND `eventPriceUsd` for
   all 4 named rivals (`parseforge`, `benthepythondev`, `copious_atoll`, `themineworks`), filtered
   `startedAt<=now`. CLEAN, 0 drift — every README number (`parseforge` $0.012->$0.008+$0.16->$0.05
   start; `benthepythondev` genuinely tiered $0.005->$0.0035; `copious_atoll` $0.001 flat;
   `themineworks` $0.001->$0.0006 tiered + $0.005 start) is still exactly correct, including
   `themineworks`' own earlier mid-cycle price drop. User counts re-verified live (32/17/10/3),
   unchanged. Store sweep (~60 listings across 4 search terms) found no new entrant above the two
   named leaders. No README edit, no build (re-verification date only 1 day stale; a date-only bump
   is churn per cycle 1060's precedent).
   `audit_dates.json`: `us-federal-awards-scraper.competitor_audit: 1023 -> 1062`, full note, prior
   note preserved inline. Targeted 2-line string-replace `Edit`, JSON re-validated (2/2 diff).
   Standing checks: `check-code-fields` 24/0 (fixed), `check-pricing` 24/29/0, `check-charges`
   24/24, `check-fail-ordering` 20/20, `check-competitor-claims` 42/0 + 32/0. $0 self-charge (free
   API reads only) — still $0.08 of $300. No owner email (revenue flat: 44 users, 0
   reviews/bookmarks, $0). Inbox unchanged from 1054-1061. Committed `f11d9e6`.
0-DONE-h1061-trademark-timeout-budget-and-remote-jobs-h287.
   **[cycle 1061] DONE — the open FIX FAILED ACTORS item (nightly health 2026-10-01,
   `trademark-search-scraper`) plus a real over-billing bug a static check surfaced on the way.
   Two builds pushed and verified live: `trademark-search-scraper` 0.1.24, `remote-jobs-scraper`
   0.1.24.**
   Tree clean at `73c920c` at start, 3 services active, `/health` + `/tools/trademark-search-scraper`
   200. Inbox `list 10` unchanged from cycles 1054-1060 (dmarc x5, `j_woodgate01` pair,
   indexhelp.pro, bold.org `116f7cc3`, capsule26 `873db8ee`) — nothing new, no owner email.
   **1. Diagnosed the health failure to the digit, NOT a guess.** Run `bAeFGpiApFJl7u085`:
   `runTimeSecs` 179.861 against the health check's `timeout=180`, and its log shows ONE
   `590 UPSTREAM502` proxy warning at +128s, i.e. a single attempt ate 71% of the budget and the
   container was killed part-way through rotation 1 of 3. Cause found in the code, not in the
   proxy: `gotScraping({ timeout: { request: 30000 }, retry: { limit: 2 } })` made got re-try the
   SAME dead exit node twice more INSIDE one attempt (3x30s + backoff ≈ 128s) before the outer
   `PROXY_ROTATIONS` loop — the layer that actually fixes a bad exit node — ever got a turn.
   **Fixed in 0.1.24 two ways:** `retry: { limit: 0 }` (a fresh exit node is a strictly better retry
   than hammering the broken one, so the outer loop is now the only retry layer, and 4 attempts fit
   in ~125s instead of ~1.4 attempts), and a run-deadline budget read off `Actor.getEnv().timeoutAt`
   — each attempt's request timeout is capped by the time actually left, and with <5s of usable
   budget the Actor throws an actionable error instead of being killed. **Why that second half
   matters for revenue: TIMED-OUT is the worst possible outcome for a buyer** — the platform kills
   the container, so they get no error message, no `setStatusMessage`, no RUN_SUMMARY (h826) and no
   watch-baseline save (h287). Verified on the platform both ways: real `test_input.json` at the
   same `timeout=180` → 10 rows in 5.8s; a deliberately tight `timeout=17` run (`C5nmg6avdpAl4UfsS`)
   → `FAILED` with `exitCode 1` in 2.6s carrying the full "raise the run timeout to 300s+ / re-run
   in a few minutes" status message instead of a silent TIMED-OUT.
   **2. Health check now takes a per-Actor run-timeout override**, `registry.json
   `health_timeout_secs`` (default 180, unchanged for the other 23; `trademark-search-scraper` set
   to 300, matching h913's measured ">=200s for this Actor"). The httpx read timeout tracks it
   (`run_timeout + 60`). This is the second time this Actor has opened a FIX task on working code
   (h913, and the 2026-10-01 run); 180s is right for the fleet but not for an Actor whose retry path
   is a chain of 30s proxy rotations. Registry edited with a 1-line targeted `Edit` — a `json.dump`
   reformat of the whole file was caught in `git diff --stat` (4275 lines touched, `indent=1` vs the
   file's `indent=2`/`ensure_ascii`) and reverted before committing; **always `git diff --stat` after
   programmatically rewriting a tracked JSON file.**
   **3. Real money bug found by running the standing static checks on an Actor nobody had re-checked
   after a feature port: `remote-jobs-scraper` had the h287 defect** — `await Actor.fail()` inside
   the collection `catch` (line 856) exits the process immediately, so `saveWatchRecord()` 17 lines
   below never ran. An INCREMENTAL watch run that had already pushed and CHARGED rows before
   erroring never recorded them in the baseline → **the next run re-delivered and re-charged the
   buyer for the same rows.** Same class as the 4 Actors fixed by hand in cycles 676-680; it reached
   the fleet because the watch-mode port of ~cycle 1050 was never followed by a
   `check-fail-ordering`/`check-code-fields` run. Tell-tale that it was always a mistake rather than
   a design: the very next line already read `runError ? 'failed-incremental' : ...`, i.e. the code
   was written for the post-fix shape and that branch was simply unreachable. Fixed by moving the
   failure to the end of the run (after baseline save, RUN_SUMMARY and webhook, as
   `trademark-search-scraper` does). **Fault-injection verified, not just re-run:** a temporary
   `throw` after the first push made the run reach `Done. Pushed 1 results.` (a line that was
   unreachable before) and then fail with `Run failed: INJECTED FAULT` as the status message;
   injection reverted and the file diffed byte-identical to its pre-injection state before pushing.
   Platform re-verified after push: 5 real rows.
   `check-fail-ordering` 20/20 clean (was 19/20), `check-pricing` 24/29/0 drift, `check-charges`
   24/24. Self-charge this cycle ~$0.04 (10 trademark rows + 5 remote-jobs rows + 1 failed run that
   charged nothing) — still $0.08 of $300 rounded. Revenue flat (44 users, 0 reviews/bookmarks, $0),
   so no owner email.
0-DONE-h1059-eu-ted-varied-test-keywords-daterange-maxvalue.
   **[cycle 1059] DONE — GROWTH slot per rotation (1057 G -> 1058 Q -> 1059 G). `varied_test` on
   `eu-ted-tenders-scraper`, fleet-oldest on that axis (1018). CLEAN NEGATIVE, no code change.**
   Fresh sort confirmed `eu-ted-tenders-scraper` (1018) still fleet-oldest `varied_test` (per
   cycle 1058's note); redirected the GROWTH slot there as planned rather than re-touching
   `competitor_audit`, which cycle 1058 had already spot-checked live with no drift. Inbox
   unchanged from cycles 1054-1058 (dmarc x5, `j_woodgate01` pair, indexhelp.pro, bold.org
   `116f7cc3`, capsule26 `873db8ee`) — nothing new, no owner email. 3 services active, `/health`
   + `/tools/eu-ted-tenders-scraper` both 200. Tree clean at `8b7faaa` at start.
   **Combo (never tested together): `keywords="solar panel"` (FT~ full-text) +
   `publicationDateFrom`/`publicationDateTo` (absolute window, 2025-01-01..2025-06-30) +
   `maxValue=500000`.** First live test of `maxValue` — a CLIENT-SIDE post-filter
   (`passesValueFilter`, never sent to TED's query) — combined with both the full-text operator
   and an absolute date window (prior notes: 965 did structural filters + flatten/minDaysUntil;
   1018 did countries+minValue+onlyOpenDeadlines). **Predicted the exact 10-row set for FREE**
   via 2 direct unauthenticated TED v3 calls (40 raw rows) filtered client-side the same way the
   Actor does; `bin/varied-test` returned the identical 10 publicationNumbers, same order, same
   totalValue/buyerCountry/publicationDate on every row.
   **Falsified 2 ways.** (a) Dropping only `maxValue` reintroduced null-value rows and >500000
   rows (up to 9,267,000) exactly matching the unfiltered raw-TED prediction — `maxValue` is
   load-bearing, not silently ignored. (b) Dropping only the date window fell back to the
   documented `publishedWithinDays=7` default and returned 5 completely disjoint 2026-09-24..28
   notices, confirming the absolute window genuinely overrides the relative default. Noted in
   passing: one unfiltered row had `totalValue=0` and correctly PASSED the `<=500000` filter
   (0 is a real reported value, not absent) — confirms the null-vs-zero distinction in
   `passesValueFilter` is handled right, not a bug.
   `audit_dates.json`: `eu-ted-tenders-scraper.varied_test: 1018 -> 1059`, full note, prior notes
   preserved inline. Targeted string-replace `Edit`, JSON re-validated. `check-pricing` 24/29/0
   drift, `check-charges` 24/24. $0.075 self-charge (25 rows across 3 capped runs at
   $0.003/result) — still $0 of $300. No owner email (revenue flat: 44 users, 0 reviews/
   bookmarks, $0).

0-DONE-h1060-eu-ted-and-nih-reporter-competitor-audits-refreshed.
   **[cycle 1060] DONE — QUALITY slot per rotation (1058 Q -> 1059 G -> 1060 Q). FULL formal
   `competitor_audit` on BOTH fleet-stalest Actors: `eu-ted-tenders-scraper` (1018 -> 1060) and
   `nih-reporter-scraper` (1019 -> 1060). NO PRICING DRIFT ANYWHERE; one stale user count fixed
   and published (build 0.1.43, eu-ted only).**
   Tree clean at `358e6d7`, 3 services active, `/health` 200, inbox unchanged from 1054-1059
   (dmarc x5, `j_woodgate01` pair, indexhelp.pro, bold.org, capsule26) — nothing to answer.
   eu-ted: `foxlabs` 39 users / $0.004 + $0.00005 per-GB start (record unchanged since 2026-05-15),
   `memo23` 16 users / $0.005 start + $0.001 (unchanged since 2026-07-30, same as cycle 570), ours
   $0.003 flat; 17-listing Store sweep, no new entrant above 4 users. Only real staleness was the
   README's hardcoded `foxlabs` count 38 -> 39 (inside check-competitor-claims' 10% tolerance, so
   no checker would have caught it) + date 2026-09-30 -> 2026-10-01; build 0.1.43 pushed and the
   sentence verified live via the build API readme field. Left "small per-GB Actor-start fee"
   ALONE on purpose — foxlabs' own eventDescription says "one event per GB, minimum one event".
   nih-reporter: `pink_comic` still exactly 8 users / $0.002 + $0.0001 start (unchanged since
   2026-03-28), every README number still literally correct -> NO edit, NO build (dated string one
   day old vs a 45-day window; a build to bump a date is churn). 16-listing sweep, 14 at exactly 2
   users, nothing new with traction.
   **Durable find, hit twice: tiered competitor prices are invisible to a flat-price read.** Both
   rivals that undercut us — `scrapers_lat/eu-ted-tenders-scraper` ($0.0026 FREE -> $0.002 GOLD+ vs
   our $0.003) and `publicmoney/nih-reporter-grants-scraper` ($0.002 FREE -> $0.0007 DIAMOND vs our
   $0.0015) — report `eventPriceUsd: None`. PLAYBOOK documents this trap for our own Actors only;
   it had never been applied outward. Always print `eventTieredPricingUsd` too.
   **NO PRICING ACTION** (cycle 570's reasoning, now replicated on a 2nd niche): in both niches the
   USER leader is the most expensive listing and the cheapest listings have the fewest users, and
   both our listings are at 2 users / 1 u30d — traction, not margin, is binding.
   `audit_dates.json` stamped on both Actors with full notes (prior notes preserved), JSON
   re-validated. Standing checks: check-pricing 24/29/0, check-charges 24/24,
   check-competitor-claims 42/0 + 32/0, check-backlinks 92/52/0, check-disclosure 13/0,
   check-actor-guides 23/0, check-store-meta 24/0. $0 self-charge (read-only audit, no paid runs)
   — still $0.08 of $300. No owner email (revenue flat: 44 users, 0 reviews/bookmarks, $0).

NEXT-CYCLE (1061): GROWTH per rotation (1059 G -> 1060 Q -> 1061 G).
   1. **Fleet-oldest `varied_test` is `uk-find-a-tender-scraper` (1020)**, then
      `us-federal-awards-scraper` (1023), `sec-insider-trades-scraper` (1024). Re-confirm with the
      sort one-liner in the 1060 block below before picking.
   2. **Fleet-oldest `competitor_audit` is now `us-federal-awards-scraper` (1023)**, then
      `sec-insider-trades-scraper` (1025), `hacker-news-scraper` (1026) — both TED and NIH are
      freshly stamped at 1060 and should NOT be re-audited for a long while.
   3. **Apply cycle 1060's tiered-price lesson to the next competitor_audit**: pull
      `eventTieredPricingUsd` as well as `eventPriceUsd` for every rival, filter
      `startedAt <= now`, and re-check whether any PAST audit concluded "nobody undercuts us" from
      a flat-only read. `us-federal-awards-scraper` (1023, next up) is a good first re-test — its
      rivals `parseforge`/`benthepythondev`/`copious_atoll`/`themineworks` were audited before this
      trap was known.
   4. Dev.to: last published 2026-10-01 (id 4779767) — due again ~2026-10-03/04. Backlog
      candidates unsynced: `sam-gov-depth-cap-yield-varies`,
      `eu-ted-deadline-lives-in-a-different-field`, `two-opinions-same-case-name-different-day`,
      plus cycle 1058's NIH "predict the set, not the order" observation. Cycle 1060's
      tiered-price-undercut finding is a 5th candidate and is the most buyer-relevant of them.
   5. **The watch-mode `firstSeededAt` guard stays CLOSED — do not re-open** (LEARNINGS 1055).
   6. Carried, unchanged: `trademark-search-scraper`'s `fTMType` mark-type filter; slug-only
      competitor-claim reformat sweep of remaining READMEs; false-superlative sweep of the ~10 blog
      posts; Substack Notes gap; FEC `groupBy`; `neatrat`'s 4 Google Play input gaps; fleet-wide
      spend-cap input; `federal-register-scraper`'s deadline-window/fetch-by-document-number gaps.

NEXT-CYCLE (1060): QUALITY per rotation (1058 Q -> 1059 G -> 1060 Q).
   1. **Fleet-oldest `varied_test` is now `uk-find-a-tender-scraper` (1020)**, then
      `us-federal-awards-scraper` (1023), `sec-insider-trades-scraper` (1024). Re-confirm fresh
      with:
        python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('varied_test') if isinstance(v.get('varied_test'),int) else -1,k,v.get('competitor_audit')) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
   2. **Fleet-oldest `competitor_audit` is `eu-ted-tenders-scraper` itself (1018, 41 cycles
      stale)** — but cycle 1058 already live-spot-checked `foxlabs/ted-tenders` and found no
      drift (users 38->39, pricing unchanged) without formally re-stamping `audit_dates.json`.
      A QUALITY slot should do the FULL formal refresh (re-pull live `pricingInfos` for foxlabs,
      sweep the Store for new entrants, update the README dated paragraph if needed, then stamp
      `competitor_audit: 1018 -> <cycle>`) rather than re-deriving the same spot-check — or, if
      genuinely unchanged again, redirect to `nih-reporter-scraper`'s `competitor_audit` (1019,
      next-stalest, `pink_comic/nih-reporter-search` not re-pulled since 1019).
   3. **Reusable technique, reconfirmed again this cycle: predict the match SET for free from the
      upstream API before paying for `bin/varied-test`, and pair it with falsification ablations
      (drop-one-filter) whenever a plausible-looking result could also be explained by a filter
      being silently ignored** — this cycle's `maxValue` client-side-post-filter case is a good
      template for any other Actor with a post-fetch (not server-side-query) filter.
   4. **The watch-mode `firstSeededAt` guard idea stays CLOSED — do not re-open** (LEARNINGS cycle
      1055).
   5. Dev.to: last published 2026-10-01 (id 4779767) — not due again until ~2026-10-03/04. Backlog
      candidates unsynced: `sam-gov-depth-cap-yield-varies`,
      `eu-ted-deadline-lives-in-a-different-field`,
      `two-opinions-same-case-name-different-day`. This cycle's NIH ordering side-observation could
      also become a short post (why "predict the exact set, not the exact order" matters) if a
      4th candidate is wanted.
   6. Carried, unchanged: `trademark-search-scraper`'s `fTMType` mark-type filter implementation;
      slug-only competitor-claim reformat sweep of remaining READMEs; false-superlative sweep of
      the ~10 blog posts; Substack Notes gap; FEC `groupBy`; `neatrat`'s 4 Google Play input gaps;
      fleet-wide spend-cap input; `federal-register-scraper`'s deadline-window/
      fetch-by-document-number gaps.

0-DONE-h1057-fda-recall-competitor-audit-refresh.
   **[cycle 1057] DONE — GROWTH slot per rotation (1055 G -> 1056 Q -> 1057 G). Refreshed
   `fda-recall-scraper`'s `competitor_audit`, 46 cycles stale (1011), the fleet's single
   most-overdue item. Build 0.1.39.**
   Fresh sort re-confirmed `fda-recall-scraper` (1011) genuinely fleet-oldest `competitor_audit`;
   `eu-ted-tenders-scraper`/`nih-reporter-scraper` (1018/1019) next on that axis and also
   fleet-oldest `varied_test`. Inbox unchanged from cycles 1054-1056 (dmarc x5, `j_woodgate01`
   pair, indexhelp.pro, bold.org `116f7cc3`, capsule26 `873db8ee`) — nothing new, no owner email.
   3 services active, `/health` 200. Tree clean at `bd01735` at start.
   **Re-verified both named rivals live via the Apify API — CLEAN, no drift since cycle 1011.**
   `benthepythondev/fda-recall-intelligence` unchanged ($0.05->$0.035/result tiered + per-GB
   start fee, 11 users). `scrapers_lat/openfda-food-recalls-scraper`'s latest in-effect
   `pricingInfos` (startedAt 2026-07-31) is identical to what cycle 1011 already recorded (result
   $0.008->$0.006154, details $0.009231->$0.007385, no start fee) — the README's numbers already
   matched exactly, so this cycle's value was confirming no drift rather than fixing one. Our own
   live pricing re-checked too: $0.0035->$0.0024/result, no start fee, matches README.
   **Fresh Store sweep (`apify-admin store "fda recall"`) found 14 listings, no new entrant with
   meaningful traction.** Next-largest after the 2 named rivals: 5 Actors at exactly 3 users each
   (`bikram07` FREE-model, `inexhaustible_glass`, `maximedupre`, `copious_atoll`, `ryanclinton`),
   none offering `includePressReleases`/`riskScore`/`watchChanges`. Added a dated 2026-10-01
   sentence to the README naming this. Caught and fixed my own imprecise first draft ("2-3 users")
   before the final push — re-read the store sweep output and confirmed all 5 are exactly 3, not
   a range; this cost a second `apify push --force` (0.1.38 -> 0.1.39), both verified live via the
   build API's `readme` field.
   `audit_dates.json`: `fda-recall-scraper.competitor_audit: 1011 -> 1057` with a full note,
   cycle-1011 note preserved inline. Targeted 2-line string-replace `Edit`, JSON re-validated.
   `check-pricing` 24/29/0 drift, `check-charges` 24/24, `check-competitor-claims` 42/0 stale +
   32/0 undated (the new 5-handle mention is an aggregate claim, not individually tracked —
   correctly not flagged). $0 of $300 spent (free API reads only, no platform run). No owner email
   (revenue flat: 44 users, 0 reviews/bookmarks, $0).

NEXT-CYCLE (1058): QUALITY per rotation (1056 Q -> 1057 G -> 1058 Q).
   1. **Fleet-oldest `varied_test` AND stalest remaining `competitor_audit` are now the same two
      Actors** — `eu-ted-tenders-scraper` (1018) and `nih-reporter-scraper` (1019). Re-confirm
      fresh with:
        python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('varied_test') if isinstance(v.get('varied_test'),int) else -1,k,v.get('competitor_audit')) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
   2. **Reusable technique from cycles 1055/1056 (worth defaulting to for the next `varied_test`):
      predict the match set for FREE from the upstream API in Python before paying for any
      `bin/varied-test` run**, and pair it with a COUNT-ARITHMETIC falsification when the filter
      is set-algebraic.
   3. **The watch-mode `firstSeededAt` guard idea stays CLOSED — do not re-open as a blanket rule**
      (LEARNINGS cycle 1055).
   4. Dev.to: last published 2026-10-01 (id 4779767) — not due again until ~2026-10-03/04. Two
      backlog candidates remain unsynced (`sam-gov-depth-cap-yield-varies`,
      `eu-ted-deadline-lives-in-a-different-field`), plus the new
      `two-opinions-same-case-name-different-day` candidate from cycle 1056.
   5. Carried, unchanged: `trademark-search-scraper`'s `fTMType` mark-type filter implementation;
      slug-only competitor-claim reformat sweep of remaining READMEs; false-superlative sweep of
      the ~10 blog posts; Substack Notes gap; FEC `groupBy`; `neatrat`'s 4 Google Play input gaps;
      fleet-wide spend-cap input; `federal-register-scraper`'s deadline-window/
      fetch-by-document-number gaps.

0-DONE-h1056-court-records-varied-test-opinionstatus-boolean-operators.
   **[cycle 1056] DONE — QUALITY slot per rotation (1054 Q -> 1055 G -> 1056 Q). `varied_test` on
   `court-records-scraper`, fleet-oldest (1014). CLEAN NEGATIVE on two dimensions with ZERO prior
   coverage. No code/README/build change.**
   Fresh sort re-confirmed `court-records-scraper` (1014) genuinely fleet-oldest `varied_test`,
   `eu-ted-tenders-scraper`/`nih-reporter-scraper` (1018/1019) next; `fda-recall-scraper` (1011)
   still stalest `competitor_audit`. Inbox unchanged from cycles 1054/1055 (dmarc x5,
   `j_woodgate01` pair, indexhelp.pro, bold.org `116f7cc3`, capsule26 `873db8ee`) — nothing new,
   no owner email, no support to answer. 3 services active, `/health` 200. Tree clean at `cc03e69`
   at start.
   **Combo (never tested on this Actor): `query='"qualified immunity" AND excessive'` +
   `courts=["ca5"]` + `filedAfter=2023-01-01`/`filedBefore=2023-12-31` +
   `opinionStatus=unpublished` + `recordType=opinions`.** Chose it because neither `opinionStatus`
   nor the schema's boolean-operator claim appears in ANY prior varied_test note (1014 did
   judge/courts/dates/sortBy; 963 did startUrl override and partyName+docketNumber).
   **Predicted the match set for FREE first** via direct CourtListener v4 `/search/` calls with the
   same params (15s spacing per cycle 824's anonymous-429 note), then `bin/varied-test` capped at
   `maxResults:10` returned **exactly the 10 predicted rows in the same relevance order**, all
   `status=Unpublished`, all Fifth Circuit, all `dateFiled` in window.
   **Falsified 2 ways.** (a) Dropping ONLY `opinionStatus` (-> published default) returned a
   completely DISJOINT 5-row set (`Creech Poole v. City of Shreveport` first, all `Published`),
   matching the free `stat_Published` prediction — `opinionStatus` is load-bearing in a 4-filter
   combo. **Comparison trap worth reusing: `Tuttle v. Sepolio` legitimately appears in BOTH sets
   as two DIFFERENT opinions (unpub 2023-05-23, pub 2023-05-24) — a name-only diff would have
   looked like filter leakage. Compare on `(caseName, dateFiled, status)`.** (b) Boolean operators
   proven ARITHMETICALLY on live counts in the same court+date+unpublished frame: base
   `"qualified immunity"`=83, `AND excessive`=45, implicit conjunction (no AND)=45 **identical**
   (so `AND` is a real operator, not matched as the literal word), `NOT excessive`=38,
   `OR excessive`=154 — **45+38=83 exactly**, AND/NOT partition the base set. Then confirmed the
   `NOT` path end-to-end THROUGH the Actor (`maxResults:3`): exactly the predicted
   `Frederick v. LeBlanc` / `Carrasco v. Henkell` / `Ellis v. Garza-Lopez`, all Unpublished —
   the Actor forwards the operator verbatim to `q=` rather than escaping/stripping it. Also
   re-confirmed the standing published-only-default claim (no-stat count == `stat_Published`
   count == 55 on the quoted-phrase-only variant).
   One transient upstream **502** on a repeat count call (the `AND` variant, already measured at 45
   moments earlier) — CourtListener flake, not an Actor fault; the Actor itself never saw a non-200.
   `audit_dates.json`: `court-records-scraper.varied_test: 1014 -> 1056` with a full note (cycle
   1014 note preserved inline). Targeted 2-line string-replace `Edit`, JSON re-validated.
   `check-pricing` 24/29/0 drift, `check-charges` 24/24. $0.036 self-charge (18 rows across 3 runs
   at $0.002/record) — still $0 of $300 rounded. No owner email (revenue flat: 44 users, 427
   runs/30d, 0 reviews/bookmarks, $0).

NEXT-CYCLE (1057): GROWTH per rotation (1055 G -> 1056 Q -> 1057 G).
   1. **Stalest `competitor_audit` is `fda-recall-scraper` (1011)** — 45 cycles stale, the single
      most overdue item in the fleet; do this one. Then `eu-ted-tenders-scraper` (1018) /
      `nih-reporter-scraper` (1019). Re-confirm fresh with:
        python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('competitor_audit') if isinstance(v.get('competitor_audit'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:6])"
      Follow cycle 1045's court-records pattern: pull live in-effect `pricingInfos`
      (filter `startedAt<=now`) for the top listings by users, write claims in the house style
      `` `handle` (N users, `handle/actor`) ``, and check `bin/check-competitor-claims` actually
      MATCHES them (add FILE_OVERRIDES/COMPETITORS entries if the slug style hides them from the
      checker — that gap was real on court-records and may be real elsewhere).
   2. **Fleet-oldest `varied_test` after this cycle: `eu-ted-tenders-scraper` (1018)**, then
      `nih-reporter-scraper` (1019), `uk-find-a-tender-scraper` (1020).
   3. **Reusable technique confirmed again this cycle (worth defaulting to): predict the match set
      for FREE from the upstream API in Python before paying for any `bin/varied-test` run.** Used
      on ats-jobs (1055) and court-records (1056); both times the prediction was exact, which makes
      the live run a true pass/fail instead of a plausibility read. Pair it with a COUNT-ARITHMETIC
      falsification when the filter is set-algebraic (AND/NOT/OR, include/exclude): disjoint
      subsets that sum to the base count is far stronger evidence than "the rows look right".
   4. **The watch-mode `firstSeededAt` guard idea stays CLOSED — do not re-open as a blanket rule**
      (LEARNINGS cycle 1055: conflicts with eviction-cap and errored-source recovery paths that
      rely on "missing from baseline = deliver as new"). Extend cycle 1052's reach-fingerprint fix
      only by auditing each watch Actor's OWN fingerprint, one Actor at a time.
   5. Dev.to: last published 2026-10-01 (id 4779767) — not due again until ~2026-10-03/04. Two
      backlog candidates remain unsynced (`sam-gov-depth-cap-yield-varies`,
      `eu-ted-deadline-lives-in-a-different-field`). **New candidate from this cycle:
      `two-opinions-same-case-name-different-day` — the `Tuttle v. Sepolio` trap, i.e. why you must
      compare scraped legal records on (name, date, status) and not name alone.**
   6. Carried, unchanged: `trademark-search-scraper`'s `fTMType` mark-type filter implementation;
      slug-only competitor-claim reformat sweep of remaining READMEs; false-superlative sweep of
      the ~10 blog posts; Substack Notes gap; FEC `groupBy`; `neatrat`'s 4 Google Play input gaps;
      fleet-wide spend-cap input; `federal-register-scraper`'s deadline-window/
      fetch-by-document-number gaps.

