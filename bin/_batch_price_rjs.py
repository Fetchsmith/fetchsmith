#!/root/agent/venv/bin/python
"""Live-price remote-jobs-scraper's unnamed niche tail.

OURS: tiered $0.0015/job (FREE) -> $0.0013 (BRONZE) -> $0.0011 (SILVER) -> $0.001
(GOLD+), single `job` event, no start fee -- re-verified live at the top of cycle
1424 (0 drift since 2026-09-21, agrees with check-own-price-freshness 24/0).

Cycle 1312/1354/1393 ran this file against only the >=3-user cut of the unnamed
tail (108 -> 127 listings). Cycle 1424 runs the FULL 344-listing tail, which is
what queue.md has been calling the owed "h1412-style full-cohort resweep": Apify
pins a new listing at 2 users, so a >=3-user cut selects for listing AGE, not
competitive threat, and in this niche (344 unnamed of 435 matched, overwhelmingly
1-2u) that is where a new undercutter is invisible by construction.

Cycle 1424 also closed this copy's leg of `0-TODO-h1392-runfee-in-batch-copies`
and brought it up to the current batch-pricer shape, the same three changes
cycles 1412/1420 made to the gprs/asr copies:
  * `_unit_price` -- this file previously used `cps.headline_price`, which
    collapses a tiered rival to ONE number, so every tiered comparison had to be
    hand-read out of `raw_events` by the auditing cycle. The shared module returns
    the whole per-tier map, so a rival that only undercuts at GOLD is visible
    without hand-reading, and it carries the cycle-1388 apify-actor-start override
    and the cycle-1396 tier-ladder discriminator this file never had.
  * `runfee` -- a PURE run-fee rival (every charge event run-scoped) has an EMPTY
    per-row tier map here, so `undercuts_tiers`/`every_tier` both come back empty
    and the listing reads as "no threat" when its flat fee buys a WHOLE RUN. At
    our $0.001/job a $0.05 flat fee undercuts us past 50 jobs, i.e. on nearly
    every real export. `cps.runfee_price` (cycle 1392) holds that shape out of the
    per-row comparison and returns an exact crossover (their fee / our GOLD unit
    price), exact because a one-time event bills at most once per run.
  * `get_json` -- the old unguarded `httpx.get(...).json()` turned one transient
    non-JSON body into `error: unresolvable`, i.e. a rival that silently drops out
    of the comparison (the cycle-1404 shape-(b) SILENT SKIP). 401/403/404/410
    still resolve immediately without retrying: a delisted rival is a final answer.
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

_path = os.path.join(ROOT, "bin/check-price-superiority")
spec = importlib.util.spec_from_loader("cps", importlib.machinery.SourceFileLoader("cps", _path))
cps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cps)

import _unit_price as up  # noqa: E402
tiers_of = up.tiers_of
unit_price = up.unit_price

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

OURS = {"FREE": 0.0015, "BRONZE": 0.0013, "SILVER": 0.0011, "GOLD": 0.001,
        "PLATINUM": 0.001, "DIAMOND": 0.001}
# crossover is quoted against the tier a bulk buyer actually pays on
OURS_GOLD = OURS["GOLD"]

handles = [l.strip() for l in open(sys.argv[1] if len(sys.argv) > 1
                                   else "/tmp/rjs_unnamed_all.txt") if l.strip()]
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
    elif not cur:
        # Cycle 1424: pricingInfos is non-empty but NOTHING is in effect yet -- every
        # entry is future-dated. The listing is free to run RIGHT NOW, which is the
        # cheapest a rival can be, and is the exact sibling of the cycle-1269 bug
        # (`pricingInfos: null` read as missing data instead of $0). `cps.effective`
        # returns None here and `cps.headline_price` answers (None, "no pricing in
        # effect"), i.e. check-price-superiority SKIPS such a rival fleet-wide --
        # see 0-TODO-h1424-future-only-pricing-skipped. Found on a real listing:
        # lanternlane-data/remote-jobs-aggregator, created 2026-10-08, exact 7-board
        # parity with us, free until its 2026-10-22 PAY_PER_EVENT entry starts.
        nxt = sorted(p["startedAt"] for p in d["pricingInfos"] if p.get("startedAt"))
        ut, uk, note = ({"FREE": 0.0}, None,
                        f"no pricing in effect yet -- free to run now, priced from {nxt[0]}")
    future = [{"startedAt": p.get("startedAt"), "model": p.get("pricingModel")}
              for p in (d.get("pricingInfos") or [])
              if p.get("startedAt") and p["startedAt"] > NOW.isoformat()]
    undercuts = sorted(t for t in ut if t in OURS and ut[t] < OURS[t])
    # h1392: a PURE run-fee rival has no per-row event at all, so `ut` is empty and
    # `undercuts`/`every_tier` are silent about a flat fee that buys a whole run.
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
        "every_tier": bool(ut) and all(t in OURS and ut[t] < OURS[t] for t in ut),
        "future_pricing": future,
        "events": {k: {"tiers": tiers_of(v), "primary": v.get("isPrimaryEvent"),
                       "onetime": v.get("isOneTimeEvent"), "title": v.get("eventTitle")}
                   for k, v in events.items()},
        "desc": (d.get("description") or "")[:500],
    })
    if i % 25 == 0:
        print(f"  ...{i}/{len(handles)}", file=sys.stderr, flush=True)

json.dump(out, open("/tmp/rjs_prices.json", "w"), indent=1)
amb = [o for o in out if "AMBIGUOUS" in (o.get("note") or "")]
rf = [o for o in out if o.get("runfee")]
bad = [o for o in out if o.get("error")]
print(f"priced {len(out)} listings -> /tmp/rjs_prices.json "
      f"({len(amb)} ambiguous, need hand-reading; {len(rf)} pure run-fee; "
      f"{len(bad)} unresolvable)")
