#!/usr/bin/env python3
"""Refresh ats-jobs-scraper/README.md's stale competitor user-count claims (cycle 1791).

Same treatment rule as bin/_refresh_claims_{gn,rjs}.py: only the volatile HEADCOUNT is
touched, every price/feature/date claim in the same sentence is left exactly as written.
7 claims flagged by bin/check-competitor-claims. Live values fetched 2026-10-16:

  >=20 live (after refresh) -> refresh to live value, dated:
    openclawai/career-site-ats-jobs-scraper   32 -> 39
    wickfeed/ats-job-aggregator               25 -> 30
    memo23/career-site-ats-jobs-api          208 -> 235
    eiv/company-jobs-scraper                  18 -> 22  (crossed the 20 line since last
      check -- published at 18/sub-20, live is now 22/>=20, so refresh rather than drop)

  sub-20 (live value still under 20) -> DROP the count per the standing 2026-10-07 rule:
    fetch_cat/ats-jobs-scraper          9 -> 11
    nomad-agent/lever-jobs-scraper      3 ->  4
    steadydata/company-career-site-jobs 3 ->  4
"""
import sys

PAIRS = [
    ("**One correction that reverses a prior finding entirely: "
     "`fetch_cat/ats-jobs-scraper` (9 users) raised its price roughly 24x since we last "
     "checked it**",
     "**One correction that reverses a prior finding entirely: "
     "`fetch_cat/ats-jobs-scraper` raised its price roughly 24x since we last "
     "checked it**"),

    ("`openclawai/career-site-ats-jobs-scraper` (32 users) still auto-detects the company",
     "`openclawai/career-site-ats-jobs-scraper` (39 users, re-verified live 2026-10-16) "
     "still auto-detects the company"),

    ("`wickfeed/ats-job-aggregator` (25 users) covers 5 of our 7 platforms",
     "`wickfeed/ats-job-aggregator` (30 users, re-verified live 2026-10-16) covers 5 of "
     "our 7 platforms"),

    ("`jobo.world/ats-jobs-api` (769 users) and `memo23/career-site-ats-jobs-api` "
     "(208 users) are general-purpose ATS scrapers",
     "`jobo.world/ats-jobs-api` (769 users) and `memo23/career-site-ats-jobs-api` "
     "(235 users, re-verified live 2026-10-16) are general-purpose ATS scrapers"),

    ("`eiv/company-jobs-scraper` (18 users, Greenhouse/Lever/Ashby/SmartRecruiters/"
     "Workable/Recruitee plus Personio and Breezy",
     "`eiv/company-jobs-scraper` (22 users, re-verified live 2026-10-16, Greenhouse/Lever/"
     "Ashby/SmartRecruiters/Workable/Recruitee plus Personio and Breezy"),

    ("`nomad-agent/company-careers-bundle` (5u, $0.0002 flat) and "
     "`nomad-agent/lever-jobs-scraper` (3u, $0.0001 flat)",
     "`nomad-agent/company-careers-bundle` (5u, $0.0002 flat) and "
     "`nomad-agent/lever-jobs-scraper` ($0.0001 flat)"),

    ("`steadydata/company-career-site-jobs` (3 users) covers 6 of our 7 platforms",
     "`steadydata/company-career-site-jobs` covers 6 of our 7 platforms"),
]

path = "/root/agent/actors/ats-jobs-scraper/README.md"
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
