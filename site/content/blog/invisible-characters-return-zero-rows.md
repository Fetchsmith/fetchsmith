---
title: Four ways an invisible character makes a scraper return zero rows — all found in our own code
description: A trailing space, a decomposed accent, an ASCII-only tokenizer and an anchored ID regex. Each one turns a valid request into a clean SUCCEEDED run with an empty dataset. We found all four in our own Actors in four days.
date: 2026-09-15
tags: webscraping, javascript, api, debugging
tool: steam-reviews-scraper
---

The worst failure mode a data API can have is not an error. It's a **200 with an empty body**. Nothing is red, nothing retries, nothing pages anyone — the caller just concludes there was no data, and moves on with a wrong answer.

Over four days of edge-case testing on our own Actors we found four separate bugs with exactly that shape, and all four came down to a character the user couldn't see. None of them were exotic. Every one of them is the kind of thing that survives a code review, because the code reads correctly right up until you look at the bytes.

Here they are, in the order we found them, with what we actually measured.

## 1. The trailing space in a keyword filter

The commonest text-field artifact in the world is a leading or trailing space — double-click a word in a spreadsheet, drag-select a phrase from a PDF, paste from a chat message. Our review scrapers accepted a `keyword` filter and did the obvious thing:

```js
const keyword = String(input.keyword ?? '').toLowerCase() || null;
// ... later
if (keyword && !hay.includes(keyword)) continue;
```

Lowercased, but never trimmed. So the space survived into the substring test, and `"good "` only matched reviews where the word *happened* to be followed by a space — not those where it ended a sentence, preceded a comma, or ended the review.

Measured live on Steam's review API (app 730, 200 reviews pulled):

| Filter | Rows returned |
|---|---|
| `"good"` | 44 |
| `"good "` | 25 |

**43% of legitimate matches silently dropped**, and the run still reports SUCCEEDED — and the caller is still billed for the full upstream fetch either way. This is the version of the bug everyone nods along to. The next three are the same shape wearing better disguises.

Fix: `String(input.keyword ?? '').trim().toLowerCase() || null`.

## 2. The accent that isn't one character

Unicode lets you write "é" two ways: as the single code point U+00E9 (NFC, composed), or as a plain "e" followed by a combining acute accent, U+0065 U+0301 (NFD, decomposed). They render identically. They are not equal strings, and `String.prototype.includes` does not care that a human would call them the same word.

Almost everything you'll scrape is already NFC. We checked: Steam reviews, Apple's iTunes Search API, three live Shopify storefronts — 2,400+ strings, all composed. So where does NFD come from? From the *user's* side of the request. Text extracted from a PDF, copied out of an older macOS text field, or round-tripped through certain filesystems arrives decomposed.

Measured live, searching French-language CS2 reviews:

| Search term | Bytes | Rows |
|---|---|---|
| `très` (composed) | `74 72 c3 a8 73` | 24 |
| `très` (decomposed) | `74 72 65 cc 80 73` | **0** |

Same word on screen. Same run status. Zero rows.

Fix: normalize **both sides** right before the comparison — the user's input *and* the haystack text:

```js
const needle = String(input.keyword).normalize('NFC').toLowerCase();
const hay = text.normalize('NFC').toLowerCase();
```

Normalizing only the input is a half-fix that works by luck as long as your upstream stays composed.

## 3. The ASCII-only tokenizer that turns a filter into a passthrough

This one is more interesting, because it fails in the *opposite* direction and is therefore much harder to notice.

Our scholarship scraper split a multi-word search query into tokens and required every token to appear:

```js
const searchTokens = query.toLowerCase().split(/[^a-z0-9+#]+/).filter(Boolean);
```

The character class is ASCII-only, so every accented letter is treated as a **separator**. "école" becomes the single token `"cole"`. "María José" becomes `"mar"`, `"a"`, `"jos"`.

That stray `"a"` is the whole problem. A one-character token is satisfied by essentially any text, so the "every token must match" rule quietly degrades into "match almost everything". A buyer who typed a narrow name search gets a near-passthrough — and pays per returned row for all of it. No error, no warning, and the result set looks plausible enough that you might never question it.

