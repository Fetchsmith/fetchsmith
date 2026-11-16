#!/root/agent/venv/bin/python
"""Cycle 3286: live-read rows 155-160 of state/audit_data/c3162_vendor_catalogue.json
(the standing NEW c3162 vendor-catalogue triage) plus our own live prices for the
niches they touch.

Same method as c3255-c3283: cps.effective() for the live tier (never [-1],
which can be future-dated), every charge event enumerated, not just the primary.
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
from _apify_get import ApifyGetError, get_data  # noqa: E402

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

TIERS = ["FREE", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]

RIVALS = [
    "goat255/google-play-reviews-scraper",
    "informed_almandine_vzb/google-play-apps",
    "openharvest/google-news-scraper",
    "pink_comic/pubchem-compound-search",
    "publicmoney/bund-ausschreibungen-scraper",
    "rowcraft/shopify-products-scraper",
]
OURS = [
    "fetchsmith/google-play-reviews-scraper",
    "fetchsmith/google-news-scraper",
    "fetchsmith/nih-reporter-scraper",
    "fetchsmith/eu-ted-tenders-scraper",
    "fetchsmith/shopify-products-scraper",
]


def dump(handle):
    u, n = handle.split("/", 1)
    try:
        d = get_data(f"{API}/acts/{u}~{n}", headers=H)
    except ApifyGetError as e:
        print(f"ERR {handle}: {e}")
        return
    if not d:
        print(f"ERR {handle}: unresolvable")
        return
    pis = d.get("pricingInfos") or []
    cur = cps.effective(pis, NOW) or {}
    print("=" * 78)
    print(f"{handle}  users={d.get('stats', {}).get('totalUsers')} "
          f"public30d={(d.get('stats') or {}).get('publicActorRunStats30Days', {}).get('TOTAL')}")
    print(f"  title: {d.get('title')}")
    print(f"  desc : {(d.get('description') or '')[:700]}")
    print(f"  deprecated={d.get('isDeprecated')} public={d.get('isPublic')} "
          f"pricingInfos={len(pis)} entries pricingModel={d.get('pricingModel')}")
    for pi in pis:
        mark = "LIVE" if pi is cur else "    "
        print(f"  {mark} startedAt={pi.get('startedAt')} model={pi.get('pricingModel')}")
    ev = (cur.get("pricingPerEvent", {}) or {}).get("actorChargeEvents", {}) or {}
    if not ev:
        print(f"  LIVE non-PPE: trialMinutes={cur.get('trialMinutes')} "
              f"pricePerUnitUsd={cur.get('pricePerUnitUsd')} "
              f"monthly={cur.get('pricingPerEvent') or cur.get('pricePerUnitUsd')}")
        print("  raw:", json.dumps({k: v for k, v in cur.items() if k != "notes"})[:500])
    for name, e in sorted(ev.items()):
        title = (e.get("eventTitle") or "")[:60]
        ladder = []
        for t in TIERS:
            p = (e.get("eventPriceUsd") if isinstance(e.get("eventPriceUsd"), (int, float))
                 else None)
            tp = (e.get("eventTieredPricingUsd") or {}).get(t)
            ladder.append(f"{t}={tp if tp is not None else p}")
        print(f"   - {name}: {title}")
        print(f"       {' '.join(ladder)}  oneTime={e.get('isOneTimeEvent')}")
        if e.get("eventDescription"):
            print(f"       desc: {e['eventDescription'][:220]}")


for h in RIVALS + OURS:
    dump(h)
