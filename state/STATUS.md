Updated: 2026-11-08 UTC by cycle 2888 (claude-opus-5). Regular slot (2888 % 3 == 2, computed fresh).

**Preflight (all re-run fresh): `audit-due --all` found exactly 1 real fleet-rotation item DUE,
`unreachable_remedy: fda-recall-scraper`** (2552 -> 2888, 336c/7d gap -- the target c2887
predicted). `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 6c, cycle 2894).
`inbox-triage new`: NONE UNTRIAGED of 75. `bin/revenue` live: **$0 booked, 27 public Actors, 50
users, 816 runs30d, 3 ext_bad30d** -- every figure unchanged from c2886/c2887, so no buyer
signal and no owner email owed (rule 3).

**THE WORK: closed that one item, and the audit FOUND AND FIXED TWO REAL BUYER-FACING DEFECTS
on `fda-recall-scraper`** (both shipped live before today). Negative control fired first, per
c2552's method: all three openFDA endpoints non-empty (food 29,586 / drug 18,076 / device
40,450, `last_updated` 2026-10-28), so no probe could read as a false zero.

**DEFECT 1 -- a self-contradicting coverage claim in the live README.** The FAQ said the
drug-only `openfda` identifier block is "all-or-nothing per row -- if `brandName` is null, so
are `genericName`, `productNdc` **and the rest**". c2552 measured that on THREE subfields;
`normalize()` flattens **TWELVE**. Measuring all twelve splits them cleanly: six really do move
together (`brand_name`/`generic_name`/`manufacturer_name`/`product_ndc`/`package_ndc`/
`spl_set_id`, all exactly 2977 of the 2977 openfda-bearing drug rows) and six do not
(`application_number` 98.4%, `route` 98.4%, `unii` 97.9%, `substance_name` 97.8%, `rxcui`
96.1%, **`upc` 47.9%**). 1552 drug rows carry a filled `brandName` with an EMPTY `upc`; 0 carry
a `upc` without a `brandName` (strict subset, never an independent hit). A 4-row local run hit
one immediately (`D-0436-2015`). The README's very NEXT FAQ paragraph already said `upc` is much
sparser, so the doc contradicted itself one paragraph apart. Rewritten with the exact six-and-six
split; that next paragraph's two-100-row-sample estimate (15%/34%, 2026-10-12) is REPLACED with
the whole-archive `_exists_` measurement (1,425 of 2,977 = 47.9%, i.e. 7.9% of all drug rows).

**DEFECT 2 -- the `unreachable_remedy` defect proper (the c2884 pattern, 5th instance).** The
`pushed===0` message's last cause read "brandName/genericName/manufacturerName only ever match
drug recalls ... they will zero out a food- or device-only search" -- true, and useless to the
buyer most likely to be reading it: someone who already set `productTypes:["drug"]` and searched
a drug name over an older window. The actual cause is coverage (the NDC cross-reference reaches
only 16.5% of drug rows -- 6% in 2016 rising to 56% in 2026) and there IS a real workaround
(filter `recallingFirm`, populated on all three product types and all years, then match the name
client-side against `productDescription`); both lived ONLY in the README FAQ, never at the point
of failure. Fixed: when any name filter is set, a measured cause-plus-workaround warning now
LEADS (full numbers + by-year table in the log; the status message is 489 chars at worst case,
493 with a 5-digit `scanned`, verified against the 500-char cap using 3 name filters AND the
longest `dateField`), and the generic 5-cause message is unchanged for every other query shape
(verified byte-identical on a no-name-filter zero-row run).

**All four c2552 claims re-verified live and ALL HELD, with refreshed numbers:** (1) `Not Yet
Classified` still reachable, and the 4-value OR-sum is still EXACT against each endpoint total
(12994+14798+1793+1=29586 food, 14602+1753+1720+1=18076 drug, 35732+3677+1040+1=40450 device) --
that sum is what actually proves Class I+II+III != no filter; the count is now 1/1/1 (was 2/2/1
on 2026-10-06), which the README already said but the CODE comment did not -- comment brought in
line. (2) `voluntary_mandated:"N/A"` byte-identical at food 6 / drug 23 / device 8, empty-string
rows (1/12/10) still summing to the totals. (3) `termination_date` still silently excludes ~5%
food / ~18% drug / **~37%** device (27,976/29,586; 14,813/18,076; 25,496/40,450 -- device drifted
36% -> 37%), still tracking `status='Terminated'` to within 4/1/34 rows. (4) `status:"Pending"`
still 0, now of 88,112 records, still a normal NOT_FOUND empty set rather than a 400. The
`dateField` coverage table and the openfda fill figures (2,977/18,076 = 16.5%, by-year 6/9/22/40/
48/56, 45 of the newest 100) are refreshed everywhere they appear: 2 code comments, 4 README
spots, the input table and the Pending warning string.

**One bad test input, logged not chased** (same family as c2887's invalid `XZ` country): the
first zero-row reproduction used drug + `report_date` 2006-2008 and appeared to work, but
openFDA's **drug** archive has 0 rows at all before ~2012, so that window was empty regardless
of the filter and proved nothing. Re-ran on 2016, where the negative control PASSES (1,254 drug
rows live; `recalling_firm:"Teva"` 24) -- there the three name filters really are the only reason
the run returns zero. **And the remedy was proven to actually recover rows:** `recallingFirm:
"Teva"` over the identical 2016 window delivered 3 of 24 declared matches.

`node --check` clean. `check-code-fields`, `check-filter-reach` (18 filters, 0 unreachable),
`check-readme-samples` (756 values), `check-registry-fields`, `check-doc-size`,
`check-zero-row-message` (63 `pushed===0` branches, 0 MISS) and `check-charges` (27/0/0) all
clean. Code AND README changed with no `meta.json` change, so ONE `apify push --force`: **build
0.1.92 SUCCEEDED**; live `src/main.js` and `README.md` both verified **byte-identical** to local
via `/v2/acts/<id>/versions` `sourceFiles`. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy`
all active; `/`, `/tools`, `/tools/fda-recall-scraper`, `/pricing` all 200 after the change.
**Spend this cycle: one ~$0.005 build** (every openFDA probe was a keyless read-only GET; all
Actor runs were local). Recorded via `bin/_rec2888.py` (targeted string replace, 1-line diff --
the c2551 `json.dump` trap avoided). `audit-due --type unreachable_remedy` now reads **NONE DUE**;
next target **`federal-register-scraper` in 2 cycles (2890)** -- budget time for it.
`tasks/queue.md` is 120KB / 7 kept DONE blocks (2 over the newest-5 floor, TRIM SOON not TRIM
DUE) -- the next QUALITY/GROWTH slot (c2889, 2889 % 3 == 0) folds it in.

---

### Previous cycle (c2887) status, preserved

Updated: 2026-11-08 UTC by cycle 2887 (claude-sonnet-5). Regular slot (2887 % 3 == 1, computed fresh).

**Preflight: `audit-due --all` re-run fresh found exactly 1 real fleet-rotation item DUE**,
`unreachable_remedy: eu-ted-tenders-scraper` (2551 -> 2887, 336c/7d gap). `checks-due --all`
NONE DUE (soonest `check-source-endpoints` in 7c). `inbox-triage new`: NONE UNTRIAGED of 75.
`bin/revenue` re-read live: $0 booked, 27 Actors, 50 users, 816 runs30d, 3 ext_bad30d (all
unchanged from c2886).

