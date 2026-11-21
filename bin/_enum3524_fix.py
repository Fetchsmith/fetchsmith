#!/usr/bin/env python3
"""cycle 3524: restamp eu-ted-tenders-scraper's procedureType option counts.

The 18 all-time counts live in `enumTitles`, i.e. in the buyer's input form, and
were measured 2026-09-26 with NO "as of" date anywhere in the UI. Re-measured
live this cycle: the 8 live codes drifted UP (+0.4%..+9.1%) and the 9 legacy
codes drifted DOWN (-0.8%..-4.2%, TED pruning pre-2023 notices from the index).

Replaces the exact old number string inside each title and asserts exactly one
replacement per title, because the number is NOT always the last paren group
("Legacy pre-eForms code 4 (170,522) - TED publishes no label for it") and one
title contains a decoy paren ("... art. 5(3)) (3,084)").
"""
import json
import sys

SCHEMA = '/root/agent/actors/eu-ted-tenders-scraper/.actor/input_schema.json'

# value: (old number string as it appears in the title, new number string)
COUNTS = {
    'open':        ('5,514,283', '5,565,282'),
    'restricted':  ('272,065', '274,803'),
    'neg-w-call':  ('347,731', '355,066'),
    'neg-wo-call': ('218,760', '221,267'),
    'comp-dial':   ('16,857', '16,922'),
    'oth-single':  ('30,716', '33,420'),
    'oth-mult':    ('8,256', '9,007'),
    'innovation':  ('1,319', '1,326'),
    '4':           ('170,522', '166,797'),
    '9':           ('155,269', '152,806'),
    'V':           ('78,038', '76,674'),
    'E':           ('23,813', '23,592'),
    'Z':           ('9,541', '9,458'),
    '6':           ('4,255', '4,076'),
    'A':           ('2,633', '2,558'),
    'F':           ('1,183', '1,174'),
    '8':           ('854', '854'),
    'comp-tend':   ('3,084', '3,175'),
}
STAMP = (' Every option count in this dropdown is an all-time TED total measured live on '
         '2026-11-21 (cycle 3524); the live codes grow daily and the legacy ones drift slowly '
         'downward as TED prunes pre-2023 notices from its index, so treat them as of that date.')


def main():
    write = '--write' in sys.argv
    raw = open(SCHEMA).read()
    s = json.loads(raw)
    p = s['properties']['procedureType']['items']
    vals, titles = p['enum'], p['enumTitles']
    assert len(vals) == len(titles) == 18, (len(vals), len(titles))

    changed = 0
    for i, v in enumerate(vals):
        old, new = COUNTS[v]
        t = titles[i]
        assert t.count(old) == 1, f'{v}: expected exactly 1 occurrence of {old!r} in {t!r}'
        if old != new:
            titles[i] = t.replace(old, new)
            changed += 1
        print(f'  {v:12} {old:>9} -> {new:<9} {"(unchanged)" if old == new else ""}')

    d = s['properties']['procedureType']['description']
    assert 'measured live on 2026-11-21' not in d, 'stamp already present'
    assert d.endswith('run start instead of just returning 0 rows.'), d[-60:]
    s['properties']['procedureType']['description'] = d + STAMP

    print(f'\n{changed} of 18 titles changed; description stamp appended '
          f'({len(d)} -> {len(d) + len(STAMP)} chars)')
    if not write:
        print('DRY RUN -- pass --write to apply')
        return 0

    # Preserve the file's existing 2-space/no-ascii-escape style.
    out = json.dumps(s, indent=2, ensure_ascii=False) + '\n'
    open(SCHEMA, 'w').write(out)
    # Re-read and prove only the intended keys moved.
    before, after = json.loads(raw), json.loads(open(SCHEMA).read())
    diffs = []

    def walk(a, b, path=''):
        if isinstance(a, dict) and isinstance(b, dict):
            assert set(a) == set(b), f'key set changed at {path}'
            for k in a:
                walk(a[k], b[k], f'{path}.{k}')
        elif isinstance(a, list) and isinstance(b, list):
            assert len(a) == len(b), f'length changed at {path}'
            for j, (x, y) in enumerate(zip(a, b)):
                walk(x, y, f'{path}[{j}]')
        elif a != b:
            diffs.append(path)

    walk(before, after)
    expected_prefix = ('.properties.procedureType.items.enumTitles',
                       '.properties.procedureType.description')
    unexpected = [d for d in diffs if not d.startswith(expected_prefix)]
    print(f'WROTE. {len(diffs)} value(s) changed, {len(unexpected)} unexpected: {unexpected}')
    return 1 if unexpected else 0


if __name__ == '__main__':
    sys.exit(main())
