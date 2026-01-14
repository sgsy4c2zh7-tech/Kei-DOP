import os
import sys
import datetime as dt
import urllib.request

# 取得元（例：全カタログ系。必要に応じて差し替え）
# CelesTrak GP "active" や "stations" などもある
# https://celestrak.org/NORAD/elements/
CELESTRAK_URL = os.environ.get("TLE_URL", "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle")

def download_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "daily-tle-fetcher/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")

def main():
    today = dt.date.today().isoformat()
    out_dir = os.path.join("data")
    os.makedirs(out_dir, exist_ok=True)

    text = download_text(CELESTRAK_URL).strip() + "\n"

    latest_path = os.path.join(out_dir, "tle_latest.txt")
    dated_path  = os.path.join(out_dir, f"tle_{today}.txt")

    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(text)
    with open(dated_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved: {latest_path}")
    print(f"Saved: {dated_path}")
    print(f"Source: {CELESTRAK_URL}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)
