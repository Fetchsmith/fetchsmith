---
title: Apple's App Store review feed has holes — and an iPhone User-Agent sees a different feed entirely
description: The same App Store customer-reviews RSS URL returns 50 entries or an empty feed depending on the page number, the sort order, and whether your User-Agent looks like an Apple device. Measured, with the numbers.
date: 2026-09-09
tags: webscraping, app-store, ios, api
tool: app-store-reviews-scraper
---

> **Correction, 2026-09-10.** The original version of this post (published 2026-09-09) claimed that empty App Store review feeds are caused by request-header *fingerprinting*, and that rotating a handful of browser User-Agents "unlocks" a feed that a plain `curl` can't see. **That explanation was wrong**, and so was the fix built on it. We re-tested it properly and found two different real mechanisms: Apple's paginated feed contains **holes** (empty pages in the middle of a result set), and there are **two separate feeds** — one served to Apple-device User-Agents and one to everything else — that can contain *completely different reviews*. This post has been rewritten around the measurements below; the URL is unchanged so existing links still work. We ship data for a living, so a correction is worth more to you than a quietly edited page.

If you scrape Apple's undocumented App Store review feed (`itunes.apple.com/<country>/rss/customerreviews/id=<id>/sortBy=<sort>/page=<n>/json`), you will hit this: a URL that worked yesterday returns a well-formed feed with zero `<entry>` elements. No error, no rate-limit header. It looks exactly like an outage.

It isn't. Here is what is actually going on, measured on 2026-09-10 from a plain cloud box with no proxy.

## Mechanism 1: the feed has holes

Apple caps this feed at 10 pages of up to 50 reviews. Those pages are **not** "full, full, …, partial, then empty forever". Empty pages appear *in the middle* of a result set, and the pattern differs per app, per storefront and per sort order:

| App / storefront / sort | Entries returned on pages 1 → 10 | Unique reviews |
|---|---|---|
| Spotify / us / `mostRecent` | 0, 0, 0, 0, **50**, 0, 0, 0, 0, 0 | 50 |
| Spotify / us / `mostHelpful` | 0, 0, 0, 0, **50**, 0, 0, 0, **50**, 0 | 100 |
| Notion / us / `mostRecent` | 0, **50**, 0, 0, 0, 0, 0, 0, **50**, 0 | 100 |
| Notion / us / `mostHelpful` | 0, 0, 0, 0, 0, 0, **50**, 0, 0, 0 | 50 |
| Spotify / gb / `mostRecent` | 0, 0, 0, 0, **50**, 0, 0, 0, **50**, 0 | 100 |

Page 1 being empty is the trap. Almost every scraper written against this endpoint — ours included, for 56 build cycles — does some version of:

```js
if (!entries.length) break;   // ← silently returns zero for Spotify/us
```

A hole at page 1 ends the scrape before it starts, and the run reports "no reviews found" with a green checkmark on it. **On a fixed-size page range, `continue` past empty pages; never `break`.** Only use `break` where the API hands you a real end-of-list cursor.

The holes are also sticky within a session — six identical back-to-back requests to an empty key returned empty 6/6 — but they **move over time**: cycle-to-cycle we have seen Spotify/us/`mostHelpful` as `50,50,0,0,0,0,50,0,0,0` on one day and `0,0,0,0,50,0,0,0,50,0` on the next. So retrying the same URL harder does nothing in the moment, and a hole map you cached yesterday is worthless today. Scan the range every run.

## Mechanism 2: two feeds, not one — and the iOS one is bigger

Now the part that is genuinely about headers, just not the way we first thought. Send the *identical* URL with an iPhone or iPad User-Agent and you get **a different feed**, not a "more unlocked" version of the same one:

| Sweep of pages 1–10, us storefront, `mostRecent` | `curl/8.5.0` UA | iPhone Safari UA | Overlap |
|---|---|---|---|
| Spotify (id 324684580) | 50 unique reviews | **200 unique reviews** | **0** |
| Notion (id 1232780281) | 100 unique | **250 unique** | 100 |
| Spotify, `gb` storefront | 100 unique | 150 unique | 50 |

For Spotify/us the two sweeps have **zero reviews in common**. Not a superset — a disjoint set. The union is 250 reviews; either User-Agent alone gets you at most 200 of them, and the naive `curl` sweep gets you 50.

Which User-Agents flip the switch? We tested one key (Spotify/us/`mostRecent`, page 1 empty for `curl`, page 5 full for `curl`), interleaving the requests so time couldn't confound the result — the split was perfectly reproducible over six rounds:

| User-Agent | page 1 | page 5 |
|---|---|---|
| `curl/8.5.0` | 0 | 50 |
| Chrome on macOS | 0 | 50 |
| Safari on macOS | 0 | 50 |
| Chrome on Android (has `Mobile` token) | 0 | 50 |
| *(no User-Agent header)* | 0 | 50 |
| **Safari on iPhone** | **50** | **0** |
| **Safari on iPad** | **50** | **0** |

So it is not "browser vs bot", and it is not "mobile vs desktop" — Android Chrome carries `Mobile` and lands with everything else. The dividing line is whether the UA claims to be an **Apple device**. Two client classes, two independently paginated indexes over the same underlying review pool, each with its own holes.

## What was wrong with the old advice, and why it survived so long

The original post recommended a 4-variant header rotation that fires on an empty page and caches the winning variant. That advice fails on both counts:

- It **cost up to 4× the requests** on every page that came back empty — and with holes everywhere, that is most pages.
- Worse, it **hid the real bug**. When a scraper has "tried four fingerprints" and still sees nothing, "it's genuinely empty" feels well-earned. It isn't: the loop had simply stopped at page 1 and never looked at page 5. Retry machinery is very good at making a wrong diagnosis feel thorough.

The lesson we'd actually pass on: **test the anti-bot theory before building machinery for it.** Fire the same URL twice under two User-Agents and diff the results. That five-line test is what finally separated "Apple blocks bots" (false) from "Apple serves Apple devices a different index" (true, and worth 4× the data).

## What to do instead

1. **Sweep the whole page range** (1–10) and skip holes. Never treat an empty page as end-of-feed.
2. **Sweep both client classes** — one pass with a default HTTP UA, one with an iOS Safari UA — and **dedupe by review id**. On the apps above this is 1.5×–5× the rows for 2× the requests.
3. **Retry the other sort order** when one is thin. `mostRecent` and `mostHelpful` are separate indexes over the same pool with different holes; the same app can be empty under one and full under the other.
4. **Then probe other storefronts.** Coverage genuinely differs by country — an app can have real reviews in `gb` and none at all in `us` — and that is a different answer from "no reviews anywhere."
5. **Say which path served the data.** Tag every row with the sort order, the storefront and whether a fallback fired. A scraper that can't tell "Apple had nothing" from "our loop stopped early" is shipping silent failure.

## Packaged version

[app-store-reviews-scraper on Apify](https://apify.com/fetchsmith/app-store-reviews-scraper) does steps 1, 3, 4 and 5 today: full-range page scanning with hole skipping, dedupe by `reviewId`, automatic sort-order fallback (every row carries `sortUsed`), and an opt-in `countryFallback` that pulls from a working storefront when the requested one is genuinely empty (rows tagged `requestedCountry`/`fallbackUsed`). The dual-client-class sweep from step 2 is the finding above, measured today — it's going into the next build. Pay-per-review pricing, no browser, no proxy required.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; findings above come from real runs against live endpoints, not documentation. When we get something wrong, we correct it in place and say so.*
