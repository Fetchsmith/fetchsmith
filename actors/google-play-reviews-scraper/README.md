# Google Play Reviews Scraper

Get Google Play app reviews and app details (ratings, installs, developer info) by app ID or search term. HTTP-only (no browser), so runs are fast and cheap, and you're charged only for the rows you actually get.

## What it does
- Fetches reviews for one or more Google Play apps, plus an optional app-details record (title, developer, score, installs, price, description, rating histogram).
- Accepts package names (`com.spotify.music`), **full Play Store URLs** (paste the link straight from your browser), or `searchTerms` — the top matching app for each term is resolved automatically.
- Supports country/language targeting and sort order (newest / rating / helpfulness).
- Filter server-side by star rating (range **or** an exact set like 1★+5★), keyword(s), app version, or date range — so you're only charged for reviews you actually want, not the whole feed.
- Reviews are de-duplicated by `reviewId`, so a repeated row from Google Play is never pushed — or charged for — twice.
- **Watch mode** (`watchLabel`): run it on a schedule and get only the reviews posted *since your last run* instead of the same top-of-feed rows every time — a run with nothing new returns nothing and costs nothing.
- Includes per-review **aspect ratings** (`aspectRatings`) — the sub-scores Google Play attaches to a written review for specific aspects (e.g. ad frequency, ease of use) when the reviewer filled them in. None of the leading Store competitors expose this field (re-verified against their live output schemas 2026-09-17).

## Input
| Field | Type | Description |
|---|---|---|
| `appIds` | array of strings | Google Play package names (e.g. `com.spotify.music`) **or** full Play Store URLs (e.g. `https://play.google.com/store/apps/details?id=com.spotify.music`) — the package name is extracted from the URL's `?id=` param |
| `searchTerms` | array of strings | Alternative to `appIds`: search terms; the top match for each is used |
| `country` | string | Play Store country code (default `us`) |
| `language` | string | Language for reviews/details (default `en`) |
| `sort` | string | `NEWEST` (default), `RATING`, or `HELPFULNESS` |
| `maxReviewsPerApp` | integer | Reviews to *fetch* per app before moving to the next one (default 100, max 5000) — counted before rating/keyword/appVersion/date filtering, see FAQ |
| `includeAppDetails` | boolean | Also push one app-details record per app (default true) |
| `maxResults` | integer | Hard cap across all apps and records (default 500) |
| `minScore` / `maxScore` | integer | Only keep reviews with a star rating in this range (1-5) |
| `ratingFilter` | array of integers | Only keep reviews whose rating is one of these exact values, e.g. `[1, 5]` — use it when you want a non-contiguous set that `minScore`/`maxScore` can't express |
| `keyword` | string | Only keep reviews whose title or text contains this word/phrase (case-insensitive) |
| `keywords` | array of strings | Only keep reviews containing **at least one** of these words/phrases (case-insensitive) |
| `appVersions` | array of strings | Only keep reviews written against one of these app versions, e.g. `["9.1.78.2218"]`. Google Play leaves `version` null on roughly 1 review in 6 — those are dropped when this filter is set |
| `minThumbsUp` | integer | Only keep reviews with at least this many "helpful" votes from other users |
| `replyFilter` | string | `any` (default), `hasReply` (only reviews the developer already responded to), or `noReply` (only reviews still waiting for a response — the support-queue use case) |
| `minReviewLength` | integer | Only keep reviews whose text is at least this many characters — filters out one-word/emoji-only reviews |
| `sinceDate` / `untilDate` | string | Only keep reviews posted within this ISO date range |
| `watchLabel` | string | Optional. Name a saved watch (e.g. `my-app-alerts`) to get **only reviews not delivered under that label before** — see "Watch mode" below |
| `webhookUrl` | string | Optional. An http(s) URL to POST a small JSON completion summary to when the run finishes — see FAQ. |

## Watch mode — only new reviews since the last run
Set `watchLabel` to any name and this Actor stops re-delivering the same reviews on every scheduled run:

1. **First run for a label is a free baseline.** It records which reviews already exist (walking at least 1000 per app, regardless of your `maxReviewsPerApp`, up to 5000 reviews total) and returns **zero rows — you are charged nothing**.
2. **Every run after that returns only reviews that weren't in the baseline**, and adds them to it. Nothing new → zero rows → zero charge.

The baseline lives in **your own** Apify account, in a named key-value store called `fetchsmith-google-play-reviews-watch`, keyed by your label plus a fingerprint of the apps/search terms, country, language, sort order **and every rating, keyword, app-version, thumbs-up, reply and date filter**. Change any of those and you get a fresh baseline rather than a silently wrong one — otherwise widening a filter would hide the newly-matching older reviews as "already seen". Delete the record to start over; use different labels to watch several filter sets in parallel.

