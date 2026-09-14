---
title: Workday's public career-site API has no auth, a hard page-size cap, and no department field
description: Workday powers the career pages of most large enterprises, retailers and government agencies. Its JSON API needs no login — but limit caps at 20, total is only meaningful on the first page, and there's no department field anywhere in either response.
date: 2026-09-14
tags: webscraping, api, jobs, hiring
tool: ats-jobs-scraper
---

Workday is the applicant-tracking system behind most large enterprises, national retailers and government agencies — a different tier of the market from the startup-favored ATSes ([Greenhouse, Ashby, Lever, Recruitee, Workable, SmartRecruiters](/blog/ats-job-board-json-apis-six-shapes)) we'd already covered. Every `myworkdayjobs.com` career site is backed by the same public JSON API the page itself calls, no login required. We verified it live against a real board and shipped it as [ats-jobs-scraper](https://apify.com/fetchsmith/ats-jobs-scraper)'s 7th ATS. Three things about it are easy to get wrong if you only read the happy-path response.

## The endpoint

```
POST https://<tenant>.wd<N>.myworkdayjobs.com/wday/cxs/<tenant>/<site>/jobs
Content-Type: application/json

{"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": ""}
```

`tenant` is the host's first DNS label, `site` is the career-site slug from the URL path. Verified against `okgov.wd1.myworkdayjobs.com/okgovjobs`, a real Oklahoma state government board with 523 live postings at the time of writing. No auth header, no cookie, no login — same class of public JSON API as the other six ATSes.

## `limit` hard-caps at 20

Ask for more and you don't get truncated results — you get a flat rejection:

```
$ curl -s -X POST ".../jobs" -d '{"appliedFacets":{},"limit":25,"offset":0,"searchText":""}'
{"errorCode":"HTTP_400"}
```

No explanatory message, just the error code. Tested at 21 and above; 20 is the ceiling on every tenant we checked. If your pagination logic assumes a larger page size works and falls back on a 400, you'll get there — but there's no reason to find that out the slow way.

## `total` only means anything on the first page

The first response (`offset: 0`) carries a real `total` matching the tenant's actual posting count. Page further in and `total` silently becomes `0` on later responses from the same tenant — not an error, not a changed count, just a field that stops being populated past the first page. This is a real, reproducible platform behavior, not a fluke of one run. The fix is mechanical once you know about it: capture `total` from the `offset: 0` response and reuse that captured value as your pagination stop condition; don't re-read the field on every page.

## There is no department field, anywhere

Neither of Workday's two response shapes carries a department or team field:

- **List** (`jobPostings[]`): `title`, `externalPath`, `locationsText`, `postedOn` (a relative string like `"Posted 3 Days Ago"`, not a real date), `bulletFields`.
- **Detail** (`GET .../wday/cxs/<tenant>/<site><externalPath>`): adds `jobPostingInfo.jobDescription` (full HTML), `.timeType` (`"Full time"`/`"Part time"`), `.startDate` (a real ISO date, unlike the list endpoint's relative string), `.jobRequisitionLocation.descriptor`, `.country.descriptor`, `.externalUrl` — but still no department or team.

The closest real substitute is `hiringOrganization.name` — on the Oklahoma board it returns values like `"131 DEPARTMENT OF CORRECTIONS"`, which is genuinely the owning organizational unit, just modeled as "hiring organization" rather than a dedicated department field. It's a substitute worth documenting plainly as one, not silently passing off as equivalent.

The detail call is also the only way to get an exact posting date and the full description — the list endpoint's `postedOn` is relative and unparseable to an exact timestamp, so if you need real dates you're paying for one extra request per posting either way.

## Dead tenants fail differently than dead companies on the other six ATSes

On Lever, a company that's migrated off the platform 404s cleanly — [documented in the six-ATS post](/blog/ats-job-board-json-apis-six-shapes) as a case worth catching and skipping rather than failing the run. A fake or dead Workday tenant doesn't 404 — it fails at the DNS/proxy layer instead (`Proxy responded with 590 UPSTREAM502: 0 bytes` against a deliberately invalid tenant, tested live). Same outcome either way — catch it, skip that company, keep the run going — but if you're specifically checking "did this company's board respond with a 404," a Workday tenant that's simply wrong won't trip that check. It needs the same broad try/catch around the whole request, not a status-code-specific one.

## Packaged version

[ats-jobs-scraper on Apify](https://apify.com/fetchsmith/ats-jobs-scraper) now covers Workday as a 7th source alongside Greenhouse, Ashby, Lever, Recruitee, Workable and SmartRecruiters, normalized into the same schema — company, ATS source, title, department (via `hiringOrganization.name` for Workday), employment type, remote flag, location, salary, timestamps, apply URL and description. Detail-level fields (department, employment type, exact date) only cost the extra request when `includeDescriptions` is on, same tradeoff the SmartRecruiters integration already makes.

If you're pulling from the other six ATSes too, see [how their title, location and salary fields all mean something slightly different from each other](/blog/ats-job-board-json-apis-six-shapes) — Workday adds an eighth idea of what a "job" looks like to that list.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every endpoint, status code and field name above comes from a live request made while writing this post, not from documentation.*
