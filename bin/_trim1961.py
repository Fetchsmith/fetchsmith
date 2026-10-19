#!/usr/bin/env python3
"""One-shot, lossless tasks/queue.md -> tasks/queue_archive.md trim for cycle 1961.

`check-doc-size` reports queue.md as OK but it has been flagged as projecting
past the 200KB line for 3 cycles running (1958/1959/1960 all deferred this).
Unlike STATUS.md's cycle-block shape, queue.md is task-items, so the cutoff is
by bullet, not by cycle header. Keeps the 2 still-open `[ ]` items plus the
newest run of closed entries (everything above line 176, the start of the
"CLOSED by cycle 1953" block); archives line 176 onward verbatim.

Also drops one stale duplicate: the `[ ]` TOP ITEM at line 47 ("finish 1958's
doc-size follow-up") describes the exact same trim task as the still-open item
kept at line 13 (carried from 1959/1960) -- it was never removed when 1959/1960
re-filed the same task under a fresher header. Keeping both would re-surface a
dead duplicate from the archive-exempt live file, so it is dropped here (not
archived -- its content is 100% redundant with the kept item, verified by eye
before this script was written).
"""
import sys

LIVE = "/root/agent/tasks/queue.md"
ARCH = "/root/agent/tasks/queue_archive.md"
FIRST_MOVE = 176          # 1-indexed: the "CLOSED by cycle 1953 ... shipped ats-jobs-scraper" line
DUP_START = 47            # 1-indexed: stale duplicate TOP ITEM start
DUP_END = 53              # 1-indexed: last line of that bullet (blank line before next bullet)
LABEL = "tasks/queue.md"

HEADER = (
    "## Archived by cycle 1961 (sonnet-5), 2026-10-19 — {label} was {lines} lines "
    "/ {kb}KB. `check-doc-size` reports OK but this trim was carried as a TOP ITEM "
    "since cycle 1959 (projects past the 200KB Read-tool-adjacent line at its own "
    "next look). Moved everything below the still-open items near the top "
    "(cycle <=1953 closed blocks) verbatim; live file keeps the 2 open items plus "
    "the newest run of closed entries (1954-1960). Newest-first below, same order "
    "as the source file.\n"
)

with open(LIVE, encoding="utf-8") as f:
    orig = f.read()
lines = orig.splitlines(keepends=True)
n = len(lines)
kb = round(len(orig.encode()) / 1024, 1)

dup_idx_start = DUP_START - 1
dup_idx_end = DUP_END  # exclusive
dup_block = lines[dup_idx_start:dup_idx_end]

move_idx = FIRST_MOVE - 1
keep_pre_dup = lines[:dup_idx_start]
keep_post_dup = lines[dup_idx_end:move_idx]
keep = keep_pre_dup + keep_post_dup
moved = lines[move_idx:]

while keep and keep[-1].strip() in ("", "---"):
    keep.pop()

problems = []
if not dup_block or "TOP ITEM for next cycle: finish 1958's doc-size follow-up" not in dup_block[0]:
    problems.append(f"dup block header mismatch: {dup_block[0][:90] if dup_block else '<empty>'!r}")
if dup_block and dup_block[-1].strip() != "":
    problems.append(f"dup block does not end on a blank line: {dup_block[-1]!r}")
if not moved:
    problems.append("nothing to move")
elif "CLOSED by cycle 1953" not in moved[0]:
    problems.append(f"first moved line is not the 1953 block: {moved[0][:90]!r}")
keep_txt_probe = "".join(keep)
if "TOP ITEM for next cycle (carried from 1959" not in keep_txt_probe:
    problems.append("the kept open trim item is missing from live")
if "NEW (cycle 1960, needs a QUALITY/GROWTH slot)" not in keep_txt_probe:
    problems.append("the kept website-screenshot-scraper item is missing from live")
if "finish 1958's doc-size follow-up" in keep_txt_probe:
    problems.append("duplicate TOP ITEM still present in kept half")
if "CLOSED by cycle 1960" not in keep_txt_probe:
    problems.append("newest closed block (1960) missing from kept half")
if problems:
    for p in problems:
        print(f"ABORT {LABEL}: {p}")
    sys.exit(1)

keep_txt = keep_txt_probe
if not keep_txt.endswith("\n"):
    keep_txt += "\n"
moved_txt = "".join(moved)

with open(ARCH, encoding="utf-8") as f:
    arch_before = f.read()
sep = "" if arch_before.endswith("\n\n") else ("\n" if arch_before.endswith("\n") else "\n\n")
new_arch = arch_before + sep + HEADER.format(label=LABEL, lines=n, kb=kb) + "\n" + moved_txt

with open(ARCH, "w", encoding="utf-8") as f:
    f.write(new_arch)
with open(LIVE, "w", encoding="utf-8") as f:
    f.write(keep_txt)

with open(ARCH, encoding="utf-8") as f:
    arch_after = f.read()
with open(LIVE, encoding="utf-8") as f:
    live_after = f.read()

if moved_txt not in arch_after:
    problems.append("moved text NOT found verbatim in archive")
if arch_before not in arch_after:
    problems.append("pre-existing archive content was altered")
missing = [l for l in moved if l.strip() and l not in arch_after]
if missing:
    problems.append(f"{len(missing)} moved lines missing from archive")
if live_after != keep_txt:
    problems.append("live file does not match computed keep half")
both = live_after + "\n" + arch_after
# every original non-blank line should be recoverable, EXCEPT the intentionally
# dropped duplicate block (checked separately above, not re-counted as "lost").
dup_set = set(l for l in dup_block if l.strip())
lost = [l for l in lines if l.strip() and l not in both and l not in dup_set]
if lost:
    problems.append(f"{len(lost)} original lines missing from live+archive+intentional-drop")

if problems:
    for p in problems:
        print(f"ABORT {LABEL}: {p}")
    sys.exit(1)

print(f"{LABEL}: {n} lines / {kb}KB -> {len(live_after.splitlines())} kept "
      f"({round(len(live_after.encode())/1024, 1)}KB), {len(moved)} moved, "
      f"{len(dup_block)} duplicate line(s) dropped")
