---
title: SAM.gov's 10,000-row depth cap doesn't promise 10,000 rows
description: A single active-opportunities query on SAM.gov's search backend (52,374 matches) was walked to its 10,000-row depth cap twice, seconds apart — one run delivered 8,925 distinct rows, the other 8,370. Same filters, same code, a 5.5-point swing from a live index reshuffling under the walk.
date: 2026-09-24
tags: webscraping, api, procurement, opendata
tool: sam-gov-opportunities-scraper
---

`sam-gov-opportunities-scraper`'s README already discloses that SAM.gov's keyless search backend caps paging at 10,000 rows per query, and that a broad enough query returns fewer *distinct* opportunities than that because the backend pages by offset over a live, relevance-sorted index that shifts under a long walk — rows repeat across pages, and repeats are dropped before billing. That disclosure was written from one measurement: a 19,834-match query where a full walk read 10,000 rows but only 8,990 distinct ids, about 10% repeats.

One measurement makes that number look like a constant. It isn't.

## Same query, seconds apart, two different answers

Active contract opportunities (`index=opp`, `is_active=true`) currently declare **52,374** matches — more than five times the depth cap, so any full walk hits the 10,000-row wall. Walking it to the cap twice, back to back, with nothing else changed:

| Run | Rows read | Distinct opportunities | Repeats dropped | Yield |
|---|---|---|---|---|
| 1 | 10,000 | 8,925 | 1,075 | 89.25% |
| 2 (re-run, same query, ~10s later) | 10,000 | 8,370 | 1,630 | 83.70% |

Same endpoint, same filters, same code path, no deploy in between — a 5.5-point swing in how much of the 10,000-row cap actually turns into new data. The repeats aren't clustered at a fixed offset either: run 1's duplicates showed up on pages 7–9 of a 10-page walk (169, 523, 383 repeats); run 2's showed up on pages 5 and 7–9 (368, 363, 449, 450). Different pages, different counts, same query — consistent with a relevance-sorted index that keeps getting re-scored while you're paging it, not with a fixed cursor artifact you could work around by adjusting page size or offset math.

## The effect only shows up once you're near the cap

A query that stays well under 10,000 total matches doesn't have anywhere for this to happen. `naics=541511` (Custom Computer Programming Services) with `is_active=true` declares 604 matches; walking all of it in a single page came back **604 distinct rows, zero repeats**. The duplicate/yield-variance problem is specific to walks that approach or exceed the depth cap — it isn't a general property of this backend's pagination.

## What this changes about the existing guidance

The Actor's `RUN_SUMMARY` already reports the real, per-run truth — `duplicateRowsDropped`, `scanned`, `delivered`, and `incompleteReason: "duplicate-rows"` or `"depth-cap"` when it applies — so no buyer relying on that record was ever shown a wrong number for their own run. What changes is the mental model for anyone reading the README's single "~10% repeats" example and treating it as a budgeting constant: for a query with `declaredMatches` well past 10,000, don't plan around a fixed discount off the cap. Two runs of the identical query landed 5.5 points apart here; the honest range to plan around is closer to "80s-to-high-80s percent of 10,000," re-measured per run via `RUN_SUMMARY`, not a single fixed number. The only way to avoid the variance entirely is the same advice the Actor already gives: narrow `naicsCodes`, `noticeTypes`, `states` or a keyword until `declaredMatches` sits under 10,000, the way the `naics=541511` query above did.

## Packaged version

[sam-gov-opportunities-scraper on Apify](https://apify.com/fetchsmith/sam-gov-opportunities-scraper) queries SAM.gov's own public search backend directly — no API key, no login, covering contract opportunities plus wage determinations, CFDA assistance listings, and PII-safe exclusion records behind the same `index=` parameter. Every run's `RUN_SUMMARY` reports `declaredMatches`, `duplicateRowsDropped`, and `incompleteReason` so you can tell "got everything" apart from "hit the depth cap" without reading logs.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every number above comes from a live request made while writing this post, not from documentation.*
