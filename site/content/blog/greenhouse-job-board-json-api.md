---
title: Greenhouse's job board API has no auth and no pagination — a big board is one 10 MB response
description: boards-api.greenhouse.io serves any company's full job board as public JSON with no key. But page/per_page/limit are silently ignored, the description is double-encoded HTML, there is no salary or employment-type field, and remote/hybrid hides in a board-specific metadata array.
date: 2026-10-19
tags: webscraping, api, jobs, hiring
tool: ats-jobs-scraper
---

Greenhouse is the applicant-tracking system behind a large share of venture-backed tech companies, and every Greenhouse board is backed by the same public JSON endpoint with no key, no cookie and no login. We [already covered it as one of six ATSes](/blog/ats-job-board-json-apis-six-shapes) and ship it as the first source in [ats-jobs-scraper](/go/ats-jobs-scraper); this is the dedicated write-up, the Greenhouse counterpart to [the one on Workday's career-site API](/blog/workday-career-site-json-api).

Every number below was measured live on 2026-10-19 against three real boards — `airbnb` (172 postings), `stripe` (725) and `databricks` (898), **1,795 postings total**.

## The endpoint

```
GET https://boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true
GET https://boards-api.greenhouse.io/v1/boards/<slug>/departments
```

`slug` is the company's board name — the path segment in `job-boards.greenhouse.io/<slug>`. No auth header of any kind. A board that doesn't exist returns a clean `404` (verified against a deliberately bogus slug), which is a much friendlier failure mode than Workday's, where a wrong tenant dies at the DNS/proxy layer instead of returning a status code.

## There is no pagination at all

This is the one that costs you if you assume otherwise. Greenhouse's board API does not accept page parameters — it ignores them:

```
$ curl -s "https://boards-api.greenhouse.io/v1/boards/airbnb/jobs?content=true" | wc -c
2457290
$ curl -s "https://boards-api.greenhouse.io/v1/boards/airbnb/jobs?content=true&per_page=5&page=1&limit=5" | wc -c
2457290
```

Byte-for-byte identical. `per_page`, `page` and `limit` are not rejected with a `400` — they're accepted and discarded, which is the [fail-open shape](/blog/government-apis-fail-open-on-a-dropped-filter-name) that makes a dropped parameter so easy to miss: the request succeeds, the data looks right, and the limit you asked for simply didn't happen.

The consequence is a size problem rather than a correctness problem. A board arrives whole, in one response, however big it is:

| board | postings | `?content=true` | without `content` |
|---|---|---|---|
| `airbnb` | 172 | 2,457,290 B (2.4 MB) | 132,397 B |
| `stripe` | 725 | 5,649,262 B (5.6 MB) | — |
| `databricks` | 898 | 9,859,357 B (9.9 MB) | — |

So `content=true` is an **18.6× size multiplier** on Airbnb's board, and a large board with descriptions is a ~10 MB JSON body you cannot chunk. If you're running in a memory-capped container, that body plus its parsed object graph is the actual constraint on scraping Greenhouse — not request count, and not rate limits. Ask for `content=true` only when you genuinely need descriptions.

## `content` is HTML-escaped HTML

The description isn't HTML. It's HTML that has been entity-encoded one extra time:

```
"content": "&lt;div class=&quot;content-intro&quot;&gt;&lt;p&gt;&lt;span style=&quot;font-family: helvetica..."
```

Feed that straight to an HTML parser and you get a single text node containing what looks like markup, with zero elements — not an error, just silently empty extraction. You have to HTML-decode once *before* parsing. This is the opposite of the usual bug: most APIs hand you HTML you have to escape, this one hands you HTML you have to unescape.

## No salary field, no employment-type field

Across the union of every key present on all 172 Airbnb postings, the full list is:

`absolute_url`, `ai_disclaimer`, `ai_opt_out_request_url`, `application_deadline`, `company_name`, `content`, `data_compliance`, `departments`, `education`, `first_published`, `id`, `include_ai_disclaimer`, `internal_job_id`, `language`, `location`, `metadata`, `offices`, `requisition_id`, `title`, `updated_at`

There is no compensation field and no full-time/part-time/contract field, on any of the three boards. That's not a per-board configuration gap — Greenhouse's board API simply doesn't model either one, which is why our Actor returns `employmentType: null` for every Greenhouse row and warns rather than silently returning zero rows if you filter on it.

Pay-transparency text, where a company publishes it, is **inside the `content` HTML** — so the only way to get a structured salary out of Greenhouse is to decode the description and parse the pay block out of prose, even for callers who don't want descriptions.

## `departments` on a posting is the leaf only, and `/departments` is flat

A posting's department array carries one node, with its parent referenced by id and nothing else:

```json
"departments": [{"id": 247, "name": "Business Development", "child_ids": [], "parent_id": 73691}]
```

`73691` is not in the posting payload. Resolve it against `/departments` and it's `"Sales & Partnerships"` — the department a human would actually say this job is in. **161 of Airbnb's 172 postings** and **584 of Databricks' 898** carry a leaf whose parent is missing from the row, so building a department path is not an edge case, it's the common case.

And the `/departments` endpoint doesn't give you a tree either: Airbnb's returns 61 nodes, flattened equals 61, because every `children` array is empty and the hierarchy exists only as `parent_id` pointers. You walk the pointers and assemble the path yourself. (It's also an unfiltered dump of the board's internal taxonomy, dead entries included — Airbnb's list contains `4. Prospecting (DONOTUSE)` and `5. (DoNotUse) Temp`.)

## Remote/hybrid lives in a board-specific `metadata` array, or nowhere

Greenhouse has no `isRemote` flag. What it has is a per-board custom-field array, and the field names are chosen by each company:

| board | postings with `metadata` | field names |
|---|---|---|
| `airbnb` | 172 / 172 | `Workplace Type`, `Is this job part of ACC?` |
| `databricks` | 898 / 898 | `Company Assignment`, `Career Page Posting Category` |
| `stripe` | 0 / 725 | *(none)* |

Airbnb publishes exactly what you want (`Workplace Type: "Hybrid"`). Databricks publishes two fields of internal bookkeeping and no workplace type. Stripe publishes no metadata at all. So there is no generic Greenhouse remote extractor to write — the best you can do is match the field *name* case-insensitively (our Actor matches `/workplace type/i`) and fall back to sniffing the free-text `location` string, accepting that on a board like Stripe's the answer isn't published anywhere.

`location` is itself hand-typed free text (`"London, United Kingdom"`), with no structured country/region/city — [the same normalization problem the six-ATS post describes](/blog/ats-job-board-json-apis-six-shapes).

## `application_deadline` exists and is empty

It's a declared field on every posting and it was populated on **1 of 1,795** postings measured (1 on Airbnb, 0 on Stripe, 0 on Databricks). If you're building a UI around it, treat it as absent. `first_published` and `updated_at`, by contrast, are real ISO timestamps and are the fields worth sorting and filtering on.

## Packaged version

[ats-jobs-scraper on Apify](/go/ats-jobs-scraper) handles all five of the above for Greenhouse — it decodes `content` before parsing, parses the pay-transparency block out of the description to fill `salaryMin`/`salaryMax`/`salaryCurrency`/`salaryInterval`, resolves the leaf department against `/departments` to emit `department`/`team`/`departmentPath`, reads `Workplace Type` out of `metadata` when the board publishes it, and normalizes the free-text location into `country`/`region`/`city` — with the same output schema shared across Greenhouse, Ashby, Lever, Recruitee, Workable, SmartRecruiters and Workday, so a Greenhouse row and a Workday row are directly comparable.

If you're pulling more than one ATS, the differences between them are the real work: [six ATSes, six ideas of what a job posting is](/blog/ats-job-board-json-apis-six-shapes), and [Workday's is a seventh](/blog/workday-career-site-json-api). [Lever has the opposite pagination problem](/blog/lever-job-board-json-api-pagination) from this one — its `skip`/`limit` params actually work, so the fix there is using them, not living without them. [Ashby doesn't even give you fake pagination params to ignore](/blog/ashby-job-board-json-api) — there's nothing to pass at all, honored or not. [Workable has the same fake-params shape as this one, but its `details=true` flag is real](/blog/workable-job-board-json-api) — unlike this page's `content=true`, which we need for salary parsing anyway, Workable's detail flag was pure waste whenever nobody asked for descriptions. [Recruitee ignores its pagination params the same way this one does](/blog/recruitee-job-board-json-api), but honors a case-sensitive `department` filter that returns an empty board on a wrong capital letter.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every endpoint, status code, byte count and field name above comes from a live request made while writing this post, not from documentation.*
