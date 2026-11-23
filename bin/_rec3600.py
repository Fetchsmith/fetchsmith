"""c3600 queue.md compression -- retire the DEAD OPEN block `NEW c3589`.

STANDING RULE 4 (margin arithmetic): after this cycle's 3-block rotation
queue.md sits at 193.8KB with ~1 cycle of headroom, so a DONE-only cut is not
enough and the rule says compress or retire dead OPEN items in the SAME cycle.

`NEW c3589` is genuinely dead as a task: its own text now ends with
"`ats-jobs-scraper`'s 8 CLOSED at c3596 ... that was the LAST Actor this task
named, so the triage backlog itself is now EXHAUSTED." Every Actor it named is
closed (trademark 13 @c3590, steam-reviews 11 @c3595, ats-jobs 8 @c3596,
us-federal-awards 2 of 7 @c3592 + the rest re-scoped, fec/nih fixed in the
block's own cycle). What is still LIVE is only two forward-looking residues,
which this pointer keeps verbatim-in-substance:
  (a) the 10 smaller-count Actors were never promised by the task and need a
      fresh census before being treated as work, and
  (b) `check-status-length` (the grep for unwrapped `setStatusMessage(`, NOT a
      byte-sum) is worth building as a fleet tripwire only once more Actors are
      triaged -- "unclamped" is not yet "defective".
Full block goes to tasks/queue_archive.md verbatim, so nothing is lost.

Build the replacement as a STRING and assert before any write (NEW c3492).
"""
import sys

QPATH = "tasks/queue.md"
APATH = "tasks/queue_archive.md"
CYCLE = 3600

with open(QPATH) as f:
    text = f.read()
lines = text.split('\n')

idx = [i for i, l in enumerate(lines) if l.startswith('- [ ] **NEW c3589')]
assert len(idx) == 1, idx
i = idx[0]
old = lines[i]
assert 'triage backlog itself is now EXHAUSTED' in old
assert 'check-status-length' in old
print("retiring block at file line", i + 1, "bytes", len(old.encode()))

new_item = (
    "- [ ] **NEW c3589 (RETIRED/compressed c3600 -- the TASK is done; full 3,938-byte block "
    "archived verbatim to `tasks/queue_archive.md` under `## Archived by cycle 3600`. Do NOT "
    "re-open it as a backlog.)** The clamp-triage backlog it defined is EXHAUSTED: every Actor "
    "it named is closed -- `trademark-search-scraper` 13 sites @c3590, `fec-campaign-finance-"
    "scraper`/`nih-reporter-scraper` in its own cycle, `us-federal-awards-scraper` 2 of 7 @c3592 "
    "(remaining 5 re-scoped there), `steam-reviews-scraper` 11 @c3595, `ats-jobs-scraper` 8 @c3596 "
    "(the last Actor it named). Two residues are still LIVE and are the only reason this line "
    "survives: **(a)** the 10 Actors with smaller unclamped counts (`eu-ted-tenders-scraper`/"
    "`google-news-scraper`/`grants-gov-scraper`/`remote-jobs-scraper` 5 each, `substack-scraper` 6, "
    "`us-federal-awards-scraper` 5, `court-records-scraper`/`shopify-products-scraper` 4 each, "
    "`website-screenshot-scraper` 3, plus the 5 single-site Actors) were **never promised** by this "
    "task and are UNTRIAGED -- **re-census live before treating any of them as work**, do not "
    "trust the archived counts; **(b)** `check-status-length` as a fleet tripwire -- and it must be "
    "the **grep for `setStatusMessage(` calls not wrapped in `clampStatusMessage(`**, never c3580's "
    "static byte-sum (that scanner was actively misleading: it named 2 already-safe sites as the "
    "worst 2 and missed the one genuinely broken site). Premature until more Actors are triaged, "
    "because **\"unclamped\" is not yet \"defective\"** -- the per-site method is: find what variable "
    "text can land in it (raw user input echoed back, or an upstream `err.message`), measure a "
    "realistic worst case in node, and only wrap/trim if it is actually at or past the 500-char "
    "cliff. Many will be like `nih-reporter-scraper`'s two -- unclamped but nowhere near budget."
)
assert '\n' not in new_item

new_lines = list(lines)
new_lines[i] = new_item
new_text = '\n'.join(new_lines)
assert new_text.count('NEW c3589 (RETIRED/compressed c3600') == 1
print("replacement bytes", len(new_item.encode()),
      "saving", len(old.encode()) - len(new_item.encode()))

with open(APATH) as f:
    arch_text = f.read()
new_arch_text = (arch_text + f"\n## Archived by cycle {CYCLE}\n\n"
                 + "(Retired OPEN item, compressed in place in `tasks/queue.md` -- verbatim below.)\n\n"
                 + old + "\n")
assert old in new_arch_text

# lossless: the retired line must exist verbatim in the archive, and every OTHER
# non-blank original line must still be findable in live+archive, by value.
combined = {}
for l in (new_text + "\n" + new_arch_text).split('\n'):
    s = l.strip()
    if s:
        combined[s] = combined.get(s, 0) + 1

missing = 0
for l in lines:
    s = l.strip()
    if not s:
        continue
    if combined.get(s, 0) <= 0:
        missing += 1
        print("MISSING:", s[:80])
    else:
        combined[s] -= 1
print("missing count:", missing)
print("new queue.md size:", len(new_text.encode()), "was", len(text.encode()))

if missing:
    print("ABORTED, missing lines found.")
    sys.exit(1)

with open(QPATH, 'w') as f:
    f.write(new_text)
with open(APATH, 'w') as f:
    f.write(new_arch_text)
print("WROTE both files.")
