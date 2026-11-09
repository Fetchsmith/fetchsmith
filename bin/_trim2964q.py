#!/usr/bin/env python3
"""c2964 proactive trim of tasks/queue.md -- a PURE CUT, no rewrites.

check-doc-size read queue.md as TRIM SOON this cycle (127.6KB/1557ln, ~14c
headroom, 255KB projected at the checker's own next look 24c out -- so the next
run reads TRIM DUE no matter what, and the checker's own advice is to trim
proactively in a QUALITY slot rather than wait for the escalation). 2964 is the
QUALITY slot (2964 = 3*988 exactly), and c2963's handoff flagged this trim as
this slot's job.

8 cycle-level DONE blocks were live, in INSERTION order (not chronological --
the same quirk c2961 documented): c2963(51) c2962(62) c2961(76) c2958(91)
c2960(107) c2959(131) c2957(157) c2956(171). This keeps the newest 5 BY CYCLE
NUMBER (c2963/c2962/c2961/c2960/c2959) and archives the oldest 3
(c2958/c2957/c2956) verbatim, matching STATUS.md's convention and the doc-trim
item's newest-5 floor for queue.md. Because the order is insertion-order, the
archive-bound set is NON-CONTIGUOUS: c2958 sits between c2961 and c2960.

Ranges re-derived fresh from the live file this cycle (doc-trim rule 3, never
paste forward). Each archive-bound range is hazard-grepped FIRST (rule 1) with
every hit printed. No rewrites, so multiset identity is asserted over the whole
file.
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c2964_queue.bak"
HEADER = "## Archived by cycle 2964 (2026-11-09)"
NLINES = 1558  # 1557 real lines + the empty trailing element from the final newline

# Each range ends on the blank separator that followed the block, so the cut
# leaves exactly the separator structure that was already there.
CUTS = [
    (91, 106, "CUT DONE c2958"),
    (157, 189, "CUT DONE c2957+c2956"),
]

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)
assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

# boundary sanity -- every DONE head position asserted, kept and archived alike
for ln, frag in [(51, "c2963"), (62, "c2962"), (76, "c2961"), (91, "c2958"),
                 (107, "c2960"), (131, "c2959"), (157, "c2957"), (171, "c2956"),
                 (191, "NEW STANDING NOTE")]:
    assert frag in lines[ln - 1], f"L{ln} does not mention {frag}: {lines[ln-1][:80]!r}"
for ln in (90, 106, 170, 189, 190):
    assert lines[ln - 1].strip() == "", f"L{ln} should be blank: {lines[ln-1][:80]!r}"

taken = {}
for a, b, label in CUTS:
    assert lines[a - 1].startswith("- [x] **DONE"), \
        f"L{a} is not a DONE head: {lines[a-1][:60]!r}"
    assert lines[b - 1].strip() == "", f"L{b} should be the blank separator ending {label}"
    for i in range(a, b + 1):
        assert i not in taken, f"overlap at L{i}: {label} vs {taken[i]}"
        taken[i] = label
        # no OPEN item may ride along in a DONE cut (c2948's near-miss, rule 7)
        assert not lines[i - 1].startswith("- [ ] "), \
            f"L{i} is an OPEN item inside {label} -- refusing to archive live work: {lines[i-1][:70]!r}"

# rule 1: hazard grep EVERY archive-bound range, print every hit
hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
chunks, total_hits = [], 0
for a, b, label in CUTS:
    hits = [(i, lines[i - 1]) for i in range(a, b + 1) if hazard.search(lines[i - 1])]
    total_hits += len(hits)
    print(f"rule-1 hazard grep -- {label} ({a}-{b}): {len(hits)} hit(s)")
    for i, l in hits:
        print(f"  L{i}: {l.strip()[:150]}")
    chunks.append(f"<!-- c2964: {label}, queue.md lines {a}-{b} -->")
    chunks.extend(lines[a - 1:b])
    chunks.append("")
print(f"total hazard hits: {total_hits}")

markers = [c for c in chunks if c.startswith("<!-- c2964: ")]
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
for frag in ["c2963", "c2962", "c2961", "c2960", "c2959"]:
    assert any(frag in h for h in heads), f"{frag} DONE block went missing"
for frag in ["c2958", "c2957", "c2956"]:
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
