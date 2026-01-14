import os, re, json

PAT = re.compile(r"^tle_(\d{4}-\d{2}-\d{2})\.txt$")

def build_one(dir_path: str):
    if not os.path.isdir(dir_path):
        return
    items = []
    for fn in os.listdir(dir_path):
        m = PAT.match(fn)
        if m:
            items.append({"date": m.group(1), "path": f"{dir_path}/{fn}".replace("\\", "/")})
    items.sort(key=lambda x: x["date"])
    out = {
        "latest": f"{dir_path}/tle_latest.txt".replace("\\", "/"),
        "archives": items
    }
    with open(os.path.join(dir_path, "index.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("Wrote", os.path.join(dir_path, "index.json"), "archives:", len(items))

def main():
    targets = [
        "data/all",
        "data/gnss/gps",
        "data/gnss/galileo",
        "data/gnss/glonass",
        "data/gnss/beidou",
        "data/gnss/qzss",
    ]
    for t in targets:
        build_one(t)

if __name__ == "__main__":
    main()
