# Remote Jobs Scraper – Remotive, Remote OK, Jobicy, Arbeitnow, Working Nomads & Himalayas in one de-duplicated feed

Six public remote-job boards, one normalized JSON schema, **de-duplicated across boards before you are charged**.

## What it does

Pulls live remote job postings from six documented, public, no-login job-board APIs and merges them:

| Source | What it covers | Salary data |
|---|---|---|
| [Remotive](https://remotive.com) | Remote tech, design, marketing, support roles, worldwide. Its public feed is small — **16 live postings total on 2026-09-28** (20 on 2026-09-21), and its API ignores every parameter it documents (`limit`, `search`, `category`, `company_name`), so you always get that whole feed | free-text range, parsed to numbers |
| [Remote OK](https://remoteok.com) | The ~100 most recent Remote OK postings | numeric USD range on many rows, rendered to text |
| [Jobicy](https://jobicy.com) | The 50 most recent Jobicy postings | numeric range + currency + period on many rows, rendered to text |
| [Arbeitnow](https://www.arbeitnow.com) | A general European board — **only** rows flagged remote are returned | none |
| [Working Nomads](https://www.workingnomads.com) | A general remote board with a `category` field on every row | none |
| [Himalayas](https://himalayas.app) | By far the largest board here — **~102,000 live postings** per its own API (measured 2026-09-23), cursor-paginated 20 at a time, so `maxPagesPerSource` caps how deep a run walks into it | numeric min/max/currency/period, rendered to text — **26 of 100 rows** carried one (measured 2026-09-29) |

Every row says which board it came from (`source`, `sourceSite`) and links to the original posting (`url`).

## Cross-board de-duplication (and what it actually measures)

When a job is syndicated to more than one of these boards, a naive aggregator returns it twice — and on a pay-per-result Actor you pay for both copies. This Actor folds copies into one row (matched on normalized company + title, newest kept) **before** the charge is made: the extra boards show up as `alsoOn: ["remoteok","jobicy"]` with their links in `duplicateUrls`, so you keep the information without paying for it twice. The company match strips common legal-entity suffixes (Inc, LLC, Ltd, Corp, GmbH, …) first, so "Acme Inc" on one board and "Acme" on another still fold into one row. Set `dedupe: false` to get one row per board copy.

**Measured honestly:** on a full five-board pull on 2026-09-23 (250 postings), **10 of 250** were duplicates (cross-board and same-board re-posts both folded) — these boards curate largely disjoint sets, so the overlap on any given day is usually small. Working Nomads syndicates some of the same postings Remotive carries, confirmed live this pull. **Himalayas is not part of that figure.** Its own inventory (~102k postings) dwarfs what any single run samples, so a capped `maxPagesPerSource` walk into it is not a "full pull" the way the other five boards' entire feeds are — a duplicate-rate measured against a partial Himalayas sample would not be comparable to the other five, so none is claimed here. Dedup against Himalayas still works exactly the same way per run — it just is not summarized as a fleet-wide overlap percentage. Treat de-duplication as a guarantee that you will never be billed twice for one posting, not as a claim that the boards overlap heavily.

## Use cases

- **Job boards and newsletters** — one merged, deduplicated feed to republish or email, with the source link each board's terms require.
- **Recruiters and sourcers** — watch which companies are hiring remotely for a given stack (`searchKeyword: "rust"`, `salaryOnly: true`).
- **Market/comp research** — collect salary ranges across boards over time; `salaryMin`/`salaryMax`/`salaryCurrency`/`salaryPeriod` are normalized where the board publishes them.
- **Job-seeker automations** — a daily run with `postedAfter` set to yesterday gives exactly the new postings, nothing else.
- **Job alerts on a schedule** — set `watchLabel` and run it hourly/daily; each run's dataset is only what's new since the last one (see "Watch mode" below), so you never pay to re-fetch roles you already have.

## Input

| Field | Type | Notes |
|---|---|---|
| `sources` | array | Any subset of `remotive`, `remoteok`, `jobicy`, `arbeitnow`, `workingnomads`, `himalayas`. Default: all six. An unknown name **fails the run** rather than being quietly dropped. |
| `searchKeyword` | string | Kept if the title, company, category or tags contain it (case-insensitive). Also passed to Jobicy's own `tag` search, which filters server-side (verified 2026-09-28: it matches company names and title phrases, not just tags). **Remotive's API ignores it** — see the note below — so Remotive rows are narrowed by this Actor alone. |
| `titleExcludeKeyword` | string | Drops postings whose title contains it, e.g. `Senior`. |
| `companyKeyword` | string | Substring match on company name. |
| `locationKeyword` | string | Substring match on the location/region field. |
| `postedAfter` / `postedBefore` | string | `YYYY-MM-DD`, UTC, **both bounds inclusive whole days**. A value that is not a real calendar date fails the run — see the FAQ. |
| `salaryOnly` | boolean | Keep only rows carrying a salary range or salary text. |
| `dedupe` | boolean | Default `true`. See above. |
| `includeDescription` | boolean | Adds `descriptionHtml`. Off by default — descriptions are large. |
| `maxPagesPerSource` | integer | Only affects the paginated sources — Arbeitnow (the board picks the page size, not you: 326 / 325 / 100 rows on pages 1–3 measured 2026-09-28, of which only ~20 / 12 / 1 are remote) and Himalayas (20/page, cursor-based). Default 2. |
| `maxResults` | integer | Stop after this many unique postings are pushed and charged. Default 100. |
| `watchLabel` | string | Optional. Turns on watch mode (see below) — only postings not delivered before under this label return. |
| `watchEvents` | array | Optional. Which watch-mode change(s) to report: `new`, `salaryAdded`, or both (default, empty = both). |
| `webhookUrl` | string | Optional. `http(s)` URL POSTed a small JSON completion summary. Best-effort; never affects the run or the bill. |

## Watch mode (only new postings since last run)
Set `watchLabel` to any name you like (`"backend-remote-eu"`) and the run stops returning the whole matching list every time and starts returning **only the postings that appeared since the previous run under that label**. This is the job-alert shape: schedule it hourly or daily and each run's dataset is your diff.

- **The first run for a label is a free baseline.** It records which postings are currently open (up to 5,000), returns **zero rows** and charges **nothing**. Run it again later to get what's new.
- **Already-delivered postings are dropped before any charge**, so a run with nothing new costs you nothing.
- **The baseline lives in your own Apify account** — a named key-value store `fetchsmith-remote-jobs-watch`, key `watch-<label>-<fingerprint>`. Nothing is kept on our side.
- **The fingerprint covers `sources`, every match filter** (`searchKeyword`, `titleExcludeKeyword`, `companyKeyword`, `locationKeyword`, `salaryOnly`, `postedAfter`, `postedBefore`) **and `maxPagesPerSource`.** Change any of them and you get a fresh baseline instead of a dump of postings the old settings had excluded. `maxPagesPerSource` is included because it changes how *deep* each board is crawled: a baseline seeded at depth 1 never recorded the postings sitting on pages 2+, so raising the depth on the same label would otherwise deliver — and charge for — a pile of *older* postings as if they were brand new. `maxResults` and `includeDescription` are *not* in the fingerprint: `maxResults` caps how many rows a run delivers, not how deep it looks, and a run that hits the cap defers the remaining new postings to your next run rather than losing them.
- **Identity is the same cross-board key used for de-duplication** (normalized company + title), so a job syndicated to two boards is ONE watched posting regardless of the `dedupe` input — you are never alerted twice for the same real-world opening.
- **`watchEvents` picks which kinds of change get delivered.** By default (empty) a watch reports both a brand-new posting and an already-delivered posting that gained a salary since you last saw it (`watchEvent: "new"`/`"salaryAdded"`, with `previousHasSalary` on the changed row). Remote OK, Jobicy and Himalayas commonly publish a posting without a salary and add one later under the same id; Arbeitnow and Working Nomads never carry a salary at all, so `salaryAdded` never fires for those. Pick just `["salaryAdded"]` to be alerted only on that and never pay for a brand-new posting. `salaryAdded` only starts firing on the run *after* a baseline recorded before this feature existed.
- **Baseline size cap:** the recorded baseline holds at most 20,000 posting ids per label; once a label crosses that, the oldest ids are dropped to make room and re-delivered (and re-charged) as "new" on a future run. A run that actually drops ids logs a warning and says so in its status message.

## Output

One object per unique posting:

```json
{
  "source": "remotive",
  "sourceSite": "https://remotive.com",
  "sourceJobId": "2091141",
  "title": "Frontend Web Application Developer",
  "company": "KoboToolbox",
  "companyLogo": "https://remotive.com/job/2091141/logo",
  "url": "https://remotive.com/remote-jobs/design/frontend-web-application-developer-2091141",
  "location": "USA, Canada, Argentina, Mexico, Peru",
  "remote": true,
  "jobType": "full_time",
  "category": "Design",
  "tags": ["api", "django", "docker", "frontend", "python", "react"],
  "salaryText": "$90k - $105k",
  "salaryMin": 90000,
  "salaryMax": 105000,
  "salaryCurrency": "USD",
  "salaryPeriod": null,
  "publishedAt": "2026-09-18T16:43:22.000Z",
  "alsoOn": [],
  "duplicateUrls": [],
  "scrapedAt": "2026-09-21T09:40:00.000Z"
}
```

### Location is a region, not a city

Remote boards publish the region a candidate must be in (`"Worldwide"`, `"USA, Canada"`, `"UK"`), not an office address, and some rows carry no location at all. `locationKeyword` therefore drops rows with an empty location — that is a filter on what the board actually published, not a geocoder.

### Job type is raw, not normalized

Unlike `salaryPeriod`, **`jobType` is passed through in each board's own words** — there is no shared vocabulary here. Measured live 2026-09-30: Remotive sends snake_case (`full_time`, `part_time`, `contract`, `freelance`), Jobicy sends Title-Case-with-hyphen (`Full-Time`, `Contract`), Himalayas sends Title Case with a space (`Full Time`, `Contractor`, `Temporary`), and Arbeitnow's `job_types` is a free-text tag array that often mixes seniority and language with the job type itself (`"Freelancer / independent contractor (freiberufler / selbstständiger)"`, `"Werkstudent"`) — joined into one comma-separated string, or empty when the posting has none. Remote OK and Working Nomads send no job-type field at all, so `jobType` is always `null` on those rows. If you need one consistent value (e.g. "is this full-time?"), match case-insensitively on a substring (`full`, `contract`, `freelance`, `part`) rather than an exact string, or filter to a single `source`.

### Salary

Every board publishes salary in exactly one shape and leaves the other empty: Remotive sends a free-text range only (`"$90k - $105k"`), Remote OK, Jobicy and Himalayas send numbers only, and Arbeitnow and Working Nomads publish none at all. **You get both columns filled from whichever one the board sent**, so you can sort and filter numerically across all sources and still show a human-readable range:

- Remotive's text is parsed into `salaryMin`/`salaryMax`/`salaryCurrency` (`"$31,2k- $52k"` → `31200`–`52000` USD; `k`/`K` suffixes, `$ € £ ₹ ¥`, spelled-out codes like `CAD`, thousands commas and European decimal commas all handled). `"up to $90k"` sets only `salaryMax`, `"from $60k"` only `salaryMin`.
- Remote OK's, Jobicy's and Himalayas' numbers are rendered into `salaryText` (`"$250,000 - $315,000 per year"`, `"Up to $127,000"`). The `per year` suffix appears only where the board stated the period — Jobicy and Himalayas send one, Remote OK does not. Jobicy and Himalayas also state a currency, Remote OK does not, so Remote OK rows read bare digits: `"250,000 - 315,000"`, no `$`.
- A value the board itself published is **never** overwritten — parsing only fills a field that was empty.

`salaryPeriod` is set **only when the posting states it** (`/hour`, `per year`, Jobicy's own field). We do not infer a period from the size of the number: `"$90k - $105k"` is almost certainly annual, but "almost certainly" is not something we will put in a data field, so it stays `null`. **Remote OK rows therefore carry `salaryPeriod: null`** — its API sends two bare numbers and no period field. Most are annual, but not all: a live posting paying 30–36 *per hour* sits in the same feed shape as one paying 250,000 *per year*, and until cycle 724 this Actor labelled both "per year". Use `salaryMin`/`salaryMax` and treat an unusually small Remote OK figure as an hourly rate. Text we cannot parse at all (`"Competitive"`) leaves the numeric fields `null` rather than guessing.

**`salaryPeriod` uses one vocabulary across all sources: `hourly`, `daily`, `weekly`, `monthly`, `yearly`, or `null`.** Boards that publish their own period field do not agree on the wording — Himalayas says `"annual"` where Jobicy and our Remotive text parser both say `"yearly"`, and it is the most common case on that board (19 of 26 salaried rows in a 100-row sample, measured 2026-09-29). Those are mapped onto the list above, so `salaryPeriod === "yearly"` catches every annual posting regardless of which board it came from, and `salaryText` reads `"$132,232 - $193,940 per year"` rather than `"... annual"`. A period word we do not recognise is passed through **unchanged** rather than guessed at or dropped — so an unexpected value means the board sent something genuinely new, not that we silently relabelled it.

Remote OK's zeros mean "not disclosed" and are normalized to `null`, not `0`. **No currency conversion is performed** — `salaryCurrency` tells you what the number is in when the board states it (a bare `$` in Remotive's text is read as USD). **Remote OK's API sends no currency field at all**, so `salaryCurrency` stays `null` on Remote OK rows rather than assuming USD — most are USD, but "most" is not a fact we will put in a data field. Use `salaryMin`/`salaryMax` at face value; if you need a guaranteed currency, filter to `source: "remotive"` or `"jobicy"`.

## Pricing

Pay per result: you are charged once per **unique** posting pushed to the dataset. No start fee, no per-run fee, nothing charged for duplicates, filtered-out rows or empty runs.

**Cheapest of the established multi-board aggregators (verified live 2026-10-01).** Of the eight multi-board remote-job aggregators on the Store with 50+ users, this one is the cheapest per job at every pricing tier. The category leader, `benthepythondev/remote-jobs-aggregator` (824 users, the same 6 boards we cover), charges $0.015/job on Free tapering to $0.0105/job on Diamond — roughly **10x our $0.0015→$0.001** — plus an Actor-start fee and a separate $0.01→$0.007 "salary-extracted" charge for parsed salary fields, which this Actor includes in the base per-job price at no extra cost. The rest, in user order: `sync-network/multi-site-remote-job-finder` (286 users) $0.003/job, `memo23/remote-jobs-aggregator` (271 users) a flat $0.00199/job plus additional-data and start fees, `hirebase/remote-jobs` (127 users) $0.003/job plus a $0.001 start fee, `flash_scraper/remote-job-aggregator` (80 users) $0.003→$0.0015/job, `hello.datawizards/RemoteJobs-Scraper` (51 users) $0.005/job plus a $0.005 start fee, and `get_anything/remote-jobs-aggregator` (50 users) $0.002→$0.0016/job.

**What we do not claim (verified live 2026-10-01).** We are **not** the cheapest listing in this niche outright — an earlier version of this section claimed that and it was wrong. Two genuine full-coverage rivals undercut us, both with small adoption: `nivlekk/remote-jobs-aggregator` (26 users) covers seven boards — our six plus We Work Remotely — at $0.0005/job plus a $0.001 start fee, and `hyperbach/remote-jobs-feed` (17 users) covers seven boards and ATSs at a flat $0.001/job with no start fee. If per-row price is your only criterion, those are cheaper. Two input filters several rivals ship are also genuinely missing here: a **numeric minimum-salary** filter (we only have the boolean `salaryOnly`; `nivlekk`, `hyperbach` and `flash_scraper` all take a number) and **job-type / seniority** filters (`benthepythondev`, `flash_scraper`). What this Actor gives you that none of the above do: a **two-sided date window** (`postedAfter` *and* `postedBefore`, both inclusive, and a malformed date fails the run instead of silently billing you for every posting on six boards — every rival offers only an open-ended "posted within N days"), a watch mode that fires on **`salaryAdded`** and not just "only new", salary parsing in the base price with a normalized `salaryPeriod` vocabulary, **no start fee of any kind**, and measured per-board limits documented in the FAQ above rather than left for you to discover on a billed run.

## FAQ

**What happens if I typo a date?** The run fails immediately with an error naming the field and the bad value. It is deliberate: if a bad `postedAfter` were ignored, the run would return (and bill for) every posting on all six boards instead of your window, and a warning line in a successful run is not something anyone reads. `2026-6-5`, `06/15/2026` and `2026-02-30` are all rejected — the last one because it is not a real date, even though JavaScript would silently roll it over to March 1.

**Are both date bounds inclusive?** Yes. `postedAfter` starts at 00:00:00.000Z of that day and `postedBefore` ends at 23:59:59.999Z, so a job posted at 14:00Z on your end date is included.

**How are duplicates detected?** Normalized company name + normalized job title (lowercased, punctuation collapsed), no source check — so it also catches a board re-listing its own posting under a new URL, not just cross-board syndication. It will not merge two genuinely different openings that share a title at the same company — those stay separate rows. Both halves are measured, not assumed: a live 356-row pull found 4 same-board reposts correctly folded (one company, Peroptyx, had 4 URLs behind one title on Working Nomads alone) and 0 of 14 same-company near-title-overlap pairs (e.g. Lemon.io's simultaneous "Senior AI/QA/DevOps/Solutions Engineer" openings) were true duplicates — confirming that loosening the match to fuzzy titles would silently merge real distinct roles far more often than it would catch missed duplicates. See [Remote job boards duplicate their own listings — and fuzzy title matching would make that worse, not better](https://fetchsmith.com/blog/remote-job-boards-duplicate-themselves-and-fuzzy-titles-lie).

**I set a small `maxResults` and got rows from only one board — is that a bug?** No. The merge is global newest-first across all six boards, so a small cap samples *recency*, not *boards*: whichever board happened to publish the freshest postings that minute fills the cap. Ask for at least 50 results to see all six represented, or run once per board with `sources` set to a single board if you need a guaranteed per-board slice.

**What if one board is down?** The run continues with the others and logs a warning naming the failed board. You are only charged for rows you actually receive.

**What if the run approaches the platform run timeout?** It stops itself short of the hard kill and pushes whatever unique postings it already collected, rather than losing the whole run to a mid-collection kill (this Actor collects and de-duplicates all six boards before pushing any row, so an unguarded timeout previously meant zero rows delivered). The closing log line gets a `(incomplete: time-budget)` suffix, and a `Board(s) not reached: ...` warning names any board the clock didn't leave time to start at all — a source missing from your results because of this is different from a source that's genuinely empty for your filters. There is no `RUN_SUMMARY` key-value record for this Actor; the log is the source of truth. If you see this, narrow the date window, lower `maxPagesPerSource`, or drop a slow `source` from the list.

**Does this need a login, API key or proxy?** No. All six endpoints are public and documented, and the Actor is HTTP-only — no headless browser.

**Why are Arbeitnow rows mostly German?** Arbeitnow is a European (largely German) board; only its postings flagged remote are returned here. Drop `arbeitnow` from `sources` if you want US-centric boards only.

**Why does Himalayas only return a handful of rows even with a high `maxResults`?** Its own feed caps page size at 20 regardless of what you request, so `maxPagesPerSource` (default 2 → 40 Himalayas rows per run) governs how deep a run walks into its ~102k-posting inventory. Raise `maxPagesPerSource` (max 20 → 400 rows) if you need more from this one board specifically.

## Sources and attribution

All six APIs are public and ask for credit in return. This Actor puts the source board and the original posting URL on every row so you can honour that downstream: **if you republish these postings, link back to [Remotive](https://remotive.com), [Remote OK](https://remoteok.com), [Jobicy](https://jobicy.com), [Arbeitnow](https://www.arbeitnow.com), [Working Nomads](https://www.workingnomads.com) and [Himalayas](https://himalayas.app), and point application buttons at the original job URL in the `url` field.** Remote OK's API terms require a followed link back; Jobicy's asks that apply buttons resolve to the original posting.

## Notes

- Public data only: no login, no personal data beyond what the boards publish publicly about a job.
- Feeds are snapshots of what each board serves at run time; Remote OK and Jobicy expose only their most recent postings, so historical `postedBefore` windows will thin out on those two.
- **Flaky-feed handling (2026-09-21).** Remote OK's edge intermittently kills the HTTP/2 stream or answers a fresh connection with a non-HTTP preamble — measured at roughly 1 fresh request in 4, and Remotive does it too. Each source is fetched once per run, so one blip used to drop that whole board from your dataset with only a warning in the log. Every transport-level failure is now retried up to 3 times, falling back to HTTP/1.1 after the first attempt. A measured back-to-back pair of runs over all four boards (pre-Working-Nomads): **83 rows before the fix, 182 after** (two blips in the same run, both recovered). A feed that answers 404 or 5xx now fails its source loudly instead of reporting zero jobs, which used to look identical to "nothing posted today".
- **Working Nomads added (cycle 699).** Closes a feature gap against the category leader (`benthepythondev/remote-jobs-aggregator`, 805 Store users), which covers 6 boards including Working Nomads and Himalayas; we now cover 5. No stable job ID in its feed — the job's own permalink URL doubles as `sourceJobId`. No salary or company-logo fields published, same shape as Arbeitnow.
- **Himalayas added (cycle 701).** Closes the last feature gap against the category leader — we now match its 6-board coverage. Public endpoint is `https://himalayas.app/jobs/api` (the documented-looking `/api/jobs` and `/api/v1/jobs` paths both 404 or return the HTML app shell; the real one was found by reading the response's own `comments` field, which documents the cursor-pagination contract). Fixed page size of 20 regardless of any `limit` query param (verified live at limit=50/100/200, all still returned 20) — depth is governed entirely by `maxPagesPerSource`, same lever as Arbeitnow. No stable numeric id; `guid` (the job's own permalink) doubles as `sourceJobId`, same gap-filling as Working Nomads.

## Related guides

- [Six public remote-job APIs with no key — and how small each feed really is](https://fetchsmith.com/blog/remote-job-board-json-apis-four-feeds) — measured feed sizes, Remotive's decorative `limit`, Remote OK's legal-notice row, Working Nomads' id-less 58-posting array, Himalayas' ~102k-posting scale and undocumented endpoint, and which boards actually syndicate
- [Remote job boards duplicate their own listings — and fuzzy title matching would make that worse, not better](https://fetchsmith.com/blog/remote-job-boards-duplicate-themselves-and-fuzzy-titles-lie) — a live 356-row pull found the same board re-listing one job under a new URL (correctly folded), and confirmed that fuzzy title matching would have wrongly merged 14 genuinely distinct roles at companies that batch-post similar titles
- [Incremental API watch mode: eight traps](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how `watchLabel` is built across the fleet, including this Actor's cross-board posting identity and its salary-disclosure change signal
- [FetchSmith blog](https://fetchsmith.com/blog) — data-source guides and API notes
- [All FetchSmith Actors](https://fetchsmith.com/tools)
