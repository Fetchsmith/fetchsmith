#!/root/agent/venv/bin/python
"""Cycle 1804: live-price the unnamed tail of fda-recall-scraper's niche.

Replaces bin/_batch_price_fda.py, which is one of the pre-1396 divergent copies: it
printed every charge event and left the "which event is the real per-row price"
judgment to the reader, which is exactly the trap LEARNINGS records at cycles 1336 /
1347 (a one-time apify-actor-start fee or a vestigial secondary dataset-item event
read as the rival's unit price -> 8 false positives in one sweep). This copy decides
in code via the shared bin/_unit_price.py, closing fda's slice of
0-TODO-h1396-repoint-batch-pricers, and carries the cycle-1491 run-fee port
(0-TODO-h1392-runfee-in-batch-copies) that the old copy also lacks.

Our own price here is TIERED (unlike ted's flat $0.0015), so a single "undercuts"
boolean is not enough: a rival between our floor and our entry undercuts only
small-volume buyers. Reported as two fields -- below_floor (undercuts us at ANY
volume, the real threat) and below_entry (undercuts our first tier only).
Both of our numbers are re-verified live at the top of the run, not trusted from
registry.json, so a drifted registry cannot silently relax the comparison.
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

HANDLES_FILE = sys.argv[1] if len(sys.argv) > 1 else "/tmp/c1804_fda_ge3.txt"
OUT_FILE = sys.argv[2] if len(sys.argv) > 2 else "/tmp/c1804_fda_prices.json"
OURS_HANDLE = "fetchsmith/fda-recall-scraper"

# --- re-verify OUR live price before comparing anything to it ---
_u, _n = OURS_HANDLE.split("/", 1)
_ours = get_data(f"{API}/acts/{_u}~{_n}", headers=H)
_ocur = cps.effective(_ours.get("pricingInfos"), NOW) or {}
_oev = (_ocur.get("pricingPerEvent", {}) or {}).get("actorChargeEvents", {}) or {}
_ot, _ok, _ofee, _onote = unit_price(_oev)
if not _ot:
    sys.exit(f"cannot read our own live unit price ({_onote}) -- refusing to compare")
OURS_ENTRY = max(_ot.values())
OURS_FLOOR = min(_ot.values())
print(f"our live price: tiers={_ot} entry={OURS_ENTRY} floor={OURS_FLOOR} "
      f"event={_ok} start_fee={_ofee}", file=sys.stderr)

handles = [l.strip() for l in open(HANDLES_FILE) if l.strip()]
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
    # a rival with no pricing record at all, or on Apify's FREE model, bills $0 (cycle 1104)
    if not d.get("pricingInfos") or model == "FREE":
        ut, uk, note = {"FREE": 0.0}, None, "FREE model / no pricing record -- $0"
    # scheduled future entries are invisible to every tool that filters startedAt<=now
    future = [{"startedAt": p.get("startedAt"), "model": p.get("pricingModel")}
              for p in (d.get("pricingInfos") or [])
              if p.get("startedAt") and p["startedAt"] > NOW.isoformat()]
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
        "below_floor": sorted(t for t, v in ut.items() if v < OURS_FLOOR),
        "below_entry": sorted(t for t, v in ut.items() if v < OURS_ENTRY),
        "every_tier_below_floor": bool(ut) and all(v < OURS_FLOOR for v in ut.values()),
        "runfee": runfee,
        "runfee_label": runfee_label,
        "runfee_crossover_rows": round(runfee / OURS_FLOOR) if runfee else None,
        "future_pricing": future,
        "events": {k: {"tiers": tiers_of(v), "primary": v.get("isPrimaryEvent"),
                       "onetime": v.get("isOneTimeEvent"), "title": v.get("eventTitle")}
                   for k, v in events.items()},
        "desc": (d.get("description") or "")[:500],
    })
    if i % 20 == 0:
        print(f"  ...{i}/{len(handles)}", file=sys.stderr)

json.dump(out, open(OUT_FILE, "w"), indent=1)
amb = [o for o in out if "AMBIGUOUS" in (o.get("note") or "")]
rf = [o for o in out if o.get("runfee")]
bf = [o for o in out if o.get("below_floor")]
print(f"priced {len(out)} listings -> {OUT_FILE} "
      f"({len(bf)} with a tier below our floor, {len(amb)} ambiguous need hand-reading, "
      f"{len(rf)} pure run-fee)")
