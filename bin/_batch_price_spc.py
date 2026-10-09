#!/root/agent/venv/bin/python
"""Cycle 1372: live-price all 64 UNNAMED listings in shopify-products-scraper's niche.

Same shape as _batch_price_ufaw.py (cycle 1333) but with a thread pool, per the
cycle-1368 lesson that 40+ sequential 30s-timeout GETs is needlessly slow.
"""
import concurrent.futures as cf
import datetime
import importlib.machinery
import importlib.util
import json
import os
import sys

import httpx

ROOT = "/root/agent"
_path = os.path.join(ROOT, "bin/check-price-superiority")
spec = importlib.util.spec_from_loader("cps", importlib.machinery.SourceFileLoader("cps", _path))
cps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cps)

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

handles = [l.strip() for l in open("/tmp/spc_unnamed.txt") if l.strip()]


def price_one(h):
    u, n = h.split("/", 1)
    try:
        r = httpx.get(f"{API}/acts/{u}~{n}", headers=H, timeout=30)
        d = r.json().get("data") if r.status_code == 200 else None
    except Exception as e:
        print(f"ERR {h}: {e}", file=sys.stderr)
        d = None
    if not d:
        return {"handle": h, "error": "unresolvable"}
    price, label = cps.headline_price(d, NOW)
    runfee, runfee_label = cps.runfee_price(d, NOW)
    cur = cps.effective(d.get("pricingInfos"), NOW) or {}
    events = (cur.get("pricingPerEvent", {}) or {}).get("actorChargeEvents", {}) or {}
    return {
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
        "tiered": {k: v.get("eventTieredPricingUsd") for k, v in events.items()},
        "monthlyUsd": cur.get("pricePerUnitUsd") or cur.get("monthlyUsd"),
        "startedAt": cur.get("startedAt"),
        "desc": (d.get("description") or "")[:300],
    }


with cf.ThreadPoolExecutor(max_workers=8) as ex:
    out = list(ex.map(price_one, handles))

json.dump(out, open("/tmp/spc_prices.json", "w"), indent=1)
print(f"priced {len(out)} listings -> /tmp/spc_prices.json")
