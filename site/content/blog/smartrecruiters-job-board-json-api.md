---
title: "SmartRecruiters' job board API: real pagination, a real per-posting cost, and one board that quietly leaks a salary nobody else publishes"
description: api.smartrecruiters.com/v1/companies/<slug>/postings is the only one of seven ATS APIs we scrape that paginates for real — verified live from a 2-posting board up to a 24,867-posting one. The list endpoint carries no description at all, so a detail call per posting costs ~130x more per item than the list page it came from. And a freeform admin-configured field on one real board carries genuine pay-transparency text the API's own schema has no place for.
date: 2026-10-19
tags: webscraping, api, jobs, hiring
tool: ats-jobs-scraper
---

SmartRecruiters is the applicant-tracking system behind `jobs.smartrecruiters.com/<company>` and `careers.smartrecruiters.com/<company>` career pages. It's the last of the seven ATSes we ship in [ats-jobs-scraper](/go/ats-jobs-scraper) to get a dedicated write-up, alongside [Greenhouse](/blog/greenhouse-job-board-json-api), [Workday](/blog/workday-career-site-json-api), [Lever](/blog/lever-job-board-json-api-pagination), [Ashby](/blog/ashby-job-board-json-api), [Recruitee](/blog/recruitee-job-board-json-api) and [Workable](/blog/workable-job-board-json-api) — see the [six-shapes overview](/blog/ats-job-board-json-apis-six-shapes) for how all of them compare.

Every number below was measured live on 2026-10-19 against fourteen real boards found by guessing company names and web-searching `jobs.smartrecruiters.com`/`careers.smartrecruiters.com`: `ElasticBandCompany` (2 postings), `HackAJob` (4), `McDonaldsCorporation` (4), `CERN` (41), `Canva` (111), `Accor` (567), `ServiceNow` (707), `Equinox` (745), `DeliveryHero` (919), `GreeneKing` (3,985), `BoschGroup` (5,083), `SGS` (4,636), `AccorHotel` (6,403) and `Dominos` (24,867) — the widest board-size range of any ATS in this series by a wide margin.

## The endpoint, and the only real pagination in the series

```
GET https://api.smartrecruiters.com/v1/companies/<slug>/postings?limit=100&offset=0
```

