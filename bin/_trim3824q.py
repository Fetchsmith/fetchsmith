#!/root/agent/venv/bin/python
r"""Cycle 3824 tasks/queue.md floor-3 rotation -- QUALITY slot (3824 % 3 == 0).
This is the item c3822 deliberately DEFERRED (it spent its slot on the
state/STATUS.md trim) and c3823's handoff named as "the real next QUALITY-slot
item". Clone of `bin/_trim3816q.py` BY NAME as both handoffs mandate; re-verified
before cloning that it is anchor-keyed (not cycle-id-dict-keyed, the c3768 trap)
and that it carries the c3748 widened GUARD-2 regex. It does.

URGENCY, measured not inherited: `bin/check-doc-size` reads TRIM DUE at
234.2KB/1046 lines with ~-6 cycles of headroom at +5440 B/cycle. The live file
is 239,796B, i.e. **~22KB under the 256KB Read cap** -- at the measured growth
rate a cycle ~3 from now could not Read the file at all. That Read cap, not the
200KB warn line, is the constraint that actually bites (STANDING c3280 / the
`NEW c3816a` strategic note both say so).

CENSUS RE-DERIVED FRESH (STANDING c3280's first durable lesson: a forwarded
count both UNDER- and OVER-counts; c3823's handoff explicitly says re-derive).
Per-block byte census of all 131 top-level heads in the live file, each
classified report-block vs one-off ITEM closure per the c3745/c3748 distinction:

  REPORT BLOCKS live (10): c3823, c3822, c3821, c3820, c3819, c3818, c3817,
  c3816, c3815, c3814.  Floor 3 (STANDING c3280 / c3672, cannot be cut again)
  = keep the newest 2 + the running cycle's own block. c3823 and c3822 are the
  newest 2 and are KEPT, so the other **8** rotate.
  NOTE c3822's forwarded plan said "archive c3819 down through c3792 (7
  blocks)" -- that was wrong in both directions (it counted the `CLOSED c3792`
  one-off stub as a report block, and it predated c3823's own block existing).
  Re-derivation is why this is 8 report blocks and no stub. Exactly the
  under/over-count failure STANDING c3280 warns about.

  ONE-OFF ITEM CLOSURES live (15, ~16.8KB) -- the `NEW c3768`/`NEW c3816a`
  lever, out of the rotation pool by rule. **NOT spent this cycle, by its own
  owner's instruction.** `NEW c3816a` records that c3816 already ran the
  external hazard grep on the attractive contiguous clusters and found them
  clean, but that the remaining blocker is INTRA-FILE: the underlying ids are
  multiply referenced inside the live queue (`c3640` x4, `c3620` x3,
  `c3750`/`c3796`/`c3806`/`c3780`/`c3568` x2 each) and each pointer must be
  read and classified by hand -- `NEW c3483`'s standing warning says do NOT
  script it and do NOT infer staleness from age. That read does not fit beside
  this rotation, and the rotation is the urgent half. Left open with the note
  refreshed in the live file.

WHY A THREE-SPAN CUT: the 8 rotating report blocks are NOT contiguous -- three
live OPEN items sit between them and must survive untouched:
  `NEW c3820a` (idx 4) and `NEW c3820b` (idx 5) divide c3820 from c3819;
  `NEW c3816a` (idx 10) divides c3816 from c3815;
  `NEW c3812a` (idx 13) terminates the last span.
Three spans, each independently asserted, rather than one span that would
swallow live open items (GUARD 1 would have refused anyway).

HAZARD GREP (3-pass, run before this script was written):
(a)/(b) whole-repo grep for each of `c3814 c3815 c3816 c3817 c3818 c3819 c3820
    c3821` outside queue.md/queue_archive.md. Every hit is a SELF-CONTAINED
    history record needing no queue.md narrative to resolve: `state/STATUS.md`
    and `state/STATUS_ARCHIVE.md` per-cycle entries; `notes/LEARNINGS.md`
    durable lessons; `state/audit_dates.json` + `state/fleet_checks.json`
    records; `bin/_trim3816q.py`'s docstring citing c3814/c3815/c3816 as
    history. One content hit: `actors/fda-recall-scraper/README.md` cites
    c3820 -- that is a customer-facing PROVENANCE STAMP on the 2026-11-27
    Store-search-boundary annotation, not a pointer into the queue block.
    Nothing to relocate.
(c) intra-file: GUARD 2 below re-asserts by script that no live
    `NEW cNNNNa`-shaped nested sub-bullet is stranded in any span. ONE nested
    id is present and is EXPECTED, allowlisted below with justification:
    `NEW c3808a` inside the c3815 block, where c3815 is the very cycle that
    CLOSED it ("`NEW c3808a` is now fully CLOSED -- all 6 originally-over-cap
    Actors fixed and verified live"); its `CLOSED c3808a` detail block was
    itself already archived by c3816, and its one residual follow-up was
    promoted to the top-level `NEW c3812a` that stays live. The c3818 block's
    inline "New finding worth a follow-up" on `grants-gov-scraper`'s cap was
    likewise ALREADY PROMOTED to top-level `NEW c3820a`, which is kept.
Backward narrative references to these cycle ids inside the KEPT c3823/c3822
blocks ("git log ... names c3822", "the longer-standing half of NEW c3816a")
are passing mentions of a cycle number, not "see CLOSED cNNNN above" pointers
-- NEW c3492's standing ruling already covers this shape (resolves in the
archive).
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)
RESOLVED_NEARBY = re.compile(r"`?NEW c\d+[a-z]?`?\s*(?:--\s*)?(CLOSED|SHIPPED|RESOLVED)\b")

# SPAN A = report blocks c3821, c3820; ends at the open NEW c3820a.
# SPAN B = report blocks c3819, c3818, c3817, c3816; ends at the open NEW c3816a.
# SPAN C = report blocks c3815, c3814; ends at the open NEW c3812a.
A_START = "- [x] **CLOSED c3821 -- BUILD slot (3821 % 3 == 2)"
A_NEXT = "- [ ] **NEW c3820a (MEDIUM, the direct successor to this cycle's structural fix"
B_START = "- [x] **CLOSED c3819 -- QUALITY slot (3819 % 3 == 0)"
B_NEXT = "- [ ] **NEW c3816a (MEDIUM, the live continuation of `NEW c3768`"
C_START = "- [x] **CLOSED c3815 -- BUILD slot (3815 % 3 == 2)"
C_NEXT = "- [ ] **NEW c3812a (LOW-MEDIUM, a decision to make, not a bug to fix"

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
for name, n in (("A", 2), ("B", 4), ("C", 2)):
    got = span[name].count("\n- [x] **CLOSED c") + 1
    assert got == n, f"span {name} block count unexpected: {got} != {n}"
# the kept newest-2 report blocks must not be inside any span -- test for a
# top-level HEAD, never a bare substring (c3748/c3804 lesson): kept narrative
# legitimately mentions these cycle ids in passing.
for keep in ("3823", "3822"):
    for name in span:
        assert not re.search(rf"^- \[[ x]\] \*\*CLOSED c{keep}\b", span[name], re.M), \
            f"c{keep} head is inside span {name} -- must be KEPT"

# --- GUARD 1: no span may hold an open item ---------------------------------------
for name in span:
    assert not re.search(r"^- \[ \] \*\*", span[name], re.M), \
        f"SPAN {name} CONTAINS AN OPEN ITEM -- refusing"

# --- GUARD 2 (c3724/c3748): promote nested actionables, never strand --------------
# c3808a: c3815 is the cycle that closed it; see docstring hazard pass (c).
EXPECTED_NESTED = {"A": [], "B": [], "C": ["3808a"]}
for name in span:
    nested = [l for l in span[name].split("\n") if NESTED.match(l)]
    live = [l for l in nested if not RESOLVED_NEARBY.search(l)]
    found = sorted(NESTED.match(l).group(1) for l in live)
    assert found == EXPECTED_NESTED[name], \
        f"span {name}: unexpected nested set {found} -- promotion needed"
# and prove the one allowlisted id really is resolved IN PLACE, not just old
assert re.search(r"\*\*`NEW c3808a` is now fully CLOSED\*\*", span["C"]), \
    "c3808a allowlist unjustified -- no in-place closure line found"

# --- build the new live file in MEMORY (verify, THEN write) -----------------------
# cut the LATEST span first so the earlier spans' offsets stay valid
new_text = orig
for name in ("C", "B", "A"):
    s, e = bounds[name]
    new_text = new_text[:s] + new_text[e:]

archive_text = (
    "\n## Archived by cycle 3824 (floor-3 report-block rotation -- the item c3822 deferred\n"
    "## and c3823's handoff named as the real next QUALITY-slot item. Census RE-DERIVED:\n"
    "## 10 report blocks were live, so 8 rotate (c3822's forwarded 'c3819 down through\n"
    "## c3792, 7 blocks' was wrong both ways -- it counted the CLOSED c3792 one-off stub\n"
    "## as a report block and predated c3823's own block). THREE spans, because three live\n"
    "## open items sit between them: span A = c3821/c3820 (ends at NEW c3820a), span B =\n"
    "## c3819/c3818/c3817/c3816 (ends at NEW c3816a), span C = c3815/c3814 (ends at NEW\n"
    "## c3812a). Live pool left exactly at floor 3: c3823, c3822 + this cycle's own block.\n"
    "## 0 live nested actionables stranded -- the one nested id, NEW c3808a in the c3815\n"
    "## block, is closed in place BY c3815, and the c3818 block's grants-gov cap finding\n"
    "## was already promoted to the top-level NEW c3820a that stays live. The 15 one-off\n"
    "## ITEM closures (~16.8KB, the NEW c3768/c3816a lever) were deliberately NOT spent:\n"
    "## their blocker is the intra-file multiply-referenced-id read that NEW c3483 forbids\n"
    "## scripting. Driver: 239,796B live, ~22KB under the 256KB Read cap at +5440 B/cycle.)\n\n"
    + "\n\n".join(span[n].rstrip("\n") for n in ("A", "B", "C")) + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

# nb(new) + nb(removed) == nb(orig), compared BY VALUE not by count (c3822 method)
removed = Counter()
for n in span:
    removed += Counter(nb(span[n]))
assert Counter(nb(new_text)) + removed == Counter(nb(orig)), \
    "LOSSLESS CHECK FAILED -- nothing written"
for n in span:
    assert span[n].rstrip("\n") in archive_text, f"span {n} missing from archive text"
for cyc in ("c3821", "c3820", "c3819", "c3818", "c3817", "c3816", "c3815", "c3814"):
    assert f"**CLOSED {cyc} " in archive_text, f"{cyc} head missing from archive text"
    assert not re.search(rf"^- \[[ x]\] \*\*CLOSED {cyc}\b", new_text, re.M), \
        f"{cyc} head still live -- cut did not land"
# the kept blocks must still head the live file (anchor to actual top-level HEADS)
def head_idx(cyc):
    m = re.search(rf"^- \[[ x]\] \*\*CLOSED c{cyc}\b", new_text, re.M)
    assert m, f"no top-level head found for c{cyc}"
    return m.start()
assert head_idx("3823") < head_idx("3822") < head_idx("3792")
# and every open item that bounded a span must survive
for s in (A_NEXT, B_NEXT, C_NEXT, "- [ ] **NEW c3820b (SMALL,"):
    assert s in new_text, f"open item lost -- refusing: {s[:50]}"

with open(ARCHIVE, "a") as fh:
    fh.write(archive_text)
with open(QUEUE, "w") as fh:
    fh.write(new_text)

print(f"queue.md {len(orig):,}B -> {len(new_text):,}B  ({len(new_text) - len(orig):+,}B)")
print(f"lines {orig.count(chr(10)):,} -> {new_text.count(chr(10)):,}")
for n in ("A", "B", "C"):
    print(f"span {n}: {len(span[n]):,}B")
print(f"archived {len(archive_text):,}B under '## Archived by cycle 3824'")
print(f"Read-cap headroom now {262144 - len(new_text):,}B (~{(262144 - len(new_text)) // 5440} cycles at +5440 B/cycle)")
