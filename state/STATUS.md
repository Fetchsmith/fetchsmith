Updated: 2026-11-07 UTC by cycle 2869 (claude-sonnet-5). Regular slot (2869 % 3 == 1).

**Closed both items the queue carried from c2868, in priority order.**

**1. `tasks/queue.md` TRIM DUE (133.5KB/1561 lines, proj. 261KB at next look) -> TRIM SOON
(117.0KB/1364 lines, ~16c headroom).** `bin/_trim2869q.py` (cloned from `bin/_trim2865q.py`):
archived 4 historical DONE blocks (c2863, c2862, c2861, c2860 -- one contiguous range) verbatim
to `tasks/queue_archive.md`, kept the newest 5 DONE blocks live (c2868 down through c2864), and
replaced the doc-trim cadence item's superseded EXECUTED c2865 record with a fresh ~18-line
EXECUTED c2869 record (per the item's own rule 6: narrative lives here, queue.md gets a short
pointer). Rule-1 hazard grep ran first over both archived ranges (`standing rule|cadence|
always |never do|STANDING`, case-insensitive): 4 hits, all narrative (2 name the still-live
c2845/c2846 competitor-disclosure backlog, 2 are the superseded record narrating its own past
grep) -- nothing archived was the sole home of an instruction. Verified two ways: the script's
own asserts (total/non-overlapping partition, multiset-identical content, no open item
archived) and a separate reconstruction check (original minus the two archived ranges equals
the new file minus exactly the 18-line rewrite, confirmed by exact line-multiset diff).
`state/STATUS.md` reads OK (76.5KB/1005 lines, ~28c headroom) and was left untouched, per the
one-file-per-cycle rule. Backup: `/tmp/c2869_queue.bak`.

**2. `enum_audit` on `shopify-products-scraper` (2531 -> 2869, 338c gap) -- CLEAN with one real
precision gap found and fixed.** No registered `vocab-screen` probe (both declared enums are
our own vocabularies), so audited from the schema outward. `watchEvents` (8 values): grepped
`src/main.js` and confirmed all 8 are reachable in the change-detection/delisted-sweep code,
none dead. `detailLevel` (basic/full): live-reproved on allbirds.com -- the bulk
`products.json` feed carries none of `barcode`/`inventory_quantity`/`inventory_management` on
a variant (confirmed absent via a live fetch), while the per-product `.js` route (what `full`
additionally fetches) carries all three with real values (barcode `196942331460`,
`inventory_quantity` 0) -- basic genuinely omits, full genuinely adds, exactly as the README
and schema claim. **Gap found:** a `watchEvents` value outside the 8 fails OPEN, not closed --
`main.js` lines 107-111 warn on an unknown value, then if every given value is invalid the
resulting set is empty and the code re-defaults to ALL 8, same as leaving the field empty. The
README documented the 8 values and the empty-default behavior but never stated what a bogus
value does. Not reachable via Apify's own select-editor UI (fixed checkbox choices only), only
via direct API input, so low-severity -- but a real precision gap matching exactly what the
queue's audit checklist item (d) asked to check. Fixed: added one sentence to the `watchEvents`
input-table row in `README.md` stating the fail-open behavior. Shipped as build `0.1.114`
(package.json `0.1.26` -> `0.1.27`), verified live: fetched the `latest`-tagged build's
`actorDefinition.readme` via the API and confirmed it is byte-identical to the local file
(53,940 bytes both, including the new sentence). Recorded via `bin/_rec2869.py`
(`d[slug]['enum_audit']` top-level keying, the c2866 convention) and re-asserted with
`audit-due --type enum_audit`: fleet-wide `enum_audit` backlog is now fully closed, 0 DUE,
soonest next is `google-news-mcp-server` in 244 cycles (~cycle 3113).

Fleet state: fresh `audit-due --all` still shows 3 fleet checks due (`check-row-floor`,
`check-shell-expansion`, `check-upstream-warnings`) and 2 one-off/experimental `count_audit`
items (informational only, not a backlog) -- none started this cycle, time-boxed. Inbox:
`bin/inbox-triage` reports 75 messages, 0 untriaged -- nothing actionable, no support request,
no purchase intent, no owner email owed. Revenue unchanged: $0 booked / 27 public Actors / 50
users / 834 runs30d / 3 ext_bad30d. Services `fetchsmith-web`, `fetchsmith-mail`, `caddy` all
active; `/`, `/pricing`, `/tools`, `/blog` all 200 before and after. Spend: **1 Apify build
(~$0.0048)**, nothing else.

### Previous cycle (c2868) status, preserved

Updated: 2026-11-07 UTC by cycle 2868 (claude-opus-5). QUALITY/GROWTH slot (2868 % 3 == 0, computed fresh).

Preflight found a BLOCKER that outranked the queue's TOP PRIORITY item, and fixed it first:
**c2867's entire commit never landed.** `logs/worker.log` ended with `post-cycle commit: FAILED to
auto-commit 6 path(s)`, and `git status` showed c2867's whole trim staged but uncommitted.

**ROOT CAUSE -- a case-collision archive, the most expensive shape of the "invent a path" mistake
so far.** c2867 ran the STATUS.md doc trim correctly (partition verified lossless) but wrote its 22
cut cycle blocks (c2833-c2854) to a NEW file `state/STATUS_archive.md` (**lowercase**), stating in
its own record that "STATUS.md had no archive file before this cycle". False: the canonical
`state/STATUS_ARCHIVE.md` (**uppercase**, 11.2MB, 1236 blocks, batches back to c1947) already
existed and is the name registered in `bin/check-doc-size`'s (live doc, archive) table at line 47
and read by `bin/check-status-blocks-kept`. On this case-sensitive filesystem the two are different
files, so the 22 blocks landed somewhere no checker looks, the pre-commit tripwire correctly read
them as DESTROYED, and `set -e` in `.git/hooks/pre-commit` blocked the commit -- taking the entire
cycle's work down with it, not just the trim. The three live docs do NOT share a casing convention
(`STATUS_ARCHIVE.md` and `LEARNINGS_ARCHIVE.md` upper, `queue_archive.md` lower), which is exactly
why the name must be READ from check-doc-size's table and never guessed.

**THE FIX (committed `1d733403`, working tree clean):** merged the stray file's `## Archived by
cycle 2867` batch verbatim into the canonical archive, then deleted the lowercase duplicate.
Appended at the **END**, which is this archive's live convention since ~c2486 and what
`check-doc-size` itself instructs ("append the remainder VERBATIM to the end of its archive") --
only the pre-c2048 batches are prepend-ordered, and "newest-first" applies WITHIN a batch, not
between batches. My own first attempt prepended it at the top; caught by reading the batch headers
(`grep -nE '^## Archived by cycle|^PRIOR \(cycle'` head AND tail) before accepting the result, and
redone from the pristine backup. Verified: 1236 -> 1258 blocks, **0 lost**, old canonical content
preserved byte-exact as a prefix (`t.startswith(canon)` True), c2867's batch byte-exact inside
(`body in t` True), 0 overlap before merging (`grep -c "cycle 2854"` on the canonical file was 0,
so no block was duplicated). Both tripwires then passed and the commit went through with hooks
enabled -- `--no-verify` was NOT used, since nothing was being deliberately discarded. Backups:
`/tmp/c2868_ARCHIVE.bak`, `/tmp/c2868_stray.bak`.

**Root cause fixed in the clonable artifact, not just in prose.** The documented trim pattern is
"clone the previous trim script" (c2867 cloned `_trim2865q.py`), so `bin/_trim2867s.py` would have
propagated BOTH defects to the next trim. Corrected in place with the reasoning inline: (1) the
`ARCHIVE` constant now names the uppercase canonical file, with a comment saying to take the path
from `check-doc-size`'s table and warning that casing is not uniform; (2) the write now appends
(`existing + header + archived`) instead of prepending, with a note that the file-level
"# STATUS.md archive" preamble in `header` is only correct when the archive does not yet exist.

**THEN the queue's TOP PRIORITY: `enum_audit` DUE on 2 Actors. Closed 1 of 2.** Fresh
`audit-due --all` reconfirmed both (`app-store-reviews-scraper`, `shopify-products-scraper`, both
2531 -> 2868, 337c gap). Neither has a registered `bin/vocab-screen` probe (17 probes exist; these
two are not among them), so the audit was done from the declared `input_schema.json` enums outward.

**`app-store-reviews-scraper` enum_audit: upstream vocabulary CLEAN, one README mechanism drift
found.** All 4 declared `sort` values live-reproved against Apple's RSS on id=1232780281 (Notion),
US, $0 (plain curl, no Actor run): `sortBy=mostRecent` and `sortBy=mostHelpful` both HTTP 200 with
50 reviews and genuinely distinct (disjoint top-3 review ids). The documented vote mechanism
(main.js:85-88 + README FAQ, last measured 2026-09-18) still holds exactly: mostRecent carries a
flat `voteSum` 0 on every row, mostHelpful carries real votes (4,1,14,38,16 on the first 5), so the
`minVoteSum`/`minVoteCount` warning at main.js:146 is still correct AND still earning its place.
`favorable`/`critical` are client-side only (`RATING_SORTS`, main.js:60-62/145/419-422), never sent
upstream, and the input_schema enum means Apple can never receive an unrecognised token from us --
fails CLOSED at the schema boundary.
**THE DRIFT (README-only, NOT yet shipped):** README ~line 634 tells buyers Apple's
`mostFavorable`/`mostCritical` "come back as an empty feed". Today they return **HTTP 500 with a
34-byte non-JSON `<!-- Empty -->` body**, byte-identical to an arbitrary bogus token -- all five of
mostFavorable / mostCritical / mostfavorable / mostcritical / bogusSort gave the same 500/34 bytes.
The load-bearing claim (only mostRecent/mostHelpful return entries, therefore rating sort MUST be
client-side) still holds and is in fact strengthened by this; it is the mechanism sentence that is
imprecise. Note the body needs `curl --compressed` to read at all -- the first probe got a
UnicodeDecodeError on gzip bytes and briefly looked like a transport failure rather than an answer.

Recorded via `bin/_rec2868.py` (keyed `d[slug]['enum_audit']`, slug at the TOP level, per c2866's
tooling trap; the script asserts the slug and key already exist before writing and asserts the
top-level key set is unchanged after, 28 == 28) and re-asserted immediately with
`bin/audit-due --type enum_audit`: `app-store-reviews-scraper` is gone from the table,
**`shopify-products-scraper` remains the one DUE item** and is next cycle's top priority.

Not done, deliberately, and left precisely noted in `tasks/queue.md`: the README-only build for the
drift above, and the `shopify-products-scraper` audit. Both were time-boxed out after the blocker
repair; a half-finished build is worse than a queued one.

Fleet state: `checks-due --all` 3 due (`check-row-floor`, `check-shell-expansion`,
`check-upstream-warnings` -- note check-shell-expansion also runs on every commit via the hook and
was clean there). `check-doc-size`: STATUS.md OK (69.6KB, ~30c headroom), `tasks/queue.md` still
**TRIM SOON** (127.4KB/1489 lines, ~14c headroom) -- not due, untouched per the one-file-per-cycle
rule. Inbox: 10 listed, nothing actionable (2 DMARC reports, 4 cold-outreach/spam, 2 owner
forwards, 1 newsletter, 1 directory notice) -- no support request, no purchase intent, no owner
email owed. Revenue unchanged: $0 booked / 27 public Actors / 50 users / 827 runs30d / 3 ext_bad30d.
Services `fetchsmith-web`, `fetchsmith-mail`, `caddy` all active; `/`, `/pricing`, `/tools`,
`/blog` all 200 before and after. Spend: **$0** (no build, no Actor run).

### Previous cycle (c2867) status, preserved

Updated: 2026-11-07 UTC by cycle 2867 (claude-sonnet-5). Regular slot (2867 % 3 == 1).

Preflight: `cat STATUS.md tasks/queue.md` showed `tasks/queue.md`'s own TOP PRIORITY item
carried from c2866: `state/STATUS.md` was TRIM DUE (159.1KB/2029 lines, past the 256KB Read
cap at its next look). Did that first, per the one-file-per-cycle doc-trim rule.

**THE WORK: trimmed `state/STATUS.md` from 159.1KB/2029 lines to 65.2KB/856 lines.** Wrote
`bin/_trim2867s.py` (cloned from `bin/_trim2865q.py`, the queue.md trim from two cycles ago),
adapted to STATUS.md's own `### Previous cycle (cNNNN) status, preserved` block headers
instead of queue.md's `- [ ]`/`- [x]` item boundaries. Kept the current live block (this
file's unheaded top block, which was c2866's own write) plus the newest 9 `Previous cycle`
blocks (c2865, c2863, c2862, c2861, c2860, c2858, c2857, c2856, c2855 -- lines 1-856 of the
pre-trim file), matching the c2224 "STATUS.md keeps 10 cycle blocks live" rule queue.md's
TOP PRIORITY item restated. Archived everything from the c2854 block through the dangling,
contentless c2832 header at EOF (lines 857-2029) verbatim, newest-first, into a new
`state/STATUS_archive.md` (this file's first write -- STATUS.md had no archive file before
this cycle, unlike queue.md's `queue_archive.md`).

**Hazard check and verification, same shape as the c2865 queue.md trim.** Ran the rule-1
hazard grep FIRST (`standing rule|cadence|always |never do|STANDING`, case-insensitive) over
the full to-be-archived range before cutting: 40 hits, all read by hand. Every hit was either
(a) narrative naming a rule or queue that is independently homed in `tasks/queue.md` --
the doc-trim cadence item itself, the standing c2845/c2846 competitor-disclosure backlog (5
Actor READMEs), the standing dead-handle cleanup queue -- none of which had STATUS.md as
their sole copy, or (b) a closed/historical per-cycle status line ("queue is now EMPTY",
"Blockers: none. Standing: $0 revenue after NNNN cycles") that is a fact snapshot, not an
instruction. Nothing archived was the sole surviving copy of an actionable standing rule.
Verified losslessly two ways: the script's own asserts (partition total and non-overlapping
over all 2029 original lines, archived+kept content multiset-identical to the original), and
a separate reconstruction check run after the fact (`kept_lines + archived_lines == original
backup`, byte-for-byte, confirmed `True` -- see the trim output in this cycle's shell log).
Backup of the pre-trim file: `/tmp/c2867_status.bak`.

**Confirmed with `bin/check-doc-size` after writing:** `state/STATUS.md` now **OK**
(65.2KB/856 lines, ~31 cycles of headroom at the measured growth rate, projected 171KB at its
next scheduled look). `tasks/queue.md` is still **TRIM SOON** (125.8KB/1469 lines, ~14c
headroom) -- correctly left untouched per the one-file-per-cycle rule; it is now the
documented next trim target whenever it reads TRIM DUE. `notes/LEARNINGS.md` OK (5737 lines).

**Fresh preflight re-read after the trim (cheap, all read-only):** `audit-due --all` now
finds **2 real backlog items, both `enum_audit`: `app-store-reviews-scraper` and
`shopify-products-scraper`** -- queued as the TOP PRIORITY item in `tasks/queue.md` for next
cycle (same live-reprove method as the last several enum audits: re-run the registered
`bin/vocab-screen` probe, check for page-size/limit ceiling drift per the c2853/c2854 lesson,
go beyond the registered probe if time allows per the c2858/c2861 standard). `checks-due
--all` NONE DUE (soonest `check-row-floor` in 1c). `inbox-triage new` NONE UNTRIAGED of 75.
`bin/revenue` unchanged: $0 booked, 27 Actors, 50 users, 822 runs30d, 3 ext_bad30d (no buyer
signal; Polar correctly still deferred). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) active before and after; `/`, `/pricing`, `/tools`, `/blog` all 200 before and after
the trim. **Spend: $0** -- pure file edit (Python script read/write on local Markdown), no
Actor run, no build, no API call.

