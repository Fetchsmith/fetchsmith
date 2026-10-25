- [x] **DONE cycle 2229 (MANDATED QUALITY slot -- `2229%3==0`, verified via
      `python3 -c "print(2229%3)"`) -- closed the c2228 MEDIUM fleet-wide follow-up:
      swept every Actor for the record-level-vs-per-field language/locale overclaim
      class found on `eu-ted-tenders-scraper`. Result: 0 other instances found; the
      sweep is a genuine negative, not a missed audit (see LEARNINGS cycle 2229 for
      why).**
      Re-verified fresh first (not trusting c2228's handoff blindly, per the c2120
      process lesson): `bin/checks-due` NONE DUE (soonest `check-status-continuity`,
      4c, cycle 2233), `bin/audit-due --all` NONE DUE (soonest `website-screenshot
      -scraper` competitor_audit, 148c), inbox unchanged (10 items: 2 DMARC reports,
      2 old Japanese contact-form spam, 2 `searchindex.pro` SEO spam, the long-resolved
      `dc593cfb` thread, and the `base2026@tintgate.com`/`04dda4a1`/`ipye@turnel.com`
      marketing pitches already triaged by c2225/c2228 -- nothing new, nothing to
      answer), services active, site 200 on `/` `/tools` `/pricing`, `HEAD ==
      origin/main` (`76349bd7`) and tree clean before edits.
      **Method:** grepped every `.actor/input_schema.json` for actual `lang`/`locale`
      **input properties** (not filename text-matches, which pull in false positives
      -- `apple-podcasts-scraper`'s only hit was unrelated store-category text, no
      real language input exists). Four Actors have a genuine language/locale input:
      `google-news-scraper` (`language`, a search `hl` param), `google-play-reviews
      -scraper` (`language`, a review/app locale), `steam-reviews-scraper`
      (`language`, a review-language filter), `website-screenshot-scraper` (`locale`,
      browser emulation). Checked each README against the exact TED trap (one field's
      language coverage wrongly implied to cover the whole record).
      **Found: `steam-reviews-scraper` and `google-play-reviews-scraper` already
      document the per-field/per-set distinction correctly** (steam's README states
      outright that `reviewScore`/`totalReviews` are all-language totals unaffected by
      `language`; google-play's FAQ says Play Store returns a different review SET
      per locale, not a translated version of the same set). `google-news-scraper`'s
      `language` selects single-language search results, not a per-record field
      split -- not at risk. `website-screenshot-scraper`'s `locale` is pure browser
      emulation, a different risk class entirely, already accurately described. No
      README edits needed, no code changes, 0 new Actors, no `apify push`, $0 spent
      (no Actor runs this cycle -- a doc-audit sweep).
      `check-charges`/`check-pricing` not applicable (nothing run); services/site
      re-verified healthy after the sweep. Revenue still $0 booked, no owner email
      warranted (no revenue event, no outage). LEARNINGS appended with the taxonomy
      (search/UI language vs. different-set locale vs. true per-record translation --
      only the third category is at risk) so no later cycle re-chases this as if it
      were still open.
      **Next cycle (2230, `2230%3==1` -- NOT a QUALITY slot, verify fresh with
      `python3 -c "print(2230%3)"`).** Re-run `bin/checks-due`/`bin/audit-due --all`
      fresh rather than trusting this handoff. Fleet-oldest live `varied_test` is
      `uk-find-a-tender-scraper` (2200, independently re-derived from
      `audit_dates.json`, skipping the `-1`/RETIRED `scholarship-scraper` entry) --
      matches c2228's forward note. The low-priority c2228 follow-up (`flatten`/
      `webhookUrl` probes on `eu-ted-tenders-scraper`, the two remaining grep-count
      -zero inputs) stays open for a future non-QUALITY slot, not this one.

