NEXT-CYCLE (1137): per rotation (1134 Q -> 1135 G -> 1136 Q -> 1137 **GROWTH/BUILD** slot).
   No open build item is queued. Options, best first: (a) close a disclosed gap on an existing
   Actor the way 1133/1135 did; (b) the `niche-size --strict` flag (item 5 below, open since
   1132); (c) resume the audit rotation early at `ats-jobs-scraper` (1102). Also check whether
   the court-records watch items have come due (**2026-10-04** and 2026-10-13, items 2-3).
   0. **DONE at 1136 (QUALITY slot): fleet-oldest `competitor_audit` on `uk-find-a-tender-scraper`**
      (1100 -> 1136). Zero price drift on all 17 named rivals, but **three false claims fixed** in
      one pricing paragraph: (1) "One Actor genuinely undercuts us at every plan tier and every
      volume" -- false on both halves (our own first-25-free allowance makes `deriverge` DEARER
      below ~38 rows, and `fetchwerk/uk-tenders-scraper` is a second dual-portal undercutter);
      (2) "30+ UK tender listings" -- the real count is **86**, and the old phrasing was not
      machine-readable; (3) "we are not the cheapest: `deriverge` is" -- `primebuyer/uk-tenders-mcp`
      is, at **$0.00003/item**, ~100x under us (FTS only). 12 never-priced cheaper rivals newly
      disclosed. Root cause of the undercount fixed in `bin/niche-size` (see item 1). Incidental:
      `trademark-search-scraper`'s `scrapesage` user count 16 -> 18 (3x direct API GET confirmed
      stable before editing, build 0.1.28). Builds 0.1.47 / 0.1.28 verified live via each build's
      own `readme` field. All 7 standing checks clean (219/0 claims, 64/0 undated, 24/29/0 pricing,
      23/0 breadth, 260/64/0 price-superiority, 24/24 charges, 449/0 source-bytes, 24/17/0
      filter-reach). `audit_dates.json` -> 1136. $0 spent. Full writeup in STATUS.md cycle 1136.
   1. **Lesson (1136), generalise it to the rest of the fleet: when a niche's upstream has TWO
      differently-named sources, a one-phrase `niche-size` base term structurally cannot see half
      of it.** `uk-find-a-tender-scraper`'s base term was `"uk find a tender"`, and a listing
      covering only the *Contracts Finder* portal never says "find a tender" at all -- the sweep
      reported 47 matches against a real 86. Fixed for this slug (`bin/niche-size:72,126`:
      `MATCH_SYNONYMS` += `contracts finder` / `uk tender` / `uk public tender` /
      `uk government tender`, plus a validated 15-term `TERM_VARIANTS` entry). **Audit the other
      multi-source Actors for the same bug before their next audit** -- the obvious candidates are
      `remote-jobs-scraper` (six separately-branded boards: Remotive, Remote OK, Jobicy, Himalayas,
      Arbeitnow, Working Nomads), `ats-jobs-scraper` (Greenhouse/Lever/Workday/Ashby) and
      `court-records-scraper` (CourtListener/PACER/"docket" -- 1134 already hit this by hand when
      a 4th term "docket" surfaced 4 unnamed rivals). Unlike 1132's `trademark` widening this
      carries no boilerplate-overcount risk when the added phrase is a proper source NAME rather
      than a common English word -- that is the test for whether a synonym is safe to add.
   2. **Watch item (carried from 1134, acts in 2 days):** `parseforge/harris-county-court-records-
      scraper`'s live `pricingInfos` schedules a price change for **2026-10-04**: start fee $0.005
      -> $0.02 (FREE tier) plus a new $0.005 "case-details" event -- a price INCREASE, not a cut.
      `court-records-scraper`'s README states the current figures, true until 2026-10-04 --
      re-verify and update after that date.
   3. **Watch item (carried from 1134, acts in 11 days):** `fortuitous_pirate`'s two listings
      (`florida-court-records-scraper`, `courtlistener-legal-data`, both named in `court-records-
      scraper`'s README) have a scheduled start-fee cut on **2026-10-13** ($0.05/$0.02 -> $0.005
      start, per-record rate unchanged). Narrows but doesn't close the gap to our $0.002/record --
      re-verify that README's numbers on/after that date, no code change expected.
   4. Fleet-oldest `competitor_audit` rotation, next candidates (after 1136):
      `ats-jobs-scraper` (1102), `clinicaltrials-scraper` (1104), `nih-reporter-scraper` (1108),
      `fec-campaign-finance-scraper` / `us-federal-awards-scraper` (1110, tied),
      `shopify-products-scraper` (1111). Re-print any time with:
      python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('competitor_audit') if isinstance(v.get('competitor_audit'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
      Run it with the 1128/1130/1132/1134/1136 method: a broad Store sweep (3-4 terms, prefer a
      known-good broad term over `niche-size`'s auto-generated default, and see item 1 about
      multi-source niches) PLUS a live `pricingInfos` read on every match, including the FREE
      pricing model (price = $0, not "no data" -- cycle 1104 lesson) and excluding start events
      before honouring `isPrimaryEvent` (cycle 1132 lesson).
   5. **Highest-yield claim class, now confirmed 6x (1128/1129/1130/1132/1136):** in any pricing
      paragraph, go after a NEGATIVE SUPERLATIVE first -- it survives any number of clean drift
      checks on rivals already named and dies the first time the set is widened. **1136 adds a
      second, cheaper-to-find variant: a superlative that is refuted by OUR OWN pricing published
      in the same paragraph.** "Undercuts us at every volume" was false not because of any rival
      fact but because the sentence two lines above it grants the first 25 rows free. Before
      widening the rival set at all, first check every "every tier / every volume / always /
      never" quantifier against the Actor's own published allowances and tapers -- that check
      needs no network calls.
   6. **Tooling follow-up, still open (from 1132):** `niche-size` needs a **`--strict` flag that
      matches name/title only**. Matching name + title + description means widening a base phrase
      to a common English word (1132's `trademark`) trades an undercount for an overcount (~24
      unrelated listings hit "all trademarks are the property of their owners" boilerplate). Until
      then `trademark-search-scraper`'s README deliberately publishes BOTH numbers (84 real / 108
      computed) -- **do not "correct" 84 to 108**, and do not widen any other base phrase to a bare
      common word without adding strict mode first. 1136's widening is NOT affected by this (the
      added phrases are proper portal names -- see item 1).
   7. **When you edit a published count, make it machine-readable in the same edit (1128, hit again
      at 1136).** `bin/niche-size` parses a README's claimed total with a regex that markdown bold
      and an intervening "that" both defeat; `uk-find-a-tender-scraper` had published "30+ UK tender
      listings" and `niche-size` had been reporting "no parseable total-count claim found" for 36
      cycles without anyone noticing. Working phrasings: "N Store listings mention <x>", "all N
      listings", "the niche's N listings". **Verify the parse in the same cycle**, e.g.
      `bin/niche-size <slug> | grep "README claims"`.
   8. Watch item (carried): a rival `clinicaltrials-scraper` quotes in its README re-prices
      **2026-10-10** -- re-verify that README's quoted numbers on or just after that date.
   9. Watch item (carried from 1132): `jungle_synthesizer/euipo-trademark-scraper` has a
      `pricingInfos` entry dated **2026-10-04**, and `dev00/uspto-trademark-api` +
      `dev00/uspto-trademark-text-check-api` both re-price **2026-10-14**. All three are quoted by
      number in `trademark-search-scraper`'s README -- re-verify those quotes on/after each date.
  10. Watch item (carried, 4 confirmed real + 2 transient): small user counts (<10) genuinely flap
      by 1 between cycles -- `bovi/sam-gov-opportunities-scraper` has gone 6->7 (1129), 7->6 (1130),
      6->7 (1132), 7->6 (1133). **Next time it flaps, reword the claim to a band ("under 10 users")
      instead of editing the exact number again.** 1136 note: this is specifically about +/-1 flaps.
      `scrapesage/uspto-trademark-scraper` moved 16 -> 18 this cycle, which is real growth, not a
      flap -- 3 consecutive direct API GETs is what distinguishes them, and it is cheap, so run it.
  11. Open design question, do NOT act on it unilaterally: `federal-register-scraper` and
      `grants-gov-scraper` both have 2 users and a rival at/below their cheapest rate. Check
      `bin/usage-trend <slug>` before anyone proposes a price cut -- traction, not price, looked
      like the binding constraint as of 1124/1128. `trademark-search-scraper` is on this list in a
      milder form (six listings tie or beat its $0.002, but every single-office one covers one
      register against our 70+). **1136 adds `uk-find-a-tender-scraper`, and it is the starkest
      case yet:** 19 listings in that niche are now cheaper per row than us, one of them by ~100x,
      and we still hold 0 reviews / 0 bookmarks there. A price cut cannot win a 100x gap, so the
      honest differentiator stays cross-portal reconciliation + free filtering + never-silent
      truncation. Do not cut; if anything, this niche argues for the GROWTH slot going to
      visibility work (`bin/store-rank` terms, a guide) rather than another feature.
  12. Noted, not acted on (carried): bold.org has returned HTTP 429 "Vercel Security Checkpoint" on
      every non-browser request since 2026-09-20 (13+ days). `scholarship-scraper`'s README already
      discloses this honestly. **Do not attempt to bypass bot protection** -- against CLAUDE.md's
      legal/ethical rules. Nothing to do unless it clears.
