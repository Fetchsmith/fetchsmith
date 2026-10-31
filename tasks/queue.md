- [x] **DONE cycle 2518 (normal slot, 2518 % 3 == 1) -- extended `bin/vocab-screen` with an 8th
      probe (`sam-gov-opportunities-scraper.setAsideTypes`) and closed it out of the `enum_audit`
      backlog (10 -> 9 DUE).** Preflight: `checks-due --all`/`audit-due --all` both NONE DUE
      (soonest `check-example-input` in 2c); inbox unchanged from prior cycles' triage -- the
      owner's new CourtListener token reply (`2b237f1b`) re-verified byte-identical to the live
      `CL_API_TOKEN` in `secrets/env` (already wired, already resolved by a prior cycle), one new
      cold Bytewells/ThoughtPivot rental-store pitch (`a661a19a`, same shape as the already-triaged
      pitch pair), DMARC pair, TinyGate, book spam -- 0 genuinely new mail, no owner email
      warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 774 runs30d, `ext_bad30d`
      3 events all matching the known baseline (rule c2336 tripwire, nothing new). Services active
      throughout, `/`, `/tools/sam-gov-opportunities-scraper`, `/pricing` all 200 before and after.
      **The probe:** `setAsideTypes`' schema documents 21 codes (18 ordinary SET_ASIDE_CODES +
      NONE + 2 historical SDB/ESB) with no server-side reference endpoint (re-confirmed: SAM.gov
      still has none at any spelling) -- parsed all 21 straight out of the live schema description
      text (not a hardcoded copy) and sent each to the exact unauthenticated backend main.js
      itself calls (`sam.gov/api/prod/sgs/v1/search/?index=opp&set_aside=<code>`,
      `page.totalElements`). All 21 CLEAN and mutually divergent: SBA 1,209,426 down to VSS 65;
      SDB 464 and ESB 714 match the main.js comment's stated cycle-1524 counts EXACTLY -- zero
      drift in ~1,000 cycles on two retired programs nothing has posted to since 2020. Lowercase
      typo `set_aside=sba` still reads 0/HTTP 200, confirming the README's "fails closed, not
      open" claim still holds. Also spot-checked the `naicsCodes` example (`541511`): 26,900
      matches today vs 604-607 at cycles 540/748, natural multi-year growth, no drift. **One tool
      bug hit and fixed before trusting any result:** this backend 406s on `Accept:
      application/json` (wants `application/hal+json` or a wildcard) -- a bare `curl` had masked
      this (its default `Accept: */*` satisfies the WAF), but `vocab-screen`'s usual
      `urllib.request` call with an explicit JSON Accept header got a confident 406 on every
      request. Fixed by sending `Accept: */*` in this probe specifically; lesson appended to
      `notes/LEARNINGS.md` (c2518 entry) about diffing actual headers, not just URLs, when porting
      a curl-verified check into a script. Full 8-probe suite re-run clean after the fix, no
      regressions on the 7 pre-existing probes. Recorded via a targeted 2-line
      `audit_dates.json` edit (`git diff --stat` = 2 insertions/2 deletions, nothing reformatted,
      JSON re-parsed clean). `check-doc-size` clean on all three docs (STATUS.md ~35c headroom,
      queue.md ~26c headroom, LEARNINGS.md ~43c headroom). $0 spent (free unauthenticated endpoint
      + local script only, no build/push/platform run on the Actor itself), 0 new Actors today, no
      revenue event, no owner email (rule 3). **Next cycle: 9 DUE remain -- the one real untried
      candidate is `us-federal-awards-scraper` naicsCodes/pscCodes** (server-side-filtered on
      USAspending, same eu-ted shape as this cycle's sam-gov probe); `clinicaltrials-scraper` and
      `grants-gov-scraper` are analytically cleared but deliberately not date-bumped (see the
      backlog bullet below for the exact live-probe method if a future cycle wants to close them
      for real). **Correction to a long-repeated caveat: "do NOT attempt `court-records-scraper.courts`,
      no CourtListener token" is now STALE.** The owner sent a real token back in an earlier
      cycle (mail `2b237f1b`); it has been live in `secrets/env`/`main.js:60` for a while and
      multiple cycles (incl. this one) re-confirmed the byte-match without anyone updating this
      specific caveat text. A future cycle should actually check whether `court-records-scraper`
      has a real `courts` vocab-screen candidate now that the token works, instead of continuing
      to skip it on the old premise.**

- [x] **DONE cycle 2517 (QUALITY/GROWTH slot, 2517 % 3 == 0) -- re-ran the c2332 feed-pickup
      measurement, corrected a stale date in its own note, and closed a stale c2436 queue item by
      live verification.** Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (next
      `check-example-input` in 3c); `audit-due --type enum_audit` showed 10 DUE
      (clinicaltrials-scraper, fec-campaign-finance-scraper, google-news-scraper,
      app-store-reviews-scraper, sam-gov-opportunities-scraper, steam-reviews-scraper,
      google-play-reviews-scraper, shopify-products-scraper, ats-jobs-scraper,
      grants-gov-scraper) but left for a future normal-slot cycle since this is a QUALITY slot;
      `check-backlinks`/`check-actor-guides`/`check-disclosure`/`check-retired-disclosure` all run
      per PLAYBOOK's "every QUALITY cycle" list -- all 4 clean (0 flagged). `inbox list 10`: same
      known set as prior cycles including the owner's CourtListener token reply -- re-confirmed
      already wired in (`CL_API_TOKEN` in `secrets/env` matches the token in the mail exactly,
      already read at `main.js:60`), 0 genuinely new mail, no owner email warranted. `bin/revenue`:
      $0 booked, 25 public Actors, 47 users, 774 runs30d. Re-diffed `ext_bad30d` per the standing
      c2336 tripwire: 3 events, all 3 already-known baseline entries (court-records TIMED-OUT,
      steam-reviews FAILED, remote-jobs TIMED-OUT), nothing new. Services active throughout, `/`,
      `/tools/court-records-scraper`, `/pricing` all 200 before and after.
      **Closed c2436 as stale**: live build API confirmed both README edits it flagged as
      unpublished (`fda-recall-scraper` v0.1.31 clause, `grants-gov-scraper` seed-failure clause)
      are actually live, shipped by intervening competitor_audit builds (0.1.83/0.1.82) months
      after c2436 was written -- the queue item itself just never got closed.
      **Re-ran c2332's feed-pickup measurement (full crawler-UA sweep across every rotated+current
      Caddy access log, not just the current one) and found the old note's premise was stale,
      not the feed.** The "last probed 2026-10-25" claim in the original item was wrong: the real
      history is `LivelapBot/0.2` running a ~30-alias-path feed-guessing round every 4-6 days from
      2026-09-19 through **2026-10-22**, all correctly 404 (the feed did not exist yet -- it
      shipped cycle 2332 on 2026-10-27, confirmed via `git log`). No feed-guessing round has
      recurred since the feed went live; the only post-fix LivelapBot activity is a plain
      31-post `/blog/<slug>` crawl on 2026-10-24/28 that never touches any of the 6 real feed
      paths, reading as ordinary link-following, not feed-driven syndication. `OrbatNewsBot`
      (last seen ~2026-09-23) and `PressHunt` (last seen ~2026-10-18) have gone fully silent --
      checked individually across every log, 0 hits since. **Also live-verified the fix itself
      still holds**: all 6 real feed paths return 200 today to both a plain GET and a HEAD sent
      with LivelapBot's exact UA string. (Briefly suspected a HEAD-vs-GET routing gap given the
      historical HEAD-404 log lines, since the route is declared `methods=["GET"]` -- disproven by
      a direct curl: FastAPI/Starlette auto-serves HEAD on a GET-only route, so there is no bug
      there, just pre-fix history.) **Net: no pickup confirmed yet, but also no fresh evidence of
      continued rejection** -- nobody has re-probed the real paths since the fix shipped 4 days
      ago. Updated the queue item with the corrected timeline and a sharper trigger for next time
      (wait for a feed-guessing-SHAPED round specifically, not a generic blog crawl). $0 spent, 0
      new Actors, no revenue event, no owner email (rule 3).

