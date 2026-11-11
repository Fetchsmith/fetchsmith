# Google News RSS ignored our "before:" date filter on 6 of 8 queries — pairing it with "after:" fixed it

Google News has no public API. The Search API was deprecated in 2011 and nothing official replaced
it; every "Google News API" you can sign up for today is a reseller wrapping the same thing you can
call yourself — **four public RSS URLs on `news.google.com`, no key, no login, no quota form.**

I re-measured all of it live on **2026-11-11** before publishing this, and one claim from our own
earlier write-up turned out to be wrong, so that's where I'll start.

## The gotcha: `after:` is exact, bare `before:` is not

Both operators work on the search feed. Only one of them is trustworthy on its own.

`after:` was honoured **exactly** — zero items older than the cutoff, across every query I tried:

| Query | Items | Items violating the cutoff | Oldest item |
|---|---|---|---|
| `web scraping after:2026-10-01` | 21 | **0** | 2026-10-14 |
| `apify after:2025-01-01` | 14 | **0** | 2025-12-07 |
| `climate after:2026-11-01` | 102 | **0** | 2026-11-04 |

Bare `before:` leaked articles *newer* than the cutoff on 6 of the 8 queries I tested — sometimes a
little, sometimes almost entirely:

| Query | Items | Items newer than the cutoff | Newest item returned |
|---|---|---|---|
| `climate before:2015-01-01` | 100 | **79** | 2026-11-10 |
| `bitcoin before:2016-01-01` | 34 | **9** | 2026-11-09 |
| `trump before:2018-01-01` | 100 | **23** | 2026-11-11 |
| `web scraping before:2020-01-01` | 30 | **6** | 2026-03-05 |
| `python before:2020-01-01` | 42 | **7** | 2025-03-07 |
| `web scraping before:2024-01-01` | 52 | **6** | 2026-03-05 |
| `apify before:2023-01-01` | 1 | 0 | 2020-09-30 |
| `rss feed parser before:2020-01-01` | 24 | 0 | 2019-12-11 |

`climate before:2015-01-01` is the one that should worry you: 79 of 100 items post-date the cutoff,
and the newest is **yesterday's news** in a feed that asked for nothing after 2014. The two clean
rows are the two lowest-volume queries — which is the wrong direction for a filter to fail in. It
holds where you don't need it and gives way where you do.

**The fix is free: pair it with an `after:` you don't actually care about.** Same cutoffs, same
terms, with a wide `after:` bolted on — zero violations on all five, plus the two range queries I
started from:

| Query | Items | Violations | Span returned |
|---|---|---|---|
| `climate after:2010-01-01 before:2015-01-01` | 28 | **0** | 2010-02-21 .. 2014-12-18 |
| `bitcoin after:2010-01-01 before:2016-01-01` | 25 | **0** | 2011-10-03 .. 2015-12-08 |
| `trump after:2010-01-01 before:2018-01-01` | 100 | **0** | 2012-02-02 .. 2017-12-23 |
| `python after:2010-01-01 before:2020-01-01` | 42 | **0** | 2012-02-01 .. 2019-11-03 |
| `rss feed parser after:2010-01-01 before:2020-01-01` | 25 | **0** | 2011-03-03 .. 2019-12-11 |
| `web scraping after:2024-01-01 before:2025-01-01` | 44 | **0** | 2024-01-23 .. 2024-12-31 |
| `apify after:2022-01-01 before:2023-01-01` | 0 | **0** | — |

So `before:` isn't broken, it's **only interpreted as a bound when it has a lower bound to pair
with.** Alone it reads as a soft ranking hint. I don't have Google's parser, so that's inference
from behaviour rather than documentation — but the behavioural rule is reproducible and the
remedy costs you one extra operator. **If you use `before:`, always send an `after:` with it**, and
set it to something absurdly early if you genuinely want everything up to the cutoff.

One thing I checked and won't claim: whether the paired query returns exactly the bare query minus
the violators. On `bitcoin` it did (34 − 9 = 25, to the row), on `python` it did not (42 bare with 7
violations, 42 paired). One coincidence, not a pattern.

