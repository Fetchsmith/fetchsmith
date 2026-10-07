#!/usr/bin/env python3
"""Strip bare sub-20 rival user-counts from sam-gov-opportunities-scraper/README.md.

Per 0-TODO-h1346-fleet-wide-sub20-counts: drop the decorative `(N users)` (and any
user-count/activity-derived growth clause riding alongside it, e.g. "0 in the last
30 days") for N<20, while keeping every price/scope/feature/date claim in the same
sentence -- non-count descriptive content inside the parens is kept, reformatted
without the count. Counts >=20 stay untouched (`jungle_synthesizer` 171,
`scrapesage` 43, `fortuitous_pirate` 116, `magicfingers` 43, `scrapebench` 29,
`pink_comic` 30, `omarchydev` 33, `taroyamada` 20). The `accountable_eel` (3 users)
mention at line ~285 is also left untouched -- it documents the >=3-user cohort cut
a dated sweep used, the same kind of cohort-band fact the prior backlog entries
(eu-ted, shopify, steam, trademark-search, clinicaltrials, grants-gov) preserved.
"""
import sys

PAIRS = [
    ("`bovi/sam-gov-opportunities-scraper` (8 users, verified live 2026-10-05) still tiers",
     "`bovi/sam-gov-opportunities-scraper` (verified live 2026-10-05) still tiers"),
    ("`publicmoney/sam-gov-opportunity-scraper` (3 users) still tapers",
     "`publicmoney/sam-gov-opportunity-scraper` still tapers"),
    ("`maydit/sam-gov-opportunities-scraper` (2 users) still tapers",
     "`maydit/sam-gov-opportunities-scraper` still tapers"),
    ("`automation-lab/samgov-government-contracts-scraper` (13 users) stacks",
     "`automation-lab/samgov-government-contracts-scraper` stacks"),
    ("`automation-lab/sam-gov-entity-exclusions-scraper` (4 users) is the same",
     "`automation-lab/sam-gov-entity-exclusions-scraper` is the same"),
    ("`alizarin_refrigerator-owner/sam-gov-contracts---federal-opportunities-search` (10 users) prices",
     "`alizarin_refrigerator-owner/sam-gov-contracts---federal-opportunities-search` prices"),
    ("`inexhaustible_glass/federal-contractor-intelligence` (5 users, $0.01 start + $0.005/row)",
     "`inexhaustible_glass/federal-contractor-intelligence` ($0.01 start + $0.005/row)"),
    ("`signalcrawl/sam-gov-contract-monitor` (3 users, $0.00005 start + $0.002/row)",
     "`signalcrawl/sam-gov-contract-monitor` ($0.00005 start + $0.002/row)"),
    ("`shipsatnight/sam-gov-contract-scraper` (3 users, $0.00005 start + $0.002/row)",
     "`shipsatnight/sam-gov-contract-scraper` ($0.00005 start + $0.002/row)"),
    ("`upward_enterprises/sam-gov-contract-radar` (3 users) ties us",
     "`upward_enterprises/sam-gov-contract-radar` ties us"),
    ("`martc03/gov-contracts-mcp` (12 users, 0 in the last 30 days) has no pricing record",
     "`martc03/gov-contracts-mcp` has no pricing record"),
    ("`ahmed_jasarevic/sam-scraper` (2 users)** advertises",
     "`ahmed_jasarevic/sam-scraper`** advertises"),
    ("`acid-base/borg-sam-contract-opportunities` (2 users) charges a flat",
     "`acid-base/borg-sam-contract-opportunities` charges a flat"),
    ("`bridged/sam-gov-opportunities-api` (1 user) charges a flat",
     "`bridged/sam-gov-opportunities-api` charges a flat"),
    ("`gochujang/gov-contract-tracker` (2 users) charges",
     "`gochujang/gov-contract-tracker` charges"),
    ("`publicrecords/govcon-opportunity-feed` (1 user) tiers",
     "`publicrecords/govcon-opportunity-feed` tiers"),
    ("`sigma-dev/usa-government-contract-scraper` (1 user) charges",
     "`sigma-dev/usa-government-contract-scraper` charges"),
    ("`oswaldocarabano/sam-gov-data-scraper` (2 users) is **dearer",
     "`oswaldocarabano/sam-gov-data-scraper` is **dearer"),
    ("`jungle_synthesizer/dol-oflc-prevailing-wage-determination-scraper` (2 users, listed 2026-10-01 — a second listing from the niche's user-count leader) tiers",
     "`jungle_synthesizer/dol-oflc-prevailing-wage-determination-scraper` (listed 2026-10-01 — a second listing from the niche's user-count leader) tiers"),
    ("`artificially/samgov-opportunities-scraper` (2 users) tiers",
     "`artificially/samgov-opportunities-scraper` tiers"),
    ("`artificially/business-data-mcp` (1 user) has no pricing record at all",
     "`artificially/business-data-mcp` has no pricing record at all"),
    ("`fetch_cat/sam-gov-contract-opportunities-monitor` (2 users, 0 in the last 30 days) charges",
     "`fetch_cat/sam-gov-contract-opportunities-monitor` charges"),
    ("`vhsgreed/us-federal-contracts` (2 users, 1 in the last 30 days) charges",
     "`vhsgreed/us-federal-contracts` charges"),
    ("`second_coming/gov-contract-monitor` (2 users), which bills",
     "`second_coming/gov-contract-monitor`, which bills"),
    ("`jtpalms/gov-tenders-monitor` (2 users) tiers",
     "`jtpalms/gov-tenders-monitor` tiers"),
    ("`steadydata/sam-gov-contract-opportunities` (2 users) tiers",
     "`steadydata/sam-gov-contract-opportunities` tiers"),
    ("`optimistprime/federal-contract-opportunities-monitor` (1 user) ties",
     "`optimistprime/federal-contract-opportunities-monitor` ties"),
    ("`tagadanar/usaspending-federal-awards` (2 users) reads",
     "`tagadanar/usaspending-federal-awards` reads"),
    ("`automation-lab/grants-gov-funding-opportunities-scraper` and `soilair/grants-gov-api` (2 users each) are both",
     "`automation-lab/grants-gov-funding-opportunities-scraper` and `soilair/grants-gov-api` are both"),
]

path = "/root/agent/actors/sam-gov-opportunities-scraper/README.md"
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
