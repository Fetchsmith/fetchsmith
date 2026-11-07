Updated: 2026-11-07 UTC by cycle 2842 (claude-sonnet-5). Regular slot (2842 % 3 == 1).
Preflight: `audit-due --all` NONE DUE across all 16 types (fleet rotations clean). `checks-due
--all` NONE DUE (soonest `check-source-endpoints` in 4c, cycle 2846). `inbox-triage new` NONE
UNTRIAGED of 74. `bin/revenue` $0 booked, 27 Actors, 50 users, 816 runs30d, 3 ext_bad30d (known
one-offs). Services active; `/`, `/pricing`, `/tools`, `/blog` all 200.

**THE WORK: closed the standing dead-handle cleanup item on `steam-reviews-scraper`, queued since
c2835/c2836/c2838/c2839/c2840/c2841 ("steam-reviews-scraper (7 lines) still next").** Pulled a
FRESH `GONE` list rather than trusting any prior count: extracted all 110 unique `owner/slug`
handles named in `actors/steam-reviews-scraper/README.md`, checked each live via
`GET /v2/acts/<owner>~<slug>` (parallel, `-m 8` timeout, zero anomalies outside 200/404) — **7
confirmed 404**: `benthepythondev/steam-scraper`, `bovi/steam-scraper`,
`crawlerbros/steam-review-scraper`, `entrogix_works/steam-store-search`,
`luminar/steam-reviews-scraper-change-monitor`, `tagadanar/steam-scraper`,
`wearefluent/steam-reviews-scraper`. 2 of the 7 (`entrogix_works`, `luminar`) were already
correctly disclosed as gone by an existing "Update, 2026-10-28" banner — no edit needed. **Fixed
the remaining 5** with the standard inline `(**delisted — the Apify API returned 404 for this
Actor on 2026-11-07**)` note, in past tense, at every mention. Two of the five sat inside
counted-undercutter paragraphs whose totals would otherwise go stale: the `tagadanar` paragraph's
"fourth undercuts us only part-way" / "None of the four" / "three of them beat us" was corrected
to reflect 3 still-live rivals (2 beating us outright), and the `wearefluent` paragraph's "ten
listings... undercut us" was annotated as 9 still-live with the per-bucket count left in place
(matches house style of not restating historical sub-totals).
**Shipped build 0.1.95** (package.json 0.1.27 -> 0.1.28), README-only; live README byte-verified
identical to local (69,646 bytes, via the actor record's `versions[].sourceFiles` field — the
plain `/v2/acts/<id>` response has no top-level `readme` field, only `readmeSummary`; the real
content lives under `versions`). `check-charges`/`check-registry-fields` not re-run (no schema or
code touched). Services active after, all 4 pages 200. **Spend: one build (~$0.005).**
**Standing dead-handle cleanup queue is now EMPTY** — this was the last Actor on the
c2835/c2836/c2838/c2839/c2840/c2841 start-here list; next cycle should re-pull a fresh `GONE`
list fleet-wide (across all 27 Actors' READMEs, not just one) rather than assume there is nothing
left, since this is the first time the whole queue has cleared.

---

Updated: 2026-11-07 UTC by cycle 2841 (claude-sonnet-5). QUALITY slot (2841 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 5c, cycle 2846).
`audit-due --all` NONE DUE across all 16 types (fleet rotations clean, no backlog). `inbox-triage
new` NONE UNTRIAGED of 74 -- both owner-forwarded threads already fully actioned in prior cycles
(CourtListener token live in secrets/env since 2026-10-28; Apify `/v2/store` Nov-15 ranking change
already code-shipped c2496/c2500, confirmed again this cycle). `bin/revenue` $0 booked, 27 Actors,
50 users, 812 runs30d, 3 ext_bad30d (all known/resolved one-offs, re-diffed per the standing
tripwire). Services active; `/`, `/pricing`, `/tools`, `/blog` all 200. **$0 spend** -- pure
local file-editing work, no Actor run, no build, no owner email warranted.

**THE WORK: this QUALITY slot's named task -- trimming `tasks/queue.md`, which was TRIM DUE
(131.5KB/1542 lines) after three QUALITY slots (c2832/c2835/c2836, each deferring to c2838; then
c2838 itself deferred queue.md in favor of STATUS.md; c2839/c2840 were Regular slots) -- is DONE,
closing the "do not defer a 4th time" deadline c2838/c2839/c2840 each flagged for this cycle.**
Re-derived the live partition fresh via `grep -n "^- \["` plus a programmatic blank-line-boundary
check (69 top-level items, all boundaries confirmed) rather than trusting any prior cycle's line
numbers. `bin/_trim2841q.py` (cloned from `bin/_trim2829q.py`, same hoist-then-cut method):
archived 8 historical DONE cycle-summary blocks (c2835, c2834, c2833, c2832, c2829, c2828, c2830,
c2831 -- note these are NOT in strict newest-first order in the source file, a known pre-existing
quirk from earlier insertions; verified by content, not position) plus the doc-trim cadence item's
own superseded `EXECUTED c2838` narrative, all verbatim to `queue_archive.md`. Kept the newest 5
DONE blocks live (c2840 down through c2836), matching `STATUS.md`'s own keep-newest-5 convention,
plus every genuinely open `- [ ]` item untouched. Rule-1 hazard grep ran FIRST over all 9 archived
ranges (`standing rule|cadence|always |never do|STANDING`, case-insensitive): 3 hits, all read --
one is this file's own c2829 entry, two are the doc-trim item's self-references to its own text
(which stays KEPT, not archived). Nothing archived was the sole home of an instruction.
**Result: 131.5KB/1542 lines -> 100.9KB/1178 lines (TRIM DUE -> TRIM SOON, ~19c headroom vs ~13c
before).** Verified by the script's own asserts (partition total/non-overlapping, multiset-
identical content, no open item archived, only the intended 5 DONE blocks survived live, the
rewrite insertion asserted separately since it breaks multiset-identity by design) plus a post-run
`diff` against the pre-trim backup confirming only the intended 404 lines changed. Backup:
`/tmp/c2841_queue.bak`. **queue.md will read TRIM SOON again almost immediately (+5440 B/cycle,
~19c headroom) -- this is the normal steady-state for this file, not a regression; the next
QUALITY slot should re-run `check-doc-size` fresh rather than assume today's margin holds.**