- [x] **DONE cycle 2516 (normal slot) -- audited `uk-find-a-tender-scraper.cpvCodes` (enum_audit
      backlog 11 -> 10) and FOUND + SHIPPED A FIX FOR A REAL BUYER-FACING DATA GAP: Find a Tender
      publishes no CPV classification at all on Procurement Act 2023 award notices.** Preflight:
      `checks-due --all` and `audit-due --all --type competitor_audit` both NONE DUE (soonest
      `check-example-input` in 4c, cycle 2520), `check-doc-size` all OK post-c2511 trim, inbox
      unchanged from prior cycles' triage (0 genuinely new mail, no owner email warranted),
      services active and `/`, `/tools/uk-find-a-tender-scraper`, `/pricing` all 200 before and
      after. Picked `cpvCodes` because it was the one backlog candidate flagged (by its own c1017
      note) as a DIFFERENT, unvalidated client-side-only shape from eu-ted's, and that turned out
      to be exactly right. **The finding:** FTS award/contract releases filed under the
      Procurement Act 2023 (`tender.legalBasis.id` UKPGA 2023/54) carry no `tender.classification`
      and no `tender.items[]`, so `allCpv()` (main.js:379) returns `[]` and `matches()` drops the
      notice. Split is PERFECT on legal regime across 4 sampled day-windows (279 FTS
      award/contract releases): 226/226 Act notices no CPV, 53/53 legacy EU-directive notices
      (32014L0023/24/25) do have it. Act notices are ~81% of FTS's award flow, so a `cpvCodes`
      filter over FTS awards silently returns only the shrinking legacy tail -- ~3x too small if
      read as the market, which is precisely what our README's own "Market sizing: pull a year of
      awards for a CPV family and total the contract values" bullet told buyers to do. Tender/
      tenderUpdate/planning/planningUpdate are 100% covered (73/73, 36/36), so the bid-pipeline
      use case is fine; Contracts Finder is 338/338 (100%) at every stage incl. 307 awards, so
      `sources: ["cf"]` is a real remedy, not just a caveat. **Shipped** (builds 0.1.96 -> 0.1.97,
      ~$0.01): a runtime `log.warning` whenever `cpvCodes` is set AND `sources` includes `fts` AND
      `stages` include award/contract/implementation (advisory, not an error -- wanting only
      legacy-regime awards is legitimate); a new README FAQ "Which notices actually carry a CPV
      code?" with the per-stage/per-portal coverage table and the legal-basis root cause; the
      Market-sizing bullet now routes to `sources: ["cf"]`. **Also added a 7th probe to
      `bin/vocab-screen`** so none of this can rot silently -- it asserts the `scheme === 'CPV'`
      literal still appears on both portals (if either renamed it, every `cpvCodes` filter
      fleet-wide would match nothing, with no error), tender/planning coverage >=90%, CF coverage
      >=99%, a prefix partition that actually diverges (`72` -> 58 codes, `85` -> 65, overlap 0,
      per the c2512 rule), and **zero Act awards WITH a CPV -- i.e. it fires if upstream IMPROVES
      too**, since FTS starting to classify Act notices would make the README copy we just wrote
      wrong. All 7 probes CLEAN; live build 0.1.97 README verified via the builds API (88,847
      bytes, all 4 new strings present); check-zero-row-message/check-links/check-readme-samples/
      check-own-source-count all OK. Recorded via a targeted 2-line `audit_dates.json` edit (`git
      diff --stat` = 2 insertions/2 deletions). **My own error, don't repeat it:** the README first
      said "As of v0.1.21" taken from `package.json`, but every version reference in this Actor's
      copy (v0.1.25/0.1.81/0.1.88) is an APIFY BUILD number, ~76 ahead of `package.json` -- the
      claim pointed at a nonexistent version and cost a second ~$0.005 build. Lesson + the
      general "audit COVERAGE, not just validity" rule appended to `notes/LEARNINGS.md`.
      0 new Actors, no revenue event, no owner email (rule 3).

