# Google Play Reviews Scraper

Get Google Play app reviews and app details (ratings, installs, developer info) by app ID or search term. HTTP-only (no browser), so runs are fast and cheap, and you're charged only for the rows you actually get.

It works as a Play Store data API and a Google Play data API in one Actor: pull the same review and app-details fields — ratings, installs, developer info, aspect ratings — as a clean dataset instead of scraping the storefront yourself. Use it as a mobile app reviews data source for any Android app, with country/language targeting and de-duplicated, watch-mode-ready results.

## What it does
- Fetches reviews for one or more Google Play apps, plus an optional app-details record (title, developer, score, installs, price, description, rating histogram).
- Accepts package names (`com.spotify.music`), **full Play Store URLs** (paste the link straight from your browser), or `searchTerms` — the top matching app for each term is resolved automatically.
- Supports country/language targeting and sort order (newest / rating / helpfulness).
- Filter server-side by star rating (range **or** an exact set like 1★+5★), keyword(s), app version, or date range — so you're only charged for reviews you actually want, not the whole feed.
- Reviews are de-duplicated by `reviewId`, so a repeated row from Google Play is never pushed — or charged for — twice.
- **Watch mode** (`watchLabel`): run it on a schedule and get only the reviews posted *since your last run* instead of the same top-of-feed rows every time — a run with nothing new returns nothing and costs nothing. It also catches **edits to reviews you already have**: a reviewer changing their own star rating, or a developer reply being added or removed (`watchEvents`).
- Includes per-review **aspect ratings** (`aspectRatings`) — the sub-scores Google Play attaches to a written review for specific aspects (e.g. ad frequency, ease of use) when the reviewer filled them in. None of the leading Store competitors expose this field (re-verified against their live output schemas 2026-09-17).

## Input
| Field | Type | Description |
|---|---|---|
| `appIds` | array of strings | Google Play package names (e.g. `com.spotify.music`) **or** full Play Store URLs (e.g. `https://play.google.com/store/apps/details?id=com.spotify.music`) — the package name is extracted from the URL's `?id=` param |
| `searchTerms` | array of strings | Alternative to `appIds`: search terms; the top match for each is used, or the first genre-matching hit of the top 5 when `genres` is also set — see FAQ |
| `country` | string | Play Store country code (default `us`) |
| `language` | string | Language for reviews/details (default `en`) |
| `sort` | string | `NEWEST` (default), `RATING`, or `HELPFULNESS` |
| `maxReviewsPerApp` | integer | Reviews to *fetch* per app before moving to the next one (default 100, max 5000) — counted before rating/keyword/appVersion/date filtering, see FAQ |
| `includeAppDetails` | boolean | Also push one app-details record per app (default true) |
| `genres` | array of strings | Only scrape apps in these Google Play genres — every other app is skipped **before any review is fetched, so it costs nothing**. Takes the genre id (`GAME_STRATEGY`, `EDUCATION`), the display name (`Strategy`, `Music & Audio`) or `GAME` for any game genre, case-insensitive. See FAQ |
| `maxResults` | integer | Hard cap across all apps and records (default 500) |
| `minScore` / `maxScore` | integer | Only keep reviews with a star rating in this range (1-5) |
| `ratingFilter` | array of integers | Only keep reviews whose rating is one of these exact values, e.g. `[1, 5]` — use it when you want a non-contiguous set that `minScore`/`maxScore` can't express. Applied **on top of** `minScore`/`maxScore` (an AND, not an override); a combination that leaves no reachable star rating, like `minScore: 4` with `ratingFilter: [1, 2]`, fails immediately instead of running. See FAQ |
| `keyword` | string | Only keep reviews whose title or text contains this word/phrase (case-insensitive) |
| `keywords` | array of strings | Only keep reviews containing **at least one** of these words/phrases (case-insensitive) |
| `appVersions` | array of strings | Only keep reviews written against one of these app versions, e.g. `["9.1.78.2218"]`. Google Play leaves `version` null on roughly 1 review in 6 — those are dropped when this filter is set |
| `minThumbsUp` | integer | Only keep reviews with at least this many "helpful" votes from other users |
| `replyFilter` | string | `any` (default), `hasReply` (only reviews the developer already responded to), or `noReply` (only reviews still waiting for a response — the support-queue use case) |
| `minReviewLength` | integer | Only keep reviews whose text is at least this many characters — filters out one-word/emoji-only reviews |
| `sinceDate` / `untilDate` | string | Only keep reviews posted within this ISO date range |
| `watchLabel` | string | Optional. Name a saved watch (e.g. `my-app-alerts`) to get **only reviews not delivered under that label before** — see "Watch mode" below |
| `watchEvents` | array | Optional, watch mode only. Which changes to report: `new`, `scoreChanged`, `developerReplied`, `replyRemoved`. Empty = all four |
| `webhookUrl` | string | Optional. An http(s) URL to POST a small JSON completion summary to when the run finishes — see FAQ. |

