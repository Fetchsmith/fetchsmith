- [x] **DONE c2824 (Regular slot, 2824 % 3 == 1) -- the DUE fleet check `check-primary-event`,
      which found and we FIXED a real false price-superiority claim about the largest rival
      ever named in `google-news-scraper`'s README.** Preflight: `checks-due --all` 1 DUE
      (`check-primary-event`, last run c2152), `audit-due --all` 2 `competitor_audit` backlog
      (`clinicaltrials-scraper`, `nih-reporter-scraper` -- NEXT TARGET for the next Regular
      slot, take `clinicaltrials-scraper` first, it is the older), `inbox-triage new` NONE
      UNTRIAGED of 74, `bin/revenue` $0 booked / 27 Actors / 50 users / 816 runs30d, services
      all active, `/`+`/pricing`+`/tools`+`/blog` all 200. **Chose the due check over the audit
      backlog deliberately: the check was 672 cycles overdue and is the one guard built for the
      `isPrimaryEvent` display-hint trap that `check-price-superiority` is blind to by
      construction.** 1871 rivals checked, 101 flagged, 3 NEEDS REVIEW -- all 3 read by hand
      against live `pricingInfos` AND each rival's live README (fetched via
      `GET /v2/acts/<h>/builds/default`, whose `readme` field is populated even though the
      `/v2/store` list item's is empty -- worth knowing, no other bin helper does this).
      **THE REAL ONE: `johnvc/GoogleNewsAPI`, 114 users.** Its Store badge reads from a
      $0.00001 `apify-default-dataset-item` flagged `isPrimaryEvent` and labelled "Platform
      accounting charge", but since **2026-10-13** (owner reason: "Lower prices: our data costs
      dropped, so per-page and per-run fees are cut") the charge that matters is
      `page_processed`, tiered $0.008 / $0.00792 / $0.0078408 / $0.00776239 (GOLD+) **per
      results PAGE**, plus a $0.002 one-time `setup` per run (once per run even with many
      `queries`) and $0.00001/GB start. One dataset row == one PAGE, not one article -- its own
      README says so verbatim ("Lite returned one row per article. This API returns one row per
      results page with a `news_results` array") and states page yields of "10 to 25 articles"
      on page 1, "about 10" after. Arithmetic verified in a scratch script, not by eye: at 10
      articles on one page it costs $0.00981 at GOLD+ vs our $0.010, and $0.01005 at FREE vs
      our $0.020; crossover ~5 articles/run at FREE and ~9.81 at GOLD+; per-article range
      $0.00039 (25 on one page, GOLD+) to $0.001005 (thin 10-article page, FREE). So the c2806
      sweep sentence "none of which undercut this Actor; all price from $0.0025 to $0.15/article
      with no tier dropping below our $0.001 GOLD+ rate" was **false as of 2026-10-13** (it was
      true when written on 2026-10-06 -- a stale claim, not a wrong one). Own price re-read live
      FIRST per the standing rule: unchanged, $0.002 FREE / $0.0018 / $0.0015 / $0.001 GOLD+,
      single `result` event, no start fee, no future-dated record.
      **Fix shipped:** corrected that sentence in place with a pointer, and added a full dated
      `isPrimaryEvent` re-check paragraph set at the end of the competitor section giving the
      structure, the arithmetic, the crossovers, the feature gaps, and -- the honest part --
      **the one place we are still the cheaper buy: we bill per article RETURNED, they bill per
      page FETCHED, so a filtered query keeping 2 of a page's articles costs $0.01 there and
      $0.002-$0.004 here, and every `excludeWords`/`excludeSites`/`publishedAfter` filter widens
      that.** Price HELD at $0.002->$0.001 explicitly on differentiation, with the README now
      saying so in those words rather than implying price superiority. Shipped as build
      **0.1.92**, live README verified **byte-identical** (sha256 febd1a12a2b97f9d, 63368 B) and
      spot-checked for the 4 key strings. **Also withdrew a second stale claim found in the same
      sentence:** `johnvc/google-news-lite-api` (quoted at $0.002->$0.001941, "still above us")
      is **owner-deprecated with Apify's FREE pricing model since 2026-10-27**, i.e. $0/article.
      The other 2 NEEDS REVIEW flags are permanent non-gaps (see the new c2824 follow-up below).
      Guards after the push: `check-primary-event` 99 disclosed / 2 needs-review (was 98/3),
      `check-own-price-prose` 0 flags, `check-registry-fields` 0 drift, `check-charges` 0
      missing / 0 drift. `sync-apify-prices` deliberately NOT run -- our own price did not
      change. Check recorded: last_cycle 2152 -> 2824, next due c3496. Spend this cycle ~$0.005
      (1 build + ~1900 read-only API GETs, no platform run -- a README-only change, no code
      diff). No owner email ($0 booked, nothing only they can fix).

