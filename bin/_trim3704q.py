#!/root/agent/venv/bin/python
"""Cycle 3704: prepend the `CLOSED c3704` cycle record to tasks/queue.md and run the
STANDING c3280 floor-3 CLOSED rotation (archive `CLOSED c3701`, the oldest of three).

Shape follows bin/_trim3672h.py / the c3672 CADENCE CHANGE: the floor is 3 -- keep the
newest 2 cycle-record blocks plus the running cycle's own. Entering this cycle the live
file carried c3703/c3702/c3701, so adding c3704 means c3701 leaves.

Per the two _trim3492q.py bugs recorded in notes/PLAYBOOK.md: (1) build both new file
texts as STRINGS and run every assert against them IN MEMORY before opening anything for
writing, so a failed check leaves both files untouched and the run is retryable; (2)
compare the rewritten/exempt lines by VALUE, never with `is`.

Only the CLOSED blocks are rotated. The standing non-report `- [x]` blocks (`NEW c3681`,
`RESOLVED c3672`, `PARTIALLY DONE`, `DECIDED c3081`) are NOT cycle records and are never
in a cut span -- asserted below, along with the rule that no OPEN `- [ ]` item is cut.
"""
import os
import sys

ROOT = "/root/agent"
QUEUE = os.path.join(ROOT, "tasks/queue.md")
ARCHIVE = os.path.join(ROOT, "tasks/queue_archive.md")

