#!/root/agent/venv/bin/python
"""Cycle 2828: live-price the FULL unnamed cohort of google-news-scraper's niche.

Rotation audit (2491 -> 2828, 337c gap). Replaces _batch_price_gn.py (c1303), which
carried BOTH known defects per the c2812 base-rate note: the c2796 argv-default trap
(hardcoded /tmp/gn_unnamed_handles.txt, frozen at c1303, no override possible) and a
missing up.persist_sweep call (sweep thrown away with /tmp). Copied from
_batch_price_cts5.py, which was already argv-clean and persist-clean.

ONE substantive change vs cts5: our google-news price is TIERED, not flat, so OURS is
our real ladder and the undercut tests go through up.undercut_tiers /
up.beats_every_tier (both flat-aware via expand_flat) instead of cts5's hand-rolled
`all(... for t in ut)`, which compares only the rungs the RIVAL happens to publish and
would call a flat-$0.0015 rival "every_tier" against a ladder it actually ties at SILVER
and loses to at FREE/BRONZE.

Usage: _batch_price_gn2.py HANDLES_FILE OUT_FILE
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

if len(sys.argv) != 3:
    sys.exit("usage: _batch_price_gn2.py HANDLES_FILE OUT_FILE -- see queue.md c2796")

HANDLES_FILE, OUT_FILE = sys.argv[1], sys.argv[2]

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

# Read live off fetchsmith~google-news-scraper's own pricingInfos this cycle, c2828.
OURS = {"FREE": 0.002, "BRONZE": 0.0018, "SILVER": 0.0015,
        "GOLD": 0.001, "PLATINUM": 0.001, "DIAMOND": 0.001}
OURS_GOLD = OURS["GOLD"]

unit_price = up.unit_price

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
    if not d.get("pricingInfos") or model == "FREE":
        ut, uk, note = {"FREE": 0.0}, None, "FREE model / no pricing record -- $0"
    future = [{"startedAt": p.get("startedAt"), "model": p.get("pricingModel")}
              for p in (d.get("pricingInfos") or [])
              if p.get("startedAt") and p["startedAt"] > NOW.isoformat()]
    try:
        undercuts = up.undercut_tiers(ut, OURS)
        every = up.beats_every_tier(ut, OURS)
        partial_err = None
    except ValueError as e:  # partial rival ladder -- decide by hand, do not guess
        undercuts, every, partial_err = [], False, str(e)
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
        "partial_ladder_error": partial_err,
        "runfee": runfee,
        "runfee_label": runfee_label,
        "runfee_crossover_rows": crossover,
        "every_tier": every,
        "future_pricing": future,
        "deprecated": bool(d.get("isDeprecated")),
        "desc": (d.get("description") or "")[:500],
    })
    if i % 50 == 0:
        print(f"  ...{i}/{len(handles)}", file=sys.stderr)

json.dump(out, open(OUT_FILE, "w"), indent=1)
saved = up.persist_sweep("gn", out)
rf = [o for o in out if o.get("runfee")]
bad = [o for o in out if o.get("error")]
pl = [o for o in out if o.get("partial_ladder_error")]
print(f"priced {len(out)} listings -> {OUT_FILE} (persisted {saved}); "
      f"{len(rf)} pure run-fee, {len(bad)} unresolvable, {len(pl)} partial-ladder")
for o in sorted(out, key=lambda x: (not x.get("every_tier"), -len(x.get("undercuts_tiers") or []))):
    if o.get("error"):
        continue
    if o.get("undercuts_tiers") or o.get("partial_ladder_error"):
        print(o["handle"], o.get("users"), o.get("model"), o.get("unit_tiers"),
              "UNDERCUTS", o.get("undercuts_tiers"), "every=", o.get("every_tier"),
              "start=", o.get("start_fee"), "runfee=", o.get("runfee"), "|", o.get("note"),
              o.get("partial_ladder_error") or "")