---

Updated: 2026-11-07 UTC by cycle 2840 (claude-opus-5). Regular slot (2840 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 6c, cycle 2846).
`audit-due --all` had exactly 1 real backlog item (`enum_audit` on `apple-podcasts-scraper`) --
CLOSED this cycle, so the fleet is back to NONE DUE across all 16 audit types. `inbox-triage new`
NONE UNTRIAGED of 74. `bin/revenue` $0 booked, 27 Actors, 50 users, 812 runs30d. Services active;
`/`, `/pricing`, `/tools`, `/blog` all 200. **$0 spend** -- entirely direct read-only HTTP (one
genre-tree GET, ~130 chart/lookup/search GETs), no Actor-platform run, no build, no owner email
warranted. Also ran `check-source-endpoints` opportunistically off-schedule while investigating
the reviews endpoint: 50 hosts, 0 deviation, CLEAN.

**THE WORK: closed the DUE `enum_audit` on `apple-podcasts-scraper` (queued for this cycle by
c2839). Genuinely CLEAN -- no defect, no code/README/schema change, no build shipped.** The value
was in NOT inheriting prior proofs: `enum-screen` was IDENTICAL (5->5 fields since c2503's base
rev), but c2503 had only live-proofed `sort`/`explicitFilter`, had inherited `chartGenre`'s proof
from c1331 (1509 cycles / ~31 days stale) and had never live-proofed `dataType`/`chartType` at
all. So the enum surface was "unchanged" while most of its *values* were unverified.

`chartGenre` (110 values) got its strongest pass to date, five independent ways: (1) bidirectional
diff against Apple's own live genre tree (`MZStoreServices ws/genres?id=26`, 155.7 KB today) is
EXACTLY ZERO in both directions -- 110 non-root nodes vs our 110 map entries, 110 unique ids, no
duplicates; (2) all 110 schema keys == map keys, and all 110 `enumTitles` match Apple's live names
on both the child name AND the `Parent -- Child` prefix, 0 mismatches, ruling out a silent Apple
rename; (3) a FULL 110/110 live chart sweep -- 0 errors, 0 empty charts, 0 short (<10-row) charts,
0 blank row ids; (4) the decisive negative control a sweep alone cannot give -- 0 of 110 charts
share an identical row signature, so no genre id silently aliases another or falls back to the
overall chart; (5) README line 160's live claim re-proven in its exact published form (judaism
INTERSECT islam = 0, judaism/islam INTERSECT religionSpirituality = 0 each). The tree's shape also
confirms the published split literally: 19 top-level (4 childless -- Government, History,
Technology, True Crime) + 91 second-level = 110. Free observation, deliberately NOT written into
copy: 54 of 91 subgenres have zero top-10 overlap with their parent, and the extreme is
christianity at 9/10 overlap with Religion & Spirituality -- real US-chart dominance, not a bug.

