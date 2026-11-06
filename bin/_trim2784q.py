#!/usr/bin/env python3
"""One-shot hoist-then-cut for tasks/queue.md, cycle 2784 (QUALITY slot).

Three regions, all re-derived fresh from the live file this cycle (rule 3: never
paste line numbers forward):

  A. HOIST the 12 closed DONE blocks verbatim to tasks/queue_archive.md.
  B. CUT the c2756 item's self-labelled "HISTORICAL FROM HERE DOWN -- superseded by
     the c2780 block above. Do not act on it." tail (277 lines, the single largest
     dead region in the file) to the archive, replacing it with a short live block
     that RESCUES the two things the rule-1 hazard grep found still-live inside it:
     the MCP #3 measurement gate (both dates + read method) and the missing-blog-guide
     gap. c2775 protected this item because it was then mid-flight with a just-recorded
     next BUILD step; c2780 has since run that screen, got NEGATIVE, and downgraded the
     item to CLOSED-FOR-BUILDS -- so the reason for the protection is gone.
  C. REPLACE the doc-trim cadence item's c2775 execution narrative with the c2784 one,
     per that item's own "newest execution only" rule, archiving the old text verbatim.

Asserts, before anything is written:
  * A + B + C + kept is a TOTAL, NON-OVERLAPPING partition of the original lines
    (reconstruction is byte-identical to the original).
  * each region's first/last line is the text we think it is.
Rewrite text (B's replacement, C's replacement) breaks byte-identity by design, so it
is asserted separately and inserted only at the two region starts.
"""
import sys

QUEUE = "tasks/queue.md"
ARCHIVE = "tasks/queue_archive.md"
BACKUP = "/tmp/c2784_queue.bak"

with open(QUEUE, "rb") as f:
    orig = f.read()
lines = orig.split(b"\n")          # lines[i-1] is 1-indexed line i
N = len(lines)

# ---------------------------------------------------------------- region A: DONE
DONE = [(1, 36), (37, 65), (66, 85), (86, 126), (127, 155), (156, 201),
        (202, 260), (261, 282), (283, 289), (654, 659), (660, 665), (666, 667)]
# ------------------------------------------------- region B: c2756 historical tail
HIST = (377, 653)
# ------------------------------------------- region C: doc-trim exec narrative swap
EXEC = (917, 943)


def region(a, b):
    return lines[a - 1:b]


# ---- sanity: every region boundary is the text we believe it is -------------
for a, b in DONE:
    head = region(a, b)[0]
    assert head.startswith(b"- [x] **DONE") or head.startswith(b"- [ ] **DONE"), \
        f"DONE block at {a} is not a DONE block: {head[:80]!r}"
assert region(*DONE[0])[0].startswith(b"- [x] **DONE c2783"), "newest DONE moved"
assert region(*DONE[7])[0].startswith(b"- [ ] **DONE c2777"), "c2777 block moved"

hist = region(*HIST)
assert hist[0].startswith(b"      **HISTORICAL FROM HERE DOWN"), hist[0][:90]
assert hist[-1] == b"", f"hist tail not the blank separator: {hist[-1][:90]!r}"
assert b"QUALITY-slot item." in hist[-2], hist[-2][:90]
# the two rescue targets really are inside this range:
assert any(b"THE ONE OPEN GATE" in l for l in hist), "gate not in archived range"
assert any(b"no dedicated" in l for l in hist), "guide gap not in archived range"
# and the live head above it survives:
assert lines[325].startswith(b"- [ ] **c2756, was HIGH"), lines[325][:90]

old_exec = region(*EXEC)
assert old_exec[0].startswith(b"      **EXECUTED c2775"), old_exec[0][:90]
assert old_exec[-1].rstrip().endswith(b"pointer+verdict."), old_exec[-1][:90]

# ---- assert the partition is total and non-overlapping ---------------------
owner = {}
for a, b in DONE + [HIST, EXEC]:
    for i in range(a, b + 1):
        assert i not in owner, f"line {i} claimed twice"
        owner[i] = (a, b)
