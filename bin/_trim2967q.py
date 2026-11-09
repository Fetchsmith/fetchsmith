#!/usr/bin/env python3
"""c2967 proactive trim of tasks/queue.md -- a PURE CUT, no rewrites.

check-doc-size read queue.md as TRIM DUE this cycle (128.9KB/1571ln, ~13c
headroom, 256KB projected at the checker's own next look 24c out). 2967 is the
QUALITY slot (2967 = 3*989 exactly), and c2966's handoff flagged this trim as
this slot's job, per the standing precedent that trims are QUALITY-slot work.

8 cycle-level DONE blocks were live, this time in INSERTION order that happens
to match chronological order: c2966(64) c2965(76) c2964(94) c2963(114)
c2962(125) c2961(139) c2960(154) c2959(178). This keeps the newest 5 BY CYCLE
NUMBER (c2966/c2965/c2964/c2963/c2962) and archives the oldest 3
(c2961/c2960/c2959), matching STATUS.md's convention and the doc-trim item's
newest-5 floor for queue.md. The archive-bound set is CONTIGUOUS this time
(c2961 through the blank line ending c2959, lines 139-204) -- no interleaved
open item to dodge, like c2961's own cut.

Ranges re-derived fresh from the live file this cycle (doc-trim rule 3, never
paste forward). The archive-bound range is hazard-grepped FIRST (rule 1) with
every hit printed. No rewrites, so multiset identity is asserted over the
whole file.
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c2967_queue.bak"
HEADER = "## Archived by cycle 2967 (2026-11-09)"
NLINES = 1572  # 1571 real lines + the empty trailing element from the final newline

CUTS = [
    (139, 204, "CUT DONE c2961+c2960+c2959"),
]

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)
assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

for ln, frag in [(64, "c2966"), (76, "c2965"), (94, "c2964"), (114, "c2963"),
                 (125, "c2962"), (139, "c2961"), (154, "c2960"), (178, "c2959"),
                 (205, "NEW STANDING NOTE")]:
    assert frag in lines[ln - 1], f"L{ln} does not mention {frag}: {lines[ln-1][:80]!r}"
for ln in (138, 204):
    assert lines[ln - 1].strip() == "", f"L{ln} should be blank: {lines[ln-1][:80]!r}"

taken = {}
for a, b, label in CUTS:
    assert lines[a - 1].startswith("- [x] **DONE"), \
        f"L{a} is not a DONE head: {lines[a-1][:60]!r}"
    assert lines[b - 1].strip() == "", f"L{b} should be the blank separator ending {label}"
    for i in range(a, b + 1):
        assert i not in taken, f"overlap at L{i}: {label} vs {taken[i]}"
        taken[i] = label
        assert not lines[i - 1].startswith("- [ ] "), \
            f"L{i} is an OPEN item inside {label} -- refusing to archive live work: {lines[i-1][:70]!r}"

hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
chunks, total_hits = [], 0
for a, b, label in CUTS:
    hits = [(i, lines[i - 1]) for i in range(a, b + 1) if hazard.search(lines[i - 1])]
    total_hits += len(hits)
    print(f"rule-1 hazard grep -- {label} ({a}-{b}): {len(hits)} hit(s)")
    for i, l in hits:
        print(f"  L{i}: {l.strip()[:150]}")
    chunks.append(f"<!-- c2967: {label}, queue.md lines {a}-{b} -->")
    chunks.extend(lines[a - 1:b])
    chunks.append("")
print(f"total hazard hits: {total_hits}")

markers = [c for c in chunks if c.startswith("<!-- c2967: ")]
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
for frag in ["c2966", "c2965", "c2964", "c2963", "c2962"]:
    assert any(frag in h for h in heads), f"{frag} DONE block went missing"
for frag in ["c2961", "c2960", "c2959"]:
    assert not any(frag in h for h in heads), f"{frag} DONE block should have been archived"
for probe in ["**NEW STANDING NOTE (c2952, HIGH value",
              "NEW c2953 backlog (REWRITTEN c2958"]:
    assert sum(probe in l for l in new_lines) == 1, f"do-not-archive probe lost/duped: {probe!r}"
print("structural asserts: OK (5 DONE blocks live, backlog header + standing note intact)")

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
