- [ ] **NEW STANDING WATCH (c2664, LOW today -- re-read on any cycle that is about to call a
      runs30d deviation "demand") -- `eu-ted-tenders-scraper`'s +15-runs/5-day step is ONE caller
      ramping, not discovery; re-check the distinct-user counts before anyone acts on it.**
      Measured c2664: series oscillated 26<->27 daily 10-23..10-29 (the steady-state shape), then
      27 -> 28 (10-29 15:30Z) -> 33 (10-30 09:00Z) -> 37 (11-02) -> **42 (11-03)**, all SUCCEEDED,
      0 failed -- sustained, not a blip. **But `stats.totalUsers7Days` = `totalUsers30Days` =
      `totalUsers90Days` = exactly `1`**, so no new user arrived; nothing about Store ranking, SEO
      or discovery is measured by it, and it does NOT license listing-copy edits (c1468/c2280
      trap). **The trigger that WOULD be real news: those windowed distinct-user counts rising
      above 1, or a bookmark/review appearing** -- `bin/usage-trend` does not print them, so read
      `stats` off `GET /v2/acts/<id>` directly. Both halves of the c2168 burst protocol came back
      healthy this cycle (charge path reached; ~23.6x net margin), so there is nothing to fix --
      this item exists only to stop the number being re-misread as traction.

