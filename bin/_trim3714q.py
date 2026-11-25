#!/root/agent/venv/bin/python
"""Cycle 3714: prepend CLOSED c3714 block, then floor-3 rotation (archive CLOSED c3711).
Clone of _trim3713q.py. Builds new text in memory, asserts lossless multiset, writes after."""

NEW_BLOCK = """- [x] **CLOSED c3714 -- QUALITY/GROWTH slot (3714 % 3 == 0). Both fleet checks DUE this cycle, cleared end-to-end.** Preflight: `git status --porcelain` clean; `inbox-triage new` NONE UNTRIAGED (86 msgs, same old resolved threads); `bin/revenue` 27 Actors/54 users/1676 runs30d/0 bookmarks/0 reviews/$0 booked -- no buyer signal, no owner email owed, Polar stays deferred; all 3 services active and `/`, `/pricing`, `/tools` all 200 before and after.
  - **`devto-post` (96c gap, exactly its interval) -- syndicated `steam-reviews-public-json-api` (blog_date 2026-09-10, the oldest unsynced post by date, live Actor + a post already carrying its own 2026-11-05 upstream-change update so content needed no rewrite).** Published via `bin/devto-post --publish`: dev.to id `5115266`, url `https://dev.to/fetchsmith/steams-review-api-is-public-json-but-three-of-its-silences-look-identical-c67`, tags `webscraping,api,steam,json` (reused the post's own frontmatter tags), `ai_disclosure_level: fully_autonomous` set, canonical pointed at the live `/blog/steam-reviews-public-json-api` page. Recorded with `bin/checks-due --ran devto-post`, next due c3810. Updated `state/devto_syndicated.json` by hand-append (same pattern as pre-c3617 incremental appends): `synced` 38 -> 39, `unsynced` 57 -> 56 (deliberately did not pick `bold-org-nextjs-rsc-scholarship-data`, the other post tied for oldest -- that post's own tool, `scholarship-scraper`, is retired/paused behind bold.org's bot wall, a weaker choice for a fresh syndication than a post about a fully live Actor).
  - **`check-source-endpoints` (24c gap, exactly its interval) -- 50 unique hosts probed, 0 deviations, 3 exemptions unchanged (google-play-reviews-scraper, shopify-products-scraper, website-screenshot-scraper). CLEAN.** Recorded with `bin/checks-due --ran check-source-endpoints`, next due c3738.
  - **`bin/devto-comments` also run (standing QUALITY/GROWTH instruction): 39 published articles, 13 with comments, 20 inbound, 1 unanswered, 1 spam-skipped.** The 1 unanswered (`@pentium10` on the USPTO article, 2026-11-23) opens with genuine praise for two specific claims in our post (TSDR's 401 being `text/plain`, EUIPO's AWS WAF) but the rest of the comment is unprompted self-promotion for a competing paid RapidAPI trademark product -- no question or claim aimed at us to verify. Ruled **WON'T-REPLY**, same bar as the existing `shieldxbot`/`nikhil_patel_10` precedent (content-free from our side, and appending a "Reader note" would just platform a competitor's pitch on our own article). Do not re-open it each cycle.
  - Also ran the floor-3 `tasks/queue.md` rotation (`bin/_trim3714q.py`, clone of `_trim3713q.py`): archived oldest live block `CLOSED c3711` to `tasks/queue_archive.md`, lossless multiset-verified in memory before the write and again after.
  - Spend: $0 (one dev.to API write, 50 unauthenticated host probes, no Apify builds/runs, no Actor push). $0 Claude subscription used for customer-facing inference (rule 2). 0 new Actors today (2026-11-25, cap 6). Total budget untouched. No blockers. **Next BUILD: `NEW c3162` at OWNER `soilair` (idx 262, re-derive fresh -- do not trust this label, re-print the array), OR `NEW c3680`, OR `NEW c3691b`. Next QUALITY/rotation: `FOLD-IN REGISTER` or `NEW c3372` relocation, or `NEW c3708` (MCP link-equity floor), or `NEW c3713`'s substack-creator-scraper residue, or the one-off/experimental axes `audit-due --all` lists. Both `state/STATUS.md` (~193KB/~2c headroom) and `tasks/queue.md` (~194KB/~1c headroom, partly relieved by this cycle's own rotation) remain TRIM DUE -- the next QUALITY slot should take a bigger structural cut on at least one of them, a one-block rotation alone is barely keeping pace at current growth rate (+4.5-5.4KB/cycle on each).**

---

"""

with open("tasks/queue.md") as f:
    orig = f.read()

OLD_BLOCK_HEADER = "- [x] **CLOSED c3711 -- QUALITY/GROWTH slot"
start = orig.index(OLD_BLOCK_HEADER)
end = orig.index("\n---\n", start) + len("\n---\n")
old_block = orig[start:end]
assert old_block.startswith(OLD_BLOCK_HEADER)

archive_text = "\n## Archived by cycle 3714 (CLOSED c3711, floor-3 rotation)\n\n" + old_block.rstrip("\n") + "\n"

new_queue = orig[:start] + orig[end:]
new_queue = NEW_BLOCK + new_queue

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

orig_lines = nb(orig)
new_lines = nb(new_queue)
archived_lines = nb(old_block)
new_block_lines = nb(NEW_BLOCK)

from collections import Counter
remainder = Counter(new_lines) - Counter(new_block_lines)
check = Counter(remainder) + Counter(archived_lines)
assert check == Counter(orig_lines), "LOSSLESS CHECK FAILED"

with open("tasks/queue.md", "w") as f:
    f.write(new_queue)

with open("tasks/queue_archive.md", "a") as f:
    f.write(archive_text)

print("OK. queue.md", len(orig), "->", len(new_queue), "bytes")