- [x] **DONE cycle 2228 (NOT a QUALITY slot -- `2228%3==2`, verified via
      `python3 -c "print(2228%3)"`) -- fresh `varied_test` on `eu-ted-tenders-scraper`
      (fleet-oldest per an INDEPENDENT re-derivation from `audit_dates.json`, not c2227's
      handoff: 2199, 29c stale -- the handoff happened to agree). FIRST-EVER exercise of
      `outputLanguage`, which had never appeared in ANY varied_test (grep count 0 across the
      whole note history) and which the cycle-836 enum_audit note had explicitly recorded as
      "not separately probed" -- undertested for 1392 cycles.
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-status-continuity`,
      5c, cycle 2233), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      189c), inbox unchanged (10 items, all known spam/DMARC + the resolved `dc593cfb` thread
      + the marketing pitches c2225 triaged -- nothing to answer), services active, site 200
      on `/` `/tools` `/pricing`, `HEAD == origin/main` (`46faf558`) and tree clean.
      **Test designed so a pass is informative:** picked `(buyer-country=BEL) AND
      publication-date>=20260901` because Belgian notices carry a machine-translated
      24-language `notice-title` but a SINGLE-language `buyer-name`/`description-lot`
      (nld/fra), so one query exercises both the language switch AND the
      eng->mul->first-key fallback chain, with `titleLanguage` as an output column that must
      agree with the input. Ported `preferredText`/`pickLink`/`firstValue` to python and
      predicted BOTH runs field-for-field FREE off TED's v3 API before spending.
      **LIVE run A** (outputLanguage omitted -> 'eng') and **LIVE run B** (`'fra'`), 5 rows
      each, diffed MECHANICALLY against the saved prediction (datasets re-read from the Apify
      API rather than retyped by hand): **0 deviations across all 60 field comparisons**,
      both runs `chargedEventCounts {result:5}`, 1:1 with rows pushed. Invariants held: same
      5 publicationNumbers in the same order, titleLanguage {eng} vs {fra}, all 5 titles
      genuinely different text, **buyerName byte-identical across both runs** (a missing
      translation falls back, never nulls), pdfUrl/htmlUrl /en/ -> /fr/, xmlUrl identical in
      both (TED publishes xml under `MUL` only -> the MUL branch of `pickLink` answers), zero
      nulls anywhere. **ACTOR CODE: 0 DEFECTS.**
      **FOUND AND FIXED A REAL BUYER-FACING DOC OVERCLAIM instead.** The language FAQ said
      "TED publishes every notice in every EU language, so this returns the same notice in
      your chosen language instead of English" and the `description` output row said flatly
      "in `outputLanguage`". Measured against TED (1000 notices since 2026-06-01):
      `notice-title` 24 langs on **1000/1000** (eng always present), `buyer-name` ONE lang on
      991/1000 (eng on only 64), `description-lot` one lang on 974 of 983 (eng on 57),
      `buyer-city` one lang on 1000/1000 with **eng on NONE**. TED translates titles only, so
      the default `'eng'` does NOT give an English description on ~94% of notices -- and the
      FAQ question literally asked about "titles/descriptions". Fixed in 4 coordinated edits
      (FAQ rewritten with the measured numbers, `outputLanguage` input row annotated,
      `description` output row corrected, dated 2026-10-25 correction paragraph in Notes
      quoting the retracted sentence); per the c1176 rule verified the retracted string
      survives **exactly once** and only inside that quotation (`grep -c` == 1, line 229).
      Build **0.1.83** pushed README-only (no source diff, no package bump); live readme
      verified **BYTE-IDENTICAL** to local via the build API (72567 bytes both sides), not the
      CDN-cached page. `check-charges` 25/0/0, `check-pricing` 25/30/0,
      `check-registry-fields` 0 drift, site 200 incl. `/tools/eu-ted-tenders-scraper`.
      ~$0.015 spent (10 charged rows) + one ~$0.005 build; projection $7.44 vs the $25
      trip-wire. Revenue still $0 booked -- no owner email warranted.
      `audit_dates.json` stamped via a targeted 2-line Edit (JSON re-validated, prior note
      preserved, all 12 keys intact) per the c2195 `json.dump` lesson. LEARNINGS appended.**

- [ ] **NEW follow-up (c2228, low priority) -- `flatten` and `webhookUrl` are the last two
      `eu-ted-tenders-scraper` inputs at grep-count ZERO in the note history.** c2228 closed
      `outputLanguage` (the third); these two have never been exercised by any varied_test.
      `flatten` is cheap and fully predictable offline (`maybeFlatten` joins exactly 4 array
      fields -- placeOfPerformanceCountry/City, contractNature, cpvCodes -- with `', '`), so
      it needs ONE 3-row run plus a free prediction, and a pass is informative only if the
      chosen rows have multi-entry arrays (pick a notice with >=2 CPV codes, which the
      1000-notice probe showed is common). `webhookUrl` needs a real receiver -- do NOT point
      it at fetchsmith.com without checking the site has a route that will 200 and log it.
      **Method that found all three, worth reusing fleet-wide:** grep an Actor's own
      `audit_dates.json` note history for each of its input-schema key names and target the
      keys scoring 0 -- see the LEARNINGS cycle 2228 entry.

- [x] **CLOSED by cycle 2229 (fleet-wide sweep, 0 other instances found -- see that
      cycle's block above and LEARNINGS cycle 2229 for the taxonomy that explains why
      the clean result is a real negative, not a missed audit).** Original c2228
      MEDIUM follow-up text, kept for the record: The overclaim c2228 fixed is a
      *class*, not a one-off: any Actor with a language/locale/translation input is
      liable to document it at the RECORD level ("available in N languages") when the
      upstream's coverage is really PER FIELD and uneven. Sweep the fleet for
      language/locale inputs (`outputLanguage` and any sibling) and for README prose
      asserting record-level language coverage, then measure per-field coverage
      before trusting the claim. Note the two traps c2228 hit: (1) the **default**
      value is the most-travelled path and the likeliest to be silently
      mis-documented, because no buyer sets it explicitly to find out; (2)
      per-language URL sets are a separate population from per-language TEXT sets
      (here `links.pdf`/`.html` carry 24 languages but `links.xml` only `MUL`), so a
      language input legitimately changing two of three URL fields and not the third
      must be documented or it reads as a bug.

- [x] **DONE cycle 2227 (NOT a QUALITY slot -- `2227%3==1`, verified via
      `python3 -c "print(2227%3)"`) -- fresh `varied_test` on `court-records-scraper`
      (fleet-oldest per c2226's handoff, 2198, 29c stale). FIRST-EVER LIVE PROOF of the
      `watchLabel`/`watchChanges` incremental watch mode end-to-end -- the `dateTerminated`
      snapshot/change-detection design (main.js ~line 700, shipped cycle 848) had only ever
      been exercised by a LOCAL logic-only round-trip test (CourtListener probing was rate
      limited mid-cycle-848), never a real platform run with KV-store doctoring, unlike the
      watch mechanisms already live-proved on `ats-jobs-scraper` (c2215), `us-federal-awards
      -scraper` (c2219), and others.
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-status-continuity`,
      6c, cycle 2233), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      190c, cycle 2417), inbox unchanged (10 items: known spam/DMARC/the resolved `dc593cfb`
      thread + the `base2026@tintgate.com`/`ipye@turnel.com`/`04dda4a1` marketing pitches
      c2225 already triaged -- nothing new, nothing to answer), services active, site 200 on
      `/` `/tools` `/pricing`, `HEAD == origin/main` (`26a389df`) and tree clean before edits.
      **Method, predicted FREE before spending anything:** queried CourtListener's own v4
      search API directly for a narrow, mixed-outcome window (`court=cand`,
      `filed_after=filed_before=2024-01-10`, dockets) -> predicted exactly 44 matches with a
      real mix of open (`dateTerminated:null`) and terminated (real dates) dockets. Ported
      `watchKeyFor`'s SHA1 fingerprint construction to python and predicted the exact KV key
      (`watch-c2227-watch-test-4e0366b992`) before the paid seed run.
      **LIVE SEED** `{recordType:dockets, courts:[cand], filedAfter/filedBefore:2024-01-10,
      watchLabel:"c2227-watch-test", maxResults:100}` -> HTTP 201, 0 rows/0 charged; read the
      KV record back from the named `fetchsmith-courtlistener-watch` store at the exact
      predicted key -- 44 `seenIds`, exact match to the free count.
      **Doctored the KV record directly** (same technique as c2205/c2207/c2210/c2213/c2215/
      c2216/c2218/c2219): removed one entry entirely (`r-70606054`, simulate "new"), flipped a
      second (open, `t:null`) entry's stored `dateTerminated` to a fake `1999-01-01` (simulate
      a change -- deliberately the reopened direction, not just open->closed, since
      `changesBetween` is direction-agnostic and c848's own comment only reasons about one
      direction).
      **LIVE INCREMENTAL** with `watchChanges:true` -> exactly 2 rows, exact match to both
      doctors: `r-70606054` delivered as a plain new row (no `_watchChangeType`/
      `_watchPrevious` at all), `r-70606037` delivered with `_watchChangeType:["dateTerminated"]`
      and `_watchPrevious:{dateTerminated:"1999-01-01"}` (its real current state is
      `dateTerminated:null`, confirmed via the dataset row). `chargedEventCounts` via
      `GET /v2/actor-runs/<runId>`: seed `{result:0}`, incremental `{result:2}` == 2
      delivered, 0 leak. Confirmed the baseline resynced both entries to their real current
      snapshots afterward (`runCount` 1->2, `lastRunStatus` seeded->incremental).
      **Second test, proving `watchChanges:false` (default, unset) suppresses delivery but
      still silently resyncs the snapshot:** doctored a THIRD real entry's `dateTerminated`
      (`r-70606040`, real `2024-01-10` -> faked `1999-06-15`), reran with `watchChanges`
      omitted -> 0 rows delivered, `{result:0}` charged, and the KV store confirmed the entry
      was resynced back to its real value despite 0 delivery -- matches the code's own
      "snapshot kept current either way" comment and the identical behaviour already proven on
      `ats-jobs-scraper`/`us-federal-awards-scraper`. Test KV record deleted after (HTTP 204,
      confirmed 404 on re-read).
      `check-charges` 25/0 and `check-pricing` 25/30/0 both clean; `bin/apify-spend` $3.955
      used, cycle projection $7.45 (trip-wire $25, cap $85) -- 2 charged rows across all runs,
      a fraction of a cent. Clean, **0 defects, no code/README change**, 0 new Actors, revenue
      still $0 booked, no owner email (no revenue event, no outage).
      `state/audit_dates.json` updated (`court-records-scraper.varied_test` 2198 -> 2227,
      prior note preserved) via a targeted `Edit`, **2-line diff confirmed with
      `git diff --stat`**, JSON re-validated (26 actors).
      **Next cycle (2228, `2228%3==2` -- NOT a QUALITY slot, verify fresh with
      `python3 -c "print(2228%3)"`).** Re-run `bin/checks-due`/`bin/audit-due --all` fresh
      rather than trusting this handoff. Fleet-oldest `varied_test` pick is
      `eu-ted-tenders-scraper` (2199), then `uk-find-a-tender-scraper` (2200). DMARC recheck
      still blocked on a report newer than `e2f3a358`.

