# Substack Scraper – Posts, Full Text & Comments

Turn any Substack newsletter into structured JSON/CSV/Excel. Give it a publication (handle, `*.substack.com` URL, or a custom domain) and it returns every post with metadata **and the full article text**, plus the comment threads if you want them.

It talks to Substack's own public JSON endpoints — no login, no cookies, no headless browser. That makes it fast and cheap: hundreds of posts per minute, and you only pay per result.

## What makes it different

- **Full article text, cleaned.** Most Substack scrapers stop at the archive listing, which contains no article body at all. This Actor fetches each post and returns readable plain text (`bodyText`), with optional raw `bodyHtml`.
- **Comments included.** The whole thread, flattened, with `parentCommentId` so you can rebuild the tree.
- **Custom domains just work.** `bigtechnology.com`, `astralcodexten.com` — redirects from `<handle>.substack.com` are followed automatically.
- **Discover newsletters by category — no URL list needed.** Give `discoverCategories` a topic like `technology` or `finance` and the Actor pulls the top publications from Substack's own category leaderboard and scrapes them in the same run.
- **Or skip post scraping entirely and pull the leaderboard itself.** `leaderboardOnly: true` returns one row per publication — rank, subscriber counts, author, subscription prices — straight from Substack's overall/free/paid leaderboard (`leaderboardTier`). No archive walk, no per-post request. Built for newsletter-market research, not article content.
- **Search inside a publication.** `searchQuery` filters the archive server-side instead of downloading everything.
- **Publication profile on every row** (`includePublicationInfo`): free subscriber count, paid-subscriber band, bestseller tier, author name/handle/bio, the actual monthly/annual/founding subscription prices, podcast flag, language and first-post date. One extra request per publication — cached, so it costs the same whether you pull 5 posts or 5,000.
- **Many publications per run**, plus direct post URLs.
- **Cheap, and no Actor-start fee:** $0.002 per full-text post on the Free plan, $0.00078 on Gold and above. Metadata-only posts ($0.00112 down to $0.00039) and comments ($0.00056 down to $0.00019) are billed on their own, cheaper events, so an archive index or a comment-heavy run isn't priced like full articles.

## Use cases

- Build a searchable corpus of a newsletter for RAG / LLM fine-tuning.
- Track competitors' or clients' publishing cadence, topics and engagement (`reactionCount`, `commentCount`, `restackCount`).
- Media monitoring: search several publications for a keyword and get every matching post.
- Audience research: pull comment threads to see what readers actually argue about.
- Archive your own Substack (posts + comments) as a backup.
- Newsletter market research: rank the top paid newsletters in a niche by subscriber count and price with `leaderboardOnly`, no article scraping needed.

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `publicationUrls` | array | — | Publications to scrape: `astralcodexten`, `astralcodexten.substack.com`, or `https://www.bigtechnology.com`. |
| `postUrls` | array | — | Individual post URLs (`https://.../p/some-slug`). |
| `discoverCategories` | array | `[]` | **Start from a topic, not a URL list.** Substack category slugs (`technology`, `business`, `finance`, `culture`, `us-politics`, `food`, …, plus subcategory slugs). Publications come back in Substack's own leaderboard order. |
| `maxPublicationsPerCategory` | integer | `10` | How many top publications to take from each discovered category. |
| `discoverType` | string | `all` | Restrict discovery to `newsletter` or `podcast` publications. |
| `leaderboardTier` | string | `all` | Which leaderboard ranking `discoverCategories` reads from: `all` (overall), `free`, or `paid`. |
| `leaderboardOnly` | boolean | `false` | Return leaderboard rows only (rank, subscriber counts, pricing) — no post scraping. Requires `discoverCategories`; `publicationUrls`/`postUrls` are ignored. |
| `searchQuery` | string | — | Only return posts matching this keyword within each publication's archive. |
| `includeBodyText` | boolean | `true` | Fetch the full body and return clean plain text (one extra request per post). |
| `includeBodyHtml` | boolean | `false` | Also return the original HTML body. |
| `includeComments` | boolean | `false` | Also return each post's comments (charged at the lower `comment` rate, not the post rate). |
| `maxCommentsPerPost` | integer | `50` | Cap on comments per post. |
| `includePublicationInfo` | boolean | `false` | Add the `publication*` profile fields (subscriber count, plan prices, author, bestseller tier) to every post row. One cached request per publication, not per post — and no extra charge. |
| `audienceFilter` | string | `all` | `all`, `free` (public posts only) or `paid` (subscriber-only posts). |
| `contentType` | string | `all` | `all`, `newsletter` (text posts only), `podcast` (episodes only) or `thread` (Notes-style threads only). Also works on `postUrls`, not just publication archives. |
| `publishedAfter` / `publishedBefore` | string | — | ISO dates, e.g. `2026-01-01`. |
| `minReactionCount` / `minCommentCount` / `minRestackCount` | integer | — | Only return posts with at least this many reactions/comments/restacks. Read straight from the archive listing, so these cost nothing extra — no per-post detail fetch needed. |
| `minWordCount` / `maxWordCount` | integer | — | Only return posts within this word-count range. Find a publication's most-discussed posts, or its short link-roundups vs. long essays, without downloading anything you don't want to pay for. |
| `maxPostsPerPublication` | integer | `50` | Archive depth per publication — posts **scanned**, before filters. |
| `maxResults` | integer | `200` | Total cap across everything — this is what you pay for. |

