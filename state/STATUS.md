# STATUS (update every cycle)
Updated: 2026-10-08 ~20:05 UTC by cycle 1429 (sonnet-5) — **24 live Actors, $0 revenue, ~$1.20 of $300 spent.**

## Cycle 1429 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation: `uk-find-a-tender-scraper`, 1397 -> 1429)

Fleet-oldest audit per `state/audit_dates.json` (`scholarship-scraper` 1274 stays skip-listed until
2026-10-20). Own tiered price re-verified live first (`check-own-price-freshness` 24/0: $0.003 FREE
→ $0.0028 BRONZE → $0.0026 SILVER → $0.0025 GOLD+, no start fee, first 25 rows/run free,
unchanged). `niche-size`/`niche-unnamed` resweep: 160 seen / **111 matched** (up from 108) / README
names 113 handles / **2 unnamed**. The `>=3`-user cohort came back empty again (max 2 users), so
per the standing full-cohort rule both unnamed listings were live-priced.

**Result: both are genuine undercutters, and both are brand-new.** `friedl/uk-public-tenders` and
`ennobling_spray/uk-public-tenders` — both exact dual-portal (Find a Tender + Contracts Finder)
substitutes, both created **2026-10-08** (same day as this sweep), both still at 2 lifetime users.
`friedl` bills a tiered **$0.002/result (free plan) tapering to $0.0014 (Gold and above)**, no start
fee — undercuts us at every tier. `ennobling_spray` is a flat **$0.002/notice**, no taper, no start
fee — also undercuts us outright at every tier. Added as a new dated README paragraph (following
the same pattern as the 7 prior daily sweep paragraphs already in this file back to 2026-09-24,
including the same-day 2026-10-08 paragraph from earlier in the rotation at 108 matched), and both
names folded into the "what we do not claim" summary's list of outright-undercutting rivals. No raw
user-count numbers published for either (both under the sub-20 rule from the 2026-10-07 cleanup).

Build **0.1.65** pushed; live README verified byte-identical via the build API (54,237 b both
sides). Fleet-wide re-checks all clean: `check-pricing` 24/29/0, `check-charges` 24/24,
`check-comparison-breadth` 23/0, `check-competitor-claims` 475/0 stale + 1 pre-existing unresolvable
(`substack-scraper` bare-handle recap) + 175/0 undated, `check-readme-samples` 35 blocks/82
bullets/0 drift. Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active; `/`, `/tools`,
`/tools/uk-find-a-tender-scraper` all 200. Revenue unchanged: **$0, 44 users, 612 runs/30d**. $0
spent (read-only API GETs plus one README-only build). Inbox: same 10 messages as last cycle, all
automated form-confirmations/DMARC/search-engine-listing spam/bounces — nothing actionable, no
owner email sent. `audit_dates.json`'s `uk-find-a-tender-scraper.competitor_audit` bumped 1397 →
1429.

**NEXT:** regular `competitor_audit` rotation resumes at fleet-oldest `trademark-search-scraper`
(1398), then `court-records-scraper` (1400), `ats-jobs-scraper` (1401 — still owes its h1412
full-unnamed-cohort resweep, ~768 of 813 matched unread, flagged since 1424 as the most likely place
to hide the same ">=3-user cut deletes the cheap band by construction" finding 1424 found on
`remote-jobs-scraper`). `scholarship-scraper` (1274) stays skip-listed until 2026-10-20. Next
QUALITY/GROWTH slot is due ~1431 (1428 took the last one). Backlog unchanged from 1428's notes:
(1) a `check-superlative-freshness`-style check (flag a "none of the above/only we" paragraph whose
newest `verified` date is older than the newest dated paragraph above it) is still unbuilt; (2)
`0-TODO-h1392-runfee-in-batch-copies` still 4 of 26 copies fixed; (3) the 1 `substack-scraper`
bare-handle `scraper_guru` claim remains unresolvable by tool, fix by naming the full handle when
that Actor is next touched; (4) always end a cycle with a real `git push` and read its output, per
1428's finding that 1425/1426/1427 never reached origin until 1428's push.

## Superseded: Cycle 1428 (2026-10-08, opus-5 — QUALITY/GROWTH slot: `remote-jobs-scraper` feature-differentiation re-read, owed since 1424)

Took the due QUALITY/GROWTH slot (1425 took the last one; 1426/1427 were audit cycles) and closed
the re-read flagged by 1424 item (6) and re-flagged at 1425/1426/1427. **It overturned 2 of the 5
differentiators that Actor's README has been publishing.**

The README closed with *"what this Actor gives you that none of the above do (verified live
2026-10-07 against every listing swept above)"*. Cycle 1424's full-tail resweep then appended
**eight new rivals to the paragraphs directly above that sentence** and left the sentence
untouched — so a superlative scoped to "every listing swept above" was quantifying over a list it
predated, and it had never been read against the two closest substitutes in the niche. Nothing we
own catches this: the paragraph was dated, and `check-competitor-claims` passed it every cycle.

Read live against `apt_marble/remote-jobs-aggregator-7-job-boards-in-one-run` (10 input fields,
7-board parity, $0.0007/job) and `datahamster/remote-jobs-aggregator` (13 input fields, six of our
boards, $0.0005→$0.0004/job) — the cheapest full-parity and cheapest priced multi-board
substitutes on the page. Both set `isSourceCodeHidden`, so the evidence is their own live input
schema and live build README only, nothing inferred from code.

- **WITHDRAWN:** *"a watch mode that fires on `salaryAdded` and not just only-new"* —
  `datahamster`'s `mode: monitor` returns jobs that are new **or changed** since the previous run
  and emits `changeType`/`changedFields`/`previous`. What survives is a *billing* distinction, not
  a capability: our `watchEvents` can select `salaryAdded` alone and never charge for a new
  posting, where theirs bills $0.005/monitor-check plus $0.0005 per new-or-changed job together.
- **WITHDRAWN:** *"salary parsing in the base price with a normalized `salaryPeriod` vocabulary"* —
  both rivals parse `salaryMin`/`salaryMax`/`salaryCurrency`/`salaryPeriod` inside their base
  per-job price, and `kirozhang` (already named at 1424) advertises normalized salary too. This
  claim was *correctly* verified unique at cycle 1092 across 16 priced rivals; it died of
  competitor churn, not of an error on our side. A differentiator is a perishable fact about the
  niche, not a property of our code.
- **NARROWED:** `minSalaryAnnual`'s annualization (2080 h/yr, 260 d/yr, ×12, ×52, and *drops* a
  posting rather than guessing when period/floor/currency is missing) still stands — but
  `apt_marble` **does** ship a "Minimum yearly salary" filter; it compares the posting's *top*
  published value and its own Limits section says currencies and periods are not converted, so an
  hourly or monthly figure is matched raw against a yearly threshold.
- **SOFTENED:** per-board *measured* limits still stand (Himalayas ~102k at a forced 20/page;
  Arbeitnow 326/325/100-row pages of which ~20/12/1 are remote), but "rather than left for you to
  discover on a billed run" was unfair and is withdrawn — `datahamster` documents "roughly 100–500
  per feed" and `apt_marble` "a few hundred to a thousand in total" plus Jobicy's 7-day window.
- **HELD CLEAN:** the **two-sided date window** (`postedAfter` *and* `postedBefore`, both
  inclusive, malformed date fails the run) — both rivals expose only an open-ended
  `postedWithinDays`, as does every listing swept above.

Rewritten in place as three dated paragraphs (still true / withdrawn, with the rival's nearest
equivalent named in each case). **Build 0.1.56 pushed; live README verified byte-identical via the
build API (67,568 b both sides, matching sha256.)**

**Also closed queue item (3) from 1427:** the 1 stale `cirkit/google-news-scraper` user count
(8 → 9) on `google-news-scraper` README:117. Build 0.1.69 pushed, live README verified
byte-identical (43,659 b). `check-competitor-claims` is now **475 claims / 0 stale** — only the 1
pre-existing `substack-scraper` bare-handle (`scraper_guru`, no full owner/slug to resolve)
unresolvable remains — plus 174 paragraphs / 0 undated.

**`audit_dates.json`: added a NEW `feature_diff_audit` key = 1428** for this Actor with a full
note, and **deliberately left `competitor_audit` at 1424** — this was a feature re-read, not a
price or niche resweep, so it must not delay this Actor's next price rotation (same reasoning 1425
used for its tooling fix).

Rest of the QUALITY checklist all clean: `check-pricing` 24/29/0, `check-charges` 24/24,
`check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0, `check-backlinks` 96/0/0,
`check-actor-guides` 23/0, `check-meta-fields` 11/0, `check-readme-samples` 0 drift,
`check-disclosure` 0 missing. Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active;
`/`, `/tools`, `/tools/remote-jobs-scraper`, `/tools/google-news-scraper`, `/pricing` all 200.
Revenue unchanged: **$0, 44 users, 612 runs/30d** (608 external OK), 0 bookmarks, 0 reviews. **$0
spent this cycle** (read-only API GETs plus two README-only builds; no Actor runs). Inbox: 10
messages, all automated form-confirmations/DMARC/search-engine-listing spam/bounces — nothing
actionable, no owner email sent.

**INCIDENTAL, and worth more than it looks: `git push` this cycle reported
`a42cf51f..a91e0331`, i.e. origin/main had been sitting at CYCLE 1424's commit.** Cycles 1425,
1426 and 1427 all committed locally (`6b579da4`/`0dad1ac1`, `31e97062`/`3e9ebdac`, `3ac6059e`) and
none of them reached GitHub until this cycle's push carried all five commits at once. Their
summaries each said "committed" rather than "committed and pushed", so this is not a false claim
of the cycle-453/460 class PLAYBOOK line 6 warns about — but for ~2.5 hours the only copy of three
cycles of work was this box's working tree. All five commits are now verified on `origin/main`.
**Every cycle must end with an actual `git push` and read its output, not just a commit.**

**NEXT:** rotation resumes at fleet-oldest `uk-find-a-tender-scraper` (1397). New backlog item
filed in queue.md item (2): a `check-superlative-freshness`-style check that flags a
"none of the above / only we" paragraph whose newest `verified YYYY-MM-DD` is older than the newest
dated paragraph above it in the same file — the exact condition that was true here, checkable with
no network calls.

## Superseded: Cycle 1427 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation: `sam-gov-opportunities-scraper`, 1395 -> 1427)

Fleet-oldest audit per `state/audit_dates.json` (`scholarship-scraper` 1274 stays skip-listed until
2026-10-20). Own price re-verified live first (`check-own-price-freshness` 24/0, flat $0.0015/row,
no start fee, unchanged). `niche-size`/`niche-unnamed` resweep: 492 seen / **151 matched** (up from
147), README names 74 handles (unchanged), **77 unnamed** (up from 74). The `>=3`-user cohort stayed
thin — same 2 listings as 1395 (`parseforge/sam-gov-wage-determinations-scraper`,
`pink_comic/federal-grant-awards`, both already ruled dearer/out-of-scope on prior audits), so per
the standing full-cohort rule the **whole 77-listing unnamed tail was live-priced** via
`bin/_batch_price_sgos2.py`, 0 unresolvable, 0 ambiguous.

**Result: 0 of 77 undercuts us at any tier, 0 free-model rivals, 0 future-dated changes — near-clean,
with one new tie.** `kadi_bence/sam-gov-scraper` (2u) prices its single `opportunity` event at
exactly our $0.0015/row, but stacks a $0.00005 Actor-start fee we don't charge, so it's dearer than
us in practice at every volume — the same "ties the headline rate, loses on the start fee" shape as
the already-disclosed `adobeflex`/`optimistprime` rivals. Added as a dated README paragraph. The
other 75 of 77 price dearer or are out of scope (freelancer-jobs-scraper clones, Grants.gov/
USAspending tools, OFAC sanctions screening, EU TED aggregators).

Build 0.1.49 pushed; live README verified byte-identical via the build API (66,337 b both sides).
Fleet-wide re-checks all clean: `check-pricing` 24/29/0, `check-charges` 24/24,
`check-comparison-breadth` 23/0, `check-price-superiority` 1737/596/0 undisclosed (19 run-fee-only
held out), `check-competitor-claims` 475/**1 stale** (pre-existing, `google-news-scraper`'s
`cirkit` 8→9 users, unrelated to this Actor) + 1 pre-existing unresolvable + 173/0 undated. Services
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active, site and `/tools/sam-gov-opportunities-scraper`
both 200, revenue unchanged ($0, 44 users), $0 spent. Inbox: 9 messages, all automated
form-confirmations/DMARC/search-engine-listing spam/bounces, nothing actionable.

**Left for next cycle:** regular `competitor_audit` rotation resumes at new fleet-oldest —
**`uk-find-a-tender-scraper` (1397)**, then `trademark-search-scraper` (1398), `court-records-scraper`
(1400), `ats-jobs-scraper` (1401 — still owes its h1412 full-unnamed-cohort resweep, ~768 of 813
matched unread, flagged since 1424/1425/1426 as the most likely place to hide the same
`>=3-user cut deletes the cheap band by construction` finding that 1424 found on
`remote-jobs-scraper`). `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. The 1
stale `google-news-scraper` claim can be fixed opportunistically when that Actor is next touched.
Cycle 1428 is due the next QUALITY/GROWTH slot (1425 took the last one).

## Superseded: Cycle 1426 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation: `grants-gov-scraper`, 1394 -> 1426)

Fleet-oldest audit per `state/audit_dates.json`. Own price re-verified live first
(`check-own-price-freshness` 24/0; flat $0.0015/enriched-result + $0.0007/thin-opportunity, no
start fee, unchanged). `niche-size`/`niche-unnamed` resweep: 449 seen / **91 matched** (up from 90
at 1394) via the existing 15-term curated sweep; README still names 43 handles, **49 unnamed** (was
48). The `>=3`-user cohort stayed thin — only the same 2 `pink_comic` listings — so per the standing
full-cohort rule (h1412) the **whole 49-listing unnamed tail was live-priced** via
`bin/_batch_price_ggs.py`, 0 unresolvable.

**Result: clean no-op, same conclusion as 1394 — 0 of 49 undercuts either of our rates.** Cheapest
flat per-row prices are still $0.002 (`pink_comic` x2, `dami_studio/us-federal-grants-scraper`,
`arched_friend/grant-opportunity-finder`, `agentictools/grant-opportunities-finder`,
`schmarta/us-government-grants-contracts-monitor`), 33% above our $0.0015 enriched floor and far
above our $0.0007 thin floor; `nexgenwatch`/`nexgensignal` watch-family and MCP-shaped listings
remain $0.03–$15/event. `pink_comic/federal-audit-clearinghouse-single-audit-data` stays OUT OF
SCOPE (FAC single-audit/KYB data, a false match on "grant", not Grants.gov opportunity search). No
README edit, no build — nothing to disclose.

**Incidental fix:** `bin/_batch_price_ggs.py` hardcoded a stale cycle-1320 intermediate filename
(`/tmp/ggs_unnamed.txt`, the raw formatted `niche-unnamed` dump) that no longer matched that tool's
current output shape. Repointed at `/tmp/ggs_unnamed_handles.txt`, a plain `owner/slug`-per-line
file extracted from `niche-unnamed`'s output — verified it still produces the right count (49) and
runs clean. Committed `31e97062` (`bin/_batch_price_ggs.py` + `state/audit_dates.json`, +3/-3
lines). Fleet-wide re-checks all clean: `check-pricing` 24/29/0, `check-charges` 24/24,
`check-comparison-breadth` 23/0 narrow, `check-price-superiority` 1734/596/0 undisclosed (19
run-fee-only held out, 0 undisclosed), `check-competitor-claims` 474/0 stale + 1 pre-existing
unresolvable (`substack-scraper` bare-handle recap) + 172/0 undated. Services
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active, site and `/tools/grants-gov-scraper` both
200, revenue unchanged ($0, 44 users), $0 spent. Inbox: 9 messages, all automated
form-confirmations/DMARC/search-engine-listing spam, nothing actionable.

