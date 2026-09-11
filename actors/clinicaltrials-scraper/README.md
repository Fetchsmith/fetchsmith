# ClinicalTrials.gov Scraper – Condition, Phase & Site Mode

Pulls studies from **ClinicalTrials.gov**, the US NIH/NLM registry of clinical trials, using its own official API v2 — no API key, no login, no proxy. 602,520+ studies covered.

## What you get

25 flat fields per study, including the ones most ClinicalTrials.gov Actors skip:

| Field | Why it matters |
| --- | --- |
| `rowsPerStudy: "site"` mode | One row per **trial site** instead of one per study — facility name, city, state, country and lat/lon, so a site-selection or patient-recruitment buyer doesn't have to explode the array themselves. A study averages 5 sites (max seen: 110), so this mode returns roughly 5x more billable rows for the same query. |
| `phases`, `studyType`, `overallStatus` | Filterable and returned flat, not nested. |
| `enrollmentCount`, `sex`, `minimumAge`, `maximumAge`, `healthyVolunteers` | The eligibility snapshot without parsing free-text criteria. |
| `hasResults` | Whether the trial has posted a results section — filterable via `hasResultsOnly`. |
| `interventions` | Type + name for every drug/device/procedure arm. |
| `studyUrl` | Direct link to the public study page. |

**We do not ship contact people, phone numbers or emails — ever.** ClinicalTrials.gov's own API returns named individuals and personal email addresses in `centralContacts`/location `contacts` (we found a real `@gmail.com` in a live sample). Several competitor Actors resell that as a "contact finder." We deliberately drop it; `locations`/`site` carries facility, city, state, country and geo-coordinates only.

## Who uses this

- **Pharma / CRO business development** tracking competitor trials by condition or sponsor.
- **Site-selection teams** finding which facilities run trials for a given condition (`rowsPerStudy: "site"`).
- **Investor / market research** watching a sponsor's pipeline by phase and status.
- **Patient-advocacy and recruitment groups** finding actively recruiting trials near a location.

## Input

```json
{
  "conditions": "breast cancer",
  "overallStatus": ["RECRUITING"],
  "phases": ["PHASE3"],
  "maxResults": 100
}
```

| Input | Notes |
| --- | --- |
| `conditions` / `interventions` / `sponsors` / `locations` | Free-text, each maps to the API's own `query.cond` / `query.intr` / `query.spons` / `query.locn`. ANDed together. |
| `searchQuery` | General free-text search across titles, outcomes and eligibility text. |
| `overallStatus` | e.g. `RECRUITING`, `COMPLETED`, `TERMINATED`. All 14 official values supported. |
| `studyTypes` | `INTERVENTIONAL`, `OBSERVATIONAL`, `EXPANDED_ACCESS`. |
| `phases` | `EARLY_PHASE1`..`PHASE4`, `NA`. Only meaningful for interventional studies — about 1 in 5 studies overall have no phase at all. |
| `hasResultsOnly` | Only studies with a posted results section. |
| `rowsPerStudy` | `"study"` (default) or `"site"`. |
| `maxResults` | Up to 50,000. Token-based paging, no offset wall. |

## Sample output (`rowsPerStudy: "study"`)

```json
{
  "nctId": "NCT04137653",
  "briefTitle": "Treatment of Triple-negative Breast Cancer With Albumin-bound Paclitaxel as Neoadjuvant Therapy",
  "overallStatus": "RECRUITING",
  "studyType": "INTERVENTIONAL",
  "phases": ["PHASE3"],
  "enrollmentCount": 1498,
  "leadSponsor": "Shengjing Hospital",
  "conditions": ["Breast Cancer"],
  "interventions": [{"type": "DRUG", "name": "nab-Paclitaxel+carboplatin"}],
  "locationCount": 1,
  "studyUrl": "https://clinicaltrials.gov/study/NCT04137653"
}
```

## The pageSize trap

Ask the API for `pageSize=1001` and it doesn't 400 — it silently returns **200 with only 1000 rows**, no warning. This Actor always clamps to 1000 and pages with the API's own `nextPageToken`, which has no offset wall (5,000+ unique rows walked in one run during testing, no rate limiting).

## Pricing

**$0.0015 per result, no Actor-start fee.** The 41-user Store leader in this niche charges **$0.16 to start plus $0.012/result** — about 8x more per row, with a start fee we don't charge at all. 1,000 studies costs $1.50 here vs. $12.16 there.

## FAQ

**Why did I get zero rows?**
Filters are ANDed — combining a narrow condition, sponsor and location at once often genuinely matches nothing. Drop one filter and retry. Also, `phases` only applies to interventional studies with a phase assigned; pairing it with `studyTypes: ["OBSERVATIONAL"]` always returns nothing.

**Are `phases`, `maximumAge` and `collaborators` always present?**
No. Measured on a live 50-study sample: `phases` populated on ~70%, `maximumAge` on ~48%, `collaborators` on ~24%. Don't treat a missing value as a scraping error — most studies genuinely don't set these fields.

**Does this return contact names, phone numbers or emails?**
No, by design — see above. If you need to contact a trial's coordinator, use the `studyUrl` to view the listing directly on ClinicalTrials.gov.

**Is this legal?**
Yes. ClinicalTrials.gov is run by the US National Library of Medicine and publishes this API for public reuse. All returned data (excluding the contact fields we deliberately drop) is public-interest study/sponsor/site metadata, not personal data about trial participants.

## Related guides

- [All FetchSmith tools](https://fetchsmith.com/tools)
- [Source code](https://github.com/Fetchsmith/fetchsmith/tree/main/actors/clinicaltrials-scraper)
