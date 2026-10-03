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
| `minPoints` | integer | Only stories with at least this many points — jobs and comments have no points in HN's own data (always `null`), so combining this with `tags: ["job"]` or `tags: ["comment"]` matches nothing, at any threshold |
| `minComments` | integer | Only stories with at least this many comments (find high-engagement discussions) — same caveat: jobs and comments have no comment count of their own |
| `excludeKeywords` | array | Drop any story/comment whose title or text contains any of these words/phrases (case-insensitive) — HN's search has no negative-term syntax, so this is applied client-side after fetching, before you're charged |
| `domainFilter` | array | Only keep stories (and comments on those stories) whose linked URL's domain matches one of these, e.g. `["github.com","arxiv.org"]` — matches the domain or any subdomain of it, applied client-side after fetching, before you're charged. A comment is matched on its parent story's domain; items with no resolvable URL (text-only posts, jobs) are dropped when this is set |
| `maxCommentDepth` | integer | Only keep comments this many hops or fewer from their story (`1` = a direct reply to the story, `2` = a reply to a top-level comment, etc). HN's search index carries no depth field, so each comment's depth is resolved by walking its `parentId` chain via HN's own Items API, cached across the run and shared between comments in the same thread — leave empty to return comments at any depth, with no lookup and no `commentDepth` populated. Stories/jobs/polls are never affected |
| `author` | string | Only items posted by this exact HN username |
| `postedAfter` / `postedBefore` | string | ISO date bounds |
| `maxItemsPerQuery` | integer | Cap per query (up to 1000, which is also HN's own hard limit per query — see FAQ) |
| `maxResults` | integer | Overall cap |
| `usernames` | array | HN usernames to fetch profile data for (karma, about, account age) — a separate lookup, not a story filter. To fetch ONLY profiles with no story search, also set `queries` and `tags` to `[]`. |
| `watchLabel` | string | Name a saved search to get **only story/comment/job hits new since its last run** — see below |
| `watchChanges` | boolean | With `watchLabel`: also re-deliver an already-seen item when its points or comment count **crosses a milestone** (default `false`) — see below |
| `watchPointMilestones` | string | Comma-separated point thresholds for `watchChanges` (default `25,50,100,250,500,1000,2500,5000`; empty disables points alerts) |
| `watchCommentMilestones` | string | Comma-separated comment-count thresholds for `watchChanges` (default `25,50,100,250,500,1000`; empty disables comment alerts) |
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
  "parentId": null,
  "commentDepth": null,
  "githubRepo": null,
  "githubStars": null,
  "githubLanguage": null,
  "githubPushedAt": null,
  "githubOpenIssues": null
}
```
`githubRepo`/`githubStars`/`githubLanguage`/`githubPushedAt`/`githubOpenIssues` are only populated when `enrichGithubLinks: true` and the item actually links to a GitHub repo (common on Show HN); otherwise they stay `null`.

`parentId` is a comment's immediate HN parent (another comment, or the story itself) — `null` on stories/jobs/polls. `commentDepth` is that comment's distance from its story (`1` = direct reply) — it stays `null` on every row, comment or not, unless you set `maxCommentDepth` on this run; set it and the field is resolved for every comment that matches, not just the ones the limit would drop.

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

**A story's id never changes when it takes off — set `watchChanges` to hear about that too.** By default watch mode only ever tells you about brand-new items: a story you were already delivered goes silent forever, even on the day it hits the front page, because HN keeps the same item id for its whole life. Set `watchChanges: true` and an already-delivered item is re-delivered — charged again, same as a new row — when its `points` or `numComments` **crosses a milestone it hadn't reached when you last saw it**, tagged with `_watchChangeType` (`["pointsMilestone"]`, `["commentsMilestone"]`, or both), `_watchPrevious` (`{"points": 99}` — where it was last time) and `_watchMilestone` (`{"points": 100}` — the rung it cleared).

Why milestones instead of a plain "the number changed" diff: points and comments tick up on nearly every poll of an active story, so a bare diff would re-charge you on essentially every scheduled run for as long as a story stays warm. With milestones each rung pays out at most once per item — a story crawling from 51 to 99 points across twenty runs returns **nothing**, then returns **once** at 100. A story's entire life from 0 to 3,000 points costs you 7 extra rows on the default ladder, not 3,000. A score that falls (a flagged or downvoted post) never fires, and a jump straight from 10 to 600 fires once, at the highest rung cleared (500), not four times.

Tune the ladders to your queries with `watchPointMilestones` / `watchCommentMilestones` (comma-separated). A Show HN or niche-tag watch rarely passes 100 points, so `25,50,100` is the whole useful range; a front-page watch spends most of its life above 100 and wants a coarser ladder. Leave either field empty to switch that signal off entirely and keep the other. A baseline seeded before this option existed keeps working unchanged — it just has no engagement snapshot for its existing ids yet, so those start reporting milestones from the first run that re-sees each of them, never retroactively. `RUN_SUMMARY` and the webhook payload split the two: `watchNewCount` counts first-time items, `watchChangedCount` counts milestone re-deliveries.

**Baseline size cap.** The delivered-ids record itself is capped at 20,000 entries; once a label's baseline grows past that, the oldest ids are dropped to bound the record's size. If that happens, a later run will treat those dropped ids as "new" again and charge for them a second time — the run's log and status message warn explicitly when this occurs, and `RUN_SUMMARY`'s `baselineTruncated`/`baselineTruncatedTotal` fields give the exact counts. It only matters for a label with a very high cumulative volume of matches over many runs; narrow the query/tags to keep the baseline well under the cap.

## GitHub enrichment (`enrichGithubLinks`)
When a story or comment's URL or text links to a GitHub repo, set `enrichGithubLinks: true` to look it up on GitHub's public API and add `githubStars`, `githubLanguage`, `githubPushedAt` and `githubOpenIssues` — handy for triaging Show HN launches or "what got built" threads by real traction rather than just HN points. Off by default (adds one extra request per distinct repo found). Bounded to 200 lookups per run against GitHub's unauthenticated 60/hour rate limit; a repo linked by multiple items in the same run is only looked up once. If the limit is hit mid-run, later items still get `githubRepo` (the match itself is free) but not the star/language/push data.

**Comment rows check the parent story's link first.** A comment has no URL of its own — HN attaches the story's `url` to it — so on a `tags: ["comment"]` search, `githubRepo` reports the *story's* linked repo whenever the story links to GitHub, even if the comment's own text names a different repo. Only when the story has no GitHub link (or no link at all) does the comment's own text get scanned. Verified live: a comment on "Modern ClojureScript" (`storyUrl: https://github.com/magomimmo/modern-cljs`) that itself links to two unrelated repos (`omcljs/om`, `reagent-project/reagent`) came back with `githubRepo: "magomimmo/modern-cljs"` — the story's repo, not either repo the comment actually names. If you want the repo(s) a comment itself links to, read them out of its `text` field rather than relying on `githubRepo` when the parent story also has a GitHub link.

