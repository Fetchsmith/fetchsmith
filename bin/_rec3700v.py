#!/root/agent/venv/bin/python
"""Cycle 3700: re-verify LIVE the already-disclosed rivals that dominate this
cycle's 5 raw every-tier hits from owner `scrapewise` (bucket 7). The c3691
lesson: a bucket-7 ruling leans on an EXISTING README disclosure, so the
dominator's live price/liveness must be re-read, not assumed -- c3691 caught a
stale price that way. Read-only: GET /v2/acts/<id>."""
import datetime, importlib.machinery, importlib.util, os, sys
ROOT = "/root/agent"
def _load(n, p):
    s = importlib.util.spec_from_loader(n, importlib.machinery.SourceFileLoader(n, p))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
cps = _load("cps", os.path.join(ROOT, "bin/check-price-superiority"))
sys.path.insert(0, os.path.join(ROOT, "bin"))
import _unit_price as up
from _apify_get import ApifyGetError, get_data
H = {"Authorization": "Bearer " + cps.token()}
NOW = datetime.datetime.now(datetime.timezone.utc)
DOMINATORS = {
    "substack-scraper": ["forgedata/substack-scraper", "maximedupre/substack-api",
                         "openharvest/substack-scraper"],
    "sam-gov-opportunities-scraper": ["pushbuild/sam-gov-opportunities", "bepolabs/sam-gov",
                                      "askerka00/samgov-contracts-pro-scraper"],
    "google-news-scraper": ["thescrappa/google-news-scraper", "eiv/news-monitoring-scraper",
                            "ilborso/google-news-article-text-scraper"],
}
for ours, rivals in DOMINATORS.items():
    print(f"=== dominators named in actors/{ours}/README.md")
    for h in rivals:
        u, n = h.split("/", 1)
        try:
            d = get_data(f"https://api.apify.com/v2/acts/{u}~{n}", headers=H)
        except ApifyGetError as e:
            print(f"  {h}: UNREACHABLE/GONE -- {e}"); continue
        cur = cps.effective(d.get("pricingInfos"), NOW) or {}
        ev = (cur.get("pricingPerEvent", {}) or {}).get("actorChargeEvents", {}) or {}
        t, k, fee, note = up.unit_price(ev)
        users = (d.get("stats") or {}).get("totalUsers")
        print(f"  {h}: model={cur.get('pricingModel')} users={users} event={k} "
              f"tiers={t} start={fee} note={note}")
