# SEC Insider Trades Scraper — Form 4 buys & sells as flat rows

Reads **SEC EDGAR ownership filings (Forms 3, 4 and 5)** straight from the SEC's own keyless
endpoints and returns **one flat row per reported transaction** — not one row per filing, and not
a PDF link you still have to parse.

Give it tickers (`AAPL`, `NVDA`) or raw CIK numbers. Tickers are resolved against SEC's official
`company_tickers.json` map, so an unlisted ticker is skipped with a warning instead of silently
returning nothing.

## Why this one

- **Parsed transactions, not filing lists.** Most EDGAR Actors hand you an index of 10-K/10-Q/8-K
  filings. This one opens the raw ownership XML behind each Form 4 and pulls out the trade:
  who, what role, which code, how many shares, at what price, how many held afterwards.
- **`transactionCode` is decoded.** `S` → `Open-market sale`, `F` → `Shares withheld for taxes`,
  `M` → `Option exercise/conversion`, and so on for all 17 codes. The distinction matters: a
  large `F` or `M` row is routine compensation mechanics, not a bearish signal, and treating
  every disposition as "insider selling" is the single most common mistake in this dataset.
- **`transactionValueUsd` is signed and pre-computed** — negative on a disposition, positive on
  an acquisition — so you can sum a column without re-deriving the sign from
  `acquiredOrDisposed`.
- **Rule 10b5-1 flag and footnotes are carried through**, which is how you tell a pre-scheduled
  plan sale from a discretionary one.
- **No personal addresses.** The ownership XML contains the reporting person's street address.
  This Actor deliberately never emits it. Names, CIKs, roles and officer titles are the public
  corporate disclosure; the address block is personal data and is not part of this product.
- **No API key, no start fee, HTTP only** (no headless browser), pay only per transaction row.

## Output fields

`id`, `accessionNumber`, `formType`, `filingDate`, `periodOfReport`, `issuerName`, `issuerCik`,
`ticker`, `insiderName`, `insiderCik`, `isDirector`, `isOfficer`, `isTenPercentOwner`, `isOther`,
`officerTitle`, `coFilers`, `derivative`, `securityTitle`, `transactionDate`, `transactionCode`,
`transactionCodeMeaning`, `acquiredOrDisposed`, `shares`, `pricePerShare`, `transactionValueUsd`,
`sharesOwnedAfter`, `directOrIndirect`, `indirectOwnershipNature`, `exercisePrice`,
`expirationDate`, `underlyingSecurityTitle`, `underlyingShares`, `rule10b5_1Plan`, `footnotes`,
`filingUrl`, `url`.

Derivative rows (options, RSUs, convertibles) carry `exercisePrice`, `expirationDate`,
`underlyingSecurityTitle` and `underlyingShares`; non-derivative common-stock rows leave them
`null`. Set `includeDerivative: false` to get common stock only.

### Sample row

```json
{
  "id": "0001140361-26-037020-n0",
  "accessionNumber": "0001140361-26-037020",
  "formType": "4",
  "filingDate": "2026-09-17",
  "periodOfReport": "2026-09-15",
  "issuerName": "Apple Inc.",
  "ticker": "AAPL",
  "insiderName": "Newstead Jennifer",
  "isOfficer": true,
  "officerTitle": "SVP, GC and Government Affairs",
  "derivative": false,
  "securityTitle": "Common Stock",
  "transactionDate": "2026-09-15",
  "transactionCode": "S",
  "transactionCodeMeaning": "Open-market sale",
  "acquiredOrDisposed": "D",
  "shares": 1438,
  "pricePerShare": 330.19,
  "transactionValueUsd": -474813.22,
  "sharesOwnedAfter": 32914,
  "rule10b5_1Plan": true,
  "footnotes": "This transaction was made pursuant to a Rule 10b5-1 trading plan adopted by the reporting person on May 5, 2026."
}
```

## Notes on the source

- Form 3 is an **initial** statement of holdings and Form 5 an annual catch-up; both are largely
  holdings rather than open-market trades, so a Form 3 often yields **zero transaction rows**.
  That is the filing, not a bug.
- A filing can be made jointly by several reporting persons. The first is used for the
  `insiderName`/role fields and the rest are listed in `coFilers` rather than dropped.
- SEC's filing index is newest-first, so `sinceDate` stops paging as soon as it passes the date.
- **`rule10b5_1Plan` is normalized across four different spellings.** Measured over 210 real Form 4
  filings from 15 large-cap issuers, the `<aff10b5One>` element came back as `0` (167 filings),
  `1` (27), `true` (9) and `false` (7) — 92% of filings use `1`/`0`, not `true`/`false`. A
  hand-rolled `=== 'true'` check therefore reports 75% of genuine plan-based trades as
  discretionary, silently and in the misleading direction. This Actor accepts both spellings.
  The element was present on all 210 filings and always at document level (never inside
  `transactionCoding`, never with conflicting values), so the flag applies to every row of a filing.
- **A third of rows carry no USD value, and which ones is predictable.** In the same 479-row
  sample, 155 rows (32.4%) had a price of `0` or no price element, so `transactionValueUsd` is
  `null`. Sales (`S`, 215/215) and tax withholding (`F`, 36/36) always priced; gifts (`G`, 0/12),
  conversions (`C`, 0/4) and `J` never; option exercises (`M`, 34/101) and grants (`A`, 31/98)
  about a third of the time — no money changed hands, so there is no price to report. Filter on
  `transactionCode` for the behaviour you mean rather than on `transactionValueUsd > 0`, which
  drops those rows. Genuine open-market purchases (`P`) were 6 of 479 rows (1.25%).
- Measured across 160 real Form 4 transactions from 11 large-cap issuers (MSFT, ADBE, ORCL, CRM,
  NOW, IBM, META, TSLA, AMZN, GOOGL, NVDA): `exercisePrice` was populated on 15/33 (45%) of
  derivative rows — the rest were RSU vests, which have no strike price — while `expirationDate`
  and `coFilers` were both 0% in this sample. RSU-heavy mega-cap grants rarely carry an
  expiration date, and none of the 11 issuers sampled had a jointly-filed Form 4 in the window
  checked; both fields do populate on option grants and family/trust co-ownership filings, just
  not reliably at large tech issuers. Set `includeDerivative: false` if you only need the
  common-stock rows.

## Related guides

- [SEC Form 4's 10b5-1 flag is not spelled "true" — 92% of filings write it as 1 or 0](https://fetchsmith.com/blog/sec-form-4-10b5-1-flag-is-not-a-boolean)
  — the 210-filing measurement behind the two notes above, plus the full transaction-code histogram.
- [We checked every other government-data Actor for the same boolean trap](https://fetchsmith.com/blog/sec-form-4-is-the-only-actor-that-parses-raw-xml)
  — why this Actor is the only one in the fleet that could have it, and how to check that mechanically instead of by domain guess.
- All FetchSmith tools: https://fetchsmith.com/tools

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/sec-insider-trades-scraper
