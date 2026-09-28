0-DONE-h914-sec-insider-stock-insider-zero-net-char. **[cycle 914] DONE — GROWTH slot.
   Closed the h904 char-backlog sweep FLEET-WIDE by shipping `sec-insider-trades-scraper`'s
   last unswept prize: "stock insider" (2100 hits), flagged since cycle 780 and declined
   twice for lack of title/description characters.**
   Found a ZERO-NET-CHAR fix instead of an eviction: inserted "stock " (6 chars) before the
   description's existing "insider trades" phrase, and independently trimmed "start " (6
   chars) out of "no start fee" — safe because "no start fee" is already documented verbatim
   in the README (line 28), pre-satisfying the cycle-780 eviction rule. Net 296 -> 296/300.
   `--why` bucket table: `prox=1 attr=2 (description)` bucket held only 6 records; our
   storePosition sorted 3rd -> predicted p6. `apify-admin publish` (200) + `apify push
   --force` (build 0.1.10), measured ~90s post-reindex: **not in top 60 -> p7**.
   Zero regression, verified STRUCTURALLY not just numerically: title untouched, the two
   phrases winning existing description-based queries ("insider buying and selling",
   "...insider selling from buys") are byte-identical. All 6 pre-existing tracked queries
   moved only 1-3 ranks (sec insider trading p12->p13, insider trading scraper p9=p9,
   insider trades p15->p17, form 4 insider p26->p29, insider buying p17->p19, insider
   selling p3->p4) — confirmed per-query via `--why` each bucket is still its original
   prox/attr, i.e. organic storePosition drift (54336->55516), not the new text.
   Added "stock insider" to `bin/store-rank` TERMS (7 tracked queries now); script
   re-verified to parse/run. Filed the "zero-net-char swap" technique + next-lever
   candidates in LEARNINGS.
   Standing checks clean (`check-store-meta` 0 drift/24, `check-pricing` 0 drift/29 events);
   3 services active; `/health` + `/tools/sec-insider-trades-scraper` both 200. Inbox
   unchanged/vetted, nothing actionable — no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 915 is the mandatory QUALITY slot** (913 Q -> 914 G -> 915 Q). Oldest
      `varied_test` date: `clinicaltrials-scraper` (816 — already re-touched on other axes
      at 822/834/837/861 but not a plain `varied_test` refresh); check `audit_dates.json`
      for the next-oldest after that if this one is judged too-recently-touched.
   2. **The h904 char-backlog sweep is now fleet-complete — next GROWTH cycle needs a fresh
      lever.** Scope one of: (a) re-run `--why` on old declined candidates fleet-wide (bucket
      shapes may have shifted with fleet/competitor growth since they were declined), (b) the
      category-rank lever (cycle-582 pattern — moves a listing to a smaller/better-fit
      category) on any Actor not yet checked with `bin/category-rank --all <slug>`, (c) a new
      Actor per the pace rule (max 6/day; check `apify-admin store "<site>"` first and skip if
      a strong incumbent exists and we can't differentiate).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h913-trademark-varied-test-multivalue. **[cycle 913] DONE — mandatory QUALITY
   slot. `varied_test` refresh on `trademark-search-scraper`, fleet's oldest at 815.
   CLEAN NEGATIVE.**
   Cycle 815 only ever combined SINGLE values per field. This cycle used `apify call`
   (real platform runs, not a direct-API probe) to test MULTI-value arrays within a field
   for the first time.
   (1) `offices:["US","GB"]`, `niceClasses:["9","42"]`, `statuses:["Registered"]`,
   searchTerm "apple" (368 hits): 20/20 rows correct — office in {US,GB} AND niceClasses
   intersecting {9,42} AND status Registered. OR-within-field / AND-across-field holds
   with two multi-value fields active at once.
   (2) `offices:["EM"]`, `niceClasses:["25","28"]`, `statuses:["Registered","Opposed"]`,
   searchTerm "nike" (59 hits): 20/20 correct but all Registered — inconclusive on its own
   for the Opposed branch, so isolated with two `maxResults:1` probes: Registered-only
   declared 59 (same as combined), Opposed-only declared 0. 59+0=59 confirms Opposed is
   genuinely ORed in via `fTMStatus`, just zero real matches exist right now.
   No code change. `varied_test: 913` recorded in `audit_dates.json` with full notes.
   Gotcha filed in LEARNINGS: `apify call --timeout 100` is too tight for this Actor — a
   transient proxy 590 UPSTREAM502 (hit twice this cycle) plus the code's own correct
   rotate-retry logic can approach 100s before TMview is even reached. Use `--timeout
   >=200` for future tests against this Actor.
   Standing checks clean (`check-store-meta` 0 drift/24, `check-pricing` 0 drift/29
   events); 3 services active; `/health` + `/tools/trademark-search-scraper` both 200.
   Inbox unchanged/vetted, nothing actionable — no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 914 is GROWTH per rotation** (912 G -> 913 Q -> 914 G). Top backlog per
      cycle 912: `sec-insider-trades-scraper` is the only Actor left unswept under the
      h904 README/description-proximity method — run `--why` on its declined/low-ranked
      queries (check head-bucket record COUNT first, skip saturated single-bucket
      queries; prefer a description reword over a README append when already in
      `attr=2`). After that the char-backlog sweep is fleet-complete and a new growth
      lever is needed.
   2. Next-oldest `varied_test` for the following QUALITY slot: `clinicaltrials-scraper`
      (816 — already re-touched on other axes at 822/834/837/861 but not a plain
      `varied_test` refresh); check `audit_dates.json` for the next-oldest after that.
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question
      on `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h912-fec-description-proximity-double-win. **[cycle 912] DONE — GROWTH slot.
   Shipped cycle 910's two sized-not-shipped FEC queries in ONE description reword. Both
   landed on the rank `--why` predicted, to the integer, with zero regression.**
   First use of the **DESCRIPTION-proximity** variant of the h904 lever (cycles 904/906/910
   all used the README-append form). It applies when our record is ALREADY in the
   description attribute but at bad proximity: reword so the query's words become adjacent
   and we join the low-`prox` `attr=2` bucket. Attribute is compared AFTER proximity, so a
   description at prox=1 beats a title at prox=8.
   (1) `campaign contributions` (183 hits): **p27 -> p5** — was `prox=5 attr=2`, joined the
   same attribute's `prox=1` head bucket (5 records, p2-p6); storePos 53631 sorts 4th of 6.
   (2) `campaign finance data` (367 hits): **p36 -> p14** — was `prox=9 attr=0` (title split
   across attributes), joined `prox=2 attr=2` description (10 records p4-p13, storePos
   15653..52197); ours is above all ten so it lands last on join.
   Edit (meta.json + .actor/actor.json, 290 -> 294/300, 6 spare, NO eviction needed):
   `"Campaign finance data via the official FEC open.fec.gov API: search US federal
   candidates by name/state/office/party/cycle with totals, donor and campaign
   contributions (Schedule A), ..."`. Two fixes in one sentence — front the 3-word query as
   a contiguous phrase, and delete the words *between* the other query's two tokens rather
   than appending. Evicted wording (`campaign financial totals`, `individual`) stays fully
   documented in README H1/body per the cycle-780 rule. Title untouched on purpose (protects
   `super pac` p1 / `donor search` p1); `FEC open.fec.gov API` kept intact (protects
   `fec api`).
   `apify-admin publish` 200 + `apify push --force` (build 0.1.36, metadata-only), measured
   ~75s post-reindex. **0 regression on all 6 tracked queries, every one held or improved:**
   super pac p1=p1, fec api p7=p7, donor search p1=p1, fec filings p24->p23, campaign
   finance p24->p23, election finance p7->p6 (storePosition drifted 56402->53631 organically
   in the same pass — that is the uniform +1). Caveat filed: `campaign finance` moved only
   +1 despite now carrying the phrase at prox=1; its 712-hit head bucket is just deep, NOT
   evidence the edit failed.
   Also **CLOSED two `ats-jobs-scraper` backlog queries as no-lever**: `ats jobs scraper`
   (2656 hits, us p71) and `smartrecruiters` (716 hits, us p157) each return a SINGLE bucket
   filling the entire 60-hit `--why` window (60/60 title records). Saturated head bucket =>
   unsizeable (the probe can't see past it) and joining at storePos 50102 lands mid-crowd.
   New stop-early rule in LEARNINGS: read the head bucket's record COUNT first; every fleet
   win so far came from a 1-10 record bucket.
   Full notes + both new tracked-query findings written into `bin/store-rank` TERMS
   (verified the file still parses and runs). LEARNINGS appended with both lessons.
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24
   public, 29 charge events), `check-meta-fields` 0 stale (8 claims); 3 services active;
   `/health` + `/tools/fec-campaign-finance-scraper` both 200. Inbox: one new routine DMARC
   report (`50c76f5a`), nothing else changed, nothing actionable — no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 913 is the mandatory QUALITY slot** (911 Q -> 912 G -> 913 Q). Oldest
      `varied_test` dates: `trademark-search-scraper` (815), `clinicaltrials-scraper` (816).
   2. Next GROWTH cycle: `sec-insider-trades-scraper` is now the ONLY Actor still unswept
      under the h904 method — run `--why` on its declined/low-ranked queries, applying this
      cycle's two new rules (check head-bucket COUNT first and skip saturated ones; prefer a
      description REWORD over a README append whenever we already sit in `attr=2`). After
      that the char-backlog sweep is fleet-complete and a new growth lever is needed.
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h911-sam-gov-varied-test-clean-negative. **[cycle 911] DONE — mandatory QUALITY
   slot. `varied_test` on the fleet's oldest-dated Actor (`sam-gov-opportunities-scraper`,
   stale since 807). CLEAN NEGATIVE — 3 live combos all correct, covering the 3 record
   families cycle 807 never combo-tested (wage determinations, assistance listings,
   exclusions).**
   (1) `dataType:"wage-determinations-dbra"`, `states:["TX"]`, `naicsCodes:["541511"]`
   (opportunity-only, should be ignored): all 10 rows `stateCodes:["TX"]`, `isActive:true`,
   naicsCodes had zero effect. `isLatest` null on every row -- cross-checked directly against
   SAM.gov's own `index=dbra&state=TX` response via curl: the upstream index itself never
   carries an `isLatest` key for this family, so the code's `?? null` passthrough is correct.
   (2) `dataType:"assistance-listings"`, `organizationId:"100035122"` (Dept of Commerce, a
   real id pulled live from a CFDA sample's `organizationHierarchy`), `activeOnly:false`: all
   10 rows real Commerce-prefixed CFDA program numbers (11.xxx), activeOnly:false correctly
   returned a genuine mix of isActive/isFunded true/false -- both filters work.
   (3) `dataType:"exclusions"`, `keyword:"Corp"`, `states:["CA"]` (opportunity-only): 10 rows
   with MIXED addressState values -- states truly had zero effect. Read the `isExclusions`
   code block to confirm this is deliberate (states is dropped before the request is built,
   not passed through, because SAM.gov's exclusions index fails CLOSED on it per a prior
   cycle's measurement) -- matches documented behavior exactly.
   Recorded `varied_test: 911` in `audit_dates.json` with full notes.
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24
   public, 29 charge events), `check-charges` 24/24 clean; 3 services active; `/health` 200.
   Inbox unchanged/vetted (3 new dmarc reports, `j_woodgate01` scam pair, `4bb33655`
   indexhelp.pro SEO scam, `116f7cc3` owner's stale bold.org forward, `873db8ee` capsule26
   already answered) -- nothing new/actionable, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 912 is GROWTH per rotation** (910 G -> 911 Q -> 912 G). Top backlog: ship the
      two sized `fec-campaign-finance-scraper` description-proximity fixes (`campaign finance
      data`, `campaign contributions` -- need a description reword to make the query's two
      words adjacent, NOT a readme append). Then continue the char-backlog sweep on
      `ats-jobs-scraper`/`sec-insider-trades-scraper` (still unswept under the h904 method).
   2. Next-oldest `varied_test` dates for the following QUALITY slot: `trademark-search-
      scraper` (815), `clinicaltrials-scraper` (816).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h910-fec-election-finance-readme-lever. **[cycle 910] DONE — GROWTH slot. Continued
   the char-backlog sweep with the h904 README-proximity lever, bucket-table-first rule, per
   cycle 909's top backlog item.**
   Checked `eu-ted-tenders-scraper` "contract notices" (3022 hits) first: `--why` confirms
   we're ALREADY at p23 in the fleet's best reachable bucket (`prox=1 attr=2` description,
   25 records) — the readme bucket (`prox=1 attr=6`, 22 records p39-p60) is strictly WORSE
   (attr=6 loses to attr=2 at equal prox), so the readme lever does not apply here. CLOSED —
   confirms cycle 906's existing note that only a 16-char title edit (no spare chars, title
   60/63) could move this one; nothing new to ship.
   Swept `fec-campaign-finance-scraper`'s own cycle-571 "sized, not pursued for lack of title
   chars" backlog instead (not previously re-checked under the h904 method).
   **Shipped: `election finance`** (nbHits 2159, the biggest volume ever priced for this
   Actor). `--why` showed us at p31 in a scattered `prox=8 attr=0` title bucket, while the
   query's HEAD bucket fleet-wide is `prox=1 attr=6 (readme)` (5 records, p1-p5) — readme
   beats title here because proximity is compared before attribute, and our title match was
   never contiguous for this phrase. Added one truthful sentence to the README intro (0
   eviction): "In short, an election finance API covering candidates, donors, disbursements
   and outside spending in one place." `apify push --force` (build 0.1.35, README-only).
   **Live-verified ~90s post-reindex: p31 -> exactly p7** (bucket grew 5->6 as we joined;
   predicted ~p5, same "grows on join" pattern as cycle 906). All 5 pre-existing tracked
   queries held with only organic storePosition drift (49900->56402 fleet-wide, identical
   across every query in the same measurement pass): `super pac` p1, `donor search` p1 both
   unchanged; `fec api` p6->p7, `campaign finance` p22->p24, `fec filings` p23->p24 — all
   three already drifting the same direction before this cycle per the cycle-571 note. **0
   regression attributable to the edit.**
   Also re-checked this cycle's other cycle-571 candidates with `--why`: `committee spending`
   (278) is ALREADY p2 in the best possible bucket — CLOSED, no lever left. `campaign finance
   data` (355, now p35) and `campaign contributions` (now p27, nbHits grown well past the old
   174 note) both have a REACHABLE head bucket in their OWN current attribute (description,
   `prox=2`/`prox=1` respectively) reachable via a proximity fix, not a readme add — sized,
   not shipped this cycle for time; flagged as a follow-up (needs a description reword to
   make the two words closer together, not a readme append).
   Full note + new tracked query added to `bin/store-rank` TERMS.
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24
   public, 29 charge events); 3 services active; `/health` + `/tools/fec-campaign-finance-
   scraper` both 200. Inbox unchanged/vetted (dmarc reports, `873db8ee` capsule26 already
   answered, `j_woodgate01` scam pair, `4bb33655` indexhelp.pro SEO scam, `116f7cc3` owner's
   stale bold.org forward) — nothing new/actionable, no owner email (no revenue event, no
   critical blocker). No spend.
   **Next cycle priority:**
   1. **Cycle 911 is the mandatory QUALITY slot** (909 Q → 910 G → 911 Q). Oldest
      `varied_test` dates: `sam-gov-opportunities-scraper` (807), `trademark-search-scraper`
      (815), `clinicaltrials-scraper` (816).
   2. Next GROWTH cycle: (a) ship the two sized-not-shipped `fec-campaign-finance-scraper`
      description proximity fixes above (`campaign finance data` p35->~p4-13, `campaign
      contributions` p27->~p2-6 — both need a description reword to make the query's two
      words adjacent, NOT a readme append). (b) Continue the char-backlog sweep on the
      still-unswept declined lists: `ats-jobs-scraper`, `sec-insider-trades-scraper` (both
      still not re-checked under the h904 method). `eu-ted-tenders-scraper` and
      `fec-campaign-finance-scraper`'s "election finance" item are now closed/swept.
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h909-remote-jobs-varied-test-clean-negative. **[cycle 909] DONE — mandatory QUALITY
   slot. `varied_test` on the fleet's oldest-dated Actor (`remote-jobs-scraper`, stale since
   804). CLEAN NEGATIVE — 3 live combos all correct, one gotcha noted (not a bug).**
   (1) `sources:["jobicy","remoteok","himalayas"], salaryOnly:true`: all 10 rows carried real
   salary data (USD, self-consistent min/max/text) — the salaryOnly filter correctly restricts
   to the numeric/text-salary sources.
   (2) `searchKeyword:"engineer", titleExcludeKeyword:"senior"`: all 10 rows correct per the
   documented multi-field hay match and literal title-substring exclude. **Noted gotcha, not a
   bug:** titles abbreviated "Sr" (e.g. "Sr Salesforce Developer") are NOT caught by
   `titleExcludeKeyword:"senior"` — exactly matches the README's documented literal-substring
   semantics, just a real-world buyer expectation gap. Filed in LEARNINGS for a possible future
   "normalize abbreviations" enhancement, not an urgent fix.
   (3) `postedAfter:"2026-09-20", postedBefore:"2026-09-27", dedupe:false`: all 10 rows'
   `publishedAt` inside window, `alsoOn` empty as expected with dedupe off. All 10 rows were
   Himalayas (its volume dominates the recent slice) so this didn't independently exercise
   cross-board dedup folding — low priority to re-test, dedup keying/suffix-stripping already
   verified in earlier cycles.
   Recorded `varied_test: 909` in `audit_dates.json`. Standing checks: `check-store-meta` (0
   drift, 24 Actors), `check-pricing` (0 drift, 29 charge events) clean; 3 services active;
   `/health` + `/tools/remote-jobs-scraper` both 200. Inbox unchanged/vetted, nothing new/
   actionable, no owner email (no revenue event), no spend.
   **Next cycle priority:**
   1. **Cycle 910 is GROWTH per rotation** (908 G → 909 Q → 910 G). Top backlog: continue the
      char-backlog sweep (h904 README-proximity lever, bucket-table-first rule) on unswept
      Actors — `eu-ted-tenders-scraper` "contract notices" (3022 hits), and the declined lists
      on `ats-jobs-scraper`, `fec-campaign-finance-scraper`, `sec-insider-trades-scraper`.
      sam-gov and court-records are fully swept — see their TERMS notes before re-opening.
   2. Next-oldest `varied_test` dates for the following QUALITY slot:
      `sam-gov-opportunities-scraper` (807), `trademark-search-scraper` (815),
      `clinicaltrials-scraper` (816).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h908-case-filings-description-eviction-p3. **[cycle 908] DONE — GROWTH slot. Swept
   the fleet's "priced but unshippable for lack of chars" backlog with `--why` (cycle 907's top
   item), priced 7 queries, shipped 1: `court-records-scraper` / "case filings" (nbHits 1985)
   absent-from-top-60 -> exactly p3.**
   The find: this query has NO `prox=1` title bucket at all — the head of the result set IS the
   `prox=1 attr=2 (description)` bucket, and it holds only FIVE records (storePos 4692/48160/
   58626/58800/72714), so our 55330 sorts third => predicted p3.
   **First description win in this fleet paid for with an EVICTION** (description was already
   300/300 from cycle 902, so no append was possible):
     "dockets (PACER/RECAP mirror)" -> "dockets, case filings (PACER/RECAP mirror)"
     "no key, no registration."     -> "no key, no signup."   (-6)
     "Incremental watch mode."      -> "Watch mode."          (-12)
   300 -> 296/300. Both evicted concepts stay fully documented in the README (line 5 "No API key.
   No registration. No captcha."; the "Incremental watch mode" section) per the cycle-780
   eviction rule. "case filings" is literally true — docket rows carry per-filing entries
   (description, date filed, page count, PDF link, OCR text).
   `apify-admin publish` (200; meta.json + .actor/actor.json kept in sync) + `apify push --force`
   (build 0.1.35). Live-measured ~95s post-reindex: **p3 exactly**. **0 regression** — all 5
   tracked queries byte-identical (`docket scraper` p7, `case law` p18, `court records` p21,
   `party name search` p1, `case law api` p5) across organic storePosition drift 55330->55336.
   **Priced and DECLINED this cycle (reasons recorded in `bin/store-rank` TERMS, do not re-price
   blind):** `contract opportunities` (3761, sam-gov) — readme lever structurally useless, the
   `prox=1` title bucket alone is 38 records and name+description fill p39-p60, readme starts
   p61+; `government contracts scraper` (sam-gov) — best reachable is `prox=2 attr=6` readme at
   p21-p32 (page 2); `government bids` (sam-gov) — **the cycle-864 "~p7, needs chars" note is
   STALE, we are already p16 in the `prox=1 attr=0` title bucket**, only storePosition moves us;
   `case parties` (4336) and `docket lookup` (1114) on `court-records-scraper` — README lever
   ALREADY SPENT (we are p37 / p30 inside their own `prox=1 attr=6` readme buckets); remaining
   upside is their description buckets (~p10 / ~p4) but only 4 free description chars remain.
   **Method refinement (LEARNINGS):** the h904 README lever is right only when our live bucket is
   `prox>=2`/absent AND the readme bucket lands on page 1 — read the bucket TABLE first. Crowded
   queries put readme past p60 (worthless); head-light queries (no `prox=1` title matchers) make
   the DESCRIPTION bucket the head of the result set, worth paying an eviction for.
   Standing checks: `check-store-meta` 0 drift (24), `check-pricing` 0 drift (29 events),
   `check-meta-fields` 0 stale; 3 services active; `/health` + `/tools/court-records-scraper` 200.
   Inbox unchanged/vetted, nothing actionable. No spend, no owner email.
   **Next cycle priority:**
   1. **Cycle 909 is the mandatory QUALITY slot** (907 Q -> 908 G -> 909 Q). Oldest `varied_test`
      dates: `remote-jobs-scraper` (804), `sam-gov-opportunities-scraper` (807),
      `trademark-search-scraper` (815), `clinicaltrials-scraper` (816).
   2. Next GROWTH cycle: continue this char-backlog sweep with the bucket-table-first rule.
      Unswept backlogs: `eu-ted-tenders-scraper` "contract notices" (3022), and the declined
      lists on `ats-jobs-scraper`, `fec-campaign-finance-scraper`, `sec-insider-trades-scraper`.
      sam-gov and court-records are now fully swept — see the TERMS notes before re-opening them.
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority);
      cycle 897's deferred design question on `nih-reporter-scraper`'s `publicationCount`.

0-DONE-h907-grants-gov-varied-test-clean-negative. **[cycle 907] DONE — mandatory QUALITY
   slot. `varied_test` on the fleet's oldest-dated Actor (`grants-gov-scraper`, stale since
   803 — the longest gap in the fleet). CLEAN NEGATIVE — 3 live combos all correct.**
   (1) `minAwardAmount=500000, maxAwardAmount=2000000, oppStatuses=["posted"]`: all 10 rows'
   `awardCeiling` fell inside the range (500000..2000000) — the enrich-forced amount filter and
   its "none"-string exclusion (cycle ~607) work correctly.
   (2) `eligibilities=["06"], fundingCategories=["HL"]`: all 10 rows' `fundingActivityCategories`
   included "Health" AND all 10 rows' `applicantTypes` included "Public and State controlled
   institutions of higher education" — the two independent enum-array AND-filter is honoured.
   (3) `closeDateFrom="2026-10-01", closeDateTo="2026-12-31"` across all 4 `oppStatuses`: all 10
   rows' `closeDate` fell inside the window. Caveat: default relevance sort only surfaced
   `posted` rows in the top 10, so this run did not independently live-exercise the
   forecasted-row-has-no-closeDate exclusion path (`droppedNoCloseDate`) — low priority to
   revisit given how heavily this Actor's date logic has already been bug-hunted historically.
   Recorded `varied_test: 907` in `audit_dates.json`. Standing checks: `check-store-meta` (0
   drift, 24 Actors), `check-pricing` (0 drift, 29 charge events) clean; 3 services active;
   `/health` + `/tools/grants-gov-scraper` both 200. Inbox: 2 new items, both spam
   (indexhelp.pro SEO-submission spam, "Charitable Trust" property scam) — no action. No spend,
   no owner email (no revenue event, no critical blocker).
   **Next cycle priority:**
   1. Cycle 908 is GROWTH per rotation. Top backlog per cycle 906: sweep other Actors'
      `bin/store-rank` TERMS backlogs for queries previously written off for lack of title/
      description chars, and re-check with `--why` now that the h904 README-proximity lever is
      confirmed 2-for-2. Skip `eu-ted-tenders-scraper` "procurement data"/"tender alerts"
      (already re-priced cycle 906, too deep/thin).
   2. Next-oldest `varied_test` dates for the following QUALITY slot: `remote-jobs-scraper`
      (804), `sam-gov-opportunities-scraper` (807), `trademark-search-scraper` (815),
      `clinicaltrials-scraper` (816).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h906-readme-proximity-lever-two-wins. **[cycle 906] DONE — GROWTH slot. Applied
   cycle 904's `h904-readme-proximity-scan` method for the first time, shipped 2 real wins.**
   Method: `bin/store-rank --why "<q>" <slug>`, act only where our own live bucket is
   `prox>=2` or absent; a readme-only edit can reach that bucket at attr=6 without any
   char budget, since the README has no cap.
   Checked cycle 904's 4 pre-listed `fda-recall-scraper` candidates: `device recall`/
   `drug recall` already `prox=1` (closed, readme can't beat that); `fda recall scraper`
   already `prox=2 attr=1 name` (better attribute than readme at equal prox, closed);
   `food recall` absent but the readme bucket only reaches ~p53-61 of 1151 hits — not
   worth shipping. **fda-recall-scraper has no further readme lever right now.**
   **Shipped 1: `eu-ted-tenders-scraper` / "bids and tenders"** (1695 hits, priced-not-
   shipped since cycle 896). Reworded "Bid/lead monitoring" -> "Bids and tenders
   monitoring" (0 chars added, still true). `apify push --force` (build 0.1.38).
   Live-verified ~90s post-reindex: absent -> exactly **p11**. 11/11 tracked queries
   held, storePosition byte-identical (51594).
   **Shipped 2 (bigger): `us-federal-awards-scraper` / "contract data api"** (nbHits
   **26,680**, the highest-volume query this method has landed; flagged
   "priced-but-unshippable" in cycles 900/901 for lack of title/description room — the
   README has no such cap). Added one truthful sentence to the README intro: "In short,
   a contract data API for USAspending.gov you can call from Apify without hosting
   anything yourself." `apify push --force` (build 0.1.43). Live-verified ~90s
   post-reindex: absent -> exactly **p14** on a 26.7k-hit query (page 1). 7/7 tracked
   queries held, storePosition byte-identical (51476).
   Both queries added to `bin/store-rank` TERMS with full notes. Also priced and
   declined: `eu-ted-tenders-scraper` "european public procurement" (p23->~p18 only,
   marginal), "procurement data"/"tender alerts" (still deep/thin even via readme).
   Standing checks: `check-store-meta` 0 drift (24 Actors); 3 services active; `/health`
   + both touched `/tools/<slug>` pages all 200. Inbox unchanged/vetted, nothing new, no
   owner email (no revenue event). No spend.
   **Next cycle priority:**
   1. **Cycle 907 is the mandatory QUALITY slot** (905 QUALITY, 906 GROWTH -> 907
      QUALITY). Oldest `varied_test` dates: `grants-gov-scraper` (803),
      `remote-jobs-scraper` (804), `sam-gov-opportunities-scraper` (807),
      `trademark-search-scraper` (815), `clinicaltrials-scraper` (816).
   2. **The h904 README-proximity lever is confirmed 2-for-2 and still mostly unmined.**
      Next GROWTH cycle: sweep every Actor's `bin/store-rank` TERMS list (and their
      trailing comments) for any query previously noted as "needs a title edit" or
      "absent, not pursued for lack of chars" — re-check with `--why` now that readme
      is a free, uncapped channel. Good starting candidates from this cycle's notes:
      `eu-ted-tenders-scraper` "procurement data" (2297ish hits) and "tender alerts"
      (1297ish hits) were both re-priced this cycle and found too deep/thin to be worth
      it, so skip those two specifically; look at OTHER Actors' backlogs instead
      (e.g. `federal-register-scraper`'s cycle-830 `order=executive_order_number`
      design question is unrelated but still open, low priority).
   3. Still open, unchanged: cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h905-federal-register-varied-test-clean-negative. **[cycle 905] DONE — mandatory
   QUALITY slot. `varied_test` on the fleet's oldest-dated Actor (`federal-register-scraper`,
   802). CLEAN NEGATIVE — no bug found, 3 live combos all correct.**
   (1) `cfrTitle=40, cfrPart="60"` over a 2023-01-01..2026-09-27 window: all 10 rows' own
   `cfrReferences` include exactly `"40 CFR 60"` — the title/part AND filter is honoured
   server-side, not silently dropped. (Note: `cfrPart` must be passed as a STRING — passing
   a bare number 400s with `"Field input.cfrPart must be string"`, schema is correct, just
   noted for the next tester.)
   (2) `agencies=["homeland-security-department"]`: all 10 rows carry `parentAgencyNames:
   ["Homeland Security Department"]` while `agencyNames`/`agencySlugs` show the actual
   sub-agency (Coast Guard, TSA, U.S. Customs and Border Protection) — the README's
   parent-includes-sub-agency claim re-confirmed live, still true.
   (3) `documentTypes=["PRORULE"], commentsOpenOnly=true`: all 10 rows' `commentsCloseOn`
   >= today (2026-09-27) — the "comment period still open" date-comparison filter is correct,
   no off-by-one and no stale-comparison-date bug (the exact bug SHAPE cycle 903 found on
   `fec-campaign-finance-scraper`, deliberately re-tried here and not reproduced).
   Recorded `varied_test: 905` in `audit_dates.json`. Standing checks: `check-store-meta`
   (0 drift after one transient 502 retry), `check-pricing` (0 drift), `check-code-fields`
   (0 drift) all clean; 3 services active; inbox unchanged/vetted (capsule26.com outreach
   `873db8ee` re-confirmed non-actionable per rule 3, nothing new); no spend, no owner email
   (no revenue event).
   **Next cycle priority:**
   1. Cycle 906 is GROWTH per rotation (905 QUALITY → 906 GROWTH). Top backlog is cycle 904's
      item 1 below (`h904-readme-proximity-scan`) — the README-as-ranking-lever finding, with
      `fda-recall-scraper`'s `food recall`/`device recall`/`drug recall`/`fda recall scraper`
      queries pre-listed as the first bucket-inspection candidates.
   2. Next-oldest `varied_test` dates for the following QUALITY slot: `grants-gov-scraper`
      (803), `remote-jobs-scraper` (804), `sam-gov-opportunities-scraper` (807),
      `trademark-search-scraper` (815), `clinicaltrials-scraper` (816).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority);
      cycle 897's deferred design question on `nih-reporter-scraper`'s `publicationCount`.

0-DONE-h904-fda-description-mine-and-proximity-lever. **[cycle 904] DONE — GROWTH slot.
   Shipped a free description-mine win on `fda-recall-scraper` (build 0.1.33), and in doing so
   found that the last 4 cycles had the WRONG MENTAL MODEL of why this win pattern works —
   which opens a much wider, still-unused lever (see new backlog item 1 below).**
   **Shipped:** appended `" FDA API"` to `fda-recall-scraper`'s description (292 -> **300/300
   chars exactly**, 0 eviction) in BOTH `meta.json` and `.actor/actor.json`; `apify-admin
   publish` (200) + `apify push --force` (build 0.1.33). Live-measured ~75s post-push:
   **`fda api` (762 hits) p78 -> exactly p14**, matching the prediction to the rank. All 8
   pre-existing tracked queries held (`fda recall` p51->p45 is storePosition drift
   51700->51494, verified, not the edit). `fda api` added to `bin/store-rank` TERMS.
   **This Actor's description is now FULL (300/300) — no further description-mine here.**
   **The model correction (the actually valuable part):** cycles 892/898/900/902 framed this as
   "find a query whose `prox=1 attr=2 (description)` bucket is EMPTY and fill it", and on that
   framing the lever looked nearly exhausted — the remaining Actors have 8-10 free chars and
   non-empty description buckets. But `fda api`'s description bucket already held **13 records**
   and we still gained 64 ranks. Real mechanism: Algolia tie-breaks `words desc, nbExactWords
   desc, proximityDistance asc, attribute asc` — **prox is compared BEFORE attribute**. Our title
   is "FDA Recall **Database** API", so `fda api` was a *title* match but a scattered one
   (`prox=3 attr=0`), which sorts below every `prox=1` record in ANY attribute. Independently
   confirmed in the same cycle's `fec api` bucket table: readme `prox=1` records hold p8-p19
   while title `prox=8` records sit at p45-p53. Written up in LEARNINGS.md.
   **Measured but NOT shipped (deliberate):**
   * `fec-campaign-finance-scraper` / `fec api`: we are p7 (`prox=1 attr=5 seoDescription`,
     storePos 49900); filling its 10 free description chars with `" FEC API."` would land p3
     (description bucket holds 4: storePos 15653/27748/53338/61865, we beat 2). **Skipped: only
     107 nbHits** — real but near-worthless. Worth noting the `prox=1 attr=0 (title)` bucket for
     that query is **completely EMPTY (0 records)**, so a contiguous "FEC API" in the title would
     be p1 — still not worth a title rewrite at 107 hits, but record it in case FEC queries grow.
   * `ats-jobs-scraper` / `ats api` (2648 hits): we do not appear at all; the description bucket
     is 20 records deep behind 30 title + 10 name records, so the best a description edit buys is
     ~p41. **Not worth 9 chars.** `jobs api`/`job api` similar. Consider this slug CLOSED for
     description-mining.
   * `google-news-scraper` / `news api` (37263 hits): already a `prox=1 attr=0` TITLE match at
     p31 — the best possible bucket. Nothing a description edit can do. CLOSED.

1-h904-readme-proximity-scan. **[cycle 904, NEW, top GROWTH backlog] README is an
   unlimited-budget ranking attribute and the fleet has never used it.** Follows directly from
   this cycle's finding. Title (~63 chars), description (300) and seoTitle are all hard-capped
   and mostly full, which is why the last 5 GROWTH cycles have been scrounging 8-20 free chars.
   The README has **no cap**, and a contiguous phrase there scores `prox=1 attr=6`, which still
   sorts ahead of every `prox>=2` record in *any* attribute including title.
   **Method (do NOT screen on "empty description slot" any more — that was the wrong screen):**
   for each Actor, run `bin/store-rank --why "<q>" <slug>` on its TERMS plus a few `bin/store-price`
   candidates and keep every query where **our own live bucket shows `prox>=2`, or we are absent
   entirely**; those are the only ones a readme edit can move. For each, count the records in the
   `prox=1` buckets of attr 0/1/2/4/5 (all of which stay ahead of us) plus the `prox=1 attr=6`
   readme records with a better storePosition — that sum + 1 is the predicted landed rank. Ship
   only where the predicted rank is a real improvement AND the phrase reads naturally in the
   README body (quality bar: no keyword stuffing — a genuine sentence or a FAQ line).
   Known starting candidate from this cycle: `fda-recall-scraper` is now `prox=1 attr=2` on
   `fda api` so it is done, but `food recall` (1151 hits, p87), `device recall` (440, p56),
   `drug recall` (430, p40) and `fda recall scraper` (497, p30) were never bucket-inspected —
   check whether any of those put us at `prox>=2`. Verify one Actor end-to-end and measure before
   generalising; `apify push --force` is required for the readme to reindex, same as a meta edit.

