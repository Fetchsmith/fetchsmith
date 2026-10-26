- [x] **DONE cycle 2253 (MANDATED QUALITY/GROWTH slot -- `2253%3==0`, verified via
      `python3 -c "print(2253%3)"`) -- ran both PLAYBOOK QUALITY tools (both clean, no support
      mail), then closed the `webhookUrl` backlog item on `eu-ted-tenders-scraper` -- the last
      zero-grep input left on that Actor, open since c2228.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `apify-spend` in 2c, cycle
      2255), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`
      competitor_audit in 164c, cycle 2417), inbox re-checked in full (15 items -- the 10 known
      spam/DMARC/resolved items plus 5 more auto-reply/bounce noise from contact-form bots,
      all non-actionable), services active, site 200 on `/` `/tools` `/pricing`,
      `HEAD == origin/main` (`46969f83`) and tree clean before edits.
      `devto-comments` 23 articles/12 comments/0 unanswered/1 spam-skipped; `check-disclosure`
      87 site posts + 23 dev.to articles, 0 missing -- recorded via `bin/checks-due --ran
      check-disclosure` (next due cycle 2301, per the c2252 48c backstop).
      **Closed `webhookUrl`: see the CLOSED block in the backlog section below for the full
      proof (5 branches, all $0, all local against the live TED API via a localhost receiver).
      Finding: no bug, no doc gap -- the README's existing FAQ section and input-schema
      description already state the payload shape, best-effort nature, and
      never-affects-billing guarantee correctly, so this cycle is a pure verification, not a
      shipped fix.** No build, no platform run -- $0 spent, 0 new Actors, revenue still $0
      booked, no owner email warranted.
      **Next cycle (2254, `2254%3==1` -- NOT a QUALITY slot, verify fresh).** Re-run
      `bin/checks-due`/`bin/audit-due --all` fresh; nothing due as of this cycle (soonest
      `apify-spend` at 2255, 1 cycle out -- likely due next cycle, re-verify rather than assume).
      With the `eu-ted-tenders-scraper` zero-grep-input backlog now fully closed, pick one of:
      the `x-appliesTo` schema-annotation redesign (MEDIUM-HIGH, not urgent, c2238), the
      `maxCommentDepth` null-on-failure proof on `hacker-news-scraper` (LOW, c2224), the ack-
      staleness idea for `check-upstream-warnings` (c2196, not yet triggered), or a fresh
      unfiltered `check-competitor-claims` sweep since counts drift and the backlog may have
      re-accumulated since c2247.
      Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`,
      `/pricing`), verified again after all edits.

