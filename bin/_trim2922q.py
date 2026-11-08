#!/usr/bin/env python3
"""c2922 QUALITY-slot trim of tasks/queue.md (mandatory per c2920's handoff: "c2922 is
a QUALITY slot and MUST trim both STATUS.md and queue.md"). DONE-block floor lever
only this cycle (STATUS.md already took the bigger cut in the same cycle; one real
compression lever per doc per cycle is plenty for a 25-minute slot).

Ranges re-derived fresh this cycle (doc-trim rule 3, never paste forward): 8
cycle-level DONE blocks live (c2920, c2919, c2918, c2917, c2916, c2914, c2915, and an
out-of-place c2921 inserted mid-file at line 564 by that cycle's own edit). Newest-5
floor (the standing queue.md convention) -> keep c2921, c2920, c2919, c2918, c2917
live, archive the 3 oldest: c2916 (106-128), c2914 (130-174), c2915 (176-206) -- all
contiguous, no open items interleaved.

Rule-1 hazard grep run FIRST over all three ranges, pattern
`standing|cadence|always |never |do not |must |\\brule\\b` (case-insensitive): 9 hits,
all read. All narrative about rules homed elsewhere (c2120 preflight rule, doc-trim
cadence) or about this exact sweep's tally, which the live "CLOSED c2896 sweep --
residue only (COMPRESSED c2916 ...)" item (further down the file) already carries
forward. No rescue needed.

Partition asserted total, non-overlapping, multiset-identical (pure cut, no
rewrites).
"""
import os

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c2922_queue.bak"
HEADER = "## Archived by cycle 2922 (2026-11-08)"

CUT = [
    (106, 128, "DONE c2916"),
    (130, 174, "DONE c2914"),
    (176, 206, "DONE c2915"),
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

    expect = {106: "DONE c2916", 130: "DONE c2914", 176: "DONE c2915"}
    for start, frag in expect.items():
        head = lines[start - 1]
        assert head.startswith("- [x] **DONE"), f"L{start} is not a DONE head: {head[:60]!r}"
        assert frag.split()[-1] in head, f"L{start} does not mention {frag}: {head[:80]!r}"

    for a, b, label in CUT:
        assert lines[a - 2].strip() == "", f"line before {label} ({a}) is not blank"
        assert lines[b].strip() == "", f"line after {label} ({b}) is not blank"

    chunks = []
    for a, b, label in sorted(CUT):
        chunks.append(f"<!-- c2922: {label}, queue.md lines {a}-{b} -->")
        chunks.extend(lines[a - 1:b])
        chunks.append("")
    archive_text = "\n".join([HEADER, ""] + chunks)

    out = [lines[i - 1] for i in range(1, n + 1) if i not in taken]
    new_live = "\n".join(out)

    def nb(text):
        from collections import Counter
        return Counter(l for l in text.split("\n") if l.strip())

    got = nb(new_live) + nb(archive_text)
    got -= nb("\n".join(c for c in chunks if c.startswith("<!-- c2922:")))
    got -= nb(HEADER)
    want = nb(orig)
    missing = want - got
    extra = got - want
    assert not missing, f"LINES LOST: {list(missing)[:5]}"
    assert not extra, f"UNEXPLAINED LINES: {list(extra)[:5]}"
    print("lossless check: OK (every non-blank original line is in live+archive)")

    import sys
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
