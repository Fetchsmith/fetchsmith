# Steam Reviews Scraper

Scrape **Steam player reviews** and **Steam store data** into JSON, CSV or Excel — no login, no browser, no proxy needed.

Give it Steam store URLs, numeric App IDs, or just game names to search for. You get every review with its full text, the reviewer's **playtime**, whether they recommend the game, helpfulness votes, whether it was a real Steam purchase, and (optionally) the game's name, developer, publisher, genres and release date attached to every row.

**Pay per result: $0.000575 per review or game record on the free plan, dropping to $0.0003 on Gold and above** (Bronze $0.0005, Silver $0.00039). **No start fee** — a run that returns nothing costs nothing.

## What you can do with it

- **Track sentiment after a patch or a price change** — pull reviews sorted by most recent, filter to `negative`, and diff week over week.
- **Find bug reports in the wild** — set `keyword` to `crash`, `stutter`, `controller` or `refund` and get only the reviews that mention it.
- **Filter out drive-by reviews** — `minPlaytimeHours: 10` keeps only reviewers who actually played the game.
- **Pull reviews from an exact historical window** — `reviewsAfter`/`reviewsBefore` (e.g. a specific patch, a controversy, a launch week years ago) reach any point in a game's history, not just the last year.
- **Study a review bomb** — `includeOffTopic: true` returns the reviews Steam itself hides when Valve flags a stretch of time as off-topic activity. On War Thunder that is 125,691 reviews you cannot see anywhere on the store page.
- **Competitive research** — `dataType: "games"` returns price, discount, genres, developer, Metacritic score, the full review-score summary (total positive/negative, % positive) and, optionally, the **live concurrent player count**.
- **Size a market, not just a game** — `includeOwnerEstimates: true` adds an estimated owner range, peak concurrent players yesterday and Steam's **crowd-voted tags with vote counts** to every game row. Those tags are what players actually call a game (Hades: `Action Roguelike`, `Rogue-lite`, `Hack and Slash`) rather than the three broad genres the store API returns (`Action`, `Indie`, `RPG`).
- **Localised research** — `language: "schinese"`, `"russian"`, `"brazilian"` … or `"all"` for every language at once.
- **Feed an LLM / dataset pipeline** — clean flat rows, stable `reviewId`, ISO-8601 timestamps.
- **Alert on new reviews only** — set `watchLabel` and schedule it; see [Watch mode](#watch-mode--only-new-reviews-since-the-last-run) below.

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `dataType` | string | `reviews` | `reviews` = player reviews; `games` = store record for each game |
| `apps` | array | — | Steam store URLs (`https://store.steampowered.com/app/1145360/Hades/`) or numeric App IDs (`1145360`) |
| `searchTerms` | array | — | Find games by name instead of / as well as URLs |
| `maxReviewsPerApp` | integer | `200` | Reviews to *scan* per game before moving to the next one (max 5000) — counted before `keyword`/`minPlaytimeHours` filtering, see FAQ |
| `maxResults` | integer | `2000` | Hard cap on rows pushed — also caps what you are charged |
| `language` | string | `english` | Steam language code, or `all` |
| `reviewType` | string | `all` | `positive` / `negative` to keep only thumbs-up / thumbs-down |
| `purchaseType` | string | `all` | `steam` excludes key activations and free weekends |
| `includeOffTopic` | boolean | `false` | Include reviews from periods Valve flagged as **off-topic review bombs** — see below |
| `sortBy` | string | `recent` | `recent`, `updated`, `all` (Steam's helpfulness ranking) or `funny` (Steam's "Funny" tab — most funny votes, all-time) |
| `dayRange` | integer | — | With `sortBy: "all"`, restrict to the last N days (1–365). Ignored in every other sort mode (Steam has no day range there) — the run warns rather than silently dropping it |
| `reviewsAfter` | string | — | ISO date (`2024-01-01`) — keep only reviews created on/after this date. Reaches any point in history, forces `sortBy` to `recent`. |
| `reviewsBefore` | string | — | ISO date — keep only reviews created before this date. Combine with `reviewsAfter` for an exact window. |
| `minPlaytimeHours` | integer | — | Keep only reviewers with at least this many hours in the game |
| `keyword` | string | — | Keep only reviews whose text contains this word/phrase |
| `country` | string | `us` | Two-letter code for store prices and availability |
| `includeGameInfo` | boolean | `true` | Attach game name/developer/publisher/genres/release date to every review |
| `includePlayerCount` | boolean | `false` | `games` mode: also fetch the live concurrent player count |
| `includeOwnerEstimates` | boolean | `false` | `games` mode: add estimated owner range, peak concurrent players yesterday, and Steam's crowd-voted tags with vote counts — see below |
| `searchLimit` | integer | `10` | Games taken from each search term |
| `watchLabel` | string | — | Turns this run into a [watch](#watch-mode--only-new-reviews-since-the-last-run) — only reviews posted since the last run under this label are returned and charged. Reviews mode only. Leave empty for normal runs. |
| `watchEvents` | array | *(both)* | Watch mode only. Which change types to report: `new` and/or `recommendationChanged` (an already-delivered review whose thumbs-up/thumbs-down flipped). Leave empty for both. |
| `webhookUrl` | string | — | Optional. An http(s) URL to POST a small JSON completion summary to when the run finishes — see FAQ. |

## Off-topic review bombs (`includeOffTopic`)

When a game gets review-bombed over something that isn't the game — a publisher decision, a
storefront policy, a controversy — Valve flags that stretch of time as *off-topic activity* and
Steam hides those reviews from its own review lists and score. **That is Steam's default, so it is
this Actor's default too.** Set `includeOffTopic: true` to get the unfiltered set instead, which is
exactly what you want if the backlash *is* the thing you are studying.

The difference is not cosmetic (checked 2026-09-17):

| Game | Reviews with the flag hidden (default) | With `includeOffTopic: true` |
|---|---|---|
| Total War: ROME II (`214950`) | 88,334 | 94,228 |
| War Thunder (`236390`) | 784,322 | 910,013 |
| NARAKA: BLADEPOINT (`1203220`) | 302,783 | 343,134 |

It applies to `dataType: "reviews"` **and** to the `reviewScore` / `totalReviews` fields on
`dataType: "games"` rows, so a game row never reports a score that contradicts the reviews you
pulled alongside it.

## Watch mode — only new reviews since the last run

Set `watchLabel` to any name and this Actor stops re-delivering the same reviews on every scheduled run:

1. **The first run for a label is a free baseline.** It records which reviews already exist for every game in your input and returns **zero rows — you are charged nothing**.
2. **Every run after that returns only reviews that weren't in the baseline**, and adds them to it. Nothing new → zero rows → zero charge.
3. **An already-delivered review isn't necessarily done changing.** Steam lets a reviewer edit their own review in place — same `reviewId`, but the thumbs-up/thumbs-down (and the review's own `updatedAt`) can flip. Set `watchEvents` to control which of `new`/`recommendationChanged` you get charged for (default: both).

The baseline lives in **your own** Apify account, in a named key-value store called `fetchsmith-steam-reviews-watch`, keyed by your label plus a fingerprint of `apps`/`searchTerms`/`searchLimit`/`country`/`language`/`reviewType`/`purchaseType`/`includeOffTopic`/`sortBy`/`dayRange` **and every `keyword`/`minPlaytimeHours`/`reviewsAfter`/`reviewsBefore` filter** — all of them decide what "new" means, so changing any of them gives you a fresh baseline rather than a silently wrong one. Delete the record to start over; use different labels to watch several filter sets in parallel.

Details worth knowing:

- **Use `sortBy: "recent"`** (the default). `sortBy: "all"` (helpfulness) and `sortBy: "funny"` (funny votes) are not chronological orderings, so a brand-new review isn't necessarily inside the scanned window and can be missed; the run logs a warning if you watch with either of them anyway.
- **`maxReviewsPerApp` is your scan-depth budget on incremental runs and is left exactly as you set it** — with `recent`, new reviews sort to the top, so your own cap doesn't hide them. If every matching review inside that window turned out to be new, the run warns you that reviews posted since the last run may sit further back — raise `maxReviewsPerApp` or run the watch more often.
- `maxReviewsPerApp` and `maxResults` are **not** part of the fingerprint (they are budgets, not filters), and neither are `includeGameInfo`/`includePlayerCount` (they change a row's contents, never which reviews count as new).
- If a `searchTerms` query resolves to a *different* game than last time, that game is baselined on the spot rather than having its entire review history delivered as "new".
- If Steam serves an incomplete review response for a game (see the FAQ below), that game is **not** baselined and the run says so — you never end up with a baseline built from an upstream fault.
- Watch mode applies to `dataType: "reviews"` only. In `games` mode a row is the same snapshot of the same game on every run, not a stream of new events, so `watchLabel` is ignored with a warning.
- **Baseline size cap:** the saved baseline holds at most 40,000 review ids across all your `apps`/`searchTerms` (the oldest drop off first). A watch this large is rare, but if it happens, the dropped ids will be delivered and **charged again** as "new" on a future run — the run's log and status message name the count when it occurs. Split a very large watch across several labels (e.g. one per game) to stay under the cap.

### Example input

```json
{
  "dataType": "reviews",
  "apps": ["https://store.steampowered.com/app/1145360/Hades/"],
  "maxReviewsPerApp": 200,
  "language": "english",
  "reviewType": "negative",
  "minPlaytimeHours": 5,
  "keyword": "crash"
}
```

## Output

### Review row (`dataType: "reviews"`)

```json
{
  "type": "review",
  "appId": 1145360,
  "reviewId": "234888482",
  "review": "Best roguelike I have ever played, and the story actually lands.",
  "language": "english",
  "recommended": true,
  "createdAt": "2026-09-10T03:35:39.000Z",
  "updatedAt": "2026-09-10T03:37:38.000Z",
  "votesUp": 0,
  "votesFunny": 0,
  "weightedVoteScore": 0.5,
  "commentCount": 0,
  "steamPurchase": true,
  "receivedForFree": false,
  "writtenDuringEarlyAccess": false,
  "refunded": false,
  "steamDeck": false,
  "playtimeForeverHours": 3.9,
  "playtimeAtReviewHours": 3.9,
  "playtimeLastTwoWeeksHours": 3.7,
  "authorSteamId": "76561197974061804",
  "authorName": "BobbyRunout",
  "authorProfileUrl": "https://steamcommunity.com/id/BobbyRunout/",
  "authorNumGamesOwned": 1180,
  "authorNumReviews": 100,
  "authorLastPlayedAt": "2026-09-13T04:15:54.000Z",
  "reviewUrl": "https://steamcommunity.com/profiles/76561197974061804/recommended/1145360/",
  "hardwareOs": "Windows 11",
  "hardwareCpu": "13th Gen Intel(R) Core(TM) i7-13620H",
  "hardwareGpu": "NVIDIA GeForce RTX 4050 Laptop GPU",
  "hardwareRamMb": 16008,
  "hardwareVramMb": 5920,
  "gameName": "Hades",
  "developers": ["Supergiant Games"],
  "publishers": ["Supergiant Games"],
  "genres": ["Action", "Indie", "RPG"],
  "releaseDate": "Sep 17, 2020",
  "storeUrl": "https://store.steampowered.com/app/1145360/",
  "scrapedAt": "2026-09-10T06:03:39.139Z"
}
```

### Game row (`dataType: "games"`)

```json
{
  "type": "game",
  "appId": 367520,
  "name": "Hollow Knight",
  "appType": "game",
  "storeUrl": "https://store.steampowered.com/app/367520/",
  "isFree": false,
  "priceCurrency": "GBP",
  "price": 12.79,
  "priceInitial": 12.79,
  "discountPercent": 0,
  "releaseDate": "24 Feb, 2017",
  "developers": ["Team Cherry"],
  "publishers": ["Team Cherry"],
  "genres": ["Action", "Adventure", "Indie"],
  "platforms": ["windows", "mac", "linux"],
  "metacriticScore": 90,
  "reviewScoreDesc": "Overwhelmingly Positive",
  "totalReviews": 560648,
  "totalPositive": 543211,
  "totalNegative": 17437,
  "positivePercent": 96.9,
  "currentPlayers": 4132,
  "country": "gb"
}
```

### Owner estimates & tags (`includeOwnerEstimates: true`)

Six extra fields are added to each game row. Real output for Hades (`1145360`):

```json
{
  "ownersEstimate": "5,000,000 .. 10,000,000",
  "ownersMin": 5000000,
  "ownersMax": 10000000,
  "peakConcurrentYesterday": 2253,
  "steamSpyTags": ["Action Roguelike", "Rogue-lite", "Hack and Slash", "Indie", "Mythology"],
  "steamSpyTagVotes": { "Action Roguelike": 1330, "Rogue-lite": 954, "Hack and Slash": 936 }
}
```

`steamSpyTags` is ordered by vote count, highest first, and `steamSpyTagVotes` gives the raw votes behind it. These come from the free public [SteamSpy](https://steamspy.com) API — Steam's own store API exposes none of them. One extra request per game, paced to SteamSpy's 1 request/second limit, and **no extra charge**: the fields ride along on the game row you are already paying for.

## FAQ

**How accurate are the owner estimates, and why is there no playtime estimate?**
`ownersEstimate` is a bucketed range (e.g. `"5,000,000 .. 10,000,000"`), not a precise number — that is how SteamSpy publishes it, and `ownersMin`/`ownersMax` are just that string parsed into integers so you can sort and filter on it. There is deliberately **no playtime estimate**: SteamSpy's `average_forever` / `median_forever` / 2-week playtime fields return a flat `0` for every game we checked (verified 2026-09-18 across Dota 2, CS:GO, Cyberpunk 2077, Stardew Valley, Monster Hunter Wilds, Call of Duty MWII and Schedule I), because Valve stopped exposing the profile data they were derived from. We don't ship a field that is always zero. If you want real playtime, use `dataType: "reviews"` — `playtimeForeverHours` and `playtimeAtReviewHours` are per-reviewer numbers that come straight from Steam.

**Some rows came back with `ownersEstimate: null` — why?**
SteamSpy didn't have that app. The rest of the row is unaffected — every Steam-sourced field is still complete — and the run log names the App IDs that were missing. It is most common for unreleased apps, non-game items and very new releases. Note that `"0 .. 20,000"` is a **real** bucket for a genuinely small game, not a "no data" marker; when SteamSpy has nothing the Actor returns `null` rather than passing that floor through as if it were an estimate.

**Do I need a Steam API key or a proxy?**
No. This Actor only reads Steam's public store endpoints over plain HTTP. No login, no key, no residential proxy, so runs are fast and cheap.

**Can I get *all* reviews of a huge game?**
Yes — the Actor paginates with Steam's review cursor. Set `maxReviewsPerApp` (up to 5000 per game) and `maxResults` for the overall cap. Remember you are charged per row returned, so set both deliberately.

**Why did I get fewer reviews than `maxReviewsPerApp`?**
`maxReviewsPerApp` is a **scan cap**, not a match count — it stops Steam pagination after that many reviews have been looked at, and `keyword`/`minPlaytimeHours` are applied *after* that, per review. So a narrow filter combined with a low cap can miss real matches sitting deeper in the feed: on Dota 2 (appId `570`) with `keyword: "toxic"`, `maxReviewsPerApp: 20` scans 20 reviews and keeps 0, but raising it to `50` finds 1 and `200` finds 2 — the matches were always there, just unscanned. When this happens the log carries a `WARN` naming the cap and how many scanned reviews were dropped, and the run's status message says the same — raise `maxReviewsPerApp` to search deeper. (`reviewsAfter`/`reviewsBefore` don't have this problem: newest-first paging stops cleanly at the date boundary instead of relying on the scan cap.) Filtered-out reviews are **not** charged either way.

**I searched for an accented word (like "très" or "café") and got zero results even though I can see matching reviews in the Steam UI — why?**
This was a real bug, fixed in v0.1.16. `keyword` is matched with a plain substring check, and Unicode represents the same accented letter two different ways — "composed" (`é` as one code point) and "decomposed" (`e` + a separate accent mark) — which look identical but don't string-match each other. Verified live on CS2 (appId `730`, French reviews): searching `"très"` typed in composed form returned 24 matches, the same query typed in decomposed form returned 0, even though both are the same word. `keyword` (and the review text it's matched against) are now Unicode-normalized before comparing, so it no longer matters which form you type.

**How is `webhookUrl` different from Apify's own platform webhooks?**
Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `summary` — see the `RUN_SUMMARY` entry below — and, if `watchLabel` is set, `watchSeeding`/`watchNewCount`/`watchSkipped`) once the run finishes and every row has already been pushed and charged. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

