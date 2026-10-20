---
title: "\"full-time\" is not a filter: employmentType across ten ATS job-board APIs"
description: Ten applicant-tracking systems publish an employment-type field ten different ways — two never populate it, one is free text the employer typed, and on Personio the string "full-time" matches zero postings because its vocabulary contains neither word.
date: 2026-10-19
tags: webscraping, api, jobs, hiring
tool: ats-jobs-scraper
---

If you are pulling public job boards and you want only the full-time roles, the obvious move is to filter on the employment-type field. It is also the move most likely to hand you an empty result set and no error.

We normalize ten applicant-tracking systems into one schema in [ats-jobs-scraper](/go/ats-jobs-scraper), so we have had to decide, per platform, what `employmentType` even means. The short answer: it is not one field with one vocabulary. It is three different kinds of field wearing the same name, and on two platforms it does not exist at all.

## The three kinds of employment-type field

**Closed vocabulary.** Ashby, SmartRecruiters, Workable, Recruitee, Breezy, Personio and Workday each publish a small fixed set of values. These are the ones you can actually filter on — once you know the set.

**Free text.** Lever's `commitment` is whatever the employer typed into it. Across eight boards and 1,913 postings we counted **18 distinct values**, including several that aren't employment types at all: `Remote`, `International EOR`, `International Office Entity`. The same concept splits four ways between boards — `Full-time`, `Full Time`, `Full Time Employee`, `Permanent`. About 2% are `null`.

**Absent.** Greenhouse's board API has no employment-type field in its schema, so every Greenhouse row is `null` — not a per-board configuration gap, a modelling gap upstream. Teamtailor is stranger: its board feed embeds a full schema.org `JobPosting`, which *has* an `employmentType` property, and the property is simply never populated. Measured across five live boards (67 postings) it was `null` every single time; re-checked today on `oatly.teamtailor.com`, still `null` on all 19 current postings.

A filter you cannot honour on these two platforms is worse than a missing field, because it looks like it worked. Setting an employment-type filter against a Greenhouse or Teamtailor board drops every posting on it and returns a clean, successful, empty run. Our Actor logs a warning naming the company when that combination is used, rather than letting a zero-row run read as "this company has no full-time openings."

## What each platform actually publishes

Measured live on 2026-10-10 across ~3,200 postings on 19 real boards; the values column is exactly what the sample contained, not a vendor-documented list.

| ATS | Shape | Values seen live | `"full-time"` matches? |
|---|---|---|---|
| Ashby | closed, camelCase | `FullTime`, `Contract`, `Intern`, `Temporary` | yes |
| SmartRecruiters | closed label | `Full-time`, `Part-time`, `Intern` | yes |
| Workable | closed label | `Full-time` | yes |
| Breezy | closed label | `Full-Time`, `Contract`, `Temporary`, `Other` | yes |
| Recruitee | code, tenure baked in | `fulltime_permanent`, `fulltime_fixed_term`, `parttime_fixed_term` | yes |
| Workday | closed, two values only | `Full time`, `Part time` — nothing else | yes |
| Lever | free text the employer types | 18 distinct values across 8 boards | usually |
| Personio | closed, lowercase snake_case | `permanent`, `intern`, `temporary`, `working_student` | **no** |
| Greenhouse | not published at all | always `null` | **no** |
| Teamtailor | schema.org property exists, never populated | always `null` | **no** |

## Personio: the vocabulary has no word for "full-time"

This is the one that cost us a wrong claim in our own documentation, so it is worth stating plainly. Personio's employment-type values are `permanent`, `intern`, `temporary` and `working_student`. A permanent, full-time role is just `permanent`. There is no `full`, no `time`, and no hyphen variant of either anywhere in the set.

