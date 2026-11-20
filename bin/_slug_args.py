"""Shared argv guard for the offline fleet checks: refuse to report a VACUOUS PASS.

The bug class this closes (found cycle 3480, by tripping it while running the cycle's own
due checks). Most fleet checks take an optional list of Actor slugs and sweep everything
when given none:

    slugs = sys.argv[1:] or sorted(os.listdir(ACTORS))
    for slug in slugs: ...
    print(f'check-foo: {n} Actor(s), {flags} flag(s)')
    if not flags: print('<reassuring green sentence>')

Hand that a name matching nothing -- a typo, a retired slug, or a flag the tool does not
define -- and the filter resolves to the EMPTY list. Every loop body is skipped, every
counter stays 0, the tool prints its green "nothing wrong anywhere" sentence and exits 0.
Nothing is checked and the output is indistinguishable from a real clean sweep.

Measured cycle 3480 on this exact class: `check-mode-scope-warning --all` printed
"25 Actor(s), 44 mode-scoped field(s), 0 flag(s)" when invoked bare, and
"0 Actor(s), 0 mode-scoped field(s), 0 flag(s)" plus its green sentence when given --all,
which it does not define. A one-token slip silently reduced a fleet sweep to nothing.

Why this is expensive rather than merely untidy: the cycle protocol STAMPS a check as run
in state/fleet_checks.json (`bin/checks-due --ran <check>`), which sets its next-due cycle
336-2016 cycles out. Recording a vacuous pass does not just lose one sweep -- it buys the
real regression up to ~2000 cycles of silence, and the STATUS.md block for that cycle will
read "0 flags" in good faith. A false clean is strictly worse than a crash.

The 10 offline checks subject to it on arrival (bogus-slug probe, cycle 3480):
check-mode-scope-warning, check-term-anchor, check-zero-row-message, check-filter-reach,
check-fail-ordering, check-seed-save, check-code-fields, check-registry-fields,
check-source-bytes (roots, not slugs -- a nonexistent root scans 0 files), and
check-validated-filters.

Three checks ALREADY got this right and are the model: check-example-input exits 1 with
"no such slug in registry.json", check-schema-claims exits 1 with "unknown argument", and
check-absence-claims exits 1 with its usage block.

DESIGN: validation only. This module never computes the selection, so wiring it in cannot
change which Actors a check sweeps -- each call site keeps its own filtering line exactly
as written, and gains one guard above it. Exit code 2 (not 1) deliberately: 1 already
means "this check found flags" fleet-wide, and a bad invocation must not be confusable
with a real finding.
"""
import sys


def validate(tool, requested, available, kind='Actor slug'):
    """Exit(2) loudly if `requested` names anything not in `available`, else return.

    tool       -- the check's own name, for the error message.
    requested  -- the names the caller took off argv (empty/None = sweep everything, always OK).
    available  -- iterable of the names that exist (slugs, term keys, roots, ...).
    kind       -- noun for the message, e.g. 'Actor slug', 'root path'.

    Returns None. Callers keep their existing selection logic unchanged.
    """
    requested = list(requested or ())
    if not requested:
        return                      # bare invocation = full sweep, nothing to validate

    have = set(available)
    unknown = [r for r in requested if r not in have]
    if not unknown:
        return

    print(f'{tool}: unknown {kind}(s): {", ".join(unknown)}', file=sys.stderr)

    # The commonest cause by far, and the one that produced this module: a flag the tool
    # does not define, read as a name to filter on. Say so explicitly -- the generic
    # "unknown slug" line alone sent cycle 3480 looking for a retired Actor.
    flaggish = [r for r in unknown if r.startswith('-')]
    if flaggish:
        print(f'{tool}: {", ".join(flaggish)} looks like a flag but is not one of this '
              f"tool's -- it was read as a name to filter on. Run it with NO arguments "
              'to sweep the whole fleet.', file=sys.stderr)

    print(f'{tool}: refusing to run, because filtering on a name that matches nothing '
          'would check 0 items and print a CLEAN result. Fix the argument, or pass none '
          'to sweep everything.', file=sys.stderr)
    sys.exit(2)
