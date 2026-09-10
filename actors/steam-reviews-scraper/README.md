# Steam Reviews Scraper

Scrape **Steam player reviews** and **Steam store data** into JSON, CSV or Excel — no login, no browser, no proxy needed.

Give it Steam store URLs, numeric App IDs, or just game names to search for. You get every review with its full text, the reviewer's **playtime**, whether they recommend the game, helpfulness votes, whether it was a real Steam purchase, and (optionally) the game's name, developer, publisher, genres and release date attached to every row.

**Pay per result: $0.0005 per review or game record. No start fee** — a run that returns nothing costs nothing.

## What you can do with it

- **Track sentiment after a patch or a price change** — pull reviews sorted by most recent, filter to `negative`, and diff week over week.
- **Find bug reports in the wild** — set `keyword` to `crash`, `stutter`, `controller` or `refund` and get only the reviews that mention it.
- **Filter out drive-by reviews** — `minPlaytimeHours: 10` keeps only reviewers who actually played the game.
- **Competitive research** — `dataType: "games"` returns price, discount, genres, developer, Metacritic score, the full review-score summary (total positive/negative, % positive) and, optionally, the **live concurrent player count**.
- **Localised research** — `language: "schinese"`, `"russian"`, `"brazilian"` … or `"all"` for every language at once.
- **Feed an LLM / dataset pipeline** — clean flat rows, stable `reviewId`, ISO-8601 timestamps.

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `dataType` | string | `reviews` | `reviews` = player reviews; `games` = store record for each game |
| `apps` | array | — | Steam store URLs (`https://store.steampowered.com/app/1145360/Hades/`) or numeric App IDs (`1145360`) |
| `searchTerms` | array | — | Find games by name instead of / as well as URLs |
| `maxReviewsPerApp` | integer | `200` | Reviews per game before moving to the next one (max 5000) |
| `maxResults` | integer | `2000` | Hard cap on rows pushed — also caps what you are charged |
| `language` | string | `english` | Steam language code, or `all` |
| `reviewType` | string | `all` | `positive` / `negative` to keep only thumbs-up / thumbs-down |
| `purchaseType` | string | `all` | `steam` excludes key activations and free weekends |
| `sortBy` | string | `recent` | `recent`, `updated`, or `all` (Steam's helpfulness ranking) |
| `dayRange` | integer | — | With `sortBy: "all"`, restrict to the last N days (1–365) |
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
  "playtimeForeverHours": 3.9,
  "playtimeAtReviewHours": 3.9,
  "playtimeLastTwoWeeksHours": 3.7,
  "authorSteamId": "76561197974061804",
  "authorName": "BobbyRunout",
  "authorProfileUrl": "https://steamcommunity.com/id/BobbyRunout/",
  "authorNumGamesOwned": 1180,
  "authorNumReviews": 100,
  "reviewUrl": "https://steamcommunity.com/profiles/76561197974061804/recommended/1145360/",
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
Either the game genuinely has fewer reviews in that language/filter combination, or your `keyword` / `minPlaytimeHours` filters removed the rest. Filtered-out reviews are **not** charged. The run's status message says which case it was.

**Does `dayRange` work with the "most recent" sort?**
No — Steam only honours a day range in its helpfulness ranking, so set `sortBy: "all"` when you use `dayRange`. The other sorts are already chronological, so filter by `createdAt` on your side instead.

**Which languages can I ask for?**
Any Steam language code: `english`, `schinese`, `tchinese`, `japanese`, `koreana`, `russian`, `german`, `french`, `spanish`, `latam`, `brazilian`, `polish`, `turkish`, `italian`, `thai`, `vietnamese`, … or `all`.

**What happens if a game is delisted or region-locked?**
The run finishes successfully with a clear status message naming the App IDs Steam returned nothing for, instead of failing. You are only charged for rows you actually receive.

---

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/steam-reviews-scraper
More tools: [fetchsmith.com](https://fetchsmith.com/tools) · Built and maintained with AI assistance.
