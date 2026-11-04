---
title: SEC Form 4 insider trades have a public JSON API with no key — here are the three endpoints
description: Every Form 4 insider trade filed with the SEC is readable over plain HTTPS with no API key, no login and no quota signup. Three endpoints do the whole job, and all three 403 on one missing header.
date: 2026-11-04
tags: webscraping, api, finance, opendata
tool: sec-insider-trades-scraper
---

Every time a corporate officer, director or 10% owner buys or sells their own company's stock, they file a **Form 4** with the SEC within two business days. All of it is public, and — unlike most financial data — all of it is readable over plain HTTPS with **no API key, no login, no quota signup and no paid tier**. There is no developer portal to register with because there is no key to issue.

Three endpoints do the entire job:

```
GET https://www.sec.gov/files/company_tickers.json          # ticker -> CIK
GET https://data.sec.gov/submissions/CIK##########.json      # every filing by one issuer
GET https://www.sec.gov/Archives/edgar/data/<cik>/<acc>/<doc>.xml   # the raw Form 4
```

That's it. Below is what each one actually returns, measured live while writing this.

## All three need a `User-Agent`, and the failure looks like a block, not a mistake

This is the single reason most first attempts fail. Send a request with no `User-Agent` and the SEC's edge rejects it:

```
$ curl -s -A "" -o /dev/null -w "%{http_code}" \
    https://www.sec.gov/Archives/edgar/daily-index/2026/QTR4/index.json
403

$ curl -s -A "" -o /dev/null -w "%{http_code}" \
    https://data.sec.gov/submissions/CIK0000320193.json
403
```

Add a header that identifies you and the same two URLs return `200`:

```
$ curl -s -H "User-Agent: YourApp/1.0 (you@example.com)" \
    -o /dev/null -w "%{http_code}" \
    https://www.sec.gov/Archives/edgar/daily-index/2026/QTR4/index.json
200
```

Both hosts enforce it — `www.sec.gov` and `data.sec.gov` alike. It is not a rate-limit response and retrying won't clear it; the SEC asks automated users to declare themselves, and the edge enforces that with a `403`. Note also that a bare `urllib.request.urlopen()` in Python sends `Python-urllib/3.x` and gets the same `403`, which is why this reads as "the SEC blocks scrapers" when it is really "the SEC blocks anonymous ones". Pair the header with a request gap — the SEC documents a ceiling of 10 requests/second (their figure, not something measured here), and our own Actor sleeps 150 ms between calls to sit comfortably under it.

## `company_tickers.json` is keyed by row number, not by ticker

The ticker-to-CIK map is one file, 796,507 bytes, 10,409 entries as of today. The shape surprises people:

```json
{"0": {"cik_str": 1045810, "ticker": "NVDA", "title": "NVIDIA CORP"},
 "1": {"cik_str": 320193,  "ticker": "AAPL", "title": "Apple Inc."},
 "2": {"cik_str": 789019,  "ticker": "MSFT", "title": "MICROSOFT CORP"},
 ...}
```

The keys are stringified **array indices**, not tickers, and the ordering is by market capitalisation rather than alphabetical — `"0"` is NVDA. So `map["AAPL"]` is `undefined` and always will be; you have to walk `Object.values()` and build the reverse index yourself.

Two more things worth knowing before you use it as a lookup table. `cik_str` is an **integer**, so it carries no leading zeros, while the submissions endpoint below wants the CIK zero-padded to ten digits — `320193` has to become `0000320193`. And the file is **not** one row per company: those 10,409 tickers resolve to only **8,004 distinct CIKs**, with **1,436 CIKs carrying more than one ticker**. Alphabet alone appears four times:

```json
{"cik_str": 1652044, "ticker": "GOOGL", "title": "Alphabet Inc."}
{"cik_str": 1652044, "ticker": "GOOG",  "title": "Alphabet Inc."}
{"cik_str": 1652044, "ticker": "GOOGN", "title": "Alphabet Inc."}
{"cik_str": 1652044, "ticker": "GOOGM", "title": "Alphabet Inc."}
```

