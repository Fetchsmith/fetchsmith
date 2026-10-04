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
- **Job-seeker automations** — a daily run with `postedAfter` set to yesterday gives exactly the new postings, nothing else; add `minSalaryAnnual: 100000` to skip roles below your floor (USD-stated rows only — see "Salary" below).
- **Job alerts on a schedule** — set `watchLabel` and run it hourly/daily; each run's dataset is only what's new since the last one (see "Watch mode" below), so you never pay to re-fetch roles you already have.

## Input

| Field | Type | Notes |
|---|---|---|
| `sources` | array | Any subset of `remotive`, `remoteok`, `jobicy`, `arbeitnow`, `workingnomads`, `himalayas`. Default: all six. An unknown name **fails the run** rather than being quietly dropped. |
| `searchKeyword` | string | Kept if the title, company, category or tags contain it (case-insensitive). Also passed to Jobicy's own `tag` search, which filters server-side (verified 2026-09-28: it matches company names and title phrases, not just tags). **Remotive's API ignores it** — see the note below — so Remotive rows are narrowed by this Actor alone. |
| `titleExcludeKeyword` | string | Drops postings whose title contains it, e.g. `Senior`. |
| `companyKeyword` | string | Substring match on company name. |
| `locationKeyword` | string | Substring match on the location/region field. |
| `jobTypeKeyword` | string | Substring match on the job-type field (e.g. `full`, `contract`, `part`), case-insensitive. Published by Remotive, Jobicy, Arbeitnow and Himalayas; Remote OK and Working Nomads carry no job-type field in their API at all, so their rows never match a non-empty filter here — dropped, not guessed at. Added 2026-10-02. |
| `seniorityKeyword` | string | Substring match on the seniority-level field (e.g. `senior`, `entry`, `director`), case-insensitive. Only Jobicy publishes a clean seniority field distinct from job type; the other five boards carry none, so their rows never match a non-empty filter here — dropped, not guessed at from the job title. Added 2026-10-02. |
| `postedAfter` / `postedBefore` | string | `YYYY-MM-DD`, UTC, **both bounds inclusive whole days**. A value that is not a real calendar date fails the run — see the FAQ. |
| `salaryOnly` | boolean | Keep only rows carrying a salary range or salary text. |
| `minSalaryAnnual` | integer | Keep only rows whose stated salary floor (`salaryMin`), annualized, is at least this many USD/year. Annualizes hourly x2080, daily x260, weekly x52, monthly x12 — stated assumptions, not facts. Drops (never assumes a pass) rows with no stated period, rows with only a ceiling and no floor (`"Up to $90k"`), and rows not explicitly in USD — see "Salary fields" below. |
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
- **The fingerprint covers `sources`, every match filter** (`searchKeyword`, `titleExcludeKeyword`, `companyKeyword`, `locationKeyword`, `jobTypeKeyword`, `seniorityKeyword`, `salaryOnly`, `minSalaryAnnual`, `postedAfter`, `postedBefore`) **and `maxPagesPerSource`.** Change any of them and you get a fresh baseline instead of a dump of postings the old settings had excluded. `maxPagesPerSource` is included because it changes how *deep* each board is crawled: a baseline seeded at depth 1 never recorded the postings sitting on pages 2+, so raising the depth on the same label would otherwise deliver — and charge for — a pile of *older* postings as if they were brand new. `maxResults` and `includeDescription` are *not* in the fingerprint: `maxResults` caps how many rows a run delivers, not how deep it looks, and a run that hits the cap defers the remaining new postings to your next run rather than losing them.
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
  "seniorityLevel": null,
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

### Seniority is one board only, not inferred

