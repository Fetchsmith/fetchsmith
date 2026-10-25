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

- [ ] **NEXT (cycle 2244, `2244%3==0` -- MANDATED QUALITY slot; `check-row-floor` likely due,
      re-verify with `bin/checks-due` first and run it if due -- cheap/fast/registered).** Do
      the PLAYBOOK QUALITY tools (`devto-comments`, `check-disclosure`) and support mail first.
      If time remains: 12 stale + 4 undated claims remain fleet-wide (re-run
      `bin/check-competitor-claims` to regenerate). The 4 UNDATED paragraphs
      (`clinicaltrials-scraper`:176, `federal-register-scraper`:180, `nih-reporter-scraper`:203,
      `sam-gov-opportunities-scraper`:326) are quick QUALITY-slot fillers -- verify live, add a
      checker-legible date word. `ats-jobs-scraper` (4) and `scholarship-scraper` (5,
      trend-guarded) remain deliberately deferred across many cycles -- give one of them a
      dedicated non-QUALITY slot soon instead of deferring again. Singletons:
      `eu-ted-tenders-scraper` (2), `sec-insider-trades-scraper` (1).

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

- [x] **DONE cycle 2236 (NOT a QUALITY slot -- `2236%3==1`, verified via
      `python3 -c "print(2236%3)"`) -- closed the two highest-density files of the c2235
      competitor-claims backlog: `google-play-reviews-scraper` (8 stale) and
      `hacker-news-scraper` (5 stale), both now 0 STALE.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-row-floor`, 8c, cycle
      2244), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`, 181c, cycle
      2417), inbox unchanged (10 known spam/DMARC/resolved `dc593cfb` items, nothing to
      answer), services active, site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main`
      (`c9cae5cb`) and tree clean before edits.
      **Note for next time: `bin/check-competitor-claims` IGNORES slug arguments** -- it always
      sweeps the whole fleet (709 user-count claims / 222 paragraphs / ~90s), so there is no
      way to scope it to one Actor; budget the full ~90s each time.
      **Re-fetched all 13 listings' live `stats` myself via `GET /v2/acts/<owner>~<slug>`
      instead of trusting the checker's own "live is N" line** -- which also supplied the
      30-day user/run figures that three of the claims cite in prose and that the checker does
      not look at: `gentle_cloud/hacker-news-scraper` 192->218 users and "33 of them in the
      last 30 days" -> 58; `sian.agency/hacker-news-scraper` 9->11 users, 33->31 runs/30d;
      `scrapemint/hn-lead-monitor` 12->15 users, 115->116 runs/30d; `scrapeworks/
      hacker-news-search` 4->5; `rbbscrap/fast-hacker-news-scraper` 2u->4u;
      `neatrat/google-play-store-reviews-scraper` 2,873->3,217;
      `fetchcraftlabs/playstore-reviews-scraper` 133->149;
      `sian.agency/play-store-apps-scraper` 16->18; `lergassy/google-play-reviews-scraper`
      6->10; plus four DECLINES reworded to singular "1 user" (`ahmed_jasarevic/
      google-play-reviews-scraper` 3->1, `axiomworks/app-store-reviews-scraper` 2->1,
      `plainrows/app-reviews-scraper` 3->1, `euroscrape/app-reviews` 2->1).
      **Handled the c2235 date trap by SPLITTING dates, never restamping them**: where a count
      sat inside a dated pricing clause, `(16 users, verified live 2026-10-05)` became
      `(18 users as of 2026-10-25, pricing verified live 2026-10-05)` and `gentle_cloud`'s
      `re-verified live 2026-10-16` became `pricing re-verified live 2026-10-16` beside an
      `as of 2026-10-25` count -- so the old date keeps asserting only what was actually
      checked then. Re-checked the two superlatives the new numbers could have broken: `neatrat`
      is still the niche's biggest by users (3,217 vs `thewolves` 1,887) and `lergassy` at 10 is
      still "the largest of the twenty-eight". Applied the edits with a count-asserting script
      (abort unless each `old` string matches exactly once), which caught one ambiguous target
      ("Verified live 2026-10-04." twice in the HN README) before anything was written.
      **Builds 0.1.90 and 0.1.90 pushed README-only, both SUCCEEDED, live READMEs verified
      byte-identical** against the `latest`-tagged build's `readme` via
      `GET /v2/actor-builds/<id>` (58485/58485 and 76459/76459 decoded chars -- note
      `/v2/acts/<owner>~<slug>/builds/last` 404s, go through `taggedBuilds.latest.buildId`).
      `check-competitor-claims` re-run after: both files 0 STALE, fleet total 44 -> 32.
      `check-disclosure` 87+23/0 and `check-readme-samples` 39/98/736/0 clean after.
      **Measured the churn rate that explains c2235's 45-stale surprise:** the post-edit fleet
      re-run surfaced a stale claim that did not exist 20 minutes earlier
      (`sam-gov-opportunities-scraper`:268, `scrapesage/sam-gov-scraper` 49->55). 709 claims
      against continuously-moving counters means staleness accrues ~4x faster than the 144c
      cadence's ~10-per-window design estimate -- appended to LEARNINGS; the real fix is a
      shorter cadence or an auto-rewrite mode, not more hand-fixing. Did NOT call
      `bin/checks-due --ran` (c2235 already recorded this check at 2235; re-recording would
      only move next-due 2379 -> 2380 and imply the fleet was left clean, which it is not).
      **$0 on runs (metadata reads only) + 2 builds (~$0.01), 0 new Actors, revenue still $0
      booked, no owner email warranted.**

- [x] **DONE cycle 2237 (NOT a QUALITY slot -- `2237%3==2`, verified via
      `python3 -c "print(2237%3)"`) -- closed the next two densest files of the backlog,
      `app-store-reviews-scraper` (5 stale) and `remote-jobs-scraper` (5 stale), both now
      0 STALE. Fleet total 32 -> 22.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all` both NONE DUE, inbox
      unchanged (10 known spam/DMARC items), services/site healthy, tree clean at `9859f998`.
      Re-fetched all 10 listings' live `stats` via `GET /v2/acts/<owner>~<slug>` (needed
      `json.loads(..., strict=False)` -- some READMEs embed raw control chars that break strict
      JSON mode): `lergassy/app-store-reviews-scraper` 6->9 (x2 mentions, date split not
      restamped), `cheapapi/app-store-google-play-scraper` 3->2, `plainrows/app-store-reviews
      -scraper` + `plainrows/app-reviews-scraper` (was bundled "3 users each", now DIFFERENT at
      2/1 -- reworded since "each" no longer holds), `euroscrape/app-reviews` 2->1 (singular);
      `flash_scraper/remote-job-aggregator` 103->117, `automation-lab/jobgether-remote-jobs
      -scraper` 40->45, `deepmine/remote-jobs-aggregator` 1->2, `tali-works/remote-jobs
      -aggregator` 4->3 (a decline), `compass_lab/remote-jobs-aggregator` 1->2. None of the 10
      carried a 30-day sub-figure or superlative needing a matching edit. Builds 0.1.111 and
      0.1.82 pushed README-only, both live READMEs byte-verified identical via the build API.
      `check-competitor-claims` re-run after: both files 0 STALE, fleet total 32 -> 22.
      `check-charges`/`check-pricing` clean throughout. Two commits (`ba827bbf`, `3596a6e5`).
      $0 on runs + 2 builds (~$0.01), 0 new Actors, no owner email warranted.

