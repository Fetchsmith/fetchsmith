#!/root/agent/venv/bin/python
"""Cycle 1398: live-price the full 31-listing unnamed tail of trademark-search-scraper's
niche (117 matched default / 91 strict, up from 114/88 at cycle 1360; README names 86).
The >=3-total-user cohort is thin (8 of 31), so per the standing full-cohort rule the whole
31-listing tail is priced, noise listings included -- a title/owner is not a scope verdict.

Repointed to the shared bin/_unit_price.py (closes this Actor's slice of
0-TODO-h1396-repoint-batch-pricers) instead of _batch_price_tms2.py's own hand-rolled
tiers_of/unit_price, which classified start fees purely on isOneTimeEvent and so lacked the
cycle-1396 tier-ladder discriminator and the apify-actor-start override.

OURS: FLAT $0.002/result on every plan tier, single `result` event (isPrimaryEvent), NO start
fee -- re-verified live at the top of cycle 1398 via check-own-price-freshness (24/0, 0 drift).
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

OURS = {t: 0.002 for t in ("FREE", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND")}

tiers_of = up.tiers_of
unit_price = up.unit_price

handles = [l.strip() for l in open("/tmp/tm_unnamed2.txt") if l.strip()]
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

json.dump(out, open("/tmp/tm_prices2.json", "w"), indent=1)
print(f"priced {len(out)} listings -> /tmp/tm_prices2.json")
for o in out:
    print(o["handle"], o.get("users"), o.get("model"), o.get("unit_tiers"), o.get("undercuts_tiers"), o.get("note"))
