---
title: Four public remote-job APIs with no key — and how small each feed really is
description: Remotive, Remote OK, Jobicy and Arbeitnow all publish remote job postings as JSON with no login. Measured live on two separate days, the four together hold under 200 postings, limit is decorative on one of them, and none of the postings overlap.
date: 2026-09-21
tags: webscraping, api, jobs, hiring
tool: remote-jobs-scraper
---

Four remote-job boards publish their postings as public JSON with no key, no cookie and no login: [Remotive](https://remotive.com), [Remote OK](https://remoteok.com), [Jobicy](https://jobicy.com) and [Arbeitnow](https://www.arbeitnow.com). We merged all four into one normalized schema for [remote-jobs-scraper](https://apify.com/fetchsmith/remote-jobs-scraper), and measured each feed on two separate days before writing anything down.

The headline result is not the one we expected going in. These are not four big overlapping firehoses that need careful de-duplication. They are four small, **disjoint** curated lists, and the interesting engineering problem is coverage, not overlap.

## The four endpoints

```
GET https://remotive.com/api/remote-jobs?limit=50
GET https://remoteok.com/api
GET https://jobicy.com/api/v2/remote-jobs?count=50
GET https://www.arbeitnow.com/api/job-board-api?page=1
```

No auth header on any of them. All four ask for attribution in return, and Remote OK's terms are explicit that a followed link back is the price of access — if you republish these postings, link to the original job URL.

## How many postings you actually get

Measured live on 2026-09-21, and re-measured on a separate pull the same day with the same result:

| Board | Postings available | Notes |
|---|---|---|
| Remote OK | **99** | The array holds 100 elements — see below |
| Jobicy | **50** | `count` caps at 50 |
| Remotive | **20** | The entire public feed, at any `limit` |
| Arbeitnow | **11** remote | Out of 600 rows across 3 pages |

That is under 200 live postings for the whole set. If you are building a job board and assumed "aggregate the free APIs" gets you to thousands of rows, it does not. What it gets you is four differently-curated slices: US-centric startup tech (Remote OK), worldwide tech/design/marketing/support (Remotive), a general worldwide board (Jobicy), and European — largely German — roles (Arbeitnow).

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

## Merging four feeds: sort globally, and know what a small cap samples

Once the four lists are normalized to one schema, the natural merge is global newest-first on `publishedAt`. That has a consequence worth stating out loud, because it looks like a bug the first time you see it.

Ask for 10 rows and you may get 10 rows from a single board. Not because the merge is unfair, but because that board happened to hold the 10 freshest postings that minute. A small cap samples **recency**, not **boards**. A default 100-result run today returned all four:

```
jobicy 50 / remoteok 24 / arbeitnow 14 / remotive 12
```

If you want all four represented, ask for at least 50 results. If you want a guaranteed per-board slice, run the Actor once per board with `sources` set to that one board — that is what the input is for.

## What we shipped

[remote-jobs-scraper](https://apify.com/fetchsmith/remote-jobs-scraper) pulls all four boards, normalizes them into a single row shape (source, title, company, url, location, jobType, category, tags, normalized salary min/max/currency/period, publishedAt), de-duplicates across boards **before** charging, and fails the run on an unparseable date bound rather than silently returning the unfiltered set. It is HTTP-only — no headless browser — and every row carries the source board and the original posting URL so you can honour the attribution these APIs ask for.

## Related guides

- [Six ATS job-board JSON APIs and their shapes](/blog/ats-job-board-json-apis-six-shapes)
- [Workday's public career-site API](/blog/workday-career-site-json-api)
- [All FetchSmith Actors](/tools)

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned.*