**Is there a machine-readable record of whether a run got everything, or stopped short?**
Yes — every run writes a `RUN_SUMMARY` record to its key-value store (`GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY`, no webhook needed). It carries `delivered`, `complete` (a boolean — a run can SUCCEED and still be short), and when `complete` is `false`, `incompleteReason` — one of `upstream-error` (Steam had an outage), `charge-limit`, `max-results`, `seed-cap` (watch baseline capped before finishing), `upstream-degraded` (some apps hit a Steam data fault, others delivered fine), `depth-cap` (`maxReviewsPerApp` was hit while a filter was still discarding matches) or `watch-saturated` (the whole scanned window was new — older new reviews may sit unread) — plus `incompleteDetail` with the specifics. Watch-mode runs also carry `baselineSaved`/`baselineSize`/`baselineTruncated`. A run that hits an upstream fault on every app no longer fails silently mid-script: the error is recorded, the watch baseline and `RUN_SUMMARY` are still written, and only then does the run end FAILED — so a failed incremental run's baseline still reflects every row it already delivered and charged.

**I'm watching a game and a review I already got paid for is coming back again — is that a bug?**
No — it's `recommendationChanged`. Steam keeps a review's id stable when its author edits it in place, and editing is exactly how a player flips their own thumbs-up/thumbs-down (verified live 2026-09-26: real reviews on appId `570` show the same `recommendationid` with `timestamp_updated` well after `timestamp_created`). A watch baseline built before this feature existed carries no recommendation state, so `recommendationChanged` only starts firing from the *second* run after you get it — the log says so explicitly. Set `watchEvents: ["new"]` if you never want to pay for a flip, only for genuinely new reviews.