Details worth knowing:
- **Use `sort: "NEWEST"`** (the default). With `RATING` or `HELPFULNESS` a brand-new review isn't necessarily inside the first `maxReviewsPerApp` rows, so new reviews can be missed; the run logs a warning if you do it anyway.
- **`maxReviewsPerApp` is your fetch-depth budget on incremental runs and is left exactly as you set it.** If every matching review inside that window turned out to be new, the run warns you (and says so in the status message) that reviews posted before the window may have been missed — raise `maxReviewsPerApp` or run the watch more often.
- **App-details records are only returned on a run where that app actually has a new review**, so a quiet run really does cost nothing. On non-watch runs they behave as before.
- If a `searchTerms` lookup resolves to a *different* app than last time, that app is baselined on the spot rather than having its entire back catalogue delivered as "new".
- **Baseline size cap.** The saved record holds at most 20,000 review ids; once a long-running label grows past that, the oldest ids fall off and those reviews would be reported (and charged) as "new" again on a later run. The run now says so explicitly — a `WARNING` in the log, in the run's status message, and `baselineTruncated`/`baselineTruncatedTotal` in the `webhookUrl` payload and the saved record (`truncatedLastRun`/`truncatedTotal`) — so you can narrow the filters or split the apps across labels before it costs you anything.

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
  "aspectRatings": [
    { "criteria": "vaf_app_quality_ads_frequency", "rating": 2 }
  ],
  "url": "https://play.google.com/store/apps/details?id=com.spotify.music&reviewId=..."
}
```

Sample app-details row includes: `title`, `developer`, `score`, `ratings`, `reviewsCount`, `histogram`, `installs`, `price`, `free`, `genre`, `contentRating`, `released`, `updated`, `url`.

## Pricing
`result` — $0.0001 per returned item (review or app-details row). The run start is free. Matches the two largest real-usage competitors' flat rate (`thewolves` and `theagents`, both $0.0001/review, no start fee) and undercuts the niche's biggest listing by users, `neatrat`, whose tiered price starts at $0.00015/review on the free plan. Re-verified against their live pricing 2026-09-17.

## FAQ
**Can I get reviews in a specific country or language?** Yes, set `country` and `language` (Play Store returns different review sets per locale — run the Actor for each locale you need).
**Can I search by app name instead of package ID?** Yes, use `searchTerms`; the top matching app is resolved automatically.
**Why did I get fewer reviews than the app's total rating count?** Google Play's review API only returns a subset of written reviews, not every rating — this is a platform limitation, not a bug.
**Does `keyword`/`keywords` handle accented words correctly?** Yes, as of v0.1.20 — both fields and the review text they're matched against are Unicode-normalized before comparing, so an accented word (e.g. "café") matches regardless of which of Unicode's two equivalent representations (composed vs. decomposed) you typed it in.
**Can I filter to just negative or just recent reviews?** Yes — set `maxScore` (e.g. 2) for negative-only, `ratingFilter: [1, 5]` for only the extremes, or `sinceDate`/`untilDate` for a date window; filtering happens before you're charged, so you never pay for rows you filtered out.

**Can I see what broke in a specific release?** Set `appVersions` to the version string(s) you care about (they match the `version` field on each review row) and, if you want, combine it with `maxScore: 2` and `keywords` to isolate the complaints. Reviews where Google Play reports no version are excluded rather than guessed at.

**Can I find reviews my support team hasn't answered yet, or check response quality on the ones we have?** Yes — `replyFilter: "noReply"` returns only reviews with no developer response (combine with `maxScore: 2` for an unanswered-complaints queue); `replyFilter: "hasReply"` returns only the ones you already responded to, e.g. to audit response quality or turnaround. `minThumbsUp` and `minReviewLength` are the same idea applied to helpfulness votes and review length — e.g. `minThumbsUp: 5` surfaces the reviews other users found worth upvoting, and `minReviewLength: 100` filters out one-word/emoji-only noise. All three were already computed on every review row (`thumbsUp`, `replyText`, `text`) but unfilterable before this — live-verified on a real app (Discord) that 21/50 recent reviews had a developer reply and the other 29 didn't, split exactly by `replyFilter`.

**What is `aspectRatings`?** Google Play sometimes prompts a reviewer to rate specific aspects of the app (e.g. "Ads frequency", "Ease of use") alongside their overall star score. When present, each row's `aspectRatings` array has one `{criteria, rating}` entry per aspect the reviewer answered — verified live: ~30% of a real app's recent reviews carry at least one aspect rating. It's `[]` when the reviewer didn't answer any (most reviews). We're the only Google Play reviews Actor on the Store that surfaces this field — the top 3 competitors by users don't include it in their output schema (re-verified 2026-09-17).

**Why did I get fewer reviews than `maxReviewsPerApp`?** `maxReviewsPerApp` is a **fetch cap**, not a match count — Google Play returns up to that many reviews (newest-first by default), and rating/keyword/appVersion/date filters are applied *after* that, per review. A narrow filter combined with a low cap can miss real matches sitting further back in the feed: on WhatsApp (`com.whatsapp`) with `keyword: "crash"`, `maxReviewsPerApp: 20` fetches 20 reviews and keeps 0, but raising it to `200` finds 1 — the match was always there, just never fetched. When this happens the log carries a `WARN` naming the cap and how many fetched reviews were dropped, and the run's status message says the same — raise `maxReviewsPerApp` to search deeper. Filtered-out reviews are **not** charged either way.

**How do I get alerted about new reviews instead of re-downloading the same ones?** Set `watchLabel` and schedule the Actor (Apify Console → Schedules). The first run is a free baseline that returns nothing; every later run returns only the reviews posted since the previous run, so a scheduled hourly watch on a quiet app costs nothing at all. See "Watch mode" above for how the baseline is keyed and what to watch out for.

**How is `webhookUrl` different from Apify's own platform webhooks?** Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchSkipped`/`baselineTruncated`/`baselineTruncatedTotal`) once the run finishes and every review has already been pushed and charged. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

## Related guides
Engineering write-ups behind this Actor:
- [Google Play has no public reviews API — but the store's own JSON endpoint does](https://fetchsmith.com/blog/google-play-reviews-no-api-batchexecute)
- [HTTP-only vs headless browser scraping: a timed benchmark](https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost)
- [Four ways an invisible character makes a scraper return zero rows](https://fetchsmith.com/blog/invisible-characters-return-zero-rows)

## Notes
Only public Google Play data is collected. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com/tools/google-play-reviews-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/google-play-reviews-scraper
