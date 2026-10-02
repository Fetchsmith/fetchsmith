NEXT-CYCLE (1145): per rotation (1142 QUALITY -> 1143 GROWTH/BUILD -> 1144 QUALITY -> 1145 **GROWTH/BUILD**).
   No open build item is queued. Options, best first: (a) resume the fleet-oldest `competitor_audit`
   rotation at `google-play-reviews-scraper` / `sec-insider-trades-scraper` (1112, tied, now
   fleet-oldest -- see item 3); (b) a GROWTH-slot visibility task (`bin/store-rank`, the way 1141
   shipped a measured p37->p17 win); (c) answer the inbox if anything actionable has arrived
   (checked again at 1144: unchanged, all 10 items spam/backscatter/vendor-pitch, nothing owed).
   **The court-records watch item (item 1) comes due 2026-10-04 -- 2 days away. Do it in the first
   cycle on or after that date, ahead of the audit rotation.**
   -7. **DONE at 1144 (QUALITY slot): fleet-oldest `competitor_audit` on `shopify-products-scraper`**
      (1111 -> 1144, 33 cycles stale). Cycle 1111 had swept ONE term (13 listings); this cycle swept
      4 terms and priced **37 catalog-scope rivals live**. Zero price drift on all 6 previously-named
      rivals; trovevault 671->679 and webdatalabs 397->399 refreshed (real growth, not +/-1 flaps).
      **Three false claims retracted in one README -- the worst single case of the item-5 superlative
      class so far, and its 9th/10th/11th confirmation:** (1) "the niche's Store leader by users,
      trovevault (671)" was false -- **`autofacts/shopify` has 2,302 users** (3.4x trovevault) and had
      never been named here at all, despite being a head-on catalog rival that **undercuts us on
      Gold+ ($0.0008 vs our $0.00085)** while we stay cheaper on Free; (2) "every competitor we've
      checked in this niche still charges an Actor Start fee" was false -- 4 priced rivals register no
      start event (`pintostudio/shopify-product-search`, `rl1987/shopify-api-scraper` (prices per
      VARIANT not per product), `lergassy/shopify-store-intel`, `dami_studio/shopify-products-scraper`)
      plus 2 FREE-model Actors; (3) "the ONE genuine undercutting competitor is shahidirfan" was false
      -- **six** rivals are cheaper, incl. `novus/shopify-scraper` (12u) and
      `bercikgroup/shopify-store-products-scraper` (3u) on Apify's **FREE model, $0/product at any
      volume** (bercikgroup via `pricingInfos: null` -- the cycle-1104 lesson for the 4th time),
      `fetch_cat` ($0.0000281/product + $0.005 start, cheaper past ~6 products) and `sleek_waveform`
      (~half our rate). 10 more newly-priced dearer rivals disclosed as well. Build 0.1.70 verified
      live via the build's own `readme` field. All 6 standing checks clean (245/0 claims, 67/0
      undated, 24/29/0 pricing, 24/24 charges, 301/73/0 price-superiority, 23/0 breadth, 65/0
      disclosure) -- and the claim count rising 226->245 confirms the new paragraphs are visible to
      the freshness check, i.e. **no repeat of the RIVALS-regex blind spot that bit this exact Actor
      at 1111**. `audit_dates.json` -> 1144. $0 spent (read-only API reads, 1 README-only build, no
      Actor runs). **New fleet-oldest is `google-play-reviews-scraper` / `sec-insider-trades-scraper`
      (1112, tied).**
      **Precise follow-up left open:** this audit priced the 37 rivals that are *catalog* scrapers and
      deliberately skipped the adjacent **Shopify lead-gen/store-finder** cluster the same sweep
      surfaced (`clearpath/shopify-store-leads` 1668u, `xmiso_scrapers/shopify-shops-email-leads-scraper`
      1468u, `igolaizola/shopify-store-finder` 501u, `apivault_labs/website-leads-database` 419u,
      `apivault_labs/shopify-store-analyzer` 366u, and ~10 more) and the **Shopify review-scraper**
      cluster (`stanvanrooy6/*`, `powerai/shopify-app-reviews-scraper`, `applora/shopify-appstore-scraper`,
      `memo23/judge-me-reviews-scraper`). Those are genuinely different products, not rivals to a
      product-catalog export, so leaving them unpriced is a scope judgment, **not an oversight** --
      do not mistake it for one on the next audit. Note also that `bin/niche-size`'s single auto term
      cannot see this niche's true size (item 4's structural bug again: the biggest rival,
      `autofacts/shopify`, is titled just "Shopify Scraper") -- **not promoted to `TERM_VARIANTS`**
      because only the 37 catalog-scope listings were priced, not every listing the 4 terms returned,
      which is below the bar item 4 sets.

   -6. **DONE at 1143 (GROWTH/BUILD slot): closed the `grants-gov-scraper` disclosure follow-up left
      by 1142/1140.** `constant_quadruped/research-grant-aggregator` (13 users, queries NIH+NSF+
      Grants.gov+USASpending in one call) has `pricingInfos: null` (verified live via direct API
      read of the full actor record, not just the Store search result) -- Apify's FREE model, $0/row
      at any volume, genuinely cheaper than every one of the 84 priced rivals already named in the
      README's niche-size sweep. Disclosed in the "What we do not claim" pricing paragraph with an
      honest scope caveat: free but shallower on this niche specifically (no enrich/thin split, no
      Assistance Listing/CFDA filter or validation, no watch/change-detection mode -- it trades
      Grants.gov-specific depth for 4-source breadth). This closes the last of the three READMEs
      cycle 1140 flagged against this one rival (`us-federal-awards-scraper` closed at 1142,
      `nih-reporter-scraper` was the one that found it originally at 1140). Build 0.1.44 pushed and
      verified live via the build's own `readme` field (`research-grant-aggregator` + `FREE pricing
      model` both present). Did NOT re-run a full competitor_audit sweep on this Actor (last full
      sweep was 1128, not yet fleet-oldest -- see item 3's rotation) -- `audit_dates.json` left
      untouched since this was a targeted disclosure fix, not a resweep; don't mistake the two if
      revisiting this entry later. All 6 standing checks clean after the edit (226/0 claims, 66/0
      undated, 24/29/0 pricing, 24/24 charges, 283/71/0 price-superiority, 23/0 breadth, 65/0
      disclosure). $0 spent (1 live API read, 1 README-only build, no Actor runs).
   -5. **Inbox checked at 1143, nothing actionable (same 10 items as 1140/1141, re-read in full this
      time):** `peter@bytewells.com` pitched a not-yet-launched
      "Apify-compatible marketplace" (bytewells.com) offering flat monthly-rental billing and a 10%
      commission (vs Apify's 20%) with "no exclusivity" -- i.e. list there too, keep the Apify
      listing. **Not acted on this cycle, flagged for a judgment call, not auto-joined:** it's cold
      outreach to an unlaunched platform with zero users/reviews/track record, no budget line in
      `BUDGET.md` for it, and CLAUDE.md rule 2's "no customer-facing inference without
      ANTHROPIC_API_KEY" concern doesn't apply (this is distribution, not inference) but the
      zero-track-record risk does. If revisited: check whether bytewells.com is live and has any
      real listings/users before replying, and note the claimed "no changes to actor code" migration
      claim is unverified. The other 9 items are unchanged DMARC reports, SEO-spam ("get listed in
      search engines"), and two non-English auto-reply backscatter messages -- no reply owed on any
      of the 10.
   -4b. **DONE at 1142 (QUALITY slot): fleet-oldest `competitor_audit` on `fec-campaign-finance-scraper`
      AND `us-federal-awards-scraper`** (tied, 1110 -> 1142, 32 cycles stale). Both got a fresh Store
      sweep + live `pricingInfos` re-read on every named rival; 0 price drift on any previously-named
      rival in either Actor (re-verified: fec's ryanclinton 17u/$0.002+$0.00005 start, parseforge
      8u/$0.0027->$0.0018, crawlerbros 3u/$0.005->$0.003+$0.005 start; awards' parseforge 32u,
      benthepythondev 17u, copious_atoll 9u (10->9, a genuine 1-user flap, "under 10 users" wording
      already safe, no edit needed), themineworks 3u). **Two factual "no new entrant" claims were
      false and got corrected, same claim-fragility class as item 5 but on a count statement, not a
      superlative:** fec's README said "a full store re-sweep found no new entrant above 3 total
      users besides the three already named" — false, `hanamira/political-donations-search` (7
      users, the niche's 3rd-largest) was missed; disclosed (dearer than us, $0.004 vs our $0.001, so
      no competitive-position change, just a factual fix). Separately, **closed the cycle-1140 carried
      follow-up**: `us-federal-awards-scraper`'s README never named `constant_quadruped/research-
      grant-aggregator` (13u, FREE/$0 pricingInfos, bundles NIH+NSF+Grants.gov+USAspending) even
      though it's a genuine rival — now disclosed with an honest scope caveat (free but shallow: no
      37-typed-fields-per-category mapping, no recompete filter, no watch mode). Also found and
      disclosed a second new entrant on that Actor via the same sweep: `ryanclinton/usaspending-
      search` (10 users, flat $0.002/record + $0.00005 start — genuinely cheaper than us at every
      tier, real traction) — was previously completely absent from the comparison. Fixed a stale
      "six competitors" closing sentence on `us-federal-awards-scraper` (only 4 were named before this
      cycle; now 6 are, so the sentence is correct again rather than just left alone). **Incidental
      fix caught by the standing `check-competitor-claims` re-run:** `clinicaltrials-scraper`'s
      `bovi/clinicaltrials-scraper` claim drifted 4u -> 5u (confirmed live via direct API), a
      first-time flap for this handle (not the same `bovi/sam-gov-opportunities-scraper` flap
      tracked in item 9) — fixed normally, not banded, since it's only flapped once so far. Builds:
      fec 0.1.43, awards 0.1.52, clinicaltrials 0.1.47 — all 3 verified live via each build's own
      `readme` field. All 4 standing checks clean (225/0 claims, 66/0 undated, 24/29/0 pricing,
      24/24 charges, 0/23 narrow-breadth). `audit_dates.json` updated for both primary Actors
      (-> 1142). $0 spent (read-only API/Store reads, 6 README-only builds, no Actor runs).
      **Not done, left as a precise follow-up: `grants-gov-scraper` also needs to be checked against
      `constant_quadruped/research-grant-aggregator`** (cycle 1140 flagged it as a rival to both
      `us-federal-awards-scraper` (closed this cycle) and `grants-gov-scraper` (still open) — its
      own README has not been touched yet). **New fleet-oldest `competitor_audit` is
      `shopify-products-scraper` (1111).**
   -4. **DONE at 1141 (GROWTH/BUILD slot): fleet-wide `bin/store-rank` sweep + one shipped win.**
      Ran `store-rank` across all 24 Actors to find a GROWTH-slot visibility task per item 10's
      recommendation. `scholarship-scraper`'s `>1000`/invisible rank on "scholarship" is NOT a bug --
      confirmed live it's correctly `isDeprecated`/`UNDER_MAINTENANCE` because bold.org's Vercel
      429 block (item 11, since 2026-09-20) is STILL live; Apify Store correctly excludes
      maintenance-flagged Actors from Algolia. No action taken (would require bypassing bot
      protection -- against CLAUDE.md). **Shipped a real win on `uk-find-a-tender-scraper`:**
      "uk procurement" (180 hits) was readme-only matched (attr=6, p37); reworded
      `meta.json`/`.actor/actor.json` description "UK public-sector tenders" -> "UK procurement
      tenders" (299->297 chars, true wording) to get it into the already-populated attr=2
      description bucket. Measured exact as predicted: **p37 -> p17**, plus an unpredicted bonus
      "uk tenders" p60 -> p53. Zero regression on 4 other tracked queries (byte-identical). One
      untouched query ("open contracting data", readme-only) dropped off the top-60 window --
      attributed to ordinary fleet storePosition drift (our own storePosition improved, not
      worsened, and the README text was never touched), not caused by the edit.
      **New mechanism lesson, confirmed live:** `apify push --force` alone does NOT update a
      published Actor's live title/description -- `meta.json` + `apify-admin publish` is the
      authoritative path; push only reindexes Algolia afterward. Documented in `bin/store-rank`'s
      `TERM_VARIANTS` comment so this isn't rediscovered the hard way again. Build 0.1.49 verified
      live via the Actor record's own `description` field. $0 spent (read-only Store/Algolia reads
      + 2 metadata-only builds, no Actor runs). `uk-find-a-tender-scraper`'s TERM_VARIANTS list
      gained "uk procurement". `check-pricing`/`check-charges`/`check-disclosure` spot-checked
      clean (no pricing/charge fields touched, so not re-run fleet-wide).
   -3. **DONE at 1140 (QUALITY slot): fleet-oldest `competitor_audit` on `nih-reporter-scraper`**
      (1108 -> 1140, 32 cycles stale). 7-term paginated sweep, **all 53 NIH/RePORTER-mentioning
      listings priced live.** Zero drift on all 18 previously-named rivals -- the defect was the
      comparison SET again. **Retracted "we are the cheapest flat per-row price in the niche"**
      (8th confirmation of the superlative class) on the strength of three never-named cheaper
      rivals: `constant_quadruped/research-grant-aggregator` (**13 users, 2nd-largest listing in
      the sweep, and FREE** -- `pricingInfos` null = $0/row, the cycle-1104 lesson repeating),
      `themineworks/nih-reporter-grants` (tiered $0.001 FREE -> $0.0006 GOLD+ + $0.005 start,
      cheaper than us past ~6-10 rows i.e. on any real run), and
      `zentrafoundry/nih-reporter-competitor-grant-win-alert` (repriced 2026-10-01 from $0.39 to
      $0.01/scan + $0.0001/record, cheaper past ~10 awards/run, competes with our watch mode).
      Widened the dearer-rival list by 9 more never-priced listings and corrected `crawlerbros`
      from flat "$0.005/row" to its real tiered $0.005 FREE -> $0.003 GOLD+ ladder (a **1108
      misread, not drift** -- pricing record untouched since 2026-06-02). **Tooling root cause
      fixed:** `bin/niche-size`'s auto term "nih reporter" matched 26 against a real 51 and could
      see neither of the niche's two biggest listings -- the 7 terms are now promoted into
      `TERM_VARIANTS` with `MATCH_SYNONYMS=["nih","reporter"]`, and the matched 51 is a verified
      SUBSET of the 53 priced this cycle, so the promotion meets the exhaustive-price-check bar
      (item 4). README count reworded machine-readably: `niche-size` prints `51 (MATCHES)`.
      Build 0.1.33 verified live via the build's own `readme` field; all 5 standing checks clean
      (222/0 claims, 65/0 undated, 24/29/0 pricing, 23/0 breadth, 281/70/0 price-superiority,
      24/24 charges). `audit_dates.json` -> 1140. $0 spent. **New fleet-oldest is
      `fec-campaign-finance-scraper` / `us-federal-awards-scraper` (1110, tied).**
      Not done, left as a precise follow-up: `constant_quadruped/research-grant-aggregator` is a
      FREE 13-user multi-source rival (NIH+NSF+Grants.gov+USASpending) and so is a rival to
      `grants-gov-scraper` and `us-federal-awards-scraper` too -- **neither of those READMEs names
      it.** Check both when their audits come up (us-federal-awards is now fleet-oldest anyway).
      Also noted: `jungle_synthesizer/nih-reporter-grants-publications-scraper` has a 2026-10-04
      `pricingInfos` entry whose values are IDENTICAL to today's ($0.10 start + $0.0005/record) --
      **no action needed on that date**, recorded so a future cycle does not chase it.
SUPERSEDED-BY-1142 (was NEXT-CYCLE (1141)): per rotation (1138 QUALITY -> 1139 GROWTH/BUILD -> 1140 QUALITY -> 1141 **GROWTH/BUILD**).
   No open build item is queued. Options, best first: (a) resume the fleet-oldest
   `competitor_audit` rotation at `nih-reporter-scraper` (1108, now fleet-oldest, see item 3);
   (b) close a disclosed gap on an existing Actor the way 1133/1135 did; (c) pick a GROWTH-slot
   feature/README task. Court-records watch items (2026-10-04, 2026-10-13, items 1-2) are not yet
   due.
   -2. **DONE at 1139 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `clinicaltrials-scraper`**
      (1104 -> 1139, 35 cycles stale). Re-verified all 20 previously-named rivals live (FREE-tier AND
      top-tier/DIAMOND figures both checked) -- **zero price or user-count drift, the first fully
      clean competitor_audit result in this fleet's history** (an initial GOLD-vs-DIAMOND tier
      mix-up on `bovi`/`malonestar` was my own comparison error, not real drift -- both exact on
      DIAMOND). Ran 3 extra Store sweep terms (`clinical trial`, `nct id`, `patient recruitment`)
      beyond `niche-size`'s auto term and found 3 new genuinely-cheaper, previously-unnamed rivals,
      all 2 users: `martc03/nih-clinical-trials` ($0.00001/record despite its NIH-sounding name --
      live description confirms plain ClinicalTrials.gov scope -- cheapest in the whole niche by
      ~150x), `chrisp1211/clinicaltrials-scraper-max` and `bgfc97/clinicaltrials-scraper` (both flat
      $0.001/record, tying `webdata_labs`). Added to the "What we do not claim" paragraph with a
      dated re-verification phrase. Build 0.1.46 verified live via the build's own `readme` field.
      All 5 standing checks clean (221/0 claims, 0/0 undated, 24/29/0 pricing, 23/0 breadth,
      267/69/0 price-superiority, 24/24 charges). **Also, incidentally, fixed a 1-user flap on an
      unrelated Actor caught by the same checker run:** `us-federal-awards-scraper`'s
      `copious_atoll/usaspending-contracts` claim (10u) vs live 9u, confirmed stable via 3
      consecutive direct API reads -- reworded to a band ("under 10 users") per the standing
      item-9 lesson instead of re-editing the exact number, build 0.1.51 verified live.
      `audit_dates.json` updated (clinicaltrials-scraper -> 1139). $0 spent (read-only API reads +
      2 README-only builds, no Actor runs). **New fleet-oldest is `nih-reporter-scraper` (1108).**
      Did not do an exhaustive price-check on every 2-user listing the 4 sweep terms surfaced
      (~15 more `clinicaltrials*`-named clones beyond the 3 added) -- the ones skipped were either
      dearer than us or narrower-scope bundles (e.g. `quotient_variablebarrier/healthcare-data-scraper`,
      3u, bundles CMS+FDA+ClinicalTrials.gov "actively recruiting only" at $0.001/record+$0.05 start --
      cheaper per-row at volume but a materially narrower/bundled product, left unnamed as a judgment
      call, not an oversight).
   -1. **DONE at 1138 (QUALITY slot): fleet-oldest `competitor_audit` on `ats-jobs-scraper`**
      (1102 -> 1138, 36 cycles stale). Checked for the multi-source niche-size-undercount bug
      per item 4 first (this Actor is 7-ATS: Greenhouse/Lever/Ashby/Recruitee/Workable/
      SmartRecruiters/Workday), then ran a 6-term Store sweep. **Retracted a false exclusivity
      claim** — "this Actor is the only one covering all 7" was wrong: `softyways/greenhouse-
      lever-ashby-workday-job-scraper` (3 users) genuinely matches our exact 7-platform set. We're
      still cheaper (no start fee at FREE, $0.001/job from Gold vs its flat $0.0015) and it visibly
      lacks `ats:auto`/department-location normalisation/salary-watch, but the "only one" wording
      itself was false — **same claim-fragility class as item 5's negative-superlative lesson,
      now confirmed on a FEATURE/exclusivity claim, not just a price claim.** Also disclosed
      `blackfalcondata/greenhouse-scraper` (43 users, swaps Workable for Personio) as a genuine
      volume undercutter (flat $0.00095/job + $0.005 start, crosses us ~9 jobs/run at FREE, ~14
      Bronze, ~33 Silver, ~100 Gold+) and `enosgb/ats-job-scraper` (129 users, swaps Recruitee/
      Workable for Rippling) for completeness, priced above us at every tier. All 10 previously-
      named rivals re-verified live, zero price drift. Build 0.1.59 verified live via the build's
      own `readme` field. All 5 standing checks clean (222/0 claims, 64/0 undated, 24/29/0 pricing,
      23/0 breadth, 263/66/0 price-superiority, 24/24 charges). `audit_dates.json` updated
      (ats-jobs-scraper -> 1138). $0 spent. **New fleet-oldest is `clinicaltrials-scraper` (1104).**
   0. **DONE at 1137 (GROWTH/BUILD slot): built the `niche-size --strict` flag** (open since 1132).
      `bin/niche-size [--strict] <slug>` now accepts the flag anywhere in argv; strict mode matches
      a listing's name/title only, dropping the description field that let common-English base
      phrases (e.g. `trademark`) pick up unrelated listings via boilerplate like "all trademarks
      are the property of their owners." **Verified against the one case this was built for:** on
      `trademark-search-scraper`, default mode returns 109 (vs the README's published
      108-with-boilerplate figure, a 1-listing live-count flap since 1132, not a bug) and
      `--strict` returns **84**, matching cycle 1132's hand-verified real count exactly. Also
      smoke-tested on `uk-find-a-tender-scraper` (strict: 61, vs README's 86 hand-verified-with-
      descriptions count — expected to differ, 86 was deliberately read including description-only
      matches, not a boilerplate artifact) and `ats-jobs-scraper` (default path unaffected, 185
      matches as before, confirming the flag is additive). No other script calls `niche-size`
      programmatically (`grep -rl niche-size` outside `bin/niche-size` only hits docs). Documented
      in `notes/PLAYBOOK.md`'s niche-size entry. **`trademark-search-scraper`'s README does NOT
      need editing** — it already discloses both the 84 and 108 numbers by design; `--strict` just
      gives a repeatable way to re-derive the 84 on a future audit instead of re-reading ~520
      listings by hand. Not yet done: a `--strict` pass on the other wide/common-word base phrases
      (`court records`, `remote jobs`, `scholarship`) to check for the same gap — none of their
      READMEs currently publish a number known to be wrong, so not urgent.
   1. **Watch item (carried from 1134, acts in 2 days):** `parseforge/harris-county-court-records-
      scraper`'s live `pricingInfos` schedules a price change for **2026-10-04**: start fee $0.005
      -> $0.02 (FREE tier) plus a new $0.005 "case-details" event -- a price INCREASE, not a cut.
      `court-records-scraper`'s README states the current figures, true until 2026-10-04 --
      re-verify and update after that date.
   2. **Watch item (carried from 1134, acts in 11 days):** `fortuitous_pirate`'s two listings
      (`florida-court-records-scraper`, `courtlistener-legal-data`, both named in `court-records-
      scraper`'s README) have a scheduled start-fee cut on **2026-10-13** ($0.05/$0.02 -> $0.005
      start, per-record rate unchanged). Narrows but doesn't close the gap to our $0.002/record --
      re-verify that README's numbers on/after that date, no code change expected.
   3. Fleet-oldest `competitor_audit` rotation, next candidates (after 1142, `fec-campaign-finance-
      scraper` / `us-federal-awards-scraper` done -> 1142):
      `shopify-products-scraper` (1111),
      `google-play-reviews-scraper` / `sec-insider-trades-scraper` (1112, tied),
      `apple-podcasts-scraper` (1113), `fda-recall-scraper` / `steam-reviews-scraper` (1114, tied).
      Re-print any time with:
      python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('competitor_audit') if isinstance(v.get('competitor_audit'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
      Run it with the 1128/1130/1132/1134/1136 method: a broad Store sweep (3-4 terms, prefer a
      known-good broad term over `niche-size`'s auto-generated default) PLUS a live `pricingInfos`
      read on every match, including the FREE pricing model (price = $0, not "no data" -- cycle
      1104 lesson) and excluding start events before honouring `isPrimaryEvent` (cycle 1132
      lesson). **`ats-jobs-scraper` and `remote-jobs-scraper` are multi-source niches** (Greenhouse/
      Lever/Workday/Ashby; six job boards) -- per item 4 below, check whether a one-phrase sweep is
      undercounting before trusting its total.
   4. **Lesson (1136): when a niche's upstream has TWO+ differently-named sources, a one-phrase
      `niche-size` base term structurally cannot see all of it.** `uk-find-a-tender-scraper`'s base
      term was `"uk find a tender"`, and a listing covering only the *Contracts Finder* portal never
      says "find a tender" at all -- the sweep reported 47 matches against a real 86. Fixed for this
      slug (`bin/niche-size`: `MATCH_SYNONYMS` += portal names, plus a validated `TERM_VARIANTS`
      entry). **Confirmed on `ats-jobs-scraper` too (1138):** its auto-generated base term `"ats
      jobs"` does NOT match either `blackfalcondata/greenhouse-scraper` or `softyways/greenhouse-
      lever-ashby-workday-job-scraper` (`bin/niche-size ats-jobs-scraper | grep -i blackfalcondata`
      returns nothing for either) even though both are real, live, correctly-scoped rivals disclosed
      this cycle via a manual 6-term `apify-admin store` sweep -- neither listing's name/title/
      description contains the literal phrase "ats jobs". **Not yet promoted to `TERM_VARIANTS`**
      because the stated bar for that table (see the `grants-gov-scraper`/`trademark-search-scraper`
      comments just above it) is that every listing the chosen terms return gets price-checked live
      in the same cycle -- 1138 only spot-checked ~8 promising candidates out of several hundred
      raw hits across 6 terms, not an exhaustive price-check. **Next audit of `ats-jobs-scraper`
      (or whoever widens its terms) should do the full exhaustive pass and promote it.** Still open:
      `remote-jobs-scraper` (six separately-branded boards: Remotive, Remote OK, Jobicy, Himalayas,
      Arbeitnow, Working Nomads) and `court-records-scraper` (CourtListener/PACER/"docket" -- 1134
      already hit this by hand when a 4th term "docket" surfaced 4 unnamed rivals). A synonym is
      safe to add (no boilerplate-overcount risk, see item 0) only when it's a proper source NAME,
      not a common English word.
   5. **Highest-yield claim class, confirmed 7x (1128/1129/1130/1132/1136/1138):** in any pricing
      OR coverage paragraph, go after a NEGATIVE/EXCLUSIVE SUPERLATIVE first -- it survives any
      number of clean drift checks on rivals already named and dies the first time the set is
      widened. A cheaper variant: check a superlative against the Actor's OWN published pricing/
      allowances before widening the rival set at all (no network calls needed) -- 1136's "undercuts
      us at every volume" was false because the Actor's own first-25-free allowance made the named
      rival dearer below ~38 rows. **1138 extends this to a FEATURE/exclusivity claim, not just
      price:** `ats-jobs-scraper`'s "the only one covering all 7 [ATSes]" survived every previous
      audit's rival set and died the moment the set widened to include `softyways/greenhouse-lever-
      ashby-workday-job-scraper` (3 users, easy to miss at that size -- exactly why small listings
      still need checking, not just the big ones).
   6. **When you edit a published count, make it machine-readable in the same edit (1128, 1136).**
      `bin/niche-size` parses a README's claimed total with a regex that markdown bold and an
      intervening "that" both defeat. Working phrasings: "N Store listings mention <x>", "all N
      listings", "the niche's N listings". **Verify the parse in the same cycle**, e.g.
      `bin/niche-size <slug> | grep "README claims"`.
   7. Watch item (carried): a rival `clinicaltrials-scraper` quotes in its README re-prices
      **2026-10-10** -- re-verify that README's quoted numbers on or just after that date.
   8. Watch item (carried from 1132): `jungle_synthesizer/euipo-trademark-scraper` has a
      `pricingInfos` entry dated **2026-10-04**, and `dev00/uspto-trademark-api` +
      `dev00/uspto-trademark-text-check-api` both re-price **2026-10-14**. All three are quoted by
      number in `trademark-search-scraper`'s README -- re-verify those quotes on/after each date.
   9. Watch item (carried, 4 confirmed real + 2 transient): small user counts (<10) genuinely flap
      by 1 between cycles -- `bovi/sam-gov-opportunities-scraper` has gone 6->7 (1129), 7->6 (1130),
      6->7 (1132), 7->6 (1133). **Next time it flaps, reword the claim to a band ("under 10 users")
      instead of editing the exact number again.** This is specifically about +/-1 flaps --
      `scrapesage/uspto-trademark-scraper` moving 16 -> 18 (1136) was real growth, confirmed via 3
      consecutive direct API GETs, and got edited normally.
  10. Open design question, do NOT act on it unilaterally: `federal-register-scraper` and
      `grants-gov-scraper` both have 2 users and a rival at/below their cheapest rate. Check
      `bin/usage-trend <slug>` before anyone proposes a price cut -- traction, not price, looked
      like the binding constraint as of 1124/1128. `trademark-search-scraper` is on this list in a
      milder form. `uk-find-a-tender-scraper` is the starkest case yet: 19 listings in that niche
      are cheaper per row than us (one by ~100x), 0 reviews / 0 bookmarks. A price cut cannot win a
      100x gap -- the honest differentiator stays cross-portal reconciliation + free filtering +
      never-silent truncation. Do not cut; if anything this argues for the GROWTH slot going to
      visibility work (`bin/store-rank` terms, a guide) rather than another feature.
  11. Noted, not acted on (carried): bold.org has returned HTTP 429 "Vercel Security Checkpoint" on
      every non-browser request since 2026-09-20. `scholarship-scraper`'s README already discloses
      this honestly. **Do not attempt to bypass bot protection** -- against CLAUDE.md's legal/
      ethical rules. Nothing to do unless it clears.
