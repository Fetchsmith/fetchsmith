#!/usr/bin/env python3
"""cycle 3548 -- full paginated-walk probe for the fec-campaign-finance-scraper guard relaxation.

Replicates EXACTLY what src/main.js's contributions-mode page walk sends
(/schedules/schedule_a/, sort=-contribution_receipt_date, sort_nulls_last=true,
per_page = 100 in watch mode / 20 otherwise) and advances the cursor with the
same `pagination.last_indexes` echo-back + cleaning rules (drop null/undefined/
false, normalise True -> 'true', stop when the cursor is empty or repeats).

Point of the probe: c3547 proved page 1 of three previously-504 shapes now
returns 200 in ~1s. A fast page 1 does NOT prove a deep walk stays fast if the
speedup is a cache/index that degrades with cursor depth. $0 -- direct
api.open.fec.gov calls, no Apify run. Rate limit on our key is 60/hour.

Usage: _fec3548_walk.py <shape> <pages> [per_page]
  shapes: unfiltered | retired | actblue | winred
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

API = 'https://api.open.fec.gov/v1/schedules/schedule_a/'
KEY = os.environ['FEC_API_KEY']

# Each shape is exactly the filter set main.js would build for that input, no more.
SHAPES = {
    # (a) main.js ~223-238: the unconditional "no narrowing filter set" fail-fast.
    'unfiltered': {},
    # (b) main.js ~519-561: the broad free-text 504 catch.
    'retired': {'contributor_occupation': 'RETIRED'},
    # (c) main.js ~157-173: committeeId gated off Schedule A for mega pass-throughs.
    'actblue': {'committee_id': 'C00401224'},
    'winred': {'committee_id': 'C00694323'},
}


def get(params):
    q = dict(params)
    q['api_key'] = KEY
    url = API + '?' + urllib.parse.urlencode(q)
    t0 = time.time()
    try:
        with urllib.request.urlopen(url, timeout=40) as r:
            body = json.loads(r.read())
            return r.status, time.time() - t0, body
    except urllib.error.HTTPError as e:
        return e.code, time.time() - t0, None
    except Exception as e:  # noqa: BLE001 -- timeouts are a result here, not a crash
        return f'ERR:{type(e).__name__}', time.time() - t0, None


def clean_cursor(last_indexes):
    """main.js L1118-1124: drop null/undefined/false, normalise true -> 'true'."""
    if not last_indexes:
        return {}
    out = {}
    for k, v in last_indexes.items():
        if v is None or v is False:
            continue
        out[k] = 'true' if v is True else v
    return out


def main():
    shape = sys.argv[1]
    pages = int(sys.argv[2])
    per_page = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    base = dict(SHAPES[shape])
    base['two_year_transaction_period'] = 2026
    base['sort'] = '-contribution_receipt_date'
    base['sort_nulls_last'] = 'true'
    base['per_page'] = per_page

    cursor = {}
    rows_deep = 0
    lats = []
    print(f'== shape={shape} per_page={per_page} pages={pages} filters={SHAPES[shape]}')
    for p in range(1, pages + 1):
        status, dt, body = get({**base, **cursor})
        lats.append(dt)
        if body is None:
            print(f'p{p:<4} depth={rows_deep:<7} {status} in {dt:.2f}s  <-- NON-200, walk aborted')
            break
        res = body.get('results') or []
        rows_deep += len(res)
        pg = body.get('pagination') or {}
        nxt = clean_cursor(pg.get('last_indexes'))
        newest = res[0].get('contribution_receipt_date') if res else None
        oldest = res[-1].get('contribution_receipt_date') if res else None
        print(f'p{p:<4} depth={rows_deep:<7} {status} in {dt:.2f}s rows={len(res):<4} '
              f'count={pg.get("count")} date_span={newest}..{oldest} cursor={json.dumps(nxt)}')
        if not res:
            print('  -> empty page, walk ends')
            break
        if not nxt or json.dumps(nxt) == json.dumps(cursor):
            print('  -> cursor exhausted/repeated, walk ends (main.js L1127 test)')
            break
        cursor = nxt
    if lats:
        print(f'-- latency: n={len(lats)} min={min(lats):.2f}s max={max(lats):.2f}s '
              f'mean={sum(lats)/len(lats):.2f}s first={lats[0]:.2f}s last={lats[-1]:.2f}s')


if __name__ == '__main__':
    main()
