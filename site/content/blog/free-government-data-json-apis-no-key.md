---
title: Eight government JSON APIs that need no key — and the specific way each one lies to you
description: Grants.gov, NIH RePORTER, USAspending, Federal Register, openFDA, ClinicalTrials.gov, EU TED and UK Find a Tender are all free and key-free. None of them 400 when you get it wrong — they return HTTP 200 with the wrong number of rows, and each does it differently.
date: 2026-09-12
tags: webscraping, api, opendata, procurement, government
---

Public-money data is the one corner of the web where you almost never need to scrape HTML. The US, EU and UK all publish grants, contracts, tenders, rules, recalls and clinical trials as JSON, from endpoints that take no API key, no OAuth, no account and no browser. We build and maintain Actors against all eight of the APIs below, and we call them from plain datacenter IPs — no residential proxies, no headless Chrome.

The catch is uniform across all eight, and it is not rate limits. **These APIs do not reliably fail.** Every one of them has at least one input you can get wrong and still receive `HTTP 200` with a plausible-looking body — just with silently truncated, silently empty, or silently unfiltered results. If your pipeline only checks the status code, you will ship a number that is quietly wrong.

## The eight endpoints

| API | Endpoint | Covers | Auth |
|---|---|---|---|
| Grants.gov | `POST https://api.grants.gov/v1/api/search2` | US federal grant opportunities | none |
| NIH RePORTER | `POST https://api.reporter.nih.gov/v2/projects/search` | NIH-funded research projects | none |
| USAspending | `POST https://api.usaspending.gov/api/v2/search/spending_by_award/` | Every US federal contract, grant, loan, IDV since 2007 | none |
| Federal Register | `GET https://www.federalregister.gov/api/v1/documents.json` | Every US rule, proposed rule and notice since 1994 | none |
| openFDA | `GET https://api.fda.gov/{drug,food,device}/enforcement.json` | FDA product recalls | none |
| ClinicalTrials.gov | `GET https://clinicaltrials.gov/api/v2/studies` | 600,000+ registered studies | none |
| EU TED | `POST https://api.ted.europa.eu/v3/notices/search` | Every public contract in the EU | none |
| UK Find a Tender | `GET https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages` | UK public contracts (OCDS) | none |

## The three ways they lie

Sort the failure modes and you get three classes. Knowing which class an API belongs to tells you what to assert on.

### Class 1 — silent truncation: you asked for more than you got

The API accepts your page size or offset, returns 200, and hands back fewer rows than you asked for without saying so.

- **ClinicalTrials.gov** caps `pageSize` at 1000. Send `pageSize=1001` and you get `200` with exactly 1000 studies and no warning field. ([full write-up](/blog/clinicaltrials-gov-json-api))
- **NIH RePORTER** has a hard offset wall around 15,000 rows. Past it, the response doesn't error — the page just shrinks. ([full write-up](/blog/nih-reporter-grants-json-api))
- **Federal Register** advertises 10,000 documents per query but clamps `per_page`, and offset paging *does* eventually 400 at row 10,000. The fix is already in the response body — the API hands you the cursor you actually need. ([full write-up](/blog/federal-register-documents-json-api))
- **openFDA** enforces a hard 25,000-row `skip` cap. Above it you stop getting new recalls. ([full write-up](/blog/fda-openfda-recall-json-api))
- **UK Contracts Finder** silently caps every page at 100 rows unless you ask in exactly the right shape. ([full write-up](/blog/uk-find-a-tender-ocds-json-api))

**Assert on:** `len(rows)` against what you requested, every page, not just the first.

### Class 2 — silent zero: a typo empties your result set

The parameter name is fine; the *value* is wrong, and the API treats "matches nothing" and "you sent nonsense" as the same answer.

- **Grants.gov** is the worst offender. `{"oppStatuses": "bananas"}` returns `{"errorcode": 0, "msg": "Webservice Succeeds", "data": {"oppHits": [], "hitCount": 0}}`. A misspelled status looks exactly like a genuinely empty filter. Parent agency codes also don't roll up to their sub-agencies, so a correct-looking agency filter can return far less than you expect. ([full write-up](/blog/grants-gov-federal-grant-opportunities-json-api))

**Assert on:** a known-good control query alongside the real one. If the control returns zero too, your filter vocabulary is wrong, not the data.

### Class 3 — silent everything: a typo removes your filter

The dangerous inverse of class 2, and the one that costs money if you pay per result.

- **NIH RePORTER**: an unrecognised field name inside `criteria` — a plural typo is enough — doesn't 400. It drops the filter and returns the entire database, 2.97 million rows, with HTTP 200.
- **Grants.gov**: an unknown top-level key like `{"totallyFakeParam": "xyz"}` is ignored outright, returning the unfiltered 10,000+ hit count.

**Assert on:** `hitCount`/`total` against an expected order of magnitude. A filtered query that suddenly returns millions has lost its filter, not found more data.

## Two more that fail differently

Not everything fits the three classes:

- **Federal Register** does hard-fail on a mistyped agency slug — but it kills the entire query rather than returning nothing for that one agency, so a single bad slug in a multi-agency filter takes down the whole request.
- **USAspending** enforces a separate field mapping per award type: you cannot ask for a contract and a grant in the same request, and the fields you get back differ by type. ([full write-up](/blog/usaspending-federal-awards-json-api))
- **EU TED** is the shape problem rather than the counting problem: multilingual value maps across 24 languages, arrays that repeat the same CPV code eight times, and a field that returns `-1` where you would expect `null`. ([full write-up](/blog/eu-ted-tenders-public-json-api))
- **UK Find a Tender** puts the money somewhere other than the award object, and one of its rate-limit errors comes back as plain text rather than JSON — so a naive `response.json()` throws on the error path instead of reporting it.

## A checklist that survives all eight

Whatever you build against public-money APIs, these four assertions catch nearly everything above:

1. **Row count per page** equals what you asked for, or you are on the last page — verify which.
2. **Total count** is within an expected order of magnitude for a filtered query.
3. **A control query with a deliberately invalid filter value** returns something different from your real query. If it doesn't, the API is ignoring your filter.
4. **Parse the error path too.** Don't assume the non-200 body is JSON.

## If you'd rather not maintain eight of these

We ship one Actor per API, each with the paging, filter-validation and shape normalisation above already handled, priced per result with no start fee and no subscription:

- [grants-gov-scraper](/tools/grants-gov-scraper) — US federal grant opportunities
- [nih-reporter-scraper](/tools/nih-reporter-scraper) — NIH-funded research projects
- [us-federal-awards-scraper](/tools/us-federal-awards-scraper) — US federal contracts, grants, loans, IDVs
- [federal-register-scraper](/tools/federal-register-scraper) — US rules, proposed rules and notices
- [fda-recall-scraper](/tools/fda-recall-scraper) — FDA food, drug and device recalls
- [clinicaltrials-scraper](/tools/clinicaltrials-scraper) — ClinicalTrials.gov studies
- [eu-ted-tenders-scraper](/tools/eu-ted-tenders-scraper) — EU public contract notices
- [uk-find-a-tender-scraper](/tools/uk-find-a-tender-scraper) — UK public contracts (OCDS)

Every one of them runs HTTP-only — no headless browser — which is [why they cost a fraction of a browser-based scraper](/blog/http-only-vs-headless-browser-scraping-cost) to run. Full list of what we build is on [the tools page](/tools), and the rest of the API write-ups are on [the blog](/blog).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned.*
