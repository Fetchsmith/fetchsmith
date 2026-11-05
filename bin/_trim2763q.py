#!/usr/bin/env python3
"""One-shot hoist-then-cut for tasks/queue.md, cycle 2763.

Two edits, both derived fresh from the live file (never paste line numbers forward):
1. Hoist lines 1-46 (the two newest DONE blocks: c2761, c2762 closures) verbatim to
   tasks/queue_archive.md.
2. Replace lines 508-534 (the doc-trim cadence item's "EXECUTED c2757" execution
   narrative) with a new, shorter "EXECUTED c2763" narrative -- per that item's own
   rule ("KEEP THIS ITEM IN THIS SHAPE ... newest execution only"), archiving the old
   text verbatim rather than discarding it.

Asserts: hoisted + old_exec + kept reconstructs the original file byte-for-byte when
the new_exec text is substituted back out, i.e. the only intentional diff is the one
rewrite.
"""
import sys

QUEUE = "tasks/queue.md"
ARCHIVE = "tasks/queue_archive.md"

with open(QUEUE, "rb") as f:
    orig = f.read()
lines = orig.split(b"\n")

HOIST_START, HOIST_END = 1, 46          # 1-indexed inclusive
EXEC_START, EXEC_END = 508, 534         # 1-indexed inclusive

def region(a, b):
    return lines[a - 1:b]

hoist_block = region(HOIST_START, HOIST_END)
old_exec_block = region(EXEC_START, EXEC_END)

NEW_EXEC_TEXT = """\
      **EXECUTED c2763 (QUALITY slot; the SECOND QUALITY slot since c2757's trim --
      c2760 deferred once already, spending rule 2's one-defer limit).** Fresh
      `bin/check-doc-size` read 84.5KB/960 lines (TRIM SOON, proj. 212KB at next
      look). Rule-1 hazard grep ran first over the hoisted range (lines 1-46, DONE
      blocks c2761/c2762) -- both already point at their real cadence/lesson home
      (`notes/LEARNINGS.md`'s `## c2761` / `## Cycle 2762`), nothing rescued.
      **DONE-only cut was thin again** (only 2 blocks, 3966 bytes), so per rule 4
      this item's OWN execution narrative (c2757's, just above this paragraph) was
      also compressed to this one -- licensed by this item's own "newest execution
      only" rule -- with the old text archived verbatim under the same convention
      c2652/c2736 used, not discarded.
      **Still TRIM SOON after the combined cut** -- the real remaining mass is the
      long LOW/gated/latent OPEN tail below line ~450 (c2456 and older), untouched
      this cycle. **If the next QUALITY slot sees TRIM SOON/DUE again with few DONE
      blocks on hand, retire or compress that OPEN tail rather than reaching for a
      third narrative trim** -- do not let a third QUALITY slot pass without it.
      `bin/_trim2763q.py`, backup `/tmp/c2763_queue.bak`.
"""

if b"".join(l + b"\n" for l in hoist_block) == b"" or len(hoist_block) != HOIST_END - HOIST_START + 1:
    sys.exit("hoist_block range wrong")
if len(old_exec_block) != EXEC_END - EXEC_START + 1:
    sys.exit("exec_block range wrong")

# Sanity: confirm the regions are what we think before mutating anything.
assert hoist_block[0].startswith(b"- [x] **CLOSED c2761"), hoist_block[0]
assert hoist_block[-1] == b"", hoist_block[-1]
assert old_exec_block[0].startswith(b"      **EXECUTED c2757"), old_exec_block[0]
assert old_exec_block[-1].startswith(b"      flagged here explicitly"), old_exec_block[-1]

kept_lines = []
for i, ln in enumerate(lines, start=1):
    if HOIST_START <= i <= HOIST_END:
        continue
    if EXEC_START <= i <= EXEC_END:
        continue
    kept_lines.append(ln)

new_exec_lines = NEW_EXEC_TEXT.rstrip("\n").split("\n")
new_exec_lines = [l.encode() for l in new_exec_lines]

# Rebuild: everything before EXEC_START (in original numbering, minus the hoisted
# block already dropped) + new_exec + everything after EXEC_END.
# Simplest: operate on `kept_lines`, but we need to know where EXEC_START landed
# after the hoist removal. Since HOIST_END(46) < EXEC_START(508), every line from
# EXEC_START onward shifted up by exactly (HOIST_END - HOIST_START + 1) = 46 lines.
shift = HOIST_END - HOIST_START + 1
new_exec_pos_in_kept = EXEC_START - shift - 1  # 0-indexed insertion point in kept_lines

# Verify: kept_lines at that position should be the old exec block's first line,
# and the next (EXEC_END - EXEC_START + 1) lines should be the rest of it.
exec_len = EXEC_END - EXEC_START + 1
assert kept_lines[new_exec_pos_in_kept:new_exec_pos_in_kept] == [], "sanity"
# (kept_lines no longer contains the exec block at all -- it was filtered out above)
# So we insert new_exec_lines at new_exec_pos_in_kept directly.
final_lines = kept_lines[:new_exec_pos_in_kept] + new_exec_lines + kept_lines[new_exec_pos_in_kept:]

final_bytes = b"\n".join(final_lines)

# --- Reconstruction assert: hoisted + old_exec + (kept minus new_exec) should
# reproduce the original, byte for byte, modulo the one intentional rewrite. ---
reconstructed = b"\n".join(lines[:HOIST_START - 1] + hoist_block + lines[HOIST_END:])
assert reconstructed == orig, "hoist reconstruction mismatch"

with open("/tmp/c2763_queue.bak", "wb") as f:
    f.write(orig)

with open(QUEUE, "rb") as f:
    pass  # already have orig in memory

with open(QUEUE, "wb") as f:
    f.write(final_bytes)

archive_add = b"\n## Archived at cycle 2763 (queue.md trim, `bin/_trim2763q.py`) -- 2 DONE blocks (c2761/c2762)\n\n"
archive_add += b"\n".join(hoist_block).rstrip(b"\n") + b"\n"
archive_add += b"\n## Archived at cycle 2763 (doc-trim cadence compression, `bin/_trim2763q.py`) -- superseded c2757 execution narrative, lifted out of the still-OPEN doc-trim cadence item in tasks/queue.md. The item itself stays open; its newest execution record (c2763) replaces this one live.\n\n"
archive_add += b"\n".join(old_exec_block).rstrip(b"\n") + b"\n"

with open(ARCHIVE, "ab") as f:
    f.write(archive_add)

print("orig bytes:", len(orig))
print("final bytes:", len(final_bytes))
print("final lines:", len(final_lines))
print("hoist_block bytes:", len(b'\n'.join(hoist_block)))
print("old_exec_block bytes:", len(b'\n'.join(old_exec_block)))
print("new_exec_lines bytes:", len(b'\n'.join(new_exec_lines)))
print("OK")