NEW_BLOCK = """- [x] **CLOSED c3704 -- BUILD slot (3704 % 3 == 2). `NEW c3162` vendor-catalogue triage at OWNER `scrupulous_waterbird_m4w` (pointer re-derived fresh off a live 321-owner `>=3x` enumeration and confirmed at idx 253, immediately after `scrolahdata`, exactly as c3703 handed it on) -- 22 live listings, 0 flagged by the sweep, 4 near-miss rows ruled MANUALLY, 0 disclosures owed.** Full-handle grep (c3628 rule): all 22 handles grepped as `vendor/slug`, exactly 3 hits and all 3 are the rows already disclosed. Per-row verdicts in `state/audit_data/c3704_scrupulous_waterbird_prices.json`.
  - **THE METHOD FIND, and it is why this batch is not a no-op despite scoring 0 flags: a 0-FLAG SWEEP IS NOT A 0-RIVAL OWNER.** `check-vendor-catalogue`'s niche-vocabulary filter flagged none of the 22, but reading the owner's TITLE LIST for product shape surfaced 4 rows that needed a real ruling -- sharpest being `sec-edgar-full-text-search`, adjacent to `sec-insider-trades-scraper`, which matched no curated term because its title and description say only "SEC EDGAR" and never "insider". The script's own docstring predicts this false negative ("can still MISS a real rival whose copy avoids every curated term"); the cheap mitigation is now carried in the `NEW c3162` tracker and in `notes/LEARNINGS.md` c3704.
  - **All 4 ruled out, 0 owed, every dominator re-read LIVE per the c3680 trap; per-row reasoning is in the audit_data JSON, not repeated here.** `sec-edgar-full-text-search`: bucket 1/2 (a filing-INDEX search -- form type, accession number, CIK, ticker, SIC -- with no shares/price/code/value field, the exact class `sec-insider-trades-scraper/README.md:267` already rules out by name and README:16's "Parsed transactions, not filing lists" bullet pre-covers) AND bucket 7 independently (at $0 it is dominated by two already-disclosed $0 rivals strictly CLOSER in scope, both re-read live). `craigslist-listings`: bucket 1 (one classified-ads site, no remote filter, no dedup, no salary normalization, not an ATS) plus bucket 7. `nyc-open-data`: bucket 1 (a single-CITY Socrata portal against four US FEDERAL datasets -- the standing `publicmoney/*` single-national-portal ruling applies a fortiori). `europe-pmc-papers`: bucket 2 (LITERATURE is a different unit from a grant AWARD, the ruling that retired `crawlerbros/icite-scraper`; covers this owner's whole arxiv/openalex/crossref/open-library cluster).
  - **First all-free owner in this triage: all 22 listings carry NO pricing record at all** (`pricingInfos: null`), i.e. $0/row across the catalogue -- which is why the rulings had to turn on product shape, price could not separate a single row.
  - **Liveness re-verify of this owner's 3 already-disclosed rows: 0 drift on all three** (the c3700 routine, which is where that cycle's real find came from) -- `clinical-trials-gov` still never-monetized, `openfda-drug-events` still 3u/FAERS-scope, `hn-launches` still $0/Launch-HN-only. `clinicaltrials-scraper/README.md:157`'s load-bearing filed-FREE-vs-never-monetized distinction was re-proved live against its own two control handles (`labrat011/clinical-trials-scraper`, `bikram07/clinical-trials-feed`, both carrying a dated explicit FREE entry effective now). One sub-threshold drift deliberately not acted on: `constant_quadruped/sec-edgar-filings-scraper` 119u -> 125u, a +6 well under the 20-user re-pricing bar, still $0, so its dated figure stands.
  - **Three ways to misread a rival's price, all three hit on this one owner, all three written up in `notes/LEARNINGS.md` c3704 (read it there, not here) -- the first two make a paid Actor look free, the third makes a free Actor look paid.** In brief: (a) `/acts/<handle>.currentPricingInfo` is ALWAYS null, verified across 4 actively-paid rivals, so it is never a $0 signal; (b) complement to the c3680 trap -- the `store?username=` row does carry the real model and full event map while `/acts` never does, so read MODEL from either but PRICE only via `/acts` -> `pricingInfos` -> `effective()`; (c) a truncated `pricingInfos` dump shows entry 0, often long superseded -- that briefly looked like a real README drift this cycle until `effective(pi, now)` cleared it, the mirror image of the c3244 rule's usual "not `pricingInfos[-1]`" framing.
  - Floor-3 rotation ran the same cycle (`bin/_trim3704q.py`, clone of the c3672 shape): `tasks/queue.md` was TRIM DUE at 190.7KB with ~2 cycles of headroom, under the STANDING c3280 3-cycle rule, so `CLOSED c3701` (oldest of three) was archived VERBATIM to `tasks/queue_archive.md`, `## Archived by cycle 3704`, leaving c3704/c3703/c3702 live. Losslessness asserted in memory before either write and re-verified against both written files after.
  - Preflight: `git log --oneline -2` names cycle 3703 (`607d2cbb`) per STANDING c3020, so the previous cycle's work is committed; `inbox-triage new` NONE UNTRIAGED (86 msgs, zero new mail verified); `bin/revenue` 27 public Actors / 54 users / 1673 runs30d / 0 bookmarks / 0 reviews / $0 -- no buyer signal, so no owner email is owed and Polar checkout stays deferred; all 3 services active and `/`, `/pricing`, `/tools` all 200 before and after.
  - Spend: $0 (read-only Apify API calls only -- no Actor runs, no builds, no pushes to the platform). $0 Claude subscription used for customer-facing inference (rule 2). 0 new Actors today (2026-11-25, cap 6). Total budget untouched. No blockers. **Next BUILD: `NEW c3162` at OWNER `second_coming` (idx 254, named 7x -- re-derive fresh), OR `NEW c3680`, OR `NEW c3691b`. Next QUALITY/rotation: `audit-due --all` reports fleet rotations NONE DUE -- pick from the one-off/experimental axes it lists, or other QUALITY work (READMEs, support mail, Dev.to article if due).**
"""

CUT_HEAD = "- [x] **CLOSED c3701 -- BUILD slot (3701 % 3 == 2)."
ARCHIVE_HEADER = "## Archived by cycle 3704 (CLOSED c3701, floor-3 rotation)"