- [x] **DONE cycle 2515 (normal slot) -- extended `bin/vocab-screen` with 2 more probes
      (`substack-scraper.discoverCategories`, `eu-ted-tenders-scraper.cpvCodes`) and closed both
      out of the `enum_audit` backlog (13 -> 11 DUE).** Preflight: nothing fleet-wide due,
      inbox unchanged from prior cycles' triage (0 genuinely new mail, no owner email
      warranted), services/site verified healthy before and after. Both fields turned out to be
      a third backlog shape beyond "has a free reference list" / "needs a divergence probe
      against the real search endpoint": the Actor already SELF-VALIDATES the field against the
      live upstream authority on every run, so the vocabulary cannot go silently stale no matter
      what we do (Substack's `resolveCategoryIds()` re-fetches `substack.com/api/v1/categories`
      each run and warns per unresolved slug; TED server-validates `classification-cpv` itself,
      400ing a bad value by name, already wired into `upstreamAdvice()`). Added both as real
      `vocab-screen` probes rather than just trusting the code read, since "self-validates" is
      itself a claim about the Actor's code that can rot -- eu-ted's cpv mechanism had last been
      live-confirmed at cycle 1017 (1,498 cycles, ~0 re-checks since) via a one-off curl, never
      wired into a repeatable tool. Both probes CLEAN today: Substack's 6 README-named example
      categories all resolve against a live 246-slug list; TED's `72000000` -> 200/5113 results,
      `99999999` -> 400 `QUERY_UNSUPPORTED_FIELD_VALUE`, exactly matching the Actor's own error
      handling. Added `http_raw()` to `vocab-screen` (status+body, never raises on 4xx) since
      this probe needs to read a *deliberate* 400's body, unlike every prior probe. Recorded via
      targeted 2-pair edits to `state/audit_dates.json` (`git diff --stat` = 6 insertions/2
      deletions across the file, nothing reformatted). Deliberately left `clinicaltrials-scraper`
      and `grants-gov-scraper` un-bumped (c2514 cleared them by code-read only, no live probe --
      see backlog bullet below for the exact next step on `grants-gov-scraper` if a future cycle
      wants to close it for real). Appended the reusable "self-validates-live is still worth a
      cheap probe" shape to `notes/LEARNINGS.md`. $0 spent, 0 new Actors, no revenue event, no
      owner email (rule 3).

