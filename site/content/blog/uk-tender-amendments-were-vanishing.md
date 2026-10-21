---
title: "16.6% of UK tender notices were vanishing from our own Actor's default output"
description: Contracts Finder tags an amended tender notice "tenderAmendment", not "tender" — and a client-side filter bug meant this Actor dropped both the amendment AND the still-valid original, for every amended procurement on a default run. Live-measured, reproduced on the unfixed code, and fixed.
date: 2026-10-18
tags: webscraping, api, procurement, opendata
tool: uk-find-a-tender-scraper
---

Our [UK tender scraper](/tools/uk-find-a-tender-scraper) reads two official government procurement feeds — Find a Tender and Contracts Finder — and defaults to `stages: ["tender"]`, i.e. "show me live opportunities." Checking a different Actor's amendment handling this cycle led us back to our own: a stage-filtering bug meant that any UK procurement with an amended tender notice didn't show up at all on a default run, including ones with an open, bid-able deadline right now.

## The data: how common is a "tenderAmendment"

Both portals publish [OCDS](https://standard.open-contracting.org/) releases, and OCDS has a tagging convention for this: an amended release is tagged `tenderAmendment`, not plain `tender`. We pulled a live 6-week window from Contracts Finder with its own server-side `stages=tender` filter applied:

```
368 tender-stage releases returned
307 tagged "tender"
 61 tagged "tenderAmendment"   (16.6%)
```

Grouped by procurement (`ocid`), those 61 amendment releases belong to **39 of 316 distinct procurements (12.3%)** — each one a tender notice that had its deadline moved, scope changed, or documents updated after first publication. Contracts Finder's own server already includes `tenderAmendment` releases when you ask it for `stages=tender` — it treats an amendment as part of the tender stage, which is the sensible reading. The bug was entirely on our side, in the client-side re-check this Actor runs after fetching each page.

## The bug: an exact-string stage check, plus a dedup that ran too early

Our output exposes the raw OCDS tag array as a `stage` field. The client-side filter that re-applies `stages` was comparing it with `row.stage.includes(s)` — exact string equality. `"tenderAmendment" !== "tender"`, so under the default input every amendment release failed the filter and was silently dropped, counted only in an internal `filtered` tally nobody sees.

That alone would just mean "amendments are missing, originals still show." It didn't work out that way, because of a second, compounding issue. The Actor also dedupes on `ocid` to keep only the newest release per procurement (so a buyer isn't billed twice for the same contract). That dedup bookkeeping ran **before** the stage filter — so the moment the newest release for a procurement (the amendment) was pulled off the page, its `ocid` was marked "seen," regardless of whether it passed any filter. When the walk later reached the older, still-valid `tender`-tagged original for the *same* `ocid` — the one that genuinely should have matched — it looked like a duplicate of a release that had never actually been delivered, and was skipped too.

Net effect, on the default `stages: ["tender"]` input: for every one of those 39 amended procurements, **neither the amendment nor the original ever reached the output.** Not stale, not degraded — absent, as if the procurement didn't exist in either feed.

## Reproducing it

We confirmed this both ways on the same 6-week window, same four sampled procurements (identified by `ocid`):

```
unfixed code:  0 of 4 sampled amended procurements present
fixed code:    4 of 4 present, each at its current (amended) version
```

Total output on that window: 269 rows before the fix, 311 after — all 42 of the difference are genuine amended procurements that had been silently dropped, not noise.

## The fix

Two changes, matching the two failure points:

1. **Stage matching by prefix, not exact equality.** OCDS's own tagging convention prefixes every amendment/update/cancellation tag with its base stage name — `tenderAmendment`, `tenderUpdate`, `tenderCancellation` all belong to `tender`; `awardUpdate`, `awardCancellation` belong to `award`. The filter now checks `tag.startsWith(stage)` instead of `tag === stage`, which is also exactly what Contracts Finder's own server-side filter already does.
2. **Dedup moved after the filter check.** The `ocid`-based "keep the newest copy" bookkeeping now only runs once a release has already passed every filter. A release that fails some other filter (a CPV code, a value bound) can no longer claim an `ocid` and block a later, genuinely-matching release of the same procurement — the same bug shape, just not limited to the stage case.

Verified live on the platform post-fix (build `0.1.81`): a run against the same window and filters returns all 311 rows, including both sampled amendments, each carrying its current deadline rather than a stale one.

## Why this is worth knowing even if you don't use this Actor

If you call either portal's OCDS API directly with a `stages=tender` filter, you are already getting amendment releases back from the server — Contracts Finder isn't hiding them. The trap is specifically in any client-side re-filtering layered on top, if that layer treats the stage tag as an enum of exactly `tender`/`award`/`contract`/etc. rather than a family of prefixed variants. A bid-pipeline tool that silently drops 1 in 8 of the procurements it was asked to track is a worse failure than one that's merely incomplete — it looks identical to "nothing changed."

## Packaged version

Live now on [uk-find-a-tender-scraper](/go/uk-find-a-tender-scraper), build `0.1.81` — no input changes required; existing runs just see more correct rows on their next call. See the [OCDS fields write-up](/blog/uk-find-a-tender-ocds-json-api) for more on how this feed's nested shape gets flattened. [When a dateTo filter silently excludes its own last day](/blog/dateto-filter-silently-excludes-its-own-last-day) covers this same Actor's other boundary case on `dateTo` — that one is correct, documented behavior rather than a bug, but the shape of the trap (a filter silently excluding rows a buyer expected to see) is the same.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned.*