## Pricing
`result` — charged per item returned. Empty queries and failed pages are free. A `watchLabel` baseline run always returns 0 rows and is charged nothing. GitHub enrichment adds no separate charge.

The niche's biggest listing by lifetime users is `epctex` (176 users, `epctex/hackernews-scraper`) — but it is a dormant 2021-era listing, not an active rival: its build is still version 0.0, and it picked up **0 new users in the last 30 days**. It rented for a flat monthly fee until 2026-10-01, when Apify's rental-pricing deprecation converted it to $0.0003 per result plus a $0.00005 start fee — 1.5x our Free-tier rate and 3x our Gold rate, with a start fee we don't charge. Its 7 inputs are `startUrls`-driven (paste HN list/item URLs), with a comment-hierarchy toggle, a page-range cap and an `extendOutputFunction`; no keyword search, no tag filter, no thresholds, no date window, no user lookups, no watch mode, no webhook. Verified live 2026-10-02.

The actively-growing leader is `gentle_cloud` (157 users, 32 of them in the last 30 days — `gentle_cloud/hacker-news-scraper`), charging the same $0.0002 per result as we do on the Free tier, **more** than us on Bronze ($0.0002 vs our $0.00017), $0.0015 per result on Silver (11x our $0.00013 there), and **the same $0.0001 as us on Gold and above — we are not cheaper than them at the top three tiers, we match them**. Their input surface, read off their current build (0.0.1, unchanged since March 2026), is 7 fields: a mode selector (top/new/best/ask/show/job feeds, keyword search, and a `user` mode that returns one username's submitted stories), relevance/date sort, a max-results cap, top-level comments per story, and an HTTP timeout. No `minPoints`/`minComments` thresholds, no `excludeKeywords`, no `postedAfter`/`postedBefore` date windows, no multi-query batching, no comment-only search, no GitHub-link enrichment, no profile fields (their `user` mode returns a user's stories, not their karma/about text/account age), no watch mode with milestone re-alerts, and no completion webhook. Verified live 2026-10-02.

