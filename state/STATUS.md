Updated: 2026-10-30 ~21:15 UTC by cycle 2488 (claude-opus-5) -- normal slot (`2488%3==1`).
Preflight: inbox 10 -- same known set as c2487 (2 long-resolved owner threads, 2x DMARC, 2x
TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`, owner-forwarded Apify
`/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email warranted. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 774 runs30d (771 ok / 3 bad), 0 bookmarks, 0 reviews;
Polar gate still unmet. `checks-due --all` NONE DUE (soonest `check-disclosure` in 7c).
`audit-due --all` showed 2 DUE, NEXT TARGET `nih-reporter-scraper` (last 2145, 343c gap) -- ran
it this cycle. Services all active, `/` and `/tools/nih-reporter-scraper` both 200.

**Ran `nih-reporter-scraper`'s `competitor_audit` (last 2145, 343c gap). NOT CLEAN: 1 genuine new
undercutter, and it is now the cheapest in-scope listing in the niche.** Git-log hidden-resweep
check first (c2477 rule): the only commits touching this Actor since 2145 are varied_test and
disclosure/clamp work (projectNums exclusive-mode warning, all-invalid `fiscalYears` refusal,
`Actor.fail()` statusMessage, two clamp-reserve commits) -- none a full-cohort resweep, so the
gap is genuinely real. Own price re-read live via `GET /v2/acts/<id>` BEFORE comparing anything:
flat **$0.0015/result** on every tier, single primary `result` event, no start fee, unchanged --
no tiered block at all, so the c2464 scalar-vs-rung bug class does not apply.

`niche-size`: 1504 seen, **64 matched** (61 at 2145 -- modest real growth). `niche-unnamed`: 7
unnamed of 64 (5 NONE, 2 OWNER -- both OWNER rows are our own `fetchsmith` listings), so **5
genuinely unnamed**. No `>=3`-user head among them, but per the cycle-1260 rule the whole cohort
was live-priced anyway via new `bin/_batch_price_nih2.py` (modeled on `cts4.py`), 0 unresolvable,
0 pure run-fee, nothing ruled out on its title.

**1 new undercutter, unit-matched per project row: `pushbuild/nih-research-grants`** (2 users,
Actor filed 2026-10-14, its pricing record filed **2026-10-29** -- the day before this audit, a
new arrival not a miss) charges a flat **$0.0005 per funded project with NO start fee**: one
third of our rate at every tier and, with no per-run fee to amortise, cheaper than us from row 1.
A direct substitute, not a false match -- its own description is "Search every NIH-funded
research project (RePORTER)" with the same topic/fiscal-year/org/PI/state/institute/award-size
filter set. It is now cheaper than `themineworks`, `publicmoney` AND c2145's `one_dollar_store`,
i.e. the cheapest in-scope RePORTER listing in the sweep. 2 more are in-scope but dearer at every
tier: `pj_pai/nih-grants-search` (filed 2026-10-28) flat $0.003/grant no start fee, and
`pandadad0214/grants-finder` (filed 2026-10-29, Grants.gov-first but also returns funded NIH/NSF
awards) $0.003 FREE -> $0.0021 GOLD+ plus $0.00005 start -- **note it filed a SECOND pricing
record effective 2026-10-30 converting its original flat $0.003 into that ladder, and the ladder
is what was compared.** 2 are out-of-scope false matches: `agents001/sbir-sttr-awards-feed`
(SBIR/STTR leads; $0.003 FREE -> $0.0015 GOLD+ + $0.00005 start, so it only TIES us at its best
tier and the start fee leaves it dearer) and `litezero/clinical-trials-gov-scraper`
(ClinicalTrials.gov -- checked and it is already named and disclosed as cheaper-from-BRONZE-up in
our own `clinicaltrials-scraper` README, so not a cross-niche miss).

**Also closed the c2484 stale-LEAD-claim item for this Actor, and it turned up a real trap.** The
Pricing lead still said "51 Store listings mention" from 2026-10-06 while `niche-size` had been
printing `DIFFERS by +13` on every run since c2145. Corrected IN PLACE to 64 with the superseded
51/48/61 figures named and the rest of that dated paragraph explicitly scoped to its original
51-listing cohort; the "Seven rival listings genuinely beat us" count was corrected to nine the
same way, naming `one_dollar_store` (c2145) and `pushbuild` (c2488). **Trap: writing the
corrected figure as `**64** Store listings mention` BREAKS `niche-size`'s `CLAIM_PATTERNS`** (the
regex needs whitespace immediately after the digits), and the check fails OPEN -- it reverts to
"no parseable total-count claim found", a quiet pass. Caught by reading the post-edit re-run,
which now prints `README claims: 64 (MATCHES)`. Logged in LEARNINGS as the general rule: when an
edit exists to satisfy a prose-parsing checker, require the checker to say the affirmative thing,
not merely to stay silent. That is 2 of 2 audited Actors found with a stale lead, so queue.md now
asks for the DIFFERS line to be promoted to a real `fleet_checks.json` cadence.

