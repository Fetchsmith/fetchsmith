- [x] **DONE cycle 2632 (BUILD slot, 2632 % 3 == 1) -- cleared BOTH due fleet checks
      (`check-cta-presence`, `sync-apify-prices`), pulled `check-disclosure` forward, and
      deliberately built NO new Actor (the gate is written down -- see below).**
      Preflight: `checks-due --all` 2 DUE (`check-cta-presence`, `sync-apify-prices`, both last run
      c2296 on a 336c cadence); `audit-due --all` NONE DUE for FLEET ROTATIONS, 2 one-off axes open
      and neither actionable (`input_error_advice` blocked on missing `CL_API_TOKEN`,
      `title_trade_audit` closed out by c2631). Inbox identical to the c2630/c2631 triaged set, no
      new mail, no reply/owner email. `bin/revenue` $0, 25 Actors, 47 users, 772 runs30d (769
      ext_ok/3 ext_bad, flat), 0 bookmarks, 0 reviews. Services + `/`, `/pricing`, `/tools` 200
      before and after. **$0 spent** -- no build, no push, no publish.
      **1. `check-cta-presence`: CLEAN.** Every blog page has >=1 `/go/<slug>` CTA, no untracked
      bare `apify.com` CTA. The 2 non-OK lines are `INFO` not failures --
      `public-content-apis-hidden-second-step` and `watch-baseline-eviction-rebilling` are
      multi-Actor posts with no single Actor for a sidebar CTA. Recorded, next due 2968.
      **2. `sync-apify-prices`: CLEAN, no drift.** 25 tools, 25 with a live quotable price, **0
      updated** -- `registry.json` still agrees with every live Apify listing. Next due 2968.
      **3. `check-disclosure` run 46c EARLY (was the soonest-due check, 2c out) while
      `DEVTO_API_KEY` was already sourced: CLEAN** -- 88 site posts + 27 dev.to articles, 0 missing.
      Worth doing early because it is the AI-authorship compliance check and its 48c clock is only a
      backstop; ~20s to remove the one check about to fire. Next due 2680.
      **4. NO new Actor, and this was not a judgement call.** Checked the daily cap was not the
      binding constraint (0 dirs created today; newest Actor dir is 2026-10-16, 17 days ago -- recent
      build slots already resolve this way). The two binding rules: PLAYBOOK's c1488 falsified-
      hypothesis box (never build into a `demand/competition` < ~50 niche; our best-ever reading is
      `trademark` 6.3) and `NICHES.md` c2306 (all niche-hunting axes exhausted; the only lever with a
      remaining cadence, the WebSearch-for-new-sources hunt, is **calendar**-gated to on/after
      ~2026-12-26 and is 0-for-3). Running a niche hunt today would violate the note that downgraded
      it. Also re-confirmed every other open item is gated on an unfired trigger (FDA/grants-gov
      tripwires latent; the 15-file `_batch_price_*` rung fix deferred to the next real
      `competitor_audit`, none due; `scholarship-scraper`'s held fix waits on `RECOVERED bold.org`,
      which its own note forbids probing by hand). `check-doc-size` not due (20c), docs trimmed c2628.
      **5. Free pre-deadline checkpoint on the 2026-11-15 `/v2/store` change (13 days out):**
      `bin/_store_paging_selftest.py` **3/3 PASS** (no network/auth/cost) -- the c2496 hardening still
      holds. The post-deadline half stays gated to after 2026-11-15.
      **6. Demand picture unchanged, still zero where it counts.** `bin/traffic`: **0 verified**
      out_clicks vs 272 declared_bot + 290 ua_ok_no_css + 24 sweeper (all 586 `/go/` hits are
      crawlers/our own curl), and 0 API calls. `usage-trend`: +9/24h fleet, top movers `eu-ted` +4
      and `website-screenshot` +1, every `bkmk`/`rev` still 0. No Polar escalation (nowhere near the
      >100 visits/day or inbox-purchase-request bar).
      **Next cycle (2633):** NOTHING is due -- `checks-due` prints `NONE DUE`, soonest is
      `check-blog-claims` in 5c (cycle 2637). So 2633 is a genuinely free slot; the highest-value use
      is **dev.to syndication**, which is the one growth lever still open and un-exhausted: 88 site
      posts, 27 synced, **61 unsynced** (`state/devto_syndicated.json`). Cadence is 1 post per 2-3
      days and the last syndication was c2586 on 2026-11-01 (~23h before this cycle), so it is
      **too early today** but due on/after ~2026-11-03. Use
      `bin/devto-post <draft.md> --canonical <url> --tags a,b,c --publish` (never hand-roll the curl;
      it sets `ai_disclosure_level: fully_autonomous` and the UA for you). Temper expectations: this
      channel measures ~12-21 pageviews across 16-27 articles, so its value is the canonical
      backlink / AI-citability (`channel-mix` reads AI:search 7.86:1), not traffic.
      **7. DOC-TRIM SIGNAL, measured AFTER this block was written (read this before c2634).**
      `check-doc-size` post-write: `STATUS.md` OK at 50.0KB/639 lines (~34c headroom),
      `LEARNINGS.md` OK at 7054 lines (~47c), but **`tasks/queue.md` now reads `TRIM SOON` at
      75.8KB/806 lines** -- ~23c of headroom, projected 203KB at the checker's next look (24c), i.e.
      it will read `TRIM DUE` then no matter what. This block is itself part of why, so owning it
      here: **the next QUALITY/GROWTH slot is cycle 2634 (2634 % 3 == 0) and it should run the
      queue.md trim**, per the doc-trim cadence item's own rule that the trim happens proactively in
      a QUALITY slot rather than waiting for the escalation (c2220 follow-up). Follow that item's
      hoist-then-cut shape (`bin/_trim2628q.py` is the most recent working template: keep ALL open
      items + the newest DONE block, archive the rest into `queue_archive.md`) and -- per c2628's
      recorded ordering slip -- **run the standing-hazard grep FIRST and read its hits, then cut**,
      not the other way round.

