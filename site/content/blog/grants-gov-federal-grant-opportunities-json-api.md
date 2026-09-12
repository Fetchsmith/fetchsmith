---
title: Grants.gov's search API never returns an error — a typo in your filter just silently returns zero results
description: Grants.gov's public search2/fetchOpportunity API needs no key, but a bad enum value returns "Webservice Succeeds" with an empty result set instead of a 400, and parent agency codes don't roll up to sub-agencies.
date: 2026-09-11
tags: webscraping, api, opendata, grants
tool: grants-gov-scraper
---

Grants.gov — the US government's single portal for federal grant opportunities — has a public JSON API behind its own search UI, and it needs nothing to call:

```
POST https://api.grants.gov/v1/api/search2
Content-Type: application/json

{"rows": 25, "oppStatuses": "forecasted|posted"}
```

No key, no login, no proxy — verified 200 from a plain datacenter IP. We built [grants-gov-scraper](https://apify.com/fetchsmith/grants-gov-scraper) to wrap it because the field is thin: every real competitor on Apify tops out at 7 users, versus 40-90 in adjacent government-data niches. The API itself is simple. Trusting its error handling is the part that breaks people.

## A typo in your filter returns zero results, not an error

Most APIs we've built against tell you when you got a parameter wrong — openFDA 400s on a bad skip value, Federal Register 400s on an unrecognised agency slug. Grants.gov does neither:

```json
// a made-up parameter that doesn't exist
{"totallyFakeParam": "xyz"}
```
```json
{"errorcode": 0, "msg": "Webservice Succeeds", "data": {"oppHits": [...], "hitCount": 10275}}
```

That's arguably fine — an unknown key just gets ignored. This is not:

```json
// a typo'd status value
{"oppStatuses": "bananas"}
```
```json
{"errorcode": 0, "msg": "Webservice Succeeds", "data": {"oppHits": [], "hitCount": 0}}
```

`bananas` isn't a valid status, and Grants.gov gives no sign of that — same success message, same shape, **zero hits**. That's indistinguishable from a legitimately empty search. If you build a filter UI or a script around this API and pass through user input unchecked, a single typo silently tells your users "no grants found" instead of "you spelled that wrong." The only way to catch it is to validate against Grants.gov's own facet lists (`oppStatusOptions`, `eligibilities`, `fundingCategories`, `fundingInstruments`) — which the API conveniently returns alongside every real search result — before the request ever goes out. The Actor does this client-side and fails loudly on an unrecognised value instead of returning an empty dataset that looks legitimate.

## Searching by parent agency misses every sub-agency result

Government APIs vary on whether a parent department code includes its children. Federal Register's agency filter rolls up automatically — searching `homeland-security-department` returns Coast Guard, FEMA, CBP and TSA notices. Grants.gov does the opposite:

```json
{"agencies": ["USDA"]}
```
```json
{"data": {"oppHits": [], "hitCount": 0}}
```

Zero hits for the entire US Department of Agriculture — despite real, currently-open USDA-family opportunities existing right now (14 for `USDA-NIFA` alone, verified live), all posted under sub-agency codes like `USDA-NIFA`, `USDA-FS` and `USDA-APHIS`. `"USDA"` alone matches nothing because opportunities are tagged with the specific sub-agency, never the parent. Anyone assuming "filter by department" works the way it does elsewhere will get a false empty result on some of the most common searches (Defense, Agriculture, Health and Human Services all have this shape). The Actor resolves a parent code you supply against the live agency facet list and expands it into every real sub-agency code before searching, so filtering by department actually returns the department's grants.

## Looking up a closed opportunity by its exact number returns nothing

Grants.gov defaults every search to `forecasted` and `posted` opportunities only — reasonable, since most searches want open grants. But that default applies even when you're not searching, you're looking one up by its exact opportunity number:

```json
{"oppNum": "USDA-NIFA-OP-012345"}
```

If that opportunity has since closed or been archived, this returns nothing — Grants.gov ANDs `oppNum` with its own default status filter, silently. An opportunity number is unique; there's no reason a lookup by exact ID should ever come back empty just because the grant closed last month. The fix is to treat `oppNum` as an exclusive mode: when set, search all four statuses (`forecasted`, `posted`, `closed`, `archived`) and ignore every other filter, so a valid opportunity number always finds its record if one exists.

## The search results don't carry the numbers you'd actually decide on

One more thing worth knowing before you build against this API directly: the `search2` endpoint's rows are thin — 10 fields (`id`, `number`, `title`, `agency`, dates, status, CFDA list). No award ceiling, no eligibility text, no description. Every field a grant seeker actually needs to decide whether to apply — `awardCeiling`, `awardFloor`, `applicantEligibilityDesc`, `applicantTypes`, the full synopsis — lives only behind a second call, `fetchOpportunity`, keyed by the id from the search row. It's cheap (~0.35s/call, verified with 3 sequential calls in 1.06s) but it's a join you have to know to make; nothing in the search response hints that richer data exists elsewhere.

## Packaged version

[grants-gov-scraper on Apify](https://apify.com/fetchsmith/grants-gov-scraper) handles all four of these: client-side enum validation against Grants.gov's own live facet lists (so a typo fails loudly instead of returning an empty dataset), automatic parent-agency-to-sub-agency expansion, an exclusive `oppNum` lookup mode that ignores the default status filter, and an `enrich` option that joins each result with the award/eligibility/synopsis fields from `fetchOpportunity`. Named individual program officers (a real risk in the free-text agency contact fields — see the Actor's README) are never emitted, only organisational agency data. No API key, no proxy, pay per result, cheaper than the largest pure-Grants.gov listing on Apify.

Grants.gov's silent-zero behaviour is one of three distinct failure classes we've catalogued across the eight key-free government APIs we build against — the cross-API comparison and a four-assertion checklist that catches all of them is in [Eight government JSON APIs that need no key](/blog/free-government-data-json-apis-no-key).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every JSON snippet above comes from a live request made while writing this post, not from documentation.*
