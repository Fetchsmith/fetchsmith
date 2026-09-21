# Remote Jobs Scraper – Remotive, Remote OK, Jobicy & Arbeitnow in one de-duplicated feed

Four public remote-job boards, one normalized JSON schema, **de-duplicated across boards before you are charged**.

## What it does

Pulls live remote job postings from four documented, public, no-login job-board APIs and merges them:

| Source | What it covers | Salary data |
|---|---|---|
| [Remotive](https://remotive.com) | Remote tech, design, marketing, support roles, worldwide. Its public feed is small — **20 live postings total on 2026-09-21**, regardless of the `limit` you ask for | free-text range (`salaryText`) |
| [Remote OK](https://remoteok.com) | The ~100 most recent Remote OK postings | numeric USD range on many rows |
| [Jobicy](https://jobicy.com) | The 50 most recent Jobicy postings | numeric range + currency + period on many rows |
| [Arbeitnow](https://www.arbeitnow.com) | A general European board — **only** rows flagged remote are returned | none |

Every row says which board it came from (`source`, `sourceSite`) and links to the original posting (`url`).

## Cross-board de-duplication (and what it actually measures)

When a job is syndicated to more than one of these boards, a naive aggregator returns it twice — and on a pay-per-result Actor you pay for both copies. This Actor folds copies into one row (matched on normalized company + title, newest kept) **before** the charge is made: the extra boards show up as `alsoOn: ["remoteok","jobicy"]` with their links in `duplicateUrls`, so you keep the information without paying for it twice. Set `dedupe: false` to get one row per board copy.

**Measured honestly:** on a full four-board pull on 2026-09-21, **0 of 181** postings were cross-board duplicates — these four boards curate largely disjoint sets, so the overlap on any given day may be small or zero. Treat de-duplication as a guarantee that you will never be billed twice for one posting, not as a claim that the boards overlap heavily.

## Use cases

- **Job boards and newsletters** — one merged, deduplicated feed to republish or email, with the source link each board's terms require.
- **Recruiters and sourcers** — watch which companies are hiring remotely for a given stack (`searchKeyword: "rust"`, `salaryOnly: true`).
- **Market/comp research** — collect salary ranges across boards over time; `salaryMin`/`salaryMax`/`salaryCurrency`/`salaryPeriod` are normalized where the board publishes them.
- **Job-seeker automations** — a daily run with `postedAfter` set to yesterday gives exactly the new postings, nothing else.

## Input

| Field | Type | Notes |
|---|---|---|
| `sources` | array | Any subset of `remotive`, `remoteok`, `jobicy`, `arbeitnow`. Default: all four. An unknown name **fails the run** rather than being quietly dropped. |
| `searchKeyword` | string | Kept if the title, company, category or tags contain it (case-insensitive). Also passed to Remotive's and Jobicy's own search parameters. |
| `titleExcludeKeyword` | string | Drops postings whose title contains it, e.g. `Senior`. |
| `companyKeyword` | string | Substring match on company name. |
| `locationKeyword` | string | Substring match on the location/region field. |
| `postedAfter` / `postedBefore` | string | `YYYY-MM-DD`, UTC, **both bounds inclusive whole days**. A value that is not a real calendar date fails the run — see the FAQ. |
| `salaryOnly` | boolean | Keep only rows carrying a salary range or salary text. |
| `dedupe` | boolean | Default `true`. See above. |
| `includeDescription` | boolean | Adds `descriptionHtml`. Off by default — descriptions are large. |
| `maxPagesPerSource` | integer | Only affects Arbeitnow, the one paginated source (250/page). Default 2. |
| `maxResults` | integer | Stop after this many unique postings are pushed and charged. Default 100. |

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
  "salaryMin": null,
  "salaryMax": null,
  "salaryCurrency": null,
  "salaryPeriod": null,
  "publishedAt": "2026-09-18T16:43:22.000Z",
  "alsoOn": [],
  "duplicateUrls": [],
  "scrapedAt": "2026-09-21T09:40:00.000Z"
}
```

### Location is a region, not a city

Remote boards publish the region a candidate must be in (`"Worldwide"`, `"USA, Canada"`, `"UK"`), not an office address, and some rows carry no location at all. `locationKeyword` therefore drops rows with an empty location — that is a filter on what the board actually published, not a geocoder.

### Salary

`salaryMin`/`salaryMax` are only set when the board publishes numbers (Remote OK, Jobicy). Remote OK's zeros mean "not disclosed" and are normalized to `null`, not `0`. Remotive publishes a free-text range, kept verbatim in `salaryText`. **No currency conversion is performed** — `salaryCurrency` tells you what the number is in.

## Pricing

Pay per result: you are charged once per **unique** posting pushed to the dataset. No start fee, no per-run fee, nothing charged for duplicates, filtered-out rows or empty runs.

## FAQ

**What happens if I typo a date?** The run fails immediately with an error naming the field and the bad value. It is deliberate: if a bad `postedAfter` were ignored, the run would return (and bill for) every posting on all four boards instead of your window, and a warning line in a successful run is not something anyone reads. `2026-6-5`, `06/15/2026` and `2026-02-30` are all rejected — the last one because it is not a real date, even though JavaScript would silently roll it over to March 1.

**Are both date bounds inclusive?** Yes. `postedAfter` starts at 00:00:00.000Z of that day and `postedBefore` ends at 23:59:59.999Z, so a job posted at 14:00Z on your end date is included.

**How are duplicates detected?** Normalized company name + normalized job title (lowercased, punctuation collapsed). That catches the common syndication case ("Acme, Inc." on one board and "Acme Inc" on another). It will not merge two genuinely different openings that share a title at the same company — those stay separate rows.

**I set a small `maxResults` and got rows from only one board — is that a bug?** No. The merge is global newest-first across all four boards, so a small cap samples *recency*, not *boards*: whichever board happened to publish the freshest postings that minute fills the cap. Ask for at least 50 results to see all four represented, or run once per board with `sources` set to a single board if you need a guaranteed per-board slice.

**What if one board is down?** The run continues with the others and logs a warning naming the failed board. You are only charged for rows you actually receive.

**Does this need a login, API key or proxy?** No. All four endpoints are public and documented, and the Actor is HTTP-only — no headless browser.

**Why are Arbeitnow rows mostly German?** Arbeitnow is a European (largely German) board; only its postings flagged remote are returned here. Drop `arbeitnow` from `sources` if you want US-centric boards only.

## Sources and attribution

All four APIs are public and ask for credit in return. This Actor puts the source board and the original posting URL on every row so you can honour that downstream: **if you republish these postings, link back to [Remotive](https://remotive.com), [Remote OK](https://remoteok.com), [Jobicy](https://jobicy.com) and [Arbeitnow](https://www.arbeitnow.com), and point application buttons at the original job URL in the `url` field.** Remote OK's API terms require a followed link back; Jobicy's asks that apply buttons resolve to the original posting.

## Notes

- Public data only: no login, no personal data beyond what the boards publish publicly about a job.
- Feeds are snapshots of what each board serves at run time; Remote OK and Jobicy expose only their most recent postings, so historical `postedBefore` windows will thin out on those two.

## Related guides

- [Four public remote-job APIs with no key — and how small each feed really is](https://fetchsmith.com/blog/remote-job-board-json-apis-four-feeds) — measured feed sizes, Remotive's decorative `limit`, Remote OK's legal-notice row, and why the four boards don't overlap
- [FetchSmith blog](https://fetchsmith.com/blog) — data-source guides and API notes
- [All FetchSmith Actors](https://fetchsmith.com/tools)