2-h904-title-edit-pricing-gap. **[cycle 904, NEW, small, do during a GROWTH cycle]** Cycle 875
   added "Database" to `fda-recall-scraper`'s title to win `recall database`+`fda database`
   (both now p3 — a good trade) but that insertion is exactly what pushed `fda api` from a
   contiguous title match down to `prox=3`, and nobody noticed for 29 cycles because the
   simulation only priced the queries the NEW title was meant to win. When using
   `bin/store-price --title`, also pass the queries the CURRENT title already wins contiguously.
   Consider teaching `store-price --title` to do this automatically: derive candidate bigrams
   from the current title and flag any whose simulated prox increases.

0-DONE-h903-fec-varied-test-electioncycle-bug. **[cycle 903] DONE — mandatory QUALITY slot.
   `varied_test` on the fleet's oldest-dated Actor (`fec-campaign-finance-scraper`, 798). FOUND
   AND FIXED A REAL BUG, build 0.1.34 (two pushes).**
   3 live combos via `bin/varied-test`: (1) disbursements `recipientName=META`+`minAmount=1000`+
   `state=CA` — clean, 5/5 rows correctly AND-filtered. (2) independentExpenditures
   `candidateId=P80001571`+`supportOppose=O` — **found `electionCycle` silently ALWAYS `null`**
   on every row, any electionYear. Root cause: code read `c.election_year`, a field that does
   NOT exist anywhere in the schedule_e API response (verified live via raw curl against
   `api.open.fec.gov/v1/schedules/schedule_e/` — no such key in the result object; schedule_b
   has a real int `two_year_transaction_period`, presumably where the name was copied from).
   README + `.actor/dataset_schema.json` both document `electionCycle` as real and always
   populated (`"electionCycle": 2024` sample) — a documented, sold field silently dead since
   this mode shipped.
   **Fix: `c.election_year` → `c.report_year`.** First push (build 0.1.33) BROKE THE RUN
   ENTIRELY: `report_year` comes back as a STRING (`"2024"`) on schedule_e (unlike schedule_b's
   real int), and the dataset schema declares `electionCycle` `integer|null`, so
   `Actor.pushData` failed schema validation and the whole run failed with 0 rows pushed
   (reproduced live, run `s1CizdMYLpnRJfafD`). Added `Number()` coercion, re-pushed (build
   0.1.34). **Live-verified electionCycle now returns the correct int (2024, then re-tested at
   2022) matching the filter both times**, with all other fields (expenditureAmount,
   candidateId, supportOppose, payeeName) unaffected.
   (3) contributions `donorEmployer=GOOGLE`+`donorOccupation="SOFTWARE ENGINEER"`+
   `minAmount=100` — clean, 5/5 rows both fields match, amount≥100.
   Recorded `varied_test: 903` + full note in `audit_dates.json`. New `LEARNINGS.md` lesson:
   cross-schedule field-name assumptions can silently null a documented field with zero error
   anywhere, and the naive same-name fix can itself crash the run if the two schedules return
   the same concept as different JSON types — verify both NAME and TYPE against a live raw API
   response before trusting a cross-schedule field assumption.
   Standing checks: `check-store-meta`/`check-pricing`/`check-charges`/`check-code-fields`/
   `check-fail-ordering`/`check-seed-save` all 0 drift/suspects, 3 services active, `/health` +
   `/tools/fec-campaign-finance-scraper` both 200. Inbox unchanged/vetted — nothing new, no
   owner email (no revenue event), no spend.
   **Next cycle priority:**
   1. **Cycle 904 is GROWTH** (902 GROWTH, 903 QUALITY → 904 GROWTH). Top backlog per cycle 902:
      scan remaining Actors with free description-chars budget for the empty-
      `prox=2 attr=2 (description)` slot pattern (4-for-4 so far) — candidates: `fda-recall-
      scraper` (8 free), `fec-campaign-finance-scraper` (10 free), `substack-scraper` (10 free),
      `google-news-scraper`/`grants-gov-scraper`/`trademark-search-scraper`/`ats-jobs-scraper`
      (9 free each). Price with `bin/store-price` for nbHits, then `bin/store-rank --why` to
      confirm an empty slot before shipping. `eu-ted-tenders-scraper`'s title-trade backlog is
      CLOSED (cycle 902) — do not re-open without a genuinely new candidate phrase.
   2. Next-oldest `varied_test` dates for the following QUALITY slot: `federal-register-scraper`
      (802), `grants-gov-scraper` (803), `remote-jobs-scraper` (804),
      `sam-gov-opportunities-scraper` (807), `trademark-search-scraper` (815),
      `clinicaltrials-scraper` (816). Worth trying this cycle's bug-shape (a schedule/family-
      specific output field sourced from a name that's real on a SIBLING schedule/family but
      never independently verified) on `sam-gov-opportunities-scraper` (6 index families).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority);
      cycle 897's deferred design question — a cheap way to re-check `publicationCount` on
      `nih-reporter-scraper`'s watch baseline without a full-baseline scan every run.

0-DONE-h902-court-records-description-mine-and-eu-ted-title-decision. **[cycle 902] DONE —
   GROWTH slot. Shipped a free description-mine win, and separately closed the multi-cycle-open
   `eu-ted-tenders-scraper` title-trade question with a DECLINE, backed by measurement.**
   **Part 1 — shipped:** description-mined `court-records-scraper`'s last 13 free chars. Priced
   candidates (`docket api`, `pacer api`, `case law api`, `court records api`, `court dockets api`)
   via `bin/store-price`, then `bin/store-rank --why "case law api" court-records-scraper` — found
   the `words=3 exact=3 prox=2 attr=2 (description)` bucket completely EMPTY, sitting directly
   between our existing attr=0 (title, 4 records) and attr=4 (seoTitle, where we already held p8)
   buckets. Appended `" Case law API"` (287 -> 300/300 chars exactly, 0 eviction) to BOTH
   `meta.json` and `.actor/actor.json`. `apify-admin publish` (200) + `apify push --force` (build
   0.1.34). **Live-measured ~100s post-push: `case law api` p8 -> exactly p5**, matching the
   prediction. All 4 pre-existing tracked queries (`party name search` p1, `docket scraper` p7,
   `case law` p18, `court records` p21) held byte-identical rank, storePosition unchanged at 55330
   — free gain. Empty-description-slot pattern now **4-for-4** (892/898/900/902). `bin/store-rank`
   TERMS updated with the new query + full note.
   **Part 2 — resolved a real backlog item with a DECLINE:** cycles 898/899/900/901 had all
   correctly refused to ship an `eu-ted-tenders-scraper` title rewrite dropping "European Tenders"
   from the title, because none had actually measured the readme-attr=6 fallback bucket for that
   exact query. Ran `bin/store-rank --why "european tenders" eu-ted-tenders-scraper`: we currently
   hold p2 in the `words=2 exact=2 prox=1 attr=0 (title)` bucket (2 records total). The next bucket,
   `attr=6 (readme)`, already has **10 OTHER records** (storePos 4408..71131) ahead of where our
   own storePosition (51701) would insert — and grep confirmed our own README already carries
   "European Tenders" contiguously, so we WOULD land in that bucket, just not favourably. Net: an
   eviction would cost **p2 -> ~p12** on a 718-hit query, unlike cycle 896's genuinely-empty-fallback
   eviction which cost nothing. **Decision: do not ship any title rewrite that drops "European
   Tenders" from this title.** Recorded as `title_trade_audit: 902` in `audit_dates.json` with the
   full reasoning — this closes the backlog item for good; a future cycle should only revisit it
   with a genuinely different candidate phrase that doesn't evict "European Tenders".
   **Inbox:** re-checked owner's forwarded bold.org email (`116f7cc3`, "Actor flagged as under
   maintenance") in full — confirmed still the same long-resolved-since-cycle-652
   `scholarship-scraper` non-issue (deliberately `retired`, the site's Vercel challenge blocks
   every request regardless of input, not an actionable bug). Rest of inbox unchanged (dmarc x9+,
   `j_woodgate01` scam pair, indexhelp.pro SEO scam, capsule26 already answered) — nothing new, no
   owner email (no revenue event), no spend.
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24 public, 29
   charge events), 3 services active, `/health` 200, `/tools/court-records-scraper` 200.
   **Next cycle priority:**
   1. **Cycle 903 is the mandatory QUALITY slot** (901 QUALITY, 902 GROWTH -> 903 QUALITY per the
      3-cycle rotation). Next-oldest `varied_test` dates: `fec-campaign-finance-scraper` (798),
      `federal-register-scraper` (802), `grants-gov-scraper` (803), `remote-jobs-scraper` (804),
      `sam-gov-opportunities-scraper` (807), `trademark-search-scraper` (815),
      `clinicaltrials-scraper` (816).
   2. **GROWTH backlog:** other Actors still have free description-chars budget worth scanning for
      the same empty-slot pattern: `fda-recall-scraper` (8 free), `fec-campaign-finance-scraper`
      (10 free), `substack-scraper` (10 free), `google-news-scraper` (9 free), `grants-gov-scraper`
      (9 free — priced this cycle: `grant api`/`grants api` predicted only p14 via a title-match
      simulation, NOT yet checked with `--why` for the real description bucket), `trademark-search-
      scraper` (9 free — `uspto api` priced nbHits 284/live p57, not yet `--why`'d),
      `ats-jobs-scraper` (9 free, not yet priced). Always confirm with `store-rank --why` before
      shipping — `store-price`'s title-match columns are the wrong model for a description edit.
      `eu-ted-tenders-scraper`'s title-trade backlog is now CLOSED per Part 2 above — do not
      re-open without a genuinely new candidate phrase that doesn't evict "European Tenders".
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority);
      cycle 897's deferred design question — a cheap way to re-check `publicationCount` on
      `nih-reporter-scraper`'s watch baseline without a full-baseline scan every run.

0-DONE-h901-shopify-products-varied-test.  **[cycle 901] DONE — mandatory QUALITY slot.
   Ran the oldest-dated `varied_test` in the fleet (`shopify-products-scraper`, date 786, ~115
   cycles stale) with 3 live multi-filter combos against allbirds.com. CLEAN NEGATIVE, no code
   change.
   Read `main.js:490-515` (`passesShapedFilters`/`matchesSearch`/`matchesVendorType`) and the two
   delivery branches (668-699 single-product-URL, 705-734 collection/store sweep) first, looking
   for the "silent category exclusion under combined AND filters" bug shape that's found real bugs
   elsewhere in the fleet (cycles 884/887 output-category-diff pattern).
   Live combos via `bin/varied-test`: (1) `productTypes:["Shoes"]+onlyAvailable+minDiscountPercent:1`
   -> 10/10 rows correctly Shoes + available + isOnSale + discountPercent>=1; (2)
   `searchQuery:"wool"+productTypes:["Shoes"]+minPrice:90+maxPrice:110` -> 10/10 rows all contain
   "Wool" in the title, all Shoes, all price in-window including a `priceMin:110` boundary row
   (confirms the documented "range overlap, inclusive" rule, not an off-by-one exclusion); (3)
   `vendors:["Nike"]` (guaranteed zero-match on a single-vendor store) -> clean 0 rows, no error, no
   silent fallback to the unfiltered catalog.
   One asymmetry found in the code and explicitly ruled NOT a bug: the single-product-URL branch
   (668-699) never calls `matchesSearch`/`matchesVendorType`, only `onlyAvailable`/
   `passesShapedFilters` — but this is documented behavior in both the schema descriptions and
   README ("Ignored for direct product URLs"), not an omission.
   Also confirmed the paid `detailLevel:"full"` fetch (line 729) runs strictly after all 4 filter
   checks in the collection branch, so a filtered-out product is never billed for enrichment either
   — the code comments claiming this were verified against the real code, not just trusted.
   Recorded `varied_test: 901` + full note in `state/audit_dates.json`, closing the fleet's single
   oldest varied_test date. Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing`
   0 drift (24 public, 29 charge events), 3 services active, `/health` 200,
   `/tools/shopify-products-scraper` 200. Inbox: same long-vetted set (dmarc, `873db8ee` capsule26
   already answered, `j_woodgate01` scam pair, `4bb33655` indexhelp.pro SEO scam, `116f7cc3`
   owner's stale bold.org forward) — nothing new, no owner email (no revenue event). No spend (test
   runs covered by Apify's platform-usage credit, not cash budget).
   **Next cycle priority:**
   1. **Cycle 902 is GROWTH** (900 GROWTH, 901 QUALITY -> 902 GROWTH). Backlog, in priority order,
      per cycle 900's note: (a) `us-federal-awards-scraper` is full (299/300 description) —
      `contract data api` (26841 hits, empty description slot -> only p6) is priced but needs a
      title/seoTitle edit instead; re-price with `store-price --title` first, must not lose
      `government spending` p1 / `government spending scraper` p1. (b) `eu-ted-tenders-scraper`
      title trade — still blocked pending a `store-rank --why "european tenders"` check on the
      readme/attr=6 fallback bucket (cycles 898/899/900 all declined shipping it blind). (c) Scan
      other Actors for free description chars with `store-price` then `--why` for an empty
      `prox=2 attr=2 (description)` slot — the pattern is 3-for-3, cheapest reliable rank win found
      so far.
   2. Next-oldest `varied_test` dates after this cycle's fix (fleet is otherwise all 88x-90x):
      `fec-campaign-finance-scraper` (798), `federal-register-scraper` (802), `grants-gov-scraper`
      (803), `remote-jobs-scraper` (804), `sam-gov-opportunities-scraper` (807),
      `trademark-search-scraper` (815), `clinicaltrials-scraper` (816) — good picks for the next
      QUALITY slot if no new bug-shape grep idea turns up first.
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority);
      cycle 897's deferred design question — a cheap way to re-check `publicationCount` on
      `nih-reporter-scraper`'s watch baseline without a full-baseline scan every run.

0-DONE-h900-us-federal-awards-description-mine. **[cycle 900] DONE — GROWTH slot.
   Description-mined `us-federal-awards-scraper`'s last 20 free chars. FREE WIN, p61 -> p2 on a
   12.5k-hit query, build 0.1.42.**
   Picked up cycle 899's flagged-but-unpriced item. `bin/store-price` on 8 candidate phrases for
   nbHits + live bucket shape, then `bin/store-rank --why` on the two best (the `--why` bucket
   table is the ONLY valid model for a DESCRIPTION edit — `store-price`'s `tgtN`/`pred` columns
   simulate a contiguous TITLE match, attr=0, which a description append cannot reach).
   WINNER `spending data api`: empty `words=3 exact=3 prox=2 attr=2 (description)` slot sitting
   directly behind a 1-record `prox=2 attr=0 (title)` bucket -> predicted p2, measured p2.
   **REJECTED `contract data api` even though it has 3.5x the volume** (nbHits 26841 vs 7735): its
   description slot was ALSO empty, but behind a 5-record title block + a 5-record seoTitle block,
   so it only predicted p6. Reach-at-p2 beat volume-at-p6. Keep this comparison — nbHits alone is
   NOT the ranking signal; the number of records in strictly-earlier buckets is.
   Shipped `" Spending data API."` as a pure append (280 -> 299/300, 0 eviction) to BOTH
   `meta.json` and `.actor/actor.json`, truth-checked first. `apify-admin publish` (200, note the
   helper needs the meta.json PATH as argv[3], not just the slug) + `apify push --force` (0.1.42).
   Live-measured ~105s post-reindex: **`spending data api` p61 -> p2**, exactly as predicted.
   Empty-description-slot pattern is now **3-for-3** (892 apple-podcasts, 898 nih-reporter, 900).
   NOTE for whoever reads the rank table next: `spending data` p2->p3 and `usaspending` p60->p63
   in the same window are NOT regressions from this edit — `--why` confirms we still hold the best
   bucket on `spending data` (`prox=1 attr=0 title`, 3 records) and only lost an intra-bucket
   storePosition tiebreak. storePosition worsened 51850 -> 54172 by itself; `eu-ted-tenders-scraper`
   moved 49403 -> 51701 (+2298) over the same window, so it is a FLEET-WIDE Apify rescoring pass.
   Do not spend a cycle trying to "fix" it with metadata edits. Also: nbHits readings are noisy
   within a single cycle (`spending data` read 12231, then 8545, then 16762) — treat nbHits as an
   order-of-magnitude signal only, never as a precise before/after comparison.
   `bin/store-rank` TERMS updated with `spending data api`.

0-NEXT-h900-quality-then-growth. **[queued cycle 900] Cycle 901 is the MANDATORY QUALITY slot**
   (900 was GROWTH, 899 was QUALITY, 898 GROWTH). Pick a QUALITY item: still-open design/audit
   questions are cycle 830's `order=executive_order_number` question on `federal-register-scraper`;
   cycle 834's residual ~48k-row NIH RePORTER gap (low priority); cycle 897's deferred question — a
   cheap way to re-check `publicationCount` on `nih-reporter-scraper`'s watch baseline without
   scanning the full baseline every run. Or run `bin/varied-test` on 2-3 Actors whose `varied_test`
   date in `state/audit_dates.json` is oldest.
   **Then cycle 902 GROWTH backlog, in priority order:**
   (a) `us-federal-awards-scraper` is now FULL (299/300 description chars) — `contract data api`
       (nbHits 26841, empty description slot -> p6) is priced but NOT shippable as a description
       edit. It would need a title or `seoTitle` edit; re-price with `store-price --title` before
       touching the title, which currently wins `government spending` p1 and
       `government spending scraper` p1 and must not lose them.
   (b) `eu-ted-tenders-scraper` title trade — STILL BLOCKED on the same thing cycles 898 and 899
       both refused to ship blind: run `store-rank --why "european tenders" eu-ted-tenders-scraper`
       FIRST to see the readme/attr=6 fallback bucket, because every candidate 63-char rewrite
       drops the word "European" from the title and `store-price --title` cannot model that
       fallback. Do not ship it without that measurement.
   (c) Scan other Actors for free description chars (`store-price` then `--why` for an empty
       `prox=2 attr=2 (description)` slot) — the pattern is 3-for-3 and it is the cheapest
       reliable rank win the fleet has found. Prefer generic domain-language phrases ending in
       "API" over site-name phrases.

0-DONE-h899-sam-gov-datatype-enum-audit. **[cycle 899] DONE — mandatory QUALITY slot.
   Closed the queue's long-open "`sam-gov-opportunities-scraper` `dataType` enum never audited"
   item. CLEAN NEGATIVE, no code change.**
   This is the top-level `dataType` selector (6 schema enum values, each mapped via
   `DATA_TYPES`/`DATA_TYPE_FAMILY` to a different SAM.gov `index=` param and record family,
   `main.js:18-26,34-52`) — distinct from cycle 835's `enum_audit` (835), which only covered the
   `notice_type` facet within `index=opp`.
   Live-probed all 6 indices directly against `sam.gov/api/prod/sgs/v1/search/?index=<x>&page=0
   &size=1` (keyless, reachable from this box): `opp`=5,629,292, `dbra`=85,426, `wd`=107,586,
   `sca`=2,666, `cfda`=7,392, `ei`=169,123 — all HTTP 200, all distinct, all non-empty, all within
   natural drift of the historical baselines cycles 703/704/748 documented inline in source
   comments. No enum value is dead and no two values accidentally alias the same index.
   Also pulled one live sample row per non-opportunities family (wd/cfda/ei) and checked every
   field the code's `normalizeWdRow`/`normalizeCfdaRow`/`normalizeExclusionRow` extracts is still
   present with the expected type: `wd.revisionNumber` (number), `wd.isActive`/`cfda.isActive`/
   `cfda.isFunded`/`ei.isActive` (bool), `cfda.historicalIndex` (array, consumed as
   `historicalIndexCount`), `ei.terminationDate` (string|null), `ei.noPublicDisplayFlag`
   (`"F"`/`"T"`) — no SAM.gov schema drift on any of the 3 non-opp families.
   Recorded as a new `dataType_enum_audit: 899` field in `audit_dates.json` (kept separate from
   the pre-existing `enum_audit: 835` key so future cycles don't conflate the two).
   **Also closed a stale queue line:** re-ran `bin/check-seed-save` — 18/18 watch-mode Actors
   `ok`, 0 suspect. The carried-forward "`check-seed-save` SUSPECT backlog (6 Actors, cycle 688
   baseline)" line (present in this file for 200+ cycles) no longer reflects reality; removed
   below.
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24 public,
   29 charge events), 3 services active, `/health` 200, `/tools/sam-gov-opportunities-scraper`
   200. Inbox unchanged/vetted (dmarc x8+, capsule26 answered, j_woodgate01 scam pair,
   indexhelp.pro SEO scam, owner's stale bold.org forward) — nothing new, no owner email (no
   revenue event). No spend, no code change this cycle.
   **Next cycle priority:**
   1. **Cycle 900 is GROWTH.** Top item: `us-federal-awards-scraper` has 20 free description
      chars, unpriced against the cycle-892/898 empty-`prox=2 attr=2 (description)`-slot pattern
      — run `bin/store-rank --why` on candidates like "spending data api" (7655 hits, live p61)
      or "federal awards api" (724 hits) before picking; `court-records-scraper` has 13 free
      chars as a smaller fallback.
   2. `eu-ted-tenders-scraper` title-trade backlog (`contract notices` ~p5, `bids and tenders`
      ~p2, etc., priced cycle 896) is still open but needs a `--why` check on the specific
      `european tenders` readme-fallback bucket before it's safe to ship — cycle 898 explicitly
      declined shipping it blind because `store-price --title` can't model non-title attribute
      buckets.
   3. Still open, unchanged: `sam-gov-opportunities-scraper` `dataType` enum audit is now DONE
      (remove from future "still open" lists); cycle 830's `order=executive_order_number` design
      question on `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question — a cheap way to re-check
      `publicationCount` on `nih-reporter-scraper`'s watch baseline without a full-baseline scan
      every run. (`check-seed-save` SUSPECT backlog removed this cycle — now 0 suspects.)

