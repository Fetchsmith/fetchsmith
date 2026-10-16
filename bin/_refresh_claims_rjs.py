#!/usr/bin/env python3
"""Refresh remote-jobs-scraper/README.md's stale competitor claims (cycle 1788).

Nine claims flagged by `bin/check-competitor-claims`. Same treatment rule as
`bin/_refresh_claims_gn.py`: only volatile HEADCOUNTS are touched, every price/feature/
date claim in the same sentence is left exactly as written.

  >=20 users, count load-bearing (it carries a "biggest in the niche" / price-ladder
  point) -> refresh to the live value, dated. Live 2026-10-16:
    hirebase/remote-jobs                            216 -> 246
    aspen-technology-labs-inc/remote-jobs-api        34 ->  43
    inlifeprojects/himalayas-jobs-scraper           794 -> 898
    inlifeprojects/remoteok-jobs-scraper            681 -> 709  (not flagged; refreshed
      anyway so the "two biggest" pair does not read half-fresh/half-stale)
    memo23/remote-jobs-aggregator                   389 -> 421  (same reason, same list)
    automation-lab/remote-rocketship-jobs-scraper    45 ->  52
    automation-lab/jobgether-remote-jobs-scraper     29 ->  40

  Sub-20 -> DROP the count per the standing 2026-10-07 rule ("counts under 20 users are
  not published since totalUsers churns too fast at that resolution to stay accurate").
  The price/board-coverage claims next to them are the durable content and are kept:
    apt_marble/remote-jobs-aggregator-7-job-boards-in-one-run (2)
    tinyrex/remote-jobs-scraper (1)   -- also fixes the "(1 users)" agreement slip
    nomad-agent/web-dev-bundle (7) + nomad-agent/american-jobs-bundle (8, paired)

NOTE this is NOT a revival of `0-TODO-h1346-fleet-wide-sub20-counts`, closed at cycle
1496 as unreachable-by-design (its regex tally counts cohort-band phrases prior cycles
decided by documented policy to keep). These three are dropped because
check-competitor-claims independently flagged them as factually stale, which is a
reachable metric; no cohort-band phrase is touched.

Last, the "three dated price changes land inside the next two weeks" forecast paragraph
has gone past all three of its dates (2026-10-09/12/15) and is resolved here against the
live records rather than left reading as a pending prediction:
  * `gochujang/remote-jobs-aggregator` -- landed as forecast: the $0.001 start fee is
    gone, a single `job-fetched` $0.001 event started 2026-10-09.
  * `hiraware/greenhouse-jobs` -- landed as forecast: FREE model started 2026-10-12.
  * `antishock/remoteok-jobs-scraper` -- resolved the OTHER WAY: it never went free, the
    Actor was deleted (Apify API 404 on 2026-10-16). One fewer $0-priced rival than this
    paragraph projected. Its count is dropped rather than refreshed (a delisted Actor has
    no current user count, and that also stops check-competitor-claims re-flagging it
    forever -- the checker has no delisted-suppression mechanism).
"""
import sys