**What is `sortBy: "funny"` and how is it different from `all`?**
It's Steam's fourth review ordering — the "Funny" tab on a store page's review list, ranked by funny votes rather than helpfulness. It returns a genuinely different set of reviews, not a re-sort of the same ones: on Dota 2 the top funny reviews have 5,000–15,000 funny votes each and date from 2013–2017, while the top *helpful* reviews are from the last 30 days with double-digit funny votes. Use it to pull a game's best-known community jokes and copypastas (community-management, marketing and meme-research work) rather than its buying-decision feedback. Two things to know: it is **always all-time** (Steam offers no date control for it, so `dayRange` is ignored and the run says so), and it is not chronological, so it's a poor choice for watch mode.

**Does `dayRange` work with the "most recent" sort?**
No — Steam only honours a day range in its helpfulness ranking, so set `sortBy: "all"` when you use `dayRange`. Verified against Steam's API: in the other three modes `dayRange` changes nothing at all, so this Actor withholds it and logs a warning instead of letting you believe a window was applied. For any other historical window, use `reviewsAfter`/`reviewsBefore` instead — the Actor forces chronological order and sends the window straight to Steam's own date filter, so it works arbitrarily far back, not just the last 365 days.

**Can I pull reviews from a specific week/month years ago, like a launch controversy?**
Yes — set `reviewsAfter` and `reviewsBefore` to that exact window (e.g. `"2024-01-15"` / `"2024-02-01"`). Steam's public UI only exposes a rolling `dayRange` capped at 365 days (the helpfulness sort), but its review API itself accepts a real date-range filter (`start_date`/`end_date`) that this Actor sends server-side whenever `reviewsAfter`/`reviewsBefore` is set — Steam does the filtering on its end instead of us paging back from today and discarding everything outside your window, so a narrow window years back is fast even on a huge game.