So ticker→CIK is many-to-one and safe; a CIK→ticker map built in the same pass silently keeps whichever share class happened to be last. It also matters for insider trades specifically: Form 4 filings attach to the **issuer's CIK**, not to a ticker, so all four Alphabet symbols return exactly the same filings — querying `GOOGL` and `GOOG` together is a duplicate request, not broader coverage.

## `submissions/CIK##########.json` caps `recent` at ~1,000 filings — a count, not a time window

This is the filing index for one issuer. For Apple (CIK `0000320193`, zero-padded, 163,919 bytes):

```json
{"cik": "320193", "name": "Apple Inc.",
 "filings": {
   "recent": {"accessionNumber": [...], "filingDate": [...], "form": [...], "primaryDocument": [...]},
   "files": [{"name": "CIK0000320193-submissions-001.json",
              "filingCount": 1271, "filingFrom": "1994-01-26", "filingTo": "2015-10-03"}]}}
```

`filings.recent` is a **columnar** object — fifteen parallel arrays (`form`, `filingDate`, `accessionNumber`, `primaryDocument` and so on), not a list of filing objects — so you select a filing by index across all arrays, not by iterating records.

It held **1,002 filings** for Apple today, spanning `2015-10-05` to `2026-11-03`, of which **601 were Form 4**. The important part: that ~1,000 is a *count* ceiling, not a date window. Apple's happens to reach back eleven years because Apple files in bursts; a company that files constantly will have a `recent` block covering months, and everything older moves into the paginated `files[]` entries (one page here, 1,271 filings from 1994 to 2015). If you are backfilling insider trades and only read `recent`, you will silently get a different depth of history per issuer — the most common way an EDGAR backfill comes out wrong without erroring.

Filter `form` for `"4"` (and `"4/A"` for amendments, `"3"` for initial statements of holdings, `"5"` for annual catch-ups), take the matching `accessionNumber` and `primaryDocument`, and you have the URL of the raw filing.

## The actual trade is in the ownership XML, not the JSON

Neither JSON endpoint contains a share count or a price. `submissions` gives you *that a Form 4 exists*; the trade itself lives in the ownership XML under `/Archives/edgar/data/<cik>/<accession-no-dashes>/<primaryDocument>`, as `<nonDerivativeTransaction>` and `<derivativeTransaction>` elements carrying the transaction date, SEC transaction code, share count, price per share, acquired-or-disposed flag and shares held afterwards. One filing routinely holds several transactions, and [one filing can name ten reporting owners](/blog/sec-form-4-joint-filings-reporting-owners), so "one filing" and "one insider trade" are not the same row — which is why a filing-index feed can never answer "what did officers buy last week".

Three traps live in that XML specifically, each measured and written up separately:

- The Rule 10b5-1 plan flag [is not spelled `true`](/blog/sec-form-4-10b5-1-flag-is-not-a-boolean) — 92% of filings write it as `1` or `0`.
- Amendments (`4/A`) correct real numbers, and [no insider-trading Actor's input schema can select them](/blog/sec-form-4-amendments-are-unselectable) by form type alone.
- Transaction codes are not all trades. A large `F` (shares withheld for taxes) or `M` (option exercise) row is compensation mechanics; counting it as "insider selling" is the most common mistake in this dataset.

## Packaged version

[sec-insider-trades-scraper on Apify](/go/sec-insider-trades-scraper) wraps all four steps: tickers or CIKs in, **one flat row per reported transaction** out, with the transaction code decoded to English, `transactionValueUsd` pre-signed so a position change is a `SUM()` over one column, and the 10b5-1 flag and footnotes carried through. Filters (`transactionCodes`, `minTransactionValue`, `insiderRoles`) run *before* billing, so "open-market buys over $250k by an officer" costs you those rows and nothing else. It deliberately never emits the reporting person's street address, which the ownership XML does contain. No API key, no start fee, HTTP only — no headless browser.

EDGAR is one of eight key-free government JSON APIs we build against; the cross-API comparison is in [Eight government JSON APIs that need no key](/blog/free-government-data-json-apis-no-key), and the full catalogue is at [fetchsmith.com/tools](https://fetchsmith.com/tools).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every status code, byte count and number above comes from a live request made while writing this post, not from documentation.*
