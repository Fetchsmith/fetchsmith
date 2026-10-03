# SEC Insider Trading Scraper — Form 4 insider trades, buys & sells as flat rows

Reads **SEC EDGAR ownership filings (Forms 3, 4 and 5)** straight from the SEC's own keyless
endpoints and returns **one flat row per reported transaction** — not one row per filing, and not
a PDF link you still have to parse.

Give it tickers (`AAPL`, `NVDA`) or raw CIK numbers. Tickers are resolved against SEC's official
`company_tickers.json` map, so an unlisted ticker is skipped with a warning instead of silently
returning nothing.

In short: an insider trading API over Form 4 data, callable from Apify without hosting an EDGAR
parser yourself.

## Why this one

- **Parsed transactions, not filing lists.** Most EDGAR Actors hand you an index of 10-K/10-Q/8-K
  filings. This one opens the raw ownership XML behind each Form 4 and pulls out the trade:
  who, what role, which code, how many shares, at what price, how many held afterwards.
- **`transactionCode` is decoded.** `S` → `Open-market sale`, `F` → `Shares withheld for taxes`,
  `M` → `Option exercise/conversion`, and so on for all 20 SEC-defined codes, including the rare
  `O` (out-of-the-money option exercise, seen a handful of times per quarter across all filers)
  and `V` (voluntarily reported early). The distinction matters: a
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
- **The filters run before billing.** `transactionCodes`, `minTransactionValue` and `insiderRoles`
  are applied to each parsed row *before* it is pushed or charged, so "only open-market buys over
  $250k by an officer" costs you those rows and nothing else.
- **No API key, no start fee, HTTP only** (no headless browser), pay only per transaction row.

## Output fields

`id`, `rowType`, `accessionNumber`, `formType`, `filingDate`, `periodOfReport`, `issuerName`, `issuerCik`,
`ticker`, `insiderName`, `insiderCik`, `isDirector`, `isOfficer`, `isTenPercentOwner`, `isOther`,
`officerTitle`, `coFilers`, `derivative`, `securityTitle`, `transactionDate`, `transactionCode`,
`transactionCodeMeaning`, `acquiredOrDisposed`, `shares`, `pricePerShare`, `transactionValueUsd`,
`sharesOwnedAfter`, `directOrIndirect`, `indirectOwnershipNature`, `exercisePrice`,
`expirationDate`, `underlyingSecurityTitle`, `underlyingShares`, `rule10b5_1Plan`, `footnotes`,
`filingUrl`, `url`.

Derivative rows (options, RSUs, convertibles) carry `exercisePrice`, `expirationDate`,
`underlyingSecurityTitle` and `underlyingShares`; non-derivative common-stock rows leave them
`null`. Set `includeDerivative: false` to get common stock only.

### Holdings rows (`includeHoldings`, off by default)

A Form 3 — and the holdings section of a Form 4/5 — reports a position the insider *holds*, not a
trade, and SEC files those in separate `<nonDerivativeHolding>`/`<derivativeHolding>` elements. With
`includeHoldings` off (the default) they are skipped, which means **a Form-3-only run returns zero
rows**; the Actor now warns about exactly that at the top of the run instead of leaving you to guess.

Set `includeHoldings: true` to get them as extra rows with `rowType: "holding"` (transaction rows are
`rowType: "transaction"`). On a holding row `transactionDate`, `transactionCode`,
`transactionCodeMeaning`, `acquiredOrDisposed`, `shares`, `pricePerShare` and `transactionValueUsd`
are `null` — there is no trade to report — and the position is in `sharesOwnedAfter` for common stock
or in `underlyingShares` for a derivative holding such as an RSU award (measured on Apple's
September 2026 Form 3s: 1 non-derivative + 7 derivative holding rows per filing, each with the full
vesting schedule in `footnotes`). It is opt-in so that an existing Form 4 caller's row count — and
therefore their bill — does not change.

### Narrowing the feed (`transactionCodes`, `minTransactionValue`, `insiderRoles`)

Most of a Form 4 feed is compensation plumbing rather than trading: across 8 consecutive Apple
Form 4s (17 rows, measured 2026-10-01) the mix was 12 `A` grants, 2 `S` open-market sales, 2 `M`
option exercises and 1 `F` tax withholding. If you only want the sales, three optional filters cut
the feed down **before anything is pushed or charged**:

- **`transactionCodes`** — e.g. `["P", "S"]` for open-market buys and sells only. All 20 SEC codes
  are selectable from the dropdown; the platform rejects anything else before the run starts.
