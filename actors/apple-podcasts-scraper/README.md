# Apple Podcasts Scraper — Episodes, Reviews, Search, Charts & Publishers

Scrape Apple Podcasts without a browser or login: **every episode** of a show (title, release date, duration, description, direct audio URL, RSS feed), **listener reviews** with star ratings, **search Apple's podcast catalogue** by keyword, pull **today's top-charts** for any storefront, or list **every show a publisher runs**. Export to JSON, CSV or Excel. Pay only per row returned.

Episodes, reviews and search live in **one Actor**, so you can go from "podcasts about AI" to "every 1-star review those shows got" in a single run — and at **$0.001 per row with no per-run start fee**, it costs a fraction of comparable Apple Podcasts Actors (commonly $0.0025–$0.004 per row, several of them with a start fee on top).

## Use cases
- **Podcast guest / sponsor prospecting** — search a topic, get every matching show with its host, genre, episode count and RSS feed.
- **Audience research** — pull listener reviews for you and your competitors and mine them for complaints, praise and topic requests.
- **Content and SEO research** — episode titles + descriptions for a whole niche, ready for keyword analysis.
- **Media monitoring** — schedule the Actor to catch new episodes or new reviews for the shows you track.
- **AI/LLM pipelines** — episode descriptions and reviews as clean JSON, plus `episodeUrl` (the direct audio file) for transcription.
- **Trend tracking** — pull the top-N chart for any storefront on a schedule to see which shows are rising or falling.
- **Network mapping** — give a publisher's Apple Podcasts artist ID and get every show they run (e.g. a media company's whole podcast slate) in one call.

