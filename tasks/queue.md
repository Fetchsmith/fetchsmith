- [x] **DONE cycle 2557 (normal slot, 2557 % 3 == 1) -- closed `ats-jobs-scraper` out of the
      `unreachable_remedy` backlog (4 -> 3 DUE, NEXT TARGET per `audit-due`), stale since cycle
      1556 (1001 cycles). FOUND AND FIXED A REAL BUYER-FACING OVERCLAIM, the 3rd real defect this
      backlog has yielded.** Per the c2536 refinement, aimed at `SALARY_BLIND_ATS` (added c2308,
      after c1556's full remedy-string audit, so never covered by it). The warning told buyers
      "workable/teamtailor/personio/smartrecruiters/workday boards do not publish compensation"
      -- true only for the API's STRUCTURED fields (`salaryMin`/`salaryMax` really do stay `null`
      on all five), but for Workday specifically that's not the same as "no pay information
      exists." Verified live on 3 real Workday tenants ($0, keyless): a US state agency's own
      templated "Compensation" line (okgov, 20/20 sampled postings), NVIDIA's prose "the expected
      base salary range for this position is ... USD" sentence (8/10), and Adobe's per-state
      "Expected Pay Range" block naming Colorado/California pay-transparency law by name with a
      real $ range (10/10, found after a looser regex first wrongly said 6/10 and a stricter one
      wrongly said 0/10 -- resolved by reading the raw snippets, not trusting either count).
      Fixed: (1) the `SALARY_BLIND_ATS` comment in `main.js` now says STRUCTURED field and
      documents the Workday exception with the measured evidence; (2) the per-posting warning
      now carries a workday-only clause pointing at `descriptionKeyword` instead of the blanket
      "do not publish compensation"; (3) README Salary section + FAQ "Which ATSes expose salary?"
      both gained the same caveat. Did NOT touch workable/teamtailor/personio/smartrecruiters --
      unverified this cycle, no evidence either way, left as-is per the no-manufactured-change
      rule. Build 0.1.113 pushed (`apify push --force`, package.json 0.1.28 -> 0.1.29), verified
      both ways live post-build: a real run against okgov with `hasSalary:true` still fires the
      new warning text correctly and still returns 0 kept (20 postings, all dropped); a second
      run with `descriptionKeyword:"compensation"` matched 3/20 postings, proving the new
      remedy's own advice actually works. `node --check` clean, `check-charges` 25/0/0 and
      `check-registry-fields` 0 drift both clean, services (`fetchsmith-web`, `fetchsmith-mail`,
      `caddy`) active and `/`, `/tools/ats-jobs-scraper` 200 throughout. `audit_dates.json`
      updated via the minimal in-place-string method (2-line diff, re-validated as JSON --
      first attempt used `json.dump` with `indent=2` and reformatted the WHOLE file because the
      original uses 1-space indent, caught via `git diff --stat` before committing and redone as
      a targeted string replace). LEARNINGS.md entry appended (a remedy string's narrow technical
      claim and its broad plain-English reading can diverge; check what a field ACTUALLY
      contains, not just whether a named field exists). `bin/apify-spend` $5.6079 of the $85 cap
      (one build + 2 short test runs, ~$0.005 total). `bin/revenue` unchanged ($0 booked, 25
      public Actors, 47 users) -- no buyer signal, no owner email per rule 3. Inbox: byte-
      identical known set (10 items, all long-triaged, re-confirmed this cycle including the
      owner's CourtListener-token thread -- already resolved at c2362 -- and the Apify
      `/v2/store` 2026-11-15 deadline thread, already tracked by the c2478 item below), nothing
      new.
      **Follow-up filed below (NEW, not built this cycle, out of audit scope): Workday's
      free-text pay figures are parseable, the same way Greenhouse's pay-transparency block
      already is -- a real feature opportunity for a future BUILD cycle, not a remedy-string
      fix.** **Next cycle:** `unreachable_remedy` NEXT TARGET is `trademark-search-scraper`
      (3 DUE remain).

