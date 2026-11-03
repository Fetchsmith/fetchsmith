#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2652 (132.3KB / 1712 lines, TRIM SOON).

check-doc-size read TRIM SOON on BOTH live docs at this cycle's preflight
(STATUS.md 132.3KB/1712 lines, ~15 cycles of headroom at +4510 B/cycle,
proj. 238KB at the checker's next automatic look) and repeated its standing
guidance: "trim proactively in a QUALITY slot rather than waiting for the
escalation (cycle 2220 follow-up)". Cycle 2652 IS a QUALITY/GROWTH slot
(2652 % 3 == 0) and c2650 named it as the natural trim point, so this is it.

Standing-hazard grep run FIRST (before this script), on all 1389
archive-bound lines -- 41 keyword hits, all narrative or with a verified live
home outside the archived range:
  - "do not re-hash vid at /24 on this one observation" -> live OPEN queue
    item (c2644, tasks/queue.md).
  - "PLAYBOOK's falsified-hypothesis box" / "never build into a low-demand
    niche" -> notes/PLAYBOOK.md.
  - "do not evict 'European Tenders' from the title" -> independently stored
    in state/audit_dates.json (eu-ted-tenders-scraper/title_trade_note).
  - CL_API_TOKEN "do not re-attempt until a token exists" -> same file
    (input_error_advice_note), plus the resolved owner thread.
  - "never round-trip a state JSON through json.dump" -> notes/LEARNINGS.md.
  - "run `learnings -c <cycle>` right after appending, a grep-based index
    fails silently" -> notes/LEARNINGS.md:7034.
  - "do not trim in a NORMAL slot" -> the live doc-trim cadence queue item
    and check-doc-size's own output.
CLEAN -- nothing needed rehoming.

Same stock method as 1836/.../2605/2628: keep the newest N cycle blocks
live, append the remainder VERBATIM to state/STATUS_ARCHIVE.md under a
dated header, source order preserved. No open items are interleaved here,
so a block-boundary cut is safe; every block must still land in the
archive -- bin/check-status-blocks-kept (pre-commit) checks this.

Structure at 2652: 29 blocks, strictly newest-first, 2651 down to 2623, no
gaps. KEEP_BLOCKS = 5 -> the contiguous window 2647..2651 stays live;
cycles <=2646 are archived. The cut lands on the 2646 header (line 324) and
line 323 is blank, so the boundary is clean. Run BEFORE this cycle's own
block is prepended.
"""
import re
import sys

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
KEEP_BLOCKS = 5

HEADER_RE = re.compile(r"^Updated:.*?by cycle (\d+)|^PRIOR \(cycle (\d+)")


def header_cycle(line):
    m = HEADER_RE.match(line)
    return int(m.group(1) or m.group(2)) if m else None


with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1712, f"expected 1712 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 29, f"expected 29 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2651, 2622, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
assert cut == 323, f"expected the cut at 0-based line 323 (the 2646 header), got {cut}"
assert lines[cut - 1].strip() == "", "line before the cut is not blank -- boundary unclean"

keep = lines[:cut]
archived = lines[cut:]

keep_txt = "".join(keep)

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    f"\n## Archived at cycle 2652 (STATUS.md trim, `bin/_trim2652.py`) -- "
    f"cycles 2623-2646\n\n" + "".join(archived)
)
new_archive = old_archive + addition

for ln in archived:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

if "".join(keep) + "".join(archived) != "".join(lines):
    sys.exit("FAIL: kept + archived does not reconstruct the original file")

with open(SRC, "w") as f:
    f.write(keep_txt)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"STATUS.md: {len(lines)} -> {len(keep_txt.splitlines())} lines "
      f"({len(''.join(lines))} -> {len(keep_txt)} bytes)")
print(f"Archived {len(archived)} lines to {ARCHIVE}")
