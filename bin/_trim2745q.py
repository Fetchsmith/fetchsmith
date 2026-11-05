#!/usr/bin/env python3
"""One-shot: archive the 8 DONE blocks out of tasks/queue.md (lines 1-318 of the
pre-trim file, 1-indexed, inclusive of trailing blank separators), keeping the
two open items interleaved among them (c2744 LOW note, c2744 TRIVIAL note) live.
Mandatory doc-trim per queue.md's own c2742/c2744 notes, executed cycle 2745."""
import datetime

QUEUE = "tasks/queue.md"
ARCHIVE = "tasks/queue_archive.md"

with open(QUEUE) as f:
    orig = f.read()
lines = orig.splitlines(keepends=True)
assert len(lines) == 1004, f"expected 1004 lines, got {len(lines)}"

# 1-indexed inclusive ranges of the 8 DONE blocks (each ending at its trailing blank line)
done_ranges_1idx = [
    (1, 39), (40, 57), (94, 129), (130, 188), (189, 230),
    (231, 264), (265, 289), (290, 318),
]
# 1-indexed inclusive ranges of the two open items interleaved among them (stay live)
kept_open_ranges_1idx = [(58, 80), (81, 93)]

def slice1(a, b):
    return lines[a - 1 : b]

archived_block = []
for a, b in done_ranges_1idx:
    archived_block.extend(slice1(a, b))

kept_open_block = []
for a, b in kept_open_ranges_1idx:
    kept_open_block.extend(slice1(a, b))

rest_block = lines[318:]  # everything from old line 319 onward, unchanged

kept_block = kept_open_block + rest_block

# sanity checks
done_headers = [l for l in archived_block if l.startswith("- [x]")]
assert len(done_headers) == 8, f"expected 8 DONE headers, got {len(done_headers)}"
assert not any(l.startswith("- [x]") for l in kept_block), "a DONE block leaked into kept range"
assert kept_block[0].startswith("- [ ] **NEW note (c2744, LOW"), "kept range does not start where expected"

open_before = sum(1 for l in lines if l.startswith("- [ ]"))
open_after = sum(1 for l in kept_block if l.startswith("- [ ]"))
assert open_before == open_after, f"open item count changed: {open_before} -> {open_after}"

# non-overlapping + total coverage: every original line appears in exactly one of the two outputs
# (archived_block covers the 8 DONE ranges; kept_block covers the 2 open ranges + 319-end;
#  together with the fact done_ranges+kept_open_ranges+[319,1004] partition [1,1004])
all_1idx_ranges = sorted(done_ranges_1idx + kept_open_ranges_1idx + [(319, 1004)])
covered = []
for a, b in all_1idx_ranges:
    covered.extend(range(a, b + 1))
assert covered == list(range(1, 1005)), "ranges do not exactly partition the file"
assert sorted(archived_block + kept_block, key=lambda x: lines.index(x)) or True  # no-op guard

new_queue = "".join(kept_block)
assert len(new_queue.encode()) < len(orig.encode()), "new queue.md is not smaller"

with open(ARCHIVE) as f:
    archive_orig = f.read()

ts = datetime.datetime.utcnow().strftime("%Y-%m-%d")
header = (f"\n\n=== archived cycle 2745 ({ts}) -- 8 DONE blocks (cycles 2734,2735,2736,"
          f"2740,2741,2742,2743,2744) cut from tasks/queue.md, verbatim; the two open "
          f"c2744 notes that were interleaved among them stayed live in queue.md ===\n\n")
new_archive = archive_orig + header + "".join(archived_block)

assert new_archive.startswith(archive_orig), "archive append is not prefix-preserving"

with open(QUEUE, "w") as f:
    f.write(new_queue)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"OK: queue.md {len(orig.encode())} -> {len(new_queue.encode())} bytes, "
      f"{len(lines)} -> {len(kept_block)} lines; open items {open_before} -> {open_after}; "
      f"archive.md {len(archive_orig.encode())} -> {len(new_archive.encode())} bytes")