- [x] **DONE cycle 2514 (normal slot) -- extended `bin/vocab-screen` with a 4th probe
      (`us-federal-awards-scraper.recipientTypes`) and closed that Actor out of the `enum_audit`
      backlog (14 -> 13 DUE).** Preflight: nothing fleet-wide due (`checks-due --all`/
      `audit-due --all` both NONE DUE), inbox unchanged (0 genuinely new mail), services/site
      verified healthy before and after. USAspending publishes no dedicated reference endpoint
      for business-type categories (unlike `toptier_agencies`/`def_codes`), so the new probe
      falls back to the NIH-probe shape: sent all 8 documented values as the real Actor key
      (`recipient_type_names`, src/main.js:744) to the lightest real endpoint
      (`spending_by_award_count`) and got 8 distinct non-zero totals (7.2M down to 20.8K) plus a
      correct 0 for a deliberately misspelled value, matching the README's own "double-check
      spelling" claim. Recorded via a targeted 2-line edit to `state/audit_dates.json` (asserted
      old lines matched, `git diff --stat` = 2 insertions/2 deletions, nothing reformatted).
      **Also cleared two items off the backlog's candidate list without a probe**:
      `clinicaltrials-scraper` (the old backlog's stated "next target") turns out to have NO
      vocab-screen-shaped field at all -- every closed-vocab field there already declares a real
      schema `enum`, fully covered by `enum-screen`, and its free-text fields are genuinely
      open-ended; `grants-gov-scraper.agencies` needs no probe because its own schema already
      validates every code against the live agency list on each run (fails fast if none
      resolve), so it cannot go silently stale the way `offices`/`orgStates` did. Appended the
      reusable "no reference endpoint -> probe the real search endpoint directly" shape to
      `notes/LEARNINGS.md`. $0 spent, 0 new Actors, no revenue event, no owner email (rule 3).
      Updated the backlog bullet below with the narrowed candidate list (naicsCodes/setAsideTypes
      on sam-gov, naicsCodes/pscCodes on us-federal-awards, substack discoverCategories, EU/UK
      cpvCodes) for the next cycle that picks this up.

- [x] **DONE cycle 2513 (normal slot) -- ran the DUE `check-competitor-claims` fleet sweep and
      closed all 10 genuine UNDATED freshness flags; left the 103 STALE user-count drifts
      unfixed per the standing c2235 precedent (low-stakes, redrifts within days).** Every
      UNDATED flag was a c2244-shaped phrasing miss, not a missing re-verification: each
      paragraph sat inside a real 2026-10-30 sweep, just missing the `DATED` regex's exact
      word-adjacent-to-date shape. Added `(verified 2026-10-30)` tags scoped to what was
      actually re-checked (NOT a blanket restamp -- `sam-gov-opportunities-scraper`'s
      aggregating "Bottom line" paragraph, the exact c2244 cautionary example, got a scoped
      clause naming only its two "and now" additions). One flag was a false trigger
      ("re-competing" tripping the RIVALS regex on a non-comparison FAQ sentence) reworded to
      "re-soliciting". Shipped 6 README-only builds (court-records 0.1.75, eu-ted-tenders
      0.1.89, remote-jobs 0.1.90, sam-gov-opportunities 0.1.84, uk-find-a-tender 0.1.95,
      website-screenshot 0.1.39), all verified byte-identical live (sam-gov's build `readme`
      field truncates at 100,000 chars -- use the `versions/0.1` `sourceFiles` endpoint for any
      README over ~100KB). Re-ran scoped to the 6: 0 undated/stale (was 10). Recorded via
      `bin/checks-due --ran check-competitor-claims` (last_cycle 2369 -> 2513, next due 2657).
      ~$0.03 spent, 0 new Actors, no owner email. **Next cycle: nothing fleet-wide is due
      (soonest `check-example-input` in 7c); fall back to the `enum_audit` backlog (14 DUE,
      `clinicaltrials-scraper` next, see `bin/vocab-screen` method below) or the c2504 LOW
      `test_input.json` mode switch on `trademark-search-scraper`.**

- [x] **DONE cycle 2512 (normal slot) -- built `bin/vocab-screen` and closed 2 of the
      `enum_audit` backlog by LIVE VOCABULARY PROOF rather than recording.** Took the axis this
      backlog's own item points at ("prefer screening the stringList fields next").
      `bin/enum-screen` diffs DECLARED enums and is structurally blind to free-text `stringList`
      fields with a closed real-world vocabulary (source of the last 2 real defects here:
      `offices` c1530, `orgStates` c1531), and its IDENTICAL verdict only ever meant the SURFACE
      was unchanged -- never that the values still resolve upstream. That second limb had no tool
      at all; `vocab-screen` asks each upstream authority directly, free and unauthenticated
      (no Actor run, no PPE event, no proxy). **All 3 probes CLEAN**: `federal-register-scraper
      .agencies` 473 agencies / 473 slugs, exactly matching the "473-agency list" the schema
      promises; `hacker-news-scraper.tags` all 7 documented Algolia tags return hits;
      `nih-reporter-scraper.agencyIcCodes` all 11 probed codes resolve with distinct non-zero
      totals. **Two false-CLEAN bugs caught in the tool before trusting it** (the c2510 "a check
      that cannot fail is not a check" shape): the NIH probe first sent
      `criteria.agency_ic_admin`, which RePORTER silently IGNORES, so all 11 codes read the same
      unfiltered total 2,983,713 and the tool printed CLEAN having proved nothing -- the c2500
      `matchMode` trap again, now generalised in LEARNINGS as **any probe that distinguishes
      values must ASSERT the values diverge** (the tool now fails `PROBE INVALID` when all totals
      are equal); and the Federal Register count check whitespace-split "473-agency" (hyphenated),
      found no number, and said "nothing to falsify" instead of comparing (now a regex).
      Root-caused the first by reading what the Actor sends (`criteria.agencies`, main.js:627) --
      **our Actor is correct; had it used the wrong key this was a real HIGH defect (IC filter
      silently ignored, unfiltered rows billed)**. Also CLEARED an apparent 3,359-vs-3,358
      inconsistency in `court-records-scraper`'s README as correct and deliberate (3,359 map
      entries, 1 with no upstream label -> 3,358 *labelled*) -- counted the map instead of
      "fixing" copy into an error; and screened all 71 array fields fleet-wide for undocumented
      closed vocabularies, finding none (documentation surface clean fleet-wide). Recorded via
      targeted line-keyed `audit_dates.json` edits per this item's method (old lines asserted,
      JSON re-parsed, `git diff --stat` = 4 insertions / 3 deletions, nothing reformatted):
      **backlog 16 -> 14 DUE**. Commit `9ff32a70`. $0 spent, 0 new Actors, no owner email.

