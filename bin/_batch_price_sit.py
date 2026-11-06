#!/root/agent/venv/bin/python
"""Cycle 1336: live-price all 60 UNNAMED listings in sec-insider-trades-scraper niche (full tiered maps + user counts).

Cycle 2813: patched for the standing c2796 anti-stale-cohort rule -- both the input and
output paths were 100% hardcoded to /tmp with no argv override, the same defect found
and fixed on ggs2 (c2806), ted (c2810) and fda2 (c2812) -- now a 4-for-4 base rate on
this fleet's batch pricers. Both are now required args (bare run exits 1), and the
missing up.persist_sweep('sit', out) call (the c2149 mandate) is added.
"""
import datetime
import importlib.util
import importlib.machinery
import json
import os
import sys

import httpx

ROOT = "/root/agent"
_path = os.path.join(ROOT, "bin/check-price-superiority")
spec = importlib.util.spec_from_loader("cps", importlib.machinery.SourceFileLoader("cps", _path))
cps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cps)

sys.path.insert(0, os.path.join(ROOT, "bin"))
import _unit_price as up  # noqa: E402

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

if len(sys.argv) < 3:
    sys.exit("usage: _batch_price_sit.py <handles-file> <out-file> -- "
             "pass an explicit fresh niche-unnamed handle list, see queue.md c2796")
HANDLES_FILE, OUT_FILE = sys.argv[1], sys.argv[2]

handles = [l.strip() for l in open(HANDLES_FILE) if l.strip()]
print(f"cohort: {len(handles)} handle(s) from {HANDLES_FILE} -- cross-check this count "
      f"against niche-unnamed's own '--- N unnamed of M matched ---' line", file=sys.stderr)
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
    price, label = cps.headline_price(d, NOW)
    runfee, runfee_label = cps.runfee_price(d, NOW)
    cur = cps.effective(d.get("pricingInfos"), NOW) or {}
    events = (cur.get("pricingPerEvent", {}) or {}).get("actorChargeEvents", {}) or {}
    out.append({
        "handle": h,
        "title": d.get("title"),
        "users": (d.get("stats") or {}).get("totalUsers"),
        "price": price,
        "label": label,
        "runfee": runfee,
        "runfee_label": runfee_label,
        "model": cur.get("pricingModel"),
        "events": {k: {"usd": cps.price_of(v), "primary": v.get("isPrimaryEvent"),
                       "onetime": v.get("isOneTimeEvent"), "title": v.get("eventTitle")}
                   for k, v in events.items()},
        "desc": (d.get("description") or "")[:400],
        "raw_events": events,
        "tiered": {k: v.get("eventTieredPricingUsd") for k, v in events.items()},
        "startedAt": cur.get("startedAt"),
    })
    if i % 10 == 0:
        print(f"  ...{i}/{len(handles)}", file=sys.stderr)

json.dump(out, open(OUT_FILE, "w"), indent=1)
up.persist_sweep("sit", out)
print(f"priced {len(out)} listings -> {OUT_FILE}")