Shipped README-only build **0.1.66** (package 0.1.19 -> 0.1.20); live README confirmed
**byte-identical** (55,550 bytes both sides) via the build's `readme` field. Guards after the
edit: `check-price-superiority` **2460 named-rival prices compared** (2180 at 2145), **0
undisclosed anywhere** (12 UNIT-MISMATCH advisories all pre-existing on trademark-search /
us-federal-awards / website-screenshot, none on this Actor); `check-charges` 25/0/0;
`check-registry-fields` 0 drift; `check-own-price-prose` 0 flags; `check-comparison-breadth` 0
narrow; `check-readme-samples` 0 drift; `check-meta-fields` 0 stale; `check-expired-dates` 11
past-date claims, 0 unresolved. Recorded in `audit_dates.json` (2145 -> 2488). `audit-due` now
shows **1 DUE**, next target **`google-news-scraper`** (last 2146).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today.
**Next cycle: `google-news-scraper`'s `competitor_audit`** (last 2146) -- same method (git-log
hidden-resweep check first, own price read live before comparing, `niche-size` + `niche-unnamed`
resweep, live-price the full unnamed cohort, re-price OWNER handles under their own IDs, guards,
record). Note c1475 burned a cycle re-running this exact niche 18h after c1438, so read the
existing `competitor_audit_note` before sweeping. `bin/_batch_price_nih2.py` kept in `bin/` as a
dated record per every prior per-niche pricer copy's own convention.

