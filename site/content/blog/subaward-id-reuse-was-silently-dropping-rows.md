---
title: "A government ID that isn't unique: USAspending reuses sub-award numbers across different filings"
description: FSRS re-files a contract modification under the same Sub-Award ID as the original, and rarely reuses one under a different sub-awardee entirely. Keying on the ID alone silently dropped real rows. Live-measured on 500 sub-awards, reproduced, and fixed.
date: 2026-10-20
tags: webscraping, api, opendata, govtech
tool: us-federal-awards-scraper
---

Our [federal awards scraper](/tools/us-federal-awards-scraper) can pull sub-awards — the sub-contracts and sub-grants reported under a prime federal award — straight from USAspending's FSRS data. The field that looks like the obvious row identity, `Sub-Award ID`, isn't one. It gets reused across genuinely different filings, and for a while this Actor's own dedup logic trusted it anyway, silently collapsing real rows into one.

## The data: how often does a Sub-Award ID repeat

We pulled 500 live sub-award rows for one DOE prime contract (`89233018CNR000004`, Fluor Marine Propulsion) directly from USAspending's public API, same filters and fields this Actor sends:

```
500 rows fetched
480 distinct Sub-Award IDs   (20 rows sit on an ID another row already used)
482 distinct full-identity keys (ID + date + amount + sub-awardee name)
```

Two different things are hiding inside those 20 collisions. **18 are real, distinct filings** — most often a later contract modification re-filed under the same `Sub-Award ID` as the original, with a new date and a different dollar amount:

```
id 204338: 2026-05-05  $5,306,000.00  MASCARO CONSTRUCTION CO LP   (original)
id 204338: 2026-05-22  $5,306,000.00  MASCARO CONSTRUCTION CO LP   (re-filed under the same ID)
```

**2 are true duplicates** — the same filing resubmitted with a sub-cent rounding difference, which is why the real-identity key rounds the amount to the dollar before comparing:

```
id 203860: 2026-03-31  $223,331.80  BRUKER AXS LLC
id 203860: 2026-03-31  $223,332.00  BRUKER AXS LLC   (same filing, re-submitted)
```

Separately — confirmed earlier on two unrelated primes across DOE and HHS — FSRS has also, rarely, reused an ID/date/amount combination under a **different sub-awardee name entirely**: one row was the prime contractor's own name misfiled onto a sub-award record. That shape needs the sub-awardee name in the key too, or one of the two real entities silently disappears.

## The bug: an ID-only dedup key

This Actor dedupes every category it scans to avoid charging a buyer twice for the same row. For prime awards that's safe — USAspending's own `generated_internal_id` really is unique. Sub-awards don't carry an equivalent: before this fix, the key fell back to `Sub-Award ID` alone. That key is a per-prime-award sequence number FSRS assigns to a *sub-award line*, not to a *filing* — and a later amendment to that line reuses the original line's number rather than getting a new one.

Net effect: whichever of a genuine original/amendment pair USAspending happened to return second was silently discarded. The row didn't error, didn't warn, didn't show up truncated — it just wasn't there, indistinguishable from a sub-award that was never reported at all. On this one prime contract, that was 18 real filings out of 500.

## The fix

The dedup key is now the tuple `Sub-Award ID` + `Sub-Award Date` + `Sub-Award Amount` (rounded to the dollar, to absorb FSRS's own sub-cent resubmission noise) + `Sub-Awardee Name`:

```
sub:<id>:<Sub-Award Date>:<Math.round(Sub-Award Amount)>:<Sub-Awardee Name>
```

Two filings that genuinely share an ID but differ in date or amount are now kept as separate rows (the amendment case). Two filings identical in every field except a fraction of a cent collapse to one (the true-duplicate case). And the rare mismatched-name case keeps both entities rather than the old code arbitrarily preferring whichever arrived first.

We checked a second, unrelated prime award (an HHS/CMS contract) before shipping, specifically to rule out "Fluor's filings are just unusually messy" — the same reuse pattern showed up there too, on a different agency and a different award type, which is what made this a dedup-key bug rather than one contract's data quality problem.

## Why this matters even if you don't use this Actor

If you're pulling FSRS sub-award data directly from USAspending's API yourself, `Sub-Award ID` looks exactly like a primary key — it's an integer, it's stable, and most of the time it genuinely does identify one filing. It just isn't guaranteed to, and USAspending publishes no documentation saying so. A naive `Map` keyed on it will quietly merge an original and its amendment, and because the amendment isn't a new API-level record — it's the same ID with new field values — there's no error response or missing-row signal to notice. The only way to find this was pulling enough real rows and checking whether the ID actually behaved like a key.

## Packaged version

Live now on [us-federal-awards-scraper](/go/us-federal-awards-scraper); existing sub-award queries just return more complete results on their next run, no input changes required. See the [USAspending fields write-up](/blog/usaspending-federal-awards-json-api) for how prime-award fields map across award types, or [Sub-award mode](/tools/us-federal-awards-scraper#sub-award-mode) in the Actor's own README for the full field table.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned. Every number above came from a live API request made while writing this post.*
