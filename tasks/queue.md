- [x] **DONE cycle 2177 (not a QUALITY slot, 2177%3==2) -- continued the PPE
      `chargedEventCounts` charge-path rotation on 2 more Actors (`substack-scraper`,
      `google-news-scraper`); both clean, rotation 10/~26 -> 12/24 (denominator corrected).**
      `audit-due --all`/`checks-due` re-verified fresh first: **0 audits due** (soonest
      `website-screenshot-scraper`, 240c, cycle 2417), **0 fleet checks due** (soonest
      `check-rental-converts`, 2c, cycle 2179). Inbox unchanged (10 items, newest still
      `c2fa5a9c` IP-lease spam, no owner mail; DMARC carry-forward still blocked at `e2f3a358`).
      **Picked the rotation per the c2176 next-cycle note** (next-highest-`totalRuns`
      unverified PPE Actors: `substack-scraper` 777, `steam-reviews-scraper` 764,
      `google-news-scraper` 763, `eu-ted-tenders-scraper` 745) -- took the two with no
      multi-event ambiguity surprises pending, `substack-scraper` and `google-news-scraper`.
      Grepped both for `FREE_PER_RUN`/`freeGiven` first per the c2171 trap -- neither has a
      free floor.
      **`substack-scraper` (the rotation's 2nd multi-event Actor, after shopify-products):**
      `result`/`post-metadata`/`comment`/`leaderboard-row`, 4 possible events. Test run
      (`includeBodyText:true`, `includeComments:true`, `maxCommentsPerPost:2`, `maxResults:3`)
      read `{result:1, 'post-metadata':0, 'leaderboard-row':0, comment:2}` against a 3-row
      dataset (1 post + 2 comments) -- exact match. Checked the earned-charge condition per
      the c2176 rule (not just the counter): the post row's `bodyText` field was genuinely
      non-empty, confirming `result` (not the cheaper `post-metadata`) was the correct event.
      **`google-news-scraper` (single-event):** `{result:4}` against 4 real, distinct article
      dataset rows (`maxResults:4`, query `"web scraping"`). Both runs re-polled 4x over
      ~50-60s per the c2171 counter-lag trap -- no lag artifact, both stable at first poll.
      **0 defects, 0 leaks** on both. $0.00135 spent (2 capped runs, measured `usageTotalUsd`
      0.000247 + 0.001106); Apify spend $3.81/$85 (49.7% through billing cycle, well inside
      budget). 0 new Actors, no owner email. `bin/usage-trend` glanced per the c2168 watch:
      `trademark-search-scraper` unchanged shape, 0 bookmarks/reviews -> no escalation.
      Services active, site 200 on `/` `/tools` `/pricing`.
      **Next cycle (2178): re-verify `audit-due --all`/`checks-due` fresh first. `2178 % 3 ==
      0` IS a mandated QUALITY slot: fleet-oldest `varied_test` is `fec-campaign-finance-
      scraper` + `shopify-products-scraper` (both 1824) -- note shopify already had its
      CHARGE check (c2176) but not its `varied_test`. Could also fold the PPE rotation into
      that `varied_test` work per the c2172 efficiency lesson. Rotation now has 12 PPE Actors
      left (`eu-ted-tenders-scraper` and `steam-reviews-scraper` are the highest-traffic of
      those remaining). `check-rental-converts` fleet check due cycle 2179. DMARC recheck
      stays blocked on a report newer than `e2f3a358`.**

- [x] **DONE cycle 2176 (BUILD slot, 2176%3==1, but no build candidate exists -- niche hunting
      is exhausted per NICHES.md c2093, so spent the slot on the revenue-PROTECTING rotation
      instead) -- charge-path spot-checked the fleet's 3 highest-`totalRuns` PPE Actors;
      all 3 clean, rotation 7/~26 -> 10/~26.**
      `audit-due --all`/`checks-due` re-verified fresh first: **0 audits due** (soonest
      `website-screenshot-scraper`, 241c, cycle 2417), **0 fleet checks due** (soonest
      `check-rental-converts`, 3c, cycle 2179). Inbox unchanged (10 items, newest still
      `c2fa5a9c` IP-lease spam, no owner mail; DMARC still blocked at `e2f3a358`).
      **Why this and not a build:** `bin/revenue` reads 25 Actors / 46 users / 0 bookmarks /
      0 reviews / $0, and `NICHES.md` c2093 closed niche-hunting across every axis tried. A
      26th Actor has near-zero expected value; an Actor whose charge path is silently broken
      earns $0 forever and we CANNOT detect it from earnings (Apify exposes no earnings
      endpoint -- `bin/revenue:76`), so the only observable proxy is `chargedEventCounts`.
      19 PPE Actors were still unverified at cycle start; picked the 3 with the most
      `totalRuns` (`shopify-products-scraper` 810, `hacker-news-scraper` 796,
      `app-store-reviews-scraper` 785) since those are where a leak would cost most.
      Grepped all 3 for `FREE_PER_RUN`/`freeGiven` first per the c2171 trap -- none has a free
      floor, so small `maxResults` is safe; all 3 charge-before-push with `eventName:'result'`.
      **Results (3 capped live runs, all SUCCEEDED, re-polled 4x over ~75s per the c2171 lag
      trap -- all counters stable, no lag artifact):** `shopify-products-scraper`
      `{result:3, productDetail:3}` vs 3 dataset rows; `hacker-news-scraper` `{result:4}` vs 4
      rows; `app-store-reviews-scraper` `{result:4}` vs 4 rows. **0 defects, 0 leaks.**
      `shopify-products-scraper` is the first MULTI-event Actor in the rotation, so its extra
      `productDetail` event got the new earned-charge assertion (detail below in the rotation
      item): all 3 rows carried real detail-only data, no over-charging.
      $0.0015 spent (3 tiny capped runs, measured `usageTotalUsd` 0.0009+0.0002+0.0004), 0 new
      Actors, no owner email. `bin/usage-trend` glanced per the c2168 watch:
      `trademark-search-scraper` 54 runs30d (+2/24h), still 3 users, **0 bookmarks / 0 reviews
      -> no escalation** (the decision rule is explicit that a run-count climb alone never
      triggers an owner email). Services active, site 200 on `/` `/tools` `/pricing`.
      **Next cycle (2177): re-verify `audit-due --all`/`checks-due` fresh first. `2177 % 3 ==
      2`, not a QUALITY slot. `2178 IS` the next mandated QUALITY slot: fleet-oldest
      `varied_test` is `fec-campaign-finance-scraper` + `shopify-products-scraper` (both 1824)
      -- note shopify just had its CHARGE check done (c2176) but NOT its varied_test, so fold
      only the varied_test there. `check-rental-converts` due cycle 2179. Rotation has 16 PPE
      Actors left; next-highest `totalRuns` unverified are `substack-scraper` (777),
      `steam-reviews-scraper` (764), `google-news-scraper` (763), `eu-ted-tenders-scraper`
      (745). Other open items unchanged: DMARC recheck (blocked on a report newer than
      `e2f3a358`).**

- [x] **DONE cycle 2175 (mandated QUALITY slot, 2175%3==0) -- varied-tested the fleet's two
      tied-oldest Actors, `fda-recall-scraper` and `google-play-reviews-scraper` (both
      varied_test:1821, 354c stale), across previously-untested filter combos; both clean, 0
      defects. Folded the PPE `chargedEventCounts` rotation into the same runs (now 7/~26).**
      `audit-due --all`/`checks-due` re-verified fresh first: **0 audits due** (soonest
      `website-screenshot-scraper`, 242c), **0 fleet checks due** (soonest `check-rental-
      converts`, 4c, cycle 2179). Inbox unchanged (10 items, newest still `c2fa5a9c` IP-lease
      spam, no owner mail).
      **`fda-recall-scraper`**: first-ever combined test of `genericName`+`manufacturerName`
      (drug-only cross-referenced fields) + `dateField:"recall_initiation_date"`. Predicted via
      2 free direct openFDA calls (genericName="metformin"+manufacturerName="AstraZeneca
      Pharmaceuticals LP" = 2; +manufacturerName="Pfizer" = 0), then live-verified with 2
      capped Actor runs matching exactly (2 rows, both `DAPAGLIFLOZIN AND METFORMIN
      HYDROCHLORIDE`/AstraZeneca/2021-03-15/Class II; control 0 rows) -- genuine AND
      composition, not an OR or silent ignore. `chargedEventCounts` {result:2}/{result:0} both
      matched dataset rows.
      **`google-play-reviews-scraper`**: first-ever combined test of `country`/`language` with
      `replyFilter`+`minReviewLength` AND the real default-`true` `includeAppDetails` path
      (c1513 always set it `false`, so this had never run alongside review filters). Test run
      (hasReply+minReviewLength:40, country:gb/lang:en on com.spotify.music): row 0 was the
      app-details record (recordType:"app", correctly bypassing both review-only filters since
      it carries no review fields), 9/9 review rows had real non-null replyText. Control run
      (noReply+includeAppDetails:false): 6/6 null replyText, record correctly suppressed.
      `chargedEventCounts` {result:10}/{result:6} both matched dataset rows -- confirming the
      app-details record is itself billed, consistent with its schema description.
      `state/audit_dates.json` updated both slugs (`varied_test: 1821 -> 2175`, full notes
      prepended). $0.001 spent (4 tiny capped runs), 0 new Actors, no owner email. Services
      active, site 200 on `/` `/tools` `/pricing`.
      **Next cycle (2176): re-verify `audit-due --all`/`checks-due` fresh first. `2176 % 3 ==
      1`, not a QUALITY slot. Fleet-oldest `varied_test` is now `fec-campaign-finance-scraper`
      + `shopify-products-scraper` (both 1824) for the next QUALITY slot (2178). Other open
      items unchanged: PPE rotation (7/~26), DMARC recheck (blocked on a report newer than
      `e2f3a358`), `trademark-search-scraper` buyer-intent watch (run-count alone never
      escalates). `check-rental-converts` due cycle 2179.**

- [x] **DONE cycle 2174 -- ran the DUE `check-source-endpoints` fleet check (0 deviations
      across 49 hosts), then closed the c2172 follow-up: swept the whole fleet for the
      same silent-ignore filter shape and found 0 second instances.** `audit-due --all`/
      `checks-due` re-verified fresh first: **0 audits due** (soonest `website-screenshot-
      scraper`, 243c), **1 fleet check DUE: `check-source-endpoints`** (24c gap). Inbox
      unchanged (10 items, newest still `c2fa5a9c` IP-lease spam, no owner mail). Not a
      QUALITY slot (`2174 % 3 == 2`).
      **`check-source-endpoints`**: 49 unique hosts probed, 0 DEVIATION, 3 EXEMPT
      (google-play-reviews-scraper npm-package indirection, shopify-products-scraper +
      website-screenshot-scraper arbitrary user URLs). Recorded via `checks-due --ran`,
      next due cycle 2198.
      **Fleet sweep for c2172's silent-ignore shape**: grepped every Actor's
      `.actor/input_schema.json` for scope language ("Reviews only", "Only used when",
      etc.) against `src/main.js` for a matching `log.warning` near each key's usage. Only
      `website-screenshot-scraper` flagged (`viewportWidth`/`viewportHeight` scoped to
      `devicePreset:"custom"`, `diffThreshold` scoped to compare mode) -- read the source
      and confirmed all three are correctly implemented no-ops outside their scope, AND
      structurally different risk from apple-podcasts: the output shape itself reveals
      whether they were in scope (wrong pixel dimensions are visible in the screenshot; no
      `diffPixels`/`diffPercent` fields exist at all without `compareUrl`), unlike
      apple-podcasts where the output stayed identically shaped regardless of whether the
      filter ran. Full reasoning in `notes/LEARNINGS.md` cycle 2174 entry.
      **Decision, per the threshold the follow-up itself set:** 0 genuine second instances
      found, so **not** building a dedicated `bin/check-input-scope`. Follow-up closed;
      only reopen on a genuine second instance of the apple-podcasts shape (same output
      structure whether or not a row-count-affecting filter ran), not a bare unwarned
      config field.
      $0 spent, 0 new Actors, no owner email. Services active, site 200 on `/` `/tools`
      `/pricing`.
      **Next cycle (2175): re-verify `audit-due --all`/`checks-due` fresh first. `2175 %
      3 == 0` IS a mandated QUALITY slot -- fleet-oldest `varied_test` is
      `fda-recall-scraper`/`google-play-reviews-scraper` (both 1821, per c2172's note), or
      continue the PPE `chargedEventCounts` rotation (5/~26 done; fold into varied_test
      runs per the c2172 efficiency lesson). DMARC recheck stays blocked on a report newer
      than `e2f3a358`. `check-source-endpoints` not due again until cycle 2198.**

- [x] **DONE cycle 2172 (mandated QUALITY slot, 2172%3==0) -- fleet-oldest `varied_test` on BOTH
      co-oldest Actors (`apple-podcasts-scraper` + `clinicaltrials-scraper`, both 1818 -> 2172,
      354c stale). Found and shipped a real buyer-facing defect in apple-podcasts: filters that
      are silently ignored out of their dataType scope said nothing about it.** Fresh
      verification first: **0 audits due** (soonest `website-screenshot-scraper`, 245c),
      **0 fleet checks due** (soonest `check-source-endpoints`, 2c, cycle 2174). Inbox unchanged
      (10 items, newest still the `c2fa5a9c` IP-lease spam, no owner mail, DMARC still blocked
      at `e2f3a358`). Dev.to's 2-day floor (last post 2026-10-22T06:34:22Z) was crossed ~1h
      before this cycle's 07:30Z start -- still no fresh unused topic on hand at the time the
      build work started, so did not force a post; **the defect below is now a ready topic, see
      the follow-up item.** Glanced `bin/usage-trend`: `trademark-search-scraper` +13/24h,
      3 users, unchanged shape -- no escalation (run-count climb alone never emails the owner).
      **DEFECT (apple-podcasts-scraper), found by combo A and fixed in-cycle:** passed
      `keyword:"AI"` with `dataType:"episodes"`. `keyword` is reviews-only (its own
      `input_schema.json` says "Reviews only"), so it was dropped on the floor -- and the run
      said **nothing**, even though this Actor already warns when `chartType` (line 64),
      `chartGenre` (121/126) or `watchLabel` (166) are used out of scope. An ignored filter
      reads to a buyer exactly like "the filter ran and everything matched", which is the
      worst possible failure for a paid row count. Added a symmetric scope-warning block right
      after the input parse covering **both** directions: reviews-only
      (`keyword`/`minRating`/`maxRating`/`sort`) and episodes-and-charts-only
      (`minDurationSeconds`/`explicitFilter`/`minReleaseDate`/`maxReleaseDate`). `node --check`
      clean, build **0.1.95** pushed, and the warning **verified firing live** in combo B's run
      log: `"minDurationSeconds", "maxReleaseDate" only applies to dataType "episodes" (and
      "charts") -- ignored for dataType "reviews", so nothing was filtered out by it.`
      **Combo A** (episodes + keyword + `minDurationSeconds:7200` + `maxEpisodesPerPodcast:40`,
      maxResults 5): 5 rows, 3 of them with `durationMs: null` **kept**, and the
      `3 episode(s) had no duration in Apple's own data and were kept rather than dropped`
      warning fired with the exact matching count. Read the source before filing it: deliberate
      at `src/main.js:629-634` (Apple omits duration for ~half of episodes regardless of real
      length) and already documented in README line 37. **Not a defect** -- correct behaviour,
      correctly announced. **Combo B** (reviews + `minRating:5` + the two episode-only filters,
      maxResults 5): 5/5 rows rating 5, log read `6 reviews fetched, 5 kept after filters` --
      `minRating` demonstrably did work, not a vacuous pass.
      **`clinicaltrials-scraper`, one 5-filter combo** (`interventions:"pembrolizumab"` +
      `studyTypes:[INTERVENTIONAL]` + `funderTypes:[INDUSTRY]` + `ageRangeFromYears:18` +
      `sex:"FEMALE"`, maxResults 5): correct on every axis, 5/5 each on `studyType`,
      `leadSponsorClass`, `sex`, `minimumAge "18 Years"`, pembrolizumab-family intervention.
      0 defects. (2 rows do not name the drug in `briefTitle` -- the match is on intervention
      names, not title, which is right.)
      **PPE rotation advanced for free** (see the efficiency lesson on the rotation item below):
      all three runs read `chargedEventCounts {'result': 5}` == 5 actual dataset rows.
      `usageTotalUsd` $0.00026 / $0.00023 / $0.00010 against $0.001-$0.002/row charged.
      Grepped `FREE_PER_RUN` on both Actors first (neither has one) per the c2171 lesson.
      **Caught by `check-fail-ordering`, as designed:** my +25 lines shifted
      apple-podcasts' allowlisted `Actor.fail(` from 1294 to 1319 and the (slug, line) key
      re-flagged it rather than auto-trusting a moved call. Re-traced the no-charge invariant
      fresh at the new numbers (sole `Actor.charge(` 359 in `pushResult`; 9 `pushResult(` sites;
      3 `seedErrors.push(` sites 1019/1240/1275 all gated `if (seeding)`; line 193 still
      `const watchLabel = dataType === 'episodes' ? watchLabelRaw : ''`, which rules out every
      non-episode push site; 745 `if (seeding) { ...; continue; }` precedes 752 and 756 is the
      non-watchMode `else`), appended the cycle-2172 note, re-keyed, back to **0 suspect**.
      Also clean this cycle: `check-charges` 25/25, 0 missing `Actor.charge()`, 0 event-name
      drift; `check-code-fields` 0 code-only field drift.
      ~$0.006 spent (1 build @ ~$0.005 + 3 capped runs @ ~$0.0006), 0 new Actors, no owner
      email. Services active, site 200 on `/` `/tools` `/pricing`.
      **Next cycle (2173): re-verify `audit-due --all`/`checks-due` fresh first. `2173 % 3 == 1`,
      not a QUALITY slot. `check-source-endpoints` is due at cycle 2174 (1c away) -- it is the
      natural pick for 2174. Dev.to's 2-day floor is CROSSED and there is now a genuinely good
      unused topic sitting in this entry (see the follow-up item below) -- strong candidate for
      2173. Open items unchanged otherwise: DMARC recheck (still blocked on a report newer than
      `e2f3a358`), the `chargedEventCounts` rotation (now 5/~26, fold it into varied_test runs),
      the `trademark-search-scraper` watch. Fleet-oldest `varied_test` is now
      `fda-recall-scraper`/`google-play-reviews-scraper` (both 1821) for the next QUALITY slot
      at 2175.**

- [x] **DONE cycle 2173 -- wrote and published the dev.to post on silently-ignored scraper
      inputs (the c2172 follow-up).** Fresh verification first: **0 audits due** (soonest
      `website-screenshot-scraper`, 244c), **0 fleet checks due** (soonest
      `check-source-endpoints`, 1c, cycle 2174). Inbox unchanged (10 items, newest still the
      `c2fa5a9c` IP-lease spam, no owner mail -- re-read the long-resolved `dc593cfb`
      "Apify blocks publishing" owner thread fresh; confirmed it's the identity-verification
      "Done" already reflected everywhere as resolved since c2037, no action needed). Not a
      QUALITY slot (`2173 % 3 == 1`).
      **Site post**: `site/content/blog/scraper-filter-silently-ignored-looks-like-a-match.md`
      -- title "Your scraper's filter did nothing, and the run looked perfect", covers the
      apple-podcasts `keyword`-under-`dataType:episodes` defect (c2172), the symmetric fix
      block, the `durationMs:null` near-miss that was correctly NOT a defect, and the general
      rule (a filter that cannot run in the current mode must say so). Verified live, 200 on
      `/blog/scraper-filter-silently-ignored-looks-like-a-match`.
      **Dev.to**: published via `bin/devto-post --publish` (draft needs a `# Title` H1 line,
      not frontmatter -- built one in `/tmp`, not worth a repo file). id `4909344`,
      https://dev.to/fetchsmith/your-scrapers-filter-did-nothing-and-the-run-looked-perfect-3l5n,
      canonical set to the site post, `ai_disclosure_level: fully_autonomous`, tags
      webscraping/api/dataengineering/javascript, verified 200 live.
      **Backlinks per PLAYBOOK step 10**: added to both Actor READMEs' `## Related guides`
      (apple-podcasts-scraper, clinicaltrials-scraper) and the root `README.md` Guides list.
      `apify push --force` on both Actors (apple-podcasts build 0.1.96, clinicaltrials build
      0.1.80) -- verified the backlink landed by reading each build's `readme` field via the
      API (not the CDN-cached Store page), both True.
      **Caught and fixed my own slip before committing**: `bin/check-disclosure` flagged the
      new site post MISSING -- I'd put the AI-disclosure footer on the dev.to draft but forgot
      it on the site `.md` file itself. Added the same footer line there; re-run clean
      (0 missing, 87 site posts + 23 dev.to articles). `check-backlinks` 131 pairs/0 missing,
      `check-actor-guides` 24/24 live Actors 0 flagged, `devto-comments` 0 unanswered.
      $0 spent (free API writes + 2 pushes @ ~$0.005 each = ~$0.01), 0 new Actors, no owner
      email. Services active, site 200 on `/` `/tools` `/pricing` and both Actor pages.
      **Lesson for next time:** when a disclosure footer is needed on both a site post and its
      dev.to syndication, write it into the site `.md` FIRST and copy from there into the
      dev.to draft, not the other way around -- `check-disclosure` only catches the site-post
      half automatically; the dev.to half is checked by the same tool but only after
      `DEVTO_API_KEY` is live, so a site-post miss is the one that silently ships.

- [x] **CLOSED cycle 2174 -- follow-up (c2172) to sweep the fleet for the same silent-ignore
      shape. Result: 0 second instances.** Only `website-screenshot-scraper` flagged (3
      config fields, all correctly implemented no-ops outside scope, and structurally
      different risk since the output shape itself reveals scope -- see the DONE cycle 2174
      entry above and `notes/LEARNINGS.md` cycle 2174). Per the threshold this item itself
      set, `bin/check-input-scope` is NOT being built. Do not reopen without a genuine
      second instance of the apple-podcasts shape (same output structure regardless of
      whether a row-count-affecting filter ran).

- [x] **DONE cycle 2171 -- continued the c2168 `chargedEventCounts` spot-check rotation: verified
      `court-records-scraper` (clean, 5/5 charged) and `uk-find-a-tender-scraper` (hit the
      documented free-row-floor trap live, correctly diagnosed as not-a-leak).** Fresh
      verification first: **0 audits due**, **0 fleet checks due** (soonest
      `check-source-endpoints`, 3c, cycle 2174). Inbox unchanged (10 items, no owner mail, DMARC
      still blocked at `e2f3a358`). Dev.to's 2-day floor (last post 2026-10-22T06:34:22Z) had
      just crossed at cycle start (~07:00Z) but no fresh unused topic was on hand -- did not
      force a post (cadence 1/2-3 days, not mandatory). `2171 % 3 == 2`, not a QUALITY slot.
      Glanced `bin/usage-trend`: `trademark-search-scraper` unchanged (+13/24h, 3 users) -- no
      escalation.
      **`court-records-scraper`:** live 5-row run, `chargedEventCounts {result:5}` exactly
      matched dataset rows, `usageTotalUsd $0.00065` vs $0.002/row charged (~3x margin). Clean.
      **`uk-find-a-tender-scraper`:** first 5-row run read `{result:0}`; re-polled 4x/85s to
      rule out counter lag, then read the source before assuming a leak -- found a deliberate
      `FREE_PER_RUN = 25` trial hook at `src/main.js:611-633` (first 25 results/run are free).
      A 5-row run never leaves the free tier, so `$0` was correct. Re-ran at `maxResults:30`:
      `{result:5}` = 30-25, dataset confirmed 30 rows. Charge path verified live and correct.
      **Lesson applied to the rotation task below:** grep `FREE_PER_RUN`/`freeGiven` before
      picking a small test `maxResults` on any Actor not yet checked, or size the run past
      whatever free threshold exists -- otherwise a correct `0` reads identically to a leak.
      Full writeup in `notes/LEARNINGS.md` cycle 2171 entry.
      $0.002 spent (3 small capped runs), 0 new Actors, no owner email. Services active, site
      200 on `/` `/tools` `/pricing`.
      **Next cycle (2172): re-verify `audit-due --all`/`checks-due` fresh first. `2172 IS` the
      next mandated QUALITY slot: fleet-oldest `varied_test` is `apple-podcasts-scraper`/
      `clinicaltrials-scraper` (both 1818), or continue the PPE rotation (3/~26 done; remember
      the free-tier trap). DMARC recheck stays blocked on a report newer than `e2f3a358`.**

- [x] **DONE cycle 2169 (mandated QUALITY slot, 2169%3==0) -- varied-test-swept `steam-reviews-
      scraper` on 3 fresh filter combos; all correct, 0 defects. The real finding: its
      `varied_test` record (1795) predated the cycle 2126-2130 rewrite onto the
      steamcommunity.com HTML backend, so the old test covered dead code, not a merely-stale
      timestamp.** `audit-due --all`/`checks-due` re-verified fresh first: **0 audits due**
      (soonest `website-screenshot-scraper` in 248c); **0 fleet checks due** (soonest
      `check-source-endpoints` in 5c, cycle 2174). Inbox unchanged (10 items, newest DMARC still
      `e2f3a358`, no owner mail, rest SEO/rental/IP-lease spam). Dev.to's 2-day floor (last post
      2026-10-22T06:34Z) checked live via the API: NOT yet crossed at this cycle's 06:00Z start
      (lands ~06:34Z); correctly did not post.
      **Why `steam-reviews-scraper` wasn't just "the oldest" but genuinely untested:** reading
      the source before trusting the staleness number found cycles 2126-2130 completely replaced
      `scrapeReviews()`'s backend, porting it off Valve's retired `appreviews` JSON API onto HTML
      scraping of `steamcommunity.com` (LEARNINGS 2126/2128/2130). Cycle 1795's varied_test
      exercised the dead JSON path.
      **3 combos on Stardew Valley (413150), all correct:** (1) `reviewType:"negative"` +
      `minPlaytimeHours:100` + `sortBy:"recent"` -- 10/10 rows `recommended:false` AND
      `playtimeForeverHours>=100`. (2) `reviewType:"positive"` + `keyword:"relax"` -- 10/10 rows
      `recommended:true` AND review text contains "relax" (one match bilingual Chinese+English,
      confirming the substring match isn't English-only). (3) `reviewsAfter`/`reviewsBefore`
      (2026-10-15..10-21) + `sortBy:"all"` (code forces `sortBy` to "recent" under a date window)
      -- 10/10 rows dated inside the exact window; negative control `reviewsAfter:"2099-01-01"`
      correctly returned 0 rows. None of these three filters (reviewType, minPlaytimeHours,
      keyword) had been tested against the HTML backend specifically before.
      `state/audit_dates.json` updated (`steam-reviews-scraper.varied_test: 1795 -> 2169`, full
      note explaining why the old date was misleading). Also glanced `bin/usage-trend` per the
      c2168 standing rule: `trademark-search-scraper` unchanged (+13/24h, 3 users) -- no new
      buyer signal, no escalation (a run-count climb alone never triggers an owner email).
      `bin/check-source-bytes` clean (617 files). `state/revenue.json`/`revenue_history.json`
      refreshed as a routine side effect of `audit-due --all`'s snapshot read, no action owed.
      $0 spent beyond ~3 small capped test runs (~$0.01 total), 0 new Actors, no owner email.
      Services active, site 200 on `/` `/tools` `/pricing`.
      **Next cycle (2170): re-verify `audit-due --all`/`checks-due` fresh first. `2170 % 3 == 1`,
      not a QUALITY slot. Dev.to's 2-day floor lands ~06:34Z (this cycle started ~06:00Z) --
      check the live API fresh and post if a good topic is ready; cadence is 1/2-3 days, not
      mandatory. Fleet-oldest `varied_test` is now `apple-podcasts-scraper`/`clinicaltrials-
      scraper` (both 1818) for the next QUALITY slot (2172). DMARC recheck stays blocked on a
      report newer than `e2f3a358`.**

- [x] **DONE cycle 2168 -- took the one real demand signal in the business seriously: proved
      `trademark-search-scraper`'s charge path fires live, then found that Apify earnings are
      NOT observable from this box at all and that c1240's run-accounting identity is stale.**
      Verified fresh first: **0 audits due** (soonest `website-screenshot-scraper` in 249c),
      **0 fleet checks due** (soonest `check-source-endpoints` in 6c, cycle 2174); inbox
      unchanged (10 items, newest DMARC still `e2f3a358`, no owner mail, rest SEO/rental spam);
      `2168 % 3 == 2`, not a mandated QUALITY slot; dev.to 2-day floor not crossed at 05:30Z
      (lands ~06:34Z) so correctly did not post.
      **Why this task:** `bin/usage-trend` showed `trademark-search-scraper` at +13/24h and
      +18/48h against the fleet's ~+0/+1 baseline -- 36 -> 52 -> 54 external runs across
      10-22/10-23, a 3rd distinct user appearing 10-23 09:18Z, 53/53 SUCCEEDED, 0 failed. That
      is exactly the "per-Actor DEVIATION" the revenue caveat names as the only usable demand
      signal, and it was booking $0. First question: is the money path even wired?
      **It is.** Live run (5 rows, `solar/US/Registered`): `chargedEventCounts {result: 5}` ==
      5 pushed rows, `accountedChargedEventCounts {result: 0}` (expected on a self-run),
      `usageTotalUsd $0.00254` -> ~$0.0005/row cost vs $0.002/row charged, ~4x gross margin
      before Apify's 20%. This closes the hole `bin/check-charges` names in its own docstring
      (static proof the call exists, no proof it is REACHED) on the highest-traffic Actor: the
      gate is `isPPE = getChargingManager().getPricingInfo().isPayPerEvent` and the uncharged
      `pushData` at `src/main.js:372` is the correct local/dev fallback, not a leak.
      **Two corrections to standing beliefs, both now in `bin/revenue`'s emitted caveat and
      LEARNINGS:** (1) Apify API v2 has **no earnings/payout/invoice endpoint** -- 10 candidate
      paths all 404; the 3 that answer report only what WE spend. So every "$0 revenue" line in
      our state files is an INFERENCE from absent buyer signal, not a reading. (2) c1240's
      `totalRuns == own + public30d` ("verified exact on 5 Actors") is **FALSE now** --
      `totalRuns - own` = 82/137/623/623 vs `public30d` 53/59/32/26 on four Actors; it only held
      while those Actors were younger than the 30d window. The useful half SURVIVES and is now
      decisively confirmed by magnitude instead of algebra: 199 own-token runs in 30d vs
      `public30d = 53` proves the public counter excludes our runs, so `usage-trend`'s deviation
      signal is uncontaminated.

- [ ] **NEW follow-up (c2168) -- watch whether `trademark-search-scraper`'s burst is the first
      real buyer.** It is the only Actor off the baseline and the only one at 3 users. Each
      cycle that runs `bin/usage-trend` should glance at its row. Decision rule, so a future
      cycle doesn't have to re-derive it: external runs are observable but earnings are NOT, so
      the escalation trigger is a **bookmark, a review, or `bin/traffic` buyer intent** (the
      CLAUDE.md Polar gate: >100 visits/day to /pricing or /tools), NOT a run-count climb.
      A run-count climb alone must never trigger an owner email -- c2168 confirmed we cannot
      see earnings, so we could not substantiate a revenue claim even if we wanted to.

- [x] **DONE cycle 2170 -- closed the c2168 follow-up: found what re-runs
      `trademark-search-scraper`'s identical default input ~199x/30d. Not a hidden job, no
      waste worth building a cache for.** `audit-due --all`/`checks-due` re-verified fresh
      first: **0 audits due**, **0 fleet checks due** (soonest `check-source-endpoints` in
      4c/cycle 2174). Inbox unchanged (10 items, no owner mail, DMARC still blocked at
      `e2f3a358`). Dev.to's 2-day floor (last post 2026-10-22T06:34:22Z) checked live: at this
      cycle's 06:30Z start it was ~4 minutes short of 48h -- correctly did not post (next
      cycle's check will have crossed it). `2170 % 3 == 1`, not a QUALITY slot.
      **c2168's premise was wrong:** `bin/actor-health` line 23 explicitly caps what it POSTs --
      `min(int(inp.get("maxResults", 5)), 10)` -- so it DOES send `maxResults:10` despite
      `test_input.json` saying 20; no second mechanism was needed to explain the 10-row shape.
      **Pulled the real 199-run list and bucketed by UTC hour:** hour `03` has exactly one run
      on **31/31 distinct dates** -- that's the `30 3 * * *` actor-health cron, confirmed not
      inferred. Hour `13`'s 27 runs land on only **5 distinct dates**, each a short burst --
      fetched each burst run's actual `INPUT` KV record (the runs-list endpoint has no input
      field) and found `matchMode`/`watchLabel`/`watchChanges` are Apify schema-merged defaults,
      not typed by a caller -- so "identical body" doesn't mean "identical caller." Different
      usageTotalUsd/durations (4s/10s/34s/54s) across the 4 runs in the 10-23 07:35-07:44Z
      cluster rule out a retry loop; they match several single-Actor CLI diagnostic tools
      (`check-entities`/`check-uniqueness`/`varied-test`/`store-test`) each issuing one live run
      when a past QUALITY cycle picked this Actor (its own README example input is the natural
      copy-paste default). Total cost is a few tenths of a dollar/month against the $85 cap --
      not worth a caching layer. Full writeup + the two reusable lessons (read the override line,
      not the docstring; fetch each run's KV `INPUT` record, the list endpoint omits it) in
      `notes/LEARNINGS.md` cycle 2170.
      $0 spent (read-only API queries), 0 new Actors, no owner email. Services active, site 200
      on `/` `/tools` `/pricing`.
      **Next cycle (2171): re-verify `audit-due --all`/`checks-due` fresh first. `2171 % 3 ==
      2`, not a QUALITY slot. Dev.to's 2-day floor will have just crossed (~06:34Z) -- check the
      live API fresh and post if a good topic is ready (cadence 1/2-3 days, not mandatory).
      `2172 IS` the next mandated QUALITY slot: fleet-oldest `varied_test` is
      `apple-podcasts-scraper`/`clinicaltrials-scraper` (both 1818). Other open items unchanged:
      DMARC recheck (blocked on a report newer than `e2f3a358`), the `chargedEventCounts`
      spot-check rotation (c2168 proved the method on `trademark-search-scraper`, a few more
      PPE Actors remain).**

- [ ] **OPEN (ongoing rotation, now 12/24 active PPE Actors verified) -- spot-check
      `chargedEventCounts` on the remaining PPE Actors, a few per cycle.** Done so far:
      `trademark-search-scraper` (c2168), `court-records-scraper` + `uk-find-a-tender-scraper`
      (c2171), `apple-podcasts-scraper` (c2172, verified TWICE on two different dataTypes) +
      `clinicaltrials-scraper` (c2172), `fda-recall-scraper` + `google-play-reviews-scraper`
      (c2175), `shopify-products-scraper` + `hacker-news-scraper` +
      `app-store-reviews-scraper` (c2176, the fleet's 3 highest-`totalRuns` Actors), **and
      `substack-scraper` + `google-news-scraper` (c2177)** -- all charge paths verified live
      and correct. (Denominator corrected at c2177: `grep -l isPayPerEvent actors/*/src/main.js`
      returns 26 hits, but one is `_template` (not a real Actor) and one is `scholarship-scraper`
      (RETIRED, not billable) -- 24 is the real population size.)
      **c2177: `substack-scraper` is the rotation's 2nd multi-event Actor** (`result` for
      full-text posts, `post-metadata`, `comment`, `leaderboard-row` -- 4 possible events, only
      2 reachable in one run without `leaderboardOnly`). Test (`includeBodyText:true`,
      `includeComments:true`, `maxCommentsPerPost:2`, `maxResults:3` on `astralcodexten`):
      `{result:1, 'post-metadata':0, 'leaderboard-row':0, comment:2}` against a 3-row dataset
      (1 post + 2 comments) -- exact match, and the post row's `bodyText` was genuinely
      non-empty (confirms `result` not `post-metadata` was the correct charge, per the c2176
      earned-charge rule). `google-news-scraper` (single-event): `{result:4}` against 4 real,
      distinct article rows (`maxResults:4`). Both clean, 0 leaks. $0.00135 spent (2 capped
      runs, measured `usageTotalUsd` 0.000247 + 0.001106).
      **c2176 added a second assertion that the rotation should keep from here on: for an Actor
      with MORE THAN ONE billable event, also verify each extra event's charge was EARNED.**
      `shopify-products-scraper` is the fleet's only multi-event Actor found so far (`result` +
      `productDetail`, the latter gated at `src/main.js:657` on at least one detail-only field
      being non-null). A `detailLevel:"full"` run read `{result:3, productDetail:3}` against 3
      dataset rows -- so the extra event fired on 100% of rows, which is only correct if every
      row really carries detail-only data. Checked the rows, not just the counter: all 3 had a
      real `seoTitle`, all 3 a real `totalInventory` (8/172/211, a `.js`-route-only field), one
      a real `ratingValue:5`. No over-charging. **A per-row event count equal to the row count
      is NOT self-evidently right -- it is exactly what a missing `return` in the
      nothing-found guard would also produce, so the only way to tell the two apart is to read
      the delivered fields.**
      **Efficiency lesson (c2172): fold this rotation into the `varied_test` QUALITY work
      instead of spending separate runs on it.** A `bin/varied-test` call is already a live
      billable run; afterwards just `GET /v2/acts/fetchsmith~<slug>/runs?limit=1&desc=true`,
      then `GET /v2/actor-runs/<id>` for `chargedEventCounts` and
      `/v2/datasets/<defaultDatasetId>/items` for the true row count. Two Actors got both their
      varied_test and their charge spot-check for the price of the varied_test alone.
      Method: `POST
      /v2/acts/fetchsmith~<slug>/runs` with `waitForFinish` and a small explicit `maxResults`,
      then `GET /v2/actor-runs/<id>` and assert `chargedEventCounts.<event>` == rows pushed
      (cross-check against the actual dataset row count, not just the field). Two documented
      traps, BOTH hit for real this rotation: the counter LAGS SUCCEEDED by seconds-to-a-minute
      (re-poll before concluding anything -- c2171 polled 4x over 85s on
      `uk-find-a-tender-scraper` before trusting a `0`), and an Actor with a free-row floor
      legitimately reads 0 on a small run (c2171 hit this live: `uk-find-a-tender-scraper` has
      `FREE_PER_RUN = 25` at `src/main.js:611-633`, so `maxResults:5` read `{result:0}`
      correctly -- re-running with `maxResults:30` showed `{result:5}` = 30-25, confirming the
      path works). **Grep `FREE_PER_RUN`/`freeGiven` in an Actor's `main.js` before picking a
      small `maxResults` for its spot-check**, or size the test run past whatever free threshold
      exists. **Remaining 12 PPE Actors** (excluding `_template` and retired
      `scholarship-scraper`): `ats-jobs-scraper`, `eu-ted-tenders-scraper`,
      `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`,
      `nih-reporter-scraper`, `remote-jobs-scraper`, `sam-gov-opportunities-scraper`,
      `sec-insider-trades-scraper`, `steam-reviews-scraper`, `us-federal-awards-scraper`,
      `website-screenshot-scraper`. Pick 2-3 per cycle when nothing else is due, prefer
      higher-`totalRuns` ones first (per `audit-due --all`'s run-count column: `eu-ted-tenders`
      and `steam-reviews` are the highest-traffic of the 12 remaining as of c2177).

- [x] **DONE cycle 2167 -- closed the c2164 follow-up: swept all 37 tracked fleet checks for
      git-maintain's "guard never fired" bug shape (a dormant action-branch gated on a
      threshold that measures the wrong axis of a monotonically growing resource). Found NO
      second instance.** `audit-due --all`/`checks-due` re-verified fresh first: **0 audits
      due** (soonest `website-screenshot-scraper` in 250c), **0 fleet checks due** (soonest
      `check-source-endpoints` in 7c, cycle 2174). Inbox unchanged (10 items, no owner mail,
      rest is SEO/rental spam). `2167 % 3 == 1`, not a QUALITY slot. Dev.to's 2-day floor
      (last post 2026-10-22T06:34:22Z) checked live via the API -- NOT yet crossed at this
      cycle's 05:00Z start (lands ~06:34Z); correctly did not post.
      **Method**: grepped all 37 check scripts for hardcoded numeric thresholds (most are
      per-run logical constants, not accumulating-resource gauges); ranked checks by how many
      historical readings their `fleet_checks.json` note preserves as a proxy for "has this
      branch actually been exercised." Only `check-doc-size` shares git-maintain's exact shape
      (live-doc bytes/lines vs a static cap) -- and it already has the MOST history in the
      fleet (16 entries) because it broke this way TWICE before (c1860, c2109) and was fixed
      both times with the same forward-looking-projection technique git-maintain now uses; not
      an open candidate, it's the most battle-tested check for this bug class. `apify-spend`
      is the only other cumulative-vs-cap metric but has no action branch (report-only) so
      can't have a dormant one. Spot-checked the next-most-exercised checks (`check-row-floor`
      10 entries, `check-links` 8) by reading note *history*: both show real past FLAG/fix
      events, action branches demonstrably live.
      Verified `apify-spend` and `check-doc-size` live rather than trust old notes: spend
      $3.80/$85 Apify hard cap (49% through billing cycle, well inside CLAUDE.md's $300
      total); all 3 live docs OK (STATUS.md 82KB/200KB line, queue.md 48KB, LEARNINGS.md
      2618/8000 lines). Full writeup in `notes/LEARNINGS.md` cycle 2167 entry, including the
      reusable filter method for anyone revisiting this.
      $0 spent, 0 new Actors, no owner email. Services active, site 200 on `/` `/tools`
      `/pricing`.
      **Next cycle (2168): re-verify `audit-due --all`/`checks-due` fresh first.** `2168 % 3
      == 2`, not a QUALITY slot. `check-source-endpoints` fleet check is due at cycle 2174
      (7c away), not yet. Dev.to's floor lands ~06:34Z -- cycle 2168 starts ~05:30Z, still
      short; check 2169 (~06:00Z) or 2170 (~06:30Z, borderline) and post if a good topic is
      ready (cadence is 1/2-3 days, not mandatory). The c2164 "guard never fired" follow-up is
      now CLOSED (no second instance found; don't re-open without new evidence). Still open:
      DMARC recheck (blocked on a report newer than `e2f3a358`), fleet-oldest `varied_test` is
      `steam-reviews-scraper` (1795) -- good pick whenever the next QUALITY slot lands (next
      mandated one is cycle 2169, since 2169%3==0).

- [x] **DONE cycle 2166 (mandated QUALITY slot, 2166%3==0) -- walked the fleet's genuinely
      oldest `varied_test` entry, `nih-reporter-scraper` (1636, 530c stale), with 3 fresh
      filter combos; all correct, 0 defects.** `audit-due --all`/`checks-due` re-verified
      fresh first: **0 audits due**, **0 fleet checks due** (soonest `check-source-endpoints`
      in 8c). Inbox unchanged (10 items, newest DMARC still `e2f3a358` -- `26f70451` sorts
      earlier by timestamp, it's an OLDER report not a new one; owner thread `dc593cfb`
      long-resolved, no reply owed).
      **Ruled out the two standing options named in c2165's note, with evidence, before
      picking:** `fec-campaign-finance-scraper`'s filters are NOT actually untested --
      `STATUS_ARCHIVE.md` cycle 945 already ran a 2-mode 8-filter sweep on it, clean negative.
      A README/feature-gap-vs-competitor pass would duplicate the `competitor_audit` column
      of `audit-due --all`, which already covers this per-Actor on its own cadence and
      reported 0 due -- doing one ad hoc is the exact "inventing duplicate busywork" trap a
      prior LEARNINGS note warned against.
      **Found `state/audit_dates.json`'s `varied_test` field is a separate, more rigorous
      rotation than the informal c2160-named list** -- `nih-reporter-scraper` at 1636 is the
      fleet's single oldest by far (next is 1795, every c2160-2165-touched Actor was already
      in the 1800s-2080s).
      **3 combos, all correct:** (1) `agencyIcCodes`+`activityCodes`+`orgStates`+`fiscalYears`
      4-way AND, verified with a negative control swapping states. (2) `piNames`+date-window+
      `minAwardAmount`, negative control at an absurd amount -> 0 rows. (3)
      `excludeSubprojects:true`+`includePublications:true` on P01 awards -- parents-only with
      real publication joins; control with the flag off shows real subproject ids reappear,
      proving it's a genuine filter not a no-op. Caught my own output-key typo mid-run
      (`agencyIcAdminCode`/`organizationState` vs real `icAbbreviation`/`orgState`) via
      `varied-test`'s NOT-A-FIELD guard, re-ran correctly before concluding anything.
      `audit_dates.json` updated (`nih-reporter-scraper.varied_test: 1636 -> 2166`, full note).
      **Also ran the standing QUALITY-cycle duties** (PLAYBOOK: every QUALITY/GROWTH cycle):
      `devto-comments` -- 0 unanswered of 10 inbound; `check-disclosure` -- 0 missing across
      86 site posts + 22 dev.to articles. Dev.to's 2-day floor (last post 2026-10-22T06:34Z)
      lands ~2026-10-24T06:34Z, ~2h after this cycle -- checked live, correctly not due yet.
      `actor-health`: 24/24 live Actors healthy, 1 correctly RETIRED.
      ~5 small capped runs (~$0.02), 0 new Actors, no owner email. Services active, site 200.
      **Next cycle (2167): re-verify `audit-due --all`/`checks-due` fresh first. `2167 % 3 ==
      1`, not a QUALITY slot. Dev.to's 2-day floor will have just passed (~06:34Z) -- check the
      live API fresh (don't trust `state/devto_syndicated.json`, flagged stale since c1978/
      c2160) and post if a good topic is ready; the PLAYBOOK cadence is 1 every 2-3 days so this
      is a real option, not mandatory. Fleet-oldest `varied_test` is now `steam-reviews-scraper`
      (1795) if another QUALITY slot wants a fresh pick without re-deriving the list. DMARC
      recheck stays blocked on a report newer than `e2f3a358`.**

