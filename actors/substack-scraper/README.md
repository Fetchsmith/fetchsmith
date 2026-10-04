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
| `discoverCategories` | array | `[]` | **Start from a topic, not a URL list.** Substack category slugs (`technology`, `business`, `finance`, `culture`, `us-politics`, `food`, …, plus subcategory slugs). Publications come back in Substack's own leaderboard order. If you set this and leave `publicationUrls` untouched, only the discovered publications are scraped — the sample publication in `publicationUrls`'s default is not scraped and not charged. |
| `maxPublicationsPerCategory` | integer | `10` | How many top publications to take from each discovered category. |
| `discoverType` | string | `all` | Restrict discovery to `newsletter` or `podcast` **publications** (not posts — see the FAQ). Leave at `all` unless you know the category has podcast-type publications. |
| `leaderboardTier` | string | `all` | Which leaderboard ranking `discoverCategories` reads from: `all` (overall) or `paid`. `free` is accepted but is NOT a real Substack tier — see the FAQ. |
| `leaderboardOnly` | boolean | `false` | Return leaderboard rows only (rank, subscriber counts, pricing) — no post scraping. Requires `discoverCategories`; `publicationUrls`/`postUrls` are ignored. |
| `searchQuery` | string | — | Only return posts matching this keyword within each publication's archive. |
| `includeBodyText` | boolean | `true` | Fetch the full body and return clean plain text (one extra request per post). |
| `includeBodyHtml` | boolean | `false` | Also return the original HTML body. |
| `includeComments` | boolean | `false` | Also return each post's comments (charged at the lower `comment` rate, not the post rate). |
| `maxCommentsPerPost` | integer | `50` | Cap on comments per post. |
| `includePublicationInfo` | boolean | `false` | Add the `publication*` profile fields (subscriber count, plan prices, author, bestseller tier) to every post row. One cached request per publication, not per post — and no extra charge. |
| `audienceFilter` | string | `all` | `all`, `free` (public posts only) or `paid` (subscriber-only posts). |
| `contentType` | string | `all` | `all`, `newsletter` (text posts only) or `podcast` (episodes only). Also works on `postUrls`, not just publication archives. A `thread` value exists for compatibility, but live testing across many publications (2026-09-29) found no post of that type in Substack's archive API — it's very likely to return 0 rows; use `all` and check `postType` on your results instead. |
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
| `postType` | `newsletter` or `podcast` in every publication we've tested; `thread` is a theoretical third value Substack's schema allows but we've never observed |
| `wordCount` | `4695` — the full article's length, as Substack reports it |
| `reactionCount`, `commentCount`, `restackCount` | `199`, `118`, `14` |
| `tags`, `section`, `language` | `[]`, `null`, `en` |
| `coverImage`, `podcastUrl`, `podcastDurationSec` | media links where present |
| `bodyText` | full article as plain text (28 kB in the sample above) |
| `bodyHtml` | original HTML (only when `includeBodyHtml`) |
| `bodyWordCount` | `4695` — words actually in `bodyText`. Equals `wordCount` on public posts; smaller on a paywalled preview |
| `bodyTruncated` | `true` when `bodyText` is **not** the whole article — no public body at all, or only the free preview of a paid post |

Only when `includeComments: true`:

| Field | Example |
|---|---|
| `commentsRetrieved` | `190` — how many comments Substack actually handed back, to compare against `commentCount` (how many it says the post has). Unaffected by `maxCommentsPerPost`, which is your own cap and applies after. `null` if the request failed |
| `commentsWithheld` | `true` when the post has comments but Substack served **none** of them — subscriber-only posts keep their comment section paywalled |

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
  "bodyWordCount": 4695,
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

