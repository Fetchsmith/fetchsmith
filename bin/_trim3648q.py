#!/usr/bin/env python3
"""_trim3648q.py -- cycle 3648 floor-5 rotation of tasks/queue.md.

Clone of bin/_trim3644q.py's rotation-only shape (STANDING c3280 records that no
structural cut remains measured, so this is rotation, not a failed hunt). Run in
the QUALITY slot it was flagged for: `check-doc-size` read 199.4KB / **0 cycles**
of headroom at preflight, and the file stands at 209.2KB with c3648's own CLOSED
block prepended -- past the 200KB trim threshold either way.

Fresh census (not forwarded, taken AFTER this cycle's block was prepended): 8
contiguous `CLOSED cNNNN` blocks, file order IS chronological -- c3648, c3647,
c3646, c3644, c3643, c3642, c3641, c3640. (c3645 has no CLOSED block in the live
file at all; verified by grep, nothing to rotate for it.) Archive the oldest 3 BY
POSITION (c3642, c3641, c3640) and keep the newest 5, so the floor of 5 holds
with this cycle's own block inside it.

Unlike c3644/c3642, the cut span contains NO `---` divider -- the one at line 22
sits after c3640's block and stays in the live file. The cut ENDS at 22 (so the
blank at line 21 goes with the archived span and the blank at 12 is retained),
which keeps the `blank / --- / blank` separator before `NEW c3632` intact.

Follows both _trim3492q.py bug-lessons recorded in PLAYBOOK: the archive text is
built as a STRING and every assert runs BEFORE either file is opened for writing,
and the lossless check compares by VALUE, never `is`.
"""
import os
import shutil
import subprocess
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3648

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")
pre_bytes = len(raw)

# ---------------------------------------------------------------- boundaries
# Boundary asserts on EXACT header text, so a drifted line number fails loudly
# instead of silently cutting the wrong place (the c3408 template's lesson).
assert pre_lines[12] == b"", repr(pre_lines[12])
assert pre_lines[13].startswith(b"- [x] **CLOSED c3642 -- QUALITY slot (3642 % 3 == 0)."), pre_lines[13][:80]
assert pre_lines[14].startswith(b"  - **Next (BUILD slot, c3643 or sooner"), pre_lines[14][:80]
assert pre_lines[15] == b"", repr(pre_lines[15])
assert pre_lines[16].startswith(b"- [x] **CLOSED c3641 -- BUILD slot (3641 % 3 == 2)."), pre_lines[16][:80]
assert pre_lines[17].startswith(b"  - **Next (BUILD slot, c3644 or sooner"), pre_lines[17][:80]
assert pre_lines[18] == b"", repr(pre_lines[18])
assert pre_lines[19].startswith(b"- [x] **CLOSED c3640 -- BUILD slot (3640 % 3 == 1)."), pre_lines[19][:80]
assert pre_lines[20].startswith(b"  - **Next (BUILD slot, c3641 or sooner"), pre_lines[20][:80]
assert pre_lines[21] == b"", repr(pre_lines[21])
assert pre_lines[22] == b"---", repr(pre_lines[22])
assert pre_lines[23] == b"", repr(pre_lines[23])
assert pre_lines[24].startswith(b"- [ ] **NEW c3632 (LOW, bias is SAFE"), pre_lines[24][:80]

# the 5 blocks we KEEP must all be CLOSED blocks, newest-5 by position
for idx, tag in ((0, b"c3648"), (2, b"c3647"), (4, b"c3646"), (7, b"c3644"), (10, b"c3643")):
    assert pre_lines[idx].startswith(b"- [x] **CLOSED " + tag), pre_lines[idx][:60]
# and nothing we archive may be an OPEN item spliced between them (c3639's wrinkle)
for i in range(13, 22):
    assert not pre_lines[i].startswith(b"- [ ] "), ("OPEN ITEM IN CUT SPAN", i, pre_lines[i][:80])

archived = pre_lines[13:22]          # c3642, c3641, c3640 (+ their trailing blanks)
post_lines = pre_lines[0:13] + pre_lines[22:]

# --------------------------------------------------- losslessness, by VALUE
pre_nb = Counter(l for l in pre_lines if l.strip())
post_nb = Counter(l for l in post_lines if l.strip())
arch_nb = Counter(l for l in archived if l.strip())
missing = pre_nb - (post_nb + arch_nb)
assert not missing, "WOULD LOSE LINES: %r" % [l[:90] for l in missing]
added = (post_nb + arch_nb) - pre_nb
assert not added, "unexpected new content: %r" % [l[:90] for l in added]

post = b"\n".join(post_lines)

# ------------------------------------------------------ 3-pass hazard grep
# (c) the intra-file pass is the one that has ever found anything real
# (c3306/c3309/c3320/c3324/c3348) -- do not skip it.
def hazard():
    hits = []
    for tag in (b"c3642", b"c3641", b"c3640"):
        for i, l in enumerate(post_lines):
            if tag in l:
                hits.append((tag.decode(), i, l[:160].decode("utf-8", "replace")))
    return hits

print("--- hazard pass (c): intra-file references to the archived cycles "
      "surviving in the live file ---")
for tag, i, txt in hazard():
    print("  %s @ live line %d: %s" % (tag, i, txt))
print("--- hazard pass (a): other state files referencing them ---")
for f in ("state/STATUS.md", "notes/PLAYBOOK.md", "notes/STANDING.md"):
    p = os.path.join("/root/agent", f)
    if not os.path.exists(p):
        continue
    out = subprocess.run(["grep", "-c", "-E", "c3642|c3641|c3640", p],
                         capture_output=True, text=True).stdout.strip()
    print("  %-22s %s match(es)" % (f, out))
print("--- hazard pass (b): archive already has a c%d header? ---" % CYCLE)
print("  %s" % ("YES -- ABORT" if ("## Archived by cycle %d" % CYCLE)
               in open(ARCHIVE, encoding="utf-8").read() else "no"))

if "--dry-run" in sys.argv:
    print("\nDRY RUN ok: %d -> %d bytes (%+.1f KB), %d -> %d lines"
          % (pre_bytes, len(post), (len(post) - pre_bytes) / 1024.0,
             len(pre_lines), len(post_lines)))
    print("  archives %d lines (c3642, c3641, c3640; no divider in the span)" % len(archived))
    sys.exit(0)

shutil.copy2(QUEUE, QUEUE + ".c3648.pre")
header = "\n\n## Archived by cycle %d\n\n" % CYCLE
body = (
    "### RULE 6b floor-5 rotation: the 3 oldest-by-position `CLOSED` blocks "
    "(c3642, c3641, c3640), verbatim. No `---` divider fell inside this span "
    "(the one after c3640 stays in the live file).\n\n"
    + "\n".join(l.decode("utf-8") for l in archived)
    + "\n"
)
with open(ARCHIVE, "a", encoding="utf-8") as fh:
    fh.write(header + body)
with open(QUEUE, "wb") as fh:
    fh.write(post)

# ---- independent re-verify against the written files, not the in-memory ones
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