`seniorityLevel` is populated **only from Jobicy's `jobLevel` field** (`Any`, `Entry-Level, Junior`, `Senior`, `Director`, verified live 2026-10-02) and is `null` on every other source. No other board publishes a seniority field distinct from a job title or job type — Himalayas' `categories` sometimes embed a seniority word inside a role-title slug (`Senior-Valuation-Analyst`), but there is no separate field to read a clean value from, so it is left `null` rather than parsed out of a title with a regex that would eventually misfire on a title like `"Senior Living Coordinator"` (seniority of the job title, not the role). `seniorityKeyword` matches on this field, so it only ever narrows Jobicy rows; use `searchKeyword` against the title if you want a best-effort seniority word match across every board.

### Salary

Every board publishes salary in exactly one shape and leaves the other empty: Remotive sends a free-text range only (`"$90k - $105k"`), Remote OK, Jobicy and Himalayas send numbers only, and Arbeitnow and Working Nomads publish none at all. **You get both columns filled from whichever one the board sent**, so you can sort and filter numerically across all sources and still show a human-readable range:

- Remotive's text is parsed into `salaryMin`/`salaryMax`/`salaryCurrency` (`"$31,2k- $52k"` → `31200`–`52000` USD; `k`/`K` suffixes, `$ € £ ₹ ¥`, spelled-out codes like `CAD`, thousands commas and European decimal commas all handled). `"up to $90k"` sets only `salaryMax`, `"from $60k"` only `salaryMin`.
- Remote OK's, Jobicy's and Himalayas' numbers are rendered into `salaryText` (`"$250,000 - $315,000 per year"`, `"Up to $127,000"`). The `per year` suffix appears only where the board stated the period — Jobicy and Himalayas send one, Remote OK does not. Jobicy and Himalayas also state a currency, Remote OK does not, so Remote OK rows read bare digits: `"250,000 - 315,000"`, no `$`.
- A value the board itself published is **never** overwritten — parsing only fills a field that was empty.

`salaryPeriod` is set **only when the posting states it** (`/hour`, `per year`, Jobicy's own field). We do not infer a period from the size of the number: `"$90k - $105k"` is almost certainly annual, but "almost certainly" is not something we will put in a data field, so it stays `null`. **Remote OK rows therefore carry `salaryPeriod: null`** — its API sends two bare numbers and no period field. Most are annual, but not all: a live posting paying 30–36 *per hour* sits in the same feed shape as one paying 250,000 *per year*, and until cycle 724 this Actor labelled both "per year". Use `salaryMin`/`salaryMax` and treat an unusually small Remote OK figure as an hourly rate. Text we cannot parse at all (`"Competitive"`) leaves the numeric fields `null` rather than guessing.

**`salaryPeriod` uses one vocabulary across all sources: `hourly`, `daily`, `weekly`, `monthly`, `yearly`, or `null`.** Boards that publish their own period field do not agree on the wording — Himalayas says `"annual"` where Jobicy and our Remotive text parser both say `"yearly"`, and it is the most common case on that board (19 of 26 salaried rows in a 100-row sample, measured 2026-09-29). Those are mapped onto the list above, so `salaryPeriod === "yearly"` catches every annual posting regardless of which board it came from, and `salaryText` reads `"$132,232 - $193,940 per year"` rather than `"... annual"`. A period word we do not recognise is passed through **unchanged** rather than guessed at or dropped — so an unexpected value means the board sent something genuinely new, not that we silently relabelled it.

Remote OK's zeros mean "not disclosed" and are normalized to `null`, not `0`. **No currency conversion is performed** — `salaryCurrency` tells you what the number is in when the board states it (a bare `$` in Remotive's text is read as USD). **Remote OK's API sends no currency field at all**, so `salaryCurrency` stays `null` on Remote OK rows rather than assuming USD — most are USD, but "most" is not a fact we will put in a data field. Use `salaryMin`/`salaryMax` at face value; if you need a guaranteed currency, filter to `source: "remotive"` or `"jobicy"`.

