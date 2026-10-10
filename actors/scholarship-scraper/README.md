# Scholarship Scraper (bold.org)

> ### ⚠️ Known issue — temporarily unable to return data (since 2026-09-20; still blocked at the last check, 2026-10-10)
>
> bold.org has switched its entire site to Vercel's **"Security Checkpoint"** bot protection, which
> answers every non-browser request with HTTP 429 and a JavaScript challenge page — including
> `robots.txt` and `sitemap.xml`. It is a browser JavaScript proof-of-work, not an IP-reputation
> block: we get the byte-identical challenge from six independent networks, including datacenter
> **and residential** proxy exits, so no input, proxy or retry setting works around it.
>
> **Runs fail immediately with that explanation and cost you nothing** — this Actor bills per
> scholarship returned, and a blocked run returns none. We re-check the site every night and will
> remove this notice the moment it clears. Everything documented below is unchanged and works as
> soon as bold.org is reachable again.

Scrape **scholarship listings from bold.org** — the largest single scholarship platform — into JSON, CSV or Excel. No login, no browser, no proxy.

Every row is a complete scholarship: award amount, number of awards, deadline, essay prompt, judging criteria, education levels, donor, and the **number of people who have already applied** — plus a computed `applicantsPerAward` ratio so you can see at a glance which awards are actually winnable.

