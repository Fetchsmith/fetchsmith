import sys, re

QPATH = "tasks/queue.md"
APATH = "tasks/queue_archive.md"
CYCLE = 3582

with open(QPATH) as f:
    text = f.read()
lines = text.split('\n')

# cut c3576 report block: lines 27-31 (1-indexed) per census -> 0-indexed 26:31
start0 = 26  # 0-indexed start of line 27
end0 = 31    # 0-indexed end-exclusive (line 31 inclusive -> index 30, plus blank at 31)
cut_lines = lines[start0:end0]
assert cut_lines[0].startswith('- [x] **CLOSED c3576'), cut_lines[0][:60]

# verify next line after cut is the NEW c3568(c) bullet (line 32, index 31)
assert lines[31].startswith("- [ ] **NEW c3568(c)"), lines[31][:60]

cut_text = '\n'.join(cut_lines)
print("CUT BLOCK bytes:", len(cut_text.encode()))
print("CUT BLOCK preview:", cut_text[:80])

# lossless pre-check: multiset of non-blank lines
orig_nonblank = [l for l in lines if l.strip() != '']

new_lines = lines[:start0] + lines[end0:]
new_text = '\n'.join(new_lines)

archive_header = f"\n## Archived by cycle {CYCLE}\n\n"
archive_block = archive_header + cut_text + "\n"

with open(APATH) as f:
    arch_text = f.read()
new_arch_text = arch_text + archive_block

# verify lossless: every non-blank line of orig must be findable in new_text+new_arch_text
combined = new_text + "\n" + new_arch_text
combined_lines_set = {}
for l in combined.split('\n'):
    s = l.strip()
    if s == '':
        continue
    combined_lines_set[s] = combined_lines_set.get(s, 0) + 1

missing = 0
for l in orig_nonblank:
    s = l.strip()
    if combined_lines_set.get(s, 0) <= 0:
        missing += 1
        print("MISSING:", s[:80])
    else:
        combined_lines_set[s] -= 1

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
