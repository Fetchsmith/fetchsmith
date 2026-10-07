#!/root/agent/venv/bin/python
"""Cycle 1363: live-price the 41-listing >=3-user unnamed cohort of ats-jobs-scraper's niche
(200 matched via niche-size, 181 unnamed total, 41 with >=3 users -- resweep of 1327's 39).

OURS: tiered $0.001/job (FREE) -> $0.00085 (BRONZE) -> $0.00075 (SILVER) -> $0.0007 (GOLD+),
no start fee -- re-verified against our own meta.json, matches check-own-price-freshness 0 drift.
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
spec = importlib.util.spec_from_loader("cps", importlib.machinery.SourceFileLoader("cps", _path))
cps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cps)

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

OURS = {"FREE": 0.001, "BRONZE": 0.00085, "SILVER": 0.00075, "GOLD": 0.0007,
        "PLATINUM": 0.0007, "DIAMOND": 0.0007}


def tiers_of(ev):
    t = ev.get("eventTieredPricingUsd") or ev.get("tieredEventPriceUsd")
    out = {}
    if isinstance(t, dict):
        for k, v in t.items():
            if isinstance(v, (int, float)):
                out[k] = v
            elif isinstance(v, dict) and isinstance(v.get("tieredEventPriceUsd"), (int, float)):
                out[k] = v["tieredEventPriceUsd"]
    if out:
        return out
    p = cps.price_of(ev)
    return {"FREE": p} if isinstance(p, (int, float)) else {}


def unit_price(events):
    onetime, recurring = {}, {}
    for k, v in events.items():
        (onetime if v.get("isOneTimeEvent") else recurring)[k] = v
    start_fee = max((min(tiers_of(v).values(), default=0.0) for v in onetime.values()),
                    default=0.0)
    if not recurring:
        return {}, None, start_fee, "no recurring event -- one-time/start-fee only"
    primary = [k for k, v in recurring.items() if v.get("isPrimaryEvent")]
    if len(primary) == 1:
        k = primary[0]
        return tiers_of(recurring[k]), k, start_fee, "primary event"
    if len(recurring) == 1:
        k = next(iter(recurring))
        return tiers_of(recurring[k]), k, start_fee, "sole recurring event (no primary flag)"
    if primary:
        k = min(primary, key=lambda k: min(tiers_of(recurring[k]).values(), default=9e9))
        return tiers_of(recurring[k]), k, start_fee, f"AMBIGUOUS: {len(primary)} primaries"
    return {}, None, start_fee, f"AMBIGUOUS: {len(recurring)} recurring, no primary flag"


handles = [l.strip() for l in open("/tmp/ats_unnamed3.txt") if l.strip()]
out = []
for h in handles:
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
    cur = cps.effective(d.get("pricingInfos"), NOW) or {}
    events = (cur.get("pricingPerEvent", {}) or {}).get("actorChargeEvents", {}) or {}
    model = cur.get("pricingModel")
    ut, uk, fee, note = unit_price(events)
    if not d.get("pricingInfos") or model == "FREE":
        ut, uk, note = {"FREE": 0.0}, None, "FREE model / no pricing record -- $0"
    undercuts = sorted(t for t in ut if t in OURS and ut[t] < OURS[t])
    out.append({
        "handle": h,
        "title": d.get("title"),
        "users": (d.get("stats") or {}).get("totalUsers"),
        "model": model,
        "unit_event": uk,
        "unit_tiers": ut,
        "start_fee": fee,
        "note": note,
        "undercuts_tiers": undercuts,
        "every_tier": bool(ut) and all(t in OURS and ut[t] < OURS[t] for t in ut),
        "desc": (d.get("description") or "")[:500],
    })

json.dump(out, open("/tmp/ats_prices3.json", "w"), indent=1)
print(f"priced {len(out)} listings -> /tmp/ats_prices3.json")
for o in out:
    print(o["handle"], o.get("users"), o.get("model"), o.get("unit_tiers"), o.get("undercuts_tiers"), o.get("note"))