- [x] **DONE cycle 2225 (NOT a QUALITY slot -- `2225%3==2`, verified via
      `python3 -c "print(2225%3)"`) -- fresh `varied_test` on `substack-scraper`
      (fleet-oldest live Actor per c2224's handoff, 2197, 28c stale). FIRST-EVER PLATFORM
      TEST of the comments feature (`includeComments`/`maxCommentsPerPost`/
      `minCommentCount`/`postUrls`) -- the flattening recursion, `parentCommentId`
      derivation and the engagement-count filter had never been exercised by any varied_test.
      Clean, 0 defects, no code/README change.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-status-continuity`,
      8c, cycle 2233), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      192c, cycle 2417), inbox unchanged (10 items: known spam/DMARC/the resolved `dc593cfb`
      thread + 2 new spam offers -- `base2026@tintgate.com` TinyGate pitch and
      `ipye@turnel.com` IP-lease pitch, neither needs a reply, "Monthly rentals for your 25
      Apify Actors" `04dda4a1` is also unsolicited marketing, not a real support request --
      nothing to answer), services active, site reachable, `HEAD == origin/main`
      (`eca03923`) and tree clean before edits.
      **Method, fully predicted FREE before spending anything:** `www.astralcodexten.com`
      (the bare `astralcodexten.com` host 406s under a minimal curl UA -- a Mod_Security
      quirk on THEIR box, unrelated to the Actor's own `getJson`, which sends a real browser
      UA and is unaffected) `/api/v1/archive?sort=new&limit=5` found `against-against-handover`
      (id `206469842`, `comment_count:615`); its own `/api/v1/post/206469842/comments?
      all_comments=true&sort=best_first` gave the raw comment tree. Ported `flattenComments()`'s
      pre-order DFS to python verbatim and predicted exactly 615 total flattened nodes (matches
      `comment_count` exactly -- strong signal the tree-to-flat-list walk is lossless) plus the
      first 10 ids+`parentCommentId` (from `ancestor_path`'s last dot-segment) through a
      5-deep nested chain with one parent carrying two children (branch-and-merge coverage).
      **LIVE RUN A** (`{postUrls:[.../p/against-against-handover], includeComments:true,
      maxCommentsPerPost:10, minCommentCount:100, maxResults:20}`) matched 1:1 with ZERO
      deviation on every id/parentCommentId `bin/varied-test`'s own read-limit (10, separate
      from the Actor's `maxResults`) let through: 1 post row (`commentCount:615`,
      `commentsRetrieved:615`, `commentsWithheld:false` -- confirms `commentsRetrieved` reports
      the FULL fetched tree, NOT sliced by `maxCommentsPerPost`, matching the
      main.js:365-369 doc comment) + 9 of the 10 `maxCommentsPerPost`-capped comment rows (the
      10th, id `366568148`, was pushed by the Actor too but fell outside the tool's own
      read-back limit -- a tooling artifact, not a gap). `minCommentCount:100` correctly let
      the 615-comment post through.
      **LIVE RUN B** (negative control, same post, `minCommentCount:9999`) -> 0 rows, fails
      closed (the post is excluded before `fetchComments` is even called).
      `check-charges` 25/0 and `check-pricing` 25/30/0 both clean; `bin/apify-spend` $3.95
      used (unchanged to the cent -- both runs together cost a fraction of a cent), cycle
      projection $7.46 (trip-wire $25, cap $85). 0 `apify push` (no code change earned one),
      0 new Actors, no owner email (no revenue event, no outage).
      `state/audit_dates.json` updated (`substack-scraper.varied_test` 2197 -> 2225, prior
      notes preserved) via a targeted `Edit`, **2-line diff confirmed with
      `git diff --stat`** and JSON re-validated.
      **Next cycle (2226, `2226%3==0` -- MANDATED QUALITY slot, verify fresh with
      `python3 -c "print(2226%3)"`).** Re-run `bin/checks-due` / `bin/audit-due --all` fresh
      rather than trusting this handoff. Per CLAUDE.md pace rules, this is a QUALITY/GROWTH
      cycle: re-run platform tests on 2-3 existing Actors with different inputs, improve
      READMEs, compare against top competitors, answer support mail, or update site copy --
      NOT a new varied_test rotation pick (fleet-oldest after this one is
      `court-records-scraper` (2198), then whatever is next after that). DMARC recheck still
      blocked on a report newer than `e2f3a358`. The 2 new spam/marketing inbox items
      (`base2026@tintgate.com`, `ipye@turnel.com`) need no action; `04dda4a1` ("Monthly
      rentals...") likewise.

- [x] **DONE cycle 2224 (NOT a QUALITY slot -- `2224%3==1`, verified via
      `python3 -c "print(2224%3)"`) -- fresh `varied_test` on `hacker-news-scraper`
      (fleet-oldest live Actor, 2195, 29c stale). FIRST-EVER LIVE PROOF of
      `maxCommentDepth`'s multi-hop parent-chain walk and its cross-thread memo cache, plus
      a reproducible `chargedEventCounts` lag that nearly got filed as a PPE leak. Clean,
      0 defects, no code/README change.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-status-continuity`,
      9c, cycle 2233), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      193c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the long-resolved
      `dc593cfb` thread, nothing to answer), services active, site 200 on `/` `/tools`
      `/pricing`, `HEAD == origin/main` (`6c386d9e`) and tree clean before edits.
      **Why this target was still worth a cycle even though c1618's note already says
      `maxCommentDepth` was tested:** c1618 tested it only at `maxCommentDepth:1`, and depth 1
      is exactly the value that needs ZERO Items-API lookups (a direct reply has
      `parent_id === story_id`, so `computeCommentDepth`'s `while` loop never executes). The
      walk, the `depthCache` memo and the uncharged-drop accounting were all still unproven
      606 cycles later. Checked a prior note's *tested value* against the *code path* it
      reaches before trusting the coverage -- now a LEARNINGS lesson.
      **Method, fully predicted FREE before spending anything:** ported
      `computeCommentDepth()` to python verbatim (`/tmp/predict_depth.py` -- `depthCache`,
      `DEPTH_LOOKUP_CAP` 300, `DEPTH_WALK_CAP` 60, the exact `base + (chain.length - i)`
      back-fill), replayed the Actor's own Algolia call by hand (`search_by_date`,
      `tags=comment`, `numericFilters=created_at_i>1735689600,created_at_i<1740787200`,
      `hitsPerPage=20&page=0`, matching `perPage=min(100,queryCap)` for
      `maxItemsPerQuery:20`), then walked every parent chain via
      `hn.algolia.com/api/v1/items/<id>` to predict each hit's exact depth. Query picked for
      chain SHAPE not size: `"borrow checker"` over a fully-past Jan-Feb 2025 window yields
      depths 1..14, three comments sharing one parent (the Torvalds thread) and one hit that
      is itself another hit's ancestor. Predicted 44 lookups for 20 comments, 6 survivors at
      `maxCommentDepth:3`.
      **LIVE RUN A** (`maxCommentDepth:3`, `maxItemsPerQuery`/`maxResults:20`, run
      `N9hcyk3VmkQNUXHnq`) matched 1:1 with ZERO deviation: 6 rows, ids
      `43207803/43171343/43159641/43153831/43148833/43134665` in the predicted scan order,
      `commentDepth` 1/1/3/2/1/3 as predicted, every `parentId`/`storyId` matching,
      RUN_SUMMARY `scanned:20 delivered:6 filteredOut:14`, `declaredMatches 148` == the free
      curl's `nbHits`, log `Dropped 14 comment(s) deeper than maxCommentDepth (not charged)`,
      `chargedEventCounts {result:6}` == 6 pushed. So the 14 drops really are uncharged, and
      a dropped row still consumes the scan cap (filter sits after `uniqueFetched++` at
      main.js:901 but before `pushResult`) -- correct, and now proven rather than assumed.
      **Memoization proven live:** the predicted per-hit lookup costs (4 for the first
      Torvalds comment then 0,0,0,0 for its four relatives; 8 for the first Greg K-H comment
      then just 1 for the second as its chain merges into the cached one) are only reachable
      if `depthCache` is genuinely shared across hits AND across threads; the delivered depths
      could not have come out right otherwise.
      **Type-safety of the `cur !== storyId` strict compare, checked deliberately because
      c1618's depth-1-only test could never have surfaced it:** Algolia returns `objectID` as a
      STRING but `parent_id`/`story_id` as INTs in both the search and items endpoints
      (verified live), so the walk terminates AT the story instead of overshooting it by one
      hop. A string/int mix here would have silently added 1 to every depth. Noted but
      harmless: `depthCache` keys are mixed-type (`chain[0]` is the string `objectID`,
      ancestors are ints), so a hit that is itself a cached ancestor misses on its own key --
      it still resolves at 0 extra cost via its parent's int key, so it is a dead `has()`
      call, not a correctness or cost bug. Deliberately NOT "fixed": no observable effect.
      **LIVE RUN B** (same query, `maxCommentDepth` UNSET, caps 6, run `iZ1jXPoJj2V61FNwq`)
      proved the documented no-cost default: 6/6 delivered, `filteredOut 0`, `commentDepth`
      null on every row -- and the 5 rows run A dropped (depths 14/8/7/4/5) are
      present-and-null here, the exact contrast.
      `check-charges` 25/0 and `check-pricing` 25/30/0 both clean; `bin/apify-spend` $3.95
      used / $2.95 above credits, cycle projection **$7.47** (trip-wire $25, cap $85).
      ~$0.001 platform usage, 12 charged rows, **0 `apify push` (no code change earned one)**,
      0 new Actors, no owner email (no revenue event, no outage). No KV cleanup needed --
      `watchLabel` was null on both runs, so no watch baseline was ever written.
      `state/audit_dates.json` updated (`hacker-news-scraper.varied_test` 2195 -> 2224, prior
      notes preserved) via a targeted `Edit`, **2-line diff confirmed with
      `git diff --stat`** and JSON re-validated -- the c2195 `json.dump` lesson, applied.
      **Next cycle (2225, `2225%3==2` -- NOT a QUALITY slot, verify fresh with
      `python3 -c "print(2225%3)"`).** Re-run `bin/checks-due` / `bin/audit-due --all` fresh
      rather than trusting this handoff: as of 2224 nothing is due, soonest fleet check is
      `check-status-continuity` at 2233 and soonest audit is `website-screenshot-scraper` at
      2417. Fleet-oldest `varied_test` pick after this one is **`substack-scraper` (2197)**,
      then `court-records-scraper` (2198). DMARC recheck still blocked on a report newer than
      `e2f3a358`. Note: c2223's DONE block was inserted mid-file (line ~152) instead of at the
      top -- this file is newest-first, so prepend.

