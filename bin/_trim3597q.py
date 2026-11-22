"""c3597 queue.md trim -- rotation lever, 3 report blocks (c3590, c3589, c3588).

Cloned from bin/_trim3594q.py (KEPT on disk per the `NEW c3516` rule: never rm a
_trim*.py, the next trim clones the most recent one).

Fresh census at c3597: the top contiguous run of `- [x] **CLOSED cNNNN` report
blocks is c3596..c3588 (8 blocks; `CLOSED c3593` sits later in the file as a lone
paragraph among the NEW items, not part of this contiguous run, left alone).
Note c3596's own block (lines 1-2) has no trailing blank/---/blank separator
before c3595 -- an existing anomaly in the file, not something this trim
introduces or fixes; preserved verbatim.
RULE 6b floor is "keep the newest 5" (c3596, c3595, c3594, c3592, c3591), so
c3590, c3589 and c3588 (each a 3-line block + its own blank/---/blank separator)
are rotatable this cycle.

Build the archive text as a STRING and assert against it BEFORE opening any file
for writing (the `NEW c3492` lesson).
"""
import sys

QPATH = "tasks/queue.md"
APATH = "tasks/queue_archive.md"
CYCLE = 3597

with open(QPATH) as f:
    text = f.read()
lines = text.split('\n')

# 0-indexed: file line N is lines[N-1]
assert lines[20].startswith('- [x] **CLOSED c3591'), lines[20][:60]
assert lines[23:26] == ['', '---', ''], lines[23:26]

assert lines[26].startswith('- [x] **CLOSED c3590'), lines[26][:60]
assert lines[27].lstrip().startswith('- **Next (BUILD slot)'), lines[27][:60]
assert lines[28].lstrip().startswith('- **Next (QUALITY slot'), lines[28][:60]
assert lines[29:32] == ['', '---', ''], lines[29:32]

assert lines[32].startswith('- [x] **CLOSED c3589'), lines[32][:60]
assert lines[33].lstrip().startswith('- **Next (BUILD slot)'), lines[33][:60]
assert lines[34].lstrip().startswith('- **Next (QUALITY slot'), lines[34][:60]
assert lines[35:38] == ['', '---', ''], lines[35:38]

assert lines[38].startswith('- [x] **CLOSED c3588'), lines[38][:60]
assert lines[39].lstrip().startswith('- **Next (BUILD slot)'), lines[39][:60]
assert lines[40].lstrip().startswith('- **Next (QUALITY slot'), lines[40][:60]
assert lines[41:44] == ['', '---', ''], lines[41:44]

assert lines[44].startswith('- [ ] **NEW c3581'), lines[44][:60]

# archive content lines only (never the blank/--- separators), newest-first
cut_content = [lines[26], lines[27], lines[28],
               lines[32], lines[33], lines[34],
               lines[38], lines[39], lines[40]]
cut_text = '\n\n'.join(cut_content)
print("CUT content bytes:", len(cut_text.encode()))
for c in cut_content:
    print("  cut:", c.lstrip()[:70])

orig_nonblank = [l for l in lines if l.strip() != '']

new_lines = lines[:26] + lines[44:]
new_text = '\n'.join(new_lines)

# seam: the kept c3591 block's `---` separator must be immediately followed by
# the first surviving live item, `NEW c3581`.
nl = new_text.split('\n')
assert nl[24] == '---', nl[24]
assert nl[25] == '', repr(nl[25])
assert nl[26].startswith('- [ ] **NEW c3581'), nl[26][:60]
assert 'CLOSED c3590' not in new_text and 'CLOSED c3589' not in new_text and 'CLOSED c3588' not in new_text

with open(APATH) as f:
    arch_text = f.read()
new_arch_text = arch_text + f"\n## Archived by cycle {CYCLE}\n\n" + cut_text + "\n"

# lossless check, by VALUE with multiplicity.
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
