#!/usr/bin/env python3
"""Refresh substack-scraper/README.md's stale competitor user-count claims (cycle 1791).

Same treatment rule as bin/_refresh_claims_{gn,rjs,ats}.py: only the volatile HEADCOUNT
is touched, every price/feature/date claim in the same sentence is left exactly as
written. 7 claims flagged by bin/check-competitor-claims. Live values fetched
2026-10-16:

  >=20 live (after refresh) -> refresh to live value, dated:
    parsebird/substack-leaderboard-scraper      28 -> 32
    sleek_waveform/substack-creator-scraper     18 -> 22  (crossed the 20 line since
      last check -- published at 18/sub-20, live is now 22/>=20, so refresh)

  sub-20 (live value still under 20) -> DROP the count per the standing 2026-10-07 rule.
  The accompanying "N in the last 30 days" / "up from N" figures are dropped alongside
  the count they qualify -- a 30-day-new or prior-sweep figure is meaningless once its
  own denominator is removed, and it churns at least as fast as the total it modifies:
    sian.agency/substack-scraper              11 -> 13  (dropped "6 in the last 30 days" too)
    hipersoft/substack-scraper                  3 ->  1
    scrapemint/substack-newsletter-intelligence 4 ->  3
    lergassy/substack-scraper                   8 -> 12  (dropped "up from 4" too)
    moving_beacon-owner1/substack-scraper        5 ->  6
"""
import sys

PAIRS = [
    ("`sian.agency/substack-scraper` (11 users, 6 in the last 30 days) tiers a "
     "$0.05-down-to-$0.005 start fee",
     "`sian.agency/substack-scraper` tiers a $0.05-down-to-$0.005 start fee"),

    ("`sleek_waveform/substack-creator-scraper` (18 users, 7 in the last 30 days) "
     "charges a flat $0.002/post with no tiering at all",
     "`sleek_waveform/substack-creator-scraper` (22 users, re-verified live 2026-10-16) "
     "charges a flat $0.002/post with no tiering at all"),

    ("Also confirmed dearer than us at every tier with no further action: "
     "`parsebird/substack-leaderboard-scraper` (28u),",
     "Also confirmed dearer than us at every tier with no further action: "
     "`parsebird/substack-leaderboard-scraper` (32u, re-verified live 2026-10-16),"),

    ("One more is a likely **owner misconfiguration worth watching, not a genuine "
     "bargain**: `hipersoft/substack-scraper` (3 users) tiers $0.001 (Free) down to "
     "$0.0005 (Gold+) on its `post-scraped` event",
     "One more is a likely **owner misconfiguration worth watching, not a genuine "
     "bargain**: `hipersoft/substack-scraper` tiers $0.001 (Free) down to "
     "$0.0005 (Gold+) on its `post-scraped` event"),

    ("and `scrapemint/substack-newsletter-intelligence` (4u) is shape-different, not a "
     "direct substitute",
     "and `scrapemint/substack-newsletter-intelligence` is shape-different, not a "
     "direct substitute"),

    ("`lergassy/substack-scraper` (8 users, up from 4) is a genuine **partial "
     "undercutter**",
     "`lergassy/substack-scraper` is a genuine **partial undercutter**"),

    ("`moving_beacon-owner1/substack-scraper` (5u) flat $0.01/result + $0.00005 start",
     "`moving_beacon-owner1/substack-scraper` flat $0.01/result + $0.00005 start"),
]

path = "/root/agent/actors/substack-scraper/README.md"
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
