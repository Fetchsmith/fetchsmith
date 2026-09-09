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
| `sort` | string | `mostRecent` (default) or `mostHelpful` |
| `maxReviewsPerApp` | integer | Up to 500 per app per country (Apple's limit) |
| `includeAppInfo` | boolean | Attach app name, developer, average rating and rating count |
| `maxResults` | integer | Total cap |

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

## Notes
Apple exposes the most recent 500 reviews per app per country. For historical archives, run on a schedule and deduplicate by `reviewId`. Only publicly available data is collected. Support: support@fetchsmith.com · Hosted API: https://fetchsmith.com/tools/app-store-reviews-scraper
