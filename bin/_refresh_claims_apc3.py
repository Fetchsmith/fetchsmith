#!/root/agent/venv/bin/python
"""Cycle 3100: clear the 3 cross-paragraph DISAGREEs + 2 stale counts that
bin/check-competitor-claims flagged on actors/apple-podcasts-scraper/README.md.

All counts fetched live from GET /v2/acts/<owner>~<slug> on 2026-11-12:
  ryanclinton/podcast-directory-scraper  221 users (28 in 30d)   was 216/217/207
  automation-lab/podcast-scraper         126 users (8 in 30d)    was 117/124
  sourabhbgp/apple-podcast-scraper        83 users (29 in 30d)   was 83/71/77
  tidydata/audio-video-transcription      32 users               was 20
  logiover/apple-podcasts-episode-scraper 78 users (20 in 30d)   was 74

Why this file is handled differently from google-play-reviews-scraper (c3100's other
fix): there the conflicting counts were plain staleness. Here the counts at lines 222
and 224 are deliberately-dated historical snapshots (cycle 2480 / 2026-10-30 and
cycle 2816 / 2026-11-06) sitting inside trend sentences that are ABOUT the movement
between them ("did not move", "did edge up since cycle 2480") -- overwriting those
numbers with today's would make both sentences false. So instead the duplicate
roll-call counts are removed from the two historical clauses (they only ever existed
to support "the trafficked listings don't compete on price", which the prose states
directly and which remains true), and the single current figure for each handle lives
in the Pricing section above. That clears the DISAGREE permanently instead of leaving
a "legitimate before/after pair" that every future cadence run must re-read by hand.

Also fixes a genuine internal contradiction found while reading: line 179 calls
`logiover` "the fastest-growing rival in the niche" and line 181 calls `ryanclinton`
"the fastest-growing listing in the niche". Live 2026-11-12 they are fastest-growing
on different measures -- logiover by RATE (20 new users in 30d on a base of 78, ~26%),
ryanclinton by ABSOLUTE new users (28 on a base of 221, ~13%) -- so each superlative
is now qualified by its measure rather than stated bare.
"""
import sys
import pathlib

P = pathlib.Path("/root/agent/actors/apple-podcasts-scraper/README.md")

# (old, new, expected_occurrences)
EDITS = [
    # --- sourabhbgp: count already correct at 83, restamp the as-of date ---
    ("`sourabhbgp` (83 users as of 2026-11-09, re-verified live 2026-10-16",
     "`sourabhbgp` (83 users as of 2026-11-12, re-verified live 2026-10-16", 1),

    # --- logiover 74 -> 78, superlative qualified to "by rate" ---
    ("The fastest-growing rival in the niche is `logiover` (74 users, 20 of them in the last 30 days, re-verified live 2026-11-05,",
     "The fastest-growing rival in the niche *by rate* is `logiover` (78 users as of 2026-11-12, 20 of them in the last 30 days "
     "— about 26% of its base, the steepest proportional growth in the niche, re-verified live 2026-11-05,", 1),

    # --- ryanclinton 216 -> 221, superlative qualified to "by absolute new users" ---
    ("`ryanclinton/podcast-directory-scraper` (216 users, 31 in the last 30 days, re-verified live 2026-11-05 — the fastest-growing listing in the niche)",
     "`ryanclinton/podcast-directory-scraper` (221 users as of 2026-11-12, 28 in the last 30 days, re-verified live 2026-11-05 "
     "— the fastest-growing listing in the niche *by absolute new users*, though `logiover` above grows faster as a share of its own base)", 1),

    # --- automation-lab 117 -> 126; "2nd-biggest" re-checked and still true
    #     (ryanclinton 221 > automation-lab 126 > sourabhbgp 83) ---
    ("`automation-lab/podcast-scraper` (117 users, 17 in the last 30 days — the niche's 2nd-biggest listing)",
     "`automation-lab/podcast-scraper` (126 users as of 2026-11-12, 8 in the last 30 days — still the niche's 2nd-biggest listing, "
     "behind `ryanclinton` below)", 1),

    # --- tidydata/audio-video-transcription 20u -> 32u (excluded-category listing,
    #     price unchanged at $0.003/min, so only the count moves) ---
    ("`tidydata/audio-video-transcription` (20u) $0.003/min",
     "`tidydata/audio-video-transcription` (32u as of 2026-11-12) $0.003/min", 1),

    # --- cycle-2480 historical roll-call: drop the duplicate counts, keep the trend ---
    ("while this niche's trafficked listings (`ryanclinton/podcast-directory-scraper` 207u, `automation-lab/podcast-scraper` 124u, "
     "`sourabhbgp/apple-podcast-scraper` 71u) did not move — growth is still entirely at the 1-2-user floor.",
     "while this niche's three trafficked listings (`ryanclinton/podcast-directory-scraper`, `automation-lab/podcast-scraper` and "
     "`sourabhbgp/apple-podcast-scraper`) did not move at this sweep — growth is still entirely at the 1-2-user floor. "
     "Their current user counts are given once, in the Pricing section above, rather than restated per sweep.", 1),

    # --- cycle-2816 historical roll-call: same treatment ---
    ("while this niche's trafficked listings did edge up since cycle 2480 (`ryanclinton/podcast-directory-scraper` 217 users, "
     "`automation-lab/podcast-scraper` 124, `sourabhbgp/apple-podcast-scraper` 77), not one of them competes on price",
     "while this niche's three trafficked listings did edge up since cycle 2480 (the same `ryanclinton`, `automation-lab` and "
     "`sourabhbgp` listings named in the Pricing section above, which carries their current counts), not one of them competes on price", 1),
]

src = P.read_text()
out = src
bad = 0
for old, new, want in EDITS:
    got = out.count(old)
    if got != want:
        print(f"FAIL expected {want} occurrence(s), found {got}: {old[:90]!r}")
        bad += 1
        continue
    out = out.replace(old, new)
if bad:
    print(f"\n{bad} edit(s) did not match -- NOTHING WRITTEN")
    sys.exit(1)

# no stale figure may survive anywhere in the file
for gone in ["(216 users", "217 users", " 207u", "(117 users", " 124u", "`automation-lab/podcast-scraper` 124",
             " 71u)", "`sourabhbgp/apple-podcast-scraper` 77", "(74 users", "(20u)",
             "2026-11-09, re-verified live 2026-10-16"]:
    assert gone not in out, f"stale figure survived: {gone}"
# live figures must be present
for need in ["221 users as of 2026-11-12", "126 users as of 2026-11-12", "83 users as of 2026-11-12",
             "32u as of 2026-11-12", "78 users as of 2026-11-12"]:
    assert need in out, f"new figure missing: {need}"
# exactly one unqualified "fastest-growing" superlative must no longer exist
assert "the fastest-growing listing in the niche)" not in out
assert "The fastest-growing rival in the niche is" not in out
# structure intact
for hdr in ["## Pricing", "## FAQ"]:
    assert out.count(hdr) == src.count(hdr), f"header count changed: {hdr}"

P.write_text(out)
print(f"OK {len(EDITS)} edit(s) applied, {len(src)} -> {len(out)} bytes "
      f"({out.count(chr(10))+1} lines, was {src.count(chr(10))+1})")
