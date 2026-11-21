#!/usr/bin/env python3
"""cycle 3524 enum_audit probe for eu-ted-tenders-scraper.

Re-proves, LIVE, all 40 declared enum values of noticeTypes[] + procedureType[]:
  (a) still ACCEPTED as a filter value by api.ted.europa.eu/v3/notices/search
  (b) count in the last 365 days  (the live/historical-only partition)
  (c) count since 2023-01-01      (the numbers quoted in both schema descriptions)

METHOD TRAP (c3188, cost that cycle ~10 min): probing 4-way concurrent made TED
answer 5 probes with retry-exhausted errors, and a None count binned as a falsy
zero fabricated a 3-code regression. So: STRICTLY SEQUENTIAL, explicit retry
ladder, and a probe that never succeeds is reported as ERROR -- never as 0.
"""
import json
import sys
import time
import urllib.error
import urllib.request

URL = 'https://api.ted.europa.eu/v3/notices/search'
SCHEMA = '/root/agent/actors/eu-ted-tenders-scraper/.actor/input_schema.json'


def probe(query, tries=5):
    """Return (count, None) on success or (None, err) -- never (0, ...) on failure."""
    payload = json.dumps({'query': query, 'page': 1, 'limit': 1,
                          'fields': ['publication-number']}).encode()
    last = None
    for attempt in range(tries):
        if attempt:
            time.sleep(min(2.5 * (2 ** (attempt - 1)), 20))
        req = urllib.request.Request(
            URL, data=payload, headers={'content-type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                body = json.load(r)
            for k in ('totalNoticeCount', 'totalNoticesCount', 'total'):
                if k in body:
                    return int(body[k]), None
            return None, f'no count key in {sorted(body)[:6]}'
        except urllib.error.HTTPError as e:
            raw = e.read().decode('utf-8', 'replace')
            if e.code == 400:
                try:
                    return None, 'HTTP400:' + json.loads(raw).get('type', '?')
                except Exception:
                    return None, 'HTTP400'
            last = f'HTTP{e.code}'
        except Exception as e:  # noqa: BLE001 - network flake, retry
            last = type(e).__name__
    return None, last or 'exhausted'


def main():
    s = json.load(open(SCHEMA))['properties']
    fields = [('notice-type', s['noticeTypes']['items']['enum']),
              ('procedure-type', s['procedureType']['items']['enum'])]

    # Control FIRST: if a bogus value does not 400, then HTTP 200 proves nothing.
    for fld in ('notice-type', 'procedure-type'):
        c, err = probe(f'{fld}=zzz-bogus')
        print(f'CONTROL {fld}=zzz-bogus -> count={c} err={err}', flush=True)
        if not (err or '').startswith('HTTP400'):
            print('ABORT: control did not 400 -- acceptance test is not valid', file=sys.stderr)
            return 2

    rows, errors = [], []
    for fld, values in fields:
        for v in values:
            d365, e365 = probe(f'{fld}="{v}" AND publication-date>=today(-365)')
            d23, e23 = probe(f'{fld}="{v}" AND publication-date>=20230101')
            if e365 or e23:
                errors.append((fld, v, e365, e23))
            rows.append({'field': fld, 'value': v, 'd365': d365, 'since2023': d23,
                         'err365': e365, 'err2023': e23})
            print(f'{fld:14} {v:18} 365d={d365 if d365 is not None else "ERR:" + str(e365):>9} '
                  f'since2023={d23 if d23 is not None else "ERR:" + str(e23):>9}', flush=True)
            time.sleep(0.6)

    json.dump(rows, open('/tmp/enum3524_rows.json', 'w'), indent=1)
    accepted = [r for r in rows if not (r['err365'] or '').startswith('HTTP400')
                and not (r['err2023'] or '').startswith('HTTP400')]
    hist = [r for r in rows if r['d365'] == 0 and (r['since2023'] or 0) > 0]
    live = [r for r in rows if (r['d365'] or 0) > 0]
    print(f'\n{len(rows)} values probed | accepted(no 400)={len(accepted)} '
          f'| live-in-365d={len(live)} | historical-only={len(hist)} | errored={len(errors)}')
    print('HISTORICAL-ONLY:', ', '.join(f"{r['value']}({r['since2023']})" for r in hist))
    if errors:
        print('ERRORS (NOT zeros -- must be resolved before any conclusion):')
        for e in errors:
            print('  ', e)
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
