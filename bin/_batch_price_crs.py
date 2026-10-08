#!/root/agent/venv/bin/python
"""Cycle 1400: live-price the full 107-listing unnamed tail of court-records-scraper's niche.

WHY THE COHORT JUMPED. This niche had never been promoted into bin/niche-size's
TERM_VARIANTS/MATCH_SYNONYMS, so every sweep since cycle 1280 ran on the single
auto-generated base phrase "court records" and reported 30 matched / 0 unnamed -- which
cycle 1362 recorded as "completeness holds". It did not. The niche's own vocabulary is
"courtlistener" / "pacer" / "recap" / "docket" / "case law" / "court opinion", and a
listing titled "CourtListener Scraper - US Case Law & Opinions" whose copy never writes
the two contiguous words "court records" could not match by construction. A 20-term sweep
with those synonyms sees 682 distinct listings and 144 matched -- 4.8x the old count --
with 107 the README has never named. Same failure mode as cycle 1124's federal-register
24 -> 90 and cycle 1152's eu-ted sweep.

Per the standing full-cohort rule (cycle 1260) the WHOLE 107-listing tail is priced, not
just the >=3-user head: a title is the vendor's marketing angle, not a scope verdict, and
any exclusion has to come off the live description. Built on the shared bin/_unit_price.py
from the start (0-TODO-h1396-repoint-batch-pricers), so it carries the cycle-1350 nested
tier shape, the cycle-1388 apify-actor-start override and the cycle-1396 tier-ladder
discriminator.

OURS: FLAT $0.002/result on every plan tier, single `result` event, NO start fee --
re-verified live at the top of this cycle via check-own-price-freshness (24 Actors, 0 flags).
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

sys.path.insert(0, os.path.join(ROOT, "bin"))
import _unit_price as up  # noqa: E402

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

OURS = {t: 0.002 for t in ("FREE", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND")}

tiers_of = up.tiers_of
unit_price = up.unit_price

handles = [l.strip() for l in open("/tmp/crs_unnamed.txt") if l.strip()]
out = []
for h in handles:
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
    # Scheduled future price changes are invisible to every tool that filters
    # startedAt <= now (cycle 1260 reading rule (a)); surface them here.
    future = [{"startedAt": p.get("startedAt"), "model": p.get("pricingModel")}
              for p in (d.get("pricingInfos") or [])
              if p.get("startedAt") and p["startedAt"] > NOW.isoformat()]
    undercuts = sorted(t for t in ut if t in OURS and ut[t] < OURS[t])
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
        "every_tier": bool(ut) and all(t in OURS and ut[t] < OURS[t] for t in ut),
        "future_pricing": future,
        "desc": (d.get("description") or "")[:500],
    })

json.dump(out, open("/tmp/crs_prices.json", "w"), indent=1)
print(f"priced {len(out)} listings -> /tmp/crs_prices.json")
for o in out:
    print(o["handle"], o.get("users"), o.get("model"), o.get("unit_tiers"),
          o.get("undercuts_tiers"), o.get("start_fee"), o.get("note"))
