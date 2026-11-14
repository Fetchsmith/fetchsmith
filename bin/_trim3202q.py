#!/usr/bin/env python3
"""One-off cycle-3202 queue.md rotation: keep newest 5 CLOSED blocks live, archive the rest verbatim.
Same shape as _trim3193q.py/_trim3196q.py. Dry-run by default; --write to apply."""
import re
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
FLOOR = 5

with open(QUEUE) as f:
    text = f.read()
lines = text.split('\n')

starts = [i for i, l in enumerate(lines) if l.startswith('- [ ] **CLOSED') or l.startswith('- [ ] **NEW')]
starts.append(len(lines))

chunks = []
for idx in range(len(starts) - 1):
    s, e = starts[idx], starts[idx + 1]
    chunk_lines = lines[s:e]
    kind = 'CLOSED' if chunk_lines[0].startswith('- [ ] **CLOSED') else 'NEW'
    m = re.search(r'CLOSED c(\d+)', chunk_lines[0])
    cyc = int(m.group(1)) if m else None
    chunks.append({'kind': kind, 'cyc': cyc, 'lines': chunk_lines})

closed_idx = [i for i, c in enumerate(chunks) if c['kind'] == 'CLOSED']
assert len(closed_idx) == 11, f"expected 11 CLOSED blocks, found {len(closed_idx)}"

keep_closed = set(closed_idx[:FLOOR])        # newest 5 (file is newest-first)
archive_closed = closed_idx[FLOOR:]          # oldest 6, to archive, in file order (newest-of-the-old first)

archived_cycles = [chunks[i]['cyc'] for i in archive_closed]
print("Archiving cycles:", archived_cycles)

new_live_lines = []
archived_text_lines = []
for i, c in enumerate(chunks):
    if c['kind'] == 'CLOSED' and i in archive_closed:
        archived_text_lines.extend(c['lines'])
    else:
        new_live_lines.extend(c['lines'])

new_live_text = '\n'.join(new_live_lines)
archived_text = '\n'.join(archived_text_lines)

# losslessness check: every non-blank original line must appear in (live+archive) combined, same multiset
orig_nonblank = [l for l in lines if l.strip()]
combined = new_live_lines + archived_text_lines
combined_nonblank = [l for l in combined if l.strip()]
assert sorted(orig_nonblank) == sorted(combined_nonblank), "LOSSY: line multiset mismatch"
print(f"Lossless check OK: {len(orig_nonblank)} non-blank lines preserved across live+archive")

if '--write' in sys.argv:
    cycle_label = archived_cycles[0]
    header = f"\n## Archived by cycle 3202 (CLOSED c{archived_cycles[0]} down to c{archived_cycles[-1]}, {len(archived_cycles)} blocks)\n\n"
    with open(ARCHIVE) as f:
        old_archive = f.read()
    with open(ARCHIVE, 'w') as f:
        f.write(header + archived_text + '\n\n' + old_archive)
    with open(QUEUE, 'w') as f:
        f.write(new_live_text)
    print("WROTE live + archive.")
else:
    print("DRY RUN only -- pass --write to apply.")
