#!/usr/bin/env python3
"""c2931 QUALITY-slot trim of tasks/queue.md (flagged TRIM SOON by check-doc-size at
c2930: 114.6KB/1384 lines, projected to read TRIM DUE at next look). DONE-block floor
lever, same pattern as _trim2922q.py/_trim2925q.py: restore the newest-5-live
convention.

Ranges re-derived fresh this cycle (doc-trim rule 3, never paste forward): 10
cycle-level DONE blocks live (c2930, c2928, c2929, c2925, c2922, c2920, c2923, c2924,
c2921, c2926). Sorted by cycle number descending: 2930, 2929, 2928, 2926, 2925, 2924,
2923, 2922, 2921, 2920. Newest-5 floor -> keep 2930/2929/2928/2926/2925 live, archive
the 5 oldest: c2922 (61-74), c2920 (75-95), c2923 (96-116+blank117), c2924 (118-135),
c2921 (437-455). The first four are contiguous (immediately follow c2925's block,
which ends at line 60) so they are cut as one range (61-135); c2921 sits far away
(after the c2836/c2816/c2815 items) and is cut separately.

Rule-1 hazard grep run FIRST over both ranges, pattern
`standing|cadence|always |never |do not |must |\\brule\\b` (case-insensitive) --
read every hit before cutting.

Partition asserted total, non-overlapping, multiset-identical (pure cut, no
rewrites).
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c2931_queue.bak"
HEADER = "## Archived by cycle 2931 (2026-11-09)"

CUT = [
    (61, 135, "DONE c2922+c2920+c2923+c2924"),
    (437, 455, "DONE c2921"),
]


def main():
    orig = open(QUEUE).read()
    lines = orig.split("\n")
    n = len(lines)
    open(BACKUP, "w").write(orig)

    taken = {}
    for a, b, label in CUT:
        for i in range(a, b + 1):
            assert i not in taken, f"overlap at line {i}: {label} vs {taken[i]}"
            assert 1 <= i <= n, f"line {i} out of range (file has {n})"
            taken[i] = label
    kept_idx = [i for i in range(1, n + 1) if i not in taken]
    assert len(kept_idx) + len(taken) == n, "partition not total"

    # header sanity: each range's first line is a DONE head naming the right cycle
    expect_head = {
        61: "c2922",
        437: "c2921",
    }
    for start, frag in expect_head.items():
        head = lines[start - 1]
        assert head.startswith("- [x] **DONE"), f"L{start} is not a DONE head: {head[:60]!r}"
        assert frag in head, f"L{start} does not mention {frag}: {head[:80]!r}"
    # the three DONE heads folded inside the big range
    for start, frag in [(75, "c2920"), (96, "c2923"), (118, "c2924")]:
        head = lines[start - 1]
        assert head.startswith("- [x] **DONE"), f"L{start} is not a DONE head: {head[:60]!r}"
        assert frag in head, f"L{start} does not mention {frag}: {head[:80]!r}"

    # boundary sanity: the line right after each cut range starts a new bullet
    for a, b, label in CUT:
        nxt = lines[b] if b < n else ""
        assert nxt.strip() == "" or nxt.startswith("- ["), (
            f"line after {label} ({b+1}) is neither blank nor a new bullet: {nxt[:60]!r}"
        )

    hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
    for a, b, label in CUT:
        hits = [(i, lines[i - 1]) for i in range(a, b + 1) if hazard.search(lines[i - 1])]
        print(f"hazard grep {label} ({a}-{b}): {len(hits)} hit(s)")
        for i, l in hits:
            print(f"  L{i}: {l[:100]}")

    chunks = []
    for a, b, label in sorted(CUT):
        chunks.append(f"<!-- c2931: {label}, queue.md lines {a}-{b} -->")
        chunks.extend(lines[a - 1:b])
        chunks.append("")
    archive_text = "\n".join([HEADER, ""] + chunks)

    out = [lines[i - 1] for i in range(1, n + 1) if i not in taken]
    new_live = "\n".join(out)

    def nb(text):
        return Counter(l for l in text.split("\n") if l.strip())

    got = nb(new_live) + nb(archive_text)
    got -= nb("\n".join(c for c in chunks if c.startswith("<!-- c2931:")))
    got -= nb(HEADER)
    want = nb(orig)
    missing = want - got
    extra = got - want
    assert not missing, f"LINES LOST: {list(missing)[:5]}"
    assert not extra, f"UNEXPLAINED LINES: {list(extra)[:5]}"
    print("lossless check: OK (every non-blank original line is in live+archive)")

    if "--dry-run" in sys.argv:
        print(f"DRY RUN: {len(orig)}B/{n}ln -> {len(new_live)}B/{len(out)}ln "
              f"({len(orig)-len(new_live)}B saved); archive +{len(archive_text)}B")
        return

    with open(ARCHIVE, "a") as f:
        f.write("\n" + archive_text + "\n")
    open(QUEUE, "w").write(new_live)
    print(f"queue.md: {len(orig)}B/{n}ln -> {len(new_live)}B/{len(out)}ln "
          f"({len(orig)-len(new_live)}B saved). Backup {BACKUP}")


if __name__ == "__main__":
    main()
