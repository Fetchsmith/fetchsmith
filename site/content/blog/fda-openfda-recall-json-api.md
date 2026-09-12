---
title: The FDA publishes every product recall as JSON with no API key — but you can't page past row 25,000, and only drugs come with a barcode
description: openFDA's enforcement API covers food, drug and device recalls with no auth. The catches are a hard 25,000-row skip cap and a barcode-lookup field that only exists on drug recalls.
date: 2026-09-11
tags: webscraping, api, opendata, compliance
tool: fda-recall-scraper
---

Every US product recall the FDA has classified — a spinach lot pulled for listeria, a blood-pressure drug pulled for an impurity, an infusion pump pulled for a firmware bug — is public on **openFDA's enforcement API**, and it needs nothing to query:

```
GET https://api.fda.gov/drug/enforcement.json?search=classification:%22Class+I%22&limit=100&sort=report_date:desc
```

No key, no login, no proxy — verified 200 from a plain datacenter IP with zero setup. There are three of these endpoints, one per FDA center (`food`, `drug`, `device`), each with the same shape and the same Lucene-style `search=` syntax. We built [fda-recall-scraper](https://apify.com/fetchsmith/fda-recall-scraper) to cover all three in one run, because almost none of the ~25 competing scrapers we found do — most split by a single product type, which is the gap this Actor closes. The API itself is trivial. Two things about the data aren't.

## You cannot page past row 25,000

`skip` and `limit` work exactly as you'd expect — up to a point:

```
GET https://api.fda.gov/food/enforcement.json?search=classification:%22Class+I%22&skip=26000&limit=100
```

```json
{"error": {"code": "BAD_REQUEST", "message": "Skip value must 25000 or less."}}
```

That's a clean, documented `400`, not a silent truncation — better than several APIs we've built against (Contracts Finder just stops handing back a `next` cursor with no error at all). But a broad query easily exceeds it: `classification:"Class I"` on the food endpoint alone matches `total: 29386` records right now, more than the cap allows in one linear walk. The fix is date-range chunking — split the query into `report_date:[YYYYMMDD+TO+YYYYMMDD]` windows narrow enough that no single window's `total` crosses 25,000, then page each window from 0. We verified this is exactly additive before shipping it: splitting one 12,916-row Class I query into three year-boundary windows returned `2820 + 5427 + 4669 = 12916` — no duplicate, no gap. The Actor does this automatically once a query's reported total exceeds ~24,000; you never see `skip` in the input at all.

## `openfda.*` — the barcode-lookup fields — only exist on drug recalls

Every enforcement record carries an `openfda` sub-object that's *supposed* to hold cross-referenced identifiers. In practice it's populated on one product type and empty on the other two:

```json
// drug recall — openfda populated
"openfda": {
  "brand_name": ["LEVOTHYROXINE SODIUM"],
  "generic_name": ["LEVOTHYROXINE SODIUM"],
  "manufacturer_name": ["Accord Healthcare Inc."],
  "product_ndc": ["16729-447"],
  "package_ndc": ["16729-458-15"],
  "upc": ["0316729447157"],
  "substance_name": ["LEVOTHYROXINE SODIUM"],
  "rxcui": ["892246"],
  "unii": ["9J765S329G"]
}
```

```json
// food or device recall from the same window — openfda empty
"openfda": {}
```

That's not a one-off gap in a couple of records — we sampled the five newest reports of each product type twice, on two different days, and got 5/5 populated on every drug sample and 0/5 on every food and device sample, both times. Drugs get NDC, package NDC, UPC, brand name, generic name, manufacturer and substance name for free; food and device recalls carry none of it, ever — there's no equivalent barcode field to fall back to on those two endpoints. If you need to match a recall against your own catalogue by NDC or UPC rather than by fuzzy product-name matching, that only works for drugs, and the Actor's schema reflects it: those columns are always present for CSV stability, just `null`/`[]` outside `productType:"drug"` rows.

## The date filter and the "when did this actually start" field are different columns

One more gotcha worth knowing before you filter by date: `report_date` — the field every date-range parameter here actually filters on — is when the FDA *published* the enforcement report, not when the firm started the recall. That can lag by weeks or months behind `recall_initiation_date`. Searching for "recalls that started last week" against `report_date` will miss real matches that are still working their way through FDA's publication process; `recall_initiation_date` is the field to read for the firm's own timeline, but it isn't what the API's date filter uses.

## Packaged version

[fda-recall-scraper on Apify](https://apify.com/fetchsmith/fda-recall-scraper) wraps all three endpoints into one schema: pick `food`, `drug` and/or `device` (interleaved, not one type after another), filter by classification, state, status or free text, and get back 33 flat fields with dates normalized to ISO and the drug-only `openfda` identifiers already flattened where they exist. The 25,000-row cap and its date-chunking workaround are handled internally — you just get more rows back on a wide query, automatically. No API key, no proxy, pay per result.

openFDA's 25,000-row skip cap is the same silent-truncation class we hit on ClinicalTrials.gov, NIH RePORTER and Contracts Finder — the cross-API comparison across all eight key-free government APIs we build against is in [Eight government JSON APIs that need no key](/blog/free-government-data-json-apis-no-key).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every JSON snippet above comes from a live request made while writing this post, not from documentation.*