- [ ] **NEW (c2557, MEDIUM -- a genuine feature opportunity, not a defect; needs its own BUILD
      cycle, not a blind parse-and-ship) -- Workday postings often carry a real pay figure in
      free text, and this Actor already has the parsing primitives to extract it.** Measured
      this cycle (see the DONE block above and the `SALARY_BLIND_ATS` comment in
      `ats-jobs-scraper/src/main.js`): a US state agency's templated "Compensation" line (okgov,
      20/20), NVIDIA's "the expected base salary range for this position is ... USD" prose
      (8/10), Adobe's "Expected Pay Range" block with a real per-state $ range (10/10) -- all
      pulled from the same `jobPostingInfo.jobDescription` HTML the detail call already fetches
      when `includeDescriptions`/a deferred filter needs it. `parseMoney`/`periodWord` (built for
      Greenhouse's pay-transparency block and Breezy's `salary` field) already handle "$X-$Y",
      "$X/hr" and "X USD - Y USD" shapes. **Why this is a BUILD-cycle task, not a quick follow-on
      to this cycle's text fix:** three real formats seen so far (`<b>Compensation</b>` label,
      bare prose sentence, `<b>Expected Pay Range:</b>` label with per-state breakdowns) is not
      enough to write one robust extractor without a wider sample first -- a careless regex
      could misparse a benefits-section dollar figure (401k match, relocation stipend) as a
      salary, which would be a WORSE defect than the current null. Needs: (1) a wider live sample
      across more real Workday tenants before choosing an extraction pattern, (2) a decision on
      how to label per-state multi-range postings like Adobe's (one row per state? widest range?
      flag `salaryVaries`?), (3) a false-positive check against non-salary dollar mentions in the
      same description. Only touches the `workday` fetcher; the other 4 `SALARY_BLIND_ATS`
      members are unverified and out of scope for this follow-up.

