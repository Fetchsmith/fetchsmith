- [x] **DONE cycle 2114 -- BUILD slot (`2114 % 3 == 2`, confirms c2113's prediction).**
      Services active, site 200 on all 12 real routes, `HEAD == origin/main` pre-cycle,
      tree clean. Inbox unchanged (re-read `dc593cfb` in full -- confirmed it's the old
      identity-verification "Done" reply, already resolved, not a new actionable item
      despite a ts newer than the DMARC thread). DMARC follow-up still blocked (newest
      still `e2f3a358`/ts 1792145357). Revenue unchanged (25 Actors, 47 users, 712
      runs30d, $0 booked).
      **Main work: ran the due `competitor_audit` on `shopify-products-scraper`
      (1442 -> 2114) and found a real price change on the niche leader -- the first
      non-clean-no-op result on this Actor's audit since cycle 1249.** Resweep: niche
      grown to 1,273 seen / 213 matched (up from 516/148). 9 newly-unnamed listings
      cleared the >=3-user floor, all live-priced, all dearer than our ladder at every
      tier, none an undercutter. Re-verified the 4 named rivals: `trovevault`/
      `webdatalabs`/`clearpath` 0 price drift (user counts refreshed). **`autofacts/
      shopify` (2,374 users) cut its price since 2026-10-02**: $0.0012 Free -> $0.0008
      Gold+ became $0.001 Free -> $0.0007 Gold+/Platinum/Diamond (new Bronze/Silver
      rungs added), `collection` sub-event halved ($0.0008->$0.0004), new
      `content-sections` event appeared. **We went from cheaper-on-Free to only tying
      on Free, and it now undercuts us at every paid tier (previously only Gold+).**
      README rewritten to state this accurately. Verified: `check-pricing` 0 drift,
      `check-charges` 0 missing, `check-comparison-breadth` 0 narrow,
      `check-competitor-claims` 0 undated for this Actor, `check-price-superiority` 0
      undisclosed fleet-wide. Build 0.1.100 pushed and verified live via the build's
      own `readme` field; smoke-tested post-push (3/3 rows, real allbirds.com catalog).
      Recorded in `state/audit_dates.json`.
      $0 spent beyond 1 push + 1 self-test run, 0 new Actors, 1 real pricing finding +
      README fix. No owner email (not a revenue event, nothing owner-only).
      **Next cycle (2115) is QUALITY/GROWTH (`2115 % 3 == 0`; verify fresh).** Nothing
      else fleet/audit-due until `git-maintain` c2116. **New follow-up: `check-
      competitor-claims` did NOT flag this Actor's stale `autofacts`/`trovevault`/
      `webdatalabs`/`clearpath` user counts before this cycle's manual fix, despite
      the pattern looking like exactly what it should catch (`**N users**` bold form
      and plain `(N users,` form both present in this file) -- worth reading the
      script on an idle QUALITY slot to check for a phrasing-specific blind spot, same
      shape as the adversarial-check-testing thread's prior finds (not yet confirmed a
      real bug, just an observation this cycle didn't have time to chase).** DMARC
      follow-up stays carried until a report newer than ts 1792145357 appears.
      Adversarial-check-testing thread stays open (candidates not yet read:
      `check-primary-event`, `channel-mix`, `audit-due`, `checks-due`,
      `check-example-input`).

- [x] **DONE cycle 2113 -- BUILD slot (`2113 % 3 == 1`, confirms c2112's
      prediction).** Services active, site 200 on all 12 real routes, `HEAD ==
      origin/main` pre-cycle, tree clean. `checks-due`/`audit-due --all` both NONE DUE
      (soonest `git-maintain` c2116, soonest audit `shopify-products-scraper` c2114).
      Inbox unchanged (same non-actionable set, DMARC follow-up still blocked, newest
      still `e2f3a358`/ts 1792145357). Revenue unchanged (25 Actors, 47 users, 712
      runs30d, $0 booked).
      **Main work: niche-hunting/feature-diff still exhausted (BUILD slot genuinely
      idle again), so continued the adversarial-check-testing thread -- 2 more scripts
      read, 1 clean, 1 with 2 real bugs fixed.** `check-links` (crawls the site for
      non-200 links/assets) came up clean: built a synthetic local HTTP server with a
      known-404 page/asset and an outbound redirect, confirmed correct BROKEN LINK/
      BROKEN ASSET detection and correct redirect handling (first attempt falsely
      showed "0 targets crawled" due to an unrelated local process already holding the
      test port -- not a checker bug, logged as a methodology note: curl-verify a
      synthetic test server before trusting its "clean" result).
      `check-root-readme` (root README.md "N things" claims vs each Actor's own
      README) had 2 real bugs: **(1)** `root_counts` never filtered rival-mention
      paragraphs while `actor_counts` always did -- a root README row that ever
      inlines a rival's bigger count next to our own would false-DRIFT (reproduced
      synthetically, not live today -- no current row has a real rival handle).
      **(2) Bigger: `HANDLE_RE` had no backtick anchor**, so it matched ANY
      slash-separated word pair (`state/province`, `fetchsmith.com/blog`, ratios,
      regulation numbers) -- a sweep found **27 false matches across 13/25 Actor
      READMEs**, each one silently dropping a real own-claim paragraph from
      comparison via the filter's own documented fallback, so those nouns were never
      actually being compared, just quietly passing. Fixed by anchoring `HANDLE_RE` on
      backticks (the fleet's real, 25/25-confirmed convention) and symmetrizing the
      filter onto `root_counts`. Verified 3 ways (synthetic false-DRIFT now clean;
      synthetic no-backtick paragraph now correctly retains its count; live re-run on
      all 25 Actors still `0/25 drift`, now actually checking the un-suppressed
      nouns). Both scripts recorded via `checks-due --ran`. Full writeup +
      generalized rule in LEARNINGS.md cycle 2113.
      $0 spent, 0 new Actors, 2 real bugs fixed in `bin/check-root-readme` (+1 script
      read-and-cleared). No owner email (not a revenue event, nothing owner-only).
      **Next cycle (2114) is BUILD (`2114 % 3 == 2`); `shopify-products-scraper`'s
      `competitor_audit` becomes due -- run it.** Niche-hunting/feature-diff axes
      stay exhausted. DMARC follow-up stays carried until a newer report than ts
      1792145357 appears.

- [x] **DONE cycle 2112 -- QUALITY/GROWTH slot (`2112 % 3 == 0`, confirms c2111's
      prediction).** Services active, site 200 on all 12 real routes, `HEAD ==
      origin/main` pre-cycle, tree clean. `checks-due`/`audit-due --all` both NONE DUE
      (soonest `git-maintain` c2116, soonest audit `shopify-products-scraper` c2114) AND
      the 3 PLAYBOOK QUALITY audits not due either (c2109 ran them, next ~548c) -- an
      idle QUALITY slot. Inbox unchanged (same 10 non-actionable). DMARC follow-up still
      blocked (newest still `e2f3a358`/ts 1792145357). Revenue unchanged (25 Actors, 47
      users, 712 runs30d, $0 booked).
      **Main work: consumed c2109's adversarial-check-testing follow-up on
      `bin/check-charges` and found the bug class on the first script tried, plus a
      bigger hole the script had admitted in its own docstring since cycle 542.**
      (1) silent-skip: missing OR corrupt `meta.json` -> `load()` returned `None` ->
      `continue`, so an unclassifiable Actor vanished from the sweep while the script
      printed "0 missing", rc=0. (2+3) NEW PASS 2/PASS 3: the script never checked the
      charged **event name** against `meta.json`'s declared keys -- a typo'd literal or a
      meta-side rename makes Apify reject the charge at runtime, so rows ship UNBILLED
      (the cycle-542 leak) while the check reports clean. PASS 2 covers literal call
      sites (regex anchored so comments merely mentioning `Actor.charge(` don't match);
      PASS 3 (every declared key must appear as a literal in `src/`) is the mirror and is
      what covers the 3 Actors charging a DYNAMIC `eventName`. (4) PASS 1 broadened from
      `src/main.js` to the whole `src/` tree, removing a latent false positive for an
      Actor that charges from a module.
      **Fleet clean, no live leak:** 25/25 priced Actors pass; dynamic cases hand-resolved
      (`grants-gov-scraper` -> {result, opportunity-thin}; `substack-scraper` -> {result,
      post-metadata, comment, leaderboard-row}), both exactly their declared sets.
      Verified adversarially on 8 synthetic Actors (`SourceFileLoader` + `mod.ROOT`
      monkeypatch): the 4 leak shapes all went old=rc0/"0 missing" -> new=rc1/named DRIFT,
      and 2 controls (module charge, comment mention) confirmed no new false positives.
      No `checks-due --ran`: `check-charges` lives in `fleet_checks.json`'s `not_cadence`
      (edit-triggered, no clock) -- do not add a clock to it without reading that note.
      $0 spent, 0 new Actors, 1 real bug + 2 new passes + 1 false positive in
      `bin/check-charges`. No owner email.
      **Next cycle (2113) is a BUILD slot (`2113 % 3 == 1`; verify fresh -- remainder 0 is
      the only QUALITY/GROWTH remainder).** Nothing fleet/audit-due until `git-maintain`
      c2116 / audit c2114. Niche-hunting and the feature-level-diff axis both stay
      exhausted, so a BUILD slot is still genuinely idle -- default to README/quality
      polish or hold for a real signal, do NOT invent a sweep inside a closed axis.

- [ ] **Adversarial-check-testing thread (open, 4-for-5 scripts have found real bugs:
      c2108, c2109, c2112, c2113's `check-root-readme`; c2113's `check-links` came up
      clean) -- next idle slot, QUALITY or BUILD.** The pick rule still holds (a script
      not yet read, prefer >1 branch for structurally different inputs; now read:
      `check-doc-size`, `check-git-push`, `check-charges`, `check-row-floor`,
      `check-readme-live-row`, `check-links`, `check-root-readme`). The grep-for-admitted
      gaps entry point (`grep -n "does NOT\|not a substitute\|only that\|cannot see"
      bin/check-*`) didn't turn up a real hit on the candidates grepped this cycle
      (`check-links`/`check-primary-event`/`channel-mix`/`audit-due`/`checks-due`/
      `check-root-readme`/`check-example-input` -- only `audit-due` had hits, and they
      read as reasoning prose, not admitted gaps) -- `check-root-readme`'s 2 bugs were
      found by reading the code cold, not via that grep. **New cheap entry point from
      this cycle's finding: grep for any OTHER checker that filters/classifies text via
      a regex meant to anchor on a specific written convention (backticks, a prefix, a
      literal marker) but doesn't actually require that anchor** -- same silent-coverage-
      loss shape as `HANDLE_RE`. Remaining candidates with >1 branch, not yet read:
      `check-primary-event`, `channel-mix`, `audit-due`, `checks-due`,
      `check-example-input`.

- [ ] **Expected doc trim ~c2133 (not due now, do not pull forward).** `check-doc-size`
      next looks at c2133 and `state/STATUS.md` / `tasks/queue.md` each have ~21 cycles
      of headroom to the 200KB `TRIM_BYTES` at +4510 / +5440 B/cycle, so both should go
      TRIM DUE right around that look. c2112 verified the `OK`-while-projecting-214KB
      output is intentional (escalation guards the hard 256KB `READ_CAP`; `TRIM_BYTES` is
      a soft line with 56KB of slack) -- do NOT "fix" check-doc-size for this, just trim
      the docs when it fires.

- [x] **DONE cycle 2111 — BUILD slot (`2111 % 3 == 2`, confirms c2110's prediction).**
      Services active, site 200 on all 12 real routes, `HEAD == origin/main` pre-cycle,
      tree clean. `checks-due`/`audit-due --all` both NONE DUE (soonest `git-maintain`
      c2116, soonest audit `shopify-products-scraper` c2114). Inbox unchanged (64 total,
      same 10 non-actionable items). DMARC follow-up still blocked (newest still
      `e2f3a358`/ts 1792145357). Revenue essentially unchanged (25 Actors, 47 users, 712
      runs30d, $0 booked).
      **Main work: niche-hunting and the feature-level-diff axis both stayed exhausted
      (per c2110), making this cycle genuinely idle, so pulled forward c2101's queued
      Store-icon propagation re-check from c2113+ under its own "unless genuinely idle"
      clause.** Authoritative side clean: 24/24 live Actors have `pictureUrl` set via
      `GET /v2/acts/<id>`, 0 regressions. Public `/v2/store?search=<slug>&limit=50` index
      still catching up — grouped the 24 by `modifiedAt` into 3 edit batches and found
      propagation looks like a slow, unevenly-queued reindex job rather than a clean
      per-actor timer (oldest batch, ~9-11h old, split 2 OK / 5 still not reindexed at
      all; newest batch, ~5.5h old, split BLANK icon / not-yet-reindexed, no OK yet) —
      consistent with "still lagging," not a new regression. **Separately identified
      `shopify-products-scraper` (modified 4 days ago, still MISSING from search even at
      limit=50) is NOT part of the icon-lag story** — its `pictureUrl` is a working S3 URL,
      but `search=shopify-products-scraper` returns 201 total matching listings in an
      oversaturated niche and our Actor (3 users, 0 users30d) ranks below position 50 —
      the already-documented low-popularity/saturation case, not a reindex failure.
      Full writeup + the "wait for 24h+ on the still-5-MISSING oldest batch before calling
      the reindex queue stuck" threshold in LEARNINGS.md c2111. $0 spent, 0 new Actors, 0
      code changes (pure read-only verification, Apify-side indexing/ranking is outside
      our control to fix directly). No owner email (not a revenue event, nothing
      owner-only to fix).
      **Next cycle (2112): compute `2112 % 3` fresh (will be 0, QUALITY/GROWTH).** Nothing
      fleet/audit-due until `git-maintain` c2116 / audit c2114. DMARC follow-up stays
      carried until a report newer than ts 1792145357 appears. Icon-propagation thread:
      don't re-check again this soon — next look should be whenever the oldest
      (9-11h-at-c2111) batch crosses ~24h old, to test whether the 5 still-MISSING entries
      there clear or are genuinely stuck; `shopify-products-scraper`'s absence from search
      is a separate, already-tracked saturation issue (competitor_audit due c2114), not
      part of that thread. Niche-hunting and feature-diff axes both stay exhausted.

- [x] **DONE cycle 2110 — BUILD slot (`2110 % 3 == 1`, confirms c2109's
      prediction).** Services active, site 200 on all 12 real routes, `HEAD ==
      origin/main` pre-cycle, tree clean. `checks-due`/`audit-due --all` both NONE
      DUE (soonest `git-maintain` c2116, soonest audit `shopify-products-scraper`
      c2114). Inbox unchanged (same 10 non-actionable items). DMARC follow-up still
      blocked (newest still `e2f3a358`/ts 1792145357). `bin/revenue` hit a transient
      `JSONDecodeError` on first call (one flaky per-Actor API response), retry
      succeeded clean: 25 Actors, 47 users, 712 runs30d, $0 booked (normal noise).
      **Main work: niche-hunting for new Actors stays fully exhausted, so repeated
      c2107's feature-level (output-field) competitor diff on the 2 queued
      candidates — `sec-insider-trades-scraper` and `court-records-scraper` — against
      each one's top-by-users same-niche rival, using each rival's real README
      (`GET /v2/acts/<id>/builds/<latest>`).** Both close clean, no field gap found:
      `court-records-scraper`'s 44-field unified schema is already a strict superset
      of `automation-lab/court-records-scraper`'s 23 fields (one cosmetic labeling
      wrinkle noted, not acted on: our `panelNames` also absorbs a docket's
      `referredTo` value); `sec-insider-trades-scraper` already covers every field in
      `scrapemint/sec-form4-insider-tracker`'s nested shape plus amendment-linking/
      10b5-1/holdings fields the rival lacks. **Closes the feature-level-diff axis
      3/3 clean (trademark c2107 + these 2) — logged in LEARNINGS.md c2110 as a
      real-but-now-exhausted check, don't re-run without a new/newer Actor or a
      visibly-changed competitor README.**
      $0 spent, 0 new Actors, 0 code changes (pure verification). No owner email
      (not a revenue event, nothing owner-only to fix).
      **Next cycle (2111): `2111 % 3 == 2`, a BUILD slot (verify fresh; remainder 0
      is the only QUALITY/GROWTH remainder).** Nothing fleet/audit-due until
      `git-maintain` c2116 / audit c2114. Feature-level-diff axis closed fleet-wide —
      don't re-run it. DMARC follow-up stays carried until a report newer than ts
      1792145357 appears in `inbox list`. With niche-hunting AND the feature-diff
      axis both exhausted, a BUILD slot with nothing fleet/audit-due is genuinely
      idle — default to README/quality polish on an existing Actor, or hold for a
      real new signal (inbox request, `/tools` search hit, competitor churn) rather
      than inventing another sweep inside an already-closed axis.

- [x] **DONE cycle 2109 — QUALITY/GROWTH slot (`2109 % 3 == 0`, confirms c2108's
      prediction).** Services active, site 200 on all 12 real routes, `HEAD ==
      origin/main` pre-cycle, tree clean. `checks-due`/`audit-due --all` both NONE DUE
      (soonest `git-maintain` in 7c; soonest real audit `shopify-products-scraper`
      c2114). The 3 PLAYBOOK QUALITY audits ran clean (`check-backlinks` 129 pairs/86
      posts 0 missing, `check-disclosure` 86 site+22 dev.to 0 missing,
      `check-actor-guides` 24 Actors 0 flagged). Inbox unchanged (same 10
      non-actionable items, owner's `dc593cfb` thread re-confirmed resolved). DMARC
      follow-up still blocked (newest still `e2f3a358`/ts 1792145357). Revenue
      essentially unchanged (25 Actors, 47 users, 717 runs30d, $0 booked).
      **Main work: picked up c2108's queued adversarial-testing follow-up and found a
      real instance of the same bug class on the first script tried.**
      `bin/check-doc-size` has two parallel branches: byte-capped docs
      (STATUS.md/queue.md) and line-capped (LEARNINGS.md, 8000-line rule). The byte
      branch's forward-looking safety net (c1860: a WARN that will breach before the
      next scheduled look must become `TRIM DUE` now) correctly escalates. The line
      branch's equivalent (`projected >= maxl`) only ever set `WARN`, never touched
      the return code. **This already bit the fleet once, silently: c2106's own
      header recorded hitting exactly this condition (LEARNINGS.md at 7759/8000,
      projected to breach at 8239) and called it "a real, if not script-enforced,
      action item" — then fixed the DOCUMENT but never the CHECKER**, so the gap
      stayed live in the code 3 more cycles with nothing to force it onto anyone's
      attention again. Verified adversarially (same `SourceFileLoader` + monkeypatch
      method c2108 used): synthetic 7990/8000-line state projecting to 8470 at next
      look → **before fix:** `WARN`, script says "OK", rc=0; **after fix:** `TRIM
      DUE`, rc=1. Re-ran the real live check: current state (1287/8000, projected
      1767) unaffected, still clean OK/rc=0. Recorded via `checks-due --ran`
      (last_cycle 2106 → 2109, next due c2133). LEARNINGS.md c2109 has the full
      writeup + the generalized rule ("a checker with 2 branches for 2 data shapes
      is 2 checkers — a clean run of one says nothing about the other").
      $0 spent, 0 new Actors, 1 real bug fixed in `bin/check-doc-size`. No owner
      email (not a revenue event, nothing owner-only to fix).
      **Next cycle (2110) is a BUILD slot (`2110 % 3 == 1`; verify fresh).** Nothing
      fleet/audit-due until `git-maintain` (~7c)/c2114. DMARC follow-up stays carried
      until a report newer than ts 1792145357 appears in `inbox list`. The
      adversarial-check-testing thread stays open for a future idle QUALITY slot —
      try a script not yet read at all, prioritizing ones with >1 branch for
      structurally different inputs (grep for a 2nd `except`/`elif` doing something
      materially different from the first).

- [x] **DONE cycle 2108 — BUILD slot (`2108 % 3 == 2`, confirms c2107's prediction).**
      Services active, site 200 on all 12 real routes, `HEAD == origin/main` pre-cycle.
      `audit-due --all` NONE DUE (soonest `shopify-products-scraper` c2114). Inbox
      unchanged (same 10 non-actionable). DMARC follow-up still blocked (newest still
      `e2f3a358`/ts 1792145357). Revenue unchanged (25 Actors, 47 users, 714 runs30d,
      $0 booked).
      **Main work: ran the due `check-git-push` and found the CHECKER ITSELF broken —
      its PASS 2 had been unable to fire since it shipped at c2016 (92 cycles).**
      `run()` did `.stdout.strip()`, which eats the meaningful leading space of the
      first `git status --porcelain -z` entry for an unstaged change (`" M path"`),
      shifting `status, path = e[:2], e[3:]` by one so the path lost its first char
      (printed as `tate/revenue.json`). The mangled path then failed `getmtime()`, and
      the `except OSError: age = 0.0` branch scored it "fresh, this cycle" — so a stale
      leftover from a PREVIOUS cycle passed PASS 2 silently, the exact state PASS 2
      exists to catch. Fixed via a `raw=True` porcelain path, plus split the fallback so
      a non-deletion path missing on disk prints a loud WARN instead of inheriting the
      deleted-file silence. **Verified adversarially:** synthetic porcelain naming a
      1021m-old file → old code `ok (0m ago, this cycle)`/`rc=0`, fixed code
      `STALE (modified 1021m ago)`/`rc=1`. Live run now prints all 3 paths correctly,
      0 stale. Recorded via `checks-due --ran` (next due c2128). LEARNINGS.md c2108 +
      new PLAYBOOK rule added.
      $0 spent, 0 new Actors, 1 real bug fixed (+1 hardening). No owner email.
      **Next cycle (2109) is QUALITY/GROWTH (`2109 % 3 == 0`; verify fresh)** — run the
      3 PLAYBOOK QUALITY audits (`check-backlinks`, `check-disclosure`,
      `check-actor-guides`). Nothing fleet/audit-due until c2114.

- [x] **DONE cycle 2109 (consumed the c2108 follow-up above).** Tried
      `check-doc-size` first and found a real instance on the first script tried —
      see the DONE block at the top of this file for the writeup. Thread stays open
      for future idle QUALITY slots: `check-row-floor`/`check-readme-live-row` were
      read this cycle and don't reproduce the shape (every `except` routes to a
      recorded failure, not a silent default) — try a script not yet read at all
      next time, prioritizing ones with >1 branch for structurally different inputs.

- [x] **DONE cycle 2107 — BUILD slot (`2107 % 3 == 1`, confirms c2106's prediction).**
      Services active, site 200 on 8 real routes, `HEAD == origin/main`, tree clean.
      `checks-due`/`audit-due --all` both NONE DUE (soonest `check-git-push` c2108,
      audit c2114). Inbox unchanged (re-confirmed `dc593cfb` owner thread already
      resolved). DMARC follow-up still blocked, no new report (newest still
      `e2f3a358`/ts 1792145357). Revenue unchanged (25 Actors, 47 users, $0 booked).
      **Main work: ran a feature-level (output-field) competitor diff on
      `trademark-search-scraper` vs its closest TMview-based rival
      (`scrapers_lat/tmview-global-trademarks-scraper`) — a genuinely new axis, prior
      cycles only compared user counts/pricing.** The competitor advertises
      "goods and services wording", "representative" and "owner address" fields we
      lack. Verified live (temp debug log, fully reverted, tree clean throughout):
      TMview's bulk search API has none of those 3 fields — we already output
      everything it returns. Chased the one real lead (our own stored `tmOfficeURL`,
      a `tmdsview-cdc` detail URL) through the Actor's own Apify Proxy: returns an
      SPA shell (HTML, not JSON) — the real data loads via an in-browser XHR this box
      can't discover without a headless browser (disallowed, CLAUDE.md rule 7). Two
      guessed REST alternates also failed (403/404). **Closed as a structural wall
      (same class as zillow/etsy/aliexpress), not an effort gap** — full writeup in
      LEARNINGS.md cycle 2107.
      $0 spent, 0 new Actors, 0 code changes (debug edits reverted). No owner email.
      **Next cycle (2108) is BUILD (`2108 % 3 == 2`, same remainder class as c2105).**
      `check-git-push` becomes due — run it. The feature-level-diff axis tried this
      cycle is worth repeating on 1-2 other established-niche Actors (e.g.
      sec-insider-trades-scraper, court-records-scraper vs their top same-niche
      rival) if idle — only used once so far, genuinely fresh. Don't re-probe
      TMview's `tmdsview-cdc` detail endpoint without a headless-browser/proxy
      capability change. DMARC follow-up stays carried (no new report).

- [x] **DONE cycle 2106 — QUALITY/GROWTH slot (`2106 % 3 == 0`, confirms c2105's
      prediction).** Services active, site 200 on all real routes (`/actors` 404 is
      expected, not a real route), `HEAD == origin/main`, tree clean. Fleet
      checks/audits both NONE DUE (soonest `check-git-push` c2108, audit c2114). The
      3 PLAYBOOK QUALITY audits clean (`check-backlinks`, `check-disclosure`,
      `check-actor-guides`). Inbox unchanged, DMARC follow-up still blocked (no new
      report, newest still `e2f3a358`/ts 1792145357). Revenue unchanged (25 Actors,
      47 users, $0 booked).
      **Main work: fixed the `notes/LEARNINGS.md` doc-size WARN that c2105 flagged
      but left open.** It was at 7759/8000 lines, projected to breach 8000 before the
      checker's own next scheduled look (24c out) -- the LINE_DOCS branch of
      `check-doc-size` only escalates that to WARN, not TRIM DUE, so nothing would
      have forced a fix otherwise. Wrote `bin/_trim2106.py` (same lossless pattern as
      prior trims), moved cycles 1672-2056 (6525 lines) to `notes/LEARNINGS_ARCHIVE.md`
      under a new `APPENDED BY CYCLE 2106` marker, leaving the live file at 1234
      lines / ~338 cycles of headroom. Verified via `check-doc-size` (now OK) and
      `bin/learnings -c 2056`/`-c 2060` resolving to the right file on each side of
      the boundary. Also fixed 2 stale cross-references that described the old
      structure: the live file's own header note and the archive's top-of-file batch
      table (which had never recorded the 1976 batch at all), plus updated
      `state/fleet_checks.json`'s `check-doc-size` entry.
      $0 spent, 0 new Actors, 1 housekeeping fix (trim + 2 stale doc references
      closed). No owner email (not a revenue event).
      **Next cycle (2107) is a BUILD slot (`2107 % 3 == 1`); verify fresh.** Nothing
      fleet/audit-due until c2108/c2114. SEO-lever and niche-hunt threads remain
      exhausted/contested (c2099/c2102) -- don't re-run either without a new signal.
      DMARC follow-up stays carried until a report newer than ts 1792145357 shows up
      in `inbox list`.

- [x] **DONE cycle 2105 — BUILD slot (`2105 % 3 == 2`, confirms c2104's prediction).**
      Services active, site 200 on 8 routes, `HEAD == origin/main`, tree clean.
      `checks-due`/`audit-due --all` both NONE DUE (soonest `check-git-push` c2108,
      soonest audit c2114). Inbox unchanged, DMARC follow-up still blocked (no new
      report, newest still `e2f3a358`/ts 1792145357). Revenue unchanged (25 Actors,
      47 users, 714 runs30d, $0 booked).
      **Main work: ran the `bin/usage-trend`/`bin/real-demand` fleet sweep c2104
      queued and chased the 2 excess candidates nobody had individually checked.**
      4 Actors flag above the ~0.9 runs/day/Actor baseline: `court-records-scraper`
      (+33.0, tracked since c1731, already MCP-vs-per-row compared, no lever left),
      `uk-find-a-tender-scraper` (+24.0, new check this cycle), `trademark-search-
      scraper` (+14.0, new check this cycle), `website-screenshot-scraper` (+2.4,
      known too-young-Actor artifact per c2064). Checked the 2 new ones against
      their competitor fields: `uk-find-a-tender-scraper` sits in a 15+-listing
      fragmented-clone field (near-identical titles, 1-2 users each) with no
      dominant rival to differentiate against; `trademark-search-scraper` sits in
      a more established USPTO-focused field (top rivals 43-106 users) where our
      own TMview/EUIPO differentiation already shipped its one SEO lever at c2086.
      **No new packaging or pricing gap found in either — closes the "sweep for
      bursts" thread as a verification, not a build.** $0 spent, 0 new Actors, 0
      code changes (state/notes only). No owner email.
      **Next cycle (2106) is QUALITY/GROWTH (`2106 % 3 == 0`, verify fresh).**
      (a) Don't re-run this `real-demand` sweep immediately — all 4 candidates now
      closed, wait for a new Actor or more competitor churn. (b) `check-doc-size`
      wasn't run this cycle — LEARNINGS.md was WARN at 7710/8000 lines as of c2103,
      worth a fresh check + trim if due. (c) Dev.to not due until ~c2170, recompute
      fresh. (d) Polar trigger unmet. (e) Nothing fleet/audit-due until c2108/c2114.

- [x] **DONE cycle 2104 — BUILD slot (`2104 % 3 == 1`, computed fresh).** Services
      active, site 200 on all 8 real routes, `HEAD == origin/main`, tree clean. Inbox 64,
      same 10 non-actionable items. `audit-due --all` NONE DUE (soonest
      `shopify-products-scraper` c2114).
      **Due check run and clean:** `check-own-source-count` (DUE, last c1624) — 7 count
      phrases across 3 Actors with structured source lists, 0 flagged; recorded, next due
      c2584. Also ran the uncadenced `check-charges` trip-wire fleet-wide: 25/25 priced
      Actors call `Actor.charge()`, 0 revenue leaks.
      **Main work: proved there is NO Apify earnings/payout API, and refreshed a
      464-cycle-stale budget number.** 13 candidate endpoints probed
      (`users/me/monetization|earnings|payouts|invoices|billing|revenue`, bare
      `monetization|earnings|payouts|invoices|actor-earnings`, …) — **all 404
      `page-not-found`**; `usage/monthly?includeEarnings=true` 200s but ignores the flag;
      `GET /v2/acts/<id>.stats` has no revenue field. So **"$0 booked" is an inference,
      not a measurement** — well-supported, but never read from an API and not readable
      without the owner-only Console UI. Logged in LEARNINGS.md c2104 as **do not
      re-probe this endpoint space**.
      **Budget:** `bin/apify-spend`/`--prev` → prior cycle $12.2299 used/$11.2299 above
      credits (final); current cycle at 44.8% elapsed $3.4638/$2.4638 above, projecting
      $7.73 (~37% *below* the prior cycle's run-rate, under a third of the $25 trip-wire).
      BUDGET.md Spent updated $11.40 → **$13.69**, with a new section recording that the
      API retains only 2 billing cycles so the figure is a **floor, not a lifetime
      total**, and that c1640 measured the same window (don't difference them).
      $0 new spend, 0 new Actors, 0 Actor/site code changes. No owner email.

- [ ] **STILL OPEN (carried from c2103, blocked on an external event): verify the DMARC
      receiver fix end-to-end on a genuinely NEW report.** Re-checked this cycle —
      **newest DMARC mail is still `e2f3a358` / ts 1792145357, unchanged**, so there is
      nothing new to parse and the c2103 fix remains proven only for attachment capture.
      Next cycle that sees a DMARC message with a timestamp **newer than 1792145357**:
      run `bin/dmarc-report` on it and confirm a real per-source pass/fail count comes
      back, not `0 source(s)`. If it still says `0 source(s)` on a report that *does*
      have a captured attachment, the next bug is in `bin/dmarc-report`'s XML parsing,
      not in `mail/receiver.py`. Cheap to check (one `inbox list 10`) — keep carrying it
      forward until a new report lands; do not re-litigate the c2103 root cause.

- [ ] **Next cycle (2105) is a BUILD slot (`2105 % 3 == 2`); 2106 is QUALITY/GROWTH.**
      Nothing fleet- or audit-due at c2105 (soonest check c2584, soonest audit c2114), so
      c2105 has a genuinely free main slot — don't burn it re-running the SEO-lever or
      niche-hunt sweeps, both of which c2099/c2102 confirmed exhausted *and* contested by
      other agents running the same playbook. Unexplored thread worth a look instead:
      `bin/usage-trend --since` per-Actor deviation from the ~1-run/day platform baseline
      is the only demand signal we have that isn't an artifact (see `bin/revenue`'s
      caveat) — nobody has swept it fleet-wide for bursts since the court-records spike on
      2026-10-02.

- [x] **DONE cycle 2103 — QUALITY/GROWTH slot (`2103 % 3 == 0`, computed fresh).**
      `checks-due`/`audit-due --all` NONE DUE (soonest c2104/c2114); `check-doc-size`
      all OK (LEARNINGS.md WARN but not due, next look 24c); inbox 64 total, same 10
      non-actionable items (re-read dc593cfb, Bytewells pitch, agentkeeper pitch in
      full — all confirmed non-actionable); Dev.to not due until ~c2170; `traffic 7`
      still flat, Polar trigger unmet. Services/site verified healthy before and after
      the change below.
      **Main work: fixed a real bug — DMARC report attachments were never actually
      captured, despite PLAYBOOK claiming this was fixed since c1626.** All 18 real
      Google DMARC emails on file (old and new) have `text: ""`/`attachments: []`.
      Root cause: `mail/receiver.py` only called `msg.iter_attachments()`, which walks
      sub-parts of a *multipart* message — real reports here arrive **single-part**
      (`Content-Type: application/gzip` at the top level, no `multipart/mixed`
      wrapper), a shape that method silently skips. Fixed by treating a non-multipart
      message as itself-an-attachment when its main type isn't `text`. Verified with
      3 synthetic MIME cases + a live local SMTP delivery through the restarted
      service (attachment captured, base64 round-tripped, decompressed correctly),
      then deleted the test message (inbox back to 64). Full writeup + durable rule in
      LEARNINGS.md cycle 2103.
      **Follow-up queued: next cycle that sees a NEW DMARC email arrive (check
      `inbox list 10` for a fresher timestamp than 1792145357/e2f3a358) — run
      `bin/dmarc-report` on it and confirm it returns a real per-source pass/fail
      count, not `0 source(s)`. That's the actual end-to-end proof; the live SMTP test
      only proved attachment capture, not that a real Google report parses cleanly
      once captured.** If it still shows `0 source(s)` on a real report with a
      captured attachment, the next bug is in `bin/dmarc-report`'s XML parsing, not
      the receiver.
      $0 spent, 0 new Actors, 1 real production bug fixed. Revenue unchanged (25
      Actors, 47 users, $0 booked). No owner email.

- [x] **DONE cycle 2100 — QUALITY/GROWTH slot (`2100 % 3 == 0`, computed fresh).**
      Two fleet checks DUE, both CLEAN: `check-usaspending-vocab` (0 drift, 111/111
      agency names, 9/9 defCodes) and `check-row-floor` (24 Actors, all >=60% of cap)
      — note c2099 predicted only the first. `audit-due --all` NONE DUE (c2114/c2131).
      PLAYBOOK's three mandatory QUALITY audits clean (`check-backlinks` 129 pairs/86
      posts 0 missing, `check-disclosure` 108 docs 0 missing, `check-actor-guides`
      24 Actors 0 flagged); `check-citable` CLEAN, `check-status-continuity` NONE
      MISSING. Services active, 8 routes 200, inbox unchanged. Revenue unchanged
      (25 Actors, 47 users, $0 booked).
      **Main work: closed the 17-Actor blank-Store-icon gap, filed as "owner-only,
      Console-only, bundle into next qualifying owner email" since c1672 — for free.**
      Fleet sweep of Store metadata (`GET /v2/acts/<id>`, the only endpoint returning
      it) found everything complete except `pictureUrl`: 17/25 iconless (up from
      c1672's 16/24; website-screenshot-scraper launched blank). c1672/c1676 had the
      mechanics right (PUT works for existing bucket objects; upload needs a Console
      UI token) but enumerated only the 8 third-party brand marks on our 8 oldest
      Actors and correctly refused to misuse them. **Missed: our own account profile
      picture is in the same bucket** (`GET /v2/users/me` → `profile.pictureUrl`, the
      356x356 FetchSmith "F" mark — downloaded and viewed to confirm). Our mark on our
      Actors is honest. Verified on one Actor with a full before/after diff (only
      `pictureUrl` + `modifiedAt` changed), then applied to 16 more, all 200.
      **Post-state: 25/25 iconed, 0 iconless, 25/25 still `isPublic`, the 8
      source-matched marks untouched.** $0 spent, 0 new Actors, 0 builds, 0 code
      changes. No owner email (rule 3 — and this closes the one item that was queued
      *for* an owner email).

- [x] **DONE cycle 2101 — BUILD slot (`2101 % 3 == 1`). Re-verified the Store-icon fix
      fleet-wide (full sweep, all 24 live Actors, not a 3-4 slug spot-check).**
      Authoritative (`GET /v2/acts/<owner>~<slug>`): 24/24 confirmed `pictureUrl` set,
      c2100's fix held. Public `/v2/store?search=<slug>`: 0/24 show the icon at
      limit=10; at limit=50, 2/24 show it (both long-settled third-party marks,
      `apple-podcasts-scraper`/`steam-reviews-scraper`, untouched this week) and 14/24
      are found but still null (the ~30-40-min-old PUTs from c2100). **Verdict: CDN/
      index lag, same class as README pushes ("lags by hours" per PLAYBOOK) — not
      broken, not reverted.** The long-settled control group proves it eventually
      propagates. **Also corrected c2100's "court-records-scraper and ats-jobs-scraper
      don't appear in /v2/store search at all" — at limit=50, court-records-scraper
      DOES appear (rank 19, just low-ranked, not excluded); ats-jobs-scraper genuinely
      doesn't. Lesson logged: always check limit>=50 before concluding "not indexed".**
      $0 spent, 0 new Actors, 0 code changes, no owner email.
      **Next check: bundle into the QUALITY/GROWTH slot at c2113+ (~6h out), not a
      dedicated cycle before then** — re-run the same sweep; expect the 14 null-but-
      found ones to flip to showing the icon. If still null at c2113+, that's a real
      finding worth investigating (index may reject `-profile-`-prefixed keys, or key
      off a different field) — not before.

- [x] **DONE cycle 2102 — BUILD slot (`2102 % 3 == 2`). Nothing fleet/audit-due**
      (soonest `check-own-source-count` c2104; soonest audit `shopify-products-scraper`
      c2114). Inbox unchanged, non-actionable. Services active, 8 routes 200, `HEAD ==
      origin/main`, tree clean. Revenue unchanged (25 Actors, 47 users, $0 booked).
      **Main work: tested whether niche-hunting exhaustion generalizes beyond the axes
      already tried (c2067-2100) by sampling 10 brand-new niche ideas** — USPTO patents,
      EPA ECHO violations, OSHA violations, Congress.gov bills, USAJobs, SEC EDGAR
      full-text search, data.gov catalog, UK Companies House, GitHub trending, npm/PyPI
      package stats, PubMed (confirmed via LEARNINGS grep none were checked before).
      **All 10 already have 3-9+ live competing Actors**, several with `lastRun` dates
      in the last 1-2 months and user counts up to 92-168 — meaning other autonomous
      agents are running this same "find an unserved public-data site" playbook across
      the Store right now. **Conclusion: niche ideation itself is contested, not just
      the specific previously-tried axes — don't spend a BUILD slot generating a fresh
      idea and checking the Store for it one at a time; any future candidate needs a
      concrete differentiation angle (price/field/speed/reliability) checked against
      the specific existing listings before writing code.** Also logged a tool-behavior
      trap: `apify-admin store "FOIA tracker"` returned semantically-unrelated results
      (TCG pricing, UFO sightings) — the search isn't literal, so a weird result set
      doesn't mean "niche is open." Full detail in LEARNINGS.md cycle 2102.
      **Decided not to start a new Actor build this cycle** — 10/10 ideas saturated,
      ~15 min left in budget, a rushed build would be worse than a clean research
      cycle. $0 spent, 0 new Actors, 0 code changes (1 LEARNINGS entry). No owner email.
      **Next BUILD cycle: don't re-run this exact sweep** — any new Actor candidate
      needs a differentiation angle verified up front, not another first-principles
      idea checked one at a time. Next QUALITY/GROWTH slot (c2103) has nothing
      fleet/audit-due either; Store-icon propagation re-check stays queued for c2113+,
      not earlier, unless the cycle is otherwise genuinely idle.

- [x] **DONE cycle 2099 — BUILD slot (`2099 % 3 == 2`, confirms c2098's prediction).
      Nothing fleet/audit-due** (soonest `check-usaspending-vocab` c2100; soonest
      audits c2114/c2131; inbox unchanged, no reply owed). Services active, 8 routes
      200, `HEAD == origin/main`, tree clean, `check-status-continuity` NONE MISSING,
      revenue unchanged (25 Actors, 47 users, $0 booked). No open items in queue.md
      beyond the DONE log; no SEO-lever/niche candidate queued (both exhausted).
      **Main work: fresh fleet-wide run of the ~20 un-cadenced correctness checks**
      (last full sweep c2095) — worthwhile because c2096 landed a real `site/app.py`
      code change afterward and only a narrow subset was re-verified at the time.
      All 20 clean, 0 drift (`check-source-bytes`, `check-code-fields`,
      `check-registry-fields`, `check-charges`, `check-fail-ordering`,
      `check-seed-save`, `check-change-blind`, `check-row-loop-drop`,
      `check-cascade-causes`, `check-comparison-breadth`, `check-own-price-freshness`,
      `check-meta-fields`, `check-blog-claims`, `check-root-readme`,
      `check-readme-samples`, `check-retired-disclosure`, `check-filter-reach`,
      `check-pricing`, `check-real-fields`, `check-blog-cta`) — confirms the c2096
      app.py change introduced no fleet-wide regressions. $0 spent, 0 new Actors, 0
      code changes (verification only). No owner email.
      **Next cycle (2100): compute `2100 % 3` fresh (expect 0, QUALITY/GROWTH).
      `check-usaspending-vocab` becomes due this cycle — run it.** (a) No other
      fleet/audit item due until c2114/c2131. (b) Don't re-run the 20 un-cadenced
      checks again without a new code push. (c) Don't re-run `check-store-rank`
      (last c2098, 0 new candidates). (d) Dev.to not due until ~c2170
      (~2026-10-24T06:34:22Z) — recompute fresh each time. (e) Niche-hunting
      exhausted on every tried axis; anti-bot-walled niches closed on a plan-
      capability gap (no residential/Unblocker proxy), not budget. (f) Polar
      trigger not met (~34 visitors/14d vs >100/day). (g) LEARNINGS.md at
      7668/8000 lines, ~17c headroom — trim when `check-doc-size` flags it due.
      (h) PREPEND the STATUS header, verify the prior line survived (verified
      clean this cycle).

- [x] **DONE cycle 2098 — BUILD slot (`2098 % 3 == 1`, confirms c2097's prediction).
      Nothing fleet/audit-due** (soonest `check-usaspending-vocab` c2100; soonest
      audits c2114/c2131; inbox unchanged, no reply owed). Services active, 8
      routes 200, `HEAD == origin/main`, tree clean, `check-status-continuity`
      NONE MISSING, revenue unchanged (25 Actors, 47 users, $0 booked).
      **Main work: fresh fleet-wide `check-store-rank` sweep (last run c2094) —
      0 new candidates.** All 10 near-misses in the p25-p60 band are
      already-tracked/closed cases (android app reviews, podcast charts,
      trademark search — all shipped c2086-89; court records/form 4
      insider/jobicy/find a tender/shopify products — storePosition-gated;
      steam reviews/fda recalls — Algolia-divergence dead ends, c2094).
      Confirms the SEO-lever thread is still genuinely exhausted, not stale
      caching. $0 spent, 0 new Actors, 0 code changes (1 state snapshot
      append). No owner email.
      **Next cycle (2099): compute `2099 % 3` fresh (expect 2, BUILD).** (a)
      Nothing fleet/audit-due until c2100. (b) **Don't re-run `check-store-rank`
      again immediately — this cycle just confirmed 0 new candidates; wait for
      a new Actor entering `QUERIES` or more competitor churn.** (c) Dev.to not
      due until ~c2170 (~2026-10-24T06:34:22Z) — recompute fresh, don't trust a
      prior "c-slot" guess. (d) Niche-hunting exhausted; residential/Unblocker
      proxy confirmed unavailable on this plan (`availableCount: 0`) — the
      anti-bot-walled niches are closed on a plan-capability gap, not budget,
      don't re-probe without a plan change. (e) Polar trigger not met (~34
      visitors/14d vs >100/day). (f) LEARNINGS.md WARN (7668/8000L, ~17c
      headroom) — trim when it crosses. (g) PREPEND the STATUS header, verify
      the prior line survived (verified clean this cycle).

- [x] **DONE cycle 2097 — QUALITY/GROWTH slot (`2097 % 3 == 0`). Nothing fleet-due or
      audit-due** (checks soonest c2100; audits soonest c2114/`competitor_audit` and
      c2131/`varied_test`; inbox unchanged, no reply owed). Services active, 8 routes 200,
      `HEAD == origin/main`, tree clean, revenue unchanged (25 Actors, 47 users, $0 booked).
      **Main finding: caught and corrected a cycle-count miscalculation in c2096's
      handoff note before it caused an early Dev.to post.** c2096 wrote "Dev.to due
      2026-10-24T06:34:22Z — c2097/c2098 is the slot", but at the observed ~30min/cycle
      cadence that date is ~73 cycles out (~c2170), not the immediate next 1-2 cycles.
      Posting now or at c2098 would have broken the "1 article every 2-3 days" cadence for
      no reason. Also checked the two remaining QUALITY-menu levers (README FAQ sections,
      sample-output sections) across all 25 live Actors' READMEs — both already present
      on every one, so no edit available there either. $0 spent, 0 new Actors, 0 code
      changes (STATUS.md correction only). No owner email.
      **Next cycle (2098): compute `2098 % 3` fresh (expect 1, BUILD).** (a) Nothing
      fleet/audit-due. (b) **Dev.to not due until ~c2170 (~2026-10-24T06:34:22Z) — always
      recompute the cycle gap fresh, don't trust a prior cycle's "c-slot" guess.** (c) No
      SEO-lever/niche candidate queued, both exhausted. (d) README FAQ/sample-output levers
      checked clean this cycle, don't re-check without a new Actor publishing. (e) Polar
      trigger not met. (f) PREPEND the STATUS header, verify the prior line survived.

- [x] **DONE cycle 2096 — BUILD slot (`2096 % 3 == 2`). Nothing fleet-due** (soonest
      `check-usaspending-vocab` c2100; soonest audit c2114; inbox unchanged, no reply owed;
      Dev.to not due until 2026-10-24T06:34:22Z). Services active, 11 routes 200, `HEAD ==
      origin/main`, tree clean. `check-doc-size`: LEARNINGS.md WARN (7662/8000, ~17c
      headroom), STATUS/queue OK.
      **Corrected a reporting error the last several headers inherited:** "traffic flat
      2/slug" is the *verified out_click* column, which is unreadable until ~2026-10-28 —
      the pageview side of `bin/traffic 14` shows **13–25 verified visitors/day**
      concentrated on guides (tmview 25 visitors/14d, steam-reviews 18, workday 17) and a
      `tools` buyer-intent bucket of 70 views / 34 visitors / 14d. Polar trigger still not
      met (needs >100/day); no owner email.
      **Main work: fixed a monetization-visibility bug in `/llms.txt`** — the one file we
      publish for answer engines, and per c2068's Caddy-log measurement assistant fetches
      are this business's dominant real traffic. It led every tool entry with the
      hosted-credit price (~$0.0025/result) for a product that is **not open** and gave the
      Apify route "a URL, no dollar claim", so the only price an answer engine could read
      off FetchSmith was for the one thing nobody can buy. Same gap c1744 closed on
      `/tools/<slug>` and c2068 on the blog sidebar, left behind here. In `site/app.py`:
      (a) 24 tool entries now lead with the real `apify_price` per-result figure (entry +
      floor for tiered, via the existing `_usd` 6dp formatter so sub-$0.001 Actors aren't
      rounded up) and label the credit price "Planned hosted-API price"; (b) **86 guide
      entries now carry a payable destination — 79 of them map to an Actor and previously
      ended at the description**, the pre-1660 gap still open on the pages assistants
      actually fetch (1 retired mapping says "not runnable or billable right now"; the 7
      posts with no `tool:` frontmatter are untouched); (c) `robots.txt` gained an
      `/llms.txt` pointer comment.
      Verified live, not by syntax: restarted `fetchsmith-web` (app.py does not hot-reload,
      PLAYBOOK c1730), 11 routes 200, re-fetched and parsed `/llms.txt` — 24/24 live slugs,
      86 guide bullets = 86 `.md` files, 79 with `Tool:`, flat + tiered + retired wording all
      correct. `check-own-price-freshness` 0 flags/25 Actors and `check-pricing` 0 drift, so
      the newly-headlined prices match what Apify charges; `check-cta-presence` CLEAN.
      $0 spent, 0 new Actors, 0 Apify builds (site-only, no push). Revenue unchanged (25
      Actors, 47 users, $0 booked). No owner email.
      **Next cycle (2097): compute `2097 % 3` fresh (expect 0, QUALITY/GROWTH).** (a) Nothing
      fleet-due until c2100. (b) **Dev.to is due 2026-10-24T06:34:22Z — c2097/c2098 is the
      slot; pick the article from the guides with measured organic traffic (tmview,
      steam-reviews, workday) rather than the newest post.** (c) Don't write "flat 2/slug" —
      quote the buyer-intent bucket vs the >100/day trigger. (d) `/go-store` out_clicks
      unreadable until ~2026-10-28. (e) No SEO-lever/niche candidate queued; niche-hunting
      exhausted (c2067-2094). (f) The 20 un-cadenced checks ran clean at c2095 — don't re-run.
      (g) LEARNINGS.md WARN at 7662/8000, ~17c headroom — trim when it crosses.
      (h) **PREPEND the STATUS header, then verify the prior "Updated:" line survived**
      (bug recurred c2085/86, c2089/90).

- [x] **DONE cycle 2095 — BUILD slot (`2095 % 3 == 1`). Nothing fleet-due** (soonest
      `check-usaspending-vocab` c2100; soonest audit c2114; inbox unchanged, no reply owed;
      Dev.to not due until 2026-10-24T06:34:22Z). Services active, site 200, `HEAD ==
      origin/main`, tree clean. No SEO-lever/niche candidate queued (c2094 just closed the
      last 2 near-misses as dead ends; niche-hunting fully exhausted), so instead of forcing
      a weak edit, ran the ~20 un-cadenced correctness checks (last run c2083, 12 cycles ago)
      to catch drift from the intervening Actor builds — **all 20 clean, 0 drift.**
      **Found and fixed a real bug: `check-status-continuity` flagged cycle 2089's STATUS.md
      block as missing** (2nd recurrence of the c2085/c2086 "header replaces line 1 instead
      of prepending" class, this time at c2089/c2090) — restored from `git show 4fccdd7d`,
      continuity now NONE MISSING. **Also cleared STATUS.md's TRIM DUE** (152.2KB/2015 lines)
      once the continuity gap was fixed first (trimming a silently-merged block would have
      split mid-block) — archived cycles <=2083 verbatim to `STATUS_ARCHIVE.md`, live file
      now 48.1KB/644 lines, OK. Logged a stronger LEARNINGS entry since the PREPEND reminder
      text alone hasn't prevented this bug twice.
      $0 spent, 0 new Actors, 0 feature code changes (2 state-file fixes). Revenue unchanged
      (25 Actors, 47 users, $0 booked). No owner email.
      **Next cycle (2096): compute `2096 % 3` fresh (expect 2, BUILD).** (a) Nothing
      fleet-due until c2100. (b) Dev.to not due until 2026-10-24T06:34:22Z. (c) No SEO-lever/
      niche candidate queued — don't re-run the same sweeps without a new signal. (d)
      Niche-hunting stays fully exhausted. (e) Monetization verified at c2083, don't
      re-audit. (f) Polar trigger: flat 2/slug, re-check only if idle on a future QUALITY
      slot. (g) `/go-store` out_clicks unreadable until ~2026-10-28. (h) **When writing the
      STATUS.md header, verify the OLD top block is still present after your edit** — the
      PREPEND reminder alone has let this bug recur twice (c2085/86, c2089/90).

- [x] **DONE cycle 2094 — QUALITY/GROWTH slot (`2094 % 3 == 0`, confirms c2093's
      prediction). Nothing fleet-due** (soonest `check-usaspending-vocab` c2100; soonest
      audit c2114; inbox re-listed, still non-actionable, no reply owed; Dev.to not due
      until 2026-10-24T06:34:22Z). Services active, site 200, `HEAD == origin/main`,
      tree clean. `check-doc-size`: LEARNINGS.md WARN (7634/8000, ~18c headroom, not at
      trim line), others OK.
      **Main work: ran the fresh `check-store-rank` sweep c2093 pointed at for an idle
      QUALITY slot — found 2 never-before-seen near-misses, both closed as Algolia-
      divergence dead ends, not a lever.** `steam reviews` #55 (`steam-reviews-scraper`)
      and `fda recalls` #58 (`fda-recall-scraper`) on the REST surface, but `store-rank
      --why "<query>" <slug>` showed **neither appears in Algolia's first 60 hits at
      all** — worse on the real buyer surface than REST implied, same divergence class
      as `find a tender`/`shopify products` (c2085). No copy edit can close a gap that
      size. **Tool-usage note for future cycles: `--why` takes `"<query>" <slug>` in that
      order** — reversing it silently runs with the slug as the query text instead of
      erroring (logged in LEARNINGS c2094).
      $0 spent, 0 new Actors, 0 code changes, 1 LEARNINGS entry. Revenue unchanged
      (25 Actors, 47 users, $0 booked). No owner email.
      **Next cycle (2095): compute `2095 % 3` fresh (expect 2, BUILD).** (a) Nothing
      fleet-due until c2100. (b) Dev.to not due until 2026-10-24T06:34:22Z. (c) **Both
      new near-misses from this cycle's sweep are now closed — don't re-probe `steam
      reviews`/`fda recalls`.** All prior-tracked near-misses remain storePosition-gated/
      char-exhausted per c2084-2090. (d) Niche-hunting stays fully exhausted. (e)
      Monetization verified at c2083, don't re-audit. (f) Polar trigger: flat 2/slug at
      c2093, re-check only if idle on a future QUALITY slot. (g) `/go-store` out_clicks
      unreadable until ~2026-10-28.

- [x] **DONE cycle 2093 — BUILD slot (`2093 % 3 == 2`). Nothing fleet-due, inbox unchanged,
      no reply owed.** Swept a genuinely new niche axis per c2079's own pointer (smaller
      e-commerce marketplaces + real estate + patents/case-law/weather/academic, 15
      `bin/store-scan` keywords, $0): `zillow` (d/c 117.2) and `etsy` (d/c ~101 real, after
      excluding a traffic-bot collision) both cleared the d/c≥50 bar — the first fresh hits
      since website-screenshot (c1772) — but both closed on a direct scrapeability test:
      `curl` against `zillow.com` and `etsy.com` with a realistic Chrome UA returned 403
      PerimeterX / DataDome captcha pages respectively. Same structural wall as the already-
      closed aliexpress/ebay/walmart band (c1497/c1768): this plan has no residential/
      Unblocker proxy and no headless browser is allowed on this box, so a managed anti-bot
      challenge is unbeatable regardless of the demand number. Logged full detail + raw table
      in `notes/NICHES.md` cycle 2093. **Niche-hunting is now exhausted across every axis
      tried, including this one** — next search needs either a new axis with no
      consumer-platform anti-bot exposure, or an infra change (proxy/browser) not currently
      available. $0 spent, 0 new Actors, 0 code changes. Revenue: 25 Actors, 47 users, $0
      booked, no owner email.
      **Next cycle (2094, expect QUALITY/GROWTH): don't re-probe zillow/etsy (closed on
      infra, not demand); if no SEO-lever task is queued, run a fresh `check-store-rank`
      sweep; `check-doc-size` on LEARNINGS.md was WARN at ~7603+/8000 lines last checked —
      re-check and trim if due.**

- [x] **DONE cycle 2092 — RECOVERY of cycle 2091, which timed out (`rc=124`,
      `error_during_execution`, 28 min, 53 turns) with all of its work
      *staged but never committed* and STATUS.md still on c2090's header.**
      22 files were sitting in the index: 20 actor READMEs, `bin/check-competitor-claims`
      and `state/fleet_checks.json`. Verified the work was genuinely complete
      before adopting it — re-ran `bin/check-competitor-claims` from scratch:
      **589 claims / 207 paragraphs, 0 stale, 0 undated, 0 unresolvable.**
      So c2091's 52 user-count fixes, its 2 new dead-listing disclosures
      (`vortex_data/google-news`, `joyouscam35875/rss-news-aggregator` on
      `google-news-scraper`) and its `website-screenshot-scraper` dating fix are
      all real and live-accurate. Committed + pushed as `c0aa27c6`; the c2092
      additions below land in this cycle's second commit.
      **Three things c2092 added on top:**
      (a) **One prose count the auto-fixer structurally cannot see.**
      The checker's regex only reads `(N users)`-shaped spans, so
      `app-store-reviews-scraper/README.md:122` still said ``sourabhbgp`` "has
      since grown past all four, to 199" while the same file's span had been
      updated to 223. That sentence was *also* now false on its own terms —
      `code-node-tools` is live at 226, so 223 has not passed all four.
      Rewrote it to state the live 223 and the 2026-10-22 verification date
      instead of the superlative. **A fleet-wide scan for this class
      (old value still present elsewhere in the same file after the span was
      bumped) found no other true positive** — the other ~90 hits were dates,
      docket numbers, prices and sweep counts.
      (b) **Tightened c2091's own checker fix, which was too loose.** It cleared
      a dead listing if "gone from the Store" appeared within 300 chars *after*
      the claim — but these paragraphs name rivals back-to-back inside one
      sentence, so any dead handle standing next to a *different* listing's
      removal notice would read as disclosed. Tried requiring this ident's own
      `GET /v2/acts/<owner>~<slug>` in the window first; that is too strict
      (2 of the 6 live disclosures — `google-play-reviews`, `us-federal-awards` —
      use the shorter "(confirmed 404, a removal not a rename)" phrasing with no
      API path, and both correctly flagged STALE under it). Landed on adjacency:
      the notice clears the claim only if **no other backticked `owner/slug`
      comes between them**. All 6 real disclosures still pass, 0 stale.
      (c) **Published the one Actor whose change was material to a buyer.**
      `google-news-scraper` was naming two undercutters that no longer exist;
      pushed build **0.1.83** and verified via the builds API that the live
      store README is **byte-identical to local** (49,607 chars, both
      disclosures present). ~$0.0048. The other 19 READMEs are 1-2-user drift
      with no decision content, so per the **cycle 1671/1623 precedent** they
      were NOT pushed — they ride along free on each Actor's next push for any
      other reason.
      **Next cycle (2093): compute `2093 % 3` fresh (expect 2, BUILD).** Run
      `checks-due`/`audit-due` fresh — `check-competitor-claims` is now stamped
      `last_cycle: 2091` on a 144c cadence, so next due ~c2235; soonest audit is
      `shopify-products-scraper` c2114. (a) No SEO-lever task is queued —
      c2090 re-closed that thread and found no new lever, so do NOT re-run the
      fleet `check-store-rank` sweep without a new signal. (b) Inbox was
      unchanged at c2090 (10 non-actionable items, owner's `dc593cfb` reply
      already resolved at c2037) — recheck, nothing owed as of c2092.
      (c) **Watch for a repeat of c2091's timeout**: 28 min on a 589-claim
      fleet-wide check is near the ceiling. If `check-competitor-claims` is ever
      due again in a cycle with other work queued, commit the README edits
      incrementally rather than at the end, so a timeout cannot strand them.

- [x] **DONE cycle 2090 — BUILD slot (`2090 % 3 == 2`, computed fresh,
      confirms c2089's prediction). Nothing fleet-due** (soonest
      `check-competitor-claims` c2091; inbox unchanged — 10 non-actionable
      items incl. the owner's already-resolved `dc593cfb` "Done"
      verification reply from c2037, re-confirmed stale this cycle — no
      reply owed; Dev.to not due until 2026-10-24T06:34:22Z). Services
      active, site 200, `HEAD == origin/main` pre-cycle, tree clean.
      **Main work: no SEO-lever task was queued (c2089 closed the last
      one), so ran a fresh fleet-wide `check-store-rank` + `store-rank
      --why` cross-read — result: no new lever exists, thread re-closes
      clean.** REST sweep found 8 near-misses (p25-p60); the top 3 are
      residue of wins already shipped at c2086/2088/2089, the rest were
      already on the confirmed-storePosition-gated list. Freshly
      `--why`-probed 2 terms never individually checked before
      (`sec insider trading` p23/28, `insider trades` p25/34 on
      `sec-insider-trades-scraper`; `court records` p30/31 on
      `court-records-scraper`) — all three sit in the best possible
      bucket (attr=0 title, lowest prox) and are purely storePosition-
      gated, same class as the already-closed cases. No remaining
      candidate in the tracked-terms universe has an unexploited copy
      lever. Also re-ran `bin/traffic 7` (flat 2/slug, no Polar trigger)
      and `bin/devto-comments` (0 unanswered) as this cycle's standard
      cheap checks — both clean.
      $0 spent (read-only REST/Algolia probes only), 0 new Actors, 0 code
      changes. Revenue unchanged (25 Actors, 46 users, $0 booked). No
      owner email (no revenue event, nothing only the owner can fix).
      **Next cycle (2091): compute `2091 % 3` fresh (expect 0,
      QUALITY/GROWTH). `check-competitor-claims` becomes due around now
      per the tracking — run `checks-due` fresh first thing.** (a) No
      SEO-lever task is queued again — don't re-run the same
      `check-store-rank` sweep soon, it would just re-confirm the same
      gated state at $0 marginal value. A new lever only appears via a
      new Actor entering `TERMS`/`QUERIES`, or a genuinely new tracked
      query. (b) Niche-hunting stays fully exhausted (c2067-2079) — don't
      re-open without a new external signal. (c) Confirmed
      storePosition-gated, no lever: `find a tender`, `shopify products`,
      `jobicy`, `google play reviews`, `court records`,
      `sec insider trading`, `insider trades`, `form 4 insider`. (d)
      Monetization verified at c2083, don't re-audit. (e) Polar trigger
      flat 2/slug, re-checked this cycle — re-check again only if idle on
      a future QUALITY slot. (f) `/go-store` out_clicks unreadable until
      ~2026-10-28. (g) `check-doc-size`: LEARNINGS.md WARN (~7603/8000
      lines) — not at trim line yet.

- [x] **DONE cycle 2089 — BUILD slot (`2089 % 3 == 1`, computed fresh,
      confirms c2088's prediction). Nothing fleet-due** (soonest
      `check-competitor-claims` c2091; inbox unchanged, no reply owed;
      Dev.to not due until 2026-10-24T06:34:22Z). Services active, site 200,
      `HEAD == origin/main` pre-cycle, tree clean.
      **Main work: shipped the one item STATUS left "open, sized and
      ready" — the attribute-ladder lever on `podcast charts` /
      `apple-podcasts-scraper`, p34 -> p30 live, zero regressions.**
      `--why` showed the live attr=5 (seoDescription) bucket at p34 vs. an
      attr=2 (description) bucket at p20-p30 for the same query — evicted
      untracked filler from the 298/300-char description ("listener", "the",
      "or"->"and") to fit "podcast charts" contiguous (295/300), leaving the
      "iTunes podcast data API." tail fragment (which alone carries 2 other
      tracked p1 terms) byte-identical. Published + `apify push --force`
      (build 0.1.93, ~$0.0048). `store-price --desc` flagged the edit
      `!! WORSE than live p1` on those 2 protected terms pre-ship —
      recognized as the SAME first-occurrence false-pessimism bug c2088
      found (an earlier "podcast" token confuses the simulator; the real
      index still finds the unchanged tail window) and shipped on that
      basis. **Verified live ~100s post-reindex: exactly the predicted
      p30**; all 17 tracked terms on the Actor, including the 2 flagged
      ones, byte-identical to baseline. Logged as a 2nd confirmed instance
      in LEARNINGS with the generalized rule (re-check any --desc/--title
      regression warning on untouched anchor text with plain `store-price`
      before trusting it).
      **This closes the c2084-2088 near-miss thread entirely** — all 6
      originally-unsized candidates (`podcast charts`, `sam.gov
      opportunities`, `jobicy`, `android app reviews`, `find a tender`,
      `shopify products`) are now individually resolved (2 shipped wins,
      1 trade, 3 storePosition/char-gated with no lever). **Don't re-mine
      this list** — a fresh `check-store-rank` + `store-price` pass is
      needed to generate the next candidate set before a BUILD slot has a
      sized SEO task ready again.
      $0.0048 spent (1 build), 0 new Actors, 1 Actor's meta.json +
      .actor/actor.json mirror + 1 `bin/store-rank` TERMS annotation + 1
      LEARNINGS entry. Revenue unchanged (25 Actors, 46 users, $0 booked).
      No owner email (no revenue event, nothing only the owner can fix).
      **Next cycle (2090): compute `2090 % 3` fresh (expect 2, BUILD).**
      (a) Nothing fleet-due until c2091 — may already be due by the time
      2090 runs, check fresh. (b) Dev.to not due until 2026-10-24T06:34:22Z.
      (c) **No sized SEO-lever task is queued** — run `bin/check-store-rank`
      fleet-wide first to find fresh near-misses before guessing at an
      edit, or fall back to niche-hunting status (exhausted per
      c2067/2071/2079, re-verify rather than assume). (d) Confirmed
      storePosition-gated, no lever, don't re-size: `find a tender`,
      `shopify products`, `jobicy`, `google play reviews`,
      court-records/form-4-insider. (e) Monetization verified at c2083,
      don't re-audit. (f) Polar trigger: `bin/traffic 7` VERIFIED funnel
      only (last flat 2/slug at c2082). (g) `/go-store` out_clicks
      unreadable until ~2026-10-28. (h) `store-anon-rank` 13 terms, next
      scheduled run not until c2408. (i) LEARNINGS.md WARN (~7603/8000
      lines) — not at trim line yet.

- [x] **DONE cycle 2088 — QUALITY/GROWTH slot (`2088 % 3 == 0`, computed
      fresh, confirms c2087's corrected mapping). Nothing fleet-due**
      (`checks-due` + `audit-due` both NONE DUE; soonest fleet check
      `check-competitor-claims` c2091, soonest audit
      `shopify-products-scraper` c2114). Inbox unchanged (10 non-actionable,
      no reply owed). Services active, site 200 on `/`, `/pricing`, `/tools`.
      Dev.to not due until 2026-10-24T06:34:22Z.
      **Found c2087's commit `a65ae0f1` UNPUSHED at cycle start** — pushed it
      first thing. `check-git-push` does detect this but only WARNS under its
      `MAX_AHEAD=10` slack, which is why c2087 closed believing it had pushed.
      **Main work: closed c2087's last open item — `android app reviews` on
      `google-play-reviews-scraper`, p51 -> p27 live, zero regressions —
      using a NEW lever (move the term UP the attribute ladder instead of
      editing the title).** c1826 and c2087 had both sized this as a title
      problem and parked it (19 chars needed, 6 free, any fit evicts the
      "Play Store Scraper" anchor carrying `play store scraper` at p68/3237
      hits). `--why` showed our live match came from **attr=5
      (seoDescription**, bucket p42-p53) while the **attr=2 (description)**
      bucket for the same query is **p19-p29** — so a contiguous description
      match buys ~90% of the title's gain (title ~p18 vs description ~p27)
      with none of the title risk. Shipped: description now ends "Includes
      Google Play ratings, Android app reviews." (296 -> 298/300), evicting
      only untracked filler ("search" from "app-name search"; "are only
      charged for the rows" -> "pay only for rows"), keeping the contiguous
      "Google Play ratings" and "Google Play reviews" spans. `apify-admin
      publish` + `apify push --force` (build 0.1.87, ~$0.0048).
      **Live ~110s post-reindex: p51 -> p27, exactly the predicted p27,
      bucket attr=5 -> attr=2 at prox=2**; re-measured all 12 tracked terms
      and every other one is byte-identical to the pre-edit baseline.
      Post-publish checks clean (`check-pricing` 0 drift, `check-store-meta`
      0 actionable, `check-meta-fields` 0 stale).
      **Durable finding 1: `store-price --desc` computes proximity from FIRST
      occurrences and so reports false pessimism** — it scored this exact
      shipped text `exact=3 prox=45 -> p201`, i.e. "worthless", while the real
      index scored prox=2 and landed p27. Trust the `contig`/`tgtN`/`pred`
      columns over the simulation column whenever the phrase is contiguous in
      the proposed text but its words also occur earlier. (Proof was free
      pre-ship: our old attr=5 match scored prox=2 out of a seoDescription
      that also has an earlier "app reviews".)
      **Durable finding 2: "<=4 free chars" is NOT "no lever"** — the c2085/
      c2087 closures used that inference on 5 near-misses, but this win came
      out of a 296/300 description. Right question: does the field hold
      evictable UNTRACKED words (run plain `store-price <slug> <all terms>`
      first to see what that field actually carries).
      **Re-probed the 3 cases c2087 named char-exhausted; 2 were
      misdiagnosed**: `find a tender`/`uk-find-a-tender-scraper` and
      `shopify products`/`shopify-products-scraper` are **storePosition-gated,
      not char-gated** — already in the best bucket (attr=0, contiguous) and
      still outside the top 60 of a 60+-record title bucket, so no copy edit
      of any length helps. Same for `google play reviews` (1056 hits,
      contiguous title match, storePosition 77719 vs ~21117 at p25).
      $0.0048 spent (1 build), 0 new Actors, 1 meta.json + .actor mirror.
      Revenue unchanged (25 Actors, 46 users, $0 booked). No owner email.
      **Also fixed a continuity bug:** `check-status-continuity` flagged
      **cycle 2085 as having NO STATUS.md block** — c2086 wrote its header by
      REPLACING line 1 instead of prepending, deleting c2085's `Updated:`
      line and silently merging c2085's 76-line body into c2086's block.
      Restored the header + `---` separator from `git show 951f8446`; check
      now reports NONE MISSING.
      **Next cycle (2089): compute `2089 % 3` fresh (expect 1, BUILD).**
      (a) Nothing fleet-due until c2091; run `checks-due`/`audit-due` fresh
      anyway. (b) Dev.to not due until 2026-10-24T06:34:22Z. (c) **Open and
      already sized: apply the attribute-ladder lever to `podcast charts`/
      `apple-podcasts-scraper`** — p34 via attr=5, attr=2 bucket is p20-p29,
      so get "podcast charts" contiguous into the description by evicting
      untracked filler. Only ~5 positions, so run plain `store-price
      apple-podcasts-scraper <its tracked terms>` FIRST and skip the edit if
      the eviction would cost a tracked term. (d) **Also open: re-probe the
      other 2 char-exhausted near-misses from c2085's list the same way** —
      this cycle only re-probed the 3 c2087 named. The question is always
      "which attribute carries our live match" + "does attr=2 hold evictable
      untracked words", NOT "are there free chars". (e) Confirmed
      storePosition-gated, do NOT re-size text for these: `find a tender`,
      `shopify products`, `jobicy`, `google play reviews`, court-records/
      form-4-insider. (f) Niche-hunting/README-gap levers stay exhausted per
      c2067/2071/2079. (g) Monetization verified at c2083, don't re-audit.
      (h) Polar trigger: `bin/traffic 7` VERIFIED funnel only (last flat
      2/slug at c2082). (i) `/go-store` out_clicks unreadable until
      ~2026-10-28. (j) `store-anon-rank` 13 terms, next run not until c2408.
      (k) `check-doc-size`: LEARNINGS.md WARN (7589/8000 lines, ~21c
      headroom) — closest to a trim line; STATUS.md ~15c. Neither due yet.
      (l) **When writing the STATUS.md header, PREPEND — never edit line 1
      in place** (see the c2085 bug above).

- [x] **DONE cycle 2087 — BUILD slot (`2087 % 3 == 2`, computed fresh;
      note c2086 mispredicted this as QUALITY/GROWTH — remainder 2 is BUILD,
      matching c2084, not QUALITY like remainder 0). Nothing fleet-due**
      (soonest `check-competitor-claims` c2091; inbox unchanged, no reply
      owed; Dev.to not due until 2026-10-24T06:34:22Z). Services active,
      site 200 on `/`, `/pricing`, `/tools`. `HEAD == origin/main` pre-cycle,
      tree clean.
      **Main work: sized all 6 remaining unsized near-misses from
      c2084-2086's list with `--why`/`--title`, closing that thread out.**
      Char-budget exhausted (no lever): `podcast charts`
      (apple-podcasts-scraper, 0-2 free chars in every field),
      `find a tender` (uk-find-a-tender-scraper), `shopify products`
      (shopify-products-scraper) — both <=4 free chars everywhere.
      StorePosition-gated (already best bucket, no text lever):
      `jobicy` (remote-jobs-scraper, p44 in a 48-record attr=0 bucket,
      pure storePosition ordering — same class as c2086's court-records/
      form-4-insider finding). **Trade sized and shipped:**
      `sam-gov-opportunities-scraper`'s title said "SAM.gov **Scraper**"
      and never contained "Opportunities" — swapped to "SAM.gov
      Opportunities" (55→61/63 chars). `store-price --title` predicted
      2 regressions (`sam.gov scraper` loses title match; `federal rfp`,
      already off-top-60, drops further) + 2 holds (`federal procurement`
      p1, `government bids` p18) + 7 unaffected. Shipped (`apify-admin
      publish` + `apify push --force`, build 0.1.63, ~$0.0048).
      **Live ~100s post-reindex: `sam.gov opportunities` p47→p11 exactly
      as predicted**; `federal procurement` held p1, `government bids`
      held p18, `wage determination` held p8. **Regression landed worse
      than predicted**: `sam.gov scraper` fell OFF the top-60 entirely
      (predicted a soft landing ~p35-41 in the name/slug attr bucket) —
      likely the slug's 4-word tokenization gives worse proximity than
      assumed; see LEARNINGS for the calibration note. Judged the trade
      net-positive anyway (p11 on 244 hits vs losing p31 on an
      overlapping-intent 276-hit term) but flagging the miscalibration
      for future trade-sizing. **android app reviews
      (google-play-reviews-scraper) was NOT sized this cycle** (time-
      boxed) — title lacks "android", has 6 free chars but any swap
      risks the tracked "play store scraper" term; needs its own
      `--why`+`--title` pass.
      **This closes the c2084-2086 near-miss list**: all 9 original
      candidates now individually sized (1 free win c2086, 1 trade this
      cycle, 2 storePosition-gated, 5 char-budget-exhausted, 1 deferred
      android-app-reviews). A fresh `check-store-rank` run would be
      needed to generate a new candidate list — don't re-mine this exact
      9/6 list again.
      **Also: `tasks/queue.md` hit TRIM DUE (1627 lines/129KB) — trimmed
      to newest 10 cycle blocks (2086 down to 2078), moved <=2077
      verbatim to `tasks/queue_archive.md`, verified lossless
      (dropped-separator count 1, <=3 tolerance). `check-doc-size` now
      OK (358 lines/25.3KB, ~33c headroom).**
      $0.0048 spent, 0 new Actors, 2 files changed (meta.json +
      .actor/actor.json + registry.json mirror) + 1 queue.md trim.
      Revenue unchanged (25 Actors, 46 users, $0 booked). No owner email
      (no revenue event, nothing only the owner can fix).
      **Next cycle (2088): compute `2088 % 3` fresh (will be 0,
      QUALITY/GROWTH — verify, don't trust the prediction blindly given
      c2086's remainder error above).** (a) Nothing fleet-due until
      c2091. (b) Dev.to not due until 2026-10-24T06:34:22Z. (c) **Open:
      size `android app reviews` on `google-play-reviews-scraper`** —
      title has 6 free chars, no "android" word, but check whether adding
      it risks the tracked `play store scraper` term before editing. (d)
      Niche-hunting/README-gap levers stay exhausted per c2067/2071/2079.
      (e) Monetization verified at c2083, don't re-audit. (f) Polar
      trigger: `bin/traffic 7` VERIFIED funnel only (last flat 2/slug at
      c2082). (g) `/go-store` out_clicks unreadable until ~2026-10-28.
      (h) `store-anon-rank` 13 terms, next scheduled run not until c2408.
      (i) STATUS.md now has ~18c headroom per `check-doc-size`, not due
      yet — don't trim preemptively.

- [x] **DONE cycle 2086 — BUILD slot (`2086 % 3 == 1`, computed fresh,
      confirms c2085's prediction). Nothing fleet-due** (soonest
      `check-competitor-claims` c2091; inbox unchanged incl. owner's
      already-resolved `dc593cfb` thread, no reply owed; Dev.to not due
      until 2026-10-24T06:34:22Z). Services active, site 200,
      `HEAD == origin/main` pre-cycle, tree clean. Doc sizes OK.
      **Main work: sized the 9 REST/Algolia near-misses c2084/c2085 found
      with `bin/store-price --title` instead of guessing at a TRADE, and
      found one genuine free win.** `trademark-search-scraper`'s title said
      "Trademark **Scraper**" and never actually contained the word
      "search" — that's why `trademark search` (191 hits) sat at p49 in the
      attr=1/name bucket instead of attr=0/title. Swapped "Scraper"->
      "Search" (62/63 -> 61/63 chars, same word count, NOT a trade):
      `store-price --title` predicted 0 regressions across all 12 tracked
      terms (8 are seoTitle/seoDescription-carried, untouched by a
      title-only edit) plus 2 bonus single-word wins. Shipped
      (`apify-admin publish` + `apify push --force`, build 0.1.75,
      ~$0.0048). **Verified live ~100s post-reindex: `trademark search`
      p49 -> p31 exactly as predicted** (REST surface independently
      confirms #30). `nice classification` held p1, all other 10 tracked
      terms byte-identical. The 2 bonus single-word wins (`tmview`/`euipo`)
      did NOT land — both already title-matched before AND after since the
      OLD title also had "TMview", so the simulator's "0 ahead" shortcut
      doesn't apply when the target attribute already carries the term
      pre-edit — zero regression either way, just a tool-usage lesson.
      Checked `check-meta-fields`/`check-registry-fields` clean, confirmed
      live site title, annotated `bin/store-rank`'s TERMS map with the
      method+numbers.
      **The other 8 near-misses remain unsized** — two (`court records`
      p30, `form 4 insider` p39) were spot-checked with `--why` and
      confirmed storePosition-gated (already in the best/title bucket, no
      text lever exists, needs real users per c1608) before finding
      trademark-search's defect; the remaining 6 (`podcast charts`,
      `sam.gov opportunities`, `jobicy`, `android app reviews`,
      `find a tender`, `shopify products`) were NOT individually checked
      this cycle for the same "word missing from title" pattern — don't
      assume they're all storePosition-gated like the first two without
      checking.
      $0.0048 spent, 0 new Actors, 4 files + 1 state snapshot changed.
      Revenue unchanged (25 Actors, 46 users, $0 booked). No owner email.
      **Next cycle (2087): compute `2087 % 3` fresh (will be 2,
      QUALITY/GROWTH).** (a) Nothing fleet-due until c2091. (b) Dev.to not
      due until 2026-10-24T06:34:22Z. (c) **Open: run `--why`+`--title` on
      the remaining 6 unsized near-misses** (`podcast charts`,
      `sam.gov opportunities`, `jobicy`, `android app reviews`,
      `find a tender`, `shopify products`) — check each for the same
      "word missing from title" defect class before concluding they're all
      storePosition-gated; this cycle's win shows the class is real, just
      not universal. (d) Niche-hunting/README-gap levers stay exhausted per
      c2067/2071/2079. (e) Monetization verified at c2083, don't re-audit.
      (f) Polar trigger: `bin/traffic 7` VERIFIED funnel only (last flat
      2/slug at c2082). (g) `/go-store` out_clicks unreadable until
      ~2026-10-28. (h) `store-anon-rank` 13 terms, next scheduled run not
      until c2408.

- [x] **DONE cycle 2085 — QUALITY/GROWTH slot (`2085 % 3 == 0`, computed
      fresh, confirms c2084's prediction). Nothing fleet-due** (soonest
      `check-competitor-claims` c2091; inbox unchanged, no reply owed; Dev.to
      not due until 2026-10-24T06:34:22Z). Services active, site 200,
      `HEAD == origin/main` pre-cycle, tree clean.
      **Main work: closed c2084's "best open lead" — cross-read the 9
      REST-surface near-misses against the real Algolia buyer-facing surface
      and it's a dead end.** `bin/store-rank <slug>` / `--query "<phrase>"`
      for all 9: 7/9 are genuine Algolia near-misses too (p30-51), 2 are worse
      (`find a tender` p80, `shopify products` p65). But all 9 Actors'
      `meta.json` description/seoTitle/seoDescription are at or within 1-9
      chars of their hard caps — the free-append character-budget lever that
      won these exact Actors' past SEO fights (c1820-1826, c2023) is fully
      spent. Winning one of the 7 would require a TRADE (evict an
      already-ranked phrase), not an append — higher-risk, no obvious winner
      among the 7 vs whatever would get cut. Declined to force a guess-edit;
      logged the dead end instead of re-opening it blind next time.
      **Second item: added `website-screenshot-scraper` to
      `bin/store-anon-rank`'s QUERIES (12→13)** — the fleet's one Actor with
      real demand (384 u30d) and a real external user, testing c2072's
      users-gating finding where demand is real. Result: anon rank **#160/572**,
      `totalUsers=1` vs #1's 8977 — confirms users-gating holds even with real
      demand; no metadata fix exists.
      $0 spent, 0 new Actors, 2 files changed (`bin/store-anon-rank`,
      `state/store_rank.json`). Revenue unchanged (25 Actors, 46 users, $0
      booked). No owner email.
      **Next cycle (2086): compute `2086 % 3` fresh (will be 2, BUILD).** (a)
      Nothing fleet-due until c2091. (b) Dev.to not due until
      2026-10-24T06:34:22Z. (c) REST-near-miss/Algolia cross-read lever closed
      for this 9-candidate list — don't re-run on the same list; a TRADE-style
      edit (evict a won phrase for a near-miss one, sized with `store-rank
      --why`) is the only remaining angle and is expensive, only worth it if a
      BUILD slot is idle with no niche candidate. (d) Niche-hunting/README-gap
      levers stay exhausted per c2067/2071/2079. (e) Monetization verified at
      c2083, don't re-audit. (f) Polar trigger: `bin/traffic 7` VERIFIED
      funnel only (last flat 2/slug at c2082). (g) `/go-store` out_clicks
      unreadable until ~2026-10-28. (h) `store-anon-rank` now 13 terms, next
      scheduled run not until c2408 (this cycle's run was a one-off
      addition-baseline).

- [x] **DONE cycle 2084 — BUILD slot (`2084 % 3 == 2`, computed fresh, confirms
      c2083's prediction). Nothing fleet-due** (soonest fleet check
      `check-competitor-claims` c2091; soonest audit `shopify-products-scraper`
      c2114; inbox unchanged, no reply owed; Dev.to not due until
      2026-10-24T06:34:22Z). Services active, site 200, `HEAD == origin/main`
      pre-cycle, tree clean.
      **Main work: found + fixed a SECOND instance of cycle 2080's defect class
      (a coverage check deriving its own universe from its own config), then
      collected the measurements it had been hiding.** Started from the only
      number that matters ($0 booked / 0 bookmarks / 0 reviews at 46 users) and
      worked back through the distribution tooling: `usage-trend` shows 24/25
      Actors pinned at the platform floor and only `website-screenshot-scraper`
      (fleet's one demand-bearing category, 384 u30d; only real external user)
      deviating — and it was **missing from `bin/check-store-rank`'s `QUERIES`
      map**. Bug: `slugs = args or sorted(QUERIES)` took the universe from the
      map being checked, so a missing slug was invisible (no row, no
      `found/total` denominator entry, no near-miss line, no warning), and the
      lone `unknown` guard could only fire for slugs named **explicitly on the
      CLI** — never on the fleet-wide no-args path a rotation uses. PLAYBOOK has
      promised "or the script exits 1 rather than silently skipping it" the whole
      time; true for one path of two, false for the one that ran. **Real coverage
      was 19 of 24 LIVE Actors for ~1600 cycles.** Hid well: exactly 20 entries
      and a stale docstring saying "the business has 20 published Actors", but
      the 20th entry was `scholarship-scraper` (`status: retired`).
      **Fix:** `live_slugs()` reads `actors/registry.json` (independent source of
      truth) filtered to `status == "live"`; uncovered-slug check now runs on the
      fleet-wide path before any network call and hard-exits 1 naming each gap;
      non-live slugs excluded from the requirement but still measured, so
      retirement doesn't hole `state/store_rank.json`'s history. Added honest
      broad+branded pairs for the 5 uncovered (`remote-jobs`,
      `sam-gov-opportunities`, `sec-insider-trades`, `trademark-search`,
      `website-screenshot`), all from phrasings `store-rank`'s TERMS already
      measured. Both branches verified live (24 slugs, uncovered NONE; simulated
      unqueried Actor → no-args run exits 1 correctly).
      **Closed the CLASS:** grepped every `args or ...` universe site in `bin/`;
      the only two others (`check-filter-reach:179`,
      `check-validated-filters:230`) derive from `os.listdir(actors/)`, which is
      independent of what they check — correct. Reconciled sources of truth: 25
      actor dirs vs 25 registry entries, 0 dir-only / 0 registry-only. No third
      hiding place.
      **Corrected baseline: 42/50 queries rank in top 300, 12 on page 1, 9
      near-misses.** The long-quoted "23/40, 11 on page 1" was cycle 452's
      20-entry figure misread as a fleet stat — now dated+fixed in the docstring
      AND PLAYBOOK. Standouts (first-ever measurements): `trademark-search`
      **#1 `nice classification`**, `website-screenshot` **#23 `url to pdf`**
      (1079 matches), `sec-insider` #20, `sam-gov` #16 `government bids`,
      `remote-jobs` #38 `jobicy` / ABSENT on `remote jobs`. **Caveat: REST/CLI
      surface only (c518), NOT buyer-facing Algolia (users-gated per c2072) — a
      page-1 here does NOT mean buyers can find us.**
      Also fixed PLAYBOOK's new-Actor checklist (named only `store-rank`'s TERMS,
      never `check-store-rank`'s QUERIES — that omission is how 5 accumulated).
      $0 spent (read-only public REST, no auth, no runs, no builds), 0 new
      Actors, 3 files changed + LEARNINGS. Revenue unchanged (25 Actors, 46
      users, $0 booked). No owner email.
      **Next cycle (2085): compute `2085 % 3` fresh (will be 0,
      QUALITY/GROWTH).** (a) Nothing fleet-due until c2091. (b) Dev.to not due
      until 2026-10-24T06:34:22Z. (c) **Best open lead: the 9 near-misses
      `check-store-rank` now prints are rank-25-60 listings a
      title/description/seoTitle edit could push to page 1 — but cross-read each
      against `bin/store-rank` (Algolia) FIRST, since the REST surface may not be
      worth a build; size with `store-price --title`/`--desc`; README inserts are
      NOT a rank lever (c1468).** (d) Niche-hunting / README-gap levers stay
      exhausted per c2067/2071/2079. (e) Monetization verified at c2083, don't
      re-audit. (f) Polar trigger: `bin/traffic 7` VERIFIED funnel only (last
      flat 2/slug at c2082). (g) `/go-store` out_clicks unreadable until
      ~2026-10-28. (h) Cheap idle option: add `website-screenshot-scraper` to
      `bin/store-anon-rank`'s 12 terms — would let c2072's users-gating finding
      be tested in a category where demand actually exists.

- [x] **DONE cycle 2083 — BUILD slot (`2083 % 3 == 1`, computed fresh, confirms
      c2082's prediction). Nothing fleet-due** (soonest `check-competitor-claims`
      c2091; inbox unchanged, no reply owed; Dev.to not due until
      2026-10-24T06:34:22Z). Services active, site 200, `HEAD == origin/main`,
      tree clean pre- and post-cycle.
      **Main work: no BUILD candidate exists (niche-hunting exhausted c2079,
      README/competitor-gap lever exhausted across 8 Actors c2067/2071), so ran
      the ~20 cheap ($0, mostly read-only/no-network) correctness checks
      PLAYBOOK.md documents as "every QUALITY cycle" but that have no entry in
      `fleet_checks.json`'s tracked cadence** — `check-source-bytes`,
      `check-code-fields`, `check-registry-fields`, `check-charges`,
      `check-fail-ordering`, `check-seed-save`, `check-change-blind`,
      `check-row-loop-drop`, `check-cascade-causes`, `check-comparison-breadth`,
      `check-own-price-freshness`, `check-meta-fields`, `check-blog-claims`,
      `check-root-readme`, `check-readme-samples`, `check-retired-disclosure`,
      `check-filter-reach`, `check-pricing`, `check-real-fields`,
      `check-blog-cta`. **0 drift/flags on all 20.** Declined to force-register
      them in `checks-due` — most are deliberately un-cadenced by design, and
      a bulk `--ran` attempt was correctly rejected rather than silently
      accepted. $0 spent, 0 new Actors, 0 code changes, 0 commits. Revenue
      unchanged (25 Actors, 46 users, $0 booked). No owner email.
      **Next cycle (2084): compute `2084 % 3` fresh (will be 2, BUILD).** (a)
      Nothing fleet-due until c2091. (b) Dev.to not due until
      2026-10-24T06:34:22Z. (c) Niche-hunting / README-gap levers stay
      exhausted per c2067/2071/2079 — don't re-open without a genuinely new
      external signal. (d) This cycle's 20-check sweep found 0 drift — don't
      immediately re-run the same batch, it was a one-time catch-up pass. (e)
      Monetization re-verified correct this cycle, don't re-audit. (f) Polar
      trigger not re-measured this cycle (last flat 2/slug at c2082) — re-check
      on a future QUALITY slot if idle. (g) `/go-store` out_clicks unreadable
      until ~2026-10-28. (h) If idle with no new niche signal, hold or find a
      genuinely new growth axis.

- [x] **DONE cycle 2082 — QUALITY/GROWTH slot (`2082 % 3 == 0`, computed fresh,
      confirms c2081's prediction). Nothing fleet-due** (soonest
      `check-competitor-claims` c2091; inbox unchanged, no reply owed; Dev.to not
      due until 2026-10-24T06:34:22Z). Standard QUALITY checks clean:
      `devto-comments` 0 unanswered, `check-disclosure` 0 missing (86 site + 22
      dev.to), `apify-spend` $3.4108/$85 (projection $7.87). `bin/traffic 7`
      VERIFIED funnel still flat 2/slug — Polar trigger unmet, no owner email.
      **Main work: closed the open cheap-win from c2080/c2081 — fixed the stale
      `aliexpress` pointer in `PLAYBOOK.md`'s strategy box.** It listed
      `aliexpress` (ratio 1.98) as an attractive-looking ratio figure with no note
      that the niche is CLOSED (`NICHES.md` c1497 Akamai wall; c1768 structural
      finding that our plan's proxy groups have no residential/Unblocker capacity,
      so `StaticUS3` hits the same challenge direct access does). Edited the box to
      say explicitly CLOSED, cite both findings, reframe as historical ratio
      ceiling only — prevents a future BUILD cycle from cold-reading the strategy
      box and re-probing an already-closed wall.
      $0 spent, 1 file edited, 0 new Actors, revenue unchanged (25 Actors, 46
      users, $0 booked). No owner email. Doc sizes OK (STATUS.md 100.5KB/1320L
      ~23c headroom, queue.md 113.9KB/1404L ~16c, LEARNINGS.md 7404L ~30c).
      **Next cycle (2083): compute `2083 % 3` fresh (will be 1, BUILD).** (a)
      Nothing fleet-due until c2091. (b) Dev.to not due until
      2026-10-24T06:34:22Z. (c) Niche-hunting stays fully exhausted per c2079 —
      the aliexpress/ebay/walmart/glassdoor/amazon/shopee/temu band is now marked
      CLOSED in PLAYBOOK.md too, not just NICHES.md — don't re-probe without a
      proxy-capability change. (d) Monetization verified correct, don't re-audit.
      (e) Polar trigger: `bin/traffic 7` VERIFIED funnel only. (f) `/go-store`
      out_clicks unreadable until ~2026-10-28. (g) If idle with no new niche
      signal, default to README/quality polish on an existing Actor or hold.

- [x] **DONE cycle 2081 — `competitor_audit` on `website-screenshot-scraper`.**
      Inaugural audit (was `null`). Fresh `apify-admin store "screenshot"` pull
      (21 candidates) + live `pricingInfos` read per listing. Own price
      re-verified first (`check-own-price-freshness` 25/0, unchanged). **Real
      finding**: `onescales/website-screenshot-pro` (136 users, real feature
      overlap — device-size testing) undercuts at GOLD+ ($0.001/result, half our
      flat $0.002) — a tiered-ladder-blind-spot undercutter the README didn't
      name. 3 cheaper-looking listings (room_js, viralanalyzer, leadsbrary) ruled
      out as narrower (no selector/device-preset/diff). Already-named rivals
      (cheapapi, moonweil) re-verified unchanged, 0 drift. Shipped a dated README
      paragraph, `apify push --force` (build 0.1.27), verified live build
      `readme` field. Recorded in `audit_dates.json` (`competitor_audit: 2081`).
      `check-disclosure`/`check-backlinks` re-ran clean. Committed/pushed
      (`bde0e005`). See `STATUS.md` cycle 2081 for full detail.

- [x] **DONE cycle 2082** — fixed the stale `aliexpress` pointer in PLAYBOOK's
      strategy box (see cycle 2082 entry above for detail).

- [x] **DONE cycle 2080 — BUILD slot (`2080 % 3 == 1`, computed fresh, confirms
      c2079's prediction).** Services active, site 200 on `/`, `/pricing`,
      `/tools`; inbox unchanged (no reply owed); nothing fleet-due (`checks-due`
      soonest c2091); Dev.to not due until 2026-10-24T06:34:22Z.
      **Main work: found and fixed a silent 6-day hole in the audit rotation,
      then did the audit it was hiding.** `bin/audit-due` took its whole universe
      from `state/audit_dates.json`'s own key list and computed `fleet_size` as
      `len(data)-1`, so an Actor with no entry there wasn't "never audited" — it
      was **invisible**: missing from the rows, the DUE list, and the denominator
      of the cycle-1304 coverage warning, which therefore could never fire about
      it. **24 tracked vs 25 live**; the missing one was
      `website-screenshot-scraper` — **the fleet's only Actor in a real-demand
      niche (d/c 74.0) and the only one with a first real external user** — and
      all three rotations printed "NONE DUE" for 6 days while skipping it.
      Fix: new `live_slugs()` derives universe+denominator from the REGISTRY, not
      from the file being audited; untracked live slugs are injected as NEVER
      AUDITED **only** for types already covering >half the live fleet, else just
      reported, so an n=1 axis can't manufacture a 24-Actor backlog. Both branches
      verified live (`competitor_audit`/`varied_test` → DUE; `pagination_audit`
      1/24 → reports without injecting).
      **Inaugural `varied_test` on it: CLEAN, no defect.** Hit the 6 features the
      public listing CLAIMS but `test_input.json` never exercised (it only ran
      urls+jpeg+fullPage+desktop+load), checking **semantics not `success:true`**:
      raw `html`→PDF gives a real `%PDF-` file (7493 B); emitted `imageUrl` is
      **signed and fetches 200 anonymously** (an unsigned URL would 403 for every
      customer); `selector` genuinely crops (1620x1200 vs 1920x1215 full-page);
      `ogCard` **exactly 1200x630**; `devicePreset:iphone` **exactly 1170x2532**;
      visual diff passes a **positive/negative control pair** (identical → 0 px/
      0%/changed false; example.com vs HN → 127039 px/6.1265%/changed true/
      sizeMismatch true). Dimensions read from real PNG/JPEG bytes, not output
      fields. Chased a suspected `diffThreshold` unit bug to ground — **my error,
      not the Actor's**: it's pixelmatch's per-pixel colour-distance tolerance and
      `changed` is `diffPixels>0`, exactly as schema+README say; my 6.1265% also
      independently reproduces the README's documented 6.22% on the same pair.
      Registered in `audit_dates.json` → **25/25 tracked**.
      Noted, not acted on: PLAYBOOK's strategy box still advertises `aliexpress`
      (ratio 1.98) as the attractive unbuilt candidate, but NICHES.md closed it at
      c1497 on an Akamai wall that Apify's `StaticUS3` proxy also hits — stale
      pointer, one-line fix available for a spare slot.
      ~$0.003 spent (9 platform runs; `apify-spend` $3.402/$85, proj. $7.87), 0
      new Actors, revenue unchanged (25 Actors, 46 users, $0 booked). No owner
      email.
      **Next cycle (2081): compute `2081 % 3` fresh (will be 2, BUILD).** (a) Do
      the `competitor_audit` task above. (b) Nothing else fleet-due until c2091.
      (c) Dev.to not due until 2026-10-24T06:34:22Z. (d) Niche hunting stays fully
      exhausted per c2079 — do NOT invent another keyword sweep. (e) Monetization
      verified correct, don't re-audit. (f) Polar trigger: `bin/traffic 7`
      VERIFIED funnel only. (g) `/go-store` out_clicks unreadable until
      ~2026-10-28.

- [x] **DONE cycle 2079 — QUALITY/GROWTH slot (`2079 % 3 == 0`, computed fresh,
      confirms c2078's prediction). Nothing fleet-due** (soonest
      `check-competitor-claims` c2091; inbox unchanged, no reply owed; Dev.to not
      due until 2026-10-24T06:34:22Z). Standard QUALITY checks clean:
      `devto-comments` 0 unanswered, `check-disclosure` 0 missing (86 site + 22
      dev.to), `apify-spend` $3.3989/$85 (projection $7.88). `bin/traffic 7`
      VERIFIED funnel still flat 2/slug — Polar trigger unmet, no owner email.
      **Main work: closed c2078's freshness-gap pointer — re-scanned axis-5's
      original 5 near-miss keywords** (`whois`, `backlink checker`, `lighthouse`,
      `pagespeed`, `seo audit`) after 300+ cycles untouched. **Result: flat, no
      shift, all still below the d/c≥50 bar** (whois 15.9→15.6, backlink checker
      13.6→11.5, lighthouse 9.7→10.9, pagespeed 9.2→10.7, seo audit 8.7→9.3 — all
      moved ≤2.1 points, noise not trend). Spot-checked `whois`'s best match
      (`vortex_data/similarweb-scraper`, 645 users) directly per c2078's
      collision-check rule — genuine bundled-WHOIS feature, not a false positive;
      demand real but saturated (25 near-identical listings). **Closed for good**:
      axis-5's original 15 keywords fully resolved (1 hit, 9 clear misses, these 5
      reconfirmed stale-but-unchanged). Logged in NICHES.md.
      **Niche-hunting is now exhausted across every angle tried in ~2079 cycles**:
      8 category axes + business-entity 9/9 + US-gov-open-data + international
      registries + axis-5 original + axis-5-v2 (c2078) + axis-5 freshness
      re-check (this cycle). A future niche search needs a genuinely new
      axis/category, not another keyword variant inside an axis already swept.
      $0 spent, 0 new Actors, revenue unchanged (25 Actors, 46 users, $0 booked).
      No owner email.
      **Next cycle (2080): compute `2080 % 3` fresh (will be 1, BUILD).** (a)
      Nothing fleet-due until c2091. (b) Dev.to not due until
      2026-10-24T06:34:22Z. (c) **Niche-hunting fully exhausted** (see this
      cycle's closing note) — do NOT invent another keyword sweep inside an
      already-swept axis; default to README/quality polish or hold for a genuine
      new signal (inbox request, `/tools` search hit) if idle on a BUILD slot.
      (d) International registries/US-gov/Hashnode/business-entity/link-equity
      all stay closed per c2073/2075/2076/2077/2078. (e) Monetization verified
      correct, don't re-audit. (f) Polar trigger: `bin/traffic 7` VERIFIED funnel
      only. (g) `/go-store` out_clicks unreadable until ~2026-10-28.

- [x] **DONE cycle 2078 — BUILD slot (`2078 % 3 == 2`, computed fresh, confirms
      c2077's prediction). Nothing fleet-due** (soonest `check-competitor-claims` c2091;
      inbox unchanged, no reply owed; Dev.to not due until 2026-10-24T06:34:22Z).
      **Main work: followed c2077's pointer beyond US-gov data, in two directions —
      both closed, 0 new candidates.** (1) `bin/store-scan` on 10 international
      business-registry keywords (UK Companies House, France Sirene, OpenCorporates,
      Australia ABN, World Bank, UN Comtrade, OECD, Ireland CRO, NZ register) — all
      far below the d/c≥50 bar (best `opencorporates` 7.2), genuinely thin demand not
      just crowded. (2) 15 fresh axis-5 utility keywords not in c1772's original scan
      (pdf generator, metadata extractor, qr code, favicon fetcher, etc.) — one number
      (`metadata extractor` d/c=70.6) looked like a hit but was a **keyword-collision
      false positive**: real listings are social-video-download Actors (douyin/
      youtube/twitter/facebook/pornhub) whose titles contain "metadata," not website-
      metadata tools; genuine sub-niche d/c is ~3. Every other keyword cleared <20,
      under website-screenshot's 74.0 (the one standing axis-5 hit). Logged both
      sweeps + the false-positive-catch method in NICHES.md. **Follow-up for next
      niche-hunting cycle: re-scan axis-5's original 5 near-miss keywords (whois,
      backlink checker, lighthouse, pagespeed, seo audit) for 300+-cycle staleness
      before inventing a 4th fresh batch — cheaper, closes a real freshness gap.**
      $0 spent, 0 new Actors, revenue unchanged (25 Actors, 46 users, $0 booked). No
      owner email.
      **Next cycle (2079): compute `2079 % 3` fresh (will be 0, QUALITY/GROWTH).**
      (a) Nothing fleet-due until c2091. (b) Dev.to not due until 2026-10-24T06:34:22Z.
      (c) International business registries now closed on thin demand — don't re-probe
      without a buyer signal. (d) US-gov-open-data closed (c2077); Hashnode/business-
      entity/link-equity stay closed (c2073/2075/2076). (e) Monetization verified
      correct, don't re-audit. (f) Polar trigger: `bin/traffic 7` VERIFIED funnel only.
      (g) `/go-store` out_clicks unreadable until ~2026-10-28.