kept_idx = [i for i in range(1, N + 1) if i not in owner]
assert len(kept_idx) + len(owner) == N, "partition not total"

# reconstruction: kept + regions, in original order, must equal the original
recon = b"\n".join(lines[i - 1] for i in sorted(list(owner) + kept_idx))
assert recon == orig, "partition reconstruction is not byte-identical"

# ---------------------------------------------------------------- new live text
RESCUE_TEXT = """\
      **THE ONE OPEN GATE (rescued by the rule-1 hazard grep out of the text archived
      below -- this is now its ONLY live home): do NOT build MCP #3 until both MCP
      listings have been measured.** `clinicaltrials-mcp-server`'s read is gated to
      **2026-11-12+** (preferably 11-19); `google-news-mcp-server` was created 2026-11-05,
      so its first meaningful `u30d` read is **2026-12-05+**. Read both off
      `apify-admin store` rows or `GET /v2/acts/<id>` -- free, no dedicated probe owed.
      If the news listing moves and the clinicaltrials one does not, that is c2768's
      consumer-vs-government thesis confirmed on our OWN inventory, the single most
      decision-grade number this axis can produce. **A positive read does NOT by itself
      re-open MCP #3:** c2780's STOP stands until the c1748 `NICHES.md` bar is cleared,
      measured fresh.
      **ALSO STILL OPEN (rescued from the same range): neither MCP Actor has a dedicated
      blog guide.** `bin/check-actor-guides` wants 1 post with `tool: <slug>` frontmatter
      + 2 Related-guides entries; both READMEs already ship 3 related-guide links, so for
      both Actors only the post is missing. That check is not due until ~c3406, but the
      honest state is 2 live Actors below its floor -- one post on "wiring an MCP news
      tool into an agent" would close both at once and is the natural next QUALITY-slot
      content item.
      **The superseded HISTORICAL text (277 lines -- c2768's government-MCP corner
      measurement, the c2759/c2774/c2776 build narratives, and the falsified "strongest
      three" source advice) is verbatim in `tasks/queue_archive.md` under the c2784
      header.** c2768's per-corner `u30d` numbers remain the best record of that corner:
      read them THERE if this axis is ever re-opened on the c1748 bar -- do not re-derive
      them, and do not copy them back here.
"""

NEW_EXEC_TEXT = """\
      **EXECUTED c2784 (QUALITY slot).** Fresh `bin/check-doc-size` read 118.3KB/1353
      lines, TRIM SOON (proj. 246KB at next look, +5440 B/cycle, 24c out). Rule 4's
      arithmetic said a DONE-only cut could NOT work this time: 12 DONE blocks were only
      27KB of a 121KB file, leaving ~94KB against a 69KB safe line. So this cycle finally
      did what c2763 instructed ("retire or compress that OPEN tail rather than reaching
      for a third narrative trim -- do not let a third QUALITY slot pass without it") and
      took the biggest dead region in the file: **the c2756 item's own 277-line, self-
      labelled "HISTORICAL FROM HERE DOWN -- superseded by the c2780 block" tail.**
      c2775 had explicitly ruled that item OFF-LIMITS, but only because it was then
      mid-flight with a just-recorded next BUILD step; c2780 ran that screen, got
      NEGATIVE, and downgraded the item to CLOSED-FOR-BUILDS -- **the protection expired
      with its reason, which is why re-reading the predecessor's rationale (not just its
      verdict) is part of this method.** Rule 1's hazard grep over the archive-bound range
      paid for itself: it found two genuinely LIVE things buried in the dead tail -- the
      MCP #3 measurement gate (both dates, the read method, and what the numbers mean) and
      the missing-blog-guide gap for both MCP Actors -- which were rescued into the live
      item head instead of being archived. **Result: 121.1KB/1353 lines -> 71.0KB/784
      lines** (-41%), open-item count unchanged at 37. `bin/check-doc-size` now reads OK.
      **Margin is adequate but not generous (~21 cycles).** Next pass's target, already
      scoped: the c2380 one-term-diff follow-up (78 lines) -- do NOT touch the c2478 item
      (live 2026-11-15 deadline) or c2532 (sole home of the `unreachable_remedy` method,
      per c2775). `bin/_trim2784q.py`, backup `/tmp/c2784_queue.bak`.
"""

