# NIH RePORTER Scraper – No 15k Row Cap, PubMed Join

Export **every NIH-funded research project** from the official [NIH RePORTER](https://reporter.nih.gov) API — 2.9M+ project records going back to 1985 — filtered by keyword, fiscal year, institute (IC), activity code, organization, state or principal investigator. Each project comes back with its award amounts, PI and program officer, institution, study section and congressional district, plus an optional join to **the PubMed papers that project produced**.

No API key, no login, no proxy. Public data only.

## What it's for

- **Biotech / pharma competitive intelligence** — who is NIH-funded in your therapeutic area, at what dollar level, and which papers came out of it.
- **University research offices & grant consultants** — benchmark awards by institute, activity code (R01 vs R21 vs SBIR R43/R44) or peer institution.
- **Research-tooling and CRO sales teams** — find labs that just received a new (`awardType: "1"`) award in your space, with the institution and city attached.
- **Bibliometrics / science-of-science** — a funding-to-publication link for a whole field in one dataset.

## Three things this Actor does that the API doesn't

**1. It gets past the 15,000-row wall.** NIH RePORTER caps `offset + limit` at 15,000 and offers no cursor — a single fiscal year already holds 83,000+ projects, so a broad query is simply untraversable against the raw API. This Actor detects when a query exceeds the wall and automatically splits it across fiscal year, then administering institute, then award type, merging and de-duplicating on `appl_id` so you never pay twice for the same record.

**2. It refuses to silently ignore your filter.** NIH RePORTER accepts an unrecognised criteria *field name* with HTTP 200 and returns the entire unfiltered index as if the filter had worked — "success" that quietly means "everything". Every criteria key is validated against an allowlist before the request is sent, so a filter either applies or the run fails loudly.

**3. It remembers what it already sent you (`watchLabel`).** Give a query a name — `watchLabel: "crispr-nci-weekly"` — and the Actor keeps a per-label record of the projects it has already delivered to you, so a scheduled run returns *only what is new since last time* and you are charged for nothing else. The first run on a new label is a **free baseline run**: it records what already matches, returns zero results, and charges nothing. Every run after that returns new projects only. This is your own baseline, not NIH's: `newlyAddedOnly` uses RePORTER's stateless "recently added to the index" flag, which keeps re-returning the same projects on every run until they age out of it. Change any other filter and the label starts a fresh baseline, so "new" always means new *for the exact query you are watching*.

## Input

| Field | Type | Description |
| --- | --- | --- |
| `keyword` | string | Full-text over project title, abstract and NIH terms (default `"cancer"`) |
| `fiscalYears` | array | e.g. `[2024, 2025]`. Empty = all years |
| `agencyIcCodes` | array | Administering institute, e.g. `["NCI","NIAID"]` |
| `activityCodes` | array | Award mechanism, e.g. `["R01","R21","R43"]` |
| `awardTypes` | array | `1` new, `2` renewal, `3` supplement, `5` continuation, … |
| `orgNames` | array | Funded organization, partial match |
| `orgStates` | array | Two-letter US state codes |
| `piNames` | array | PI name contains, e.g. `["Doudna"]` |
| `minAwardAmount` | integer | Only awards of at least this many dollars (e.g. `1000000`) |
| `maxAwardAmount` | integer | Only awards of at most this many dollars — combine with the minimum for an exact band |
| `projectNums` | array | Exact lookup — **ignores every other filter** |
| `activeOnly` | boolean | Currently active projects only |
| `newlyAddedOnly` | boolean | Only projects recently added to RePORTER — cheap incremental pulls |
| `watchLabel` | string | Name a saved query to get **only projects new since its last run** — see below |
| `excludeSubprojects` | boolean | Drop P01/U54 subproject duplicates (default `true`) |
| `includePublications` | boolean | Join linked PubMed PMIDs (default `true`) |
| `includeAbstract` | boolean | Include abstract + public-health relevance (default `true`) |
| `maxResults` | integer | Stop after this many records (default 100) |

`projectNums` is an exclusive mode on purpose: looking up `R01CA234538` while a fiscal-year or institute filter is set would otherwise return zero rows, which is indistinguishable from a typo. Ask by number, get that project.

## Output

`applId`, `projectNum`, `coreProjectNum`, `subprojectId`, `fiscalYear`, `projectTitle`, `activityCode`, `awardType`, `fundingMechanism`, `awardAmount`, `directCostAmt`, `indirectCostAmt`, `isActive`, `isNew`, `projectStartDate`, `projectEndDate`, `budgetStart`, `budgetEnd`, `awardNoticeDate`, `dateAdded`, `agencyCode`, `icCode`, `icAbbreviation`, `icName`, `icFundings[]`, `opportunityNumber`, `cfdaCode`, `studySection`, `spendingCategoriesDesc`, `contactPiName`, `principalInvestigators[]`, `programOfficers[]`, `orgName`, `orgCity`, `orgState`, `orgCountry`, `orgZip`, `orgDeptType`, `orgUei`, `orgType`, `congDist`, `latitude`, `longitude`, `terms[]`, `url`, `abstractText`, `publicHealthRelevance`, `publicationCount`, `pubmedIds[]`

Sample row (trimmed):

```json
{
  "projectNum": "5R01CA279801-02",
  "coreProjectNum": "R01CA279801",
  "fiscalYear": 2024,
  "projectTitle": "Orthogonal CRISPR GEMMs",
  "activityCode": "R01",
  "awardAmount": 635830,
  "directCostAmt": 393703,
  "icAbbreviation": "NCI",
  "studySection": "Genomics, Computational Biology and Technology Study Section[GCAT]",
  "contactPiName": "MCMANUS, MICHAEL T",
  "orgName": "UNIVERSITY OF CALIFORNIA, SAN FRANCISCO",
  "orgState": "CA",
  "congDist": "CA-11",
  "publicationCount": 0,
  "pubmedIds": [],
  "url": "https://reporter.nih.gov/project-details/10794392"
}
```

### Field population — read this before you build on a field

Grant records (R/P/U/K/F activity codes) populate almost everything. **R&D contract records (`N01`, `funding_mechanism: "R and D Contracts"`) are much thinner** — verified live: `publicHealthRelevance`, `awardType`, `opportunityNumber`, `cfdaCode` and `studySection` all come back `null`, and `directCostAmt`/`indirectCostAmt` are usually absent on older rows too. Filter on `fundingMechanism` if you need a uniformly populated set.

`publicationCount` is legitimately `0` for many recent projects — papers take years to appear, so a 2024 new award usually has none yet. It is not a join failure.

## FAQ

**Does it need an NIH account or API key?** No. NIH RePORTER's API is fully public.

**How do I get more than 15,000 rows?** Just raise `maxResults`; the chunking is automatic. If a query is so broad that even chunking can't reach the rest, the log says so explicitly rather than silently truncating.

**Why does one project appear several times?** NIH RePORTER records one row per *fiscal year of funding*. `R01CA234538` returns six rows for its six funded years. De-duplicate on `coreProjectNum` if you want one row per project.

**Can I filter by award size?** Yes — `minAwardAmount` and `maxAwardAmount`, either alone or as a band. One caveat we measured rather than assumed: NIH RePORTER excludes projects with **no award amount recorded** from any amount-filtered query — about 2.8% of a 500-row FY2024 sample, matching a 2.6% drop in the reported total. So an amount filter is slightly narrower than "every project in that range"; the run log warns you whenever one is active.

**How do I pull only what's new since my last run?** Two options. `watchLabel` is the precise one: name your query, and the Actor returns only the projects it has not already delivered under that name (first run = free baseline, zero results). `newlyAddedOnly: true` is the coarse one — RePORTER's own "recently added to the index" flag, about 8.9k projects index-wide when measured, almost all current-fiscal-year. Use `watchLabel` for a scheduled alert on a specific query; use `newlyAddedOnly` for a cheap sweep of whatever NIH just published. They combine fine.

**Where is the watch baseline kept, and can I reset it?** In a named key-value store, `fetchsmith-nih-watch`, **on your own Apify account** — one record per label + filter combination, holding the `appl_id`s already sent plus the last run time. Delete the record (or just use a new label) to start over. Nothing about your saved queries leaves your account. Two caveats worth knowing: a project that was skipped because it fell outside `maxResults` is *not* marked as delivered, so it comes back on the next run; and a baseline caps at 15,000 projects (RePORTER's own paging wall), so watch a query narrow enough to fit under that — the run log warns you if it doesn't.

**Is any personal contact data collected?** No. The NIH RePORTER schema contains no email or phone field at all. PI and program-officer **names** are included because they are statutory public disclosure, published on every reporter.nih.gov project page — the same class of data as a federal contract awardee's name.

## Pricing

`result` — **$0.0015 per returned item, no Actor-start fee.** Below the per-result price of the largest NIH RePORTER listing on Apify, and with no start fee to pay before the first row.

## Notes

Only public data from NIH RePORTER's official API is collected. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides

- https://fetchsmith.com/blog/nih-reporter-grants-json-api
- https://fetchsmith.com/blog/grants-gov-federal-grant-opportunities-json-api
- https://fetchsmith.com/tools

## Source code

https://github.com/Fetchsmith/fetchsmith/tree/main/actors/nih-reporter-scraper