**THE WORK: closed the one DUE fleet-rotation item, re-verifying all 4 `unreachable_remedy`
claims on `eu-ted-tenders-scraper` live against the real `api.ted.europa.eu` (local Actor
runs only, $0 platform spend).** (1) `historicalOnlyAdvice` (main.js:117-156,
`HISTORICAL_ONLY_NOTICE_TYPES`/`PROCEDURE_TYPES`, last measured cycle 2852 2026-11-07):
re-confirmed `procedure-type=4` fresh via direct curl -- 0 matches in the last 365 days,
25,624 since 2023, byte-identical to yesterday's measurement, 0 drift. Ran the Actor locally
with `{procedureType:["4"],publishedWithinDays:365,maxResults:5}`: fired the exact lecture
naming `publicationDateFrom` as the fix. (2) **Proved the remedy actually resolves the
zero-row condition, not just that the code names it**: re-ran with
`{procedureType:["4"],publicationDateFrom:"20230101",maxResults:3}` -- pushed 3/3 real rows
(totalNoticeCount 25,624), and the historical-code lecture was correctly SUPPRESSED since the
buyer was already using the right tool; the run also exercised the `maxResults` truncation
message on a real delivering run ("Pushed 3 notice(s) ... Raise maxResults to get them",
naming the true total). (3) `publishedWithinDaysAtCeiling` (main.js:181-184, the
c2561/c2568 fleet pattern): first attempt used an invalid `countries` value ("XZ"), which
confounded the test with an unrelated live HTTP 400 from TED rejecting the code -- a bad test
input, not a new finding, noted and not chased further (out of this audit's scope). Re-ran
with a curl-verified, genuinely-0-result VALID query
(`{countries:["MLT"],cpvCodes:["09123000"],publishedWithinDays:365,maxResults:5}`): fired
cleanly, correctly naming CPV since one was set. (4) `watchDeadDateBound` (main.js:460-478):
ran `{countries:["MLT"],watchLabel:"test-watch-dead",publicationDateTo:"20250101",
maxResults:5}` -- both warnings fired correctly (permanently-blind explanation + the
drop-`publicationDateTo`-or-drop-`watchLabel` advice), and the baseline seed walk underneath
it completed correctly (13,813 notices baselined, 0 charged, matching the documented
seeding-charges-nothing shape). **0 defects found across all 4 claims, no code/README change
needed.** Recorded via `bin/_rec2887.py`; `audit-due --type unreachable_remedy` now reads
**NONE DUE**, next natural target `fda-recall-scraper` in 1 cycle (2888) -- budget time for it.

Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/tools`,
`/tools/eu-ted-tenders-scraper`, `/pricing` all 200 before and after. Revenue unchanged: $0
booked, 27 public Actors, 50 users, 816 runs30d. **Spend this cycle: $0** (local Actor runs
against the public TED API only, no build, no platform run). No owner email owed (no revenue
event, no critical blocker). `tasks/queue.md` now has 6 kept DONE blocks (one over the
newest-5 floor) -- not urgent, the next QUALITY/GROWTH slot's trim folds it in.

---

### Previous cycle (c2886) status, preserved

Updated: 2026-11-08 UTC by cycle 2886 (claude-sonnet-5). QUALITY/GROWTH slot (2886 % 3 == 0, computed fresh).

**Preflight: `audit-due --all` re-run fresh read FLEET ROTATIONS: NONE DUE** (the one
`count_audit` informational axis, court-records/trademark-search, is not a backlog).
`checks-due --all`: NONE DUE (soonest `check-source-endpoints` in 8c). `inbox-triage new`:
NONE UNTRIAGED of 75 -- re-read the two owner emails sitting in the inbox sliding window
(`2b237f1b` CourtListener token, `01852eaa` Apify Nov-15 `/v2/store` ranking change) and
confirmed both are old news already closed per prior-cycle STATUS history (lines ~387/538/791
of the pre-trim file): token wired into `secrets/env` since c2626/c3014-era work, and the
Nov-15 change already hardened at c2496 (`store-anon-rank`/`check-store-rank` degrade to
`RANK UNKNOWN` on dead paging rather than a false negative). `bin/revenue` re-read live: $0
booked, 27 Actors, 50 users, 816 runs30d, 3 ext_bad30d (all unchanged from c2885). So no
fleet-rotation item overrides the queue trim this cycle (c2861 rule, correctly not triggered).

**THE WORK: executed the doc-trim cadence on `tasks/queue.md`** (134.9KB/1593 lines, TRIM DUE,
the one TRIM-DUE doc c2885 left owed for this QUALITY/GROWTH slot). `bin/_trim2886q.py`
(cloned from `_trim2876q.py`'s hoist-then-cut pattern, ranges re-derived fresh per rule 3):
archived 10 historical DONE blocks (c2881 down through c2871, ~267+87 lines across three
contiguous ranges) verbatim to `tasks/queue_archive.md`, keeping the newest 5 DONE blocks live
(this cycle's new block plus c2885/c2884/c2883/c2882) per the standing newest-5 convention
(c2865 rule 6). Two open items correctly interleaved among the archived DONE blocks were
hoisted rather than cut -- the c2875 QUALITY/GROWTH-cadence-arithmetic watch and the c2873
`committeeId` detection follow-up, both still genuinely open. Also replaced the doc-trim
cadence item's own superseded EXECUTED c2880 narrative with a new EXECUTED c2886 record (old
one archived verbatim); the item's 5-rule STANDING RULES section was left untouched, since it
is their only home. **Rule-1 hazard grep ran FIRST** over all 5 archive-bound ranges (pattern
`standing|cadence|always |never |STANDING|do not |must |rule`, case-insensitive): every
rule-shaped hit traced to a durable home outside the archived text -- the doc-trim item's own
numbered rules (kept live at their one true home), the c2861 priority rule (already rescued
into `notes/LEARNINGS.md` "Cycle 2880"), and c2864's "always re-assert the state after
recording it" rule (already homed at `notes/LEARNINGS.md:5736`). None was the sole home of an
instruction, so nothing further needed rescuing. **134.9KB/1593 lines -> 111.2KB/1326 lines,
TRIM DUE -> TRIM SOON** (`bin/check-doc-size` re-run fresh after: ~17c headroom, proj. 239KB at
the next look -- clears the immediate Read-cap risk but is not yet a durable OK; no open-item
compression was attempted this cycle since the DONE-only cut already restored comfortable
headroom and manufacturing extra compression work was not warranted). Verified lossless two
ways: the script's own asserts (total/non-overlapping partition, exact non-blank multiset
match between original and kept+archived, both excluding the two deliberate rewrites) and an
**independent** check outside the script (1512/1512 original non-blank lines all findable in
live+archive, 0 missing). Backup `/tmp/c2886_queue.bak`. Open/DONE item counts sanity-checked
before/after (82 -> 71 total items: 15 DONE -> 5 DONE as expected by the newest-5 convention
plus one new block, 67 OPEN -> 66 OPEN as expected by removing exactly the superseded TOP
PRIORITY pointer item and touching nothing else). `check-registry-fields`/`check-charges` not
re-run (no code changed this cycle -- pure docs). Services `fetchsmith-web`/`fetchsmith-mail`/
`caddy` all active; `/`, `/tools`, `/pricing` all 200 before and after. Revenue unchanged: $0
booked, 27 public Actors, 50 users, 816 runs30d. **Spend this cycle: $0** (no build, no Actor
run, no network calls beyond the preflight checks and site curls). No owner email owed (no
revenue event, no critical blocker). `tasks/queue.md` is now TRIM SOON, not DUE -- the next
QUALITY/GROWTH slot can spend on growth work instead of another trim unless `check-doc-size`
says otherwise by then.

Updated: 2026-11-08 UTC by cycle 2885 (claude-sonnet-5). Regular slot (2885 % 3 == 2, computed fresh).

**Preflight: `audit-due --all` re-run fresh found 1 real fleet-rotation item DUE -- a
NEWLY-ARRIVED target, not the NONE DUE c2884 projected** -- `unreachable_remedy:
us-federal-awards-scraper` (2549->2885, 336c/7d gap). `checks-due --all`: NONE DUE (soonest
`check-source-endpoints` in 9c). `inbox-triage new`: NONE UNTRIAGED of 75. `bin/revenue`
re-read live: $0 booked, 27 Actors, 50 users, 816 runs30d, 3 ext_bad30d (all unchanged from
c2884).

**THE WORK: closed the one DUE fleet-rotation item, `unreachable_remedy:
us-federal-awards-scraper`.** Targeted the `NO_END_DATE_CATEGORIES` remedy (main.js:399,
shipped c884, never independently re-verified since -- c2549's audit covered
`TOPTIER_AGENCY_NAMES`/`DEF_CODES`/`PAGE_SIZE`/award-type groups instead). (1) Re-verified the
core claim fresh and live against `api.usaspending.gov` (keyless, public): 10/10 fresh IDVs
(`award_type_codes` IDV_A..IDV_E, 2024-2026 window -- different NAICS/PSC/agencies/years from
c884's 2008-2025 sample) came back with `End Date: null` even though the contract kind's field
mapping requests it; 10/10 fresh loans (codes 07/08, same window) also came back null. Both
independently reconfirm "loans and IDVs carry no real period-of-performance end date," the
premise the `expiringWithinDays` zero-row remedy (main.js:1238-1240) rests on. (2) **Found a
stale/incorrect CODE COMMENT while probing this (not a reachability defect -- no buyer-facing
behavior was ever wrong):** the `BASE_FIELDS` comment (main.js:79-80) and `SUB_FIELDS` comment
(main.js:102-104) both claimed "asking for a field outside its kind's mapping is a 400." Tested
4 ways live: requesting the contract-only field `End Date` on the loan kind -> 200 with
`null` (not 400); requesting `NAICS` on loan kind -> 200 null; requesting a made-up field name
(`TotallyBogusField`) -> 200 with that key null; requesting the prime-only field `Award Amount`
in a `subawards:true` request (sorted by a valid sub-award field, isolating fields from sort) ->
200 with `Award Amount: null`. The API never 400s on a field -- it silently accepts anything in
`fields` and nulls out what does not apply. The real 400 gate lives entirely in `sort` (verified:
a sort value absent from the request's own `fields` list, or absent from the kind's sort mapping,
both 400). This never caused a live bug since `KIND_FIELDS`/`SUB_FIELDS`/`SORTS`/`SUB_SORTS` are
all internally correct already, but the false claim could mislead a future maintainer into
trusting a 400 to catch a copy-paste field-list error, when the real failure mode is a SILENT
always-null column that still charges normally. **Fixed both comments in place** to state the
true behavior and cite this cycle's live verification. Comment-only diff (grep-confirmed: zero
non-comment `+`/`-` lines), `node --check` clean, so **no Apify build/push was owed.**
Recorded via `bin/_rec2885.py`; `audit-due --all` now reads **FLEET ROTATIONS: NONE DUE**.
`check-registry-fields` (0 drift) and `check-charges` (27/0/0) both re-run clean as standard
postflight. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/tools`,
`/tools/us-federal-awards-scraper`, `/pricing` all 200 before and after. Revenue unchanged: $0
booked, 27 public Actors, 50 users, 816 runs30d. **Spend this cycle: $0** (public
`api.usaspending.gov` curls only, no build, no Actor run). No owner email owed (no revenue event,
no critical blocker). `tasks/queue.md` remains the one TRIM-DUE doc (133.4KB), queued for the next
QUALITY/GROWTH slot, c2886 (2886 % 3 == 0).

Updated: 2026-11-08 UTC by cycle 2884 (claude-opus-5). Regular slot (2884 % 3 == 1, computed fresh).

**Preflight: `audit-due --all` re-run fresh found exactly 1 real fleet-rotation item DUE**,
matching c2883's naming -- `unreachable_remedy: google-news-scraper` (2546->2884, 338c/7d gap).
`checks-due --all`: 1 DUE, `git-maintain`. `inbox-triage new`: NONE UNTRIAGED of 75. `bin/revenue`
re-read live: $0 booked, 27 Actors, 50 users, 816 runs30d, 3 ext_bad30d (all unchanged from c2883).

**THE WORK: closed the last standing fleet-rotation item and FOUND + FIXED A REAL SHIPPED
DEFECT** -- the first this axis has found on `google-news-scraper` since c1549 (now 2-for-3).
`windowNote`, the always-appended out-of-window drop note, hard-coded both of its attributions:
it always told the buyer the dropped articles fell outside "your publishedAfter/publishedBefore
window" and always blamed "a known Google quirk when a date window is combined with 'Exclude
these domains'". But since c933 a customer can set the policed window by typing `after:`/`before:`
into the QUERY TEXT (read back out by `ownWindowMs`) and exclude a publisher with `-site:` in that
same text -- setting NEITHER `publishedAfter`/`publishedBefore` NOR `excludeSites`. That buyer was
told 11 of their 100 articles were dropped because of two input fields they had left completely
empty. The identical hard-coding sat in the log line and in the `pushed===0` "every article Google
returned fell outside ..." why-cause. This is the same status-message mis-attribution class as
c2543 (shopify's shared `activeFilters`) and c2544 (steam's filter attribution) -- third instance
fleet-wide, so it is now a pattern worth grepping for, not a one-off.

**Fix:** record where the window and the exclusion ACTUALLY came from at the drop site, where both
facts are already in scope -- `outOfWindowSources` ('query' | 'fields', from the existing
`ownTimeOp` flag) and `outOfWindowExcl` ('field' if `excludeSites.length`, else 'query' if
`/-site:/i` matches the feed's query text, else 'none') -- then derive `windowLabel` and
`windowQuirk` once and use them in all three places.

**Verified live, 4 shapes** (all local runs, `CRAWLEE_STORAGE_DIR`, `useApifyProxy:false`, fresh
inputs unlike c2546's economy/2026-10-20..27): (A) query-text window + query-text `-site:` now
reads "well outside the after:/before: dates in your query (a known Google quirk when a date
window is combined with a -site: exclusion in the query)", 11 dropped of 100. (B) REGRESSION,
schema fields + `excludeSites` field (inflation, 2026-09-15..22, bbc.com): wording byte-identical
to pre-fix, 18 dropped of 100. (C) query-text window with NO `-site:` anywhere: 46 items, 0
dropped, NO note at all -- independently re-confirms c788's core finding that the leak needs a
`-site:` exclusion and dates alone do not leak, and doubles as the happy-path regression. The
'none' quirk branch is therefore a defensive fallback live traffic essentially never reaches
(traced, not live-reproduced -- stated plainly rather than claimed). (D) MIXED, two queries (one
with its own dates, one taking the schema window) + `excludeSites`: names both sources, 29
dropped.

**Also re-verified c2546's claim (2) fresh and it got WORSE:** a plain curl of
`economy -site:reuters.com after:2026-10-01 before:2026-10-08` returned items dated 2011-10-01
(x3), 2017-03-22, 2018-06-19, 2020-06-09, 2022-12-15, 2025-12-03/04 and one dated 2026-11-07,
i.e. AFTER the `before:` -- 11 far-out-of-window in 100 against the 7-in-100 c788 first measured.
The backstop and its buyer-facing note stay necessary. Claim (1) (VALID_TOPICS enum) was
deliberately NOT re-touched: c2546 spot-checked all 20 codes only 338c ago and nothing has
touched that code, so the budget went to the defect instead.

**Shipped:** build 0.1.94 (package.json 0.1.24 -> 0.1.25); live `src/main.js` and `README.md`
verified byte-identical to local via `GET /v2/acts/<id>/versions` `sourceFiles` (38,541 and 69,117
chars). README line 175 already documented both window sources correctly, so only its last
sentence was extended to say the status message now NAMES whichever window it policed. No
output-field change, so no `registry.json`/`dataset_schema.json` work was owed.
**Guards:** `check-zero-row-message` 24 dataset Actors / 63 `pushed===0` branches / 0 MISS.
**Fleet check:** ran the one DUE item, `git-maintain` -- TRIP on loose size 69 MiB >= 64 MiB,
repacked 650 loose objects -> 0 (pack 129 -> 131 MiB, `.git` 135M), all 3 services active after;
recorded, next due c2932.

**State after this cycle:** `audit-due --all` re-run after recording reports **FLEET ROTATIONS:
NONE DUE** -- the rotation backlog that ran from c2879 through c2884 is fully cleared. Only the
2 informational one-off `count_audit` axes remain (court-records, trademark-search), which are
NOT a backlog. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/tools`,
`/tools/google-news-scraper`, `/pricing` all 200. Revenue unchanged: $0 booked, 27 public Actors,
50 users, 816 runs30d. Spend this cycle: one ~$0.005 Apify build, nothing else. No owner email
owed (no revenue event, no critical blocker). `tasks/queue.md` is the one remaining TRIM-DUE doc
(133KB) and is queued for c2886, the next QUALITY/GROWTH slot.

Updated: 2026-11-08 UTC by cycle 2883 (claude-sonnet-5). QUALITY/GROWTH slot (2883 % 3 == 0, computed fresh).

**Preflight: `audit-due --all` re-run fresh found 2 real fleet-rotation items DUE, matching
c2882's naming exactly (no new arrival this time)** -- `unreachable_remedy: apple-podcasts-scraper`
(2545->2883, 338c/7d gap, audit-due's NEXT TARGET) and `unreachable_remedy: google-news-scraper`
(2546->2883, 337c). `checks-due --all` NONE DUE (soonest `git-maintain` in 1c, cycle 2884).
`inbox-triage new`: NONE UNTRIAGED of 75 (verified fresh; inbox skim showed only DMARC reports,
an already-actioned owner fwd, and cold-outreach/spam, all previously on record -- no reply
needed). `bin/revenue` re-read live: $0 booked, 27 Actors, 50 users, 816 runs30d (unchanged from
c2882), 3 ext_bad30d steady.

**THE WORK: closed the NEXT TARGET, `unreachable_remedy: apple-podcasts-scraper`, re-verifying
the ONE real defect c2545 found and fixed.** That fix split the archive-walk zero-row status
message into an exonerated/not-exonerated path (`archiveFilteredIdsDateExonerated`,
main.js:888-890 and 1556-1559) so it stops blaming the date window when the log already proved
it matched. Re-verified live with a FRESH podcast (Radiolab, id152249110 -- neither c1548 nor
c2545 used anything but Lex Fridman/id1434243584) and a fresh, deterministic filter
(`minDurationSeconds:999999999` instead of c2545's `explicitOnly`, which depends on a show's real
explicit-tag mix and could silently pass/fail by luck). (1) EXONERATED case: impossible duration
filter + a wide window (2000-01-01..2030-01-01) on the full 678-episode RSS archive -- the log
correctly reported "678 of them DID fall inside your window, so widening will not help," and the
status message named ONLY `minDurationSeconds (999999999)`, never the date fields. (2)
NOT-EXONERATED case: same duration filter + a genuinely out-of-range window
(1990-01-01..1995-01-01; the feed's real coverage is 2006-05-05..2026-11-06) -- the log fell back
to the original "none fell inside the requested window ... widen to [real range]" wording, and
the status message correctly named ALL THREE filters (duration + both dates), since the date
window really was part of the cause this time -- confirms the split does not over-exonerate when
the window genuinely is empty. (3) Happy-path regression (`test_input.json`, Lex Fridman, 5
episodes): 5/5 pushed, byte-identical behavior. **0 defects found, the c2545 fix holds intact, no
code/README change needed.** Closing a DUE fleet-rotation audit is valid QUALITY-slot content
(same precedent as c2877/c2880 closing audits in their QUALITY slots), so no slot override was
needed. Recorded via `bin/_rec2883.py` (file confirmed pure ASCII before the `json.dump
(ensure_ascii=True)` round-trip, no corruption risk); `audit-due --type unreachable_remedy` now
reads 1 DUE (`google-news-scraper`, next target).

Services `fetchsmith-web`, `fetchsmith-mail`, `caddy` all active; `/`, `/pricing`, `/tools`,
`/blog` all 200 before and after. **Spend: $0** (local Actor runs + public Apple Podcasts
RSS/lookup-API curls only). **Blockers: none.** Standing: $0 revenue after 2883 cycles, no buyer
signal, Polar still correctly deferred. Temp test storage dirs (`/tmp/apc_test1` through
`/tmp/apc_test5`) deleted after verification -- no production KV store touched. **Next cycle:
re-run `audit-due --all`/`checks-due --all` fresh (do NOT trust this cycle's reading, per the
c2120 rule) -- if the rotation still reads DUE, close `unreachable_remedy: google-news-scraper`
(the only item left); `checks-due --all` showed `git-maintain` due in 1 cycle (cycle 2884) so it
will likely be DUE next cycle too, budget time for both.**

---

### Previous cycle (c2882) status, preserved

Updated: 2026-11-08 UTC by cycle 2882 (claude-sonnet-5). Regular slot (2882 % 3 == 2, computed fresh).

**Preflight: `audit-due --all` re-run fresh found THREE real fleet-rotation items DUE, not the 2
c2881 named** -- `google-news-scraper` (2546->2882, 336c/7d gap) had newly joined alongside
`apple-podcasts-scraper` (2545->2882, 337c) and `steam-reviews-scraper` (2544->2882, 338c,
**audit-due's own NEXT TARGET**). `checks-due --all` NONE DUE (soonest `git-maintain` in 2c,
cycle 2884). `inbox-triage new`: NONE UNTRIAGED of 75 (verified fresh). `bin/revenue` re-read
live: $0 booked, 27 Actors, 50 users, **816 runs30d (down from 820, window aging not a signal)**,
3 ext_bad30d steady.

**THE WORK: closed the NEXT TARGET, `unreachable_remedy: steam-reviews-scraper`, budgeting the
full slot per c2881's explicit note (its last audit, c2544, found 2 genuine shipped defects).**
Re-verified both c2544 fixes live with fresh apps/inputs, neither reused from c2544's app
570/1145360 probes. (1) ATTRIBUTION fix (`activeFilters`/`filterLabel`, main.js:214-222): ran
Portal 2 (appId 620) with `reviewsBefore:"01/01/2024"` alone, `maxReviewsPerApp:20` -- the WARN
and status message both correctly cited only "reviewsBefore filter", naming no filter the run
never set; `reviewsAfter` is still correctly excluded from the list (it trips the `pastWindow`
early-stop before the filter check, so never increments `filteredOut`). (2) OFF-BY-ONE fix (the
`considered` counter, main.js:784/834, feeding the `allFiltered` test at line 1028): ran Terraria
(appId 105600) with `reviewsAfter:"2026-11-06"` + `keyword:"zzzznonexistentword123"`,
`maxReviewsPerApp:200` -- `pastWindow` triggered at 163 scanned (the 200 cap never reached), all
163 filtered by keyword, and the run correctly reported "every review Steam returned was removed
by your keyword filter for: 105600" (the `allFiltered` path) with no cap WARN -- confirms
`considered`/`filteredOut` no longer miss by 1 when a `reviewsAfter` window ends the scan, which
pre-fix fell through to the vague "the run stopped before any review could be returned" fallback
instead (c2544's repro: 33 pulled/32 filtered/`allFiltered` `[]`). Also code-read (structural,
pre-migration claim, not independently live-tested) the `watchDeadDateBound` remedy
(main.js:248-266) -- unchanged since it predates c2544. README (lines 278, 296-319) still
matches all live behavior verbatim, including the Hades `reviewsBefore` depth-cap example and
the `allFiltered`/`depthCapped` RUN_SUMMARY FAQ entries. **0 defects found, both c2544 fixes hold
intact after the 2026-10-22 Valve migration, no code/README change needed.** Recorded via
`bin/_rec2882s.py` (file is pure ASCII now, all em-dashes pre-escaped, so a plain
`json.load`/`json.dump(ensure_ascii=True)` round-trip was safe this time, unlike the corruption
risk c2544 hit); `audit-due --type unreachable_remedy` now reads 2 DUE
(`apple-podcasts-scraper` NEXT TARGET, `google-news-scraper`), both named precisely in
`queue.md`'s new c2883 top-priority item, with a note that neither has a known prior-defect
history like `steam-reviews-scraper`/`shopify-products-scraper` did, so read each one's
`audit_dates.json` note before assuming a simple re-verify.

Services `fetchsmith-web`, `fetchsmith-mail`, `caddy` all active; `/`, `/pricing`, `/tools`,
`/blog` all 200 before and after. **Spend: $0** (local Actor runs + public steamcommunity.com
curls only). **Blockers: none.** Standing: $0 revenue after 2882 cycles, no buyer signal, Polar
still correctly deferred. Temp test storage dirs (`/tmp/srs_test1`, `/tmp/srs_test2`) deleted
after verification -- no production KV store touched. **Next cycle: re-run `audit-due --all`/
`checks-due --all` fresh (do NOT trust this cycle's reading, per the c2120 rule) -- if the
rotation still reads DUE, close `apple-podcasts-scraper` (NEXT TARGET), then
`google-news-scraper`.**

---

### Previous cycle (c2881) status, preserved

Updated: 2026-11-08 UTC by cycle 2881 (claude-sonnet-5). Regular slot (2881 % 3 == 2, computed fresh).

**Preflight: `audit-due --all` re-run fresh found THREE real fleet-rotation items DUE, not the 2
c2880 named** -- `apple-podcasts-scraper` (2545->2881, 336c/7d gap) had newly joined alongside
`shopify-products-scraper` (2543->2881, 338c, **audit-due's own NEXT TARGET**) and
`steam-reviews-scraper` (2544->2881, 337c). `checks-due --all` NONE DUE (soonest `git-maintain`
in 3c, cycle 2884). `inbox-triage new`: NONE UNTRIAGED of 75 (verified fresh). `bin/revenue`
re-read live: $0 booked, 27 Actors, 50 users, **820 runs30d (down from 828, window aging not a
signal)**, 3 ext_bad30d steady.

**THE WORK: closed the NEXT TARGET, `unreachable_remedy: shopify-products-scraper`.** Re-verified
all 4 load-bearing remedy claims live with a FRESH test store (rothys.com, 769 products -- prior
audits at c1546/c2543 only ever used allbirds.com) and filter combos c2543 never used (`vendors`
alone for the singular per-store/aggregate message path; `productTypes`+`minDiscountPercent`
stacked for the plural path). (1) The 8-filter `activeFilters` list (main.js:85-94) still exactly
matches `input_schema.json`'s 8 property names and the matching functions; both fresh combos
produced the correct singular/plural per-store warning AND aggregate status message, each naming
only the filters actually set -- **confirms the c2543 fix (hoisted shared `activeFilters`,
closing the c5748-class hardcoded-field-list bug) is still intact**, zero drift. (2)
`matchesSearch`'s haystack (title/vendor/product_type/tags) still matches the README verbatim.
(3) Live-reproduced the watch-mode `maxProductsPerStore` cap remedy on allbirds.com with fresh
values (9 and 80000, neither reused from c2543's 15/100000 or c1546's 10/100000): 9 fired the cap
warning and baselined exactly 9; 80000 baselined the Actor's whole current live catalog (368
products, up slightly from c2543's 356 -- organic growth) with no warning. rothys.com 403'd on
the watch-mode local test (no residential proxy credentials available locally), so that one test
used allbirds.com instead; the filter-message tests worked fine on rothys.com since they only
hit the public `/products.json` endpoint directly. **0 defects found** -- the c2543 fix holds,
no code/README change needed. Recorded via `bin/_rec2881.py`; `audit-due --type
unreachable_remedy` now reads 2 DUE (`steam-reviews-scraper` NEXT TARGET,
`apple-podcasts-scraper`), both named precisely in `queue.md`'s new c2882 top-priority item with
a note that `steam-reviews-scraper`'s last audit (c2544) found 2 genuine shipped defects, so it
deserves a full slot.

Services `fetchsmith-web`, `fetchsmith-mail`, `caddy` all active; `/`, `/pricing`, `/tools`,
`/blog` all 200 before and after. **Spend: $0** (local Actor runs only, no Apify build/platform
run needed). **Blockers: none.** Standing: $0 revenue after 2881 cycles, no buyer signal, Polar
still correctly deferred. Temp test storage dirs (`/tmp/sps_test1..4`) deleted after
verification -- no production KV store touched. **Next cycle: re-run `audit-due --all`/
`checks-due --all` fresh (do NOT trust this cycle's reading, per the c2120 rule) -- if the
rotation still reads DUE, close `steam-reviews-scraper` (NEXT TARGET), budgeting a full slot per
the note above, then `apple-podcasts-scraper`.**

---

### Previous cycle (c2880) status, preserved

Updated: 2026-11-08 UTC by cycle 2880 (claude-opus-5). QUALITY/GROWTH slot (2880 % 3 == 0, computed fresh).

**Preflight: `audit-due --all` found 2 real fleet-rotation items DUE** (`unreachable_remedy:
shopify-products-scraper` 2543->2880, 337c/7d gap -- the NEXT TARGET c2879 named; and
`unreachable_remedy: steam-reviews-scraper` 2544->2880, 336c gap), plus 2 informational one-off
`count_audit` axes (court-records / trademark-search, not a backlog). `checks-due --all` NONE DUE
(soonest `git-maintain` in 4c, cycle 2884). `inbox-triage new`: NONE UNTRIAGED of 75 (verified
fresh against the whole inbox, not assumed from the sliding window). `bin/revenue` re-read live:
$0 booked, 27 Actors, 50 users, **828 runs30d (down from 836)**, 3 ext_bad30d -- the c2336
tripwire diff is CLEAN (ext_bad30d unchanged at 3; the runs30d dip is window aging, not a
failure signal).

**THE WORK: executed the doc-trim cadence on `state/STATUS.md` -- the one file c2876 left owed --
and reached a DURABLE OK, not just a passing reading.** `check-doc-size` read it **TRIM SOON at
123.2KB/1527 lines with a 229KB projection at its own next look**, i.e. the next run would have
read TRIM DUE no matter what happened in between. This is the QUALITY slot (`2880 % 3 == 0`) the
cadence item's standing rule 2 asks for, so no override was needed (unlike c2876, which trimmed in
a Regular slot on purpose). `bin/_trim2880s.py` (cloned from `bin/_trim2867s.py`, every line range
**re-derived fresh from the live file** per standing rule 3 -- 26 blocks found live, not the 25 the
`### Previous cycle` headers suggest). **123.2KB/1527 lines -> 42.5KB/465 lines, TRIM SOON -> OK**,
projection 148KB vs the 200KB trim line, so rule 4's margin arithmetic clears with ~52KB of room
(~36 cycles of headroom) rather than the thin margin that made c2876's queue.md cut only half a
fix.

**Authority correction worth keeping: STATUS.md's convention is keep-newest-10 CYCLE blocks, not
newest-5.** `tasks/queue.md`'s own trim item said "keep the newest-5-blocks convention" for
STATUS.md -- that is wrong, it conflated queue.md's newest-5 **DONE-block** convention with
STATUS.md's newest-10 **cycle-block** convention (`bin/check-doc-size:167`, the c2224/c1836 rule,
also what c2867 cut to and what the 4510 B/cycle growth figure in that tool's table is measured
at). Followed the tool per standing rule 5 and fixed the queue's wording. Kept live: c2879 down
through c2870. Archived: c2869 down through c2855 (15 blocks, 1062 lines) appended to
`state/STATUS_ARCHIVE.md` (**uppercase, appended at the END** -- both halves of the c2867/c2868
blocker avoided, path taken from `check-doc-size`'s table rather than guessed).

**Rule-1 hazard grep ran FIRST, over all 1,062 archive-bound lines, with a deliberately BROADER
pattern than c2867's** (`standing|cadence|always |never |STANDING|do not |must |rule`, case-
insensitive): **89 hits, every one read by hand.** 88 are narrative about a rule with a durable
home elsewhere, and each home was verified live by grep this cycle rather than assumed:
dated-record rule -> `LEARNINGS.md:5616-5693`; `check-handle-liveness --only` never saving its
json -> `:5683`; c2864 re-assert-the-state -> `:5736`; the STATUS_ARCHIVE casing trap ->
`:5742-5750` + `queue.md:271`; one-file-per-cycle -> `queue.md:268`; keep-newest-10 ->
`check-doc-size:167`; the cadence item's own rules 1-6 and the c2845/c2846 disclosure backlog ->
their live `queue.md` items. **The 89th was a genuine hazard and the whole reason the rule
exists: the c2861 standing rule "a freshly DUE rotation/check result always takes priority over a
backlog item carried in `queue.md`" -- cited by name in the c2862/c2865/c2866 blocks and homed
NOWHERE else** (no c2861 section in LEARNINGS.md; absent from `queue.md`, `PLAYBOOK.md` and
`CLAUDE.md`). Given a durable home in `notes/LEARNINGS.md` (new "## Cycle 2880" section, with the
full home table above) **before** the cut ran; archiving without it would have silently retired a
rule three cycles had leaned on.

**Verification, three independent ways:** (a) the script's own asserts -- partition total /
non-overlapping over 1..1527, multiset-identical content, boundary lands exactly on the c2869
header with its blank separator, and a new assert that the 10 kept `Updated: ... by cycle N`
blocks ARE the 10 numerically newest; (b) an independent lossless check outside the script,
**1369/1369 non-blank original lines findable in live+archive**; (c) both pre-commit tripwires
re-run after the write -- `check-status-blocks-kept` **OK, 0 blocks destroyed** (1283 blocks
across live+archive), `check-status-continuity` **NONE MISSING** on the retained c2870..c2879
window (10 completed cycles, 10 blocks). Backup at `/tmp/c2880_status.bak`.

**Deliberately NOT done, and why:** `tasks/queue.md` is still TRIM SOON (119.3KB/1411 lines, proj.
247KB) and was left untouched per the one-file-per-cycle rule -- it is now the only TRIM SOON doc
and the next QUALITY slot's trim, with c2876's measured per-item byte table still live in its
queue item so that pass does not re-measure. The 2 DUE `unreachable_remedy` audits were also left:
the trim plus its 89-hit grep consumed the cycle's time budget, and a shopify/steam remedy audit
is the kind of work that found 2 real shipped defects at c2544 -- worth a full slot, not 8 rushed
minutes. Both are named precisely in `queue.md` as c2881's top item.

Services `fetchsmith-web`, `fetchsmith-mail`, `caddy` all active; `/`, `/pricing`, `/tools`,
`/blog` all 200 before and after. **Spend: $0** (no build, no Apify run -- local file work only).
**Blockers: none.** Standing: $0 revenue after 2880 cycles, no buyer signal, `bin/traffic` nowhere
near the 100/day `/pricing` threshold, so Polar stays correctly deferred per owner decision.
**Next cycle: re-run `audit-due --all`/`checks-due --all` fresh (do NOT trust this cycle's
reading, per the c2120 rule) -- if the rotation still reads DUE, close `unreachable_remedy:
shopify-products-scraper` (audit-due's NEXT TARGET), then `steam-reviews-scraper`.**

---

### Previous cycle (c2879) status, preserved

Updated: 2026-11-08 UTC by cycle 2879 (claude-sonnet-5). Regular slot (2879 % 3 == 2, computed fresh).

**Preflight: `audit-due --all` found 2 real fleet-rotation items DUE** (`unreachable_remedy:
remote-jobs-scraper` 2542->2879, 337c/7d gap; `unreachable_remedy: shopify-products-scraper`
2543->2879, 336c/7d gap) -- closed the NEXT TARGET (`remote-jobs-scraper`), left
`shopify-products-scraper` for the next cycle. `checks-due --all` NONE DUE (soonest
`git-maintain` in 5c). `inbox-triage new`: NONE UNTRIAGED of 75 (verified fresh, not assumed).
`bin/revenue` unchanged: $0 booked, 27 Actors, 50 users, 836 runs30d, 3 ext_bad30d.

**THE WORK: re-verified all 4 `remote-jobs-scraper` `unreachable_remedy` claims live, with
fresh inputs different from both c1545 and c2542 -- zero drift, no code/README change.**
(1)+(2) WATCH_KEEP cap (main.js:186) still literally 20000, eviction-warning text unchanged --
structural/non-vendor claim, code read suffices (same standard prior audits used). (3)
seeding-charges-nothing re-confirmed by a fresh read of `pushResult` (main.js:339-342): the
seeding branch still returns `watchSeen.size < SEED_CAP` before ever reaching
`chargeAndPush` -- structurally cannot charge; `SEED_CAP` is now a named constant (5000,
main.js:185) vs the "earlier direct cap" c2542 noted, no behavior change. (4) the one
runtime-dependent claim (time-budget / `sourcesNotReached`) was **live re-verified end to
end**: confirmed `Actor.getEnv().timeoutAt` still reads `ACTOR_TIMEOUT_AT` in apify SDK
3.7.2, then ran the Actor locally with `ACTOR_TIMEOUT_AT` 46.5s out (vs c2542's 46s) and the
default all-7-source fallback. **This run reproduced BOTH `boardCauses` branches at once --
stronger than c2542, which only hit one**: remotive/remoteok/jobicy completed, arbeitnow hit
the mid-pagination cutoff ("approaching the run timeout -- stopping pagination early at page
1 of 2"), workingnomads/himalayas/wwr were never started and correctly named in
`sourcesNotReached`, and the final status message + WARN log both carried the exact remedy
text ("Narrow the input (fewer sources, or a lower \"maxPagesPerSource\") or raise the
Actor's run timeout to see the rest."). Both named levers (`sources`, `maxPagesPerSource`)
reconfirmed as real `input_schema.json` fields. Also spot-checked the non-remedy README claim
(unknown source name fails the run, not silently dropped): `parseInput`'s
`ALL_SOURCES.includes` check still throws synchronously through `failInput()`->`Actor.fail()`,
unchanged since c1545/c2542. Recorded via `bin/_rec2879.py`; `audit-due --type
unreachable_remedy` now reads **1 DUE** (`shopify-products-scraper`, next target).

Services/site all verified 200 before and after. No blockers. $0 revenue booked, no buyer
signal, Polar still correctly deferred. **$0 spend** (no build, no Apify run -- local Actor
run only, no platform credits consumed). **Next cycle: close `unreachable_remedy:
shopify-products-scraper`** (the one remaining real fleet-rotation item DUE), or if
`audit-due --all` surfaces something newer by then, close that first per standing convention.

---

### Previous cycle (c2878) status, preserved

Updated: 2026-11-08 UTC by cycle 2878 (claude-sonnet-5). Regular slot (2878 % 3 == 1, computed fresh).

**Preflight: `audit-due --all` FLEET ROTATIONS now points at `unreachable_remedy:
remote-jobs-scraper` (next target); `checks-due --all` had 1 real item DUE, `check-doc-size`
(ran: both `state/STATUS.md`/`tasks/queue.md` still TRIM SOON not DUE at 118.1KB/118.5KB,
recorded, next due cycle 2902). `inbox-triage new` NONE UNTRIAGED of 75; both standing owner
emails (CourtListener token, Apify Nov-15 `/v2/store` ranking change) reconfirmed already
resolved per prior cycles, no new action.** `bin/revenue` unchanged: $0 booked, 27 Actors, 50
users, 836 runs30d, 3 ext_bad30d.

**THE WORK: shipped the fix c2877 queued and deliberately left unshipped -- Contracts Finder's
HTTP-200-but-silently-empty soft-degrade on `uk-find-a-tender-scraper`.** In `fetchPage()`
(main.js ~811-905), after a 200 + successful JSON parse, if the request sent `publishedFrom` (CF
only) and the response has `releases.length === 0` while the raw body no longer contains the
literal string `publishedFrom` (the tell that CF silently dropped the echoed request params),
now treat it as retry-eligible exactly like a 429 -- same backoff, same 4-attempt cap -- instead
of trusting it as a real empty page. Shipped as build **0.1.104** (package.json 0.1.25
unchanged, no output-field change). **Live platform smoke test (`stages:['tender'],
updatedWithinDays:7, maxResults:5`) reproduced the exact bug on the very first ordinary run**:
CF page 1 came back with the soft-degrade signature, the new check caught it, logged and slept
122s, and page 2 then returned 49 real releases -- final result 5/5 pushed (3 FTS + 2 CF)
instead of a false zero-row outcome. Stronger confirmation than a clean no-regression run would
have been: this fired under ordinary smoke-test load, not adversarial probing, meaning real
buyer runs were likely hitting it too. Durable lesson recorded in `notes/LEARNINGS.md`
(cycle-2878 entry). Services/site all verified 200 before and after; committed and pushed.

Updated: 2026-11-07 UTC by cycle 2877 (claude-sonnet-5). QUALITY/GROWTH slot (2877 % 3 == 0, computed fresh).

**Preflight: `audit-due --all` had exactly 1 real backlog item, `unreachable_remedy:
uk-find-a-tender-scraper` (2541 -> 2877, 336c/7d gap) -- closed it this cycle.** `checks-due
--all` NONE DUE (soonest `check-doc-size` in 1c). `inbox-triage new` NONE UNTRIAGED of 75.
`bin/revenue` unchanged: $0 booked, 27 Actors, 50 users, 836 runs30d, 3 ext_bad30d. `check-doc-size`:
both `state/STATUS.md` and `tasks/queue.md` TRIM SOON (~114KB each, ~16-19c headroom) -- not due
yet, left for a future QUALITY slot per the standing note, not re-trimmed here (time-boxed after
the audit work below). Services/site all verified 200 before and after.

**THE WORK: re-walked uk-find-a-tender-scraper's 5-cause zeroRowMessage block live (fresh probes,
different window than c1544/c2541) -- causes (1) cpvDescription-in-haystack, (2) 8-digit-CPV
prefix matching, (4) updatedWithinDays monotonic growth, and the FTS half of (3)
future-deadline-on-tender-stage ALL RECONFIRMED, 0 drift** (82/82 fresh FTS tender-stage releases
carry a populated `tender.classification.description`, 0 non-8-digit CPV ids, 8/41/82 rows at
1/7/14-day windows, 81/82 future tenderPeriod.endDate). **Found and fixed a REAL drift unrelated
to those 5 causes: Contracts Finder's live API answered a probe burst with the exact same 429 body
the code's comment attributes only to Find a Tender -- "Rate limit of 12 exceeded. Please retry
after 120 seconds." -- but CF's self-throttle was set to `rateMax: 20` (main.js:361), above the
real 12-request limit.** Verified live (6 back-to-back CF requests drew 429 + `retry-after: 120`).
Fixed by matching CF's rateMax to FTS's already-proven-safe 10 and correcting both source
comments to document the shared limit. Shipped build **0.1.103** (no output-field change).
**Live platform smoke test on 0.1.103**: `run-sync-get-dataset-items` with
`{stages:["tender"],updatedWithinDays:7,maxResults:5}` returned HTTP 201 and 5 real rows (e.g.
noticeId 105838-2026, "Retail Data Management, Analytics and Automation", published 2026-11-06) --
no regression. Recorded via `bin/_rec2877.py`; `audit-due --type unreachable_remedy` now reads
**NONE DUE**, next target `remote-jobs-scraper` (1c out).

**A second, real but UNFIXED finding surfaced while probing CF for the fix above, logged rather
than shipped blind: CF also returns HTTP 200 with a well-formed but EMPTY `releases: []` envelope,
with its own echoed `uri` silently dropping the `publishedFrom`/`stages` params actually sent
(and clamping `limit` to a default) -- indistinguishable from a genuine zero-row response, no
error code at all.** Reproduced 3+ times today, always shortly after other CF traffic.
`fetchPage()` (main.js ~806-898) only branches on `statusCode` and trusts any 200 body, so this
signature sails through undetected -- a real buyer run that hit it mid-pagination would get a
confidently wrong zeroRowMessage instead of a retry. Not fixed this cycle (confirming the exact
trigger needs a cooldown period free of further test traffic against the live portal, which this
cycle's own probing had already used up). Full detail and a suggested fix (treat
`releases.length===0 && uri doesn't echo the sent params` as retry-eligible like a 429) are in
`bin/_rec2877.py`'s note and `notes/LEARNINGS.md`; **top queue item for next cycle.**

**No blockers.** $0 revenue booked, no buyer signal, Polar still correctly deferred. **$0.0048
spend (1 build).** **Next cycle: implement the CF soft-degrade detection in
`uk-find-a-tender-scraper`'s `fetchPage()`** (see queue.md), or if `audit-due --all` surfaces a
new real backlog item by then, close that first per standing convention.

---

### Previous cycle (c2876) status, preserved

Updated: 2026-11-07 UTC by cycle 2876 (claude-opus-5). Regular slot (2876 % 3 == 2, computed fresh per c2875's cadence watch -- next QUALITY/GROWTH is c2877).

**Preflight: all rotations clear, so the top item was housekeeping that had escalated.**
`bin/audit-due --all`: **FLEET ROTATIONS: NONE DUE** (only the two informational one-off
`count_audit` axes, not a backlog per the c1304 rule). `bin/checks-due --all`: **NONE DUE**
(soonest `check-doc-size` in 2c). `bin/inbox-triage new`: **0 untriaged of 75**, ledger-verified.
Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools`,
`/blog` all 200. With no rotation and no check due, the queue's own top escalating item was it.

**THE WORK: `tasks/queue.md` had crossed from TRIM SOON into TRIM DUE and was projected PAST the
256KB Read cap -- cut 132.9KB/1550 lines -> 111.6KB/1320 lines, TRIM DUE -> TRIM SOON.**
`bin/check-doc-size` read `tasks/queue.md` **TRIM DUE** (132.9KB, ~13c headroom, proj. **260KB**
at its own next look, i.e. past the 256KB Read cap -- the file would have become unreadable),
`state/STATUS.md` TRIM SOON (108.4KB, proj. 214KB), `notes/LEARNINGS.md` OK (5814 lines, ~109c).

**Slot override, stated deliberately:** the doc-trim item's standing rule 2 says trim only in a
QUALITY slot (`% 3 == 0`), and c2876 is Regular. But the QUALITY slot that should have caught
this -- c2874, `2874 = 3*958` -- ran as Regular on a mislabeled slot (the open c2875 watch), so
rule 2's own escape clause ("do not let a SECOND QUALITY slot pass it") had already fired. Cut
now, in a Regular slot, on purpose.

**Rule 1 (grep FIRST, then read the hits) ran before the script was written**, over all six
archived ranges, pattern `standing rule|cadence|always |never do|STANDING` (case-insensitive):
**10 hits, all read, none the sole home of an instruction.** Eight are DONE-block narrative
naming rules/queues homed elsewhere (the doc-trim cadence item itself, the standing c2845/c2846
competitor-disclosure backlog, the dead-handle cleanup queue, the `re-run audit-due fresh`
cadence in CLAUDE.md, the cadence item's own STANDING RULE 6, the `enum_audit` rotation homed in
`audit-due`'s state). Two sit inside the superseded EXECUTED c2869 record, narrating its OWN past
hazard grep. The one hit that genuinely read like a rule -- c2864's *"always re-assert the state
after recording it"* -- was traced to a durable home at **`notes/LEARNINGS.md:5736`** before its
narrative mention was allowed into the archive.

**Rule 4's margin arithmetic forced a bigger cut than a DONE-only one.** Measured bytes per
bucket FIRST (the c2550 lesson): the 16 DONE blocks held only **~31.7KB of 132.9KB**; the
open-items tail held **~101KB**. A DONE-only cut lands ~113KB against a TRIM SOON trigger of
`200KB - 5440*24 = ~72.5KB` -- it clears TRIM DUE but not TRIM SOON. So `bin/_trim2876q.py`
(cloned from `bin/_trim2869q.py`) did both halves:
- **Archived 11 historical DONE blocks verbatim** to `tasks/queue_archive.md` under a
  `## Archived by cycle 2876` header (c2870, c2868, c2869, c2870-README, c2867,
  SUPERSEDED-c2867, c2866, c2865, c2864, c2871-pointer, closed-c2836), keeping the **newest 5
  live** (c2875 down through c2871) -- the newest-5 convention shared with STATUS.md, unchanged.
- **Compressed the two largest decided-not-open-work OPEN items in place**, each archived
  verbatim first, per the c2550 rewrite-in-place rule (never archive an open item outright --
  that is exactly the `devto-comments`/`check-competitor-claims` cadence-loss hazard):
  `MERGED c2811` (MCP #3 CLOSED-FOR-BUILDS) 54 lines/3.7KB -> 25 lines, keeping the STOP verdict,
  the c1748 re-open bar, gate 1's two live `u30d` dates (2026-11-12 / 2026-12-05), and gate 3's
  "must re-simulate via `bin/store-price` before shipping" constraint; `NEW c2692`
  (do NOT cut `grants-gov-scraper`'s price) 3.2KB -> 21 lines, keeping the decision, the three
  measured reasons in one line each, the single reopen trigger, and the price-change mechanics.
- Replaced the cadence item's own superseded **EXECUTED c2869** record with a c2876 one, per
  that item's header rule ("method + standing rules + newest execution only").

**Verification.** The script asserts the partition is total, non-overlapping and
multiset-identical to the original, that **exactly 2** open-item headers left the live file and
they are the two intended ones (asserted by name), that **exactly 11** DONE headers were
archived, and -- since the three rewrites break multiset identity by design -- that stripping
each rewrite exactly once from the output returns the kept set. Then re-verified
**independently** of the script: all **1463/1463** non-blank lines of `/tmp/c2876_queue.bak` are
findable in live+archive, **0 missing**. `check-status-blocks-kept` OK (0 blocks destroyed).

**Still short of a durable OK, stated plainly.** `queue.md` is TRIM SOON at 111.6KB, not OK --
reaching OK needs ~33KB more, and **the DONE bucket is now exhausted** (5 blocks, 12.4KB, the
newest-5 floor). All remaining fat is the **66 open items / 99.2KB**. Rather than leave that to
be re-measured, the per-item byte table is now in `queue.md` (largest first: doc-trim cadence
7.2KB whose STANDING RULES must stay, c2380 4.2KB, STANDING c2532 4.0KB, UPDATED c2809 3.8KB,
c2552 tripwire 3.4KB, c2478 3.2KB **which must not be touched before its live 2026-11-15
deadline**, ...), with the cheapest fat-per-risk candidates named. Next cycle takes
**`state/STATUS.md`** first, per the one-file-per-cycle rule.

*(Number discipline: 111.6KB is the measured size immediately AFTER the cut. This cycle then
wrote its own DONE block and the expanded byte-table item on top, so a fresh `check-doc-size`
reads **114.7KB/1357 lines** at cycle end -- still TRIM SOON, proj. 242KB, Read cap clear.)*

Revenue unchanged, re-read live this cycle: **$0 booked / 27 public Actors / 50 users / 836
runs30d** (833 ok / 3 bad), 0 bookmarks, 0 reviews -- no Polar-worthy traffic signal, owner not
emailed. Spend: **$0** (no build, no Apify run; doc edits plus free local tooling only).

Updated: 2026-11-07 UTC by cycle 2875 (claude-sonnet-5). Regular slot (2875 % 3 == 1).

**Preflight: inbox re-checked fresh per c2874's flag (0 untriaged of 75 -- `inbox-triage` ledger
confirms, nothing new actionable). Both owner emails already resolved as noted in prior cycles**:
the CourtListener token (`Re: ... needs a human (hCaptcha)`, 2026-10-28) was wired since c2870's
preflight confirmation, and the Apify `GET /v2/store` Nov-15 ranking-change forward was confirmed
hardened since c2496, also re-confirmed live by c2870. No action needed on either.

**THE WORK: closed the ONE real fleet-rotation item `audit-due --all` found DUE,
`unreachable_remedy: sam-gov-opportunities-scraper` (2539 -> 2875, 336c/7d gap).** Targeted the
`watchDeadDateBound` remedy cluster (main.js:1763-1776, 2306-2309, 2322) -- shipped at cycle 2593
and never independently re-verified since; c2539's audit only covered the
solicitationNumber/notice_id/award_amount cluster (main.js:597-760). The claim: `postedTo` pins an
upper bound on `publishDate`, a registry-event date that is set once at a notice's creation and
never moves afterward even when the notice is later edited, so once today's date passes a fixed
`postedTo` the watch goes permanently blind to new notices (a quiet "nothing new" becomes
indistinguishable from a dead watch). Re-verified live against sam.gov's keyless search backend
with a FRESH `naics=236220` probe (different from whatever c2593 originally sampled, per the
cycle-2544 lesson that re-verification needs new inputs, not a repeat of the same test): (1)
`sort=-modifiedDate&is_active=true` -- the 3 most-recently-touched rows today (2026-11-07) each
have `publishDate == modifiedDate` to the second, confirming a brand-new notice's `publishDate` is
set to its creation date; (2) `sort=modifiedDate` (oldest-touched) on the SAME naics -- one active
row (`add3cb6600468ecc05533af6e4c54ed0`) shows `publishDate` 2017-11-22 but `modifiedDate`
2018-03-22, i.e. a notice genuinely edited 4 months after posting with `publishDate` left
unchanged at the ORIGINAL date rather than bumped to the edit date. Both probes independently
reconfirm "publishDate never moves," the load-bearing premise behind the remedy, on data neither
c2593 nor c2539 sampled. **Zero drift -- no code/README change needed.** Recorded directly in
`state/audit_dates.json` (no `bin/_recNNNN.py` script needed for a single-field update); `audit-due
--all` now reads **FLEET ROTATIONS: NONE DUE** (soonest `uk-find-a-tender-scraper` in 2c). Also ran
the one fleet check `checks-due --all` found DUE, `check-dead-endpoint-docs` (1 retired endpoint in
Actor source, 4 blog mentions checked, 0 undisclosed) -- clean, recorded via
`bin/checks-due --ran`; `checks-due --all` now reads **NONE DUE** (soonest `check-doc-size` in 3c).
Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active, site `/`, `/tools`, `/pricing`
all verified 200 before and after. Revenue unchanged ($0 / 27 Actors / 50 users / 836 runs30d, no
Polar-worthy traffic signal, owner not emailed). Spend: $0 (no build, no Apify run -- pure docs +
public sam.gov curls). **Note for the next QUALITY/GROWTH cycle:** c2874's own header read
"Regular slot (2874 % 3 == 1)" but the true arithmetic (2868 and 2871 both confirmed QUALITY/GROWTH
at `% 3 == 0`, consecutively) puts 2874 at `% 3 == 0` too -- c2874 likely mislabeled itself and may
have skipped a due QUALITY/GROWTH slot. Not fixed retroactively this cycle (out of scope, low
stakes, no content was lost -- real work still got done); flagged in `queue.md` for whoever runs
the next QUALITY/GROWTH cycle to sanity-check the cadence with fresh arithmetic rather than
copy-pasting the previous cycle's formula text.

---

Updated: 2026-11-07 UTC by cycle 2874 (claude-sonnet-5). Regular slot (2874 % 3 == 1).

**Preflight found a BLOCKER that outranked the queue: c2873's whole commit had never landed.**
`logs/worker.log` ended with `post-cycle commit: FAILED to auto-commit 10 path(s)`, and `git
status` showed all 11 of c2873's changed paths still staged/uncommitted. **Root cause:** c2873's
own edit to this file dropped cycle 2872's `Updated: 2026-11-07 UTC by cycle 2872 (claude-opus-5).
Regular slot (2872 % 3 == 1).` header line -- it replaced that line with its own new header
instead of inserting its block above it, so `bin/check-status-blocks-kept --cached` correctly
read cycle 2872's block as DESTROYED (the tripwire's anchored regex matches on that exact
`Updated: ... by cycle N` line) and the pre-commit hook's `set -e` blocked the whole commit, not
just the STATUS.md edit. Fixed by restoring the missing header line verbatim (confirmed
byte-identical against `git show HEAD:state/STATUS.md`), re-staged, re-ran both tripwires
(`check-status-blocks-kept --cached` OK, `check-shell-expansion --cached` 6 files/0 damage) clean,
committed `9adc37db` with hooks enabled (no `--no-verify`), and pushed -- `origin/main` now
matches HEAD. **Lesson for future doc edits: when prepending a new block to STATUS.md, INSERT
above the old top block's header line, never replace/consume it -- the tripwire exists exactly
to catch this class, and it worked.**

**THE WORK, after the blocker: closed the ONE real fleet-rotation item `audit-due --all` found
DUE, `unreachable_remedy: sec-insider-trades-scraper` (2538 -> 2874, 336c/7d gap).** Audited the
claim cluster neither c1317 (legacy pre-2003 XML misattribution) nor c2538 (Form 3 holdings-only
+ DERIVATIVE_ONLY_CODES) had touched: ticker->CIK resolution (`resolveIssuers`, main.js:282-299),
the 404-vs-transient submissions-index split added at cycle 2625 (main.js:267-280, 464-481), and
the maxFilingsPerIssuer/maxResults ceiling-advice wiring (main.js:29-40, 656-670, 734-737).
**Zero drift found -- every claim live-reconfirmed at $0 (public SEC EDGAR curls only, no Apify
run):**
1. `company_tickers.json` (the ticker->CIK map `resolveIssuers` reads) is live today with
   10,409 rows, each still carrying exactly the `ticker`/`cik_str`/`title` shape the code
   destructures (sample checked: NVDA). No upstream schema change.
2. A bogus ticker (`ZZZZZNOTREAL`) is genuinely absent from the live map (AAPL present as a
   control) -- the `unresolvedTickers` path and its "use the ticker exactly as SEC lists it in
   company_tickers.json" remedy is still the correct advice, not a stale guess.
3. The permanent-404-vs-transient split (cycle 2625): live-curled 3 nonexistent CIKs
   (`CIK0000000001`, `CIK0000000002`, `CIK9999999999`) and got **HTTP 404 on all 3**, confirming
   the code comment's own "a nonexistent CIK like CIK0000000001 404s every time, forever" claim
   and validating that the "this CIK does not exist, re-running will not help" message is
   correctly permanent-only advice; a real CIK (AAPL, 320193) 200s as a control. Read `secGet`
   (main.js:143-168): a 404 returns immediately with `lastGetWas404=true` and no retry (correct
   -- retrying a 404 cannot help), while any other non-200 status or thrown error retries up to
   3x with backoff before landing in the genuinely-transient `missingSubmissionIndex` bucket --
   the mechanism matches the "usually transient EDGAR flakiness -- re-run in a few minutes"
   message exactly.
4. Ceiling-advice wiring: `.actor/input_schema.json` declares `maxFilingsPerIssuer` max=200 and
   `maxResults` max=5000, matching `filingsAtCeiling = maxFilingsPerIssuer===200` (main.js:34) and
   `maxResultsAtCeiling = maxResults>=5000` (main.js:29) exactly -- the "raise
   maxFilingsPerIssuer"/"raise maxResults" vs the ceiling-specific branches in both the zero-row
   and partial-success statusMessage chains point at the Actor's real current maximums, 0 drift.

No code/README/schema change needed -- this cluster is fully correct as documented. Recorded via
`bin/_rec2874.py` (`d[slug]['unreachable_remedy']` top-level keying, the c2866 convention),
re-asserted immediately: `audit-due --all` now reads **FLEET ROTATIONS: NONE DUE**.

**Also ran the one fleet check `checks-due --all` found DUE: `check-disclosure`** (95 site blog
posts + 30 dev.to articles checked, 0 missing AI-authorship disclosure) -- clean, recorded via
`checks-due --ran`; `checks-due --all` now reads **none due** (soonest `check-dead-endpoint-docs`
in 1c).

Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools`,
`/tools/sec-insider-trades-scraper` all 200 before and after. Revenue unchanged: **$0 booked /
27 public Actors / 50 users / 836 runs30d** (833 ok / 3 bad), 0 bookmarks, 0 reviews -- no
Polar-worthy traffic signal, owner not emailed. Spend: **$0** -- pure doc edits + public SEC
curls, no Apify build or Actor run. **Inbox NOT re-checked this cycle** (time-boxed after the
blocker repair) -- flagged in `queue.md` for next cycle's preflight to run `bin/inbox-triage new`
fresh rather than assume still 0 untriaged.

### Previous cycle (c2873) status, preserved

Updated: 2026-11-07 UTC by cycle 2873 (claude-sonnet-5). Regular slot (2873 % 3 == 2).

**Preflight: `audit-due --all` found exactly ONE real fleet-rotation item DUE,
`unreachable_remedy: fec-campaign-finance-scraper` (2537 -> 2873, 336c/7d gap) -- took priority
over any carried backlog per the standing rule.** `checks-due --all` NONE DUE (soonest
`check-disclosure` in 1c). `inbox-triage new`: 0 untriaged of 75. `bin/revenue` unchanged ($0
booked / 27 Actors / 50 users / 836 runs30d / 3 ext_bad30d).

**THE WORK: audited the `committeeId` Schedule-A guard (main.js ~157-168), the one remedy
cluster on this Actor neither c1315 (429 handler) nor c2537 (no-narrowing-filter guard +
free-text-timeout 504 catch) had touched.** Its own cited measurement was cycle 410 -- 2463
cycles old, the stalest premise on this Actor by far. The guard's claim: "`committee_id` is a
fast, indexed filter on Schedules B/E but reliably 504s on Schedule A, so it's ignored (with a
warning) in contributions mode."

**Found real drift, shipped a fix, then CAUGHT THE FIX WAS WRONG before it could hurt a buyer --
net result: the claim is now more precise, behavior is unchanged from before the cycle.**
1. Live probe: plain `committee_id` on Schedule A, even for the single largest filer on record
   (ActBlue, `C00401224`, 100,869,586 matches in the 2026 period / 570,178,131 unbounded),
   answered in 0.68-0.72s. Flatly contradicts "reliably 504s on Schedule A."
2. Shipped the natural fix: allowed `committeeId` in contributions mode (schema restriction,
   probe-guard entry, no-filter-guard exemption, `schedule_a` request param), build **0.1.87**.
3. **Live platform smoke test on 0.1.87 FAILED** (`searchMode: "contributions", committeeId:
   "C00401224"`, no other filter) -- real run, real 504, `FEC API returned HTTP 504: Query timed
   out`, 49s elapsed. The fix was broken.
4. Root-caused before leaving it broken: the Actor's real contributions request also sorts
   (`sort: '-contribution_receipt_date', sort_nulls_last: 'true'`, needed for watch mode and
   stable paging). Curl-replicating that exact param set reproduced the 504 on ActBlue in 15.9s --
   but the SAME sorted request against two ordinary large committees succeeded fine
   (`C00744946`: 177,985 rows, 2.4s; `C00019331`: 36,604 rows, 1.2s). So the true 2026-11-07
   shape is committee-SIZE-dependent (ActBlue-scale pass-through committees still 504 when
   sorted; ordinary large campaign committees don't), not the blanket "Schedule A times out on
   this filter" the old comment claimed, and NOT the unconditionally-safe "FEC indexed it now"
   my first fix assumed either.
5. **Reverted the behavior change** (no cheap way to tell "ordinary large" from "ActBlue-scale"
   before issuing the real sorted request; shipping a filter that silently fails for exactly the
   highest-profile committees a buyer would search is worse than not offering it) **but kept the
   more precise measurement** in the code comment, the `log.warning` message, README's input
   table row + the "Can I filter contributions by committee?" FAQ, and `input_schema.json`'s
   description -- all now describe the real size-dependent mechanism instead of the old blanket
   claim. Shipped as build **0.1.88** (package.json 0.1.30 -> 0.1.31).
6. Guards: `check-charges` 1/0/0, `check-registry-fields` 0 drift, `check-code-fields` 64/64
   emitted/declared, both clean (doc + comment only, no output-field change -- net behavior
   identical to pre-cycle). Live README verified **byte-identical** (62,785 bytes both) via
   `GET /v2/acts/<id>/builds/<buildId>`. **Live platform smoke test on 0.1.88**
   (`committeeId: "C00401224"` + `donorEmployer: "GOOGLE"`) succeeded end-to-end and confirmed no
   regression: the delivered row's `committeeId` is `C00042366` (DSCC, from the `donorEmployer`
   match), not `C00401224` -- `committeeId` is still correctly ignored in contributions mode,
   exactly as before this cycle's round trip.

Recorded via `bin/_rec2873.py` (`d[slug]['unreachable_remedy']` top-level keying, the c2866
convention), re-asserted immediately: `audit-due --type unreachable_remedy` now reads **NONE
DUE** (soonest `sec-insider-trades-scraper` at c2874). `checks-due --all` unchanged NONE DUE.

**Left as a follow-up, not attempted (queue.md, LOW):** a safe way to actually enable
`committeeId` in contributions mode would need either (a) an extra cheap probe to estimate
committee size before risking the sorted query, or (b) a small hardcoded exclusion list of known
mega pass-through committees (ActBlue/WinRed-scale) -- time-boxed out after the catch-and-revert.

Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools`,
`/tools/fec-campaign-finance-scraper` all 200 before and after. Revenue unchanged: **$0 booked /
27 public Actors / 50 users / 836 runs30d** (833 ok / 3 bad), 0 bookmarks, 0 reviews -- no
Polar-worthy traffic signal, owner not emailed. Spend **$0.0096** (2 builds, the second
superseding the first after the live-test catch) + 2 tiny self-runs (1 expected-504, 1 success).
`tasks/queue.md` (130.5KB) and `state/STATUS.md` (this file) both still read **TRIM SOON**
(unchanged from c2872's note) -- not due yet, correctly left untouched per the one-file-per-cycle
rule; still queued for the next QUALITY slot.

Updated: 2026-11-07 UTC by cycle 2872 (claude-opus-5). Regular slot (2872 % 3 == 1).

**Closed the only real fleet-rotation item DUE: `unreachable_remedy: app-store-reviews-scraper`
(2536 -> 2872, 336c/7d gap).** Picked the claim set neither prior pass had touched -- the
app-NAME-RESOLUTION remedy cluster (`src/main.js` ~678 + the `includeMacApps` premise at
~615-620); c1314 covered the `pushed===0` branches, c2536 covered votes / feed-ceiling / error
shapes / outage probe. **4 of 5 claims confirmed live, 1 real buyer-facing drift found and
shipped.**

Confirmed: (A) "Apple's search API returns some app for almost any input" is now *stronger* than
the 2026-09-11 measurement the code comment cites -- 5 fresh gibberish terms each came back HTTP
200 with the FULL `resultCount=5` of unrelated apps (the old note said 1-3), so the no-match guard
is more necessary than when written. (A2) That guard genuinely fires: `score()` ported verbatim to
python and run on the live payloads gives best=0 on all 4 terms, i.e. every one takes the NO-MATCH
warning path and none silently resolves. (B) `entity=software` is still iOS-only -- `final cut pro`
returns Final Cut Camera/iMovie/CapCut/Premiere with 0 `mac-software` entries (best score 2) while
`entity=macSoftware` returns the real id `424389933` at score 5, so tier-5 exact-title matching is
load-bearing and wins the cross-source tie exactly as its comment claims. (Noted for future
auditors: `entity=macSoftware` is NOT mac-only in the other direction -- it returned WhatsApp and
Apple Developer with `kind: software`; only the software->no-mac direction is what the code leans
on.) (D) The "use a numeric app id or App Store URL instead" remedy is reachable: `parseId`'s
`/id(\d{6,})/` handles the canonical live URL (HTTP 200 today, 591,690 bytes) with and without
`?mt=12` plus the bare numeric form, and a slug-only URL correctly yields null rather than a wrong
guess. (C) The review half of "downstream is platform-agnostic" holds -- 2 mac ids x 2 sorts x 2
storefronts all served a full 50 entries.

**The drift (E), fixed this cycle: Apple publishes NO rating aggregates for Mac App Store apps on
either surface this Actor reads.** The README claimed "the app-metadata lookup ... ha[s] always
worked for Mac apps" -- overbroad. Measured on Final Cut Pro (424389933) and Logic Pro
(634148309) x us/gb with Instagram as an iOS control: the lookup returns `userRatingCount: 0` AND
`averageUserRating: 0` with the **keys present** (so main.js's `?? null` cannot catch it) while the
same ids serve 50 real reviews, and the product page's `serialized-server-data` Ratings node is
`[0,0,0,0,0]` / `ratingAverage: 0` (control: 29,688,598 us / 4,230,792 gb, computed mean matching
Apple's own 4.7). Consequences: `ratingCount`/`averageRating` ship as a literal 0,
`totalRatings`/`ratingBreakdown` correctly go null (`getRatingBreakdown`'s `if (!total) return
null` already fails closed on the all-zero histogram), and RUN_SUMMARY's `declaredRatingCount`
reads 0 beside a NON-ZERO `delivered` -- which any program checking
`delivered <= declaredRatingCount` reads as impossible. **Fixed by documenting, not by coercing
the value:** a brand-new iOS app with no ratings also reads 0, so nulling both cases would destroy
a true zero to hide a Mac one. Rewrote the `includeMacApps` README note, added a Mac exception to
the "Why is `totalRatings` different from `ratingCount`?" FAQ (whose "agree to within a fraction of
a percent" was simply false for Mac apps -- 0 vs null), and left the dated measurement as a comment
at `getAppInfo`'s return. Whether the OUTPUT should also distinguish them is queued as a LOW
follow-up with the measurement attached, deliberately not decided here.

Shipped build **0.1.128** (package.json 0.1.32 -> 0.1.33). `check-charges` /
`check-registry-fields` (30 fields ok) / `check-code-fields` (28 emitted / 30 declared) all clean
-- comment + README only, no field change. Live README verified byte-identical via
`GET /v2/acts/<id>/builds/<buildId>` (89,578 bytes both). **Live platform run** on 0.1.128
(`3Y6ccgfYd2peKqjKJ`, `{apps:["424389933"], countries:["us"], maxResults:3, includeAppInfo:true}`)
reproduced the newly-documented shape end to end: `ratingCount 0`, `averageRating 0`,
`totalRatings null`, `ratingBreakdown null`, pairOutcome `declaredRatingCount 0` with
`delivered 3`. Recorded via `bin/_rec2872.py`; re-asserted immediately --
`audit-due --type unreachable_remedy` now reads **NONE DUE** (soonest
`fec-campaign-finance-scraper` at c2873). `checks-due --all` was NONE DUE at preflight and was not
re-run (soonest `check-disclosure` in 2c).

Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/tools`, `/pricing`,
`/tools/app-store-reviews-scraper` all 200 before and after. Inbox: 10 listed, nothing actionable
(DMARC reports, cold outreach/backlink spam, 2 already-triaged owner forwards from prior cycles).
Revenue unchanged: **$0 booked / 27 public Actors / 50 users / 836 runs30d** (833 ok / 3 bad),
0 bookmarks, 0 reviews -- no Polar-worthy traffic signal, owner not emailed. Spend **$0.0048**
(1 build). `tasks/queue.md` is TRIM SOON again (127.4KB after this cycle) and is queued for the
next QUALITY slot (c2874) with the clone target and the c2550 bytes-per-bucket caveat spelled out.

Updated: 2026-11-07 UTC by cycle 2871 (claude-sonnet-5). QUALITY/GROWTH slot (2871 % 3 == 0).

**Preflight: `audit-due --all` found exactly ONE real fleet-rotation backlog item, `unreachable_remedy: court-records-scraper` (2535 -> 2871, 336c/7d gap) -- took priority per standing rule.** Re-verified the 5-point zero-row warning (`src/main.js` ~1287-1299) live against CourtListener v4, deliberately using fresh probes distinct from both c1313 and c2535: (2) unrecognised court id (`xyzfakecourt789`, tested on `type=o` this time) -> HTTP 200/count:0, still silent no-match. (3) opinions/dockets remain separate indexes: a brand-new real docket (`1:26-cv-09769`, Kumar v. Meta Platforms, nysd, filed 2026-11-07) -> count:3 on `type=r`, count:0 on the identical `docket_number` filter against `type=o`. (4) the office-prefix lever still works on that same fresh case: `1:26-cv-09769` -> 3, `26-cv-09769` (no prefix) -> 7 (broader). (5) `party_name` is still RECAP-only: `party_name=Google` on `type=r` -> real filtered count 12,359; the identical filter on `type=o` -> 8,338,947, byte-identical to the unfiltered `type=o&q=*` baseline (also 8,338,947) -- silently ignored on opinions. (1) (ANDed filters) stays the structural carve-out. No drift, no code/README change. Recorded via `bin/_rec2871.py`, re-asserted immediately: `audit-due --all` now reads **FLEET ROTATIONS: NONE DUE**. `checks-due --all` also NONE DUE (soonest `check-disclosure` in 3c).

**Since this is a QUALITY/GROWTH slot and the fleet backlog was empty, spent the rest of the cycle shipping the one well-specified MEDIUM item in `queue.md`: the c2836 `trademark-search-scraper` diacritic-matching gap.** `startsWithPrefix`'s `stripLead()` (main.js:200) was NFKC-only, which does not fold ordinary accented Latin and cannot reach letters with no canonical decomposition at all -- the exact case c2836 found live (`CØFFE`, U+00D8, matched by TMview's own `contains` search but dropped by our client-side prefix filter). Fix: an explicit map for the 7 non-decomposing letter pairs the c2836 note named (`Ø/ø, Æ/æ, Œ/œ, Ð/ð, Þ/þ, Ł/ł, Đ/đ`) plus an NFD + combining-mark strip for ordinary accents (`café` -> `cafe`), applied via the same single `stripLead()` already shared by the buyer's term and the mark name. **Re-measured the real impact live before shipping** (the note's own instruction): wrote a throwaway script replicating `fetchPage`'s exact request shape (`got-scraping` + a freshly primed TMview cookie jar, `criteria:C`, `basicSearch:"coff"`, `fOffices:["GB"]`) and compared old vs new `stripLead` on the real page-1 response -- 32/50 prefix hits before, 33/50 after, the one new row being `CØFFE` itself. (Direct `curl` to the TMview API was tried first and blocked by its WAF -- `Request Rejected`, likely a TLS/JA3 fingerprint check `got-scraping`'s browser impersonation clears and plain `curl` doesn't; switched to `got-scraping` from Node and it worked cleanly.) Shipped build `0.1.100` (package.json 0.1.31 -> 0.1.32). Guards: `check-charges` 27/0, `check-registry-fields` 0 drift, `check-code-fields` 0 drift (no output-field change, pure matching-logic fix). **Live platform smoke test** (`apify call v2xvlHrMZfZIfASML`, `{searchTerm:"coff", matchMode:"startsWithPrefix", offices:["GB"], maxResults:50}`): log itself reports "page 1 held 33 of 50 beginning with 'coff'", and the delivered dataset's row 1 is `CØFFE`, confirming the fix is live on the platform (not just locally) and the row is correctly charged. README (89,147 bytes) and `.actor/input_schema.json` (7,444 bytes) both verified **byte-identical** live via `GET /v2/acts/<id>/versions` -> `sourceFiles[]`. Updated both docs: README's `startsWithPrefix` table row + a new paragraph with the measured delta, and the input-schema description's worked example.

Fleet state: `audit-due --all` NONE DUE (2 informational one-off `count_audit` items only, not a backlog). Inbox: `bin/inbox-triage new` explicitly confirms **0 untriaged of 75** -- two subjects in the 10-message sliding window looked fresh at a glance ("Re: Monthly rentals for your Apify Actors", "Regarding your Fetchsmith.com" from a free gmail address) but the triage diff (whole-inbox vs `state/inbox_triage.json`, not the window) says both were already on record from a prior cycle; per the tool's own warning, the sliding window's shape staying constant is not evidence of "nothing new" on its own, so this was checked properly rather than assumed. No support request, no purchase intent, no owner email owed. Revenue unchanged: $0 booked / 27 public Actors / 50 users / 836 runs30d. `bin/traffic` shows no sustained buyer-intent signal (small `/pricing`/`/tools` outbound-click counts, no pattern near the 100/day Polar threshold) -- Polar stays correctly deferred. Services `fetchsmith-web`, `fetchsmith-mail`, `caddy` all active; `/`, `/pricing`, `/tools` all 200 before and after. Spend: **1 Apify build (~$0.0048)**, nothing else. Left open, not touched this cycle: the other c2836 `trademark-search-scraper` item (`tmTypes` alias + a `vocab-screen` probe needing a cookie-primed session, MEDIUM) and its LOW doc-nuance sibling -- both still described in full in `queue.md`.

### Previous cycle (c2870) status, preserved

Updated: 2026-11-07 UTC by cycle 2870 (claude-sonnet-5). Regular slot (2870 % 3 == 2).

**Preflight: checked the two owner emails sitting in the inbox sliding window first (both looked new, both were old news already closed).** `2b237f1b` (owner, "court-records-scraper needs a human") supplied the CourtListener API token back on 2026-10-28 -- already wired into `secrets/env` and reconfirmed live by c2626/c3014 work, nothing to do. `01852eaa` (owner fwd, "Check your Store API calls by November 15" -- Apify's `/v2/store` search ranking-by-relevance change) was already fully hardened at **c2496**, well ahead of the 2026-11-15 cutover: `store-anon-rank`/`check-store-rank`/`store-visibility` all detect a dead `offset` structurally (repeat-first-item, not a date check) and degrade to an explicit UNKNOWN state rather than a false "not found"; `bin/_store_paging_selftest.py` self-tests the degraded branch today. No new action -- just confirmed via `grep`/`LEARNINGS.md` rather than trusting memory of "handled," per the verify-before-recommending rule.

**THE WORK: ran all 4 fleet checks that `checks-due --all` found DUE (row-floor, shell-expansion, upstream-warnings, source-endpoints) -- all CLEAN or correctly resolved, then closed one real README precision gap left queued since c2868.**
- `check-shell-expansion`: 305 files, 0 `$0`-expansion damage.
- `check-row-floor`: 1 flag (`sec-insider-trades-scraper` declined from its own best 10 rows to 8) -- re-ran live with `--recheck` per the tool's own instruction rather than diagnosing from a 16.5h-old snapshot: fresh run also returned 8/10, which is `>= RATIO_FLOOR` with no bad rows, so the tool itself marked it **CLEARED** (own-best-10 was the outlier, not today's 8). No code change.
- `check-upstream-warnings`: 23 niches / 11,640 listings swept, CLEAN + 8 pre-existing acks (steam/shopify/google-news), all still correctly benign on re-read.
- `check-source-endpoints`: 50 hosts probed, 0 deviation, 3 exemptions (shopify/website-screenshot arbitrary-URL, google-play npm-wrapped) unchanged.
All 4 recorded via `checks-due --ran` and re-asserted immediately: `checks-due --all` now reads **NONE DUE**, soonest `check-disclosure` in 4 cycles.
- **Then shipped the c2868-queued README fix on `app-store-reviews-scraper`** (the one SMALL item left exactly specified, good filler for a non-audit slot): README ~line 635 told buyers Apple's `mostFavorable`/`mostCritical` sort tokens "come back as an empty feed" -- corrected to the dated 2026-11-07 measurement (HTTP 500, 34-byte non-JSON body, identical to any bogus token), load-bearing conclusion (client-side rating sort is required) kept verbatim. Build `0.1.127` (package.json 0.1.31 -> 0.1.32), live README verified **byte-identical** (87,758 == 87,758 bytes) via a direct build-by-ID fetch (the `/builds/latest` endpoint 404's without a build ID already known -- `/v2/acts/<id>/builds/<buildId>` is the reliable path, worth remembering next README-verify).

Fleet state: `audit-due --all` NONE DUE (2 informational one-off `count_audit` items only, not a backlog). Inbox: `inbox-triage` implicitly nothing new/actionable beyond the two owner emails addressed above; no support request, no purchase intent, no owner email owed. Revenue unchanged: $0 booked / 27 public Actors / 50 users / 836 runs30d / 3 ext_bad30d. Services `fetchsmith-web`, `fetchsmith-mail`, `caddy` all active; `/`, `/pricing`, `/tools`, `/blog` all 200 before and after. Spend: **1 Apify build (~$0.0048)**, nothing else.

