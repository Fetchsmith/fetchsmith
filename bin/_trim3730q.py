#!/root/agent/venv/bin/python
"""Cycle 3730 floor-3 tasks/queue.md rotation: archive CLOSED c3725 (oldest of the
4 live CLOSED blocks: c3730/c3729/c3726/c3725), restoring the floor of 3. Checked
first for nested `  - **NEW cNNNN` sub-bullets inside the span per the c3724 lesson --
0 found (the two `NEW c3162` hits in the span are inline prose references to the
standing tracker, not nested sub-bullet item headers). Lossless multiset-verified
before writing.
"""
import re

PATH = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(PATH) as f:
    text = f.read()

m = re.search(r"(- \[x\] \*\*CLOSED c3725.*?)\n\n---\n", text, re.S)
assert m, "CLOSED c3725 span not found"
span = m.group(1)
assert not re.search(r"^\s+- \*\*NEW c\d+", span, re.M), "nested NEW item found, abort"

before_lines = sorted(l for l in text.splitlines() if l.strip())
new_text = re.sub(r"\n{3,}", "\n\n", text[: m.start(1)] + text[m.end(1) :])
after_lines = sorted(l for l in new_text.splitlines() if l.strip())
archived_lines = sorted(l for l in span.splitlines() if l.strip())

assert sorted(after_lines + archived_lines) == before_lines, "lossless check FAILED"

with open(PATH, "w") as f:
    f.write(new_text)

with open(ARCHIVE) as f:
    arch = f.read()
with open(ARCHIVE, "w") as f:
    f.write(
        "## Archived by cycle 3730 (CLOSED c3725, floor-3 rotation)\n\n"
        + span.rstrip()
        + "\n\n"
        + arch
    )

print("OK: archived CLOSED c3725, lossless-verified.")
