---
title: CourtListener's court-records API needs no key — except for the one endpoint most wrapper docs point you at first
description: The search index behind CourtListener's federal docket and opinion data is fully anonymous, but its docket/opinion detail endpoints 401 without a token — and combining two indexes in one query has a pagination trap that silently drops an entire record type.
date: 2026-09-17
tags: webscraping, api, opendata, legal, government
tool: court-records-scraper
---

Every federal court docket in RECAP's public PACER mirror, and every published federal court opinion, is queryable with a single anonymous request:

```
GET https://www.courtlistener.com/api/rest/v4/search/?q=patent+infringement&type=o
```
```json
{"count": 59685, "next": "...", "results": [{"absolute_url": "/opinion/2416294/...", "caseName": "...", ...}]}
```

No key, no login, no cookies — that request just returned real data from a bare `curl` on a datacenter IP. We built [court-records-scraper](https://apify.com/fetchsmith/court-records-scraper) on this endpoint. Two things about it will trip up anyone building against it from the docs alone.

## The API has two auth tiers, and the docs lead with the one that needs a key

CourtListener's REST API is one base path, `/api/rest/v4/`, and its own documentation walks through `/dockets/` and `/opinions/` first — the *detail* endpoints, one record per call. Try either without a token:

```
GET https://www.courtlistener.com/api/rest/v4/dockets/?q=test
```
```json
{"detail": "Authentication credentials were not provided."}
```

`401`, every time. Read that first and the reasonable conclusion is "this API needs an account" — which is exactly what several existing scraper listings assume, registration flow and all. But the endpoint every real competitor we found is actually built on isn't the detail endpoint at all, it's the **search index**, one path over:

```
GET https://www.courtlistener.com/api/rest/v4/search/?q=test&type=r
```
```json
{"count": 143653, "next": "...", "results": [{"docketNumber": "5:26-cr-00442", "caseName": "United States v. Ledesma", "assignedTo": "Noel Wise", "attorney": ["Sarah Elizabeth Griswold", "Varell Laphalle Fuller"], ...}]}
```

`200`, fully anonymous, and it already carries the case name, parties, attorneys, firms, assigned judge, docket number and per-filing entries inline — everything the detail endpoint would have given you one record at a time, for free, in bulk, with cursor pagination built in. The two tiers aren't documented as a decision point anywhere obvious; you find it by noticing which URL the working competitor listings actually call. `type=r` searches the RECAP (PACER-mirror) docket index; `type=o` searches published opinions. The account-gated detail endpoints exist for looking up one already-known record by ID — not for search, and not something this Actor, or apparently anyone shipping a real product here, needs at all.

## Asking for "both" record types the naive way returns one of them and silently drops the other

Both indexes are big enough, for almost any real query, that a page-size cap alone will exhaust before you run out of matches:

```
GET .../api/rest/v4/search/?q=patent+infringement&type=o   → count: 59685
GET .../api/rest/v4/search/?q=patent+infringement&type=r   → count: 143653
```

Both numbers comfortably exceed any sane `maxResults`. That matters because a natural way to implement "give me opinions *and* dockets in one run" is to walk the opinion index until the budget is spent, then move on to the docket index with whatever's left. We shipped exactly that in a first draft, and measured the result on a 40-row budget: **40 opinions, 0 dockets.** The opinion query alone had far more than 40 matches, so the docket index was never even queried — the loop finished before it got there.

Nothing in the response tells you this happened. `count` on the request you *did* make is accurate; the request you *didn't* make just doesn't exist, so there's no field to check and no warning to catch. A buyer who asked for "both" and validated the response shape (docket rows and opinion rows both present, both structurally valid) would see a schema that looks entirely correct and still be missing an entire record type.

The fix is to never let either index go first indefinitely: split the budget evenly up front (`ceil(maxResults / 2)` per index), run both, and hand whatever one index couldn't fill to the other in a second pass. Re-measured on the same query and budget: 20 opinions, 20 dockets, then any unused remainder carried over. The general shape — "when merging N independently-paginated indexes into one result set, giving any single index first claim on the shared budget silently starves the others whenever that index alone can fill it" — isn't specific to CourtListener; it's the same bug class as a round-robin scheduler with no fairness guarantee, just easy to miss because the failure mode is a clean, correctly-typed, entirely plausible response with fewer record types in it than you asked for.

## Not every docket entry has a document behind it

One smaller trap, worth a line: RECAP is a *mirror* of documents its contributors have actually purchased from PACER and donated, not a live PACER feed. A docket entry can exist — case name, date, description, page count all populated — with no retrievable file:

```json
{"description": "CRIMINAL COMPLAINT as to Andrew Ledesma (1)...", "page_count": 3, "is_available": true, ...}
```

`is_available` is a real field on every filing entry, and it's `false` on a meaningful share of them — 30 of 72 filing entries in a live N.D. Cal. sample we measured. Nothing about the rest of the row hints at this; the description and page count are populated identically whether or not the PDF exists. Check the flag before assuming a downloadable document is behind every entry you got back.

## `filed_after` is inclusive — and a malformed date is dropped, not rejected

Two things worth knowing before you filter by filing date.

**Both bounds are inclusive.** Not documented either way, so we measured it on SCOTUS opinions: `filed_after=2024-06-13&filed_before=2024-06-13` returns **6**, the same window on `2024-06-14` returns **9**, and `2024-06-13 .. 2024-06-14` returns **15**. 6 + 9 = 15, so neither endpoint is being trimmed. Build your windows as closed intervals.

**The dangerous half.** CourtListener *does* reject a date it can't parse — `filed_after=2024-06-31` and `filed_after=0615-20-24` both come back `HTTP 400 {"detail":"The date entered has an invalid format."}`. The risk isn't upstream, it's in whatever normalizes the date before it gets there. Our own client used to do this:

```js
const digits = String(v).replace(/[^0-9]/g, '');
if (digits.length !== 8) return null;   // <- silently drops the filter
```

That looks defensive and is the opposite. `"2024-6-5"` — a date a human types constantly — strips to six digits, returns `null`, and the filter is simply never sent. The request still succeeds, so nothing anywhere reports a problem. Asking for SCOTUS opinions filed 5–9 June 2024 returned ten opinions filed between **1795 and 1831**: the whole archive, unfiltered, in a response that looks completely normal. On a per-result pricing model every one of those rows is billable.

The same parser mangles `"06/15/2024"` into `"0615-20-24"` — eight digits, so it passes the length check — and the user gets a 400 naming a date they never typed.

The general rule: **when a filter fails to parse, ask whether dropping it narrows the result set or widens it.** A dropped `stat_Published` narrows (you get the default), and falling back is fine. A dropped `filed_after` widens to the entire corpus, so falling back is the worst available option — fail loudly instead. The fix is to parse strictly, accept every *unambiguous* spelling (`2024-6-5`, `2024/6/5`, `20240605` all normalize to `2024-06-05`), calendar-validate by round-trip so `2023-02-29` never reaches the wire, and throw on anything left — including `06/15/2024`, because `06/15` and `15/06` can't be told apart and guessing wrong silently returns the wrong quarter.

This is the same shape as [the CPV prefix trap](/blog/uk-find-a-tender-ocds-json-api) in our UK tender client: a filter that quietly stops filtering is far more expensive than one that errors.

## Packaged version

[court-records-scraper on Apify](https://apify.com/fetchsmith/court-records-scraper) is built directly on the anonymous search index — no account, no token, no captcha — and merges opinions and dockets with the fair-share split described above, so asking for `recordType: "both"` never silently drops one type. `is_available` ships on every filing entry so you can filter on document availability instead of assuming it. $0.002/result, no run-start fee, incremental `watchLabel` mode for scheduled monitoring.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every JSON snippet above comes from a live request made while writing this post, not from documentation.*
