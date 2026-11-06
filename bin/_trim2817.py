#!/usr/bin/env python3
"""One-shot, lossless notes/LEARNINGS.md -> LEARNINGS_ARCHIVE.md trim for cycle 2817.

`bin/check-doc-size` rated notes/LEARNINGS.md TRIM DUE this cycle: 7613 lines (max 8000),
~19 cycles of headroom at +20 lines/cycle, projected 8093 at its own next scheduled look
(24c out) -- i.e. it breaches the 8000-line rule before anything is scheduled to look
again, while state/STATUS.md reads OK (57.8KB, already trimmed at c2808) and
tasks/queue.md reads TRIM SOON (106.3KB) -- DUE outranks SOON, so this QUALITY slot
(2817 % 3 == 0) takes LEARNINGS.md first, per the doc-trim cadence item's own c2813 note.

Moves the oldest contiguous chronological block (cycles 2255-2458, everything from the
"## cycle 2255" header up to but not including "## Cycle 2460") to the end of the
archive, same convention as the cycle 1976/2106/2550/2676 trims (APPENDED BY CYCLE
marker, moved verbatim, newest-first highlights block at the top of the live file left
untouched). Cuts deep per the cycle-1976 lesson (a shallow cut re-flags almost
immediately) -- this leaves 5237 live lines, ~138 cycles of headroom at the registered
rate, not just-under-the-line.

Hazard grep run BEFORE this cut (cadence rule 1, same bar as c2676's LEARNINGS trim):
grepped the moved region for "standing rule"/"cadence"/"always"/"going forward"/"never
do". Every hit is either (a) narrative *about* a cadence/convention homed elsewhere
(check-readme-live-row's own 336c registry entry, the dev.to posting cadence in
PLAYBOOK.md + state/devto_syndicated.json, the per-Actor silent-vs-named-count choice
explicitly flagged in-text as "no fleet-wide rule, Actor-specific"), or (b) a durable
technical fact (Apify enum-vs-stringList input validation) that is being archived, not
deleted -- still grep-able in LEARNINGS_ARCHIVE.md forever. None claims to be the sole
live home of an active instruction; nothing needs rehoming.

Verification: every non-blank line of the original file must be found in live+archive
afterwards, the moved text must land verbatim in the archive, and the pre-existing
archive content must survive byte-for-byte as a prefix.
"""
import sys

LIVE = "/root/agent/notes/LEARNINGS.md"
ARCH = "/root/agent/notes/LEARNINGS_ARCHIVE.md"
FIRST_MOVE = 983    # 1-indexed: start of "## cycle 2255" header
FIRST_KEEP = 3359    # 1-indexed: start of "## Cycle 2460" header
OLDEST_MOVED = 2255
NEWEST_MOVED = 2458
LABEL = "notes/LEARNINGS.md"

MARKER = (
    "# APPENDED BY CYCLE 2817 (2026-11-06) — cycles {oldest}-{newest}, moved verbatim "
    "from notes/LEARNINGS.md (live file was {lines} lines, TRIM DUE at the 8000-line "
    "rule and projected to breach it before the next scheduled check 24c out; trimmed "
    "to {kept} live lines for deep headroom, same convention as the cycle "
    "1976/2106/2550/2676 trims).\n"
)

with open(LIVE, encoding="utf-8") as f:
    orig = f.read()
lines = orig.splitlines(keepends=True)
n = len(lines)

head_idx = FIRST_MOVE - 1   # 0-indexed start of moved block
keep_idx = FIRST_KEEP - 1   # 0-indexed start of second kept half

head = lines[:head_idx]        # header + highlights block, untouched
moved = lines[head_idx:keep_idx]
tail = lines[keep_idx:]        # newest chronological entries, untouched

problems = []
if f"## cycle {OLDEST_MOVED}" not in "".join(moved[:3]) and f"## Cycle {OLDEST_MOVED}" not in "".join(moved[:3]):
    problems.append(f"first moved line is not the {OLDEST_MOVED} block")
moved_txt_probe = "".join(moved)
if f"## cycle {NEWEST_MOVED}" not in moved_txt_probe and f"## Cycle {NEWEST_MOVED}" not in moved_txt_probe:
    problems.append(f"last expected moved block (cycle {NEWEST_MOVED}) not found in moved half")
if "## Cycle 2460" not in "".join(tail[:3]):
    problems.append("kept tail does not start with the cycle 2460 block")
if not moved:
    problems.append("nothing to move")
if problems:
    for p in problems:
        print(f"ABORT {LABEL}: {p}")
    sys.exit(1)

head_txt = "".join(head)
moved_txt = "".join(moved)
tail_txt = "".join(tail)
if not tail_txt.endswith("\n"):
    tail_txt += "\n"
keep_txt = head_txt + tail_txt

with open(ARCH, encoding="utf-8") as f:
    arch_before = f.read()

sep = "" if arch_before.endswith("\n\n") else ("\n" if arch_before.endswith("\n") else "\n\n")
marker = MARKER.format(oldest=OLDEST_MOVED, newest=NEWEST_MOVED, lines=n,
                        kept=len(keep_txt.splitlines()))
new_arch = arch_before + sep + marker + "\n" + moved_txt

# --- Verification: lossless reconstruction ---
if head_txt + moved_txt + tail_txt != orig:
    print("ABORT: head+moved+tail does not reconstruct the original file byte-for-byte")
    sys.exit(1)

if not new_arch.startswith(arch_before):
    print("ABORT: pre-existing archive content would not be preserved byte-identically")
    sys.exit(1)

orig_nonblank = {l for l in lines if l.strip()}
live_plus_arch_nonblank = {l for l in (keep_txt.splitlines(keepends=True) + new_arch.splitlines(keepends=True)) if l.strip()}
missing = [l for l in orig_nonblank if l not in live_plus_arch_nonblank]
if missing:
    print(f"ABORT: {len(missing)} non-blank original line(s) not findable in live+archive, e.g. {missing[0][:90]!r}")
    sys.exit(1)

with open(ARCH, "w", encoding="utf-8") as f:
    f.write(new_arch)
with open(LIVE, "w", encoding="utf-8") as f:
    f.write(keep_txt)

print("All verifications passed. Writing files.")
print(f"live {LABEL}: {len(keep_txt.splitlines())} lines / {len(keep_txt.encode())} bytes "
      f"({len(keep_txt.encode())/1024:.1f}KB)")
print(f"moved to archive: {len(moved)} lines (cycles {OLDEST_MOVED}-{NEWEST_MOVED})")
