#!/root/agent/venv/bin/python
"""Cycle 1351: live-price the FULL unnamed tail of substack-scraper's niche.
The >=3-user cut at this cycle's niche-unnamed sweep was thin (only 1 of 115
unnamed listings has >=3 users), so per the standing full-cohort rule the whole
115-listing tail is priced end to end, 0-2-user floor included, no top-N cut.

Repointed to the shared bin/_unit_price.py (closes this Actor's slice of
0-TODO-h1396-repoint-batch-pricers) instead of this file's own hand-rolled
tiers_of/unit_price, which classified start fees purely on isOneTimeEvent and so
lacked both the cycle-1388 apify-actor-start override and the cycle-1396
tier-ladder discriminator.

Our own live price (full-text post, the 'result' event, re-verified live at the
top of cycle 1351): 0.002 FREE -> 0.00078 GOLD+. This is a multi-event product
(also post-metadata/leaderboard-row/comment) -- OURS below is the result event
only; metadata-only rivals need separate hand comparison against our 0.00112->
0.00039 post-metadata ladder, noted per-listing in `desc` for hand reading.
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
tiers_of = up.tiers_of
unit_price = up.unit_price

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

OURS = 0.002  # our FREE-tier "result" (full-text post) price; GOLD+ floor is 0.00078

handles = [l.strip() for l in open("/tmp/substack_unnamed_handles.txt") if l.strip()]
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
        "every_tier": bool(ut) and all(v < OURS for v in ut.values()),
        "future_pricing": future,
        "events": {k: {"tiers": tiers_of(v), "primary": v.get("isPrimaryEvent"),
                       "onetime": v.get("isOneTimeEvent"), "title": v.get("eventTitle")}
                   for k, v in events.items()},
        "desc": (d.get("description") or "")[:500],
    })
    if i % 20 == 0:
        print(f"  ...{i}/{len(handles)}", file=sys.stderr)

json.dump(out, open("/tmp/substack_prices.json", "w"), indent=1)
amb = [o for o in out if "AMBIGUOUS" in (o.get("note") or "")]
print(f"priced {len(out)} listings -> /tmp/substack_prices.json ({len(amb)} ambiguous, need hand-reading)")