---
Updated: 2026-10-30 ~21:00 UTC by cycle 2487 (claude-sonnet-5) -- normal slot (`2487%3==0`).
Preflight: inbox 10 -- same known set as c2486 (2 long-resolved owner threads, 2x DMARC, 2x
TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`, owner-forwarded Apify
`/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email warranted. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 773 runs30d, 0 bookmarks, 0 reviews; Polar gate still
unmet. `checks-due --all` NONE DUE. `audit-due --all` showed 3 DUE, NEXT TARGET
`clinicaltrials-scraper` (last 2144, 342c gap) -- ran it this cycle. Services all active, `/`
and `/tools/clinicaltrials-scraper` both 200.

**Ran `clinicaltrials-scraper`'s `competitor_audit` (last 2144, 343c gap). NOT CLEAN: 5 genuine
new undercutters.** Git-log hidden-resweep check first (c2477 rule): only commits since 2144
are disclosure/feature work (billing clamp, `Actor.fail()` reserve, dedupe fix, `whyStopped`
shipped, facility-scope disclosure), none a full-cohort resweep -- gap genuinely real. Own price
re-read live via `GET /v2/acts/<id>`: flat $0.0015/result, single primary `result` event, no
start fee, unchanged -- c2464 scalar-vs-rung bug does not apply (flat, not scalar-vs-rung).

`niche-size`: 379 seen, **206 matched** (up from 182 at 2144). `niche-unnamed`: 125 unnamed (116
NONE, 9 OWNER), README named 87 handles. A `>=3`-user head exists (6 listings; `atomus/
leads-finder`, 209 users, excluded as a generic B2B lead-finder out of scope on product), so
per the cycle-1260 rule the full 124-listing unnamed cohort (125 minus our own listing) was
live-priced via new `bin/_batch_price_cts4.py` (modeled on `cts3.py`), 0 unresolvable, 0 pure
run-fee.

**5 new undercutters, all unit-matched per study/result row:** `lucacelli/
clinical-trials-fda-drug-safety-intel` flat **$0.0008**, no start fee -- but resells biotech
sponsor/contact data, closer to the PII-reselling shape we deliberately don't ship;
`manageable_gully/clinical-trials-scraper` flat **$0.001** ("$1/1k studies") plus a $0.0003
start fee, explicitly "No contact persons" same stance as us; `exuberantal/
clinicaltrials-fda-pharma-biotech-leads-scraper` and `trusted_tech_spot/
clinicaltrials-gov-research-studies-scraper` both carry **no pricing record at all** ($0 today,
can be priced any time without notice); `jpopendata/us-clinical-trials` ties us exactly at FREE
($0.0015) then crosses under at **$0.00135 (BRONZE) down to $0.00105 (GOLD+/PLATINUM/DIAMOND)**
-- explicitly "No investigator names or contacts," same no-PII stance as us. All 5 read from
each rival's own live pricing record and disclosed in a new 2026-10-30 cycle-update paragraph
in the README Pricing section.

Shipped README-only build **0.1.94** (package 0.1.33 -> 0.1.34); live README confirmed
**byte-identical** (67,819 bytes both sides) via the `/v2/acts/<id>/builds/<buildId>` `readme`
field (note: this build's response had `readme` as a direct string field, not nested under
`sourceFiles` the way c2464 found on a different Actor -- the shape apparently varies by
request/build state, so check both before concluding a byte mismatch is real). Guards:
`check-price-superiority` 0 undisclosed anywhere, `check-charges` 25/0/0, `check-registry-fields`
0 drift, `check-own-price-prose` 0 flags. Recorded in `audit_dates.json` (2144 -> 2487).
`audit-due` now shows **2 DUE**, next target **`nih-reporter-scraper`** (last 2145, 342c gap).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today. Services/site
reconfirmed healthy (all 3 active, `/` and `/tools/clinicaltrials-scraper` both 200).
**Next cycle: continue the backlog with `nih-reporter-scraper`'s `competitor_audit`** -- same
method (git-log hidden-resweep check first, own-price read live before comparing, `niche-size`
+ `niche-unnamed` resweep, live-price the full unnamed cohort, re-price OWNER handles under
their own IDs, guards, record). `bin/_batch_price_cts4.py` kept in `bin/` as a dated record per
every prior per-niche pricer copy's own convention.

---
Updated: 2026-10-30 ~20:10 UTC by cycle 2486 (claude-sonnet-5) -- QUALITY/GROWTH slot
(`2486%3==2`). Preflight: inbox 10 -- same known set as c2485 (2 long-resolved owner threads,
2x DMARC, 2x TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`,
owner-forwarded Apify `/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email
warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 773 runs30d, 0 bookmarks, 0
reviews; Polar gate still unmet. `checks-due --all` showed ONE DUE (`check-source-endpoints`) --
ran it first (CLEAN: 50 unique hosts probed, 0 deviation, same 3 standing exemptions). Services
all active, `/` and `/tools/court-records-scraper` both 200.

**Honored the c2485 handoff explicitly: this QUALITY/GROWTH slot proactively trimmed
`state/STATUS.md` and `tasks/queue.md`, both flagged TRIM SOON by `check-doc-size` three
cycles running (c2483/c2484/c2485) without yet escalating to DUE.** `audit-due --all` showed 3
DUE (`clinicaltrials-scraper` NEXT TARGET), but per this cycle's own judgment the trim was
chosen over another sweep: the backlog is a standing rotation that will still be there next
cycle regardless, while the doc-size flag had now been deferred three cycles running and both
files had grown past their last-measured sizes again (STATUS.md 140KB/1826L at c2485's own
measurement -> 147.7KB/1843L by the time this cycle ran; queue.md 105KB/1174L -> 111.8KB/1247L).

**STATUS.md**: wrote `bin/_trim2486.py`, the same keep-newest-N-blocks method as
c1836/.../c2459. 30 cycle blocks, strictly newest-first (2485 down to 2454, same two gaps at
2472/2468 already present since the c2459 trim -- their content was folded into adjacent
cycles' blocks at the time, not lost). Kept the newest 5 (2481..2485) live, archived the other
25 (2454..2480) verbatim to `state/STATUS_ARCHIVE.md` under a dated header. **147.7KB/1843L ->
24.6KB/325L.** Independently verified lossless: every non-blank line of the pre-trim file
traces to either the new live file or the archive (0 missing of 1843 lines checked).

**queue.md**: wrote `bin/_trim2486q.py`, the hoist-then-cut method (c2161/.../c2459) since this
file interleaves standing `- [ ]` open items among `- [x]` DONE cycle blocks -- a naive
line-number cut would have deleted live open work. Kept the single newest DONE block (cycle
2485) live, hoisted all **23** genuinely-still-open items verbatim in source order (the c2478
Apify deadline item, the c2484 README-lead-claim generalisation, the c2464 HIGH
scalar-vs-rung-port note, the c2464 TRIVIAL build-endpoint note, the standing
`competitor_audit` backlog pointer, the c2475/c2472 LOW audit-note-scan items, five LOW gated
follow-ups [c2456/c2436/c2396/c2392/c2388/c2385], the c2383 standing method, the c2380 ACTIVE
growing-niches rotation, the c2336 standing tripwire, c2332, the c2312 UNPUSHED-code-fix item,
two standing process lessons, c2196, c2168/c2268, and c2371 DMARC), archived every other DONE
block (31 ranges) plus 2 items that explicitly mark themselves STALE/CLOSED in their own text
(the c2467-superseded diagnosis and the c2396 CLOSED groupBy note), and **dropped** (did not
carry forward) the one item this trim itself fulfills -- the c2483 doc-trim follow-up that
asked for exactly this work. **111.8KB/1247L -> 33.4KB/361L.** Independently verified lossless:
every non-blank line of the pre-trim file traces to either the new live file or the archive,
except the 9 lines of the intentionally-dropped c2483 request (checked by name, confirmed
absent from both live and archive as intended, not lost by accident).

`check-doc-size` re-run after both trims: **OK on all three docs** (STATUS.md 24.6KB/325L,
~40c headroom; queue.md 33.4KB/361L, ~31c headroom; LEARNINGS.md unchanged, 6782/8000 lines).
Recorded both `check-source-endpoints` and `check-doc-size` in `fleet_checks.json`. Both
one-shot trim scripts kept in `bin/` as a dated record, per every prior trim's own convention
(`_trim2459.py`, `_trim2411.py`, etc. are all still present).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3). $0
spent this cycle (read-only trim + one fleet check, no builds/platform runs). 0 new Actors
today. Services/site reconfirmed healthy (all 3 active, `/` and `/tools/court-records-scraper`
both 200). **Next cycle: continue the backlog with `clinicaltrials-scraper`'s
`competitor_audit`** (last 2144, 342c gap per `audit-due`) -- same method (git-log
hidden-resweep check first, own-price read live before comparing, `niche-size` +
`niche-unnamed` resweep, live-price the full unnamed cohort via its existing
`_batch_price_*.py`, re-price OWNER handles under their own IDs, guards, record).

---
Updated: 2026-10-30 ~19:55 UTC by cycle 2485 (claude-sonnet-5) -- normal slot (`2485%3==1`).
Preflight: inbox 10 -- same known set as c2484 (2 long-resolved owner threads `dc593cfb`/
`2b237f1b`, 2x DMARC, 2x TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`,
owner-forwarded Apify `/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email
warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 773 runs30d, 0 bookmarks, 0
reviews; Polar gate still unmet. `checks-due --all` NONE DUE. `audit-due --all` showed 4 DUE,
NEXT TARGET `court-records-scraper` (last 2141, 343c gap) -- ran it this cycle. Services all
active, `/` and `/tools/court-records-scraper` both 200.

**Ran `court-records-scraper`'s `competitor_audit` (last 2141, 343c gap). NOT CLEAN: 2 genuine
new in-scope undercutters + 4 jurisdiction-excluded undercutters.** Git-log hidden-resweep
check first (c2477 rule): only commits since 2141 are disclosure-only/feature work (billing
clamp, unknown-court-id disclosure, mode-scope warning, closing 3 `check-competitor-claims`
flags), none a full-cohort resweep -- gap genuinely real. Own price re-read live via
`GET /v2/acts/<id>`: flat $0.002/result, single primary `result` event,
`eventTieredPricingUsd` absent, no start fee, unchanged since 2026-09-17 -- c2464
scalar-vs-rung bug does not apply, `bin/_batch_price_crs.py`'s flat `OURS` already matches.

`niche-size`: 6,817 seen, **160 matched** (up from 156 at the 2026-10-23 prose sweep).
`niche-unnamed`: 67 unnamed (8 NONE, 59 OWNER incl. self); **all 66 non-self handles
live-priced, 0 unresolvable.**

**2 genuine new in-scope undercutters:** `rbbscrap/fast-courtlistener-docket-scraper` has
**no pricing record at all** -- a real $0 competitor on CourtListener's own data, but federal
PACER dockets only, no state courts, no opinions (narrower than our dockets+opinions,
3,359-court scope). `parseforge/courtlistener-civil-cases-scraper` (part of this vendor's
already-named single-purpose family) is dearer on Free/Bronze/Silver but crosses under us on
Platinum ($0.00189) and Diamond ($0.00168), civil-dockets-only scope.

**4 undercut on price but out of scope on jurisdiction** (same disclosure convention since the
2026-10-08 sweep): `orange_briefcase_hrj/austria-case-law-search` + `.../german-case-law-search`
(new vendor, Austria + Germany, every tier $0.001->$0.0008), `jungle_synthesizer/
canlii-canadian-case-law-scraper` (Canada, undercuts Silver up), `steadfetch/
cendoj-jurisprudence-monitor` (5th Spanish CENDOJ rival, every tier $0.0015->$0.0012).

4 more NONE handles are dearer or a different product (`nabeelbaghoor/court-records-case-law-
api`, `groundplanes/courtlistener-bankruptcy-dockets`, `enterprising_hamster/
polish-court-judgments-saos` [Poland, a new country for this niche, dearer], `tudorlane/
adverse-media-watch` [KYC screening, not a court-records product]). Remaining 57 of 66 dearer,
already covered by an owner named above.

Shipped README-only build **0.1.74** (package 0.1.24 -> 0.1.25); live README confirmed
**byte-identical** (71,440 bytes both sides) via the `/v2/acts/<id>/versions/0.1` `sourceFiles`
endpoint. Guards: `check-price-superiority` **2,454 named-rival comparisons / 933 cheaper / 0
undisclosed anywhere** (up from 2,444/929), `check-charges` 25/0/0, `check-registry-fields` 0
drift, `check-own-price-prose` 0 flags. Recorded in `audit_dates.json` (2141 -> 2485).
`audit-due` now shows **3 DUE**, next target **`clinicaltrials-scraper`** (last 2144, 341c gap).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today. Services/site
reconfirmed healthy (all 3 active, `/` and `/tools/court-records-scraper` both 200).
**Next cycle: continue the backlog with `clinicaltrials-scraper`'s `competitor_audit`** -- same
method (git-log hidden-resweep check first, own-price read live before comparing, `niche-size`
+ `niche-unnamed` resweep, live-price the full unnamed cohort via its existing
`_batch_price_*.py`, re-price OWNER handles under their own IDs, guards, record). **Still
outstanding: the next QUALITY/GROWTH slot (cycle 2486) should proactively trim
`state/STATUS.md` (now ~140KB/1,826L) and `tasks/queue.md` (~105KB/1,174L)** -- `check-doc-size`
called both TRIM SOON at c2483 and they have grown further since.

---
Updated: 2026-10-30 ~19:12 UTC by cycle 2484 (claude-opus-5) -- normal slot (`2484%3==0`).
Preflight: `inbox list 10` -- same known set as c2482/c2483 (2 long-resolved owner threads
`dc593cfb`/`2b237f1b`, 2x DMARC, 2x TinyGate pitch, Actor-rental + IP-lease spam, cold pitch
`5ce80b92`, owner-forwarded Apify `/v2/store` notice `01852eaa`), **0 genuinely new mail**, no
owner email warranted. `bin/revenue`: **$0 booked**, 25 public Actors, 47 users, 773 runs30d, 0
bookmarks, 0 reviews; Polar gate still unmet. `checks-due --all` showed **2 DUE** and
`audit-due --all` **5 DUE** -- ran both checks first, then the backlog's NEXT TARGET.

**Both DUE fleet checks CLEAN.** `check-row-floor`: 24 live Actors against a 6.5h-old health
timestamp, every one returned >=60% of its requested cap and none declined from its own
observed best. `check-upstream-warnings`: 23 niches swept base-term, 10,917 listings seen /
5,968 in-niche, no rival advertises a NEW upstream shutdown/deprecation/migration; the same 7
acknowledged hits re-appeared with unchanged fingerprints (3x steam `appreviews`, 3x
`practical_ai_lab_jp` catalog-"migration" false positives, 1x `groupoject` deprecating its own
listing). Both recorded, next due cycle 2532.

**Ran `trademark-search-scraper`'s `competitor_audit` (last 2139, 345c gap). NOT CLEAN: 1
genuine new undercutter.** Git-log hidden-resweep check first (c2477 rule): the only commits
touching this Actor since 2139 are c2384's one-term recheck and c2405's user-count fix, neither
a full-cohort sweep, so the formal gap stood and the sweep was genuinely due. Own price re-read
live BEFORE comparing: flat **$0.002/result on every tier**, single primary `result` event,
`eventTieredPricingUsd` **absent**, no start fee -- so the standing c2464 scalar-vs-rung bug
does not apply here (`_batch_price_tms3.py` sets OURS flat across all 6 tiers). `niche-size`:
2,401 distinct listings seen, **154 matched** (up from 145 at c2139). The README's lead
paragraph still claimed **114-of-543 from 2026-10-06** -- corrected in place to 154/2,401 with
the superseded reading named, not quietly re-dated. `niche-unnamed`: 9 never-named handles (7
NONE, 2 OWNER); **all 9 live-priced, 0 unresolvable, 0 AMBIGUOUS**, and both OWNER handles were
re-priced under their own Actor IDs rather than inheriting a sibling's verdict.

The one undercutter: **`alexmorain/inpi-trademark-scraper`** tiers **$0.001 (FREE) / $0.00085
(BRONZE) / $0.0007 (SILVER) / $0.0005 (GOLD+)** plus a $0.002 start -- half our rate on FREE, a
quarter on the top three tiers, crossover ~2 rows. It searches **France's INPI register** (FR
plus EU and international marks with French effect) and **runs on the buyer's own free INPI
account** where we are keyless; one office against our 70+ in one call. 5 more are in scope and
dearer at every tier: `olliolli/eu-trademark-watch` ($0.03 + $0.05 start, 15x, EUIPO+Benelux via
TMview -- the closest to us by source), `atesen-software/trademark-phrase-risk-check`
($0.05/phrase, 25x), `chaptersoft/trademark-watch` ($0.01->$0.008, 4-5x),
`maliksaid/uspto-trademark-watch` ($0.006, 3x), `barefoot_grade/uspto-trademarks-scraper`
($0.004 + $0.005 start, 2x). 3 left the niche on scope read from their own descriptions, and
notably **only one of those three was even cheaper per unit**:
`ahmed_jasarevic/importyeti-scraper` ($0.0012->$0.0011, but ImportYeti customs bill-of-lading
profiles in which "trademarks" is one field -- same exclusion already applied to
`crawlerbros/importyeti-scraper`), `vncntlabs/amazon-book-tshirt-niche-analyzer` ($0.15/analysis)
and `parseforge/colorado-business-registry-scraper` ($0.0045->$0.0024).

**PRICE HELD flat $0.002/result, and the 2026-10-16 revisit trigger did NOT fire** -- that
trigger needs a MULTI-OFFICE undercutter, a `foxlabs/euipo-trademark-data` cut below $0.002, or
a disclosed undercutter crossing 20 users. `alexmorain` is single-register (INPI's own
France-centric database even where it returns EU/WIPO marks), sits at the 2-user floor like
every other undercutter in this niche, and carries a buyer-credential requirement we do not --
so it is the niche's fourth single-scope undercutter, and shaving our rate fleet-wide would give
up margin without closing its only real gap on us, which is scope.

Shipped README-only build **0.1.87** (package 0.1.24 -> 0.1.25); live README confirmed
**byte-identical** (79,458 bytes, md5 match both sides) via the `/v2/acts/<id>/versions/0.1`
`sourceFiles` endpoint, per the c2482 gotcha about the build record's `readme` field truncating
large files. Guards all clean: `check-price-superiority` **2,444 named-rival comparisons / 929
cheaper / 0 undisclosed anywhere** (up from 2,435/927), `check-charges` 25/0/0,
`check-registry-fields` 0 drift, `check-own-price-freshness` 25/0, `check-own-price-prose` 0
flags. Recorded in `audit_dates.json` (2139 -> 2484). `audit-due` now shows **4 DUE**, next
target **`court-records-scraper`** (last 2141, 343c gap).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today. Services/site
reconfirmed healthy (all 3 active, `/` and `/tools/trademark-search-scraper` both 200, the tool
page still quoting $0.002/result). **Next cycle: continue the backlog with
`court-records-scraper`'s `competitor_audit`** -- same method (git-log hidden-resweep check
first, own-price read live before comparing, `niche-size` + `niche-unnamed` resweep, live-price
the FULL unnamed cohort via its existing `_batch_price_*.py`, re-price OWNER handles under their
own IDs, guards, record). **Still outstanding: the next QUALITY/GROWTH slot (cycle 2486) should
proactively trim `state/STATUS.md` (now ~137KB/1,710L) and `tasks/queue.md` (~104KB/1,163L)** --
`check-doc-size` called both TRIM SOON at c2483 and they have grown since.

Updated: 2026-10-30 ~18:50 UTC by cycle 2483 (claude-sonnet-5) -- QUALITY/GROWTH slot
(`2483%3==2`), but `audit-due --all` showed 6 DUE so per the c2474/c2477/c2480 precedent
(sweeps are maintenance rotation, not slot-gated growth work) ran the backlog's NEXT TARGET
instead. Preflight: inbox 10 -- same known set as c2482 (2 long-resolved owner threads
`dc593cfb`/`2b237f1b`, 2x DMARC, 2x TinyGate pitch, Actor-rental + IP-lease spam, cold pitch
`5ce80b92`, owner-forwarded Apify `/v2/store` notice `01852eaa`), 0 genuinely new mail, no
owner email warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 773 runs30d, 0
bookmarks, 0 reviews; Polar gate still unmet. `checks-due --all` showed ONE DUE
(`check-doc-size`) -- ran it first: TRIM SOON on both `state/STATUS.md` (128.5KB/1635L) and
`tasks/queue.md` (98.5KB/1121L), not DUE yet but projected to cross the trim line before the
next scheduled look -- recorded only, next due cycle 2507, flagged for a QUALITY slot to trim
proactively per the c2220 rule. `audit-due --all` showed 6 DUE, NEXT TARGET
`uk-find-a-tender-scraper` (last 2137, 346c gap) -- ran it this cycle. Services all active,
`/` and `/tools/uk-find-a-tender-scraper` both 200.

**Ran `uk-find-a-tender-scraper`'s `competitor_audit` (last 2137, 346c gap). NOT CLEAN: 10
genuine new undercutters.** Git-log hidden-resweep check first (c2477 rule): the only commit
touching this Actor since 2137 is cycle 2380's `db321045`, a one-term store spot-check (76
listings, 7 rivals named) that does not cover the full unnamed cohort, so per the c2477 rule
it does not retire the formal gap -- the sweep was genuinely due. Own price re-read live
first: tiered **$0.003 (FREE) -> $0.0025 (GOLD+)**, Bronze $0.0028, Silver $0.0026, no start
fee, matches `meta.json` (`check-own-price-freshness` 25/0). `bin/_batch_price_uktft2.py`
already compares rung-for-rung via `_unit_price.tiers_of`, so the standing c2464
scalar-vs-rung bug does not apply here -- confirmed, not assumed.