So a substring filter for `"full-time"` returns **zero rows on every Personio board**, no matter how many full-time jobs are on it. Measured across five boards and 25 postings (`ottonova`, `clark`, `orderbird`, `exporto`, and Personio's own board), 20 of 25 were `permanent`. Re-checked today, `ottonova.jobs.personio.de/xml` returns 10 postings: 8 `permanent`, 2 `intern`.

The right filter on Personio is `"permanent"`. And `"contract"` matches nothing either — the closest Personio gets to contingent work is `temporary` or `working_student`.

For a while our own README claimed that `"full-time"` and `"part-time"` "work on every ATS that publishes the field." That was true of the first eight platforms and false the moment Personio landed. The field was there, the values were there, the filter ran without error, and the answer was silently empty. We found it by sampling the vocabulary rather than by testing the filter — which is the only way this class of bug surfaces.

## Separators are a solved problem; vocabulary isn't

There is a second, smaller trap underneath the vocabulary one, and it is worth separating because it has a real fix.

The same employment type is spelled with a different separator on nearly every platform: Ashby writes `FullTime` with none, Workable and Breezy use a hyphen, Workday uses a space, Recruitee uses an underscore and lowercases everything. A naive `value.toLowerCase().includes(query.toLowerCase())` bridges casing but not separators, so `"full-time"` — the most natural way for a human to type it — matched Workday's `Full time` and missed Ashby's `FullTime` entirely. On `ashby:ramp` that was a 0-row answer for a board that is overwhelmingly full-time: re-checked today, 167 postings, **159 of them `FullTime`**, plus 5 `Intern` and 3 `Temporary`.

We fixed that by stripping spaces, hyphens and underscores from *both* sides before matching, so `"full-time"`, `"full time"` and `"fulltime"` all match all five spellings. That is a fair thing to normalize away, because every one of those strings means the same thing.

Vocabulary is not, and we deliberately did not normalize it. Mapping Personio's `permanent` onto a synthetic `Full-time` would be inventing a fact: `permanent` is a statement about tenure, not about hours, and a permanent part-time role is a normal thing in the markets Personio serves. Recruitee makes the same point from the other direction — it fuses both dimensions into one code, so `fulltime_fixed_term` and `fulltime_permanent` are distinct values that a tenure-blind mapping would collapse. We pass the raw value through and tell you what each platform's set looks like.

## Workday publishes the field you want, just not per posting

Workday deserves its own note because the data you are probably after exists and is still unreachable per job.

The only employment type on a Workday job-detail payload is `timeType`, and it is a closed two-value field: `Full time` or `Part time`. We verified that against Workday's own `timeType` facet on three unrelated tenants — the facet counts partition the whole board into exactly those two buckets (443/81, 2674/2, 1521/14).

The classification most buyers actually want — `Regular`, `Temporary`, `Seasonal`, `Intern`, `Contractor`, `Fixed Term`, `Apprentice` — lives in a separate `workerSubType` facet. Workday exposes that one **only** at board level, as a facet with counts. It is absent from the listing rows and absent from the per-job detail payload, so there is no per-posting value for any scraper to return, ours included. If you need interns off a Workday board, filter on the job title.

## Practical rules

- **Sample the vocabulary before you filter on it.** One request per platform tells you the value set; a filter test only tells you that today's query returned nothing, which is the same thing you'd see if the jobs didn't exist.
- **Never let an unmatched filter read as an empty board.** Warn, name the company, and say which field could not be honoured.
- **Use titles as the fallback, not a guess.** On Greenhouse, Teamtailor and Workday, a title or description keyword (`"intern"`, `"contract"`) is the only honest way to split by employment type.
- **Normalize format, never meaning.** Separators and casing are noise. `permanent` vs `full-time` is not.

[ats-jobs-scraper](/go/ats-jobs-scraper) covers all ten platforms behind one schema and applies the separator-insensitive match described above, with a per-company warning whenever an employment-type filter hits a board that cannot answer it. Pay per job posting returned, no start fee, no browser needed for any of the ten.

## Related reading

- [Location is not one field either: normalizing ten ATS job-board APIs down to city/region/country](/blog/ats-location-field-is-not-one-shape)
- [Six ATS job-board JSON APIs, six different ideas of what a job posting is](/blog/ats-job-board-json-apis-six-shapes)
- [Teamtailor, Personio and Breezy — three more ATS job-board APIs, three more shapes](/blog/teamtailor-personio-breezy-job-board-apis)
- [Workday's public career-site API has no auth, a hard page-size cap, and no department field](/blog/workday-career-site-json-api)
- [Lever's job board API actually paginates — the one ATS that does](/blog/lever-job-board-json-api-pagination)

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every field name, value and count above comes from real requests to live job boards, and the Ashby, Teamtailor and Personio figures quoted as re-checked were fetched while writing this post.*
