---
title: The EU publishes every public contract as JSON — in 24 languages, with the CPV code repeated eight times
description: TED, the EU's official procurement journal, has a free key-free JSON API for every public contract awarded in the union. The catch is the shape of the data — multilingual maps, duplicated arrays and a field that returns -1 instead of null.
date: 2026-09-10
tags: webscraping, api, procurement, opendata
tool: eu-ted-tenders-scraper
---

Every public contract awarded anywhere in the EU — a German county buying servers, a French hospital's cleaning contract, Deutsche Bahn's e-learning platform — gets published to **TED (Tenders Electronic Daily)**, the EU's official procurement journal. And unlike most government-data portals, TED's search API is a plain, free, key-free JSON endpoint. No login, no per-country quirks, no PDF scraping.

```
POST https://api.ted.europa.eu/v3/notices/search
Content-Type: application/json

{"query": "buyer-country=DEU AND classification-cpv=72000000 AND publication-date>=today(-30)",
 "fields": ["publication-number", "notice-title", "buyer-name", "total-value"],
 "limit": 10}
```

That's it. No auth header, no API key, no proxy. We built [eu-ted-tenders-scraper](https://apify.com/fetchsmith/eu-ted-tenders-scraper) on exactly this endpoint. The API itself is trivial; the raw response is what takes work.

## Every text field is a 24-language map — and the shapes don't agree with each other

Ask for `notice-title` and you get every EU official language back at once, unasked:

```json
"notice-title": {
  "eng": "Germany – Servers – Erweiterung Nutanix HCI Lösung",
  "deu": "Deutschland – Server – Erweiterung Nutanix HCI Lösung",
  "fra": "Allemagne – Serveurs – Erweiterung Nutanix HCI Lösung",
  "hun": "Németország – Szerverek – Erweiterung Nutanix HCI Lösung",
  ...
}
```

24 keys, one string each. Fine — pick `eng`, fall back to whatever key exists if it's missing. Except `buyer-name` on the very same notice looks like this:

```json
"buyer-name": { "deu": ["Landratsamt Würzburg"] }
```

Not a string. An **array of one string**, and often only a single language key (the buyer only ever registered their name in German). `buyer-city` is a third shape again:

```json
"buyer-city": { "mul": ["Würzburg"] }
```

`mul` — TED's own code for "multilingual/undetermined" — as the only key, still wrapped in an array. Three fields on the same notice, three different value shapes under the same nominal "multilingual map" structure. A normalizer that assumes every map value is a string (correct for `notice-title`) silently returns `"[object Object]"` or `undefined` the first time it hits `buyer-name`. One that assumes every value is an array (correct for `buyer-name`) does the same thing to `notice-title`. We shipped the first version of this Actor with exactly that bug — it picked a non-English fallback language on any field shaped as an array, because the string-vs-array branch was missing. Every real normalizer for this API has to check both shapes per field, not assume one.

## Arrays repeat themselves, a lot

A single notice's `classification-cpv` (the EU's standard product/service classification codes) came back as:

```json
["48820000", "48000000", "32420000", "72700000", "48820000", "48000000", "32420000", "72700000"]
```

Four distinct codes, each listed twice. TED's schema is per-lot, and a multi-lot notice repeats shared metadata once per lot rather than deduplicating it — we've seen the same CPV code repeated close to 20 times on notices with many lots. If you're counting "how many contracts mention CPV 72700000" or building a facet count from the raw array length, you will overcount by whatever the lot count happens to be. Deduplicate before you count anything.

## `total-value` sometimes means "not disclosed" — and once meant literally `-1`

Not every notice discloses a contract value; plenty of rows simply omit `total-value` and `total-value-cur` entirely, which is a normal, honest "we don't know." But one live notice in our sample returned:

```json
"total-value": -1
```

Not missing. Not `null`. The literal number `-1`. There's no negative contract in the world this could represent — it's a sentinel for "no value," except one that will pass a naive `if (value)` check with a false-looking-real number and probably poison your average-contract-value chart with an outlier that isn't hiding a real number at all. We guard it: any value `<= -1` normalizes to `null`, same as if the field were absent.

## The field-name list isn't in public docs — it's in the API's own error message

TED's request/response reference documents the notice *schema* but doesn't cleanly enumerate the exact `fields` strings the search API accepts by name (there are roughly 1,800 of them, one per legal metadata element). The fast way to find one: ask for a field name you're guessing at, wrong, and read the 400 body.

```
$ curl -s -X POST https://api.ted.europa.eu/v3/notices/search \
    -d '{"query":"publication-date>=today(-1)","fields":["not-a-real-field"],"limit":1}'
{"message":"Parameter 'fields' contains unsupported value (supported values are:
 sme-part, touchpoint-gateway-ted-esen, submission-url-lot, ...
 organisation-email-tenderer, organisation-country-buyer, ...
```

The error dumps the entire valid `fields` enum, comma-separated, right there in the message body. That's how we found `organisation-email-buyer` and `organisation-tel-buyer` — the two fields that turn a procurement notice from reference data into an actual lead:

```json
"organisation-email-buyer": ["ausschreibungen@lra-wue.bayern.de"],
"organisation-tel-buyer": ["+49 3029756741"]
```

A direct email or phone number for the procurement office behind the contract, present on the large majority of notices we sampled. If you're building anything for the bid side of this market — agencies, consultancies, contractors looking for public work — a buyer's name and a CPV code tell you a contract exists; an email tells you who to write to about it.

## Packaged version

[eu-ted-tenders-scraper on Apify](https://apify.com/fetchsmith/eu-ted-tenders-scraper) wraps this: filter by buyer country, CPV code, notice type and publication date (or pass a raw TED expert-query string), and get back one flat row per notice — English-preferred title, deduplicated CPV and place-of-performance arrays, a guarded `totalValue`, and the buyer's email/phone/URL where TED has them. HTTP-only, no browser, no proxy, pay per result.

If you need the UK's or the US's equivalent public-procurement feed instead, see [UK Find a Tender / Contracts Finder](/blog/uk-find-a-tender-ocds-json-api) and [USAspending federal awards](/blog/usaspending-federal-awards-json-api) — same idea, different shapes and gotchas per country.

TED's shape problems sit alongside the counting problems of the other seven key-free government APIs we build against — the full cross-API comparison is in [Eight government JSON APIs that need no key](/blog/free-government-data-json-apis-no-key).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every JSON snippet above comes from a live request made while writing this post, not from documentation.*
