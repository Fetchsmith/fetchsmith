# Substack Scraper – Posts, Full Text & Comments

Turn any Substack newsletter into structured JSON/CSV/Excel. Give it a publication (handle, `*.substack.com` URL, or a custom domain) and it returns every post with metadata **and the full article text**, plus the comment threads if you want them.

It talks to Substack's own public JSON endpoints — no login, no cookies, no headless browser. That makes it fast and cheap: hundreds of posts per minute, and you only pay per result.

## What makes it different

- **Full article text, cleaned.** Most Substack scrapers stop at the archive listing, which contains no article body at all. This Actor fetches each post and returns readable plain text (`bodyText`), with optional raw `bodyHtml`.
- **Comments included.** The whole thread, flattened, with `parentCommentId` so you can rebuild the tree.
- **Custom domains just work.** `bigtechnology.com`, `astralcodexten.com` — redirects from `<handle>.substack.com` are followed automatically.
- **Search inside a publication.** `searchQuery` filters the archive server-side instead of downloading everything.
- **Many publications per run**, plus direct post URLs.
- **Cheap:** $0.002 per result, roughly 60% under the usual $0.005.

## Use cases

- Build a searchable corpus of a newsletter for RAG / LLM fine-tuning.
- Track competitors' or clients' publishing cadence, topics and engagement (`reactionCount`, `commentCount`, `restackCount`).
- Media monitoring: search several publications for a keyword and get every matching post.
- Audience research: pull comment threads to see what readers actually argue about.
- Archive your own Substack (posts + comments) as a backup.

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `publicationUrls` | array | — | Publications to scrape: `astralcodexten`, `astralcodexten.substack.com`, or `https://www.bigtechnology.com`. |
| `postUrls` | array | — | Individual post URLs (`https://.../p/some-slug`). |
| `searchQuery` | string | — | Only return posts matching this keyword within each publication's archive. |
| `includeBodyText` | boolean | `true` | Fetch the full body and return clean plain text (one extra request per post). |
| `includeBodyHtml` | boolean | `false` | Also return the original HTML body. |
| `includeComments` | boolean | `false` | Also return each post's comments (charged as results). |
| `maxCommentsPerPost` | integer | `50` | Cap on comments per post. |
| `audienceFilter` | string | `all` | `all`, `free` (public posts only) or `paid` (subscriber-only posts). |
| `publishedAfter` / `publishedBefore` | string | — | ISO dates, e.g. `2026-01-01`. |
| `maxPostsPerPublication` | integer | `50` | Archive depth per publication. |
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

Two record shapes, distinguished by `type`.

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

## Pricing

Pay per result: **$0.002** per post or comment returned. `maxResults` is a hard cap, so a run can never cost more than `maxResults × $0.002`. Nothing is charged for items that are filtered out or for failed requests.

## FAQ

**Does it get paywalled content?** No. It returns exactly what a logged-out visitor can see: paywalled posts come back with metadata and `bodyTruncated: true`. There is no login or paywall bypass, by design.

**Does it work with custom domains?** Yes — pass either the `*.substack.com` handle or the custom domain; redirects are followed either way.

**Why are comments optional?** They're charged like posts, and a popular post can have hundreds. Turn them on with `includeComments` and bound them with `maxCommentsPerPost`.

**How far back can it go?** The whole archive — `maxPostsPerPublication` up to 5,000 posts per publication, paginated 50 at a time.

**Is it reliable?** It uses documented-shape public JSON endpoints rather than HTML parsing, so it doesn't break when Substack restyles its site. Runs are tested nightly.

**Rate limits?** Requests are retried with backoff on 429/5xx. For very large jobs, split them across runs or lower concurrency by running publications separately.

## Related guides
Engineering write-ups behind this Actor:
- [Substack's archive API returns a body_html field for every post — it's just always null](https://fetchsmith.com/blog/substack-full-text-json-api)
- [HTTP-only vs headless browser scraping: a timed benchmark](https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost)


---

Built and maintained by [FetchSmith](https://fetchsmith.com) — small, fast, HTTP-only scrapers. Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/substack-scraper

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools) — 17 HTTP-only Actors for public data sources, no browser required.

Please scrape responsibly: this Actor only reads publicly available pages, and you are responsible for how you use the data (copyright in article text stays with the author).
