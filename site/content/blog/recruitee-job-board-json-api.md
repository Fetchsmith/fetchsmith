---
title: "Recruitee's job board API: one real filter hiding among ignored ones, and a 42 MB board that's 97% pasted screenshots"
description: <slug>.recruitee.com/api/offers/ serves any company's open roles as public JSON with no key. page, limit, offset and per_page are silently ignored — but department is real, exact-match and case-sensitive, so one wrong capital letter returns an empty board instead of an error. And the largest board we measured is 42 MB for 86 postings, 97.6% of which is base64 PNGs pasted into the job descriptions.
date: 2026-10-19
tags: webscraping, api, jobs, hiring
tool: ats-jobs-scraper
---

Recruitee (now Tellent Recruitee) is the applicant-tracking system behind `<company>.recruitee.com` career pages. We already covered it as one of [six ATS job-board shapes](/blog/ats-job-board-json-apis-six-shapes) and ship it as a source in [ats-jobs-scraper](/go/ats-jobs-scraper); this is the dedicated write-up, alongside the ones on [Greenhouse](/blog/greenhouse-job-board-json-api), [Workday](/blog/workday-career-site-json-api), [Lever](/blog/lever-job-board-json-api-pagination), [Ashby](/blog/ashby-job-board-json-api) and [Workable](/blog/workable-job-board-json-api).

Every number below was measured live on 2026-10-19 against eight real boards: `dpgmedia` (86 postings), `infomedics` (30), `greenchoice` (14), `vandebron` (13), `channable` (12), `nmbrs` (8), `personio` (1) and `tellent` (0).

## The endpoint

```
GET https://<slug>.recruitee.com/api/offers/
```

`slug` is the company's subdomain. No auth header, no key, no cookie. The envelope is `{"offers": [...]}` and each offer carries **56 keys**. A bogus slug is a clean `404` with `{"error":"Not Found"}` — distinguishable from a real board with nothing open, which is a `200` carrying exactly `{"offers":[]}` (13 bytes; `tellent`, Recruitee's own board, is in that state today). That distinction matters if you're crawling a slug list: "this company doesn't use Recruitee" and "this company is not hiring" are different answers and the API does tell them apart.

## No pagination — the whole board, every time

`page`, `limit`, `per_page` and `offset` are all accepted and silently discarded. Against `vandebron` (13 postings, 202,410 bytes):

```
$ curl -s "https://vandebron.recruitee.com/api/offers/"                 | wc -c   # 202410
$ curl -s "https://vandebron.recruitee.com/api/offers/?page=2"          | wc -c   # 202410
$ curl -s "https://vandebron.recruitee.com/api/offers/?limit=2"         | wc -c   # 202410
$ curl -s "https://vandebron.recruitee.com/api/offers/?offset=5"        | wc -c   # 202410
$ curl -s "https://vandebron.recruitee.com/api/offers/?per_page=2"      | wc -c   # 202410
$ curl -s "https://vandebron.recruitee.com/api/offers/?page=2&limit=2"  | wc -c   # 202410
```

Same byte count, same 13 offers, same ids in the same order every time. This puts Recruitee in the same class as [Greenhouse](/blog/greenhouse-job-board-json-api), [Ashby](/blog/ashby-job-board-json-api) and [Workable](/blog/workable-job-board-json-api): you get the entire board or nothing, and [Lever](/blog/lever-job-board-json-api-pagination) remains the only one of the six that honors real `skip`/`limit`.

## But `department` is real — exact-match, case-sensitive, and it fails closed

This is the part worth knowing. Throw a made-up parameter at the endpoint and it's ignored, like the pagination knobs. Throw `department` at it and it filters. On `vandebron`:

```
?nonsense_param=1       -> 13 offers   (ignored)
?location=Amsterdam     -> 13 offers   (ignored)
?location=Nope          -> 13 offers   (ignored)
?remote=true            -> 13 offers   (ignored)
?status=closed          -> 13 offers   (ignored)
?kind=job               -> 13 offers   (ignored)
?department=Marketing   ->  3 offers   (honored — matches the 3 in the payload)
?department=marketing   ->  0 offers   (honored, and case-sensitive)
?department=Nope        ->  0 offers   (honored, fails closed)
```

