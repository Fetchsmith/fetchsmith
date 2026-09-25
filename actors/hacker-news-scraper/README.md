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
| `excludeKeywords` | array | Drop any story/comment whose title or text contains any of these words/phrases (case-insensitive) — HN's search has no negative-term syntax, so this is applied client-side after fetching, before you're charged |
| `author` | string | Only items posted by this exact HN username |
| `postedAfter` / `postedBefore` | string | ISO date bounds |
| `maxItemsPerQuery` | integer | Cap per query (up to 1000, which is also HN's own hard limit per query — see FAQ) |
| `maxResults` | integer | Overall cap |
| `usernames` | array | HN usernames to fetch profile data for (karma, about, account age) — a separate lookup, not a story filter. To fetch ONLY profiles with no story search, also set `queries` and `tags` to `[]`. |
| `watchLabel` | string | Name a saved search to get **only story/comment/job hits new since its last run** — see below |
| `enrichGithubLinks` | boolean | When a result links to a GitHub repo, add star count, primary language, last-push date and open-issue count (default `false`) |
| `webhookUrl` | string | Optional. POST a small JSON completion summary (items pushed, hits scanned, dataset ID, watch new/skipped counts, per-query completeness) here when the run finishes — see FAQ |

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
  "engagementScore": 161,
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

`engagementScore` is `points + numComments × 0.5`, rounded to 1 decimal — a single number for sorting/filtering a result set by engagement without hand-weighing two columns yourself. It is **not** decayed by age (unlike HN's own front-page ranking): an age-decayed score collapses to ~0 for anything older than a few days, which would make it useless on relevance search or `sortBy:"date"` results spanning years — the common case for a keyword search. `null` on comment rows, which never carry `points`/`numComments`.

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
Name a saved search — `watchLabel: "my-launch-watch"` — and the Actor keeps a per-label record of every story/comment/job hit it has already delivered under that name, so a scheduled run returns **only what is new since last time** and you are charged for nothing else. The first run on a new label is a **free baseline run**: it records what already matches and returns zero results. HN's search API never serves more than 1000 hits for one query (see FAQ), so **a query with more than 1000 current matches cannot be fully baselined** — the un-recorded tail would come back as "new" and be charged on your next run. The baseline run detects this and says so explicitly in its status message, naming each query and its declared match count; narrow those queries (tighter keywords, `minPoints`, or a `postedAfter` window) until each fits under 1000, then re-seed under a fresh `watchLabel`. Every run after that returns only new items. Change `queries`, `tags`, `author`, `sortBy`, the date range or the point/comment thresholds and the label starts a fresh baseline, instead of dumping everything the old narrower filter excluded as "new". `usernames` profile lookups are unaffected — they run and are charged normally every time, since a profile snapshot isn't a discrete new item.

**Baseline size cap.** The delivered-ids record itself is capped at 20,000 entries; once a label's baseline grows past that, the oldest ids are dropped to bound the record's size. If that happens, a later run will treat those dropped ids as "new" again and charge for them a second time — the run's log and status message warn explicitly when this occurs, and `RUN_SUMMARY`'s `baselineTruncated`/`baselineTruncatedTotal` fields give the exact counts. It only matters for a label with a very high cumulative volume of matches over many runs; narrow the query/tags to keep the baseline well under the cap.

## GitHub enrichment (`enrichGithubLinks`)
When a story or comment's URL or text links to a GitHub repo, set `enrichGithubLinks: true` to look it up on GitHub's public API and add `githubStars`, `githubLanguage`, `githubPushedAt` and `githubOpenIssues` — handy for triaging Show HN launches or "what got built" threads by real traction rather than just HN points. Off by default (adds one extra request per distinct repo found). Bounded to 200 lookups per run against GitHub's unauthenticated 60/hour rate limit; a repo linked by multiple items in the same run is only looked up once. If the limit is hit mid-run, later items still get `githubRepo` (the match itself is free) but not the star/language/push data.

## Pricing
`result` — charged per item returned. Empty queries and failed pages are free. A `watchLabel` baseline run always returns 0 rows and is charged nothing. GitHub enrichment adds no separate charge.

## Tips
- Want the current front page? Set `queries` to `[]` and `tags` to `["front_page"]` — no keyword needed, returns the stories on HN's front page right now (verified against `hacker-news.firebaseio.com/v0/topstories.json`, refreshes on the same cadence as the live site).
- For the current "Who is hiring?" thread: set `queries` to `["Ask HN: Who is hiring"]`, `tags: ["story"]`, `sortBy: "date"`, `maxItemsPerQuery: 1` to find the thread, or use `tags: ["comment"]` with `postedAfter` set to the 1st of the month to pull all replies.
- Use `sortBy: "date"` for a live monitoring feed of new mentions of your keyword.
- Use `author` to pull everything a specific user has posted (e.g. track a founder's HN activity), or `minComments` to surface only high-engagement discussions.
- Use `excludeKeywords` to keep a broad query narrow, e.g. `queries: ["rust"]` + `excludeKeywords: ["cryptocurrency"]` keeps Rust-the-language discussions and drops mentions of an unrelated Rust-named crypto project.
- Leaving both `queries` and `tags` empty is not a "browse everything" mode — it's rejected (with a warning, no charge) rather than matching HN's entire 46M+ item history by relevance. Always set at least one tag (e.g. `["story"]`, `["front_page"]`) or a search query.

## FAQ
**I asked for a common word and got exactly 100 (or 1000) rows — is that everything?** No, and the run now tells you so instead of leaving you to guess. Two separate ceilings apply. Yours: `maxItemsPerQuery` (default 100). HN's: **Algolia's HN index never returns more than 1000 hits for a single query**, whatever you set — a search for `ai` declares nearly 2 million matches (measured: `nbHits: 1,978,072`) and will still only ever hand over 1000 of them; page 1000 returns Algolia's own pagination-limit message, not an error. When either ceiling truncates a query, the run's status message names the query with both numbers ("20 scanned of 60108 declared"), and the per-query detail lands in a machine-readable `RUN_SUMMARY` record. To actually get more than 1000, split one broad query into consecutive `postedAfter`/`postedBefore` windows — verified live to reconstruct the true total exactly with no gap or double-count (twelve monthly slices of `python` summed to the same 3,995 as one over-the-ceiling yearly query) — but **the window width has to match how hot the query is**: monthly stays under the ceiling for `python` (256–447/month) but not for `ai` (3,368 in one month alone, needing ~weekly slices instead). Read `hitPaginationCeiling` back and halve the window whenever it's `true`, rather than guessing a fixed width. See [the 1,000-hit ceiling guide](https://fetchsmith.com/blog/hacker-news-1000-hit-search-ceiling) for the full live measurement.

**How do I check completeness from code, without reading the log?** Every run writes a `RUN_SUMMARY` key-value record — `GET https://api.apify.com/v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY` — with a top-level `complete` boolean and one entry per query: `declaredMatches` (what HN says exists), `scanned`, `delivered`, `filteredOut`, `status`, `complete`, `incompleteReason` and `hitPaginationCeiling`. `status` and `complete` are deliberately separate: a query can be `"ok"` *and* truncated, which is the case worth catching. The top-level `timeBudgetExceeded` boolean tells you whether the run stopped itself short of the platform run timeout rather than hitting `maxResults`/the charge limit — when it's `true`, any query still marked `notReached` was never searched because the clock ran out, not because nothing was left to check; narrow the input (fewer queries, lower `maxItemsPerQuery`, or `enrichGithubLinks:false`) or run them separately. When `watchLabel` is set, `baselineTruncated`/`baselineTruncatedTotal` report whether this run's baseline record hit its 20,000-id size cap (see "Baseline size cap" above) — non-null and non-zero means some already-delivered ids will be re-charged on a future run.
```json
{ "complete": false, "pushed": 25, "queriesIncomplete": 2, "queriesNotReached": 1,
  "queries": [
    { "query": "rust", "declaredMatches": 60108, "scanned": 20, "delivered": 20, "filteredOut": 0,
      "status": "ok", "complete": false, "incompleteReason": "max-items-per-query", "hitPaginationCeiling": false, "scanCap": 20 },
    { "query": "kubernetes", "declaredMatches": null, "scanned": 0, "delivered": 0, "filteredOut": 0,
      "status": "notReached", "complete": false, "incompleteReason": null, "hitPaginationCeiling": false, "scanCap": null }
  ] }
```
`incompleteReason` is one of `algolia-pagination-ceiling`, `max-items-per-query`, `seed-cap`, `max-results`, `charge-limit`, `scan-short-of-declared`, `request-failed` or `time-budget` (the run stopped itself short of the platform run timeout, not a real data ceiling). The same fields are posted to `webhookUrl` if you set one.

**I passed 5 queries but rows only came back for the first two.** Three possible causes, and the status message and `RUN_SUMMARY` tell you which: the run hit `maxResults` (or your pay-per-event charge limit) partway through, or — if `timeBudgetExceeded` is `true` in `RUN_SUMMARY` — the run was approaching the platform run timeout and stopped itself before the clock ran out, which is a different problem with a different fix (narrow the input rather than raising `maxResults`). Either way the remaining queries are never searched — they appear in `RUN_SUMMARY` with `status: "notReached"` and are named in the status message, so "we never looked there" can't be mistaken for "nothing matched there".

**Why did my run return 0 items with status SUCCEEDED?** The status message distinguishes "no matches for this query/tags/date/points filter" from "the Algolia request failed" — check it before assuming the query is wrong.
**What happens if Algolia's API has a transient blip mid-run?** Each page request is retried up to 3 times on a connection-level failure (measured on `remote-jobs-scraper`'s upstream boards at roughly 1 fresh request in 4 for HTTP/2 faults, 2026-09-21) before that query is given up on and named in the status message — a single blip no longer silently truncates a query to whatever page it reached.
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

**How is `webhookUrl` different from Apify's own platform webhooks?** Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `scanned`, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchSkippedCount`) once the run finishes and every item is already pushed and charged. Especially useful with `watchLabel` on a scheduled keyword alert: your endpoint is told how many new hits landed without polling the dataset, and `watchSeeding: true` distinguishes "this was the free baseline run" from "your watch is live and quiet" — both report zero new rows otherwise. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing. Note: a run that ends in an unhandled error exits before this block runs, so `webhookUrl` reports what the run found, not that it happened — pair it with Apify's own run-status webhook if you need failure alerts too.
**Why are `githubStars`/`githubLanguage` null even though `githubRepo` is set?** Either GitHub's public API had nothing at that path (repo renamed, deleted or private — rare) or the run's 200-lookup budget or GitHub's own unauthenticated rate limit was hit; `githubRepo` itself is a free regex match against the item's own URL/text, not an API call, so it's always populated when a link is found.
**Why isn't there a "NOT" or negative-term operator in `queries`?** HN's underlying Algolia search doesn't support one — `excludeKeywords` gets you the same result a different way: it fetches your normal `queries`/`tags` match set, then drops (uncharged) any item whose title or text contains one of your excluded words, so you only pay for what's left.

## Related guides
Engineering write-ups behind this Actor:
- [HN search caps every query at 1,000 hits, no matter what nbHits claims](https://fetchsmith.com/blog/hacker-news-1000-hit-search-ceiling) — live proof of the ceiling, and why the date-slicing workaround's window width has to match how hot the query is
- [HN's search API: commas mean AND, not OR](https://fetchsmith.com/blog/hacker-news-algolia-tags-and-not-or)
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how `watchLabel` is built and the three-run test that proves a baseline is complete
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for.
- [Substack, Apple Podcasts, Google News and Hacker News — four free APIs where the first response isn't the finished product](https://fetchsmith.com/blog/public-content-apis-hidden-second-step) — how this Actor's second-step trap compares to the other three content platforms we scrape.

Only publicly available data is collected via HN's official search API. Questions or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com/tools/hacker-news-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/hacker-news-scraper
