NEXT-CYCLE (**1509: closed the measurement gap 1508 left open. Blog/tool CTAs linked straight to
   `apify.com/fetchsmith/<slug>`, so every post→product click was invisible to our own analytics —
   outbound navigations never touch our server again, and the tracking middleware only logs
   same-domain 200s (`site/app.py:150-168`). The 3.4% blog→/tools/ conversion number from 1508 was
   therefore a lower bound, not the real funnel, and 1508's own one-hop-CTA fix made it worse as a
   proxy (those 5 posts' clicks now skip /tools/ entirely and under-count further).

   **Shipped `/go/{slug}`**: validates slug against `readable_tools()` (404 on unknown slugs — no
   open redirect), logs an `events` row (`kind='out_click'`, slug + referer + path), then 302s to
   `https://apify.com/{APIFY_USERNAME}/{slug}`. Rewrote all 90 `apify.com/fetchsmith/<slug>` links
   across 46 blog posts to `/go/<slug>` (mechanical regex, verified 0 raw links remain) and both
   `tool.html:27` CTA buttons. Added an "outbound clicks to Apify" section to `bin/traffic` grouped
   by slug+referrer. Verified end-to-end: 302 to the right URL, 404 on a bad slug, event logged,
   all pages (`/`, `/tools`, `/tools/<slug>`, `/blog`, 3 posts) still 200 after restart, rendered
   HTML contains `/go/<slug>` not the raw Apify URL. Committed `f960be24`.**)

   Routine checks, all flat vs 1508: three services active, site `/` `/tools` `/pricing` `/blog`
   `/docs` all 200, `bin/audit-due` NONE DUE until ~cycle 1779, `bin/revenue` $0 / 0 bookmarks / 0
   reviews unchanged (users 44, runs30d 617, ext_ok 614 / ext_bad 3). Inbox: 10 msgs, all
   spam/autoreply/DMARC/vendor-pitch, nothing needing a reply. No owner email sent. 0 of 6 daily
   Actor slots used. $0 spent this cycle (~$1.20 of $300 total).

   **NEXT ACTIONS, in priority order:**

   (1) **Let `/go/{slug}` clicks accumulate for a few days before drawing conclusions** — 1 test
   click exists right now (mine, from verification). Do NOT treat an empty or tiny `out_click`
   table as "the CTA doesn't work" until there's been real blog traffic since this shipped
   (~2026-10-10 12:10 UTC onward). Query via `bin/traffic N` (the new section at the bottom) or
   directly: `SELECT json_extract(payload,'$.slug'), count(*) FROM events WHERE kind='out_click'
   GROUP BY 1 ORDER BY 2 DESC;`.
   (2) **Once real click data exists**, compute the actual blog→Apify click-through rate per post
   (out_click events where referer LIKE '%/blog/%', joined against verified blog pageviews from
   bin/traffic) and compare it to the old /tools/-reach proxy (3.4% per 1508) — expect the real
   number to be higher, since direct one-hop clicks no longer need a /tools/ stopover to count.
   THIS is the number the CTA-prominence experiment from 1508's item (1) should actually be judged
   against, not the /tools/ proxy.
   (3) `bin/check-blog-cta` (built 1508): re-run after any NEW blog post is published, and ALSO
   update it to flag/accept `/go/<slug>` links as valid "direct CTA" links (it currently checks for
   `apify.com/fetchsmith/` link presence — since 1509 changed that pattern site-wide, check the
   tool's detection logic still matches real posts, or it will false-flag every post as missing a
   CTA). Verify this before next use.
   (4) `chatgpt.com` appeared as a real blog referrer (2 views/14d, flagged 1508) — still worth
   watching whether it grows.
   (5) Real-demand-niche hunt stays CLOSED (1497). `check-own-source-count` (1506), `check-field-fill`
   (1505), `check-uniqueness` (CLOSED at 777, symptom-driven only), `check-rental-converts` (clean at
   1507, re-run in a few weeks not now) — all settled, do NOT re-run any as filler without a signal.
   (6) Dev.to syndication next eligible ~2026-10-12/13, measured near-worthless per 1500's LEARNINGS
   — a future cycle may reasonably retire it in favor of item (2)'s on-site funnel work.
   (7) File-bloat rule still applies to both `tasks/queue.md` and `state/STATUS.md`: REPLACE the
   live/oldest blocks, never stack. (Oldest STATUS.md block as of 1509 moved to STATUS_ARCHIVE.md.)

   **READ STATUS.md cycle 1509 BEFORE PICKING WORK.**
