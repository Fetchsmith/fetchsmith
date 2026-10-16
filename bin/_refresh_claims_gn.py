#!/usr/bin/env python3
"""Refresh google-news-scraper/README.md's stale competitor user-count claims (cycle 1788).

`bin/check-competitor-claims` is deliberately date-blind on user counts (10% tolerance,
compared against the live API): a Store-page reader sees the printed number, not the
dated-sweep archaeology around it, so a count 10%+ off is a marketing claim we cannot
back up. That is compatible with the standing "leave dated paragraphs standing" practice
because only the volatile HEADCOUNTS are touched here -- every price, feature and date
claim in the same sentence is left exactly as written.

Four claims flagged this cycle. Live values fetched 2026-10-16:
  memo23/google-news-scraper      120 -> 140 users (51 -> 52 new/30d)
  fetch_cat/google-news-scraper    29 ->  33 users (11 -> 12 new/30d)
  scrapesage/google-news-scraper   32 ->  37 users
  simple.actors/google-search      DELISTED (API 404 on 2026-10-16)

The delisted one is the durable fix of the four -- a free, $0/result undercutter that no
longer exists overstates this niche's price pressure. Its count is dropped rather than
refreshed (a delisted Actor has no current user count, and dropping it also stops
check-competitor-claims re-flagging it forever with no suppression mechanism), and a
dated 404 note is put where a reader meets the claim. The surviving singular-handle
`simple.actor/google-search` is NOT the same listing: created 2026-09-08, PAY_PER_EVENT
since launch, never on the FREE model, so the README's "different owner handle" reading
below still stands.
"""
import sys

PAIRS = [
    # memo23 -- count is load-bearing ("growing fast"), so refresh rather than drop.
    ("`memo23` (120 users, `memo23/google-news-scraper`, created June 2026 and growing fast "
     "— 51 of its 120 users joined in the last 30 days)",
     "`memo23` (140 users, `memo23/google-news-scraper`, created June 2026 and growing fast "
     "— 52 of its 140 users joined in the last 30 days; counts re-verified live 2026-10-16)"),

    # fetch_cat -- refresh the count, and scope the superlative: at 12 new/30d it is no
    # longer the fastest-growing small listing in the niche (scrapesage is at 13), so the
    # claim is narrowed to the sweep it was actually measured in rather than left false.
    ("`fetch_cat/google-news-scraper` (29 users, 11 new in the last 30 days — the "
     "fastest-growing small listing found)",
     "`fetch_cat/google-news-scraper` (33 users, 12 new in the last 30 days, counts "
     "re-verified live 2026-10-16 — the fastest-growing small listing in that sweep)"),

    # simple.actors -- delisted; drop the count, flag it inline.
    ("`simple.actors/google-search` (25u, re-verified 2026-10-07) moved to Apify's FREE "
     "model on 2026-10-04",
     "`simple.actors/google-search` (**delisted — the Apify API returned 404 for this "
     "Actor on 2026-10-16, so it is no longer a live competitor in this niche; the rest of "
     "this sentence is the dated 2026-10-07 record and should not be read as current**) "
     "moved to Apify's FREE model on 2026-10-04"),

    # scrapesage -- the counts in this list carry its "several bigger than any rival named
    # above" point, so refresh rather than drop.
    ("`scrapesage/google-news-scraper` (32u) and `cloud9_ai/google-news-scraper` (22u) among them",
     "`scrapesage/google-news-scraper` (37u, re-verified live 2026-10-16) and "
     "`cloud9_ai/google-news-scraper` (22u) among them"),
]

path = "/root/agent/actors/google-news-scraper/README.md"
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