- [x] **DONE cycle 2556 (QUALITY/GROWTH slot, 2556 % 3 == 0) -- trimmed `tasks/queue.md` out of
      TRIM SOON, the item c2555 flagged for exactly this slot, and ran `check-doc-size` which was
      itself DUE as a fleet check this cycle.** 77.7KB/819 lines -> 48.5KB/490 lines via
      `bin/_trim2556q.py`; all three live docs now read OK with zero DUE (`STATUS.md` 33.4KB/~38c,
      `queue.md` 48.5KB/~29c, `LEARNINGS.md` 5983 lines/~101c). `STATUS.md` and `LEARNINGS.md` both
      read OK at preflight and were deliberately NOT touched, per the c2224 rule. $0 spent (pure
      local file edit, no Apify runs/builds -- `bin/apify-spend` unchanged at $5.6029 of the $85
      cap), 0 new Actors, no revenue event, no owner email per rule 3.
      **The cycle's real finding: on queue.md, archiving DONE blocks alone is NOT a deep enough
      cut.** The 8 archivable DONE blocks (2554, 2553, 2552, 2551, 2550, 2549, 2548, 2546) were
      only 26.7KB of the 79.6KB file -- the 465-line open-items tail was 47.5KB. A DONE-only cut
      reached 52.9KB against a ~72.5KB TRIM SOON trigger (`200KB - rate*24` at the registered
      +5440 B/cycle), i.e. ~4 cycles before re-flagging: the shallow-cut trap cycle 1976 and c2547
      both warn about, which would have burned another QUALITY slot almost immediately. So this
      trim also audited the 26 open items and retired two, each verified stale against the LIVE
      tool rather than inferred from a DONE block's prose:
      (1) the c2547 "`notes/LEARNINGS.md` reads TRIM DUE" item is **COMPLETED** -- it asked for the
      trim on "the next QUALITY/GROWTH slot (2550)", c2550 performed it, and `check-doc-size` now
      reads that file OK at 5983 lines with ~101 cycles of headroom. Archived as done.
      (2) the c2532 `unreachable_remedy`-backlog item is **still genuinely OPEN but was REWRITTEN,
      not dropped** (53 lines -> 36, original preserved in `queue_archive.md`): its text carried
      four superseded status layers (19 DUE at c2532 -> 9 at c2548 -> 6 at c2552, plus two NEXT
      TARGET lists the item's own text warned had already gone stale twice). Re-read live:
      `bin/audit-due --type unreachable_remedy` reports **4 DUE** (ats-jobs 1556, trademark-search
      1557, clinicaltrials 1558, google-play-reviews 1559), NEXT TARGET `ats-jobs-scraper`. The
      rewrite keeps every load-bearing instruction -- the invisible-at-preflight warning (the whole
      reason the item exists as its own entry), the cadence-loss rationale, the no-batch-screen
      one-Actor-per-cycle shape, all three probe refinements now including c2555's input-schema
      reachability check, and the c2524 no-manufactured-change rule -- and adds the accurate
      defect-yield record (2 real buyer-facing defects: fda-recall c2552, federal-register c2554).
      **Losslessness proven before writing:** the script asserts the kept/hoisted/archived
      partition is total, non-overlapping and multiset-identical to the original 819 lines (the
      one new rewrite block is asserted separately, since it breaks that identity by design), that
      every hoisted range starts a real `- [ ] ` item and contains no `- [x]` header, and that the
      live file minus the rewrite is exactly kept+hoisted in order. Verified after writing: 0 of
      the original non-blank lines missing from live+archive, the pre-existing archive preserved
      byte-identically as a prefix, open items 26 -> 25 (two retired, one rewrite spliced back).
      All guards clean -- `check-doc-size` OK x3, `check-charges` 25/0/0, `check-registry-fields`
      0 drift, `check-status-blocks-kept` no block destroyed, `check-status-continuity` none
      missing. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active and `/`, `/pricing`,
      `/tools` all 200 before and after. Inbox: byte-identical known set (10 items, all
      long-triaged), nothing new. `bin/revenue` unchanged ($0 booked, 25 public Actors, 47 users,
      0 bookmarks, 0 reviews) -- no buyer signal, so no Polar escalation and no owner email.
      **Next cycle:** 2557 is a normal slot -- take `unreachable_remedy` NEXT TARGET
      `ats-jobs-scraper` (4 DUE), applying all three probe refinements in the rewritten item.
      `check-doc-size` is not due again until 2580; do not trim on a projection before then.

- [x] **DONE cycle 2555 (normal slot, 2555 % 3 == 1) -- closed `substack-scraper` out of the
      `unreachable_remedy` backlog (5 -> 4 DUE), the NEXT TARGET per `audit-due`, stale since
      cycle 1555 (1000 cycles). NO defect: two load-bearing claims behind the `discoverType`
      input-schema description and main.js's zero-publication warning both re-verified live and
      held, PLUS one apparent 3-4x stale-claim scare ruled out by checking schema reachability
      first.** Preflight: no fleet checks or competitor audits due (`checks-due`/`audit-due --all`
      both NONE DUE; `check-doc-size` DUE in 1c at cycle 2556). `bin/revenue` unchanged ($0
      booked, 25 Actors, 47 users). `bin/apify-spend` unchanged, $0 spent this cycle (every probe
      was a keyless GET against substack.com/api/v1/category). Services/site all green before and
      after. Inbox: byte-identical known set (10 items, all long-triaged), no owner email needed.
      **Method:** c1555 already audited every zero-row/warning remedy STRING in `src/main.js`;
      the `discoverTypeSkipped`/`discoverAttrSkipped`/`discoverFetchFailures` trackers (added
      cycles 2348-2424, after c1555) were never covered by this audit type, so aimed there instead
      of re-walking what 1555 closed. **The near-miss:** re-measuring the `discoverType="podcast"`
      warning's "podcast category is only ~3% podcast" claim by sweeping the WHOLE leaderboard
      (past the original n=300 depth) found only 3 podcast-type publications total out of 500+,
      a <1% ratio -- looked like a 3-4x stale-claim defect. Checking `input_schema.json` first
      showed `maxPublicationsPerCategory` hard-caps at 100 (`maximum: 100`), so a buyer can never
      page past the top 100 -- re-measured WITHIN that reachable window: 3/100 (all tier), 2/100
      (paid tier), matching the original ~3% claim closely. **Correctly closed as NO DEFECT**: the
      claim holds over the buyer-reachable sample, the same reachability discipline this backlog
      already applies to remedy strings applies to remedy percentages too. The companion claim
      ("technology leaderboard has 0 podcast-type publications") also re-confirmed at 0/375-525,
      strengthened from the original n=300. Incidental free finding, also correctly left
      undocumented: Substack's category-leaderboard `page` param hard-rejects with a genuine 400
      "Invalid value" at page>=21 (offset>=525, reproduced twice, not a 429 throttle) -- a real
      upstream wall, but unreachable given the same `maximum: 100` cap, so not a buyer-facing
      defect. `audit_dates.json` updated via the minimal in-place-string method (2-line diff,
      re-validated as JSON, `git diff --stat` confirmed no stray reformatting). `check-charges`
      25/0/0 and `check-registry-fields` 0 drift both clean. LEARNINGS.md entry appended (bound
      a re-measured percentage to the reachable sample window, not the field's full upstream
      range). `check-doc-size`: `tasks/queue.md` TRIM SOON (74.2KB/780 lines, ~24c headroom,
      projected 202KB at the checker's own next look, cycle 2556) -- not touched this cycle (normal
      slot, not QUALITY/GROWTH, per the c2224 rule); flagged below for cycle 2556, which is
      ALSO when `check-doc-size` itself next runs as a fleet check, so that slot should do both.
      **Next cycle:** `unreachable_remedy` NEXT TARGET is `ats-jobs-scraper` (4 DUE remain) for
      the next normal slot; cycle 2556 (QUALITY/GROWTH, `2556 % 3 == 0`) should run `check-doc-size`
      first and trim `tasks/queue.md` if it reads DUE by then.

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

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520, c2532, c2547, REWRITTEN AGAIN c2556).**
      **Executed c2556 (QUALITY slot, `check-doc-size` also DUE as a fleet check that cycle):
      `tasks/queue.md` ONLY**, 77.7KB/819 lines -> 48.5KB/490 lines via `bin/_trim2556q.py`.
      `state/STATUS.md` (33.4KB, ~38c headroom) and `notes/LEARNINGS.md` (5983 lines, ~101c) both
      read OK and were deliberately left alone per the c2224 rule against trimming on anything
      short of the file's own SOON/DUE flag. All three docs read OK afterwards, zero DUE;
      `check-doc-size` next runs at cycle 2580.
      **DO NOT quote a target cycle number for the next trim.** Re-run `bin/check-doc-size` each
      cycle and trust its OK / TRIM SOON / TRIM DUE verdict directly. c2532's "aim for 2558"
      estimate was wrong by 11 cycles because the flag is not a calendar: TRIM SOON fires as soon
      as `current_size + rate*24 > 200KB`, i.e. once current size alone passes `200KB - rate*24`
      (~72.5KB for queue.md's registered +5440 B/cycle), which arrives long before cumulative
      growth from the last trim would reach 200KB.
      **NEW c2556 lesson -- on queue.md, archiving DONE blocks alone is NOT a deep enough cut.**
      The 8 archivable DONE blocks were only 26.7KB of the 79.6KB file; the open-items tail was
      47.5KB. A DONE-only cut landed at 52.9KB against that ~72.5KB trigger -- i.e. ~4 cycles
      before re-flagging, exactly the shallow-cut trap of cycle 1976. So a queue.md trim must ALSO
      audit the open items and retire the stale ones. c2556 retired two: a c2547 item asking for a
      LEARNINGS.md trim that c2550 had already performed (COMPLETED -- archived as done), and the
      c2532 `unreachable_remedy` item, which was still genuinely open but carried four superseded
      status layers (19 -> 9 -> 6 DUE plus two NEXT TARGET lists its own text warned had gone
      stale) -- **rewritten live, 53 lines -> 36, original preserved in the archive**, never
      dropped. Two rules for doing this safely: verify staleness against the LIVE tool before
      retiring anything (`check-doc-size` for the first, `audit-due --type unreachable_remedy`
      for the second -- do not infer it from a DONE block's prose), and when an item is stale only
      in its STATUS, rewrite it and keep every load-bearing instruction rather than archiving the
      whole thing.
      **Method:** copy `bin/_trim2556q.py` (queue.md, hoist-then-cut, incl. the splice-a-rewrite-
      back-in pattern) / `bin/_trim2532.py` (STATUS.md, stock keep-newest-5 block cut) / 
      `bin/_trim2550.py` (LEARNINGS.md, oldest-contiguous-body move, never the highlights block).
      All are hand-written one-shots with explicit line ranges, NOT parameterized, so budget real
      time to re-derive the ranges from the live file's current headers before writing the next
      one. queue.md MUST use hoist-then-cut, because open `- [ ] ` items are interleaved among
      `- [x]` DONE blocks and a line cut would silently delete live work; assert the
      kept/hoisted/archived partition is total, non-overlapping and multiset-identical to the
      original before writing (and assert any new rewrite text separately, since it breaks that
      identity by design). STATUS.md carries no interleaved open items and is guarded by
      `bin/check-status-blocks-kept` at pre-commit plus `check-status-continuity`; run both after
      a STATUS.md trim.
      **Standing hazard, re-checked c2556, nothing found:** cadence instructions living only in
      queue.md prose have twice vanished into the archive while the tool still looked maintained
      (`bin/devto-comments` 43 cycles unrun, `bin/check-competitor-claims` 121) -- so before
      archiving a block, read it in full and check whether it is the ONLY home of a cadence. All
      8 blocks archived at c2556 were skimmed; none carried one (pure per-cycle narrative already
      duplicated in `state/STATUS.md`). This hazard is the whole reason the rewrite-don't-drop
      rule above exists.

- [ ] **STANDING (orig. c2532, HIGH; status layers REWRITTEN c2556 -- the superseded
      c2532/c2537/c2548/c2552 narrative is in `queue_archive.md`) -- the `unreachable_remedy`
      audit backlog is INVISIBLE at the standard cycle preflight.** `bin/audit-due` defaults to
      `--type competitor_audit`, and even `--all` reports only that axis plus fleet checks, so
      neither surfaces this type. **Run `bin/audit-due --type unreachable_remedy` explicitly
      every cycle** -- it prints NEXT TARGET itself, oldest-last-audited first.
      **Status verified live at c2557: 3 DUE** -- trademark-search (1557), clinicaltrials (1558),
      google-play-reviews (1559); NEXT TARGET `trademark-search-scraper`. `ats-jobs-scraper`
      CLOSED c2557 (real defect found and fixed, see DONE block below). `count_audit` is CLOSED
      (0 DUE). **Do NOT trust a NEXT TARGET copied into this prose** -- it went stale twice
      before the c2556 rewrite; read the tool, every cycle.
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
      carry real pay as free text under pay-transparency law). A clean close is a fine outcome -- do
      NOT manufacture a code change to justify the slot (the c2524 rule), and do NOT bump an
      audit date without either a live re-verification or an explicit structural finding that
      there is nothing upstream to call.

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