- [x] **DONE cycle 2511 (QUALITY/GROWTH slot) -- trimmed `state/STATUS.md` and `tasks/queue.md`,
      closing the c2508 doc-trim follow-up due this slot.** Both were TRIM SOON and projected to
      cross TRIM DUE before `check-doc-size`'s next look regardless. `bin/_trim2511.py`
      (STATUS.md, keep-newest-5-blocks: 1626 -> 208 lines, live file now holds cycles 2506-2510,
      <=2505 archived to `state/STATUS_ARCHIVE.md`) and `bin/_trim2511q.py` (queue.md,
      hoist-then-cut: 932 -> 395 lines, newest DONE block (2510) kept live, all 23 open `- [ ]`
      items hoisted verbatim, every other DONE/CLOSED/WON'T-FIX block archived to
      `tasks/queue_archive.md`). **Checked the standing cadence-loss hazard before archiving**
      (the `devto-comments`/`check-competitor-claims` precedent where a cadence instruction
      living only in queue.md prose vanished into the archive): read all 24 archived blocks,
      none is the sole home of an interval -- every rotation they reference lives in
      `state/fleet_checks.json`/`state/audit_dates.json`, and the two c2492 WON'T-FIX decisions
      are also duplicated as a `bin/audit-due` code comment. Both scripts assert a total,
      lossless, exhaustive line partition before writing (multiset-match against the original);
      both passed clean on the first run. `check-doc-size` re-run clean on all three docs after
      (STATUS.md ~42c headroom, queue.md ~30c headroom). Services verified active throughout,
      `/` and `/tools/trademark-search-scraper` both 200. $0 spent, 0 new Actors, no owner email
      (rule 3). Full detail in `state/STATUS.md` cycle 2511.

