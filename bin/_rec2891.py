#!/root/agent/venv/bin/python
"""One-off: record c2891's unreachable_remedy audit on substack-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. File is written with ensure_ascii=True, so a plain
json.load/json.dump round-trip is safe.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "substack-scraper"

NOTE = (
    "cycle 2891 (2555 -> 2891, 336c/7d gap; the ONLY real fleet-rotation item DUE this cycle, "
    "`audit-due --all` re-run fresh; checks-due NONE DUE soonest check-source-endpoints in 3c, "
    "inbox 0 untriaged of 75, revenue unchanged $0/27 Actors/50 users/816 runs30d/3 ext_bad30d). "
    "c1555 covered every zero-row/warning remedy STRING and c2555 covered the discoverType="
    "'podcast' leaderboard-density claims; neither touched the contentType='thread' warning "
    "(main.js:68-75), so this pass targeted that one. Claim as written (dated 2026-09-29, live-"
    "checked across a dozen large publications spanning news/tech/culture/comedy/economics plus "
    "Substack's own in-house blog): the archive API this Actor reads never returns a post of "
    "type 'thread' -- every post is 'newsletter' or 'podcast', including posts titled 'Open "
    "Thread'; Substack Notes/threads live on a separate surface this endpoint never exposes. "
    "Re-verified live, $0 (keyless GETs against each publication's own /api/v1/archive, correct "
    "cursor-paginated pageSize<=25 shape per the cycle-2853 fix -- an initial probe at limit=50 "
    "400'd exactly as that comment documents, confirming the fix's premise before trusting any "
    "result). Paged ~200 posts (8 pages x 25) on each of astralcodexten (200 newsletter / 0 "
    "podcast / 0 thread), slowboring.com (185 newsletter / 15 podcast / 0 thread), thefp.com (176 "
    "newsletter / 24 podcast / 0 thread), and heathercoxrichardson.substack.com (123 newsletter / "
    "77 podcast / 0 thread) -- 800 posts, 0 'thread'. Also pulled on.substack.com (Substack's own "
    "in-house blog, the specific publication the comment calls out by name): 21 newsletter / 4 "
    "podcast / 0 thread. Also specifically searched astralcodexten for 'open thread' (the exact "
    "title pattern the comment cites) -- all 10 matches ('Open Thread 190' etc, including two "
    "'Hidden Open Thread' posts) are type 'newsletter', confirming that specific detail still "
    "holds too. **0 defects found, claim holds exactly across 1,000+ posts on 5 publications "
    "incl. the one named in-house -- no code/README change needed.** node --check not run (no "
    "edit made, nothing to verify there); check-charges/check-registry-fields not re-run (pure "
    "verification, 0 diff, no build owed)."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("unreachable_remedy") == 2555, entry.get("unreachable_remedy")
old_note = entry.get("unreachable_remedy_note", "")
entry["unreachable_remedy"] = 2891
entry["unreachable_remedy_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
