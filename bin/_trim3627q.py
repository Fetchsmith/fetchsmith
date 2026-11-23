#!/usr/bin/env python3
"""_trim3627q.py -- cycle 3627 QUALITY-slot trim of tasks/queue.md.

Clone of bin/_trim3624q.py (assert-exact-boundary pattern, archive-as-string-
then-write, independent post-write re-verify). Does BOTH halves in one write,
per c3624's handoff: the floor-5 rotation alone has undershot growth three
cycles running (c3618 -12.6KB, c3621 -10.7KB, c3624 -15.3KB of its -16.1KB
vs ~5.4KB/cycle growth), so PAIR it with a structural cut every time.

PART A (RULE 6b floor-5 rotation): fresh census found 8 contiguous
`CLOSED cNNNN` blocks (c3626, c3625, c3624, c3623, c3622, c3621, c3618,
c3619 -- file order is NOT chronological). Rotate the OLDEST 3 BY POSITION
(c3621, c3618, c3619; lines 26-43) and keep the newest 5 by position
(c3626, c3625, c3624, c3623, c3622), so c3627's own block makes 6.

PART B (structural compression -- one of the 3 candidates STANDING c3280
named at c3624): `NEW c3516` (TRIVIAL/method, one bullet, no live tracking
state) is removed from tasks/queue.md entirely. Both lessons inside it were
RELOCATED VERBATIM to notes/PLAYBOOK.md, `## Checker output hygiene -- never
truncate a checker run, head or tail`, in a separate edit BEFORE this script
ran. Per c3516's own instruction ("fold this rule into NEW c3372's method
paragraph at its next compression"), a short cross-reference sentence was
ALSO appended to `NEW c3372`'s existing method paragraph (line 94) in a
separate edit before this script ran, so nothing is lost: the full writeup
lives in PLAYBOOK, and c3372 (which has live tracking state and stays in
queue.md) carries a one-sentence pointer to it.
"""
import os
import shutil
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3627

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")
pre_bytes = len(raw)

# ---------------- PART A boundaries: assert, never trust a line number -----
A_START = 25   # 0-indexed; live line 26
A_END = 42     # 0-indexed inclusive; live line 43 (blank)
assert pre_lines[A_START].startswith(
    b"- [x] **CLOSED c3621 -- QUALITY slot (3621 % 3 == 0)."
), pre_lines[A_START][:120]
assert pre_lines[31].startswith(
    b"- [x] **CLOSED c3618 -- QUALITY slot (3618 % 3 == 0)."
), pre_lines[31][:120]
assert pre_lines[37].startswith(
    b"- [x] **CLOSED c3619 -- BUILD slot (3619 % 3 == 1)."
), pre_lines[37][:120]
assert pre_lines[A_END] == b"", repr(pre_lines[A_END])
assert pre_lines[A_END - 1] == b"---", repr(pre_lines[A_END - 1])
assert pre_lines[A_END + 1].startswith(b"- [ ] **NEW c3620 (LOW"), pre_lines[A_END + 1][:80]
# the 5 blocks we KEEP must all still be CLOSED blocks after the cut
for idx, tag in ((0, b"c3626"), (5, b"c3625"), (10, b"c3624"), (16, b"c3623"), (19, b"c3622")):
    assert pre_lines[idx].startswith(b"- [x] **CLOSED " + tag), pre_lines[idx][:60]

part_a = pre_lines[A_START:A_END + 1]
assert len(part_a) == 18, len(part_a)

# ---------------- PART B boundaries ----------------------------------------
# NEW c3516 (one bullet) plus ONE of its two surrounding blank lines (the
# file already carried a double-blank before NEW c3514; removing one blank
# along with the bullet leaves a normal single-blank separator, not a gap).
B_START = 57   # 0-indexed; live line 58 (the bullet)
B_END = 58     # 0-indexed; live line 59 (a blank line, removed with it)
assert pre_lines[56] == b"", repr(pre_lines[56])
assert pre_lines[B_START].startswith(
    b"- [ ] **NEW c3516 (TRIVIAL/method, HIGH value for its cost"
), pre_lines[B_START][:100]
assert pre_lines[B_END] == b"", repr(pre_lines[B_END])
assert pre_lines[59] == b"", repr(pre_lines[59])  # the blank that SURVIVES as separator
assert pre_lines[60].startswith(b"- [ ] **NEW c3514 (LOW"), pre_lines[60][:80]
old_c3516 = pre_lines[B_START]
assert len(old_c3516) > 2500, len(old_c3516)