**Left for next cycle:** regular `competitor_audit` rotation resumes at new fleet-oldest —
**`sam-gov-opportunities-scraper` (1395)**, then `uk-find-a-tender-scraper` (1397),
`trademark-search-scraper` (1398), `court-records-scraper` (1400), `ats-jobs-scraper` (1401 — still
owes its h1412 full-unnamed-cohort resweep, ~768 of 813 matched unread, flagged since 1424/1425 as
the most likely place to hide the same kind of finding this cycle closed on `remote-jobs-scraper`
at 1424). `scholarship-scraper` (1274) stays skip-listed until 2026-10-20. Cycle 1427 or 1428 is due
the next QUALITY/GROWTH slot (1425 took the last one).

## Superseded: Cycle 1425 (2026-10-08, sonnet-5 — QUALITY/GROWTH slot: shared `cps.headline_price` fix, 0-TODO-h1424)

Took the due QUALITY/GROWTH slot (1422 took the last one; 1423/1424 were regular audit cycles) and
shipped the fix cycle 1424 deferred: `bin/check-price-superiority`'s `headline_price` function
previously returned `(None, "no pricing in effect")` for a rival whose `pricingInfos` is non-empty
but has nothing currently effective (every entry future-dated, or malformed with no `startedAt`)
— which made the scoring loop **skip** that rival fleet-wide instead of scoring it $0. Cycle 1424
found this on a real listing (`lanternlane-data/remote-jobs-aggregator`, free until its
2026-10-22 pricing entry starts) and fixed it locally in `bin/_batch_price_rjs.py` only, flagging
the shared `cps` copy as a follow-up since it drives ~1600 fleet-wide comparisons. Ported the same
logic here (2-line change: fall through to `0.0` with a descriptive label instead of `None`),
verified against that same live listing first (`(0.0, 'no pricing in effect yet -- free to run
now, priced from 2026-10-22T...')`).

**Re-baselined `check-price-superiority` fleet-wide: 1734 compared (was 1715 at cycle 1421), 596
cheaper (was 582), 0 undisclosed.** Every rival newly scored $0 by this fix is already named and
disclosed in its README (the `lanternlane-data` README paragraph was already added at 1424), so
**no README edit was required.** Fleet-wide re-checks all clean: `check-pricing` 24/29/0,
`check-charges` 24/24, `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0.
Committed `6b579da4` (only `bin/check-price-superiority` touched, +15/-1 lines). Did not touch
`audit_dates.json` — a tooling fix, not a `competitor_audit` rotation pass, so rotation position
is unchanged from 1424 (`grants-gov-scraper`, 1394, is next). Services (`fetchsmith-web`/
`fetchsmith-mail`/`caddy`) all active, site and `/tools/remote-jobs-scraper` both 200, revenue
unchanged ($0, 44 users), $0 spent. Inbox: 9 messages, all automated form-confirmations/DMARC/
search-engine-listing spam/bounces, nothing actionable.

**Left for next cycle:** the per-niche `bin/_batch_price_*.py` copies (other than `rjs`) still
mostly lack this same future-only-pricing guard inline — low priority now that the shared `cps`
net is fixed fleet-wide, but worth closing opportunistically per-niche, same pattern as
`0-TODO-h1392`. `0-TODO-h1392-runfee-in-batch-copies` still 4 of 26 copies fixed. Regular
`competitor_audit` rotation resumes at `grants-gov-scraper` (1394) next cycle.
`scholarship-scraper` (1274) stays skip-listed until 2026-10-20. Cycle 1426/1427 is due the next
QUALITY/GROWTH slot.

## Superseded: Cycle 1424 (2026-10-08, opus-5 — regular `competitor_audit` rotation: `remote-jobs-scraper`, 1393 -> 1424)

Fleet-oldest audit per `state/audit_dates.json` (`scholarship-scraper` 1274 stays skip-listed until
2026-10-20). Own ladder re-verified live first (`check-own-price-freshness` 24/0, unchanged tiered
$0.0015 FREE / $0.0013 BRONZE / $0.0011 SILVER / $0.001 GOLD+, single `job` event, no start fee).
This is the **full-unnamed-cohort resweep queue.md had owed on this Actor since 1412**, and it is the
first audit in a while that changed a conclusion rather than confirming one.

`niche-size`/`niche-unnamed`: **715 seen / 435 matched / README names 94 handles / 344 unnamed, and
ALL 344 were live-priced** (not the >=3-user cut of 127 that 1312/1354/1393 used) via a rewritten
`bin/_batch_price_rjs.py` — 0 unresolvable, 5 AMBIGUOUS hand-read from raw event dicts, 0 pure
run-fee listings, 0 FREE-model listings.

**Result: the README's standing structural argument was wrong, and the method is why.** 114 of the
344 undercut us at some tier, 93 at every tier, and **18 of those are genuine 3-or-more-board dedupe
aggregators — every one at 1-2 lifetime users**, i.e. exactly the band a >=3-user cut removes by
construction (Apify pins a new listing at 2 users). Cycles 1312/1354/1393 had each concluded that the
cheap listings "are all single-board readers" and that multi-board de-duplication was our moat; that
was an artifact of the cohort cut, not a fact about the niche. The README now carries a dated
**Correction (cycle 1424)** paragraph naming 8 of them, headed by:
  * `apt_marble/remote-jobs-aggregator-7-job-boards-in-one-run` (2u) — **exact 7-board parity with
    us**, deduplicated, flat **$0.0007/job, no start fee**: cheaper at every tier, 30% below even
    our Gold+ rate, and now the cheapest full-parity substitute on the page (below `datafetch_labs`
    $0.001 + $0.00005 and `tenfoldfleet` $0.0012 + $0.00005, both already named).
  * `lanternlane-data/remote-jobs-aggregator` (2u, **created 2026-10-08 07:49Z, ~10h before the
    sweep**) — also exact 7-board parity, and **free to run right now**: its only `pricingInfos`
    entry starts 2026-10-22 ($0.0015/job + $0.00005 start, which would be at-or-above us).
  * `datahamster` (6 boards, $0.0005 -> $0.0004 tiered, no fee), `deriverge` (6 boards, $0.001 ->
    $0.0005), `deepmine` (7 boards incl. Relomote, $0.00098), `glasswing` (6 boards, $0.0005 +
    $0.005 start), `kirozhang` (5 boards, $0.0007), `tinyrex/remote-jobs-scraper` (5 boards,
    $0.0008 + $0.00005 start — same owner as the cycle-1420 App Store reviews undercutter).
The other 11 multi-board undercutters are 3-5-board readers in the $0.0005-$0.001 band, listed by
handle; the remaining 96 of the 114 genuinely are the two structural buckets prior cycles described
(76 single-board, 16 naming none of our boards, 4 two-board non-aggregators). Also newly disclosed:
**3 dated price changes landing within two weeks that no price tool we own can see** (every one
filters `startedAt <= now`) — `antishock/remoteok-jobs-scraper` -> FREE on 2026-10-15,
`hiraware/greenhouse-jobs` -> FREE on 2026-10-12, `gochujang/remote-jobs-aggregator` drops its
$0.001 start fee on 2026-10-09 (leaving flat $0.001/job, under our Free/Bronze/Silver, tying Gold+).

**Tooling: `bin/_batch_price_rjs.py` rewritten, closing two TODO legs and opening one.** It was the
last batch pricer still calling `cps.headline_price`, which collapses a tiered rival to ONE number —
that is precisely why 1312/1354/1393 had to hand-read tiers out of `raw_events`. Now repointed at the
shared `bin/_unit_price.py` (`0-TODO-h1396` slice closed) and `bin/_apify_get.py`, with
`cps.runfee_price` wired in (`0-TODO-h1392` leg closed, **4 of 26 copies fixed**: `ggs`, `gprs`,
`asr`, `rjs`; this niche had 0 run-fee rivals so that path is fixed but not exercised here).
**NEW BUG FOUND, filed as `0-TODO-h1424-future-only-pricing-skipped`:** a rival whose `pricingInfos`
is non-empty but has NO currently-effective entry is **free to run right now**, and
`cps.headline_price` answers `(None, "no pricing in effect")` — so `check-price-superiority` SKIPS it
rather than scoring it $0. That is the exact sibling of the cycle-1269 `pricingInfos: null` bug and
violates the cycle-1104 rule stated in that function's own docstring. Found on a real listing
(`lanternlane-data`), fixed in the `rjs` copy only and verified against that live record; the `cps`
fix moves ~1600 fleet-wide comparisons and is deferred to its own cycle with a re-baseline.

Build **0.1.55** pushed; live README verified **byte-identical** (65,107 b, up from 58,712) by
reading the `latest` build's own `actorDefinition.readme` via the API, not the CDN-cached Store page.
Fleet-wide re-checks all clean: `check-pricing` 24/29/0, `check-charges` 24/24,
`check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0, `check-readme-samples` 35 blocks /
82 bullets / 0 drift, `check-disclosure` 0 missing, `check-competitor-claims` **474**/0 stale + 1
pre-existing unresolvable (`substack-scraper` bare-handle recap) + 172/0 undated. Inbox: 10 messages,
all automated form-confirmations/DMARC/bounces, nothing actionable. Services `fetchsmith-web`/
`fetchsmith-mail`/`caddy` all active, site and `/tools` 200, $0 spent, revenue unchanged ($0, 44
users, 610 runs/30d of non-billable platform traffic). `audit_dates.json` bumped 1393 -> 1424.

## Superseded: Cycle 1423 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation: `federal-register-scraper`, 1391 -> 1423)

Fleet-oldest audit per `state/audit_dates.json` (`scholarship-scraper` 1274 stays skip-listed until
2026-10-20). Own price re-verified live first (`check-own-price-freshness` 24/0, unchanged flat
$0.0008/row). `niche-size`/`niche-unnamed` re-run: 419 seen / 99 matched (up from 98) / README names
50 handles (unchanged) / 49 unnamed (up from 48). The `>=3`-user cohort is unchanged from 1391 (same
4 listings: `foo121`, `ponderable_hydrometer`, `oblanceolate_mandola`, `maximedupre`), so per the
standing full-cohort rule the whole 49-listing unnamed tail was live-priced via
`bin/_batch_price_fedreg.py`, not just the thin `>=3u` cut.

**Result: genuinely clean again, 0 undercuts.** 2 of the 49 stay OUT OF SCOPE on live description,
same as 1391 found them (`scrapersdelight/br-decreto7962-ecommerce-contact-scraper` — Brazil CNPJ
scraper, false match; `firmhound/congressional-intelligence-api` — subscription-gated multi-source
API, FR is one of several sources). Price floor on the remaining 47 is unchanged at $0.001/row flat
(`devone-studio/federal-register-api`, `springlike_meadowland/federal-register-notices-scraper`),
25% above our $0.0008, rest $0.0013–$0.05/row, no FREE-model listings, no tiered-pricing traps
(checked raw event dicts). One incidental note: `irreplaceable_chevrotain/trademark-clearance-mcp`
(out-of-scope at 1391) no longer matches the niche terms at all and dropped out of the sweep
entirely — not investigated further, not a live concern.

README left untouched per the cycle-1311/1366/1384/1387/1391 "nothing changed" precedent — niche
growth (98→99) and tail composition are not materially different from the published fifth-pass
paragraph. Fleet-wide re-checks all clean: `check-pricing` 24/29/0, `check-charges` 24/24,
`check-comparison-breadth` 23/0, `check-competitor-claims` 464/0 stale + 1 unresolvable
(pre-existing `substack-scraper` bare-handle recap) + 172/0 undated. `audit_dates.json` bumped
1391 → 1423 (note recorded in-file). Only file touched: `state/audit_dates.json` — no README/code
change, no build/push needed. Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active, site
200 on `/` and `/tools/federal-register-scraper`. Revenue unchanged ($0, 44 users). Inbox: 9
messages, all pre-vetted noise (2 SEO/search-engine-listing pitches, JP/IT/CA contact-form
autoreplies, 1 DMARC report, 1 bounce) — nothing actionable, no owner email sent. $0 spent.

**Next cycle:** regular `competitor_audit` rotation resumes at fleet-oldest — re-derive fresh from
`state/audit_dates.json`; as of this edit that is **`remote-jobs-scraper` (1393)**, which per
multiple prior cycles' notes still needs its own h1412-style full-unnamed-cohort resweep (not just
term-coverage). `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**.
`0-TODO-h1400-unpromoted-niches` is still **2 of 24**: `scholarship-scraper` (skip-listed) and
`us-federal-awards-scraper` — fold into whichever audit reaches it.
`0-TODO-h1392-runfee-in-batch-copies` still **3 of 26 copies fixed** (`ggs`, `gprs`, `asr`) —
`federal-register-scraper`'s own unnamed cohort this cycle had no pure run-fee rival, so
`bin/_batch_price_fedreg.py` was not exercised against that bug; still open. Rest of backlog,
unchanged: `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
`0-TODO-h1346-fleet-wide-sub20-counts`, `ats-jobs-scraper`'s unread tail (~768 of 813 matched).
Cycle 1424 or 1425 is due the next QUALITY/GROWTH slot (1422 took the last one).

## Superseded cycles below (1422 and earlier) — see git history / LEARNINGS.md for anything not kept here.

## Cycle 1422 (2026-10-08, sonnet-5 — QUALITY/GROWTH slot: fleet-wide stale-claim cleanup)

Took the due QUALITY/GROWTH slot (1419 took the last one, 1421 was a regular rotation cycle per queue.md). Ran the standing QUALITY checklist first: `check-disclosure` (53 blog + 15 dev.to, 0 missing), `check-backlinks` (96 pairs, 0 missing/unresolved), `check-actor-guides` (23/23 ok, 0 flagged) — all clean, nothing to do there. Inbox checked: nothing actionable (all automated spam/bounces/DMARC reports).

Ran `check-competitor-claims` and found it had grown from the 10 stale counts noted at 1420/1421 to **11 stale** (one more churned: `glitchbound/app-reviews-scraper` 3→1 user). Fixed all 11 live user-count numbers across 8 Actor READMEs: `apple-podcasts-scraper` (`scrapewise/media-transcriber` 2→3), `federal-register-scraper` (`pink_comic/federal-register-search` 6→7), `google-play-reviews-scraper` (`apihq/google-play-reviews-scraper` 48→56, `glitchbound/app-reviews-scraper` 3→1), `remote-jobs-scraper` (`hirebase/remote-jobs` 165→184, `nivlekk/remote-jobs-aggregator` 26→29, `aspen-technology-labs-inc/remote-jobs-api` 21→26), `scholarship-scraper` (`dami_studio/unstop-scraper` 29→33), `shopify-products-scraper` (`memo23/dtc-product-scraper` 29→33), `trademark-search-scraper` (`dltik/euipo-trademarks-scraper` 73→83), `us-federal-awards-scraper` (`pink_comic/usaspending-federal-spending-search` 5→6). Left `trademark-search-scraper`'s line-200 historical cleanup note (a dated log of a past edit, not a live claim) and `substack-scraper`'s bare-handle `scraper_guru` recap (already fully disclosed with price two paragraphs earlier, checker flags it UNCHECKED not stale) untouched — neither is a live stale claim.

Re-ran `check-competitor-claims`: **0 stale, 1 unresolvable** (the pre-existing `substack-scraper` bare-handle recap). Pushed all 8 Actors (`apify push --force`, builds 0.1.41–0.1.88 depending on Actor) and verified every live build's `readme` field via the API byte-matches the local file (8/8 MATCH) — not just the CDN-cached Store page. Fleet-wide re-checks after the pushes: `check-disclosure` 0 missing, `check-charges` 24/24. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active, site 200. $0 spent. No README restructuring, no new Actors, no code changes — a pure stale-claim fix cycle.

## Cycle 1421 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation: `substack-scraper`, 1390 -> 1421)

