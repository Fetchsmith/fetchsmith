#!/root/agent/venv/bin/python
"""Record cycle 2888's unreachable_remedy audit of fda-recall-scraper.

Targeted string replace, NOT json.dump -- a json.dump rewrite reformats/re-escapes
the whole file (the c2551 trap: 630 lines of diff for a 2-field change).
"""
import re, pathlib
p = pathlib.Path('/root/agent/state/audit_dates.json')
s = p.read_text()
blk = re.search(r'"fda-recall-scraper":\s*\{.*?\n  \}', s, re.S)
assert blk, 'actor block not found'
old = blk.group(0)
assert '"unreachable_remedy": 2552' in old, 'expected old value 2552, got: %r' % old[:400]
new = old.replace('"unreachable_remedy": 2552', '"unreachable_remedy": 2888')
s2 = s.replace(old, new, 1)
assert s2 != s and len(s2) == len(s)  # 2552 -> 2888, same width
p.write_text(s2)
print('recorded unreachable_remedy 2552 -> 2888 for fda-recall-scraper')
