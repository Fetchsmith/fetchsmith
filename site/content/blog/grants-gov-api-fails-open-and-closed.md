---
title: Grants.gov's search API has two opposite silent failures — and only one of them is safe
description: A typo'd filter value on Grants.gov returns zero results. A typo'd filter NAME returns the entire unfiltered catalog, at the same errorcode 0 "Webservice Succeeds". Measured both, found the free detector in the response, and shipped a guard.
date: 2026-09-24
tags: webscraping, api, opendata, government
tool: grants-gov-scraper
---

We [already documented](/blog/grants-gov-federal-grant-opportunities-json-api) that Grants.gov's search API never reports a bad parameter: it answers `errorcode: 0`, `"Webservice Succeeds"`, and hands back a silently empty result set. That was measured once, believed to be the whole story, and written into our scraper's source as a one-line warning.

It is not the whole story. There are **two** silent failure modes, they point in opposite directions, and the one nobody had measured is the one that costs money.

All counts below come from live `POST https://api.grants.gov/v1/api/search2` calls made within the same minute while writing this post. No API key, no auth — this endpoint is open.

## The baseline

```json
{"rows": 1}
```

→ `hitCount: 1533`. Worth noting before anything else: this is not "everything." The response's own echo block reveals the server applied a default of `oppStatuses: "forecasted|posted"`. Grants.gov has filters running before you send any.

## Failure mode 1: a bad VALUE fails closed

Send a real parameter with a garbage value and you get nothing:

| request | hitCount |
|---|---|
| `{"oppStatuses": "posted"}` | 942 |
| `{"oppStatuses": "postd"}` | **0** |
| `{"oppStatuses": "zzzz"}` | **0** |

Every response was HTTP 200, `errorcode: 0`, `"Webservice Succeeds"`. We repeated this with `ZZZZNOTREAL` as the value for `agencies`, `eligibilities`, `fundingCategories`, `fundingInstruments`, `cfda`, `sortBy`, `dateRange` and `oppNum` — all eight returned `hitCount: 0`.

`sortBy` is the surprise in that list. A garbage **sort** value doesn't give you an unsorted result set; it deletes the result set. Sorting is not a presentation-layer concern on this API.

This mode is annoying but financially harmless. You get zero rows, you notice immediately, and under per-result pricing you are billed for nothing.

## Failure mode 2: a bad NAME fails open

Now misspell the parameter *name* instead of its value:

| request | hitCount |
|---|---|
| `{"totallyMadeUpParam": "posted"}` | 1533 |
| `{"oppStatus": "posted"}` | 1533 |
| `{"agency": "posted"}` | 1533 |
| `{"eligibility": "posted"}` | 1533 |
| `{"fundingCategory": "posted"}` | 1533 |
| `{"postedFromDate": "posted"}` | 1533 |

1533 is the unfiltered baseline. An unrecognized parameter is **dropped without a word** and you are served the whole catalog — same HTTP 200, same `errorcode: 0`, same `"Webservice Succeeds"`. A known parameter set to an empty string (`{"oppStatuses": ""}`) behaves identically: treated as absent, 1533 rows.

The reason this is a trap rather than a curiosity is the **singular/plural near miss**. Grants.gov's filter parameters are plural, but the rows it returns are described in the singular, so the singular is exactly what you'd guess:

| what you meant | what you typed | rows you asked for | rows you got |
|---|---|---|---|
| `eligibilities: "25"` | `eligibility: "25"` | 690 | **942** (+37%) |
| `oppStatuses: "posted"` | `oppStatus: "posted"` | 942 | **1533** (+63%) |

Nothing in either response indicates a problem. Under a per-result pricing model you have just paid 37–63% extra for rows you explicitly filtered out — and if you were shipping those rows onward, your downstream now contains records that fail your own stated criteria.

The same shape breaks pagination. `startRecordNum: 10` correctly returns a different page than `startRecordNum: 0`. Misspell it as `startRecordNo: 10` and you silently get page 1 again — a pager built on the wrong name re-serves the first page until it hits your row cap, charging you for duplicates the whole way.

## The free detector: read `searchParams` back

The good news is that the API tells you, if you ask the right question. Every response carries a `data.searchParams` block that echoes what the server **actually recognized and applied**:

```
POST {"rows":1,"oppStatuses":"posted","eligibilities":"25"}
  → hitCount 690, searchParams: {resultType: json, oppStatuses: "posted", eligibilities: "25", rows: 1}

POST {"rows":1,"oppStatuses":"posted","eligibility":"25"}
  → hitCount 942, searchParams: {resultType: json, oppStatuses: "posted", rows: 1}
```

The dropped filter is simply **absent** from the echo. That's your assertion.

One thing to get right: don't compare *key sets*. The echo block always carries a core group of keys with empty-string defaults whether you sent them or not, so "is the key present" gives you false confidence. Compare **non-empty values** — for each filter you sent, assert the echo came back carrying the value you sent. That check costs zero extra requests, because the echo rides along on a response you already paid for.

## What we shipped

`grants-gov-scraper` now round-trips every filter through `searchParams` on each search page and **throws** if one didn't come back with the value we sent, rather than delivering a wider set than the buyer asked for. That matches the rule this Actor already applied to bad date bounds: under per-result pricing, a failure that *narrows* your results can warn, but a failure that *widens* them has to stop the run — nobody reads a warning inside an otherwise-successful run, and by the time they'd read it they've been billed.

We verified all 13 parameters the Actor sends (`resultType`, `rows`, `startRecordNum`, `oppStatuses`, `keyword`, `keywordEncoded`, `agencies`, `eligibilities`, `fundingCategories`, `fundingInstruments`, `cfda`, `sortBy`, `dateRange`) round-trip cleanly today, so the guard cannot false-positive on our own known-good names — a full run over 110 matching opportunities passed it silently on every page. Then we proved it actually fires by temporarily shipping `eligibility` instead of `eligibilities` and watching the run stop with a named error instead of quietly returning 37% too many rows.

The guard exists for the day Grants.gov renames or retires a parameter underneath us. On an API that reports every mistake as `"Webservice Succeeds"`, a change like that would otherwise look exactly like business as usual.

## If you're calling the API yourself

1. Establish your unfiltered baseline count first. If a filtered query returns exactly that number, your filter isn't running.
2. Assert non-empty `data.searchParams` values against what you sent, on every request.
3. Remember the parameters are plural (`oppStatuses`, `agencies`, `eligibilities`, `fundingCategories`, `fundingInstruments`) even though the data reads singular.
4. `hitCount: 0` means your value was wrong. The full catalog means your *name* was wrong. Neither will ever be an error status.

[grants-gov-scraper on Apify](https://apify.com/fetchsmith/grants-gov-scraper) handles all of this — live-resolved agency codes (a parent code like `USDA` expands to its sub-agencies), client-side absolute date ranges the API doesn't offer, and now a fail-open guard on every search page. $0.002/result thin, no run-start fee, incremental `watchLabel` mode for scheduled monitoring.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every number above comes from a live request made while writing this post, not from documentation.*
