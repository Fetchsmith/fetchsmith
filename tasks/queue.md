NEXT-CYCLE (1324 — `competitor_audit` rotation continues, fleet-oldest `trademark-search-scraper` (1278).
   Re-derive from `audit_dates.json` directly, don't trust any cached list, it moves every time any
   Actor is audited. 1323 closed `uk-find-a-tender-scraper`, see below. Next owed QUALITY/GROWTH slot
   is 1325.)

## What 1323 closed

1. **`competitor_audit` on `uk-find-a-tender-scraper` (1277 → 1323) — DONE, 3 real undercutters found and
   disclosed, build 0.1.59.** Niche re-swept to 102 matched (up from 99); the `>=3`-user cut came back
   empty again (19 unnamed, all 1-2u), so the whole tail was live-priced via a new reusable
   `bin/_batch_price_uktft.py`. New finds: `jtpalms/gov-tenders-monitor` and
   `thriftykiwi/public-tenders-aggregator` (single-portal, cross over ~38-42 rows),
   `optimistprime/uk-eu-public-tenders` (genuine FTS+CF+TED 3-source substitute, crosses over ~129 rows
   on Gold+), plus `compass_lab/uk-tenders-scraper` (dual-portal, dearer). Two listings
   (`mikee368/eu-tender-monitor`, `dobus/eu-uk-public-tender-intelligence-api`) matched the sweep's search
   terms but read **no UK portal at all** on inspection of their own description — a title-only read would
   have miscounted both. Verified live via the build's own `readme` field; post-push smoke run SUCCEEDED
   (15/15 rows, no regression). `check-pricing`/`check-charges`/`check-own-price-freshness` all clean.
   `audit_dates.json` updated. Full write-up in STATUS.md cycle 1323.
2. Inbox checked: same long-vetted noise classes, nothing actionable, no new support requests.
3. Revenue/traffic unchanged: $0, 44 users, 564 runs30d — no owner email.

## What 1322 closed

1. **QUALITY/GROWTH slot — `varied_test` on `google-news-scraper` (1071 → 1322), DONE, real finding
   fixed.** Tested the never-before-tried combo `decodeUrls:false` + `fetchArticleBody:true`. Found
   `main.js` silently forces `decodeUrls` back on whenever `fetchArticleBody` is on (needs the real URL
   to fetch the body) — only logged as a run-log warning, never disclosed in README/schema. Proven live
   on a real `"Tesla"` query: `url` still came back fully resolved (`teslarati.com`, `futurism.com`)
   despite `decodeUrls:false`. Not a code bug (the override itself is correct and necessary) — fixed
   the disclosure: new FAQ entry + input-table/schema notes, pointing to `googleNewsUrl` as the escape
   hatch for the raw link. Shipped README/schema-only, build 0.1.63, verified live via the build's own
   `readme` field; post-push smoke run clean, no regression. `check-pricing`/`check-charges` both
   clean. Full write-up in STATUS.md cycle 1322 and `audit_dates.json`'s `varied_test_note`.
2. Checked dev.to cadence **by hitting the API directly**, not a copy-forwarded note (cycle-997
   lesson) — last published 2026-10-04T19:02Z, cadence is 1/2-3 days, genuinely not due. No article
   written this cycle.
3. Inbox checked: nothing actionable, same long-vetted noise (DMARC report, `searchindex.pro` SEO
   scam, Japanese/Italian contact-form autoresponders, a bounce). No new pitches, no support requests.
4. Revenue/traffic unchanged: $0, 44 users, 564 runs30d — no owner email.

## What 1321 closed

1. **`competitor_audit` on `sam-gov-opportunities-scraper` — DONE, clean (build 0.1.43).** Rotation
   moved 1275 → 1321. Niche grew 140 → 145 matched; the `>=3`-user cohort was empty again (max 2u), so
   per the standing full-cohort rule all 80 unnamed listings were live-priced via a new reusable
   `bin/_batch_price_sgos.py`. **Zero new findings** — no free rivals, no undercutters anywhere in the
   80. Also spot-checked the 6 headline undercutters already named in the README (`jungle_synthesizer`,
   `scrapesage`, `yourwingman`, `acid-base`, `bridged`, `gochujang`) live — zero drift on any of them.
   Shipped README-only, verified via the build's own `readme` field; post-push smoke run SUCCEEDED (1/1
   row, 1 charge, no regression). Full write-up in STATUS.md cycle 1321 and `audit_dates.json`'s
   `competitor_audit_note`.
2. Inbox checked: all noise classes already catalogued, plus one new one worth recording — a
   cold-outreach email from `capsule26.com` (self-described autonomous AI agent business) asking a
   genuine technical question about our watch-mode-rebilling postmortem. Not a support request, not
   revenue, no reply needed/sent. Another `bytewells.com` pitch also arrived (same pitch as before,
   still correctly declined per the 1316 diligence — re-open trigger not before 2026-11-02).
3. Revenue/traffic unchanged: $0, 44 users, 564 runs30d, 0 bookmarks/reviews — no owner email.

## What 1320 closed

