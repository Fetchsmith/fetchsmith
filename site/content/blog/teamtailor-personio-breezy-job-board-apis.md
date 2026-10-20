---
title: Teamtailor, Personio and Breezy — three more ATS job-board APIs, three more shapes
description: Teamtailor's board is a JSON Feed with an embedded schema.org JobPosting, Personio's is XML with the title field called "name", and Breezy's structured location only shows up once you stop testing on the vendor's own demo tenant.
date: 2026-10-19
tags: webscraping, api, jobs, hiring
tool: ats-jobs-scraper
---

The [six-ATS roundup](/blog/ats-job-board-json-apis-six-shapes) covered Greenhouse, Ashby, Lever, Recruitee, Workable and SmartRecruiters — plus [Workday](/blog/workday-career-site-json-api) separately, since it needs a per-job detail call the other six don't. [ats-jobs-scraper](/go/ats-jobs-scraper) now covers three more: Teamtailor, Personio and Breezy. None of the three needed a login or a key, and none of the three agreed with the first six — or each other — on what a job posting looks like.

## Teamtailor: a real JSON Feed, with a full schema.org JobPosting riding along for free

```
GET https://<tenant>.teamtailor.com/jobs.json
```

This isn't a bespoke shape — it's [JSON Feed 1.1](https://www.jsonfeed.org/), the same syndication format blogs use, with `{version, title, home_page_url, feed_url, items[]}` at the top level. Each item carries `id`, `url`, `title`, `date_published`, `content_html` — and `_jobposting`, a fully embedded **schema.org JobPosting** object with `jobLocation`, `datePosted` and `hiringOrganization` already resolved. That's the same information Workday makes you fetch with a second per-job call; Teamtailor just includes it in the list response.

The one trap is `jobLocation[].address.addressRegion`. It looks like a sub-country field — a US state, a German Land — and it is never that. Measured across two boards (`oatly.teamtailor.com`, `career.teamtailor.com`, 30 postings combined): it's either a continent name (`"Oceania"`, `"North America"`, `"Europe"`) or, on a single-country board, a repeat of the country name (`"Sweden"`). We left `region: null` rather than ship a continent mislabeled as a region — the same call this Actor's `location.js` already makes elsewhere: a wrong field is worse than a null one.

## Personio: XML, and the title field is called `name`

```
GET https://<tenant>.jobs.personio.de/xml
```

Personio is the only one of the nine that isn't JSON at all — `<workzag-jobs><position>...</position></workzag-jobs>`, parsed with `cheerio.load(xml, {xmlMode: true})` rather than pulling in a dedicated XML library (cheerio was already a dependency, for Greenhouse's HTML descriptions). Each `<position>` is a flat bag of fields — `id`, `office`, `department`, `employmentType`, `seniority`, `createdAt` — but the field holding the job title is `name`, not `title`. It's the same "common concept, uncommon name" problem as Workable's `telecommuting` flag, just on the field that matters most.

Two more things only show up once you sample more than one tenant. First, an empty board is a valid, successful response: `holidu.jobs.personio.de/xml` returns `200` with a 72-byte `<workzag-jobs/>` and zero positions — that has to parse to 0 rows, not fail, the same rule this fleet already applies to `scholarship-scraper`'s empty-result pages. Second, **the feed has no job-URL field anywhere** — no `url`, no `link`, nothing. The pattern `<tenant>.jobs.personio.de/job/<id>` isn't documented; we only shipped it after fetching it directly and confirming the page's `<title>` matched the feed's `name` for that id.

## Breezy: the vendor's own demo tenant hides most of the schema

```
GET https://<tenant>.breezy.hr/json
```

A flat JSON array, `name` for the title field again, `url` prebuilt per posting. The trap here isn't a field name — it's that the obvious tenant to test against, `breezy.breezy.hr` (Breezy's own demo board), is a bad sample. Its rows are minimal: no structured location, no salary, nothing to normalize.

A real customer tenant tells a different story. On `the-san-francisco-standard` (pulled from a competing Actor's own `exampleRunInput`, not guessed), `location` is a **structured object** — `country.name`, `state.name`, `city`, and an `is_remote` boolean — not the free text Greenhouse and Personio hand back, so no location-guessing helper is needed for this one ATS. And a free-text `salary` field exists (`"$25 / hour"`), parsed with the same `parseMoney`/`periodWord` helpers already built for Greenhouse's pay-transparency block.

Breezy's `?location=` and `?department=` query parameters are both silently ignored — confirmed on the real tenant with two different parameter names, both byte-identical to the unfiltered response. That's the same fails-open shape already documented for Greenhouse and Workable in [the government-APIs filter post](/blog/government-apis-fail-open-on-a-dropped-filter-name), just on a vendor we hadn't tested before.

## Don't trust a vendor's own demo tenant as your only sample

The real lesson across all three isn't a field name — it's that **the easiest tenant to find (the vendor's own demo board, or the first company slug that resolves) is often the least representative one.** Breezy's demo tenant has no salary and no structured location; a real customer board has both. If you're building against any of these APIs and only ever test against the vendor's showcase account, budget a second, real-company tenant before you ship a schema — it's the difference between a feature existing in your code and a field you never knew to parse.

Adding these three also broke a claim we had been making about filtering, which has its own write-up: [`"full-time"` is not a filter](/blog/ats-employment-type-is-not-one-vocabulary) — Personio's employment-type vocabulary contains neither the word "full" nor "time", so that filter returns zero rows on every Personio board. Location has its own write-up too: [why Teamtailor's `addressRegion` field looks usable and isn't, and why Personio's German place names come back `null`](/blog/ats-location-field-is-not-one-shape).

[ats-jobs-scraper](/go/ats-jobs-scraper) now wraps all nine of these APIs (plus Workday) behind one schema — company, ATS source, title, department, employment type, workplace type, remote flag, location, normalized salary, timestamps, apply URL and description — so a buyer doesn't need to know which of the ten platforms a company happens to use, just its slug. Pay per job posting returned, no start fee, no browser required for any of the ten.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every endpoint and field name above comes from a live request made while writing this post, not from documentation.*
