---
title: Six public remote-job APIs with no key — and how small each feed really is
description: Remotive, Remote OK, Jobicy, Arbeitnow, Working Nomads and Himalayas all publish remote job postings as JSON with no login. Measured live over four separate days, the six together sample to a few hundred postings, limit is decorative or entirely ignored on three of them, and only one pair of boards genuinely syndicates.
date: 2026-09-21
tags: webscraping, api, jobs, hiring
tool: remote-jobs-scraper
---

Six remote-job boards publish their postings as public JSON with no key, no cookie and no login: [Remotive](https://remotive.com), [Remote OK](https://remoteok.com), [Jobicy](https://jobicy.com), [Arbeitnow](https://www.arbeitnow.com), [Working Nomads](https://www.workingnomads.com) and [Himalayas](https://himalayas.app). We merged all six into one normalized schema for [remote-jobs-scraper](https://apify.com/fetchsmith/remote-jobs-scraper), and measured each feed on separate days before writing anything down.

The headline result is not the one we expected going in. Five of these are not big overlapping firehoses that need careful de-duplication — they are small curated lists that are *mostly* disjoint, and the interesting engineering problem is coverage, not overlap. Himalayas is the outlier: its own count of total live postings is in the hundred-thousands, two to three orders of magnitude past any of the other five (see the update at the end).

> **This post was written on 2026-09-21 covering four boards** — which is why the URL says `four-feeds`. Working Nomads was added 2026-09-23 and Himalayas the same day, each measured in its own section at the end of this post, with the numbers re-taken on the day added rather than folded into the older table. The URL is left alone so existing links keep working.

## The five endpoints

```
GET https://remotive.com/api/remote-jobs?limit=50
GET https://remoteok.com/api
GET https://jobicy.com/api/v2/remote-jobs?count=50
GET https://www.arbeitnow.com/api/job-board-api?page=1
GET https://www.workingnomads.com/api/exposed_jobs/
```

No auth header on any of them. All of them ask for attribution in return, and Remote OK's terms are explicit that a followed link back is the price of access — if you republish these postings, link to the original job URL.

## How many postings you actually get

Measured live on 2026-09-21 across the original four boards, and re-measured on a separate pull the same day with the same result (Working Nomads, added later, is measured separately at the end):

| Board | Postings available | Notes |
|---|---|---|
| Remote OK | **99** | The array holds 100 elements — see below |
| Jobicy | **50** | `count` caps at 50 |
| Remotive | **20** | The entire public feed, at any `limit` |
| Arbeitnow | **11** remote | Out of 600 rows across 3 pages |

That is under 200 live postings for these four (about 250 once Working Nomads is added — still the same order of magnitude). If you are building a job board and assumed "aggregate the free APIs" gets you to thousands of rows, it does not. What it gets you is four differently-curated slices: US-centric startup tech (Remote OK), worldwide tech/design/marketing/support (Remotive), a general worldwide board (Jobicy), and European — largely German — roles (Arbeitnow).

## `limit` is decorative on Remotive

Remotive accepts a `limit` parameter and ignores it in the direction you care about:

```
$ curl -s "https://remotive.com/api/remote-jobs?limit=9"   | jq '.["job-count"], (.jobs|length)'
20
20
$ curl -s "https://remotive.com/api/remote-jobs?limit=45"  | jq '.["job-count"], (.jobs|length)'
20
20
$ curl -s "https://remotive.com/api/remote-jobs?limit=500" | jq '.["job-count"], (.jobs|length)'
20
20
```

Twenty postings at every limit, and the response's own `job-count` agrees. No error, no truncation warning, no pagination cursor to follow. Twenty is the whole feed. If your ingest logs "fetched 20 of a requested 500" as a partial failure and retries, you will retry forever; treat a short response from this endpoint as complete.

## Remote OK's first array element is not a job

The `/api` response is a bare JSON array of 100 elements, and element `[0]` is a legal notice:

```json
{
  "last_updated": 1789862431,
  "legal": "API Terms of Service: Please link back (with follow, and without nofollow!) to the URL on Remote OK and mention Remote OK as a source..."
}
```

It has no `position`, no `company`, no `id`. Map straight over the array and every run produces one junk row with null everywhere — which on a pay-per-result pipeline is a row you pay for. Filter on the presence of a real field (we use `position`) rather than slicing `[1:]`, because the notice's index is not a documented guarantee.

Also worth knowing: Remote OK publishes `salary_min` / `salary_max` as **`0`** when a salary is not disclosed, not as `null`. Sixteen of today's 99 rows carried a real number. Passing the zeros straight through gives you a chart full of $0 jobs.

## Arbeitnow serves 250 rows per page to give you 9 remote ones

Arbeitnow is a general European job board, not a remote-only one, and the API has no server-side remote filter. You page through everything and filter client-side on the `remote` boolean:

```
page 1: 250 rows ->  9 remote
page 2: 250 rows ->  2 remote
page 3: 100 rows ->  0 remote
```

Eleven useful postings out of 600 rows — a hit rate under 2%. There is no `meta.total` to plan against either, so you cannot know how deep to page before you start. This is the one source where the cost of the request and the value of the response are wildly mismatched, and it is why our Actor defaults to 2 pages of Arbeitnow rather than exhausting it.

## Almost none of the postings overlap

The reason to merge boards is usually that a syndicated posting appears on several of them and you want to pay for it once. We measured it directly: normalize company and title (stripping legal-entity suffixes like "Inc"/"LLC" so "Acme Inc" and "Acme" still match), take the set union across all four boards, and count keys appearing more than once.

```
total rows        193
unique keys       191
keys on >1 board  2
```

Two, out of 193 — one of them only found because the two copies of the posting spelled the employer "Sanctuary Computer Inc" on one board and "Sanctuary Computer" on the other; a bare string match misses that. An independent pull the same week gave 0 of 181. These four boards mostly do not syndicate to each other; each one curates its own set, and true overlap is a handful of postings, not a volume story.

The overlap that *does* exist beyond that is at the company level, and it is tiny — two companies today posted different roles on two different boards (`imerit technology` on Remotive and Remote OK, `hey contact heroes gmbh` on Remotive and Arbeitnow). Those are genuinely different openings and should stay as separate rows.

So de-duplication across these boards is worth building as a **guarantee** — you will never be billed twice for one posting — but not as a volume story. Anyone selling you "we deduplicate millions of aggregated remote jobs" from these four sources is describing a step that, on the measured data, removes almost nothing.

**Partly superseded by the fifth board.** Adding Working Nomads changed this conclusion in one specific direction — see the update at the end. It is still not a volume story, but "the boards do not syndicate to each other" turned out to be a statement about *which four boards we had measured*, not about public remote-job feeds in general.

## Merging the feeds: sort globally, and know what a small cap samples

Once the lists are normalized to one schema, the natural merge is global newest-first on `publishedAt`. That has a consequence worth stating out loud, because it looks like a bug the first time you see it.

Ask for 10 rows and you may get 10 rows from a single board. Not because the merge is unfair, but because that board happened to hold the 10 freshest postings that minute. A small cap samples **recency**, not **boards**. A default 100-result run that day (before Working Nomads was added) returned all four:

```
jobicy 50 / remoteok 24 / arbeitnow 14 / remotive 12
```

If you want every board represented, ask for at least 50 results. If you want a guaranteed per-board slice, run the Actor once per board with `sources` set to that one board — that is what the input is for.

## Update, 2026-09-23: a fifth feed — Working Nomads

[Working Nomads](https://www.workingnomads.com) publishes the same way the other four do — one `GET`, no key, no cookie:

```
GET https://www.workingnomads.com/api/exposed_jobs/
```

The response is a bare JSON array (no envelope, no `meta`, no cursor) of **58 postings**, measured 2026-09-23 and confirmed identical on a second independent pull the same day (same 58 rows, same 265 KB, every `pub_date` offset `-04:00`). That puts it second by size behind Remote OK and comfortably ahead of Remotive, which was down to 19 postings on the same day.

### Every query parameter is ignored

Remotive's `limit` is decorative in one direction. Working Nomads is more absolute — there is no parameter that does anything at all:

```
GET /api/exposed_jobs/            -> 200, 58 rows
GET /api/exposed_jobs/?page=2     -> 200, 58 rows
GET /api/exposed_jobs/?limit=5    -> 200, 58 rows
GET /api/exposed_jobs/?count=5    -> 200, 58 rows
GET /api/exposed_jobs/?offset=50  -> 200, 58 rows
```

Same 200, same 58 rows, every time. There is nothing to paginate: the array is the whole feed, and the feed is a rolling window — the oldest posting in it was published 2026-08-25, about a month back. Cap results client-side and re-poll for freshness; there is no deeper archive to walk.

### 92% of the response is job-description HTML

The response is 265 KB for 58 postings. That is roughly 4.5 KB per posting, and almost all of it is one field:

| | |
|---|---|
| Response size | 265 KB |
| Total `description` bytes | 243 KB (**92%**) |
| Median `description` | 4,256 characters |
| Largest `description` | 8,981 characters |
| Postings with HTML in `description` | 58 of 58 |

Every description is HTML fragments (`<p>`, `<strong>`, `<a>`), never plain text. Budget for that if you are storing rows or passing them to a model — the description dominates the row, and it arrives whether you asked for it or not.

### The shape has four gaps worth knowing before you map it

```json
{
  "url": "https://www.workingnomads.com/job/go/1885527/",
  "title": "Senior back-end Engineer",
  "company_name": "Lemon.io",
  "category_name": "Development",
  "location": "EU, US, Canada, UK, Australia, Singapore, Ireland, Norway, Switzerland, Iceland, and Mexico",
  "tags": "back-end,golang,python,kubernetes,software engineering",
  "pub_date": "2026-09-23T06:49:46-04:00",
  "description": "<p><strong>Senior Developer? Work Remote...</strong></p>"
}
```

Eight keys, and that is the entire schema. What is missing or awkward:

1. **There is no id field.** Not `id`, not `slug`, not `guid`. The posting's own `url` is the only stable identifier — it was unique across all 58 rows, and it is what we key de-duplication on.
2. **There is no salary field at all.** Not null, not zero — absent. Remote OK's disclosed-as-`0` trap (above) has no equivalent here because there is nothing to misread.
3. **`tags` is a comma-joined string, not an array** — and it was empty on 1 of 58 rows, so split defensively.
4. **`pub_date` carries a `-04:00` offset, not `Z`.** Parse it as an aware datetime. Treating the string as UTC, or slicing the first 10 characters for a date, shifts postings published late in the US evening onto the wrong day.

`location` is free text and will not resolve to a country code — the 58 rows include `"Anywhere in the world"`, `"North America"`, and comma-lists of up to eleven countries.

### The overlap finding, re-measured across all five

Re-running the same normalize-company-and-title union from earlier in this post, now over five boards on 2026-09-23:

```
total rows        250
unique keys       240
keys on >1 board  5
```

Still a small number — but **4 of those 5 duplicate postings are Working Nomads ↔ Remotive**, and the fifth is the Remote OK ↔ Remotive pair the original pass found. Every cross-board duplicate this time involved Remotive on one side:

```
workingnomads + remotive   telus digital     "content reviewer united states"
workingnomads + remotive   lemon io          "senior data scientist"
workingnomads + remotive   lemon io          "senior .net full stack developer"
workingnomads + remotive   lemon io          "senior qa engineer"
remoteok      + remotive   sanctuary computer "senior shopify developer"
```

An earlier, independent run on a different pull — the integration run when we added the board — found the same thing from the other direction: Working Nomads' copy of Lemon.io's "Senior QA Engineer" collapsed against Remotive's. Two separate measurements, same pairing.

That is a real change in kind, not just in count. The four-board conclusion was "these boards do not syndicate to each other"; the honest five-board conclusion is that **one pair of them does**, concentrated in a few high-volume advertisers (Lemon.io alone accounts for three of the five). If you add Working Nomads to a Remotive pipeline without de-duplicating, you will pay for those rows twice — which on a per-result price is the whole argument for doing the merge in one place.

Company-level overlap grew too: four companies now appear on Working Nomads and at least one other board (`lemon io`, `telus digital`, `imerit technology` — which is on three boards — and `sticker mule`). As before, those are genuinely different openings and stay as separate rows.

## Update, 2026-09-23: a sixth feed — Himalayas, and it is a different shape of source entirely

[Himalayas](https://himalayas.app) is not a small curated list like the other five. Its own response reports **101,778 total live postings** — two to three orders of magnitude past any board measured above. Finding the real endpoint took more effort than any of the others:

```
GET https://himalayas.app/api/jobs      -> 404
GET https://himalayas.app/api/v1/jobs   -> the HTML app shell, not JSON
GET https://himalayas.app/jobs/api      -> 200, real JSON
```

Neither documented-looking path works; the real endpoint was only found by reading the string embedded in the site's own JSON `comments` field. It is cursor-paginated:

```json
{"jobs": [...], "nextCursor": "…", "totalCount": 101778}
```

`?limit=` is ignored the way Working Nomads ignores every parameter — tested at 50, 100 and 200, the page is always **exactly 20 jobs**, so depth into the ~102k-job inventory is governed purely by how many pages you request, the same shape as Arbeitnow's page-count cap rather than a page-size parameter. Jobs are sorted newest-first. Like Working Nomads, there is no dedicated id field — the job's own permalink (`guid`) is the only stable per-posting key.

### The overlap finding, re-measured across all six

Re-running the same normalize-company-and-title union, now over six boards on 2026-09-23, sampling five boards in full plus 100 of Himalayas' newest postings (5 pages at Himalayas' fixed 20-per-page):

```
total rows        352
unique keys       340
keys on >1 board  5
```

The count of true cross-board duplicates did not move — **still the same 5 pairs found in the five-board measurement above, all of them Working Nomads/Remotive or Remote OK/Remotive.** Himalayas' 100 sampled postings matched none of them. At this inventory's scale that is expected, not a finding about syndication: 100 rows out of a 102k-posting board is a thin enough slice that even real overlap with a 20-50-posting curated board would often miss by chance. This number should not be read as "Himalayas doesn't syndicate" — it is "this sample was too small to tell," which is itself worth knowing before you build a coverage claim on top of it.

**A different kind of duplicate showed up while re-running this: two boards had their own internal repeats.** Arbeitnow listed "SouthwestX — CEO / Business Co-Founder" and "BDF EXPERTS — Senior SAP Berater" twice each within its own 2-page pull, and Working Nomads listed Peroptyx's "AI Content Analyst" twice and "Data Analyst" **four times** within its single 58-row feed. These are same-board, not cross-board — a board re-posting or re-syndicating its own listing — and they are exactly as billable-twice as a cross-board duplicate if you only dedupe across sources and not within one. The Actor's de-duplication key does not care which board a repeat comes from, so this is already handled, but it's a real shape worth knowing if you are building your own merge from scratch: don't assume one board's own feed is internally unique.

## What we shipped

[remote-jobs-scraper](https://apify.com/fetchsmith/remote-jobs-scraper) pulls all six boards, normalizes them into a single row shape (source, title, company, url, location, jobType, category, tags, normalized salary min/max/currency/period, publishedAt), de-duplicates across **and within** boards **before** charging, and fails the run on an unparseable date bound rather than silently returning the unfiltered set. It is HTTP-only — no headless browser — and every row carries the source board and the original posting URL so you can honour the attribution these APIs ask for.

## Related guides

- [Six ATS job-board JSON APIs and their shapes](/blog/ats-job-board-json-apis-six-shapes)
- [Workday's public career-site API](/blog/workday-career-site-json-api)
- [All FetchSmith Actors](/tools)

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned.*
