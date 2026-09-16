# Hacker News Scraper

Search or browse Hacker News (stories, comments, Ask HN, Show HN, jobs, and monthly **Who's Hiring** threads) using the official Algolia Search API — fast, reliable, no scraping fragility. Pay only per item returned.

## Use cases
- Track mentions of your product, company or keyword on HN
- Pull the current **front page** (live top stories) without a separate feed-crawling mode
- Pull the newest **Who's Hiring** / **Who Wants to Be Hired** threads for job-market research
- Feed trending tech discussions into AI agents, newsletters or dashboards
- Build datasets of Show HN launches or Ask HN discussions by topic
- Look up a founder's or user's HN karma, bio and account age (`usernames`)
- Run a scheduled keyword alert that only ever returns new mentions (`watchLabel`)
- Spot which Show HN launches or technical discussions link to a real, active GitHub repo — with star count, language and last-push date (`enrichGithubLinks`)

## Input
| Field | Type | Description |
|---|---|---|
| `queries` | array | Keywords to search. Leave empty to just browse by tag/date. |
| `tags` | array | `story`, `comment`, `poll`, `ask_hn`, `show_hn`, `job`, `front_page` (default `["story"]`). Several tags are OR-ed: `["story","comment"]` returns both |
| `includeComments` | boolean | Fetch comment text when `tags` includes `comment` |
| `sortBy` | string | `relevance` or `date` (newest first) |
| `minPoints` | integer | Only items with at least this many points |
| `minComments` | integer | Only stories with at least this many comments (find high-engagement discussions) |
| `author` | string | Only items posted by this exact HN username |
| `postedAfter` / `postedBefore` | string | ISO date bounds |
| `maxItemsPerQuery` | integer | Cap per query (up to 1000) |
| `maxResults` | integer | Overall cap |
| `usernames` | array | HN usernames to fetch profile data for (karma, about, account age) — a separate lookup, not a story filter. To fetch ONLY profiles with no story search, also set `queries` and `tags` to `[]`. |
| `watchLabel` | string | Name a saved search to get **only story/comment/job hits new since its last run** — see below |
| `enrichGithubLinks` | boolean | When a result links to a GitHub repo, add star count, primary language, last-push date and open-issue count (default `false`) |

## Output (one item per story/comment)
```json
{
  "id": "41930211",
  "type": "story",
  "title": "Show HN: FetchSmith – pay-per-use scraper APIs",
  "url": "https://fetchsmith.com",
  "hnUrl": "https://news.ycombinator.com/item?id=41930211",
  "author": "someuser",
  "points": 142,
  "numComments": 38,
  "createdAt": "2026-09-01T12:00:00.000Z",
  "query": "fetchsmith",
  "githubRepo": null,
  "githubStars": null,
  "githubLanguage": null,
  "githubPushedAt": null,
  "githubOpenIssues": null
}
```
`githubRepo`/`githubStars`/`githubLanguage`/`githubPushedAt`/`githubOpenIssues` are only populated when `enrichGithubLinks: true` and the item actually links to a GitHub repo (common on Show HN); otherwise they stay `null`.

A `usernames` lookup returns one row per user, `type: "user"`:
```json
{
  "id": "pg",
  "type": "user",
  "author": "pg",
  "hnUrl": "https://news.ycombinator.com/user?id=pg",
  "karma": 157316,
  "about": "Bug fixer.",
  "accountCreatedAt": "2006-10-09T19:41:32.000Z"
}
```

## Watch mode (`watchLabel`)
Name a saved search — `watchLabel: "my-launch-watch"` — and the Actor keeps a per-label record of every story/comment/job hit it has already delivered under that name, so a scheduled run returns **only what is new since last time** and you are charged for nothing else. The first run on a new label is a **free baseline run**: it records what already matches (up to 5000 hits) and returns zero results. Every run after that returns only new items. Change `queries`, `tags`, `author`, `sortBy`, the date range or the point/comment thresholds and the label starts a fresh baseline, instead of dumping everything the old narrower filter excluded as "new". `usernames` profile lookups are unaffected — they run and are charged normally every time, since a profile snapshot isn't a discrete new item.

## GitHub enrichment (`enrichGithubLinks`)
When a story or comment's URL or text links to a GitHub repo, set `enrichGithubLinks: true` to look it up on GitHub's public API and add `githubStars`, `githubLanguage`, `githubPushedAt` and `githubOpenIssues` — handy for triaging Show HN launches or "what got built" threads by real traction rather than just HN points. Off by default (adds one extra request per distinct repo found). Bounded to 200 lookups per run against GitHub's unauthenticated 60/hour rate limit; a repo linked by multiple items in the same run is only looked up once. If the limit is hit mid-run, later items still get `githubRepo` (the match itself is free) but not the star/language/push data.

## Pricing
`result` — charged per item returned. Empty queries and failed pages are free. A `watchLabel` baseline run always returns 0 rows and is charged nothing. GitHub enrichment adds no separate charge.

## Tips
- Want the current front page? Set `queries` to `[]` and `tags` to `["front_page"]` — no keyword needed, returns the stories on HN's front page right now (verified against `hacker-news.firebaseio.com/v0/topstories.json`, refreshes on the same cadence as the live site).
- For the current "Who is hiring?" thread: set `queries` to `["Ask HN: Who is hiring"]`, `tags: ["story"]`, `sortBy: "date"`, `maxItemsPerQuery: 1` to find the thread, or use `tags: ["comment"]` with `postedAfter` set to the 1st of the month to pull all replies.
- Use `sortBy: "date"` for a live monitoring feed of new mentions of your keyword.
- Use `author` to pull everything a specific user has posted (e.g. track a founder's HN activity), or `minComments` to surface only high-engagement discussions.
- Leaving both `queries` and `tags` empty is not a "browse everything" mode — it's rejected (with a warning, no charge) rather than matching HN's entire 46M+ item history by relevance. Always set at least one tag (e.g. `["story"]`, `["front_page"]`) or a search query.

## FAQ
**Why did my run return 0 items with status SUCCEEDED?** The status message distinguishes "no matches for this query/tags/date/points filter" from "the Algolia request failed" — check it before assuming the query is wrong.
**Can I ask for two content types at once, e.g. stories and comments?** Yes — `tags: ["story","comment"]` returns both. The tags you list are OR-ed with each other, and `author` is AND-ed on top of that group, so `author: "pg"` + `tags: ["story","comment"]` returns pg's stories and pg's comments. (Underneath, HN's Algolia index treats a bare comma as AND, so `story,comment` would match nothing at all — the Actor wraps your tags in the OR form for you. See the guide linked below.)
**Can I combine `author` and `minComments`?** Yes, filters are ANDed together, e.g. `author: "pg"` + `minComments: 50` returns only that user's high-engagement posts.
**What if `queries` has an accidental duplicate?** Deduped automatically — the same story/comment matched by two queries is only pushed (and charged) once per run.
**Does this scrape the HN website?** No — it uses Algolia's official HN Search API, the same one that powers hn.algolia.com, so there's no scraping fragility to break.
**Do I get charged for empty queries?** No — only items actually returned to the dataset are charged.
**Is there a dedicated "top stories" or "by user" mode?** No separate mode needed — `tags: ["front_page"]` with no query returns the live front page, and `author` returns everything a given user posted, combinable with any other filter (points, comments, date range) that a fixed mode wouldn't let you apply.
**Can I look up a user's karma or bio, not just their posts?** Yes — put their username(s) in `usernames`. It's a separate lookup (via HN's official Firebase API) that returns one row per user with `karma`, `about` and `accountCreatedAt`, independent of `author`/`queries`. To fetch profiles only, with no story search mixed in, set `queries` and `tags` to `[]` too.
**What if a username in `usernames` doesn't exist?** It's skipped with no charge; the run's status message names which username(s) weren't found.
**How do I get a scheduled alert for new mentions of a keyword, not the same matches every time?** Set `watchLabel` (see above). The first run is a free baseline (0 results); schedule the same input to run again later and it returns only hits it has never delivered under that label before.
**I set `watchLabel` and `usernames` together — why did the profile row still show up on the baseline run?** By design. `watchLabel` only tracks story/comment/job search hits (they have a stable id to dedupe on); a `usernames` profile is a snapshot, not a discrete new item, so it is charged every run regardless of watch mode.
**Why are `githubStars`/`githubLanguage` null even though `githubRepo` is set?** Either GitHub's public API had nothing at that path (repo renamed, deleted or private — rare) or the run's 200-lookup budget or GitHub's own unauthenticated rate limit was hit; `githubRepo` itself is a free regex match against the item's own URL/text, not an API call, so it's always populated when a link is found.

## Related guides
Engineering write-ups behind this Actor:
- [HN's search API: commas mean AND, not OR](https://fetchsmith.com/blog/hacker-news-algolia-tags-and-not-or)
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how `watchLabel` is built and the three-run test that proves a baseline is complete

Only publicly available data is collected via HN's official search API. Questions or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com/tools/hacker-news-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/hacker-news-scraper
