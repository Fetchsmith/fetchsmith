#!/usr/bin/env python3
"""_trim3672s.py -- cycle 3672 QUALITY-slot trim of state/STATUS.md.

Same c1836 process and keep-9 floor as bin/_trim3633s.py (its direct clone).
Counted the live `^Updated: ` blocks fresh: 48 live blocks (c3671 down to the
file's prior tail) against the keep-9 floor, 193.4KB/444ln and TRIM DUE with
~2 cycles of headroom. Keep the newest 9 (c3671 down to c3663) so this
cycle's own prepended `Updated: ... cycle 3672` block lands the file at
exactly 10. Archive the other 39, verbatim, newest-first, to
state/STATUS_ARCHIVE.md.
"""
import os
import shutil
import sys
from collections import Counter

STATUS = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
CYCLE = 3672
N_ARCHIVED = 39

raw = open(STATUS, "rb").read()
pre_lines = raw.split(b"\n")
pre_bytes = len(raw)

idx = [i for i, l in enumerate(pre_lines) if l.startswith(b"Updated: ")]
assert len(idx) == 48, len(idx)
assert len(idx) - 9 == N_ARCHIVED, (len(idx), N_ARCHIVED)
assert idx[8] == 50, idx[8]   # 9th kept block: cycle 3663
assert idx[9] == 60, idx[9]   # 10th block (first archived): cycle 3662
assert pre_lines[idx[8]].startswith(
    b"Updated: 2026-11-24 UTC by cycle 3663 "
), pre_lines[idx[8]][:80]
assert pre_lines[idx[9]].startswith(
    b"Updated: 2026-11-24 UTC by cycle 3662 "
), pre_lines[idx[9]][:80]

A_START = idx[9]              # 60, 0-indexed; first archived block
A_END = len(pre_lines) - 1    # last line of file (trailing blank)
assert pre_lines[A_START - 1] == b"", repr(pre_lines[A_START - 1])
assert pre_lines[A_START - 2] == b"---", repr(pre_lines[A_START - 2])
assert pre_lines[A_END] == b"", repr(pre_lines[A_END])
assert pre_lines[A_END - 1] == b"---", repr(pre_lines[A_END - 1])

part = pre_lines[A_START:A_END + 1]
kept = pre_lines[:A_START]

pre_nb = Counter(l for l in pre_lines if l.strip())
kept_nb = Counter(l for l in kept if l.strip())
part_nb = Counter(l for l in part if l.strip())
missing = pre_nb - (kept_nb + part_nb)
assert not missing, "WOULD LOSE LINES: %r" % [l[:90] for l in missing]
added = (kept_nb + part_nb) - pre_nb
assert not added, "unexpected new content: %r" % [l[:90] for l in added]

post = b"\n".join(kept)

if "--dry-run" in sys.argv:
    print("DRY RUN ok: %d -> %d bytes (%+d), %d -> %d lines; archiving %d lines (%d blocks)"
          % (pre_bytes, len(post), len(post) - pre_bytes,
             len(pre_lines), len(kept), len(part), N_ARCHIVED))
    sys.exit(0)

shutil.copy2(STATUS, STATUS + ".c3672.pre")
header = ("\n## Archived by cycle %d (from state/STATUS.md: the %d oldest cycle "
          "blocks, c3662 down to the file's prior tail, newest-first and verbatim. "
          "RULE 6b counted fresh off the anchored `^Updated: ` header and found 48 "
          "live blocks against the keep-9 floor. Kept the newest 9 (c3671..c3663) "
          "so c3672's own prepended block lands the file at exactly 10.)\n\n"
          % (CYCLE, N_ARCHIVED))
body = "\n".join(l.decode("utf-8") for l in part) + "\n"
with open(ARCHIVE, "a", encoding="utf-8") as fh:
    fh.write(header + body)
with open(STATUS, "wb") as fh:
    fh.write(post)

live_now = open(STATUS, "rb").read().split(b"\n")
arch_now = open(ARCHIVE, "rb").read().split(b"\n")
have = Counter(l for l in live_now if l.strip()) + Counter(l for l in arch_now if l.strip())
still_missing = [l for l in pre_nb if have[l] < 1]
assert not still_missing, "POST-WRITE LOSS: %r" % [l[:90] for l in still_missing]
print("WROTE. %d -> %d bytes (%+.1f KB), %d -> %d lines. 0 lines lost (re-verified "
      "against the pre-image, %d distinct non-blank lines checked)."
      % (pre_bytes, len(post), (len(post) - pre_bytes) / 1024.0,
         len(pre_lines), len(kept), len(pre_nb)))
print("archive now %.1f MB" % (os.path.getsize(ARCHIVE) / 1048576.0))