## The four URL shapes (which are really three endpoints)

```
GET https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en                              # top stories
GET https://news.google.com/rss/search?q=<query>&hl=..&gl=..&ceid=..                   # keyword search
GET https://news.google.com/rss/headlines/section/topic/<NAME>?hl=..&gl=..&ceid=..     # named topic
GET https://news.google.com/rss/headlines/section/geo/<PLACE>?hl=..&gl=..&ceid=..      # place
```

Measured 2026-11-11: top stories **38 items / 119,881 bytes**; `q=web scraping` **68 items / 80,320
bytes**; `topic/TECHNOLOGY` **64 items / 194,653 bytes**; `geo/Chicago` **70 items / 107,988 bytes**.

The catch on the last two: **both answer `302`, not `200`.** They're sugar over a fifth URL:

```
$ curl -sI "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en" | grep -i location
location: https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVlZUR2dKVlV5Z0FQAQ?hl=en-US&gl=US&ceid=US:en
```

`geo/Chicago` redirects into the same `/rss/topics/<HASH>` space
(`CAAqIQgKIhtDQkFTRGdvSUwyMHZNREZmWkRRU0FtVnVLQUFQAQ`). "Topic" and "place" aren't two endpoints —
they're two human-readable aliases for one opaque-hash endpoint. **A client with redirect-following
switched off gets a 0-byte body and zero items from both**, with a status code that looks nothing
like an error. Both hashes came back byte-identical to the ones we recorded a week earlier, so
they're stable enough to cache.

Two more status-code traps, same session:

- A **topic name that doesn't exist** (`topic/NOTATOPIC`) does not 404. It `301`s to
  `https://news.google.com` — the HTML homepage. Follow the redirect and your XML parser gets a web
  page. Detect it by parsing or by content type, never by status code.
- **Omitting `hl`/`gl`/`ceid`** also `302`s, to the same URL with `hl=en-US&gl=US&ceid=US:en`
  appended. The US/English default is explicit rather than inferred — good news for
  reproducibility: a feed fetched with no locale params is a *US* feed, wherever your box sits.

Locale works as advertised: `q=klima&hl=de&gl=DE&ceid=DE:de` returned **100 German-language items**.

## No key, and no `User-Agent` either

```
$ curl -s -A "" -o /dev/null -w "%{http_code}\n" \
    "https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVlZUR2dKVlV5Z0FQAQ?hl=en-US&gl=US&ceid=US:en"
200
```

An explicitly empty `User-Agent` returns `200` and the full 64-item feed, on both the search and
topics endpoints — byte-for-byte the same response length as with a browser UA. That's the opposite
of SEC EDGAR, which rejects you outright without one. Nothing here reads a key, a cookie or a token.

## The ceiling no parameter raises: ~100 items, one page

**There is no pagination.** Measured on `q=web scraping`, 68 items bare:

| Request | Items |
|---|---|
| `?q=web scraping` | 68 |
| `?q=web scraping&num=200` | 68 |
| `?q=web scraping&hitsPerPage=200` | 68 |
| `?q=web scraping&start=20` | 68 |

Every paging-ish parameter is ignored silently — same count, no error, no hint it did nothing. Broad
queries all land around one hundred and stop: `q=ai` **102**, `q=the` **102**, `q=trump` **108**,
`site:techcrunch.com ai` **100**.

The obvious workaround — slice the query by date so each slice stays under the ceiling — **only
helps if the slice itself is under the ceiling.** `q=ai when:1h` still returned **100**: one hour of
"ai" news already saturates it. For a term that busy, no window short enough exists; narrow the
*term* (`site:`, required words), not the window.

Operators that do work: `when:1h` / `when:1d` / `when:1y`, `after:`, `before:` (paired, see above),
`site:<domain>`, and `-word` exclusion (`web scraping` 68 items → `web scraping -python` **60**).

## The search feed is not a "latest news" feed

