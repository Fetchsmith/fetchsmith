---
title: The Federal Register tells you tomorrow's rules today — but only for 16 hours a day
description: The Public Inspection desk (federalregister.gov's /public-inspection-documents.json) publishes filed-but-not-yet-official documents 1-3 business days early. Verified live, one document read a full day before it existed on the official archive endpoint — and the desk has an undocumented daily blackout window a naive daily cron will misread as "nothing new."
date: 2026-09-24
tags: webscraping, api, opendata, json
tool: federal-register-scraper
---

Every rule in the *Federal Register* is public JSON the moment it's officially published — that's the subject of [our first guide to this API](/blog/federal-register-documents-json-api). What's less known: the Office of the Federal Register runs a second, smaller endpoint that shows you documents **before** they're official.

## Proof, not a claim: reading tomorrow's rule today

At 05:01 Eastern on 2026-09-24, this returned a real, scheduled rule:

```
GET https://www.federalregister.gov/api/v1/public-inspection-documents.json?per_page=1
```

```json
{
  "document_number": "2026-19681",
  "title": "Atlantic Highly Migratory Species: Atlantic Bluefin Tuna Fisheries; Closure of the General Category September Fishery for 2026",
  "type": "Rule",
  "filed_at": "2026-09-23T20:15:00Z",
  "filing_type": "special",
  "publication_date": "2026-09-25",
  "pdf_url": "https://public-inspection.federalregister.gov/2026-19681.pdf"
}
```

Full title, agency, page count and a working PDF — for a rule NOAA filed the previous afternoon (4:15pm Eastern) that isn't scheduled to publish until the **next day** (2026-09-25). We confirmed it wasn't reachable yet the normal way:

```
GET https://www.federalregister.gov/api/v1/documents/2026-19681.json
→ 404 Not Found
```

That's the whole value proposition of `dataset: "publicInspection"` in one pair of requests: the same document is fully readable through Public Inspection roughly a day before the "official" endpoint even acknowledges it exists.

## The desk isn't open 24 hours — and it doesn't tell you that with an empty result

Here's the part that isn't in our own README yet, and isn't obvious from the schema. The response envelope carries a `meta` block most integrations never look at:

```json
"meta": {
  "pil_unavailability_message": "The Public Inspection list is unavailable after 12AM Eastern time and will return on Thursday, September 24 at 8:45AM Eastern time."
}
```

We hit that message live, at 05:01 Eastern — inside the stated blackout window. Critically, **the endpoint did not return zero rows or an error**. It returned 3 documents, all `filing_type: "special"`, all `filed_at` the previous afternoon, all carrying `last_public_inspection_issue: "2026-09-23"` — yesterday's leftover carryover, served as if it were live data.

If you build a naive "poll once a day, alert on anything new" cron and it happens to run before 8:45am Eastern, you'll either re-process yesterday's special filings as new, or — worse — conclude the desk is thin that day when the real issue simply hasn't posted yet. The fix is one field: compare `last_public_inspection_issue` against today's date (Eastern) before trusting a result as current, and treat `meta.pil_unavailability_message` (present or absent) as an explicit signal, not decoration.

## What this means for a watch-mode buyer

Combined with the immutability finding from [our first guide](/blog/federal-register-documents-json-api) — a published Federal Register document never mutates, corrections ship as new documents citing the original — the two endpoints form a clean pipeline: `publicInspection` for same-day advance warning of what's about to become law of record, `published` with `watchLabel` for the durable, citable, append-only history once it does. Watching only the published archive means finding out when everyone else does; watching Public Inspection on a schedule that respects its 8:45am–midnight Eastern window means finding out first.

---

[federal-register-scraper on Apify](https://apify.com/fetchsmith/federal-register-scraper) supports both datasets: `dataset: "published"` (the full 1994-present archive, with `watchLabel` incremental mode) and `dataset: "publicInspection"` (documents filed but not yet official, with the same `filedAt`/`filingType`/`onPublicInspection` fields shown above). No API key, no proxy, pay per result at $0.0008 — no start fee.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every response shape and timestamp above comes from live requests made while writing this post, not from documentation.*
