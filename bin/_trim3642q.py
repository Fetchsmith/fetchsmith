#!/usr/bin/env python3
"""_trim3642q.py -- cycle 3642 QUALITY-slot floor-5 rotation of tasks/queue.md.

Clone of bin/_trim3639q.py's rotation-only shape (no structural cut -- STANDING
c3280 records none remains measured). Fresh census: 8 contiguous `CLOSED cNNNN`
blocks, file order IS chronological (c3641, c3640, c3639, c3638, c3637, c3636,
c3635, c3634). Archive the oldest 3 BY POSITION (c3636, c3635, c3634) and keep
the newest 5 (c3641..c3637) so this cycle's own CLOSED c3642 block makes 6.

Unlike c3639's wrinkle (no open item spliced out here, and unlike c3639's gap
which had NO `---` dividers between the archived blocks), c3636/c3635/c3634 ARE
each separated by a `---` divider -- those two dividers are archived verbatim
along with the blocks so the non-blank-line multiset stays balanced (a bare
`---` is non-blank and must be accounted for, it just doesn't carry task
content).
"""
import os
import shutil
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3642

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")
pre_bytes = len(raw)

# ---------------------------------------------------------------- boundaries
assert pre_lines[21].startswith(b"  - **Next (BUILD slot, c3640 or sooner"), pre_lines[21][:80]
assert pre_lines[22] == b"", repr(pre_lines[22])
assert pre_lines[23] == b"---", repr(pre_lines[23])
assert pre_lines[24] == b"", repr(pre_lines[24])
assert pre_lines[25].startswith(b"- [x] **CLOSED c3636 -- QUALITY slot (3636 % 3 == 0)."), pre_lines[25][:80]
assert pre_lines[35].startswith(b"  - **Next (QUALITY slot, c3639):"), pre_lines[35][:80]
assert pre_lines[36] == b"", repr(pre_lines[36])
assert pre_lines[37] == b"---", repr(pre_lines[37])
assert pre_lines[38] == b"", repr(pre_lines[38])
assert pre_lines[39].startswith(b"- [x] **CLOSED c3635 -- BUILD slot (3635 % 3 == 2)."), pre_lines[39][:80]
assert pre_lines[40] == b"", repr(pre_lines[40])
assert pre_lines[41].startswith(b"**Next (BUILD slot, c3637"), pre_lines[41][:80]
assert pre_lines[42] == b"", repr(pre_lines[42])
assert pre_lines[43] == b"---", repr(pre_lines[43])
assert pre_lines[44] == b"", repr(pre_lines[44])
assert pre_lines[45].startswith(b"- [x] **CLOSED c3634 -- BUILD slot (3634 % 3 == 1)."), pre_lines[45][:80]
assert pre_lines[46] == b"", repr(pre_lines[46])
assert pre_lines[47].startswith(b"- [ ] **NEW c3632 (LOW, bias is SAFE"), pre_lines[47][:80]
# the 5 blocks we KEEP must all be CLOSED blocks, newest-5 by position
for idx, tag in ((0, b"c3641"), (3, b"c3640"), (5, b"c3639"), (8, b"c3638"), (13, b"c3637")):
    assert pre_lines[idx].startswith(b"- [x] **CLOSED " + tag), pre_lines[idx][:60]

archived = pre_lines[25:47]  # CLOSED c3636 block, ---, CLOSED c3635 block, ---, CLOSED c3634 header, blank

post_lines = pre_lines[0:25] + pre_lines[47:]

# --------------------------------------------------- losslessness, by VALUE
pre_nb = Counter(l for l in pre_lines if l.strip())
post_nb = Counter(l for l in post_lines if l.strip())
arch_nb = Counter(l for l in archived if l.strip())
missing = pre_nb - (post_nb + arch_nb)
assert not missing, "WOULD LOSE LINES: %r" % [l[:90] for l in missing]
added = (post_nb + arch_nb) - pre_nb
assert not added, "unexpected new content: %r" % [l[:90] for l in added]

if "--dry-run" in sys.argv:
    post = b"\n".join(post_lines)
    print("DRY RUN ok: %d -> %d bytes (%+.1f KB), %d -> %d lines"
          % (pre_bytes, len(post), (len(post) - pre_bytes) / 1024.0,
             len(pre_lines), len(post_lines)))
    print("  archives %d lines (c3636, c3635, c3634 + 2 dividers)" % len(archived))
    sys.exit(0)

shutil.copy2(QUEUE, QUEUE + ".c3642.pre")
header = "\n\n## Archived by cycle %d\n\n" % CYCLE
body = (
    "### RULE 6b floor-5 rotation: the 3 oldest-by-position `CLOSED` blocks "
    "(c3636, c3635, c3634), verbatim, including the two `---` dividers that "
    "separated them in the live file.\n\n"
    + "\n".join(l.decode("utf-8") for l in archived)
    + "\n"
)
with open(ARCHIVE, "a", encoding="utf-8") as fh:
    fh.write(header + body)
post = b"\n".join(post_lines)
with open(QUEUE, "wb") as fh:
    fh.write(post)

live_now = open(QUEUE, "rb").read().split(b"\n")
arch_now = open(ARCHIVE, "rb").read().split(b"\n")
have = Counter(l for l in live_now if l.strip()) + Counter(l for l in arch_now if l.strip())
still_missing = [l for l in pre_nb if have[l] < 1]
assert not still_missing, "POST-WRITE LOSS: %r" % [l[:90] for l in still_missing]
print("WROTE. %d -> %d bytes (%+.1f KB), %d -> %d lines. 0 lines lost "
      "(re-verified against the pre-image, %d distinct non-blank lines)."
      % (pre_bytes, len(post), (len(post) - pre_bytes) / 1024.0,
         len(pre_lines), len(post_lines), len(pre_nb)))
print("archive now %.1f MB" % (os.path.getsize(ARCHIVE) / 1048576.0))
