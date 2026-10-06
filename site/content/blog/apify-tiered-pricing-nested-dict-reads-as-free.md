---
title: "A rival's price was nested two dicts deep — and the obvious min() read 20 competitors as free"
description: Apify's Store API reports a PAY_PER_EVENT Actor's tiered price as {TIER: {tieredEventPriceUsd: x}}, not a flat number. The natural "take the minimum" parser drops every tier as a non-number and reports no price at all — which, under the reasonable rule that no price means free, turns 20 of 60 real competitors into phantom free listings.
date: 2026-10-06
tags: webscraping, api, javascript, dataengineering
---

We price-audit our own Apify Actors against every competing listing in their niche, on a standing rotation — live, via Apify's own Store API, not by reading marketing copy. Writing a fresh batch pricer for one niche's 60 unnamed rivals, the first version collected a candidate price per listing like this:

```js
const candidates = [ev.eventPriceUsd, ...Object.values(ev.eventTieredPricingUsd || {})]
  .filter(v => typeof v === 'number');
const price = candidates.length ? Math.min(...candidates) : null;
```

That reads as correct: take the flat price if there is one, take every tier price if there isn't, keep the cheapest. It compiled, it ran, and it quietly threw away a third of the dataset.

## What `eventTieredPricingUsd` actually looks like

Here is one real rival's charge event, fetched live from `GET /v2/acts/<owner>~<name>`, un-edited:

```json
{
  "apify-default-dataset-item": {
    "eventTitle": "Insider transaction",
    "isOneTimeEvent": false,
    "eventTieredPricingUsd": {
      "FREE":     { "tieredEventPriceUsd": 0.003 },
      "BRONZE":   { "tieredEventPriceUsd": 0.0015 },
      "SILVER":   { "tieredEventPriceUsd": 0.0014 },
      "GOLD":     { "tieredEventPriceUsd": 0.0012 },
      "PLATINUM": { "tieredEventPriceUsd": 0.0012 },
      "DIAMOND":  { "tieredEventPriceUsd": 0.0012 }
    },
    "isPrimaryEvent": true
  }
}
```

`Object.values(eventTieredPricingUsd)` is not `[0.003, 0.0015, 0.0014, 0.0012, 0.0012, 0.0012]`. It is six objects — `{"tieredEventPriceUsd": 0.003}` and so on. The real number lives one level further in, at `tier.tieredEventPriceUsd`. A plain `typeof v === 'number'` filter correctly rejects every one of those six objects, `candidates` ends up empty, and the listing comes back with **no priced event found.**

In a flat-rate `eventPriceUsd` world this bug can't happen — there's nothing nested to miss. It only shows up the moment a rival is on Apify's rental-plan tiered pricing, which is exactly the pricing shape a well-run, actively-sold Actor tends to land on.

## Why "no price found" is the dangerous failure, not an error

The parser didn't crash. It returned a clean `null`, and `null` is a value every downstream step already knows how to handle: our standing rule, correct for most of the Apify Store, is that an Actor with no priced event listed is free — not every Actor charges, and `pricingModel: "FREE"` genuinely means `$0` at any volume. So `null` flowed straight into "this is a free competitor" with no exception raised anywhere.

Of the 60 unnamed listings in that one sweep, **20 came back as "no priced event."** All 20 were real `PAY_PER_EVENT` Actors with real tiered prices; none were actually free. Three of the cycle's five genuine findings — including the closest feature-for-feature rival in the whole niche — were sitting inside that silently-broken 20, about to be published as three new *free* substitutes for a paid product. The bug wasn't a crash to debug. It was a quiet, confident, wrong answer that happened to point at the three most important rows in the dataset.

## The one-line fix, and the check that makes it durable

```js
function tierPrices(ev) {
  const t = ev.eventTieredPricingUsd;
  if (!t) return [];
  return Object.values(t).map(tier => tier.tieredEventPriceUsd);
}
```

Read the tier object's own field name, don't assume `Object.values` already gives you numbers. The durable version of the fix isn't the one-liner, though — it's a reusable classifier with three outcomes instead of two:

```js
function priceStatus(data) {
  const pi = data.pricingInfos?.at(-1);
  if (!pi || pi.pricingModel === 'FREE') return { status: 'free' };
  const events = pi.pricingPerEvent?.actorChargeEvents || {};
  const prices = Object.values(events).flatMap(ev =>
    [ev.eventPriceUsd, ...tierPrices(ev)].filter(v => typeof v === 'number'));
  if (!prices.length) return { status: 'PARSE_FAILURE', raw: events };  // inspect by hand
  return { status: 'priced', min: Math.min(...prices) };
}
```

`pricingModel !== 'FREE'` but zero numeric prices extracted is never a legitimate state for a `PAY_PER_EVENT` Actor — Apify requires at least one priced event for that model. Treat it as `PARSE_FAILURE`, log the raw event object, and look at it by hand. That third bucket is what turns a silent miscount into a loud one: in the fixed version, those same 20 listings don't disappear into "free," they stop the batch and print their raw JSON, which is how the nested-dict shape above got noticed at all.

## The mirror bug: the *cheapest-looking* line isn't always the real price

The same niche had a second, opposite trap. One rival's cheapest-looking charge event:

```json
"apify-default-dataset-item": { "eventPriceUsd": 0.00001, "isPrimaryEvent": null }
```

A dataset-row price of $0.00001 ranks as the cheapest listing in the niche by roughly 180×, if "cheapest" means "take the minimum across every event." But the same listing's full event set, fetched live, is:

```json
"company-scan":        { "eventPriceUsd": 0.015,  "isPrimaryEvent": true },
"apify-actor-start":   { "eventPriceUsd": 0.005 },
"apify-default-dataset-item": { "eventPriceUsd": 0.00001, "isPrimaryEvent": null }
```

`company-scan` is `isPrimaryEvent: true` — Apify's own field for "this is the event the owner intends to be read as this Actor's real price." Every row it ever pushes to the dataset is billed at a near-zero nominal rate; the actual charge is per *company scanned*, not per row, at $0.015 plus a $0.005 start fee. A `min()`-over-events sweep ranks this listing as the cheapest in its class. Reading `isPrimaryEvent` instead puts it near the dearest.

The two bugs are mirror images of the same mistake — picking a number out of the pricing JSON without checking what the number is actually attached to — and the fix for both is the same discipline: read the schema's own signal (`isPrimaryEvent`, the tier object's real key) before reducing a set of prices to one.

Neither of these is a comparison between *our* price and a rival's — both are about getting a rival's *own* real price right before comparing anything. If their unit doesn't match yours (per-company vs. per-row, here), the honest output isn't "cheaper" or "dearer," it's the crossover point: at $0.015/company flat against $0.0018/row, that rival only wins above roughly 11 transactions per company. Publishing the crossover number lets a buyer check it themselves; publishing a verdict just asks them to trust you.

## If you're pulling Apify's pricing API yourself

- `GET /v2/acts/<owner>~<name>` → `data.pricingInfos` is an **array**, ordered oldest→newest; take the last entry (`.at(-1)`) for the current price, not the first.
- A flat-rate event has `eventPriceUsd` as a plain number. A tiered event has `eventTieredPricingUsd: {TIER: {tieredEventPriceUsd: number}}` instead — one dict layer deeper than the flat case, on the *same* event object, distinguished only by which of the two keys is present.
- `isPrimaryEvent: true` marks the event the owner considers this Actor's real unit of sale. A generic `apify-default-dataset-item` row charge can coexist on the same Actor as a far more expensive primary event — the row charge isn't fake, it's just not the point.
- `pricingModel === 'FREE'` is the only state that legitimately means $0. A `PAY_PER_EVENT` Actor with zero extractable numeric prices is a parser bug in your own code, not a free competitor — assert on it rather than letting it fall through to `null`.

We write these up as we find them, mostly from auditing Apify's SEC-filing, government-contract and job-board niches against our own [sec-insider-trades-scraper](/tools/sec-insider-trades-scraper) and its siblings — the same per-tier price table shows up on [fec-campaign-finance-scraper](/tools/fec-campaign-finance-scraper)'s and [us-federal-awards-scraper](/tools/us-federal-awards-scraper)'s competitor sections too, for anyone who wants to see it compiled rather than described.

More API deep-dives at [fetchsmith.com/blog](/blog).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every JSON shape and price above comes from a live request to Apify's own API made while writing this post, not from documentation.*
