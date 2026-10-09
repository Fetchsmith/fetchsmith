#!/root/agent/venv/bin/python
"""Cycle 1344: live-price the whole unnamed tail of the hacker-news niche.

Reuses check-price-superiority's headline_price()/effective() verbatim via import
so the batch agrees with the fleet checker instead of re-deriving pricing rules.
"""
import datetime
import importlib.machinery
import importlib.util
import json
import os
import sys

import httpx

ROOT = "/root/agent"
_path = os.path.join(ROOT, "bin/check-price-superiority")
# extensionless script: spec_from_file_location can't infer a loader, so name one
spec = importlib.util.spec_from_loader("cps", importlib.machinery.SourceFileLoader("cps", _path))
cps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cps)

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

handles = [l.strip() for l in open("/tmp/hn_handles.txt") if l.strip()]
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
        # full event map so start fees / secondary charges are visible, not just the headline
        "events": {k: {"usd": cps.price_of(v), "primary": v.get("isPrimaryEvent"),
                       "onetime": v.get("isOneTimeEvent"), "title": v.get("eventTitle"),
                       "tiered": v.get("eventTieredPricingUsd")}
                   for k, v in events.items()},
        # cycle-1260 rule (a): a scheduled future price is invisible to effective()
        "future": [{"model": p.get("pricingModel"), "startedAt": p.get("startedAt")}
                   for p in (d.get("pricingInfos") or [])
                   if p.get("startedAt") and p["startedAt"] > NOW.isoformat()],
        "desc": (d.get("description") or "")[:400],
    })
    if i % 25 == 0:
        print(f"  ...{i}/{len(handles)}", file=sys.stderr)

json.dump(out, open("/tmp/hn_prices.json", "w"), indent=1)
print(f"priced {len(out)} listings -> /tmp/hn_prices.json")
