---
title: The FEC publishes campaign finance as key-free JSON — and its three rate limits contradict each other
description: api.open.fec.gov serves every US federal candidate and their fundraising totals with no account, via DEMO_KEY. The header says 10 calls, the error says 40, and Retry-After says come back in 16 hours. All three are on the same response.
date: 2026-09-14
tags: webscraping, api, opendata, government
---

Every candidate for US federal office — House, Senate, President — files with the Federal Election Commission, and the FEC publishes the whole thing as JSON at `api.open.fec.gov`. No account, no OAuth, no browser:

```
GET https://api.open.fec.gov/v1/candidates/?api_key=DEMO_KEY&q=Warren&state=MA&office=S
```

That's the shared `DEMO_KEY` from api.data.gov, the same one that fronts a dozen other federal APIs. We built an Actor against this API and then **did not ship it** — the reason is the whole point of this post. It's the ninth key-free government API we've built on, and the first one that's *honest* about bad input: where the [other eight](/blog/free-government-data-json-apis-no-key) return `200` with the wrong rows, the FEC returns a clean `422` and tells you the valid values:

```json
{"message":{"query":{"office":{"0":["Must be one of: , H, S, P."]}}},"status":422}
```

So the failure mode moved somewhere else. Here's where.

## The rate limit is three different numbers on one response

Send five requests past the quota and the fifth one comes back `429`. Read it carefully:

```json
{
  "error": {
    "code": "OVER_RATE_LIMIT",
    "message": "You have exceeded your rate limit of 40 calls per hour for the DEMO_KEY, 1000 calls per hour for a personal key, or 120 calls per minute for an upgraded key. ..."
  }
}
```

Now the headers on that exact same response:

```
x-ratelimit-limit: 10
x-ratelimit-remaining: 0
retry-after: 57263
```

The header says the budget is **10**. The error body says the budget is **40 per hour**. And `Retry-After` says **57263 seconds — 15.9 hours**, not the one hour the message just promised. We watched `x-ratelimit-remaining` count 9, 8, 7… down to 0 across single requests, so the header is at least self-consistent; it is the *only* one of the three you should write code against. Treat the prose in the error body as decoration, and do not implement a naive `sleep(retry-after)` retry unless you are happy with a job that hangs until tomorrow afternoon.

The practical reading: **DEMO_KEY is a smoke-test credential, not a budget.** It is shared across every anonymous caller on your egress IP, so your real ceiling depends on who else is behind the same NAT. A free personal key from `api.data.gov/signup/` moves you to 1000/hour, and that is the difference between "this API works" and "this API works on Tuesdays."

## `includeTotals` is an N+1, and the FEC's quota is where you pay for it

The candidate record and the money live at different endpoints. `/v1/candidates/` gives you identity — name, party, office, state, district, incumbency, election years — and nothing financial. Receipts and cash on hand come from:

```
GET /v1/candidate/{candidate_id}/totals/
```

One request per candidate. So a 20-candidate search with totals enabled is 1 + 20 = **21 requests**, which is over every published DEMO_KEY ceiling, including the most generous one. This is the single biggest thing to plan for: on a shared key, your result count *is* your request count.

It also fails asymmetrically, which is worse than failing outright. Ask for the totals of a minor 2004 House candidate:

```
GET /v1/candidate/H4MI03185/totals/?per_page=1&sort=-candidate_election_year
```

```json
{"pagination": {"count": 0, ...}, "results": []}
```

`HTTP 200`, zero rows. Not a `404` — the candidate exists, they just never filed a financial summary the API will serve. An empty `results` array here means "no report on file"; it does **not** mean you got rate limited, and a rate limit does **not** look like this. If you fold both into a null — which is the natural thing to do, and which our own implementation did until we wrote this post — you lose the ability to tell "this candidate raised nothing" from "we ran out of quota halfway down the page." Keep them separate: a missing totals row should yield explicit `null` financial fields on a candidate row that still carries full identity data, while a `429` should abort the run loudly rather than emit a page of quietly empty money columns.

