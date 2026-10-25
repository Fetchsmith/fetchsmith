- [x] **DONE cycle 2245 (NOT a QUALITY slot -- `2245%3==1`, verified via
      `python3 -c "print(2245%3)"`) -- closed `scholarship-scraper`'s entire trend-guarded
      stale backlog (5 of 5), per c2244's "give one of ats-jobs-scraper/scholarship-scraper
      the next non-QUALITY slot, do not defer again."**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-source-endpoints`,
      1c, cycle 2246), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      172c, cycle 2417), inbox unchanged (10 known spam/DMARC/resolved items), services/site
      healthy, tree clean before edits.
      `--only ats-jobs-scraper --only scholarship-scraper` confirmed the shape: `ats-jobs
      -scraper` 4 stale (3 superlative-guarded, 1 trend-guarded), `scholarship-scraper` 5
      stale (all trend-guarded in one dense paragraph). Picked `scholarship-scraper` as the
      cleaner single-paragraph fix. **Independently re-fetched all 9 single-site-scraper
      listings named in that paragraph live via the Apify API**, including the 4 unflagged
      ones since the whole paragraph was being rewritten: `parseforge/niche-scholarships
      -scraper` 3->1, `dadhalfdev/scholarships-com-scraper` 3->2, `dadhalfdev/fastweb
      -scraper` 2->3, `jungle_synthesizer/unigo-scholarship-match-scraper` 2->3,
      `parseforge/college-board-scholarship-search-scraper` 2->3 had drifted;
      `dadhalfdev/scholarshipportal-scraper` (3), `dadhalfdev/scholarshipsads-scraper` (3),
      `jungle_synthesizer/scholarships-com-directory-scraper` (2) and
      `jungle_synthesizer/collegescholarships-org-directory-scraper` (1, still down from 2)
      were genuinely unchanged -- left untouched. Each changed count got a scoped
      `as of 2026-10-25`, never restamping the paragraph's own lead pricing-verification
      date (`verified live 2026-10-04`, which attests to price not count, not re-checked
      this cycle).
      Build **0.1.32** pushed README-only, SUCCEEDED, live README byte-verified identical
      (15867 local == 15867 live). `--only scholarship-scraper` after: 0 stale, 0 undated.
      `check-charges` 25/0 and `check-pricing` 25/30/0 both clean throughout. One commit
      (`b8f47475`, bundled with the routine revenue-state refresh).
      $0 on runs + 1 build (~$0.005), 0 new Actors, revenue still $0 booked, no owner email
      warranted.

