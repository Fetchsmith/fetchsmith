# Steam Reviews Scraper

Scrape **Steam player reviews** and **Steam store data** into JSON, CSV or Excel — no login, no browser, no proxy needed.

Give it Steam store URLs, numeric App IDs, or just game names to search for. You get every review with its full text, the reviewer's **playtime**, whether they recommend the game, helpfulness votes, whether it was a real Steam purchase, and (optionally) the game's name, developer, publisher, genres and release date attached to every row.

**Pay per result: $0.000575 per review or game record on the free plan, dropping to $0.0003 on Gold and above** (Bronze $0.0005, Silver $0.00039). **No start fee** — a run that returns nothing costs nothing.

## What you can do with it

- **Track sentiment after a patch or a price change** — pull reviews sorted by most recent, filter to `negative`, and diff week over week.
- **Find bug reports in the wild** — set `keyword` to `crash`, `stutter`, `controller` or `refund` and get only the reviews that mention it.
- **Filter out drive-by reviews** — `minPlaytimeHours: 10` keeps only reviewers who actually played the game.
- **Pull reviews from an exact historical window** — `reviewsAfter`/`reviewsBefore` (e.g. a specific patch, a controversy, a launch week years ago) reach any point in a game's history, not just the last year.
- **Competitive research** — `dataType: "games"` returns price, discount, genres, developer, Metacritic score, the full review-score summary (total positive/negative, % positive) and, optionally, the **live concurrent player count**.
- **Localised research** — `language: "schinese"`, `"russian"`, `"brazilian"` … or `"all"` for every language at once.
- **Feed an LLM / dataset pipeline** — clean flat rows, stable `reviewId`, ISO-8601 timestamps.

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
| `sortBy` | string | `recent` | `recent`, `updated`, or `all` (Steam's helpfulness ranking) |
| `dayRange` | integer | — | With `sortBy: "all"`, restrict to the last N days (1–365) |
| `reviewsAfter` | string | — | ISO date (`2024-01-01`) — keep only reviews created on/after this date. Reaches any point in history, forces `sortBy` to `recent`. |
| `reviewsBefore` | string | — | ISO date — keep only reviews created before this date. Combine with `reviewsAfter` for an exact window. |
| `minPlaytimeHours` | integer | — | Keep only reviewers with at least this many hours in the game |
| `keyword` | string | — | Keep only reviews whose text contains this word/phrase |
| `country` | string | `us` | Two-letter code for store prices and availability |
| `includeGameInfo` | boolean | `true` | Attach game name/developer/publisher/genres/release date to every review |
| `includePlayerCount` | boolean | `false` | `games` mode: also fetch the live concurrent player count |
| `searchLimit` | integer | `10` | Games taken from each search term |

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

## FAQ

**Do I need a Steam API key or a proxy?**
No. This Actor only reads Steam's public store endpoints over plain HTTP. No login, no key, no residential proxy, so runs are fast and cheap.

**Can I get *all* reviews of a huge game?**
Yes — the Actor paginates with Steam's review cursor. Set `maxReviewsPerApp` (up to 5000 per game) and `maxResults` for the overall cap. Remember you are charged per row returned, so set both deliberately.

**Why did I get fewer reviews than `maxReviewsPerApp`?**
`maxReviewsPerApp` is a **scan cap**, not a match count — it stops Steam pagination after that many reviews have been looked at, and `keyword`/`minPlaytimeHours` are applied *after* that, per review. So a narrow filter combined with a low cap can miss real matches sitting deeper in the feed: on Dota 2 (appId `570`) with `keyword: "toxic"`, `maxReviewsPerApp: 20` scans 20 reviews and keeps 0, but raising it to `50` finds 1 and `200` finds 2 — the matches were always there, just unscanned. When this happens the log carries a `WARN` naming the cap and how many scanned reviews were dropped, and the run's status message says the same — raise `maxReviewsPerApp` to search deeper. (`reviewsAfter`/`reviewsBefore` don't have this problem: newest-first paging stops cleanly at the date boundary instead of relying on the scan cap.) Filtered-out reviews are **not** charged either way.

**I searched for an accented word (like "très" or "café") and got zero results even though I can see matching reviews in the Steam UI — why?**
This was a real bug, fixed in v0.1.16. `keyword` is matched with a plain substring check, and Unicode represents the same accented letter two different ways — "composed" (`é` as one code point) and "decomposed" (`e` + a separate accent mark) — which look identical but don't string-match each other. Verified live on CS2 (appId `730`, French reviews): searching `"très"` typed in composed form returned 24 matches, the same query typed in decomposed form returned 0, even though both are the same word. `keyword` (and the review text it's matched against) are now Unicode-normalized before comparing, so it no longer matters which form you type.

**Does `dayRange` work with the "most recent" sort?**
No — Steam only honours a day range in its helpfulness ranking, so set `sortBy: "all"` when you use `dayRange`. For any other historical window, use `reviewsAfter`/`reviewsBefore` instead — the Actor forces chronological order and stops paging as soon as it passes your window, so it works arbitrarily far back, not just the last 365 days.

**Can I pull reviews from a specific week/month years ago, like a launch controversy?**
Yes — set `reviewsAfter` and `reviewsBefore` to that exact window (e.g. `"2024-01-15"` / `"2024-02-01"`). Steam's own API has no such filter (only a rolling `dayRange` capped at 365 days for the helpfulness sort); this Actor gets there by paging newest-first and stopping the instant it's past your window, so a narrow window years back is cheap even on a huge game.

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

---

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/steam-reviews-scraper
More tools: [fetchsmith.com](https://fetchsmith.com/tools) · Built and maintained with AI assistance.

## Related guides
Engineering write-ups behind this Actor:
- [Steam's review API is public JSON — but three of its silences look identical](https://fetchsmith.com/blog/steam-reviews-public-json-api)
- [Steam quietly attaches a reviewer's PC specs to their review — for about 1 in 15](https://fetchsmith.com/blog/steam-review-hardware-specs-json-field)
- [Four ways an invisible character makes a scraper return zero rows](https://fetchsmith.com/blog/invisible-characters-return-zero-rows)

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools)
