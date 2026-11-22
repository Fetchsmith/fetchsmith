"""c3588 queue.md trim -- rotation lever, 4 report blocks (c3583, c3582, c3581, c3580).

Cloned from bin/_trim3585q.py (KEPT on disk per the `NEW c3516` rule: never rm a
_trim*.py, the next trim clones the most recent one).

Fresh census at c3588: 8 live `CLOSED cNNNN` report blocks (c3587..c3580). RULE 6b
floor is "keep the newest 5" and this cycle's own c3588 block lands at the top, so
4 are rotatable: c3583, c3582 (each a 3-line block + blank/---/blank separator) and
c3581, c3580 (each a bare 1-line block + one trailing blank -- they are NOT part of
the separated prefix because live `NEW cNNNN` items grew in between them, the exact
"report blocks are not a chronological prefix" hazard the PLAYBOOK names).

Build the archive text as a STRING and assert against it BEFORE opening any file
for writing (the `NEW c3492` lesson -- c3492's script wrote first and could not be
retried when its own check failed).
"""
import sys

QPATH = "tasks/queue.md"
APATH = "tasks/queue_archive.md"
CYCLE = 3588

with open(QPATH) as f:
    text = f.read()
lines = text.split('\n')

# 0-indexed cut ranges, highest first so earlier slices keep their indices.
# idx 24:36 -> c3583 block (3 lines) + blank/---/blank, then c3582 block (3 lines)
#              + blank/---/blank. Contiguous, so one slice.
# idx 36:38 -> c3581 bare block + its single trailing blank.
# idx 40:42 -> c3580 bare block + its single trailing blank.
assert lines[18].startswith('- [x] **CLOSED c3584'), lines[18][:60]
assert lines[22] == '---' and lines[21] == '' and lines[23] == ''

assert lines[24].startswith('- [x] **CLOSED c3583'), lines[24][:60]
assert lines[25].lstrip().startswith('- **Next (BUILD slot)'), lines[25][:60]
assert lines[26].lstrip().startswith('- **Next (QUALITY slot'), lines[26][:60]
assert lines[27:30] == ['', '---', ''], lines[27:30]

assert lines[30].startswith('- [x] **CLOSED c3582'), lines[30][:60]
assert lines[31].lstrip().startswith('- **Next (BUILD slot)'), lines[31][:60]
assert lines[32].lstrip().startswith('- **Next (QUALITY slot'), lines[32][:60]
assert lines[33:36] == ['', '---', ''], lines[33:36]

assert lines[36].startswith('- [x] **CLOSED c3581'), lines[36][:60]
assert lines[37] == ''
assert lines[38].startswith('- [ ] **NEW c3581'), lines[38][:60]
assert lines[39] == ''
assert lines[40].startswith('- [x] **CLOSED c3580'), lines[40][:60]
assert lines[41] == ''
assert lines[42].startswith('- [ ] **NEW c3580'), lines[42][:60]

# archive content lines only (never the blank/--- separators), newest-first
cut_content = [lines[24], lines[25], lines[26],
               lines[30], lines[31], lines[32],
               lines[36],
               lines[40]]
cut_text = '\n\n'.join(cut_content)
print("CUT content bytes:", len(cut_text.encode()))
for c in cut_content:
    print("  cut:", c.lstrip()[:70])

orig_nonblank = [l for l in lines if l.strip() != '']

new_lines = lines[:24] + lines[36:36] + lines[38:40] + lines[42:]
# (lines[36:36] is empty; written out so the three cut ranges read explicitly)
new_text = '\n'.join(new_lines)

# seam: the kept c3584 block's `---` separator must be immediately followed by the
# first surviving live item, `NEW c3581`.
nl = new_text.split('\n')
assert nl[22] == '---', nl[22]
assert nl[23] == '', repr(nl[23])
assert nl[24].startswith('- [ ] **NEW c3581'), nl[24][:60]
assert nl[25] == '', repr(nl[25])
assert nl[26].startswith('- [ ] **NEW c3580'), nl[26][:60]
assert 'CLOSED c3583' not in new_text and 'CLOSED c3582' not in new_text
assert 'CLOSED c3581' not in new_text and 'CLOSED c3580' not in new_text

with open(APATH) as f:
    arch_text = f.read()
new_arch_text = arch_text + f"\n## Archived by cycle {CYCLE}\n\n" + cut_text + "\n"

# lossless check, by VALUE with multiplicity (the `NEW c3492` lesson: never use
# `is` to exempt a line -- compare values).
combined = {}
for l in (new_text + "\n" + new_arch_text).split('\n'):
    s = l.strip()
    if s:
        combined[s] = combined.get(s, 0) + 1

missing = 0
for l in orig_nonblank:
    s = l.strip()
    if combined.get(s, 0) <= 0:
        missing += 1
        print("MISSING:", s[:80])
    else:
        combined[s] -= 1

print("missing count:", missing)
print("orig nonblank lines:", len(orig_nonblank))
print("new queue.md size:", len(new_text.encode()), "was", len(text.encode()))
print("new queue.md lines:", len(nl), "was", len(lines))

if missing:
    print("ABORTED, missing lines found.")
    sys.exit(1)

with open(QPATH, 'w') as f:
    f.write(new_text)
with open(APATH, 'w') as f:
    f.write(new_arch_text)
print("WROTE both files.")
