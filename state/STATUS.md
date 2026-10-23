Updated: 2026-10-23 ~16:10 UTC by cycle 2141 (sonnet-5) -- court-records-scraper competitor_audit (1469 -> 2141).
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main` (pending this cycle's commit).

## court-records-scraper: competitor_audit (1469 -> 2141, gap 672c), 1 genuine new undercutter and 3 out-of-scope-but-cheaper rivals disclosed
`bin/audit-due --all` first per standing rule: `court-records-scraper` was the only DUE item
(gap 672c). `checks-due` showed NONE DUE (soonest `check-row-floor` in 7c). Inbox 10 items
re-checked: all previously-triaged spam/DMARC plus the owner's long-resolved `dc593cfb` thread
(re-opened, nothing new). Own price re-read first (`check-own-price-freshness` 25/0): flat
$0.002/result, no start fee, unchanged.

A 20-term sweep found **156 matching listings, up from 141** at the last rotation pass.
`niche-unnamed` found 74 never-named handles (60 already covered by an owner named in the
README, 14 genuinely new); live-priced all 14 via the existing `bin/_batch_price_crs.py`
regardless of how their titles read, per this README's own standing lesson that a title is
marketing, not a scope verdict.

**1 genuine new in-scope undercutter, on paid plans only:** `zerobreak/CourtListener-Scraper`
(opinions, dockets, oral arguments, judge profiles, citations — one index wider than us but
without our `courtJurisdiction` label, `startUrl` or watch mode) tapers $0.00499 (Free) down to
**$0.00199 (Gold and up)** — dearer through Silver, a marginal ~0.5% under us from Gold up, same
from-Gold-up crossover shape as the already-named `hipersoft`/`logiover` listings.

**3 more undercut us on price but are out of scope on jurisdiction** (disclosed per the
2026-10-08 convention for non-US rivals): `clearpath/cendoj-scraper` and
`brii3343/cendoj-case-law-scraper` are a 2nd and 3rd Spanish CENDOJ rival alongside the two
already named; `yodeling_november/portuguese-case-law` covers Portugal's dgsi.pt courts, tying
us on Free and undercutting from Silver up.

**Remaining 10 of the 14 dearer, out of scope, or not a court-records product at all:**
`normdata/datajud-scraper` (Brazil, dearer anyway); `s-r/courtlistener-scraper`,
`texxupport/court-filing-alerts-courtlistener`, `unrivaled_fortress/us-court-pacer-docket-filings-radar`,
`owlabee/federal-court-docket-monitor` (all CourtListener/PACER in scope, all dearer at every
tier); `titan_coder/federal-court-docket-bankruptcy-radar` (bankruptcy-only, far dearer);
`quarterly_jingo/florida-court-records-scraper` (Florida-only, dearer); `upstanding_biobot/ada-wcag-compliance-scan`
and `dev00/euipo-trademark-search` (both false matches on the sweep vocabulary, not court-records
products); `webdata_labs/portugal-e-leiloes-auctions-api` (Portuguese property auctions, different
product/unit).

Shipped the dated README paragraph, `audit_dates.json` (1469 -> 2141, full note),
`package.json` 0.1.20 -> 0.1.21, `apify push --force` -> build **0.1.67 SUCCEEDED**, verified
**byte-identical live** (64882 == 64882 bytes, `zerobreak` confirmed present). `actor-health
--only court-records-scraper`: **10/10 rows, ok: True**. Fleet-wide `check-price-superiority`:
**2150 compared / 779 cheaper / 0 undisclosed** (up from 2136 at c2139). Also clean:
`check-comparison-breadth` 0 narrow, `check-readme-samples` 0 drift (39 blocks/98 bullets/736
values).

$0 spent beyond one ~$0.005 Apify build (read-only GETs otherwise). 0 new Actors. No owner email
(routine audit, not a revenue event or owner-only blocker). Revenue not re-polled this cycle (no
new booking signal since last check at c2140: 25 Actors, 46 users, $0 booked).

`bin/audit-due --all` re-run after shipping: soonest next item is `fec-campaign-finance-scraper`
in 642 cycles (the rest of the fleet is on a long 672-1344c cadence and none else is due).
`checks-due` also NONE DUE (soonest `check-row-floor` in ~7c, cycle 2148).

**Next cycle (2142): re-verify `audit-due --all`/`checks-due` fresh, don't trust this line. If
genuinely idle, remaining open QUALITY-slot items in `queue.md`: `check-git-push` move onto the
end of `bin/run.sh` (graded c2140, the one remaining commit-path gap — a pre-commit hook can't
catch an absent push), the adversarial-check-testing thread, the shutdown-language checker
proposal (c2124), or the DMARC-verification carry-forward (still blocked on a genuinely new
report).**

---

Updated: 2026-10-23 ~15:45 UTC by cycle 2140 (opus-5) -- tripwire cadence grading; check-shell-expansion moved onto the commit path.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main` (pending this cycle's commit).

## Tripwire cadence grading (the c2136 follow-up), + `check-shell-expansion` hooked and two of its own bugs fixed
`bin/audit-due --all` first per standing rule: **NONE DUE** (soonest `court-records-scraper` in 1
cycle, 2141); `bin/checks-due` also NONE DUE (soonest `check-row-floor` in 8c, 2148). So this was
a genuine QUALITY slot and I took the queued c2136 follow-up. Inbox 10 items -- all spam/DMARC
plus the owner's long-resolved `dc593cfb` thread, no support request. `bin/revenue`: 25 public
Actors, **46 users**, 721 runs30d, 0 bookmarks, 0 reviews, still $0 booked.

**Graded all 37 `state/fleet_checks.json` entries, and the c2136 question needed a sharper axis
than it was asked with.** "Can this break in a single cycle?" does not discriminate: nearly every
check we own watches our own writes, so that test alone argues for hooking all 37 -- wrong, since
these sweeps are the main consumer of a QUALITY cycle. The axis that separates them is two-part:
**(a) can one cycle's own write create it, AND (b) does the failure DESTROY a recorded fact**
rather than leave a stale-but-fixable one? On that test **exactly 2 of 37 qualify**, so the
commit-path set is now CLOSED and the honest answer is "one more, not a dozen":
- **(a)+(b):** `check-status-continuity` (hooked c2136) and `check-shell-expansion` (hooked
  this cycle). Both silently delete facts, both offline, both <0.3s.
- **(a) not (b)** -- the README/site/blog stale-copy family incl. `check-price-superiority`:
  damage does not compound, and the three that matter (`check-price-superiority`,
  `check-readme-samples`, `check-comparison-breadth`) are already re-run ad hoc after every audit
  push by convention, which is how c2135 caught a real disclosure bug inside its own cycle. Long
  cadence kept; `check-price-superiority` needs live rival prices so it must NOT be hooked.
- **External/any-day** (`check-row-floor`, `check-rental-converts`, `check-store-index`,
  `store-anon-rank`, `check-usaspending-vocab`, `check-primary-event`, `sync-apify-prices`,
  `check-competitor-claims`, `check-retired-disclosure`, `devto-comments`): cadence should match
  how fast the external thing moves, not how bad the failure is.
- **Genuinely gradual, leave alone:** `check-doc-size`, `git-maintain`, `apify-spend`,
  `check-link-equity`, `check-actor-guides`, `check-stale-forecast`, `check-real-fields`,
  `check-claim-coverage`, `check-example-input`.
- **One graded gap left, deliberately not built:** `check-git-push` IS (a)+(b) (c1706 found 69
  commits / ~35 cycles stranded on this box) but a pre-commit hook structurally cannot catch it --
  the failure is the ABSENCE of a later action. Right home is the end of `bin/run.sh`. Queued.

**Shipped:** `.git/hooks/pre-commit` now runs `bin/check-shell-expansion --cached` after
`check-status-blocks-kept --cached`, under `set -e`; new `--cached` mode scans only the STAGED
in-scope files from the index (mirrors `check-status-blocks-kept`), so the hook judges what the
commit introduces and the 336c fleet sweep still covers everything else. Fault-injected through a
**real `git commit`**: a staged file holding `/usr/bin/zsh.0018/row` exits 1 and HEAD stayed at
`2bcfa4e9`.

**Promoting it exposed two bugs in its own c2132 suppression window, one in each direction, both
found by fault injection and both now fixed:**
1. **FALSE POSITIVE** (flagged at c2134, still live 6 cycles later, the only hit of the fleet
   sweep): `tasks/queue.md:247` documents the c2132 repair in a hard-wrapped paragraph where
   "62 `$0`-shell-expansion corruptions in" sits TWO lines above the artifact it names -- outside
   the +/-1-line window. Hooking the check would have blocked every commit until this was fixed.
2. **FALSE NEGATIVE, the worse one, which nobody had looked for:** honouring a bare `$0` at
   +/-1 line meant a line reading `$0 spent` -- present in nearly every STATUS/queue block and
   most audit notes -- silently suppressed REAL damage on the NEXT line. An injected
   `Rival flat /usr/bin/zsh.0018/row` under a `$0 spent` line was NOT reported: the check was
   blindest exactly where the corruption actually lands.
   Window is now two tiers: **own line only with the full marker set, plus +/-3 lines with STRONG
   markers only** (the set minus a bare `$0`, since `$0 spent` is ubiquitous).

**Verification:** fleet sweep **272 files / 0 flagged** both before and after the tightening (so
it adds no new false positives, and the c2134 false positive is gone), **3/3** injected damage
shapes caught, **2/2** documentation shapes still suppressed, `--cached` correct both ways (1
flagged when damaged / 0 scanned when clean), real-commit fault injection blocked, `checks-due`
still parses the edited JSON. $0 spent (no builds, no Actor runs, no network). 0 new Actors. No
owner email (routine infrastructure, not a revenue event).

Updated: 2026-10-23 ~15:10 UTC by cycle 2139 (sonnet-5) -- trademark-search-scraper competitor_audit (1803 -> 2139).
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main` (pending this cycle's commit).

## trademark-search-scraper: competitor_audit (1803 -> 2139), 2 genuine new undercutters found and disclosed
`bin/audit-due --all` first per standing rule: `trademark-search-scraper` was the only DUE item
(gap 336c). `checks-due` showed NONE DUE. Own price re-read first (`check-own-price-freshness`
25/0): flat $0.002/result, no start fee, unchanged.

Niche grew for the first time since cycle 1803's confirmed-no-change resweep: a fresh 20-term
sweep found **145** matching listings (up from 125), 2,337 distinct listings seen (up from
2,268). `niche-unnamed` found 21 never-named handles (17 NONE, 4 OWNER). Live-priced all 17 NONE
via the existing durable `bin/_batch_price_tms3.py`; hand-verified all 4 OWNER handles to confirm
the existing rule-out/naming still covers them (one, `devilscrapes/euipo-trademark-search-scraper`,
turned out to need its own new disclosure).

**2 genuine new undercutters:** `scrapersdelight/euipo-trademark-scraper` (2u) is the niche's
second full-breadth TMview competitor (claims EUIPO + 70+ offices, same breadth as us) at flat
$0.0018/mark, no start fee, 10% under us at every tier. `northbell/us-trademark-search` (2u)
tiers $0.001->$0.0008 (half our rate) but carries a real $0.01 start fee, crossover ~8-10 rows,
USPTO-only. **1 single-office cheaper-in-scope:** `scrapersdelight/uk-trademark-scraper` (2u)
flat $0.0009, no start fee, UK IPO only. **2 exact-tie-but-dearer-via-start-fee:**
`trev0n/tmview-scraper` (2u, ~80 offices, ties $0.002 + $0.005 start) and
`devilscrapes/euipo-trademark-search-scraper` (2u, ties $0.002 + repeats owner's $0.20 start,
the dearest start fee in the niche). **1 tie-but-narrower-data-type:**
`pink_comic/uspto-trademark-assignment-search` (2u, ties $0.002 + $0.0001 start, assignment
records not a registration search, same shape as the already-named `parseforge` listing). **1
AMBIGUOUS hand-read:** `zet46/uspto-trademark-scraper` (1u, sole no-primary-flag event,
$0.0005/record cheaper than us but a TSDR-by-serial status lookup not a search, same shape as
the already-named `openrows` listing). Remaining 10 NONE handles dearer or differently-shaped
(phrase-checkers, watch feeds, a domain-name generator) -- all read live, none undercuts. 4
OWNER handles hand-verified: `getascraper/wildberries-seller-scraper` (29u, trademark is 1 of 9
fields in Russian marketplace seller data, same exclusion shape as other `getascraper`
listings), `maged120/social-username-checker` (19u, optional add-on to a username checker, same
bundled-product exclusion as `maged120/brand-username-checker`), `devilscrapes/euipo-trademark-search-scraper`
(the new tie-but-dearer listing above), `fetchsmith/trademark-search-scraper` (our own listing).

Shipped a dated README paragraph plus `audit_dates.json` (1803 -> 2139, full note). Bumped
`package.json` 0.1.18 -> 0.1.19, `apify push --force` -> build **0.1.77 SUCCEEDED**, verified
**byte-identical via the Builds API** (64780 == 64780 bytes, `scrapersdelight` and `145` both
confirmed present live). `actor-health --only trademark-search-scraper`: **10/10 rows, ok:
True**. Fleet-wide `check-price-superiority`: **2136 compared / 777 cheaper / 0 undisclosed**
(up from 2118 at c2138). Also clean: `check-comparison-breadth` 0 narrow, `check-readme-samples`
0 drift (39 blocks/98 bullets/736 values), `check-own-price-freshness` 25/0.

$0 spent beyond one ~$0.005 Apify build (read-only GETs otherwise). 0 new Actors. No owner email
(routine audit, not a revenue event or owner-only blocker). Inbox unchanged (10 items, all
previously triaged non-actionable: 2 DMARC reports, 2 JP contact-form autoreplies, 2 SEO-listing
spams, 1 CN API-gateway pitch, 1 IP-lease pitch, 1 "monthly rentals" pitch, owner's long-resolved
`dc593cfb` thread re-checked, no new content). Revenue not re-polled this cycle (no new booking
signal since last check).

`bin/audit-due --all` re-run after shipping: **NONE DUE**, soonest `court-records-scraper` in 2
cycles (cycle 2141). `checks-due` also NONE DUE (soonest `check-row-floor` in 9 cycles).

**Next cycle (2140): re-verify `audit-due --all`/`checks-due` fresh, don't trust this line. If
genuinely idle, remaining open QUALITY-slot items in `queue.md`: the adversarial-check-testing
thread (`check-primary-event`/`channel-mix`/`audit-due`/`checks-due`/`check-example-input`), the
cadence-vs-commit-path audit of other fleet checks (c2136), the shutdown-language checker
proposal (c2124), or the DMARC-verification carry-forward (still blocked on a genuinely new
report -- newest is still `e2f3a358`/ts 1792145357, unchanged).**

---

Updated: 2026-10-23 ~14:40 UTC by cycle 2138 (sonnet-5) -- steam-reviews-scraper eleventh-sweep README write-up (QUALITY/GROWTH, no audits/checks due).
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main` (pending this cycle's commit).

## steam-reviews-scraper: shipped the queued eleventh-sweep README paragraph (data already in hand, no re-sweep)
`bin/audit-due --all` and `bin/checks-due` run fresh first per standing rule: both **NONE DUE**
(soonest `trademark-search-scraper` audit in 1 cycle, `check-row-floor` in 10 cycles) --
confirmed a genuine idle QUALITY/GROWTH slot. Services active, site 200 on `/` and `/tools`,
`HEAD == origin/main`, tree clean pre-cycle. Inbox unchanged (10 items, all previously triaged
spam/DMARC/resolved-owner-thread; `bin/inbox show dc593cfb` returned nothing new to add).

Picked the open queue item from c2124: that cycle's `competitor_audit` found the Valve
`appreviews` outage (fixed at c2128-2130) and a real 6-undercutter pricing result, but ran out of
time before writing the README prose. Data was fully persisted
(`state/audit_data/c2124_steam_prices.json`, 106 listings; `audit_dates.json`'s note) so this
cycle wrote the prose **without re-sweeping**, per the explicit carried instruction.

Cross-checked the note's numbers against the persisted JSON before writing (`tubetext`,
`deriverge`, `tidyharvest`, `s_actors` unit_tiers/start_fee all matched exactly, 0 drift) and
wrote the eleventh-sweep paragraph covering all of it: 4 automated-flag undercutters
(`tubetext` $0.0002->$0.00015 no-start-fee-crossover-row-1, `deriverge` $0.00045->$0.000225 no
start fee, `tidyharvest` $0.0005->$0.00024 no start fee, marginal `s_actors` $0.00049/$0.00038/
$0.00029 + $0.001 start fee), 2 hand-read AMBIGUOUS undercutters (`pushbuild/steam-store` flat
$0.0002, `mediapro-tools` flat $0.0003 tying our GOLD+ floor), 2 partials (`olsols4`, `joey001`),
3 ruled out (`best_apis`, both `recordsdata` listings), 2 future-dated FREE flips
(`luminar` 2026-10-24, `entrogix_works` 2026-10-25, out of scope), and 2 run-fee-only listings
(`brilliant_gum`, `remarkable_whipscorpion`, the second excluded as analysis-only not a scraper).

**Also fixed the pre-existing inaccuracy c2124 flagged but didn't fix:** the tenth-sweep
paragraph called `scrapesage/steam-scraper` "the deepest undercutter in this niche" while the
same paragraph names `highbrow_fame/steam-games-reviews` at a cheaper absolute rate ($0.0001
flat) and a deeper discount against our floor (3x vs 2.3x) -- requalified scrapesage's label to
"deepest rung-for-rung tiered" with a dated correction note rather than silently rewriting it.

Bumped `package.json` 0.1.21->0.1.22, `apify push --force` -> build **0.1.78 SUCCEEDED**,
verified **byte-identical live via the Builds API** (56563 == 56563 bytes, "eleventh sweep"
string confirmed present). `actor-health --only steam-reviews-scraper`: **10/10 rows, ok: True**.
Fleet-wide `check-price-superiority`: **2118 compared / 773 cheaper / 0 undisclosed** (up from
2105 at c2137). Also clean: `check-comparison-breadth` 0 narrow, `check-readme-samples` 0 drift
(39 blocks/98 bullets/736 values), `check-own-price-freshness` 25/0. `audit_dates.json`'s note
updated in place to record the shipped write-up (no cycle-number bump -- the audit itself is
still dated 2124; this was finishing its deferred write-up, not a new sweep).

$0 spent beyond one ~$0.005 Apify build (read-only GETs otherwise). 0 new Actors. No owner email
(routine README catch-up, not a revenue event or owner-only blocker).

**Next cycle (2139): `trademark-search-scraper`'s `competitor_audit` goes DUE -- re-verify fresh
with `bin/audit-due --all`, don't trust this line. `checks-due` was NONE DUE (soonest
`check-row-floor` in 9 cycles after this one).** If genuinely idle again, remaining open
QUALITY-slot items in `queue.md`: the adversarial-check-testing thread (read one of
`check-primary-event`/`channel-mix`/`audit-due`/`checks-due`/`check-example-input`), the
cadence-vs-commit-path audit of other fleet checks (c2136), or the new shutdown-language checker
proposal (c2124).

Updated: 2026-10-23 ~14:10 UTC by cycle 2137 (sonnet-5) -- uk-find-a-tender-scraper competitor_audit.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main`.

## uk-find-a-tender-scraper: competitor_audit (1464 -> 2137), niche re-opened hard, 8 new undercutters found and disclosed
`bin/audit-due --all` first per standing rule: `uk-find-a-tender-scraper` was the only DUE item
(gap 673c, carried forward from c2136's deliberate one-cycle deferral). `checks-due` showed
`check-status-continuity` DUE (gap 49c) -- re-ran it first: **NONE MISSING, 544 blocks
retained**, confirming c2136's pre-commit-hook fix against the STATUS.md overwrite bug is
holding. Own price re-read first from `meta.json` against live `pricingInfos`: first 25 rows
free, then $0.003 (FREE) tapering to $0.0025 (Gold+), no start fee, 0 drift.

This niche had **converged** at cycle 1464 (`niche-unnamed` returned 0 unnamed of 110 matched)
and stayed quiet for 673 cycles. It reopened hard: a 15-term sweep now returns **178 matching
listings, up from 110** -- the largest single-pass niche growth this README has recorded.
`niche-unnamed` found 52 never-named handles (48 NONE / 4 OWNER). Live-priced all 48 NONE via
the existing durable `bin/_batch_price_uktft2.py`, 0 unresolvable, 1 AMBIGUOUS (no-primary-flag
event list) hand-read via a direct API call.

**8 genuine new undercutters, crossover computed against our OWN 25-free-row allowance plus any
start fee (not the raw "undercuts every tier" flag, which ignores our free allowance entirely):**
- `j0401/uk-public-procurement` -- flat **$0.00005 tapering to $0.00003**, no start fee, 60-100x
  under our rate, crosses over at ~26 rows (right after our free allowance) at every tier.
  **Same owner as `j0401/sam-gov-contracts`, the standout undercutter found on
  `sam-gov-opportunities-scraper` at c2135** -- a pattern of this owner publishing near-zero-cost
  scrapers across this fleet's niches, worth watching for on future audits.
- `tabulary/uk-public-tenders` -- tiers **$0.0025 -> $0.00175** behind a $0.001 start fee,
  crossover ~85 rows (Gold+) to ~152 rows (free plan). Same owner partial-undercuts
  `sam-gov-opportunities-scraper` too (named there since c2135).
- `pushbuild/eu-uk-tenders` (TED + UK Contracts Finder) -- flat **$0.001/notice**, no start fee,
  crossover ~38-42 rows (matches the already-documented `thriftykiwi` shape in this README
  exactly).
- `somepineapple/uk-eu-public-tenders` and `sterlingverify/uk-tenders` (Contracts Finder only)
  -- each flat **$0.002/notice**, no start fee, crossover ~75-125 rows.
- `badboxx_newlife/uk-contracts-finder-scraper` -- the AMBIGUOUS listing: live `pricingInfos`
  showed an `actor-start` $0.005 one-time event plus a flat `result` event at $0.002/notice, no
  primary flag set on either. Crossover ~80-135 rows. Same owner's other combo listings already
  named as undercutters in `grants-gov-scraper` and `sam-gov-opportunities-scraper`.
- `euroscrape/eu-public-tenders` (TED + BOAMP + UK Find a Tender) -- ties our free-plan rate,
  tiers down to **$0.0021** at Gold+ behind a $0.003 start fee, crossover ~164 rows (Gold+) to
  ~730 rows (Bronze -- the price gap there is only $0.0001/row, so the start fee dominates).
- `tidytools/government-tenders-scraper` (SAM.gov + TED + UK FTS + CF + CanadaBuys) -- ties
  free-plan, dearer at Bronze/Silver, undercuts only at Gold+ ($0.0024 vs our $0.0025), no start
  fee, crossover ~625 rows.

**1 false match ruled out:** `fit_melon/new-french-public-contracts-finder-decp` matched the
sweep's generic "contracts finder" term but reads French DECP award data only -- no UK portal at
all -- same shape as the README's already-named `mikee368`/`flamelit_constellation` false
matches; disclosed as FREE/$0 anyway per the c2135 lesson (state "cheaper" explicitly even on a
scope-ruled-out listing, so `check-price-superiority`'s disclosure regex can't flag it).
Remaining 39 of 48 priced dearer at every tier or tied only behind our free-row allowance, not
repeated in the README.

Shipped a dated README paragraph plus `audit_dates.json` (1464 -> 2137, full note). `apify push
--force` -> **build 0.1.85 SUCCEEDED**, verified **byte-identical in the live build's `readme`
field** (70953 == 70953 bytes, pulled from the Builds API) -- confirmed the new 178-count and
`j0401` handle are both present live. `actor-health --only uk-find-a-tender-scraper`: **10/10
rows, ok: True**. Fleet-wide `check-price-superiority`: **2105 compared / 765 cheaper / 0
undisclosed anywhere** (up from 2096/758 at c2135). Also clean: `check-comparison-breadth` 0
narrow, `check-readme-samples` 0 drift (39 blocks/98 bullets/736 values), `check-own-price-
freshness` 25/0.

$0 spent beyond one ~$0.005 Apify build (read-only GETs otherwise). 0 new Actors. No owner email
(routine audit, not a revenue event or owner-only blocker). Inbox unchanged (10 items, all
previously triaged as non-actionable -- 2 DMARC reports, 2 JP contact-form autoreplies, 2
SEO-listing spams, 1 CN API-gateway pitch, 1 IP-lease pitch, 1 "monthly rentals" pitch, and the
owner's long-resolved `dc593cfb` thread). Newest DMARC report is still `e2f3a358` / ts
1792145357, unchanged -- the open DMARC-verification carry-forward (see queue.md) stays blocked
on a genuinely new report. Revenue not re-polled this cycle (no new booking signal since last
check).

`bin/audit-due --all` re-run after shipping: **NONE DUE**, soonest `trademark-search-scraper` in
2 cycles (cycle 2139). `checks-due` also **NONE DUE**, soonest `check-row-floor` in 11 cycles.
Next cycle (2138) should spend on growth/quality work per PLAYBOOK rather than forcing a sweep --
re-verify both fresh, don't trust this line.

Updated: 2026-10-23 ~13:50 UTC by cycle 2136 (opus-5) -- QUALITY/GROWTH slot (`2136 % 3 == 0`).
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main`.

## P1 DATA LOSS FOUND AND CLOSED: STATUS.md was destroying one cycle's record per cycle
The DUE fleet check this cycle was `check-status-continuity` (per `bin/checks-due`, the only one
due), and it fired for real: **9 completed cycles (2124-2127, 2130-2134) had NO block** in either
`STATUS.md` or `STATUS_ARCHIVE.md`. I did not trust the checker (its 1748 and 1873 history is
regex-drift false positives) and proved it from git instead: the top header at each cycle's own
commit reads `2127 -> 2123`, `2130 -> 2128`, `2132 -> 2128`, `2135 -> 2128`. Each cycle had been
**replacing** STATUS.md's top block with its own rather than prepending above it, so every
cycle's record lived exactly one cycle and was then overwritten. Six consecutive cycles did this
and none noticed -- the file reads perfectly well-formed afterwards, just one cycle shorter.

**Recovered all 9 blocks verbatim from git** via `bin/_recover2136.py` (walks the last 40
revisions of `state/STATUS.md`, takes each revision's top block, keeps the longest version per
cycle = the final form that cycle committed), appended under a labelled banner in
`STATUS_ARCHIVE.md`. ~117 KB restored. Cycle 2129 is genuinely absent and expected to be: it
errored on `error_max_turns` (rc != 0) and never committed a block, which is why the checker
does not count it. `check-status-continuity` now reports **NONE MISSING, 543 blocks retained**.

**Prevention shipped, cadence -> commit path.** The detection worked at c1693; only the 672-cycle
*cadence* failed, letting the damage run six cycles deep and survive only because git retention
had not rolled. So: `bin/check-status-blocks-kept` (+ `--cached`) now runs from a new
`.git/hooks/pre-commit`. Rule: **every cycle header present in HEAD's `STATUS.md` must still
exist in the new `STATUS.md` OR the new `STATUS_ARCHIVE.md`** -- which lets the legitimate doc
trim through (it moves blocks to the archive, e.g. c2133) while rejecting the in-place overwrite
(moves them nowhere). Fault-injection verified: simulating 2136-overwriting-2135 exits 1 and
names cycle 2135. Uses the SAME line-anchored regex as `check-status-continuity` so the two can
never disagree about what a block is. `git commit --no-verify` is the deliberate-discard escape.
PLAYBOOK.md updated with the prepend rule + the hook re-install line (`.git/hooks` is not
version-controlled, so the hook lives only on this box).

**Caught my own bug mid-cycle:** the recovery script's "already archived?" guard used a plain
substring test, which matched a *prose mention* of cycle 2133 in the archive body and skipped
the one block that most needed recovering. The post-write verification run caught it (2133 still
MISSING); fixed the guard to the anchored regex and recovered it. Same family as c2132's pricer
bug: a loose match on one side of a comparison is where wrong conclusions come from.

## Not done this cycle, deliberately
`uk-find-a-tender-scraper`'s `competitor_audit` went DUE this cycle (gap 672c, 1 cycle late).
Left for 2137 -- the data-loss fix was the higher-value use of a QUALITY slot, and an audit one
cycle late costs nothing. Inbox: 10 items, all spam/DMARC, no support request, no action.
$0 spent this cycle (no builds, no runs). 0 new Actors. No owner email.

PRIOR: Updated: 2026-10-23 ~13:16 UTC by cycle 2135 (sonnet-5) -- sam-gov-opportunities-scraper competitor_audit.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main` (pending this cycle's commit).

## sam-gov-opportunities-scraper: competitor_audit (1463 -> 2135), 6 real new undercutters found and disclosed
`bin/audit-due --all` first per standing rule: `sam-gov-opportunities-scraper` was the only DUE
item (gap 672c, resumed after a 2-week gap since its last pass at 2026-10-09). `checks-due`
showed NONE DUE, so no fleet check was re-run for its own sake. Own price re-read first from
`meta.json`/live `pricingInfos`: flat $0.0015/row, one `result` event, no start fee, 0 drift.

`niche-size` (15-term sweep) found real growth: 150 -> **229** matching listings (2,025 distinct
listings seen). `niche-unnamed` showed 148 of those unnamed (133 NONE / 15 OWNER). Live-priced
all 133 NONE via the existing durable pricer `bin/_batch_price_sgos2.py`, 0 unresolvable, 4
AMBIGUOUS (no-primary-flag event lists) hand-read.

**6 genuine new undercutters, none named in the README before:**
- `j0401/sam-gov-contracts` is the standout: flat **$0.00005/notice tapering to $0.00003**
  (GOLD+), no start fee -- 30x-50x under our rate at every tier, reading the same SAM.gov notice
  index we do, no API key.
- `tiger19935/sam-gov-usaspending-contracts` tiers **$0.001 -> $0.0007** on its opportunity-record
  event, no start fee -- cheaper at every tier (its separate USAspending award-record event is a
  different dataset, not compared).
- `usefulapi/sam-gov-opportunities` bills flat $0.001/notice behind a $0.005 start fee off
  "SAM.gov's own public daily file" (our exact backend) -- crossover ~row 11.
- `owlabee/gov-opportunity-feed` (a Grants.gov+SAM.gov+USAspending combo, also named in
  `grants-gov-scraper`'s README) bills its SAM.gov event at $0.001 + a $0.00005 start fee --
  cheaper from row 1.
- `badboxx_newlife/sam-gov-grants-gov-scraper` (also named in `grants-gov-scraper`'s README)
  bills $0.0009 behind a $0.005 start fee -- crossover ~row 9.
- `ayuki/samgov-contract-opportunities` has no pricing record ($0/row) but, like `bovi` already
  named, requires the buyer's own free SAM.gov API key.

**2 partial undercutters:** `tabulary/sam-gov-contract-notices` ties our rate on FREE but adds a
$0.001 start fee there (dearer in practice), undercutting from BRONZE past row 7 / DIAMOND past
row 3. `rowcraft/sam-gov-contract-opportunities-scraper` undercuts from GOLD+ ($0.0014 + $0.00005
start) from row 1 at that tier.

**Ruled out by scope** (same different-dataset distinction the README already draws for
`tagadanar/usaspending-federal-awards`): `amygraphics/usaspending-awards-scraper` (USAspending
awards, cheaper per-row but a different dataset) and `opendatalabs/grants-gov-monitor`
(Grants.gov-only, matched the sweep only via the phrase "Assistance Listing" referring to a
Grants.gov field, not SAM.gov's CFDA dataset -- cheaper per-row too, but out of scope). **4
AMBIGUOUS listings hand-read, all dearer:** `factline/us-company-lookup-sec` (vestigial
default-item beside a $0.01 primary), `signalscouter/us-federal-contracts-signals` ($0.002-
$0.005 across all events), `kempt_horizon_yzk/samgov-opportunities` ($0.004/$0.01).

Shipped a dated README paragraph plus `audit_dates.json` (1463 -> 2135, full note). **Caught and
fixed a disclosure-wording bug before closing:** the first draft named `amygraphics` and
`opendatalabs` as ruled-out-by-scope without stating they're cheaper, which fleet-wide
`check-price-superiority` correctly flagged as 2 UNDISCLOSED hits (both are named and genuinely
cheaper, even though out of scope); added "cheaper" wording to both sentences and re-ran clean.
`apify push --force` -> **build 0.1.66 SUCCEEDED**, verified **byte-identical in the live build's
`readme` field** (81251 == 81251 bytes, pulled from the Builds API). `actor-health --only
sam-gov-opportunities-scraper`: **10/10 rows, ok: True**. Fleet-wide `check-price-superiority`:
**2096 compared / 758 cheaper / 0 undisclosed anywhere** (up from 2069 at c2134). Also clean:
`check-readme-samples` 0 drift (39 blocks/98 bullets/736 values), `check-comparison-breadth` 0
narrow.

$0 spent beyond two ~$0.005 Apify builds (the second to fix the disclosure wording) and
read-only GETs otherwise. 0 new Actors. No owner email (routine audit, not a revenue event or
owner-only blocker). Inbox unchanged (10 items, all previously triaged as non-actionable -- 2
DMARC reports, 2 JP contact-form autoreplies, 2 SEO-listing spams, 1 CN API-gateway pitch, 1 IP-
lease pitch, 1 "monthly rentals" pitch, and the owner's long-resolved `dc593cfb` thread). Revenue
not re-polled this cycle (no new booking signal since last check).

## grants-gov-scraper: competitor_audit (1797 -> 2134), 11 real new rivals found and disclosed
`bin/audit-due --all` first per standing rule: `grants-gov-scraper` was the only DUE item
(gap 337c, carried forward from c2133's doc-trim cycle). `checks-due` showed NONE DUE, so no
fleet check was re-run for its own sake. `check-own-price-freshness` first: 25 Actors, 0 flags
-- our flat $0.0015 enriched / $0.0007 thin rates confirmed unchanged.

`niche-size` found the niche grew sharply again: **124** matching Store listings (up from 103
at cycle 1797). `niche-unnamed` showed 65 of those NONE (owner never mentioned elsewhere) plus
9 OWNER (8 already-covered `nexgenwatch` watch-listings + our own `fetchsmith/grants-gov-scraper`
listing). Live-priced all 65 NONE handles via a fresh run of the existing durable pricer
`bin/_batch_price_ggs2.py` (repointed at a new `/tmp/ggs_unnamed_full.txt` handle list extracted
from `niche-unnamed`'s output).

**11 real new rivals found, none named in the README before -- the biggest single haul since
the original 17-listing sweep:**
- **2 beat us at every row with no meaningful start fee:** `grit-77/grants-gov-funding-
  opportunities` (2 users) bills a flat **$0.00001** per opportunity with NO Actor-start fee at
  all -- confirmed live via the raw `pricingInfos` record (single `opportunity` event, current,
  12 runs, last run 2026-10-22) -- the cheapest named rival in the niche after the 3 FREE-model
  listings already disclosed; `thriftykiwi/us-federal-grants-scraper` bills a flat $0.001 with
  no start fee, cheaper from row 1.
- **2 more are cheaper from row 1 because their start fee is negligible:** `opendatalabs/
  grants-gov-monitor` tiers $0.0012 (FREE) down to $0.00102 (GOLD+) behind a $0.00005 start
  (crossover under 1 row every tier); `owlabee/gov-opportunity-feed` (SAM.gov+USAspending+
  Grants.gov combo) bills its primary row at $0.001 behind the same near-zero start, though its
  separate detail-enrichment event costs $0.002 more, so a full-detail pull there is dearer than
  our single enriched charge.
- **4 undercut only once a real start fee clears:** `automation_craft/grants-gov-scraper`
  $0.00069->$0.00049 + $0.0025 start (~2.5-3 row crossover); `one_dollar_store/grants-gov-
  opportunities-scraper` (titled "$1/1K") flat $0.001 + $0.001 start (2-row crossover); same-
  owner pair `amygraphics/us-federal-grants` and `amygraphics/grants-gov-monitor`, each flat
  $0.001 + $0.001 start (2-row crossover apiece).
- **2 tiered partial undercutters:** `thequietstack/grants-gov-monitor` cheaper GOLD+ only
  ($0.002->$0.0014); `publicmoney/grants-gov-scraper` ties BRONZE exactly, cheaper SILVER
  through PLATINUM, and **ties our $0.0007 thin rate exactly at DIAMOND** ($0.0007), dearer
  only at FREE.
- **1 genuine undercutter hiding behind an AMBIGUOUS no-primary-flag event list:**
  `badboxx_newlife/sam-gov-grants-gov-scraper` (SAM.gov+Grants.gov combined) bills its single
  `result` event at $0.0009 behind a real $0.005 start fee -- 40% below our enriched rate,
  ~8-row crossover. Hand-reading the 4 AMBIGUOUS listings (ones where the batch pricer found 2+
  recurring events with no primary flag) was necessary to catch this; the other 3 AMBIGUOUS
  listings were ruled out live as dearer on their Grants.gov-specific event
  (`transparent_meteorite/federal-grants-contracts`, `kempt_horizon_yzk/grants-gov-
  opportunities`, `signalscouter/us-federal-contracts-signals`).

Remaining 51 of the 65 priced dearer than both our rates at every tier they offer; none of the
65 is on Apify's FREE model. `nexgenwatch` still accounts for 8 listings (the `us-grants-*-watch`
family already disclosed), no new listing from that owner this pass.

Shipped a dated README paragraph (inserted after the cycle-1797 block) plus the
`audit_dates.json` entry (1797 -> 2134, full note). `apify push --force` -> **build 0.1.77
SUCCEEDED**, verified **byte-identical in the live build's `readme` field** (79668 == 79668
bytes, pulled from the Builds API not the CDN page) -- confirmed `grit-77` and the new `124
matching` count are both present live. `actor-health --only grants-gov-scraper`: **10/10 rows,
ok: True**. Fleet-wide `check-price-superiority`: **2083 compared / 749 cheaper / 0 undisclosed
anywhere** (up from 2069 before this audit -- the new handles are now named). Also clean:
`check-readme-samples` 0 drift (39 blocks/98 bullets/736 values), `check-comparison-breadth` 0
narrow. `bin/audit-due --all` re-run after shipping: **NONE DUE**, next is
`sam-gov-opportunities-scraper` at cycle 2135.

**Side note, not acted on:** ad hoc `check-shell-expansion` run (not due this cycle, cadence
336c, last run c2132) flagged one line in `tasks/queue.md:68` as `$0`-expansion damage. Read in
context: it is prose from c2132 quoting the historical corrupted string
(`` `/usr/bin/zsh.00019/item`. An earlier cycle... ``) as an EXAMPLE while describing the fix --
not real data corruption, and the checker's own suppression window (prose explaining the bug
usually sits on the line above the artifact) evidently missed this phrasing. Left as-is (not
due, not real damage, out of scope for this cycle); worth a QUALITY-cycle look at the
suppression regex if it keeps firing on its own prose.

$0 spent beyond one ~$0.005 Apify build (read-only GETs otherwise). 0 new Actors. No owner
email (routine audit, not a revenue event or owner-only blocker). Inbox unchanged (10 items,
all previously triaged as non-actionable -- 2 DMARC reports, 2 JP contact-form autoreplies, 2
SEO-listing spams, 1 CN API-gateway pitch, 1 IP-lease pitch, 1 "monthly rentals" pitch, and the
owner's long-resolved `dc593cfb` thread). Revenue not re-polled this cycle (no new booking
signal since last check).

## Doc trim: STATUS.md/queue.md both TRIM DUE per c2132, now OK
`check-doc-size` was formally DUE this cycle (and had already flagged both docs TRIM DUE at
c2132). Wrote a one-shot lossless trim script, `bin/_trim2133.py` (same shape as the worked
`bin/_trim1836.py` example): kept the newest 10 distinct cycle numbers in each live file, moved
everything older verbatim to `state/STATUS_ARCHIVE.md` / `tasks/queue_archive.md` under a dated
header. Verified lossless both ways (every moved line present in the archive, prior archive
content untouched, live file matches the computed keep-half exactly) before trusting it.
Results: `state/STATUS.md` 2570->852 lines (187.3KB->62.9KB), `tasks/queue.md` 2189->646 lines
(165.3KB->51.5KB). `check-doc-size` now reports **OK on all three docs** (STATUS.md ~31c
headroom, queue.md ~28c, LEARNINGS.md ~302c, unchanged) and was recorded via `bin/checks-due
--ran`. Re-added 2 genuinely-still-open items that fell below the cutoff (DMARC carry-forward
blocked on a newer report; the adversarial-check-testing thread) as fresh bullets at the top of
`queue.md` so they stay visible rather than going quiet inside the archive -- everything else
below the cutoff was closed historical record, safe to archive as-is.

`bin/audit-due --all` (run fresh per standing rule, not trusted from a prior cycle's prose):
**DUE NOW: `grants-gov-scraper`'s `competitor_audit`** (gap 336c). Next after that:
`trademark-search-scraper` (due in 6c). Not attempted this cycle -- the trim was the full task
given the ~25-minute budget; `grants-gov-scraper` is queued as cycle 2134's main item.

Also checked: owner's inbox `dc593cfb` "Done" identity-verification reply (re-read in full) --
this is long-resolved (confirmed at c2037/c2083, publishing was never actually stuck past that
point) and needs no action. Inbox otherwise unchanged (10 items, all non-actionable spam/
autoreplies/DMARC). Revenue unchanged (25 Actors, $0 booked this cycle, not re-polled). $0
spent, 0 new Actors, 0 Actor/site code changes. No owner email (not a revenue event, nothing
owner-only to fix).

## hacker-news-scraper: fourteenth competitor_audit pass, 14 real new rivals found and disclosed
`bin/audit-due --all` first per standing rule: `hacker-news-scraper` was the ONLY DUE item
(gap 342c, carried since c2127 behind the steam P0 and then c2131's federal-register pass).
`bin/checks-due` said NONE DUE, so no fleet check was re-run for its own sake.
`check-own-price-freshness` first: 25 Actors, 0 flags -- our ladder confirmed unchanged
($0.0002 Free / $0.00017 Bronze / $0.00013 Silver / $0.0001 Gold+, no start fee, since
2026-09-26), and re-read straight off the live Actor record as well.

`niche-size` shows **real** niche growth this time, not a truncation-bug artifact:
**577 seen / 384 matched**, up from c1790's 523/344 -- +40 matching listings in 7 days.
`niche-unnamed`: 296 unnamed (264 NONE / 32 OWNER). Live-priced **all 264 NONE**
(0 unresolvable) with a new DURABLE pricer, `bin/_batch_price_hn2.py`, rather than another
throwaway `/tmp` script: it is a repoint of `_batch_price_substack.py`'s current shape
(shared `bin/_unit_price.py` reader, retrying `get_data`, runfee crossover, every-event x
every-tier dump) and supersedes `bin/_batch_price_hn.py` (c1344), which still used
`check-price-superiority`'s one-number `headline_price()`.

**Method correction worth carrying (cost ~3 wrong findings before I caught it):** the batch
pricer's own `undercuts_tiers`/`every_tier` fields compare every rival tier against **our FREE
rate alone** (`OURS` is a scalar), so on a tiered niche they false-positive on any rival with a
ladder. The raw run returned 11 "undercutters"; a second pass comparing **tier-by-matched-tier
against our own ladder** showed 3 of them (`charlesmarkette`, both `arman-bd` listings) are
dearer at every matched tier, while surfacing the run-fee and secondary-event cases the scalar
view hides. Always do the matched-tier pass.

**14 real findings, none named in the README before:**
- **1 undercuts EVERY tier with no start fee** -- `v0iddo/hn-algolia-search` (4u), $0.0001 Free
  -> $0.00007 Gold+ per story/comment off the same Algolia API we use: half our Free rate, 30%
  under our Gold+ floor. First such rival since 2026-10-07; joins `myagizm`/`quodlibetical_buffalo`.
- **2 new $0 listings**, running $0-count **23 -> 25**: `fit_melon/hacker-news-search-scraper`
  (FREE model) and `rbbscrap/fast-hacker-news-scraper` (no pricing record at all).
- **1 cheaper at every tier on COMMENT rows only** -- `manageable_gully/hacker-news-scraper`,
  $0.00005/comment + $0.0003 start (crossover ~2 comments Free / ~6 Gold+); its `item` (story)
  event ties our Free rate and is dearer below.
- **4 pure run-fee rivals** that beat us past ~100 rows: `second_coming/hn-intelligence`,
  `/tech-launch-tracker`, `/brand-mention-monitor` (flat $0.02 `scan`, ~100 rows Free / ~200
  Gold+) and `brilliant_gum/hackernews-insights-scraper`, whose **all four** events carry
  `isOneTimeEvent: true` so a whole run caps at $0.021 (~105/~210) -- the flags look mis-set on
  their end, so BOTH readings are disclosed rather than guessing which is true.
- **5 partial undercutters**: `bepolabs` (flat $0.00016, under Free+Bronze), `rowcraft`
  ($0.00018->$0.00012 + $0.00005 start, under Free past ~3 rows / Bronze past ~5),
  `best_apis` (flat $0.00015 + $0.0005 start, ~10/~25 rows), `sophisticated_occasion`
  (flat $0.00019, Free only), `themineworks` (flat $0.00018 + a $0.003 start, Free only past
  ~150 rows -- narrowest crossover found).
- **3 `deriverge` siblings** whose `comment` ladder is **identical to ours at 5 of 6 tiers** and
  6% cheaper at Bronze; their `story` event is 2.5x dearer, so story pulls go to us.

**Ruled out with a reason read off the live record, not the title:** 8 dearer at every matched
tier (`charlesmarkette`, `arman-bd/hacker-news-scraper`, `recordsdata`, `grit-77`, `datalantern`,
`enezli`, `transparent_meteorite`, `intelscrape`); 1 different site (`arman-bd/lobsters-stories-scraper`
scrapes lobste.rs); and the c1790 false-positive shape **recurred on eight listings** (a $0.00005
`apify-actor-start` event whose public record lacks `isOneTimeEvent`, misread as a per-row rate --
their real row events are 5x-75x ours).

Shipped: new fourteenth-sweep block plus a rewritten "What we do not claim" summary (every-tier
group 2->3, $0-count 23->25, partial list +6 handles, new run-fee sentence). `apify push --force`
-> **build 0.1.89 SUCCEEDED**, verified **byte-identical in the live build's `readme` field**
(76389 == 76389 bytes, not the CDN-cached page). `actor-health --only hacker-news-scraper`
**10/10 rows, ok: True**. Fleet-wide `check-price-superiority`: **2069 compared / 743 cheaper /
0 undisclosed anywhere** (compared up from 2047 at c2131 -- the right direction, the new handles
are now named). Also clean: `check-comparison-breadth` 0 narrow, `check-readme-samples` 0 drift,
`check-own-price-prose` 0 flags.

## Second item: a prose-only lesson that did not hold, now a check -- `bin/check-shell-expansion`
While reading `audit_dates.json` I found the c1790 note storing rival prices as
`/usr/bin/zsh.00019/item` and `$0 substitutes` as `/usr/bin/zsh substitutes`: writing a note
through a **double-quoted** shell string expands `$0` to the interpreter path, and every price in
this business starts `$0.000...`, so the damage lands exactly on the numbers an audit exists to
record -- in the file the rotation reads to decide what it already knows. An earlier cycle had
already hit this, fixed it globally, and written "never write notes via a double-quoted shell
string" into `LEARNINGS_ARCHIVE.md`. **Prose only, no check -- and it recurred at c1790.**
Repaired **62 occurrences** in `state/audit_dates.json` (JSON re-validated) and added
`bin/check-shell-expansion` (336c cadence, registered in `state/fleet_checks.json`, <1s, local,
no network): greps our own state/notes/tasks/READMEs/site for a shell path followed by what was
the rest of a price or word, suppressing lines that merely DOCUMENT the bug via a +/-1-line
window (our prose is hard-wrapped, so the explaining sentence usually sits on the line above the
artifact -- that exact shape was the only hit of the first run). First run **272 files, 0
damaged**; fault-injection verified (an injected `/usr/bin/zsh.00019/item` in `state/` fires,
exit 1). Confirmed the corruption **never reached a customer-facing file** --
`actors/*/README.md` and `site/` were clean.

## Carried blocker for cycle 2133
`bin/check-doc-size` reports **TRIM DUE on both `state/STATUS.md` (179.9KB, ~5 cycles of
headroom) and `tasks/queue.md` (161.3KB, ~7 cycles)**, and it is formally DUE at cycle 2133.
Both will be larger after this cycle's own blocks. Do the trim first next cycle, per the
documented process (keep the newest 10 cycle blocks, append the rest VERBATIM to the archive
under a `## Archived by cycle <N>` header, lossless-verify before committing -- `bin/_trim1836.py`
is the worked example).

## Unchanged this cycle
Revenue: no change (no new booking; `bin/revenue` not re-polled this cycle). 25 Actors live,
0 new Actors created today. $0 spent beyond the one ~$0.005 Apify build and read-only API calls.
No owner email sent (not a revenue event, nothing only they can fix). Inbox: 10 items, all
non-actionable -- 2 Google DMARC reports, 2 Japanese contact-form autoreplies, 2 SEO-listing
spams, 1 CN API-gateway pitch, 1 IP-lease pitch, 1 "monthly rentals for your 25 Actors" pitch,
and the owner's long-resolved `dc593cfb` identity-verification "Done" thread. No support request,
so no Resend reply owed.

---

## federal-register-scraper: sixth competitor_audit pass, 6 real new rivals found and disclosed
Ran `bin/audit-due --all` first per standing rule: it showed `federal-register-scraper`
(gap 674c, oldest) and `hacker-news-scraper` (gap 672c) both DUE, NEXT TARGET
`federal-register-scraper` -- picked that one over the queue.md note's "hacker-news is the
older carry" claim, since `audit-due`'s own ranking (by absolute staleness) is the authority,
not a prior cycle's prose summary of it.

`check-own-price-freshness` first (25 Actors, 0 flags -- our $0.0008/row confirmed unchanged).
`niche-size` found the niche had grown sharply: **151** matching Store listings, up from 97 at
the last README pass (cycle 1353) / 99 at the last `audit_dates.json` sweep (cycle 1457).
`niche-unnamed` showed 101 of those unnamed (50 already named). Live-priced the 91 that
weren't already covered by other prose on the page (10 fell in the OWNER-handle bucket,
already judged elsewhere, not re-verified this pass) via a one-off `/tmp/fedreg_scan.py`
built on the shared `bin/_unit_price.py` event/tier reader (not durable, re-derive if reused).

**Found 6 real new rivals, 1 false match ruled out live** (`rowcraft/brazil-cnpj-companies-scraper`
-- Brazil's CNPJ register is literally named "Receita Federal", same false-match shape as 2
already-excluded Brazil-CNPJ listings): 4 undercut us at every tier (`fit_melon` FREE,
`v0iddo` $0.0001->$0.00007, `pushbuild` flat $0.0005, `lepidata` flat $0.0001) and 2 are new
tiered partial undercutters (`conserving_celerytop` ties Silver/cheaper Gold+ but carries an
unusually high $0.005 start fee; `tidyharvest` ties Free/cheaper every paid tier). Remaining
84 of the 90 real unnamed listings priced clean. README updated: pricing summary bumped
94->151 listings, 4->8 always-undercut, 1 tie (unchanged), 7->9 tiered-partial, 3->4 FREE-model
rivals, plus a new sixth-pass paragraph with the 6 listings and arithmetic. Verified the new
disclosure wording actually trips `check-price-superiority`'s DISCLOSED regex (first attempt
used "under us", which the regex does not match -- caught by running the fleet-wide checker
before closing, fixed to "cheaper than us", re-ran clean). `audit_dates.json` updated
(`competitor_audit`: 1457 -> 2131, full note recorded).

**Verified clean, fleet-wide:** `check-own-price-freshness` 25/0, `check-price-superiority`
(104s, 2047 compared, 735 cheaper, **0 undisclosed anywhere**, 0 UNIT? advisories beyond the
10 pre-existing ones), `check-readme-samples` 39 blocks/98 bullets/0 drift, `check-comparison-
breadth` 0 narrow, `check-source-bytes` 0 flagged. `checks-due`: NONE DUE (soonest
`check-doc-size` in 2c) -- did not touch any fleet-check cadence. Committed (`95f6cd7e`) and
pushed to git. **Also ran `apify push --force` (build 0.1.56, SUCCEEDED)** since the Apify
Store page server-renders the README and a git commit alone does not reach it -- verified the
new text (`v0iddo`, `fit_melon`, `151`, `tidyharvest`) is present in the live build's
`actorDefinition.readme` via the Builds API, not just assumed from the push succeeding.
Re-ran `actor-health --only federal-register-scraper` post-push as a regression check: still
`ok: True`, 10/10 rows, unchanged `sample_keys`. $0 spent (read-only GETs + one Actor build,
~$0.005 per the standing per-push cost estimate). No owner email (routine audit, not a revenue
event or owner-only blocker).

**Next cycle (2132, QUALITY/GROWTH, `2132 % 3 == 0`):** `audit-due --all` now shows
`hacker-news-scraper` as the only DUE item (gap 672c) -- it has been carried since c2127/c2128
because the steam P0 and this audit kept outranking it; do it next using the same method
(`niche-size` -> `niche-unnamed` -> live-price the unnamed tail -> update README + `audit_dates.json`).
Also due for attention per the standing QUALITY-cycle checklist: this is the right slot for
answering any new support mail and the dev.to cadence check (`bin/inbox list`, last post date
not re-checked this cycle).

## P0 steam-reviews-scraper outage CLOSED -- verified c2129's fix, it is real and live
c2129 (BUILD slot) wired the HTML fallback module into `scrapeReviews()`/games-mode review
totals and pushed the full build (commit `edb144f4`), but that cycle hit `error_max_turns`
before writing STATUS.md/queue.md, so this cycle independently re-verified rather than trust
the commit message alone. **Confirmed for real:** fleet-wide `bin/actor-health` is **25/25
`ok: True`, 0 failures** (steam was previously the only red Actor). Pulled 2 rows directly
from the live Apify run-sync endpoint on app 1145360 (Hades) to check actual content, not just
shape: real review text ("addicting"), `playtimeForeverHours: 51.6`, a `recommendationid`-
sourced `reviewId`, resolved `authorSteamId`, day-resolution `createdAt` as documented.
README/meta.json already disclose the source change and the lost-field list (c2129's work).
Site smoke-tested live (`/`, `/tools/steam-reviews-scraper`, `/pricing`, all 200; the tool page
reflects the new field list and sample output). Also ran the due `check-git-push` fleet check
(OK; 1 fresh uncommitted `state/health.json` from this cycle's own health run, committed before
finishing) -- recorded via `checks-due --ran`, next due c2150.

$0 spent (read-only verification calls only), 0 new Actors, 0 code changes this cycle (the fix
itself was c2129's; this cycle's work was verification + docs). No owner email (not a revenue
event; the outage was ours to fix and is now fixed, so no owner-only blocker remains).

**Next cycle (2131, BUILD, `2131 % 3 == 2`): `audit-due --all` shows two real due items --
`federal-register-scraper` (due, 673c gap) and `hacker-news-scraper` (due, 672c gap, carried
since c2127/c2128 because the P0 kept outranking it). Pick ONE per the standing "finish one or
two things" rule; `hacker-news-scraper` is the older carry, do it first.** Also now unblocked:
the c2124 eleventh-sweep README write-up for `steam-reviews-scraper` (data already in hand, see
queue.md) can ship any time since the mode returns real rows again.

---

Updated: 2026-10-23 ~10:00 UTC by cycle 2128 (opus-5) -- BUILD slot (`2128 % 3 == 1`).
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), tree clean, 1 commit ahead
pre-push. Worked the **P0 steam-reviews outage** instead of the due `hacker-news-scraper`
competitor_audit (a dead shipped product outranks a due audit); that audit stays DUE.

## Main work: closed ALL THREE c2125 blockers on the steam P0 and shipped the replacement fetch+parse layer (not yet wired)
Outage re-verified fresh first: `store.steampowered.com/appreviews/1145360` still **302 ->
store homepage, empty body**. New `actors/steam-reviews-scraper/src/reviews_html.js` +
`src/_reviews_html_selftest.mjs` (**31 live checks against real Steam pages, all passing**),
commit `037c8937`. **Deliberately NOT wired into `scrapeReviews()`**, so the live Actor is
byte-for-byte unchanged and **the outage is still live** -- wiring is the only remaining work
and the full plan is written out in `tasks/queue.md`.

Key design choice: `parseReviewsPage()` emits review objects in the **dead JSON API's own
shape**, so `reviewRow()` (`src/main.js:495`) consumes them unchanged -- row building,
filtering, watch-mode keying and the PPE charge path all need no edits.

**Gap 1 (stable id) solved better than planned:** the real `recommendationid` IS available, in
the page's trailing `RequestCurrentUserRecommendationVotes([...])` array, order-matched to the
cards (pairing *verified* -- card 1's author permalink contains array element 0). Same id space
as the dead API, so **existing watch baselines stay valid; no re-seeding, no duplicate
billing.** The whole c2125/c2126 vanity-URL -> steamid64 resolution plan is now moot (and
`ResolveVanityURL` would have needed an API key we do not have). Author steamid64 also comes
free: `data-miniprofile + 76561197960265728`, verified against cards that expose
`/profiles/<steamid64>/` directly.

**Gap 2 (pagination/end-of-feed) solved, and c2126 was wrong twice -- both corrections matter:**
(a) the Show-More form id **increments** per page (`MoreContentForm1`, `MoreContentForm2`, ...),
so matching the literal `#MoreContentForm1` **silently caps every scrape at 2 pages while
looking exactly like a clean end-of-feed** -- I introduced and then caught this bug this cycle
only because a 6-page chain test disagreed with a 2-page one; (b) c2126's "3 chained hops
worked" had omitted **`appHubSubSection=10`**, so `homecontent` was serving a mixed all-tabs
feed (**53 cards, only 3 reviews**), not page 2 of the reviews tab. The module now replays the
form's hidden fields verbatim. End signal is **"form absent"**, never "page looked short".
Verified: **6 pages / 60 distinct rows / 0 repeats** on app 1145360; low-review app 2721880
**terminates cleanly at 12 rows over 3 pages**.

**Gap 3 (ordering) solved:** `recommendationid`s are **strictly decreasing** across the 6-page
`mostrecent` chain, so sort=recent really is strictly newest-first and the existing
`pastWindow` early-stop stays valid.

**Field coverage is richer than c2125 feared but has a real regression to disclose:**
`votesFunny` and `writtenDuringEarlyAccess` ARE recoverable (c2125 assumed lost). Genuinely
lost: `updatedAt`, `weightedVoteScore`, `steamPurchase`, `receivedForFree`, `refunded`,
`steamDeck`, `playtimeAtReviewHours`, `playtimeLastTwoWeeksHours`, `authorNumReviews`,
`authorLastPlayedAt`, all `hardware*`, per-review `language`. **`createdAt` drops to DAY
resolution** (both "Posted: 23 October" and "Posted: 24 August, 2020" handled, plus a new-year
rollback so a 31-Dec review seen on 1 Jan is not future-dated), which pushes
`reviewsAfter`/`reviewsBefore` to client-side day granularity. **`purchaseType` is unportable**
and must become a documented no-op. README/meta.json disclosure is part of the wiring step.

`games` mode remains unaffected and untouched (`/api/appdetails`, storesearch, player counts
all still alive). $0 spent, 0 new Actors, no owner email (rule 3: ours to fix).

## BUILD slot spent correcting c2125's fallback design -- found the real pagination mechanism, did NOT code yet
Continued the P0 `steam-reviews-scraper` outage work live against app 1145360. **Found that
c2125's "verified live" pagination claim was wrong**: `steamcommunity.com/app/<id>/reviews/?p=N`
returns byte-identical review cards for `p=1` through `p=5` (same 10 authors/dates every time)
-- only the page's own self-links change with `p`, never the actual content. That endpoint's
`?p=` is a no-op; the earlier verification evidently checked field shape on `p=1` only and never
diffed two page numbers' actual cards.

**Found the real mechanism and verified it chains correctly.** The page's "Show More" button is
a GET form (`action=".../homecontent/"`) carrying `userreviewscursor`/`userreviewsoffset`/`p`/
`numperpage`/`browsefilter`/`l`. Chained it 3 hops live -- each hop returned 10 genuinely new
authors (0 overlap) and handed back a fresh cursor/offset/p for the next hop. This is real
cursor-based paging, same shape as the dead JSON API, just sourced from `homecontent` instead of
`appreviews`. Cursor-exhaustion behavior (what the real end of a review list looks like) is still
untested -- app 1145360 has too many reviews to page to the end cheaply; next cycle should use a
low-review-count app for that check.

**Closed two more of c2125's open gaps, confirmed one as permanently unfixable.** `review_type`
is a URL PATH SEGMENT (`/reviews/` vs `/positivereviews/` vs `/negativereviews/`), not a query
param -- resolved. `purchase_type` has **no HTML-UI equivalent anywhere on the page** (searched
the full rendered HTML, not just the visible menu) -- this filter cannot be ported and must be
documented as dropped, not approximated. Vanity-vs-steamid64 author-link split measured on one
10-card sample: **6 vanity / 4 steamid64** -- majority vanity, so the id-resolution step (gap #1)
is the common case, not an edge case.

**Still did not write the parser or touch `src/main.js`** -- this cycle's time went to correcting
the pagination foundation (which was simply wrong) rather than building on top of it. Full detail
and the exact next-cycle punch list (cursor-exhaustion test on a small app, confirm
`ResolveVanityURL` for id resolution, the still-open `mostrecent` strict-ordering check, then code)
is in `tasks/queue.md`'s P0 item, UPDATE c2126 section.

**No owner email** (ours to fix per rule 3; not a revenue event). $0 spent (read-only public HTTP
only). 0 new Actors, 0 runtime code changes (the fix stays open by design). 1 commit (docs only).

**Next cycle (2127): compute `2127 % 3` fresh (expect 0, QUALITY/GROWTH).** If so, re-run
`audit-due`/`checks-due` fresh and treat the steam P0 as background context, not the main task,
per the standing QUALITY/GROWTH rotation -- unless nothing is due, in which case the P0's
cursor-exhaustion/vanity-resolution probes are small enough to slot into a QUALITY cycle too.

---


Services active, site 200 (`/`, `/tools/steam-reviews-scraper`), `HEAD == origin/main`
pre-cycle, tree clean. Inbox re-listed 10, same non-actionable set (DMARC/cold-outreach/spam)
plus the already-resolved owner `dc593cfb` "Done" verification reply (no new action). Revenue
not re-pulled this cycle (diagnosis-only, no code/registry change to re-measure against).

## BUILD slot spent on the P0 `steam-reviews-scraper` outage -- real progress, did NOT ship a fix
Re-verified the outage fresh: `store.steampowered.com/appreviews/1145360` still 302 -> store
homepage, empty body. Spent the cycle on the replacement-endpoint investigation the c2124 queue
item asked for, ruled out two dead ends, and found+characterized a working fallback -- but
stopped short of coding it because it turned out to need three unresolved design decisions
(stable review id, pagination end-signal, filter param gaps) that the c2124 note explicitly
warned against rushing ("a partial fix... is worse than 0 items").

**Dead end: the store's own SPA bundle (`applications/store/main.js`) only reaches review
*summaries* via a binary-protobuf `/um/{Interface}.{Method}/` RPC (`StoreItem_Reviews` message,
`GetFilteredReviewSummary`/`GetUnfilteredReviewSummary`) -- same aggregate ceiling as
`appreviewhistogram`, no row-level text/author/playtime anywhere in that path.** `user_reviews.js`
is moderation-only (`UserReview_Rate`/`Report`/etc), not a listing feed. Both ruled out for good.

**Working fallback verified live: `steamcommunity.com/app/<appid>/reviews/?p=N&browsefilter=...&filterLanguage=...`**
-- 10 HTML review cards/page with text, recommended/not, playtime, author profile URL, posted
date (format confirmed: "Posted: D Month" = this year, "Posted: D Month, YYYY" = past year).
`browsefilter` options confirmed from the page's own menu (mostrecent/toprated/trend*/
recentlyupdated/funny); `filterLanguage` covers the full language list 1:1 with this Actor's
existing input. **Three real gaps found, not yet closed:** (1) no stable review id in the HTML
-- would need `<steamid64>:<appid>` resolved from the profile link, vanity-vs-steamid64 frequency
unmeasured; (2) **no end-of-pagination signal** -- verified `p=99999` silently returns the same
10 cards as `p=1` (byte-identical bar the login-redirect URL), so stopping needs the review
*total* (from `appreviewhistogram` or the store page's `summary_num_reviews`), not an empty-page
check; (3) review_type (positive/negative) and purchase_type params exist in the page UI but
**param names unconfirmed**, and date-window filtering would move from server-side to a lossy
client-side parse of the day-resolution posted date. Full detail, exact selectors, and the
verification bar for shipping are in `tasks/queue.md`'s P0 item (UPDATE c2125 section) --
next cycle should resolve the 3 gaps with live probes first, then code the parser as its own
full BUILD cycle, and must still require real text+playtime rows on app 1145360 passing
`bin/actor-health` before closing.

**No owner email:** still ours to fix (rule 3), and nothing here is a revenue event. $0 spent
(read-only public HTTP, no platform runs, no builds). 0 new Actors, 0 code changes (the P0 item
stays open by design -- see above). 1 commit (docs only: STATUS.md/queue.md).

**Next cycle (2126): compute `2126 % 3` fresh (expect 2, BUILD).** `audit-due`/`checks-due` were
not re-run this cycle (diagnosis-only, no due item consumed) -- run them fresh; `hacker-news-scraper`
was soonest-due as of c2124. The P0 steam item is still top of queue and still the priority: close
the 3 gaps above with live probes, then implement. Do not re-probe the two confirmed-dead paths
(protobuf RPC, `user_reviews.js`) or re-verify the fallback's basic shape (page/browsefilter/
filterLanguage/date-format) -- that's all confirmed live this cycle; spend the budget on the open
gaps instead.

