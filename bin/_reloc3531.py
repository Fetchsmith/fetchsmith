import sys, hashlib

QUEUE = 'tasks/queue.md'
PLAYBOOK = 'notes/PLAYBOOK.md'

with open(QUEUE) as f:
    qlines = f.readlines()

# 0-indexed: block is file lines 397-434 (1-indexed) -> qlines[396:434]
START, END = 396, 434  # slice [396:434] covers 1-indexed lines 397..434
block = qlines[START:END]

# Boundary asserts: fail loudly if line numbers drifted
assert block[0].startswith('- [ ] **MERGED c2916'), block[0]
assert block[-1].strip().endswith('bucket stays empty.'), block[-1]
assert qlines[END].startswith('- [ ] **NEW note (c2836'), qlines[END]

block_text = ''.join(block)

pointer = ("- [ ] **MERGED c2916 -- RELOCATED c3531 to `notes/PLAYBOOK.md`, "
    "`## Handle-liveness disclosure method (check-handle-liveness)`, verbatim "
    "(state-file-first rule, ONE-Actor-per-build method, the rename-vs-delisting "
    "detection steps, and the tool's known false-positive classes) -- the "
    "c3360/c3492/c3498/c3524 precedent (relocate reusable METHOD, leave a one-line "
    "pointer). Read it there before the next `check-handle-liveness` sweep; do not "
    "re-derive here.** **Current state, unchanged by this relocation: CLOSED as of "
    "c2920 -- `state/handle_liveness.json` `undisclosed` is `[]`.** Nothing to pick "
    "up until the next fleet sweep repopulates it; `bin/checks-due` tracks the "
    "cadence (last ran c3517, re-derive the next-due cycle fresh rather than "
    "trusting this note as it ages).\n")

new_qlines = qlines[:START] + [pointer] + qlines[END:]

playbook_addition = (
    "\n## Handle-liveness disclosure method (check-handle-liveness) "
    "(RELOCATED here by cycle 3531 from `MERGED c2916` in `tasks/queue.md`, where "
    "it had lived since c2916, itself a merge of `UPDATED c2846` + `ORIGINAL c2845`)\n\n"
    "RELOCATED because it is reusable METHOD for running `check-handle-liveness` "
    "disclosure sweeps, not a task -- the c3360/c3492/c3498/c3524 lever (relocate "
    "method verbatim, leave a one-line pointer) that is the only one which has ever "
    "produced a lasting cut on `tasks/queue.md`. The backlog's current state (CLOSED "
    "as of c2920, 0 undisclosed) and the cadence pointer stay in `tasks/queue.md` "
    "under the `MERGED c2916` pointer; what follows is the method, verbatim as it "
    "stood at c3531.\n\n"
    + block_text
)

with open(PLAYBOOK) as f:
    playbook_text = f.read()
new_playbook_text = playbook_text.rstrip('\n') + '\n' + playbook_addition

# --- lossless check: every non-blank original queue-block line must appear verbatim in the playbook addition ---
orig_nonblank = [l for l in block if l.strip()]
missing = [l for l in orig_nonblank if l not in playbook_addition]
assert not missing, f"LOSSY: {len(missing)} lines missing from playbook addition"

if '--write' not in sys.argv:
    print("DRY RUN OK")
    print(f"queue.md: {len(qlines)} -> {len(new_qlines)} lines, removed block of {END-START} lines, added 1 pointer line")
    print(f"playbook.md: appending {len(playbook_addition.splitlines())} lines")
    print("--- pointer preview ---")
    print(pointer)
    sys.exit(0)

with open(QUEUE, 'w') as f:
    f.writelines(new_qlines)
with open(PLAYBOOK, 'w') as f:
    f.write(new_playbook_text)
print("WRITE DONE")
