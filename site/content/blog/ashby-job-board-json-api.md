---
title: "Ashby's job board API: no pagination, no size cap, and pay bands baked into one number"
description: api.ashbyhq.com/posting-api serves any company's open roles as public JSON with no key. There's no limit/offset param at all — a 814-posting board arrives as one 13.5 MB response, descriptions included whether you want them or not — but the compensation field already does the hard part of merging multi-location pay bands for you.
date: 2026-10-19
tags: webscraping, api, jobs, hiring
tool: ats-jobs-scraper
---

Ashby is the applicant-tracking system behind `jobs.ashbyhq.com/<company>` career pages, and every board is backed by the same public JSON endpoint — no key, no cookie, no login. We already covered it as one of [six ATS job-board shapes](/blog/ats-job-board-json-apis-six-shapes) and ship it as a source in [ats-jobs-scraper](/go/ats-jobs-scraper); this is the dedicated write-up, alongside [the ones on Greenhouse](/blog/greenhouse-job-board-json-api), [Workday](/blog/workday-career-site-json-api) and [Lever](/blog/lever-job-board-json-api-pagination).

Every number below was measured live on 2026-10-19 against five real boards of very different sizes — `linear` (29 postings), `webflow` (20), `notion` (129), `ramp` (167) and `openai` (814).

## The endpoint

```
GET https://api.ashbyhq.com/posting-api/job-board/<slug>?includeCompensation=true
```

`slug` is the company's board name — the path segment in `jobs.ashbyhq.com/<slug>`. No auth header of any kind. A bogus or migrated-off slug returns a clean `404` (same friendly shape as Greenhouse and Lever) — re-verified fresh this cycle on three companies that no longer board here: `retool`, `rippling`, `anthropic`. The response is an envelope, `{"jobs": [...]}`, with each job carrying a `isListed` flag; every posting returned on all five boards above had `isListed: true` — the public endpoint doesn't appear to leak unlisted/draft postings for us to filter out, so there's nothing to guard against there.

## No pagination parameters exist at all — not even silently-discarded ones

Greenhouse accepts `page`/`per_page`/`limit` and quietly ignores them. Lever's `skip`/`limit` are real and change the result. Ashby has **no such parameters whatsoever** — there is nothing to pass, honored or not, and a board of any size comes back as one response:

| board | postings | full response size |
|---|---|---|
| `webflow` | 20 | 440,875 B |
| `linear` | 29 | 402,338 B |
| `notion` | 129 | 2,365,579 B (2.4 MB) |
| `ramp` | 167 | 3,037,506 B (3.0 MB) |
| `openai` | 814 | 13,559,863 B (13.6 MB) |

814 postings is a modest board by the standards of this niche — Lever's `jobgether` was 4,222 — but it already costs 13.6 MB in one request with no way to ask for less. There's no cap to find in testing because there's no knob to turn: unlike Lever (which forced our hand with real `skip`/`limit` support we weren't using), Ashby gives nothing to request a narrower slice with, so [ats-jobs-scraper](/go/ats-jobs-scraper) fetches the whole body on every run and applies `maxJobsPerCompany` after the fact, same as it has to for Greenhouse.

## Descriptions aren't behind a flag — they're always in the response

Greenhouse's `content=true` is an opt-in that roughly doubles response size. Ashby has no equivalent switch: `descriptionHtml` and `descriptionPlain` are present on every job whether or not the caller wants them.

```
$ curl -s ".../openai?includeCompensation=true" | wc -c   # 14,225,286
$ curl -s ".../openai"                                    | wc -c   # 13,559,863
```

