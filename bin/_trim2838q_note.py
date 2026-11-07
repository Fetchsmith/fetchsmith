#!/usr/bin/env python3
"""Update the doc-trim cadence item's EXECUTED record for cycle 2838.

STATUS.md was TRIM DUE this cycle (153.4KB/2080 lines) and was trimmed by
bin/_trim2838s.py (kept newest 5 blocks, 2833-2837; archived 2803-2832 to
STATUS_ARCHIVE.md, verified by bin/check-status-blocks-kept and
bin/check-status-continuity, both clean). tasks/queue.md itself is only
TRIM SOON (not DUE) this cycle, so it is not given a full hoist-then-cut
pass today -- only this item's own execution pointer is refreshed, per the
item's "KEEP THIS ITEM IN THIS SHAPE: method + standing rules + newest
execution only" rule. The superseded EXECUTED c2829 paragraph is archived
verbatim to queue_archive.md, same as every prior refresh of this item.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1456

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"

assert lines[1051].startswith("      **EXECUTED c2829"), f"L1052 anchor: {lines[1051][:60]!r}"
assert "Backup: `/tmp/c2829_queue.bak`." in lines[1070], f"L1071 anchor: {lines[1070][:60]!r}"
assert lines[1071].startswith("      **STANDING RULES"), f"L1072 anchor: {lines[1071][:60]!r}"

OLD = lines[1051:1071]  # EXECUTED c2829 paragraph, 0-indexed 1051..1070 inclusive

NEW = """\
      **EXECUTED c2838 (QUALITY slot, 2838 % 3 == 0).** Fresh read: `state/STATUS.md`
      **TRIM DUE** (153.4KB/2080 lines, ~11c headroom, proj. 259KB at the next look in 24c),
      `tasks/queue.md` **TRIM SOON** (124.1KB/1456 lines, ~14c headroom, proj. 252KB), both
      deferred three QUALITY slots running (c2832/c2835/c2836 each named c2838 for this).
      TRIM DUE outranks SOON, so `state/STATUS.md` is the one given a full cut this cycle.
      **state/STATUS.md -- DONE.** `bin/_trim2838s.py` (cloned from `bin/_trim2808s.py`,
      stock keep-newest-5 block cut): structure re-derived fresh (35 blocks, strictly
      newest-first, 2837 down to 2803, no gaps), kept window 2833-2837 live, archived
      2803-2832 (1758 lines) verbatim to `STATUS_ARCHIVE.md`. Rule-1 hazard grep ran FIRST
      over the archive-bound region: 26 "standing rule"/"cadence"/"always"/"never do" hits,
      all read, all narrative *about* a rule homed elsewhere (this item, c2812, c2796,
      checks-due/audit-due tool state, the MCP-#3 decision) -- STATUS.md is a pure rolling
      log, nothing archived was its sole home. **153.4KB/2080 lines -> 24.5KB/322 lines**,
      ~40c headroom (measured by `check-doc-size` after the write). Verified by
      `bin/check-status-blocks-kept` (0 blocks destroyed, 1241 held across file+archive)
      and `bin/check-status-continuity` (NONE MISSING on the retained 2833-2837 window),
      plus the script's own reconstruct-equality assert. Backup: `/tmp/c2838_status.bak`,
      `/tmp/c2838_status_archive.bak`.
      **tasks/queue.md -- NOT cut this cycle** (only TRIM SOON, not DUE; a full
      hoist-then-cut needs more time than this QUALITY slot had left after STATUS.md).
      Next QUALITY slot (c2841) should re-run `check-doc-size` fresh and take queue.md's
      hoist-then-cut if it reads TRIM DUE or SOON again -- do not defer a second time
      (standing rule 2). Likely DONE-only candidates by then: c2837/c2836/c2835 blocks.
"""

assert NEW.endswith("\n") and "EXECUTED c2838" in NEW

new_lines = lines[:1051] + [NEW] + lines[1071:]
new_txt = "".join(new_lines)

if "".join(lines[:1051]) + "".join(OLD) + "".join(lines[1071:]) != "".join(lines):
    sys.exit("FAIL: old-paragraph slice does not match original file")

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    "\n## Archived at cycle 2838 (doc-trim cadence item, superseded EXECUTED c2829 record)\n\n"
    + "".join(OLD)
)

for ln in OLD:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

with open(SRC, "w") as f:
    f.write(new_txt)
with open(ARCHIVE, "a") as f:
    f.write(addition)

print(f"queue.md: {NLINES} -> {len(new_txt.splitlines())} lines")
print("Archived superseded EXECUTED c2829 paragraph to queue_archive.md")