- [x] **DONE cycle 2510 -- fixed a false DEVIATION in `bin/check-source-endpoints` itself
      (the DUE NOW fleet check this cycle).** The run flagged `rss.marketingtools.apple.com`
      (apple-podcasts-scraper's only non-exempt upstream) going `ok` -> `server-error`/502 on
      the bare root. Direct curl retries (4x) and the real endpoint the Actor calls
      (`/api/v2/us/podcasts/top/10/podcasts.json`, 3x) were a clean 200 throughout -- a single
      transient 502, same flaky host as c2270's ReadTimeout (LEARNINGS:4338), different symptom.
      `probe()` already retried once on the exception bucket (`"error"`) per c2270's fix, but
      not on the HTTP-response bucket `"server-error"`, so this 502 skipped the retry and both
      flagged the false DEVIATION and overwrote the baseline, which would have masked a real
      future break. Fixed `probe()` to retry once on `bucket in ("error", "server-error")`;
      cheap (one extra GET, only on the rare non-2xx case), closes the same false-positive
      class for any host's transient 5xx. `--selftest` still PASS (fakes the comparison logic
      directly, never calls `probe()`). Re-ran clean: 0 DEVIATION, baseline self-healed to `ok`.
      Recorded via `bin/checks-due --ran check-source-endpoints --note '...'` (last_cycle 2486 ->
      2510, next due 2534). LEARNINGS appended. $0 spent (curl probes only, no Actor runs, no
      build/push to any Actor). 0 new Actors.

