---
title: "The EU's tender deadline isn't in the field called \"deadline\" — 48/50 live in a different one"
description: TED's procurement API has three separate deadline fields, and the one that actually holds a bid deadline on live call-for-competition notices isn't the generic-sounding one. A 50-notice measurement, split by notice type, of where the date really lives.
date: 2026-09-24
tags: webscraping, api, procurement, opendata
tool: eu-ted-tenders-scraper
---

TED (Tenders Electronic Daily), the EU's official procurement journal, has one field that sounds like the obvious place to find a tender's submission deadline: `deadline-date-lot`. We built [eu-ted-tenders-scraper](https://apify.com/fetchsmith/eu-ted-tenders-scraper) reading exactly that field first — and shipped a version where `deadlineDate` came back `null` on almost every notice, because the actual date almost never lives there.

## Three fields, one concept

TED's per-lot schema carries the submission deadline under three different keys, and which one a notice uses depends on its procedure type:

- `deadline-receipt-tender-date-lot` — the deadline for submitting a full tender, used by the standard open/restricted procedures.
- `deadline-date-lot` — a generic deadline field, used by a minority of procedure shapes.
- `deadline-receipt-expressions-date-lot` — the deadline for an *expression of interest*, used only by two-stage procedures where a shortlist is chosen before tenders are invited.

Any one of the three can be the only one present on a given notice, and a client that reads just `deadline-date-lot` — the field whose name looks generic enough to be "the" deadline field — gets `null` on most real notices, not an error, so the bug is silent.

## Measured live: 48/50 call-for-competition notices use the field you'd guess last

Pulled 50 fresh `cn-standard` notices (the "call for competition" type — an open invitation to bid, published while the tender is still live) from the last 30 days and checked which of the three fields was populated on each:

| Field | Notices (of 50) |
|---|---|
| `deadline-receipt-tender-date-lot` | **48** |
| `deadline-date-lot` | 1 |
| `deadline-receipt-expressions-date-lot` | 0 |
| none of the three | 1 |

96% of the notices you'd actually want a deadline for carry it under `deadline-receipt-tender-date-lot`. This matches an earlier, smaller sample we took while building the fix (9/10 on a single-country slice) — now confirmed at n=50 across the full EU.

## And on notices where bidding is already over, the count flips to zero

The obvious follow-up question: what happens on `can-standard` notices — contract-award results, published *after* the tender closed? Pulled 50 of those from the same 30-day window and checked the same three fields:

| Field | Notices (of 50) |
|---|---|
| `deadline-receipt-tender-date-lot` | 0 |
| `deadline-date-lot` | 0 |
| `deadline-receipt-expressions-date-lot` | 0 |
| none of the three | **50** |

Zero out of 50. Not a data-quality gap — a result notice has nothing left to bid on, so TED correctly omits every deadline field rather than publish a stale or meaningless date. This is exactly why our `onlyOpenDeadlines` filter treats "no deadline published" as **closed, not unknown**: on a `can-standard` notice, "no deadline" doesn't mean "ask again later," it means the bidding window is already gone.

## What the Actor does with this

`deadlineDate` is built by trying the three fields in the order the 50-notice measurement above justifies — tender-receipt first, then the generic field, then expressions-of-interest — and `deadlineType` on the output row says which of the three it actually came from, so you can tell a standard tender deadline apart from a shortlist-stage one without re-deriving it yourself. `daysUntilDeadline` is the whole-UTC-days countdown from that date, and `onlyOpenDeadlines`/`minDaysUntilDeadline` filter on it — so "give me tenders I can still bid on, with at least 2 weeks to prepare" is one filter, not a nested date check you write by hand.

[eu-ted-tenders-scraper on Apify](https://apify.com/fetchsmith/eu-ted-tenders-scraper) wraps the full TED search API — buyer country, CPV code, notice type, publication date or a raw expert-query string — into one flat row per notice, with this deadline logic, deduplicated CPV/place arrays, a guarded `totalValue`, and the buyer's email/phone where TED publishes one. See [the first TED guide](/blog/eu-ted-tenders-public-json-api) for the multilingual-map shapes, the CPV-subtree matching trap, and the `-1`-as-null sentinel on `total-value`.

If you need the UK's or the US's equivalent feed instead, see [UK Find a Tender / Contracts Finder](/blog/uk-find-a-tender-ocds-json-api) and [USAspending federal awards](/blog/usaspending-federal-awards-json-api).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every number above comes from a live request made while writing this post, not from documentation.*
