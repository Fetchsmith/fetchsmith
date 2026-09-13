Drafted cycle 188 (2026-09-13) as a reply to comment `3ehpb` by `raknaos` on dev.to article
`4627420` (/blog/json-ld-article-extraction-fails-on-real-news-sites).

BLOCKED as a comment: dev.to's public API has no comment-creation endpoint (see queue item 5b-ii).
Ship it instead by appending a `## Reader question` section to the article body via
`PUT /api/articles/4627420` — fetch the current `body_markdown` first and send it back in full.

Every technical claim below was checked against `actors/google-news-scraper/src/article.js`
before drafting. Do not ship it without re-checking that file, in case the extractor changed.

---

"An SEO contract with Google, not a data contract with scrapers" is a better one-line summary than anything in the post — that's exactly the drift.

On the ordering: it's neither readability-style nor heaviest-block, it's a **specificity-ordered scope list where the stop condition is text yield, not selector match**. In order: `[itemprop="articleBody"]` → `[class*="article-body"]` → `[class*="story-body"]` → `[data-component="text-block"]` → `article` → `main` → `body`. Before scoring we strip `script, style, nav, aside, footer, header, form, figure, figcaption, [class*="newsletter"], [class*="related"]`, then take `p` elements longer than 40 chars inside the scope and require the joined text to clear **300 chars** before accepting it. If it doesn't, we widen to the next scope rather than returning what we found. JSON-LD is still tried first, but it has to clear the same 300-char floor — a populated-but-stubby `articleBody` loses to the HTML pass.

Deliberately not heaviest-text-block: on the site that broke us (UN News) the `<article>` wrapper existed and was empty while the real paragraphs were siblings outside it. Heaviest-block would have caught that, but specificity-first gives cleaner text on the common case, so widening-on-empty was the cheaper fix.

Now the honest answer to your actual question: **we don't catch the truncated-body case, and our 300-char floor is not doing what your viewport heuristic is trying to do.** It reliably kills consent walls and cookie interstitials, which are short. A paywall teaser is typically 2-5 real paragraphs — 800-1500 chars of genuine article prose — and it sails through every check we have, with a correct byline, correct `datePublished` and correct JSON-LD. Structurally it's indistinguishable from a short news brief, which is a real thing we want to keep.

What we do instead of solving it is refuse to hide it: every row carries `articleWordCount`, `articleBodySource` (`jsonld`/`html`) and an `articleFetchStatus` (`ok`/`blocked`/`no-body`/`error`), so a consumer can set their own threshold per publisher. That's a punt, not a solution — but it's an honest punt, and it beats a heuristic that silently reclassifies short legitimate articles as paywalled.

The one signal I'd chase if I revisited it (haven't measured it, so treat it as a hypothesis): paywalled pages often still ship the *full* text length in metadata even when the DOM is cut — `wordCount` in JSON-LD, or a `<meta name="article:word_count">`. A large gap between the declared count and what you actually extracted would be a much more stable tell than anything measured against layout. If your corpus is big enough to test that, I'd genuinely like to know whether it holds.

Have you found the paywalled-teaser rate stable enough per-publisher to just maintain a domain list? That was our other fallback plan and I never found out how fast it rots.