**Competitors, verified 2026-10-03.** The Store's biggest Substack scraper, `automation-lab/substack-scraper` (532 users, 144 in the last 30 days), tiers full-text posts from $0.0023 (Free) down to $0.00056 at Diamond ($0.0012 at Gold, $0.0008 at Platinum), plus a flat $0.005 Actor-start fee on every run. We have no start fee, so we're cheaper on small or Free-plan runs — 5 posts costs $0.01 here vs their $0.0165, and even 1,000 posts on the Free plan is $2.00 here vs their $2.305 — but their lower per-post rate wins on large Diamond-tier runs (1,000 posts: $0.78 here vs their $0.565), because at that volume it outweighs the flat start fee. The cheapest well-trafficked listing, `sourabhbgp/substack-scraper` (93 users, 21 in the last 30 days), charges a flat $0.0003 per post with full HTML regardless of plan tier — 2.6x to 6.7x below our price at every tier — and also scrapes Substack Notes (`notesHandles`), which we don't offer. It has no equivalent to our category-based discovery (`discoverCategories`), standalone leaderboard mode (`leaderboardOnly`), or engagement/word-count filters (`minReactionCount`/`minCommentCount`/`minRestackCount`/`minWordCount`/`maxWordCount`) that let you avoid paying for posts you don't want — but on raw per-post price for plain full-text scraping, it undercuts everyone in the niche, us included. Three newer entrants stay below the 50-u30d bar for a full schema check but cost more either way: `easyapi/substack-posts-scraper` (273 users, 29u30d) charges a flat $0.00499/result plus a $0.09 start fee, `fatihtahta/substack-scraper` (246 users, 34u30d) charges $0.0025/result on Free and a flat $0.00199 from Bronze up, and `cryptosignals/substack-scraper` (72 users, 6u30d, never previously named) charges a flat $0.005/result with no separate start fee — all three well above our $0.002-down-to-$0.00078 full-text rate.

**Two more rivals, each bigger than `sourabhbgp`, found in a fresh Store sweep and never previously named (verified 2026-10-03).** `digispruce/substack-scraper` (122 users, 12 in the last 30 days) splits its charge into three separate per-post events — newsletter info ($0.003 Free → $0.0019 Gold+, billed once per publication, not per post), post metadata ($0.001 Free → $0.0005 Gold+), and post content ($0.001 Free → $0.0005 Gold+) — so a full-text post costs metadata + content: $0.002 Free (tied with us) or $0.001 Gold+ (cheaper per-post than our $0.00078 Gold+... but their per-publication fee adds $0.0019–$0.003 on top of every run, which our zero-start-fee pricing never does, so we are cheaper at every tier and every run size once that fee is counted: at Gold+, our cost crosses below theirs at 1 post already, $0.00078 vs $0.0029). `brilliant_gum/substack-insights-scraper` (128 users, 29 in the last 30 days) charges a flat $0.015 per entity (publication, post, comment, note, or author) plus a $0.01 Actor-start fee — 7x to 19x our full-text rate depending on tier, with no crossover in our favor at any volume; it does scrape Notes and subscriber-growth history, which we don't.

**One more rival, found in the same sweep and never previously named — a leaderboard-only specialist (verified 2026-10-03).** `easyapi/substack-leaderboard-scraper` (107 users, 7 in the last 30 days) scrapes only Substack category leaderboards (publication rank, subscriber counts, pricing, author details) — a narrower tool than our general scraper, but it goes head-to-head with our own standalone `leaderboardOnly` mode. It charges a flat $0.00299/row plus a $0.09 Actor-start fee; our leaderboard-row event is $0.0015 (Free) down to $0.0005 (Gold+), with no start fee at all — roughly 2x cheaper per row even on our Free plan before the start fee is counted, and the gap widens every tier up.

**Two real undercutters, found by widening the Store search past Apify's own per-query result cap, never previously named (verified 2026-10-04).** `scraper_guru/substack-scraper` (65 users) bills one `Post` event — full article content (plain text, Markdown and HTML), nested comments, and publication/author metadata all included, no separate comment charge — at $0.0005 (Free) down to $0.00035 (Gold+), plus a flat one-time $0.00035 Actor-start fee: **cheaper than our own full-text rate at every tier**, 4x on Free and 2.2x on Gold+, and it doesn't split comments into a second billable event the way we do. `benthepythondev/newsletter-scraper` (60 users) charges a flat $0.001/result for full content in Markdown/HTML/plain-text plus an LLM token count — cheaper than our $0.002 Free-tier rate but above our $0.00078 Gold+ rate; it advertises Beehiiv and Ghost support, but its own README says those are "in active development" and only Substack is live today, so the cross-platform claim is aspirational, not a current scope advantage. Three more `easyapi` single-purpose siblings exist alongside their already-named Posts/Leaderboard Actors — `easyapi/substack-publications-scraper` (88 users), `easyapi/substack-notes-scraper` (83 users), `easyapi/substack-people-scraper` (61 users) — all three on a flat $19.99/month subscription rather than pay-per-result, a different pricing model we don't compete on directly. Ruled out as non-substitutes: `contactminerlabs/substack-email-scraper` and `sourabhbgp/substack-lead-gen` (43u/40u) sell contact-email and B2B lead lists, not post content; `stanvanrooy6/substack-scraper` ($10/month flat, 38u) returns post metadata only, no body text. **Watch item:** `dacoder/substack-scraper` (38 users) is on Apify's genuinely-FREE pricing model today (an automatic migration off its old $24/month rental, dated 2026-10-01), but it already has a PAY_PER_EVENT schedule queued to start **2026-10-15**: $0.0015/post (Free) + a $0.0025 full-text add-on, i.e. $0.004 Free-tier / $0.0032 Gold+ once combined — dearer than us at every tier once it lands, so no action needed, just don't mistake the current $0 price for the standing one if this niche comes up again after mid-October.

