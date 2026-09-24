---
title: SEC Form 4's 10b5-1 flag is not spelled "true" — 92% of filings write it as 1 or 0
description: A 210-filing live pull across 15 large-cap issuers found the aff10b5One element serialized four different ways, with the obvious boolean check ("=== 'true'") wrong on 92% of them. The same 479 rows also show why sorting Form 4 data by USD value quietly discards a third of it, and that genuine open-market insider buying is 1.25% of rows.
date: 2026-09-24
tags: webscraping, sec, edgar, finance, dataquality
tool: sec-insider-trades-scraper
---

[sec-insider-trades-scraper](https://apify.com/fetchsmith/sec-insider-trades-scraper) reads SEC EDGAR's raw ownership XML and emits one flat row per reported Form 3/4/5 transaction. Two parts of that mapping were reasoned about but never measured at scale: how the 10b5-1 plan checkbox is actually serialized by real filing agents, and how much of the `transactionValueUsd` column is usable. A live pull of 210 Form 4 filings from 15 large-cap issuers — AAPL, NVDA, JPM, MSFT, TSLA, WMT, XOM, KO, GS, PFE, DIS, BA, CVS, F, GE — yielding 479 transaction rows, answered both. The first answer is a trap that anyone parsing this XML themselves will fall into.

## The 10b5-1 flag has four spellings, and "true" is the rare one

Rule 10b5-1 is the pre-arranged trading plan defence: a sale made under a plan adopted months earlier is a scheduled liquidation, not a signal. Since the 2022 amendments, Form 4 carries a checkbox for it, and the XML element is `<aff10b5One>`. It is a boolean field, so the natural line to write is `aff10b5One === 'true'`.

Across all 210 filings, every one carried the element — it is never absent on recent filings — but the value came back four different ways:

| Serialized value | Filings | Share |
|---|---|---|
| `0` | 167 | 79.5% |
| `1` | 27 | 12.9% |
| `true` | 9 | 4.3% |
| `false` | 7 | 3.3% |

So 194 of 210 filings (92.4%) use `1`/`0` and only 16 (7.6%) use `true`/`false`. The choice tracks the filing agent, not the issuer or the transaction — the same element, in the same schema position, in the same week.

The consequence for a `=== 'true'` check is not a parse error, it is a silent wrong answer in the safe-looking direction: every `1` becomes `false`. Of the 36 filings in this sample that actually declare a 10b5-1 plan, 27 spell it `1` — so that check reports **75% of genuine plan-based trades as discretionary**, which is exactly backwards from the interpretation a reader wants. Nothing throws, no field is empty, and the column looks fully populated.

The Actor's coercion accepts both spellings (`s === 'true' || s === '1'`), so `rule10b5_1Plan` is correct on all 210. Worth stating as a verified negative rather than an assumption, because it was one.

A second thing this pull settled: `<aff10b5One>` sits at document level in **210 of 210** filings, outside every `<transactionCoding>` block, and no filing carried conflicting values. A per-filing read is therefore the right shape — a filing never mixes plan and non-plan transactions in practice — and the flag can be applied to every row the filing produces.

## A third of the USD value column is structurally empty

`transactionValueUsd` is derived (`shares x price`, signed negative on a disposition) because every buyer computes it and half get the sign wrong. But it can only exist where the filing reports a price, and 155 of the 479 rows (32.4%) have no usable price — either an explicit `0` or no `<transactionPricePerShare>` value at all. Which rows those are is entirely predictable from the transaction code:

| Code | Meaning | Rows | With usable USD | Zero/absent |
|---|---|---|---|---|
| S | Open-market sale | 215 | 215 | 0 |
| M | Option exercise/conversion | 101 | 34 | 67 |
| A | Grant/award | 98 | 31 | 67 |
| F | Shares withheld for taxes | 36 | 36 | 0 |
| G | Gift | 12 | 0 | 12 |
| P | Open-market purchase | 6 | 6 | 0 |
| C | Conversion of derivative | 4 | 0 | 4 |
| J | Other | 4 | 0 | 4 |
| D | Disposition to issuer | 3 | 2 | 1 |

Sales and tax withholding always carry a price — those are real transactions at a real market price. Grants, RSU vests, gifts and conversions frequently do not, because no money changed hands: an RSU vesting at `A` with price `0` is a compensation event, not a $0 purchase.

The practical failure is a filter, not a crash. `transactionValueUsd > 0`, the obvious way to ask for "insider buying," drops all 12 gifts, all 4 conversions, and 134 of the 199 grant and exercise rows — about a third of the dataset, and specifically the entire compensation story. Filter on `transactionCode` for the behaviour you mean and treat a null value as "no price was reported," not as zero. `includeDerivative: false` removes the derivative half of the `M`/`A` noise if common-stock rows are all you need.

## Insider buying is 1.25% of Form 4 rows

The code histogram above is itself the most useful output of this pull. Code `P` — an insider actually buying shares on the open market with their own money, the event the phrase "insider buying" refers to — is **6 of 479 rows, 1.25%**. Code `S` is 215 rows, 45%. Grants and exercises are another 199, 42%.

Form 4 is overwhelmingly a record of compensation being issued and then sold. That is not a data-quality problem; it is what the form is for. But it does mean a dashboard that plots "insider transactions" over time is plotting the vesting calendar, and any signal worth acting on lives in a thin 1% slice that has to be selected for explicitly. Pull the `P` rows, and cross-reference `rule10b5_1Plan` before reading intent into an `S` — in this sample, 111 of the 215 sales were plan-based.

## Reproducing

```json
{
  "issuers": ["AAPL", "NVDA", "JPM", "MSFT", "TSLA", "WMT", "XOM", "KO",
              "GS", "PFE", "DIS", "BA", "CVS", "F", "GE"],
  "formTypes": ["4"],
  "maxFilingsPerIssuer": 14,
  "maxResults": 500
}
```

Counts are from filings current as of 2026-09-24 and will drift as issuers file; the serialization split and the code-to-price relationship are structural and should not.

[sec-insider-trades-scraper](https://apify.com/fetchsmith/sec-insider-trades-scraper) normalizes all four `aff10b5One` spellings, decodes every transaction code into `transactionCodeMeaning`, and signs `transactionValueUsd` so a disposition is negative — leaving `null` where the filing reported no price rather than pretending it was zero. No API key, no start fee.

## Related guides

- All FetchSmith tools: https://fetchsmith.com/tools

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every number above comes from a live request made while writing this post, not from documentation.*
