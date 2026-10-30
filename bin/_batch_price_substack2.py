#!/root/agent/venv/bin/python
"""Cycle 2464: live-price the FULL unnamed tail of substack-scraper's niche (213 handles).

Supersedes bin/_batch_price_substack.py (cycle 1351/1491), which carried the bug cycle
2460 found and fixed for steam: its `OURS` was a single scalar (our FREE price, 0.002)
and every rival rung was compared against it. An Apify pricing tier is the BUYER's plan,
not the seller's discount, so that comparison reads a rival's GOLD rung against our FREE
rung and over-flags: a rival can sit below our FREE price at every rung while still being
dearer than us at the rung a given buyer actually pays. Here we compare RUNG FOR RUNG
through cps.tier_price_at (flat single-rung ladders apply at every tier; a genuinely
multi-rung ladder missing a key yields None rather than a guess).

Our live price, re-verified live at the top of this cycle (unchanged since 2026-09-18,
so unchanged since the last audit at cycle 2127):
  result (post w/ article text)  FREE 0.002   -> GOLD+ 0.00078
  post-metadata                  FREE 0.00112 -> GOLD+ 0.00039
  leaderboard-row                FREE 0.0015  -> GOLD+ 0.0005
  comment                        FREE 0.00056 -> GOLD+ 0.00019
  no start fee.
`result` is the headline event compared below. This is a MULTI-EVENT product: a rival that
only ships post metadata (no article text) must be hand-read against the post-metadata
ladder instead, so `cmp_vs_metadata` carries that second verdict per listing and `desc` is
retained for hand reading.
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
TIERS = ["FREE", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]

OURS_HANDLE = "fetchsmith/substack-scraper"
_u, _n = OURS_HANDLE.split("/", 1)
_ours = get_data(f"{API}/acts/{_u}~{_n}", headers=H)
_oev = (cps.effective(_ours.get("pricingInfos"), NOW) or {}).get(
    "pricingPerEvent", {}).get("actorChargeEvents", {}) or {}
OUR_RESULT = up.tiers_of(_oev["result"])
OUR_META = up.tiers_of(_oev["post-metadata"])
OUR_ENTRY = max(OUR_RESULT.values())
OUR_FLOOR = min(OUR_RESULT.values())
print(f"our result ladder: {OUR_RESULT}\nour metadata ladder: {OUR_META}", file=sys.stderr)


def rung_cmp(ut, our):
    """Rung-for-rung verdict: which tiers the rival undercuts US at, counting only rungs
    where BOTH sides publish a comparable number."""
    cheaper, dearer, compared = [], [], []
    for t in TIERS:
        rv = cps.tier_price_at(ut, t)
        ov = cps.tier_price_at(our, t)
        if rv is None or ov is None:
            continue
        compared.append(t)
        (cheaper if rv < ov else dearer).append(t)
    return {"compared": compared, "cheaper_at": cheaper, "dearer_at": dearer,
            "every_rung": bool(compared) and not dearer}


handles = [l.strip() for l in open("/tmp/substack_unnamed_handles.txt") if l.strip()]
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
    ut, uk, fee, note = up.unit_price(events)
    if not d.get("pricingInfos") or model == "FREE":
        ut, uk, note = {"FREE": 0.0}, None, "FREE model / no pricing record -- $0"
    runfee, runfee_label = cps.runfee_price(d, NOW)
    out.append({
        "handle": h,
        "title": d.get("title"),
        "users": (d.get("stats") or {}).get("totalUsers"),
        "model": model,
        "unit_event": uk,
        "unit_tiers": ut,
        "start_fee": fee,
        "note": note,
        # rung-for-rung (the honest read, cycle 2460 lesson)
        "cmp_vs_result": rung_cmp(ut, OUR_RESULT),
        "cmp_vs_metadata": rung_cmp(ut, OUR_META),
        # legacy scalar read, KEPT ONLY to measure how badly it over-flags vs rung-for-rung
        "legacy_every_tier_vs_our_FREE": bool(ut) and all(v < OUR_ENTRY for v in ut.values()),
        "runfee": runfee,
        "runfee_label": runfee_label,
        "runfee_crossover_rows": round(runfee / OUR_FLOOR) if runfee else None,
        "future_pricing": [{"startedAt": p.get("startedAt"), "model": p.get("pricingModel")}
                           for p in (d.get("pricingInfos") or [])
                           if p.get("startedAt") and p["startedAt"] > NOW.isoformat()],
        "events": {k: {"tiers": up.tiers_of(v), "primary": v.get("isPrimaryEvent"),
                       "onetime": v.get("isOneTimeEvent"), "title": v.get("eventTitle")}
                   for k, v in events.items()},
        "desc": (d.get("description") or "")[:500],
    })
    if i % 25 == 0:
        print(f"  ...{i}/{len(handles)}", file=sys.stderr)

json.dump({"our_result_ladder": OUR_RESULT, "our_metadata_ladder": OUR_META,
           "listings": out}, open("/tmp/substack_prices2.json", "w"), indent=1)
amb = [o for o in out if "AMBIGUOUS" in (o.get("note") or "")]
err = [o for o in out if o.get("error")]
rf = [o for o in out if o.get("runfee")]
ev = [o for o in out if o.get("cmp_vs_result", {}).get("every_rung")]
lg = [o for o in out if o.get("legacy_every_tier_vs_our_FREE")]
print(f"priced {len(out)} -> /tmp/substack_prices2.json ({len(err)} unresolvable, "
      f"{len(amb)} ambiguous, {len(rf)} pure run-fee)")
print(f"every-rung undercutters (rung-for-rung): {len(ev)}   "
      f"legacy scalar-vs-our-FREE would have said: {len(lg)}")