**Why these two didn't surface before (verified 2026-10-04):** not a search-ranking blind spot — re-running the exact old 11-variant auto-fallback sweep confirms both listings were already inside its matched set. The real gap is the one cycle 1188 named for `uk-find-a-tender-scraper`: a niche whose matched count is bigger than its *named* handle count has a tail nobody reads, because every audit before this one stopped at the sweep's printed top-10-by-users table. `scraper_guru` (65u) and `benthepythondev` (60u) both rank just below that cutoff, under already-named listings with only slightly more users — counted in every sweep's number, never actually opened and priced until this cycle read past rank 10.

## FAQ

**Does it get paywalled content?** No. It returns exactly what a logged-out visitor can see, and it tells you when that is less than the whole article. Substack serves a *free preview* of most subscriber-only posts — a real body, but cut off partway through, while the post's own `wordCount` still reports the full length. Re-measured live across 69 posts from 7 publications: paid posts returned 0%–97% of the declared word count (median 34%), free posts 98%–140% (median 101%), and preview length is a per-publication setting — 2–5% on one publication, 25–37% on another, 34–46% on a third. Note that the listing's `audience` field is **not** a reliable proxy: 4 of the 27 paid posts in that sample came back essentially whole (96%–97%), because publications unlock posts without changing the flag. Rows that really are short come back with `bodyTruncated: true` and a `bodyWordCount` well below `wordCount`, so you can filter or discount them instead of mistaking a preview for a full article. Posts with no public body at all are `bodyTruncated: true` with an empty `bodyText`. There is no login or paywall bypass, by design.

**How do I avoid paying for previews?** Set `audienceFilter: "free"` — public posts only, which are the ones that come back complete. The filter is applied from the archive listing, before any body is fetched or charged.
**What if I list the same publication or post twice?** Deduped automatically — `publicationUrls`/`postUrls` entries that resolve to the same origin or the same post are only fetched (and charged) once.

**Does it work with custom domains?** Yes — pass either the `*.substack.com` handle or the custom domain; redirects are followed either way.

**Why are comments optional?** They're charged like posts, and a popular post can have hundreds. Turn them on with `includeComments` and bound them with `maxCommentsPerPost`.

**I turned on `includeComments` and got no comments, even though the posts show hundreds.** The comment section of a subscriber-only post is paywalled too, and Substack's API says so by answering `200 OK` with an empty list rather than an error. Measured live across three publications, the split is total: all 15 public posts sampled returned their full tree (318–1200 comments, no server-side cap), and all 15 subscriber-only posts returned **zero** — one of them on a post declaring 5,426 comments. Those rows come back `commentsWithheld: true` with `commentsRetrieved: 0`, and the run log and status message both name the count, so it is visible rather than looking like a broken run. Set `audienceFilter: "free"` to scrape only posts whose comments you can actually get. You are never charged for a comment that wasn't returned.

**What's the difference between `leaderboardOnly` and `discoverCategories` + `includePublicationInfo`?** Both read the same Substack leaderboard data, but `discoverCategories` alone uses the leaderboard only to find publications, then scrapes their posts (charged per post). `leaderboardOnly: true` skips the post scraping and returns the leaderboard rows themselves — rank, subscriber counts, pricing — as the entire result, at a fraction of the cost of a post-scraping run. Use it for "who are the top 20 paid tech newsletters and what do they charge", not "give me their articles".

**I set `minReactionCount`/`minWordCount`/`audienceFilter`/etc. together with `leaderboardOnly` and nothing changed.** Expected — leaderboard rows are publication summaries, not posts, so post-level filters (`audienceFilter`, `contentType`, `publishedAfter`/`publishedBefore`, `minReactionCount`, `minCommentCount`, `minRestackCount`, `minWordCount`, `maxWordCount`) have nothing to apply to and are ignored (the run log carries a warning naming them). To filter individual posts by engagement or word count, run without `leaderboardOnly`.

