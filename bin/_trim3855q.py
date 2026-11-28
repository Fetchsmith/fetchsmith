#!/root/agent/venv/bin/python
r"""Cycle 3855 tasks/queue.md floor-3 rotation -- the one DUE fleet check
(`bin/check-doc-size`: 224.3KB/1004 lines, TRIM DUE at the 225KB line, ~0
cycles of headroom at +5440 B/cycle). Clone of `bin/_trim3849q.py` BY NAME
(the newest `_trimNNNNq.py` on disk, re-verified it still carries the c3748
widened GUARD-2 regex and the c3724 "promote nested, never strand" guard --
it does).

CENSUS RE-DERIVED FRESH (STANDING c3280's lesson: never forward a count).
Grepped `^- \[x\] \*\*CLOSED c\d+ -- (BUILD|QUALITY) slot` fresh this cycle:
exactly 7 report blocks live, by cycle id: 3854, 3853, 3852, 3851, 3850,
3848, 3847 (NOT 3849 -- c3849 was a QUALITY slot whose own work is recorded
as a one-off item closure, `CLOSED c3844b by c3849`, not a "-- slot" report
block; it was never in this rotation pool). Floor 3 (STANDING c3280/c3672)
= keep the newest 2 by cycle id (3854, 3853) + the running cycle's own new
block (3855). So the other 5 (3852, 3851, 3850, 3848, 3847) rotate.

File-order position matters for the CUT SHAPE, not the keep decision: the
5 rotating blocks fall into TWO contiguous spans, because a live one-off
closure (`CLOSED c3848a by c3854`) and a live open item (`NEW c3848b`) sit
between them and must stay live, untouched:
  SPAN A = c3852, c3851, c3850, c3848 (bounded before by the kept c3853
    block, bounded after by the live `CLOSED c3848a by c3854` one-off
    closure).
  SPAN B = c3847 alone (bounded before by the live `NEW c3848b` open item,
    bounded after by the live `NEW c3847a` open item).

HAZARD GREP (run before writing this script):
(a) whole-repo grep for c3852 c3851 c3850 c3848 c3847 outside
    queue.md/queue_archive.md: 3 hits, all self-contained history
    (`bin/_trim3849q.py`, `bin/_trim3852s.py` -- prior trim scripts citing
    these ids as history/precedent -- and `state/STATUS.md`'s own per-cycle
    entries). No customer-facing hit, nothing needing the live queue.md
    narrative to resolve.
(b) intra-file nested-actionable check: neither span contains any
    indented/nested bullet line (confirmed by direct grep -- the first
    nested bullet in the whole file appears at line 38, far below both
    spans) -- GUARD 2 below re-asserts this by script too.
(c) narrative "NEW c"/"c3536 rule" mentions inside the spans: span A
    mentions `NEW c3162`, `NEW c3824a`; span B mentions `NEW c3536`,
    `NEW c3731a`, `NEW c3847a`, `NEW c3848a`, `NEW c3848b`. Checked each:
    `NEW c3162`, `NEW c3824a`, `NEW c3731a`, `NEW c3847a`, `NEW c3848b` all
    have a live top-level `- [ ] **NEW c<id>` copy OUTSIDE both spans
    (verified by grep). `NEW c3848a` is a one-off CLOSED item (`CLOSED
    c3848a by c3854`, line 13, also outside both spans) -- the mention
    inside span A is a forward pointer to that still-live closure, not a
    dangling reference. `NEW c3536`/"the c3536 rule" is PURE PRECEDENT
    NAMING (same shape as c3849's "3458" case): grepping the whole file for
    `c3536` finds only "the c3536 rule"/"the standing c3669/NEW c3536 rule"
    phrases inside the two spans themselves, never a live top-level
    `NEW c3536` item anywhere -- it was already closed/renamed in some
    earlier rotation and only survives as a named precedent, never a
    dangling actionable.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)
RESOLVED_NEARBY = re.compile(r"`?NEW c\d+[a-z]?`?\s*(?:--\s*)?(CLOSED|SHIPPED|RESOLVED)\b")

A_START = "- [x] **CLOSED c3852 -- QUALITY slot (3852 % 3 == 0). Spent it on the two DUE doc-size trims"
A_NEXT = "- [x] **CLOSED c3848a by c3854 -- `bin/enum-screen` now validates its audit-type argument"
B_START = "- [x] **CLOSED c3847 -- BUILD slot (3847 % 3 == 1). Closed the oldest DUE `enum_audit` rotation: lap on `trademark-search-scraper`"
B_NEXT = "- [ ] **NEW c3847a (MEDIUM) -- wire `bin/vocab-screen`'s trademark-search-scraper probe"

ANCHORS = (("A", A_START, A_NEXT), ("B", B_START, B_NEXT))
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
a, b = bounds["A"], bounds["B"]
assert a[1] <= b[0] < b[1], "spans out of order or overlapping"
EXPECTED_A_IDS = ["3852", "3851", "3850", "3848"]
EXPECTED_B_IDS = ["3847"]
assert span["A"].count("\n- [x] **CLOSED c") + 1 == len(EXPECTED_A_IDS), \
    f"span A block count unexpected: {span['A'].count(chr(10)+'- [x] **CLOSED c') + 1}"
assert span["B"].count("- [x] **CLOSED c") == len(EXPECTED_B_IDS), \
    f"span B block count unexpected: {span['B'].count('- [x] **CLOSED c')}"
all_ids = EXPECTED_A_IDS + EXPECTED_B_IDS
whole = span["A"] + span["B"]
for cyc in all_ids:
    found = re.search(rf"^- \[[ x]\] \*\*CLOSED c{cyc}\b", whole, re.M)
    assert found, f"c{cyc} head not found in spans"
# the one-off closure and open item between A and B must stay live
assert not any(re.search(r"CLOSED c3848a by c3854", span[n]) for n in span), \
    "CLOSED c3848a one-off closure must stay OUTSIDE the cut spans"
assert not any(re.search(r"^- \[ \] \*\*NEW c3848b\b", span[n], re.M) for n in span), \
    "NEW c3848b open item must stay OUTSIDE the cut spans"
for keep in ("3854", "3853"):
    for name in span:
        assert not re.search(rf"^- \[[ x]\] \*\*CLOSED c{keep}\b", span[name], re.M), \
            f"c{keep} head is inside span {name} -- must be KEPT"

# --- GUARD 1: no span may hold an open item -----------------------------
for name in span:
    assert not re.search(r"^- \[ \] \*\*", span[name], re.M), \
        f"SPAN {name} CONTAINS AN OPEN ITEM -- refusing"

# --- GUARD 2 (c3724/c3748): promote nested actionables, never strand ----
EXPECTED_NESTED = {"A": [], "B": []}
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
outside = orig[:a[0]] + orig[a[1]:b[0]] + orig[b[1]:]
# Manually verified by direct grep before writing this script:
#   3536 -- pure precedent naming ("the c3536 rule"/"the standing c3669/NEW
#           c3536 rule"); no live top-level NEW c3536 item exists anywhere
#           in the file, grepped whole-file -- already closed/renamed in an
#           earlier rotation, same shape as c3849's "3458" case.
#   3848a -- IS the one-off closure kept live outside the spans as
#            `CLOSED c3848a by c3854`; the mention inside span A is a
#            forward pointer to that still-live closure, not a dangling
#            reference.
KNOWN_RESOLVED_WITHIN_ROTATION = {"3536", "3848a"}
for mid in mentioned:
    if re.search(rf"^- \[ \] \*\*`?NEW c{mid}\b", outside, re.M):
        continue
    assert mid in KNOWN_RESOLVED_WITHIN_ROTATION, \
        f"NEW c{mid} mentioned in a cut span has no live top-level copy outside it, " \
        f"and is not in the manually-verified resolved set -- investigate before cutting"

# --- build the new live file in MEMORY (verify, THEN write) -------------
new_text = orig
for name in ("B", "A"):
    s, e = bounds[name]
    new_text = new_text[:s] + new_text[e:]

archive_text = (
    "\n## Archived by cycle 3855 (floor-3 report-block rotation -- the one\n"
    "## DUE fleet check, `bin/check-doc-size`, flagged `tasks/queue.md` TRIM\n"
    "## DUE at 224.3KB/1004 lines). Census RE-DERIVED: 7 report blocks were\n"
    "## live, so 5 rotate (c3854/c3853 are the newest 2 by cycle id and stay\n"
    "## KEPT, plus this cycle's own new block). TWO spans, because the live\n"
    "## one-off closure `CLOSED c3848a by c3854` and the live open item\n"
    "## `NEW c3848b` sit between them and are kept live, untouched: span A =\n"
    "## c3852/c3851/c3850/c3848 (ends at the live CLOSED c3848a closure),\n"
    "## span B = c3847 alone (ends at the live NEW c3847a open item). 0 live\n"
    "## nested actionables stranded -- every narrative NEW-c mention inside\n"
    "## either span was confirmed to have a live top-level copy outside the\n"
    "## cut, or (NEW c3536, NEW c3848a) independently verified historical/\n"
    "## already-live-elsewhere, before this script ran.)\n\n"
    + "\n\n".join(span[n].rstrip("\n") for n in ("A", "B")) + "\n"
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
# the one-off closure and open item must survive, still live, between the
# two surviving spans
assert re.search(r"^- \[x\] \*\*CLOSED c3848a by c3854", new_text, re.M), \
    "CLOSED c3848a one-off closure lost -- refusing"
assert re.search(r"^- \[ \] \*\*NEW c3848b\b", new_text, re.M), \
    "NEW c3848b open item lost -- refusing"

def head_idx(cyc, text):
    m = re.search(rf"^- \[[ x]\] \*\*CLOSED c{cyc}\b", text, re.M)
    assert m, f"no top-level head found for c{cyc}"
    return m.start()
assert head_idx("3854", new_text) < head_idx("3853", new_text)

for s in ("- [ ] **NEW c3848b", "- [ ] **NEW c3847a", "- [ ] **NEW c3844a", "- [x] **CLOSED c3848a by c3854"):
    assert s in new_text, f"open item/closure lost -- refusing: {s[:50]}"

with open(ARCHIVE, "a") as fh:
    fh.write(archive_text)
with open(QUEUE, "w") as fh:
    fh.write(new_text)

print(f"queue.md {len(orig):,}B -> {len(new_text):,}B  ({len(new_text) - len(orig):+,}B)")
print(f"lines {orig.count(chr(10)):,} -> {new_text.count(chr(10)):,}")
for n in ("A", "B"):
    print(f"span {n}: {len(span[n]):,}B")
print(f"archived {len(archive_text):,}B under '## Archived by cycle 3855'")
print(f"Read-cap headroom now {262144 - len(new_text):,}B (~{(262144 - len(new_text)) // 5440} cycles at +5440 B/cycle)")