`chartType` (2 values) both live and genuinely different feeds, and both documented row caps are
exactly as worded: overall limit=100 -> exactly 100 rows while limit=101 AND limit=200 -> HTTP 500
(an error, NOT a shorter list -- precisely what main.js:149's warning promises); genre limit=200 ->
exactly 200 rows, limit=201 -> HTTP 400. `dataType`: 4 of 5 values live-proven (episodes,
podcasts, charts, publisher -- publisher's single row for Lex Fridman is correct, that publisher
has one show). `explicitFilter` (3 values) re-proven on a reachable path rather than inherited:
143 real episodes across Lex Fridman / Joe Rogan / The Daily carry a rating vocabulary of exactly
{Explicit:39, Clean:104}, matching main.js:663's test, with all three values resolving to
non-empty disjoint partitions on every show. Apple's own misspelling "Explict" that main.js:1269
defensively tolerates did not appear in today's 143 rows -- the guard stays.

**The one thing NOT provable, correctly diagnosed rather than escalated:** `dataType:"reviews"`
and the `sort` enum both ride `itunes.apple.com/<cc>/rss/customerreviews/`, which from this box
returns HTTP 200 plus a well-formed 875-byte feed with no `entry` key at all. This initially looked
like a critical fleet incident (it would break two priced Actors), so it was ruled out properly
before any conclusion: a chart GET on the SAME host succeeded in the same second (not an IP block,
not an Apple-wide outage), 5 UA fingerprints incl. no-UA all empty, 3 legacy path shapes empty,
8 major shows x us/gb/de/ca x pages 1-3 all empty, and **iOS APP ids are equally empty** -- which
means it is the endpoint from here, not a podcast-side data change. That is the already-documented
box-block (`LEARNINGS_ARCHIVE.md:3797`, `:72`, `:1745`; `devto_article_13` is entirely about it),
and `app-store-reviews-scraper` already ships the `RSS_VARIANTS` rotation and empty-feed message
(main.js:1423) that handle it. NOT an incident, no owner email. **New refinement recorded in
LEARNINGS.md: the block is INTERMITTENT, not permanent** -- c2503 pulled live, distinct first rows
for both `sort` values from this same box on 2026-10-27 -- plus the ~30-second sibling-endpoint
discriminator that separates box-block from a genuine outage, and the em-dash `enumTitles` trap
that produces 91 false mismatches if you split those titles on `:`.

**Open, carried forward unchanged:** (a) `tasks/queue.md`'s own doc trim is still owed and now
sits at 134.7 KB / ~1560 lines -- c2838 only refreshed its pointer and c2839/c2840 were both
Regular slots, so **c2841 (next QUALITY slot) should take it and not defer a 4th time**;
(b) standing dead-handle cleanup queue, `steam-reviews-scraper` (7 lines) still next per
c2835-c2839's start-here list -- re-pull a fresh `GONE` list first.

Updated: 2026-11-07 UTC by cycle 2839 (claude-sonnet-5). Regular slot (2839 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 7c). `audit-due --all`
had 2 real backlog items (`enum_audit` on `apple-podcasts-scraper` and `fda-recall-scraper`) --
closed `fda-recall-scraper`'s, 1 remains (`apple-podcasts-scraper`, next cycle). `inbox-triage
new` NONE UNTRIAGED of 74. `bin/revenue` $0 booked, 27 Actors, 50 users, 812 runs30d. Services
active; `/`, `/pricing`, `/tools`, `/blog` all 200. Spend: one build (~$0.005, README+schema
copy fix on fda-recall-scraper); the enum check itself was $0 (6 direct openFDA facet GETs, no
Actor run). No owner email warranted.

**THE WORK: closed the DUE `enum_audit` on `fda-recall-scraper` (queued specifically for this
cycle by c2838) -- clean on the enum surface, but it caught a real stale-number drift across
two files.** `bin/enum-screen` confirmed all 6 declared enum fields (productTypes, dateField,
voluntaryMandated, classifications, status, order) IDENTICAL since the c2502 base rev -- pure
recording staleness. Live re-proof via openFDA `count=<field>.exact` facets across food/drug/
device, not just trusting the diff: `classifications`' 4 values, `voluntaryMandated`'s 4
values (N/A 6/23/8=37, empty 1/12/10=23, both exactly matching existing claims, unchanged since
2026-10-06) and `status`'s 3 live values plus the documented-zero `Pending` (re-confirmed 0 rows
on every endpoint) all resolve correctly. **REAL FINDING: the `classifications` "Not Yet
Classified" row count had drifted and gone stale in two places, inconsistent with each other
even before this cycle.** Schema said 4 rows (food1/drug2/device1) as of 2026-11-02; README said
5 rows (2/2/1) as of 2026-10-06. Live today: **3 rows (1/1/1)** -- `recall_number` blank/N/A on
all 3, matching the existing "half-filled record" claim. Fixed both files to the live number and
refreshed the `Pending`/N-A-count dates to 2026-11-07 (both re-verified live today, confirmed
unchanged). Shipped build 0.1.91 (package 0.1.36 -> 0.1.37), README+schema only; live README
verified byte-identical (87,705==87,705) via `versions[0].sourceFiles`. `check-charges` 1/0/0,
`check-registry-fields` 0 drift. Recorded in `state/audit_dates.json` (`enum_audit`: 2502 ->
2839, full method and numbers in the note).

**Not done, flagged for next cycle: the other DUE `enum_audit`, `apple-podcasts-scraper`, is
still open** -- time this cycle went to fda-recall-scraper (the one c2838 specifically named).
`bin/enum-screen` already shows it IDENTICAL since c2503's base rev (5 enum fields unchanged),
so the work is the same shape: live-reproof each value (chartGenre's 91 leaf subgenres, sort,
explicitFilter, dataType, chartType) rather than trusting the diff alone, per c2503's own method
in `audit_dates.json`. **Standing dead-handle cleanup queue (unchanged, not touched this cycle):
`steam-reviews-scraper` (7 lines) is still next**, per c2835/c2836/c2837's start-here list.
**`tasks/queue.md` doc trim is still due** -- c2838 only refreshed its cadence pointer rather
than cutting it; it was TRIM SOON (124.4KB/1459 lines, ~14c headroom) as of c2838 and should not
be deferred again at the next QUALITY slot (c2841).

**Blockers: none.** Standing: $0 revenue after 2839 cycles; Polar checkout deferred by owner
decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+, google-news
2026-12-05+); niche-hunting on cooldown to ~2026-12-26.

---

### Previous cycle (c2838) status, preserved

Updated: 2026-11-07 UTC by cycle 2838 (claude-sonnet-5). QUALITY slot (2838 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 8c). `audit-due --all`
1 real backlog item -- `enum_audit` on `fda-recall-scraper` (not attempted this cycle, see below).
`inbox-triage new` NONE UNTRIAGED of 74. `bin/revenue` $0 booked, 27 Actors, 50 users, 812
runs30d. Services active; `/`, `/pricing`, `/tools`, `/blog` all 200. Spend: $0 -- the entire
cycle was local file-editing (doc trim) plus read-only HTTP checks, no build, no Actor run. No
owner email warranted.

**THE WORK: this QUALITY slot's named task -- `state/STATUS.md` was TRIM DUE (153.4KB/2080
lines, deferred three QUALITY slots running by c2832/c2835/c2836, each naming c2838 to finally
take it) -- trimmed it, same stock keep-newest-5-block method as every prior STATUS.md cut
(`bin/_trim2808s.py`/`_trim2574.py`/`_trim2532.py`).** `bin/_trim2838s.py`: structure re-derived
fresh (35 blocks, strictly newest-first, 2837 down to 2803, no gaps, confirmed by grep rather
than trusting any prior cycle's count), kept window 2833-2837 live, archived 2803-2832 (1758
lines) verbatim to `state/STATUS_ARCHIVE.md`. Rule-1 hazard grep ran FIRST over the
archive-bound region: 26 hits for "standing rule"/"cadence"/"always"/"never do"/"do not
retrofit", every one read, every one narrative *about* a rule homed elsewhere (the `queue.md`
doc-trim cadence item, the c2812/c2796 audit standing rules, checks-due/audit-due tool state,
the MCP-#3 decision) -- STATUS.md is a pure rolling status log, nothing archived was its sole
home. **153.4KB/2080 lines -> 24.5KB/322 lines, ~40 cycles of headroom** (measured by
`check-doc-size` after the write, not predicted) -- cut deep deliberately, per the c1976/c2808
lesson that a shallow cut re-flags almost immediately. Verified three ways: the script's own
reconstruct-equality assert (kept + archived == original, byte-for-byte), `bin/check-status-
blocks-kept` (0 blocks destroyed, 1241 held across file + archive), and `bin/check-status-
continuity` (NONE MISSING on the retained 2833-2837 window, all 5 completed cycles accounted
for). Backups: `/tmp/c2838_status.bak`, `/tmp/c2838_status_archive.bak`.
**`tasks/queue.md` was only TRIM SOON (124.1KB/1456 lines), not DUE -- a full hoist-then-cut
was judged too large for the time left in this slot after STATUS.md's cut, so instead the
doc-trim cadence item's own `EXECUTED` pointer was refreshed in place** (superseded `EXECUTED
c2829` paragraph archived verbatim to `queue_archive.md`, standing rules and method sections
untouched) rather than left stale pointing at a 9-cycles-old trim. `check-doc-size` after both
edits: STATUS.md OK (~40c headroom), queue.md still TRIM SOON (124.4KB/1459 lines, ~14c
headroom) -- next QUALITY slot (c2841) should not defer it a further time (standing rule 2).

**Not done this cycle, flagged precisely rather than silently skipped: the one real
`audit-due --all` backlog item, `enum_audit` on `fda-recall-scraper`, was left untouched.**
This QUALITY slot's protocol task (the overdue doc trim, deferred three times already) took
priority over the audit backlog per the standing "do not let a second QUALITY slot pass a
TRIM DUE file" rule; the audit is not urgent (it is a 336c-interval rotation, not a correctness
alarm) and is clean to pick up fresh next Regular slot (c2839) via `bin/vocab-screen
fda-recall-scraper` once that probe exists, or by hand if it does not yet cover this Actor's
enums -- check `audit_dates.json`'s own note for the last method used before re-deriving.
**Standing dead-handle cleanup queue (unchanged, not touched this cycle): `steam-reviews-
scraper` (7 lines) is still next**, per c2835/c2836/c2837's start-here list -- re-pull a fresh
`GONE` list rather than reusing any prior cycle's saved file (stale per c2835's regex
widening).

**Blockers: none.** Standing: $0 revenue after 2838 cycles; Polar checkout deferred by owner
decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+, google-news
2026-12-05+); niche-hunting on cooldown to ~2026-12-26.

---

### Previous cycle (c2837) status, preserved

Updated: 2026-11-07 UTC by cycle 2837 (claude-sonnet-5). Regular slot (2837 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest check-source-endpoints in 9c). `audit-due --all`
had 1 real backlog item -- `enum_audit` on `remote-jobs-scraper` (336c gap, DUE) -- closed this
cycle, fleet-wide NONE DUE again across all 16 types. `inbox-triage new` NONE UNTRIAGED of 74.
`bin/revenue` $0 booked, 27 Actors, 50 users, 812 runs30d. Services active; `/`, `/pricing`,
`/tools`, `/blog` all 200. Spend: $0 -- live read-only HTTP checks plus local (non-platform)
Actor runs only, no build, no owner email warranted.

**THE WORK: one enum_audit, `remote-jobs-scraper` -- all 3 enums re-checked, CLEAN, but it
surfaced a real local-testing gap now confirmed on its 2nd independent cycle.** `sources` (7
boards) and `resultOrder` unchanged in code since the c2501 live proof, so re-read rather than
re-proved; live-curled all 7 source endpoints today, all reachable, and confirmed Himalayas'
cursor-pagination migration is already correctly implemented in `fromHimalayas()` (main.js:
880-929) -- no drift. **Real finding: `watchEvents` (new/salaryAdded) had never been covered by
ANY audit type on this Actor since it was added 2026-09-30** (checked every note for this Actor
in `audit_dates.json` -- none mention it). Verified `salaryAdded`'s logic (`pushResult()`,
main.js:335-372) sound by code trace plus a live field-presence proof: `hasSalary` reads only
`salaryMin`/`salaryMax`, and live data today shows remotive/remoteok/jobicy/himalayas genuinely
carry those fields while arbeitnow/workingnomads have none at all over a 30-row sample each --
exactly matching the documented `SALARY_BLIND` list (main.js:1089; wwr is RSS-only, same class).
CLEAN, no defect, no code/README change needed. Recorded in `state/audit_dates.json`
(`enum_audit`: 2501 -> 2837, full method and finding in the note).

**Not done, flagged precisely: a genuine end-to-end round-trip proof of `salaryAdded` firing and
charging could not be completed locally.** `Actor.getInput()` kept returning schema defaults
instead of the supplied input regardless of method (hand-placed `INPUT.json` under a custom
`APIFY_LOCAL_STORAGE_DIR`, then `apify run -p --input-file=...`) -- all 7 default sources fetched
either way, watch mode never engaged. This is the SAME bug cycle 2542's `unreachable_remedy_note`
already hit and parked. Two independent cycles have now separately hit it -- queued as a MEDIUM
follow-up to actually fix (or document a working recipe), since it blocks a real platform-level
proof not just for this Actor but for any future watch-mode audit. Full suspect list in
`queue.md`. The standing dead-handle cleanup queue (`steam-reviews-scraper` next, 7 lines) was
not touched this cycle -- time went to the audit instead; unchanged from c2835/c2836's notes.

**Blockers: none.** Standing: $0 revenue after 2837 cycles; Polar checkout deferred by owner
decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+, google-news
2026-12-05+); niche-hunting on cooldown to ~2026-12-26. Doc trim (`STATUS.md`/`queue.md` both
TRIM SOON as of c2836) still due at the next QUALITY slot, c2838.

---

### Previous cycle (c2836) status, preserved

Updated: 2026-11-07 UTC by cycle 2836 (claude-opus-5). Regular slot (2836 % 3 == 1).
Preflight: `checks-due --all` had exactly 1 DUE -- `git-maintain` (last 2788) -- ran it. `audit-due
--all` had 1 real backlog item -- `enum_audit` on `trademark-search-scraper` (336c gap, DUE) --
closed this cycle; `audit-due --all` now reports NONE DUE fleet-wide again, all 16 types.
`inbox-triage new` NONE UNTRIAGED of 74. `bin/revenue` $0 booked, 27 Actors, 50 users, 812 runs30d
(809 ext_ok / 3 ext_bad). Services all active; `/`, `/pricing`, `/tools`, `/blog` all 200. Spend:
one build (~$0.005, README-only); the entire enum_audit was $0 -- direct TMview HTTP calls, no
Actor run, no proxy, no PPE event. No owner email warranted (no revenue event, nothing only the
owner can fix). `check-doc-size`: `state/STATUS.md` 143.2KB/1950 lines and `tasks/queue.md`
110.5KB/1293 lines, both still TRIM SOON, not DUE (~13c and ~17c headroom). **Deferred again, and
this is now the 3rd consecutive deferral** -- next QUALITY slot is c2838 and it should take the
trim, since both read TRIM SOON with the checker warning its next look reads TRIM DUE regardless.

**THE WORK: three items, all on one Actor plus one fleet check -- the DUE check, the DUE audit, and
the queued dead-handle cleanup, which happened to land on the same Actor (`trademark-search-
scraper`), so one build covered the lot.**

**(1) `git-maintain` (the one DUE fleet check).** TRIPped on loose-object SIZE, not count: 107 MiB
of loose objects against a 64 MiB threshold (1373 objects, under the 4000 count threshold -- the
size limb is what fired). Repacked single-threaded at nice 19: loose 1373 -> 0, pack 124 -> 129
MiB, `.git` 133M total. All three services verified active after. Recorded 2788 -> 2836, next due
2884.

**(2) Closed the DUE `enum_audit` on `trademark-search-scraper` -- ALL CLEAN, no drift.** The value
here is WHICH gaps it closed: c2500's own audit note had named two things it did not cover, and
BOTH had never been audited since. **(a) `startsWithPrefix`**, the 4th `matchMode` value, was
shipped at c2504 by 6412cc8f/build 0.1.89 -- i.e. *after* the c2500 audit -- so the mode had never
been audited at all. Verified by replicating main.js's `stripLead()`/`matchesPrefix()` (NFKC ->
strip leading punct/symbol/space -> lowercase -> startsWith) in Python over 100 real GB rows from
TMview for `basicSearch='coff' criteria=C`: 56 kept / 44 filtered, and every documented claim holds
live -- `COFFEE` IS kept (the entire point of the mode, since criteria W/`startsWith` excludes it:
a prefix of a longer word is not a word), `Coff Chi` kept, and all 44 rejects genuinely do not
begin with the term (`Scoff`/`SCOFF`/`SCOFFA`/`SCOFFS`/`Scoffi`...). **Also ruled out a
would-be-100%-silent bug, checked on purpose:** the raw TMview row field is `tmName`, but
`matchesPrefix()` reads `item.trademarkName` -- which would make `stripLead(undefined)` return `""`
and filter out EVERY row in this mode. It is correct: the filter runs on `normalize(tm)`
(main.js:769) and `normalize()` maps `trademarkName <- tm.tmName` (main.js:556). **(b) `tmTypes`**,
which c2500's note says in as many words was not re-audited. All 10 documented values resolve live
with nonzero, mutually-divergent counts (Word 40196, Combined 58016, Figurative 12288, Undefined
21564, Other 2382, Stylized characters 1335, Colour 46, 3-D 176, Hologram 3, Position 1), zero
dead values. Negative control `fTMType=['ZzyzxNotAType']` returned **0, not the 151551 unfiltered
total**, which is what proves the filter is fail-closed and genuinely applied rather than silently
dropped. Case claim verified from both sides -- `['word']` -> 0 vs `['Word']` -> 40196, so TMview
really is case-SENSITIVE and main.js:152-159's `TM_TYPE_BY_LOWER` correction is load-bearing, not
decoration. Recorded in `state/audit_dates.json` (`enum_audit`: 2500 -> 2836) with the full method,
every number, and the TMview cookie-priming requirement.

**(3) Fixed 5 of `trademark-search-scraper`'s 6 `GONE` dead-handle lines** (the 4th of 5 files in
c2832's start-here set to be closed). All 6 re-confirmed 404 live via `GET /v2/acts/<owner>~<name>`
before any edit. 4 were genuine delisted priced rivals (`luminar/uspto-trademark-monitor`,
`crawlerbros/uspto-trademark-search-scraper`, `crawlerbros/euipo-trademark-design-search-scraper`,
`barefoot_grade/uspto-trademarks-scraper`), rephrased past-tense with the standard inline delisted
note, surrounding price prose kept as the historical record. The 5th,
`parseforge/ziprecruiter-scraper`, is a real dead handle but a **scope-exclusion** mention rather
than a price claim, and it appears TWICE (the exclusion list plus a back-reference parenthetical)
-- the exact shape that bit court-records-scraper at c2833; grepped first, disclosed once at the
list mention, which covers both since they share a paragraph. The 6th, `owner/slug`, is
**CONFIRMED the literal placeholder-prose false positive that c2834 and c2835 both predicted in
advance** -- the phrase is "by full `owner/slug` handle", never an Apify listing -- left untouched,
same as on court-records-scraper. Shipped build 0.1.98 (package 0.1.29 -> 0.1.30), README-only;
live README verified **byte-identical** (88,496 == 88,496) via `versions[0].sourceFiles`.
**Verified purely corrective with a real before/after `check-price-superiority` run:** 2714
compared / 1040 cheaper / 0 undisclosed identical on both sides, fleet `gone` 65 -> 60 and
`gone_disclosed` 50 -> 55 -- exactly -5/+5, no existing verdict moved. Guards after:
`check-charges` 27/0/0, `check-registry-fields` 0 drift, `check-own-price-prose` 27/0.

**Blockers: none.** Flags for next cycle, all in `queue.md`: (a) a real MEDIUM buyer-facing gap the
audit surfaced -- `startsWithPrefix` is STRICTER than TMview's own matching in the harmful
direction (TMview folds diacritics and returned a slashed-O `COFFE` for "coff"; our NFKC-only
`stripLead()` does not decompose U+00D8, so the mode drops a row upstream considered a match --
same class of harm as c2500's defect, but a missing feature rather than a false claim, with the
exact fix shape and the NFD-alone-won't-work trap written down); (b) add a `trademark-search-
scraper` probe to `bin/vocab-screen` -- it would be the 18th but the FIRST needing a cookie-primed
session, since TMview returns a non-JSON empty body to the bare POST `vocab-screen`'s helpers send;
(c) 2 LOW `tmTypes` doc nuances (`3-D` is an upstream alias group that also returns `3D shape`
rows; the "known incomplete" warning now has a measured number -- 15,544 of 151,551 rows, 10.3%,
unaccounted by the 10 confirmed values). **`steam-reviews-scraper` (7 lines) is the only file left
in c2832's dead-handle start-here set**; re-pull a fresh `GONE` list rather than reusing
`c2832_gone_handles.txt` (c2835's regex widening made its classifications stale, and reported line
numbers drift -- grep the handle, do not trust the line). Standing: $0 revenue after 2836 cycles;
Polar checkout deferred by owner decision; MCP #3 closed-for-builds (gated on dates:
clinicaltrials 2026-11-12+, google-news 2026-12-05+); niche-hunting on cooldown to ~2026-12-26.

---

### Previous cycle (c2835) status, preserved

Updated: 2026-11-07 UTC by cycle 2835 (claude-sonnet-5). QUALITY slot (2835 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `git-maintain` in 1c, cycle 2836). `audit-due --all`
had 1 real backlog item -- `enum_audit` on `hacker-news-scraper` (336c gap, DUE) -- closed this
cycle, now NONE DUE fleet-wide again, all 16 types. `inbox-triage new` NONE UNTRIAGED of 74.
`bin/revenue` $0 booked, 27 Actors, 50 users, 812 runs30d (809 ext_ok / 3 ext_bad). Services all
active; `/`, `/pricing`, `/tools`, `/blog` all 200. Spend: one build (~$0.005, hacker-news-
scraper README fix); the enum_audit and all `check-price-superiority` verification were $0
read-only. No owner email warranted. `check-doc-size`: both `state/STATUS.md` (138.5KB/1890
lines) and `tasks/queue.md` (107.5KB/1257 lines) are TRIM SOON, not yet DUE, despite prior
cycles flagging c2835 to take the trim pre-emptively -- deferred again in favour of the DUE
audit plus the dead-handle work below, which was correctly-scoped real work; next QUALITY slot
(c2838) should trim if either reads TRIM DUE or SOON again by then.

**THE WORK: two items on the same Actor, since the one real audit-backlog entry
(`hacker-news-scraper`) was also next on the c2832 dead-handle cleanup list. (1) Closed the DUE
`enum_audit`.** `bin/vocab-screen hacker-news-scraper` re-verified the `tags` vocabulary live --
all 7 documented values (story/comment/poll/ask_hn/show_hn/job/front_page) resolve against
Algolia's HN Search API with real nonzero `nbHits` -- **this was the FIRST time this probe has
ever run for this Actor** (added cycle 2512, after the c2499 enum_audit, so this closes a
never-probed gap, not just a staleness recheck, same shape as c2521's finding for other
Actors). Also re-verified `sortBy` (relevance/date) live, matching c2499's own method and
mapping (main.js:47) exactly, and git-logged every `.actor/input_schema.json` commit since 1307
to confirm neither enum's values have changed (only defaults/prefills did, at 83f4ba55). ALL
CLEAN, no drift. Recorded in `state/audit_dates.json` (`enum_audit`: 2499 -> 2835).
**(2) Fixed `hacker-news-scraper`'s 6 `GONE` dead-handle lines, c2832's start-here list.** All 6
confirmed 404 live first. 3 were genuine dead listings never before disclosed --
`bovi/hacker-news-scraper`, `darknezz/sentiment-analyzer`, `luminar/hackernews-scraper-monitor`
-- rephrased past-tense with the standard `(**delisted -- the Apify API returned 404 for this
Actor on 2026-11-07**)` inline note. **1 was already disclosed in prose but missed by the
automated DEAD_DISCLOSED detector on a wording gap:** `wearefluent/hn-search`'s own sentence
said "is genuinely 404", and the regex only matched the literal substring "is 404" -- fixed by
widening it to `is (?:\w+ )?404` in `bin/check-price-superiority`, verified fleet-wide via a
full before/after sweep (only this one line's classification changed, `gone` 69->68 that step,
2714/1040/0 otherwise byte-identical) before touching any README. **2 are a confirmed new
instance of the GitHub-repo-name false-positive class flagged in advance last cycle:**
`omcljs/om` and `reagent-project/reagent` (README.md:123) are real ClojureScript GitHub repos
named as an example of what a comment's own text can link to, never Apify Store listings --
left untouched, same reasoning as c2833's `owner/slug` finding (confirmed 404 like any invented
string would be, but never a real handle). Shipped build 0.1.105 (package.json 0.1.28 ->
0.1.29), README-only; live README verified byte-identical (90,069 == 90,069) via
`versions[0].sourceFiles`. Final fleet sweep: 2714/1040/0 unchanged, `gone` 69 -> 65 (-4: the 3
new disclosures plus the regex-fix catch), `gone_disclosed` 46 -> 50. Per-Actor guards:
`check-charges` 1/0/0, `check-registry-fields` 0 drift, `check-own-price-prose` 27/0, all clean.

**Not done, flagged for the next cleanup cycle:** `steam-reviews-scraper` (7 lines) and
`trademark-search-scraper` (6 lines, one of which, `owner/slug` at README.md:150, is almost
certainly the SAME placeholder-prose false positive already confirmed on court-records-scraper
-- verify before editing) are next on the c2832 start-here list; 13 of 83 lines will remain
after both. The regex widening above may also newly reclassify a handful of other files' lines
as `gone_disclosed` -- this cycle's fleet sweep already reflects that (65 vs 69), so the next
cleanup cycle should re-pull a fresh `GONE` list rather than reuse c2832's now-stale one.

**Blockers: none.** Standing: $0 revenue after 2835 cycles; Polar checkout deferred by owner
decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+, google-news
2026-12-05+); niche-hunting on cooldown to ~2026-12-26.

---

### Previous cycle (c2834) status, preserved

Updated: 2026-11-07 UTC by cycle 2834 (claude-sonnet-5). Regular slot (2834 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `git-maintain` in 2c, cycle 2836). `audit-due
--all` had 1 real backlog item -- `enum_audit` on `court-records-scraper` (336c gap, DUE) --
closed this cycle, now NONE DUE fleet-wide again, all 16 types. `inbox-triage new` NONE
UNTRIAGED of 74 -- re-read both open owner threads visible in raw `inbox list` (the
`court-records-scraper` hCaptcha/CourtListener-token ask and the Apify `/v2/store` Nov-15
forward); both remain fully actioned (`CL_API_TOKEN` confirmed present in `secrets/env`,
40 chars, matches the token the owner sent 2026-10-28). `bin/revenue` $0 booked, 27 Actors,
50 users, 812 runs30d (809 ext_ok / 3 ext_bad). Services all active; `/`, `/pricing`,
`/tools`, `/blog` all 200. Spend: one build (~$0.005, apple-podcasts-scraper README fix);
the enum_audit (`bin/vocab-screen`, 5 live GETs) and all verification were $0 read-only.
No owner email warranted.

**THE WORK: two items, since the preflight audit backlog had exactly one real entry and it
was quick. (1) Closed the DUE `court-records-scraper` `enum_audit`.** `bin/vocab-screen
court-records-scraper` re-verified the `courts` vocabulary live: CourtListener
`/api/rest/v4/courts/` count 3359 == baked snapshot (harvested 2026-09-19); live
`in_use=true` count 472 == snapshot's claimed 472; 5 spot-checked ids (scotus, ca9, cand,
nysd, cacb, ohctapp1) plus a negative control (`zzyzxqplonknonexistentcourtfetchsmithtest`,
correctly 404) all match their baked in_use/jurisdiction flags exactly. **ALL CLEAN -- no
drift since c2498 (1191c/~25d stale before this cycle).** Recorded in
`state/audit_dates.json` (`enum_audit`: 2498 -> 2834, with a note); `audit-due --all` now
reports NONE DUE fleet-wide again, all 16 types, 7th clean preflight running since c2828.

**(2) Continued the dead-handle cleanup queue: `apple-podcasts-scraper`'s 8 `GONE` lines,
all genuine 404s, no false-positive class this time.** Each of the 8 handles
(`crawlerbros/applepodcasts-listennotes-scraper`, `crawlerbros/itunes-podcast-scraper`,
`crawlerbros/itunes-podcasts-scraper`, `crawlerbros/podchaser-scraper`,
`datagleaner/podcast-email-finder`, `himanshu-data/audio-podcast-transcriber`,
`neuro-scraper/itunes-podcast-host-email-and-phone-number-scraper`,
`neuro-scraper/itunes-podcast-host-phone-number-scraper`) was re-confirmed 404 live via
`GET /v2/acts/<owner>~<name>` before editing, per the procedure c2832 wrote down. Unlike
`court-records-scraper` last cycle, none of the 8 turned out to be a placeholder/shorthand
false positive -- all are real dead Store listings named in dense comparison prose. Grepped
each handle across the whole README first to check for a second recurrence (the shape that
bit court-records-scraper's line-224 summary); none found here, each appears exactly once.
Rephrased each in place with the same `(**delisted -- the Apify API returned 404 for this
Actor on 2026-11-07**)` inline note used on court-records-scraper, keeping the surrounding
price/feature prose as the historical record rather than deleting it. Shipped build 0.1.119
(package.json 0.1.38 -> 0.1.39), README-only; live README verified **byte-identical**
(72,417 == 72,417) via `versions[0].sourceFiles`. **Verified purely corrective with a real
before/after `check-price-superiority` run:** 2714 compared / 1040 cheaper / 0 flagged
unchanged both before and after, fleet `gone` 77 -> 69 and `gone_disclosed` 38 -> 46 --
exactly -8/+8, no existing verdict moved. Per-Actor guards after: `check-charges` 1/0/0,
`check-registry-fields` 0 drift, `check-own-price-prose` 27/0, all clean.

**Not done, flagged for the next cleanup cycle:** two of the remaining 19 `GONE` lines look
like they may be the same false-positive class found on court-records-scraper, and should be
read in context before editing rather than assumed real: `trademark-search-
scraper/README.md:150` names `owner/slug` (the exact literal-placeholder token that was a
false positive before), and `hacker-news-scraper/README.md:123` names `omcljs/om` and
`reagent-project/reagent` together, which read like ClojureScript library names rather than
Apify Store handles.

**Blockers: none.** Standing: $0 revenue after 2834 cycles; Polar checkout deferred by owner
decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+, google-news
2026-12-05+); niche-hunting on cooldown to ~2026-12-26. Both `STATUS.md` and `tasks/queue.md`
remain TRIM SOON (grew again this cycle rather than being trimmed) -- re-check
`check-doc-size` fresh next cycle; a QUALITY slot should take the trim if either now reads
TRIM DUE. **`steam-reviews-scraper` (7 lines) is next on the c2832 start-here list**, same
procedure: re-confirm each handle 404 live first, check for the false-positive shape, then
`trademark-search-scraper` (6), `hacker-news-scraper` (6) -- 19 of 83 lines will remain after
steam-reviews.

---

### Previous cycle (c2833) status, preserved

Updated: 2026-11-07 UTC by cycle 2833 (claude-sonnet-5). Regular slot (2833 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `git-maintain` in 3c, cycle 2836). `audit-due
--all` NONE DUE fleet-wide, all 16 types (6th clean cycle running since c2828). `inbox-triage
new` NONE UNTRIAGED of 74. `bin/revenue` $0 booked, 27 Actors, 50 users, 812 runs30d (809
ext_ok / 3 ext_bad). Services all active; `/`, `/pricing`, `/tools`, `/blog` all 200. Spend:
one build (~$0.005); all else was $0 read-only (6 Apify `GET /v2/acts/<handle>` liveness
checks, 2 full `check-price-superiority` live sweeps). No owner email warranted.

**THE WORK: worked the top of c2832's revised dead-handle start-here list --
`court-records-scraper`'s 8 lines, all now resolved.** Of the 8 `GONE` lines
`state/audit_data/c2832_gone_handles.txt` listed for this file, 6 were genuine dead Apify
handles (all re-confirmed live via `GET /v2/acts/<owner>~<name>` -> 404 before editing, per
the file's own procedure): `cloudastra-technologies/india-court-case-search`,
`crawlerbros/case-law-scraper`, `crawlerbros/top-class-actions-scraper`,
`dami_studio/courtlistener-cases-scraper`, `hipersoft/courtlistener-scraper`,
`parseforge/caselaw-access-scraper`. Each was rephrased in place, copying the worked-example
shape from `google-news-scraper`'s `simple.actors/google-search` fix: a bold inline
`(**delisted -- the Apify API returned 404 for this Actor on 2026-11-07** ...)` note, with the
surrounding price/feature claim converted to past tense rather than deleted (the README's own
stated principle: a disclosure paragraph citing a dead rival as current evidence is a stale-
prose bug, not a reason to erase the historical comparison). **Two of those six recur in a
second place** (`README.md`'s own "what we do not claim" summary at line 224 restates
`dami_studio`, `hipersoft` and `parseforge/caselaw-access-scraper` as current every-tier/paid-
tier undercutters) -- fixed both occurrences of each so the file does not contradict itself
after the first-mention edit.

**The other 2 of the 8 were NOT dead handles at all -- a second false-positive class the
c2832 filter still misses, found and verified before touching anything.** `owner/slug`
(README.md:214) is literal placeholder prose ("71 carry no full `owner/slug` handle on this
page"), and `parseforge/harris-county` (README.md:174) is an in-sentence shorthand back-
reference to `parseforge/harris-county-court-records-scraper`, named in full earlier in the
same sentence -- neither was ever a real Apify listing. Confirmed by the same live 404 check
used for the other six (both happen to also 404, as any invented string would, which is why a
naive "is it dead" read would wrongly count them as fixable). **Not fixed in the checker this
cycle** (time-boxed, see queue) -- `is_apify_handle()` has no way to know a backtick token is
an abbreviated repeat of a handle already spelled out nearby, and a quick heuristic risks a
false negative on a real short handle; queued precisely instead of rushed.

**Shipped as build 0.1.81** (`court-records-scraper` package.json 0.1.27 -> 0.1.28),
README-only, no code diff. Live README verified **character-identical** (77,641 == 77,641 --
measured by decoded character count, not raw bytes, since the file's em-dashes are 3-byte
UTF-8 and a byte-count comparison across local-vs-API would be a false mismatch) via
`GET /v2/actor-builds/<id>`, comfortably under the ~100k truncation wall. **Verified purely
corrective with a real before/after `check-price-superiority` run, not a self-test:** 2714
compared / 1040 cheaper / 0 flagged both before and after (byte-identical to c2832's own
published numbers -- no existing verdict moved), with the fleet-wide `gone` count dropping
83 -> 77 and `gone_disclosed` rising 32 -> 38, exactly +6/-6 as expected. The 2 remaining
`court-records-scraper` `GONE` lines in that output are now only `owner/slug` and
`parseforge/harris-county`, matching the false-positive finding above.

**Blockers: none.** Standing: $0 revenue after 2833 cycles; Polar checkout deferred by owner
decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+, google-news
2026-12-05+); niche-hunting on cooldown to ~2026-12-26. Both `STATUS.md` (~17c headroom at
c2832) and `tasks/queue.md` (~20c headroom at c2832) remain TRIM SOON -- this cycle added to
both rather than trimming, so re-check `check-doc-size` fresh next cycle rather than trust the
c2832 figures; a QUALITY slot should take the trim if either now reads TRIM DUE.
**`apple-podcasts-scraper` (8 lines) is next on the c2832 start-here list**, same procedure:
re-confirm each handle 404 live first, then `steam-reviews-scraper` (7), `trademark-search-
scraper` (6), `hacker-news-scraper` (6) -- 47 of 83 lines will remain after apple-podcasts.

---

### Previous cycle (c2832) status, preserved

