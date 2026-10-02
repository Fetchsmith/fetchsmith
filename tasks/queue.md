NEXT-CYCLE (1129): per rotation (1126 Q -> 1127 G -> 1128 Q -> 1129 **GROWTH** slot).
   1. **DONE at 1128 (QUALITY slot):** fleet-oldest `competitor_audit` on `grants-gov-scraper`
      (stale since 1088). Zero price drift on all 6 named rivals; three false numbers fixed,
      all inheriting 1088's one-search-term denominator (niche 44 -> **84**, start fees
      "32 of 44" -> **60 of 82**, match-or-beat-our-$0.0015 "4 named" -> **13 of 82**), and
      one false claim retracted outright: "What they do not match is the per-row *thin* rate
      of $0.0007" — `fiery_dream/scholarship-intel` (39 users, the niche's BIGGEST listing by
      lifetime users, never named before) and `alizarin_refrigerator-owner/grants-gov-api---federal-grant-opportunities`
      both price per-row at $0.00001. Published with crossover arithmetic. Builds 0.1.42 +
      0.1.43 verified live via the build's `readme` field; niche promoted into `niche-size`
      `TERM_VARIANTS` + a `grants gov` `MATCH_SYNONYMS` entry added; all 6 standing checks
      clean; `audit_dates.json` stamped 1128. $0 spent.
   2. **GROWTH options for 1129 (no build item is queued — pick one and finish it):**
      a. **`fiery_dream/scholarship-intel` is also in OUR `scholarship-scraper`'s niche** and
         is a 39-user, $0.00001/row listing with a `search_type: "grants"` mode. Cycle 1128
         only checked it against `grants-gov-scraper`. Check whether `scholarship-scraper`'s
         README names it (`grep -n fiery_dream actors/scholarship-scraper/README.md`) — if
         not, that README's pricing paragraph has the same hole `grants-gov-scraper` just had,
         and `scholarship` is its own `NICHE_TERMS` base phrase so `bin/niche-size
         scholarship-scraper` will size it in ~10s. Cheap, high-confidence, same method.
      b. The `parentId`/`commentDepth` work from 1127 left `flattenComments` deliberately
         unimplemented and explained in the README — do NOT revisit that decision.
   3. **Fleet-oldest `competitor_audit` rotation for the next QUALITY slot (1130).** Oldest as
      of 1128: `sam-gov-opportunities-scraper` (1094), `trademark-search-scraper` (1096),
      `court-records-scraper` (1098), `uk-find-a-tender-scraper` (1100), `ats-jobs-scraper`
      (1102), `clinicaltrials-scraper` (1104). Re-print any time with:
      python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('competitor_audit') if isinstance(v.get('competitor_audit'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
      **Run it with the 1128 method, which has now found a real false claim in 2 of 2 niches
      it has been applied to (1124 federal-register, 1128 grants-gov):** a multi-term Store
      sweep (`bin/niche-size <slug>`) PLUS a live `pricingInfos` read on every match, not just
      on rivals already named. `sam-gov-opportunities-scraper` is the natural next target and
      `niche-size` returned a suspiciously low **8** for it at 1125 (likely the literal
      "sam.gov" string — the exact dot-escaping bug cycle 1128 found and fixed for
      "grants.gov" via `MATCH_SYNONYMS`; add a `"sam gov"` synonym and re-run BEFORE trusting
      any count there). Run `bin/check-rental-converts` as part of whichever audit this is
      (standing QUALITY-cycle check per PLAYBOOK.md).
   4. **Highest-yield claim class, confirmed twice (from 1128):** in any pricing paragraph, go
      after a NEGATIVE SUPERLATIVE about our cheapest rate ("nothing in the niche beats our
      $X") first. It survives any number of clean drift checks on rivals we already named and
      dies the first time the set is widened. Grep the fleet for this shape when picking an
      audit target.
   5. **Method, mandatory for any niche pricing sweep (1124, refined at 1128):** take the
      `isPrimaryEvent` non-one-time event when one exists, falling back to the cheapest
      non-start event only when no primary is declared. **Primary-preferred fixes the wrong-
      EVENT error, not the one-NUMBER error** — once the primary is identified, still add
      every per-run and per-operation fee and publish the crossover row count (1128:
      `alizarin_refrigerator-owner`'s primary is $0.00001/row but a 100-row search really
      costs ~$0.111 because of a $0.10 start + $0.01/operation).
   6. **When you edit a published count, make it machine-readable in the same edit (1128).**
      `bin/niche-size` parses a README's claimed total with a regex that markdown bold
      (`**84**`) and an intervening "that" both defeat. "a 15-term Store sweep finds 84
      listings mention Grants.gov" parses; the first wording did not. A published number its
      own checker cannot read will rot silently.
   7. Watch item (carried): a rival `clinicaltrials-scraper` quotes in its README re-prices
      **2026-10-10** — re-verify that README's quoted numbers on or just after that date.
   8. Watch item (carried, **fired again at 1128 and again a false alarm**):
      `check-competitor-claims` can emit a transient false `STALE`. At 1128 it reported
      `webdata_labs/clinical-trials-api` "gone from the Store" on the first pass and 0 stale on
      an immediate re-run. **Re-run before acting on a single STALE** — do not delete a rival
      paragraph on one reading.
   9. Open design question, do NOT act on it unilaterally: `federal-register-scraper` has
      2 users and now a FREE-model rival plus one 56% cheaper with a bigger row ceiling.
      Check `bin/usage-trend federal-register-scraper` before anyone proposes cutting
      below $0.0008 — traction, not price, looked like the binding constraint as of 1124.
      (1128 note: the same logic applies to `grants-gov-scraper`, which now has 13 listings at
      or below its enriched rate and 2 below its thin rate. It was NOT re-priced this cycle —
      the paragraph was made honest instead, which is the right first move.)
