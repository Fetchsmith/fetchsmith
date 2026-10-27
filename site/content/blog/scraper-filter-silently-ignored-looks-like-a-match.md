---
title: Your scraper's filter did nothing, and the run looked perfect
description: An input key that is valid for an Actor but out of scope for the mode you picked gets accepted, dropped, and never mentioned. The run exits 0 with a clean-looking row count, and that count is indistinguishable from "everything matched" — found live on our own Apple Podcasts Actor, fixed, then swept across the fleet.
date: 2026-10-24
tags: webscraping, api, dataengineering, javascript
---

A scraper with a mode switch — `dataType`, `chartType`, `scrapeType`, whatever you call it — almost always has input fields that only make sense in *some* of those modes. [Apple Podcasts](/tools/apple-podcasts-scraper)'s Actor is a clean example: set `dataType` to `reviews` and you get `keyword`, `minRating`, `maxRating`, `sort`; set it to `episodes` and you get `minDurationSeconds`, `explicitFilter`, a release-date window. Both sets live in the same `input_schema.json`, because the Actor handles both modes. That's normal, and it's also exactly the shape that produces this bug.

## The run that filtered nothing and said nothing

We passed `keyword: "AI"` alongside `dataType: "episodes"`. `keyword` is a reviews-only field — the schema's own description says "Reviews only" — so the episodes code path never reads it. The run came back with episodes, `0` errors, a normal row count, and **no warning**. Nothing in the log told us the filter had been ignored.

That silence is the expensive failure mode, not a cosmetic one. This Actor is pay-per-result: a buyer who sets `keyword` expecting episode titles filtered down to "AI" gets back every episode, pays for all of them, and has no way to tell "the filter ran and nothing matched" apart from "the filter never ran." Both look like a row count. Only one of them is what was promised.

The frustrating part is that the fix pattern already existed *in the same file*, just not applied consistently. This Actor already warns when other out-of-scope inputs are used — `chartType` outside chart mode, `chartGenre` on the episode chart, `watchLabel` outside episode mode all get an explicit `log.warning(...)`. Four inputs were covered. Eight more — the entire reviews/episodes filter split — were not. It wasn't a missing feature, it was a coverage gap in a convention that was already half-applied.

## The fix is one symmetric block, not eight scattered checks

Rather than add a warning next to each filter, we added one block right after the input parse that checks both directions at once:

```js
const reviewOnlyIgnored = ['keyword', 'minRating', 'maxRating', 'sort']
  .filter((k) => input[k] !== undefined);
if (dataType !== 'reviews' && reviewOnlyIgnored.length) {
  log.warning(`${reviewOnlyIgnored.join(', ')} only applies to dataType "reviews" — ` +
    `ignored for dataType "${dataType}", so nothing was filtered out by it.`);
}

const episodeOnlyIgnored = ['minDurationSeconds', 'explicitFilter', 'minReleaseDate', 'maxReleaseDate']
  .filter((k) => input[k] !== undefined);
if (dataType !== 'episodes' && dataType !== 'charts' && episodeOnlyIgnored.length) {
  log.warning(`${episodeOnlyIgnored.join(', ')} only applies to dataType "episodes" (and "charts") — ` +
    `ignored for dataType "${dataType}", so nothing was filtered out by it.`);
}
```

Each message names the exact keys that were ignored, says which mode they apply to, and states the consequence in words a non-engineer buyer reading a run log will understand: *nothing was filtered out by it*. We verified it firing live — a follow-up run with `minDurationSeconds` and `maxReleaseDate` set under `dataType: "reviews"` logged exactly that sentence, with both field names in the message.

## A near-miss that looked like the same bug and wasn't

The same test pass set `minDurationSeconds: 7200` under `dataType: "episodes"` and got back rows where 3 of 5 had `durationMs: null` — kept, not dropped, even though the filter was supposedly in scope this time. That looks like the identical bug from the other side: a filter silently not applying.

It wasn't. Apple's own episode data omits duration for roughly half of all episodes, independent of how long they actually run, so treating a missing duration as "too short" would silently drop real episodes that happen to lack metadata — a worse failure than keeping them. The Actor already documents this and already announces it per-run with an exact count: `3 episode(s) had no duration in Apple's own data and were kept rather than dropped`. Read the source before filing a defect that already has a deliberate, disclosed answer; a filter that correctly declines to drop ambiguous rows is not the same bug as a filter that silently never ran at all.

## The general rule

A filter key that is *valid* for an Actor but *out of scope* for the mode you selected is worse than a key the schema rejects outright, because the schema itself blessed it — there's no validation error to notice. Apify already handles the other half of this for you: an *undeclared* key is simply dropped with no error, which is the reason tools like our internal `varied-test` harness pre-flight every test input against `input_schema.json` before running it. Declared-but-wrong-mode keys get no such safety net; the schema says they're fine, and "fine" is not the same as "used."

The rule that falls out of it: **a filter that cannot run in the current mode must say so**, because silence reads to a buyer as "it ran and everything matched" — the one outcome a pay-per-result Actor cannot afford to produce by accident.

[ClinicalTrials.gov](/tools/clinicaltrials-scraper)'s filter set doesn't have this trap — every one of its filters is active regardless of other inputs chosen, so there's no mode split for a key to fall outside of. That's worth noting on its own: the bug isn't inherent to having filters, it's inherent to having a mode switch with filters that don't apply uniformly across every mode.

The warning block described above is live in [the Apple Podcasts Actor](/go/apple-podcasts-scraper); [the ClinicalTrials.gov Actor](/go/clinicaltrials-scraper) is the no-mode-split counter-example. Both run on Apify with a $0 flat run fee and per-result pricing, no API key required from you. ([Our full Apify catalogue](/go-store) for the rest; fields and sample output per Actor are on [our own tool pages](/tools).)

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every log line and field name above comes from a live run made while writing this post, not from documentation.*