```json
{
  "publicationUrls": ["astralcodexten", "https://www.bigtechnology.com"],
  "includeBodyText": true,
  "includeComments": true,
  "maxCommentsPerPost": 3,
  "maxPostsPerPublication": 4,
  "maxResults": 20
}
```

## Output

Three record shapes, distinguished by `type`.

**`type: "post"`**

| Field | Example |
|---|---|
| `id` | `207542232` |
| `title` | `God Help Us, Let's Try To Learn About Mechanistic Interpretability Techniques` |
| `subtitle`, `description` | short blurbs shown on the archive page |
| `slug` | `god-help-us-lets-try-to-learn-about` |
| `url` | `https://www.astralcodexten.com/p/god-help-us-lets-try-to-learn-about` |
| `publicationName`, `publicationUrl`, `publicationId` | `Astral Codex Ten`, `https://astralcodexten.substack.com`, `89120` |
| `authors` | `["Scott Alexander"]` |
| `postDate` | `2026-09-08T12:04:21.658Z` |
| `audience`, `isPaid` | `everyone`, `false` |
| `postType` | `newsletter`, `podcast`, `thread`, … |
| `wordCount` | `4695` |
| `reactionCount`, `commentCount`, `restackCount` | `199`, `118`, `14` |
| `tags`, `section`, `language` | `[]`, `null`, `en` |
| `coverImage`, `podcastUrl`, `podcastDurationSec` | media links where present |
| `bodyText` | full article as plain text (28 kB in the sample above) |
| `bodyHtml` | original HTML (only when `includeBodyHtml`) |
| `bodyTruncated` | `true` when the post is paywalled and no public text exists |

Only when `includePublicationInfo: true` (values below from a real run on `bigtechnology.com`):

| Field | Example |
|---|---|
| `publicationSubscriberCount`, `publicationSubscriberCountLabel` | `156000`, `Over 156,000 subscribers` — both `null` when the publication hides its count |
| `publicationPaidSubscribersLabel` | `Hundreds of paid subscribers` (Substack publishes a band, never an exact paid number) |
| `publicationBestsellerTier` | `100` — Substack's bestseller badge threshold (`100`, `1000`, `10000`) |
| `publicationAuthorName`, `publicationAuthorHandle`, `publicationAuthorBio` | `Alex Kantrowitz`, `bigtechnology`, `I write Big Technology and host Big Technology Podcast` |
| `publicationPlans` | `[{"interval":"month","intervalCount":1,"amount":8,"currency":"USD","name":"$8 a month"}, …]` |
| `publicationType`, `publicationLanguage`, `publicationFirstPostDate` | `newsletter`, `en`, `2020-05-26T20:21:30.375Z` |
| `publicationHasPodcast`, `publicationInviteOnly`, `publicationPaymentsEnabled` | `true`, `false`, `true` |
| `publicationDescription`, `publicationLogoUrl` | tagline and logo from the publication homepage |

