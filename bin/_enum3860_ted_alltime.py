#!/usr/bin/env python3
"""cycle 3860 enum_audit companion for eu-ted-tenders-scraper.

bin/_enum3524_ted.py re-proves ACCEPTANCE + the 365d/since-2023 live-vs-historical
partition.  It deliberately never measures the ALL-TIME totals that the
procedureType dropdown's 18 enumTitles quote (and the two the noticeTypes
description quotes), because those need an unbounded query.  c3524 restamped
them by hand; this script makes that step repeatable.

Same method trap as c3188: STRICTLY SEQUENTIAL, retry ladder, a probe that never
succeeds is ERROR, never 0.
"""
import json, sys
sys.path.insert(0, '/root/agent/bin')
from importlib.machinery import SourceFileLoader
m = SourceFileLoader('e3524', '/root/agent/bin/_enum3524_ted.py').load_module()

SCHEMA = '/root/agent/actors/eu-ted-tenders-scraper/.actor/input_schema.json'


def main():
    s = json.load(open(SCHEMA))['properties']
    targets = [('procedure-type', v) for v in s['procedureType']['items']['enum']]
    targets += [('notice-type', v) for v in ('cn-standard', 'can-standard')]
    rows, errs = [], []
    for fld, v in targets:
        c, e = m.probe(f'{fld}="{v}"')
        if e:
            errs.append((fld, v, e))
        print(f'{fld:14} {v:14} alltime={c if c is not None else "ERR:" + str(e)}', flush=True)
        rows.append({'field': fld, 'value': v, 'alltime': c, 'err': e})
    json.dump(rows, open('/tmp/enum3860_alltime.json', 'w'), indent=1)
    print(f'\n{len(rows)} probed, {len(errs)} error(s)')
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
