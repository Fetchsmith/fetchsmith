---
title: NIH RePORTER's 15,000-row wall doesn't error — it silently shrinks your page, and a plural typo returns 2.97 million unfiltered rows
description: NIH's public grants API needs no key, but the offset wall truncates results instead of rejecting them, and an unrecognised criteria field name returns the entire database with HTTP 200.
date: 2026-09-11
tags: webscraping, api, opendata, nih, grants
tool: nih-reporter-scraper
---

Every research project NIH has funded since 1985 — 2.97 million of them — is queryable as JSON with no key, no login, no proxy:

```
POST https://api.reporter.nih.gov/v2/projects/search
Content-Type: application/json

{"criteria": {"pi_names": [{"any_name": "Doudna"}]}, "limit": 25}
```

We built [nih-reporter-scraper](https://apify.com/fetchsmith/nih-reporter-scraper) on this endpoint. Two things about it will silently corrupt a naive integration, and neither one throws an error.

## A plural typo doesn't 400 — it hands you the whole database

Ask for a real principal investigator with the correct field name and you get exactly what you'd expect:

```json
{"criteria": {"pi_names": [{"any_name": "Doudna"}]}, "limit": 5}
```
```json
{"meta": {"total": 84, ...}}
```

84 real matches. Now make the single most natural mistake a developer skimming the schema would make — drop the trailing `s`:

```json
{"criteria": {"pi_name": [{"any_name": "Doudna"}]}, "limit": 5}
```
```json
{"meta": {"total": 2975461, ...}}
```

Same HTTP 200, same response shape, no error field anywhere — and the "filtered" result is **the entire 2.97-million-row index**, 35,000× larger than the real answer. NIH RePORTER doesn't validate criteria key names at all: an unrecognised field is dropped silently and the query runs as if you'd asked for nothing. There is no way to tell "no filter matched" apart from "you spelled the filter wrong" by looking at the response — the only defence is validating every criteria key against a fixed allowlist before the request goes out, which is what the Actor does; an unrecognised key now fails the run loudly instead of quietly billing you for 100 unfiltered rows.

## The 15,000-row wall doesn't reject you — it shrinks your last page

NIH RePORTER caps how deep you can page into any single query, and the docs (such as they are) describe this as "`offset + limit` may not exceed 15000." That phrasing implies a clean validation error. It isn't one:

```json
{"criteria": {}, "offset": 14501, "limit": 500}
```
```json
{"meta": {"total": 2975461, "offset": 14501, "limit": 500, ...},
 "results": [ /* 499 rows, not 500 */ ]}
```

HTTP 200. `meta.limit` still says `500`. `meta.total` still says the full 2,975,461. But `results` silently comes back one row short. Push `offset` further into the same request and the gap grows exactly as predicted — at `offset: 14999, limit: 500` you get **1** row back, not 500. The formula is exact and mechanical: reachable rows = `max(0, 15000 - offset)`, enforced by quietly shrinking the array, not by rejecting the request. Only once `offset` itself reaches 15000 does the API finally 400 ("Not a valid request"), and even then the message gives no hint that a truncation wall — not a normal end-of-data condition — is what you actually hit.

This matters because the standard pagination idiom — "if I got fewer rows than I asked for, I've reached the end" — is exactly wrong here. A query with millions of real matches will look like it politely ran out of data at row 15,000 when in fact 2.9 million rows are sitting unreachable behind a wall with no cursor past it. The Actor detects the wall by position, not by a short page, and once a query's own `total` exceeds it, fans the query out across fiscal year, then administering institute, then award type — chunks small enough to stay under 15,000 each — merging and de-duplicating on `appl_id` so the same project can never be counted (or billed) twice across chunks.

## The publications join batches for free

NIH RePORTER also runs `/v2/publications/search`, which maps funded projects to the PubMed papers they produced. The useful thing here, verified live: it accepts a **batch** of project numbers in one call —

```json
{"criteria": {"core_project_nums": ["R01CA234538", "R01CA279801"]}, "limit": 25}
```

— and returns every linked PMID for both projects in a single request. That turns a naive "one publications call per project" join into one call per **25** project numbers (the batch cap we measured), which is why the Actor defaults `includePublications` to `true`: the grants-to-papers link most buyers actually want costs a small fraction of a request per row instead of one full extra round-trip per row.

## Packaged version

[nih-reporter-scraper on Apify](https://apify.com/fetchsmith/nih-reporter-scraper) wraps all three of these: a criteria-key allowlist that fails loudly on an unrecognised field instead of silently returning the unfiltered index, automatic chunking across fiscal year/institute/award-type that walks straight past the 15,000-row wall with de-duplication on `appl_id`, and a batched PubMed join on by default. No API key, no proxy, pay per result, no Actor-start fee. NIH RePORTER has no email or phone field anywhere in its schema, so — unlike most of our other government-data Actors — nothing needs to be redacted; principal investigator and program officer names ship as-is, the same statutory public disclosure already on every `reporter.nih.gov` project page.

The unfiltered-2.97-million-row failure above is the most expensive of three failure classes shared across the eight key-free government APIs we build against — see [Eight government JSON APIs that need no key](/blog/free-government-data-json-apis-no-key) for the cross-API comparison and the assertions that catch each one.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every JSON snippet above comes from a live request made while writing this post, not from documentation.*
