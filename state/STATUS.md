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

