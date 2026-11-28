#!/root/agent/venv/bin/python
r"""Cycle 3872 tasks/queue.md floor-3 rotation.

WHY NOW: `bin/check-doc-size` read TRIM DUE at 260.3KB/1058 lines against its
own 225KB trim line for this file, with NEGATIVE headroom (~-7 cycles at
+5440 B/cycle) -- and after this cycle's own block was prepended the file
passed 271KB, i.e. past the 256KB Read cap, so the next cycle could not have
read it whole. Clone of `bin/_trim3855q.py` BY NAME (STANDING c3280 lesson 2:
never clone the newest `_trim*q.py` on disk), re-verified it still carries the
c3748 widened GUARD-2 regex and the c3724 "promote nested, never strand" guard.

CENSUS RE-DERIVED FRESH (STANDING c3280 lesson 1: never forward a count, and
classify each head rather than trusting a bare grep). Grepped
`^- \[x\] \*\*CLOSED c\d+ -- (BUILD|QUALITY) slot` fresh: exactly 16 report
blocks live, by cycle id 3872, 3871, 3870, 3869, 3868, 3867, 3865, 3864, 3863,
3862, 3860, 3859, 3858, 3856, 3854, 3853. Deliberately NOT in the pool (they
are one-off item closures, not "-- slot" report blocks, same classification
call _trim3855q.py made for c3849): `CLOSED c3855`, `CLOSED c3856a by c3857`,
`CLOSED c3848a by c3854`, `CLOSED c3848b by c3856` and every other
`CLOSED cNNNNx by cMMMM` head. Floor 3 (STANDING c3280 / c3672 ruling) = keep
the newest 2 by cycle id (3871, 3870) plus the running cycle's own block
(3872), so the other 13 rotate.

File-order position decides the CUT SHAPE, not the keep decision. The 13
rotating blocks fall into THREE contiguous spans, because two live open items
and two live one-off closures sit between them and must stay live, untouched:
  SPAN A = c3869/c3868/c3867/c3865/c3864/c3863/c3862/c3860
           (bounded before by the kept c3870 block, after by the live open
           item `NEW c3860a`).
  SPAN B = c3859/c3858/c3856
           (bounded before by `NEW c3860a`, after by the live one-off closure
           `CLOSED c3856a by c3857`).
  SPAN C = c3854/c3853
           (bounded before by the live `CLOSED c3855` one-off closure -- with
           the live open item `NEW c3856b` and `CLOSED c3856a` above it --
           after by the live `CLOSED c3848a by c3854` closure).

HAZARD GREP (run before writing this script):
(a) whole-repo grep for the 13 ids outside queue.md/queue_archive.md: hits are
    all self-contained history -- prior `bin/_trim*.py` / `bin/_rec*.py`
    docstrings citing them as precedent, and `state/STATUS.md`'s own per-cycle
    blocks (which keep the full narrative independently). No customer-facing
    hit, nothing that needs the live queue.md narrative to resolve.
(b) nested-actionable check: asserted BY SCRIPT per span below (GUARD 2), not
    by eye.
(c) narrative `NEW cNNNN` mentions inside the spans: asserted BY SCRIPT to
    have a live top-level copy OUTSIDE the cut, with the only permitted
    exceptions listed explicitly in KNOWN_RESOLVED_WITHIN_ROTATION below.

Verify-in-MEMORY-then-write, per the _trim3492q.py bug (1) lesson.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)
RESOLVED_NEARBY = re.compile(r"`?NEW c\d+[a-z]?`?\s*(?:--\s*)?(CLOSED|SHIPPED|RESOLVED)\b")

A_START = '- [x] **CLOSED c3869 -- BUILD slot (3869 % 3 == 2; c3868\'s own handoff mislabeled this a "QUALITY'
A_NEXT = "- [ ] **NEW c3860a (MEDIUM -- make the all-time-count restamp a standing step of the `enum_audit`"
B_START = "- [x] **CLOSED c3859 -- BUILD slot (3859 % 3 == 1; `bin/checks-due` NONE DUE, soonest `check-mo"
B_NEXT = "- [x] **CLOSED c3856a by c3857 -- measured first, as the item itself prescribed"
C_START = "- [x] **CLOSED c3854 -- BUILD slot (3854 % 3 == 2). No fleet check or audit rotation was DUE"
C_NEXT = "- [x] **CLOSED c3848a by c3854 -- `bin/enum-screen` now validates its audit-type argument"

ANCHORS = (("A", A_START, A_NEXT), ("B", B_START, B_NEXT), ("C", C_START, C_NEXT))
for _, s, n in ANCHORS:
    for anchor in (s, n):
        assert orig.count(anchor) == 1, f"anchor not unique or missing: {anchor[:70]}"

bounds = {}
for name, start, nxt in ANCHORS:
    si, ni = orig.index(start), orig.index(nxt)
    assert si < ni, f"span {name}: start not before next-anchor"
    bounds[name] = (si, ni)
span = {n: orig[s:e] for n, (s, e) in bounds.items()}

# --- boundary asserts ---------------------------------------------------
a, b, c = bounds["A"], bounds["B"], bounds["C"]
assert a[1] <= b[0] < b[1] <= c[0] < c[1], "spans out of order or overlapping"
EXPECTED = {
    "A": ["3869", "3868", "3867", "3865", "3864", "3863", "3862", "3860"],
    "B": ["3859", "3858", "3856"],
    "C": ["3854", "3853"],
}
for name, ids in EXPECTED.items():
    n_heads = len(re.findall(r"^- \[x\] \*\*CLOSED c\d+ -- (?:BUILD|QUALITY) slot", span[name], re.M))
    assert n_heads == len(ids), f"span {name} report-block count {n_heads} != {len(ids)}"
    for cyc in ids:
        assert re.search(rf"^- \[x\] \*\*CLOSED c{cyc}\b", span[name], re.M), \
            f"c{cyc} head not found in span {name}"
all_ids = [i for ids in EXPECTED.values() for i in ids]
assert len(all_ids) == 13

# the kept report blocks must be OUTSIDE every span
for keep in ("3872", "3871", "3870"):
    for name in span:
        assert not re.search(rf"^- \[[ x]\] \*\*CLOSED c{keep}\b", span[name], re.M), \
            f"c{keep} head is inside span {name} -- must be KEPT"
# the live one-off closures and open items between the spans must stay out
for must_stay in (r"^- \[ \] \*\*NEW c3860a\b", r"^- \[x\] \*\*CLOSED c3856a by c3857\b",
                  r"^- \[ \] \*\*NEW c3856b\b", r"^- \[x\] \*\*CLOSED c3855\b",
                  r"^- \[x\] \*\*CLOSED c3848a by c3854\b"):
    for name in span:
        assert not re.search(must_stay, span[name], re.M), \
            f"{must_stay} is inside span {name} -- must stay LIVE"

# --- GUARD 1: no span may hold an open item -----------------------------
for name in span:
    assert not re.search(r"^- \[ \] \*\*", span[name], re.M), \
        f"SPAN {name} CONTAINS AN OPEN ITEM -- refusing"

# --- GUARD 2 (c3724/c3748): promote nested actionables, never strand ----
EXPECTED_NESTED = {"A": [], "B": [], "C": []}
for name in span:
    nested = [l for l in span[name].split("\n") if NESTED.match(l)]
    live = [l for l in nested if not RESOLVED_NEARBY.search(l)]
    found = sorted(NESTED.match(l).group(1) for l in live)
    assert found == EXPECTED_NESTED[name], \
        f"span {name}: unexpected nested set {found} -- promotion needed"

# every narrative "NEW cNNNN" mention inside the spans must either have a live
# top-level copy OUTSIDE the spans, or be independently verified below.
mentioned = set()
for name in span:
    mentioned |= set(re.findall(r"`?NEW c(\d+[a-z]?)`?", span[name]))
outside = orig[:a[0]] + orig[a[1]:b[0]] + orig[b[1]:c[0]] + orig[c[1]:]
# Verified by direct grep before writing this script (never a bare skip):
#   3536  -- pure precedent naming ("the c3536 rule"/"the standing c3669/NEW
#            c3536 rule"); no live top-level `NEW c3536` exists anywhere in the
#            file, and the RULE itself lives in notes/PLAYBOOK.md's enum_audit
#            section, not in this queue block. Same call _trim3855q.py made.
#   3848a, 3848b, 3856a, 3844b, 3828a -- one-off items whose CLOSURES are kept
#            LIVE in this file as `CLOSED cNNNNx by cMMMM` heads outside every
#            span, so a mention inside a cut span is a pointer to a live
#            closure, not a dangling actionable.
KNOWN_RESOLVED_WITHIN_ROTATION = {"3536", "3848a", "3848b", "3856a", "3844b", "3828a"}
unresolved = []
for mid in sorted(mentioned):
    if re.search(rf"^- \[ \] \*\*`?NEW c{mid}\b", outside, re.M):
        continue
    if mid in KNOWN_RESOLVED_WITHIN_ROTATION:
        continue
    unresolved.append(mid)
assert not unresolved, (
    f"NEW c{unresolved} mentioned in a cut span with no live top-level copy outside it "
    "and not in the manually-verified resolved set -- investigate before cutting")

# --- build the new live file in MEMORY (verify, THEN write) -------------
new_text = orig
for name in ("C", "B", "A"):
    s, e = bounds[name]
    new_text = new_text[:s] + new_text[e:]

archive_text = (
    "\n## Archived by cycle 3872 (floor-3 report-block rotation -- `bin/check-doc-size`\n"
    "## read tasks/queue.md TRIM DUE at 260.3KB/1058 lines against its own 225KB line,\n"
    "## with NEGATIVE headroom, and this cycle's own prepended block pushed the file\n"
    "## past the 256KB Read cap). Census RE-DERIVED fresh: 16 report blocks were live,\n"
    "## so 13 rotate -- c3871/c3870 are the newest 2 by cycle id and stay KEPT, plus\n"
    "## this cycle's own c3872 block. THREE spans, because two live open items\n"
    "## (`NEW c3860a`, `NEW c3856b`) and three live one-off closures (`CLOSED c3856a by\n"
    "## c3857`, `CLOSED c3855`, `CLOSED c3848a by c3854`) sit between them and are kept\n"
    "## live, untouched: span A = c3869/c3868/c3867/c3865/c3864/c3863/c3862/c3860,\n"
    "## span B = c3859/c3858/c3856, span C = c3854/c3853. 0 live nested actionables\n"
    "## stranded -- every narrative NEW-c mention inside a span was confirmed BY SCRIPT\n"
    "## to have a live top-level copy outside the cut, or (NEW c3536 precedent-only;\n"
    "## c3848a/c3848b/c3856a/c3844b/c3828a, whose one-off closures stay live) verified\n"
    "## by hand first. Full narrative for every rotated cycle also survives\n"
    "## independently in state/STATUS.md and its archive.\n\n"
    + "\n\n".join(span[n].rstrip("\n") for n in ("A", "B", "C")) + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

removed = Counter()
for n in span:
    removed += Counter(nb(span[n]))
assert Counter(nb(new_text)) + removed == Counter(nb(orig)), \
    "LOSSLESS CHECK FAILED -- nothing written"
for n in span:
    assert span[n].rstrip("\n") in archive_text, f"span {n} missing from archive text"
for cyc in all_ids:
    assert f"**CLOSED c{cyc} " in archive_text, f"c{cyc} head missing from archive text"
    assert not re.search(rf"^- \[[ x]\] \*\*CLOSED c{cyc}\b", new_text, re.M), \
        f"c{cyc} head still live -- cut did not land"

for s in ("- [ ] **NEW c3860a", "- [ ] **NEW c3856b", "- [x] **CLOSED c3855",
          "- [x] **CLOSED c3856a by c3857", "- [x] **CLOSED c3848a by c3854",
          "- [ ] **NEW c3847a", "- [ ] **NEW c3824a", "- [ ] **NEW c3372"):
    assert s in new_text, f"open item/closure lost -- refusing: {s[:50]}"

def head_idx(cyc, text):
    m = re.search(rf"^- \[[ x]\] \*\*CLOSED c{cyc}\b", text, re.M)
    assert m, f"no top-level head found for c{cyc}"
    return m.start()
assert head_idx("3872", new_text) < head_idx("3871", new_text) < head_idx("3870", new_text)
assert len(re.findall(r"^- \[x\] \*\*CLOSED c\d+ -- (?:BUILD|QUALITY) slot", new_text, re.M)) == 3

with open(ARCHIVE, "a") as fh:
    fh.write(archive_text)
with open(QUEUE, "w") as fh:
    fh.write(new_text)
print(f"queue.md {len(orig)} -> {len(new_text)} bytes; archived {len(archive_text)} bytes "
      f"({len(all_ids)} report blocks, 3 spans)")
