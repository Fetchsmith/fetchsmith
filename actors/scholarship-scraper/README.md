# Scholarship Scraper (bold.org)

Scrape **scholarship listings from bold.org** — the largest single scholarship platform — into JSON, CSV or Excel. No login, no browser, no proxy.

Every row is a complete scholarship: award amount, number of awards, deadline, essay prompt, judging criteria, education levels, donor, and the **number of people who have already applied** — plus a computed `applicantsPerAward` ratio so you can see at a glance which awards are actually winnable.

**Pay per result: $0.0005 per scholarship. No start fee** — a run that returns nothing costs nothing, and scholarships removed by your filters are never charged.

## What you can do with it

- **Build a scholarship feed for a school, newsletter or app** — crawl `by-major`, `by-state`, `by-type` and `by-demographics` categories and get a de-duplicated list.
- **Find the winnable ones** — sort your dataset by `applicantsPerAward`; a $1,000 award with 40 applicants beats a $10,000 award with 12,000.
- **"Closing this month" lists** — set `deadlineBefore` to the end of the month and `openOnly: true`.
- **Filter by money** — `minAwardAmount: 5000` keeps only the serious awards.
- **Search by topic** — `searchQuery: "nursing"` finds the matching categories for you, so you do not have to know bold.org's category slugs.
- **Prep essays in bulk** — `essayTopic` gives the actual essay question(s) as plain text, with `essayMinLength` / `essayMaxLength`.
- **Segment by audience** — `educationLevels: ["highschool"]` for graduating seniors, `["graduate"]` for grad students.

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `categoryTypes` | array | `["by-major"]` | Which category families to crawl: `by-major`, `by-state`, `by-type`, `by-demographics`, `by-year` |
| `maxCategoryPages` | integer | `20` | How many category pages to fetch (≈30 scholarships each) |
| `maxResults` | integer | `200` | Hard cap on rows returned — also your cost cap |
| `startUrls` | array | — | Specific bold.org category **or** individual scholarship URLs, instead of sitemap discovery |
| `searchQuery` | string | — | Free-text filter, e.g. `nursing` or `first generation`. Every word must appear in the name, description, category, slug or criteria (the word "scholarship" is ignored). Also crawls matching category pages first |
| `openOnly` | boolean | `true` | Drop scholarships whose deadline has passed (rolling deadlines are always kept) |
| `minAwardAmount` | integer | — | Minimum single-award size in USD |
| `deadlineAfter` | string | — | Only deadlines on/after this date (`YYYY-MM-DD`) |
| `deadlineBefore` | string | — | Only deadlines on/before this date (`YYYY-MM-DD`) |
| `educationLevels` | array | — | `highschool`, `undergraduate`, `graduate` |
| `includeEssayPrompt` | boolean | `true` | Include the essay question(s) as plain text |

### Example input

```json
{
  "categoryTypes": ["by-major", "by-type"],
  "maxCategoryPages": 10,
  "maxResults": 200,
  "minAwardAmount": 1000,
  "deadlineBefore": "2026-12-31",
  "educationLevels": ["highschool"]
}
```

## Sample output

```json
{
  "name": "Pamela Branchini Memorial Scholarship",
  "slug": "pamela-branchini-memorial-scholarship",
  "url": "https://bold.org/scholarships/pamela-branchini-memorial-scholarship/",
  "description": "This scholarship seeks to honor the life of Pamela Branchini by supporting students who are pursuing degrees in the fine arts.",
  "category": "Arts",
  "deadline": "2026-11-05T23:59:59Z",
  "isRollingDeadline": false,
  "announcementDate": "2026-12-06T00:00:00.000Z",
  "awardAmount": 1000,
  "awardAmounts": [1000, 1000],
  "totalAwardAmount": 2000,
  "numberOfAwards": 2,
  "numberOfApplicants": 665,
  "applicantsPerAward": 332.5,
  "educationLevels": ["highSchool", "undergraduate", "graduate"],
  "acceptsHighSchool": true,
  "criteria": ["Ambition", "Need", "Boldest Bold.org Profile"],
  "requiresEssay": true,
  "essayTopic": "Tell us about a piece of art you made and what it means to you.",
  "essayMinLength": 400,
  "essayMaxLength": 600,
  "isMultiYear": false,
  "donorName": "Dan Branchini and the Glitter Team at Community Lutheran",
  "donorProfileUrl": "https://bold.org/profile/bruce-ewing/",
  "imageUrl": "https://static.bold.org/pamelabranchinimemorialscholarship....jpeg",
  "publishedAt": "2026-05-06T19:31:45.646Z",
  "updatedAt": "2026-09-10T00:40:38.001Z",
  "sourceUrl": "https://bold.org/scholarships/by-major/art-scholarships/",
  "scrapedAt": "2026-09-10T10:21:03.552Z"
}
```

## FAQ

**Do I need a proxy or a browser?**
No. bold.org ships the full scholarship records inside the initial HTML response, so this Actor is plain HTTP — fast, cheap and it runs fine on the smallest memory setting.

**How many scholarships can I get?**
One category page yields about 30 complete records in a single request, and there are 500+ category pages across the five category families. Raise `maxCategoryPages` and `maxResults` together; results are de-duplicated by scholarship ID across categories, so overlapping categories never bill you twice for the same scholarship.

**Why did I get fewer rows than `maxResults`?**
Either the crawl ran out of category pages (raise `maxCategoryPages`), or your filters removed them. The log prints how many records were found and how many survived filtering on every page. Filtered-out records are not charged.

**What is `applicantsPerAward`?**
`numberOfApplicants / numberOfAwards`, rounded to one decimal — bold.org publishes the live applicant count, so this is a real competitiveness signal, not an estimate. It is `null` when either number is unavailable.

**Is the data live?**
Yes, each run fetches the pages fresh. `updatedAt` is bold.org's own last-modified timestamp for the scholarship, and `scrapedAt` is when we read it.

**Is this allowed?**
Only public pages are read, and only paths that bold.org's `robots.txt` permits — it disallows query-string URLs (`Disallow: /*?*`), so this Actor never requests one. No login, no personal data about applicants: the applicant *count* is a public number on the listing page.

**How does this compare to other bold.org scrapers?**
Depth. This Actor returns ~28 typed fields per scholarship — including `numberOfAwards`, `numberOfApplicants`, `applicantsPerAward`, the essay prompt(s), judging criteria and donor — versus the 11 fields typical of other bold.org Actors, where `amount` is usually a plain string with no award-count or applicant data at all. All four filters (`searchQuery`, `minAwardAmount`, `deadlineAfter`/`deadlineBefore`, `educationLevels`) are verified against real runs: each one measurably changes which rows come back, not just a passthrough flag.

**Can I scrape one specific scholarship?**
Yes — put its page URL in `startUrls`, e.g. `https://bold.org/scholarships/chris-jackson-scholarship/`.