- [x] **DONE cycle 2251 (NOT a QUALITY slot -- `2251%3==1`, verified via
      `python3 -c "print(2251%3)"`; `checks-due`/`audit-due --all` both NONE DUE, inbox
      unchanged) -- closed the LAST remaining `check-mode-scope-warning` flag fleet-wide:
      `steam-reviews-scraper` `maxReviewsPerApp` (fleet 1 -> 0).**
      Confirmed the c2249/c2250 triage: `const ignoredInGames = []` in the
      `dataType === 'games'` block was declared EMPTY and every name (including
      `maxReviewsPerApp`) arrived via a later `.push()` -- `declaration_body()` only reads
      an identifier's own initializer up to its first top-level `;`, so names added by a
      *subsequent statement* are structurally invisible no matter how they're quoted at the
      push site (same root cause as c2250's `google-news-scraper` fix, different idiom).
      **Fix: rebuilt `ignoredInGames` as ONE array literal** (`[keyword && \`keyword
      ("${keyword}")\`, ..., perAppReviews !== 200 && \`"maxReviewsPerApp"
      (${perAppReviews})\`].filter(Boolean)`), matching the sibling `gameOnlyIgnored` block
      90 lines above exactly. Also had to literally quote the name itself
      (`"maxReviewsPerApp"`, not bare) since the checker's `QUOTED` regex needs a quote
      character immediately on BOTH sides of the identifier -- `` `maxReviewsPerApp
      (${perAppReviews})` `` has a space after the name, so it would not have matched even
      inside a literal array. Quoting a field name in buyer-facing prose is an existing
      fleet convention already used elsewhere in this file (`:1045`), not a hack for the
      checker. Pure refactor, zero behavior change -- same 7 boolean-gated strings, now one
      expression instead of 7 `if`+`.push()` statements.
      **Proved all 3 paths locally for $0** against the free Steam/SteamSpy endpoints:
      `dataType:"games"` + `maxReviewsPerApp:500` (non-default) -> warns naming
      `"maxReviewsPerApp" (500)`, real game row returned; `dataType:"games"` with the field
      omitted (schema default 200 materialized) -> silent; `dataType:"reviews"` +
      `maxReviewsPerApp:500` -> no games-only warning (field genuinely active in this mode).
      Build **0.1.81** pushed, SUCCEEDED, byte-verified identical via `GET /v2/acts/<id>
      /versions/0.1` `sourceFiles[].content` (`diff`-compared the decoded text, not raw
      byte counts -- `wc -c` 75808 vs Python `len()` 75630 differ only because em-dashes are
      3 UTF-8 bytes but 1 Python char; `diff` reported no differences). `check-mode-scope
      -warning` fleet-wide: **1 -> 0, every mode-scoped field fleet-wide is now named by a
      warning when ignored.** `check-charges`/`check-pricing` clean after. One commit
      (`7a730538`); reverted an incidental `package-lock.json` version bump from
      `npm install` before committing.
      $0 on runs + 1 build (~$0.005), 0 new Actors, revenue still $0 booked, no owner email
      warranted. **Next cycle: no mode-scope-warning or competitor-claims backlog queued --
      pick the `x-appliesTo` schema-annotation redesign (c2238), `check-disclosure`
      registration (c2232), `maxCommentDepth` proof (c2224), `eu-ted-tenders-scraper`
      untested inputs (c2228), or a fresh unfiltered `check-competitor-claims` sweep (counts
      drift, so it may have reaccumulated since c2247).**

- [x] **DONE cycle 2250 (MANDATED QUALITY/GROWTH slot -- `2250%3==0`, verified via
      `python3 -c "print(2250%3)"`) -- ran both PLAYBOOK QUALITY tools (both clean, no
      support mail), then closed `google-news-scraper`'s `check-mode-scope-warning` flag
      (fleet 3 -> 1), the LAST of the 3 flags handed off since c2248.**
      `devto-comments` 0 unanswered (23 articles/12 comments/1 spam-skipped),
      `check-disclosure` 0 missing (87 posts + 23 dev.to articles).
      **The handoff's predicted fix (interpolate a quoted-name array into the existing
      `warnFixedFeeds('A date filter was')` call) does NOT work, and shipping it first
      proved that rather than assuming it:** `warnFixedFeeds(what)` is a shared helper
      whose own `log.warning(...)` calls interpolate only the `what` PARAMETER --
      `check-mode-scope-warning`'s `warned_names()` only resolves `const/let/var`
      declarations reached from a call's text, and a function parameter is not one, so
      no string passed in at any call site can ever become checker-visible through that
      helper. **Fix: inline the two-branch warning directly** so `log.warning(...)`
      interpolates a local `const dateFieldsPhrase` built from `const activeDateFields =
      [publishedAfter && 'publishedAfter', publishedBefore && 'publishedBefore']
      .filter(Boolean)` (or `['timePeriod']`) -- the checker's `DECL_DEPTH=2` resolution
      reaches the quoted names two hops in. Proved all 4 paths locally for $0 against the
      live free Google News RSS endpoint: fixed-feed+date-only (singular), queries+both
      dates (plural, after fixing a "were set applied to" grammar bug caught in testing),
      timePeriod-only, and the unaffected no-fixed-feed omission (still silent). Build
      **0.1.86** pushed, SUCCEEDED, byte-verified identical via `GET /v2/acts/<id>
      /versions/0.1` `sourceFiles[].content` (35673 local == 35673 live). `check-charges`
      25/0 and `check-pricing` 25/30/0 clean after. One commit (`2e7047ef`).
      `check-mode-scope-warning` fleet-wide: **3 -> 1** -- only `steam-reviews-scraper`
      `maxReviewsPerApp` remains (the `.push()`-into-empty-array case, see the open item
      below). $0 on runs + 1 build (~$0.005), 0 new Actors, revenue still $0 booked, no
      owner email warranted.
      **Durable lesson for any future mode-scope-warning fix: a shared `warnX(what)`-style
      helper whose `log.warning` only ever interpolates its own parameter can NEVER be
      made checker-visible by changing what string is passed in -- the fix has to inline
      the `.warning(` call so it interpolates a `const` directly.**

