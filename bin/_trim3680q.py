#!/root/agent/venv/bin/python
"""Cycle 3680 trim on tasks/queue.md -- two passes, both lossless, both verified from disk.

PASS 1 (ordinary floor-3 rotation, per the c3672 cadence in notes/PLAYBOOK.md): with this
cycle's own `CLOSED c3680` prepended the file holds 5 CLOSED blocks (c3680, c3679, c3678,
c3677, c3676). Archive the two oldest -- `CLOSED c3677` and `CLOSED c3676` -- verbatim, to
hold the floor at 3.

PASS 2 (structural, because the rotation alone does not clear the 200,000B line): cut the
two DEAD parentheticals out of the `PARTIALLY DONE` tracker head and compress the dead
`Running score` line. Both are declared dead BY THE FILE'S OWN TEXT -- the index-era
figures are "kept as history only, NOT to be advanced or reconciled" and the running-score
counters are "BOTH COUNTERS ARE UNRELIABLE, do not quote either as fact" -- and both are
already recoverable from `queue_archive.md`/git. What SURVIVES in place, deliberately:
the OWNER-pointer resumption authority, the HAND-EDIT-DRIFT LESSON, the one-line-per-batch
RULE, the "resume pointer lives in NEW c3162 and NOWHERE ELSE" rule, and the pointer to
`NEW c3348` as the open reconciliation.

Rewritten lines are compared BY VALUE (the _trim3492q.py lesson), not by multiset identity.
"""
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCH = "/root/agent/tasks/queue_archive.md"
HEADER = "## Archived by cycle 3680"

orig = open(QUEUE).read()
lines = orig.split("\n")


def block(head_prefix, src):
    start = next(i for i, l in enumerate(src) if l.startswith(head_prefix))
    end = start + 1
    while end < len(src) and not src[end].startswith(("- [ ] **", "- [x] **")):
        end += 1
    assert src[end - 1].strip() == "", repr(src[end - 1])
    return start, end


# ---------- PASS 1: floor-3 rotation ----------
cuts = []
work = list(lines)
for head in ("- [x] **CLOSED c3677 --", "- [x] **CLOSED c3676 --"):
    s, e = block(head, work)
    cuts.append(work[s:e - 1])            # body only, no separating blank
    work = work[:s] + work[e - 1:]
assert cuts[0][0].startswith("- [x] **CLOSED c3677 --")
assert cuts[1][0].startswith("- [x] **CLOSED c3676 --")

moved = Counter(lines) - Counter(work)
assert moved == Counter(cuts[0]) + Counter(cuts[1]), moved

# ---------- PASS 2: structural ----------
s, _ = block("- [x] **PARTIALLY DONE -- row-count accounting SUSPENDED", work)
head = work[s]
score = work[s + 2]
assert score.startswith("  **Running score -- BOTH COUNTERS ARE UNRELIABLE"), score[:60]

dead1_a = head.index(" (Last index-era figures")
dead1_b = head.index("**RULE, tightened at c3320")
# The HAND-EDIT-DRIFT LESSON sits inside this parenthetical and is LIVE reusable method
# (grepped c3680 per the c3492 rule: 0 hits in LEARNINGS/PLAYBOOK/STANDING, so queue.md is
# its only home). Preserve it verbatim in place; cut only the dead history around it.
keep_a = head.index("The HAND-EDIT-DRIFT LESSON")
keep = head[keep_a:dead1_b].rstrip()
assert keep.startswith("The HAND-EDIT-DRIFT LESSON") and keep.endswith("left the other behind.)")
keep = "(" + keep                        # re-open the parenthesis the cut removed
dead1 = head[dead1_a:keep_a]
assert dead1.startswith(" (Last index-era figures") and "COMPRESSED c3672" in dead1
new_head = head[:dead1_a] + " " + keep + " " + head[dead1_b:]

new_score = ("  **Running score -- SUSPENDED, both counters unreliable (do not quote either); "
             "the open reconciliation is `NEW c3348` below, and the NAMED FINDS in the "
             "per-batch line are the reliable record.** Dead figures and the full c3348 "
             "narrative: `tasks/queue_archive.md`, `## Archived by cycle 3680` (this line's "
             "own earlier versions are under `## Archived by cycle 3348`/`3360`).")

new_lines = list(work)
new_lines[s] = new_head
new_lines[s + 2] = new_score
new_queue = "\n".join(new_lines)

# relocated-verbatim payload for pass 2
reloc = [
    "**Relocated verbatim from the `PARTIALLY DONE` tracker head (dead index-era figures and "
    "c3672 compression meta -- the block's own text had already declared them history, NOT to "
    "be advanced or reconciled):**",
    "",
    dead1.strip(),
    "",
    "**Relocated verbatim -- the dead `Running score` line (both counters declared unreliable "
    "by their own text; replaced in place by a one-sentence pointer):**",
    "",
    score.strip(),
]

arch_orig = open(ARCH).read()
new_arch = (arch_orig.rstrip("\n") + "\n\n" + HEADER + "\n\n"
            + "\n".join(cuts[0]) + "\n\n" + "\n".join(cuts[1]) + "\n\n"
            + "\n".join(reloc) + "\n")

# ---------- losslessness, BEFORE any write ----------
for l in cuts[0] + cuts[1]:
    assert l in new_arch, l[:80]
assert dead1.strip() in new_arch and score.strip() in new_arch
# every survivor of the two rewritten lines must still be present somewhere
for keep in ("progress is now tracked by OWNER in the `NEW c3162` RESUME POINTER below",
             "The HAND-EDIT-DRIFT LESSON survives and still applies to the OWNER pointer",
             "append AT MOST ONE LINE per future batch",
             "Resume pointer lives in `NEW c3162` below and NOWHERE ELSE",
             "`NEW c3348`"):
    assert keep in new_queue, keep
# nothing else in the file moved
untouched_before = Counter(l for i, l in enumerate(work) if i not in (s, s + 2))
untouched_after = Counter(l for i, l in enumerate(new_lines) if i not in (s, s + 2))
assert untouched_before == untouched_after

open(QUEUE, "w").write(new_queue)
open(ARCH, "w").write(new_arch)

# ---------- independent post-write re-verify ----------
q2, a2 = open(QUEUE).read(), open(ARCH).read()
assert q2 == new_queue and a2 == new_arch
for l in cuts[0] + cuts[1]:
    assert l not in q2.split("\n"), l[:80]
    assert l in a2.split("\n"), l[:80]
assert dead1.strip() not in q2 and dead1.strip() in a2
assert score not in q2.split("\n") and score.strip() in a2
print(f"queue.md {len(orig)}B/{len(lines)}ln -> {len(q2)}B/{len(q2.split(chr(10)))}ln; "
      f"archive {len(arch_orig)}B -> {len(a2)}B; rotated CLOSED c3677+c3676 "
      f"({len(cuts[0]) + len(cuts[1])} lines) and relocated {len(dead1) + len(score)}B of "
      f"dead tracker text, lossless.")
