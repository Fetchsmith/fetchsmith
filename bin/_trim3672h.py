#!/usr/bin/env python3
"""_trim3672h.py -- cycle 3672, the STRUCTURAL half of the queue.md trim.

bin/_trim3672q.py ran the ordinary floor-5 rotation first and landed the file
at 201,996B -- STILL over the 200KB line, which is exactly the failure mode
`NEW c3667` filed as a STANDING concern after c3667 and c3669 both hit it.
This script does the two cuts that actually clear it:

(A) LOWER THE queue.md CLOSED-BLOCK FLOOR FROM 5 TO 3. Archive CLOSED c3669
    and CLOSED c3668 as well, keeping c3671/c3670 + this cycle's own c3672 = 3.
    JUSTIFICATION (the reason this is not information loss, and the reason
    nobody had to spend a cycle finding a new "lever"): a cycle's record
    exists in THREE places -- its `CLOSED cNNNN` block here, its own
    `Updated: ... cycle N` block in `state/STATUS.md` (which keeps the newest
    9 + the running cycle's, re-verified this cycle at exactly 10 by
    bin/_trim3672s.py), and verbatim in `tasks/queue_archive.md` forever.
    Nothing a CLOSED block carries that is still ACTIONABLE stays inside it
    anyway: every live follow-up is promoted to its own `NEW cNNNN` OPEN item
    (NEW c3668/c3667/c3664 are this very cycle's examples, all three left
    live). So kept blocks 4 and 5 were a third copy of a record held twice
    elsewhere, costing ~8KB/trim-cycle in the one file that cannot afford it.
    This is a cadence change, not a one-off: recorded in notes/PLAYBOOK.md's
    `## Doc-size trim cadence for tasks/queue.md` in the same commit.

(B) COMPRESS THE DEAD INDEX-ERA ARITHMETIC out of the `PARTIALLY DONE`
    tracker head (3,933B, the single largest line in the file). c3668 SUSPENDED
    row-count accounting as unreliable and the head's own text says the figures
    are "kept as history only, NOT to be advanced or reconciled" -- so the six
    `(Advanced cNNNN from X/Y ...)` parentheticals, the `(REPAIRED c3649 ...)`
    narrative and the now-MOOT `RULE -- the CONTIGUOUS row count is the ONLY
    authoritative figure ... DERIVE both, NEVER hand-edit them` are all dead
    weight: that rule's subject (a durable contiguous count) no longer exists.
    Archived verbatim; the two rules that are STILL live and enforced (append
    at most one line per batch; the resume pointer lives in `NEW c3162` and
    nowhere else) are kept in place untouched.

Both cuts are archived verbatim under the same `## Archived by cycle 3672`
history as the rotation, and both are asserted lossless before any write.
"""
import os
import subprocess
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3672

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")

# ---- (A) floor 5 -> 3: archive CLOSED c3669 (idx11-17) and c3668 (idx18-25).
assert pre_lines[0].startswith(b"- [x] **CLOSED c3671"), pre_lines[0][:60]
assert pre_lines[2].startswith(b"- [x] **CLOSED c3670"), pre_lines[2][:60]
assert pre_lines[10] == b"", repr(pre_lines[10])
assert pre_lines[11].startswith(b"- [x] **CLOSED c3669"), pre_lines[11][:60]
assert pre_lines[17] == b"", repr(pre_lines[17])
assert pre_lines[18].startswith(b"- [x] **CLOSED c3668"), pre_lines[18][:60]
assert pre_lines[25] == b"", repr(pre_lines[25])
assert pre_lines[26].startswith(b"- [ ] **NEW c3668"), pre_lines[26][:60]
for i in range(11, 26):
    assert not pre_lines[i].startswith(b"- [ ] "), ("OPEN ITEM IN CUT SPAN", i, pre_lines[i][:80])

span_a = pre_lines[11:26]              # c3669 + c3668, file order, with blanks
kept = pre_lines[0:11] + pre_lines[26:]

# ---- (B) compress the PARTIALLY DONE tracker head.
h = [i for i, l in enumerate(kept) if l.startswith(b"- [x] **PARTIALLY DONE")]
assert len(h) == 1, h
HI = h[0]
head = kept[HI].decode("utf-8")
assert len(head) == 3933, len(head)

KEEP_A_END = head.index("See `notes/LEARNINGS.md` c3668 and `NEW c3668`.)") + \
    len("See `notes/LEARNINGS.md` c3668 and `NEW c3668`.)")
CUT_START = head.index(" (Advanced c3661 from 1006/479")
CUT_END = head.index("**RULE, tightened at c3320")
assert KEEP_A_END == CUT_START, (KEEP_A_END, CUT_START)
assert CUT_END > CUT_START, (CUT_START, CUT_END)

cut_text = head[CUT_START:CUT_END]
assert "(Advanced c3659" in cut_text and "(REPAIRED c3649" in cut_text, cut_text[:120]
assert "DERIVE both, NEVER hand-edit them" in cut_text
assert "append AT MOST ONE LINE" not in cut_text         # live rule must not be cut
assert "NOWHERE ELSE" not in cut_text                    # live rule must not be cut