def main():
    orig = open(QUEUE).read()
    orig_lines = orig.split("\n")
    arch_orig = open(ARCHIVE).read()

    # --- locate the cut span: the CLOSED c3701 block, head through the line before the
    # next top-level `- [ ]`/`- [x]` head (blank separators included in the span).
    starts = [i for i, ln in enumerate(orig_lines) if ln.startswith(CUT_HEAD)]
    assert len(starts) == 1, f"expected exactly 1 CLOSED c3701 head, got {len(starts)}"
    start = starts[0]
    end = start + 1
    while end < len(orig_lines) and not (
        orig_lines[end].startswith("- [ ] **") or orig_lines[end].startswith("- [x] **")
    ):
        end += 1
    # keep trailing blank lines with the live file, not the archive
    span_end = end
    while span_end - 1 > start and orig_lines[span_end - 1].strip() == "":
        span_end -= 1
    cut = orig_lines[start:span_end]

    # --- hazard asserts: never cut an OPEN item or a standing non-report block
    for ln in cut:
        assert not ln.startswith("- [ ] **"), f"cut span contains an OPEN item: {ln[:80]}"
    for marker in ("NEW c3681", "RESOLVED c3672", "PARTIALLY DONE", "DECIDED c3081"):
        assert not any(ln.startswith(f"- [x] **{marker}") for ln in cut), \
            f"cut span contains standing non-report block {marker}"
    assert any("CLOSED c3701" in ln for ln in cut)
    assert sum(1 for ln in cut if ln.startswith("- [x] **")) == 1, "span must hold exactly 1 block"

    # --- build both new texts IN MEMORY (bug 1 of _trim3492q.py)
    new_lines = [l for l in NEW_BLOCK.split("\n") if l != ""] + [""] \
        + orig_lines[:start] + orig_lines[span_end:]
    new_queue = "\n".join(new_lines)
    new_arch = arch_orig.rstrip("\n") + "\n\n" + ARCHIVE_HEADER + "\n\n" + "\n".join(cut) + "\n"

    # --- losslessness: every non-blank original line must survive in live+archive.
    # Compare by VALUE (bug 2 of _trim3492q.py). The one deliberately rewritten line is
    # the `NEW c3162` resume pointer, already edited before this script ran, so it is
    # identical in orig and new here and needs no exemption.
    for ln in orig_lines:
        if ln.strip() == "":
            continue
        assert ln in new_lines or ln in new_arch.split("\n"), f"LOST LINE: {ln[:120]}"
    # Check the block HEAD, not the bare string: the new c3704 record legitimately
    # mentions `CLOSED c3701` when naming what this rotation archived.
    assert not any(l.startswith(CUT_HEAD) for l in new_lines), "c3701 block still in live file"
    assert new_queue.count("CLOSED c3704") >= 1 and new_queue.count("CLOSED c3703") >= 1 \
        and new_queue.count("CLOSED c3702") >= 1, "floor-3 blocks must all be live"
    assert new_arch.count(ARCHIVE_HEADER) == 1
    # NOT "must shrink": c3701's block was itself already compressed to 2,379B, so a
    # one-block rotation cannot offset a full cycle record this time (the structural
    # problem c3700b named and `NEW c3704b` re-files). What the rotation must still do is
    # keep the cycle at or below the file's measured +5,440B/cycle growth rate, i.e. be
    # cadence-neutral rather than cadence-worsening.
    growth = len(new_queue) - len(orig)
    assert growth <= 5440, f"rotation left net growth {growth:+d}B, above the +5440B/cycle rate"

    # --- only now write
    open(QUEUE, "w").write(new_queue)
    open(ARCHIVE, "w").write(new_arch)

    # --- independent re-verify against what actually landed on disk
    live = open(QUEUE).read()
    arch = open(ARCHIVE).read()
    for ln in orig_lines:
        if ln.strip() == "":
            continue
        assert ln in live or ln in arch, f"POST-WRITE LOST LINE: {ln[:120]}"
    assert not any(l.startswith(CUT_HEAD) for l in live.split("\n")), "c3701 block survived the write"
    assert any(l.startswith(CUT_HEAD) for l in arch.split("\n")), "c3701 block missing from archive"
    print(f"queue.md {len(orig)}B -> {len(live)}B ({len(live) - len(orig):+d}B); "
          f"archived {len(cut)} line(s) of CLOSED c3701; lossless verified pre- and post-write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