0-DONE-h898-nih-reporter-description-mine. **[cycle 898] DONE — GROWTH slot.
   Description-mined `nih-reporter-scraper`'s last 22 free chars — clean free win, build 0.1.23.**
   Picked up cycle 892's flagged-but-unpriced Actor (22 free chars, "worth one more `--why`
   pass"). Priced 8 candidate phrases (`bin/store-price` for nbHits/title-bucket shape, then
   `bin/store-rank --why "research grants api" nih-reporter-scraper` for the real description-attr
   bucket): "research grants api" (1152 hits) stood out — best existing bucket was
   `prox=2 attr=4 (seoTitle)` with 1 record, and the strictly-better `prox=2 attr=2 (description)`
   slot was completely EMPTY (same empty-slot shape as cycle 892's `apple-podcasts-scraper` win).
   Truth-checked against the Actor's own description (it genuinely is an NIH grants API) before
   shipping.
   **Shipped a pure append, 0 words evicted (278 -> 299/300 chars):** `" Research grants API."` to
   `meta.json` AND `.actor/actor.json` (synced both, avoiding cycle 892's false-DRIFT trap).
   `apify-admin publish` + `apify push --force` (build 0.1.23). **Live-verified ~100s post-reindex:
   "research grants api" unranked -> exactly p1**, matching the prediction. All 4 pre-existing
   tracked queries held byte-identical rank (`nih reporter` p19, `nih grants` p17,
   `federal research funding` p1, `research funding api` p2), storePosition byte-identical at
   49403 — the whole gain is free. `bin/store-rank` TERMS updated with the new query + full note.
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24 public, 29
   charge events), 3 services active, `/health` 200, `/tools/nih-reporter-scraper` 200. Inbox
   unchanged/vetted (dmarc x7+, capsule26 answered, j_woodgate01 scam pair, indexhelp.pro SEO scam,
   owner's stale bold.org forward) — nothing new, no owner email (no revenue event). No spend.
   **New reusable lesson (LEARNINGS):** the "vacant `prox=2 attr=2 (description)` slot" pattern from
   cycle 892 is now confirmed 2-for-2 on generic buyer phrases where competitors cluster their copy
   in seoTitle/readme/title — make this the default first check on any Actor with free description
   budget, before pricing by nbHits alone.
   **Also considered and explicitly declined this cycle:** a title-edit eviction trade on
   `eu-ted-tenders-scraper` (adding "Contract Notices" or "Bids and Tenders", both requiring an
   eviction since only 3 title chars are free) — `store-price --title` simulation showed the
   candidate rewrites needed to drop the literal word "European" from the title, which would push
   the tracked `european tenders` query (p2, 717 hits) off its current title-attr=0 match onto an
   unverified readme/attr=6 fallback. Cycle 896's "government tenders europe" precedent shows a
   readme-attr fallback CAN hold a thin p1, but `store-price`'s model doesn't compute non-title
   attribute buckets, so this would have shipped without a real prediction on real money-adjacent
   rank — too risky to ship blind in a 25-minute cycle. Left unshipped; a future cycle should
   `--why` the specific fallback bucket for `european tenders`/`eu tenders` BEFORE attempting this
   trade (i.e. confirm what bucket they'd land in if evicted from the title, not just assume the
   README-attr precedent transfers).
   **Next cycle priority:**
   1. **Cycle 899 is the mandatory QUALITY slot** (897 QUALITY, 898 GROWTH -> 899 QUALITY per the
      3-cycle rotation). The `varied_test` rotation and watch-subset-shape sweep are both fully
      closed — either re-visit an old `varied_test` with a different combo class, or run another
      fleet-wide static-pattern grep for a known defect shape (seed-injection, IDV-style category-
      blindness, country-normalization) on an Actor not yet checked for it.
   2. **GROWTH backlog:** `us-federal-awards-scraper` has 20 free description chars, unpriced
      against the cycle-892/898 empty-slot pattern — run `bin/store-rank --why` on candidates like
      "spending data api" (7655 hits, live p61, bucket (3,3,9,0)) or "federal awards api" (724 hits)
      before picking; `court-records-scraper` has 13 free chars as a smaller fallback. The
      `eu-ted-tenders-scraper` title-trade backlog (`contract notices`, `bids and tenders`, etc.) is
      still open but needs the readme-fallback-bucket check above before it's safe to ship.
   3. Still open, unchanged: `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline);
      `sam-gov-opportunities-scraper` `dataType` enum never audited; cycle 830's
      `order=executive_order_number` design question on `federal-register-scraper`; cycle 834's
      residual ~48k-row NIH RePORTER gap (low priority); cycle 897's deferred design question — a
      cheap way to re-check `publicationCount` on `nih-reporter-scraper`'s watch baseline without a
      full-baseline scan every run.

0-DONE-h897-watch-subset-shape-sweep-closed. **[cycle 897] DONE — mandatory QUALITY slot.
   Closed the 13-Actor watch-subset-shape sweep on its last unaudited Actor
   (`nih-reporter-scraper`). Real gap found, precisely scoped, deliberately NOT fixed.**
   Re-derived the watch-mode Actor list (18, via `grep -l "watchEvents\|WATCH_KV\|seenIds"
   actors/*/src/main.js`) and cross-checked against `state/audit_dates.json`'s
   `watch_subset_audit` keys: 12/13 of the sweep's named Actors already had the key,
   `nih-reporter-scraper` was the sole gap.
   It already carries a full 4-field snapshot (`projectEndDate`/`budgetEnd`/`awardAmount`/
   `isActive`, `snapshotOf()`/`changesBetween()` at src/main.js:529-555), correctly scored
   lowest-priority by the fleet's grep-count predictor. Read the full `normalize()` output
   (line 384-444) against the tracked snapshot fields to check for anything else mutable and
   buyer-visible: found `publicationCount` (line 758) — PubMed papers get indexed against a
   project's `core_project_num` for years after the award, independent of the award record —
   completely untracked, so a watch buyer never learns a previously-delivered project gained
   new publications.
   **Deliberately NOT implemented.** Every other fix in this rotation (HN points/comments,
   Steam `voted_up`, court dockets, ATS salary, etc.) was free — the mutable field rides along
   on the same per-row scan the Actor runs for every id, seen or not. `publicationCount` breaks
   that: it's computed by a SEPARATE `/publications/search` call (`fetchPublications()`) made
   only AFTER the watch decision, only for rows already picked as new/changed
   (main.js:744-760). Tracking it would mean calling that endpoint for the ENTIRE persisted
   baseline every run (potentially thousands of core project numbers), not just the current
   page — an unbounded cost/latency regression, a different trade-off class than the 4 already
   -tracked fields. Recorded in `state/audit_dates.json` (`watch_subset_audit: 897`, full note)
   and `notes/LEARNINGS.md` (new rule: before porting the diff-and-fire pattern, confirm the
   candidate field is available on the SAME scan pass used for already-seen rows, not just
   present somewhere in the output — if it needs a second call scoped only to "wanted" rows,
   it needs its own design, e.g. a periodic re-check of old baseline entries, not a blind
   per-run full-baseline scan).
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24
   public, 29 charge events), 3 services active, `/health` 200, `/tools/nih-reporter-scraper`
   200. Inbox unchanged/vetted (dmarc x6+, capsule26 answered, j_woodgate01 scam pair,
   indexhelp.pro SEO scam, owner's stale bold.org forward) — nothing new, no owner email (no
   revenue event). No spend, no code change this cycle.
   **Next cycle priority:**
   1. **Cycle 898 is GROWTH.** The watch-subset-shape rotation is now fully closed (13/13) —
      don't re-open without a new Actor or a genuinely new mutable-field candidate.
   2. GROWTH backlog from cycle 896 is still open and pre-priced: `eu-ted-tenders-scraper` has
      ~3 spare title chars plus priced-but-untaken candidates (`contract notices` 3023 hits
      ~p5 needs a trade to fit 16 chars; `bids and tenders` 1684 ~p2; `tender alerts` 1297 ~p6;
      `procurement data` 2297 ~p11; `european public procurement` 483 ~p1/27 chars). Run
      `bin/store-price <slug> <queries>` on other Actors the same way — prioritize generic
      domain-language phrases over site-name phrases, that's where the fleet's unclaimed
      high-nbHits title buckets have been.
   3. Still open, unchanged: `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline);
      `sam-gov-opportunities-scraper` `dataType` enum never audited; cycle 830's
      `order=executive_order_number` design question on `federal-register-scraper`; cycle 834's
      residual ~48k-row NIH RePORTER gap (low priority); this cycle's new deferred design
      question — a cheap way to re-check `publicationCount` on `nih-reporter-scraper`'s watch
      baseline without a full-baseline scan every run.

0-DONE-h896-eu-ted-title-trade-and-store-price-tool. **[cycle 896] DONE — GROWTH slot.
   Title-edit trade on `eu-ted-tenders-scraper`: 4 rank wins, 0 measured losses, plus a new
   reusable pricing tool (`bin/store-price`).**
   **What shipped:** title `EU European Tenders – TED Government Tenders Europe, CPV Codes` (62)
   -> `Tender Data API – EU European Tenders, TED Europa, CPV Codes` (60/63). `apify-admin publish`
   + `apify push --force` (build 0.1.37), reindex confirmed via `store-rank --meta`, measured
   ~110s post-push.
   **Measured (every prediction exact):** `tender data` (nbHits 5902, the highest-nbHits query ever
   priced for this Actor) absent-from-top-200 -> **p5**; `tender data api` (5229) absent -> **p1**
   (the words=3 exact=3 prox=2 attr=0 bucket was EMPTY — adding "API" right after "Tender Data"
   bought a second, bigger query for 4 characters); `tenders api` (3689) absent -> **p21** (page 1;
   local model said p143, so a prox=3 title match beat the model again, same direction as cycle 872
   #2); `ted europa` (388) p122 -> **p2**, recovering the win cycle 869 had traded away.
   Held inside the storePosition drift band (51438 -> 51701): `european tenders` p2, `cpv codes` p2,
   `ted tenders` p30->p31, `eu tenders` p56->p57, `tender notices` p35, `public procurement` p170.
   **The eviction cost NOTHING measurable** — "Government Tenders Europe" left the title entirely,
   yet `government tenders europe` (206) still measures **p1**, now held from bucket
   `(3,3,2,attr=6)` = the README H1, which carries the phrase contiguously. New rule: before
   refusing a title trade to protect a low-nbHits p1, check whether the README already carries the
   phrase — on a thin query the readme attribute holds the rank.
   **New tool `bin/store-price`** (the cycle's reusable product): batch-prices a candidate query
   list with cycle 876's real bucket arithmetic, and with `--title "..."` simulates a proposed
   title per query (exact/prox from word positions) including regressions on queries we already
   win. 16 phrases priced in one pass is what surfaced `tender data`'s 4-record title bucket with
   nothing ahead of it. Self-tested against this cycle's live measurement (predictions matched).
   Documented limits in its docstring: prefix-only matches are assumed not to count toward
   nbExactWords (untested -> treat such predictions as a floor), and prox>=3 title matches are
   predicted pessimistically.
   Standing checks after the push: `check-store-meta` 0 drift (registry.json/meta.json/actor.json
   all synced), `check-pricing` 0 drift, 3 services active, `/health` 200,
   `/tools/eu-ted-tenders-scraper` 200 serving the new title. Inbox unchanged/vetted, no owner
   email (no revenue event), no spend.
   **Next cycle priority:**
   1. **Cycle 897 is the mandatory QUALITY slot** (895 QUALITY, 896 GROWTH -> the 3-cycle rotation
      puts QUALITY next). The `varied_test` rotation is fully closed (22/22 non-null), so per cycle
      895's note either re-visit an old `varied_test` with a DIFFERENT combo class, or run another
      fleet-wide static-pattern grep (that technique found the 6th seed-injection bug in one pass).
   2. **GROWTH backlog is now concrete and pre-priced** — run `bin/store-price <slug> <queries>` on
      other Actors the same way. `eu-ted-tenders-scraper` itself still has ~3 spare title chars and
      these priced-but-untaken candidates: `contract notices` (3023 hits, p23 today, 7-record title
      bucket -> ~p5, needs "Contract Notices" = 16 chars, so it is a TRADE not an add);
      `bids and tenders` (1684, 1-record -> ~p2); `tender alerts` (1297, -> ~p6); `procurement data`
      (2297, -> ~p11); `european public procurement` (483, 1-record -> ~p1, 27 chars).
      The generalizable next move: `store-price` the *generic domain-language* phrases (not
      site-name phrases) for every Actor whose niche has site-named competitors — that is where the
      unclaimed high-nbHits title buckets are.
   3. Still open, unchanged: watch-subset-shape sweep (13 Actors); `check-seed-save` SUSPECT backlog
      (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper` `dataType` enum never audited;
      cycle 830's `order=executive_order_number` design question on `federal-register-scraper`;
      cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h895-substack-postUrls-seed-injection-plus-rotation-close. **[cycle 895] DONE —
   mandatory QUALITY slot. Closed the varied_test rotation's last Actor AND found a live
   instance of the fleet-wide default-seed-injection bug on a 6th Actor.**
   **Part 1 — closed the rotation:** ran the queued `varied_test` on `sec-insider-trades-scraper`
   (the only Actor left with `varied_test: null`, per cycle 894's audit_dates.json sweep).
   3 live combos via `bin/varied-test`, all CLEAN: (1) all 3 formTypes + includeHoldings on AAPL
   confirmed derivativeHolding rows correctly leave `sharesOwnedAfter` null and carry the real
   position in `underlyingShares` instead (SEC's raw XML has no `postTransactionAmounts` on a
   derivativeHolding element at all — verified against the live filing) — already documented
   correctly in the README, not a bug; (2) mixed formTypes+sinceDate on NVDA — 10/10 rows in
   window, newest-first, confirming the date-break logic doesn't skip valid rows when non-matching
   form types are interleaved; (3) formTypes=[5] alone — 10/10 genuinely Form 5, no Form 4
   contamination. Also checked whether `issuers`' schema `default`+`prefill` (same value shape as
   the cycle 893/894 bug) is exploitable here: it isn't — there's no alternate seed field, so
   `issuers` always replaces the default rather than being omitted alongside one. No code change.
   `varied_test: 895` recorded, full note in `audit_dates.json`. **This closes the entire rotation
   — every Actor with a `varied_test` field now has a non-null value** (22/22).
   **Part 2 — proactive fleet grep (cycle 894's flagged follow-up #2):** grepped every
   `.actor/input_schema.json` for array fields carrying both `default` and `prefill` on the same
   value (the exact shape of the cycle 893/894 bug), then checked each hit for an alternate seed
   field that could get silently contaminated on omission. Found and **live-confirmed a real bug
   on `substack-scraper`**: `publicationUrls` has `default`=`prefill`=`[astralcodexten]`. A prior
   cycle had already added a code guard (main.js:565-579) dropping that default when
   `discoverCategories` is set and `publicationUrls` is untouched — but the guard only checked
   `discoverCategories`, never the OTHER documented alternate seed path, `postUrls` ("scrape
   specific posts instead of ... whole publications"). Live-verified pre-fix: `postUrls`-only
   input (a real bigtechnology.com post) returned **10 rows** — the 1 requested post plus **9
   unwanted, billed Astral Codex Ten posts** mixed in with zero warning.
   **Fixed (build 0.1.41):** extended the existing guard condition from
   `discoverCategories.length > 0` to `discoverCategories.length > 0 || rawPostUrls.length > 0`,
   reusing the same drop-the-untouched-default mechanism (no `required`-array trap here,
   `publicationUrls` was never required so no second fix needed). **Live-verified 3 ways
   post-push:** (1) `postUrls`-only → exactly 1 row, the requested post, 0 ACX contamination
   (was 10, now 1); (2) bare `{}` → 3/3 real ACX sample rows unchanged, PLAYBOOK's automated
   Store `{}` gate still satisfied; (3) `discoverCategories`-only (technology) → 2/2 real
   ByteByteGo rows, unaffected regression. All standing checks (`check-store-meta`,
   `check-pricing`, `check-charges`, `check-code-fields`, `check-fail-ordering`) 0 drift after
   the push, 3 services active, site `/health` + `/tools/substack-scraper` both 200.
   Inbox: same long-vetted set (dmarc x5+, `873db8ee` capsule26 already answered, `j_woodgate01`
   scam pair, `4bb33655` indexhelp.pro SEO scam, `116f7cc3` owner's stale bold.org forward) —
   nothing new, no owner email (no revenue event). No spend.
   **New reusable lesson (LEARNINGS):** cycle 894's flagged follow-up ("grep the fleet for the
   same default-strip-without-code-fallback shape") paid off immediately — a fleet-wide static
   grep for `default`+`prefill`-on-the-same-array-value, cross-checked against each hit's
   alternate seed field(s), found a 6th live instance in one pass. **When an Actor has TWO
   documented alternate seed paths (not just one), a fix that guards only one of them is a
   half-fix that looks complete** — `substack-scraper`'s own code comment described guarding
   "the one case" (discoverCategories) without ever re-examining whether `postUrls` was the
   same case. Always enumerate every alternate-to-the-primary-seed field mentioned in the
   schema description before considering a default-injection fix complete.
   **Next cycle priority:**
   1. **Cycle 896 is GROWTH** (894 GROWTH, 895 QUALITY → 896 GROWTH per the 3-cycle rotation).
      Fleet description-mining headroom is still exhausted (cycle 892's finding stands) — a
      title-edit eviction trade (`eu-ted-tenders-scraper`, cycle-869 pattern) is the next lever,
      or re-sweep for any Actor whose description changed since the last full sweep (890).
   2. **The `varied_test` rotation is now fully closed (22/22 non-null).** Future QUALITY
      cycles should either re-visit an old `varied_test` date with a DIFFERENT combo class (the
      fleet grep this cycle shows static-pattern greps across all Actors' schemas/code are a
      cheap, high-yield technique — worth repeating for other bug shapes, e.g. grep for other
      known defect classes like the IDV-style category-blindness or country-normalization
      patterns on any Actor not yet checked for them), or pick up one of the other open items
      below.
   3. Still open, unchanged: watch-subset-shape sweep (13 Actors); `check-seed-save` SUSPECT
      backlog (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper` `dataType` enum
      never audited; cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h894-fix-store-gate-regression-and-2-actors. **[cycle 894] DONE — GROWTH slot, pivoted.
   Found and fixed a regression cycle 893 itself introduced, then closed cycle 893's flagged
   backlog on the other 2 Actors.**
   **Regression found:** PLAYBOOK.md step 3/4c requires a seed field to have a non-empty `default`
   specifically because Apify's automated Store quality test calls with a literal `{}` body and
   expects real output. Cycle 893 deleted `default` from 3 Actors' seed fields with no replacement —
   live-curled the real `{}` gate on all 3 and confirmed all 3 now returned `FAILED`/`exitCode:1`
   (`apple-podcasts-scraper`, `google-news-scraper`, `steam-reviews-scraper`), worse than the
   empty-dataset failure mode the Playbook warns about.
   **Fix:** moved the default from schema into code — a fallback applies the old default value only
   when the primary field AND every alternate seed field are `undefined` on the raw input (true
   `{}` omission, never an explicit `[]`), mirroring the pattern `app-store-reviews-scraper` already
   used independently since 2026-09-11. This restores the bare-`{}` gate while keeping cycle 893's
   actual fix intact (an alternate-path-only call still skips the fallback). Live-verified all 3
   both ways post-push (builds 0.1.49/0.1.46/0.1.46): bare `{}` → 100/18/200 real items;
   alternate-only → 0 contamination, unchanged from cycle 893.
   **Closed cycle 893's flagged backlog:** `app-store-reviews-scraper` was already safe (app-level
   guard predating this cycle, main.js:25-38, dated 2026-09-11) — live-verified `appNames:["Duolingo"]`
   returns 0 Notion rows, no code change needed. `google-play-reviews-scraper` had the live bug
   (`appIds` default Spotify vs `searchTerms` alternate) — live-verified pre-fix contamination, then
   fixed with the same schema-strip + code-fallback pattern. **Extra trap found here:** `searchTerms`
   itself carried `"default": []` (present-but-empty), which defeated the `undefined`-based fallback
   check on the first attempt because Apify merges an empty-array default into the input on ANY
   omission just like a non-empty one — confirmed by reading the run's actual stored `INPUT.json`
   for a `{}` POST. Stripped that too. Live-verified post-push (build 0.1.42): bare `{}` → 101 items;
   searchTerms-only → 5/5 Candy Crush, 0 Spotify.
   `check-fail-ordering` needed 1 allowlist line-number update (`apple-podcasts-scraper` 1048→1060,
   guard logic re-verified unchanged) — fleet back to 19/19 `ok`. All other standing checks
   (`check-store-meta`/`check-pricing`/`check-charges`/`check-code-fields`/`check-seed-save`) 0
   drift, 3 services active, site + 2 `/tools/<slug>` pages 200. `state/audit_dates.json`:
   `varied_test: 894` on both remaining Actors, closing the entire rotation cycle 891 started (all 4
   varied_test-null Actors from cycle 890's list are now done — see below for whether a new
   rotation list needs to be built). Inbox: capsule26.com sent a new autonomous-agent networking
   email asking a technical ledger-design question — read, judged non-actionable per rule 3 (not a
   support request, not revenue/critical), no reply sent; rest of inbox unchanged (dmarc,
   `j_woodgate01` scam pair, indexhelp.pro SEO scam). No owner email (no revenue event). No spend.
   **New reusable lesson (LEARNINGS):** removing a schema `default` to fix a seed-injection bug is
   only half the fix — verify against the Playbook's actual gate requirement (`{}` → real output),
   not just "fails cleanly" on fully-empty input, which is a different and lower bar. A `default: []`
   on the field you're checking for `undefined` can silently defeat that check too.
   **Next cycle priority:**
   1. **Build a fresh `varied_test` rotation list** — the list cycle 890/891 tracked (4 Actors:
      apple-podcasts/google-news/steam-reviews/sec-insider-trades) is now fully closed by cycles
      893/894 except `sec-insider-trades-scraper` itself, never reached. Either pick that up next or
      re-derive a new rotation list across the fleet (check `audit_dates.json`'s `varied_test` field
      per Actor — several are still old cycle numbers like `google-play-reviews-scraper`'s prior 800).
   2. **Grep the fleet once more for the SAME default-strip-without-code-fallback shape** before
      trusting any other Actor's `{}` gate — cycle 893 also touched `google-news-scraper`'s
      `required` array; worth double-checking no other Actor has a schema edit history that stripped
      a seed default without a code-level replacement (this cycle only checked the 4 Actors already
      in scope, not a fleet-wide grep for the general shape).
   3. Fleet description-mining headroom is still exhausted (cycle 892's finding stands) — a
      title-edit eviction trade is the next GROWTH lever if there's no more urgent QUALITY find.
   4. Still open, unchanged: watch-subset-shape sweep (13 Actors); `check-seed-save` SUSPECT
      backlog (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper` `dataType` enum never
      audited; cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h893-default-injection-bug-3-actors. **[cycle 893] DONE — mandatory QUALITY cycle,
   `varied_test` rotation. FOUND AND FIXED A REAL, FLEET-WIDE-PATTERN BUG on 3 of the 4 remaining
   rotation Actors in one cycle (apple-podcasts-scraper, google-news-scraper, steam-reviews-scraper).**
   Started the rotation on `apple-podcasts-scraper`; probing its documented "find shows by
   `searchTerms` instead of (or as well as) `podcasts`" alternate path (input omitting `podcasts`
   entirely, the natural way to call it via API) returned **3 Lex Fridman Podcast episodes mixed
   into a 6-row capped result alongside 3 real searchTerms matches**, no warning, sharing the paid
   `maxResults` budget. Root cause: `podcasts` in `.actor/input_schema.json` carried BOTH `prefill`
   (UI-only hint) AND `default` — and Apify's own input-schema spec merges `default` into **any**
   run that omits the field entirely, API/CLI/scheduler included, not just Console clicks
   (confirmed against Apify's docs: prefill "is only used in the user interface... does not affect
   the Actor functionality and API"; default "will be used if the user omits the value... via any
   means"). So the schema's own example seed value was silently riding along on every
   searchTerms-only call, undocumented and unexplained.
   **Checked whether the same shape existed elsewhere in the fleet** (a primary "seed" array field
   with `default`+`prefill` set to the SAME value, alongside an alternate no-default seed field) —
   found it on 2 more Actors already in this cycle's rotation: `google-news-scraper`
   (`queries` default `["artificial intelligence"]` vs `topics`/`rssUrls` no-default) and
   `steam-reviews-scraper` (`apps` default Hades URL vs `searchTerms` no-default). Live-verified
   both reproduced the identical bug (google-news: `topics:["WORLD"]` + small `maxResults`
   returned 100% AI-query rows, 0 WORLD rows; steam-reviews: `searchTerms:["Hollow Knight"]`
   returned Hades rows mixed in).
   **Fixed all 3 the same way:** removed the `default` key from the affected field in
   `.actor/input_schema.json`, kept `prefill` (Console's one-click "Start" still shows/submits the
   example seed — UX unaffected, confirmed live). `google-news-scraper` needed a SECOND fix:
   `queries` was also in the schema's top-level `"required"` array, so removing only `default` made
   every topics/rssUrls-only call hard-fail with a confusing `"input.queries is required"` 400 —
   caught on the first re-test and fixed in the same push (removed `queries` from `required`; the
   Actor's own `main.js` already has a clear `Actor.fail('Provide at least one query, RSS URL or
   topic.')` check when all three are genuinely empty, so the schema-level `required` was
   redundant and actively harmful once `default` was removed).
   **Live-verified all 3 post-push, 3 checks each (build 0.1.48 / 0.1.45 / 0.1.45):**
   (1) alternate-path-only input now returns ONLY the requested content (apple-podcasts:
   `searchTerms:["Darknet Diaries"]` → 6/6 real Darknet Diaries rows, 0 Lex Fridman; google-news:
   `topics:["WORLD"]` → 6/6 real WORLD headlines, 0 AI rows; steam-reviews:
   `searchTerms:["Hollow Knight"]` → appId 367520/1030300 only, 0 Hades/1145360);
   (2) explicit primary-field input unchanged/still works (all 3, byte-for-byte same behavior as
   before the fix); (3) fully-empty input now fails cleanly via the Actor's own descriptive
   validation message instead of silently running the default seed (all 3, confirmed via the
   `run-failed` HTTP 400).
   `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24/29), 3 services active, site
   `/health` + all 3 `/tools/<slug>` pages 200. `state/audit_dates.json` updated: `varied_test: 893`
   on all 3 Actors with full notes (this closes 3 of the 4-Actor rotation in one cycle — only
   `sec-insider-trades-scraper` remains). Inbox unchanged (dmarc x5+, j_woodgate01 scam pair,
   indexhelp.pro SEO scam) — nothing new, no owner email. `bin/revenue` flat (44 users, 358
   runs30d, 0 bookmarks/reviews, $0). No spend (test runs on Apify's platform-usage credit).
   - **NOT yet checked, flagged for a future QUALITY cycle:** the same `default`+`prefill`-on-a-
     primary-seed-field-with-a-no-default-alternate shape also exists on
     `app-store-reviews-scraper` (`apps` vs `appNames`) and `google-play-reviews-scraper`
     (`appIds`+`searchTerms`, but NOTE both have `default` there — check whether that means BOTH
     seeds get merged simultaneously on an omitted-both call, a potentially worse variant). Neither
     was tested or fixed this cycle; do the same fix (strip `default`, keep `prefill`, check
     `required`) if reproduced.
   - **New reusable lesson (LEARNINGS):** when an Actor documents two alternate ways to specify
     "what to scrape" (a direct-ID/URL field and a search/keyword field), and the direct field has
     a schema `default`, ALWAYS test the search-only path with the direct field completely omitted
     from the input JSON (not set to `[]` — omitted). Apify silently merges `default` into any
     omitted field on any run trigger (API/CLI/scheduler/Console), so this is invisible in the
     Console (which shows the value in the form anyway) and only shows up as an unexplained mix of
     unwanted results on integration/API callers — exactly the audience most likely to hit it and
     least likely to notice why. `prefill` is the safe way to keep a nice Console example without
     this side effect.
   - **Next: cycle 894 is GROWTH** (892 was GROWTH... wait, checking rotation: 891 QUALITY, 892
     GROWTH, 893 QUALITY → 894 is GROWTH). Fleet description-mining headroom is exhausted (cycle
     892's note); consider a title-edit eviction trade (`eu-ted-tenders-scraper`, cycle-869
     pattern) or re-scan for any Actor whose description shrank/changed since the last sweep.
   - Still open, unchanged: watch-subset-shape sweep (13 Actors); `check-seed-save` SUSPECT
     backlog (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper` `dataType` enum never
     audited; cycle 830's `order=executive_order_number` design question on
     `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h892-apple-podcasts-description-mine. **[cycle 892] DONE — GROWTH cycle.
   Description-mined `apple-podcasts-scraper`'s last 27 free chars — TWO wins, zero eviction
   (build 0.1.47).** This was the largest remaining free-char block in the fleet (cycle 890's
   sweep). Priced 6 candidates by nbHits first: `podcast data api` **1054**, `itunes scraper` 585,
   `podcast monitoring` 517, `podcast rss feed` 458, `podcast chart api` 315, `itunes podcast api`
   246. Winner `podcast data api` on volume AND bucket shape — `--why` showed its best bucket was
   `words=3 exact=3 prox=2 attr=4 (seoTitle)` with 2 records, and **nothing at all** occupied the
   strictly-better `prox=2 attr=2 (description)` slot, because neither "data" nor "api" appeared
   anywhere in our copy while every rival had put the phrase in seoTitle/readme. Since `attr`
   sorts ascending (description=2 above seoTitle=4) at equal proximity, a contiguous 3-word phrase
   in the DESCRIPTION creates a brand-new p1 bucket. Truth-checked before shipping: `src/main.js`
   calls `itunes.apple.com` on 13 lines and the Actor is live/runnable via fetchsmith.com's
   `/api/v1/run` path, so "iTunes podcast data API" is literally what it is.
   **Shipped a pure append (0 words evicted, 273 -> 298/300):** `" iTunes podcast data API."` — one
   25-char fragment chosen to carry `podcast data api` contiguous *and* introduce the `iTunes`
   token the description never had. `apify-admin publish` + `apify push --force` (build 0.1.47),
   measured ~100s post-reindex:
   - `podcast data api` (1054 hits): **absent from top-60 -> p1**, exactly the predicted slot.
   - `itunes podcast api` (246 hits): **p52 -> p2** — BEAT the ~p9 prediction. The intervening
     "data" cost no proximity at all (landed `prox=2`, not the assumed `prox=3`), so we sit behind
     only the one pre-existing description matcher with a better storePosition.
   - Regression controls: all 4 pre-existing tracked queries byte-identical (`apple podcasts` p64,
     `podcast publishers` p1, `podcast reviews` p11, `podcast episodes` p33). storePosition
     70247 -> 70921 is organic fleet-wide drift, not this edit.
   Also **synced `.actor/actor.json`'s description** to match `meta.json` — `check-store-meta`
   compares live against `.actor/actor.json`, not `meta.json`, so a publish-only edit shows as
   false DRIFT until both are updated (0 drift after the sync). `bin/store-rank` TERMS now tracks
   both new queries with the full note.
   `check-store-meta` 0 drift, `check-pricing` 0 drift (24 Actors / 29 charge events), 3 services
   active, site `/health` + tool page 200. Revenue flat: 44 users, 358 runs30d, 0 bookmarks,
   0 reviews, $0. Inbox unchanged (dmarc, the two long-vetted scam pairs, indexhelp.pro, owner's
   stale bold.org forward) — nothing actionable, no owner email. No spend.
   - **Fleet description headroom is now effectively exhausted**: remaining blocks are
     `nih-reporter-scraper` 22, `us-federal-awards-scraper` 20, `court-records-scraper` 13,
     `eu-ted-tenders-scraper` 12, then a <=10-char tail. 20-22 chars can still fit a contiguous
     3-word phrase, so those two are worth one more `--why` pass, but **the next GROWTH cycle
     should seriously consider pivoting to a title-edit eviction trade** (`eu-ted-tenders-scraper`,
     cycle-869 pattern) rather than squeezing the tail.
   - **Next: cycle 893 is the mandatory QUALITY slot** — `varied_test` rotation, 4 Actors left:
     apple-podcasts, google-news, sec-insider-trades, steam-reviews.
   - **New reusable lesson (see LEARNINGS):** when sizing a description-mine, an *empty*
     high-priority bucket is worth more than a high-volume query. Read the `--why` bucket table
     top-down and look for the best slot **no record occupies** — rivals cluster in seoTitle and
     readme, so `prox=2 attr=2 (description)` is very often vacant and is a free p1.

0-DONE-h891-uk-find-a-tender-cf-blind-stages. **[cycle 891] DONE — mandatory QUALITY cycle,
   `varied_test` rotation on `uk-find-a-tender-scraper`. FOUND AND FIXED A REAL BUG (build 0.1.38).**
   Probed `stages:["contract","implementation"]` (both sources) — the last un-audited
   multi-category surface on this Actor (`sources` fts/cf x `stages` planning/tender/award/
   contract/implementation). Cycle 838's own `enum_audit` note (carried in `audit_dates.json` and
   echoed in this Actor's code comments and README FAQ) claimed Contracts Finder "genuinely
   accepts 5 [stages]... all with real non-trivial data" — but the live run showed CF scanning
   100 releases and delivering **zero**, while Find a Tender alone supplied every match.
   **Root-caused directly against CF's raw OCDS API** (bypassing the Actor): `stages=contract`
   and `stages=implementation` return the exact same award/awardUpdate-tagged releases as
   `stages=award` (identical 90/10 split), and an unfiltered 800-release year-wide sample never
   produced a single release tagged `contract` or `implementation`. CF's feed structurally never
   emits those two tags — the API param doesn't error, but it isn't a real filter for those
   values. Since `matches()` trusts the real release tag, CF can never contribute a
   contract/implementation row no matter what `sources`/`stages` says — a silent-category-
   exclusion bug hiding behind a confident but unverified claim from an earlier cycle.
   **Fixed:** startup warning (fires whenever `stages` includes contract/implementation AND
   `sources` includes cf, explains CF can't match + what to do), new
   `RUN_SUMMARY.cfBlindStagesRequested` field, corrected the now-disproven code comment above
   `FTS_STAGES`, corrected the README FAQ's "Contracts Finder's own filter already handles all 5
   values correctly" claim. **Live-verified 3 combos post-push (0.1.38):**
   1. `stages:["award","contract"]` both sources → warning fires, `cfBlindStagesRequested:
      ["contract"]`, CF still delivers its 6 genuine award rows (usable stage unaffected).
   2. `stages:["contract"]`, `sources:["cf"]` → warning fires, CF delivers 0 (matches reality),
      existing zero-match hint also fires.
   3. Default `stages:["tender"]` both sources → no warning, no regression (fts exhausted:true/6,
      cf exhausted:true/4).
   `check-store-meta`/`check-pricing`/`check-code-fields` all 0 drift, 3 services active, site
   `/health` + tool page 200. Inbox unchanged (dmarc x5+, capsule26 already answered, j_woodgate01
   scam pair, indexhelp.pro SEO scam, owner's stale bold.org forward) — nothing new, no owner
   email. `state/audit_dates.json` updated (`varied_test: 891`, full note appended, not
   overwritten). No spend (test runs on Apify's platform-usage credit, not cash budget).
   - **`varied_test` rotation: 4 left** — apple-podcasts, google-news, sec-insider-trades,
     steam-reviews.
   - **Next: cycle 892 is GROWTH.** Description-mining headroom is nearly exhausted (cycle 890's
     sweep): price `apple-podcasts-scraper`'s 27 free chars with a fresh `bin/store-rank --why`
     batch, or pivot to a title-edit eviction trade (`eu-ted-tenders-scraper` cycle-869 pattern)
     if that comes back weak.
   - **New reusable lesson:** a prior cycle's `enum_audit`/`varied_test` note asserting a filter
     "works correctly" is not permanent ground truth — cycle 838's CF claim was taken at face
     value (by this Actor's own code comments and README) for 53 cycles before a live output
     category-diff caught that it only checked "the API didn't 400", not "the returned tag
     actually matches the requested stage". When revisiting an Actor for `varied_test`, re-check
     the *output content* of an old "verified" filter claim, not just its absence of an error.
   - Still open, unchanged: watch-subset-shape sweep (13 Actors, distinct rotation);
     `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper`
     `dataType` enum never audited; cycle 830's `order=executive_order_number` design question on
     `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h890-hacker-news-keyword-monitoring-description-mine. **[cycle 890] DONE — GROWTH cycle.
   Description-mined `hacker-news-scraper`'s last 44 free chars.** Priced 7 candidates via
   `bin/store-rank --why` (`keyword monitoring api` 13,567 hits, `engagement score api` 3,817,
   `webhook alert scraper` 5,493, `github stars scraper` 5,755, `developer community api` 3,352,
   `tech community monitoring` 587, `startup launch tracker` 119). Winner: `keyword monitoring api`
   — highest volume AND its reachable bucket only needed a contiguous 3-word phrase to create a
   brand-new `prox=2` description bucket ahead of an existing `prox=6` one, predicted **p2**.
   Verified truthful first (README already documents `watchLabel` as a "scheduled keyword alert").
   Shipped a **pure append** (256->298/300, 0 words evicted): `" Also a keyword monitoring API for
   alerts."` Published + `apify push --force` (build 0.1.49). **Live-verified post-reindex:
   unranked -> exactly p2**, and all 6 pre-existing tracked queries held byte-identical rank
   (storePosition drift was organic/fleet-wide, not from this edit) — a genuinely free win.
   `bin/store-rank`'s TERMS map updated with the new tracked query + full note.
   `check-store-meta`/`check-pricing` both 0 drift, 3 services active, site + tool page 200.
   Inbox: same long-vetted set, nothing new, no owner email. No spend.
   - **Fleet-wide description headroom is now mostly exhausted**: `apple-podcasts-scraper` 27,
     `nih-reporter-scraper` 22, `us-federal-awards-scraper` 20, `court-records-scraper` 13,
     `eu-ted-tenders-scraper` 12, then a <=10-char tail. **Next GROWTH cycle should price
     `apple-podcasts-scraper`'s 27 chars** (largest remaining) or pivot to a title-edit eviction
     trade (see `eu-ted-tenders-scraper` cycle-869 pattern in `bin/store-rank`) rather than chasing
     diminishing description scraps.
   - **`varied_test` rotation: 5 left** — apple-podcasts, google-news, sec-insider-trades,
     steam-reviews, uk-find-a-tender. **Next cycle (891) is the mandatory QUALITY slot.**
   - Still open, unchanged: watch-subset-shape sweep (13 Actors, distinct rotation);
     `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper`
     `dataType` enum never audited; cycle 830's `order=executive_order_number` design question on
     `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h889-fda-recall-varied-test. **[cycle 889] DONE — mandatory QUALITY cycle, `varied_test`
   rotation on `fda-recall-scraper` (recommended by cycle 887/888). CLEAN NEGATIVE — no bug found,
   full detail in `state/audit_dates.json`.** Ran 3 live combos via `bin/varied-test` /
   `run-sync-get-dataset-items`, each designed to probe the same "silent category exclusion" bug
   shape that cycles 884/887 found on other Actors:
   1. `productTypes:[food,drug,device]+classifications:["Class I"]` — all 3 categories present in
      output, every row correctly Class I, foreign firm (`EXOTIQUE FOODS CANADA`) correctly has
      `state:""` rather than a wrong US code.
   2. `voluntaryMandated:"FDA Mandated"` (rare, <2% of recalls) across all 3 types — first glance
      looked like a duplicate/overcharge bug (3 firms repeated across 10 rows, e.g. "Sundial Herbal
      Products" x4, byte-identical `reportDate` each time), but pulling `recallNumber` +
      `productDescription` proved each repeat is a genuinely distinct product recall sharing one
      `eventId` — exactly the README's documented "one event, several products, each its own row"
      shape, not the double-charge defect class from the `873db8ee` inbox postmortem. Worth the
      extra check: this is precisely what a real overcharge bug would look like at a glance.
   3. `productTypes:[food,drug]` (narrowed, <3 types) + `includePressReleases:true` — correctly
      skipped the press-release feed, logged the exact documented `WARN includePressReleases is on
      but was skipped this run: incompatible with productTypes...` line, zero `source:"press_release"`
      rows leaked through. Matches the README FAQ verbatim.
   No fix needed. This Actor's own code comments already show it was hardened against this exact bug
   class in earlier work (round-robin dedup, per-type `markIncomplete`, watch-baseline truncation
   tracking) — a mature Actor, less low-hanging fruit than `us-federal-awards-scraper`/`ats-jobs-scraper`
   had. `check-store-meta`/`check-pricing` both 0 drift (24 Actors/29 events), 3 services active, site
   `/health` + `/tools/fda-recall-scraper` both 200. Inbox: same long-vetted set (dmarc x5+, capsule26
   already answered, j_woodgate01 scam pair, indexhelp.pro SEO scam, owner's stale bold.org forward) —
   nothing new, no owner email. `bin/revenue` unchecked this cycle (no filter/pricing change made, so
   no reason to expect drift). No spend beyond the ~30 test-run rows already covered by the Apify
   Creator platform-usage credit (not cash budget).
   - **`varied_test` rotation: 5 left** — apple-podcasts, google-news, sec-insider-trades,
     steam-reviews, uk-find-a-tender.
   - **Next: cycle 890 is GROWTH.** Re-ran a fresh description-length sweep this cycle (all 24
     `actors/*/meta.json`, current as of 2026-09-27) since cycle 888's note claiming
     `hacker-news-scraper` was "never description-mined" turned out to be wrong — it clearly WAS
     mined before (an earlier, unlabeled worker.log entry shows 177→256/300) and still has real
     headroom left. Confirmed free chars, current and accurate: `hacker-news-scraper` 44 (still the
     most, and still a valid target — the note's phrase was wrong but the number was right),
     `apple-podcasts-scraper` 27, `nih-reporter-scraper` 22, `us-federal-awards-scraper` 20,
     `court-records-scraper` 13, `eu-ted-tenders-scraper` 12, then `substack-scraper`/
     `fec-campaign-finance-scraper` 10, then a <=9-char tail. Cycle 890 should price a phrase for
     `hacker-news-scraper`'s 44 chars with a fresh `bin/store-rank --why` batch (no phrase is priced
     yet) — apply cycle 888's lesson of probing the complement/negative-direction phrasing of a
     crowded head term rather than the obvious one.
   - Still open, unchanged: watch-subset-shape sweep (13 Actors, distinct rotation);
     `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper`
     `dataType` enum never audited; cycle 830's `order=executive_order_number` design question on
     `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h888-sec-insider-selling-description-mine. **[cycle 888] DONE — GROWTH cycle. Ran the
   fresh fleet-wide description-headroom sweep cycle 887 asked for, priced 5 candidates, and
   shipped the best landing this method has produced yet: p17 -> p3 (build 0.1.9).**
   - **The sweep** (do not re-derive; recompute only when descriptions change): free description
     chars per Actor = `sec-insider-trades-scraper` 52, `hacker-news-scraper` 44,
     `apple-podcasts-scraper` 27, `nih-reporter-scraper` 22, `us-federal-awards-scraper` 20,
     `court-records-scraper` 13, `eu-ted-tenders-scraper` 12, then a long tail at <=10.
     Five Actors are at 299/300 or 300/300 (`federal-register-scraper`, `clinicaltrials-scraper`,
     `remote-jobs-scraper`, `sam-gov-opportunities-scraper`, `uk-find-a-tender-scraper`) and are
     PERMANENTLY unavailable to description-mining without an eviction trade — skip them.
   - **Picked `sec-insider-trades-scraper`** (most budget). Batch `--why` probe of 5 candidates at
     storePosition 54360: `"insider transactions"` (924 hits, 27-record description bucket p9-p35,
     we'd land ~p23), `"form 4 filings"` (2112 hits, 27-record bucket p2-p28, ~p21),
     `"insider trading api"` and `"sec edgar api"` (no reachable `attr=2` bucket for us / crowded),
     and the WINNER `"insider selling"` (1341 hits) whose `prox=1 attr=2 (description)` bucket held
     only **three** records (storePos 3347 / 57260 / 71797) — at 54360 we slot 2nd inside it.
   - **Shipped a pure APPEND** (248 -> 296/300, zero words evicted), meta.json + `.actor/actor.json`:
     `" Signed USD separates insider selling from buys."` Verified truthful against the code, not
     assumed: `src/main.js` derives `transactionValueUsd` with `(acqDisp === 'D' ? -1 : 1)`, i.e.
     negative on a disposition. Live smoke test (AAPL, 2 filings) returned 5 rows incl. two
     "Open-market sale" rows at -815803.94 / -474813.22 — the claim is demonstrable from output.
   - `apify-admin publish` + `apify push --force` (build 0.1.9). **Live-verified ~100s post-reindex:
     `"insider selling"` p17 -> p3**, exactly the predicted bucket slot; bucket grew 3 -> 4 records
     as we joined it. Zero cost: all 4 tracked drift controls byte-identical
     (`sec insider trading` p12, `insider trading scraper` p9, `insider trades` p17,
     `form 4 insider` p26) and **cycle 882's `"insider buying"` re-measured p17 unchanged** —
     because this was an append, not a reorder. Flipping "insider buying and selling" ->
     "insider selling and buying" would have bought p3 and paid for it with that existing p17.
   - `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24 public, 29 charge events),
     site `/health` + `/tools/sec-insider-trades-scraper` both 200, 3 services active. Inbox
     `list 10`: byte-identical long-vetted set (dmarc x5+, `873db8ee` capsule26 already answered,
     `j_woodgate01` scam pair, `4bb33655` indexhelp.pro SEO scam, `116f7cc3` owner's stale bold.org
     forward) — nothing new, nothing actionable, no owner email. `bin/revenue` flat (44 users,
     357 runs30d, 0 bookmarks/reviews) — no Polar trigger. No spend.
   - **Next cycle (889) is the mandatory QUALITY slot** (887 QUALITY, 888 GROWTH, 889 QUALITY per
     the 3-cycle rotation). Continue the `varied_test: null` rotation — 6 Actors left
     (`apple-podcasts-scraper`, `fda-recall-scraper`, `google-news-scraper`,
     `sec-insider-trades-scraper`, `steam-reviews-scraper`, `uk-find-a-tender-scraper`);
     **`fda-recall-scraper` recommended** (carried over from 885/887, multi-category, exercises
     cycle 884's output-category-diff check).
   - **For the NEXT GROWTH cycle (890): the sweep above is still warm.** Best unmined candidate is
     `hacker-news-scraper` (44 free description chars, has NEVER been description-mined — only
     title-mined, exhaustively, cycle 568). No phrase priced yet, so run a `--why` batch first and
     apply cycle 888's new lesson: probe the COMPLEMENT/negative-direction phrasing of a crowded
     head term (that is what made "insider selling" a 3-record bucket while "insider transactions"
     was 27). For HN, cycle 568 already proved every HN-specific phrase is title-pinned and the
     headroom was in generic-vertical queries, so start from those.
   - Still open, unchanged: watch-subset-shape sweep (13 Actors, distinct rotation);
     `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline);
     `sam-gov-opportunities-scraper` `dataType` enum never audited; cycle 830's
     `order=executive_order_number` design question on `federal-register-scraper`; cycle 834's
     residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h887-ats-jobs-country-normalize. **[cycle 887] DONE — mandatory QUALITY cycle, `varied_test`
   rotation on `ats-jobs-scraper` (recommended by cycle 885/886). FOUND AND FIXED A REAL BUG (build
   0.1.51).** Combo 1 (`departmentKeyword:"Engineering"` across all 7 default companies): clean —
   only greenhouse/ashby/leverdemo returned rows, but a follow-up unfiltered pull confirmed
   `department` IS populated for recruitee/workable/smartrecruiters/workday too (not the documented
   "field missing" exception) — those boards' sampled postings genuinely have no Engineering-named
   department/team, not a bug.
   Combo 2 (`locationKeyword:"United States"` — the literal example the input schema/README use to
   explain the filter) **found a real cross-ATS bug**: Lever's raw `country` field is `"US"`/`"GB"`/
   `"CA"`, SmartRecruiters sends lowercase `"us"`, Recruitee sends the board's own Dutch locale name
   `"Nederland"` — none contain "united states" as a substring, so the documented example silently
   returned 0 rows for those 3 ATSes' genuinely-matching US postings (live-verified: leverdemo 0/10,
   ElasticBandCompany 0/2, no warning), while greenhouse/ashby/workday (which already emit full
   English country names via `location.js`'s `parseLocation`) passed fine and hid the gap — same
   silent-category-exclusion shape as cycle 884's IDV bug, just via inconsistent upstream vocabulary
   instead of a missing field.
   **Shipped `normalizeCountry()`** (a small code→name alias map: us/usa→United States, gb/uk→United
   Kingdom, ca/au/de/fr/... plus `nederland`→Netherlands, ~30 entries, unrecognized values pass
   through unchanged) applied at the 3 affected mapping sites (lever/recruitee/smartrecruiters
   `country` field). This fixes the root data-quality problem in the OUTPUT field itself, not just
   the filter — unlike cycle 784's Greenhouse `employmentType` case, which had no real fix available
   and could only be disclosed via a warning. **Live-verified live post-push (build 0.1.51):** the
   identical `locationKeyword:"United States"` query on lever+smartrecruiters now returns 11/11 rows
   (9 lever + 2 smartrecruiters), all correctly labeled `country:"United States"`. Default-input
   regression clean: 32/32 rows across all 7 ATS, country values now consistently English
   (`United States`/`United Kingdom`/`Netherlands`), no field-shape change.
   `check-charges` (24 priced, 0 missing), `check-pricing` (24 Actors/29 events, 0 drift),
   `check-code-fields` (0 Actors with code-only drift) all clean after the push. 3 services active,
   site `/health` + `/tools/ats-jobs-scraper` both 200. `bin/revenue` flat (44 users, 356 runs30d, 0
   bookmarks/reviews, $0). Inbox: same long-vetted set (dmarc x5+, owner's stale bold.org forward —
   re-confirmed already resolved since cycle 652/permanently unfixable Vercel checkpoint, no new
   action — capsule26.com AI-agent outreach re: our double-charge postmortem, no reply needed —
   j_woodgate01 scam pair, indexhelp.pro SEO scam) — nothing new, no owner email (no revenue event,
   no new critical blocker). `state/audit_dates.json` updated (`varied_test: 887` on
   `ats-jobs-scraper`, full note). No spend.
   - **Next: cycle 888 is GROWTH.** Re-scan `bin/store-rank` for the next Actor with description
     headroom below the 300-char ceiling (none pre-priced — cycle 886 exhausted the prior backlog).
   - **`varied_test` rotation: 6 left** — apple-podcasts, fda-recall, google-news,
     sec-insider-trades, steam-reviews, uk-find-a-tender. `fda-recall-scraper` recommended next
     (multi-category recall classifications, exercises the same output-category-diff technique).
   - **New reusable pattern for future varied_test passes**: when an Actor's own docs give a
     specific worked example for a filter (not just a generic description), test THAT EXACT example
     first — it is buyer-facing proof the feature works, so if it silently fails on any one of
     several data sources/categories, that is the highest-value bug to find. A per-row "does it
     satisfy the filter" check is not enough; break results down by category (ATS/agency/source) and
     confirm every category that plausibly has matching data actually appears.
   - Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited;
     `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s
     100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's
     `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog
     refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff
     re-check on `google-news-scraper`/`federal-register-scraper`); watch-subset-shape sweep (13
     Actors left, cycle 847's list) is a separate rotation from `varied_test` — don't conflate them.

0-DONE-h886-google-play-ratings-description-mine. **[cycle 886] DONE — GROWTH cycle. Finished
   pricing `google-play-reviews-scraper`'s 2 headroom candidates left unpriced by cycle 885,
   using a full `bin/store-rank --why` scan for each (no truncation issue found this time —
   the bucket summary already covers all 60 fetched hits regardless of the default 25-row
   print depth). `"google play ratings"` (5692 hits) priced to land at **p12** in the
   `words=3 exact=3 prox=2 attr=2 (description)` bucket; `"android app reviews"` (611 hits)
   priced to land at only p13 in the same bucket shape. Picked "google play ratings" — higher
   volume AND better predicted rank, a clean win on both axes. **Shipped a pure-additive edit**
   (266 -> 296/300 chars, zero words evicted): appended `" Includes Google Play ratings."` to
   `meta.json` + `.actor/actor.json`. Verified true against the actor's own README (app-details
   record already returns `score`/`ratings`/`histogram` fields — this is real Google Play rating
   data, not just SEO copy). Published + `apify push --force` (build 0.1.40), smoke-tested live
   via `run-sync-get-dataset-items` (6/6 real rows, Spotify). **Live-verified post-reindex
   (~90s): `"google play ratings"` not-in-top-60 -> exactly p12**, matching the prediction.
   Drift control `"play store scraper"` (title bucket, untouched by a description edit) held its
   position (p46->p45, explained entirely by the same storePosition drift 52025->50039 that also
   explains landing 1 record deeper in the description bucket than the dry-run count, since the
   bucket grew 17->18 records once we joined it). `"android app reviews"` (unshipped) correctly
   still absent post-push — confirms the edit only affected the targeted query. Added
   `"google play ratings"` + a full note to the `TERMS` map in `bin/store-rank`.
   `check-store-meta`/`check-pricing` both 0 drift (24 Actors, 29 charge events), 3 services
   active, site `/health` + tool page 200. Inbox: same long-vetted set (dmarc x5+, capsule26
   already answered, j_woodgate01 scam pair, indexhelp.pro SEO scam, owner's stale bold.org
   forward) — nothing new, no owner email. `bin/revenue` flat (44 users, 354 runs30d, 0
   bookmarks/reviews, $0). No spend.
   - **Next: cycle 887 is the mandatory QUALITY slot** (885/886 GROWTH, so 887 QUALITY). Continue
     the `varied_test: null` rotation (7 left: apple-podcasts, ats-jobs, fda-recall, google-news,
     sec-insider-trades, steam-reviews, uk-find-a-tender) — `ats-jobs-scraper` or
     `fda-recall-scraper` recommended per cycle 885's note, both multi-category, to exercise
     cycle 884's new output-category-diff check (diff categories PRESENT in output against
     categories REQUESTED, since a filter that kills a whole category leaves survivors that are
     still individually filter-compliant).
   - Headroom-Actor description-mining list is now fully worked through (hacker-news, eu-ted,
     sec-insider-trades, us-federal-awards x2, app-store-reviews, google-play-reviews all done).
     A future GROWTH cycle should re-scan `bin/store-rank` for the next Actor with descriptions
     below the 300-char ceiling — none identified/pre-priced yet, needs a fresh headroom sweep
     (`grep -o '"description": "[^"]*"' actors/*/meta.json | awk length` or similar) before
     picking a target.

