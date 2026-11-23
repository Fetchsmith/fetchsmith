#!/root/agent/venv/bin/python
"""_trim3621q.py -- cycle 3621 QUALITY-slot trim of tasks/queue.md.
RULE 6b floor-5 rotation: 8 contiguous CLOSED blocks live (c3620..c3613),
keep newest 5 (c3620, c3619, c3618, c3617, c3616), rotate oldest 3
(c3615, c3614, c3613), lines 31-48 (18 lines), to tasks/queue_archive.md.
Same assert-exact-boundary-strings-before-write pattern as _trim3618q.py.
"""
import sys

QPATH = "tasks/queue.md"
APATH = "tasks/queue_archive.md"

with open(QPATH) as f:
    lines = f.readlines()

assert len(lines) == 987, f"expected 987 lines, got {len(lines)}"
assert lines[30].startswith("- [x] **CLOSED c3615"), lines[30][:60]
assert lines[47] == "\n", repr(lines[47])
assert lines[48].startswith("- [ ] **NEW c3620"), lines[48][:60]

span = lines[30:48]  # lines 31-48, 0-indexed 30:48
assert span[0].startswith("- [x] **CLOSED c3615")
assert span[-1] == "\n"

# multiset of non-blank lines for lossless check
pre_nonblank = [l for l in span if l.strip()]
assert len(pre_nonblank) == 12, len(pre_nonblank)  # 3 blocks x (CLOSED + Next-BUILD + Next-QUALITY + ---)

new_lines = lines[:30] + lines[48:]
assert len(new_lines) == 987 - 18

header = "\n## Archived by cycle 3621 (QUALITY slot, rotated oldest 3 of 8 contiguous CLOSED blocks per RULE 6b floor-5: c3615, c3614, c3613)\n\n"

with open(APATH, "a") as f:
    f.write(header)
    f.writelines(span)

with open(QPATH, "w") as f:
    f.writelines(new_lines)

# lossless verify: every non-blank line of span findable verbatim in archive
with open(APATH) as f:
    arch_content = f.read()
missing = [l for l in pre_nonblank if l.rstrip("\n") not in arch_content]
assert not missing, f"MISSING {len(missing)} lines from archive!"

with open(QPATH) as f:
    verify_lines = f.readlines()
assert len(verify_lines) == 987 - 18
assert verify_lines[30].startswith("- [ ] **NEW c3620")

print("OK: rotated 18 lines (c3615, c3614, c3613) -> archive; queue.md now", len(verify_lines), "lines")
