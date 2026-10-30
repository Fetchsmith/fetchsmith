#!/root/agent/venv/bin/python
"""Cycle 2468: live-price the FULL unnamed tail of hacker-news-scraper's niche
(fifteenth sweep). Supersedes bin/_batch_price_hn2.py (cycle 2132), which supersedes
bin/_batch_price_hn.py (cycle 1344).

Why this copy exists -- the c2464 HIGH follow-up, ported for THIS niche:
hn2's `OURS` was a single scalar (our FREE rate, 0.0002) and every rival RUNG was
compared against it, so a rival with a tier ladder reads as an undercutter whenever its
GOLD rung dips under our FREE rung -- even when it is DEARER than us at the rung a given
buyer actually pays. An Apify tier is the BUYER's plan, not the seller's discount.
c2132 caught this by hand ("KEY METHOD CORRECTION ... cutting 11 raw hits to the real
set"); this script does it in code via cps.tier_price_at, rung for rung, and KEEPS the
old scalar flag alongside purely to measure the over-flag factor (substack2's shape).

Also closes, for this niche, c2466's open item (a): the AMBIGUOUS / unresolvable / no-
recurring-event listings are PRINTED as a required hand-read list, not summarised as a
count, because up.unit_price returns {} for a multi-event rival with no isPrimaryEvent
flag and that path DROPS listings from the findings (under-reporting, the unsafe
direction) instead of over-flagging them.

Our live price, re-verified live at the top of this cycle (unchanged since 2026-09-26,
so unchanged since the last audit at cycle 2132), single recurring event:
  result   FREE 0.0002 / BRONZE 0.00017 / SILVER 0.00013 / GOLD+ 0.0001, no start fee.

Input:  /tmp/hn_unnamed_handles.txt (the NONE section of bin/niche-unnamed)
Output: /tmp/hn_prices3.json  +  state/audit_data/c<cycle>_hn_prices.json (c2149 mandate)
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

OURS_HANDLE = "fetchsmith/hacker-news-scraper"
_u, _n = OURS_HANDLE.split("/", 1)
_ours = get_data(f"{API}/acts/{_u}~{_n}", headers=H)
_oev = (cps.effective(_ours.get("pricingInfos"), NOW) or {}).get(
    "pricingPerEvent", {}).get("actorChargeEvents", {}) or {}
OUR_RESULT = up.tiers_of(_oev["result"])
OUR_ENTRY = max(OUR_RESULT.values())   # our FREE rung -- the legacy scalar, kept to measure
OUR_FLOOR = min(OUR_RESULT.values())   # our GOLD+ rung -- used for run-fee crossover
print(f"our result ladder: {OUR_RESULT}", file=sys.stderr)


def rung_cmp(ut, our):
    """Rung-for-rung verdict: which tiers the rival undercuts US at, counting only rungs
    where BOTH sides publish a comparable number (cps.tier_price_at: a flat single-rung
    ladder applies at every tier; a multi-rung ladder missing a key yields None)."""
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
        # rung-for-rung (the honest read: c2460 steam / c2464 substack lesson)
        "cmp_vs_result": rung_cmp(ut, OUR_RESULT),
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

json.dump({"our_result_ladder": OUR_RESULT, "listings": out},
          open("/tmp/hn_prices3.json", "w"), indent=1)
up.persist_sweep("hn", out)   # c2149 mandate -- hn2 and substack2 both still skip this

err = [o for o in out if o.get("error")]
rf = [o for o in out if o.get("runfee")]
ev = [o for o in out if o.get("cmp_vs_result", {}).get("every_rung")]
some = [o for o in out if o.get("cmp_vs_result", {}).get("cheaper_at")
        and not o["cmp_vs_result"]["every_rung"]]
lg = [o for o in out if o.get("legacy_every_tier_vs_our_FREE")]
print(f"priced {len(out)} -> /tmp/hn_prices3.json ({len(err)} unresolvable, {len(rf)} pure run-fee)")
print(f"every-rung undercutters (rung-for-rung): {len(ev)}   "
      f"legacy scalar-vs-our-FREE would have said: {len(lg)}")
print(f"some-rung-only undercutters: {len(some)}")

# c2466 item (a): the DROPPED bucket must be a hand-read LIST, never a count.
drop = [o for o in out if not o.get("error") and not o.get("unit_tiers")]
print(f"\n=== HAND-READ REQUIRED: {len(drop)} listing(s) with NO resolved per-row ladder ===")
print("(up.unit_price returned {} -- AMBIGUOUS multi-event/no-primary-flag, or no recurring"
      " event at all. This path DROPS listings from the verdict, so it UNDER-reports.)")
for o in drop:
    print(f"  {o['handle']:<55} users={o.get('users')} note={o.get('note')!r}")
    for k, v in (o.get("events") or {}).items():
        print(f"      event {k!r:<28} tiers={v['tiers']} primary={v['primary']} "
              f"onetime={v['onetime']}")
for o in err:
    print(f"  {o['handle']:<55} UNRESOLVABLE")
