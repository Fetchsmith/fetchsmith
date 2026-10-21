---
title: The FEC's donor-search API accepts a page number on every request — and silently ignores it on three of four
description: api.open.fec.gov's /schedules/schedule_a/, schedule_b/ and schedule_e/ endpoints take a page= parameter, return 200, and hand back page 1 forever. Only /candidates/ actually pages. The real cursor is a field nobody reads by default.
date: 2026-10-17
tags: webscraping, api, opendata, government
tool: fec-campaign-finance-scraper
---

Our [earlier FEC post](/blog/fec-campaign-finance-json-api-demo-key) covered candidate search and financial totals — `/v1/candidates/` and `/v1/candidate/{id}/totals/`. The same API also serves the other half of campaign finance: who actually gave the money. `/v1/schedules/schedule_a/` is itemized individual contributions — donor name, employer, occupation, amount, date — and it's what powers donor-research questions like "how much did Google employees give in the 2024 cycle":

```
GET https://api.open.fec.gov/v1/schedules/schedule_a/?contributor_employer=GOOGLE&two_year_transaction_period=2024&per_page=5&sort=-contribution_receipt_date
```

That one query alone matches **129,917 rows**. No result set this size can come back in one page, so you reach for the obvious parameter: `page`. It's right there in the response:

```json
{"pagination": {"count": 129917, "pages": 25984, "per_page": 5, ...}}
```

25,984 pages, so page it is. Here's where it goes wrong.

## `page=2`, `page=30`, `page=500` all return page 1

Request the same query with `page=1`, `page=2`, and `page=3` and compare the first row's `sub_id` on each response:

```
page=1 first sub_id: 4051220251193594988
page=2 first sub_id: 4051220251193594988
page=3 first sub_id: 4051220251193594988
```

Identical. Not close — byte-identical, same transaction. Try `page=30` and `page=500`: same result, `HTTP 200`, no error, no warning header, `pagination.count` and `pagination.pages` both still correctly reporting the full 129,917/25,984. The API isn't rejecting the deep page — it's accepting the parameter and quietly doing nothing with it. A naive loop that pages until it sees an empty array will instead loop forever, re-fetching (and, in a billed pipeline, re-counting) the same five rows up to whatever iteration cap you happen to have.

We checked this wasn't a schedule_a-specific fluke. `/v1/schedules/schedule_e/` (independent expenditures — the super-PAC spending data) does the same thing: `page=1` and `page=5` on an identical `candidate_id` filter return the same `sub_id` first row. Our Actor's code comment, written after finding this the hard way, names a third: `schedule_b/` (committee disbursements). All three transaction schedules share it.

The control that proves it's not a general API quirk: `/v1/candidates/` pages normally.

```
page=1 first candidate: H4MI03185
page=2 first candidate: H2RI02085
```

Different candidate, every time. So the FEC API has two pagination regimes live on the same base URL, and nothing in a `200` response tells you which one you're talking to.

## The real cursor is `pagination.last_indexes`, not `page`

Every schedule_a/b/e response carries the field that actually works, buried in the pagination block:

```json
"last_indexes": {"last_contribution_receipt_date": "2024-12-31", "last_index": "4050920251189652739"}
```

Feed those two values back as query parameters — `last_index` plus the schedule-specific sort-field name (`last_contribution_receipt_date` for schedule_a, sorted by `-contribution_receipt_date`) — and the *next* page actually arrives:

```
first page last sub_id:  4050920251189652739
next seek page first sub_id: 4050920251189567782
```

Different row. That's the whole mechanism: a keyset cursor, not an offset. It has to be read off the previous response and threaded into the next request by name — there's no `next_url` to just follow — and the field name changes depending which schedule you're querying (`last_contribution_receipt_date` for Schedule A, `last_disbursement_date` for Schedule B, `last_expenditure_date` for Schedule E). Get the field name wrong and the API's fallback is, consistent with everything else here, to not error: it just ignores the unrecognized cursor and hands back page 1 again.

## A secondary trap in the same query: `contributor_employer` is a partial, tokenized match

While we had the employer filter open, we checked whether it does exact matching. It doesn't:

```
contributor_employer=GOOGLE       -> 129,917 rows
contributor_employer=GOOGLE LLC   ->  21,835 rows
contributor_employer=GOOGL        -> 129,954 rows
```

`GOOGLE` on its own pulls in every filer who wrote "GOOGLE INC.", "GOOGLE LLC", "GOOGLE WIFI" or just "GOOGLE" as their self-reported employer — it's a free-text match on the field, not an equality filter, which is what you want for donor research (self-reported employer strings are never normalized) but means a narrower-looking query can return *more* rows than the string you'd assume it's a substring of, if the index is also doing stemming or token-prefix matching rather than plain substring containment — `GOOGL` outscoring `GOOGLE` by 37 rows only makes sense that way. Don't treat a smaller row count as validation that your filter is more specific; check what the extra or missing rows actually say before trusting either number.

## The packaged version

Our [FEC Campaign Finance Scraper](/tools/fec-campaign-finance-scraper)'s `contributions`, `disbursements` and `independentExpenditures` search modes all walk the `last_indexes` cursor internally — `page` is never sent to these three endpoints at all, because a parameter that silently no-ops is worse than one that errors; you can't detect the bug from the response, only from running the same page twice and diffing. `candidates` mode, correctly, still uses normal `page` paging, since that's the one endpoint where it actually works.

Paging is only the question of *which* rows you get back; a separate trap sits on the rows themselves. The committee object embedded in a Schedule A contribution has a plural `candidate_ids` list, and reading "2+ entries" as "joint fundraising committee" is wrong 92% of the time — [a two-cycle scan of the full committee registry](https://fetchsmith.com/blog/fec-committee-candidate-ids-plural-is-not-joint-fundraising) found 426 of 430 such committees are one person holding a House id and a Senate id at once. Worth reading alongside this post if you are attributing contributions to candidates yourself, because the same reasoning does *not* carry over to Schedule B, where the embedded committee is the payer rather than the recipient.

If you're building against FEC data generally, the candidate/totals-side traps (rate limits, N+1 totals, duplicate election-year rows) are in the [earlier post](/blog/fec-campaign-finance-json-api-demo-key), and the comparison across eight other key-free government APIs we ship against is in [Eight government JSON APIs that need no key](/blog/free-government-data-json-apis-no-key). Full tool list at [fetchsmith.com/tools](/tools). [Run the FEC scraper on Apify](/go/fec-campaign-finance-scraper).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every JSON snippet and number above comes from a live request made while writing this post, not from documentation.*
