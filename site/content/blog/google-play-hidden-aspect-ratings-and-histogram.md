---
title: Google Play's review API carries two fields almost nobody reads — a full star histogram and a hidden per-review "aspect" breakdown
description: Every Google Play app record ships a 1-5 star histogram that reconciles with the public rating count to within 0.0001%, and roughly a quarter of reviews carry per-aspect thumbs Google's own web UI never renders — including categories its internal taxonomy names "never display."
date: 2026-09-24
tags: webscraping, api, googleplay, json
tool: google-play-reviews-scraper
---

We already wrote about the [batchexecute endpoint that makes Google Play reviews scrapable at all](/blog/google-play-reviews-no-api-batchexecute). Two fields that ride along on the same calls didn't make that post, and both are worth a closer look — one is a reliable data point almost no review scraper surfaces, the other is a genuinely undocumented one.

## The histogram is real, not a display artifact

Every app-details response carries a `histogram` object — a count of ratings at each star level, 1 through 5. It's easy to assume this is a rounded, cosmetic number cooked up for the star-bar graphic on the store page. Live-checked across four apps with very different rating volumes, it isn't: the histogram sums to the app's public `ratings` total almost exactly.

| App | `ratings` (total) | histogram sum | difference |
|---|---:|---:|---:|
| Spotify | 36,360,620 | 36,360,604 | -0.0000% |
| WhatsApp | 244,287,322 | 244,287,243 | -0.0000% |
| Duolingo | 49,102,744 | 49,102,711 | -0.0001% |
| Candy Crush Saga | 38,932,893 | 38,932,880 | -0.0000% |

The gap in every case is a handful of ratings out of tens of millions — almost certainly write skew between the two counters in the seconds between the two calls we made, not rounding. That makes the histogram a genuine per-star breakdown, not a decorative approximation, and it's a field the Actor already returns on every `recordType: "app"` row (`histogram`) that most review scrapers don't expose at all — useful for anyone tracking whether a rating average is drifting because of real sentiment change or because a burst of 1-star reviews just landed.

## `aspectRatings`: the per-review data Google Play's own UI doesn't show

The reviews endpoint also returns a `criterias` array on some reviews — things like `{"criteria": "vaf_app_quality_ads_frequency", "rating": 2}`, effectively a per-aspect thumbs score attached to a single review. None of the top 3 Store-leader competitor Actors by users expose it in their output schema (re-verified 2026-09-17). We map it through as `aspectRatings`.

Sampling 200 of the newest reviews on each of the same four apps (800 reviews total):

| App | Reviews with ≥1 aspect rating | Distinct aspect names seen |
|---|---:|---:|
| Spotify | 72 / 200 (36%) | 19 |
| WhatsApp | 50 / 200 (25%) | 15 |
| Duolingo | 23 / 200 (12%) | 12 |
| Candy Crush Saga | 73 / 200 (37%) | 50 |

Overall: **218 of 800 reviews (27.3%) carried at least one aspect rating**, across 603 individual criteria entries. The taxonomy is category-aware, not one fixed list: the two utility apps (WhatsApp, Duolingo) mostly get generic `vaf_app_quality_*` tags (usability, stability, battery, ads) plus a couple of feature-specific ones (`vaf_phase1_voice_messaging` on WhatsApp). The game got a much richer set — `vaf_games_genre_match_3_v1`, `vaf_player_resonance_motivation_system_completion`, `vaf_games_graphic_style_cartoon_v2` — Google Play is clearly running a genre-specific classifier over game reviews that a chat or education app never triggers.

## The categories literally named "never display"

The one finding worth flagging on its own: **11 of the 603 criteria entries (1.8%) use a `vaf_never_display_*` prefix**, and at least one showed up on every single app tested — `vaf_never_display_ease_of_use` and `vaf_never_display_inappropriate_ads` on WhatsApp, `vaf_never_display_app_description` and `vaf_never_display_considerate_of_time` on Duolingo, `vaf_never_display_difficult_to_use` on Candy Crush, `vaf_never_display_ease_of_use` and `vaf_never_display_battery_efficiency` on Spotify.

The naming is Google's own — this isn't a value we're inferring. It reads as an internal instruction to whatever renders Google Play's own review UI ("do not surface this category to users"), and that instruction is honored on the store page: none of these labels appear anywhere in the Play Store app. But the instruction lives in the label, not in the API response, so the raw JSON this endpoint returns includes them in the same array as every normally-displayed aspect, with no flag distinguishing the two. If you're building anything that assumes `aspectRatings` reflects only what Google itself considers presentable, it doesn't — filter by name if that distinction matters to your use case.

## Packaged version

[google-play-reviews-scraper on Apify](https://apify.com/fetchsmith/google-play-reviews-scraper) returns both fields as part of every run at no extra cost — `histogram` on the one app-details row per app, `aspectRatings` on every review that carries one. See the [first Google Play guide](/blog/google-play-reviews-no-api-batchexecute) for the `num`/`country`/`language` behavior and the invalid-app-id error asymmetry, and [how each platform's "empty" means something different](/blog/app-store-review-apis-three-silent-empties) if you're also pulling App Store or Steam reviews.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every number above comes from live calls made while writing this post.*
