#!/usr/bin/env python3
"""c2958 trim of tasks/queue.md -- a PURE CUT, no rewrites.

check-doc-size read queue.md as TRIM DUE this cycle (141.3KB/1716ln, ~11c headroom,
269KB projected at the checker's own next look). 11 cycle-level DONE blocks were live
(c2957 down to c2944, non-contiguous -- an open item, NEW STANDING NOTE c2952, rides
between the c2952 and c2951 blocks). This keeps the newest 5 (c2957/c2956/c2955/c2954/
c2953) and archives the other 6 (c2952/c2951/c2950/c2949/c2948/c2944) verbatim, matching
STATUS.md's convention and rule 6's newest-5 floor.

Ranges re-derived fresh from the live file this cycle (doc-trim rule 3, never paste
forward). Both archive-bound ranges are hazard-grepped FIRST (rule 1) with every hit
printed. No rewrites, so multiset identity is asserted over the whole file.
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c2958_queue.bak"
HEADER = "## Archived by cycle 2958 (2026-11-09)"
NLINES = 1717  # 1716 real lines + the empty trailing element from the final newline

# TWO ranges: the NEW STANDING NOTE (c2952) open item sits at 261-280, between the
# c2952 DONE block and the c2951 DONE block, and must stay live.
CUTS = [(241, 260, "CUT DONE c2952"),
        (281, 369, "CUT DONE c2951+c2950+c2949+c2948+c2944")]

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)
assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

# boundary sanity
assert lines[139].strip() == "" or True  # (no-op placeholder, real checks below)
for ln, frag in [(137, "c2957"), (151, "c2956"), (170, "c2955"), (184, "c2954"),
                  (225, "c2953"), (241, "c2952"), (261, "NEW STANDING NOTE"),
                  (281, "c2951"), (298, "c2950"), (312, "c2949"), (332, "c2948"),
                  (352, "c2944"), (370, "NEW c2948")]:
    head = lines[ln - 1]
    assert frag in head, f"L{ln} does not mention {frag}: {head[:80]!r}"

taken = {}
for a, b, label in CUTS:
    assert lines[a - 1].startswith("- [x] **DONE"), \
        f"L{a} is not a DONE head: {lines[a-1][:60]!r}"
    assert lines[b - 1].strip() == "", f"L{b} should be the blank closing {label}"
    assert lines[b].startswith("- [ ") or lines[b].startswith("- [x"), \
        f"L{b+1} should start a new item: {lines[b][:60]!r}"
    for i in range(a, b + 1):
        assert i not in taken, f"overlap at L{i}: {label} vs {taken[i]}"
        taken[i] = label
        # no OPEN item may ride along in a DONE cut (c2948's near-miss, rule 7)
        assert not lines[i - 1].startswith("- [ ] "), \
            f"L{i} is an OPEN item inside {label} -- refusing to archive live work: {lines[i-1][:70]!r}"
assert lines[260].startswith("- [ ] **NEW STANDING NOTE"), \
    f"L261 must remain live (the nested open item): {lines[260][:60]!r}"

# rule 1: hazard grep EVERY archive-bound range, print every hit
hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
chunks, total_hits = [], 0
for a, b, label in CUTS:
    hits = [(i, lines[i - 1]) for i in range(a, b + 1) if hazard.search(lines[i - 1])]
    total_hits += len(hits)
    print(f"rule-1 hazard grep -- {label} ({a}-{b}): {len(hits)} hit(s)")
    for i, l in hits:
        print(f"  L{i}: {l.strip()[:150]}")
    chunks.append(f"<!-- c2958: {label}, queue.md lines {a}-{b} -->")
    chunks.extend(lines[a - 1:b])
    chunks.append("")
print(f"total hazard hits: {total_hits}")

markers = [c for c in chunks if c.startswith("<!-- c2958: ")]
archive_text = "\n".join([HEADER, ""] + chunks)
new_live = "\n".join([l for i, l in enumerate(lines, 1) if i not in taken])

def nb(text):
    return Counter(l for l in text.split("\n") if l.strip())

got = nb(new_live) + nb(archive_text) - nb(HEADER) - nb("\n".join(markers))
missing, extra = nb(orig) - got, got - nb(orig)
assert not missing, f"LINES LOST: {list(missing)[:5]}"
assert not extra, f"UNEXPLAINED LINES: {list(extra)[:5]}"
print("lossless check: OK (pure cut, multiset identity over live+archive)")

new_lines = new_live.split("\n")
heads = [l for l in new_lines if l.startswith("- [x] **DONE c29")]
assert len(heads) == 5, f"expected 5 cycle-level DONE blocks live, got {len(heads)}"
for frag in ["c2957", "c2956", "c2955", "c2954", "c2953"]:
    assert any(frag in h for h in heads), f"{frag} DONE block went missing"
for probe in ["**STANDING RULES -- the first six were rescued",
              "1. **Grep FIRST, then cut.**",
              "6. **DONE blocks are capped in LENGTH, not count",
              "stop re-reading it each QUALITY slot",
              "**NEW STANDING NOTE (c2952, HIGH value"]:
    assert sum(probe in l for l in new_lines) == 1, f"do-not-archive probe lost/duped: {probe!r}"
print("structural asserts: OK (5 DONE blocks live, do-not-archive section + standing note intact)")

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
