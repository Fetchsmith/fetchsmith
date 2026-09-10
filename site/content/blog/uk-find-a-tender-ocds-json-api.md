---
title: The UK publishes every public contract as OCDS JSON — and the money isn't where you'd look
description: Find a Tender, the UK's post-Brexit replacement for EU TED, has a free key-free OCDS API. The award value is rarely on the award, the rate-limit error is plain text (not JSON), and the honest volume is about 7 tenders a day.
date: 2026-09-10
tags: webscraping, api, procurement, opendata
tool: uk-find-a-tender-scraper
---

Every UK public contract above the procurement threshold — a council's heating-maintenance contract, an NHS trust's cleaning tender, a housing association's software project — gets published to **Find a Tender**, the UK government's official post-Brexit replacement for EU TED. It speaks [OCDS](https://standard.open-contracting.org/) (Open Contracting Data Standard), and the API is free and key-free:

```
GET https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages?updatedFrom=2026-09-01T00:00:00Z
```

No auth header, no API key, no proxy. We built [uk-find-a-tender-scraper](https://apify.com/fetchsmith/uk-find-a-tender-scraper) on exactly this endpoint, and paired it with [eu-ted-tenders-scraper](https://apify.com/fetchsmith/eu-ted-tenders-scraper) — post-Brexit UK notices are **not** in EU TED, so the two together are additive coverage, not a duplicate. As usual, the API itself is trivial; the shape of what it returns is where the real work is.

## The awarded value is (almost) never on the award

The obvious place to look for how much a contract is worth is `awards[].value`. On a live sample of 25 award notices, that field was `null` on every single one:

```json
"awards": [{
  "id": "1",
  "title": "Heating Maintenance 2026-2031",
  "value": null,
  "suppliers": [{"name": "City Plumbing Ltd"}]
}]
```

The real number lives one level over, on the **signed contract**:

```json
"contracts": [{
  "id": "1",
  "awardID": "1",
  "value": {"amount": 710000, "currency": "GBP"},
  "dateSigned": "2026-08-14"
}]
```

19 of the same 25 notices had a value there. So the Actor's value resolver prefers an explicit award value if one exists and otherwise totals the linked `contracts[].value` entries, exposing both `contractCount` (how many contracts were summed) and `awardValueSource` (`"award"` or `"contracts"`) so a buyer of the data can see which number they're getting rather than trusting a silently-merged field.

## A rate-limit error that looks like an empty result, not an error

Find a Tender rate-limits at roughly a dozen requests before returning `429`. Nothing unusual there — except the body isn't JSON:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 120
Content-Type: text/plain

Rate limit of 12 exceeded. Please retry after 120 seconds.
```

A client built with `responseType: 'json'` — a completely reasonable default against a JSON API — throws or silently gets `undefined` back from the parser on a plain-text body. In our first build, that meant `releases` came back `undefined`, the loop found nothing to push, and **the run finished reporting "Scanned 0 releases, pushed 0" with no error at all.** Nothing crashed. Nothing logged a warning. It looked exactly like "there's nothing matching your filter today" — the worst kind of bug, because it's indistinguishable from a correct empty result unless you already know what a real empty result looks like.

The fix: fetch as text, parse manually, and only decode JSON once the response actually looks like JSON. Honour `Retry-After` if it's present in the headers (it is, reliably, even though the body isn't JSON). We verified live that this actually recovers: force a 429, the Actor logs it, waits the full 120 seconds, resumes, and returns the identical rows a clean run would have. The Actor also self-throttles to 10 requests per rolling 60 seconds, comfortably under the observed burst capacity, so a normal-sized run shouldn't hit this path at all — but a client that can't tell a rate-limit body from an empty page will fail silently regardless of how good its throttle is.

## `links.next` is absent, not empty, when there's nothing left

OCDS release packages paginate with a `links.next` URL. The gotcha isn't a bug so much as a scale-expectation trap: Find a Tender carries roughly **7–8 new tender-stage notices a day**. Query a 7-day window and you'll get one page, `links.next` simply won't be present in the response at all (not `null`, not an empty string — the key is missing), and that's the correct, complete result. If your pagination loop checks for the key's *presence* rather than truthiness that's fine; if it assumes multi-page results are the norm and treats a missing `next` as suspicious, you'll go looking for a bug that isn't there. This is a lead-quality feed, not a firehose — we say so in the product rather than implying otherwise.

## Packaged version

[uk-find-a-tender-scraper on Apify](https://apify.com/fetchsmith/uk-find-a-tender-scraper) wraps this: filter by CPV code, free-text query, value range and open/closed status, and get back one flat row per notice — buyer email/phone/URL, a value that's actually populated, deduplicated CPV codes gathered from every lot and item, and named winning suppliers on award notices. HTTP-only, no browser, no proxy, pay per result, and every filtered-out row is free.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every response shape above comes from a live request made while writing this post, not from documentation.*
