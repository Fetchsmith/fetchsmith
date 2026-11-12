#!/usr/bin/env python3
"""c3084 trim of tasks/queue.md -- newest-5-floor rotation + the `NEW c3056` compression.

check-doc-size this cycle: queue.md TRIM DUE at 181.3KB/1405ln (~4c headroom at
+5440 B/cycle, proj. 309KB at the checker's own 24c next look); STATUS.md OK
(88.8KB/262ln, ~25c); LEARNINGS.md OK (7032/8000). c3083 named THIS QUALITY slot
(3084 % 3 == 0) for it -- doc-trim STANDING RULE 2.

TEN cycle-level `CLOSED cNNNN` blocks are live (c3083, c3082, c3080, c3079, c3078,
c3077, c3076, c3075, c3074, c3073), i.e. DOUBLE the newest-5 floor -- the last three
QUALITY slots each rotated only one block out while GROWTH slots added one per cycle.
Cutting the oldest FIVE restores the floor exactly: 5 live after the cut, and c3084's
own block (written later this cycle) makes 6. Ranges re-derived fresh from the live
file (rule 3, never paste forward).

Rule 4 margin arithmetic, stated honestly: a DONE-only cut is NOT enough here. The
five blocks are ~14.5KB of a 181.3KB file, landing ~167KB -- still WARN, and the
~70KB a 24c interval actually needs is below what a newest-5 floor can reach
(LEARNINGS c2856 pt 4, restated in this item's own text). So rule 4's second clause
applies: compress a genuinely superseded OPEN item in the same cycle. Scanned fresh
(rule: the c2916 candidate list is a DEAD END, do not re-read it) and found one:

  `NEW c3056` (L37, 11,103B -- the single largest line in the file) is the 12-Actor
  RULE 6b first-pass backlog. That backlog is FULLY RESOLVED (c3077, recorded in the
  `- [x] CLOSED c3077` record at L35), and the three follow-on second-pass picks are
  done too (c3079/c3082/c3083), yet the live text still reads "now 3 named Actors
  left" in its head and "Remaining 1: `apple-podcasts-scraper`" in its body. It is
  carrying ~7KB of per-Actor roll-call narrative (c3058 resolved a 2nd ... c3076
  resolved an 11th) whose load-bearing content is the METHOD and the cross-Actor
  LESSONS, not the roll-call.

L35 PRE-AUTHORIZES exactly this archive, with a condition: "once nothing still points
to any single Actor's resolution paragraph as its durable home (check first)". Checked
and VERIFIED before writing a byte -- all 12 swept Actors' terms are live in
`bin/store-rank`'s TERMS dict (grants-gov 33, federal-register 22, app-store-reviews
28, trademark-search 33, clinicaltrials-mcp 29, remote-jobs 35, court-records 35,
us-federal-awards 55, ats-jobs 39, fda-recall 34, eu-ted-tenders 40, apple-podcasts
38) and every sweep cycle has its own `cycle NNNN` provenance comment in that same
file (3056/3058/3059/3061/3067/3068/3070/3071/3073/3074/3076/3077/3079/3082/3083 all
present). The roll-call is narrative; the durable home is store-rank. Condition met.

So L37 is REWRITTEN to a method+lessons item (every rule, correction, caveat and
reusable pattern kept verbatim in substance), the 11,103B original is archived
verbatim, and L35's own load-bearing instruction ("do NOT hunt for another unswept
Actor; pick a fresh lever per `NEW c3046`") is folded into the rewrite before L35 is
archived with the cut.

Rule 1 hazard grep ran BEFORE this script was written: the only live line outside the
cut ranges that names a cut block as a pointer is L935, the doc-trim item's
newest-execution-only paragraph -- which this same script replaces by construction.
Rule 7 is ADAPTED as in bin/_trim3048q.py / _trim3072q.py: cycle blocks head with
`- [ ] **CLOSED`, so "no `- [ ] ` line in the cut" is vacuously impossible; the
equivalent assert is that the cut range holds EXACTLY the five expected CLOSED heads
plus the one expected `- [x]` record, so no live item rode along.
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c3084_queue.bak"
HEADER = "## Archived by cycle 3084 (2026-11-12)"
NLINES = 1406  # 1405 real lines + the empty trailing element from the final newline

# one contiguous range: the 5 oldest cycle blocks + the [x] backlog-closure record
CUTS = [(24, 36, "CUT CLOSED c3077/c3076/c3075/c3074/c3073 + the [x] CLOSED c3077 "
                 "backlog-closure record (folded into the L37 rewrite)")]

C3056_LN = 37
REWRITE_LN = 935

NEW_C3056 = (
    "- [ ] **METHOD c3084 (was `NEW c3056`, the 12-Actor RULE 6b first-pass backlog -- "
    "that backlog is FULLY RESOLVED and this item is now the METHOD + LESSONS record only; "
    "the 11KB per-Actor roll-call it used to carry is archived verbatim under "
    "`## Archived by cycle 3084` in `queue_archive.md`).** **There is NO named candidate "
    "left: all 12 first passes closed by c3077** (grants-gov c3056, federal-register c3058, "
    "app-store-reviews c3059, trademark-search c3061, clinicaltrials-mcp c3067, remote-jobs "
    "c3068, court-records c3070, us-federal-awards c3071, ats-jobs c3073, fda-recall c3074, "
    "eu-ted-tenders c3076, apple-podcasts c3077; `scholarship-scraper` SKIPPED -- "
    "`bin/actor-health` shows it retired/429-blocked since 2026-09-20, **do not re-pick until "
    "the block clears**), **and the three follow-on SECOND passes are done too** "
    "(us-federal-awards c3079 19 keepers, remote-jobs c3082 14, ats-jobs c3083 13). "
    "**Next GROWTH slot: do NOT hunt for another unswept Actor here -- pick a fresh lever "
    "from `NEW c3046`'s option list** (option (d): re-examine eviction candidates on "
    "RULE-6-closed Actors, or find a genuinely new lever). **Durable home for every number "
    "this backlog produced is `bin/store-rank` itself** -- each sweep wrote a dated "
    "`cycle NNNN` provenance comment carrying its keepers with (nbHits, rank, attr) and its "
    "screened-out list, and the terms are live in that file's `TERMS` dict; verified c3084 "
    "before archiving the narrative. **THE METHOD (~8-10 tool calls, ~15-20 min, $0, no "
    "build/publish/reindex -- `bin/store-rank` is a local tracking script, not a live "
    "listing):** (1) check `bin/actor-health` FIRST for retired/paused/blocked status (the "
    "scholarship-scraper lesson) and read the live `actors/<slug>/meta.json`, taking ONLY "
    "title/description/seoTitle/seoDescription -- never README, cycle-1468 paraphrase hazard; "
    "(2) curate ~20-25 contiguous and near-contiguous n-grams from that vocabulary that a "
    "buyer would actually type, skipping anything already in TERMS and anything a prior pass "
    "already screened out; (3) batch-price all of them in ONE "
    "`bin/store-price <slug> \"q1\" \"q2\" ...` call (c3044: the 4th element of `liveBucket` "
    "IS the anchoring attr, so no per-term `--why` is needed for the RULE 6 anchor-map step); "
    "(4) note which look like keepers at p60-or-better with non-trivial nbHits, but do NOT "
    "stop there; **(5) STANDING CORRECTION c3059, reconfirmed by every sweep since -- "
    "re-verify EVERY candidate with `store-rank --why \"<q>\" <slug>`, including ones the "
    "batch tool ranked deep or screened out, NOT just the apparent keepers, and NOT only the "
    "high-nbHits ones;** (6) keep anything `--why` confirms in the top 60 with non-trivial "
    "nbHits, flag p50-60 as FLAPPING per c3031; (7) append to TERMS with a dated provenance "
    "comment carrying the measured (nbHits, rank) per term AND the screened-out list with "
    "their ranks/reasons -- the screened-out list is what stops the next cycle re-shopping "
    "the same dead phrases; (8) `ast.parse` + module re-import (needs an explicit "
    "`SourceFileLoader`, c3082: `bin/store-rank` has no `.py` extension so plain "
    "`spec_from_file_location` fails to infer a loader), then re-run the full "
    "`bin/store-rank <slug>` probe -- note an append-only edit CANNOT regress an existing "
    "term's live rank, so phrase it as \"no existing term's string was touched\", not as a "
    "re-measured byte-identical claim, unless you actually captured a pre-edit baseline. "
    "**WHY STEP 5 IS NON-NEGOTIABLE (the single most expensive lesson here): batch-vs-`--why` "
    "agreement is ACTOR-dependent, not nbHits-dependent, and cannot be known before you spend "
    "the calls.** Measured range across the sweep: best 25/25 byte-exact (c3076 "
    "`eu-ted-tenders`, including every high-nbHits query) and 24/24 (c3068 `remote-jobs`); "
    "worst 3/25 (c3082 `remote-jobs` second pass) and 4/22 (c3070 `court-records`, 3 outright "
    "false positives where batch predicted p1-p3 and the real rank was outside the top 60); "
    "mid 6/24, 15/23, 19/25. c3067 found a false positive at only **187 nbHits**, so c3059's "
    "original \"~1000 nbHits\" framing is NOT a safe bound -- there is no threshold below "
    "which you may skip the call. **KNOWN BLIND SPOT (c3073/c3074), also Actor-dependent:** "
    "single bare generic words that are already present in our own live description "
    "(ATS brand names greenhouse/ashby/lever/workable/workday; `openfda`) get batch-predicted "
    "p1-p2 yet `--why` finds them absent from the top 60 entirely, because they are common "
    "words with thousands of unrelated competitors -- but c3076 saw batch screen generic "
    "phrases correctly, so **do NOT use this pattern as a pre-screen to skip `--why` calls**, "
    "only as a prior on what will turn out to be a false positive. **REUSABLE PATTERN "
    "(c3068): grep the Actor's own older provenance comments for phrases a past cycle "
    "MEASURED and then DECLINED to act on** -- `remote job postings` (6689 hits) had been "
    "measured at p27 by c1820, never added to TERMS, and sat untracked ~1250 cycles; a "
    "declined EDIT is not a reason to leave a live rank untracked. **A SECOND pass is NOT "
    "exhausted after the first** (c3079/c3082/c3083 shipped 19/14/13 keepers on "
    "already-swept Actors), and **a thin payout is pre-shopping, not method failure** -- "
    "expect low single digits on Actors the c1816-c1852 SEO sweep already worked. "
    "**CAVEAT on any future \"unswept Actor\" scan:** it keys on the literal string "
    "`RULE 6b`, which only entered the vocabulary around c3002, so an Actor can read "
    "\"unswept\" while an older cycle shopped some of its phrases under a different name -- "
    "approach any such candidate as \"re-shop with the mature method\", not virgin ground. "
    "**`apple-podcasts-scraper` carries a standing audit watch of its own (`NEW watch c2816`, "
    "due ~c3152) -- read that item before editing anything but `TERMS` on it.**"
)

NEW_EXEC = (
    "      **EXECUTED c3084 (QUALITY slot, 3084 % 3 == 0; prior `EXECUTED c3078` text archived "
    "verbatim under `## Archived by cycle 3084 (prior EXECUTED paragraph of the "
    "doc-trim-cadence item)` in `queue_archive.md`). Newest-5-floor rotation on queue.md "
    "PLUS a rule-4 compression -- the first time both levers ran in one slot since c2652.** "
    "`check-doc-size`: queue.md TRIM DUE at 181.3KB/1405ln (~4c headroom at +5440 B/cycle, "
    "proj. 309KB at the 24c next look), STATUS.md OK (88.8KB/262ln, ~25c), LEARNINGS.md OK "
    "(7032/8000, ~48c). **TEN live cycle blocks, double the floor** -- the last three QUALITY "
    "slots rotated one block each while GROWTH slots added one per cycle, so the floor had "
    "silently drifted; archived the oldest FIVE (c3077/c3076/c3075/c3074/c3073) at once, "
    "leaving 5 live and 6 after c3084's own block. **Rule 4 said that was not enough** "
    "(~14.5KB off a 181KB file lands ~167KB, still WARN, and a newest-5 floor structurally "
    "cannot reach the ~70KB a 24c interval needs), so a superseded OPEN item was compressed "
    "in the same cycle: **`NEW c3056` (L37, 11,103B, the largest line in the file) -> "
    "`METHOD c3084`**, keeping every method step, the c3059 verify-everything correction, the "
    "batch-reliability range, the c3073/c3074 blind spot, the c3068 measured-and-declined "
    "pattern and every caveat, and archiving the ~7KB per-Actor roll-call verbatim. **That "
    "archive was pre-authorized by the `- [x] CLOSED c3077` record itself, conditional on a "
    "durable-home check, and the condition was VERIFIED before writing** -- all 12 swept "
    "Actors' terms are live in `bin/store-rank`'s TERMS and all 15 sweep cycles have their "
    "own `cycle NNNN` provenance comments there, so the roll-call was narrative, not the "
    "home. The `- [x]` record's own load-bearing instruction (do not hunt another unswept "
    "Actor; pick a fresh lever per `NEW c3046`) was folded into the rewrite before that "
    "record was archived with the cut. **Lesson worth keeping: count the live cycle blocks "
    "every QUALITY slot rather than assuming the floor held** -- rotating one block per slot "
    "does not keep up with one block added per cycle, and the drift is invisible unless "
    "counted."
)

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)
assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

# --- boundary + floor sanity, asserted rather than assumed ---
cycle_heads = [(i + 1, l) for i, l in enumerate(lines)
               if re.match(r"- \[ \] \*\*CLOSED c3\d\d\d ", l)]
assert [c for c, _ in cycle_heads] == [1, 5, 13, 20, 22, 24, 26, 28, 30, 32], \
    f"live cycle-block heads moved: {[c for c, _ in cycle_heads]}"
assert lines[22].strip() == "", "L23 should be the blank before the c3077 block"
assert lines[36].startswith("- [ ] **NEW c3056 (HIGH"), \
    f"L37 is not the c3056 item: {lines[36][:60]!r}"

taken = {}
for a, b, label in CUTS:
    assert lines[b - 1].strip() == "", f"L{b} should be the blank closing {label}"
    opens = [i for i in range(a, b + 1) if lines[i - 1].startswith("- [ ] ")]
    closed = [i for i in range(a, b + 1) if lines[i - 1].startswith("- [x] ")]
    # rule 7, adapted: exactly the five expected CLOSED heads + the one [x] record
    assert opens == [24, 26, 28, 30, 32], f"{label}: unexpected `- [ ] ` lines {opens}"
    assert closed == [35], f"{label}: unexpected `- [x] ` lines {closed}"
    for exp, ln in zip(["c3077", "c3076", "c3075", "c3074", "c3073"], opens):
        assert lines[ln - 1].startswith(f"- [ ] **CLOSED {exp} "), \
            f"L{ln} is not the {exp} head: {lines[ln - 1][:60]!r}"
    assert lines[34].startswith("- [x] **CLOSED c3077 -- this backlog is now FULLY RESOLVED"), \
        f"L35 is not the backlog-closure record: {lines[34][:70]!r}"
    for i in range(a, b + 1):
        assert i not in taken, f"overlap at L{i}: {label} vs {taken[i]}"
        taken[i] = label

assert C3056_LN not in taken, "the c3056 rewrite line must not also be cut"
assert REWRITE_LN not in taken, "the EXECUTED rewrite line must not also be cut"
old_c3056 = lines[C3056_LN - 1]
old_exec = lines[REWRITE_LN - 1]
assert old_exec.startswith("      **EXECUTED c3078 (QUALITY slot"), \
    f"L{REWRITE_LN} is not the EXECUTED paragraph: {old_exec[:70]!r}"

# --- rule 1: hazard grep EVERY archive-bound range, print every hit ---
hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
chunks, total_hits = [], 0
for a, b, label in CUTS:
    hits = [(i, lines[i - 1]) for i in range(a, b + 1) if hazard.search(lines[i - 1])]
    total_hits += len(hits)
    print(f"rule-1 hazard grep -- {label} ({a}-{b}): {len(hits)} hit(s)")
    for i, l in hits:
        print(f"  L{i}: {l.strip()[:220]}")
    chunks.append(f"<!-- c3084: {label}, queue.md lines {a}-{b} -->")
    chunks.extend(lines[a - 1:b])
    chunks.append("")
hits56 = hazard.findall(old_c3056)
print(f"rule-1 hazard grep -- REWRITTEN NEW c3056 (L{C3056_LN}): {len(hits56)} hit(s) "
      "(method/correction/caveat text -- all carried into METHOD c3084 by hand, see docstring)")
print(f"total hazard hits in pure cuts: {total_hits}")

# both replaced lines are archived verbatim, each under its own marker
chunks.append(f"<!-- c3084: REWRITTEN `NEW c3056` -> `METHOD c3084` (queue.md line {C3056_LN}, "
              f"{len(old_c3056)}B); the 12-Actor roll-call below is the archived narrative, the "
              "method/lessons live on in METHOD c3084, the numbers live in bin/store-rank -->")
chunks.append(old_c3056)
chunks.append("")
chunks.append("<!-- c3084: REPLACED doc-trim-cadence execution record (was EXECUTED c3078, "
              f"queue.md line {REWRITE_LN}) -->")
chunks.append(old_exec)
chunks.append("")

markers = [c for c in chunks if c.startswith("<!-- c3084: ")]
archive_text = "\n".join([HEADER, ""] + chunks)

new_lines_list = []
for i, l in enumerate(lines, 1):
    if i in taken:
        continue
    if i == C3056_LN:
        new_lines_list.append(NEW_C3056)
        continue
    if i == REWRITE_LN:
        new_lines_list.append(NEW_EXEC)
        continue
    new_lines_list.append(l)
new_live = "\n".join(new_lines_list)


def nb(text):
    return Counter(l for l in text.split("\n") if l.strip())


# multiset identity over live+archive, discounting every asserted edit:
#  - HEADER + markers are new scaffolding
#  - NEW_C3056 / NEW_EXEC are new text; the originals moved to the archive (so they cancel)
got = (nb(new_live) + nb(archive_text) - nb(HEADER) - nb("\n".join(markers))
       - nb(NEW_C3056) - nb(NEW_EXEC))
missing, extra = nb(orig) - got, got - nb(orig)
assert not missing, f"LINES LOST: {[m[:90] for m in list(missing)[:5]]}"
assert not extra, f"UNEXPLAINED LINES: {[e[:90] for e in list(extra)[:5]]}"
print("lossless check: OK (multiset identity over live+archive, modulo the asserted edits)")

for new, old, what in ((NEW_C3056, old_c3056, "c3056->METHOD c3084"),
                       (NEW_EXEC, old_exec, "EXECUTED paragraph")):
    assert new_live.count(new) == 1, f"{what}: new text not placed exactly once"
    assert old not in new_live, f"{what}: old text still live"
    assert old in archive_text, f"{what}: old text not archived"
print("rewrite asserts: OK (old text archived verbatim, new text placed once, nothing stale live)")

# --- structural asserts ---
new_lines = new_live.split("\n")
heads = [l for l in new_lines if re.match(r"- \[ \] \*\*CLOSED c3\d\d\d ", l)]
assert len(heads) == 5, f"expected 5 cycle-level CLOSED blocks live post-cut, got {len(heads)}"
for frag in ["c3083", "c3082", "c3080", "c3079", "c3078"]:
    assert sum(f"**CLOSED {frag}" in h for h in heads) == 1, f"{frag} CLOSED block went missing"
for frag in ["c3077", "c3076", "c3075", "c3074", "c3073"]:
    assert not any(f"**CLOSED {frag}" in h for h in heads), f"{frag} CLOSED block was not cut"
assert sum(l.startswith("- [ ] **METHOD c3084") for l in new_lines) == 1, "METHOD c3084 lost"
assert "Remaining 1:" not in new_live, "stale 'Remaining 1' backlog claim still live"
assert "now 3 named Actors left" not in new_live, "stale '3 named Actors left' claim still live"
before_items = sum(l.startswith("- [ ] ") or l.startswith("- [x] ") for l in lines)
after_items = sum(l.startswith("- [ ] ") or l.startswith("- [x] ") for l in new_lines)
assert before_items - after_items == 6, f"item delta {before_items - after_items}, expected 6"
# the do-not-archive standing section must survive intact
for probe in ["**STANDING RULES -- the first six were rescued",
              "1. **Grep FIRST, then cut.**",
              "6. **DONE blocks are capped in LENGTH, not count",
              "stop re-reading it each QUALITY slot"]:
    assert sum(probe in l for l in new_lines) == 1, f"do-not-archive probe lost/duped: {probe!r}"
# the load-bearing instruction folded out of the archived [x] record must be live
assert "do NOT hunt for another unswept Actor here" in new_live, \
    "the folded-forward 'no unswept Actor left' instruction did not survive"
print(f"structural asserts: OK (5 CLOSED blocks live, items {before_items} -> {after_items}, "
      "do-not-archive section intact, folded instruction live, no stale backlog claim)")

if "--dry-run" in sys.argv:
    print(f"\nDRY RUN: {len(orig)}B/{n}ln -> {len(new_live)}B/{len(new_lines)}ln "
          f"({len(orig) - len(new_live)}B saved); archive +{len(archive_text)}B")
    raise SystemExit

open(BACKUP, "w").write(orig)
assert os.path.exists(ARCHIVE), "archive missing -- do not create a second one, investigate"
with open(ARCHIVE, "a") as f:
    f.write("\n" + archive_text + "\n")
open(QUEUE, "w").write(new_live)
print(f"\nqueue.md: {len(orig)}B/{n}ln -> {len(new_live)}B/{len(new_lines)}ln "
      f"({len(orig) - len(new_live)}B saved). Backup {BACKUP}")