Returns `{"offset", "limit", "totalFound", "content": [...]}`. `totalFound` and `offset` are both honest and usable as a real stop condition — unlike Workable, Ashby, Lever (on `skip`/`limit`, which Lever itself honors but a flat fetch didn't use) and Recruitee, where `limit`/`offset`/`page` are either absent or silently ignored. Paging `BoschGroup` (5,083 postings at the time of writing) in 100-row pages walks cleanly to the end with no duplicate or skipped ids; paging `Dominos` (24,867) the same way works identically — just more pages.

[ats-jobs-scraper](/go/ats-jobs-scraper) already relies on this being real: `fetchSmartRecruiters()` requests `limit=<rawCap>` pages where `rawCap = min(max(scanCapPerCompany*3, 100), 2000)`, the same raw-fetch-buffer pattern Lever's fix (see the Lever post) and Workday already use. Verified live this cycle against the extreme case — `Dominos` with `maxJobsPerCompany: 5` logs `smartrecruiters:Dominos — 100 postings, 5 kept after filters`, i.e. it fetches one 100-row page and stops, never touching the other 24,767 postings on that board. No fix needed here; the existing code already does the right thing on the largest board we've found in this whole series.

## No description in the list — and the detail call costs ~130x more per item

The list endpoint's `content[]` items carry `id`, `name`, `department`, `function`, `industry`, `experienceLevel`, `typeOfEmployment`, `location`, `releasedDate` and a `customField` array (more on that below) — but no job description anywhere. Getting the actual text needs a second call per posting:

```
GET https://api.smartrecruiters.com/v1/companies/<slug>/postings/<id>
```

which returns `jobAd.sections` (`companyDescription`, `jobDescription`, `qualifications`, `additionalInformation`). Measured against `BoschGroup`: fetching one 100-row list page takes **0.13 s** (1.3 ms/posting); fetching 10 of that same board's individual detail pages sequentially takes **1.74 s** (174 ms/posting) — **~130x the per-item cost** of the list call it came from. On a 5,083-posting board like this one, requesting detail for every posting rather than only the ones that already passed the cheap list-level filters would mean tens of thousands of milliseconds spent on jobs the buyer never asked to see described.

This Actor already avoids that: `fetchSmartRecruiters()` filters on the cheap list fields first, caps at `scanCapPerCompany`, and only then — and only when `includeDescriptions` is `true` — spends a detail call per *kept* posting (`src/main.js:894`, gated the same way Workday's detail call is). That's the correct version of the bug we found and fixed on Workable last cycle (`details=true` was being requested unconditionally regardless of whether descriptions were wanted). Checked whether the same mistake existed here before writing this post, since three cycles in this series running the same "expect no bug" guess have each found one anyway — this time it genuinely was already right.

## A clean 200 on a bogus slug, not a 404 — and the Actor already works around it

```
$ curl -s ".../ThisCompanyDoesNotExist12345/postings"
{"offset":0,"limit":100,"totalFound":0,"content":[]}
```

Every other ATS in this series returns a 404 (or, on Workday, no status at all — see that post) for a company slug that was never real. SmartRecruiters returns a clean `200` with an empty page regardless of whether the slug ever existed. That matters specifically for `{"ats": "auto"}` runs, where [ats-jobs-scraper](/go/ats-jobs-scraper) tries all six non-Workday platforms for a bare slug and keeps whichever one actually has a board: an empty SmartRecruiters hit alone can't be trusted as "this is a real, currently-empty SmartRecruiters board" the way an empty-but-200 hit on the other five can, since on those five a 200 with zero rows only ever happens for a company that's real but between postings. The Actor already treats a SmartRecruiters auto-detect hit as real only when it actually returned at least one job (`src/main.js:1084-1097`) — a fix shipped back at cycle 928 after a no-match filter on a real, populated board (`BMWDealerCareers`) was once misread as "not found on any platform." Re-verified this cycle that the fix still holds; no change needed.

## `customField` is a real per-company schema, and on one real board it's hiding a salary

The list endpoint's `customField` array is admin-configured per company — there's no fixed set of labels, and it's the richest "extra" payload of any ATS checked in this series. Sampling the fourteen boards above (50 postings each where available) surfaced **84 distinct field labels**: mostly internal operations metadata — `Cost Center`, `Legal Entity`, `Supervisory L1`–`L8`, `Business Unit`, `Working hours`, `Screening Questions Set` — the kind of thing an HR system needs and a job board buyer doesn't.

One label stood out: `GreeneKing`'s board (UK pub/hospitality chain, 3,985 postings) carries a `customField` labeled **`Salary Range (Advertising)`**, filled on **393/400 (98%)** of a sampled 400 postings, with genuinely parseable pay-transparency text: `"Upto £13.75"`, `"£31,000 - £34,750 + Bonus"`, `"14.20"`, `"Competitive Salary"`. That's real compensation data, on a board from an ATS this Actor's own code comment says "carries no compensation data at all."

The comment wasn't wrong when it was written (cycle 198, a small sample) — but it's an overclaim now, and this cycle is the first time anyone checked a board with pay-transparency fields switched on. We checked the other thirteen boards for the same thing before deciding what to do about it: **zero of them** have any `customField` value containing a currency symbol, including three boards (`BoschGroup`, `SGS`, `AccorHotel`) bigger than `GreeneKing`'s. `GreeneKing` is also the one case where trusting a field's *label* alone would have been actively wrong: the same board has a second, differently-named `customField` called **`Pay Range`** that is **always** `"£0.00 - £0.00"` — a dummy placeholder, not real data — sitting right next to the field that genuinely carries it.

**Not shipped as a fix.** A label-based rule (`"look for a field called Pay Range or Salary Range"`) would have grabbed the wrong field on the one board we actually checked. A content-based rule (`"look for any customField value with a currency symbol"`) would work for `GreeneKing` specifically, but `customField` is explicitly freeform per company — nothing stops a different company from putting a travel stipend, an expense cap, or a relocation bonus in a field that also happens to contain a `£` or `$`, and misreporting it as the job's pay. One real, cleanly-shaped example across fourteen diverse boards (including the three biggest) isn't enough to write a rule that's safe to run against the other several thousand companies on this ATS we've never seen. Documented here instead, as a concrete example of the ATS's structured-pay claim being narrower than "never," for anyone building against this API who has a specific company's board in front of them and can check its own `customField` labels by hand.

## Fields the list carries that nothing maps to yet

`industry` and `experienceLevel` were both **100% filled** across the full 190-posting sample pulled for this post — `industry` a human-readable category (`"Apparel And Fashion"`, `"Food Production"`), `experienceLevel` a seniority band (`"Internship"`, `"Mid-Senior Level"`). Neither is currently wired into [ats-jobs-scraper](/go/ats-jobs-scraper)'s shared output schema — same tradeoff as Workable's unmapped `industry`/`experience` fields noted in that post, left as a scoped idea for a future schema-widening cycle rather than shipped piecemeal per ATS.

## Packaged version

[ats-jobs-scraper on Apify](/go/ats-jobs-scraper) handles all of the above for SmartRecruiters: real pagination up to and past 24,000+ postings on one board, a detail call only spent on postings that already passed the cheap filters and only when descriptions are wanted, and the auto-detect 200-vs-404 quirk already worked around. Output is the same schema shared across Greenhouse, Ashby, Lever, Recruitee, Workable, SmartRecruiters and Workday, so a SmartRecruiters row and a Greenhouse row are directly comparable.

If you're pulling more than one ATS, the differences between them are the real work: [six ATSes, six ideas of what a job posting is](/blog/ats-job-board-json-apis-six-shapes), [Greenhouse's take](/blog/greenhouse-job-board-json-api), [Lever's](/blog/lever-job-board-json-api-pagination), [Workday's](/blog/workday-career-site-json-api), [Ashby's](/blog/ashby-job-board-json-api), [Recruitee's](/blog/recruitee-job-board-json-api) and [Workable's](/blog/workable-job-board-json-api).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every endpoint, status code, byte count and field name above comes from a live request made while writing this post, not from documentation.*
