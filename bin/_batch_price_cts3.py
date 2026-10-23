#!/root/agent/venv/bin/python
"""Cycle 2144: live-price the full 116-listing unnamed cohort of clinicaltrials-scraper's niche.

Rotation audit (1472 -> 2144, 672-cycle interval). niche-size: 182 matched of 337 seen (1472
saw 128 of 145 -- the niche grew ~42% in matched listings); niche-unnamed: 117 unnamed of 182
(109 NONE, 8 OWNER), README already names 69 handles. Unlike 1472 (where the entire unnamed
cohort sat at 1-2 users), there IS a >=3-user head this time -- 9 listings -- so the cycle-1260
rule bites on both halves: price the whole >=3 cohort AND never rule a listing out on its title.
All 116 (117 minus our own listing) are priced here, same as 1472 did for its 72.

OURS: FLAT $0.0015/result on every plan tier, single `result` event, NO start fee --
re-verified live at the top of this cycle via check-own-price-freshness + check-own-price-prose
(25 Actors, 0 flags each).
"""
import datetime
import importlib.machinery
import importlib.util
import json
import os
import sys

ROOT = "/root/agent"
_path = os.path.join(ROOT, "bin/check-price-superiority")
spec = importlib.util.spec_from_loader("cps", importlib.machinery.SourceFileLoader("cps", _path))
cps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cps)

sys.path.insert(0, os.path.join(ROOT, "bin"))
import _unit_price as up  # noqa: E402
from _apify_get import ApifyGetError, get_data  # noqa: E402

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

OURS = {t: 0.0015 for t in ("FREE", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND")}
OURS_GOLD = OURS["GOLD"]

tiers_of = up.tiers_of
unit_price = up.unit_price

handles = [l.strip() for l in open("/tmp/cts_unnamed.txt") if l.strip()]
out = []
for h in handles:
    u, n = h.split("/", 1)
    try:
        d = get_data(f"{API}/acts/{u}~{n}", headers=H)
    except ApifyGetError as e:
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
    # h1392: a PURE run-fee rival has no per-row event at all, so `ut`/`undercuts` are
    # silent about a flat fee that buys a whole run.
    runfee, runfee_label = cps.runfee_price(d, NOW)
    crossover = round(runfee / OURS_GOLD) if runfee else None
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
        "runfee": runfee,
        "runfee_label": runfee_label,
        "runfee_crossover_rows": crossover,
        "every_tier": bool(ut) and all(t in OURS and ut[t] < OURS[t] for t in ut),
        "future_pricing": future,
        "desc": (d.get("description") or "")[:500],
    })

json.dump(out, open("/tmp/cts_prices.json", "w"), indent=1)
rf = [o for o in out if o.get("runfee")]
print(f"priced {len(out)} listings -> /tmp/cts_prices.json ({len(rf)} pure run-fee)")
for o in out:
    print(o["handle"], o.get("users"), o.get("model"), o.get("unit_tiers"),
          o.get("undercuts_tiers"), o.get("start_fee"), o.get("note"))