- [x] **DONE cycle 2667 -- `google-news-scraper` varied_test (the item c2666 left OPEN below).**
      Picked the leak-protection candidate (the other named candidate, `topics`/`topicsHashed`,
      stays open for a future varied_test slot -- not re-queued separately since `audit-due` will
      naturally re-surface this Actor in ~336c and either candidate is still valid then). Ran live
      via `bin/run-charged`: `publishedAfter:"2026-09-01"`, `publishedBefore:"2026-09-10"`,
      `excludeSites:["pinterest.com"]`, `queries:["artificial intelligence"]`,
      `maxItemsPerQuery:50`, `maxResults:50` (run `W3jSYB5d7MsWvJ1WK`) -- the exact c788 bug
      shape (explicit date window + excludeSites), never before driven through the real Actor by
      a varied_test (c788/c933 only direct-curl'd Google). Result: 46 rows pushed, all
      `publishedAt` within 2026-09-01..09-10 (inside the documented tolerance), statusMessage
      correctly reported "Dropped 4 article(s) that Google returned well outside your
      publishedAfter/publishedBefore window ... you were not charged for them", and
      `chargedEventCounts` settled `{result:46}` -- exactly the pushed count, so the 4 leaked
      rows were genuinely uncharged (no over- or under-billing). Backstop verified working
      end-to-end on current code, 0 defects, no code change. `check-charges` 25/25 clean,
      `actor-health --only google-news-scraper` ok. Recorded in `state/audit_dates.json`
      (`varied_test: 2667`). `audit-due --type varied_test --all` now reads **0 DUE across all
      25 Actors** -- the backlog c2666 found is fully closed. ~$0.083 spent (46 charged rows).

- [x] **DONE cycle 2668 -- the c2666 fleet-wide sweep for the "fixed order decides between
      populated candidates" bug class. Found and fixed exactly ONE more instance
      (`app-store-reviews-scraper`, build 0.1.121); the rest of the fleet is genuinely clean.**
      Method matters and is written up in LEARNINGS cycle 2668: the keyword grep
      (`auto.?detect|fetchAuto|firstNonEmpty`) hits ONLY `ats-jobs-scraper` and would have closed
      this item as "nothing found" -- the class is structural, so the real sweep is "wherever
      several POPULATED candidates get reduced to one by `.find()`/`break`/`[0]`, ask what decides
      the winner". Audited every such site in all 25 `src/main.js`. Verdicts: SAFE/one-ranked-source
      `google-play-reviews-scraper:539` (Google Play's own relevance order -- order *within* one
      upstream ranking is real signal, do NOT "fix" it); SAFE/refuses-to-guess
      `sam-gov-opportunities-scraper:1504-1509` (agency-key collision -> both `null`) and
      `sec-insider-trades-scraper:356` (`length === 1` or nothing) -- these are the pattern to copy
      when no quality signal exists; everything else is transient-failure retry or enum
      normalisation, not candidate selection. **BROKEN: `app-store-reviews-scraper.resolveAppName`**
      -- built `results = [...iosHits, ...macHits]` then `find(exactTitle) ||
      find(anyTokenSubstringAnywhere)`, so iOS-concatenated-first decided between two equally
      "relevant" populated candidates. Two wrong answers proved live with FREE
      `itunes.apple.com/search` probes (no Actor run): (1) `"sketch app"` + `includeMacApps:true`
      -> iOS "Sketchbook®" (substring hit) beat the real Mac "Sketch" (word hit); (2)
      `"affinity photo"` -> "Canva AI Photo & Video Editor", silently, on the generic token `photo`
      alone, and the caller was then CHARGED for Canva's reviews -- while the function's own warning
      string had promised for years that "an unrelated top hit is treated as no match rather than
      guessed". **Fixed** with a scored scan (5 exact title / 4 all tokens as whole words in title /
      3 all tokens anywhere / 2 partial-but-whole-word / 1 partial substring), best tier wins and
      list order survives only as the tie-break WITHIN a tier, plus a coverage gate (multi-token
      query, candidate matching < half the query's token chars -> score 0) and a warning that now
      names what actually matched. **Verified by OLD-vs-NEW diff on live payloads** (edited block
      sliced straight out of `src/main.js` into a throwaway harness, 17 names x {iOS-only, +Mac} =
      34 outcomes): 2 fixed, 31 byte-identical, 1 incidental wash. Then live on platform (run
      `GvHuRPNAEZH9N0Qa9`): `"sketch app"` -> `Sketch (id 1667260533) in the Mac App Store`,
      `"affinity photo"` -> the new honest NO-match warning naming `matched only "photo"`. 5 rows,
      `chargedEventCounts {result:0}` -- CORRECT, not a leak: `FREE_REVIEWS_PER_RUN = 10`
      (`src/main.js:387`) makes the first 10 reviews of every run free. Post-push `check-charges`
      25/25 clean, `actor-health --only app-store-reviews-scraper` ok (201, 10 items, 0 fail_rows).
      No output-field change, so `check-registry-fields`/`check-meta-fields` are not triggered, and
      `test_input.json` is untouched so `exampleRunInput` cannot have drifted.

- [ ] **NEW follow-up (c2668, LOW -- genuinely optional, do NOT spend a cycle on it unless an
      `appNames` support question arrives).** The c2668 OLD-vs-NEW diff logged one incidental
      reshuffle: `"sketch app"` with `includeMacApps` OFF now resolves to "AR Drawing: Sketch &
      Paint" (tier 2, `sketch` as a whole word) instead of "Sketchbook®" (tier 1, substring). Both
      are the wrong app -- the real Sketch is Mac-only, so iOS-only has no correct answer and this
      is a wash, not a regression. It is recorded only so a future cycle reading the tier table
      does not re-discover it and assume a bug. The only principled improvement would be weighting
      Apple's own result rank into the tie-break *within* a tier, which is a real design question
      (rank is signal within one source, noise across two) and not worth a build on zero demand.

- [x] **DONE cycle 2666 (NORMAL slot, 2666 % 3 == 2 -- recomputed fresh, NOT the QUALITY slot
      c2665 guessed forward) -- `audit-due --type varied_test` found 2 Actors DUE
      (`ats-jobs-scraper`, `google-news-scraper`); ran the first end-to-end and it surfaced a real,
      previously-unknown defect instead of a clean no-op, which ate the full cycle.** Preflight
      first, all clean: `checks-due --all` NONE DUE (soonest `check-row-floor` in 10c, cycle 2676);
      `audit-due --all` showed exactly the one real backlog (`varied_test` on the 2 named Actors,
      all other types CLOSED or not due); `inbox list 10` same known 10 triaged items, zero new
      mail; `bin/revenue` $0 booked, 25 Actors, 48 users, 778 runs30d, `ext_bad30d` same 4 known
      events; `bin/apify-spend` $6.084/$85 (82.5% elapsed, projection $7.37); services + `/`,
      `/pricing`, `/tools`, `/tools/ats-jobs-scraper` all 200/active before and after.
      **Edge case picked for `ats-jobs-scraper`: auto-detect (`"ats":"auto"`) on a slug that is a
      genuinely POPULATED board on two different platforms at once** -- never isolated this way
      before (c2330's varied_test used a nonexistent-slug warning + happy path, not a same-slug
      cross-platform collision). Used the Actor's OWN `input_schema.json` default example
      (`slug:"ramp"`, documented there as the canonical Ashby case) with `ats` omitted: auto-detect
      resolved to **Greenhouse** instead -- a 1-posting junk/test board ("Copy of Chief Legal
      Officer"), confirmed live via a free, non-billable direct call to
      `boards-api.greenhouse.io/v1/boards/ramp/jobs` -- silently returning the WRONG company
      instead of the real Ramp (fintech) Ashby board (confirmed live via
      `api.ashbyhq.com/posting-api/job-board/ramp`, dozens of real postings). The run SUCCEEDED
      with plausible-looking output (a real title, a real location) and no warning at all.
      **Root cause:** `fetchAuto()` picked the first non-empty board in a fixed `AUTO_DETECT_ATS`
      priority order (Greenhouse first) rather than the largest non-empty board, so a small decoy
      beats a large real match whenever the decoy sits earlier in the priority list. **Fixed:**
      replaced the priority-order `.find()` with a `boardSize()`-max `reduce` over all non-empty
      candidates (fixed priority order kept only as the all-empty tie-break, unchanged). Pushed
      `ats-jobs-scraper` build **0.1.117** (~$0.005), re-ran the identical `auto:ramp` input live
      -- now returns real Ashby rows (Security Engineer, Mobile Engineer, etc.), `atsSource:ashby`
      confirmed. **Paired edge case in the same cycle** (per the established pattern of combining
      a never-tested edge case with a happy-path/second check):
      `employmentTypeKeyword:"contract"` on `auto:airbnb` (resolves to Greenhouse) + explicit
      `workday:okgov` in one run -- SUCCEEDED, `chargedEventCounts {job:0}` (correctly uncharged
      for 0 kept rows), per-board WARN logs named the exact reason on both platforms (Greenhouse:
      field not published at all; Workday: only "Full time"/"Part time" exposed), and the
      aggregate status message's "373 open posting(s)" matched the two boards' own 213+160 counts
      exactly. Post-push: `check-charges` 0 drift, `actor-health --only ats-jobs-scraper` 10/10
      clean. Full root-cause writeup + the generalizable lesson in `notes/LEARNINGS.md` (cycle
      2666 entry) and the LOW fleet-wide follow-up item above.
      **`google-news-scraper`'s varied_test stayed DUE — did not start it this cycle** (the
      ats-jobs-scraper investigation, fix, push and re-verification filled the time budget; see
      the OPEN item above for the next cycle's starting point, with 2 specific untested-edge-case
      candidates already named so it doesn't need to re-derive them).
      ~$0.005 spent (one build), $0 revenue change, no owner email (a reliability fix is not a
      revenue event and nothing here is owner-fixable).
      **Next cycle:** finish `google-news-scraper`'s varied_test (still DUE, gap now 336c+1 — it
      does not go stale, `audit-due` just keeps showing it DUE until run). Nothing fleet-wide is
      due until `check-row-floor`/`check-upstream-warnings` at ~cycle 2676. Recompute `cycle % 3`
      fresh rather than trusting any prior cycle's printed slot label (c2665 mislabeled 2666 as
      QUALITY; true value is 2666 % 3 == 2, NORMAL).

