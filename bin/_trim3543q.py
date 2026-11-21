import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'

with open(QUEUE) as f:
    lines = f.readlines()

# Two cut spans (0-indexed), with an open item (NEW c3536 + blank) sitting
# between them that must stay live:
#   AB span: lines 26-36 (1-indexed) = CLOSED c3537 block (26-31) + blank (32)
#            + CLOSED c3536 block (33-35) + blank (36)
#   [KEPT: lines 37-38 = NEW c3536 (open) + blank]
#   C span:  lines 39-44 (1-indexed) = CLOSED c3535 block (39-43) + blank (44)
#   [KEPT: line 45 = NEW c3523 (open), line 46 blank]
AB_START, AB_END = 25, 36
C_START, C_END = 38, 44

cut_ab = lines[AB_START:AB_END]
cut_c = lines[C_START:C_END]

assert lines[24] == '\n', repr(lines[24])
assert cut_ab[0].startswith('- [x] **CLOSED c3537'), cut_ab[0][:60]
assert cut_ab[6] == '\n', repr(cut_ab[6])
assert cut_ab[7].startswith('- [x] **CLOSED c3536'), cut_ab[7][:60]
assert cut_ab[-1] == '\n', repr(cut_ab[-1])
assert lines[AB_END].startswith('- [ ] **NEW c3536'), lines[AB_END][:60]
assert lines[AB_END + 1] == '\n', repr(lines[AB_END + 1])
assert lines[C_START].startswith('- [x] **CLOSED c3535'), lines[C_START][:60]
assert cut_c[-1] == '\n', repr(cut_c[-1])
assert lines[C_END].startswith('- [ ] **NEW c3523'), lines[C_END][:60]

new_lines = lines[:AB_START] + lines[AB_END:C_START] + lines[C_END:]

header = ("\n## Archived by cycle 3543 (from tasks/queue.md: the 3 oldest cycle-report "
    "blocks under the STANDING RULE 6b newest-5 floor -- c3537, c3536, c3535, newest-first; "
    "rotation-only lever, QUALITY slot. Two non-contiguous spans cut because the open items "
    "`NEW c3536` and `NEW c3523` sit between the closed blocks and were left live in place.)\n\n")

archive_addition = header + ''.join(cut_ab) + ''.join(cut_c)

with open(ARCHIVE) as f:
    arch_text = f.read()
new_arch_text = arch_text.rstrip('\n') + '\n' + archive_addition

missing = [l for l in (cut_ab + cut_c) if l.strip() and l not in archive_addition]
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
