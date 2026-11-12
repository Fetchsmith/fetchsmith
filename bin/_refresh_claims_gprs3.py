#!/root/agent/venv/bin/python
"""Cycle 3100: clear the 7 cross-paragraph DISAGREEs + 4 stale counts that
bin/check-competitor-claims flagged on actors/google-play-reviews-scraper/README.md.

Every number below was fetched live from GET /v2/acts/<owner>~<slug> on 2026-11-12,
so this aligns all mentions of each handle onto ONE current figure rather than
picking the most-recently-dated of the conflicting snapshots. Two of the edits are
prose, not just a number:

  - unfenced-group/google-play-store-scraper: 3 -> 6 users, but its 30-day run count
    collapsed from the 153 this README has cited since 2026-10-05 to **1**
    (publicActorRunStats30Days.SUCCEEDED). The "low user count hides real usage"
    argument the README built on that figure no longer holds and is retracted in
    place. Its PRICE was re-verified live and is unchanged (flat $0.00005/review at
    all six tiers, $0.00069 per app row on FREE), so the undercutter claim stands.
  - thequietstack/google-play-reviews: the c3099-era "now at 20" correction is itself
    now stale (25), so the correction gets its own dated restatement.

Each (old, new) pair asserts an exact expected occurrence count before writing.
"""
import sys
import pathlib

P = pathlib.Path("/root/agent/actors/google-play-reviews-scraper/README.md")

