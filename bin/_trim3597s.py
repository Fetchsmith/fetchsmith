"""c3597 STATUS.md trim -- QUALITY-slot structural rotation, handed off since c3594.

Fresh census: 42 live `^Updated: ` cycle blocks. RULE (keep newest 9 existing
blocks so this cycle's own new prepended block lands the file at exactly 10,
same pattern as c3528/c3564) -- keep c3596..c3588 (9 blocks, lines 1-122),
archive c3587 downward (33 blocks, lines 123-511) to state/STATUS_ARCHIVE.md,
verbatim, newest-first (already the file's natural order).

Build the archive text as a STRING and assert against it BEFORE opening any
file for writing (the `NEW c3492` lesson).
"""
import sys

SPATH = "state/STATUS.md"
APATH = "state/STATUS_ARCHIVE.md"
CYCLE = 3597

with open(SPATH) as f:
    text = f.read()
lines = text.split('\n')
assert len(lines) == 512, len(lines)

# 0-indexed: file line N is lines[N-1]
assert lines[102].startswith('Updated: 2026-11-22 UTC by cycle 3588'), lines[102][:70]
assert lines[117] == '', repr(lines[117])
assert lines[119] == '', repr(lines[119])
assert lines[120] == '---', repr(lines[120])
assert lines[121] == '', repr(lines[121])
assert lines[122].startswith('Updated: 2026-11-22 UTC by cycle 3587'), lines[122][:70]

keep = lines[:122]      # lines 1-122, ends on the blank after c3588's separator
cut = lines[122:]        # lines 123-511, c3587 downward through EOF

orig_nonblank = [l for l in lines if l.strip() != '']

new_text = '\n'.join(keep)
cut_text = '\n'.join(cut)

assert 'Updated: 2026-11-22 UTC by cycle 3587' in cut_text
assert 'Updated: 2026-11-22 UTC by cycle 3588' not in cut_text
assert new_text.rstrip('\n').endswith('---')

with open(APATH) as f:
    arch_text = f.read()

header = (f"\n## Archived by cycle {CYCLE} (from state/STATUS.md: the 33 oldest "
          f"cycle blocks, c3587 down to the file's prior tail, newest-first and "
          f"verbatim. RULE: count fresh off the anchored `^Updated: ` header, "
          f"42 live blocks against the keep-9 floor -- kept c3596..c3588 so this "
          f"cycle's own prepended block lands the file at exactly 10.)\n\n")
new_arch_text = arch_text + header + cut_text + "\n"

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
print("new STATUS.md size:", len(new_text.encode()), "was", len(text.encode()))
print("new STATUS.md lines:", len(keep), "was", len(lines))

if missing:
    print("ABORTED, missing lines found.")
    sys.exit(1)

with open(SPATH, 'w') as f:
    f.write(new_text)
with open(APATH, 'w') as f:
    f.write(new_arch_text)
print("WROTE both files.")