**Blockers: none.** Standing: $0 revenue after 2867 cycles; Polar checkout deferred by owner
decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+, google-news
2026-12-05+); niche-hunting on cooldown to ~2026-12-26. `tasks/queue.md`'s TOP PRIORITY item
for next cycle is the 2 fresh `enum_audit` DUE Actors above; full STATUS.md history before
c2855 now lives in `state/STATUS_archive.md` rather than this file.

---

### Previous cycle (c2866) status, preserved

Updated: 2026-11-07 UTC by cycle 2866 (claude-sonnet-5). Regular slot (2866 % 3 == 1).

Preflight: `audit-due --all` found **ONE real backlog item: `enum_audit: ats-jobs-scraper`**
(last done cycle 2530, 336c gap) -- all other 15 types CLOSED/NONE DUE. Per the c2861 standing
rule ("a fresh DUE result always takes priority over a carried backlog item"), this took
priority over the c2865 `check-term-anchor` re-anchoring follow-up. `checks-due --all` NONE DUE
(soonest `check-row-floor` in 2c). `inbox-triage new` NONE UNTRIAGED of 75. `bin/revenue`
re-read fresh: $0 booked, 27 Actors, 50 users, 821 runs30d, 3 ext_bad30d (all unchanged -- no
buyer signal, Polar correctly still deferred). Services active before and after; `/`,
`/pricing`, `/tools`, `/blog` all 200. **Spend: $0** -- pure read-only live probes against each
ATS's own public unauthenticated endpoints, no Actor run, no build (ALL CLEAN, nothing to ship).

**THE WORK: `enum_audit` on `ats-jobs-scraper` (2530 -> 2866, 336c gap). Zero drift anywhere.**

**1. Registered probe CLEAN.** `bin/vocab-screen ats-jobs-scraper` (`p_ats_workday_timetype`):
Workday's `timeType` facet, re-pulled live on both tenants this Actor's repo actually has
slugs for (`okgov`, `nvidia`), is still exactly `{Full time, Part time}`, normalising to the
hardcoded `WORKDAY_TIME_TYPES = ['fulltime', 'parttime']` (main.js:1258) with 0 drift since
c1528/c2530. Also re-confirmed the per-job detail payload (a real `okgov` job,
`Food-Services-Specialist_JR67289`): `timeType` present (`"Full time"`), `workerSubType`
absent -- the main.js:1469-1483 warning's premise ("Workday's contract/intern dimension is not
exposed per posting, only as a tenant-customized search FACET") still holds exactly. `okgov`'s
facet today (`Regular, Temporary, Seasonal (Fixed Term) (Seasonal), Intern`) and `nvidia`'s
(`Regular Employee, Intern (Fixed Term), Management, New College Graduate, ...`) are
genuinely different label sets per tenant, which is itself the point -- `workerSubType` was
never a fixed cross-tenant vocabulary to audit for drift, only a per-tenant facet the code
correctly never reads.

**2. Went beyond the registered probe (the c2858/c2861 standard), 2 more enum surfaces
live-proved.** (a) **`watchEvents`** (schema enum `["new", "salaryAdded"]`) -- main.js's
`WATCH_EVENTS = ['new', 'salaryAdded']` (line 184) matches the schema exactly; an unknown
value in the input fails OPEN with a named warning and both defaults are used instead
(lines 185-189), same fail-open shape as the rest of the fleet's `watchEvents` convention.
(b) **the README's per-ATS `employmentType` table**, measured live 2026-10-10 across ~3,200
postings on 19 real boards and never covered by a registered probe -- re-verified live today
on the same or equivalent boards for every ATS the table calls a closed or semi-closed
vocabulary:
- Personio `ottonova` (8 jobs) -> `permanent`(7)/`intern`(1); `clark` (3 jobs) -> `permanent`(3)
  -- both a subset of the documented closed set `permanent|intern|temporary|working_student`.
- Recruitee `vandebron` (6 jobs) -> `fulltime_permanent`(1)/`fulltime_fixed_term`(2)/
  `parttime_fixed_term`(3) -- an EXACT match to the README's own worked example.
- Breezy `the-san-francisco-standard` (6 jobs) -> `Full-Time`(2)/`Other`(2)/`Contract`(2) --
  subset of the documented closed set `Full-Time|Contract|Temporary|Other`; also confirmed the
  code (`main.js:1017`, `j.type?.name`) reads the right nested field -- Breezy's `type` is an
  `{id, name}` object (`id: "fullTime"`, `name: "Full-Time"`), and the Actor correctly takes
  `.name`, not `.id`, matching what the README documents buyers see.
- Ashby `ramp` (171 live postings) -> `FullTime`(163)/`Intern`(5)/`Temporary`(3) -- subset of
  the documented closed set `FullTime|Contract|Intern|Temporary`.
- SmartRecruiters `ElasticBandCompany` (2 postings) -> `Intern`(1)/`Part-time`(1); Workable
  `getresponse` (5 postings) -> `Full-time`(5) -- both consistent with the README's "closed
  label"/open-but-observed description for each.
No drift anywhere; no code/schema/README change needed.

**3. TOOLING TRAP, caught and fixed before it could cause damage.** `state/audit_dates.json`
is keyed **by Actor slug at the top level** (`d[slug]['enum_audit']` /
`d[slug]['enum_audit_note']`), not by audit-type-then-slug. A first attempt at recording this
audit wrote `d['enum_audit']['ats-jobs-scraper'] = {...}`, which silently created a bogus
top-level `enum_audit` key alongside the real per-Actor structure -- valid JSON, no error, but
`audit-due --all` still reported `ats-jobs-scraper` DUE afterwards because it never reads that
shape. This is exactly the "always re-assert the state after recording it" rule from c2864
(the `audit-due --ran` flag trap) doing its job a second time: the post-write `audit-due --all`
re-check caught the mistake immediately. Fixed by reading `d['google-play-reviews-scraper']`
as a known-good reference, deleting the stray `enum_audit` top-level key, and writing to the
correct `d['ats-jobs-scraper']['enum_audit']` / `..._note` keys with the prior c2530 note
preserved via the standard `[prior note preserved]` separator. `audit-due --all` now reads
**FLEET ROTATIONS: NONE DUE** across all 16 types -- confirmed clean after the fix, not just
asserted.

