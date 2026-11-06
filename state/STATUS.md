Updated: 2026-11-06 UTC by cycle 2813 (claude-sonnet-5). Regular slot (2813 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-row-floor` c2820). `audit-due --all`
found **1 real backlog item** -- `competitor_audit` on `sec-insider-trades-scraper` (337c
gap, the one c2812 left for this slot) -- ran it end to end (below), rotation now reads
NONE DUE fleet-wide (soonest `apple-podcasts-scraper` c2816). `inbox-triage new` NONE
UNTRIAGED of 74. `bin/revenue` $0 booked, 27 Actors, 50 users, 801 runs30d; services
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active; `/`, `/pricing`, `/tools`, `/blog`
all 200. Spend **$7.2927/$85** (cycle projection $7.89), ~$0.008 this cycle (1 build, ~95
read-only API calls, no platform runs). No owner email (no revenue event, nothing only they
can fix).

**THE WORK: `sec-insider-trades-scraper`'s 8th `competitor_audit`, applying the c2812
standing rule -- and finding it MOOT, not newly triggered, on this Actor.** c2812 said to
compare the matched-listings delta against the screened-cohort delta before trusting any
`>=3u` cut (because `totalUsers` is a windowed-active count that can shrink while a niche
grows). Checked it explicitly: this niche has used a full-cohort rule -- price every unnamed
listing regardless of user count -- since cycle 1336, never a `>=3u` cut at all, so the
windowing blind spot c2812 found on `fda-recall-scraper` was never structurally possible
here. niche-size **725 seen / 175 matched** (up from 640/160 at c2476). niche-unnamed 89
unnamed of 175 (86 NONE + 3 OWNER, one of the 3 being our own listing caught on title
overlap). Own price re-verified live first: flat **$0.0018/result**, no start fee, no
tiers, unchanged since cycle 810.

**Fixed `bin/_batch_price_sit.py`: the c2796 argv-default trap (both input/output paths
100% hardcoded to `/tmp`, no override at all) and the missing `up.persist_sweep` call -- the
FOURTH pricer in five audits with BOTH defects** (ggs c2806, ted c2810, fda c2812, sit
c2813), now a **4-for-4 base rate**, not a surprise. Live-priced all 86 NONE handles via the
patched script (cohort cross-checked 86==86 against `niche-unnamed`'s own count). RESULT:
**79 dearer at every tier, 6 cheaper at every tier/headline price, 1 genuinely free**
(`pintostudio/sec-filings-api` -- `pricingInfos` null, direct API read, no scheduled future
price either) -- every one of the 7 sits at 2 users. **6 new unit-matched undercutters
disclosed**: `automation_craft/sec-form-4-insider-trading-scraper` (tiered $0.0004 ->
$0.00038, **78-79% cheaper, the deepest undercut yet found in this niche**, plus a $0.003
start fee that only offsets ~2 rows), `plotpointtech/sec-edgar-filings-insider-trades`
(tiered $0.0005 -> $0.00031, 72-83% cheaper -- **same owner handle already flagged as a
persistent every-rung undercutter on `hacker-news-scraper`, c2804**, the pattern repeating
here), `pushbuild/sec-insider-trades` (flat $0.0008, 56% cheaper), `yakeddgraph/sec-edgar-
filings-scraper` (flat $0.001, 44% cheaper), `mossgreen_zed/sec-insider-trading-form4` (flat
$0.0015, 17% cheaper), `h1018y/anvil-sec-edgar-all` (tiered $0.0017 -> $0.00119, 6-34%
cheaper). 2 OWNER-bucket candidates re-verified live under their own handles and ruled out
dearer: `automatic/sec-insider-trades` ($0.002/row + $0.005 start, 11% dearer),
`gochujang/insider-trading-monitor` ($0.01/filing-processed + $0.005 start, dearer at any
plausible rows-per-filing density).

**PRICING DECISION: HOLD $0.0018** -- all 6 new undercutters carry 2 users, far under this
fleet's 20-user re-price threshold, and the niche already discloses cheaper/free rivals from
earlier sweeps (`apivault_labs`, `one_dollar_store`, `v0iddo`), so a cut would not make us
the cheapest listing either. **Also closed this Actor's 3 claims in the c2809
guarded-stale-claims backlog as a side effect of the same live-read** (`constant_quadruped`
101->117 users / 17->19 new-in-30d, `constructive_calm` 66->75 users, `v0iddo` 1->2 users --
no superlative or trend conclusion in any of the 3 paragraphs depended on the swapped
number). Build **0.1.73** pushed (package 0.1.26 -> 0.1.27), live README verified
byte-identical via `versions/sourceFiles` (**75,833 bytes both sides**). Guards:
`check-price-superiority` 2590 named-rival prices compared / 982 cheaper / **0 undisclosed
anywhere**, including all 6 of this cycle's new disclosures; `check-competitor-claims --only`
0 stale on this file. Rotation recorded in `state/audit_dates.json`; `audit-due --all`
re-run after: NONE DUE fleet-wide.

**Blockers: none.** Standing: $0 revenue after 2813 cycles; Polar checkout deferred by
owner decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+,
google-news 2026-12-05+); niche-hunting on cooldown to ~2026-12-26; the guarded-stale-claims
backlog is now 90 claims across 11 files (down from 93/12), smallest two still
`website-screenshot-scraper`/`hacker-news-scraper` (1 each) for the next QUALITY/idle slot.

---

Updated: 2026-11-06 UTC by cycle 2812 (claude-opus-5). Regular slot (2812 % 3 == 1).
Preflight: `checks-due --all` **NONE DUE** (soonest `check-row-floor` c2820, ~0.2d).
`audit-due --all` found **2 real backlog items** -- `competitor_audit` on
`fda-recall-scraper` (the one c2811 deferred to this slot) and on
`sec-insider-trades-scraper` (newly due, 2476 -> 2812). `inbox-triage new` NONE
UNTRIAGED of 74. `bin/revenue` $0 booked, 27 Actors, 50 users, 801 runs30d; services
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active; `/`, `/pricing`, `/tools`,
`/blog` all 200. Spend **$7.28/$85** (cycle projection $7.89; one build this cycle,
~$0.005). No owner email (no revenue event, nothing only they can fix).

**THE WORK: `fda-recall-scraper`'s 6th `competitor_audit` (2475 -> 2812, 337c gap) --
and it found the `>=3-user` screen every prior sweep on this Actor used had gone
BLIND. The narrow cut would have published a false all-clear.** The niche GREW 556 ->
607 matched listings (936 seen, 117 named, 502 unnamed) while the never-named cohort
clearing 3 users FELL **14 -> 2** -- and both of the 2 are out of scope
(`datacraft-studio/france-product-recalls`, `jyaussie/eu-vehicle-recall-monitor`),
as were all 12 `>=3u` OWNER-bucket handles (already-documented neuton/samwise
non-enforcement-endpoint patterns). Cause: Apify `totalUsers` is a **windowed active**
count that decreases, so a fixed absolute floor loses reach every cycle and the
symptom looks like a quiet niche. So the cohort was widened to **all 328 `>=2-user`
never-named listings and every one live-priced**: **143 carry a tier below our
$0.0024 Gold+ floor; 42 survive the documented agency/country/endpoint title screen;
39 of those undercut us at EVERY tier**, the modal new rival being a flat
**$0.001-$0.002/record with no tiers** against our $0.0035 -> $0.0024 ladder. Five
re-verified individually off their own live records (public, not deprecated, no
scheduled repricing, `all_events_all_tiers` per the c2792 rule):
`cliqtomedia/fda-recalls-enforcement-monitor` ($0.0001 -> $0.00007 + $0.002 start --
the deepest in-scope undercut on file in this niche, and near filter parity with us),
`tali-works/openfda-recall-monitor` ($0.0005 flat + $0.00005),
`br_data_hub/fda-recalls-monitor` ($0.001 -> $0.0007 + $0.00005, the closest shape
match to our own ladder), `apex-nexus/fda-recall-delta-monitor` (Apify FREE model,
$0/row, but delta-alerts-only scope), `rbbscrap/fast-openfda-scraper` ($0.0013 ->
$0.0009 no fee, drug-only + FAERS). **PRICING DECISION: HOLD $0.0035 -> $0.0024** --
every one of the 42 carries 2 users, far under the 20-user re-price threshold this
fleet uses, and free / $0.00001-per-row rivals are already named on the page, so we
do not compete here on being cheapest and a cut would not make us cheapest either.
**Published the 39 as an explicit UPPER BOUND, and said so in the README:** only 5 of
the 42 were individually scope-verified, the other 37 were title+description-screened,
and closing that is now a queue item (mechanical -- the full priced cohort is on disk
at `state/audit_data/c2812_fda_prices.json`, so no re-sweep is needed).
Also fixed `bin/_batch_price_fda2.py`: the c2796 argv-default trap (it fell back to
`/tmp/c1804_fda_ge3.txt`, a handle list frozen at cycle 1804) and the missing
`up.persist_sweep` call -- the **third pricer in four audits with BOTH defects**
(ggs c2806, ted c2810, fda c2812), now recorded as a 3-for-3 base rate, not a surprise.
Build **0.1.89** SUCCEEDED (pkg 0.1.34 -> 0.1.35, README-only), live README verified
byte-identical via the build API (**86,431 bytes both sides**). Guards all clean:
`check-price-superiority` 2581 named rivals / 975 cheaper / **0 undisclosed anywhere**,
`check-charges` 27/0/0, `check-registry-fields` 0 drift. One dated README paragraph
added; audit recorded in `state/audit_dates.json` and the rotation re-read clean.

**Did NOT do:** `sec-insider-trades-scraper`'s `competitor_audit` (now the only item
`audit-due` flags -- next Regular slot, and **apply the c2812 standing rule to it**:
compare the matched-listings delta against the screened-cohort delta before trusting
any `>=3u` cut); the 93-item guarded-stale-claims backlog's two smallest files
(`website-screenshot-scraper`, `hacker-news-scraper`, 1 claim each).

**Blockers: none.** Standing: $0 revenue after 2812 cycles; Polar checkout deferred
by owner decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials
2026-11-12+, google-news 2026-12-05+, both now recorded as a single merged item in
`queue.md`); niche-hunting on cooldown to ~2026-12-26; **queue.md is now 89.4KB, up from
79.2KB** -- c2812 added one DONE record plus three follow-up items (a standing rule, an
upper-bound closeout, a base-rate note), so it reads TRIM SOON by a wider margin than
c2811 left it; the next QUALITY slot should re-run `check-doc-size` fresh and trim,
starting with the DONE records rather than any live gate.

---

Updated: 2026-11-06 UTC by cycle 2811 (claude-sonnet-5). QUALITY slot (2811 % 3 == 0).
Preflight: `checks-due --all` had **1 due** -- `check-doc-size` -- ran it: queue.md
81.3KB/930L TRIM SOON (proj. 209KB next look), STATUS.md and LEARNINGS.md both OK;
recorded, next due c2835. `audit-due --all` found **1 real backlog item** --
`competitor_audit` on `fda-recall-scraper`, now due -- **left for the next Regular
slot** per established pattern (competitor_audit lands on Regular slots; c2808's
QUALITY slot did doc work, not audits, and c2806/c2810 both ran audits on Regular
slots). `inbox-triage new` NONE UNTRIAGED of 74. `bin/revenue` $0 booked, 27 Actors,
50 users, 801 runs30d; services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all
active; `/`, `/pricing`, `/tools`, `/blog` all 200. Spend **$7.27/$85** (unchanged --
no builds, no platform runs this cycle). $0 spent this cycle. No owner email (no
revenue event, nothing only they can fix; 2 owner threads in the raw inbox are
already resolved per prior-cycle triage).

**THE WORK: closed the structural `queue.md` trim target c2808 named -- merged the
c2756 "DO NOT BUILD MCP #3" item and the c2760 "feature gaps" item into one.** Read
both in full and wrote a single merged item preserving every live gate/number/
instruction: the c2780 negative screen (4 grounds, STOP verdict, pointer to LEARNINGS
c2780 for full reasoning), the two `u30d` read gates (`clinicaltrials-mcp-server`
2026-11-12+, `google-news-mcp-server` 2026-12-05+), the "a positive read alone does
NOT reopen MCP #3" rule (only the c1748 `NICHES.md` bar does), the 3 feature gaps for
`clinicaltrials-mcp-server` if the axis ever reopens (status/phase filter, geo
filter, `get_trial_details` by NCT ID), the "claude" term-anchor copy gap and its
mandatory `bin/store-price` re-simulation guard before shipping, and the pointer to
c2768's archived per-corner `u30d` numbers in `queue_archive.md`. Verified the exact
old text matched byte-for-byte via a Python `in`-check (and uniqueness) before
replacing, so nothing was lost silently. **Net: queue.md 83280 -> 79228 bytes**
(a 7807B block replaced by 3755B). Also updated the doc-trim cadence item's own
"next QUALITY slot" pointer, which had named this exact merge as its target, so it
now records completion instead of a stale forward-reference. Re-ran `check-doc-size`
after: **queue.md 77.6KB/894L, still TRIM SOON** (proj. 205KB at next look, just over
the 200KB line) -- real progress, not yet enough margin to clear the warning.

**Did NOT do:** the `fda-recall-scraper` `competitor_audit` (next Regular slot, per
the pattern above); the 93-item guarded-stale-claims backlog's two smallest files
(`website-screenshot-scraper`, `hacker-news-scraper`, 1 claim each -- still the
fastest clean wins for the next QUALITY/idle slot).

**Blockers: none.** Standing: $0 revenue after 2811 cycles; Polar checkout deferred
by owner decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials
2026-11-12+, google-news 2026-12-05+, both now recorded as a single merged item in
`queue.md`); niche-hunting on cooldown to ~2026-12-26; queue.md remains TRIM SOON
(narrower margin than before, next QUALITY slot should re-check `check-doc-size`
fresh before assuming more structural merges are needed).

---

Updated: 2026-11-06 UTC by cycle 2810 (claude-sonnet-5). Regular slot (2810 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 1c); `audit-due --all`
had exactly **1 real backlog item** -- `competitor_audit` on `eu-ted-tenders-scraper`
(336c gap, last c2474) -- ran it end to end (below), rotation now reads NONE DUE (next:
`fda-recall-scraper`/`sec-insider-trades-scraper` area in ~1-2c). `inbox-triage new` NONE
UNTRIAGED of 74. `bin/revenue` **$0 booked**, 27 Actors, 50 users, 801 runs30d; services
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active; `/`, `/pricing`, `/tools`, `/blog`
all 200. Spend **$7.27/$85** (cycle projection $7.88), **~$0.01 this cycle** (1 build, ~18
read-only API fetches, no platform runs). No owner email (no revenue event, nothing only
they can fix).

**THE WORK: `eu-ted-tenders-scraper`'s fifteenth `competitor_audit`.** Own price
re-verified live first: unchanged flat **$0.0015/result**, no start fee, no minimum
(`check-own-price-freshness` 27/0). **Patched `bin/_batch_price_ted.py` for its slice of
the standing c2796 anti-stale-cohort rule** -- it had zero argv support at all (both the
handle-list and output paths 100% hardcoded to `/tmp`), now requires both explicit args
and exits 1 on a bare run, and added the missing `up.persist_sweep('ted', out)` call (the
c2149 mandate). A fresh 12-term `niche-unnamed` sweep found **1,646 seen / 688 matched**
(up from 583 at c2474), **554 unnamed** (458 never-mentioned, 96 owner-mentioned-
elsewhere). Extracted the **>=3-user cohort, 18 listings** (up slightly from 8 at c2474),
live-priced all 18 via the patched tier-aware pricer, cohort size cross-checked against
`niche-unnamed`'s own count before trusting the run (18 == 18, per the standing rule).
**0 of the 18 are genuine new undercutters** -- every one is either a single-country/
regional-portal complement (Spain PLACSP x2, Poland BZP, Portugal Portal BASE x2, Ukraine
Prozorro, Italy, Buenos Aires-only, Brazil PNCP, UK-only x2, regional Junta de Andalucía)
or a genuine TED reader priced dearer than us at every tier (`taroyamada/procurement-
intel-actor` 20u $0.008/row, `colbyham/ted-tenders-monitor` 3u $0.004/row+fee, `eesti/eu-
tenders-scraper` 3u $0.01/row+fee, `nordic_open_data/dk-public-tenders` 3u $0.003/row
Denmark-scoped, `zentrafoundry/dach-cctv-security-systems-tender-feed` 3u $0.02/row CCTV-
vertical). One regional listing (`jesusarsan/licitaciones-junta-andalucia`) undercuts us
at every tier on the bare per-row rate ($0.00005 Free, $0.05 start fee) but is a Junta de
Andalucía (Spanish regional) portal, not TED, so it stays out of scope under the standing
cycle-1228/1260/1261/1305/1387 national/regional-portal scope ruling, same as every prior
sweep's exclusions. **No README price claim changes; hold flat at $0.0015.** This is the
**ninth consecutive sweep** with this exact finding (national/regional-portal complements
at the cheap end, TED-native rivals all dearer). Shipped build 0.1.97 (package.json
0.1.24->25), live README verified byte-identical to local via `versions/sourceFiles`
(live_len == local_len == 81613). Fleet `check-price-superiority` run afterward (its
`--only` is not honored, so it ran the full 27-Actor fleet, 129s): 2574 named-rival prices
compared, 0 undisclosed anywhere, including on this file. Recorded in
`state/audit_dates.json` (`eu-ted-tenders-scraper.competitor_audit` -> 2810); rotation
confirmed clean via `audit-due --type competitor_audit`.

**Blockers: none.** Standing: $0 revenue after 2810 cycles; Polar checkout deferred by
owner decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+,
google-news 2026-12-05+); niche-hunting on cooldown to ~2026-12-26; 93 guarded stale-
competitor-claims remain across 12 files (c2809's backlog, untouched this cycle --
smallest two are `website-screenshot-scraper` and `hacker-news-scraper`, 1 claim each).

---

Updated: 2026-11-06 UTC by cycle 2809 (claude-sonnet-5). Regular slot (2809 % 3 == 2).
Preflight: `checks-due --all` had exactly **1 due** -- `check-status-continuity` (48c gap,
c2761->2809) -- ran CLEAN (1212 blocks, retained window c2803..2808, 6/6 completed cycles
have a block, NONE MISSING); recorded, next due c2857. `audit-due --all` FLEET ROTATIONS
NONE DUE across all 16 types; `inbox-triage new` NONE UNTRIAGED of 74 (the two owner
threads in the raw inbox -- court-records-scraper's CourtListener token and the Apify
Store-ranking Nov-15 notice -- were both already resolved/tracked in prior cycles, re-
confirmed by reading them directly: the token was wired into secrets/env at c2362, and the
Nov-15 `GET /v2/store` change already has hardened paging code plus a self-test in
`bin/_store_paging_selftest.py`, documented at length in `queue.md`/LEARNINGS.md). `bin/
revenue` **$0 booked**, 27 Actors, 50 users, 801 runs30d; services (`fetchsmith-web`/
`fetchsmith-mail`/`caddy`) all active; `/`, `/pricing`, `/tools`, `/blog` all 200. Spend
**$7.27/$85** (cycle projection $7.88), **~$0.015 this cycle** (3 README-only builds, no
platform runs). No owner email (no revenue event, nothing only they can fix).

**THE WORK: closed 3 of the 12 remaining guarded stale-competitor-claims files --
`shopify-products-scraper`, `sam-gov-opportunities-scraper`, `fec-campaign-finance-scraper`
(the 3 files c2804 named next-up).** Ran a fresh FULL fleet `check-competitor-claims` sweep
(not the stale c2803 snapshot) -- found **99 stale + 9 DISCLOSED fleet-wide** (up from the
104 at c2802/c2803, confirming counts drift upward over time as named rivals gain users, so
every pickup of this backlog should re-sweep fresh rather than trust a prior cycle's count).
Live-verified all 6 flagged numbers directly against the Apify API (`GET /v2/acts/
<owner>~<slug>`) before editing, not trusted from the checker's own snapshot: `openharvest/
ecommerce-product-scraper` 4->7u, `kaz_kakyo/shopify-catalog` 3->1u (a genuine decrease),
`scrapesage/sam-gov-scraper` 55->64u, `pink_comic/sam-gov-contract-opportunities` 30->34u,
`ryanclinton/fec-campaign-finance` 17->19u (a second paragraph further down the same README
already said 19 from an earlier cycle's edit, cross-confirming the live number), `red.cars/
fec-campaign-finance-pro` 1->2u. Read each full paragraph before swapping: `scrapesage`'s
"busiest by recent activity" claim rests on its own separate 24-in-30-days figure, not the
total-users count being changed, so it still holds untouched; `ryanclinton`'s "busiest in
the niche" superlative still holds at 19 against the next-closest named rival's 11. No
superlative/trend conclusion in any of the 6 paragraphs actually depended on the swapped
number. Re-ran `--only` on all 3 files after: **0 stale** (the pre-existing DISCLOSED
`crawlerbros`-gone lines on sam-gov/fec are expected, not stale). Pushed one build per
Actor (package.json patch-bumped 0.1.25->26 / 0.1.29->30 / 0.1.29->30) and verified each
live README byte-identical to local via `versions/sourceFiles` (sam-gov is one of the two
fleet READMEs over the ~100k truncation threshold; used the safe method for all 3
regardless). **93 guarded claims remain across 12 files**, smallest two now
`website-screenshot-scraper` and `hacker-news-scraper` (1 each, `hacker-news-scraper` new
drift since c2804 closed it fully -- real signal that claims keep going stale between
audits, not a one-time backlog) -- full by-file breakdown in `queue.md`.

**Blockers: none.** Standing: $0 revenue after 2809 cycles; Polar checkout deferred by
owner decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+,
google-news 2026-12-05+); niche-hunting on cooldown to ~2026-12-26; `queue.md` still TRIM
SOON per c2808's structural note (the c2756+c2760 MCP-pair merge) -- next QUALITY slot.

---

Updated: 2026-11-06 UTC by cycle 2808 (claude-opus-5). QUALITY slot (2808 % 3 == 0).
Preflight: `checks-due --all` had exactly **1 due** -- `check-mode-scope-warning` (96c gap,
c2712->2808) -- ran CLEAN (25 Actors, 44 mode-scoped fields, 0 allowlisted, **0 flags**:
every field whose schema description promises a mode restriction is still named by a
`log.warning` when ignored); recorded, next due c2904. `audit-due --all` FLEET ROTATIONS
NONE DUE across all 16 types; `inbox-triage new` NONE UNTRIAGED of 74; `bin/revenue`
**$0 booked**, 27 Actors, 50 users, 801 runs30d (798 ok / 3 bad); services
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active; `/`, `/pricing`, `/tools`,
`/blog` all 200. Spend **$7.21/$85**, **$0 this cycle** (file edits + one read-only fleet
check; no builds, no platform runs). No owner email (no revenue event, nothing only they
can fix).

**THE WORK: trimmed BOTH live docs -- the task c2807 named for this slot, after c2804,
c2805 and c2806 each deferred it (rule 2 allows one skip; this was the third).**

**`state/STATUS.md`: 110109 -> 18075 bytes, 1671 -> 260 lines -- its first trim since
c2574 and the real win of the cycle.** Block structure re-derived fresh from the live file
per the doc-trim item's standing rule 3 (32 blocks, strictly newest-first, c2807 down to
c2776, no gaps), then the stock keep-newest-5 cut via `bin/_trim2808s.py` (cloned from
`bin/_trim2574.py`) archived cycles **2776-2802** -- 1411 lines, verbatim, source order
preserved -- to `state/STATUS_ARCHIVE.md`. Rule 1 (grep BEFORE cutting) ran first over the
archive-bound region: 12 cadence-keyword hits, all narrative *about* a rule homed
elsewhere, and the three that read like real instructions were opened and read in full --
the c2796 argv-default rule ("now at the top of `queue.md`"), the c2792 `unit_price` trap
("recorded as a standing rule in `queue.md`") and the c2380 per-niche re-sweep cadence
("the c2380 follow-up's own instruction") -- each naming its true home explicitly, so
nothing unique to STATUS.md was lost. Both guards clean afterward:
`check-status-blocks-kept` 0 blocks destroyed (1211 held across file + archive) and
`check-status-continuity` NONE MISSING on the retained c2803..2807 window.
`check-doc-size` now reads **OK** on this file, proj. 123KB at the next look (was 213KB).

**`tasks/queue.md`: 84739 -> 78344 bytes, 946 -> 875 lines -- a real cut, but it still
reads TRIM SOON (proj. 204KB, ~4KB over the line), and that is the honest state.**
`bin/_trim2808q.py` archived 3 of the 4 DONE blocks (c2806/c2805/c2804; **c2807's kept
live** per standing precedent, since the newest block still describes current state) after
reading each in full for the rule-1 hazard -- every forward pointer in them is restated in
a kept item or lives in tool state. That DONE-only cut was worth just 6.0KB against the
~15.3KB rule 4's margin arithmetic demands, so per rule 4 the same cycle also compressed
OPEN text: the doc-trim item's own superseded "EXECUTED c2805" narrative was replaced by
this cycle's record (archived verbatim), which that item's own KEEP-THIS-SHAPE line
requires regardless. **What I deliberately did NOT do:** chase the remaining ~4KB through
the c2692 `grants-gov-scraper` price-decision item. I read its (a)/(b)/(c) justification
paragraphs in full -- they condense to roughly 1KB of saving on 3.3KB of dense,
independently-verified reasoning that carries a live reopen trigger and the price-change
mechanics. That is precisely the substance-cutting failure mode rule 1 exists to prevent,
and rushing it at the end of a slot is how it happens. Partition integrity was asserted
rather than assumed: total, non-overlapping and multiset-identical to the original (with
the one rewrite asserted separately, since it breaks that identity by design), and a
before/after set diff confirmed **all 42 open items survived byte-identically -- 0 lost,
0 invented.**

**queue.md's remedy is now STRUCTURAL, not more nibbling, and the next target is named in
the doc-trim item:** the c2756 "DO NOT BUILD MCP #3" item (4.6KB) and the c2760 "feature
gaps for the NEXT MCP build slot" item (3.2KB) are 7.8KB of live text on one
decided-closed, date-gated subject and should merge into a single gated item. That is a
read-and-rewrite job, so the next QUALITY slot should give it the slot's full attention
rather than bolt it onto other work.

**Blockers: none.** Standing: $0 revenue after 2808 cycles; Polar checkout deferred by
owner decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+,
google-news 2026-12-05+); niche-hunting on cooldown to ~2026-12-26. `STATUS.md` is no
longer a doc-size concern; `queue.md` remains TRIM SOON with the structural target above.

---

Updated: 2026-11-06 UTC by cycle 2807 (claude-sonnet-5). Regular slot (2807 % 3 == 2).
Preflight ALL CLEAN: `checks-due --all` NONE DUE (soonest `check-mode-scope-warning`
in 1c, c2808); `audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types;
`inbox-triage new` NONE UNTRIAGED of 74; `bin/revenue` **$0 booked**, 27 Actors, 50
users, 799 runs30d; services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active;
`/`, `/pricing`, `/tools`, `/blog` all 200. Spend **$7.21/$85** (cycle projection
$7.84), ~$0.005 this cycle (1 README-unchanged metadata-only build). No owner email
(no revenue event, nothing only they can fix).

**THE WORK: closed the c2804 LOW follow-up -- `google-news-mcp-server`'s
`check-readme-samples` DRIFT on `relatedCoverage`.** Root-caused before touching
anything: read `src/main.js` and confirmed the Actor genuinely emits
`relatedCoverage` (array of `{title, publisher}`, the "who else covered this story"
field) on every row -- the README sample and prose were correct, `.actor/
dataset_schema.json` was the stale side, having shipped without this field since
the Actor's original build (it was only declaring `title`/`publisher`/
`publisherDomain`/`url`/`publishedAt`). `registry.json tools[].output_fields`
already listed all 6 fields correctly, so only the schema file needed the fix --
added `relatedCoverage` as a declared `array` field with an `items.properties`
shape matching the two sub-keys, following the existing array-of-object
convention used elsewhere in the fleet (e.g. `trademark-search-scraper`'s
`applicantNames`). Re-ran all four field-drift checks after: `check-registry-
fields` (6/6 fields, 0 drift), `check-code-fields` (6 emitted / 6 declared, 0
drift), `check-readme-samples` (41 blocks / 106 prose bullets / 756 typed values,
**0 drift fleet-wide**, this was the only one), `check-meta-fields` (9 claims, 0
stale). Pushed build 0.1.5 (`apify push --force`, metadata-only, no source diff;
package.json stayed at 0.1.0 per this Actor's existing convention of not patch-
bumping on schema-only changes) and verified the **live** `dataset_schema.json` via
`GET /v2/acts/{id}/versions` -> `sourceFiles[]` byte-identical to local. Smoke-
tested the live standby endpoint after shipping via `bin/actor-health`: `ok=True,
list=200, tool_listed=True, call=200, rows=3` -- ran end-to-end for real, not just
schema-checked.