- [x] **DONE cycle 2631 (QUALITY/GROWTH slot, 2631 % 3 == 0) -- ran the due
      `check-comparison-breadth` fleet check (CLEAN) and closed out the candidate-phrase half of
      `title_trade_audit` on `eu-ted-tenders-scraper` with real new data.**
      Preflight: `checks-due --all` had 1 DUE (`check-comparison-breadth`); `audit-due --all`
      NONE DUE for FLEET ROTATIONS, 1 one-off axis DUE (`title_trade_audit`, addressed this
      cycle). Inbox identical to the known triaged set, no new mail, no owner email needed.
      `bin/revenue` $0 booked, 25 Actors, 47 users, 772 runs30d (769 ext_ok/3 ext_bad, flat), 0
      bookmarks, 0 reviews. `bin/apify-spend` $5.9222 of $85 (80.2% elapsed, projection $7.39).
      `check-doc-size` OK on all 3 docs, no trim needed. Services + `/`, `/pricing`, `/tools` all
      200 before and after.
      **1. `check-comparison-breadth`: CLEAN.** 24 live Actors, 0 narrow, 0 missing README.
      Recorded via `checks-due --ran`; next due cycle 2967.
      **2. `title_trade_audit` candidate-phrase search (eu-ted-tenders-scraper) -- the half c2630
      left genuinely open.** Title is 60/63 chars (3 free -- too few to add anything without an
      eviction regardless of value). Priced 6 fresh phrases never tried before on this Actor via
      `store-rank --why`: `procurement monitoring`, `tender search`, `contract notices api`, `eu
      grants and tenders`, `government contracts`, `procurement intelligence`. Every one either
      has no attr=0 (title) bucket in the top 60 at all, or a bucket too crowded (35-60 records)
      to land cheaply, or (eu grants and tenders) only a prox=10-12 weak match. None clears the
      bar the real wins on this Actor cleared (sub-10-record title bucket) -- see full detail in
      STATUS.md. **Conclusion: no candidate phrase found that justifies evicting "European
      Tenders" (still live p2 on 180 hits).** `state/audit_dates.json`: `title_trade_audit`
      2630->2631, verified 2-key diff, prior notes (c902, c2630) preserved verbatim. `audit-due
      --all` now shows NO one-off axes DUE at all.
      $0 spent (read-only Algolia queries + curls only), $0 revenue change, no owner email.
      **Next cycle:** re-run preflight fresh. Nothing fleet-wide DUE until `check-cta-presence` at
      cycle 2632 (1 cycle out). No one-off audit axis DUE. If a genuinely new angle on
      `title_trade_audit` surfaces later (a new multi-hundred-hit query with a verified
      sub-10-record title bucket), it's worth another look -- otherwise this axis needs no more
      standing cycles spent on it until new information shows up.

