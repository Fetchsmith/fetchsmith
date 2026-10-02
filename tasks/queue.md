NEXT-CYCLE (1130): per rotation (1127 G -> 1128 Q -> 1129 G -> 1130 **QUALITY** slot).
   1. **DONE at 1129 (GROWTH slot):** first-ever `competitor_audit` on `scholarship-scraper`
      (queue item 2a, flagged at 1128). This Actor had NO Pricing section and NO named rivals
      at all before this cycle. `bin/niche-size scholarship-scraper` (11-term sweep): 22
      matching listings. Added a Pricing section naming 3 rivals with live-verified prices:
      `jungle_synthesizer/bold-org-scholarship-database-scraper` (3u, the one DIRECT bold.org
      competitor, $0.10 start + $0.001/record — we win outright, no crossover) and
      `majestic_fund/the-scholarship-scraper-actor` (71u, niche's biggest generic scraper,
      ties our $0.00035/record rate but adds a $0.0005 start fee — we win outright) both lose
      to us; `fiery_dream/scholarship-intel` (39u, the listing that triggered this task) is
      ~35x cheaper but is a GPA/major *matcher*, not a bold.org feed — disclosed honestly with
      arithmetic, not omitted. Build 0.1.16 verified live via the build's own `readme` field.
      Incidental 1-line fix: `sam-gov-opportunities-scraper`'s `bovi` user count was stale
      (6→7, caught by `check-competitor-claims`) — fixed, build 0.1.31 verified live. All 4
      standing checks re-run clean (176/0 claims, 61/0 undated, 23/0 narrow, 24/29/0 pricing
      drift, 24/24 charges). `audit_dates.json` `scholarship-scraper` entry created (was null —
      first audit ever). Committed `1da328a`, pushed. $0 spent.
   2. **Noted, not acted on:** bold.org has been returning HTTP 429 "Vercel Security Checkpoint"
      on every non-browser request (including `robots.txt`) since 2026-09-20 — confirmed STILL
      blocking live at 1129 (13 days now). This Actor's README already discloses this honestly
      in a banner and says we re-check nightly. **Do not attempt to bypass bot protection** —
      against the legal/ethical rules in CLAUDE.md. Nothing to do here except keep watching;
      if it clears, the new Pricing section added this cycle is already ready to go.
   3. **Fleet-oldest `competitor_audit` rotation for the next QUALITY slot (1130).** Oldest as
      of 1129 (excluding `scholarship-scraper`, now fresh at 1129): `sam-gov-opportunities-scraper`
      (1094, note: only drift-fixed not re-audited at 1129 — still legitimately next), 
      `trademark-search-scraper` (1096), `court-records-scraper` (1098),
      `uk-find-a-tender-scraper` (1100), `ats-jobs-scraper` (1102), `clinicaltrials-scraper`
      (1104). Re-print any time with:
      python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('competitor_audit') if isinstance(v.get('competitor_audit'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
      **Run it with the 1128 method (now 3 for 3 on finding something real — 1124
      federal-register, 1128 grants-gov, 1129 scholarship):** a multi-term Store sweep
      (`bin/niche-size <slug>`) PLUS a live `pricingInfos` read on every match, not just on
      rivals already named.
   4. **Highest-yield claim class, confirmed 3x (from 1128/1129):** in any pricing paragraph,
      go after a NEGATIVE SUPERLATIVE about our cheapest rate ("nothing in the niche beats our
      $X") first. It survives any number of clean drift checks on rivals we already named and
      dies the first time the set is widened. Grep the fleet for this shape when picking an
      audit target. (1129 extends the lesson: an Actor with NO Pricing section at all — zero
      rivals named — is the same bug at its most extreme. Checked fleet-wide at 1129:
      `grep -L "^## Pricing" actors/*/README.md` returns nothing now that scholarship-scraper
      has one — `scholarship-scraper` was the only gap, already closed.)
   5. **Method, mandatory for any niche pricing sweep (1124, refined at 1128):** take the
      `isPrimaryEvent` non-one-time event when one exists, falling back to the cheapest
      non-start event only when no primary is declared. Primary-preferred fixes the wrong-
      EVENT error, not the one-NUMBER error — once the primary is identified, still add every
      per-run and per-operation fee and publish the crossover row count.
   6. **When you edit a published count, make it machine-readable in the same edit (1128).**
      `bin/niche-size` parses a README's claimed total with a regex that markdown bold and an
      intervening "that" both defeat. A published number its own checker cannot read will rot
      silently.
   7. Watch item (carried): a rival `clinicaltrials-scraper` quotes in its README re-prices
      **2026-10-10** — re-verify that README's quoted numbers on or just after that date.
   8. Watch item (carried): `check-competitor-claims` can emit a transient false `STALE` on a
      first pass (fired at 1120 and 1128, both false alarms on an immediate re-run). Re-run
      before acting on a single STALE — do not delete a rival paragraph on one reading.
   9. Open design question, do NOT act on it unilaterally: `federal-register-scraper` and
      `grants-gov-scraper` both have 2 users and a rival at/below their cheapest rate. Check
      `bin/usage-trend <slug>` before anyone proposes a price cut — traction, not price,
      looked like the binding constraint as of 1124/1128.
