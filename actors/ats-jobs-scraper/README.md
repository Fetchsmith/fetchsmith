# ATS Jobs Scraper – Greenhouse, Ashby, Lever & Recruitee

Live job postings straight from any company's own career board on **Greenhouse, Ashby, Lever or Recruitee**, normalized into one schema — no matter which ATS the company uses.

## What it does
- Fetches each company's public job-board API directly (no browser, no login) for **Greenhouse**, **Ashby**, **Lever** and **Recruitee**.
- Normalizes every posting into one shared schema (title, department, team, employment type, workplace type, remote flag, location, salary where the ATS exposes it, timestamps, apply URL, description).
- Client-side filters (title keyword, location keyword, remote-only, posted-after date) are applied **before** charging, so you only pay for postings you actually want.
- Companies that have migrated off an ATS (very common for Lever) are skipped with a warning, not a failed run.
- Pay per result: you are charged only for job postings actually returned. **No start fee.**

## Input
| Field | Type | Description |
|---|---|---|
| `companies` | array | `[{"ats": "greenhouse\|ashby\|lever\|recruitee", "slug": "<company-slug>"}]`. The slug is the company identifier in their career-board URL, e.g. `jobs.ashbyhq.com/ramp` → `{"ats":"ashby","slug":"ramp"}`. |
| `titleKeyword` | string | Only keep postings whose title contains this text. |
| `locationKeyword` | string | Only keep postings whose location/city/country contains this text. |
| `remoteOnly` | boolean | Only keep postings the ATS marks as remote. Default `false`. |
| `postedAfter` | string | ISO date; only keep postings published on/after it. |
| `includeDescriptions` | boolean | Include full HTML + plain-text description. Default `true`. |
| `maxJobsPerCompany` | integer | Cap postings pulled per company before filters. Default `500`. |
| `maxResults` | integer | Cap total postings returned across all companies. Default `2000`. |
| `proxyConfiguration` | object | Apify Proxy config. Default: Apify Proxy on. |

### Finding a company's slug
- **Greenhouse**: `boards.greenhouse.io/<slug>` or the `gh_jid`-style URL on their careers page.
- **Ashby**: `jobs.ashbyhq.com/<slug>`.
- **Lever**: `jobs.lever.co/<slug>`. Many well-known companies have migrated to a different ATS — if the slug 404s, they're no longer on Lever and the Actor skips them without failing.
- **Recruitee**: `<slug>.recruitee.com`.

## Output
One row per job posting:
`company, atsSource, jobId, title, department, team, employmentType, workplaceType, isRemote, location, secondaryLocations, country, region, city, salaryMin, salaryMax, salaryCurrency, publishedAt, updatedAt, jobUrl, applyUrl, descriptionHtml, descriptionText, scrapedAt`

Salary fields are populated when the ATS itself exposes them (confirmed on Recruitee and Lever boards that publish pay ranges); left `null` otherwise rather than guessed.

## Pricing
`job` — $0.0015 per job posting returned. No start fee.

## Notes
Only public, no-login job-board data is collected — the same postings anyone can see on the company's own careers page. Job descriptions occasionally include a named recruiter contact the company itself chose to publish; this Actor does not extract or highlight individual contact data as a feature. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides
- https://fetchsmith.com/tools
- Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/ats-jobs-scraper