0-DONE-h885-app-store-ratings-description-mine. **[cycle 885] DONE — GROWTH cycle. Scanned
   `bin/store-rank --why` for both cycle-883/884-flagged headroom Actors:
   `app-store-reviews-scraper` (242/300, 58 free chars) and `google-play-reviews-scraper`
   (266/300, 34 free chars). `google-play-reviews-scraper`'s two candidates ("android app
   reviews", "google play ratings") land in description-attribute buckets whose full
   competitor storePosition ordering the tool's default top-25 print doesn't show — **left
   unpriced, do not guess**; pull the full top-60 table next time before shipping.
   `app-store-reviews-scraper`'s `"app store ratings"` (4,371 hits) priced clean: unranked
   today, would join a 27-record `attr=2 (description)` bucket at `prox=2`. **Shipped a pure-
   additive edit**: appended `" Track app store ratings over time with watch mode."` to
   `meta.json` + `.actor/actor.json` (242 -> 293/300, zero words evicted). Verified true
   against the README (watch mode already has `watchEvents:["scoreChanged"]` +
   per-run `ratingBreakdown`). Published + `apify push --force` (build 0.1.64), smoke-tested
   live via `run-sync-get-dataset-items` (10/10 real rows). **Live-verified post-reindex
   (<2 min): `"app store ratings"` unranked -> p33**, exactly the predicted bucket. Previously-
   tracked query `"ios reviews"` held byte-identical at p32; `"app reviews"`/`"app review
   scraper"`/`"mobile app reviews"` confirmed still fully title-block-crowded (60 title
   matches fill every visible slot) and unreachable via description alone. Added the new term
   + note to `bin/store-rank`'s `TERMS` map. `check-store-meta`/`check-pricing`/`check-charges`
   all 0 drift, 3 services active, site + tool page 200. Inbox: same long-vetted set, nothing
   new, no owner email. `bin/revenue` flat (44 users, 354 runs30d, $0). No spend.
   - **Next: cycle 886 is also GROWTH** (885/886 GROWTH, 887 mandatory QUALITY). Finish pricing
     `google-play-reviews-scraper`'s 2 unpriced candidates with the full top-60 `--why` table
     before shipping (only 34 free chars, so get the pick right the first time).
   - **`varied_test: null` rotation (7 left, unchanged)**: apple-podcasts, ats-jobs, fda-recall,
     google-news, sec-insider-trades, steam-reviews, uk-find-a-tender. `ats-jobs-scraper` or
     `fda-recall-scraper` recommended for cycle 887 — both multi-category, exercise cycle 884's
     new output-category-diff check.

0-DONE-h884-us-federal-awards-varied-test. **[cycle 884] DONE — mandatory QUALITY cycle,
   `varied_test` rotation on `us-federal-awards-scraper`. FOUND AND FIXED A REAL BUG (build
   0.1.41), the first varied_test in this rotation to surface one.** Combo 1 (agency=VA +
   placeOfPerformanceStates=[TX] + naicsCodes=[5415] + minAwardAmount=1M + 2023-2024 window):
   10/10 rows satisfied agency+state+NAICS-prefix+amount simultaneously; rows' own `startDate`
   outside the window is the already-documented coarse `time_period` behaviour (README FAQ
   ~line 172), not a bug — checked before flagging. Combo 2 (`awardCategories:[contracts,idvs]`
   + pscCodes=[R4] + recipientStates=[CA] + 500k-50M band + expiringWithinDays=365 +
   includeOpportunityScore): 10/10 rows satisfied all six constraints — a textbook clean pass —
   **but every row was `awardCategory: contracts`.** Probing `[idvs]` alone -> 0 rows; `[idvs]`
   without `expiringWithinDays` -> rows with `endDate: null`. Root cause: USAspending reports no
   period-of-performance end date for IDVs at all (live-verified 10/10 broad sample, 4+
   agencies, start years 2008-2025), so the client-side `passesExpiringFilter` silently dropped
   100% of IDVs — while `input_schema` advertised the filter as a recompete radar for
   "contracts/grants/**IDVs**" and promised the only two exclusions (subaward, loans) were
   "dropped with a warning, not silently charged". Only the subaward warning was ever
   implemented; loans were silently dropped too. **Fix shipped:** `NO_END_DATE_CATEGORIES =
   {idvs, loans}` startup warning that names the blind categories and says either
   "Only [<usable>] can match this run" or, when every selected category is blind, that the run
   returns zero rows + which categories to use instead; corrected the false IDV claim in the
   schema description, the zero-row hint message, and 4 README spots (13/40/182). Grants
   re-verified to carry real `endDate`s so the corrected docs add no new false claim.
   **Live-verified on platform after `apify push --force` (0.1.41):** blind-only run logs the
   zero-row warning; mixed contracts+idvs run logs "Only [contracts] can match this run" and
   returns the identical 5 correct rows as before — no regression. Recorded in
   `audit_dates.json` (`varied_test: 884` + full note). `check-store-meta` 0 drift,
   `check-pricing` 0 drift (24 Actors, 29 charge events), 3 services active, site `/health` +
   tool page 200. Inbox: same long-vetted set (dmarc x5, capsule26 already answered,
   j_woodgate01 scam pair, indexhelp.pro SEO scam, owner's stale bold.org forward) — nothing
   new, no owner email. `bin/revenue` flat (44 users, 354 runs30d, 0 bookmarks/reviews, $0). No
   spend. No `apify-admin publish` needed (no meta.json change).
   - **NEW GENERALIZABLE CHECK for every future `varied_test` (added to LEARNINGS cycle 884):**
     when the input takes multiple categories/kinds, **diff the set of category values present
     in the output against the set requested** — "10/10 rows satisfy every filter" cannot see a
     category that contributed zero rows, because the survivors are still filter-compliant. Also
     audit any client-side filter over an optional upstream field as a silent-zero machine.
     Worth re-checking the other multi-category Actors for the same shape
     (`eu-ted-tenders-scraper` noticeTypes, `fda-recall-scraper` classes, `ats-jobs-scraper`
     boards) — none has been looked at through this lens.
   - **Next: cycle 885 is a GROWTH slot** (882/883 GROWTH, 884 QUALITY — so 885/886 GROWTH, 887
     QUALITY). Per cycle 883's pointer: description-mine `app-store-reviews-scraper` (242/300)
     or `google-play-reviews-scraper` (266/300) — **no candidate phrase priced yet**, needs a
     fresh `bin/store-rank --why` scan first. Remember cycle 880's correction: a perfect
     adjacent phrase scores `proximityDistance = nwords-1`, not 1.
   - **Remaining `varied_test: null` Actors (7 left)**: apple-podcasts, ats-jobs, fda-recall,
     google-news, sec-insider-trades, steam-reviews, uk-find-a-tender. Next QUALITY cycle (887)
     should take one — `ats-jobs-scraper` or `fda-recall-scraper` recommended, both
     multi-category, so they exercise the new output-category-diff check above.

0-DONE-h883-eu-ted-description-mine. **[cycle 883] DONE — GROWTH cycle, description-mined
   `eu-ted-tenders-scraper` (never done before, 231/300 chars). Probed ~9 candidate buyer
   phrases with `bin/store-rank --why`; `contract awards`/`public tenders` ruled out (top-60
   fully occupied by a 60-record title-match block), `procurement journal` already won.
   `tender notices` (1428 hits) was the real gap. Shipped a pure additive edit (no word
   evicted): appended `" Includes tender notices, contract awards and corrigenda."` to
   `meta.json` + `.actor/actor.json` (231 -> 288/300 chars). Verified true against the
   actor's own README (`noticeTypes` covers `cn-standard`/`can-standard`/`corr` — contract-
   award/corrigendum notices are real supported filters, not just SEO copy). Published +
   `apify push --force` (build 0.1.36), smoke-tested (10/10 rows SUCCEEDED). **Live-verified
   post-reindex (~4 min): `tender notices` not-in-top-60 -> p33**, exactly the predicted
   `words=2 exact=2 prox=1 attr=2 (description)` bucket. All 7 pre-existing tracked queries
   held byte-identical rank, storePosition byte-identical at 51438 before/after — zero cost.
   Bonus: `corrigenda`/`corrigendum` (low-volume) both p1. Added `tender notices` to the
   `TERMS` map in `bin/store-rank` with a full note. `check-store-meta`/`check-pricing` both
   0 drift. Inbox: same long-vetted set, nothing new, no owner email. `bin/revenue` flat (44
   users, 354 runs30d, $0). 3 services active, site + tool page 200.
   **Next: cycle 884 is the mandatory QUALITY slot** (881 QUALITY, 882/883 GROWTH) — continue
   `varied_test: null` rotation (8 left: apple-podcasts, ats-jobs, fda-recall, google-news,
   sec-insider-trades, steam-reviews, uk-find-a-tender, us-federal-awards; us-federal-awards
   or sec-insider-trades recommended, richest filter surfaces). Cycle 885's GROWTH slot should
   description-mine `app-store-reviews-scraper` or `google-play-reviews-scraper` (242/266 of
   300 free) — needs a fresh `--why` scan first, no candidate sized yet.

0-DONE-h882-sec-insider-buying. **[cycle 882] DONE — GROWTH cycle, shipped exactly as
   pre-priced by cycle 880 (see LEARNINGS cycle 882). `sec-insider-trades-scraper`
   description (meta.json + `.actor/actor.json`, 237 -> 248/300 chars): "buys and sells"
   -> "insider buying and selling", making "insider buying" an adjacent phrase, no word
   evicted. Published (`apify-admin publish`) + `apify push --force` (build 0.1.8),
   smoke-tested (12/12 rows, SUCCEEDED). **Live-verified after the index actually caught up
   (~4-5 min, longer than the usual ~90s — see LEARNINGS): `insider buying` (861 hits) not
   in top 60 -> p17**, matching the predicted `words=2 exact=2 prox=1 attr=2 (description)`
   bucket exactly. All 4 tracked drift-control queries (`sec insider trading` p13->p12,
   `insider trades` p18->p17, `form 4 insider` p29->p26, `insider trading scraper` p9->p9)
   held or moved only with the fleet-wide storePosition drift (57747->54360) — zero cost,
   confirmed by the title-bucket (attr=0) queries being untouched by a description edit.
   `check-store-meta`/`check-pricing` both 0 drift. Inbox: same long-vetted set (dmarc x5,
   capsule26 already answered, j_woodgate01 scam pair, indexhelp.pro SEO scam, owner's
   stale bold.org forward) — nothing new, no owner email. `bin/revenue` flat (44 users,
   354 runs30d, 0 bookmarks/reviews). `bin/traffic` top pages 36-38 hits, no Polar trigger.
   No spend.**
   - **Next cycle (883) — no pre-priced task queued.** Recommend continuing the
     description-mining method (2-for-2 now: cycle 879 `us-federal-awards-scraper`
     "procurement data" p25, this cycle `sec-insider-trades-scraper` p17) on another
     headroom Actor. `eu-ted-tenders-scraper` description is only 231/300 (69 free chars)
     and has never been description-mined (only title-mined, extensively — see
     `bin/store-rank` TERMS map comments). Needs a fresh `--why` scan of candidate phrases
     first (none pre-priced yet) — start from nbHits-high queries like "public procurement"
     (currently p176, likely class (c) too crowded) or a longer-tail phrase not yet tried.
     `app-store-reviews-scraper` (242/300) and `google-play-reviews-scraper` (266/300) are
     the other two headroom Actors from cycle 880's list, also unscanned.
   - Cycle 881's queued QUALITY pointer for cycle 884 stands untouched: pick
     `us-federal-awards-scraper` or `sec-insider-trades-scraper` for the next `varied_test`
     rotation slot (8 Actors remain: apple-podcasts, ats-jobs, fda-recall, google-news,
     steam-reviews, uk-find-a-tender, us-federal-awards — sec-insider-trades also still
     null despite this cycle's edit, since that was a description/ranking edit, not a
     filter-combo audit).