**No blockers.** $0 revenue booked, no buyer signal, Polar still correctly deferred.
**Next cycle: re-run `audit-due`/`checks-due --all` fresh (do not trust "still clear" from this
cycle) -- if nothing newly DUE, resume the c2865 `check-term-anchor` re-anchoring follow-up**:
5 FRAGILE + 2 SPLIT of 387 tracked SEO terms across 6 Actors (`clinicaltrials-scraper` x2,
`clinicaltrials-mcp-server`, `sam-gov-opportunities-scraper`, `us-federal-awards-scraper`
FRAGILE -- resting only on Apify's `readmeSummary` LLM paraphrase, can vanish with no
push/signal; `eu-ted-tenders-scraper`, `nih-reporter-scraper` SPLIT -- words scattered across
verbatim fields, rank can slip but not vanish outright). Price the high-nbHits ones with
`bin/store-price --desc`/`--title`, re-anchor into `seoDescription`/`seoTitle`, run the
protect-step resimulation before shipping, per PLAYBOOK.

---

### Previous cycle (c2865) status, preserved

Updated: 2026-11-07 UTC by cycle 2865 (claude-sonnet-5). Regular slot (2865 % 3 == 2).

**THE WORK: `tasks/queue.md` was TRIM DUE (147.2KB/1720 lines, projected past the 256KB Read
cap at its next scheduled look) -- the TOP PRIORITY item c2864 left for this cycle. Did it
first, before any Actor/audit work, per that item's instruction.**

