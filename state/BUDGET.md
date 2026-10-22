# Budget ($300 total). Only spend against a line here.
| Item | Approved | Spent | Notes |
|---|---|---|---|
| Domain fetchsmith.com | $10 | $10 (owner) | Cloudflare |
| Apify plan base fee | $6 | $6 (owner) | CUSTOM/BRONZE, $1/mo base, billed TWICE_A_YEAR |
| Apify platform usage above included credits | $120 | ~$13.69 (measured, cycle 2104) | **$1/mo included credits only — see below** |
| Directory listings (paid) | $0 | — | not approved yet (no card) |
| Ads | $0 | — | not approved |

## Apify platform usage — corrected cycle 1640 (the "$500 allowance" was never real)

This file previously said the Apify plan came with **"$500 platform usage"**, and ~1500 cycles of
STATUS.md prose used that to report platform runs/builds as "$0 cash". The live API contradicts it:

- `GET /v2/users/me` → plan `CUSTOM`/`BRONZE`, `monthlyBasePriceUsd: 1`,
  **`monthlyUsageCreditsUsd: 1`**, `maxMonthlyUsageUsd: 85` (a hard *cap*, not an allowance),
  `isPaying: true`.
- Measured usage (`bin/apify-spend --prev`, cycle 1640):
  - billing cycle 2026-09-09..2026-10-08: **$12.23 used, $11.23 above the included credit**
  - billing cycle 2026-10-09..2026-11-08: $1.17 used at 13.7% elapsed → **~$8.6 projected**
- So real platform consumption to date is **~$13.40, of which ~$11.40 is above included credits**
  (not the "~$1.4 of $300" STATUS.md had been carrying). Still a small fraction of the $300
  envelope, but it is real money and it was being reported as zero.

### Re-measured cycle 2104 (the figure above is a FLOOR, not a lifetime total)

`bin/apify-spend` / `--prev` on 2026-10-22:

- completed cycle 2026-09-09..2026-10-08: **$12.2299 used, $11.2299 above credits** (final)
- current cycle 2026-10-09..2026-11-08 at 44.8% elapsed: **$3.4638 used, $2.4638 above
  credits**, cycle projection **$7.73** — i.e. the run-rate is *down* ~37% vs the prior
  cycle's $12.23, and is less than a third of the $25 stop-and-investigate trip-wire.
- Sum of those two = **$13.69 above credits**, which is what the table now carries.

**The API retains only the current and previous billing cycle**, so anything consumed before
2026-09-09 is unmeasurable from the server. Treat the Spent cell as a *floor*. Cycle 1640's
"~$11.40" was the same two-cycle window measured 464 cycles earlier, not a cumulative total —
do not read the two numbers as "+$2.29 of lifetime growth".

**Cost driver is Actor BUILDS, not runs** (in-window: builds 148 jobs/$0.72 vs runs 311
jobs/$0.21). Every `apify push` is a billable platform build at **~$0.0048** and we average ~36
builds/day across the 24 Actors. Compute units are 75% of all spend.

**Rules going forward:**
1. Quote `bin/apify-spend` for any spend statement. Never quote a credit/allowance figure from
   prose. There is no invoice endpoint (`/users/me/invoices`, `/billing-info` both 404), so this
   measures chargeable usage, not a confirmed card charge.
2. Treat a push as a **$0.005 purchase**: one push per Actor per cycle, batching code + README +
   `.actor/` metadata into that single build. Don't push to "verify" when the local diff is empty.
3. The $120 line above is carved out of the owner's existing $300 envelope (≈12 months of the
   current ~$9.6/mo run-rate). If `bin/apify-spend` ever projects a cycle above **$25**, stop and
   find the cause before pushing/running anything else — that is a 2.5x run-rate break, not drift.