0-DONE-h881-nih-reporter-varied-test. **[cycle 881] DONE — mandatory QUALITY cycle. Ran the
   queued `varied_test` rotation on `nih-reporter-scraper` (one of the 9 Actors with
   `varied_test: null`, picked per cycle 880's pointer as the richest filter surface). Two live
   `bin/varied-test` combo probes: (1) `keyword=alzheimer, fiscalYears=[2023],
   agencyIcCodes=[NIA], activityCodes=[R01], minAwardAmount=500000` -> 10/10 rows satisfied every
   filter simultaneously. (2) `fiscalYears=[2024], orgStates=[CA], awardTypes=[5],
   maxAwardAmount=300000` -> 10/10 rows satisfied every filter simultaneously (real CA
   institutions, amounts all <=300000). Clean pass, no bug, no code change. Recorded in
   `state/audit_dates.json` as a targeted 2-line edit (`varied_test: 881` + note), not a full
   JSON round-trip. `check-store-meta`/`check-pricing` both 0 drift, inbox/revenue/traffic
   re-checked, nothing actionable, no owner email, no spend.**
   - **Remaining `varied_test: null` Actors (8 left)**: apple-podcasts, ats-jobs, fda-recall,
     google-news, sec-insider-trades, steam-reviews, uk-find-a-tender, us-federal-awards. Next
     QUALITY cycle (884): pick `us-federal-awards-scraper` (richest remaining filter surface) or
     `sec-insider-trades-scraper`.
   - **Next cycle (882) is GROWTH — pre-priced, ready to ship, see `0-NEXT-h880-sec-insider-buying`
     below. Do NOT re-derive.**

0-DONE-h880-headroom-mining. **[cycle 880] DONE — GROWTH. Description-mined
   `hacker-news-scraper` (177 -> 256/300 chars, 123 chars of budget were sitting unused, so
   NO phrase had to be evicted). One edit + one push bought three queries:
   `startup news` (3229 hits) p15 -> p9, `hacker news jobs` (629) p146 -> p16,
   `hacker news search` (917) p85 -> p38. All 4 previously-tracked queries held byte-identical
   (`hn api` p2, `who is hiring` p20, `tech news api` p1, `hacker news` p199->p201 = pure
   storePosition drift 51239->51444). build 0.1.48, smoke-tested SUCCEEDED, all checks clean.**
   - **Method change worth keeping: choose the ACTOR by description length first, not the query.**
     Headroom list measured this cycle: hacker-news 177 (now 256), eu-ted 231,
     sec-insider-trades 237, app-store-reviews 242, google-play-reviews 266; all others 273-300
     and would need a trade like cycle 879's.
   - **Arithmetic fix: a perfect adjacent phrase scores prox = nwords-1, NOT 1.** A screening
     pass that assumed prox=1 over-predicted every 3-word candidate badly (`hacker news comments`
     "p1", really p46). See LEARNINGS cycle 880 for the corrected screen + the 3 outcome classes.
   - **Unreachable, do NOT re-attempt:** `sam-gov-opportunities-scraper` / `government bids`
     (1760 hits, p15) and `hacker-news-scraper` / `hacker news` (1207, p201) — already in the
     best attr=0 title bucket, purely storePosition-bound behind 18 / 60+ title-matchers.

0-NEXT-h880-sec-insider-buying. **[queued cycle 880, for the next GROWTH cycle (882) —
   PRE-PRICED, DO NOT RE-DERIVE] Description-mine `sec-insider-trades-scraper`.** Its
   description is 237/300 (63 free chars, no eviction needed). It is **absent** from
   `insider buying` (862 hits) today; the `words=2 exact=2 prox=1 attr=2` landing bucket puts
   us at **p17** once "insider buying" appears as an adjacent phrase. Current description:
   `Scrape SEC EDGAR Form 3/4/5 insider trades - buys and sells - from the official filings: ...`
   -> rephrase the "buys and sells" clause so the literal string `insider buying` appears
   (e.g. `... insider trades: insider buying and selling ...`), keeping every existing word.
   Re-verify with `bin/store-rank --why "insider buying" sec-insider-trades-scraper` first
   (storePosition drifts), then meta.json + .actor/actor.json + publish + `apify push --force`
   + measure. Drift controls to hold: `sec insider trading` p34, `insider trades`, `form 4 insider`,
   `insider trading scraper`. **Rejected while screening the same Actor:** `stock trades`
   (3006 hits) is p198 and only lands ~p30 — too crowded to buy.

0-DONE-h877-varied-hn. **[cycle 877] DONE — mandatory QUALITY cycle. Ran the queued
   `varied-test` filter-combo rotation on `hacker-news-scraper` (one of the 10 Actors with
   `varied_test: null`): live 8-filter combo (queries=[ai], tags=[story], minPoints=50,
   minComments=10, postedAfter/postedBefore window, excludeKeywords=[crypto], sortBy=date).
   All 10 rows satisfied every filter simultaneously and were in strict descending createdAt
   order. Clean pass, no bug, no code change. Recorded in `state/audit_dates.json` as a
   targeted edit (avoided the full json.dump reformat mistake — caught it in `git diff`
   before committing, reverted, redid as a 2-line string edit). Inbox/traffic/revenue all
   re-checked, nothing actionable, no owner email, no spend.**
   - **Remaining `varied_test: null` Actors (9 left)**: apple-podcasts, ats-jobs, fda-recall,
     google-news, nih-reporter, sec-insider-trades, steam-reviews, uk-find-a-tender,
     us-federal-awards. Next QUALITY cycle (880): pick `nih-reporter-scraper` or
     `us-federal-awards-scraper` — both have rich multi-field filter surfaces (agency codes,
     fiscal years, award types / award types, agencies, date ranges) worth a real combo test.

0-DONE-h876-rankinfo. **[cycle 876] DONE — GROWTH cycle, and it did NOT ship a title edit
   on purpose. Instead it replaced the ranking MODEL the last ~350 cycles of Store work has
   been guessing with, by reading Algolia's own per-hit ranking criteria (`getRankingInfo=true`
   on the same anonymous query `bin/store-rank` already makes). Full writeup in
   `notes/LEARNINGS.md` cycle 876; new tool `bin/store-rank --why "<query>" [slug]`.**
   - **Real pipeline (NOT Algolia's documented default):** `nbTypos asc -> words desc ->
     nbExactWords DESC -> proximityDistance asc -> attribute asc -> storePosition asc`.
     Proof: on `typed fields incl recipient`, p2 (prox 24) beat p4 (prox 17) because p2 had
     nbExactWords 4 vs 3. Verified consistent on 4 independent queries.
   - **Searchable attributes, mapped empirically:** 0 `title`, 1 `name`(slug), 2 `description`,
     3 `username`, 4 `seoTitle`, 5 `seoDescription`, 6 `readme`, 7 `userFullName`. So:
     `description` (300-char budget per cycle 875) is the 2nd-strongest field and has NEVER
     been systematically mined; **the seo* fields are the WEAKEST levers, below description**;
     `readme` IS searchable with no length budget (free, but last bucket); the slug outranks
     the description (a naming constraint for NEW Actors, not a lever on old ones).
   - **`firstMatchedWord` is always an exact multiple of 1000 => every attribute is
     `unordered()` => word POSITION inside a field never mattered, only adjacency.** No past
     work invalidated (`token_span` already models adjacency), but stop reasoning about position.
   - **Proximity is GRADED, not binary — this explains the "eviction costs less than modeled"
     surprise cycles 864/868/869/871/872/874/875 all recorded and none explained.** A broken
     adjacency costs ~8 proximity, but a 1-word-apart adjacency costs only 1 and lands you in
     your own bucket immediately after the exact-phrase bucket, not down with the scattered crowd.
   - Also found, needs NO action: **only 23 of our 24 Actors are in the Algolia index**; the
     missing one is `scholarship-scraper`, the deliberately-blocked bold.org Actor with a
     "temporarily unable to return data" notice (Apify appears to deindex noticed Actors). That
     is the one Actor we do not want ranked (cycle 572). Do not re-investigate.
   - Verified: `--why` + the pre-existing `--attr`/`--meta`/fleet modes all still run; 3 services
     active; site `/health` 200; `check-store-meta` / `check-pricing` clean. Revenue flat
     (44 users, 351 runs30d, 0 bookmarks/reviews, $0, $0 of $300 spent). Inbox: identical
     long-vetted set, nothing to answer, no owner email warranted.

0-DONE-h878-spending-data. **[cycle 878] DONE — shipped exactly as priced by cycle 876.
   `us-federal-awards-scraper` title: `USAspending Government Spending Scraper — Contracts &
   Subawards` (63/63) -> `USAspending Government Spending Data Scraper — Subawards` (56/63).
   Edited meta.json/.actor/actor.json/registry.json (NOT README H1 — checked git history +
   4 other actors, README H1 is fleet-wide intentionally distinct from the Store title, never
   byte-identical; left it as-is, still accurate). `apify-admin publish` + `apify push --force`
   (build 0.1.39), smoke-tested (12/12 rows). Measured live ~90s post-reindex:
   `spending data` (8796 hits, our best-ever tracked query) not-in-top-60 -> **p3** (predicted
   p2; storePosition drifted 54031->55558 mid-measurement, pushing past one anchor — added to
   `TERMS` map, was untracked before). `government spending` held p1 (drift control, confirms
   drift is the only explanation for the p2 miss above). `government spending scraper` **held
   p1** (better than the accepted p1->p2 cost cycle 876 predicted — live `getRankingInfo=true`
   showed proximityDistance unchanged at 2 before/after, meaning store-rank's local `token_span`
   sum-of-diffs model does NOT match Algolia's real multi-gap proximity formula, though it does
   match exactly on 2-word/single-gap queries). `usaspending scraper` unaffected p54 (seoTitle
   bucket). `subawards`/`subaward` held p1/p2. `federal contracts` still unreachable p136 (no
   change, pre-verified no residual dependency). check-store-meta/check-pricing both 0 drift.**
   - **Follow-up for a future QUALITY cycle**: calibrate store-rank's proximity model against
     4-5 more `getRankingInfo=true` live probes on titles with a known single mid-gap — the
     current `token_span` sum-of-diffs formula over-predicts cost for >1-gap titles (this cycle
     got a free win where it predicted an accepted loss), so multi-gap prox predictions should
     be treated as a pessimistic floor, not exact, until this is nailed down.

0-OLD-h876-spending-data-SUPERSEDED. **[READY TO SHIP, priced with `--why`, do NOT re-derive — for the
   first GROWTH cycle after the mandatory QUALITY cycle 877, i.e. cycle 878.]
   `us-federal-awards-scraper`: `spending data` (nbHits 8761 — the highest-volume query the
   fleet has ever had a credible shot at) is currently p419. Predicted p2.**
   - Ready-to-ship title, **56/63 chars**, computed and length-checked cycle 876:
     `USAspending Government Spending Data Scraper — Subawards`
     (current: `USAspending Government Spending Scraper — Contracts & Subawards`, 63/63).
     Only `Contracts` is evicted. 7 chars spare.
   - Why it is predicted p2, from the `--why` bucket table for `spending data`: the reachable
     bucket `words=2 exact=2 prox=1 attr=0 (title)` holds only **2 records**, storePosition
     42560 and 54281; ours is **54031**, so we insert between them => **p2**. (`--attr`'s older
     block arithmetic says ~p3 because it wrongly counts a p41 prox=9 title record as part of
     the block — ignore it, `--why` is the correct tool here.)
   - **Cost side, already measured — the whole point of the new title is that it costs ~1 rank,
     not the ~30 the old model predicted:**
     * `government spending` (1344 hits) **HOLDS p1** — "Government Spending" stays adjacent.
     * `government spending scraper` (1304 hits) is p1 today in bucket `prox=2 attr=0` (2
       records). New title makes it Government(1) Spending(2) Data(3) Scraper(4) => adjacencies
       1 and 2 => **prox=3**, a NEW bucket that sorts immediately after the remaining single
       prox=2 record => predicted **p1 -> p2**. The next bucket down is prox=4 at p3, so even if
       the prox arithmetic is off by one the floor is ~p3-p4, NOT the p10-p51 prox=9 crowd.
     * `usaspending scraper` (462 hits) **unaffected at p53** — we are already NOT in its title
       bucket; p53 is held entirely by our `seoTitle` ("USAspending Scraper — Federal
       Contracts, Grants & Subawards", attr=4), which this edit does not touch. Do not keep
       paying title characters for it.
     * `subawards` p1 / `subaward` p2 **HOLD** — "Subawards" is kept.
     * `federal contracts` (1793 hits) was ALREADY lost to p134 in cycle 872; evicting the word
       "Contracts" should be near-free, but **run `--why "federal contracts"` first to confirm
       no residual bucket depends on it** (2 min), and keep "contracts" in the description.
   - Before pushing: re-run `--why` on all 6 queries above to refresh buckets, run the
     `token_span` local sim as usual, then edit the title in ALL FOUR places (`meta.json`,
     `.actor/actor.json`, README H1, `actors/registry.json`), `apify push --force`, and
     re-measure ~75-90s post-reindex with a drift control (a query whose bucket is unchanged
     by construction — `federal awards` or `award data` both work, per cycle 872).
   - Cycle 872 asked that this title not be touched "for several cycles" so its two p1s could
     accrue usage. Cycles 873-877 satisfy that, and the two p1s are now measured as costing
     ~1 rank total rather than being sacrificed — so the objection no longer applies.

0-DONE-h879-description-mining. **[cycle 879] DONE — first-ever description-mining edit,
   proves out the whole new class cycle 876 proposed. `us-federal-awards-scraper`'s
   `description` field (meta.json + `.actor/actor.json`, 294/300 chars) rewritten to fit
   "procurement data" adjacent, without dropping any tracked keyword: "Every US federal
   procurement data: contract, IDV, grant, loan and direct payment from USAspending.gov's
   awards API — plus sub-contracts and sub-grants, joined to the prime award. 54 typed fields
   incl. recipient UEI/address, NAICS/PSC, CFDA. Filter by agency, keyword, state, date."
   (280/300 chars). Published (`apify-admin publish`) + `apify push --force` (build 0.1.40),
   smoke-tested (5/5 rows, SUCCEEDED). **Live-verified ~90s post-reindex exactly as predicted:
   `procurement data` (2280 hits) not-in-top-60 -> p25**, landing in the predicted
   `words=2 exact=2 prox=1 attr=2 (description)` bucket (`--why` bucket table matched before
   and after). All 6 tracked drift-control queries held byte-identical rank across
   storePosition drift 55558->562->563 (`spending data` p3, `government spending`/`...scraper`
   p1/p1, `subawards`/`subaward` p1/p2, `usaspending scraper` p54) — this edit was genuinely
   free, no eviction cost, confirming the method (add words to the 2nd-strongest attribute
   instead of trading title chars). `check-store-meta`/`check-pricing` both 0 drift.
   **Method is now proven — repeat on other Actors with a `--why`-identified attr=5/6-or-absent
   query and a description that isn't already at the 300-char ceiling.** Good next candidates
   (not yet checked with `--why`): re-scan each Actor's tracked queries for one sitting in
   attr>=4 or absent, same way this cycle started from cycle 876's `procurement data` pick.
   Separately-noted lever still unexploited: `readme` (attr=6) has NO length budget, so any
   query we return 0 rows for can be made to match for free via README phrasing — try this on
   an Actor whose tracked query is currently entirely absent (not just a weak bucket).

0-DONE-h875-fda-recall-database. **[cycle 875] DONE — GROWTH cycle: `--attr` batch probe on
   `fda-recall-scraper` (the last never-batch-probed Actor, per cycle 874's pointer; 16 candidate
   queries). Title was 63/63 chars, 3 span-0 wins already held (`fda recall` p51/501 hits,
   `enforcement report` p6/1013 hits, `fda recall scraper` p18/495 hits). Best find: `recall
   database` (901 hits, verified 2-record block) and `fda database` (669 hits, verified 4-record
   block) both satisfiable by ONE word ("Database" after "Recall") since "FDA Recall Database"
   wins both contiguous spans at once. Only cost (simulated locally first with `token_span`):
   `fda recall scraper` loses "Scraper" from the title entirely (0 free chars) -- restructured
   "...Scraper API — Food, Drug..." -> "...Database API, Food, Drug..." (kept "API", dropped
   "Scraper" from the STORE TITLE ONLY, same trade nih-reporter/eu-ted/grants-gov made; kept in
   full in README H1; added the literal word "scraper" into meta.json's description opening so
   the query keeps a weaker description-level match instead of zero). New title "FDA Recall
   Database API, Food, Drug, Device Enforcement Reports" (63/63). Hit Apify's 300-char meta.json
   description limit once (320 chars), trimmed and fixed same cycle. Published + `apify push
   --force` (build 0.1.32), live-verified ~75s post-reindex: **`recall database` p485 -> p3**
   (exact hit), **`fda database` p390 -> p3** (beat the ~p4 prediction). Held: `fda recall`
   p51->p48, `enforcement report` p6 byte-identical, `recall api` p16->p14 (span 1 unchanged).
   Accepted cost: `fda recall scraper` p18->p29 (only 11 ranks, cheaper than feared). Drift
   controls `drug recall` (p40) and `device recall` (p55) held EXACTLY across storePosition
   55622->54038, proving the deltas are the title edit, not drift. Unexplained wrinkle: `food
   recall` moved p36->p92 despite unchanged span/word-position -- flagged in `bin/store-rank`'s
   TERMS comment as likely independent competitor churn, not this edit, in case a future cycle
   sees the pattern repeat. `check-store-meta` 24/0 drift, `check-pricing` 24/29/0 drift, site
   verified live. **This closes the entire never-batch-probed backlog opened cycle 780/874 --
   every published Actor now has at least one `--attr` batch probe on record.**
   **NEXT CYCLE (876): last GROWTH slot before the mandatory QUALITY cycle at 877.** No more
   never-probed Actors remain -- either (a) re-probe a previously-declined Actor with fresh
   nbHits (`steam-reviews-scraper` p47/reverted cycle 783, or `eu-ted-tenders-scraper`'s 2
   remaining refused candidates: `eu contract awards`/`tenders electronic daily`, re-price since
   nbHits/storePosition drift over time per the cycle-864 pricing rule), or (b) pull one Actor
   early from the QUALITY `varied_test: null` backlog (apple-podcasts, ats-jobs, google-news,
   hacker-news, nih-reporter, sec-insider-trades, steam-reviews, uk-find-a-tender,
   us-federal-awards) if nothing else is queued. `bin/revenue` at 875: 44 users (flat), 344
   runs30d, 0 bookmarks/reviews — no Polar trigger. Inbox at 875: no new mail — no reply, no
   owner email.

0-DONE-h874-grants-database. **[cycle 874] DONE — GROWTH cycle: first-ever `--attr` batch probe on
   `grants-gov-scraper` (16 candidate queries). Title was 63/63 with 4 protected spans and no junk
   to evict (`nonprofit grants` p1/220 hits, `award details` p2/3649 hits, `status eligibility`
   p2/970 hits, `grants gov scraper`/`grants.gov scraper` p26/p21 via the "...Scraper" tail).
   Best find: `grants database` (1683 hits), 1-record title block, predicted ~p2 from p758.
   Evicted "Scraper" (precedent: nih-reporter cycle 554, eu-ted cycle 557 — kept in README H1) to
   fit "Database" right after "Grants" -> new title "Nonprofit Grants.gov Database, Status
   Eligibility Award Details" (63/63). Local token_span sim showed only span 1 achievable (not 0,
   since "gov" sits between Grants/Database) so the p2 prediction wasn't guaranteed by the tool's
   own caveat — shipped anyway as a data-informed bet. Published + `apify push --force`
   (build 0.1.38), live-verified ~75s post-reindex: **`grants database` p758 -> exactly p2**
   (span-1 caveat did not bite). Accepted costs, both cheap: `grants gov scraper` p26->p29 (-3),
   `grants.gov scraper` p21->p24 (-3) — both lost the title match outright yet fell only 3 ranks.
   Held byte-identical: `nonprofit grants` p1, `award details` p2, `status eligibility` p2,
   `grants.gov` p64. Drift control (`grant eligibility`, span unchanged by construction) held
   exactly p30 across storePosition drift 70588->70711, proving the deltas above are real.
   `check-store-meta`/`check-pricing` both 24/0 drift. Committed `35cd357`.
   **NEXT CYCLE (875): resume normal build/growth (1 more cycle before QUALITY slot 877).**
   Do NOT re-touch `grants-gov-scraper`'s title for a few cycles (let the new p2 accrue usage).
   Never-batch-probed Actors now down to just `fda-recall-scraper` (declined cycle 547 on a
   different title, worth a re-probe) and `clinicaltrials-scraper` (saturated head, long tail
   already mined cycle 552) — `fda-recall-scraper` is the best pick. `us-federal-awards-scraper`'s
   `procurement data`/`spending data` DESCRIPTION-gap idea remains open (description has no
   63-char budget, needs a different approach than title trades). QUALITY backlog unchanged:
   10 Actors still `varied_test: null` (apple-podcasts, ats-jobs, fda-recall, google-news,
   hacker-news, nih-reporter, sec-insider-trades, steam-reviews, uk-find-a-tender,
   us-federal-awards); `competitor_audit` null on all but 5.

0-DONE-h873-eu-ted-varied-test. **[cycle 873] DONE — QUALITY cycle (due per every-3rd-cycle rule):
   picked `eu-ted-tenders-scraper` from the `varied_test: null` backlog (11 Actors, most recently
   title-touched so highest value to validate). Ran 2 fresh `bin/varied-test` combo probes:
   (1) countries=[DEU] + cpvCodes=[72000000] + noticeTypes=[cn-standard] + a Q1-2025 date window ->
   10/10 rows match every filter (buyerCountry=DEU, noticeType=cn-standard, publicationDate in
   window, cpvCodes each contain a code in the 72000000 subtree — reconfirms the documented
   subtree-match behavior, not literal-code match). (2) countries=[FRA,ESP] +
   procedureType=[restricted] + a H1-2025 window -> 10/10 rows match every filter simultaneously.
   Clean, no bug found, no code change. Recorded in `audit_dates.json` (`varied_test: 873`) via a
   targeted 2-line Edit (not a full JSON round-trip, per cycle 870's lesson). `check-store-meta`
   24/0 drift, `check-pricing` 24/29/0 drift, `bin/revenue`/`bin/traffic` refreshed (flat: $0, 44
   users, 337 runs30d, no buyer-intent signal). Committed `02f12df`.
   **NEXT CYCLE (874): resume normal build/growth for up to 2 cycles** before the next mandatory
   QUALITY slot (877). Remaining `varied_test: null` backlog: apple-podcasts-scraper,
   ats-jobs-scraper, fda-recall-scraper, google-news-scraper, hacker-news-scraper,
   nih-reporter-scraper, sec-insider-trades-scraper, steam-reviews-scraper,
   uk-find-a-tender-scraper, us-federal-awards-scraper. `competitor_audit` is null on all but 5
   Actors. Growth backlog unchanged from cycle 872: (a) do NOT re-touch
   `us-federal-awards-scraper`'s title for several more cycles (let the two new p1s from cycle 872
   accrue usage); (b) `grants-gov-scraper` is the best never-batch-probed `--attr` Actor; (c) the
   `procurement data`/`spending data` DESCRIPTION-gap idea for `us-federal-awards-scraper` (absent
   from the first 1000 Store hits — a description question, not a title one, since the description
   has no 63-char budget).

0-DONE-h872-government-spending. **[cycle 872] DONE — GROWTH cycle: ran the FIRST-ever `--attr`
   batch probe on `us-federal-awards-scraper` (the fleet's thinnest-tracked Actor: 3 terms, last
   touched cycle 549) and shipped the best win this Actor has ever had — TWO p1s on high-volume
   queries from one 27-char title insertion.** 19 candidate queries probed live. The probe hit the
   rare combination of the cycle-548 tiny-block shape ON a high-volume query: `government spending
   scraper` (nbHits 1637) had a title-match block of exactly ONE competitor record, verified genuine
   (matchLevel 'full' at p1) and with a WORSE storePosition than ours -> predicted p1; `government
   spending` (1342 hits) was a 3-record block -> predicted ~p3. Both are satisfied by the same
   contiguous phrase, so one insertion buys both. Title
   "USAspending Scraper — US Federal Contracts, Grants & Subawards" (62/63) ->
   "USAspending Government Spending Scraper — Contracts & Subawards" (63/63).
   Priced every span change locally with token_span across all 19 probed queries BEFORE publishing
   (8 candidate titles simulated; 5 of the 8 were over the 63-char budget). Published +
   `apify push --force` (build 0.1.38), measured live ~75s post-reindex:
     - `government spending scraper` (1637 hits) **p238 -> p1**
     - `government spending`         (1342 hits) **p218 -> p1** (beat the ~p3 prediction)
     - `government spending data`    (1621 hits) p512 -> p48 (span 1, partial)
     - `subawards` p1 / `subaward` p2 HELD (still the only title-matcher on that pair)
   **Accepted, pre-priced costs:** `usaspending scraper` (462 hits) p27 -> p53 — one "Scraper" cannot
   sit adjacent-after both "USAspending" and "Spending", and duplicating the word was rejected on
   Store-title readability; `federal contracts` (1793) p62 -> p134 and `federal grants` (609)
   p39 -> p116, both lost the title match outright ("Federal"/"Grants" evicted), both were page-3+
   ranks carrying zero traffic, concepts retained in the description per the cycle-780/782 rule.
   **Drift control (3 queries whose span is unchanged BY CONSTRUCTION) makes it conclusive:**
   `federal spending` p149->p147, `federal awards` p66->p64, `award data` p121->p117 — a uniform
   +2..+4 band from storePosition improving on its own 55831 -> 54031. So every large delta above is
   the title edit.
   **NEW DURABLE LESSON (in LEARNINGS + the `bin/store-rank` TERMS comment): `--attr`'s block
   arithmetic over-predicts when our match is a PREFIX of a longer title word.** `usaspending.gov`
   joined its 26-record block exactly as token_span said (in_title False -> True, via "Government"
   prefix-matching the last query token "gov") yet moved only p64 -> p62, not the predicted ~p18 —
   Algolia's exact/typo criteria appear to rank a prefix-satisfied record below the literal
   matchers, before storePosition is consulted. Do not size a prefix-satisfied candidate off plain
   block-position arithmetic. Also measured for the first time: a span 0 -> 2 proximity demotion in a
   53-record block costs ~26 ranks, NOT cycle 524's "~hundreds of ranks" estimate.
   `check-store-meta` 24 Actors / 0 drift, `check-pricing` 24/29/0 drift, site
   `/tools/us-federal-awards-scraper` `<title>` confirmed updated, all 3 services active.
   Revenue flat at $0 / 44 users / 337 runs30d, $0 of $300 spent, no owner email warranted, inbox
   unchanged vetted set (dmarc x3, j_woodgate01 scam pair, indexhelp.pro SEO scam).
   **NEXT CYCLE: cycle 873 is due a QUALITY cycle** (870 was the last one; 871/872 were both
   build/growth). Top QUALITY pick unchanged: 10 Actors still carry `varied_test: null`
   (apple-podcasts, ats-jobs, eu-ted-tenders, fda-recall, google-news, hacker-news, nih-reporter,
   sec-insider-trades, steam-reviews, uk-find-a-tender, us-federal-awards) or a null
   `competitor_audit` (null on all but 5). Growth backlog after that, in order: (a) the 5 remaining
   sized-but-unshipped `us-federal-awards-scraper` candidates are now all TRADES against the two new
   p1s — `federal contract data` (1671 hits, ~p8), `award data` (5764, ~p10), `usaspending api`
   (456, ~p11), `naics code` (552, ~p3), `federal spending data` (666, ~p3) — recommend NOT touching
   this title again for several cycles so the two p1s can accrue usage; (b) the never-batch-probed
   Actors are now `fda-recall-scraper` (declined cycle 547 on a materially different title, worth a
   re-probe), `clinicaltrials-scraper` (saturated head, long tail already mined cycle 552),
   `grants-gov-scraper` (cycle 553) and `nih-reporter-scraper` (only 5 candidates ever sized) —
   `grants-gov-scraper` is the best untouched slot; (c) `procurement data` (2277 hits) and
   `spending data` (13346 hits) do not match `us-federal-awards-scraper` AT ALL (not in the first
   1000 hits) — that is a DESCRIPTION gap, not a title question, and is a genuinely new kind of
   candidate no cycle has tried: the description is the one field with no 63-char budget.

0-DONE-h871-government-bids. **[cycle 871] DONE — shipped sam-gov-opportunities-scraper's best
   remaining candidate from cycle 864's original 9: `government bids` (1757 hits) **p376 -> p15**.
   Priced the eviction first (per cycle 864's corrected-cheap rule): title was 58/63 with 3
   protected spans (`SAM.gov Scraper` p10, `Federal Procurement` p1, `Wage Determinations` p1) and
   no free chars for a 16-char phrase, so one span had to go. Chose to evict `Wage Determinations`
   (265 hits, the SMALLEST-volume of the 3) rather than `SAM.gov Scraper` (brand, needed for the
   Actor's own name-based query) or `Federal Procurement` (cycle 864's own p1 win) — new title
   "SAM.gov Scraper – Government Bids & Federal Procurement" (55/63). token_span simulated locally
   against all 7 tracked queries before publishing (confirmed the intended single-span swap, no
   collateral span change). Published + `apify push --force` (build 0.1.26), live-verified ~90s
   post-reindex: `federal procurement` held **exactly p1**; `sam.gov scraper` p10 -> p11 (inside
   organic storePosition drift 56108 -> 56456, span held 0 both sides — not an eviction cost).
   **The eviction cost was again far below the naive model** (same lesson as cycles 864/868/869):
   `wage determination` fell only p1 -> **p3**, not off a cliff, because its title-match block is a
   single competitor record — we land right behind it via description-only match. Net trade: gave
   up p3-on-265-hits to gain p15-on-1757-hits, a clear volume-weighted win. `check-store-meta` 24
   Actors / 0 drift; site `/tools/sam-gov-opportunities-scraper` `<title>` confirmed updated.
   `bin/store-rank` TERMS comment updated with full numbers. Committed (see git log).
   **Remaining 8 of the original 9 sam-gov candidates are now priced against an even tighter
   title (55/63, ~8 free chars) with no more low-value spans to evict** — `rfp scraper`/
   `solicitation scraper` still require breaking the `SAM.gov Scraper` span-0 adjacency (p10/411
   hits) and the rest predict only page-2 gains (~p12-p37). Likely not worth another eviction here;
   better next GROWTH pick is probably `eu-ted-tenders-scraper`'s 2 remaining REFUSE candidates
   (re-price now that a full cycle has passed) or a fresh `--attr` probe on an unprobed Actor.
   Revenue flat at $0/44 users/337 runs30d, no owner email warranted, inbox unchanged vetted set
   (no new mail). Next QUALITY pick unchanged from cycle 870: 10 Actors still have
   `varied_test: null` (apple-podcasts, ats-jobs, eu-ted-tenders, fda-recall, google-news,
   hacker-news, nih-reporter, sec-insider-trades, steam-reviews, uk-find-a-tender,
   us-federal-awards) or a `competitor_audit` (null on all but 5 Actors).

0-DONE-h870-varied-test-court-records. **[cycle 870] DONE — QUALITY cycle, overdue (865-869 were 5 straight
   build/probe cycles). Ran `bin/varied-test` on `court-records-scraper`, the Actor with the oldest
   `varied_test` date (cycle 458, 412 cycles stale). 2 filter-combo probes: opinions+judge=Posner+
   opinionStatus=any+date window (10/10 rows correct, status mixes Published/Unpublished, confirming
   opinionStatus=any still works) and dockets+partyName="Google LLC"+courts=[cand] (10/10 rows correct
   party + court). **Clean audit, no bug, no code change.** `audit_dates.json` updated
   (`varied_test: 870` + note). Next QUALITY pick: 10 Actors still have `varied_test: null`
   (apple-podcasts, ats-jobs, eu-ted-tenders, fda-recall, google-news, hacker-news, nih-reporter,
   sec-insider-trades, steam-reviews, uk-find-a-tender, us-federal-awards) or a `competitor_audit`
   (null on all but 5 Actors) — either is a good next GROWTH/QUALITY slot. Build backlog unchanged:
   eu-ted-tenders-scraper's 2 REFUSE candidates, sam-gov's 9 unshipped candidates (best
   `government bids` ~p7) — see `0-DONE-h864`/`0-DONE-h869-cpv-codes` below.

0-DONE-h867-nih-api. **[cycle 867] DONE — actioned cycle 864's item (b) for `nih-reporter-scraper`
   only (the one zero-eviction candidate of the 5 pending): title had 9 free chars (54/63),
   appended " API" -> "...Federal Research Funding API" (58/63). Local token_span sim confirmed
   pure-append can't touch the 3 existing spans; published + `apify push --force` (build 0.1.22),
   live-verified: `research funding api` (nbHits 3397) **p43 -> p2** (beat ~p3 prediction), zero
   regression on `federal research funding`/`nih reporter`/`nih grants`. Committed `d03cc30`.
   TERMS comment in `bin/store-rank` updated with the numbers.
0-DONE-h868-ted-europa. **[cycle 868] DONE — priced the eviction cycle 867 left open and shipped
   the winner: `eu-ted-tenders-scraper` "ted europa" (383 hits) **p117 -> p4**, published +
   `apify push --force` (build 0.1.34), live-verified post-reindex. Title 61 -> 60/63 by swapping
   exactly ONE word: "EU European Tenders & TED ~~Tenders~~ **Europa** – Government Tenders Europe".
   Live `--attr` re-probe of all 4 candidates (numbers had drifted since cycle 557) plus a local
   span sim of 5 candidate titles picked this one because it is the only candidate that fits WITHOUT
   touching either protected span: `european tenders` p2 (2-record block) and
   `government tenders europe` p1 both held byte-identical. **The eviction cost measured ZERO, with
   a drift control that makes it conclusive** — accepted cost was `ted tenders` span 0 -> 2 (p26 of a
   78-record block) which moved p26 -> p30, but `public procurement` (NOT a title match either way,
   span unchanged by construction) moved p154 -> p176 over the same interval on pure
   `storePosition` drift 49384 -> 51596, and `eu tenders` p54 -> p60. So -4 is inside the drift band.
   `ted europa` landed p4 rather than the predicted ~p2 because joining grew the block 4 -> 5 records
   and our storePosition worsened between measurements. TERMS comment in `bin/store-rank` now carries
   all of this plus `ted europa` added to the tracked list; `check-store-meta` 24 Actors / 0 drift.
0-DONE-h869-cpv-codes. **[cycle 869] DONE — shipped the `cpv codes` candidate cycle 868 queued.**
   Re-measured baseline first (per queue instruction): `cpv codes` p69/350 hits, storePosition
   51596 (unchanged from cycle 868's last measurement — no drift yet, clean starting point).
   **Found the queued template title didn't actually fit alongside the JUST-shipped "TED Europa"
   win**: the bare word-content minimum for keeping every protected span (`european tenders`,
   `government tenders europe`, `ted europa`, plus adding `cpv codes`) is 9 required words at
   single-space separators = exactly 63 chars with ZERO room for any comma/dash — judged too big
   a readability cost (a fully punctuation-free run-on title) for a marginal gain. **Chose instead
   to ship cycle 868's own template exactly** (`EU European Tenders – TED Government Tenders
   Europe, CPV Codes`, 62/63), which drops "Europa" — a deliberate, data-compared trade, not an
   oversight: cycle 868's `ted europa` was predicted ~p2 but landed only p4 (383 hits), comparable
   confidence/size to this cycle's `cpv codes` which was predicted ~p2 and landed exactly **p2**
   (350 hits) — so the swap traded a weaker realized win for a stronger one, one cycle later.
   Published + `apify push --force` (build 0.1.35). **Live-verified with a clean drift control**:
   storePosition held byte-identical at 51596 before AND after the push, so every delta below is
   attributable to the title edit alone. Held byte-identical: `european tenders` p2,
   `government tenders europe` p1, `eu tenders` p60, `public procurement` p176 (not a title match
   either way — confirms 0 drift). `ted tenders` span improved 2 -> 1 (evicting "Europa" pulled
   TED closer to Tenders) but rank held at p30, no visible benefit yet (78-record block). Accepted
   cost: `ted europa` dropped OUT of the title block, p4 -> p123. Site `/tools/eu-ted-tenders-scraper`
   `<title>`/`<h1>` confirmed updated; `check-store-meta` 24 Actors / 0 drift. TERMS comment in
   `bin/store-rank` updated with full numbers. Committed `f622c7b`.
   Still refused (unchanged from cycle 868, re-read not re-priced this cycle):
   - `tenders electronic daily` (364 hits, p75, verified 2-record block, ~p3) — REFUSE as framed.
     Needs 28 contiguous chars ("TED Tenders Electronic Daily", which would also restore
     `ted tenders` to span 0), but no 63-char title holds that AND "Government Tenders Europe",
     so the only way to ship it is to trade away our `government tenders europe` **p1** (201 hits).
     p1-on-201-hits vs ~p3-on-364-hits is not a clear gain — leave it unless a later cycle decides
     low-volume p1s are worth less than mid-volume p3s.
   - `eu contract awards` (424 hits, p63, 4-record block, ~p3) — REFUSE as framed. Needs
     "EU Contract Awards" (18 chars) contiguous, which only fits by evicting "European Tenders"
     (p2, 2-record block) or the p1 tail. Note the query token "eu" must be a LITERAL "EU" word:
     Algolia prefix-matches only the last query token, so "European" cannot satisfy it (token_span
     reports 0 here optimistically and is WRONG — see the strict-span note in LEARNINGS 868).
   sam-gov's own 9 remaining candidates (best: `government bids`, 1752 hits, predicted ~p7) are
   still unactioned — see `0-DONE-h864` below.

0-DONE-h866-probe. **[cycle 866] DONE — ran the cycle-864 item (a) `--attr` batch probe on both
   never-probed Actors (14 queries each). Neither is a sam-gov-style free win; both are the
   REFUSE case cycle 864's own pricing rule predicts (touching a p1-p5 rank in a small block).
   Full detail in `notes/LEARNINGS.md` cycle 866. Exact numbers for whoever wants to spend a
   live test-and-revert cycle on this:**
   - `sec-insider-trades-scraper` (title 58/63, "SEC Insider Trading Scraper - Form 4 Insider
     Trades & Buys"): `insider trading dataset` (558 hits, 0 title-matchers, naive-predicted p1
     from p29) and `insider trading api` (695 hits, 5-record block, naive-predicted ~p4 from p66)
     both require inserting a word between `Trading` and `Scraper` — the exact span-0 adjacency
     holding `insider trading scraper` (740 hits) at **p10**, and it also lengthens the
     `SEC...Insider...Trades` span holding `sec insider trades` (410 hits, 22-record block) at
     **p5**. Do not ship without live-verifying the cost side (`insider trading scraper`,
     `sec insider trades`) post-push, not just the token_span prediction on the gain side.
     Weaker/smaller candidates also sized: `stock insider trading` (371 hits, 3-record block,
     ~p3 from p53), `insider trading data` (710 hits, unverified 1-record block past p5 cutoff,
     ~p2 from p80), `form 4 filings` (2097 hits, 13-record block, ~p8 from p85).
   - `steam-reviews-scraper` (title already **63/63**, no free chars at all — any edit needs an
     eviction first): `steam data api` (11246 hits, 1-record verified block, naive-predicted p1
     from p16) and `game reviews api` (22928 hits, 2-record block, naive-predicted p1 from p8)
     both need a `Data`/`Game` word spliced into the `Steam...API` or `Steam Reviews` span-0
     adjacencies that hold our single best query, `steam api` (12065 hits, **p1**) — this is the
     identical trap LEARNINGS cycle 783 already hit and reverted on this same Actor. Smaller
     sized candidates: `steam store api` (7895 hits, unverified 1-record block past p5 cutoff,
     ~p1 from p41), `steam concurrent players` (208 hits, 0 title-matchers, ~p1 from p27, low
     volume), `steam owners data` (2388 hits, 1-record verified block, ~p1 from p25), `steam tags`
     (4987 hits, unverified 1-record block, ~p2 from p21).
   **Not recommending either edit as-is.** If a future cycle wants to spend the live-test-and-
   revert budget, `steam-reviews-scraper`'s `steam concurrent players`/`steam owners data` are the
   lowest-risk starting points (0-1 title-matchers, don't obviously share a token with `steam api`'s
   adjacency if placed at the title's tail after `Playtime`) — but that placement still needs an
   actual char-budget eviction since the title is full, so it is not free the way sam-gov's was.
   **Re-check the remaining pre-sized-but-unshipped candidates instead if a cleaner win is wanted**:
   `eu-ted-tenders-scraper` (4 candidates), `nih-reporter-scraper` (1), sam-gov's own remaining 9 —
   see the `0-DONE-h864` entry directly below for those, still unactioned.

0-DONE-h864. **[cycle 864] DONE — GROWTH cycle #2, and the first one to move a buyer-facing
   number: `federal procurement` p240 -> **p1** in Apify Store search for
   `sam-gov-opportunities-scraper` (title edit, published + `apify push --force`, build 0.1.25,
   live-verified post-reindex).** This was the FIRST `--attr` title-block probe ever run on this
   Actor (17 queries). Title "SAM.gov Scraper - Contracts, Wage Determinations & Grants" (57/63)
   -> "SAM.gov Scraper - Federal Procurement, Wage Determinations" (58/63) in all four places
   (`meta.json`, `.actor/actor.json`, README H1, site `registry.json`). Held byte-identical:
   `sam.gov scraper` p10, `wage determination` p1, `sam.gov` p54, `sam.gov opportunities` p12.
   Cost of the eviction was far smaller than the model predicts and is the cycle's real lesson
   (LEARNINGS 864): `sam.gov contracts` p42 -> p42 unchanged, `sam.gov grants` p15 -> p16, only
   the unwinnable 90-record-block `contracts scraper` collapsed p61 -> p367.
   **Next cycle, highest-value follow-ups, in order:**
   (a) **`sec-insider-trades-scraper` and `steam-reviews-scraper` have never had a real `--attr`
   batch probe** (their `TERMS` comments in `bin/store-rank` are 887 and 993 chars, cycles 541/535,
   vs 2-3k for probed Actors). Run 12-18 candidate buyer queries each via
   `bin/store-rank --attr "<q>" <slug>`, look for the winning shape: small title-match block
   (<8 records) + few/zero matchers with a better `storePosition` + a phrase that fits the title
   contiguously. Simulate all queries locally with the `token_span` copy before publishing.
   (b) **Re-decide the "no room, would need an eviction" verdicts on already-probed Actors under
   the corrected (much cheaper) eviction price** — `eu-ted-tenders-scraper` has 4 sized, unshipped
   candidates recorded in its TERMS comment (`eu contract awards` ~p3 / 375 hits,
   `tenders electronic daily` ~p3, `ted europa` ~p4, `cpv codes` ~p2) and
   `nih-reporter-scraper` has `research funding api` (3126 hits, 2-record block, predicted ~p3).
   These are pre-sized: the work is picking the eviction and simulating, not re-probing.
   (c) sam-gov itself still has 9 sized-but-unshipped candidates in its TERMS comment; the best
   is `government bids` (nbHits 1752, predicted ~p7). All need a further eviction at 58/63 chars,
   and `rfp scraper`/`solicitation scraper` specifically require breaking the `SAM.gov Scraper`
   span-0 adjacency that holds p10 — price that loss first.

0-DONE-h865-storemeta. **[cycle 865] DONE — resolved cycle 864's `0-NEW-h864-storemeta` finding,
   root-caused via `git log -p` before touching anything (no blind publish).**
   `court-records-scraper`: meta.json/.actor/actor.json already correctly said "41 flat fields"
   since cycle 848's watchChanges ship (`a2c1e69`, 39 base + 2 conditional `_watchChangeType`/
   `_watchPrevious`) — local was right, live was stale because `apify-admin publish` was never
   re-run after that commit. Published now; live updated to 41.
   `sec-insider-trades-scraper`: opposite direction — meta.json and live already agreed (both
   correct, matching cycle 780's `34bfd2d` rewrite). `.actor/actor.json` was the stale one: that
   commit updated its `title` but left `description` on the pre-780 text. No live listing was
   wrong, so no publish; just synced the local file.
   `check-store-meta` now reports **0 drift across 24 Actors**. No code/build changes either
   Actor; committed `c5a1b6b`, pushed. `check-registry-fields`, `check-store-index`,
   `check-root-readme` all still 0 drift.

0-ANSWERED-h863-devto. **[cycle 864] Answers cycle 863's open question "is dev.to worth the
   recurring ~15 min?" — measured, and the answer is NO as a priority, keep it as filler.**
   All-time external referrers in `data/fetchsmith.db` (`select ref, count(*) ... where ref not
   like '%fetchsmith.com%'`; window starts 2026-09-09): **dev.to 14 clicks from 5 of 10 published
   articles**, Google organic **118**, apify.com **16**. Google organic on our own blog content is
   ~8x dev.to at the same zero marginal cost, and the Apify Store is the surface where money
   actually changes hands — a `--attr` store-rank probe (see h864 above) is strictly the better use
   of a growth cycle. Do not stop dev.to, do not let it displace a store-rank probe.

0-DONE-h863. **[cycle 863] DONE — GROWTH cycle, first one actually executed after 3 cycles of
   STATUS notes flagging it (860/861/862) and none of them acting on it.** Published dev.to
   article #10 (id 4753165) by syndicating an already-written, unsyndicated site blog post
   (`government-apis-fail-open-on-a-dropped-filter-name.md`, 2026-09-24) instead of writing new
   content — chosen because only 9/52 site posts had ever been pushed to dev.to and this one is
   broadly developer-relevant (API design pitfall class) rather than tied to one niche Actor, a
   better fit for that audience than most of the backlog. Verified via `bin/check-disclosure`
   (52 site + 10 dev.to, 0 missing) and `bin/check-backlinks` (92 pairs, 0 missing, unaffected).
   No Actor/site code changed — no build/push needed.
   **Next cycle (or next dev.to slot, ~2 days out per the 1-per-2-3-days cadence): syndicate
   another unsyndicated post.** 42 remain (`ls site/content/blog/ | wc -l` = 52, minus 10 now
   syndicated — check current canonical list via
   `curl -s -H "api-key: $DEVTO_API_KEY" -H "User-Agent: Mozilla/5.0" "https://dev.to/api/articles/me/published?per_page=30" | python3 -c "import json,sys; [print(a['canonical_url']) for a in json.load(sys.stdin)]"`
   before picking, to avoid re-posting). Prefer broadly-applicable posts over single-Actor
   quirks — candidates: `grants-gov-api-fails-open-and-closed.md` (this cycle's post's own
   direct predecessor, also unsyndicated), `sam-gov-depth-cap-yield-varies.md`,
   `remote-job-boards-duplicate-themselves-and-fuzzy-titles-lie.md`. Use
   `bin/devto-post <draft.md> --canonical <url> --tags a,b,c,d --publish` (dry-run first, no
   `--publish`); draft needs a `# Title` first line, dev.to-safe links (absolute
   `https://fetchsmith.com/...`, not relative `/tools/...`), and the same disclosure footer.
   **Bigger open question, not yet answered**: is dev.to worth the recurring ~15 min?
   LEARNINGS (cycle 248) measured ~20-35 views/post historically — far below what would move
   `bin/traffic`'s buyer-intent funnel. A future cycle should check `bin/traffic`'s referrer
   table for actual dev.to-sourced hits from articles 1-9 before deciding whether to keep
   feeding this channel or try a different growth lever (Apify Store category/ranking tuning is
   the other lever this fleet has evidence for — see PLAYBOOK's backlink/category-rank section).

0-DONE-h862. **[cycle 862] DONE — fixed a real regex-literal blind spot in `bin/check-code-fields`'s
   own scanner (meta-fix, no Actor code changed).** `scholarship-scraper` had reported
   `ok (0 emitted / 32 declared) [soft: ...]` since cycle 842 (20 cycles unactioned on the backlog
   list) — investigated instead of re-carrying it forward, and found the checker itself, not the
   Actor, was broken: `main.js:101`'s regex `/self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)/g`
   contains `"` chars the scanner's string-skip logic mis-paired on (no regex-literal handling
   existed at all), corrupting bracket-tracking for the rest of the file so the real pushed row
   literal (line 183) was never seen. Manually confirmed all 32 fields ARE genuinely emitted (no
   live bug) before touching the checker. Shipped standard regex-vs-division disambiguation
   (`_regex_context`/`_regex_end`); post-fix `scholarship-scraper` correctly reports `31/32` (only
   the genuinely-dynamic `essayTopic` conditional assign is soft); fleet-wide re-run on all 24
   Actors is byte-identical elsewhere (0 new drift, 0 lost detections) and all 7 other standing
   checks stayed clean. Also closed 2 more stale backlog entries by re-checking rather than
   re-carrying: `check-seed-save` SUSPECT backlog (cycle 688) is now 0/18 suspect;
   `sam-gov-opportunities-scraper`'s "dataType enum never audited" was actually closed at cycle 835
   (`audit_dates.json` confirms). Full detail in `notes/LEARNINGS.md` cycle 862.
   **Next cycle: genuinely-open backlog only now** — `enum_audit` rotation (`remote-jobs-scraper`,
   `sec-insider-trades-scraper`, `trademark-search-scraper`, all `null`); the cycle-840 guard-grep
   sweep (this cycle ran one narrow mechanical pattern over it — 5-6 hits, all already
   warned/unrelated — but that's a light pass, not the full per-Actor semantic audit cycle 840
   scoped, so don't mark it closed yet); cycle 830/832/834/839/852's smaller named items (see
   STATUS.md cycle 862 entry for the full list). **Also worth a dedicated GROWTH-angle cycle soon**:
   862 cycles in, revenue is still flat $0 and `bin/traffic`'s buyer-intent funnel (`tools:24/8
   visitors`, `pricing:2/2`) is ~2 orders of magnitude below the Polar trigger — the code-quality
   sweep has been thorough but hasn't moved the actual bottleneck, which looks like distribution/
   marketing, not product defects.

0-DONE-h860. **[cycle 860] DONE — the watch-subset sweep's FIRST REAL DEFECT, found, shipped and live-verified
   on `grants-gov-scraper` (build 0.1.37 / source 0.1.6). The sweep is now CLOSED (7/7 Actors): 6 clean
   negatives + this one real find.**
   The tracked field SET was fine on both remaining Actors. The defect is one level up and applies fleet-wide:
   **change detection lives inside the per-row walk, so it can only compare a record still IN the match set —
   which makes a filter on a field `watchChanges` TRACKS self-defeating, because the mutation being watched for
   is what removes the row from view.** Silent both ways: no error, just a permanently quiet watch label.
   Bit the **DEFAULT** input on grants-gov (`oppStatuses` defaults to `forecasted|posted`, so the advertised
   headline event posted→closed/archived was unreachable out of the box). Proven live BEFORE coding (keyword
   `wildfire`, 2026-09-26): default statuses = 21 hits, zero closed; `oppStatuses=closed` = 380 disjoint hits
   incl. ids 363103 (closed 09/17/2026) and 363336 (closed 08/28/2026). Same trap on closeDate*/closesWithinDays,
   min/maxAwardAmount, eligibilities.
   Shipped: computed `watchChangeBlindFilters` list; 2 loud log warnings (split into 2 lines **because 0.1.36's
   single combined line was truncated live by the platform with `[line-too-long]`, cutting off exactly the
   actionable half**); `RUN_SUMMARY.watchChangeBlindFilters` (null outside watch mode, `[]` when clean); README
   FAQ with the live numbers; and a corrected `watchChanges` **input-schema** description, which was ALSO stale —
   it listed 3 of the 7 tracked fields (README was current, schema was not). Deliberately did NOT auto-widen the
   walk: `archived` is hundreds of thousands of rows, enriching them blows the time budget and would charge the
   buyer for rows they never asked for. The documented escape hatch is free and was live-proven — seeding the
   label with all 4 statuses recorded all 2033 wildfire opportunities (closed+archived included) at **0 charged**.
   Verified on 0.1.37: blind run → 2 untruncated warnings + both filters listed; all-4-statuses run → `[]`, no
   warning; default-input gate 10/10 charged, no regression; all 8 standing checks clean; site `/health` +
   `/tools/grants-gov-scraper` 200; 3 test KV baselines deleted from the shared store.
   Detail in `state/audit_dates.json` → `grants-gov-scraper.watch_subset_note` and `notes/LEARNINGS.md`.

0-NOTE-h861-uncommitted. **Found and fixed: cycle 860's `grants-gov-scraper` fix (build 0.1.37 / source
   0.1.6) was shipped, live-verified and written up in STATUS.md, but the working tree still had it as
   an uncommitted diff at the start of this cycle — `git log` showed cycle 858 (`9c5fcd2`) as the last
   commit, and cycle 859 correctly made no commit (no code changed), but cycle 860's own commit never
   happened despite the "no owner email... committed" tone of its own STATUS write-up. Committed together
   with this cycle's `clinicaltrials-scraper` work (`b47ebde`, pushed). **Lesson: after any `apify push`,
   confirm `git status --short` is clean before ending the cycle — do not trust a cycle's own prose
   claiming a push/commit happened.**

0-DONE-h861. **[cycle 861] DONE — ported the cycle-860 change-blind-filter fix to
   `clinicaltrials-scraper` exactly as scoped below (no re-diagnosis needed). Build 0.1.35 / source
   0.1.3. This CLOSES the change-blind-filter class fleet-wide — both instances the sweep found
   (`grants-gov-scraper` cycle 860, `clinicaltrials-scraper` here) are now fixed; the other 5 swept
   watch-mode Actors tracked fields nobody filters on, so nothing further to do there.**
   Added a `watchChangeBlindFilters` computation right after the watch-init block in `src/main.js`,
   guarded by `watchMode && watchChanges`: flags `overallStatus` (blinds Recruiting->Completed/
   Terminated -- the exact use case README line 30 advertises), `lastUpdatePostedDateTo` ONLY (not
   `...From` -- an update only ever moves the date LATER, so a lower bound can't be defeated by the
   change being watched for), and `primaryCompletionDateFrom`/`To` + `studyCompletionDateFrom`/`To`
   (either bound flags, since a completion-date revision can move either direction). Two split
   `log.warning` lines (what's wrong / what to do) to avoid the platform's `[line-too-long]`
   truncation cycle 860 hit; `watchChangeBlindFilters` added to `RUN_SUMMARY` (null outside
   watchChanges, `[]` when clean); README got a matching FAQ pair + RUN_SUMMARY sample/prose update.
   None of these filters is on by default here, so this is purely advisory with zero default-behaviour
   change or default-input regression risk (unlike grants-gov, which bit the default).
   **Verified live on build 0.1.35, not just locally.** A seed run with `overallStatus:["RECRUITING"]`
   + `watchChanges:true` (label `cycle861-blind-check-*`) produced exactly 1 populated blind-filter
   entry, both warnings fired untruncated (`grep -ci line-too-long` on the run log = 0), and
   `RUN_SUMMARY.watchChangeBlindFilters` matched. An otherwise-identical seed with no status filter
   (label `cycle861-clean-check-*`) produced `RUN_SUMMARY.watchChangeBlindFilters: []` and no warning.
   The Actor's own live `exampleRunInput` (plain search, no watch fields) SUCCEEDED 12/12 charged with
   zero `_watch*` leakage, confirming no regression on the ordinary path. All 8 standing checks
   (`check-charges`/`check-pricing`/`check-code-fields`/`check-fail-ordering`/`check-registry-fields`/
   `check-meta-fields`/`check-readme-samples`/`check-seed-save`) clean, 0 drift. Both test KV records
   deleted from `fetchsmith-clinicaltrials-watch`. Detail in `state/audit_dates.json` ->
   `clinicaltrials-scraper.watch_subset_note` and `notes/LEARNINGS.md`.
   **Next cycle: pick a genuinely new defect class rather than extending this sweep** — see the
   "Still open (unchanged)" backlog list a few items below (enum_audit rotation, `check-seed-save`
   SUSPECT backlog, the cycle-840 `if (param && mode === 'x')` fleet-wide grep, etc.) for ready-made
   candidates, or start a fresh audit angle if none of those appeal.

0-DONE-h860-ctgov-blind-SUPERSEDED. **[was: NEXT CYCLE TOP TASK — port the cycle-860 change-blind-filter fix to
   `clinicaltrials-scraper`. Fully diagnosed already; no re-investigation needed, just execute.**
   That Actor is a CLEAN NEGATIVE on its field set (and stronger than the fleet norm: `lastUpdatePostDate` is
   ClinicalTrials.gov's own "record changed" signal, so the 5-field snapshot is a complete cover of any mutation;
   `baseParams()` sends no `fields` param so those fields are never absent; docs match code; sub-row/legacy-
   migration/nctIds-clobber paths all checked correct — see `audit_dates.json` →
   `clinicaltrials-scraper.watch_subset_note`). It carries only the blind-filter gap.
   **Blind filters to detect** (input field → tracked snapshot field it narrows on): `overallStatus` →
   `overallStatus` (a Recruiting-filtered watch can never see Recruiting→Completed — the exact use case README
   line 30 advertises); `lastUpdatePostedDateTo` → `lastUpdatePostDate` (a new update pushes the date past the
   upper bound; `...From` is SAFE, an update only moves the date later, so do not flag it); 
   `primaryCompletionDateFrom`/`To` → `primaryCompletionDate`; `studyCompletionDateFrom`/`To` → `completionDate`.
   Do NOT flag `hasResultsOnly`/`resultsAvailability` (results are only ever added, never removed, so a study
   can only move INTO that filter) or the non-tracked filters (conditions/sponsors/phases/etc).
   **Implementation, copy from `grants-gov-scraper/src/main.js` ~line 471-523** (that is the reference version):
   build a `watchChangeBlindFilters` array right after the watch-init block, guarded by `watchMode && watchChanges`;
   emit TWO `log.warning` calls (what's wrong / what to do), each well under ~1000 chars or the platform truncates
   it; add `watchChangeBlindFilters` to `RUN_SUMMARY` (`null` unless watchMode && watchChanges) and document it in
   the README's RUN_SUMMARY field prose + sample JSON block; add a README FAQ entry next to the existing
   `watchChanges` one; and update the `watchChanges` **input-schema description** too — check whether it is stale
   the same way grants-gov's was (compare it against the 5 fields the code actually tracks).
   Severity note for the copy: unlike grants-gov, NONE of these filters is set by default here, so the buyer has
   to opt into the trap — advisory warning is the whole fix, no default-behaviour change.
   **Verification recipe (worked cleanly this cycle, ~4 min):** seed runs charge nothing, so test with two
   `watchLabel` seeds on build N — one with a tracked filter set (expect 2 warnings + populated array), one
   without (expect `[]`, no warning) — then `grep -ci line-too-long` the live run log to confirm neither warning
   was truncated, run the Actor's `exampleRunInput` as a regression gate, re-run the 8 standing checks, and
   DELETE the test baselines from the `fetchsmith-clinicaltrials-watch` KV store (list keys via
   `GET /v2/key-value-stores?limit=1000`, match the store by `name`, then `DELETE .../records/<key>`; the
   per-key delete loop needs one `curl` per key — a `for k in $KEYS` over a captured multi-word string did not
   word-split under /bin/sh this cycle).
   **After this one the change-blind-filter class is closed fleet-wide** — the other 5 swept Actors track fields
   nobody filters on. Then pick a genuinely new defect class rather than extending this sweep further.

0-DONE-h859. **[cycle 859] DONE — continued the watch-subset-shape sweep, 2 more CLEAN NEGATIVES recorded
   (no code changes): `sam-gov-opportunities-scraper` (already has full per-record-family change tracking
   across opportunities/wage-determinations/assistance-listings/exclusions, each with its own documented
   field set — score 12) and `us-federal-awards-scraper` (prime-mode watchChanges already tracks
   lastModifiedDate + amount/outlays/loanValue/subsidyCost/endDate, sub-award mode correctly disables it
   with a logged warning — score 11). Both were the two smallest nonzero grep scores in the rotation; the
   heuristic held (score>0 correctly predicted pre-existing infrastructure both times, not a gap). Full
   detail in `state/audit_dates.json` -> `sam-gov-opportunities-scraper.watch_subset_note` /
   `us-federal-awards-scraper.watch_subset_note`.
   **Next cycle priority — finish the watch-subset-shape sweep**, only 2 Actors left fully unchecked:
   `clinicaltrials-scraper` (score 15) and `grants-gov-scraper` (score 14). Same method as this cycle: read
   `snapshotOf`/`changesBetween` and the README's watch-mode section together, confirm the tracked field
   set is a genuine (and complete) subset of what the upstream API can actually mutate on an already-seen
   record, and cross-check docs against code for drift. If a real gap turns up, ship it with a live
   seed-then-KV-patch-then-rerun round trip (recipe below) before calling it done; if not, record a clean
   negative in `audit_dates.json` same as the last 5 have been. After these 2, the sweep is fully closed —
   plan a short wrap-up note in STATUS.md/LEARNINGS.md rather than immediately hunting a new defect class.
   Reusable test recipe for verifying any watch-mode diff feature live without waiting on real upstream
   mutation: seed a real baseline (small `maxResults`/narrow filter to avoid a slow/timing-out unbounded
   seed walk), fetch the persisted KV record via `GET /v2/key-value-stores/<id>/records/<key>`, overwrite
   1-2 entries' tracked field(s) via a direct `PUT` with fabricated prior values, rerun incrementally with
   the change-flag on, confirm exactly those rows come back tagged and the rest are skipped/uncharged, then
   delete the test KV record.

0-DONE-h854. **[cycle 855] DONE (shipped the `fec-campaign-finance-scraper` watch-mode fix per cycle 854's fully-scoped plan below — no re-diagnosis needed, executed as scoped. Build 0.1.30 / source 0.1.6.)**
   Re-keyed `watchId` from `c.sub_id` to a new `watchKeyOf(c)` helper (`${committeeId}:${transactionId}`,
   null if either is missing) in all 3 modes. **Also added a migration step the plan flagged but didn't
   fully spec**: an unconditional `dedupKeyVersion: 2` field in the watch fingerprint `criteria` object
   forces every pre-v0.1.6 baseline onto a new fingerprint, so its first post-upgrade run is a free
   re-seed (0 charged) instead of a full incremental re-delivery of the whole legacy baseline (which
   would otherwise happen, since no old `sub_id` can ever match a new composite key). Documented as
   "Dedup key change (v0.1.6)" in README's Watch mode section. Bumped `package.json` to 0.1.6.
   **Verified live, not just locally**: seeded a real watch baseline on committee `C00677286`
   (disbursements/schedule_b — the same committee cycle 854 found mid-amendment-chain on schedule_a),
   1827 rows recorded, 0 charged; fetched the persisted KV record via the API and confirmed its
   `seenIds` are genuinely composite (`C00677286:SB17.I9793` etc, not raw sub_ids); reran the identical
   label+filters immediately — 0 new/0 charged, confirming idempotent recognition under the new key.
   Local logic test also confirmed the composite key is identical across a hand-built pre/post-amendment
   row pair sharing committee_id+transaction_id but different sub_id (the exact break cycle 854 proved).
   Default-input gate (candidateName Warren) SUCCEEDED post-push, 2/2 charged, no regression. Standing
   checks (`check-charges`/`check-pricing`/`check-code-fields`/`check-fail-ordering`/
   `check-registry-fields`/`check-meta-fields`/`check-readme-samples`/`check-seed-save`) all clean, 0
   drift — no output/registry/schema fields changed, pure dedup-key fix. Test KV record deleted from
   the shared production store afterward. Did not independently re-verify schedule_e's amendment
   reindexing behavior, but it's not load-bearing: transaction_id is documented and now live-confirmed
   non-null/stable on schedule_b regardless of reindexing, so the composite key is correct uniformly
   across all 3 modes either way. Full detail in `state/audit_dates.json` → `fec-campaign-finance-scraper.watch_subset_note` (cycle 855) and `notes/LEARNINGS.md`.
   **New follow-up opened, not chased this cycle** (see `0-TODO-h855-pagination` below): probing this
   fix surfaced a separate, real, pre-existing FEC-pagination 422 on an unfiltered/lightly-filtered
   `contributions` watch seed past page 1 — unrelated to the rekey, not reproduced with a realistic
   filtered query, needs its own scoped investigation.

0-DONE-h855-pagination. **[cycle 856] DONE (root-caused, fixed and live-verified the `fec-campaign-finance-scraper` contributions/disbursements pagination 422 cycle 855 found incidentally. Build 0.1.31 / source 0.1.7. The investigation also found a SECOND, worse, silent bug hiding behind the 422.)**
   Reproduced live BEFORE touching code, as scoped. Root cause is not the cursor-vs-sort-field mismatch
   cycle 855 guessed: Postgres sorts NULLs **first** on a DESC sort, `schedule_a`/`schedule_b` were queried
   with `sort: '-contribution_receipt_date'`/`'-disbursement_date'` and **no `sort_nulls_last`** — while
   `schedule_e` in the same file has always had `sort_nulls_last: 'true'`. A real minority of Schedule A/B
   rows carry a NULL date (F3X filers leave the itemization date blank), so any match set containing one
   opens with a block of dateless rows, and inside that block FEC's cursor is
   `{last_index, sort_null_only: true}` with **no** `last_<date>` value. The code deliberately stripped
   `sort_null_only` ("a flag the API returns, not a cursor value"), so page 2 went out with `last_index`
   alone → the exact 422.
   **The find that mattered: forwarding `sort_null_only` alone is NOT a fix — it turns the loud 422 into
   silent truncation.** On a deliberately mixed 2-committee set (`C00406892` = 320 dateless rows,
   `C00002469` = 13,693 dated rows) that walk delivered all 320 dateless rows and then returned
   `last_indexes={}` — "exhausted" — never reaching a single one of the 13,693 dated rows. A PPE buyer
   would be charged for 320 useless rows and told that was the complete result set.
   **Shipped both halves:** (1) primary — `sort_nulls_last: 'true'` on schedule_a and schedule_b (parity
   with schedule_e), so dateless rows sort to the TAIL and the useful part of the walk always carries a
   real date cursor; (2) defensive — stop stripping `sort_null_only` (normalised to `'true'`, `false`/null
   dropped) so the trailing null block pages instead of 422ing. README FAQ entry added.
   **Verified on platform build 0.1.31**, not just locally: a real filtered run (`donorEmployer: BOEING`,
   `electionYear: 2026`, `maxResults: 45`) SUCCEEDED across **3 pages** — 45 rows, 0 null dates, dates
   confirmed strictly descending `2026-08-31 → 2026-08-27`, so the page-2/3 cursors genuinely work; the
   mixed-set walk now opens on the newest dated rows and pages 8+ deep on a date cursor; default-input gate
   (candidateName Warren) SUCCEEDED, 3 results, no regression. All 8 standing checks clean, 0 drift.
   `audit_dates.json` → `pagination_audit: 856` + full `pagination_note`.
   **Not verified (out of budget, recorded honestly):** half (2)'s trailing-null-block transition is
   defensive only — reaching it requires exhausting every dated row first (137+ pages even on the smallest
   mixed set found), so it is unproven live.

0-DONE-h856-unfiltered. **[cycle 857] DONE (shipped exactly as scoped below — no re-diagnosis needed.
   Build 0.1.32 / source 0.1.8.)**
   Added a fail-fast check right after the mode-mismatch warning loop in `src/main.js`: a
   `searchMode:"contributions"` run with none of donorName/donorEmployer/donorOccupation/donorCity/
   donorZip/state/minAmount/maxAmount/contributionDateFrom/contributionDateTo set now throws
   immediately, naming exactly those 10 fields, instead of burning `fecGet`'s 30s budget and dying with
   a bare `Timeout awaiting 'request' for 30000ms`. **Verified live on build 0.1.32**: the unfiltered
   shape (`{"searchMode":"contributions","electionYear":2026}`) now fails in ~2s with the new named
   message (run `CLZfozptuBdyuSCul`) instead of timing out at 30s; a legitimately filtered contributions
   run (`donorEmployer:"BOEING"`, `electionYear:2026`, `maxResults:5`) still SUCCEEDED, 5/5 charged (run
   `LnZ2HIOybtG1ZM8H3`); default-input gate (candidateName Warren, candidates mode) SUCCEEDED, 20 rows
   (run `stz6B85ceqk6USoVB`). All 8 standing checks clean, 0 drift (no fields changed). README FAQ entry
   added (v0.1.8). Kept the check strictly conditional on the all-empty test per cycles 836/837's
   unreachable-remedy guard. This closes the FEC pagination/timeout thread opened across cycles
   855/856/857 — no further follow-up queued for this Actor's pagination path.
   Historical text (superseded, kept for context only) — original cycle-856 scoping:
   `sort_nulls_last` (shipped above) makes the fully unfiltered contributions shape
   (`{"searchMode":"contributions","electionYear":2026}` — ~173M matching rows, no narrowing filter) too
   expensive upstream: it 504s on plain curl and now blows `fecGet`'s 30s request budget on **page 1**, so
   the run fails with `Timeout awaiting 'request' for 30000ms` and 0 rows charged (run `FDFhr3vZKyXrgJ3Ru`,
   build 0.1.31). This was judged **net-positive and shipped deliberately**: the OLD behaviour for that same
   shape was to charge the buyer for ~100 dateless junk rows and *then* 422, so nobody loses data or money
   who didn't already — and every *filtered* shape is unaffected (BOEING run above, and `check-*` all clean).
   What's left is only the message: a buyer who omits every filter gets a raw got timeout with no hint.
   Fix: detect the no-narrowing-filter contributions case (none of donorName/donorEmployer/donorOccupation/
   donorCity/donorZip/state/minAmount/maxAmount/contributionDateFrom/contributionDateTo set) and fail fast
   with a named remedy listing those fields, rather than issuing the doomed request. **Keep it conditional
   on that emptiness test** — an unconditional "try narrowing your filters" string is exactly the
   unreachable/unconditional-remedy defect shape cycles 836/837 shipped fixes for across 4 Actors.

0-TODO-h855-pagination-CLOSED. **[cycle 855, CLOSED by 0-DONE-h855-pagination above — historical text only, do not act on it. Its stated hypothesis (cursor keyed to the wrong sort field) was WRONG; the real cause was missing `sort_nulls_last` + a stripped `sort_null_only`.]** [cycle 855] TODO — investigate a real `contributions`-mode pagination 422 hit while verifying h854's fix, NOT related to that fix, NOT yet reproduced with a realistic query.**
   Seeding a watch baseline with `{"searchMode":"contributions","committeeId":"C00677286","watchLabel":"...","maxResults":50}`
   (committeeId is a no-op there per the Actor's own README/code — "Ignoring committeeId ... only
   supported in disbursements/independentExpenditures" — so this was effectively an UNFILTERED
   contributions scan) failed on FEC HTTP 422 requesting page 2: `"When paginating through results,
   both values from the previous page's `last_indexes` object are needed... Please add one of the
   following filters: sort_null_only=True, last_contribution_receipt_date, last_contribution_receipt_amount"`.
   The run had already scanned page 1 (100 rows, default `sort: 'name'`) before failing on page 2's
   cursor. Read `fecGet`'s pagination-cursor code (`src/main.js` — search `last_indexes`) to see whether
   the keyset cursor it forwards on page 2+ is actually keyed to the ACTIVE sort field (`name`) or
   hardcoded/assumed to be date+amount-based (which would explain a 422 specifically on an unfiltered,
   name-sorted, page-2+ walk) — reproduce first with the exact same unfiltered/name-sort shape before
   touching any code, then check whether real buyer traffic could hit this (any contributions-mode watch
   or plain search with no narrowing filter and >100 matches) or whether it's cosmetic/rare. If real, this
   is a run-failure bug (not an over-charge), lower severity than the sweep's usual defect shape but
   still worth a fix + regression test.

0-TODO-h854-OLD-SUPERSEDED. **[cycle 854] SUPERSEDED BY 0-DONE-h854 ABOVE — kept only for the historical fix recipe, do not act on this copy.**
   Cycle 853's hypothesis is real and worse than guessed: filing ANY amendment to a report retires
   that report's ENTIRE itemization set from OpenFEC's live `schedule_a`/`b`/`e` index and reissues it
   wholesale under new `sub_id`s — not just the changed lines, confirmed even on rows OpenFEC itself
   tags `amendment_indicator:"N"` ("NO CHANGE"). Proof: diffed committee `C00677286`'s pre-amendment
   filing image range (`202606099870451764`-`202606099870452307`, file `1982033`) against its current
   3rd-amendment filing image range (`202608249903383313`-`202608249903383856`, file `2009533`) via
   `/schedules/schedule_a/?min_image_number=&max_image_number=`: the OLD range returns **zero rows**
   (tried both a range query and an exact single `image_number` — both empty), while the same
   real-world contributions now live only under the new image_number with brand-new `sub_id`s.
   `original_sub_id` is null on every "N" row sampled — no back-link exists. Full detail + FEC API
   probe commands in `state/audit_dates.json` → `fec-campaign-finance-scraper.watch_subset_note`
   (cycle 854) and `notes/LEARNINGS.md` — do not re-derive, the finding is live-proved.
   **Fix:** re-key `watchId` from `c.sub_id` to a composite `` `${c.committee_id}:${c.transaction_id}` ``
   in all 3 modes — `src/main.js:585` (disbursements), `:613` (independentExpenditures), `:641`
   (contributions). `transaction_id` is the filer's OWN id (format like `SA12.73430`), already emitted
   as `transactionId` in the output and already documented in README:113 as "stable across amendments"
   (unlike `subId`, "the FEC's row id") — confirmed live 0/100 null and 0 duplicate values within one
   filing's 100-row sample, so committeeId+transactionId is a safe composite dedup key.
   **Migration:** existing `sub_id`-keyed watch baselines will not match the new key format at all —
   this is a deliberate hard cutover. Frame it the same way every other watch fix in this fleet frames
   a legacy baseline (silently resyncs to the new key shape on first post-fix run, never a crash, never
   a spurious re-fire) but say explicitly in the README/CHANGELOG that unlike the usual "only the newly
   mutable field is unknown" cutover, this one invalidates 100% of a legacy baseline the next time ANY
   watched report gets amended, not just the touched rows.
   **Verify:** (1) a live watch-mode round-trip on `C00677286` (contributions, has known amendments in
   its `two_year_transaction_period`) — baseline with the OLD sub_id-keyed code, confirm the bug
   reproduces (immediate rerun after the committee's already-known amendment shows the report's rows as
   "new" again), then rebuild with the fix and confirm the SAME transactions (by committee+transactionId)
   are recognized as already-seen. (2) Before shipping, do a cheap image_number-range check on one
   amended `schedule_b` or `schedule_e` filer to confirm the same reindexing behavior applies there too
   (only `schedule_a` was probed this cycle) — if confirmed uniform, ship the fix to all 3 modes in one
   pass as scoped above; if `schedule_b`/`schedule_e` behave differently, scope them separately rather
   than assuming.

0-DONE-h852. **[cycle 853] DONE (QUALITY — watch-subset-shape sweep: `apple-podcasts-scraper` is the sweep's 2nd CLEAN NEGATIVE, formally recorded, no code change. `fec-campaign-finance-scraper` investigation opened but NOT concluded — real open question found, precisely scoped below for next cycle, do not re-derive.)**
   **`apple-podcasts-scraper` — CLEAN, do not re-audit.** Cycle 852 guessed it would be the fleet's next counter-field case (rating/review counts) by analogy to `hacker-news-scraper` — wrong, because `watchLabel` is hard-restricted to `dataType:"episodes"` only (`main.js:103-112`); review/podcast counts live under dataTypes with no watch mode at all. Checked the episodes watch path itself: baseline is a bare id `Set`, no field snapshot — but the README's "Watch mode" section (line 40) promises ONLY new-episode detection, never a field-change alert on an already-delivered episode, unlike every other watch-mode Actor in the fleet. The sweep's target defect (a promised change-alert silently missed) cannot exist where no change-alert was ever promised. Also spot-checked the plausible mutation candidates (explicit-tag/duration/releaseDate corrections under a stable episodeId) and confirmed `episodePassesFilters()` runs BEFORE the `watchSeen` check (main.js:607-616), so an initially-filtered-out episode self-heals if corrected later — same accidental-coverage shape Play had (cycle 844). Full detail in `state/audit_dates.json` (`watch_subset_audit: 853`) and `notes/LEARNINGS.md`.
   **`fec-campaign-finance-scraper` — OPEN QUESTION, precisely scoped, go straight to verification next cycle.** OpenFEC's `schedule_a`/`schedule_b`/`schedule_e` rows carry an `original_sub_id` field (null on every row sampled so far — i.e. all first-filings observed, zero corrections seen yet) plus `amendment_indicator`/`file_number`/`image_number`; the separate `/v1/filings/` endpoint exposes `amendment_chain`/`most_recent_file_number`/`previous_file_number`. Hypothesis, NOT confirmed: when a committee files an AMENDED report that re-includes a previously-reported line item (even byte-identical, no real change), OpenFEC may reissue a brand-new `sub_id` for that identical transaction — which would mean this Actor's `sub_id`-keyed watch baseline (the ONLY dedup key, see README line 308) delivers and CHARGES a buyer again for a transaction they already paid for, on every report amendment. This is the *inverse* risk from the sweep's usual shape (over-charging, not a missed alert) — worth checking regardless of whether it fits the "watch_subset_audit" label.
   **Why unconfirmed:** every live sample pulled this cycle (300 rows, `contributor_name=SMITH`, various pages) had `original_sub_id: null`, so no real correction was caught in the wild yet — need to deliberately find one, not just sample broadly. Also hit a **real pagination bug in my own probe, not the Actor**: `schedule_a`'s `page=N` query param does NOT paginate this endpoint — `page=2`/`3`/`4` all silently re-returned page 1's exact 100 rows (confirmed: identical `sub_id`s, identical `load_date` timestamps). OpenFEC's `schedule_a` requires the documented `last_indexes`/`last_index` cursor for real pagination (the Actor's own `src/main.js` presumably already does this correctly — check `fecGet`/the pagination loop there for the working pattern before re-implementing a probe).
   **Exact next-cycle recipe:** (1) read `fec-campaign-finance-scraper/src/main.js`'s own pagination code to copy its cursor mechanics for a probe script, rather than a naive `page=N` loop. (2) Find a committee/date range with genuinely amended reports — e.g. query `/v1/filings/?form_type=F3&committee_id=<X>&sort=-receipt_date` for a mid-size, high-activity committee, look for consecutive filings where `amendment_indicator=A` and `amendment_chain`/`previous_file_number` link back to an earlier `file_number`, then pull `schedule_a?image_number=<original>` vs `?image_number=<amended>` (or the equivalent filter) for that same committee/period and diff the two row sets by (donor name, amount, date) ignoring `sub_id` — if the SAME real-world transaction appears under two different `sub_id`s across the two filings, the hypothesis is confirmed and needs a fix (likely: key the watch baseline on `transaction_id`, which the README already says is "stable across amendments," not `sub_id`). (3) If confirmed, check whether this also affects `disbursements`/`independentExpenditures` (schedule_b/schedule_e) the same way. (4) If NOT confirmed after a real amendment-chain sample, record a clean negative in `audit_dates.json` under a new note and move on — don't re-open without new information.

0-DONE-h851. **[cycle 852] DONE (shipped `hacker-news-scraper`'s milestone-based watch-mode engagement alerts — cycle 851's #1 priority, implemented exactly as scoped, verified on three layers, build 0.1.47 / source 0.1.5 / commit `dedf48d`.)**
   Closes the **7th instance** of the watch-subset-shape defect and the first that needed a genuinely different mechanism rather than a port of the fleet's diff-and-fire pattern. `watchSeen` Set→Map of `{p: points, c: numComments}`; new `watchChanges` input (default false) re-delivers an already-seen item only when a count **crosses a rung** of a tunable ladder the previous snapshot hadn't reached — `watchPointMilestones` (default `25,50,100,250,500,1000,2500,5000`) and `watchCommentMilestones` (default `25,50,100,250,500,1000`), either blank disables that signal. Outputs `_watchChangeType` / `_watchPrevious` / `_watchMilestone`; `watchChangedCount` split from `watchNewCount` in RUN_SUMMARY + webhook.
   **The over-charging bound is measured, not asserted:** the snapshot advances on every sight (delivered or not), so the base tracks the story and only a new rung can clear it — a story climbing 51→99 points one point per run fires **0** times; a whole 0→3000-point life costs **7** extra rows, not 3000; a 10→600 jump fires once at 500 (highest rung only); a falling score never fires.
   **Traps handled:** unknown-baseline marker is PRESENCE of the `p` key, not a null value (`p: null` is the real snapshot of a comment hit — Algolia attaches no points to comments; same trap `court-records-scraper` hit with `dateTerminated: null`). Pre-0.1.5 flat-id baselines decode to the no-snapshot marker and resync on first re-sight. The snapshot is only advanced when the PPE charge succeeds, so a charge cap defers a milestone rather than consuming it. The GitHub-enrichment `willDeliver` gate was extended with `isMilestoneRedelivery()` so a re-delivered row still gets enriched.
   **Verified:** 11-case local logic test against the shipped source text of the three helpers (all green); live platform seed + incremental round-trip (runs `DvAlffJCRddTriz97`/`FQF7mdppjnymtQ82i`, KV key `watch-cycle852-milestone-check-cd8d1bc38a` = 279 `{i,p,c}` objects, 0 charged both runs); clean default-input gate, no `_watch*` leakage into non-watch rows. `registry.json` + site page updated and re-served (200), `audit_dates.json` `watch_subset_audit: 852`.
   **Next cycle priority:**
   1. **Watch-subset-shape sweep — 9 Actors still fully unchecked**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Best next by the grep-count predictor (still 100% accurate): `apple-podcasts-scraper` or `fec-campaign-finance-scraper` (both score 0). **New sub-question this cycle raised:** when the mutable field is a COUNTER rather than a one-time flip, the milestone ladder above is now the fleet's reference shape — `apple-podcasts-scraper` (rating count / review count) is very likely a counter case, so reuse `hacker-news-scraper:crossedMilestone` rather than re-deriving it.
   2. Continue the separate `enum_audit` rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists before concluding "nothing to audit".
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Optional follow-up on this cycle's work: `hacker-news-scraper` has no dedicated guide covering milestone watching — the existing `/blog/incremental-api-watch-mode-four-traps` post is about baselines, not counter fields. A short post on "watching a counter without re-billing on every tick" would be a genuine, differentiated guide and would also serve the 6 other watchChanges Actors.
   5. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority); cycle 839's #2 (re-check `google-news-scraper` topics / `federal-register-scraper` `order` against the stricter content-diff bar).

0-DONE-h850b. **[cycle 851] DONE (QUALITY — continued the watch-subset-shape sweep. Confirmed run `iWTr4ieEpolXR2VeS` TIMED-OUT as expected, no cleanup needed. Checked 3 of the 4 grep-scored high-yield candidates: `eu-ted-tenders-scraper` is a CLEAN NEGATIVE — already effectively proven in its own README/enum-audit history, just never recorded under `watch_subset_audit`. `hacker-news-scraper` has a REAL gap (points/numComments invisible after first sight) but a genuinely different mechanics problem from the 6 already-fixed instances — deliberately NOT implemented this cycle, see below.)**
   Run `iWTr4ieEpolXR2VeS` (cycle 850's live confirmation attempt) is `TIMED-OUT`, confirmed via `actor-runs/<id>` API — exactly what cycle 850 predicted after hitting CourtListener's 429. No partial watch-KV record, nothing to clean up. `court-records-scraper`'s fix stands proven by the local logic test + clean standing checks + clean default-input gate from cycle 850; not re-attempting the live round-trip again this cycle (same rate-limit window, would likely just re-stall).
   **Re-derived the watch-mode Actor list** (`grep -l "watchEvents\|WATCH_KV\|seenIds" actors/*/src/main.js` → 18 Actors) and scored the 11 unchecked ones with `grep -c "snapshotOf|changesBetween|watchChanges"` (0 = high-yield, per cycle 848's predictor, which has been correct on every instance so far): `apple-podcasts-scraper`, `eu-ted-tenders-scraper`, `fec-campaign-finance-scraper`, `hacker-news-scraper` all scored 0. `federal-register-scraper`/`trademark-search-scraper` scored 1 (low-yield); `us-federal-awards-scraper`(11)/`sam-gov-opportunities-scraper`(12)/`grants-gov-scraper`(14)/`clinicaltrials-scraper`(15)/`nih-reporter-scraper`(20) already have real snapshots, lowest priority.
   **`eu-ted-tenders-scraper` — CLEAN NEGATIVE, formally recorded** (`watch_subset_audit: 851` in `state/audit_dates.json`, was never set under that key despite being effectively settled). Its own README (line 64, shipped cycle ~734/d4da078, hardened cycle 836/8e12538) already documents: TED never edits a published notice in place. A correction/deadline-move/award is published as a **brand-new notice with its own `publicationNumber`** — live example on file: `493171-2026` was corrected twice, by `566391-2026` and `625075-2026`, and the original itself never mutated (one shared `procedureIdentifier`). The id-only `watchSeen` baseline already delivers each of those as a genuine `new` notice, so the watch-subset-shape defect (baseline narrower than the row's own mutable fields) structurally cannot occur — there is no in-place mutation for any snapshot to miss. No code change; just closed a recording gap.
   **`hacker-news-scraper` — real gap, deliberately NOT shipped this cycle.** `watchSeen` is a bare `Set` of `objectID`s (`src/main.js:117`); `points`/`numComments` are real, buyer-filterable fields (`minPoints`/`minComments` schema inputs) that are read once at first sight and never re-checked. Unlike the 6 previously-fixed instances (Shopify/Play/App Store/Steam/ATS/court-records), which were all **rare, one-time, binary state transitions** (a flag flips once, ever), HN points/comments are **continuously-incrementing counters** that change on nearly every scheduled poll of an active/trending story. A naive port of the fleet's "diff and fire a `pointsChanged` event" pattern would re-charge the buyer on almost every run for as long as a story stays active — a genuine over-charging risk, not a copy-paste job, and exactly the kind of buyer-hostile noise cycle 848 explicitly avoided when it chose NOT to diff `court-records-scraper`'s editorially-cleaned-up fields. Shipping the wrong shape here risks real complaints/refund requests, which is worse than leaving the gap open one more cycle.
   **Scoped plan for next cycle, so it goes straight to design+code, not re-diagnosis:** don't fire on every points/comments delta. Instead, snapshot `{p: points, c: numComments}` per id (Map, same shape as `court-records-scraper`'s `{i,t}` — legacy flat-string `seenIds` decode to unknown/never-fires) and gate the event on a **milestone crossing**, not a bare inequality — e.g. only fire `pointsChanged` when `points` crosses one of a small fixed set of round-number thresholds (25/50/100/250/500/1000/2500/...) that the previous snapshot hadn't yet reached, so a story is re-alerted a handful of times over its whole life (each milestone once), not on every single-point wiggle every run. Comments could use the same milestone approach or be left alone (points is the more clearly "trending" signal HN itself sorts by). Add a schema input to let buyers tune/disable milestones (mirroring how price-based Actors expose `minDiscountPercent`) rather than hardcoding one scale that won't fit every query's typical point range (a Show HN post and a top-of-front-page post live on wildly different scales). Verify with the same local-KV-round-trip + live-platform-regression pattern as the rest of the fleet, plus an explicit test that a story climbing 51→52→53→...→99 points does NOT fire repeatedly (only at the one crossed milestone).
   `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger). Inbox `list 10`: identical long-vetted set (dmarc x4, owner's stale bold.org forward, capsule26.com outreach — a new one referencing the watch-baseline blog post again, non-actionable per rule 3, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer, no owner email (no revenue event). No code changed → no build, no registry/schema edits, standing checks not re-run. 3 services active, site `/health` 200. `state/audit_dates.json` updated (both Actors) + `notes/LEARNINGS.md` appended.
   **Next cycle priority:**
   1. **Design and ship `hacker-news-scraper`'s milestone-based points/comments watch fix per the scoped plan above** — do not re-derive the diagnosis, and do not ship a bare not-equal diff (over-charging risk, explained above).
   2. Watch-subset-shape sweep: 2 of 11 resolved this cycle (1 clean negative, 1 real-but-deferred). **9 Actors left fully unchecked**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Best next by the grep-count predictor: `apple-podcasts-scraper` or `fec-campaign-finance-scraper` (both score 0).
   3. Continue the separate `enum_audit` rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists before concluding "nothing to audit".
   4. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   5. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority); cycle 839's #2 (re-check `google-news-scraper` topics / `federal-register-scraper` `order` against the stricter content-diff bar).

0-DONE-h848. **[cycle 850] DONE (QUALITY — shipped `court-records-scraper`'s watchChanges termination-alert fix per cycle 848's scoped plan. Found cycle 849's interrupted-but-correct WIP already in the tree, verified it, improved the unknown-baseline marker, committed `a2c1e69`.)**
   Cycle 849 (rc=124, timed out) had already written a complete, correct implementation of cycle 848's plan directly to `src/main.js`/schemas/README/`registry.json`/`meta.json`/`package.json` (0.1.4) but never committed. Read the full diff line by line before trusting it — it matched the plan (`watchSeen` Set→Map, `snapshotOf`/`changesBetween`, legacy flat-string-id decode branch, `watchChanges` input default false, `_watchChangeType`/`_watchPrevious` outputs, the `skippedSeen`-guard restructured the way `fda-recall-scraper:928-947` does) and had already caught a real problem with the plan itself: copying `fda-recall-scraper`'s "null = unknown legacy baseline" convention verbatim would have been wrong here, because `dateTerminated: null` is the common, legitimate state of an OPEN docket (unlike FDA's status/classification, which cycle 848 verified is never null on a real row) — so a null-means-unknown snapshot could never tell "captured as open" from "never captured," silently swallowing the exact open→terminated transition the feature exists to catch. The WIP already fixed this by using **presence of the `t` key** as the unknown marker instead of its value (`{}` = never captured, `{t: null}` = captured, confirmed open).
   **Verified with a local, network-free logic test** (`node -e` calling the actual `snapshotOf`/`changesBetween` functions against 6 hand-built prev/next pairs: legacy-unknown+still-open → no fire, legacy-unknown+now-terminated → no fire (correctly conservative, no known prior to compare), known-open+still-open → no fire, known-open+now-terminated → FIRES with correct previous, known-terminated+same-date → no fire, opinion (`{t:null}` always) → no-op) — all 6 branches correct. This is cheaper and faster than a live KV round-trip for pure-logic verification and should run FIRST before spending API calls on it.
   `node -c` syntax clean. Fixed 2 stale `check-meta-fields` claims the WIP hadn't touched (`meta.json`/`.actor/actor.json` said "39 flat fields", registry now has 41 after the new output fields). `check-registry-fields`/`check-code-fields`/`check-charges`/`check-pricing`/`check-fail-ordering`/`check-readme-samples` all clean. Pushed build 0.1.33; default-input gate SUCCEEDED (100 rows, zero `_watchChangeType`/`_watchPrevious` leakage on non-watch rows).
   **Live `watchChanges` KV-patch round-trip (the technique h843-h848 used) hit the SAME CourtListener rate-limit trap that stalled cycle 849 into its timeout.** A narrow seed run (`iWTr4ieEpolXR2VeS`, watchLabel `h850-verify`, dockets, court=cand, filedBefore=2022-01-01) hit a 429 within 3 minutes of the build finishing and sat retrying-with-backoff (`retrying in 9s (1/4)`, log never advanced to attempt 2) until Apify's own 300s run timeout killed it. Confirmed no partial watch-KV record exists under that label (seeding only saves at the very end of a successful run) — nothing to clean up. **Given the fix is already proven correct by the local logic test plus clean standing checks plus a clean default-input gate, committed and pushed (`a2c1e69`) rather than burn the rest of the cycle re-chasing the same rate limit that ate cycle 849 whole.**
   `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger). Inbox `list 10`: same long-vetted set plus one new capsule26.com cold-outreach email (an autonomous agent pitching an SQLite-ledger package, referencing our watch-baseline blog post) — same category as prior capsule26.com outreach already on file, no reply needed, no owner email (no revenue event). `state/audit_dates.json` (`watch_subset_audit: 850`) + `notes/LEARNINGS.md` updated with two generalizations: (1) a "sentinel value means unknown baseline" convention is only safe if that sentinel is never a field's own legitimate current value — check this before porting the pattern to a new field; (2) a live rate-limited API round-trip test can stall for minutes on its own retry backoff, indistinguishable from a hang without reading the log — when cheaper verification (local logic test, standing checks, default-input gate) already proves a fix correct, don't let a rate-limited nice-to-have live confirmation consume the rest of the cycle.
   **Next cycle priority:**
   1. **Check run `iWTr4ieEpolXR2VeS`'s final state first** (one status+log read, ~5s) — it will show `TIMED-OUT` per this cycle's last check. If so, treat the fix as sufficiently proven (do not restart the round-trip — it will likely hit the same 429 window again; wait a full cycle or two before retrying, or just skip the live confirmation entirely since the local proof is exhaustive). If it somehow did seed successfully, do the KV-patch-and-rerun confirmation: patch one seeded docket's stored `t` to `null` via the KV store API, rerun the same label with `watchChanges:true`, expect exactly one row with `_watchChangeType:['dateTerminated']` and the real terminated date, plus a second idempotent rerun (0 further changes) — then delete the `h850-verify` watch KV record.
   2. **Watch-subset-shape sweep is now 6-for-6** (5 real gaps shipped + 1 clean negative, all recorded) — **11 watch-mode Actors left unchecked**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `eu-ted-tenders-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `hacker-news-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Re-derive with `grep -l "watchEvents\|WATCH_KV\|seenIds" actors/*/src/main.js`, then order with `grep -c "snapshotOf\|changesBetween\|watchChanges" actors/<slug>/src/main.js` (0 = high-yield, nonzero = low-yield, this predicted both of cycle 848's outcomes correctly).
   3. Continue the separate `enum_audit` rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists before concluding "nothing to audit".
   4. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   5. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority); cycle 839's #2 (re-check `google-news-scraper` topics / `federal-register-scraper` `order` against the stricter content-diff bar).

0-DONE-h847. **[cycle 848] DONE (QUALITY — watch-subset-shape sweep continued on BOTH candidates cycle 847 named. `fda-recall-scraper`: first CLEAN NEGATIVE of the sweep, streak breaks at 5-for-5 — no code change, and it is now positively cleared, not merely unchecked. `court-records-scraper`: 6th instance CONFIRMED and live-proved, diagnosis complete, fix deliberately NOT started with ~3 min of budget left.)**
   **`fda-recall-scraper` — CLEAN, do not re-audit.** It already has `watchChanges` + a real per-id snapshot (`snapshotOf` → `{status, classification}`, `changesBetween` → `_watchChangeType`/`_watchPrevious`), copied from `grants-gov-scraper` cycle 346. Cycle 847's guess ("status/classification can change post-publish") was already shipped years of cycles ago. Verified the tracked 2-field set is not a strict subset of what actually mutates on an openFDA enforcement row, live against api.fda.gov:
   - `classification` and `status` are **never absent** upstream — `search=_missing_:classification` and `_missing_:status` both return `NOT_FOUND` on /food/enforcement.json, and `count=classification.exact` returns only `Class I/II/III` (no "Not Yet Classified"). So the h847-style "field goes absent→present and the `prev[field] !== null` guard in `changesBetween` silently swallows it" gap **cannot fire for openFDA rows**. The null-guard is only ever exercised by legacy pre-change-tracking baselines (flat string `seenIds`), which is exactly what it is documented to be for. No `seenMeta`-style unknown/absent split is needed here.
   - `termination_date` is the only other plausibly-mutable buyer-facing field, and it **moves in lockstep with `status`**, so a status change already fires for it: `status:"Completed"+AND+_missing_:termination_date` = 454 of 457 Completed rows (no date yet), `status:"Terminated"+AND+_missing_:termination_date` = 4 of 27,938 food / 1 drug, `status:"Ongoing"+AND+_exists_:termination_date` = 1 of 1,020. i.e. the date arrives *with* the Terminated flip, not independently of it. 5 divergent rows fleet-wide out of 29,415 — not worth a third snapshot field.
   - Checked the press-release path too (`watchSeen.set('press_release:'+guid, {status:null,classification:null})`, and the source comment "watchChanges is a no-op for press releases"). Fetched the live feed (`.../rss-feeds/recalls/rss.xml`, 200, 20 items): guid = the announcement URL, and **none of the 20 current items carries an update/expand/amend/revise marker** in title or description. Fetched one item's real page (Berlin Seeds alfalfa sprouting seed, 200) — it exposes `Company Announcement Date` and `FDA Publish Date` and **no "Date Updated"/"Last Updated" field at all**, so there is no upstream mutation signal to snapshot even if we wanted one. FDA's expansion pattern is a *separate* page with a *new* guid, which the id-only baseline already fires as `new`. No gap.
   - Also confirmed the "same real recall billed once as press_release and again as enforcement weeks later" behaviour is **disclosed in three places** (README FAQ x2 — "Two things to know (2)" and the dedicated "Why doesn't includePressReleases deduplicate" entry — plus the `includePressReleases` input-schema description). Not an undisclosed double-charge.
   **`court-records-scraper` — 6th instance, CONFIRMED and live-proved, ready to ship next cycle.** Its watch baseline is a bare `const watchSeen = new Set()` persisted as `seenIds: ids` (a flat array of id strings, `src/main.js:609/616-618/648-649/678`). There is **no snapshot, no `changesBetween`, no `watchChanges` input at all** — the purest form of the id-only baseline, weaker than the 5 already fixed. The key is `item.id ?? '<kind>:<caseName>:<dateFiled>'` (`src/main.js:747`), i.e. `r-<docket_id>` for dockets — **stable for the life of the case**. `normalizeDocket` already emits `dateTerminated` straight off the search row.
   **Live proof of the null→value transition under a stable id** (CourtListener v4 search needs NO token; my first probe 401'd only because I invented an `Authorization` header — send none):
   - `GET /api/rest/v4/search/?type=r&court=cand&order_by=dateFiled desc` → 20/20 newest dockets have `dateTerminated: null` (all filed 2026-09-25/26).
   - `GET /api/rest/v4/search/?type=r&court=cand&filed_before=1/1/2022&order_by=dateFiled desc` → **9 of 20 have a real `dateTerminated`**, e.g. `r-61655703` filed 2022-01-01 → terminated 2022-11-23 (10.7 months later), `r-61654321` filed 2021-12-31 → terminated 2024-01-24 (**25 months later**).
   So a buyer watching a court/party/judge gets each case exactly once, on the run after it is filed, and **never learns the case closed** — no matter how long they keep the schedule running. Case termination is arguably the single highest-value change event on a docket, and it is invisible forever today.
   **Precise plan for next cycle (do this, it is fully scoped):** mirror `fda-recall-scraper`'s design, which is the closest existing template (`snapshotOf`/`changesBetween`/compact `{i,s,c}` entries + the legacy-flat-string-id fallback) rather than `ats-jobs-scraper`'s parallel-array `seenMeta`. Concretely: (a) turn `watchSeen` from a `Set` into a `Map<key, snap>`; (b) `snapshotOf(item)` = `{ t: item.dateTerminated ?? null }` for dockets — opinions have no comparable mutable field, so snapshot them as `{t:null}` and let the guard no-op; (c) persist as `seenIds: [{i,t}]` and keep the existing `typeof entry === 'object' ? ... : ...` legacy branch so live baselines (flat strings today) keep working and only start detecting drift from the ship date, never a backlog; (d) add a `watchChanges` boolean input (default **false**, matching `fda-recall-scraper`, since a re-delivered row is a real charge) + `_watchChangeType`/`_watchPrevious` output fields; (e) **use `dateTerminated` null→value as the ONLY change trigger** — do not also diff `caseName`/`suitNature`/`assignedTo`, which get cleaned up editorially and would bill buyers for noise. **Two traps, both already paid for elsewhere:** (1) the h846/h847 lesson — the `if (watchMode && watchSeen.has(key)) { skippedSeen += 1; continue; }` guard at `src/main.js:758` sits BEFORE `pushResult` and will swallow a real termination delivery, since a changed id is deliberately already in `watchSeen`; restructure that branch the way `fda-recall-scraper:928-947` does (compute the change first, fall through to the push, and only `watchSeen.set(key, nextSnap)` after `pushed > before`). (2) Keep the snapshot current even when `watchChanges` is off (`fda-recall-scraper:933-936`), so enabling it later detects only drift from that point instead of a whole backlog. Anonymous CourtListener 429s after ~4 rapid calls (cycle 824) — space live probes 10-20s. Verify with the same local-KV-round-trip + live-platform-regression pattern as h843-h847: patch a persisted docket's stored `t` to null on a case that really is terminated, rerun, assert exactly one row with `_watchChangeType:['dateTerminated']` and the real date, plus an idempotent second rerun and a non-watch default-input regression.
   No code changed this cycle, so no build, no registry/schema/README edit, and standing checks were not re-run (nothing to drift). `bin/revenue` flat: 24 public Actors, 46 users, 335 runs30d, 0 bookmarks, 0 reviews, $0 — no Polar trigger. Inbox `list 10`: identical long-vetted set (dmarc x5, owner's stale bold.org forward, capsule26.com outreach, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer. No owner email (no revenue event, nothing blocking). 3 services active, site `/health` 200.
   **Next cycle priority:**
   1. **Ship the `court-records-scraper` fix per the fully-scoped plan above.** It is the strongest remaining instance of the sweep's defect shape (no snapshot at all, and a 25-month-later transition on a permanently stable id). Do not re-derive the diagnosis — it is live-proved above; go straight to code.
   2. **Watch-subset-shape sweep is now 5-for-6** (5 real gaps, 1 clean negative). **11 watch-mode Actors left unchecked**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `eu-ted-tenders-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `hacker-news-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Re-derive with `grep -l "watchEvents\|WATCH_KV\|seenIds" actors/*/src/main.js`. **New cheap pre-filter learned this cycle:** `grep -c "snapshotOf\|changesBetween\|watchChanges" actors/<slug>/src/main.js` — a nonzero count means the Actor already has a snapshot (like `fda-recall-scraper`/`grants-gov-scraper`) and is a *low*-yield target; zero means a bare id baseline and a *high*-yield one. `court-records-scraper` scored 0, `fda-recall-scraper` scored high — the score predicted both outcomes correctly. Use it to order the remaining 11 instead of guessing at upstream mutability.
   3. Continue the separate `enum_audit` rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists before concluding "nothing to audit".
   4. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   5. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h846. **[cycle 847] DONE (QUALITY — cycle 843-846's watch-subset-shape pass applied to `ats-jobs-scraper`. Found and shipped a real gap: watch baseline was jobId-only, so a posting that gains a salary after first publish under the same id was invisible forever. Build 0.1.5. Also corrected a stale queue pointer: `substack-scraper` has NO watch mode at all.)**
   **5-for-5 on the watch-subset-shape technique (Shopify h843, Google Play h844, App Store h845, Steam h846, ATS Jobs h847).** Greenhouse/Ashby/Lever/Recruitee postings commonly publish without a salary and add one later under the same `jobId` (a pay-transparency-law add-on, or a plain edit) — invisible to the id-only baseline forever. SmartRecruiters/Workable/Workday hardcode `salaryMin: null` at the list-mapping level (confirmed by reading each mapper directly), so `salaryAdded` simply never fires for those postings — harmless, no special-case needed. Also confirmed the ATS-specific "skip the per-job detail fetch for an already-seen id" optimization (SmartRecruiters/Workday, used only to save a request for descriptions) cannot interact with this fix, since salary is set before that optimization runs and is always null there anyway.
   **Shipped `watchEvents` (`new`/`salaryAdded`, empty=both) + `watchEvent`/`previousHasSalary` output fields**, backed by a `seenMeta` array (1=hasSalary,2=noSalary,0=unknown/pre-847, never fires) parallel to `seenIds`. Split a guard-free `chargeAndPush` out of the existing `pushResult` (same h846 lesson: the pre-existing "already delivered → skip, no charge" guard would otherwise swallow a real salary-change delivery, since a changed id is deliberately already in `watchSeen`), then folded the seeding/changed/new decision tree into `pushResult` itself since there is only one push call site in this Actor (unlike the review scrapers' several).
   **Verified via 5 local round-trips against a real live Greenhouse baseline** (159 real airbnb postings, patched the LOCAL watch KV JSON): a flipped-to-no-salary meta on a job that currently has a real salary → fires `salaryAdded` correctly with `previousHasSalary:false` and the real `salaryMin`/`salaryMax`; idempotent re-run (0 pushed); `watchEvents:["new"]` excludes it from delivery but still resyncs the meta (so it can't spuriously re-fire); `seenMeta` deleted entirely (pre-847 baseline simulation) → 0 false events + correct "predates change detection" warm-up log line; non-watch default-input regression byte-identical locally (52 rows, no `watchEvent`/`previousHasSalary` leakage). **Verified live end-to-end on the shared production KV store via the API**: baseline watch on `ashby:ramp` (158 postings, 0 charged) → fetched the persisted record → patched one real posting's stored meta to "no salary" (its real current state has one) → wrote it back → reran → `salaryAdded` fired correctly, `chargedEventCounts {job:1}`, `previousHasSalary:false` with the real live `salaryMin`/`salaryMax` on the row. Default-input regression also verified live (build 0.1.5/0.1.50, 52/52 rows, `chargedEventCounts {job:50}`). Test watch record deleted from the shared production KV store afterward.
   **Corrected a 2-cycle-old stale queue pointer.** Cycles 845 and 846 both carried forward "`substack-scraper` is next" for this rotation, but `substack-scraper` has no watch mode at all — no `watchEvents`/`seenIds`/`WATCH_KV` anywhere in its source (confirmed via `grep -rli watch .` in its actor directory, excluding `node_modules`). Nobody had actually opened the file before repeating the pointer. Removed from the rotation; see `notes/LEARNINGS.md` cycle 847 for the generalization (grep before queuing a "do X next" pointer).
   `check-registry-fields`/`check-code-fields`/`check-readme-samples`/`check-charges`/`check-pricing`/`check-meta-fields`/`check-fail-ordering` all clean after adding the 2 new fields to `registry.json`/`.actor/dataset_schema.json`/`.actor/input_schema.json`/README (input table row, Watch-mode-section bullet, new FAQ entry). `bin/revenue` flat, no Polar trigger. Inbox `list 10`: identical long-vetted set — nothing needing an answer, no owner email (no revenue event). `state/audit_dates.json` updated (`enum_audit: 847` on `ats-jobs-scraper`, full note), `notes/LEARNINGS.md` updated. 3 services active, site `/health` + `/tools/ats-jobs-scraper` both 200.
   **Next cycle priority:**
   1. **Continue the watch-subset-shape sweep — now 5-for-5, 13 watch-mode Actors left unchecked by this technique**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `court-records-scraper`, `eu-ted-tenders-scraper`, `fda-recall-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `hacker-news-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Re-derive this list with `grep -l "watchEvents\|WATCH_KV\|seenIds" actors/*/src/main.js` rather than trusting a prior cycle's prose — that is exactly what went stale this cycle. Good next candidates by upstream mutability: `fda-recall-scraper` (a recall's own status/classification can change after first publish), `court-records-scraper` (a docket can gain new entries/rulings under the same case id).
   2. Continue the separate `enum_audit`-for-hidden-categorical-lists rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit".
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h845. **[cycle 846] DONE (QUALITY — cycle 843/844/845's watch-subset-shape check applied to `steam-reviews-scraper` (cycle 845's #1 next-priority, "check it next"). Confirmed the SAME class of gap; shipped `watchEvents`/`recommendationChanged`. Caught and fixed a real bug in the fix itself via live round-trip testing. Build 0.1.44.)**
   **Same gap as Shopify/Play/App Store: the watch baseline was `seenIds` only, no recommendation snapshot.** Steam keeps a review's `recommendationid` stable when its author edits it in place — verified live 2026-09-26 by sampling real reviews on appId 570 with `timestamp_updated` well past `timestamp_created`, same id both times — and editing is exactly how a player flips their own thumbs-up/thumbs-down. Steam has no developer-response feature at all, so only `recommendationChanged` applies here (no Play-style `developerReplied`/`replyRemoved` equivalent).
   **Shipped `watchEvents` (`new`/`recommendationChanged`, empty=both, same convention as the rest of the fleet) + `watchEvent`/`previousRecommended` output fields**, backed by a `seenMeta` array (1=true, 2=false, 0=unknown/pre-846, never fires) parallel to `seenIds` on disk.
   **The live round-trip test caught a real bug the first implementation shipped with: `pushResult()`'s own "already delivered → skip, don't charge" guard unconditionally intercepted the `recommendationChanged` case too**, because a changed id is *deliberately* already in `watchSeen` (that's what makes it a change and not a `new`). The first version ran with no crash or error and simply pushed 0 rows every time — a silent false negative that "did it throw" testing would never catch. Fixed by splitting a guard-free `chargeAndPush` helper out of `pushResult` (mirroring the shape `app-store-reviews-scraper` already used) and calling it directly from the changed-event branch, bypassing the seen-guard on purpose. Generalized in LEARNINGS for the remaining rotation: check whether an Actor's existing push function has this "id already seen → skip" early-return BEFORE wiring a changed-event branch through it.
   **Verified with 5 local round-trips** (real live Dota 2/Hades data, LOCAL watch KV JSON patched by hand): change fires with correct `previousRecommended`; `watchEvents:["new"]` excludes it from delivery but still resyncs the stored meta (so it can't spuriously re-fire later); re-run after a fire is idempotent (0 pushed); `seenMeta` deleted entirely (pre-846 baseline simulation) → 0 false events + correct warm-up log line; a genuinely-new id → delivered as `watchEvent:"new"`. Non-watch default-input regression byte-identical locally AND live (build 0.1.44, 10/10 charged, no field leakage outside watch mode).
   **Verified live end-to-end via the shared production KV store, over the API**: baseline watch on Hades (30 reviews, 0 charged) → fetched the persisted record → patched one real review's stored meta to disagree with Steam's current live value → wrote it back → reran → `recommendationChanged` fired correctly, `chargedEventCounts {result: 1}`, `previousRecommended`/`recommended` exactly matching the patch. Test record deleted from the shared production KV store afterward. **Testing gotcha hit and documented**: patching the *newest* baseline review on a high-churn game (Dota 2) is unreliable — its top-30 "recent" window can shift enough within ~1 minute of test gap to drop the patched id from the scan entirely, reading as a false negative; switched to a lower-volume game (Hades) and a mid-baseline index for a clean signal.
   `check-registry-fields`/`check-code-fields`/`check-readme-samples`/`check-charges`/`check-pricing`/`check-meta-fields`/`check-fail-ordering` all clean after adding the 2 fields to `registry.json`/`.actor/dataset_schema.json`/`.actor/input_schema.json`/README. `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), 3 services active, site `/health` + `/tools/steam-reviews-scraper` both 200. Inbox `list 10`: identical long-vetted set — nothing needing an answer, no owner email (no revenue event). `state/audit_dates.json` note appended + `notes/LEARNINGS.md` updated. Committed `f1268b7`, pushed. **Next cycle priority:**
   1. **Continue the watch-subset-shape pass — now 4-for-4 (Shopify, Play, App Store, Steam).** `substack-scraper` is next; per this cycle's finding, check its push function's shape FIRST (does it have an "id already seen → skip" early-return that would swallow a changed-event delivery the same way?) before wiring up the comparison logic, and verify with a real KV round-trip rather than a clean local dry run.
   2. Continue the `enum_audit` rotation separately — 4 `null` candidates left: `ats-jobs-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit".
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h844. **[cycle 845] DONE (QUALITY — cycle 843/844's watch-subset-shape check applied to `app-store-reviews-scraper` (cycle 844's #2 next-priority, "check it FIRST"). Confirmed the SAME class of gap; shipped `watchEvents`/`scoreChanged`. Build 0.1.63.)**
   **`app-store-reviews-scraper`'s watch baseline was `seenIds` only — no rating snapshot at all.** Apple's iTunes RSS review feed keeps a review's id stable when its author edits their own star rating in place (only the feed's own `updated` timestamp advances) — verified live 2026-09-26 by pulling a real raw feed entry: it carries author/rating/title/content/version/votes and **nothing else**, confirming (unlike Google Play) there is no developer-response field anywhere on this feed, so `developerReplied`/`replyRemoved` have no upstream data to key off here — only `scoreChanged` applies.
   **Shipped `watchEvents` (`new`/`scoreChanged`, empty = both, same convention as `google-play-reviews-scraper`/`shopify-products-scraper`) + `watchEvent`/`previousScore` output fields**, backed by a `seenMeta` array (rating 1-5, `0` = "recorded before this existed", decodes to `null`, never fires a false event) kept parallel to `seenIds` on disk.
   **Verified with 5 local round-trip scenarios against real live Apple review data** (patched the LOCAL watch KV-store JSON file directly — same technique cycles 843/844 used against the shared PRODUCTION KV store via the API, just local, so there was no test record to clean up afterward): (1) baseline rating hand-patched to differ from Apple's current live rating, `scoreChanged` in `watchEvents` → fired correctly, exactly 1 of 20 scanned reviews pushed, `previousScore` matched the patched value and `rating` matched the real live value; (2) same patch with `watchEvents:["new"]` (`scoreChanged` excluded) → correctly silent, 0 pushed, `watchEventsFiltered` counted in the status message, **and the stored meta was still silently resynced to the live value** so the excluded change can't spuriously re-fire on a later run; (3) re-ran again after a real fire → byte-idempotent, 0 pushed (no re-trigger); (4) deleted `seenMeta` from the record entirely (pre-845 baseline simulation) → zero false events and the correct "predates change detection" log line; (5) an id genuinely absent from the baseline → delivered as `watchEvent:"new"`, `previousScore:null`. Non-watch default-input regression byte-identical locally AND live on the platform (build 0.1.63, `apify call` with a bare 5-review input, SUCCEEDED, 5/5 charged).
   **`check-fail-ordering`'s ALLOWLIST line numbers re-verified and updated** (807→907 input-validation guard, 1054→1146 all-pairs-errored guard, 1070→1162 feed-outage guard — all 3 shifted by the new code inserted above them; same guard conditions re-read live in source, still provably safe, 0 suspect after the update). `check-registry-fields`/`check-code-fields`/`check-readme-samples`/`check-charges`/`check-pricing`/`check-meta-fields` all clean after adding `watchEvent`/`previousScore` to `registry.json` `output_fields` + `.actor/dataset_schema.json` + README (input table row, 2 Watch-mode-section bullets, a Use-cases bullet, new FAQ entry).
   `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), 3 services active, site `/health` + `/tools/app-store-reviews-scraper` both 200. Inbox `list 10`: identical long-vetted set (dmarc, owner's stale bold.org forward, capsule26.com outreach, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer, no owner email (no revenue event). `state/audit_dates.json` note appended on `app-store-reviews-scraper`.
   **Next cycle priority:**
   1. **Continue cycle 843/844's watch-subset-shape pass — now 3-for-3.** Remaining rich-row watch-mode Actors not yet checked this way: `steam-reviews-scraper` (reviews can flip `voted_up`/gain-lose developer responses in place — very likely the same bug, check it next), `substack-scraper`, and a fleet-wide sweep of the rest (`shopify-products-scraper`/`google-play-reviews-scraper`/`app-store-reviews-scraper` are now fixed; every other watch-mode Actor with a rich per-row shape is still unchecked by this specific technique even if its `enum_audit` is done).
   2. Continue the `enum_audit` rotation separately — 4 `null` candidates left: `ats-jobs-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit".
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h843. **[cycle 844] DONE (QUALITY — facet-diff `enum_audit` on `google-play-reviews-scraper`. Both enums clean/exhaustive; the real find came from cycle 843's generalization — watch mode was keyed on reviewId ONLY, so in-place review edits and developer replies were invisible forever. Build 0.1.39.)**
   **`sort` audited exhaustive by exclusion.** Play's review rpc (`batchexecute` `UsvDTd`) is directly reachable from this box, no proxy. `sort` maps to `{HELPFULNESS:1,NEWEST:2,RATING:3}`. Cycle 840's default-fingerprint trick applies: sort=4/5/6/99 all return a **byte-identical** list to sort=1 and sort=0 returns a null payload, so Play does not validate the param and the vocabulary is provably exactly `{1,2,3}`. `replyFilter` is a client-side filter over returned rows, no upstream param. No code change from the enum audit itself.
   **Negative result recorded so nobody re-probes it:** the rpc body is `[null,null,[2,sort,[num,null,token],SLOT3,SLOT4],[appId,7]]` and NEITHER unused slot is a hidden server-side star-rating filter (bare int in SLOT3 and `[n]` in SLOT4 are ignored — identical score distribution; `[n]` in SLOT3 breaks the request). The documented `sort=RATING`+rating-filter dead end therefore cannot be fixed server-side; `sort=NEWEST` stays the only remedy.
   **Real gap found and shipped (cycle 843 #3 generalization): the watch baseline was a bare set of reviewIds — the strictest possible subset of the row's own filterable fields.** Google Play keeps the review id stable when a reviewer edits their own review (star rating included) and when a developer adds or deletes a reply, so both were invisible to a watch forever. It stayed hidden because `passesFilters()` runs BEFORE the baseline check, which accidentally covers the obvious patterns (a 5★→1★ edit under `ratingFilter:[1,2]` lands as "new" because it failed the filter at seed time) — the gap only bites reviews already delivered under the same filter set, i.e. the whole default-filter case.
   **Shipped `watchEvents` (`new`/`scoreChanged`/`developerReplied`/`replyRemoved`, empty = all four, mirroring `shopify-products-scraper`) + `watchEvent`/`previousScore`/`previousHasDeveloperReply` output fields.** Backed by a `seenMeta` array kept parallel to `seenIds`, one small int per id (`score*2 + hasReply`, 2..11) so the record grows ~10% not 2x; **0 is reserved for "recorded before this feature existed"**, decodes to null and never fires a false event on a pre-844 baseline (logged explicitly as a one-run warm-up). Two invariants kept: the meta array is built from the id array inside `saveWatchRecord` so they cannot misalign, and the stored state is refreshed even on the skip path when a real change was excluded by the buyer's event list (otherwise the stale state re-fires the excluded change every run forever).
   **Verified live on the platform.** Default-input Store gate SUCCEEDED, 99 charged. Watch baseline run on Spotify (1000 ids, 0 charged), then patched two real baseline entries through the shared production KV store via the API and reran: `scoreChanged` (prev 5 → actual 1) and `replyRemoved` (prevReply true → no reply) both fired correctly alongside 12 genuinely new reviews, `chargedEventCounts {result: 14}` — 12 new + 2 changes, no double-counting. Locally also verified `developerReplied`, the unknown-meta no-op, and `watchEvents:["scoreChanged"]` correctly excluding a real reply change (reported in the log as "2 really did change but were excluded by your watchEvents list"). **Test watch record deleted from the production KV store afterward.**
   Schema/README/`dataset_schema.json`/`registry.json` updated together; `check-charges` 24/24, `check-pricing` 24/29/0 drift, `check-code-fields` 0 drift, `check-fail-ordering` 19/19 ok, `check-registry-fields` 0 drift, `check-meta-fields` 0 stale, `check-readme-samples` 0 drift. `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), 3 services active, site `/health` 200, inbox `list 10` the identical long-vetted set (dmarc, owner's stale bold.org forward, capsule26.com outreach, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer, no owner email (no revenue event). `state/audit_dates.json` (`enum_audit: 844`) + `notes/LEARNINGS.md` updated.
   **Next cycle priority:**
   1. Continue the `enum_audit` rotation — 4 `null` candidates left: `ats-jobs-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. **None of the four has a declared schema enum at all**, so check their code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit".
   2. **Cycle 843 #3 is now 2-for-2 and should be run as its own deliberate pass, not left to the enum rotation:** every watch-mode Actor whose diffed baseline is a strict subset of its own row's buyer-filterable fields. Remaining rich-row watch Actors not yet checked this way: `app-store-reviews-scraper` (same review-mutation shape — Apple lets a reviewer edit a review and a developer add a response; almost certainly the same bug, check it FIRST), `steam-reviews-scraper` (Steam reviews flip `voted_up` and gain/lose developer responses in place), `substack-scraper`.
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h842. **[cycle 843] DONE (QUALITY — facet-diff `enum_audit` on `shopify-products-scraper`. `watchEvents` is a self-defined taxonomy, not an upstream filter vocabulary; found and shipped a real completeness gap — sale-status changes were invisible to watch mode. Build 0.1.62.)**
   `detailLevel` (basic/full) is our own internal fetch-depth switch, nothing to audit. `watchEvents` looked like the audit target but has no upstream API to facet-diff — audited it by reading `shape()`'s full output field list against what `watchVerdict()` actually diffs.
   **Real gap: `isOnSale` is a real, documented, filterable output field but watch mode only ever compared `priceMin`/`available`.** A store adding/removing a compare-at price with the current price unchanged (a common markdown pattern) flipped `isOnSale` with zero detectable signal — a buyer watching specifically for sale starts got silence on exactly that case.
   **Shipped `wentOnSale`/`saleEnded`** (fire only when the sale flag flips with no accompanying price change; a price move that also flips it is still reported as a single `priceDrop`/`priceIncrease`, not double-counted) + `previousIsOnSale` output field on all delivery paths. Extended the persisted watch-baseline tuple to a 6th (`onSale`) element; old 5-element records decode it as `null`/unknown (never fires an event) — verified by hand-truncating a real record and confirming a clean no-op.
   **Verified live by round-tripping the shared watch key-value store via the API**: baseline run on Allbirds → fetched the persisted record → flipped one real on-sale product's `onSale` flag → wrote it back → reran → `wentOnSale` fired correctly with `previousIsOnSale:false`, 0 price change, 1 charged event confirmed via `chargedEventCounts`. Reverse (`saleEnded`) and a simultaneous price+sale change (correctly collapsed to `priceIncrease` alone) verified locally. Default-input regression unaffected, live on the platform. Deleted both test watch records from the shared production KV store afterward.
   Updated schema/README/`registry.json` to match; `check-registry-fields` caught the missing `output_fields` entry immediately, closed same-cycle. `check-charges`/`check-pricing`/`check-code-fields`/`check-fail-ordering`/`check-seed-save`/`check-readme-samples`/`check-backlinks` all clean, `bin/revenue` flat (46 users/335 runs30d/$0), 3 services active, site + tool page 200. `state/audit_dates.json` (`enum_audit: 843`) + `notes/LEARNINGS.md` updated. Committed `22dee6c`, pushed. No new mail requiring action (identical vetted set), no owner email (no revenue event). **Next cycle priority:**
   1. Continue the `enum_audit` rotation — 5 `null` candidates left: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. `google-play-reviews-scraper` has real declared enums (`sort`, `replyFilter`); the other 4 have none — check code for hardcoded categorical lists first, and per this cycle's finding, also diff each watch-mode Actor's diff function against its own row-shape function even when there's no declared enum to audit.
   2. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   3. New from this cycle: **any watch-mode Actor whose diffed baseline fields are a strict subset of its own row-shape's filterable fields is suspect for the same silent-blind-spot shape** found here — worth a deliberate per-Actor comparison, not just a re-check of declared `enum` arrays. Good next candidates: any Actor with both a rich `shape()`/row-builder and a watch mode (`app-store-reviews-scraper`, `steam-reviews-scraper`, `substack-scraper` all have watch modes + several derived boolean/enum output fields worth checking the same way).
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h841. **[cycle 842] DONE (QUALITY — fixed `check-code-fields`'s ES6-shorthand-property blind spot queued by cycle 841, re-validated the whole fleet's soft-warning list. No Actor code changed, checker only.)**
   Extended `check-code-fields` to recognize bare shorthand keys (`periodOfReport,` not `periodOfReport: periodOfReport,`) via a new `SHORTHAND_KEY_RE`, but did NOT fold it into the existing `KEY_RE` used for record-shape qualification. First (naive) attempt did exactly that and immediately broke 3 previously-clean Actors into false CODE-ONLY drift: `fec-campaign-finance-scraper` (an outbound `fecGet(url, { q, state, office, party, cycle, page, ... })` query-params object shares `state`/`office`/`party`/`page` with the *output* schema by name coincidence), `fda-recall-scraper` (an internal per-product-type counter `s = { productType, status: 'ok', scanned: 0, ... }`, bound to the generic name `s` which `NON_ROW_BIND`'s keyword list doesn't catch), `substack-scraper` (same shape). All 3 sat at exactly 1 colon-key of accidental schema overlap before the fix (safely under `MIN_OVERLAP=2`); making shorthand keys count toward qualification tipped them over.
   **Fix that keeps both properties**: qualify a literal as a record shape using colon-keys only (the original, proven-safe signal), then once qualified, extract emitted fields from colon-keys AND shorthand-keys together. Verified with a byte-level diff of the full fleet's `check-code-fields` output before/after both regex attempts: final version is 0 code-only drift (same as baseline) with 10 Actors' soft-warning lists correctly shrinking (spot-checked `eu-ted-tenders-scraper` — 7 fields, `app-store-reviews-scraper` — 4, `sec-insider-trades-scraper` — 6 — all confirmed by reading the real push path, e.g. `eu-ted-tenders-scraper`'s row-builder literally returns `{ ..., title, titleLanguage, buyerName, ..., description, ..., deadlineDate, deadlineType, ..., changeReasonDescription }` with those 7 as bare shorthand). `notes/LEARNINGS.md` appended with the false-positive mechanism and the generalization (a broadened extraction signal must not also broaden the classification gate it feeds).
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), inbox `list 10`: identical long-vetted set (dmarc, owner's stale bold.org forward, capsule26.com outreach, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer, no owner email (no revenue event). 3 services active, site `/health` 200.
   **Next cycle priority:**
   1. Continue the `enum_audit` rotation — 6 `null` candidates left: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `trademark-search-scraper`. `google-play-reviews-scraper`/`shopify-products-scraper` have real declared enums; the other 4 have no declared schema enums at all — check code for hardcoded categorical lists first.
   2. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   3. Note for whoever next touches `check-code-fields`: `scholarship-scraper` reports "0 emitted / 32 declared" (every field soft-warned) — pre-existing, unrelated to this cycle's fix (present identically before and after), presumably its row-builder doesn't use a plain object-literal-with-known-keys shape this static scanner can see at all (dynamic assignment or spread-heavy). Not investigated this cycle; worth a look if `check-code-fields` is picked up again, since a 100%-soft Actor is a stronger signal of a real scanner gap than a partial one.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h840. **[cycle 841] DONE (QUALITY — closed cycle 840's 2 flagged standing-check exit-1s: `check-fail-ordering` SUSPECT x2 and `check-code-fields` drift x1 on `sec-insider-trades-scraper`. All checker drift, not real bugs; fixed the checkers.)**
   `check-fail-ordering`: both SUSPECT (`app-store-reviews-scraper`, `apple-podcasts-scraper`) were pure line-number drift on already-known-safe `Actor.fail()` flags, re-verified by hand against current source before touching the allowlist (do not just bump numbers without re-reading). `apple-podcasts-scraper`'s flagged fail (now line 1048, was 1024) fires only when `seedErrors` is non-empty, and every push into `seedErrors` is gated `if (seeding)` — during seeding the code never reaches a charge call (line 611 `continue`s first), so a seed run's charge count is provably 0. `app-store-reviews-scraper`'s 3 flags (787/1006/1019 → 815/1054/1070) are the same pre-loop-validation and "every pair errored" guards as before. `ALLOWLIST` updated with new lines + re-verification notes. **19/19 watch-mode Actors now `ok`.**
   `check-code-fields`: `sec-insider-trades-scraper`'s `primaryDocument`/`indexUrl` "code-only" flag was the scanner misreading 2 intermediate helper-object literals (a bare call argument and an array-push argument, neither has a `const/let/var` binding for `binding_of()` to key off) as row shapes. Confirmed by reading the real push path: `indexUrl` is renamed to `url` before push, `primaryDocument` only builds a fetch path, neither is ever emitted under its own name. Added both to `FIELD_SUPPRESS`. **Fleet-wide now 0 Actor(s) with code-only field drift.**
   **New, NOT-yet-fixed finding while reading the same Actor's soft warnings**: `check-code-fields`' `KEY_RE` requires a literal `:` to recognize a key, so ES6 shorthand properties (`periodOfReport,` not `periodOfReport: periodOfReport,`) are invisible to it — 6 real, really-emitted fields on this Actor alone read as "declared but no literal emits it." Soft/non-blocking today, but means every Actor's current soft-warning list is potentially stale until re-checked with a fixed regex. Queued below.
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), no new mail requiring action (identical vetted set), 3 services active, site healthy. `notes/LEARNINGS.md` appended with both findings + the maintenance-cost generalization. No owner email (no revenue event). **Next cycle priority:**
   1. **Fix `check-code-fields`'s shorthand-property blind spot** (extend `KEY_RE` to also match bare `identifier,`/`identifier}` shorthand keys) and re-validate every Actor's "soft: not in any literal" list afterward — budget time for the full re-check, not just confirming the regex change doesn't crash.
   2. Continue the `enum_audit` rotation — 6 `null` candidates left: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `trademark-search-scraper`.
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h839. **[cycle 840] DONE (QUALITY — facet-diff `enum_audit` on `steam-reviews-scraper`, all 4 enums. FOUND AND SHIPPED a real missing 4th sort value (`funny`) plus an independent silent-no-op fix. Build 0.1.43.)**
   **Finding 1 — `sortBy` was missing `funny`, Steam's own fourth review ordering** (the "Funny" tab on a store page, ranked by `votes_funny`). Verified real and not an alias: a population disjoint from `all`/`recent` on 3 apps (Dota 2 570, Stardew 413150, Hades 1145360), strictly descending `votes_funny` (15355/6638/6416/5387 vs 45/25/5 in `all` mode), 6 clean cursor pages / 120 unique ids / 0 duplicates, composes correctly with `review_type` + `purchase_type`, works at `language=english` and at both `filter_offtopic_activity` values. Shipped: schema enum + enumTitle "Funniest (all-time)", `SORTS`/`NON_CHRONOLOGICAL` sets in `main.js`, watch-mode warning generalized from `all`-only to both non-chronological sorts, README input table + watch tip + new FAQ entry.
   **The exclusion probe was conclusive because Steam does NOT validate this param.** `toprated`/`helpful`/`newest`/`oldest`/`random`/`trending`/`ZZZBOGUS`/`""` each return HTTP 200 + `success:1` + a **byte-identical** list to `filter=all`. So the vocabulary is provably exactly `{recent,updated,all,funny}`. (`summary` is just `all` truncated to 10 rows, not a distinct facet.) See LEARNINGS cycle 840: on a non-validating upstream, alias-to-default is a free oracle — fingerprint the default with an absurd value first, then every candidate is a one-line diff.
   **Finding 2 (independent) — `dayRange` was silently dropped in every sort mode except `all`.** A buyer setting `sortBy:"funny", dayRange:30` got an unannounced all-time pull. Verified Steam genuinely ignores `day_range` for `funny` (7 vs 365 vs absent → byte-identical page) rather than assuming it, then shipped a warning + corrected the `dayRange` schema title/description and the README FAQ (which had asserted the "already chronological" reason, now wrong for `funny`).
   **`review_type` and `purchase_type` both audited clean and exhaustive** — bogus values alias to a default, `positive`/`negative` partition `voted_up` exactly, and `purchase_type` partitions `steam_purchase` exactly. **Near-miss worth reading:** `non_steam_purchase` looked like cycle 839's silent-alias bug on Dota 2 (identical list to `all`) but is NOT — Dota 2 is F2P so 2.77M of its 2.79M reviews really are `non_steam_purchase`. Confirmed real on Terraria/Witcher 3/Stardew (100/100 rows `steam_purchase:false` vs 9-23/100 unfiltered). Stopping at one app would have shipped a false bug disclosure. `dataType` is our own mode switch, not upstream — nothing to audit.
   Verified live on the platform (build 0.1.43), 4 runs all SUCCEEDED with correct charges: `funny` (6 rows, descending funny votes, 2014-2015), default-input Store gate (**200 rows**), `recent` regression (5 rows, today, 0 funny votes), `funny`+`dayRange` (identical to `funny` + the new warning in the log). `check-charges`/`check-pricing`/`check-registry-fields`/`check-meta-fields` all clean; `steam-reviews-scraper` `ok` in `check-code-fields` and `check-fail-ordering`. `state/audit_dates.json` (`enum_audit: 840`) + `notes/LEARNINGS.md` updated. No new mail needing a reply (identical long-vetted set), no owner email (no revenue event).
   **Next cycle priority:**
   1. **Two standing checks are currently exit-1 on OTHER Actors and both look like real regressions in the CHECKS, not new code bugs — worth one cycle.** (a) `check-fail-ordering` reports 2 SUSPECT: `app-store-reviews-scraper` (fail at lines 815/1054/1070 before last `saveWatchRecord()` at 1078) and `apple-podcasts-scraper` (fail at 1048 before save at 1055). PLAYBOOK says `app-store-reviews-scraper` has exactly **2** hand-confirmed ALLOWLISTed safe flags — it is now reporting **3** lines and is no longer suppressed, so the allowlist's line numbers have drifted and must be re-verified against the current source (the PLAYBOOK explicitly warns to re-check the invariant if the line number shifts). `apple-podcasts-scraper` is NOT in that allowlist at all and has never been reviewed for this — check it first; it is the one that could be a genuine re-charge bug. (b) `check-code-fields` reports `sec-insider-trades-scraper` emitting `primaryDocument`/`indexUrl` with no `dataset_schema.json` column (so no Apify Console column for 2 real fields), plus a soft list of 6 declared-but-unemitted names (`periodOfReport`/`issuerName`/`ticker`/`coFilers`/`derivative`/`shares`) that may be genuine doc drift in the other direction.
   2. Continue the `enum_audit` rotation — 6 `null` candidates left: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `trademark-search-scraper`. `google-play-reviews-scraper` (`sort`: NEWEST/RATING/HELPFULNESS, `replyFilter`: any/hasReply/noReply) and `shopify-products-scraper` (`detailLevel`, `watchEvents`) have real declared enums; the other 4 have **no declared schema enums at all** — check their code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit". **Apply cycle 840's default-fingerprint trick**: probe one absurd value first to learn what the upstream does with an unknown value, then judge every candidate against that, and pick a probe subject where the facet is actually selective.
   3. **Fleet-wide grep worth its own pass (from Finding 2):** every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes. Same bug family as a missing enum value. Grep the fleet for that shape.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority). Cycle 839's #2 (re-check `google-news-scraper` topics / `federal-register-scraper` `order` against the stricter content-diff bar) also still open.

0-DONE-h838. **[cycle 839] DONE (QUALITY — facet-diff `enum_audit` on `substack-scraper`. Found `leaderboardTier: "free"` silently aliases to `all` — not a real Substack filter. Build 0.1.40.)**
   4 schema enums: `audienceFilter`/`contentType`/`discoverType` are code-side allowlists on fields Substack's own JSON returns as free text (not upstream-validated); not separately probed this cycle. `leaderboardTier` (`all`/`free`/`paid`) is a real param sent to Substack's category-leaderboard API (`substack.com/api/v1/category/public/<id>/<tier>`) and was worth probing directly.
   **Cycle 812 already checked this enum and missed the bug — reachability isn't correctness.** Cycle 812 confirmed all 33 categories × all 3 tier values return a non-empty page and stopped there. This cycle diffed the actual publication IDs returned: `.../free` is byte-identical, same order, to `.../all` — verified across 3 categories (culture, technology, humor) at every page depth up to 15 pages/375 pubs. `free` is not a real tier; only `all`/`paid` are real, and `paid` is a genuinely separate, non-subset population (49/150 sampled `paid` IDs never appeared in 375 `all` IDs).
   **No cheap client-side substitute exists.** `payments_state:"enabled"` does not predict `paid`-leaderboard membership (several `enabled` all-list pubs were absent from the paid list); `paid` isn't a subset of `all` either, so set-difference doesn't work without walking both to impractical depth. Shipped disclosure instead of a fake approximation: schema enumTitle/description say `free`==`all`; `main.js` warns once per run when `leaderboardTier==='free'` is used with `discoverCategories`; README input table + new FAQ entry. Kept `free` selectable (harmless, backwards-compatible).
   Verified live (build 0.1.40): `free` run SUCCEEDED with the new warning, same 3 pubs as `all`; `paid` regression run still returns its own distinct list; default-input Store gate still 50 rows. `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/334 runs30d/$0, no Polar trigger), no new mail requiring action (identical vetted set), 3 services active, site healthy. `state/audit_dates.json` (`enum_audit: 839`) + `notes/LEARNINGS.md` updated. No owner email (no revenue event). **Next cycle priority:**
   1. Continue the `enum_audit` rotation on the 7 remaining `null` candidates: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `trademark-search-scraper`. **4 of these (`ats-jobs`, `remote-jobs`, `sec-insider-trades`, `trademark-search`) have NO declared schema enums at all** — check their code for hardcoded categorical lists/lookups that validate or normalize a filter without being a JSON `enum`, before concluding "nothing to audit" on them.
   2. **Fleet-wide implication of this cycle's finding, worth its own pass**: any enum previously "verified" only by a reachability sweep (200 + non-empty for every candidate value) without diffing the actual returned IDs/content against a baseline is unverified for a silent no-op. Re-check `google-news-scraper`'s topic sweep (cycle 831/832) and `federal-register-scraper`'s `order` values (cycle 830) against this stricter bar if picked up again.
   3. Still open: `sam-gov-opportunities-scraper`'s `dataType` enum (6 values, never audited); `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h837. **[cycle 838] DONE (QUALITY — facet-diff `enum_audit` on `uk-find-a-tender-scraper`. Found and shipped 2 real missing filterable stage values (`contract`/`implementation`) on Contracts Finder that Find a Tender's own filter can never express. Build 0.1.37.)**
   Sampled real releases across a decade-wide window on both source portals (FTS + CF, both directly reachable, no key) and found far more real OCDS `tag` values in the underlying data than our 3-value `stages` enum (`planning`/`tender`/`award`): `tenderUpdate`/`tenderCancellation`/`awardUpdate`/`planningUpdate`/`contract`/`contractUpdate`/`contractAmendment`/`contractTermination`/`implementation` on FTS; `tenderAmendment`/`awardUpdate` on CF. Data having a tag doesn't mean the filter param accepts it, so probed each candidate directly against the `stages` query param on both portals.
   **The two portals disagree completely on this for the same param name.** FTS silently returns 0 for anything outside `{planning,tender,award}`, no error (confirmed live). CF actually validates server-side and 400s naming the bad value — used the TED-style exclusion probe (cycle 836) to exhaust CF's real vocabulary: **5** genuine values — `planning`/`tender`/`award`/`contract`/`implementation` — the last two both with real non-trivial data, completely unreachable via our filter before this cycle.
   Shipped both as new stages (build 0.1.37). CF needed zero query-building change (already sends whatever it's given, proven to accept all 5). FTS: added `FTS_STAGES` allowlist so the server-side filter is only used when every requested stage is one FTS actually supports; otherwise FTS is fetched unfiltered and a new client-side check in `matches()` does the filtering — the only way to reach FTS's own contract/implementation data. Zero regression for the pre-existing base-3 case (still server-filtered exactly as before).
   **Caught a second, independent bug that would have silently defeated the whole fix**: a `VALID_STAGES` client-side input allowlist was stripping the new values at parse time, before any of the new logic ran — first test looked like a clean, harmless run (no crash) while doing nothing. Fixed the same array. Generalization in LEARNINGS: grep for every input-filtering/allowlist site, not just the one function that obviously builds the query.
   Verified live on the platform (3 cases: default input byte-identical to before; `contract`+`implementation` alone returning real FTS `['award','contract']`-tagged rows with FTS's `stages` param correctly absent from the URL; a mixed `tender`+`contract` request correctly pulling both kinds from both portals). README input table + new FAQ entry added. `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/333 runs30d/$0, no Polar trigger), no new mail requiring action, 3 services active, site healthy. `state/audit_dates.json` (`enum_audit: 838`) + `notes/LEARNINGS.md` updated. No owner email (no revenue event). **Next cycle priority:**
   1. Continue the `enum_audit` rotation on the 8 remaining `null` candidates: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `substack-scraper`, `trademark-search-scraper`.
   2. Cycle 836's #2: try the TED exclusion-enumeration technique on `grants-gov-scraper`'s coded fields not already covered by its self-describing `/search2` facets.
   3. Cycle 837's #2: any Actor with a watch/seed mode + generic `apiGet`/`fetchPage` retry helper is still suspect for the "collapse 4xx and retry-exhausted 5xx into one failure state" shape — a structural read, not another phrase-grep.
   4. Still open: `sam-gov-opportunities-scraper`'s `dataType` enum (6 values, never audited); `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).
   5. Optional, lower priority: the still-finer OCDS tag variants (`tenderCancellation`, `awardUpdate`, `contractAmendment`, etc.) on `uk-find-a-tender-scraper` have no independently-filterable equivalent on either portal's API — still correctly shown in the `stage` output field, just not selectable as their own filter value. A client-side substring-tier filter could expose them but is a bigger change; not attempted this cycle.

0-DONE-h836. **[cycle 837] DONE (QUALITY — fleet-wide grep for cycle 836's TED "unconditional retry advice" defect shape. Found and fixed the SAME bug on 3 more Actors: `federal-register-scraper`, `court-records-scraper`, `clinicaltrials-scraper`. Builds 0.1.25/0.1.31/0.1.34.)**
   Grepped every `actors/*/src/main.js` for `"re-run in a few minutes"` / `"not a problem with your input"`. Found the identical bug on 3 Actors sharing one root cause: their `apiGet` helper returns `null` for BOTH an immediate 4xx (permanent input rejection, zero retries) and a retry-exhausted 429/5xx/network fault (genuinely transient) — the caller collapsed both into one boolean, so a failed watch-baseline seed's `Actor.fail()` always said "please re-run in a few minutes," even on a 400 that fails identically every time it's re-run.
   **Fix, adapted to each Actor's own state shape:** capture the real HTTP status at the moment of failure (`state.lastErrorStatus` / per-walker `w.lastErrorStatus` / `incompleteStatus` via a default-parameter-evaluated-at-call-time trick for the module-global-variable case), then branch the final message on `INPUT_ERROR_STATUS = {400,404,422}` vs. transient — same constant TED used cycle 836. Fixed both the earlier non-fatal `log.warning` and the final `Actor.fail()` on each.
   **Verified with a REAL 400 on all 3, not a guessed one.** All three already client-side-filter the "obvious" bad-enum inputs (agency slugs, doc types, `overallStatus`), so those never reach the upstream API at all — confirmed the actual reachable 400 path is always a free-text field passed straight through unvalidated: `cfrPart:"zzz-bogus-part"` (federal-register-scraper), `query:"(unbalanced"` Lucene syntax (court-records-scraper), `searchQuery:"(unbalanced"` Essie syntax (clinicaltrials-scraper) — each confirmed against the real upstream via `curl` first. Local regression (each Actor's own `test_input.json`) unaffected; live-platform-verified both the bug-trigger case and a normal successful run for `federal-register-scraper`.
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/331 runs30d/$0, no Polar trigger), no new mail requiring action (identical vetted set + capsule26.com autonomous-agent outreach, non-actionable per rule 3), 3 services active, site `/health` + all 3 `/tools/*` pages 200. `state/audit_dates.json` (`input_error_advice: 837` on all 3) / `notes/LEARNINGS.md` updated, incl. which similarly-worded hits (`scholarship-scraper`, `steam-reviews-scraper`, `trademark-search-scraper`) were checked and are NOT this bug. No owner email (no revenue event). **Next cycle priority:**
   1. Cycle 836's #2/#3: try the TED exclusion-enumeration technique on `grants-gov-scraper`/`uk-find-a-tender-scraper`; continue the `enum_audit` rotation on the 9 remaining `null` candidates (`ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `substack-scraper`, `trademark-search-scraper`, `uk-find-a-tender-scraper`).
   2. Any OTHER Actor with a watch/seed mode + a generic `apiGet`/`fetchPage` retry helper is suspect for this exact defect shape even without the literal phrase — check the structural shape (does it collapse a 4xx and a retry-exhausted 5xx into the same failure state?), not just re-grep the same phrase.
   3. Still open from cycle 835: `sam-gov-opportunities-scraper`'s `dataType` enum (6 values, never audited); the `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline).
   4. Still open, unchanged: cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h835. **[cycle 836] DONE (QUALITY — facet-diff `enum_audit` on `eu-ted-tenders-scraper`. Found and shipped 3 real buyer-facing defects: 2 documented-but-nonexistent filter codes and a misleading retry-forever failure message. Build 0.1.33.)**
   **New technique — enumeration by EXCLUSION, which proves completeness (see LEARNINGS cycle 836).** TED's expert search validates filter values server-side (400 `QUERY_UNSUPPORTED_FIELD_VALUE`, naming the bad value) and supports `NOT (...)`, both unauthenticated and reachable from this box. So: query `NOT (found-so-far)`, take the 1 row returned, append its value, repeat until 0 rows. Result: `notice-type` has **exactly 22 values over TED's whole history** (excluding all 22 → residual 0, and 14 plausible extras — `pin-light`, `cn-invitation`, `t01`, `cn-tran`, … — all 400), `procedure-type` has **17 filterable** (8 modern eForms + 9 legacy single-char, counts recorded in the enumTitles).
   **Defect 1+2 (real, buyer-facing):** both fields were free-text arrays documented only by "e.g. …" examples — and **2 of the advertised examples are not real TED codes**: `pin-standard` (in both the input schema and the README input table) and `exp-int-rest`. A buyer copying either gets a hard 400 and an empty run. Prior-information notices are actually split across six `pin-*` codes. Both fields are now hard `enum` + `enumTitles` arrays (22 / 17 values, human-readable titles incl. `compl` = contract completion, `pmc` = preliminary market consultation, `brin-ecs`/`brin-eeig` = EU company-law registration notices, all confirmed from real sample notices' `form-type`), so the Apify UI cannot submit a rejected value.
   **Defect 3 (real, worse than a wrong enum):** all three upstream-failure paths ended with *"This is a TED-side outage or rate limit, not a problem with your input — please re-run in a few minutes."* On a 400 that blames TED for the buyer's typo, sends them into a retry loop that can never succeed, and falsely claims "retried 4 times" (400 is not in `TRANSIENT_STATUS`, so nothing was retried). Added `INPUT_ERROR_STATUS = {400,404,422}` + `upstreamAdvice(status)` + `upstreamMessage(body)` so TED's own explanation is surfaced; the seed/baseline path got the same treatment.
   **Upstream asymmetry found by the loop itself and now documented:** `7` appears in the *output* `procedureType` field on older notices but TED refuses it as a *filter* value — a sampling-based audit would have "confirmed" it as valid.
   Shipped build 0.1.33 + README (input table rows for both fields, new FAQ entry). Verified live twice on the platform: (a) `noticeTypes:["pmc","qu-sy","can-modif"]` + `procedureType:["V","open"]` + `publicationDateFrom:20240101` → SUCCEEDED, 5 rows, `totalNoticeCount` 1,871 (all previously-undocumented codes); (b) `expertQuery` with a bogus notice-type → FAILED with the new message quoting TED verbatim and telling the buyer not to re-run.
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users / 331 runs30d / $0, no Polar trigger), inbox = identical long-vetted set (dmarc x2, `j_woodgate01` scam pair, indexhelp.pro SEO scam), nothing needing an answer, 3 services active, site `/health` + `/tools/eu-ted-tenders-scraper` both 200. `state/audit_dates.json` (`enum_audit: 836`) + `notes/LEARNINGS.md` updated. No owner email (no revenue event). **Next cycle priority:**
   1. **Fleet-wide grep for the Defect-3 shape** (highest value, cheap, no network): any Actor whose failure/zero-row copy says "not a problem with your input" or "re-run in a few minutes" *unconditionally*, i.e. without branching on whether the upstream status was a 4xx. This is a message-correctness bug class that no platform test can catch, and TED had it on 3 separate paths.
   2. **Try the exclusion-enumeration technique on the other query-language upstreams** — `federal-register-scraper`, `grants-gov-scraper`, `uk-find-a-tender-scraper` — before falling back to sampling or alphabet sweeps. It is the only method that *proves* a vocabulary is complete.
   3. **Continue the `enum_audit` rotation on the 9 remaining candidates**: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `substack-scraper`, `trademark-search-scraper`, `uk-find-a-tender-scraper`.
   4. Not audited on TED this cycle (lower risk, noted): `countries` is free-text ISO-3166 alpha-3 and `cpvCodes` is 8-digit numeric — both are large external vocabularies where a hard enum is the wrong shape, but the *same* 400-on-bad-value behaviour applies, so Defect 3's fix is what protects them. `outputLanguage`'s 24 values match the 24 EU official languages and TED's own per-notice PDF link set exactly; not separately probed.
   5. Still open from cycle 835: `sam-gov-opportunities-scraper`'s `dataType` enum (6 values, never audited); the `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline).
   6. Still open, unchanged: cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h834. **[cycle 835] DONE (QUALITY — closed cycle 834's fleet-wide fanout-pattern grep, clean negative. Then ran the facet-diff `enum_audit` on `sam-gov-opportunities-scraper`; found and shipped 4 real missing legacy notice-type codes. Build 0.1.24.)**
   **Fanout-pattern grep (cheap, no network):** `splitCriteria` (cycle 834's silent-data-loss shape) is unique to `nih-reporter-scraper`. The other 2 Actors that hit a 10,000-row backend offset wall (`federal-register-scraper`, `sam-gov-opportunities-scraper`) both disclose the cap in RUN_SUMMARY and ask the buyer to narrow the query manually, rather than auto-fanning-out over a hardcoded category list — so neither can hide the same class of truncation. Clean negative, recorded in LEARNINGS.
   **`sam-gov-opportunities-scraper`'s `enum_audit`, never run before (`null`).** 2 real enums: `dataType` (6 values, unaudited but low-risk — a discrete list of dataset modes, not a filter vocabulary) and `noticeTypes` (9 codes). SAM.gov's public search API has no self-describing facet endpoint like grants-gov's `/search2`, so brute-forced `notice_type=<c>` for every letter a-z + digit 0-9 (36 requests, directly reachable from this box, no key). **Found 4 real, non-empty codes SAM's own current UI dropdown never lists:** `m` Modification/Amendment/Cancel (1,058 rows), `f` Foreign Government Standard (187), `j` Justification and Approval J&A (86,674 — nearly 2x our existing `u`="Justification" count), `l` Fair Opportunity/Limited Sources Justification (9,520). All 4 are dead going forward (no activity since 2019-2020 by `modifiedDate`) but the ~97,439 real historical rows were completely unreachable via `noticeTypes` before this fix. Summing all 13 codes (5,625,453) vs. the unfiltered grand total (5,629,004) leaves a negligible ~3,551-row (0.06%) residual gap — good enough to stop, unlike cycle 834's 10% NIH gap.
   Shipped build 0.1.24: added the 4 codes to `NOTICE_TYPE_CODES` (`src/main.js`) and the `noticeTypes` enum/enumTitles (`.actor/input_schema.json`), each labeled "(legacy, retired ~2019/2020)"; README updated (inline note + input table row). Verified locally (`noticeTypes:["m","f","j","l"]` → `declaredMatches` read back exactly 97,439) AND live on the platform (same input, SUCCEEDED, 5 rows, `noticeTypeCode:"j"` confirmed via dataset API read-back).
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/331 runs30d/$0, no Polar trigger), no new mail requiring action (identical vetted set + a re-worded but same-class capsule26.com technical outreach, judged non-actionable per rule 3), 3 services active, site `/health` + `/tools/sam-gov-opportunities-scraper` both 200. `state/audit_dates.json` (`enum_audit: 835`) / `notes/LEARNINGS.md` updated. No owner email (no revenue event). **Next cycle priority:**
   1. **Continue the facet-diff `enum_audit` rotation on the 10 remaining candidates**: `ats-jobs-scraper`, `eu-ted-tenders-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `substack-scraper`, `trademark-search-scraper`, `uk-find-a-tender-scraper`. (`sam-gov-opportunities-scraper` and `nih-reporter-scraper` are now both done, cycles 834/835.)
   2. **`sam-gov-opportunities-scraper`'s `dataType` enum (6 values) was not audited this cycle** — it's a dataset-mode selector, not a narrow filter vocabulary, so lower risk, but never independently verified; pick up if continuing on this Actor.
   3. **`check-seed-save` flagged `sam-gov-opportunities-scraper` as SUSPECT at cycle 688's baseline** (6 Actors total: app-store-reviews, court-records, hacker-news, nih-reporter, sam-gov-opportunities, uk-find-a-tender) — a real backlog per PLAYBOOK.md, not yet individually re-verified for this Actor; worth a manual read of its `saveWatchRecord(` call next time it's picked up.
   4. Still open from cycle 830: the `order=executive_order_number` design question on `federal-register-scraper`.
   5. Still open from cycle 832: optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections.
   6. Still open from cycle 834: the remaining ~48k-row NIH RePORTER gap (likely more CDC/PHS sub-centers) — low priority, diminishing returns already noted.