## Input
| Field | Type | Description |
|---|---|---|
| `dataType` | string | `episodes` (default), `reviews`, `podcasts` (show records), `charts` (today's top podcasts — no `podcasts`/`searchTerms` needed), or `publisher` (every show by a publisher/artist) |
| `podcasts` | array | Apple Podcasts show URLs/IDs, e.g. `https://podcasts.apple.com/us/podcast/lex-fridman-podcast/id1434243584`. For `dataType: "publisher"`, give the publisher's artist URL/ID instead, e.g. `https://podcasts.apple.com/us/artist/the-new-york-times/121664449` |
| `searchTerms` | array | Find shows by keyword instead of, or as well as, giving URLs |
| `searchLimit` | integer | Shows to take per search term (default 10, max 200) |
| `chartCount` | integer | Charts only: how many top shows to fetch (default 50, max 200) |
| `maxPodcastsPerPublisher` | integer | Publisher only: how many shows to return per publisher (default 200, max 200) |
| `country` | string | Storefront code — `us` (default), `gb`, `de`, `jp`, ... Reviews, availability and charts differ per storefront |
| `maxEpisodesPerPodcast` | integer | Up to 200 most recent episodes per show (Apple's limit) |
| `maxReviewsPerPodcast` | integer | Up to 500 reviews per show per storefront (Apple's limit) |
| `sort` | string | Reviews only: `mostRecent` (default) or `mostHelpful` |
| `includePodcastInfo` | boolean | Attach show name, host, genre, RSS feed and episode count to every row (default `true`) |
| `maxResults` | integer | Overall cap across all shows — also caps what you pay |
| `minRating` / `maxRating` | integer | Reviews only: keep reviews rated within 1-5 |
| `keyword` | string | Reviews only: keep reviews whose title or text contains this word/phrase |
| `minReleaseDate` / `maxReleaseDate` | string | Episodes only: keep episodes released in this window (`YYYY-MM-DD` or full ISO). This narrows *within* the `maxEpisodesPerPodcast` most-recent episodes Apple returns, not further back into a show's archive |
| `minDurationSeconds` | integer | Episodes only: drop episodes shorter than this (e.g. exclude trailers/ads). **Apple omits duration for ~half of episodes on some shows regardless of actual length** (measured on a real 20-episode sample) — episodes with unknown duration are always kept, never assumed short |
| `explicitFilter` | string | Episodes only: `all` (default), `clean` (exclude Explicit-flagged), or `explicitOnly` |

Filtering happens **before** you're charged — you never pay for rows a filter removed.

### Example: every 1- and 2-star review for the top 5 "meditation" podcasts
```json
{
  "searchTerms": ["meditation"],
  "searchLimit": 5,
  "dataType": "reviews",
  "maxRating": 2,
  "maxReviewsPerPodcast": 200
}
```

## Output

**`dataType: "episodes"`** — one item per episode:
```json
{
  "type": "episode",
  "collectionId": 1434243584,
  "podcastName": "Lex Fridman Podcast",
  "episodeId": 1000786117598,
  "title": "#501 – DHH: Future of Programming, AI, Agentic Engineering...",
  "episodeNumber": null,
  "seasonNumber": null,
  "releaseDate": "2026-08-26T21:47:04Z",
  "durationMs": 19317000,
  "durationMinutes": 322,
  "description": "DHH is the creator of Ruby on Rails...",
  "episodeUrl": "https://media.blubrry.com/.../lex_ai_dhh_2.mp3",
  "episodeFileExtension": "mp3",
  "episodeGuid": "https://lexfridman.com/?p=6506",
  "explicit": true,
  "artworkUrl": "https://is1-ssl.mzstatic.com/image/thumb/...",
  "episodePageUrl": "https://podcasts.apple.com/us/podcast/...",
  "feedUrl": "https://lexfridman.com/feed/podcast/",
  "artistName": "Lex Fridman",
  "primaryGenre": "Technology",
  "episodeCount": 502
}
```

**`dataType: "reviews"`** — one item per review:
```json
{
  "type": "review",
  "collectionId": 1434243584,
  "reviewId": "14514424096",
  "title": "Amazing breadth",
  "content": "I've listened to Lex for many years...",
  "rating": 5,
  "author": "FatBoyTig",
  "updatedAt": "2026-09-05T10:26:18-07:00",
  "voteSum": 0,
  "voteCount": 0,
  "country": "us",
  "podcastName": "Lex Fridman Podcast",
  "artistName": "Lex Fridman",
  "primaryGenre": "Technology"
}
```

**`dataType: "podcasts"`** — one item per show: `collectionId`, `podcastName`, `artistName`, `podcastUrl`, `feedUrl`, `primaryGenre`, `genres`, `episodeCount`, `latestReleaseDate`, `explicit`, `contentAdvisoryRating`, `artworkUrl`, and `searchTerm` when it came from a search.

**`dataType: "charts"`** — same shape as `podcasts`, plus `chartRank` (1 = #1 in the storefront). Set `includePodcastInfo:false` to skip the per-show detail lookup and get just the raw chart fields (name, artist, genre, artwork, URL) faster.

**`dataType: "publisher"`** — same shape as `podcasts`, plus `publisherId` (the artist ID you gave). One item per show the publisher runs.

## FAQ

**How do I find a publisher's artist ID?** It's the trailing number on their "See All" / artist page on podcasts.apple.com (e.g. `.../artist/the-new-york-times/121664449`), or run `dataType: "podcasts"` for any one of their shows first — the search/lookup result carries `artistId` even though this Actor doesn't surface it by default on `podcasts` rows (open a request if you need it added).

**Do I need an Apple account or API key?** No. Everything comes from Apple's public podcast endpoints. No login, no browser, no proxy required.

**Why did I get zero results?** The run's status message says exactly why. The usual causes: the show isn't available in the `country` storefront you asked for (try `us`), Apple has no reviews for that show in that storefront (reviews are per-storefront — a show can have hundreds in `us` and none in `de`), or the ID wasn't an Apple Podcasts ID.

**How many episodes can I get?** Apple's endpoint exposes up to 200 of the most recent episodes per show. For the complete back catalogue of a show, use the `feedUrl` returned on every row — that's the show's public RSS feed.

**How fast is it?** HTTP-only, no headless browser: a show's 200 episodes come from a single request, and reviews page 50 at a time. Runs cost a few seconds of compute plus the per-result fee.

**Can I get genre-specific charts?** No — Apple's public chart endpoint currently only exposes an overall top-podcasts chart per storefront, not per-genre. Each chart row still includes the show's genre(s), so you can filter client-side.

**Is this legal?** It only reads public, unauthenticated Apple endpoints — the same data any visitor sees on podcasts.apple.com. No personal data beyond the public reviewer nicknames Apple itself publishes.

## Pricing
Pay per result: **$0.001 per row** (episode, review or podcast) returned to your dataset. **No Actor-start fee** — an empty or filtered-out run costs you nothing. Set `maxResults` to cap any run.

---
Built by [FetchSmith](https://fetchsmith.com) — fast, HTTP-only scrapers with honest pricing. Questions or a field you need? Email support@fetchsmith.com.

## Related guides
Engineering write-ups behind this Actor:
- [Apple Podcasts has a public JSON API — four endpoints, no key, and one that doesn't exist](https://fetchsmith.com/blog/apple-podcasts-public-json-api)

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools)

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/apple-podcasts-scraper
