#!/root/agent/venv/bin/python
"""One-off triage (c2426 follow-up, queue.md line 320): for each Actor, find
log.warning( calls that report a per-run FACT (not a generic network/retry message) whose
named identifier(s) never appear in any Actor.setStatusMessage(...) or RUN_SUMMARY
(Actor.setValue('RUN_SUMMARY', {...})) text later in the same file. That combination means
the fact is invisible on a SUCCEEDED run unless the buyer reads the log tab line by line.

Read-only triage only. No code changes. Output is a list of CANDIDATES for a human to read
in context -- many will turn out to be already disclosed under a different variable name or
to be pure error/retry chatter that was never meant to reach status, per the c2423 lesson
("read the code, not just the grep").
"""
import os
import re

ACTORS = '/root/agent/actors'
OPEN, CLOSE = '([{', ')]}'


def balanced_span(src, start):
    depth = 0
    for i in range(start, len(src)):
        c = src[i]
        if c in OPEN:
            depth += 1
        elif c in CLOSE:
            depth -= 1
            if depth == 0:
                return src[start:i + 1]
    return src[start:]


INTERP_IDENT = re.compile(r'\$\{\s*([A-Za-z_][A-Za-z0-9_.]*)')
QUOTED = re.compile(r'[\'"`]([A-Za-z_][A-Za-z0-9_]*)[\'"`]')
BAREIDENT = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\b')


def base(ident):
    """Strip a `.length`/`.join(...)` suffix so `notFoundIds.length` and the bare
    `notFoundIds` key in a plain object literal (no `${}`, so INTERP_IDENT can't see it)
    compare equal."""
    return ident.split('.', 1)[0]

# Generic retry/network/http chatter that is never meant to become a per-run buyer-facing
# fact -- excluding these keeps the candidate list to things actually worth a human reading.
NOISE = re.compile(
    r'retry|retrying|backoff|timeout|timed out|rate.?limit|429|5\d\d|ECONNRESET|ENOTFOUND|'
    r'attempt \d|network error|fetch failed|request failed',
    re.I)


def warning_calls(src):
    out = []
    for m in re.finditer(r'\.warning\s*\(', src):
        call = balanced_span(src, m.end() - 1)
        out.append((m.start(), call))
    return out


def declaration_body(src, ident):
    """Source text of `const/let/var <ident> = {...}` or `= [...]`, the initializer only."""
    m = re.search(r'\b(?:const|let|var)\s+' + re.escape(ident) + r'\s*=\s*', src)
    if not m:
        return ''
    rest = src[m.end():]
    if rest[:1] not in '{[':
        return ''
    return balanced_span(rest, 0)


CALLNAME = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\(')


def function_body(src, name):
    """Source of `function name(...) {...}` or `const name = (...) => {...}`."""
    m = re.search(r'\bfunction\s+' + re.escape(name) + r'\s*\(', src)
    if not m:
        m = re.search(r'\b(?:const|let|var)\s+' + re.escape(name) + r'\s*=\s*(?:\([^)]*\)|[A-Za-z_]\w*)\s*=>', src)
    if not m:
        return ''
    brace = src.find('{', m.end())
    if brace == -1:
        return ''
    return balanced_span(src, brace)


def status_text(src):
    """Concatenated text of every setStatusMessage(...) call and every
    Actor.setValue('RUN_SUMMARY', {...}) block, PLUS the body of any helper function
    those calls invoke (one level) -- e.g. court-records-scraper's `unknownCourtsNote()`,
    which is itself the thing that actually interpolates `unknownCourts`."""
    parts = []
    for m in re.finditer(r'setStatusMessage\s*\(', src):
        parts.append(balanced_span(src, m.end() - 1))
    for m in re.finditer(r"setValue\(\s*['\"]RUN_SUMMARY['\"]\s*,\s*", src):
        rest = src[m.end():]
        bare = re.match(r'[A-Za-z_][A-Za-z0-9_]*', rest)
        if bare and not rest[bare.end():].lstrip().startswith(')'):
            # e.g. `setValue('RUN_SUMMARY', { ... })` where our match ate into the brace --
            # fall through to the literal-brace case below.
            bare = None
        if bare:
            # `setValue('RUN_SUMMARY', runSummary)` -- the object is a named const built
            # earlier, not written inline. Clinicaltrials/fda-recall/app-store-reviews all use
            # this shape; resolving the call text alone would see no fields at all.
            body = declaration_body(src, bare.group(0))
            if body:
                parts.append(body)
            continue
        brace = rest.find('{')
        if brace != -1 and rest[:brace].strip() == '':
            parts.append(balanced_span(src, m.end() + brace))
    direct = '\n'.join(parts)
    called = set(CALLNAME.findall(direct))
    for name in called:
        body = function_body(src, name)
        if body:
            parts.append(body)
    return '\n'.join(parts)


def main():
    slugs = sorted(d for d in os.listdir(ACTORS) if not d.startswith('_'))
    total_calls = total_candidates = 0
    for slug in slugs:
        main_path = os.path.join(ACTORS, slug, 'src', 'main.js')
        if not os.path.exists(main_path):
            continue
        with open(main_path) as f:
            src = f.read()
        status = status_text(src)
        # Plain object/array literals (the common RUN_SUMMARY shape, `notFoundIds: ids,`) have
        # no `${}` or quotes around the identifier at all -- only a bare-word scan sees them.
        status_idents = {base(i) for i in
                          set(INTERP_IDENT.findall(status)) | set(QUOTED.findall(status)) | set(BAREIDENT.findall(status))}
        slug_candidates = []
        for pos, call in warning_calls(src):
            if NOISE.search(call):
                continue
            idents = {base(i) for i in set(INTERP_IDENT.findall(call)) | set(QUOTED.findall(call))}
            if not idents:
                continue
            total_calls += 1
            if idents & status_idents:
                continue
            line = src.count('\n', 0, pos) + 1
            slug_candidates.append((line, call.replace('\n', ' ')[:140], sorted(idents)))
        if slug_candidates:
            total_candidates += len(slug_candidates)
            print(f'\n{slug}  ({len(slug_candidates)} candidate(s))')
            for line, call, idents in slug_candidates:
                print(f'  L{line}  idents={idents}  {call}')
    print(f'\n_proto_statusvis: {total_calls} fact-bearing warning(s) scanned fleet-wide, '
          f'{total_candidates} candidate(s) (idents never appear in setStatusMessage/RUN_SUMMARY)')


if __name__ == '__main__':
    main()