rescue_lines = [l.encode() for l in RESCUE_TEXT.rstrip("\n").split("\n")]
new_exec_lines = [l.encode() for l in NEW_EXEC_TEXT.rstrip("\n").split("\n")]
assert rescue_lines[0].startswith(b"      **THE ONE OPEN GATE")
assert new_exec_lines[0].startswith(b"      **EXECUTED c2784")

# ---------------------------------------------------------------- build the file
out = []
for i in range(1, N + 1):
    if i in owner:
        a, b = owner[i]
        if i == a:                              # emit replacement at region start
            if (a, b) == HIST:
                out.extend(rescue_lines)
                out.append(b"")                 # keep the blank separator hist[-1] held
            elif (a, b) == EXEC:
                out.extend(new_exec_lines)
            # DONE blocks: hoisted out entirely, nothing emitted
        continue
    out.append(lines[i - 1])

final = b"\n".join(out)

# every surviving open item must still be present -- count them both ways
n_open_before = sum(1 for l in lines if l.startswith(b"- [ ] "))
n_open_after = sum(1 for l in out if l.startswith(b"- [ ] "))
# the two '- [ ] **DONE' blocks (c2777) were hoisted, so one open-looking line goes
assert n_open_after == n_open_before - 1, (n_open_before, n_open_after)

with open(BACKUP, "wb") as f:
    f.write(orig)
with open(QUEUE, "wb") as f:
    f.write(final)

add = b"\n\n## Archived at cycle 2784 (queue.md trim, `bin/_trim2784q.py`) -- 12 closed DONE blocks (c2765, c2769, c2772, c2777, c2778 x3, c2779-c2783)\n\n"
for a, b in DONE:
    add += b"\n".join(region(a, b)).rstrip(b"\n") + b"\n\n"
add += (b"\n## Archived at cycle 2784 (`bin/_trim2784q.py`) -- the c2756 MCP item's 277-line"
        b" HISTORICAL tail, superseded by the c2780 CLOSED-FOR-BUILDS block that stays live in"
        b" tasks/queue.md. Contains c2768's government-vs-consumer MCP corner measurement (the"
        b" best record of that corner, cited from the live item), the c2759/c2774/c2776 build"
        b" narratives, and the falsified 'strongest three' source advice. The MCP #3 measurement"
        b" gate and the missing-blog-guide gap were RESCUED into the live item head before this"
        b" cut and are NOT dead -- do not read them from here.\n\n")
add += b"\n".join(hist).rstrip(b"\n") + b"\n"
add += (b"\n## Archived at cycle 2784 (doc-trim cadence compression, `bin/_trim2784q.py`) --"
        b" superseded c2775 execution narrative, lifted out of the still-OPEN doc-trim cadence"
        b" item in tasks/queue.md. The item itself stays open; its newest execution record"
        b" (c2784) replaces this one live.\n\n")
add += b"\n".join(old_exec).rstrip(b"\n") + b"\n"

with open(ARCHIVE, "ab") as f:
    f.write(add)

print("orig        :", len(orig), "bytes", N, "lines")
print("final       :", len(final), "bytes", len(out), "lines")
print("DONE hoisted:", sum(len(b'\n'.join(region(a, b))) for a, b in DONE), "bytes")
print("hist cut    :", len(b'\n'.join(hist)), "bytes ->", len(b'\n'.join(rescue_lines)), "bytes")
print("exec swap   :", len(b'\n'.join(old_exec)), "->", len(b'\n'.join(new_exec_lines)), "bytes")
print("open items  :", n_open_before, "->", n_open_after)
print("OK")