- **`minTransactionValue`** — a USD floor compared on the **absolute** value, so a $2M sale
  (`transactionValueUsd: -2000000`) passes a `500000` floor exactly like a $2M purchase. Rows with
  no reportable value — holdings, and grants filed with no price — cannot be shown to clear the
  floor and are excluded.
- **`insiderRoles`** — any of `officer`, `director`, `tenPercentOwner`, `other`. Matched against the
  filing's first reporting owner; on a joint filing the other reporting persons appear in
  `coFilers` as names only and are not role-matched.

The filters are combined with AND, and they narrow **rows**, not filings: `maxFilingsPerIssuer`
still decides how far back the run looks, so a strict filter can return few rows from a filer who
simply made no matching trades recently. The run log prints how many rows each run dropped, and
says so explicitly when the filters removed everything.

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

## Pricing

`result` — **$0.0018 per returned transaction row, no Actor-start fee.**

Among listings that specialize in parsed insider-trading output, `ryanclinton` (52 users, `ryanclinton/sec-insider-trading`) remains the biggest, charging $0.002 per trade plus a small Actor-start fee — we're ~10% cheaper per row with no start fee at all. Their listing markets "behavioural insider-trading signal classification" (cluster-buy/regime-shift detection) over a 140+ field output schema; the extra fields we sampled at launch (cycle 810) read as speculative/AI-generated Store-listing padding (`signalGenome`, `manipulationResistance`, `institutionalNarrative`) rather than values a buyer could actually trust, so we did not copy them. This Actor instead differentiates on data fidelity: all 20 SEC transaction codes decoded (not just the common ones), a signed pre-computed USD value, the 10b5-1 plan flag normalized across its four real on-the-wire spellings (measured across 210 filings — see Related guides), and `sinceDate` that follows EDGAR's older paginated filing index instead of stopping at the ~12-month inlined window every other Actor in this niche appears to read from. Re-verified against their live pricing and stats 2026-10-03 — still 52 users at $0.002 per trade plus a $0.00005 Actor-start fee, unchanged since cycle 810's original audit.

**By raw user count, several generic multi-filing-type EDGAR scrapers are now bigger than any insider-trading specialist, including `ryanclinton`** — a 97-match, 7-term Store sweep, checked live 2026-10-03 (promoted into `bin/niche-size`'s `TERM_VARIANTS` this cycle; the single-term auto-sweep had returned only 15), surfaced them. `constant_quadruped/sec-edgar-filings-scraper` (101 users, 17 new in the last 30 days — the fastest-growing listing in this entire comparison) is on Apify's **FREE pricing model ($0/row)** and lists "insider trades" among 100+ fields across 10-K/10-Q/8-K/Form 4 filings; `constructive_calm/sec-edgar-scraper` (57 users) charges $0.0004 per **filing** fetched (10-K, 8-K, Form 4, 13F, etc. all the same price) plus a $0.01 start fee. Neither beats us on an apples-to-apples basis: both charge **per filing fetched, not per transaction parsed** — exactly the baseline this README's first "Why this one" bullet already describes, now named and priced. Apple's 8 sampled Form 4s average ~2.1 transaction rows per filing, so $0.0004/filing is closer to ~$0.0002/transaction-equivalent in practice — genuinely cheaper than our $0.0018, but neither decodes transaction codes, signs the USD value, or normalizes the 10b5-1 flag, and a buyer still has to parse the raw filing index or XML themselves to get a trade out of it. `constant_quadruped`'s $0 is unbeatable on sticker price regardless. Two more of the same class, dearer than us either way: `benthepythondev/sec-edgar-filings-intelligence` (20 users, $0.029 FREE → $0.0203 Diamond per filing row plus AI scoring) and `crawlerbros/sec-edgar-scraper` (12 users, $0.005 start + $0.002 FREE → $0.001 Diamond per filing row — a *different* listing from the already-named `crawlerbros/open-insider-scraper` below).

Across the whole Form 4 niche this remains the cheapest per-row listing by a wide margin, re-checked live 2026-10-02 against each rival's current pricing record with no drift from the previous audit: `scrapemint/sec-form4-insider-tracker` (13 users) charges $0.025 per filing row, `scrapers_lat/sec-form4-insider-trades-scraper` (2 users) $0.012 down to $0.0102 on the higher plans, and `parseforge/sec-form4-scraper` (2 users) $0.04999 down to $0.03749 plus a $0.005 start fee — 6x to 28x this Actor's $0.0018. The honest comparison is on filters rather than price: `scrapemint` is the one competitor with a comparable, non-speculative feature list, and the code / minimum-value / role filters above exist because it had them and this Actor did not.

**What we do not claim:** a Store sweep checked live 2026-10-02 (2 search terms, 20 live listings priced) found `jweninger16/insider-trading-monitor` (3 users) on Apify's **FREE pricing model — $0/row at any volume**, genuinely cheaper than this Actor at every row count. Its own listing describes structured per-trade output (who traded, shares, price, post-trade position) comparable in shape to this Actor's, so it is a real rival, not a shallow clone — we have not inspected its actual output fields closely enough to know whether it decodes all 20 transaction codes, signs `transactionValueUsd`, or normalizes the 10b5-1 flag's four spellings the way this Actor does. No per-row price can beat $0; the differentiator here stays data fidelity (code decoding, signed value, normalized plan flag, EDGAR pagination past the ~12-month inlined window) rather than price. Also newly priced and disclosed for completeness, all dearer than us: `entrepreneurial_lens_ehi/openinsider-scraper` (3 users, tiered $0.0038 FREE down to $0.00171 GOLD+ — undercuts us only from GOLD+ and up, but scrapes openinsider.com's own generic Title/Url/Description fields rather than parsed EDGAR XML, so it is a narrower/shallower product despite the lower per-row ceiling), its dearer sibling-category listing `crawlerbros/open-insider-scraper` (12 users, 4 new/30d, same openinsider.com source, $0.005 start + tiered $0.005 FREE down to $0.003 GOLD+ — dearer than us and than `entrepreneurial_lens_ehi` at every tier), `pink_comic/sec-insider-trading-tracker` (3 users, $0.002/row), `bb-tradetec/sec-form4-transaction-normalizer` (2 users, $0.002/row), `great_pistachio/sec-filings-monitor` (2 users, $0.01/row), `gochujang/insider-trading-tracker` (2 users, $0.002/row), `straightforward_hydra/sec-form4-insider-trading-monitor` (2 users, $0.005/row), `neuton/sec-form4-insider-transactions-scraper` (2 users, $0.004/row), `nexgendata/sec-edgar-filings-api` (13 users, re-verified 2026-10-03 — was two listings at 2 users each in an earlier audit, now one at 13; its own marketing covers "Form 4 insider trades, 8-K, 13F... and 20+ more" but the live pricing's only charge event is literally named `form-d-filing` at $0.05, so Form D is what you're actually billed under regardless of which filing type you pick), `andrew_avina/sec-insider-mcp` (2 users, $0.003/row). None of these beat our price; only `jweninger16` and `entrepreneurial_lens_ehi` (partially) do.