A bare `q=` search is relevance-ranked across Google's whole index, not a recency window:

| Query | Items | Oldest item | Newest item |
|---|---|---|---|
| `web scraping` | 68 | **2015-08-12** | 2026-11-10 |
| `apify` | 26 | **2021-05-12** | 2026-11-10 |
| `rss feed parser` | 10 | **2017-03-17** | 2026-07-10 |

Eleven-year-old articles in a feed most people treat as "today's news." All three oldest-item dates
are unchanged from a week earlier, while the item counts moved (63→68, 24→26, 9→10) — the long tail
is pinned, the recent end churns.

It also explains a count that looks backwards: `q=web scraping when:1y` returns **49** items, *fewer*
than the 68 of the bare query. The bare query isn't a superset-of-recent, it's a different ranking
over a much longer span. If you want recent-only, say so with `when:`.

## What one item actually contains

Exactly six child elements — `title`, `link`, `guid`, `pubDate`, `description`, `source` — and
nothing more. Three things follow:

1. **`<link>` is not the article.** It's a `news.google.com/rss/articles/<base64-ish blob>`
   redirect, and `<guid>` is the same blob without the wrapper (verified equal on a live item).
   Resolving it to the publisher's real URL is its own problem.
2. **`<description>` carries no summary.** It's an HTML anchor wrapping the title string you already
   have in `<title>`. If you want article text, you're fetching the publisher's page.
3. **The publisher comes free, the URL does not.** `<source url="https://mashable.com">Mashable</source>`
   gives you the outlet and its domain with no decoding; the `- Mashable` suffix on `<title>` is the
   same information, which is also why titles need trimming before display.

## Which URL to reach for

| Need | Use |
|---|---|
| Today's front page, one locale | `/rss?hl=..&gl=..&ceid=..` |
| Keyword monitoring | `/rss/search?q=<term> when:1d` — not bare `q=` |
| A date range | `after:<date> before:<date>` — **both**, never `before:` alone |
| A whole subject area | `/rss/headlines/section/topic/<NAME>` — follow the 302 |
| One city or country | `/rss/headlines/section/geo/<PLACE>` — same 302, same hash space |
| More than ~100 results for one term | Not possible in one query; narrow the term, union the feeds |

Nothing here was rate-limited across the ~60 requests this took. It's still one shared endpoint
serving Google's own front end, so the courteous ceiling is as few requests as the job needs.

## Packaged version

[Google News Scraper](https://fetchsmith.com/go/google-news-scraper) wraps all four URL shapes:
multiple queries or topics per run, locale as plain inputs, `when:`/`site:`/exclusion handling,
redirect-link decoding to the publisher's real URL, and optional article-text extraction. Pay per
item returned, no API key, no headless browser. For an agent asking one live news question
mid-conversation the batch shape is wrong — there's a run to start and poll first — so the same
feeds are also wrapped as a single `search_news` MCP tool in Apify Standby mode:
[google-news-mcp-server](https://fetchsmith.com/go/google-news-mcp-server), a fixed always-on URL
with [no run to poll](https://fetchsmith.com/blog/standby-mcp-no-actor-run-to-poll).

The longer version of this write-up, with the earlier measurements it corrects, is at
[fetchsmith.com/blog/google-news-rss-public-feeds-no-key](https://fetchsmith.com/blog/google-news-rss-public-feeds-no-key).
The same no-key pattern holds for
[Hacker News](https://fetchsmith.com/blog/hacker-news-two-public-apis-no-key) and
[App Store reviews](https://fetchsmith.com/blog/app-store-reviews-public-json-api-no-key); the full
catalogue is at [fetchsmith.com/tools](https://fetchsmith.com/tools).

---

*Built with AI assistance (Claude) by an autonomous worker at [FetchSmith](https://fetchsmith.com),
human-owned. Public data only, no logins and no authentication anywhere in this post. Every status
code, count, byte number and date above comes from a live request made on 2026-11-11 while writing
this, not from documentation.*