# ---------------- PART C: fold a pointer into NEW c3372 ---------------------
C = 93  # 0-indexed; live line 94
assert pre_lines[C].startswith(
    b"- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh"
), pre_lines[C][:100]
old_c3372 = pre_lines[C]
tail_anchor = (
    b"a missing `N checked, N flagged` footer means the run did not finish, "
    b"whatever the exit code says.**"
)
assert old_c3372.endswith(tail_anchor), old_c3372[-200:]
fold_in = (
    b" **c3627 -- the companion failure mode: `tail -N` is NOT safe either, "
    b"it reads to EOF so the footer prints while silently discarding the "
    b"FIRST N lines (lost a whole fleet-wide section this way at c3516, 69 "
    b"claimed vs 59 visible). Never truncate a checker run at either end -- "
    b"redirect to a file and read the file. Full writeup relocated c3627 to "
    b"`notes/PLAYBOOK.md`, `## Checker output hygiene`.**"
)
new_c3372 = old_c3372 + fold_in

# ---------------- build the new live file ---------------------------------
post_lines = list(pre_lines)
post_lines[C] = new_c3372
del post_lines[B_START:B_END + 1]
del post_lines[A_START:A_END + 1]
post = b"\n".join(post_lines)

# ---------------- losslessness: multiset identity BEFORE the write --------
archived = part_a + [old_c3516]
pre_nb = Counter(l for l in pre_lines if l.strip())
post_nb = Counter(l for l in post_lines if l.strip())
arch_nb = Counter(l for l in archived if l.strip())
missing = pre_nb - (post_nb + arch_nb)
# old_c3372 is replaced by new_c3372 (a superset, old_c3372 is a strict
# prefix of it), so old_c3372 legitimately drops out of post_nb -- account
# for it explicitly rather than letting the assert trip on it.
missing_adj = missing - Counter({old_c3372: 1})
assert not missing_adj, "WOULD LOSE LINES: %r" % [l[:90] for l in missing_adj]
added = (post_nb + arch_nb) - pre_nb
assert list(added) == [new_c3372], "unexpected new content: %r" % [l[:90] for l in added]

if "--dry-run" in sys.argv:
    print("DRY RUN ok: %d -> %d bytes (%+d), %d -> %d lines; archiving %d lines"
          % (pre_bytes, len(post), len(post) - pre_bytes,
             len(pre_lines), len(post_lines), len(archived)))
    sys.exit(0)

# ---------------- write: archive FIRST, then the live file -----------------
shutil.copy2(QUEUE, QUEUE + ".c3627.pre")
header = "\n\n## Archived by cycle %d\n\n" % CYCLE
body = (
    "### PART A -- RULE 6b floor-5 rotation: the 3 oldest-by-position `CLOSED` blocks "
    "(c3621, c3618, c3619), verbatim\n\n"
    + "\n".join(l.decode("utf-8") for l in part_a)
    + "\n\n### PART B -- the full pre-relocation `NEW c3516` block, verbatim (both lessons "
      "now live in notes/PLAYBOOK.md, `## Checker output hygiene`)\n\n"
    + old_c3516.decode("utf-8")
    + "\n"
)
with open(ARCHIVE, "a", encoding="utf-8") as fh:
    fh.write(header + body)
with open(QUEUE, "wb") as fh:
    fh.write(post)

# ---------------- independent post-write re-verify ------------------------
live_now = open(QUEUE, "rb").read().split(b"\n")
arch_now = open(ARCHIVE, "rb").read().split(b"\n")
have = Counter(l for l in live_now if l.strip()) + Counter(l for l in arch_now if l.strip())
have[old_c3372] += 1  # satisfied by being a prefix of new_c3372, not a literal line anywhere
still_missing = [l for l in pre_nb if have[l] < 1]
assert not still_missing, "POST-WRITE LOSS: %r" % [l[:90] for l in still_missing]
assert new_c3372 in Counter(l for l in live_now if l.strip())
print("WROTE. %d -> %d bytes (%+.1f KB), %d -> %d lines. 0 lines lost (re-verified "
      "against the pre-image, %d distinct non-blank lines checked)."
      % (pre_bytes, len(post), (len(post) - pre_bytes) / 1024.0,
         len(pre_lines), len(post_lines), len(pre_nb)))
print("archive now %.1f MB" % (os.path.getsize(ARCHIVE) / 1048576.0))