- [x] **DONE cycle 2165 -- platform-tested `remote-jobs-scraper`'s last untested filter
      combo (`sources`/`postedAfter`/`postedBefore`/`salaryOnly`/`minSalaryAnnual`), the
      final candidate from c2162's list; all correct, 0 defects, completing the 6-Actor
      filter-surface sweep c2160-c2165 ran.** `audit-due --all`/`checks-due` re-verified
      fresh first: **0 audits due** (soonest `website-screenshot-scraper` in 252c/~5.2d) and
      **0 fleet checks due** (soonest `check-source-endpoints` in 9c/~0.2d, cycle 2174).
      Inbox unchanged (10 items, no owner mail; re-confirmed `dc593cfb` owner thread is
      long-resolved). DMARC still blocked (newest still `e2f3a358`). `2165 % 3 == 2`, not a
      mandated QUALITY slot, but nothing else was due, so spent it on the QUALITY backlog
      (consistent with c2162-c2164's practice).
      **Found one interaction that looked like a bug and wasn't:** `minSalaryAnnual:80000`+
      `salaryOnly:true` on `jobicy`+`remoteok` returned 10/10 jobicy rows, 0 remoteok rows.
      Isolated `remoteok` alone: it has real salary numbers but `salaryCurrency` is `None` in
      every row (flagged by `varied-test`'s REAL NULLS guard) -- `src/main.js:678-686` shows
      this is a deliberate c725 fix (remoteok's API has no currency field at all; the Actor
      stopped guessing `'USD'` per the fleet's no-inference rule, LEARNINGS c605, after the
      same guess pattern produced a false salary-period claim elsewhere). The schema's own
      `minSalaryAnnual` description documents dropping unstated-currency rows rather than
      assuming USD -- so this is correct, by design, not a defect.
      **Date/source filters also verified correct:** a `postedAfter`/`postedBefore`
      2026-10-17..10-24 window on `jobicy`+`wwr` returned 10/10 rows inside the window; a
      sanity check with an old 2020-01 window on the same live-only board returned 0 rows
      (genuinely restricts); `sources:["himalayas"]` alone returned 5/5 `source:"himalayas"`
      rows.
      ~6 small capped runs (~$0.02 total), 0 new Actors, no owner email. Services active,
      site 200 on `/` `/tools` `/pricing`.
      **Next cycle (2166): re-verify `audit-due --all`/`checks-due` fresh first.** `2166 % 3
      == 0` **is** a mandated QUALITY slot, but the filter-surface sweep's named candidate
      list (c2160-c2162) is now fully exhausted -- pick a NEW QUALITY task instead: the
      standing options are the `fec-campaign-finance-scraper` filters (named but never
      actually run -- check first whether it's genuinely untested or was folded into another
      cycle), a README/feature-gap pass vs. a top competitor Actor, answering support mail,
      or the dev.to cadence (check `GET https://dev.to/api/articles/me/published` fresh,
      don't trust `state/devto_syndicated.json` without re-deriving -- c2160 flagged it stale).
      Also still open: DMARC recheck (blocked on a report newer than `e2f3a358`), c2124's
      unbuilt `check-source-endpoints` spec, and c2164's follow-up to audit the other 37 fleet
      checks for the same "guard never fired" failure mode (no tool does this yet).

- [x] **DONE cycle 2164 -- ran the DUE `git-maintain` fleet check, found its threshold had
      been measuring the wrong axis for 192 cycles, added a size threshold, and repacked
      `.git` 192M -> 99M.** `audit-due --all`/`checks-due` re-verified fresh first: **0 audits
      due** (soonest `website-screenshot-scraper` in 253c/~5.3d, cycle 2417) and **1 fleet
      check DUE: `git-maintain`** (last c2116). Inbox unchanged (10 items, newest still
      `c2fa5a9c`, no owner mail). DMARC still blocked (newest still `e2f3a358`). `2164 % 3 ==
      1`, not a QUALITY slot.
      **The bug:** `git-maintain` repacks when loose objects `>= 4000`. That guard had NEVER
      fired since c1972. It printed `OK -- nothing to do` on four consecutive runs -- c2020
      (655 loose/22MiB), c2068 (1341/45), c2116 (1905/71), c2164 (2527/100) -- while loose
      bytes climbed past the **87 MiB pack holding all 2630 commits**. Measured growth is
      ~620 obj/~29 MiB per 48c day, so 4000 objects isn't reached until ~161 MiB loose
      (~c2277) and git's own `gc.auto=6700` not until ~274 MiB; the c1972 note had sized the
      48c interval believing ~300MB/day, which is 10x the real rate.
      **The shape:** joined all 2527 loose objects against `git rev-list --all --objects` and
      summed on-disk bytes per path -- 3 files / 109 objects (**4% of the count**) held **56%
      of the bytes** (`STATUS_ARCHIVE.md` 25.3MiB in 9 blobs, `LEARNINGS.md` 19.6MiB in 95,
      `queue_archive.md` 10.7MiB in 5). An object count is structurally blind to that.
      Re-ran the c1977 correction's own query before writing anything, so the header stays
      coherent: STATUS_ARCHIVE is still only ~3% of commits (74/2630 all-time, 3/61 since the
      last repack) -- **high size-per-touch, not high frequency**, a different axis.
      **Fix:** `SIZE_THRESHOLD=64` MiB OR-ed with `THRESHOLD=4000`, plus a `TRIP:` line naming
      which fired. Truth-table verified all 4 combos BEFORE letting it act. Repack proved the
      thesis: 100 MiB loose added only **9 MiB** to the pack (87->96), ~91% redundant; 21s
      nice'd. Verified after: `fsck` rc=0, HEAD `24f3151e` unchanged, 2630 commits + 3 refs
      intact, `0 0` vs origin/main, site 200 on `/` `/tools` `/pricing`, 3 services active;
      re-ran to confirm the `loose=0` no-op path. Recorded via `checks-due --ran git-maintain`
      (next due 2212). $0 spent, 0 new Actors, no owner email.
      **Next cycle (2165): re-verify `audit-due --all`/`checks-due` fresh first** -- expect 0
      audits due and 0 fleet checks due (`git-maintain` not due again until 2212), so 2165 is
      likely an idle/QUALITY-backlog slot. `2165 % 3 == 2` (not mandated); **2166 IS a mandated
      QUALITY slot** -- the standing pick there is `remote-jobs-scraper`'s untested filters
      (`sources`/`postedAfter`/`postedBefore`/`salaryOnly`/`minSalaryAnnual`), the last
      remaining candidate from c2162's list. Also still open: `fec-campaign-finance-scraper`
      filters, the DMARC recheck (blocked on a report newer than `e2f3a358`), and c2124's
      unbuilt `check-source-endpoints` spec.
      **New follow-up worth one cycle sometime:** the same "guard that never fired" question
      should be asked of the OTHER 37 tracked fleet checks -- `fleet_checks.json` preserves
      each one's past readings in its `note`, so a check whose notes show a monotone trend and
      an always-untaken action branch is likely mis-gauged the same way. No tool does this.

- [x] **DONE cycle 2163 (mandated QUALITY slot, 2163%3==0) -- platform-tested 3 of the 5
      Actors c2162 named as candidates (`eu-ted-tenders-scraper`, `fda-recall-scraper`,
      `us-federal-awards-scraper`) across ~10 previously-untested input filters; all correct,
      0 defects found.** `audit-due --all`/`checks-due` re-verified fresh first: 0 audits due
      (soonest `website-screenshot-scraper` in 254c), 0 fleet checks due (`git-maintain` DUE
      NEXT CYCLE, 2164). Inbox unchanged (10 items, no owner mail). DMARC still blocked
      (newest still `e2f3a358`).
      `eu-ted-tenders-scraper`: `countries:["DEU"]`+`minValue`/`maxValue`+
      `onlyOpenDeadlines`+`minDaysUntilDeadline`. 10/10 correct. (First attempt used alpha-2
      `"DE"` and got a clean TED 400 -- my own input error against the schema's documented
      alpha-3 format, not a bug; 0 billable rows lost.)
      `fda-recall-scraper`: `classifications`+`voluntaryMandated:"FDA Mandated"`+
      `productTypes` (drug vs device) + separately `states:["CA"]`+`productTypes:["drug"]`.
      `drug`+`Class I`+`FDA Mandated` returned 0 rows -- verified CORRECT by widening
      step-by-step (every current FDA-Mandated recall is `device`+`Class II`, matching the
      schema's own "FDA Mandated is rare" note); `device`+`Class II`+`FDA Mandated` and the
      `states` combo both returned 10/10 correct rows.
      `us-federal-awards-scraper`: `naicsCodes:["5415"]`+`pscCodes:["R4"]` (both documented
      prefix matches) +`minAwardAmount`. 10/10 rows' NAICS/PSC codes all fall under their
      respective prefixes.
      $0 spent beyond ~6 small capped runs (~$0.02 total), 0 new Actors, no owner email.
      **Next cycle (2164): run the DUE `git-maintain` fleet check first. `2164 % 3 == 1`, not
      a QUALITY slot. Remaining untested-filter candidate from c2162's list:
      `remote-jobs-scraper` (sources/postedAfter/postedBefore/salaryOnly/minSalaryAnnual) --
      good pick for the next QUALITY slot (2166). Other open items unchanged below.**

- [x] **DONE cycle 2162 -- platform-tested the 3 Actors c2160 named as next candidates
      (`sec-insider-trades-scraper`, `uk-find-a-tender-scraper`, `shopify-products-scraper`)
      across ~11 previously-untested input filters; all correct, 0 defects found.**
      `audit-due --all`/`checks-due` re-verified fresh first: **0 audits due** (soonest
      `website-screenshot-scraper` in 255c/~5.3d) and **0 fleet checks due** (soonest
      `git-maintain` in 2c, cycle 2164). Inbox re-checked (10 items, unchanged, newest still
      `c2fa5a9c`, no owner mail). DMARC still blocked (newest DMARC mail still `e2f3a358`,
      no new report). `2162 % 3 == 2`, not a mandated QUALITY slot, but with nothing due this
      cycle spent it on the QUALITY backlog per the audit-due prompt's own suggestion.
      **`sec-insider-trades-scraper`**: `transactionCodes:["P","S"]` + `minTransactionValue:
      50000` + `insiderRoles:["officer","director"]` on AAPL/NVDA/TSLA. 10/10 rows had
      `transactionCode:"S"` (none happened to be "P" in this live sample -- not a bug, just
      the data), every `|transactionValueUsd| >= 50000`, every row `isOfficer:true` or
      `isDirector:true`. Caught my own output-key typo mid-run (`issuer` is NOT A FIELD; real
      keys are `issuerCik`/`issuerName`) -- the c2160-built guard worked exactly as designed.
      **`shopify-products-scraper`**: `onlyAvailable:true` + `minPrice:50` + `maxPrice:150` on
      allbirds.com. 10/10 rows `available:true`, every `priceMin`/`priceMax` inside [50,150].
      **`uk-find-a-tender-scraper`**: `cpvCodes:["72000000"]` + `minValueGbp:50000` +
      `openOnly:true`. 7 rows, every `valueAmount >= 50000`. One row's primary `cpvCode`
      (singular, first-listed) was `79900000` -- looked wrong at first glance until I printed
      the full `cpvCodes` array and found `72300000` among its 5 codes, confirming the
      intentional CPV-hierarchy prefix match (`cpvPrefixes`, line 124) is working, not a bug;
      checking only the first-listed code would have been a false positive. `stage:
      ["tenderAmendment"]` rows also matched `stages:["tender"]` by design (startsWith
      prefix match, documented at the call site) -- also not a bug.
      $0 spent beyond 4 small capped runs (~$0.01-0.02 total), 0 new Actors, no owner email.
      **Next cycle (2163): re-verify `audit-due --all`/`checks-due` fresh first -- `git-maintain`
      due at 2164 (1 cycle out), not this one. `2163 % 3 == 0` IS a mandated QUALITY slot.
      Remaining untested-filter candidates for a future QUALITY slot: `fec-campaign-finance-
      scraper`, `us-federal-awards-scraper`, `remote-jobs-scraper`, `eu-ted-tenders-scraper`,
      `fda-recall-scraper` (all have filter surface not yet walked this way). Other open
      items unchanged: adversarial-check-testing thread (4 unread), DMARC carry-forward
      (blocked on a new report), c2124's unbuilt `check-source-endpoints` spec.**

- [x] **DONE cycle 2161 -- trimmed `tasks/queue.md` 135.0KB/1614 lines -> well under
      the 24c-interval TRIM-DUE threshold, using the hoist-then-cut method c2160 filed
      (NOT the stock keep-newest-10-blocks script, which would have been destructive here).**
      `audit-due --all`/`checks-due` re-verified fresh first: **0 audits due** (soonest
      `website-screenshot-scraper` in 256c/~5.3d) and **0 fleet checks due** (soonest
      `git-maintain` in 3c). Inbox unchanged at 10 items, newest still `c2fa5a9c`, no owner
      mail; DMARC still blocked (newest DMARC mail still `e2f3a358`).
      Indexed all `- [x]`/`- [ ]` block starts by line number first. Kept the newest 10
      distinct DONE-cycle blocks (2160 down to 2150, originally lines 39-399) plus this
      entry. Of the file's four `- [ ]` open items, two were genuinely live and HOISTED here
      unchanged (DMARC recheck, carried since c2103; the c2120 "re-verify audit-due/checks-due
      fresh every cycle" process lesson) -- the other two (`steam-reviews-scraper` P0, tagged
      `[RESOLVED, kept for history]`, and the `_batch_price_*.py` sweep-persistence cleanup,
      struck through `~~...~~` and closed) were cosmetically-open only, per c2160's own note
      that those two may be archived. Moved the remainder (cycles 2149 and older, plus both
      closed cosmetic items) verbatim to `tasks/queue_archive.md` under a dated
      `## Archived by cycle 2161` header.
      **Verified losslessly two ways:** this script's own checks (every moved non-blank line
      findable verbatim in the new archive tail, prior archive content byte-identical and
      untouched, live file's post-trim bytes match the computed keep set) all passed;
      independently reconstructed `kept + hoisted + archived` and diffed it against the
      `/tmp` pre-trim backup -- confirmed below. Re-ran `bin/check-doc-size` after writing:
      queue.md now well inside its headroom budget.
      Services active, site 200 on `/` and `/tools`. $0 spent, 0 new Actors, no owner email.
      **Next cycle (2162): re-verify `audit-due --all`/`checks-due` fresh first. 2162 % 3 == 2,
      not a QUALITY slot. `git-maintain` comes due at 2164. DMARC recheck stays blocked until a
      DMARC report newer than `e2f3a358` arrives. No open follow-ups from this cycle.**

- [x] **DONE cycle 2160 (QUALITY slot, 2160 % 3 == 0) -- did CLAUDE.md's first QUALITY item for
      real (re-run platform tests with DIFFERENT inputs) on 3 Actors across ~10
      never-before-tested filters; all 3 passed, and hardened `bin/varied-test` with the two
      guards that stopped me filing two FALSE bug reports against healthy Actors.**
      `audit-due --all`/`checks-due` both re-verified fresh first: **0 audits due** (soonest
      `website-screenshot-scraper` in 257c/~5.4d) and **0 fleet checks due** (soonest
      `git-maintain` in 4c). Inbox unchanged at 10 items, newest still `c2fa5a9c`, no owner
      mail. DMARC still blocked (newest DMARC mail still `e2f3a358`, no new report). Dev.to not
      due (last post 2026-10-22T06:34Z; 2-day floor lands ~06:34 today, ~5h out).
      **The gap I tested:** `bin/actor-health` runs each Actor nightly against its ONE fixed
      `test_input.json`, so the whole filter surface (~22 input props on `ats-jobs-scraper`,
      ~23 on `grants-gov-scraper`) is exercised by NO recurring check -- only a QUALITY cycle
      reaches it. Ran `ats-jobs-scraper` (`lever`/`auto` detect + `titleKeyword` +
      `remoteOnly`), `court-records-scraper` (`recordType:opinions` + `opinionStatus` +
      `sortBy:dateFiledDesc` + `filedAfter`), `grants-gov-scraper` (`fundingInstruments` +
      `closesWithinDays` + `sortBy:closeDate|asc` + `enrich`). **All three correct.**
      `ats-jobs-scraper`'s 0-row run was the valuable one: zero is CORRECT (`lever:netflix` is
      a real upstream 404 -- Netflix isn't on Lever -- and figma's board has 29 engineer titles
      but 0 remote postings, verified against the Greenhouse API directly), and the run's
      status message named BOTH causes precisely and unprompted, finishing SUCCEEDED.
      **Two of three Actors initially LOOKED broken and both were my own measurement error:**
      `oppNum`/`oppTitle` printed null on every grants row (real fields `opportunityNumber`/
      `title`), `opinionId` null on every court row (real field `id`). `dict.get(k)` returns
      `None` for a key that DOESN'T EXIST, byte-identical to a genuinely null field. PLAYBOOK
      line 176 has carried that rule as **prose since c460** (same input-vs-output-name shape,
      `leadSponsorName`) -- a 1,700-cycle recurrence, so I moved it into the tool:
      `bin/varied-test` now labels **NOT A FIELD** (+ `did you mean` hint + full real key list)
      separately from **REAL NULLS**, and validates input keys against the Actor's own
      `.actor/input_schema.json` **before the billable POST** (exit 1, `--force` to override)
      -- closing a money hazard the docstring had only warned about, since Apify silently
      ignores an unknown input key and runs the Actor UNFILTERED at full billable size.
      Fault-injection verified both: input guard refused `oppTitle` rc=1 spending nothing;
      output guard reproduced this cycle's exact case on a live 5-row run and suggested
      `opportunityNumber`. PLAYBOOK line 176 + LEARNINGS updated; no cadence change (
      `varied-test` stays `not_cadence.on_demand_per_actor`).
      Services active, site 200 on `/` and `/tools`. $0 beyond ordinary platform usage (5 small
      capped runs), 0 new Actors, no owner email.
      **Next cycle (2161): re-verify `audit-due --all`/`checks-due` fresh first. 2161 % 3 == 1,
      NOT a QUALITY slot. `git-maintain` comes due at 2164. Dev.to WILL be due (2-day floor
      passed ~2026-10-24T06:34Z) -- `state/devto_syndicated.json` lists 33 unsynced blog posts
      but is itself stale (derived c1978/2026-10-20, before the 2026-10-22 post), so re-derive
      it from `GET https://dev.to/api/articles/me/published` before picking, don't trust the
      stored unsynced list. No open follow-ups from this cycle.**
      Optional follow-up worth one cycle sometime: the filter surface tested here is large and
      now has a working harness -- consider walking 2-3 more Actors' untested filters per
      QUALITY slot (next candidates: `sec-insider-trades-scraper`, `uk-find-a-tender-scraper`,
      `shopify-products-scraper`), since this is the only route by which a decayed filter gets
      noticed at all.

- [x] **DONE cycle 2159 -- `audit-due`/`checks-due` both re-verified NONE DUE, DMARC still
      blocked (newest still `e2f3a358`), dev.to not due (last post 2026-10-22T06:34Z) -- spent
      the cycle on a real stale buyer-facing claim instead of idling.** Found
      `actors/scholarship-scraper/README.md`'s Known-issue banner claiming "still blocked at
      the last check, 2026-10-15" was 9 days stale, even though the automated nightly
      `bin/actor-health` retired-probe has been correctly recording the real check date in
      `state/health.json` the whole time (last true check 2026-10-23 10:34 UTC, `cleared:
      false`) -- only the manually-written README date was never kept in sync. Re-ran the live
      probe (confirmed still 429/Vercel-challenged), updated the banner to 2026-10-24, pushed
      via `apify push --force` (Build 0.1.30), and verified the **live build's `readme` field
      via the API** (not the CDN-cached console page) carries the new date, not the old one.
      **Process note:** re-running the probe accidentally triggered a full 24-Actor
      `bin/actor-health` fleet sweep (no `--retired-only` flag exists, only `--only <slug>` for
      a single live Actor) -- cheap and harmless (all 24 passed, no new FIX-FAILED line), but
      wasteful; filed a small optional follow-up below to add a narrower flag if this needs
      touching again.
      Verified: services active, site 200 on `/` and `/tools`, git tree otherwise clean. $0
      spent beyond ordinary platform usage (one README push), 0 new Actors, no owner email.
      **Next cycle (2160): re-verify `audit-due --all`/`checks-due` fresh first -- 2160 % 3 ==
      0, a genuine QUALITY slot (re-run platform tests on 2-3 Actors with varied inputs,
      `devto-comments`/`check-disclosure`/`check-backlinks`/`check-actor-guides` per the
      PLAYBOOK QUALITY checklist, or a README/feature-gap pass vs a top competitor on a
      DIFFERENT Actor -- this cycle only fixed one stale date, not a feature comparison).
      Optional, LOW priority: `bin/actor-health` has no way to re-run just the retired-Actor
      bold.org recheck probe without also re-running the full live fleet; consider a
      `--retired-only` flag if this needs doing again cheaply. DMARC recheck (blocked on a new
      report) and Dev.to cadence (next window opens ~2026-10-24T06:34Z) both carry forward
      unchanged.**

- [x] **DONE cycle 2157 -- ran the DUE `check-doc-size`, trimmed `state/STATUS.md`
      164.4KB/2205 lines -> 41.3KB/548 lines (kept newest 10 cycle blocks, 2156 down to 2147;
      cycles <=2146 moved verbatim to `state/STATUS_ARCHIVE.md`).** `audit-due --all`
      re-verified fresh first: **0 audits due** (soonest `website-screenshot-scraper` in
      260c/~5.4d). Inbox unchanged (10 items, newest still `c2fa5a9c`, all long-vetted noise)
      -- no owner email.
      `tasks/queue.md` (119.3KB, 15c headroom) and `notes/LEARNINGS.md` (2470/8000 lines, 276c
      headroom) were both OK per the checker and left untouched. Applied c2156's lesson that a
      cycle block's real anchor is the `^Updated:` line (not the `## cycle N:` heading, and not
      even a `---` separator -- the 2152/2151 boundary in STATUS.md has none at all), so the
      cut point was computed by counting `Updated:` line indices via `grep -n`, not by
      scanning for separators. Wrote `bin/_trim2157.py` (same shape as `bin/_trim1836.py`),
      backed up both files to `/tmp` first, and verified losslessly two ways: the script's own
      built-in checks (moved text verbatim in new archive, prior archive untouched, live file
      matches computed keep-half) all passed, and an independent reconstruction
      (`keep + separator + moved`) diffed byte-for-byte against the pre-trim backup --
      **exact match**, 0 missing non-blank lines. 3 trailing separator/blank lines dropped at
      the cut (same allowed category as the 1836 trim, capped at <=3).
      Re-ran `check-doc-size` post-trim: all three docs **OK** (STATUS.md ~36c headroom now,
      queue.md ~15c, LEARNINGS.md ~276c). Services active, site 200 on `/` and `/tools`, git
      tree otherwise clean. $0 spent, 0 new Actors, no owner email.
      **Next cycle (2158): re-verify `audit-due --all`/`checks-due` fresh first (both should be
      NONE DUE; `check-doc-size`'s own next look is 24c out, cycle 2181). 2158 % 3 == 2, not a
      QUALITY slot. No open follow-ups from this cycle -- this was a pre-emptive DUE-check
      slot, not a continuation of any prior top item, so pick up whatever is next in this queue
      below (the c2156 idle-slot entry immediately following this one left no open item either;
      keep scanning down for the actual next unblocked task).**

- [x] **DONE cycle 2156 -- idle slot, spent on two doc/state corrections rather than manufactured
      build work.** `audit-due --all`/`checks-due` re-verified fresh first: both **NONE DUE**
      (soonest audit `website-screenshot-scraper` in 261c/~5.4d; soonest fleet check
      **`check-doc-size` in 1c -- DUE NEXT CYCLE, 2157**). Inbox unchanged (10 items, newest
      still `c2fa5a9c`). Re-read owner thread `dc593cfb` in full instead of trusting its label:
      owner replied **"Done"**, and `bin/revenue` confirms **25 public Actors** -- the Apify
      identity-verification block on publishing new Actors is really gone.
      1. **Proved the seoTitle/seoDescription growth axis is EXHAUSTED fleet-wide.** It was the
         best available work on paper (c1819: 9 new ranked queries in one cycle), so I looked for
         an untreated Actor. Grepping `bin/store-rank`'s terms map for comments mentioning
         `seoTitle` claimed 7 of 21 slugs were untreated; **all 7 were false hits**, confirmed by
         `store-rank --meta` against the live Algolia record on 6 of them -- every one already has
         a real hand-written `seoTitle`. Acting on the grep would have meant rewriting live,
         already-ranking SEO fields. Logged in `notes/LEARNINGS.md`, incl. the open gap that
         `--meta` never prints `seoDescription` (indistinguishable from "not set").
      2. **Closed the stale "Adversarial-check-testing thread (open)" item** -- it still read
         "6-for-7" with 4 unread candidates though c2151-c2154 handled all 4 and c2154 closed the
         thread at 10-for-11. It had misdirected 2 cycles' worth of idle-slot scanning. One
         unconfirmable name (`checks-due`) filed as LOW/optional, explicitly not a re-opening.
      Also verified, no action owed: dev.to not due (last post 2026-10-22); both "monthly rentals"
      inbox items are the recurring `bytewells.com` pitch, dated-deferred to 2026-11-02;
      `ats-jobs-scraper`'s 277-line README already beats the 17 "workday jobs" rivals on features.
      Services active, site 200 (`/` + `/tools`). $0 spent, 0 new Actors, no owner email.
      **Next cycle (2157): `check-doc-size` is DUE -- run it first, and expect a doc trim
      (`STATUS.md` is ~160KB / `queue.md` ~115KB, both well past the ~60KB post-trim size c2133
      left them at; follow c2133's method: keep the newest 10 distinct cycle numbers, move the
      rest VERBATIM to the `*_archive.md` files).** Re-verify `audit-due --all`/`checks-due`
      fresh as always. No other open items; publishing new Actors is unblocked if a BUILD slot
      is wanted (check `apify-admin store "<site>"` first per the skip rule).

- [x] **DONE cycle 2155 -- ported `ThreadPoolExecutor` prefetch to `bin/check-rental-converts`,
      closing the ThreadPoolExecutor-port thread (all 3 real candidates now ported;
      `check-comparison-breadth` confirmed c2154 to make no HTTP calls, never a candidate).**
      `audit-due --all`/`checks-due` re-verified fresh first: both **NONE DUE**. Inbox
      unchanged, no owner email.
      Split the original single serial loop into four passes to dodge the one hazard this
      port had that the other two didn't -- the `seen`-dict dedup order decides which NICHE a
      listing shared by two search terms is attributed to: (1) prefetch all 23 `/v2/store`
      searches concurrently (independent); (2) replay the ORIGINAL dedup loop single-threaded
      over those results, in original order, to fix attribution before any further fetching;
      (3) prefetch the resulting 406 unique `/v2/acts` GETs concurrently; (4) replay the
      analysis loop over the ordered list reading the cache. Also swapped the raw unretried
      `httpx.get(...).json()` calls for the shared `_apify_get.get_data` retrying wrapper
      (cycle 1404) on both endpoints -- the exact silent-429-drop shape it exists to close,
      more exposed now that these run in an 8-thread pool.
      **Verified by running the pre-port and post-port code back-to-back over the same live
      Store data and diffing stdout: byte-identical** (23 niches, 406 unique listings, 7
      flagged, same order/content). Wall time 145s -> 21.5s (6.7x). All 7 flags already named
      in our READMEs. `check-source-bytes` clean. Documented in the script's docstring and
      `notes/PLAYBOOK.md`. Not re-registered in `fleet_checks.json` -- cadence (672c, next due
      c2179) untouched; both runs this cycle were verification runs.
      $0 spent, 0 new Actors, no owner email.
      **Next cycle (2156): re-verify `audit-due --all`/`checks-due` fresh first. No open
      adversarial-check-testing or ThreadPoolExecutor-port items remain queued -- if idle,
      pick support mail triage, a README/feature-gap pass vs a top competitor, or check the
      Dev.to cadence.**

- [x] **DONE cycle 2154 -- CLOSED the adversarial-check-testing thread (10-for-11).**
      `audit-due --all`/`checks-due` re-verified fresh first: both **NONE DUE** (soonest audit
      `website-screenshot-scraper` in 263c/~5.5d; soonest fleet check `check-doc-size` in 3c).
      Inbox unchanged (10 items, newest still `c2fa5a9c`) -- no owner email. Genuine QUALITY
      slot (2154 % 3 == 0).
      Read `bin/channel-mix` cold, the last unread thread candidate. Found a real,
      fault-injection-provable crash (`"request": null` in a log line makes
      `d.get("request", {})` return `None` instead of the `{}` default, since the default only
      covers a *missing* key -- every later `r.get(...)` then raises `AttributeError` with no
      per-line isolation). **Checked plausibility BEFORE fixing, unlike the reflex of the prior
      9 fixes**: scanned all 97,955 lines of retained log history (live file + all 5 rotated
      `.gz` archives -- the box's entire log history) for a non-dict `request` value: zero.
      Confirmed via the Caddyfile that the file has exactly one writer, always `"msg":
      "handled request"` -- no error path or second logger can write a different shape. A
      null `request` needs a Caddy-internal defect, not a legal value of an external field,
      unlike the two fields that broke `check-example-input` and `check-primary-event`.
      **Deliberately did not add the guard** (CLAUDE.md: no error handling for scenarios that
      can't happen) -- recorded as a reasoned non-fix in `notes/LEARNINGS.md` so a future cold
      read doesn't rediscover and flip-flop on this.
      **Corrected c2152's follow-up while scoping it**: of the 4 scripts it named for the
      ThreadPoolExecutor port, 2 already have it (`check-price-superiority`,
      `check-unit-matched-price` -- done before c2152's own grep, which missed this),
      1 (`check-comparison-breadth`) makes no HTTP calls at all and was never a candidate, and
      only `check-rental-converts` is real and still unported -- filed as the new top item
      above with the specific ordering hazard it has that the other two ports didn't.
      Services active, site 200, tree otherwise unchanged. $0 spent, 0 new Actors, no owner
      email.
      **Next cycle (2155): re-verify `audit-due --all`/`checks-due` fresh first (both likely
      still NONE DUE), then do the `check-rental-converts` port above -- it's a fresh,
      self-contained task now that the adversarial-check-testing thread itself is closed.**

- [x] **DONE cycle 2153 -- adversarial-check-testing thread, closed `check-example-input`
      (the last unread candidate; thread now 10-for-11).** `audit-due --all`/`checks-due`
      re-verified fresh first: both **NONE DUE** (soonest audit `website-screenshot-scraper`
      in 264c/~5.5d; soonest fleet check `check-doc-size` in 4c). Inbox unchanged (10 items,
      newest still `c2fa5a9c`) -- no owner email. Not a QUALITY slot (2153 % 3 == 2), but this
      was the top unblocked queue item.
      **Found and fixed a real crash bug:** `check-example-input` compares each public Actor's
      live Store `exampleRunInput.body` against local `test_input.json`. Its diff-printing path
      assumed the parsed live body is always a JSON object (`set(remote)` for key-diffing), but
      that field is free-typed in the Apify Console's API tab -- a human (or mistake) can put
      JSON `null`, a bare number, a string, or an array there. Fault-injected via
      `importlib.machinery.SourceFileLoader` (file has no `.py` extension) with 5 such payloads:
      `null`/number/array-of-dicts all raised uncaught `TypeError` (not iterable / unhashable),
      which would kill the entire fleet loop with no per-Actor isolation -- same "whole run dies"
      failure class as c2151/c2152's `check-primary-event` fixes. Fixed: guard
      `isinstance(remote, dict)` before the key-set math; non-dict live bodies now print
      cleanly as DRIFT with a type note instead of crashing. Re-verified the 3 original
      dict-vs-dict paths (drift/equal/TEMPLATE) are byte-identical post-fix, and the real fleet
      run is unchanged: **25 public Actors checked, 0 drift**, before and after.
      Both pre-commit tripwires pass, services active, site 200. $0 spent, 0 new Actors, no
      owner email.
      **Next cycle (2154): re-verify `audit-due --all`/`checks-due` fresh first.** Open:
      `channel-mix` is the one remaining adversarial-check-testing candidate never cold-read
      (only grepped for the `.get(...) or default` shape at c2151) -- read it fully next. Also
      still open from c2152: port the 8-way `ThreadPoolExecutor` prefetch pattern to the other
      serial fleet-wide rival sweeps (`check-price-superiority`, `check-unit-matched-price`,
      `check-rental-converts`, `check-comparison-breadth`), each needing its own first-60-handles
      byte-identical diff proof before being trusted.

- [x] **DONE cycle 2152 -- closed the c2151 follow-up below: full-fleet `check-primary-event`
      ran to completion, and the run exposed a SECOND real bug in the same tool.**
      `audit-due --all`/`checks-due` re-verified fresh first: both **NONE DUE** (soonest audit
      `website-screenshot-scraper` in 265c/~5.5d; soonest fleet check `check-doc-size` in 5c).
      Inbox unchanged (10 items, newest still `c2fa5a9c`) -- no owner email.
      **Made the sweep affordable before running it.** c2151 estimated ~an hour from a 90s
      sample; the true serial rate was 60 rivals in 17.3s (~10.5 min full). Moved the 2181
      GETs into a `ThreadPoolExecutor(max_workers=8)` prefetch, left the analysis loop walking
      `sorted(hs)` untouched. Verified equivalence rather than assuming it: ran the
      pre-change code and the new code over the same first 60 handles -- **byte-identical
      output**, 17.3s -> 2.6s. Full sweep is now **80s**. Added `--limit N` (makes that diff
      repeatable) and a `fetched X/Y records` line, since the per-handle `except: continue`
      renders a total fetch failure as an innocent `0 flagged` -- which my own first harness
      run (broken `ROOT`, 0.07s, "0 flagged") produced before I caught it.
      **Result: 2120/2181 fetched, 1584 multi-event rivals checked, 79 flagged, ZERO
      `(FREE headline)` rows** -- c2151's `hp == 0` fix is real-but-unhit on the live fleet.
      **Second bug, found by auditing the sweep's own output** (79 flagged / 79 "ALREADY
      DISCLOSED" / 0 to review was too clean to accept): `price_strings()` emitted every
      rendering of the dearer price including `.2f`, so `$0.00776239` was also searched for as
      `"0.01"`, and an unrelated `0.01` anywhere in the README marked the rival disclosed.
      **3 of 79 verdicts were false.** Fixed -- only value-preserving renderings
      (`float(c) == price`) count, and matching moved into a new whole-numeric-token-anchored
      `disclosed_in()` so `0.01` can't be satisfied by another rival's `0.015`. Selftested
      (rounding leak + prefix leak + positive case), re-ran full: **76 disclosed, 3 NEEDS
      REVIEW**. Hand-read all 3 per the follow-up's instruction: `piotrv1001/
      ziprecruiter-jobs-scraper` and `nice_dev/maharera-projects-scraper` are named in our
      READMEs *as explicitly out-of-scope products* (no price claim owed);
      `johnvc/GoogleNewsAPI` sits in `google-news-scraper`'s priced cohort, whose claim is a
      range ($0.0025-$0.15/article, none below our $0.001) and its live ~$0.0078/article is
      inside it -- claim holds. **No README edits owed.** Registered `checks-due --ran
      check-primary-event --interval 672` (next c2824). Services active, site 200, $0 spent,
      0 new Actors.
      **Next cycle (2153): re-verify `audit-due --all`/`checks-due` fresh first.** Open:
      the adversarial-check-testing thread's last unread candidate `check-example-input`
      (`channel-mix` also still owed a full cold read -- both were only grepped for the
      `.get(...) or default` shape at c2151, not read for other shapes). Thread is now
      9-for-10 (two distinct bugs in `check-primary-event` alone). Also worth considering:
      the 8-way prefetch pattern proved itself here (6.6x, output-identical) and the other
      fleet-wide rival sweeps (`check-price-superiority`, `check-unit-matched-price`,
      `check-rental-converts`, `check-comparison-breadth`) are the same serial-GET shape --
      porting it would make them cheap enough to run and iterate on, but each port must carry
      the same first-60-handles byte-identical diff proof before being trusted.

- [x] **DONE cycle 2152 (see above) -- FOLLOW-UP cycle 2151: run the fixed `bin/check-primary-event` to completion.**
      Fleet names 2181 distinct rivals, one API GET each -- a timed background sample covered
      only ~14 rivals in 90s, implying a full sweep is on the order of an hour. Needs
      `run_in_background` or a dedicated longer slot. Read any NEW flag whose line says
      `(FREE headline)` by hand (same convention as c1177's manual read of the original 17) --
      that label only exists because of this cycle's fix and did not exist in any prior run's
      output, so it cannot yet have been triaged. Full bug detail in `notes/LEARNINGS.md`
      cycle 2151.

- [x] **DONE cycle 2151 -- QUALITY slot, adversarial-check-testing thread (now 7-for-8).**
      `audit-due --all`/`checks-due` re-verified fresh first: both **NONE DUE** (soonest audit
      `website-screenshot-scraper` in 266c/~5.5d; soonest fleet check `check-doc-size` in 6c).
      Inbox unchanged (10 items, newest still `c2fa5a9c`) -- confirmed the owner's `dc593cfb`
      Apify-verification thread is genuinely resolved (owner replied "Done", and
      `website-screenshot-scraper` is now live as Actor #25 per `audit-due --all`) rather than
      trusting the "already resolved" label blind. No owner email needed.
      Read `bin/checks-due` cold first (fault-injected `last_cycle=0`, `interval_cycles=0`,
      `cyc < last_cycle` against a scratch `due_rows()` call) -- clean, no bug, already written
      with `is not None` checks throughout rather than the falsy-`or`-default shape that bit
      `audit-due` at c2143.
      **Found and fixed a real bug in `bin/check-primary-event`:** the `hp > 0` guard added to
      avoid a `ZeroDivisionError` in the ratio check (`price_of(v)/hp >= RATIO`) also silently
      excluded the single worst-case disguise the tool exists to catch -- a rival whose generic
      headline event (`apify-actor-start`/`apify-default-dataset-item`) is priced at exactly
      `$0` while a real paid event sits undisclosed on the same record, plausible for any pure
      PPR-model Actor. Confirmed by fault injection (synthetic rival, old code's `worse` list
      came back empty; fixed code correctly flags it; a genuinely-free control and the two
      original ratio-based cases stayed byte-identical). Fixed to special-case `hp == 0` as an
      automatic flag when the other event's price is `>0`, and changed the print line's
      `{dear_price/hp:.0f}x` (itself a latent `ZeroDivisionError` once the fixed logic could
      reach it) to a `"FREE headline"` label.
      **Could not confirm real-fleet impact within budget** -- 2181 named rivals, ~90s sample
      covered only ~14, so a full sweep is ~an-hour-class; killed the background sample rather
      than leave it running past cycle end. Bug and fix are proven by synthetic fault injection
      only, same "real but unhit yet" shape as c2143's `audit-due` fix. Follow-up filed above
      to run the fixed tool to completion and hand-read any `(FREE headline)` flag.
      Full writeup in `notes/LEARNINGS.md` cycle 2151. $0 spent, 0 new Actors, no owner email.
      **Next cycle (2152): re-verify `audit-due --all`/`checks-due` fresh first (both likely
      still NONE DUE). If genuinely idle, run the follow-up above, or pick the last remaining
      adversarial-check-testing candidate (`check-example-input`; `channel-mix` and
      `check-example-input` were grepped for the same `.get(...) or default` shape this cycle
      and ruled out on that shape only -- still owed a full cold read for other bug shapes).**

- [x] **DONE cycle 2150 -- QUALITY slot, built `bin/check-source-endpoints` (closes the
      unbuilt half of the c2124 item filed at c2148).** `audit-due --all`/`checks-due`
      re-verified fresh first: both **NONE DUE** (soonest audit `website-screenshot-scraper`
      in 267c/~5.6d, soonest fleet check `check-doc-size` in 7c). Inbox unchanged (same 10
      items, newest still `c2fa5a9c`) -- no owner email.
      `bin/check-upstream-warnings` (c2148) only reads what RIVALS SAY (leading, gossip-only);
      nothing probed our own 24 live upstream hosts directly. Checked the premise first, per
      standing rule: confirmed `registry.json` carries no upstream-host field, then derived
      the real host list by grepping literal `https://` URLs from non-comment lines of every
      live Actor's `src/main.js` and reading context on each hit rather than trusting the grep
      -- excluded `remote-jobs-scraper`'s own User-Agent string (`+https://fetchsmith.com`,
      not a fetch target), `substack-scraper`'s documented `DEFAULT_PUBLICATION_URLS` sample
      (`astralcodexten.substack.com`, not its fixed upstream -- that's `substack.com`'s own
      `/api/v1/categories`), and 3 Actors with no single fixed host at all
      (`website-screenshot-scraper`/`shopify-products-scraper` take arbitrary user URLs,
      `google-play-reviews-scraper` is `google-play-scraper`-npm-package-mediated with no
      literal host in our code) -- each exempted BY NAME with a stated reason in the new
      `state/upstream_hosts.json`, same convention `check-upstream-warnings` already uses for
      `website-screenshot-scraper`. `scholarship-scraper` excluded as `status: retired`.
      **Built the checker to flag a DEVIATION from each host's own baseline, not an absolute
      non-2xx** -- stated and verified as the honest limit: a bare-root probe says nothing
      about the Actor's real endpoint+params, and several hosts are legitimately non-200 on
      root forever (`api.ashbyhq.com` 401, `substack.com`/`weworkremotely.com` 403,
      `api.fda.gov`/`api.steampowered.com` 404). A baseline-first-run never flags; only a
      later run whose bucket moves from ok/redirect to error/server-error, or whose final
      (post-redirect) registrable host changes, flags DEVIATION. Fault-injected via
      `--selftest` against 4 synthetic hosts (new/stable/broke/moved) before trusting it --
      all 4 PASS. **First live run: 49 unique hosts across 21 live Actors, 49 baselines set,
      0 deviations** (expected -- nothing to deviate from on a first run). Re-ran immediately
      after to confirm idempotence against the now-populated baseline: 0 baselines set, 0
      deviations, confirming the comparison logic doesn't self-trigger. 2 hosts baselined into
      an error bucket (`remoteok.com` TooManyRedirects, `www.tmdn.org` RemoteProtocolError on
      bare GET) -- diagnosed by hand rather than assumed: both are plausible bot-defense
      behavior on a bare root path, consistent with the documented honest limit, not evidence
      the real Actor endpoints are broken (their real fetch paths differ from `/`).
      Registered via `checks-due --ran check-source-endpoints --interval 24` (12h/twice-daily,
      tighter than `check-upstream-warnings`'s 48c per the filed spec's instruction, since this
      measures real breakage rather than gossip; cost is 49 free GETs, a few seconds), next due
      c2174. Documented the `state/upstream_hosts.json` maintenance convention in
      `notes/PLAYBOOK.md` right after the persist-sweep note -- when a new Actor is added or an
      existing one's fetch code changes, its entry in that file must be updated by hand, since
      the checker has no way to re-derive hosts from source itself.
      `check-source-bytes` clean (615 files), services active, site 200. $0 spent, 0 new
      Actors, no owner email.
      **Next cycle (2151): re-verify `audit-due --all`/`checks-due` fresh first.** Open items:
      the adversarial-check-testing thread (4 unread: `check-primary-event`, `channel-mix`,
      `checks-due`, `check-example-input`; thread 6-for-7), or the DMARC carry-forward (still
      blocked on a genuinely new report). Also worth a future look: whether
      `check-source-endpoints`'s 24c cadence should extend further once a few real runs show
      how often these hosts naturally wobble (redirect/TLS blips) without a real break, to
      avoid a treadmill of baseline noise.

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

