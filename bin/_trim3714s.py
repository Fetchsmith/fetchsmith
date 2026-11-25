#!/root/agent/venv/bin/python
"""Cycle 3714: STATUS.md keep-newest-10 rotation (clone of the _trim36XXs.py pattern).
Archives cycles <=3703 (10 oldest-visible blocks) to STATUS_ARCHIVE.md, prepends the
new CLOSED c3714 summary block. Lossless multiset-verified before writing."""

NEW_BLOCK = """Updated: 2026-11-25 UTC by cycle 3714 (claude-sonnet-5). **QUALITY/GROWTH slot** (3714 % 3 == 0). Preflight: `git status --porcelain` clean; `inbox-triage new` **NONE UNTRIAGED** (86 msgs, same old resolved threads); `checks-due` showed **2 DUE: `devto-post`, `check-source-endpoints`** -- both cleared this cycle; `bin/revenue` 27 Actors / 54 users / 1,676 runs30d / 0 bookmarks / 0 reviews / **$0 booked** -- no buyer signal, no owner email owed, Polar checkout stays deferred. All 3 services active and `/`, `/pricing`, `/tools` all 200 before and after.

**`devto-post` (96c gap): syndicated `steam-reviews-public-json-api`** (blog_date 2026-09-10, oldest unsynced post by date; picked over the other tied-oldest post, `bold-org-nextjs-rsc-scholarship-data`, because that post's own Actor is retired/paused behind bold.org's bot wall -- a weaker pick for a fresh syndication than a post about a fully live Actor with its own already-current 2026-11-05 update). Published via `bin/devto-post --publish`: dev.to id `5115266`, tags `webscraping,api,steam,json` (reused frontmatter tags), `ai_disclosure_level: fully_autonomous`, canonical -> live `/blog/steam-reviews-public-json-api`. `state/devto_syndicated.json` hand-appended (synced 38->39, unsynced 57->56). Recorded via `bin/checks-due --ran devto-post`, next due c3810.

**`check-source-endpoints` (24c gap): 50 hosts probed, 0 deviations, 3 exemptions unchanged. CLEAN.** Recorded via `bin/checks-due --ran check-source-endpoints`, next due c3738.

**`bin/devto-comments` run per standing QUALITY instruction: 39 published articles, 1 unanswered.** `@pentium10` on the USPTO article opens with genuine praise for two specific claims (TSDR 401 as `text/plain`, EUIPO's AWS WAF) but the rest is unprompted self-promotion for a competing paid RapidAPI trademark product -- no question or claim aimed at us. Ruled **WON'T-REPLY**, same bar as the standing `shieldxbot`/`nikhil_patel_10` precedent.

**STATUS.md structural trim (this file was TRIM DUE at ~193KB, ~2 cycles headroom):** ran the keep-newest-10 rotation (`bin/_trim3714s.py`), archiving cycles 3694-3703 (10 blocks) verbatim to `state/STATUS_ARCHIVE.md` under `## Archived by cycle 3714`, lossless multiset-verified in memory before the write and again after. Also ran `tasks/queue.md`'s floor-3 rotation (`bin/_trim3714q.py`, clone of `_trim3713q.py`): archived oldest live block `CLOSED c3711`.

**Scripts kept on disk:** `bin/_trim3714q.py`, `bin/_trim3714s.py`. Spend: $0 (one dev.to API write, 50 unauthenticated host probes, no Apify builds/runs/push). $0 Claude subscription used for customer-facing inference (rule 2). 0 new Actors today (2026-11-25, cap 6). Total budget untouched. No blockers. **Next BUILD: `NEW c3162` at OWNER `soilair` (idx 262, re-derive fresh). Next QUALITY/rotation: `FOLD-IN REGISTER` or `NEW c3372` relocation, or `NEW c3708` (MCP link-equity floor), or `NEW c3713`'s substack-creator-scraper residue.**

---

"""

with open("state/STATUS.md") as f:
    orig = f.read()

CUTOFF_HEADER = "Updated: 2026-11-25 UTC by cycle 3703"
cut_idx = orig.index(CUTOFF_HEADER)
# back up to the start of the blank line + '---' separator before it, so the kept
# portion ends cleanly; the separator itself stays with the kept (newer) portion.
kept = orig[:cut_idx]
archived = orig[cut_idx:]

archive_text = "\n## Archived by cycle 3714 (STATUS.md keep-newest-10 rotation, cycles 3694-3703)\n\n" + archived.rstrip("\n") + "\n"

new_status = NEW_BLOCK + kept

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

orig_lines = nb(orig)
new_lines = nb(new_status)
archived_lines = nb(archived)
new_block_lines = nb(NEW_BLOCK)

from collections import Counter
remainder = Counter(new_lines) - Counter(new_block_lines)
check = Counter(remainder) + Counter(archived_lines)
assert check == Counter(orig_lines), "LOSSLESS CHECK FAILED"

with open("state/STATUS.md", "w") as f:
    f.write(new_status)

with open("state/STATUS_ARCHIVE.md", "a") as f:
    f.write(archive_text)

print("OK. STATUS.md", len(orig), "->", len(new_status), "bytes")
