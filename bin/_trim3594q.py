"""c3594 queue.md trim -- rotation lever, 2 report blocks (c3587, c3586).

Cloned from bin/_trim3591q.py (KEPT on disk per the `NEW c3516` rule: never rm a
_trim*.py, the next trim clones the most recent one).

Fresh census at c3594: the top contiguous run of `- [x] **CLOSED cNNNN` report
blocks is c3592..c3586 (7 blocks; `CLOSED c3593` sits later in the file as a lone
paragraph among the NEW items, not part of this contiguous run, and is left alone).
RULE 6b floor is "keep the newest 5" (c3592, c3591, c3590, c3589, c3588), so c3587
and c3586 (each a 3-line block + its own blank/---/blank separator) are rotatable
this cycle.

Build the archive text as a STRING and assert against it BEFORE opening any file
for writing (the `NEW c3492` lesson).
"""
import sys

QPATH = "tasks/queue.md"
APATH = "tasks/queue_archive.md"
CYCLE = 3594

with open(QPATH) as f:
    text = f.read()
lines = text.split('\n')

assert lines[24].startswith('- [x] **CLOSED c3588'), lines[24][:60]
assert lines[27] == '' and lines[28] == '---' and lines[29] == ''

assert lines[30].startswith('- [x] **CLOSED c3587'), lines[30][:60]
assert lines[31].lstrip().startswith('- **Next (BUILD slot)'), lines[31][:60]
assert lines[32].lstrip().startswith('- **Next (QUALITY slot'), lines[32][:60]
assert lines[33:36] == ['', '---', ''], lines[33:36]

assert lines[36].startswith('- [x] **CLOSED c3586'), lines[36][:60]
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

# seam: the kept c3588 block's `---` separator must be immediately followed by the
# first surviving live item, `NEW c3581`.
nl = new_text.split('\n')
assert nl[28] == '---', nl[28]
assert nl[29] == '', repr(nl[29])
assert nl[30].startswith('- [ ] **NEW c3581'), nl[30][:60]
assert 'CLOSED c3587' not in new_text and 'CLOSED c3586' not in new_text

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
