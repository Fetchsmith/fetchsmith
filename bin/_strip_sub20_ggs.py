#!/usr/bin/env python3
"""Strip bare sub-20 rival user-counts from grants-gov-scraper/README.md.

Per 0-TODO-h1346-fleet-wide-sub20-counts: drop the decorative `(N users)` for N<20
while keeping every price/scope/feature claim in the same sentence. Counts >=20 stay
(`fiery_dream/scholarship-intel` 39, `pink_comic/irs-990-nonprofit-search` 24).
Cohort-range phrases ("1-2-user listings", ">=3-user cohort") stay too -- they define
which cohort a dated sweep covered, and the already-done READMEs (eu-ted,
uk-find-a-tender, shopify, steam, trademark-search, clinicaltrials, court-records)
all preserve them.
"""
import sys

PAIRS = [
    ("`solidcode/grants-gov-scraper` (8 users) prices $0.0096/result",
     "`solidcode/grants-gov-scraper` prices $0.0096/result"),
    ("`thoob/grants-gov-feed` (2 users) has no enrich/thin split",
     "`thoob/grants-gov-feed` has no enrich/thin split"),
    ("`alizarin_refrigerator-owner/grants-gov-api---federal-grant-opportunities` (7 users) is a genuine Grants.gov API wrapper",
     "`alizarin_refrigerator-owner/grants-gov-api---federal-grant-opportunities` is a genuine Grants.gov API wrapper"),
    ("`constant_quadruped/research-grant-aggregator` (13 users) queries NIH RePORTER",
     "`constant_quadruped/research-grant-aggregator` queries NIH RePORTER"),
    ("`scrapepilot/grant-foundation-opportunities-scraper` (11 users) genuinely reads Grants.gov itself",
     "`scrapepilot/grant-foundation-opportunities-scraper` genuinely reads Grants.gov itself"),
    ("`fortuitous_pirate/grants-gov-scraper` (5 users) advertises itself",
     "`fortuitous_pirate/grants-gov-scraper` advertises itself"),
    ("`parseforge/grants-gov-scraper` (4 users) runs a result/detail split",
     "`parseforge/grants-gov-scraper` runs a result/detail split"),
    ("`aurumworks/us-federal-grant-scraper` (14 users) is a flat $0.009/result",
     "`aurumworks/us-federal-grant-scraper` is a flat $0.009/result"),
    ("`signalcrawl/federal-grant-fit-finder` (7 users, 3 new in the last 30 days — the fastest-growing listing in this comparison) is a scored-match product",
     "`signalcrawl/federal-grant-fit-finder` is a scored-match product"),
    ("`martc03/grant-finder-mcp` (3 users) is an MCP server",
     "`martc03/grant-finder-mcp` is an MCP server"),
    ("`soilair/grants-gov-api` (2 users) is the closest head-on substitute",
     "`soilair/grants-gov-api` is the closest head-on substitute"),
    ("`vhsgreed/us-federal-contracts` (2 users) is a broader-scope aggregator",
     "`vhsgreed/us-federal-contracts` is a broader-scope aggregator"),
    ("`brightpath-data/grants-gov-search` (2 users, $0.0015 + $0.0001 start)",
     "`brightpath-data/grants-gov-search` ($0.0015 + $0.0001 start)"),
    ("`gubidonius/grants-gov` (1 user, $0.0015 + a steep $0.002 start)",
     "`gubidonius/grants-gov` ($0.0015 + a steep $0.002 start)"),
    ("`upward_enterprises/grants-gov-opportunity-finder` (1 user), which runs an enrich/thin split",
     "`upward_enterprises/grants-gov-opportunity-finder`, which runs an enrich/thin split"),
    ("`nimble_flash/grant-fit-scout` (2 users) carries a vestigial",
     "`nimble_flash/grant-fit-scout` carries a vestigial"),
    ("`stefano_seggio/australia-grantconnect-monitor` (2 users) covers Australian GrantConnect",
     "`stefano_seggio/australia-grantconnect-monitor` covers Australian GrantConnect"),
    ("`great_pistachio/grants-gov-scraper` (3 users) has no enrich/thin split",
     "`great_pistachio/grants-gov-scraper` has no enrich/thin split"),
    ("`preservable_mocha/us-federal-grants-aggregator` (3 users) is a flat $0.003/result",
     "`preservable_mocha/us-federal-grants-aggregator` is a flat $0.003/result"),
    ("`caffein.dev/grants-actor` (3 users, broader scope — queries NIH RePORTER and Duke Research Funding alongside Grants.gov in one call) charges",
     "`caffein.dev/grants-actor` (broader scope — queries NIH RePORTER and Duke Research Funding alongside Grants.gov in one call) charges"),
    ("`bakos_bence/grants-gov` (2 users) tiers its enriched",
     "`bakos_bence/grants-gov` tiers its enriched"),
    ("`datalayer/grants-gov-funding` (2 users) tiers its `opportunity` event",
     "`datalayer/grants-gov-funding` tiers its `opportunity` event"),
    ("`publicrecords/govcon-opportunity-feed` (1 user, broader SAM.gov+Grants.gov scope) tiers",
     "`publicrecords/govcon-opportunity-feed` (broader SAM.gov+Grants.gov scope) tiers"),
    ("`automation-lab/grants-gov-funding-opportunities-scraper` (2 users) tiers its `item` event",
     "`automation-lab/grants-gov-funding-opportunities-scraper` tiers its `item` event"),
    ("`tagadanar/us-grants-monitor` (2 users, Grants.gov alerts + NIH award history) carries",
     "`tagadanar/us-grants-monitor` (Grants.gov alerts + NIH award history) carries"),
]

path = "/root/agent/actors/grants-gov-scraper/README.md"
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
