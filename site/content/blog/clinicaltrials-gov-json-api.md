---
title: The ClinicalTrials.gov API silently caps pageSize at 1000 — and its phase filter doesn't exist where you'd look for it
description: ClinicalTrials.gov's API v2 covers 600,000+ studies with no key and no login, but pageSize=1001 returns 200 with 1000 rows (no error), filter.hasResults and filter.phase are both rejected outright, and the real filters live somewhere else entirely.
date: 2026-09-11
tags: webscraping, api, healthcare, json
tool: clinicaltrials-scraper
---

Every clinical trial registered in the United States — 602,520 of them and counting — is public JSON, no API key, no login, no proxy:

```
GET https://clinicaltrials.gov/api/v2/studies?query.cond=breast+cancer&pageSize=100
```

That's ClinicalTrials.gov's official API v2, run by the NIH's National Library of Medicine. We built [clinicaltrials-scraper](https://apify.com/fetchsmith/clinicaltrials-scraper) on it, and three of its rougher edges are worth knowing before you write a client against it.

## `pageSize=1001` doesn't error — it just gives you 1000 rows

Most APIs we've built against (openFDA, Federal Register) reject a page size over their limit with a clean `400`. This one doesn't:

```
GET /api/v2/studies?pageSize=1001&fields=NCTId
→ HTTP 200, 1000 studies returned, no warning, no truncation flag
```

Ask for 1001 and you silently get 1000. If your code assumes "a 200 means I got what I asked for" — a fair assumption after working with APIs that 400 on an out-of-range page size — you'll under-fetch by one row on every maxed-out page and never notice, because nothing in the response tells you it happened. The fix is boring: always clamp your own request to 1000 and page forward with the response's own `nextPageToken` (which has no offset wall — we walked 5,000+ consecutive rows in one run with no rate limiting).

## `filter.hasResults` doesn't exist. The real filter is `aggFilters=results:with`

The API's field names are `hasResults`, `phases`, `studyType` — so the obvious guess for "only trials with posted results" is `filter.hasResults=true`. That guess gets rejected outright, not silently ignored:

```
GET /api/v2/studies?filter.hasResults=true&pageSize=1
→ 400 `filter.hasResults` is unknown parameter
```

The actual parameter is `aggFilters`, and it uses a `field:value` string, not a boolean flag:

```
GET /api/v2/studies?aggFilters=results:with&pageSize=3&fields=NCTId,HasResults
→ 200, three studies, all hasResults: true
```

At least this one fails loud. The next one doesn't.

## Filtering by phase or study type isn't a top-level filter at all

Try the same `filter.<fieldName>` pattern for phase and you get the same clean rejection:

```
GET /api/v2/studies?filter.phase=PHASE3&pageSize=1
→ 400 `filter.phase` is unknown parameter
```

`phases` and `studyType` turn out not to be filterable via any `filter.*` or `query.*` parameter at all. The only way to filter on them is `filter.advanced`, which takes a Lucene-style `AREA[FieldName]value` expression:

```
GET /api/v2/studies?filter.advanced=AREA[Phase]PHASE3&pageSize=2&fields=NCTId,Phase
→ 200, both rows have phases: ["PHASE3"]
```

Multiple conditions combine with `AND`/`OR` inside the same string — e.g. `AREA[StudyType]INTERVENTIONAL AND AREA[Phase]PHASE3`. There's no error message here pointing you at the right syntax; the plain `filter.phase` guess just 400s and stops, and nothing in that error tells you `filter.advanced` is where phase filtering actually lives. We found it by reading the API's own OpenAPI spec, not by guessing off the error text — worth doing for any field that 400s with "unknown parameter" here rather than assuming it isn't filterable at all.

## One more thing: don't ship the contact fields

Two `centralContacts[]` and per-location `contacts[]` blocks come back on every study with named individuals and personal emails — a live sample turned up a `@gmail.com` address on a real trial coordinator. Several competitor Actors in this niche resell that as a "contact finder." [clinicaltrials-scraper](https://apify.com/fetchsmith/clinicaltrials-scraper) drops it entirely — facility name, city, state, country and geo-coordinates only, never a person's name, phone or email.

## Packaged version

If you just want the rows — with phase/status/site filters, a `rowsPerStudy: "site"` mode for one-row-per-trial-site output, and the contact fields already stripped — [clinicaltrials-scraper](https://apify.com/fetchsmith/clinicaltrials-scraper) runs on Apify at $0.0015/result, no start fee.
