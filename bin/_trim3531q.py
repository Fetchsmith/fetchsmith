import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'

with open(QUEUE) as f:
    lines = f.readlines()

# 0-indexed slice [21:25] == 1-indexed lines 22-25: CLOSED c3525 block (22-23) + CLOSED c3524 block (24-25)
START, END = 21, 25
cut = lines[START:END]

assert cut[0].startswith('- [x] **CLOSED c3525'), cut[0][:60]
assert cut[1] == '\n', repr(cut[1])
assert cut[2].startswith('- [x] **CLOSED c3524'), cut[2][:60]
assert cut[3] == '\n', repr(cut[3])
# line after the cut must be the next live item (NEW c3523), untouched
assert lines[END].startswith('- [ ] **NEW c3523'), lines[END][:60]
# line before the cut must be the blank line after CLOSED c3526
assert lines[START-1] == '\n', repr(lines[START-1])

new_lines = lines[:START] + lines[END:]

header = ("\n## Archived by cycle 3531 (from tasks/queue.md: the 2 oldest cycle-report "
    "blocks under the STANDING RULE 6b newest-5 floor -- c3525, c3524, newest-first; "
    "rotation-only lever, re-derived fresh. The RELOCATION lever was also spent this "
    "cycle, separately: `MERGED c2916` moved to `notes/PLAYBOOK.md`, see that file's "
    "`## Handle-liveness disclosure method` section.)\n\n")

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
