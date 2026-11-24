#!/usr/bin/env python3
"""_trim3672q.py -- cycle 3672 floor-5 rotation of tasks/queue.md.

QUALITY slot (3672 % 3 == 0). check-doc-size reads TRIM DUE at 208.8KB/1003ln,
~-2 cycles of headroom -- past the 200KB line, flagged by both c3670's and
c3671's handoffs. Same rotation-only shape as every prior floor-5 trim
(_trim3669q.py template): keep the newest 5 CLOSED blocks (counting this
cycle's own c3672 block once prepended), archive the rest down to the
standing '---' divider.

Fresh census (0-indexed, taken BEFORE this cycle's own block is prepended):
7 contiguous CLOSED blocks at the top -- c3671, c3670, c3669, c3668, c3667,
c3666, c3665 -- then '---' at idx43. Keep c3671/c3670/c3669/c3668 (idx0-26,
which also holds the interleaved OPEN item NEW c3668 untouched); once c3672
is prepended that's 5 kept. Archive c3667 (idx28-30), c3666 and c3665
(idx33-40). The cut is TWO spans, not one, because the OPEN items NEW c3667
(idx31) and NEW c3664 (idx41) are interleaved between the CLOSED blocks and
must stay live -- NEW c3667 is this trim's own STANDING concern.

Per STANDING c3667 a bare rotation no longer clears the line on its own;
bin/_trim3672h.py runs the second half (compressing the dead index-era
arithmetic out of the PARTIALLY DONE tracker head) in the same cycle.
"""
import os
import subprocess
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3672

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")

assert pre_lines[0].startswith(b"- [x] **CLOSED c3671"), pre_lines[0][:60]
assert pre_lines[2].startswith(b"- [x] **CLOSED c3670"), pre_lines[2][:60]
assert pre_lines[11].startswith(b"- [x] **CLOSED c3669"), pre_lines[11][:60]
assert pre_lines[18].startswith(b"- [x] **CLOSED c3668"), pre_lines[18][:60]
assert pre_lines[26].startswith(b"- [ ] **NEW c3668"), pre_lines[26][:60]
assert pre_lines[27] == b"", repr(pre_lines[27])
assert pre_lines[28].startswith(b"- [x] **CLOSED c3667"), pre_lines[28][:60]
assert pre_lines[30] == b"", repr(pre_lines[30])
assert pre_lines[31].startswith(b"- [ ] **NEW c3667"), pre_lines[31][:60]
assert pre_lines[32] == b"", repr(pre_lines[32])
assert pre_lines[33].startswith(b"- [x] **CLOSED c3666"), pre_lines[33][:60]
assert pre_lines[38].startswith(b"- [x] **CLOSED c3665"), pre_lines[38][:60]
assert pre_lines[40] == b"", repr(pre_lines[40])
assert pre_lines[41].startswith(b"- [ ] **NEW c3664"), pre_lines[41][:60]
assert pre_lines[43] == b"---", repr(pre_lines[43])

# Two cut spans; neither may contain an OPEN item.
SPANS = ((28, 31), (33, 41))
for a, b in SPANS:
    for i in range(a, b):
        assert not pre_lines[i].startswith(b"- [ ] "), ("OPEN ITEM IN CUT SPAN", i, pre_lines[i][:80])

# Archive newest-first, in file order: c3667, then c3666 + c3665.
archived = pre_lines[28:31] + pre_lines[33:41]
post_lines = pre_lines[0:28] + pre_lines[31:33] + pre_lines[41:]

pre_nb = Counter(l for l in pre_lines if l.strip())
post_nb = Counter(l for l in post_lines if l.strip())
arch_nb = Counter(l for l in archived if l.strip())
missing = pre_nb - (post_nb + arch_nb)
assert not missing, "WOULD LOSE LINES: %r" % [l[:90] for l in missing]
added = (post_nb + arch_nb) - pre_nb
assert not added, "unexpected new content: %r" % [l[:90] for l in added]

post = b"\n".join(post_lines)

TAGS = (b"c3667", b"c3666", b"c3665")

print("--- hazard pass (c): intra-file references to archived cycles surviving in live file ---")
for tag in TAGS:
    for i, l in enumerate(post_lines):
        if tag in l:
            print("  %s @ live line %d: %s" % (tag.decode(), i, l[:160].decode("utf-8", "replace")))

print("--- hazard pass (a): other state files referencing them ---")
for f in ("state/STATUS.md", "notes/PLAYBOOK.md", "notes/LEARNINGS.md", "notes/STANDING.md"):
    p = os.path.join("/root/agent", f)
    if not os.path.exists(p):
        continue
    out = subprocess.run(["grep", "-c", "-E", "|".join(t.decode() for t in TAGS), p],
                         capture_output=True, text=True)
    print("  %s: %s hits" % (f, out.stdout.strip()))

with open(QUEUE, "wb") as f:
    f.write(post)

header = ("\n## Archived by cycle %d (floor-5 rotation of tasks/queue.md: CLOSED c3667, "
          "c3666 and c3665, verbatim, file order. The interleaved OPEN items NEW c3667 and "
          "NEW c3664 were left live.)\n\n" % CYCLE).encode()
with open(ARCHIVE, "ab") as f:
    f.write(header)
    f.write(b"\n".join(archived))
    f.write(b"\n")

# Independent post-write re-verify against the pre-image.
live_now = open(QUEUE, "rb").read().split(b"\n")
arch_now = open(ARCHIVE, "rb").read().split(b"\n")
have = Counter(l for l in live_now if l.strip()) + Counter(l for l in arch_now if l.strip())
still_missing = [l for l in pre_nb if have[l] < 1]
assert not still_missing, "POST-WRITE LOSS: %r" % [l[:90] for l in still_missing]

print("--- sizes ---")
print("pre  bytes=%d lines=%d" % (len(raw), len(pre_lines)))
print("post bytes=%d lines=%d" % (len(post), len(post_lines)))
print("0 lines lost (%d distinct non-blank lines re-verified against the pre-image)" % len(pre_nb))
print("DONE")