PAIRS = [
    ("`memo23/remote-jobs-aggregator` (389 users) a flat $0.00199/job plus additional-data "
     "and start fees, `hirebase/remote-jobs` (216 users) $0.003/job plus a $0.001 start fee,",
     "`memo23/remote-jobs-aggregator` (421 users) a flat $0.00199/job plus additional-data "
     "and start fees, `hirebase/remote-jobs` (246 users) $0.003/job plus a $0.001 start fee,"),

    ("`aspen-technology-labs-inc/remote-jobs-api` (34 users, $0.003→$0.0015/job plus a start fee)",
     "`aspen-technology-labs-inc/remote-jobs-api` (43 users, $0.003→$0.0015/job plus a start fee)"),

    ("`inlifeprojects/himalayas-jobs-scraper` (794 users) and "
     "`inlifeprojects/remoteok-jobs-scraper` (681 users)",
     "`inlifeprojects/himalayas-jobs-scraper` (898 users) and "
     "`inlifeprojects/remoteok-jobs-scraper` (709 users, both re-verified live 2026-10-16)"),

    ("`automation-lab/remote-rocketship-jobs-scraper` (45 users) reads Remote Rocketship",
     "`automation-lab/remote-rocketship-jobs-scraper` (52 users) reads Remote Rocketship"),

    ("`automation-lab/jobgether-remote-jobs-scraper` (29 users) reads Jobgether",
     "`automation-lab/jobgether-remote-jobs-scraper` (40 users) reads Jobgether"),

    # --- sub-20: drop the count, keep everything else
    ("`apt_marble/remote-jobs-aggregator-7-job-boards-in-one-run` (2 users) — **exact 7-board parity",
     "`apt_marble/remote-jobs-aggregator-7-job-boards-in-one-run` — **exact 7-board parity"),

    ("`tinyrex/remote-jobs-scraper` (1 users) — five of our boards,",
     "`tinyrex/remote-jobs-scraper` — five of our boards,"),

    ("`nomad-agent/american-jobs-bundle` (8 users) and `nomad-agent/web-dev-bundle` (7 users) each bill",
     "`nomad-agent/american-jobs-bundle` and `nomad-agent/web-dev-bundle` each bill"),

    # --- resolve the expired forecast
    ("Three dated price changes land inside the next two weeks and are already in the live "
     "records (every price tool we own, ours included, filters to `startedAt <= now` and so "
     "cannot see them): `antishock/remoteok-jobs-scraper` (2 users, RemoteOK alone) switches "
     "to Apify's **FREE** model on **2026-10-15**; `hiraware/greenhouse-jobs` (Greenhouse, "
     "not one of our boards) switches to **FREE** on **2026-10-12**; and "
     "`gochujang/remote-jobs-aggregator` (2 users, Remotive + We Work Remotely) **drops its "
     "$0.001 start fee on 2026-10-09**, leaving a flat $0.001/job that undercuts our "
     "Free/Bronze/Silver and ties Gold+.",
     "Three dated price changes were pending inside the following two weeks, already in the "
     "live records (every price tool we own, ours included, filters to `startedAt <= now` and "
     "so cannot see them): `antishock/remoteok-jobs-scraper` (RemoteOK alone) was to switch "
     "to Apify's **FREE** model on **2026-10-15**; `hiraware/greenhouse-jobs` (Greenhouse, "
     "not one of our boards) to **FREE** on **2026-10-12**; and "
     "`gochujang/remote-jobs-aggregator` (Remotive + We Work Remotely) to **drop its $0.001 "
     "start fee on 2026-10-09**, leaving a flat $0.001/job that undercuts our "
     "Free/Bronze/Silver and ties Gold+. **All three dates have now passed and were resolved "
     "against the live records on 2026-10-16: two landed as forecast, one did not.** "
     "`gochujang` is confirmed at a single `job-fetched` $0.001 event with no start fee "
     "(effective 2026-10-09), exactly as projected, so it is a real flat-$0.001 rival at "
     "Remotive + We Work Remotely only — two of our seven boards, no merge or de-duplication. "
     "`hiraware/greenhouse-jobs` is confirmed on the FREE model (effective 2026-10-12), and "
     "remains irrelevant to this Actor: Greenhouse is not one of the seven boards it reads. "
     "**`antishock/remoteok-jobs-scraper` resolved the other way — it never went free; the "
     "Actor was deleted, and the Apify API returns 404 for it as of 2026-10-16.** So this "
     "niche ended up with one fewer $0-priced rival than the forecast projected, and the "
     "lesson for reading future-dated `pricingInfos` is that a scheduled price is an "
     "intention, not an outcome — an owner can withdraw the listing before the date lands."),
]

path = "/root/agent/actors/remote-jobs-scraper/README.md"
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
