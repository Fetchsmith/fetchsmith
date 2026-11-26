#!/usr/bin/env python3
"""One-off: service NEW c3768 -- promote residues (a)/(b)/(c), cut the 4 stale
one-off ITEM-closure heads (NEW c3728, CLOSED c3764, CLOSED c3544, CLOSED c3760)
and close c3768 itself. Index-keyed by unique line prefix, not by cycle id
(c3768's own lesson: ids collide across heads)."""
import sys

PATH = "tasks/queue.md"

with open(PATH, encoding="utf-8") as f:
    lines = f.readlines()

PREFIXES = {
    "c3728": "- [x] **NEW c3728 -- SHIPPED c3729.",
    "c3764": "- [x] **CLOSED c3764 (was `NEW c3760`",
    "c3544": "- [x] **CLOSED c3544 (DONE c3720",
    "c3760": "- [x] **CLOSED c3760 (was `NEW c3458`",
    "c3768": "- [ ] **NEW c3768 (MEDIUM",
}

found = {}
for key, prefix in PREFIXES.items():
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(hits) == 1, f"{key}: expected 1 match for {prefix!r}, got {len(hits)}"
    found[key] = hits[0]

NEW_BLOCK = (
    "- [x] **CLOSED c3789 (was `NEW c3768`) -- promoted the 3 residues the 4 "
    "target one-off ITEM closures held (`a`/`b`/`c` below), then cut all 4 "
    "heads (`NEW c3728`, `CLOSED c3764`, `CLOSED c3544`, `CLOSED c3760`) now "
    "that nothing live is lost.** `NEW c3728` had no residue (fully done, per "
    "its own c3768 note); the other 3 each held exactly one live fact, now "
    "promoted below. Net removed ~6.3KB (4 heads) minus ~0.9KB added (3 "
    "one-liners + this closure note).\n"
    "- [ ] **NEW c3789a (LOW) -- `zero_listing_prescreen()` is still "
    "syntax-checked but UNPROVEN against a live 0-listing owner** (both "
    "c3764 batches had listings, 13 and 24). It lives in whichever `bin/_rec*.py` "
    "is newest -- run `ls -t bin/_rec*.py` before cloning, do not hardcode a "
    "filename here (the `_rec3764.py` pointer this residue replaces was itself "
    "already stale). The next 0-listing owner the `NEW c3162` walk hits is "
    "its first real test; fallback is the hand method: probe each disclosed "
    "handle via `GET /v2/acts/<owner>~<slug>` (never `GET /v2/users/<owner>`, "
    "see `notes/LEARNINGS.md` \"c3760\" for why), all-404 => dead vendor "
    "(0 owed once the naming README discloses it), any-live => the "
    "`search_owner()` blind spot (file the tool gap, do not record find-free).\n"
    "- [ ] **NEW c3789b (LOW) -- do NOT re-probe `scrapebench~shopify-change-tracker`**, "
    "confirmed 404 three times (most recently 2026-11-26); already fully "
    "disclosed in `shopify-products-scraper/README.md` as a delisting, not a "
    "price cut.\n"
    "- [ ] **NEW c3789c (LOW, open design question, not actioned) -- should "
    "`competitor_audit` own our-own-platform-count recounts (e.g. "
    "`ats-jobs-scraper`'s \"N of our 12\" sentences) rather than relying on "
    "one-off notes to catch drift when we add a platform?** Raised by the "
    "now-cut `CLOSED c3544`.\n"
)

cut_idx = {found["c3728"], found["c3764"], found["c3544"], found["c3760"]}
out = []
for i, l in enumerate(lines):
    if i == found["c3768"]:
        out.append(NEW_BLOCK)
    elif i in cut_idx:
        continue
    else:
        out.append(l)

# Verify: every line not touched is preserved by VALUE, in order.
untouched_before = [l for i, l in enumerate(lines) if i not in cut_idx and i != found["c3768"]]
untouched_after = [l for l in out if l != NEW_BLOCK]
assert untouched_before == untouched_after, "untouched lines drifted"

with open(PATH, "w", encoding="utf-8") as f:
    f.writelines(out)

print("OK: cut 4 heads, replaced c3768 with closure + 3 promoted one-liners")
print("removed line indices:", sorted(cut_idx), "replaced index:", found["c3768"])
