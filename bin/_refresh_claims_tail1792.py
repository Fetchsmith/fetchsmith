#!/usr/bin/env python3
"""Close out the fleet-wide stale competitor user-count cleanup (cycle 1792, part 2):
the remaining 14 flags spread across 10 Actors (1-3 each). Same treatment rule as
bin/_refresh_claims_{gn,rjs,ats,sub,apc2,gprs2}.py: only the volatile HEADCOUNT is
touched, every price/feature/date/ranking claim in the same sentence is left verbatim.
Live values fetched 2026-10-16.

  >=20 live -> refresh to live value + inline "re-verified live 2026-10-16":
    fortuitous_pirate/courtlistener-legal-data     21 ->  24
    dltik/ted-europa-scraper                       32 ->  37
    scrapesage/sam-gov-scraper                     43 ->  49
    parsebird/unstop-jobs-internships-scraper      52 ->  60
    lurkapi/shopify-product-reviews-scraper-api    61 ->  68
    automation-lab/steam-game-reviews-scraper      82 ->  96
    automation-lab/steam-scraper                   25 ->  28

  sub-20 live -> DROP the count per the standing 2026-10-07 rule:
    inexhaustible_glass/fda-intelligence-scraper    4 ->   3
    tictechid/vanzi-us-recall-intelligence          2 ->   1
    ai_solutionist/regulatory-intelligence-api      3 ->   4
    memo23/unstop-jobs-internships-scraper          2 ->   1
    ryanclinton/usaspending-search                 12 ->  14

TWO EXCEPTIONS to the plain sub-20 drop, both recorded as new wrinkles:

  (1) jungle_synthesizer/bold-org-scholarship-database-scraper (3 -> 4). Sub-20, so the
      count drops -- but it carried an attached "dormant -- 0 new users in 30 days".
      The listing GAINED a user, so that figure is now probably false, and "dormant" rests
      entirely on it. Dropping the count while leaving either behind would publish an
      unsupported (likely wrong) claim, so the whole parenthetical goes. The dismissal does
      not depend on it: the price argument (2.9x our per-row rate before its $0.10 start
      fee) carries the sentence on its own.

  (2) sutraflow/sec-insider-trading-signals (1 -> 2). Sub-20, but the count is the SUBJECT
      of its clause ("Only X cleared the usual >=3-user floor at the time of that sweep")
      and the clause is explicitly dated "as of 2026-10-09". Dropping the number would
      destroy a dated historical argument, which the standing "leave dated paragraphs
      standing" principle protects. Refreshed + re-dated instead: still under the >=3
      floor at 2 users, which is the point the sentence makes.
"""
import sys

EDITS = {
    "/root/agent/actors/court-records-scraper/README.md": [
        ("`fortuitous_pirate/courtlistener-legal-data` (21 users, not previously named)",
         "`fortuitous_pirate/courtlistener-legal-data` (24 users, re-verified live "
         "2026-10-16, not previously named)"),
    ],
    "/root/agent/actors/eu-ted-tenders-scraper/README.md": [
        ("`dltik/ted-europa-scraper` (32 users) charges $0.005/tender flat",
         "`dltik/ted-europa-scraper` (37 users, re-verified live 2026-10-16) charges "
         "$0.005/tender flat"),
    ],
    "/root/agent/actors/fda-recall-scraper/README.md": [
        ("`inexhaustible_glass/fda-intelligence-scraper` (4 users) charges $0.005/result",
         "`inexhaustible_glass/fda-intelligence-scraper` charges $0.005/result"),

        ("`tictechid/vanzi-us-recall-intelligence` (2 users, FDA + CPSC + USDA FSIS with "
         "severity scoring)",
         "`tictechid/vanzi-us-recall-intelligence` (FDA + CPSC + USDA FSIS with severity "
         "scoring)"),
    ],
    "/root/agent/actors/federal-register-scraper/README.md": [
        ("`ai_solutionist/regulatory-intelligence-api` (3 users) charges $0.002/row",
         "`ai_solutionist/regulatory-intelligence-api` charges $0.002/row"),
    ],
    "/root/agent/actors/sam-gov-opportunities-scraper/README.md": [
        ("`scrapesage/sam-gov-scraper` (43 users, 24 in the last 30 days — the niche's "
         "busiest by recent activity)",
         "`scrapesage/sam-gov-scraper` (49 users, re-verified live 2026-10-16, 24 in the "
         "last 30 days — the niche's busiest by recent activity)"),
    ],
    "/root/agent/actors/scholarship-scraper/README.md": [
        # exception (1) -- see module docstring
        ("`jungle_synthesizer/bold-org-scholarship-database-scraper` (3 users, dormant — "
         "0 new users in 30 days), charges",
         "`jungle_synthesizer/bold-org-scholarship-database-scraper` charges"),

        ("`parsebird/unstop-jobs-internships-scraper` (52 users)",
         "`parsebird/unstop-jobs-internships-scraper` (60 users, re-verified live "
         "2026-10-16)"),

        ("plus a smaller fourth, `memo23/unstop-jobs-internships-scraper` (2 users) —",
         "plus a smaller fourth, `memo23/unstop-jobs-internships-scraper` —"),
    ],
    "/root/agent/actors/sec-insider-trades-scraper/README.md": [
        # exception (2) -- see module docstring
        ("`sutraflow/sec-insider-trading-signals` (1 user as of 2026-10-09, down from 3)",
         "`sutraflow/sec-insider-trading-signals` (2 users as of 2026-10-16, down from 3)"),
    ],
    "/root/agent/actors/shopify-products-scraper/README.md": [
        ("`lurkapi/shopify-product-reviews-scraper-api` (61 users)",
         "`lurkapi/shopify-product-reviews-scraper-api` (68 users, re-verified live "
         "2026-10-16)"),
    ],
    "/root/agent/actors/steam-reviews-scraper/README.md": [
        ("competitor by users is `automation-lab` (82 users, "
         "`automation-lab/steam-game-reviews-scraper`)",
         "competitor by users is `automation-lab` (96 users, re-verified live 2026-10-16, "
         "`automation-lab/steam-game-reviews-scraper`)"),

        ("`automation-lab/steam-scraper` (25 users, same owner as this niche's biggest "
         "review scraper;",
         "`automation-lab/steam-scraper` (28 users, re-verified live 2026-10-16, same "
         "owner as this niche's biggest review scraper;"),
    ],
    "/root/agent/actors/us-federal-awards-scraper/README.md": [
        ("`ryanclinton/usaspending-search` (12 users) at a flat $0.002/result",
         "`ryanclinton/usaspending-search` at a flat $0.002/result"),
    ],
}

fails = []
staged = {}
for path, pairs in EDITS.items():
    text = open(path, encoding="utf-8").read()
    orig_len = len(text)
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            fails.append(f"{path}: {n} matches for: {old[:90]}")
            continue
        text = text.replace(old, new)
    staged[path] = (text, orig_len)

if fails:
    print("ABORT -- non-unique/missing anchors (nothing written):")
    for f in fails:
        print("  " + f)
    sys.exit(1)

for path, (text, orig_len) in staged.items():
    open(path, "w", encoding="utf-8").write(text)
    print(f"{path.split('/')[-2]}: {len(EDITS[path])} repl; {orig_len} -> {len(text)} bytes")
