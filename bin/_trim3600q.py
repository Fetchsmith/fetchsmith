"""c3600 queue.md trim -- rotation lever, 3 report blocks (c3594, c3592, c3591).

Cloned from bin/_trim3597q.py (KEPT on disk per the `NEW c3516` rule: never rm a
_trim*.py, the next trim clones the most recent one).

Fresh census at c3600 (STANDING RULE 3 -- re-derived from the live file, no line
numbers pasted forward): the top contiguous run of `- [x] **CLOSED cNNNN` report
blocks is c3599, c3598, c3597, c3596, c3595, c3594, c3592, c3591 (8 blocks).
`CLOSED c3593` again sits later in the file as a lone paragraph among the NEW
items, not part of this contiguous run -- left alone.
Note c3596's own block has no trailing blank/---/blank separator before c3595 --
a pre-existing anomaly first recorded at c3597, not introduced or fixed here;
preserved verbatim.
RULE 6b floor is "keep the newest 5" (c3599, c3598, c3597, c3596, c3595), so
c3594, c3592 and c3591 (each a 3-line block + its own blank/---/blank separator)
are rotatable this cycle. Same line-index shape as _trim3597q.py.

STANDING RULE 1 (grep FIRST, then cut) was done before writing this: `c3594`,
`c3592`, `c3591` each appear in the surviving file only as historical narrative
inside other cycles' own blocks, never as a positional pointer into cut content.

Build the archive text as a STRING and assert against it BEFORE opening any file
for writing (the `NEW c3492` lesson).
"""
import sys

QPATH = "tasks/queue.md"
APATH = "tasks/queue_archive.md"
CYCLE = 3600

with open(QPATH) as f:
    text = f.read()
lines = text.split('\n')

# 0-indexed: file line N is lines[N-1]
assert lines[20].startswith('- [x] **CLOSED c3595'), lines[20][:60]
assert lines[23:26] == ['', '---', ''], lines[23:26]

assert lines[26].startswith('- [x] **CLOSED c3594'), lines[26][:60]
assert lines[27].lstrip().startswith('- **Next (BUILD slot)'), lines[27][:60]
assert lines[28].lstrip().startswith('- **Next (QUALITY slot'), lines[28][:60]
assert lines[29:32] == ['', '---', ''], lines[29:32]

assert lines[32].startswith('- [x] **CLOSED c3592'), lines[32][:60]
assert lines[33].lstrip().startswith('- **Next (BUILD slot)'), lines[33][:60]
assert lines[34].lstrip().startswith('- **Next (QUALITY slot'), lines[34][:60]
assert lines[35:38] == ['', '---', ''], lines[35:38]

assert lines[38].startswith('- [x] **CLOSED c3591'), lines[38][:60]
assert lines[39].lstrip().startswith('- **Next (BUILD slot)'), lines[39][:60]
assert lines[40].lstrip().startswith('- **Next (QUALITY slot'), lines[40][:60]
assert lines[41:44] == ['', '---', ''], lines[41:44]

assert lines[44].startswith('- [ ] **NEW c3598'), lines[44][:60]

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

# seam: the kept c3595 block's `---` separator must be immediately followed by
# the first surviving live item, `NEW c3598`.
nl = new_text.split('\n')
assert nl[24] == '---', nl[24]
assert nl[25] == '', repr(nl[25])
assert nl[26].startswith('- [ ] **NEW c3598'), nl[26][:60]
assert 'CLOSED c3594' not in new_text and 'CLOSED c3592' not in new_text and 'CLOSED c3591' not in new_text

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
