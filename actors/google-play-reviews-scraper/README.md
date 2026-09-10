# Google Play Reviews Scraper

Get Google Play app reviews and app details (ratings, installs, developer info) by app ID or search term. HTTP-only (no browser), so runs are fast and cheap, and you're charged only for the rows you actually get.

## What it does
- Fetches reviews for one or more Google Play apps, plus an optional app-details record (title, developer, score, installs, price, description, rating histogram).
- Accepts either exact `appIds` (package names, e.g. `com.spotify.music`) or `searchTerms` — the top matching app for each term is resolved automatically.
- Supports country/language targeting and sort order (newest / rating / helpfulness).
- Filter server-side by star rating, keyword, or date range — so you're only charged for reviews you actually want, not the whole feed.

## Input
| Field | Type | Description |
|---|---|---|
| `appIds` | array of strings | Google Play package names, e.g. `com.spotify.music` (from the app's Play Store URL `?id=` param) |
| `searchTerms` | array of strings | Alternative to `appIds`: search terms; the top match for each is used |
| `country` | string | Play Store country code (default `us`) |
| `language` | string | Language for reviews/details (default `en`) |
| `sort` | string | `NEWEST` (default), `RATING`, or `HELPFULNESS` |
| `maxReviewsPerApp` | integer | Stop after this many reviews per app (default 100) |
| `includeAppDetails` | boolean | Also push one app-details record per app (default true) |
| `maxResults` | integer | Hard cap across all apps and records (default 500) |
| `minScore` / `maxScore` | integer | Only keep reviews with a star rating in this range (1-5) |
| `keyword` | string | Only keep reviews whose title or text contains this word/phrase (case-insensitive) |
| `sinceDate` / `untilDate` | string | Only keep reviews posted within this ISO date range |

## Output
One item per row, either an app-details record (`recordType: "app"`) or a review (`recordType: "review"`).

Sample review row:
```json
{
  "recordType": "review",
  "appId": "com.spotify.music",
  "reviewId": "24191734-8bd7-4aac-a714-46193c46b4d4",
  "userName": "Nikhil Rathod",
  "reviewerProfileImageUrl": "https://play-lh.googleusercontent.com/a-/...",
  "score": 5,
  "title": null,
  "text": "my motivation",
  "date": "2026-09-08T03:01:35.135Z",
  "language": "en",
  "thumbsUp": 0,
  "version": null,
  "replyText": null,
  "replyDate": null,
  "url": "https://play.google.com/store/apps/details?id=com.spotify.music&reviewId=..."
}
```

Sample app-details row includes: `title`, `developer`, `score`, `ratings`, `reviewsCount`, `histogram`, `installs`, `price`, `free`, `genre`, `contentRating`, `released`, `updated`, `url`.

## Pricing
`result` — $0.0001 per returned item (review or app-details row). The run start is free. Matches the two largest real-usage competitors' flat rate (`thewolves` 1440 users, `theagents` 603 users, both $0.0001/review no start fee) — cheaper than `neatrat`'s (2583 users) tiered $0.00015 FREE-tier rate too.

## FAQ
**Can I get reviews in a specific country or language?** Yes, set `country` and `language` (Play Store returns different review sets per locale — run the Actor for each locale you need).
**Can I search by app name instead of package ID?** Yes, use `searchTerms`; the top matching app is resolved automatically.
**Why did I get fewer reviews than the app's total rating count?** Google Play's review API only returns a subset of written reviews, not every rating — this is a platform limitation, not a bug.
**Can I filter to just negative or just recent reviews?** Yes — set `maxScore` (e.g. 2) for negative-only, or `sinceDate`/`untilDate` for a date window; filtering happens before you're charged, so you never pay for rows you filtered out.

## Related guides
Engineering write-ups behind this Actor:
- [HTTP-only vs headless browser scraping: a timed benchmark](https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost)

## Notes
Only public Google Play data is collected. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com/tools/google-play-reviews-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/google-play-reviews-scraper