```json
{
  "type": "post",
  "id": 207542232,
  "title": "God Help Us, Let's Try To Learn About Mechanistic Interpretability Techniques",
  "url": "https://www.astralcodexten.com/p/god-help-us-lets-try-to-learn-about",
  "publicationName": "Astral Codex Ten",
  "authors": ["Scott Alexander"],
  "postDate": "2026-09-08T12:04:21.658Z",
  "audience": "everyone",
  "isPaid": false,
  "wordCount": 4695,
  "reactionCount": 199,
  "commentCount": 118,
  "restackCount": 14,
  "bodyText": "The Story So Far\nMechanistic interpretability is the science of \"reading an AI's mind\"...",
  "bodyTruncated": false
}
```

**`type: "comment"`**

```json
{
  "type": "comment",
  "id": 332367021,
  "postId": 207542232,
  "postTitle": "God Help Us, Let's Try To Learn About Mechanistic Interpretability Techniques",
  "postUrl": "https://www.astralcodexten.com/p/god-help-us-lets-try-to-learn-about",
  "parentCommentId": null,
  "author": "Johannes Müller",
  "authorHandle": "derideonobis623245",
  "body": "ai research will end with a couch, a clipboard, and \"tell me more about this activation.\"",
  "date": "2026-09-08T13:08:44.304Z",
  "reactionCount": 6,
  "replyCount": 2,
  "isDeleted": false
}
```

**`type: "leaderboard"`** (only when `leaderboardOnly: true` — real row from `discoverCategories: ["technology"], leaderboardTier: "paid"`)

| Field | Example |
|---|---|
| `rank` | `1` — position on that category's leaderboard |
| `category`, `leaderboardTier` | `technology`, `paid` |
| `name`, `publicationUrl`, `handle`, `customDomain` | `SemiAnalysis`, `https://newsletter.semianalysis.com`, `semianalysis`, `newsletter.semianalysis.com` |
| `publicationSubscriberCount`, `publicationSubscriberCountLabel` | `316000`, `Over 316,000 subscribers` |
| `publicationPaidSubscribersLabel` | `Thousands of paid subscribers` |
| `publicationBestsellerTier` | `1000` |
| `publicationAuthorName`, `publicationAuthorHandle`, `publicationAuthorBio` | `Dylan Patel`, `semianalysis`, `Bridging the gap between business and the world's most important industry.` |
| `publicationPlans` | `[{"interval":"month","amount":50,"currency":"USD","name":"$50 a month"}, {"interval":"year","amount":500,"currency":"USD","name":"$500 a year"}]` |
| `publicationType`, `publicationLanguage`, `publicationFirstPostDate` | `newsletter`, `en`, `2020-05-22T21:26:00.000Z` |
| `publicationHasPodcast`, `publicationInviteOnly`, `publicationPaymentsEnabled` | `false`, `false`, `true` |
| `publicationDescription`, `publicationLogoUrl` | tagline and logo, same fields `includePublicationInfo` adds to post rows |

```json
{
  "type": "leaderboard",
  "rank": 1,
  "category": "technology",
  "leaderboardTier": "paid",
  "name": "SemiAnalysis",
  "publicationUrl": "https://newsletter.semianalysis.com",
  "publicationSubscriberCount": 316000,
  "publicationPaidSubscribersLabel": "Thousands of paid subscribers",
  "publicationAuthorName": "Dylan Patel",
  "publicationPlans": [
    {"interval": "month", "amount": 50, "currency": "USD", "name": "$50 a month"},
    {"interval": "year", "amount": 500, "currency": "USD", "name": "$500 a year"}
  ]
}
```

## Pricing

Pay per result, split by item type so metadata-only and comment-heavy runs aren't billed at full-article rates. **No Actor-start fee** — a 5-post run costs 5 results, not 5 results plus a fixed charge.