# (old, new, expected_occurrences)
EDITS = [
    # --- thewolves 2362/2291/2253 -> 2433 (live 2026-11-12) ---
    ("`thewolves/google-play-reviews-scraper` (2,362 users, re-verified live 2026-11-09)",
     "`thewolves/google-play-reviews-scraper` (2,433 users, re-verified live 2026-11-12)", 1),
    ("`thewolves/google-play-reviews-scraper` (2,291 users)",
     "`thewolves/google-play-reviews-scraper` (2,433 users)", 1),
    ("`thewolves/google-play-reviews-scraper` (2,253 users) does",
     "`thewolves/google-play-reviews-scraper` (2,433 users) does", 1),

    # --- theagents 827/811 -> 840 ---
    ("`theagents/googleplay-reviews` (827 users)",
     "`theagents/googleplay-reviews` (840 users)", 1),
    ("`theagents/googleplay-reviews` (811 users)",
     "`theagents/googleplay-reviews` (840 users)", 1),

    # --- neatrat 3217/3395/3368 -> 3524 (still the niche leader by users) ---
    ("`neatrat/google-play-store-reviews-scraper` (3,217 users, count re-verified live 2026-10-25)",
     "`neatrat/google-play-store-reviews-scraper` (3,524 users, count re-verified live 2026-11-12)", 1),
    ("`neatrat/google-play-store-reviews-scraper` (3,395 users, the niche leader)",
     "`neatrat/google-play-store-reviews-scraper` (3,524 users, the niche leader)", 1),
    ("`neatrat/google-play-store-reviews-scraper` (3,368 users)",
     "`neatrat/google-play-store-reviews-scraper` (3,524 users)", 1),

    # --- curious_coder 2702/2925/2911 -> 2965 (still 2nd-biggest by users) ---
    ("`curious_coder/google-play-scraper` (2,702 users — the niche's second-biggest listing by users",
     "`curious_coder/google-play-scraper` (2,965 users as of 2026-11-12 — the niche's second-biggest listing by users", 1),
    ("`curious_coder/google-play-scraper` (2,925 users)",
     "`curious_coder/google-play-scraper` (2,965 users)", 1),
    ("`curious_coder/google-play-scraper` (2,911 users)",
     "`curious_coder/google-play-scraper` (2,965 users)", 1),

    # --- automation-lab 1345/1293 -> 1409 (still 4th-biggest by users) ---
    ("`automation-lab/google-play-scraper` (1,345 users, re-verified live 2026-11-09 — the niche's fourth-biggest listing by users",
     "`automation-lab/google-play-scraper` (1,409 users, re-verified live 2026-11-12 — the niche's fourth-biggest listing by users", 1),
    ("`automation-lab/google-play-scraper` (1,293 users)",
     "`automation-lab/google-play-scraper` (1,409 users)", 1),

    # --- solidcode/google-play-apps-scraper 464/435 -> 480 ---
    ("`solidcode/google-play-apps-scraper` (464 users, re-verified live 2026-11-09)",
     "`solidcode/google-play-apps-scraper` (480 users, re-verified live 2026-11-12)", 1),
    ("`solidcode/google-play-apps-scraper` (435 users)",
     "`solidcode/google-play-apps-scraper` (480 users)", 1),

    # --- code-node-tools 402/419 -> 433 users, 101 -> 109 users-in-30d ---
    ("`code-node-tools/google-play-reviews-scraper` (402 users)",
     "`code-node-tools/google-play-reviews-scraper` (433 users)", 1),
    ("`code-node-tools/google-play-reviews-scraper` (419 users as of 2026-11-09, 101 in the last 30 days)",
     "`code-node-tools/google-play-reviews-scraper` (433 users as of 2026-11-12, 109 in the last 30 days)", 1),

    # --- lergassy 21 -> 26 (superlative "largest of the twenty-eight" re-checked: the
    #     other 27 sit at 1-3 users, so it still holds) ---
    ("`lergassy/google-play-reviews-scraper` (21 users as of 2026-11-09 — the largest of the twenty-eight)",
     "`lergassy/google-play-reviews-scraper` (26 users as of 2026-11-12 — the largest of the twenty-eight)", 1),

    # --- thequietstack 20 -> 25, in the sweep list and in the "ceiling" correction ---
    ("`thequietstack/google-play-reviews` (20 users as of 2026-11-09)",
     "`thequietstack/google-play-reviews` (25 users as of 2026-11-12)", 1),
    ("`thequietstack/google-play-reviews` (named above in the 2026-10-30 sweep at 4 users) is now at 20**",
     "`thequietstack/google-play-reviews` (named above in the 2026-10-30 sweep at 4 users) is now at 25** "
     "(re-verified live 2026-11-12; it read 20 on 2026-11-09, so it is still climbing)", 1),

    # --- unfenced-group: 3 -> 6 users AND the 153-runs claim retracted (live: 1) ---
    ("**`unfenced-group/google-play-store-scraper` (3 users but 153 successful runs in the last 30 days) charges a flat $0.00005 per review at every plan tier",
     "**`unfenced-group/google-play-store-scraper` (6 users as of 2026-11-12, but only **1** successful run in the last 30 days — "
     "down from the 153 this README cited from 2026-10-05 through 2026-11-09, so the \"a low user count is hiding real usage here\" "
     "reading of this listing is retracted; its price, re-verified live 2026-11-12, is unchanged) charges a flat $0.00005 per review at every plan tier", 1),
    ("**`unfenced-group/google-play-store-scraper` (3 users, 153 runs in the last 30 days) overlaps our review filter set",
     "**`unfenced-group/google-play-store-scraper` (6 users as of 2026-11-12, and just 1 run in the last 30 days — see the Pricing section: "
     "the 153-runs figure this README used to cite no longer holds, though its price and schema do) overlaps our review filter set", 1),

    # --- date the re-verified-counts sentence in the 2026-11-06 re-verify paragraph ---
    ("**And every listing in this niche that has real traction is still at parity with us or dearer:**",
     "**And every listing in this niche that has real traction is still at parity with us or dearer** "
     "(prices as verified 2026-11-06; every user count in this sentence re-fetched live 2026-11-12)**:**", 1),

    # --- the aspectRatings FAQ carries a field-name date; counts are now newer ---
    ("under the field name `criterias`, not `aspectRatings` (re-verified live 2026-11-03)",
     "under the field name `criterias`, not `aspectRatings` (field name re-verified live 2026-11-03, user counts 2026-11-12)", 1),
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

# structural asserts: none of the stale figures may survive anywhere in the file
for gone in ["2,362 users", "2,291 users", "2,253 users", "(827 users)", "(811 users)",
             "3,217 users", "3,395 users", "3,368 users", "2,702 users", "2,925 users",
             "2,911 users", "1,345 users", "1,293 users", "(464 users", "(435 users)",
             "(402 users)", "(419 users", "153 successful runs", "(3 users, 153 runs"]:
    assert gone not in out, f"stale figure survived: {gone}"
# and the live figures must each be present
for need in ["2,433 users", "(840 users)", "3,524 users", "2,965 users", "1,409 users",
             "(480 users", "(433 users", "26 users as of 2026-11-12", "25 users as of 2026-11-12",
             "6 users as of 2026-11-12"]:
    assert need in out, f"new figure missing: {need}"
# the file must not have changed length wildly or lost its section headers
for hdr in ["## Pricing", "## FAQ", "**What we do not claim.**"]:
    assert out.count(hdr) == src.count(hdr), f"header count changed: {hdr}"

P.write_text(out)
print(f"OK {len(EDITS)} edit(s) applied, {len(src)} -> {len(out)} bytes "
      f"({out.count(chr(10))+1} lines, was {src.count(chr(10))+1})")