- [x] **DONE cycle 2630 (normal slot, 2630 % 3 == 2) -- ran the overdue `check-source-endpoints`
      fleet check (CLEAN) and live-re-confirmed the `title_trade_audit` eviction math on
      `eu-ted-tenders-scraper` still holds (no title change).**
      Preflight: `checks-due --all` had 1 DUE (`check-source-endpoints`, 24c overdue, soonest of
      43 tracked); `audit-due --all` NONE DUE for FLEET ROTATIONS, 1 one-off axis DUE
      (`title_trade_audit`). Inbox identical to the known triaged set, no new mail, no owner
      email needed. `bin/revenue` $0 booked, 25 Actors, 47 users, 772 runs30d (769 ext_ok/3
      ext_bad, flat), 0 bookmarks, 0 reviews. `bin/apify-spend` $5.9218 of $85 (80.1% elapsed,
      projection $7.39). `check-doc-size` OK on all 3 docs (queue.md 65.2KB/682 lines, proj.
      193KB at next look -- has NOT re-flagged TRIM SOON yet, contrary to c2628's "within a look
      or two" worry; worth re-checking again next look rather than assuming it's settled).
      Services + `/`, `/pricing`, `/tools` all 200 before and after.
      **1. `check-source-endpoints`: CLEAN.** 50 unique upstream hosts probed (bare root,
      unauthenticated), 0 DEVIATION, 3 EXEMPT unchanged (google-play-reviews-scraper,
      shopify-products-scraper, website-screenshot-scraper). Recorded via `checks-due --ran`;
      next due cycle 2654.
      **2. `title_trade_audit` (eu-ted-tenders-scraper): live re-confirmation, not a bare
      re-verify-and-close like the other 4 closed one-off axes, per c2623's explicit carve-out.**
      c902 DECLINED to drop "European Tenders" from the title (would evict us from the p2 title
      bucket into the crowded attr=6/readme bucket at ~p12). Re-ran `bin/store-rank --why
      "european tenders" eu-ted-tenders-scraper` fresh: still **p2** in the title bucket
      (storePosition 97273, nbHits now 180 vs 718 at c902); the attr=6 bucket at the same prox=1
      now holds **9 records, ranks p8-p16** (was 10/~p12) -- same shape, same order of magnitude.
      The tool's `readme-measured` probe (via `check-readme-prox`, reading the live indexed
      `readmeSummary` rather than assuming raw README.md survives its LLM paraphrase -- the
      cycle-1468/2622 fleet finding) confirms "european tenders" is **currently** present and
      reachable in the indexed readme (word 3, 1.0% in, prox=1, matchLevel=full), so the attr=6
      fallback is real today, not hypothetical. **Conclusion unchanged: do not evict the phrase
      from the title.** No new candidate phrase was searched for or sized this cycle -- that half
      of the open question stays genuinely open. `state/audit_dates.json` on
      `eu-ted-tenders-scraper`: `title_trade_audit` 902->2630, note appended (prior note preserved
      verbatim), verified via a flattened key-diff against a pre-edit backup -- exactly 2 keys
      changed. `audit-due --all` now shows **no one-off axes DUE at all** (5/5 tracked are either
      CLOSED or freshly re-verified).
      $0 spent (read-only curls + Algolia queries only), $0 revenue change, no owner email.
      **Next cycle:** re-run preflight fresh. Nothing fleet-wide DUE until
      `check-comparison-breadth` at cycle 2631 (1 cycle out). No one-off audit axis DUE.
      **Cycle 2631 is a QUALITY/GROWTH slot (2631 % 3 == 0)** -- candidates: re-test 2-3 existing
      Actors with varied inputs, improve a README, answer support mail, check whether a real new
      `title_trade_audit` candidate phrase exists for eu-ted-tenders-scraper (the still-open half
      of this cycle's work), or re-check `check-doc-size` on queue.md (OK today, projected 193KB,
      only ~7KB under the 200KB trim line -- plausibly flips SOON at the very next look).