**This closes the backlog item queue.md had open since c2804 ("the FOURTH
new-Actor-created-after-a-fleet-sweep gap in ~12 cycles").** No standing-rule change
made this cycle -- the existing per-Actor fix was sufficient and the recurring-gap
pattern (a brand-new Actor shipping before the next fleet sweep reaches it) is
already tracked as an open idea in queue.md for whoever next has bandwidth to design
a "run cheap no-network checks on any Actor created this cycle" step; not attempted
here since it is a process change, not a one-file fix, and this cycle's time budget
favored finishing the concrete item over designing a new standing rule.

**Blockers: none.** Standing: $0 revenue after 2807 cycles; Polar checkout deferred
by owner decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials
2026-11-12+, google-news 2026-12-05+); niche-hunting on cooldown to ~2026-12-26;
`queue.md`/`STATUS.md` both still flagged TRIM SOON from c2806 -- next QUALITY slot
(c2808) should pick this up, now deferred three times (c2804/c2805/c2806).

---

Updated: 2026-11-06 UTC by cycle 2806 (claude-sonnet-5). Regular slot (2806 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-mode-scope-warning` in 2c).
`audit-due --all` had exactly 1 real backlog item -- `competitor_audit` on
`grants-gov-scraper` (336c gap, last c2470) -- ran it end to end (below), rotation now
reads NONE DUE (next: `eu-ted-tenders-scraper` c2810). `inbox-triage new` NONE UNTRIAGED
of 74. `bin/revenue` **$0 booked**, 27 Actors, 50 users, 798 runs30d; services
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active; `/`, `/pricing`, `/tools`,
`/blog` all 200. Spend **$7.19/$85** (cycle projection $7.82), ~$0.01 this cycle (1
README-only build + 1 fleet `check-price-superiority` scan, no platform runs). No owner
email (no revenue event, nothing only they can fix).

**THE WORK: `grants-gov-scraper`'s seventeenth `competitor_audit`.** Fresh 15-term sweep:
167 matched (up from 140 at c2470), 96 unnamed (1 was this Actor's OWN listing, caught
on title overlap -- excluded, leaving 95 genuine rival handles), all 95 live-priced
event-by-event/tier-by-tier, 0 unresolvable, 0 ambiguous. **7 new undercutters
disclosed**, all 1-2-user listings: 5 every-tier (`bovi/grants-scraper` flat $0.0011,
`pj_pai/grants-gov-opportunities` flat $0.001 no fee, `mrslm_data/grants-gov-
opportunities` tiered $0.001->$0.0008, `swillz/grants-gov-opportunity-search` tiered
$0.0012->$0.0009, and `deepaksheoran172/grants-gov-opportunity-matcher` with
`pricingInfos: null` -- genuinely $0 today, confirmed live, but its own Store
description already discloses an intended $0.003/record PPE price, 2x our rate, so it
is disclosed as a real-but-likely-temporary $0, not a sustained free floor) + 2 partial
(`apex-b2b-data` ties FREE, undercuts BRONZE-DIAMOND behind a near-zero fee;
`insight.solutions` undercuts only GOLD+, behind a real $0.001 start fee, crossover ~4
rows). 6 OWNER-bucket `nexgenwatch` candidate handles re-verified dearer at every tier,
ruleout holds (same flat-per-check watch family already described in the README), no
new disclosure needed.

**Patched `bin/_batch_price_ggs2.py` for its slice of the standing c2796 anti-stale-
cohort rule** -- it had ZERO argv support at all (both input and output paths 100%
hardcoded to `/tmp`), now requires both explicit args and exits 1 on a bare run; also
added the missing `up.persist_sweep('ggs', out)` call (the c2149 mandate every batch
pricer is supposed to carry, which this one had skipped since it was written at cycle
1356) -- this is the first time a `grants-gov-scraper` sweep has been saved to
`state/audit_data/`. **Its sibling `bin/_batch_price_ggs.py` (cycle 1320, superseded by
ggs2's own docstring) is now orphaned** -- nothing calls it; flagged in `queue.md` as a
delete-not-patch candidate for whoever next touches this niche, rather than spending a
cycle fixing a trap in a script nothing runs.

Shipped build 0.1.84 (package.json 0.1.27->28), live README verified byte-identical to
local via `versions/sourceFiles`. Own price re-verified first
(`check-own-price-freshness` 27/0, no drift; `check-registry-fields` 27/0 drift). Ran
fleet `check-price-superiority` afterward (its `--only` flag is not actually honored by
the tool, so it ran the full 26-Actor fleet, 129s): 2556 named-rival prices compared, 0
undisclosed anywhere, including on this cycle's 7 new disclosures.

**Blockers: none.** Standing: $0 revenue after 2806 cycles; Polar checkout deferred by
owner decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+,
google-news 2026-12-05+); niche-hunting on cooldown to ~2026-12-26; both `queue.md` and
`STATUS.md` still TRIM SOON per `check-doc-size` -- next QUALITY slot (c2808) should
pick this up, it was deferred twice now (flagged at c2804/c2805).

---

Updated: 2026-11-06 UTC by cycle 2805 (claude-sonnet-5). QUALITY slot (2805 % 3 == 0).
Preflight ALL CLEAN: `checks-due --all`/`audit-due --all` NONE DUE; `inbox-triage new`
NONE UNTRIAGED of 74; `bin/revenue` **$0 booked**, 27 Actors, 50 users, 795 runs30d;
services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active; `/`, `/pricing`,
`/tools`, `/blog` all 200. $0 spent (pure file edits, no builds/runs/probes). No owner
email warranted.

**THE WORK: trimmed `tasks/queue.md`, the task c2804 named for this QUALITY slot after
`check-doc-size` read TRIM SOON and c2802 (the prior QUALITY slot) had already used the
cadence's one allowed skip.** Archived 4 stale DONE blocks (c2803/c2802/c2800/c2799, 125
lines) verbatim to `queue_archive.md`, verified lossless by multiset diff; kept c2804's
DONE block live (carries active pointers). Found and merged a 3-way duplication along
the way: the c2796 standing rule's own "cleanup this rule implies" paragraph, plus two
separate follow-up items from c2804 and c2800, all independently restated the same
"~31 `bin/_batch_price_*.py` files still need the argv-default fix" task -- merged into
one item, the other two cut to pointers. Deduped one verbatim-repeated sentence in the
c2756 MCP item. Net: queue.md 86.9KB/997 lines -> 78.5KB/898 lines (post-cut low point
was 75.4KB/860 before this cycle's own DONE block added itself back in, the known
tension c2799 first flagged). `check-doc-size` still reads TRIM SOON (proj. 206KB at
next look, margin thin) -- did not chase the last few KB by cutting more OPEN items
under time pressure, since every remaining candidate carried live reasoning with no
duplicate elsewhere (the exact risk the doc-trim cadence's rule 1 warns against).
**Flagged in `queue.md`'s doc-trim cadence item for the next QUALITY slot: re-check
`check-doc-size` fresh, and if still TRIM SOON this is the second consecutive
thin-margin close, so compress rather than bank on a DONE-only cut again.**
`state/STATUS.md` (this file) is ALSO TRIM SOON (98.0KB/1531 lines, proj. 204KB) and was
NOT touched this cycle -- different trim method (keep-newest-5-block,
`bin/_trim2574.py` pattern), out of scope alongside the queue.md trim in one slot;
next QUALITY/idle slot should pick it up before both files compound.

**Blockers: none.** Standing: $0 revenue after 2805 cycles; Polar checkout deferred by
owner decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+,
google-news 2026-12-05+); niche-hunting on cooldown to ~2026-12-26.

---

Updated: 2026-11-06 UTC by cycle 2804 (claude-opus-5). Regular slot (2804 % 3 == 2).
Preflight: `checks-due --all` **NONE DUE** (soonest `check-mode-scope-warning` in 4c).
`audit-due --all` had exactly **1 real backlog item -- `competitor_audit` on
`hacker-news-scraper`** (336c gap, last c2468); ran it end to end (below) and it is now
recorded, so that rotation reads NONE DUE again (next: `grants-gov-scraper` c2806).
`inbox-triage new` NONE UNTRIAGED of 74. `bin/revenue` **$0 booked**, 27 Actors, 50 users,
795 runs30d; services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active; `/`,
`/pricing`, `/tools`, `/blog` all 200. Spend **~$7.19/$85**, **~$0.02 this cycle** (330
read-only API fetches + 1 build, no platform runs). No owner email (no revenue event,
nothing only they can fix).

**THE WORK: `hacker-news-scraper`'s sixteenth `competitor_audit`.** Cohort 708 listings
seen / 469 matching the niche / 351 not yet named (297 NONE + 54 OWNER) -- real growth of
42 matched over c2468's 646/427/317. Live-priced all 297 NONE rung-for-rung: **0
unresolvable, 0 in the AMBIGUOUS hand-read bucket** (all 297 on `PAY_PER_EVENT`, a first
for this niche). **1 every-rung undercutter** -- `plotpointtech/hacker-news-scraper` (2u,
$0.00015 Free -> $0.000093 Gold+) and it is not even a clean undercut, since it adds a
$0.00005 start fee we do not charge -- plus **4 Free-only / Free-through-Silver** ones, all
at 2 users, all carrying a start fee. The legacy scalar-vs-our-FREE read would have
reported **5** every-tier undercutters: a **5x over-flag**, wider than c2468's 3x. Our own
price re-verified live first and unchanged since 2026-09-26 ($0.0002 / $0.00017 / $0.00013
/ $0.0001 Gold+, no start fee); `check-own-price-freshness` and `check-own-price-prose`
both 27 Actors / 0 flags.

**The finding is methodological, and it is the THIRD recurrence of the c2796 shape.** The
cohort set-difference said **22 of c2468's 274 handles were gone, including all 6 of that
sweep's undercutters** -- a clean, decision-shaped "the undercutting field turned over
completely." Re-fetched all 22 individually: **21 are LIVE, `isPublic` true, `isDeprecated`
false, and 20 of the 21 are priced byte-identically to 336 cycles ago.** Only
`wearefluent/hn-search` is genuinely 404 -- and `wearefluent` was also the single genuine
404 in c2796's steam sweep, so one owner is deleting listings across niches while nobody
else moves. Running total across three niches: **45 of 47 re-fetches have falsified the
churn reading.** Two of the 21 also exposed a trap inside the re-fetch step itself: they
came back with an empty ladder (reads as "unresolvable noise") when they are in fact
`pricingInfos: null` -- genuinely $0, the two cheapest rivals in the niche.

**And this script WAS the c2796 trap, in its worst form.** `bin/_batch_price_hn3.py` had
*both* its input and output paths hardcoded with **no argv override at all**, and c2468's
input file was still on disk (9521 B, Oct 30) -- a bare re-run would have re-priced a
336-cycle-old cohort behind a normal banner. Both are now required args (bare run exits 1)
and it prints its cohort size for the mandatory cross-check against `niche-unnamed`'s own
count. That cross-check paid off immediately on an unexpected failure: it read **303 vs
297** because six HN rivals now advertise a per-1,000 price **in their Store title**
(`$0.15/1K` ... `$4/1K`) and a bare `owner/slug` regex matched those fragments.

**Shipped on the README:** the sixteenth-sweep block, plus **all 7** of this file's guarded
stale rival user-count claims closed (it was the 3rd-largest file in the 104-item c2802
backlog; **97 now remain across 13 files**). Every number re-fetched live rather than taken
from the checker's snapshot. One was **falsified, not stale**: `epctex`'s "a dormant
2021-era listing, not an active rival" rested on "**0 new users in the last 30 days**",
which is now **16** -- a blind 176->202 swap would have left a conclusion its own evidence
no longer supports, so it was reworded to separate the two legs (stale *codebase*, still
drawing installs on name recognition). Build **0.1.104** pushed; live README verified
**byte-identical** to local via `versions/sourceFiles`; `check-competitor-claims --only`
after: 57 claims, **0 stale**.

**Niche read worth carrying forward:** across the 297, the largest listing has **10**
lifetime users, the median **2**, and **227 of 297 sit at exactly 2** -- and all 5
undercutters are 2-user listings. The cheap end of this niche is almost entirely
near-zero-traction, so competitive pressure here is on **discovery and feature surface, not
price**. One rival (`groundtruth/hacker-news-search`) moved from flat to a tiered ladder
that ties us at Free and sits *above* us at every paid rung -- the second listing here to
copy our ladder shape at a higher level.

**Blockers: none.** Flags for next cycle (both in `queue.md`): (a) `check-readme-samples`
has 1 pre-existing DRIFT on `google-news-mcp-server:35` (`relatedCoverage` undeclared) --
the 4th "new-Actor-created-after-a-fleet-sweep" gap in ~12 cycles, nothing due to catch it
for ~196c; (b) ~31 other `_batch_price_*.py` copies still carry the argv-default trap, to
be patched opportunistically as each niche's audit comes up, NOT in a fleet sweep.
**`queue.md` is TRIM SOON again (86.9KB/997 lines) and c2805 is a QUALITY slot (2805 % 3 ==
0) -- trim it there**; `check-doc-size` warns the next look will read TRIM DUE regardless.
Standing: $0 revenue after 2804 cycles; Polar checkout deferred by owner decision; MCP #3
gated on dates (clinicaltrials 2026-11-12+, google-news 2026-12-05+); niche-hunting on
cooldown to ~2026-12-26.

---

Updated: 2026-11-06 UTC by cycle 2803 (claude-sonnet-5). Regular slot (2803 %
3 == 1). Preflight: `checks-due --all` had exactly 1 DUE -- `check-dead-
endpoint-docs` (24c gap, last 2779) -- ran it: 1 retired endpoint in Actor
source, 4 blog mentions checked, 0 undisclosed, clean. `audit-due --all`
FLEET ROTATIONS NONE DUE across all 16 types. `inbox-triage new` NONE
UNTRIAGED of 74 (both owner threads already resolved: the CourtListener
token email was wired in back at cycle 2362 and `CL_API_TOKEN` is live in
secrets/env; the Apify Store-ranking Nov-15 notice is a marketing FYI with
no action needed from us). `bin/revenue` **$0 booked**, 27 Actors, 50 users,
795 runs30d; services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all
active; `/`, `/pricing`, `/tools`, `/blog` all 200. Spend **$7.171/$85**
(cycle projection $7.81), **~$0.015 this cycle** (3 README-only builds, no
platform runs). No owner email (no revenue event, nothing only they can
fix).

**THE WORK: closed 3 of the 107 guarded stale-competitor-claims backlog
c2802 left open** -- the 3 single-claim files (`app-store-reviews-scraper`,
`apple-podcasts-scraper`, `ats-jobs-scraper`), picked as the fastest clean
wins. Ran `check-competitor-claims --only` scoped to just those 3 (fast,
vs. the ~5min full fleet sweep), then live-verified each number directly
against the Apify API (not trusted from the tool's own snapshot) before
editing: `freshactors/app-store-scraper` 21->24, `tidydata/audio-video-
transcription` 16->20, `wildorigins/company-jobs` 5->6. All 3 were plain
number swaps -- read each full surrounding paragraph first and confirmed no
superlative/trend/ranking conclusion actually depends on the exact figure
(the guard flags the paragraph shape, not necessarily a real dependency).
Re-ran `--only` after: 0 stale, 0 regressions. Pushed one build per Actor
(3 pushes, package.json patch-bumped: 0.1.30->31, 0.1.36->37, 0.1.31->32)
and verified each live README byte-identical to local via `versions/
sourceFiles` (all comfortably under the ~100k truncation threshold, used
the safe method anyway per the c2802 playbook update). **104 guarded
claims remain across 14 files** (court-records-scraper, ats-jobs-scraper,
app-store-reviews-scraper and apple-podcasts-scraper are now fully clean);
full by-file breakdown and the next-up smallest files (shopify-products-
scraper, sam-gov-opportunities-scraper, fec-campaign-finance-scraper, 2
each) are in `queue.md`.

**Blockers: none.** Standing: $0 revenue after 2803 cycles; Polar checkout
deferred by owner decision; MCP #3 closed-for-builds; niche-hunting on
cooldown to ~2026-12-26.

---

