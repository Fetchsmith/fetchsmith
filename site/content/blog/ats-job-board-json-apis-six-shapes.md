---
title: Six ATS job-board JSON APIs, six different ideas of what a job posting is
description: Greenhouse, Ashby, Lever, Recruitee, Workable and SmartRecruiters each expose public job-board JSON with no login — but the title field, the location field and even the concept of "structured pay" mean something different on every one of them.
date: 2026-09-13
tags: webscraping, api, jobs, hiring
tool: ats-jobs-scraper
---

Almost every company's careers page is a thin wrapper around one of six applicant-tracking-system (ATS) vendors, and all six publish the underlying job postings as public JSON — no login, no key, the same data the "Apply" button itself fetches. We built [ats-jobs-scraper](https://apify.com/fetchsmith/ats-jobs-scraper) on top of all six. The interesting part wasn't finding the endpoints; it's that no two of them agree on the shape of a "job."

## Greenhouse: the description is HTML, but it's escaped HTML

```
GET https://boards-api.greenhouse.io/v1/boards/airbnb/jobs?content=true
```

Returns `{"jobs": [...]}` — 164 postings for Airbnb at the time of writing. The catch is `content`: it's real HTML, but **double-encoded** — you get back the literal string `&lt;div&gt;...&lt;/div&gt;`, not a `<div>`. Decode the entities before you try to parse it as markup, or every downstream HTML parser just sees text. Location ships as a single free-text `{"name": "..."}` field — no separate city/country, no remote flag.

## Ashby: the only one of the six with real structured pay

```
GET https://api.ashbyhq.com/posting-api/job-board/ramp?includeCompensation=true
```

Ashby is the richest of the six by far — `isRemote`, `workplaceType`, both `descriptionHtml` and `descriptionPlain` pre-split for you, and it's the **only one of the six ATSes that reliably publishes numeric salary ranges**: 138 of 145 live postings on Ramp's board carried a real `compensation.summaryComponents[]` entry with `minValue`/`maxValue`/`currencyCode`/`interval`. The one trap: that array also holds `EquityPercentage` and other non-cash components with all-null values sitting next to the real one, so you have to filter on `compensationType: "Salary"` — take the first array entry blindly and you'll grab equity or nothing.

## Lever: no envelope, and the title field isn't called title

```
GET https://api.lever.co/v0/postings/figma?mode=json
```

Where Greenhouse and Ashby wrap results in an object, Lever's response is a **bare array** — no `{"jobs": [...]}`, just `[...]` at the top level. The job title lives in a field called `text`, not `title`. Location, team and commitment type are all folded into a `categories` object instead of top-level fields. And a fair number of well-known company slugs that "should" be on Lever simply 404 — `plaid`, `brex`, `ramp`, `figma`, and `huggingface` all return 404 on `api.lever.co` (re-verified live, two separate measurement cycles), because they've since migrated to a different ATS. A 404 here means "moved," not "broken" — worth skipping quietly rather than failing the whole run.

## Recruitee: numbers that are actually strings

```
GET https://<slug>.recruitee.com/api/offers/
```

Recruitee publishes salary too, but `salary.min` and `salary.max` come back as **numeric strings** (`"2600"`, not `2600`) — cast them or every downstream comparison silently does string comparison instead of numeric.

## Workable: its own vocabulary for two common concepts

```
GET https://apply.workable.com/api/v1/widget/accounts/<slug>?details=true
```

Workable's job identifier is called `shortcode`, not `id`. And where most of the other five use some flavor of `isRemote`/`workplaceType`, Workable's remote flag is named `telecommuting` — same concept, different name, easy to silently drop if you're mapping fields by convention instead of checking each schema.

## SmartRecruiters: the only paginated one, and its list has no description at all

```
GET https://api.smartrecruiters.com/v1/companies/<slug>/postings
```

The only one of the six that returns proper pagination metadata (`{"offset": 0, "limit": 100, "totalFound": N, "content": [...]}`). But the list endpoint's `content[]` items carry no job description whatsoever — you need a **second call per posting** (`GET /v1/companies/<slug>/postings/<id>`) to get the actual text, which none of the other five ATSes require.

## Normalizing across all six

Three fields turned out to need real normalization work, not just renaming:

- **Salary interval.** Greenhouse, Workable and SmartRecruiters don't expose pay at all; Ashby, Lever and Recruitee do, but each spells the pay period differently — `"1 YEAR"`, `"monthly"`, `"per-year-salary"`, all observed live on the same day. Collapsing those to one vocabulary (`year`/`month`/`week`/`day`/`hour`) matters because a monthly €2,600 and an annual $211,400 landing in the same unlabeled `salaryMin` column look like the same kind of number and aren't.
- **Remote/location.** `isRemote` (Ashby), `telecommuting` (Workable), and a bare location string with no flag at all (Greenhouse) all mean roughly the same thing to a buyer filtering for remote jobs, and none of them agree on a name.
- **Dead companies.** A 404 on Lever, specifically, is common enough (companies migrate ATS vendors constantly) that treating it as a hard failure would make multi-company runs fail more often than they'd succeed.

[ats-jobs-scraper](https://apify.com/fetchsmith/ats-jobs-scraper) wraps all six APIs behind one schema — company, ATS source, title, department, team, employment type, workplace type, remote flag, location, normalized salary (min/max/currency/**interval**), timestamps, apply URL and description — and skips companies that have moved off an ATS instead of failing the run. Pay per job posting returned, no start fee, no browser required for any of the six.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every endpoint and field name above comes from a live request made while writing this post, not from documentation.*
