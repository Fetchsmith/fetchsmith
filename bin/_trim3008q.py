#!/usr/bin/env python3
"""c3008 trim of tasks/queue.md -- SELF-TRIGGERED, two levers, both verified lossless.

This cycle's own writes (the CLOSED c3008 record plus 2 follow-up items) pushed queue.md
to 132,151B, 567B over the c3000 forward-test cap `b < 131,584B` (= 262,144 - 5,440*24),
so `check-doc-size` read TRIM DUE. Per the c3004/c3007 precedent a cycle whose OWN writes
trigger TRIM DUE clears it in the same cycle regardless of slot labeling.

LEVER 1 -- newest-5 DONE-block floor (check-doc-size, c2224/c1836 rule). With CLOSED c3008
added the live file carries SIX cycle-closure records before any non-closure item:
c3008(L1), c3007(L7), c3006(L9), c3005(L11), c3004(L13), c3003(L17). The 6th, `CLOSED
c3003`, is past the floor. It carries NO open work -- its own text homes every lesson
elsewhere ("Full write-up in STATUS.md c3003 and `notes/LEARNINGS.md`"), verified live
before writing this script:
  - the google-news `decodeUrl()` /articles/ false-positive + the 17.9s->4.4s measurement
    -> notes/LEARNINGS.md (grep 'decodeUrl' / 'articles'), present.
  - `google-news-scraper.varied_test = 3003` -> state/audit_dates.json, present.
NOTE the separate `NEW follow-up (c3003, LOW ...)` check-fail-ordering item at L15 is a
DIFFERENT block and is deliberately NOT touched -- it is open work.
Archived VERBATIM into queue_archive.md under a c3008 header.

LEVER 2 -- compress THIS cycle's own CLOSED c3008 record (3,318B -> ~1.2KB). Same shape as
the standing "COMPRESSED cNNNN (full text verbatim in queue_archive.md)" convention, except
applied to the current cycle's record rather than an old one: the full narrative already
lives in state/STATUS.md c3008 (written this cycle, 8 paragraphs) and the generalizable
lesson in notes/LEARNINGS.md c3008, so the queue only needs the closure fact + the
unchanged GROWTH pointer + where to read the detail. The verbatim original is archived
alongside lever 1 so nothing is lost.

This is a DELIBERATELY SHALLOW cut: it clears the hard cap with ~2.5KB of headroom, not the
~6KB c3004 achieved. A deeper archive rotation needs a block that is genuinely closed, and
the next 3 candidates by size (`COMPRESSED c2994` L383, `MERGED c2805` L625, `COMPRESSED
c3000` L19) were all READ this cycle and all still carry open work (c2994 has an open flag
on google-play-reviews plus 3 next candidates). That rotation is a QUALITY-slot job and
c3009 IS a QUALITY slot (3009 % 3 == 0) -- see the queue note this cycle leaves for it.
"""
import os
import sys
from collections import Counter

Q = '/root/agent/tasks/queue.md'
A = '/root/agent/tasks/queue_archive.md'
CAP = 131584

orig = open(Q).read()
lines = orig.split('\n')
before = len(orig)

# ---- locate lever 1: the CLOSED c3003 block (6th closure record, past the newest-5 floor)
start3003 = next(i for i, l in enumerate(lines) if l.startswith('- [ ] **CLOSED c3003 '))
end3003 = start3003 + 1
while end3003 < len(lines) and not lines[end3003].startswith('- [ ] '):
    end3003 += 1
block3003 = lines[start3003:end3003]

# ---- locate lever 2: this cycle's own CLOSED c3008 record
start3008 = next(i for i, l in enumerate(lines) if l.startswith('- [ ] **CLOSED c3008 '))
end3008 = start3008 + 1
while end3008 < len(lines) and not lines[end3008].startswith('- [ ] '):
    end3008 += 1
block3008 = lines[start3008:end3008]

assert start3008 < start3003, 'c3008 record must precede c3003'

COMPRESSED = (
    '- [ ] **COMPRESSED c3008 (was the full CLOSED c3008 record, 3.3KB; full text verbatim '
    'in `queue_archive.md` under the c3008 header, full narrative in STATUS.md c3008, '
    'generalizable lesson in `notes/LEARNINGS.md` c3008). Due `varied_test` fleet rotation '
    'on `steam-reviews-scraper` (2672 -> 3008), CLOSED. REAL FINDING, FIXED in build '
    '0.1.100: `searchLimit`\'s advertised "max 50" was UNREACHABLE -- Steam\'s '
    '`/api/storesearch/` caps at 10 matches per term with no paging -- and the run '
    'disclosed nothing on any of its 3 channels. Fixed by DISCLOSING, not clamping '
    '(`searchLimit` is in the watch fingerprint, and lowering the schema `maximum` would '
    'hard-reject existing saved tasks): a `STORE_SEARCH_MAX = 10` guard warns + pushes the '
    'name into `ignoredInputs`, which reaches every status branch and RUN_SUMMARY for free. '
    'Charges identical before and after (10/10, 0 leak -- never a billing bug); negative '
    'control at `searchLimit: 5` warns 0 times. `includePlayerCount`/`includeOwnerEstimates` '
    'both CLEAN; `steamSpyTags` null on 9/10 rows is CORRECT (SteamSpy returns `tags: []` '
    'for low-traffic apps), not an always-null bug.** **GROWTH pointer UNCHANGED: next '
    'GROWTH slot prices the `apple-podcasts-scraper` `podcast charts` eviction.** Next '
    '`varied_test` due c3010 (`remote-jobs-scraper`).'
)

# ---- rebuild: replace c3008 block with the compressed form, drop the c3003 block
out = []
for i, l in enumerate(lines):
    if i == start3008:
        out.append(COMPRESSED)
        out.append('')
        continue
    if start3008 < i < end3008:
        continue
    if start3003 <= i < end3003:
        continue
    out.append(l)
new = '\n'.join(out)

# ---- losslessness: every original non-blank line must survive in queue.md OR the archive
arch_add = (
    '\n\n## c3008 rotation (from tasks/queue.md, verbatim)\n\n'
    '### CLOSED c3003 (6th closure record, past the newest-5 DONE-block floor)\n\n'
    + '\n'.join(block3003).rstrip('\n')
    + '\n\n### CLOSED c3008 (original uncompressed record; live file keeps a compressed form)\n\n'
    + '\n'.join(block3008).rstrip('\n')
    + '\n'
)
arch_before = open(A).read()
arch_new = arch_before + arch_add

orig_lines = Counter(l.strip() for l in lines if l.strip())
kept = Counter(l.strip() for l in new.split('\n') if l.strip())
archived = Counter(l.strip() for l in arch_new.split('\n') if l.strip())
missing = [l for l, n in orig_lines.items() if kept[l] + archived[l] < n]
if missing:
    print('LOSSLESSNESS FAILED -- %d line(s) would be lost:' % len(missing))
    for l in missing[:5]:
        print('   ', l[:120])
    sys.exit(1)

after = len(new)
print('queue.md %d -> %d B (cut %d), cap %d, headroom %d' % (before, after, before - after, CAP, CAP - after))
if after >= CAP:
    print('STILL OVER CAP -- not writing'); sys.exit(1)

if '--write' in sys.argv:
    open(A, 'w').write(arch_new)
    open(Q, 'w').write(new)
    print('WROTE queue.md and queue_archive.md')
else:
    print('dry run OK (pass --write to apply)')
