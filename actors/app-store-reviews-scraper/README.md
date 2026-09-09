# App Store Reviews Scraper (Apple)

Get customer reviews for any iOS / macOS app from the Apple App Store, for any country storefront, as JSON, CSV or Excel. Each review includes rating, title, text, app version, author and date, plus optional app metadata (name, developer, average rating, rating count). Pay only per review returned.

## Use cases
- Product research and competitor analysis across countries
- Sentiment analysis, feature-request mining, churn reasons
- Monitoring your own app's newest reviews on a schedule
- Feeding reviews into AI agents and dashboards

## Input
| Field | Type | Description |
|---|---|---|
| `apps` | array | App Store URLs or numeric app IDs |
| `countries` | array | Storefront codes, e.g. `us`, `gb`, `de`, `jp`, `br` (default `us`) |
| `countryFallback` | boolean | If a storefront returns nothing, pull that app's reviews from one that works (default `false`) |
| `sort` | string | `mostRecent` (default) or `mostHelpful` |
| `maxReviewsPerApp` | integer | Up to 500 per app per country (Apple's limit) |
| `includeAppInfo` | boolean | Attach app name, developer, average rating and rating count |
| `maxResults` | integer | Total cap |
| `minRating` / `maxRating` | integer | Only keep reviews with a star rating in this range (1-5) |
| `keyword` | string | Only keep reviews whose title or content contains this word/phrase (case-insensitive) |

Filtering happens before you're charged — you never pay for rows that got filtered out.

## Output (one item per review)
```json
{
  "reviewId": "14523209599",
  "appId": "1232780281",
  "country": "us",
  "title": "Great for planning",
  "content": "I use it every day for ...",
  "rating": 5,
  "version": "3.42.0",
  "author": "jane_doe",
  "authorUrl": "https://itunes.apple.com/us/reviews/id...",
  "updatedAt": "2026-09-07T16:13:22-07:00",
  "voteSum": 0,
  "voteCount": 0,
  "appName": "Notion: Notes, Docs, Tasks",
  "developer": "Notion Labs, Incorporated",
  "averageRating": 4.7,
  "ratingCount": 512345
}
```

## Pricing
`result` — charged per review returned. App lookups, empty pages and errors are free. HTTP-only and fast.

## Never silently returns an empty result
Apple's public review feed is inconsistent: for the same app the same URL returns a full page of reviews on one request and an empty feed on the next, and coverage differs per storefront. Most scrapers hand you an empty dataset and a green "succeeded" run. This one:

- retries each empty page under several request fingerprints before believing there are no reviews;
- when a storefront really is empty, probes other storefronts and **tells you which ones have reviews** for that app;
- with `countryFallback: true`, fetches from a working storefront automatically — rows keep the real `country` plus `requestedCountry` and `fallbackUsed: true`, so nothing is mislabelled;
- sets a run status message explaining *why* a run returned few or no rows (empty Apple feed vs. your own rating/keyword filters).

You are never charged for empty pages or for retries.

## Notes
Apple exposes the most recent 500 reviews per app per country. For historical archives, run on a schedule and deduplicate by `reviewId`. Only publicly available data is collected. Support: support@fetchsmith.com · Hosted API: https://fetchsmith.com/tools/app-store-reviews-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/app-store-reviews-scraper
