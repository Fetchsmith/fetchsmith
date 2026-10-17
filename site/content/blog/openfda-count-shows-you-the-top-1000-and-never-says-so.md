---
title: openFDA's count= aggregation shows you the top 1,000 values and never tells you it stopped — we recovered 5,526 recalling firms from a "complete" list of 1,000
description: openFDA's count parameter silently defaults to 100 buckets, hard-caps at 1,000, refuses skip, and strips the meta.results block that would have told you the total. Date-partitioning recovers every missing value, exactly additively.
date: 2026-10-17
tags: webscraping, api, opendata, compliance
tool: fda-recall-scraper
---

`count=` is the most useful parameter on [openFDA](https://open.fda.gov/)'s enforcement (recall) API and the easiest one to misread. It turns a 29,485-row corpus into a one-request frequency table:

```
GET https://api.fda.gov/food/enforcement.json?count=classification.exact
```

```json
{"results": [
  {"term": "Class II", "count": 14745},
  {"term": "Class I",  "count": 12976},
  {"term": "Class III", "count": 1762},
  {"term": "Not Yet Classified", "count": 2}
]}
```

Four values, all of them, done. The trap is that a response that looks exactly like this one — a clean `200`, a tidy `results` array, no flag of any kind — is what you also get when the API has thrown away most of the answer.

## The count response has no `meta.results` block at all

Every ordinary search on this API tells you how big the answer is:

```
GET https://api.fda.gov/food/enforcement.json?limit=1
→ meta: {disclaimer, terms, license, last_updated, results: {skip: 0, limit: 1, total: 29485}}
```

Add `count=` and the `results` sub-object disappears from `meta` entirely:

```
GET https://api.fda.gov/food/enforcement.json?count=recalling_firm.exact&limit=1000
→ meta: {disclaimer, terms, license, last_updated}
```

No total, no echo of your limit, no "truncated": `true`. The number of distinct terms that *exist* is never stated anywhere in the payload. That matters, because:

## The default is 100 buckets and the ceiling is 1,000

Same query, four limits, on the food endpoint:

| Request | Buckets returned | Smallest count in the tail |
|---|---|---|
| `count=recalling_firm.exact&limit=10` | 10 | 219 |
| `count=recalling_firm.exact` (no limit) | **100** | 39 |
| `count=recalling_firm.exact&limit=1000` | **1000** | 5 |
| `count=recalling_firm.exact&limit=1001` | `400 BAD_REQUEST` — *"Limit cannot exceed 1000 results for count requests."* |

So the no-limit default hands you the top **100** firms out of thousands, and a reader who never passes `limit` gets a frequency table that silently excludes every firm with fewer than 39 recalls. Raising it to the maximum still stops at 1,000, and the tail of that list sits at count = 5 — meaning every firm with four recalls or fewer is simply not in the answer.

`1000` is not a coincidental total, either. All three enforcement endpoints return exactly it:

| Endpoint | Corpus rows | Distinct `recalling_firm.exact` buckets at `limit=1000` |
|---|---|---|
| `food/enforcement.json` | 29,485 | 1000 |
| `drug/enforcement.json` | 18,010 | 1000 |
| `device/enforcement.json` | 40,249 | 1000 |

Three different corpora, three different sizes, the same round number out. That is a ceiling, not a count.

## You cannot page past it — `skip` is rejected outright

The obvious fix doesn't exist:

```
GET https://api.fda.gov/food/enforcement.json?count=recalling_firm.exact&limit=1000&skip=1000
```

```json
{"error": {"code": "BAD_REQUEST", "message": "Should not use skip param when using count."}}
```

Credit where it's due: that's a clean, explicit `400`, not the silent no-op we measured on [Apple's podcast endpoints](/blog/apple-podcasts-episode-archive-is-not-there), where `offset` is accepted and ignored across the entire host. openFDA tells you no. But it is still a no — within a single query, the top 1,000 terms is all you can ever have.

## Partition the corpus instead — and the counts are exactly additive

`count=` applies *after* `search=`, so you can slice the corpus into windows small enough that no window hits the ceiling, and union the results. We ran the food endpoint year by year on `report_date`:

```
GET .../food/enforcement.json?search=report_date:[20160101+TO+20161231]&count=recalling_firm.exact&limit=1000
```

| | Distinct firms |
|---|---|
| One global query at the maximum limit | **1,000** |
| Union of 15 single-year windows (2012–2026) | **5,526** |

The real answer is **5.5× larger** than the "complete" list the API hands back. Three checks that the union is sound, not inflated:

1. **Nothing was lost.** All 1,000 terms from the global query appear in the union — zero missing.
2. **The counts add up exactly.** Summing every bucket across all 15 windows gives **29,485**, which is `meta.results.total` for the whole unfiltered corpus, to the row. No window double-counted, none dropped.
3. **Per-term additivity holds.** The largest firm, Garden-Fresh Foods, Inc., reports **633** globally and sums to **633** across the windows.

The one thing you must check per window: the busiest year returned 677 buckets, comfortably under 1,000, so no window was itself truncated. **If any window comes back with exactly `limit` buckets, treat it as truncated and subdivide it** — quarters, then months. Since the response carries no total, bucket-count-equals-limit is the only truncation signal you get.

## While you're here: `count=` without `.exact` returns a 500, not a 400

A string field counted without the `.exact` suffix doesn't produce a validation error. It produces a server error that leaks the backing Elasticsearch exception:

```
GET https://api.fda.gov/food/enforcement.json?count=recalling_firm
```

```
HTTP/1.1 500
{"error": {"code": "SERVER_ERROR", "message": "Check your request and try again",
 "details": "[illegal_argument_exception] Text fields are not optimised for operations that
  require per-document field data like aggregations and sorting, so these operations are
  disabled by default. Please use a keyword field instead. …"}}
```

This is not limited to long free-text fields. `classification` — a four-value enum — does it too, as do `state`, `voluntary_mandated` and `product_description`; we got the same 500 on the drug and device endpoints as well (`drug?count=classification`, `device?count=state`), so it's the field mapping, not one bad endpoint. Any retry-on-5xx client you've written will dutifully hammer a request that can never succeed, because the status code says "our fault, try again" about a client-side mistake. Add `.exact` and all of them work.

The same split governs `sort=`, with a different status code for the same underlying cause: `sort=recalling_firm:asc` is a clean `400`, while `sort=recalling_firm.exact:asc` and `sort=report_date:desc` both return `200`. Date fields need no suffix anywhere.

## And `limit` means nothing at all on a date count

One more inconsistency worth knowing before you build a dashboard on this. For a *term* count, `limit` caps the buckets. For a *date* count, it is ignored:

| Request | Buckets |
|---|---|
| `count=report_date` | 745 |
| `count=report_date&limit=5` | **745** |
| `count=report_date&limit=1000` | 745 |

`count=report_date` returns the full daily time series (keyed `time`, not `term`) regardless of what you ask for — which is convenient, and also means the same parameter silently caps one aggregation type and is discarded by the other.

## What this means if you're pulling recall data

If you only ever ask "who are the biggest recallers", the top-1,000 list is the right answer and none of this bites you. It bites the moment the question becomes *"how many distinct firms"*, *"has this specific small firm ever been recalled"*, or *"give me the complete vocabulary of this field"* — all three get a confidently wrong answer from a `200` response with no truncation signal in it.

[fda-recall-scraper](/go/fda-recall-scraper) doesn't use `count=` at all: it walks the records themselves and date-chunks automatically once a query's `total` approaches the separate 25,000-row `skip` cap, so the rows it returns to you are complete for your filter by construction. The two caps are independent and worth keeping straight — the 25,000 one is on *records* and announces itself with an error, the 1,000 one is on *distinct values* and says nothing.

For the record-level traps on this same API — the 25,000-row skip ceiling, and the `openfda.*` barcode fields that exist only on drug recalls — see [the first openFDA post](/blog/fda-openfda-recall-json-api).

Numbers above are live as of 2026-10-17, against an index openFDA stamps `last_updated: 2026-10-07`; corpus totals grow, the ceilings don't.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every status code and count above comes from a live request made while writing this post, not from documentation.*
