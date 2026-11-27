#!/root/agent/venv/bin/python
r"""Cycle 3816 tasks/queue.md rotation -- QUALITY slot (3816 % 3 == 0),
check-doc-size read TRIM DUE at 249.5KB/-9c headroom (file is 255,452B, i.e.
~0.5KB under the 256KB Read cap -- next cycle could not have Read it at all,
so this is the urgent item of the slot). Clone of `_trim3807q.py`, which is
the live descendant of the mandated `_trim3748q.py` lineage; re-verified
before cloning that it carries the c3748 widened GUARD-2 regex (it does) and
that it is anchor-keyed, not cycle-id-dict-keyed (the c3768 trap).

CENSUS RE-DERIVED FRESH (not inherited -- STANDING c3280's first and second
durable lessons: a forwarded count both UNDER- and OVER-counts). A per-block
byte census of all 130 top-level heads in the live file, each classified
report-block vs one-off ITEM closure per the c3745/c3748 distinction:

  REPORT BLOCKS live (9): c3813, c3812, c3811, c3810, c3809, c3808, c3807,
  c3804, c3803.  Floor 3 (STANDING c3280 / c3672, cannot be cut again) =
  keep newest 2 + the running cycle's own block. c3815 and c3814 are the
  newest 2 and are KEPT, so all 9 above are above the floor and rotate.

  ONE-OFF ITEM CLOSURES live (16, ~28.6KB) -- the `NEW c3768` lever, out of
  the rotation pool by rule and never rotated by anything. This cycle spends
  exactly ONE of them, the newest and by far the largest: `CLOSED c3808a`
  (11,690B), which `state/STATUS.md` records as **fully CLOSED at c3815**
  (all 6 over-cap Actors fixed and verified live across c3809-c3815, fleet
  `check-readme-cap` now 0 RED). The other 15 are small (235B-2,396B) and
  each needs its own hazard pass; left for the next QUALITY slot, see the
  `NEW c3816a` note filed in the live file.

WHY A TWO-SPAN CUT: `NEW c3812a` (idx 8) is an OPEN item that sits BETWEEN
the c3808 report block and the c3808a item closure, so the harvest is not
contiguous. Two spans, each independently asserted, rather than one span
that would swallow a live open item (GUARD 1 would have refused anyway).

HAZARD GREP (3-pass, run before this script was written):
(a)/(b) whole-repo grep for each of `c3803 c3804 c3807 c3808a c3809 c3810
    c3811 c3812 c3813` outside queue.md/queue_archive.md. Every hit is a
    SELF-CONTAINED history record needing no queue.md narrative to resolve:
    `state/STATUS.md` + `state/STATUS_ARCHIVE.md` per-cycle entries;
    `notes/LEARNINGS.md` durable lessons; `state/fleet_checks.json` check
    records; prior trim-script docstrings (`_trim3804q.py`, `_trim3807q.py`,
    `_trim3756q.py`, `_trim3552q.py`, `_trim3714q.py`, `_trim3714s.py`)
    citing the ids as history. c3808a additionally appears in six live Actor
    `README.md`/`COMPETITORS.md` files -- those are PROVENANCE STAMPS on the
    cap-fix relocations ("moved by c3808a"), customer-facing disclosure, not
    pointers into the queue block. Nothing to relocate.
(c) intra-file: GUARD 2 below re-asserts by script that no live
    `NEW cNNNNa`-shaped nested sub-bullet is stranded in either span, so a
    drifted boundary cannot cut a different block cosmetically. Note the one
    nested actionable this effort produced, `NEW c3812a`, was ALREADY
    PROMOTED to a top-level open item by c3812 and is explicitly outside
    both spans (it is the divider between them).
Backward narrative references to these cycle ids inside the KEPT c3815/c3814
blocks ("Continued `NEW c3808a`", "git log ... names c3814") are passing
mentions of a cycle number, not "see CLOSED cNNNN above" pointers -- NEW
c3492's standing ruling already covers this shape (resolves in the archive).
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)
RESOLVED_NEARBY = re.compile(r"`?NEW c\d+[a-z]?`?\s*(?:--\s*)?(CLOSED|SHIPPED|RESOLVED)\b")

# SPAN A = the 6 contiguous report blocks c3813..c3808, ending at the open
# NEW c3812a item.  SPAN B = c3808a + the 3 report blocks c3807/c3804/c3803,
# ending at the small CLOSED c3792 stub (kept: it is the anchor the c3807
# rotation also used, and its 548B is not worth a fresh hazard pass).
A_START = "- [x] **CLOSED c3813 -- QUALITY slot (3813 % 3 == 0)"
A_NEXT = "- [ ] **NEW c3812a (LOW-MEDIUM, a decision to make, not a bug to fix"
B_START = "- [x] **CLOSED c3808a (was HIGH, CONFIRMED DEFECT, revenue-facing"
B_NEXT = "- [x] **CLOSED c3792 -- the overdue `tasks/queue.md` trim this item flagged HIGH"

for s in (A_START, A_NEXT, B_START, B_NEXT):
    assert orig.count(s) == 1, f"anchor not unique: {s[:60]}"

a_start, a_end = orig.index(A_START), orig.index(A_NEXT)
b_start, b_end = orig.index(B_START), orig.index(B_NEXT)
span_a, span_b = orig[a_start:a_end], orig[b_start:b_end]

# --- boundary asserts: a drifted line must fail loudly, never cut the wrong place ---
assert a_start < a_end <= b_start < b_end, "spans out of order or overlapping"
# c3748 lesson: anchor to a top-level HEAD, never bare narrative text.
for name, span, n in (("A", span_a, 6), ("B", span_b, 4)):
    got = span.count("\n- [x] **CLOSED c") + 1
    assert got == n, f"span {name} block count unexpected: {got} != {n}"
# the kept newest-2 report blocks must not be inside either span. c3748/c3804
# lesson: test for a top-level HEAD, never a bare substring -- span B's c3808a
# block legitimately says "Full detail in the `CLOSED c3814` block at the top of
# this file", a FORWARD pointer to a block that stays live (so it still resolves
# from the archive; only the words "this file" go loose, which NEW c3492 covers).
for keep in ("3815", "3814"):
    for name, span in (("A", span_a), ("B", span_b)):
        assert not re.search(rf"^- \[[ x]\] \*\*CLOSED c{keep}\b", span, re.M), \
            f"c{keep} head is inside span {name} -- must be KEPT"

# --- GUARD 1: neither span holds an open item ---
for name, span in (("A", span_a), ("B", span_b)):
    assert not re.search(r"^- \[ \] \*\*", span, re.M), \
        f"SPAN {name} CONTAINS AN OPEN ITEM -- refusing"

# --- GUARD 2 (c3724/c3748): promote nested actionables, never strand -------------
for name, span in (("A", span_a), ("B", span_b)):
    nested = [l for l in span.split("\n") if NESTED.match(l)]
    live = [l for l in nested if not RESOLVED_NEARBY.search(l)]
    found = sorted(NESTED.match(l).group(1) for l in live)
    assert found == [], f"span {name}: unexpected nested set {found} -- promotion needed"

# --- build the new live file in MEMORY (verify, THEN write) ----------------------
# cut the LATER span first so the earlier span's offsets stay valid
new_text = orig[:b_start] + orig[b_end:]
new_text = new_text[:a_start] + new_text[a_end:]

archive_text = (
    "\n## Archived by cycle 3816 (floor-3 report-block rotation PLUS the first spend of\n"
    "## the `NEW c3768` one-off-ITEM-closure lever. TWO spans, because the open item\n"
    "## `NEW c3812a` sits between them. Span A = the 6 report blocks c3813/c3812/c3811/\n"
    "## c3810/c3809/c3808; span B = `CLOSED c3808a` (11,690B, recorded fully CLOSED at\n"
    "## c3815 -- all 6 over-cap Actors fixed, fleet check-readme-cap 0 RED) plus the 3\n"
    "## report blocks c3807/c3804/c3803. Live pool left exactly at floor 3: c3815,\n"
    "## c3814 + this cycle's own block. 0 nested actionables stranded in either span\n"
    "## (`NEW c3812a` was already promoted top-level by c3812). 15 smaller one-off\n"
    "## closures (~16.9KB) deliberately NOT cut -- each needs its own hazard pass, see\n"
    "## `NEW c3816a` in the live file.)\n\n"
    + span_a.rstrip("\n") + "\n\n" + span_b.rstrip("\n") + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

# nb(new) + nb(removed) == nb(orig)  (compare BY VALUE, not by count)
removed = Counter(nb(span_a)) + Counter(nb(span_b))
assert Counter(nb(new_text)) + removed == Counter(nb(orig)), \
    "LOSSLESS CHECK FAILED -- nothing written"
assert span_a.rstrip("\n") in archive_text and span_b.rstrip("\n") in archive_text
for cyc in ("c3813", "c3812", "c3811", "c3810", "c3809", "c3808a", "c3807", "c3804", "c3803"):
    assert cyc in archive_text, f"{cyc} missing from archive text"
# the kept blocks must still head the live file (anchor to actual top-level HEADS,
# not bare substrings -- kept narrative mentions cycle ids in passing)
def head_idx(cyc):
    m = re.search(rf"^- \[[ x]\] \*\*CLOSED c{cyc}\b", new_text, re.M)
    assert m, f"no top-level head found for c{cyc}"
    return m.start()
assert head_idx("3815") < head_idx("3814") < head_idx("3792")
# and the open item that divided the spans must survive
assert A_NEXT in new_text, "NEW c3812a was lost -- refusing"

with open(ARCHIVE, "a") as fh:
    fh.write(archive_text)
with open(QUEUE, "w") as fh:
    fh.write(new_text)

print(f"queue.md {len(orig):,}B -> {len(new_text):,}B  ({len(new_text) - len(orig):+,}B)")
print(f"lines {orig.count(chr(10)):,} -> {new_text.count(chr(10)):,}")
print(f"span A {len(span_a):,}B (6 report blocks), span B {len(span_b):,}B (c3808a + 3 report blocks)")
print(f"archived {len(archive_text):,}B under '## Archived by cycle 3816'")
