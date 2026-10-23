#!/root/agent/venv/bin/python
"""Cycle 2132: live-price the FULL unnamed tail of hacker-news-scraper's niche
(fourteenth sweep). Successor to bin/_batch_price_hn.py (cycle 1344), which still
used check-price-superiority's one-number headline_price() and so could not see a
multi-event rival's cheap leg or a tier ladder; this copy is a byte-for-byte port of
bin/_batch_price_substack.py (the newest shape: shared bin/_unit_price.py reader,
retrying get_data, runfee crossover, every-event/every-tier dump) repointed at the
HN handle list, so the batch agrees with the fleet checkers instead of re-deriving
pricing rules.

Our own live price (the 'result' event, re-verified by check-own-price-freshness at
the top of cycle 2132: 25 Actors, 0 flags): 0.0002 FREE / 0.00017 BRONZE /
0.00013 SILVER / 0.0001 GOLD+, no start fee. OURS below is the FREE tier.

Input:  /tmp/hn_unnamed_handles.txt (the NONE section of bin/niche-unnamed)
Output: /tmp/hn_prices2.json
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
tiers_of = up.tiers_of
unit_price = up.unit_price

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

OURS = 0.0002  # our FREE-tier per-row price; ladder 0.0002/0.00017/0.00013/0.0001 GOLD+, no start fee

handles = [l.strip() for l in open("/tmp/hn_unnamed_handles.txt") if l.strip()]
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
    cur = cps.effective(d.get("pricingInfos"), NOW) or {}
    events = (cur.get("pricingPerEvent", {}) or {}).get("actorChargeEvents", {}) or {}
    model = cur.get("pricingModel")
    ut, uk, fee, note = unit_price(events)
    if not d.get("pricingInfos") or model == "FREE":
        ut, uk, note = {"FREE": 0.0}, None, "FREE model / no pricing record -- $0"
    future = [{"startedAt": p.get("startedAt"), "model": p.get("pricingModel")}
              for p in (d.get("pricingInfos") or [])
              if p.get("startedAt") and p["startedAt"] > NOW.isoformat()]
    undercuts = sorted(t for t, v in ut.items() if v < OURS)
    # h1392: a PURE run-fee rival has no per-row event at all, so `ut`/`undercuts` are
    # silent about a flat fee that buys a whole run.
    runfee, runfee_label = cps.runfee_price(d, NOW)
    crossover = round(runfee / OURS) if runfee else None
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
        "every_tier": bool(ut) and all(v < OURS for v in ut.values()),
        "future_pricing": future,
        "events": {k: {"tiers": tiers_of(v), "primary": v.get("isPrimaryEvent"),
                       "onetime": v.get("isOneTimeEvent"), "title": v.get("eventTitle")}
                   for k, v in events.items()},
        "desc": (d.get("description") or "")[:500],
    })
    if i % 20 == 0:
        print(f"  ...{i}/{len(handles)}", file=sys.stderr)

json.dump(out, open("/tmp/hn_prices2.json", "w"), indent=1)
amb = [o for o in out if "AMBIGUOUS" in (o.get("note") or "")]
rf = [o for o in out if o.get("runfee")]
print(f"priced {len(out)} listings -> /tmp/hn_prices2.json ({len(amb)} ambiguous, need hand-reading; {len(rf)} pure run-fee)")
