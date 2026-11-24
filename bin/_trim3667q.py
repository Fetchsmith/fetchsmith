#!/usr/bin/env python3
"""_trim3667q.py -- cycle 3667 floor-5 rotation of tasks/queue.md.

OWED THIS CYCLE per c3666's URGENT flag (explicit override: "do this FIRST
regardless of slot type" -- c3667 is a BUILD slot, 3667 % 3 == 1, but the
flag and STANDING rule 2's <2-slot-deferral cap both say not to wait for
the next QUALITY slot). check-doc-size reads TRIM DUE at 212.8KB/986ln,
~-2 cycles of headroom (past the 200KB trim line, not merely projected).
Same rotation-only shape as every prior floor-5 trim (_trim3663q.py,
_trim3660q.py): keep the newest 5 CLOSED blocks (counting this cycle's own
c3667 block once prepended), archive the rest down to the standing '---'
divider.

Fresh census (0-indexed, taken BEFORE this cycle's own block is prepended):
7 contiguous CLOSED blocks at the top -- c3666, c3665, c3663, c3662, c3661,
c3660, c3659 -- then '---' at line 26. Keep c3666/c3665/c3663/c3662/c3661
(lines 0-18); once c3667 is prepended that's 5 kept. Archive c3660/c3659
(lines 19-25). The OPEN item `NEW c3664` at line 8 sits inside the kept
range and is untouched either way.
"""
import subprocess
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3667

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")

assert pre_lines[0].startswith(b"- [x] **CLOSED c3666"), pre_lines[0][:60]
assert pre_lines[5].startswith(b"- [x] **CLOSED c3665"), pre_lines[5][:60]
assert pre_lines[8].startswith(b"- [ ] **NEW c3664"), pre_lines[8][:60]
assert pre_lines[10].startswith(b"- [x] **CLOSED c3663"), pre_lines[10][:60]
assert pre_lines[14].startswith(b"- [x] **CLOSED c3662"), pre_lines[14][:60]
assert pre_lines[16].startswith(b"- [x] **CLOSED c3661"), pre_lines[16][:60]
assert pre_lines[18] == b"", repr(pre_lines[18])
assert pre_lines[19].startswith(b"- [x] **CLOSED c3660"), pre_lines[19][:60]
assert pre_lines[23].startswith(b"- [x] **CLOSED c3659"), pre_lines[23][:60]
assert pre_lines[25] == b"", repr(pre_lines[25])
assert pre_lines[26] == b"---", repr(pre_lines[26])
assert pre_lines[27] == b"", repr(pre_lines[27])

for i in range(19, 26):
    assert not pre_lines[i].startswith(b"- [ ] "), ("OPEN ITEM IN CUT SPAN", i, pre_lines[i][:80])

archived = pre_lines[19:26]          # c3660, c3659 (+ trailing blank)
post_lines = pre_lines[0:19] + pre_lines[26:]

pre_nb = Counter(l for l in pre_lines if l.strip())
post_nb = Counter(l for l in post_lines if l.strip())
arch_nb = Counter(l for l in archived if l.strip())
missing = pre_nb - (post_nb + arch_nb)
assert not missing, "WOULD LOSE LINES: %r" % [l[:90] for l in missing]
added = (post_nb + arch_nb) - pre_nb
assert not added, "unexpected new content: %r" % [l[:90] for l in added]

post = b"\n".join(post_lines)

TAGS = (b"c3660", b"c3659")

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
for f in ("state/STATUS.md", "notes/PLAYBOOK.md", "notes/LEARNINGS.md", "notes/STANDING.md"):
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
