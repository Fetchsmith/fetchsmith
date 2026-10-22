"""FetchSmith web app: catalog, legal pages, API (keys + credits), Polar checkout/webhooks."""
import os, json, time, secrets, sqlite3, hmac, hashlib, base64, logging
from datetime import date, datetime, timezone
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException, Depends, Header
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

ROOT = Path("/root/agent")
DB_PATH = ROOT / "data" / "fetchsmith.db"
REGISTRY = ROOT / "actors" / "registry.json"
SITE_URL = "https://fetchsmith.com"
SUPPORT_EMAIL = "support@fetchsmith.com"
log = logging.getLogger("fetchsmith")
logging.basicConfig(level=logging.INFO)

def env(k, d=""):
    return os.environ.get(k, d)

def _vid_salt():
    """Stable secret salt for visitor tokens (must survive restarts, else same-day
    dedupe breaks). Generated once on first boot; never leaves this box."""
    f = ROOT / "data" / ".vid_salt"
    try:
        return f.read_text().strip()
    except OSError:
        s = secrets.token_hex(16)
        f.write_text(s)
        os.chmod(f, 0o600)
        return s

VID_SALT = _vid_salt()

app = FastAPI(title="FetchSmith", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=str(ROOT / "site" / "static")), name="static")
tpl = Jinja2Templates(directory=str(ROOT / "site" / "templates"))


def _usd(v):
    """Format a per-result price for display: 0.002 -> '0.002', 0.000575 -> '0.000575'.

    Added cycle 1744 for the Apify price line on tool pages. `'%.4f'` (what the credit
    price used) truncates the fleet's cheapest Actors to '0.0001' correctly but would
    round 0.000575 to '0.0006' and 0.00085 to '0.0009' -- quoting a price we do not
    charge. 6dp covers every live price in the fleet ($0.0001-$0.004); the max() floor
    keeps a hypothetical sub-6dp price from rendering as the bare string '0.'."""
    try:
        return ("%.6f" % max(float(v), 0.000001)).rstrip("0")
    except (TypeError, ValueError):
        return None


tpl.env.filters["usd"] = _usd

