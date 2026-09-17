# App Store Reviews Scraper (Apple)

Get customer reviews for any iOS / macOS app from the Apple App Store, for any country storefront, as JSON, CSV or Excel. Each review includes rating, title, text, app version, author and date, plus optional app metadata (name, developer, average rating, rating count) and the **full per-star ratings breakdown** — how many 1★, 2★, 3★, 4★ and 5★ ratings the app has in that storefront. Pay only per review returned.

## Use cases
- Product research and competitor analysis across countries
- Sentiment analysis, feature-request mining, churn reasons
- Monitoring your own app's newest reviews on a schedule
- Feeding reviews into AI agents and dashboards
- **Alerting on new reviews only** — set `watchLabel` and schedule it; see [Watch mode](#watch-mode--only-new-reviews-since-the-last-run) below

## Input
| Field | Type | Description |
|---|---|---|
| `apps` | array | App Store URLs or numeric app IDs |
| `appNames` | array | Free-text app names (e.g. `"Notion"`) — auto-resolved to an app id via Apple's own search API. See caveat below. |
| `includeMacApps` | boolean | Also search the **Mac App Store** when resolving `appNames` (default `false`). Apple's app-name search is iOS-only, so Mac-only apps are invisible without it — see below. |
| `countries` | array | Storefront codes, e.g. `us`, `gb`, `de`, `jp`, `br` (default `us`) |
| `countryFallback` | boolean | If a storefront returns nothing, pull that app's reviews from one that works (default `false`) |
| `sort` | string | `mostRecent` (default) or `mostHelpful` |
| `maxReviewsPerApp` | integer | Up to 500 per app per country (Apple's limit) — counted before minRating/maxRating/keyword filtering, see FAQ |
| `includeAppInfo` | boolean | Attach app name, developer, average rating, rating count and the per-star `ratingBreakdown` (default `true`) |
| `maxResults` | integer | Total cap |
| `minRating` / `maxRating` | integer | Only keep reviews with a star rating in this range (1-5) |
| `keyword` | string | Only keep reviews whose title or content contains this word/phrase (case-insensitive) |
| `reviewsAfter` | string (ISO date) | Only keep reviews posted on or after this date. Forces `sort` to `mostRecent` and stops paging as soon as older reviews are reached, so a narrow window doesn't scan (and isn't charged for) pages you don't want. |
| `watchLabel` | string | Turns this run into a [watch](#watch-mode--only-new-reviews-since-the-last-run) — only reviews posted since the last run under this label are returned and charged. Leave empty for normal runs. |

Filtering happens before you're charged — you never pay for rows that got filtered out.

## Watch mode — only new reviews since the last run
Set `watchLabel` to any name and this Actor stops re-delivering the same reviews on every scheduled run:

1. **First run for a label is a free baseline.** It records which reviews already exist for every `apps`/`countries` pair (always walking Apple's full 500-review ceiling per pair, regardless of `maxReviewsPerApp`) and returns **zero rows — you are charged nothing**.
2. **Every run after that returns only reviews that weren't in the baseline**, and adds them to it. Nothing new → zero rows → zero charge.

The baseline lives in **your own** Apify account, in a named key-value store called `fetchsmith-app-store-reviews-watch`, keyed by your label plus a fingerprint of `apps`/`appNames`/`countries`/`countryFallback`/`sort` **and every minRating/maxRating/keyword/reviewsAfter filter** (Apple's feed takes none of those server-side, so all of them decide what "new" means). Change any of those and you get a fresh baseline rather than a silently wrong one. Delete the record to start over; use different labels to watch several filter sets in parallel.

Details worth knowing:
- **Use `sort: "mostRecent"`** (the default). `mostHelpful` isn't date-ordered, so a brand-new review isn't necessarily inside the scanned window and can be missed; the run logs a warning if you watch with `mostHelpful` anyway.
- **`maxReviewsPerApp` is your scan-depth budget on incremental runs and is left exactly as you set it** — with `mostRecent`, new reviews sort at the top, so your own cap doesn't hide them. If every matching review inside that window turned out to be new, the run warns you that reviews posted since the last run may sit further back — raise `maxReviewsPerApp` or run the watch more often.
- If an `appNames` search resolves to a *different* app than last time (or a new `countries` entry appears), that app/country pair is baselined on the spot rather than having its entire review history delivered as "new".
- `countryFallback` still applies during a watch — a baselined pair whose storefront later goes empty falls back the same way a normal run does.
- Reviews with no id Apple can hand back (rare) are skipped in watch mode, since they can't be recognized on the next run — never charged.

**`appNames` caveat, verified live:** Apple's search API almost never returns zero results — even keyboard-mash gibberish gets back an unrelated app (measured: nonsense strings matched an Arabic quiz game, an emoji trivia app, etc., every time). A naive "take the first hit" would silently resolve a typo'd name to the wrong app. This Actor only accepts a match that shares a real word with the requested name (in the app's name, developer, or bundle id); otherwise it skips the name with a "no match found" warning instead of guessing. Use a numeric app id or Store URL when you need certainty. Also note: if you pass `appNames` and leave `apps` untouched, the Actor deliberately ignores `apps`'s own example default rather than mixing an uninvited app into your results.

**Mac App Store apps (`includeMacApps`), verified live 2026-09-17:** Apple's name-search entity for apps is iOS-only. Searching `"Final Cut Pro"` by name returns Final Cut Camera, iMovie and CapCut — the actual Mac app is never in the list, so before this option a name lookup would quietly hand you a *different* app. With `"includeMacApps": true` the Mac App Store is searched too and an exact title match wins over a loose one, so `"Final Cut Pro"` resolves to id `424389933` and returns its real Mac reviews. Everything after resolution is platform-agnostic: **you never needed this option if you pass a numeric id or an `apps.apple.com` URL** — the review feed and the app-metadata lookup are keyed by app id, not by platform, and have always worked for Mac apps. It is off by default so that an existing iOS-only name lookup can't start matching a same-named Mac app.

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
  "reviewUrl": "https://itunes.apple.com/us/review?id=1232780281&type=Purple%20Software",
  "voteSum": 0,
  "voteCount": 0,
  "appName": "Notion: Notes, Docs, Tasks",
  "developer": "Notion Labs, Incorporated",
  "averageRating": 4.7,
  "ratingCount": 512345,
  "totalRatings": 519312,
  "ratingBreakdown": { "five": 432140, "four": 51220, "three": 15870, "two": 6190, "one": 13892 }
}
```

## Per-star ratings breakdown (`ratingBreakdown`)
An app's average rating hides the shape of its distribution: 4.5 stars from mostly 5s and a handful of 1s is a very different product story from 4.5 stars from a wall of 4s. Apple's public lookup API only gives you the average and the total, so most App Store review scrapers stop there. This Actor also returns the **actual count of ratings at each star level**, per storefront, on every row when `includeAppInfo` is on:

```json
"totalRatings": 29481802,
"ratingBreakdown": { "five": 25284650, "four": 2000235, "three": 696048, "two": 274710, "one": 1226159 }
```

- Counts are **ratings**, not reviews — they include the millions of users who tapped a star without writing anything, so `totalRatings` is far larger than the 500 reviews Apple's feed will hand you.
- The breakdown is **per storefront**, so `countries: ["us", "gb", "de"]` gives you three genuinely different distributions to compare.
- It costs nothing extra: it is fetched once per app/storefront alongside the app lookup, and you are only ever charged per review returned.
- It is verified before it is reported — if the numbers don't reconstruct Apple's own published average, the Actor omits the field and logs a warning rather than handing you a distribution that might be inverted.

Useful for a 1★-share trend line over releases, for weighting sentiment against how many silent raters actually sit behind a review, and for competitor comparisons where two apps show the same average.

## Pricing
`result` — charged per review returned. App lookups, empty pages and errors are free. HTTP-only and fast.

## Never silently returns an empty result
Apple's public review feed is full of holes. For one app in one storefront, page 1 can be empty while pages 2 and 7 return a full 50 reviews each; an app can be completely empty under `mostRecent` and have hundreds under `mostHelpful`; and coverage differs per storefront. Most scrapers stop at the first empty page and hand you an empty dataset with a green "succeeded" run. This one:

- **scans Apple's entire page range and skips over the empty pages** instead of treating the first one as the end of the reviews;
- if the sort order you asked for is empty, **retries under the other sort order** — same review pool, and every row records which one it came from in `sortUsed`;
- **re-requests an empty page as a different client** before believing it. Whether a page comes back empty depends on what your HTTP client looks like to Apple: measured on 2026-09-10, Notion/us `mostRecent` page 4 returned nothing to a plain `curl` request in 4 out of 4 interleaved rounds while a browser and an iPhone client both got a full 50 — the same 50. Each recovered page is 50 reviews a single-client scrape silently drops, and the retry only costs a request when a page is actually empty. Rows carry `clientClass` so you can see which client served them;
- when a storefront really is empty, probes other storefronts and **tells you which ones have reviews** for that app;
- with `countryFallback: true`, fetches from a working storefront automatically — rows keep the real `country` plus `requestedCountry` and `fallbackUsed: true`, so nothing is mislabelled;
- sets a run status message explaining *why* a run returned few or no rows (empty Apple feed vs. your own rating/keyword filters);
- **fails loudly instead of returning a misleading empty result when the fault is Apple's, not yours.** Apple sometimes serves an empty feed for *everything* — measured 2026-09-16: every app, storefront, page, sort and client came back `HTTP 200` with zero entries. From one app's response that is indistinguishable from "this app has no reviews", so when a run ends up with no reviews at all we re-check two control apps that always have hundreds of thousands of reviews (three attempts, spaced). If those are empty too, the run **fails** with a message naming the Apple-side fault, rather than telling you no reviews matched your filters. A watch-mode baseline is never written from such a run either — otherwise the next run would treat the app's whole review history as "new" and charge you for it.

You are never charged for empty pages, for retries, or for a run that fails this way.

## FAQ
**Why did my run return 0 reviews with status SUCCEEDED?** Check the run's status message first — it tells you whether Apple's feed was genuinely empty for that app/storefront or your own `minRating`/`maxRating`/`keyword` filters removed every row.
**Can I get more than 500 reviews for one app?** No — Apple's public feed caps at 500 most-recent reviews per app per country. Run on a schedule and deduplicate by `reviewId` to build a larger archive over time. Note that `totalRatings`/`ratingBreakdown` are **not** capped: they cover every rating the app has ever received in that storefront, so you still get the full-population distribution even though only 500 written reviews are reachable.
**Why is `totalRatings` different from `ratingCount`?** They come from two different Apple sources and are both real. `ratingCount` is Apple's lookup API figure; `totalRatings` is the sum of the per-star histogram shown on the App Store product page, which updates on a slightly different schedule. Expect them to agree to within a fraction of a percent — if you need the number that matches `ratingBreakdown` exactly, use `totalRatings`.
**Does `keyword` handle accented words correctly?** Yes, as of v0.1.29 — `keyword` and the review text it's matched against are Unicode-normalized before comparing, so an accented word (e.g. "café") matches regardless of which of Unicode's two equivalent representations (composed vs. decomposed) you typed it in.
**Is `reviewUrl` unique per review?** No, and it isn't presented as such. It's Apple's own "related" link from the feed entry, which points at the app's review page for that storefront — the same URL for every review of that app in that country. Apple does not publish a per-review permalink; use `reviewId` as the unique key.
**Does `countryFallback` change the `country` field on rows I already have?** No — fallback rows are clearly tagged with `fallbackUsed: true` and keep both the real `country` they came from and the `requestedCountry` you asked for.
**Do I get charged for empty pages or retries?** No — only reviews actually returned to the dataset are charged.
**Why did I get fewer reviews than `maxReviewsPerApp`?** `maxReviewsPerApp` is a **scan cap**, not a match count — it stops paging Apple's feed after that many reviews have been looked at, and `minRating`/`maxRating`/`keyword` are applied *after* that, per review. A narrow filter combined with a low cap can miss real matches sitting deeper in the feed: on Spotify (`324684580`) with `maxRating: 1`, `maxReviewsPerApp: 5` scans 5 reviews and keeps 0, but raising it to `100` finds 12 — the matches were always there, just unscanned. When this happens the log carries a `WARN` naming the cap and how many scanned reviews were dropped, and the run's status message says the same — raise `maxReviewsPerApp` to search deeper. Filtered-out reviews are **not** charged either way.

## Notes
Apple exposes the most recent 500 reviews per app per country. For historical archives, run on a schedule and deduplicate by `reviewId`.

## Related guides
Engineering write-ups behind this Actor:
- [Apple's review feed has holes, and whether you hit one depends on your HTTP client](https://fetchsmith.com/blog/apple-app-store-reviews-header-fingerprint)
- [The App Store's per-star ratings breakdown isn't in any of Apple's APIs — it's in the page's JSON blob](https://fetchsmith.com/blog/app-store-per-star-ratings-breakdown)
- [Four ways an invisible character makes a scraper return zero rows](https://fetchsmith.com/blog/invisible-characters-return-zero-rows)

Only publicly available data is collected. Support: support@fetchsmith.com · Hosted API: https://fetchsmith.com/tools/app-store-reviews-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/app-store-reviews-scraper
