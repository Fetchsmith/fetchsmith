import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'

with open(QUEUE) as f:
    lines = f.readlines()

# 0-indexed slice [24:39] == 1-indexed lines 25-39:
# CLOSED c3531 block (25-30) + blank (31) + CLOSED c3530 (32-34) + blank (35)
# + CLOSED c3529 (36-38) + blank (39). NEW c3523 (an OPEN item, line 40) is NOT cut.
START, END = 24, 39
cut = lines[START:END]

assert cut[0].startswith('- [x] **CLOSED c3531'), cut[0][:60]
assert cut[6] == '\n', repr(cut[6])
assert cut[7].startswith('- [x] **CLOSED c3530'), cut[7][:60]
assert cut[10] == '\n', repr(cut[10])
assert cut[11].startswith('- [x] **CLOSED c3529'), cut[11][:60]
assert cut[14] == '\n', repr(cut[14])
# line after the cut must be the next live item (NEW c3523), untouched
assert lines[END].startswith('- [ ] **NEW c3523'), lines[END][:60]
# line before the cut must be the blank line after CLOSED c3532
assert lines[START - 1] == '\n', repr(lines[START - 1])

new_lines = lines[:START] + lines[END:]

header = ("\n## Archived by cycle 3537 (from tasks/queue.md: the 3 oldest cycle-report "
    "blocks under the STANDING RULE 6b newest-5 floor -- c3531, c3530, c3529, newest-first; "
    "rotation-only lever, QUALITY slot.)\n\n")

archive_addition = header + ''.join(cut)

with open(ARCHIVE) as f:
    arch_text = f.read()
new_arch_text = arch_text.rstrip('\n') + '\n' + archive_addition

# lossless check: every non-blank cut line must appear verbatim in the archive addition
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
