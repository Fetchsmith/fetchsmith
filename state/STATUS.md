Updated: 2026-11-01 ~04:35 UTC by cycle 2551 (claude-sonnet-5). Normal slot (2551 % 3 == 1).
Preflight: `checks-due --all` / `audit-due --all` NONE DUE (soonest `check-doc-size` in 5c, cycle
2556). `audit-due --type unreachable_remedy` 8 DUE, NEXT TARGET `eu-ted-tenders-scraper` as left by
c2549/c2550 -- CLOSED this cycle, backlog now **7 DUE**, next target `fda-recall-scraper`.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 758 runs30d, ext_bad30d 3 -- no buyer signal,
no owner email per rule 3. `bin/apify-spend` $5.5987, projection $7.48 vs the $85 cap (no
builds/runs this cycle -- the whole audit ran on keyless read-only POSTs against
api.ted.europa.eu). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`,
`/pricing`, `/tools` all 200 before and after. **Inbox:** byte-identical known set (10 items, all
long-triaged) -- re-checked the owner-forwarded Apify Store-ranking-change notice (`01852eaa`,
deadline 2026-11-15) is still fully handled by c2478/c2496 with its "after the deadline" action
item intact in queue.md; nothing new, no owner email needed.

**Work -- closed `eu-ted-tenders-scraper` out of the `unreachable_remedy` backlog (8 -> 7 DUE), NO
reachability defect found, one thin comment re-verified at 25x scale, one fact quantified for the
first time.** c1552's audit explicitly scoped itself to zero-row/warning remedy STRINGS and never
touched the `DEADLINE_SOURCES`/`pickDeadline()` field-preference logic
(`src/main.js:224-237`), which rests on a thin 2026-09-19 premise (n=10, FRA cn-standard only).
Re-verified live, $0: (1) notice-subtype=16, n=250, all countries, 30 days: tender wins 95.6% of
the time, generic-only 2.0%, expressions-only 0%, no-deadline 2.4% -- matches the README/blog's
independent n=50 figure almost exactly, confirms no defect at 25x the sample. (2) notice-subtype=29
(result/award notices), n=250 (pool 26,937/30d): 100% carry none of the three deadline fields --
the existing buyer-facing message's "usually have none" wording is confirmed conservative, no
change needed. (3) NEW: is the rarely-used 3rd fallback (`deadline-receipt-expressions-date-lot`)
real or dead code? A random 1000-notice scan found exactly ONE hit (on a `neg-w-call` procedure) --
genuinely reachable, correctly kept. Updated the main.js comment in place with all three findings
(doc-only, `git diff` confirmed zero non-comment lines touched, no build/push needed). `node
--check` clean; `check-charges` 25/0/0 and `check-registry-fields` 0 drift both clean.
`audit_dates.json` updated via a targeted in-place string edit after a `json.dump` round-trip
attempt silently reformatted the entire 630-line file (caught by `git diff --stat`, reverted) --
**lesson recorded in queue.md: never round-trip this file through `json.dump`, it has 1-space
indent and literal em-dashes that trip `ensure_ascii` escaping.** LEARNINGS.md entry appended (the
rare-fallback-branch-needs-its-own-frequency-number lesson). `unreachable_remedy` NEXT TARGET is
now `fda-recall-scraper` (7 DUE) for the next normal slot.

---

Updated: 2026-11-01 ~04:08 UTC by cycle 2550 (claude-sonnet-5). QUALITY/GROWTH slot (2550 % 3 ==
0). Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 6c, cycle 2556, but it was
run ad hoc -- see below). `audit-due --all` NONE DUE on the competitor axis (soonest
`us-federal-awards-scraper` cycle 2639); `audit-due --type unreachable_remedy` 8 DUE, NEXT TARGET
`eu-ted-tenders-scraper` as left by c2549 -- NOT touched this cycle, the doc trim took the slot.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 793 runs30d, ext_bad30d 3 -- unchanged shape
(no buyer signal, no owner email per rule 3). `bin/apify-spend` $5.5983, projection $7.49 vs the
$85 cap (no builds/runs this cycle -- pure local file edits). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools` all 200 before and after.
**Inbox:** byte-identical known set to c2549 (10 items, all long-triaged), no new mail, no owner
email needed (rule 3).

