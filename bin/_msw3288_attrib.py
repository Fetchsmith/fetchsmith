#!/usr/bin/env python3
"""c3288: per-field attribution audit for check-mode-scope-warning.

The check has now printed 25 Actors / 44 mode-scoped fields / 0 flags on six
consecutive runs (c2712, c2808, c2904, c3000, c3096, c3192, c3288). A clean count
says only "every scoped field is named by SOME gated disclosure warning". It does
not say WHICH warning, and c2452 already had to close one hole of exactly that
shape (an unrelated warning donating the name). This probe answers, per field:
how many distinct gated warning calls donate it, and what their text is -- so a
pass backed only by a CONTEXTUAL mention inside a sibling field's disclosure
warning becomes visible instead of counting as clean.
"""
import importlib.util, json, os, re, sys

spec = importlib.util.spec_from_loader('msw', None)
msw = importlib.util.module_from_spec(spec)
src = open('/root/agent/bin/check-mode-scope-warning', encoding='utf-8').read()
exec(compile(src.split("def main(")[0], 'check-mode-scope-warning', 'exec'), msw.__dict__)

ACTORS = '/root/agent/actors'
declared = msw.load_declared()

def donors(main_src):
    """{name: [warning call text, ...]} -- per-call version of warned_names()."""
    out = {}
    for call, loop_header in msw.warning_calls(main_src):
        if not msw.IGNORE_WORD.search(call + ' ' + loop_header):
            continue
        names = set(msw.QUOTED.findall(call))
        names |= set(msw.INTERP_IDENT.findall(call))
        names |= set(msw.IDENT.findall(call))
        names |= set(msw.QUOTED.findall(loop_header))
        seeds = set(msw.INTERP_IDENT.findall(call)) | set(msw.IDENT.findall(loop_header))
        texts, seen = [], set()
        for ident in seeds:
            seen.add(ident)
            b = msw.declaration_body(main_src, ident)
            if b: texts.append(b)
        for _ in range(msw.DECL_DEPTH):
            nxt = []
            for t in texts:
                names |= set(msw.QUOTED.findall(t))
                for ident in set(msw.IDENT.findall(t)) - seen:
                    seen.add(ident)
                    b = msw.declaration_body(main_src, ident)
                    if b: nxt.append(b)
            texts = nxt
            if not texts: break
        for n in names:
            out.setdefault(n, []).append(' '.join(call.split())[:300])
    return out

total = multi = 0
rows = []
for slug in sorted(os.listdir(ACTORS)):
    sp = os.path.join(ACTORS, slug, '.actor/input_schema.json')
    mp = os.path.join(ACTORS, slug, 'src/main.js')
    if not (os.path.exists(sp) and os.path.exists(mp)):
        continue
    schema = json.load(open(sp))
    main_src = open(mp, encoding='utf-8').read()
    d = donors(main_src)
    for field, specd in (schema.get('properties') or {}).items():
        phrase = msw.scope_phrase(specd.get('description') or '')
        if not phrase and declared.get(slug, {}).get(field):
            phrase = 'sidecar'
        if not phrase:
            continue
        total += 1
        calls = d.get(field, [])
        rows.append((slug, field, len(calls), calls))
        if len(calls) != 1:
            multi += 1

print(f'{total} mode-scoped field(s); {multi} donated by != 1 gated warning call')
for slug, field, n, calls in rows:
    if n != 1:
        print(f'\n  {slug}  {field}  -- {n} donor call(s)')
        for c in calls:
            print(f'      | {c[:260]}')
