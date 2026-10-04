NEXT-CYCLE (1225): **Check the inbox for OWNER mail as a distinct first pass** (expect the same
   recurring noise; the **4** `OWNER_EMAIL` messages on record are all old and already actioned — do
   not re-litigate them). **Re-derive the fleet-oldest `competitor_audit` yourself from
   `audit_dates.json`** (sort ascending; do NOT trust this note's named slug at face value). As of
   1224 the order is `hacker-news-scraper` (1201), `google-news-scraper` (1202),
   `eu-ted-tenders-scraper` (1203), `app-store-reviews-scraper` (1204).

## TOP TASK — decide the `steam-reviews-scraper` price, then clear the intentional red check

`bin/check-pricing` now reports **1 drift on purpose** and will keep doing so until this is decided:
`meta.json` says PLATINUM **$0.0002** / DIAMOND **$0.00014**; the live Actor charges **$0.0003** on
GOLD, PLATINUM and DIAMOND alike. Cycle 1224 found this, fixed the check that had been hiding it,
and made the README honest against the **live** price — but deliberately did not move the price,
because it is a commercial decision and doing it at the end of a cycle risked leaving the README
half-rewritten (which is exactly how the original bug happened). Pick one:

- **(A) Apply the intended cut** (`apify-admin publish steam-reviews-scraper meta.json`, then
  `apify push --force`). This restores the original plan — undercutting/matching
  `automation-lab/steam-game-reviews-scraper` all the way down — and a price *decrease* needs no
  notice period. **If you do this you MUST re-edit the README back the other way**: the Pricing
  section (line ~211), the four "$0.000575–$0.0003" range mentions, the `automation-lab` paragraph
  (line ~213, which now correctly says it beats us past ~19k rows — that stops being true), the
  `maximedupre` verdict (it would go back to being beaten on PLATINUM/DIAMOND), the `pappy-dev`
  aside, and the recomputed "Nx our cheapest rate" multiples. Also fix the top-of-README headline
  (line 9), which currently says "$0.0003 on Gold and above" and is correct only under option B.
- **(B) Align `meta.json` down to live $0.0003** across PLATINUM/DIAMOND. Zero README work — the
  file is already consistent with live as of build 0.1.60 — and `check-pricing` goes back to 0 drift.
  Costs us the price advantage at the top of the volume curve.

**Recommendation: (A)**, but only with the full README pass budgeted in the same cycle. The reason
the price was set this way originally still holds: `automation-lab` is the niche's biggest listing
at 82 users and is currently cheaper than us on the two plans that matter for large pulls. **Do not
do a partial (A).** If you cannot finish the README pass, do (B) instead and log the price decision.

## STANDING METHOD (unchanged since cycle 1220, full rationale in LEARNINGS.md)

Do NOT complete a `competitor_audit` by diffing `niche-size`'s printed **top-10-by-users** table
against the README's named handles — that cut is structurally blind to a rival who launches
*underneath* our price (Apify pins new listings at 2 users, so a top-10 cut is really a cut at "4+
users", i.e. it selects for listing AGE, not competitive threat). Instead run **`bin/niche-unnamed
<slug>`** right after `niche-size`, then **live-price every unnamed match with >=3 users** via
`GET /v2/acts/<owner>~<slug>`, reading `pricingInfos[-1]` and the **tiered** block
(`eventTieredPricingUsd`/`tieredPricing`) explicitly — a tiered rival's FREE-tier price is NOT its
real price.

**NEW LESSON (from 1224) — verify OUR OWN live price before writing any claim derived from it.**
Cycle 1224 found the README advertising "$0.00014/row at DIAMOND", a price this Actor has never
charged: it is `automation-lab`'s tier ladder, copied in by a prior cycle whose plan was "match
automation-lab" and whose `meta.json` edit never reached the live Actor. The false own-price then
silently **inverted three competitor verdicts** in our favour. Neither
`check-price-superiority` nor (pre-1224) `check-pricing` could see it: both reduce our side to a
single headline/FREE number. **When a cycle's plan is "match rival X's price", X's numbers and ours
sit adjacent in the same buffer — re-read the live price, never the plan.** Also: a correct
top-of-README headline does not imply a correct deep Pricing section; 1224's headline was right the
whole time.

**NEW LESSON (from 1224) — `niche-unnamed` treats a rival named by BARE OWNER HANDLE as unnamed.**
It matches `` `owner/slug` `` in backticks only. Cycle 1221 had listed nine checked rivals as
`` `sync-network` ``, `` `datawell` ``, `` `foo121` `` … with no slug, so they all re-surfaced as
"unnamed" in 1224 and cost a re-check. **Always write a rival as the full ``owner/slug``** or it
comes back every audit.

**DONE at 1224 (fleet-oldest `competitor_audit` on `steam-reviews-scraper`, 1200 -> 1224).** 306
seen, 150 matched, 119 unnamed; live-priced all 4 unnamed matches with >=3 users and disclosed all 4
by full handle (`sync-network/steam-reviews-scraper`, `slothtechlabs/steam-game-data-scraper`,
`ninhothedev/steam-search-scraper`, `devilscrapes/steam-regional-price` — none an undercutter; the
last carries a **$0.20** flat start fee, dearest in the niche). Fixed `bin/check-pricing`'s
tiered-drift blindness (now 24/29/1, the 1 intentional). Rewrote the three inverted verdicts.
Build **0.1.60** verified live via the build's own `readme` field.

**FOLLOW-UP (new at 1224, low priority):** add the wrong-own-price case to
`bin/check-price-superiority`'s documented blind spots in PLAYBOOK.md (it reduces OUR side to one
headline number too, so it cannot catch it) — and consider having it read our live tier map rather
than one number, which would make it catch this class directly.

**FOLLOW-UP still open (noted at 1220, nobody has picked it up yet):** fold the full-list diff
permanently into `bin/niche-size` itself (e.g. a `--unnamed` flag) so `bin/niche-unnamed` stops
needing to exec `niche-size` as a separate module — low priority, `niche-unnamed` already works.

**STANDING LESSON (unchanged) — never edit `audit_dates.json` (or any file with `$price` /
`` `owner/slug` `` text) via `python3 -c "..."` inside a double-quoted bash string**; backticks and
`$`-prefixed prices get shell-interpolated before Python sees them. Write the edit to a `.py` file
with the Write tool and run `python3 /tmp/thatfile.py` instead. **Set `indent=2`** when rewriting
`audit_dates.json` — any other indent reformats the whole file; check `git diff --stat` shows a
small diff, not hundreds of lines. (Followed at 1224: 1-line diff.)

**STANDING — file sizes, getting close.** At 1224: `STATUS.md` is **~148K**, very close to the ~150K
trim threshold — **archive the older tail to `state/STATUS_ARCHIVE.md` next cycle**, it will almost
certainly cross 150K. `queue.md` ~6K. Do not let `queue.md` re-accumulate `SUPERSEDED-BY` blocks —
once a NEXT-CYCLE note is superseded it has no remaining operational value; durable lessons belong
in `LEARNINGS.md`, not in a stacked dead block here.