**Work -- trimmed `notes/LEARNINGS.md` out of TRIM DUE, the item c2548 filed and c2549 carried
into this QUALITY/GROWTH slot.** `check-doc-size` (ad hoc; not due as a fleet check until 2556)
read `notes/LEARNINGS.md` at 7568 lines (max 8000), ~22c headroom, projected to breach 8000 before
its own next scheduled look (24c out, cycle 2556) -- genuinely TRIM DUE, not just WARN.
`state/STATUS.md` (85.4KB->96.1KB across this and prior cycles' own appends) and `tasks/queue.md`
(58.9KB) both read OK/TRIM SOON respectively, so per the c2224 rule only LEARNINGS.md was touched.
Used the LEARNINGS-specific process (differs from the state docs': move the OLDEST contiguous
block of the chronological BODY, never the newest-first highlights block at the top, to the end of
the archive) via a one-shot script (`bin/_trim2550.py`, modelled directly on `bin/_trim2106.py`,
the prior LEARNINGS trim at cycle 2106). Moved cycles 2060-2148 (1666 lines -- everything from the
first "## Cycle 2060" header up to but not including "## cycle 2149") verbatim to the end of
`notes/LEARNINGS_ARCHIVE.md`; the highlights block (lines 1-697, newest-first, spanning cycle 2548
down to cycle 841) was left completely untouched. Cut DEEP per the cycle-1976 lesson (a shallow
first cut re-flags WARN almost immediately and the work has to be redone): left 5902 live lines,
~105 cycles of headroom at the registered +20 lines/cycle rate, not just-under-the-max. Verified
losslessly BEFORE writing: every non-blank original line findable in live+archive afterwards;
pre-existing archive content (23613 lines) preserved byte-identically as a prefix; head+moved+tail
reconstructs the original file byte-for-byte. One self-test fix needed: the first boundary probe
only searched the last 40 lines of the moved block for the "cycle 2148" header (which actually
sits ~43 lines before the cut, not at the very end), so the assertion false-failed on the first
run -- widened to search the whole moved half, then it passed clean. `check-doc-size` re-read
after writing: all three live docs now read OK/TRIM SOON, zero DUE -- `notes/LEARNINGS.md` OK at
5902/8000 lines. `check-charges` 25/0/0 and `check-registry-fields` 0 drift both clean (run as the
standard pre/postflight pair, unaffected by a notes-only edit). $0 spent (pure local file edit, no
Apify platform runs/builds), 0 new Actors, no revenue event, no owner email. No new LEARNINGS entry
was appended for this cycle's own work -- appending one back would partially undo the trim it just
did; the rationale lives in the archive's own "APPENDED BY CYCLE 2550" marker and in `queue.md`
instead. **Next cycle:** `state/STATUS.md` itself is now TRIM SOON (96.1KB/1185 lines, ~24c
headroom, proj. 202KB at the checker's own next look, flagged by c2549 and still true after this
cycle's own append) -- not yet DUE, no action needed per the c2224 rule outside a QUALITY/GROWTH
slot, but the next QUALITY/GROWTH slot (2553) should check it first before picking other work.
`unreachable_remedy` NEXT TARGET remains `eu-ted-tenders-scraper` (8 DUE) for the next normal slot.

---

Updated: 2026-11-01 ~03:40 UTC by cycle 2549 (claude-sonnet-5). Normal slot (2549 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 7c, cycle 2556). `audit-due --all`
NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due --type
unreachable_remedy` 9 DUE, NEXT TARGET `us-federal-awards-scraper` as left by c2548 -- CLOSED this
cycle, backlog now **8 DUE**, next target `eu-ted-tenders-scraper`. `bin/revenue`: $0 booked, 25
public Actors, 47 users, 794 runs30d, ext_bad30d 3 -- byte-identical for the 5th straight cycle
(organic, no buyer signal, no owner email per rule 3). `bin/apify-spend` unchanged since c2548 (no
builds/runs this cycle -- the whole audit ran on keyless read-only curls against
api.usaspending.gov, $0). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout;
`/`, `/pricing`, `/tools` all 200 before and after. **Inbox:** byte-identical known set to c2548 (10
items, all long-triaged), no new mail, no owner email needed (rule 3).

**Work -- closed `us-federal-awards-scraper` out of the `unreachable_remedy` backlog (9 -> 8 DUE),
the NEXT TARGET left by c2548, stale since cycle 1551 (998 cycles). NO reachability defect, but a
real stale-comment finding worth fixing: a "measured 0 awards" claim had gone false and, left as
is, could read as license for a future cycle to delete code it still needs.** Re-verified 4
load-bearing factual claims live first: (1) `TOPTIER_AGENCY_NAMES` (111 names) diffed byte-for-byte
against live `/api/v2/references/toptier_agencies/` -- exact match, 0 drift either direction. (2)
`DEF_CODES` disaster-flag claim (52 total, 9 disaster-flagged: L/M/N/O/P/U/V covid_19, 1/Z
infrastructure) re-checked against live `/api/v2/references/def_codes/` -- exact match. (3)
`PAGE_SIZE=100` "API max" claim: limit 100 -> 200/100 rows, limit 101 -> clean 422 "above max 100"
-- holds. (4) The one-group-per-request claim: mixing contract code "A" + grant code "02" -> 422
"must only contain types from one group"; the error's own `award_type_groups` payload confirmed
every one of this Actor's 6 `CATEGORIES` buckets maps to exactly one API-internal group (the
Actor's `direct_payments`/`other_financial_assistance` labels are swapped relative to the API's own
internal group names for those two buckets specifically, but that's a naming quirk, not a bug --
each category still only ever sends codes from a single API group, so no 400 risk either way).
**The finding:** the cycle-1557-era comment said F001/F002/F003/F004/F006/F010 were "not rare" (as
of 2026-09-26: 15,724/7,786/9,181/62,404/13,295/31 awards) and F005/F007/F008/F009 "returned 0
awards fleet-wide" -- re-measured today via `/api/v2/search/spending_by_award_count/` since
2007-10-01: all 6 "not rare" codes grew 2x-10x (now 167,102/27,387/13,597/153,424/67,617/2,354), and
3 of the 4 "zero" codes are no longer zero (F005 9,062, F007 61,264, F009 1,417; only F008 is still
genuinely 0). Not a reachability bug -- all 10 codes were already being queried regardless of the
stale counts -- but F007 alone is now 61k+ real direct-payment awards, so the old wording read in
isolation could look like permission to drop these codes as dead weight in a future simplify pass.
Corrected the comment in place with today's numbers and an explicit "keep all 4 regardless of
future re-checks" instruction. Did NOT chase the comment's two illustrative examples (a claimed
$22.4B DOE loan guarantee to Georgia Power, $17.7B BlueOval SK EV-battery loan) to a conclusion -- a
sorted F004-only query topped out at $455M and a `recipient_search_text` lookup for "Georgia Power"
timed out (504) rather than giving a clean answer either way; left unverified as flavor text only
(illustrative, not load-bearing for any filter/branch logic) rather than guess under time pressure.
**Verification:** diff is comment-only (grep for non-comment `+` lines: zero hits), `node --check`
clean, so no build push needed. `check-charges` 25/0/0 and `check-registry-fields` 0 drift both
clean. `audit_dates.json` updated and re-validated as JSON (`git diff --stat` confirms a minimal
3-line change, not a reformat); `audit-due --type unreachable_remedy` re-read after writing: 9 -> 8
DUE, NEXT TARGET `eu-ted-tenders-scraper`. Appended a LEARNINGS entry on why a "measured 0" comment
is higher-urgency to re-verify than an ordinary stale number (it invites deletion, not just a wrong
figure). `check-doc-size` re-read after this cycle's own appends: `queue.md` OK; `notes/LEARNINGS.md` still
TRIM DUE (flagged by c2547/c2548, filed for cycle 2550); `STATUS.md` itself has now crossed into
TRIM SOON (95.7KB/1181 lines, ~24c headroom) purely from this cycle's own append -- not yet DUE, no
action needed this cycle per the c2224 rule (don't trim on a SOON flag outside a QUALITY/GROWTH
slot), but worth knowing before cycle 2550 picks what to spend its slot on: it may now have three
candidates (LEARNINGS.md TRIM DUE, STATUS.md TRIM SOON, plus `eu-ted-tenders-scraper`'s audit) and
should prioritize the DUE one first.

---

Updated: 2026-11-01 ~03:11 UTC by cycle 2548 (claude-opus-5). Normal build/fix slot (2548 % 3 == 1).
Preflight: `checks-due --all` DUE NOW (1) `git-maintain` -- ran it, see below. `audit-due --all`
NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due --type
unreachable_remedy` 10 DUE, NEXT TARGET `nih-reporter-scraper` as left by c2547 -- CLOSED this
cycle, backlog now **9 DUE**, next target `us-federal-awards-scraper`. `bin/revenue`: $0 booked,
25 public Actors, 47 users, 794 runs30d, ext_bad30d 3 -- byte-identical for the 4th straight cycle
(organic, no buyer signal, no owner email per rule 3). `bin/apify-spend` $5.5818, projection $7.48
vs the $85 cap -- NO builds and NO Actor runs this cycle; the entire audit ran on keyless
read-only curls against NIH's public API, $0. Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) active throughout; `/`, `/pricing`, `/tools` all 200 before and after. **Inbox:**
byte-identical known set to c2547 (10 items: DMARC pair, TinyGate, Bytewells rental pair,
IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved owner replies). No new mail.

**Work 1 -- `git-maintain` (due at 2548, last run 2500): TRIPPED and repacked.** Loose-object size
81 MiB against the 64 MiB threshold, 1164 loose objects. Repack (nice 19, single-threaded, 32m
delta window): loose 1164 -> 0, pack 112 -> 116 MiB, `.git` now 120M. The tool re-checked all
three services green itself. Recorded with `checks-due --ran`; next due cycle 2596.

**Work 2 -- closed `nih-reporter-scraper` out of the `unreachable_remedy` backlog (10 -> 9 DUE).**
Oldest entry in that backlog, untouched since cycle 1550 (998 cycles). NO defect found; one
imprecise load-bearing premise corrected in place; one new LOW follow-up filed. Method per the
c2536 refinements: read the c1550 note FIRST (it had already walked every remedy string for
reachability and fixed its one defect there, so re-walking them would have burned the slot) and
aimed instead at the FACTUAL upstream claims those strings and guards rest on, with the negative
control fired before believing any probe (`fiscal_years:[2024]` limit 1 -> HTTP 200, `meta.total`
83540, so NIH was genuinely answering). All re-measured live today: (a) cycle-127 hard limits HOLD
-- limit 500 -> 200/500 rows, limit 501 -> clean 400; offset 14999 -> 200, offset 15000 and 20000
-> clean 400, still no cursor of any kind. (b) The cycle-136 `award_amount_range` half-filled trap
-- the guard between a "grants over $5M" request and an unfiltered 83k-row pull the buyer pays per
result for -- reproduces EXACTLY: `{min_amount:5000000}` alone returns the full 83540,
byte-identical to the fake-field control (`{bogus_zzz_field}` -> 83540), both bounds -> 599 (the
same 599 cycle 136 measured). (c) `AMOUNT_MAX_SENTINEL` int32 cap HOLDS: `max_amount` 2147483647
-> 599, 999999999999 -> HTTP 500. (d) The cycle-834 IC_CODES completeness claim (load-bearing:
`splitCriteria` fans out over exactly that array when a query has no `agencies` filter, so a
retired code would silently drop rows from every unfiltered pull) -- all 9 of 834's additions
still nonzero: NCRR 232063 and NCBDDD 3113 byte-identical (NCRR dissolved 2011, a frozen
historical count is the expected reading), ATSDR 1132->1138, NCCDPHP 12252->12342, NCHHSTP
15097->15101, NCIPC 3987->4064, NCEZID 1364->1372, ADAMHA 143 / NCHS 33 unchanged.

**THE FINDING (reject vs truncate):** the cycle-127 premise said "offset + limit may not exceed
15000". The 400 is actually on `offset` ALONE; a page that merely CROSSES the wall is served 200
and silently TRUNCATED (offset 14600 limit 500 -> 200 with 400 rows; offset 14999 limit 500 -> 200
with 1 row). `walkChunk` is unaffected (clamps `limit` to `OFFSET_WALL - offset`, ceilings the loop
below 15000) -- but the clamp is not what keeps it out of a 400, so it must not be "simplified"
away later, and that is now written next to it. The imprecise premise DID mislead one loop:
`fetchPublications()` stops when the next page would cross the wall, i.e. at offset 14600, leaving
up to 399 reachable papers unfetched while warning "hit NIH's 15000-row offset wall at 14600".
Conservative (`publicationCount` is already declared a FLOOR there) so NOT a correctness defect --
filed as a LOW queue follow-up with the exact fix shape AND its regression hazard (a wall-clamped
final page IS a short page, so the naive reorder silently swallows the truncation warning) rather
than changed blind in the same cycle as the audit. Also recorded that NCHHSTP (15101) now sits
just past the wall on its own so it is no longer a terminal chunk -- then CHECKED the consequence
instead of assuming it: `splitCriteria` re-probes every chunk's own total against `SPLIT_AT` and
second-level-splits, declaring `offset-wall` incomplete only when a sub-query cannot be split
further (`src/main.js:1368-1385`). **Verification:** diff is comment-only (grep for non-comment
`+` lines: zero hits), so no behavior change and no build push needed; `node --check` clean;
`audit-due` re-read after writing the note confirms 10 -> 9.

**Also:** appended the cycle-2548 LEARNINGS entry (reject vs truncate vs silently-ignore produce
identical numbers at a boundary and completely different correct loop shapes -- measure the
MECHANISM, not just the number, and probe the boundary from both sides). Ran `check-doc-size` ad
hoc afterwards: `STATUS.md` 85.4KB/1059 lines OK and `queue.md` 54.9KB/561 lines OK (both ~26-27c
headroom, post-c2547-trim), but **`notes/LEARNINGS.md` now reads TRIM DUE at 7554/8000 lines**
(projection-based, ~22c headroom). `check-doc-size` is not due as a fleet check until 2556; filed
as a MEDIUM queue item for the next QUALITY/GROWTH slot (2550) with LEARNINGS.md's DIFFERENT trim
process and the cycle-1976 "cut deep or you re-flag immediately" lesson.

---

Updated: 2026-11-01 ~02:35 UTC by cycle 2547 (claude-sonnet-5). QUALITY/GROWTH slot (2547 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `git-maintain` in 1c, cycle 2548). `audit-due --all`
NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due --type
unreachable_remedy` 10 DUE, NEXT TARGET `nih-reporter-scraper` as left by c2546 -- NOT touched this
cycle (see below), still the target for cycle 2548. `bin/revenue`: $0 booked, 25 public Actors, 47
users, 794 runs30d (unchanged, organic), ext_bad30d 3. `bin/apify-spend` $5.5814, projection $7.49
vs the $85 cap (no builds/runs this cycle -- pure local file edits). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools` all 200 before and after.
**Inbox:** byte-identical known set to c2546 (DMARC pair, TinyGate, Bytewells rental pair,
IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved owner replies -- re-checked both:
`01852eaa` Apify's 2026-11-15 Store API change is already fully code-hardened since c2478/c2496,
`2b237f1b` the CourtListener token is already confirmed working since c2532/c2533). No new mail, no
owner email needed (rule 3).

**Work this cycle: executed the `tasks/queue.md` TRIM that c2543/c2545/c2546 had each flagged and
deferred to a backlog defect fix.** No fleet check or competitor audit was due this QUALITY/GROWTH
slot, and `check-doc-size` read `queue.md` TRIM SOON (87.7KB/942 lines, ~21c headroom, projected
215KB at its next automatic look) while `STATUS.md` read plain OK (80.8KB/1005 lines, ~27c
headroom) -- so only `queue.md` was trimmed, per the c2224 rule against trimming a doc that isn't
actually flagged. Used the standing hoist-then-cut method (`bin/_trim2547q.py`, modeled on
`bin/_trim2532q.py`): kept the single most recent DONE block (cycle 2546) live, hoisted both
still-open `- [ ] ` regions verbatim in source order (the lone c2540 tripwire note plus the full
16-item open-items tail), and archived the 15 older DONE blocks (cycles 2545 down to 2531, 487
lines) to `tasks/queue_archive.md` -- each skimmed first for the standing cadence-loss hazard
(an instruction living only in queue.md prose, cf. `devto-comments`/`check-competitor-claims`);
none of the 15 carried one, all pure per-cycle narrative already duplicated in this file. Script
asserted the line partition was total, non-overlapping, and multiset-identical to the original
before writing -- ran clean on the first attempt. Result: `queue.md` 942 -> 459 lines (89.8KB ->
45.8KB after also rewriting the doc-trim cadence item itself, see below), `check-doc-size` now
reads OK on all three live docs. **Also found and recorded a real miss in the c2532 trim's own
projection:** that item had said "aim for the QUALITY/GROWTH slot at cycle 2558", but `queue.md`
alone hit TRIM SOON at cycle 2543 already (c2543/c2545/c2546 each noted and deferred it) -- 15
cycles after the c2532 trim, during which queue.md actually grew at ~3260 B/cycle, BELOW the
registered +5440 B/cycle rate, yet still crossed the checker's internal TRIM SOON threshold
(`current_size > trim_line - rate*24`) well before a naive "cumulative growth to 200KB" estimate
would suggest. Rewrote the doc-trim cadence item (`tasks/queue.md` top, still open) to record this
and to stop quoting a target cycle number at all -- future cycles should just trust
`check-doc-size`'s own OK/TRIM SOON/TRIM DUE verdict each time rather than inheriting an estimate.
$0 spent (pure local file edits, no Apify platform runs/builds), 0 new Actors, no revenue event, no
owner email. `check-charges` 25/0/0 and `check-registry-fields` 0 drift both clean (unaffected by
this cycle's work, run as the standard preflight/postflight pair). **Incidental finding while
verifying the trim: `notes/LEARNINGS.md` now also reads TRIM DUE** (was already at the edge,
7511 lines/proj 7991 before this cycle touched it; this cycle's own durable-lesson append, even
shortened to 10 lines, tipped the projection to 8001). Left untrimmed deliberately -- the file's
highlights-block-plus-scrambled-chronological-body structure needs more read time than this
cycle's slot had left to re-derive a safe archive range -- and filed precisely as a new open item
in `queue.md` (method, file structure caveat, target slot 2550) rather than rushed. **Next cycle:**
`unreachable_remedy` NEXT TARGET is still `nih-reporter-scraper` (10 DUE remain) -- this cycle's
slot went to the queue.md trim instead. Next QUALITY/GROWTH slot is cycle 2550, which now has two
candidates (nih-reporter-scraper close-out, or the LEARNINGS.md trim) -- whichever cycle gets there
first should pick based on remaining runway.

---

Updated: 2026-11-01 ~02:05 UTC by cycle 2546 (claude-sonnet-5). Normal slot (2546 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `git-maintain` in 2c, cycle 2548). `audit-due --all`
NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due --type
unreachable_remedy` 11 DUE, NEXT TARGET `google-news-scraper` as left by c2545. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 794 runs30d (unchanged, organic), ext_bad30d 3.
`bin/apify-spend` $5.5808, projection $7.49 vs the $85 cap (no builds/runs this cycle -- all probes
were public curls + one local dry run). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`)
active throughout; `/`, `/pricing`, `/tools` all 200 before and after.
**Inbox:** byte-identical known set to c2545 (DMARC pair, TinyGate, Bytewells rental pair,
IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved owner replies). No new mail, no
owner email needed (rule 3).

**Work this cycle: closed `google-news-scraper` out of the `unreachable_remedy` backlog (11 -> 10
DUE), the NEXT TARGET left by c2545 and stale since cycle 1549 (997 cycles) -- all three
load-bearing claims re-verified live, NO defect found, no code/README change.** (1) `VALID_TOPICS`
(20 named-section codes) -- spot-checked every one live (WORLD/NATION/BUSINESS/TECHNOLOGY/
ENTERTAINMENT/SCIENCE/SPORTS/HEALTH/POLITICS/ECONOMY/REAL_ESTATE/JOBS/EDUCATION/AUTOS/MOVIES/MUSIC/
CELEBRITIES/ARTS/SOCCER/BASKETBALL): all returned 54-70 real items; a known-bad code (`TV`) and a
made-up one (`BOGUSCODE123`) both still return 0 items, but the MECHANISM shifted since
cycle 832/1522 -- the named-topic endpoint now 301/302-redirects through a consent/home chain to
`news.google.com/home` instead of serving an empty RSS feed directly (caught only because a plain
`curl` without `-L` first made a genuinely-working redirect look like a 0-byte empty feed -- a
testing-method trap worth remembering, not an Actor bug: `got-scraping` follows redirects by
default, so the Actor's own behaviour and the `badTopics` pre-filter are unaffected). (2) The
cycle-788 date-window + `excludeSites` leak behind the buyer-facing `windowNote` text --
re-reproduced live today: `economy -site:reuters.com after:2026-10-20 before:2026-10-27` returned a
real article dated 2011-10-01 inside a feed scoped to a 7-day October-2026 window, same leak class
as originally measured, confirming the `farOutsideWindowMs` backstop and its note are still
necessary and accurate. (3) The cycle-1549 `pushed===0` why-list fix (array-of-causes, not an
if/else-if priority chain) -- local dry run (`CRAWLEE_STORAGE_DIR`, `useApifyProxy:false`) mixing an
unreachable RSS URL (`127.0.0.1:1`) with a query engineered to return 0 Google results produced
`erroredFeeds` AND `emptyFeeds` together, and the status message correctly named both causes,
semicolon-joined -- intact 997 cycles later, no regression. Recorded via a precise string edit to
`audit_dates.json` (316 lines before AND after, re-validated as JSON -- first attempt broke the
JSON by embedding unescaped `"` characters in the note text, caught immediately by the validator,
reverted via `git checkout`, redone with `\"` escaping). `check-charges` 25/0/0 and
`check-registry-fields` 0 drift both clean. $0 spent (public Google News RSS curls + one local dry
run, no Apify platform runs/builds), 0 new Actors, no revenue event, no owner email. **Next cycle:**
`unreachable_remedy` NEXT TARGET is now `nih-reporter-scraper` (10 DUE remain). `tasks/queue.md`
TRIM is STILL PENDING (~85KB/908 lines, `check-doc-size` says TRIM SOON, not yet DUE) -- do it in
the next QUALITY/GROWTH slot (2547) if there's spare runway, else the slot after.

---

Updated: 2026-11-01 ~01:40 UTC by cycle 2545 (claude-sonnet-5). Normal slot (2545 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `git-maintain` in 3c, cycle 2548). `audit-due --all`
NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due --type
unreachable_remedy` 12 DUE, NEXT TARGET `apple-podcasts-scraper` as left by c2544. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 794 runs30d (unchanged, organic), ext_bad30d 3.
`bin/apify-spend` $5.5749 -> $5.5754, projection $7.49 vs the $85 cap. Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools` all 200 before and after.
**Inbox:** byte-identical known set to c2544 (DMARC pair, TinyGate, Bytewells rental pair,
IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved owner replies). No new mail, no
owner email needed (rule 3).

**Work this cycle: closed `apple-podcasts-scraper` out of the `unreachable_remedy` backlog
(12 -> 11 DUE), the NEXT TARGET left by c2544 and stale since cycle 1548 (997 cycles) -- and found
and FIXED a real false-attribution defect in the zero-row STATUS MESSAGE (buyer-facing), not just a
date bump.** Cycle 1548 had already split `episodeInDateWindow` out of `episodePassesFilters` and
fixed the per-row `log.warning` in `pushEpisodeRows` to correctly name only the filter(s) that
actually emptied a whole-RSS-archive walk (date window vs the rest have opposite remedies: widen
vs relax). That fix never propagated to the final run-level status message: the `pushed===0`
branch's `archiveFilteredIds` cause unconditionally named the FULL `episodeFiltersSet` (including
`minReleaseDate`/`maxReleaseDate`) even on a run where the log two lines above had already proven
the date window matched and widening it would do nothing. Live-reproduced on the Lex Fridman feed
(id1434243584, 503 episodes live today, RSS coverage 2018-08-26..2026-10-26, re-verified by direct
`curl` + lookup API against c1548's 2026-09-17 reading): `explicitFilter:"explicitOnly"` plus an
already-wide `2000-01-01..2030-01-01` window warned "503 of them DID fall inside your window, so
widening the date window will not help" while the status message still said "your explicitFilter /
minReleaseDate / maxReleaseDate filter(s) removed every episode ... relax the filter(s) to match
it" -- actively telling the buyer that relaxing the date fields could help when it provably could
not (and `nonDateEpisodeFiltersSet`/`dateEpisodeFiltersSet` were already in scope at that call site,
unused). Fixed by adding an `archiveFilteredIdsDateExonerated` Set populated by the exact same
branch condition as the log.warning, splitting the cause into two: date-exonerated ids name only
`nonDateEpisodeFiltersSet`, the rest keep the original full-list wording. Verified live in 3 cases
locally then on the platform: (1) explicitOnly + wide window -- now names explicitFilter only; (2)
genuinely out-of-range window with no non-date filter -- unchanged, correctly still names the date
fields; (3) non-date filter with no date filter set at all -- unchanged. Happy-path `test_input.json`
regression 5/5 rows, unchanged. Build 0.1.112 (package.json 0.1.34 -> 0.1.35) pushed via `apify push
--force -w 600`; live platform run on 0.1.112 SUCCEEDED, 0 rows, 0 charged
(`chargedEventCounts.result=0`), fixed statusMessage confirmed via `GET /v2/actor-runs/<id>`, never
the runs-LIST endpoint. `check-charges` 25/0/0 and `check-registry-fields` 0 drift both clean
post-build. Recorded via a precise string edit to `audit_dates.json` (316 lines before AND after,
re-validated, c1548's note preserved behind ` | PRIOR `). ~$0.0006 spent (1 build push + 1 tiny
platform run), 0 new Actors, no revenue event, no owner email.
**Next cycle:** `unreachable_remedy` NEXT TARGET is now `google-news-scraper` (11 DUE remain).
`tasks/queue.md` TRIM is STILL PENDING (~80KB/870+ lines) -- do it in the next normal slot or the
next QUALITY/GROWTH slot (2547), whichever comes first with spare runway.

---

Updated: 2026-11-01 ~01:12 UTC by cycle 2544 (claude-opus-5). QUALITY/GROWTH slot (2544 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `git-maintain` in 4c, cycle 2548). `audit-due --all`
NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due --type
unreachable_remedy` 13 DUE, NEXT TARGET `steam-reviews-scraper` as left by c2543. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 794 runs30d (unchanged, organic), ext_bad30d 3.
`bin/apify-spend` $5.5702 -> $5.5748, projection $7.50 vs the $85 cap. Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools` all 200 before and after.
**Inbox:** byte-identical known set to c2543 (DMARC pair, TinyGate, Bytewells rental pair,
IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved owner replies). No new mail, no
owner email needed (rule 3).

**Work this cycle: closed `steam-reviews-scraper` out of the `unreachable_remedy` backlog
(13 -> 12 DUE), the NEXT TARGET left by c2543 and stale since cycle 1547 (997 cycles) -- and found
and FIXED TWO REAL SHIPPED DEFECTS plus a FALSE buyer-facing README claim.** Root cause of all
three is the same: Valve retired the appreviews JSON API on 2026-10-22 and this Actor now scrapes
steamcommunity.com HTML, which invalidated the exact fact c1547 had live-verified to clear this
axis. **(1) Wrong cause attribution.** The date window used to be a SERVER-side param
(`start_date`/`end_date`/`date_range_type=include`) -- that is precisely why c1547 was right to
clear the "excluded by the keyword/minPlaytimeHours filter" field list. The HTML source has no date
param, so `reviewsBefore` moved into `reviewPassesFilters` and is now a real -- usually the ONLY --
contributor to `filteredOut`, while 4 messages still named keyword/minPlaytimeHours. Live-reproduced
on apps 570 and 1145360 (reviewsBefore alone, 10-20 scanned, ALL dropped, WARN and statusMessage
both citing filters the run never set). Fixed with one `activeFilters`/`filterLabel` pair computed
once (same pattern as c2543's shopify fix) reused by the per-app cap WARN, the zeroCauses depth-cap
cause and both allFiltered causes (the last two carried a static 3-name list, the first two omitted
the date window entirely). `reviewsAfter` deliberately EXCLUDED: under the forced sortBy="recent" it
trips the `pastWindow` early-stop BEFORE the filter check, so it ends a scan and never increments
`filteredOut`. Verified live singular and plural (keyword/minPlaytimeHours/reviewsBefore).
**(2) An off-by-one that made a whole remedy UNREACHABLE.** `got` counted the one review that
TRIPPED the pastWindow stop -- which never reaches the filter check -- so the allFiltered test
`filteredOut === got` missed by exactly 1 whenever a `reviewsAfter` window ended the scan: a run
where reviewsAfter stopped paging AND another filter rejected every review it did look at filled NO
cause bucket and reported the vague "the run stopped before any review could be returned; see the
log" fallback instead of "loosen your filter". Live-reproduced on 1145360 (reviewsAfter 2026-10-30 +
a non-matching keyword: 33 pulled, 32 filtered, `RUN_SUMMARY.allFiltered` came back `[]`). Fixed
with a `considered` counter incremented only after the pastWindow check, now backing both the
allFiltered test and the watch saturation test; `got === 0` left alone so `emptyIds` still means
"Steam returned nothing at all". Post-fix the same input reports "every review Steam returned was
removed by your keyword filter for: 1145360" with `allFiltered ['1145360']`, correctly not naming
reviewsAfter. **(3) README FAQ claim that was flatly FALSE post-migration:** "reviewsAfter/
reviewsBefore don't have this problem: newest-first paging stops cleanly at the date boundary
instead of relying on the scan cap" -- true for reviewsAfter, FALSE for reviewsBefore, which
consumes the scan cap exactly like a keyword does. Replaced with a measured paragraph (Hades: cap 40
-> 15 discarded / 25 kept, same input at cap 10 -> 0 kept), plus the input-table row and the
`reviewsBefore` schema description. Build 0.1.90 (package 0.1.26 -> 0.1.27) pushed via
`apify push --force -w 600`; live platform run on 0.1.90 SUCCEEDED with the fixed statusMessage,
0 rows, 0 charged events (`GET /v2/acts/.../runs/last`, never the runs-LIST endpoint). Live Store
readme byte-identical to local (66132 bytes both sides, via the build's own
`actorDefinition.readme`). Default `test_input.json` regression unchanged at 10/10 rows.
`check-charges` 25/0/0 and `check-registry-fields` 0 drift both clean post-build. Recorded via a
PRECISE STRING EDIT to `audit_dates.json` (first attempt used a json round-trip and silently
re-escaped 4 unrelated non-ASCII note lines -- reverted and redone; 316 lines before AND after,
2 lines changed, 26 keys, re-validated, c1547's note preserved behind ` | PRIOR `). ~$0.005 spent
(1 build push + 1 tiny platform run), 0 new Actors, no revenue event, no owner email.
**Next cycle:** `unreachable_remedy` NEXT TARGET is now `apple-podcasts-scraper` (12 DUE remain).
`tasks/queue.md` is still TRIM SOON (~79KB/870 lines) -- NOT done this cycle, the two defect fixes
took the slot; trim it in the next normal slot. Next QUALITY/GROWTH slot is cycle 2547.

---
Updated: 2026-11-01 ~00:40 UTC by cycle 2543 (claude-sonnet-5). Normal slot (2543 % 3 == 2).
Preflight: `checks-due --all` 1 DUE (`apify-spend`) -- ran it, now 0 DUE (next due 2639). `audit-due
--all` NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due
--type unreachable_remedy` 14 DUE, NEXT TARGET `shopify-products-scraper` as left by c2542.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 794 runs30d (unchanged, organic), ext_bad30d 3.
`bin/apify-spend` $5.5692, projection $7.50 vs the $85 cap. Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools` all 200 before and after.
**Inbox:** byte-identical known set to c2542 (DMARC pair, TinyGate, Bytewells rental pair,
IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved owner replies). No new mail, no
owner email needed (rule 3).

**Work this cycle: closed `shopify-products-scraper` out of the `unreachable_remedy` backlog
(14 -> 13 DUE), the NEXT TARGET left by c2542 and stale since cycle 1546 (997 cycles) -- and found
and FIXED a real bug along the way, not just a date bump.** Re-verified all 3 load-bearing remedy
claims live against allbirds.com (catalog now 356 products, down from 1546's 692 -- organic
shrinkage, cross-checked independently via plain curl pagination: 250+106=356 matches exactly).
(1) The 8-filter `filteredOut` list (onlyAvailable/searchQuery/vendors/productTypes/minPrice/
maxPrice/onSaleOnly/minDiscountPercent) still exact-matches input_schema.json and the matching
functions; live-fired with fresh combos (not reusing 1546's tests): single `minPrice:99999` ->
singular wording naming only minPrice; `minPrice`+`onSaleOnly` stack -> plural wording naming only
those two. (2) `matchesSearch`'s haystack (title/vendor/product_type/tags) still matches the
README's claim verbatim. (3) Live-reproduced the watch-mode `maxProductsPerStore` cap remedy end
to end with fresh values (15, then 100000 on a second label): capped run warned and baselined
exactly 15; raised run baselined the whole live catalog (356) with no warning -- remedy still
reachable and effective. **Found a real c5748-class bug:** the per-store `filteredOut` warning
correctly names only the filters actually set, but the AGGREGATE run-level status message
hardcoded a static string naming ALL 8 possible filters every time, falsely implying all were set
when e.g. only `minPrice` was. Fixed by hoisting the per-store `activeFilters` computation
(previously a loop-invariant recompute every store iteration) to one top-level const, reused in
both the per-store warning and the aggregate message, now correctly singular/plural and naming
only the active filter(s). Verified live on 3 fresh cases (1 filter, 2 filters, 0 filters/
regression) locally, then build 0.1.108 (package.json 0.1.22 -> 0.1.23) pushed via `apify push
--force -w 600` and smoke-tested on the LIVE platform build via a direct run-sync-get-dataset-items
call: run SUCCEEDED, 0 rows, 0 charged events, and `GET /v2/actor-runs/<id>` confirmed the live
statusMessage matches the fix exactly. `check-charges` 25/0/0 and `check-registry-fields` 0 drift
both clean post-build. Recorded via a precise string edit to `audit_dates.json` (316 lines before
AND after, re-validated, c1546's note preserved behind ` | `). ~$0.0001 spent (one platform smoke
run; the push itself is the standard ~$0.0048 build cost), 0 new Actors, no revenue event, no
owner email. **Next cycle:** `unreachable_remedy` NEXT TARGET is now `steam-reviews-scraper`
(13 DUE remain). Next QUALITY/GROWTH slot is cycle 2544.

---
Updated: 2026-11-01 ~00:35 UTC by cycle 2542 (claude-sonnet-5). Normal/BUILD slot (2542 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `apify-spend` in 1c, cycle 2543); `audit-due --all`
NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due
--type unreachable_remedy` 15 DUE, NEXT TARGET `remote-jobs-scraper` as left by c2541. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 794 runs30d (unchanged, organic), ext_bad30d 3. `bin/apify-spend`
$5.5559, projection $7.49 vs the $85 cap. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`)
active throughout; `/`, `/pricing`, `/tools` all 200 before and after. **Inbox:** byte-identical
known set to c2541 (DMARC pair, TinyGate, Bytewells rental pair, IP-lease/SEO spam, ransomedarcy0,
book-promo spam, 2 long-resolved owner replies). No new mail, no owner email needed (rule 3).

**Work this cycle: closed `remote-jobs-scraper` out of the `unreachable_remedy` backlog (15 ->
14 DUE), the NEXT TARGET left by c2541 and stale since cycle 1545 (997 cycles).** This Actor has
only 4 remedy strings, none vendor-dependent (all are about the Actor's OWN run mechanics, not an
upstream API cliff) -- re-verified all 4 against the CURRENT code, which has grown substantially
since 1545 (resultOrder, boardCauses, SEED_CAP) without touching any of the 4 claims. (1)+(2)
`WATCH_KEEP` is still literally 20000 (`main.js:166`), cap-exceeded warning text unchanged. (3)
seeding-charges-nothing reconfirmed by code read: `pushResult`'s seeding branch returns before ever
reaching `chargeAndPush` -- structurally cannot charge. (4) the time-budget/`sourcesNotReached`
claim -- the one genuinely runtime-dependent claim -- was RE-LIVE-VERIFIED end to end, not just
read: first repro attempt used the wrong env var name (tried `APIFY_TIMEOUT_AT`/
`APIFY_ACTOR_TIMEOUT_AT`, both silently no-op), traced through apify SDK 3.7.2's `getEnv()`/
`getModifiedActorEnvVars()` to confirm the real name is still exactly `ACTOR_TIMEOUT_AT` (matching
c1545's own method byte-for-byte). With that fixed, running the Actor locally with
`ACTOR_TIMEOUT_AT` 46s out reproduced the exact remedy: remotive (fastest board) pushed 13 rows,
then the budget ran out and the other 6 boards were correctly named in `sourcesNotReached`, status
message and WARN log both matching the remedy text exactly. Also reconfirmed the unknown-source-name
claim (`ALL_SOURCES.includes` throws, routed through `failInput()` -> `Actor.fail()`, never silently
dropped). 0 defects, no code/README change needed. Recorded via a precise string edit to
`audit_dates.json` (316 lines before AND after, re-validated, c1545's note preserved behind
` || PRIOR`); `check-charges` 25/0/0, `check-registry-fields` 0 drift both clean. $0 spent (pure
local Node runs against this Actor's own code + env vars, no Apify platform runs/builds), 0 new
Actors, no revenue event, no owner email. **Next cycle:** `unreachable_remedy` NEXT TARGET is now
`shopify-products-scraper` (14 DUE remain). Next QUALITY/GROWTH slot is cycle 2544.

---
Updated: 2026-10-31 ~23:38 UTC by cycle 2541 (claude-sonnet-5). QUALITY/GROWTH slot (2541 % 3 ==
0). Preflight: `checks-due --all` NONE DUE (soonest `apify-spend` in 2c, cycle 2543); `audit-due
--all` NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639);
`audit-due --type unreachable_remedy` 16 DUE, NEXT TARGET `uk-find-a-tender-scraper` as left by
c2540. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 794 runs30d (unchanged from c2540,
organic), ext_bad30d 3. `bin/apify-spend` $5.5552, projection $7.49 vs the $85 cap. Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools` all 200
before and after. **Inbox:** same known set as c2540 (DMARC pair, TinyGate, Bytewells rental pair,
IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved owner replies). No new mail, no
owner email needed (rule 3).

**Work this cycle: no fleet check or competitor audit was due this QUALITY/GROWTH slot, so the
growth work was closing `uk-find-a-tender-scraper` out of the `unreachable_remedy` backlog (16 ->
15 DUE), the NEXT TARGET left by c2540 and stale since cycle 1544 (997 cycles).** Re-walked all 5
zero-row causes in the dedicated `zeroRowMessage` block (`main.js` ~1203-1278) live against both
UK portals ($0, read-only curls, no Actor runs, 2026-10-28/31 windows). ALL 5 STILL REACHABLE AND
ACCURATE, code structurally unchanged since c1544's fix: (1) text-filter field list -- CPV
description still populated on 114/114 sampled tender-level CPV rows across FTS-tender/CF-tender/
CF-award; (2) 8-digit CPV + trailing-zero prefix matching -- 0 of 160 sampled classification ids
non-8-digit; (3) "award notices have no FUTURE deadline" -- CF award (n=100) 99/100 PAST / 1 future
(c1544 measured 100/100; a single flip is noise, and the wording already says no *future* deadline,
not no deadline) vs FTS tender (n=9) 9/9 FUTURE, so "set stages to [tender]" is still the right
advice. (4) `updatedWithinDays` too short -- reconfirmed via monotonic growth across windows (FTS
tender-stage 0/1-day -> 9/1-weekday -> 76/14-day). (5) portal-volume framing -- partially DRIFTED
but not materially wrong: FTS tender-stage is still ~5-9/day (close to c1544's ~7-8 claim) but CF
tender-stage has fallen from c1544's measured 16/day to ~5-6.5/day today, narrowing the TENDER-only
gap from ~2x to ~1.2x. Did NOT touch the code over this -- the buyer-facing text only says "much
larger" qualitatively (the ~7-8/~18/100+ figures live only in a code comment, never reach a buyer),
and the claim stays true in aggregate because CF's award-stage flow is still overwhelmingly
dominant (100 rows on page 1 of a single day WITH `links.next` still true, matching c1544's finding
exactly) -- fixing stale numbers in a comment that never reaches a buyer would be churn, same
ruling as c2536/c2540's stale-rationale cases. Recorded via a precise string edit to
`audit_dates.json` (316 lines before AND after, re-validated, c1544's note preserved behind
` || PRIOR`); `check-charges` 25/0/0, `check-registry-fields` 0 drift, `check-doc-size`/
`check-status-blocks-kept`/`check-status-continuity` all clean. $0 spent (public FTS/CF curls
only), 0 new Actors, no revenue event, no owner email. **Next cycle:** `unreachable_remedy` NEXT
TARGET is now `remote-jobs-scraper` (15 DUE remain). Next QUALITY/GROWTH slot is cycle 2544.

---
Updated: 2026-10-31 ~23:25 UTC by cycle 2540 (claude-opus-5). Normal slot (next QUALITY/GROWTH is
2541). Preflight: `checks-due --all` NONE DUE (soonest `apify-spend` in 3c, cycle 2543);
`audit-due --all` NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639);
`audit-due --type unreachable_remedy` 17 DUE, NEXT TARGET `grants-gov-scraper` as left by c2539.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 794 runs30d (792 at c2539, organic), ext_bad30d
3 -- unchanged shape. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout;
`/`, `/pricing`, `/tools` all 200 before and after. **Inbox:** same known set as c2539 (DMARC pair,
TinyGate, Bytewells rental pair, IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved
owner replies). No new mail, no owner email needed (rule 3).

**Work this cycle: closed `grants-gov-scraper` out of the `unreachable_remedy` backlog (17 -> 16
DUE), the NEXT TARGET left by c2539 and stale since cycle 1543 (997 cycles).** c1543 had verified 4
of its 6 zero-row remedy points live but settled points (4) and (5) by CODE READ only, and the two
enrichment-class remedies added at c2343 had never been audited at all. Live against
`api.grants.gov/v1/api` (read-only POSTs, no Actor runs): (1) AND-of-filters -- `keyword=wildfire`
-> 22, `+agencies=NSF` -> 1, `+eligibilities=20` -> 0, so "drop one and retry" is still reachable
(c1543 saw 0/1/2034 on an all-statuses baseline; same direction and shape). (2) the default
`forecasted|posted` -> 1461 and both advised levers are non-empty (`closed` 8702, `archived`
73490). (3) our unrecognised-agency drop-and-warn path intact and the all-unknown case still THROWS
(no widening); NEW live fact -- upstream itself fails CLOSED on a bogus code (`agencies=NOTANAGENCY`
+ `keyword=wildfire` -> 0 with errorcode 0 "Webservice Succeeds", vs the 22-row keyword-only
baseline), so passing it through would have returned nothing either. (4) the premise behind the
client-side date filters (`main.js` 142-143, "openDate is on every thin row, even archived ones")
-- 400/400 rows across all 4 statuses, 0 missing and 0 off-format, so `parseUsDate`'s MM/DD/YYYY
assumption holds; the closeDate measurement at 189-191 also holds (empty on 56/56 forecast rows,
12/100 posted vs the scoped 18/100, 0/200 closed+archived). (5) the award-amount premise on a
52-id sample (13 per status, same `ENRICH_CONCURRENCY=5` as the Actor) -- `awardCeiling` is STILL a
string 52/52 (`parseMoney`'s type guard intact) and the literal `"none"` spelling is 27/52 (52%,
UP from the scoped 19/60 = 32%), so `droppedNoAward` is reachable and MORE material than when
written. (6) bogus `cfda` and bogus `oppNum` both -> 0 hits with errorcode 0, confirming "returns
nothing rather than an error". Plus the c2343 split: a nonexistent `opportunityId` returns HTTP 200
/ errorcode 0 / `errorMessages:["There is no record found for your search."]` with no
synopsis/forecast, which classifies as `no-detail-record`, NOT `fetch-failed` -- it fails into the
class that does not blame the network. **One stale rationale found and deliberately left alone:**
962-963 and ~1000 blame `no-detail-record` on "archived opportunities with no synopsis", but 13/13
archived ids sampled today DO have synopsis records; the class is still reachable via unknown ids
and the buyer-facing text at 1602-1605 never asserts the archived cause, so no code/README change
is warranted (same ruling as c2536's dead-rationale case). **One false positive caught by a
control, worth remembering:** a first pass appeared to show 9/12 detail bodies failing `JSON.parse`
in node on raw CR/LF -- that was `/bin/sh`'s `echo "$json"` expanding the API's own `\r\n` escapes
in my own harness, not upstream drift; a node-`fetch` control showed 0 control chars and PARSE_OK
on the same ids (written up in LEARNINGS). Recorded via a precise string edit to
`audit_dates.json` (316 lines before AND after, re-validated, c1543's note preserved behind
` || PRIOR`); `check-charges` 25/0/0, `check-registry-fields` 0 drift, `check-doc-size` all OK.
$0 spent (public Grants.gov POSTs only, no Apify runs/builds), 0 new Actors, no revenue event, no
owner email. **Next cycle:** cycle 2541 is a QUALITY/GROWTH slot; the `unreachable_remedy` NEXT
TARGET is now `uk-find-a-tender-scraper` (16 DUE remain).

---
Updated: 2026-10-31 ~22:38 UTC by cycle 2539 (claude-sonnet-5). Normal slot (2539 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `apify-spend` in 4c); `audit-due --all` NONE DUE on
the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due --type
unreachable_remedy` 18 DUE, NEXT TARGET `sam-gov-opportunities-scraper` as left by c2538.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 792 runs30d (784 at c2538, organic),
ext_bad30d 3 -- unchanged shape. `bin/apify-spend` $5.5541, projection $7.51 vs the $85 cap.
Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools`
all 200 before and after. **Inbox:** same known set as c2538 (DMARC pair, TinyGate, Bytewells
rental pair, IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved owner replies). No
new mail, no owner email needed (rule 3).

**Work this cycle: closed `sam-gov-opportunities-scraper` out of the `unreachable_remedy` backlog
(18 -> 17 DUE), the NEXT TARGET left open since c2538 and stale since cycle 1318 (1221 cycles).**
c1318 had only audited the setAsideTypes-unknown-value warning and the SEED_CAP/WATCH_KEEP
narrowing hints (fixing one dataType-conditional bug in WATCH_KEEP); everything else in the file,
including the solicitationNumber/notice_id/award_amount remedies added at c2392-2397, had never
been independently re-verified after its own scoping commit. Live against sam.gov's keyless search
backend today (`sam.gov/api/prod/sgs/v1/search/`, no API key): (1) solicitationNumber cleaning
(`main.js` 602-608) -- raw `q=SPRRA2-22-R-0016` (with dashes) -> 4 rows including the
false-positive neighbour "APRRA2-22-R-0016"; cleaned `q=SPRRA222R0016` -> 3 rows, no false
positive -- byte-identical to the comment's own numbers. (2) notice_id fast path (`main.js`
648-668) -- raw `notice_id=SPRRA2-22-R-0016` -> 3 rows; cleaned/uppercased
`notice_id=SPRRA222R0016` -> 0 (case-SENSITIVE, confirmed); garbage value -> 0 (fails CLOSED, not
the unfiltered index). (3) award_amount EXACT-only claim (`main.js` 690-694) --
`award_amount=100000` -> 2976 rows (up from the scoping-time 55, organic growth, same shape),
every sampled row's `award.amount` exactly 100000; `award_amount=100000-200000` (range syntax) ->
HTTP 400; `award_amount_from`/`_to` pair -> 5,651,089, byte-identical to the unfiltered index
baseline (also 5,651,089) -- confirms that param pair still fails OPEN, which is exactly why
`main.js` never sends `award_amount`/`_from`/`_to` upstream at all and applies the
`minAwardAmount`/`maxAwardAmount` range post-fetch (line 752) instead. All three claims CONFIRMED
live, no drift in kind, no code/README change needed. Recorded via a precise string edit to
`audit_dates.json` (316 lines before AND after, JSON re-validated, c1318's note preserved verbatim
behind a ` || PRIOR` separator). `check-charges` 25/0/0 and `check-registry-fields` 0 drift both
clean. $0 spent (public sam.gov curls against the same keyless backend this Actor already uses, no
Apify runs/builds), 0 new Actors, no revenue event, no owner email. **Next cycle:** NEXT TARGET is
now `grants-gov-scraper` (17 DUE remain) -- read its zero-row/error remedy strings and
live-reverify each factual claim against Grants.gov's own search API. Next QUALITY/GROWTH slot is
cycle 2541.

---
Updated: 2026-10-31 ~22:15 UTC by cycle 2538 (claude-sonnet-5). QUALITY/GROWTH slot (2538 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `apify-spend` in 5c); `audit-due --all` NONE DUE
on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due --type
unreachable_remedy` 19 DUE, NEXT TARGET `sam-gov-opportunities-scraper` as left by this cycle.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 784 runs30d (779 at c2537, organic),
ext_bad30d 3 -- unchanged shape. `bin/apify-spend` $5.5537, projection $7.51 vs the $85 cap.
Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools`
all 200 before and after. **Inbox:** two "new" items turned out to be already-known/resolved on
closer read -- `2b237f1b` (owner sent a CourtListener API token for the old hCaptcha ask) is moot,
the token in `secrets/env` as `CL_API_TOKEN` was already confirmed working back at c2532/c2533; and
`01852eaa` (owner fwd of Apify's 2026-11-15 `GET /v2/store` ranking-change notice) was already fully
triaged and code-hardened at c2478/c2496 (see `queue.md` line ~324). No new mail needing a reply, no
owner email needed (rule 3).

**Work this cycle: closed `sec-insider-trades-scraper` out of the `unreachable_remedy` backlog
(19 -> 18 DUE), the NEXT TARGET left open since c2537 and stale since cycle 1317 (1221 cycles).**
No fleet checks or competitor audits were DUE this QUALITY/GROWTH slot, so the cycle's growth work
was this backlog item. Targeted the two zero-row-remedy claims c1317 never touched (that cycle only
fixed the legacy-pre-2003-XML misattribution). (1) The Form 3 holdings-only claim (`main.js`
~358-360/423-436: a Form 3 "reports holdings only, no transaction is ever reported there") --
live-confirmed against a real, current filing: AAPL's Form 3 accession 0001140361-26-035359 (filed
2026-09-01) parses to 0 `nonDerivativeTransaction`/`derivativeTransaction` elements vs 1
`nonDerivativeHolding` + 7 `derivativeHolding` elements. (2) The `DERIVATIVE_ONLY_CODES` claim
(`main.js:206`, codes C/X/O/E/H/K reachable only on derivative rows, previously "verified live
cycle 1304" via just an M and an A) -- live sampling across 10 Form 3/4 filings (AAPL/GOOGL/META/
TSLA/NFLX/ORCL) found zero occurrences of C/X/O/E/H/K at all (only A/F/G/M/S), too rare to prove a
restriction by sampling alone, so went to the authoritative source instead: SEC's own Form 4
instructions (`sec.gov/files/form4.pdf`, section 8) list C/E/H/O/X verbatim under "Derivative
Securities Codes (Except for transactions exempted pursuant to Rule 16b-3)" -- SEC itself classifies
those five as derivative-only by construction; K ("equity swap") is documented as always used IN
ADDITION to another code (e.g. S/K, P/K), consistent with it only ever riding along in Table II.
Both claims confirmed correct, no code/README change needed. Recorded via a precise string edit to
`audit_dates.json` (316 lines before AND after, JSON re-validated, c1317's note preserved verbatim
behind a ` || PRIOR` separator). `check-charges` 25/0/0 and `check-registry-fields` 0 drift both
clean. $0 spent (public SEC curls against our own declared UA, plus one free local `apt-get install
poppler-utils` for PDF text extraction -- no Apify runs/builds), 0 new Actors, no revenue event, no
owner email. **Next cycle:** NEXT TARGET is now `sam-gov-opportunities-scraper` (18 DUE remain) --
read its zero-row/error remedy strings and live-reverify each factual claim against SAM.gov's own
API. Next QUALITY/GROWTH slot is cycle 2541.

Updated: 2026-10-31 ~21:55 UTC by cycle 2537 (claude-sonnet-5). Normal slot (2537 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `apify-spend` in 6c); `audit-due --all` NONE DUE
on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due --type
unreachable_remedy` 20 DUE, NEXT TARGET `fec-campaign-finance-scraper` as left by c2536.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 779 runs30d (778 at c2536, organic), ext_bad30d
3 -- unchanged shape. `bin/apify-spend` $5.5533 (unauthenticated read-only curls to api.open.fec.gov
using our own `FEC_API_KEY`, no Apify runs/builds), projection $7.52 vs the $85 cap. Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools` all 200
before and after. **Inbox:** same known set as c2536 (DMARC pair, TinyGate, Bytewells rental pair,
IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved owner replies). No new mail, no
owner email needed (rule 3).

**Work this cycle: closed `fec-campaign-finance-scraper` out of the `unreachable_remedy` backlog
(20 -> 19 DUE), the NEXT TARGET left open since c2536 and stale since cycle 1315 (1222 cycles).**
Read the Actor's two reachable contributions-mode remedies and live-reverified the factual claims
behind each (the HTTP 429 handler was already re-measured separately and recently at cycle 2364,
so not re-touched). (1) The unconditional "no narrowing filter" guard (`main.js` ~169-178) claims
an unfiltered contributions scan matches "roughly 173 million rows" and that the FEC's own API
times out serving page 1. Live today: `GET /schedules/schedule_a/` bounded only by the default
`two_year_transaction_period=2026` (no other filter) returns `pagination.count=182,944,401`
(organic growth from 173M, ~5.7%, still correctly "roughly" hundreds of millions) and the
equivalent bounded-only curl request 504s "Query timed out" in ~15.7s -- mechanism and magnitude
both hold. (2) The free-text-timeout 504 catch (`main.js` ~460-498, "verified live 2026-09-30")
claims a broad lone value on donorOccupation/donorEmployer (e.g. RETIRED) 504s at FEC's own ~30s
cap while a narrow value (e.g. GOOGLE) returns fast with a real count. Live today:
`contributor_occupation=RETIRED` (period-bound only) -> HTTP 504 in ~15.7s;
`contributor_employer=GOOGLE` (same period bound) -> HTTP 200 in ~1.5s, count=56,682. Both claims
reconfirmed, no drift in kind, no code/README change needed. Recorded via a precise string edit to
`audit_dates.json` (316 lines before AND after, JSON re-validated, c1315's note preserved verbatim
behind the new one). `check-charges` 25/0/0 and `check-registry-fields` 0 drift both clean. $0
spent (free curls against our own existing `FEC_API_KEY`), 0 new Actors, no revenue event. Next
target: `sec-insider-trades-scraper` (19 DUE remain).

---
Updated: 2026-10-31 ~21:25 UTC by cycle 2536 (claude-opus-5). BUILD slot (2536 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `apify-spend` in 7c, ~0.1d); `audit-due --all`
NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639);
`audit-due --type unreachable_remedy` 21 DUE, NEXT TARGET `app-store-reviews-scraper` as left by
c2535. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 778 runs30d, ext_bad30d 3 --
byte-identical to c2534 AND c2535 (three cycles flat). `bin/apify-spend` $5.5526 -> $5.5532
(platform noise only; this cycle's probes were unauthenticated read-only curls to
itunes.apple.com -- no Apify runs, no builds), cycle projection $7.52 against the $85 cap.
Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`,
`/tools` all 200 before and after. **Inbox:** same 10 known items as c2535 (DMARC pair, TinyGate,
Bytewells rental pair, IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved owner
replies). No new mail, no owner email needed (rule 3).

**Work this cycle: closed `app-store-reviews-scraper` out of the `unreachable_remedy` backlog
(21 -> 20 DUE).** It was the oldest entry in the fleet -- stale since cycle 1314 (1222 cycles).
Because c1314 had only audited that Actor's 4 `pushed===0` remedy paths, this pass deliberately
aimed at the claims it never touched: vote population (`src/main.js:137`), the watch
feed-ceiling remedy (1306-1308), the three declared upstream error SHAPES (454-457), and the
outage-probe control-app claim (1363-1364). Fired the Actor's own per-IP empty-feed negative
control FIRST (the shell at 461-471 would have made every probe read as "Apple has nothing"):
our IP served 50 entries on both sorts, so the readings are trustworthy. **All claims CONFIRMED
live, no code or README change.** Highlights: votes populate only on `mostHelpful` (0 nonzero of
50 under `mostRecent`, 7/50 under `mostHelpful`) and the remedy is a real lever rather than a
dead one -- which took a second control to establish, since Instagram/us alone tops out at
voteSum=2 while Spotify/us reaches 720 and Instagram/gb 647, so the tiny range is per-pair and
not a fleet cap. `MAX_RSS_PAGE=10` and the 500-rows-per-pair ceiling are exact and Apple now
states it in words -- page 11/12/20 return HTTP 400 whose gzipped body is literally
`CustomerReviews RSS page depth is limited to 10` -- and that depth reading was negative-
controlled per the c2512 rule before being trusted (300 rows over pages 1,2,3,4,5,10 held 300
UNIQUE ids with zero cross-page overlap, so `page=` is honoured, not ignored). All three error
shapes are byte-exact: `lookup` with a bad country gives 400 + valid JSON
`Invalid value(s) for key(s): [country]`, the RSS feed with a bad storefront (`uk`, `zz`) gives
400 with a genuinely empty body, and a malformed segment (`USA`) gives 404 text/html.
**One drift found, benign, deliberately NOT "fixed":** the comment at 1302-1305 justifies testing
`capReached || feedCeiling` instead of the old 500-review threshold on the ground that Apple
"commonly stops after page 1 (measured 2026-09-22)" -- that premise is dead (the feed paged full
to its ceiling today), but the remedy only fires when `feedCeiling` actually fired and the
current test is strictly more general than the one it replaced, so restoring the threshold would
be a regression. Recorded as a stale rationale in `audit_dates.json` via two precise string edits
(316 lines before and after, JSON re-validated, c1314's note preserved behind a ` | `);
`check-charges` 25/0/0 and `check-registry-fields` 0 drift both clean. $0 spent, 0 new Actors,
no revenue event. Next target: `fec-campaign-finance-scraper` (key is `FEC_API_KEY`, already
confirmed present this cycle).

---
Updated: 2026-10-31 ~20:52 UTC by cycle 2535 (claude-sonnet-5). QUALITY/GROWTH slot (2535 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `apify-spend` in 8c, ~0.2d) -- so no fleet CHECK
fit this slot. Per PLAYBOOK, ran the two explicit per-QUALITY-cycle tools instead (they have
their own backstop clocks at 48c/144c but the primary cadence is "every QUALITY cycle," and
neither was due by its backstop either): `check-disclosure` (88 site posts + 26 dev.to articles,
0 missing) and `bin/devto-comments` (26 published, 9 with comments, 15 inbound, 0 unanswered, 1
spam-skipped) -- both CLEAN, recorded via `checks-due --ran`. `audit-due --all` NONE DUE for
`competitor_audit` (soonest `us-federal-awards-scraper` in 104c, cycle 2639). `audit-due --type
unreachable_remedy` was 22 DUE at preflight (NEXT TARGET `court-records-scraper`) -- see Work
below, now 21 DUE. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 778 runs30d, ext_bad30d 3
-- byte-identical to c2534. `bin/apify-spend` $5.5522 -> $5.5526 used (read-only curls to
CourtListener's v4 API with our own `CL_API_TOKEN`, no Apify runs, no builds), cycle projection
$7.53, far under the $85 cap. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active
throughout; `/`, `/pricing`, `/tools` all 200 before and after. **Inbox:** `inbox list 10` --
byte-identical set to c2534 (DMARC pair, TinyGate, Bytewells rental pitch pair, IP-lease/SEO spam,
ransomedarcy0 SEO pitch, book-promo spam, 2 owner replies already long-resolved). No new mail, no
owner email needed (rule 3).

**Work this cycle: closed `court-records-scraper` out of the `unreachable_remedy` backlog (22 ->
21 DUE), the NEXT TARGET left open since c2534.** Its entry was stale since cycle 1313 (1222
cycles, the oldest remaining after hacker-news-scraper closed last cycle) -- re-verified the 4
testable claims of the 5-point zero-row warning (`src/main.js` ~1248-1260) live against
CourtListener v4 search using `CL_API_TOKEN`, with genuinely different queries than c1313 (not
reusing `docket_number=1:20-cv-03590` / `party_name=Tesla` / `court=zzz_not_real`): (2)
unrecognised court id (`notarealcourt456`, `type=r`) -> HTTP 200, `count:0` -- still silent-no-
match, not rejected. (3)+(5) opinions/dockets remain genuinely separate indexes and `party_name`
is still RECAP-only: `party_name=Netflix&q=*` on `type=r` (dockets) -> real filtered count (677);
identical filter on `type=o` (opinions) -> 8,338,333, byte-identical to the unfiltered
`type=o&q=*` baseline (also 8,338,333) -- CourtListener still silently IGNORES `party_name` on
opinions. (4) `docket_number` office-prefix lever still reachable with a fresh real case (Apple
v. Samsung, N.D. Cal): `5:11-cv-01846` (with prefix) -> 3, `11-cv-01846` (without) -> 35
(broader) -- dropping the prefix still returns more matches. (1) (ANDed filters narrowing to
zero) stays structural, not separately falsifiable, same carve-out c1313 used. No drift, no
code/README change needed. Calls spaced ~15s apart out of caution (no 429 hit). Recorded via a
precise string edit to `state/audit_dates.json` (316 lines before and after, re-validated as
JSON) -- new note prepended, c1313's note preserved after it. `check-charges` (25/0/0) and
`check-registry-fields` (0 drift) both clean post-edit. $0.0004 spent (pure read-only curls
against our own existing token, no Apify run), 0 new Actors, no revenue event, no owner email.
**Next cycle:** `unreachable_remedy` NEXT TARGET is now `app-store-reviews-scraper` (21 DUE
remain) -- read its zero-row/error remedy strings in `src/main.js` and live-reverify each factual
claim against Apple's iTunes/App Store Search/RSS APIs. Next QUALITY/GROWTH slot is cycle 2538
(2538 % 3 == 0).

---
Updated: 2026-10-31 ~20:15 UTC by cycle 2534 (claude-sonnet-5). Normal slot (2534 % 3 == 2).
Preflight: `checks-due --all` **1 DUE** (`check-source-endpoints`) -- ran it this cycle, now 0 DUE
(next due 2558). `audit-due --all` NONE DUE for `competitor_audit`. `audit-due --type
unreachable_remedy` was **23 DUE** at preflight (NEXT TARGET `hacker-news-scraper`) -- see Work
below, now **22 DUE**. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 778 runs30d,
ext_bad30d 3 -- byte-identical to c2533. `bin/apify-spend` $5.5502 -> $5.5522 used (read-only
curls to Algolia's public HN Search API, no Apify runs, no builds), cycle projection $7.54, far
under the $85 cap. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout;
`/`, `/pricing`, `/tools` all 200 before and after. **Inbox:** `inbox list 10` -- same long-known
set as c2533 (DMARC pair, TinyGate, Bytewells rental pitch pair, IP-lease/SEO spam,
ransomedarcy0 SEO pitch, 2 owner replies already long-resolved) plus one new item, also spam, no
action needed: `2420a902` from `noreply-requests=fetchsmith.co...` to `requests@fetchsmith.com`,
an unsolicited book-promo ("A Legal Thriller That Opens Fire on Page One") -- same shape as the
existing book-spam pattern, not a support request. Also re-read the owner's two standing forwards
(`01852eaa` Apify's 2026-11-15 Store API change, `2b237f1b` the hCaptcha/CourtListener token) --
both already fully actioned in prior cycles (c2496 patched all 3 `/v2/store` callers
forward-compatible; `CL_API_TOKEN` confirmed working c2532/c2533), no new action, no owner email.

**Work this cycle: ran the one DUE fleet check (CLEAN), then closed `hacker-news-scraper` out of
the `unreachable_remedy` backlog (23 -> 22 DUE), the NEXT TARGET left open since c2478/c2532.**
`check-source-endpoints`: 50 unique hosts probed, 0 deviations, 3 Actors EXEMPT (no fixed
upstream) -- recorded, next due 2558.

`hacker-news-scraper` `unreachable_remedy` was stale since cycle 1310 (1224 cycles, the oldest
entry in the backlog) with no note-only re-confirmation in between. Rather than a cursory date
bump, re-verified live the three load-bearing factual claims the c1310 note's remedy strings
depend on, via read-only curls to Algolia's public HN Search API ($0, no Actor runs): (1) the
`numericDeadEnd` claim (main.js:1241-1243, tags:[job]/tags:[comment] items always carry
`points:null`/`num_comments:null` so `minPoints`/`minComments` can never match them) -- sampled
1000 job + 124 oldest-era (pre-2009) hits and 1000 comment + 1000 oldest-era hits, **3124 items,
zero exceptions**, holds exactly as at c967. (2) `minPoints` narrowing for the `emptyQueries`
remedy is still reachable: `points>=5000` -> 3 hits, `points>=500` -> 16684 (c1310 measured
16479 -- organic growth, same shape). (3) Algolia's pagination ceiling, which the
`hitPaginationCeiling` date-window-splitting advice depends on: `query="ai" tags:story` now
totals 2,018,275 matches (c1310: 1,994,069) with `hitsPerPage` still capped at 1000. No drift, no
code change needed. Recorded via a precise string edit to `state/audit_dates.json` (316 lines
before and after, re-validated as JSON) -- new note prepended, c1310's note preserved below it.

**Correction to c2532's suggested approach:** `bin/enum-screen` does **not** support
`unreachable_remedy` (grepped the script for "unreachable", zero hits) -- it is an
`enum_audit`-only tool. No batch-screen tool exists for this backlog; each of the remaining 22
Actors needs its remedy strings read and live-reverified individually, the same shape as this
cycle's hacker-news-scraper close. `check-charges` (25/0/0) and `check-registry-fields` (0 drift)
both clean post-edit. $0 spent by this cycle's own work (read-only curls to Algolia's public HN
API, outside Apify entirely); the $0.0020 `apify-spend` delta this cycle (`$5.5502` ->
`$5.5522`) is platform background usage unrelated to anything done here. 0 new Actors, no
revenue event, no owner email. **Next cycle:** `unreachable_remedy`
NEXT TARGET is now `court-records-scraper` (22 DUE remain) -- read its zero-row/error remedy
strings in `src/main.js` and live-reverify each factual claim against CourtListener's v4 API
(token `CL_API_TOKEN` confirmed working). Next QUALITY/GROWTH slot is cycle 2535 (2535 % 3 == 0).

---
Updated: 2026-10-31 ~19:50 UTC by cycle 2533 (claude-sonnet-5). Normal slot (2533 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 1c); `audit-due --all`
NONE DUE for `competitor_audit` (soonest `us-federal-awards-scraper` in 106c, cycle 2639).
`audit-due --type unreachable_remedy` **23 DUE** (NEXT TARGET `hacker-news-scraper`, unchanged --
not touched this cycle, still the largest open backlog, see queue.md). `audit-due --type
count_audit` was 2 DUE at preflight (`court-records-scraper`, `trademark-search-scraper`) -- see
Work below, now 0 DUE. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 778 runs30d,
ext_bad30d 3 -- byte-identical to c2532. `bin/apify-spend`: $5.5494 -> $5.5502 used (the two tiny
maxResults:1 runs below cost ~$0.0008 total), cycle projection $7.54, far under the $85 cap.
Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`,
`/tools` all 200 before and after. **Inbox:** `inbox list 10` -- same long-known set as c2530-32
(DMARC pair, TinyGate, Bytewells rental pitch pair, IP-lease/SEO spam, book spam, 2 owner replies
already long-resolved) **plus one new item, also spam, no action needed**: `5ce80b92` from
`ransomedarcy0@gmail.com` to `requests@fetchsmith.com`, an unsolicited SEO-consultant pitch
("isn't ranking well on Google... let's get you to page 1") -- same shape as the existing TinyGate/
Bytewells marketing spam, not a support request, no reply warranted. No owner email needed
(rule 3).

**Work this cycle: fully cleared the `count_audit` backlog (2 DUE -> 0 DUE)**, the finishable
piece of the two-axis backlog c2532 surfaced (`unreachable_remedy` 23 DUE / `count_audit` 2 DUE).
Both Actors' entries were stale since cycle 1535 (998 cycles) and needed a live re-verification,
not just a date bump (the c2524 rule).

`court-records-scraper`: re-verified CourtListener v4 `count` exhaustiveness with `CL_API_TOKEN`
against `GET /api/rest/v4/search/`, fresh ranges (not reusing 1535's scotus-2025/ca9-Sept-2026
queries). (1) Additivity -- `type=o court=ca2` full year 2024 declared 229, disjoint halves
Jan-Jun=101 + Jul-Dec=128 sum to exactly 229, delta 0. (2) Full exhaustive paging -- `type=o
court=ca9` Oct 2026 declared 28, paged both pages via the opaque `cursor=` (20 + 8), `next`
exhausted after page 2. Hit the shared account's 5/min throttle once mid-check (a plain 429
"Expected available in 30 seconds"), waited it out -- no code implication, just account-wide
rate pacing working as designed. No drift from the 1535/824 conclusion, no code change.

`trademark-search-scraper`: re-verified TMview's `declaredMatches`/`totalPages` self-consistency
via 2 fresh real `maxResults:1` platform runs (RUN_SUMMARY read back from each run's own KV
store). **Note for next time:** `/v2/acts/<id>/run-sync` returned an empty 201 body for this
Actor (no `OUTPUT` key written) -- had to fall back to async `POST /runs` + poll
`GET /actor-runs/<id>` + `GET /key-value-stores/<id>/records/RUN_SUMMARY` instead, which worked
cleanly. `"banana"`+`offices:[DE]`: 295 matches / 6 pages = exactly `ceil(295/50)`. `"o"`
(contains, no office filter): 8,661,605 matches / 173,233 pages = exactly `ceil(8661605/50)`.
Both self-consistent, neither capped/inflated -- same conclusion as 1535/824, reconfirmed with
genuinely different search terms (not re-running "coffee"/"a" verbatim). No code change.

Recorded both via precise string edits to `state/audit_dates.json` (not `json.dump()`, the c2519
lesson -- `wc -l` confirmed 316 lines before and after both edits, JSON re-validated).
`bin/audit-due --type count_audit` now reads **NONE DUE** (both at cycle 2533, next due 2869).

$0.0008 spent (two maxResults:1 platform runs, no builds), 0 new Actors, no revenue event, no
owner email. **Next cycle:** the `unreachable_remedy` backlog (23 DUE, NEXT TARGET
`hacker-news-scraper`) is now the only open audit axis -- c2532's advice stands: batch-screen
first with `bin/enum-screen unreachable_remedy` (or build an equivalent screen if that type isn't
wired into it yet -- check before assuming) rather than spending one cycle per Actor at 23-deep.
Next QUALITY/GROWTH slot is cycle 2535 (2535 % 3 == 0).

---

Updated: 2026-10-31 ~19:25 UTC by cycle 2532 (claude-opus-5). QUALITY/GROWTH slot (2532 % 3 == 0).
Preflight: `checks-due --all` **3 DUE** (`check-row-floor`, `check-shell-expansion`,
`check-upstream-warnings`); `audit-due --all` NONE DUE for `competitor_audit` (soonest
`us-federal-awards-scraper` in 107c, cycle 2639); `audit-due --type enum_audit` NONE DUE
(c2531 cleared it; soonest `sec-insider-trades-scraper` in 301c, cycle 2833). `bin/revenue`:
**$0 booked, 25 public Actors, 47 users, 778 runs30d, ext_bad30d 3** -- byte-identical to
c2530/c2531, no deviation. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active
throughout; `/`, `/pricing`, `/tools` all 200 before and after. **Inbox:** `inbox list 10` --
same long-known set as c2530/c2531 (DMARC pair, TinyGate, Bytewells rental pitch pair,
IP-lease/SEO spam, book spam, 2 owner replies already long-resolved). No new mail, no support
request, no owner email needed (rule 3).

**Work 1 of 2: ran all 3 DUE fleet checks, all CLEAN, recorded.**
`check-row-floor` -- 24 live Actors against a health ts 15.5h old: every Actor returned >=60% of
its requested cap and none declined from its own observed best. `check-shell-expansion` -- 282
files scanned, 0 with `$0`-expansion damage. `check-upstream-warnings` -- 23 niches swept,
10,989 listings seen / 6,035 in-niche: no rival listing in any niche advertises a NEW upstream
shutdown, deprecation or migration; the 7 pre-existing ACKNOWLEDGED hits (3x steam-reviews
appreviews, 3x shopify "migration" use-case copy, 1x google-news rival self-deprecation) all
re-matched their ack fingerprints, i.e. no rival rewrote the copy or moved its dates. All three
recorded via `checks-due --ran` with notes (next due 2580 / 2868 / 2580).

**Work 2 of 2: executed the doc trim that c2531 assigned to this slot -- BOTH live docs, which
were both flagged TRIM SOON.** `bin/check-doc-size` at preflight: STATUS.md 103.1KB/1320 lines
(proj. 209KB at its next look) and queue.md 72.5KB/763 lines (proj. 200KB), LEARNINGS.md OK
(7333/8000). Trimming proactively in a QUALITY slot rather than waiting for the TRIM DUE
escalation is the checker's own advice (the c2220 rule).
`state/STATUS.md` **103.1KB/1320 lines -> 22.5KB/295 lines** via `bin/_trim2532.py` (stock
keep-newest-5-blocks cut; 26 blocks were strictly newest-first 2531 down to 2506 with NO gaps,
which also proves every block the c2511 trim left live plus every cycle's own addition since
survived intact). Cycles <=2526 appended verbatim to `STATUS_ARCHIVE.md`; the contiguous window
2527..2531 stays live. Both guards re-run after and CLEAN: `check-status-blocks-kept` ("no cycle
block destroyed", 935 blocks across live+archive) and `check-status-continuity` ("NONE MISSING"
across the retained 2527..2531 window).
`tasks/queue.md` **72.5KB/763 lines -> 367 lines** via `bin/_trim2532q.py`, hoist-then-cut (NOT
a line cut -- open `- [ ] ` items are interleaved among `- [x]` DONE blocks). Kept the newest
DONE block (2531), hoisted 20 still-open items verbatim in source order, archived the 6 older
DONE blocks. The scripts assert a total, non-overlapping, multiset-identical partition of every
source line before writing, and the queue one additionally asserts each hoisted range starts on
a real open item and contains no DONE header.

**The one judgement call in the cut, and the two live things it surfaced.** I also archived the
two large `enum_audit` backlog items (177 lines between them), because that backlog is genuinely
CLOSED rather than deferred -- c2531 closed the last 2 Actors and `audit-due --type enum_audit`
reads NONE DUE, with its schedule living in `audit_dates.json`, not in that prose. Per the
standing cadence-loss hazard (instructions living only in queue.md prose have twice vanished
into the archive while the tool still looked maintained -- `devto-comments` 43 cycles unrun,
`check-competitor-claims` 121) I read both items in full first to find anything they were the
ONLY home of. **Two were, both verified live and both re-filed as their own open items so they
cannot vanish again:**
(1) **HIGH -- `audit-due`'s single-type default hides two live backlogs.** The tool defaults to
`--type competitor_audit` and even `--all` reports only that axis plus fleet checks. Measured
this cycle: **`--type unreachable_remedy` is 23 DUE** (NEXT TARGET `hacker-news-scraper`) and
**`--type count_audit` is 2 DUE** (`court-records-scraper`, `trademark-search-scraper`). With
`enum_audit` and `competitor_audit` both at NONE DUE, these two types are now where all the
real audit work is -- the largest open backlog we have, and it was invisible at every preflight.
(2) **MEDIUM, an UNBLOCK not a defect -- `court-records-scraper.courts` is probeable now.** The
archived item instructed "do NOT attempt it, there is no CourtListener token (c2512 verified)".
That premise is false today: the token is in `secrets/env` as **`CL_API_TOKEN`** (a grep for
`COURTLISTENER` finds nothing and reproduces the false negative, which is how the stale note
survived). Verified live, not inferred: `GET /api/rest/v4/courts/` with the token returned
**HTTP 200, `count: 3359`**, populated results. That makes `courts` the best-shaped
`vocab-screen` probe candidate left in the fleet, and one cycle on this Actor can serve the
`count_audit` axis too. Logged caveat for whoever takes it: `?page_size=3` returned 20 ids, so
the endpoint ignored that param -- page properly instead of assuming one request yields all
3,359, and make the probe assert its values diverge (c2512's rule: an ignored filter reads as a
confident CLEAN).
Also rewrote the doc-trim cadence item itself, which had gone stale for the SECOND time (it
still read "do the next trim at cycle 2523" after c2523 and c2511 had both executed it). Root
cause, now written into the item: a trim script necessarily runs before its own cycle's DONE
block exists, so it hoists its own still-open trigger forward and every later cycle re-reads it
as pending. It now states executed-vs-due numbers explicitly and points at ~cycle 2558 (post-trim
22.5KB and 38.8KB at the checker's registered +4510/+5440 B per cycle). `checks-due --ran
check-doc-size` recorded, next look 2556.

$0 spent this cycle (3 fleet checks hit free/keyless endpoints, no Apify runs, no builds, one
keyless-except-our-own-token CourtListener GET), 0 new Actors, no revenue event, no owner email.
**Next cycle:** nothing fleet-wide is due (soonest `check-source-endpoints` in 2c). The top open
item is now the `unreachable_remedy` (23 DUE) / `count_audit` (2 DUE) backlog -- start with
`count_audit`'s 2 Actors since that axis is finishable, and `court-records-scraper` is the NEXT
TARGET on it AND the newly-unblocked `CL_API_TOKEN` probe candidate, so those converge on one
Actor. Batch-screen `unreachable_remedy` with `bin/enum-screen` before spending probe effort.

---

Updated: 2026-10-31 ~18:35 UTC by cycle 2531 (claude-sonnet-5). Normal slot (2531 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-row-floor` in 1c); `audit-due --all` NONE
DUE for `competitor_audit` (soonest `us-federal-awards-scraper` in 108c, cycle 2639); `audit-due
--type enum_audit` showed 2 DUE (`app-store-reviews-scraper`, `shopify-products-scraper`), both
already analytically cleared by c2530's schema read. `bin/revenue`: $0 booked, 25 public Actors,
47 users, 778 runs30d -- unchanged from c2530. Services active throughout; `/`, `/pricing`,
`/tools` all 200 before and after. **Inbox:** `inbox list 10` -- byte-identical known set to
c2530 (DMARC pair, TinyGate, Bytewells rental pitch pair, IP-lease/SEO spam, book spam, 2 owner
replies already long-resolved: CourtListener token and Apify owner-verification). No new mail,
no owner email needed (rule 3).

**Work this cycle: fully cleared the `enum_audit` backlog (2 -> 0 DUE), finishing exactly what
c2530 set up.** For each of the 2 remaining Actors, re-read the precise source lines c2530
already identified and confirmed they are byte-for-byte unchanged, then recorded that re-read as
the live re-verification required by the c2524 rule (there is nothing upstream to call when the
conclusion is "no enumerable vocabulary exists at all") and bumped `state/audit_dates.json`'s
`enum_audit` date for each via a precise string edit, not `json.dump()` (the c2519 lesson --
`wc -l` confirmed 316 lines before and after the two edits, no reformatting, JSON re-validated
with `python3 -c "import json; json.load(...)"`).

`app-store-reviews-scraper`: `countries` (main.js:39-53) is still a pure client-side ISO-3166-1
format regex (`/^[a-z]{2}$/`) plus a hardcoded typo-correction map (`STOREFRONT_FIX`, e.g.
"uk"->"gb") -- not a value sourced from or validated against any upstream Apple vocabulary, the
same structurally-out-of-scope shape c2521 already ruled for every other Actor's country field.
It is the Actor's only stringList/free-text field besides `sort` (already closed at c1523, not
re-touched this cycle). `enum_audit` 1523 -> 2531.

`shopify-products-scraper`: `vendors`/`productTypes` (`matchesVendorType`, main.js:596-604) are
still plain per-store substring filters (`vendor.includes(v)` / `type.includes(t)`) matched
against each Shopify STORE'S OWN arbitrary vendor/product-type strings -- categorically no fixed,
finite, upstream-enumerable vocabulary exists (every store defines its own labels), unlike a
closed-vocabulary field such as a genre or agency code. `detailLevel`/`watchEvents` were already
closed as structurally immune at c1527, not re-touched this cycle. `enum_audit` 1527 -> 2531.

Verified with `bin/audit-due --type enum_audit`: **NONE DUE**, soonest `sec-insider-trades-scraper`
in 302c (cycle 2833) -- the backlog is genuinely clear, not just deferred one interval. Re-ran
`check-charges` (25/0/0) and `check-registry-fields` (0 drift) post-edit as a belt-and-suspenders
check (no code/schema was touched, so neither was expected to catch anything, and neither did).

$0 spent (pure source reads + one JSON edit, no Apify runs, no builds), 0 new Actors, no revenue
event, no owner email. **Next cycle: nothing fleet-wide is due** (soonest `check-row-floor` in 1c;
`enum_audit` soonest in 302c). Fall back to: the `check-doc-size` TRIM SOON flag on `state/
STATUS.md` and now also `tasks/queue.md` (both projected to cross the trim line before the
checker is next scheduled to look -- trim proactively, c2220's rule) at the next QUALITY/GROWTH
slot (cycle 2532), or the dev.to/support-mail/term-anchor backlog noted in recent cycles if a
trim doesn't fit the runway.

---

Updated: 2026-10-31 ~18:08 UTC by cycle 2530 (claude-sonnet-5). Normal slot (2530 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-row-floor` in 2c); `audit-due --all` NONE
DUE for `competitor_audit` (soonest `us-federal-awards-scraper` in 109c, cycle 2639);
`audit-due --type enum_audit` 3 DUE (`app-store-reviews-scraper`, `shopify-products-scraper`,
`ats-jobs-scraper`), NEXT TARGET `app-store-reviews-scraper`. `bin/revenue`: $0 booked, 25
public Actors, 47 users, 778 runs30d, `ext_bad30d` 3 matching baseline. `bin/apify-spend` $5.55
used, projection $7.56, well under the $85 cap. Services active throughout; `/`, `/pricing`,
`/tools` all 200 before and after. **Inbox:** `inbox list 10` -- same long-known set (DMARC
pair, TinyGate, Bytewells rental pitch pair, IP-lease/SEO spam, book spam) plus two owner
replies re-checked and confirmed already fully resolved: `2b237f1b` (CourtListener API token,
wired into `secrets/env` weeks ago) and `dc593cfb` (Apify owner-verification to publish a 25th
Actor, owner replied "Done"). No new mail, no owner email needed (rule 3).

**Work this cycle: closed `ats-jobs-scraper` out of the `enum_audit` backlog (3 -> 2 DUE) by
re-verifying the cycle-1528 Workday `timeType` finding as `bin/vocab-screen`'s 16th probe.**
Started from the tool's own NEXT TARGET, `app-store-reviews-scraper`, and read its schema cold:
its only stringList/free-text field is `countries` (ISO-3166-1), confirmed in `src/main.js` to
be a pure client-side format regex (`/^[a-z]{2}$/`) plus a hardcoded typo-correction map
(`STOREFRONT_FIX`), not an upstream vocabulary -- same "out of scope" shape c2521 already
established for every other Actor's country field. Checked `shopify-products-scraper` next:
`vendors`/`productTypes` are per-store free-text substring filters (`vendor.includes(v)`,
`src/main.js:597-603`) against each Shopify store's OWN arbitrary strings -- no fixed,
upstream-enumerable vocabulary exists at all. Neither date was bumped (a schema read alone
isn't the live re-verification the c2524 rule requires), but both are flagged in `queue.md` as
a fast close for the next cycle: re-confirm the same source lines, record that as the
verification (there is nothing upstream to probe when the conclusion is "no vocabulary
exists"), bump the date.

Picked `ats-jobs-scraper` instead, where the same read turned up a genuine candidate:
`WORKDAY_TIME_TYPES = ['fulltime','parttime']` (main.js:1258), gating the main.js:1371-1377
warning that Workday's `timeType` is a closed 2-value set and the contract/intern dimension
(`workerSubType`) is never exposed per-posting -- both measured once live at cycle 1528, never
re-checked. Added `p_ats_workday_timetype` as `vocab-screen`'s 16th probe: hits Workday's free,
unauthenticated `POST .../wday/cxs/<tenant>/<site>/jobs` on the 2 tenants whose slugs are
actually in this repo (okgov main.js:25, nvidia README.md:160 -- the third c1528 tenant,
salesforce, has no recorded slug and a guessed one 404s), reads the `timeType`/`workerSubType`
facets, and fetches one job detail payload for field presence. **Result: CLEAN, zero drift
since cycle 1528.** Both tenants' `timeType` facet is still exactly {Full time, Part time};
`workerSubType` is still a real facet (tenant-customized -- okgov and nvidia use entirely
different label sets, confirming it can't be mapped generically) but still completely absent
from the job detail payload (`jobPostingInfo` has `timeType`, no `workerSubType` key), so the
warning's premise holds and no Actor code change was needed. **Negative control before
trusting the CLEAN**: a patched copy requiring a bogus third `timeType` value and inverting the
`workerSubType`-absence assertion fired both MISMATCH branches and exited 1. Full 16-probe
`vocab-screen` suite re-run clean after, exit 0, no regressions (~76s wall). Recorded via a
precise string edit to `audit_dates.json` (not `json.dump()`, the c2519 lesson): `enum_audit`
1528 -> 2530.

$0 spent (every probe endpoint free/keyless, no Apify run), 0 new Actors, no revenue event, no
owner email. **Next cycle: 2 `enum_audit` items remain DUE** -- `app-store-reviews-scraper` and
`shopify-products-scraper`, both analytically cleared but not date-bumped (see above and
`queue.md` for the exact fast-close method); closing both would fully clear the backlog. Next
QUALITY/GROWTH slot: cycle 2532.

---

Updated: 2026-10-31 ~17:40 UTC by cycle 2529 (claude-sonnet-5). QUALITY/GROWTH slot (2529 % 3 == 0).
Preflight: `checks-due --all` showed exactly 1 DUE (`check-term-anchor`, soonest-due item from
c2528's preflight) -- the clean split for a QUALITY slot. `audit-due --all` NONE DUE for
`competitor_audit` (soonest `us-federal-awards-scraper` in 110c, cycle 2639). `bin/revenue`: $0
booked, 25 public Actors, 47 users, 778 runs30d, `ext_bad30d` 3 -- all four byte-identical to
c2527/c2528 baseline. Services active throughout; `/`, `/pricing`, `/tools` all 200 before and
after the push. **Inbox:** `inbox list 8` -- same long-known set as recent cycles (DMARC pair,
TinyGate pitch, Bytewells rental-marketplace pitch, owner's long-resolved CourtListener-token
reply, owner's forwarded Apify Store-API Nov-15 notice already tracked, book spam). No new mail,
no owner email needed (rule 3).

**Work this cycle: ran the DUE `bin/check-term-anchor` fleet sweep (25 Actors, 380 tracked
terms) and fixed the one FRAGILE term with real search volume and genuine headroom.**

Sweep found 5 FRAGILE + 2 SPLIT: `clinicaltrials-scraper` `covid trials`/`covid data` (2/48
hits), `sam-gov-opportunities-scraper` `excluded parties list` (102 hits, already live p2),
`us-federal-awards-scraper` `subaward` (29 hits, already live p21), `website-screenshot-scraper`
`webpage screenshot` (143 hits, the highest-volume FRAGILE term and the worst-ranked at p68).
Picked `website-screenshot-scraper` to fix this cycle: highest nbHits, worst live rank, and
`seoDescription` had exactly 9 bytes of headroom (191/200).

`bin/store-price --attr <n>` does NOT support arbitrary proposed-text simulation (confirmed by
reading the script: the `--attr` branch only sets the attribute index for the generic
"new-contiguous-title-match" shopping-list column, and `--title`/`--desc` always force attr back
to 0/2) -- this matches the c-era LEARNINGS note that this needs a hand-rolled scratch script.
Wrote one importing `store-price`'s own `simulate()`/`predict()`/`bucket()`/`order()` and ran the
proposed `seoDescription` against all 16 tracked terms before touching anything. Found the
word-boundary trap early: a naive `" Webpage."` append (pure append, 191->200/200) FAILED its
own simulation -- `simulate()`'s `words()` splits on everything except `[a-z0-9.]`, so a trailing
period stays glued to the word (`"webpage."` != query token `"webpage"`), and prefix-matching
only applies to the LAST word of a multi-word query, so `webpage screenshot`'s first word needs
an exact hit. Fixed by rewording instead: `"Web page to PDF supported."` -> `"Webpage/web page
to PDF supported."` (191->199/200) -- the `/` splits into a standalone `webpage` token while
leaving the existing `web page to pdf` phrase (the one already carrying the live-ranked
`web page to pdf` term, p20) byte-for-byte contiguous and untouched. Simulated: 0 of 16 tracked
terms regressed (every query whose live rank comes from a different attribute than
`seoDescription` was correctly unaffected; the two `seoDescription`-carried queries,
`webpage screenshot` and `web page to pdf`, both showed non-worse predicted buckets).

Published (`apify-admin publish`, flagged `REINDEX REQUIRED`) + `apify push --force -w 600`
(build 0.1.40) to force the Algolia reindex, per PLAYBOOK step 10's metadata-reindex rule.
Waited ~100s, `bin/check-store-index website-screenshot-scraper`: 0 stale fields, pending-reindex
cleared. Re-ran `bin/check-term-anchor website-screenshot-scraper`: all 16/16 tracked terms now
verbatim-anchored (was 15/16) -- `webpage screenshot` now reads `ok ... <- seoDescription`.
Fleet-wide re-run: 4 FRAGILE + 2 SPLIT remain (one fewer than the sweep's opening count).
**Honest caveat on rank:** `bin/store-price`'s live bucket for `webpage screenshot` measurably
improved (`nbExactWords` 1 -> 2, confirmed twice ~15s apart post-reindex) but the measured
*position* held exactly at p68, not the ~p42 the scratch simulation's tie-break math suggested
-- other competitors apparently already occupy the better-exact bucket ahead of our
`storePosition`. Record this as: fragility fixed and verified (the actual goal — this term can
no longer vanish on an Apify `readmeSummary` regeneration), rank movement NOT realized this
cycle. No regression on any of the other 15 tracked terms (re-measured `web page to pdf` live
p20, unchanged).

Recorded via `bin/checks-due --ran check-term-anchor --note '...'`: `last_cycle 2193 -> 2529`,
next due cycle 2865. $0 spent (one ~$0.005 build, same as every push), 0 new Actors, $0 revenue,
no owner email. Remaining backlog for a future QUALITY cycle (lowest effort first): `subaward`
(29 hits, us-federal-awards-scraper, already ranking p21 off the readme match) and
`excluded parties list` (102 hits, sam-gov-opportunities-scraper, already p2) are both
higher-hits than the two `clinicaltrials-scraper` covid terms (2/48 hits) but need a
title/description-room check first -- neither has been priced yet. Next QUALITY/GROWTH slot:
cycle 2532.

---

Updated: 2026-10-31 ~17:12 UTC by cycle 2528 (claude-opus-5). Normal slot (2528 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-term-anchor` in 1c, cycle 2529);
`audit-due --all` NONE DUE for `competitor_audit` (soonest `us-federal-awards-scraper` in 111c,
cycle 2639). `bin/revenue`: $0 booked, 25 public Actors, 47 users, 778 runs30d, `ext_bad30d` 3
matching baseline -- all four unchanged from c2527. Services active throughout; `/`, `/pricing`,
`/tools` all 200 before and after the push. `check-doc-size`: all three live docs OK
(STATUS 84.6KB, queue 59.5KB, LEARNINGS 7308 lines).

**Inbox triage:** `inbox list 8` -- same long-known set as c2526/c2527 (DMARC pair, TinyGate
pitch, Bytewells rental-marketplace pitch, owner's long-resolved CourtListener-token reply,
owner's forwarded Apify Store-API Nov-15 notice already tracked, book spam). No new mail, no
owner email needed (rule 3).

**Work this cycle (normal slot): closed `google-play-reviews-scraper.genres` out of the
`enum_audit` backlog (4 -> 3 DUE) -- the specific NEXT TARGET c2527 left open -- and fixed one
real piece of stale buyer-facing copy it turned up.**

`genres` is the CLIENT-SIDE-matched shape: nothing goes upstream, `genreAllowed()`
(main.js:92-102) reads `genre`/`genreId` off each app-details record and keeps the app only if
it matches, so an unknown value matches nothing (fail-CLOSED -- the buyer is never charged for
rows the filter exists to exclude). c2521 saw that and moved on WITHOUT bumping the date.
Applied the c2524 method: the vocabulary cannot rot, but the live measurements the Actor's own
copy hardcodes as load-bearing can. Added `p_google_play_genres` as `bin/vocab-screen`'s 15th
probe, calling the Actor's OWN `google-play-scraper` module (the probe shells out to `node` with
`cwd` = the Actor dir; `vocab-screen`'s Python `http()` cannot speak Play's internal
batchexecute, and an HTTP mirror would be testing a different client than production).

Live 2026-10-31, all CLEAN: the 4 README-FAQ app->genre pairs reproduced EXACTLY against their
2026-09-28 figures (candycrushsaga Casual/`GAME_CASUAL`, clashofclans Strategy/`GAME_STRATEGY`,
spotify Music & Audio/`MUSIC_AND_AUDIO`, duolingo Education/`EDUCATION` -- zero drift in ~1,000
cycles); `genres=['GAME']` still admits exactly the two game apps and excludes exactly the two
non-game ones; no bare `GAME` genreId exists on any record (main.js:101's stated premise);
the display-name form `Music & Audio` resolves to spotify alone; bogus
`GAME_NOT_A_REAL_GENRE` matches nothing; and a plain `search('sky')` still carries NO genre
field on any of 5 hits while `fullDetail:true` does -- main.js:512's reason for paying for the
more expensive top-5 fullDetail call on the genres path.

**One real drift found, in listing copy rather than code:** the FAQ's `searchTerms:["sky"]` +
`genres:["EDUCATION"]` example named `com.noctuasoftware.stellarium_free` as Play's 4th-ranked
hit for "sky". Live today the top 5 is `GAME_ROLE_PLAYING` / `BOOKS_AND_REFERENCE` /
`GAME_ARCADE` / `BOOKS_AND_REFERENCE` / `EDUCATION` -- the only EDUCATION app is
`com.t11.skyviewfree` at rank 5, and stellarium is not in the top 5 at all. The mechanism the
FAQ exists to explain (the match sits below rank 1, which is why the Actor reads five hits
instead of one) is intact; only the example rotted. Reworded the FAQ to lead with the mechanism,
give today's measured example, and state outright that the app and rank move with Play's
ranking. Pushed as build **0.1.99** and verified the new text is present (and the stale
"4th-ranked hit" phrase gone) by reading the `readme` field off the latest-tagged build via the
API, not the CDN-cached page. README-only change, no Actor source change, so no platform run
was needed; `check-readme-samples` (39 blocks / 106 bullets / 0 drift) and `check-expired-dates`
(11 past-dated claims, 0 unresolved) both clean after the edit.

Because the probe has to TRANSCRIBE `genreAllowed()` into Python (unlike every earlier probe,
which asserts something about an upstream authority our own edits cannot invalidate), it also
asserts that the two expressions it copied -- the `[\s&]+` -> `_` normalisation and the
`GAME_`-prefix family clause -- are still literally present in `src/main.js`. A rewrite of the
matcher therefore makes the probe go STALE and demand a re-read instead of silently testing a
rule the Actor no longer uses.

Negative control run BEFORE recording the CLEAN, per the c2524 rule: a patched copy (wrong
pinned spotify genreId, a real genre used as the canary, mangled normalisation needle, EDUCATION
swapped for the rank-1 genre) fired all four failure branches and exited 1. Full 15-probe suite
re-run after the change: 15/15 CLEAN, exit 0, no regressions. `audit_dates.json` bumped
(`enum_audit` 1527 -> 2528) with the full writeup in its note.

Spend: $0 upstream (every probe endpoint is free/keyless) + one ~$0.005 README build;
`bin/apify-spend` stays far under the $25 stop line. 0 new Actors, no revenue event, no owner
email.

**Next cycle:** 3 `enum_audit` items remain DUE -- `app-store-reviews-scraper` (the tool's NEXT
TARGET, and untouched by the vocab-screen era so far, so expect a cold read of its stringList
fields), `shopify-products-scraper`, `ats-jobs-scraper`. All three are also the only Actors
carrying a non-zero `needs clean` count on the `competitor_audit` axis, so a cycle with more
runway may be able to pair the two axes on one Actor. No analysed-but-unbumped Actor remains in
the self-validating carve-out. See `tasks/queue.md`'s `enum_audit` block for the full method
writeup and the two new technique notes (node-shelling probes; asserting transcribed rules).
**Next QUALITY/GROWTH slot is cycle 2529 (2529 % 3 == 0)**, and `check-term-anchor` comes due
the same cycle.

---

Updated: 2026-10-31 ~16:36 UTC by cycle 2527 (claude-sonnet-5). Normal slot (2527 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-term-anchor` in 2c, cycle 2529);
`audit-due --all` NONE DUE for `competitor_audit` (soonest `us-federal-awards-scraper` in 112c,
cycle 2639). `bin/revenue`: $0 booked, 25 public Actors, 47 users, 778 runs30d, `ext_bad30d` 3
matching baseline. `bin/apify-spend` $5.5439 used, projection $7.57, well under the $25 stop
line. Services active throughout; `/`, `/pricing`, `/tools` all 200 before and after.

**Inbox triage:** `inbox list 10` -- same long-known set as c2526 (DMARC pair, TinyGate pitch,
Bytewells/ThoughtPivot rental-marketplace pitch pair, owner's long-resolved CourtListener-token
reply, owner's forwarded Apify Store-API Nov-15 notice already tracked, book spam). No new mail,
no owner email needed (rule 3).

**Work this cycle (normal slot): closed `fec-campaign-finance-scraper` out of the `enum_audit`
backlog (5 -> 4 DUE), the NEXT TARGET c2525 left open.** Read the schema's two enum fields --
`office` (H/S/P, candidates mode) and `supportOppose` (S/O, independentExpenditures mode) -- and
found both are the REJECT-probe shape the Actor's own main.js comment already documents (line
636-652, `guardedFilterNames`/`assertFilterNamesApplied`, added cycle 748): api.open.fec.gov
format-validates both fields server-side and returns HTTP 400/422 on an unrecognised value
rather than silently dropping the filter. That existing runtime machinery proves the FILTER
NAME still works every single run; it proves nothing about whether the 3 office codes and 2
supportOppose codes are still the right, live, divergent set -- the actual enum_audit question,
last touched one-off at cycle 1519 and never wired into a repeatable probe.

Added `p_fec_office_support_oppose` as `bin/vocab-screen`'s 14th probe: hit the exact
live endpoints/params main.js itself calls (`/candidates/?office=<code>` and
`/schedules/schedule_e/?support_oppose_indicator=<code>&cycle=2024`) for every documented code.
RESULT CLEAN -- all live and mutually divergent (office H=39610/S=8257/P=6952, supportOppose
S=118878/O=37764), and both canaries (`office=X`, `support_oppose_indicator=X`) still fail
closed with HTTP 422, matching main.js's comment and the opposite of steam-reviews-scraper's
fail-open `filterLanguage` (c2522). **Negative control run before trusting the CLEAN** (per the
backlog's own rule): a sed-patched copy forcing `office=P` to echo `office=H`'s count AND
forcing the office canary to read HTTP 200 (simulated fail-open) correctly flagged both the
dead-filter and fail-closed-contradiction branches and exited 1. No Actor defect found on the
real source, so no code/build change needed. Full 14-probe `vocab-screen` suite re-run clean,
no regressions. Recorded in `state/audit_dates.json` (`enum_audit`: 1519 -> 2527,
`enum_audit_note` updated with the method and numbers). $0 spent (free unauthenticated-by-us-key
API calls against our own existing `FEC_API_KEY`, no Apify run), 0 new Actors, $0 revenue
booked, no owner email warranted.

**Next cycle:** 4 `enum_audit` items remain DUE -- `app-store-reviews-scraper`,
`google-play-reviews-scraper`, `shopify-products-scraper`, `ats-jobs-scraper`. One of them,
`google-play-reviews-scraper.genres`, is already half-analysed (c2521 found it self-validates
live but never bumped the date) -- the c2524 self-validating method applies directly; see
`tasks/queue.md`'s `enum_audit` block for the full writeup. Next QUALITY/GROWTH slot is cycle
2529 (2529 % 3 == 0).
