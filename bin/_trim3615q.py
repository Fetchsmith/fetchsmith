import sys

QUEUE = "tasks/queue.md"
ARCHIVE = "tasks/queue_archive.md"

with open(QUEUE) as f:
    lines = f.readlines()

assert len(lines) == 985, f"expected 985 lines, got {len(lines)}"
assert lines[30].startswith("- [x] **CLOSED c3609"), "line 31 boundary mismatch"
assert lines[47] == "\n", "line 48 boundary mismatch"
assert lines[48].startswith("- [ ] **NEW c3589"), "line 49 boundary mismatch"

rotated = lines[30:48]  # c3609, c3608, c3607 blocks + their separators (0-indexed 30..47)
assert rotated[0].startswith("- [x] **CLOSED c3609")
assert rotated[-1] == "\n"

new_live = lines[:30] + lines[48:]

with open(ARCHIVE) as f:
    archive_content = f.read()

archive_addition = (
    "\n\n## Archived by cycle 3615 (QUALITY slot, rotated oldest 3 of 8 contiguous "
    "CLOSED blocks per RULE 6b floor-5: c3609, c3608, c3607)\n\n"
    + "".join(rotated)
)

new_archive = archive_content + archive_addition

# Lossless check: every non-blank line removed from queue.md must appear in the archive addition
removed_nonblank = [l for l in rotated if l.strip()]
for l in removed_nonblank:
    assert l in archive_addition, f"missing line in archive addition: {l[:60]!r}"

with open(QUEUE, "w") as f:
    f.writelines(new_live)

with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print("OK: queue.md", len(lines), "->", len(new_live), "lines")
