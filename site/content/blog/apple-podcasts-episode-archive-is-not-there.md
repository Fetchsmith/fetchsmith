---
title: Apple's podcast API tells you a show has 2,752 episodes and then hands you 44
description: The episode lookup caps at 200, offset is silently ignored everywhere, and for high-frequency shows the index is decimated rather than truncated. The publisher RSS "escape hatch" is also trimmed more often than not. Four shows, measured.
date: 2026-10-17
tags: webscraping, api, podcasts, json
tool: apple-podcasts-scraper
---

Our [earlier Apple Podcasts post](/blog/apple-podcasts-public-json-api) mapped the four public JSON endpoints — charts, search, show lookup, episodes, reviews, no API key on any of them. One paragraph in it says that `limit` on the episode endpoint "caps out well before every episode ever" and that for a complete back catalogue you should take `feedUrl` and parse the publisher's own RSS.

The first half is true but far too vague. The second half is wrong often enough to break a pipeline. Here's what we measured.

## The ceiling is 200, and it clamps silently

```
GET https://itunes.apple.com/lookup?id=1434243584&country=us&entity=podcastEpisode&limit=N
```

Walking `N` upward against the Lex Fridman Podcast:

| `limit=` | `resultCount` | response bytes |
|---|---|---|
| 5 | 6 | 23,621 |
| 100 | 101 | 437,816 |
| 200 | 201 | 843,886 |
| 201 | 201 | 843,886 |
| 300 | 201 | 843,886 |
| 1000 | 201 | 843,886 |

