---
title: "HN search caps every query at 1,000 hits, no matter what nbHits claims — here's the live proof and the workaround"
description: "Algolia's HN Search API reports the true match count in nbHits (measured: 1,978,072 for query=ai) but silently refuses to serve past hit 1,000. Verified live: page 1000 returns Algolia's own pagination-limit message, and date-slicing reconstructs the full set exactly — but the slice width has to match how hot the query is."
date: 2026-09-24
tags: webscraping, hacker-news, api, algolia
tool: hacker-news-scraper
---

Hacker News's search — really Algolia's `hn.algolia.com/api/v1/search` — answers every query with an `nbHits` field that looks like a total you can page through. It isn't. Past the 1,000th hit, the API stops serving results entirely, and it does this quietly enough that a naive integration can believe it received a complete result set when it received one one-thousandth of it.

## The ceiling is real, and it isn't `nbHits`

Query `ai` under `tags=story`:

```
GET /api/v1/search?query=ai&tags=story&hitsPerPage=1
→ nbHits: 1,978,072, nbPages: 1000
```

Paging works fine right up to the edge — page 999 (0-indexed, `hitsPerPage=1`) still returns a real hit. One page further:

```
GET /api/v1/search?query=ai&tags=story&hitsPerPage=1&page=1000
→ nbHits: 0, nbPages: 0, hits: []
→ message: "you can only fetch the 1000 hits for this query.
   You can extend the number of hits returned via the paginationLimitedTo
   index parameter or use the browse method..."
```

That's Algolia's own words, returned live, not an inference from docs. `nbHits` never changes — it's the true count of matching documents in the index — but nothing past the 1,000th of them is reachable through `search`, regardless of `hitsPerPage` or how many pages you're willing to request. [Hacker News Scraper](/tools/hacker-news-scraper) already surfaces this per-query as `hitPaginationCeiling` in its `RUN_SUMMARY` record rather than let it pass silently, but if you're calling the raw API yourself, nothing tells you unless you go looking.

## The workaround works, and it reconstructs exactly

The standard fix is to slice the query by time window with `created_at_i` numeric filters (`postedAfter`/`postedBefore` in the Actor) so each slice's `nbHits` stays under 1,000, then run every slice. Does that actually reconstruct the full set with no gaps or double-counting? Measured live, not assumed: query `python` under `tags=story`, month-by-month for 2020.

| Month | `nbHits` |
|---|---|
| Jan | 342 |
| Feb | 328 |
| Mar | 324 |
| Apr | 357 |
| May | 447 |
| Jun | 377 |
| Jul | 339 |
| Aug | 324 |
| Sep | 301 |
| Oct | 305 |
| Nov | 295 |
| Dec | 256 |
| **Sum** | **3,995** |

The full-year query (`created_at_i>2020-01-01,created_at_i<2021-01-01`, no monthly split) reports `nbHits: 3,995` — the exact same number the twelve monthly slices sum to. No overlap, no gap, at half-open boundaries (`>start,<end`) chosen precisely to avoid double-counting a story created at exactly midnight on a boundary. Twelve requests under the ceiling recover what one request over the ceiling cannot.

## The slice width isn't a constant — it has to match how hot the query is

This is the part worth knowing before you hardcode "monthly" and move on: monthly is comfortably under 1,000 for `python` (256–447/month, confirmed above) but **not** for a hotter term. Query `ai`, January 2025 alone:

```
nbHits: 3,368  (already over the ceiling in a single month)
```

Splitting that same month into four ~7-day windows instead:

| Week | `nbHits` |
|---|---|
| 1 | 560 |
| 2 | 730 |
| 3 | 752 |
| 4 | 834 |

Every weekly slice clears the ceiling with room to spare; the monthly slice didn't clear it at all. There's no single safe window size across queries — `python` needs monthly, `ai` needs weekly, and a query hotter still (a single day's front-page discussion of a major release, say) could need slicing by the hour. Guessing a fixed width and moving on is exactly how a "complete" export quietly drops everything past hit 1,000 in whichever slice ran hot that period.

## What to actually do about it

Don't guess the width — read it back. [Hacker News Scraper](/tools/hacker-news-scraper)'s `RUN_SUMMARY` sets `hitPaginationCeiling: true` on any query slice that came back truncated (`declaredMatches` exceeds what was actually deliverable within the 1,000-hit window), so the correct loop is: run a slice, check the flag, and only if it's `true` split that slice in half and retry — rather than picking a width up front and hoping. That adapts automatically to both directions: a quiet month stays as one request instead of twelve wasted narrow ones, and a trending topic gets split as many times as it actually needs.

This is the same failure shape as a silently-capped API elsewhere: an answer that looks complete because nothing errors, and only a second measurement reveals otherwise. See the [comma-vs-parentheses guide](/blog/hacker-news-algolia-tags-and-not-or) for how the same index's `tags` field has an identical "no error, just quietly wrong" trap on the query-logic side, and the [public content APIs roundup](/blog/public-content-apis-hidden-second-step) for the same pattern on three other data sources.

[Hacker News Scraper](/tools/hacker-news-scraper) wraps HN's search, tag AND/OR composition, watch mode, and this pagination-ceiling detection into one flat-row-per-item Actor — pay only for items actually returned.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every number above comes from a live request made while writing this post, not from documentation.*
