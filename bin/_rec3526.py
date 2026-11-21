#!/usr/bin/env python3
"""One-off stamp for cycle 3526's enum_audit rotation on substack-scraper and
uk-find-a-tender-scraper (both DUE per audit-due --type enum_audit)."""
import json

R = "/root/agent"
p = R + "/state/audit_dates.json"
d = json.load(open(p))

results = {}

e = d["substack-scraper"]
prior = e["enum_audit"]
e["enum_audit"] = 3526
e["enum_audit_note"] = (
    "cycle 3526 (3189 -> 3526, 337c gap, DUE per audit-due --type enum_audit): "
    "bin/enum-canary --actor substack-scraper CLEAN on all 4 declared enum fields "
    "(discoverType, leaderboardTier, contentType, audienceFilter) -- deployed build "
    "matches repo exactly, order included, $0/no run created (HTTP 400 echo). "
    "bin/vocab-screen substack-scraper CLEAN on the one closed stringList vocabulary "
    "(discoverCategories): live /api/v1/categories still 35 top-level / 248 incl. "
    "subcategories, all 6 named example slugs (technology, business, finance, culture, "
    "us-politics, food) resolve. README carries no dated lifetime-count claim tied to "
    "either vocabulary (checked, unlike eu-ted-tenders-scraper's enumTitles -- nothing "
    "to restamp here). 0 drift, no code/README change needed. Cost $0."
    "\n\nPRIOR: " + e["enum_audit_note"]
)
results["substack-scraper"] = prior

e = d["uk-find-a-tender-scraper"]
prior = e["enum_audit"]
e["enum_audit"] = 3526
e["enum_audit_note"] = (
    "cycle 3526 (3190 -> 3526, 336c gap, DUE per audit-due --type enum_audit): "
    "bin/enum-canary --actor uk-find-a-tender-scraper CLEAN on both declared enum "
    "fields (sources[], stages[]) -- deployed build matches repo exactly, order "
    "included, $0/no run created. bin/vocab-screen uk-find-a-tender-scraper CLEAN on "
    "the cpvCodes closed vocabulary: live 824-code partition unchanged in shape "
    "(prefix '72' -> 80 codes, '85' -> 91 codes, 0 overlap, matches README's own IT "
    "example), tender/planning-stage CPV coverage both still 100% on Contracts Finder, "
    "classification scheme still exactly ['CPV'] on both portals. No dated "
    "lifetime-count claim tied to either enum vocabulary in the README (the many dated "
    "figures there are competitor_audit pricing/count claims, a different audit axis, "
    "not enum_audit scope). 0 drift, no code/README change needed. Cost $0."
    "\n\nPRIOR: " + e["enum_audit_note"]
)
results["uk-find-a-tender-scraper"] = prior

json.dump(d, open(p, "w"), indent=2, sort_keys=True)
for slug, prior in results.items():
    print("stamped enum_audit: %s %d -> 3526" % (slug, prior))
