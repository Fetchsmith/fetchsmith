#!/root/agent/venv/bin/python
"""One-shot: run an Actor fully (not run-sync-get-dataset-items) and print its RUN_SUMMARY KV record.
Usage: bin/_kv_run.py <slug> '<json input>'
"""
import json, sys, time, httpx
env = dict(l.rstrip("\n").split("=", 1) for l in open("/root/agent/secrets/env") if "=" in l and not l.startswith("#"))
T = env["APIFY_TOKEN"]; API = "https://api.apify.com/v2"
user = httpx.get(f"{API}/users/me", headers={"Authorization": f"Bearer {T}"}).json()["data"]["username"]
reg = {t["slug"]: t for t in json.load(open("/root/agent/actors/registry.json"))["tools"]}
slug = sys.argv[1]; inp = json.loads(sys.argv[2])
mem = reg[slug].get("memory_mb", 1024)
r = httpx.post(f"{API}/acts/{user}~{slug}/runs", params={"token": T, "memory": mem}, json=inp, timeout=60)
r.raise_for_status()
run = r.json()["data"]
run_id = run["id"]
print("run started", run_id)
while True:
    time.sleep(5)
    st = httpx.get(f"{API}/actor-runs/{run_id}", params={"token": T}, timeout=30).json()["data"]
    status = st["status"]
    print("status:", status)
    if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
        break
kv_store_id = st["defaultKeyValueStoreId"]
kv = httpx.get(f"{API}/key-value-stores/{kv_store_id}/records/RUN_SUMMARY", params={"token": T}, timeout=30)
print("RUN_SUMMARY:", json.dumps(kv.json(), indent=2))