**Pay per result: $0.00035 per scholarship. No start fee** — a run that returns nothing costs nothing, and scholarships removed by your filters are never charged.

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
  "featured": false,
  "donorName": "Dan Branchini and the Glitter Team at Community Lutheran",
  "donorProfileUrl": "https://bold.org/profile/bruce-ewing/",
  "donorVerified": false,
  "imageUrl": "https://static.bold.org/pamelabranchinimemorialscholarship....jpeg",
  "winnersCount": 0,
  "publishedAt": "2026-05-06T19:31:45.646Z",
  "updatedAt": "2026-09-10T00:40:38.001Z",
  "sourceUrl": "https://bold.org/scholarships/by-major/art-scholarships/",
  "scrapedAt": "2026-09-10T10:21:03.552Z"
}
```

## Pricing
Pay per result: **$0.00035 per scholarship, no start fee** — a run that returns nothing costs nothing, and scholarships removed by your filters are never charged.

**Pricing verified live 2026-10-04** against the whole niche, not just one rival: an 11-term Store sweep for "scholarship" surfaces 23 comparable listings. The one direct bold.org competitor, `jungle_synthesizer/bold-org-scholarship-database-scraper` (3 users, dormant — 0 new users in 30 days), charges a **$0.10 Actor-start fee plus $0.001 per record** — 2.9x our per-row rate before the start fee is even added, so we are cheaper at every run size and from the first row. Its 10-field output (name, amount, deadline, education level, field of study, eligibility summary, category, sponsor, applicant count, no-essay flag) matches the "about 11 fields, no essay text" shape described above — it does not carry judging criteria, `numberOfAwards`, `applicantsPerAward`, `donorVerified` or `winnersCount`.

The niche's biggest generic scholarship scraper, `majestic_fund/the-scholarship-scraper-actor` (71 users, 7 new in the last 30 days — the most active listing we found), **ties our exact $0.00035 per-record rate but adds a $0.0005 Actor-start fee** on top, so we are cheaper on every run regardless of size. It scrapes "multiple scholarship databases and platforms" per its own listing; we could not confirm bold.org is one of them, so treat it as a possible substitute, not a verified bold.org alternative.

**What we do not claim:** we are not the cheapest listing in the scholarship niche. `fiery_dream/scholarship-intel` (39 users) charges $0.00005 Actor-start plus **$0.00001 per result** — about 35x cheaper than our rate, undercutting us from the first row (a 100-row pull costs roughly $0.0011 there against $0.035 here). It is a student-facing scholarship *matcher*, not a bold.org feed: its inputs are GPA, degree level, field of study and first-generation status, it is not scoped to bold.org or any single site, and it cannot return bold.org's per-listing depth (essay prompt text, judging criteria, `applicantsPerAward`, donor fields). Price-shop on the feature list and the site you actually need, not the headline rate alone.

**Re-verified live 2026-10-04 to check for new entrants since the last audit:** the same 11-term sweep now returns 23 matching listings out of 31 seen (up 1 from the last audit, noise-level) — and all three rivals named in this section re-verified with zero price drift. `rhapsodic_groundhopper/buildher-compass-opportunity-intelligence` (6 users, 0 new in 30 days) collects internships, fellowships, scholarships, bootcamps and hackathons for African women in tech from unspecified public sources. Checked and deliberately left unnamed: it is a demographic-targeted, multi-category opportunity feed, not a bold.org-specific scholarship scraper, and its own primary charge event bills **$0.2 per extracted item** plus a $0.00005 start fee — roughly 570x our per-row rate — so it would not be a price concern even if it were in scope.

**Also found, scoped to other scholarship sites, not bold.org — 9 single-site scrapers in total, all verified live 2026-10-04, all pricier than us at every tier:** `parseforge/niche-scholarships-scraper` (3 users) scrapes Niche.com at a tiered **$0.004 (Free) → $0.00362 (Diamond) per result** plus a $0.02→$0.0178 start fee (11x–50x our rate). `dadhalfdev/scholarshipportal-scraper` (3 users, ScholarshipPortal.com/Studyportals), `dadhalfdev/scholarships-com-scraper` (3 users, Scholarships.com) and `dadhalfdev/fastweb-scraper` (2 users, Fastweb.com) each tier from **$0.003 (Free) down to $0.0015 (Gold+)** plus a flat $0.00005 start fee (4x–8.5x our rate). `dadhalfdev/scholarshipsads-scraper` (2 users, ScholarshipsAds.com) tiers **$0.005 → $0.003** plus the same $0.00005 start fee (8.5x–14x). `jungle_synthesizer/unigo-scholarship-match-scraper` (2 users, Unigo.com) tiers **$0.003 → $0.0024** plus a $0.0001 start fee (6.8x–8.5x). `jungle_synthesizer/scholarships-com-directory-scraper` (2 users) and `jungle_synthesizer/collegescholarships-org-directory-scraper` (1 user, down from 2 — re-verified live 2026-10-06), for Scholarships.com and CollegeScholarships.org, tier **$0.001 → $0.0008** plus a $0.10 start fee (2.3x–2.9x, the closest of the nine, but still dearer from the first row once the start fee is counted). **New at cycle 1234:** `parseforge/college-board-scholarship-search-scraper` (2 users, College Board BigFuture) tiers **$0.006 (Free) → $0.00543 (Gold+)** per result with no separate start fee (15.5x–17x our rate) — found as the one unnamed listing left in the niche's full 23-match sweep (previously invisible to the top-10-by-users table at only 2 users). None of these nine is a bold.org substitute — each reads a different source site entirely — but all nine confirm that no scholarship-specific scraper found in this niche, for any site, undercuts our per-row price.

**Checked and left out of scope (not scholarship-specific), verified live 2026-10-04:** three Unstop.com opportunity scrapers surfaced by this niche's keyword sweep are bigger by users than any rival named above — `solidcode/unstop-scraper` (96 users), `parsebird/unstop-jobs-internships-scraper` (52 users) and `dami_studio/unstop-scraper` (33 users), plus a smaller fourth, `memo23/unstop-jobs-internships-scraper` (2 users) — but all four scrape Unstop's full mix of hackathons, competitions, jobs, internships, quizzes, workshops and conferences, where scholarships are only one of eight listing types rather than a dedicated feed, and their per-opportunity pricing bundles all eight types together, so there is no clean per-scholarship rate to compare. `saadithya/scholarships-competitions-internships-extractor` (19 users) is similarly multi-category (11 RSS feed categories spanning scholarships, competitions, internships and challenges) and charges a flat $0.05 per category per run rather than per row. Four more 1-2-user listings are false matches on the bare word "scholarship", not scholarship data products at all: `jungle_synthesizer/top-law-schools-tls-forum-scraper` scrapes law-school admissions forum *discussion threads* (some about scholarship negotiation, not listings); `bstandco/france-parcoursup-programs` scrapes French university program data where "scholarships" is one applicant-profile field among many; `maryse_gahou/africa-opportuscan` and `dabooti/grant-scholarship-monitor` are vague, single/near-zero-user "configurable sources" opportunity monitors with no bold.org-comparable depth; `lovablelynx/opportunity-radar` (1 user) is a thin scholarship-matching tool, same non-substitute class as `fiery_dream/scholarship-intel` above but with no users yet to warrant naming on price.

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
Depth. This Actor returns 32 typed fields per scholarship — including `numberOfAwards`, `numberOfApplicants`, `applicantsPerAward`, the essay prompt(s), judging criteria, donor (with `donorVerified`) and `winnersCount` — versus the 11 fields typical of other bold.org Actors, where `amount` is usually a plain string with no award-count or applicant data at all. All four filters (`searchQuery`, `minAwardAmount`, `deadlineAfter`/`deadlineBefore`, `educationLevels`) are verified against real runs: each one measurably changes which rows come back, not just a passthrough flag.

**Can I scrape one specific scholarship?**
Yes — put its page URL in `startUrls`, e.g. `https://bold.org/scholarships/chris-jackson-scholarship/`.

**Does `searchQuery` handle accented names correctly?**
Yes. A name like `José` or `María` is kept as one search token instead of being split on the accented letter — matters if you're searching a scholarship named after a person.

## Related guides
Engineering write-ups behind this Actor:
- [Next.js App Router ships your whole database table in the HTML — bold.org's RSC flight stream, decoded](https://fetchsmith.com/blog/bold-org-nextjs-rsc-scholarship-data)
- [Four ways an invisible character makes a scraper return zero rows](https://fetchsmith.com/blog/invisible-characters-return-zero-rows)

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools)

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/scholarship-scraper