- [x] **DONE cycle 2244 (MANDATED QUALITY slot -- `2244%3==0`, verified via
      `python3 -c "print(2244%3)"`) -- ran the 3 due fleet checks (all CLEAN), both PLAYBOOK
      QUALITY tools (both clean), then did the proactive STATUS.md + queue.md trim
      `check-doc-size` asked for and closed the entire 4-file UNDATED-paragraph backlog.**
      Re-verified fresh first rather than trusting c2243's handoff (c2120 lesson): `checks-due`
      read **3 DUE**, not the handoff's 1 -- `check-row-floor`, `check-doc-size`,
      `check-upstream-warnings`. `audit-due --all` NONE DUE (soonest
      `website-screenshot-scraper`, 173c, cycle 2417), inbox unchanged (10 known
      spam/DMARC/resolved `dc593cfb` items), services active, site 200 on `/` `/tools`
      `/pricing`, `HEAD == origin/main` (`8d73652b`) and tree clean before edits.
      1. **All 3 due fleet checks CLEAN, all recorded.** `check-row-floor`: 24 live Actors,
         every one >=60% of requested cap, none declined from its own observed best.
         `check-upstream-warnings`: 23 niches / 10,514 listings seen / 5,523 in-niche, no rival
         advertises a new upstream shutdown; the 2 known `steam-reviews-scraper` acks unchanged.
         `check-disclosure` 0 missing across 87 blog posts + 23 dev.to articles;
         `devto-comments` 23 articles / 12 inbound / **0 unanswered**. No support mail.
      2. **`check-doc-size` was the real find: TRIM SOON on both live docs**, projecting ~240KB
         (STATUS.md) and ~241KB (queue.md) at its OWN next look (24c, cycle 2268) -- past both
         the 150KB warn and 200KB trim lines BETWEEN looks. Its own advice is to pre-empt that
         in a QUALITY slot, so both were trimmed: **STATUS.md 134.3KB/232 lines -> 21.5KB/61
         lines** (`bin/_trim2244.py`, keeps the newest 5 blocks 2239..2243) and **queue.md
         113.5KB/1410 lines -> 24.0KB/306 lines** (`bin/_trim2244q.py`, keeps the 5 DONE blocks
         matching the STATUS window + 10 hoisted open items). Everything else moved VERBATIM
         into the two archives; 6 lossless verifications each (full-file reconstruction,
         archive-append-only, no cycle block or open item destroyed). Re-run after: both **OK**,
         41 and 33 cycles of headroom. `check-status-continuity` NONE MISSING and
         `check-status-blocks-kept` OK on the new 650-block window.
         **KEEP_BLOCKS=5, not c2220's 8, for a reason worth reusing:** blocks are not stored
         newest-first (2236 sat above 2237/2238), so only the 5- and 8-prefixes are hole-free
         for `check-status-continuity` -- and 8 leaves 36.7KB, projecting 146.8KB at 2268, i.e.
         ON the warn line. c2220 made exactly that call and came within 3KB of having to redo
         it. 5 leaves 21.5KB and projects 131.6KB.
      3. **Found a duplicate task while auditing open items for the trim:** the c2224
         `maxCommentDepth` null-on-failure follow-up existed TWICE (old :929 and :994), carried
         as two separate open items for ~20 cycles. :994 is a strict superset (adds the
         `bin/run-charged` instruction); the trim script asserts :929 is a word-level subset
         before archiving it as closed, so the de-dup is proven, not assumed. 12 open items -> 10.
      4. **Closed the whole UNDATED-paragraph backlog (4 of 4).** None was genuinely undated:
         each sat under a real 2026-10-23 sweep and merely lacked a date in the shape `DATED`
         matches. Read the checker's regex instead of guessing a phrasing, then made the
         minimal truthful edit per file, scoping each date to what that pass actually
         re-verified (see the carried backlog item below for the `sam-gov` scoping decision).
         Builds **0.1.82** (clinicaltrials), **0.1.57** (federal-register), **0.1.60**
         (nih-reporter), **0.1.67** (sam-gov) all pushed README-only and all SUCCEEDED; all 4
         live READMEs byte-verified identical via the build API's `readme` field
         (59440/42061/50237/80884 chars, local == live on each).
      `--only` sweep of the 4 files after: **0 stale, 0 undated.** `check-charges` 25/0 and
      `check-pricing` 25/30/0 clean after the pushes; services + site re-verified 200 after all
      edits. $0 on runs, 4 builds (~$0.02), 0 new Actors, revenue still $0 booked, no owner
      email warranted (no revenue event, no outage).

- [x] **DONE cycle 2243 (NOT a QUALITY slot -- `2243%3==2`, verified via
      `python3 -c "print(2243%3)"`) -- closed the next two smallest competitor-claims backlog
      files per c2242's handoff: `fec-campaign-finance-scraper` and `remote-jobs-scraper`,
      both 1 superlative-guarded claim each. Fleet total 14 -> 12 stale (4 undated untouched).**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-row-floor`, 1c, cycle
      2244), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`, 174c, cycle
      2417), inbox unchanged (10 known spam/DMARC/resolved `dc593cfb` items), services/site
      healthy, tree clean at `68f62a1d` after.
      Re-fetched both listings' live `stats` myself via the Apify API:
      `parseforge/fec-campaign-finance-contributions-scraper` 9->11 users (date split -- the
      existing `re-verified live 2026-10-16` attests only to its pricing ladder, reworded
      `pricing re-verified live 2026-10-16` beside a new `11 users as of 2026-10-25`);
      `deriverge/remote-jobs-scraper` 2->3 users (plain `as of 2026-10-25` append, no
      pre-existing date -- matched the `flash_scraper/remote-job-aggregator` precedent already
      in the same README). Checked both paragraphs' superlatives for breakage: `fec`'s
      "`ryanclinton/fec-campaign-finance` (17 users, the busiest in the niche)" still holds
      against the new 11 (ryanclinton itself drifted to 18 live, under the checker's 10%
      tolerance, left untouched); `remote-jobs-scraper`'s nearby "cheapest full-parity
      substitute" bullets don't reference `deriverge`, so the guard was conservative not wrong.
      Builds **0.1.77** (fec) and **0.1.83** (remote-jobs) pushed README-only, both live
      READMEs byte-verified identical via the build API (56582/56582 and 88086/88086 decoded
      chars). `check-charges` 25/0 and `check-pricing` 25/30/0 both clean throughout. One
      commit (`68f62a1d`).
      $0 on runs + 2 builds (~$0.01), 0 new Actors, revenue still $0 booked, no owner email
      warranted.

