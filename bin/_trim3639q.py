#!/usr/bin/env python3
"""_trim3639q.py -- cycle 3639 QUALITY-slot floor-5 rotation of tasks/queue.md.

Clone of bin/_trim3633q.py's rotation-only shape (no structural cut this time --
STANDING c3280 records none remains measured). Fresh census: 8 contiguous
`CLOSED cNNNN` blocks, file order IS chronological (c3638, c3637, c3636, c3635,
c3634, c3633, c3632, c3631). Archive the oldest 3 BY POSITION (c3633, c3632,
c3631) and keep the newest 5 (c3638..c3634) so this cycle's own CLOSED c3639
block makes 6.

WRINKLE vs every prior rotation: the archive range is NOT one contiguous span.
A still-OPEN item, `- [ ] **NEW c3632 (LOW ...)**` (0-indexed line 44), sits
physically between the CLOSED c3632 and CLOSED c3631 blocks. It is an active,
unchecked task (fold the google-news-scraper README drift into the next push)
and must NOT be archived with its CLOSED neighbours. So this script cuts two
sub-ranges (idx 39-43 and idx 46-48) and splices the kept NEW c3632 line back
into the live file in between.
"""
import os
import shutil
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3639

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")
pre_bytes = len(raw)

# ---------------------------------------------------------------- boundaries
assert pre_lines[37].startswith(b"- [x] **CLOSED c3634 -- BUILD slot (3634 % 3 == 1)."), pre_lines[37][:80]
assert pre_lines[38] == b"", repr(pre_lines[38])
assert pre_lines[39].startswith(b"- [x] **CLOSED c3633 -- QUALITY slot (3633 % 3 == 0)."), pre_lines[39][:80]
assert pre_lines[40].startswith(b"  - **Next (QUALITY slot, c3636):"), pre_lines[40][:80]
assert pre_lines[41] == b"", repr(pre_lines[41])
assert pre_lines[42].startswith(b"- [x] **CLOSED c3632 -- BUILD slot (3632 % 3 == 2)."), pre_lines[42][:80]
assert pre_lines[43] == b"", repr(pre_lines[43])
assert pre_lines[44].startswith(b"- [ ] **NEW c3632 (LOW, bias is SAFE"), pre_lines[44][:80]
assert pre_lines[45] == b"", repr(pre_lines[45])
assert pre_lines[46].startswith(b"- [x] **CLOSED c3631 -- BUILD slot (3631 % 3 == 1)."), pre_lines[46][:80]
assert pre_lines[47].startswith(b"  - **Next (BUILD slot, c3632"), pre_lines[47][:80]
assert pre_lines[48].startswith(b"  - **Next (QUALITY slot, c3633):"), pre_lines[48][:80]
assert pre_lines[49] == b"", repr(pre_lines[49])
assert pre_lines[50] == b"---", repr(pre_lines[50])
assert pre_lines[51] == b"", repr(pre_lines[51])
assert pre_lines[52].startswith(b"- [ ] **NEW c3620 (LOW"), pre_lines[52][:60]
# the 5 blocks we KEEP must all be CLOSED blocks, newest-5 by position
for idx, tag in ((0, b"c3638"), (5, b"c3637"), (17, b"c3636"), (31, b"c3635"), (37, b"c3634")):
    assert pre_lines[idx].startswith(b"- [x] **CLOSED " + tag), pre_lines[idx][:60]

archived_a = pre_lines[39:44]   # CLOSED c3633, Next, blank, CLOSED c3632, blank
kept_new_c3632 = pre_lines[44]  # the open item, stays live
archived_b = pre_lines[46:49]   # CLOSED c3631, Next, Next

post_lines = (
    pre_lines[0:39]
    + [kept_new_c3632, b""]
    + pre_lines[50:]
)

# --------------------------------------------------- losslessness, by VALUE
pre_nb = Counter(l for l in pre_lines if l.strip())
post_nb = Counter(l for l in post_lines if l.strip())
arch_nb = Counter(l for l in (archived_a + archived_b) if l.strip())
missing = pre_nb - (post_nb + arch_nb)
assert not missing, "WOULD LOSE LINES: %r" % [l[:90] for l in missing]
added = (post_nb + arch_nb) - pre_nb
assert not added, "unexpected new content: %r" % [l[:90] for l in added]

if "--dry-run" in sys.argv:
    post = b"\n".join(post_lines)
    print("DRY RUN ok: %d -> %d bytes (%+.1f KB), %d -> %d lines"
          % (pre_bytes, len(post), (len(post) - pre_bytes) / 1024.0,
             len(pre_lines), len(post_lines)))
    print("  archives %d lines (c3633, c3632, c3631), keeps NEW c3632 live"
          % (len(archived_a) + len(archived_b)))
    sys.exit(0)

shutil.copy2(QUEUE, QUEUE + ".c3639.pre")
header = "\n\n## Archived by cycle %d\n\n" % CYCLE
body = (
    "### RULE 6b floor-5 rotation: the 3 oldest-by-position `CLOSED` blocks "
    "(c3633, c3632, c3631), verbatim. (The still-open `NEW c3632` item that "
    "sat between the CLOSED c3632 and CLOSED c3631 blocks was NOT archived -- "
    "it stayed live in `tasks/queue.md`.)\n\n"
    + "\n".join(l.decode("utf-8") for l in archived_a)
    + "\n\n"
    + "\n".join(l.decode("utf-8") for l in archived_b)
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
