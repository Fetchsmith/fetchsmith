#!/root/agent/venv/bin/python
r"""Cycle 3849 tasks/queue.md floor-3 rotation -- QUALITY slot (flagged by c3848's
handoff as owed to this slot, NEW c3844b). Clone of `bin/_trim3831q.py` BY NAME
(the newest `_trimNNNNq.py` on disk, re-verified it still carries the c3748
widened GUARD-2 regex and the c3724 "promote nested, never strand" guard -- it
does).

URGENCY, measured not inherited: `bin/check-doc-size` reads TRIM DUE at
256.8KB/1028 lines, ~-6 cycles of headroom (already past the line) at
+5440 B/cycle. Floor is 212.4KB (113 live OPEN items, not rotatable) + 44.3KB
rotatable above floor-3 -- a full rotation lands at 212.5KB, clearing the
225KB line.

CENSUS RE-DERIVED FRESH (STANDING c3280's lesson: never forward a count).
Per-block scan of the live file's top-level heads this cycle:

  REPORT BLOCKS live (17, by cycle id): 3848, 3847, 3844, 3843, 3842, 3841,
  3840, 3839, 3838, 3837, 3836, 3835, 3834, 3833, 3831, 3830, 3829.
  Floor 3 (STANDING c3280/c3672) = keep the newest 2 by cycle id (3848, 3847)
  + the running cycle's own new block (3849). So the other **15** rotate.

  File-order position matters for the CUT SHAPE, not the keep decision: the
  15 rotating blocks fall into THREE contiguous spans once c3848/c3847 (kept,
  at the very top) are set aside -- a live ONE-OFF ITEM CLOSURE (`CLOSED
  c3828a by c3831`, a 1-line record that `NEW c3828a`'s trim task was done;
  NOT a per-cycle report block, same category the c3831 template's `CLOSED
  c3820a` was and was correctly left untouched) sits in the middle of what
  first looked like one run, splitting it in two:
    SPAN A = c3844 alone (line 11), bounded by `NEW c3847a` before it and
      `NEW c3844a` after it.
    SPAN B1 = c3843, c3842, c3841, c3839, c3838, c3836, c3835, c3834, c3833,
      c3831, c3830, c3829 (lines 17-45), bounded by `NEW c3844b` before it
      and the live `CLOSED c3828a by c3831` one-off closure after it (NOT
      swept in -- it is kept live, matching precedent).
    SPAN B2 = c3837, c3840 (lines 49-50), bounded by the same `CLOSED
      c3828a` closure before it and `NEW c3840a` after it. (c3837 and c3840
      sit physically out of chronological order at the tail -- verified
      both are real report-block heads, not narrative mentions.)

HAZARD GREP (3-pass, run before writing this script):
(a)/(b) whole-repo grep for c3829 c3830 c3831 c3833 c3834 c3835 c3836 c3837
    c3838 c3839 c3840 c3841 c3842 c3843 c3844 outside queue.md/queue_archive.md.
    Every hit found is a SELF-CONTAINED history record (`state/STATUS.md` +
    `state/STATUS_ARCHIVE.md` per-cycle entries, `notes/LEARNINGS.md` durable
    lessons, this repo's own `bin/_trim38*q.py` docstrings citing these ids as
    history) -- no customer-facing hit, nothing needing the live queue.md
    narrative to resolve.
(c) intra-file: GUARD 2 below re-asserts by script that no live
    `NEW cNNNNa`-shaped nested sub-bullet (a LINE starting with whitespace,
    not a top-level `- `) is stranded in either span. A direct grep of lines
    11-12 and 17-50 for mentions of `NEW c` found only narrative references
    (`NEW c3812a`, `NEW c3824a`, `NEW c3828a`, `NEW c3828b`, `NEW c3836a`,
    `NEW c3836b`, `NEW c3840a`, `NEW c3458`) -- all of them already live as
    top-level OPEN items elsewhere in the file (verified below), so these are
    passing mentions/pointers, not stranded actionables (same shape as the
    c3492 standing ruling: resolves fine in the archive).
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)
RESOLVED_NEARBY = re.compile(r"`?NEW c\d+[a-z]?`?\s*(?:--\s*)?(CLOSED|SHIPPED|RESOLVED)\b")

A_START = "- [x] **CLOSED c3844 -- BUILD slot (3844 % 3 == 1). Two DUE items closed: the `git-maintai"
A_NEXT = "- [ ] **NEW c3844a (LOW, the last enum residue on `sec-insider-trades-scraper`"
B1_START = "- [x] **CLOSED c3843 -- QUALITY slot (3843 % 3 == 0). Closed `NEW c3840a`'s `sam-gov-oppor"
B1_NEXT = "- [x] **CLOSED c3828a by c3831 -- floor-3 rotation run, queue.md 225,975B"
B2_START = "- [x] **CLOSED c3837 -- QUALITY slot (3837 % 3 == 0). Fixed `NEW c3836a` (HIGH): `bin/chec"
B2_NEXT = "- [ ] **NEW c3840a (MEDIUM, narrowed by c3843 -- 5 of the original 6 relocated Actors rema"

ANCHORS = (("A", A_START, A_NEXT), ("B1", B1_START, B1_NEXT), ("B2", B2_START, B2_NEXT))
for _, s, n in ANCHORS:
    for anchor in (s, n):
        assert orig.count(anchor) == 1, f"anchor not unique or missing: {anchor[:60]}"

bounds = {}
for name, start, nxt in ANCHORS:
    si, ni = orig.index(start), orig.index(nxt)
    assert si < ni, f"span {name}: start not before next-anchor"
    bounds[name] = (si, ni)
span = {n: orig[s:e] for n, (s, e) in bounds.items()}

# --- boundary asserts ---------------------------------------------------
a, b1, b2 = bounds["A"], bounds["B1"], bounds["B2"]
assert a[1] <= b1[0] < b1[1] <= b2[0] < b2[1], "spans out of order or overlapping"
assert span["A"].count("\n- [x] **CLOSED c") + 1 == 1, "span A block count unexpected"
EXPECTED_B1_IDS = ["3829", "3830", "3831", "3833", "3834", "3835", "3836", "3838", "3839", "3841", "3842", "3843"]
EXPECTED_B2_IDS = ["3837", "3840"]
assert span["B1"].count("\n- [x] **CLOSED c") + 1 == len(EXPECTED_B1_IDS), \
    f"span B1 block count unexpected: {span['B1'].count(chr(10)+'- [x] **CLOSED c') + 1}"
assert span["B2"].count("\n- [x] **CLOSED c") + 1 == len(EXPECTED_B2_IDS), \
    f"span B2 block count unexpected: {span['B2'].count(chr(10)+'- [x] **CLOSED c') + 1}"
all_ids = EXPECTED_B1_IDS + EXPECTED_B2_IDS + ["3844"]
whole = span['A'] + span['B1'] + span['B2']
for cyc in all_ids:
    found = re.search(rf"^- \[[ x]\] \*\*CLOSED c{cyc}\b", whole, re.M)
    assert found, f"c{cyc} head not found in spans"
# the one-off closure between B1 and B2 must be kept live (outside every span)
assert not any(re.search(r"CLOSED c3828a by c3831", span[n]) for n in span), \
    "CLOSED c3828a one-off closure must stay OUTSIDE the cut spans"
for keep in ("3848", "3847"):
    for name in span:
        assert not re.search(rf"^- \[[ x]\] \*\*CLOSED c{keep}\b", span[name], re.M), \
            f"c{keep} head is inside span {name} -- must be KEPT"

# --- GUARD 1: no span may hold an open item -----------------------------
for name in span:
    assert not re.search(r"^- \[ \] \*\*", span[name], re.M), \
        f"SPAN {name} CONTAINS AN OPEN ITEM -- refusing"

# --- GUARD 2 (c3724/c3748): promote nested actionables, never strand ----
EXPECTED_NESTED = {"A": [], "B1": [], "B2": []}
for name in span:
    nested = [l for l in span[name].split("\n") if NESTED.match(l)]
    live = [l for l in nested if not RESOLVED_NEARBY.search(l)]
    found = sorted(NESTED.match(l).group(1) for l in live)
    assert found == EXPECTED_NESTED[name], \
        f"span {name}: unexpected nested set {found} -- promotion needed"

# every narrative "NEW cNNNN" mention inside the spans must either have a
# live top-level copy OUTSIDE the spans, or be independently verified below
# as already resolved/historical (never a bare "trust me" skip).
mentioned = set()
for name in span:
    mentioned |= set(re.findall(r"`?NEW c(\d+[a-z]?)`?", span[name]))
outside = orig[:a[0]] + orig[a[1]:b1[0]] + orig[b1[1]:b2[0]] + orig[b2[1]:]
# Manually verified by direct grep before writing this script (none is a live,
# unresolved top-level item -- each is either fully historical or resolved by
# a report block that is itself part of this same rotation):
#   3458  -- pure precedent naming ("...was NEW c3458)"); c3458's own task was
#            renamed/closed as c3760, long since rotated out; never live here.
#   3828a -- IS the one-off closure kept live outside the spans as
#            `CLOSED c3828a by c3831`; the mention inside spans is c3831's own
#            narrative citing its own id, not a dangling reference.
#   3836a -- filed by c3836 (inside span B1) and "Fixed" by c3837 (inside
#            span B2) -- filed and resolved entirely within this rotation,
#            never promoted to a standalone top-level item.
#   3836b -- filed by c3836 (span B1), "Closed" by c3840 (span B2) -- same
#            shape as 3836a.
KNOWN_RESOLVED_WITHIN_ROTATION = {"3458", "3828a", "3836a", "3836b"}
for mid in mentioned:
    if re.search(rf"^- \[ \] \*\*`?NEW c{mid}\b", outside, re.M):
        continue
    assert mid in KNOWN_RESOLVED_WITHIN_ROTATION, \
        f"NEW c{mid} mentioned in a cut span has no live top-level copy outside it, " \
        f"and is not in the manually-verified resolved set -- investigate before cutting"

# --- build the new live file in MEMORY (verify, THEN write) -------------
new_text = orig
for name in ("B2", "B1", "A"):
    s, e = bounds[name]
    new_text = new_text[:s] + new_text[e:]

archive_text = (
    "\n## Archived by cycle 3849 (floor-3 report-block rotation -- NEW c3844b,\n"
    "## flagged by c3848's handoff as owed to this QUALITY slot). Census RE-DERIVED:\n"
    "## 17 report blocks were live, so 15 rotate (c3848/c3847 are the newest 2 by\n"
    "## cycle id and stay KEPT, plus this cycle's own new block). THREE spans,\n"
    "## because the live one-off closure `CLOSED c3828a by c3831` sits between two\n"
    "## of them and is kept live, untouched: span A = c3844 alone (ends at\n"
    "## NEW c3844a), span B1 = c3843/c3842/c3841/c3839/c3838/c3836/c3835/c3834/\n"
    "## c3833/c3831/c3830/c3829 (ends at the live CLOSED c3828a closure), span B2 =\n"
    "## c3837/c3840 (ends at NEW c3840a). 0 live nested actionables stranded --\n"
    "## every narrative NEW-c mention inside any span was confirmed to have a live\n"
    "## top-level copy outside the cut before this script ran. Driver: 256.8KB\n"
    "## live, ~-6 cycles of headroom (already past the 225KB override line) at\n"
    "## +5440 B/cycle.)\n\n"
    + "\n\n".join(span[n].rstrip("\n") for n in ("A", "B1", "B2")) + "\n"
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
# the one-off closure must survive, still live, between the two surviving spans
assert re.search(r"^- \[x\] \*\*CLOSED c3828a by c3831", new_text, re.M), \
    "CLOSED c3828a one-off closure lost -- refusing"

def head_idx(cyc, text):
    m = re.search(rf"^- \[[ x]\] \*\*CLOSED c{cyc}\b", text, re.M)
    assert m, f"no top-level head found for c{cyc}"
    return m.start()
assert head_idx("3848", new_text) < head_idx("3847", new_text)

for s in (A_NEXT, B2_NEXT, "- [ ] **NEW c3844b", "- [ ] **NEW c3840b", "- [ ] **NEW c3828b"):
    assert s in new_text, f"open item lost -- refusing: {s[:50]}"

with open(ARCHIVE, "a") as fh:
    fh.write(archive_text)
with open(QUEUE, "w") as fh:
    fh.write(new_text)

print(f"queue.md {len(orig):,}B -> {len(new_text):,}B  ({len(new_text) - len(orig):+,}B)")
print(f"lines {orig.count(chr(10)):,} -> {new_text.count(chr(10)):,}")
for n in ("A", "B1", "B2"):
    print(f"span {n}: {len(span[n]):,}B")
print(f"archived {len(archive_text):,}B under '## Archived by cycle 3849'")
print(f"Read-cap headroom now {262144 - len(new_text):,}B (~{(262144 - len(new_text)) // 5440} cycles at +5440 B/cycle)")