The *only* optional query param that exists at all, `includeCompensation`, adds compensation data for **4.9% more bytes** (665,423 B on top of 13,559,863 B for `openai`'s 814 postings) — nowhere near Greenhouse's 18.6x multiplier for `content=true`, because the expensive part (full job descriptions) was never optional to begin with. If your use case is "list open roles, no descriptions," Ashby still makes you pay for the HTML on the wire; [ats-jobs-scraper](/go/ats-jobs-scraper)'s `needDescriptions` input only controls whether that already-downloaded text gets written to the output row, not whether it gets fetched.

## Structured fields are reliably filled — a sharp contrast with Greenhouse

Every field we checked was present on **100% of postings on every one of the five boards**, data or no data to put in it:

| board | n | `department` | `team` | `employmentType` | `compensation` object present |
|---|---|---|---|---|---|
| `webflow` | 20 | 20/20 | 20/20 | 20/20 | 20/20 |
| `linear` | 29 | 29/29 | 29/29 | 29/29 | 29/29 |
| `notion` | 129 | 129/129 | 129/129 | 129/129 | 129/129 |
| `ramp` | 167 | 167/167 | 167/167 | 167/167 | 167/167 |
| `openai` | 814 | 814/814 | 814/814 | 814/814 | 814/814 |

`isRemote` is the one boolean that genuinely varies — not because the field is unreliable, but because it reflects real company policy: `webflow` and `linear` are 100% remote-flagged, `ramp` 89.8% (150/167), `notion` 63.6% (82/129) and `openai` 65.1% (530/814). It's always a real `true`/`false`, never `null` — a cleaner shape than Greenhouse, where remote status is buried in a free-form `metadata` array that's absent on some boards entirely.

## One compensation field, several pay bands — and Ashby already merges them for you

Some postings carry more than one geography-based pay tier. On `openai`'s 814 postings, 8 had 2 or 3 `compensationTiers` — distinct salary bands keyed to where you'd actually sit:

```
"Senior Technical Program Manager - Security" (US - Remote):
  San Francisco, Seattle or New York:  $207,000 – $285,000
  Zone A:                              $186,300 – $256,500
  Zone B:                              $165,400 – $228,000
```

That could easily become a bug for anyone who parses `compensationTiers[0]` as "the" salary — you'd report this role's range as $207K–$285K and miss that it goes as low as $165.4K depending on where the hire actually lives. Ashby avoids that trap itself: the payload also carries `summaryComponents`, a pre-merged figure spanning every tier — `$165.4K – $285K` for the job above, confirmed as literally `min(all tier minimums)` to `max(all tier maximums)` across all 8 multi-tier postings we checked. [ats-jobs-scraper](/go/ats-jobs-scraper)'s `ashbySalary()` already reads `summaryComponents` first (`src/main.js:592`), so our `salaryMin`/`salaryMax` output is the correct merged range without any change needed — worth confirming rather than assuming, since the same multi-tier shape elsewhere could easily be a one-tier-only bug if you build your own parser against `compensationTiers` directly instead.

## Packaged version

[ats-jobs-scraper on Apify](/go/ats-jobs-scraper) handles all of the above for Ashby — the full board on every run (there's no partial-fetch option on this ATS), `descriptionHtml`/`descriptionPlain` passed through only when `needDescriptions` is set, and `salaryMin`/`salaryMax` read from Ashby's own pre-merged `summaryComponents` rather than the first pay tier found. Output is the same schema shared across Greenhouse, Ashby, Lever, Recruitee, Workable, SmartRecruiters and Workday, so an Ashby row and a Greenhouse row are directly comparable.

If you're pulling more than one ATS, the differences between them are the real work: [six ATSes, six ideas of what a job posting is](/blog/ats-job-board-json-apis-six-shapes), [Greenhouse's take](/blog/greenhouse-job-board-json-api), [Lever's](/blog/lever-job-board-json-api-pagination), [Workday's](/blog/workday-career-site-json-api), [Workable's](/blog/workable-job-board-json-api), [Recruitee's](/blog/recruitee-job-board-json-api) — the one board shape where a single posting can be 2.4 MB because somebody pasted a screenshot into the job ad — and [SmartRecruiters'](/blog/smartrecruiters-job-board-json-api), the only ATS in this whole series with pagination that actually works.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every endpoint, status code, byte count and field name above comes from a live request made while writing this post, not from documentation.*