## Watch mode — only new reviews since the last run
Set `watchLabel` to any name and this Actor stops re-delivering the same reviews on every scheduled run:

1. **First run for a label is a free baseline.** It records which reviews already exist (walking at least 1000 per app, regardless of your `maxReviewsPerApp`, up to 5000 reviews total) and returns **zero rows — you are charged nothing**.
2. **Every run after that returns only reviews that weren't in the baseline**, and adds them to it. Nothing new → zero rows → zero charge.
3. **Reviews already in the baseline are re-delivered when they actually change.** Google Play keeps a review's id stable when the reviewer edits their own star rating and when you add or delete a developer reply, so an id-only watch would go silent forever on exactly those events. Pick which ones you want with `watchEvents` (`new`, `scoreChanged`, `developerReplied`, `replyRemoved`; leave empty for all four). Changed rows carry `watchEvent`, `previousScore` and `previousHasDeveloperReply` so you can see what moved.

The baseline lives in **your own** Apify account, in a named key-value store called `fetchsmith-google-play-reviews-watch`, keyed by your label plus a fingerprint of the apps/search terms, country, language, sort order **and every rating, keyword, app-version, thumbs-up, reply, genre and date filter**. Change any of those and you get a fresh baseline rather than a silently wrong one — otherwise widening a filter would hide the newly-matching older reviews as "already seen". Delete the record to start over; use different labels to watch several filter sets in parallel.

Details worth knowing:
- **Change events need one run to warm up.** A baseline created before `watchEvents` existed stores review ids but not the star rating/reply state to diff against; the first run after upgrading records that state (and says so in the log), so `scoreChanged`/`developerReplied`/`replyRemoved` start firing from the run after that. New reviews are unaffected.
- **A score edit that also added a reply is one row, not two.** The change is reported under its primary event (`scoreChanged`) and charged once; the row's own `replyText` shows the current reply state.
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
`result` — $0.0001 per returned item (review or app-details row). The run start is free, and rows dropped by your filters are never charged. That matches the flat rate of the two busiest real-usage rivals, `thewolves/google-play-reviews-scraper` (1,653 users) and `theagents/googleplay-reviews` (667 users), both $0.0001/review with no start fee. Against the niche's biggest competitor by users, `neatrat/google-play-store-reviews-scraper` (2,873 users), we are cheaper on the lower plans and level on the higher ones: their per-review price is tiered $0.00015 FREE, $0.00013 BRONZE, $0.00011 SILVER, then $0.0001 from GOLD through DIAMOND. Re-verified against all three live listings 2026-10-03.

**What we do not claim.** We are not the cheapest per-review Actor in this niche — a wider Store sweep found two more undercutters beyond the one this section used to name. `x.com/google-playstore-review-scraper` (17 users) charges a flat **$0.00001 per review** plus a $0.00005 start fee — about 90% below our $0.0001 on any run of a few hundred reviews or more. `apihq/google-play-reviews-scraper` (48 users, 18 of them in the last 30 days) charges a flat $0.00008 per review with no Actor-start fee, in force since 2026-07-10. `delectable_incubator/google-play-store-reviews-scraper-low-cost` (2 users) charges a flat $0.00009/review plus the same $0.00005 start fee. All three undercut our $0.0001, with no crossover point where we win on price alone; verified live 2026-10-03. Choose this Actor over any of theirs for the app-resolution, filtering and watch-mode features described below, not for a lower unit price.

