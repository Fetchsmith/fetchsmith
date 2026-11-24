#!/usr/bin/env python3
"""_trim3663q.py -- cycle 3663 floor-5 rotation of tasks/queue.md.

OWED THIS QUALITY SLOT per c3661/c3662's flags: check-doc-size read TRIM DUE
at 210.6KB/981ln, ~-2 cycles of headroom (past the 200KB trim line, not
merely projected to cross it). Same rotation-only shape as every prior
floor-5 trim (_trim3657q.py, _trim3660q.py): keep the newest 5 CLOSED
blocks (counting this cycle's own c3663 block once prepended), archive the
rest down to the standing '---' divider.

Fresh census (0-indexed, taken BEFORE this cycle's own block is prepended):
7 contiguous CLOSED blocks at the top -- c3662, c3661, c3660, c3659, c3658,
c3657, c3656 -- then '---' at line 21. Keep c3662/c3661/c3660/c3659 (lines
0-11); once c3663 is prepended that's 5 kept. Archive c3658/c3657/c3656
(lines 12-20).
"""
import subprocess
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3663

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")

assert pre_lines[0].startswith(b"- [x] **CLOSED c3662"), pre_lines[0][:60]
assert pre_lines[2].startswith(b"- [x] **CLOSED c3661"), pre_lines[2][:60]
assert pre_lines[5].startswith(b"- [x] **CLOSED c3660"), pre_lines[5][:60]
assert pre_lines[9].startswith(b"- [x] **CLOSED c3659"), pre_lines[9][:60]
assert pre_lines[11] == b"", repr(pre_lines[11])
assert pre_lines[12].startswith(b"- [x] **CLOSED c3658"), pre_lines[12][:60]
assert pre_lines[15].startswith(b"- [x] **CLOSED c3657"), pre_lines[15][:60]
assert pre_lines[19].startswith(b"- [x] **CLOSED c3656"), pre_lines[19][:60]
assert pre_lines[20] == b"", repr(pre_lines[20])
assert pre_lines[21] == b"---", repr(pre_lines[21])
assert pre_lines[22] == b"", repr(pre_lines[22])

for i in range(12, 21):
    assert not pre_lines[i].startswith(b"- [ ] "), ("OPEN ITEM IN CUT SPAN", i, pre_lines[i][:80])

archived = pre_lines[12:21]          # c3658, c3657, c3656 (+ trailing blanks)
post_lines = pre_lines[0:12] + pre_lines[21:]

pre_nb = Counter(l for l in pre_lines if l.strip())
post_nb = Counter(l for l in post_lines if l.strip())
arch_nb = Counter(l for l in archived if l.strip())
missing = pre_nb - (post_nb + arch_nb)
assert not missing, "WOULD LOSE LINES: %r" % [l[:90] for l in missing]
added = (post_nb + arch_nb) - pre_nb
assert not added, "unexpected new content: %r" % [l[:90] for l in added]

post = b"\n".join(post_lines)

TAGS = (b"c3658", b"c3657", b"c3656")

def hazard():
    hits = []
    for tag in TAGS:
        for i, l in enumerate(post_lines):
            if tag in l:
                hits.append((tag.decode(), i, l[:160].decode("utf-8", "replace")))
    return hits

print("--- hazard pass (c): intra-file references to archived cycles surviving in live file ---")
for tag, i, txt in hazard():
    print("  %s @ live line %d: %s" % (tag, i, txt))

print("--- hazard pass (a): other state files referencing them ---")
import os
for f in ("state/STATUS.md", "notes/PLAYBOOK.md", "notes/LEARNINGS.md"):
    p = os.path.join("/root/agent", f)
    if not os.path.exists(p):
        continue
    out = subprocess.run(["grep", "-c", "-E", "|".join(t.decode() for t in TAGS), p],
                          capture_output=True, text=True)
    print("  %s: %s hits" % (f, out.stdout.strip()))

with open(QUEUE, "wb") as f:
    f.write(post)

arch_block = b"\n".join(archived)
header = ("\n## Archived by cycle %d\n\n" % CYCLE).encode()
with open(ARCHIVE, "ab") as f:
    f.write(header)
    f.write(arch_block)
    f.write(b"\n")

print("--- sizes ---")
print("pre  bytes=%d lines=%d" % (len(raw), len(pre_lines)))
post_raw = open(QUEUE, "rb").read()
print("post bytes=%d lines=%d" % (len(post_raw), len(post_raw.split(b"\n"))))
print("DONE")
