#!/root/agent/venv/bin/python
"""Live-price UNNAMED listings in the google-play-reviews-scraper niche (full tiered maps + user counts).

Cycle 1338: first version, 49 >=3-user listings. Cycle 1378 re-ran it on 67.
Cycle 1412: closed this copy's leg of `0-TODO-h1392-runfee-in-batch-copies` and repointed the
GET at `bin/_apify_get.py`. Two changes, both for reasons already proven on this fleet:
  * `runfee` — `cps.headline_price` collapses a PURE run-fee rival (every charge event
    run-scoped) to one number and so reads it as "pricier" when $0.02 there buys a WHOLE RUN.
    `cps.runfee_price` (cycle 1392) holds that shape out of the per-row comparison and returns
    an exact crossover. This niche makes it concrete, not hypothetical: the cohort contains
    `alexmorain/app-store-play-store-scraper`, whose own title advertises "$0.01/App, No Cap".
  * `get_json` — the old unguarded `httpx.get(...).json()` turned one transient non-JSON body
    into `error: unresolvable`, i.e. a rival that silently drops out of the comparison (the
    cycle-1404 shape-(b) SILENT SKIP). 401/403/404/410 still resolve immediately without
    retrying, because a delisted rival is a real final answer.
Input: one `owner/slug` per line in /tmp/gprs_ge3.txt. Output: /tmp/gprs_prices.json."""
import datetime
import importlib.util
import importlib.machinery
import json
import os
import sys

ROOT = "/root/agent"
sys.path.insert(0, os.path.join(ROOT, "bin"))
from _apify_get import ApifyGetError, get_data  # noqa: E402

_path = os.path.join(ROOT, "bin/check-price-superiority")
spec = importlib.util.spec_from_loader("cps", importlib.machinery.SourceFileLoader("cps", _path))
cps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cps)

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

handles = [l.strip() for l in open("/tmp/gprs_ge3.txt") if l.strip()]
out = []
for i, h in enumerate(handles, 1):
    u, n = h.split("/", 1)
    try:
        d = get_data(f"{API}/acts/{u}~{n}", headers=H)
    except ApifyGetError as e:
        d = None
        print(f"ERR {h}: {e}", file=sys.stderr)
    if not d:
        out.append({"handle": h, "error": "unresolvable"})
        continue
    price, label = cps.headline_price(d, NOW)
    runfee, runfee_label = cps.runfee_price(d, NOW)
    cur = cps.effective(d.get("pricingInfos"), NOW) or {}
    events = (cur.get("pricingPerEvent", {}) or {}).get("actorChargeEvents", {}) or {}
    out.append({
        "handle": h,
        "title": d.get("title"),
        "users": (d.get("stats") or {}).get("totalUsers"),
        "price": price,
        "label": label,
        "runfee": runfee,
        "runfee_label": runfee_label,
        "model": cur.get("pricingModel"),
        "events": {k: {"usd": cps.price_of(v), "primary": v.get("isPrimaryEvent"),
                       "onetime": v.get("isOneTimeEvent"), "title": v.get("eventTitle")}
                   for k, v in events.items()},
        "desc": (d.get("description") or "")[:400],
        "raw_events": events,
        "tiered": {k: v.get("eventTieredPricingUsd") for k, v in events.items()},
        "startedAt": cur.get("startedAt"),
    })
    if i % 10 == 0:
        print(f"  ...{i}/{len(handles)}", file=sys.stderr)

json.dump(out, open("/tmp/gprs_prices.json", "w"), indent=1)
print(f"priced {len(out)} listings -> /tmp/gprs_prices.json")