For completeness, every other priced rival in the niche costs more than us at typical run sizes, verified live 2026-10-03: `curious_coder/google-play-scraper` (2,702 users — the niche's second-biggest listing by users, and a Store sweep's first time naming it) charges a flat $0.0003/review with no start fee, 3x our rate; it scrapes app details and developer/category data as well as reviews, but at triple the per-row price. `solidcode/google-play-store-reviews-scraper` (130 users) $0.0002/review plus a $0.00005 start fee, `shahidirfan/Google-Play-Store-Reviews-Scraper` (16 users) $0.0002 plus a $0.0005 start fee, `benthepythondev/google-play-reviews-scraper` (39 users) $0.002 tapering to $0.0014 at DIAMOND, `coder_zoro/google-play-app-reviews-scraper` (118 users) $0.00499 tapering to $0.00299, `easyapi/google-play-reviews-scraper` (646 users) $0.00299 per review plus a $0.09 start fee, `webdatalabs/google-play-reviews-scraper` (173 users) $0.01 tapering to $0.007 plus a $0.004 start fee, and `scrapesmith/google-play-store-reviews-scraper` (18 users) $0.0001/review (tying our rate) plus a $0.01 start fee that makes every run dearer than ours. One exception with a real crossover: `fetchcraftlabs/playstore-reviews-scraper` (133 users) charges a $0.05 start fee plus a review rate tiered $0.0001 FREE down to $0.00007 GOLD and above — its flat start fee means it's dearer than us below roughly 1,700 reviews in a single run at its cheapest tier, but cheaper above that, a genuine high-volume undercut we didn't have named before. A further listing, `moving_beacon-owner1/my-actor-1` ("Google Play Store Reviews Scraper Pro", 351 users) at $0.004999/review plus a $0.00005 start fee, carries Apify's own `UNDER_MAINTENANCE` notice as of 2026-10-03 — dearer than us even if it were reliable, and not recommended as a live alternative while that notice stands. Verified live 2026-10-03.

On features, rival `neatrat` takes a **single** app per run (`appIdOrUrl` is one string) and offers rating/keyword/version/date filters plus a device-type filter we don't have. This Actor instead accepts **many** apps per run, resolves apps from `searchTerms` when you don't know the package names, filters whole apps by `genres` before fetching a single review, and adds `replyFilter`, `minThumbsUp`, `minReviewLength`, `includeAppDetails`, stateful watch mode with edit/reply change events, and a completion `webhookUrl` — none of which exist in their live input schema, checked property by property against their 2026-09-30 build rather than their Store description. Verified live 2026-10-01.

The one rival that does overlap our review-level filters is `code-node-tools/google-play-reviews-scraper` (257 users, 55 in the last 30 days). Its input schema carries `minThumbsUp` and `minReviewLength` under those exact names, plus `hasReply` (our `replyFilter`), `dateFrom`/`dateTo` (our `sinceDate`/`untilDate`), `minScore`/`maxScore` and `keywords`, and like us it takes many apps per run — so treat the filter list above as what `neatrat` lacks, not as unique to us in the niche. What it has no equivalent for: `searchTerms` app resolution, `genres` app-level filtering, `includeAppDetails`, watch mode, `webhookUrl`, and per-review aspect ratings (its documented output row has no aspect-rating field). It also bills a $0.002 Actor-start fee on every run plus $0.0005 per review on the free plan ($0.0003 at Gold and above), so 1,000 reviews costs about $0.50 there versus $0.10 here. Input schema and pricing verified live 2026-10-01.

## FAQ
**Can I get reviews in a specific country or language?** Yes, set `country` and `language` (Play Store returns different review sets per locale — run the Actor for each locale you need).
**Can I search by app name instead of package ID?** Yes, use `searchTerms`; the top matching app is resolved automatically.
**Why did I get fewer reviews than the app's total rating count?** Google Play's review API only returns a subset of written reviews, not every rating — this is a platform limitation, not a bug.
**Does `keyword`/`keywords` handle accented words correctly?** Yes, as of v0.1.20 — both fields and the review text they're matched against are Unicode-normalized before comparing, so an accented word (e.g. "café") matches regardless of which of Unicode's two equivalent representations (composed vs. decomposed) you typed it in.
**Can I filter to just negative or just recent reviews?** Yes — set `maxScore` (e.g. 2) for negative-only, `ratingFilter: [1, 5]` for only the extremes, or `sinceDate`/`untilDate` for a date window; filtering happens before you're charged, so you never pay for rows you filtered out.

