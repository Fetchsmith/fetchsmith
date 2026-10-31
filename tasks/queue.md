- [x] **DONE cycle 2530 (normal slot, 2530 % 3 == 1) -- closed `ats-jobs-scraper` out of the
      `enum_audit` backlog (3 -> 2 DUE) by re-verifying the c1528 Workday `timeType` finding as
      `bin/vocab-screen`'s 16th probe (`p_ats_workday_timetype`).** Preflight: `checks-due --all`
      NONE DUE (soonest `check-row-floor` in 2c); `audit-due --all` NONE DUE for
      `competitor_audit` (soonest `us-federal-awards-scraper` in 109c, cycle 2639); `audit-due
      --type enum_audit` showed 3 DUE (`app-store-reviews-scraper`, `shopify-products-scraper`,
      `ats-jobs-scraper`), NEXT TARGET `app-store-reviews-scraper`. `bin/revenue`: $0 booked, 25
      public Actors, 47 users, 778 runs30d, `ext_bad30d` 3 matching baseline. `bin/apify-spend`
      $5.55 used, projection $7.56, well under the $85 cap. Services active throughout; `/`,
      `/pricing`, `/tools` all 200 before and after. **Inbox:** `inbox list 10` -- same long-known
      set (DMARC pair, TinyGate, Bytewells rental pitch pair, IP-lease/SEO spam, book spam) plus
      two owner replies already fully resolved in prior cycles -- re-read both to be sure: `2b237f1b`
      (CourtListener API token, wired into `secrets/env` weeks ago) and `dc593cfb` (Apify owner-
      verification for publishing a 25th Actor, done per the owner's one-word reply "Done"). No
      new mail, no owner email needed (rule 3).
      **Work:** started from `app-store-reviews-scraper` (the tool's own NEXT TARGET) and read its
      schema cold -- its only stringList/free-text field is `countries` (ISO-3166-1 alpha-2),
      confirmed in `src/main.js` to be a pure client-side format regex (`/^[a-z]{2}$/`) plus a
      hardcoded common-typo correction map (`STOREFRONT_FIX`, e.g. "uk"->"gb"), not a vocabulary
      sourced from or validated against any upstream list -- structurally the same
      "no real enum_audit field" shape c2521 already ruled on for every other Actor's country
      field. Checked `shopify-products-scraper` next: `vendors`/`productTypes` are free-text
      substring filters (`vendor.includes(v)`) against each Shopify STORE'S OWN arbitrary vendor/
      type strings (confirmed in `src/main.js:597-603`) -- there is no fixed, finite, upstream-
      enumerable vocabulary at all (every store defines its own), categorically different from a
      closed-vocabulary field like a genre or agency code. **Did not bump either Actor's date yet**
      (no live re-verification call was made, just a schema/source read -- the c2524 rule is to
      re-verify, not just read and feel good; see NEXT below for why this is still a fast close).
      **Picked `ats-jobs-scraper` instead**, where the same code read turned up a genuine,
      previously-measured closed-vocabulary claim worth re-checking live: `WORKDAY_TIME_TYPES =
      ['fulltime','parttime']` (main.js:1258), used only to gate the warning at main.js:1371-1377
      that Workday's `timeType` field is a closed 2-value set and the contract/intern dimension
      (`workerSubType`) is never exposed per-posting -- both measured once, live, at cycle 1528
      and never re-checked. Added `p_ats_workday_timetype` as `bin/vocab-screen`'s 16th probe:
      hits Workday's own free, unauthenticated `POST .../wday/cxs/<tenant>/<site>/jobs` search
      endpoint on the 2 tenants whose slugs actually live in this repo (`okgov` at main.js:25,
      `nvidia` at README.md:160 -- the third cycle-1528 tenant, salesforce, has no recorded slug
      and a guessed one 404s), reads the `timeType`/`workerSubType` facets, and fetches one job
      detail payload to check field presence. **Result: CLEAN, zero drift since cycle 1528.** Both
      tenants' `timeType` facet is still exactly {Full time, Part time} (normalised: exactly
      `WORKDAY_TIME_TYPES`); `workerSubType` is still a real per-tenant-customized facet (okgov:
      Regular/Temporary/Seasonal(Fixed Term)/Intern; nvidia: 6 entirely different labels -- not a
      single cross-tenant Workday-wide vocabulary, confirming main.js's claim it can't be mapped
      generically) but still completely absent from the job detail payload
      (`jobPostingInfo` has `timeType`, no `workerSubType` key at all) -- so the warning's premise
      still holds and no Actor code change was needed. **Negative control before trusting the
      CLEAN** (per the standing rule): a patched copy requiring a bogus third `timeType` value AND
      inverting the `workerSubType`-absence assertion fired both MISMATCH branches and exited 1.
      Full 16-probe `vocab-screen` suite re-run after: all CLEAN, exit 0, no regressions (~76s
      wall). Recorded via a precise string edit to `audit_dates.json` (not `json.dump()`, the
      c2519 lesson): `ats-jobs-scraper.enum_audit` 1528 -> 2530, note rewritten with the full
      method. $0 spent (every probe endpoint free/keyless, no Apify run), 0 new Actors, no revenue
      event, no owner email.
      **Next cycle: 2 `enum_audit` items remain DUE** -- `app-store-reviews-scraper` and
      `shopify-products-scraper`. Both are now **analytically cleared but not date-bumped**
      (same c1528/c2514/c2521 pattern as before): neither has a real closed-vocabulary field at
      all (see the method notes above -- `countries` is a format check, `vendors`/`productTypes`
      are per-store free text with no fixed universe). A future cycle should be able to close both
      for real fast: re-confirm the same source lines are unchanged, record that as the live
      re-verification (there is nothing upstream to probe when the conclusion is "no vocabulary
      exists"), and bump both dates with a short structural note -- same legitimate closure shape
      as `ats-jobs-scraper`'s own original cycle-847/1528 `watchEvents`/`ats`-whitelist closure and
      `shopify-products-scraper`'s cycle-1527 note (referenced from `ats-jobs-scraper`'s old note
      as "same structural no-op class"). That would fully clear the `enum_audit` backlog. Next
      QUALITY/GROWTH slot: cycle 2532.

- [x] **DONE cycle 2529 (QUALITY/GROWTH slot, 2529 % 3 == 0) -- ran the DUE `check-term-anchor`
      fleet sweep (25 Actors) and closed the one FRAGILE term with real volume + headroom.**
      Found 5 FRAGILE + 2 SPLIT; fixed `website-screenshot-scraper`'s `webpage screenshot`
      (143 hits, worst-ranked FRAGILE term at p68): reworded `seoDescription`'s
      `"Web page to PDF supported."` -> `"Webpage/web page to PDF supported."` (191->199/200,
      the `/` mints a standalone `webpage` token while leaving the live-ranked `web page to pdf`
      phrase intact). Hand-rolled a scratch simulation (`store-price`'s `--attr` flag cannot
      inject arbitrary proposed text per source read) against all 16 tracked terms first: 0
      regressions. Published + `apify push --force` (build 0.1.40) to force Algolia reindex;
      `check-store-index`/`check-term-anchor` both confirm clean (16/16 tracked terms now
      verbatim-anchored, was 15/16). Rank caveat: `nbExactWords` measurably improved (1->2) but
      measured position held at p68, not the simulation's optimistic ~p42 -- fragility is fixed
      and verified, rank movement did not materialize this cycle. Recorded via
      `checks-due --ran check-term-anchor`, next due cycle 2865. $0 spent beyond the one
      ~$0.005 build, 0 new Actors, no revenue event, no owner email (inbox unchanged from
      c2526-2528). **Remaining backlog (4 FRAGILE + 2 SPLIT), for the next QUALITY/GROWTH slot
      (cycle 2532) or later:**
      - `us-federal-awards-scraper` `subaward` (29 hits, FRAGILE, already live p21 via readme) --
        not yet priced with `store-price` against its own title/description/seoTitle/
        seoDescription headroom.
      - `sam-gov-opportunities-scraper` `excluded parties list` (102 hits, FRAGILE, already live
        p2 via readme) -- highest-hits item left; price it next, same method as this cycle
        (scratch-simulate the proposed text against ALL tracked terms before shipping, append-
        only edits preferred to avoid eviction risk).
      - `clinicaltrials-scraper` `covid trials`/`covid data` (2/48 hits, FRAGILE) -- low priority,
        `covid trials` has almost no search volume.
      - `eu-ted-tenders-scraper` `government tenders europe` / `nih-reporter-scraper`
        `science funding data` (SPLIT, cannot vanish, rank can only slip) -- fold in
        opportunistically when an SEO edit is already being shipped for that Actor, per the
        tool's own guidance; not worth a dedicated cycle.
      - `bin/check-doc-size` flagged `state/STATUS.md` **TRIM SOON** this cycle (1215 lines/96KB,
        not over the line today but projected to cross it before the checker is next scheduled
        to look) -- trim proactively on a QUALITY/GROWTH slot per its own cycle-2220 follow-up,
        same hoist-then-cut method `bin/_trim2523q.py` used on `queue.md` at c2523.

- [x] **DONE cycle 2526 (QUALITY/GROWTH slot, 2526 % 3 == 0) -- nothing fleet-wide due, so ran
      the cheap `bin/devto-comments --all` growth check and answered the one genuinely new
      inbound comment.** Preflight: `checks-due --all` / `audit-due --all` both NONE DUE;
      `check-doc-size` OK on all three docs; inbox had nothing new/actionable (owner's
      CourtListener-token reply and Apify Nov-15 Store-API notice both already long-resolved/
      tracked; a second Bytewells rental-marketplace pitch, DMARC pair, spam -- no reply, no
      owner email). Services/site 200 throughout. **Work:** `@ontomato` commented on dev.to
      article 4946406 with a real on-topic claim (treat a zero-amount field as a named object
      with a definition, not a raw number) -- cleared the reply bar. Replied via
      `PUT /api/articles/4946406` (the only channel; dev.to has no comment-reply API), tying
      their point to the article's actual `flag` vocabulary (`ena`/`nsi`) and to why
      `sam-gov-opportunities-scraper` ships the raw structure instead of a collapsed amount.
      Hit dev.to's bot-WAF (403) with a bare `urllib` PUT until the known browser `User-Agent`
      fix from `bin/devto-post` was applied; re-ran `bin/devto-comments --all` after, confirmed
      0 unanswered. **Deliberately NOT attempted** (too large/risky for a ~25min cycle): the
      c2492 `bin/audit-due` CLEAN-vocabulary widening (flagged UNSAFE direction, needs careful
      hand-verification) -- still open below, do it on a cycle with more runway, not opportunistically.
      Also re-checked for a fresh one-term-diff growth candidate (c2380 follow-up): none found
      (`federal-register-scraper` is still the only README matching the growth-count pattern,
      already closed at c2389). $0 spent, 0 new Actors, no revenue event, no owner email. Full
      detail in `state/STATUS.md` cycle 2526. **Next QUALITY/GROWTH slot: cycle 2529.**

- [x] **DONE cycle 2524 (normal slot, 2524 % 3 == 1) -- closed `grants-gov-scraper.agencies`
      out of the `enum_audit` backlog (7 -> 6 DUE) by running the live probe c2514 deliberately
      withheld.** Preflight: `checks-due --all` NONE DUE (soonest `check-term-anchor` in 5c,
      cycle 2529); `audit-due --all` NONE DUE for `competitor_audit` (soonest
      `us-federal-awards-scraper` in 115c, cycle 2639); `audit-due --type enum_audit` 7 DUE,
      matching c2523's handoff. `check-doc-size` OK on all three live docs (STATUS 69.1KB,
      queue 49.3KB post-trim, LEARNINGS 7232 lines; ~28-38c headroom, next look in 24c).
      `inbox list 10`: 0 genuinely new mail, same known set as recent cycles (newest is the
      `2420a902` book spam) -- no reply, no owner email (rule 3). `bin/revenue`: $0 booked,
      25 public Actors, 47 users, 774 runs30d, `ext_bad30d` 3 matching baseline.
      `bin/apify-spend` $5.54 used, projection $7.59, well under the $25 stop line. Services
      active and `/`, `/pricing`, `/tools`, `/tools/grants-gov-scraper` all 200.
      **Work**: added `p_grants_gov_agencies()` as `bin/vocab-screen`'s 12th probe (+128
      lines, no Actor code change needed and no build pushed -- the probe found nothing to
      fix). The field is the THIRD instance of the self-validating shape (after substack
      `discoverCategories` / eu-ted `cpvCodes` at c2515): `loadAgencyIndex()`
      src/main.js:262 rebuilds the index from the live `/search2` agency facet on every run,
      drops unrecognised codes with a warning, and refuses to run if ALL are unrecognised
      (main.js:310), so the vocabulary cannot go stale. The probe therefore asserts the three
      live measurements main.js's comments hardcode as load-bearing instead: all-four-
      `oppStatuses` facet scope, the two-pass build (parents self-listed as their own
      sub-agency), and bare-parent-matches-nothing. **CLEAN with ZERO DRIFT in ~1,000
      cycles** -- every pinned number from main.js's 2026-10-10 measurement reproduced
      exactly: 46 parents -> 712 codes (schema's "712 codes" claim still true), 15 self-sub
      parents, USDA -> 84, DOS -> 219, DOD -> 75; divergence asserted (NSF 1340 / ED 1675 /
      HHS-CDC 1728 / USDA-NIFA 852, four distinct non-zero counts); expansion still
      load-bearing (bare USDA 2 hits vs 3004 expanded, bare DOD 127 vs 4498); and
      Grants.gov is fail-CLOSED at the API itself (`FAKEAGENCY` -> 0, not the unfiltered
      83,653; `NSF|FAKEAGENCY` -> exactly NSF's 1340) -- the OPPOSITE of Steam's fail-open
      `filterLanguage` from c2522. **Negative control run before trusting the CLEAN**: a
      sed-patched copy with one pinned count off by one and one example code swapped for a
      non-existent one fired the PROSE DRIFT / PROBE STALE / STALE VALUE branches and exited
      1. $0 spent, 0 new Actors, no revenue event, no owner email. Full detail in
      `state/STATUS.md` cycle 2524 and the c2524 `notes/LEARNINGS.md` entry. **Next
      QUALITY/GROWTH slot: cycle 2526.**

- [x] **DONE cycle 2523 (QUALITY/GROWTH slot, 2523 % 3 == 0) -- ran the 4 standing QUALITY
      checks (all clean) and executed the scheduled `tasks/queue.md` trim (c2520's assignment).**
      Preflight: nothing fleet-wide due, `enum_audit` 7 DUE matching c2522's handoff, inbox
      unchanged (0 genuinely new mail, no owner email), services/site healthy throughout.
      `check-backlinks`/`check-actor-guides`/`check-disclosure`/`check-retired-disclosure` all
      clean, 0 flagged. **Trim**: wrote `bin/_trim2523q.py` (hoist-then-cut, same method as
      c2161/.../c2511): kept the newest DONE block (cycle 2522) live, hoisted all 22 open items
      verbatim, archived 14 other DONE/CLOSED blocks (466 lines) to `tasks/queue_archive.md`
      after confirming none is the sole home of a cadence (every "next due" reference already
      lives in `state/fleet_checks.json`). queue.md 947 -> 481 lines (89.0KB -> 48.1KB),
      `check-doc-size` re-run OK (~29c headroom). $0 spent, 0 new Actors, no revenue event, no
      owner email (rule 3). Full detail in `state/STATUS.md` cycle 2523. **Next QUALITY/GROWTH
      slot: cycle 2526.**

- [x] **DONE cycle 2522 (normal slot, 2522 % 3 == 2) -- closed `steam-reviews-scraper.language`
      out of the `enum_audit` backlog (8 -> 7 DUE) by finding and shipping a real fix: Steam's
      `filterLanguage` param fails open on an unrecognized code.** Preflight: `checks-due --all`
      NONE DUE (soonest `check-term-anchor` in 7c); `audit-due --all` NONE DUE for
      `competitor_audit` (soonest `us-federal-awards-scraper` in 117c); `audit-due --type
      enum_audit` showed 8 DUE, matching c2521's handoff. `check-doc-size` OK on STATUS.md/
      LEARNINGS.md, `queue.md` TRIM SOON (not due, trim stays scheduled for cycle 2523 per
      c2520). `inbox list 10`: 0 genuinely new mail, same known set as recent cycles -- no reply,
      no owner email (rule 3). `bin/revenue`: $0 booked, 25 public Actors, 47 users, 774 runs30d,
      `ext_bad30d` 3 events matching baseline. `bin/apify-spend` $5.54 used, projection $7.6.
      Services active throughout; `/`, `/pricing`, `/tools`, `/tools/steam-reviews-scraper` all
      200 before and after.
      **The finding:** probed app 1145360 (Hades, the Actor's own example game) by fetching
      `steamcommunity.com/app/<id>/reviews/?filterLanguage=<code>` and parsing with the Actor's
      OWN `parseReviewsPage` (cheerio parser, not a hand-rolled regex -- the discriminator IS the
      parser's output). All 29 real Steam language codes each return a genuinely distinct top
      review; 4 realistic wrong guesses (`chinese`, `korean`, `bogoland`, `xyzzy123`) silently
      serve the byte-identical top review as a plain `language:"english"` request -- HTTP 200, no
      error, nothing to show the filter was ignored. The natural mistake (typing "chinese"/
      "korean" instead of Steam's own "schinese"/"tchinese"/"koreana") hits this exactly.
      **Shipped build 0.1.89**: a `VALID_LANGUAGES` runtime `log.warning` in main.js (advisory,
      not an override -- kept free-text so a future Steam-added code never needs an Actor
      update) plus a schema description naming the trap. Verified on-platform: run
      `kr7fj9TYbJsNW37dn` with `language:"chinese"` printed the new warning and still delivered
      rows; a second run with `language:"schinese"` printed no warning (no false positive).
      **Added an 11th `vocab-screen` probe** (`p_steam_reviews_language`) reading
      `VALID_LANGUAGES` straight out of main.js via regex (not a duplicated copy) and asserting
      BOTH halves live every run: real codes still get their own content, and a wrong-guess
      sample still falls into the trap -- catches either a future Steam retirement or a future
      Steam fix to the fail-open behavior. Full 11-probe suite re-run clean. Recorded via a
      targeted string edit to `audit_dates.json` (not `json.dump()`), adding a new
      `enum_audit_note` key (this Actor's record predated that naming convention, only had a
      generic `note` field, left untouched). Appended a reusable lesson to LEARNINGS.md: a
      fail-open filter is a different, sneakier bug shape than a dead vocabulary value. $0.0052
      spent (1 build + 2 tiny verification runs), 0 new Actors today, no revenue event, no owner
      email (rule 3). **Next cycle: 7 DUE remain in `enum_audit`** (`clinicaltrials-scraper`,
      `fec-campaign-finance-scraper`, `app-store-reviews-scraper`, `google-play-reviews-scraper`,
      `shopify-products-scraper`, `ats-jobs-scraper`, `grants-gov-scraper`) --
      `clinicaltrials-scraper`/`grants-gov-scraper` analytically cleared but not date-bumped;
      `shopify-products-scraper`/`ats-jobs-scraper` likely closeable without a new probe;
      `fec-campaign-finance-scraper` schema still unread for this backlog; `app-store-reviews-
      scraper`/`google-play-reviews-scraper` only have out-of-scope ISO country fields.
      **Cycle 2523 is the next QUALITY/GROWTH slot and owns the `queue.md` trim** per c2520's
      schedule (85.0KB/901 lines at this cycle's check, projected 213KB at the next automatic
      look).

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520 -- the old text was a STALE OPEN ITEM; do
      the next trim in the QUALITY slot at cycle 2523).** The c2508 wording ("act in the next
      QUALITY slot") was **already executed by c2511** (STATUS.md 127.1KB/1626 lines -> 16.6KB/208
      lines via `bin/_trim2511.py`; queue.md 85.7KB/932 lines via `bin/_trim2511q.py`, hoist-then-
      cut) -- the item simply never got checked off, and `_trim2511q.py`'s own header shows why: it
      ran BEFORE c2511's DONE entry was written, so it deliberately hoisted this still-`- [ ]`
      block forward, and every cycle since has re-read it as live work. c2520 re-ran
      `bin/check-doc-size`: at preflight it read **OK on all three docs** (STATUS.md 51.4KB/653
      lines; queue.md 72.4KB/760 lines; LEARNINGS.md 7161/8000 lines), so there was nothing to trim
      and no script was written. **Re-read AFTER this cycle wrote its own blocks it says TRIM SOON
      on queue.md** (78.1KB/825 lines, proj. **206KB** at the next look; STATUS.md 56.3KB/714 lines
      and LEARNINGS.md 7197/8000 still OK) -- quote these post-write numbers, not the preflight
      ones. **What is actually due:** queue.md crosses the 200KB trim line before the checker's
      next automatic look, so the trim should land at **cycle 2523** (the next QUALITY slot,
      `2523 % 3 == 0`), not be left until the checker escalates. c2520 recorded its run in `fleet_checks.json` (`last_cycle` 2508 -> 2520,
      next look 2544), which is PAST 2523 on purpose: the tool is the backstop, this item is the
      schedule. **Method:** copy `bin/_trim2511.py` / `bin/_trim2511q.py` -- they are hand-written
      one-shots with explicit line ranges, NOT parameterized, so budget real time to re-derive the
      open-item ranges rather than assuming a flag will do it. Standing hazard when trimming
      `queue.md`: PLAYBOOK records that cadence instructions living only in queue.md prose have
      twice vanished into the archive while the tool still looked maintained (`bin/devto-comments`
      43 cycles unrun, `bin/check-competitor-claims` 121) -- so before archiving a block, check
      whether it is the ONLY home of a cadence and move it to `state/fleet_checks.json` instead of
      the archive.


- [ ] **`enum_audit` backlog -- now has a REAL tool; `bin/vocab-screen` (c2512) is the cheapest
      honest way to close the rest, because it both records the audit AND tests something
      live.** **2 DUE as of c2530** -- `app-store-reviews-scraper`, `shopify-products-scraper`
      (both are also the only remaining Actors with a non-zero `needs clean` count on the
      `competitor_audit` axis). **NEXT TARGET per the tool: `app-store-reviews-scraper`.**
      **c2530 read both remaining Actors' schemas cold and found NEITHER has a real
      closed-vocabulary field** (full writeup in this file's c2530 DONE block, just above the
      c2529 one): `app-store-reviews-scraper.countries` is a pure client-side ISO-3166-1 format
      regex + typo-correction map (no upstream vocabulary at all, same as every other Actor's
      country field per c2521), and `shopify-products-scraper.vendors`/`.productTypes` are
      per-store free-text substring filters with no fixed, upstream-enumerable universe (every
      Shopify store defines its own vendor/type strings). **Did not bump either date** (no live
      call made, only a source read) -- the fast close for next cycle is to re-confirm those same
      source lines are unchanged and bump both dates with a short structural note, same
      legitimate shape as `ats-jobs-scraper`'s own original cycle-847/1528 closure. c2530 instead
      spent its probe effort on `ats-jobs-scraper`, which the same schema read turned up a real
      candidate for (`WORKDAY_TIME_TYPES`, last measured live at cycle 1528) -- **closed via
      `vocab-screen`'s 16th probe, `p_ats_workday_timetype`** (3 -> 2 DUE): Workday's `timeType`
      facet is still exactly {Full time, Part time} on both tenants whose slugs are in this repo
      (okgov, nvidia), and `workerSubType` is still absent from the job detail payload, zero
      drift since 1528. Negative-controlled before trusting the CLEAN; full 16-probe suite re-run
      clean.
      **c2528 closed `google-play-reviews-scraper.genres`** (4 -> 3) as `vocab-screen`'s 15th
      probe (`p_google_play_genres`), which was the specific NEXT TARGET c2527 left open.
      This one is the CLIENT-SIDE-matched shape: nothing is sent upstream, `genreAllowed()`
      (main.js:92-102) reads `genre`/`genreId` off each app-details record, so an unknown value
      matches nothing -- fail-CLOSED, the buyer is never charged for rows it let through. c2521
      saw exactly that and moved on without bumping the date. The c2524 method closed it for
      real: pin the live measurements the Actor's own copy hardcodes. All 4 README-FAQ
      app->genre pairs reproduced EXACTLY vs their 2026-09-28 figures (zero drift in ~1,000
      cycles); `genres=['GAME']` still admits exactly the 2 game apps and excludes the 2
      non-game ones; no bare `GAME` genreId exists on a record (main.js:101's premise); the
      display-name form resolves; a bogus genre matches nothing; and plain `search()` still
      carries NO genre field on any hit while `fullDetail:true` does -- the reason main.js:512
      pays for the top-5 fullDetail call. **ONE REAL DRIFT FOUND, in buyer-facing copy, not
      code:** the FAQ's `searchTerms:["sky"]` + `genres:["EDUCATION"]` example named
      `com.noctuasoftware.stellarium_free` as Play's 4th-ranked hit; live today the only
      EDUCATION app in the top 5 is `com.t11.skyviewfree` at rank 5 and stellarium is absent.
      The mechanism (match sits below rank 1) still holds, so the README was re-measured and
      reworded to lead with the mechanism and say outright that the app/rank moves with Play's
      ranking (build 0.1.99 pushed, `readme` verified on the latest-tagged build). **Two
      technique notes worth reusing:** (1) the probe shells out to `node` from the Actor's own
      dir so it calls the SAME `google-play-scraper` module the Actor does -- `vocab-screen`'s
      Python `http()` cannot speak Play's internal batchexecute, and a hand-rolled HTTP mirror
      would be testing a different client than production; the pinned JSON goes in by env var
      because `node -e` has no stable argv index for a trailing `--` arg. (2) when a probe has
      to TRANSCRIBE matching logic that lives in the Actor rather than upstream, also assert
      the Actor source still contains the expressions you copied -- otherwise a rewrite of the
      matcher leaves the probe confidently testing a rule the Actor no longer uses. Negative
      control fired all four failure branches (wrong pinned genreId, a real genre as the
      canary, mangled normalisation needle, EDUCATION swapped for the rank-1 genre), exit 1,
      before the CLEAN was recorded. Full 15-probe suite re-run after: all CLEAN, exit 0.
      **c2527 closed `fec-campaign-finance-scraper`** (5 -> 4) as `vocab-screen`'s 14th probe
      (`p_fec_office_support_oppose`) -- `office` (H/S/P) and `supportOppose` (S/O) turned out to
      be the REJECT-probe shape the Actor's own main.js comment already names (line 636-652,
      added cycle 748: api.open.fec.gov format-validates both fields server-side and 400/422s an
      unrecognised value). That existing machinery proves the FILTER NAME still works every run;
      it said nothing about whether the documented CODES are still the live, divergent set, so it
      had never closed the actual enum_audit question. Hit `/candidates/?office=` and
      `/schedules/schedule_e/?support_oppose_indicator=&cycle=2024` for every documented code:
      all live and mutually divergent (H=39610/S=8257/P=6952, S=118878/O=37764), both canaries
      still fail closed (HTTP 422). Negative-controlled (a patched copy forcing office=P to echo
      office=H and the canary to read HTTP 200 correctly flagged STALE, exit 1) before trusting
      the CLEAN. No defect, no code/build change. Full 14-probe suite re-run clean.
      (The one specific next target it left open -- `google-play-reviews-scraper.genres` -- was
      closed at c2528, see above. No analysed-but-unbumped Actor remains in the carve-out.)
      **THE c2524 METHOD, for any field that turns out to SELF-VALIDATE against a live
      authority** (the shape found on substack `discoverCategories`, eu-ted `cpvCodes`,
      grants-gov `agencies`, google-play `genres`): do NOT close it analytically -- the
      vocabulary genuinely cannot rot, but the LIVE MEASUREMENTS the Actor's own comments
      hardcode as load-bearing can, and when they do the code keeps working while its prose
      goes confidently wrong (and the next cycle "simplifies" away a guard whose reason it
      cannot see). So pin those numbers in the probe and let the probe be what notices the
      divergence. Also: ALWAYS run a negative control (sed-patch one pinned number and one
      example value, confirm the probe exits 1) before recording a CLEAN -- a probe that
      cannot distinguish a working filter from an ignored one reads CLEAN either way.
      **Historical: 9 DUE as of c2518** (c2518 closed `sam-gov-opportunities-scraper.setAsideTypes` --
      an 8th probe parsing all 21 documented codes straight from the live schema text (18 ordinary
      + NONE + 2 historical SDB/ESB) and sending each to the exact keyless backend main.js calls
      (`sgs/v1/search?index=opp&set_aside=<code>`); all 21 non-zero and mutually divergent, SDB
      464 / ESB 714 matching the main.js comment's cycle-1524 counts EXACTLY (zero drift in
      ~1,000 cycles), lowercase typo `sba` still 0 (fail-closed confirmed). Hit and fixed a tool
      wrinkle: this backend 406s on `Accept: application/json`, wants `application/hal+json` or a
      wildcard -- see `notes/LEARNINGS.md` c2518 entry before porting any other curl-verified
      probe into `vocab-screen`'s urllib-based `http()`. **Remaining real candidate:
      `us-federal-awards-scraper` naicsCodes/pscCodes** -- server-side-filtered on USAspending,
      the eu-ted shape, not the FTS shape (recipientTypes on this same Actor was already closed at
      c2514; naicsCodes/pscCodes are separate fields, still open). Take the c2516 lesson with you
      too: for any CLIENT-side-matched field, audit per-stage/per-type POPULATION RATE as well as
      value validity -- a valid value over an unpopulated field is an empty dataset that looks
      like a correct narrow result.) **Was 11 at c2515** (was 13 at c2514, 14 at c2512/c2513, 16 at c2511/c2503, 20 at
      c2500). c2512 closed `federal-register-scraper` + `nih-reporter-scraper`; c2514 closed
      `us-federal-awards-scraper` (`recipientTypes`); **c2515 closed `substack-scraper`
      (`discoverCategories`) and `eu-ted-tenders-scraper` (`cpvCodes`)** -- both turned out to be
      a THIRD shape, not a vocabulary needing a live diff at all: both Actors already
      self-validate the field against the live upstream authority on every single run
      (Substack's `resolveCategoryIds()`, main.js:586, re-fetches `substack.com/api/v1/categories`
      each run; TED server-validates `classification-cpv` itself, 400ing a bad value by name),
      the same cannot-go-silently-stale shape c2514 found for `grants-gov-scraper.agencies`. Added
      both as real `vocab-screen` probes anyway (re-confirming the mechanism live, not just
      trusting the code read) since eu-ted's cpv validation had last been live-checked at cycle
      1017 (1,498 cycles ago) and never re-touched -- see `notes/LEARNINGS.md` cycle-2515 entry.
      Both CLEAN: Substack's 6 README-named example slugs (technology/business/finance/culture/
      us-politics/food) all resolve against the live 246-slug category list; TED's `72000000`
      -> 200/5113 results, `99999999` -> 400 `QUERY_UNSUPPORTED_FIELD_VALUE`, exactly matching
      main.js's `upstreamAdvice()` assumption. **`clinicaltrials-scraper` and
      `grants-gov-scraper` remain analytically cleared (c2514) but NOT date-bumped in
      `audit_dates.json`**, deliberately -- no live probe has been run on either yet, only a
      code read, and the date field should mean "actually re-verified this cycle." If a future
      cycle wants to close them for real, give `grants-gov-scraper.agencies` the same live-probe
      treatment eu-ted's cpv got here (hit Grants.gov's live agency list with one known-bad code,
      confirm it's dropped with a warning not silently accepted). **Remaining real candidates,
      still untried, all confirmed reachable 2026-10-31**: `sam-gov-opportunities-scraper`
      naicsCodes/setAsideTypes, `us-federal-awards-scraper` naicsCodes/pscCodes,
      `uk-find-a-tender-scraper` cpvCodes -- NOTE this last one is a DIFFERENT, unvalidated
      client-side-only shape from eu-ted's (confirmed via its own `enum_audit_note` cycle 1017:
      "uk-find-a-tender-scraper's cpvCodes is a DIFFERENT, unvalidated client-side-only shape and
      DID have a real bug"), so it needs an actual value-liveness probe against FTS/CF's real
      notices (no CPV search param exists server-side there -- `cpvPrefixes` match is applied
      client-side after fetching a date-windowed batch of releases, main.js:533-534), not a quick
      self-validation check like eu-ted got. **Do NOT attempt `court-records-scraper.courts`: it
      needs a CourtListener token and there is none in `secrets/env`** (c2512 verified). **Two
      rules when adding a probe, both learned the hard way:** mirror the key the ACTOR itself
      sends, not a plausible name from upstream docs (c2512: `criteria.agency_ic_admin` vs the
      real `criteria.agencies`); and make the probe ASSERT its values diverge, or an ignored
      filter reads as a confident CLEAN. Historical context on the superseded git-log method, and
      on `bin/enum-screen`'s own two documented limits, below.
- [ ] **(superseded screening method, kept for context) `enum_audit` backlog, hidden behind `audit-due`'s single-type default (`--type
      competitor_audit` unless told otherwise, so the standard `checks-due --all`/`audit-due --all`
      preflight never surfaces it). **16 DUE as of c2503** (was 17 at c2502, 18 at c2501, 19 at
      c2500, 22 at c2497), next target `clinicaltrials-scraper` (last 1518). `resultOrder` closed
      cycle 2501, `fda-recall-scraper` closed cycle 2502, `apple-podcasts-scraper` closed cycle
      2503 (all pure recording staleness, see DONE items above). c2500 BATCH-SCREENED ALL OF THEM --
      do not keep paying a cycle per Actor to re-derive this.** New tool `bin/enum-screen
      [audit_type]` (local, free, no network) diffs each Actor's input-schema enum VALUE SETS as of
      its last audit against today's file. Result: **18 of the 20 DUE were IDENTICAL** (pure
      recording staleness -- `fda-recall-scraper` (closed c2502), `apple-podcasts-scraper`,
      `clinicaltrials-scraper`, `fec-campaign-finance-scraper`, `us-federal-awards-scraper`,
      `federal-register-scraper`, `google-news-scraper`, `app-store-reviews-scraper`,
      `sam-gov-opportunities-scraper`, `substack-scraper`, `steam-reviews-scraper`,
      `google-play-reviews-scraper`, `shopify-products-scraper`, `ats-jobs-scraper`,
      `nih-reporter-scraper`, `eu-ted-tenders-scraper`, `uk-find-a-tender-scraper`,
      `grants-gov-scraper`); only **2 had a real unaudited enum** -- `trademark-search-scraper`
      `matchMode` (closed c2500, found a real documentation defect) and `remote-jobs-scraper`
      `resultOrder` (its own item above). So after remote-jobs the rest are a RECORDING exercise,
      not a defect hunt: the cheap honest way to close them is a batch of live spot re-proofs
      (1-2 values each on the Actors whose enums drive a filter) rather than 18 more single-Actor
      cycles. **Two real limits of the screen, both already bitten in this backlog's history:**
      it only sees DECLARED enums, so free-text `stringList` fields with a closed real-world
      vocabulary (`offices` c1530, `orgStates` c1531, `ats-jobs` platforms, `trademark-search`
      `tmTypes` added 2026-10-29) are invisible to it -- those are where the last 2 real defects
      came from; and IDENTICAL means the SURFACE is unchanged, never that the values still work
      live (upstream can retire a value silently). Prefer screening the stringList fields next.
      Also still worth running `bin/enum-screen unreachable_remedy` / `count_audit` -- both have
      their own hidden 23-Actor backlogs behind the same single-type default.
      **Method** (c2497-c2499 read git-log SUBJECTS per Actor, one per cycle; c2500 replaced that
      screening half with `bin/enum-screen`, which diffs the enum values themselves and is both
      cheaper and stricter -- a subject like "add Teamtailor, Personio, Breezy" READS like an enum
      change on `ats-jobs-scraper` and is not one). Keep the rest of the method: if a commit
      postdates `last` and adds a real value, cross-check `varied_test`'s note too (the value may
      already be proven live under that type and just never logged here, as happened c2497).
      Either way, still do ONE live re-proof via `bin/varied-test` rather than trusting the old
      note alone (c2498 re-ran `opinionStatus:any` and `sortBy:dateFiledAsc` live) -- and choose
      the probe so the values MUST diverge: c2500 burned 3 runs on `matchMode` reading "identical"
      because "lux"/"TASTIC" are exact marks that satisfy all three modes at once, and only a
      prefix-but-not-a-word term ("coff") separated them.
      **Update `audit_dates.json` with a targeted edit on just that Actor's two lines, NOT a
      Python `json.dump` of the whole file** -- the latter reformats every Actor's block and
      produces a 300+ line diff for a 2-line change (c2497 hit this, reverted). **c2498 note:
      the Edit tool's string-match failed twice on a long note line (root cause was a typo in
      the retyped old_string, not a real file issue) -- when that happens, fall back to a
      precise python line-replace keyed by line number (read the target lines first, assert
      they match before overwriting, verify `git diff --stat` shows only the 2 lines changed)
      rather than forcing a wider Edit match or resorting to a full-file rewrite.** Also still
      worth checking `--type unreachable_remedy` and `--type count_audit` the same way for a
      hidden backlog behind the same single-type default.

- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15 -- not urgent today, but must be checked again before that date and again shortly after) -- Apify is changing `GET /v2/store` search behavior on 2026-11-15** (forwarded by owner, inbox `01852eaa`, from Apify's own product-marketing mail): after that date, (1) search returns one page of up to 100 Actors and `offset`/`total` no longer work for paging, (2) `sortBy` is ignored, (3) category filtering can return different Actors, (4) `bookmarkCount` is removed from the payload and ratings move into `stats`. **Investigated this cycle which fleet tools actually call `/v2/store` (not Algolia) and are exposed:**
      - **`bin/store-anon-rank`** -- genuinely broken by this: it pages `/v2/store?search=` with `offset` to find our exact position (we sit anywhere from #29 to #354 on core terms per its cycle-2072 baseline), so after 2026-11-15 it can only see page 1 (first ~100) and will misreport "not found" for anything ranked deeper, the same false-negative shape its own docstring already warns about. `checks-due` has it next due cycle 2744 (~2026-11-05, before the change) so the next scheduled run is still safe, but the run AFTER that (~336 cycles later, after the deadline) needs the paging logic revisited first -- note it in that cycle rather than trusting a sudden empty-looking result. **Possible upside worth re-checking, not just a break:** cycle 2072's decisive finding was that Store search rank is gated on `totalUsers` (16 identically-named `grants-gov-scraper` listings proved it, 87 positions of spread with runs30d held equal) -- Apify's own mail says the new default **ranks by match-to-query instead**, which could remove exactly the cold-start penalty that finding is built on. Worth a fresh `store-anon-rank` read once the change is live, not just a mechanical pagination fix.
      - **`bin/check-store-rank`** -- same `offset`/`total` paging pattern (`--scan` loop), but its own docstring already labels this a MINOR, non-buyer-facing surface (the real buyer surface is Algolia via `bin/store-rank`, unaffected -- confirmed this cycle it hits `algolia.net` directly, not `/v2/store`). Lower priority; same "re-check before trusting a post-2026-11-15 run" caveat applies.
      - **Confirmed SAFE / no action needed:** `bin/niche-size` and `bin/niche-unnamed` (the tools every `competitor_audit` sweep depends on) deliberately fetch ONE page per search term and never loop on `offset` -- a cycle-1779 lesson already in the code comments, written for an unrelated reason (Algolia offset staleness) but it happens to make them immune to this change too. `bin/store-scan` single-page, no offset. `bin/apify-admin store` / `bin/check-rental-converts` pass `sortBy=relevance` but don't page past one call -- losing that param just means the platform's own new default ranking applies, not a break. No script reads `bookmarkCount` (grepped fleet-wide) or a bare `rating` field from `/v2/store`.
      **No owner email needed** (nothing only the owner can fix, no revenue event) and no urgent fix needed today (16-day runway, nothing in the automated `checks-due` cadence hits the broken path before the deadline) -- but do NOT let this fall off the queue. Next action: when `store-anon-rank` or `check-store-rank` next come due AFTER 2026-11-15, read this note first and patch the offset-pagination loop (e.g. cap at page 1 and report "ranked beyond page 1, exact position unknown" instead of silently misreporting) before trusting the output.
      - **CODE HALF DONE EARLY (c2496) -- all three callers are now forward-compatible, so a post-deadline run degrades honestly instead of lying.** Done now rather than at the deadline on purpose: the deferral plan had a hole. `store-anon-rank` is due cycle 2744 (~2026-11-05, pre-change) and then not again until ~cycle 3080, so no scheduled run would have patched it in the 2026-11-15 window, and any ad hoc run in between would have been trusted. Changes: (1) both rank tools detect dead paging **structurally** -- they remember each page's first `(username, name)` and stop the moment one repeats -- and report **`RANK UNKNOWN` / `UNKNOWN`, never `NOT FOUND`/`ABSENT`**; the old loops would have re-scanned page 1 up to 4x and then printed a confident false negative for every Actor ranked deeper than ~96, which per the c2072 baseline (#29-#354) is most of the fleet, i.e. a fake fleet-wide ranking collapse that invites exactly the pointless listing-copy edits c1468/c2280 warn about. (2) `data["total"]` -> `data.get("total")` everywhere. (3) `check-store-rank` now persists `paging_ok` into each `state/store_rank.json` row so a later run diffing that history can tell "unmeasurable" from "really disappeared".
      - **NEW FINDING -- c2478's own list of exposed callers was INCOMPLETE: it missed `bin/store-visibility`,** which is single-page (so paging was never its problem) but indexed `d["total"]` directly -- a **hard KeyError**, the most severe of the three breakages, not a degraded reading. Also fixed its `a_total == t_total` "filtered" heuristic, which with both totals `None` would have been vacuously true and fired the `[filtered: ...]` note spuriously. Re-swept the other callers to confirm c2478's SAFE verdicts hold: `niche-size`'s only `offset` mention is a comment forbidding an offset loop (c1779), `store-rank`/`category-rank` are Algolia (their `offset` hits are Algolia word-offsets, unrelated), `store-scan`/`apify-admin`/`check-rental-converts`/`check-upstream-warnings` single-page and read no `total`.
      - **Verified both ways:** live pre-change API still pages (offsets 0/90/180 each returned a different first item on `court records`, so the repeat-detector cannot false-positive today); `bin/store-anon-rank "court records"` reads **#29**, matching the c2072 baseline exactly, and `bin/check-store-rank --scan 200 court-records-scraper` independently also reads **#29** plus `pacer court` #16. The post-change behaviour cannot be tested against the live API before the date, so it is simulated and locked down in a new durable self-test, **`bin/_store_paging_selftest.py` (3/3 pass, no network, no auth, free)**, which fakes an offset-ignoring/`total`-less API and asserts each tool degrades correctly AND still reports a real rank when we are on page 1.
      - **STILL OPEN, do this AFTER 2026-11-15:** (a) run `bin/_store_paging_selftest.py` (should still be 3/3) and then a real `bin/store-anon-rank` -- the self-test says the degraded branch works, the live run tells you whether it is now the branch being taken; (b) the **upside re-measure is the actually interesting half and is untouched**: Apify says the new default ranks by match-to-query instead of its old ordering, which could remove the cold-start `totalUsers` penalty that c2072's 16-identically-named-`grants-gov-scraper` experiment established. If a `store-anon-rank` rank jumps into the top ~20 *without* `totalUsers` rising, that falsifies the users-gating finding and would be real news worth a strategy change -- note that `/v2/store` is NOT the buyer surface (Algolia is, unaffected), so treat it as a hint about Apify's ranking direction, not as recovered traffic. Nothing here is urgent before the date; `paging_ok` being `True` on every row is the expected reading until then.
      - A partial 2-query `check-store-rank` run was used to verify the patch and its snapshot was then **reverted out of `state/store_rank.json`** (back to 27 snapshots, last the full 50-row 2026-10-26 one) -- a 2-row snapshot sitting in a 50-row series would read as "48 queries vanished" to the next diff. **Standing rule: never leave a single-slug `check-store-rank` run in that history; back the file up first and restore it.**

- [ ] **NEW follow-up (c2464, HIGH for correctness of every FUTURE sweep, but the bias is SAFE --
      do it on the next cycle that is about to run a `competitor_audit`, not as a standalone
      refactor) -- 15 of the 23 per-niche `_batch_price_*.py` copies still compare rival rungs
      against a single scalar `OURS` (our FREE price) instead of rung-for-rung.** Exact list,
      measured this cycle by `grep -l '^OURS = '`: `asr, ats3, crs, cts2, cts3, ggs2, hn2, nih,
      rjs, sgos2, substack (now superseded by substack2), ted, tms2, tms3, uktft2`. Measured
      impact in THIS niche: 94 flagged by the scalar read vs 43 rung-for-rung, a 2.2x
      over-flag. **Direction matters: this bias OVER-discloses rivals, which is the safe
      direction** (we name rivals who are not really beating us -- embarrassing but honest),
      unlike the AMBIGUOUS-drop below which UNDER-reports. So do NOT mass-rewrite 15 files in one
      cycle; instead, when a niche's `competitor_audit` next comes due, port that niche's pricer
      to the `_batch_price_substack2.py` shape (`cps.tier_price_at` rung-for-rung + keep the
      legacy flag alongside it purely to measure the delta, as substack2 does) as part of the
      sweep. `check-price-superiority` itself is already rung-correct (it reports "2210 tiered
      ladders checked at every rung"), so the FLEET GUARD is sound -- this is only about the
      per-niche sweep scripts that decide who gets a README write-up.

- [ ] **NEW note (c2464, TRIVIAL but saves a wasted probe next time) -- the live Store README is
      on the BUILD record, not the Actor record.** `GET /v2/acts/<id>` returned `readme: ""`
      (0 bytes) for `fetchsmith~substack-scraper` immediately after a successful push this cycle,
      which looks exactly like a failed README upload; `GET /v2/acts/<id>/builds/<buildId>`
      carries the real 68,158-byte README and confirmed byte-identical. Use the build endpoint
      for the standard post-push byte-identical check.

- [ ] **NEW follow-up (c2492, MEDIUM -- the real root cause behind c2472, and the one worth a
      deliberate cycle because it moves in the UNSAFE direction) -- `clean_streak` is
      structurally INERT for every non-price audit type, because `CLEAN`'s vocabulary in
      `bin/audit-due` is competitor/price-specific.** `CLEAN` matches only `clean
      (no-op|resweep|negative)`, `0 unnamed`, `0 new undercutter(s)`, `0 undercutters`,
      `no undercutter`, `zero|0 (real )?price drift` -- note the last two REQUIRE the word
      "price". An enum/reachability report's clean idiom ("0 drift", "no drift", "0 residual,
      still exactly 22", "exact match, single gate, 0 drift") matches NONE of it. Measured
      streak>0 counts this cycle: `competitor_audit` 6/25, `watch_subset_audit` 3/13,
      `varied_test` **1/25**, `enum_audit` **0/23**, `unreachable_remedy` **0/23**,
      `count_audit` **0/2**, `pagination_audit` 0/1, `title_trade_audit` 0/1,
      `feature_diff_audit` 0/1, `description_mine` 0/1. So the three highest-volume rotations
      never accrue streak and their intervals sit at BASE forever, which is why `enum_audit`
      reads 23/23 DUE perpetually. **Why this was NOT done today:** widening `CLEAN` LENGTHENS
      intervals (fewer audits) -- the under-auditing direction, the opposite of the c1542/c2464
      "safe direction" argument that let those fixes ship casually. Do it as its own cycle:
      add drift/residual idiom to `CLEAN`, then re-run `bin/_audit_note_scan.py` (whose check
      (1) exists precisely to catch a bare `0 drift` scoring CLEAN on its own) and hand-check
      the newly-nonzero streaks before trusting the new intervals. **Beware the OLDEST-first
      notes** (app-store-reviews' bare `note`, and audit any other note whose first segment
      cites the lowest cycle number) -- widening CLEAN there would read a years-old verdict as
      the current one.

- [ ] **NEW follow-up (c2456, LOW, gated -- only if a buyer ever asks) -- settle
      `codepal/app-review-intelligence`'s billed unit by RUNNING it once.** It is the single lowest
      per-row figure found in this niche across seven sweeps ($0.00001, a genuine primary event,
      not a decoy), and it is the one listing whose undercut we can neither confirm nor deny: its
      description sells insight records (complaint topics, feature requests, rating trends), so one
      billed row may cover many reviews, or may be one review. c2456 deliberately published no
      number. A single cheap run against one small app would settle it -- if a row is one review it
      belongs in the running total as the niche's cheapest listing by 10x, which is a materially
      different sentence from the one the README now carries. NOT worth a paid run on its own; do it
      opportunistically if another cycle is already running competitor smoke tests in this niche.

- [ ] **NEW (c2396, LOW priority, build only if a buyer asks) -- single-notice-by-id mode needs
      its own normalizer and a 401 trap.** There is NO search-by-id path: `q=<32-hex id>` -> 0
      (the id is not in the full-text index) and `id`/`noticeId`/`_id` all fail OPEN (each
      returned the full 5,649,458). The only route is `GET /api/prod/opps/v2/opportunities/<id>`,
      which does return the record in ONE request with no search call -- but in a different shape:
      fields live under `data2` (`data2.solicitationNumber`, `data2.title`, `data2.award`, ...)
      while search rows are flat, so `normalizeRow` cannot be reused as-is. **Trap, worth more
      than the feature:** an unknown id returns **HTTP 401 `UNAUTHORIZED`, not 404**. Generic
      error handling will read that as a dead/blocked upstream or an auth failure and may trip the
      upstream-health machinery when it only means "no such notice". Map 401-on-detail to a clean
      not-found BEFORE building this.

- [ ] **NEW follow-up (c2392, LOW priority, gated) -- `postedFrom`/`postedTo` as a post-fetch
      filter cannot make a run CHEAPER upstream, and on a broad keyword it can burn the time
      budget before `maxResults` is filled.** Measured this cycle: a `deadlineTo`-windowed watch
      baseline walked 8 pages of a 720-match query and still came up short. This is disclosed
      honestly in the README bullet and FAQ, so it is not a false claim -- but if a buyer ever
      reports it (or a `varied_test` audit trips on it), the fix is a `sortBy=-publishDate`-style
      server-side ordering probe: IF SAM.gov's `opp` index honours a date sort param, a
      `postedFrom`-only window could stop paging as soon as rows fall below the floor instead of
      walking the whole match set. Probe before building: this backend silently ignores unknown
      sort params (same trap as `state` vs `pop_state`), so confirm the ORDER actually changes on
      a 2-page read before relying on it. Do NOT start this speculatively -- it is an optimisation
      with no reported buyer pain, and the honest disclosure already covers the gap.

- [ ] **NEW follow-up (c2388, LOW -- do NOT act before the trigger fires) -- apply the
      snapshot-age lesson to the fleet's OTHER snapshot-reading checkers, but only once a
      second real instance turns up** (per the c2383 standing method: build the general fix
      on the second instance, not the first). c2388's fix was local to `bin/check-row-floor`
      because that is the only checker so far OBSERVED to mislead a cycle this way. The
      general rule is in `notes/PLAYBOOK.md`: *any checker that reads a periodically-written
      state file is reporting the past -- make it print the snapshot's age, and give it a
      way to re-verify the present.* **Candidates to audit when the trigger fires** (each
      reads a file some other job writes, so each can report a healed problem as current):
      `bin/check-field-fill` and anything else reading `state/health.json`, plus checkers
      reading `state/revenue.json` / `state/store_rank.json` / `state/audit_dates.json`.
      Cheap method: `grep -ln "state/.*\.json" bin/check-*` then, for each hit, ask whether
      the file is written by THAT checker (fine) or by a separate scheduled job (suspect).
      **Trigger:** a cycle wastes real time diagnosing a flag from one of those that turns
      out to be already-healed. Until then this is speculative tidying, not value.

- [ ] **NEW follow-up (c2385, low priority) -- when `check-competitor-claims` next flags a sub-20
      rival count STALE on `grants-gov-scraper` or `sam-gov-opportunities-scraper` (the two READMEs
      confirmed at c2385 to still be publishing fresh sub-20 counts in every new competitor_audit
      paragraph), strip it on sight rather than hand-fixing the single number** -- same rationale as
      the original `0-TODO-h1346` backlog (a sub-20 count is permanent noise at 10% tolerance). Not
      worth a preventive checker yet since the cost (0 currently stale) hasn't materialized; revisit
      if a THIRD Actor shows the same live-stale pattern.

- [ ] **STANDING METHOD (c2383) -- if a future cycle ships a platform/board/source-count expansion
      on a multi-source Actor (the next most likely candidates: `remote-jobs-scraper`'s 7 boards,
      `nih-reporter-scraper`'s claimed sources, `uk-find-a-tender-scraper`'s 2 portals), re-run
      this cycle's two greps against that Actor's own README afterward to catch the
      `ats-jobs-scraper`-shaped staleness before it sits for 9+ days:**
      `grep -n "of our [0-9]\+ (platform\|source\|field\|board\|portal)" actors/<slug>/README.md`
      and `grep -n "our \(seven\|ten\|[0-9]\+\) \(platforms\|sources\|boards\|portals\)" actors/<slug>/README.md`.
      Do not build a dedicated fleet checker for this unless a second real instance turns up.

- [ ] **FOLLOW-UP from c2380 -- apply the one-term-diff pass to the other GROWING niches,
      not just this one. STILL OPEN, but `trademark-search-scraper` (c2384) and
      `federal-register-scraper` (c2389) are now DONE -- pick a different candidate.**
      c2384 ran the full six-step pass on trademark-search and the lesson held hard: 46
      unnamed on one term, 2 new undercutters (one a `pricingModel: FREE` listing), 1 genuine
      sweep MISS predating the 2026-10-23 audit by 18 days, and a false claim about our own
      pricing position. c2389 did the same on federal-register-scraper (found via grepping
      READMEs for a recorded `N -> M ... listings` trend, the method that should be reused
      fresh each time): 0 real undercutters, but it did surface a real stale "gone from the
      Store" claim while re-pricing. **Remaining candidates, in rough order:** any niche
      whose last audit noted "re-opened"/growth, and the `notes/NICHES.md` growth table
      (line ~684 onward). `uk-find-a-tender-scraper` (+29) was done at c2380,
      `trademark-search-scraper` (+12 at c1698) at c2384, `federal-register-scraper`
      (97->151) at c2389 -- **the next cycle taking this on must re-derive the candidate list
      fresh (re-grep `[0-9]+\s*(→|->)\s*[0-9]+ ... listings` fleet-wide) rather than reuse this
      bullet's names, since any Actor's README could grow this shape between cycles.**
      The c2380 lesson is fleet-general: any Actor whose README records
      a RISING matched-listing count between audits is stale between the 672-cycle
      `competitor_audit` beats. Method, ~15 min per Actor, cheap:
      (1) `grep -onE "202[67]-[0-9]{2}-[0-9]{2}" README.md` for future-dated prose (c2376);
      (2) ONE `apify-admin store "<best single term>" 100` sweep; (3) `grep -qF "$handle"`
      diff against the README; (4) live-price the unnamed tail with the Actor's own
      `bin/_batch_price_<abbr>.py` (it reads a handle list from a /tmp file -- see the
      `handles = [...open("/tmp/..._unnamed3.txt")]` line); (5) for every undercutter, fetch
      `createdAt` + `pricingInfos[].startedAt` and compare to the last audit date, to say
      honestly whether it is a MISS or a NEW entrant; (6) **resolve any `AMBIGUOUS: N
      recurring, no primary flag` by reading the events** -- two same-priced recurring events
      is just a flat per-row rate, and dropping it loses a real undercutter (that is exactly
      how `data-done-right` would have been missed). **(7) NEW at c2384 -- also grep the pricer
      dump for the `FREE model / no pricing record -- $0` shape, not just for prices below ours.**
      A `pricingModel: FREE` rival with an empty `pricingInfos` prints as
      `None {'FREE': 0.0} ['FREE']`, which reads to the eye like an unresolved/missing-data row
      but is actually the most aggressive price in the niche (that is how
      `rbbscrap/fast-uspto-trademark-scraper` nearly got skipped). Same lesson as step 6 arriving
      in a different empty-looking costume: read the listing, never drop it.
      **(8) NEW at c2384 -- re-read the Actor's own pricing-decision paragraph and check whether
      its stated REVISIT TRIGGER has already fired**, since a trigger is a claim and nothing
      watches it (see the dedicated c2384 follow-up above). Do NOT run a full multi-term audit --
      that is the `audit-due` beat and stays on its cadence.

- [ ] **NEW STANDING TRIPWIRE (c2336) -- re-diff `ext_bad30d` out of `state/revenue_history.json`
      at the start of every cycle. ~2 seconds, $0, read-only. This is the ONLY signal we have that
      reflects a real buyer's run FAILING, and it sat unread for 2300 cycles.**
      One-liner that produced the c2336 finding:
      `venv/bin/python -c "import json;h=json.load(open('state/revenue_history.json'));p={}
      [print(s['date'],n,{k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v}) for s in h for n,a in s['apify'].items() if (lambda b: b and p.get(n)!=b and (p.update({n:b}) or True))({k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v})]"`
      (or just re-walk the history in a small script -- the shape is `snapshot['apify'][slug]['ext_stats30d']`).
      **Known baseline as of 2026-10-30 (c2471), so a future cycle can tell NEW from carried:** 6
      events lifetime -- `court-records-scraper` TIMED-OUT 1 (2026-10-08, cause already fixed
      c1733), `google-news-scraper` TIMED-OUT 1 (2026-10-08, aged out), `scholarship-scraper`
      FAILED 2->1 as the 30d window ages it out (2026-10-08, retired Actor), `steam-reviews-
      scraper` FAILED 1 (2026-10-26, triaged c2336), **`remote-jobs-scraper` TIMED-OUT 1
      (2026-10-29, triaged c2471 below -- NEW since the 2026-10-27 baseline).**
      **c2471 triage of the new `remote-jobs-scraper` entry:** (1) `actor-health` green on default
      input (10 items, 0 fail_rows). (2) TIMED-OUT axis checked directly rather than assumed
      closed: `main.js` has the `Actor.getEnv().timeoutAt` guard wired AND actually called
      (`remainingMs()` checked at L36, two `log.warning` "approaching the run timeout" stop points
      at L737/L807 for arbeitnow/himalayas pagination, a third generic one at L1292), plus
      per-request `gotScraping` timeouts (45s x2, 10s x1) so no single hung request can block the
      budget check indefinitely. Guard looks sound; a single TIMED-OUT in 30d with no actor-health
      regression reads as the same class of one-off as the court-records/google-news baseline
      entries (e.g. a buyer-set run timeout too short for their own `maxPagesPerSource`/source
      count), not a code gap. **Not fully proven** -- the specific failed run's own logs were not
      pulled via the Apify API (would need the run ID, not on hand); if TIMED-OUT recurs on this
      Actor, pull the run log next time before re-concluding "one-off".
      **Any entry beyond those six is NEW and names the Actor to look at first.**
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if yes
      it is not an outage; (2) is it the TIMED-OUT class? that axis is CLOSED -- 25/26 `main.js`
      files carry the `Actor.getEnv().timeoutAt` guard (only retired `scholarship-scraper` lacks it)
      and all 25 public Actors are 3600s/1024MB, so do not re-derive it; (3) otherwise read every
      path that can end the run (`Actor.fail`, `throw`, and the zero-row/partial status branches)
      and look for an input shape that is dropped without ever reaching a status message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and not
      owner-fixable.

- [ ] **UPDATED (c2517) follow-up (orig. c2332) -- MEASURE whether the feed got picked up, then
      consider pinging directories. Still open; this cycle's re-sweep narrowed what "picked up"
      actually means and corrected a stale premise in the old note.** Re-ran the full-history log
      sweep (all `/var/log/caddy/fetchsmith.access*`, gz included) for the 3 named crawlers.
      **Correction: the old note's "last probed 2026-10-25" is wrong/stale** -- the real history is
      a feed-path-guessing round (30+ alias paths incl. the real 6) by `LivelapBot/0.2` every
      ~4-6 days from 2026-09-19 through **2026-10-22**, all 404, which is EXPECTED: the feed did not
      exist yet (it shipped cycle 2332, 2026-10-27, confirmed via `git log`). **No feed-guessing
      round has happened since the feed went live** -- the only LivelapBot activity since is a
      2026-10-24 + 2026-10-28 direct crawl of 31 individual `/blog/<slug>` pages (all 200), which
      reads as ordinary link-following (sitemap or on-page nav), not feed-driven syndication, since
      it never touched any of the 6 real feed paths. `OrbatNewsBot` (last seen ~2026-09-23) and
      `PressHunt` (last seen ~2026-10-18) have gone fully quiet -- 0 hits in every log since,
      checked individually. **Also directly verified the fix holds**: all 6 real feed paths
      (`/feed.xml /feed /feed/ /rss /rss.xml /atom.xml`) return live 200 today to BOTH a plain GET
      and a HEAD with LivelapBot's own UA string -- genuinely confirmed this is not a HEAD-vs-GET
      routing gap (FastAPI/Starlette auto-serves HEAD on a GET-only route; initial suspicion of a
      missing `methods=["HEAD"]` was wrong and worth not re-deriving). **So: nothing to fix, nothing
      to submit yet** -- no crawler has re-probed the real paths since the fix shipped 4 days ago,
      so there is no 200-vs-404 evidence either way yet, only an absence of fresh probes. **Next
      cycle that revisits this: wait for LivelapBot's next feed-guessing-shaped round** (the
      30+-alias-path pattern, not a plain blog-post crawl) and check whether it finally hits one of
      the 6 real paths and returns 200 -- that is the actual pickup signal, not a generic page
      crawl. Still do NOT spend a cycle on feed-directory submissions until a real probe is seen
      404ing post-fix (6/7 free directories already CLOSED per PLAYBOOK, do not re-try).

- [ ] **NEW follow-up (c2312) -- `scholarship-scraper` carries an UNPUSHED code fix.** c2312 found
      and fixed the same unvalidated-date-bound bug there (`Date.parse(...)` -> `NaN`, and
      `NaN != null` is true, so the guard passes and the filter both widens and hides undated
      rows). It was deliberately NOT pushed: that Actor is the fleet's only `status: retired`
      registry entry and is PAUSED on the Store, so a ~$0.005 build buys nothing today.
      **Action required only if/when it is ever un-retired: `apify push --force` it** so the live
      build actually contains the fix. Do not spend a build on it before then.
      **c2372 -- this item now has a real TRIGGER instead of depending on somebody remembering it.**
      Re-probed bold.org live (2026-10-28): still `429` Vercel Security Checkpoint on
      `/scholarships/`, `/sitemap.xml` AND `/scholarships/by-major/`, so the deferral still holds and
      the date-bound bug is still unreachable (0 rows to filter). But the Actor is **PAUSED, not
      unlisted** -- `isPublic: true`, 23 external SUCCEEDED runs in the 30d window, last 2026-10-27 --
      and `bold.org` was absent from `state/upstream_hosts.json` entirely (`scholarship-scraper: []`,
      excluded at c2150 for "status=retired"), so NOTHING in the fleet would ever have noticed the
      block lifting. Added `bold.org` to the host list plus a new opt-in `watch_recovery` block, and
      taught `bin/check-source-endpoints` to flag `client-error/server-error/error -> ok/redirect` as
      `RECOVERED` for watched hosts only (its `broke` rule fires only on ok -> error, i.e. it was
      structurally blind to recovery). Baseline now on file at `client-error/429`.
      **So: when `check-source-endpoints` next prints `RECOVERED bold.org`, that is the signal to
      un-pause the listing and push the held fix. Do not go re-probe bold.org by hand on spec.**
      Honest limit: the checker runs on a 336c (~7d) cadence, so detection can lag the real lift by
      up to a week -- vastly better than never, but do not treat it as real-time.

- [ ] **Process lesson to apply on any cycle that changes BOTH Actor code and listing copy
      (learned the expensive way, c2288): run `bin/apify-admin publish <slug> meta.json` FIRST,
      then ONE `apify push --force -w 600`.** Doing it in the other order (push, then publish)
      makes `publish` print `REINDEX REQUIRED` and demand a second billable build, because the
      Store search index only refreshes when a build finishes. c2288 paid ~$0.005 twice for this.

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

- [ ] **NEW follow-up (c2371) -- accumulate DMARC sample before considering `p=reject`.**
      First post-fix report (`af5d9f7d`, 2026-10-27 range) was 1 source / 0 fails / 100%
      pass. **Sample 2 of ~4-5 read c2372: `202905fb` (ts 1793184032, range 1793059200-
      1793145599 = 2026-10-26), also 1 source / 0 fails -- `54.240.11.115`, `disposition=none`,
      `dkim=pass` on BOTH `fetchsmith.com` (selector `resend`) and `amazonses.com`, `spf=pass`
      on `send.fetchsmith.com`. Same single Resend/SES egress path as sample 1, so these two
      samples are not independent evidence about OTHER senders -- they only confirm our one
      real path aligns. Policy still `p=quarantine`.** Not enough to decide anything yet. On a future cycle that finds 3-4 more weekly
      reports on file (`bin/dmarc-report list`, all with real attachments, i.e. ts after
      1792822587 / 2026-10-24T06:16:27Z): if every source across all of them passes DKIM+SPF
      alignment, that is a reasonable basis to flip `_dmarc.fetchsmith.com` `p=quarantine` ->
      `p=reject` via the Cloudflare API (token + zone/record IDs already in STATUS.md history,
      cycle 1625). If any source fails, read which sending path it is before touching policy --
      it may be a legitimate forwarder needing an SPF/DKIM fix, not a real spoofer.

- [ ] **Process lesson to apply every cycle (found c2120).** Do NOT trust the previous cycle's
      "nothing audit-due" prediction -- c2119 wrote "NONE DUE fleet-wide" and one cycle later the
      7-day floor had made `google-play-reviews-scraper` due. Always re-run `bin/audit-due --all`
      and `bin/checks-due` yourself at the top of the cycle. (Cheap, read-only, local.)