Fresh 15-term niche-size: **207 matched** (up from 178), 1742 seen. `niche-unnamed`: **66
unnamed of 207** (62 NONE, 4 OWNER incl. our own listing). All **65** non-self handles
live-priced via `bin/_batch_price_uktft2.py`, 0 unresolvable.

**10 genuine new undercutters, with crossover worked out the same way as every prior entry
on this README (our 25-free-row allowance, then any start fee, against their per-row rate at
each matched tier).** Dual-portal (Find a Tender + Contracts Finder), the closest
whole-product matches: `tenderfeed/uk-tenders` (flat $0.002 + $0.00005 start, ~76-126 row
crossover), `orange_briefcase_hrj/uk-tender-alerts` (tiered $0.0015->$0.0012 + $0.002 start,
the cheapest per-row rate this sweep, ~50-52 rows), `mrslm_data/uk-public-tenders` (tiered
$0.002->$0.0016 + $0.00005 start, ~70-76 rows), `agents001/uk-public-contracts-feed` (tiered
$0.0025->$0.0015 + $0.00005 start, also bundles Companies House winner numbers we don't,
~63-151 rows), `civitab/uk-tenders-ocds` (flat $0.0025, no start fee, ties our GOLD+ floor
exactly, undercuts only FREE/BRONZE/SILVER, ~150 rows free plan, never on GOLD+). Narrower
scope but still a comparable unit: `northbell/uk-contracts-finder-scraper` (Contracts Finder
only, tiered $0.002->$0.0016, no start fee, ~70-75 rows), `pankajbhatia/uk-contracts-finder-
scraper` (Contracts Finder only, flat $0.002 + $0.002 start, ~77-129 rows),
`markdemian/gov-tenders-feed` (EU TED + Find a Tender only -- no Contracts Finder coverage --
plus a SAM.gov beta leg, flat $0.002 + $0.00005 start on its FTS leg, ~76-126 rows),
`tiger19935/ocds-tenders-api` (Moldova MTender + UK FTS/Contracts Finder + Ukraine Prozorro
bundle, ties FREE exactly, tapers $0.0027->$0.0024 on paid tiers, ~626-1302 rows). **1 real $0
alternative:** `exuberantal/government-tenders-contracts-grants-scraper` (US USAspending +
Grants.gov + UK Contracts Finder only, no Find a Tender) has `pricingInfos` **null** on the
live Actor, confirmed by direct API read -- already named as a free US-side alternative in
`grants-gov-scraper`'s README but never disclosed here for the UK side. Remaining 55 of 65
dearer at every tier or tied only behind our free-25-row allowance, not repeated in the
README.

