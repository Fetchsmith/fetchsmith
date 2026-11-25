#!/root/agent/venv/bin/python
"""Cycle 3695: `NEW c3162` vendor-catalogue triage at OWNER `scrapesage` --
first sweep of this owner (pointer advanced here by c3689 after closing
`scrapersdelight`). Fresh discovery sweep (never trust a forwarded list) plus
live per-row pricing for every flagged row, via the per-handle
`GET /v2/acts/<owner>~<name>` route -- the c3680 lesson: `store?username=`
listing rows carry `currentPricingInfo` but NOT `pricingInfos`, so pricing off
a listing row reports every rival as free.

Unlike the per-niche `_batch_price_*` scripts, this owner's catalogue spans many
niches at once, so OURS is resolved PER ROW from the niche(s) the row's own text
matched (niche-size's curated vocabulary, same source check-vendor-catalogue
uses). Our own live ladder is re-read per niche and cached, never hardcoded.

Read-only: GET /v2/store?username= + GET /v2/acts/<id>. No runs, no writes
outside the out-file.
"""
import datetime
import importlib.machinery
import importlib.util
import json
import os
import sys

ROOT = "/root/agent"
OWNER = "scrapesignal_labs"


def _load(name, path):
    spec = importlib.util.spec_from_loader(name, importlib.machinery.SourceFileLoader(name, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cvc = _load("cvc", os.path.join(ROOT, "bin/check-vendor-catalogue"))
cps = _load("cps", os.path.join(ROOT, "bin/check-price-superiority"))
sys.path.insert(0, os.path.join(ROOT, "bin"))
import _unit_price as up  # noqa: E402
from _apify_get import ApifyGetError, get_data  # noqa: E402

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)
OUT_FILE = sys.argv[1] if len(sys.argv) > 1 else sys.exit("usage: _rec3691.py <out-file>")

# --- fresh discovery, same code path check-vendor-catalogue uses -------------
hs = cvc.our_handles()
vocab = cvc.niche_vocab()
_o, items = cvc.search_owner(OWNER)
if items is None:
    sys.exit(f"{OWNER} unreachable -- refusing to report a partial sweep")
print(f"{OWNER}: {len(items)} live listings (fresh)", file=sys.stderr)

flagged = []
disclosed = off_niche = 0
for it in items:
    name = it.get("name")
    if not name:
        continue
    handle = f"{OWNER}/{name}"
    if handle in hs:
        disclosed += 1
        continue
    niches = cvc.matching_niches(f"{it.get('title', '')} {it.get('description', '')}", vocab)
    if not niches:
        off_niche += 1
        continue
    flagged.append({"handle": handle, "niches": niches,
                    "users": (it.get("stats") or {}).get("totalUsers") or 0})
flagged.sort(key=lambda r: -r["users"])
print(f"flagged {len(flagged)} / disclosed {disclosed} / off-niche {off_niche} "
      f"-- cross-check flagged against c3688's 55", file=sys.stderr)

# --- our own live ladder, per niche, cached ---------------------------------
OURS = {}


def ours(slug):
    if slug not in OURS:
        if not os.path.isdir(os.path.join(ROOT, "actors", slug)):
            OURS[slug] = None
            return None
        try:
            d = get_data(f"{API}/acts/fetchsmith~{slug}", headers=H)
        except ApifyGetError as e:
            print(f"ERR ours {slug}: {e}", file=sys.stderr)
            OURS[slug] = None
            return None
        cur = cps.effective(d.get("pricingInfos"), NOW) or {}
        ev = (cur.get("pricingPerEvent", {}) or {}).get("actorChargeEvents", {}) or {}
        tiers, k, fee, note = up.unit_price(ev)
        OURS[slug] = {"tiers": tiers, "event": k, "fee": fee, "note": note} if tiers else None
        if tiers:
            print(f"ours {slug}: {tiers} fee={fee}", file=sys.stderr)
    return OURS[slug]


# --- price every flagged row -------------------------------------------------
out = []
for r in flagged:
    u, n = r["handle"].split("/", 1)
    try:
        d = get_data(f"{API}/acts/{u}~{n}", headers=H)
    except ApifyGetError as e:
        print(f"ERR {r['handle']}: {e}", file=sys.stderr)
        out.append(dict(r, error="unresolvable"))
        continue
    cur = cps.effective(d.get("pricingInfos"), NOW) or {}
    ev = (cur.get("pricingPerEvent", {}) or {}).get("actorChargeEvents", {}) or {}
    model = cur.get("pricingModel")
    ut, uk, fee, note = up.unit_price(ev)
    if not d.get("pricingInfos") or model == "FREE":
        ut, uk, note = {"FREE": 0.0}, None, "FREE model / no pricing record -- $0"
    runfee, runfee_label = cps.runfee_price(d, NOW)
    verdicts = {}
    for slug in r["niches"]:
        o = ours(slug)
        if not o:
            verdicts[slug] = "ours-unreadable"
            continue
        verdicts[slug] = {
            "ours": o["tiers"],
            "undercuts_tiers": up.undercut_tiers(ut, o["tiers"]),
            "every_tier": up.beats_every_tier(ut, o["tiers"]),
            "runfee_crossover_rows": (round(runfee / (o["tiers"].get("GOLD")
                                      or min(o["tiers"].values()))) if runfee else None),
        }
    out.append(dict(r, title=d.get("title"), model=model, unit_event=uk, unit_tiers=ut,
                    start_fee=fee, note=note, runfee=runfee, runfee_label=runfee_label,
                    verdicts=verdicts, desc=(d.get("description") or "")[:400]))

json.dump(out, open(OUT_FILE, "w"), indent=1)
hits = [o for o in out if any(isinstance(v, dict) and (v["undercuts_tiers"] or v["every_tier"])
                              for v in o.get("verdicts", {}).values())]
print(f"\npriced {len(out)} -> {OUT_FILE}; {len(hits)} row(s) undercut us at >=1 tier")
for o in out:
    mark = "HIT " if o in hits else "    "
    print(mark, o["handle"], f"{o.get('users')}u", o.get("model"), o.get("unit_tiers"),
          "start=" + str(o.get("start_fee")), "runfee=" + str(o.get("runfee")),
          "niches=" + ",".join(o["niches"]))
    for slug, v in (o.get("verdicts") or {}).items():
        if isinstance(v, dict) and (v["undercuts_tiers"] or v["every_tier"]):
            print(f"        vs {slug}: ours={v['ours']} undercuts={v['undercuts_tiers']} "
                  f"every_tier={v['every_tier']} crossover={v['runfee_crossover_rows']}")
