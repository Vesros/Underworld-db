import hashlib, json, os, time

GITHUB_USER = "Vesros"
REPO_NAME   = "Underworld-db"
CDN_FOLDER  = "cdn"

SRC = "db_src"
ver = time.strftime("%Y.%m.%d.%H%M")

out_dir = os.path.join(CDN_FOLDER, ver)
os.makedirs(out_dir, exist_ok=True)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1<<20), b""):
            h.update(b)
    return h.hexdigest()

files = []
for name in sorted(os.listdir(SRC)):
    if not name.lower().endswith(".json"):
        continue
    src = os.path.join(SRC, name)
    dst = os.path.join(out_dir, name)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(src, "rb") as r, open(dst, "wb") as w:
        w.write(r.read())
    url = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@db-{ver}/{CDN_FOLDER}/{ver}/{name}"
    files.append({
        "table": os.path.splitext(name)[0],
        "url": url,
        "sha256": sha256(dst),
        "size": os.path.getsize(dst)
    })

manifest = {"version": ver, "files": files}
with open("manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, separators=(",",":"))

print(ver)