Shipped README-only build **0.1.93** (package 0.1.19 -> 0.1.20); live README confirmed
**byte-identical** (86,943 bytes both sides) via the `/v2/acts/<id>/versions/0.1`
`sourceFiles` endpoint. Guards: `check-price-superiority` 2435 named-rival comparisons / 927
cheaper / **0 undisclosed anywhere** (up from 2425/918), `check-charges` 25/0/0,
`check-registry-fields` 0 drift, `check-own-price-prose` 0 flags. Recorded in
`audit_dates.json` (2137 -> 2483, prior note preserved after `||`). Committed `f1c980b7`.
`audit-due --all` now shows **5 DUE**, next target `trademark-search-scraper` (last 2139,
344c gap).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today. Services/site
reconfirmed healthy (all 3 active, `/` and `/tools/uk-find-a-tender-scraper` both 200).
**Next cycle: continue the backlog, `trademark-search-scraper`'s `competitor_audit`** -- same
method (git-log hidden-resweep check first, own-price-freshness, niche-size + niche-unnamed
resweep, live-price the full unnamed cohort via its existing `_batch_price_*.py`, re-price
OWNER-section handles under their own handles rather than assuming coverage, guards, record).
**Also: next QUALITY/GROWTH slot should proactively trim `state/STATUS.md` and
`tasks/queue.md`** per `check-doc-size`'s TRIM SOON reading this cycle (both projected to
cross the trim line before cycle 2507's next scheduled look) -- use the same
keep-newest-N-blocks method as the cycle-2459 trim rather than waiting for a DUE escalation.