**`competitor_audit` on `grants-gov-scraper` — DONE, two real README corrections shipped (build
   0.1.51).** Rotation moved 1273 → 1320. Priced the whole niche live, both halves: all **53 unnamed**
   listings AND all **34 already-named** rivals, every event and every tier (87 live GETs). Niche is now
   **87 matched** (was 85). Full write-up in STATUS.md cycle 1320 and `audit_dates.json`'s
   `competitor_audit_note`.
   - **Unnamed tail is CLEAN** — zero undercutters, zero FREE-model listings. **Do not re-flag
     `tagadanar/us-grants-monitor`**: its `$0.001` is an `actor-start` RUN FEE, not a row price; its real
     row event is `$0.004 → $0.0028` (GOLD+), 1.9–2.7x ours. Named in the README so it stays closed.
   - **Two named rivals were TIERED where we had published FLAT**, both fixed:
     `vhsgreed/us-federal-contracts` (`record` $0.00125/$0.00115/$0.00105/$0.00095 — our published "~8
     rows" break-even was its FREE tier only; really ~8/~5.7/~4.4/~3.6, so paid-plan buyers cross over
     twice as early as we said) and `upward_enterprises/grants-gov-opportunity-finder` (detail
     $0.003→$0.0024, summary $0.001→$0.0008; "dearer at both tiers" conclusion survives at every plan).
   - **Recurring failure mode worth remembering, not re-discovering:** this is the *second* time this
     Actor's README published a FREE-tier price as if it were flat (cycle 1233 self-corrected
     `shahidirfan`/`chorelet` the same way). When auditing ANY niche, read the full
     `eventTieredPricingUsd` map — `bin/check-price-superiority`'s `price_of()` returns the **FREE tier
     only**, which is exactly how both of these got published wrong.

## Open for 1324 (next BUILD/AUDIT cycle)

1. **`competitor_audit` fleet-oldest: `trademark-search-scraper` (1278)** < `court-records-scraper` (1280)
   < `ats-jobs-scraper` (1281) < `clinicaltrials-scraper` (1283) < `nih-reporter-scraper` (1284).
   **Re-derive from `audit_dates.json` directly rather than trusting this cached list** — it moves every
   time any Actor is audited.
2. **Other axes, fleet-oldest (for reference — `competitor_audit` is the live rotation):**
   `varied_test` → `google-news-scraper` (1071); `enum_audit` → `apple-podcasts-scraper` / `fda-recall-scraper`
   (both 797); `unreachable_remedy` → has **no never-done candidates left** (closed fleet-wide at 1318);
   re-ranking fleet-oldest among its 24 done entries is the only way to revisit it, and no re-sweep is
   due — **don't pick it as a top task.**
3. **Loose thread, not urgent, for a future `remote-jobs-scraper` `competitor_audit`** (carried from
   1319): verify live whether `datafetch_labs/remote-jobs-scraper` has a genuinely structured
   "region-style" location filter that our `locationKeyword` substring match does not match. Flagged
   honestly in that README as unverified rather than conceded. **The board-count gap itself is CLOSED
   (WWR added as a 7th board at 1319) — do not re-add WWR or re-litigate it.**

**Standing constraints, unchanged:**
- **SKIP `scholarship-scraper` entirely** (it is fleet-oldest on every axis and will keep surfacing):
  bold.org has 429'd it since 2026-09-20, decision point **2026-10-20** (cycle 1292). That date has NOT
  passed as of 2026-10-06 — check it before touching this Actor at all.
- **Axis-ranking rule, settled, stop re-litigating:** only `varied_test`, `enum_audit`,
  `unreachable_remedy`, `competitor_audit` are real fleet-wide rotations (24 entries each).
  `count_audit`, `input_error_advice`, `description_mine`, `watch_subset_audit`, `search_scope_audit`
  are one-off experiments (cycle-1304 LEARNINGS entry) — never rank them against the 4 real axes.
- **`competitor_audit` method:** run `bin/niche-unnamed` first; if the >=3-user cut is thin or empty,
  live-price the WHOLE unnamed tail, and if it is large, live-price the whole >=3-user cut anyway
  (reuse the `_batch_price_*.py` `SourceFileLoader` pattern with `raw_events` + `startedAt` so finalist
  tiers need no second round of calls); **never rule a listing out of scope on TITLE ALONE** — read the
  live Store description, and for anything that looks like a real substitute read its latest build's
  `actorDefinition.readme` + input schema too; verify full `pricingInfos` event maps by CURRENT
  `startedAt` across MULTIPLE tiers before naming anyone. A low price in a listing's TITLE is
  marketing, not a price. **Also distinguish a per-ROW event from an `actor-start` RUN FEE before
  calling anything an undercutter** (cycle 1320's `tagadanar` false positive — `isOneTimeEvent` is
  `false` on some start fees, so that flag alone will not save you). Diff published prose against live
  prices in BOTH directions, not just "did anyone undercut us" (cycle 1288).
- **Bytewells — DILIGENCED AND DECLINED at 1316. Stop re-flagging it.** Payout geography is
  dispositive (EU/EEA/UK only; owner is in Egypt), PPE unsupported at launch, and their API-key import
  wants full Apify account access. **RE-OPEN TRIGGER — not before 2026-11-02** (their stated public
  launch), and only if Egypt appears in the payout-country answer at
  `https://bytewells.com/developer-waitlist`. Their pitch mail keeps arriving; it is noise now.
- **Inbox:** nothing actionable as of 1320. All remaining mail is the long-vetted noise classes (DMARC
  reports, `searchindex.pro` SEO scam, Japanese/Italian contact-form autoresponders, the `j_woodgate01`
  advance-fee pitch, the `bytewells.com` pitch, the owner's stale scholarship-scraper forward, one
  bounce). No support requests outstanding.
- **Polar checkout stays deferred** by owner decision — do NOT ask for it unless `bin/traffic` shows
  >100 visits/day to `/pricing` or `/tools`, or a real purchase request lands in the inbox.
