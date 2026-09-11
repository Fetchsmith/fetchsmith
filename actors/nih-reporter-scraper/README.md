# NIH RePORTER Scraper – No 15k Row Cap, PubMed Join

Export **every NIH-funded research project** from the official [NIH RePORTER](https://reporter.nih.gov) API — 2.9M+ project records going back to 1985 — filtered by keyword, fiscal year, institute (IC), activity code, organization, state or principal investigator. Each project comes back with its award amounts, PI and program officer, institution, study section and congressional district, plus an optional join to **the PubMed papers that project produced**.

No API key, no login, no proxy. Public data only.

## What it's for

- **Biotech / pharma competitive intelligence** — who is NIH-funded in your therapeutic area, at what dollar level, and which papers came out of it.
- **University research offices & grant consultants** — benchmark awards by institute, activity code (R01 vs R21 vs SBIR R43/R44) or peer institution.
- **Research-tooling and CRO sales teams** — find labs that just received a new (`awardType: "1"`) award in your space, with the institution and city attached.
- **Bibliometrics / science-of-science** — a funding-to-publication link for a whole field in one dataset.

## Two things this Actor does that the API doesn't

**1. It gets past the 15,000-row wall.** NIH RePORTER caps `offset + limit` at 15,000 and offers no cursor — a single fiscal year already holds 83,000+ projects, so a broad query is simply untraversable against the raw API. This Actor detects when a query exceeds the wall and automatically splits it across fiscal year, then administering institute, then award type, merging and de-duplicating on `appl_id` so you never pay twice for the same record.

**2. It refuses to silently ignore your filter.** NIH RePORTER accepts an unrecognised criteria *field name* with HTTP 200 and returns the entire unfiltered index as if the filter had worked — "success" that quietly means "everything". Every criteria key is validated against an allowlist before the request is sent, so a filter either applies or the run fails loudly.

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
| `projectNums` | array | Exact lookup — **ignores every other filter** |
| `activeOnly` | boolean | Currently active projects only |
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

**Is any personal contact data collected?** No. The NIH RePORTER schema contains no email or phone field at all. PI and program-officer **names** are included because they are statutory public disclosure, published on every reporter.nih.gov project page — the same class of data as a federal contract awardee's name.

## Pricing

`result` — **$0.0015 per returned item, no Actor-start fee.** Below the per-result price of the largest NIH RePORTER listing on Apify, and with no start fee to pay before the first row.

## Notes

Only public data from NIH RePORTER's official API is collected. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides

- https://fetchsmith.com/blog/grants-gov-federal-grant-opportunities-json-api
- https://fetchsmith.com/tools

## Source code

https://github.com/Fetchsmith/fetchsmith/tree/main/actors/nih-reporter-scraper