- [x] **DONE cycle 2240 (NOT a QUALITY slot -- `2240%3==2`, verified via
      `python3 -c "print(2240%3)"`) -- rebuilt `bin/check-competitor-claims --fix` so a dated
      paragraph is no longer a blocker, added `--only <substr>` scoping, and closed
      `scholarship-scraper`:115 including a FALSE comparative claim next door.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-row-floor`, 4c, cycle
      2244), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`, 177c, cycle
      2417), inbox unchanged (10 known spam/DMARC/resolved `dc593cfb` items), services active,
      site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main` (`5f767d65`), tree clean.
      1. **Replaced c2239's date guard with `fix_plan()`** -- c2239's "any YYYY-MM-DD in the
         paragraph" guard fired on 100% of the backlog, so --fix fixed 0. The hazard was never
         a date's presence, it was RESTAMPING one; `fix_plan()` now splices an `as of <today>`
         scoped to the count and never touches the paragraph's other dates (an `as of` already
         on that same count is restamped, not duplicated). Added a **trend-claim guard**
         (`down from|up from|up N|unchanged|was N|grew|doubl`) because a fresh count can
         falsify "1 user, down from 2" by itself. Proved all 6 cases (split / restamp /
         plain-swap / 3 guards) on `actors/zzztest-fixture/README.md`, deleted after (confirmed
         via `git status`).
      2. **Added `--only <substr>` (repeatable)** -- positional slug args were always IGNORED
         (c2236), so every run swept 113 files / 709 claims / 5+ min. `--only` makes it
         seconds, which is what makes --fix usable in one cycle. It prints a loud NOTE and is
         NOT a valid run of record for the `fleet_checks.json` cadence; keep the cadence sweep
         unfiltered.
      3. **Honest yield: 1 of 13.** On the three densest backlog files it auto-fixed only
         `dami_studio/unstop-scraper` 39 -> 45. The other 12 are blocked by the OTHER guards
         (superlative 4, 30-day 1, trend 6) -- see LEARNINGS c2240; prose shape, not tooling,
         is the remaining lever.
      4. **Found and fixed a pre-existing public falsehood** the fix sat next to:
         `scholarship-scraper`:115 claimed three Unstop scrapers "are bigger by users than any
         rival named above" -- live, only `solidcode` (104) is; `parsebird` (69) and
         `dami_studio` (45) both trail `majestic_fund`'s 78 (re-fetched all 6 listings myself).
         It was false at the old number too. Reworded truthfully and wrote
         `majestic_fund/the-scholarship-scraper-actor`'s 78 as a backticked full-slug count so
         the checker now monitors the comparison's own baseline. Build **0.1.31** pushed
         (README-only), live build README verified **byte-identical** via
         `GET /v2/actor-builds/OcJOkL4CAYpTjhTd0`. `--only scholarship-scraper` after: line 115
         clean, only the 5 guarded line-113 claims left.
      $0 on runs, 1 build (~$0.005), 0 new Actors, revenue still $0 booked, no owner email
      warranted.

- [x] **DONE cycle 2241 (MANDATED QUALITY slot -- `2241%3==0`) -- ran both PLAYBOOK QUALITY
      tools (clean), then closed `shopify-products-scraper` and `trademark-search-scraper`
      end-to-end: 3 auto-fixed via `--only --fix`, 2 hand-fixed after independent live
      re-verification. Fleet total 22 -> 18 stale, 6 -> 5 undated.**
      `devto-comments` 0 unanswered, `check-disclosure` 0 missing. `--only shopify-products
      -scraper --only trademark-search-scraper --fix` auto-fixed `clearpath/shop-by-shopify
      -product-scraper` 111->130, `scrapewise/uspto-trademark-scraper` 2->3,
      `automation-lab/euipo-tmview-trademarks-scraper` 55->66. Hand-fixed:
      `lurkapi/shopify-product-reviews-scraper-api` 68->80 (superlative guard was about
      price, not this count -- safe to touch; date split since the existing date attested
      to scope not count); `trademark-search-scraper`:321 UNDATED only because its heading
      date lacked a checker-recognized word -- re-verified `scrapersdelight/
      euipo-trademark-scraper` and `northbell/us-trademark-search` live, both unchanged at
      2 users, added a recognized `re-verified live 2026-10-25` phrase without restamping a
      count that didn't move. Builds 0.1.101 / 0.1.78 pushed README-only, both live READMEs
      byte-verified identical via the build API. `check-charges`/`check-pricing` clean
      throughout. One commit (`f41aabb0`). $0 on runs + 2 builds (~$0.01), 0 new Actors, no
      owner email warranted.

- [x] **DONE cycle 2242 (NOT a QUALITY slot -- `2242%3==1`, verified via
      `python3 -c "print(2242%3)"`) -- closed `website-screenshot-scraper` (1 stale +
      1 undated) and `substack-scraper` (3 guarded stale), both now 0 STALE/UNDATED.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all` both NONE DUE, inbox
      unchanged (10 known spam/DMARC/resolved items), services/site healthy, tree clean at
      `55cd924d`.
      `website-screenshot-scraper`: `--only --fix` auto-fixed `cheapapi/website-screenshot
      -api` 247->302 (date split, as the handoff predicted). The :131 UNDATED paragraph
      named `dz_omar/ultimate-screenshot` and `scrapeai/screenshot-downloader` with a
      discovery date but no verification word -- re-fetched both live (users and tiered
      PAY_PER_EVENT pricing both within the checker's 10% tolerance, i.e. genuinely
      unchanged) and appended a checker-legible `re-verified live 2026-10-25` phrase.
      `substack-scraper`: all 3 guarded claims had drifted past 10% since the c2241 handoff
      (fresh sweep, not the stale 1-claim handoff number) -- `brilliant_gum/substack
      -insights-scraper` 199->231 users (30-day sub-figure also updated 72->57, dedicated
      date restamped since it attests only to this one parenthetical); `contactminerlabs/
      substack-email-scraper---advanced-cheapest-reliable` 57->64u (dedicated date
      restamped) -- **the superlative guard fired on this one as a FALSE POSITIVE: the
      word "cheapest" is baked into the Actor's own slug, not an actual superlative claim
      in the paragraph's prose; worth tightening the guard regex to skip slug text, but
      hand-verifying is cheap enough that it wasn't worth it this cycle**;
      `haketa/substack-scraper` 3u->1u (count-scoped `as of` appended, NOT restamping the
      paragraph's shared lead date which also covers 4 other rivals not re-verified this
      cycle).
      Both pushed README-only (builds 0.1.29 website-screenshot-scraper, 0.1.83
      substack-scraper, both SUCCEEDED) and live READMEs verified byte-identical via the
      build API (18657/18657 and 55566/55566 chars). `check-charges`/`check-pricing` clean
      throughout. Two commits (`5fe0625d`, `438474b8`).
      **Fresh fleet-wide re-run after both fixes: 18 -> 14 stale, 5 -> 4 undated** (not a
      `--ran` run-of-record since the fleet isn't clean yet, same judgment call as c2236/
      c2239).
      $0 on runs (Apify metadata-read API calls only) + 2 builds (~$0.01), 0 new Actors,
      revenue still $0 booked, no owner email warranted.

