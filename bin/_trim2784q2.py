#!/usr/bin/env python3
"""Second c2784 QUALITY-slot cut: compress the c2380 one-term-diff item's narrative.

Rule 4 follow-through -- after the main cut, `check-doc-size` still projected 197KB
against a 200KB line (a ~3KB margin), so an OPEN item gets compressed in the SAME
cycle rather than banking on the next pass. Target is the one c2775 scoped for this
slot (the c2380 follow-up), and only its DATED NARRATIVE half.

DELIBERATELY NOT ARCHIVED: the item's 8-step one-term-diff METHOD (the block from
"The c2380 lesson is fleet-general" to the end). LEARNINGS 2394-2428 carries the
*lessons* behind steps 6/7/8 but not the operational recipe (the `apify-admin store`
sweep, the `grep -qF "$handle"` diff, the `bin/_batch_price_<abbr>.py` /tmp handle-list
trick), so per rule 1 this file is its only home and it stays live, untouched.

Archived verbatim: lines 615-668 (roster + superseded c2779/c2780 measurement + the
c2739 re-grep narrative), replaced by a shorter block that keeps every live verdict.
"""
import sys

QUEUE = "tasks/queue.md"
ARCHIVE = "tasks/queue_archive.md"
BACKUP = "/tmp/c2784_queue2.bak"

with open(QUEUE, "rb") as f:
    orig = f.read()
lines = orig.split(b"\n")

NARR = (615, 668)                      # 1-indexed inclusive
narr = lines[NARR[0] - 1:NARR[1]]

assert narr[0].startswith(b"- [ ] **FOLLOW-UP from c2380"), narr[0][:90]
assert narr[-1].rstrip().endswith(b"noise either."), narr[-1][:90]
# the method block must survive immediately after the replaced range:
assert lines[NARR[1]].startswith(b"      The c2380 lesson is fleet-general"), lines[NARR[1]][:90]
assert any(b"NEW at c2384" in l for l in lines[NARR[1]:NARR[1] + 25]), "method block moved"

NEW = """\
- [ ] **FOLLOW-UP from c2380 -- the one-term-diff pass. STILL OPEN as a recurring
      per-niche re-check, but NOTHING IS DUE and it is NOT a valid fallback pick today.
      (Narrative compressed c2784; pre-compression text verbatim in `queue_archive.md`
      under the c2784 header. Per-niche execution detail: `notes/LEARNINGS.md` cycles
      2384/2730/2735/2737/2738 and `queue_archive.md` c2685/c2736/c2766.)**
      **Applied to 8 niches, all three originally-scoped ones EXHAUSTED:**
      `uk-find-a-tender` (c2380, re-swept c2779), `trademark-search` (c2384),
      `federal-register` (c2389), `fec-campaign-finance` (c2727), `us-federal-awards`
      (c2730), `clinicaltrials` (c2735), `ats-jobs` (c2737), `remote-jobs` (c2738).
      Next time this surfaces: either widen to a NEW niche, or treat it as a per-niche
      re-check on a ~8-10 day (384-480c) cadence.
      **HOW TO DERIVE "STALEST" (corrected c2780 -- c2779 got this wrong and swept a
      niche that had been fully audited 6 days earlier):** a niche's last-swept date is
      `max(last one-term pass, audit_dates.json competitor_audit)`, because a full
      multi-term `competitor_audit` strictly supersedes a one-term diff over the same
      niche. **Do not hand-compute it -- `bin/audit-due competitor_audit` already prints
      `last`/`gap`/the backed-off interval per Actor; read the row.** Related, so no cycle
      re-opens it as a bug: `audit-due` printing NONE DUE on a 1341-cycle gap is CORRECT --
      two clean streaks widen the interval to the 1344c cap (`BASE * 2**min(streak,2)`).
      **Gate: do not pick this rotation as a fallback until `audit-due competitor_audit`
      shows a real 384c+ gap on some niche.** (Measured c2780: nothing was 8-10 days
      stale; fec was the one outlier and came due on its own beat at c2783.)
      **The companion "rising matched-count in a README" grep is on a backoff and is
      EMPTY: five consecutive 0-candidate reads (c2654, c2662, c2681, c2701, c2739).**
      Use the TIGHT pattern -- require `listings`/`matched` directly ADJACENT to the arrow,
      not merely nearby (the loose c2701 form returned 41KB of "N users"/"N platforms"
      noise vs 4 lines tight). Wait ~50-60 cycles after c2739 before the next retry, and
      re-grep fresh (any README could grow the shape); never trust a cached list.
"""

new_lines = [l.encode() for l in NEW.rstrip("\n").split("\n")]
assert new_lines[0].startswith(b"- [ ] **FOLLOW-UP from c2380")

final_lines = lines[:NARR[0] - 1] + new_lines + lines[NARR[1]:]
final = b"\n".join(final_lines)

# open-item count must be unchanged (we replaced one '- [ ] ' header with one header)
nb = sum(1 for l in lines if l.startswith(b"- [ ] "))
na = sum(1 for l in final_lines if l.startswith(b"- [ ] "))
assert nb == na, (nb, na)

# reconstruction: putting the old narrative back must restore the original exactly
recon = b"\n".join(lines[:NARR[0] - 1] + narr + lines[NARR[1]:])
assert recon == orig, "reconstruction mismatch"

with open(BACKUP, "wb") as f:
    f.write(orig)
with open(QUEUE, "wb") as f:
    f.write(final)

add = (b"\n\n## Archived at cycle 2784 (c2380 one-term-diff item narrative compression,"
       b" `bin/_trim2784q2.py`) -- the dated roster, the superseded c2779/c2780 staleness"
       b" measurement, and the c2739 re-grep narrative, lifted out of the still-OPEN c2380"
       b" item in tasks/queue.md. The item stays open and its 8-step METHOD block was"
       b" deliberately NOT archived (rule 1: tasks/queue.md is the method's only home).\n\n")
add += b"\n".join(narr).rstrip(b"\n") + b"\n"
with open(ARCHIVE, "ab") as f:
    f.write(add)

print("orig :", len(orig), "bytes", len(lines), "lines")
print("final:", len(final), "bytes", len(final_lines), "lines")
print("narrative:", len(b'\n'.join(narr)), "->", len(b'\n'.join(new_lines)), "bytes")
print("open items:", nb, "->", na)
print("OK")
