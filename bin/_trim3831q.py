#!/root/agent/venv/bin/python
r"""Cycle 3831 tasks/queue.md floor-3 rotation -- QUALITY slot (3831 % 3 == 0).
This is `NEW c3828a`, deliberately deferred by c3828 (which spent its slot on
the grants-gov-scraper COMPETITORS.md relocation) and named by every handoff
since as the real next QUALITY-slot item. Clone of `bin/_trim3824q.py` BY NAME
as instructed; re-verified before cloning that it is anchor-keyed (not
cycle-id-dict-keyed, the c3768 trap) and carries the c3748 widened GUARD-2
regex. It does.

URGENCY, measured not inherited: `bin/check-doc-size` reads TRIM DUE at
220.7KB/1013 lines, ~1 cycle of headroom at +5440 B/cycle (proj. 348KB at the
next 24-cycle look). Floor is 200.9KB (107 live OPEN items, not rotatable) +
19.8KB rotatable above floor-3 -- a full rotation lands exactly there and
CLEARS the 225KB line.

CENSUS RE-DERIVED FRESH (STANDING c3280's lesson: never forward a count).
Per-block scan of the live file's top-level heads, classified report-block
(the per-cycle "CLOSED cNNNN -- BUILD/QUALITY slot" narrative) vs one-off ITEM
closure per the c3745/c3748 distinction:

  REPORT BLOCKS live (9): c3830, c3829, c3828, c3827, c3826, c3825, c3824,
  c3823, c3822. Floor 3 (STANDING c3280/c3672) = keep the newest 2 + the
  running cycle's own new block. c3830 and c3829 are the newest 2 and are
  KEPT, so the other **7** (c3828 down through c3822) rotate.

  ONE-OFF ITEM CLOSURES immediately after this span (c3820a, c3820b at the
  live lines just past c3822) are NOT report blocks and are NOT touched --
  out of the rotation pool by rule, same as every prior rotation.

WHY A THREE-SPAN CUT: the 7 rotating report blocks are NOT contiguous --
two live OPEN items sit inside the range and must survive untouched:
  `NEW c3828a` (this item) and `NEW c3828b` divide c3828 from c3827;
  `NEW c3824a` divides c3824 from c3823.
Three spans, each independently asserted, rather than one span that would
swallow live open items (GUARD 1 refuses that anyway).

HAZARD GREP (3-pass, run before writing this script):
(a)/(b) whole-repo grep for c3822 c3823 c3824 c3825 c3826 c3827 c3828 outside
    queue.md/queue_archive.md. Every hit is a SELF-CONTAINED history record:
    `state/STATUS.md` + `state/STATUS_ARCHIVE.md` per-cycle entries,
    `notes/LEARNINGS.md` durable lessons, `bin/check-doc-size`'s own docstring
    citing c3822/c3824, `bin/_trim3824q.py`'s docstring citing c3822/c3823.
    No customer-facing hit, nothing needing the live queue.md narrative.
(c) intra-file: GUARD 2 below re-asserts by script that no live
    `NEW cNNNNa`-shaped nested sub-bullet is stranded in any span. A direct
    grep of lines 5-41 for an indented `NEW c` bullet start found none --
    EXPECTED_NESTED is empty for all three spans.
Backward narrative mentions of these cycle ids inside the KEPT c3830/c3829
blocks ("git log ... names c3829/c3828") are passing mentions, not "see
CLOSED cNNNN above" pointers -- NEW c3492's standing ruling covers this shape
(resolves in the archive).
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)
RESOLVED_NEARBY = re.compile(r"`?NEW c\d+[a-z]?`?\s*(?:--\s*)?(CLOSED|SHIPPED|RESOLVED)\b")

# SPAN A = report block c3828 alone; ends at the open NEW c3828a.
# SPAN B = report blocks c3827, c3826, c3825, c3824; ends at the open NEW c3824a.
# SPAN C = report blocks c3823, c3822; ends at the one-off closure CLOSED c3820a.
A_START = "- [x] **CLOSED c3828 -- QUALITY slot (3828 % 3 == 0)"
A_NEXT = "- [ ] **NEW c3828a (HIGH, next QUALITY slot"
B_START = "- [x] **CLOSED c3827 -- BUILD slot. Closed the oldest DUE `competitor_audit` rotation: twenty-first sweep"
B_NEXT = "- [ ] **NEW c3824a (MEDIUM, and it is now the ONLY lever"
C_START = "- [x] **CLOSED c3823 -- BUILD slot (3823 % 3 == 1)"
C_NEXT = "- [x] **CLOSED c3820a by c3828"

for s in (A_START, A_NEXT, B_START, B_NEXT, C_START, C_NEXT):
    assert orig.count(s) == 1, f"anchor not unique: {s[:60]}"

bounds = {}
for name, start, nxt in (("A", A_START, A_NEXT), ("B", B_START, B_NEXT), ("C", C_START, C_NEXT)):
    bounds[name] = (orig.index(start), orig.index(nxt))
span = {n: orig[s:e] for n, (s, e) in bounds.items()}

# --- boundary asserts: a drifted line must fail loudly, never cut the wrong place ---
a, b, c = bounds["A"], bounds["B"], bounds["C"]
assert a[0] < a[1] <= b[0] < b[1] <= c[0] < c[1], "spans out of order or overlapping"
# c3748 lesson: anchor to a top-level HEAD, never bare narrative text.
for name, n in (("A", 1), ("B", 4), ("C", 2)):
    got = span[name].count("\n- [x] **CLOSED c") + 1
    assert got == n, f"span {name} block count unexpected: {got} != {n}"
# the kept newest-2 report blocks must not be inside any span.
for keep in ("3830", "3829"):
    for name in span:
        assert not re.search(rf"^- \[[ x]\] \*\*CLOSED c{keep}\b", span[name], re.M), \
            f"c{keep} head is inside span {name} -- must be KEPT"

# --- GUARD 1: no span may hold an open item ---------------------------------------
for name in span:
    assert not re.search(r"^- \[ \] \*\*", span[name], re.M), \
        f"SPAN {name} CONTAINS AN OPEN ITEM -- refusing"

# --- GUARD 2 (c3724/c3748): promote nested actionables, never strand --------------
EXPECTED_NESTED = {"A": [], "B": [], "C": []}
for name in span:
    nested = [l for l in span[name].split("\n") if NESTED.match(l)]
    live = [l for l in nested if not RESOLVED_NEARBY.search(l)]
    found = sorted(NESTED.match(l).group(1) for l in live)
    assert found == EXPECTED_NESTED[name], \
        f"span {name}: unexpected nested set {found} -- promotion needed"

# --- build the new live file in MEMORY (verify, THEN write) -----------------------
new_text = orig
for name in ("C", "B", "A"):
    s, e = bounds[name]
    new_text = new_text[:s] + new_text[e:]

archive_text = (
    "\n## Archived by cycle 3831 (floor-3 report-block rotation -- NEW c3828a, deferred by\n"
    "## c3828 and named by every handoff since as the real next QUALITY-slot item). Census\n"
    "## RE-DERIVED: 9 report blocks were live, so 7 rotate (c3830/c3829 are the newest 2 and\n"
    "## stay KEPT, plus this cycle's own new block). THREE spans, because two live open items\n"
    "## sit between them: span A = c3828 alone (ends at NEW c3828a), span B = c3827/c3826/\n"
    "## c3825/c3824 (ends at NEW c3824a), span C = c3823/c3822 (ends at the one-off closure\n"
    "## CLOSED c3820a, itself untouched). Live report-block pool left exactly at floor 3.\n"
    "## 0 live nested actionables stranded -- a direct grep of the cut range for an indented\n"
    "## NEW c bullet start found none. Driver: 220.7KB live, ~1 cycle of headroom at\n"
    "## +5440 B/cycle against the 225KB override line.)\n\n"
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
for cyc in ("c3828", "c3827", "c3826", "c3825", "c3824", "c3823", "c3822"):
    assert f"**CLOSED {cyc} " in archive_text, f"{cyc} head missing from archive text"
    assert not re.search(rf"^- \[[ x]\] \*\*CLOSED {cyc}\b", new_text, re.M), \
        f"{cyc} head still live -- cut did not land"
def head_idx(cyc):
    m = re.search(rf"^- \[[ x]\] \*\*CLOSED c{cyc}\b", new_text, re.M)
    assert m, f"no top-level head found for c{cyc}"
    return m.start()
assert head_idx("3830") < head_idx("3829") < head_idx("3792")
for s in (A_NEXT, B_NEXT, C_NEXT, "- [ ] **NEW c3828b (LOW).**"):
    assert s in new_text, f"open item lost -- refusing: {s[:50]}"

with open(ARCHIVE, "a") as fh:
    fh.write(archive_text)
with open(QUEUE, "w") as fh:
    fh.write(new_text)

print(f"queue.md {len(orig):,}B -> {len(new_text):,}B  ({len(new_text) - len(orig):+,}B)")
print(f"lines {orig.count(chr(10)):,} -> {new_text.count(chr(10)):,}")
for n in ("A", "B", "C"):
    print(f"span {n}: {len(span[n]):,}B")
print(f"archived {len(archive_text):,}B under '## Archived by cycle 3831'")
print(f"Read-cap headroom now {262144 - len(new_text):,}B (~{(262144 - len(new_text)) // 5440} cycles at +5440 B/cycle)")
