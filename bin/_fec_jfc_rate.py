#!/usr/bin/env python3
"""Measure the share of schedule_a contributions routed through multi-candidate
joint fundraising committees (JFCs), using the FEC's keyset cursor (not the
broken offset `page=` param, confirmed broken live in cycle 1930).

Usage: _fec_jfc_rate.py <YYYY-MM-DD> <num_pages> [per_page]

Scoped to a single min_date=max_date day (keyset-paginated within that day) --
an unbounded two_year_transaction_period query with a date sort 504s upstream
(confirmed live, cycle 1931: per_page=100/20 with no date bound times out at
30-60s; a single-day bound returns in <1s).

Free (no Apify spend) -- hits api.open.fec.gov directly with FEC_API_KEY.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.parse

API_BASE = "https://api.open.fec.gov/v1/schedules/schedule_a/"
API_KEY = os.environ["FEC_API_KEY"]


def fetch(params):
    url = API_BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    day = sys.argv[1]
    num_pages = int(sys.argv[2])
    per_page = int(sys.argv[3]) if len(sys.argv) > 3 else 100

    cursor = {}
    total_rows = 0
    total_amount = 0.0
    jfc_rows = 0
    jfc_amount = 0.0
    jfc_committees = {}
    declared_count = None

    year = int(day[:4])
    period = year if year % 2 == 0 else year + 1
    params_base = {
        "api_key": API_KEY,
        "two_year_transaction_period": period,
        "min_date": day,
        "max_date": day,
        "per_page": per_page,
    }

    for page in range(num_pages):
        params = {**params_base, **cursor}
        try:
            body = fetch(params)
        except Exception as e:
            print(f"ERROR on page {page}: {e}", file=sys.stderr)
            break

        if declared_count is None:
            declared_count = body.get("pagination", {}).get("count")

        results = body.get("results", [])
        if not results:
            print(f"Exhausted at page {page} (0 results)", file=sys.stderr)
            break

        for row in results:
            total_rows += 1
            amt = row.get("contribution_receipt_amount") or 0
            total_amount += amt
            committee = row.get("committee") or {}
            cand_ids = committee.get("candidate_ids") or []
            if len(cand_ids) > 1:
                jfc_rows += 1
                jfc_amount += amt
                cid = committee.get("committee_id")
                jfc_committees[cid] = jfc_committees.get(cid, 0) + 1

        next_cursor = body.get("pagination", {}).get("last_indexes") or {}
        cleaned = {
            k: ("true" if v is True else v)
            for k, v in next_cursor.items()
            if v is not None and v is not False
        }
        if not cleaned or cleaned == cursor:
            print(f"Cursor exhausted at page {page}", file=sys.stderr)
            break
        cursor = cleaned
        time.sleep(0.15)  # be polite to the public API

    print(f"declared_total_matches={declared_count}")
    print(f"pages_fetched={page + 1}")
    print(f"total_rows={total_rows}")
    print(f"total_amount={total_amount:.2f}")
    print(f"jfc_rows={jfc_rows}")
    print(f"jfc_amount={jfc_amount:.2f}")
    if total_rows:
        print(f"jfc_row_rate={jfc_rows / total_rows * 100:.2f}%")
    if total_amount:
        print(f"jfc_amount_rate={jfc_amount / total_amount * 100:.2f}%")
    print(f"distinct_jfc_committees={len(jfc_committees)}")
    top = sorted(jfc_committees.items(), key=lambda kv: -kv[1])[:5]
    print(f"top_jfc_committees={top}")


if __name__ == "__main__":
    main()