**Can I restrict a run to games (or to any one app category)?** Yes — set `genres`. `["GAME"]` keeps every game genre (`GAME_STRATEGY`, `GAME_CASUAL`, `GAME_PUZZLE`, …); `["GAME_STRATEGY", "Music & Audio"]` mixes an exact genre id with a display name. Verified 2026-09-28: with `genres: ["GAME"]`, `com.king.candycrushsaga` (`GAME_CASUAL`) and `com.supercell.clashofclans` (`GAME_STRATEGY`) were scraped while `com.spotify.music` (`MUSIC_AND_AUDIO`) and `com.duolingo` (`EDUCATION`) were skipped with zero reviews fetched and zero charged. It needs one app-details lookup per app, so it works with `includeAppDetails` off too, and if the genre can't be read the app is skipped rather than scraped unfiltered — you are never billed for rows the filter exists to exclude.

**With `genres` set, does a `searchTerms` lookup still use just the top hit?** No — when `genres` is set it pulls the top 5 search hits (instead of 1) and keeps the first one whose own genre already matches, falling back to the top hit only if none of the 5 do. Without `genres`, `searchTerms` still resolves to the single top hit, same as always. This matters because Play's #1 result for a term is not always the right category: verified 2026-09-28, `searchTerms: ["sky"]` with `genres: ["EDUCATION"]` resolved to `com.noctuasoftware.stellarium_free` (`EDUCATION`, Play's 4th-ranked hit for "sky") — the unranked #1 hit for "sky" is a role-playing game. Before this fix, a term like that returned zero apps instead of the education one buried a few ranks down.

**Can I see what broke in a specific release?** Set `appVersions` to the version string(s) you care about (they match the `version` field on each review row) and, if you want, combine it with `maxScore: 2` and `keywords` to isolate the complaints. Reviews where Google Play reports no version are excluded rather than guessed at.

**Can I find reviews my support team hasn't answered yet, or check response quality on the ones we have?** Yes — `replyFilter: "noReply"` returns only reviews with no developer response (combine with `maxScore: 2` for an unanswered-complaints queue); `replyFilter: "hasReply"` returns only the ones you already responded to, e.g. to audit response quality or turnaround. `minThumbsUp` and `minReviewLength` are the same idea applied to helpfulness votes and review length — e.g. `minThumbsUp: 5` surfaces the reviews other users found worth upvoting, and `minReviewLength: 100` filters out one-word/emoji-only noise. All three were already computed on every review row (`thumbsUp`, `replyText`, `text`) but unfilterable before this — live-verified on a real app (Discord) that 21/50 recent reviews had a developer reply and the other 29 didn't, split exactly by `replyFilter`.

**What is `aspectRatings`?** Google Play sometimes prompts a reviewer to rate specific aspects of the app (e.g. "Ads frequency", "Ease of use") alongside their overall star score. When present, each row's `aspectRatings` array has one `{criteria, rating}` entry per aspect the reviewer answered — verified live across 800 reviews on 4 major apps (Spotify, WhatsApp, Duolingo, Candy Crush Saga): 27.3% carried at least one aspect rating, and the taxonomy is category-aware (games get dozens of genre-specific criteria, utility apps get a small generic set). It's `[]` when the reviewer didn't answer any (most reviews). We're the only Google Play reviews Actor on the Store that surfaces this field — the top 3 competitors by users don't include it in their output schema (re-verified 2026-09-17). One quirk worth knowing: ~2% of criteria entries use a `vaf_never_display_*` prefix — Google's own internal name implying its UI won't render that category, yet it comes back in the same array as every normal one, with nothing distinguishing the two. See the [full write-up](https://fetchsmith.com/blog/google-play-hidden-aspect-ratings-and-histogram) for the per-app numbers.

**Why did I get fewer reviews than `maxReviewsPerApp`?** `maxReviewsPerApp` is a **fetch cap**, not a match count — Google Play returns up to that many reviews (newest-first by default), and rating/keyword/appVersion/date filters are applied *after* that, per review. A narrow filter combined with a low cap can miss real matches sitting further back in the feed: on WhatsApp (`com.whatsapp`) with `keyword: "crash"`, `maxReviewsPerApp: 20` fetches 20 reviews and keeps 0, but raising it to `200` finds 1 — the match was always there, just never fetched. When this happens the log carries a `WARN` naming the cap and how many fetched reviews were dropped, and the run's status message says the same — raise `maxReviewsPerApp` to search deeper. Filtered-out reviews are **not** charged either way.
**Why does `ratingFilter: [1, 2]` return 0 rows even though the app clearly has low ratings?** Check `sort`. `RATING` sorts highest-first, so the `maxReviewsPerApp` fetch cap (applied before any filter, see above) can fill up entirely with 5-star reviews and never reach a 1★ or 2★ one — same root cause as the fetch-cap FAQ, just with sort order as the trigger instead of a low cap. **Use `sort: "NEWEST"` (the default) when hunting for specific low ratings — raising `maxReviewsPerApp` will not rescue a `RATING`-sorted run on a popular app.** Verified 2026-09-25 on Spotify (`com.spotify.music`): with `sort: "RATING"`, `maxReviewsPerApp: 5000` (the maximum) fetched all 5000 and kept **0** for both `ratingFilter: [1, 2]` and `ratingFilter: [4]` — every one of the 5000 was a 5★ review, so no allowed cap value can reach lower stars. The run now warns about this combination up front, before spending the fetch budget.

