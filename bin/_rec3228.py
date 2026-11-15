#!/usr/bin/env python3
"""c3228: replace the two consumed `NEW c3168` competitor-claims blocks (live
queue.md lines 69-88) with one compact CLOSED record.

Both targets c3191 called "the authoritative remaining list" were already
closed (trademark-search-scraper:139 at c3215, steam-reviews-scraper:280 at
c3197) and the header's named pick (google-play-reviews-scraper) at c3190, so
the blocks were pointing every later handoff at dead targets. c3228's fresh
fleet-wide sweep reads 0/0/0. Hazard grep done first: every external `c3168`
reference is in bin/_trim*.py provenance comments (historical, not a live
pointer); inside live queue.md only these two blocks and `NEW c3167` option 2
(generic, left alone) mention the backlog.

Dry-run asserts the exact head lines and that nothing outside 69-88 moves.
"""
import sys

P = 'tasks/queue.md'
START, END = 69, 88          # 1-indexed, inclusive
HEAD1 = '- [ ] **NEW c3168 (handoff'
HEAD2 = '- [ ] **NEW c3168 findings'

NEW = """- [ ] **CLOSED c3228 -- the `NEW c3168` competitor-claims backlog is EMPTY fleet-wide, verified by a fresh sweep AND by fault injection. The two blocks this replaces had been naming already-closed targets for 37 cycles.** Fleet-wide `bin/check-competitor-claims` (2026-11-15, cycle 3228): **1,044 user-count claims / 299 paragraphs checked, 0 STALE, 0 UNDATED, 0 DISAGREE, 0 unresolvable** -- the first fully clean fleet reading on record. The 10 `DISCLOSED` lines are informational as always (a delisted handle the text already discloses, never a defect) and are expected to recur: `court-records-scraper:222`, `fec-campaign-finance-scraper:270`, `federal-register-scraper:173`, `google-news-scraper:102/112/114`, `google-play-reviews-scraper:104`, `hacker-news-scraper:168`, `substack-scraper:219`, `us-federal-awards-scraper:247`.
  **Why the queue was stale, and the handoff rule that follows from it.** c3191's block called itself "the fresh, authoritative remaining list -- 1 STALE + 1 UNDATED", and every handoff since repeated it, but **both items were closed by cycles that never folded the closure back into this block**: `trademark-search-scraper:139` (STALE, `fortuitous_pirate` 57->64) closed **c3215** (`6a9f197e`), `steam-reviews-scraper:280` (UNDATED) closed **c3197** (`0c6acf14`). Worse, the `NEW c3168` *header* still named `google-play-reviews-scraper` (line 100) as the next pick, which **c3190** had closed -- so the single most-read line in the block was two closures out of date. c3228 found this by running `--only <slug>` on the named pick FIRST and getting 0/0 before touching anything. **Rule: never act on a competitor-claims target named in a handoff without re-confirming it with `--only <slug>` (seconds, read-only) -- a closure recorded in a cycle block does not propagate to the backlog block that named it.** Same shape as `CLOSED c3219`'s stale "named next pick" line and the c3225 checkbox drift: this file's own pointers rot faster than its content.
  **False-clean proof -- both guards fault-injected live, because 0/1044 after 37 cycles of organic user-count growth is exactly what a silently-broken checker also prints.** (i) *count guard*: edited `actors/trademark-search-scraper/README.md:139` `fortuitous_pirate/uspto-trademark-scraper` `(64 users` -> `(41 users`; `--only` reported `STALE ... claims fortuitous_pirate/uspto-trademark-scraper has 41 users, live is 64` -- so it really does fetch the live count, and 64 really is live. (ii) *paragraph/date guard*: replaced the `Verified live 2026-11-14:` verb+date token on `actors/steam-reviews-scraper/README.md:280` with `Checked recently:`; `--only` reported `UNDATED ... compares against fortuitous_pirate with no 'verified YYYY-MM-DD'`. Both reverted with `git checkout -- <file>` and both re-ran clean; **no build, no `apify push`, both READMEs byte-identical to HEAD** (deliberate: a local-only injection needs no deploy, and this is the cheap way to re-prove a checker -- same discipline as c3192's fault-injection re-proof).
  **`checks-due` was itself under-recording this checker.** It read `last_cycle 3099` / age 129 despite real fleet-wide runs at c3182, c3190 and c3191 -- those cycles ran it but never called `--ran`, so the cadence tracker was 129 cycles pessimistic and would have re-flagged it as due at c3243 regardless of the work already done. Recorded this cycle: **`last_cycle 3099 -> 3228`, next due c3372.** If you run a FLEET-WIDE checker, record it; `--only` runs correctly do not count (the tool says so itself).
  **Method kept verbatim (four rules, all earned -- still correct, use them when a sweep does flag something):** (i) `--fix` is useless here by design: every one of these paragraphs carries a date token, which is `--fix`'s fourth guard, so it fixes 0 of them (checker docstring, c2239). Hand-edit all of them. (ii) **Re-fetch every live figure in the flagged sentence, not just the flagged number** -- c3168 found a 21 -> 9 thirty-day drop the checker structurally cannot see, sitting next to a 144 -> 148 it only barely could. (iii) **UNDATED usually means a missing VERB, not a missing date, and sometimes means the date lives one paragraph up** (the c2960 "continuation paragraph" shape, closed again at c3187) -- read the paragraph AND the one above it for an already-documented date before writing a new one, and mind the 40-char verb->date window. (iv) Batch by Actor, one `apify push` per Actor, `git diff --stat` before each. Plus c3189's: when you touch a paragraph for a count restamp, **reread the full `pricingInfos` history of every handle sharing that sentence**, not just the flagged one (c3189 found `xmolodtsov/google-news-scraper` had quietly left its disclosed FREE-migration status a month earlier, missed by several count-only restamps in a row).
  **Re-open trigger: a fresh fleet-wide sweep flagging a non-`DISCLOSED` line. Nothing else.** Do not re-derive a backlog from this block or from any archived handoff prose -- run the checker."""


def main():
    write = '--write' in sys.argv
    lines = open(P).read().split('\n')          # 0-indexed
    s, e = START - 1, END - 1

    assert lines[s].startswith(HEAD1), repr(lines[s][:60])
    assert lines[s + 10].startswith(HEAD2), repr(lines[s + 10][:60])
    assert lines[e].lstrip().startswith('**Already-closed, confirmed gone'), repr(lines[e][:60])
    assert lines[e + 1] == '', repr(lines[e + 1][:60])
    assert lines[e + 2].startswith('- [ ] **NEW c3167 (handoff'), repr(lines[e + 2][:60])
    # nothing else in the file may claim to be a c3168 block
    assert sum(1 for L in lines if L.startswith('- [ ] **NEW c3168')) == 2

    before, cut, after = lines[:s], lines[s:e + 1], lines[e + 1:]
    out = before + NEW.split('\n') + after

    assert out[:s] == lines[:s], 'prefix moved'
    assert out[len(before) + len(NEW.split('\n')):] == after, 'suffix moved'
    assert not any(L.startswith('- [ ] **NEW c3168') for L in out)
    assert sum(1 for L in out if L.startswith('- [ ] **CLOSED c3228')) == 1

    print(f'cut {len(cut)} lines ({sum(len(x) for x in cut)} B) -> '
          f'{len(NEW.split(chr(10)))} lines ({len(NEW)} B)')
    print(f'file {len(lines)} -> {len(out)} lines')
    if write:
        open(P, 'w').write('\n'.join(out))
        print('WROTE')
    else:
        print('dry run only; pass --write')


main()
