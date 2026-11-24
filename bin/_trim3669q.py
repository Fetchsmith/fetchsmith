#!/usr/bin/env python3
"""_trim3669q.py -- cycle 3669 floor-5 rotation of tasks/queue.md.

QUALITY slot (3669 % 3 == 0). check-doc-size reads TRIM DUE, file past the
200KB line (219,808 bytes before this cycle's own prepended block). Same
rotation-only shape as every prior floor-5 trim (_trim3667q.py template):
keep the newest 5 CLOSED blocks (counting this cycle's own c3669 block
once prepended), archive the rest down to the standing '---' divider.

Fresh census (0-indexed, taken BEFORE this cycle's own block is prepended):
7 contiguous CLOSED blocks at the top -- c3668, c3667, c3666, c3665, c3663,
c3662, c3661 -- then '---' at line 34. Keep c3668/c3667/c3666/c3665 (lines
0-24, which also holds the interleaved OPEN items NEW c3668/NEW c3667/NEW
c3664 untouched); once c3669 is prepended that's 5 kept. Archive
c3663/c3662/c3661 (lines 25-33).
"""
import subprocess
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3669

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")

assert pre_lines[0].startswith(b"- [x] **CLOSED c3668"), pre_lines[0][:60]
assert pre_lines[8].startswith(b"- [ ] **NEW c3668"), pre_lines[8][:60]
assert pre_lines[10].startswith(b"- [x] **CLOSED c3667"), pre_lines[10][:60]
assert pre_lines[13].startswith(b"- [ ] **NEW c3667"), pre_lines[13][:60]
assert pre_lines[15].startswith(b"- [x] **CLOSED c3666"), pre_lines[15][:60]
assert pre_lines[20].startswith(b"- [x] **CLOSED c3665"), pre_lines[20][:60]
assert pre_lines[23].startswith(b"- [ ] **NEW c3664"), pre_lines[23][:60]
assert pre_lines[24] == b"", repr(pre_lines[24])
assert pre_lines[25].startswith(b"- [x] **CLOSED c3663"), pre_lines[25][:60]
assert pre_lines[29].startswith(b"- [x] **CLOSED c3662"), pre_lines[29][:60]
assert pre_lines[31].startswith(b"- [x] **CLOSED c3661"), pre_lines[31][:60]
assert pre_lines[33] == b"", repr(pre_lines[33])
assert pre_lines[34] == b"---", repr(pre_lines[34])
assert pre_lines[35] == b"", repr(pre_lines[35])

for i in range(25, 34):
    assert not pre_lines[i].startswith(b"- [ ] "), ("OPEN ITEM IN CUT SPAN", i, pre_lines[i][:80])

archived = pre_lines[25:34]          # c3663, c3662, c3661 (+ trailing blank)
post_lines = pre_lines[0:25] + pre_lines[34:]

pre_nb = Counter(l for l in pre_lines if l.strip())
post_nb = Counter(l for l in post_lines if l.strip())
arch_nb = Counter(l for l in archived if l.strip())
missing = pre_nb - (post_nb + arch_nb)
assert not missing, "WOULD LOSE LINES: %r" % [l[:90] for l in missing]
added = (post_nb + arch_nb) - pre_nb
assert not added, "unexpected new content: %r" % [l[:90] for l in added]

post = b"\n".join(post_lines)

TAGS = (b"c3663", b"c3662", b"c3661")

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