**Can I use `ratingFilter` and `minScore`/`maxScore` together?** Yes, but they are ANDed, not overridden — a review must satisfy both. That means some combinations can never match anything: `minScore: 4` with `ratingFilter: [1, 2]` asks for reviews that are simultaneously ≥4★ and exactly 1★ or 2★, and Google Play reviews only carry whole stars 1-5. **Such a run now fails immediately with an explanation instead of silently returning 0 reviews.** That mattered because the old behaviour was actively misleading: verified 2026-09-30 on Spotify (`com.spotify.music`), `minScore: 4` + `ratingFilter: [1, 2]` fetched all 60 requested reviews, dropped all 60, and closed with "raise `maxReviewsPerApp` to search further" — advice that cannot work at any depth, because the contradiction is in the input, not in the feed. The same check catches a `ratingFilter` containing only values outside 1-5 (e.g. `[6]` or `[4.5]`), which the input editor accepts. Partial overlaps are left alone and still work normally: `minScore: 2`, `maxScore: 4` with `ratingFilter: [1, 3]` legitimately means "3★ only".

**How do I get alerted about new reviews instead of re-downloading the same ones?** Set `watchLabel` and schedule the Actor (Apify Console → Schedules). The first run is a free baseline that returns nothing; every later run returns only the reviews posted since the previous run, so a scheduled hourly watch on a quiet app costs nothing at all. See "Watch mode" above for how the baseline is keyed and what to watch out for.

**Can I be alerted when someone edits a review I already downloaded?** Yes — that is what `watchEvents` is for. Google Play lets a reviewer rewrite their own review (same review id, new star rating) and lets a developer add or delete a reply at any time, and a watch keyed only on review ids can never see either. With a `watchLabel` set, this Actor also diffs the star rating and reply state each review had when it was last delivered, and re-delivers it as `watchEvent: "scoreChanged"`, `"developerReplied"` or `"replyRemoved"` with `previousScore`/`previousHasDeveloperReply` filled in. Restrict it to the events you care about (e.g. `["scoreChanged"]` to track only rating downgrades) so you never pay for the rest. A baseline created before this existed needs one run to record the state it will diff against.

**How is `webhookUrl` different from Apify's own platform webhooks?** Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchSkipped`/`baselineTruncated`/`baselineTruncatedTotal`) once the run finishes and every review has already been pushed and charged. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

## Related guides
Engineering write-ups behind this Actor:
- [Google Play has no public reviews API — but the store's own JSON endpoint does](https://fetchsmith.com/blog/google-play-reviews-no-api-batchexecute)
- [Google Play's review API carries two fields almost nobody reads — a full star histogram and a hidden per-review "aspect" breakdown](https://fetchsmith.com/blog/google-play-hidden-aspect-ratings-and-histogram)
- [HTTP-only vs headless browser scraping: a timed benchmark](https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost)
- [Four ways an invisible character makes a scraper return zero rows](https://fetchsmith.com/blog/invisible-characters-return-zero-rows)
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for. This is the Actor the bug was first found and reproduced on.
- [App Store, Google Play and Steam reviews — three JSON APIs, three unrelated meanings of "empty"](https://fetchsmith.com/blog/app-store-review-apis-three-silent-empties) — how this Actor's specific silent-empty failure mode compares to the other two review platforms we scrape.
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — the fleet-wide survey of watch-mode failure shapes across all nineteen incremental Actors, this one included.

## Notes
Only public Google Play data is collected. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com/tools/google-play-reviews-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/google-play-reviews-scraper
