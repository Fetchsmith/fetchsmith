#!/usr/bin/env python3
"""_trim3654q.py -- cycle 3654 floor-5 rotation of tasks/queue.md.

Clone of bin/_trim3648q.py's rotation-only shape (STANDING c3280 / PLAYBOOK's
doc-size-trim-cadence section records no structural cut remains measured, so
this is rotation, not a failed hunt). Run in the QUALITY slot flagged for it
by c3653's handoff: queue.md measured 221.5KB/981ln at c3654 preflight, past
the ~200KB equilibrium threshold either way.

Fresh census (not forwarded, taken BEFORE this cycle's own CLOSED block is
prepended): 10 contiguous `CLOSED cNNNN` blocks at the top of the live file,
file order chronological (newest first) -- c3653, c3652, c3651, c3650, c3649,
c3648, c3647, c3646, c3644, c3643. (c3645 has no CLOSED block in the live file
at all, consistent with c3648's census -- nothing to rotate for it.) Once this
cycle's own c3654 block is prepended that becomes 11 blocks; keep the newest 5
(c3654, c3653, c3652, c3651, c3650) and archive the oldest 6 BY POSITION
(c3649, c3648, c3647, c3646, c3644, c3643) -- a bigger-than-usual rotation
because no trim ran at c3651 (that QUALITY slot spent itself on the
uk-find-a-tender-scraper batch instead), so two cycles' growth stacked up.

The cut span (lines 11-24 of the PRE-PREPEND file) contains no `---` divider
-- the one at (pre-prepend) line 25 sits after c3643's block and stays live,
same shape as c3648's trim.

Follows both _trim3492q.py bug-lessons recorded in PLAYBOOK: the archive text
is built as a STRING and every assert runs BEFORE either file is opened for
writing, and the lossless check compares by VALUE, never `is`.
"""
import os
import shutil
import subprocess
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3654

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")
pre_bytes = len(raw)

# ---------------------------------------------------------------- boundaries
# Boundary asserts on EXACT header text, so a drifted line number fails loudly
# instead of silently cutting the wrong place (the c3408 template's lesson).
assert pre_lines[11].startswith(b"- [x] **CLOSED c3649 -- BUILD slot (3649 % 3 == 1)."), pre_lines[11][:80]
assert pre_lines[12].startswith(b"  - **Next (BUILD slot, c3650 or sooner"), pre_lines[12][:80]
assert pre_lines[13].startswith(b"- [x] **CLOSED c3648 -- QUALITY slot (3648 % 3 == 0)."), pre_lines[13][:80]
assert pre_lines[14].startswith(b"- [x] **CLOSED c3647 -- BUILD slot (3647 % 3 == 2)."), pre_lines[14][:80]
assert pre_lines[15].startswith(b"  - **Next (BUILD slot, c3648 is QUALITY"), pre_lines[15][:80]
assert pre_lines[16].startswith(b"- [x] **CLOSED c3646 -- BUILD slot (3646 % 3 == 1)."), pre_lines[16][:80]
assert pre_lines[17].startswith(b"  - **Next (BUILD slot, c3647 or sooner"), pre_lines[17][:80]
assert pre_lines[18] == b"", repr(pre_lines[18])
assert pre_lines[19].startswith(b"- [x] **CLOSED c3644 -- BUILD slot (3644 % 3 == 2)."), pre_lines[19][:80]
assert pre_lines[20].startswith(b"  - **Next (BUILD slot, c3646 or sooner"), pre_lines[20][:80]
assert pre_lines[21] == b"", repr(pre_lines[21])
assert pre_lines[22].startswith(b"- [x] **CLOSED c3643 -- BUILD slot (3643 % 3 == 1)."), pre_lines[22][:80]
assert pre_lines[23].startswith(b"  - **Next (BUILD slot, c3646 or sooner"), pre_lines[23][:80]
assert pre_lines[24] == b"", repr(pre_lines[24])
assert pre_lines[25] == b"---", repr(pre_lines[25])
assert pre_lines[26] == b"", repr(pre_lines[26])

# the 5 blocks we KEEP (pre-prepend; this cycle's own block makes 6 -> floor 5
# after the next cycle's prepend, consistent with the c3648 precedent where
# the trimming cycle's own block is one of the kept 5)
for idx, tag in ((0, b"c3653"), (3, b"c3652"), (6, b"c3651"), (9, b"c3650")):
    assert pre_lines[idx].startswith(b"- [x] **CLOSED " + tag), pre_lines[idx][:60]
# and nothing we archive may be an OPEN item spliced between them
for i in range(11, 25):
    assert not pre_lines[i].startswith(b"- [ ] "), ("OPEN ITEM IN CUT SPAN", i, pre_lines[i][:80])

archived = pre_lines[11:25]          # c3649, c3648, c3647, c3646, c3644, c3643 (+ their trailing blanks)
post_lines = pre_lines[0:11] + pre_lines[25:]

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
# (c3306/c3309/c3320/c3324/c3348/c3648) -- do not skip it.
TAGS = (b"c3649", b"c3648", b"c3647", b"c3646", b"c3644", b"c3643")

def hazard():
    hits = []
    for tag in TAGS:
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
    out = subprocess.run(["grep", "-c", "-E", "|".join(t.decode() for t in TAGS), p],
                         capture_output=True, text=True).stdout.strip()
    print("  %-22s %s match(es)" % (f, out))
print("--- hazard pass (b): archive already has a c%d header? ---" % CYCLE)
print("  %s" % ("YES -- ABORT" if ("## Archived by cycle %d" % CYCLE)
               in open(ARCHIVE, encoding="utf-8").read() else "no"))

if "--dry-run" in sys.argv:
    print("\nDRY RUN ok: %d -> %d bytes (%+.1f KB), %d -> %d lines"
          % (pre_bytes, len(post), (len(post) - pre_bytes) / 1024.0,
             len(pre_lines), len(post_lines)))
    print("  archives %d lines (c3649, c3648, c3647, c3646, c3644, c3643)" % len(archived))
    sys.exit(0)

shutil.copy2(QUEUE, QUEUE + ".c3654.pre")
header = "\n\n## Archived by cycle %d\n\n" % CYCLE
body = (
    "### RULE 6b floor-5 rotation: the 6 oldest-by-position `CLOSED` blocks "
    "(c3649, c3648, c3647, c3646, c3644, c3643), verbatim -- a larger-than-usual "
    "rotation because no trim ran at c3651. No `---` divider fell inside this "
    "span (the one after c3643 stays in the live file).\n\n"
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
