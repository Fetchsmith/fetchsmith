---
title: Four ways an "only new since last run" watch mode silently stops working
description: "New" is not a property of a public API — it's a property of your own history. Shipping incremental watch mode across four government APIs (NIH RePORTER, Federal Register, Grants.gov, openFDA) surfaced four failure modes, and every one of them keeps the run log green while delivering nothing.
date: 2026-09-15
tags: webscraping, api, opendata, scheduling
---

Almost every buyer of a public-data scraper eventually wants the same thing: *don't send me the same 18,000 rows every morning, send me what changed.* That sounds like a filter. It isn't. Every public API we work with will happily tell you what **it** thinks is recent — and none of them know what **you** already received. "New" lives in your own history, which means a watch mode is a stateful feature bolted onto a stateless scraper, and that is where it goes wrong.

We shipped this mode (`watchLabel`) across four government-data Actors in four consecutive days: [NIH RePORTER](/tools/nih-reporter-scraper), the [Federal Register](/tools/federal-register-scraper), [Grants.gov](/tools/grants-gov-scraper) and [openFDA recalls](/tools/fda-recall-scraper). The state machine was the easy part — it copied across all four almost unchanged. What did not copy were the four traps below. Each one was found on a *different* API, each produces a run that exits 0 with a cheerful log line, and each delivers either zero rows forever or a silent under-count.

## Trap 0: the API's own "recent" flag is not your "new"

NIH RePORTER has a `newly_added_projects_only` boolean, and it is genuinely useful — but it means "recently added to the index", index-wide. Set it and you get roughly the same ~8,900 projects back on every run until they age out of the flag. That is a perfectly correct answer to a question nobody asked. A weekly alert needs "something new matched **my** query", and no server-side flag can answer that, because the server has no idea what you fetched last Tuesday.

So: you keep a baseline of ids you have already delivered, and you diff against it. Everything below is a consequence of that.

## Trap 1: your state store resets every run

On Apify, `Actor.openKeyValueStore()` with no argument gives you the **default** store, which is created fresh per run. Write your baseline there and every run starts from an empty set — so every row looks new, every run delivers everything, and on a per-result pricing model the buyer pays full freight forever. The log says `delivered 18458 new rows`, which is exactly what "working" looks like.

The fix is a *named* store, which persists on the caller's own account:

```js
const store = await Actor.openKeyValueStore('fetchsmith-nih-watch');
```

Two details that bit us:

- **The key needs the criteria baked in, not just the label.** We use `watch-<label>-<sha1(criteria).slice(0,10)>`. If the buyer widens a filter, that is a *different question*, and it deserves a fresh baseline — otherwise the first run after the edit dumps every row the old, narrower filter happened to exclude and bills it as "new".
- **Apify KV keys only allow `[a-zA-Z0-9!-_.'()]`.** The obvious separator, a colon, is invalid. Sanitise the label rather than passing it through.

## Trap 2: fingerprint what the user typed, not what your code computed

This one is the reason to write the post. The Federal Register Actor's publication-date window defaults to a rolling *last 90 days*; the openFDA one defaults to a rolling *last 365 days*. Both resolve that default to absolute dates at run start, from `new Date()`.

Hash the **resolved** dates into your criteria fingerprint and a scheduled daily watch gets a brand-new key every single day. Which means: it seeds a fresh baseline, correctly returns zero rows because a seed run is a baseline run, logs `seeded 51 ids, nothing new`, exits 0 — and does that tomorrow, and the day after, forever. It never delivers a row, it never errors, and it never charges anything, so there is no bill to notice and no alert to miss. It just quietly is not a product.

The rule that fixes it is one line long: **the fingerprint is built from the buyer's raw input, never from the value your code derived.** If they left the date window alone, the fingerprint entry is `null`. Any input with a relative default — `last N days`, `today`, "since the previous quarter" — has this trap.

## Trap 3: a baseline walk and a result walk need different paging

The first run has to enumerate the *entire* current match set, because anything it misses will be reported as new later. A normal run only has to satisfy `maxResults`. Those are different jobs, and reusing the result pager for the seed is where two real bugs came from:

