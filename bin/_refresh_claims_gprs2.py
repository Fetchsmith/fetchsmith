#!/usr/bin/env python3
"""Refresh the stale competitor user-count claims on google-play-reviews-scraper,
app-store-reviews-scraper and hacker-news-scraper (cycle 1792). Same treatment rule as
bin/_refresh_claims_{gn,rjs,ats,sub,apc2}.py: only the volatile HEADCOUNT is touched,
every price/feature/date/ranking claim in the same sentence is left exactly as written.
14 claims flagged by bin/check-competitor-claims. Live values fetched 2026-10-16.

Split judged by the LIVE value, not the published one (cycle-1791 wrinkle), and an
attached "N in the last 30 days"/"N new" figure is dropped alongside a dropped sub-20
count (also cycle-1791) because it churns at least as fast as the total it modifies.

  >=20 live -> refresh to live value + inline "re-verified live 2026-10-16":
    thewolves/google-play-reviews-scraper       1653 -> 1887
    x.com/google-playstore-review-scraper         20 ->   23   (published 20, live 23)
    automation-lab/google-play-scraper           882 -> 1035
    scrapesage/google-play-scraper                25 ->   28
    thewolves/appstore-reviews-scraper          2370 -> 2688
    johnvc/apple-app-store-reviews-api           479 ->  550
    gentle_cloud/hacker-news-scraper             162 ->  192

  sub-20 live -> DROP the count per the standing 2026-10-07 rule:
    cheapapi/app-store-google-play-scraper         2 ->    3
    lightmoon/google-play-store-reviews-scraper    1 ->    2
    darknezz/google-play-reviews-scraper           3 ->    1
    bikram07/app-store-reviews                     5 ->    7
    hiver/app-reviews-scraper                      0 ->    1
    bikram07/hn-who-is-hiring                     10 ->   13  (+ "3 of them in the last 30 days")
    nomad-agent/hackernews-scraper                 6 ->    7  (+ "1 new in the last 30 days")
"""
import sys

EDITS = {
    "/root/agent/actors/google-play-reviews-scraper/README.md": [
        # >=20 -> refresh + date
        ("rivals, `thewolves/google-play-reviews-scraper` (1,653 users) and",
         "rivals, `thewolves/google-play-reviews-scraper` (1,887 users, re-verified live "
         "2026-10-16) and"),

        ("`x.com/google-playstore-review-scraper` (20 users) charges a flat",
         "`x.com/google-playstore-review-scraper` (23 users, re-verified live 2026-10-16) "
         "charges a flat"),

        ("`automation-lab/google-play-scraper` (882 users — the niche's fourth-biggest "
         "listing by users",
         "`automation-lab/google-play-scraper` (1,035 users, re-verified live 2026-10-16 "
         "— the niche's fourth-biggest listing by users"),

        ("`scrapesage/google-play-scraper` (25 users) $0.0008 → $0.0002 per review",
         "`scrapesage/google-play-scraper` (28 users, re-verified live 2026-10-16) "
         "$0.0008 → $0.0002 per review"),

        # sub-20 -> drop the count
        ("and `cheapapi/app-store-google-play-scraper` (2 users) at **$0.00009 per review**",
         "and `cheapapi/app-store-google-play-scraper` at **$0.00009 per review**"),

        ("and `lightmoon/google-play-store-reviews-scraper` (1 user) starts at $0.00017",
         "and `lightmoon/google-play-store-reviews-scraper` starts at $0.00017"),

        ("`darknezz/google-play-reviews-scraper` (3 users, explicit FREE pricing model)",
         "`darknezz/google-play-reviews-scraper` (explicit FREE pricing model)"),
    ],
    "/root/agent/actors/app-store-reviews-scraper/README.md": [
        # >=20 -> refresh + date
        ("`thewolves/appstore-reviews-scraper` (2,370 users) and `theagents/appstore-reviews`",
         "`thewolves/appstore-reviews-scraper` (2,688 users, re-verified live 2026-10-16) "
         "and `theagents/appstore-reviews`"),

        ("`johnvc/apple-app-store-reviews-api` (479 users) is $0.00125–$0.00144/review",
         "`johnvc/apple-app-store-reviews-api` (550 users, re-verified live 2026-10-16) is "
         "$0.00125–$0.00144/review"),

        # sub-20 -> drop the count (the "zero runs in the last 30 days" dormancy read is
        # not a headcount, so it stays, as does the line-286 back-reference to it)
        ("`bikram07/app-store-reviews` (5 users) is\nlisted `FREE`",
         "`bikram07/app-store-reviews` is\nlisted `FREE`"),

        ("- `hiver/app-reviews-scraper` (0 users) — **$0.00009 (Free/Bronze)",
         "- `hiver/app-reviews-scraper` — **$0.00009 (Free/Bronze)"),
    ],
    "/root/agent/actors/hacker-news-scraper/README.md": [
        # >=20 -> refresh + date (the attached "33 of them in the last 30 days" keeps its
        # denominator, so it is left verbatim per the cycle-1791 treatment of `logiover`)
        ("The actively-growing leader is `gentle_cloud` (162 users, 33 of them in the last "
         "30 days — `gentle_cloud/hacker-news-scraper`)",
         "The actively-growing leader is `gentle_cloud` (192 users, re-verified live "
         "2026-10-16, 33 of them in the last 30 days — "
         "`gentle_cloud/hacker-news-scraper`)"),

        # sub-20 -> drop the count AND its attached 30-day figure
        ("**`bikram07/hn-who-is-hiring` (10 users, 3 of them in the last 30 days) is on "
         "Apify's FREE pricing model",
         "**`bikram07/hn-who-is-hiring` is on Apify's FREE pricing model"),

        ("`nomad-agent/hackernews-scraper` (6 users, 1 new in the last 30 days) charges a "
         "flat $0.0001",
         "`nomad-agent/hackernews-scraper` charges a flat $0.0001"),
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
    print(f"{path}: applied {len(EDITS[path])} replacements; {orig_len} -> {len(text)} bytes")
