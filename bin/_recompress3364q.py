#!/root/agent/venv/bin/python
"""Recompress the 2 vendor-catalogue tracker entries that check-doc-size's new
ENTRY_CAP warning named at cycle 3364: c3354 (553B) and c3361 (613B).

This is NOT an archive trim -- it is the style fix the checker names. Both batches'
full narrative is already in state/STATUS.md (4 mentions each, verified before this
ran), and c3354's is also in tasks/queue_archive.md, so compressing the queue copy
loses no record.

ONE THING IS NOT BATCH NARRATIVE and is therefore RELOCATED, not dropped: c3354's
closing claim that exact-handle grep has returned 0 hits fleet-wide for every handle
in every batch since c3297. That is reusable method (it says the grep step is cheap
confirmation, not a filter), it existed ONLY on this line -- grep -c '0 hits
fleet-wide' was 1 in queue.md and 0 in STATUS.md and LEARNINGS.md -- and deleting it
would lose it. It moves up into the tracker's own method area, the same treatment
c3360 gave the standing ruling buckets when it relocated them to PLAYBOOK.md.
"""
import re
import sys

PATH = "/root/agent/tasks/queue.md"

OLD_C3354 = (
    "c3354 rows 383-388: 0/6, 4 vendors (3 bucket 2 -- a Brazil company-registry "
    "mistagged into the `federal-register-scraper` niche, a BuiltWith-style "
    "tech-stack/lead-gen tool, a per-company hiring-signal watch; 1 bucket 1 "
    "remote-jobs at 4 of our 7 boards; 1 flat-$0.0002 HN that ties our FREE tier "
    "and is dearer at every paid rung; 1 dearer sec-insider-trades). **Exact-handle "
    "grep has returned 0 hits fleet-wide for every handle in every batch since "
    "c3297 -- the catalogue is genuinely all-new handles, so that step is cheap "
    "confirmation, not a filter.** "
)
NEW_C3354 = (
    "c3354 rows 383-388: 0/6, 4 vendors (3 bucket 2 -- Brazil company-registry "
    "mistagged into the `federal-register-scraper` niche, BuiltWith-style lead-gen, "
    "per-company hiring-signal watch; 1 bucket 1 remote-jobs at 4 of our 7 boards; "
    "1 flat-$0.0002 HN tying our FREE tier, dearer at every paid rung; 1 dearer "
    "sec-insider-trades). "
)

OLD_C3361 = (
    "c3361 rows 407-412: 0/6, all `automation_studio` except one (2 "
    "dearer-at-every-tier $0.005->$0.003 vs our $0.0035->$0.0024 and flat $0.0018; "
    "1 bucket 1 scope-excluded 4-of-12-ATS job board, also dearer; 1 "
    "tied-at-best/dearer-primary CourtListener split-event clone (metadata ties our "
    "flat $0.002, full-text opinions at $0.005 are 2.5x dearer, no tier beats us); "
    "2 bucket 2 category mismatches -- a PI/sponsor-contact lead-gen product "
    "explicitly reselling PII, the exact already-excluded shape, and a Shopify-App-"
    "Store review-churn tool mistagged against Apple's App Store on \"app store "
    "reviews\" vocabulary alone)."
)
NEW_C3361 = (
    "c3361 rows 407-412: 0/6, all `automation_studio` bar one (2 "
    "dearer-at-every-tier; 1 bucket 1 scope-excluded 4-of-12-ATS board, also "
    "dearer; 1 tied-at-best CourtListener split-event clone, no tier beats us; 2 "
    "bucket 2 -- a PII-reselling lead-gen tool and a Shopify-App-Store tool "
    "mistagged on \"app store reviews\" vocabulary)."
)

# Where the relocated method sentence lands: appended to the tracker's own
# STANDING RULING BUCKETS line, which is already the block's method home.
BUCKETS_ANCHOR = "**STANDING RULING BUCKETS -- RELOCATED c3360 to `notes/PLAYBOOK.md`"
RELOCATED = (
    " **Exact-handle grep (RELOCATED c3364 off the per-batch line, where it was the "
    "only copy): it has returned 0 hits fleet-wide for every handle in every batch "
    "since c3297 -- the catalogue is genuinely all-new handles, so that step is "
    "cheap confirmation, not a filter.**"
)


def main():
    with open(PATH, encoding="utf-8") as f:
        text = f.read()
    before = len(text.encode("utf-8"))

    for old in (OLD_C3354, OLD_C3361):
        if text.count(old) != 1:
            print(f"ABORT: expected exactly 1 occurrence, got {text.count(old)}:\n{old[:80]!r}")
            return 1
    lines = text.split("\n")
    anchors = [i for i, ln in enumerate(lines) if BUCKETS_ANCHOR in ln]
    if len(anchors) != 1:
        print(f"ABORT: buckets anchor matched {len(anchors)} lines, want 1")
        return 1

    text = text.replace(OLD_C3354, NEW_C3354).replace(OLD_C3361, NEW_C3361)
    lines = text.split("\n")
    i = anchors[0]
    lines[i] = lines[i].rstrip() + RELOCATED
    text = "\n".join(lines)

    # Losslessness: the relocated method sentence must still be present, and no
    # NAMED FIND (the reliable record per the tracker's own running-score note) may
    # be dropped from either entry.
    assert "0 hits fleet-wide for every handle in every batch since c3297" in text
    for keep in ("automation_studio", "CourtListener", "sec-insider-trades",
                 "federal-register-scraper", "rows 383-388", "rows 407-412"):
        assert keep in text, keep

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(text)
    after = len(text.encode("utf-8"))
    print(f"queue.md {before} -> {after} B ({before - after:+d} reclaimed, net of "
          f"{len(RELOCATED)}B relocated method)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