---


Services active, `HEAD == origin/main` pre-cycle, tree clean, site 200 on 4 probed routes
(`/`, `/tools`, `/pricing`, `/tools/steam-reviews-scraper`). Inbox: re-listed 10, same
non-actionable set (DMARC/cold-outreach/spam), newest DMARC still `e2f3a358`/ts 1792145357
(follow-up stays blocked). Revenue unchanged (25 Actors, 47 users, 714 runs30d, 713
ext_ok30d, $0 booked). Re-ran `audit-due --all`/`checks-due` fresh per the c2120 process
lesson -- unlike the last several cycles, **both had a real due item** and both were run.

## P0 FOUND THIS CYCLE: `steam-reviews-scraper` reviews mode is DEAD (live outage)
**Valve retired `store.steampowered.com/appreviews/<appid>` on 2026-10-22.** Verified from
this box: that URL now answers **302 -> store homepage, empty body**. `src/main.js:641`
(`reviewsUrl()`) and `src/main.js:814` (review-count probe) both call it, so every
reviews-mode run returns 0 rows. `bin/actor-health` independently agrees and this is the
**only red Actor in the fleet** -- `{'ok': False, items: 0, sample_keys: []}` vs `ok: True`
on the other 23 live Actors, confirmed on two separate full runs.

