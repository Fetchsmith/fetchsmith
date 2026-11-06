#!/root/agent/venv/bin/python
"""Cycle 2818: live-price the unnamed tail of federal-register-scraper's niche.

Replaces bin/_batch_price_fedreg.py (cycle 1311), which carried the c2796 argv-default
trap: both input (`/tmp/fedreg_unnamed_handles.txt`) and output
(`/tmp/fedreg_prices.json`) paths hardcoded, no argv override, no `persist_sweep` call.
Same defect shape as apc/fda/sit/ggs/ted before each got a "2" replacement -- now
6-for-7 audits carrying it.

Follows the _batch_price_apc2.py pattern: both paths are required args (a bare run
exits 1), the cohort size is printed for the mandatory cross-check against
niche-unnamed's own `--- N unnamed of M matched ---` line, our own live price is
re-read before anything is compared to it, and the sweep is persisted to
state/audit_data/.

Our own price here is FLAT ($0.0008/result, no start fee, no eventTieredPricingUsd --
c2481 confirmed this precedes the c2464 scalar-vs-rung bug entirely), so entry == floor.
"""
import datetime
import importlib.machinery
import importlib.util
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

if len(sys.argv) < 3:
    sys.exit("usage: _batch_price_fedreg2.py <handles-file> <out-file> -- "
             "pass an explicit fresh niche-unnamed handle list, see queue.md c2796")
HANDLES_FILE, OUT_FILE = sys.argv[1], sys.argv[2]
OURS_HANDLE = "fetchsmith/federal-register-scraper"

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
print(f"cohort: {len(handles)} handle(s) from {HANDLES_FILE} -- cross-check this count "
      f"against niche-unnamed's own '--- N unnamed of M matched ---' line", file=sys.stderr)
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

import json
json.dump(out, open(OUT_FILE, "w"), indent=1)
up.persist_sweep("fedreg", out)
amb = [o for o in out if "AMBIGUOUS" in (o.get("note") or "")]
rf = [o for o in out if o.get("runfee")]
bf = [o for o in out if o.get("below_floor")]
print(f"priced {len(out)} listings -> {OUT_FILE} "
      f"({len(bf)} with a tier below our floor, {len(amb)} ambiguous need hand-reading, "
      f"{len(rf)} pure run-fee)")
