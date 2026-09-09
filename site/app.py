"""FetchSmith web app: catalog, legal pages, API (keys + credits), Polar checkout/webhooks."""
import os, json, time, secrets, sqlite3, hmac, hashlib, base64, logging
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

app = FastAPI(title="FetchSmith", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=str(ROOT / "site" / "static")), name="static")
tpl = Jinja2Templates(directory=str(ROOT / "site" / "templates"))

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
        """)
init_db()

def load_registry():
    try:
        return json.loads(REGISTRY.read_text()).get("tools", [])
    except Exception:
        return []

def public_tools():
    return [t for t in load_registry() if t.get("status") in ("live", "beta")]

# ---------- lightweight analytics (no cookies) ----------
@app.middleware("http")
async def track(request: Request, call_next):
    resp = await call_next(request)
    p = request.url.path
    if resp.status_code == 200 and not p.startswith(("/static", "/api", "/webhooks", "/health")) and "." not in p.rsplit("/", 1)[-1]:
        try:
            with db() as c:
                c.execute("INSERT INTO pageviews(path,ref,ua,ts) VALUES(?,?,?,?)",
                          (p, request.headers.get("referer", "")[:200], request.headers.get("user-agent", "")[:200], int(time.time())))
        except Exception:
            pass
    return resp

def render(request, name, **ctx):
    ctx.setdefault("site_url", SITE_URL)
    ctx.setdefault("support_email", SUPPORT_EMAIL)
    ctx.setdefault("apify_user", env("APIFY_USERNAME", "hejazi"))
    return tpl.TemplateResponse(request, name, ctx)

# ---------- pages ----------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    tools = public_tools()
    return render(request, "home.html", tools=tools[:12], count=len(tools))

@app.get("/tools", response_class=HTMLResponse)
def tools_page(request: Request):
    return render(request, "tools.html", tools=public_tools())

@app.get("/tools/{slug}", response_class=HTMLResponse)
def tool_page(request: Request, slug: str):
    t = next((t for t in public_tools() if t["slug"] == slug), None)
    if not t:
        raise HTTPException(404)
    return render(request, "tool.html", t=t)

@app.get("/pricing", response_class=HTMLResponse)
def pricing(request: Request):
    return render(request, "pricing.html", packs=CREDIT_PACKS)

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
    return "User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /webhooks/\nSitemap: https://fetchsmith.com/sitemap.xml\n"

@app.get("/llms.txt", response_class=PlainTextResponse)
def llms():
    lines = ["# FetchSmith", "", "> Pay-per-result web data extraction tools: hosted APIs and Apify Actors. No subscription required; buy credits, call an endpoint, get JSON.", "", "## Tools"]
    for t in public_tools():
        lines.append(f"- [{t['title']}]({SITE_URL}/tools/{t['slug']}): {t.get('summary','')}")
    lines += ["", "## Docs", f"- [API docs]({SITE_URL}/docs)", f"- [Pricing]({SITE_URL}/pricing)"]
    return "\n".join(lines) + "\n"

@app.get("/sitemap.xml")
def sitemap():
    urls = ["", "/tools", "/pricing", "/docs", "/about", "/contact", "/terms", "/privacy", "/refunds"] + [f"/tools/{t['slug']}" for t in public_tools()]
    body = "".join(f"<url><loc>{SITE_URL}{u}</loc></url>" for u in urls)
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
        raise HTTPException(503, "Checkout is not configured yet. Email support@fetchsmith.com.")
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
    actor_id = t.get("apify_actor_id") or f"{env('APIFY_USERNAME','hejazi')}~{t['slug']}"
    async with httpx.AsyncClient(timeout=300) as cl:
        r = await cl.post(f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items",
                          params={"token": token, "timeout": 240, "memory": t.get("memory_mb", 256), "clean": "true", "limit": max_results}, json=body)
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