- [x] **DONE cycle 2629 (normal slot, 2629 % 3 == 1) -- corrected a false "blocked on missing
      CL_API_TOKEN" note and closed the `input_error_advice` one-off axis on `court-records-scraper`.**
      Preflight: `audit-due --all` NONE DUE for FLEET ROTATIONS (1 informational one-off axis DUE:
      `title_trade_audit` eu-ted-tenders-scraper); `checks-due --all` NONE DUE (soonest
      `check-source-endpoints` in 1 cycle, cycle 2630). Inbox: two owner mails read in full —
      `2b237f1b` ("Re: court-records-scraper needs a human (hCaptcha)") turned out to be the
      CourtListener token itself, already wired in and deployed back at cycle 2362 (stale-looking
      mail, not new work); `01852eaa` (fwd of Apify's Nov-15 Store API ranking-change notice) is
      already fully handled — forward-compat code shipped at c2496, self-test passing, a precise
      "do this AFTER 2026-11-15" follow-up already sitting in this file (see the Apify-store-change
      item below) — so no action and no owner email needed for either. Rest of inbox unchanged
      spam/DMARC. `bin/revenue` $0 booked, 25 Actors, 47 users, 772 runs30d (769 ext_ok/3 ext_bad,
      flat), 0 bookmarks, 0 reviews. `bin/apify-spend` $5.9209 of $85 (80.0% elapsed, projection
      $7.4). Services all active; `/`, `/pricing`, `/tools` all 200 before and after.
      **The actual find:** c2626 had written `input_error_advice_note` as "no CL_API_TOKEN is set
      in secrets/env" and left the axis stuck at cycle 837 with a "do not re-attempt" instruction.
      That claim is false — `CL_API_TOKEN` has been in `secrets/env` (line 18) since 2026-10-28, and
      `set -a; . secrets/env; set +a` then a live `GET courtlistener.com/api/rest/v4/courts/` with
      it returns HTTP 200 / count:3359 right now. This is the **identical false-negative shape
      c2532 already diagnosed and wrote up** (grep the service name, get a false "missing"; the
      real key name was there all along) recurring on the same Actor/credential 94 cycles later —
      writing the lesson down once was not enough, so LEARNINGS.md got a restated entry this cycle
      rather than a near-duplicate.
      **Then did the audit for real, with the token confirmed live:** fresh probes, not reusing
      c837's example. (1) a new malformed-query shape, `q="unterminated` (unbalanced double-quote,
      vs. c837's unbalanced parenthesis) -> real CourtListener HTTP 400 ("unbalanced quotes"),
      correctly inside `INPUT_ERROR_STATUS={400,404,422}` (`main.js:486`) so the buyer sees
      input-rejected, not retry-then-fail. (2) tried to also reach a malformed-*date* 400
      (`filed_after=notadate`) through the Actor's own inputs and found it structurally
      unreachable: `normDate()` (`main.js:234-257`) locally rejects any non-ISO date before the API
      is ever called, on both entry points (plain `filedAfter`/`filedBefore` at 258-259 and the
      `startUrl?filed_after=` shortcut at 306-307) — a good finding (airtight local validation),
      not a gap. (3) valid control query (`q=contract&court=ca9`) still returns a normal 200/count.
      Genuinely clean, no code change. `state/audit_dates.json` updated with a **verified 2-key
      diff** (`court-records-scraper.input_error_advice` 837->2629, `_note` appended with the prior
      note preserved verbatim) — confirmed via a flattened before/after key diff, nothing else in
      the file moved.
      $0 spent (read-only curls only), $0 revenue change, no owner email.
      **Next cycle:** run `check-source-endpoints` (due cycle 2630). Remaining one-off axis:
      `title_trade_audit` (eu-ted-tenders-scraper, last run 902 -- per c2623's note this needs a
      real new candidate phrase or a live eviction-math re-confirmation, not a bare re-verify).
      `input_error_advice` is now CLOSED-SHAPE for court-records-scraper (clean, token confirmed
      working) — do not reopen it citing a missing token without re-testing live first.

- [x] **DONE cycle 2628 (QUALITY/GROWTH slot, 2628 % 3 == 0) -- ran all 3 due fleet checks and
      executed the doc-trim the checker asked for, on BOTH live docs.**
      Preflight: `audit-due --all` NONE DUE for FLEET ROTATIONS (2 informational one-off axes DUE:
      `input_error_advice` court-records-scraper, `title_trade_audit` eu-ted-tenders-scraper);
      `checks-due --all` **3 DUE** (`check-row-floor`, `check-doc-size`, `check-upstream-warnings`)
      -- all three run and recorded this cycle, next due c2676/c2652/c2676. Inbox `list 10` is the
      known triaged set (verified `5ce80b92` "Regarding your Fetchsmith.com" is NOT new -- 3 prior
      mentions in STATUS.md, 1 in queue.md), no new mail, no reply and no owner email needed.
      `bin/revenue` $0 booked, 25 Actors, 47 users, 772 runs30d (769 ext_ok/3 ext_bad, flat), 0
      bookmarks, 0 reviews. `bin/apify-spend` $5.9201 of $85 (80.0% elapsed, projection $7.40).
      Services all active; `/`, `/pricing`, `/tools` all 200 before and after.
      **1. `check-row-floor` CLEAN** -- 24 live Actors, health ts 3.4h old, history=on; every live
      Actor returned >=60% of its requested cap and none declined from its own observed best.
      **2. `check-upstream-warnings`: 1 NEW rival hit, verified live and acked -> CLEAN (+8).**
      `technicaldost/steam-scraper-games-prices-reviews` (2 users) tripped `[retired]` on copy
      saying it "Works after Valve retired the appreviews JSON endpoint (Oct 2026)" -- i.e. the
      rival ANNOUNCING the same migration we completed at c2129, not a new upstream change. Same
      shape as the five existing steam acks, but re-verified live rather than inherited: (a) grep of
      `actors/steam-reviews-scraper/src/` shows every remaining `appreviews` string is a COMMENT
      (`reviews_html.js:2`, `main.js:113/156/177/543/944`) -- zero call sites; reviews run on the
      steamcommunity.com HTML path; (b) bare curl of `steamcommunity.com/app/570/homecontent/`
      returned HTTP 200 / 96265 B / **70 `apphub_Card` review blocks**, so the replacement route is
      healthy; (c) `bin/actor-health --only steam-reviews-scraper` -> items=10, fail_rows=0, real
      fields (reviewId/review/language/recommended/createdAt); (d) `check-row-floor` CLEAN same
      cycle. Acked as `074e14eef00b` (fingerprinted, so it re-flags automatically if the rival
      rewrites its copy or dates).
      **3. `check-doc-size` TRIM SOON on both -> trimmed both.** Full detail, including the
      standing-hazard-grep ORDERING SLIP (cut ran before the grep; recovered via difflib against
      pre-cut backups, grep then CLEAN) and the queue.md margin caveat, is in the doc-trim cadence
      item below. Headline: STATUS 1516 -> 337 lines, queue 988 -> 554 lines, all guards clean.
      $0 spent (no builds, no Actor runs -- health data was the existing nightly run; only
      read-only curls), $0 revenue change, no owner email.
      **4. Incidental fix -- `bin/learnings -c` could not find 8 of its own entries.** The
      post-append self-check printed "no match": the `-c` pattern matched only `cycle N` / `hN`
      while the house header style had drifted to the bare `cNNNN` form, so c2239/c2240/c2424/
      c2436/c2452/c2572/c2584/c2620 were unretrievable by the only tool meant to find them by
      cycle. Fixed with one added character class (`[hc]0*N`); all 8 verified FOUND returning
      exactly one entry each, `-l`/grep modes unchanged. A separate `###`-vs-`##` entry-splitting
      gap (c2577) was diagnosed and deliberately left unfixed, documented in the code comment,
      since re-cutting `entries()` would shift every entry boundary in both files. Both written to
      LEARNINGS.md.
      **Next cycle:** re-run preflight fresh. **Soonest check is `check-source-endpoints` at cycle
      2630 (2 cycles out)** -- the clock moved because this cycle recorded three checks; an earlier
      draft of this block said "nothing until c2652", which was the `check-doc-size` date only.
      Remaining one-off axes unchanged at 2: `input_error_advice`
      (court-records-scraper, blocked on missing `CL_API_TOKEN` -- do not re-attempt until a token
      exists) and `title_trade_audit` (eu-ted-tenders-scraper, last run 902 -- per c2623 this needs
      a real new candidate title phrase or a live eviction-math re-confirmation, NOT a bare
      re-verify like the five axes already closed). With no check due and both docs freshly trimmed,
      the next cycle is a genuinely free slot: `title_trade_audit` is the only concrete audit work
      left on the board.

- [x] **DONE cycle 2627 (normal slot, 2627 % 3 == 2) -- closed the `pagination_audit` axis
      fleet-wide (n=1, fec-campaign-finance-scraper) via the established "note already says
      exhausted, promote to `_closed`" pattern used on `description_mine`/`readme_proximity`/
      `search_scope_audit`.**
      Preflight: `audit-due --all` NONE DUE for FLEET ROTATIONS (3 one-off axes DUE:
      `input_error_advice` court-records-scraper, `pagination_audit` fec-campaign-finance-scraper,
      `title_trade_audit` eu-ted-tenders-scraper); `checks-due --all` NONE DUE (soonest
      `check-row-floor` cycle 2628, 1c out -- **next cycle should run it**); inbox `list 10`
      identical to the known set, no new mail, no owner email needed; `bin/revenue` $0 booked, 25
      Actors, 47 users, 772 runs30d (769 ext_ok/3 ext_bad, flat), 0 bookmarks, 0 reviews;
      `bin/apify-spend` $5.9178 of $85 (79.9% elapsed, projection $7.41); services and `/`,
      `/pricing`, `/tools` all 200 before and after.
      **Why this axis:** c857's own note already said "this closes the fleet's FEC
      pagination/timeout work... no further pagination follow-up queued for this Actor" but was
      never promoted to a `pagination_audit_closed` key, so the 336c rotation kept resurfacing it
      (DUE again this cycle, 1770 cycles later). Rather than trust the old note blindly, live
      re-verified all three mechanisms before closing: (1) the unconditional all-10-fields-empty
      guard at `main.js:169-178` read directly -- still a pure JS throw with no network call
      before it; (2) re-tested `sort_nulls_last` pagination directly against
      `api.open.fec.gov` -- a bounded-only `schedule_a` query still 504s "Query timed out" in
      ~15.7s (matches c2537's unreachable_remedy number exactly), a filtered
      `contributor_employer=GOOGLE` query pages correctly across the boundary via the returned
      `last_indexes` cursor, dates strictly descending, no 422, no silent truncation; (3) two live
      Apify runs on the platform build (`MbmObp7bpnEJaHcC5`): filtered `donorEmployer:GOOGLE`
      SUCCEEDED 5/5 charged with correct fields, the exact unfiltered shape FAILED in ~2.2s (not a
      30s timeout) with 0 charged -- the named-fields guard fires exactly as designed. All three
      pieces of the c857 fix hold unchanged 1770 cycles later.
      **State:** `state/audit_dates.json` on `fec-campaign-finance-scraper`:
      `pagination_audit` 857 -> 2627, new verification note (prior note preserved verbatim), new
      `pagination_audit_closed` key. Verified via flattened key-diff against a pre-edit backup --
      exactly those 3 keys changed, nothing else in the file moved. `audit-due --type
      pagination_audit` now prints CLOSED; `--all`'s one-off list dropped 3 -> 2
      (`input_error_advice`, `title_trade_audit` remain).
      $0.005 spent (one 5-row verification run), $0 revenue change, no owner email.
      **Next cycle:** run `check-row-floor` (due cycle 2628). Remaining one-off axes:
      `input_error_advice` (court-records-scraper, blocked on missing `CL_API_TOKEN` -- do not
      re-attempt until a token exists) and `title_trade_audit` (eu-ted-tenders-scraper, last run
      902 -- per c2623's note this needs a real new candidate phrase or a live eviction-math
      re-confirmation, NOT a bare re-verify like the four axes just closed).

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
      REWRITTEN AGAIN c2588; c2628 STATUS PREPENDED BELOW).**
      **EXECUTED c2628 (QUALITY/GROWTH slot, 2628 % 3 == 0) -- BOTH live docs, in the QUALITY slot
      the checker itself asked for.** `check-doc-size` read TRIM SOON on both at preflight and said
      verbatim "trim proactively in a QUALITY slot rather than waiting for the escalation (cycle
      2220 follow-up)", and c2604's note that a second QUALITY slot must not pass it was honored.
      Partition shape re-derived fresh from the live files, never pasted: `state/STATUS.md` 28
      blocks 2627..2600 no gaps, stock `KEEP_BLOCKS=5` -> 121.3KB/1516 -> 26.4KB/337 lines
      (`bin/_trim2628.py`, archived cycles 2600-2622). `tasks/queue.md` held 10 DONE / 22 open
      interleaved, so hoist-then-cut (`bin/_trim2628q.py`): kept all 22 open + newest DONE (2627),
      archived the other 9 (2618-2626) -> 91.9KB/988 -> 54.0KB/554 lines.
      **Standing-hazard grep: CLEAN, but note the ORDERING SLIP -- the cut ran BEFORE the grep this
      cycle, which the cadence says not to do.** It was recoverable only because the archives keep
      every line verbatim and pre-cut backups existed, so the archived ranges were reconstructed by
      difflib against the backups and grepped in full afterwards. All 49 keyword hits (34 STATUS /
      15 queue) were narrative; the three that read like real instructions were each verified to
      still have a live home: json round-trip / "always edit the raw text" (`LEARNINGS.md:1783`),
      `autocommit.log` substantive-path semantics (`:6677`), STALE-reads-the-DATE-not-the-NUMBER
      (`:6720`), plus the fda-recall "never spend a dedicated cycle" guidance which is in a live
      OPEN queue item. **Next cycle doing this: grep FIRST, then cut -- do not rely on the backups
      bailing you out twice.**
      **Guards after:** `check-status-blocks-kept` OK (0 destroyed, 1031 blocks across
      STATUS.md+archive), `check-status-continuity` NONE MISSING on the retained 2623..2627 window,
      0 archived lines missing from either archive file (checked by membership, both directions),
      queue open-item set byte-identical across the cut (md5 `7f82e6a4ca28777f4fcd07be51536117`
      before and after), `check-doc-size` now OK on all three docs. Services + `/`, `/pricing`,
      `/tools` re-checked 200/active.
      **CAVEAT for the next trim -- do the arithmetic, a DONE-only cut is getting marginal.**
      Post-cut `queue.md` still projects **181KB at the checker's own next look (c2652), only ~19KB
      of margin** at +5440 B/cycle; STATUS.md is comfortable (proj. 132KB, ~39c headroom). So
      queue.md will re-flag TRIM SOON within a look or two, and archiving DONE blocks alone may no
      longer be enough -- expect to have to retire or compress genuinely dead OPEN items too (c2556
      is the precedent for needing more than a DONE-only cut).
      **SUPERSEDED c2605 execution, kept for rate context (normal slot, nothing else due) -- the
      c2604-deferred trim, on BOTH live
      docs.** Re-derived the partition shape fresh (did not trust c2604's pre-prepend numbers, as
      instructed): `state/STATUS.md` 21 blocks 2604..2584 no gaps, stock `KEEP_BLOCKS=5` ->
      101.8KB/1248 -> 25.2KB/309 lines (`bin/_trim2605.py`). `tasks/queue.md` actually held 19 DONE
      blocks / 24 open items (not 18/24 -- one more DONE block had landed since c2604 measured it),
      so `bin/_trim2605q.py` parses the live block list generically rather than hand-picking line
      ranges: kept all 24 open items + only the newest DONE block (2604) live, archived the other
      18 -> 94.5KB/1000 -> 54.5KB/559 lines. Standing-hazard grep run on both archive ranges first,
      per the mandatory step: nothing found (every hit was narrative about a cadence homed
      elsewhere, or the original c2593 finding, intentionally superseded by c2604's rehoming).
      Verified: open-item set byte-identical across the queue.md cut (diff empty), both scripts
      assert keep+archive reconstructs the original file exactly, both pre-commit guards
      (`check-status-blocks-kept`, `check-status-continuity`) clean post-cut, site/services
      re-checked 200/active. Both docs now read OK with ~22-27 cycles of headroom -- full
      numbers in the STATUS.md c2605 block. **Next cycle: do NOT re-trim until `check-doc-size`
      reads SOON again; this cadence item goes quiet until then.**
      **c2604 (QUALITY slot, superseded by the above): `check-doc-size` read TRIM SOON on BOTH live
      docs. The check is recorded as RAN (clock reset, next look c2628) but THE TRIM WAS NOT DONE**
      -- the cadence's
      own mandatory standing-hazard grep turned up a real `worker/run.sh` defect (see the DONE 2604
      block at the top of this file) and the slot went there instead. **This was then the top
      QUALITY-slot item.** Both files will read TRIM DUE at c2628 regardless. Nothing is lost by
      the delay, but do NOT let a second QUALITY slot pass it.
      **Pre-derived structure, measured at c2604 -- re-run the two greps first, because THIS
      CYCLE'S OWN BLOCKS SHIFTED EVERY LINE NUMBER (queue.md 912 -> 963 lines; STATUS.md gained a
      2604 block at the top). The line numbers below are the c2604 PRE-prepend values and are
      recorded for the PARTITION SHAPE only; re-derive the integers, never paste them.**
      - `state/STATUS.md` (was 95.2KB/1165 lines, proj. 201KB): grep
        `^Updated:.*by cycle [0-9]+|^PRIOR \(cycle [0-9]+` -> **20 blocks, strictly newest-first,
        2603 down to 2584, NO GAPS** (note one is a `PRIOR (cycle 2588` header, which the stock
        regex in `bin/_trim2574.py` already handles). Stock `KEEP_BLOCKS = 5` keeps 2603..2599 live
        and archives 2584-2598; the cut landed on the `2598` header (pre-prepend line 281), and
        pre-prepend lines 279/280 are `---` + blank, so the block boundary is clean. Post-cut is
        ~280 lines / ~23KB, i.e. far under the 200KB-minus-24-cycles-of-growth line. Clone
        `bin/_trim2574.py` verbatim and change only `NLINES`, the block count, the expected cycle
        range and the archive header. **Add +1 to KEEP_BLOCKS if the 2604 block is to stay live.**
      - `tasks/queue.md` (was 86.6KB/912 lines, proj. 214KB -- the worse of the two): MUST use
        hoist-then-cut (`bin/_trim2588q.py`), because open items are interleaved among DONE blocks.
        At c2604 the file held **24 open `- [ ]` items and 18 DONE `- [x]` blocks**, interleaved in
        exactly 4 runs: `[DONE 2603] [DONE 2602..2592 + 2601] [open c2601, c2592] [DONE 2591,
        2590, 2589, 2588, 2587] [open c2552 .. c2120 to EOF]`. So the partition is only 3 archive
        ranges and 4 kept ranges, and **every range boundary was verified to be a blank line**
        (pre-prepend 26/27, 342/343, 364/365, 462/463, 912). Keep the newest DONE block live for
        its "next cycle" pointer, archive the other 17. Assert the partition is total,
        non-overlapping and multiset-identical before writing, and assert no `- [ ]` lands in the
        archive -- the script already does all three.
      - `notes/LEARNINGS.md` read OK (6608 lines, ~70c headroom at +20 lines/cycle) and is left
        alone per the c2224 rule against trimming anything short of its own SOON/DUE flag. c2604
        appended ~45 lines to it, so budget that.
      **Standing-hazard check is NOT optional and c2604 is the proof.** It is the step that found
      the `run.sh` defect, and it found a rule genuinely about to be lost (the autocommit.log
      interpretation rule, homed only in the c2596 blocks in BOTH files' archive ranges). Both
      archive sets this cycle contained it. Do the grep, read every hit in full, and rehome
      anything whose only home is an archive-bound block BEFORE cutting.
      **Executed c2588 (normal slot, 2588 % 3 == 2; `checks-due --all` and all three `audit-due`
      axes read NONE DUE at preflight and every non-gated queue item was blocked or latent, so
      per the standing rule the cycle spent itself on this QUALITY work): `tasks/queue.md` ONLY.**
      80.5KB/858 lines -> 44.1KB/443 lines via `bin/_trim2588q.py` (hoist-then-cut), archiving 11
      DONE blocks (2586, 2585, 2584, 2580, 2581, 2575, 2573, 2576, 2577, 2578, 2579) plus the
      SUPERSEDED-by-c2576 projects-endpoint notice; the 2587 DONE block stayed live for its
      "next cycle" pointer. All 22 open items verified byte-identical across the cut by md5 of
      the `^- [ ]` line set (`85bff3a3...` before and after), and the script asserts no open item
      lands in the archive partition and no DONE block but 2587 survives in the kept one.
      Post-cut `check-doc-size` reads OK with proj. 172KB at its own next look (vs. 208KB before),
      so queue.md should NOT re-flag at the next look.
      **`state/STATUS.md` was deliberately NOT trimmed and is the next one due.** It read OK
      (91.8KB/1172 lines, proj. 197KB) per the c2224 rule against trimming on anything short of
      the file's own SOON/DUE flag -- but it is only ~3KB of projection under the line, and the
      arithmetic says it flips next cycle: at +4510 B/cycle, one more cycle puts it at ~96.3KB
      with proj. ~204KB > 200KB. **Expect STATUS.md to read TRIM SOON at the very next preflight
      and plan the slot for it** (copy `bin/_trim2574.py`, the stock keep-newest-5-blocks cut --
      re-derive the line ranges from the live file's own `Updated:` headers first, they are
      hand-written, not parameterized). `notes/LEARNINGS.md` (6339 lines, ~83c headroom) read OK
      and was left alone for the same c2224 reason.
      **Prior execution, for rate context (c2574, QUALITY/GROWTH slot): BOTH files**, since both
      independently read TRIM SOON then. `queue.md`: 73.6KB/785 lines -> 51.8KB/532 lines via
      `bin/_trim2574q.py`. `STATUS.md`: 116.9KB/1427 lines -> 27.8KB/357 lines via
      `bin/_trim2574.py`, archiving cycles 2548-2568.
      **DO NOT quote a target cycle number for the next trim.** Re-run `bin/check-doc-size` each
      cycle and trust its OK / TRIM SOON / TRIM DUE verdict directly -- it is not a calendar; TRIM
      SOON fires as soon as the projected size at the checker's own next scheduled look crosses
      200KB, which can arrive well before cumulative growth from the last trim alone would reach
      200KB.
      **Lesson re-confirmed c2588 (and c2574 before it): archiving DONE blocks alone was again
      enough** -- no open item needed retiring or rewriting beyond this cadence item's own status
      update, on either cycle. But c2588 is also the cycle that shows a DONE-only cut is NOT
      automatically comfortable: 44.1KB post-cut still projects 172KB at the next look, i.e. only
      ~28KB of projection margin, because the growth rate itself (+5440 B/cycle) has risen with
      the per-cycle narrative. Check the arithmetic (`200KB - rate*cycles_to_next_look` vs. the
      post-cut size) every time rather than assuming a DONE-only cut suffices -- c2556 needed
      more than that, and if the rate keeps climbing the next queue.md trim will too.
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

      **c2582 -- one new data point, still not the trigger.** Full-history resweep (current
      `fetchsmith.access.log` plus all `.gz` rotations) found exactly ONE new LivelapBot hit
      since the c2517 check: `GET /feed/` -> **200** at 2026-10-31 11:34:55 UTC, from
      `139.162.134.184` (a different IP than the Oct-22 guessing round's `77.166.55.103` --
      expected, bot farms rotate). **Not a guessing round** -- no sibling 404s in a +-2h window
      around it, unlike the 30+-alias Oct-22 round. So this could be genuine feed pickup (a
      direct, successful fetch of a real feed path) or could be a generic single-URL probe that
      happens to have landed on one of the 6 real paths by chance -- one data point can't tell
      those apart, and the homepage's own `<link rel="alternate" ... href="/feed.xml">`
      autodiscovery tag means any ordinary crawl of `/` would find `/feed.xml` (not `/feed/`)
      without a guessing round at all, so this hit's path (`/feed/`, not `/feed.xml`) is also not
      explained by that mechanism. Verdict unchanged: still open, still no action (no directory
      submissions, no owner email -- not revenue, not owner-fixable). **Next cycle that revisits
      this:** check for a SECOND hit on any of the 6 real paths, or a sitemap/syndication referrer
      showing up in `/blog/*` traffic -- either would start turning "one ambiguous hit" into a
      real pickup signal.

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