**`minSalaryAnnual`** applies this same no-inference rule to a numeric floor. Because there is no currency conversion, a floor can only be honestly compared against a row explicitly stated in USD — rows with `salaryCurrency: null` (most Remote OK rows) or a non-USD currency are dropped when the floor is set, not assumed to pass or fail. Because a period is required to annualize (`"$85/hour"` is not below a $100k floor; `null`-period Remote OK rows cannot be annualized at all, so they are dropped too when the floor is set), and because the floor compares against `salaryMin` specifically — a ceiling-only row (`"Up to $90k"`, `salaryMin: null`) has no known floor, so it is also dropped rather than assumed to clear the bar.

## Pricing

Pay per result: you are charged once per **unique** posting pushed to the dataset. No start fee, no per-run fee, nothing charged for duplicates, filtered-out rows or empty runs.

**Cheapest of the established *remote-specific* multi-board aggregators (verified live 2026-10-03).** Of the seven other multi-board remote-job aggregators on the Store with 50+ users, this one is the cheapest per job at every pricing tier. The category leader, `benthepythondev/remote-jobs-aggregator` (831 users, the same 6 boards we cover), charges $0.015/job on Free tapering to $0.0105/job on Diamond — roughly **10x our $0.0015→$0.001** — plus an Actor-start fee and a separate $0.01→$0.007 "salary-extracted" charge for parsed salary fields, which this Actor includes in the base per-job price at no extra cost. The rest, in user order: `sync-network/multi-site-remote-job-finder` (286 users) $0.003/job plus a $0.00005 start fee, `memo23/remote-jobs-aggregator` (300 users) a flat $0.00199/job plus additional-data and start fees, `hirebase/remote-jobs` (142 users) $0.003/job plus a $0.001 start fee, `flash_scraper/remote-job-aggregator` (85 users) $0.003→$0.0015/job, `hello.datawizards/RemoteJobs-Scraper` (51 users) $0.005/job plus a $0.005 start fee, and `get_anything/remote-jobs-aggregator` (52 users) $0.002→$0.0016/job. **Note for `flash_scraper`: a pricing change already filed on the platform takes effect 2026-10-14** — its ladder plateaus at $0.0021/job from Gold up instead of falling to $0.0015 on Diamond, and a $0.00005 start fee is added, so it gets dearer, not cheaper, from that date (its own change note says "per-job prices unchanged", which the live ladder contradicts).

**Read the scope word in that claim.** It says *remote-specific*, and that qualifier is doing real work: **a broader-scope job-board aggregator undercuts us at every tier.** `code-node-tools/job-listings-scraper` (54 users, 28 of them new in the last 30 days — the fastest-growing listing anywhere in this comparison) reads 180+ job boards and ATS platforms (Greenhouse, Lever, Workday, SmartRecruiters, Ashby, RemoteOK, hh.ru …) for $0.001/result on Free tapering to $0.0007 from Gold up, plus a $0.00005 start fee. That is below our price on **every** tier, and one of its 180+ sources is Remote OK, one of our six. It is not a remote-jobs product — there is no remote filter across those boards, no cross-board de-duplication of the same posting, and no normalized salary scale — but if your buying question is "cheapest per row", it wins, and we are not going to bury that behind an adjective. A third broader-scope aggregator, `doggo/uk-jobs-board-scraper` (407 users, 40 new in the last 30 days, verified live 2026-10-04), reads Indeed, Reed, Totaljobs, CV-Library and Adzuna plus two of our six boards, Remote OK and Arbeitnow, at $0.005/result on Free tapering to $0.004 from Gold up, **plus a flat $0.10 Actor-start fee charged on every run regardless of tier** — 4-5x our per-job rate before that start fee is even counted, so unlike `code-node-tools` it is dearer than us, not cheaper; it is named here only because it is large and growing, and because two of its sources overlap ours. Separately, `lenient_grove/Daily-Job-Pulse-Multi-Source-Job-Opportunity-Aggregator` (618 users — the fourth-biggest listing in the whole niche sweep) aggregates 25+ general platforms (LinkedIn, Naukri, Indeed, Glassdoor, RemoteOK) with a dashboard, at $0.08/result on Free tapering to $0.05 from Gold up: **33–53x our rate**, the dearest listing found in this niche.

