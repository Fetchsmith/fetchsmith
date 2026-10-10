#!/root/agent/venv/bin/python
"""Cycle 1436: live-price ALL 51 matched listings in nih-reporter-scraper's niche --
the NAMED cohort, not the unnamed tail (which has been 0-unnamed for 4 consecutive
audits: 1330, 1366, 1404, 1436). Purpose is the blind spot check-price-superiority
documents on itself: its price_of() reads only the FREE tier of a tiered event, so a
named rival whose BRONZE/SILVER/GOLD/PLATINUM tier undercuts us is scored at its most
expensive tier and never flagged. Uses bin/_unit_price (tier-aware, start-fee-aware).

Cycle 1491: closes this copy's leg of 0-TODO-h1392-runfee-in-batch-copies (get_data retry,
cps.runfee_price, runfee_crossover_rows in the output -- same port as gprs/asr/rjs).
"""
import datetime
import importlib.machinery
import importlib.util
import json
import os
import sys

ROOT = "/root/agent"
sys.path.insert(0, os.path.join(ROOT, "bin"))
from _apify_get import ApifyGetError, get_data  # noqa: E402


def _load(name, path):
    spec = importlib.util.spec_from_loader(name, importlib.machinery.SourceFileLoader(name, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cps = _load("cps", os.path.join(ROOT, "bin/check-price-superiority"))
up = _load("up", os.path.join(ROOT, "bin/_unit_price.py"))

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)
OURS = 0.0015  # flat $0.0015/result, single `result` event, verified live this cycle

handles = [l.strip() for l in open("/tmp/nih_matched.txt") if l.strip()]
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
    tiers, key, start_fee, note = up.unit_price(events)
    # future-dated entries matter (cycle 1260 reading rule (a)): a listing that reads FREE
    # today can have a PAY_PER_EVENT entry already scheduled, invisible to startedAt<=now.
    future = [{"startedAt": p.get("startedAt"), "model": p.get("pricingModel")}
              for p in (d.get("pricingInfos") or [])
              if p.get("startedAt") and datetime.datetime.fromisoformat(
                  p["startedAt"].replace("Z", "+00:00")) > NOW]
    # h1392: a PURE run-fee rival has no per-row event at all, so `tiers` is empty and
    # the min/free-tier reads are silent about a flat fee that buys a whole run.
    runfee, runfee_label = cps.runfee_price(d, NOW)
    crossover = round(runfee / OURS) if runfee else None
    out.append({
        "handle": h,
        "title": d.get("title"),
        "users": (d.get("stats") or {}).get("totalUsers"),
        "model": cur.get("pricingModel"),
        "unit_tiers": tiers,
        "unit_key": key,
        "start_fee": start_fee,
        "note": note,
        "min_tier": min(tiers.values()) if tiers else None,
        "free_tier": tiers.get("FREE") if tiers else None,
        "runfee": runfee,
        "runfee_label": runfee_label,
        "runfee_crossover_rows": crossover,
        "future_pricing": future,
        "desc": (d.get("description") or "")[:400],
        "raw_events": events,
        "startedAt": cur.get("startedAt"),
    })
    if i % 10 == 0:
        print(f"  ...{i}/{len(handles)}", file=sys.stderr)

json.dump(out, open("/tmp/nih_prices.json", "w"), indent=1)
rf = [o for o in out if o.get("runfee")]
print(f"priced {len(out)} listings (ours ${OURS}/result) -> /tmp/nih_prices.json ({len(rf)} pure run-fee)")