(`resultCount` is one higher than the episode count throughout, because the show's own `wrapperType: "track"` row ships in the same array — filter by `wrapperType`, as the earlier post says.)

So 200 episodes is the hard ceiling, and everything above it returns **HTTP 200 with a byte-identical body**. No error, no warning, no `truncated` flag. Ask for 1,000 and the response looks exactly as healthy as asking for 200.

## `offset` doesn't work — on any endpoint, for any media type

The obvious fix is to page: `limit=200&offset=200`. Every offset returns the same first episode:

| request | first episode returned |
|---|---|
| `lookup?...&limit=5` (no offset) | `#502 – Psychiatry, Insane Asylums…` |
| `lookup?...&limit=5&offset=0` | `#502 – Psychiatry, Insane Asylums…` |
| `lookup?...&limit=5&offset=5` | `#502 – Psychiatry, Insane Asylums…` |
| `lookup?...&limit=5&offset=50` | `#502 – Psychiatry, Insane Asylums…` |
| `lookup?...&limit=5&offset=200` | `#502 – Psychiatry, Insane Asylums…` |
| `lookup?...&limit=5&offset=400` | `#502 – Psychiatry, Insane Asylums…` |

Identical `trackId` every time. This is the same silent-no-op shape we hit on [the FEC's donor-search API](/blog/fec-schedule-a-page-parameter-ignored), where `page=` is accepted and ignored on three of four endpoints — so the natural next question is whether some *other* endpoint on this host pages properly and we're just using the wrong one. We checked `/search`, and then checked a non-podcast media type to see whether this was podcast-specific:

```
search?term=true+crime&media=podcast&limit=5&offset=0 -> 1322200189,1464919521,1628964677,1089216339,987967575
search?term=true+crime&media=podcast&limit=5&offset=5 -> 1322200189,1464919521,1628964677,1089216339,987967575
search?term=beatles&media=music&limit=5&offset=0      -> 1441164426,1441133100,1441164359,1441164524,1441164495
search?term=beatles&media=music&limit=5&offset=5      -> 1441164426,1441133100,1441164359,1441164524,1441164495
```

Full ID lists, not just the first row — identical. Unlike the FEC case there is no working regime to switch to: `offset` is inert across `/lookup` and `/search` and across media types. There is no cursor field either. **The 200 is absolute**, not a page size.

## For some shows it isn't 200 — it's 44, and the gaps are in the middle

This is the part that will actually corrupt your data. Four shows, each at `limit=1000`, compared against `trackCount` from the show row in the same response:

| show | `trackCount` | episodes returned | oldest returned |
|---|---|---|---|
| Dan Carlin's Hardcore History | 13 | 13 | — complete |
| Lex Fridman Podcast | 502 | 200 | 2022-07-17 |
| Up First from NPR | 1,425 | 200 | 2026-04-11 |
| The Daily | 2,752 | **44** | 2025-12-14 |

The Daily returns 44 episodes. Not 200. And the easy assumption — "Apple keeps a short recency window for high-frequency shows" — is wrong, because those 44 episodes span **307 days**. A weekday-daily show over 307 days is roughly 215 episodes; we got 44 of them, from inside the window Apple does cover.

Looking at the dates explains it:

```
oldest 6 returned: 2025-12-14, 2025-12-21, 2025-12-28, 2026-01-18, 2026-01-25, 2026-02-01
newest 6 returned: 2026-10-10, 2026-10-11, 2026-10-14, 2026-10-15, 2026-10-16, 2026-10-17
```

The recent end is daily. The old end is **weekly** — all Sundays, 7 days apart, with one 21-day hole. Apple's episode index for this show is *decimated*, thinning out as it goes back, not truncated at a clean boundary. Largest gap between consecutive returned episodes: 21 days. 5 of the 43 intervals are over a week.

The practical consequence: if you take Apple's episode list for a high-frequency show and compute anything per-period — episodes per month, average duration by quarter, publishing cadence — you get a confident-looking number off by an order of magnitude, with no missing-data signal anywhere in the response. Up First and The Daily are both daily news podcasts; one gives you 200 dense episodes, the other 44 sparse ones. Nothing in the input tells you which you're getting.

## The free truncation detector nobody uses

The fix for *detecting* this is already in the response you have. The show row carries `trackCount` — the real catalogue size — in the same payload as the episodes:

```
trackCount: 2752, episodes returned: 44  -> truncated
trackCount: 502,  episodes returned: 200 -> truncated
trackCount: 13,   episodes returned: 13  -> complete
```

Compare `trackCount` against the number of `podcastEpisode` rows you actually got. If it's short, you are looking at a sample, and you should say so in your output rather than let a downstream consumer assume completeness. This costs nothing — no extra request, no calibration constant, no guessing at what the cap "should" be, which matters precisely because the cap is not a fixed 200.

## The RSS escape hatch is real, and it is not a full archive

So take `feedUrl` from the show record and parse the publisher's RSS — that's what our earlier post told you to do, and what our own code comments claimed gets you everything. For Lex Fridman it does: 502 `<item>` elements, 502 `<enclosure>` audio URLs, oldest `Sun, 26 Aug 2018`. Exactly `trackCount`. Complete.

Then we checked the other two:

| show | `trackCount` | Apple lookup | publisher RSS `<item>`s | RSS oldest | best obtainable |
|---|---|---|---|---|---|
| Lex Fridman Podcast | 502 | 200 | **502** | 2018-08-26 | 100% |
| Up First from NPR | 1,425 | 200 | 500 | 2025-06-30 | 35% |
| The Daily | 2,752 | 44 | 66 | 2021-10-24 | 2.4% |

Publishers trim their own feeds. Most podcast hosts default to a rolling window, because the feed is served to podcast apps on every refresh and nobody wants to ship a 50 MB XML file to a million clients an hour. NPR keeps 500. The Daily keeps 66 — and note its RSS reaches back to 2021 while holding only 66 items, so that feed is sampled too, exactly like Apple's index.

RSS is still unambiguously the better source — 500 beats 200, 66 beats 44, and it carries fields Apple's JSON never exposes (`episodeType`, full HTML show notes, enclosure byte size, transcript URLs). It is just not a complete archive, and for a long-running high-frequency show it is nowhere close. **If you need every episode a show ever published, no public endpoint will give it to you.** That archive exists only in the publisher's own CMS.

A corollary worth stating plainly, since `trackCount` makes it checkable: for The Daily, both of the two sources available to anyone — Apple's index and the publisher's feed — are missing more than 97% of the catalogue. A scraper that quietly returns 66 rows for a 2,752-episode show isn't broken; it has hit the edge of what is public. The difference between a tool you can trust and one you can't is whether it tells you that.

## Corrections to our earlier post

Two claims in [the earlier Apple Podcasts post](/blog/apple-podcasts-public-json-api) are now annotated there: "`limit` caps out well before every episode ever" is sharpened to the measured 200-or-fewer ceiling, and "for a complete back catalogue, parse the publisher's own RSS" is corrected — RSS is deeper, not complete. We'd rather fix the claim than leave a tidier version of it standing.

## The packaged version

Our [Apple Podcasts Scraper](/tools/apple-podcasts-scraper) already clamps `maxEpisodesPerPodcast` to Apple's 200 and ships a `useRssForFullArchive` option that pulls episodes from the publisher's feed instead (raising that clamp to 20,000), with a fallback to the lookup API if the feed fails — so the deeper source is one boolean, and every episode row carries a `source` field (`rss` or `itunes`) so you can tell which path produced it. Each podcast row also exposes `episodeCount`, mapped from `trackCount`, which is the comparison this post recommends you make.

What it does *not* yet do is warn you when `episodeCount` exceeds the rows it actually delivered — the detector is in your output but we don't raise it for you, and after measuring The Daily that's clearly the wrong default. That warning is queued.

For the endpoint map — charts, search, lookup, reviews, and the genre chart that returns 200 with silently unfiltered data — start with [the earlier post](/blog/apple-podcasts-public-json-api). The review-pagination holes on this same host are measured in [Apple's review feed has holes](/blog/apple-app-store-reviews-header-fingerprint). Full tool list at [fetchsmith.com/tools](/tools). [Run the Apple Podcasts scraper on Apify](/go/apple-podcasts-scraper).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every JSON snippet and number above comes from a live request made while writing this post, not from documentation.*
