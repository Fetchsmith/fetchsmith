#!/usr/bin/env python3
"""c2948 trim of tasks/queue.md -- a PURE CUT, no rewrites.

check-doc-size escalated queue.md to TRIM DUE this cycle (130.7KB/1577ln, ~13c headroom,
258KB projected at the checker's own next look). The documented lever that actually works
is the DONE-block-floor rotation (c2940's standing verdict: the c2916 candidate list is a
dead end, do not re-read it). 10 cycle-level DONE blocks were live; this keeps the newest
5 (c2948, c2944, c2942, c2941, c2940) and archives c2939/c2938/c2937/c2936/c2935 verbatim,
matching STATUS.md's convention.

Ranges re-derived fresh from the live file this cycle (doc-trim rule 3, never paste
forward). The archive-bound range is hazard-grepped FIRST (rule 1) with every hit printed.
No rewrites, so multiset identity is asserted over the whole file.
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c2948_queue.bak"
HEADER = "## Archived by cycle 2948 (2026-11-09)"
NLINES = 1577  # 1576 real lines + the empty trailing element from the final newline
# TWO ranges, not one: an OPEN follow-up item (`UPDATED c2937`, the shopify
# negative-control control) is nested at 177-210 BETWEEN the c2936 and c2935 DONE blocks.
# The first draft of this script cut 101-226 in one span and its asserts all PASSED --
# boundary heads matched and the multiset check was satisfied because the open item was
# merely moved to the archive, not lost. Caught only by grepping the range for `- [ ]`
# independently. That grep is now a hard assert below: a DONE-block cut must contain NO
# open item, and "every line is somewhere" is NOT the same property as "nothing live moved".
CUTS = [(101, 176, "CUT DONE c2939+c2938+c2937+c2936"),
        (211, 226, "CUT DONE c2935")]

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)
assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

# boundary sanity
assert lines[99].strip() == "", "L100 should be the blank before the c2939 block"
for ln, frag in [(101, "c2939"), (116, "c2938"), (134, "c2937"), (157, "c2936"), (211, "c2935")]:
    head = lines[ln - 1]
    assert head.startswith("- [x] **DONE"), f"L{ln} is not a DONE head: {head[:60]!r}"
    assert frag in head, f"L{ln} does not mention {frag}: {head[:80]!r}"
taken = {}
for a, b, label in CUTS:
    assert lines[b - 1].strip() == "", f"L{b} should be the blank closing {label}"
    assert lines[b].startswith("- [ ") or lines[b].startswith("- [x"), \
        f"L{b+1} should start a new item: {lines[b][:60]!r}"
    for i in range(a, b + 1):
        assert i not in taken, f"overlap at L{i}: {label} vs {taken[i]}"
        taken[i] = label
        # THE assert the first draft lacked -- no OPEN item may ride along in a DONE cut
        assert not lines[i - 1].startswith("- [ ] "), \
            f"L{i} is an OPEN item inside {label} -- refusing to archive live work: {lines[i-1][:70]!r}"
assert lines[176].startswith("- [ ] **UPDATED c2937"), \
    f"L177 must remain live (the nested open item): {lines[176][:60]!r}"

# rule 1: hazard grep EVERY archive-bound range, print every hit
hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
chunks, total_hits = [], 0
for a, b, label in CUTS:
    hits = [(i, lines[i - 1]) for i in range(a, b + 1) if hazard.search(lines[i - 1])]
    total_hits += len(hits)
    print(f"rule-1 hazard grep -- {label} ({a}-{b}): {len(hits)} hit(s)")
    for i, l in hits:
        print(f"  L{i}: {l.strip()[:150]}")
    chunks.append(f"<!-- c2948: {label}, queue.md lines {a}-{b} -->")
    chunks.extend(lines[a - 1:b])
    chunks.append("")
print(f"total hazard hits: {total_hits}")

markers = [c for c in chunks if c.startswith("<!-- c2948: ")]
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
for frag in ["c2948", "c2944", "c2942", "c2941", "c2940"]:
    assert any(frag in h for h in heads), f"{frag} DONE block went missing"
for probe in ["**STANDING RULES -- these six were rescued",
              "1. **Grep FIRST, then cut.**",
              "6. **DONE blocks are capped in LENGTH, not count",
              "stop re-reading it each QUALITY slot"]:
    assert sum(probe in l for l in new_lines) == 1, f"do-not-archive probe lost/duped: {probe!r}"
print("structural asserts: OK (5 DONE blocks live, do-not-archive section intact)")

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
