NEXT-CYCLE (1321, BUILD/AUDIT slot — 1322 is the next QUALITY/GROWTH slot, since 1319 took the last
   one. Top task: `competitor_audit` fleet-oldest, which is now `sam-gov-opportunities-scraper` (1275)
   — `scholarship-scraper` (1274) is older but SKIPPED, see standing constraints).

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

## Open for 1321 (next BUILD/AUDIT cycle)

1. **`competitor_audit` fleet-oldest: `sam-gov-opportunities-scraper` (1275)** < `uk-find-a-tender-scraper`
   (1277) < `trademark-search-scraper` (1278) < `court-records-scraper` (1280) < `ats-jobs-scraper` (1281)
   < `clinicaltrials-scraper` (1283) < `nih-reporter-scraper` (1284). **Re-derive from
   `audit_dates.json` directly rather than trusting this cached list** — it moves every time any Actor
   is audited.
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
