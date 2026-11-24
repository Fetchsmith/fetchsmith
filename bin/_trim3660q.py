#!/usr/bin/env python3
"""_trim3660q.py -- cycle 3660 floor-5 rotation of tasks/queue.md.

Clone of bin/_trim3657q.py's rotation-only shape (STANDING c3280 /
PLAYBOOK's doc-size-trim-cadence section records that no structural cut
remains measured on this file after six successive censuses, so this is a
rotation, not a failed hunt). OWED FIRST THING at c3660: queue.md measured
205.4KB/979ln at this cycle's `check-doc-size` preflight, ~-1 cycles of
headroom, past the "below ~3 cycles is overdue" rule, and c3658/c3659 both
flagged it for this QUALITY slot (a BUILD slot must not run the trim).

Fresh census (re-derived here, NOT forwarded from c3657, and taken BEFORE
this cycle's own CLOSED block is prepended): 7 contiguous `CLOSED cNNNN`
blocks at the top of the live file, file order chronological (newest
first) -- c3659, c3658, c3657, c3656, c3655, c3654, c3653. Once this
cycle's own c3660 block is prepended that becomes 8 blocks; keep the
newest 5 (c3660, c3659, c3658, c3657, c3656) and archive the oldest 3 BY
POSITION (c3655, c3654, c3653) -- the usual-size rotation (no slot was
skipped since the last trim at c3657, 3 cycles ago).

The cut span (lines 12-20 of the PRE-PREPEND file) contains no `---`
divider -- the one at (pre-prepend) line 21 sits after c3653's block and
stays live, same shape as every prior rotation-only trim. Unlike c3657's
span this one ends on a blank line, so the blank kept at line 11 is what
separates the newest-kept block from that divider.

Follows both _trim3492q.py bug-lessons recorded in PLAYBOOK: the archive
text is built as a STRING and every assert runs BEFORE either file is
opened for writing, and the lossless check compares by VALUE, never `is`.
"""
import os
import shutil
import subprocess
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3660

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")
pre_bytes = len(raw)

# ---------------------------------------------------------------- boundaries
assert pre_lines[11] == b"", repr(pre_lines[11])
assert pre_lines[12].startswith(b"- [x] **CLOSED c3655 -- BUILD slot (3655 % 3 == 1)"), pre_lines[12][:80]
assert pre_lines[13].startswith(b"  - **Next (BUILD slot, c3658 or sooner"), pre_lines[13][:80]
assert pre_lines[14] == b"", repr(pre_lines[14])
assert pre_lines[15].startswith(b"- [x] **CLOSED c3654 -- QUALITY slot (3654 % 3 == 0)"), pre_lines[15][:80]
assert pre_lines[16].startswith(b"  - **Next (QUALITY slot, c3657 or sooner"), pre_lines[16][:80]
assert pre_lines[17] == b"", repr(pre_lines[17])
assert pre_lines[18].startswith(b"- [x] **CLOSED c3653 -- BUILD slot (3653 % 3 == 2)"), pre_lines[18][:80]
assert pre_lines[19].startswith(b"  - **Next (BUILD slot, c3656 or sooner"), pre_lines[19][:80]
assert pre_lines[20] == b"", repr(pre_lines[20])
assert pre_lines[21] == b"---", repr(pre_lines[21])
assert pre_lines[22] == b"", repr(pre_lines[22])

# the 4 blocks we KEEP (pre-prepend; this cycle's own block makes 5 -> floor 5)
for idx, tag in ((0, b"c3659"), (3, b"c3658"), (6, b"c3657"), (10, b"c3656")):
    assert pre_lines[idx].startswith(b"- [x] **CLOSED " + tag), pre_lines[idx][:60]
# and nothing we archive may be an OPEN item spliced between them
for i in range(12, 21):
    assert not pre_lines[i].startswith(b"- [ ] "), ("OPEN ITEM IN CUT SPAN", i, pre_lines[i][:80])

archived = pre_lines[12:21]          # c3655, c3654, c3653 (+ their trailing blanks)
post_lines = pre_lines[0:12] + pre_lines[21:]

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
TAGS = (b"c3655", b"c3654", b"c3653")

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
    print("  archives %d lines (c3655, c3654, c3653)" % len(archived))
    sys.exit(0)

shutil.copy2(QUEUE, QUEUE + ".c3660.pre")
header = "\n\n## Archived by cycle %d\n\n" % CYCLE
body = (
    "### RULE 6b floor-5 rotation: the 3 oldest-by-position `CLOSED` blocks "
    "(c3655, c3654, c3653), verbatim -- the usual-size rotation, no slot was "
    "skipped since the last trim at c3657. No `---` divider fell inside this "
    "span (the one after c3653 stays in the live file).\n\n"
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