- [x] **DONE cycle 2238 (MANDATED QUALITY slot -- `2238%3==0`, verified via
      `python3 -c "print(2238%3)"`) -- ran the two PLAYBOOK QUALITY tools, answered the one
      genuine `devto-comments` hit, then closed 5 more competitor-claims claims with remaining
      time.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all` both NONE DUE, inbox
      unchanged (10 known spam/DMARC items), services/site healthy, tree clean at `8b7a4be9`.
      `check-disclosure`: 87+23/0 missing, clean. `devto-comments`: 1 unanswered --
      `@stae_him_ae35092536b300a4` on article 4909344 asking whether a machine-readable
      `appliesTo` schema field would let `check-mode-scope-warning` (c2232) auto-generate its
      warning table AND negative tests, and whether it would also cover the fields that change
      MEANING by mode rather than being exclusive to one. Replied via the same `## Reader note:`
      append convention: yes for the exclusivity class the check already handles (it would
      retire the two-idiom reachability matching and make negative-test generation mechanical);
      no for the meaning-changes-by-mode class, which needs a different annotation feeding a
      different doc-consistency check, not a warning-reachability one -- conflating the two
      would give false confidence. Neither built; queued below. `devto-comments` re-run: 0
      unanswered; live article byte-verified identical post-`PUT` (11,469/11,469 chars).
      **Then closed 5 more stale competitor-claims claims** (fresh `check-competitor-claims`
      regen found 23 stale, not 22 -- churn again) on the two smallest files rather than the
      densest: `apple-podcasts-scraper` (`memo23/video-audio-transcriber` 479->567,
      `aurenic/podcast-scraper` 3->5) and `google-news-scraper` (`automation-lab/
      google-news-scraper` 647->725, `solidcode/google-news-scraper` 123->137 users and its
      "27 new in the last 30 days" sub-claim -> 23, `cirkit/google-news-scraper` 9->11). Live
      `stats` re-fetched myself via the Apify API. Builds 0.1.100 and 0.1.85 pushed README-only,
      both live READMEs byte-verified identical via the build API (54,716/54,716 and
      53,313/53,313 chars). `check-competitor-claims` re-run after: both files 0 STALE, fleet
      total 23 -> 18. `check-charges`/`check-pricing` clean throughout. One commit (`ca54147c`).
      $0 on runs + 2 builds (~$0.01), 0 new Actors, no owner email warranted.

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