- [x] **DONE cycle 2239 (NOT a QUALITY slot -- `2239%3==1`) -- built the `--fix` mode
      queued by c2236, verified the mechanism, then found it fixes 0 of the current backlog.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all` both NONE DUE, inbox
      unchanged (10 known spam/DMARC items, nothing new to answer), services/site healthy,
      tree clean at `0abe861a`.
      Added `--fix` to `bin/check-competitor-claims`: a guarded helper (`guard_reason`)
      scans the WHOLE PARAGRAPH (not just the sentence -- deliberately coarser, so it only
      ever skips more than a human would, never less) around a stale numeric claim for a
      date token, a "30 day" substring, or a superlative; if none are present and `--fix`
      is passed, the live count is spliced in in place (preserving comma formatting, and
      flipping "user"/"users" when the new count is exactly 1), the file is rewritten, and
      a `FIXED` line is printed instead of `STALE`. Guarded claims still print as
      `STALE (guard: ...)` -- unchanged hand-fix backlog, nothing silently dropped.
      **Verified the mechanism on a synthetic fixture** (`actors/zzztest-fixture/README.md`,
      deleted after): dry run correctly printed plain `STALE` (no guard) for
      `` `gentle_cloud/hacker-news-scraper` has 5 users ``; `--fix` rewrote it to
      `218 users` (live at the time) with correct pluralization, then the fixture was
      removed and `git status` confirmed no stray files.
      **Then ran it for real and got a null result: all 22 of the fleet's currently-stale
      claims are guarded, 0 fixed.** Not over-caution -- spot-checked
      `trademark-search-scraper`:288 by hand and the date (`2026-10-16`) sits in the exact
      same sentence as the stale count, the precise c2235/c2236 trap the guard exists to
      catch. **Root cause, written up in LEARNINGS c2239: once a paragraph is hand-fixed
      once it carries a date forever, and the next time its count drifts the date is still
      sitting next to it** -- so a "number is the only thing wrong" claim is structurally
      rare on this fleet, and the c2236 premise ("hand-fixing cannot converge, `--fix` is
      the cheap alternative") doesn't hold against the current shape of the backlog.
      `--fix` is still real and committed (useful for first-time/undated competitor
      mentions and as a regression guard), just not a shortcut through the 22 that remain.
      `check-charges`/`check-pricing`/`check-shell-expansion` clean; services/site healthy
      throughout. One commit (`8db0e6bc`). $0 spent (no Actor runs, no builds -- no README
      content changed on any real Actor this cycle), 0 new Actors, revenue still $0 booked,
      no owner email warranted.

- [ ] **CARRIED follow-up (c2236 -> c2246, MEDIUM) -- `scholarship-scraper` CLOSED c2245,
      `ats-jobs-scraper` CLOSED c2246 (4 of 4: 3 superlative-guarded + 1 trend-guarded; the
      trend-guarded `scrapebench` one turned out to be a real pricing-model misdescription,
      not just a stale count -- its live `pricingInfos` show a flat per-job charge, not the
      "per-run fee, break-even at 2 jobs" the README used to claim; see DONE block above).
      Fleet-wide remainder is now just 3 small singletons -- do them next, any slot, they're
      quick:** `eu-ted-tenders-scraper`:136 (`foxlabs/ted-tenders` 46->52 as of 2026-10-25
      fresh sweep, trend-guarded) and :170 (`jungle_synthesizer/marchespublics-morocco
      -public-tenders-scraper` 5->7, 30-day-guarded), `sec-insider-trades-scraper`:247
      (`constructive_calm/sec-edgar-scraper` 58->65, 30-day-guarded). Re-measure stale fresh
      with `bin/check-competitor-claims` (unfiltered -- only 711 claims / 222 paragraphs,
      fast enough to run whole) before starting, it drifts within a cycle. `--fix` works on
      the plain-date case but NOT on superlative/30-day/trend guards, see LEARNINGS c2240.
      **Lesson from this cycle: don't trust a prior cycle's "this is the ENTIRE remaining
      backlog" line without re-running the unfiltered sweep yourself** -- c2245 said
      `ats-jobs-scraper` was the entire fleet-wide remainder, but these 3 singletons were
      already sitting in this very item's text the whole time, just not restated in that
      cycle's summary.
      **All 4 UNDATED paragraphs were CLOSED in c2244** (`clinicaltrials-scraper`:176,
      `federal-register-scraper`:180, `nih-reporter-scraper`:203,
      `sam-gov-opportunities-scraper`:326). None of them was actually undated work -- each sat
      under a real 2026-10-23 sweep and just lacked a date in the shape `DATED` matches
      (`(verified|checked|re-verified|rechecked)[^.]{0,40}?YYYY-MM-DD`, i.e. the word and the
      date in the SAME sentence within 40 chars). Phrases like "read live via `pricingInfos`
      on 2026-10-23" or "Sixth sweep, 2026-10-23" are invisible to it. **Scope the date to
      what the pass actually re-verified, not to the whole paragraph** -- c2244's `sam-gov`
      fix says the "and now" names were verified 2026-10-23 while every other name keeps its
      own pass's date, because the 2026-10-23 pass live-priced the 133 unnamed listings, not
      the 50 already named on the page. Restamping the lot would have been a cheap way to make
      a checker green by publishing a claim we had not re-checked.
      **Use c2240-c2242's method:** start with `--only <slug> [--only <slug>] --fix`
      (seconds, not 5+ min; prints a loud NOTE, NOT a valid run of record for
      `fleet_checks.json` -- keep the periodic sweep unfiltered), then hand-fix the guarded
      remainder after independently re-fetching live stats via the Apify API. **Before
      restamping vs splitting a date, check whether the existing date is DEDICATED to this
      one claim's own parenthetical (restamp it) or SHARED across a paragraph covering
      several rivals (split -- append a count-scoped `as of <date>`, never restamp the
      shared one unless every claim it covers was re-verified this cycle)** -- c2242 found
      both shapes in the same file. **Also watch for the superlative-guard false positive
      c2242 found**: a rival's own Actor slug can contain a superlative word
      ("...-cheapest-reliable") that trips the guard with no actual superlative claim in
      the prose -- safe to hand-fix after confirming the paragraph itself makes no such
      claim, not a reason to leave it stale. **c2240 lesson: when a count changes, read the
      WHOLE paragraph** -- comparative sentences built on it
      ("bigger by users than any rival named above") are invisible to every check we own, and
      one was already false at `scholarship-scraper`:115.

- [ ] **NEW follow-up (c2238, MEDIUM-HIGH, not urgent -- a real redesign) -- add a machine-
      readable `x-appliesTo` (mode allowlist) schema annotation, and separately a per-mode
      MEANING annotation, to replace prose-mining in `check-mode-scope-warning`.** Raised by a
      dev.to reader on article 4909344 (`@stae_him_ae35092536b300a4`), answered in full there and
      in this cycle's STATUS.md. Two distinct pieces, do not conflate: (1) `x-appliesTo: [modes]`
      on a schema property replaces the check's prose-sentence parsing and two-idiom
      (array-`.filter`/loop-table) reachability matching with a structured fact, and makes
      negative-test generation (field set outside its modes -> expect warning; field omitted in
      an excluded mode -> expect silence) mechanical instead of hand-verified per fix -- this is
      the valuable half. (2) A separate per-mode-meaning map (e.g. for fec's
      `contributionDateFrom`/`contributionDateTo` or this Actor's own release-date window) would
      feed a DIFFERENT check -- "does the field's description state what it means in each mode
      it's active in" -- not a warning-reachability one; building it as the same annotation as
      (1) would create false confidence. Scope before starting: retrofitting every mode-scoped
      field's schema across the fleet, and the generator itself becomes load-bearing (a wrong
      annotation means a field gets silently zero coverage instead of a loud grep failure).

- [ ] **NEW follow-up (c2232, MEDIUM; `fec-campaign-finance-scraper` and
      `apple-podcasts-scraper` slices CLOSED) -- judge the remaining fields
      `check-mode-scope-warning` flags on the fleet.** These are CANDIDATES, not confirmed
      bugs until the code path is read. **5 flags remain**: `court-records-scraper`
      (`judge`, NO schema default -- `!== undefined` is the correct check), `google-news
      -scraper` (`publishedAfter`, `publishedBefore`, both NO default), `steam-reviews
      -scraper` (`maxReviewsPerApp` -- **HAS `"default": 200`, use a default-comparison
      check like `input.X !== 200`, NOT `!== undefined`** -- `includePlayerCount`,
      `includeOwnerEstimates`, both NO default). For each: read the wrong-mode code path,
      decide whether a buyer can be charged for unfiltered rows, and **before writing the
      check, grep the field's schema entry for `"default"` and pick the right idiom (see
      LEARNINGS cycle 2234)** -- two of the last two fixes shipped a false-positive from
      skipping exactly that step. **Default answer to a flag is to ADD the warning, not to
      allowlist** -- `state/mode_scope_allow.json` exists (currently empty on purpose, so
      these stay visible) and an entry requires a real reason sentence; the check flags an
      empty one. Do one Actor per cycle and batch the warning + README into that Actor's
      single push. **Also: after shipping any `!== undefined` mode-scope check, test the
      OMISSION case live (field never mentioned in the input JSON), not just an explicit
      wrong-mode value** -- an explicit-value-only test cannot distinguish a correct check
      from one that fires on every run.

- [ ] **NEW follow-up (c2232, LOW) -- `bin/check-disclosure` is NOT in
      `state/fleet_checks.json`.** Its "run on every QUALITY cycle" instruction lives only
      in PLAYBOOK prose, which is the exact failure shape `fleet_checks.json`'s own `_readme`
      was created (c1624) to close for `devto-comments` and `check-competitor-claims`. It
      did get run this cycle, so nothing is currently rotting -- but it is unregistered and
      therefore invisible to `bin/checks-due`. Decide deliberately: either register it with a
      justified interval, or write into the `_readme` why a PLAYBOOK-cadence check is
      exempt. Do not silently register it without picking an interval from measured drift.

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