Fix: normalize first, then split on a Unicode-aware class:

```js
const searchTokens = query.normalize('NFC').toLowerCase()
  .split(/[^\p{L}\p{N}+#]+/u).filter(Boolean);
```

Keep `+` and `#` in the class if your data has categories like "C++" or "C#" — otherwise you've just introduced bug #3's cousin.

## 4. The anchored ID regex next to an unanchored URL regex

Our app/review scrapers accept either a full store URL or a bare numeric ID in the same array field. The parser had one branch per format:

```js
const urlMatch = s.match(/id(\d{6,})/);          // unanchored
if (urlMatch) { ids.push(urlMatch[1]); continue; }
if (/^\d{6,}$/.test(s)) { ids.push(s); continue; }  // anchored
log.warning(`Could not parse "${s}" — skipping`);
```

Both branches look symmetric. They are not. The URL branch is an unanchored search, so it shrugs off surrounding whitespace for free. The bare-ID branch is anchored at both ends, so a single leading space makes it fail — and then the entry is skipped with nothing but a log line.

If that was the *only* app you asked for, the run ends `201` with an empty dataset. And because we only charge per pushed result, it also ends with **no charge** — which sounds fair until you realize it means there's no billing anomaly to notice either. The failure leaves no trace anywhere a caller would look.

Verified live before the fix, on three Actors:

| Input | Before | After |
|---|---|---|
| `apps: [" 1232780281"]` (App Store) | `201`, 0 rows | 3 rows |
| `apps: [" 730 "]` (Steam) | `201`, 0 rows | 3 rows |
| `podcasts: [" 1434243584"]` (Apple Podcasts) | `201`, 0 rows | 100 rows |

A bare numeric ID with a leading space isn't a contrived input — it's what you get pasting a column out of a spreadsheet.

Fix: `.trim()` in the initial normalization, before any parsing branch runs:

```js
const entries = raw.map(String).map((s) => s.trim()).filter(Boolean);
```

## The pattern underneath all four

Every one of these bugs lives in the gap between **what the user sees** and **what the comparison sees**, and every one of them fails silently because the code's error path is "no match" rather than "bad input".

Three rules fell out of fixing them, and they're now house style for every input we accept:

1. **Normalize at the boundary, once.** Trim and NFC-normalize every user-supplied string the moment it enters the program — not at each use site, where you will eventually miss one. The four bugs above are four different use sites of two missing boundary operations.
2. **Normalize both sides of a comparison.** A needle-only fix is a coin flip on your upstream's encoding choices, which you don't control and which can change without notice.
3. **Treat a silent zero as a bug report.** If a filter can produce zero rows, it should be possible to tell "genuinely nothing matched" from "your input didn't parse". A `log.warning` and `continue` is not that — nobody reads Actor logs on a run that says SUCCEEDED. Either fail loudly on unparseable input, or surface the count of skipped entries where the caller will actually see it.

The third one is the one we'd push hardest. Bugs #1 and #3 changed a row count; bugs #2 and #4 changed it to zero. In all four cases the run status was green, and in all four cases the only honest signal available to the caller was a number they had no independent way to check.

If you run a scraper or data API of your own, the cheapest version of this audit is one grep: find every `.includes(`, every `.test(`, and every `===` that touches a user-supplied string, and check whether both sides were normalized before they got there. It took us four days to find these four. The grep takes five minutes.

---

*The Actors referenced here — [Steam Reviews](https://apify.com/fetchsmith/steam-reviews-scraper), [App Store Reviews](https://apify.com/fetchsmith/app-store-reviews-scraper), [Apple Podcasts](https://apify.com/fetchsmith/apple-podcasts-scraper), [Google Play Reviews](https://apify.com/fetchsmith/google-play-reviews-scraper), [Shopify Products](https://apify.com/fetchsmith/shopify-products-scraper) and [Scholarships](https://apify.com/fetchsmith/scholarship-scraper) — are all HTTP-only and pay-per-result. Full list at [fetchsmith.com/tools](https://fetchsmith.com/tools).*

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned.*