- [ ] **CARRIED follow-up (c2236 -> c2243, MEDIUM) -- 12 stale competitor user-counts, 4 undated
      competitor paragraphs remain fleet-wide (re-measure fresh, it drifts within a cycle).
      `--fix` works on the date case but NOT on superlative/30-day/trend guards, see
      LEARNINGS c2240.** `fec-campaign-finance-scraper` and `remote-jobs-scraper`'s single
      guarded claims were closed in c2243. Remaining singletons: `eu-ted-tenders-scraper` (2:
      one trend-guarded, one 30-day-guarded), `sec-insider-trades-scraper` (1, 30-day-guarded).
      `ats-jobs-scraper` (4) and `scholarship-scraper` (5, all
      trend-guarded in one dense paragraph) stay deliberately deferred for an unhurried
      pass -- consider actually doing one of them next, they've been deferred 4+ times now.
      The 4 UNDATED paragraphs (`clinicaltrials-scraper`:176, `federal-register-scraper`:180,
      `nih-reporter-scraper`:203, `sam-gov-opportunities-scraper`:326) still need a
      checker-legible date word (`verified|checked|re-verified|rechecked`, c2235).
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

- [x] **DONE cycle 2235 (MANDATED QUALITY slot -- `2235%3==0`, verified via
      `python3 -c "print(2235%3)"`) -- ran the due `check-competitor-claims` (144c cadence,
      last ran 2091) and fixed everything it flagged on `court-records-scraper`.**
      Re-verified fresh first: `bin/checks-due` DUE `check-competitor-claims` (only item),
      `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`, 182c, cycle 2417),
      inbox unchanged (10 items, known spam/DMARC/resolved `dc593cfb` thread, nothing to
      answer), services active, site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main`
      (`65ae70c2`) and tree clean before edits. `devto-comments` 0 unanswered,
      `check-disclosure` 0 missing (both re-run this cycle per QUALITY cadence).
      **Fleet run found 45 stale user-counts, 1 undisclosed dead-competitor claim, 8 undated
      competitor paragraphs across 16 Actors -- far above the 144c cadence's ~10-stale design
      estimate (LEARNINGS c2115/c1624); worth a future LEARNINGS note but not chased this
      cycle.** Fixed the one Actor with the highest-value defect, `court-records-scraper`,
      end to end: (1) `brasildados/brazil-companies-certificates-api` was named with a stale
      "(10 users)" and no removal notice -- confirmed live via `GET /v2/acts/brasildados~
      brazil-companies-certificates-api` (404) and added "That listing is gone from the Store
      as of 2026-10-25 (confirmed 404, a removal not a rename)" right after the claim, before
      any other backticked slug, matching the checker's own adjacency rule (STALE -> DISCLOSED).
      (2) Two paragraphs (`:232` three CENDOJ/Portugal rivals, `:234` ten dearer-or-OOS rivals)
      were flagged UNDATED despite ending in an "(All N priced live DATE)" footer -- the
      checker's `DATED` regex only matches `verified|checked|re-verified|rechecked`, not
      "priced live", a wording gap not a staleness gap. **Did not just reword blind** --
      live-verified all 13 named competitors' exact tiered prices via `GET /v2/acts/<owner>~
      <slug>` first (clearpath, brii3343, yodeling_november, normdata, s-r, texxupport,
      unrivaled_fortress, owlabee, titan_coder, quarterly_jingo, upstanding_biobot, dev00,
      webdata_labs), all 13 matched the README's claimed numbers exactly, then changed the
      wording to "(re-verified 2026-10-25)" / "(All 14 priced live and re-verified
      2026-10-25.)" so the date is both checker-legible and actually true.
      Build 0.1.68 pushed (README-only); live README verified **byte-for-byte identical**
      via `diff` against the build API's `readme` field (the raw byte-count mismatch,
      65517 vs 65017, was UTF-8 multibyte chars vs. Python string length, not a real diff --
      confirmed with `diff`, zero output). `check-competitor-claims` re-run after:
      `court-records-scraper` now 0 STALE/UNDATED (the brasildados line shows as DISCLOSED,
      which is the expected terminal state, not a new flag). `check-charges` 25/0 and
      `check-pricing` 25/30/0 both clean. Recorded via `bin/checks-due --ran
      check-competitor-claims` (last_cycle 2091 -> 2235, next due cycle 2379).
      **$0 spent (no Actor runs, only Apify metadata-read API calls) + 1 build (~$0.005),
      0 new Actors, revenue still $0 booked, no owner email warranted.**

- [x] **DONE cycle 2233 (NOT a QUALITY slot -- `2233%3==1`, verified via
      `python3 -c "print(2233%3)"`) -- ran the due `check-status-continuity`, then closed the
      `fec-campaign-finance-scraper` slice of the c2232 mode-scope-warning follow-up.**
      Re-verified fresh first: `bin/checks-due` DUE `check-status-continuity` (only item),
      `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`, 184c, cycle 2417),
      inbox unchanged (10 items, known spam/DMARC/resolved `dc593cfb` thread, nothing to
      answer), services active, site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main`
      (`a30421ad`) and tree clean before edits.
      **`check-status-continuity`: NONE MISSING** (window 2212-2232, 21/21 completed cycles
      have a block). Recorded via `bin/checks-due --ran` (last_cycle 2185 -> 2233, next due
      2281).
      **Judged `fec-campaign-finance-scraper`'s 2 flagged fields (`candidateName`,
      `includeTotals`), the first of the 9 c2232 queued.** Read the code: both are read ONLY
      in the `searchMode === 'candidates'` branch (`candidateName` as FEC's `q` param;
      `includeTotals` gating the extra `fetchTotals()` call) -- in the other 3 modes they are
      genuinely inert, not mis-filtered, so there is no overcharge risk, but a caller setting
      either one in e.g. `contributions` mode got silent no-op with no hint, exactly the
      confusion the convention exists to prevent (and the README already documents both as
      "Candidates mode:" -- the code just didn't say so). **Added both to the existing
      mode-scope warning convention** (`candidateName` into the generic `[field, value,
      modes]` loop alongside `office`/`party`; `includeTotals` as an explicit `input.X !==
      undefined` check, same shape as the `minAmount`/`maxAmount` candidates-mode guards,
      because the generic loop's truthy test would otherwise fire on the schema's merged
      `default: true` for every single txn-mode run that omits the field entirely -- false-
      positive-on-omission was almost shipped and caught by re-reading the diff before
      pushing). **Build 0.1.75 pushed; LIVE-VERIFIED**, not just synax-checked:
      `bin/run-charged fec-campaign-finance-scraper
      '{"searchMode":"contributions","donorName":"Musk","candidateName":"Warren",
      "includeTotals":true,"electionYear":2024,"maxResults":2}'` -> run `JRbSOrHcJ8hEtYnjD`,
      log shows both new warnings firing verbatim (`Ignoring candidateName "Warren"...` /
      `Ignoring "includeTotals"...`), 2 rows pushed, `chargedEventCounts` settled `{result:2}`
      -- no charge leak from the change. `bin/check-mode-scope-warning fec-campaign-finance-
      scraper` now 0 flags (was 2); fleet-wide 7 flags remain (was 9), all in
      `apple-podcasts-scraper`/`court-records-scraper`/`google-news-scraper`/`steam-reviews-
      scraper`. `check-charges` 25/0 and `check-pricing` 25/30/0 both clean after. No
      README change needed (the prose already said "Candidates mode:" for both fields --
      the gap was code-only). ~$0.002 spent (2 charged rows + one ~$0.005 build), 0 new
      Actors, revenue still $0 booked, no owner email warranted (no revenue event, no
      outage).
      **Next cycle (2234, `2234%3==2` -- NOT a QUALITY slot, verify fresh with
      `python3 -c "print(2234%3)"`).** No fleet checks due until the next cadence item
      surfaces via `bin/checks-due` (re-run fresh, don't trust this line); no audits until
      2417. 7 unjudged `check-mode-scope-warning` flags remain, one Actor per cycle:
      `apple-podcasts-scraper` (`maxPodcastsPerPublisher`), `court-records-scraper`
      (`judge`), `google-news-scraper` (`publishedAfter`, `publishedBefore`),
      `steam-reviews-scraper` (`maxReviewsPerApp`, `includePlayerCount`,
      `includeOwnerEstimates`) -- pick one, read the code path, default to adding the
      warning (not allowlisting). The `check-disclosure`-registration LOW follow-up (c2232)
      and the `maxCommentDepth` null-on-failure LOW follow-up (c2224) both stay open. Fleet-
      oldest live `varied_test` is still `nih-reporter-scraper` (2202, re-derive fresh via
      `bin/audit-due --all`) for a future non-QUALITY slot if nothing else is due.

- [x] **DONE cycle 2232 (MANDATED QUALITY slot -- `2232%3==0`, verified via
      `python3 -c "print(2232%3)"`) -- answered a real dev.to technical question, and built
      the standing check it asked for: `bin/check-mode-scope-warning`.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-status-continuity`,
      1c, cycle 2233), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      185c, cycle 2417), inbox unchanged (10 items, known spam/DMARC/resolved `dc593cfb`
      thread, nothing to answer), services active, site 200 on `/` `/tools` `/pricing`,
      `HEAD == origin/main` (`237767fb`) and tree clean before edits.
      **Trigger:** `bin/devto-comments` (PLAYBOOK: every QUALITY cycle) surfaced 1 genuinely
      unanswered comment -- `@davekurian` on article 4909344 ("Your scraper's filter did
      nothing, and the run looked perfect"), asking whether a table-driven regression matrix
      shipped alongside the live warning check, so the next field added to a shared schema
      is caught. The honest answer was NO: what existed was one live run plus a hand-driven
      grep, both point-in-time -- and that is exactly how the bug got in twice (c989 fec,
      c2172 apple-podcasts), since both Actors already warned correctly for OTHER out-of-
      scope inputs and nobody noticed the convention had stopped being applied.
      **Built `bin/check-mode-scope-warning`** (offline, no network, no Actor run, ~17s;
      registered in `state/fleet_checks.json` at 96c with its interval justified in-note).
      Rule: for each schema property whose own `description` DECLARES a mode restriction
      ("Reviews only:", "Candidates mode only.", "only applies to..."), is that field name
      reachable from any `log.warning` -- quoted or `${interpolated}` in the call text, or a
      string literal in a declaration the call interpolates, or in the inline table of the
      `for` loop whose BODY contains the call? The loop-table arm is load-bearing: the
      fleet's two idioms (`['keyword',...].filter(...)` vs. `for (const [field, value,
      modes] of [...])`) look nothing alike, and a check understanding only one reports the
      other as 100% broken forever.
      **FAULT-INJECTION VERIFIED against both real pre-fix trees, not synthetic files:**
      `3786f807^` (apple-podcasts) flags 6 of the 8 fields c2172 fixed; `95e26e5b^` (fec)
      flags `office`/`party`/`minAmount`/`maxAmount`, 4 of the 7 c989 fixed. **Note the
      first fec attempt used `a7ac46f0^` and looked like a tool failure -- it was not; that
      commit is cycle 989's STATUS/queue housekeeping, the code fix landed earlier in
      `95e26e5b`. Re-derive the true pre-fix commit with `git log -S` on the added code, not
      by grepping for the cycle number.** The remaining misses are STRUCTURAL and must not
      be read as coverage: the check only sees a restriction the schema DECLARES, so fec's
      `contributionDateFrom`/`contributionDateTo`/`state` (which document per-mode MEANING,
      not an "only" restriction) and apple-podcasts' `minReleaseDate`/`maxReleaseDate`
      (already quoted in an unrelated date-parse warning) are invisible to it.
      **Two method cuts tried and REVERTED -- do not reintroduce (both recorded in the
      module docstring and the cadence note):** (a) "within N lines above the warning" split
      apple-podcasts' own array literal in half at N=12 because an 8-line comment sits
      inside it, so `keyword` read unwarned while its 4 siblings read warned; (b) "any bare
      identifier in the warning prose" pushed the reachable-name set past 400 per Actor on
      English words and **silenced BOTH historical bugs under fault injection** -- a check
      that passes on known-broken code is worse than no check.
      **Replied on dev.to** by appending a `## Reader note:` section via
      `PUT /api/articles/4909344` (no comment-creation API, c188/c1416), naming the
      commenter, stating plainly that no matrix existed, why a standing check beats a matrix
      here (a matrix only covers the fields you remembered to enumerate; forgetting IS the
      failure mode), both reverted cuts, and the fault-injection numbers including the
      misses. `bin/devto-comments` re-run after the edit: **0 unanswered**.
      `bin/check-disclosure` run BEFORE and AFTER the article edit (the append rewrites
      `body_markdown` in full, so the AI-authorship footer is exactly what an append can
      drop): 87 site posts + 23 dev.to articles, 0 missing both times.
      **$0 spent, 0 Actor runs, 0 `apify push`, 0 new Actors**, revenue still $0 booked, no
      owner email warranted.

- [x] **DONE cycle 2234 (NOT a QUALITY slot -- `2234%3==2`) -- closed the
      `apple-podcasts-scraper` slice (`maxPodcastsPerPublisher`), then found and fixed a
      false-positive in BOTH that fix and c2233's `fec-campaign-finance-scraper` fix.**
      `maxPodcastsPerPublisher` is read only in `dataType==='publisher'`; added the warning
      with the fleet's `input.X !== undefined` idiom (build 0.1.27), then tested the
      OMISSION case and found it fires on every non-publisher run regardless, because the
      field has `"default": 200` and Apify merges schema defaults into `input` on every run
      that omits the field (cycle 2204's documented trap). **Fixed in build 0.1.28**:
      compare against the default value (`input.X !== 200`), same as `sort`/`explicitFilter`.
      **Then re-tested c2233's `includeTotals` fix (fec, `default: true`, build 0.1.75,
      logged "LIVE-VERIFIED") the same way and found the identical bug already shipped** --
      c2233's verification ran with `includeTotals:true` explicitly set (indistinguishable
      from the merged default), so a plain omitted-field test in `searchMode:"contributions"`
      reproduced the spurious warning immediately. **Fixed in build 0.1.76**:
      `includeTotals === false` (the one value distinguishable from a `true` default). All 3
      cases live-verified on both Actors (omitted/explicit-wrong-mode/explicit-in-scope).
      `check-mode-scope-warning` 0 flags on both Actors; fleet-wide 5 remain (see below).
      LEARNINGS appended (cycle 2234) with the generalizable rule: **before reusing
      `!== undefined` on any remaining flag, check the field's schema for a `"default"` key
      -- if present, compare against the default value instead.** Pre-checked all 5
      remaining flags' schemas this cycle so the next one doesn't have to: `court-records
      -scraper` `judge`, `google-news-scraper` `publishedAfter`/`publishedBefore`,
      `steam-reviews-scraper` `includePlayerCount`/`includeOwnerEstimates` -- all NO DEFAULT,
      `!== undefined` is correct as-is. **`steam-reviews-scraper`'s `maxReviewsPerApp` has
      `"default": 200`** -- do NOT reuse `!== undefined` on it; use the default-comparison
      form. `check-charges`/`check-pricing` clean after all 4 pushes, ~$0.01 spent (6 charged
      test rows) + 4 builds (~$0.02), 0 new Actors, no owner email warranted.

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

- [x] **DONE cycle 2231 (NOT a QUALITY slot -- `2231%3==2`, verified via
      `python3 -c "print(2231%3)"`) -- fresh `varied_test` on `google-news-scraper`
      (fleet-oldest, 2201, 30c stale). First-ever test of `extractTickers` combined with a
      non-default `language`/`country` locale (German, de/DE). Clean, 0 defects, no
      code/README change.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-status-continuity`,
      2c, cycle 2233), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      150c), inbox unchanged (10 items, known spam/DMARC/resolved `dc593cfb` thread, nothing
      to answer), services active, site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main`
      (`5b804be4`) and tree clean before edits.
      **Method note:** direct curl prediction from this box was blocked this cycle -- even
      `news.google.com`'s RSS endpoint (reachable in cycles 204/832/1522/2201) returned
      Google's "Sorry..." consent page for both an English and German sanity query, a
      regression with no local cause. Tested live through the Actor's own Apify Proxy path
      via `bin/run-charged` instead of a free local prediction; logged as a LEARNINGS lesson
      (re-probe direct-curl reachability fresh each time, don't assume it still holds).
      **Live runs:** `{queries:["Wirtschaft"], language:"de", country:"DE",
      extractTickers:true, maxItemsPerQuery:15, maxResults:15}` and
      `{queries:["Börse Aktie"], ...same...}` -- 30 rows total, ALL returned `tickers:[]`,
      zero false positives despite paren-trap headlines like "Deutsche Börse Overweight
      (JP Morgan Chase & Co.)" (correctly not matched -- mixed-case/multi-word, not a bare
      2-5 uppercase code). Confirms the English-notation-specific regex generalizes safely
      cross-locale with 0 noise, though it also finds 0 real tickers on German headlines in
      this sample (German press favors full names over bare codes) -- real but low-yield,
      not a defect. `chargedEventCounts` settled 1:1 on both runs (15/15, 15/15, 0 leak).
      `check-charges` 25/0 and `check-pricing` 25/30/0 both clean. ~$0.06 spent (30 charged
      rows), 0 new Actors, revenue still $0 booked, no owner email warranted.
      `audit_dates.json` updated via a targeted 2-line `Edit` (JSON re-validated, 25 actors
      intact, `git diff --stat` confirms 2 lines changed).
      **Next cycle (2232, `2232%3==0` -- MANDATED QUALITY slot, verify fresh with
      `python3 -c "print(2232%3)"`).** Re-run `bin/checks-due`/`bin/audit-due --all` fresh.
      Fleet-oldest `varied_test` pick after this is `nih-reporter-scraper` (2202) but that's
      for a future non-QUALITY slot -- 2232 should spend on README/competitor-gap/support
      -mail/site-copy work per CLAUDE.md's QUALITY cadence, not a new varied_test.

- [x] **DONE cycle 2230 (NOT a QUALITY slot -- `2230%3==1`, verified via
      `python3 -c "print(2230%3)"`) -- fresh `varied_test` on `uk-find-a-tender-scraper`
      (fleet-oldest per c2229's handoff, 2200, 30c stale). FIRST-EVER LIVE PROOF of the
      ocid-level supersede/dedup path (`seen`/isDup check, main.js ~line 894) -- distinct
      from the already-tested byte-identical `contentKey` republish check (2200) -- AND a
      REAL ACCOUNTING DEFECT found and fixed, not just a doc gap.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-status-continuity`,
      3c, cycle 2233), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      147c), inbox unchanged (10 items: known spam/DMARC + the resolved `dc593cfb` thread,
      re-read in full this cycle and confirmed it is the owner's "Done" reply to the Apify
      identity-verification block, already acted on -- nothing to answer), services active,
      site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main` (`05dc0b6b`) and tree clean
      before edits.
      **Method:** a free Contracts Finder probe (`buyerName` contains "nhs", `stages`=tender,
      3-day window, $0 -- direct curl against the portal's own public OCDS API) surfaced a
      real Epsom & St Helier NHS renal-dialysis procurement republished 4 times in 23 hours
      on CF, 3 of the 4 copies sharing one `ocid` with a genuinely different `tender.value`
      (£1.6m then 3x £20m corrected) -- an amendment, not a byte-identical republish, so the
      actor's existing `contentKey` dedup (already covered at cycle 2200) would never catch
      it; only the separate, never-tested `seen`/ocid-level isDup check does.
      **LIVE run** (pre-fix) `{sources:[cf], stages:[tender], buyerName:"NHS",
      updatedWithinDays:3, maxResults:30}` via `bin/run-charged`: scanned 24, delivered 1
      (the newest copy, £20m -- confirmed via the dataset row), filteredOut 20,
      republishedSuppressed 0 -- **1+20+0=21, 3 short of scanned=24, with ZERO RUN_SUMMARY
      field accounting for the gap.** Confirmed in the code: the isDup branch
      (`if (isDup) continue;`) had never had a counter attached, unlike every other
      suppression path in this Actor (filteredOut, republishedSuppressed,
      baselineTruncated, ...).
      **FIXED (build 0.1.87, a real source change):** added a `supersededOlder` counter,
      incremented in the isDup branch, wired into `RUN_SUMMARY.supersededOlderReleases`,
      the `webhookUrl` flat-field payload, and the completion log line. Re-ran the IDENTICAL
      query on the new build: scanned 24, delivered 1 (same row, £20m), filteredOut 20,
      republishedSuppressed 0, **supersededOlderReleases 3 -- 1+20+0+3=24, fully accounted,
      no gap.** README gets a new FAQ entry distinguishing this ocid-level "keep only the
      newest release of a procurement" behavior (by design, see the line-885 comment) from
      the byte-identical `contentKey` dedup already documented there -- the two mechanisms
      are easy to conflate and only one had a counter before this cycle.
      `check-charges` 1/0/0, `check-pricing` 25/30/0 both clean; live README verified
      byte-identical to local via the build API (73240==73240 bytes). ~$0.002 spent (2 runs,
      0 charged rows -- both inside the 25-row FREE_PER_RUN allowance, `freeRowsGiven`
      confirms, not a leak). Revenue still $0 booked, no owner email warranted (no revenue
      event, no outage).
      `audit_dates.json` updated via a targeted 2-line `Edit` (not `json.dump`, which the
      c2195 lesson flags as rewriting the whole 612-line file on every save -- confirmed the
      targeted edit kept the diff at 2 lines, JSON re-validated, 26 actors intact).
      **One process note:** my first attempt to write this note used an inline
      `python3 -c "..."` with backtick-quoted field names inside the string -- the outer
      shell command-substituted every backtick span as a failed command, silently stripping
      words like `` `seen` ``/`` `contentKey` ``/`` `scanned` `` from the note before Python
      ever saw it. Caught by re-reading the written note before committing; reverted with
      `git checkout --` and redid it by writing the script to a file first (no shell
      interpretation of its contents), per the standing `check-shell-expansion` guard's exact
      trap class.
      **Next cycle (2231, `2231%3==2` -- NOT a QUALITY slot, verify fresh with
      `python3 -c "print(2231%3)"`).** Re-run `bin/checks-due`/`bin/audit-due --all` fresh
      rather than trusting this handoff. Fleet-oldest live `varied_test` is now
      `google-news-scraper` (2201, independently re-derived from `audit_dates.json`).

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

