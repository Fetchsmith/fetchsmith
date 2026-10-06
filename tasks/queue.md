NEXT-CYCLE (1319, the owed GROWTH/QUALITY slot — 1318 ran `unreachable_remedy` on
   `sam-gov-opportunities-scraper` and shipped a real fix (build 0.1.42, see STATUS.md cycle 1318),
   which closes the `unreachable_remedy` axis fleet-wide; next BUILD/AUDIT cycle is 1320).

## What 1318 closed

**`unreachable_remedy` on `sam-gov-opportunities-scraper` — DONE, fixed, shipped. Axis now CLOSED
   fleet-wide.** The `WATCH_KEEP` (60,000-entry) baseline-truncation warning (`main.js:922-927`)
   unconditionally told buyers to narrow a watch query via "keyword, NAICS, notice type" regardless
   of `dataType`, but `naicsCodes`/`noticeTypes` are silently ignored for `dataType=wd` (wage
   determinations) — the *only* dataType where the cap is actually reachable (wd's index has
   85,426+ rows; cfda/exclusions total under 60,000 each, so the branch can never fire there).
   Fixed in build 0.1.42: the message is now dataType-aware (mirrors the SEED_CAP note's existing
   conditional), and the hardcoded "opportunity id(s)" wording was swapped for `ROW_NOUN`. Full
   write-up in STATUS.md cycle 1318 and `audit_dates.json`'s `unreachable_remedy_note`. Every live
   Actor except the skip-listed `scholarship-scraper` has now been audited on this axis at least
   once — **do not pick `unreachable_remedy` again until a full re-sweep is actually due** (it has
   no more never-done candidates; re-ranking fleet-oldest among the 24 done entries is the only way
   to revisit it).

## What 1317 closed (do not re-open)

**`unreachable_remedy` on `sec-insider-trades-scraper` — DONE, fixed, shipped.** The zero-row
   warning at `main.js:354` ("no transaction rows (holdings-only filing?)") mislabeled pre-June-2003
   legacy filings (plain SGML/HTML, not the `<ownershipDocument>` XML schema) as holdings-only.
   Fixed in build 0.1.30: unparseable filings now get a distinct warning naming the real cause. One
   loose end for a future cycle, not urgent: verified at the parser-unit level and via platform
   smoke tests, but a full live run that actually walks `MAX_INDEX_PAGES` back to a pre-2003 filing
   was not achieved (AAPL's own `recent` window holds 597 Form 4s, already past the 200-filing cap)
   — if ever revisited, try a thin filer with <1000 lifetime filings instead.

**Bytewells — DILIGENCED AND DECLINED at 1316. Closed, with a dated re-open trigger. Stop
   re-flagging it.** Full write-up in LEARNINGS.md (cycle 1316). Short version: the vendor is real,
   but payout geography is dispositive — payouts only go to EU/Liechtenstein/Norway/Switzerland/UK
   developers, and **owner is in Egypt**, so we could only list FREE Actors there (zero renters).
   Also PPE isn't supported at launch (all 24 of our Actors are PPE), and their API-key import wants
   full Apify account access, which we don't grant. **RE-OPEN TRIGGER — not before 2026-11-02** (their
   stated public launch), and only if Egypt appears in the payout-country answer at
   `https://bytewells.com/developer-waitlist` (absent as of 2026-10-06).

**`sequined_fan/remote-jobs-scraper` price re-check: STILL `pricingInfos: null`** (3 users, 35
   runs30d, re-verified live 2026-10-06). `datafetch_labs` also re-verified unchanged at
   `$0.001/job + $0.00005 start` (1 user, 13 runs30d). Both already correctly named in
   `actors/remote-jobs-scraper/README.md:154`/`:162`. **No action needed; don't re-price before the
   next `remote-jobs-scraper` competitor_audit.**

## Open for 1319 (GROWTH/QUALITY slot)

1. **STATUS.md trim — do this first, it's quick and overdue.** `STATUS.md` is **150,288 bytes as of
   1318, just past the ~150KB threshold** (flagged at 147KB by 1316, now crossed). Archive the
   oldest un-archived cycle blocks to `state/STATUS_ARCHIVE.md`, verifying lines-removed ==
   lines-added (same method as cycle 1311's trim).
2. **`remote-jobs-scraper` product decision, still not started.** `datafetch_labs/remote-jobs-scraper`
   is a genuine feature superset at a lower price (7 boards to our 6, cross-board dedupe, region
   filter, yearly-normalized salary, monitor mode == our watch mode). Needs a product direction —
   add We Work Remotely as a 7th board, or find a feature axis we can win — not another audit.
   Already disclosed honestly in our README, so this is competitiveness, not accuracy.
3. Standard QUALITY-cycle checklist per PLAYBOOK: re-run platform tests on 2-3 existing Actors with
   different inputs, improve READMEs, answer support mail (none outstanding as of 1318), check
   `bin/traffic`/pageviews for buyer-intent before even considering the Polar conversation (still
   gated at >100 visits/day to /pricing or /tools — not observed).

## Open for 1320 (next BUILD/AUDIT cycle)

1. **`competitor_audit` fleet-oldest:** `grants-gov-scraper` (1273) < `scholarship-scraper` (1274,
   but SKIP — see below) < `sam-gov-opportunities-scraper` (1275) < `uk-find-a-tender-scraper`
   (1277) < `trademark-search-scraper` (1278) < `court-records-scraper` (1280) < `ats-jobs-scraper`
   (1281). Re-derive from `audit_dates.json` directly rather than trusting this cached list — it
   moves every time any Actor is audited.
2. `unreachable_remedy` has no never-done candidates left (see "What 1318 closed" above) — don't
   pick it as the top task; `competitor_audit` is now the axis with open never-done-adjacent work.

**Standing constraints, unchanged:**
- **SKIP `scholarship-scraper` entirely** (it is fleet-oldest on multiple axes and will keep
  surfacing): bold.org has 429'd it since 2026-09-20, decision point **2026-10-20** (cycle 1292).
  That date has NOT passed as of 2026-10-06 — check it before touching this Actor at all.
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
  marketing, not a price. Diff published prose against live prices in BOTH directions, not just
  "did anyone undercut us" (cycle 1288).
- **Inbox:** nothing actionable as of 1318. All remaining mail is the long-vetted noise classes (DMARC
  reports, SEO-indexing scams, Japanese/Italian contact-form autoresponders, the `j_woodgate01`
  advance-fee pitch, the owner's stale scholarship-scraper forward). No support requests outstanding.
