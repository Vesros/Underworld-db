import hashlib, json, os, sys, time
SRC = "db_src"
DIST = "dist"
ver = time.strftime("%Y.%m.%d.%H%M")  # or read from CLI
out_dir = os.path.join(DIST, ver)
os.makedirs(out_dir, exist_ok=True)

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1<<20), b""):
            h.update(b)
    return h.hexdigest()

files = []
for name in os.listdir(SRC):
    if not name.endswith(".json"): continue
    src = os.path.join(SRC, name)
    dst = os.path.join(out_dir, name)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(src, "rb") as r, open(dst, "wb") as w:
        w.write(r.read())
    files.append({
        "table": os.path.splitext(name)[0],
        "path": f"{ver}/{name}",
        "sha256": sha256(dst),
        "size": os.path.getsize(dst)
    })

manifest = {"version": ver, "files": files}
with open(os.path.join("dist","manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, separators=(",",":"))
print(ver)
