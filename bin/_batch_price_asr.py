#!/root/agent/venv/bin/python
"""Cycle 1350: live-price the FULL unnamed tail (0-2-user floor included) of
app-store-reviews-scraper's niche -- cycle 1306 only live-priced the 2 listings
with >=3 users and left the other 120 unchecked, which the eu-ted-tenders-scraper
sweep (cycle 1348) showed is exactly where undercutters hide in a mostly-new niche.

Same isPrimaryEvent-safe unit_price() logic as bin/_batch_price_ted.py (see that
file's docstring for the full rule set) -- copied rather than imported pending the
0-TODO-h1348-backport-unit-price-helper shared-module task.
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

# our own live price, flat per review, re-verified live at the top of cycle 1350
OURS = 0.0001
TIERS = ("FREE", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND")


def tiers_of(ev):
    """All tier prices for one charge event. Apify uses two different shapes for
    eventTieredPricingUsd across listings -- {"FREE": 0.006, ...} (flat float, what
    bin/_batch_price_ted.py's version of this function assumed) and
    {"FREE": {"tieredEventPriceUsd": 0.006}, ...} (nested dict, found cycle 1350 on
    36/122 of this niche's unnamed tail) -- and the flat-only version silently
    returned {} (no undercut, no AMBIGUOUS, just invisible) on every nested-shape
    listing. Handle both."""
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


handles = [l.strip() for l in open("/tmp/asr_unnamed_handles.txt") if l.strip()]
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

json.dump(out, open("/tmp/asr_prices.json", "w"), indent=1)
amb = [o for o in out if "AMBIGUOUS" in (o.get("note") or "")]
print(f"priced {len(out)} listings -> /tmp/asr_prices.json ({len(amb)} ambiguous, need hand-reading)")
