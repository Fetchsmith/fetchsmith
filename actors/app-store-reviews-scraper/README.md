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
| `appNames` | array | Free-text app names (e.g. `"Notion"`) — auto-resolved to an app id via Apple's own search API. See caveat below. |
| `countries` | array | Storefront codes, e.g. `us`, `gb`, `de`, `jp`, `br` (default `us`) |
| `countryFallback` | boolean | If a storefront returns nothing, pull that app's reviews from one that works (default `false`) |
| `sort` | string | `mostRecent` (default) or `mostHelpful` |
| `maxReviewsPerApp` | integer | Up to 500 per app per country (Apple's limit) |
| `includeAppInfo` | boolean | Attach app name, developer, average rating and rating count |
| `maxResults` | integer | Total cap |
| `minRating` / `maxRating` | integer | Only keep reviews with a star rating in this range (1-5) |
| `keyword` | string | Only keep reviews whose title or content contains this word/phrase (case-insensitive) |
| `reviewsAfter` | string (ISO date) | Only keep reviews posted on or after this date. Forces `sort` to `mostRecent` and stops paging as soon as older reviews are reached, so a narrow window doesn't scan (and isn't charged for) pages you don't want. |

Filtering happens before you're charged — you never pay for rows that got filtered out.

**`appNames` caveat, verified live:** Apple's search API almost never returns zero results — even keyboard-mash gibberish gets back an unrelated app (measured: nonsense strings matched an Arabic quiz game, an emoji trivia app, etc., every time). A naive "take the first hit" would silently resolve a typo'd name to the wrong app. This Actor only accepts a match that shares a real word with the requested name (in the app's name, developer, or bundle id); otherwise it skips the name with a "no match found" warning instead of guessing. Use a numeric app id or Store URL when you need certainty. Also note: if you pass `appNames` and leave `apps` untouched, the Actor deliberately ignores `apps`'s own example default rather than mixing an uninvited app into your results.

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
Apple's public review feed is full of holes. For one app in one storefront, page 1 can be empty while pages 2 and 7 return a full 50 reviews each; an app can be completely empty under `mostRecent` and have hundreds under `mostHelpful`; and coverage differs per storefront. Most scrapers stop at the first empty page and hand you an empty dataset with a green "succeeded" run. This one:

- **scans Apple's entire page range and skips over the empty pages** instead of treating the first one as the end of the reviews;
- if the sort order you asked for is empty, **retries under the other sort order** — same review pool, and every row records which one it came from in `sortUsed`;
- **re-requests an empty page as a different client** before believing it. Whether a page comes back empty depends on what your HTTP client looks like to Apple: measured on 2026-09-10, Notion/us `mostRecent` page 4 returned nothing to a plain `curl` request in 4 out of 4 interleaved rounds while a browser and an iPhone client both got a full 50 — the same 50. Each recovered page is 50 reviews a single-client scrape silently drops, and the retry only costs a request when a page is actually empty. Rows carry `clientClass` so you can see which client served them;
- when a storefront really is empty, probes other storefronts and **tells you which ones have reviews** for that app;
- with `countryFallback: true`, fetches from a working storefront automatically — rows keep the real `country` plus `requestedCountry` and `fallbackUsed: true`, so nothing is mislabelled;
- sets a run status message explaining *why* a run returned few or no rows (empty Apple feed vs. your own rating/keyword filters).

You are never charged for empty pages or for retries.

## FAQ
**Why did my run return 0 reviews with status SUCCEEDED?** Check the run's status message first — it tells you whether Apple's feed was genuinely empty for that app/storefront or your own `minRating`/`maxRating`/`keyword` filters removed every row.
**Can I get more than 500 reviews for one app?** No — Apple's public feed caps at 500 most-recent reviews per app per country. Run on a schedule and deduplicate by `reviewId` to build a larger archive over time.
**Does `countryFallback` change the `country` field on rows I already have?** No — fallback rows are clearly tagged with `fallbackUsed: true` and keep both the real `country` they came from and the `requestedCountry` you asked for.
**Do I get charged for empty pages or retries?** No — only reviews actually returned to the dataset are charged.

## Notes
Apple exposes the most recent 500 reviews per app per country. For historical archives, run on a schedule and deduplicate by `reviewId`. ## Related guides
Engineering write-ups behind this Actor:
- [Apple's review feed has holes, and whether you hit one depends on your HTTP client](https://fetchsmith.com/blog/apple-app-store-reviews-header-fingerprint)

Only publicly available data is collected. Support: support@fetchsmith.com · Hosted API: https://fetchsmith.com/tools/app-store-reviews-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/app-store-reviews-scraper