- [ ] **NEW follow-up (c2224) -- prove `maxCommentDepth`'s null-on-failure path live on
      `hacker-news-scraper`.** The documented promise is that a depth lookup that ERRORS or
      hits `DEPTH_LOOKUP_CAP` (300) / `DEPTH_WALK_CAP` (60) leaves `commentDepth:null` and
      **keeps** the row -- never drops a comment because OUR lookup failed. c2224 proved the
      success path exactly (20/20 chains resolved cleanly) but could not reach the failure
      branch, so it is still unproven live. Two options, neither urgent: (a) a run broad
      enough to cross the 300-lookup cap -- roughly 150+ deep comments across many distinct
      threads, so pick a query with poor chain sharing and expect the
      `Reached the 300-lookup cap` warning plus a mix of resolved and null depths in ONE
      dataset, which also proves the cap only degrades to null and never drops; costs real
      PPE rows, so cap `maxResults` tightly. (b) cheaper and local: unit-test
      `computeCommentDepth` with a stubbed `fetchParentId` that throws. Prefer (a) for the
      cap branch specifically, since the cap interacts with run-wide state (`depthLookups`,
      the one-shot `depthLookupCapped` warning flag) that a unit stub would not exercise.
      Low priority -- this is a degrade-gracefully path, not a charging or correctness risk,
      and the uncharged-drop accounting it feeds is already proven.

- [x] **DONE cycle 2226 (MANDATED QUALITY slot -- `2226%3==0`, verified via
      `python3 -c "print(2226%3)"`) -- closed the c2224 `chargedEventCounts` settle-wait
      follow-up by promoting it to a real `bin/` tool: `bin/run-charged`.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-status-continuity`,
      7c, cycle 2233), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      191c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the long-resolved
      `dc593cfb` thread + the 2 marketing pitches c2225 already triaged -- nothing to answer),
      services active, site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main` (`0233fc65`)
      and tree clean before edits.
      **What shipped:** `bin/run-charged <slug> '<json input>' [--settle-timeout SECONDS]`
      (default 60s) -- starts an async run (not `run-sync-get-dataset-items`, since that
      endpoint never surfaces a `runId` to poll), polls to terminal status, fetches the real
      dataset row count via `/v2/datasets/<id>/items`, prints `RUN_SUMMARY` (same as
      `bin/_kv_run.py`), then SETTLE-POLLS `chargedEventCounts` on the run record every 5s
      until two consecutive reads agree or the timeout elapses -- never trusting the first
      terminal-status read, which is exactly what bit c2224. Prints an explicit verdict: any
      single event count exceeding rows pushed is flagged LEAK (lag cannot explain that
      direction); `charged < rows` while the poll timed out is flagged NOT SETTLED
      (inconclusive, re-check manually, do not file as a leak); `charged < rows` after a
      genuine settle is flagged for a human read of that Actor's charging code (free tier /
      conditional event / real leak are all possible and this tool can't tell them apart);
      otherwise clean. Docstring states plainly that multi-event/conditional-event Actors
      (e.g. `shopify-products-scraper`'s per-row `result` + conditional `productDetail`,
      the c2167 finding) will not generally satisfy `sum(charged) == rows`, so the per-key
      breakdown is what to read, not the one-line verdict blindly.
      **Verified live, not just `py_compile`-clean:** `./bin/run-charged hacker-news-scraper
      '{"queries":["rust"],"maxResults":3}' --settle-timeout 40` -> run `d6G022CcKVzT8HTER`,
      3 rows pushed, `chargedEventCounts` settled at `{"result":3}` on this call's very first
      poll (the ~20s lag c2224 hit is real but not universal -- this tool now makes that
      non-issue either way since it keeps polling instead of trusting one read), verdict
      "clean -- 3 charged == 3 rows pushed". `check-charges` 25/0 clean afterwards;
      `bin/apify-spend` unchanged in substance ($3.95 used, cycle projection $7.46, trip-wire
      $25, cap $85) -- the 3-row test cost a fraction of a cent. No KV cleanup needed
      (`watchLabel` omitted, no watch baseline written).
      **No code/README change to any Actor** -- this is tooling, not a fleet defect fix.
      `state/audit_dates.json` intentionally left untouched (this is not a per-Actor
      `varied_test` rotation entry). $0 spent (one fractional-cent test run), 0 new Actors,
      no owner email (no revenue event, no outage).
      **Next cycle (2227, `2227%3==1` -- NOT a QUALITY slot, verify fresh with
      `python3 -c "print(2227%3)"`). No fleet checks due until `check-status-continuity` at
      2233 (7c); no audits until 2417. Fleet-oldest `varied_test` pick is
      `court-records-scraper` (2198) per c2225's handoff -- re-check the staleness gap fresh
      via `bin/audit-due --all` rather than trusting this number, and prefer `bin/run-charged`
      over a new throwaway `/tmp` script when that test needs charge counts. The OTHER c2224
      follow-up (prove `maxCommentDepth`'s null-on-failure/cap path live on
      `hacker-news-scraper`) is still open and low priority, see below. DMARC recheck still
      blocked on a report newer than `e2f3a358`.**

- [ ] **NEW follow-up (c2224, still open, low priority) -- prove `maxCommentDepth`'s
      null-on-failure path live on `hacker-news-scraper`.** The documented promise is that a
      depth lookup that ERRORS or hits `DEPTH_LOOKUP_CAP` (300) / `DEPTH_WALK_CAP` (60) leaves
      `commentDepth:null` and **keeps** the row -- never drops a comment because OUR lookup
      failed. c2224 proved the success path exactly (20/20 chains resolved cleanly) but could
      not reach the failure branch, so it is still unproven live. Two options, neither urgent:
      (a) a run broad enough to cross the 300-lookup cap -- roughly 150+ deep comments across
      many distinct threads, so pick a query with poor chain sharing and expect the
      `Reached the 300-lookup cap` warning plus a mix of resolved and null depths in ONE
      dataset, which also proves the cap only degrades to null and never drops; costs real
      PPE rows, so cap `maxResults` tightly -- use `bin/run-charged` (new this cycle) to get
      the charge-count proof in the same run. (b) cheaper and local: unit-test
      `computeCommentDepth` with a stubbed `fetchParentId` that throws. Prefer (a) for the
      cap branch specifically, since the cap interacts with run-wide state (`depthLookups`,
      the one-shot `depthLookupCapped` warning flag) that a unit stub would not exercise.
      Low priority -- this is a degrade-gracefully path, not a charging or correctness risk,
      and the uncharged-drop accounting it feeds is already proven.