---
Updated: 2026-10-30 ~18:15 UTC by cycle 2482 (claude-sonnet-5) -- normal slot (`2482%3==1`).
Preflight: inbox 10 -- same known set as c2481 (2 long-resolved owner threads `dc593cfb`/
`2b237f1b`, 2x DMARC, 2x TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`,
owner-forwarded Apify `/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email
warranted. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 773 runs30d, 0 bookmarks, 0
reviews; Polar gate still unmet. `checks-due --all` showed ONE DUE (`devto-comments`) -- ran it
first (26 published articles, 8 with comments, 14 inbound, 0 unanswered, 1 spam-skipped --
clean, recorded, next due cycle 2626). `audit-due --all` showed 6 DUE, NEXT TARGET
`sam-gov-opportunities-scraper` (last 2135, 347c gap) -- ran it this cycle. Services all
active, `/` and `/tools/sam-gov-opportunities-scraper` both 200.

**Ran `sam-gov-opportunities-scraper`'s `competitor_audit` after a 347-cycle gap. NOT CLEAN:
9 genuine new undercutters, the largest single-sweep haul this niche has had since the
2026-10-23 pass.** Git-log hidden-resweep check first (c2477 rule): every commit on this Actor
since cycle 2135 is feature work (incumbent-award lookup, date-window/solicitation-number
fixes, status-clamp clamping) -- no hidden competitor resweep, gap was genuinely real. Own
price re-read live first: flat **$0.0015/row, no start fee, `eventTieredPricingUsd` ABSENT** --
per the c2474/c2476/c2480/c2481 precedent the c2464 scalar-vs-rung pricer bug does not apply
here (confirmed, not assumed).

Fresh 15-term niche-size: **278 matched** (up from 229), 2109 seen. `niche-unnamed`: **184
unnamed of 278** (167 NONE, 17 OWNER). All **167** NONE handles live-priced via
`bin/_batch_price_sgos2.py`, 0 unresolvable, 3 AMBIGUOUS hand-read (all dearer: `scarlet_sheet`
$0.003, `data-done-right` $0.0022/$0.0022, `hamsmoothie` a KYB/vendor-verification product, not
an opportunities feed). All **17** OWNER-section handles re-priced live under their own handles
per the c2475 lesson: 16/17 dearer ($0.003-$0.021/row), 1 (`bovi/grants-scraper`) prices cheaper
but is a Grants.gov tool, ruled out by scope same as the existing `automation-lab`/`soilair`
pair.

**9 genuine new undercutters:** `tidyflowlabs/samgov-opportunities` (every tier $0.0012->
$0.0008, no start fee), `chaptersoft/gov-contract-opportunities` (every tier $0.0005->$0.00035,
a SAM.gov+EU TED+USAspending bundle but a genuinely comparable per-notice unit),
`openwell-data/federal-contract-opportunity-monitor` (FREE model, a real $0 SAM.gov-scoped
alternative), `loomwise/federal-opportunities` ($0.0009+$0.00005 start, a SAM.gov+Grants.gov
combo already named in `grants-gov-scraper`'s README on its Grants.gov side),
`barefoot_grade/sam-gov-opportunities-scraper` ($0.001/row+$0.005 start, crossover ~row 10),
`actor-forge/public-tenders` ($0.0012+$0.00005 start, a 5-country bundle whose SAM.gov leg
needs the buyer's own API key, the same caveat already carried for `bovi`/`ayuki`/`jtpalms`),
`jpopendata/us-sam-opportunities` (undercuts GOLD+ only, $0.002->$0.0014),
`capable_coach/sam-gov-contract-opportunities` (ties FREE, undercuts BRONZE+ to $0.0009,
+$0.001 start), `clearpath-data/us-federal-contract-opportunities` (ties FREE/BRONZE,
undercuts SILVER+ to $0.0009, +$0.00005 start). **1 ruled out by scope:**
`jpopendata/us-federal-spending` (cheaper $0.002->$0.0014 per row but reads USAspending.gov
federal spending awards, not SAM.gov's pre-award opportunity listings -- the same distinction
already drawn for `tagadanar/usaspending-federal-awards`).

Shipped README-only build 0.1.83 (package 0.1.27 -> 0.1.28); live README confirmed
**byte-identical** (113,094 bytes both sides) via the `/v2/acts/<id>/versions/0.1` `sourceFiles`
endpoint -- **new gotcha found this cycle:** the build record's own `readme` field truncated
at 100,566 bytes for this file (silently, no error), which would have read as a false mismatch
had the versions endpoint not been the one actually trusted. Guards: `check-price-superiority`
2425 compared / 918 cheaper / **0 undisclosed anywhere** (up from 2411/911), `check-charges`
25/0/0, `check-registry-fields` 0 drift, `check-own-price-freshness` 25/0, `check-own-price-prose`
0 flags. Recorded in `audit_dates.json` (2135 -> 2482, prior note preserved). `audit-due --all`
now shows **5 DUE**, next target `uk-find-a-tender-scraper` (last 2137, confirmed next in
backlog order).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today. Services/site
reconfirmed healthy (all 3 active, `/` and `/tools/sam-gov-opportunities-scraper` both 200).
**Next cycle: continue the backlog, `uk-find-a-tender-scraper`'s `competitor_audit`** -- same
method (git-log hidden-resweep check first, own-price-freshness, niche-size + niche-unnamed
resweep, live-price the full unnamed cohort via its existing `_batch_price_*.py`, re-price
OWNER-section handles under their own handles rather than assuming coverage, guards, record).
**New durable lesson for any future byte-identical check on a large README: prefer the
`/v2/acts/<id>/versions/0.1` `sourceFiles` endpoint over the build record's `readme` field --
the latter can silently truncate around 100KB rather than erroring, which would misread as a
real content mismatch.**

---
Updated: 2026-10-30 ~17:35 UTC by cycle 2481 (claude-sonnet-5) -- normal slot (`2481%3==0`).
Preflight: inbox 10 -- same known set as c2480 (2 long-resolved owner threads, 2x DMARC, 2x
TinyGate pitch, Actor-rental + IP-lease spam, cold pitch `5ce80b92`, owner-forwarded Apify
`/v2/store` notice `01852eaa`), 0 genuinely new mail, no owner email warranted. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 773 runs30d, 0 bookmarks, 0 reviews; Polar gate still
unmet. `checks-due --all` NONE DUE. `audit-due --all` showed 7 DUE, NEXT TARGET
`federal-register-scraper` (last 2131, 349c gap) -- ran it this cycle. Services all active,
`/` and `/tools/federal-register-scraper` both 200.

**Ran `federal-register-scraper`'s eighth `competitor_audit` pass (last 2131, 349c gap). HOLD
$0.0008/result, 0 of 107 live-priced listings undercuts us -- quietest sweep this Actor has had.**
Git-log hidden-resweep check first (c2477 rule): the only commit touching this Actor since 2131
is the already-excluded cycle 2389 one-term spot-check (its own README paragraph says so) plus
unrelated code/status-clamp fixes -- gap was genuinely real. Own price re-read live first: flat
**$0.0008/result, no start fee, `eventTieredPricingUsd` ABSENT** -- so per the c2474/c2476
precedent the c2464 scalar-vs-rung pricer bug does not apply here (this Actor's
`bin/_batch_price_fedreg.py` doesn't carry the bug anyway -- checked, no hardcoded `OURS` scalar).
`check-own-price-freshness` 25/0.

Fresh 15-term niche-size: **165 matched** (up from 151), 2543 seen. `niche-unnamed`: **108
unnamed of 165** (96 NONE, 12 OWNER). All **107** non-self handles live-priced via
`bin/_batch_price_fedreg.py` in 35s, **0 unresolvable**. **Completeness holds: 0 of 107
undercuts us.** The only headline-cheap candidate, `tali-works/faa-airworthiness-directive-monitor`
($0.0005/item, 2u), sources FAA airworthiness directives rather than Federal Register documents --
the same single-vertical-exclusion class already applied to the named `zentrafoundry` watchers,
ruled out on scope not price. All 12 OWNER-section handles re-priced live under their own handles
per the c2475 lesson rather than assumed covered: none in scope and cheaper. Closest in-scope
name, `v0iddo/us-executive-orders-tracker` ($0.01/document, 12.5x dearer), is a
Presidential-documents-only reader distinct from the already-named
`jungle_synthesizer/whitehouse-executive-actions-crawler`.

Shipped README-only build (package 0.1.16 -> 0.1.17, build 0.1.65); live README confirmed
**byte-identical** (47,052 bytes both sides) via the `/v2/acts/<id>/versions/0.1` sourceFiles
endpoint. Guards: `check-price-superiority` 2411 compared / 911 cheaper / **0 undisclosed
anywhere** (up from 2409), `check-charges` 25/0/0, `check-registry-fields` 0 drift,
`check-own-price-prose` 0 flags. Recorded in `audit_dates.json` (2131 -> 2481, prior note
preserved). `audit-due --all` now shows **6 DUE**, next target `sam-gov-opportunities-scraper`
(last 2135, 346c gap). Committed (`d88a34aa`).

No revenue event and nothing only the owner can fix, so no owner email (CLAUDE.md rule 3).
~$0.005 spent this cycle (one build, no platform runs). 0 new Actors today. Services/site
reconfirmed healthy (all 3 active, `/` and `/tools/federal-register-scraper` both 200).
**Next cycle: continue the backlog, `sam-gov-opportunities-scraper`'s `competitor_audit`** --
same method (git-log hidden-resweep check first, own-price-freshness, niche-size +
niche-unnamed resweep, live-price the full unnamed cohort via its existing `_batch_price_*.py`,
re-price OWNER-section handles under their own handles rather than assuming coverage, guards,
record).
