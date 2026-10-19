#!/usr/bin/env python3
"""Measure WHICH KIND of FEC committee carries 2+ `candidate_ids`, and whether
those ids are the same person or genuinely different candidates.

Why this exists (cycle 1936): cycles 1931/1932 measured the multi-candidate rate
over `designation=J` (joint fundraising committees) ONLY -- 4 of 1,330 (0.3%) --
and `fec-campaign-finance-scraper`'s README + v0.1.68/0.1.70 behaviour both
generalised that to "2+ candidate_ids means a JFC splitting money across several
candidates". A scan of the FULL cycle-2026 committee registry says otherwise:
430 of 20,903 committees list 2+ candidate ids, and only 4 of them are JFCs --
the overwhelming majority are `designation=P` principal campaign committees for
ONE person who holds several FEC candidate ids (a House id and a Senate id, or
two ids for the same seat in different cycles).

Usage:
  _fec_multicand_scan.py registry [CYCLE]       # full registry scan + designation split
  _fec_multicand_scan.py names <in.json> [N]    # resolve candidate names on a sample

`registry` writes its multi-candidate rows to /tmp/fec_multicand_<cycle>.json for
the `names` step. Free (no Apify spend) -- hits api.open.fec.gov with FEC_API_KEY.

RATE LIMIT WARNING (learned the hard way in 1936): resolving every candidate id
in one pass (~790 ids) trips HTTP 429 on this key. The `names` mode samples and
sleeps 1s between batches, with 429 backoff. Keep N small (<= 20 committees).

NAME MATCHING: exact string equality is TOO STRICT and will under-report the
same-person case -- the FEC spells the same human differently across ids
("DURBIN, RICHARD JOSEPH" vs "DURBIN, RICHARD J.", "BANKS, JAMES E HON." vs
"BANKS, JAMES E. HON."). This script prints both the strict verdict and a
surname+first-initial verdict so the gap is visible rather than silently chosen.
"""
import collections
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_KEY = os.environ["FEC_API_KEY"]


def get(path, **params):
    params["api_key"] = API_KEY
    url = f"https://api.open.fec.gov/v1{path}?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(20 * (attempt + 1))
                continue
            raise
    raise RuntimeError(f"429 after retries: {path}")


def norm_person(name):
    """Surname + first initial, punctuation/honorifics stripped -- tolerant enough
    to call 'DURBIN, RICHARD JOSEPH' and 'DURBIN, RICHARD J.' the same person."""
    if not name:
        return None
    n = re.sub(r"\b(MR|MRS|MS|DR|HON|JR|SR|I{1,3}|IV)\b\.?", "", name.upper())
    n = re.sub(r"[^A-Z, ]", " ", n)
    parts = [p.strip() for p in n.split(",") if p.strip()]
    if not parts:
        return None
    surname = parts[0].split()[0] if parts[0].split() else ""
    first = parts[1].split()[0] if len(parts) > 1 and parts[1].split() else ""
    return f"{surname}|{first[:1]}"


def registry(cycle):
    page, total = 1, 0
    hist = collections.Counter()
    multi = []
    declared = None
    while True:
        body = get("/committees/", cycle=cycle, per_page=100, page=page, sort="committee_id")
        results = body.get("results", [])
        if not results:
            break
        for c in results:
            ids = c.get("candidate_ids") or []
            total += 1
            hist[len(ids)] += 1
            if len(ids) > 1:
                multi.append({
                    "committee_id": c["committee_id"],
                    "name": c.get("name"),
                    "n": len(ids),
                    "designation": c.get("designation"),
                    "committee_type": c.get("committee_type"),
                    "candidate_ids": ids,
                })
        pg = body.get("pagination", {})
        if declared is None:
            declared = pg.get("count")
        if page >= (pg.get("pages") or 1):
            break
        page += 1
        time.sleep(0.1)

    n_multi = sum(v for k, v in hist.items() if k > 1)
    print(f"cycle={cycle} declared={declared} scanned={total}")
    print(f"candidate_ids length histogram: {dict(sorted(hist.items()))}")
    print(f"multi-candidate committees: {n_multi} / {total} = {n_multi / total * 100:.2f}%")
    with_any = sum(v for k, v in hist.items() if k >= 1)
    if with_any:
        print(f"  ... as a share of committees listing ANY candidate: "
              f"{n_multi} / {with_any} = {n_multi / with_any * 100:.2f}%")
    desig = collections.Counter(m["designation"] for m in multi)
    print(f"designation split of the multi-candidate ones: {dict(desig.most_common())}")
    print("  (P=principal campaign cte, A=authorized, J=JOINT FUNDRAISING, "
          "D=leadership PAC, U=unauthorized, B=lobbyist/registrant PAC)")
    out = f"/tmp/fec_multicand_{cycle}.json"
    json.dump(multi, open(out, "w"), indent=1)
    print(f"wrote {len(multi)} rows -> {out}")


def names(path, n):
    rows = json.load(open(path))
    random.seed(1936)
    sample = random.sample(rows, min(n, len(rows)))
    ids = sorted({i for r in sample for i in r["candidate_ids"] if i[:1] in "HSP"})
    resolved = {}
    for i in range(0, len(ids), 40):
        body = get("/candidates/", candidate_id=ids[i:i + 40], per_page=100)
        for c in body["results"]:
            resolved[c["candidate_id"]] = c.get("name")
        time.sleep(1.0)

    strict = collections.Counter()
    tolerant = collections.Counter()
    for r in sample:
        got = [resolved.get(i) for i in r["candidate_ids"]]
        uniq_strict = {x for x in got if x}
        uniq_person = {norm_person(x) for x in got if x} - {None}
        v_strict = "same" if len(uniq_strict) == 1 else "multi"
        v_person = "same" if len(uniq_person) == 1 else "multi"
        strict[v_strict] += 1
        tolerant[v_person] += 1
        flag = "" if v_strict == v_person else "   <-- spelling-only difference"
        print(f"{r['designation']} strict={v_strict:5} person={v_person:5} "
              f"{r['committee_id']} {(r['name'] or '')[:40]:42} "
              f"{list(zip(r['candidate_ids'], got))}{flag}")
    print(f"\nsample={len(sample)}  strict-name: {dict(strict)}  "
          f"surname+initial: {dict(tolerant)}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "registry"
    if mode == "registry":
        registry(int(sys.argv[2]) if len(sys.argv) > 2 else 2026)
    elif mode == "names":
        names(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 12)
    else:
        sys.exit(__doc__)