- **Page size inherited from `maxResults`.** The Federal Register seed ran with `per_page = 50` and recorded 50 of 51 matching documents. The openFDA Actor derives its page size the same way (`min(1000, max(20, min(maxResults, 200)))`). A seed must pin page size to the API maximum — it is covering the whole set, not one page of it.
- **More than one shape of "next page".** `federalregister.gov/api/v1/documents.json` returns `next_page_url` as a `search_after_cursor` link for large walks **and** as a plain `?page=N` link for small result sets. Our pager only understood the cursor and broke out of the loop otherwise. That was harmless for normal runs — page one already satisfies `maxResults` — but fatal in watch mode, where nearly every row is skipped as already-seen and the walk *must* keep going to find the handful that aren't.

The check that catches both takes one line: compare your recorded seed count against the API's own `count`/total for the identical query. 50 versus 51 is invisible by eye and obvious by subtraction.

## Trap 4: a cheap seed still has to reproduce the exact predicate

Seeding is supposed to be cheap — you only need ids, so you skip the per-row detail fetch. On Grants.gov that would have been wrong, not just cheap. Its `minAwardAmount`/`maxAwardAmount` filter can only be evaluated *after* a per-opportunity detail fetch. An opportunity whose award ceiling is not yet populated at seed time doesn't match the filter — but ceilings do get filled in later (a real, observed field-level edit on that API), at which point it legitimately becomes a match. If the thin seed had dumped every raw hit id into the baseline, that opportunity would be marked "already seen" before it ever qualified, and would never surface.

So: **the seed must apply the same predicate a real run would, not a cheaper approximation of it.** Cost-cutting the seed is only safe for the parts of the filter that don't depend on an enrichment or join step. Where the filter is evaluated purely on fields the search endpoint already returns — openFDA's recall rows, for instance — an id-only seed is provably equivalent, and we checked that by reading the code rather than assuming it.

## How to actually test it

Unit tests do not catch any of the four. All of them need real runs against the live API, and the sequence that catches them is three runs:

1. **Seed.** Compare the recorded id count to the API's own total for the same query. (Catches trap 3.)
2. **Rerun the identical input.** Must return exactly zero. (Catches a broken key or a resetting store — traps 1 and 2.)
3. **Delete a few ids from the stored baseline via the KV API, then rerun.** Exactly those rows must come back, fully populated.

Step 3 is only a real test if you choose the ids carefully. Delete from the **tail** of the recorded set — the ids scanned on the final page — and, if you can, include the last row of page two. With the Federal Register paging bug in place, deleting three ids from the middle returns three rows and looks like a pass; deleting the last row of page two returns two of three, and still reads as a success in the log unless you are counting.

Our own results, on real platform runs: NIH RePORTER 82 ids seeded → 0 on rerun → exactly 3 returned; Federal Register 51 (matching the API's `count`, which is how the off-by-one showed up); Grants.gov 18,458 on a deliberately broad `keyword=water` query; openFDA 108 Class I recalls across the food, drug and device endpoints.

One last design note that is easy to get backwards: **mark a row as delivered only after the charge and the write succeed**, not when you decide to send it. A row dropped by a `maxResults` cap or a charge limit should stay "new" and come back next run, rather than being silently consumed by a run that never actually delivered it.

## Where this is live

`watchLabel` is an optional input on four of our Actors — leave it unset and they behave exactly as before:

- [NIH RePORTER Scraper](/tools/nih-reporter-scraper) — baseline keyed on `appl_id`
- [Federal Register Scraper](/tools/federal-register-scraper) — `document_number`
- [Grants.gov Scraper](/tools/grants-gov-scraper) — opportunity `id`
- [FDA Recall Scraper](/tools/fda-recall-scraper) — `recall_number`

The first run under a new label seeds and charges nothing. After that you pay only for rows you have never been sent before, which for a daily schedule on a slow-moving dataset is usually a rounding error against re-pulling the full set every morning.

If you want the underlying APIs themselves, all four are free and key-free, and each has its own separate way of returning `HTTP 200` with the wrong answer — we catalogued those in [Eight government JSON APIs that need no key](/blog/free-government-data-json-apis-no-key).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every count, field name and failure mode above comes from real runs we made against these live APIs while building the feature, not from documentation.*
