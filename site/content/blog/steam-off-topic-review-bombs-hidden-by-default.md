---
title: Steam hides review-bomb reviews from its own score by default — includeOffTopic undoes it
description: When a game gets review-bombed over something unrelated to the game itself, Valve flags that stretch of reviews as off-topic and excludes them from the score Steam shows you. The exclusion is silent and the gap is large — measured on three games, live.
date: 2026-10-20
tags: webscraping, steam, gaming, api
tool: steam-reviews-scraper
---

Steam's review score is not simply "every review a game has ever received." When a large wave of reviews shows up over something that isn't about the game — a publisher decision, a storefront policy change, a controversy unrelated to the actual product — Valve's moderation marks that stretch of time as **off-topic review activity** and excludes those reviews from the public review score and review lists by default. If you pull reviews through Steam's own `appreviews` endpoint without knowing this, you get the filtered set and never see the gap.

## The flag, and what it does

Steam's `appreviews/<appid>` endpoint takes a `filter_offtopic_activity` parameter. `1` (Steam's own default) excludes off-topic-flagged reviews from the count and the list; `0` includes everything. Pulled fresh just now, no key, no login:

```
$ curl -s "https://store.steampowered.com/appreviews/214950?json=1&filter=all&language=all&purchase_type=all&filter_offtopic_activity=1&num_per_page=1"
{"query_summary": {"total_reviews": 88799, ...}}

$ curl -s "https://store.steampowered.com/appreviews/214950?json=1&filter=all&language=all&purchase_type=all&filter_offtopic_activity=0&num_per_page=1"
{"query_summary": {"total_reviews": 94696, ...}}
```

That's **5,897 reviews** for *Total War: ROME II* that exist on Steam's own servers but never show up in the default review count. Checked on two more games with well-known review-bomb history, same request, same day:

| Game | App ID | Default (off-topic hidden) | Unfiltered |
|---|---|---|---|
| Total War: ROME II | 214950 | 88,799 | 94,696 |
| War Thunder | 236390 | 792,328 | 917,795 |
| NARAKA: BLADEPOINT | 1203220 | 303,350 | 343,674 |

War Thunder's gap alone is **125,467 reviews** — more than most games get in total. This isn't a rounding effect or an edge case; for a game with an active review-bomb history, the hidden slice can be a meaningful fraction of the whole dataset.

## It isn't just the review list

The same flag changes the score Steam shows on the store page itself. `reviewScore` and `totalReviews` on a game's summary record are computed from whichever set `filter_offtopic_activity` selects — pull a game's summary with the flag off and its review count jumps by exactly the same gap shown above. A tool that reports a game's review score from one of these two numbers while pulling the review list from the other would show a score that doesn't match the reviews it just listed.

## Why the default is probably what you want — except when it isn't

Steam's own default (`1`, exclude off-topic) is the right choice for "what does this game's review score actually say about the game" — that's the whole point of the moderation flag, and it's why it's this Actor's default too. But it's the wrong choice for a different, equally legitimate question: **studying the backlash itself.** If a publisher's pricing change, a DRM decision, or a disabled feature triggered a wave of one-star "reviews" that aren't really about gameplay, those reviews *are* the data you want — Steam's exclusion is specifically designed to hide them from you.

There's no way to tell from a single pulled review whether it's been off-topic-flagged; the API doesn't expose a per-review flag, only the aggregate inclusion/exclusion. The only way to see the excluded set is to flip the parameter and diff.

## Packaged version

[steam-reviews-scraper on Apify](/go/steam-reviews-scraper) defaults to Steam's own `filter_offtopic_activity=1` behavior (because that matches the score Steam itself advertises), and exposes `includeOffTopic: true` as a one-line opt-in to pull the unfiltered set instead — for `dataType: "reviews"` and for the `reviewScore`/`totalReviews` fields on `dataType: "games"` rows alike, so a game row never reports a score that contradicts the reviews pulled alongside it in the same run.

If you're pulling reviews from more than one storefront, see [how App Store, Google Play and Steam each handle an "empty" result differently](/blog/app-store-review-apis-three-silent-empties) — three platforms, three different silent gotchas, none of them this one.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every status code, field name and number above comes from live requests made while writing this post, not from documentation.*