**I set `discoverType: "podcast"` and got zero rows.** `discoverType` filters the *publications* Substack's category leaderboard returns, and those leaderboards are almost entirely `newsletter`-type publications — we swept the whole technology leaderboard live (300 publications, 12 pages, both the `all` and `paid` tiers) and found not a single podcast-type one; even Substack's dedicated `podcast` category is only about 3% podcast-type. So `discoverType: "podcast"` legitimately matches nothing in most categories, and raising `maxPublicationsPerCategory` cannot help because the whole leaderboard has already been read. The run log and status message now say exactly this instead of pointing at the cap. If what you actually want is podcast **episodes**, leave `discoverType: "all"` and set `contentType: "podcast"` — newsletter-type publications do publish podcast posts (a `discoverCategories: ["technology"]` run returns `postType: "podcast"` rows from `newsletter.pragmaticengineer.com`, verified live).

**The status message says "the Substack leaderboard request failed" or "the leaderboard returned no publications".** These are two different causes and the message names which one you hit. A *failed request* is transient (Substack rate-limits or a 5xx) — just re-run; changing `discoverCategories`, `leaderboardTier` or `maxPublicationsPerCategory` cannot help, because the leaderboard was never read. A leaderboard that genuinely *returned nothing* is rare: we checked all 33 Substack categories against all three `leaderboardTier` values live (2026-09-25) and every single combination returned a full page of publications, so if you see it, try `leaderboardTier: "all"` or a category slug straight from `substack.com/api/v1/categories`. Raising `maxPublicationsPerCategory` is never the fix for either case — it is a cap on how many publications to *keep*, not how deep to look.

**I set `leaderboardTier: "free"` expecting free-only newsletters.** Substack's category leaderboard API does not actually have a free-only tier. Verified live (2026-09-26) across 3 categories at every page depth: `.../category/public/<id>/free` returns the byte-identical publication list, in the same order, as `.../all` — it never filters anything out. Only `all` (everyone) and `paid` (a genuinely separate, paid-subscriber-ranked list) are real. `leaderboardTier: "free"` still runs (it's kept for backwards compatibility and the run log warns when you use it) but it is equivalent to `"all"`, which mixes free and paid-tier publications — there's no reliable way to reconstruct a true free-only list client-side either, since a publication's `payments_state` field does not predict membership in the `paid` leaderboard. If you specifically want monetized newsletters, use `leaderboardTier: "paid"`.

**How far back can it go?** The whole archive — `maxPostsPerPublication` up to 5,000 posts per publication, paginated 50 at a time.

**I used a filter and got far fewer posts than I expected.** `maxPostsPerPublication` is a *scan depth*: it counts posts read from the archive, before `audienceFilter`, `contentType`, `publishedAfter`/`publishedBefore` and the `minReactionCount`/`minCommentCount`/`minRestackCount`/`minWordCount`/`maxWordCount` filters are applied. Searching `astralcodexten` for `prediction` with `publishedAfter: 2024-06-01` returns 2 posts at the default depth of 50 but 23 at depth 100 — the rest were simply never reached. `searchQuery` makes this easier to hit, because Substack returns search matches in relevance order rather than newest-first. When you combine filters, raise `maxPostsPerPublication` well above the number of rows you want; the run log and status message will tell you when a run was cut short this way. Only `maxResults` affects what you pay for.

**Is it reliable?** It uses documented-shape public JSON endpoints rather than HTML parsing, so it doesn't break when Substack restyles its site. Runs are tested nightly.

**Rate limits?** Requests are retried with backoff on 429/5xx. For very large jobs, split them across runs or lower concurrency by running publications separately.

## Related guides
Engineering write-ups behind this Actor:
- [Substack's archive API returns a body_html field for every post — it's just always null](https://fetchsmith.com/blog/substack-full-text-json-api)
- [HTTP-only vs headless browser scraping: a timed benchmark](https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost)
- [A Substack paywalled post returns a body_html that looks complete — it's a preview, and `audience` won't tell you](https://fetchsmith.com/blog/substack-paywalled-post-preview-vs-full-text)
- [Substack, Apple Podcasts, Google News and Hacker News — four free APIs where the first response isn't the finished product](https://fetchsmith.com/blog/public-content-apis-hidden-second-step) — how this Actor's second-step trap compares to the other three content platforms we scrape.


---

Built and maintained by [FetchSmith](https://fetchsmith.com) — small, fast, HTTP-only scrapers. Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/substack-scraper

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools) — 19 HTTP-only Actors for public data sources, no browser required.

Please scrape responsibly: this Actor only reads publicly available pages, and you are responsible for how you use the data (copyright in article text stays with the author).
