---
title: One key-free API searches trademarks in 70+ offices — and its worst failure returns no HTTP status at all
description: TMview's public search endpoint covers USPTO, EUIPO, UK, DE, JP and 70+ more registries with no key and no login. Omit one header and it doesn't 403 you, it drops the TCP connection. Every date is anchored at midday UTC on purpose, and the same field is 100% populated in one office and 0% in the next.
date: 2026-09-24
tags: webscraping, api, trademarks, opendata
tool: trademark-search-scraper
---

If you want to know whether a brand name is already taken, the official answer lives in each country's own trademark register — USPTO in the US, EUIPO for the EU mark, the UKIPO, the DPMA, JPO, CNIPA, WIPO. Checking a name properly means checking all of them, and every one of those offices has its own site, its own search UI, and (mostly) no usable API.

[TMview](https://www.tmdn.org/tmview/), run by EUIPO's TMDN network, already solved that: it is a single federated index over **70+ national and regional trademark offices**. What is less advertised is that the web UI is a thin client over a plain JSON API, and that API needs no key, no account and no login:

```
POST https://www.tmdn.org/tmview/api/search/results
Content-Type: application/json

{"page":"1","pageSize":"50","criteria":"C","basicSearch":"solarwinds"}
```

```json
{"tradeMarks": [...], "page": 1, "totalPages": 30, "totalResults": 148}
```

We build [trademark-search-scraper](https://apify.com/fetchsmith/trademark-search-scraper) on this endpoint. The API itself is a fifteen-minute integration. The three things below are what actually cost time, and two of them fail in ways that don't look like failures.

## 1. Without a User-Agent you get no HTTP response at all

The usual way an edge WAF tells a script it isn't welcome is `403`. TMview does something quieter. Four variants of the exact same POST, three attempts each, from the same host, one minute apart:

| Headers sent | Result (3 attempts) |
|---|---|
| `Content-Type` only | `000`, `000`, `000` |
| `Content-Type` + `Accept: application/json` | `000`, `000`, `000` |
| `Content-Type` + browser `User-Agent` | `200`, `200`, `200` |
| `Content-Type` + `User-Agent` + `Accept` | `200`, `200`, `200` |

`000` is curl's placeholder for *there was no HTTP status line*. Run it without `-s` and you see why:

```
curl: (56) Recv failure: Connection reset by peer
```

The request is accepted, then the connection is reset before a response. `Accept` makes no difference; the `User-Agent` alone flips it. This matters more than an ordinary block would, because of **where** the failure lands in your code:

```js
const res = await gotScraping({ url: API, method: 'POST', json: body, throwHttpErrors: false });
if (res.statusCode !== 200) { /* never reached */ }
```

`throwHttpErrors: false` is the standard way to handle a hostile endpoint gracefully — it converts 4xx/5xx into an ordinary response object you can branch on. It does nothing here. There is no status code to inspect, so the socket error propagates as a thrown exception straight past the handler you carefully wrote, and your run dies on a stack trace that reads like an upstream outage rather than a missing header.

The same shape bit us a second time on the same Actor from the other direction. Routing through a datacenter proxy, a bad exit node answered every request with `The proxy responded with 590 UPSTREAM502` — again a CONNECT-level failure with no HTTP response to check, while the identical query returned `200` on a direct connection at the same moment. TMview was up; that one egress path was not.

Two rules fall out of this, and they generalise to any JSON API you did not get documentation for:

- **Send a real browser `User-Agent` on API calls, not just on HTML fetches.** Library defaults like `python-requests/2.x` or a bare `node` UA are exactly what this class of edge filter drops. (`got-scraping`, which the Actor uses, sends a browser UA by default — which is why this only shows up when you reproduce the call by hand.)
- **Handle transport failure separately from HTTP failure.** A `try/catch` around the request and a `statusCode` check are two different error paths, and the nastier one is the path that has no status code. Retrying on a fresh proxy session belongs in the `catch`, not in the status branch.

## 2. Every timestamp is anchored at midday UTC, and that is deliberate

Every date TMview returns is a full ISO timestamp:

```json
"applicationDate":      "2012-04-23T12:00:00.000Z",
"registrationDate":     "2012-10-30T12:00:00.000Z",
"oppositionPeriodStart":"2012-07-27T12:00:00.000Z",
"expirationDate":       "2032-04-23T12:00:00.000Z"
```

Across a 200-row sample spanning four offices (US, EM, GB, DE), **683 of 683 non-null date values carried exactly the suffix `T12:00:00.000Z`**. Not one midnight, not one real clock time.

These are calendar dates, not events — a filing happened on a day, not at a second. Midnight would have been the obvious encoding and it is the wrong one: `2012-04-23T00:00:00Z` rendered in any timezone west of UTC is *22 April*, and a renewal deadline that silently moves a day earlier in every US-based dashboard is a real bug. Anchoring at 12:00 makes the rendered calendar day stable across the whole ±12h range of real timezone offsets, in both directions.

So: slice to ten characters and treat it as a date string (which is what our Actor emits), or parse it and format in UTC. What you must *not* do is assume a timestamp implies a known time of day — nothing here is accurate to the hour, and code that filters on "notices after 09:00" is filtering on an artefact.

## 3. The same field is 100% populated in one office and 0% in the next

This is the part that turns a working integration into a support ticket. TMview federates 70+ registries that publish genuinely different data, and it does not fill the gaps. Same query (`solar`), 50 rows per office, four offices:

| Field | US | EM (EUIPO) | GB | DE |
|---|---|---|---|---|
| `applicationDate` | 48/50 | 50/50 | 50/50 | 50/50 |
| `registrationDate` | 37/50 | 43/50 | 49/50 | 44/50 |
| `expirationDate` | **0/50** | 30/50 | **49/50** | **0/50** |
| `oppositionDeadLine` | **0/50** | 47/50 | 25/50 | 44/50 |
| `seniorityClaimed` | **0/50** | 1/50 | **50/50** | **50/50** |
| `markImageURI` | **50/50** | 21/50 | 8/50 | 20/50 |

Read the `expirationDate` row again: a renewal-tracking dashboard built and tested against UK records works perfectly, ships, and returns an empty column for every US and German mark. Nothing errors. The field is simply absent, because those offices don't publish it through this channel.

The `oppositionDeadLine` row has a second trap in the field name itself. Its siblings are `oppositionPeriodStart` and `oppositionPeriodEnd`, camelCase throughout — but the deadline is spelled with a capital **L**. `tm.oppositionDeadline` is `undefined` forever, in every office, and looks exactly like the "this office doesn't publish it" case above. We normalise it to `oppositionDeadline` on output; if you are calling the API directly, copy the key, don't type it.

`markImageURI` is the one that inverts the intuition. The US is the *only* office in the sample that returns an image URI on every row, while EUIPO returns one on 21 of 50 — and on EM, GB and DE the image count matches the `viennaCodes` count exactly (21/21, 20/20, 8/8). Vienna codes classify figurative elements, so those three offices are returning imagery for figurative marks only, while the USPTO attaches a rendering to word marks too.

The practical rule: **treat per-office field availability as a property of the office, not of the record.** Sample the offices you actually care about before you promise a column to anyone, and make any null-to-UI mapping say "not published by this office" rather than "unknown" or, worse, "none".

## What this ends up being good for

A search that costs nothing per office is a different tool from one that costs a lawyer's hour per office. The three things people do with it:

- **Clearance screening** — run a proposed name across all 70+ offices before you file anywhere, and see the collisions in one result set instead of thirty tabs.
- **Opposition watch** — new filings that collide with your mark are only actionable inside the opposition window, and `oppositionPeriodStart`/`oppositionDeadline` tell you how much of it is left. Our Actor's `watchLabel` mode returns and charges for only marks that are new since the previous run on the same label, so a daily scheduled watch is cheap; the [watch-mode trap guide](/blog/incremental-api-watch-mode-four-traps) covers how that baseline is keyed and what it deliberately does not track.
- **Competitor portfolio mapping** — `applicantNames` plus `office` plus `niceClasses` across a result set is a readable map of where a company has actually secured protection, and in which classes.

One caveat worth stating plainly: this is a screening index, not a clearance opinion. TMview is the offices' own data, but a real freedom-to-operate analysis weighs similar marks, not identical strings, and that is a trademark attorney's job.

If you want the normalised version — 22 flat fields per mark, dates already sliced to calendar dates, the capital-L key already renamed, and the transport-failure retry already written — it is [trademark-search-scraper](https://apify.com/fetchsmith/trademark-search-scraper) on Apify, priced per returned mark.

The header-drop failure mode in section 1 is the same class as the silent empties we hit on Apple's review feed — see [Three ways a public review API returns an empty list instead of an error](/blog/app-store-review-apis-three-silent-empties) for the version of this that returns `200` and lies to you instead.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every response shape, status code and fill-rate number above comes from live requests made while writing this post, not from documentation.*
