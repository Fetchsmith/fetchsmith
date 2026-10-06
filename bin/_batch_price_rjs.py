#!/root/agent/venv/bin/python
"""Cycle 1312: live-price the 127-listing >=3-user unnamed cut of remote-jobs-scraper's niche."""
import datetime
import importlib.util
import importlib.machinery
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

handles = [l.strip() for l in open("/tmp/rjs_unnamed3.txt") if l.strip()]
out = []
for i, h in enumerate(handles, 1):
    u, n = h.split("/", 1)
    try:
        r = httpx.get(f"{API}/acts/{u}~{n}", headers=H, timeout=30)
        d = r.json().get("data") if r.status_code == 200 else None
    except Exception as e:
        d = None
        print(f"ERR {h}: {e}", file=sys.stderr)
    if not d:
        out.append({"handle": h, "error": "unresolvable"})
        continue
    price, label = cps.headline_price(d, NOW)
    cur = cps.effective(d.get("pricingInfos"), NOW) or {}
    events = (cur.get("pricingPerEvent", {}) or {}).get("actorChargeEvents", {}) or {}
    out.append({
        "handle": h,
        "title": d.get("title"),
        "users": (d.get("stats") or {}).get("totalUsers"),
        "price": price,
        "label": label,
        "model": cur.get("pricingModel"),
        "events": {k: {"usd": cps.price_of(v), "primary": v.get("isPrimaryEvent"),
                       "onetime": v.get("isOneTimeEvent"), "title": v.get("eventTitle")}
                   for k, v in events.items()},
        "desc": (d.get("description") or "")[:400],
        # keep the full current event map so finalists' tiers can be checked
        # without a second round of live calls
        "raw_events": events,
        "startedAt": cur.get("startedAt"),
    })
    if i % 10 == 0:
        print(f"  ...{i}/{len(handles)}", file=sys.stderr)

json.dump(out, open("/tmp/rjs_prices.json", "w"), indent=1)
print(f"priced {len(out)} listings -> /tmp/rjs_prices.json")
