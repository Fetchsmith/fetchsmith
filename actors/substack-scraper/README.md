# Substack Scraper – Posts, Full Text & Comments

Turn any Substack newsletter into structured JSON/CSV/Excel. Give it a publication (handle, `*.substack.com` URL, or a custom domain) and it returns every post with metadata **and the full article text**, plus the comment threads if you want them.

It talks to Substack's own public JSON endpoints — no login, no cookies, no headless browser. That makes it fast and cheap: hundreds of posts per minute, and you only pay per result.

## What makes it different

- **Full article text, cleaned.** Most Substack scrapers stop at the archive listing, which contains no article body at all. This Actor fetches each post and returns readable plain text (`bodyText`), with optional raw `bodyHtml`.
- **Comments included.** The whole thread, flattened, with `parentCommentId` so you can rebuild the tree.
- **Custom domains just work.** `bigtechnology.com`, `astralcodexten.com` — redirects from `<handle>.substack.com` are followed automatically.
- **Discover newsletters by category — no URL list needed.** Give `discoverCategories` a topic like `technology` or `finance` and the Actor pulls the top publications from Substack's own category leaderboard and scrapes them in the same run.
- **Or skip post scraping entirely and pull the leaderboard itself.** `leaderboardOnly: true` returns one row per publication — rank, subscriber counts, author, subscription prices — straight from Substack's overall/free/paid leaderboard (`leaderboardTier`). No archive walk, no per-post request. Built for newsletter-market research, not article content.
- **Filter discovery by podcast or monetization status, at zero extra cost.** `requirePodcast` and `requirePaymentsEnabled` keep only the publications on the leaderboard that actually have a podcast feed or paid subscriptions enabled — the flags are already on every leaderboard entry, so no extra request is made.
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
| `requirePodcast` | boolean | `false` | Only keep discovered publications that have a podcast feed enabled (Substack's `podcast_enabled` flag — different from `discoverType`, see FAQ). Costs nothing extra: this flag is already on every leaderboard entry. |
| `requirePaymentsEnabled` | boolean | `false` | Only keep discovered publications with paid subscriptions enabled. Same zero-extra-cost source as `requirePodcast`. |
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
| `authors` | `["Scott Alexander"]` — see note below, this can be empty |
| `postDate` | `2026-09-08T12:04:21.658Z` |
| `audience`, `isPaid` | `everyone`, `false` |
| `postType` | `newsletter` or `podcast` on the vast majority of posts; `restack` (the publication reshared someone else's post into its own archive — see `isRestack` below) shows up on a small minority — found live 2026-10-10 on 2 of 412 sampled posts across 18 publications. `thread` is a theoretical fourth value Substack's schema allows but we've never observed |
| `isRestack` | `true` when `postType` is `restack`. With `contentType: "all"` (the default) these rows pass through like any other post, but the title/subtitle/cover image are the ORIGINAL publication's, not this one's — and if `includeBodyText`/`includeBodyHtml` is on, the body fetched is also the original author's full article (Substack resolves the per-post detail request straight through to it), not anything this publication wrote. Set `contentType: "newsletter"` (or `"podcast"`) to exclude restacks outright, or filter on `isRestack` yourself if you want `"all"`'s engagement counts but not the reshared content. |
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

**Competitors, verified 2026-10-03, user count refreshed 2026-10-23.** The Store's biggest Substack scraper, `automation-lab/substack-scraper` (661 users, 144 in the last 30 days), tiers full-text posts from $0.0023 (Free) down to $0.00056 at Diamond ($0.0012 at Gold, $0.0008 at Platinum), plus a flat $0.005 Actor-start fee on every run. We have no start fee, so we're cheaper on small or Free-plan runs — 5 posts costs $0.01 here vs their $0.0165, and even 1,000 posts on the Free plan is $2.00 here vs their $2.305 — but their lower per-post rate wins on large Diamond-tier runs (1,000 posts: $0.78 here vs their $0.565), because at that volume it outweighs the flat start fee. The cheapest well-trafficked listing, `sourabhbgp/substack-scraper` (105 users, 21 in the last 30 days), charges a flat $0.0003 per post with full HTML regardless of plan tier — 2.6x to 6.7x below our price at every tier — and also scrapes Substack Notes (`notesHandles`), which we don't offer. It has no equivalent to our category-based discovery (`discoverCategories`), standalone leaderboard mode (`leaderboardOnly`), or engagement/word-count filters (`minReactionCount`/`minCommentCount`/`minRestackCount`/`minWordCount`/`maxWordCount`) that let you avoid paying for posts you don't want — but on raw per-post price for plain full-text scraping, it undercuts everyone in the niche, us included. Three newer entrants stay below the 50-u30d bar for a full schema check but cost more either way: `easyapi/substack-posts-scraper` (273 users, 29u30d) charges a flat $0.00499/result plus a $0.09 start fee, `fatihtahta/substack-scraper` (246 users, 34u30d) charges $0.0025/result on Free and a flat $0.00199 from Bronze up, and `cryptosignals/substack-scraper` (81 users, 6u30d, never previously named) charges a flat $0.005/result with no separate start fee — all three well above our $0.002-down-to-$0.00078 full-text rate.

**Two more rivals, each bigger than `sourabhbgp`, found in a fresh Store sweep and never previously named (verified 2026-10-03).** `digispruce/substack-scraper` (122 users, 12 in the last 30 days) splits its charge into three separate per-post events — newsletter info ($0.003 Free → $0.0019 Gold+, billed once per publication, not per post), post metadata ($0.001 Free → $0.0005 Gold+), and post content ($0.001 Free → $0.0005 Gold+) — so a full-text post costs metadata + content: $0.002 Free (tied with us) or $0.001 Gold+ (cheaper per-post than our $0.00078 Gold+... but their per-publication fee adds $0.0019–$0.003 on top of every run, which our zero-start-fee pricing never does, so we are cheaper at every tier and every run size once that fee is counted: at Gold+, our cost crosses below theirs at 1 post already, $0.00078 vs $0.0029). `brilliant_gum/substack-insights-scraper` (231 users, 57 in the last 30 days, re-verified 2026-10-25) charges a flat $0.015 per entity (publication, post, comment, note, or author) plus a $0.01 Actor-start fee — 7x to 19x our full-text rate depending on tier, with no crossover in our favor at any volume; it does scrape Notes and subscriber-growth history, which we don't.

**One more rival, found in the same sweep and never previously named — a leaderboard-only specialist (verified 2026-10-03).** `easyapi/substack-leaderboard-scraper` (107 users, 7 in the last 30 days) scrapes only Substack category leaderboards (publication rank, subscriber counts, pricing, author details) — a narrower tool than our general scraper, but it goes head-to-head with our own standalone `leaderboardOnly` mode. It charges a flat $0.00299/row plus a $0.09 Actor-start fee; our leaderboard-row event is $0.0015 (Free) down to $0.0005 (Gold+), with no start fee at all — roughly 2x cheaper per row even on our Free plan before the start fee is counted, and the gap widens every tier up.

**Two real undercutters, found by widening the Store search past Apify's own per-query result cap, never previously named (verified 2026-10-04).** `scraper_guru/substack-scraper` (65 users) bills one `Post` event — full article content (plain text, Markdown and HTML), nested comments, and publication/author metadata all included, no separate comment charge — at $0.0005 (Free) down to $0.00035 (Gold+), plus a flat one-time $0.00035 Actor-start fee: **cheaper than our own full-text rate at every tier**, 4x on Free and 2.2x on Gold+, and it doesn't split comments into a second billable event the way we do. `benthepythondev/newsletter-scraper` (60 users) charges a flat $0.001/result for full content in Markdown/HTML/plain-text plus an LLM token count — cheaper than our $0.002 Free-tier rate but above our $0.00078 Gold+ rate; it advertises Beehiiv and Ghost support, but its own README says those are "in active development" and only Substack is live today, so the cross-platform claim is aspirational, not a current scope advantage. Three more `easyapi` single-purpose siblings exist alongside their already-named Posts/Leaderboard Actors — `easyapi/substack-publications-scraper` (88 users), `easyapi/substack-notes-scraper` (83 users), `easyapi/substack-people-scraper` (61 users) — all three on a flat $19.99/month subscription rather than pay-per-result, a different pricing model we don't compete on directly. Ruled out as non-substitutes: `contactminerlabs/substack-email-scraper` and `sourabhbgp/substack-lead-gen` (43u/40u) sell contact-email and B2B lead lists, not post content; `stanvanrooy6/substack-scraper` ($10/month flat, 38u) returns post metadata only, no body text. **`dacoder/substack-scraper`, update verified live 2026-10-28:** the PAY_PER_EVENT schedule flagged below as a future watch item (originally found 2026-10-04, queued to start 2026-10-15) has now landed — `startedAt` 2026-10-15T15:16:56Z, no pending future-change notification — and is the standing price, not a watch item any more: $0.0015/post (Free) down to $0.0012 (Gold+) plus a $0.0025 (Free) → $0.002 (Gold+) full-text add-on and a $0.00005 one-time Actor-start fee, i.e. $0.004 Free-tier / $0.0032 Gold+ combined. Dearer than us at every tier exactly as forecast (39 users now, was 38) — no change to our pricing position, just no longer the $0 price this niche saw between 2026-10-01 and 2026-10-15.

**Why these two didn't surface before (verified 2026-10-04):** not a search-ranking blind spot — re-running the exact old 11-variant auto-fallback sweep confirms both listings were already inside its matched set. The real gap is the one cycle 1188 named for `uk-find-a-tender-scraper`: a niche whose matched count is bigger than its *named* handle count has a tail nobody reads, because every audit before this one stopped at the sweep's printed top-10-by-users table. `scraper_guru/substack-scraper` (65u) and `benthepythondev` (60u) both rank just below that cutoff, under already-named listings with only slightly more users — counted in every sweep's number, never actually opened and priced until this cycle read past rank 10.

**One clear new undercutter, three partial/shape-different ones, and two parity listings, found by a full scope-first `niche-unnamed` sweep — 164 matched, 18 already named, every ≥3-user unnamed listing skimmed for scope before pricing (verified 2026-10-04).** `scrapesage/substack-scraper` (17 users, 5 in the last 30 days, re-verified 2026-10-18) bills its `post` event — "full content when enabled," directly comparable to our full-text rate — at $0.001 (Free) down to $0.00025 (Diamond), with no separate Actor-start fee found: **cheaper than us at every tier**, 2x on Free widening to ~3.1x at Diamond ($0.00055 Gold, $0.00038 Platinum). It also sells a separate publication-profile event with a 0-100 lead score and a contact-enrichment add-on (emails/phone/socials) — product surface we don't offer and don't want to (PII lead-gen is out of scope for this Actor), so treat those two events as a different, non-competing product bolted onto a genuinely cheaper post-scraper. Two narrower partial undercutters: `hata1234/substack-scraper` (34 users, 3 in the last 30 days) charges a flat $0.001/post plus a $0.005 start fee — cheaper than us above ~5-10 posts/run on Free/Bronze/Silver, but never beats our $0.00078 Gold+ rate at any volume since its per-post rate alone exceeds ours; `sian.agency/substack-scraper` tiers a $0.05-down-to-$0.005 start fee plus per-post rates that only dip below ours at Diamond ($0.0006 full-content / $0.0003 metadata-only vs our $0.00078 / $0.00039), crossing over only above ~28 full-content or ~56 metadata-only posts in a single Diamond-tier run — dearer than us at every other tier and at any volume on Free through Platinum. One shape-different bulk-volume undercutter: `opalescent_quintet/substack-newsletter-scraper` (8 users, 1 in the last 30 days) charges a near-zero $0.00001/post plus a flat $1 per-run completion fee instead of per-post pricing — dearer than us below ~500 posts/run (Free) or ~1,300 posts/run (Gold+), cheaper above that, a different bet for buyers who run very large single batches. Two parity listings, cheaper only on Free and tied or dearer everywhere else: `sleek_waveform/substack-creator-scraper` (22 users, re-verified live 2026-10-16) charges a flat $0.002/post with no tiering at all, matching our Free rate exactly but losing every tier above it since we drop and it doesn't; `logiover/substack-newsletter-scraper` (10 users, 1 in the last 30 days) ties our Free and Bronze rates ($0.002/$0.0018) and is marginally dearer from Silver up ($0.0016 vs our $0.0015, $0.0014 vs our $0.00078 at Gold+). Ruled out by scope without pricing (different product shape, not a substitute): five Substack Notes scrapers (`scrapestorm/substack-notes-scraper---cheap`, `fetch_cat/substack-notes-scraper`, `maximedupre/substack-notes`, plus `automation-lab/substack-notes-search-author-monitor`'s author-monitor mode — we don't scrape Notes), three lead-gen/sponsor-finder tools (`silentshadow55/newsletter-sponsors-actor`, `axlymxp/substack-newsletter-lead-finder`, `automation-lab/substack-recommendations-network-scraper`), a people/username finder with no Substack-specific scope (`scrapestorm/substack-people-scraper---cheap`, `memo23/username-social-finder`), a newsletter-discovery/directory tool (`getdataforme/substack-discovery-scraper`, `jungle_synthesizer/inboxreads-newsletter-directory-scraper`), a generic RSS converter that only name-matched on "substack" in its description (`gabrielaxy/website-to-rss`), and a leads-focused discovery listing (`thequietstack/substack-scraper`). Also confirmed dearer than us at every tier with no further action: `parsebird/substack-leaderboard-scraper` (32u, re-verified live 2026-10-16), `saswave/substack-leaderboard-profile-scraper` (26u, 0 runs in the last 30 days — dormant), `memo23/substack-scraper` (19u), `scrapestorm/substack-posts-scraper---cheap` (10u), `crawlerbros/substack-scraper` (gone from the Store as of 2026-10-09, confirmed 404 — was 9u, dearer than us), `scrapestorm/substack-leaderboards-scraper---cheap` (9u), `doggo/substack-scraper-posts-comments-authors` (a $0.05-$0.1 start fee alone exceeds our whole-run cost on small jobs), and `extremescrapes/substack-articles-extractor` ($0.05 **per record** — 25x-65x our rate, despite a misleadingly tiny-looking dataset-item line price).

**The previously-unpriced tail, now live-priced (verified 2026-10-05) — two real undercutters, the rest confirmed dearer.** `cirkit/substack-newsletter-scraper` (3 users) charges a flat **$0.0007 per post row**, no separate Actor-start fee found on the live record — cheaper than us at **every** tier, including our own $0.00078 Gold+ floor, on any run size. `darknezz/substack-posts-scraper` (1 user) carries two pricing records: an older PAY_PER_EVENT ladder (Actor-start $0.00005 + $0.005/post) superseded on 2026-08-26 by a newer entry that switched the whole Actor to Apify's **FREE** pricing model — it is $0 today, undercutting our whole ladder by construction, and neither `check-price-superiority` nor `check-rental-converts` would catch this since it's an owner-chosen FREE switch with no `reasonForChange`, not the rental auto-migration. Both are genuine new undercutters with no feature parity check done (time budget) — neither README text we could find advertises comments, metadata-only billing, or leaderboard mode, so our scope is still wider, just not cheaper on raw per-post price anymore.

One more is a likely **owner misconfiguration worth watching, not a genuine bargain**: `hipersoft/substack-scraper` tiers $0.001 (Free) down to $0.0005 (Gold+) on its `post-scraped` event, described as "Charged per post scraped" — but the live record flags that event `isOneTimeEvent: true`, so as published it bills once per run regardless of post count, not once per post. This is the same misconfiguration shape already disclosed on this owner's other Actor (`hipersoft/remote-jobs-aggregator`, see `remote-jobs-scraper`'s README) — worth a recheck in a future audit to see if either gets fixed, since a correctly-wired per-post version at that price would beat our Gold+ rate too.

Seven more confirmed dearer at every tier and run size, no crossover: `makework36/substack-scraper` (5u) flat $0.005/post + $0.00005 start; `seemuapps/substack-post-content` (4u) flat $0.0035/post + $0.00005 start; `cloud9_ai/substack-scraper` (2140 runs/30d despite the low user count) flat $0.003/result + $0.00005 start (a superseded 2026-03-25 record read $0.0015, replaced a day later); `skootle/substack-posts` (3u) tiers $0.004 (Free) down to $0.002 (Diamond) plus a flat $0.005 start fee; `getdataforme/substack-posts-scraper` (1u) flat $0.009/result plus a $0.05 start fee, the dearest in this batch; `easyapi/substack-publication-scraper` (singular — distinct from the already-named plural `substack-publications-scraper`) flat $0.00499/result plus a $0.09 start fee, having converted off an old 2024 flat-monthly-rental record in 2026-05; and `scrapemint/substack-newsletter-intelligence` is shape-different, not a direct substitute — it charges $0.01 per *publication* row bundling recent-post summaries and comment counts at no extra charge (first 3 rows free), closer to a lightweight profile-intelligence product than our per-post or per-leaderboard-row pricing, and dearer than both regardless.

**A fresh sweep of this niche (verified 2026-10-06) found one partial undercutter and one listing that went to $0 the day before.** The niche has grown to 173 Store listings; these are every unnamed one with 3 or more users, priced off its *current* live pricing record.

`lergassy/substack-scraper` is a genuine **partial undercutter**: no start fee, and it tiers a `post` metadata event from $0.0006 (Free) to $0.00045 (Gold+) with a separate full-text add-on for free posts at the same $0.0006 → $0.00045. Full text therefore costs $0.0012 on Free and $0.0009 at Gold+ against our $0.002 → $0.00078, and metadata-only costs $0.0006 → $0.00045 against our $0.00112 → $0.00039 — so **it is cheaper than us on Free, Bronze and Silver (about 1.5x–1.9x) and we are cheaper at Gold, Platinum and Diamond** on both full text and metadata. Its full-text add-on covers free posts only. It bills publication metadata as its own $0.002 → $0.0014 row, where our `includePublicationInfo` attaches the same kind of publication fields to posts without a separate charge, and it has no comment rows, no category/leaderboard discovery (`discoverCategories`, `leaderboardOnly`) and no engagement or word-count filters, so our scope stays wider — we are simply not the cheapest option below Gold anymore.

`qpayre/substack-scraper` (468 users, the largest listing in the niche by lifetime users) was a **$20/month rental since 2023 and was automatically switched to Apify's FREE pricing model on 2026-10-05** during Apify's rental sunset, so its Actor price is $0 today and the buyer pays only Apify platform usage. Two things keep that from being a straight comparison: it is an author-page *crawler* that fetches and parses article HTML, so platform compute — not an Actor fee — is the real cost on any sizeable run, and its scope is narrow (all posts from one author, with an optional parsed article body; no comments, no publication/leaderboard discovery, no filters). It also looks unmaintained: 3 users in the last 30 days against 468 lifetime, and its published example input is still the `{"helloWorld": 123}` placeholder. Treat it as a $0-price option for small author archives, not as a feature-comparable alternative.

Five more confirmed dearer at every tier, no crossover in their favour: `contactminerlabs/substack-email-scraper---advanced-cheapest-reliable` (64u, re-verified 2026-10-25 — the renamed slug of the contact-email product already ruled out above as a non-substitute) flat $0.00999/result + $0.00005 start; `moving_beacon-owner1/substack-scraper` flat $0.01/result + $0.00005 start; `apricot_blackberry/substack-all-in-one` charges a flat $0.03 Actor-start fee — more than 15 full-text posts cost here on the Free plan — on top of $0.002/post, $0.003 with content, $0.001/comment (vs our $0.00056 → $0.00019) and $0.003/publication, none of it tiered, so it ties us only on the Free tier and loses from Bronze up; `parseforge/substack-publication-scraper` (3u) tiers $0.011 → $0.00825 per item, 5.5x–10.6x our full-text rate; and `undivided_alpenglow/substack-intelligence` (3u) charges a $0.005 start fee plus flat $0.003 per post with body (dearer than us everywhere) and flat $0.001 per metadata post — its one narrow edge is metadata-only runs of more than about 42 posts on the Free plan, where the start fee is outweighed; from Bronze up our per-row rate alone is lower at any volume.

**The previously-deferred 1-2-user tail, now fully closed (verified 2026-10-07).** 1308 live-priced only the ≥3-user unnamed cohort (7 listings) and explicitly left the rest of the tail (then ~113 listings) as a known follow-up. This sweep priced the entire unnamed tail end to end — 115 listings, 0-2-user floor included, no top-N cut — and found the niche's price floor for plain full-text post scraping has dropped sharply since the last full check: a large majority of the newest 1-3-user entrants now charge flat or tiered rates well under our $0.002 Free-tier full-text price, and many beat our $0.00078 Gold+ floor too. All are too new for an exact user count to stay accurate under the standing ≥20-user rule, so none are published with one.

Representative genuine undercutters, all verified against each listing's own live, `isPrimaryEvent`-flagged charge event (not a marketing headline number): a Substack posts scraper billing a flat **$0.0004 → $0.00026/post** (Free → Gold+) advertises itself as "$0.0002 per post," but that figure is the per-post rate alone — the listing also carries a real one-time Actor-start fee of **$0.002 → $0.0013**, so a 1-post run actually costs more than our own Free-tier full run of the same size, a branding-vs-live-price gap in the same shape already on file for `scrapestorm`'s "Cheap" siblings elsewhere in this fleet. Others undercut cleanly with no such catch: a full-HTML-and-comments scraper at a flat **$0.0008 → $0.0004/post**; a publication-JSON-archive reader (optional full text) at **$0.0005 → $0.0003**; a full-content-plus-nested-comments scraper advertising unlimited archive depth and keyword discovery at **$0.00099 → $0.00039** (ties our own Gold+ floor almost exactly on its own Free tier); and a newsletter-feed scraper at **$0.0015 → $0.00027**. None of these documents our category-based discovery (`discoverCategories`), standalone leaderboard mode (`leaderboardOnly`), engagement/word-count filters, or free publication metadata via `includePublicationInfo` — our scope stays wider, we are simply not the cheapest raw per-post price in this niche's long tail anymore, on top of already not being the cheapest among the bigger, previously-named listings.

Two listings ruled out of scope on their own live description, not their title: one bills a `recommendation-edge` event and maps which publications recommend which others — a relationship graph, not post content, so it is not a substitute at any price. One leaderboard-only listing prices its leaderboard-row event at **$0.00003 → $0.00001**, undercutting our own `leaderboardOnly` mode's $0.0015 → $0.0005 rate by roughly 50-100x, but it has no post-scraping event at all, so it only competes with the standalone leaderboard use case, not full-text or metadata scraping. The remainder of the 115 split between dearer-at-every-tier listings (no crossover, not worth individual write-ups) and out-of-scope products already covered by this README's standing exclusions (Substack Notes scrapers, lead-gen/sponsor-finder and contact-enrichment tools, generic newsletter-list or RSS converters, flat-monthly-subscription listings).

**A fresh sweep of the niche's newest ≥3-user unnamed listings (verified 2026-10-08) found one genuine new partial undercutter.** `apium/substack-scraper` (3 users) bills a single primary event — full text, authors, dates, likes, and comment counts, directly comparable to our own full-text post event — at a flat $0.001/result plus a $0.00005 one-time Actor-start fee, no tiering. That undercuts us on Free, Bronze and Silver ($0.002 / $0.0018 / $0.0015, about 1.5x–2x cheaper) but we're cheaper from Gold up ($0.00078 vs their flat $0.001). Three more checked and confirmed dearer at every tier, no crossover: `haketa/substack-scraper` (1u as of 2026-10-25, was 3u) tiers $0.0025 → $0.00175 plus a $0.00005 start fee; `gio21/substack-tech-scraper` (3u) charges a flat $0.003/row and its own Store description is the literal placeholder "auto-scaffolded," a sign of an unmaintained listing; `feedforge/substack-scraper` (3u) charges a flat $0.002/row plus a $0.00005 start fee, so it ties our Free tier at best and loses from Bronze up. One more ruled out of scope: `dataflow-tools/newsletter-sponsor-intelligence` (3u) enriches newsletters with contact info and audits sponsor disclosures — a lead-gen tool, not a post-content substitute, matching this README's standing lead-gen exclusion above.

**Rotation resweep (verified 2026-10-09): niche-size 185 matched (up from 182), 120 unnamed, still thin — the highest lifetime-user count anywhere in the unnamed tail is 2, so nothing clears the ≥3-user floor.** Per the standing rule, spot-checked the 6 unnamed listings whose own Store title advertises a per-1k or "low-cost" rate, live-pricing each from its own `pricingInfos` rather than trusting the title. One is a new record for this niche: `scrapesignal_labs/substack-newsletter-scraper` (2 users) bills a single flat, untiered primary event — full article text/HTML, author, publication, date, categories, word count, summaries, and canonical URL, directly comparable to our own full-text event — at **$0.0002/post plus a $0.00005 one-time Actor-start fee**, and its title's "$0.20/1K" claim matches that live price exactly, unlike the mismarked "$0.0002 per post" listing already on file two paragraphs up. That makes it the cheapest verified real price found in this niche to date: about 4x under our own $0.00078 Gold+ floor, and about 2x under the $0.0004 → $0.00026 listing already disclosed above at every tier. `glasswing/substack-scraper` (2u) bills a flat $0.0005/post plus a $0.005 start fee — its start fee is paid back by row ~4 ($0.005 ÷ ($0.002 − $0.0005)), so it is cheaper than us in practice on any normal-sized run. The other four title-advertised listings turned out dearer than their own marketing, not cheaper than us, so none is a threat: `ahmed_jasarevic/substack-scraper` ("$2.5/1k" title) actually bills a flat ~$0.0025/post, dearer than us at every tier; `bovi/substack-publication` ("$1.50/1K" title) actually bills $0.003 → $0.00285/listing — double its own advertised rate — dearer than us at every tier; and both `delectable_incubator` "low-cost" listings bill a flat $0.00238/post, dearer than our own Free tier, let alone Gold+.

**Twelfth sweep (verified 2026-10-23): niche grown to 263 matched (up from 185), 196 unnamed — still thin on its own, but a tooling-gap fix this cycle surfaced a real new undercutter the old code would have misread.** `hridayrungta/substack-scraper` (2u, title "$0.25 / 1K") carries a one-time `actor-started` fee that TIERS by plan ($0.0017 Free → $0.00119 Gold+) with `isPrimaryEvent: true` and `isOneTimeEvent` left unset — our own `_unit_price.py` read that as the recurring primary price until this cycle, because its only override for an unflagged one-time fee required a FLAT ladder (see fix below), and the event's own `eventDescription` ("One-time fee charged once per run, regardless of how many posts or comments it finds") was never read. With that fixed, the real comparable event is `post-scraped`: **$0.00025 (Free) → $0.000175 (Gold+)**, matching its own "$0.25/1K" title exactly — 8x under our Free rate, 4.5x under our Gold+ floor. Its start fee pays for itself by post 1 at Free and by post 2 at Gold+, so it is cheaper than us at any realistic run size. It also bills a separate `comment-scraped` event at $0.00012 → $0.000084, under our own $0.00056 → $0.00019 comment rate.

`maximedupre/substack-api` (2u) bills its `substack-post-retrieved` primary event at $0.0018 (Free) down to $0.00025 (Diamond) — a clean full-category undercutter at every tier, 10%–68% below us depending on plan. `fetch_cat/substack-posts-scraper` (2u) bills an extremely cheap $0.000032 → $0.0000167/post plus a $0.005 start fee — the fee pays back by post 3 at Free, so it undercuts us above that at every tier. `fetch_cat/substack-leaderboard-scraper` (1u, brand new) prices its `result` row at $0.0000346 → $0.00001, directly against our own `leaderboardOnly` mode's $0.0015 → $0.0005 — a 43x–50x undercut if it holds up with more runs, same shape as the already-named `easyapi/substack-leaderboard-scraper` comparison. `axlymxp/substack-scraper` (2u) bills Apify's generic dataset-item event (its only charge, so not a decoy) at a flat $0.0015 plus a $0.005 start fee — only beats our Free tier, and only above ~10 posts/run; dearer than us from Bronze up.

Four `delectable_incubator` "low-cost" listings (two more than previously named) all bill the same generic dataset-item event at $0.00198–$0.00238 across their tiers — dearer than our $0.002 Free-tier full-text rate outright on three of the four, and the fourth (`substack-explore-leaderboards-scraper-low-cost`) is still roughly 4x dearer than our dedicated $0.0005 Gold+ leaderboard rate once compared against the right unit, not our post price. None is a threat. Two more ruled out by scope: `maximedupre/substack-recommendations` (3u) maps publication-to-publication recommendation edges, the same non-substitute shape as the already-ruled-out `recommendation-edge` listing above; `getdataforme/substack-profile-scraper` (2u) is a $0.009/row + $0.05-start profile-only tool, dearer regardless of scope.

**Tooling fix shipped alongside this sweep:** `bin/_unit_price.py`'s `is_start_fee` now also trusts an explicit `eventDescription` saying "once per run" as a one-time-fee signal, not just `isOneTimeEvent` or a flat ladder — closing the gap `hridayrungta`'s listing exposed (a one-time fee that tiers by plan, which the old flat-ladder-only override couldn't recognize). Verified via 5 fault-injected cases (the real `hridayrungta` shape plus 4 controls: a `hipersoft`-shape real per-row event misflagged one-time, `hyperbach`'s flat unflagged run fee, a `lepidata`-shape real per-row `job` event, and a decoy per-row description that mentions "run" without the exact phrase) and a full `bin/_unit_price_selftest.py` replay (1176 listings, 26 moved — byte-identical to the pre-fix baseline via `git stash`, all 26 the pre-existing documented FLAT-schema replay gap, none caused by this change).

**Lightweight recheck (verified live 2026-10-28): one genuine new partial undercutter among this cycle's newest unnamed listings, the rest ruled out.** `exciting_pawpaw/substack-scraper` (6 users, created 2026-10-09) bills one flat `result` event at **$0.001** (full text or metadata, same price) plus a flat **$0.001** one-time Actor-start fee — cheaper than us above ~1-2 posts/run on Free, Bronze and Silver ($0.002/$0.0018/$0.0015 here), but we stay cheaper at Gold and above ($0.00078) at any run size since its per-post rate alone ($0.001) exceeds our Gold+ floor. Its own description doesn't mention comments-as-a-separate-charge, category/leaderboard discovery or Notes, so our scope stays wider — same partial-undercutter shape as `lergassy`/`hata1234`/`sian.agency` already on this page. Seven more unnamed listings surfaced in the same sweep, all ruled out: `email_scraper/substack-email-scraper` (18u) and `premiumscraper/substack-email-scraper` (14u) are both contact-email/lead-gen tools, the same non-substitute class as the already-excluded `contactminerlabs`/`sourabhbgp` listings; `brick_joey_yto/substack-notes-scraper` (5u) scrapes Notes only, which we don't offer, same class as the other excluded Notes scrapers; `automation_craft/substack-scraper` (4u) tiers post+post-content to $0.004 Free / $0.0032 Gold+ combined plus a $0.005 start fee — dearer than us at every tier; `samwise.agency/substack-scraper` (3u) and `fast_api/substack-scraper` (3u) both bill a flat $0.01/result, 5x–13x our rate; `devilscrapes/substack-newsletter-scraper` (3u) carries a $0.2 one-time start fee alone exceeding our whole-run cost on any normal-sized job. No README dollar figures were stale elsewhere on this page — the only edit this cycle needed was the `dacoder` update above.

## FAQ

**Does it get paywalled content?** No. It returns exactly what a logged-out visitor can see, and it tells you when that is less than the whole article. Substack serves a *free preview* of most subscriber-only posts — a real body, but cut off partway through, while the post's own `wordCount` still reports the full length. Re-measured live across 69 posts from 7 publications: paid posts returned 0%–97% of the declared word count (median 34%), free posts 98%–140% (median 101%), and preview length is a per-publication setting — 2–5% on one publication, 25–37% on another, 34–46% on a third. Note that the listing's `audience` field is **not** a reliable proxy: 4 of the 27 paid posts in that sample came back essentially whole (96%–97%), because publications unlock posts without changing the flag. Rows that really are short come back with `bodyTruncated: true` and a `bodyWordCount` well below `wordCount`, so you can filter or discount them instead of mistaking a preview for a full article. Posts with no public body at all are `bodyTruncated: true` with an empty `bodyText`. There is no login or paywall bypass, by design.

**`authors` came back `[]` and `publicationName` came back `null` on a real post from a real publication — is that a bug?** No, and it's not gated by any input option — `publicationName`/`authors` both come from Substack's own `publishedBylines` field on the post object, and on some publications Substack simply leaves it an empty array on most posts, including in the full per-post detail (not just the lighter archive listing). Measured live (2026-10-12) across 8 real publications: 100% of posts carried a non-empty `publishedBylines` on `astralcodexten`, `bigtechnology`, `garbageday`, `noahpinion`, `newcomer` and `pirate-wires`, but only **2 of 23 (9%)** did on `jcbruce.substack.com` — a normal, actively-published single-author newsletter, not a team blog or an edge case. We can't infer the author Substack itself won't name. `publicationUrl` is unaffected — it's built from the publication you asked for, not from this field — so use it, not `publicationName`, if you need a reliable per-row publication key.

**How do I avoid paying for previews?** Set `audienceFilter: "free"` — public posts only, which are the ones that come back complete. The filter is applied from the archive listing, before any body is fetched or charged.
**What if I list the same publication or post twice?** Deduped automatically — `publicationUrls`/`postUrls` entries that resolve to the same origin or the same post are only fetched (and charged) once.

**Does it work with custom domains?** Yes — pass either the `*.substack.com` handle or the custom domain; redirects are followed either way, **with one exception** — see the next question.

**I passed a bare handle (`"lennysnewsletter"`) and got 0 rows with a "redirected to a Substack profile page" message, even though the publication is real and active.** A small number of publications' `<handle>.substack.com` no longer redirects to the newsletter's own site — it 302s to a `substack.com/@handle` *profile* page instead, which returns HTML, not the archive JSON this Actor reads. Verified live (2026-10-20): 1 of 6 well-known newsletters sampled this way (`lennysnewsletter` → `https://substack.com/@lennysnewsletter`); the other 5 (`platformer`, `theankler`, `bigtechnology`, `garbageday`, `stratechery`) all redirected correctly to their real site. **Re-measured the same day at 5x the sample size (30 newsletters): 2/30 redirected** (adding `divinity` → `https://substack.com/@divinity`) — see [the dedicated guide](https://fetchsmith.com/blog/substack-bare-handle-redirects-to-profile-not-archive) for the full breakdown and why status code, redirect-family and body-presence checks all pass on the broken case. The fix is the one in the error message — pass the exact custom domain or full `https://<handle>.substack.com` URL you'd actually visit in a browser (e.g. `lennysnewsletter.com`) instead of the bare handle; the Actor cannot derive it from the handle alone once this redirect shape is in play.

**Why are comments optional?** They're charged like posts, and a popular post can have hundreds. Turn them on with `includeComments` and bound them with `maxCommentsPerPost`.

**I turned on `includeComments` and got no comments, even though the posts show hundreds.** The comment section of a subscriber-only post is paywalled too, and Substack's API says so by answering `200 OK` with an empty list rather than an error. Measured live across three publications, the split is total: all 15 public posts sampled returned their full tree (318–1200 comments, no server-side cap), and all 15 subscriber-only posts returned **zero** — one of them on a post declaring 5,426 comments. Those rows come back `commentsWithheld: true` with `commentsRetrieved: 0`, and the run log and status message both name the count, so it is visible rather than looking like a broken run. Set `audienceFilter: "free"` to scrape only posts whose comments you can actually get. You are never charged for a comment that wasn't returned.

**What's the difference between `leaderboardOnly` and `discoverCategories` + `includePublicationInfo`?** Both read the same Substack leaderboard data, but `discoverCategories` alone uses the leaderboard only to find publications, then scrapes their posts (charged per post). `leaderboardOnly: true` skips the post scraping and returns the leaderboard rows themselves — rank, subscriber counts, pricing — as the entire result, at a fraction of the cost of a post-scraping run. Use it for "who are the top 20 paid tech newsletters and what do they charge", not "give me their articles".

**I set `minReactionCount`/`minWordCount`/`audienceFilter`/etc. together with `leaderboardOnly` and nothing changed.** Expected — leaderboard rows are publication summaries, not posts, so post-level filters (`audienceFilter`, `contentType`, `publishedAfter`/`publishedBefore`, `minReactionCount`, `minCommentCount`, `minRestackCount`, `minWordCount`, `maxWordCount`) have nothing to apply to and are ignored (the run log carries a warning naming them). To filter individual posts by engagement or word count, run without `leaderboardOnly`.

**I set `discoverType: "podcast"` and got zero rows.** `discoverType` filters the *publications* Substack's category leaderboard returns, and those leaderboards are almost entirely `newsletter`-type publications — we swept the whole technology leaderboard live (300 publications, 12 pages, both the `all` and `paid` tiers) and found not a single podcast-type one; even Substack's dedicated `podcast` category is only about 3% podcast-type. So `discoverType: "podcast"` legitimately matches nothing in most categories, and raising `maxPublicationsPerCategory` cannot help because the whole leaderboard has already been read. The run log and status message now say exactly this instead of pointing at the cap. If what you actually want is podcast **episodes**, leave `discoverType: "all"` and set `contentType: "podcast"` — newsletter-type publications do publish podcast posts (a `discoverCategories: ["technology"]` run returns `postType: "podcast"` rows from `newsletter.pragmaticengineer.com`, verified live).

**What's the difference between `requirePodcast` and `discoverType: "podcast"`?** `discoverType` filters on the publication's *type classification*, which is almost always `newsletter` even when the publication also runs a podcast (see the previous FAQ entry). `requirePodcast` instead reads Substack's own `podcast_enabled` flag — the same field this Actor already exposes as `publicationHasPodcast` — which is a much more common signal: a live sweep of the `technology` leaderboard (2026-10-29) found 15 of 72 top publications (~21%) had it set, while scanning every category/subcategory for one where `requirePodcast` or `requirePaymentsEnabled` drops an *entire* category found none — both flags are common enough on real leaderboards that, unlike `discoverType: "podcast"`, you should expect these filters to actually narrow a category rather than empty it. `requirePaymentsEnabled` is the data-level equivalent of `leaderboardTier: "paid"` — use it when you want to combine `leaderboardTier: "all"` (or `discoverType`/`requirePodcast`) with "and only the monetized ones."

**The status message says "the Substack leaderboard request failed" or "the leaderboard returned no publications".** These are two different causes and the message names which one you hit. A *failed request* is transient (Substack rate-limits or a 5xx) — just re-run; changing `discoverCategories`, `leaderboardTier` or `maxPublicationsPerCategory` cannot help, because the leaderboard was never read. A leaderboard that genuinely *returned nothing* is rare: we checked all 33 Substack categories against all three `leaderboardTier` values live (2026-09-25) and every single combination returned a full page of publications, so if you see it, try `leaderboardTier: "all"` or a category slug straight from `substack.com/api/v1/categories`. Raising `maxPublicationsPerCategory` is never the fix for either case — it is a cap on how many publications to *keep*, not how deep to look.

**I set `leaderboardTier: "free"` expecting free-only newsletters.** Substack's category leaderboard API does not actually have a free-only tier. Verified live (2026-09-26) across 3 categories at every page depth: `.../category/public/<id>/free` returns the byte-identical publication list, in the same order, as `.../all` — it never filters anything out. Only `all` (everyone) and `paid` (a genuinely separate, paid-subscriber-ranked list) are real. `leaderboardTier: "free"` still runs (it's kept for backwards compatibility and the run log warns when you use it) but it is equivalent to `"all"`, which mixes free and paid-tier publications — there's no reliable way to reconstruct a true free-only list client-side either, since a publication's `payments_state` field does not predict membership in the `paid` leaderboard. If you specifically want monetized newsletters, use `leaderboardTier: "paid"`.

**How far back can it go?** The whole archive — `maxPostsPerPublication` up to 5,000 posts per publication, paginated 50 at a time.

**I used a filter and got far fewer posts than I expected.** `maxPostsPerPublication` is a *scan depth*: it counts posts read from the archive, before `audienceFilter`, `contentType`, `publishedAfter`/`publishedBefore` and the `minReactionCount`/`minCommentCount`/`minRestackCount`/`minWordCount`/`maxWordCount` filters are applied. Searching `astralcodexten` for `prediction` with `publishedAfter: 2024-06-01` returns 2 posts at the default depth of 50 but 23 at depth 100 — the rest were simply never reached. `searchQuery` makes this easier to hit, because Substack returns search matches in relevance order rather than newest-first. When you combine filters, raise `maxPostsPerPublication` well above the number of rows you want; the run log and status message will tell you when a run was cut short this way. Only `maxResults` affects what you pay for.

**I passed a malformed `publishedAfter`/`publishedBefore` and the run failed instead of just ignoring it.** By design, since 2026-10-21. Both fields are parsed strictly as `YYYY-MM-DD`; before this, a non-empty value that failed to parse became JavaScript's `Invalid Date`, which is truthy but compares `false` to everything — so the filter silently matched every post instead of bounding anything, the opposite of a visible failure. Now a value that isn't empty and isn't `YYYY-MM-DD` throws immediately, naming the field and the bad value, rather than quietly widening the result set.

**Is it reliable?** It uses documented-shape public JSON endpoints rather than HTML parsing, so it doesn't break when Substack restyles its site. Runs are tested nightly.

**Rate limits?** Requests are retried with backoff on 429/5xx. For very large jobs, split them across runs or lower concurrency by running publications separately.

## Related guides
Engineering write-ups behind this Actor:
- [Substack's archive API returns a body_html field for every post — it's just always null](https://fetchsmith.com/blog/substack-full-text-json-api)
- [HTTP-only vs headless browser scraping: a timed benchmark](https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost)
- [A Substack paywalled post returns a body_html that looks complete — it's a preview, and `audience` won't tell you](https://fetchsmith.com/blog/substack-paywalled-post-preview-vs-full-text)
- [Substack, Apple Podcasts, Google News and Hacker News — four free APIs where the first response isn't the finished product](https://fetchsmith.com/blog/public-content-apis-hidden-second-step) — how this Actor's second-step trap compares to the other three content platforms we scrape.
- [A bare Substack handle can redirect to a profile page instead of the archive](https://fetchsmith.com/blog/substack-bare-handle-redirects-to-profile-not-archive) — measured across 30 live newsletters; the 302 lands on a real `200` HTML page, not an error.


---

Built and maintained by [FetchSmith](https://fetchsmith.com) — small, fast, HTTP-only scrapers. Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/substack-scraper

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools) — HTTP-only Actors for public data sources, no browser required.

Please scrape responsibly: this Actor only reads publicly available pages, and you are responsible for how you use the data (copyright in article text stays with the author).