Confirmed on two more boards: `channable` `department=Support` → 1, `department=support` → 0; `infomedics` `department=IT` → 20, `department=it` → 0; `greenchoice` `department=IT%20%26%20Data` → 2 (ampersands and spaces are fine, it's a literal exact match on the string Recruitee publishes in the `department` field).

So the endpoint silently drops five of the six filters we tried, and the one it does honor is the one that can silently wipe out your result set. A lowercase `department=engineering` returns `{"offers":[]}` with a `200` — exactly the same response as a company that has closed all its roles. This is the mirror image of the [fail-open dropped-filter-name pattern](/blog/government-apis-fail-open-on-a-dropped-filter-name) we've documented on government APIs: there, a typo'd filter name gets ignored and you quietly get *more* rows than you asked for. Here, a typo'd filter *value* gets honored and you quietly get *none*. Both are silent; the empty one is more likely to be mistaken for a real answer.

One more trap in the same parameter: `?department=` (empty value) returns 0 offers, not all of them. And `department` is frequently null in the payload — 66 of `dpgmedia`'s 86 postings have no department at all — so there is no value you can pass that reaches those rows. Server-side `department` filtering can only ever return the subset that has a department set.

## You cannot hash the response to detect changes

Recruitee's JSON key order is **randomized on every request**. Three consecutive identical `curl`s to `vandebron` returned three different MD5s at an identical byte count, with identical offer ids in identical order and not one differing field value once parsed. The first keys of the first offer, across those three responses:

```
["close_at", "options_cover_letter", "max_hours", "position", ...]
["locations_question_type", "location", "mailbox_email", "position", ...]
["options_photo", "options_salutation", "position", "mailbox_email", ...]
```

That's the signature of an Erlang/Elixir map being serialized without an ordering pass — Recruitee's stack. It's harmless until you build the obvious cheap change detector: hash the response body, compare to last run's hash, skip if equal. On Recruitee that detector reports "changed" on every single poll, forever. Diff parsed objects (or offer ids and `updated_at`), never bytes. It's a different failure from the ones in [eight ways a watch mode silently stops working](/blog/incremental-api-watch-mode-four-traps), and it fails noisily rather than quietly, which is the better direction to fail — but it will cost you a full re-process on every poll if you don't know.

## The 42 MB board

`dpgmedia` is 86 postings in a single 41,935,464-byte response. That is 487 KB per posting, and it is not pagination-fixable, because there is no pagination. Where the bytes go:

| Field | Bytes | Share |
|---|---|---|
| `translations` | 20.80 MB | 49.7% |
| `description` | 20.66 MB | 49.3% |
| `open_questions` | 0.20 MB | 0.5% |
| `requirements` | 0.08 MB | 0.2% |
| everything else (52 fields) | 0.12 MB | 0.3% |

`translations` is a per-locale copy of the description, title, requirements and sharing fields (`{"nl": {...}, "en": {...}}` — 84 of the 86 postings carry `nl`, 4 carry `en`). It roughly doubles the payload and there is no flag to turn it off. It's genuinely useful if you want English copy off a Dutch-language board, which is the one case where Recruitee beats the other five ATSes outright — but you pay for it on every request whether you read it or not.

The `description` half is the interesting one.

## 97.6% of that description HTML is pasted screenshots

Recruitee's job-description editor accepts pasted images and inlines them into the description HTML as base64 data URIs. Across `dpgmedia`'s 86 postings:

- **20.15 MB of base64 inside 20.65 MB of description HTML — 97.6%.**
- 10 of 86 postings affected.
- Median description: **6,150 bytes**. Largest: **2,436,168 bytes**, of which 2,426,348 (99.6%) is one `image/png`.

The markup looks like this, mid-sentence, in the middle of a perfectly normal Dutch job ad:

```html
...én krijg je de mogelijkheid om hybride te werken.</p>
<figure><img style="width:790px" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABdwAAAH0C...
```

That single posting is 400x the median. If you're writing those rows to a CSV, the cell is 74x past Excel's 32,767-character limit. If you're writing to a database, one job ad just became your largest row. And you fetched it, parsed it, and stored it to learn nothing about the job.

Worth noting what those 2.4 MB buy, for scale: that is one pasted PNG of an office, and it is *larger* than a full-page PNG screenshot of the entire English Wikipedia article on web scraping, which [we measured at 2,408,123 bytes](/blog/screenshot-png-vs-jpeg-byte-size-measured) — a page far taller and denser than anything a job ad contains. Nobody chose this byte budget; a paste did.

### A 42 MB board is a timeout problem before it's a storage problem

One more consequence, and it's the kind you only find by running the thing somewhere other than your laptop. `dpgmedia` downloads in **0.98 s direct** from a cheap VPS. Through a datacenter proxy it does not finish in 30 seconds — we watched our own scraper burn three attempts and skip the board entirely, with a clean "this company failed to answer, re-run to retry just those" message and zero rows. The same board on the same proxy from the same code now takes **109 s**. 42 MB at ~0.4 MB/s is simply a different request from the 200 KB one next to it.

If you're setting an HTTP timeout for an unpaginated API, one flat `request` budget makes you choose between failing fast on dead hosts and succeeding on big bodies. Split it: cap time-to-first-byte separately (30 s is plenty — a dead board still fails fast) and give the body itself minutes. We now run `{ response: 30_000, request: 150_000 }` for every board fetch in the Actor.

We checked the other ATSes for the same habit on 2026-10-19 and found none — `airbnb` on Greenhouse (2.5 MB), `dnb` on Lever (1.1 MB) and `hireframe` on Workable (399 KB) contain zero `;base64,` occurrences between them. This looks like a Recruitee-editor behavior, not an industry-wide one.

## Recruitee's own vocabulary

Reconfirmed from the six-shapes overview, plus what we found this time:

- `salary.min` / `salary.max` are **numeric strings** (`"2600"`, not `2600`) — cast them or every downstream comparison is a string comparison. `salary.period` is `"yearly"`/`"monthly"`, which matters more on Recruitee than elsewhere because monthly figures are common on its mostly-European boards.
- Remote status is three separate booleans — `remote`, `on_site`, `hybrid` — not one enum.
- `employment_type_code` is snake_case (`fulltime_permanent`), not the human string.
- High-fill fields nothing else in the six exposes: `education_code`, `experience_code` and `category_code` (13/13 each on `vandebron`), and the hours range — `min_hours` 108/163 and `max_hours_per_week` 113/163 across the six multi-posting boards. European part-time hours ranges are a real signal and only Recruitee publishes them.
- The offer object is **56 keys on every board** we checked, with no per-board custom fields leaking into the top level (`dynamic_fields` exists for that and was empty everywhere). Unlike Workday or SmartRecruiters, you can map this schema once and trust it.
- `status` was `"published"` on all 163 postings across all six boards — the endpoint appears to serve only live offers, so don't count on `status` as a filter you can rely on seeing vary.

## Packaged version

[ats-jobs-scraper on Apify](/go/ats-jobs-scraper) handles all of the above for Recruitee: the salary string coercion, the three remote booleans collapsed into one `workplaceType` plus `isRemote`, the pay period normalized to a bare unit shared across all seven sources, and the whole board fetched in one request because that is the only option.

As of this cycle it also strips inline base64 image payloads out of `descriptionHtml` before the row is written. The `<img>` tag stays, with the image type and byte count in place of the payload (`src="data-uri-stripped:image/png:2426348"`), so the HTML still records that an image was there — and that worst-case `dpgmedia` posting goes from 2,436,168 bytes to 9,833, a 248x reduction, with `descriptionText` byte-for-byte unchanged. We deliberately did not make it an option: nobody is buying job data in order to receive a screenshot of an office, and leaving it on by default meant a buyer could pay dataset storage for 20 MB of PNG without ever knowing why their rows were huge.

If you're pulling more than one ATS, the differences between them are the real work: [six ATSes, six ideas of what a job posting is](/blog/ats-job-board-json-apis-six-shapes), [Greenhouse's take](/blog/greenhouse-job-board-json-api), [Lever's](/blog/lever-job-board-json-api-pagination), [Workday's](/blog/workday-career-site-json-api), [Ashby's](/blog/ashby-job-board-json-api), [Workable's](/blog/workable-job-board-json-api) and [SmartRecruiters'](/blog/smartrecruiters-job-board-json-api) — the one other ATS here whose pagination actually works, unlike this one's silently-ignored params.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every endpoint, status code, byte count and field name above comes from a live request made while writing this post, not from documentation.*
