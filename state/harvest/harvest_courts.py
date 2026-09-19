#!/usr/bin/env python3
"""Resumable harvest of CourtListener's court-id -> jurisdiction-code map (task h112(b)).

Why this exists: `/api/rest/v4/courts/` is the only authoritative source for each court's
`jurisdiction` code (F/FD/S/MA/...). We want a static courtId -> code map baked into
actors/court-records-scraper so `courtJurisdiction` can be emitted at ~100% fill on BOTH
opinion and docket rows (the old passthrough was scotus-only, ~9%).

Two things make this slow, both measured on cycle 496:
  * `page_size` is IGNORED — the endpoint is hard-wired to 20 rows/page, so `?in_use=true`
    (472 courts) is 24 pages, NOT the 5 pages earlier notes assumed.
  * Anonymous rate limiting TIGHTENS progressively from this box's IP: pages 1-8 came back
    with only brief 429 bursts, page 9 took ~4 retries, page 10 exhausted all 8 attempts.

So: run this repeatedly across cycles. It reads the partial file, skips pages whose rows it
already has, and only fetches what's missing. Safe to re-run any time; it never re-fetches
a completed page and writes after every page.

    python3 /root/agent/state/harvest/harvest_courts.py

Do NOT substitute the courtlistener GitHub fixture (cl/search/fixtures/court_data.json) for
this. It was checked on cycle 496 and is STALE: it has 422 courts vs 472 live, and it still
classifies the five military courts (acca, afcca, armfor, mc, nmcca) as "FS" where the live
API says "MA". Using it would bake wrong values into the Actor.
"""
import json
import os
import re
import sys
import time

import requests

UA = {'User-Agent': 'FetchSmith/1.0'}
MAX_WAIT = 240  # seconds; longer than this means the budget is hours out, so stop and re-run later
OUT = '/root/agent/state/harvest/courts_partial.json'
PAGES = 24  # 472 in_use courts / 20 per page, rounded up
URL = 'https://www.courtlistener.com/api/rest/v4/courts/?in_use=true&page={}'


def load():
    if os.path.exists(OUT):
        with open(OUT) as fh:
            return json.load(fh)
    return {}


def save(rows):
    with open(OUT, 'w') as fh:
        json.dump(rows, fh, indent=0, sort_keys=True)


def retry_after(resp, default):
    """CourtListener's 429 body states the exact wait: 'Expected available in N seconds.'

    Honouring it beats a fixed backoff — cycles 496-499 burned whole runs retrying every
    15s against a multi-hour budget. Capped so one huge number can't hang a cycle.
    """
    try:
        detail = resp.json().get('detail', '')
    except Exception:  # noqa: BLE001 - non-JSON error body, fall back
        return default
    m = re.search(r'in (\d+) seconds', detail)
    if not m:
        return default
    return min(int(m.group(1)) + 2, MAX_WAIT)


def fetch_page(page, attempts=8, delay=15):
    """Return the page's results, or None if the rate limiter never let us through."""
    for attempt in range(attempts):
        try:
            r = requests.get(URL.format(page), timeout=60, headers=UA)
        except Exception as exc:  # noqa: BLE001 - network flake, just retry
            print(f'p{page} a{attempt} ERR {exc}', flush=True)
            time.sleep(delay)
            continue
        if r.status_code == 200:
            return r.json()['results']
        wait = retry_after(r, delay) if r.status_code == 429 else delay
        print(f'p{page} a{attempt} {r.status_code} wait={wait}s', flush=True)
        if wait >= MAX_WAIT:
            # Budget is hours out, not seconds - give up now instead of sleeping the cycle away.
            print(f'p{page} LONG-THROTTLE ({wait}s) - abandoning run, re-run later', flush=True)
            return None
        time.sleep(wait)
    return None


def main():
    rows = load()
    print(f'resuming with {len(rows)} courts already harvested', flush=True)
    # A page is "done" only if we recorded a full 20 rows for it, so a partially-written
    # page is re-fetched rather than silently left short.
    done_pages = set(json.load(open(OUT + '.pages')) if os.path.exists(OUT + '.pages') else [])
    still_missing = []
    for page in range(1, PAGES + 1):
        if page in done_pages:
            continue
        results = fetch_page(page)
        if results is None:
            print(f'p{page} GIVEUP (rate limited) - re-run later', flush=True)
            still_missing.append(page)
            continue
        for c in results:
            rows[c['id']] = {
                'jurisdiction': c.get('jurisdiction'),
                'short_name': c.get('short_name'),
                'full_name': c.get('full_name'),
            }
        done_pages.add(page)
        save(rows)
        with open(OUT + '.pages', 'w') as fh:
            json.dump(sorted(done_pages), fh)
        print(f'p{page} ok ({len(results)} rows) total {len(rows)}', flush=True)
        time.sleep(8)
    save(rows)
    print(f'DONE total={len(rows)} expected=472 missing_pages={still_missing}', flush=True)
    return 0 if not still_missing else 1


if __name__ == '__main__':
    sys.exit(main())
