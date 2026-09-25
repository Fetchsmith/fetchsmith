# ATS Jobs Scraper – Greenhouse, Ashby, Lever, Recruitee, Workable, SmartRecruiters & Workday

Live job postings straight from any company's own career board on **Greenhouse, Ashby, Lever, Recruitee, Workable, SmartRecruiters or Workday**, normalized into one schema — no matter which ATS the company uses.

## What it does
- Fetches each company's public job-board API directly (no browser, no login) for **Greenhouse**, **Ashby**, **Lever**, **Recruitee**, **Workable**, **SmartRecruiters** and **Workday** — the ATS behind 10,000+ career sites, including many large employers no other field in this list reaches.
- **Don't know which ATS a company uses?** Leave `ats` off (or set it to `"auto"`) and give just the slug — the Actor checks all 6 non-Workday platforms for you and uses whichever one is real. See [Don't know which ATS a company uses?](#dont-know-which-ats-a-company-uses-use-ats-auto).
- Normalizes every posting into one shared schema (title, department, team, employment type, workplace type, remote flag, location, salary where the ATS exposes it, timestamps, apply URL, description).
- Client-side filters (title keyword + exclude, location keyword + exclude, remote-only, has-salary, posted-after date) are applied **before** charging, so you only pay for postings you actually want.
- Companies that have migrated off an ATS (very common for Lever) are skipped with a warning, not a failed run.
- Pay per result: you are charged only for job postings actually returned. **No start fee.**

## Use cases
- **Job-board aggregation** — pull live openings from every company you track across 7 different ATSes into one feed, instead of maintaining 7 separate scrapers.
- **Recruiting/sourcing intelligence** — spot when a target company opens a new role in a specific team or location, with `department`/`team`/`location` already normalized so you can filter without per-ATS cleanup.
- **Salary benchmarking** — `salaryMin`/`salaryMax`/`salaryCurrency`/`salaryInterval` give a normalized comparable across Ashby, Lever, Recruitee and Greenhouse postings that publish pay ranges.
- **Remote-work tracking** — `remoteOnly` plus the normalized `workplaceType`/`isRemote` fields build a remote-jobs feed across every ATS at once, not just the ones with a "remote" search filter.
- **Skill/tech-stack sourcing** — `descriptionKeyword` searches the full posting body, so you can pull every role at 50 companies that mentions `Kubernetes`, `Rust` or `visa sponsorship` — requirements that almost never appear in the job title.
- **Hiring-trend research** — `postedAfter`/`postedBefore` plus `publishedAt` let you track how fast a company (or a whole market segment) is opening new roles over time.
- **Job alerts / new-posting watch** — set `watchLabel` and a scheduled run returns *only* the roles that opened since the last run, not the same open-roles list every time. You are charged for new postings only (see [Watch mode](#watch-mode-only-new-postings-since-last-run)).

## Input
| Field | Type | Description |
|---|---|---|
| `companies` | array | `[{"ats": "auto\|greenhouse\|ashby\|lever\|recruitee\|workable\|smartrecruiters\|workday", "slug": "<company-slug>"}]`. The slug is the company identifier in their career-board URL, e.g. `jobs.ashbyhq.com/ramp` → `{"ats":"ashby","slug":"ramp"}`. **Omit `ats` or set it to `"auto"` to skip knowing which platform a company uses** — the Actor tries all 6 non-Workday platforms for that slug and keeps whichever one actually has a board. **Workday's slug is `"<host>/<site>"`** (see below) since a Workday board has no single short identifier, and it always needs an explicit `"ats":"workday"` — it cannot be auto-detected. |
| `titleKeyword` | string | Only keep postings whose title contains this text. |
| `titleExcludeKeyword` | string | Drop postings whose title contains this text, e.g. `"Senior"` to filter out senior roles. |
| `locationKeyword` | string | Only keep postings whose location/city/region/country contains this text. |
| `locationExcludeKeyword` | string | Drop postings whose location/city/region/country contains this text, e.g. a country you don't hire in. |
| `employmentTypeKeyword` | string | Only keep postings whose normalized `employmentType` contains this text, e.g. `"full"` or `"contract"`. Postings where the ATS never exposes this field are dropped when set — **on Greenhouse boards that is every posting** (see Employment type below). |
| `departmentKeyword` | string | Only keep postings whose `department`, `team` or `departmentPath` contains this text, e.g. `"Engineering"`. Postings where the ATS never exposes a department are dropped when set. |
| `descriptionKeyword` | string | Only keep postings whose **description text** contains this text, e.g. `"Kubernetes"` or `"visa sponsorship"` — the requirements a job title never mentions. Matched against the plain text, not the HTML. |
| `descriptionExcludeKeyword` | string | Drop postings whose description text contains this text, e.g. `"security clearance"`. |
| `hasSalary` | boolean | Only keep postings that come back with a salary — an ATS compensation field (Ashby, Lever, Recruitee) or a pay-transparency range printed in the posting body (Greenhouse). Default `false`. |
| `minSalary` / `maxSalary` | integer | Only keep postings whose salary range overlaps this floor/ceiling, e.g. `minSalary:150000`. Compared against the number as posted — no currency conversion, no pay-interval normalization (check `salaryCurrency`/`salaryInterval` on the row, since ranges mix year/month/week/day/hour). Postings with no salary never match either. |
| `remoteOnly` | boolean | Only keep postings the ATS marks as remote. Default `false`. |
| `postedAfter` | string | `YYYY-MM-DD` (or full ISO datetime); only keep postings published on/after it. The named day is included. An unparseable date stops the run — see "Date bounds" below. |
| `postedBefore` | string | `YYYY-MM-DD` (or full ISO datetime); only keep postings published on/before it — the named day is included in full. Pair with `postedAfter` for a date window (e.g. everything a company opened in one quarter). |
| `includeDescriptions` | boolean | Include full HTML + plain-text description. Default `true`. The description filters still work with this off — the text is fetched, matched, then dropped from the rows. |
| `maxJobsPerCompany` | integer | Cap on how many postings that pass your filters are kept per company — filters are applied first, then this cap. Default `50` — kept low so a run with no input at all (e.g. an API caller omitting the field) stays fast and cheap; pass a higher value explicitly for bulk pulls (up to `5000`). |
| `maxResults` | integer | Cap total postings returned across all companies. Default `300` — same reasoning as above; pass a higher value explicitly for bulk pulls (up to `100000`). |
| `watchLabel` | string | Optional. Name a saved job alert and return only postings not delivered under that label + filter set before. First run per label is a free baseline. See [Watch mode](#watch-mode-only-new-postings-since-last-run). |
| `webhookUrl` | string | Optional. POST a small JSON completion summary (postings pushed, companies scanned/errored, dataset ID, watch new/skipped counts) here when the run finishes — see FAQ. |
| `proxyConfiguration` | object | Apify Proxy config. Default: Apify Proxy on. |

### Don't know which ATS a company uses? Use `"ats": "auto"`
If you only have a guess at the slug (e.g. the company's own name, lowercased) and not the platform, pass `{"slug": "<slug>"}` with no `ats`, or `{"ats": "auto", "slug": "<slug>"}`. The Actor tries Greenhouse, Ashby, Lever, Recruitee, Workable and SmartRecruiters for that exact slug in parallel and keeps whichever platform actually has a board there — `atsSource` on the returned rows shows what it found. If the same slug happens to be a real, populated board on more than one platform (rare, but generic slugs like `demo` can collide), it keeps the one with postings; if more than one has postings, it logs the ambiguity and picks by a fixed priority order. If no platform has that slug at all, the company is skipped and reported the same as a wrong explicit `ats` guess (see below) — nothing is charged for it. Auto-detect costs the same as specifying the platform directly: only the postings actually returned are charged. **Workday is never auto-detected** — its slug format is `"<host>/<site>"`, not a bare company name, so there's nothing to guess; always pass `"ats": "workday"` explicitly for it.

### Finding a company's slug
- **Greenhouse**: `boards.greenhouse.io/<slug>` or the `gh_jid`-style URL on their careers page.
- **Ashby**: `jobs.ashbyhq.com/<slug>`.
- **Lever**: `jobs.lever.co/<slug>`. Many well-known companies have migrated to a different ATS — if the slug 404s, they're no longer on Lever and the Actor skips them without failing.
- **Recruitee**: `<slug>.recruitee.com`.
- **Workable**: `apply.workable.com/<slug>`.
- **SmartRecruiters**: `jobs.smartrecruiters.com/<slug>` (identifier is case-sensitive, e.g. `BMWDealerCareers`).
- **Workday**: use `"<host>/<site>"` from the board's own URL, e.g. `okgov.wd1.myworkdayjobs.com/okgovjobs` → `{"ats":"workday","slug":"okgov.wd1.myworkdayjobs.com/okgovjobs"}`. The `wd<N>` host segment and the site name are both required and vary per company — copy them straight from the address bar on the company's own Workday career page (`https://<host>/<site>`).

## Output
One row per job posting:
`company, atsSource, jobId, title, department, team, departmentPath, employmentType, workplaceType, isRemote, location, secondaryLocations, country, region, city, salaryMin, salaryMax, salaryCurrency, salaryInterval, publishedAt, updatedAt, jobUrl, applyUrl, descriptionHtml, descriptionText, scrapedAt`

### Department and team (changed in 0.1.36)

A Greenhouse job carries exactly one department, and it is the **leaf** of the board's own org tree — on a large board that is an internal cost-centre node, not a department anyone would group by. Measured over **1,909 live postings across 5 boards**, **76% sit at depth ≥ 1** in the tree (up to depth 3 on Stripe: `Tech > Security (Planning Org) > Security (Planning Group) > 8611 Security Analytics`).

Since 0.1.36 this Actor also reads the board-level department endpoint — **one extra request per company, not per job** — rebuilds the chain, and reports:

| Field | Value |
| --- | --- |
| `department` | the **top-level** department (`"Tech"`) |
| `team` | the **leaf** the posting actually sits in (`"8611 Security Analytics"`), `null` when the job is already top-level |
| `departmentPath` | the whole chain root→leaf as an array, `null` on sources with no hierarchy |

The point is cross-company grouping: distinct `department` values on the same live boards collapse from **191 → 4** (Stripe), **44 → 13** (Databricks), **29 → 3** (Airbnb), **17 → 5** (Discord). `team` went from `null` on every Greenhouse row to filled on **76%**.

`departmentKeyword` now matches against `department`, `team` **and** `departmentPath` together, so a filter you wrote against a leaf name before 0.1.36 still matches — the filter got strictly wider, never narrower. If the departments endpoint is unavailable for a board, `department` falls back to the leaf name exactly as before and `team` is `null`. Ashby and Lever expose a real `team` field of their own and are unchanged; Recruitee, Workable, SmartRecruiters and Workday have no team concept and return `null`.

**Workday's board-listing API doesn't carry `department`, `employmentType` or an exact `publishedAt` date** — those only come back from a per-job detail call, which this Actor makes automatically for every kept posting when `includeDescriptions` is `true` (the default) **or when you set a filter that needs one of those fields** (`employmentTypeKeyword`, `departmentKeyword`, `postedAfter`, `postedBefore`, `descriptionKeyword`, `descriptionExcludeKeyword`) — so those filters work on Workday boards even with `includeDescriptions: false`. With descriptions off and none of those filters set, the detail call is skipped for a faster, cheaper-in-wall-clock run and those three fields come back `null` for Workday postings only (every other ATS is unaffected either way). `department` is populated from the posting's hiring organization name (e.g. `"131 DEPARTMENT OF CORRECTIONS"`), which is what Workday boards actually expose in place of a dedicated department field.

### Employment type
**Greenhouse boards never publish an employment type**, so `employmentType` is always `null` on Greenhouse rows and setting `employmentTypeKeyword` drops the entire board (measured: `airbnb`, 163 live postings → **0 rows**, while the same `"full"` filter returns rows on Ashby and Lever). The run logs a warning naming the company when this combination is used. This is an upstream gap, not a fetch this Actor can defer: Greenhouse's public job-board API has no such field. Filter Greenhouse companies on `titleKeyword` (`"intern"`, `"contract"`) or `descriptionKeyword` instead. Ashby (`FullTime`), Lever (`Regular Full Time (Salary)`), Recruitee, Workable and SmartRecruiters all expose it from the listing; Workday exposes it via the per-job detail call described above.

### Location
`location` is always the board's own text. `city`, `region` and `country` are the normalised breakdown, and both `locationKeyword` and `locationExcludeKeyword` match against all four plus `secondaryLocations` — so `locationExcludeKeyword: "United States"` drops a Greenhouse posting whose text only reads `"San Francisco, CA"`, and `locationKeyword: "California"` keeps it. Measured on the 163 live `airbnb` postings: `locationKeyword: "California"` returns **15** rows, only **1** of which says "California" in the board's own text.

Ashby, Lever, Recruitee, SmartRecruiters and Workable publish structured geography, so it is passed straight through. **Greenhouse publishes none** — it has a single hand-typed string per posting, and the same board mixes `"United States"`, `"San Francisco, CA"`, `"Bengaluru, India"`, `"Remote - Texas"` and `"Northeast - United States"`. This Actor normalises that string against a country/state/city vocabulary: measured over 1,914 live postings (`airbnb`, `databricks`, `figma`, `stripe`, `discord`, September 2026) it fills `country` on **95%**, `city` on **67%** and `region` on **50%**.

**Workday** publishes no geography in its list payload either — just one text field per posting, written differently by every tenant (`"US, CA, Santa Clara"`, `"France - Paris"`, `"Canada, Toronto"`). The same normaliser runs on it, so Workday rows now carry `city`/`region`/`country` instead of the nulls they returned before. Measured over 800 live postings (`nvidia`, `salesforce`, `adobe`, `okgov`, September 2026): from the list payload alone `country` fills on **35%**, `city` **22%** and `region` **14%**; when `includeDescriptions` is on, the per-job detail call adds Workday's one structured field and `country` reaches **100%** (its spelling `"United States of America"` is normalised to `"United States"` so it groups with every other source). The detail call also resolves multi-site postings the list shows only as `"3 Locations"`, which is where most of the extra `city`/`region` comes from. The practical effect on filtering: `locationKeyword: "United States"` matched **0** of those 800 Workday postings before and matches **89** now; `"California"` goes from **6** to **70**.

**Fixed in 0.1.39:** on county-government boards where the list text has no place name at all (`okgov`'s `"Muskogee County"`, `"Craig County"`, ...), `locationKeyword`/`locationExcludeKeyword` used to be checked before the per-job detail call that resolves `country`, silently dropping every one of those postings even though the resolved value would have matched. Measured live on `okgov`: `locationKeyword: "United States"` went from **0 of 10** to **10 of 10**, with `locationExcludeKeyword: "United States"` now correctly complementary (0 kept). Billing unchanged (1 `job` event per returned row).

**Re-measured after the fix (September 2026), and the "89 of 800" figure above is now a floor, not current:** a fresh live pull of `nvidia` (list text already parseable, unaffected by the bug) and the full visible `okgov` board (60 of 60 postings, not just the earlier 10-row sample) matched `locationKeyword: "United States"` on **101–102 of 120 postings (≈84%)**, run twice a minute apart (live boards drift slightly). The county-government board alone went from the old code's **0 of 60** to the fixed code's **60 of 60** — the earlier 10-row proof generalizes to the whole board, not just the sample.

Anything the vocabulary does not recognise stays `null` rather than being guessed, because a wrong country is worse than a missing one. In practice that means: multi-country zones (`"EMEA"`, `"APAC"`), placeholders (`"N/A"`, `"Remote"`), internal abbreviations some boards use for their own offices (`"SF"`, `"CHI"`, `"ATL"`), and the bare token `"Georgia"`, which is equally the US state and the country. Where a posting lists several places, the fields describe the **first** one and the rest stay in `secondaryLocations`. Greenhouse's `offices[]` array is deliberately **not** used to fill these fields: on some boards it contradicts the posting outright (a `databricks` posting located in `"Finland"` carries a `"Denmark"` office), so trusting it would invent wrong answers. The same restraint applies to Workday: its `"3 Locations"`/`"8 Locations"` placeholders, `"Statewide"`, county names (`"Tulsa County"`) and the street addresses some tenants put in the detail location (`"Stringtown - 13001 N Highway 69"`) all stay `null` rather than becoming a bogus city.

### Salary
Pay is returned when the board itself publishes it, and left `null` otherwise rather than guessed — **Ashby**, **Lever** and **Recruitee** expose structured pay ranges in their APIs, and **Greenhouse** boards with pay transparency switched on render the range as a structured block in the posting itself, which this Actor reads. Workable, SmartRecruiters and Workday carry no compensation data at all, so those stay `null`.

Coverage measured on live boards (September 2026): Ashby `ramp` 141/148 postings, Greenhouse `airbnb` 139/166, `databricks` 472/874, `figma` 99/152. Greenhouse boards that never turned pay transparency on (`stripe`, `discord`) return `null` — there is nothing in their payload to read.

Two Greenhouse specifics worth knowing. **The currency comes from the ISO code the board prints, not from the symbol** — 17 of airbnb's ranges pay in CAD and still show `$`, so reading the symbol would mislabel them USD; where a board prints a bare `$` with no code, `salaryCurrency` stays `null` instead of guessing. **A salary printed in prose is not parsed** — only Greenhouse's structured pay block is read, so a sentence like "the base salary range for this position is $196,000 to $220,500" buried in the description is left alone rather than risk picking up some other number from the text.

`salaryMin`/`salaryMax` are also filled on Greenhouse when `includeDescriptions` is `false` — the pay block is read out of the payload either way, so switching descriptions off to save bandwidth does not cost you the salary.

`salaryInterval` says what the number actually means — `year`, `month`, `week`, `day` or `hour`. Each ATS spells its period differently (`1 YEAR`, `monthly`, `per-year-salary`); they are normalized to one vocabulary so an hourly rate and an annual salary are never silently compared.

## Watch mode (only new postings since last run)
Set `watchLabel` to any name you like (`"backend-remote-eu"`) and the run stops returning the whole open-roles list every time and starts returning **only the postings that appeared since the previous run under that label**. This is the job-alert shape: schedule it hourly or daily and each run's dataset is your diff.

- **The first run for a label is a free baseline.** It records which postings are currently open (up to 5,000), returns **zero rows** and charges **nothing**. Run it again later to get what's new.
- **Already-delivered postings are dropped before any charge**, so a run with nothing new costs you nothing.
- **The baseline lives in your own Apify account** — a named key-value store `fetchsmith-ats-watch`, key `watch-<label>-<fingerprint>`. Nothing is kept on our side.
- **The fingerprint covers the company list and every filter** (`titleKeyword`, `titleExcludeKeyword`, `locationKeyword`, `locationExcludeKeyword`, `employmentTypeKeyword`, `hasSalary`, `remoteOnly`, `postedAfter`, `includeDescriptions`, plus `departmentKeyword`, `descriptionKeyword`, `descriptionExcludeKeyword`, `postedBefore`, `minSalary` and `maxSalary` when you set them). Change any of them and you get a fresh baseline instead of a dump of postings the old filters had excluded. `maxJobsPerCompany`/`maxResults` are *not* in the fingerprint — they are cost caps, not criteria.
- **`maxJobsPerCompany` caps what is delivered, not what is checked.** In watch mode the run scans the whole match set for each company (so a new role that sorts 40th is still found) but still delivers at most `maxJobsPerCompany` new postings per company per run; the rest arrive on the following run.
- **Baseline size cap:** the recorded baseline holds at most 20,000 posting ids per label; once a label crosses that, the oldest ids are dropped to make room. A dropped id is re-delivered — and re-charged — as "new" on a future run. This only bites a very broad, unfiltered watch on a long company list; narrowing `titleKeyword`/`locationKeyword` or trimming `companies` keeps a label well under the cap. A run that actually drops ids logs a warning and says so in its status message.

## Pricing
Pay per result: **$0.0015 per job posting on the free plan, dropping to $0.001 on Gold and above** (Bronze $0.0013, Silver $0.0011), with no Actor-start fee. 1,000 postings costs $1.50 on the free plan, $1.00 on Gold. You are charged only for postings that pass your filters and actually reach your dataset.

## FAQ
**How do `titleKeyword`, `locationKeyword`, `descriptionKeyword`, `remoteOnly` and the date bounds combine?** All of them must pass (AND) — set only the ones you need, leave the rest empty/`false`.

**Can I filter on the description without paying for description columns?** Yes. `descriptionKeyword`/`descriptionExcludeKeyword` work with `includeDescriptions: false`: the text is fetched, matched against your keyword, then stripped from the row, so you get lean rows filtered on their full body text.
**What if `companies` has the same `{ats, slug}` entry twice?** Deduped automatically — an exact repeat is only fetched (and charged) once per run.

**What happens if a board has a transient connection blip mid-run?** Every ATS request (Greenhouse, Ashby, Lever, Recruitee, Workable, SmartRecruiters and Workday, including Workday's paged listing calls) is retried up to 3 times on a connection-level failure — measured at roughly 1 fresh request in 4 for HTTP/2 faults, 2026-09-21 — before that company is marked errored in the completion summary. A single blip no longer costs you that company's whole board.

**Does `maxJobsPerCompany` cap before or after my filters run?** After. Filters are applied first, then up to `maxJobsPerCompany` of the *matching* postings are kept per company — so `{"titleKeyword": "engineer", "maxJobsPerCompany": 3}` returns 3 postings that actually contain "engineer", not the first 3 raw postings off the board (verified live: a real Greenhouse board run with those exact inputs returned 3/3 titles containing "Engineer"/"Engineering").

**Date bounds: both ends inclusive, and a bad date stops the run.** `postedAfter` starts at 00:00:00.000 UTC on the day you name and `postedBefore` ends at 23:59:59.999 UTC on the day you name, so `postedAfter: "2026-08-01"` + `postedBefore: "2026-08-31"` is exactly August — no posting is trimmed off either end. Both accept `YYYY-MM-DD` or a full ISO datetime (`2026-08-01T12:00:00Z`) and **nothing else**: `06/15/2026`, `2026-8-1`, `last week` and calendar-impossible dates like `2026-02-30` fail the run with an error naming the input. That is deliberate. This Actor charges per posting, and the obvious alternative — parse what we can, ignore the rest — means an unreadable bound silently *deletes* your date filter and hands you (and bills you for) the entire unfiltered board. A filter that can't be honoured should stop the run, not quietly widen it.

**Will `postedAfter`/`postedBefore` filter out a posting that has no date?** No — if an ATS doesn't return a `publishedAt` for a posting, that posting is kept regardless of the date bounds. On Workday the date comes only from the per-job detail call, and setting either bound now triggers that call automatically, so the window applies to Workday boards too.

**Which ATSes expose salary?** Ashby, Lever and Recruitee publish a structured pay range in their API, and Greenhouse boards with pay transparency on print one in the posting body, which this Actor parses (139/166 postings on a live airbnb board, 472/874 on databricks). Workable, SmartRecruiters and Workday carry no compensation data at all, so those come back `null` rather than guessed.

**Does `minSalary`/`maxSalary` compare against an annual salary?** Not necessarily — it compares the raw number as the ATS posted it, in whatever `salaryInterval` that posting uses (year, month, week, day or hour all appear in the wild). Mixing companies on very different intervals in one run means the filter isn't apples-to-apples; check `salaryInterval`/`salaryCurrency` on each row if that matters to you.

**A company I need isn't on any of these 7 ATSes — can it still be scraped?** Only if it uses one of the 7 (or a client-side board no ATS API backs, which this Actor can't reach). Message support@fetchsmith.com with the company's careers URL if you're unsure which ATS it runs on.

**I set `watchLabel` and got zero results — is it broken?** No. Either it was the baseline run (the log says so explicitly, and you were charged nothing), or nothing new has been posted on those boards since your last run. For a watch, zero is the normal, expected, free result most of the time.

**How do I reset a watch baseline?** Delete its record from the `fetchsmith-ats-watch` key-value store in your Apify account, or just use a new `watchLabel`. Changing any filter also starts a fresh baseline automatically.

**One of my boards failed during the baseline run — what happens?** That board contributes nothing to the baseline, so its currently-open postings will come back as "new" (and billable) on the next run. The baseline run logs a loud warning naming any board that failed, so you can re-seed before scheduling it.

**Why did a company I listed return zero postings?** Either it's genuinely down to 0 open roles, or it has migrated off that ATS — the run logs (not a failure) list any company that 404s so you can find its new slug/ATS instead of getting a silently empty result.

**How is `webhookUrl` different from Apify's own platform webhooks?**
Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `companiesScanned`, `companiesErrored`, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchSkippedCount`/`baselineTruncated`/`baselineTruncatedTotal`) once the run finishes and every posting is already pushed and charged. Especially useful with `watchLabel` on a scheduled job alert: your endpoint gets told how many new postings landed without polling the dataset, and `companiesErrored` warns you when a board failed to answer. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

## Notes
Only public, no-login job-board data is collected — the same postings anyone can see on the company's own careers page. Job descriptions occasionally include a named recruiter contact the company itself chose to publish; this Actor does not extract or highlight individual contact data as a feature. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides
- [Six ATS job-board JSON APIs, six different ideas of what a job posting is](https://fetchsmith.com/blog/ats-job-board-json-apis-six-shapes)
- [Workday's public career-site API has no auth, a hard page-size cap, and no department field](https://fetchsmith.com/blog/workday-career-site-json-api)
- [A Try-for-free click shouldn't cost a first-time buyer $1.26 and five minutes](https://fetchsmith.com/blog/default-inputs-should-not-cost-you-five-minutes)
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — the general failure modes `watchLabel` is built to avoid.
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for. Reproduced on this Actor, closed with truncation tracking.
- https://fetchsmith.com/tools
- Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/ats-jobs-scraper
