#!/root/agent/venv/bin/python
"""Cycle 1397: live-price the unnamed tail of uk-find-a-tender-scraper's niche.

Repointed to the shared bin/_unit_price.py (closes this Actor's slice of
0-TODO-h1396-repoint-batch-pricers) instead of this file's own hand-rolled
tiers_of/unit_price, which classified start fees purely on isOneTimeEvent and so
lacked the cycle-1396 tier-ladder discriminator and the apify-actor-start override.

OURS: tiered $0.003/result (FREE) -> $0.0028 (BRONZE) -> $0.0026 (SILVER) -> $0.0025 (GOLD+),
no start fee, first 25 rows/run free -- re-verified live at the top of cycle 1397 against the
actor's own pricingInfos record (0 drift from meta.json, check-own-price-freshness 24/0).
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

sys.path.insert(0, os.path.join(ROOT, "bin"))
import _unit_price as up  # noqa: E402

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

OURS = {"FREE": 0.003, "BRONZE": 0.0028, "SILVER": 0.0026, "GOLD": 0.0025,
        "PLATINUM": 0.0025, "DIAMOND": 0.0025}

tiers_of = up.tiers_of
unit_price = up.unit_price

handles = [l.strip() for l in open("/tmp/uktft_unnamed3.txt") if l.strip()]
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

json.dump(out, open("/tmp/uktft_prices2.json", "w"), indent=1)
print(f"priced {len(out)} listings -> /tmp/uktft_prices2.json")
for o in out:
    print(o["handle"], o.get("users"), o.get("model"), o.get("unit_tiers"), o.get("undercuts_tiers"), o.get("note"))
