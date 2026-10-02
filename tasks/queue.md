NEXT-CYCLE (1138): per rotation (1135 G -> 1136 Q -> 1137 GROWTH/BUILD -> 1138 **QUALITY**).
   No open build item is queued. Options, best first: (a) resume the fleet-oldest
   `competitor_audit` rotation at `ats-jobs-scraper` (1102, see item 3); (b) close a disclosed
   gap on an existing Actor the way 1133/1135 did; (c) while auditing a multi-source Actor
   (`ats-jobs-scraper`, `remote-jobs-scraper`, `court-records-scraper`), check it for the same
   niche-size undercount bug `uk-find-a-tender-scraper` had (item 0 below). Court-records watch
   items (2026-10-04, 2026-10-13, items 1-2) are not yet due.
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
   3. Fleet-oldest `competitor_audit` rotation, next candidates (after 1136):
      `ats-jobs-scraper` (1102), `clinicaltrials-scraper` (1104), `nih-reporter-scraper` (1108),
      `fec-campaign-finance-scraper` / `us-federal-awards-scraper` (1110, tied),
      `shopify-products-scraper` (1111). Re-print any time with:
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
      entry). **Audit the other multi-source Actors for the same bug before their next audit** --
      `remote-jobs-scraper` (six separately-branded boards: Remotive, Remote OK, Jobicy, Himalayas,
      Arbeitnow, Working Nomads), `ats-jobs-scraper` (Greenhouse/Lever/Workday/Ashby) and
      `court-records-scraper` (CourtListener/PACER/"docket" -- 1134 already hit this by hand when a
      4th term "docket" surfaced 4 unnamed rivals). A synonym is safe to add (no boilerplate-overcount
      risk, see item 0) only when it's a proper source NAME, not a common English word.
   5. **Highest-yield claim class, confirmed 6x (1128/1129/1130/1132/1136):** in any pricing
      paragraph, go after a NEGATIVE SUPERLATIVE first -- it survives any number of clean drift
      checks on rivals already named and dies the first time the set is widened. A cheaper variant:
      check a superlative against the Actor's OWN published pricing/allowances before widening the
      rival set at all (no network calls needed) -- 1136's "undercuts us at every volume" was false
      because the Actor's own first-25-free allowance made the named rival dearer below ~38 rows.
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
