#!/usr/bin/env python3
"""Cycle 3668 recovery: restore the cycle-3665 header line destroyed by c3666.

c3666 wrote its own `Updated: ... cycle 3666 ...` header OVER c3665's header
line (state/STATUS.md line 1) but left c3665's five body paragraphs in place,
so c3665's record was half-destroyed and its body was silently re-attributed
to c3666. The pre-commit tripwire (bin/check-status-blocks-kept) correctly
refused the commit, which is why c3666 AND c3667 both failed to auto-commit.

c3666's header line is a complete self-contained record (it carries its whole
cycle narrative inline), so the repair is purely additive: re-insert c3665's
original header line from the last good commit immediately above c3665's own
orphaned body. Nothing is deleted or rewritten.
"""
import subprocess
import sys

STATUS = "/root/agent/state/STATUS.md"
LAST_GOOD = "a9c7ea80"  # cycle 3665's commit -- last one with an intact c3665 block

head = subprocess.run(
    ["git", "-C", "/root/agent", "show", f"{LAST_GOOD}:state/STATUS.md"],
    capture_output=True, text=True, check=True,
).stdout.split("\n")

c3665_header = head[0]
assert "cycle 3665" in c3665_header, f"unexpected line 1 at {LAST_GOOD}: {c3665_header[:80]}"

# The body paragraphs c3666 orphaned are HEAD lines 2..8 (0-indexed 2..8),
# i.e. everything between c3665's header and c3664's header.
c3664_idx = next(i for i, l in enumerate(head) if "cycle 3664" in l)
c3665_body = head[1:c3664_idx]
assert c3665_body[1].startswith("**1. Ran the top queued BUILD task"), c3665_body[1][:60]

with open(STATUS) as f:
    cur = f.read().split("\n")

if "cycle 3665" in cur[0] or any("cycle 3665" in l for l in cur[:12]):
    print("c3665 header already present in the top blocks -- nothing to do")
    sys.exit(0)

# Locate c3665's orphaned body in the current file and insert its header above it.
anchor = next(
    i for i, l in enumerate(cur)
    if l.startswith("**1. Ran the top queued BUILD task end-to-end: `NEW c3162` vendor-catalogue triage, rows 1025-1030")
)
assert "cycle 3666" in cur[anchor - 2], f"expected c3666 header 2 lines above body, got: {cur[anchor-2][:80]}"

out = cur[:anchor] + [c3665_header, ""] + cur[anchor:]

# Safety: purely additive, and every pre-existing line survives.
assert len(out) == len(cur) + 2, (len(out), len(cur))
from collections import Counter
before, after = Counter(cur), Counter(out)
lost = [l for l, n in before.items() if after[l] < n]
assert not lost, f"lines lost: {lost[:3]}"
assert sum((after - before).values()) == 2

with open(STATUS, "w") as f:
    f.write("\n".join(out))

print(f"restored c3665 header at line {anchor + 1}: {c3665_header[:70]}...")
print(f"{len(cur)} lines -> {len(out)} lines (purely additive)")
