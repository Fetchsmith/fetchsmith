# App Store Reviews Scraper (Apple)

Get customer reviews for any iOS / macOS app from the Apple App Store, for any country storefront, as JSON, CSV or Excel. Each review includes rating, title, text, app version, author and date, plus optional app metadata (name, developer, average rating, rating count) and the **full per-star ratings breakdown** — how many 1★, 2★, 3★, 4★ and 5★ ratings the app has in that storefront. Pay only per review returned.

## Use cases
- Product research and competitor analysis across countries
- Sentiment analysis, feature-request mining, churn reasons
- Monitoring your own app's newest reviews on a schedule
- Feeding reviews into AI agents and dashboards
- **Alerting on new reviews only** — set `watchLabel` and schedule it; see [Watch mode](#watch-mode--only-new-reviews-since-the-last-run) below
- **Alerting on rating reversals** — `watchEvents: ["scoreChanged"]` catches a reviewer editing their own star rating on a review you already have, e.g. a 5★→1★ downgrade after a bad update

## Input
| Field | Type | Description |
|---|---|---|
| `apps` | array | App Store URLs or numeric app IDs |
| `appNames` | array | Free-text app names (e.g. `"Notion"`) — auto-resolved to an app id via Apple's own search API. See caveat below. |
| `includeMacApps` | boolean | Also search the **Mac App Store** when resolving `appNames` (default `false`). Apple's app-name search is iOS-only, so Mac-only apps are invisible without it — see below. |
| `countries` | array | Storefront codes, e.g. `us`, `gb`, `de`, `jp`, `br` (default `us`) |
| `countryFallback` | boolean | If a storefront returns nothing, pull that app's reviews from one that works (default `false`) |
| `sort` | string | `mostRecent` (default), `mostHelpful`, or `favorable`/`critical` to deliver reviews ordered by star rating (highest/lowest first, newest first within a tied rating) — see FAQ. `favorable`/`critical` cannot be combined with `watchLabel`. |
| `maxReviewsPerApp` | integer | Up to 500 per app per country (Apple's documented limit; in practice its feed often stops sooner — the run says so, see FAQ) — counted before the review filters (rating/keyword/length/votes/date), see FAQ |
| `includeAppInfo` | boolean | Attach app name, developer, average rating, rating count and the per-star `ratingBreakdown` (default `true`) |
| `maxResults` | integer | Total cap |
| `minRating` / `maxRating` | integer | Only keep reviews with a star rating in this range (1-5) |
| `keyword` | string | Only keep reviews whose title or content contains this word/phrase (case-insensitive) |
| `reviewsAfter` | string (ISO date) | Only keep reviews posted on or after this date. Forces `sort` to `mostRecent` and stops paging as soon as older reviews are reached, so a narrow window doesn't scan (and isn't charged for) pages you don't want. |
| `reviewsBefore` | string (ISO date) | Only keep reviews posted on or before this date (a bare date includes the whole of that day). Pair it with `reviewsAfter` for a date range. |
| `minReviewLength` | integer | Only keep reviews whose **body text** is at least this many characters — drops one-word "Great!" ratings without discarding a short review that happens to have a long title. |
| `minVoteSum` / `minVoteCount` | integer | Only keep reviews with at least this many net helpful votes / total helpfulness votes. Requires `sort: mostHelpful` — see FAQ. |
| `watchLabel` | string | Turns this run into a [watch](#watch-mode--only-new-reviews-since-the-last-run) — only reviews posted since the last run under this label are returned and charged. Leave empty for normal runs. |
| `watchEvents` | array | Optional, watch mode only. `new` and/or `scoreChanged` — pick `scoreChanged` alone to be alerted only when an existing reviewer edits their own star rating, and pay for nothing else. Leave empty for both. See [Watch mode](#watch-mode--only-new-reviews-since-the-last-run). |
| `webhookUrl` | string | Optional. An http(s) URL to POST a JSON completion summary to when the run finishes — row counts plus the per-pair completeness records, see FAQ. The same records are always written to the run's `RUN_SUMMARY` key-value record whether or not you set this. |

Filtering happens before you're charged — you never pay for rows that got filtered out.

## Watch mode — only new reviews since the last run
Set `watchLabel` to any name and this Actor stops re-delivering the same reviews on every scheduled run:

1. **First run for a label is a free baseline.** It records which reviews already exist for every `apps`/`countries` pair — walking as deep as Apple will serve, up to 500 per pair and regardless of `maxReviewsPerApp` — and returns **zero rows — you are charged nothing**. Apple's feed often stops well short of 500 (see the FAQ), so a baseline may only cover the newest ~50 reviews of a pair; that is safe, see the next bullet.
2. **Every run after that returns only reviews that weren't in the baseline**, and adds them to it. Nothing new → zero rows → zero charge.
3. **A review older than the baseline could reach is never billed as "new".** Each pair also records the oldest review date its baseline walk actually scanned. If Apple's feed serves deeper on a later run than it did at baseline time, the extra older reviews are recognised as pre-existing — not delivered, not charged — and the run says how many. Reviews posted after the baseline are always newer than that date, so real alerts are never suppressed.
4. **An already-delivered review whose author edits their own star rating is delivered again, as a `scoreChanged` event, not silently missed.** Apple keeps a review's id stable when the reviewer edits it in place (only the feed's own `updated` date advances) — so without this, a review your watch already delivered at 5★ could quietly drop to 1★ and you'd never know. Every row carries `watchEvent` (`new` or `scoreChanged`) and, on a `scoreChanged` row, `previousScore` (the rating last recorded for it). Use `watchEvents` to receive only one kind, e.g. `["scoreChanged"]` to watch an app you already track elsewhere purely for sentiment reversals. There is no developer-reply field anywhere in this review feed (unlike Google Play), so that isn't an event this Actor can offer.

The baseline lives in **your own** Apify account, in a named key-value store called `fetchsmith-app-store-reviews-watch`, keyed by your label plus a fingerprint of `apps`/`appNames`/`countries`/`countryFallback`/`sort` **and every review filter (`minRating`/`maxRating`/`keyword`/`minReviewLength`/`reviewsAfter`/`reviewsBefore`/`minVoteSum`/`minVoteCount`)** (Apple's feed takes none of those server-side, so all of them decide what "new" means). Change any of those and you get a fresh baseline rather than a silently wrong one. Delete the record to start over; use different labels to watch several filter sets in parallel.

Details worth knowing:
- **Use `sort: "mostRecent"`** (the default). `mostHelpful` isn't date-ordered, so a brand-new review isn't necessarily inside the scanned window and can be missed; the run logs a warning if you watch with `mostHelpful` anyway.
- **`maxReviewsPerApp` is your scan-depth budget on incremental runs and is left exactly as you set it** — with `mostRecent`, new reviews sort at the top, so your own cap doesn't hide them. If every matching review inside that window turned out to be new, the run warns you that reviews posted since the last run may sit further back — raise `maxReviewsPerApp` or run the watch more often.
- If an `appNames` search resolves to a *different* app than last time (or a new `countries` entry appears), that app/country pair is baselined on the spot rather than having its entire review history delivered as "new".
- `countryFallback` still applies during a watch — a baselined pair whose storefront later goes empty falls back the same way a normal run does.
- Reviews with no id Apple can hand back (rare) are skipped in watch mode, since they can't be recognized on the next run — never charged.
- **Change events need one run to warm up.** A baseline created before `watchEvents` existed stores review ids but not the star rating to diff against; the first run after upgrading records that state (and says so in the log), so `scoreChanged` starts firing from the run after that. New reviews are unaffected.
- **Baseline size cap:** the saved baseline holds at most 40,000 review ids across all your `apps`/`countries` pairs (the oldest drop off first). A watch this large is rare, but if it happens, the dropped ids will be delivered and **charged again** as "new" on a future run — the run's log and status message name the count when it occurs (`RUN_SUMMARY.baselineTruncated`/`baselineTruncatedTotal`). Split a very large watch across several labels (e.g. one per app) to stay under the cap.

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
- sets a run status message explaining *why* a run returned few or no rows (empty Apple feed vs. your own rating/keyword filters vs. a storefront Apple refused);
- **separates "Apple has no reviews here" from "Apple refused this request".** A storefront code that is well-formed but isn't a real Apple store answers every request with `HTTP 400`; that pair ends on its first refusal rather than paging on, the message says what Apple actually returned, and if *every* pair in the run was refused the run **fails** instead of reporting an empty result. In watch mode a refused pair is deliberately left out of the baseline, so a broken storefront can never be silently recorded as "already delivered";
- **retries connection-level failures up to 3 times before believing them.** A dropped connection is not an answer, but got's own retry list doesn't cover the HTTP/2 connection faults measured at roughly 1 fresh connection in 4 across this fleet (2026-09-21), so one blip used to end an app's scan or quietly return `ratingBreakdown: null`. Every review-feed, lookup, search and ratings-page request now retries with backoff first. A real HTTP error from Apple (a wrong storefront code) still fails immediately with the explanation instead of looping;
- **fails loudly instead of returning a misleading empty result when the fault is Apple's, not yours.** Apple sometimes serves an empty feed for *everything* — measured 2026-09-16: every app, storefront, page, sort and client came back `HTTP 200` with zero entries. From one app's response that is indistinguishable from "this app has no reviews", so when a run ends up with no reviews at all we re-check two control apps that always have hundreds of thousands of reviews (three attempts, spaced). If those are empty too, the run **fails** with a message naming the Apple-side fault, rather than telling you no reviews matched your filters. A watch-mode baseline is never written from such a run either — otherwise the next run would treat the app's whole review history as "new" and charge you for it.

- **says all of that in a form a program can read, not just in English.** Every run writes a `RUN_SUMMARY` record to its key-value store with one entry per app/storefront pair: how many reviews were `scanned`, how many `delivered`, how many your filters removed, how many ratings Apple *declares* the app has (`declaredRatingCount`), and a `complete` flag with the reason that made it false. A status message is for a human reading the run page; this is for the pipeline that never reads it (see FAQ).

You are never charged for empty pages, for retries, or for a run that fails this way.

## FAQ
**Can I be alerted when someone edits a review I already downloaded?** Yes — that is what `watchEvents` is for. Apple lets a reviewer rewrite their own review (same review id, new star rating, only the feed's own `updated` date advances) — there is no "new review" event to catch that, since it isn't new. With a `watchLabel` set, this Actor also diffs the star rating each review had when it was last delivered and re-delivers it as `watchEvent: "scoreChanged"` with `previousScore` filled in. Restrict it with `watchEvents: ["scoreChanged"]` to track only rating edits (e.g. skip the noise of every brand-new review and pay only for reversals) or `["new"]` to keep today's behavior. A baseline created before this existed needs one run to record the state it will diff against. There is no developer-reply field on this feed, so unlike Google Play there's no equivalent "developer replied" event to offer.

**Why did my run return 0 reviews with status SUCCEEDED?** Check the run's status message first — it tells you whether Apple's feed was genuinely empty for that app/storefront or your own review filters (rating/keyword/length/votes/date) removed every row.
**What country codes does `countries` take?** Apple storefronts are two-letter ISO-3166-1 **alpha-2** codes — the UK is `gb`, not `uk`, and there is no `usa`/`uk`/`eng`. A wrong code used to look like an app with no reviews (Apple answers `uk` with `HTTP 400` carrying valid JSON and no results); now a recognisable wrong code fails the run in about a second, before the first request and before any charge, and names the code you should have used. A well-formed code Apple simply doesn't run a store in (e.g. `zz`) ends that app/storefront pair on its first refusal instead of walking the rest of the page range, and the run says which pairs Apple refused.
**Can I get more than 500 reviews for one app?** No — Apple's public feed caps at 500 most-recent reviews per app per country, and **in practice it usually serves fewer**. Its review RSS is served from a patchy index: measured 2026-09-22, the walk commonly ends on a full page well before page 10, so a heavily-reviewed app like Notion or Spotify returns ~100 rather than 500 per storefront. The Actor retries every empty page under a second client class to recover as much as it can, and when the feed quits early it says so explicitly (next FAQ) instead of letting a short result look complete. Widen `countries` for more coverage. Run on a schedule and deduplicate by `reviewId` to build a larger archive over time. Note that `totalRatings`/`ratingBreakdown` are **not** capped: they cover every rating the app has ever received in that storefront, so you still get the full-population distribution even though only 500 written reviews are reachable.
**How do I know whether Apple cut the feed off or the app simply has no more reviews?** The run tells you, as of v0.1.51. Whenever the last page Apple served came back **full** and the Actor was still willing to take more, the run's status message names those app/storefront pairs, says which page the feed quit at and how many reviews it handed over, and states plainly that raising `maxReviewsPerApp` cannot reach the older ones (widen `countries`, or schedule with `watchMode` instead). This covers both the documented 500/10-page ceiling and the much more common early stop. A run that ends on a **partial** page genuinely exhausted what Apple serves for that pair — so a *missing* note is itself the "you got everything available" signal.
**Why is `totalRatings` different from `ratingCount`?** They come from two different Apple sources and are both real. `ratingCount` is Apple's lookup API figure; `totalRatings` is the sum of the per-star histogram shown on the App Store product page, which updates on a slightly different schedule. Expect them to agree to within a fraction of a percent — if you need the number that matches `ratingBreakdown` exactly, use `totalRatings`.
**Does `keyword` handle accented words correctly?** Yes, as of v0.1.29 — `keyword` and the review text it's matched against are Unicode-normalized before comparing, so an accented word (e.g. "café") matches regardless of which of Unicode's two equivalent representations (composed vs. decomposed) you typed it in.
**Is `reviewUrl` unique per review?** No, and it isn't presented as such. It's Apple's own "related" link from the feed entry, which points at the app's review page for that storefront — the same URL for every review of that app in that country. Apple does not publish a per-review permalink; use `reviewId` as the unique key.
**Does `countryFallback` change the `country` field on rows I already have?** No — fallback rows are clearly tagged with `fallbackUsed: true` and keep both the real `country` they came from and the `requestedCountry` you asked for.
**Do I get charged for empty pages or retries?** No — only reviews actually returned to the dataset are charged.
**Why does `minVoteSum` return nothing?** Apple only populates helpfulness votes (`voteSum`/`voteCount`) on its **mostHelpful** feed. Every review served by the `mostRecent` feed comes back with `0` votes — that is real data (new reviews genuinely have no votes yet), not a gap we can fill, and it is why `reviewsAfter` (which forces `mostRecent`) can't be combined with a vote floor above 0. Set `sort: "mostHelpful"` and the filter works as expected; the run log warns you when it can't.
**How is `webhookUrl` different from Apify's own platform webhooks?** Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchSkipped`, plus `pairsIncomplete` and the full per-pair `pairs` array described above) once the run finishes and every review has already been pushed and charged. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

**How do I check in code whether a run got everything?** Read the run's `RUN_SUMMARY` key-value record — `GET https://api.apify.com/v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY` (no webhook needed; the same data is also POSTed to `webhookUrl` as `pairs` if you set one). It holds run-level `complete` / `incompleteReason` / `incompleteDetail`, the counts `pushed`, `pairsPlanned`, `pairsAttempted`, `pairsIncomplete`, `pairsUnknown`, and a `pairs` array with one record per app/storefront:

```json
{
  "app": "310633997", "country": "us", "status": "ok",
  "scanned": 50, "delivered": 50, "filteredOut": 0,
  "declaredRatingCount": 18632949,
  "complete": false, "incompleteReason": "apple-feed-ceiling",
  "scanDepthCap": 500, "feedStopPage": 4, "reason": null
}
```

That row is the honest version of a 50-row dataset for an app with 18.6 million ratings: you got everything Apple's public feed served, and Apple served a fraction of what exists. `status` is one of `ok`, `empty` (Apple's feed has nothing for that pair), `filteredOut` (reviews found, your filters removed all of them), `watchBaselined`, `watchNoChanges`, `error` (Apple refused the request — `reason` quotes it), `badAppId` (an `apps` entry no app id could be parsed from), `notReached` (the run stopped before it got there), or `timedOut` (the run was approaching its platform run timeout and stopped before this pair returned anything — this says nothing about whether Apple has reviews for it). `complete` is deliberately **separate** from `status`: a pair can deliver reviews perfectly normally and still have been cut short, and `incompleteReason` names which — `apple-feed-ceiling` (Apple stopped serving; no input value can reach deeper), `max-reviews-per-app`, `max-results`, `charge-limit`, `baseline-cap`, or `time-budget` (the run stopped itself short of the platform run timeout so the rows already collected would still be returned — narrow the input, raise the Actor's run timeout, or split the pairs across runs). `complete: null` and `declaredRatingCount: null` mean *not observed*, never zero (`declaredRatingCount` is only filled when `includeAppInfo` is on).

**Just tell me if the run got everything — one field.** Read the top-level `complete` on the same record. It is `true` only when every pair came back complete, `false` if any pair fell short *or* could not report at all, and `null` when no pair was attempted. `incompleteReason` names the first pair that fell short (same vocabulary as the per-pair field, plus `storefront-error`, `bad-app-id`, `not-reached` and `time-budget` for pairs that have no reason of their own), and `incompleteDetail` says which pair and how many others. This is the same `complete` / `incompleteReason` / `incompleteDetail` contract every FetchSmith Actor's `RUN_SUMMARY` carries, so one pipeline can check all of them the same way. Watch `pairsUnknown` too: it counts pairs with *no* completeness to report, which `pairsIncomplete` (known-short pairs only) deliberately excludes.

**How does `sort: "favorable"`/`"critical"` work?** Apple's feed has no server-side "sort by rating" — there is no such request you can make. Instead, the Actor scans that app/storefront pair under `mostRecent` exactly as usual (so `maxReviewsPerApp`/`reviewsAfter` mean exactly what they mean today), then re-orders everything it kept **after filtering, before delivery**: `favorable` is 5★-to-1★, `critical` is 1★-to-5★, and reviews tied on rating stay newest-first. Because the whole pair's result has to be assembled before anything can be ordered, it can't be combined with `watchLabel` (whose "only what's new" logic depends on delivering in scan order) — use `mostRecent`/`mostHelpful` for watches.

**Why did I get fewer reviews than `maxReviewsPerApp`?** `maxReviewsPerApp` is a **scan cap**, not a match count — it stops paging Apple's feed after that many reviews have been looked at, and the review filters (rating/keyword/length/votes/date) are applied *after* that, per review. A narrow filter combined with a low cap can miss real matches sitting deeper in the feed: on Spotify (`324684580`) with `maxRating: 1`, `maxReviewsPerApp: 5` scans 5 reviews and keeps 0, but raising it to `100` finds 12 — the matches were always there, just unscanned. When this happens the log carries a `WARN` naming the cap and how many scanned reviews were dropped, and the run's status message says the same — raise `maxReviewsPerApp` to search deeper. Filtered-out reviews are **not** charged either way.

## Notes
Apple exposes the most recent 500 reviews per app per country. For historical archives, run on a schedule and deduplicate by `reviewId`.

## Related guides
Engineering write-ups behind this Actor:
- [Apple's review feed has holes, and whether you hit one depends on your HTTP client](https://fetchsmith.com/blog/apple-app-store-reviews-header-fingerprint)
- [The App Store's per-star ratings breakdown isn't in any of Apple's APIs — it's in the page's JSON blob](https://fetchsmith.com/blog/app-store-per-star-ratings-breakdown)
- [Four ways an invisible character makes a scraper return zero rows](https://fetchsmith.com/blog/invisible-characters-return-zero-rows)
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for.
- [App Store, Google Play and Steam reviews — three JSON APIs, three unrelated meanings of "empty"](https://fetchsmith.com/blog/app-store-review-apis-three-silent-empties) — how this Actor's specific silent-empty failure mode compares to the other two review platforms we scrape.
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — the fleet-wide survey of watch-mode failure shapes across all nineteen incremental Actors, this one included.

Only publicly available data is collected. Support: support@fetchsmith.com · Hosted API: https://fetchsmith.com/tools/app-store-reviews-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/app-store-reviews-scraper