| Event | Free | Bronze | Silver | Gold and above |
| --- | --- | --- | --- | --- |
| Post with article text | $0.002 | $0.0018 | $0.0015 | $0.00078 |
| Post, metadata only | $0.00112 | $0.00098 | $0.00076 | $0.00039 |
| Comment | $0.00056 | $0.00049 | $0.00038 | $0.00019 |
| Leaderboard row (`leaderboardOnly`) | $0.0015 | $0.0013 | $0.001 | $0.0005 |

- **Metadata-only** is charged automatically whenever `includeBodyText` and `includeBodyHtml` are both off. You still get all 20+ non-body fields (title, subtitle, dates, audience/paywall status, reactions, restacks, comment counts, tags, section, podcast URL and duration, cover image). Turn the body off when you only need an index of a publication's archive — it's also much faster, because no per-post request is made.
- **Comments** are only charged when `includeComments` is on.
- **Leaderboard rows** are the only event charged when `leaderboardOnly` is on — no article/detail requests happen in this mode at all.

`maxResults` is a hard cap across every event type, so a run can never cost more than `maxResults × $0.002`. Nothing is charged for items that are filtered out or for failed requests.

## FAQ

**Does it get paywalled content?** No. It returns exactly what a logged-out visitor can see: paywalled posts come back with metadata and `bodyTruncated: true`. There is no login or paywall bypass, by design.
**What if I list the same publication or post twice?** Deduped automatically — `publicationUrls`/`postUrls` entries that resolve to the same origin or the same post are only fetched (and charged) once.

**Does it work with custom domains?** Yes — pass either the `*.substack.com` handle or the custom domain; redirects are followed either way.

**Why are comments optional?** They're charged like posts, and a popular post can have hundreds. Turn them on with `includeComments` and bound them with `maxCommentsPerPost`.

**What's the difference between `leaderboardOnly` and `discoverCategories` + `includePublicationInfo`?** Both read the same Substack leaderboard data, but `discoverCategories` alone uses the leaderboard only to find publications, then scrapes their posts (charged per post). `leaderboardOnly: true` skips the post scraping and returns the leaderboard rows themselves — rank, subscriber counts, pricing — as the entire result, at a fraction of the cost of a post-scraping run. Use it for "who are the top 20 paid tech newsletters and what do they charge", not "give me their articles".

**How far back can it go?** The whole archive — `maxPostsPerPublication` up to 5,000 posts per publication, paginated 50 at a time.

**I used a filter and got far fewer posts than I expected.** `maxPostsPerPublication` is a *scan depth*: it counts posts read from the archive, before `audienceFilter`, `contentType`, `publishedAfter`/`publishedBefore` and the `minReactionCount`/`minCommentCount`/`minRestackCount`/`minWordCount`/`maxWordCount` filters are applied. Searching `astralcodexten` for `prediction` with `publishedAfter: 2024-06-01` returns 2 posts at the default depth of 50 but 23 at depth 100 — the rest were simply never reached. `searchQuery` makes this easier to hit, because Substack returns search matches in relevance order rather than newest-first. When you combine filters, raise `maxPostsPerPublication` well above the number of rows you want; the run log and status message will tell you when a run was cut short this way. Only `maxResults` affects what you pay for.

**Is it reliable?** It uses documented-shape public JSON endpoints rather than HTML parsing, so it doesn't break when Substack restyles its site. Runs are tested nightly.

**Rate limits?** Requests are retried with backoff on 429/5xx. For very large jobs, split them across runs or lower concurrency by running publications separately.

## Related guides
Engineering write-ups behind this Actor:
- [Substack's archive API returns a body_html field for every post — it's just always null](https://fetchsmith.com/blog/substack-full-text-json-api)
- [HTTP-only vs headless browser scraping: a timed benchmark](https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost)


---

Built and maintained by [FetchSmith](https://fetchsmith.com) — small, fast, HTTP-only scrapers. Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/substack-scraper

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools) — 19 HTTP-only Actors for public data sources, no browser required.

Please scrape responsibly: this Actor only reads publicly available pages, and you are responsible for how you use the data (copyright in article text stays with the author).
