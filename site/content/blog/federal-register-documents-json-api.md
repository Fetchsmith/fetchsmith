---
title: The Federal Register API says it has 10,000 documents. It doesn't — and the fix is already in the response
description: Every US federal rule, proposed rule and notice since 1994 is free JSON with no API key. But `count` is clamped, offset paging 400s at row 10,000, and a mistyped agency slug kills the whole query instead of returning nothing.
date: 2026-09-11
tags: webscraping, api, opendata, json
tool: federal-register-scraper
---

Every rule, proposed rule, notice and presidential document the US government has published since **1994-01-03** is available as JSON with no API key, no login, no proxy and no rate-limit header in sight:

```
GET https://www.federalregister.gov/api/v1/documents.json?per_page=1000&conditions[type][]=PRORULE
```

That's the machine-readable side of the *Federal Register* — the daily journal in which federal agencies publish everything they are legally required to publish. If a rule affecting your industry exists, it is in here, usually with the date by which you can still comment on it. We built [federal-register-scraper](https://apify.com/fetchsmith/federal-register-scraper) on this endpoint, and three things about it will quietly break a naive crawler.

## `count` is clamped at 10,000, so never use it as a total

Ask for a single row of anything and look at the envelope:

```
GET /api/v1/documents.json?per_page=1&fields[]=document_number
→ {"count": 10000, "total_pages": 50, ...}
```

The Federal Register has published far more than 10,000 documents — that one query matches the entire archive, millions of pages of it. `count` is not the match total; it is the match total **capped at 10,000**. We saw the same 10000 on a `PRORULE`-only query that obviously matches a different number of rows.

The practical damage isn't cosmetic. If you drive your pagination loop with `while fetched < count`, or draw a progress bar from it, you will stop early on any query broader than 10,000 rows and never know. Treat `count` as "at least this many" and nothing else.

## Offset paging hits a hard wall at row 10,000

The clamp isn't just a display quirk — the API enforces it on the way in too. Walk `per_page=1000` forward and page 11 is an error, not an empty list:

```
GET /api/v1/documents.json?per_page=1000&page=11
→ 400 {"status":400,"message":"Pagination limit exceeded.  No more than 10000 items can be requested at a time"}
```

This is the same shape of wall as [openFDA's `skip` cap at 25,000](/blog/fda-openfda-recall-json-api), where the only way through is to chop your query into date windows and page each one separately. The good news here: you don't have to.

## The cursor past the wall is already in the response you have

Every response carries a `next_page_url`, and from page 2 onward that URL has a `search_after_cursor` in it:

```
"next_page_url": "https://www.federalregister.gov/api/v1/documents?...&page=2&per_page=2
                  &search_after_cursor=WzE3ODkwODQ4MDAwMDAsIjIwMjYtMTg2NDUiXQ"
```

Base64-decoded, that cursor is just `[<publication timestamp>, "<document number>"]` — a keyset pointer at the last row you were handed. Follow `next_page_url` instead of incrementing `page` yourself and the 10,000-row wall disappears: we walked **14,000 consecutive rows** back to 2026-03-03 in one uninterrupted run, no 400, no gap, no date chunking.

The general lesson is worth more than this one API: **when a JSON API hands you a `next_page_url`, use it verbatim rather than reconstructing pagination from its parts.** The URL is where the API puts the escape hatch from its own offset limits, and it costs nothing to follow.

## Half the interesting fields only exist on half the document types

The schema is rich — `significant`, `comments_close_on`, `regulation_id_numbers` (RIN), `cfr_references`, `docket_ids`. It's tempting to advertise all of them. We sampled **200 live rows per document type** first, and the fields turn out to be sharply type-specific:

| field | RULE | PRORULE | NOTICE | PRESDOCU |
|---|---|---|---|---|
| `significant` | 86/200 | 79/200 | **0/200** | **0/200** |
| `comments_close_on` | 17/200 | **185/200** | 71/200 | 0/200 |
| `regulation_id_numbers` | 119/200 | 138/200 | 1/200 | 0/200 |
| `cfr_references` | 200/200 | 200/200 | **0/200** | 0/200 |
| `subtype` | 0/200 | 0/200 | 0/200 | **200/200** |

Two consequences. First, `comments_close_on` is a genuinely useful field — it tells you the date by which you can still influence a rule — but it lives on **proposed rules**, at 185/200, and it is mostly absent everywhere else. Second, and easier to get wrong: `significant: null` on a notice does **not** mean "this notice isn't significant". Significance is a rules-only designation; on a notice the field is simply not applicable. Render that as a `false` in your UI and you've invented a fact.

If you want only documents whose comment period is still open, the API has a filter for exactly that: `conditions[comment_date][gte]=2026-09-11`.

## A mistyped agency slug 400s the entire query

Filtering by agency is the most valuable filter here, and it has a sharp edge:

```
GET /api/v1/documents.json?conditions[agencies][]=homeland-security
→ 400 {"errors":{"agencies":"invalid value"}}
```

The correct slug is `homeland-security-department`. Get it wrong — a plausible guess, a stale slug, a user's free-text input — and you don't get an empty result set you can detect and report. You get a 400 that kills the whole run, including the other five agencies you asked for correctly.

The fix is to never send a guess. `GET /api/v1/agencies.json` returns all **472** agencies with `slug`, `name`, `short_name` and `child_slugs`, so you can resolve user input client-side, accept either a slug or a full agency name, and drop unrecognised values with a named warning instead of a dead run. **Whenever an API 400s on a bad enum value rather than returning nothing, look for its list endpoint and validate against it before you call.**

One nice thing worth knowing while you're there: agency filtering **rolls up**. A single `conditions[agencies][]=homeland-security-department` returned Coast Guard (45/100 rows), FEMA (24), CBP (7), TSA (5) and USCIS (4) alongside the parent department. One parent slug is a whole-department filter — you don't need to enumerate children.

## Smaller things we measured

- `order=oldest` reaches **1994-01-03**. The full archive really is there.
- `order` silently falls back to newest on an unrecognised value instead of erroring — the opposite of the agency-slug behaviour, in the same query string.
- No rate-limit headers are exposed at all, so there's nothing to read and budget against. Stay sequential and back off on 429/5xx.
- The bracketed parameters (`conditions[type][]`, `fields[]`) must be URL-encoded. Raw brackets work in curl but can silently misparse depending on your HTTP client.

## Packaged version

[federal-register-scraper on Apify](https://apify.com/fetchsmith/federal-register-scraper) wraps all of the above: cursor pagination past the 10,000-row wall, agency names or slugs resolved against the live 472-agency index before any request goes out, a `significantOnly` toggle, a comment-deadline filter, and 30 flat fields per document with each one documented against the type it actually appears on. No API key, no proxy, pay per result at $0.0008 — no start fee.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every JSON snippet and number above comes from a live request made while writing this post, not from documentation.*
