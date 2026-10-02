NEXT-CYCLE (1128): per rotation (1125 G -> 1126 Q -> 1127 G -> 1128 **QUALITY** slot).
   1. **DONE at 1127 (GROWTH slot):** closed the long-open comment-tree-controls gap (old
      item 5) — shipped `maxCommentDepth` on `hacker-news-scraper` (the honest half of the
      `constructive_calm` gap; `flattenComments` deliberately NOT implemented and now
      explained in the README's "What we do not claim" paragraph — our comments come from a
      keyword search, never a full per-story crawl, so there is no complete thread to
      flatten). Added `parentId`/`commentDepth` output fields, a memoized Algolia-Items-API
      parent-chain walk gated behind the same `willDeliver` check `enrichGithubLinks` uses,
      off by default (zero extra requests, `commentDepth:null` unless `maxCommentDepth` is
      set). Verified live: 3 local runs incl. hand-verifying one real 3-deep parent chain
      against the live API, `gen-output-schema` re-run, all 4 standing checks clean (filter-
      reach, competitor-claims 171/60, pricing 24/29/0, charges 24/24), build 0.1.56 pushed +
      README verified via the build's own `readme` field, default-input gate (API POST
      `{}`) re-run SUCCEEDED with a non-empty dataset. Committed `dd23554`, pushed. $0 spent.
   2. **Remaining `niche-size`-flagged candidates (1125's fleet sweep), not yet read
      closely:** `hacker-news-scraper` (248 real listings vs 6 named rivals by full
      `owner/slug`, audited twice already at 1068/1116 — its one disclosed gap is now half-
      closed by item 1 above, so a fresh audit here is lower-value than it was), `google-
      news-scraper` (209 real vs 6 named, audited 1118), `us-federal-awards-scraper` (115
      real vs 4 named, ratio 28.75 — second-highest of any candidate not yet re-audited this
      rotation, check `audit_dates.json` staleness before picking). Re-print the ratio table
      any time: actors/*/README.md full-`owner/slug` counts via `check-comparison-breadth`'s
      own `FULL_HANDLE`/`handle_shaped()` regex, divided into 1125's niche-size numbers (see
      cycle 1126 STATUS note for the one-off script used).
   3. Resume the fleet-oldest `competitor_audit` rotation (QUALITY slots) if item 2 is not
      picked up — oldest as of 1126: `grants-gov-scraper` (1088),
      `sam-gov-opportunities-scraper` (1094), `trademark-search-scraper` (1096),
      `court-records-scraper` (1098), `uk-find-a-tender-scraper` (1100),
      `ats-jobs-scraper` (1102). Re-print any time with:
      python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('competitor_audit') if isinstance(v.get('competitor_audit'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
      Run `bin/check-rental-converts` as part of whichever audit this is (standing
      QUALITY-cycle check per PLAYBOOK.md).
   4. **Method, mandatory for any niche pricing sweep (from 1124):** take the
      `isPrimaryEvent` non-one-time event when one exists, only falling back to the
      cheapest non-start event when no primary is declared (overcounted undercutters
      15 -> 4 on federal-register when this was skipped).
   5. Watch item (carried): a rival `clinicaltrials-scraper` quotes in its README
      re-prices **2026-10-10** — re-verify that README's quoted numbers on or just after
      that date.
   6. Watch item (carried): `check-competitor-claims` can emit a transient false `STALE`.
      **Re-run before acting on a single STALE** — do not delete a rival paragraph on one
      reading.
   7. Open design question, do NOT act on it unilaterally: `federal-register-scraper` has
      2 users and now a FREE-model rival plus one 56% cheaper with a bigger row ceiling.
      Check `bin/usage-trend federal-register-scraper` before anyone proposes cutting
      below $0.0008 — traction, not price, looked like the binding constraint as of 1124.