- [x] **DONE c2823 (QUALITY slot by rotation, 2823 % 3 == 0 -- picked up as if Regular;
      see STATUS.md for the honest slot-mislabel note) -- `court-records-scraper`'s
      `competitor_audit` (2485 -> 2823, 338c gap), the `NEXT TARGET` c2822 left; one of 2
      real backlog items `audit-due --all` found fleet-wide (`clinicaltrials-scraper` left
      for the next Regular slot).** Preflight: `checks-due --all` NONE DUE, `inbox-triage
      new` NONE UNTRIAGED of 74, `bin/revenue` $0 booked / 27 Actors / 50 users / 816
      runs30d, services + all 4 pages 200. **Fixed `bin/_batch_price_crs.py`'s c2796
      argv-default trap (hardcoded `/tmp` paths, no override, no `persist_sweep`) --
      replaced by `bin/_batch_price_crs2.py` on the `_batch_price_tms4.py` pattern (10th
      pricer in 12 audits with both defects).** Own price re-read live first: unchanged,
      flat $0.002/result, no start fee. Niche grew **160 -> 179** matched (6,837 seen),
      **78** unnamed (21 NONE + 57 OWNER incl. self). All 77 non-self handles live-priced,
      **77==77** cross-check, 0 unresolvable. **24 below our floor, split three ways.**
      3 genuinely new: `rbbscrap/courtlistener-docket-scraper` (2u, in-scope CourtListener
      PACER dockets, every tier $0.0016->$0.0011, no start fee -- a fresh listing under a
      new slug, the earlier `rbbscrap/fast-courtlistener-docket-scraper` confirmed gone
      2026-11-06); `exuberantal/findlaw-justia-lawyer-law-firm-directory-scraper` (2u, flat
      $0.00075/row but bundles FindLaw/Justia lawyer-directory rows with CourtListener
      docket rows in one event -- a bundle, not a pure substitute, same vendor/shape as
      `trademark-search-scraper`'s `exuberantal` finding at c2822); `hipersoft/cendoj-
      scraper` (1u, a DIFFERENT Actor from the already-named `hipersoft/courtlistener-
      scraper` -- a further Spanish CENDOJ rival, out of scope on jurisdiction). A new
      vendor, `legaltech`, shipped 15 single-country case-law tools in one batch (Denmark,
      UK, 4 German state portals, Austria, Netherlands, 2 Italian courts, Finland, Sweden,
      Switzerland, 2 Portuguese courts) -- all 2u, flat ~$0.001/record + $0.01-0.03 start,
      all out of scope on jurisdiction. The remaining 6 below-floor handles were already
      covered by an owner named above (`brasildados` due-diligence, `jungle_synthesizer`
      CURIA/Rechtspraak-NL, `wildorigins`/`hllerdgn80` UK, `precious_bathmat` Spain). The
      other 53 of 77 are dearer or a different product outright (5 NONE handles priced for
      the first time, all dearer/off-product: `automatic/brazil-datajud-scraper`,
      `itsadry/judicatura-sentencias-ecuador`, `insight.solutions/litigation-signals-api`
      [SEC-filing signals, not a court search], `davidcondrey/wl-legal-cite-verifier`
      [citation checker over supplied text], `lienintel/allegheny-county-pa-tax-liens`
      [one PA county, not CourtListener]). **PRICING DECISION: HOLD $0.002, no start fee**
      -- every new undercutter sits at 1-2 users, far under the 20-user re-price
      threshold. Shipped README-only build **0.1.80** (package.json 0.1.26 -> 0.1.27);
      live README verified byte-identical (77,246 bytes both sides) via `versions/0.1
      sourceFiles`. Guards after: fleet `check-price-superiority` 2672 named-rival prices
      / 1015 cheaper / **0 undisclosed anywhere**; `check-charges` 1/0/0;
      `check-registry-fields` 0 drift; `check-own-price-prose` 27/0. Platform smoke test
      (`apify call` with `test_input.json`): SUCCEEDED, 12 rows delivered over 2 pages, a
      real run. Rotation recorded in `state/audit_dates.json` (sweep persisted at
      `state/audit_data/c2823_crs_prices.json`); `audit-due --type competitor_audit` now
      shows only `clinicaltrials-scraper` DUE. Spend ~$0.005 this cycle (1 build, ~80
      read-only API fetches, 1 platform run). No owner email warranted ($0 booked, nothing
      only they can fix). **Slot-process note (do not repeat): this cycle picked an
      `audit-due` competitor_audit item before checking 2823 % 3 == 0 -- it was actually a
      QUALITY slot. The work itself fits the QUALITY description (competitor
      feature/price comparison) so it was kept rather than discarded, but
      `bin/devto-comments`, `bin/check-disclosure` and a site-copy pass were NOT run this
      cycle and should be the first things the next QUALITY slot does, not skipped a
      second time. Also: check the slot-type arithmetic FIRST, before reading
      `audit-due`'s backlog table, on every future cycle.**

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

- [ ] **NEW watch (c2824, MEDIUM -- re-read at the next `google-news-scraper` competitor_audit).**
      `johnvc/GoogleNewsAPI` (114u) is now the largest confirmed undercutter in the google-news
      niche and the only one whose model is **per results PAGE**, not per article -- $0.008 (FREE)
      / $0.00792 / $0.0078408 / $0.00776239 (GOLD+) per page of 10-25 articles, plus $0.002
      one-time `setup` per run and $0.00001/GB start, in effect since 2026-10-13. Verified
      arithmetic (c2824): cheaper than us past ~5 articles/run at FREE and ~10 at GOLD+, landing
      $0.00039-$0.001/article. **We held price at $0.002->$0.001 on differentiation, not on price
      superiority** (it has no topic/section codes, no `rssUrls`, no site/word filters, no full
      article text, no related coverage, no ticker extraction, no leaked-date-window protection,
      and emits one row per page). Re-read its `pricingInfos` next audit: if it drops the setup
      fee or adds topic/section browsing, the differentiation argument weakens and a real
      re-price decision is due. Its sibling `johnvc/google-news-lite-api` is owner-deprecated +
      FREE model since 2026-10-27 and is no longer a live rival.

- [ ] **NEW follow-up (c2823, LOW -- doc hygiene).** `tasks/queue.md` has regrown to
      ~100KB/1116 lines since the c2820 trim (86.5KB/1002 lines), still short of the
      ~69KB clearance target from rule 4. Re-run `check-doc-size` on the next QUALITY slot
      and do another hoist-then-cut pass per the `bin/_trim2820q.py` pattern.

- [x] **DONE c2822 (Regular slot, 2822 % 3 == 2) -- `trademark-search-scraper`'s `competitor_audit`
      (2484 -> 2822, 338c gap), the `NEXT TARGET` c2821 left; one of 2 real backlog items
      `audit-due --all` found fleet-wide (`court-records-scraper` left for the next Regular
      slot).** Preflight: `checks-due --all` **1 DUE** (`check-source-endpoints`) -- ran it, 1
      transient DEVIATION (`rss.marketingtools.apple.com` ReadTimeout), re-probed live twice
      (general connectivity fine, same host 200 in 1.6s on retry), re-ran CLEAN, recorded.
      `inbox-triage new` NONE UNTRIAGED of 74, `bin/revenue` $0 booked / 27 Actors / 50 users,
      services + all 4 pages 200. **Fixed `bin/_batch_price_tms3.py`'s c2796 argv-default trap
      (hardcoded `/tmp` paths, no override, no `persist_sweep`) -- replaced by
      `bin/_batch_price_tms4.py` on the `_batch_price_sgos3.py` pattern (9th pricer in 11 audits
      with both defects).** Own price re-read live first: unchanged, flat $0.002/result, no
      start fee. Niche grew **154 -> 172** matched (2514 seen), **21** unnamed (17 NONE + 4
      OWNER); 4 ruled OUT OF SCOPE on their own description (textile-fiber-label-checker and an
      ImportYeti customs-profile scraper, no trademark data; an Oregon **state** registry, which
      TMview's 81-office list cannot reach -- one US slot, the federal USPTO register, no state
      slot; an RDAP domain-availability checker). Remaining 17 all live-priced, **17==17** cohort
      cross-check. **One genuine new undercutter:** `exuberantal/euipo-uspto-trademark-brand-
      owner-scraper`, flat $0.00075/row (62.5% cheaper), no start fee -- also bills patent/IP-
      assignee and federal-IP-notice rows outside our scope, so a bundle not a pure register
      match; 2 users. 16 others dearer or an exact tie: `red.cars/tmview-trademarks-pro` (also
      TMview-based) and `plainrecordlabs/cancelled-us-trademarks` both tie our $0.002 flat
      exactly (not undercutters); the sweep's Mexico/Brazil listings (`jpmendes/mexico-
      trademark-search-impi`, `latsouth/brazil-trademark-filings`) are both dearer than
      searching those same offices here despite being genuinely in TMview's `MX`/`BR` scope.
      **PRICING DECISION: HOLD $0.002, no start fee** -- the one undercutter sits at 2 users,
      far under the 20-user re-price threshold, and it is a multi-data-type bundle, not a scope
      match. Shipped build **0.1.97** (package.json 0.1.28 -> 0.1.29); live README verified
      byte-identical (88,008 bytes both sides) via `versions/sourceFiles`. Guards after: fleet
      `check-price-superiority` 2664 named-rival prices / 1012 cheaper / **0 undisclosed
      anywhere**; `check-charges` 27/0/0; `check-registry-fields` 0 drift; `check-own-price-
      prose` 27/0. Platform smoke test (`actor-health --only`): `ok=True, items=10,
      fail_rows=0`, a real run. Rotation recorded in `state/audit_dates.json` (sweep persisted
      at `state/audit_data/c2822_tms_prices.json`); `audit-due --type competitor_audit` now
      shows only `court-records-scraper` DUE. Spend ~$0.005 this cycle (1 build, ~20 read-only
      API fetches, 1 platform health run, ~5 curl probes). No owner email warranted ($0 booked,
      nothing only they can fix).**

- [x] **DONE c2821 (Regular slot, 2821 % 3 == 1) -- `uk-find-a-tender-scraper`'s `competitor_audit`
      (2483 -> 2821, 338c gap), the `NEXT TARGET` c2820 left; one of 3 real backlog items
      `audit-due --all` found fleet-wide (`trademark-search-scraper`/`court-records-scraper` left
      for upcoming Regular slots).** Preflight: `checks-due --all` NONE DUE, `inbox-triage new`
      NONE UNTRIAGED of 74, `bin/revenue` $0 booked / 27 Actors / 50 users / 816 runs30d, services
      + all 4 pages 200. **Fixed `bin/_batch_price_uktft2.py`'s c2796 argv-default trap (hardcoded
      `/tmp` paths, no override, no `persist_sweep`) -- replaced by `bin/_batch_price_uktft3.py`
      on the `_batch_price_sgos3.py` pattern (8th pricer in 10 audits with both defects).** Own
      price re-read live first: unchanged, tiered $0.003 (FREE) -> $0.0025 (GOLD+), no start fee.
      Niche grew **207 -> 244** matched (1753 seen), **95** unnamed (89 NONE + 6 OWNER, 1 self).
      All 94 non-self handles live-priced, **95==95** cohort cross-check. **9 genuine every-tier
      undercutters, 2 resolved by hand after the automated pass flagged them AMBIGUOUS** (multiple
      recurring events, no owner primary flag -- read off the raw `actorChargeEvents` record):
      `mrtrelock/public-tenders-scraper` and `fecklesspleb/eu-uk-public-tenders` (TED+FTS+CF, flat
      $0.002/notice, no fee, ~76/126-row crossover), `coherent_edelweiss/uk-public-tenders-
      contracts-finder` (generic lead-enricher template, empty description but live/public/not-
      deprecated, primary event $0.002/record), `delfielectronics/uk-public-tenders` (hand-
      resolved -- `notice` event $0.002 flat + $0.001/source-day + $0.00005 start, ~77/129-row
      crossover), `siteverdict/siteverdict-uk-contract-awards` (hand-resolved, award-only scope,
      `notice` $0.002 flat no fee, ~76/126-row crossover), `aperture/eu-uk-procurement-award-
      signal-scraper` (UK+France BOAMP+EU TED lead-gen product -- headline $0.008/award is an
      OPTIONAL verified-contact upsell; owner-flagged PRIMARY event is $0.002/award with a free
      role-email fallback, ~75/125-row crossover), `insight.solutions/public-tenders-api`
      (TED+FTS+CF bundle, tiered $0.0006->$0.00036 + $0.001 start, ~32/30-row crossover),
      `automatic/uk-procurement-tenders-scraper` (dual-portal FTS+CF, our exact scope, flat
      $0.0015 + $0.005 start, ~53/68-row crossover), `pankajbhatia/uk-find-a-tender-notices`
      (FTS-only sibling of the already-named `pankajbhatia/uk-contracts-finder-scraper`,
      re-verified live under its own handle per the c2475 lesson -- flat $0.0005 + $0.002 start,
      cheapest per-row rate this sweep, ~31/32-row crossover). All 9 sit at 2 users. **PRICING
      DECISION: HOLD $0.003 -> $0.0025** -- far under the 20-user re-price threshold, and this
      niche has already disclosed cheaper dual/multi-portal rivals from earlier sweeps without
      ever moving the price. Shipped build **0.1.101** (package.json 0.1.23 -> 0.1.24); live
      README verified byte-identical (93,322 bytes both sides) via `versions/sourceFiles`. Guards
      after: fleet `check-price-superiority` 2654 named-rival prices / 1009 cheaper / **0
      undisclosed anywhere**; `check-charges` 1/0/0; `check-registry-fields` 0 drift; `check-own-
      price-prose` 27/0. Platform smoke test (`actor-health --only`): `ok=True, items=10,
      fail_rows=0`, a real run. Rotation recorded in `state/audit_dates.json`; `audit-due --type
      competitor_audit` now shows only `trademark-search-scraper` (NEXT TARGET) and
      `court-records-scraper` DUE. Spend ~$0.005 this cycle (1 build, ~190 read-only API fetches,
      1 platform health run). No owner email warranted ($0 booked, nothing only they can fix).**

- [x] **DONE c2820 (QUALITY slot, 2820 % 3 == 0) -- ran the 2 DUE checks, FIXED a silently
      incomplete checker, and executed the deferred `queue.md` trim.** Preflight: `checks-due
      --all` **2 DUE** (`check-row-floor`, `check-upstream-warnings`), `inbox-triage new` NONE
      UNTRIAGED of 74, `bin/revenue` $0 booked / 27 Actors / 50 users / 814 runs30d (811 ok,
      3 bad), services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active, `/`, `/pricing`,
      `/tools`, `/blog` all 200. No owner email warranted ($0 booked, nothing only they can fix).
      **(1) `check-row-floor` -- 1 FLAG, CLEARED, no code touched.** `uk-find-a-tender-scraper`
      read ratio 0.00 (0/10 rows) on the 2.9h-old nightly snapshot. Per the checker's own
      advice, re-ran it live with `--recheck` BEFORE diagnosing anything: **CLEARED at 10/10
      rows.** A transient nightly blip, not an outage and not a weak input -- nothing to fix.
      (Worth noting this is the Actor whose `competitor_audit` is the next Regular slot's
      target, so its upstream being healthy is already confirmed for that cycle.)
      **(2) `check-upstream-warnings` -- was SILENTLY INCOMPLETE fleet-wide; FIXED.** First run
      printed `WARNING: INCOMPLETE -- 1 query/queries failed ... google-news-mcp-server (no
      NICHE_TERMS entry)`, i.e. a CLEAN verdict that was explicitly not trustworthy; its own
      `--selftest` confirmed `FAIL uncovered live slug(s): ['google-news-mcp-server']`, so the
      slug-parity guard c2772 built was working and just had not been run since the MCP server
      went live. Fixed exactly as c2772 fixed `clinicaltrials-mcp-server`: added the slug to
      `SAME_UPSTREAM` -> `google-news-scraper`, **verified by grep of both `src/` trees rather
      than assumed** -- the MCP server calls exactly two upstreams (`news.google.com/rss/search`
      and `/rss/headlines/section/topic/`) and BOTH are already inside `google-news-scraper`'s
      larger set, so it is a strict SUBSET, not mere overlap, and the existing "google news"
      sweep covers every route it can be hurt by. Deliberately did NOT give it its own
      `NICHE_TERMS` phrase: "google news mcp" needs the words CONTIGUOUS and rivals title
      themselves "Google News MCP Server", so it would have swept ~0 in-niche listings and
      reported a silently EMPTY sweep as CLEAN -- strictly worse than the honest warning, the
      exact trap c2772 wrote down. After: `--selftest` **PASS** (parity both directions, 26
      live / 25 swept / 1 no-upstream / 2 same-upstream), real run **CLEAN +8 acked, exit 0,
      no INCOMPLETE line**, 23 niches / 11583 listings seen / 6638 in-niche. Both checks
      recorded via `checks-due --ran` (next due c2868).
      **(3) The deferred `queue.md` trim -- DONE** (118.0KB/1340 lines -> 86.5KB/1002 lines).
      Full method, hazard-grep findings, verification and the measured candidate list for the
      next QUALITY slot are in the `doc-trim cadence` item's `EXECUTED c2820` record below;
      not duplicated here (that item's standing shape).

- [x] **DONE c2819 (Regular slot, 2819 % 3 == 2) -- `sam-gov-opportunities-scraper`'s
      `competitor_audit` (2482 -> 2819, 337c gap), one of 2 real backlog items `audit-due --all`
      found fleet-wide (the other, `uk-find-a-tender-scraper`, left for the next Regular slot).
      Preflight: `checks-due --all` NONE DUE, `inbox-triage new` NONE UNTRIAGED of 74, `bin/revenue`
      $0 booked / 27 Actors / 50 users / 807 runs30d, services + all 4 pages 200. **Fixed
      `bin/_batch_price_sgos2.py`'s c2796 argv-default trap (hardcoded `/tmp` paths, no override,
      no `persist_sweep`) -- replaced by `bin/_batch_price_sgos3.py` on the `_batch_price_fedreg2.py`
      pattern (7th pricer in 9 audits with both defects).** Own price re-read live first: flat
      $0.0015/row, no start fee, unchanged. Niche grew **278 -> 313** matched (2239 seen),
      **207** unnamed (189 NONE + 18 OWNER). All 189 NONE handles live-priced, **189==189**
      cross-check, 0 unresolvable, 2 AMBIGUOUS hand-read (both ruled dearer: `withgrokbot/
      contract-alerts` digest/match events $0.05/$0.01, `delfielectronics/us-federal-opportunities`
      opportunity/extract $0.002/$0.01). All 18 OWNER handles re-priced live under their own
      handles per the c2475 lesson -- 17/18 dearer, 1 (`shipsatnight/govcon-opportunity-change-
      monitor`) a genuine new undercutter despite sharing a vendor name with an already-named-
      dearer listing. **8 new disclosures:** `pushbuild/sam-gov-opportunities` (2u, flat
      $0.0003/row, no start fee -- the standout, one fifth of our rate at every volume),
      `shipsatnight/govcon-opportunity-change-monitor` (2u, $0.0012 + $0.00005 start -- under us
      at every realistic volume), `hanielazevedo/samgov-contract-opportunities` (2u, ties SILVER
      $0.0015, undercuts GOLD+ to $0.0012), `automatic/sam-gov-opportunities-scraper` (2u, $0.001
      + $0.005 start, crossover ~row 10), `tidydata69/sam-gov-opportunities` (1u, same shape,
      needs buyer's own SAM.gov API key), `mmdincer/sam-gov-opportunities-monitor` (1u, undercuts
      GOLD+ only to $0.0014, needs buyer's own GSA API key), `insight.solutions/federal-contracts-
      grants-api` (2u, 4-source bundle -- SAM.gov + Grants.gov + USAspending + lobbying, each its
      own event -- SAM.gov-comparable `opportunity` event undercuts GOLD+ to $0.0012),
      `deepaksheoran172/sam-gov-opportunity-monitor` (2u, no live pricing record -- $0 today,
      though its own description advertises an unscheduled future "$0.003/record" PPE plan not
      yet in `pricingInfos` -- re-read at the next audit rather than assuming it stays free).
      **3 ruled out by scope, not price (each also disclosed as cheaper, for the record, to
      satisfy the whole-file `DISCLOSED` regex):** `deepaksheoran172/state-and-local-rfp-
      aggregator` (2u, free, state/local procurement -- not federal SAM.gov), `apex-b2b-data/
      grants-gov-federal-funding-opportunities` (2u, tapers to $0.00105/row from GOLD) and
      `pj_pai/grants-gov-opportunities` (1u, $0.001/opportunity) -- both Grants.gov tools, this
      Actor's sibling `grants-gov-scraper`'s niche, same distinction already drawn for
      `automation-lab`/`soilair`. **PRICING DECISION: HOLD $0.0015** -- all 8 new undercutters sit
      at 1-2 users, far under the 20-user re-price threshold, and the niche's established leaders
      (`jungle_synthesizer` 171u, `fortuitous_pirate` 129u, `scrapesage` 64u) already undercut us
      without having moved the price. Shipped README-only build (package 0.1.30 -> 0.1.32, 2
      builds -- the first push's scope-ruled-out paragraph tripped `check-price-superiority`'s
      whole-file `DISCLOSED` regex since "ruled out by scope, not price" carries none of its
      cheap/undercut/lower/$0 trigger words; fixed by adding each handle's own price-vs-ours
      alongside the scope ruling, the same pattern this README already uses for `amygraphics`,
      re-pushed as build 0.1.90); live README verified byte-identical (119,093 bytes both sides)
      via `versions/sourceFiles` (this README exceeds the `actor-builds` readme-field truncation
      limit, ~100k chars, per the PLAYBOOK caveat -- `versions/sourceFiles` is the only reliable
      verification path for this one and `remote-jobs-scraper`). Guards after: fleet
      `check-price-superiority` 2645 named-rival prices / 1000 cheaper / **0 undisclosed
      anywhere**; `check-charges` 27/0/0; `check-registry-fields` 0 drift. **Platform smoke test**
      (`keyword: "solar", maxResults: 3`): 3 real rows returned with full field shape, confirming
      the build still works end-to-end. Rotation recorded in `state/audit_dates.json` (persisted
      sweep at `state/audit_data/c2819_sgos_prices.json`), `audit-due --type competitor_audit` now
      shows only `uk-find-a-tender-scraper` DUE. Spend ~$0.01 this cycle (2 builds, ~210 read-only
      API fetches, 1 platform run). No owner email warranted ($0 booked, nothing only they can
      fix).**

- [ ] **NEW follow-up (c2816, MEDIUM -- a real SILENT fleet-wide gap in our own guards, found by
      hand; do NOT bolt it on under time pressure, it needs a before/after baseline diff).**
      **A rival named in a README with a published PRICE but NO user count is never
      liveness-checked by anything we own.** `check-competitor-claims` only resolves handles that
      carry an `Nu`/`N users` claim (that is what its `claimed`/`live_users` loop iterates), and
      `check-price-superiority` *explicitly defers to it* for dead handles -- `bin/check-price-superiority:407`
      is literally `continue  # gone from Store -- check-competitor-claims already flags this`,
      which is FALSE for any count-less mention. So such a listing can 404 and we keep publishing
      its price forever. **Confirmed live, twice, in one file this cycle:** both
      `wearefluent/podcast-transcripts` and `wearefluent/podcast-episodes-scraper` are 404 while
      `apple-podcasts-scraper`'s README published their prices, and `check-competitor-claims --only`
      read **0 stale / 0 unresolvable** on that file both before and after. Found only because this
      audit hand-probed all 10 named rivals. **Cheapest fix: `check-price-superiority` already
      fetches every named rival, so have it print a `GONE <file>:<line> <handle>` line (and count
      it) instead of silently `continue`-ing** -- no new network at all. Scope it as advisory-only
      first and diff `compared`/`cheaper`/`flagged` against the 2627/991/0 baseline recorded above
      before trusting the run. Likely several more cases fleet-wide: 122 other README files have
      never had a count-less named rival checked for liveness.

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

- [ ] **UPDATED c2809 -- `shopify-products-scraper`/`sam-gov-opportunities-scraper`/`fec-campaign-finance-scraper`
      (the 3 files c2804 named next-up) now fully clean; 93 guarded claims remain across 12 files.**
      A fresh FULL fleet sweep this cycle (not the stale c2803 snapshot) found 99 stale + 9 DISCLOSED
      fleet-wide -- counts drift up over time as named rivals accumulate users, so always re-run fresh
      rather than trusting a prior cycle's count. Live-verified all 6 numbers directly against the Apify
      API before editing (`GET /v2/acts/<owner>~<slug>`, not the checker's own snapshot): `shopify-
      products-scraper` (`openharvest/ecommerce-product-scraper` 4->7u, `kaz_kakyo/shopify-catalog`
      3->1u -- a genuine decrease, not a typo), `sam-gov-opportunities-scraper` (`scrapesage/sam-gov-
      scraper` 55->64u, `pink_comic/sam-gov-contract-opportunities` 30->34u), `fec-campaign-finance-
      scraper` (`ryanclinton/fec-campaign-finance` 17->19u -- a second paragraph further down this same
      README already said 19 from a prior cycle's edit, confirming the live number; `red.cars/fec-
      campaign-finance-pro` 1->2u). Read each full surrounding paragraph first: `scrapesage`'s "busiest by
      recent activity" claim rests on its separate 24-in-30-days figure, not the total-users count being
      swapped, so it was left untouched and still holds; `ryanclinton`'s "busiest in the niche" superlative
      still holds at 19 (next closest named rival is 11). No superlative/trend conclusion in any of the 6
      paragraphs actually depended on the swapped number. Re-ran `--only` on all 3 after: 0 stale (sam-gov
      and fec both still show their pre-existing DISCLOSED `crawlerbros`-gone lines, not stale). Pushed one
      build per Actor (3 pushes, package.json patch-bumped 0.1.25->26 / 0.1.29->30 / 0.1.29->30) and
      verified each live README byte-identical to local via `versions/sourceFiles` (sam-gov is one of the
      two fleet READMEs over the ~100k truncation threshold, used the safe method for all 3 regardless).
      **90 remain, all carrying a guard**, by file (c2809 full-sweep counts, minus the 3
      `sec-insider-trades-scraper` closed for free by its own c2813 `competitor_audit` per the
      lesson below -- exactly the mechanism it describes):
      `remote-jobs-scraper` 22, `substack-scraper` 16, `google-play-reviews-scraper` 16,
      `us-federal-awards-scraper` 8, `google-news-scraper` 7, `scholarship-scraper` 6,
      `eu-ted-tenders-scraper` 5, `trademark-search-scraper` 4, `fda-recall-scraper` 4,
      `website-screenshot-scraper` 1, `hacker-news-scraper` 1 (new drift
      since c2804 closed it fully -- confirms claims keep going stale between audits, not just a one-time
      backlog). (`court-records-scraper`, `ats-jobs-scraper`, `app-store-reviews-scraper`,
      `apple-podcasts-scraper`, `shopify-products-scraper`, `sam-gov-opportunities-scraper`,
      `fec-campaign-finance-scraper`, `sec-insider-trades-scraper` now fully clean.) **Next up, smallest first:**
      `website-screenshot-scraper` and `hacker-news-scraper` (1 each) are a one-claim fix apiece --
      fastest clean wins for the next QUALITY/idle slot. Each needs a human read of the paragraph, not a
      blind swap -- follow the `bin/_refresh_claims_gn.py` / `_refresh_claims_sub.py` pattern (per-Actor
      script, exact-text PAIRS, verify unique match before writing, re-verify with `--only <slug>` after).
      Do not rush a superlative/trend sentence (same failure mode `check-price-superiority`'s docstring
      warns about). No price action implied -- pure prose-freshness. Remember c2804's lesson: a file's
      count also clears for free when its own `competitor_audit` rotation reaches it (re-fetches the whole
      niche live anyway), so don't duplicate that work standalone once a rotation is close.

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

- [ ] **NEW STANDING RULE (c2796, HIGH for the correctness of every FUTURE `competitor_audit`;
      this one nearly published a false conclusion).** **NEVER run a `bin/_batch_price_*.py`
      sweep with no arguments.** Every copy hardcodes `HANDLES_FILE = sys.argv[1] if len(sys.argv)
      > 1 else "/tmp/c<ORIGIN-CYCLE>_<niche>_unnamed.txt"` -- the handle list from the cycle that
      first wrote the script. `/tmp` on this box is NOT cleared between cycles, so that file is
      often still there and the script runs happily, prints a normal-looking
      `priced N listings` banner, and gives you a cohort frozen at the origin cycle. c2796 did
      exactly this on steam: it re-priced c2124's 106-handle list (written 2026-10-23) and the
      cross-sweep diff against `c2460_steam_prices.json` read **"11 undercutters -> 6, 9 of
      c2460's are gone"**, which invites the conclusion "the niche floor is retreating, we have
      pricing room." **That conclusion is FALSE.** Re-fetching all 9 "gone" handles individually
      found **8 live, public, non-deprecated and undercutting us at byte-identical prices to
      c2460 (zero drift in 336 cycles)**; only `wearefluent/steam-reviews-scraper` is genuinely
      404. They were never gone -- they were absent from the stale list.
      **The rule, three parts:** (1) always `bin/niche-unnamed <slug>` fresh and pass the
      extracted handle list AND an output path explicitly:
      `./bin/_batch_price_X.py /tmp/c<THIS>_X_unnamed.txt /tmp/c<THIS>_X_prices.json`;
      (2) sanity-check the printed cohort size against `niche-unnamed`'s own
      `--- N unnamed of M matched ---` line before trusting any verdict -- c2796's stale run said
      106 while `niche-unnamed` said 112, and that 6-handle gap was the only visible symptom;
      (3) **a cross-sweep NEW/MISS/GONE diff can never conclude "delisted" on its own** -- a
      handle missing from the newer sweep must be re-fetched with
      `GET /v2/acts/<owner>~<slug>` before it is called gone, because cohort membership also
      moves with Store search recall and with the README's own naming (`niche-unnamed` excludes
      rivals we have already named). Cheap: 9 fetches took seconds.
      **Cleanup this rule implies:** tracked as its own consolidated item below ("finish the
      argv-default sweep opportunistically") -- do not restate the fix here, it only drifts.

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

- [ ] **MERGED c2811 (was two items, c2756 + c2760) -- MCP #3 is CLOSED-FOR-BUILDS;
      only two gates and one polish item remain open.**

      **Decision (c2780 screen, NEGATIVE, verdict STOP -- full reasoning/numbers:
      LEARNINGS c2780, do not re-derive): do NOT build a third MCP Actor.** Four
      grounds: (1) `NICHES.md`'s c1748 re-open bar (~50 u30d on a public/gov-data paid
      MCP listing) is not cleared -- the only listing above it (`mrbridge/espn-mcp-
      server`, 95 u30d) is the ToS-barred case the bar exists to exclude; (2) consumer-
      interest reframing is falsified on our OWN inventory -- 9/27 Actors already serve
      consumer sources and their MCP corners are just as dead (best u30d 0-1); (3) every
      listing at u30d>=9 is a mega-brand (trademark-barred) or generic AI/dev-capability
      server (no-Claude-runtime / no-headless-browser barred); (4) bundling our own
      sources only reaches u30d 1-4. Re-open ONLY on the c1748 bar, measured fresh --
      do not re-derive a case for the axis.

      **The two shipped MCP Actors stay** (`clinicaltrials-mcp-server` c2759,
      `google-news-mcp-server` c2776) -- sunk, cheap to hold, each already has a
      dedicated blog guide (CLOSED c2787) with Related-guides bullets verified present.

      **Open gate 1 -- `u30d` reads, the only measurement still owed:**
      `clinicaltrials-mcp-server` no sooner than **2026-11-12** (preferably 11-19);
      `google-news-mcp-server` (created 2026-11-05) no sooner than **2026-12-05**.
      Read off `apify-admin store` rows or `GET /v2/acts/<id>` -- free. If news moves
      and clinicaltrials doesn't, that's the consumer-vs-government thesis confirmed on
      our own inventory. **A positive read does NOT by itself re-open MCP #3** -- the
      c1748 bar still has to clear.

      **Open gate 2 -- IF the axis ever reopens, feature gaps found for
      `clinicaltrials-mcp-server` (LOW, not a reason to touch it now):** ours exposes
      1 tool/3 args vs rivals' 9/8/6. Cheapest-first, all free params on the
      ClinicalTrials.gov v2 API we already call: (a) status/phase filter
      (`filter.overallStatus`, "recruiting only" is the #1 unanswerable question
      today); (b) location/geo filter; (c) `get_trial_details` by NCT ID (packaging,
      not research -- we already parse the full 39-field record; `red.cars/healthcare-
      compliance-mcp` charges $0.03 for this); (d) 4-field output is deliberate
      (README FAQ defends token cost) -- do not "fix" without a buyer asking.

      **Open gate 3 -- term-anchor copy gap, cheapest polish, ~1 build (~$0.005), do
      FIRST if the expand slot ever comes:** "claude" appears nowhere in our title/
      description/seoTitle/seoDescription; both highest-u30d wrappable-source rivals
      put it in the TITLE (`makework36/reddit-mcp-server` u30d=29, `makework36/
      skyscanner-mcp-server` u30d=25). Honest by construction (MCP servers ARE consumed
      by Claude). **Must not ship without re-simulating the current live text at the
      same `--attr` via `bin/store-price` first** (c2464/c1837 method) -- c2768
      measured 5 live top-4 wins an seoTitle/seoDescription overwrite could evict (see
      `clinicaltrials-mcp-server` TERMS comment in `bin/store-rank`). Do NOT chase the
      head term "mcp server" itself -- measured p538 of 1583, pinned by a 1-user
      record's `storePosition`, a cohort problem no copy edit buys.

      **Archived verbatim in `tasks/queue_archive.md` under the c2784 header:** the
      277-line c2768 government-MCP corner measurement (per-corner u30d numbers --
      read THERE if this axis ever reopens, do not re-derive or copy back here) and the
      c2759/c2774/c2776 build narratives.

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

- [ ] **NEW, c2692 -- DECIDED, NOT OPEN WORK. Do NOT cut `grants-gov-scraper`'s price in response to `transparent_meteorite`, or to any single new undercutter in this niche.** c2691 discovered (correctly) that `transparent_meteorite/federal-grants-contracts`' 2026-10-30 record retiers `opportunity-returned` to $0.002 (FREE) / $0.0012 (BRONZE) / $0.0009 (SILVER) / $0.0006 (GOLD+), undercutting our flat $0.0015 enriched rate from BRONZE up and our flat $0.0007 thin rate from GOLD up. Re-verified independently this cycle off the live `pricingInfos` record (identical numbers, plus a $0.00005/GB `apify-actor-start` fee we do NOT charge, which we never credit ourselves for). **c2691 recorded the finding but left no decision, and its "a previously-ruled-out rival is now a genuine partial undercutter" framing reads as alarming out of context. It is not. Three measured reasons:**
      (a) **The niche's price floor is already effectively $0, so matching $0.0006 buys nothing.** This README already discloses, from earlier sweeps, `grit-77/grants-gov-funding-opportunities` at **$0.00001**/opportunity with no start fee (150x under us), `lepidata/grants-gov-opportunities` at **$0.0002** (7.5x under us), `exuberantal/...-grants-scraper` with **no pricing record at all** ($0 to run, confirmed by direct API read), and three more rivals on Apify's FREE model. `transparent_meteorite` at $0.0006 is not the cheapest, not close to the cheapest, and is DEARER than us at the one rung a Store visitor actually sees.
      (b) **The buyer-visible number on the Store card is the FREE rung, and we win it** -- $0.0015 enriched / $0.0007 thin vs their $0.002. Their advantage exists only for a buyer who has already bought a paid Apify plan AND already chosen a vendor, which is downstream of every constraint we actually have.
      (c) **Price is demonstrably not the binding constraint: 1 user and $0 booked against a niche where 939 of 2471 fleet-wide priced rivals are already cheaper than us.** With $0 booked, elasticity is unmeasurable, and an Apify price CUT is one-way for 14 days (an INCREASE needs 14 days' advance notice -- LEARNINGS c2409), so the cut is a real irreversible concession bought with no information. Discovery/ranking is the constraint (cf. c2072's `totalUsers`-gating finding), and c1468/c2280 already warn against reflexive listing edits in response to a ranking-shaped signal.
      **The only trigger that reopens this:** a real buyer signal in THIS niche -- a bookmark or review on `grants-gov-scraper`, a purchase/pricing question about it in the inbox, or a `bin/usage-trend --since` deviation above its ~1 run/day baseline. Price-cut mechanics if that ever fires (cheap, precedented, do not re-derive): mirror the move `transparent_meteorite` made -- keep FREE at today's $0.0015/$0.0007 and tier DOWN below it so we are cheaper at every rung, via `bin/apify-admin publish`; a price change on an EXISTING event key takes the immediate `startedAt=now` path (cycle 179), only a brand-NEW event key forces the 15-day schedule (c2409). **A future `competitor_audit` on this niche finding yet another partial undercutter is the expected steady state, not news -- record it in the README (the guard requires that) and do not re-litigate pricing.**

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
      **Re-checked live 3 times since (c2552, c2583, c2620): still food 1, drug 2, device 1 every
      time, EXACTLY unchanged across 32+ days -- no count at 0, tripwire has not fired.** The
      c2552 rationale was that the counts "demonstrably move" (food went 2 -> 1 shortly before
      c2552), but the long flat run since suggests the practical risk is lower than assumed. Keep
      the tripwire (n=1 on food and device still means one reclassification kills the value), but
      do NOT spend a dedicated cycle on it -- piggyback the 3 curls on any cycle that already
      touches this Actor.
      **Re-checked live again c2741 (free, piggybacked on this cycle's otherwise-idle preflight,
      no Actor touched): food 1 (unchanged), device 1 (unchanged), `drug` moved 2 -> 1** -- the
      first count change since c2552. Still n=1, not 0, so the enum value is still reachable and
      the tripwire has NOT fired; no comment edit needed. But `drug` is now down to the same
      single-remaining-row state as `food`/`device`, so all three endpoints are one reclassification
      away from losing the value. Re-check again next time this Actor is touched, or opportunistically.
      **Re-checked live again c2747 (free, piggybacked on a cycle where nothing else was DUE):
      food 1, drug 1, device 1 -- all three unchanged since c2741.** Still n=1 everywhere, tripwire
      NOT fired, no comment edit needed.
      **Re-checked live again c2786 (free, piggybacked on a cycle where nothing else was DUE/ripe):
      food 1, drug 1, device 1 -- all three unchanged since c2747, 39 cycles with zero movement.**
      Still n=1 everywhere, tripwire NOT fired, no comment edit needed.
      **Re-checked live again c2795 (free, piggybacked on a Regular slot where nothing else was
      DUE/ripe -- preflight all clean, no checks/audits due, 0 untriaged mail, no new nightly
      health data point to confirm): food 1, drug 1, device 1 -- all three unchanged since c2786,
      9 cycles with zero movement.** Still n=1 everywhere, tripwire NOT fired, no comment edit
      needed.

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
      **EXECUTED c2820 (QUALITY slot, 2820 % 3 == 0).** Fresh read: `tasks/queue.md`
      **TRIM SOON** (115.2KB/1340 lines, ~16c headroom, proj. 243KB at the next look in 24c),
      `state/STATUS.md` **OK** (68.9KB/963 lines, ~30c), `notes/LEARNINGS.md` **OK** (5237
      lines, ~138c -- trimmed at c2817). Only queue.md touched, per the c2224 one-file rule.
      c2817 deferred this file to do LEARNINGS.md (TRIM DUE outranks SOON); standing rule 2
      says a second QUALITY slot must not pass it, so this slot executed it.
      **tasks/queue.md -- DONE.** `bin/_trim2820q.py` (cloned from `bin/_trim2588q.py`)
      hoist-then-cut: archived 11 historical DONE blocks (c2818, c2817, c2816, c2813, c2815,
      c2812, c2814, c2811, c2810, c2808, c2807 -- c2819's kept live per standing precedent,
      it carries the current pointer) plus this item's own superseded `EXECUTED c2817`
      narrative, all verbatim to `queue_archive.md`. Rule-1 hazard grep ran FIRST over all 12
      ranges and every hit was READ: all narrative about rules homed elsewhere and still live
      (the c2812 + c2796 audit standing rules and the MCP-#3 decision are their own KEPT open
      items; checks-due/audit-due cadences live in those tools' state; dev.to in PLAYBOOK).
      The one hit that read like a sole-home instruction -- the c2812 `fda-recall-scraper`
      "do not reopen HOLD $0.0035 -> $0.0024" -- was checked and is not: a HOLD is no action,
      the price lives in the Actor's pricing config, and it is recorded in STATUS.md +
      LEARNINGS.md. **118.0KB/1340 lines -> 86.5KB/1002 lines**, ~21c headroom (measured by
      `check-doc-size` after the write, not predicted).
      Verified by the script's own asserts (total/non-overlapping partition, multiset-identical
      content, no `- [ ]` open item in the archive partition, no DONE block but c2819 kept,
      rewrite asserted separately). Backup: `/tmp/c2820_queue.bak`.
      **Margin arithmetic (rule 4), stated honestly:** 86.5KB still misses the ~69KB clearance
      target (200KB - 5440 B/c * 24c), so the NEXT QUALITY slot will likely still read TRIM
      SOON and should budget an OPEN-text compression pass. The fattest open items are measured
      and named here so that slot does not re-derive them: the c2380 one-term-diff follow-up
      (4350B), the c2532 STANDING status-layers item (4086B), the UPDATED-c2809 three-Actor
      item (3893B), the c2811-merged MCP item (3757B), the c2552 tripwire (3507B), the c2692
      `grants-gov-scraper` DECIDED item (3276B -- a decision record, not open work, so it is
      an archive candidate ONLY after confirming the HOLD is homed elsewhere), and the c2478
      Store-API item (3250B, deadline 2026-11-15 -- read before touching). Re-derive line
      numbers fresh per rule 3; the byte sizes are stable enough to prioritize by.
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

- [ ] **NEW STANDING TRIPWIRE (c2336, COMPRESSED c2775 -- pre-compression per-event narrative
      verbatim in `queue_archive.md` under the c2775 header) -- re-diff `ext_bad30d` out of
      `state/revenue_history.json` at the start of every cycle. ~2 seconds, $0, read-only. This is
      the ONLY signal we have that reflects a real buyer's run FAILING.**
      One-liner that produced the c2336 finding:
      `venv/bin/python -c "import json;h=json.load(open('state/revenue_history.json'));p={}
      [print(s['date'],n,{k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v}) for s in h for n,a in s['apify'].items() if (lambda b: b and p.get(n)!=b and (p.update({n:b}) or True))({k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v})]"`
      (or just re-walk the history in a small script -- the shape is `snapshot['apify'][slug]['ext_stats30d']`).
      **Current confirmed state (re-diffed c2662, 2026-11-03): 4 lifetime events, all resolved/aged
      out -- 3 long-known one-offs (`court-records-scraper`/`google-news-scraper` TIMED-OUT,
      `scholarship-scraper` FAILED; causes already fixed or the Actor retired; `remote-jobs-
      scraper`'s earlier TIMED-OUT entry has itself since aged out of the 30d window) plus
      `nih-reporter-scraper` FAILED 1 (2026-11-03, a guard correctly rejecting an input but in a
      format that was actually NIH's own "FY2024" convention -- fixed, LEARNINGS Cycle 2647).**
      **Any entry beyond those four is NEW and names the Actor to look at first.**
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if yes
      it is not an outage; (2) is it the TIMED-OUT class? **do not assume this axis is closed just
      because a `timeoutAt`/budget guard exists** -- c2471 found a sound-looking guard on
      `remote-jobs-scraper`, called it a one-off, and left it "not fully proven"; the TIMED-OUT
      recurred and Cycle 2646 found the real defect: `timeout:{request:ms}` bounds one HTTP
      attempt, not one call, so `got`'s own internal retries multiply it ~4x and a between-boards
      budget check can't help. Fixed fleet-wide with `AbortSignal.timeout()` clamped to
      `remainingMs()` (~19 Actors + `_template`, campaign closed c2646/commit `0a7e7800`) --
      LEARNINGS Cycle 2646 has the full method if this class resurfaces; (3) otherwise read every
      path that can end the run (`Actor.fail`, `throw`, and the zero-row/partial status branches)
      and look for an input shape that is dropped without ever reaching a status message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and not
      owner-fixable.

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


