# Apple Podcasts Scraper — Episodes, Reviews, Search, Charts & Podcast Publishers

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
| `dataType` | string | `episodes` (default), `reviews`, `podcasts` (show records), `charts` (today's top shows or trending episodes, see `chartType` — no `podcasts`/`searchTerms` needed), or `publisher` (every show by a publisher/artist) |
| `podcasts` | array | Apple Podcasts show URLs/IDs, e.g. `https://podcasts.apple.com/us/podcast/lex-fridman-podcast/id1434243584`. For `dataType: "publisher"`, give the publisher's artist URL/ID instead, e.g. `https://podcasts.apple.com/us/artist/the-new-york-times/121664449`. **You can also paste a direct RSS/podcast feed URL** for any show — including ones not indexed by Apple at all — but only with `dataType: "episodes"`, since the feed itself has no Apple ID for reviews/search/charts |
| `searchTerms` | array | Find shows by keyword instead of, or as well as, giving URLs |
| `searchLimit` | integer | Shows to take per search term (default 10, max 200) |
| `chartType` | string | Charts only: `shows` (default — Apple's Top Shows chart) or `episodes` (Apple's separate **Trending Episodes** chart: one row per episode, with audio URL, duration and release date) |
| `chartCount` | integer | Charts only: how many chart entries to fetch (default 50). Apple caps the overall charts (Top Shows, Trending Episodes) at **100** and a genre chart at 200; higher values are clamped with a warning |
| `chartGenre` | string | Charts only: restrict the Top Shows chart to one category (`comedy`, `trueCrime`, `news`, `business`, ... 19 total) instead of the overall top chart. Leave empty for the overall chart. Ignored for `chartType: "episodes"` — Apple publishes no per-genre episode chart |
| `maxPodcastsPerPublisher` | integer | Publisher only: how many shows to return per publisher (default 200, max 200) |
| `country` | string | Storefront code — `us` (default), `gb`, `de`, `jp`, ... Reviews, availability and charts differ per storefront |
| `maxEpisodesPerPodcast` | integer | Up to 200 most recent episodes per show (Apple's limit) — up to 20,000 with `useRssForFullArchive` (default 100). On Apple's API it counts episodes **fetched** (it is the API's own limit, so the other filters narrow within them); on RSS the whole feed arrives in one request, so it counts episodes **kept** after filtering and a date window can match anywhere in the archive |
| `useRssForFullArchive` | boolean | Episodes only: fetch the show's own RSS feed instead of Apple's lookup API to get the **complete episode archive**, not just the most recent ~200 (default `false`; verified live: a real feed returned 502 episodes vs. Apple's 200-episode ceiling for the same show). Also unlocks `episodeType`, `showNotesHtml`, `audioFileSize` and `transcriptUrl` — fields Apple's own API never exposes. Falls back to Apple's lookup API for any show without a usable feed |
| `maxReviewsPerPodcast` | integer | Up to 500 reviews per show per storefront (Apple's limit), though **in practice Apple's feed usually serves fewer** — see FAQ. Counts reviews **scanned**, before `minRating`/`maxRating`/`keyword` filtering |
| `sort` | string | Reviews only: `mostRecent` (default) or `mostHelpful` |
| `includePodcastInfo` | boolean | Attach show name, host, genre, RSS feed and episode count to every row (default `true`) |
| `maxResults` | integer | Overall cap across all shows — also caps what you pay |
| `minRating` / `maxRating` | integer | Reviews only: keep reviews rated within 1-5 |
| `keyword` | string | Reviews only: keep reviews whose title or text contains this word/phrase |
| `minReleaseDate` / `maxReleaseDate` | string | Episodes only: keep episodes released in this window (`YYYY-MM-DD` or full ISO). This narrows *within* the `maxEpisodesPerPodcast` most-recent episodes Apple returns, not further back into a show's archive — enable `useRssForFullArchive` to search the whole archive instead, where `maxEpisodesPerPodcast` caps matches kept rather than episodes walked, so a window years back still returns rows. If a whole-archive walk matches nothing, the run log names the feed's real first/last episode dates so you can widen the window to fit |
| `minDurationSeconds` | integer | Episodes only: drop episodes shorter than this (e.g. exclude trailers/ads). **Apple omits duration for ~half of episodes on some shows regardless of actual length** (measured on a real 20-episode sample) — episodes with unknown duration are always kept, never assumed short |
| `explicitFilter` | string | Episodes only: `all` (default), `clean` (exclude Explicit-flagged), or `explicitOnly`. **The flag is read from whichever source the run uses** — Apple's Store rating by default, or the feed's own `<itunes:explicit>` tag (per episode, else show-level) when `useRssForFullArchive` is on. Real feeds disagree with Apple: the Lex Fridman feed carries no per-episode tag at all and declares the show `false` at channel level, while Apple rates those same episodes Explicit, so `explicitOnly` returns rows via Apple and none via RSS (measured 2026-09-18). The run log warns when this applies |
| `webhookUrl` | string | Optional http(s) URL to POST a small JSON completion summary to (items pushed, dataType, dataset ID, and — if `watchLabel` is set — `watchSeeding`/`watchSkippedCount`/`baselineTruncated`/`baselineTruncatedTotal`) — a convenience ping without setting up an Apify platform webhook. Best-effort: a failed or slow webhook is logged as a warning and never affects the run or your bill |
| `watchLabel` | string | Episodes only: name a saved watch (e.g. `"daily-check"`) and this run returns **only episodes not delivered under that label before**, instead of every episode every time. The first run for a label is a free baseline (0 rows, 0 charged) that records what already exists; run it again later — on a schedule — to get only what's new. Changing any other filter starts a fresh baseline instead of re-delivering previously-excluded episodes as "new". An episode **older than the deepest point the baseline reached** is also never billed as new: if a later run gets further back into a show's archive than the baseline did (Apple's lookup caps at 200 episodes, and an RSS full-archive fetch can fail), those older episodes are recognised as pre-existing — not delivered, not charged — and the run says how many. Episodes published after the baseline are always newer than that date, so real alerts are never suppressed |

Filtering happens **before** you're charged — you never pay for rows a filter removed.

### Example: get notified only about new episodes (run on a schedule)
```json
{
  "podcasts": ["https://podcasts.apple.com/us/podcast/lex-fridman-podcast/id1434243584"],
  "dataType": "episodes",
  "watchLabel": "lex-daily",
  "webhookUrl": "https://your-server.example.com/new-episode"
}
```
The first run seeds the baseline (0 rows, 0 charged). Every run after that returns only episodes published since the previous run — pair with `webhookUrl` to get pinged the moment a new episode lands, without polling the full archive yourself.

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
  "episodeType": null,
  "showNotesHtml": null,
  "audioFileSize": null,
  "keywords": null,
  "transcriptUrl": null,
  "source": "itunes",
  "artistName": "Lex Fridman",
  "primaryGenre": "Technology",
  "episodeCount": 502
}
```
`episodeType`, `showNotesHtml`, `audioFileSize` and `transcriptUrl` are only populated when `useRssForFullArchive` is on and the show's feed provides them (`source` reads `"rss"` instead of `"itunes"` for those rows) — Apple's own lookup API has no equivalent fields.

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

**`dataType: "charts"`** — with the default `chartType: "shows"`, the same shape as `podcasts`, plus `chartRank` (1 = #1 in the storefront). Set `includePodcastInfo:false` to skip the per-show detail lookup and get just the raw chart fields (name, artist, genre, artwork, URL) faster.

**`dataType: "charts"` + `chartType: "episodes"`** — the same shape as `episodes` (title, `releaseDate`, `durationMinutes`, `description`, direct `episodeUrl` audio file, `episodeGuid`, `feedUrl`, show metadata), plus `chartRank`. The episode filters apply here too (`explicitFilter`, `minDurationSeconds`, `minReleaseDate`/`maxReleaseDate`), and filtered-out entries are never charged, so ranks can legitimately have gaps.

**`dataType: "publisher"`** — same shape as `podcasts`, plus `publisherId` (the artist ID you gave). One item per show the publisher runs.

## FAQ

**What country codes does `country` take?** Apple storefronts are two-letter ISO-3166-1 **alpha-2** codes — the UK is `gb`, not `uk`, and there is no `usa`/`uk`/`eng`. A wrong code used to look like a show that doesn't exist (Apple answers `uk` with `HTTP 400` carrying valid JSON and no results, and the review feed with an empty body); now a recognisable wrong code fails the run in about a second, before the first request and before any charge, and names the code you should have used.
**How do I find a publisher's artist ID?** It's the trailing number on their "See All" / artist page on podcasts.apple.com (e.g. `.../artist/the-new-york-times/121664449`), or run `dataType: "podcasts"` for any one of their shows first — the search/lookup result carries `artistId` even though this Actor doesn't surface it by default on `podcasts` rows (open a request if you need it added).
**Does `keyword` handle accented words correctly?** Yes, as of v0.1.16 — `keyword` and the text it's matched against are Unicode-normalized before comparing, so an accented word (e.g. "café") matches regardless of which of Unicode's two equivalent representations (composed vs. decomposed) you typed it in.

**Do I need an Apple account or API key?** No. Everything comes from Apple's public podcast endpoints. No login, no browser, no proxy required.

**Why did I get zero results?** The run's status message says exactly why. The usual causes: the show isn't available in the `country` storefront you asked for (try `us`), Apple has no reviews for that show in that storefront (reviews are per-storefront — a show can have hundreds in `us` and none in `de`), or the ID wasn't an Apple Podcasts ID.

**Why did I get fewer reviews than `maxReviewsPerPodcast`, or exactly zero with `minRating`/`maxRating`/`keyword` set?** `maxReviewsPerPodcast` is a scan-depth cap, not a results cap — it's how many of the show's most-recent reviews get read from Apple's feed before your rating/keyword filter is applied, not how many matching reviews exist. A rare keyword can sit past the reviews you scanned. Example: The Joe Rogan Experience + `keyword:"propaganda"` returns 0 kept reviews at `maxReviewsPerPodcast:50` (only page 1 scanned) but 2 at `maxReviewsPerPodcast:100` (page 2 scanned) — the run log and status message call this out by name when it happens, telling you to raise `maxReviewsPerPodcast`. That advice only applies when **your** cap ended the scan; when Apple's feed ended it (next FAQ), raising the cap changes nothing and the run says so instead.

**Why did I get 50 reviews for a show with thousands?** Because Apple stopped serving, not because the show ran out. Apple's public review RSS is served from a patchy index: measured 2026-09-22, the walk commonly ends on a full page long before the documented 500-review/10-page ceiling — Crime Junkie in the `gb` storefront returned exactly 50 (one full page, nothing on page 2) at `maxReviewsPerPodcast: 500`. **No input value reaches the reviews behind that wall**, so raising `maxReviewsPerPodcast` is not the fix; ask for other `country` storefronts (reviews are per-storefront), or run on a schedule and deduplicate by `reviewId` to build a deeper archive over time.

**How do I know whether Apple cut the feed off or the show simply has no more reviews?** The run tells you, as of v0.1.37. Whenever the last page Apple served came back **full** while the Actor was still willing to take more, the run's status message and log name those shows and say which page the feed quit at. A run that ends on a **partial** page genuinely exhausted what Apple serves for that show and storefront — so a *missing* note is itself the "you got everything available" signal. Either way you are only charged for rows actually delivered.

**How many episodes can I get?** Apple's endpoint exposes up to 200 of the most recent episodes per show. For the complete back catalogue, set `useRssForFullArchive: true` — the Actor fetches the show's own RSS feed directly instead (verified live on a real show: 502 episodes vs. Apple's 200-episode cap for the same ID).

**Can I scrape a show that isn't on Apple Podcasts, or that I can't find by search?** Yes — paste its RSS feed URL directly into `podcasts` instead of an Apple URL/ID, with `dataType: "episodes"`. The Actor reads the feed itself, so no Apple lookup happens at all (verified live: a non-Apple-searched NPR feed returns full episode rows this way). Reviews, search and charts still need a real Apple ID, since that data only exists on Apple's side.

**How fast is it?** HTTP-only, no headless browser: a show's 200 episodes come from a single request, and reviews page 50 at a time. Runs cost a few seconds of compute plus the per-result fee.

**Can I chart individual episodes, not just shows?** Yes — `dataType: "charts"` with `chartType: "episodes"` returns Apple's **Trending Episodes** chart, which is a different chart from Top Shows, not a view of it (on the 2026-09-17 US chart, the #1 *show* was The Daily while the #1 *episode* was one specific Daily episode, and ranks 2-12 were episodes of eleven different shows). Each entry is enriched into a full episode row — audio URL, duration, release date, description — via one cached lookup per show. Two limits worth knowing: Apple's episode chart has no genre breakdown (`chartGenre` is ignored, with a warning), and Apple-exclusive/subscriber-only shows publish no episode list at all, so those entries arrive with `source: "chart"` and the chart's own title/artwork instead of full episode detail rather than being dropped (measured 19 of 20 entries fully enriched on a real US chart).

**Can I get genre-specific charts?** Yes — set `chartGenre` (e.g. `comedy`, `trueCrime`, `business`) to get that category's own top chart instead of the overall one, using Apple's own per-genre chart feed. 19 genres are supported; an unrecognized value is ignored with a warning rather than silently returning the wrong chart.

**What happens if Apple's endpoint has a transient blip mid-run?** Every lookup, search, review-feed and RSS request is retried up to 3 times on a connection-level failure (measured at roughly 1 fresh connection in 4 for HTTP/2 faults across this fleet, 2026-09-21) before it is given up on and named in the log. A single blip no longer costs you a whole show's episodes, a page of reviews, or — with `useRssForFullArchive: true` — a silent downgrade back to Apple's 200-episode cap. A real HTTP error from Apple (e.g. a wrong storefront code) still fails immediately with the explanation instead of being retried.

**Is this legal?** It only reads public, unauthenticated Apple endpoints — the same data any visitor sees on podcasts.apple.com. No personal data beyond the public reviewer nicknames Apple itself publishes.

**Baseline size cap.** The recorded `watchLabel` baseline holds at most 60,000 episode ids per label; once a label's cumulative baseline grows past that, the oldest ids are dropped to bound the record's size. A dropped id is treated as "new" again on a later run and re-charged, even though you already paid for it. This only bites a label tracking a very high cumulative volume of episodes over many runs — narrowing the input (fewer podcasts/searchTerms, or a `minReleaseDate`) keeps a baseline well under the cap. A run that actually drops ids says so explicitly in its log and status message, and reports the exact counts as `baselineTruncated`/`baselineTruncatedTotal` in the `webhookUrl` payload.

## Pricing
Pay per result: **$0.001 per row** (episode, review or podcast) returned to your dataset. **No Actor-start fee** — an empty or filtered-out run costs you nothing. Set `maxResults` to cap any run.

---
Built by [FetchSmith](https://fetchsmith.com) — fast, HTTP-only scrapers with honest pricing. Questions or a field you need? Email support@fetchsmith.com.

## Related guides
Engineering write-ups behind this Actor:
- [Apple Podcasts has a public JSON API — four endpoints, no key, and one that doesn't exist](https://fetchsmith.com/blog/apple-podcasts-public-json-api)
- [Four ways an invisible character makes a scraper return zero rows](https://fetchsmith.com/blog/invisible-characters-return-zero-rows)
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for.
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — the fleet-wide survey of watch-mode failure shapes across all nineteen incremental Actors, this one included.
- [Substack, Apple Podcasts, Google News and Hacker News — four free APIs where the first response isn't the finished product](https://fetchsmith.com/blog/public-content-apis-hidden-second-step) — how this Actor's second-step trap compares to the other three content platforms we scrape.

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools)

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/apple-podcasts-scraper
