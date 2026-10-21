---
title: A federal-awards watch mode that alerts on changes — unless you filtered on the field that changed
description: "Filtering a watch on minAwardAmount/maxAwardAmount or expiringWithinDays silently hides the exact change you're watching for. Measured live today: award 70T05026F5900N033 ($958,748.70) matches maxAwardAmount=1,000,000 and vanishes under maxAwardAmount=900,000 — so a watch bounded at $900k would never see that same award's amount grow into the gap."
date: 2026-10-20
tags: webscraping, api, procurement, opendata
tool: us-federal-awards-scraper
---

`us-federal-awards-scraper`'s watch mode (`watchLabel` + `watchChanges`) re-delivers an award you've already seen if USAspending's own `lastModifiedDate` moved, or if `awardAmount`/`totalOutlays`, `loanValue`/`subsidyCost`, or the period-of-performance `endDate` differ from the snapshot it stored last time. The README already names a trap: filtering on a field you're also watching for changes hides the change, because the filter decides which awards come back *before* the comparison runs. Re-measured both halves of that claim live today against the real USAspending API — no Apify spend, the same public `spending_by_award` endpoint the Actor itself calls.

## The amount filter hides exactly the direction you'd want to know about

Award `70T05026F5900N033` — Award Amount $958,748.70 — comes back from USAspending's live search right now:

```
award_amounts: none                    -> 1 result (958748.7)
award_amounts: {upper_bound: 1000000}  -> 1 result (958748.7)
award_amounts: {upper_bound: 900000}   -> 0 results
```

Both bounded queries hit `api.usaspending.gov/api/v2/search/spending_by_award/` directly, today, with every other filter held identical. `maxAwardAmount: 900000` makes the award disappear entirely — not flagged, not returned-with-a-note, just absent, same as if it had never existed.

Now put that inside a running watch. Say a buyer sets `maxAwardAmount: 900000` on a `watchLabel` to keep a saved search cheap and focused on sub-$900k awards, and `watchChanges: true` because they also want to hear about amount changes. The Actor's own `award_amounts` filter is sent to USAspending as the server-side bound on the *same* `Award Amount` field `watchChanges` is diffing. If this award had been $880,000 at baseline time and a contract modification bumped it to $958,748.70, the run wouldn't report an amount increase — it would report nothing, because the now-$958,748.70 award no longer matches `maxAwardAmount: 900000` and never reaches the comparison step at all. A lower bound has the same problem in the other direction: it hides de-obligations and descopes, the awards getting *smaller*. Either bound only has visibility into amount changes that stay inside the window the whole time — the boring case, not the one anyone sets up a watch to catch.

## The same shape, on the end date

`expiringWithinDays` filters on `endDate` — the period-of-performance end date — which is also one of the six fields `watchChanges` diffs. A live contract sitting in that window right now:

```
Award 123J1426F1541 — ASSOCIATED MILK PRODUCERS INC — Department of Agriculture
End Date: 2026-10-31  (11 days from today, 2026-10-20)
```

Fetched live from `spending_by_award` with no amount filter beyond the Actor's own default window. Set `expiringWithinDays: 30` and this award is in scope today. If the next scheduled run happens after a contract modification extends that end date past day 30 — the exact kind of change a "tell me when something I'm tracking gets extended" watch exists to catch — the award drops out of the `expiringWithinDays` window *before* `watchChanges` ever compares old-`endDate` to new-`endDate`. The run reports nothing, because as far as the filter is concerned the award simply stopped matching, which looks identical to "nothing changed."

## Why this is easy to miss

Both traps share one shape: the filter and the watched field are the same field, so narrowing your search and blinding your watch are the same action. Nothing about the request looks wrong — `maxAwardAmount`/`expiringWithinDays` are documented, ordinary filters, and a narrower watch *feels* like the responsible choice (cheaper runs, a tighter saved search). The run still exits 0, still returns real rows for whatever currently matches, and gives no indication that an award you used to track just aged out of visibility rather than staying flat.

## What this Actor does about it

`us-federal-awards-scraper` detects the overlap itself: setting `minAwardAmount`/`maxAwardAmount` or `expiringWithinDays`/`expiringAfterDays` alongside `watchChanges` adds the affected field(s) to a `watchChangeBlindFilters` list, logged as a named warning and included in the run's status message and `webhookUrl` payload — so the blind spot is stated up front rather than discovered later as a report that never arrived. The fix is two labels: a narrow one with the filter, for finding new awards, and a second, wider one with `watchChanges` and no filter on the field you care about, filtering the delivered rows on your own side instead of USAspending's.

## Packaged version

[us-federal-awards-scraper on Apify](/go/us-federal-awards-scraper) covers all six USAspending award categories (contracts, IDVs, grants, loans, direct payments, other financial assistance) plus FSRS sub-awards, with `watchLabel`/`watchChanges` built in and `watchChangeBlindFilters` surfaced on every run that could otherwise go quiet without saying so. Sub-award mode had the mirror-image version of this failure on our own side of the wire — [a reused `Sub-Award ID` collapsing real filings in the dedup key](/blog/subaward-id-reuse-was-silently-dropping-rows), 18 dropped rows out of 500 measured — which is why every drop the Actor makes on purpose now gets named in the run summary.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every number above comes from a live request made while writing this post, not from documentation.*