# ---------- db ----------
def db():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS customers(id INTEGER PRIMARY KEY, email TEXT UNIQUE, polar_customer_id TEXT, created INTEGER);
        CREATE TABLE IF NOT EXISTS api_keys(key TEXT PRIMARY KEY, customer_id INTEGER, created INTEGER, revoked INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS credits(customer_id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS ledger(id INTEGER PRIMARY KEY, customer_id INTEGER, delta INTEGER, reason TEXT, ref TEXT, ts INTEGER);
        CREATE TABLE IF NOT EXISTS usage(id INTEGER PRIMARY KEY, key TEXT, tool TEXT, results INTEGER, cost INTEGER, ts INTEGER);
        CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, kind TEXT, payload TEXT, ts INTEGER);
        CREATE TABLE IF NOT EXISTS pageviews(id INTEGER PRIMARY KEY, path TEXT, ref TEXT, ua TEXT, ts INTEGER);
        CREATE TABLE IF NOT EXISTS asset_hits(vid TEXT PRIMARY KEY, ts INTEGER);
        """)
        # cycle 32: pseudonymous per-day visitor token, so crawler traffic can be told
        # apart from real browsers (UA alone overstates humans ~40x). Added by migration
        # because the table predates it.
        cols = {r[1] for r in c.execute("PRAGMA table_info(pageviews)")}
        if "vid" not in cols:
            c.execute("ALTER TABLE pageviews ADD COLUMN vid TEXT")
init_db()

def load_registry():
    try:
        return json.loads(REGISTRY.read_text()).get("tools", [])
    except Exception:
        return []

def public_tools():
    return [t for t in load_registry() if t.get("status") in ("live", "beta")]

def readable_tools():
    # `retired` tools are gone from the grid, the docs and /api/v1/run (all of which use
    # public_tools), but their /tools/<slug> page must keep resolving: the URL is indexed and
    # linked from blog posts, and a 404 tells a visitor nothing. The page renders read-only --
    # see the t.status == 'retired' branches in tool.html. Added cycle 652 when bold.org put
    # its whole site behind a Vercel bot challenge and scholarship-scraper was retired.
    return [t for t in load_registry() if t.get("status") in ("live", "beta", "retired")]

# ---------- blog (markdown files in site/content/blog) ----------
BLOG_DIR = ROOT / "site" / "content" / "blog"
_blog_cache = {"stamp": None, "posts": []}

def _parse_post(path: Path):
    raw = path.read_text()
    meta, body = {}, raw
    if raw.startswith("---"):
        head, _, body = raw[3:].partition("\n---")
        for line in head.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        body = body.lstrip("\n")
    try:
        import markdown
        html = markdown.markdown(body, extensions=["fenced_code", "tables"])
    except Exception:  # never let a rendering dep take the site down
        log.exception("markdown render failed for %s", path.name)
        html = "<pre>" + body.replace("<", "&lt;") + "</pre>"
    return {
        "slug": path.stem,
        "title": meta.get("title", path.stem),
        "description": meta.get("description", ""),
        "date": meta.get("date", ""),
        "date_modified": max(
            meta.get("date", ""),
            datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d"),
        ),
        "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
        "tool": meta.get("tool", ""),
        "syndicated": meta.get("syndicated", ""),
        "html": html,
    }

def load_posts():
    try:
        files = sorted(BLOG_DIR.glob("*.md"))
    except Exception:
        return []
    stamp = tuple((f.name, f.stat().st_mtime) for f in files)
    if _blog_cache["stamp"] != stamp:
        posts = []
        for f in files:
            try:
                posts.append(_parse_post(f))
            except Exception:
                log.exception("bad blog post %s", f.name)
        posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
        _blog_cache.update(stamp=stamp, posts=posts)
    return _blog_cache["posts"]

# ---------- lightweight analytics (no cookies) ----------
def visitor_token(request: Request) -> str:
    """Pseudonymous per-day visitor id: sha256(daily salt + client ip + ua), truncated.

    Not reversible to an IP and it rotates every day, so this stays within the privacy
    policy's "without identifying you" — but it lets us count distinct visitors and,
    combined with asset_hits, separate real browsers from UA-spoofing crawlers.
    """
    ip = (request.headers.get("x-forwarded-for", "").split(",")[0].strip()
          or (request.client.host if request.client else ""))
    day = time.strftime("%Y-%m-%d", time.gmtime())
    raw = f"{VID_SALT}|{day}|{ip}|{request.headers.get('user-agent','')}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

@app.middleware("http")
async def track(request: Request, call_next):
    # Cycle 1688: FastAPI's @app.get registers ONLY GET (plain Starlette Route auto-adds
    # HEAD; APIRoute does not), so every route on the site answered `405 Method Not Allowed`
    # to a HEAD probe -- crawlers, directory-submission link checkers and PLAYBOOK's own
    # `curl -I` recipe all use HEAD. Serve HEAD as GET and strip the body per RFC 9110
    # (same headers, incl. Content-Length, no payload).
    head = request.method == "HEAD"
    if head:
        request.scope["method"] = "GET"
        # Handlers see method == "GET" after the rewrite, so anything that WRITES on a
        # request (e.g. /go/<slug>'s out_click row) must test this flag, not request.method.
        request.scope["fs_head"] = True
    resp = await call_next(request)
    if head:
        # Drain the downstream body so BaseHTTPMiddleware's producer task finishes cleanly,
        # then reply header-only. Deliberately NOT recorded as a pageview: HEAD traffic is
        # bots/link-checkers, and cycle 1652 already showed how badly those distort bin/traffic.
        async for _ in resp.body_iterator:
            pass
        return Response(status_code=resp.status_code, headers=resp.headers)
    p = request.url.path
    if resp.status_code != 200:
        return resp
    try:
        if p.startswith("/static"):
            # A client that loads our CSS/JS is a real browser, not a link enumerator.
            with db() as c:
                c.execute("INSERT OR IGNORE INTO asset_hits(vid,ts) VALUES(?,?)",
                          (visitor_token(request), int(time.time())))
        elif not p.startswith(("/api", "/webhooks", "/health")) and "." not in p.rsplit("/", 1)[-1]:
            with db() as c:
                c.execute("INSERT INTO pageviews(path,ref,ua,ts,vid) VALUES(?,?,?,?,?)",
                          (p, request.headers.get("referer", "")[:200], request.headers.get("user-agent", "")[:200],
                           int(time.time()), visitor_token(request)))
    except Exception:
        pass
    return resp

def render(request, name, status_code=200, **ctx):
    ctx.setdefault("site_url", SITE_URL)
    ctx.setdefault("support_email", SUPPORT_EMAIL)
    ctx.setdefault("apify_user", env("APIFY_USERNAME", "fetchsmith"))
    ctx.setdefault("checkout_live", bool(polar_products()))
    # Available to every template so a page can quote a real $/result without hardcoding it
    # (cycle 1660: `/` is our most AI-fetched page and carried no dollar figure at all).
    ctx.setdefault("packs", CREDIT_PACKS)
    return tpl.TemplateResponse(request, name, ctx, status_code=status_code)

def _best_blog_match(slug):
    """Token-set overlap against known slugs, so an answer engine's guessed URL
    (e.g. /blog/workday-cxs-api) lands on the real post instead of a dead 404.
    Deliberately dumb: no fuzzy-match library, just split-on-'-' set overlap."""
    want = set(slug.split("-"))
    best_slug, best_score, best_overlap = None, 0.0, 0
    for p in load_posts():
        cand = set(p["slug"].split("-"))
        overlap = want & cand
        union = want | cand
        score = len(overlap) / len(union) if union else 0.0
        if len(overlap) >= 2 and (score, len(overlap)) > (best_score, best_overlap):
            best_slug, best_score, best_overlap = p["slug"], score, len(overlap)
    return best_slug if best_score >= 0.3 else None

# ---------- pages ----------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    tools = public_tools()
    return render(request, "home.html", tools=tools[:12], count=len(tools), all_tools=tools)

@app.get("/tools", response_class=HTMLResponse)
def tools_page(request: Request):
    tools = public_tools()
    # Cycle 1744 fixed /tools/<slug> to lead with the live Apify price (the only one a
    # buyer can actually pay while checkout_live is false) instead of the flat $0.0025/
    # result credit price. This grid's own hero line and card pills had the identical
    # bug -- see queue.md cycle 1745. `price_range` lets the template state the true
    # spread instead of a single fabricated number.
    entries = [t["apify_price"]["entry"] for t in tools if t.get("apify_price")]
    price_range = (min(entries), max(entries)) if entries else None
    return render(request, "tools.html", tools=tools, all_tools=tools, price_range=price_range)

@app.get("/tools/{slug}", response_class=HTMLResponse)
def tool_page(request: Request, slug: str):
    t = next((t for t in readable_tools() if t["slug"] == slug), None)
    if not t:
        raise HTTPException(404)
    return render(request, "tool.html", t=t, guides=[p for p in load_posts() if p.get("tool") == slug])

@app.get("/go-store")
def go_store(request: Request):
    """Outbound click-through to our Apify PUBLISHER PROFILE (apify.com/<user>), logged
    the same way /go/<slug> is, under the sentinel slug `_store`.

    Added cycle 2044. Why a separate route: cycle 2044 measured that exactly 7 blog posts
    (the multi-Actor roundups: `free-government-data-json-apis-no-key`,
    `public-content-apis-hidden-second-step`, `app-store-review-apis-three-silent-empties`,
    `government-apis-fail-open-on-a-dropped-filter-name`, `watch-baseline-eviction-rebilling`,
    `apify-tiered-pricing-nested-dict-reads-as-free`, `incremental-api-watch-mode-four-traps`)
    had NO one-hop path to any Actor anywhere on the page: they carry no `tool:` frontmatter,
    so post.html's sidebar falls through to the generic "Browse tools" box, and their bodies
    link only /tools/<slug> (two hops to Apify). `bin/check-blog-cta` deliberately does not
    flag roundups, because picking one arbitrary Actor out of a 4-20 Actor list as THE CTA
    would be dishonest. The publisher profile is the honest one-hop target for a roundup:
    it is the whole catalogue the post is actually about. Verified 200 live before shipping.

    Keep this consistent with go() below: same HEAD handling (a link check is not a click),
    same out_click payload shape, so bin/traffic's existing queries pick it up unchanged.
    """
    dest = f"https://apify.com/{env('APIFY_USERNAME', 'fetchsmith')}"
    if request.scope.get("fs_head"):
        return RedirectResponse(dest, status_code=302)
    try:
        with db() as c:
            c.execute("INSERT INTO events(kind,payload,ts) VALUES(?,?,?)",
                      ("out_click", json.dumps({"slug": "_store", "path": str(request.url.path),
                                                "ref": request.headers.get("referer", "")[:200],
                                                "ua": request.headers.get("user-agent", "")[:200],
                                                "vid": visitor_token(request)}),
                       int(time.time())))
    except Exception:
        pass
    return RedirectResponse(dest, status_code=302)

@app.get("/go/{slug}")
def go(request: Request, slug: str):
    """Outbound click-through to the Apify Store listing, logged as an `events`
    row (kind=out_click) before redirecting. Added cycle 1509: blog CTAs linked
    straight to apify.com, which meant every post->product click was invisible
    to our own analytics (outbound links don't generate a pageview here). This
    is now the only way blog/tool CTAs reach Apify, so bin/traffic can finally
    see conversion instead of the /tools/ proxy metric.

    Cycle 1652: also record `ua` and `vid`, so out_clicks get the same bot
    verification `pageviews` has had since cycle 32 (UA test + asset_hits). Without
    them the metric ran ~2x inflated: of 232 /go/ hits in one 5-day access-log window
    only 85 were human-looking -- 93 were declared crawlers walking every /go/ slug
    (AI answer engines: OAI-SearchBot, PerplexityBot, Amazonbot) and 54 our own curl.
    """
    _t = next((t for t in readable_tools() if t["slug"] == slug), None)
    if _t is None:
        raise HTTPException(404)
    # Cycle 1956: an Actor with `apify_listed: false` has no public Store page, so the
    # redirect below would hand the visitor an apify.com 404. Send them to our own tool
    # page (which explains why it isn't runnable yet) instead of off-site into nothing.
    # The templates already hide these CTAs; this covers indexed links and crawlers.
    if _t.get("apify_listed") is False:
        return RedirectResponse(f"/tools/{slug}", status_code=302)
    # Cycle 1688: HEAD is now served (see the `track` middleware), but a HEAD probe is a
    # link check, not a click -- log only real GETs or this metric regains the ~2x bot
    # inflation cycle 1652 fixed. `request.method` is already rewritten here, so read the flag.
    if request.scope.get("fs_head"):
        return RedirectResponse(f"https://apify.com/{env('APIFY_USERNAME', 'fetchsmith')}/{slug}", status_code=302)
    try:
        with db() as c:
            c.execute("INSERT INTO events(kind,payload,ts) VALUES(?,?,?)",
                      ("out_click", json.dumps({"slug": slug, "path": str(request.url.path),
                                                 "ref": request.headers.get("referer", "")[:200],
                                                 "ua": request.headers.get("user-agent", "")[:200],
                                                 "vid": visitor_token(request)}),
                       int(time.time())))
    except Exception:
        pass
    return RedirectResponse(f"https://apify.com/{env('APIFY_USERNAME', 'fetchsmith')}/{slug}", status_code=302)

@app.get("/blog", response_class=HTMLResponse)
def blog_index(request: Request):
    return render(request, "blog.html", posts=load_posts())

@app.get("/blog/{slug}", response_class=HTMLResponse)
def blog_post(request: Request, slug: str):
    p = next((p for p in load_posts() if p["slug"] == slug), None)
    if not p:
        match = _best_blog_match(slug)
        if match:
            return RedirectResponse(f"/blog/{match}", status_code=301)
        return render(request, "404.html", status_code=404)
    # readable_tools, not public_tools: a guide for a retired tool should say so in its
    # sidebar (post.html's tool.status == 'retired' branch) rather than fall through to the
    # generic "Browse tools" blurb, which told a reader nothing about the tool they came for.
    tool = next((t for t in readable_tools() if t["slug"] == p.get("tool")), None)
    return render(request, "post.html", p=p, tool=tool)

@app.get("/pricing", response_class=HTMLResponse)
def pricing(request: Request):
    return render(request, "pricing.html", packs=CREDIT_PACKS, tools=public_tools()[:6])

@app.get("/docs", response_class=HTMLResponse)
def docs(request: Request):
    return render(request, "docs.html", tools=public_tools())

for page in ("terms", "privacy", "refunds", "contact", "about"):
    def _mk(page):
        def _view(request: Request):
            return render(request, f"{page}.html")
        return _view
    app.add_api_route(f"/{page}", _mk(page), methods=["GET"], response_class=HTMLResponse)

@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    # Cycle 2096: the llms.txt pointer is a comment, not a directive -- no robots.txt field
    # carries it, and inventing one would be ignored at best. It is here because an agent
    # fetching robots.txt first is the one most likely to want the curated index.
    return ("User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /webhooks/\n"
            "Sitemap: https://fetchsmith.com/sitemap.xml\n"
            "# LLM-readable index of every tool, price and guide: https://fetchsmith.com/llms.txt\n")

@app.get("/llms.txt", response_class=PlainTextResponse)
def llms():
    # Cycle 1660: every tool entry now carries its runnable apify.com/<user>/<slug> URL and its
    # price. llms.txt is the one file we publish *for* answer engines, and it previously gave
    # neither -- a model summarising it could name our tools but could not tell a buyer what a
    # row costs or where to run one. Same gap cycle 1656 closed on `/` and `/tools`.
    # The credit $/result figure is derived from CREDIT_PACKS (the hosted-credit product) -- do
    # NOT conflate it with the Apify price: the two are separate products with separate prices
    # (LEARNINGS cycle 480), so each is quoted against its own product by name.
    # Cycle 2096: this file still LED with the credit price for a hosted product that is not
    # open, and gave the Apify route a URL with "no dollar claim" -- so the only price an answer
    # engine could read off it was for the one thing nobody can buy today. That is exactly the
    # gap cycle 1744 closed on /tools/<slug> and cycle 2068 closed on the blog sidebar, left
    # behind on the one file we publish *for* answer engines (and per cycle 2068's Caddy-log
    # measurement, assistant fetches are the dominant real traffic). While checkout_live is
    # false, lead every entry with the Apify per-result price from registry `apify_price` --
    # the payable-today number -- and label the credit price as planned.
    au = env("APIFY_USERNAME", "fetchsmith")
    starter = next((p for p in CREDIT_PACKS if p["id"] == "starter"), None)
    rate = (starter["usd"] / starter["credits"]) if starter else 0.0025
    checkout_live = bool(polar_products())

    def apify_price_phrase(t):
        """'$0.002 per returned result' for a listed Actor, else None. Tiered Actors state the
        entry price and the floor, matching the tool page and blog sidebar wording."""
        ap = t.get("apify_price") or {}
        if t.get("apify_listed") is False or not ap.get("entry"):
            return None
        s = f"${_usd(ap['entry'])} per returned result on Apify Store"
        if ap.get("floor") and ap["floor"] != ap["entry"]:
            s += f" (down to ${_usd(ap['floor'])} per result on higher Apify plans)"
        return s

    lines = ["# FetchSmith", "",
             "> Pay-per-result web data extraction tools, runnable today as Apify Actors. No subscription required; you are charged only for rows actually returned, and failed or empty runs cost nothing."
             f" Every tool runs under the FetchSmith publisher account on Apify Store (https://apify.com/{au}) with pay-per-event billing through your Apify account, at the per-result price given on each entry below."
             + ("" if checkout_live else
                f" A hosted API on prepaid credits (about ${rate:.4f} per result) is planned but NOT open yet, so the Apify price is the one a buyer can pay today."),
             "", "## Tools",
             "Each entry gives the tool's documentation page, then the price and the Apify Actor URL you can run it from today."]
    for t in public_tools():
        cpr = int(t.get("credits_per_result", 1) or 1)
        credit = f"{cpr} credit{'' if cpr == 1 else 's'} per returned result (about ${rate * cpr:.4f} per result on the smallest prepaid pack)"
        ap_phrase = apify_price_phrase(t)
        if ap_phrase and not checkout_live:
            price = f"{ap_phrase}. Planned hosted-API price: {credit}"
        elif ap_phrase:
            price = f"{credit} on the hosted API; {ap_phrase}"
        else:
            price = credit
        run = ("" if t.get("apify_listed") is False
               else f" Run it on Apify Store: https://apify.com/{au}/{t['slug']}")
        lines.append(f"- [{t['title']}]({SITE_URL}/tools/{t['slug']}): {t.get('summary','')} "
                     f"Price: {price}.{run}")
    lines += ["", "## Pricing",
              "Prepaid credit packs for the hosted API (credits never expire, one credit is one returned result for most tools):"]
    for p in CREDIT_PACKS:
        lines.append(f"- {p['name']}: ${p['usd']} for {p['credits']:,} credits (${p['usd'] / p['credits']:.4f} per result) -- {p['blurb']} {SITE_URL}/pricing")
    lines.append(f"- Usage-based alternative, available now: run any tool as an Apify Actor at https://apify.com/{au} and pay per event through your Apify account.")
    if load_posts():
        # Cycle 2096: a guide entry used to end at its description, so the 79-of-86 posts that
        # document the exact API one of our Actors is built on gave an answer engine no payable
        # destination -- the same gap the Tools section had before cycle 1660. Each mapped guide
        # now names its tool, its price and its runnable URL. A retired tool says so instead of
        # advertising an Actor that cannot return data (mirrors tool.html / post.html).
        by_slug = {t["slug"]: t for t in readable_tools()}
        lines += ["", "## Guides",
                  "Technique notes measured against the live API, each linked to the tool built on it."]
        for p in load_posts():
            entry = f"- [{p['title']}]({SITE_URL}/blog/{p['slug']}): {p['description']}"
            t = by_slug.get(p.get("tool"))
            if t and t.get("status") == "retired":
                entry += (f" Tool: {t['title']} ({SITE_URL}/tools/{t['slug']}) -- not runnable or"
                          " billable right now; the guide stands on the technique alone.")
            elif t:
                ap_phrase = apify_price_phrase(t)
                entry += f" Tool: [{t['title']}]({SITE_URL}/tools/{t['slug']})"
                if ap_phrase:
                    entry += (f", {ap_phrase}, runnable at "
                              f"https://apify.com/{au}/{t['slug']}.")
                else:
                    entry += "."
            lines.append(entry)
    lines += ["", "## Docs", f"- [API docs]({SITE_URL}/docs)", f"- [Pricing]({SITE_URL}/pricing)",
              f"- [Apify Store profile (all {len(public_tools())} tools, runnable today)](https://apify.com/{au})"]
    return "\n".join(lines) + "\n"

_STATIC_PAGE_TEMPLATES = {
    "": "home.html", "/tools": "tools.html", "/pricing": "pricing.html", "/docs": "docs.html",
    "/blog": "blog.html", "/about": "about.html", "/contact": "contact.html",
    "/terms": "terms.html", "/privacy": "privacy.html", "/refunds": "refunds.html",
}

def _file_date(path: Path):
    try:
        return date.fromtimestamp(path.stat().st_mtime).isoformat()
    except OSError:
        return None

@app.get("/sitemap.xml")
def sitemap():
    # lastmod uses filesystem mtime (template file for static pages, actor meta.json for tool
    # pages, the post's own frontmatter `date` for blog -- that one is already authoritative and
    # cheaper than a stat call). Omitted, not guessed, if the backing file is missing.
    entries = []
    for u, tmpl in _STATIC_PAGE_TEMPLATES.items():
        entries.append((u, _file_date(ROOT / "site" / "templates" / tmpl)))
    for t in public_tools():
        entries.append((f"/tools/{t['slug']}", _file_date(ROOT / "actors" / t["slug"] / "meta.json")))
    for p in load_posts():
        entries.append((f"/blog/{p['slug']}", p.get("date")))
    body = "".join(
        f"<url><loc>{SITE_URL}{u}</loc>{f'<lastmod>{lm}</lastmod>' if lm else ''}</url>"
        for u, lm in entries
    )
    return Response(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>', media_type="application/xml")

@app.get("/health")
def health():
    return {"ok": True, "tools": len(public_tools()), "ts": int(time.time())}

# ---------- credits & checkout (Polar) ----------
CREDIT_PACKS = [
    {"id": "starter", "name": "Starter", "credits": 2000, "usd": 5, "blurb": "Good for a few thousand rows."},
    {"id": "pro", "name": "Pro", "credits": 12000, "usd": 19, "blurb": "For regular pulls and small pipelines."},
    {"id": "scale", "name": "Scale", "credits": 50000, "usd": 59, "blurb": "For agencies and data teams."},
]
POLAR_API = "https://api.polar.sh/v1"

def polar_headers():
    tok = env("POLAR_ACCESS_TOKEN")
    if not tok:
        raise HTTPException(503, "Checkout is not configured yet. Email support@fetchsmith.com.")
    return {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}

def polar_products():
    try:
        return json.loads((ROOT / "state" / "polar_products.json").read_text())
    except Exception:
        return {}

@app.get("/checkout/{pack_id}")
async def checkout(pack_id: str):
    pack = next((p for p in CREDIT_PACKS if p["id"] == pack_id), None)
    if not pack:
        raise HTTPException(404)
    pid = polar_products().get(pack_id)
    if not pid:
        return RedirectResponse(f"/checkout-soon?pack={pack_id}", status_code=303)
    async with httpx.AsyncClient(timeout=20) as cl:
        r = await cl.post(f"{POLAR_API}/checkouts/", headers=polar_headers(),
                          json={"products": [pid], "success_url": f"{SITE_URL}/welcome?checkout_id={{CHECKOUT_ID}}", "metadata": {"pack": pack_id}})
    if r.status_code >= 300:
        log.error("polar checkout error %s %s", r.status_code, r.text[:300])
        raise HTTPException(502, "Checkout temporarily unavailable.")
    return RedirectResponse(r.json()["url"], status_code=303)

def grant_credits(email: str, credits: int, reason: str, ref: str, polar_customer_id: str = None):
    with db() as c:
        row = c.execute("SELECT id FROM customers WHERE email=?", (email,)).fetchone()
        if row:
            cid = row["id"]
        else:
            cid = c.execute("INSERT INTO customers(email,polar_customer_id,created) VALUES(?,?,?)", (email, polar_customer_id, int(time.time()))).lastrowid
        if c.execute("SELECT 1 FROM ledger WHERE ref=?", (ref,)).fetchone():
            return None  # idempotent
        c.execute("INSERT INTO credits(customer_id,balance) VALUES(?,0) ON CONFLICT(customer_id) DO NOTHING", (cid,))
        c.execute("UPDATE credits SET balance=balance+? WHERE customer_id=?", (credits, cid))
        c.execute("INSERT INTO ledger(customer_id,delta,reason,ref,ts) VALUES(?,?,?,?,?)", (cid, credits, reason, ref, int(time.time())))
        key = c.execute("SELECT key FROM api_keys WHERE customer_id=? AND revoked=0", (cid,)).fetchone()
        if not key:
            k = "fs_" + secrets.token_urlsafe(24)
            c.execute("INSERT INTO api_keys(key,customer_id,created) VALUES(?,?,?)", (k, cid, int(time.time())))
        else:
            k = key["key"]
        return k

def verify_polar_signature(secret: str, body: bytes, headers) -> bool:
    # Standard Webhooks: webhook-id, webhook-timestamp, webhook-signature ("v1,<b64>")
    try:
        wid = headers.get("webhook-id"); ts = headers.get("webhook-timestamp"); sig = headers.get("webhook-signature", "")
        if not (wid and ts and sig):
            return False
        if secret.startswith("whsec_"):
            secret = secret[6:]
        key = base64.b64decode(secret)
        signed = f"{wid}.{ts}.".encode() + body
        expect = base64.b64encode(hmac.new(key, signed, hashlib.sha256).digest()).decode()
        return any(hmac.compare_digest(expect, s.split(",", 1)[1]) for s in sig.split() if "," in s)
    except Exception:
        return False

@app.post("/webhooks/polar")
async def polar_webhook(request: Request):
    body = await request.body()
    secret = env("POLAR_WEBHOOK_SECRET")
    if secret and not verify_polar_signature(secret, body, request.headers):
        raise HTTPException(401, "bad signature")
    evt = json.loads(body or b"{}")
    kind = evt.get("type", "")
    data = evt.get("data", {})
    with db() as c:
        c.execute("INSERT INTO events(kind,payload,ts) VALUES(?,?,?)", (kind, body.decode("utf-8", "ignore")[:20000], int(time.time())))
    if kind == "order.paid" or (kind == "order.created" and data.get("paid")):
        email = (data.get("customer") or {}).get("email") or data.get("user", {}).get("email")
        pack_id = (data.get("metadata") or {}).get("pack") or (data.get("product") or {}).get("metadata", {}).get("pack")
        pack = next((p for p in CREDIT_PACKS if p["id"] == pack_id), None)
        if not pack:
            # match by product id
            inv = {v: k for k, v in polar_products().items()}
            pack = next((p for p in CREDIT_PACKS if p["id"] == inv.get((data.get("product") or {}).get("id"))), None)
        if email and pack:
            key = grant_credits(email, pack["credits"], f"purchase:{pack['id']}", f"polar_order:{data.get('id')}", (data.get("customer") or {}).get("id"))
            if key:
                await send_key_email(email, key, pack)
                await notify_owner(f"FetchSmith sale: {pack['name']} ${pack['usd']}", f"Order {data.get('id')} from {email}. Credits granted: {pack['credits']}.")
    return {"ok": True}

@app.get("/checkout-soon", response_class=HTMLResponse)
def checkout_soon(request: Request, pack: str = ""):
    return render(request, "checkout_soon.html", pack=pack, tools=public_tools())

@app.get("/welcome", response_class=HTMLResponse)
def welcome(request: Request, checkout_id: str = ""):
    return render(request, "welcome.html", checkout_id=checkout_id)

# ---------- email ----------
async def resend_send(to: str, subject: str, text: str):
    key = env("RESEND_API_KEY")
    if not key:
        return
    async with httpx.AsyncClient(timeout=20) as cl:
        r = await cl.post("https://api.resend.com/emails", headers={"Authorization": f"Bearer {key}"},
                          json={"from": "FetchSmith <hello@fetchsmith.com>", "to": [to], "reply_to": SUPPORT_EMAIL, "subject": subject, "text": text})
        if r.status_code >= 300:
            log.error("resend error %s %s", r.status_code, r.text[:200])

async def send_key_email(email, key, pack):
    await resend_send(email, "Your FetchSmith API key",
        f"Thanks for buying the {pack['name']} pack ({pack['credits']} credits).\n\nYour API key:\n{key}\n\nQuick start:\ncurl -H 'Authorization: Bearer {key}' '{SITE_URL}/api/v1/account'\n\nDocs: {SITE_URL}/docs\nQuestions: {SUPPORT_EMAIL}\n")

async def notify_owner(subject, text):
    owner = env("OWNER_EMAIL")
    if owner:
        await resend_send(owner, subject, text)

# ---------- API ----------
def auth(authorization: str = Header(default="")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing API key. Use: Authorization: Bearer <key>")
    k = authorization[7:].strip()
    with db() as c:
        row = c.execute("SELECT k.customer_id, cr.balance FROM api_keys k JOIN credits cr ON cr.customer_id=k.customer_id WHERE k.key=? AND k.revoked=0", (k,)).fetchone()
    if not row:
        raise HTTPException(401, "Invalid API key")
    return {"key": k, "customer_id": row["customer_id"], "balance": row["balance"]}

@app.get("/api/v1/account")
def account(a=Depends(auth)):
    return {"credits": a["balance"]}

@app.get("/api/v1/tools")
def api_tools():
    return {"tools": [{"slug": t["slug"], "title": t["title"], "credits_per_result": t.get("credits_per_result", 1), "input": t.get("input", {})} for t in public_tools()]}

@app.post("/api/v1/run/{slug}")
async def run_tool(slug: str, request: Request, a=Depends(auth)):
    t = next((t for t in public_tools() if t["slug"] == slug), None)
    if not t:
        raise HTTPException(404, "Unknown tool")
    body = await request.json() if (await request.body()) else {}
    max_results = int(body.get("max_results", 50))
    cpr = int(t.get("credits_per_result", 1))
    if a["balance"] < cpr:
        raise HTTPException(402, "Insufficient credits. Buy more at https://fetchsmith.com/pricing")
    max_results = max(1, min(max_results, a["balance"] // cpr, 1000))
    body["max_results"] = max_results
    # Run the Apify actor synchronously
    token = env("APIFY_TOKEN")
    actor_id = t.get("apify_actor_id") or f"{env('APIFY_USERNAME','fetchsmith')}~{t['slug']}"
    async with httpx.AsyncClient(timeout=300) as cl:
        r = await cl.post(f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items",
                          params={"token": token, "timeout": 240, "memory": t.get("memory_mb", 1024), "clean": "true", "limit": max_results}, json=body)
    if r.status_code >= 300:
        log.error("apify run error %s %s", r.status_code, r.text[:300])
        raise HTTPException(502, "Tool run failed; you were not charged.")
    items = r.json()
    if isinstance(items, dict) and "data" in items:
        items = items["data"]
    n = len(items)
    cost = n * cpr
    with db() as c:
        c.execute("UPDATE credits SET balance=balance-? WHERE customer_id=?", (cost, a["customer_id"]))
        c.execute("INSERT INTO usage(key,tool,results,cost,ts) VALUES(?,?,?,?,?)", (a["key"], slug, n, cost, int(time.time())))
    return {"tool": slug, "results": n, "credits_charged": cost, "credits_left": a["balance"] - cost, "items": items}

@app.get("/{key}.txt", response_class=PlainTextResponse)
def indexnow_key(key: str):
    p = ROOT / "state" / "indexnow.key"
    if p.exists() and p.read_text().strip() == key:
        return key
    raise HTTPException(404)
