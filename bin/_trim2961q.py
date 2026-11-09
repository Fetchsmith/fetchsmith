#!/usr/bin/env python3
"""c2961 trim of tasks/queue.md -- a PURE CUT, no rewrites.

check-doc-size read queue.md as TRIM DUE this cycle (129.6KB/1579ln, ~13c
headroom, 257KB projected at the checker's own next look). 8 cycle-level DONE
blocks were live (c2958/c2960/c2959/c2957/c2956/c2955/c2954/c2953, in
insertion order, not strictly chronological). This keeps the newest 5 by
cycle number (c2960/c2959/c2958/c2957/c2956) and archives the oldest 3
(c2955/c2954/c2953) verbatim, matching STATUS.md's convention and rule 6's
newest-5 floor for queue.md.

Range re-derived fresh from the live file this cycle (doc-trim rule 3, never
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
BACKUP = "/tmp/c2961_queue.bak"
HEADER = "## Archived by cycle 2961 (2026-11-09)"
NLINES = 1580  # 1579 real lines + the empty trailing element from the final newline

CUTS = [(142, 211, "CUT DONE c2955+c2954+c2953")]

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)
assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

# boundary sanity
for ln, frag in [(43, "c2958"), (59, "c2960"), (83, "c2959"), (109, "c2957"),
                  (123, "c2956"), (142, "c2955"), (156, "c2954"), (197, "c2953"),
                  (212, ""), (213, "NEW STANDING NOTE")]:
    head = lines[ln - 1]
    if frag:
        assert frag in head, f"L{ln} does not mention {frag}: {head[:80]!r}"
    else:
        assert head.strip() == "", f"L{ln} should be blank: {head[:80]!r}"

taken = {}
for a, b, label in CUTS:
    assert lines[a - 1].startswith("- [x] **DONE"), \
        f"L{a} is not a DONE head: {lines[a-1][:60]!r}"
    assert lines[b - 1].strip() != "", f"L{b} should be real content (last line of {label})"
    assert lines[b].strip() == "", f"L{b+1} should be the blank separator after {label}"
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
    chunks.append(f"<!-- c2961: {label}, queue.md lines {a}-{b} -->")
    chunks.extend(lines[a - 1:b])
    chunks.append("")
print(f"total hazard hits: {total_hits}")

markers = [c for c in chunks if c.startswith("<!-- c2961: ")]
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
for frag in ["c2960", "c2959", "c2958", "c2957", "c2956"]:
    assert any(frag in h for h in heads), f"{frag} DONE block went missing"
for frag in ["c2955", "c2954", "c2953"]:
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