A 7-term niche sweep checked live 2026-10-03 also surfaced `saswave/advanced-finviz-scraper` (17 users, $0.001/row flat — genuinely cheaper than us) for the first time. It is not a competing product: it is a general Finviz.com page scraper ("collect data from public listed companies... for easier analysis and insider trade / news monitoring") where insider-trade data is one scrapeable Finviz page among several, sourced from Finviz's own secondary display rather than parsed EDGAR XML — no transaction-code decoding, no signed USD value, no 10b5-1 flag. Noted for completeness, not folded into the "beats us on price" list above since it is not a Form-4 specialist.

## Notes on the source

- Form 3 is an **initial** statement of holdings and Form 5 an annual catch-up. A Form 3 never
  contains a transaction element at all (verified across Apple's four most recent Form 3s: 0
  transactions, 1–2 non-derivative and 2–7 derivative holdings each), so with the default
  `includeHoldings: false` a Form-3-only run yields **zero rows** — turn `includeHoldings` on to
  get those positions. Form 5 does carry real transactions.
- A filing can be made jointly by several reporting persons. The first is used for the
  `insiderName`/role fields and the rest are listed in `coFilers` rather than dropped.
- SEC's filing index is newest-first, so `sinceDate` stops paging as soon as it passes the date.
- **`sinceDate` reaches past EDGAR's inlined filing window, which matters for prolific filers.**
  EDGAR's per-issuer submissions file inlines only the larger of ~1000 filings or the trailing
  12 months; everything older lives in separate paginated index pages. For a heavy filer that
  window is shallow in *time* — JPMorgan carries ~26,000 filings in it spanning just one year —
  so reading only the inlined window would answer `sinceDate: "2024-01-01"` with nothing before
  late 2025 and no indication anything was missing. This Actor follows the older index pages,
  skipping any page whose date range ends before `sinceDate` without fetching it, up to 30 pages
  per issuer (it logs a warning naming the oldest date actually reached if it hits that ceiling).
  Measured on JPMorgan Form 4s with `sinceDate: "2024-01-01", maxFilingsPerIssuer: 200`: the
  inlined window alone yields 134 filings and stops there; following the older pages reaches the
  full 200 requested after 8 of them. Peak memory for that run was 92 MB.
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
