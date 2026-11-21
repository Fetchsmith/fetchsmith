"""c3540 tasks/queue.md trim -- THREE levers in one pass (clone of bin/_trim3537q.py).

Per NEW c3492 lesson (1): every assert runs against IN-MEMORY strings; files are
opened for writing only after all checks pass.

Levers, applied high-line-number first so earlier indices never shift:
  (1) RELOCATION  -- the `FOLLOW-UP from c2380` one-term-diff METHOD (two contiguous
      spans, L867-874 "HOW TO DERIVE STALEST" and L880-907 the tight-pattern lesson +
      the fleet-general 8-step method) moves VERBATIM to notes/PLAYBOOK.md. Live state
      (the 8-niche applied list, the fallback gate, the backoff counter) stays in
      queue.md with a pointer. This is the c3531/MERGED-c2916 split-relocation shape,
      and it satisfies c3534's condition (the moved text is pure transferable method;
      nothing dated or actively-tracked moves). c3046/c2994/c2336 stay REJECTED.
  (2) DE-DUPE    -- COMPRESSED c2994 carries the `+7 CLOSED c3316` paragraph TWICE
      (L358-362 is a truncated near-duplicate that ends on a dangling colon; L363+ is
      the complete one). Drop the truncated copy; it is archived verbatim anyway so the
      lossless check stays exact.
  (3) ROTATION   -- STANDING RULE 6b newest-5 floor: 8 report-shaped `CLOSED c3`
      headers live (c3532..c3539; standing one-offs c3329/c3336/c3496 and the combined
      c3518/c3520/c3529 handle note excluded, same derivation as c3537). Archive the
      oldest 3 (c3534, c3533, c3532, newest-first), keep c3535..c3539.

Usage: python bin/_trim3540q.py [--write]
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
PLAYBOOK = 'notes/PLAYBOOK.md'

with open(QUEUE) as f:
    lines = f.readlines()
orig_len = len(lines)
orig_bytes = sum(len(l) for l in lines)

# ---------------------------------------------------------------- lever 1 spans
# 0-indexed slices; 1-indexed L867-874 and L880-907.
M1A, M1B = 866, 874          # "HOW TO DERIVE STALEST" .. the 1344c-cap sentence
M2A, M2B = 879, 906          # "Use the TIGHT pattern" .. the final step-(8) sentence
method_a = lines[M1A:M1B]
method_b = lines[M2A:M2B]

assert method_a[0].lstrip().startswith('**HOW TO DERIVE "STALEST"'), method_a[0][:70]
assert method_a[-1].rstrip().endswith("(`BASE * 2**min(streak,2)`)."), method_a[-1][-40:]
assert method_b[0].lstrip().startswith('Use the TIGHT pattern'), method_b[0][:70]
assert method_b[-1].rstrip().endswith('that is the `audit-due` beat and stays on its cadence.'), method_b[-1][-60:]
# boundaries that must survive untouched in queue.md
assert lines[M1A - 1].lstrip().startswith('re-check on a ~8-10 day'), lines[M1A - 1][:60]
assert lines[M1B].lstrip().startswith('**Gate: do not pick this rotation'), lines[M1B][:60]
assert lines[M2A - 1].lstrip().startswith('EMPTY: five consecutive 0-candidate reads'), lines[M2A - 1][:60]
assert M2B == len(lines) or lines[M2B].strip() == '' or lines[M2B].startswith('- ['), repr(lines[M2B][:60])

POINTER = ("      **METHOD RELOCATED c3540 to `notes/PLAYBOOK.md`, "
    "`## One-term-diff pass: how to derive \"stalest\" and the 8-step per-niche method` "
    "(verbatim).** Read it there before running one: it holds the `max(last one-term pass, "
    "audit_dates.json competitor_audit)` staleness rule (and why a NONE DUE on a 1341c gap "
    "is correct), the TIGHT vs loose matched-count grep pattern, and the 8 numbered sweep "
    "steps. Only the live state above stays here.\n")

# ---------------------------------------------------------------- lever 2 span
D1A, D1B = 357, 362          # 1-indexed L358-362, the truncated duplicate
dupe = lines[D1A:D1B]
assert dupe[0].lstrip().startswith('**+7 CLOSED c3316, all TRUE / 0 edits -- total now 79/137.** Ran on the back of the'), dupe[0][:90]
assert dupe[-1].rstrip().endswith('counts in STATUS.md c3316):'), dupe[-1][-40:]
# the surviving complete copy must start on the very next line
assert lines[D1B].lstrip().startswith('**+7 CLOSED c3316, all TRUE / 0 edits -- total now 79/137.** Ran on the back of'), lines[D1B][:90]
assert lines[D1A - 1].lstrip().startswith('line-number shift re-flagging the same 5.'), lines[D1A - 1][:60]

# ---------------------------------------------------------------- lever 3 span
R1A, R1B = 29, 41            # 1-indexed L30-41
rot = lines[R1A:R1B]
assert rot[0].startswith('- [x] **CLOSED c3534'), rot[0][:60]
assert rot[5] == '\n', repr(rot[5])
assert rot[6].startswith('- [x] **CLOSED c3533'), rot[6][:60]
assert rot[7].startswith('- [x] **CLOSED c3532'), rot[7][:60]
assert rot[11] == '\n', repr(rot[11])
assert lines[R1A - 1] == '\n', repr(lines[R1A - 1])
assert lines[R1B].startswith('- [ ] **NEW c3523'), lines[R1B][:60]   # open item, untouched

# ---------------------------------------------------------------- rebuild queue
new_lines = (lines[:R1A] + lines[R1B:D1A] + lines[D1B:M1A] + [POINTER]
             + lines[M1B:M2A] + lines[M2B:])

# ---------------------------------------------------------------- archive text
arch_add = (
    "\n## Archived by cycle 3540 (from tasks/queue.md: three levers -- "
    "(1) the 3 oldest cycle-report blocks under the STANDING RULE 6b newest-5 floor "
    "(c3534, c3533, c3532, newest-first); (2) the truncated DUPLICATE `+7 CLOSED c3316` "
    "paragraph removed from `COMPRESSED c2994` in place -- the complete copy stays LIVE in "
    "tasks/queue.md, this is the redundant one; (3) the `FOLLOW-UP from c2380` one-term-diff "
    "METHOD, which is NOT lost -- it is verbatim in notes/PLAYBOOK.md under "
    "`## One-term-diff pass: how to derive \"stalest\" and the 8-step per-niche method`, "
    "copied here only so this file stays a lossless record of every line cut.)\n\n"
    "### (1) Rotated cycle-report blocks c3534, c3533, c3532\n\n"
    + ''.join(rot) +
    "\n### (2) Truncated duplicate `+7 CLOSED c3316` paragraph cut from `COMPRESSED c2994`\n\n"
    + ''.join(dupe) +
    "\n### (3) One-term-diff METHOD relocated to notes/PLAYBOOK.md\n\n"
    + ''.join(method_a) + ''.join(method_b)
)

# ---------------------------------------------------------------- playbook text
pb_add = (
    "\n## One-term-diff pass: how to derive \"stalest\" and the 8-step per-niche method "
    "(RELOCATED here by cycle 3540 from `FOLLOW-UP from c2380` in `tasks/queue.md`, where it "
    "had lived since c2380, COMPRESSED c2784)\n\n"
    "RELOCATED because it is reusable METHOD for running a cheap one-term competitor diff over "
    "one niche, not a task -- the c3360/c3492/c3498/c3531 lever (relocate method verbatim, "
    "leave a one-line pointer) that is the only one which has ever produced a lasting cut on "
    "`tasks/queue.md`, and it meets c3534's condition that only pure transferable method may "
    "move: the block's LIVE state (the 8 niches already swept, the `audit-due competitor_audit` "
    "384c+ fallback gate, and the companion matched-count grep's five-read EMPTY backoff "
    "counter) stays in `tasks/queue.md` under the `FOLLOW-UP from c2380` pointer. Text below is "
    "verbatim as it stood at c3540. Per-niche execution detail remains in `notes/LEARNINGS.md` "
    "cycles 2384/2730/2735/2737/2738 and `tasks/queue_archive.md` c2685/c2736/c2766; the "
    "pre-compression narrative is under the c2784 header. **One pointer inside the text below "
    "does NOT resolve in either file and was ALREADY dangling before this relocation (hazard "
    "pass (c), c3540):** step (8)'s \"see the dedicated c2384 follow-up above\" -- that block "
    "(`NEW follow-up (c2384)`, the trademark-search README one-word-drift note) was archived to "
    "`tasks/queue_archive.md`, `## Archived by cycle 2387`. Left unedited to keep this text "
    "verbatim, same convention as `NEW c3492`'s archived-pointer ruling.\n\n"
    + ''.join(method_a) + ''.join(method_b)
)

with open(ARCHIVE) as f:
    arch_text = f.read()
new_arch_text = arch_text.rstrip('\n') + '\n' + arch_add

with open(PLAYBOOK) as f:
    pb_text = f.read()
new_pb_text = pb_text.rstrip('\n') + '\n' + pb_add

# ---------------------------------------------------------------- lossless checks
cut_all = rot + dupe + method_a + method_b
assert len(new_lines) == orig_len - len(cut_all) + 1, (len(new_lines), orig_len, len(cut_all))

# every non-blank cut line must survive in the archive addition
missing = [l for l in cut_all if l.strip() and l not in arch_add]
assert not missing, f"LOSSY vs archive: {len(missing)} missing -- {missing[:2]}"
# every non-blank relocated METHOD line must ALSO survive in the playbook addition
missing_pb = [l for l in (method_a + method_b) if l.strip() and l not in pb_add]
assert not missing_pb, f"LOSSY vs playbook: {len(missing_pb)} missing -- {missing_pb[:2]}"
# and every non-blank ORIGINAL line must be findable in new queue + archive addition
new_q_text = ''.join(new_lines)
orphan = [l for l in lines if l.strip() and l not in new_q_text and l not in arch_add]
assert not orphan, f"ORPHANED: {len(orphan)} -- {orphan[:2]}"

new_bytes = sum(len(l) for l in new_lines)
print(f"queue.md {orig_bytes/1024:.1f}KB/{orig_len}ln -> {new_bytes/1024:.1f}KB/{len(new_lines)}ln "
      f"(-{(orig_bytes-new_bytes)/1024:.1f}KB)")
print(f"  lever 1 relocation: {sum(len(l) for l in method_a+method_b)}B method -> PLAYBOOK "
      f"(+{len(pb_add)}B there), {len(POINTER)}B pointer kept")
print(f"  lever 2 de-dupe:    {sum(len(l) for l in dupe)}B truncated duplicate")
print(f"  lever 3 rotation:   {sum(len(l) for l in rot)}B (c3534/c3533/c3532)")
print(f"  archive +{len(arch_add)}B; all lossless asserts PASSED")

if '--write' not in sys.argv:
    print("DRY RUN -- pass --write to commit")
    sys.exit(0)

with open(ARCHIVE, 'w') as f:
    f.write(new_arch_text)
with open(PLAYBOOK, 'w') as f:
    f.write(new_pb_text)
with open(QUEUE, 'w') as f:
    f.write(new_q_text)
print("WROTE queue.md, queue_archive.md, notes/PLAYBOOK.md")
