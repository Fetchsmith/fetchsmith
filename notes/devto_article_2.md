# We tested "JSON-LD only" article extraction against 8 real news sites. It got 0.

If you're pulling article text out of news pages, the textbook approach is: fetch the page, find the `<script type="application/ld+json">` block with `"@type": "Article"` or `"@type": "NewsArticle"`, and read `articleBody`. It's clean, it's structured, and it's what schema.org was built for. Several scraper tools advertise exactly this as their extraction method.

We tried it against 8 real publishers — BBC, The Guardian, NPR, Al Jazeera, UN News, Inside Climate News, ESG Dive, NextCity — while building full-text extraction into our [Google News Scraper](https://apify.com/fetchsmith/google-news-scraper). Result: **zero of eight** had `articleBody` populated in their JSON-LD. Publishers include the `Article` node — headline, author, datePublished, image — almost every field except the one with the actual text.

That matches what publishers actually want structured data for: rich snippets in search results and social cards. Nobody's optimizing their JSON-LD for scrapers reading the body copy, so the field with the real payoff for a scraper is the one most commonly left out.

## What actually works: read the rendered HTML, but pick the right container

Every one of our 8 test articles extracted cleanly once we fell back to the HTML paragraphs — but the *how* mattered more than expected.

The naive approach: pick the first element matching a plausible selector (`[itemprop=articleBody]`, `article`, `main`, ...) and grab its paragraph text. This fails silently on sites where the semantic wrapper exists but is empty or near-empty — UN News, for example, has an `<article>` element in the DOM, but the actual body paragraphs live as siblings outside it, not inside. Stop at the first *matching* selector and you get nothing; no error, just an empty string.

The fix: try selectors in order of specificity (`[itemprop=articleBody]` → `[class*=article-body]` → `[class*=story-body]` → `article` → `main` → `body`), but don't stop at the first *match* — stop at the first one that actually **yields text** (we used a threshold of ≥300 characters across paragraphs longer than 40 characters, to filter out nav/byline noise). That one change took our extraction rate on a real platform run from 3/5 articles to 5/5.

## Practical takeaways if you're building this yourself

- Don't build JSON-LD-only extraction and assume it covers "most" sites — test against your actual target publishers first. In our sample it covered none.
- Keep JSON-LD as the first attempt anyway — it's cheaper to parse and cleaner when it *is* there (some smaller/niche publishers do populate it).
- When falling back to HTML, score candidate containers by extracted text volume, not by selector priority alone. A wrapper existing in the DOM doesn't mean the content is inside it.
- Cache which extraction path (JSON-LD vs. which HTML selector) worked per publisher hostname. Publishers don't change their template every request, so after the first article from a given domain you can skip straight to the winning strategy — this keeps a long run at ~1 request per article instead of retrying every selector every time.

This is now shipped in Google News Scraper as an opt-in `fetchArticleBody` input — full cleaned article text, author, image, keywords and section, on top of the usual title/source/date/snippet, at no extra cost per article.

*Built by [FetchSmith](https://fetchsmith.com) — HTTP-only Apify Actors, AI-assisted development, disclosed.*
