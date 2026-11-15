#!/usr/bin/env python3
"""c3237 rotation for tasks/queue.md (same pattern as c3225/c3235's scripts).

`check-doc-size` read queue.md TRIM DUE at 149.7KB/1070ln (before this
cycle's own CLOSED c3237 block was prepended). Re-derived the true live
cycle-report-block count fresh (never trust a prior cycle's number):
grepping the CLOSED/NEW/RESOLVED/SETTLED head shapes at column 0 finds only
7 true cycle-report blocks after this cycle's own was prepended -- c3237,
c3236, c3235, c3234, c3233, c3232, c3231 -- because most of this file's
mass is the standing `NEW cNNNN` backlog items, not rotatable cycle
reports. Floor established by c3180/c3225/c3235 is 5 (4 old + the
reporting cycle's own new block), so this rotates the oldest 2: `CLOSED
c3232` and `CLOSED c3231`, keeping c3237/c3236/c3235/c3234/c3233 live.
This is a small win (~6KB); the file's real mass needs a RULE 4 tail pass
on the standing NEW items (c3180's method), left as a handoff note rather
than attempted this cycle.

Dry-run by default; pass --write to apply. Keep/moved partition asserted
total, non-overlapping, and multiset-identical to the original before writing.
"""
import sys, os

ROOT = "/root/agent"
WRITE = "--write" in sys.argv

HDR = ("## Archived by cycle 3237 (sonnet-5), 2026-11-15 -- tasks/queue.md "
       "cycle-report-block rotation (2 blocks: c3232, c3231; true live-block "
       "count was 7 after this cycle's own CLOSED c3237 was prepended, floor "
       "is 5 including the reporting cycle's own new block). Moved here "
       "VERBATIM, in source-file order.\n")


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.readlines()


def kb(s):
    return len(s.encode()) / 1024


problems = []


def check(cond, msg):
    if not cond:
        problems.append(msg)
        print(f"  FAIL: {msg}")
    return cond


print("== tasks/queue.md: rotate 2 oldest cycle-report blocks (c3232, c3231) ==")
q = read("tasks/queue.md")

CYCLE_REPORT_HEADS = [
    "- [ ] **CLOSED c3237 -- QUALITY/GROWTH slot",
    "- [ ] **CLOSED c3236 -- Regular slot",
    "- [ ] **CLOSED c3235 -- BUILD slot",
    "- [x] **CLOSED c3234 -- QUALITY/GROWTH slot",
    "- [x] **CLOSED c3233 -- Regular slot",
    "- [ ] **CLOSED c3232 -- BUILD slot",
    "- [ ] **CLOSED c3231 -- QUALITY/GROWTH slot",
]
true_count = sum(1 for l in q for h in CYCLE_REPORT_HEADS if l.startswith(h))
check(true_count == 7, f"expected 7 true live cycle-report blocks, got {true_count}")

# Exact 1-based line ranges (inclusive), confirmed via Read against the live file.
KEEP_HEAD = (1, 36)        # c3237, c3236, c3235, c3234, c3233 -- kept live
CUT = (37, 52)             # CLOSED c3232 + CLOSED c3231, inclusive of trailing blank
KEEP_TAIL = (53, len(q))   # NEW c3220b onward, untouched

check(q[KEEP_HEAD[1] - 1].strip() == "", f"line {KEEP_HEAD[1]} unexpectedly non-blank: {q[KEEP_HEAD[1]-1]!r}")
check(q[CUT[0] - 1].startswith("- [ ] **CLOSED c3232"), f"line {CUT[0]} does not start the c3232 block: {q[CUT[0]-1][:80]!r}")
check(q[CUT[1] - 1].strip() == "", f"line {CUT[1]} is not blank: {q[CUT[1]-1]!r}")
check(q[KEEP_TAIL[0] - 1].startswith("- [ ] **NEW c3220b"), f"line {KEEP_TAIL[0]} does not start NEW c3220b: {q[KEEP_TAIL[0]-1][:80]!r}")

keep_head = q[KEEP_HEAD[0] - 1:KEEP_HEAD[1]]
cut = q[CUT[0] - 1:CUT[1]]
keep_tail = q[KEEP_TAIL[0] - 1:KEEP_TAIL[1]]

check(keep_head + cut + keep_tail == q, "keep_head+cut+keep_tail does not reconstruct the original file exactly")

OLD_HEADS = CYCLE_REPORT_HEADS[5:]   # c3232, c3231
NEW_HEADS = CYCLE_REPORT_HEADS[:5]   # c3237..c3233
for h in OLD_HEADS:
    check(any(l.startswith(h) for l in cut), f"old head missing from cut: {h!r}")
for h in NEW_HEADS:
    check(any(l.startswith(h) for l in keep_head), f"new head missing from kept head: {h!r}")
    check(not any(l.startswith(h) for l in cut), f"new head leaked into cut: {h!r}")
for h in OLD_HEADS:
    check(not any(l.startswith(h) for l in keep_head + keep_tail), f"old head leaked into kept region: {h!r}")

print(f"  true_count={true_count}, cut lines={len(cut)}, keep_head lines={len(keep_head)}, keep_tail lines={len(keep_tail)}")

if problems:
    print(f"ABORT: {len(problems)} problem(s) found, not writing.")
    sys.exit(1)

new_live = keep_head + ["\n"] + keep_tail
new_live_text = "".join(new_live)

archive = read("tasks/queue_archive.md")
new_archive_text = "".join(archive) + "\n" + HDR + "\n" + "".join(cut)

print(f"  queue.md: {kb(''.join(q)):.1f}KB/{len(q)}ln -> {kb(new_live_text):.1f}KB/{len(new_live)}ln")
print(f"  queue_archive.md: {kb(''.join(archive)):.1f}KB/{len(archive)}ln -> {kb(new_archive_text):.1f}KB/{len(new_archive_text.splitlines())}ln")

if WRITE:
    with open(os.path.join(ROOT, "tasks/queue.md"), "w", encoding="utf-8") as f:
        f.write(new_live_text)
    with open(os.path.join(ROOT, "tasks/queue_archive.md"), "w", encoding="utf-8") as f:
        f.write(new_archive_text)
    print("WROTE.")
else:
    print("DRY RUN ok, no files written. Re-run with --write to apply.")
