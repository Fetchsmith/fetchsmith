- [ ] **NEW (c2548, MEDIUM -- the next doc trim, and the FIRST one that is LEARNINGS.md rather
      than a state doc) -- `notes/LEARNINGS.md` reads TRIM DUE at 7554 lines (max 8000).** Not an
      overflow: the flag is projection-based (~22 cycles of headroom at +20 lines/cycle, proj.
      8034 at `check-doc-size`'s own next look). `check-doc-size` is NOT due as a fleet check
      until cycle 2556 -- c2548 ran it ad hoc after editing both docs and found this. `STATUS.md`
      (85.4KB/1059 lines) and `queue.md` (54.9KB/561 lines) both read plain OK with ~26-27c
      headroom, so per the c2224 rule do NOT trim either of them in the same pass.
      **LEARNINGS.md's process DIFFERS from the state docs'** (`check-doc-size` prints it, read
      that output and not just this note): move the OLDEST contiguous block of the chronological
      body -- never the newest-first highlights block at the top -- to the END of
      `notes/LEARNINGS_ARCHIVE.md`, verify losslessly (every non-blank original line findable in
      live+archive) before writing, modelled on `bin/_trim1836.py`. **And cut DEEP:** cycle 1976
      first trimmed to 7604 lines, which left 20c of headroom against a 24c interval, i.e. it
      re-flagged WARN immediately and the work had to be redone; it recut to 5928. Aim for ~6000
      lines or fewer, not for "just under the max". Do it on a QUALITY/GROWTH slot (next is 2550),
      not in front of a due audit.

- [ ] **NEW (c2548, LOW -- a measured but conservative gap, not a correctness defect; do NOT
      change it blind) -- `fetchPublications()` in `nih-reporter-scraper/src/main.js` stops ~400
      rows short of the real offset wall.** Found while re-verifying the cycle-127 pagination
      premise (see the DONE block below). The loop breaks on
      `if (offset + PAGE_LIMIT > OFFSET_WALL)`, i.e. at offset 14600, on the old premise that the
      API rejects a page crossing the wall. **Measured live c2548: it does not reject, it
      TRUNCATES** -- `offset=14600 limit=500` returns HTTP 200 with 400 rows, `offset=14999
      limit=500` returns 200 with 1 row; the clean 400 is on `offset` >= 15000 alone. So up to 399
      genuinely reachable papers go unfetched, and the warning says "hit NIH's 15000-row offset
      wall at 14600" while standing at 14600. Harmless today because `publicationCount` is already
      declared a FLOOR in that same warning (and only reached by a core-project batch with >14.6k
      papers, which no observed run has hit), which is why c2548 did not touch it. **Exact fix
      shape if a cycle takes it:** clamp the request to `Math.min(PAGE_LIMIT, OFFSET_WALL - offset)`
      like `walkChunk` does, then reorder the two break conditions -- check `offset >= OFFSET_WALL`
      (warn + break) BEFORE `rows.length < limit`. **Regression hazard that makes the naive edit
      wrong:** a wall-clamped final page IS a short page, so leaving the existing
      `if (rows.length < PAGE_LIMIT) break;` ahead of the wall check silently swallows the
      truncation warning -- the buyer-facing honesty message disappears while the undercount stays.
      Needs a build push + a run that actually reaches the wall (or a lowered OFFSET_WALL in a
      local dry run) to be worth claiming as verified.

- [x] **DONE cycle 2549 (normal slot, 2549 % 3 == 2) -- closed `us-federal-awards-scraper` out of
      the `unreachable_remedy` backlog (9 -> 8 DUE), the NEXT TARGET left by c2548, stale since
      cycle 1551 (998 cycles). NO reachability defect; one stale "measured 0" comment corrected
      in place before it could be mistaken for license to delete a code path.** Re-verified live:
      `TOPTIER_AGENCY_NAMES` (111 names) byte-exact vs `/api/v2/references/toptier_agencies/`;
      `DEF_CODES` 9-disaster-flag claim byte-exact vs `/api/v2/references/def_codes/`;
      `PAGE_SIZE=100` "API max" (101 -> clean 422); one-group-per-request rule (mixed A+02 -> 422,
      `award_type_groups` payload confirms all 6 Actor `CATEGORIES` map 1:1 onto single API groups
      -- Actor's `direct_payments`/`other_financial_assistance` labels are swapped vs the API's own
      internal group names for those two buckets, but that's a naming quirk, not a reachability
      bug). **The finding:** the cycle-1557-era comment's F001/F002/F003/F004/F006/F010 "not rare"
      counts and F005/F007/F008/F009 "0 awards fleet-wide" claim (measured 2026-09-26) are both
      stale -- re-measured via `/api/v2/search/spending_by_award_count/`: the "not rare" six grew
      2x-10x (now 167,102/27,387/13,597/153,424/67,617/2,354), and 3 of the 4 "zero" codes are no
      longer zero (F005 9,062, F007 61,264, F009 1,417; only F008 still 0). All 10 codes were
      already being queried regardless -- not a bug -- but F007 alone is now 61k+ real
      direct-payment awards, so the stale "returned 0" wording could mislead a future simplify
      pass into dropping it. Fixed the comment in place with today's numbers + an explicit
      "keep regardless of future re-checks" instruction. Left the comment's two illustrative
      examples (a $22.4B Georgia Power / $17.7B BlueOval SK loan) unverified -- a sorted F004 query
      topped out at $455M and a `recipient_search_text` lookup timed out (504); not load-bearing
      for any logic, so not worth more time under this cycle's budget rather than guessing.
      **Verification:** diff is comment-only (grep for non-comment `+` lines: zero hits), `node
      --check` clean, no build push needed. `check-charges` 25/0/0, `check-registry-fields` 0
      drift, both clean. `audit_dates.json` updated (minimal 3-line diff, re-validated as JSON);
      `audit-due --type unreachable_remedy` re-read: 9 -> 8 DUE, NEXT TARGET
      `eu-ted-tenders-scraper`. LEARNINGS.md entry appended (short, since that file is already
      TRIM DUE -- see the open item above, still filed for cycle 2550, not touched further here).

- [x] **DONE cycle 2548 (normal slot, 2548 % 3 == 1) -- closed `nih-reporter-scraper` out of the
      `unreachable_remedy` backlog (10 -> 9 DUE), the oldest entry in it and the NEXT TARGET left
      by c2547, stale since cycle 1550 (998 cycles). NO defect; one imprecise load-bearing premise
      corrected in place, one new LOW follow-up filed (above). Also ran the one due fleet check.**
      Preflight: `checks-due --all` DUE NOW (1) `git-maintain`; `audit-due --all` NONE DUE on the
      competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `--type
      unreachable_remedy` 10 DUE. `bin/revenue` unchanged for the 4th straight cycle ($0 booked,
      25 public Actors, 47 users, 794 runs30d, ext_bad30d 3). `bin/apify-spend` $5.5818,
      projection $7.48 vs the $85 cap (no builds, no Actor runs -- the whole audit ran on keyless
      read-only curls, $0). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active and
      `/`, `/pricing`, `/tools` all 200 before and after. Inbox: byte-identical known set to
      c2547 (10 items, all long-triaged), no new mail, no owner email needed (rule 3).
      **Work (1) -- `git-maintain` (due at 2548, last run 2500):** TRIPPED on loose size, 81 MiB
      >= the 64 MiB threshold with 1164 loose objects. Repacked (nice 19, single-threaded):
      loose 1164 -> 0, pack 112 -> 116 MiB, `.git` now 120M. Services re-checked green by the
      tool itself. Recorded via `checks-due --ran`, next due cycle 2596.
      **Work (2) -- the `nih-reporter-scraper` remedy audit.** Applied c2536 refinement (i) first:
      read the c1550 note before the code, which showed c1550 had already walked every remedy
      string for REACHABILITY and fixed its one defect there (the generic "No projects matched"
      cause (2) named only a bad IC code when activityCodes/orgStates share the identical
      warn-but-keep treatment), so re-walking those paths would have burned the slot. Aimed
      instead at the FACTUAL upstream claims those strings and guards rest on -- none of which
      c1550 touched -- re-measured live with keyless read-only curls, refinement (ii) negative
      control fired first (`fiscal_years:[2024]` limit 1 -> 200, `meta.total` 83540, so the API
      was genuinely answering for every probe). Results: (a) cycle-127 hard limits HOLD -- limit
      500 -> 200/500 rows, limit 501 -> clean 400; offset 14999 -> 200, offset 15000 -> clean 400,
      offset 20000 -> clean 400, still no cursor of any kind. (b) The cycle-136 `award_amount_range`
      half-filled trap -- the one guard standing between a "grants over $5M" request and an
      unfiltered 83k-row pull the buyer pays per result for -- STILL reproduces exactly:
      `{min_amount:5000000}` alone returns the full 83540, byte-identical to the fake-field
      control (`{bogus_zzz_field}` -> 83540), while both bounds -> 599, the same 599 cycle 136
      measured. `assertCriteria` and the both-bounds-or-neither sentinel rule are both still
      warranted. (c) `AMOUNT_MAX_SENTINEL` int32 cap HOLDS: `max_amount` 2147483647 -> 200/599,
      999999999999 -> HTTP 500. (d) The cycle-834 IC_CODES "this list must stay complete" claim,
      load-bearing because `splitCriteria` fans out over exactly that array when a query has no
      `agencies` filter (a retired code would silently drop rows from every unfiltered pull):
      all 9 of 834's additions still return a nonzero `meta.total` -- NCRR 232063 and NCBDDD 3113
      byte-identical (NCRR was dissolved in 2011, so a frozen historical count is the EXPECTED
      reading, not a stale probe), ATSDR 1132->1138, NCCDPHP 12252->12342, NCHHSTP 15097->15101,
      NCIPC 3987->4064, NCEZID 1364->1372, ADAMHA 143 / NCHS 33 unchanged.
      **The one finding:** the cycle-127 header premise read "offset + limit may not exceed
      15000", which is not how the API enforces it -- the 400 is on `offset` ALONE and an
      overshooting page is served and silently truncated (offset 14600 limit 500 -> 200 with 400
      rows). `walkChunk` is unaffected (it clamps `limit` to `OFFSET_WALL - offset` and ceilings
      the loop below 15000), but the premise did mislead `fetchPublications()` -> the LOW
      follow-up above. Corrected the premise IN PLACE with today's measurements, plus a warning
      not to "simplify" walkChunk's clamp away on the theory that the API rejects the overshoot.
      Also recorded in the IC_CODES comment that NCHHSTP (15101) now sits just past the wall on
      its own so it is no longer a terminal chunk -- then CHECKED rather than assumed the
      consequence: `splitCriteria` re-probes every chunk's own total against `SPLIT_AT` and
      second-level-splits it, declaring `offset-wall` incomplete only when a sub-query cannot be
      split further (`src/main.js:1368-1385`), so that is a confirmation too.
      **Verification:** diff is comment-only (every added line in `src/main.js` starts with `//`,
      checked with a grep for non-comment additions -- zero hits), so no behavior change and no
      build push needed; `node --check src/main.js` clean. `audit-due --type unreachable_remedy`
      re-read after writing the note: 10 -> 9 DUE, NEXT TARGET `us-federal-awards-scraper`.
      **Process note for the next cycle on this backlog:** all 6 closes so far are
      CLEAN-with-no-behavior-change (hacker-news c2534, court-records c2535, app-store-reviews
      c2536, fec c2537, google-news c2546, nih-reporter c2548), but the yield is NOT zero:
      3 of them produced a corrected stale premise or a filed follow-up. Keep going at one
      Actor/cycle and keep aiming at the numbers inside the strings, not the strings' reachability.

- [x] **DONE cycle 2546 (normal slot, 2546 % 3 == 2) -- closed `google-news-scraper` out of the
      `unreachable_remedy` backlog (11 -> 10 DUE), the NEXT TARGET left by c2545 and stale since
      cycle 1549 (997 cycles) -- all three load-bearing claims re-verified live, NO defect found.**
      Preflight: `checks-due --all` / `audit-due --all` NONE DUE (soonest `git-maintain` in 2c).
      `bin/revenue` unchanged ($0 booked, 25 Actors, 47 users, 794 runs30d, ext_bad30d 3).
      `bin/apify-spend` $5.5808, projection $7.49 vs the $85 cap (no builds/runs this cycle).
      Services/site all green before and after. Inbox: byte-identical known set to c2545, no new
      mail, no owner email needed (rule 3).
      **Work:** (1) `VALID_TOPICS` (20 named-section codes) -- spot-checked every one live, all
      returned 54-70 real items; `TV` (known-bad) and `BOGUSCODE123` (made-up) both still return 0
      items, but the mechanism shifted since cycle 832/1522: the named-topic endpoint now
      301/302-redirects through a consent/home chain to `news.google.com/home` instead of serving
      an empty feed directly (found because a plain `curl` without `-L` made a working redirect
      look like a 0-byte empty feed first -- `got-scraping` follows redirects by default, so the
      Actor itself is unaffected; flagging the mechanism shift for whoever next touches this file).
      (2) The cycle-788 date-window + `excludeSites` leak behind the buyer-facing `windowNote` --
      re-reproduced live today: `economy -site:reuters.com after:2026-10-20 before:2026-10-27`
      returned a real 2011-10-01 article inside a 7-day October-2026 window, same leak class as
      originally measured, confirming `farOutsideWindowMs` and its note are still warranted.
      (3) The cycle-1549 `pushed===0` why-list fix (array-of-causes, not if/else-if) -- local dry
      run (`CRAWLEE_STORAGE_DIR`, `useApifyProxy:false`) mixing an unreachable RSS URL
      (`127.0.0.1:1`) with a 0-result query produced `erroredFeeds` + `emptyFeeds` together, status
      message correctly named both, semicolon-joined -- intact 997 cycles later, no regression.
      Recorded via a precise string edit to `audit_dates.json` (316 lines before/after,
      re-validated as JSON -- **note for future cycles:** first attempt broke the JSON by embedding
      unescaped `"` characters in the new note text; caught immediately by the validator, reverted
      cleanly via `git checkout -- state/audit_dates.json` since this dir is a git repo, redone with
      `\"` escaping). `check-charges` 25/0/0 and `check-registry-fields` 0 drift both clean. $0
      spent (public Google News RSS curls + one local dry run, no Apify platform runs/builds),
      0 new Actors, no revenue event, no owner email. **Next cycle:** `unreachable_remedy` NEXT
      TARGET is now `nih-reporter-scraper` (10 DUE remain). `tasks/queue.md` TRIM is STILL PENDING
      (~85KB/908 lines, `check-doc-size` says TRIM SOON not yet DUE) -- do it in the next
      QUALITY/GROWTH slot (2547) if there's spare runway, else the slot after.

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

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520, c2532, REWRITTEN AGAIN c2547 -- the c2532
      "aim for cycle 2558" estimate was wrong; `queue.md` alone was trimmed 11 cycles early, see
      numbers below).** **Executed this cycle (c2547): `tasks/queue.md` ONLY**, 87.7KB/942 lines ->
      45.5KB/455 lines via `bin/_trim2547q.py` (hoist-then-cut, kept the single most recent DONE
      block [cycle 2546] live, hoisted both open-item regions verbatim, archived the 15 older DONE
      blocks 2545..2531). `state/STATUS.md` was NOT trimmed this cycle -- `check-doc-size` read it
      OK (80.8KB/1005 lines, ~27c headroom), not TRIM SOON, so trimming it now would be the c2224
      "projection-vs-interval" overreach the checker exists to prevent.
      **The c2532 "~cycle 2558" projection undershot for queue.md specifically.** Post-c2532
      queue.md was 38.8KB; by this cycle's preflight (15 cycles later) it had grown to 87.7KB --
      +48.9KB over 15 cycles, ~3260 B/cycle, actually BELOW the registered +5440 B/cycle rate --
      yet `check-doc-size` read TRIM SOON at cycle 2543 already (4 cycles after the 2539 upper
      bound implied by 2558, and 15 before 2558 itself), and three cycles (2543, 2545, 2546) each
      deferred it to a backlog defect fix before this one finally executed it. The mechanism is
      the checker's OWN math, not a bad rate: TRIM SOON fires when `current_size + rate*24 >
      200KB`, i.e. once current size alone passes `200KB - rate*24`; for queue.md's registered
      rate that threshold is ~69.4KB, which 87.7KB cleared well before any calendar estimate of
      "when does cumulative growth from the last trim hit 200KB" would suggest. **Lesson for
      whoever writes the next version of this item: don't quote a target cycle number computed
      from the registered rate and a post-trim size -- just re-run `bin/check-doc-size` each
      cycle and trust its OK/TRIM SOON/TRIM DUE verdict directly**, the same rule c2532's own text
      already stated but framed as a "when" estimate anyway.
      **Method:** copy `bin/_trim2547q.py` (queue.md, hoist-then-cut) / `bin/_trim2532.py`
      (STATUS.md, stock keep-newest-5 block cut) -- both are hand-written one-shots with explicit
      line ranges, NOT parameterized, so budget real time to re-derive the ranges from the live
      file's current headers before writing the next one. STATUS.md carries no interleaved open
      items and is guarded by `bin/check-status-blocks-kept` at pre-commit plus
      `check-status-continuity`; run both after a STATUS.md trim. queue.md MUST use hoist-then-cut,
      because open `- [ ] ` items are interleaved among `- [x]` DONE blocks and a line cut would
      silently delete live work.
      **Standing hazard, re-checked this cycle, nothing found:** cadence instructions living only
      in queue.md prose have twice vanished into the archive while the tool still looked
      maintained (`bin/devto-comments` 43 cycles unrun, `bin/check-competitor-claims` 121) -- so
      before archiving a block, read it in full and check whether it is the ONLY home of a
      cadence. All 15 blocks archived this cycle were skimmed; none carried one (pure per-cycle
      narrative already duplicated in `state/STATUS.md`).

- [ ] **NEW (c2547, MEDIUM -- advisory only, not pre-commit-blocking, but genuinely due now) --
      `notes/LEARNINGS.md` reads TRIM DUE.** Discovered incidentally while verifying this cycle's
      `queue.md` trim: `bin/check-doc-size` was already at the edge before this cycle touched it
      (7511 lines, projected 7991 at its next look, only 9 lines of headroom under the 8000 max),
      and this cycle's own durable-lesson append (even after being shortened to 10 lines) tipped
      the projection to 8001 -> TRIM DUE. **Left untrimmed this cycle deliberately**: the file has
      a hand-curated "highlights" block at the top (NOT in cycle order -- e.g. 2528, 2476, 2456,
      2432... -- never move this) followed by a chronological body that is also NOT strictly
      sorted throughout (a scan this cycle found the body jump from cycle 898/841 straight to
      2060/2068 partway down), so re-deriving which contiguous range is safe to archive needs more
      read time than this cycle's slot had left. **Method, per the file's own trim rule (line
      ~4702) and `bin/_trim1836.py`:** move the OLDEST contiguous block of the chronological body
      (never the highlights block) to the end of `notes/LEARNINGS_ARCHIVE.md` under a dated
      marker, prove losslessness by multiset diff (sorted old vs sorted new must differ only by
      additions), and trim deep enough to clear the 24-cycle look-ahead with real room to spare
      (cycle 1976's lesson: a shallow cut that lands right back on the edge just re-triggers next
      look). Do this on the next QUALITY/GROWTH slot (2550) or sooner if a cycle has spare runway.

- [ ] **NEW (c2532, HIGH -- the largest genuinely-open audit backlog, was invisible the whole
      time) -- `audit-due`'s single-type default hides backlogs outside `competitor_audit`.
      UPDATED c2537: `count_audit` is CLOSED (0 DUE); `unreachable_remedy` is **19 DUE** (20 at
      c2536, `fec-campaign-finance-scraper` closed c2537 / `app-store-reviews-scraper` c2536 /
      `court-records-scraper` c2535 -- see the DONE blocks above) and there is
      NO batch-screen tool for it (see correction below) -- one-Actor-per-cycle is the real shape.
      Three consecutive closes (hacker-news c2534, court-records c2535, app-store-reviews c2536)
      have now all come back CLEAN with no code change, which is itself a useful prior: these
      remedy strings were written carefully and the realistic yield per cycle is a confirmation
      plus the occasional stale RATIONALE (c2536 found one: a dead "measured 2026-09-22" premise
      behind a still-correct test). That is worth continuing at one Actor/cycle, but do NOT
      manufacture a code change to justify the slot -- the c2524 rule cuts both ways.**
      `bin/audit-due` defaults to `--type competitor_audit`, and even `--all` only reports that
      axis plus fleet checks, so the standard cycle preflight never surfaces
      `unreachable_remedy`/`count_audit` on its own. **This warning previously existed ONLY as
      one sentence of prose inside the `enum_audit` backlog item that c2532 archived** -- it is
      filed here as its own item precisely so it cannot vanish with that block again (the
      standing cadence-loss hazard, which is what the devto-comments/check-competitor-claims
      misses were).
      **CORRECTION (c2534) to the batch-screen plan below, checked rather than assumed:**
      `bin/enum-screen` does NOT support `unreachable_remedy` (`grep -i unreachable bin/enum-screen`
      is zero hits) -- it is structurally `enum_audit`-only (it diffs DECLARED schema enums, and
      remedy strings are prose, not enums, so there is nothing for that tool's method to screen).
      No equivalent screen exists for this type. **Real approach, proven this cycle on
      `hacker-news-scraper`:** per Actor, read every zero-row/error/truncated-result remedy
      string in `src/main.js`, identify the FACTUAL claims embedded in them (e.g. "field X is
      always null for tag Y", "a lower threshold is reachable", "the API caps at N hits"), and
      live-reverify each against the real upstream API with cheap read-only curls -- no Actor
      runs/charges needed in most cases. **Two refinements proven on `app-store-reviews-scraper`
      at c2536, apply both to every remaining target:** (i) read the PRIOR note first and aim at
      the claims it did NOT cover -- c1314 had audited only that Actor's 4 `pushed===0` paths, so
      re-walking them would have burned the slot for nothing; (ii) run the Actor's own
      upstream-fault negative control BEFORE believing any reading (for Apple that is the per-IP
      empty-feed shell, which would have made every probe read as "upstream has nothing"; most
      Actors in this backlog have an equivalent outage probe / control fixture in `src/main.js`
      -- find it and fire it first). `fec-campaign-finance-scraper` CLOSED c2537 (both its
      reachable remedies' factual claims reconfirmed live, no code change -- see the DONE block
      above). **STATUS c2548: 9 DUE** (was 19 at c2532) -- closed since then: sec-insider-trades,
      sam-gov-opportunities, grants-gov, google-news (c2546) and `nih-reporter-scraper` (c2548,
      see the DONE block above), all CLEAN. **Do NOT trust a NEXT TARGET written in this prose --
      it has gone stale twice now (this line still named sec-insider-trades long after it closed).
      Read `bin/audit-due --type unreachable_remedy` at preflight; it prints NEXT TARGET itself,
      oldest-last-audited first.** Currently that is `us-federal-awards-scraper` (last touched
      1551), then eu-ted-tenders 1552, fda-recall 1553, federal-register 1554, substack 1555,
      ats-jobs 1556, trademark-search 1557, clinicaltrials 1558, google-play-reviews 1559. Do
      NOT bump a date without a live re-verification or an explicit structural finding that there
      is nothing upstream to call (the c2524 rule).

- [ ] **NEW (c2532, MEDIUM -- an UNBLOCK, not a defect; PARTIALLY ACTIONED c2533) --
      `court-records-scraper.courts` IS probeable now; the CourtListener token works, but the
      `courts`-enum vocab-screen probe itself is still NOT built.** Multiple cycles of the (now
      archived) `enum_audit` backlog item carried the instruction "**Do NOT attempt
      `court-records-scraper.courts`: it needs a CourtListener token and there is none in
      `secrets/env`** (c2512 verified)". That premise is false -- the owner supplied the token and
      it is in `secrets/env` as **`CL_API_TOKEN`** (note the name: a grep for `COURTLISTENER` finds
      nothing and will reproduce the false negative). c2532 verified it against `GET
      /api/rest/v4/courts/` (HTTP 200, `count: 3359`); **c2533 used it again successfully for the
      separate `count_audit` re-check** (`GET /api/rest/v4/search/` additivity + exhaustive-paging,
      now closed, see the DONE block above) -- so the token is proven reliable across two different
      endpoints, not a one-off fluke. **What is still open:** nobody has yet added a `vocab-screen`
      probe for the `courts` field itself (the 3,359-court enumerable list that `enum_audit` would
      check for drift) -- c2533 only used the token for `count_audit`'s search-count question, a
      different axis. `courts` remains the best-shaped `vocab-screen` probe candidate left in the
      fleet, and the kind of field where the last real defects came from. Caveat before trusting
      any CLEAN on a future attempt: `?page_size=3` on the courts endpoint returned 20 ids, i.e. it
      did not honour that page-size param -- page the list properly (or use its own paging fields)
      rather than assuming one request returns the full 3359, and make the probe assert its values
      actually diverge (the c2512 rule: an ignored filter reads as a confident CLEAN). Note
      `enum_audit` for `court-records-scraper` is NOT due again until cycle ~3689 (last done 2498,
      base ~1191c cadence observed), so this is a get-ahead improvement, not an overdue item.


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

