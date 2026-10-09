#!/root/agent/venv/bin/python
"""Cycle 1472: live-price the full 72-listing unnamed tail of clinicaltrials-scraper's niche.

Rotation audit (1435 -> 1472). niche-size: 128 matched of 145 seen (1329 saw 74 unnamed);
niche-unnamed: 72 unnamed of 128, README already names 61 handles. NOTE: the entire unnamed
cohort sits at 1-2 users this time -- there is no >=3-user head at all -- so per the cycle-1260
full-cohort rule every one of the 72 is priced, including the three whose titles advertise a
price outright ("No Login, $3/1k", "$3.5/1k", "$5/1k").

OURS: FLAT $0.0015/result on every plan tier, single `result` event, NO start fee --
re-verified live at the top of this cycle via check-own-price-freshness (24 Actors, 0 flags).
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

OURS = {t: 0.0015 for t in ("FREE", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND")}

tiers_of = up.tiers_of
unit_price = up.unit_price

handles = [l.strip() for l in open("/tmp/cts_unnamed.txt") if l.strip()]
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
    # Scheduled future price changes are invisible to every tool that filters
    # startedAt <= now (cycle 1260 reading rule (a)); surface them here.
    future = [{"startedAt": p.get("startedAt"), "model": p.get("pricingModel")}
              for p in (d.get("pricingInfos") or [])
              if p.get("startedAt") and p["startedAt"] > NOW.isoformat()]
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
        "future_pricing": future,
        "desc": (d.get("description") or "")[:500],
    })

json.dump(out, open("/tmp/cts_prices.json", "w"), indent=1)
print(f"priced {len(out)} listings -> /tmp/cts_prices.json")
for o in out:
    print(o["handle"], o.get("users"), o.get("model"), o.get("unit_tiers"),
          o.get("undercuts_tiers"), o.get("start_fee"), o.get("note"))