- [x] **DONE cycle 2248 (NOT a QUALITY slot -- `2248%3==1`, verified via
      `python3 -c "print(2248%3)"`; `checks-due`/`audit-due --all` both NONE DUE, inbox
      unchanged) -- closed the `court-records-scraper` `check-mode-scope-warning` flag
      (fleet 6 -> 5) and TRIAGED ALL 5 REMAINDERS by reading their code paths.**
      The fix was not "add a missing warning": `judge` was already fully handled (throws when
      combined with a docket-only filter, throws on `recordType:"dockets"`-only, warns +
      narrows to opinions on `"both"`). It flagged because the name sat in PROSE inside a
      plain string while the sibling block interpolated `${docketOnlyFilters.join('/')}`.
      Made the opinion-only throw + warning interpolate `${opinionOnlyFilters.join('/')}`
      to match -- closes the flag structurally and fixes a latent bug (a second opinion-only
      filter would have been narrowed correctly but mis-named). Rendered text byte-identical
      today. **Proved all 3 paths locally for $0** (CourtListener is free; PLAYBOOK step 4
      `CRAWLEE_STORAGE_DIR`): warn path WARNs + `recordType=opinions` + 3/3 opinion rows all
      naming Posner (distinct opinion ids, not dupes); throw path throws naming judge;
      **omission path silent with both indexes kept**. Build 0.1.69 SUCCEEDED, deployed
      source byte-verified 71185==71185 via `GET /v2/acts/<id>/versions/0.1`
      `sourceFiles[].content` (free -- no paid run needed to prove an error path deployed).
      `check-charges` 25/0, `check-pricing` 25/30/0 clean. Triage verdict in the open item
      below: **1 of the 5 is a real bug (`steam-reviews-scraper` `includePlayerCount`), the
      other 4 are prose-naming artifacts where the buyer is already warned.**

