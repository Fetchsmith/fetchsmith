#!/root/agent/venv/bin/python
"""Cycle 2821: live-price the unnamed tail of uk-find-a-tender-scraper's niche.

Replaces bin/_batch_price_uktft2.py (cycle 1397/1491), which carried the c2796
argv-default trap: both input (`/tmp/uktft_unnamed3.txt`) and output
(`/tmp/uktft_prices2.json`) paths hardcoded, no argv override, no `persist_sweep`
call. Same defect shape as apc/fda/sit/ggs/ted/fedreg/sgos before each got a
numbered replacement.

Follows the _batch_price_sgos3.py/_batch_price_fedreg2.py pattern: both paths are
required args (a bare run exits 1), the cohort size is printed for the mandatory
cross-check against niche-unnamed's own '--- N unnamed of M matched ---' line, our
own live price is re-read before anything is compared to it, and the sweep is
persisted to state/audit_data/.

OURS here is a TIERED ladder (not flat), so this copy keeps uktft2's
up.undercut_tiers/up.beats_every_tier comparison rather than the sgos3
floor/entry scalar shape -- re-read live below, not hardcoded.
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

if len(sys.argv) < 3:
    sys.exit("usage: _batch_price_uktft3.py <handles-file> <out-file> -- "
             "pass an explicit fresh niche-unnamed handle list, see queue.md c2796")
HANDLES_FILE, OUT_FILE = sys.argv[1], sys.argv[2]
OURS_HANDLE = "fetchsmith/uk-find-a-tender-scraper"

_u, _n = OURS_HANDLE.split("/", 1)
_ours = get_data(f"{API}/acts/{_u}~{_n}", headers=H)
_ocur = cps.effective(_ours.get("pricingInfos"), NOW) or {}
_oev = (_ocur.get("pricingPerEvent", {}) or {}).get("actorChargeEvents", {}) or {}
OURS_TIERS, _ok, _ofee, _onote = up.unit_price(_oev)
if not OURS_TIERS:
    sys.exit(f"cannot read our own live unit price ({_onote}) -- refusing to compare")
OURS_GOLD = OURS_TIERS.get("GOLD") or min(OURS_TIERS.values())
print(f"our live price: tiers={OURS_TIERS} entry_fee={_ofee} event={_ok}", file=sys.stderr)

handles = [l.strip() for l in open(HANDLES_FILE) if l.strip()]
print(f"cohort: {len(handles)} handle(s) from {HANDLES_FILE} -- cross-check this count "
      f"against niche-unnamed's own '--- N unnamed of M matched ---' line", file=sys.stderr)

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
    ut, uk, fee, note = up.unit_price(events)
    if not d.get("pricingInfos") or model == "FREE":
        ut, uk, note = {"FREE": 0.0}, None, "FREE model / no pricing record -- $0"
    undercuts = up.undercut_tiers(ut, OURS_TIERS)
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
        "every_tier": up.beats_every_tier(ut, OURS_TIERS),
        "desc": (d.get("description") or "")[:500],
    })

json.dump(out, open(OUT_FILE, "w"), indent=1)
up.persist_sweep("uktft", out)
rf = [o for o in out if o.get("runfee")]
et = [o for o in out if o.get("every_tier")]
print(f"priced {len(out)} listings -> {OUT_FILE} "
      f"({len(et)} every-tier undercutters, {len(rf)} pure run-fee)")
for o in out:
    print(o["handle"], o.get("users"), o.get("model"), o.get("unit_tiers"), o.get("undercuts_tiers"), o.get("note"))