POINTER = (" (COMPRESSED c3672: the six index-era `(Advanced cNNNN from X/Y ...)` "
           "parentheticals (c3661, c3659, c3658, c3656, c3655, c3653), the "
           "`(REPAIRED c3649 ...)` scalar-drift narrative, the `(COMPRESSED c3516 ...)` "
           "pointer, and the now-MOOT `the CONTIGUOUS row count is the ONLY authoritative "
           "figure -- DERIVE both, NEVER hand-edit them` RULE (c3436/c3472 drift) are "
           "verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3672`. They were "
           "cut because c3668 SUSPENDED row-count accounting outright: the rule's subject, "
           "a durable contiguous count, does not exist, so there is nothing left to derive "
           "or hand-edit. The HAND-EDIT-DRIFT LESSON survives and still applies to the "
           "OWNER pointer -- never advance a progress figure by hand, re-derive it; c3436 "
           "found a pair summing to 1,479 not 1,485 and c3472 found `778 of` against `rows "
           "1-784 CONTIGUOUS` in one sentence, each time because a cycle advanced one "
           "figure and left the other behind.) ")
new_head = head[:CUT_START] + POINTER + head[CUT_END:]
assert "append AT MOST ONE LINE" in new_head
assert "NOWHERE ELSE" in new_head
assert "Advanced c3661" not in new_head

post_lines = list(kept)
post_lines[HI] = new_head.encode("utf-8")

# ---- losslessness: everything cut must be in the archive text; the only
# rewritten line is the head, compared BY VALUE (the _trim3492q.py lesson).
archived = span_a + [b"", b"CUT FROM THE `PARTIALLY DONE` TRACKER HEAD (verbatim):", b"",
                     cut_text.strip().encode("utf-8")]

pre_nb = Counter(l for l in pre_lines if l.strip())
post_nb = Counter(l for l in post_lines if l.strip())
arch_nb = Counter(l for l in archived if l.strip())
exempt = Counter([kept[HI]])                     # the one rewritten line, by value
missing = (pre_nb - exempt) - (post_nb + arch_nb)
assert not missing, "WOULD LOSE LINES: %r" % [l[:90] for l in missing]
assert pre_nb[kept[HI]] == 1, pre_nb[kept[HI]]
assert cut_text.strip() in archived[-1].decode("utf-8")

post = b"\n".join(post_lines)

TAGS = (b"c3669", b"c3668")
print("--- hazard pass (c): intra-file refs to archived cycles surviving in live file ---")
for tag in TAGS:
    for i, l in enumerate(post_lines):
        if tag in l:
            print("  %s @ live line %d: %s" % (tag.decode(), i, l[:150].decode("utf-8", "replace")))
print("--- hazard pass (a): other state files ---")
for f in ("state/STATUS.md", "notes/PLAYBOOK.md", "notes/LEARNINGS.md", "notes/STANDING.md"):
    p = os.path.join("/root/agent", f)
    out = subprocess.run(["grep", "-c", "-E", "|".join(t.decode() for t in TAGS), p],
                         capture_output=True, text=True)
    print("  %s: %s hits" % (f, out.stdout.strip()))

with open(QUEUE, "wb") as f:
    f.write(post)
header = ("\n## Archived by cycle %d (part 2, the STRUCTURAL half -- see bin/_trim3672h.py. "
          "(A) CLOSED c3669 and CLOSED c3668, verbatim, file order, archived because c3672 "
          "LOWERED the queue.md CLOSED-block floor from 5 to 3 (a cycle's record is also in "
          "state/STATUS.md's newest-10 window and here forever, and every actionable "
          "follow-up is promoted to its own NEW item). (B) the dead index-era arithmetic cut "
          "from the `PARTIALLY DONE` tracker head.)\n\n" % CYCLE).encode()
with open(ARCHIVE, "ab") as f:
    f.write(header)
    f.write(b"\n".join(archived))
    f.write(b"\n")

live_now = open(QUEUE, "rb").read().split(b"\n")
arch_now = open(ARCHIVE, "rb").read().split(b"\n")
have = Counter(l for l in live_now if l.strip()) + Counter(l for l in arch_now if l.strip())
still_missing = [l for l in (pre_nb - exempt) if have[l] < 1]
assert not still_missing, "POST-WRITE LOSS: %r" % [l[:90] for l in still_missing]

print("--- sizes ---")
print("pre  bytes=%d lines=%d" % (len(raw), len(pre_lines)))
print("post bytes=%d lines=%d  (%+.1f KB)" % (len(post), len(post_lines),
                                              (len(post) - len(raw)) / 1024.0))
print("0 lines lost (%d distinct non-blank lines re-verified; 1 rewritten head line "
      "archived verbatim)" % len(pre_nb))
print("DONE")
