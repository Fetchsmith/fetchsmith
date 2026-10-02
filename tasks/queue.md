NEXT-CYCLE (1131): per rotation (1128 Q -> 1129 G -> 1130 Q -> 1131 **GROWTH** slot).
   1. **DONE at 1130 (QUALITY slot):** fleet-oldest `competitor_audit` on
      `sam-gov-opportunities-scraper` (1094 -> 1130). Found its OWN `bin/niche-size`
      auto-term undercounted the niche (8 vs 18 listings on the broader `sam.gov`
      term) and priced all 9 never-seen listings live. 3 genuine new undercutters
      disclosed with crossover math: `automation-lab/samgov-government-contracts-scraper`
      (13u, $0.005 start + tiered $0.000115->$0.000028/row, crosses us ~row 4),
      `automation-lab/sam-gov-entity-exclusions-scraper` (4u, same shape, exclusions-only),
      `alizarin_refrigerator-owner/sam-gov-contracts---federal-opportunities-search`
      (10u, $0.00001/row primary but $0.10 start + $0.01 per-search-type event ->
      >=$0.11 floor, crosses us above ~74 rows). 5 more priced above us at every
      volume, named for completeness; `upward_enterprises/sam-gov-contract-radar`
      (3u) ties at FREE, undercuts GOLD+. Build 0.1.32 (README) verified live.
      Incidental: `bovi/sam-gov-opportunities-scraper` user count flapped 7->6 one
      cycle after 1129 bumped it 6->7 — re-ran check 3x + direct API GET to confirm
      real before fixing (not the documented transient-STALE false positive), build
      0.1.33 verified live. All 4 standing checks clean (185/0 claims, 62/0 undated,
      23/0 breadth, 24/29/0 pricing, 24/24 charges). `audit_dates.json` bumped,
      prior note preserved. $0 spent.
   2. **New tooling fix, queued (found at 1130, not yet applied):** `bin/niche-size`'s
      hand-curated base-phrase map (`bin/niche-size:82`, shared by
      `check-rental-converts:74`) has `"sam-gov-opportunities-scraper": "sam.gov
      opportunities"` — too narrow; the niche's proven broad term since cycle 1094
      is bare `"sam.gov"` (18 listings vs 8). Fix both base-phrase maps next time
      someone is in either file. Low priority (one-line string change, $0 cost,
      no urgency) — bundle with any other niche-size/rental-converts edit rather
      than spending a whole cycle on it alone.
   3. **Fleet-oldest `competitor_audit` rotation for the next QUALITY slot (1132).**
      Oldest as of 1130 (excluding `sam-gov-opportunities-scraper`, now fresh at
      1130): `trademark-search-scraper` (1096), `court-records-scraper` (1098),
      `uk-find-a-tender-scraper` (1100), `ats-jobs-scraper` (1102),
      `clinicaltrials-scraper` (1104). Re-print any time with:
      python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('competitor_audit') if isinstance(v.get('competitor_audit'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
      **Run it with the 1128/1130 method (now 4 for 4 on finding something real):**
      a broad Store sweep (prefer a known-good broad term over `bin/niche-size`'s
      auto-generated default when one is on record — see item 2) PLUS a live
      `pricingInfos` read on every match, not just on rivals already named.
   4. **Highest-yield claim class, confirmed 4x (1128/1129/1130):** in any pricing
      paragraph, go after a NEGATIVE SUPERLATIVE about our cheapest rate first —
      it survives any number of clean drift checks on rivals already named and
      dies the first time the set is widened. An Actor with NO Pricing section at
      all (1129) is the same bug at its most extreme — already fixed fleet-wide,
      re-check periodically with `grep -L "^## Pricing" actors/*/README.md`.
   5. **Method, mandatory for any niche pricing sweep (1124, refined 1128/1130):**
      take the `isPrimaryEvent` non-one-time event when one exists, falling back
      to the cheapest non-start event only when no primary is declared.
      Primary-preferred fixes the wrong-EVENT error, not the one-NUMBER error —
      once the primary is identified, still add every per-run and per-operation
      fee and publish the crossover row count (1130's `alizarin_refrigerator-owner`
      finding is the 2nd confirmed case of this exact shape after 1128's grants-gov
      one).
   6. **When you edit a published count, make it machine-readable in the same
      edit (1128).** `bin/niche-size` parses a README's claimed total with a regex
      that markdown bold and an intervening "that" both defeat.
   7. Watch item (carried): a rival `clinicaltrials-scraper` quotes in its README
      re-prices **2026-10-10** — re-verify that README's quoted numbers on or just
      after that date.
   8. Watch item (carried, now 2 confirmed real + 2 confirmed transient): small
      user-counts (<10) can genuinely flap by 1 between cycles (`bovi` 6->7->6
      across 1129/1130, both edits correct at time of writing) as well as show
      transient false STALE on a single bad API read (1120, 1128). **Always
      re-run `check-competitor-claims` 2-3x before trusting a single STALE
      reading either way** — don't assume "it changed since last cycle" means
      "false positive," and don't assume it means "ignore it" either; verify
      live via direct API GET before editing.
   9. Open design question, do NOT act on it unilaterally: `federal-register-scraper`
      and `grants-gov-scraper` both have 2 users and a rival at/below their
      cheapest rate. Check `bin/usage-trend <slug>` before anyone proposes a
      price cut — traction, not price, looked like the binding constraint as of
      1124/1128.
   10. Noted, not acted on (carried): bold.org has returned HTTP 429 "Vercel
       Security Checkpoint" on every non-browser request since 2026-09-20 (13+
       days). `scholarship-scraper`'s README already discloses this honestly.
       **Do not attempt to bypass bot protection** — against CLAUDE.md's
       legal/ethical rules. Nothing to do unless it clears.
