---
title: Next.js App Router ships your whole database table in the HTML — bold.org's RSC flight stream, decoded
description: bold.org renders scholarship data server-side and never hydrates it into a JSON API. The React Server Components flight stream in the raw HTML has the full records anyway — 30 per request, no browser, plus a sitemap that lies about how many pages actually exist.
date: 2026-09-10
tags: webscraping, nextjs, api, javascript
tool: scholarship-scraper
---

bold.org has no public API for its scholarship listings. It doesn't need one — it's a Next.js App Router site, which means every category page (`/scholarships/by-major/nursing-scholarships/` and 500+ others) does its data fetching on the server and ships the *result* straight into the initial HTML response. No client-side fetch, no hydration call to watch in devtools, nothing to reverse-engineer as "the API." The data is already sitting in the page source, wrapped in React's internal wire format.

```
$ curl -s https://bold.org/scholarships/by-major/nursing-scholarships/ | grep -c '__next_f.push'
```

We built [scholarship-scraper](https://apify.com/fetchsmith/scholarship-scraper) entirely on top of that one response — no headless browser, no proxy, ~30 complete scholarship records per HTTP request.

## The flight stream: one `JSON.parse`, several string chunks

React Server Components ship their payload as a sequence of script tags, each pushing one fragment of a single logical stream:

```
self.__next_f.push([1,"1:\"$Sreact.fragment\"\n2:..."])
self.__next_f.push([1,"a:[[\"$\",\"link\",\"0\",{...}]]\n"])
self.__next_f.push([1,"...\"scholarships\":[{\"acceptHighSchool\":false,...}]..."])
```

Each pushed value is a JSON-encoded *string* (note the escaped quotes) — decode each one with `JSON.parse`, concatenate them in order, and you get back a single text blob. Buried inside it, one straightforward `"scholarships":[` key away, is a plain JSON array of complete scholarship objects — award amounts, deadlines, essay prompts, donor names, the works. No `$L`/`$D`-reference resolution needed for the fields we ship; just find the key and slice out the balanced `[...]` that follows it (a small brace-counting scanner that's string- and escape-aware, since the payload itself contains JSON inside JSON inside a string literal).

That's the entire scraper, structurally: reassemble the chunks, find `"scholarships":[`, slice, `JSON.parse`. One category page = one HTTP request = ~30 full records, live-verified today at `694305` bytes of HTML → a `388539`-byte reassembled stream → one `nursing-scholarships` page yielding 20+ complete records including the exact one below.

## Not every value is plain JSON — some are references into other chunks

The flight format isn't *pure* JSON underneath; some values are wire-format references the client is meant to resolve against other chunks it hasn't loaded yet. Two you'll hit immediately on bold.org records, both live-observed today on the same nursing scholarship:

```json
"announcementDate": "$D2026-10-28T00:00:00.000Z",
"content": "$54"
```

`$D<value>` is cheap to handle — it's a **date marker**, and the value after the prefix is the plain ISO string you wanted; strip the two characters and you're done (`s.announcementDate.replace(/^\$D/, '')`). We apply the same strip to `publishedAt`/`updatedAt`.

`$54` is a different animal — a **chunk reference**, shorthand for "look up the object at ID `54` elsewhere in the stream." That's how React reassembles the full page component tree lazily on the client; it is not a value we can `.replace()` our way out of. bold.org uses it for the `content` field (the long-form HTML description body, as opposed to the short `description` summary we do ship), and resolving it correctly means indexing every numbered chunk in the stream and matching reference IDs — a real parser for a wire format that isn't stably documented anywhere, for one extra field. We ship the ~28 other typed fields and deliberately don't promise `content`; a `$D` prefix is a one-line fix, a bare `$<number>` reference is a different, harder problem, and treating the two the same in a scraper is how you ship a field that silently returns `"$54"` as a string instead of the description text a customer expected.

## The sitemap enumerates category pages — with the same URL listed over and over

bold.org's `sitemap.xml` is the natural way to discover category pages without hardcoding slugs, and it works — but it is not a set. Counting `<loc>` entries live today:

| Category family | Raw `<loc>` entries | Distinct URLs |
|---|---|---|
| `by-year` | 111 | 10 |
| `by-demographics` | 82 | 23 |
| `by-major` | 113 | 70 |
| `by-type` | 165 | 71 |
| `by-state` | 71 | 50 |

`by-year` lists the same 10 URLs 11 times over on average. A crawler that walks the sitemap in document order and stops after *N* pages, without deduplicating, spends most of its budget re-fetching pages it already has — we shipped exactly that bug for a while: a `by-year, maxCategoryPages: 5` run covered only 3 distinct pages instead of 5, and it only became visible once a features change (prioritizing matching pages for a search query) made the same URL show up three times running in the crawl log. The fix is a one-line `[...new Set(urls)]` per category type, but you only find the bug by counting raw-vs-distinct, not by trusting that a sitemap's `<loc>` list is already unique — nothing in the sitemap spec requires that, and this one isn't.

## `robots.txt` is permissive, with one sharp edge

```
User-agent: *
Disallow: /*?*
```

Plain paths are unrestricted — no crawl-delay, no blocked sections for the pages this Actor touches. The one rule that matters is the query-string blanket-disallow: `Disallow: /*?*` blocks *any* URL containing a `?`, which rules out using bold.org's own site-search query parameters as a crawl shortcut. That's fine here — the sitemap-plus-dedupe approach above never needs one — but it's the kind of rule that's easy to violate by accident if you build a "just add `?search=...`" shortcut later without re-checking the file.

## What this buys a scraper vs. a browser

Zero JS execution, zero DOM, zero proxy — a `curl`-class HTTP client and a stream reassembler get every field a headless browser would eventually render, at a fraction of the memory and none of the anti-bot surface area a real browser presents. The tradeoff is that the wire format is React's internal implementation detail, not a stable public contract — a Next.js version bump could reshape the chunk boundaries or the reference syntax without any external announcement. Detect that early by asserting the fields you actually rely on (we assert `slug` and `name` are present on every parsed record, not just that `JSON.parse` didn't throw) rather than trusting that "it parsed" means "it parsed correctly."

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned.*
