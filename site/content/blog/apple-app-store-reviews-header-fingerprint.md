---
title: Apple's App Store review feed has holes — and whether you hit one depends on your HTTP client
description: The same App Store customer-reviews RSS URL returns 50 entries or an empty feed depending on the page number, the sort order, and what your HTTP client looks like. Three rounds of measurements, including two we had to correct.
date: 2026-09-09
tags: webscraping, app-store, ios, api
tool: app-store-reviews-scraper
---

> **Correction, 2026-09-10 (second update, same day).** This post has now been corrected twice, and the second correction retracts part of the first. The original (2026-09-09) blamed empty feeds on request-header *fingerprinting* and recommended rotating User-Agents — wrong. The first correction, earlier today, replaced that with two mechanisms: feed **holes** (right, and confirmed again below) and **two separate review indexes split by Apple-device User-Agent** (wrong — see the retraction under Mechanism 2). What survives all three rounds of measurement is: holes are real, they move, and *whether a given request hits one depends on what your HTTP client looks like to Apple* — but there is one index, not two. The URL is unchanged so existing links still work. We ship data for a living, so watching us correct ourselves in public is worth more to you than a quietly edited page.

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

## Mechanism 2: your HTTP client decides whether a page is a hole — but there is only one feed

**Retracted, 2026-09-10.** This section previously reported that an iPhone User-Agent gets a *second, disjoint* review index — Spotify/us returning 50 unique reviews to `curl` and 200 to an iPhone UA with zero overlap. Re-running the identical sweeps the next session, that did not reproduce at all:

| Full 1–10 sweep, `mostRecent` | `curl/8.5.0` | iPhone Safari | macOS Chrome | Generated browser headers | Overlap |
|---|---|---|---|---|---|
| Spotify/us | 500 unique | 500 | 500 | 500 | **500 (identical)** |
| Notion/us | 450 (hole at page 4) | 500 | 500 | 500 | 450 |
| Spotify/gb | 500 | 450 (hole at page 6) | 450 (hole at page 4) | 450 (hole at page 4) | 450 |

Every client sees the **same reviews**. When the counts differ it is purely because one client hit a hole — and note Spotify/gb, where the *iPhone* client is the one that lost a page. So there is one index, and the earlier "two disjoint indexes" reading was an artifact of measuring during a heavily holed window and attributing the pattern to the wrong variable.

What is real, and reproducible today, is narrower but still useful: **the client class changes whether a specific page is a hole.** Interleaved, on Notion/us `mostRecent` page 4:

| Client | 4 consecutive requests |
|---|---|
| `curl/8.5.0` | 0, 0, 0, 0 |
| Safari on iPhone | 50, 50, 50, 50 |
| Chrome on macOS | 50, 50, 50, 50 |
| Generated browser headers | 50, 50, 50, 50 |

A plain `curl` request got nothing on that page, every time, while three browser-shaped clients got a full 50 — the same 50. The split here is `curl` versus real-browser headers, *not* Apple-device versus everything else, which is exactly the variable the previous version got backwards. Note also that a plain retry does not fix a hole: seven identical `curl` requests to that page all returned empty. Changing the client is what fixes it.

If you take one thing from the two retractions in this post: when a request-shape variable seems to change your results, vary it along more than one axis before you name the mechanism. "iPhone vs curl" and "browser vs curl" predict identical data on the first test and opposite data on the second.

## What was wrong with the old advice, and why it survived so long

The original post recommended a 4-variant header rotation that fires on an empty page and caches the winning variant. That advice fails on both counts:

- It **cost up to 4× the requests** on every page that came back empty — and with holes everywhere, that is most pages.
- Worse, it **hid the real bug**. When a scraper has "tried four fingerprints" and still sees nothing, "it's genuinely empty" feels well-earned. It isn't: the loop had simply stopped at page 1 and never looked at page 5. Retry machinery is very good at making a wrong diagnosis feel thorough.

The lesson we'd actually pass on: **test the anti-bot theory before building machinery for it** — and then test it again on another day, because a scraping target measured once is a scraping target measured during one of its moods. The five-line diff (same URL, two clients, compare the review ids) is what separated "Apple blocks bots" from "some clients hit more holes"; running it a second time is what stopped us shipping a 2×-cost dual sweep for data we already had.

## What to do instead

1. **Sweep the whole page range** (1–10) and skip holes. Never treat an empty page as end-of-feed.
2. **Send browser-shaped headers, and re-request an empty page as a different client** before believing it — one retry under another client class, only on pages that came back empty. Do *not* sweep every page twice under two clients: you will pay double for the same review ids. Dedupe by review id regardless.
3. **Retry the other sort order** when one is thin. `mostRecent` and `mostHelpful` are separate indexes over the same pool with different holes; the same app can be empty under one and full under the other.
4. **Then probe other storefronts.** Coverage genuinely differs by country — an app can have real reviews in `gb` and none at all in `us` — and that is a different answer from "no reviews anywhere."
5. **Say which path served the data.** Tag every row with the sort order, the storefront and whether a fallback fired. A scraper that can't tell "Apple had nothing" from "our loop stopped early" is shipping silent failure.

## Packaged version

[app-store-reviews-scraper on Apify](https://apify.com/fetchsmith/app-store-reviews-scraper) does steps 1, 3, 4 and 5 today: full-range page scanning with hole skipping, dedupe by `reviewId`, automatic sort-order fallback (every row carries `sortUsed`), and an opt-in `countryFallback` that pulls from a working storefront when the requested one is genuinely empty (rows tagged `requestedCountry`/`fallbackUsed`). The dual-client-class sweep from step 2 is the finding above, measured today — it's going into the next build. Pay-per-review pricing, no browser, no proxy required.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; findings above come from real runs against live endpoints, not documentation. When we get something wrong, we correct it in place and say so.*
