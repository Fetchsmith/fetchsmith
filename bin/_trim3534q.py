import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'

with open(QUEUE) as f:
    lines = f.readlines()

# 0-indexed slice [21:34] == 1-indexed lines 22-34:
# CLOSED c3528 block (22-28) + 2 blanks (29-30) + CLOSED c3527 (31) + blank (32)
# + CLOSED c3526 (33) + blank (34). NEW c3523 (an OPEN item, line 35) is NOT cut.
START, END = 21, 34
cut = lines[START:END]

assert cut[0].startswith('- [x] **CLOSED c3528'), cut[0][:60]
assert cut[7] == '\n', repr(cut[7])
assert cut[8] == '\n', repr(cut[8])
assert cut[9].startswith('- [x] **CLOSED c3527'), cut[9][:60]
assert cut[10] == '\n', repr(cut[10])
assert cut[11].startswith('- [x] **CLOSED c3526'), cut[11][:60]
assert cut[12] == '\n', repr(cut[12])
# line after the cut must be the next live item (NEW c3523), untouched
assert lines[END].startswith('- [ ] **NEW c3523'), lines[END][:60]
# line before the cut must be the blank line after CLOSED c3529
assert lines[START - 1] == '\n', repr(lines[START - 1])

new_lines = lines[:START] + lines[END:]

header = ("\n## Archived by cycle 3534 (from tasks/queue.md: the 3 oldest cycle-report "
    "blocks under the STANDING RULE 6b newest-5 floor -- c3528, c3527, c3526, newest-first; "
    "rotation-only lever. The RELOCATION lever's 3 named candidates (NEW c3046, "
    "COMPRESSED c2994, NEW STANDING TRIPWIRE c2336) were re-read in full this cycle and "
    "found to be live operational state/backlog, not reusable method -- NOT relocated; "
    "see tasks/queue.md's c3534 report block for the correction.)\n\n")

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