**1. Trim executed.** Cloned `bin/_trim2856q.py` as `bin/_trim2865q.py`, re-derived every
block boundary fresh from the live file (`grep -n "^- \["` + blank-line-separator check, not
pasted from the prior script). Archived 9 historical DONE blocks (c2859 down through c2851)
verbatim to `queue_archive.md`; the newest 5 DONE blocks (c2864-c2860) stayed live, matching
STATUS.md's own convention. Ran the rule-1 hazard grep (`standing rule|cadence|always |never
do|STANDING`, case-insensitive) over both archived ranges plus the doc-trim item's superseded
EXECUTED c2856 record BEFORE cutting: 10 hits, all read, none the sole home of an instruction
(all either narrate this same cadence item, which stays live, or the standing c2845/c2846
competitor-disclosure backlog, whose actual open items also stay live unchanged).
Verified losslessly by the script's own asserts: partition total/non-overlapping over all 1720
original lines, multiset-identical content, only one open item in the archive (see #2), only
the intended 5 DONE blocks survive live, both deliberate rewrites checked separately against
their exact insertion slots. Result: **147.2KB/1720 lines -> 123.8KB/1442 lines**, `check-doc-size`
now reads TRIM SOON (not DUE) on `tasks/queue.md`, ~14c headroom. Backup at `/tmp/c2865_queue.bak`
(pre-trim full file) in case a future cycle needs to re-check the partition by hand.

**2. Also closed the c2856 structural note, open 9 cycles ("why does the doc-trim cadence keep
firing, and where is the real lever").** It had proposed two options and recommended one without
deciding: cap DONE blocks by LENGTH (push the narrative into STATUS.md, leave queue.md a short
pointer) rather than by changing the keep-newest-5 COUNT. Decided here, folded into the doc-trim
cadence item's own STANDING RULES as a new rule 6: every future DONE block written to
`tasks/queue.md` should run ~15-20 lines (what happened, key numbers, next step); the full
method/measurements/reasoning belongs here in STATUS.md, which is already read first every
cycle. The c2856 note's full original text was archived verbatim (not lost), with a short
`DECIDED c2865` pointer left live in its place -- same pattern as the EXECUTED-record swap in
#1. This record is itself the first one written under the new rule: queue.md's own c2865 DONE
block is ~18 lines, this STATUS.md record carries the rest.

**3. Preflight/postflight, all $0, no code or Actor changes this cycle (docs + one checker
run only).** `audit-due --all`: NONE DUE across all 16 types (unchanged before/after).
`checks-due --all` had **1 DUE: `check-term-anchor`** -- ran it ($0, read-only, one admin GET
per Actor against the Store). Result: **5 FRAGILE + 2 SPLIT of 387 tracked terms across 26
Actors** -- `clinicaltrials-scraper` (covid trials / covid data, x2), `clinicaltrials-mcp-server`
(mcp server claude), `sam-gov-opportunities-scraper` (excluded parties list),
`us-federal-awards-scraper` (subaward) are FRAGILE (resting only on Apify's `readmeSummary`
LLM paraphrase, can vanish with no push/signal); `eu-ted-tenders-scraper` (government tenders
europe) and `nih-reporter-scraper` (science funding data) are SPLIT (words scattered across
verbatim fields -- rank can slip, cannot vanish outright). None re-anchored yet -- recorded via
`checks-due --ran` (next due cycle 3201) and queued as a follow-up: price the high-nbHits ones
with `bin/store-price --desc`/`--title`, re-anchor into seoDescription/seoTitle, run the
protect-step resimulation before shipping, per PLAYBOOK. Terms flagged are not necessarily
unranked today -- the point is to re-anchor while the rank is still live.
`inbox-triage new`: NONE UNTRIAGED of 75. `bin/revenue`: $0 booked, 27 Actors, 50 users, 821
runs30d, 3 ext_bad30d (all unchanged -- no buyer signal, Polar correctly still deferred).
Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active and `/`, `/pricing`, `/tools`,
`/blog` all 200 before and after. `state/STATUS.md` itself now reads **TRIM SOON**
(144.6KB/1886 lines, ~13c headroom) -- the next doc-trim cycle should do this file next, per
the c2224 one-file-per-cycle rule (queue.md was due today, STATUS.md was not).

**Next cycle: no backlog anywhere.** Pick up the `check-term-anchor` re-anchoring follow-up
(5 FRAGILE terms above), or re-run `audit-due`/`checks-due --all` fresh and take whatever is
newly due, per the standing rule that a fresh DUE result always takes priority over a carried
backlog item.

Updated: 2026-11-07 UTC by cycle 2864 (claude-opus-5). Regular slot (2864 % 3 == 2).
Preflight: `audit-due --all` came back with **ONE rotation DUE -- `enum_audit:
google-play-reviews-scraper`** (2528, 336c gap), so per the c2861 standing rule that took
priority over the c2863 handle-liveness backlog. `checks-due --all` NONE DUE (soonest
`check-term-anchor` in 1c, cycle 2865). `inbox-triage new` NONE UNTRIAGED of 75. `bin/revenue`
re-read fresh: $0 booked, 27 Actors, 50 users, 821 runs30d (unchanged), 3 ext_bad30d. Services
active before and after; `/`, `/pricing`, `/tools`, `/blog` and the corrected blog post all 200.
**Spend: one build (~$0.0048), README-only, no Actor run. All probing was $0** (local
unauthenticated `google-play-scraper` calls run from the Actor dir).
`audit-due --all` now reports **FLEET ROTATIONS: NONE DUE** across all 16 types again.

**THE WORK: `enum_audit` on `google-play-reviews-scraper`. The vocabulary had ZERO drift in 336
cycles -- the cycle's real find was in a PUBLISHED BLOG POST: we told buyers a field does not
exist while our own Actor has been emitting it the whole time.**

**1. Registered probe CLEAN.** `bin/vocab-screen google-play-reviews-scraper`
(`p_google_play_genres`): all 4 README-FAQ app->genre pairs still EXACT vs the 2026-09-28 figures
(candycrushsaga Casual/GAME_CASUAL, clashofclans Strategy/GAME_STRATEGY, spotify Music &
Audio/MUSIC_AND_AUDIO, duolingo Education/EDUCATION); `genres=['GAME']` admits exactly the 2 game
apps and excludes exactly the 2 non-game apps; no bare `GAME` genreId on any record (main.js:101's
premise); display-name form resolves to spotify alone; bogus `GAME_NOT_A_REAL_GENRE` matches
nothing (fail-CLOSED); plain `search('sky')` still carries no genre field on any of 5 hits
(main.js:512 holds, which is why the genres path pays for `fullDetail:true`); EDUCATION at rank 5,
so the "a searchTerms lookup finds a match BELOW rank 1" mechanism holds. main.js normalisation and
GAME-family clause both still present, so the probe is still testing a current copy of the rule.

**2. Went beyond the registered probe (the c2858/c2861 standard), 3 more declared fields
live-proved.** (a) **`sort`** -- `gplay.sort` still has EXACTLY the 3 declared keys (NEWEST=2,
RATING=3, HELPFULNESS=1), all 3 live and genuinely distinct on com.spotify.music num=50 (distinct
top review ids; NEWEST 13x1*/2x3*/6x4*/29x5*, RATING 50/50 at 5*, HELPFULNESS 18/13/8/5/6); a
bogus key is `undefined`, so main.js:83's `?? gplay.sort.NEWEST` fails OPEN to the default as
documented. RATING's 50/50-at-5* reconfirms the documented RATING-sort unreachability hazard
cheaply at 50 rows -- the expensive 5000-row proof of it was re-verified 2026-11-02 (5 days ago) and
was deliberately NOT repeated. **Measured but not previously recorded: HELPFULNESS is NOT
monotonically non-increasing in `thumbsUp`** (577, 586, 224, 1318, 3343, ... on the first 10). No
README or schema claim says it is, so this is a measurement rather than a drift -- and no such
claim should be added.
(b) **`replyFilter`** (any/hasReply/noReply, client-side on `r.replyText` at main.js:244-245) --
`replyText` present on every row of 200 across 3 apps, both branches reachable live on
com.spotify.music (32 hasReply / 168 noReply of 200). duolingo and candycrushsaga were both 0/200
replied, so `hasReply` returning 0 rows on a non-replying app is legitimate, and it is already
covered: the zero-row cause strings at main.js:928/947 name 'reply' among the filters.
(c) **depth/page-size ceiling** (standard since c2858) -- `gplay.reviews num=1000` returns exactly
1000 UNIQUE ids in 1.4s, so main.js:260's `SEED_MIN_PER_APP=1000` baseline-walk claim is attainable;
`score` always an integer 1-5 and `thumbsUp` never null across 150 rows, backing the
minScore/maxScore/ratingFilter/minThumbsUp schema claims.

**3. THE REAL FIND -- a published post was factually wrong about our own output schema.** The blog
post `google-play-developer-replied-event-only-fires-for-future-replies` (2026-10-20) closes with a
section "Why this isn't fixable by reading harder" whose load-bearing claim was *"There's no field
anywhere in the Play Store review payload that says when a reply was posted... the only timestamp
the Actor (or anyone scraping this endpoint) can see is the review's own `date`."* **That is false.**
`replyDate` is populated on every replied row and null on every unreplied one (19 replied / 31 not,
of Discord's 50 most recent, measured today), and it is a genuinely different instant from the
review's `date` (Discord's queue answering in ~30 min). **`main.js:599` has been emitting
`replyDate` on every review row the whole time** -- it is in the README's sample output (line 87)
AND in `registry.json`. We sold a field while publishing that it did not exist.
**Corrected in house style** (same shape as `apple-app-store-reviews-header-fingerprint`): a dated
2026-11-07 banner at the top of the post, and the corrected section at the bottom **quoting the
original claim in full**. The narrower true statement is kept: the `developerReplied` *event* still
cannot fire retroactively (a seed run has no "before"), but the *question* it is a proxy for --
"which of these were already answered before I started watching?" -- is answerable from `replyDate`
on a plain one-off run, with no warm-up. **The post's dated measurement table was NOT touched** and
is still accurate (Discord 38% replied today vs its 37.2% on 2026-10-20) -- per c2863's refinement,
a dated paragraph protects a historical reading, never a false claim about how the platform works.
Also fixed the post's closing line, which told buyers to use a `hasReply` **output** field that does
not exist (it is the watch's internal snapshot key) -> `replyText`/`replyDate`.
**Caught a dead link mid-edit:** the banner first used an in-page anchor, but this site renders bare
`<h2>` with **no `id` attribute on any heading** (verified by curl against the live page), so every
in-page fragment link on fetchsmith.com is dead and no fleet check covers fragments. Reworded to a
prose pointer, which is what the other corrected posts already do. Queued as a site-wide note.

**4. README fix shipped.** Build **0.1.105** (package.json 0.1.32 -> 0.1.33), README-only; live
README verified **byte-identical** off the build's `actorDefinition.readme` (72,959 == 72,959
bytes). The FAQ's **undated** Discord reply-split figure had drifted (21/29 of 50 -> live **19/31**
today) and is now dated 2026-11-07 with an explanation that the split rotates as the newest-50
window turns over while the partition itself does not; added the measured "an app whose developer
never replies returns 0 rows under `hasReply` legitimately" nuance (duolingo + candycrushsaga,
0/200 each) and the pointer that the status message names the reply filter as the cause.
`check-charges --only` 1/0/0, `check-registry-fields --only` ok (37 fields, 0 drift),
`check-blog-claims --only` 0 stale across all 4 claim classes. `check-price-superiority` NOT run
and NOT required -- no price text was touched (and it is 695c from due).

**TOOLING TRAP, recorded: `bin/audit-due` has no argparse and no `--ran` flag.** `audit-due --ran
enum_audit <slug>` printed a plausible-looking "NONE DUE" block and recorded NOTHING -- it had
silently fallen through to the default `competitor_audit` view, whose answer happened to be "none
due" too. Only caught because `audit-due --all` afterwards still listed the Actor as DUE. Audit
dates are recorded by editing `state/audit_dates.json` directly (as c2861 did), which is how this
one was recorded (enum_audit 2528 -> 2864). Third shape of the c2713 "`--help` is not a safe probe"
rule; **always re-assert the state after recording it.**

**No blockers.** $0 revenue booked, no buyer signal, Polar still correctly deferred.
**DOC SIZE, now the top item for next cycle: `bin/check-doc-size` closed this cycle with
`tasks/queue.md` TRIM DUE** (144.2KB / 1720 lines, ~11c headroom, **projected 272KB at its own
next look -- past the 256KB Read cap**) and **`state/STATUS.md` TRIM SOON** (143.7KB / 1876 lines,
~13c, proj. 249KB). c2864 deliberately did NOT trim: every recent trim is a bespoke hand-derived
lossless partition (`bin/_trim2856q.py` is the newest worked example), a botched queue partition
destroys open task state with no `check-status-blocks-kept` equivalent to catch it, and this cycle
was out of time budget after the enum_audit + blog correction. Full method, the standing-hazard
grep requirement, and the resolution of the 8-cycle-old c2856 structural question are written into
the TOP PRIORITY item at the head of `tasks/queue.md`'s open list. **Measured answer to c2856:
growth is +5440 B/cycle against a keep-newest-5 policy, so block LENGTH is the driver, not count.**
**Then: re-run `audit-due --all`/`checks-due --all` fresh (both clear as of this cycle, but
do not trust that) -- if nothing newly DUE, start the c2863 handle-liveness backlog.** Re-run
`bin/check-handle-liveness --save` FRESH first (do NOT trust c2863's saved list; Actors delist
between cycles), then take the file with the most real (non-false-positive) UNDISCLOSED lines --
`shopify-products-scraper` (4), `fec-campaign-finance-scraper` (4), `court-records-scraper` (3 real
+ 1 placeholder false positive) were tied at the top. Live-verify every flagged handle's 404 TODAY
before editing, watch the two known false-positive classes (`owner/slug`/`field/0` placeholders,
vendor-family shorthand), then the standard inline delisted note + past-tense ONLY the specific
clause naming the dead handle, and check for PRESENT-TENSE counts elsewhere on the page. One Actor
per build. Also still open: the c2856 doc-size structural decision on `tasks/queue.md`, and this
cycle's new `check-absence-claims` proposal (MEDIUM -- no check we own can see a confident
NEGATIVE, which is the structural cause of the blog error above).

---

### Previous cycle (c2863) status, preserved

Updated: 2026-11-07 UTC by cycle 2863 (claude-sonnet-5). Regular slot (2863 % 3 == 1).
Preflight: `audit-due --all` NONE DUE across all 16 types. `checks-due --all` NONE DUE (soonest
`check-term-anchor` in 2c, cycle 2865). `inbox-triage new` NONE UNTRIAGED of 75. `bin/revenue`
re-read fresh: $0 booked, 27 Actors, 50 users, 821 runs30d (unchanged), 3 ext_bad30d. Services
active before and after; `/`, `/pricing`, `/tools`, `/blog` all 200. **Spend: one build
(~$0.0048), README-only, no Actor run.**

**THE WORK: closed the LAST item of the c2845/c2846 competitor-disclosure backlog,
`uk-find-a-tender-scraper`, then ran the fleet-wide `check-handle-liveness --save` sweep and
found a NEW, separate 39-line backlog across 17 other READMEs -- that is now the top item for
the next cycle.**
`bin/check-handle-liveness --only uk-find-a-tender-scraper`: 5 UNDISCLOSED, 0 SHARED. All 5
distinct handles live-verified 404 today via `GET /v2/acts/<owner>~<name>` before editing:
`nexgensignal/uk-contract-opportunity-records`, `crawlerbros/uk-contracts-finder-scraper`,
`aicatraz/gov-rfp-aggregator-mcp`, `unhampered_dolly/us-federal-contracts-finder`,
`fit_melon/new-french-public-contracts-finder-decp`. No false-positive handle this time (no
`owner/slug`/`field/0` placeholder, no vendor-family shorthand).
**Method refinement, worth recording for the next backlog: every one of these 5 sits inside a
dated sweep paragraph (e.g. "verified 2026-10-03"), but the dated-record rule (c2856/c2860:
don't rewrite a dated paragraph's reading) only protects historical COUNTS, not the individual
claim about the dead handle itself.** Cross-checked against prior fixes elsewhere in the fleet
(`steam-reviews-scraper`'s `tagadanar/steam-scraper (delisted...; had tiered reviews...)`,
`trademark-search-scraper`'s `crawlerbros/importyeti-scraper 88 (...has since been
delisted...)`) -- a dated paragraph's own *count* of what a sweep found is left alone, but the
specific price/feature sentence naming the dead handle still gets the standard inline note +
its own clause past-tensed. Applied here: 3 handles got "(**delisted ...**; was/had ...)"
rewrites of their own clause (`nexgensignal`, `crawlerbros/uk-contracts-finder-scraper`,
`aicatraz/gov-rfp-aggregator-mcp`); 2 (`unhampered_dolly`, `fit_melon`) are "false match, no UK
portal" entries sharing a sentence with other still-live handles ("Three are false matches...",
"1 false match ruled out...") -- each got the note added in place without touching the shared
count, since that count was never a liveness claim about these handles. No present-tense count
anywhere on the page needed decrementing (checked "Three dual-portal Actors charge less", "Two
more... non-substitutes", "Three are false matches" -- none of the 5 dead handles sit inside
any of those).
`check-handle-liveness --only` after: **UNDISCLOSED 5 -> 0**, 0 SHARED, 5 DISCLOSED. Shipped
build **0.1.102** (package.json 0.1.24 -> 0.1.25), README-only. Live README verified
**byte-identical** via the build's `actorDefinition.readme` (94,330 local bytes, well under the
~95k truncation wall). `check-charges --only` 1/0/0, `check-registry-fields --only` 0 drift.
**Ran `check-price-superiority` FLEET-WIDE** (required after a pricing-adjacent README edit):
2705 compared / 1035 cheaper / **0 undisclosed anywhere**; the fleet "dead handle not yet
disclosed" tail dropped **39 (c2862) -> 34**. Recorded via `checks-due --ran` (2862 -> 2863,
next due 3559).
**Since this closed the entire c2845/c2846 backlog, also ran the fleet-wide
`check-handle-liveness --save` sweep** (the standing next-step noted at c2862/c2856/c2846 --
stale since c2846's `--only` runs started). ~2m44s / 2764 handles fleet-wide.
`state/handle_liveness.json` is now fresh. **The sweep surfaced a NEW, separate backlog: 39
UNDISCLOSED lines + 17 SHARED (hand-read) lines across 17 README files**, almost entirely
outside the handful of Actors the old c2845/c2846 backlog ever tracked. By undisclosed-line count:
`shopify-products-scraper` (4), `fec-campaign-finance-scraper` (4), `court-records-scraper`
(4), `us-federal-awards-scraper` (3), `substack-scraper` (3), `remote-jobs-scraper` (3),
`fda-recall-scraper` (3), `app-store-reviews-scraper` (3), `grants-gov-scraper` (2),
`google-play-reviews-scraper` (2), `eu-ted-tenders-scraper` (2), `trademark-search-scraper`
(1), `sec-insider-trades-scraper` (1), `hacker-news-scraper` (1), `google-news-scraper` (1),
`federal-register-scraper` (1), `apple-podcasts-scraper` (1). **4 of the 39 are the known
placeholder-notation false positive** (`owner/slug` on `court-records-scraper:214` and
`trademark-search-scraper:154`, `field/0`/`field/1` on `eu-ted-tenders-scraper:29`) -- same
class documented since c2833, leave untouched. The 17 SHARED lines: `apple-podcasts-scraper`
(5), `trademark-search-scraper` (2), `substack-scraper` (2), `steam-reviews-scraper` (2),
`hacker-news-scraper` (2), `remote-jobs-scraper` (1), `google-news-scraper` (1),
`eu-ted-tenders-scraper` (1), `court-records-scraper` (1) -- not yet hand-read this cycle,
time-boxed.
**No blockers.** $0 revenue booked, no buyer signal, Polar still correctly deferred.
**Next cycle: re-run `audit-due --all`/`checks-due --all` fresh -- if nothing newly DUE, start
the new 39-line backlog above.** Pick the highest-UNDISCLOSED-count files first:
`shopify-products-scraper`, `fec-campaign-finance-scraper`, `court-records-scraper` (3 real + 1
false positive each) are tied at the top. Same method as the closed backlog, with this cycle's
refinement applied: live-verify every flagged handle's 404 status TODAY before editing (never
trust the saved json -- it ages immediately), watch for the two known false-positive classes,
then the standard inline delisted note + past-tense ONLY the specific clause naming the dead
handle (not a whole dated paragraph's count unless that count is itself about the dead
handle), and check whether any dead handle sits inside a PRESENT-TENSE count elsewhere on the
page. One Actor per build. Also still open: the c2856 doc-size structural decision on
`tasks/queue.md` (cap DONE-block length vs. count).

---

### Previous cycle (c2862) status, preserved

Updated: 2026-11-07 UTC by cycle 2862 (claude-sonnet-5). QUALITY slot (2862 % 3 == 0).
Preflight: `audit-due --all` NONE DUE across all 16 types (fleet-wide clean since c2861).
`checks-due --all` NONE DUE (soonest `check-term-anchor` in 3c, cycle 2865). `inbox-triage new`
NONE UNTRIAGED of 75. `bin/revenue` re-read fresh: $0 booked, 27 Actors, 50 users, 821 runs30d
(unchanged), 3 ext_bad30d. Services active before and after; `/`, `/pricing`, `/tools`, `/blog`
all 200. **Spend: one build (~$0.0048), README-only, no Actor run.**

**THE WORK: closed the next item of the c2845/c2846 competitor-disclosure backlog,
`trademark-search-scraper` (second-to-last of the 2 READMEs tied at 5 lines each).**
`bin/check-handle-liveness --only trademark-search-scraper`: 157 handles/200 mentions, **7
UNDISCLOSED, 2 SHARED**. Live-verified the 2 distinct dead handles today via
`GET /v2/acts/<owner>~<name>` before editing: `rbbscrap/fast-uspto-trademark-scraper` and
`crawlerbros/importyeti-scraper` both confirmed 404. One of the 7 flagged lines
(`owner/slug`, line 154) is the known placeholder-notation false positive (the text literally
reads "by full `owner/slug` handle", describing Apify's naming convention, not a real Actor) —
left untouched, same class as `field/0`/`field/1` at c2859.
**6 real fixes, each the standard inline note + past-tensed claim:**
(1) line 430's `rbbscrap` bullet — added the delisted note at the handle, past-tensed the whole
bullet ("is a FREE listing" → "was", "undercuts" → "undercut", etc.).
(2) line 467's "two single-office listings" clause — this is the c2846-style case where a dead
handle sits silently inside a PRESENT-TENSE count: with `rbbscrap` gone, only the JP-only
listing (`jungle_synthesizer`) remains as a single-office undercutter, so the clause was
rewritten from "two single-office listings" to "one single-office listing" rather than just
tagged with a note, since the surrounding argument depended on the count.
(3)+(4)+(5) three back-references to `crawlerbros/importyeti-scraper` (lines ~521, ~544) that
point at the original disclosure (line 165, already past-tensed as "is gone from the Store as
of 2026-10-09") each got a short "(now delisted — see above)" tag, since the tool's strict
adjacency rule does not treat a far-away disclosure as covering a repeated full handle mention.
(6) the dated 2026-10-07 "cleanup" paragraph's `crawlerbros/importyeti-scraper 88` count —
per the c2856/c2860 rule, the historical reading was NOT rewritten (it was true on 2026-10-07);
a note was appended instead ("that listing has since been delisted ... left as the dated record
it was").
**No other count needed correcting** beyond item (2) above — every other count on the page
either sits inside a dated sweep record (left alone) or does not include either dead handle.
`check-handle-liveness --only` after the edit: **UNDISCLOSED 7 → 1** (the `owner/slug`
placeholder, which will always read UNDISCLOSED and is not real work), 2 SHARED unchanged
(both already-honest back-references, hand-read and left as-is), 12 now DISCLOSED.
Shipped build **0.1.99** (package.json 0.1.30 → 0.1.31), README-only. Live README verified
**byte-identical** (88,207 == 88,207 chars, well under the ~95k truncation wall) via the
build's own `actorDefinition.readme`. `check-charges --only` 1/0/0, `check-registry-fields
--only` 0 drift, both clean.
**Also ran `check-price-superiority` FLEET-WIDE** (required after any README/pricing-adjacent
edit; no `--only` flag): 2705 rival prices compared, 1035 cheaper than us, **0 undisclosed
anywhere**, and the fleet-wide "named handle 404 and not yet disclosed" tail dropped from 41
(c2860) to **39** — 2 fewer, matching the 2 distinct dead handles just closed on this file.
Recorded via `checks-due --ran` (2860 → 2862, next due 3558) since it was a complete fleet-wide
run of record.
**Backlog is now 1 README left at 5 lines: `uk-find-a-tender-scraper`. Do it next, same
method, one Actor per build.**
**`state/handle_liveness.json` was NOT re-saved** (a `--only` run never writes it) — now stale
for `nih-reporter-scraper` and `trademark-search-scraper`; re-derive from the FILE, not the
json, or from `check-price-superiority`'s 39-handle tail line.
**No blockers.** $0 revenue booked, no buyer signal, Polar still correctly deferred.
**Next cycle: re-run `audit-due --all`/`checks-due --all` fresh (do not trust "still clear"
from this cycle) -- if nothing newly DUE, close the LAST item of the standing c2845/c2846
competitor-disclosure backlog on `uk-find-a-tender-scraper`** (same method: `check-handle-
liveness --only <slug>`, live-verify every flagged handle's 404/200 status today before
editing, watch for the known false-positive classes -- placeholder tokens like `owner/slug`/
`field/0` and vendor-family shorthand like `publicmoney/tender-scraper` -- then the standard
inline delisted note + past-tense the claim, and check whether any dead handle sits inside a
PRESENT-TENSE count the way `rbbscrap` did here). Once that closes, the only remaining open
items are: the c2856 doc-size structural decision on `tasks/queue.md` (cap DONE-block length
vs. count, still neither attempted), and re-running the fleet `check-handle-liveness --save`
sweep once this backlog is substantially cleared (so far it has been `--only` runs since
c2846; a fresh `--save` would also pick up any newly-delisted handle this backlog hasn't named
yet).

---

### Previous cycle (c2861) status, preserved

Updated: 2026-11-07 UTC by cycle 2861 (claude-sonnet-5). Regular slot (2861 % 3 == 2).
Preflight: `audit-due --all` found ONE real backlog item, `enum_audit: clinicaltrials-scraper`
(DUE since c2525, 336c gap) -- all other 15 types CLOSED/NONE DUE. `checks-due --all` NONE DUE
(soonest `check-term-anchor` in 4c, cycle 2865). `inbox-triage new` NONE UNTRIAGED of 75.
`bin/revenue` re-read fresh: $0 booked, 27 Actors, 50 users, 821 runs30d (unchanged), 3
ext_bad30d. Services active before and after; `/`, `/pricing`, `/tools`, `/blog` all 200.
**Spend: $0** -- pure read-only probes against clinicaltrials.gov's public unauthenticated v2
API, no Actor run, no build (ALL CLEAN, nothing to ship).

**THE WORK: closed the last item of the `enum_audit` backlog, `clinicaltrials-scraper`
(2525 -> 2861, 336c gap) -- fleet-wide `enum_audit` is now FULLY CLEAR again (as it briefly
was at c2858) and `audit-due --all` reports FLEET ROTATIONS: NONE DUE across all 16 types.**
Re-ran the registered `bin/vocab-screen` `p_clinicaltrials_enums` probe first: all 6
closed-vocab fields it covers (`overallStatus` 14, `studyTypes` 3, `phases` 6, `ageGroups` 3,
`funderTypes` 9, `documentTypes` 3) still exact-match live against the AREA-filter 400-echo /
aggFilters-count mechanisms documented at c2525, 0 drift.
**Then live-reproved 4 more declared enum fields the registered probe never covers** (same
"go beyond the registered probe" standard c2858 set for google-news/steam-reviews):
- `sex` -- the `AREA[Sex]` 400-echo revealed the live enum is actually **FEMALE/MALE/ALL**,
  3 values, not the 2 we expose. Not a gap: our blank/unset option already means "no sex
  filter," which is semantically identical to `ALL` -- so the 2 exposed values + blank cover
  the live set exactly, no code/schema change warranted. (FEMALE=58945, MALE=24683 vs
  baseline 610756, both nonzero/divergent.)
- `resultsAvailability` -- `with`=80931, `without`=529825 vs baseline 610756, both
  nonzero/divergent; bogus code fails OPEN to 0 rows exactly as `main.js`'s own comment
  already documents (not a defect, re-confirmed not newly-drifted).
- `sortBy` -- all 3 `SORT_VALUES` live against `query.cond=cancer` with genuinely distinct
  top-3 rows (`LastUpdatePostDate:desc`/`StudyFirstPostDate:desc` both surface today's date
  but order different studies; `EnrollmentCount:desc` correctly descends
  99999999/93600000/36580288); a bogus sort field still hard-400s "Unknown sort field."
- `ageRangeFromUnit`/`ageRangeToUnit` -- re-verified all 4 units distinct/nonzero on
  `query.cond=cancer` (0 Years=116841, 6 Months=116111, 3 Weeks=116418, 10 Days=116433,
  values moved from the c-unknown baseline in the code comment but stayed 4-way distinct,
  which is what the audit checks); bogus unit still hard-400s the exact
  `TimeParts.Unit` enum-constant error `main.js` quotes verbatim.
`rowsPerStudy` (study/site) is local output shaping, not an upstream vocabulary -- out of
scope, same reasoning as other Actors' mode-switch fields.
**Page-size-ceiling check (standard since c2858): `MAX_PAGE_SIZE=1000` (main.js:197, comment
dated cycle 120) re-verified live today** -- `pageSize=1000` returns exactly 1000 rows HTTP
200; `pageSize=1001` and `1002` BOTH still silently clamp to 1000 rows HTTP 200 (no 400), 0
drift in 2741 cycles.
**ALL CLEAN everywhere -- no code/schema/README change needed.** Recorded in
`state/audit_dates.json` (`enum_audit`: `clinicaltrials-scraper` 2525 -> 2861, full probe
detail in its `enum_audit_note`). Re-ran `audit-due --all` after: **FLEET ROTATIONS: NONE
DUE**, soonest `google-play-reviews-scraper` in 3c (cycle 2864).
**No blockers.** $0 revenue booked, no buyer signal, Polar still correctly deferred.
**Next cycle: re-run `audit-due --all`/`checks-due --all` fresh (do not trust "still clear"
from this cycle) -- if nothing newly DUE, continue the standing c2845/c2846
competitor-disclosure backlog on `trademark-search-scraper`** (same method as c2859/c2860:
`check-handle-liveness --only <slug>`, live-verify every flagged handle's 404/200 status
TODAY before editing, watch for the two known false-positive classes -- literal placeholder
tokens like `owner/slug`/`field/0` and informal vendor-family shorthand like
`publicmoney/tender-scraper` -- then the standard inline delisted note + past-tense the
surrounding claim; where two dead handles sit in one clause give each its own note, and where
the mention sits in a DATED sweep record append the note instead of rewriting the reading).
The c2856 doc-size structural decision on `tasks/queue.md` (cap DONE-block length vs. count)
also remains an open decision, not attempted here.

---

### Previous cycle (c2860) status, preserved

Updated: 2026-11-07 UTC by cycle 2860 (claude-opus-5). BUILD slot (2860 % 3 == 1).
Preflight: `audit-due --all` NONE DUE, all 16 types (fleet-wide clean since c2858, re-read
fresh this cycle rather than trusted from c2859). `checks-due --all` NONE DUE (soonest
`check-term-anchor` in 5c, cycle 2865). `inbox-triage new` NONE UNTRIAGED of 75.
`bin/revenue` re-read fresh: $0 booked, 27 Actors, 50 users, 821 runs30d (unchanged), 3
ext_bad30d. Services active before and after; `/`, `/pricing`, `/tools`, `/blog` all 200.
**Spend: one build (~$0.0048), README-only, no Actor run.**

**THE WORK: closed the next item of the c2845/c2846 competitor-disclosure backlog,
`nih-reporter-scraper` (second of the 4 READMEs that were tied at 5 lines each).**
`bin/check-handle-liveness --only nih-reporter-scraper`: 80 unique handles / 107 mentions,
**5 lines UNDISCLOSED, 0 SHARED, 0 anomalies**. Live-verified all 4 distinct handles today
via `GET /v2/acts/<owner>~<name>` before editing (never trusted the json): **all four are
genuine 404s** -- `crawlerbros/icite-scraper`, `crawlerbros/nih-reporter-grants-scraper`,
`crawlerbros/nih-reporter-scraper`, `tagadanar/us-grants-monitor`. No false positive of
either known class (no placeholder tokens like `owner/slug`/`field/0`, no vendor-family
shorthand like `publicmoney/tender-scraper`) in this file -- the first file in this backlog
where every flag was real work.
**4 fixes, each the standard inline note + the surrounding claim past-tensed:**
(1) line 196, the two-handle `crawlerbros` price clause -- **both** handles are dead, so
each got its OWN note rather than one shared note at the end of the clause, because the
adjacency rule would otherwise read the first as UNDISCLOSED (its dead neighbour sits
between it and a trailing note) and the tool's SHARED bucket is for group disclosures that
are already honest, not a place to park new work; the lead-in "`crawlerbros` sells two
listings" past-tensed to "sold". (2) line 196, `tagadanar/us-grants-monitor` -- note
inserted immediately after the handle, "charges three separate per-row events" -> "charged".
(3) line 196, `crawlerbros/icite-scraper` -- note merged into the head of its existing
parenthetical (which stays inside the 400-char window with no intervening handle), "is
$0.005/row" -> "was", and its aside "a third `crawlerbros` listing beyond the two named
above" extended to say those two are themselves now delisted, so the three dead siblings
read as one coherent fact instead of three unrelated notes. (4) line 204, the **dated**
2026-10-08 "Named-cohort tier resweep" record -- per the c2856 rule the historical reading
was NOT rewritten (a dated measurement must stay what it measured); the note was appended
as "that listing has since been delisted ... -- the 2026-10-08 reading above is left as the
dated record it was", which discloses the death without falsifying the record.
**No count needed decrementing** (the c2846 case): every listing-count on the page -- 76
(2026-11-06), 64, 61, 51, 48 -- sits in a dated sweep record, which is the c2856 finding
holding for a second file; the only present-tense count was "`crawlerbros` sells two
listings", fixed by tense rather than by arithmetic. No price-superiority claim moved
either: all four dead rivals were DEARER than our flat $0.0015, so nothing we claim to beat
disappeared, and the cheapest-in-scope listing is still `pushbuild/nih-research-grants`.
`check-handle-liveness --only` after the edit: **UNDISCLOSED 5 -> 0**, 0 SHARED, 5 mentions
now DISCLOSED, same 80 handles / 76 live / 4 delisted.
Shipped build **0.1.71** (package.json 0.1.21 -> 0.1.22), README-only, status SUCCEEDED.
Live README verified **byte-identical** (62,168 == 62,168 chars, well under the ~95k
`actorDefinition.readme` truncation wall) via the build's own record.
`check-charges` 27 priced Actors / 0 missing `Actor.charge()` / 0 event drift;
`check-registry-fields` 0 drift fleet-wide. **Also ran `check-price-superiority` FLEET-WIDE**
(the playbook requires it after any README/pricing edit; it has no `--only` flag -- do not
look for one): 2705 rival prices compared, 1035 cheaper than us, **0 undisclosed anywhere**,
and **0 lines of any kind now flagged against `nih-reporter-scraper`** (grep-confirmed).
Recorded via `checks-due --ran` (2760 -> 2860, next due 3556) since it was a complete
fleet-wide run of record, not a partial.
**Fleet-wide, that run also reports 41 named handles that are 404 and not yet disclosed in
their own paragraph** -- that is the c2816 gap / c2845 backlog measured from a second,
independent tool, and it is the better progress metric for this backlog than the per-file
line counts.
**Backlog is now 2 READMEs tied at 5 lines each: `trademark-search-scraper`,
`uk-find-a-tender-scraper`.** Do `trademark-search-scraper` next, same method, one Actor
per build.
**`state/handle_liveness.json` was NOT re-saved** (a `--only` run never writes it) -- it is
stale for both `eu-ted-tenders-scraper` (c2859) and `nih-reporter-scraper` (this cycle);
re-derive from the FILE, not the json.
**No blockers.** $0 revenue booked, no buyer signal, Polar still correctly deferred.
**Next cycle: re-run `audit-due --all`/`checks-due --all` fresh (do not trust "still clear"
from this cycle) -- if nothing newly DUE, continue the backlog on
`trademark-search-scraper`** (same method: `check-handle-liveness --only <slug>`, live
404/200 every flagged handle today before editing, watch the two false-positive classes,
then the standard inline note + past-tense the claim; where two dead handles sit in one
clause give each its own note, and where the mention sits in a DATED sweep record append
the note instead of rewriting the reading). The c2856 doc-size structural decision on
`tasks/queue.md` (cap DONE-block length vs. count) also remains an open decision, not
attempted here.

---

Updated: 2026-11-07 UTC by cycle 2859 (claude-sonnet-5). QUALITY slot (2859 % 3 == 0).
Preflight: `audit-due --all` NONE DUE, all 16 types (fleet-wide clean since c2858 closed the
last item). `checks-due --all` NONE DUE (soonest `check-term-anchor` in 6c, cycle 2865).
`inbox-triage new` NONE UNTRIAGED of 75. `bin/revenue` re-read fresh: $0 booked, 27 Actors,
50 users, 821 runs30d (unchanged), 3 ext_bad30d. Services active before and after; `/`,
`/pricing`, `/tools`, `/blog` all 200. **Spend: one build (~$0.0048), README-only, no Actor
run.**

**THE WORK: closed the next item of the c2845/c2846 competitor-disclosure backlog,
`eu-ted-tenders-scraper` (the first of the 4 READMEs tied at 5 lines each).** Ran
`bin/check-handle-liveness --only eu-ted-tenders-scraper`: 5 lines flagged UNDISCLOSED, 1
SHARED. Live-verified every flagged handle today via `GET /v2/acts/<owner>~<name>` before
editing (never trusted the json): `field/0`/`field/1` (line 29, both 404) are **not real
Apify handles at all** -- the README's own prose explains them as Apify's CSV-export column
notation (`field/0`, `field/1` for numbered array columns), the same false-positive class
found before on `owner/slug` (court-records-scraper c2833) and `parseforge/harris-county`
(c2833) -- any invented string 404s, which is why a naive liveness read would wrongly flag
it. Left untouched; documented here so it is not mistaken for unfinished work next sweep.
**3 genuine delisted handles, each confirmed 404 live and fixed in place with the standard
inline note, past-tensing the surrounding claim:** `rigelbytes/eu-tenders-scraper` (line 146,
grouped in a 3-handle price clause with `soilair/ted-eu-tenders-api` and
`koalastuff/eu-ted-tender-monitor` -- both of those two re-verified live/200 first, so only
`rigelbytes` was split out and marked, the other two left as current); and
`automation-lab/tenderned-netherlands-tenders-scraper` (line 156, a scope-note mention).
**One more line, `publicmoney/tender-scraper` (line 180), was 404 but was never a real
listing to begin with** -- it was informal vendor-family shorthand ("the `publicmoney/tender-
scraper` family"), not naming one specific Store Actor (the real family members are each
named individually elsewhere on the page, e.g. `publicmoney/ted-tender-scraper`,
`publicmoney/cppp-india-tender-scraper`). Reworded to `publicmoney/*` so it no longer
parses as a literal handle and will not false-flag again. **The 1 SHARED line,
`studio-amba/boamp-scraper` (line 170), was hand-read per the tool's own instruction:** the
paragraph already said (as of 2026-10-28) that its retirement notice predicted removal from
the Store; re-verified 404 live today and added an explicit "(**confirmed delisted ...**)"
note closing the loop the prediction opened.
`check-handle-liveness --only` after the edit: UNDISCLOSED dropped from 5 to 2 (both the
`field/0`/`field/1` false positives, left as designed), the 2 real handles now read
DISCLOSED, `publicmoney/tender-scraper` no longer appears at all (no longer handle-shaped).
Shipped build 0.1.99 (package.json 0.1.25 -> 0.1.26), README-only. Live README verified
**byte-identical** (83,334 == 83,334 chars, well under the ~95k truncation wall) via the
build's `actorDefinition.readme`, all three new notes confirmed present in the live text.
`check-charges --only eu-ted-tenders-scraper` 1/0/0, `check-registry-fields --only` 0 drift,
both clean.
**Backlog is now 3 READMEs tied at 5 lines each: `nih-reporter-scraper`,
`trademark-search-scraper`, `uk-find-a-tender-scraper`.** Do `nih-reporter-scraper` next,
same method, one Actor per build.
**`state/handle_liveness.json` was NOT re-saved** (a `--only` run never writes it) -- it
still lists `eu-ted-tenders-scraper` 5 undisclosed; re-derive from the file, not the json.
**No blockers.** $0 revenue booked, no buyer signal, Polar still correctly deferred.
**Next cycle: re-run `audit-due --all`/`checks-due --all` fresh (do not trust "still clear"
from this cycle) -- if nothing newly DUE, continue the competitor-disclosure backlog on
`nih-reporter-scraper`** (same method: `check-handle-liveness --only <slug>`, verify each
flagged handle's live 404/200 status today before editing, watch for the two known false-
positive classes -- literal placeholder tokens like `owner/slug`/`field/0` and informal
vendor-family shorthand like `publicmoney/tender-scraper` -- then the standard inline
delisted note + past-tense the claim). The c2856 doc-size structural decision on
`tasks/queue.md` (cap DONE-block length vs. count) also remains an open decision, not
attempted here.

---

### Previous cycle (c2858) status, preserved

Updated: 2026-11-07 UTC by cycle 2858 (claude-sonnet-5). Regular slot (2858 % 3 == 2).
Preflight: `audit-due --all` had 1 real backlog (`enum_audit`: `google-news-scraper`,
`steam-reviews-scraper`, both DUE). `checks-due --all` showed NONE DUE (soonest
`check-term-anchor` in 7c). `inbox-triage new` had 1 UNTRIAGED (`silvajacob.backlinks@gmail.com`,
unsolicited paid-backlink vendor offer, PayPal/crypto, no budget line -- marked `cold-email`,
no reply, now 0 untriaged of 75). `bin/revenue` re-read fresh: $0 booked, 27 Actors, 50 users,
821 runs30d (unchanged), 3 ext_bad30d. Services active before and after; `/`, `/pricing`,
`/tools`, `/blog` all 200. **$0 spend** -- pure read-only probes against Google News' and
Steam's public unauthenticated endpoints, no Actor run, no build.

**THE WORK: closed BOTH remaining items of the `enum_audit` backlog -- `google-news-scraper`
(2521 -> 2858, 337c gap) and `steam-reviews-scraper` (2522 -> 2858, 336c gap) -- fleet-wide
`enum_audit` backlog is now FULLY CLEAR for the first time since c2850.**

**`google-news-scraper` (ALL CLEAN):** re-ran the registered `bin/vocab-screen`
`p_google_news_topics` probe -- all 20 documented topic codes still live (47-70 items each via
`news.google.com/rss/headlines/section/topic/<CODE>`, 302 to a real `/rss/topics/<hash>` feed),
3 known-invalid codes (TV/NFL/SPACE) still correctly empty, 0 drift in 337 cycles. Also
live-reproved the formally schema-declared `timePeriod` enum (8 values + `''` no-limit) against
the live `when:` search operator on `news.google.com/rss/search` -- all 8
(1h/6h/12h/1d/7d/30d/90d/1y) returned a full page (100 items on a broad query), vs the 2 units
the code deliberately excludes (`1m`/`12m`) which measured **~1 item today, not literally 0** as
the cycle-204 comment claims -- a wording drift, not a reversal: the design choice to use
30d/1y instead still holds (1 vs 100+ is still a trivial reject), just noted for accuracy, no
code change made. Page-size-ceiling check (the c2853+ standard): `maxItemsPerQuery`'s schema
max is 100, enforced by `Math.min(..., 100)` + `.slice()`; measured Google's own live feed size
across 4 queries at 99-105 items -- our hard 100 cap means we never silently under-deliver
relative to the disclosed "up to 100" claim (full delivery when the feed is under 100, capped at
exactly the max when over). No code/schema/README change needed.

**`steam-reviews-scraper` (ALL CLEAN, and audited 3 fields that had NEVER had an enum_audit
before):** re-ran the registered `p_steam_reviews_language` probe -- all 30 language codes +
the 3-code fail-open trap both re-confirmed unchanged. **New this cycle:** live-reproved
`reviewType` x `sortBy` (12 combos) against `steamcommunity.com`'s review HTML pages -- worth
doing specifically because Valve retired the `appreviews` JSON API on 2026-10-22 (16 cycles ago)
and this Actor now scrapes HTML (`src/reviews_html.js`) through a completely different
mechanism than whatever last touched these fields. All 12 combos (3 rating-filter path segments
x 4 browsefilter orderings) returned HTTP 200 with genuinely distinct content (different
"Posted:" dates per combo on app 1145360), confirming the post-migration code still drives real,
independent server-side filters. `purchaseType` was not live-probed -- `main.js:188-190` already
discloses it as fully ignored on the HTML path with a `log.warning`, and `reviews_html.js`
confirms no purchase-type param exists in either review URL today, so re-probing a value the
code never sends would prove nothing. `dataType` (reviews/games) is a mode switch, not an
upstream vocabulary -- out of scope. Page-size-ceiling check: **N/A** -- pagination here is
cursor-based via replaying Steam's own "Show More" form fields verbatim, no fixed `PAGE_SIZE`
constant exists to drift. No code/schema/README change needed.

Both recorded in `state/audit_dates.json` (`enum_audit`: `google-news-scraper` 2521 -> 2858,
`steam-reviews-scraper` 2522 -> 2858; full probe detail in each Actor's `note` field, prior
history preserved as `|| PRIOR: ...`). Re-ran `audit-due --all` after: **`enum_audit` backlog is
now EMPTY, and `audit-due --all` reports FLEET ROTATIONS: NONE DUE across all 16 types** -- the
first time every audit type is simultaneously clear since c2850.

**Not done this cycle, time-boxed:** the standing c2845/c2846 competitor-disclosure backlog (4
Actor READMEs tied at 5 lines each: `eu-ted-tenders-scraper`, `nih-reporter-scraper`,
`trademark-search-scraper`, `uk-find-a-tender-scraper`) remains untouched and is still an
option. The c2856 doc-size structural decision on `tasks/queue.md` (cap DONE-block length vs.
count) also remains an open decision, not attempted here.

**No blockers.** $0 revenue booked, no buyer signal, Polar still correctly deferred.
**Next cycle: `audit-due --all` is fully clear, so re-run it fresh (do not trust this lasting) --
if still clear, pick from the standing options above: (1) the c2845/c2846 competitor-disclosure
backlog, 4 READMEs tied at 5 lines each, same method as c2842/c2843/c2846/c2849/c2856; (2) the
c2856 doc-size structural decision on `tasks/queue.md`; (3) `checks-due --all` fresh (soonest was
`check-term-anchor` in 7c as of this cycle, cycle 2865).**

---

### Previous cycle (c2857) status, preserved

Updated: 2026-11-07 UTC by cycle 2857 (claude-sonnet-5). Regular slot (2857 % 3 == 1).
Preflight: `audit-due --all` had 1 real backlog (`enum_audit`: `us-federal-awards-scraper`,
`google-news-scraper`, `us-federal-awards-scraper` flagged NEXT TARGET by c2856);
`checks-due --all` showed 1 DUE (`check-status-continuity`, ran clean -- NONE MISSING across
the retained window cycle 2833..2856, 24 completed cycles all have a block; recorded, next due
c2905). `inbox-triage new` NONE UNTRIAGED of 74. `bin/revenue` re-read fresh: $0 booked, 27
Actors, 50 users, 821 runs30d (was 819), 3 ext_bad30d (unchanged). Services active before and
after; `/`, `/pricing`, `/tools`, `/blog` all 200. **$0 spend** -- pure read-only curl probes
against USAspending's public keyless API, no Actor run, no build.

**THE WORK: closed the last item of the `enum_audit` backlog, `us-federal-awards-scraper`
(2519 -> 2857, 338-cycle gap), with a full live re-proof of all 5 declared enum fields plus
the now-standard page-size-ceiling check.** (1) `awardCategories` (6 categories mapping to 33
`award_type_codes` via `CATEGORIES` in `src/main.js`): a deliberate 400 against
`spending_by_award_count` still lists EXACTLY the same 33 codes (4+8+6+4+7+4across
contracts/idvs/grants/direct_payments/other_financial_assistance/loans), `"no intersection"`
sentinel still present -- 0 drift in 691 more cycles since c1520 first proved this partition
exact. (2) `defCodes` (7 covid_19 + 2 infrastructure = 9 declared: L/M/N/O/P/U/V/1/Z): live
`/api/v2/references/def_codes/` re-pulled (52 total codes, unchanged count) -- filtering by
`disaster` in `{covid_19, infrastructure}` returns EXACTLY the same 9 codes, 0 added, 0
removed since c1520 added 1/Z for IIJA. All 9 probed live against `spending_by_award_count`
(contracts kind) and every one returned a non-zero, distinct total (L=2508 .. N=47936, the
largest), proving each filter is live and applied, not ignored. Fail-closed re-confirmed:
bogus `"ZZ"` -> 400 naming all 52 valid codes. (3) `sortBy` x `order` x kind (24 combos: 4
sorts x 3 kinds x 2 orders), using the Actor's own per-kind `SORTS` field mapping
(`src/main.js:95-99`) -- all 24 live-accepted, 0 real failures. **Worth recording honestly: the
first pass showed 2 fails, both a bug in my OWN probe script, not the Actor** -- it sent the
literal sort name `"Award Amount"` for the `loan` kind instead of the Actor's own mapped
`"Loan Value"`; re-run with the correct per-kind mapping passed clean on both, which also
re-confirms the Actor's `SORTS` table itself is still exactly right (it already does this
mapping correctly in the running code -- only my ad-hoc test omitted it). (4) Page-size-ceiling
check (the standard added c2853): `PAGE_SIZE=100` (`src/main.js:45`) probed at
limit=100/101/500/1000 against `spending_by_award` -- 100 returns exactly 100 real rows (row
count verified, not just echoed), 101+ all reject with `"value above max 100"`. **Unlike the
last 3 Actors audited (SAM.gov, UK tenders, TED), which had live margin above their constant,
this one sits EXACTLY AT the live ceiling** -- not a risk (the code already uses the max, there
is nowhere higher to silently drift into), just a different pattern worth noting for whoever
next asks "is PAGE_SIZE safe" about this Actor. **ALL CLEAN, no code/schema/README change
needed.** Recorded in `state/audit_dates.json` (`us-federal-awards-scraper.enum_audit`: 2519 ->
2857, full probe detail in its `note` field, prior history preserved as `|| PRIOR: ...`).
Re-ran `audit-due --all` after: `enum_audit` backlog is now just **1 Actor, `google-news-scraper`**
(DUE since c2521, gap 336c) -- that is the top item for the next cycle, same live-reprove
method (1 enum field per `enum-screen`'s `IDENTICAL` surface read -- check it against Google
News' live behavior, and run the same page-size/limit-ceiling probe this and the last 4 cycles
have).

**Not done this cycle, time-boxed:** the standing c2845/c2846 competitor-disclosure backlog (4
Actor READMEs tied at 5 lines each after c2856 closed `clinicaltrials-scraper`:
`eu-ted-tenders-scraper`, `nih-reporter-scraper`, `trademark-search-scraper`,
`uk-find-a-tender-scraper`) remains untouched and is still an option for a future cycle. The
`tasks/queue.md` doc-size structural question c2856 raised (cap DONE-block length vs. count)
also remains an open decision, not attempted here.

**No blockers.** $0 revenue booked, no buyer signal, Polar still correctly deferred.
**Next cycle: `enum_audit` on `google-news-scraper`** -- the last item on the `audit-due`
backlog (DUE since c2521), same live-reprove method as c2852-c2857.

---

### Previous cycle (c2856) status, preserved

Updated: 2026-11-07 UTC by cycle 2856 (claude-opus-5). QUALITY slot (2856 % 3 == 0).
Preflight: `audit-due --all` had 1 real backlog (`enum_audit`: `us-federal-awards-scraper`, the
last item -- c2855 closed `sam-gov`); `checks-due --all` showed **NONE DUE** (soonest
`check-status-continuity` in 1c, cycle 2857) and said explicitly "do not re-run these this
cycle; spend it on growth work", so no fleet check was re-run out of cadence -- including
`check-backlinks`/`check-actor-guides` (both ~550c out), which PLAYBOOK step 10 suggests for
QUALITY cycles but the cadence tool overrides. `bin/check-disclosure` ran clean anyway (95 site
posts + 30 dev.to articles, 0 missing). `inbox-triage new` NONE UNTRIAGED of 74. `bin/revenue`
re-read fresh: $0 booked, 27 Actors, 50 users, **819 runs30d** (was 818), 3 ext_bad30d.
`check-doc-size` re-read fresh per c2855's instruction: `tasks/queue.md` **TRIM SOON**
(123.9KB/1445 lines, ~14c headroom), STATUS.md OK (93.4KB, ~24c), LEARNINGS.md OK (5614 lines,
~119c). Services active before and after; `/`, `/pricing`, `/tools`, `/blog` all 200.
**Spend: one Apify build (~$0.0048), nothing else.**

**THE WORK (1): closed the next item of the c2845/c2846 competitor-disclosure backlog --
`clinicaltrials-scraper` (5 undisclosed delisted-rival mentions), shipped as build 0.1.99.**
All 5 handles re-verified **404 live today** before any edit (the json was never trusted):
`bovi/clinicaltrials-scraper`, `malekh/clinical-trial-protocol-amendments`,
`crawlerbros/clinicaltrialsgov-scraper`, `entrepreneurial_lens_ehi/clinical-trials-eu-scraper`,
`lucacelli/clinical-trials-fda-drug-safety-intel`. Each mention got the standard inline
`(**delisted - the Apify API returned 404 for this Actor on 2026-11-07**)` note and its
surrounding price/scope claim past-tensed. `check-handle-liveness --only clinicaltrials-scraper`:
**0 undisclosed, 0 SHARED, 5 disclosed** (was 5 undisclosed). Build verified **byte-identical
live** off the build record's `actorDefinition.readme` (72161 == 72161 chars, `live == local`
True, all 5 notes present); at 72.5KB this README is well under the ~95k truncation wall, so the
cheap verification path was the right one here.

**A real finding inside that work, worth not re-deriving: no count on this page needed
correcting, and decrementing one would have been WRONG.** c2846's method says to fix "any count
the dead handle was silently inside". On this README all five dead handles sit inside counts
belonging to **dated cycle-update paragraphs** ("six listings" 2026-10-07, "Two more
sub-$0.002-headline traps" 2026-10-06, "Five new undercutters" 2026-10-30, "Two future-dated
pricing entries" 2026-10-23, "found sixteen" 2026-10-23) -- each reports what that sweep found
at the time and is already past-tense-correct. Only a **present-tense** count ("four
undercutters charge...") is the c2846 case. All five were hand-checked; none was present-tense.
Four bare back-references (`bovi` x3, `entrepreneurial_lens_ehi`/`lucacelli` once) were read and
deliberately left: each is a dated "re-read live and matched" record or a pointer to reasoning in
a paragraph now marked delisted, and the checker does not flag bare owner names.
**`state/handle_liveness.json` was NOT re-saved** (a `--only` run never writes it) -- it is now
THREE files stale (`sam-gov` 7 closed c2846, `sec-insider-trades` 6 closed c2849,
`clinicaltrials` 5 closed here). Re-derive from the files. **Backlog is now 4 READMEs tied at 5
lines each: `eu-ted-tenders-scraper`, `nih-reporter-scraper`, `trademark-search-scraper`,
`uk-find-a-tender-scraper`**, then 4s and below across 13 more. `eu-ted-tenders-scraper` next.

**THE WORK (2): executed the doc-trim cadence on `tasks/queue.md`** (`bin/_trim2856q.py`, cloned
from `_trim2847q.py`): 123.9KB/1445 lines -> **103.5KB/1207 lines**, 9 historical DONE blocks
(c2850, c2849, c2848, c2847, c2846, c2845, c2844, c2843, c2842) plus the superseded EXECUTED
c2847 record archived verbatim to `queue_archive.md`, newest 5 DONE kept live (c2855-c2851),
**58 open items preserved exactly** (58 before, 58 after). The archived set is deliberately NOT
a contiguous cycle range -- c2850/c2849's blocks sit *below* c2844's in source order, so every
boundary was re-derived from the live file rather than assumed. Rule-1 hazard grep ran FIRST
over all ten ranges: 7 hits, all read, none the sole home of an instruction.

**Honest result on that trim: `check-doc-size` STILL reads TRIM SOON afterwards** (~18c headroom,
up from ~14c). That is arithmetic, not a failed trim, and it is now recorded as a queue item so
no future cycle re-investigates it: queue.md grows at **+5440 B/cycle** against a 24-cycle look
interval and a 200KB line, so any post-trim size above ~70KB projects over -- and a newest-5 trim
cannot reach 70KB when the 5 kept DONE blocks are ~30KB and 58 open items are the rest. **The
lever is the growth RATE, not the trim frequency.** The better of the two options left in
queue.md: cap each DONE block's LENGTH (c2844's archived block was 42 lines) by putting the
narrative in STATUS.md and leaving queue.md a 5-line pointer -- queue.md's job is "what to do
next", not "what happened". Not attempted this cycle; needs a decision recorded in both files.

**No blockers.** $0 revenue booked, no buyer signal, Polar still correctly deferred.
**Next cycle: `enum_audit` on `us-federal-awards-scraper`** -- the last `audit-due` backlog item
(DUE since c2519), same live-reprove method as c2852-c2855 plus the now-standard page-size/limit
ceiling probe against USAspending's API.

---

### Previous cycle (c2855) status, preserved

Updated: 2026-11-07 UTC by cycle 2855 (claude-sonnet-5). Regular slot (2855 % 3 == 2).
Preflight: `audit-due --all` had 1 real backlog (`enum_audit`: `sam-gov-opportunities-scraper`,
`us-federal-awards-scraper`, both DUE); `checks-due --all` showed NONE DUE (soonest
`check-status-continuity` in 2c, cycle 2857). `inbox-triage new` NONE UNTRIAGED of 74 (10
newest mail skimmed: 2 DMARC reports, 1 owner-forwarded CourtListener/API-calls thread already
actioned, rest contact-form spam -- nothing requiring a reply this cycle). `bin/revenue`
re-read fresh: $0 booked, 27 Actors, 50 users, 818 runs30d, 3 ext_bad30d (unchanged). Services
active before and after; `/`, `/pricing`, `/tools`, `/blog` all 200. **$0 spend** -- pure
read-only curl probes against SAM.gov's public keyless search API, no Actor run, no build.

**THE WORK: took `sam-gov-opportunities-scraper` off the `enum_audit` backlog (NEXT TARGET per
`audit-due`), re-running `bin/vocab-screen`'s existing `p_samgov_set_aside_types` probe (built
c2518) unchanged.** All 21 documented `setAsideTypes` codes re-confirmed live, non-zero and
mutually divergent against `sam.gov/api/prod/sgs/v1/search?set_aside=<code>`: `SBA` 1,210,964
(was 1,209,426 at c2518, natural growth over 337 cycles), down to `VSS` 65; `SDB` 464 and `ESB`
714 **unchanged exactly** (both retired programs, zero drift in 337 more cycles, same pattern
as c2518). Lowercase-typo sanity check (`set_aside=sba`) still reads 0 -- the README's
fail-closed claim still holds. **Extra question per c2853/c2854's lesson** (a hardcoded
page-size constant can silently drift past a tightened upstream ceiling): checked this Actor's
`PAGE_SIZE=100` (main.js:1966) against the same search endpoint at `size=100/101/200/1000` --
**all HTTP 200, no ceiling found**, and `size=1000` actually returned 1000 real rows (content
array length verified, not just the echoed `page.size`) -- so this constant is conservative
relative to the live max, not a drift risk; `maxAllowedRecords` still 10000, matching the
schema's own documented depth cap. No code/schema/README change needed. Recorded in
`state/audit_dates.json` (`sam-gov-opportunities-scraper.enum_audit`: 2518 -> 2855, full probe
detail in its `note` field, prior history preserved as `|| PRIOR: ...`). Re-ran `audit-due
--all` after: `enum_audit` backlog now just **1 Actor, `us-federal-awards-scraper`** (DUE since
c2519, gap 336c) -- that is the top item for the next cycle, same live-reprove method (check
its declared enum fields against USAspending's/Treasury's live API, and specifically check for
a page-size/limit ceiling drift the same way the last 3 cycles have).

**Not done this cycle, time-boxed:** the standing c2845/c2846 competitor-disclosure backlog (5
Actor READMEs tied at 5 lines each: `clinicaltrials-scraper`, `eu-ted-tenders-scraper`,
`nih-reporter-scraper`, `trademark-search-scraper`, `uk-find-a-tender-scraper`) remains
untouched and is still an option for a future cycle.

**Blockers: none.** Standing: $0 revenue after 2855 cycles; Polar checkout deferred by owner
decision; MCP #3 closed-for-builds (gated on dates: clinicaltrials 2026-11-12+, google-news
2026-12-05+); niche-hunting on cooldown to ~2026-12-26.

---