**I set `sortBy: "all"` and got way fewer reviews than expected — why?**
Steam silently caps its helpfulness ranking to the **last 30 days** if you don't also set `dayRange`. For a true all-time "most helpful" pull, set `dayRange: 365` explicitly alongside `sortBy: "all"`.

**My search term matched a soundtrack or DLC, not the game — is that a bug?**
No, that's Steam's own search behaviour: `storesearch` returns soundtracks and some DLC as regular `type: "app"` results alongside the base game. If you're using `searchTerms`, check the `name`/`appId` in your results, or switch to `apps` with the exact App ID to avoid ambiguity.

**Which languages can I ask for?**
Any Steam language code: `english`, `schinese`, `tchinese`, `japanese`, `koreana`, `russian`, `german`, `french`, `spanish`, `latam`, `brazilian`, `polish`, `turkish`, `italian`, `thai`, `vietnamese`, … or `all`.

**What happens if a game is delisted or region-locked?**
The run finishes successfully with a clear status message naming the App IDs Steam returned nothing for, instead of failing. You are only charged for rows you actually receive.

**Do reviews say whether they were written on Steam Deck, or when the reviewer last played?**
Yes — every review row includes `steamDeck` (true if the review was primarily written on Steam Deck) and `authorLastPlayedAt` (ISO timestamp of the author's last session in the game), straight from Steam's own review API.

**My run returned zero reviews for a game I know has thousands. What happened?**
Steam's review API occasionally serves an incomplete response — HTTP 200, `success: 1`, but no reviews and no review totals — for hours at a time, across games and IP ranges. The Actor recognises that specific shape, retries it twice with a delay, and if Steam is still returning it, **fails the run with a status message naming the upstream fault** rather than quietly reporting "no reviews found". So a zero-row *successful* run always means your filters or the game, never a silent Steam outage — and since billing is per row, a degraded run costs you nothing. Just re-run it later.

**Can I see the reviewer's PC specs?**
When Steam has them, yes: `hardwareOs`, `hardwareCpu`, `hardwareGpu`, `hardwareRamMb`, `hardwareVramMb` come straight from the reviewer's Steam Hardware Survey opt-in, attached to the review itself. It's only present on a minority of reviews (roughly 1 in 5–25, game-dependent) — everyone else gets `null` on all five fields, never a guess. No other Steam reviews Actor exposes this.

**A row came back with fewer fields than usual, or `ownersEstimate`/review totals were null when they shouldn't be — could that be a transient network blip?**
It used to be able to. Every request to Steam and SteamSpy now retries automatically (up to 3 attempts, short backoff) on a connection-establishment fault before giving up, not just once. Before this, a single dropped connection on one of these secondary calls silently shipped that row with a missing field and only a log warning — the run still succeeded, you just got less than you paid for. A field is still `null` when Steam/SteamSpy genuinely has nothing to say (see the two FAQ entries above), never as a side effect of a network hiccup.

---

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/steam-reviews-scraper
More tools: [fetchsmith.com](https://fetchsmith.com/tools) · Built and maintained with AI assistance.

## Related guides
Engineering write-ups behind this Actor:
- [Steam's review API is public JSON — but three of its silences look identical](https://fetchsmith.com/blog/steam-reviews-public-json-api)
- [Steam quietly attaches a reviewer's PC specs to their review — for about 1 in 15](https://fetchsmith.com/blog/steam-review-hardware-specs-json-field)
- [Four ways an invisible character makes a scraper return zero rows](https://fetchsmith.com/blog/invisible-characters-return-zero-rows)
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for.
- [App Store, Google Play and Steam reviews — three JSON APIs, three unrelated meanings of "empty"](https://fetchsmith.com/blog/app-store-review-apis-three-silent-empties) — how this Actor's specific silent-empty failure mode compares to the other two review platforms we scrape.
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — the fleet-wide survey of watch-mode failure shapes across all nineteen incremental Actors, this one included.

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools)