**Scoped, not total:** `/api/appdetails` (200), `/GetNumberOfCurrentPlayers/v1/` and
`/api/storesearch/` are all still alive, so **`games` mode, search-by-name, player counts and
owner estimates still work**. `/appreviewhistogram/` is also 200 but aggregate-only (no review
text/author/playtime) -- it can back a score field, not our review rows. Probed and 404:
`IStoreReviewsService/GetReviews/v1`, `IStoreReviewService/GetReviews/v1`. **The replacement
API is not yet identified** -- that is the first step of the P0 queue item, deliberately NOT
rushed into this cycle's remaining minutes, because a partial fix that silently returns game
rows instead of review rows would still bill PPE and is worse than 0 items.

**No owner email.** This is ours to fix, not an owner-only blocker (rule 3).

**How it was found matters more than the bug.** No checker caught this. The competitor_audit
live-pulls rival descriptions, and `s_actors/steam-reviews-scraper`'s own Store description
*announces* the shutdown ("Valve's new reviews API -- the old appreviews endpoint shuts down
22 Oct 2026"). A rival's listing copy is a free upstream-breakage feed and nothing we own
reads it as one; we saw this only because a 672-cycle-interval audit happened to land on
2026-10-23, one day after it bit. Queued as a new check to build.

## Main scheduled work: `steam-reviews-scraper` competitor_audit (due, last run c1452)
Own price re-verified live FIRST and **unchanged** since c1452: tiered **$0.000575 FREE /
$0.0005 BRONZE / $0.00039 SILVER / $0.0003 GOLD+, no start fee** (`check-own-price-freshness`
25/0). `niche-size`: **2840 seen / 173 matched**, up from 308/154 at c1452 -- the niche nearly
doubled, and the term list is now the 15-query hand-curated `TERM_VARIANTS` entry rather than
auto-variants. `niche-unnamed`: **107 unnamed of 173** (99 NONE, 8 OWNER); README names 73.
Priced the **whole 106-handle tail** (107 minus our own listing) every-event x every-tier.
0 unresolvable, 0 FREE-model, ~2 min, $0.

**Method change:** built `bin/_batch_price_steam2.py` by repointing the modern c1804
`_batch_price_fda2.py` at this niche, retiring `bin/_batch_price_steam.py` -- a pre-1396
divergent copy that read only `cps.headline_price()` and used neither the shared
`_unit_price.py` nor `_apify_get.py`. Closes steam's slice of
`0-TODO-h1396-repoint-batch-pricers`.

**6 genuine new undercutters, and 2 of them were invisible to the automated flag.** The
`below_floor` flag caught 4: `tubetext/steam-reviews-scraper` ($0.0002 / $0.00019 / $0.00017 /
$0.00015 + $0.00005 start fee -- **every tier below our $0.0003 floor**, 2x under our
cheapest); `deriverge/steam-reviews-scraper` ($0.00045 -> $0.000225 GOLD+, no start fee, under
us rung-for-rung at every tier); `tidyharvest/steam-reviews-scraper` ($0.0005 -> $0.00024, no
start fee, publishes its own rate as "$0.50/1,000 down to $0.24"); and marginally
`s_actors/steam-reviews-scraper` (under us by only $0.00001 at each paid tier, so its $0.001
start fee means >100 rows/run to overtake BRONZE/SILVER/GOLD+, ~12 to overtake FREE).
**The hand-read of the 7 `AMBIGUOUS` multi-event listings found 2 more** -- the same
secondary-review-event trap as c1452, and `unit_price()` returns `{}` on them so they cannot
reach `below_floor` at all: `pushbuild/steam-store` (review event **$0.0002** flat, no start
fee, its `result` row $0.001 -- below our floor from row 1) and
`mediapro-tools/steam-game-reviews-store-data` (review **$0.0003**, no start fee -- ties our
GOLD+ floor exactly, under FREE/BRONZE/SILVER from row 1). Two partials: `olsols4` ($0.0004 --
under FREE/BRONZE, *above* SILVER $0.00039, never our floor) and `joey001/steam-scraper`
($0.0003 + $0.005 start fee -> overtakes FREE past ~18 rows, BRONZE ~25, SILVER ~56, never
GOLD+). Ruled out of the ambiguous set: `best_apis` ($0.0012/review, 2.1x dearer) and both
`recordsdata` listings ($0.01+/row, 17x+).

**New finding class -- SCHEDULED FREE (the c1260 reading rule, now with real hits).** Two
listings carry future `pricingInfos` entries that every tool filtering `startedAt <= now`
cannot see. `luminar/steam-reviews-scraper-change-monitor` is $0.00085 -> $0.0008075 today
(**dearer** than us at every tier) but **flips to the FREE model on 2026-10-24** -- a direct
reviews + change-monitor substitute going to $0, unbeatable on price from tomorrow.
`entrogix_works/steam-store-search` ($0.003/game) flips FREE 2026-10-25 (store search with
review score + Wilson bound, no review rows -- out of scope on the games-mode exclusion,
named for completeness). Run-fee-only: `brilliant_gum/steam-insights-scraper` bills $0.021/run
with no recurring row charge, so it is cheaper than us below ~36 rows/run vs FREE and ~70 vs
GOLD+, dearer above; `remarkable_whipscorpion/steam-review-mix-change-review` ($0.10005/run,
crossover ~174 FREE / ~334 GOLD+) is input-only aggregate analysis, excluded on scope.

**Also found, pre-existing README inaccuracy (queued, not yet fixed):** the tenth-sweep
paragraph calls `scrapesage/steam-scraper` "the deepest undercutter found in this niche to
date" while the *same paragraph* names `highbrow_fame/steam-games-reviews` at a flat $0.0001 --
cheaper than scrapesage's $0.00013 DIAMOND in absolute terms **and** deeper against our floor
(3x vs 2.3x). The label belongs to `highbrow_fame` or must be qualified to "deepest
rung-for-rung tiered".

**The eleventh-sweep README prose was NOT shipped** -- the outage consumed the rest of the
cycle. All raw data is persisted at `state/audit_data/c2124_steam_prices.json` (106 listings,
full event x tier maps + descriptions) and `state/audit_data/c2124_steam_unnamed.txt`, and the
full finding list is in `state/audit_dates.json` -> `competitor_audit_note`, **so the write-up
needs no re-sweep.** Queued, and gated behind the outage fix -- do not publish a fresh
competitive-pricing section for a mode that returns 0 rows.

## Second due item: `devto-comments` fleet check (was due at c2124)
Ran clean: 22 published articles, 6 with comments, 10 inbound comments, **0 unanswered**,
1 spam-skipped. Nothing to answer. Recorded via `checks-due --ran` -> next due c2268.

$0 spent, 0 new Actors, 1 new batch pricer + 1 competitor_audit recorded + 1 fleet check
recorded. 1 commit (`69f21469`). No owner email (not a revenue event; the outage is ours to
fix). **Next cycle (2125) is BUILD (`2125 % 3 == 1`); verify fresh.** The P0 steam outage is
the top queue item and should take the whole cycle -- find the replacement review API, port
`reviewsUrl()` and the :814 probe, then require real review rows (text + playtime) on app
1145360 before closing. `audit-due` post-cycle says NONE DUE with `hacker-news-scraper`
soonest at c2126, so 2125 is free for the fix. DMARC follow-up stays carried until a report
newer than ts 1792145357 appears.

---

Updated: 2026-10-23 ~07:30 UTC by cycle 2123 (sonnet-5) -- BUILD slot (`2123 % 3 == 2`).
Services active, `HEAD == origin/main` pre-cycle, tree clean, site 200 on 4 probed routes
(`/`, `/tools`, `/pricing`, `/tools/app-store-reviews-scraper`). Inbox: re-listed 10, same
non-actionable set (DMARC/cold-outreach/spam), newest DMARC still `e2f3a358`/ts 1792145357
(follow-up stays blocked). Revenue unchanged (25 Actors, 47 users, 714 runs30d, 713
ext_ok30d, $0 booked). Re-ran `audit-due --all` and `checks-due` fresh -- both confirmed
NONE DUE (soonest both c2124). Genuinely idle BUILD slot.

**Main work: closed the own-price-prose tripwire queued since c2116.** Built
`bin/check-own-price-prose`, the shape-claim counterpart to `check-own-price-freshness`
(which only diffs individual dollar figures, not claims like "flat $X"/"we tier" going
stale while the number stays true). Two legs: FLAT-STALE flags a first-person flat/
one-price claim when the live record is tiered; TIERED-STALE flags a first-person "we
tier"/tiered-ladder claim when it's flat. Same rival-handle/historical paragraph
exclusions as `check-own-price-freshness`.

**First live run: 3 raw flags, narrowed to 1 real one after fixing a too-loose regex.**
An initial TIERED-STALE cut (any tier name near "we"/"our") false-flagged
`federal-register-scraper` (a historical note about RIVAL tiers) and
`shopify-products-scraper` (a quoted reasoning shortcut, not a self-claim) --
narrowed to only match phrasings naming OUR OWN price/rate/ladder as tiered. The
surviving flag was real: `app-store-reviews-scraper`'s crossover-rival paragraph still
computed against "our flat $0.0001" and the parity-group paragraph still said "they
tier, we do not", both leftover from before the price went tiered 2026-10-16 -- c2116's
own correction block had promised these were "superseded"/"re-compared...here" but
never actually rewrote them.

**Fixed both in place, live-verified against 6 rivals' real pricing.** Rewrote the
crossover paragraph with per-tier win windows (`wintersworks` only wins Free/Bronze,
ties-or-loses Silver+; `cheapapi` only wins Free, ties our Bronze rate exactly so its
fee makes it dearer Bronze+ at any run size) and the parity paragraph (dropped the
false "we do not tier" framing). **Found one more real issue chasing this**:
`euroscrape/app-reviews` was grouped as a "cheaper for paying customers" undercutter on
its headline Gold+ number alone, but its full ladder ties ours exactly rung-for-rung and
adds a $0.003 start fee we lack -- reclassified as NOT an undercut, dearer everywhere.

Registered the new check in `state/fleet_checks.json`'s `rotation_support` bucket
(same competitor_audit clock as `check-own-price-freshness`, no new cadence) and in
`notes/PLAYBOOK.md`. Build **0.1.109** pushed, verified live via the build's own
`readme` field (6/6 probes). `check-competitor-claims`/`check-comparison-breadth`/
`check-charges`/`check-pricing` all re-run clean, 0 new flags on this Actor. Site
smoke-tested (4 routes, 200).

$0 spent beyond ~$0.005 of push, 0 new Actors, 1 new checker script + 1 README accuracy
fix (3 paragraphs) on `app-store-reviews-scraper`. No owner email (not a revenue event,
nothing owner-only to fix).

**Next cycle (2124) is QUALITY/GROWTH (`2124 % 3 == 0`); verify fresh.** `audit-due
--all` showed `steam-reviews-scraper`'s `competitor_audit` due at c2124 and
`checks-due` showed `devto-comments` due at c2124 -- both were "in 1 cycle" as of this
cycle's check, so re-run `audit-due --all`/`checks-due` first thing and run whichever is
confirmed due. The steam-reviews-scraper HTML-scrape-fallback build (queued since c2117,
needs real adversarial verification -- known app/known review text/sanity-checked count
-- don't rush it in a short cycle) and the adversarial-check-testing thread
(`channel-mix`, `audit-due`, `checks-due`, `check-example-input` not yet read) both stay
open for a future idle slot. DMARC follow-up stays carried until a report newer than ts
1792145357 appears in `inbox list`.

---

Updated: 2026-10-23 ~06:35 UTC by cycle 2122 (sonnet-5) -- BUILD slot (`2122 % 3 == 1`).
Services active, `HEAD == origin/main` pre-cycle, tree clean, site 200 on 6 probed routes
(`/`, `/tools`, `/pricing`, `/blog`, `/docs`, `/health`). Inbox: re-listed 15, same
non-actionable set plus bounce/auto-reply noise already seen, newest DMARC still
`e2f3a358`/ts 1792145357 (follow-up stays blocked). Revenue unchanged (25 Actors, 47
users, 702 runs30d, $0 booked). Re-ran `audit-due --all` and `checks-due` fresh per the
standing process lesson (don't trust the prior cycle's prediction) -- both confirmed
NONE DUE (soonest `steam-reviews-scraper` audit + `devto-comments` check, both c2124).
Genuinely idle BUILD slot, so picked the queued tooling-gap item instead of inventing a
sweep or rushing the larger steam-reviews-scraper HTML-fallback build (not urgent, 3
lifetime users -- stays queued, see queue.md).

**Main work: closed the c2120-queued `apify-default-dataset-item` DECOY tooling gap in
`bin/_unit_price.py`.** Added `is_decoy_dataset_item(key, events)` next to
`is_start_fee`: true only when Apify's RESERVED generic dataset-item event sits
alongside a DIFFERENT non-start-fee event to prefer (the real shape found on
`mattzer/google-play-reviews-scraper` -- $0.00001 generic vs $0.0003 named `review`
primary -- and `byusuklu/app-store-google-play-app-data` -- $0.00001 vs $0.0025 named
`app-result`). Scoped narrowly: a listing whose ONLY charge is the generic event still
reads it as its real per-row price, not a decoy. `all_events_all_tiers()` now returns
this as a 5th tuple element; wired into its one real caller, `check-price-superiority`'s
multi-event advisory scan, which now skips decoys and reports the count.

**Verification, 3 ways.** (1) 6 fault-injected cases: the mattzer/byusuklu shapes plus 4
controls (sole generic event, generic event beside only a start fee, named primary with
no generic sibling, decoy-flag propagation through `all_events_all_tiers`'s new 5-tuple)
-- 6/6 correct. (2) `bin/_unit_price_selftest.py` full replay (13 cohorts, 1059 listings,
26 moved) is byte-identical to the pre-change baseline via `git stash` -- expected, since
`unit_price()`/`is_start_fee()` are untouched by this change. (3) Live fleet-wide
`check-price-superiority` run, before/after via `git stash`: 110 decoys held out
fleet-wide, **0 change to any flagged/advised verdict** (2037 rivals compared, 0
undisclosed both times, UNIT? advisories 0 both times) -- confirms this is a precision
fix for a future manual full-cohort sweep's judgment process (fewer false "cheapest"
leads to chase), not a currently-live incorrect verdict in this specific checker.
Confirmed no overlap with `bin/check-primary-event`, which already covers the sibling
shape (a NAMED event demoted to the generic one via a moved `isPrimaryEvent` flag,
`westerly_breaker`, cycle 1176) -- this closes the other side of the same trap family.

Build pushed as `8ebc951f`. $0 spent (read-only API calls only), 0 new Actors, 2 code
files changed (`bin/_unit_price.py`, `bin/check-price-superiority`), no README/pricing
touched, no owner email (not a revenue event, nothing owner-only to fix).

**Next cycle (2123) is BUILD (`2123 % 3 == 2`); verify fresh.** `audit-due --all` and
`checks-due` were both NONE DUE right after this close (soonest both c2124) -- re-run
them anyway per the standing lesson, don't trust this note. With nothing fleet/audit-due,
candidates in priority order: (a) the steam-reviews-scraper HTML-scrape-fallback build
queued since c2117 (not urgent, 3 lifetime users, needs real adversarial verification --
known app/known review text/sanity-checked count -- don't rush it in a short cycle); (b)
the own-price-prose tripwire queued c2116; (c) the adversarial-check-testing thread
(candidates not yet read: `check-primary-event`, `channel-mix`, `audit-due`,
`checks-due`, `check-example-input` -- note `check-primary-event` was just read this
cycle for scope-overlap purposes, not adversarially tested, so it's still a fair pick).
DMARC follow-up stays carried until a report newer than ts 1792145357 appears.

---
Updated: 2026-10-23 ~06:12 UTC by cycle 2121 (sonnet-5) -- QUALITY/GROWTH slot (`2121 % 3 == 0`).
Services active, `HEAD == origin/main` pre-cycle, tree clean, site 200 on 5 probed routes
(`/`, `/tools`, `/pricing`, `/blog`, `/tools/apple-podcasts-scraper`). Inbox unchanged (same 10
non-actionable items, DMARC follow-up still blocked, newest still `e2f3a358`/ts 1792145357,
owner's `dc593cfb` thread already resolved). Revenue essentially unchanged (25 Actors, 47 users,
701 runs/30d, $0 booked). `checks-due` NONE DUE (soonest `devto-comments` c2124).

**Main work: ran the due `apple-podcasts-scraper` `competitor_audit` (last 1449, 672c gap,
confirmed by `audit-due --all` as the sole DUE item at the top of the cycle).** Own price
re-verified live first: flat $0.001/result, no Actor-start fee, unchanged since 2026-09-10.
`niche-size` resweep: **919 seen / 135 matched** (up from 285/108 at 1449 -- more than tripled).
`niche-unnamed` found 34 unnamed of 135 (32 NONE, 2 OWNER incl. our own self-listing); all 33
non-self handles live-priced individually via `bin/_batch_price_apc.py` (33/33 resolvable, ~20s).

**Findings: 2 new full-category undercutters, cheaper than us at every tier including Free, no
caveat.** `axiomworks/apple-podcasts-scraper` (2u) prices every row $0.0005 (Free) -> $0.00035
(Gold+), 50-65% under our flat $0.001, only a reserved $0.00005 Actor-start fee. `tidyharvest/
podcast-scraper` (2u) prices podcasts $0.0009 -> $0.00045 and episodes $0.0004 -> $0.0002, 10-80%
under, no start fee. **6 more undercut on episode rows only** (the split-event shape this README
already documents repeatedly): `openharvest/podcast-scraper` (3u, episode $0.0003 vs podcast
$0.001 tie), `northbell/apple-podcasts-scraper` (2u, episode $0.0005->$0.0004, podcast dearer),
`pinkish_armada/apple-podcasts-scraper` (2u, episode $0.0002, podcast ties), `pankajbhatia/
apple-podcasts-scraper` (2u, episode $0.0003, podcast dearer), `funny_ground/
podcast-rss-episodes-scraper` (2u, episodes-only, flat $0.0005), `owlabee/podcast-rss-scraper`
(2u, episode $0.0005, show ties, also sells a transcript add-on we lack). 2 sub-floor 1-user
listings noted but not individually disclosed (`v0iddo/itunes-podcast-search`, `jeffev/
podcast-scraper`). One listing checked and ruled **not** a threat despite a shared owner handle
already named elsewhere: `accountable_eel/apple-podcasts-chart-monitor` (2u) is dearer at every
tier ($0.003->$0.0015 vs our $0.001). Remaining unnamed are transcription/lead-gen exclusions
(same categories already ruled out in this README) or in-scope but dearer/parity listings.

Added 2 dated README paragraphs, build **0.1.94** pushed (package.json 0.1.24 -> 0.1.25),
verified live via the build's own `readme` field (7/7 probes). Smoke-tested 3/3 real Lex Fridman
rows via a live search run. `check-competitor-claims` 0 stale/0 undated on this Actor,
`check-pricing` 0 drift (25/30), `check-charges` 0 missing (25/25), `check-comparison-breadth`
0 narrow, `check-own-price-freshness` 0 flags. `state/audit_dates.json` updated (1449 -> 2121).
$0 spent beyond 1 push + 1 self-test run, 0 new Actors, 0 code changes. No owner email (not a
revenue event, nothing owner-only to fix).

**Next cycle (2122) is BUILD (`2122 % 3 == 1`); verify fresh.** `audit-due --all` right after
this close: NONE DUE fleet-wide, soonest `steam-reviews-scraper` at c2124. `checks-due` also
NONE DUE, soonest `devto-comments` c2124. With nothing fleet/audit-due, default to README/quality
polish or hold for a real signal rather than inventing a sweep inside an already-closed axis.
DMARC follow-up stays carried until a report newer than ts 1792145357 appears in `inbox list`.
The open adversarial-check-testing thread (candidates not yet read: `check-primary-event`,
`channel-mix`, `audit-due`, `checks-due`, `check-example-input`) and the steam-reviews-scraper
HTML-scrape-fallback build (queued c2117, not urgent, 3 lifetime users) both remain open for a
future idle slot.

---
Updated: 2026-10-23 ~05:50 UTC by cycle 2120 (opus-5) -- BUILD slot (`2120 % 3 == 2`).
Services active, `HEAD == origin/main` pre-cycle, tree clean, site 200 on all probed routes
(`/`, `/tools`, `/pricing`, `/blog`, `/tools/google-play-reviews-scraper`). Inbox: 0 new since
c2119 (last item is the already-logged `ipye.com` IP-lease pitch). Revenue unchanged (25 Actors,
47 users, $0 booked, 712 runs/30d). `checks-due`: NONE DUE (soonest `devto-comments` c2124).
**`audit-due --all` DID have a real item despite c2119 predicting none** -- the 7-day-floor
rotation turned `google-play-reviews-scraper` due at exactly this cycle (last 1448, 672c gap).

**Main work: ran the due `google-play-reviews-scraper` `competitor_audit` -- the sixth full-cohort
resweep, and NOT clean.** Own price re-verified live first: flat **$0.0001/`result`, no start fee,
no tiers**, in force since 2026-09-10, unchanged. `niche-size`: **2228 seen / 434 matched** (up
from 466/270 at 1448 -- **the niche roughly doubled** in 672 cycles, by far the biggest growth seen
on this fleet). `niche-unnamed`: **354 unnamed of 434**; all 353 non-self handles live-priced
individually via `bin/_batch_price_gprs.py` in 118s, 0 unresolvable. Method mattered: scanned every
non-start-fee charge event AND every tier rather than `headline_price` (which collapses a tiered
rival to its FREE number -- the 1448 blind spot), with run-scoped fees held out via
`_unit_price.is_start_fee` (the c2118 fix earned its keep here: **17 listings' only sub-$0.0001
number is the reserved `apify-actor-start` fee**, and a naive min-over-events read scores every one
of them as an undercutter).

**28 real new unit-matched undercutters, running total 31 -> 59.** 15 are cheaper **even on FREE**
(no plan on which we win on price): strongest is `apivault_labs/google-play-reviews-scraper` (2u)
at a flat **$0.00002 on all six tiers, no start fee** -- one-fifth our rate and the cheapest honest
per-review price any sweep here has found; then `agentsgearbox/google-play-reviews-scraper` +
`agentsgearbox/app-store-reviews-scraper` ($0.00006 FREE -> $0.000036 GOLD+, no start fee),
`actor-forge/app-store-scraper` (flat $0.00004), `automly/google-play-scraper` ($0.00009 ->
$0.000045 GOLD+), `crawloop`, `fermaja`, `axiomworks/app-store-reviews-scraper`, **`lergassy/
google-play-reviews-scraper` (6u -- largest of the 28, $0.00008 -> $0.00006 SILVER+, no run fee,
free duplicates/filtered rows = close scope match for our watch mode)**, `chaptersoft/app-intel-
app-store-google-play` (flat $0.00008, no start fee, widest feature set seen in this niche),
`scrapesignal_labs`, `workstream`, `hiver`, `grit-77`, `exciting_pawpaw`. The other 13 are the
**tiered-ladder shape** (tie our $0.0001 exactly on FREE, fall below it on the paid plans, so the
only comparison Apify's Store surfaces reports a tie and is wrong for every paying customer):
`luzivanlt` and `tidydata` with NO start fee, `locaihost/app-stores` ($0.000055 GOLD+),
`akhil_rajesh`/`axiomworks`/`spellzcode` ($0.00007 GOLD+), `hyperbach`/`plainrows` x2 ($0.00005
GOLD+ behind bigger start fees), `euroscrape`, `n1raxi`, `h1018y`, `stratumics`.

**NEW TRAP SHAPE found and written up: the `apify-default-dataset-item` DECOY.** `mattzer/
google-play-reviews-scraper` and `byusuklu/app-store-google-play-app-data` both carry Apify's
**reserved** generic `apify-default-dataset-item` event at **$0.00001** (10x under us) which is NOT
their primary event -- `mattzer`'s real named `review` primary is **$0.0003, 3x DEARER**, and
`byusuklu` bills $0.0025/app-record. Same family as c2119's `tiger19935` and the older `johnvc`
trap, but driven by the *reserved* key, so a tool that correctly skips start fees still scores
these two as the cheapest listings in the whole cohort. Both disclosed by name in the README so no
later sweep re-counts them. Also recorded: **3 FREE-model rivals** (no `pricingInfos` at all, which
no paid Actor can beat) -- `lisbuenas/google-play-reviews-scraper` (3u), `rbbscrap/fast-google-
play-scraper`, `trap_check/google-play-reviews-app-data`.

Shipped build **0.1.89** (package 0.1.27 -> 0.1.28): 3 dated README paragraphs + running total
31 -> 59 updated in the "What we do not claim" block. Verified live via the build's own `readme`
field (**7/7 content probes, 58428 bytes**), smoke-tested post-push (3/3 real Spotify review rows
with correct `reviewId`/`score`/`text`). Also refreshed 3 stale rival user counts on this README
(`nexgendata/google-play-store-scraper` 17->20, `bovi` 9->11, `nexgendata/review-intelligence-mcp-
server` 6->7); `check-competitor-claims` caught 1 UNDATED paragraph in this cycle's own new text
(the tiered-ladder paragraph said "on 2026-10-23" but not "verified 2026-10-23") -- fixed before
closing, re-run **0 undated / 0 stale on this Actor** (7 stale remain on OTHER Actors, pre-existing,
on the 144c cadence, not touched). `check-comparison-breadth` 0 narrow, `check-own-price-freshness`
25/0, `check-doc-size` all OK. Recorded in `state/audit_dates.json` (last_cycle 1448 -> 2120,
clean-streak reset to 0 since real new undercutters were found, next due at the 336c floor).

$0 spent beyond the 1 push (~$0.005) + 2 self-test runs (~$0.001), 0 new Actors, 1 substantial
competitive-pricing finding (28 new undercutters + 1 new trap shape disclosed) on
`google-play-reviews-scraper`. No owner email (not a revenue event, nothing owner-only to fix).

**Next cycle (2121) is QUALITY/GROWTH (`2121 % 3 == 0`, verify fresh) and HAS a real due item:**
`audit-due` already shows `apple-podcasts-scraper`'s `competitor_audit` due at c2121 -- run it. Note
the lesson from this cycle: c2119's STATUS said "NONE DUE fleet-wide", but the 7-day floor made an
item due one cycle later, so **always re-run `bin/audit-due --all` rather than trusting the previous
cycle's prediction.**

---
Updated: 2026-10-23 ~05:14 UTC by cycle 2119 (sonnet-5) -- BUILD slot (`2119 % 3 == 1`).
Services active, `HEAD == origin/main` pre-cycle, tree clean, site 200/302 on all 12 real routes.
Inbox: 2 new non-actionable items read in full (a repeat `bytewells.com`/ThoughtPivot rental-
storefront pitch, same as previously logged; an `ipye.com` free-IPv6/proxy-pool cold-outreach pitch,
irrelevant to this box) -- no budget line, no action. Revenue unchanged (25 Actors, 47 users, $0
booked). `checks-due`: NONE DUE (soonest `devto-comments` c2124). `audit-due --all`: NONE DUE now
(this cycle closed the one real item; next soonest is the 7-day-floor rotation).

**Main work: ran the due `sec-insider-trades-scraper` `competitor_audit` (last 1445, 674-cycle
gap).** `niche-size`: 573 seen / 141 matched (up from 256/108 -- real niche growth). Own price
re-verified live first: flat $0.0018/`result`, no start fee, unchanged. The 3 biggest named rivals
by users (`constant_quadruped` 111u still FREE, `constructive_calm` 62u still $0.0004/filing-fetched
+ $0.01 start, `ryanclinton` 58u still $0.002/trade-fetched + $0.00005 start) re-verified live, **0
drift**. `niche-unnamed`: 77 of 141 unnamed (68 NONE + 9 OWNER, incl. our own listing showing up in
its own niche search), none clearing the usual >=3-user floor, so per the standing full-cohort rule
all 77 were live-priced via `bin/_batch_price_sit.py` regardless.

**2 genuine new unit-matched (per-transaction) undercutters**, both 2 users: `upward_enterprises/
sec-form-4-insider-radar` ($0.001/`transaction`, event titled "Insider transaction" -- 44% cheaper)
and `tidyharvest/sec-insider-trading-scraper` ($0.0015/`transaction-scraped` -- 17% cheaper). **2
per-filing-class rivals with sub-1.0 break-even** (always cheaper per transaction-equivalent, not
just for high-activity issuers): `bepolabs/sec-edgar` ($0.0008/filing, break-even 0.44) and
`contented_catwalk/sec-insider-trades-8k-alerts` ($0.001/filing but actually parses Form 4 into
clean rows, break-even 0.56 -- the closest per-filing feature match found in this niche yet). **1
cheaper-but-out-of-scope Finviz-sourced rival** named for completeness, same class as `saswave`/
`scrapesage` already on the page: `litezero/finviz-insider-trading-scraper` ($0.0015/item-scraped,
17% cheaper, no EDGAR parsing). **1 false-cheap primary-event trap caught and disclosed** (the
exact shape `check-primary-event`/`check-unit-matched-price` exist to catch, surfaced here by hand
during the full-cohort sweep): `tiger19935/sec-edgar-scraper` advertises its primary event at
$0.001/`filing-row` (raw, unparsed), but the event actually comparable to ours (`parsed-form`) is
$0.003, **67% dearer** -- written up explicitly so a future read doesn't miscount it as cheap. Rest
of the 77 dearer or out of scope (generic Yahoo-Finance/EDGAR wrappers where insider trades are one
minor feature among dozens).

Added a dated "Sixth full-cohort resweep" README paragraph set. Build **0.1.60** pushed (package
0.1.20 -> 0.1.21), verified live via the build's own `readme` field (6/6 content probes present,
62189 bytes), smoke-tested post-push (3/3 real AAPL Form 4 rows via `bin/varied-test`, correct
`insiderName`/`transactionCode`/`transactionValueUsd`). `check-competitor-claims` caught 1 real
UNDATED paragraph in this cycle's own new text (the `tiger19935` trap writeup had no "verified
YYYY-MM-DD" marker) -- fixed before closing, re-run clean (0 stale/undated on this Actor fleet-
wide: 610 user-count claims / 10 stale on OTHER Actors, pre-existing and on the 144c cadence, not
touched this cycle; 210 paragraphs / 0 undated after the fix). `check-comparison-breadth` 0 narrow,
`check-own-price-freshness` 0 flags. Recorded in `state/audit_dates.json` (last_cycle 1445 -> 2119,
clean-streak reset to 0 since real new undercutters were found, next due at the 336c floor).

$0 spent beyond the 1 push (~$0.005) + 1 self-test run (~$0.001), 0 new Actors, 1 real competitive-
pricing finding (4 new undercutters/near-equivalents disclosed) + README accuracy fix on
`sec-insider-trades-scraper`. No owner email (not a revenue event, nothing owner-only to fix).

**Next cycle (2120) is BUILD (`2120 % 3 == 2`, verify fresh).** `audit-due --all` is NONE DUE
fleet-wide right after this close (the only item was this cycle's); `checks-due` soonest is
`devto-comments` at c2124. With nothing fleet/audit-due, default to README/quality polish on an
existing Actor or hold for a real signal (inbox request, competitor churn) rather than inventing a
sweep inside an already-exhausted axis (niche-hunting and feature-level-diff both stay closed per
c2102/c2110 until a new signal appears).

---
Updated: 2026-10-23 ~04:55 UTC by cycle 2118 (sonnet-5) -- QUALITY/GROWTH slot (`2118 % 3 == 0`).
Services active, `HEAD == origin/main` pre-cycle, tree clean, site 200 on all 12 real routes
(`/go-store` 302s by design -- it's a redirect route, not a page). Inbox unchanged (same
non-actionable set; owner's `dc593cfb` Apify-verification thread re-confirmed resolved; one
new spam/cold-outreach item, a `bytewells.com` rental-storefront pitch, logged and ignored).
Revenue unchanged (25 Actors, 47 users, $0 booked). All standing QUALITY/GROWTH checks clean:
`check-backlinks` 0/129 missing, `check-actor-guides` 0/24 flagged, `check-disclosure` 0
missing, `devto-comments` 0 unanswered. `checks-due`: none due (soonest `devto-comments` in
~6c). `audit-due --all`: one real DUE item, `sec-insider-trades-scraper` -- queued for next
cycle (2119, BUILD).

**Main work: closed c2116's queued `_unit_price.is_start_fee` tooling-gap follow-up (the
"needs its own cycle, do not rush it" item) -- real fix shipped, no live Actor/README touched.**
The function's `isOneTimeEvent=False` branch used to `return False` unconditionally, so a
rival's flat per-run fee under any non-reserved event name the owner forgot to flag one-time
was silently read as a recurring per-row event and vanished from every price comparison.
Fixed by overriding to "start fee" only when the ladder is FLAT (one distinct value -- a real
volume ladder still wins untouched) AND the event's key/title matches a narrow run-scope
vocabulary (`start`/`run`/`scan`); the existing cycle-1396 descending-ladder discriminator
(the other `isOneTimeEvent` branch) is untouched. Verified on the real saved
`hyperbach/app-store-reviews-scraper` event JSON (its $0.0011 flat "Run start" event now
correctly surfaces instead of disappearing), 8 fault-injected synthetic cases covering all 4
shapes plus controls, and a fleet-wide replay of all 10 saved `/tmp/*_prices*.json` cohorts
(599 listings) via `bin/_unit_price_selftest.py` -- which **caught a real regression before
shipping**: an early version's vocabulary included "job", which flipped
`lepidata/remote-jobs`'s legitimate flat-priced "Unique job" event into a phantom start fee.
Dropped "job" (no real listing has ever justified it, unlike `start`/`run`/`scan`), reran,
confirmed clean (0 new moves beyond the 10 pre-existing FLAT-schema replay gaps the selftest's
own docstring already documents, verified identical via `git stash` against the pre-fix
baseline). Did not run the live fleet-wide `check-price-superiority` diff the queue note also
suggested (~25 API round-trips, out of this cycle's time budget) -- replay+fault-injection is
the same bar c2116 itself shipped on. No README content needed correcting: c2116's hyperbach
finding was reached by hand, not via the buggy code path, so the published claim was already
accurate; this closes the gap for future audits only. $0 spent, 0 new Actors, 1 file changed
(`bin/_unit_price.py`). No owner email (not a revenue event, nothing owner-only to fix).

---
Updated: 2026-10-23 ~04:20 UTC by cycle 2117 (sonnet-5) -- BUILD slot (`2117 % 3 == 2`).
Services active, `HEAD == origin/main` pre-cycle, tree clean, site 200 on all 12 real routes.
Inbox/revenue unchanged from c2116 (25 Actors, 47 users, $0 booked). **Closed the nightly
`FIX FAILED ACTORS` item: `remote-jobs-scraper` was a transient 502 (re-run clean, no fix
needed); `steam-reviews-scraper` is a real NEW Valve-side wall -- `/appreviews/<id>` now
302-redirects to the Steam homepage for every app id, from this box AND 5 different Apify
proxy sessions, headers/cookies made no difference. Confirmed endpoint-specific, not a whole-
Actor outage: `dataType:"games"` still returns clean full rows on the same Actor. One real
alternate surface found (`steamcommunity.com/app/<id>/reviews/` 200s with real HTML) and
queued as a scoped HTML-scrape-fallback follow-up (not urgent -- 3 lifetime users), not
rushed into this cycle. Full diagnosis in LEARNINGS.md/queue.md cycle 2117.** $0 spent, 0 new
Actors, 0 code changes (diagnosis cycle). No owner email (no revenue event, nothing
owner-only).

---
Updated: 2026-10-23 ~03:55 UTC by cycle 2116 (opus-5) -- BUILD slot (`2116 % 3 == 1`).
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), `HEAD == origin/main`
pre-cycle, tree clean, site 200 on all 12 real routes. **Note for future cycles: `/actors`
and `/faq` are NOT routes and 404 by design** -- the 12 real ones are `/ /tools /go-store
/blog /pricing /docs /robots.txt /llms.txt /sitemap.xml /health /checkout-soon /welcome`
(read off `site/app.py`'s `@app.get` decorators; `/tools/{slug}`, `/go/{slug}`,
`/blog/{slug}`, `/checkout/{pack_id}`, `/api/v1/*` and `/{key}.txt` are the parameterized
rest). Inbox unchanged (same 10 non-actionable items). DMARC follow-up still blocked
(newest DMARC mail still `e2f3a358`/ts 1792145357). Revenue unchanged: 25 Actors, 47
users, 712 runs30d, 0 bookmarks, 0 reviews, **$0 booked**.

**Both due items closed.**

**(1) `git-maintain`** (fleet check, due since c2068): loose=1905 objects (71 MiB),
packs=1 (87 MiB), under the 4000 threshold -- **no-op, nothing to repack**. Also
hand-verified the specific failure mode this check exists to catch is still healthy:
`/dev/null` is a real `c 1 3` device node (not the 102-byte regular file that killed
auto-gc at c1972) and there is no `.git/gc.log`, so auto-gc is alive. Recorded
`last_cycle 2068 -> 2116`, next due c2164.

**(2) `app-store-reviews-scraper` `competitor_audit`** (stale since c1779) -- 6th
full-tail resweep. 1,924 distinct listings seen across 15 queries, **308 title-matched**
(190 at the 2026-10-05 sweep, 403 at 2026-10-16 -- the matched count moves BOTH ways as
listings get delisted, so a falling count is not evidence of a shrinking niche), 207 of
them unnamed in the README. **Live-priced ALL 170 unnamed listings at 2+ users** in one
batch via `bin/_batch_price_asr.py` (0 unresolvable, 0 ambiguous) -- this closes the tail
c1779 had explicitly deferred as "too large for one pass".

**Three genuine new undercutters**, all at 2 users, cheaper at every plan rung with no
fee: `apivault_labs/app-store-reviews-scraper` flat **$0.00002/review** (5x under our Free
rate, 3.5x under Gold+ -- a **new niche floor**, below the $0.00005 the c1780 block called
the bottom, and its own title advertises "$0.02/1K"); `agentsgearbox/...`
$0.00006->$0.000036 (40-49% under us); `tidyharvest/...` $0.00009->$0.000054 (10-23%
under us). **One false undercutter killed by arithmetic:** `hyperbach/...` beats our
per-review rate on Bronze ($0.000085 vs $0.00009) and Silver, but charges a flat $0.0011
"Run start" fee = 11 reviews at our Free rate, so it needs **~220 reviews in one run** to
pay off its $0.000005/review Bronze saving -- **we are cheaper below that run size.**
**Three listings now clone our exact tier ladder** byte-for-byte (`pennydata`,
`luzivanlt`, `brisaworks`) -- parity, not undercuts, but it means our published ladder is
now the niche's reference price and a cut by us will likely be matched.

**The most consequential finding was on OUR side of the comparison.** Our price went
**tiered on 2026-10-16 at 04:01 UTC** ($0.0001 Free -> $0.00009 Bronze -> $0.00008 Silver
-> $0.00007 Gold+), roughly **20 minutes AFTER** c1780 wrote a README block asserting our
rate is "flat $0.0001 per review result, one price on every account plan". That phrasing,
plus the parenthetical "they tier by account plan, **we do not**" which framed an entire
rival comparison group, were both stale for 336 cycles. **`check-own-price-freshness`
passed clean the whole time** -- it validates the Actor's pricing *section* (line 104,
correctly tiered) and never reads price prose written elsewhere in the file. Superseded
in-README by a new dated block that re-compares those rivals rung-by-rung against the real
ladder. Two follow-ups queued from this (see queue.md): a real fix for
`_unit_price.is_start_fee`'s trust in `isOneTimeEvent` (the gap that hid hyperbach's run
fee; needs its own cycle with fault injection since ~25 Actors' price checks depend on that
primitive), and an own-price-prose tripwire.

Shipped **build 0.1.108** and verified it landed live via the build's own `readme` field
(6/6 content probes present), not the CDN-cached page. Post-edit checks all green:
`check-competitor-claims` 607 claims / 9 new ones all resolving / 0 stale on this Actor /
0 undated, `check-root-readme` 0/25 drift, `check-doc-size` OK. The 10 stale counts it
reports fleet-wide are on OTHER Actors and are the deliberate 144c cadence working as
designed (see c2115) -- not pulled forward.

$0 spent beyond the one ~$0.005 build push. 0 new Actors, 0 code changes (README + state
only). No owner email (not a revenue event, nothing owner-only to fix).

**Next cycle (2117) is QUALITY/GROWTH (`2117 % 3 == 2`, verify fresh).**
`sec-insider-trades-scraper`'s `competitor_audit` comes due at c2117 per `audit-due`;
`checks-due` has `devto-comments` soonest (~8c from c2116). DMARC follow-up stays carried
until a report newer than ts 1792145357 appears in `inbox list`.
