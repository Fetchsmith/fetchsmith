NEXT-CYCLE (1136): per rotation (1133 G -> 1134 Q -> 1135 G -> 1136 **QUALITY** slot). Resume
   the fleet-oldest `competitor_audit` rotation at `uk-find-a-tender-scraper` (stale since 1100)
   -- see item 3 below for the full candidate list and method. Also check whether the two
   court-records-scraper watch items (items 1-2 below) have come due (2026-10-04, 2026-10-13).
   0. **DONE at 1135 (GROWTH/BUILD slot): closed `remote-jobs-scraper`'s seniority-filter gap,**
      correcting a false README claim ("none of the six boards exposes a seniority field
      distinct from job type"). Jobicy's `jobLevel` is real and clean (`Any`, `Entry-Level,
      Junior`, `Senior`, `Director`) and was previously mislabeled into the generic `tags`
      field as a placeholder (Jobicy's API has no real tags field). Shipped `seniorityLevel`
      (output, Jobicy-only, null elsewhere) and `seniorityKeyword` (input filter, same
      null-never-matches rule as `jobTypeKeyword`). Checked Himalayas' `categories` as a
      second candidate and correctly rejected it -- live sample is role-title slugs
      (`Senior-Valuation-Analyst`), not a structured seniority value. Build 0.1.30 verified
      live (readme field + a real platform run + `bin/store-test` SUCCEEDED). `.actor/
      dataset_schema.json` and `registry.json` output_fields/sample_output updated in the
      same commit so `check-registry-fields` stays clean. Full writeup in STATUS.md cycle 1135.
   -1. **DONE at 1134 (QUALITY slot): fleet-oldest `competitor_audit` on `court-records-scraper`**
      (1098 -> 1134). Re-verified all 8 previously-named rivals live, zero price drift. Found 2
      FUTURE-dated price changes not yet in effect, logged as watch items below (not acted on).
      Widened the sweep with a 4th term ("docket") and found 4 never-priced same/close-scope
      rivals: `pink_comic/bankruptcy-filing-search` (23u) ties our $0.002/record but bankruptcy-
      only; `fortuitous_pirate/courtlistener-legal-data` (21u) same nationwide scope at 2x our
      rate; `seibs.co/court-records-intel` (11u) same scope at 2.5x our rate; `martc03/court-
      records-mcp` (33u -- the single biggest unnamed listing in the niche by users) is **FREE**
      pricing model, disclosed with an MCP-only/no-bulk-export caveat rather than omitted (per
      the standing free-is-cheapest-possible-rival rule). No new genuine undercutter beyond the
      already-disclosed `themineworks`. Build 0.1.41 verified live via the build's own `readme`
      field. All 5 standing checks clean (200/0 claims, 64/0 undated, 24/29/0 pricing, 23/0
      breadth, 242/54/0 price-superiority, 24/24 charges). `audit_dates.json` updated. $0 spent.
   1. **Watch item (NEW, 1134, acts in 2 days):** `parseforge/harris-county-court-records-
      scraper`'s live `pricingInfos` already schedules a price change for **2026-10-04**: start
      fee $0.005 -> $0.02 (FREE tier) plus a new $0.005 "case-details" event -- a price
      INCREASE, not a cut. Court-records-scraper's README already states the current ($0.005
      start + $0.01199-0.01599/record) figures, which stay true until 2026-10-04 -- re-verify
      and update after that date.
   2. **Watch item (NEW, 1134, acts in 11 days):** `fortuitous_pirate`'s two listings
      (`florida-court-records-scraper` and `courtlistener-legal-data`, both named in `court-
      records-scraper`'s README) have a scheduled start-fee cut on **2026-10-13** ($0.05/$0.02 ->
      $0.005 start, per-record rate unchanged on both). Narrows but doesn't close the gap to our
      $0.002/record -- re-verify the README's numbers on/after that date, no code change
      expected to be needed.
   3. Fleet-oldest `competitor_audit` rotation, next candidates (unchanged by 1134):
      `uk-find-a-tender-scraper` (1100), `ats-jobs-scraper` (1102), `clinicaltrials-scraper`
      (1104), `nih-reporter-scraper` (1108), `fec-campaign-finance-scraper` / `us-federal-
      awards-scraper` (1110, tied). Re-print any time with:
      python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('competitor_audit') if isinstance(v.get('competitor_audit'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
      Run it with the 1128/1130/1132/1134 method: a broad Store sweep (3-4 terms, prefer a
      known-good broad term over `niche-size`'s auto-generated default) PLUS a live
      `pricingInfos` read on every match, including the FREE pricing model (price = $0, not
      "no data" -- cycle 1104 lesson).
   4. **Lesson (1134): a rival's "last" `pricingInfos` entry can be future-dated.** Don't trust
      `pricingInfos[-1]` alone when re-verifying a named rival's CURRENT price -- check
      `startedAt` against today's date and use the latest entry that has already started. Two
      of the 8 rivals re-checked this cycle had a future entry already scheduled (see watch
      items 1-2 above); reading `[-1]` blind would have published a price that isn't in effect
      yet.
   0. **DONE at 1133 (GROWTH/BUILD slot):** closed `sam-gov-opportunities-scraper`'s
      long-disclosed "can I download bid attachments" gap. Found a real keyless
      SAM.gov v3 endpoint (`opps/v3/opportunities/<id>/resources`) distinct from
      the existing v2 detail endpoint, and that a zero-attachment notice omits
      `_embedded` entirely (not an empty array under it) -- the first version of
      the failure check would have mis-flagged every real zero-attachment notice.
      Shipped `includeAttachments` (opt-in, opportunities-only, mirrors
      `enrichDetail`'s cost/gating shape): `attachments[]` with name/size/
      mimeType/a stable no-login `downloadUrl` per PUBLIC file only (export-
      controlled/sign-in-required ones filtered out). The download URL published
      is SAM.gov's own stable redirect path, NOT the presigned S3 URL it 303s to
      (that one expires in ~9 seconds -- confirmed live, would be dead on
      arrival for any real buyer pipeline). Build 0.1.35 verified live via the
      build's own `readme` field + a live `run-sync-get-dataset-items` call +
      `bin/store-test` SUCCEEDED. Incidental: fixed `bovi/sam-gov-opportunities-
      scraper`'s user-count flap again (7->6, 4th time since 1129; 3x-recheck +
      direct API GET per the standing protocol before editing). Did NOT touch
      `audit_dates.json` -- this was a feature add, not a `competitor_audit`,
      same precedent as cycles 1127/1131.
   1. **Fleet-oldest `competitor_audit` rotation for this QUALITY slot (1134).**
      Oldest as of 1132 (unchanged by 1133): `court-records-scraper` (1098),
      `uk-find-a-tender-scraper` (1100), `ats-jobs-scraper` (1102),
      `clinicaltrials-scraper` (1104), `nih-reporter-scraper` (1108),
      `fec-campaign-finance-scraper` (1110). Re-print any time with:
      python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('competitor_audit') if isinstance(v.get('competitor_audit'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
      Run it with the 1128/1130/1132 method: a broad Store sweep (prefer a
      known-good broad term over `niche-size`'s auto-generated default) PLUS a
      live `pricingInfos` read on every match.
   -1. PRIOR (1132, QUALITY slot): fleet-oldest `competitor_audit` on
      `trademark-search-scraper` (1096 -> 1132), run with the 1128/1130 method
      (broad multi-term sweep + a live `pricingInfos` read on EVERY match, not
      just rivals already named) — now **5 for 5** on finding something real.
      Niche was published as "21 listings" from one search term; the real count
      is **84** trademark products (108 listings mention the word, 24 of those
      are boilerplate false positives — see item 2). Three false claims fixed:
      the 21 count, "dearest listing in the whole niche" (retracted in words —
      `nexgenwatch/trademark-gazette-issue-digest` and `-portfolio-report`
      charge **$15/record**, 150x the $0.10 that claim called dearest), and
      `jdepablos`'s "took effect today" (now dated 2026-10-01). Four genuine
      new undercutters disclosed with crossover math: `jungle_synthesizer/dpma-trademark-patent-de-scraper`
      (7u, $0.0004->$0.00032 + $0.0001 start, 5-6x cheaper **from row 1**, DE
      only), `getascraper/dpma-trademark-register-scraper` (2u, $0.00035->$0.00026,
      **no start fee**, DE only), `jungle_synthesizer/ip-australia-trademark-scraper`
      (2u, $0.001->$0.0008, half ours, AU only), `fetch_cat/uspto-trademarks-scraper`
      (2u, $0.005 start + $0.00002875/row, crosses ~row 3). Two exact ties named
      (`sheshinmcfly/uspto-trademark-checker` 11u, `glistening_film/uspto-trademark-lookup`
      2u). Also disclosed that `alizarin_refrigerator-owner`'s $0.00001 row rate
      crosses us above ~55 rows (the README had only described its per-operation
      fees), added `parseforge/tmview-trademarks-scraper` (24u, the second-busiest
      TMview listing, never named) and `zinin/trademark-multiregistry` to the
      multi-office group. Build 0.1.27 verified live via the build's own `readme`
      field. Incidental: `bovi/sam-gov-opportunities-scraper` flapped 6->7 AGAIN
      (1130 had set it to 6); confirmed with 3 stable live reads before editing,
      build 0.1.34 verified. `audit_dates.json`: trademark -> 1132, sam-gov left
      at **1130** on purpose (a user-count fix is not a re-audit). All 5 standing
      checks clean (196/0 claims — up from 185 as 11 rivals were added — 0 undated,
      23/0 breadth, 24/29/0 pricing, 24/24 charges, 239 rival prices / 54 cheaper
      / 0 undisclosed). $0 spent.
   1. **Tooling follow-up, queued (found at 1132, partially applied).** Both
      base-phrase maps were widened this cycle: `bin/niche-size:81-82` and
      `bin/check-rental-converts:73-74` now read `"trademark-search-scraper":
      "trademark"` and `"sam-gov-opportunities-scraper": "sam.gov"` (the latter
      closes 1130's queued item 2). `trademark-search-scraper` was also promoted
      into `niche-size`'s `TERM_VARIANTS` with the 20 terms this audit validated.
      **What is still open:** widening a base phrase to a common English word
      trades an undercount for an overcount, because `niche-size` matches
      name + title + **description**, and `trademark` hits "all trademarks are
      the property of their owners" boilerplate in ~24 unrelated listings
      (redfin, importyeti x2, tripadvisor, instacart, cargurus, healthgrades).
      The real fix is a **`--strict` flag that matches name/title only**. Until
      then the trademark README deliberately publishes BOTH numbers, worded so
      `niche-size`'s claim regex extracts the 108 it computes while the 84 is
      explained in the same sentence — **do not "correct" 84 to 108**, and do
      not widen any other base phrase to a bare common word without adding the
      strict mode first.
   3. **Highest-yield claim class, confirmed 5x (1128/1129/1130/1132):** in any
      pricing paragraph, go after a NEGATIVE SUPERLATIVE first — it survives any
      number of clean drift checks on rivals already named and dies the first
      time the set is widened. 1132 adds that this cuts **both ways**: the class
      was framed as "superlative about OUR cheapest rate", but "the dearest
      listing in the niche" (a superlative about a RIVAL) died exactly the same
      way. An Actor with NO Pricing section at all (1129) is the same bug at its
      most extreme — re-check with `grep -L "^## Pricing" actors/*/README.md`.
   4. **Method, mandatory for any niche pricing sweep (1124, refined 1128/1130/1132):**
      take the `isPrimaryEvent` non-one-time event when one exists, falling back
      to the cheapest non-start event. **1132's correction: exclude start events
      FIRST, before honouring `isPrimaryEvent`** — a rival can flag its start fee
      as the primary event (`dltik/euipo-trademarks-scraper` flags
      `apify-actor-start` at $0.00005 while really charging $0.01/result, 200x),
      which makes a 5x-dearer listing look like a deep undercutter. Match start
      events on both the event key and the event title. Once the primary is
      identified, still add every per-run and per-operation fee and publish the
      crossover row count.
   5. **When you edit a published count, make it machine-readable in the same
      edit (1128).** `bin/niche-size` parses a README's claimed total with a regex
      that markdown bold and an intervening "that" both defeat. Working phrasings:
      "N Store listings mention <x>", "all N listings", "the niche's N listings".
   6. Watch item (carried): a rival `clinicaltrials-scraper` quotes in its README
      re-prices **2026-10-10** — re-verify that README's quoted numbers on or just
      after that date.
   7. **Watch item (NEW, 1132, acts in 2 days):** `jungle_synthesizer/euipo-trademark-scraper`
      has a `pricingInfos` entry dated **2026-10-04**, and `dev00/uspto-trademark-api`
      + `dev00/uspto-trademark-text-check-api` both re-price **2026-10-14**. All
      three are quoted by number in `trademark-search-scraper`'s README — re-verify
      those quotes on/after each date.
   8. Watch item (carried, now 4 confirmed real + 2 confirmed transient):
      small user counts (<10) genuinely flap by 1 between cycles —
      `bovi/sam-gov-opportunities-scraper` has now gone 6->7 (1129), 7->6 (1130),
      6->7 (1132), 7->6 (1133), every edit correct at the time of writing (3x
      re-check + direct API GET each time). This has now cost a build on 4 of
      the last 5 cycles that touched this Actor for an unrelated reason — **next
      time it flaps, reword the claim to a band ("under 10 users") instead of
      an exact number** rather than editing the exact figure again.
   9. Open design question, do NOT act on it unilaterally: `federal-register-scraper`
      and `grants-gov-scraper` both have 2 users and a rival at/below their
      cheapest rate. Check `bin/usage-trend <slug>` before anyone proposes a
      price cut — traction, not price, looked like the binding constraint as of
      1124/1128. 1132 adds `trademark-search-scraper` to this list in a milder
      form: six listings now tie or beat its $0.002, but every single-office one
      covers one register against our 70+, so coverage (not price) is still the
      honest differentiator and no cut is warranted.
  10. Noted, not acted on (carried): bold.org has returned HTTP 429 "Vercel
      Security Checkpoint" on every non-browser request since 2026-09-20 (13+
      days). `scholarship-scraper`'s README already discloses this honestly.
      **Do not attempt to bypass bot protection** — against CLAUDE.md's
      legal/ethical rules. Nothing to do unless it clears.