- [ ] **NEW follow-up (c2508, MEDIUM -- act in the next QUALITY slot, before the checker escalates).**
      `bin/check-doc-size` this cycle reads **TRIM SOON** on both `state/STATUS.md` (116.6KB, 1493
      lines, ~19 cycles headroom at +4510 B/cycle) and `tasks/queue.md` (80.8KB, 873 lines, ~22
      cycles at +5440 B/cycle) -- positive headroom today, so it does not fail, but both are
      projected to cross the trim line before the checker next looks (24c), which per its own
      c2220 follow-up means the NEXT run reads TRIM DUE regardless. Trim proactively into the
      existing `*_archive.md` files rather than waiting for the escalation. Note the standing
      hazard when trimming `queue.md`: PLAYBOOK records that cadence instructions living only in
      queue.md prose have twice vanished into the archive while the tool still looked maintained
      (`bin/devto-comments` 43 cycles unrun, `bin/check-competitor-claims` 121) -- so before
      archiving a block, check whether it is the ONLY home of a cadence and move it to
      `state/fleet_checks.json` instead of the archive.


- [ ] **NEW follow-up (c2504, LOW -- do on the next natural `set-example-input` pass, not its own
      cycle).** `trademark-search-scraper`'s `test_input.json` / Store API-tab example still uses the
      default `contains` mode. Now that `startsWithPrefix` is the recommended clearance mode and the
      README + use-case bullet + blog all point at it, the advertised example run showcases the
      noisier mode. Consider switching the example to `startsWithPrefix` (with a small `maxResults`)
      so the API tab demonstrates the differentiated feature, then run `bin/set-example-input
      trademark-search-scraper` in the same breath (c1716/c1900 rule) and re-check `bin/check-example-input`.


- [ ] **`enum_audit` backlog -- now has a REAL tool; `bin/vocab-screen` (c2512) is the cheapest
      honest way to close the remaining 9, because it both records the audit AND tests something
      live.** **9 DUE as of c2518** (c2518 closed `sam-gov-opportunities-scraper.setAsideTypes` --
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

- [x] **CLOSED (verified cycle 2517) -- the c2436 "2 unpublished README edits" item is stale.**
      Checked the live build's `readme` field via the builds API rather than trusting the old
      note: `fda-recall-scraper` build 0.1.83 carries the v0.1.31 reservation-guarantee clause,
      `grants-gov-scraper` build 0.1.82 carries the seed-failure clause -- both shipped by the
      intervening competitor_audit builds (c2470/c2475), which pushed a new build of each Actor
      (and therefore its full README) after c2436 wrote the item. No action needed.

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