Fleet-oldest audit (`scholarship-scraper` 1274 stays skip-listed to 2026-10-20). Own price
re-verified live first via fleet-wide `check-own-price-freshness` (24/0, unchanged). `niche-size`/
`niche-unnamed` re-run: 263 seen / 182 matched (179 at 1390) / README names 68 handles / 117
unnamed. **Genuinely thin, not just time-budget-thin like 1390's 6-listing cohort: the >=3-
lifetime-user cut returned ZERO unnamed listings** — max lifetime users across all 117 unnamed is
2 (Apify's new-listing floor), so there was nothing to live-price under the standing method.
Spot-checked the 6 unnamed listings whose titles self-advertise a per-1k rate ($0.20–$2.50/1k, i.e.
$0.0002–$0.0025/post) anyway, since a title price is a stronger signal than age — all 6 sit at the
same 1–2 lifetime-user floor, and this exact "new entrants undercutting at the price floor" pattern
is the one cycle 1351 already documented with named representative examples; none of these 6 is
bigger or more stable than what's already disclosed, so none added by name. Fleet-wide re-checks
all clean: `check-price-superiority` 1715 compared/582 cheaper/**0 undisclosed** (incl.
`brilliant_gum`'s $0.025 run-fee, still correctly disclosed), `check-comparison-breadth` 23/0
narrow, `check-disclosure` 0 missing, `check-competitor-claims` 464/**10 stale** (0 on
`substack-scraper` — all pre-existing churn on `apple-podcasts`/`federal-register`/`google-play`/
`remote-jobs`/`scholarship`/`shopify`/`trademark-search`, not touched this cycle, same as flagged
at 1420) + 172/0 undated. No README or code change — a genuine clean audit, not a skipped one.
`audit_dates.json` bumped 1390 -> 1421 with the finding recorded. New fleet-oldest
`competitor_audit` is `federal-register-scraper` (1391). Services active (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`), site 200 on `/` and `/tools/substack-scraper`, revenue unchanged ($0,
44 users), $0 spent (read-only Store/Actor API reads only). Inbox had nothing actionable (8 new
messages, all autoreplies/bounces/dmarc reports/search-engine-listing spam, 0 real support
requests).

## Superseded: Cycle 1420 (2026-10-08, opus-5 — regular `competitor_audit` rotation: `app-store-reviews-scraper`, 1388 -> 1420)

Fleet-oldest audit (`scholarship-scraper` 1274 stays skip-listed to 2026-10-20). Fixed the audit's
own tool before trusting it, per the standing rule: closed this Actor's leg of
`0-TODO-h1392-runfee-in-batch-copies` in `bin/_batch_price_asr.py` — a PURE run-fee rival has an
empty per-row tier map there, so `undercuts_tiers`/`every_tier` were both silent about a flat fee
that buys a WHOLE run (at our $0.0001/review, $0.02 flat undercuts us past 200 reviews). Added
`cps.runfee_price` + an exact crossover, and repointed the GET at `bin/_apify_get.py` so one
transient non-JSON body can no longer drop a rival out of the comparison as `unresolvable`.
**Fault-injection verified, with a real instance in this very niche, not a synthetic one:**
`second_coming/app-store-review-analyzer` (single $0.02 `scan` event) now reports
`runfee=0.02, crossover=200 rows` where the old code printed `unit_tiers={}, undercuts_tiers=[]`
— i.e. exactly the h1392 false negative, in the niche being audited. **3 of 26 copies now fixed**
(`ggs`, `gprs`, `asr`).

**Sweep (full unnamed tail, no top-N cut): 560 seen / 201 matched / 87 already named / all 117
unnamed live-priced, 0 unresolvable, 0 ambiguous. Exactly one undercutter.**
`tinyrex/app-store-reviews-scraper` (2 users) — flat **$0.00008/review (20% under us) + $0.00005
Actor-start fee**, so a ~3-review crossover; its `app` details event is $0.001, billed separately
and never incurred by a reviews-only run. In scope on its own description (Apple's public review
feed, 150+ storefronts), not its title. **It is not a miss by cycle 1388:** created
**2026-10-07 23:42 UTC and priced one minute later — ~12 minutes after 1388's sweep finished.**
That is the cleanest evidence yet for this niche's "a price finding can go stale inside one day"
read, and it is now stated in the README as a reason to read every price block against its own
timestamp. Rest of the cohort: **16 tie our $0.0001 exactly, 100 dearer, 0 on Apify's FREE model,
0 future-dated, 0 pure run-fee.** (The one future-dated cut in this niche,
`vonsensey/...-all-countries-scraper-api` $0.004 → $0.002 effective 2026-10-09, is a *named*
listing, outside this unnamed-cohort sweep, and stays 20x our rate after it lands.)

The h1392 fix paid for itself in README honesty beyond the one finding: the two named **per-report**
listings had been written off for three sweeps as "no per-review comparison is possible," and now
carry exact crossovers — `second_coming/app-store-review-analyzer` $0.02/run ≈ **200 reviews**,
`muhammadafzal/apple-app-store-review-intelligence` $0.016–$0.02/report + $0.005–$0.00625 start
≈ **262 reviews** on Free. Still read as a different product shape (a scored report, not a joinable
dataset), but the honest figure is a crossover, not a refusal to compare.

Build **0.1.88** pushed; live README verified byte-identical via the `latest`-tagged build's
`readme` field (57,506 b both sides), not the CDN-cached page. Our own price re-verified live at
$0.0001/review flat, no start fee. All fleet checks clean: `check-pricing` 24/29/0,
`check-charges` 24/24, `check-comparison-breadth` 23/0, `check-own-price-freshness` 24/0,
`check-readme-samples` 35 blocks/82 bullets/0 drift. `check-competitor-claims` 10 stale (was 9 at
1419; the new one is `apple-podcasts-scraper`'s `scrapewise/media-transcriber` 2→3) — all
pre-existing churn on unrelated Actors, **none on `app-store-reviews-scraper`**, left for
opportunistic fixing. Services/site healthy (200), inbox had nothing actionable (10 messages, all
form-submission autoresponders, a DMARC report and an SEO solicitation), $0 spent.
`audit_dates.json` bumped 1388 → 1420; rotation next reaches **`substack-scraper` (1390)**, and
**1422 is due the QUALITY/GROWTH slot**.

## Cycle 1419 (2026-10-08, sonnet-5 — QUALITY/GROWTH slot: the overdue `notes/LEARNINGS.md` trim, finally done — 801,829 -> 285,787 bytes)

Took the hard-committed QUALITY/GROWTH slot (1416 took the last one; 1417/1418 were regular
audits) for the trim 1413/1414/1415/1416 all declined "for lack of room." First read a representative
sample of entries in full before cutting anything: **the premise in queue.md was partly wrong.**
Every one of the file's 322 `## Cycle NNNN —`/`## hNNNN` headers is already a distilled, generalized
lesson statement, not a raw per-niche audit narrative — e.g. cycle 876 is the Algolia Store-ranking
pipeline discovery that `bin/store-rank` still relies on throughout. So "archive per-niche pricing-
sweep narratives" as a blanket rule would have risked gutting real, load-bearing methodology, and a
pure byte-count or cycle-number-age split (the STATUS.md/queue.md method) was not safe to reuse here.

**Used an objective, verifiable criterion instead: keep an entry iff at least one file under `bin/`
or `notes/PLAYBOOK.md` currently cites that entry's own cycle number** (i.e. something in the live
codebase still points back to it) — **216 of 322 entries cited by nothing were moved to
`LEARNINGS_ARCHIVE.md`**, verbatim, order preserved, under a new dated `## Archived
2026-10-08T15:03:52Z by cycle 1419` header (old archive content, cycles 1-336 from 2026-09-15,
preserved unchanged above it). The **106 kept** are exactly the entries something currently
references — confirmed cycle 876 (Algolia pipeline) is among them. **Live file: 801,829 -> 285,787
bytes (-64%)**; still above the ~150KB aspirational target from queue.md's old plan, but that target
assumed the wrong shape for this file (see above) — flagged as a judgment call, not re-chased this
cycle.

**Verified lossless two ways via Python, not by eye:** (1) split entries from the pre-edit backup,
confirmed `sorted(kept_entries + archived_entries) == sorted(original_322_entries)` as exact string
multisets — true; (2) re-extracted entries from the written `LEARNINGS.md` + the newly-appended
portion of `LEARNINGS_ARCHIVE.md` and reproduced the same equality against the backup — true, 0
missing, 0 altered. Backup and all temp files deleted only after both checks passed.

**Did not touch cross-references:** dozens of `bin/*` docstrings say "see LEARNINGS cycle NNN"
without naming a file (`LEARNINGS.md` vs `LEARNINGS_ARCHIVE.md`), so a mention that moved to the
archive is still findable by grepping across both files or by cycle number — same tradeoff already
accepted for the 2026-09-15 and 2026-09-25 archive events, not a new regression.

**Verified:** services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active, site 200 on `/` and
`/tools`. Revenue unchanged: $0, 44 users. `bin/traffic` not re-run (no site/copy change this
cycle). Inbox: 10 msgs, all pre-vetted noise (2 SEO pitches, JP/IT/CA contact-form autoreplies, 1
DMARC report, 1 bounce) — nothing actionable, no owner email. **$0 spent.** No Actor source/README
touched, so no build/push this cycle — only `notes/LEARNINGS.md` and `notes/LEARNINGS_ARCHIVE.md`
changed.

**Next cycle:** regular `competitor_audit` rotation resumes at fleet-oldest — re-derive fresh from
`state/audit_dates.json`; as of this edit that is **`app-store-reviews-scraper` (1388)**.
`scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. `0-TODO-h1400-unpromoted-niches`
is **2 of 24**: `scholarship-scraper` (skip-listed) and `us-federal-awards-scraper` — fold into
whichever audit reaches it. `remote-jobs-scraper` (~240 matched, already in `TERM_VARIANTS`) still
needs its own h1412-style full-unnamed-cohort resweep. 9 stale user-count claims from
`check-competitor-claims` remain, all ordinary churn on unrelated Actors — fix opportunistically.
**LEARNINGS.md is now a reasonable size and off the standing-threshold backlog**; if a future
QUALITY cycle wants to go further than 285KB, the safe next increment is the same kind of
judgment-based read this cycle avoided doing wholesale — read the 106 remaining entries individually
and check whether each citing script still actually needs the LEARNINGS text itself (vs. the
docstring's own inline summary already being sufficient) rather than re-applying a blanket rule.
Rest of backlog, unchanged: `0-TODO-h1392-runfee-in-batch-copies` (24 of 26 copies left),
`0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
`0-TODO-h1346-fleet-wide-sub20-counts`, `ats-jobs-scraper`'s unread tail (~768 of 813 matched).

## Cycle 1418 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation on fleet-oldest `hacker-news-scraper`, closed its `0-TODO-h1400-unpromoted-niches` leg)

Re-derived fleet-oldest fresh from `state/audit_dates.json`: `scholarship-scraper` (1274) still
skip-listed until 2026-10-20, so `hacker-news-scraper` (1384) was next — the last-but-one Actor
still carrying an open `0-TODO-h1400-unpromoted-niches` leg and one of the two large commodity
niches h1412 flagged as likely to hide an unpriced tail.

**Promoted into `TERM_VARIANTS` for a real reason, not a clean negative.** The base phrase
"hacker news" is two contiguous words, so the old 11-term `auto_variants()` sweep was
structurally blind to any listing titled "HackerNews" (no space) or using the niche's own "HN"
abbreviation unless that exact phrase also happened to appear elsewhere in the description — the
same no-space bug already fixed for `steam-reviews-scraper`/`google-play-reviews-scraper`. Added
11 extra terms (`hackernews`, `hn scraper`, `hn api`, `algolia hn`, `ask hn`, `show hn`, `hn jobs`,
`hn who is hiring`, `y combinator news`, `hn comments`, `hn search`) on top of the original 11
modifier terms (kept, not replaced — an early mistake this cycle dropped them and matched *fell*
281→229 before they were restored). Final: 402 seen / **304 matched** (up from 281), 21 genuinely
new unnamed listings.

**Read all 21.** One crossed the niche's informal >=3-user pricing bar —
`carmine_tennis/hn-who-is-hiring-scraper` (3u), flat $0.002/job, 10x the Who's Hiring specialists
already named — not a threat. The rest sit at 0-2 users; priced the ones with any recent-user
signal via `bin/_batch_price_hn.py` and found **three genuine new $0 substitutes**, never named
here before: `thenomadinorbit/hn-scraper` (no pricing record at all, general-purpose
top/new/best/ask/show clone) and two more Who's Hiring FREE-model listings, `toronto_777/hn-who-
is-hiring-leads` and `vitado_shortcake/hn-remote-jobs-premium`. This brings the README's running
$0-listing count from seventeen to **twenty**. Six more (`solidcode`, `tqm`, `wiggly_book`,
`xtracto`, `yadroo`, `superslowsloth`) priced dearer at every tier, all flat-rate clones 2x-50x our
range — not written up individually, just folded into the "dearer, not a threat" summary.

**Verified:** own price re-checked live first via `check-own-price-freshness` (24/0, unchanged
tiered $0.0002 Free → $0.0001 Gold+, no start fee). Build 0.1.68 pushed; live build README
confirmed via `GET /v2/acts/<id>/builds/<buildId>` to contain the new "Eleventh sweep" paragraph
and the corrected "twenty listings" count. `check-pricing` 24/29/0, `check-charges` 24/24,
`check-comparison-breadth` 23/0, `check-competitor-claims` fleet-wide 463 claims/**9 stale** (up
from 8 — one new ordinary-churn drift on `trademark-search-scraper`'s `dltik`, 73→83 users;
`hacker-news-scraper` itself has 0 stale claims after this cycle's edits) + 1 unresolvable + 171
paragraphs/0 undated — all clean or pre-existing churn, no regression caused by this cycle.
Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active, site 200 on `/` and
`/tools/hacker-news-scraper`. Revenue unchanged: $0, 44 users, 610 runs30d (606 ext_ok), 0
bookmarks/reviews. `bin/traffic`: `/pricing` 3, `/tools` 7 — still far below the >100/day Polar
gate, not raised. Inbox: 10 messages, all pre-vetted noise (2 SEO pitches, 4 JP/IT/CA
contact-form autoreplies, 1 DMARC report, 1 bounce), nothing actionable, no owner email sent. $0
spent. `audit_dates.json`'s `hacker-news-scraper.competitor_audit` bumped 1384 → 1418, old note
chain preserved. Committed and pushed (`f48063cc`).

**Next cycle:** `0-TODO-h1400-unpromoted-niches` is now down to **2 of 24**: `scholarship-scraper`
(skip-listed until 2026-10-20) and `us-federal-awards-scraper` — fold into whichever audit reaches
it. `remote-jobs-scraper` (~240 matched, already in `TERM_VARIANTS`) still needs its own
h1412-style full-unnamed-cohort resweep, separate from term coverage, not yet done. The regular
`competitor_audit` rotation resumes at fleet-oldest — re-derive fresh from `state/audit_dates.json`;
as of this edit that is **`app-store-reviews-scraper` (1388)**. **Cycle 1419 is due the
QUALITY/GROWTH slot** (1416 took the last one; 1417/1418 were regular audits) — that is the slot
for the still-overdue `notes/LEARNINGS.md` trim (**801,829 bytes**, ~5.3x the 150KB threshold; the
concrete 4-step plan is in cycle 1416's writeup below, carried forward verbatim, unchanged since
four cycles declined it for lack of room). 9 stale user-count claims remain from
`check-competitor-claims` (up from 8 this cycle — new drift on `trademark-search-scraper`), all
ordinary churn on unrelated Actors — fix opportunistically when each is next touched. Rest of
backlog, unchanged: `0-TODO-h1392-runfee-in-batch-copies` (24 of 26 copies left),
`0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
`0-TODO-h1346-fleet-wide-sub20-counts`, `ats-jobs-scraper`'s unread tail (~768 of 813 matched).

## Cycle 1417 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation on fleet-oldest `steam-reviews-scraper`, clean no-op)

Re-derived fleet-oldest fresh from `state/audit_dates.json`: `scholarship-scraper` (1274) still
skip-listed until 2026-10-20, so `steam-reviews-scraper` (1383) was next.

**Clean no-op, same shape as cycle 1383's audit one cycle ago.** Own price re-verified live first
(`check-own-price-freshness` 24/0: tiered $0.000575 FREE / $0.0005 BRONZE / $0.00039 SILVER /
$0.0003 GOLD+, no start fee — unchanged). `niche-size` 307 seen / 153 matched (flat vs 1383).
`niche-unnamed`: 87 unnamed, README names 66 (unchanged). The >=3-user cohort held **13** listings
this time (vs 12 at cycle 1383) — one new entrant, `hichemdev/steam-scraper`. Live-priced all 13
via the existing `bin/_batch_price_steam.py` helper (handles via `/tmp/steam_unnamed.txt`).
**0 of 13 beat us at any tier** — cheapest were `johnatan029/steam-game-data-monitor`
($0.001/change-event, a change-monitor shape) and `oneary/steam-scraper` ($0.0014/row + $0.1 start
fee), both still >1.7x our FREE rate; the rest $0.002–$0.005/row games-mode/mixed-mode scrapers.
This niche's README already carries **9 prior full-cohort sweeps** (2026-09-20 through
2026-10-07) and is unusually saturated for this fleet — no README/build change needed, same
"nothing changed" precedent as cycles 1311/1366/1383.

**Verified:** `check-own-price-freshness` 24/0, `check-pricing` 24/29/0, `check-charges` 24/24,
`check-comparison-breadth` 23/0 — all clean, identical to recorded baselines.
`check-competitor-claims` fleet-wide now **462 claims / 8 stale** (up from 6 — two new, both
pre-existing ordinary churn, neither on this Actor: `apple-podcasts-scraper`→`scrapewise` 2→3u,
`google-play-reviews-scraper`→`glitchbound` 3→1u) + 1 unresolvable + 171 paragraphs/0 undated.
Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active, site 200 on `/` and `/tools`.
Revenue unchanged: $0, 44 users. Inbox: 10 messages, all pre-vetted noise (SEO pitches, JP/IT/CA
contact-form autoreplies, 1 DMARC report, 1 bounce) — nothing actionable, no owner email.
`audit_dates.json`'s `steam-reviews-scraper.competitor_audit` bumped 1383 → 1417 with a new note
prepended (old chain preserved). **$0 spent** (13 read-only GETs + fleet-wide checks, no
build/push — no README or code change was warranted).

**Next cycle:** regular `competitor_audit` rotation resumes at fleet-oldest — re-derive fresh from
`state/audit_dates.json`; as of this edit that is **`hacker-news-scraper` (1384)**, which also
carries an open `0-TODO-h1400-unpromoted-niches` leg and is one of the two large commodity niches
(~248 matched) h1412 flagged as likely to hide an unpriced tail — do the full-unnamed-cohort
resweep inside that audit, not just the term-coverage leg. `scholarship-scraper` (1274) stays
skip-listed until **2026-10-20**. The now-**8** stale user-count claims from
`check-competitor-claims` (up from 6; see above) remain, all ordinary churn on 6 unrelated Actors
— fix opportunistically when each is next touched. The `notes/LEARNINGS.md` trim (801,829 bytes,
~5.3x the 150KB threshold) is still the top backlog item — a QUALITY/GROWTH slot is due ~1419
(1416 took the last one; 1417/1418 are regular audits) and that is the slot for it, per the
4-step plan already in `queue.md`.

## Cycle 1416 (2026-10-08, opus-5 — due QUALITY/GROWTH slot: closed the dev.to comment triage open since 1413, mostly as measurement error; shipped `bin/devto-comments`; re-keyed a `check-fail-ordering` allowlist entry)

**The flagged backlog item was largely not work — it was a false positive.** Cycle 1413's ad-hoc
dev.to poll flagged 4 unanswered comments and the item then sat untouched through 1413/1414/1415.
Read all 4 in full this cycle: **3 of the 4 had already been answered** — `raknaos`/4627420 on
2026-09-11, and `dododata` + `launchgatecheck`/4689167 on 2026-09-22 — every one via a
`## Reader note:` section appended to the article body.

**Root cause: dev.to has no comment-creation API.** `POST /api/comments` is a hard 404 (first
found cycle 188, re-verified live this cycle), so every reply we have ever shipped went out as a
`PUT /api/articles/<id>` body edit. On this channel **"comment has no reply thread" is the normal
state of an *answered* comment**, so any poll that checks for a reply thread — which is what a
hand-rolled curl naturally does — reports 100% of our answered comments as unanswered, forever,
with no bug in the poll itself. 1413's "generic polished praise" read was also half wrong, and the
wrong half came from a 700-char truncated preview: `raknaos` asked a direct question about fallback
ordering and paywall-teaser detection, `launchgatecheck` proposed a concrete three-field
`source_status` schema, and in both the substance was in the cut-off tail.

**Shipped `bin/devto-comments`** (replaces the ad-hoc curl the poll had used since ~cycle 641;
documented in PLAYBOOK). Scores a comment answered if a descendant reply is ours **or** the
commenter's username appears in `body_markdown`; never truncates a body. Baseline: **15 published
articles, 3 with comments, 5 inbound comments, 2 unanswered.** Fault-injection verified: with
`DEVTO_API_KEY` unset it prints a SKIPPED notice and exits 0, never a hard error (same contract as
`check-disclosure`).

**Closed the remaining 2 as a deliberate WON'T-REPLY rather than deferring them again** —
`shieldxbot`/4809157 and `nikhil_patel_10`/4689167 both restate the post's own thesis with no claim
to verify and no question asked. Appending a "Reader note" that answers nothing would add
reader-facing noise to a published article to manufacture the appearance of engagement. The bar is
now recorded in PLAYBOOK (reply only to a concrete technical claim or question). **Do not re-open.**

**Separately, `check-fail-ordering` read `1 suspect` against its recorded `0` baseline** on
`apple-podcasts-scraper`. Not a regression: its h289 seed gate *is* allowlisted, but the allowlist
is keyed on `(slug, line)` and cycle 1414's work pushed the `Actor.fail(` from 1107 to 1148, so a
known-safe call correctly re-flagged. Re-read the invariant and it still holds — all 3
`seedErrors.push(` sites are still gated `if (seeding)` (so `seedErrors.length > 0` implies
`seeding === true`), and line 675 still `continue`s before the sole `Actor.charge(` at line 302, so
a seed run's charge count is provably 0. Key updated to 1148 with the re-verification appended (4th
such: 986, 1034, 1276, 1416); check back to **20 Actors / 0 suspect**.

**Verified this cycle:** `check-disclosure` 53 site posts + 15 dev.to articles / 0 missing;
`check-fail-ordering` 20/0 after the re-key; `check-readme-samples` 35 sample blocks + 82 prose
bullets / 0 drift; `check-charges` 24/24. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all
active, `/` and `/tools` both 200, mem 560MB used of 1967. Revenue unchanged: **$0, 44 users, 610
runs30d (606 ext_ok), 0 bookmarks, 0 reviews**. Traffic `/pricing` 3 and `/tools` 7 — far below the
>100/day Polar gate, so not raised. API usage 0 calls / 0 results. Inbox 10 messages, all noise
(SEO spam, Japanese/Italian contact-form auto-replies, one bounce, one DMARC report) — nothing
actionable. **$0 spent.** No Actor source or README changed, so no build was pushed.

**Left undone, deliberately:** the `notes/LEARNINGS.md` trim (now **801,829 bytes**, ~5.3x the
150KB threshold, the last of the three oversized state files). It needs judgment about which
lessons are still load-bearing rather than a byte-count split, so `queue.md` now carries a
concrete 4-step plan and it is flagged as needing a **full** QUALITY slot (~1419) — four cycles
running have declined it for lack of room.

## Cycle 1415 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation on fleet-oldest `fda-recall-scraper`, a mature niche already full-cohort swept 6 times — clean re-check plus one stale-claim fix)

Re-derived fleet-oldest fresh from `state/audit_dates.json`: `scholarship-scraper` (1274) still
skip-listed until 2026-10-20, so `fda-recall-scraper` (1382) was next — already in `TERM_VARIANTS`,
not one of the `0-TODO-h1400-unpromoted-niches` legs.

**Clean re-check.** Own price re-verified live first (0 drift: $0.0035/$0.003/$0.0027/$0.0024
FREE/Bronze/Silver/Gold+, no start fee). `niche-size` 290 matched (up from 282 at 1382),
`niche-unnamed` 221 unnamed. This README already carries 6 full-cohort live-pricing sweeps between
2026-09-20 and 2026-10-07 (the last two on the same day, down to a 3-user floor with 34+ handles
named), so rather than re-price all 221 again for a niche this saturated, checked whether any
listing newly crossing the 3-user floor broke the established pattern. None did: every one was
CPSC/NHTSA/EU-Safety-Gate/NZ/UAE/China-SAMR out-of-scope agency data, or one of `neuton`'s dozen
single-endpoint openFDA listings (adverse events/labels/UDI/shortages — not the enforcement/recall
endpoint this Actor reads) — the same out-of-scope shape every prior sweep already documented.
Spot-checked 4 sub-3-user, generically-named listings anyway on the chance a new entrant was
pricing aggressively (per the h1412 lesson that low user count correlates with price aggression in
a saturated niche): `whitel1ght/fda-recalls`, `weirworks/drug-device-recall-tracker`,
`zentrafoundry/product-recall-unified-monitor`, `zentrafoundry/fda-safety-signal-monitor-v2` — all
dearer than us, $0.003–$0.02/record flat. No new undercutter.

**Fixed one stale claim:** `check-competitor-claims` flagged `copious_atoll/fda-food-recalls` as 3
users in the README vs 4 live — this was exactly the item queue.md flagged for this Actor's next
touch. Fixed and added one dated paragraph recording the re-check and the correction.

**Verified:** build 0.1.60 pushed (package.json 0.1.20→0.1.21); live build README confirmed via
`GET /v2/acts/<id>/builds/<buildId>` byte-identical (57,717 == 57,717 bytes), containing both the
new paragraph and the corrected count. `check-competitor-claims` fleet-wide 462 claims/**6 stale**
(down from 7 — this Actor's fixed; the other 6 are pre-existing ordinary churn on 4 unrelated
Actors, unchanged, carried forward)/1 unresolvable + 171 paragraphs/0 undated. `check-pricing`
24/29/0, `check-charges` 1/0 missing, `check-own-price-freshness` 24/0, `check-comparison-breadth`
23/0 — all clean. Services (web/mail/caddy) active, site 200 on `/` and
`/tools/fda-recall-scraper`. Revenue unchanged: $0, 44 users, 610 runs30d (606 ext_ok/4 ext_bad), 0
bookmarks/reviews. `bin/traffic`: `/tools` 7, `/pricing` 3 — still far below the >100/day Polar
gate, not raised. Inbox: 10 msgs, all pre-vetted noise (2 SEO pitches, JP/CA/IT contact-form
autoreplies, 1 DMARC report, 1 bounce), nothing actionable, no owner email sent. $0 spent.
`audit_dates.json`'s `fda-recall-scraper.competitor_audit` bumped 1382 → 1415 with a new note
prepended (old chain preserved).

**Next cycle:** regular `competitor_audit` rotation resumes at fleet-oldest — re-derive fresh from
`state/audit_dates.json`; as of this edit that is `steam-reviews-scraper` (1383), then
`hacker-news-scraper` (1384). `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**.
`hacker-news-scraper` (1384, next-but-one) still has an open `0-TODO-h1400-unpromoted-niches` leg
plus an h1412-style full-unnamed-cohort resweep due (~248 matched, one of the two large commodity
niches flagged as likely to hide an unpriced tail) — fold both into that audit.
`remote-jobs-scraper` (~240 matched, already in TERM_VARIANTS) still needs its own h1412-style
full-unnamed-cohort resweep, separate from the term-coverage question, not yet done. A
QUALITY/GROWTH slot is due ~1416 (1413 took the last one) — good slot to finally pick up the 3
unanswered dev.to comments (`shieldxbot`/4809157, `launchgatecheck`+`nikhil_patel_10`/4689167,
`raknaos`/4627420, flagged since 1413) and start the `notes/LEARNINGS.md` 792KB trim. Backlog,
unchanged: `0-TODO-h1392-runfee-in-batch-copies` (24 of 26 copies left), 6 remaining stale
user-count claims on 4 unrelated Actors (`remote-jobs-scraper` x3, `scholarship-scraper`,
`shopify-products-scraper`, `trademark-search-scraper`) — fix opportunistically when each is next
touched, `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
`0-TODO-h1346-fleet-wide-sub20-counts`.

## Cycle 1414 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation on fleet-oldest `apple-podcasts-scraper`, closed its `0-TODO-h1400-unpromoted-niches` leg)

Re-derived fleet-oldest fresh from `state/audit_dates.json`: `scholarship-scraper` (1274) still
skip-listed until 2026-10-20, so `apple-podcasts-scraper` (1379) was next, and it carried an open
`0-TODO-h1400-unpromoted-niches` leg (one of the last 4 Actors never promoted into `niche-size`'s
hand-curated `TERM_VARIANTS`) plus a stale `spokentext` count flagged by 1413's handoff.

**Closed the TERM_VARIANTS leg.** The 11-term `auto_variants()` sweep (base phrase "apple podcasts"
+ generic modifiers) already hits 149 seen / 108 matched, and the README's last full-tail sweep
(cycle 1339) already names 104 of those 108 by hand — a mature niche. Tested 7 extra hand-picked
terms ("itunes podcast", "podcast scraper", "podcast directory", "podcast charts", "podcast rss",
"podcast episodes", plus variant forms): widened raw `seen` to 282 but matched stayed at 108 —
**a genuine clean negative, not a rescue** (same shape as the shopify-products-scraper and
nih-reporter promotions). Promoted the niche into `TERM_VARIANTS` anyway so this niche's counts
stop carrying the UNMEASURED caveat from LEARNINGS cycle ~1400.

**One real new find anyway:** the wider sweep surfaced exactly one genuinely new handle,
`tidytools/app-store-top-charts` (2u, primarily an App Store ASO/keyword-rank tracker) whose
`chart-entry` billing event explicitly covers "one app (or podcast) in a chart" — flat $0.0005
(Free) -> $0.0004 (Diamond), no Actor-start fee, **half our flat $0.001/row on the `charts` data
type specifically** (no episodes/reviews/search/publisher coverage at all, so scoped to chart rows
only). `recordsdata/apple-podcasts-scraper` (2u, charts+search) also newly surfaced, dearer at
every tier ($0.004/chart-record, $0.0025/podcast-record). Added as 1 new dated README paragraph.

**Fixed the stale claim 1413 flagged:** `check-competitor-claims` showed `spokentext/spotify-
podcast-transcript` as 2 users live vs 2 claimed — re-checked directly and found the discrepancy is
real but subtle: `totalUsers` (all-time, what the check reads) is 3, while `totalUsers30Days` (what
I'd eyeballed first) is 2 — same listing, two different live numbers. Fixed the README to 3u.

**Verified:** build 0.1.76 pushed (package.json 0.1.17->0.1.18); live build README (not the
CDN-cached Store page) confirmed via `GET /v2/acts/<id>/builds/<buildId>` to contain both new
handles and the corrected count. `check-competitor-claims` fleet-wide 462 claims/**7 stale** (down
from 8 — the spokentext one is now fixed; the other 7 are pre-existing ordinary churn on 4 unrelated
Actors, carried forward, not chased this cycle)/1 unresolvable + 171 paragraphs/0 undated.
`check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0,
`check-comparison-breadth` 23/0, `check-readme-samples` 35/82/0 drift — all clean. Services
(web/mail/caddy) active, site 200 on `/` and `/tools/apple-podcasts-scraper`. Revenue unchanged: $0,
44 users, 610 runs30d (606 ext_ok/4 ext_bad), 0 bookmarks/reviews. `bin/traffic`: `/tools` 7,
`/pricing` 3, `/contact` 10 — still far below the >100/day Polar gate, not raised. Inbox: 10 msgs,
all pre-vetted noise (2 SEO pitches from `searchindex.pro`, 5 JP/CA contact-form autoreplies, 1
DMARC report, 1 bounce, 1 CO-Sol autoreply), nothing actionable, no owner email sent. $0 spent.
`audit_dates.json`'s `apple-podcasts-scraper.competitor_audit` bumped 1379 -> 1414 with a new note
prepended (old chain preserved).

**Not done this cycle, carried forward:** the 3 unanswered dev.to comments flagged by 1413 (still
unread/untriaged), and `notes/LEARNINGS.md`'s overdue 792KB trim — neither touched, both still open.

**Next cycle:** regular `competitor_audit` rotation resumes at fleet-oldest — re-derive fresh from
`state/audit_dates.json`; as of this edit that is `fda-recall-scraper` (1382), then
`steam-reviews-scraper` (1383), `hacker-news-scraper` (1384). `scholarship-scraper` (1274) stays
skip-listed until **2026-10-20**. `0-TODO-h1400-unpromoted-niches` is now **3 of 24**:
`hacker-news-scraper`, `scholarship-scraper`, `us-federal-awards-scraper` — fold into whichever is
next audited; `hacker-news-scraper` (1384, soon due) has an open leg, worth doing inside that audit
given it's also one of the two large commodity niches h1412 flagged as likely to hide an unpriced
tail (~248 matched; `remote-jobs-scraper` ~240 is the other, already promoted into TERM_VARIANTS
but not yet given an h1412-style full-unnamed-cohort resweep). A QUALITY/GROWTH slot is due ~1416
(1413 took the last one). Backlog, unchanged: `0-TODO-h1392-runfee-in-batch-copies` (24 of 26
copies left), triage the 3 dev.to comments, `notes/LEARNINGS.md` trim, `0-TODO-h1368-newly-visible-
stale`, `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`.

## Cycle 1413 (2026-10-08, sonnet-5 — QUALITY/GROWTH slot: trimmed STATUS.md/queue.md, well past the 150KB standing threshold)

Took the due QUALITY/GROWTH slot (1412's handoff said 1413 should, not a third audit). Checked file
sizes first per the cycle-1219 standing rule and found both tracking files badly overdue: `STATUS.md`
had reached **406,770 bytes** (101 cycle entries, cycles 1304-1412) and `tasks/queue.md` **332,235
bytes** — both >2x the 150KB trim line, and large enough that the `Read` tool now hard-errors on them
(256KB max), meaning every future cycle reading this file for context was already degraded before
doing any real work.

**Trimmed both, verified lossless.** `STATUS.md`: moved cycles 1304-1399 (2,687 lines) into
`state/STATUS_ARCHIVE.md` under a new `## Archived 2026-10-08T12:01:51Z by cycle 1413` header,
prepended ahead of the existing archive content; live file now holds cycles 1400-1412 at **60,205
bytes**. `tasks/queue.md`: per the cycle-1225 standing note that superseded `NEXT-CYCLE` blocks have
**zero** remaining operational value once replaced (durable lessons belong in LEARNINGS.md, not here),
moved every `## Superseded:` block (lines 91-3824, all history back to ~cycle 780) into
`tasks/queue_archive.md`, leaving just the one live `NEXT-CYCLE` block at **8,029 bytes**. Verified
losslessness both ways by `cat`-ing the split files back together and diffing against a pre-edit
backup — byte-identical for both STATUS.md and queue.md. `notes/LEARNINGS.md` is also oversized
(792,264 bytes, 303 cycle entries) but is a different shape (lessons, not supersede-based) and needs
more careful curation than a mechanical split — left as a follow-up, not attempted this cycle.

**Also ran the dev.to comment poll** (cheap, high-yield per LEARNINGS cycle 641/863): 15 published
articles, 3 have comments (4809157: 1, 4689167: 3, 4627420: 1), all top-level with no reply posted
yet. One (`dododata` on 4689167) was already measured and deliberately left unreplied in
LEARNINGS_ARCHIVE:3516 (their fix doesn't apply to our already-correct stat). The other 3
(`shieldxbot`/4809157, `launchgatecheck` + `nikhil_patel_10`/4689167, `raknaos`/4627420) are generic
promotional-sounding praise from oddly-branded accounts (SaaS-product-like usernames) — plausible
engagement-farming, not evaluated deeply this cycle for time; flagged in queue.md rather than replied
to without checking whether a reply is actually warranted.

**Verified:** services (web/mail/caddy) active, site 200 on `/` and `/tools`. Revenue unchanged: $0,
44 users, 608 runs30d (604 ext_ok/4 ext_bad), 0 bookmarks/reviews. `bin/traffic`: `/tools` 7,
`/pricing` 3, `/contact` 10, `/docs` 5 — still far below the >100/day Polar gate, not raised. Inbox:
9 msgs, all pre-vetted noise (2 SEO pitches from `searchindex.pro`, 5 JP/CA/IT contact-form
autoreplies, 1 DMARC report, 1 bounce), nothing actionable, no owner email sent. $0 spent. No Actor
code touched, so no build/smoke run was needed; regular `competitor_audit` rotation untouched this
cycle, resumes next cycle exactly where 1412 left it.

## Cycle 1412 (2026-10-08, opus-5 — regular `competitor_audit` rotation on fleet-oldest `google-play-reviews-scraper`)

Re-derived fleet-oldest fresh from `state/audit_dates.json`: `scholarship-scraper` (1274) still
skip-listed until **2026-10-20**, so the target was `google-play-reviews-scraper` (1378 → 1412).
**This audit produced the largest batch of undercutters any cycle on this fleet has found — because
it finally priced the 1-and-2-user tail that cycles 1338 and 1378 had both logged as a known
unpriced gap.** Own price re-verified live first: flat $0.0001/result, no start fee, no tiers, 0
drift. `niche-size` 467 seen / 268 matched (flat vs 467/271 at 1378). `niche-unnamed`: **224 unnamed
of 268, but only 62 clear the ≥3-user floor** — the ≥3u-only method prior cycles used was
structurally blind to 162 listings. Live-priced all 224 individually, 0 unresolvable.

**Fifteen previously-unnamed effective undercutters, and every single one sits at 1–2 users** (all 15
inside the skipped tail). Six carry **no start fee**, so they beat us at every run size with no
crossover in our favour: `scrapersdelight/google-play-reviews-scraper` at **$0.000045** (55% under
us, the cheapest honest per-review price in the niche), `steadyscrape/…` and `pappy-dev/google-play-
reviews` at $0.00005, `realai_pl/google-play-reviews-fast` and `peerless_columbine/…-api` at
$0.00008, `cheapapi/app-store-google-play-scraper` at $0.00009. Nine more sit behind only a $0.00005
(Apify default) or $0.0001 start fee — crossover **2–5 reviews**, below any real run, so reported as
plain undercutters, including `cirkit/google-play-store-scraper` whose $0.00008 review event is *not*
its Store-displayed primary ($0.0006/app record) and so was invisible to any headline comparison.
Two genuine crossovers remain: `superslowsloth` (67 reviews) and `tactful_anvil` ($0.00008 + $0.01
start = **500 reviews**, the one case where we are still the cheaper choice for small/medium pulls).

**Closed `0-TODO-h1392-runfee-in-batch-copies`' leg for the script in use and it paid off the same
cycle:** repointed `bin/_batch_price_gprs.py` at `bin/_apify_get.py` (its old unguarded `.json()`
turned a transient blip into `error: unresolvable` — a rival silently dropping out of the
comparison) and added `cps.runfee_price`, which automatically surfaced `second_coming/app-store-
review-analyzer`: flat **$0.02/scan**, no per-row event at all, crossover ~200 reviews. That is the
**second** run-fee-only rival from this same owner after `brand-mention-monitor` at 1384/1392.

**One ruled out, and it breaks an existing diagnostic tell:** `listless_adzuki/app-store-review-
scraper` shows $0.00001/row, but that is Apify's generic `apify-default-dataset-item` platform
charge sitting beside a named `review-result` event at $0.004 (40× us) — the same trap as `johnvc`
at 1378, **except that here the generic platform event is the one flagged `isPrimaryEvent`**. So
`primary` is not a reliable guide to what a rival bills. Written up as **`h1412` in LEARNINGS**,
whose generalizable rule is: **never apply a user-count floor in a niche with >100 matched listings
or an own-price at the compute floor** — in a commodity niche the only way a new entrant wins a
first customer is to launch *underneath* the incumbent price, so price aggression and low user
count are positively correlated, and a user-count floor filters out exactly the population it most
needs to see. 224 listings cost ~4 min of read-only GETs and $0.

**No claim was inverted** — this README already stated "we are not the cheapest per-review Actor in
this niche, and we are not even close to it", which is now far better evidenced. Added 2 dated
paragraphs, raised the running undercutter total 10 → 25, and replaced the stale "long tail of
1-and-2-user listings we have not priced one by one" caveat with the closed result.

**Verified:** build 0.1.69 pushed (package.json 0.1.18→0.1.19); live README confirmed via `GET
/v2/actor-builds/<buildId>` byte-identical to local (41,628 == 41,628) and containing all 6 probed
new strings — not the CDN-cached Store page, per the standing rule. `check-store-index` 0 stale,
index reindexed 11:39:05 vs build 11:39:27. `check-competitor-claims` fleet-wide 460 claims (up from
450 — the new handles) / **0 stale on this Actor** / 171 paragraphs / 0 undated. `check-pricing`
24/29/0, `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0, `check-charges` 24/24,
`check-readme-samples` 35 blocks / 82 bullets / 0 drift — all identical to recorded baselines.
`_batch_price_gprs.py` `py_compile` clean. Services (web/mail/caddy) active, site 200 on `/` and
`/tools/google-play-reviews-scraper`. Revenue unchanged: $0, 44 users, 606 runs30d, 0
bookmarks/reviews. `bin/traffic` `/pricing` 3, `/tools` 7 — far below the >100/day gate, Polar NOT
raised. Inbox 10 msgs, all pre-vetted noise, nothing actionable, no owner email. $0 spent.
`audit_dates.json`'s `google-play-reviews-scraper.competitor_audit` bumped 1378 → 1412 with a new
note prepended (old chain preserved).

**Next cycle:** **a QUALITY/GROWTH slot is due (~1413)** — 1411 took the last one and 1412 was a
regular audit, so 1413 should take it rather than a third audit in a row. Then apply h1412 to the
rotation: the ≥3u floor was standard before ~1410, so the same blind spot plausibly hides
undercutters in the other large commodity niches — `hacker-news-scraper` (~248 matched) and
`remote-jobs-scraper` (~240) are the obvious candidates, worth prioritising over strict
oldest-first; price the FULL unnamed cohort from now on. Otherwise rotation resumes at fleet-oldest
(re-derive fresh; currently `apple-podcasts-scraper`, 1379, which also has an open
`0-TODO-h1400-unpromoted-niches` leg and a stale `spokentext` count to fix inside that audit).
Backlog: `0-TODO-h1392-runfee-in-batch-copies` (**24 of 26 copies left**), `0-TODO-h1368-newly-
visible-stale`, `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`.

## Cycle 1411 (2026-10-08, sonnet-5 — QUALITY/GROWTH slot, closed `0-TODO-h1396-ted-invisible-60`)

Closed the fleet's highest-priority open tool TODO: `bin/_batch_price_ted.py`'s cycle-1348
`eu-ted-tenders-scraper` audit had reported "no undercutters" over a cohort where **60 of 151
listings carried `tiers: {}`** from a since-fixed flat-only pricing-reader bug, so that
conclusion was unsupported for those 60. Extracted the exact 60 handles (matching
`bin/_unit_price_selftest.py`'s own lost-key logic), re-priced them live via the
already-repointed script, and merged the fresh data back into the full 151-row cohort —
`_unit_price_selftest.py` on that file now reports **0 unreplayable (was 60)**.

**Found and disclosed 2 genuine, previously-invisible undercutters:** `deriverge/public-
tenders-scraper` (2 users, explicitly reads TED + UK Find a Tender + Contracts Finder) is
tiered **$0.001 (Free) → $0.0005 (Gold+)** against our flat $0.0015, cheaper at *every* tier and
run size, no start fee. `humble-echidna/eu-ted-tenders` (3 users, same TED+UK scope) is tiered
$0.002 → **$0.0014 (Gold+)**, a partial undercut from Gold up. A third, `andok/eu-tenders-
scraper`, undercuts only on its hardest-to-reach Diamond tier and its $0.0028 start fee pushes
the real crossover to ~28 notices/run — noted but called immaterial. 5 of the 60 confirmed OUT
OF SCOPE (single-country portals, not TED); the rest price at or above our rate. Added as a new
"Twelfth sweep" README paragraph following the page's own established convention.

Also ran `_unit_price_selftest.py` with no args across all 29 saved cohorts (the TODO's own
suggested follow-up): **0 unreplayable fleet-wide** — `ted` was the only cohort with the
tiers-lost bug, confirming the cycle-1396 repoint already closed it everywhere else it could
recur. 30 MOVED verdicts turned up in 11 other, mostly FLAT-schema cohorts — expected per the
selftest's own documented FLAT-schema limitation (can't see a tier ladder), not a confirmed bug,
left for each Actor's next regular audit rather than chased now.

**Verified:** own price re-read live first (flat $0.0015/result, no start fee, 0 drift). Build
pushed (`eu-ted-tenders-scraper` package.json 0.1.10→0.1.11, Apify build 0.1.64); live README
confirmed via `GET /v2/actor-builds/<buildId>` (not the CDN-cached Store page) to contain the
new paragraph and both new handles. Fleet-wide `check-pricing` 24/29/0,
`check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0, `check-charges` 24/24 all
clean. `check-competitor-claims`: 450 claims/5 stale/1 unresolvable, **0 of the 5 on this
Actor** — the 5 are pre-existing 1-3-user drift on 4 unrelated Actors, left for opportunistic
fixing. Services (web/mail/caddy) active, site 200 on `/` and `/tools/eu-ted-tenders-scraper`.
Revenue unchanged: $0, 44 users, 606 runs30d, 0 bookmarks/reviews. `audit_dates.json`'s
`eu-ted-tenders-scraper.competitor_audit` bumped 1387→1411 with a new note prepended (old chain
preserved — this was a targeted TODO fix, not a fresh niche-size/niche-unnamed sweep, so the
regular rotation audit is still due separately). Inbox: 8 msgs, all pre-vetted noise, nothing
actionable, no owner email. $0 spent.

**Next cycle:** regular `competitor_audit` rotation resumes — re-derive fleet-oldest fresh from
`audit_dates.json` (currently `apple-podcasts-scraper`, 1379). Next QUALITY/GROWTH slot due
~1414. Remaining backlog: `0-TODO-h1392-runfee-in-batch-copies`, `0-TODO-h1368-newly-visible-
stale`, `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`.

## Cycle 1410 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation on fleet-oldest `sec-insider-trades-scraper`)

Re-derived fleet-oldest fresh from `state/audit_dates.json`: `scholarship-scraper` (1274) still
skip-listed until 2026-10-20, so `sec-insider-trades-scraper` (1376) was next.

**Audit found a real, if small, disclosure gap — not a flat "clean negative."** `niche-size`:
256 seen / 108 matched (up from 254/108 at 1376, no change in matched count). `niche-unnamed`: 46
unnamed (down from 55, README now names 64 vs 53). Own price re-verified live first: flat
**$0.0018/`result`, no start fee**, unchanged. Only `sutraflow/sec-insider-trading-signals` (3
users) cleared the usual ≥3-user floor ($0.01 start + $0.01/txn — dearer, no undercut). Per the
standing full-cohort rule for this niche, live-priced the entire remaining 45-listing tail (0-1
users each) anyway: **0 new per-row undercutters**, modal price ~$0.003-$0.005/row, consistent
with every prior sweep.

**The real find: two volume-dependent near-misses, same class as the README's existing
per-filing break-even paragraphs, just on the per-search/per-ticker side instead.**
`m_ctim/insider-trading-alert` charges one flat `insider-search` fee ($0.007 FREE → $0.0055
DIAMOND) regardless of how many transactions a search returns — breaks even against our
$0.0018/row at **3.1-3.9 rows**, below the 8 rows this README's own Apple sample already pulled
from one accession. `zinin/insider-trading-tracker` charges per ticker delivered ($0.005 FREE →
$0.004 DIAMOND) covering that ticker's "bounded Form 3/4/5 activity" — breaks even at **2.2-2.8
rows/ticker**, again below Apple's 8 (though above MSFT/JPM's 1-row-per-filing sample). Neither
is a confirmed undercut (both 1 user, neither's listing claims the code-decode/signed-value/flag
fidelity this Actor leads on), but both price per-search/per-ticker rather than per-row, so a
buyer pulling a high-activity issuer would pay less there than here. Added as a new paragraph
disclosing both with their break-evens, following the README's own established convention for
this exact shape.

**Verified, caught and fixed my own slip:** `check-competitor-claims` (run after the first push)
flagged my own new paragraph — I'd written `sutraflow` as "2 users" when the live count was 3.
Fixed and re-pushed (build 0.1.38 → 0.1.39). The same check run also caught an unrelated
pre-existing stale claim on `app-store-reviews-scraper` (`apihq/app-store-reviews-scraper` stated
as 25 users, live 28) — fixed and pushed that Actor's build too (0.1.21 → 0.1.22). Live build
readme confirmed to contain the new text (`httpx`/API read of the `latest` build, not the
CDN-cached Store page). Fleet-wide `check-pricing` 24/29/0, `check-charges` 24/24,
`check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0, `check-readme-samples` 0 drift
— all clean, all identical to prior baselines. `check-competitor-claims` fleet-wide now 447
claims/**1 stale** (the pre-existing `apple-podcasts-scraper`→`spokentext` 2-vs-3-user drift,
found but left — ordinary single-user churn outside this cycle's scope, not chased)/1
unresolvable (the long-standing `scraper_guru` case) + 170 paragraphs/0 undated. Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; site 200 on `/` and
`/tools/sec-insider-trades-scraper`. Revenue unchanged: $0, 44 users, 606 runs30d, 0
bookmarks/reviews. `bin/traffic`: `/pricing` 3, `/tools` 7 — below the >100/day Polar gate, so
per owner instructions Polar not raised. Inbox: 10 messages, all pre-vetted noise (2x
searchindex.pro SEO pitch, JP/CA/IT contact-form autoreplies, 1 DMARC report, 1 bounce) — nothing
actionable, no owner email sent. `audit_dates.json`'s `sec-insider-trades-scraper.competitor_audit`
bumped 1376 → 1410 with a new note prepended (old chain preserved). $0 spent.

**NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes — re-derive fleet-oldest fresh
from `state/audit_dates.json`, do not trust this guess: as of this edit it is
`google-play-reviews-scraper` (1378), then `apple-podcasts-scraper` (1379). `scholarship-scraper`
(1274) stays skip-listed until 2026-10-20. (2) `0-TODO-h1400-unpromoted-niches` is still **4 of
24** (unchanged this cycle — `sec-insider-trades-scraper` was already promoted into
`TERM_VARIANTS` as of the 1220/1376 work, this cycle just re-ran it): `apple-podcasts-scraper`,
`hacker-news-scraper`, `scholarship-scraper`, `us-federal-awards-scraper`. (3) The incidental
`apple-podcasts-scraper`→`spokentext` 2-vs-3-user staleness found by this cycle's
`check-competitor-claims` run is trivial and low-priority — fix opportunistically whenever that
Actor is next touched, not worth a dedicated cycle. (4) `ats-jobs-scraper`'s unread tail (~768 of
813 matched) is still open. (5) Backlog unchanged, priority order:
`0-TODO-h1396-ted-invisible-60`, `0-TODO-h1392-runfee-in-batch-copies`,
`0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
`0-TODO-h1346-fleet-wide-sub20-counts`. (6) A QUALITY/GROWTH slot is due ~1411 (1408 took the
last one, 1409/1410 were both regular audits).

## Cycle 1409 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation on fleet-oldest `shopify-products-scraper`, also closed that Actor's leg of `0-TODO-h1400-unpromoted-niches`)

Re-derived fleet-oldest fresh from `state/audit_dates.json`: `scholarship-scraper` (1274) still
skip-listed until 2026-10-20, so `shopify-products-scraper` (1372) was next.

**Audit: clean negative.** `niche-size`/`niche-unnamed` (old 11-term auto sweep): 396 seen / 145
matched / 60 unnamed (README already names 106 handles). Only 4 unnamed listings cleared the
usual >=3-user noise floor — `hipersoft/shopify-product-scraper`, `jamhimself/shopify-products-
scraper`, `catalini82/shopify-price-restock-monitor`, `frabi/shopify-store-intelligence-scraper`
— all live-priced via `GET /v2/acts/<owner>~<slug>`, all dearer than our $0.001→$0.00085 tiered
rate at every tier (hipersoft $0.002→$0.001 tiered + a $0.001/store-page fee + $0.00005 start;
jamhimself flat $0.004/product; catalini82 flat $0.0015/result; frabi flat $0.002/product-
scraped). No undercutter, no README/build change needed.

**Also closed this Actor's leg of `0-TODO-h1400-unpromoted-niches` (now 4 of 24).** Promoted
`shopify-products-scraper` into `bin/niche-size`'s `TERM_VARIANTS` — a THIRD "no rescue needed"
instance after `nih-reporter-scraper` (1404) and `google-news-scraper` (1405): the base phrase
"shopify products" already stems to match "shopify product" and the matcher's name+title+
description blob already catches no-space/reworded titles. Went further than the previous two
promotions by actually testing 6 extra hand-picked terms from this niche's own cycle-1144
vocabulary (`shopify scraper`, `shopify store products`, `shopify catalog`, `shopify store`,
`shopify product`, `shopify ecommerce`) against the live Store search — they widened `seen` from
396 to 511 but added only 4 matches, 3 of them tiny (0-3 users) and dearer, and the 4th a **false
positive**: `mighty_monk/shopify-reviews-scraper` (65 users) scrapes Shopify **review widgets**
(Judge.me/Loox/Stamped/Yotpo/Okendo), not the product catalog — it only matched because its own
description happens to say "Shopify product pages". The real `mighty_monk` catalog rival
(`shopify-product-scraper`) is already named in the README. Kept the extra terms in the
hand-curated list anyway (documented, zero cost) but made **no README change** from them —
nothing real to disclose. `niche-size` now reports 148 matched under the 17-term hand-curated
list vs 145 under the old 11-term auto sweep; the 3-listing delta is exactly the 3 tiny dearer
rivals, not a coverage fix.

**Verified:** `bin/niche-size` `py_compile` clean; re-ran live post-edit and got 148 matched
(hand-curated, 17 queries) vs 145 pre-edit (auto-generated, 11 queries) — consistent with the
analysis above; `niche-unnamed` re-run post-edit reproduces the same top line
(`mighty_monk/shopify-reviews-scraper` at 63u, the false positive, then the 4 live-priced >=3u
listings). Fleet-wide `check-pricing` 24/29/0, `check-charges` 24/24, `check-comparison-breadth`
23/0, `check-own-price-freshness` 24/0 — all clean, all identical to prior baselines (no
regression from the `TERM_VARIANTS` edit). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) all active; site 200 on `/` and `/tools`. Revenue unchanged: $0, 44 users, 606 runs30d,
0 bookmarks/reviews. Inbox: 9 messages, all pre-vetted noise (2x searchindex.pro SEO pitch, JP/
CA/IT contact-form autoreplies, 1 DMARC report) — nothing actionable, no owner email, no reply
sent. `audit_dates.json`'s `shopify-products-scraper.competitor_audit` bumped 1372 → 1409 with a
new note prepended (old chain preserved). No README/Actor build pushed this cycle (no code/
copy change was warranted — only `bin/niche-size` changed), $0 spent.

**NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes — re-derive fleet-oldest fresh
from `state/audit_dates.json`, do not trust this guess: as of this edit it is
`sec-insider-trades-scraper` (1376), then `google-play-reviews-scraper` (1378).
`scholarship-scraper` (1274) stays skip-listed until 2026-10-20. (2)
`0-TODO-h1400-unpromoted-niches` is now **4 of 24**: `apple-podcasts-scraper`,
`hacker-news-scraper`, `scholarship-scraper`, `us-federal-awards-scraper` — expect "no rescue
needed" to remain the common outcome (three consecutive instances now), but still worth the
`niche-unnamed` check each time since the *disclosure* side (new live-priced rivals) is the real
value, not the promotion itself. (3) `ats-jobs-scraper`'s unread tail (~768 of 813 matched) is
still open. (4) Backlog unchanged, priority order: `0-TODO-h1396-ted-invisible-60`,
`0-TODO-h1392-runfee-in-batch-copies`, `0-TODO-h1368-newly-visible-stale`,
`0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. (5) A QUALITY/GROWTH
slot is due ~1411 (1408 took the last one).

## Cycle 1408 (2026-10-08, opus-5 — QUALITY/GROWTH slot: closed the 4-cycle `_apify_get` repoint, which surfaced a fleet-wide FALSE POSITIVE in `check-store-index`)

Took the due QUALITY/GROWTH slot (1405 took the last one). Closed queue item (4), the
`_apify_get` repoint carried over unfinished from 1404/1405/1406/1407 — and finishing it
exposed a real bug that had been hiding behind a never-run check.

**1. `_apify_get` repoint — DONE, item (4) closed.**
- `check-store-index`: all 3 Apify call sites repointed. Each `.json()["data"]` could raise
  `JSONDecodeError` *and* `KeyError`; more importantly each needed a *different* policy, not a
  blanket guard: the `?my=true` fleet listing is the tool's **denominator**, so a failure there
  now `sys.exit`s FATAL (an empty fleet would otherwise have printed a confident "0 stale");
  a 404/403 on a per-Actor record we just read out of our own listing is **not** a normal
  absence, so it prints `LIVE RECORD UNREADABLE` and joins a new `unknown` list; an unreadable
  build prints `readme=UNKNOWN(status)`. A new `WARNING: INCOMPLETE CHECK` line names every
  uncompared Actor (the cycle-1404 completeness rule).
- `check-disclosure`: the handoff's warning was right and understated — **both** call sites are
  dev.to, not Apify (lines 78 and 83). Repointed anyway (`get_json` is host-agnostic; only the
  `FINAL_MISSING`/`RETRY_STATUS` split is Apify-tuned, and that split is correct for dev.to too).
  The crash was not the real bug: one `try/except` wrapped the *whole* leg, so a blip on any
  single article aborted the rest while printing only "SKIPPED", and the verdict line
  "0 missing disclosure(s)" + exit 0 looked identical whether dev.to was fully checked or not
  checked at all. Per-article failures are now counted (`UNCHECKED`), and a
  `COVERAGE INCOMPLETE` line prints beside the verdict. Exit code deliberately stays 0 on an
  unreachable dev.to — offline usability is the documented design intent.

**2. The real find: `check-store-index` was reporting `stale=['readme']` on all 24 Actors, and
every one was a FALSE POSITIVE.** Apify **removed the `readme` attribute from the
`prod_PUBLIC_STORE` index** (hits now carry `readmeSummary`, an ~285-word AI-generated summary).
The cycle-972 compare did `norm(hit.get("readme")) != norm(bmd)` — `.get` on a *missing* key gave
`None`, `norm` made it `""`, and the tool diffed that against a 6,612-word build readme.
Guaranteed mismatch, every Actor, permanently. **Confirmed three ways:** dumped a hit's keys (no
`readme` key at all, `readmeSummary` present); `-v` showed "indexed 0 words vs build 6612 words";
and **re-ran the pre-edit file via `git show HEAD:bin/check-store-index`, which produced the
identical 24/24 — proving the bug predated this cycle's edits and that the repoint is
behaviour-neutral.** What exposed it was the contradiction with `LEARNINGS:168` ("fleet run after
the fix: 0 stale") — a fleet-wide *uniform* failure is nearly always the measurement, not the
fleet. `readmeSummary` is NOT substitutable (derived prose; word-diffing it is wrong by
construction), so the fix **reports the lost coverage** rather than retargeting the check at the
nearest-looking field to keep a green tick. Fleet now reads **0 stale / 24** with an explicit
`readme NOT CHECKED for 24 Actor(s)` note. This matters beyond cosmetics: `LEARNINGS:168` makes
"run `check-store-index <slug>` after every readme change" a standing rule and every h904
readme-proximity measurement is gated on "0 stale" — that gate was unsatisfiable.

**Verified (not assumed):** both tools `py_compile` clean; **fault-injected both new guards** —
a bogus token reproduces `FATAL: could not list our own Actors (status=401)` with **script exit
1**, and a deliberately-wrong slug reproduces `LIVE RECORD UNREADABLE (status=404)` plus the
`WARNING: INCOMPLETE CHECK` naming all 24. Live runs: `check-disclosure` 53 site posts + 15
dev.to articles / 0 missing / no COVERAGE INCOMPLETE line; `check-store-index` 0 stale / 24.
Standing checks all match recorded baselines exactly — `check-pricing` 24/29/0, `check-charges`
24/24, `check-own-price-freshness` 24/0, `check-competitor-claims` 446/0 stale + the 1
pre-existing unresolvable (`scraper_guru` in substack-scraper's README, unrelated) + 169/0
undated. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; site 200 on `/` and
`/tools`. Revenue unchanged: **$0, 44 users, 606 runs30d, 0 bookmarks / 0 reviews.** `bin/traffic`
checked for the Polar gate: `/pricing` 3 and `/tools` 7 hits — far below >100/day, so per owner
instructions Polar was **not** raised. Inbox: 10 messages, all the same pre-vetted noise (2x
searchindex.pro SEO pitch, JP/CA/IT contact-form autoreplies, 1 DMARC report, 1 bounce) —
nothing actionable, no owner email, no reply sent. **No README/Actor change, no build pushed,
$0 spent.** No `competitor_audit` ran (QUALITY slot), so `audit_dates.json` is untouched by
design.

**Deliberately NOT done:** the `shopify-products-scraper` leg of
`0-TODO-h1400-unpromoted-niches`. The `_apify_get` repoint was the older, 4-cycle-deferred item
and it opened into a live false-positive worth finishing properly; the niche leg is unblocked and
carried forward intact.

## Cycle 1407 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation on re-derived fleet-oldest `us-federal-awards-scraper`)

Re-derived fleet-oldest fresh from `state/audit_dates.json`: `scholarship-scraper` (1274) still
skip-listed until 2026-10-20; next is `us-federal-awards-scraper` (1369).

**Clean negative — no new undercutter, no drift, no README/build change.** `niche-size`/
`niche-unnamed`: 147 seen / 126 matched / 40 unnamed (up from 145/125/38 at cycle 1369 — normal
churn in a heavily-templated niche). The unnamed tail's `>=3u` cut is thin (3 listings): 2 of
those 3 (`nasasurfer`, `carranza-tech`) are already covered by the README's bare-handle "tie our
Free tier" sentence, and the third (`crawlerbros/usaspending-scraper`, plus its sibling listing
`crawlerbros/usa-spending-federal-data`) ties $0.005 FREE → $0.003 GOLD+ + a $0.005 start fee —
dearer than our $0.004→$0.0025 ladder at every tier. Live-priced a 30-listing sample of the 2u
tail too: everything resolvable priced at $0.004+. The one listing that looked like a steal,
`datasignalslab/gov-contract-awards-monitor` ($0.00001 on the default dataset-item event), is
the same misleadingly-cheap-default-event trap the cycle-1218 note on this same Actor already
flagged on `omarchydev` — its real `isPrimaryEvent` is `company-analyzed` at $0.02, a different
shape (per-company risk score, not bulk award export), correctly left unnamed. Spot-checked 8
headline named rivals (`parseforge`, `benthepythondev`, `ryanclinton`, `copious_atoll`,
`fortuitous_pirate`, `pink_comic`, `jungle_synthesizer/samgov-scraper`, `datamule`) for drift —
every price that resolved matched the README exactly. Per the 1311/1353/1369 "nothing changed"
precedent, README left untouched, no build pushed. `audit_dates.json`'s
`us-federal-awards-scraper.competitor_audit` bumped 1369 → 1407 with a new note prepended (old
chain preserved).

- Verified fleet-wide: `check-competitor-claims` 446/0 stale + 1 pre-existing unresolvable
  (`substack_guru`, unrelated) + 169/0 undated; `check-price-superiority` 1673/557/**0
  undisclosed** (18 run-fee-only rivals held out, 0 undisclosed); `check-pricing` 24/29/0;
  `check-charges` 24/24 — all clean, all identical to the 1404-1406 baselines (no regression).
  Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active, site 200 on `/` and
  `/tools`.
- `bin/traffic` checked for the Polar-checkout gate: no sustained >100/day hits to `/pricing` or
  `/tools` — per owner instructions, still do NOT raise Polar.
- Demand unchanged: revenue $0, 44 users, 606 runs30d, 0 bookmarks/reviews. Inbox: 9 messages,
  same pre-vetted noise (2x searchindex.pro SEO pitch, JP/CA/IT contact-form autoreplies, 1 DMARC
  report, 1 bounce) — nothing actionable, no owner email.
- Spend: $0 cash, no Actor runs beyond free live-pricing GETs, no build pushed.
- Next cycle resumes the regular `competitor_audit` rotation at the new fleet-oldest unblocked
  Actor — re-derive fresh, expected `shopify-products-scraper` (1372) then
  `sec-insider-trades-scraper` (1376), but VERIFY per the standing process lesson. Next
  QUALITY/GROWTH slot due ~1408.

## Cycle 1406 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation on re-derived fleet-oldest `fec-campaign-finance-scraper`)

Re-derived fleet-oldest unblocked straight from `state/audit_dates.json` (sorted fresh, per the
standing 1403 process lesson) rather than trusting 1405's handoff guess: `fec-campaign-finance-
scraper` (1368), confirmed `scholarship-scraper` (1274) still skip-listed until 2026-10-20.

**Clean for a THIRD consecutive time.** `niche-size`/`niche-unnamed`: 460 seen / 42 matched / 0
unnamed — stable vs 459/42/0 at both cycle 1332 and 1368. Re-priced all 42 named rivals live in
parallel (`bin/_batch_price_fec.py`), then checked for price drift by locating each handle's own
README **paragraph** (blank-line-scoped) rather than a fixed-char window, which bleeds into
neighbouring rivals' numbers — exactly the trap the cycle-1332 note on this same Actor already
flagged. Every in-scope rival's live price matches a dollar figure in its own paragraph within
5%. The one non-match (`nexgendata/lda-lobbying-disclosure-scraper`, live $0.05) is one of the 4
listings this README explicitly excludes as out-of-scope (CA/NY state-level filings, 1 UK
scraper, 5 LDA-lobbying products) and correctly carries no price claim — not drift. **Zero real
price drift; no README/build change needed** (1311/1353 churn precedent). `audit_dates.json`
bumped `fec-campaign-finance-scraper.competitor_audit` 1368 -> 1406 with note prepended, old
chain preserved.

- Verified: fleet-wide `check-price-superiority` 1673/557/**0 undisclosed**,
  `check-competitor-claims` 446/0 stale + 1 pre-existing unresolvable + 169/0 undated,
  `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0,
  `check-comparison-breadth` 23/0 — all clean, all counts identical to cycles 1404/1405's
  baselines (no silent regression from the 1404 `_apify_get` repoint). Services
  (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active, site 200 on `/` and `/tools`.
- `bin/traffic` checked for the Polar-checkout gate: no sustained >100/day hits to `/pricing` or
  `/tools` pages — per owner instructions, still do NOT raise Polar.
- Demand unchanged: revenue $0, 44 users, 606 runs30d, 0 bookmarks/reviews. Inbox: 9 messages,
  all pre-vetted noise (2x searchindex.pro SEO pitch, JP/CA/IT contact-form autoreplies, 1 DMARC
  report, 1 bounce) — nothing actionable, no owner email.
- Spend: $0 cash, no Actor runs beyond free live-pricing GETs, no build pushed.
- Next cycle resumes the regular `competitor_audit` rotation at the new fleet-oldest unblocked
  Actor — re-derive fresh, expected `us-federal-awards-scraper` (1369) then
  `shopify-products-scraper` (1372), but VERIFY per the standing process lesson. Next
  QUALITY/GROWTH slot due ~1408.

## Cycle 1405 (2026-10-08, sonnet-5 — due QUALITY/GROWTH slot; closed the `google-news-scraper` leg of `0-TODO-h1400-unpromoted-niches`, confirming it as the second "no rescue needed" outcome after nih-reporter)

Promoted `google-news-scraper` into `bin/niche-size`'s `TERM_VARIANTS` (its existing 11-term
`auto_variants()` sweep made explicit/hand-curated; no `MATCH_SYNONYMS` needed). Verified live
**before and after**: 389 seen / 232 matched, unchanged — this niche's base phrase "google news"
already is the product's own name (unlike CourtListener/Greenhouse-style niches where the base
phrase was wrong), and the matcher's name+title+description blob already catches no-space
name-field variants (`johnvc/GoogleNewsAPI`) via their spaced title field. Re-ran `niche-unnamed`:
top unnamed is 19u, below the fleet's >=20u disclosure threshold — nothing new for the README.
The niche's two known real gaps (DataForSEO's SERP tool, `simple.actor/google-search`) were found
by hand-reading descriptions in cycles 1260/1303/1347, not by keyword search, and no
`TERM_VARIANTS` entry can recover them — documented in the code comment so no future cycle
re-attempts that rescue. No code/README change, no build, $0 spent. `audit_dates.json`'s
`competitor_audit` bumped 1385 -> 1405 with note prepended (old note preserved). `0-TODO-
h1400-unpromoted-niches` now **5 of 24**: `apple-podcasts-scraper`, `hacker-news-scraper`,
`scholarship-scraper`, `shopify-products-scraper`, `us-federal-awards-scraper`.

- Verified: `bin/niche-size` syntax-checked clean; fleet-wide `check-pricing` 24/29/0 clean
  post-edit. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active, site 200.
- Demand unchanged: revenue $0. Inbox: 9 messages, all noise (SEO "get listed" pitches, JP
  contact-form autoreplies/bounce, 1 DMARC report) — nothing actionable, no reply sent.
- Spend: $0 cash, no Actor runs, no build pushed.
- Next cycle resumes the regular `competitor_audit` rotation — re-derive fleet-oldest fresh from
  `state/audit_dates.json`, expected `fec-campaign-finance-scraper` (1368) then
  `us-federal-awards-scraper` (1369), but verify.

## Cycle 1404 (2026-10-08, opus-5 — ran the fleet-oldest `competitor_audit` (`nih-reporter-scraper`), which came back clean for the THIRD time; the real find was a transient-API-failure class that was silently corrupting the checks themselves)

**Audit (`nih-reporter-scraper`, 1366 -> 1404).** Re-derived fleet-oldest fresh from
`state/audit_dates.json` as 1403's handoff insisted (sorted the `competitor_audit` values at
read time rather than trusting a cached ordering — the exact bug 1403 fixed).
`scholarship-scraper` (1274) stays skip-listed until 2026-10-20, so `nih-reporter-scraper`
(1366) was next. `niche-size`: 277 seen / **51 matched**, README claims 51 and MATCHES.
`niche-unnamed`: **0 unnamed of 51**. That is the third consecutive clean sweep (1330, 1366,
1404) with an identical matched count, so README left untouched per the cycle-1353/1311
"date-only bump is churn" precedent. No build pushed, $0 spent.

**First negative result for the ats-jobs/court-records playbook.** Rather than re-confirm a
saturated sweep a fourth time, tested whether the MATCH RULE was under-matching, as it had been
on `ats-jobs-scraper` (200 -> 813 matched) and `court-records-scraper` (4.8x). **It was not.**
Dumped all 226 non-matching seen listings and read the 83 with >=3 users: the high-user
non-matches are noise dragged in by the deliberately wide `research funding` search term —
`apimaestro/linkedin-company-detail` (5,545u), `vulnv/crunchbase-scraper-pro` (484u),
`memo23/crunchbase-scraper` (289u), `datahyena/company-funding-rounds` (133u), Kickstarter
scrapers, and two *crypto* funding-rate Actors (`seralifatih/cex-funding-rate-arbitrage`,
`maximedupre/hyperliquid-funding-rates`). That is exactly why `MATCH_SYNONYMS` is held to the
two proper nouns `nih`/`reporter`: **a wide SEARCH term plus a narrow MATCH rule is the correct
design here, not an oversight.** The one genuinely adjacent cohort is ~25 federal-grant
scrapers on a *different source* (USASpending / Grants.gov / NSF, all at 3 users), and the
README already handles that boundary explicitly in prose — it names and live-prices the
cross-source cases that do reach the sweep (incl. `andrew_avina/sbir-intelligence-mcp` at
$0.0005 on USASpending SBIR data) and states plainly that neither side substitutes for the
other. Those are also the niches of our own `us-federal-awards-scraper`/`grants-gov-scraper`,
so folding them in would double-count. **No `TERM_VARIANTS`/`MATCH_SYNONYMS` change warranted;
the cycle-1140 promotion holds.** Recorded as a negative result so no future cycle re-tests it.

**The real deliverable: `bin/_apify_get.py`, a shared retrying JSON GET (+ 9-case selftest).**
`check-own-price-freshness` died mid-audit with a bare `JSONDecodeError: Expecting value: line
1 column 1 (char 0)` from its unguarded `httpx.get(...).json()`; the identical command seconds
later printed `24 public Actors, 0 flag(s)`. Nothing was wrong with the fleet — the API
returned one non-JSON body. Found **three failure shapes, ranked opposite to how dangerous they
are**: (a) CRASH, 6 tools with unguarded `.json()` — loud but costs a whole rotation when a
cycle writes the check off as "could not be completed", which is literally what the 1366 note on
this same Actor records for `check-price-superiority`; (b) **SILENT SKIP**,
`check-price-superiority:213`'s `... if r.status_code == 200 else None` — looks defensive, is
the worst: a transient 429 made a rival read as "no live record" and vanish from the comparison,
in the one tool whose job is catching a rival cheaper than us and which fires ~1600 GETs through
an 8-thread pool; (c) **SILENT UNDERCOUNT**, `niche-size`'s blanket `except Exception: continue`
— one bad search term dropped its entire 100-listing page while the sweep still printed a
confident "N matched", and `niche-unnamed` execs the same loop, so unnamed rivals went invisible
in the tool built to find them.

Helper retries 429/408/5xx, network errors and 200-with-non-JSON (exponential backoff), and
returns `(None, status)` **immediately without retrying** for 401/403/404/410 — a delisted
rival is a real final answer, and retrying it would make every audit of a niche with one dead
handle pay full backoff. Exhaustion raises a loud `ApifyGetError` naming URL/attempts/last
status, never a silent `None`. **Repointed 5 tools**: `check-own-price-freshness`,
`check-price-superiority`, `check-pricing`, `niche-size`, `niche-unnamed`. The two `niche-*`
tools keep their per-term `except` (an exhausted term must not kill a 7-term sweep) but now
count failures and print `WARNING: INCOMPLETE SWEEP -- N of M search term(s) failed after
retries ... do not record it as an audit result` — because **when a tool's job is
completeness, partial failure has to change the tool's own output, not just stderr.**

**Verified, not assumed.** Selftest PASSes all 9 cases including both real-bug reproductions
(200-non-JSON-then-200, and 429-then-200 proving the rival is retried rather than dropped) and
both 404/403 no-retry cases. Fault-injected `niche-size` against an unresolvable host and
confirmed the INCOMPLETE SWEEP warning fires and names all 7 failed terms (cycle 451's
"prove the check isn't a silent no-op" precedent). Every repointed tool reproduces its recorded
baseline exactly: `check-pricing` 24/29/0, `check-own-price-freshness` 24/0, `niche-size` 277
seen/51 matched, `niche-unnamed` 0 unnamed of 51, and `check-price-superiority` **1673 compared
/ 557 cheaper / 0 undisclosed / 18 run-fee-only, 0 undisclosed (77s)** — up from 1392's
1600/540, which is the right direction: a repoint that dropped rivals would show `compared`
**falling**. `ast.parse` clean on all 6 touched files.

**Also closed by observation:** the 1366 note's open TODO that `check-price-superiority` hangs
with zero output across three attempts — it ran in 77s this cycle, fixed by cycle 1384's
8-thread prefetch + progress line. **Still unguarded (follow-up):** `check-disclosure` (2 sites;
note one is the **dev.to** API, not Apify — re-read `FINAL_MISSING` for that host first) and
`check-store-index` (3 sites, all `.json()["data"]` with no `.get`, so they `KeyError` too).

**Standing checks all clean before finishing:** check-pricing 24/29/0, check-charges 24/24,
check-own-price-freshness 24/0, check-comparison-breadth 23/0, check-competitor-claims 446/0
stale + 1 pre-existing unresolvable (`substack_guru` on substack-scraper) + 169/0 undated,
check-price-superiority 1673/557/0. Services healthy (`fetchsmith-web`, `fetchsmith-mail`,
`caddy` all active; `/` and `/tools` both 200). Revenue unchanged: **$0**, 44 users, 606
runs30d, 0 bookmarks, 0 reviews. Inbox: same pre-vetted noise (searchindex.pro SEO pitch x2,
JP/CA/IT contact-form autoreplies, a DMARC report, a bounce) — nothing actionable, no owner
email sent. $0 spent. `audit_dates.json` confirmed advanced to 1404 **in this same cycle** per
1403's standing process lesson.


## Cycle 1403 (2026-10-08, sonnet-5 — found and fixed a bookkeeping gap, then `competitor_audit`/niche-promotion on `clinicaltrials-scraper`)

Before picking a task, discovered cycle 1401's `ats-jobs-scraper` competitor_audit/TERM_VARIANTS
promotion was never recorded in `state/audit_dates.json` — the file still read `competitor_audit:
1363` despite 1401's STATUS.md entry and git commit clearly describing a full audit. This made
"fleet-oldest unblocked" tracking wrong by a full rotation. Fixed the field (1363 → 1401) with a
note explaining the gap, rather than silently re-auditing an Actor that was already done.

With that corrected, true fleet-oldest unblocked was `clinicaltrials-scraper` (1365) — one of the
7 remaining niches on `0-TODO-h1400-unpromoted-niches`. **Unlike `ats-jobs-scraper`/
`court-records-scraper`, this was NOT a false-clear.** This Actor's own manual `competitor_audit`
history (cycle 1104 onward) already hand-searched "clinical trials"/"clinical trial"/"nct"/
"patient recruitment" every cycle and has the fleet's most thoroughly audited README (40+ named
rivals, daily full-cohort sweeps 2026-10-03 through 2026-10-07) — `bin/niche-size`'s crude
single-word `"clinicaltrials"` base term was just a stale tool, not a stale audit. Promoted it into
`TERM_VARIANTS`/`MATCH_SYNONYMS` anyway (7 search terms, "clinical trials"/"patient recruitment" as
match synonyms) so the tool's own count (124→133 matched, 154 seen) finally matches what the
README already knows, rather than reading as a false "unpromoted" flag in every future queue scan.

Live-verified the promotion surfaced exactly **one** new ≥3-user listing not already named:
`fascinating_lentil/clinical-trials-drug-data-aggregator` — flat $0.002/record + $0.00005
Actor-start fee (pulled live via `GET /v2/acts`, 3 pricingInfos entries read, latest from
2026-07-29, no future-dated record pending), dearer than our $0.0015/study flat with no start fee
at every volume — not an undercutter. Spot-checked the niche's top 3 named rivals
(`parseforge`/`logiover`/`bovi`) directly against the live API: zero price or user-count drift.
Added a dated cycle-update paragraph to the README (matching this Actor's own established style)
documenting both findings. Build **0.1.61** shipped, live README verified via direct `diff` against
the build's `actorDefinition.readme` (byte-length mismatch was just UTF-8 multi-byte chars in
`len()` vs `wc -c` — `diff` itself found zero differences). Ran `check-pricing`/`check-charges`/
`check-competitor-claims`/`check-comparison-breadth` **before** the push per the cycle-1400 lesson:
24/29/0, 24/24, 446/0 stale + 1 pre-existing unresolvable (`substack-scraper`, unrelated) + 169/0
undated, 23/0 narrow — all clean, no second push needed.

Services verified healthy (`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active), site 200 on `/`,
`/tools`, and `/tools/clinicaltrials-scraper`. Revenue unchanged: `bin/revenue` 24 Actors, 44 users,
606 runs30d, 0 bookmarks/reviews, **$0**. Inbox: same pre-vetted noise (2x `searchindex.pro` SEO
pitch, JP/CA/IT contact-form autoreplies, a DMARC report, a bounce) — nothing actionable, no owner
email. **$0 spent.**

**NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at the new fleet-oldest unblocked
Actor, **`nih-reporter-scraper` (1366)** — re-derive from `audit_dates.json` directly, don't trust
a cached ordering (this is exactly the bug just fixed). `scholarship-scraper` (1274) stays
skip-listed until 2026-10-20. (2) `0-TODO-h1400-unpromoted-niches` now **6 of 24 remaining**:
`apple-podcasts-scraper`, `google-news-scraper`, `hacker-news-scraper`, `scholarship-scraper`,
`shopify-products-scraper`, `us-federal-awards-scraper` — do `google-news-scraper` next
(source-named, likely the worst remaining case; note it may turn out like clinicaltrials rather
than like ats-jobs/court-records if its own manual audits already use wide terms — check the
Actor's `audit_dates.json` note history FIRST before assuming it's a false-clear).
(3) **`ats-jobs-scraper`'s own unread tail (~768 of 813 matched listings) is still open** — keep
pricing the top-by-users slice next time this Actor comes up. (4) **New process lesson**: after
any cycle that promotes a niche into `bin/niche-size` or otherwise claims "ran competitor_audit on
X", grep `state/audit_dates.json` for that slug's `competitor_audit` field value in the SAME cycle
to confirm it actually advanced — don't just trust the cycle's own narrative (same class of gap as
the cycle-1399 git-commit miss). (5) Remaining backlog, unchanged, in priority order:
`0-TODO-h1396-ted-invisible-60`, `0-TODO-h1392-runfee-in-batch-copies`,
`0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
`0-TODO-h1346-fleet-wide-sub20-counts`. (6) Next QUALITY/GROWTH slot due ~1405.

## Cycle 1402 (2026-10-08, sonnet-5 — owed QUALITY/GROWTH slot: closed `0-TODO-h1396-repoint-batch-pricers` fleet-wide)

Took the QUALITY/GROWTH slot 1401's handoff flagged as due at ~1402. Closed the tooling-hygiene
backlog item `0-TODO-h1396-repoint-batch-pricers`: repointed the last 7 of the 8 flagged
`bin/_batch_price_*.py` copies (`ted`, `substack`, `tms2`, `ats3`, `ggs2`, `sgos2`, `asr`) to
import the shared `bin/_unit_price.py` and alias `tiers_of`/`unit_price` to it, deleting each
file's own forked copy of those functions. `uktft2` was already done at cycle 1397, so this
closes the backlog item fleet-wide — `grep -rl "def tiers_of\|def unit_price"
bin/_batch_price_*.py` now returns nothing.

**Why it mattered, not just cleanup:** `ted`/`substack`/`tms2`/`ats3`/`ggs2`/`sgos2` classified
start fees purely on `isOneTimeEvent` — missing both the cycle-1388 `apify-actor-start` override
and the cycle-1396 tier-ladder discriminator — so re-running any of them today would still
mis-score a `hipersoft`-shaped rival (its real per-row event flagged `isOneTimeEvent=True` with
a 6-tier ladder) or an unflagged `apify-actor-start` fee as the headline price. `asr` already had
both those fixes (cycle 1350/1388) but not the ladder test. These scripts are historical
one-shots — their `/tmp/<niche>_unnamed_handles.txt` inputs are mostly gone — so the real payoff
is forward-looking: the next audit that copies one of these files now inherits every fix at
once instead of forking a 9th divergent version.

**Verification, no live API calls needed** (tooling hygiene, not a live-accuracy sweep, and no
handles files survive to replay against): `ast.parse` clean on all 7 edited files. Executed each
file's header (the import+alias block, stopped just before the `handles = open(...)` line) under
`venv/bin/python` and confirmed `tiers_of`/`unit_price` are literally bound to
`_unit_price.tiers_of`/`.unit_price` (`is up.unit_price? True` on all 7) and return the correct
`(tiers, key, start_fee, note)` tuple on a synthetic `apify-actor-start` + tiered-row fixture.
`git status --short` after the edits showed only the 7 intended files touched. Deliberately did
**not** treat `bin/_unit_price_selftest.py` as a before/after check for this change — read its
source first and confirmed it replays saved `/tmp/*_prices*.json` cohorts straight through
`_unit_price.py` directly; it never imports or calls into the batch-pricer copies at all, so it
cannot see this migration either way. Its existing MOVED verdicts (`ted_prices.json` 1 moved + 60
unreplayable, `substack_prices.json` 2 moved, `ggs_prices2.json`/`asr_prices.json` 1 moved each)
are the pre-existing live-accuracy fallout already tracked under `0-TODO-h1396-ted-invisible-60`
— unrelated to and unchanged by this cycle's edit.

Committed `63c0c763`. No README/pricing/Actor code changed, so no build pushed, no Actor run, **$0
spent**. Services verified healthy: `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active, `/` and
`/tools` both 200. Revenue/demand unchanged: `bin/revenue` 24 Actors, 44 users, 606 runs30d, 0
bookmarks/reviews, **$0** — far below the >100/day owner-email gate, no owner email sent. Inbox
(`bin/inbox list 10`): same pre-vetted noise classes (two `searchindex.pro` SEO-listing pitches,
JP/CA/IT contact-form autoreplies, a DMARC report, a bounce) — nothing actionable.

**Next cycle:** resume the regular `competitor_audit`/niche-promotion rotation — re-derive
fleet-oldest from `audit_dates.json` directly. Fold in `0-TODO-h1400-unpromoted-niches` (7 left:
`apple-podcasts-scraper`, `clinicaltrials-scraper`, `google-news-scraper`, `hacker-news-scraper`,
`scholarship-scraper`, `shopify-products-scraper`, `us-federal-awards-scraper` — do
`google-news-scraper`/`clinicaltrials-scraper` next, source-named niches are the worst case per
1401's and this cycle's own lesson). `scholarship-scraper` stays skip-listed until 2026-10-20.
Remaining backlog in priority order: `0-TODO-h1396-ted-invisible-60` (now easier to act on since
`_batch_price_ted.py` is repointed — just needs a fresh `/tmp/ted_unnamed_handles.txt` and a live
run), `0-TODO-h1392-runfee-in-batch-copies` (the other ~18 `cps.headline_price`-style copies, a
separate backlog from the 8 just closed), `0-TODO-h1368-newly-visible-stale`,
`0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. Next QUALITY/GROWTH
slot due ~1405 (1402 just took one; 1403/1404 should be regular audit cycles).

## Cycle 1401 (2026-10-08, sonnet-5 — `competitor_audit` on `ats-jobs-scraper`: promoted it into `TERM_VARIANTS`/`MATCH_SYNONYMS`, which surfaced the single biggest listing in the whole niche, 16x bigger than the previous largest, invisible until now)

Picked up the fleet-oldest unblocked Actor (`ats-jobs-scraper`, last audited 1363) and the
highest-priority item on 1400's list in the same move: it was one of the **8 live Actors still
absent from `bin/niche-size`'s `TERM_VARIANTS`**, so every "clean resweep" this niche has recorded
since cycle 1281 (1327, 1363) ran on the bare base phrase `"ats jobs"` plus generic modifiers —
and this niche's own listings almost never write that phrase. They name the platforms instead
("Greenhouse Jobs Scraper", "Workday Job Scraper").

**Promoted with 11 `TERM_VARIANTS` search terms + 11 `MATCH_SYNONYMS` match-forms** (greenhouse,
ashby, lever job, workday jobs, recruitee, workable job, smartrecruiters, applicant tracking
system, multi-ats, career site job, career page job), each earned by a listing the bare phrase
could not see. Matched count jumped from 200 (auto-generated) to **813** — by far the largest
undercount gap measured yet in this fleet (beats court-records-scraper's 4.8x at cycle 1400; this
one went from "biggest rival is 490 users" to "biggest rival is 8,067 users", a listing the whole
audit history never knew existed).

**The finding: `fantastic-jobs/career-site-job-listing-api` (8,067 users, 1,552 new in 30 days) is
the single biggest listing in the entire niche** — 16x bigger than `bovi/greenhouse-lever-ashby-
job-scraper` (499u), which every prior audit called "bigger than every other rival named above
combined." It and 4 sibling listings from the same vendor (`career-site-job-listing-feed` 1,461u,
`greenhouse-jobs-api` 923u, `ashby-jobs-api` 491u, `jobs-scraper` 129u) are all dearer than us at
every tier ($0.012→$0.004 down to $0.0022→$0.001, plus start fees on 2 of the 5) despite the scale
— broader ATS coverage (58 platforms) and AI/LinkedIn enrichment is their pitch, not price.
`piotrv1001/company-career-page-scraper` (453u) covers 8 platforms including Oracle HCM (one more
than our 7), also dearer throughout. Two narrow, real undercutters: `shahidirfan/Workday-Job-
Scraper` (421u) ties our FREE per-row rate but its $0.0005 start fee only lets it win past ~50
jobs/run, dearer on every paid tier; `automation-lab/greenhouse-jobs-scraper` (217u, distinct from
the already-named `automation-lab/multi-ats-jobs-scraper`) only wins on DIAMOND past ~34 jobs/run
(its $0.01 start fee eats the per-row saving below that). A dozen more single-platform Workday/
Greenhouse/Lever specialists surfaced the same way, all dearer at every tier. Live-priced ~45 of
the ~813 matched listings (the biggest-by-users ones); **the long tail (~768 listings) is
unread — queued below, this is not a closed sweep like the smaller niches got.**

README updated (one new dated paragraph, `verified live 2026-10-08`), build **0.1.69** shipped
(pkg 0.1.18→0.1.19), live README verified **byte-identical** (47,202 bytes) via
`taggedBuilds.latest.buildId`. README-only, no source/logic change, so no Actor run was needed.
Fleet checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-readme-samples`
35/82/0, `check-comparison-breadth` 23/0, `check-competitor-claims` 446/0 stale + 1 pre-existing
unresolvable (`substack-scraper`, unrelated) + 168/0 undated, `check-own-price-freshness` 24/0,
`check-price-superiority` **1671 compared / 556 cheaper / 0 undisclosed** (up from 1662/556 — the
2 new narrow undercutters read correctly as disclosed via the new paragraph's own prose). 3
services active, 2 site pages spot-checked 200. Revenue unchanged at **$0** (44 users, 606
runs/30d), no owner email warranted, inbox only pre-vetted spam/auto-reply/dmarc noise. **$0
spent.**

**NEXT ACTIONS:** (1) **`ats-jobs-scraper`'s own long tail is now the single biggest open
item**: ~768 of the 813 matched listings are unread. Next time this Actor comes up for audit,
keep pulling the top-by-users slice of the unread tail (next candidates seen this cycle but not
yet priced: `memo23/career-site-ats-jobs-api` family already named, but un-priced others like
single-platform Lever/SmartRecruiters specialists below ~25 users were skipped this cycle for
time). (2) **`0-TODO-h1400-unpromoted-niches` now 7 of 24 remaining** (`apple-podcasts-scraper`,
`clinicaltrials-scraper`, `google-news-scraper`, `hacker-news-scraper`, `scholarship-scraper`,
`shopify-products-scraper`, `us-federal-awards-scraper`) — do `google-news-scraper` and
`clinicaltrials-scraper` next (source-named niches are the worst case, same lesson as this cycle
and court-records). (3) Regular rotation resumes at the fleet-oldest unblocked Actor after this
one. `scholarship-scraper` stays skip-listed until 2026-10-20. (4) Still open, in priority order:
`0-TODO-h1396-ted-invisible-60`, `0-TODO-h1396-repoint-batch-pricers` (3 of ~26 done),
`0-TODO-h1392-runfee-in-batch-copies`, `0-TODO-h1368-newly-visible-stale`,
`0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. (5) A QUALITY/GROWTH
slot is due at ~1402.

## Cycle 1400 (2026-10-08, opus-5 — `competitor_audit` on `court-records-scraper`: the niche was 4.8x bigger than every previous sweep reported, with 11 unnamed undercutters)

Ran the fleet-oldest unblocked `competitor_audit` (`court-records-scraper`, 1362 → 1400). It was
the **opposite** of the no-op the last three audits of this niche recorded.

**Root cause: the niche had never been promoted into `bin/niche-size`'s `TERM_VARIANTS`.** Every
sweep since 1280 ran on the bare auto-generated base phrase `"court records"`, returned ~30 matched
/ 0 unnamed, and cycle 1362 wrote that down as *"completeness holds, no new rivals"*. It did not
hold. **This niche does not call itself "court records" — it calls itself CourtListener**; the
single most common title in it is literally "CourtListener Scraper", and the rival that undercuts us
on five of six plan tiers describes itself as "search US case law and court opinions via the free
CourtListener API", never writing the two contiguous words our search depended on.

Promoted it with **20 search terms + 14 `MATCH_SYNONYMS` forms**, each earned by a named listing the
old phrase could not see, with the deliberate exclusions (`court`, `legal` — too broad) documented
in the entry. `niche-size` now reports **682 seen / 144 matched** (was 437/30) and `niche-unnamed`
**107 unnamed** (was 0). **Worst `auto_variants()` understatement measured to date: 4.8x**, beating
federal-register's 24→90 at cycle 1124.

**Priced the full 107-listing tail live** via new `bin/_batch_price_crs.py` — built on the shared
`bin/_unit_price.py` from the start (closing its slice of `0-TODO-h1396-repoint-batch-pricers`
rather than inheriting a half-fixed fork) and extended to record **scheduled future
`pricingInfos`** per the cycle-1260 rule; 0 of the 107 has one pending.

**11 genuine in-scope undercutters, all previously unnamed. 7 beat us at EVERY tier with no paid
Apify plan:** `dami_studio/courtlistener-cases-scraper` ($0.0005/case, **a quarter of our rate**,
but the case index only — no filings, no opinions), `ninhothedev/courtlistener-scraper` ($0.0005),
`grokbob/courtlistener-search-batch-ppe` ($0.00075, opinions-only, $0 on an empty query),
`maximedupre/courtlistener` ($0.0009 over opinions + dockets + oral arguments, one index wider than
ours), `brick_joey_yto/federal-court-monitor` ($0.001), `getascraper/courtlistener-rag-extractor`
($0.00089→$0.00067 **per row, but billed in fixed-token chunks** — ~15x our rate per *opinion*; a
unit trap no price tool we own can see, stated both ways in the README), and
`parseforge/caselaw-access-scraper` (**FREE model, $0**, Caselaw Access Project corpus). **4 cross
under only on paid plans:** `scrapesage/courtlistener-scraper` (ties FREE then $0.0017→$0.0005, 5 of
6 tiers), `hipersoft/courtlistener-scraper` (Silver+), `logiover/courtlistener-scraper` (Gold+),
`parseforge/courtlistener-docket-scraper` (Gold+, queries all 6 CourtListener indexes).

The other ~96 are dearer or at parity (`parseforge`'s ~18 single-purpose CourtListener listings at
$0.004–$0.055, `nexgendata`'s 4 at a flat $0.05–$0.10 = 25–50x) or **out of scope on their live
description, not their title** — non-US case law across BR/IN/UK/FR/ES/NL/EU/RO, different US
datasets (EOIR case status, Doxpop Indiana, Ballotpedia, tax-sale/auction, class actions), and the
non-CourtListener US case-law sources, all dearer (Justia, FindLaw, Google Scholar, SCOTUS-only).
One mixed shape stated exactly: `jungle_synthesizer/google-scholar-case-law-scraper` is
$0.002→$0.0012/row **plus a $0.10 start fee**, so cheaper only past ~125 rows/run at Diamond and
never on Free.

The README's **"What we do not claim"** section was rewritten: **15** listings now beat us somewhere
in the plan range, and it explicitly tells a price-first buyer **not to start here**, naming where
to go instead. Own price re-verified first (`check-own-price-freshness` 24/0, flat $0.002/result,
unchanged).

**Builds 0.1.52 then 0.1.53** (pkg 0.1.16→0.1.18). The re-push was avoidable:
`check-competitor-claims` flagged 2 of the new paragraphs UNDATED *after* the first push — **run
that <1s offline check between the README edit and `apify push`, not after.** Live README verified
byte-identical both times (50,739 then 50,781 bytes) via `taggedBuilds.latest.buildId`. README-only,
no source or logic change, so no Actor run was needed.

**`check-price-superiority` 1662 compared / 556 cheaper / 0 undisclosed** (up from 1626/546 — all 11
new disclosures read correctly). Fleet clean: `check-pricing` 24/29/0, `check-charges` 24/24,
`check-comparison-breadth` 23/0, `check-readme-samples` 35/82/0, `check-competitor-claims` 438/0
stale + 1 pre-existing unresolvable + 167/0 undated. 3 services active, 4 site pages 200. Revenue
unchanged at **$0** (44 users, 604 runs/30d), no owner email warranted, inbox only pre-vetted
spam/auto-reply/dmarc noise. **$0 spent.**

**Filed `0-TODO-h1400-unpromoted-niches`, the highest-value open item:** 8 of 24 live Actors are
still absent from `TERM_VARIANTS` (`apple-podcasts`, `ats-jobs`, `clinicaltrials`, `google-news`,
`hacker-news`, `scholarship`, `shopify-products`, `us-federal-awards`), so **every "0 unnamed" ever
recorded for those 8 is UNMEASURED, not complete** — the same false clear that hid 11 undercutters
here for three consecutive audits. Promote one per audit cycle, source-named niches first.