Two rivals ship point/comment thresholds and a date window. `automation-lab` (28 users, `automation-lab/hackernews-scraper`) charges $0.001 per run start plus $0.00115 per story on the Free tier: a 100-story run bills $0.116 there against $0.02 here, and we charge nothing to start a run. It has no comment search, no user lookups, no `excludeKeywords`, no multi-query batching, no watch mode and no webhook. The more capable one is `constructive_calm` (23 users, `constructive_calm/hacker-news-scraper`, 15 inputs): it charges a **$0.01 Actor-start fee** plus $0.0004 per story (2x our Free rate) — but only **$0.00015 per comment, below our flat $0.0002 on the Free tier**. On a comment-heavy run that start fee is what decides it: their $0.01 + $0.00015/comment crosses our $0.0002/comment at about **200 comments**, so for comment-only pulls larger than that they are genuinely cheaper than us on the Free tier, and we only win below that size. From Silver down ($0.00013 and lower) we are cheaper at every run size. `shahidirfan` (56 users, `shahidirfan/hacker-news-data-scraper`) is $0.0009 per result plus a $0.00005 start fee, 4.5x our Free rate, with only 3 inputs. Verified live 2026-10-02.

**The most feature-rich rival in this niche, never named here before, is `ryanclinton/hackernews-search`** (131 users, 26 of them in the last 30 days — more lifetime users than `automation-lab`, `constructive_calm` and `shahidirfan` combined, and the fastest-growing rival here after `gentle_cloud`). Its 31-field input schema goes past ours in several places: a 0-100 author-influence score computed from karma/age/submission count (we expose the raw karma/about/account-age fields but compute no score), a GitHub-link "correlation" mode that classifies a linked repo's freshness and maturity (we return stars/language/push-date/open-issues but no classification), sentiment/theme/risk heuristics on results, a two-window period-compare mode, and — the one gap worth calling out against our own FAQ above — it **auto-splits a query past Algolia's 1,000-hit ceiling into date-bucketed sub-runs for you** (`autoSplitLargeQueries`/`maxSplitRuns`), where we only document the ceiling and leave the date-slicing to you. It is also the dearest rival priced in this README: $0.005 per item on Free down to $0.0009 on Platinum/Diamond plus a $0.00005 start fee — **9x to 25x our own $0.0002-$0.0001 range**, so none of the above comes free. Verified live 2026-10-03 (input schema read off build 1.1.6).

For the Who's Hiring use case specifically, `logiover/hacker-news-who-is-hiring-scraper` (60 users) is dedicated to that one thread type (jobs, salary, tech stack extraction) at $0.0035/result on Free down to $0.00199 Gold+ — pricier than our flat rate at every tier and narrower in scope (job threads only, no keyword/story/comment search), not a general-purpose rival. Three more listings this sweep surfaced are checked and not a threat: `mrbridge/latest-news-mcp-server` (108 users) and `miccho27/trends-aggregator` (63 users) both bundle Hacker News as one of many sources alongside global news, crypto, weather, Reddit and Google Trends at $0.005-$0.008/item — a different product shape, not a head-on HN search tool — and `nexgendata/hacker-news-scraper` (51 users) outputs aggregate trend analytics (topic/domain breakdowns, top authors) at $0.05/record rather than per-item rows, also a different shape and far dearer. Verified live 2026-10-03.

**What we do not claim.** Our input surface is still not a strict superset of every rival's in this niche. We closed one of the two gaps named here at cycle 1116 (`domainFilter`, added 2026-10-02): it restricts stories, and comments on those stories, to a given set of link domains the same way `constructive_calm`'s does. We've now closed half of the other: `constructive_calm` ships `maxCommentDepth` and `flattenComments`; we added `maxCommentDepth` at cycle 1127 (resolved by walking each comment's parent chain, see Output above), but not `flattenComments` — our comments come from a keyword/tag search across the whole site, not a full per-story crawl, so we never hold a complete thread to flatten in the first place, only the scattered subset that matched. `constructive_calm` also exposes user profiles like we do, so profile lookups are no longer unique to us here. `ryanclinton` goes further still: an author-influence score, GitHub freshness/maturity classification, sentiment/trend/compare heuristics and automatic date-bucketed splitting past the 1,000-hit ceiling (see above) are all gaps in our own input surface, not theirs. We are also not the cheapest listing at every tier or every shape of run: see the Gold-tier match with `gentle_cloud` and the ~200-comment crossover with `constructive_calm` above. Verified live 2026-10-03.

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
**I set `minPoints` or `minComments` with `tags: ["job"]` or `tags: ["comment"]` and got 0 rows — why?** Verified live: job and comment hits carry `points: null` and no comment count at all in HN's own Algolia data, so those filters can never match a job or comment item, however low the threshold. The status message says so explicitly and names which of the two filters is set. Drop the filter, or search `tags: ["story"]` instead if you want a points/comment-count floor.
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
**For a comment, is `githubRepo` a repo the comment itself links to?** Not necessarily — see "Comment rows check the parent story's link first" above. It's the first GitHub repo found checking the story's link, then the comment's own text, then its title, in that order — so a comment discussing repos the story itself doesn't link to only surfaces them when the story has no GitHub link at all.
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