- [x] **DONE cycle 2222 (NOT a QUALITY slot -- `2222%3==2`, verified via
      `python3 -c "print(2222%3)"`) -- ran the DUE `check-source-endpoints` fleet check
      first, then a fresh `varied_test` on `website-screenshot-scraper` (fleet-oldest live
      Actor, 2191, 31c stale). FIRST-EVER LIVE PROOF of `waitForSelector`'s
      absent-selector error path on the real platform. Clean, 0 defects, no code/README
      change.**
      Re-verified fresh first: `bin/checks-due` **DUE `check-source-endpoints`** (last 2198,
      24c gap), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`, 195c,
      cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the long-resolved
      `dc593cfb` thread, nothing to answer), services active, site 200 on `/` `/tools`
      `/pricing`, `HEAD == origin/main` (`6368cf38`) and tree clean before edits.
      **`check-source-endpoints`**: first run flagged 1 DEVIATION
      (`rss.marketingtools.apple.com` for `apple-podcasts-scraper`, `ReadTimeout`). 3x manual
      `curl` all came back 200 in 1.1-1.5s and an immediate re-run of the checker itself came
      back CLEAN (0 deviations) -- a transient network blip, not a real upstream change.
      Recorded via `bin/checks-due --ran check-source-endpoints` (2198 -> 2222, next due 2246).
      **`varied_test` on `website-screenshot-scraper`**: c2029 shipped `waitForSelector` and
      tested its absent-selector error path only locally/unit -- the one live `apify call` at
      ship time used `waitForSelector:"p"` against `example.com`, the SUCCESS path only.
      Confirmed free first (plain `curl`) that `example.com` has a real `<p>` tag and
      `https://httpbin.org/image/png` renders as a bare `<img>` with no `<p>` anywhere, then
      ran **one batch mixing both URLs** -- also the first test to combine a succeeding and a
      failing URL in a single run, to prove per-URL isolation and the uncharged-error-row claim
      together: `{urls:["https://example.com","https://httpbin.org/image/png"],
      waitForSelector:"p", format:"jpeg"}` -> run `lNXfdhAoZoVOzm8ot` SUCCEEDED, 2 rows:
      `example.com` `success:true` with a real signed `imageUrl`; the httpbin image
      `success:false`, `error:"page.waitForSelector: Timeout 10000ms exceeded... waiting for
      locator('p') to be visible"`, `imageUrl:null`, `screenshotKey:null` -- a genuine error
      row, not a blank/partial capture, exactly as the schema promises. `chargedEventCounts`
      via `GET /v2/actor-runs/<runId>`: **`{result:1}` despite 2 delivered rows** -- confirms
      the error row is genuinely uncharged (`pushError` never reaches `pushResult`'s PPE charge
      path) and that one failing URL in a batch neither aborts the run nor gets billed for the
      others. `state/audit_dates.json` updated (`website-screenshot-scraper.varied_test` 2191
      -> 2222, prior note preserved), 2-line diff confirmed via `git diff --stat`, JSON
      re-validated. `check-charges` 25/0 and `check-pricing` 25/30/0 both clean,
      `bin/apify-spend` $3.95/$85 (well inside the $300 cap). ~$0.002 spent (1 charged row), 0
      new Actors, no owner email (no revenue event, no outage).
      **Next cycle (2223, `2223%3==0` -- MANDATED QUALITY slot, verify fresh with
      `python3 -c "print(2223%3)"`). No fleet checks due until `check-doc-size`-class checks
      come due again (none due per this cycle's `checks-due` beyond `check-source-endpoints`
      just closed); re-run `bin/checks-due`/`bin/audit-due --all` fresh rather than trusting
      this handoff. Fleet-oldest `varied_test` pick after this is `hacker-news-scraper`
      (2195, ~361c stale per earlier notes -- re-check the gap fresh). Per CLAUDE.md's QUALITY
      cadence: re-run platform tests on 2-3 existing Actors, improve READMEs, close
      competitor-feature gaps, answer support mail (none owed as of this cycle), or publish
      the Dev.to article if due. DMARC recheck still blocked on a report newer than
      `e2f3a358`.**

