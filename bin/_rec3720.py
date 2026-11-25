#!/root/agent/venv/bin/python
"""Cycle 3720 (QUALITY slot): live-read the 6 rivals named in ats-jobs-scraper's
"Honest comparison" block so `NEW c3544`'s per-rival platform recount is MEASURED
against our current 12-entry SUPPORTED_ATS, not guessed.

c3544's whole point is "do NOT just substitute 12 for 7" -- each sentence states how
many of OUR platforms a specific rival covers, so every count has to be re-derived
from that rival's own live listing text against the live 12, one rival at a time.

Prints, per handle: users, title, pricing summary, and which of our 12 platform names
its own title+description names (plus any extra ATSes it names that we do NOT cover).
The platform match is a NAME SEARCH over the rival's own prose -- a candidate list for a
human read, never the final count on its own (vendors abbreviate, say "and more", or
name a platform only in a screenshot), so the printed description is read by hand too.
"""
import importlib.machinery
import importlib.util
import json
import os
import re
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

# Our live scope, read from source rather than retyped (src/main.js:14).
SRC = open(os.path.join(ROOT, "actors/ats-jobs-scraper/src/main.js"), encoding="utf-8").read()
m = re.search(r"const SUPPORTED_ATS = \[([^\]]*)\]", SRC)
OURS = [s.strip().strip("'\"") for s in m.group(1).split(",") if s.strip()]
print(f"OUR SUPPORTED_ATS ({len(OURS)}): {', '.join(OURS)}\n")

# Display/prose spellings for each of our 12 keys.
ALIASES = {
    "greenhouse": ["greenhouse"],
    "ashby": ["ashby", "ashbyhq"],
    "lever": ["lever"],
    "recruitee": ["recruitee"],
    "workable": ["workable"],
    "smartrecruiters": ["smartrecruiters", "smart recruiters"],
    "workday": ["workday"],
    "teamtailor": ["teamtailor", "team tailor"],
    "personio": ["personio"],
    "breezy": ["breezy"],
    "rippling": ["rippling"],
    "bamboohr": ["bamboohr", "bamboo hr"],
}
# ATSes we do NOT cover, so an "extra breadth" claim can be reported honestly too.
OTHERS = ["successfactors", "icims", "taleo", "jazzhr", "ukg", "dayforce", "paylocity",
          "oracle", "jobvite", "pinpoint", "polymer", "comeet", "zoho", "jobdiva",
          "bullhorn", "myworkday", "eightfold", "phenom", "avature", "gupy", "factorial"]

HANDLES = [
    "softyways/greenhouse-lever-ashby-workday-job-scraper",
    "openclawai/career-site-ats-jobs-scraper",
    "wickfeed/ats-job-aggregator",
    "webdata_labs/greenhouse-lever-ashby-jobs-scraper",
    "automation-lab/multi-ats-jobs-scraper",
    "blackfalcondata/greenhouse-scraper",
]

out = {}
for h in HANDLES:
    user, name = h.split("/", 1)
    try:
        d = get_data(f"{API}/acts/{user}~{name}", headers=H)
    except ApifyGetError as e:
        print(f"=== {h}\n  UNREADABLE: {e}\n")
        out[h] = {"error": str(e)}
        continue
    if not d:
        print(f"=== {h}\n  NO LIVE RECORD (404/delisted)\n")
        out[h] = {"error": "no record"}
        continue
    title = d.get("title") or ""
    desc = d.get("description") or ""
    seo = d.get("seoDescription") or ""
    prose = f"{title} {desc} {seo}".lower()
    hit = [k for k, al in ALIASES.items() if any(a in prose for a in al)]
    extra = [o for o in OTHERS if o in prose]
    pricing = (d.get("pricingInfos") or [])
    cur = pricing[-1] if pricing else None
    out[h] = {
        "users": d.get("stats", {}).get("totalUsers", 0),
        "title": title,
        "description": desc,
        "seoDescription": seo,
        "ours_named": hit,
        "ours_named_count": len(hit),
        "ours_missing": [k for k in OURS if k not in hit],
        "extra_named": extra,
        "pricing": cur,
    }
    print(f"=== {h}  ({out[h]['users']} users)")
    print(f"  title: {title}")
    print(f"  NAMES {len(hit)}/{len(OURS)} of ours: {', '.join(hit) or '(none)'}")
    print(f"  missing: {', '.join(out[h]['ours_missing']) or '(none)'}")
    print(f"  extra (not ours): {', '.join(extra) or '(none)'}")
    print(f"  desc: {desc[:700]}")
    print()

dest = os.path.join(ROOT, "state/audit_data/c3720_ats_rival_scope.json")
with open(dest, "w") as fh:
    json.dump(out, fh, indent=2, sort_keys=True)
    fh.write("\n")
print(f"wrote {dest}")
