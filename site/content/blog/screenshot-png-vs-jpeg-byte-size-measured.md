---
title: PNG to JPEG saved 15-63% on a full-page screenshot, depending on the page. Cropping beat both.
description: We priced a screenshot Actor by measuring it twice, on a text page and a photo page, and the format switch everyone recommends turned out to be real but wildly page-dependent — and still the weaker lever either way.
date: 2026-10-16
tags: webscraping, api, javascript, dataengineering
tool: website-screenshot-scraper
---

The standard advice for headless-browser screenshots is "default to JPEG, not PNG — it's 5-10x smaller." We wrote that rule into our own build notes while costing out a screenshot Actor, on the strength of two measurements. Then we measured it properly on a text-heavy page and it mostly evaporated — 15%, not 5-10x. So we measured it again on a photo-heavy page, to find out whether 15% was the real number or just a bad page to test on.

## The setup

Two URLs, same Actor, same settings (1024 MB, single run each), captured three ways — full-page PNG, full-page JPEG q80, viewport-only JPEG q80:

```
$ # full-page PNG, full-page JPEG q80, viewport-only JPEG q80
$ curl -s -X POST "https://api.apify.com/v2/acts/<actor>/run-sync-get-dataset-items?memory=1024" \
    -H 'Content-Type: application/json' \
    -d '{"urls":["<page>"],"format":"png","fullPage":true}'
```

`byteSize` comes off the output row. The cost lines come off the run record's own `usageUsd` object, not from a pricing page.

**Text-heavy page** — `en.wikipedia.org/wiki/Web_scraping`, a long article, black text on flat white:

| capture | `byteSize` | vs. full-page PNG | compute units | total billed |
|---|---|---|---|---|
| full-page PNG | 2,408,123 | — | 0.001289 | $0.000318 |
| full-page JPEG q80 | 2,040,985 | **-15%** | 0.000746 | $0.000204 |
| viewport JPEG q80 | 274,046 | **-89%** | 0.001111 | $0.000275 |

**Photo-heavy page** — `en.wikipedia.org/wiki/Wikipedia:Featured_pictures`, a gallery of large photographs stacked down the page:

| capture | `byteSize` | vs. full-page PNG | compute units | total billed |
|---|---|---|---|---|
| full-page PNG | 1,954,342 | — | 0.001406 | $0.000487 |
| full-page JPEG q80 | 724,581 | **-63% (2.7x)** | 0.001109 | $0.000367 |
| viewport JPEG q80 | 189,873 | **-90%** | 0.006127 | $0.000613 |

## The format switch is real, but the size of it is page-dependent

Fifteen percent on the text page. Sixty-three percent on the photo page. Same Actor, same quality setting, a 4x difference in how much the format switch is worth — which answers the question the first measurement left open: was 15% a property of JPEG-vs-PNG, or a property of that one page? It's the page.

The mechanism is the same one we guessed at the first time, now confirmed by varying the one thing that should matter: a Wikipedia article is close to PNG's best case and close to JPEG's worst — black text on large flat regions, exactly what PNG's filtering and run-length compression are built for, while JPEG q80 spends bits putting faint ringing noise *into* those flat areas. A gallery of photographs is the opposite case on both counts, and the saving swings from "barely worth it" to "worth more than half the file."

**Cropping still wins either way.** `fullPage: false` cut the text page 89% and the photo page 90% off the PNG baseline — both comfortably bigger than the best-case format saving. If you only need the top of the page, crop first; the format only matters for what's left after that.

So the honest, now-evidence-based version of the advice is: **pick your crop first, your format second, and expect JPEG's win to range roughly 15-65%+ depending on how photo-heavy the page is** — real savings, just not a fixed number, and smaller than cropping in both cases we've measured.

## What the run record says about where the money goes

Two things in the billing lines surprised us, and the second one has now shown up twice.

**The image's bytes are not billed as egress when you capture them.** A run that produced a 2.41 MB PNG recorded `DATA_TRANSFER_EXTERNAL_GBYTES: 5.31e-06` — about 5.3 KB, roughly 0.2% of the image. The screenshot goes into the key-value store, which bills per *write* ($0.00005 on this run), not per byte; the bytes only leave the platform later, when something actually fetches the image URL. At our plan's live rates (`ACTOR_COMPUTE_UNITS` $0.2/CU, `DATA_TRANSFER_EXTERNAL_GBYTES` $0.2/GB, both read from the API rather than assumed), compute was 81% of that PNG run's total. We had budgeted for the opposite — for big images to be expensive at capture time. They're expensive at *download* time, which is a different line item on a different day.

**Compute units don't track output size, on either page.** On the text page, the viewport capture produced 7.4x fewer bytes than the full-page JPEG and still billed more compute (0.001111 vs 0.000746 CU). On the photo page it was starker: 3.8x fewer bytes, 5.5x *more* compute (0.006127 vs 0.001109 CU). Two unrelated pages, same direction both times — CU tracks how long the page took to load and settle, which depends on network conditions and image-decode time, not on what you crop or compress afterward. If you're trying to predict an Actor's compute cost from its output size, you're reading the wrong column.

## Packaged version

[website-screenshot-scraper](/tools/website-screenshot-scraper) captures any public URL as JPEG, PNG or PDF with `fullPage`, `selector`, device presets and a 1200x630 Open Graph card mode, and returns `byteSize` on every row so you can see this tradeoff on your own pages instead of taking ours. Failed URLs come back as an error row and aren't charged. It's also on the Apify Store as [website-screenshot-scraper](/go/website-screenshot-scraper).

If you're deciding whether you need a browser for a scraping job at all, the cheaper question comes first: we [timed HTTP-only extraction against headless Chromium on the same page](/blog/http-only-vs-headless-browser-scraping-cost) and it wasn't close. Screenshots are one of the few jobs where the browser isn't optional.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every byte count, compute-unit figure and billing line above comes from live runs and live API reads made while writing this post, not from documentation.*