**What we do not claim (verified live 2026-10-03).** We are **not** the cheapest listing in this niche outright — an earlier version of this section claimed that and it was wrong. A 15-term Store sweep run on 2026-10-03 saw 658 distinct listings, 393 of which mention remote work or one of the six boards by name, and **six of them undercut us** (up from the two this paragraph listed before cycle 1156 — the other four were simply never found, not disclosed and then hidden). Cheaper than us at every tier: `nivlekk/remote-jobs-aggregator` (26 users) covers seven boards — our six plus We Work Remotely — at $0.0005/job plus a $0.001 start fee; `code-node-tools/job-listings-scraper` (54 users) at $0.001→$0.0007 across 180+ boards, described above. Cheaper on our Free/Bronze/Silver tiers and roughly tied from Gold up: `hyperbach/remote-jobs-feed` (17 users) covers seven boards and ATSs at a flat $0.001/job with no start fee; `delightful_unicorn/remote-jobs-aggregator` (17 users) merges Remote OK, We Work Remotely and Working Nomads at a flat $0.001/job plus a $0.00001 start fee; `feedforge/remote-jobs-scraper` (7 users) reads four boards at a flat $0.001/job plus a $0.00005 start fee; and `newbs/RemoteOk-Premium-Job-Scraper` (102 users, but 0 new in the last 30 days) does Remote OK alone at a flat $0.001/job with no start fee. If per-row price is your only criterion, those are cheaper. One more worth knowing about: `scrapesage/remote-jobs-scraper` (9 users, 7 boards) starts far above us at $0.004/job but steepens to $0.001 on Diamond, where it ties us exactly. We closed half of a disclosed input gap at cycle 1131: `jobTypeKeyword` now filters on job type (`benthepythondev` and `flash_scraper` both ship this), matching Remotive, Jobicy, Arbeitnow and Himalayas rows — Remote OK and Working Nomads publish no job-type field at all, so their rows cannot be filtered on it, by us or by anyone reading the same public APIs. Cycle 1135 closes the other half, with a correction: this README previously said no board exposes a seniority field distinct from job type — that was wrong. **Jobicy's `jobLevel` is a real, clean seniority enum** (`Any`, `Entry-Level, Junior`, `Senior`, `Director`, verified live 2026-10-02), now its own `seniorityLevel` output field and `seniorityKeyword` input filter rather than being buried inside `tags`. Himalayas' `categories` (the other field this README used to point to) are role-title slugs like `Senior-Valuation-Analyst`, not a structured seniority field — a seniority word sometimes rides along inside the slug, but there is nothing to filter on cleanly, so Himalayas rows (and every other board's) carry `seniorityLevel: null` and never match a non-empty `seniorityKeyword`. Coverage is 1 of 6 boards, honestly partial — same shape as `jobTypeKeyword`'s partial coverage above.

Outside the multi-board comparison above (verified live 2026-10-03), the niche's two *biggest* listings by users are actually single-board specialists: `inlifeprojects/himalayas-jobs-scraper` (794 users) and `inlifeprojects/remoteok-jobs-scraper` (681 users), each scraping exactly one of our six boards at a flat $0.001/job plus a $0.00005 start fee. Neither merges or de-duplicates anything — if you want more than one board, you still need an aggregator — but if you only ever want Himalayas or only Remote OK, they roughly tie our GOLD+ rate once the start fee is counted and undercut our FREE/BRONZE/SILVER tiers. Two more large specialists, both named here for the first time at cycle 1156: `logiover/himalayas-remote-jobs-scraper` (316 users) is a second Himalayas-only reader at $0.003→$0.0021/job plus a $0.00005 start fee, 2–3x our rate; and `parsebird/wwr-jobs-scraper` (302 users) covers We Work Remotely — a seventh board we do **not** read — at $0.004 per listing plus $0.035 per full job detail. `orgupdate/remote-co-jobs-scraper` (112 users) covers Remote.co, another board nothing here touches, at $0.012 per record plus a $0.02 start fee: 8–12x our per-row rate, and roughly 20x on a single-row run. **Correction (cycle 1156): this paragraph previously priced `orgupdate` at "$0.14–$0.2 per record … 100x+ pricier", which is about ten times its live price.** It is still the dearest single-board reader on this page, but not by the margin we published, and overstating a rival's price flatters our own comparison, so the real number is above.

**Also checked live on 2026-10-03 and dearer than us at every tier, so not individually argued above:** `scrapemint/remote-jobs-scraper` (45 users, 4 boards, flat $0.003/job), `nomad-agent/remote-boards-scraper` (16 users, $0.002→$0.0016 plus a $0.005 start fee that is **not** flagged one-time, so it bills per GB of memory), `nexgendata/job-market-mcp-server` (13 users, $0.05 per tool call — an MCP server, not a dataset product), `nomad-agent/ml-ai-dev-bundle` (10 users), `cancap/remote-jobs-actor` (8 users, 7 boards, $0.003/job), `charliemorrisondev/remote-jobs-aggregator` (8 users, 8 boards, $0.002/job), `actorworks/remote-jobs-aggregator` (6 users, 8 boards, $0.002→$0.0015 plus a start fee), `straightforward_hydra/remote-jobs-aggregator-9-in-one` (5 users, $0.002/job plus a $0.006 digest event), and `techforce.global/all-jobs-scraper` (4 users, 26 boards, $0.0045→$0.0031).
What this Actor gives you that none of the above do: a **two-sided date window** (`postedAfter` *and* `postedBefore`, both inclusive, and a malformed date fails the run instead of silently billing you for every posting on six boards — every rival offers only an open-ended "posted within N days"), a `minSalaryAnnual` floor that annualizes hourly/daily/weekly/monthly figures onto one scale instead of comparing raw numbers across different pay periods, a watch mode that fires on **`salaryAdded`** and not just "only new", salary parsing in the base price with a normalized `salaryPeriod` vocabulary, **no start fee of any kind**, and measured per-board limits documented in the FAQ above rather than left for you to discover on a billed run.

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
- **`seniorityLevel` / `seniorityKeyword` added (cycle 1135), correcting a false claim.** This README used to say no board exposes a seniority field distinct from job type. Verified live 2026-10-02: Jobicy's `jobLevel` is a real, clean enum (`Any`, `Entry-Level, Junior`, `Senior`, `Director`) that was being read into the `tags` output field as a placeholder (Jobicy's API has no actual tags field). It now has its own `seniorityLevel` field and `seniorityKeyword` filter; every other board stays `null` — Himalayas' `categories` looked like a second candidate but turned out to be role-title slugs (`Senior-Valuation-Analyst`), not a structured seniority value, so it was not used.

## Related guides

- [Six public remote-job APIs with no key — and how small each feed really is](https://fetchsmith.com/blog/remote-job-board-json-apis-four-feeds) — measured feed sizes, Remotive's decorative `limit`, Remote OK's legal-notice row, Working Nomads' id-less 58-posting array, Himalayas' ~102k-posting scale and undocumented endpoint, and which boards actually syndicate
- [Remote job boards duplicate their own listings — and fuzzy title matching would make that worse, not better](https://fetchsmith.com/blog/remote-job-boards-duplicate-themselves-and-fuzzy-titles-lie) — a live 356-row pull found the same board re-listing one job under a new URL (correctly folded), and confirmed that fuzzy title matching would have wrongly merged 14 genuinely distinct roles at companies that batch-post similar titles
- [Incremental API watch mode: eight traps](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how `watchLabel` is built across the fleet, including this Actor's cross-board posting identity and its salary-disclosure change signal
- [FetchSmith blog](https://fetchsmith.com/blog) — data-source guides and API notes
- [All FetchSmith Actors](https://fetchsmith.com/tools)
