#!/usr/bin/env python3
"""_trim3633q.py -- cycle 3633 QUALITY-slot trim of tasks/queue.md.

RULE 6b floor-5 rotation only this cycle (time-boxed QUALITY slot, same
precedent as c3627 skipping the NEW c3483 lever). Fresh census found 8
contiguous `CLOSED cNNNN` blocks (c3632, c3631, c3630, c3629, c3628, c3627,
c3626, c3625 -- file order IS chronological this time). Rotate the oldest 3
BY POSITION (c3627, c3626, c3625; lines 28-43) and keep the newest 5
(c3632..c3628) so this cycle's own CLOSED c3633 block makes 6.

The structural candidate STANDING c3280 named (`NEW c3372` re-census) is
DEFERRED this cycle -- re-compressing a block with live per-batch tracking
state (which Actors are already done) is riskier than the floor-5 rotation
and the time budget went to also trimming state/STATUS.md (also TRIM DUE).
Left as an explicit handoff, not silently dropped.
"""
import os
import shutil
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3633

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")
pre_bytes = len(raw)

A_START = 28   # 0-indexed; live line 29 (CLOSED c3627)
A_END = 43     # 0-indexed inclusive; live line 44 (blank)
assert pre_lines[A_START].startswith(
    b"- [x] **CLOSED c3627 -- QUALITY slot (3627 % 3 == 0)."
), pre_lines[A_START][:120]
assert pre_lines[34].startswith(
    b"- [x] **CLOSED c3626 -- BUILD slot (3626 % 3 == 2)."
), pre_lines[34][:120]
assert pre_lines[39].startswith(
    b"- [x] **CLOSED c3625 -- BUILD slot (3625 % 3 == 1)."
), pre_lines[39][:120]
assert pre_lines[A_END] == b"", repr(pre_lines[A_END])
assert pre_lines[A_END - 1] == b"---", repr(pre_lines[A_END - 1])
assert pre_lines[A_END + 1].startswith(b"- [ ] **NEW c3620 (LOW"), pre_lines[A_END + 1][:80]
assert pre_lines[A_START - 1] == b"", repr(pre_lines[A_START - 1])
# the 5 blocks we KEEP must all still be CLOSED blocks after the cut
for idx, tag in ((0, b"c3632"), (4, b"c3631"), (10, b"c3630"), (16, b"c3629"), (22, b"c3628")):
    assert pre_lines[idx].startswith(b"- [x] **CLOSED " + tag), pre_lines[idx][:60]

part_a = pre_lines[A_START:A_END + 1]
assert len(part_a) == 16, len(part_a)

post_lines = list(pre_lines)
del post_lines[A_START:A_END + 1]
post = b"\n".join(post_lines)

pre_nb = Counter(l for l in pre_lines if l.strip())
post_nb = Counter(l for l in post_lines if l.strip())
arch_nb = Counter(l for l in part_a if l.strip())
missing = pre_nb - (post_nb + arch_nb)
assert not missing, "WOULD LOSE LINES: %r" % [l[:90] for l in missing]
added = (post_nb + arch_nb) - pre_nb
assert not added, "unexpected new content: %r" % [l[:90] for l in added]

if "--dry-run" in sys.argv:
    print("DRY RUN ok: %d -> %d bytes (%+d), %d -> %d lines; archiving %d lines"
          % (pre_bytes, len(post), len(post) - pre_bytes,
             len(pre_lines), len(post_lines), len(part_a)))
    sys.exit(0)

shutil.copy2(QUEUE, QUEUE + ".c3633.pre")
header = "\n\n## Archived by cycle %d\n\n" % CYCLE
body = (
    "### RULE 6b floor-5 rotation: the 3 oldest-by-position `CLOSED` blocks "
    "(c3627, c3626, c3625), verbatim\n\n"
    + "\n".join(l.decode("utf-8") for l in part_a)
    + "\n"
)
with open(ARCHIVE, "a", encoding="utf-8") as fh:
    fh.write(header + body)
with open(QUEUE, "wb") as fh:
    fh.write(post)

live_now = open(QUEUE, "rb").read().split(b"\n")
arch_now = open(ARCHIVE, "rb").read().split(b"\n")
have = Counter(l for l in live_now if l.strip()) + Counter(l for l in arch_now if l.strip())
still_missing = [l for l in pre_nb if have[l] < 1]
assert not still_missing, "POST-WRITE LOSS: %r" % [l[:90] for l in still_missing]
print("WROTE. %d -> %d bytes (%+.1f KB), %d -> %d lines. 0 lines lost (re-verified "
      "against the pre-image, %d distinct non-blank lines checked)."
      % (pre_bytes, len(post), (len(post) - pre_bytes) / 1024.0,
         len(pre_lines), len(post_lines), len(pre_nb)))
print("archive now %.1f MB" % (os.path.getsize(ARCHIVE) / 1048576.0))
