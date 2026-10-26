#!/usr/bin/env python3
"""Prototype for c2260's follow-up (queue.md): is a checker for "same number stated
twice with two different values" worth registering?

Scope per c2260: parse numeric claims out of each Actor's `.actor/input_schema.json`
descriptions and its `README.md`, and flag any claim where the SAME unit word (e.g.
"sites", "fields", "studies") appears attached to two DISAGREEING numbers somewhere
in that Actor's own docs. This is a measurement run only -- not registered in
state/fleet_checks.json. Prints every flagged (unit, numbers, locations) group so the
false-positive rate can be read off by hand before deciding whether to keep it.

Claim extraction: a number token followed within 2 words by a lowercase alpha word,
skipping filler words (of/or/more/plus/other/than/up/to/the/a/an/at/least/per/each/in).
Numbers under 2 or claims whose unit word is a pure stopword are dropped up front --
they produced the bulk of the noise in a first pass (e.g. "a 2-day window").
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILLER = {"of", "or", "more", "plus", "other", "than", "up", "to", "the", "a", "an",
          "at", "least", "per", "each", "in", "and", "is", "are", "with", "for"}

NUM = re.compile(r"\b(\d[\d,]*(?:\.\d+)?)\b")


def collect_schema_text(path):
    data = json.load(open(path))
    out = []
    props = data.get("properties", {})
    for key, spec in props.items():
        d = spec.get("description")
        if d:
            out.append((f"{key}.description", d))
    return out


def claims_in(text):
    """Yield (number_str, unit_word) for each number followed by a real unit word."""
    words = re.findall(r"\S+", text)
    # map each word's start char-ish index isn't needed; work token-wise instead.
    for i, tok in enumerate(words):
        m = NUM.fullmatch(tok.strip(".,;:()"))
        if not m:
            continue
        num = m.group(1)
        try:
            if float(num.replace(",", "")) < 2:
                continue
        except ValueError:
            continue
        unit = None
        for j in range(i + 1, min(i + 3, len(words))):
            w = re.sub(r"[^a-zA-Z]", "", words[j]).lower()
            if not w:
                continue
            if w in FILLER:
                continue
            unit = w
            break
        if unit and len(unit) > 2:
            yield num, unit


def norm(n):
    return float(n.replace(",", ""))


checked_actors = 0
total_claims = 0
flagged_groups = 0

for schema_path in sorted(glob.glob(os.path.join(ROOT, "actors/*/.actor/input_schema.json"))):
    actor_dir = os.path.dirname(os.path.dirname(schema_path))
    slug = os.path.basename(actor_dir)
    readme_path = os.path.join(actor_dir, "README.md")
    if not os.path.isfile(readme_path):
        continue
    checked_actors += 1

    by_unit = {}  # unit -> list of (number_str, location)

    for loc, text in collect_schema_text(schema_path):
        for num, unit in claims_in(text):
            by_unit.setdefault(unit, []).append((num, f".actor/input_schema.json:{loc}"))

    readme_text = open(readme_path, encoding="utf-8").read()
    for num, unit in claims_in(readme_text):
        by_unit.setdefault(unit, []).append((num, "README.md"))

    for unit, entries in by_unit.items():
        total_claims += len(entries)
        distinct = {norm(n) for n, _ in entries}
        if len(distinct) > 1:
            flagged_groups += 1
            print(f"{slug}: unit={unit!r} disagreeing numbers {sorted(distinct)}")
            for num, loc in entries:
                print(f"    {num}  <- {loc}")

print(f"\n_proto_numclaim: {checked_actors} actors scanned, {total_claims} candidate claims, "
      f"{flagged_groups} unit-groups with disagreeing numbers")
