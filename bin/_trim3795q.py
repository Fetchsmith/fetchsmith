#!/root/agent/venv/bin/python
"""Cycle 3795 tasks/queue.md floor-3 rotation -- the OVERDUE trim flagged HIGH by
`NEW c3792` (filed because growth had put this file ~4 cycles from the 256KB Read
cap). Clone of _trim3783q.py BY NAME (the mandated lineage per notes/PLAYBOOK.md),
widened to TWO non-contiguous spans because an OPEN item (`NEW c3792` itself) sits
between the two oldest pools of CLOSED report blocks.

CENSUS RE-DERIVED FRESH (c3795, not inherited): `grep -n "^- \\[[ x]\\] \\*\\*"` found
14 CLOSED "report-shaped" blocks newest-to-oldest: c3794, c3793, c3792, c3791, c3790,
c3789(report), c3788, c3787, c3786, c3785, c3784, c3783(the "ran all 4 checks" shape),
c3782, c3779. Floor 3 (STANDING c3280 / c3672 cadence) = keep newest 2 (c3794, c3793)
+ this cycle's own block, so the cut is EVERY report block from c3792 down to c3779
(12 blocks) -- far deeper than the routine 5-block cuts, matching NEW c3792's explicit
"trim DEEP" instruction (rotation-only cuts to just-under-threshold have gone straight
back to WARN every time per the c1976 lesson).

SPAN A = the c3792 report block alone (lines 8-13), because the OPEN item `NEW c3792`
(the trim flag itself -- now resolved by this very script) sits immediately after it
and must not be swallowed. It is replaced in place by a one-line closure note.
SPAN B = c3791 report through c3779 report, 11 blocks (c3791/c3790/c3789-report/c3788/
c3787/c3786/SHIPPED-c3786/c3785/c3784/c3783/c3782/c3779 -- SHIPPED c3786 is a fully
self-contained, already-verified fix record with no residue, swept up in the same span),
ending right before the one-off `CLOSED c3789 (was NEW c3768)` item, which is NOT a
report block and must stay (it is the promoted-residue closure, already past this
file's floor-3 pool by definition).

HAZARD GREP (3-pass, all run before this script was written):
(a) whole-repo grep for every cut cycle's `cNNNN\b` outside queue.md/queue_archive.md/
    STATUS.md -- every hit is a self-contained LEARNINGS.md lesson paragraph or a
    main.js code comment citing the cycle as historical context, never a pointer that
    NEEDS the queue.md narrative to resolve. Nothing to relocate.
(b) same as (a), narrower paths -- no additional hits.
(c) intra-file: `NEW c3162`/`c3488`/`c3568`/`c2312`/`c3789a-c`/`c3744a`/`c3744b`/`c3784`/
    `c3788` all have their OWN live top-level definitions OUTSIDE both spans (verified
    by direct grep) -- every mention of them INSIDE the spans is a backward reference
    to an already-separately-defined item, not a hidden definition. Three LIVE items
    outside the spans (`NEW c3744a` L96, the `NEW c3784` gate-closure L98, `NEW c3744b`
    L101) say "see CLOSED c3791/c3788/c3790 above" where "above" is about to become
    FALSE (the target moves to the archive) -- but `NEW c3492`'s own bookkeeping ruling
    (still live in this file) explicitly covers this exact shape: a pointer into an
    archived CLOSED block resolves in `tasks/queue_archive.md` under its
    `## Archived by cycle NNNN` header, and is deliberately left unedited rather than
    spending bytes on inline "(archived)" markers. Not a new hazard; not touched.

GUARD 2 (c3748 lesson, widened regex): both spans hand-inspected for nested
`\s+(?:- )?\*\*`?NEW c\d+[a-z]?`?\b` sub-bullets that are NOT already-closed narrative
mentions. Zero found -- every `NEW cNNNN` string inside either span is prose ("closed
NEW c3744a's probeGet leg", "NEW c3162 owner cohort", etc.) pointing at a definition
that lives elsewhere, never an un-promoted actionable. No promotion needed.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
TOP = re.compile(r"^- \[[ x]\] \*\*", re.M)
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)

SPAN_A_START = "- [x] **CLOSED c3792 -- QUALITY slot (3792 % 3 == 0)"
SPAN_A_NEXT = "- [ ] **NEW c3792 (HIGH -- the first genuinely OVERDUE"
SPAN_B_START = "- [x] **CLOSED c3791 -- BUILD slot (3791 % 3 == 2)"
SPAN_B_NEXT = "- [x] **CLOSED c3789 (was `NEW c3768`)"

a_start = orig.index(SPAN_A_START)
a_end = orig.index(SPAN_A_NEXT)
span_a = orig[a_start:a_end]

b_start = orig.index(SPAN_B_START)
b_end = orig.index(SPAN_B_NEXT)
span_b = orig[b_start:b_end]

assert a_start < a_end < b_start < b_end, "span ordering drifted -- re-locate before cutting"
assert span_a.count("- [x] **CLOSED c") == 1, "span A shape unexpected"
assert span_b.count("- [x] **CLOSED c") == 12, \
    f"span B block count unexpected: {span_b.count('- [x] **CLOSED c')}"  # 11 report blocks + CLOSED c3791a (one-off, resolved, no residue)
# one-off closures and still-open items must never be swallowed by either span
for keep in ("3789a", "3789b", "3789c", "3789 (was", "3768 (was", "3744a", "3744b",
             "3784` CLOSED", "3788` CLOSED"):
    assert keep not in span_a, f"span A unexpectedly swallowed {keep}"
assert "CLOSED c3789 (was" not in span_b, "span B would breach the one-off boundary"
assert "CLOSED c3794" not in span_a and "CLOSED c3794" not in span_b
assert "CLOSED c3793" not in span_a and "CLOSED c3793" not in span_b
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span_a, re.M), "SPAN A CONTAINS AN OPEN ITEM -- refusing"
assert not re.search(r"^- \[ \] \*\*", span_b, re.M), "SPAN B CONTAINS AN OPEN ITEM -- refusing"

# ---- GUARD 2 (c3724/c3748): promote nested actionables, never strand ----------
# A nested `NEW cNNNN` hit is exempt only if the text immediately names it CLOSED/SHIPPED
# in the same breath (already-resolved narrative, e.g. "`NEW c3784` CLOSED -- both hooks
# are now gated..." inside the c3790 block) -- that is a historical record, not a live
# actionable, and its real top-level definition lives elsewhere, outside both spans.
RESOLVED_NEARBY = re.compile(r"`?NEW c\d+[a-z]?`?\s+(CLOSED|SHIPPED)\b")
for name, span in (("A", span_a), ("B", span_b)):
    nested_lines = [l for l in span.split("\n") if NESTED.match(l)]
    live = [l for l in nested_lines if not RESOLVED_NEARBY.search(l)]
    found = sorted(NESTED.match(l).group(1) for l in live)
    assert found == [], f"span {name} unexpected nested set {found} -- promotion needed"

CLOSURE_NOTE = (
    "- [x] **CLOSED c3792 (the overdue `tasks/queue.md` trim this item flagged HIGH) "
    "-- done at c3795, see this cycle's own `CLOSED c3795` report block above and "
    "`bin/_trim3795q.py`.**\n"
)

# ---- build the new live file in MEMORY (verify, THEN write) -------------------
new_text = orig[:a_start] + CLOSURE_NOTE + orig[a_end:b_start] + orig[b_end:]

archive_text = (
    "\n## Archived by cycle 3795 (floor-3 rotation, TWO non-contiguous spans --\n"
    "## span A: CLOSED c3792; span B: CLOSED c3791/c3790/c3789(report)/c3788/c3787/\n"
    "## c3786/SHIPPED-c3786/c3785/c3784/c3783/c3782/c3779 -- 0 nested actionables\n"
    "## found in either span, nothing to promote; the three live \"see CLOSED cNNNN\n"
    "## above\" pointers left in the file (NEW c3744a/c3744b/the c3784 gate-closure)\n"
    "## now resolve here per NEW c3492's standing ruling, not edited)\n\n"
    + span_a.rstrip("\n") + "\n\n" + span_b.rstrip("\n") + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

# nb(new_text) + nb(span_a+span_b) == nb(orig) + the one new closure line.
removed = Counter(nb(span_a)) + Counter(nb(span_b))
kept_check = Counter(nb(new_text)) + removed - Counter(nb(CLOSURE_NOTE))
assert kept_check == Counter(nb(orig)), "LOSSLESS CHECK FAILED"
assert span_a.rstrip("\n") in archive_text
assert span_b.rstrip("\n") in archive_text
for cyc in ("3792", "3791", "3790", "3788", "3787", "3786", "3785", "3784", "3783", "3782", "3779"):
    assert f"c{cyc}" in archive_text

open(QUEUE, "w").write(new_text)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_text)} bytes (-{len(orig)-len(new_text)})")
print(f"   span A {len(span_a)}B (1 block), span B {len(span_b)}B (11 blocks)")
