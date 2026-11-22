"""c3591 queue.md trim -- rotation lever, 2 report blocks (c3585, c3584).

Cloned from bin/_trim3588q.py (KEPT on disk per the `NEW c3516` rule: never rm a
_trim*.py, the next trim clones the most recent one).

Fresh census at c3591: 7 live `CLOSED cNNNN` report blocks (c3590..c3584) -- MORE
than the 5-block floor the c3588/c3589/c3590 handoffs assumed ("spent to its floor"),
because two new blocks (c3589, c3590) landed since c3588 without any corresponding
archive. RULE 6b floor is "keep the newest 5" (c3590, c3589, c3588, c3587, c3586),
so c3585 and c3584 (each a 3-line block + its own blank/---/blank separator) are
rotatable this cycle.

Build the archive text as a STRING and assert against it BEFORE opening any file
for writing (the `NEW c3492` lesson).
"""
import sys

QPATH = "tasks/queue.md"
APATH = "tasks/queue_archive.md"
CYCLE = 3591

with open(QPATH) as f:
    text = f.read()
lines = text.split('\n')

# 0-indexed. lines[30:42] = CLOSED c3585 block (3 lines) + its blank/---/blank
# separator, then CLOSED c3584 block (3 lines) + its blank/---/blank separator.
assert lines[24].startswith('- [x] **CLOSED c3586'), lines[24][:60]
assert lines[27] == '' and lines[28] == '---' and lines[29] == ''

assert lines[30].startswith('- [x] **CLOSED c3585'), lines[30][:60]
assert lines[31].lstrip().startswith('- **Next (BUILD slot)'), lines[31][:60]
assert lines[32].lstrip().startswith('- **Next (QUALITY slot'), lines[32][:60]
assert lines[33:36] == ['', '---', ''], lines[33:36]

assert lines[36].startswith('- [x] **CLOSED c3584'), lines[36][:60]
assert lines[37].lstrip().startswith('- **Next (BUILD slot)'), lines[37][:60]
assert lines[38].lstrip().startswith('- **Next (QUALITY slot'), lines[38][:60]
assert lines[39:42] == ['', '---', ''], lines[39:42]

assert lines[42].startswith('- [ ] **NEW c3581'), lines[42][:60]

# archive content lines only (never the blank/--- separators), newest-first
cut_content = [lines[30], lines[31], lines[32],
               lines[36], lines[37], lines[38]]
cut_text = '\n\n'.join(cut_content)
print("CUT content bytes:", len(cut_text.encode()))
for c in cut_content:
    print("  cut:", c.lstrip()[:70])

orig_nonblank = [l for l in lines if l.strip() != '']

new_lines = lines[:30] + lines[42:]
new_text = '\n'.join(new_lines)

# seam: the kept c3586 block's `---` separator must be immediately followed by the
# first surviving live item, `NEW c3581`.
nl = new_text.split('\n')
assert nl[28] == '---', nl[28]
assert nl[29] == '', repr(nl[29])
assert nl[30].startswith('- [ ] **NEW c3581'), nl[30][:60]
assert 'CLOSED c3585' not in new_text and 'CLOSED c3584' not in new_text

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