## `/totals/` returns each election year twice

Pull Elizabeth Warren's totals and the pagination says `count: 12` — for a senator with four election years on file. The rows come in pairs:

```json
{"candidate_election_year": 2030, "cycle": null, "receipts": 4413931.4, "coverage_end_date": "2026-06-30T00:00:00"}
{"candidate_election_year": 2030, "cycle": 2026, "receipts": 4413931.4, "coverage_end_date": "2026-06-30T00:00:00"}
```

Same numbers, different `cycle`. The `cycle: null` row is the aggregate across the candidate's full election cycle — six years for a Senate seat — and the numbered row is one two-year FEC cycle inside it. Early in a Senate term they're identical, because only one two-year cycle has happened yet. They diverge later, and if you `sum()` the rows you will double-count every dollar.

## The newest totals row is for an election that hasn't happened

This is the one most likely to end up in someone's chart with a wrong label. Sort totals by `-candidate_election_year` and take the first row — the obvious "give me the latest" move, and what our Actor does — and for Warren you get `candidate_election_year: 2030`:

```json
{"candidate_election_year": 2030, "receipts": 4413931.4,
 "coverage_start_date": "2025-01-01T00:00:00", "coverage_end_date": "2026-06-30T00:00:00"}
```

$4.4M. Her *last completed* campaign is the row below it:

```json
{"candidate_election_year": 2024, "receipts": 21088321.25, "disbursements": 28730962.36,
 "coverage_start_date": "2019-01-01T00:00:00", "coverage_end_date": "2024-12-31T00:00:00"}
```

$21.1M. The newest row is a partial, in-progress period for a future election, and it will keep growing for four more years. Both are correct; they answer different questions. Always read `coverageStartDate`/`coverageEndDate` alongside `receipts` before you compare two candidates — one of them may be 18 months into a cycle while the other has a completed six-year total. Our output carries both coverage dates on every row for exactly this reason.

## `q` is a full-text name match, not a surname

Last small trap: `q=Warren` returns **127 candidates**, and the first one alphabetically is `ADAMS, WARREN` — a 2004 Libertarian House candidate from Michigan. `q` searches the whole filed name, first names included. Adding `state=MA&office=S` cuts 127 to 2:

```
S2MA00170 | WARREN, ELIZABETH | DEMOCRATIC PARTY | [2012, 2018, 2024, 2030]
S2MA00139 | WARREN, SETTI     | DEMOCRATIC PARTY | [2012]
```

Given the N+1 above, filtering hard on `state`/`office`/`party` isn't a nicety — every candidate you fail to filter out is another request off your quota, spent on someone you didn't want.

## Why there's no packaged version of this one

Every other API we write up here ends with a link to a hosted Actor. This one doesn't, and the rate limit is why.

A hosted scraper has to work when a stranger clicks Start. On `DEMO_KEY` it can't: the quota is shared per egress IP, so one user's 20-candidate run exhausts it for everyone else on that host, and `Retry-After` then says come back in 16 hours. The fix is a free personal `api.data.gov` key, which is a one-line change — `api_key=DEMO_KEY` becomes a config value — but it has to be a real key, obtained and held by whoever runs the thing. Until then, shipping it would mean selling a tool whose failure mode is "works when you demo it, 429s when your customer tries."

So the code sits unpublished, and this post is the useful half: the endpoints, the traps and the field semantics are the same whichever key you put in front of them. If you're building against public-money data generally, the comparison of how eight *other* key-free government APIs fail — all of which we do ship — is in [Eight government JSON APIs that need no key](/blog/free-government-data-json-apis-no-key), and the live tools are at [fetchsmith.com/tools](/tools). The FEC is the one that 422s instead of lying, and then hides its real limit in a header nobody reads.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every JSON snippet, header and error above comes from a live request made while writing this post, not from documentation.*