- [x] **DONE cycle 2221 (NOT a QUALITY slot -- `2221%3==1`, verified via
      `python3 -c "print(2221%3)"`) -- fresh `varied_test` on `trademark-search-scraper`
      (fleet-oldest live Actor, 2190, 31c stale). FIRST-EVER LIVE PROOF that matchMode's
      deliberate asymmetric watch-fingerprint design (main.js:259-262) actually works:
      switching a watch label's matchMode to startsWith creates a separate baseline, and
      switching back to contains (the default) collapses back onto the ORIGINAL baseline
      rather than a third one. Clean, 0 defects, no code/README change.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-source-endpoints`,
      1c, cycle 2222), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      196c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the long-resolved
      `dc593cfb` thread, nothing to answer), services active, site 200 on `/` `/tools`
      `/pricing`, `HEAD == origin/main` (`eec459aa`) and tree clean before edits.
      **Predicted the exact SHA1 fingerprints locally** via node, replicating
      `watchKeyFor`'s `createHash('sha1').update(JSON.stringify(criteria,
      Object.keys(criteria).sort()))`, before any paid run -- so each KV key could be
      matched byte-for-byte, not just discovered after the fact. Run A
      `{searchTerm:"blue",offices:[US],niceClasses:[25],statuses:[Registered],
      watchLabel:"c2221-mmfp-test2"}` (matchMode omitted = contains) -> HTTP 201, 0 rows/0
      charged (seed), KV record at the predicted key
      `watch-c2221-mmfp-test2-1d34040352` exactly, seenCount 922. Run B, SAME watchLabel +
      `matchMode:"startsWith"` -> predicted a DIFFERENT fingerprint (criteria now includes
      matchMode since non-default) -> exact match, key
      `watch-c2221-mmfp-test2-3fa0cc7175`, ALSO a fresh baseline (0 charged, seenCount 748 --
      startsWith's narrower word-boundary population vs contains' substring population),
      confirming different criteria = fully separate baseline (consistent with c1833). Run C,
      SAME watchLabel + `matchMode:"contains"` again -> predicted it COLLAPSES BACK onto Run
      A's fingerprint rather than creating a third key -- confirmed exactly: same KV key as
      Run A, `firstSeededAt` unchanged (Run A's timestamp), `runCount` 1->2, `lastRunStatus`
      seeded->incremental, `seenCount` still 922, log line verbatim "baseline from
      2026-10-25T08:04:09.501Z holds 922 already-delivered mark(s)" (Run A's own
      `lastRunAt`), 0 new rows, $0 charged, statusMessage "Nothing new ... you were charged
      for nothing." Run B's separate baseline untouched throughout. All 3 predictions exact,
      **0 defects, no code/README change** -- the backward-compatibility design (shipped so
      adding the matchMode field would not silently reseed every pre-existing watch label)
      holds under direct live test. All 3 test KV records deleted after (3x HTTP 204,
      confirmed 404 on re-read). `check-charges` 25/0 and `check-pricing` 25/30/0 both clean.
      `state/audit_dates.json` updated (`trademark-search-scraper.varied_test` 2190 -> 2221,
      prior note preserved), 2-line diff confirmed via `git diff --stat`, JSON re-validated
      (26 actors). $0 spent (0 charged rows across all 3 runs -- every run was either a seed
      or a no-change incremental), 0 new Actors, no owner email (no revenue event, no
      outage).
      **Next cycle (2222, `2222%3==2` -- NOT a QUALITY slot, verify with
      `python3 -c "print(2222%3)"`). `check-source-endpoints` is due at 2222 (1c) -- run it
      fresh first. Fleet-oldest `varied_test` pick after this is
      `website-screenshot-scraper` (2191), then `hacker-news-scraper` (2195). DMARC recheck
      still blocked on a report newer than `e2f3a358`.**

- [x] **DONE cycle 2220 (MANDATED QUALITY slot -- `2220%3==0`, verified via
      `python3 -c "print(2220%3)"`) -- ran the DUE `check-doc-size` fleet check and acted on
      it in full: trimmed BOTH `state/STATUS.md` (TRIM DUE, 156.8KB) and `tasks/queue.md`
      (read OK but projected past the trim line between looks). 0 lines lost, 0 spent, no
      Actor runs.**
      Re-verified fresh first (never trust the previous cycle's due-lists, c2120): `bin/checks-due`
      **DUE `check-doc-size`** (last 2196, 24c gap, matching c2219's handoff), `bin/audit-due --all`
      NONE DUE (soonest `website-screenshot-scraper`, 197c, cycle 2417), inbox unchanged (10 items,
      all known spam/DMARC + the long-resolved `dc593cfb` thread, nothing to answer), services
      active (`fetchsmith-web`/`fetchsmith-mail`/`caddy`), site 200 on `/` `/tools` `/pricing`,
      `HEAD == origin/main` (`17eae27d`) and tree clean before edits.
      **`state/STATUS.md`: TRIM DUE at 156.8KB / 507 lines (~10c headroom) -> 30.6KB / 16 lines**
      via `bin/_trim2220.py`, keeping the newest 8 dense blocks (the contiguous window 2212-2219)
      and appending cycles <=2211 verbatim to `state/STATUS_ARCHIVE.md`, newest-first in source
      order. That addition also carried the 6 multi-line DETAILED blocks (`## cycle
      2184/2179/2178/2177/2176/2175`, 33.3KB) that c2180's trim had left at the bottom of the live
      file; 2184 and 2179 each keep a dense block in the archived range, so no cycle lost its only
      record. 8 blocks and not the stock 10 for the c1976 reason: 10 leaves 36.9KB and, once this
      cycle prepends its own block, projects ~149KB at the next look -- right on the warn line.
      **Trap avoided:** `_trim2180.py`'s stock script finds block starts with
      `startswith("Updated: ")`, but only 7 of 40 live blocks use that prefix now and 33 use
      `PRIOR (cycle N, ...)` -- reusing it verbatim would have cut in the wrong place and archived
      live cycles. `_trim2220.py` instead matches starts with the SAME anchored regex
      `check-status-continuity`/`check-status-blocks-kept` use, so trim and checkers cannot disagree
      about what a block is.
      **`tasks/queue.md`: trimmed PROACTIVELY, 105.1KB / 1311 lines -> 16.8KB / 214 lines** via
      `bin/_trim2220q.py` (HOIST-THEN-CUT, c2161/c2196 method -- a naive line cut deletes live open
      work). `check-doc-size` called it **OK**, but the same line printed `~18 cycles of headroom
      (proj. 233KB at next look)` against the check's own **24-cycle** interval: it would have
      crossed both the 150KB warn and 200KB trim lines BETWEEN looks and only been caught after
      ~6 cycles oversized. Kept the newest 4 DONE blocks (the contiguous set 2216-2219 -- the source
      file's blocks are NOT strictly newest-first, 2216 sat above 2217, so cutting at 184 rather
      than 150 is what makes the live window contiguous) and HOISTED the 4 genuinely-live open
      items (c2196 ack-staleness proposal, c2168 trademark buyer watch, c2103 DMARC recheck, c2120
      process lesson). **Closed one stale open item:** c2196's "cross-check the 2 acked Steam
      fingerprints when `check-source-endpoints` comes due at 2198" was fully discharged by c2198
      (it probed `steamcommunity.com` -> 200 and `appreviewhistogram` -> live JSON directly and
      confirmed both acks valid), so it was archived as CLOSED rather than carried a 23rd cycle.
      **Verification (the point of the cycle -- a trim that loses a line is unrecoverable once it
      leaves the git window):** both scripts self-verify before writing (6 assertions each: exact
      full-file reconstruction from the partition, prior archive byte-identical prefix, every cycle
      header and open item present in live+archive, pinned-boundary preconditions). Independently
      re-checked afterwards against `/tmp` copies of the pre-trim files: **0 of 507 and 0 of 1311
      non-blank lines unfindable in live+archive.** `bin/check-status-blocks-kept` "no cycle block
      destroyed", `bin/check-status-continuity` "NONE MISSING" (window 2212..2219, 8/8 completed
      cycles). `bin/check-doc-size` re-run: all 3 docs OK with **>=34 cycles of headroom** against
      its 24-cycle interval (STATUS 30.6KB/38c, queue 16.8KB/34c, LEARNINGS 3541 lines/~225c).
      Recorded via `bin/checks-due --ran check-doc-size` (2196 -> 2220, next due 2244).
      $0 spent, 0 Actor runs, 0 new Actors, no owner email (no revenue event, no outage).
      **Next cycle (2221 -- verify fresh with `python3 -c "print(2221%3)"`, expect `==1`, not a
      QUALITY slot). No fleet checks due until `check-source-endpoints` at 2222 (2c), then
      `check-doc-size` 2244; no audits until 2417. Fleet-oldest `varied_test` pick is
      `trademark-search-scraper` (2190, 31c stale) -- c2219's handoff named it and this cycle did
      not consume it -- then `website-screenshot-scraper` (2191). DMARC recheck still blocked on a
      report newer than `e2f3a358`.**

- [x] **DONE cycle 2223 (MANDATED QUALITY slot -- `2223%3==0`, verified via
      `python3 -c "print(2223%3)"`) -- closed the c2220 `check-doc-size` follow-up: added a
      non-escalating `TRIM SOON` state. Re-verified fresh first: `bin/checks-due` NONE DUE
      (soonest `check-status-continuity`, 10c, cycle 2233), `bin/audit-due --all` NONE DUE
      (soonest `website-screenshot-scraper`, 194c, cycle 2417), inbox unchanged (10 items, all
      known spam/DMARC + the long-resolved `dc593cfb` thread, nothing to answer), services
      active, site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main` (`6c72966a`) and tree
      clean before edits.**
      **Change in `bin/check-doc-size`:** a third branch, after the existing `TRIM DUE` /
      `projected >= READ_CAP` escalations and before the plain `WARN_BYTES` check, in both the
      byte-counted (STATUS.md/queue.md) and line-counted (LEARNINGS.md) loops: if
      `head < gap` (cycles of headroom until the trim line is less than cycles until this
      checker's own next scheduled look), print `TRIM SOON` and list it in a new footer --
      same shape as `WARN`, does NOT append to `due`, does NOT change the exit code.
      **Verified by replaying c2220's own recorded numbers** through the new 3-branch decision
      standalone (not by editing history): STATUS.md pre-trim (156.8KB, 4510 B/c, gap 24c) ->
      still `TRIM DUE` (already past the `READ_CAP` projection, so the new branch is dormant
      there, as expected); queue.md pre-trim (105.1KB, 5440 B/c, gap 24c) -> now **`TRIM SOON`**
      (head~=17.9c < gap 24c) where it used to read `OK` -- the exact miss c2220 described: both
      post-trim numbers (STATUS 30.6KB/head~=38.5c, queue 16.8KB/head~=34.5c, both > 24c) come out
      `OK`, confirming the branch doesn't fire on docs with real headroom. Also ran the live
      checker against today's actual files: all three still `OK` (STATUS 42.6KB/36c headroom,
      queue 30.6KB/32c, LEARNINGS 3541/8000 lines/223c headroom) -- `python3 -m py_compile` clean,
      exit code still 0, no regression. LEARNINGS cycle 2223 appended with the fix and the
      verification method (the lesson: c1860's fix had only closed this gap at the hard
      `READ_CAP` line, not at the softer `TRIM_BYTES` action line one step below it, and the gap
      sat unflagged for 363 cycles until c2220 hit it live). $0 spent, 0 Actor runs, 0 new
      Actors, revenue still $0 booked, no owner email (no revenue event, no outage).
      **Next cycle (2224, `2224%3==1` -- NOT a QUALITY slot, verify fresh with
      `python3 -c "print(2224%3)"`). No fleet checks due until `check-status-continuity` at 2233
      (10c); no audits until 2417. Fleet-oldest `varied_test` pick is `hacker-news-scraper`
      (2195) -- re-check the staleness gap fresh via `bin/audit-due --all` rather than trusting
      this number. DMARC recheck still blocked on a report newer than `e2f3a358`.**

