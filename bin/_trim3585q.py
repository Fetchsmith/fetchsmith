import sys

QPATH = "tasks/queue.md"
APATH = "tasks/queue_archive.md"
CYCLE = 3585

with open(QPATH) as f:
    text = f.read()
lines = text.split('\n')

# cut the oldest report block, c3579: lines 27-29 (1-indexed) plus its trailing
# blank/---/blank separator at 30-32 -> 0-indexed 26:32. The blank at line 26
# (0-indexed 25) that PRECEDES the block stays, so the c3580 bullet above remains
# separated from the `NEW c3568(c)` bullet that follows.
start0 = 26
end0 = 32
cut_lines = lines[start0:end0]
assert cut_lines[0].startswith('- [x] **CLOSED c3579'), cut_lines[0][:60]
assert cut_lines[1].lstrip().startswith('- **Next (BUILD slot)'), cut_lines[1][:60]
assert cut_lines[2].lstrip().startswith('- **Next (QUALITY slot'), cut_lines[2][:60]
assert cut_lines[3:] == ['', '---', ''], cut_lines[3:]
assert lines[32].startswith('- [ ] **NEW c3568(c)'), lines[32][:60]

cut_text = '\n'.join(cut_lines[:3])  # archive the 3 content lines, not the separator
print("CUT BLOCK bytes:", len(cut_text.encode()))
print("CUT BLOCK preview:", cut_text[:80])

orig_nonblank = [l for l in lines if l.strip() != '']

new_lines = lines[:start0] + lines[end0:]
new_text = '\n'.join(new_lines)

archive_block = f"\n## Archived by cycle {CYCLE}\n\n" + cut_text + "\n"
with open(APATH) as f:
    arch_text = f.read()
new_arch_text = arch_text + archive_block

# lossless check: every non-blank original line must still be findable, counting
# multiplicity, across live queue + archive.
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
print("new queue.md size:", len(new_text.encode()))

if missing == 0:
    with open(QPATH, 'w') as f:
        f.write(new_text)
    with open(APATH, 'w') as f:
        f.write(new_arch_text)
    print("WROTE both files.")
else:
    print("ABORTED, missing lines found.")
    sys.exit(1)
