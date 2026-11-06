#!/root/agent/venv/bin/python
"""Cycle 2816: live-price the unnamed tail of apple-podcasts-scraper's niche.

Replaces bin/_batch_price_apc.py (cycle 1339), which carried the c2796 argv-default
trap in its WORST form -- not even an argv fallback, both input and output paths
hardcoded (`/tmp/apc_unnamed.txt`, `/tmp/apc_prices.json`), and c2480's input file
was still on disk, so a bare re-run would have silently re-priced a 336-cycle-old
cohort behind a normal-looking banner. Same shape as _batch_price_hn3.py before
c2804 fixed it. The old copy also never called `up.persist_sweep`, so every apc
sweep ever run was thrown away in /tmp, and it printed every charge event and left
the "which event is the per-row rate" judgment to the reader -- the LEARNINGS
c1336/c1347 trap that `bin/_unit_price.py` exists to decide in code.

This copy follows the _batch_price_fda2.py pattern: both paths are required args
(a bare run exits 1), the cohort size is printed for the mandatory cross-check
against niche-unnamed's own `--- N unnamed of M matched ---` line, our own live
price is re-read before anything is compared to it, and the sweep is persisted to
state/audit_data/.

Our own price here is FLAT ($0.001/result, no start fee, no tier map -- re-read
live each run, never trusted from registry.json), so entry == floor and the two
below_* fields collapse to the same answer; they are still both emitted so the
output shape matches every other niche's sweep and the selftest corpus stays
uniform. This niche is full of SPLIT-EVENT listings (a dearer podcast/show row
plus a cheaper episode row), so `events` keeps the full per-event tier map for the
hand-read pass -- `unit_price` picking one event is the comparison, not the record.
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

if len(sys.argv) < 3:
    sys.exit("usage: _batch_price_apc2.py <handles-file> <out-file> -- "
             "pass an explicit fresh niche-unnamed handle list, see queue.md c2796")
HANDLES_FILE, OUT_FILE = sys.argv[1], sys.argv[2]
OURS_HANDLE = "fetchsmith/apple-podcasts-scraper"

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
up.persist_sweep("apc", out)
amb = [o for o in out if "AMBIGUOUS" in (o.get("note") or "")]
rf = [o for o in out if o.get("runfee")]
bf = [o for o in out if o.get("below_floor")]
print(f"priced {len(out)} listings -> {OUT_FILE} "
      f"({len(bf)} with a tier below our floor, {len(amb)} ambiguous need hand-reading, "
      f"{len(rf)} pure run-fee)")
