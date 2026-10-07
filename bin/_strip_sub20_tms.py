#!/usr/bin/env python3
"""Strip bare sub-20 rival user-counts from trademark-search-scraper/README.md.

Per 0-TODO-h1346-fleet-wide-sub20-counts: drop the decorative `(N users)` for N<20
while keeping every price/scope/feature claim in the same sentence. Counts >=20 stay.
Cohort-range phrases ("1-2 users", "1-2-user tail") stay too -- they define which
cohort a dated sweep covered, and the already-done READMEs (eu-ted, uk-find-a-tender,
shopify, steam) all preserve them.
"""
import sys

PAIRS = [
    # --- multi-office listings ---
    ("`scrapers_lat` (12 users, `scrapers_lat/tmview-global-trademarks-scraper`) is the closest structural match",
     "`scrapers_lat/tmview-global-trademarks-scraper` is the closest structural match"),
    ("`zinin/trademark-multiregistry` (1 user) spans",
     "`zinin/trademark-multiregistry` spans"),
    ("`jdepablos` (15 users, `jdepablos/trademark-watch-tmview`) prices watching",
     "`jdepablos/trademark-watch-tmview` prices watching"),
    # --- three further multi-office listings ---
    ("`s-r/trademark-search` (2 users) is the closest never-named",
     "`s-r/trademark-search` is the closest never-named"),
    ("`everyotherfriday/trademark-search` (2 users) reads TMview",
     "`everyotherfriday/trademark-search` reads TMview"),
    ("`nexgendata/trademark-patent-search-api` (1 user) is the widest",
     "`nexgendata/trademark-patent-search-api` is the widest"),
    # --- single-register listings ---
    ("`dev00/uspto-trademark-text-check-api` (3 users, $0.005 per text check) carries",
     "`dev00/uspto-trademark-text-check-api` ($0.005 per text check) carries"),
    ("`scrapesage/uspto-trademark-scraper` (18 users) is $0.004/record",
     "`scrapesage/uspto-trademark-scraper` is $0.004/record"),
    ("`sheshinmcfly/uspto-trademark-checker` (11 users) and `glistening_film/uspto-trademark-lookup` (2 users) both match",
     "`sheshinmcfly/uspto-trademark-checker` and `glistening_film/uspto-trademark-lookup` both match"),
    ("`ryanclinton/euipo-trademark-search` (16 users) matches",
     "`ryanclinton/euipo-trademark-search` matches"),
    # --- report/alerting products ---
    ("`nexgenwatch/trademark-portfolio-report` (2 users each) charge",
     "`nexgenwatch/trademark-portfolio-report` charge"),
    ("`sian.agency/uspto-trademark-search-status-scraper` (3 users) at $0.00234",
     "`sian.agency/uspto-trademark-search-status-scraper` at $0.00234"),
    ("`silentflow/uspto-scraper` (2 users) at $0.002507",
     "`silentflow/uspto-scraper` at $0.002507"),
    # --- start-fee-not-row-rate paragraph ---
    ("`khadinakbar/uspto-trademark-batch-search`, 10 users, pairs a $0.00005 start",
     "`khadinakbar/uspto-trademark-batch-search` pairs a $0.00005 start"),
    ("`nexgendata/india-trademark-search`, 7 users, pairs the same",
     "`nexgendata/india-trademark-search` pairs the same"),
    # --- cheaper-from-the-first-row paragraph ---
    ("`jungle_synthesizer/dpma-trademark-patent-de-scraper` (7 users) is $0.0004/record",
     "`jungle_synthesizer/dpma-trademark-patent-de-scraper` is $0.0004/record"),
    ("`getascraper/dpma-trademark-register-scraper` (2 users) is cheaper still",
     "`getascraper/dpma-trademark-register-scraper` is cheaper still"),
    ("`jungle_synthesizer/ip-australia-trademark-scraper` (2 users) is $0.001 to $0.0008",
     "`jungle_synthesizer/ip-australia-trademark-scraper` is $0.001 to $0.0008"),
    # --- 1-2-user tail paragraph (cohort range itself preserved) ---
    ("`noahadler/euipo-uspto-trademark-search` (2 users), which prices",
     "`noahadler/euipo-uspto-trademark-search`, which prices"),
    # --- thirteen-more-listings paragraph ---
    ("`devilscrapes/uspto-trademark-scraper` (2 users) is $0.005/result",
     "`devilscrapes/uspto-trademark-scraper` is $0.005/result"),
    ("`scrapers_lat/uspto-trademarks-scraper` (1 user) tiers",
     "`scrapers_lat/uspto-trademarks-scraper` tiers"),
    ("`neuton/uspto-trademark-keyword-search` (2 users) is a flat",
     "`neuton/uspto-trademark-keyword-search` is a flat"),
    ("`neverempty/uspto-trademark-search-monitor` (2 users) is the closest in shape",
     "`neverempty/uspto-trademark-search-monitor` is the closest in shape"),
    ("`crawlerbros/euipo-trademark-design-search-scraper` (1 user) covers",
     "`crawlerbros/euipo-trademark-design-search-scraper` covers"),
    ("`unrivaled_fortress/wipo-global-trademark-brand-watch` (2 users, newly registered WIPO-international and US filings) at",
     "`unrivaled_fortress/wipo-global-trademark-brand-watch` (newly registered WIPO-international and US filings) at"),
    ("`accountable_eel/trademark-filing-watch` (2 users, USPTO **and** EUIPO new applications by Nice class) at",
     "`accountable_eel/trademark-filing-watch` (USPTO **and** EUIPO new applications by Nice class) at"),
    ("`automation_studio/uspto-trademark-radar` (2 users) at $0.005",
     "`automation_studio/uspto-trademark-radar` at $0.005"),
    ("`friendlyapi/uspto-trademark-scraper` (2 users) sells",
     "`friendlyapi/uspto-trademark-scraper` sells"),
    ("`nexgendata/trademark-conflict-watch` (2 users) bills",
     "`nexgendata/trademark-conflict-watch` bills"),
    ("`stefano_seggio/kipris-patent-trademark-status-monitor` (1 user, Korea KIPRIS) is $0.02",
     "`stefano_seggio/kipris-patent-trademark-status-monitor` (Korea KIPRIS) is $0.02"),
    ("`openrows/us-trademark-status` (2 users) is a TSDR",
     "`openrows/us-trademark-status` is a TSDR"),
    ("`nexgenwatch/trademark-dispute-mcp` (1 user) answers",
     "`nexgenwatch/trademark-dispute-mcp` answers"),
    # --- amortise-the-start-fee paragraph ---
    ("`fetch_cat/uspto-trademarks-scraper` (2 users) is the same shape",
     "`fetch_cat/uspto-trademarks-scraper` is the same shape"),
    ("`jungle_synthesizer/euipo-trademark-scraper` (3 users) matches our $0.002",
     "`jungle_synthesizer/euipo-trademark-scraper` matches our $0.002"),
]

path = "/root/agent/actors/trademark-search-scraper/README.md"
text = open(path, encoding="utf-8").read()
orig = text
fails = []
for old, new in PAIRS:
    n = text.count(old)
    if n != 1:
        fails.append(f"{n} matches for: {old[:90]}")
        continue
    text = text.replace(old, new)
if fails:
    print("ABORT -- non-unique/missing anchors:")
    for f in fails:
        print("  " + f)
    sys.exit(1)

open(path, "w", encoding="utf-8").write(text)
print(f"applied {len(PAIRS)} replacements; {len(orig)} -> {len(text)} bytes")
