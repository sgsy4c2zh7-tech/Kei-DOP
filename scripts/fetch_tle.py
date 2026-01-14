import os
import datetime as dt
import urllib.request

BASE = "https://celestrak.org/NORAD/elements/gp.php"

SETS = [
    # 全衛星（かなり大きい）
    {"name": "all", "url": f"{BASE}?GROUP=all&FORMAT=tle", "out_dir": "data/all"},
    # GNSS（DOP用）
    {"name": "gps",     "url": f"{BASE}?GROUP=gps-ops&FORMAT=tle", "out_dir": "data/gnss/gps"},
    {"name": "galileo", "url": f"{BASE}?GROUP=galileo&FORMAT=tle", "out_dir": "data/gnss/galileo"},
    {"name": "glonass", "url": f"{BASE}?GROUP=glonass&FORMAT=tle", "out_dir": "data/gnss/glonass"},
    {"name": "beidou",  "url": f"{BASE}?GROUP=beidou&FORMAT=tle", "out_dir": "data/gnss/beidou"},
    {"name": "qzss",    "url": f"{BASE}?GROUP=qzss&FORMAT=tle", "out_dir": "data/gnss/qzss"},
]

def download_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "kei-dop-daily-tle/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8", errors="replace")

def write_snapshot(out_dir: str, text: str, today: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    latest_path = os.path.join(out_dir, "tle_latest.txt")
    dated_path  = os.path.join(out_dir, f"tle_{today}.txt")

    text = text.strip() + "\n"
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(text)
    with open(dated_path, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    today = dt.date.today().isoformat()
    for s in SETS:
        print(f"[{s['name']}] downloading...")
        text = download_text(s["url"])
        write_snapshot(s["out_dir"], text, today)
        print(f"[{s['name']}] saved -> {s['out_dir']}")

if __name__ == "__main__":
    main()
