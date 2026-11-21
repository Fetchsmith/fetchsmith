import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'

with open(QUEUE) as f:
    lines = f.readlines()

# Rotation lever (QUALITY slot c3546): archive the oldest 3 of the 8 report-shaped
# `CLOSED c3NNN` headers (c3545, c3544, c3543, c3542, c3541, c3540, c3539, c3538),
# keeping the newest 5 (c3545..c3541) at the standing RULE 6b floor.
# Cut span (0-indexed slice [31:46] = 1-indexed lines 32-46): CLOSED c3540 block,
# CLOSED c3539 block, CLOSED c3538 block, each with its trailing blank+---+blank,
# ending on the blank line right before `NEW c3536` so the kept file reads
# "---" blank "NEW c3536" with no doubled blank.
START, END = 31, 46

cut = lines[START:END]

assert lines[START - 1] == '\n', repr(lines[START - 1])
assert lines[START - 2] == '---\n', repr(lines[START - 2])
assert cut[0].startswith('- [x] **CLOSED c3540'), cut[0][:60]
assert cut[5].startswith('- [x] **CLOSED c3539'), cut[5][:60]
assert cut[10].startswith('- [x] **CLOSED c3538'), cut[10][:60]
assert cut[-1] == '\n', repr(cut[-1])
assert lines[END].startswith('- [ ] **NEW c3536'), lines[END][:60]

new_lines = lines[:START] + lines[END:]

header = ("\n## Archived by cycle 3546 (from tasks/queue.md: the 3 oldest cycle-report "
    "blocks under the STANDING RULE 6b newest-5 floor -- c3540, c3539, c3538, newest-first; "
    "rotation-only lever, QUALITY slot.)\n\n")

archive_addition = header + ''.join(cut)

with open(ARCHIVE) as f:
    arch_text = f.read()
new_arch_text = arch_text.rstrip('\n') + '\n' + archive_addition

missing = [l for l in cut if l.strip() and l not in archive_addition]
assert not missing, f"LOSSY: {len(missing)} missing"

if '--write' not in sys.argv:
    print("DRY RUN OK")
    print(f"queue.md: {len(lines)} -> {len(new_lines)} lines (-{len(lines)-len(new_lines)})")
    print(f"archive: +{len(archive_addition.splitlines())} lines")
    sys.exit(0)

with open(QUEUE, 'w') as f:
    f.writelines(new_lines)
with open(ARCHIVE, 'w') as f:
    f.write(new_arch_text)
print("WRITE DONE")
