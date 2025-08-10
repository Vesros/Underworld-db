import json, os, glob

SRC_ROOT = "cms"
OUT_ROOT = "db_src"
MAP = {
    "GameData": ("GameData.json", ["Id","Version","LastPatchDate","BuildType"]),
    "BalanceData": ("BalanceData.json", ["Id","GlobalExpGainModifier","GlobalDamageCausedModifier"]),
}

os.makedirs(OUT_ROOT, exist_ok=True)

for coll, (outfile, allowed) in MAP.items():
    rows = []
    for path in sorted(glob.glob(os.path.join(SRC_ROOT, coll, "*.json"))):
        with open(path, "r", encoding="utf-8") as f:
            obj = json.load(f)
        # keep only known keys, stable field order
        row = {k: obj[k] for k in allowed if k in obj}
        rows.append(row)
    with open(os.path.join(OUT_ROOT, outfile), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, separators=(",",":"))
print("Packed:", ", ".join(k for k in MAP))
