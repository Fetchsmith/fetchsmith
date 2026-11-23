#!/usr/bin/env python3
"""_trim3644q.py -- cycle 3644 floor-5 rotation of tasks/queue.md.

Clone of bin/_trim3642q.py's rotation-only shape (STANDING c3280 records no
structural cut remains measured). Run in a BUILD slot rather than the usual
QUALITY slot deliberately: `check-doc-size` measured 196.3KB / ~1 cycle of
headroom BEFORE this cycle's own CLOSED block, which is below STANDING c3280's
"re-trim when headroom drops below ~3 cycles" rule, and c3643 had already
deferred it once. Deferring a second time would have crossed the 200KB trim
threshold (the file is 207.8KB with c3644's block prepended).

Fresh census (not forwarded): 8 contiguous `CLOSED cNNNN` blocks, file order IS
chronological -- c3644, c3643, c3642, c3641, c3640, c3639, c3638, c3637.
Archive the oldest 3 BY POSITION (c3639, c3638, c3637) and keep the newest 5
(c3644..c3640), so the floor of 5 holds with this cycle's own block inside it.

Like c3642 (and unlike c3639), the archived span contains a `---` divider -- the
one at line 20, between c3638 and c3637. It is archived verbatim along with the
blocks so the non-blank-line multiset stays balanced (a bare `---` is non-blank
and must be accounted for, it just carries no task content). The cut ENDS at
line 30 rather than 31 so the blank line at 31 is retained, which keeps the
`blank / --- / blank` separator before `NEW c3632` structurally intact instead
of leaving c3640's "Next" line butted against a divider.

Follows both _trim3492q.py bug-lessons recorded in PLAYBOOK: the new archive
text is built as a STRING and every assert runs against it BEFORE either file
is opened for writing, and the lossless check compares by VALUE, never `is`.
"""
import os
import shutil
import subprocess
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3644

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")
pre_bytes = len(raw)

# ---------------------------------------------------------------- boundaries
# Boundary asserts on EXACT header text, so a drifted line number fails loudly
# instead of silently cutting the wrong place (the c3408 template's lesson).
assert pre_lines[13].startswith(b"  - **Next (BUILD slot, c3641 or sooner"), pre_lines[13][:80]
assert pre_lines[14].startswith(b"- [x] **CLOSED c3639 -- QUALITY slot (3639 % 3 == 0)."), pre_lines[14][:80]
assert pre_lines[15].startswith(b"  - **Next (BUILD slot, c3640 or sooner"), pre_lines[15][:80]
assert pre_lines[16] == b"", repr(pre_lines[16])
assert pre_lines[17].startswith(b"- [x] **CLOSED c3638 -- BUILD slot (3638 % 3 == 2)."), pre_lines[17][:80]
assert pre_lines[18].startswith(b"  - **Next (BUILD slot, c3641 or sooner"), pre_lines[18][:80]
assert pre_lines[19] == b"", repr(pre_lines[19])
assert pre_lines[20] == b"---", repr(pre_lines[20])
assert pre_lines[21] == b"", repr(pre_lines[21])
assert pre_lines[22].startswith(b"- [x] **CLOSED c3637 -- BUILD slot (3637 % 3 == 1)."), pre_lines[22][:80]
assert pre_lines[30].startswith(b"  - **Next (BUILD slot, c3640 or sooner"), pre_lines[30][:80]
assert pre_lines[31] == b"", repr(pre_lines[31])
assert pre_lines[32] == b"---", repr(pre_lines[32])
assert pre_lines[33] == b"", repr(pre_lines[33])
assert pre_lines[34].startswith(b"- [ ] **NEW c3632 (LOW, bias is SAFE"), pre_lines[34][:80]

# the 5 blocks we KEEP must all be CLOSED blocks, newest-5 by position
for idx, tag in ((0, b"c3644"), (3, b"c3643"), (6, b"c3642"), (9, b"c3641"), (12, b"c3640")):
    assert pre_lines[idx].startswith(b"- [x] **CLOSED " + tag), pre_lines[idx][:60]
# and nothing we archive may be an OPEN item spliced between them (c3639's wrinkle)
for i in range(14, 31):
    assert not pre_lines[i].startswith(b"- [ ] "), ("OPEN ITEM IN CUT SPAN", i, pre_lines[i][:80])

archived = pre_lines[14:31]          # c3639, c3638, the --- divider, c3637
post_lines = pre_lines[0:14] + pre_lines[31:]

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
    for tag in (b"c3639", b"c3638", b"c3637"):
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
    out = subprocess.run(["grep", "-c", "-E", "c3639|c3638|c3637", p],
                         capture_output=True, text=True).stdout.strip()
    print("  %-22s %s match(es)" % (f, out))
print("--- hazard pass (b): archive already has a c%d header? ---" % CYCLE)
print("  %s" % ("YES -- ABORT" if ("## Archived by cycle %d" % CYCLE)
               in open(ARCHIVE, encoding="utf-8").read() else "no"))

if "--dry-run" in sys.argv:
    print("\nDRY RUN ok: %d -> %d bytes (%+.1f KB), %d -> %d lines"
          % (pre_bytes, len(post), (len(post) - pre_bytes) / 1024.0,
             len(pre_lines), len(post_lines)))
    print("  archives %d lines (c3639, c3638, c3637 + 1 divider)" % len(archived))
    sys.exit(0)

shutil.copy2(QUEUE, QUEUE + ".c3644.pre")
header = "\n\n## Archived by cycle %d\n\n" % CYCLE
body = (
    "### RULE 6b floor-5 rotation: the 3 oldest-by-position `CLOSED` blocks "
    "(c3639, c3638, c3637), verbatim, including the `---` divider that "
    "separated c3638 from c3637 in the live file.\n\n"
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