- [x] **DONE cycle 2665 (NORMAL slot, 2665 % 3 == 1) -- full independent preflight re-run, one
      real due check executed, one standing doubt about DMARC sample size resolved with no code
      change needed.** `checks-due --all` had exactly 1 DUE: ran `check-status-continuity` fresh
      (retained window 2647..2664, 17 completed cycles per `worker.log`, **NONE MISSING**),
      recorded via `checks-due --ran` (next due cycle 2713). `audit-due --all` FLEET ROTATIONS
      NONE DUE. Zero new mail (same 10 known triaged items), $0 revenue change (25 Actors, 48
      users, 778 runs30d, `ext_bad30d` same 4 known events), `apify-spend` $6.0667/$85 (82.5%
      elapsed, proj. $7.36), `actor-health` 24/24 green + `scholarship-scraper` still PAUSED/429
      as expected, `traffic` still no buyer-intent signal, services/site all 200/active before
      and after.
      **Then checked a nagging detail rather than re-stating the preflight prose: STATUS.md/
      queue.md have been citing "DMARC sample still only 2 reports" for many cycles, but the
      full (untruncated) inbox actually holds 22 `dmarc@fetchsmith.com` messages, not 2.** Read
      every one of the 22 directly (not through `inbox list 10`'s truncation) against
      `dmarc-report`'s own `attachments`-array selection logic: **only 2 of the 22
      (`af5d9f7d`, `202905fb`) carry an `attachments` array**; the other 20 have no
      `attachments` key, `text`, or `html` field at all -- confirmed these are relics of the
      pre-cycle-1626 receiver.py bug the tool's own docstring already documents ("every DMARC
      report unreadable" before the fix), and the raw body was never stored for them, so there
      is nothing recoverable. **Conclusion: the "2 reports" figure was correct all along, not
      stale** -- closed the doubt with evidence instead of leaving it to be re-wondered next
      cycle. Both real reports are 1-source/1-message/0-fail (`54.240.11.115`, SPF+DKIM pass),
      so `p=reject` stays parked per the standing c2371 guidance (needs more weekly drops).
      Also re-confirmed the Apify `/v2/store` 2026-11-15 item (below) has no action due today --
      its own note already says the next step is strictly post-deadline.
      No code change (nothing was broken), no owner email (closing an internal doubt is neither
      a revenue event nor owner-fixable). $0 spent.
      **Next cycle:** nothing fleet-wide due until ~cycle 2676 (`check-row-floor`/
      `check-upstream-warnings`); 2666 is a true QUALITY/GROWTH slot (2666 % 3 == 0, recompute
      fresh). If 2666 also reads clean, the best-queued real work is the c2464 `_batch_price_*.py`
      rung-for-rung port below -- but only once a `competitor_audit` for that niche actually
      comes due, per its own gating.

- [x] **DONE cycle 2664 (QUALITY/GROWTH slot, 2664 % 3 == 0 -- recomputed fresh per the c2659
      rule) -- spent the slot on the fleet's one live demand signal instead of re-running c2663's
      battery, as c2663 asked.** Preflight first, all clean: `checks-due --all` / `audit-due --all`
      NONE DUE (soonest `check-status-continuity` in 1c, cycle 2665); `inbox list 10` the same 10
      known triaged items, zero new mail, zero replies owed; `bin/revenue` $0 booked, 25 Actors, 48
      users, 778 runs30d, `ext_bad30d` still the same 4 known events; `bin/apify-spend` $6.0513/$85
      (82.4% elapsed, projection $7.34, far under the $25 trip-wire); `bin/actor-health` 24/24
      public Actors green, `scholarship-scraper` still PAUSED/429 (`cleared=False`, so the c2372
      bold.org gate has NOT opened -- the unpushed c2312 fix stays unpushed); `bin/traffic` still
      no /pricing or /tools buyer-intent signal, so the Polar trigger has not fired and was not
      raised; services active and `/`, `/pricing`, `/tools` 200 before and after.
      **Then did real work on the one deviation `bin/usage-trend` reports** (details in the standing
      watch above and in LEARNINGS c2664): established it is one caller ramping rather than
      traction via the windowed distinct-user counts, then ran the c2168 demand-burst protocol on
      it end-to-end. (a) **Charge path live-re-verified** with `bin/run-charged` -- 5 pushed, 5
      charged, settled, clean; charge-before-push shape (`main.js:441-445`) means a buyer charge
      limit cannot yield unpaid rows. Recorded as `charge_event_verified: 2664` in
      `state/audit_dates.json` (explicitly labelled a re-verification, since c2305 already closed
      the full 30-event matrix). (b) **Unit economics measured live for the first time on this
      Actor:** $0.0000508/row cost vs live-read $0.0015/result at 20% Apify margin -> $0.0012/row
      net, **~23.6x net / ~29.5x gross** (trademark-search was ~4x at c2168), so this traffic is no
      cost risk at any plausible scale. (c) Confirmed `RUN_SUMMARY: none (HTTP 404)` on this Actor
      is **deliberate** (`main.js:6-8` documents the absent framework), not a regression -- noted so
      it is not chased again. One paid Actor run, ~$0.00025, against the BUDGET.md "Apify platform
      usage above included credits" line ($120 allocated, ~$6 used). **Next cycle:**
      `check-status-continuity` is due at 2665 (run it); DMARC sample still only 2 reports so
      `p=reject` stays parked; growing-niches retry and niche-hunting both still gated (~2026-12-26);
      the `/v2/store` 2026-11-15 item needs its pre-deadline look in the next ~12 days.

- [x] **DONE cycle 2663 (NORMAL slot, 2663 % 3 == 2) -- independently re-ran every preflight
      check fresh (not just trusted c2662's prose) and confirmed, again, that nothing is
      actionable.** `bin/checks-due --all` / `bin/audit-due --all`: NONE DUE, soonest
      `check-status-continuity` in 2c (cycle 2665). `bin/inbox list 15`: same 15 known items,
      all previously triaged (cold-pitch/SEO/DMARC spam, `ba1bf931`/`06daa491`/`9d15ac17`
      tintgate.com repeats, `5ce80b92` `ransomedarcy0@gmail.com` already logged as spam) --
      zero new mail, zero replies owed. `bin/revenue`: $0 booked, 25 Actors, 48 users, 778
      runs30d, `ext_bad30d` still the same 4 known events (no new entry). `bin/apify-spend`:
      $6.0367/$85, flat, $0 spent this cycle. `bin/actor-health` (all 25, not a subset): 24/24
      public Actors green (`ok: True`, 0 fail_rows each), `scholarship-scraper` still PAUSED
      429 as expected (matches the c2372 bold.org gate -- not RECOVERED, no action). `bin/
      traffic`: still 0 pageviews signal on /pricing and /tools and no purchase-intent mail --
      the Polar-checkout trigger (>100 visits/day or buyer mail) has NOT fired, so per the
      owner's deferral, did not raise it. Services (`fetchsmith-web`, `fetchsmith-mail`,
      `caddy`) active, `/`, `/pricing`, `/tools` 200 before and after. `git status`: only
      volatile cache files (`state/health.json`, `state/revenue.json`,
      `state/revenue_history.json`) touched by the checks just run -- no substantive diff, no
      code change manufactured (c2524 rule: don't force a change when nothing is ready).
      **Next cycle:** same as c2662 said -- nothing fleet-wide due until `check-status-
      continuity` at 2665; DMARC sample still only 2 reports (unchanged, needs more weekly
      drops before revisiting `p=reject`); growing-niches retry still gated (c2654's "wait
      ~19 cycles," only 9 elapsed); niche-hunting gated to ~2026-12-26. If 2665 also reads
      clean, consider varying the verification mix further (e.g. `check-source-endpoints`
      cadence check, or a fresh competitor-feature scan on 1-2 Actors) rather than repeating
      the identical preflight battery every single cycle.

- [x] **DONE cycle 2661 (QUALITY/GROWTH slot, 2661 % 3 == 0) -- trimmed `tasks/queue.md`
      proactively, the TRIM SOON case `check-doc-size` flagged at c2660.** Preflight:
      `checks-due`/`audit-due` both NONE DUE, zero new mail (confirmed the 2 owner threads on
      the inbox list stay resolved: CourtListener token wired c2362, Apify `/v2/store` change
      hardened c2496), $0 revenue change, $0 spent, services/site all 200/active before and
      after. `check-doc-size` read `tasks/queue.md` TRIM SOON (83.7KB/917 lines, projected
      211KB by its next scheduled look) while `state/STATUS.md` stayed OK -- trimmed queue.md
      only. Ran the standing-hazard grep first over the 10 archive-bound DONE blocks (cycles
      2646, 2651-2659): clean, nothing needed rehoming (the c2646 AbortSignal campaign and the
      c2357 bare-throw/`Actor.fail()` campaign are both independently confirmed closed
      fleet-wide, so a stale "3 Actors remaining" note from an older STATUS.md passage is dead
      and was not carried forward). Wrote `bin/_trim2661q.py` (hoist-then-cut: keep every OPEN
      block + the newest DONE block by cycle number, archive the other 10 to
      `tasks/queue_archive.md`, asserts on block/cycle counts and line-count conservation so a
      structural surprise aborts instead of corrupting the file). Archived 379 lines (cycles
      2646, 2651-2659). **Verified**: `check-doc-size` now reads `OK tasks/queue.md 52.3KB 538
      lines ~28 cycles of headroom` (was TRIM SOON); the script's own conservation asserts
      passed; `queue_archive.md` grew by exactly the archived content. No Actor code touched,
      no build, no push beyond the doc commit. Full narrative in `state/STATUS.md` cycle-2661
      block.
      **Next cycle:** nothing fleet-wide due until `check-status-continuity` at 2665.
      `state/STATUS.md` is still OK (58.2KB, ~32c headroom) -- re-check `check-doc-size` fresh
      rather than assuming; no open AbortSignal/bare-throw follow-up remains anywhere in this
      file.

- [x] **DONE cycle 2660 (NORMAL slot, 2660 % 3 == 2 -- recomputed fresh from the integer per
      c2659's process finding) -- ran all 3 due fleet checks (all clean) and then the 2
      cadence-less QUALITY checkers, which surfaced and fixed one real doc-hygiene defect.**
      Preflight: `audit-due --all` FLEET ROTATIONS NONE DUE; `checks-due --all` 3 DUE. Zero new
      mail (same known 10 triaged), no owner email. `bin/revenue` $0 booked, 25 Actors, 48 users,
      775 runs30d, ext_bad30d 4 (same 3 long-known + already-fixed nih-reporter-scraper).
      `bin/apify-spend` $6.0352/$85, flat, $0 spent -- no build, no push. Services + `/`,
      `/pricing`, `/tools` 200/active before and after.
      **(a) The 3 due checks, all clean, all recorded via `checks-due --ran`:** `check-blog-cta`
      88 posts, 0 missing-CTA / 0 roundup-no-one-hop-path / 0 bad-slug / 0 dead internal link
      (2324 -> 2660, next 2996); `check-backlinks` 131 post(guide)-Actor pairs across 88 posts, 0
      missing, 0 unresolved (1988 -> 2660, next 3332); `check-actor-guides` 24 live Actors, 0
      flagged, every Actor clears the floor with room (min dedicated=2, min related=3;
      `ats-jobs-scraper` richest 12/15) (1988 -> 2660, next 3332).
      **(b) Leaned QUALITY-flavored per c2659's note on the silently-skipped c2658 QUALITY slot**
      and ran the two checkers with NO `checks-due` cadence (PLAYBOOK "every QUALITY cycle"):
      `check-code-fields` = **0 Actors with code-only field drift** fleet-wide (all remaining
      annotations are the known-benign soft/non-row-literal/FIELD_SUPPRESS classes);
      `check-source-bytes` = `692 files checked, 1 flagged`, and **the single fleet-wide hit was
      `notes/LEARNINGS.md:7318` itself** -- the c2655 note documenting the `gen-output-schema`
      soft-hyphen fix, which **quoted the offending artifact (`"U.S.<U+00AD>-based"`) with the raw
      U+00AD still embedded**. c2655 fixed the real bug correctly and then reintroduced the exact
      byte class it had purged, into the record of the fix.
      **Fixed rather than annotated, deliberately.** Checked the tool first: `check-source-bytes`
      is a plain byte scan over `TEXT_SUFFIXES` with **no allowlist/suppress mechanism** (grepped;
      only `SKIP_PARTS` for node_modules/.git/storage) and **no `checks-due` cadence** -- there is
      nowhere to record "intentional", so leaving it would make every future QUALITY cycle
      re-investigate the same self-referential flag while a genuinely new hit hid inside an
      already-normal-looking non-zero count. Rewrote the quote as the spelled-out escape
      `<U+00AD>` + a short inline note on why; meaning preserved exactly (an invisible char in a
      quotation conveyed nothing to a reader) and strictly more legible. **`check-source-bytes`
      now reads 0 flagged across 692 files.** No Actor code touched, nothing buyer-facing -> no
      build, no push needed (unlike c2655, whose instance was in a live `dataset_schema.json` and
      did require pushing `sam-gov-opportunities-scraper` 0.1.86).
      Appended the durable lesson to `notes/LEARNINGS.md` (verified the new note is itself clean
      -- it names codepoints, never pastes them): **when documenting a byte/codepoint finding
      anywhere under `/root/agent`, name the codepoint (`U+00AD`, `U+200B`, `\x00`), never paste
      the character**; general form, **a checker with no suppress list must be kept at a zero
      baseline because its only signal is the count, so any "known-benign" hit left in place
      silently spends that signal** (same reasoning as c2478's `RANK UNKNOWN`-vs-`NOT FOUND`).
      **Also confirmed so it is not re-opened early:** the c2478 Apify `/v2/store` item (deadline
      2026-11-15, 12 days out) needs nothing today -- code half done early at c2496, remaining
      half explicitly post-deadline, `store-anon-rank` next due ~c2744 (pre-change), expected
      reading `paging_ok: True` until the date.
      **For the next cycle:** nothing fleet-wide due for 5 cycles (`check-status-continuity`
      soonest ~2665). **Both cadence-less checkers are now at a clean zero baseline as of 2660 --
      any non-zero `check-source-bytes` count from here is a real new hit; do NOT re-derive the
      LEARNINGS self-flag.** 2661 % 3 == 0, so 2661 is a true QUALITY/GROWTH slot (recompute
      yourself anyway). Worth a look there: `check-doc-size` is not due until ~2676, but STATUS.md
      has grown 25.2KB (post-c2652-trim) -> ~53KB and queue.md 65.4KB -> ~79KB, so the doc-trim
      cadence may read TRIM SOON before its checker is scheduled.

- [ ] **NEW follow-up (c2644, LOW -- SAFE direction, do not rush) -- `vid` is unstable within a
      single session when the visitor's egress IP rotates, which makes `VERIFIED` UNDERCOUNT
      real humans.** Same c2644 sample, opposite direction to the overcount fixed above: one
      session's pageview came from `74.7.228.187` and its `out_click` 2 seconds later from
      `74.7.228.253` -- same /24, different /32, so `sha256(salt|day|ip|ua)` produced a
      DIFFERENT vid for one continuous visitor. Consequence: for anyone behind a rotating
      egress pool (corporate proxy, CGNAT, mobile carrier) the `/static/*` fetch can land under
      a different vid than the pageview, so `vid IN (SELECT vid FROM asset_hits)` -- the oldest
      and most load-bearing half of `VERIFIED` -- fails for a GENUINE human. **Why this is not
      urgent:** the bias is an undercount, so it cannot forge a Polar escalation; it can only
      hide real buyer intent. **Do NOT change `visitor_token()` to /24 granularity on this one
      observation** -- the only sample is a single OAI-SearchBot session (its UA carries
      `OAI-SearchBot/1.4` appended after a Chrome string, so it was correctly excluded anyway),
      i.e. there is as yet NO evidence a real human was undercounted. Cheap check for a future
      cycle once more `ip` data has accumulated: count distinct vids per (ip /24, day) where
      the UAs are IDENTICAL -- identical UA + same /24 + different /32 is the rotating-egress
      signature. Only if that shows a material number of human-looking sessions is it worth
      hashing the /24 instead of the /32 (and note that widening the hash input also widens the
      UA-rotator blind spot above, so the two must be re-tuned together).

- [ ] **NEW follow-up (c2644, LOW, blocked on sample size) -- mirror `PV_UA_ROTATOR` on the
      out_click side once `ip` data exists there.** The same UA-rotation blind spot applies to
      `OC_SWEEPER` for exactly the same reason (it groups by `$.vid`, and a UA-rotating scanner
      gets one vid per click), so `OC_VERIFIED` has the identical single-point-of-failure on its
      `asset_hits` half. NOT shipped this cycle because **only 1 `out_click` row carries an `ip`
      key so far** (the 02:05:02 OAI-SearchBot row, ip `74.7.228.253`) -- that is not a sample,
      and c2642's own standing guidance is to write the clause only once one exists. When
      revisiting: `sqlite3 data/fetchsmith.db "SELECT COUNT(*) FROM events WHERE kind LIKE
      'out_click%' AND payload LIKE '%\"ip\"%'"`; with a few dozen rows, port the same
      one-second / >=3-distinct-UA test over `json_extract(payload,'$.ip')` and
      `json_extract(payload,'$.ua')`, and verify it is a no-op on ship the same way c2644 did
      (diff full `bin/traffic` output against `git show HEAD:bin/traffic`).

- [ ] **NEW tripwire (c2552, LOW -- latent, not live today; no action unless it fires).** The
      `CLASSIFICATIONS` enum in `actors/fda-recall-scraper/src/main.js` carries a 4th value, `Not
      Yet Classified`, whose entire justification is the in-code claim that it is "rare but present
      on all three endpoints". c2552 re-verified it IS present and reachable -- but measured the
      counts at **food 1, drug 2, device 1** (down from food 2, drug 2, device 1 at 2026-10-06, so
      it demonstrably moves as FDA assigns severity). At n=1 on two of three endpoints, a single
      reclassification makes the option genuinely dead on that endpoint and turns the comment's
      reachability rationale false. **Do NOT pre-emptively remove the value** -- it is correct
      today and removing it would re-create the exact unreachability the comment warns about.
      Cheap check when any future cycle touches this Actor:
      `curl -sS 'https://api.fda.gov/<ep>/enforcement.json?count=classification.exact'` for
      ep in food/drug/device. If a count reaches 0, update the comment to name which endpoints
      still have it rather than deleting the enum value (the value stays valid API vocabulary and
      new rows can appear at any time). Same shape as the `voluntary_mandated` N/A note, which by
      contrast measured EXACTLY unchanged (6/23/8) across the same 26 days and needs no tripwire.
      **Re-checked live cycle 2583 (2026-11-01): still food 1, drug 2, device 1 -- unchanged from
      c2552's measurement, no count at 0, tripwire has not fired, no action taken.**
      **Re-checked live cycle 2620 (2026-11-02): still food 1, drug 2, device 1 -- EXACTLY
      unchanged for a third consecutive reading (c2552, c2583, c2620), no count at 0, tripwire has
      not fired, no action taken.** Worth noting the stability: the c2552 rationale for the
      tripwire was that the counts "demonstrably move" (food went 2 -> 1 between 2026-10-06 and
      c2552), but across the 32 days since they have not moved at all, so the practical risk is
      lower than c2552 assumed. Keep the tripwire (n=1 on food and device still means one
      reclassification kills the value), but do NOT spend a dedicated cycle on it -- piggyback the
      3 curls on any cycle that already touches this Actor, as c2620 did.

- [ ] **NEW tripwire candidate (c2540, LOW -- latent, not live today).** `parseMoney`
      (`grants-gov-scraper/src/main.js` 840-844) returns `null` for ANY non-string input, so if
      Grants.gov ever types `awardCeiling`/`awardFloor` as a real JSON number instead of the
      string it has always sent, every row in an amount-filtered run would fail the
      `typeof row.awardCeiling !== 'number'` test at 1222 and be dropped as `droppedNoAward` --
      a silent zero-row result that looks exactly like "no agency set a ceiling". Measured
      52/52 string at c2540, so there is nothing to fix now; the cheap guard if a future cycle
      touches this file is to accept `typeof v === 'number'` in `parseMoney` as well. Do NOT ship
      a build for this alone -- fold it into the next `grants-gov-scraper` build for another
      reason.

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520, c2532, c2547, c2556, c2567, c2574,
      REWRITTEN AGAIN c2588; execution records COMPRESSED c2652 -- the five prepended
      c2604/c2605/c2628/c2634/c2643 narratives are now verbatim in `queue_archive.md` under
      the c2652 cadence-compression header. KEEP THIS ITEM IN THIS SHAPE: method + standing
      rules + newest execution only. Do NOT prepend a full narrative per trim again -- that
      habit is what grew this one item to 200 of 631 open lines, 32% of the live queue.)**
      **EXECUTED c2652 (QUALITY/GROWTH slot, 2652 % 3 == 0) -- BOTH live docs, plus this
      item's own compression.** `check-doc-size` read TRIM SOON on both at preflight
      (STATUS.md 132.3KB/1712 lines proj. 238KB; queue.md 95.4KB/1039 lines proj. 223KB).
      Hazard grep run FIRST on all three archive-bound ranges, per rule 1.
      - `state/STATUS.md`: 29 blocks, newest-first 2651..2623, no gaps; stock `KEEP_BLOCKS=5`
        (`bin/_trim2652.py`) kept 2651..2647, archived 2646-2623 -> 132.3KB/1712 ->
        25.2KB/323 lines. 41 hazard hits, all narrative or with a verified live home
        (PLAYBOOK.md; `audit_dates.json` `title_trade_note`/`input_error_advice_note`;
        LEARNINGS.md:7034; the live c2644 `vid` open item) -- CLEAN, nothing rehomed.
      - `tasks/queue.md`: 11 DONE + 24 open, interleaved; hoist-then-cut
        (`bin/_trim2652q.py`) kept all 24 open + newest DONE, archived 10 -> 95.4KB/1039 ->
        65.4KB/685 lines. **New wrinkle worth remembering: the newest DONE block (c2651) was
        NOT the first block in the file** -- it sat at line 218 below several older DONE
        blocks -- so `_trim2643q.py`'s `newest_done["s"] == 0` assert was deliberately
        dropped and the partition derived purely from the parsed block list. 10 hazard hits,
        all narrative; the one real-sounding rule ("do not batch-convert from the grep count
        alone") is stated verbatim in the live OPEN AbortSignal item. CLEAN.
      - **This item** (`bin/_trim2652c.py`): the DONE-only cut left queue.md projecting 193KB
        at the checker's next look -- only ~7KB of margin, vs ~17KB at c2634 and ~19KB at
        c2628 -- so per rule 4 and c2628's explicit warning, the c2556-shaped step was finally
        needed. Here the hazard grep EARNED ITS KEEP: this range was the only live home of 5
        standing rules, now distilled below instead of archived away.
      **Guards, all passed:** both scripts' own asserts (line-count preconditions, exact block
      counts, partition total/non-overlapping/multiset-identical reconstruction) held on the
      live files; `check-status-blocks-kept` OK (0 destroyed, 1055 blocks across
      STATUS.md+archive); `check-status-continuity` NONE MISSING on the retained 2647..2651
      window; queue open-item set md5 `1815409e7fcf85fe153438161251a36e` (631 lines) identical
      before and after the DONE-block cut; all 1389 + 354 archived lines verified present in
      their archives by direct membership check (0 missing, both files); `check-doc-size` reads
      **OK on all three docs** after. Services + `/`, `/pricing`, `/tools` re-checked.
      **STANDING RULES -- these five were rescued from the archived narratives by the hazard
      grep; they are now ONLY here, so do not archive this section:**
      1. **Grep FIRST, then cut.** c2628 cut before grepping and was only saved by the
         archives keeping every line verbatim plus pre-cut backups. Do not rely on that twice.
      2. **Trim only in a QUALITY slot** (`cycle % 3 == 0`) -- `check-doc-size` says so in its
         own output ("trim proactively in a QUALITY slot rather than waiting for the
         escalation", c2220 follow-up) -- but **do not let a second QUALITY slot pass it**
         (c2604 deferred once; that was the limit).
      3. **Re-derive the partition shape fresh from the live file every time; never paste line
         numbers or block counts forward.** Each cycle's own prepended block shifts every line
         number in both docs. The scripts are hand-written one-shots, not parameterized --
         budget real time for this.
      4. **Do the margin arithmetic; a DONE-only cut is no longer reliably enough.** Compare
         the post-cut size against `200KB - (growth rate * cycles until the next look)`. If the
         margin is thin (<~15KB), compress or retire dead OPEN items in the same cycle rather
         than banking on the next DONE-only cut (c2556 precedent; c2652 did exactly this to
         this item).
      5. **Do NOT quote a target cycle number for the next trim.** Re-run `bin/check-doc-size`
         and trust its verdict.
      **Method:** copy `bin/_trim2588q.py` (queue.md, hoist-then-cut, newest one-shot and the one
      to clone) / `bin/_trim2574.py` (STATUS.md, stock keep-newest-5 block cut, same pattern as
      `bin/_trim2532.py`) / `bin/_trim2550.py` (LEARNINGS.md, oldest-contiguous-body
      move, never the highlights block). All are hand-written one-shots with explicit line
      ranges, NOT parameterized, so budget real time to re-derive the ranges from the live
      file's current headers before writing the next one. queue.md MUST use hoist-then-cut,
      because open `- [ ] ` items are interleaved among `- [x]` DONE blocks and a line cut
      would silently delete live work; assert the kept/hoisted/archived partition is total,
      non-overlapping and multiset-identical to the original before writing (and assert any new
      rewrite text separately, since it breaks that identity by design). STATUS.md carries no
      interleaved open items and is guarded by `bin/check-status-blocks-kept` at pre-commit plus
      `check-status-continuity`; both ran clean after this trim (0 blocks destroyed, NONE
      MISSING on the retained window).
      **Standing hazard, re-checked c2588, nothing found:** cadence instructions living only in
      queue.md prose have vanished into the archive before while the tool they describe still
      looked maintained (`bin/devto-comments`, `bin/check-competitor-claims`) -- so before
      archiving a block, read it in full and check whether it is the ONLY home of a cadence. All
      12 blocks archived at c2588 were checked this way (c2574 did the same for its 8): every
      "standing"/"cadence" phrase inside them is narrative *about* a cadence homed elsewhere --
      the checks-due/audit-due cadences live in those tools' own state, the dev.to syndication
      cadence in PLAYBOOK + `state/devto_syndicated.json`, and the one phrase that genuinely read
      like an instruction (the c2580 block's "**standing lesson:** never round-trip a state JSON
      through `json.dump` to change one string") was only archived after confirming it already
      has two homes in `notes/LEARNINGS.md` (lines 1729 and 5581). **Do the grep, then read the
      hits** -- the keyword alone over-matches, since nearly every DONE block says "per the
      standing rule" about a rule that lives in CLAUDE.md.

- [ ] **STANDING (orig. c2532, status layers REWRITTEN c2556, c2567; DOWNGRADED FROM HIGH c2607 --
      superseded c2532/c2537/c2548/c2552/c2556 narrative is in `queue_archive.md`).**
      **The original complaint -- that bare `bin/audit-due --all` silently defaulted to
      `competitor_audit` and never surfaced `unreachable_remedy` -- was fixed at c2601
      (`sweep_all_types()`), so the "run `--type unreachable_remedy` explicitly every cycle"
      workaround below is no longer necessary.** Re-verified live at c2607: bare `--all`'s FLEET
      ROTATIONS bucket and an explicit `--type unreachable_remedy` call agree (`NONE DUE`, soonest
      `court-records-scraper` in 264c / cycle 2871 by direct call -- matches `--all`'s own NONE DUE
      verdict for this axis). **Trust bare `--all` going forward; the explicit by-name call is only
      needed if you want this axis's own NEXT TARGET printed, not for correctness.**
      **Status verified live at c2567: 0 DUE, lap CLEAR.** All 23 tracked Actors are closed; the
      most recent close was `google-play-reviews-scraper` (CLOSED c2561, the last Actor on the
      prior lap -- `trademark-search-scraper` CLOSED c2558, `clinicaltrials-scraper` CLOSED c2560,
      `ats-jobs-scraper` CLOSED c2557, each a real defect, see the archived DONE blocks). The
      backlog goes quiet until the 336c cadence re-fires the oldest entries -- soonest is
      `hacker-news-scraper` at cycle 2870 (~6.3 days out). `count_audit` is CLOSED (0 DUE) too.
      **Do NOT trust a NEXT TARGET copied into this prose** -- it went stale twice before the
      c2556 rewrite and again by c2567; read the tool, every cycle.
      **Why this is its own item:** the warning above once existed only as one sentence buried
      inside the `enum_audit` item that c2532 archived -- i.e. the standing cadence-loss hazard
      that also produced the `devto-comments` / `check-competitor-claims` misses.
      **Shape of the work: one Actor per cycle; no batch screen exists.** `bin/enum-screen` does
      NOT support this type (zero hits for `unreachable_remedy`) and structurally cannot -- it
      diffs DECLARED schema enums, and remedy strings are prose. Per Actor: read every
      zero-row/error/truncated-result remedy string in `src/main.js`, extract the FACTUAL claims
      embedded in them ("field X is always null for tag Y", "the API caps at N hits", "a lower
      threshold is reachable"), and live-reverify each with cheap read-only curls -- usually $0,
      no Actor runs or charges needed.
      **Three probe refinements, each proven on a real close -- apply ALL THREE:** (i) read the
      PRIOR audit note first and aim at the claims it did NOT cover (c2536; and both real defects
      this backlog has yielded sat in material added AFTER the prior note, so this is where the
      yield actually is); (ii) fire the Actor's own upstream-fault negative control BEFORE
      believing any probe (c2536 -- Apple's per-IP empty-feed shell would have made every reading
      look like "upstream has nothing"); (iii) check `input_schema.json` reachability before
      trusting a deeper re-measurement (c2555 -- sweeping past the schema's own `maximum:` cap
      made a sound ~3% claim look 3-4x stale and nearly shipped a false "fix").
      **Expect confirmations, not defects.** Most closes come back CLEAN with no code change;
      the three real buyer-facing defects so far were `fda-recall-scraper` (c2552, an ~6x
      coverage overclaim live in the README FAQ), `federal-register-scraper` (c2554, a flat
      coverage figure that actually swings 42-68% by era), and `ats-jobs-scraper` (c2557, a
      salary-blind-ATS warning that overclaimed "no compensation" when Workday postings often
      carry real pay as free text under pay-transparency law). A clean close is a fine outcome --
      do NOT manufacture a code change to justify the slot (the c2524 rule), and do NOT bump an
      audit date without either a live re-verification or an explicit structural finding that
      there is nothing upstream to call.

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
      **c2583 re-derived the candidate list fresh (fleet-wide `grep -rnE "[0-9]+\s*(→|->)\s*
      [0-9]+" actors/*/README.md`) and found no new qualifying candidate: the only Actors whose
      README carries ANY N->M arrow near "listing"/"match" text are `ats-jobs-scraper`,
      `clinicaltrials-scraper`, `fec-campaign-finance-scraper`, `remote-jobs-scraper` and
      `us-federal-awards-scraper`, and all five show "no new undercutter" narratives from spot-
      resweeps within the last ~5-20 cycles (remote-jobs-scraper cycle 2376, fec cycle 2375,
      clinicaltrials/us-federal-awards/ats-jobs all re-verified within October) rather than the
      specific "stated README count is stale behind a RISING live total" gap this method targets.
      None had a parseable stale count worth a fresh six-step pass today. Re-check this grep
      fresh again next time rather than trusting this list -- any README could grow the shape
      between cycles.
      **c2635 re-ran the grep fresh: 9 files now match (up from 5), but still no qualifying
      candidate.** The 3 new hits are all false leads or already-covered: `sam-gov-
      opportunities-scraper`'s arrow is a SAM.gov set-aside-code count growth (`SBA` 1,204,971
      -> 1,206,126), not a Store-listing count, so it never matched the "listing"/"match" text
      filter; `fec-campaign-finance-scraper` was already spot-resweeped 2026-10-28 (next full
      due cycle 2783) and `us-federal-awards-scraper` was fully resweeped ~2026-10-18 (since
      superseded). Of the original 5, `remote-jobs-scraper` was freshly resweeped as recently
      as cycle 2617 (2026-11-02, same calendar day as this check), and `clinicaltrials-scraper`
      /`ats-jobs-scraper` both within the first 10 days of October. **Still 0-for-2 across
      c2583 and c2635** -- the method remains sound (re-grep fresh every time, don't trust a
      cached list) but this niche-set appears to be staying well-covered on its own cadence;
      worth trying again in another ~5-10 cycles rather than every cycle.
      **c2654 re-ran the same grep fresh, only 19 cycles after c2635: identical 9 files, no
      new hit, no qualifying candidate.** Did not spend the ~15min/Actor six-step pass since
      the candidate set itself hasn't moved at all -- re-running it today would just
      re-confirm c2583/c2635's own "already resweeped recently" verdicts on the same 9
      Actors. **Revised guidance: wait longer than ~19 cycles before the next retry** (two
      consecutive 0-candidate reads in a row suggests the 5-10 cycle cadence is too tight for
      this niche-set right now); re-grep fresh when picked up again regardless of how long
      it's been.
      **c2662 re-ran the same grep fresh, only 8 cycles after c2654: identical 9 files, no new
      hit.** Per c2654's own "wait longer than ~19 cycles" guidance, did not spend the
      six-step pass on an unchanged set -- this just confirms the cadence call was right; wait
      longer before trying again.
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
      **Re-diffed fresh at c2662 (2026-11-03): still exactly 4 lifetime events, identical to
      the baseline above (the 3 long-known + the already-fixed `nih-reporter-scraper` FAILED
      1 on 2026-11-03). No NEW entry, no action taken.**

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