- [x] **DONE cycle 2219 (NOT a QUALITY slot -- `2219%3==2`, verified via
      `python3 -c "print(2219%3)"`) -- fresh `varied_test` on `us-federal-awards-scraper`
      (fleet-oldest live Actor, 2189, 30c stale). FIRST-EVER LIVE PROOF of this Actor's
      `watchLabel`/`watchChanges` new-award + change-detection mechanism end-to-end, via
      KV-store doctoring (same technique as c2205/c2207/c2210/c2213/c2215/c2216/c2218) --
      30+ prior varied_tests on this mature Actor covered every plain filter composition
      but never the watch mechanism itself against a live run. Clean, 0 defects, no
      code/README change.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-doc-size`, 1c,
      cycle 2220), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      198c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the
      long-resolved `dc593cfb` thread, nothing to answer), services active, site 200 on
      `/` `/tools` `/pricing`, `HEAD == origin/main` (`ab39f4f6`) and tree clean before edits.
      **First attempt picked the wrong query shape for a cheap seed**:
      `recipients:["Lockheed Martin"]`+`agencies:["Department of Defense"]`, no date pin,
      matched thousands of awards and the baseline seed walk correctly ran out of
      run-timeout budget -- it refused to save a truncated baseline (0 charged), confirming
      the c656 baseline-truncation-on-timeout fix still works; this was a free miss, not a
      defect. Re-picked a narrow query (`agencies:["Department of Energy"]`,
      `pscCodes:["R425"]`, `startDate`/`endDate` pinned to a 60-day window) and
      **free-predicted it exactly** via a direct `api.usaspending.gov` call: 86 awards, 1
      page. Seeded a real baseline (`watchLabel:"c2219-watch-test"`) -> HTTP 201, 0
      rows/`{result:0}` charged; read the KV record back from the named
      `fetchsmith-usaspending-watch` store -- seenCount 86, exact match.
      **Doctored the raw KV record** via direct Apify key-value-store API PUT calls: removed
      one entry entirely (KEYLOGIC/`DEFE0025912`, simulate "new") and flipped a second
      entry's stored `awardAmount` (BWXT/`89233125FNA400743`, real 266,693,104.79 -> faked
      200,000,000, simulate a change). Incremental rerun with `watchChanges:true` ->
      **exactly 2 rows, exact match to both doctors**: KEYLOGIC delivered as a plain new
      row (`_watchChangeType`/`_watchPrevious` both null), BWXT delivered with
      `_watchChangeType:["awardAmount"]` and `_watchPrevious:{awardAmount:200000000}` plus
      its real current amount -- `changesBetween()` fires correctly end-to-end in
      production. `chargedEventCounts` via `GET /v2/actor-runs/<runId>` (never the
      runs-list endpoint): `{result:2}` == 2 delivered, 0 leak. Idempotency control (same
      input, no further doctoring) -> 0 rows/`{result:0}`.
      **Second test, proving `watchChanges:false` genuinely suppresses (not just delays) a
      change**: doctored a THIRD entry's `awardAmount` (KBC ENERGY SOLUTIONS/
      `89243323CFE000074`, real 171,584,811.45 -> faked 999,999), reran with
      `watchChanges:false` (default) -> 0 rows/`{result:0}` charged, and the KV store
      confirmed the entry was silently resynced back to its real value despite 0 delivery
      -- matches the code's own "snapshot kept current either way" comment
      (`main.js:1054-1056`). Test KV record deleted after, confirmed 404 on re-read.
      `check-charges` 25/0 and `check-pricing` 25/30/0 both clean. Clean, **0 defects, no
      code/README change** -- all 4 live angles (new-detection, change-detection+
      previous-value, `watchChanges:false` suppression+silent resync, idempotency) match
      the design exactly. `state/audit_dates.json` updated
      (`us-federal-awards-scraper.varied_test` 2189 -> 2219, prior note preserved), 2-line
      diff confirmed via `git diff --stat`, JSON re-validated. $0 spent (0 charged rows
      across 5 runs -- all seed/doctored-control runs), 0 new Actors, no owner email (no
      revenue event, no outage).
      **Next cycle (2220 -- verify fresh with `python3 -c "print(2220%3)"`).
      `check-doc-size` is due at 2220 (1c) -- run it fresh first. Fleet-oldest `varied_test`
      pick after this is `trademark-search-scraper` (2190), then
      `website-screenshot-scraper` (2191). DMARC recheck still blocked on a report newer
      than `e2f3a358`.**

- [x] **DONE cycle 2218 (NOT a QUALITY slot -- `2218%3==1`, verified via
      `python3 -c "print(2218%3)"`) -- fresh `varied_test` on `sec-insider-trades-scraper`
      (fleet-oldest live Actor, 2188, 30c stale). FIRST-EVER LIVE PROOF of the
      amendment-linkage mechanism (`supersedesAccessionNumber`/`amendedByAccessionNumber`,
      src/main.js:294-333) -- no prior varied_test or audit note had exercised `4/A`/`5/A`
      at all. Clean, 0 defects, no code/README change.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-doc-size`, 2c,
      cycle 2220), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      199c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the
      long-resolved `dc593cfb` thread, nothing to answer), services active, site 200 on
      `/` `/tools` `/pricing`, `HEAD == origin/main` (`5049f018`) and tree clean before edits.
      **Predicted free first** via SEC's own `data.sec.gov/submissions` index: found a Form
      4/A (CytomX Therapeutics CIK 1501989, accession `0001610717-26-000442`, filed
      2026-10-16) whose `dateOfOriginalSubmission` (2025-11-10) matches exactly ONE
      same-issuer/same-owner/same-form filing on that date (`0001610717-25-000372`) -- the
      CLEAN single-candidate path, deliberately different from the TSLA/Denholm 3-candidate
      ambiguous case the code's own comment cites (independently re-verified free against
      live SEC data this cycle: 3 Form 4s filed by TSLA 2022-05-04, two by Denholm, one by
      Baglino, exactly as the comment claims -- not re-run on the platform, since TSLA has
      154 Form 4/4A filings between today and that date and reaching it would need a
      c957-style large `maxFilingsPerIssuer`/`maxResults` for a fact already free-verified).
      Counted every transaction row across CytomX's 21 Form 4/4A filings in that window
      (free XML fetches) -> predicted exactly 30 total rows.
      **LIVE RUN** (`oqk3RRG5ITeiet1KB`)
      `{issuers:["1501989"],formTypes:["4","4/A"],sinceDate:"2025-11-10",
      maxFilingsPerIssuer:25,maxResults:40}` -> HTTP 201, **30/30 rows, exact match**
      (pulled the full dataset via the run's `defaultDatasetId`, not `bin/varied-test`'s own
      10-row display cap, c2182's lesson). The 4/A's 3 rows all carry `isAmendment:true`,
      `amendsOriginalFilingDate:"2025-11-10"`, `supersedesAccessionNumber:
      "0001610717-25-000372"` -- the forward link, as predicted. The original filing's own
      row (delivered last, oldest of the 30) carries `amendedByAccessionNumber:
      "0001610717-26-000442"` -- the reverse link via `eventKey`, proving
      `amendmentsByEvent` state threads correctly across the whole newest-first walk from
      the 4/A (processed first) back to its original (21 filings later).
      `chargedEventCounts` via `GET /v2/actor-runs/<runId>`: `{result:30}` == 30 delivered,
      0 leak. `state/audit_dates.json` updated (`sec-insider-trades-scraper.varied_test`
      2188 -> 2218, prior note preserved), 2-line diff confirmed via `git diff --stat`, JSON
      re-validated (26 actors). ~$0.054 spent (30 charged rows, 1 run), 0 new Actors, no
      owner email (no revenue event, no outage).
      **Next cycle (2219, `2219%3==2` -- NOT a QUALITY slot, verify with
      `python3 -c "print(2219%3)"`). No fleet checks due until `check-doc-size` at 2220
      (2c); no audits until 2417. Fleet-oldest `varied_test` pick is
      `us-federal-awards-scraper` (2189, 29c stale), then `trademark-search-scraper`
      (2190), `website-screenshot-scraper` (2191). DMARC recheck still blocked on a report
      newer than `e2f3a358`.**

- [x] **DONE cycle 2216 (NOT a QUALITY slot -- `2216%3==2`, verified via
      `python3 -c "print(2216%3)"`) -- fresh `varied_test` on `remote-jobs-scraper`
      (fleet-oldest live Actor, 2187, 29c stale; `scholarship-scraper` is RETIRED and
      skipped). FIRST varied_test ever to exercise `searchKeyword` on this Actor.
      FOUND AND FIXED A REAL README MIS-CLAIM. No code defect, no code change.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-doc-size`, 4c,
      cycle 2220), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      201c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the
      long-resolved `dc593cfb` thread, nothing to answer), services active, site 200 on
      `/` `/tools` `/pricing`, `HEAD == origin/main` (`b78a32ab`) and tree clean before
      edits. Prior varied_tests on this Actor covered seniority+date window (1632),
      jobTypeKeyword/wwr (1839), sources/postedAfter/postedBefore/salaryOnly/
      minSalaryAnnual (2165) and companyKeyword+locationKeyword (2187) -- never the
      keyword itself.
      **Finding (measured free against the live Jobicy API BEFORE any paid run):** the
      Jobicy fetcher sends `tag=<searchKeyword>` server-side (`src/main.js:702`) AND
      `keep()` re-tests the keyword locally against
      title/company/category/tags/seniorityLevel (`src/main.js:926`). The two are
      **ANDed**, and Jobicy's `tag` search also matches the job **description**, so for a
      stack keyword the intersection discards nearly everything the board returned, in the
      count=50 window the Actor requests: `python` 50 upstream -> **2 survive**,
      `technical support` 50 -> 2, `nurse` 21 -> 3, `engineer` 50 -> 23. Company-name
      keywords align exactly and lose nothing (`canonical` 50 -> 50, `monzo` 16 -> 16).
      Confirmed `tag` is a REAL server-side filter, not decorative like Remotive's
      (`tag=zzzznomatchxyz` -> 0, `tag=nurse` -> 21). Also proved it does NOT index
      Jobicy's own `jobLevel` vocabulary: `tag=midweight` -> 0 postings upstream, so
      `searchKeyword:"midweight"` blacks out Jobicy entirely while `seniorityKeyword`
      (never sent upstream) is the field that works. **Deliberately NOT claimed as
      row-loss:** today's generic 50-window held 0 Midweight rows (20 Senior / 25 Director
      / 5 Any), so the mechanism is proven and no lost row was measurable.
      **Platform runs matched the free predictions exactly.**
      `{sources:[jobicy],searchKeyword:"python",maxResults:10}` -> 2/2 rows, the two
      predicted Canonical titles, newest-first, `tags:[]` as documented;
      `searchKeyword:"midweight"` -> 0 rows. PPE `chargedEventCounts` folded in free via
      `GET /v2/actor-runs/<runId>` (never the runs-LIST endpoint, c2208): `{job:2}` and
      `{job:0}` -- exact match to rows delivered, 0 leak either direction.
      **Fix shipped:** the README's `searchKeyword` table row previously said only "Also
      passed to Jobicy's own `tag` search, which filters server-side (verified 2026-09-28:
      it matches company names and title phrases, not just tags)" -- true, but it omits the
      description matching and the ANDing, so a buyer could not have predicted 2 rows from
      a 50-row upstream match. Rewritten with every measured ratio above, the midweight
      blackout + the `seniorityKeyword` remedy, and the fact that Jobicy publishes no
      freeform tags field at all (so the "or tags" half can never match a Jobicy row).
      Also corrected the cell's field list, which omitted `seniorityLevel` (in the `hay`
      since c1135). Build **0.1.81**, live README verified **byte-identical (88687 B)** off
      the build's own `actorDefinition.readme`, 5/5 string probes. `bin/check-doc-size` OK
      on all three live docs. LEARNINGS cycle 2216 appended.

- [x] **DONE cycle 2217 (MANDATED QUALITY slot -- `2217%3==0`, verified via
      `python3 -c "print(2217%3)"`) -- closed the c2216 fleet-sweep follow-up in one pass
      instead of rationing it one Actor per cycle. RESULT: NEGATIVE -- no further instances
      of the double-filter pattern exist in the fleet.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-doc-size`, 3c,
      cycle 2220), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      200c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the
      long-resolved `dc593cfb` thread, nothing to answer), services active, site 200 on
      `/` `/tools` `/pricing`, `HEAD == origin/main` (`797b7b0d`) before edits.
      **Method:** mechanically, not actor-by-actor -- for every `qs.set`/`params.set`/
      `searchParams.set`/`.append('param', VAR)` call across all 25 live Actors'
      `src/main.js`, grepped the same file for that exact VAR reappearing inside a local
      `.includes(`/`.test(`/`RegExp(` call (the shape of c2216's Jobicy finding: same
      variable sent upstream AND re-tested locally). **Exactly one hit in the whole
      fleet: `remote-jobs-scraper`'s `searchKeyword` against Jobicy's `tag=` -- the case
      c2216 already found and fixed.** Checked and ruled out by hand: court-records-scraper
      (`query`/`partyName`/`attorneyName`/`judge`/`docketNumber` -- upstream-only, no local
      re-test), sam-gov-opportunities-scraper (`keyword` -- upstream-only), federal-register-
      scraper (`searchQuery` -- upstream-only via `conditions[term]`), substack-scraper
      (`searchQuery` -- upstream-only), hacker-news-scraper (`query`/`tags` -- Algolia IS the
      search, no local re-test), ats-jobs-scraper (`titleKeyword`/`descriptionKeyword` --
      LOCAL-ONLY, no upstream param exists since ATS APIs are fetched in full and filtered
      client-side, so no AND is possible). uk-find-a-tender-scraper's `stages`/`s` hits on
      `.includes(` are enum validation (`VALID_STAGES.includes(s)`) and the unrelated
      `CF_BLIND_STAGES` warning guard, not a recall-loss AND.
      **No code or README change this cycle** -- this was a verification sweep, not a new
      defect. LEARNINGS cycle 2217 appended with the exact grep pair so a future new fetcher
      can be checked in seconds rather than waiting for fleet rotation. $0 spent (no Actor
      runs needed -- static analysis only), 0 new Actors, no owner email.
      **Next cycle (2218, `2218%3==1` -- NOT a QUALITY slot). No fleet checks due until
      `check-doc-size` at 2220 (2c); no audits until 2417. Fleet-oldest `varied_test` pick is
      `sec-insider-trades-scraper` (2188), then `us-federal-awards-scraper` (2189). DMARC
      recheck still blocked on a report newer than `e2f3a358`.**

- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS warning in `check-upstream-warnings`.**
      Acks currently never expire. An ack written against a correct verification stays silent
      even if, 500 cycles later, we refactor the Actor back onto the dead upstream (unlikely) or
      the rival's warning becomes relevant to a DIFFERENT Actor of ours sharing that upstream.
      Cheap, bounded fix: print `ACK STALE (acked cNNNN, >672c ago -- re-verify)` next to any
      acked hit older than the longest audit interval, without changing the exit code. Only
      worth doing once there are >2 acks or the oldest crosses ~672 cycles (i.e. ~cycle 2868);
      noted now so the decision is deliberate rather than forgotten.

- [ ] **NEW follow-up (c2168) -- watch whether `trademark-search-scraper`'s burst is the first
      real buyer.** It is the only Actor off the baseline and the only one at 3 users. Each
      cycle that runs `bin/usage-trend` should glance at its row. Decision rule, so a future
      cycle doesn't have to re-derive it: external runs are observable but earnings are NOT, so
      the escalation trigger is a **bookmark, a review, or `bin/traffic` buyer intent** (the
      CLAUDE.md Polar gate: >100 visits/day to /pricing or /tools), NOT a run-count climb.
      A run-count climb alone must never trigger an owner email -- c2168 confirmed we cannot
      see earnings, so we could not substantiate a revenue claim even if we wanted to.

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

