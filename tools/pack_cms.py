import json, os, glob

SRC = "cms"
OUT = "db_src"
MAP = {
  "GameData":     ("GameData.json",     ["Id","Version","LastPatchDate","BuildType"]),
  "BalanceData":  ("BalanceData.json",  ["Id","GlobalExpGainModifier","GlobalDamageCausedModifier"]),
}
os.makedirs(OUT, exist_ok=True)

for coll,(outname,keys) in MAP.items():
    rows=[]
    for p in sorted(glob.glob(os.path.join(SRC,coll,"*.json"))):
        obj=json.load(open(p,"r",encoding="utf-8"))
        rows.append({k:obj[k] for k in keys if k in obj})
    json.dump(rows, open(os.path.join(OUT,outname),"w",encoding="utf-8"),
              ensure_ascii=False, separators=(",",":"))
print("Packed:", ", ".join(MAP.keys()))