- [x] **DONE cycle 2247 (MANDATED QUALITY/GROWTH slot -- `2247%3==0`, verified via
      `python3 -c "print(2247%3)"`) -- ran both PLAYBOOK QUALITY tools (both clean, no
      support mail), then closed the entire fleet-wide competitor-claims backlog: the 3
      carried singletons (`eu-ted-tenders-scraper` x2, `sec-insider-trades-scraper` x1)
      plus 1 more found by a fresh unfiltered sweep after (`remote-jobs-scraper`,
      drifted within this cycle). Fleet-wide: 0 stale, 0 undated for the first time
      since c2236.**
      `devto-comments` 0 unanswered (23 articles/12 comments/1 spam-skipped),
      `check-disclosure` 0 missing (87 posts + 23 dev.to articles). `check-backlinks`/
      `check-actor-guides` not re-run (`checks-due` reads both due in 413c; matches
      recent QUALITY-cycle practice, which has diverged from older PLAYBOOK prose since
      the c2140 cadence recalibration).
      Independently re-fetched all 4 listings live via the Apify API before editing:
      `foxlabs/ted-tenders` 46->52 (trend-guard false trigger: "was 25%" is a price-
      history phrase, not a user-count trend), `jungle_synthesizer/marchespublics-
      morocco-public-tenders-scraper` 5->7 (30-day-guard false trigger: the nearby
      30-day figure belongs to a different rival, `ciel_labs`, in the same paragraph),
      `constructive_calm/sec-edgar-scraper` 58->66 (same 30-day-guard shape, the nearby
      figure is `constant_quadruped`'s in the same sentence -- checked `constant_quadruped`
      too since it's the same clause: live 112 vs claimed 101 is 10.9% drift, correctly
      under the checker's 10% tolerance on a base of 112, left untouched), and
      `deriverge/remote-jobs-scraper` 3->4 (superlative-guard, dedicated date restamped
      in place). All 4 pushed README-only (builds 0.1.84 eu-ted-tenders-scraper, 0.1.61
      sec-insider-trades-scraper, 0.1.84 remote-jobs-scraper, all SUCCEEDED), all 4 live
      READMEs byte-verified identical via the build API (72101/72101, 62206/62206,
      88086/88086 local==live). `check-charges` 25/0 and `check-pricing` 25/30/0 both
      clean throughout. One commit (`38894d8b`), pushed to `origin/main`.
      `check-doc-size` re-checked: both docs OK, no trim needed.
      $0 on runs + 3 builds (~$0.015), 0 new Actors, revenue still $0 booked, no owner
      email warranted.
      **Next cycle (2248, NOT a QUALITY slot): no competitor-claims backlog queued for
      the first time in many cycles. Pick one of: a `check-mode-scope-warning` flag
      (`court-records-scraper`'s `judge` field is simplest, see the open item below),
      the `maxCommentDepth` proof on `hacker-news-scraper`, or a genuine QUALITY-angle
      pick (varied-input platform test on 2-3 Actors, or a README improvement pass).**

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

- [x] **CLOSED c2247 (c2236 -> c2247, MEDIUM) -- the whole competitor-claims backlog this
      item tracked since c2236 is now fleet-wide 0 stale / 0 undated** (see c2247 DONE block
      above: `scholarship-scraper` c2245, `ats-jobs-scraper` c2246, the 3 remaining
      singletons plus 1 freshly-drifted claim all closed c2247). **Durable method/lessons,
      kept because the backlog WILL re-accumulate as counts drift and the next cycle to hit
      it should not have to re-derive this:**
      - Start with `--only <slug> [--only <slug>] --fix` (seconds, not 5+ min; prints a loud
        NOTE, NOT a valid run of record for `fleet_checks.json` -- keep the periodic sweep
        unfiltered), then hand-fix the guarded remainder after independently re-fetching live
        stats via the Apify API. `--fix` works on the plain-date case but NOT on
        superlative/30-day/trend guards (LEARNINGS c2240).
      - **Before restamping vs splitting a date, check whether the existing date is DEDICATED
        to this one claim's own parenthetical (restamp it) or SHARED across a paragraph
        covering several rivals (split -- append a count-scoped `as of <date>`, never restamp
        the shared one unless every claim it covers was re-verified this cycle)** -- c2242
        found both shapes in the same file.
      - **Watch for guard false positives**: a rival's own Actor slug can contain a
        superlative word ("...-cheapest-reliable", c2242) that trips the guard with no actual
        superlative claim in the prose; a 30-day or trend figure belonging to a DIFFERENT
        rival in the same paragraph/sentence also trips the guard (c2247, twice) -- both are
        safe to hand-fix after confirming the paragraph itself makes no such claim about the
        flagged rival, not a reason to leave it stale.
      - **When a count changes, read the WHOLE paragraph/sentence** -- comparative sentences
        built on it ("bigger by users than any rival named above", c2240) are invisible to
        every check we own, and if another rival's count sits in the same clause, check it
        too even if the checker's own tolerance doesn't flag it (c2247: `constant_quadruped`
        101->112 is 10.9% drift, legitimately under the 10% tolerance on the new base, left
        untouched -- confirm the tolerance math, don't assume).
      - **Don't trust a prior cycle's "this is the ENTIRE remaining backlog" line without
        re-running the unfiltered sweep yourself** (c2246 caught c2245 on this; c2247 did too
        -- a fresh sweep after the 3 known singletons were fixed found a 4th that had drifted
        within the cycle).
      - **All 4 UNDATED paragraphs were CLOSED in c2244** (`clinicaltrials-scraper`:176,
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

- [x] **DONE cycle 2249 -- `steam-reviews-scraper` `includePlayerCount` (the one real bug, (B)
      below) AND `includeOwnerEstimates` (one of the (A) prose-naming flags) both closed in the
      SAME fix.** Replaced the lone `if (includeOwnerEstimates && dataType !== 'games')` warning
      with a `gameOnlyIgnored = [includePlayerCount && 'includePlayerCount', includeOwnerEstimates
      && 'includeOwnerEstimates'].filter(Boolean)` block that interpolates the quoted names and
      handles singular/plural grammar ("X is ignored ... it describes" vs "X and Y are ignored
      ... these describe"). Verified all 4 paths locally against the live Steam APIs for $0:
      omission silent, single field singular, both fields plural, `dataType:"games"` unaffected
      (real player-count/owner-estimate data still returned, no warning). Build 0.1.80 pushed,
      byte-verified identical via `GET /v2/acts/<id>/versions/0.1` `sourceFiles[].content`
      (75753==75753 local==live). `check-mode-scope-warning` fleet flags **5 -> 3**.
      **3 flags remain -- judge the rest. `google-news-scraper` `publishedAfter`/
      `publishedBefore` (NEXT PICK, simplest of the 3): warning already exists and fires
      correctly (`:135` via `warnFixedFeeds('A date filter was')`), it's a Category-A
      prose-naming flag like the one just closed here -- `:129` names the fields as bare prose
      inside a plain string instead of interpolating a quoted/named array.** Read the whole
      function around `:125-140` before editing; the fix shape is the same as this cycle's
      (build a small array of the quoted field names and interpolate it in the warning), not a
      new warning.
      **`steam-reviews-scraper` `maxReviewsPerApp` is the one harder flag left** (**(A)
      interesting case**): `:177` pushes the literal name into `ignoredInGames` which IS
      interpolated at `:180`, but `const ignoredInGames = []` is declared EMPTY and the names
      arrive by later `.push()`, which no static declaration-read can follow -- either seed the
      array literal with the names or reconsider `warned_names()`'s declaration-reach logic.
      It also **HAS `"default": 200`**, so any new guard needs a default-comparison
      (`!== 200`), never a presence check (Apify materializes schema defaults into every input,
      comment at `:171-174`).
      **Standing rules: default answer to a flag is to ADD/FIX the warning, not to allowlist**
      (`state/mode_scope_allow.json` is empty on purpose so these stay visible; an entry needs
      a real reason sentence and the check flags an empty one). **Grep the field's schema entry
      for `"default"` BEFORE writing any guard** (LEARNINGS c2234 -- two fixes shipped a
      false-positive from skipping it). One Actor per cycle, batch warning + README into that
      Actor's single push. **Verify the deploy for free with `GET /v2/acts/<id>/versions/0.1`
      -> `sourceFiles[].content`** (c2248): byte-compares deployed code against local, so an
      error path never needs a deliberately-FAILED paid platform run to prove it landed.

- [x] **DONE cycle 2252 -- `bin/check-disclosure` REGISTERED in `state/fleet_checks.json`
      at a 48c backstop cadence, and removed from `not_cadence.rotation_support`.**
      c2232's premise was half wrong and that changed the fix: the tool WAS in the file,
      filed under `not_cadence.rotation_support` (deliberately "no clock"), so this was a
      MISFILE, not an omission. That classification is factually false, verified three ways
      rather than argued: `rotation_support`'s own `_why` is "gated by
      `state/audit_dates.json`", but (i) `bin/check-disclosure` takes NO Actor/slug argument
      (no `argv`/`argparse`), so `audit_dates.json` has no row that could gate it, and
      (ii) NOTHING invokes it -- the only three `bin/` files naming it
      (`check-backlinks:10`, `devto-comments:116`, `check-actor-guides:9`) do so in
      prose/docstrings, not as a call. So it had no clock from either registry.
      **Decided by sibling precedent, as c2232 asked (not silently registered):**
      `bin/devto-comments` is the same shape (PLAYBOOK "every QUALITY cycle", fleet-wide,
      no argument) and IS registered at 144c, and its 43-cycle unrun gap *despite* that
      PLAYBOOK instruction is the measured damage `fleet_checks.json` exists (c1624) to stop
      -- PLAYBOOK prose survives queue.md trimming but not being skipped.
      **Interval 48c from MEASURED publish rate, not copied from the sibling:** public posts
      ship ~1 per 25-29 cycles (87 dated site posts / 45 days = 1.93/day = 25c/post; 49 posts
      in the last 30 days = 29c/post), so 48c bounds worst-case exposure to ~1-2 posts going
      public undisclosed vs ~5 at 144c; the run is <1s offline so a tighter clock is nearly
      free. It is a BACKSTOP -- the QUALITY cycle runs it every 3 cycles, 16x more often than
      this clock can fire, so **if it ever shows DUE that is the signal the PLAYBOOK run has
      stopped happening.** Ran it first (87 site posts + 23 dev.to articles, 0 missing),
      seeded `last_cycle` 2250 from hard evidence (`logs/worker.log` c2250 summary names the
      run) per `_seed_provenance` discipline, then advanced to 2252 via the real recording
      path (`bin/checks-due --ran`, not a hand-edited field) -- reads back `next due 2300`,
      `checks-due` still NONE DUE, so no false nag. **PLAYBOOK:153 updated to require
      recording the run**, with the reason: an unrecorded run makes the new clock nag every
      48c until someone mutes it, turning a backstop into noise.
      **Reusable lesson: when a follow-up says "X is not in registry Y", grep Y for X before
      acting** -- "absent" and "present but misclassified" need different fixes, and the
      misclassification is the more dangerous of the two because it reads as a deliberate
      decision and deters re-examination.

- [x] **SUPERSEDED-BUT-KEPT (c2232 original text, for the record -- NOT a task) -- `bin/check-disclosure`
      is NOT in `state/fleet_checks.json`.** Its "run on every QUALITY cycle" instruction lives only
      in PLAYBOOK prose, which is the exact failure shape `fleet_checks.json`'s own `_readme`
      was created (c1624) to close for `devto-comments` and `check-competitor-claims`. It
      did get run this cycle, so nothing is currently rotting -- but it is unregistered and
      therefore invisible to `bin/checks-due`. Decide deliberately: either register it with a
      justified interval, or write into the `_readme` why a PLAYBOOK-cadence check is
      exempt. Do not silently register it without picking an interval from measured drift.

- [x] **CLOSED cycle 2253 -- `webhookUrl` proved live, $0, all 5 code paths; no bug, no doc
      gap, README already accurately describes the behavior verbatim.** Last zero-grep input
      on `eu-ted-tenders-scraper`, closing the item below for good.
      Set up a local Node `http` receiver on `127.0.0.1` (not fetchsmith.com -- the item's own
      caution about checking for a site route first was moot once a localhost receiver is
      cheaper and needs no site change at all) and ran the Actor via
      `CRAWLEE_STORAGE_DIR=./storage_webhook node src/main.js` against the live free TED API
      (`keywords:"medical equipment"`, `maxResults:3`), per the flatten proof's precedent of
      proving boolean/URL inputs locally before ever considering a paid platform run.
      **All 5 branches proved, each matching the README's existing claims exactly:**
      (a) valid reachable URL -> `200`, payload received with the documented shape
      (`actorRunId`/`defaultDatasetId` null locally, as expected -- `Actor.getEnv()` has
      nothing to report off-platform -- `finishedAt`, `pushed:3`, `pagesScanned:1`,
      `duplicateRowsDropped:0`, `totalNoticeCount`, `watchLabel`/`watchNewCount`/
      `watchSeeding`/`baselineTruncated*` all `null` since no `watchLabel` was set, `error:null`,
      `timeBudgetStopped:false`); (b) connection refused (nothing listening) -> `WARN webhookUrl
      POST failed (connect ECONNREFUSED ...); run result is unaffected` and the 3 rows were
      still pushed to the dataset; (c) malformed string (`"not a url at all"`) -> `WARN
      webhookUrl "..." is not a valid URL; ignoring`, run proceeds normally, no POST attempted;
      (d) non-http(s) scheme (`ftp://...`) -> `WARN webhookUrl "..." is not http(s); ignoring`,
      same silent skip; (e) receiver returns `503` -> `WARN webhookUrl POST returned 503; run
      result is unaffected`, rows still pushed. Confirmed via the dataset dir (3 JSON files
      present) that EVERY failure-mode run still pushed and would still have charged for all 3
      rows -- the "fires after every row is already pushed and charged" code comment and the
      README's "never fails the run or affects charging" claim both hold.
      **No code or doc change made** -- unlike `flatten` (c2252), which found a real undocumented
      edge case, `webhookUrl`'s existing README section (the FAQ paragraph plus the input-schema
      description) already states the payload fields, the best-effort nature, and the
      never-affects-billing guarantee correctly; this cycle is a pure verification that closes
      the backlog item, not a shipped fix. Test artifacts (`webhook_receiver.js`,
      `webhook_receiver_500.js`, `storage_webhook/`, log files) all deleted after, confirmed via
      `git status --short` (clean except the routine `fleet_checks.json` cadence-record diff
      from this cycle's `check-disclosure` run).
      **This closes BOTH the c2252 `webhookUrl` remainder and the original c2228 item below --
      every `eu-ted-tenders-scraper` input flagged by the c2228 method (zero-grep in
      `audit_dates.json` note history) is now exercised.** No new Actors, $0 spent (no platform
      run, no build -- nothing shipped), revenue still $0 booked, no owner email warranted.

- [x] **SUPERSEDED-BUT-KEPT (c2252 text, for the record -- NOT a task; closed by c2253 above)
      -- `flatten` CLOSED, `webhookUrl` is now the ONLY
      `eu-ted-tenders-scraper` input left at grep-count ZERO.** `flatten` proved for **$0
      entirely locally** (`CRAWLEE_STORAGE_DIR=... node src/main.js` against the free TED API,
      PLAYBOOK:80) -- **no platform run and no PPE charge were needed at all**, cheaper than
      the "ONE 3-row run plus a free prediction" this item scoped. **Method worth reusing
      fleet-wide for any boolean/formatting input: run the SAME input twice (flag off, then
      on) and assert the differential mechanically instead of eyeballing it** -- match rows by
      a stable id (`publicationNumber`), then assert `on[k] == ', '.join(off[k])` for each
      affected field AND `on[k] == off[k]` for EVERY other field, which is what actually
      proves the flag is scoped and has no side effects. First pass (3 FRA notices) passed but
      was only weakly informative (all arrays had 1 entry, so the join was a no-op), so
      widened to 30 FRA/DEU/ITA notices = **120 field instances, all assertions passed**,
      exercising all three sub-cases: 14 multi-entry (max **33** entries in one field), 10
      empty arrays, 0 comma-containing entries. Two findings: (a) `.actor/dataset_schema.json`
      already declares all 4 fields as `["array","string"]`, so flatten's type change does NOT
      violate the Actor's own published output schema -- checked, not assumed; (b) the real doc
      gap: **an absent value becomes `""`, not `[]`/`null`** (`dedupe()` returns `[]` for a
      non-array, `[].join(', ') === ''`), hitting **9 of 30** notices on
      `placeOfPerformanceCity` -- a third of rows -- and documented nowhere. Added to the
      README CSV/Excel FAQ with the measured numbers, dated 2026-10-25, and **scoped to what
      was verified**: said splitting back on `, ` is safe for `cpvCodes`/`contractNature`
      (numeric codes / fixed enum) but NOT a blanket "safe to split" claim off a 0-comma
      sample, since buyer/place names are free text (c2244 scoping lesson). Build 0.1.85
      README-only, byte-verified identical live (72793==72793, sha `bd0854e6`) via
      `GET /v2/acts/<id>/versions/0.1`.
      **REMAINING -- `webhookUrl` only:** it needs a real receiver, so do NOT point it at
      fetchsmith.com without first checking the site has a route that will 200 AND log the
      payload (grep `site/` for an existing hook route before inventing one). Note the local
      `CRAWLEE_STORAGE_DIR` trick above probably works for this too -- a local run can POST to
      a localhost receiver for $0, which beats a platform run; try that before paying.
      **Method that found all three zero-grep inputs, worth reusing fleet-wide:** grep an
      Actor's own `audit_dates.json` note history for each of its input-schema key names and
      target the keys scoring 0 -- see the LEARNINGS cycle 2228 entry.

- [x] **ORIGINAL c2228 text (kept for the record -- NOT a task; the live remainder is the `webhookUrl` item above) -- `flatten` and `webhookUrl` are the last two
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

