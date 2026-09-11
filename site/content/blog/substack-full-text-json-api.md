---
title: Substack's archive API returns a body_html field for every post — it's just always null
description: Substack's public JSON endpoints need no login or cookies, but the field that promises full article text on the archive listing is present and empty on every row. The real text lives one request away, per post.
date: 2026-09-11
tags: webscraping, api, newsletters, json
tool: substack-scraper
---

Every Substack publication exposes its whole archive as plain JSON, no login required:

```
GET https://<handle>.substack.com/api/v1/archive?sort=new&limit=1
```

(follow the 301 — a custom domain like `astralcodexten.com` redirects the API path too, not just the site). The response is a list of full post objects, and each one already has a `body_html` key. It looks like the entire article, ready to read:

```json
{
  "id": 172993382,
  "slug": "royce-on-san-francisco",
  "title": "Royce On San Francisco",
  "post_date": "2026-09-09T13:00:00.000Z",
  "wordcount": 3812,
  "body_html": null,
  "truncated_body_text": "Content warning: discussion of illegal drug use, dead bodies..."
}
```

That's a live row from `astralcodexten`'s archive, fetched while writing this post. `body_html` is a real field on every item — not missing, not renamed — and its value is `null` on every single row, regardless of `wordcount` or whether the post is free or paywalled. The only text you get from the archive endpoint is `truncated_body_text`, a short teaser.

## The 200 is real, the field is just empty — the actual text is one request away

The full body lives on the single-post endpoint:

```
GET https://<handle>.substack.com/api/v1/posts/<slug>
```

Same `body_html` key, same post, this time populated — 14,799 characters of real HTML for that same `royce-on-san-francisco` post, fetched seconds after the archive call above returned `null`. One extra HTTP request per post is the entire cost of going from "a list of titles" to "the actual article."

This is the same failure shape as the [Apple Podcasts default-input holes](/blog/apple-podcasts-public-json-api) we wrote up earlier: a 200 status and a well-formed JSON object don't mean the field you actually want is populated. If a scraper's differentiator is "full article text," the only way to know it delivers is to check the length of the string, not just that the key exists.

## In-publication search takes one specific parameter combination

The archive endpoint also does server-side search — but only one way. Ask for `sort=search`:

```
GET /api/v1/archive?sort=search&search=AI&limit=1
```

```json
{"errors": [{"location": "query", "param": "sort", "msg": "Invalid value"}], "status": 400}
```

A clean `400`, not a silent empty result. The working combination is `sort=new&search=<query>` — keep the normal sort value and add `search` alongside it:

```
GET /api/v1/archive?sort=new&search=AI&limit=2
```

returns real matches (`"God Help Us, Let's Try To Understand AI Monosemanticity"`, `"Make A Personalized AI Kids' Book"` from a live query against `astralcodexten`, both genuinely AI-topical). There's also a global `substack.com/api/v1/post/search` endpoint that looks like it should search across every publication at once — it returns 200 with an empty result set for every query we tried, so treat it as non-functional rather than building a cross-publication feature on it.

## Comments come back as a tree, and you have to ask for it correctly

```
GET /api/v1/post/<id>/comments?token=&all_comments=true&sort=best_first
```

Leaving out `token=` (even empty) gets you a `400` for a missing required param — it has to be present, just blank. The response nests replies inside a `children` array on each comment rather than a flat list with a parent pointer, so reconstructing a flat, queryable thread means walking the tree yourself and recording each comment's depth from its own recursion, not reading a `parentCommentId` field that doesn't exist in the raw response.

## Packaged version

[substack-scraper on Apify](https://apify.com/fetchsmith/substack-scraper) does the extra work this API needs: one archive call to find the posts, one follow-up call per post for the real `body_html` (cleaned to plain text, HTML kept optional), and a recursive flatten of the comment tree with a `parentCommentId` field added back in for you. `searchQuery` uses the working `sort=new&search=` combination automatically. Custom domains (`bigtechnology.com`, `astralcodexten.com`) work the same as the `<handle>.substack.com` form — no login, no browser, pay per result.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every JSON snippet above comes from a live request made while writing this post, not from documentation.*
