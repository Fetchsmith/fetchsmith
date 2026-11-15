#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3235 (preflight found 1 fleet
check due -- check-dead-endpoint-docs, closed clean, 0 undisclosed -- leaving
time for the standing TRIM DUE housekeeping, same as c3225/c3180's pattern).

`check-doc-size` reads queue.md TRIM DUE at 173.5KB/1125ln, ~5c headroom.
Re-derived the TRUE live cycle-report-block count via `grep -n` for the four
head shapes (CLOSED/NEW/RESOLVED/SETTLED, either checkbox state) at column 0
(sub-items are indented and excluded by construction): 11 live blocks, newest
to oldest -- c3234, c3233, c3232, c3231, c3228, c3226, c3225, c3224, c3223,
c3222, c3221. Floor established by c3180/c3225 is 5 total including the
reporting cycle's own new block, i.e. keep 4 old + 1 new = 5. 11 - 4 = 7 to
rotate: c3228, c3226, c3225, c3224, c3223, c3222, c3221 (oldest 7), keeping
c3234/c3233/c3232/c3231 (newest 4) live.

RULE 1/8 hazard grep ran first: `grep -rn "CLOSED c322[1-8]\|CLOSED c3226\b"`
style bare-cycle references outside queue.md found only the expected
self-contained provenance (`bin/_trim3225q.py`'s own docstring narrating
c3221-3224 by name, `notes/LEARNINGS.md`'s own dated history, STATUS.md's own
per-cycle narrative -- a separate document, not a pointer INTO queue.md). The
c3060 second grep ON the live queue for c3221-3228 OUTSIDE the cut range found
none -- `NEW c3220b`'s sub-items (c3227/c3229/c3230) reference "the named next
target" and prior candidates by Actor slug, never by citing "CLOSED c3222"
etc. by number, so nothing dangles.

Dry-run by default; pass --write to apply. Keep/moved partition asserted
total, non-overlapping, and multiset-identical to the original before writing.
"""
import sys, os

ROOT = "/root/agent"
WRITE = "--write" in sys.argv

HDR = ("## Archived by cycle 3235 (sonnet-5), 2026-11-15 -- tasks/queue.md "
       "RULE 6b rotation (7 cycle-report blocks: c3228 down to c3221; true "
       "live-block count was 11, floor is 5 including the reporting cycle's "
       "own new block, so keep newest 4 live). Moved here VERBATIM, in "
       "source-file order.\n")


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


print("== tasks/queue.md: RULE 6b rotation (7 oldest cycle-report blocks) ==")
q = read("tasks/queue.md")

CYCLE_REPORT_HEADS = [
    "- [x] **CLOSED c3234 -- QUALITY/GROWTH slot",
    "- [x] **CLOSED c3233 -- Regular slot",
    "- [ ] **CLOSED c3232 -- BUILD slot",
    "- [ ] **CLOSED c3231 -- QUALITY/GROWTH slot",
    "- [ ] **CLOSED c3228 -- QUALITY/GROWTH slot",
    "- [ ] **CLOSED c3226 -- Regular slot",
    "- [ ] **CLOSED c3225 -- QUALITY/GROWTH slot",
    "- [ ] **CLOSED c3224 -- Regular slot",
    "- [ ] **CLOSED c3223 -- Regular slot",
    "- [ ] **CLOSED c3222 -- QUALITY/GROWTH slot",
    "- [ ] **CLOSED c3221 -- `NEW c3220` SHIPPED",
]
true_count = sum(1 for l in q for h in CYCLE_REPORT_HEADS if l.startswith(h))
check(true_count == 11, f"expected 11 true live cycle-report blocks, got {true_count}")

# Exact 1-based line ranges (inclusive), confirmed via Read against the live file.
KEEP_HEAD = (1, 29)     # c3234, c3233, c3232, c3231 -- kept live
CUT = (30, 99)          # blank sep + c3228..c3221, inclusive of trailing blank
KEEP_TAIL = (100, len(q))  # NEW c3220b onward, untouched

EXPECT_CUT_START = "\n"  # line 30 is the blank separator before c3228
EXPECT_CUT_FIRST_HEAD = "- [ ] **CLOSED c3228 -- QUALITY/GROWTH slot"
EXPECT_CUT_LAST_BLANK = True  # line 99 is blank
EXPECT_TAIL_HEAD = "- [ ] **NEW c3220b (MEDIUM, fleet-wide)"

check(q[KEEP_HEAD[1] - 1].strip() != "", "line 29 unexpectedly blank")
check(q[CUT[0] - 1] == EXPECT_CUT_START, f"line 30 is not the expected blank separator: {q[CUT[0]-1]!r}")
check(q[CUT[0]].startswith(EXPECT_CUT_FIRST_HEAD), f"line 31 does not start the c3228 block: {q[CUT[0]][:80]!r}")
check(q[CUT[1] - 1].strip() == "", f"line 99 is not blank: {q[CUT[1]-1]!r}")
check(q[KEEP_TAIL[0] - 1].startswith(EXPECT_TAIL_HEAD), f"line 100 does not start NEW c3220b: {q[KEEP_TAIL[0]-1][:80]!r}")

keep_head = q[KEEP_HEAD[0] - 1:KEEP_HEAD[1]]
cut = q[CUT[0] - 1:CUT[1]]
keep_tail = q[KEEP_TAIL[0] - 1:KEEP_TAIL[1]]

# multiset/total identity: every original line is in exactly one of the three parts
check(keep_head + cut + keep_tail == q, "keep_head+cut+keep_tail does not reconstruct the original file exactly")

# the 7 oldest heads must all be present in `cut`, and the 4 newest must NOT be
OLD_HEADS = CYCLE_REPORT_HEADS[4:]   # c3228..c3221
NEW_HEADS = CYCLE_REPORT_HEADS[:4]   # c3234..c3231
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
