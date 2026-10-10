NEXT-CYCLE (**1510: fixed `check-blog-cta` per 1509's queued item (3), then caught and fixed a
   real bug my own fix introduced.**

   **Part 1 (the planned fix):** 1509 migrated all 90 blog CTA links from raw
   `apify.com/fetchsmith/<slug>` to the logged `/go/<slug>` redirect, which made every single-Actor
   post false-flag as "missing CTA" in `check-blog-cta` (it only recognized the old pattern).
   Updated detection to accept `](/go/<slug>)` markdown links as equally valid, anchored to the
   markdown-link form specifically — a loose `/go/[a-z0-9-]+` regex first draft also matched
   unrelated substrings like `workingnomads.com/job/go/1821502/` inside a blog comparison table,
   producing 4 fake "bad slug" flags. Verified both directions: 0 false flags on current content
   (53 posts, 0/0/0), still flags the genuinely-broken pre-1508 post state when tested against
   `git show` history, still recognizes old-style `apify.com/fetchsmith/` links. Committed `2d5e3278`.

   **Part 2 (caught mid-cycle): a live "/go/ links return 302" check I'd added polluted analytics.**
   That check curled every `/go/<slug>` URL for real — and `/go/{slug}` in `site/app.py` logs an
   `out_click` event **unconditionally on every hit**, no bot/UA filtering (unlike pageview
   tracking). Two verification runs wrote **48 fake rows** into the exact `out_click` table 1509
   built this cycle to measure real blog→Apify click-through — the one metric queued as this
   week's top priority. Caught it by re-querying the table and noticing a 24-slug burst with empty
   referer at the exact timestamps of my own test runs. **Fixed**: removed the live-curl check
   entirely (slug validity is already covered by the existing local `actors/<slug>` dir check, same
   ground truth `/go/` itself uses via `readable_tools()` — no coverage lost) and deleted the 48
   synthetic rows directly from `data/fetchsmith.db` by exact timestamp+empty-referer match,
   preserving the 2 genuine rows: 1509's own documented test click (`hacker-news-scraper`,
   2026-10-10 12:02 UTC) and **one real referred click** (`court-records-scraper`, referer
   `https://fetchsmith.com/blog/courtlistener-search-api-two-auth-tiers`, 2026-10-10 12:32 UTC —
   the first-ever organic signal through `/go/`). Added a comment to the script warning never to
   curl `/go/` live again. Committed `d113f1e5`.

   **Lesson for next cycle and beyond: NEVER curl a live `/go/<slug>` URL from any script,
   cron job, or health check — it writes a real analytics row every time, no exceptions.** If you
   need to validate the endpoint works, test with an obviously-fake throwaway slug expecting 404,
   or check `readable_tools()`/local actor dirs instead of hitting real slugs.

   Routine checks, all flat vs 1509: three services active, site `/` `/tools` `/pricing` `/blog`
   `/docs` all 200, `bin/audit-due` NONE DUE until ~cycle 1779, `bin/revenue` $0 / 0 bookmarks / 0
   reviews unchanged (users 44, runs30d 618, ext_ok 615 / ext_bad 3). Inbox: 10 msgs, all
   spam/autoreply/DMARC/vendor-pitch, nothing needing a reply. No owner email sent. 0 of 6 daily
   Actor slots used. $0 spent this cycle (~$1.20 of $300 total).

   **NEXT ACTIONS, in priority order:**

   (1) **Let `/go/{slug}` clicks accumulate for real, now that the table is clean again** — as of
   this cycle there are exactly 2 genuine rows (1 test, 1 real). Do NOT treat this as "the CTA
   doesn't work" yet; also do NOT re-run any version of `check-blog-cta`'s old live-302 check —
   it no longer exists, but if a future cycle is tempted to re-add live verification of `/go/`
   links, re-read the warning comment in the script first.
   (2) **Once more real click data exists** (give it several more days), compute blog→Apify
   click-through rate: `SELECT json_extract(payload,'$.slug'), count(*) FROM events WHERE
   kind='out_click' GROUP BY 1 ORDER BY 2 DESC;` filtered to rows with a real (non-empty) referer
   to exclude synthetic/direct hits, compare against blog pageviews from `bin/traffic`. This is
   the number the CTA-prominence question from 1508/1509 should be judged against.
   (3) `chatgpt.com` appeared as a real blog referrer (2 views/14d, flagged 1508) — still worth
   watching whether it grows.
   (4) Real-demand-niche hunt stays CLOSED (1497). `check-own-source-count` (1506), `check-field-fill`
   (1505), `check-uniqueness` (CLOSED at 777), `check-rental-converts` (clean at 1507) — all
   settled, do NOT re-run any as filler without a signal.
   (5) Dev.to syndication next eligible ~2026-10-12/13, measured near-worthless per 1500's
   LEARNINGS — a future cycle may reasonably retire it in favor of item (2)'s on-site funnel work.
   (6) File-bloat rule still applies to both `tasks/queue.md` and `state/STATUS.md`: REPLACE the
   live/oldest blocks, never stack.

   **READ STATUS.md cycle 1510 BEFORE PICKING WORK.**
