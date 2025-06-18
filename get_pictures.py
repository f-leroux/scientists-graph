#!/usr/bin/env python3
"""
Download the portrait image for each scientist listed in
`scientists_pre1900_top400.csv` (or another CSV with an `img_url` column).

If you haven’t added `img_url` yet, run the SPARQL snippet from the
previous message first to populate that column.
"""

import os, pathlib, urllib.parse, requests, pandas as pd

# ------------------------------------------------------------------
# 0.  Settings
# ------------------------------------------------------------------
CSV_FILE   = "scientists.csv"   # ← change if needed
OUT_DIR    = pathlib.Path("portraits")
TIMEOUT    = 30     # seconds per HTTP request

HEADERS = {
    # any recent UA string is fine – here’s Chrome 125 on macOS
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_0) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/125.0.0.0 Safari/537.36")
}

OUT_DIR.mkdir(exist_ok=True)
df = pd.read_csv(CSV_FILE)

def safe_filename(text: str) -> str:
    """Turn a slug or name into a filesystem-friendly filename."""
    keep = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")
    return "".join(c if c in keep else "_" for c in text)

# ------------------------------------------------------------------
# 1.  Download loop
# ------------------------------------------------------------------
for _, row in df.iterrows():
    url = row.get("img_url")
    if pd.isna(url) or not isinstance(url, str):
        continue      # no picture → skip

    # derive a filename: prefer the 'slug' col if present, else fall back to name
    base = row.get("slug") or row.get("name") or f"Q{row.get('wd_id')}"
    filename = safe_filename(base)

    # preserve the image extension if it exists, else default to .jpg
    ext = os.path.splitext(urllib.parse.urlparse(url).path)[1]
    if ext.lower() not in {".jpg", ".jpeg", ".png"}:
        ext = ".jpg"
    dest = OUT_DIR / f"{filename}{ext}"

    if dest.exists():
        #print(f"✓ {dest.name} already downloaded")
        continue

    try:
        print(f"⬇  {dest.name}")
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        with open(dest, "wb") as fh:
            fh.write(r.content)
    except Exception as exc:
        print(f"  ⚠  failed for {row.get('name', 'unknown')}: {exc}")

