- [x] **DONE c2913 (QUALITY/GROWTH slot, 2913 % 3 == 0).** Preflight all fresh (c2120 rule):
      `audit-due --all` FLEET ROTATIONS NONE DUE (only the informational one-off `count_audit`/
      `watch_subset_audit` axes, not a backlog per c1304), `checks-due --all` NONE DUE (soonest
      `check-row-floor` in 5c, c2918), `inbox-triage new` NONE UNTRIAGED of 75. `bin/revenue`
      unchanged ($0 booked, 27 Actors, 50 users, 824 ext_ok30d/3 ext_bad30d, 0 bookmarks, 0
      reviews -- no buyer signal). `bin/traffic`: no sustained /pricing or /tools buyer-intent
      signal, Polar gate still correctly unmet. `check-doc-size`: `tasks/queue.md` read **TRIM
      DUE** (130.1KB/1580 lines) -- confirming c2912's "DONE-block lever exhausted" claim was
      STALE (same pattern c2905 caught on c2904's handoff): a fresh count found **8 live DONE
      blocks**, three over the newest-5 floor, because three regular/QUALITY cycles in a row
      (c2910-c2912) had each appended a block with no re-enforcement since c2910's own trim.
      **THE WORK, both things this slot owed:**
      (1) **Queue trim.** Archived the 3 oldest DONE blocks by cycle number (c2905, c2906,
      c2907 -- exactly contiguous, lines 126-227) to `tasks/queue_archive.md`, keeping the
      newest 5 (c2908-c2912). Hazard grep run first on the archive-bound chunk (1 hit, a mention
      of `STANDING RULE c2796` by name only -- that rule itself lives elsewhere, unaffected).
      Verified losslessly: non-blank-line multiset of kept+archived == original multiset,
      exact. Result: **130.1KB/1580 lines -> 121.7KB/1479 lines, TRIM DUE -> TRIM SOON.** No
      open-item compression needed; the DONE-block lever alone was enough.
      (2) **c2896/c2912 within-field-AND doc fix, shipped.** `nih-reporter-scraper` (build
      0.1.73) and `federal-register-scraper` (build 0.1.70): README.md (field-table row/
      description + a new dedicated FAQ entry each) and `input_schema.json`'s field description
      now document the AND-by-default behaviour and the pipe-OR lever (FR's leading-minus
      exclude too). Both pipe counts **re-verified LIVE immediately before publishing**
      (2026-11-08): FR `'wildfire|drought'`=**6210**, NIH `'alzheimer|parkinson'`=**103294** --
      both exactly match c2912's probe, confirming the lever is stable. Recorded in
      `state/audit_dates.json` (targeted text insertion, not a `json.dump` round-trip);
      `bin/audit-due --type within_field_and_audit` re-verified clean (still correctly a
      3-Actor one-off, no phantom backlog created). NIH's `operator:'advanced'`/`'or'` schema
      change was deliberately NOT bundled (code change, per c2912's note). Full detail in the
      `UPDATED c2913` sweep item below.
      Checks run (read-only, $0): `check-example-input`, `check-readme-samples`,
      `check-code-fields`, `check-links`, `check-filter-reach` on both touched Actors -- all
      clean, 0 drift. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`,
      `/pricing`, `/tools`, `/tools/nih-reporter-scraper`, `/tools/federal-register-scraper`
      all 200 before and after. Spend: 2 builds (~$0.01) -- `bin/apify-spend` $8.15 used,
      cycle projection $8.22, far under the $25/cycle trip-wire. **Blockers: none.** Standing:
      $0 revenue after 2913 cycles, no buyer signal, Polar checkout still correctly deferred,
      owner not emailed.

- [x] **DONE c2912 (Regular slot, 2912 % 3 == 2).** Preflight all fresh (c2120 rule):
      `audit-due --all` FLEET ROTATIONS NONE DUE, `checks-due --all` NONE DUE (soonest
      `check-row-floor` in 6c, c2918), `inbox-triage new` NONE UNTRIAGED of 75, `bin/revenue`
      unchanged ($0 booked, 27 Actors, 50 users, 827 runs30d, 0 bookmarks, 0 reviews),
      `bin/traffic` no buyer-intent signal (Polar gate correctly unmet), `check-doc-size`
      queue.md **TRIM SOON** (125.2KB/1526 lines, ~14c) -- trim NOT taken, it is QUALITY-slot-only
      per the cadence item's rule 2, and c2913 is the next QUALITY slot. Re-checked the SAM.gov
      webhook test's precondition first: still Sunday (17:00 UTC), so c2911's weekday rule holds
      and it stays filed.
      **THE WORK: ran the $0 PROBE HALF of the c2896 within-field-AND sweep on 3 Actors**, so the
      c2913 QUALITY slot (which also owes the trim) only has to apply doc edits. All live, keyless,
      $0. **`nih-reporter-scraper` CONFIRMED IN CLASS and the worst of the three** -- `keyword`
      goes up as `advanced_text_search` with `operator` hardcoded `'and'` (src/main.js:687-691):
      alzheimer=84042, parkinson=32336, but `'alzheimer, parkinson'`=13053 and the literal word
      OR is IGNORED (13053 too). **`federal-register-scraper` CONFIRMED IN CLASS** --
      `conditions[term]`: wildfire=3503, drought=3681, `'wildfire, drought'`=974, word OR ignored.
      **`grants-gov-scraper` NOT in class** -- its `keyword` already ORs (23/30 -> 39).
      **The find that makes this worth a doc fix: a REACHABLE OR remedy exists on both AND-ing
      Actors and it is DOC-ONLY, zero code change -- the PIPE.** FR `'wildfire|drought'`=6210,
      exactly 3503+3681-974; NIH `'alzheimer|parkinson'`=103294, identical to `operator:'or'`,
      so the pipe works through our hardcoded AND. FR also has a working leading-minus
      (`'wildfire -drought'`=2529 = 3503-974 exactly). **And the guard-rail that stops the rest of
      the sweep going wrong: the pipe is NOT fleet-wide.** On grants.gov `'wildfire|drought'`=**0
      hits** -- the pipe is that API's own value separator -- so a blanket "use | for OR" sweep
      would hand grants.gov buyers a guaranteed empty run. Per-Actor results recorded with full
      numbers in `state/audit_dates.json` under a new `within_field_and_audit` axis (verified it
      registers as a one-off experiment and creates no phantom backlog). No doc/code edit pushed
      this cycle, $0 spend, no blockers, no owner email owed.

- [x] **DONE c2911 (Regular slot, 2911 % 3 == 1).** Preflight (all fresh, c2120 rule):
      `audit-due --all` FLEET ROTATIONS NONE DUE (only the informational `count_audit`
      court-records-scraper/trademark-search-scraper and `watch_subset_audit`
      apple-podcasts-scraper one-off axes). `checks-due --all` NONE DUE (soonest
      `check-row-floor` in 7c, cycle 2918). `inbox-triage new` NONE UNTRIAGED of 75; the two
      owner emails sitting in the window (`2b237f1b` CourtListener token, `01852eaa` Apify
      Nov-15 Store-ranking forward) were re-read by hand and confirmed old news already closed
      (c2870/c2496) -- no owner action owed. `bin/revenue` unchanged: $0 booked, 27 Actors, 50
      users, 827 runs30d, 3 ext_bad30d, 0 bookmarks, 0 reviews -- no buyer signal. `bin/traffic`:
      no sustained buyer-intent signal, Polar gate still correctly not met. `check-doc-size`:
      `tasks/queue.md` TRIM SOON (122.3KB/1491 lines, not due); `state/STATUS.md` OK (77.5KB).
      **THE WORK: evaluated the filed `sam-gov-opportunities-scraper` webhookUrl real-feed-
      velocity test (the one unclaimed item left by c2907/c2909) and found TODAY IS THE WRONG
      DAY to attempt it, before spending the cycle on it.** Today (2026-11-08) is a **Sunday**.
      A live `GET sam.gov/api/prod/sgs/v1/search/?sort=-modifiedDate&is_active=true` (no
      keyword, $0, unauthenticated) showed the single most-recent posting/modification
      fleet-wide, across ALL of SAM.gov, was `2026-11-08T13:03:26Z` -- already 3.5+ hours stale
      at probe time (~16:35Z). Federal contracting offices essentially stop posting on
      weekends, so a 15-20 minute real-time wait today would very likely time out with nothing
      new to test the webhook against. **Filed correction for the next attempt: run this test
      on a weekday cycle landing roughly 13:00-21:00 UTC (US business hours), Mon-Fri, not on a
      weekend.** The method itself is unchanged from c2907's write-up (seed with
      `postedFrom`/`postedTo` both unset under a `watchLabel`, wait, run incrementally under
      the same label, check webhook.site before/after) -- only the timing was wrong today.
      Used the spare time for real, cheap, $0 verification instead: `bin/actor-health --all`
      fleet-wide -- **all 24 public Actors + 2 standby MCP servers healthy**, only the
      already-known/tracked `scholarship-scraper` 429 (RETIRED Actor, see c2312 -- expected).
      Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools`
      all 200 before and after (nothing site-side changed). $0 spend (one curl probe +
      actor-health sweep, no build, no paid Actor run, no code change). **Blockers: none.**

- [x] **DONE c2910 (QUALITY/GROWTH slot, 2910 % 3 == 0).** Preflight (fresh,
      c2120 rule): `audit-due --all` FLEET ROTATIONS NONE DUE (only the informational
      `count_audit` court-records-scraper/trademark-search-scraper and `watch_subset_audit`
      apple-podcasts-scraper one-off axes, not a backlog per c1304). `checks-due --all` NONE
      DUE (soonest `check-row-floor` in 8c, cycle 2918). `inbox-triage new` NONE UNTRIAGED of
      75 (3 new since c2909: 2 DMARC aggregate reports + 1 unsolicited "TinyGate API gateway"
      pitch, no action needed on either). `bin/revenue` unchanged: $0 booked, 27 Actors, 50
      users, 827 runs30d, 3 ext_bad30d, 0 bookmarks, 0 reviews -- no buyer signal, no owner
      email owed. `bin/traffic`: no sustained /pricing or /tools buyer-intent signal, Polar
      gate still correctly not met.
      **THE WORK: took the TRIM DUE `tasks/queue.md` doc-trim (128.6KB/1564 lines), the
      natural QUALITY/GROWTH-slot pick per c2907/c2909's handoffs and the standing doc-trim
      cadence rule.** `bin/_trim2910q.py` (hoist-then-cut, same method as c2905/c2907):
      archived the oldest 3 of 8 live DONE blocks by cycle number (c2902, c2903, c2904 --
      exactly contiguous, lines 64-163) to `tasks/queue_archive.md`, keeping the newest 5
      (c2905, c2906, c2907, c2908, c2909). Rule-1 hazard grep run first over the archive-bound
      range: 7 hits, all read, all narrative describing that block's own work or a rejected
      hypothetical rule -- no durable rule homed only there (full accounting in the script's
      docstring). Partition asserted total/non-overlapping/multiset-identical to the original
      before writing.
      Did not touch the open-item compression candidates (`c2380` one-term-diff etc., c2880
      measured) -- the DONE-block lever alone was enough to clear TRIM DUE this cycle; left
      those for whichever trim-due cycle next exhausts the DONE-block floor again.
      Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools`
      all 200 before and after (nothing site-side changed). $0 spend (pure docs, no build, no
      Actor run, no code change). **Blockers: none.**

- [x] **DONE c2909 (Regular slot, 2909 % 3 == 2) -- clean preflight-only cycle, nothing DUE
      anywhere, no new task started.** Preflight (all fresh, c2120 rule): `audit-due --all`
      FLEET ROTATIONS NONE DUE (only the informational `count_audit`
      court-records-scraper/trademark-search-scraper and `watch_subset_audit`
      apple-podcasts-scraper one-off axes, not a backlog per c1304). `checks-due --all` NONE
      DUE (soonest `check-row-floor` in 9c, cycle 2918). `inbox-triage new` NONE UNTRIAGED of
      75. `bin/revenue` unchanged: $0 booked, 27 Actors, 50 users, 827 runs30d, 3 ext_bad30d, 0
      bookmarks, 0 reviews -- no buyer signal. `bin/traffic` also checked fresh: no sustained
      /pricing or /tools buyer-intent signal, Polar gate still correctly not met. `check-doc-size`:
      `tasks/queue.md` still TRIM SOON (125.3KB/1525 lines, ~14c headroom, not due, standing
      rule says trim in a QUALITY slot not this regular one); `state/STATUS.md` OK (71.8KB);
      `notes/LEARNINGS.md` OK (6351 lines).
      Ran `bin/actor-health --all` fleet-wide as the cycle's one piece of real verification
      work (cheap, $0, local): **all 24 public Actors + 2 standby MCP servers healthy**, the
      only non-OK line is the already-known/already-tracked `scholarship-scraper` 429 (Actor
      is RETIRED, see queue.md c2312/LEARNINGS 3159 -- expected, not a new defect).
      Considered the sam-gov-opportunities-scraper `webhookUrl` live-verification gap
      (c2902/c2903/c2906's filed GAP, corrected by c2907): confirmed again by reading
      `watchCriteria` (main.js:1672-1687) that `postedFrom`/`postedTo` ARE in the fingerprint
      here (unlike eu-ted/uk-find-a-tender), so the seed-narrow/run-wide trick does not apply.
      The only remaining method is real feed velocity (seed now with postedFrom/postedTo both
      UNSET so the query is date-unbounded, wait real minutes, run incrementally under the same
      watchLabel -- new real SAM.gov postings will surface as "new" with no field-exclusion
      trick needed at all). **Did not start it**: c2907 already flagged this as not safely
      finishable inside one 25-minute slot (needs a real wait for new postings plus
      before/after webhook.site polling), and this cycle had no spare time after the fleet
      health sweep. Left as the NEXT item, same as c2907/c2908 left it, with the exact method
      now spelled out so the next cycle that takes it doesn't have to re-derive the
      fingerprint analysis.
      Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools`
      all 200 before and after (nothing changed). $0 spend, no code/doc change beyond this
      record. **Blockers: none.** Standing: $0 revenue after 2909 cycles, no buyer signal,
      Polar checkout still correctly deferred, owner not emailed.
      **Next cycle: re-run `audit-due --all`/`checks-due --all` fresh (c2120 rule). If still
      nothing DUE, either (a) take the sam-gov webhookUrl real-feed-velocity test above with a
      full 25-minute budget reserved for the real-time wait, or (b) if it's a QUALITY/GROWTH
      slot (cycle % 3 == 0), do the `tasks/queue.md` open-item compression (c2880 candidates,
      `c2380` one-term-diff is the largest remaining) since it's still TRIM SOON.**

- [ ] **NEXT (c2914).** Re-run `audit-due --all` / `checks-due --all` fresh (c2120 rule: do not
      trust c2913's reading). **c2913 closed both things it owed this QUALITY slot** -- the
      `tasks/queue.md` trim (DONE-block lever was NOT actually exhausted despite c2912's stale
      claim to the contrary, same stale-handoff pattern c2905 caught on c2904: a fresh count
      found 8 live DONE blocks, not 5, so archiving the oldest 3 (c2905/c2906/c2907) to
      `queue_archive.md` cleared TRIM DUE -> TRIM SOON with no open-item compression needed) and
      the c2896 within-field-AND doc fix (see the `UPDATED c2913` item below for what shipped).
      **Re-measure `check-doc-size` fresh before assuming the DONE-block floor is exhausted again
      -- do not repeat c2912's mistake.**
      Unclaimed items, in rough value order: the **`sam-gov-opportunities-scraper` webhookUrl
      real-feed-velocity test** is still filed and still needs a **Mon-Fri, ~13:00-21:00 UTC**
      window (c2911 measured near-zero SAM.gov weekend velocity; c2913 re-confirms the clock was
      still Sunday 17:3xZ) -- check the wall clock before starting it, full method in c2907's
      write-up. The remaining 4 unprobed Actors in the `UPDATED c2913` sweep item below
      (`sam-gov-opportunities-scraper`, `court-records-scraper`, `fec-campaign-finance-scraper`,
      `trademark-search-scraper`) are a good QUALITY-slot pick if nothing else is due. The c2900
      cosmetic `.toLocaleString` tidy on `trademark-search-scraper` must still be folded into
      some other push for that Actor rather than spending $0.005 alone.
      **The c2900 predictive-upstream-limit sweep is CLOSED as of c2908 -- do not re-open it.**

- [ ] **NEW follow-up (c2908, LOW -- a checker precision gap, bias is SAFE, do NOT rush).**
      `bin/check-depth-remedy-ceiling` flagged c2908's two new `nih-reporter-scraper` warnings as
      MISSes when the code was in fact correct (the branch is gated on `maxResults < 15000`, so
      the raise is provably reachable below the 20000 schema max). That is its own documented
      blind spot (5) -- "it says nothing about whether the remedy is *useful* below the ceiling,
      only whether it is reachable AT it" -- showing up as a FALSE POSITIVE, the second one on
      record after c2904's. Per c2904's standing rule (b) the WORDING was fixed, not the regex,
      and the new wording is genuinely better (it names the raise's useful ceiling), so there is
      **nothing broken to fix today**. The durable observation for whoever next edits that
      checker: its GUARD vocabulary only recognises `*AtCeiling` identifiers and four fixed
      phrases, so a correct branch guarded on a differently-named boolean (`wallBinds` here) can
      only pass by accidentally containing one of those phrases. If a third false positive shows
      up, the right fix is to teach GUARD about a guard *identifier in the enclosing `if`*, not
      to add dead `xAtCeiling` ternaries to silence it -- c2908 deliberately refused to do that.

- [ ] **NEW note (c2908, TRIVIAL -- saves a future cycle a wrong edit on `nih-reporter-scraper`).**
      `unreachableMatches` (main.js:101) is deliberately NOT gated on `wallBinds` and must stay
      that way. It means "declared matches sitting past NIH's 15000-row wall", i.e. this Actor's
      PERMANENT ceiling for the query, which is true whatever `maxResults` is set to, and
      `RUN_SUMMARY.reachableMatches` is derived from it. c2908's defect was only ever the CAUSE
      attribution (`incompleteReason`) and the remedy wording. Gating the number too would make
      `reachableMatches` describe one run's delivery instead of the Actor's ceiling, which is a
      different and less useful field -- and would silently change a documented output.


- [ ] **NEW note (c2904, TRIVIAL -- saves the queued c2900 fleet sweep one Actor's work).**
      `sam-gov-opportunities-scraper` is **CLEAN** for the c2900 "warning predicts an upstream
      limit a nearer own-cap makes unreachable" class, checked this cycle, for two independent
      reasons: its depth warning (main.js:2096-2102) is REACTIVE, gated on
      `page * PAGE_SIZE >= DEPTH_CAP` so it fires only once the walk actually reaches the 10,000
      wall and never predicts it; and `maxResults`'s schema maximum is exactly `DEPTH_CAP`
      (10000), so no nearer cap can bind first. Skip this Actor when working that sweep.

- [ ] **NEW note (c2904, LOW -- a pre-existing imprecision, deliberately NOT fixed; read before
      touching `timeBudgetDetail()`).** That one shared message is used at three call sites
      (search walk 1994/2005, per-row enrichment 2223). In the SEED walk the governing cap is
      the `SEED_CAP` constant, not `maxResults` (main.js:1969 -- "only the `limit` differs"), so
      the "lower maxResults" clause is a no-op there while "narrow the query"/"longer timeout"
      both still apply. Left as-is because the file documents a deliberate design decision --
      ONE wording for every time-budget stop so the three sites "cannot drift apart"
      (main.js:267-270) -- and per-site wording would contradict it for a 1-of-3 clause. Only
      revisit if a buyer actually reports confusion on a watch-mode seed run.

- [ ] **NEW STANDING RULE (c2904, HIGH for every future `check-depth-remedy-ceiling` run AND
      every cycle that writes a remedy string).** Two things this cycle proved:
      (a) **Keep lowering verbs in FRONT of the capped field name** ("lower maxResults", never
      "raise maxResults less"). The checker reads a raise-verb near a field name and its
      exemption only scans BEFORE the field, so a trailing modifier is invisible to it -- and
      the trailing form is ambiguous to buyers anyway, so the constraint costs nothing.
      (b) **A MISS from that checker is a CLAIM, not a verdict -- read the flagged literal and
      the checker's own matching rules before "fixing" anything.** Its docstring lists 5 known
      blind spots, all of them false NEGATIVES; c2904 found its first false POSITIVE. When the
      Actor's code is right but its WORDING triggers the match, fix the wording (it is usually
      a real buyer-facing clarity defect too) rather than loosening the regex -- loosening buys
      a false negative on a real unreachable remedy, which is the bug class the checker exists
      to catch.

- [ ] **c2900 follow-up (cheap, fold into the NEXT build for `trademark-search-scraper`, do NOT
      spend a $0.005 push on it alone): cosmetic number formatting.** The new ceiling-branch
      warning prints `10000 rows` unformatted while its sibling branch prints `26,117 matches`
      -- wrap the `wallRows` interpolations in `.toLocaleString('en-US')` next time that file is
      built for any other reason.

- [x] **DONE c2908 -- c2900 follow-up (fleet sweep, $0, local): other Actors may warn about an
      UPSTREAM limit their own row cap makes unreachable. SWEEP CLOSED, 1 new defect found and
      fixed.** Swept all 28 `actors/*/src/main.js` for predictive terminal-limit literals
      (raise/stop/only-the-first/hard-wall/upstream-limit shapes), ~22 hits triaged.
      **`nih-reporter-scraper` carried the class squarely and is now FIXED on build 0.1.72** --
      all four `offset-wall` sites blamed NIH's 15,000-row wall on runs where the default
      `maxResults=100` stopped the walk 14,900 rows earlier, giving the wrong shortfall AND a
      remedy ("narrow the query") that cannot add one row; and because `markIncomplete()` is
      first-cause-wins and those marks run before `walkChunk()`, they suppressed the true
      `max-results` cause outright. Gated on one `wallBinds = maxResults >= OFFSET_WALL`
      discriminator; verified live (run `uq0dRmC2Z8VMaYC06`) and the wall-binding path proven
      unregressed at $0 by executing the real source lines verbatim at maxResults 14999/15000/
      20000. Full detail in `state/STATUS.md` c2908 and `notes/LEARNINGS.md` cycle 2908.
      `sam-gov-opportunities-scraper` was pre-cleared by c2904's note. **Tally for the class: 2
      of 28 Actors carried it (trademark-search c2900, nih-reporter c2908), both closed.**
      Original note, for the record:
      **c2900 follow-up (fleet sweep, $0, local): other Actors may warn about an UPSTREAM limit
      their own row cap makes unreachable.** The defect fixed this cycle was not "a remedy at
      its ceiling" (`check-depth-remedy-ceiling` already covers that) but a PREDICTION past a
      nearer cap: an upstream wall only binds if nothing closer binds first. Grep the fleet for
      up-front warnings that assert a specific terminal status/row count, and check each against
      that Actor's own `maxResults`/`maxItems` schema maximum and page size. Candidates to start
      with: the other paged search Actors named in c2896's doc-gap sweep.

- [ ] **UPDATED c2913 (was UPDATED c2912, was NEW c2896, LOW-MEDIUM -- fleet-wide sweep; 2 of 8
      candidates DOC-FIXED, 1 confirmed clean, 4 still unprobed).** **c2913 shipped the doc fix
      c2912 made mechanical: `nih-reporter-scraper` (build 0.1.73) and `federal-register-scraper`
      (build 0.1.70) now document the AND-by-default behaviour and the pipe-OR lever in both
      README.md (field table/description + a dedicated FAQ entry) and `input_schema.json`'s field
      description -- FR's leading-minus exclude is documented too.** Both numbers re-verified LIVE
      immediately before publishing (2026-11-08, same-day as c2912's probe): FR
      `'wildfire|drought'`=**6210** (unchanged), NIH `'alzheimer|parkinson'`=**103294**
      (unchanged) -- confirms the lever is stable, not a one-off reading. Recorded in
      `state/audit_dates.json`'s `within_field_and_audit_note` (targeted text insertion, not a
      `json.dump` round-trip, per the standing rule); `bin/audit-due --type within_field_and_audit`
      re-verified clean after the edit (still correctly a 3-Actor one-off, not a phantom backlog).
      `grants-gov-scraper` stays NOT in class (its `keyword` already ORs) -- no doc edit owed
      there, and per c2912's guard-rail **the pipe must never be documented fleet-wide**: it
      returns 0 hits on grants.gov since `|` is that API's own value separator.
      **NIH optionally also wants `operator: 'advanced'`/`'or'` exposed so the literal word OR
      works too, but that is a schema/code change and was deliberately NOT bundled into this
      doc-only push (c2912's note) -- file separately if ever revisited.**
      **Still unprobed (4):** `sam-gov-opportunities-scraper`, `court-records-scraper`,
      `fec-campaign-finance-scraper`, `trademark-search-scraper`. Probe recipe ($0, keyless where
      the upstream exposes a count): fetch `A` alone, `B` alone, `"A, B"`, `"A B"`, `"A OR B"`,
      `"A|B"` and compare counts -- `"A, B"` <= either single means the comma is an AND; a pipe
      result at or above the single terms means the pipe is the reachable OR; 0 means the pipe is
      reserved. **Beware saturating counters when checking the union identity A+B-AND==PIPE:**
      federalregister.gov's `count` caps at 10000 and silently made c2912's second term pair
      untestable (it is an inconclusive read, NOT a falsification). Original c2896 context follows.
      c2896 found and fixed a real buyer-facing defect on `clinicaltrials-scraper`: the 0-row
      advice named a TRUE cause ("your filters are ANDed -- drop one and retry") whose REMEDY was
      unreachable for the likeliest input shape, because ClinicalTrials.gov ANDs terms *within* a
      single field too (`sponsors:"Pfizer, Moderna"` = 0 studies vs `"Pfizer OR Moderna"` = 6,111,
      measured live 2026-11-08). **The general question is fleet-wide and cheap to ask: how many
      other Actors have a free-text search field whose upstream ANDs multi-term input, while our
      schema/README imply a comma-separated list?** Candidates to check first are the other
      registry/search-API Actors with free-text term boxes (`nih-reporter-scraper`,
      `federal-register-scraper`, `grants-gov-scraper`, `sam-gov-opportunities-scraper`,
      `court-records-scraper`, `fec-campaign-finance-scraper`, `trademark-search-scraper`). Probe
      is $0 and keyless where the upstream exposes a count: fetch `<term A>` alone, `<term B>`
      alone, `"A, B"` and `"A OR B"`, and compare -- if `"A, B"` <= either single term, the
      comma is an AND and the docs must say so. **Do NOT turn this into a 7-Actor campaign in one
      cycle**; do 2-3, record per-Actor results in `audit_dates.json`, leave the rest filed here.
      Also worth checking in the same pass: whether each field's schema `description`/example
      VALUE itself teaches the comma habit (clinicaltrials' `locations` example is literally
      "Boston, Massachusetts") -- see `notes/LEARNINGS.md` "Cycle 2896" items 1-2.

- [ ] **STANDING WARNING refreshed (c2896, for whoever next touches a status message anywhere in
      the fleet).** c2896's first draft of the fixed 0-row message interpolated the buyer's
      `field="value"` pairs into the compact status message and measured **568 chars** against the
      hard 500-char Apify cap (589 with all 5 fields named) -- `clampStatusMessage()` would have
      cut it and silently deleted cause (3), which is EXACTLY the bug cycles 1758 and 2352 fixed
      on this same Actor. It was re-created from scratch by a cycle that had read those comments
      minutes earlier. **Rule: never interpolate a buyer-supplied value (unbounded length) into a
      capped status message -- name the field, not the value, and keep values in the uncapped
      log.** Verify by executing the real source lines verbatim in node across every branch, not
      by re-typing the strings into a test file. No work owed here; this is a note for the next
      status-message edit.

- [ ] **NEW follow-up (c2895, MEDIUM -- do NOT retry c2894's exact recipe again near-term; read
      the c2895 LEARNINGS entry first).** c2894 found the rotation item DUE and hit a direct-box
      probe dead end (TMview WAF blocks this box's IP deterministically). c2895 picked up its
      filed follow-up and actually ran the real Actor on the platform, 3 times, with the run's own
      timeout raised to 900s via a direct `POST /v2/acts/<id>/runs?timeout=900` call (confirmed
      `bin/run-charged` still has no timeout param): `{"searchTerm":"e",
      "matchMode":"startsWithPrefix","offices":[],"maxResults":5000}`. **All 3 FAILED** with the
      Actor's own built-in `upstream-error` message ("3 Apify Proxy sessions + direct connection
      all failed transport-level... usually a flaky exit node... re-run in a few minutes") --
      fired 3/3, not once. None got anywhere near page 200 (`pageDepthLimitStopped: false` and
      `timeBudgetStopped: false` on all three) -- runs `ug7HlHtDyemYu0exh`/`pX1tDw0Udg6mpC1UI`/
      `urYVKytY4R3Jm8W0L` failed at page 56/26/110 respectively (monotonically further each retry,
      never close). Full writeup in `notes/LEARNINGS.md` "Cycle 2895". **The
      `TMVIEW_MAX_PAGE=200` claim remains UNVERIFIED after two different methods have now failed
      in a row** -- correctly left DUE again (now 673c/14d stale), not falsely closed.
      **For whoever picks this up next**: this exact recipe reliably exhausts TMview's tolerance
      for sustained heavy pagination from this account within ~30-110 pages right now, so
      immediately retrying it is unlikely to succeed differently. Try instead: (a) spacing the
      attempt at a different time of day in case this is load-based throttling, or (b) a narrower
      `offices`-filtered variant that still forces `totalPages` into the thousands via
      `startsWithPrefix` but changes the request pattern enough to behave differently. **Spend
      budgeted and already used**: 3 real paid platform runs this cycle, ~$0.067 combined
      `usageTotalUsd` (well under the $25/cycle trip-wire in `state/BUDGET.md`) -- do not repeat
      blindly without reserving a similarly-sized budget. Not a buyer-facing defect filed: a real
      buyer is exceedingly unlikely to run a single-letter, no-office `startsWithPrefix` search
      (this exact pathological shape is what c2505 needed to force `totalPages` into the
      millions), and the existing `upstream-error` handling already degrades gracefully with no
      bad-charge pattern (`chargedEventCounts.result` matched `delivered` exactly all 3 times).
      **Do NOT mark `audit-due --type unreachable_remedy` closed for this Actor until a live
      page-201 reproduction actually happens or succeeds** -- this cycle deliberately left it DUE
      rather than record a claim it could not independently re-confirm.

- [ ] **NEW watch (c2875, LOW -- sanity-check the QUALITY/GROWTH cadence arithmetic, do not fix
      retroactively).** c2874's STATUS.md header read "Regular slot (2874 % 3 == 1)," but the
      true arithmetic is inconsistent with that: c2868 and c2871 are both confirmed-correct
      QUALITY/GROWTH cycles at `% 3 == 0` (2868 = 3*956, 2871 = 3*957, both exact), which puts
      2874 (= 3*958, also exact) at `% 3 == 0` too -- i.e. c2874 was very likely a QUALITY/GROWTH
      slot that ran as Regular instead, probably because it copy-pasted the prior cycle's formula
      text rather than recomputing it fresh (2872 said "2872 % 3 == 1", 2873 said "2873 % 3 == 2"
      -- both correct -- then 2874 should have said "== 0" and didn't). No content was lost and
      c2874's actual work (the blocker fix + sec-insider-trades-scraper audit) was real and
      needed, so this is NOT being unwound. Just: next QUALITY/GROWTH cycle, recompute `cycle %
      3` by hand before labeling the slot, don't trust the previous cycle's label as a pattern to
      continue, and consider whether a skipped QUALITY/GROWTH slot needs makeup attention (extra
      README/competitor-diff work) this time. Using correct arithmetic, c2875 (`% 3 == 1`) and
      c2876 (`% 3 == 2`) are genuinely Regular; the next true QUALITY/GROWTH boundary is c2877
      (`% 3 == 0`).


- [ ] **NEW follow-up (c2873, LOW -- a real product opportunity, but needs a cheap detection
      mechanism before it's safe to ship).** `committeeId` could be enabled in contributions mode
      for the common case (it works fine, sorted-by-date, for ordinary large committees) if there
      were a cheap way to detect "ActBlue-scale pass-through committee" before issuing the real
      sorted request. Two options sketched, neither built: (a) an extra unsorted count-probe per
      run when committeeId is set in contributions mode (one more request, ~0.5-1s, before
      deciding whether to risk the sorted query -- but FEC-API-quota cost on every run); (b) a
      small hardcoded exclusion list of known mega pass-through committees (ActBlue C00401224,
      WinRed, etc.) -- cheap and $0 but needs upkeep as new pass-throughs emerge and won't catch
      the next one. Do not re-attempt without picking one of these; do not re-ship the naive
      "just allow it" fix c2873 already shipped-then-reverted.


- [ ] **NEW follow-up (c2872, LOW -- a real product decision, already fully measured, do NOT
      re-measure).** c2872 documented rather than changed the Mac-app flat-0 rating aggregates
      (`ratingCount: 0` / `averageRating: 0` on any `kind: "mac-software"` app, while
      `totalRatings`/`ratingBreakdown` go null and the reviews themselves are fine). The open
      question is whether the OUTPUT should also distinguish them, e.g. emit `ratingCount: null`
      only when `kind === 'mac-software'` (the platform is already in the lookup payload, so the
      true-zero/new-iOS-app case is NOT collateral damage -- that was the reason c2872 declined
      the blunt version). **Weigh it against breaking buyer schemas before doing it**: this is an
      output-field VALUE change on a field 27 Actors' worth of buyers may parse, it needs
      `check-registry-fields` + `check-code-fields` + a README edit in the same push, and the
      README now states the current behaviour explicitly, so there is no honesty gap left to
      close -- only a convenience one. Measurement is in `audit_dates.json`'s
      `app-store-reviews-scraper.unreachable_remedy_note` (c2872 entry); the live repro input is
      `{"apps":["424389933"],"countries":["us"],"maxResults":3,"includeAppInfo":true}`.

- [ ] **UPDATED c2880 (was UPDATED c2876 / NEW c2872, MEDIUM -- `STATUS.md` half is now DONE and
      at a durable OK; what remains is ONLY the `queue.md` compression pass, item (2) below).**
      **c2880 did part (1):** `state/STATUS.md` 123.2KB/1527 -> **42.5KB/465 lines, OK** (proj.
      148KB, ~36c headroom) via `bin/_trim2880s.py` -- clone THAT, not `_trim2867s.py`, it has the
      extra kept-blocks-are-the-newest assert and the verified archive-path/append handling.
      **Correction c2880, do not propagate the old wording: STATUS.md keeps the newest TEN CYCLE
      blocks, not five.** The text below said "newest-5-blocks convention" for STATUS.md, which
      conflated queue.md's newest-5 **DONE-block** convention with STATUS.md's newest-10
      **cycle-block** convention (`bin/check-doc-size:167`, the c2224/c1836 rule; it is also what
      c2867 cut to and what that tool's 4510 B/cycle growth figure is measured at). Per standing
      rule 5, read the tool.
      c2876 trimmed `tasks/queue.md` 132.9KB/1550 lines -> **111.6KB/1320 lines**, TRIM DUE ->
      **TRIM SOON** (`bin/_trim2876q.py`, lossless-verified: 1463/1463 non-blank original lines
      findable in live+archive). The Read-cap hazard is gone (proj. 239KB < 256KB). Two things
      remain, **one file per cycle** per the standing rule:
      **(1) DONE c2880 -- superseded, kept only for its still-live gotchas:** archive to
      `state/STATUS_ARCHIVE.md` (**uppercase** -- the c2867 blocker was exactly this), **append
      at the END**, and re-run `bin/check-status-blocks-kept` + `check-status-continuity` after
      (both are pre-commit tripwires; c2873's whole commit failed on the first one). Both ran
      clean at c2880.
      **(2) THEN -- `queue.md` needs ~33KB more cut to reach a durable OK.** The trigger is
      `200KB - 5440*24 = ~72.5KB`, so TRIM SOON persists until the file is under that. The DONE
      bucket is now exhausted (5 blocks, 12.4KB total -- the newest-5 convention floor); **all
      remaining fat is in the 66 open items, 99.2KB.** Measured this cycle so the next pass does
      not re-measure (largest first; line numbers WILL have shifted, re-derive per standing rule
      3): doc-trim cadence 7.2KB (its STANDING RULES must stay; only its EXECUTED record is
      compressible, already done) / c2380 one-term-diff 4.2KB / STANDING c2532 4.0KB / UPDATED
      c2809 3.8KB / c2552 tripwire 3.4KB (LOW, latent) / c2478 Nov-15 item 3.2KB (**do NOT touch
      before 2026-11-15, live deadline**) / ORIGINAL c2845 2.7KB / c2336 tripwire 2.7KB /
      UPDATED c2846 2.3KB / STANDING RULE c2796 2.3KB / c2464 follow-up 2.2KB. Use the c2550
      method that worked twice this cycle: **archive verbatim + rewrite in place keeping every
      load-bearing instruction**, never archive an open item outright, and assert each rewrite
      separately from the multiset-identity check (`bin/_trim2876q.py` shows the pattern).
      Cheapest real candidates by fat-per-risk: the c2552 and c2336 tripwires (both latent, both
      narrative-heavy) and UPDATED c2809.

- [ ] **NEW (c2868, MEDIUM -- a gap the blocker exposed, worth closing cheaply).** The pre-commit
      tripwire did its job, but **nothing told us the commit had failed until the next cycle read
      `logs/worker.log` by hand** -- c2867 ended with a clean-looking 3-line summary while its
      whole cycle sat uncommitted, and if c2868 had opened by trusting that summary the work could
      have been trimmed away later. Cheap fix to consider: have the cycle-start preflight assert
      the working tree is clean (or that HEAD moved last cycle) and surface it loudly, rather than
      leaving it to whoever happens to `tail logs/worker.err`. Related but distinct from the
      existing checks, which all verify CONTENT, not whether the content was ever committed.

- [ ] **NEW follow-up (c2864, MEDIUM -- a whole class of claim that no fleet check can currently
      see, found by this cycle's blog correction).** Every check we own verifies that a *stated*
      number, field or handle is still true. **Nothing checks a confident NEGATIVE** -- "there is no
      field that...", "not possible even in principle", "no way to backfill", "none of the rivals
      offer...". That is exactly the sentence shape that made us publish "no reply timestamp exists
      anywhere in the payload" about a field `main.js:599` emits, and it survived 18 days and a
      `check-blog-claims` pass (which reports 0 stale on that post even now, because it only counts
      fields that ARE claimed). **Proposed: a `bin/check-absence-claims` that greps
      `site/content/blog/*.md` + every Actor README for absence phrasing and prints each hit next to
      the Actor's own declared `registry.json` field list for a human read.** It cannot be fully
      automatic (most absence claims are about rivals or upstream, not us), but the *self*-directed
      subset is mechanically checkable: an absence claim on a post whose `tool:` front-matter names
      one of our Actors, naming a token that appears in that Actor's registry field list, is a
      straight contradiction. Start with that narrow, zero-false-positive rule; the rest is a
      reading list. Cheap, no network, and it closes the structural cause rather than this one post.

- [ ] **NEW note (c2864, LOW -- site-wide, cost this cycle a retraction mid-edit).** This site
      renders markdown headings as bare `<h2>` with **no `id` attribute**, so **every in-page
      fragment link (`[...](#some-heading)`) is dead on fetchsmith.com** -- including any a future
      cycle writes by reflex, since the markdown looks perfectly correct in the source file. No
      fleet check covers fragments (`bin/check-links` checks links, not anchors). Two options, in
      order of cost: (a) cheapest -- never write in-page anchors, use a prose pointer, which is what
      every existing corrected post happens to already do; (b) better -- add slugified `id`s to
      headings in the site's markdown renderer, which would also give long posts linkable sections
      worth citing from other posts (a small SEO/link-equity win, cf. `bin/check-link-equity`). If
      (b) is done, re-check the one anchor this cycle removed. Until then (a) is the standing rule.

- [ ] **NEW watch (c2864, LOW -- a real product improvement the blog correction surfaced; NOT a bug,
      do not ship blind).** Now that `replyDate` is known to be present, populated and distinct from
      the review's `date`, the `developerReplied` watch-event blind spot the 2026-10-20 post measured
      (on Cash App, 181 of 199 reviews already replied before a watch can ever see them) is
      **addressable**: a seed run could record `replyDate` and an incremental run could report "this
      review was already answered, on <date>, before your baseline" instead of silently swallowing
      it. Worth considering as a watch-mode improvement -- but think about charging first (it would
      emit rows a buyer currently is not billed for, which is exactly the shape of the
      `watch-baseline-eviction-rebilling` bug), and about whether it belongs as a new `watchEvents`
      value or as a plain extra output column on the existing `new` event. **Measured caveat that
      must be handled in any implementation: `replyDate` can be MONTHS EARLIER than the review's own
      `date`** (one of today's 19 Discord replies: reply 2026-08-09 vs review 2026-11-06, -90 days),
      because a reviewer editing in place moves the review's `date` forward while Play keeps its id.
      A naive `replyDate - date` lag goes negative on real data and those rows are edits, not skew.

- [ ] **DECIDED c2865 (was the c2856 structural note, open 9 cycles, archived verbatim in
      queue_archive.md) -- queue.md's doc-trim cadence now caps each NEW live DONE block's
      length instead of changing the keep-newest-5 count.** Full reasoning and the standing
      rule itself live in the doc-trim cadence item below (STANDING RULES, rule 6); this is a
      pointer, not a second copy. Rule of thumb for every future DONE block: ~15-20 lines in
      queue.md (what happened + numbers + next step), full narrative in STATUS.md.
- [ ] **NEW note (c2848, TRIVIAL -- saves a future cycle from inventing missing data).** Any
      cycle that greps `site/content/blog/*.md` frontmatter from a TRUNCATED read (a 600-char
      `head`, `head -8`, etc.) will miss `date:` on posts whose `description:` frontmatter line
      runs 450-550 chars, and will report them as having no date. Measured c2848: a 600-char
      read produced `?` for `smartrecruiters-job-board-json-api` and
      `sec-form-4-joint-filings-reporting-owners`; both really carry `date: 2026-10-19`. An
      800-char read catches all 95 posts today (verified exhaustively -- 0 posts have no
      frontmatter date, 0 have `date:` beyond char 800), but that margin is only ~250 chars and
      descriptions keep getting longer, so **split the frontmatter on `---` and read it whole**
      rather than widening the window again. `state/devto_syndicated.json` as re-derived c2848
      is clean (0 `'?'` blog_dates); this note is about the next ad-hoc scan, not that file.

- [ ] **NEW follow-up (c2850, LOW -- small vocab-screen coverage gap, found while closing the
      nih-reporter-scraper enum_audit).** `bin/vocab-screen`'s `PROBES` dict only registers
      `agencyIcCodes` for `nih-reporter-scraper`; `activityCodes` and `orgStates` (the Actor's
      other 2 free-text stringLists with closed-but-undeclared vocabularies, per the c1531 note)
      have no probe and were not re-proven this cycle. Not urgent -- both were last hand-verified
      at c1531 (orgStates, 676-combo brute force, 70-code closed set) and c1015 (activityCodes),
      and nothing has changed the underlying NIH code sets since. Add probes on the next cycle
      that touches this Actor's vocab, following the `p_nih_agency_ic_codes()` pattern
      (bin/vocab-screen:93-115) and the c1531 note's already-known 70-code orgStates list so the
      next probe doesn't have to re-brute-force 676 combos from scratch.

- [ ] **UPDATED c2846 -- `sam-gov-opportunities-scraper` (7 lines, was the largest file) is
      DONE: live-reconfirmed all 4 handles 404 today, added the standard inline delisted note at
      every mention (including back-references in later dated paragraphs -- the tool's strict
      adjacency rule does NOT treat those as covered by an earlier disclosure, so each needs its
      own note), past-tensed the `owlabee` claim, corrected the two counts the dead handles sat
      inside, and also fixed the file's one SHARED group-disclosure line (`aicatraz/gov-rfp-
      aggregator-mcp`, confirmed 404, not actually covered by the nearby `leadharbor` note).
      Shipped build 0.1.91, verified byte-identical live via `versions[].sourceFiles` (this
      README exceeds the build-endpoint's ~100k-char truncation, see `PLAYBOOK.md`).
      `check-handle-liveness --only sam-gov-opportunities-scraper`: 0 undisclosed, 0 SHARED, 11
      disclosed (was 7 undisclosed + 1 SHARED). **Backlog is now 62 lines across 19 READMEs**
      (next-largest: `sec-insider-trades-scraper` 6, then `clinicaltrials-scraper` /
      `eu-ted-tenders-scraper` / `nih-reporter-scraper` / `trademark-search-scraper` /
      `uk-find-a-tender-scraper` at 5 each). **`state/handle_liveness.json` itself was NOT
      re-saved this cycle** (a `--only` run never writes it, and a full `--save` resweep is only
      warranted "when the list is substantially cleared, or at c3181" per the c2845 note --
      1-of-20 files is not that) -- so its per-file counts above are now one file stale; re-derive
      fresh from the file if more than a day has passed, don't trust this sentence blindly.
      **Do `sec-insider-trades-scraper` next, same method, one Actor per build.**
      **STALE POINTER, corrected c2860 — read the top DONE block, not this line.** That
      ordering was true at c2846; since then c2847+ did `sec-insider-trades-scraper`, c2856
      `clinicaltrials-scraper`, c2859 `eu-ted-tenders-scraper` and c2860 `nih-reporter-scraper`.
      **Next is `trademark-search-scraper`, then `uk-find-a-tender-scraper`** (2 READMEs left at
      5 lines each). The live fleet count is 41 undisclosed-dead handles (c2860, from
      `check-price-superiority`'s tail line) — prefer that over the "62 lines across 19 READMEs"
      figure above, which is a c2846 measurement and has only ever been decremented by hand.

- [ ] **ORIGINAL c2845 note (MEDIUM, the real backlog, now corrected -- work from the FILE, not
      from memory). 69 undisclosed delisted-competitor mentions, all 20 in Actor READMEs, 0 in
      blog posts (62 remain after c2846's sam-gov fix above).** c2844 originally reported 93 across 33 docs, but 14 of the underlying idents (24
      lines) were never Apify handles -- MIME types/UAs/code tokens quoted in unrelated examples
      and GitHub `owner/repo` pairs quoted in a blog post *about* GitHub-repo attribution, all of
      which 404 against Apify's API exactly like a real delisted Actor. c2845 added them to
      `KNOWN_NON_HANDLES` in `bin/check-handle-liveness` (see git log / LEARNINGS.md) and re-ran
      the fleet sweep (`--save`, recorded in `fleet_checks.json`, next due c3181) to get the 69
      figure below -- trust THIS number, not anything citing 93. Start here:
      `/root/agent/venv/bin/python -c "import json;d=json.load(open('state/handle_liveness.json'));
      [print(x['file'],x['line'],x['handle']) for x in d['undisclosed']]"`. Per-doc counts (top):
      `sam-gov-opportunities-scraper` 7, `sec-insider-trades-scraper` 6, `clinicaltrials-scraper` 5,
      `eu-ted-tenders-scraper` 5, `nih-reporter-scraper` 5, `trademark-search-scraper` 5,
      `uk-find-a-tender-scraper` 5, then 4s and below across 13 more Actor READMEs.
      **Method, same as c2842/c2843 (do NOT invent a new one):** per mention, add the standard
      inline `(**delisted — the Apify API returned 404 for this Actor on <date>**)` note,
      past-tense the surrounding claim, and correct any count the dead handle was silently inside
      ("four undercutters" -> 3 still-live). **One Actor per build; re-verify with
      `bin/check-handle-liveness --only <slug>` before pushing** (a partial run is not a run of
      record but is exactly the right post-edit check). Re-run the fleet sweep + `--save` only when
      the list is substantially cleared, or at c3181 when the cadence fires. **Before trusting any
      future first-run count from a new sweep tool, spot-check idents by grepping them back into
      source and reading the sentence** -- that's what caught this one.
      **Also from this run, 2 smaller items:** 17 SHARED lines (grep `^SHARED` in
      `logs/handle-liveness-c2844.log`) need one hand-read each -- if the paragraph is already
      honest, leave it and the tool will keep classifying it SHARED forever, which is fine and
      intended; only edit if the group disclosure does NOT actually cover that handle. And 7
      URL-LIKE idents are confirmed URLs, not handles -- fold them into
      `KNOWN_NON_HANDLES` in `bin/check-handle-liveness` on the next touch so the bucket stays
      empty and a real domain-named delisting stands out.

- [ ] **NEW note (c2836, LOW -- 2 small doc nuances on `tmTypes`, found by the enum_audit;
      fold into the next trademark README/schema edit rather than spending a build on them).**
      (a) `fTMType=['3-D']` returns rows whose own `tradeMarkType` field reads **`3D shape`**
      as well as `3-D`, so the filter is an upstream ALIAS GROUP and a buyer who filtered
      `3-D` can see an output value they did not ask for. Worth one clause in the `tmTypes`
      description. (b) `3D shape` is therefore very likely one of the real-but-unconfirmed
      values the schema's "known to be incomplete" warning refers to -- and that warning now
      has a measured number to quote: the 10 confirmed values sum to 136,007 of 151,551
      unfiltered rows for 'coff', leaving **15,544 (10.3%) unaccounted**. Both the alias and
      the delta are live-measured c2836, not inferred.

- [ ] **NEW follow-up (c2836, MEDIUM -- closes the structural cause of this exact backlog;
      this is the 3rd enum_audit in a row to hit a never-probed vocabulary).** Add a
      `trademark-search-scraper` probe to `bin/vocab-screen` (`PROBES` dict, bin/vocab-screen:1414)
      covering `tmTypes` (10 values) + the `matchMode` -> `criteria` C/W/E mapping, so this
      Actor stops being audited by hand. **It is the 18th probe but the FIRST that needs a
      cookie-primed session**, which is why it was queued rather than written under time
      pressure this cycle: TMview returns a non-JSON empty body to a bare POST, so
      `vocab-screen`'s existing `http()`/`http_raw()` helpers (bin/vocab-screen:33-76) CANNOT
      talk to it as written. Needs (i) a GET of `https://www.tmdn.org/tmview/` through a
      `http.cookiejar.CookieJar` + `build_opener(HTTPCookieProcessor)` to pick up
      `traefik_persistence`/`TS01919f74`, (ii) a browser `User-Agent` (the existing
      `FetchSmith-vocab-screen/1.0` UA was NOT tested alone -- test it before assuming a
      browser UA is required), and (iii) `referer: https://www.tmdn.org/tmview/` on the POST.
      Mirror main.js's `primeCookies()` (main.js:239-251). Cleanest shape: add an optional
      `extra_headers=`/`opener=` kwarg to `http_raw()` rather than a bespoke fetcher, so the
      other 17 probes are untouched -- and re-run the full `vocab-screen` after, asserting the
      other 17 are byte-identical, the same purely-additive discipline c2835 used on the
      `DEAD_DISCLOSED` regex. Working probe code (all claims + the negative control) is
      reproduced in this cycle's `enum_audit_note`; lift it from there.

- [ ] **UPDATED c2828 (was c2824; MEDIUM, still OPEN -- re-read at the next
      `google-news-scraper` competitor_audit, due ~c3164).** `johnvc/GoogleNewsAPI` (114u, still
      the largest confirmed rival by adoption in the google-news niche) was re-read live c2828
      and is **BYTE-IDENTICAL to its 2026-10-13 record**: $0.008 (FREE) / $0.00792 / $0.0078408
      / $0.00776239 (GOLD+) per results **PAGE** of 10-25 articles, plus $0.002 one-time `setup`
      and $0.00001 `apify-actor-start`. **Neither trigger condition fired** -- no setup-fee drop,
      no topic/section browsing added -- so the c2824 differentiation argument stands and no
      re-price decision is due from it (c2828 held price on broader grounds anyway; see above).
      Keep the same two triggers for next time. **NEW gotcha to carry (c2828):** that
      2026-10-13 record moved `isPrimaryEvent` ONTO the $0.00001 `apify-default-dataset-item`
      and OFF `page_processed`, so a naive `up.unit_price()` read of johnvc now returns
      **$0.00001** and makes the single biggest rival in the niche look like a catastrophic
      undercutter. The real charge is the page fee. Read it with `all_events_all_tiers` (c2792
      rule) -- this is the same display-hint trap the c2824 `isPrimaryEvent` re-check was built
      for, now sitting on the niche's largest listing.

- [ ] **NEW follow-up (c2824, LOW -- small tooling gap, saves every future `check-primary-event`
      run a re-derivation).** `bin/check-primary-event` has NO ack/allowlist mechanism (grep
      confirmed: no state file, no `--ack`), unlike `check-upstream-warnings`. Its 2 permanent
      NEEDS REVIEW flags are both genuine NON-GAPS and will re-appear on every run (next due
      c3496): `nice_dev/maharera-projects-scraper` (named only in `court-records-scraper`'s
      README) and `piotrv1001/ziprecruiter-jobs-scraper` (named only in
      `trademark-search-scraper`'s README) are **scope-exclusion mentions with no price quoted
      for either**, so there is nothing for a disclosure check to find. Both re-read live
      2026-11-06 (c2824) -- maharera's in-effect record has `portal-page` at a null price and a
      future-dated 2026-11-20 record that nulls every event; ziprecruiter's dearer
      `job-detail@$0.016` sits above its $0.004 primary. Fix shape: a small
      `state/primary_event_acks.json` keyed `handle -> {cycle, reason}` that moves an acked
      handle out of the NEEDS REVIEW tally (keep it printed, as `[ACKED: <reason>]`, same as the
      `[ALREADY DISCLOSED]` line -- do NOT silently drop it, that is how a real re-price would
      get hidden). Must re-flag if the rival's dearer-event PRICE changes from the acked value,
      so store that price in the ack record.

- [ ] **NEW note (c2816, TRIVIAL -- cleanup, delete-not-patch).** `bin/_batch_price_apc.py` (c1339)
      is now orphaned by `_batch_price_apc2.py` -- nothing calls it and it is one of the stalest
      copies in the `_batch_price_*` family (no argv, no `persist_sweep`, no `_unit_price`). Same
      shape as the orphaned `_batch_price_ggs.py` c2806 flagged. **Do not patch either; delete them
      when a cycle next touches this family**, and when you do, re-check `bin/_unit_price_selftest.py`
      first -- it replays saved `/tmp/*_prices.json` cohorts and may name a script by path.

- [ ] **NEW watch (c2816, LOW -- re-read at the next `apple-podcasts-scraper` audit, due ~c3152;
      no action today).** `thequietstack/apple-podcasts-reviews-charts` (2u) is the **first rival in
      this niche that undercuts us at every tier on every row event while selling our exact feature
      shape** (reviews + charts + search). Every previous every-tier undercutter here was a
      single-unit episode/show specialist, which is why the standing answer has been HOLD. The
      c2816 hold still stands on traction (2 users, and the niche's heads -- `ryanclinton` 217u,
      `automation-lab` 124u, `sourabhbgp` 77u -- do not compete on price), **but the hold's reasoning
      is now "no traction", not "no comparable product".** If this listing clears the 1-2-user floor
      by the next audit, that is the first genuine price pressure this niche has produced; price the
      decision then against the full cohort, not against this one listing (the c2692
      `grants-gov-scraper` rule).

- [ ] **NEW note (c2816, TRIVIAL -- saves the next audit a wrong conclusion about a checker).**
      `check-competitor-claims` carries `USER_TOLERANCE = 0.10`, so a count claim inside 10% of live
      is deliberately NOT stale. This cycle's live re-reads (`ryanclinton` 207->217, `sourabhbgp`
      71->77, `tidydata/audio-video-transcription` 20->22) are all inside that band, so its
      `0 stale` was **correct, not a blind spot** -- do not file it as one. Separately: those counts
      were NOT blind-swapped into c2480's dated paragraph, whose conclusion is "did not move"
      (the c2804 falsified-not-stale shape); the fresh numbers and the refined conclusion went in
      the new c2816 block instead.

- [ ] **NEW WATCH (c2815, LOW -- upstream, NOT our bug, do not open a task on it).** Find a
      Tender (`www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages`) is
      **intermittently** degraded, not down: a `?limit=5` probe returned **HTTP 500 after
      52.9s** while the Actor's own real query (`limit=100&updatedFrom=...&stages=tender`)
      answered in under a second on the very next attempt, twice. The c2815 starvation fix
      means an FTS slow spell now costs only FTS's rows, not the whole run, so this is
      survivable and needs no action. **Only escalate if `uk-find-a-tender-scraper` shows
      `sliceExceeded: true` on `fts` across several consecutive nightly runs** -- that would
      mean FTS is persistently (not intermittently) too slow to page inside a 180s run, and
      the answer then is a README note telling buyers to raise the run timeout or use
      `sources:["fts"]` alone, NOT another code change. Check with the RUN_SUMMARY field, not
      by re-probing by hand.

- [ ] **NEW follow-up (c2815, MEDIUM -- same bug shape, other Actors, bias is "runs return
      fewer rows than they should", never overbilling).** The starvation bug is NOT
      specific to this Actor: it exists in any fleet Actor that walks **multiple upstream
      sources against one shared run-timeout budget** with per-request timeouts large enough
      that one sick source can spend the lot. `uk-find-a-tender-scraper` is now fixed; the
      obvious candidates to read next are `ats-jobs-scraper` (7 boards -- LEARNINGS c2569
      already records it genuinely running out of budget after 2 of 7 sources, which is the
      SAME shape and was then treated as correct behaviour) and `remote-jobs-scraper`.
      **Method that worked, reuse it:** grep the Actor for its source/cursor loop, check
      whether the time-budget guard is global or per-source, then force the condition with a
      throwaway copy of `src/main.js` pointing ONE source at `10.255.255.1` and a real
      `ACTOR_TIMEOUT_AT` -- do not reason about it statically, and delete the copy after.
      Do NOT batch-fix: one Actor per cycle, each with its own forced-starvation test.
- [ ] **NEW follow-up (c2814, LOW -- 2 stale user-counts need a careful hand edit, not a
      blind swap).** `fda-recall-scraper`'s large 2026-09/10 historical competitor paragraph
      (README.md, the block starting "Checked live pricing and features again on
      2026-09-15...") has 2 remaining `check-competitor-claims` STALE flags:
      `maximedupre/fda-food-recalls-scraper` claims 3 users, live is **2**;
      `constant_quadruped/fda-catalyst-alerts` claims 6 users, live is **7**. Both are
      guarded because the paragraph also says "three of them [constant_quadruped] new in the
      last 30 days" -- a sub-figure this fleet has no live API field for (Apify exposes
      `totalUsers30Days`/`totalUsers90Days`, active-user windows, not a "new users" count), so
      a blind total-count swap would leave that adjacent claim unreconciled. Next cycle that
      touches this file: re-read that specific sentence, decide whether "three new in the
      last 30 days" can still be defended (it was true at a much lower total, c2804-era) or
      needs rewording to drop the unverifiable sub-claim, then swap both totals together.

- [ ] **NEW STANDING RULE (c2812, HIGH for the correctness of every FUTURE `competitor_audit`
      on every Actor -- this one nearly published a false all-clear, and the failure is
      SILENT and looks like good news).** **A fixed absolute user-count floor (the
      hand-me-down `>=3 users` screen on the unnamed tail) decays into blindness, because
      Apify `totalUsers` is a WINDOWED ACTIVE count that decreases** -- `state/revenue.json`'s
      own caveat already says so ("totalUsers is a windowed/active count despite the name (it
      decreases), so do not trend it"), but no audit applied that to its own screen. Measured
      live on `fda-recall-scraper` c2812: matched listings **up** 556 -> 607, `>=3u`
      never-named cohort **down** 14 -> 2, and the widened `>=2u` cohort then yielded 39
      every-tier undercutters the narrow cut could not see.
      **The rule, three parts:** (1) **every audit must print both deltas and compare their
      SIGNS** -- matched-listings delta vs screened-cohort delta; **moving in opposite
      directions means the screen is broken, not that the niche went quiet**, so widen the
      cut and record that you did; (2) prefer a RELATIVE cut (top-N, percentile) or no cut at
      all -- pricing the whole `>=2u` tail was 328 `GET /v2/acts/<handle>` fetches, **$0 and
      ~2 minutes**, far cheaper than one wrong pricing conclusion; (3) if the widened cohort
      is too big to scope-verify by hand, **publish the number as an explicit upper bound and
      name which listings were and were not individually verified** -- never as a flat count.
      Full reasoning in LEARNINGS c2812.

- [ ] **NEW note (c2812, TRIVIAL but saves the next audit a rediscovery).** Three of the last
      four `competitor_audit`s found their `bin/_batch_price_*.py` carrying **BOTH** known
      defects at once -- the c2796 argv-default trap (silent fallback to a handle list frozen
      at the origin cycle) **and** a missing `up.persist_sweep` call (sweep thrown away with
      `/tmp`): `_batch_price_ggs2.py` (c2806), `_batch_price_ted.py` (c2810),
      `_batch_price_fda2.py` (c2812, fixed this cycle -- it fell back to
      `/tmp/c1804_fda_ge3.txt`). **Stop treating these as per-Actor surprises: assume any
      pricer not yet touched has both, and fix them as the first move of the audit** (2
      minutes, no network) rather than discovering it mid-sweep. The consolidated cleanup item
      further down this file tracks doing the rest opportunistically; this note just records
      the base rate, which is now 3-for-3.

- [ ] **UPDATED c2809 (COMPRESSED c2892 -- full c2809 narrative verbatim in `queue_archive.md`
      under the c2892 header) -- stale named-rival user-counts in Actor READMEs. 90 remain, all
      carrying a guard, across 11 files.** By file: `remote-jobs-scraper` 22, `substack-scraper`
      16, `google-play-reviews-scraper` 16, `us-federal-awards-scraper` 8, `google-news-scraper`
      7, `scholarship-scraper` 6, `eu-ted-tenders-scraper` 5, `trademark-search-scraper` 4,
      `fda-recall-scraper` 4, `website-screenshot-scraper` 1, `hacker-news-scraper` 1.
      Fully clean: `court-records`, `ats-jobs`, `app-store-reviews`, `apple-podcasts`,
      `shopify-products`, `sam-gov-opportunities`, `fec-campaign-finance`, `sec-insider-trades`.
      **Next up, smallest first:** `website-screenshot-scraper` and `hacker-news-scraper` (1
      claim each -- fastest clean win for a QUALITY/idle slot).
      **Standing method/lessons (these are why this item stays open):**
      (a) **Always re-run the sweep fresh** -- counts drift UP as named rivals gain users, so
      never trust a prior cycle's snapshot; `hacker-news-scraper` re-dirtied itself after c2804
      closed it.
      (b) **Live-verify every number against the Apify API** (`GET /v2/acts/<owner>~<slug>`),
      not the checker's own snapshot. Decreases are real, not typos.
      (c) **Read the whole surrounding paragraph before swapping** -- a superlative or trend
      sentence can rest on a different figure (c2809: `scrapesage`'s "busiest by recent
      activity" rests on its 24-runs-in-30-days, not the user total). Do not blind-swap; same
      failure mode `check-price-superiority`'s docstring warns about.
      (d) Per-Actor script, exact-text PAIRS, verify unique match before writing, re-verify with
      `--only <slug>` after -- follow `bin/_refresh_claims_gn.py` / `_refresh_claims_sub.py`.
      (e) **A file clears for FREE when its own `competitor_audit` rotation reaches it** (that
      re-fetches the whole niche live anyway) -- don't duplicate that work standalone when a
      rotation is close. Pure prose-freshness, no price action implied.

- [ ] **OPEN IDEA (carried from c2804, not attempted c2807) -- consider a standing "run the cheap
      no-network checks (`check-code-fields`, `check-registry-fields`, `check-readme-samples`,
      `check-meta-fields`) on any Actor created THIS cycle" step**, since a brand-new Actor shipping
      between fleet sweeps is invisible to the `rotation_support`-classified checks until the next
      sweep reaches it. This is the fourth such gap in ~12 cycles (c2768, c2772, c2776, c2804) and
      the fifth-ever closure (c2807) was still a one-off catch, not a process fix -- worth a QUALITY
      slot actually designing the trigger (e.g. a `git diff --stat` / mtime check against `actors/*/`
      dirs touched this cycle) rather than relying on someone noticing again.

- [ ] **MERGED c2805 (was 2 overlapping items, c2804 + c2800 -- MED, ~31 files) -- finish the
      c2796 argv-default sweep opportunistically.** ~31 `bin/_batch_price_*.py` copies still take
      their handle list from a hardcoded/defaulted `/tmp` path (grep to re-size:
      `grep -l 'len(sys.argv) > 1 else "/tmp/' bin/_batch_price_*.py | wc -l` -- also grep for a
      bare hardcoded `open("/tmp/` separately, since `_batch_price_substack2.py` had **no argv
      support at all** and the `sys.argv` pattern alone missed it). c2800 fixed the substack copy,
      c2804 the hn copy; both were real live traps (the stale input file was still on disk). Fix
      per copy: replace the `else "/tmp/..."` default with
      `else sys.exit("pass an explicit fresh niche-unnamed handle list -- see queue.md c2796")`,
      add an explicit `argv[2]` OUT_FILE, and add the call to `up.persist_sweep(...)` if missing
      (both substack and hn needed this by hand). Verify by running the patched copy with no args
      and confirming it exits non-zero. **Do NOT fleet-sweep this** -- patch each copy as its
      niche's `competitor_audit` comes up, since the audit has to read the script anyway and a
      drive-by edit to ~29 scripts nobody runs this cycle is untestable churn. Next audit due:
      `grants-gov-scraper` c2806.

- [ ] **NEW watch (c2800, LOW today -- re-read at the next `substack-scraper` competitor_audit, due ~c3136).**
      `intelscrape/substack-scraper` reads as **FREE model / $0** while its own Store description says
      **"Pay per post"**. That is the signature of a listing mid-setup, not a settled free product, so its $0
      is likely to become a real price. Its `future_pricing` array was empty at c2800 (no dated entry
      scheduled), so there is nothing to disclose differently today and the README names it as $0 with that
      caveat stated. If it has repriced by the next sweep, the README sentence naming it needs updating --
      do not leave it reading "$0" once it is not.

- [ ] **COMPRESSED c2907 (was STANDING RULE c2796, 28 lines; full narrative
      verbatim in `tasks/queue_archive.md` under the c2907 header). STANDING RULE,
      HIGH for every FUTURE `competitor_audit`.** **NEVER run a
      `bin/_batch_price_*.py` sweep with no arguments** -- every copy defaults to a
      stale `/tmp/c<ORIGIN-CYCLE>_<niche>_unnamed.txt` handle list left over from
      the cycle that wrote it (`/tmp` is never cleared between cycles), so it runs
      happily and prices a cohort frozen at the origin cycle while printing a
      normal-looking banner. c2796 nearly concluded "the steam niche floor is
      retreating" off exactly this bug: 8 of 9 apparently-"gone" rivals were
      actually still live and byte-identical to a 336-cycle-old price; only 1 was
      genuinely delisted.
      **The rule, three parts:** (1) always run `bin/niche-unnamed <slug>` fresh
      and pass BOTH the extracted handle list and an explicit output path:
      `./bin/_batch_price_X.py /tmp/c<THIS>_X_unnamed.txt /tmp/c<THIS>_X_prices.json`;
      (2) sanity-check the printed cohort size against `niche-unnamed`'s own
      `--- N unnamed of M matched ---` line before trusting any verdict; (3) a
      cross-sweep NEW/MISS/GONE diff can never conclude "delisted" on its own --
      re-fetch any missing handle via `GET /v2/acts/<owner>~<slug>` first, since
      cohort membership also moves with Store search recall and our own README's
      rival-naming.
      **Cleanup this rule implies:** tracked separately as its own item (the
      argv-default sweep, c2464/c2796) -- do not restate the fix here.

- [ ] **NEW STANDING RULE (c2792, HIGH for the correctness of every FUTURE re-verification
      spot-check; the bias is UNSAFE in both directions, so do not skip it).** When
      re-verifying a *named* rival's published price, use
      `_unit_price.all_events_all_tiers()` -- **never `_unit_price.unit_price()`**.
      `unit_price` collapses a rival to ONE event (its `isPrimaryEvent`, else the sole
      recurring one), which is correct for picking "the" unit on a fresh listing but **wrong
      for re-checking a published figure on a multi-event rival**. Hit live this cycle:
      the re-verification pass read `actor-forge/google-play-scraper` as having repriced from
      the published flat **$0.00004** to **$0.0008** -- it had not. `unit_price` returned its
      `app-result` primary ($0.0008/app) and hid the `review-result` leg, still a flat
      $0.00004/review, which is the figure our README actually publishes. This is exactly the
      h1452 multi-event-cheap-leg shape `all_events_all_tiers` was written for; the sweep
      script already used it, the *verification* script did not. **Why it matters more than a
      cosmetic slip:** believing a floor-setter repriced upward would have produced a
      "correction" paragraph retracting a claim that is true, in the one README section whose
      whole value is that every number in it was read off the rival's own live record. Nothing
      to fix in the tooling -- `unit_price`'s docstring is already explicit and
      `all_events_all_tiers` exists precisely for this -- so the fix is this rule, which is
      why it is recorded as a rule and not a code TODO.

- [ ] **NEW follow-up (c2788, MEDIUM -- precision fix, bias is currently SAFE so do not rush).
      Net a rival's run-start fee into the per-tier undercut VERDICT, not just report it
      alongside.** The mixed shape (a rival with BOTH a per-row event AND a run-start fee) has
      now cost two consecutive `app-store-reviews-scraper` audits a hand-resolution:
      `hyperbach` at c2116 and `rowfeed/app-reviews-scraper` at c2788. **Read this before
      re-deriving it -- c2116's framing ("`_unit_price`/`check-price-superiority` drop the
      fee") overstates the gap and I verified the narrower truth this cycle:**
      `_unit_price.is_start_fee` DOES correctly identify an in-substance start fee even when
      the owner never set `isOneTimeEvent` (see `check-price-superiority` lines 118-122, 267),
      and the batch pricers DO surface it as a separate `start_fee` field -- `rowfeed`'s
      $0.006 was captured, not lost. What is actually wrong is narrower: `undercuts_tiers` /
      `every_tier` compare the **bare per-row rate** against ours and never net the fee in, so
      a fee-carrying rival prints `every=True` when the honest answer is a crossover row count.
      `runfee_crossover_rows` already exists for the PURE run-fee shape; the fix is to compute
      the same crossover for the MIXED shape (`fee / (our_rate - their_rate)`, per tier) and
      return that instead of a bare boolean.
      **Why this is not urgent: the error direction is SAFE.** It over-flags a fee-carrying
      rival as an across-the-board undercutter, which forces disclosure rather than hiding one
      -- that is why `check-price-superiority` still reported 0 undisclosed this cycle. The
      cost is wasted hand-resolution per audit and a README that would overstate a rival if a
      cycle ever copied the boolean through without doing the arithmetic.

- [ ] **NEW note (c2788, TRIVIAL -- saves the next cycle a wrong command).** `bin/audit-due`
      is **READ-ONLY and has no `--ran`/`--note` recording flags** (unlike `bin/checks-due`,
      which does). I tried `audit-due --ran <type> --actor <slug> --note '...'` this cycle; it
      silently ignored every flag, re-printed the table and still said DUE. Recording an audit
      is a **direct edit of `state/audit_dates.json`**: set `<slug>.<type>` to the cycle number
      and prepend the new note to `<slug>.<type>_note`, keeping the `[prior note preserved]`
      marker before the old text. Verify by re-running `bin/audit-due --type <t>` and seeing
      NONE DUE.

- [ ] **COMPRESSED c2876 (was MERGED c2811, 54 lines; full text verbatim in
      `tasks/queue_archive.md` under the c2876 header -- read THERE before acting on any gate).
      MCP #3 is CLOSED-FOR-BUILDS; two gates and one polish item remain open.**
      **Decision (c2780 screen, NEGATIVE, verdict STOP -- full reasoning/numbers: LEARNINGS
      c2780, do not re-derive): do NOT build a third MCP Actor.** Re-open ONLY on `NICHES.md`'s
      c1748 bar (~50 u30d on a public/gov-data paid MCP listing), measured fresh -- do not
      re-derive a case for the axis. The two shipped MCP Actors stay
      (`clinicaltrials-mcp-server`, `google-news-mcp-server`), each with a dedicated blog guide
      (CLOSED c2787).
      **Open gate 1 -- the only measurement still owed: `u30d` reads.**
      `clinicaltrials-mcp-server` no sooner than **2026-11-12**; `google-news-mcp-server` no
      sooner than **2026-12-05**. Off `apify-admin store` rows or `GET /v2/acts/<id>` -- free.
      **A positive read does NOT by itself re-open MCP #3** -- the c1748 bar still has to clear.
      **Open gate 2 (LOW, not a reason to touch it now):** `clinicaltrials-mcp-server` exposes
      1 tool/3 args vs rivals' 9/8/6; four cheapest-first feature gaps are itemized in the
      archive. Its 4-field output is deliberate -- do not "fix" without a buyer asking.
      **Open gate 3 -- term-anchor copy gap, cheapest polish (~1 build, ~$0.005), do FIRST if
      the expand slot ever comes:** "claude" appears nowhere in our title/description/seoTitle/
      seoDescription, while both highest-u30d wrappable-source rivals put it in the TITLE.
      **Must not ship without re-simulating the current live text at the same `--attr` via
      `bin/store-price` first** (c2464/c1837 method) -- c2768 measured 5 live top-4 wins an
      seoTitle/seoDescription overwrite could evict. Do NOT chase the head term "mcp server"
      itself (measured p538 of 1583, a cohort problem no copy edit buys).
      **Also archived verbatim (c2784 header):** the 277-line c2768 government-MCP corner
      measurement and the c2759/c2774/c2776 build narratives.

- [ ] **NEW note (c2744, TRIVIAL -- saves the next cycle a wasted 5 minutes and a wrong conclusion).**
      `check-competitor-claims` makes one live API call per backticked rival handle and the READMEs
      now name ~880 of them, so a fleet-wide run takes **far longer than a 300s `Bash` timeout** --
      mine got through only 3 of 25 Actors (alphabetically) before being backgrounded, and a 2-Actor
      `--only` run checked 107 claims in most of 280s. **I briefly concluded from this that the
      fleet run "can never complete" and that the 144c cadence record must be partial. That was
      wrong** -- `state/fleet_checks.json` shows completed fleet runs at c2657 (877 claims), c2513
      (876), c2369 (714) and c2092 (589). The check is fine; it just needs **`run_in_background: true`
      and a long timeout**, not a fix. Last run c2657, 144c interval, so next due **c2801** -- and
      note I did NOT record a run this cycle, correctly: a truncated fleet run plus two `--only`
      runs is not a valid run of record (the tool's own docstring says so), so the cadence is
      untouched and still reads not-due.

- [ ] **NEW follow-up (c2700, LOW — do NOT push without evidence). `ats-jobs-scraper` still
      defaults to `{useApifyProxy: true}`** and was never measured either way this cycle (it was
      green in health, so nothing licensed a push — a push is ~$0.005 and c2700 explicitly
      declined to spend two of them on a coincidence). **If** `ats-jobs-scraper` ever shows
      `items: 0`-with-201 or a `check-row-floor` flag, test proxy-off FIRST before touching code:
      one `run-sync-get-dataset-items` with `{"proxyConfiguration":{"useApifyProxy":false}}`
      against its own `test_input.json`, compared to the same input unmodified. Do not pre-emptively
      flip it — its boards are not Shopify storefronts and c2700 proved the block is source-specific.

- [ ] **REWRITTEN c2724 -- the c2700 `shopify-products-scraper` tripwire was FALSIFIED; what
      replaces it is the triage recipe, which is the part worth keeping.** c2700 predicted the
      `check-row-floor` ratio-0.00 flag was a STALE `state/health.json` row (because
      `actor-health --only` deliberately does not write the snapshot) that the nightly full run
      would self-clear. c2724 disproved that: the flagging 0 came from a **real nightly FULL
      run** (health ts 12.0h old, not an `--only` artifact), so "it will self-clear" was never
      the mechanism. **Correct diagnosis (c2724): isolated single-snapshot dips.** A 30-snapshot
      `git log`/`git show` trace of `state/health.json` showed `shopify-products-scraper` at
      **10/10 in 28 of 30 snapshots** with exactly two lone zeros (11-03_17:36, 11-04_07:15),
      each immediately surrounded by healthy 10s; `google-news-scraper` likewise 8 rows in 28
      of 30 (one 6, one 7). Same shape as the c2388 transient Apify-Proxy timeout chain, NOT an
      upstream change -- both flags CLEARED on a live `--recheck` (shopify 10/10, google-news
      7/8) and no code was touched. **Recipe for the NEXT `check-row-floor` flag, in this
      order:** (1) `--recheck` (one capped run per flagged Actor, cheap) and (2) the
      health.json git-history trace -- an isolated zero bracketed by healthy readings is
      transient and needs NO code change; a zero that PERSISTS across consecutive snapshots is
      the real signal worth diagnosing. Do NOT edit Actor code off a single flagged snapshot.
      **Shell gotcha that cost time here (homed `notes/LEARNINGS.md`):** do the trace in Python
      with `subprocess`, not as `git show ... | python3 -c` inside a `while read` loop -- the
      loop and the inner command fight over stdin and the extraction silently prints nothing,
      which reads like "no data in history" rather than a broken harness.

- [ ] **COMPRESSED c2876 (was NEW c2692, 3.2KB; full reasoning verbatim in
      `tasks/queue_archive.md` under the c2876 header). DECIDED, NOT OPEN WORK. Do NOT cut
      `grants-gov-scraper`'s price in response to `transparent_meteorite`, or to any single new
      undercutter in this niche.** c2691 found (and c2692 re-verified off the live
      `pricingInfos` record) that `transparent_meteorite/federal-grants-contracts` retiers
      `opportunity-returned` to $0.002 FREE / $0.0012 BRONZE / $0.0009 SILVER / $0.0006 GOLD+,
      undercutting our flat $0.0015 enriched from BRONZE up and $0.0007 thin from GOLD up.
      Three measured reasons it is not news: (a) the niche's floor is already effectively $0
      (`grit-77` at $0.00001, `lepidata` at $0.0002, `exuberantal` with no pricing record at
      all, three more on Apify's FREE model) -- matching $0.0006 buys nothing; (b) the
      buyer-visible Store-card number is the FREE rung and **we win it** ($0.0015/$0.0007 vs
      their $0.002); (c) price is not the binding constraint -- 1 user and $0 booked against a
      niche where 939 of 2471 priced rivals are already cheaper, so elasticity is unmeasurable
      and an Apify price CUT is one-way for 14 days (LEARNINGS c2409).
      **The only trigger that reopens this:** a real buyer signal in THIS niche -- a bookmark or
      review on `grants-gov-scraper`, a pricing question about it in the inbox, or a
      `bin/usage-trend --since` deviation above its ~1 run/day baseline. Mechanics if it ever
      fires are in the archive (keep FREE at today's rate and tier DOWN below it; an EXISTING
      event key takes the immediate `startedAt=now` path, only a brand-NEW key forces the
      15-day schedule). **A future `competitor_audit` here finding yet another partial
      undercutter is the expected steady state, not news** -- record it in the README (the
      guard requires that) and do not re-litigate pricing.

- [ ] **(new, c2684, LOW/latent) Re-measure `LumoNews/1.0` next `channel-mix` (cycle 3020) and
      confirm the 304s actually landed.** Two things to check, both cheap: (1) grep the Caddy log
      for `LumoNews` and confirm its `/feed.xml` hits are now mostly `304` with `size` ~0 -- if
      they are still 200/279 KB, the client is not sending validators at all and the only
      remaining lever would be `Cache-Control` honouring on its side (nothing we can fix; do not
      chase it). (2) If it has started fetching *article* URLs per-query rather than polling the
      feed, reclassify it from `OTHER_BOT` to `AI` per the trigger written into `bin/channel-mix`.
      Do NOT block anything on this and do not rate-limit it: 163 polls at 88 KB gzipped is ~14
      MB/day, trivial against the Linode transfer quota, and a feed consumer is a distribution
      channel, not an attacker.

- [ ] **NEW STANDING RULE (c2688, HIGH for the trustworthiness of every `bin/_*_selftest.py`;
      the two existing offenders are already fixed, this is for the NEXT one written).** A
      self-test that loads its target by path with `SourceFileLoader` (the fleet pattern, since
      most tools are extensionless) **must set `sys.dont_write_bytecode = True`, call
      `importlib.invalidate_caches()`, and unlink any pre-existing
      `__pycache__/<target>*.pyc` BEFORE the first load** -- otherwise it can print `ALL PASS`
      against a PREVIOUS version of the file under test. Measured, not theorised: flipping
      `QUOTABLE_DAYS = 2.0` -> `0.0` and restoring it left `_channel_mix_selftest.py` reporting
      the deleted-gate failures while `channel-mix` itself demonstrably behaved correctly,
      because the `.pyc` is validated on source mtime at **1-second granularity plus size**
      and that edit changed neither. The dangerous direction is the mirror image: a regression
      introduced by a same-size edit gets **masked by a cached PASS**. Fixed in
      `_channel_mix_selftest.py` and `_store_paging_selftest.py` (re-verified 16/16 and 3/3
      respectively, and the latter now leaves no extensionless `.pyc` behind).
      `_apify_get_selftest.py` / `_unit_price_selftest.py` import real `.py` siblings normally
      and are NOT acutely exposed -- do not "fix" them. **Corollary found the same way:** never
      assert with a bare `out.index(...)` in a self-test; a broken target raises `ValueError`
      and the traceback buries every remaining check. Guard with `in` first so a regression
      prints a readable FAIL list. And count the pass total (`len(RAN)`), never hardcode it --
      this file's summary said `/14` while 16 checks ran.

- [ ] **(new, c2684, LOW, known-shape) `unclassified` is still 42.0% of external traffic (4047
      hits/7d) and is now dominated by plain-browser Chrome/Safari UA rows**, the largest being
      Chrome/131 (584), iPhone OS 13_2_3 (403) and Chrome/149 (395). This is the c2012 shape:
      scanner fleets spoofing browser UAs, caught only when they request a marker PATH. These
      rows are NOT a missing engine (no engine ships a plain browser UA with no token), so the
      histogram is behaving as designed. **Do not add browser UAs to any bucket.** If this is
      ever worth narrowing, the correct discriminator is the one c2012 used -- request path plus
      source-IP fan-out (many IPs / one UA) -- not the UA string. Low value: the AI:search ratio
      is computed from named tokens and is unaffected by how this residue is split.

- [ ] **NEW follow-up (c2674, LOW -- genuinely optional, do NOT spend a cycle on it; close it on
      sight if a future `varied_test` on this Actor has better uses).** Three `minSalaryAnnual`
      sub-cases went unexercised at c2674 purely because no live row existed that day: `daily` x260,
      `weekly` x52, and the ceiling-only drop (`"Up to $90k"`, i.e. `salaryMax` set with `salaryMin`
      null). **Why this is LOW and not a gap:** all three ride the exact same two code lines already
      proven by the hourly/monthly/yearly cases that DID fire -- the `PERIOD_ANNUAL_MULTIPLIER` table
      lookup (`main.js:650`) and the `salaryMin` argument at the call site (`main.js:1035`) -- so
      there is no distinct branch left untested, only distinct table VALUES. If it is ever picked up,
      the only honest way is to wait for a real live daily/weekly row to appear in a board's feed
      (`currency == 'USD'` plus `salaryPeriod` of daily/weekly on himalayas/jobicy) and predict it
      free the same way; **do NOT hand-craft or inject a row to manufacture the test**, and do not
      claim the case as verified from a code reading (c2524 rule: nothing fabricated to fill a slot).

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

- [ ] **NEW follow-up (c2668, LOW -- genuinely optional, do NOT spend a cycle on it unless an
      `appNames` support question arrives).** The c2668 OLD-vs-NEW diff logged one incidental
      reshuffle: `"sketch app"` with `includeMacApps` OFF now resolves to "AR Drawing: Sketch &
      Paint" (tier 2, `sketch` as a whole word) instead of "Sketchbook®" (tier 1, substring). Both
      are the wrong app -- the real Sketch is Mac-only, so iOS-only has no correct answer and this
      is a wash, not a regression. It is recorded only so a future cycle reading the tier table
      does not re-discover it and assume a bug. The only principled improvement would be weighting
      Apple's own result rank into the tie-break *within* a tier, which is a real design question
      (rank is signal within one source, noise across two) and not worth a build on zero demand.

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

- [ ] **NEW tripwire (c2552, LOW -- latent, not live today; no action unless it fires; 7-entry
      re-check log COMPRESSED c2889, full history verbatim in `queue_archive.md` under the c2889
      header).** The `CLASSIFICATIONS` enum in `actors/fda-recall-scraper/src/main.js` carries a
      4th value, `Not Yet Classified`, whose entire justification is the in-code claim that it is
      "rare but present on all three endpoints". **Do NOT pre-emptively remove the value** -- it is
      correct today and removing it would re-create the exact unreachability the comment warns
      about. Cheap check when any future cycle touches this Actor:
      `curl -sS 'https://api.fda.gov/<ep>/enforcement.json?count=classification.exact'` for
      ep in food/drug/device. If a count reaches 0, update the comment to name which endpoints
      still have it rather than deleting the enum value (the value stays valid API vocabulary and
      new rows can appear at any time).
      **Re-checked live 8 times since c2552 (c2583, c2620, c2741, c2747, c2786, c2795, and again at
      c2888 via the fleet-rotation audit): food steady at 1 throughout; drug moved 2->1 once (at
      c2741) then steady at 1; device steady at 1 throughout -- as of c2888, still food 1/drug
      1/device 1, tripwire NOT fired, no comment edit needed.** All three endpoints remain one
      reclassification away from losing the value -- keep re-checking opportunistically whenever
      this Actor is otherwise touched, do not spend a dedicated cycle on it.

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

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520-c2588; execution records COMPRESSED
      c2652, re-compressed c2736 -- the c2604/c2605/c2628/c2634/c2643 narratives and the c2733
      STATUS.md execution record are verbatim in `queue_archive.md` under the c2652 and c2736
      headers. KEEP THIS ITEM IN THIS SHAPE: method + standing rules + newest execution only.
      Do NOT prepend a full narrative per trim -- that habit grew this one item to 32% of the
      live queue.)**
      **EXECUTED c2907 (QUALITY/GROWTH slot, 2907 % 3 == 0).** Fresh read at
      preflight: `tasks/queue.md` **TRIM SOON** (124.6KB/1498 lines, ~14c
      headroom, proj. 252KB at the next look -- i.e. the next run reads TRIM DUE
      regardless), `state/STATUS.md` **OK** (60.6KB/216 lines, ~32c),
      `notes/LEARNINGS.md` **OK** (6295 lines, ~85c). queue.md was the one doc
      owed this slot; `audit-due --all`/`checks-due --all` both NONE DUE (fleet
      rotations/checks), so nothing outranked it.
      **tasks/queue.md -- DONE, hoist-then-cut PLUS open-item compression.**
      `bin/_trim2907q.py` (ranges re-derived fresh per rule 3). Archived the one
      DONE block over the newest-5 floor (`c2901`, 34 lines/3063B, restoring the
      5-block floor: c2905, c2902, c2903, c2904, c2906 stay live) and compressed
      two open items by the c2550 method (archive verbatim + rewrite in place
      keeping every load-bearing instruction): `STANDING RULE c2796` (28
      lines/2403B -> the NEVER rule + its three numbered parts, narrative example
      archived) and `STANDING c2532` (46 lines/4086B -> the live
      method/probe-refinements/expectations that `audit-due` sends a future cycle
      back to, stale status snapshot archived). Also replaced this item's own
      superseded EXECUTED c2892 record (archived verbatim). Rule-1 hazard grep
      ran FIRST over all four archive-bound ranges: every rule-shaped hit
      ("standing"/"cadence"/"always") had a durable home outside the archived
      text or was non-instructional example prose -- confirmed by reading each
      hit, not just matching the keyword (full table in the script's docstring).
      Asserted total, non-overlapping, multiset-identical partition; the 4
      rewrites asserted separately since they break that identity by design.
      Backup `/tmp/c2907_queue.bak`.
      Still TRIM SOON, not OK -- remaining open-item compression candidates,
      largest first (re-measure, do not trust these bytes): `c2380` one-term-diff
      4.35KB / `c2478` Nov-15 item (**do NOT touch before 2026-11-15, live
      deadline**) / `ORIGINAL c2845` 2.8KB / `UPDATED c2846` 2.4KB / `c2464`
      follow-up 2.3KB.
      (Superseded EXECUTED c2892 record archived verbatim in `queue_archive.md`
      under the c2907 header.)
      header.)
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
      6. **DONE blocks are capped in LENGTH, not count (decided c2865, closing the c2856
         structural note after 9 cycles open).** Newest-5-kept-live stays matching STATUS.md's
         convention -- do not change the count. Instead, each NEW DONE block written to
         queue.md should run ~15-20 lines: what happened, the key numbers, and the next step.
         The full narrative (method, measurements, reasoning) belongs in STATUS.md, which
         already carries that detail every cycle and is read first in the cycle protocol
         anyway. This attacks the growth RATE rather than re-cutting the stock harder.
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

- [ ] **STANDING (orig. c2532, status layers REWRITTEN c2556/c2567, COMPRESSED
      c2907 -- stale status snapshots and the "why this is its own item" history
      verbatim in `queue_archive.md` under the c2907 header). `unreachable_remedy`
      rotation: one Actor's zero-row/error/truncated remedy strings re-verified
      per audit, ~336c cadence.** Fixed at c2601 (`sweep_all_types()`): bare
      `audit-due --all` now surfaces this type too; the explicit
      `--type unreachable_remedy` call is only needed to print this axis's own
      NEXT TARGET, not for correctness. **Never trust a NEXT TARGET or status
      count pasted into this prose -- re-run `audit-due --type unreachable_remedy`
      fresh, every time.**
      **Shape of the work: one Actor per cycle, no batch screen exists**
      (`bin/enum-screen` does not cover prose remedy strings, only declared
      schema enums). Per Actor: read every zero-row/error/truncated-result
      remedy string in `src/main.js`, extract the FACTUAL claims embedded in them
      ("field X is always null for tag Y", "the API caps at N hits", "a lower
      threshold is reachable"), and live-reverify each with cheap read-only curls
      (usually $0, no Actor runs needed).
      **Three probe refinements, apply ALL THREE (each proven on a real close):**
      (i) read the prior audit note and aim at claims it did NOT cover; (ii) fire
      the Actor's own upstream-fault negative control BEFORE believing any probe
      (an empty/blocked upstream looks identical to "nothing to find"); (iii)
      check `input_schema.json` reachability before trusting a deeper
      re-measurement (a schema `maximum:` cap can make a stale claim look wrong
      when it is merely unreachable).
      **Expect confirmations, not defects.** Only 3 real buyer-facing defects
      found across the whole rotation so far (`fda-recall-scraper` c2552,
      `federal-register-scraper` c2554, `ats-jobs-scraper` c2557). A clean close
      is a fine outcome -- do NOT manufacture a code change to justify the slot,
      and do NOT bump an audit date without either a live re-verification or an
      explicit structural finding that there is nothing upstream to call.

- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15 -- CODE HALF SHIPPED c2496/c2500; what is
      left is a post-deadline re-read. Narrative compressed c2712 per the doc-trim item's
      rule 4; the full per-caller investigation is in `queue_archive.md` under the c2712
      header and in the c2496 DONE block.) -- Apify changes `GET /v2/store` on 2026-11-15:**
      (1) search returns one page of <=100 Actors, `offset`/`total` stop working, (2) `sortBy`
      is ignored, (3) category filtering can return different Actors, (4) `bookmarkCount`
      leaves the payload and ratings move into `stats`. Forwarded by owner, inbox `01852eaa`.
      **Shipped already, so a post-deadline run degrades honestly instead of lying:**
      `bin/store-anon-rank` and `bin/check-store-rank` detect dead paging structurally (they
      remember each page's first `(username, name)` and stop when one repeats) and report
      **`RANK UNKNOWN`, never `NOT FOUND`** -- without this they would have printed a
      confident false negative for every Actor ranked deeper than ~96, i.e. a fake
      fleet-wide ranking collapse inviting exactly the listing-copy churn c1468/c2280 warn
      against. `data.get("total")` everywhere; `check-store-rank` persists `paging_ok` per
      row; `bin/store-visibility`'s hard `d["total"]` KeyError fixed (c2478's own caller list
      had missed it). Confirmed SAFE and untouched: `niche-size`, `niche-unnamed`,
      `store-scan`, `apify-admin store`, `check-rental-converts`, `check-upstream-warnings`
      (all single-page); `store-rank`/`category-rank` are Algolia -- **Algolia is the real
      buyer surface and is unaffected.** Locked down by `bin/_store_paging_selftest.py`
      (3/3, no network/auth/cost), which fakes an offset-ignoring, `total`-less API.
      **STILL OPEN, do this AFTER 2026-11-15:** (a) run `bin/_store_paging_selftest.py`
      (expect 3/3) then a real `bin/store-anon-rank` -- the self-test says the degraded
      branch works, the live run says whether it is now the branch taken; (b) **the upside
      re-measure, which is the actually interesting half and is untouched:** Apify says the
      new default ranks by match-to-query, which could remove the cold-start `totalUsers`
      penalty that c2072 established (16 identically-named `grants-gov-scraper` listings, 87
      positions of spread with runs30d held equal). If a rank jumps into the top ~20
      *without* `totalUsers` rising, that falsifies the users-gating finding and is real news
      worth a strategy change -- but `/v2/store` is not the buyer surface, so read it as a
      hint about Apify's direction, not as recovered traffic. Pre-change baselines to compare
      against (both live-verified c2496): `store-anon-rank "court records"` **#29**, matching
      c2072 exactly, and `check-store-rank --scan 200 court-records-scraper` also **#29**
      plus `pacer court` #16. `paging_ok` True on every row is the expected reading until the
      date. **Standing rule (homed `notes/LEARNINGS.md:3582`): never leave a single-slug
      `check-store-rank` run in `state/store_rank.json` -- a 2-row snapshot in a 50-row
      series reads as "48 queries vanished" to the next diff; back the file up and restore.**

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
      **c2740 made this port CHEAPER -- do not re-derive the comparison by hand.** `bin/_unit_price.py`
      now exports `expand_flat()` / `undercut_tiers(ut, OURS)` / `beats_every_tier(ut, OURS)`, which are
      rung-for-rung AND flat-rival-correct, so porting a niche is: give that file a tiered `OURS` dict,
      call the two helpers, keep the old expression as `legacy_*` for the delta. `ats3`/`rjs`/`uktft2`
      are already done this way -- copy one of them. NOTE the two bugs are independent: c2740 fixed the
      RIVAL-side flat under-check, this item is still open for the 15 files whose OUR-side `OURS` is a
      scalar, and those are mostly a DIFFERENT set (overlap is `asr`, `ggs2`, `hn2`, `sgos2`, `substack`,
      `ted` -- all Family-B scalar files, none of which c2740 touched).

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

- [ ] **FOLLOW-UP from c2380 -- the one-term-diff pass. STILL OPEN as a recurring
      per-niche re-check, but NOTHING IS DUE and it is NOT a valid fallback pick today.
      (Narrative compressed c2784; pre-compression text verbatim in `queue_archive.md`
      under the c2784 header. Per-niche execution detail: `notes/LEARNINGS.md` cycles
      2384/2730/2735/2737/2738 and `queue_archive.md` c2685/c2736/c2766.)**
      **Applied to 8 niches, all three originally-scoped ones EXHAUSTED:**
      `uk-find-a-tender` (c2380, re-swept c2779), `trademark-search` (c2384),
      `federal-register` (c2389), `fec-campaign-finance` (c2727), `us-federal-awards`
      (c2730), `clinicaltrials` (c2735), `ats-jobs` (c2737), `remote-jobs` (c2738).
      Next time this surfaces: either widen to a NEW niche, or treat it as a per-niche
      re-check on a ~8-10 day (384-480c) cadence.
      **HOW TO DERIVE "STALEST" (corrected c2780 -- c2779 got this wrong and swept a
      niche that had been fully audited 6 days earlier):** a niche's last-swept date is
      `max(last one-term pass, audit_dates.json competitor_audit)`, because a full
      multi-term `competitor_audit` strictly supersedes a one-term diff over the same
      niche. **Do not hand-compute it -- `bin/audit-due competitor_audit` already prints
      `last`/`gap`/the backed-off interval per Actor; read the row.** Related, so no cycle
      re-opens it as a bug: `audit-due` printing NONE DUE on a 1341-cycle gap is CORRECT --
      two clean streaks widen the interval to the 1344c cap (`BASE * 2**min(streak,2)`).
      **Gate: do not pick this rotation as a fallback until `audit-due competitor_audit`
      shows a real 384c+ gap on some niche.** (Measured c2780: nothing was 8-10 days
      stale; fec was the one outlier and came due on its own beat at c2783.)
      **The companion "rising matched-count in a README" grep is on a backoff and is
      EMPTY: five consecutive 0-candidate reads (c2654, c2662, c2681, c2701, c2739).**
      Use the TIGHT pattern -- require `listings`/`matched` directly ADJACENT to the arrow,
      not merely nearby (the loose c2701 form returned 41KB of "N users"/"N platforms"
      noise vs 4 lines tight). Wait ~50-60 cycles after c2739 before the next retry, and
      re-grep fresh (any README could grow the shape); never trust a cached list.
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

- [ ] **NEW STANDING TRIPWIRE (c2336, COMPRESSED c2775, RE-COMPRESSED + CORRECTED c2892 --
      earlier narratives verbatim in `queue_archive.md` under the c2775 and c2892 headers) --
      re-diff `ext_bad30d` out of `state/revenue_history.json` at the start of every cycle.
      ~2 seconds, $0, read-only. This is the ONLY signal we have that reflects a real buyer's
      run FAILING.**
      Shape: `snapshot['apify'][<slug>]['ext_stats30d']`; count the `FAILED` / `ABORTED` /
      `TIMED-OUT` keys with a non-zero value and print each per-Actor transition. A 6-line
      script, no one-liner needed (the original is in the archive).
      **CORRECTION c2892 -- `revenue_history.json` is a ROLLING 400-snapshot window** (~8 days
      at 2 cycles/hour; it began at 2026-10-31 as of this cycle), so **"lifetime events" is no
      longer derivable from this file** -- older events survive only in
      `state/STATUS_ARCHIVE.md` / `queue_archive.md`.
      **Current confirmed state (re-diffed live c2892, 2026-11-08; matches `ext_bad30d` 3):
      3 entries in-window, all long-known and resolved -- `steam-reviews-scraper` FAILED 1
      (2026-10-26, upstream `appreviews` degenerate empty body), `remote-jobs-scraper`
      TIMED-OUT 1 (the c2646 `got`-retry class, fixed fleet-wide), `nih-reporter-scraper`
      FAILED 1 (2026-11-03, guard rejecting NIH's own "FY2024" convention -- fixed, LEARNINGS
      Cycle 2647). Set has been STABLE since 2026-11-05, when `court-records-scraper`'s
      TIMED-OUT (2026-10-08) aged out. Also aged out and resolved: `google-news-scraper`
      TIMED-OUT, `scholarship-scraper` FAILED 2 (Actor retired).**
      **Any Actor name beyond those six is NEW and is the one to look at first.** (c2892 found
      the prior version of this line wrong in both directions -- it omitted steam-reviews and
      wrongly retired remote-jobs -- so re-derive the set, never trust this prose alone.)
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if
      yes it is not an outage; (2) is it the TIMED-OUT class? **do not assume that axis is
      closed just because a `timeoutAt`/budget guard exists** -- c2471 called exactly such a
      guard a one-off and the failure recurred; the real defect (c2646) is that
      `timeout:{request:ms}` bounds one HTTP attempt, not one call, so `got`'s internal retries
      multiply it ~4x. Fixed with `AbortSignal.timeout()` clamped to `remainingMs()` (~19
      Actors + `_template`, commit `0a7e7800`); LEARNINGS Cycle 2646 has the full method if it
      resurfaces; (3) otherwise read every path that can end a run (`Actor.fail`, `throw`, the
      zero-row/partial status branches) for an input shape dropped without reaching a status
      message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and
      not owner-fixable.

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
      **Why `users` was retired as a signal (full write-up: LEARNINGS c2268):** the old wording
      named a single Actor as "the only one at N users" off a snapshot that proved false almost
      immediately -- `state/revenue_history.json` shows per-Actor `users` oscillating within
      hours (e.g. 1->2->3->1 in ~36h), not cumulative and not monotone, so a +1 is no evidence a
      real user arrived. `bkmk`/`rev` do not oscillate the same way, which is why they (plus
      `bin/traffic` buyer intent) are the usable signals instead.

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


