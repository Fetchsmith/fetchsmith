import subprocess, collections
P='tasks/queue.md'; A='tasks/queue_archive.md'
orig=open(P,encoding='utf8').read()
lines=orig.split('\n')
# 1-indexed span 28..37 == c3575 block + its own leading/trailing seam + the `---` + c3574 block
start,end=28,37
cut=lines[start-1:end]
assert cut[0].startswith('- [x] **CLOSED c3575'), cut[0][:60]
assert any(l.startswith('- [x] **CLOSED c3574') for l in cut), 'c3574 not in span'
assert cut[-1].strip()=='', repr(cut[-1])
assert lines[start-2].strip()=='', 'line before span must be blank'
assert lines[end].startswith('- [ ] **NEW c3568(c)'), lines[end][:60]
kept=lines[:start-1]+lines[end:]
# lossless: multiset of non-blank lines
before=collections.Counter(l for l in lines if l.strip())
after=collections.Counter(l for l in kept if l.strip())+collections.Counter(l for l in cut if l.strip())
assert before==after, 'LOSSY'
# seam: double-blank count unchanged
dbl=lambda ls: sum(1 for i in range(len(ls)-1) if not ls[i].strip() and not ls[i+1].strip())
print('double-blanks before/after:', dbl(lines), dbl(kept))
assert dbl(kept)==dbl(lines), 'seam changed double-blank count'
open(A,'a',encoding='utf8').write('\n\n## Archived by cycle 3580\n\n'+'\n'.join(cut).rstrip()+'\n')
open(P,'w',encoding='utf8').write('\n'.join(kept))
print('cut %d lines, %d bytes' % (len(cut), len('\n'.join(cut))))
print('queue: %d -> %d bytes, %d -> %d lines' % (len(orig), len('\n'.join(kept)), len(lines), len(kept)))
